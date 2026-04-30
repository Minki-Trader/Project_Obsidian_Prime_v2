from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from stage_pipelines.stage12 import extratrees_standalone_batch20_support as _support

globals().update({name: getattr(_support, name) for name in dir(_support) if not name.startswith("__")})


def _prepare_dataset() -> tuple[pd.DataFrame, list[str], str, str]:
    if not _exists(DATASET_PATH):
        raise FileNotFoundError(DATASET_PATH)
    if not _exists(FEATURE_ORDER_PATH):
        raise FileNotFoundError(FEATURE_ORDER_PATH)
    dataset_hash = _sha256(DATASET_PATH)
    feature_hash = _sha256(FEATURE_ORDER_PATH)
    frame = pd.read_parquet(io_path(DATASET_PATH))
    feature_order = [
        line.strip()
        for line in _read_text(FEATURE_ORDER_PATH, encoding="utf-8").splitlines()
        if line.strip()
    ]
    missing = [feature for feature in feature_order if feature not in frame.columns]
    if missing:
        raise ValueError(f"missing feature columns: {missing[:5]}")
    required = ["timestamp", "split"]
    missing_required = [col for col in required if col not in frame.columns]
    if missing_required:
        raise ValueError(f"missing required columns: {missing_required}")
    frame = frame.copy()
    if "label_class" in frame.columns:
        frame["label_class"] = frame["label_class"].astype(int)
    elif "label_direction" in frame.columns:
        frame["label_class"] = frame["label_direction"].map(LABEL_TO_CLASS).astype(int)
    else:
        raise ValueError("missing label_class or label_direction")
    if "label_direction" not in frame.columns:
        frame["label_direction"] = frame["label_class"].map(CLASS_TO_LABEL).astype(int)
    return frame, feature_order, dataset_hash, feature_hash


def run() -> dict[str, Any]:
    started_at = _utc_now()
    specs = _variant_specs()
    frame, feature_order, dataset_hash, feature_hash = _prepare_dataset()
    _write_plan(specs, dataset_hash, feature_hash)

    train = frame[frame["split"] == "train"].reset_index(drop=True)
    validation = frame[frame["split"] == "validation"].reset_index(drop=True)
    oos = frame[frame["split"] == "oos"].reset_index(drop=True)
    split_frames = {"train": train, "validation": validation, "oos": oos}
    feature_sets = _resolve_feature_sets(feature_order, train)

    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    io_path(RUN_DIR / "results").mkdir(parents=True, exist_ok=True)
    io_path(RUN_DIR / "predictions").mkdir(parents=True, exist_ok=True)
    io_path(RUN_DIR / "reports").mkdir(parents=True, exist_ok=True)

    model_cache: dict[tuple[str, tuple[str, ...]], ExtraTreesClassifier] = {}
    prob_cache: dict[tuple[str, tuple[str, ...]], dict[str, np.ndarray]] = {}
    result_rows: list[dict[str, Any]] = []
    scored_frames: list[pd.DataFrame] = []

    for spec in specs:
        features = feature_sets[spec.feature_selector]
        feature_key = tuple(features)
        cache_key = (spec.model_key, feature_key)
        if cache_key not in model_cache:
            params = _model_params(spec)
            model = ExtraTreesClassifier(**params)
            model.fit(train[features], train["label_class"].astype(int))
            model_cache[cache_key] = model
            prob_cache[cache_key] = {
                split_name: _ensure_probs(model, split_frame[features])
                for split_name, split_frame in split_frames.items()
            }
        model = model_cache[cache_key]
        probs_by_split = prob_cache[cache_key]
        val_probs = probs_by_split["validation"]
        val_conf = np.maximum(val_probs[:, 0], val_probs[:, 2])
        threshold = float(np.quantile(val_conf, spec.threshold_quantile))

        split_model_metrics = {
            split_name: _split_model_metrics(split_frame["label_class"].astype(int), probs)
            for split_name, split_frame, probs in [
                ("train", train, probs_by_split["train"]),
                ("validation", validation, probs_by_split["validation"]),
                ("oos", oos, probs_by_split["oos"]),
            ]
        }
        split_signal_metrics: dict[str, dict[str, Any]] = {}
        for split_name in ["train", "validation", "oos"]:
            decision = _decision_frame(split_frames[split_name], probs_by_split[split_name], threshold, spec)
            split_signal_metrics[split_name] = _signal_metrics(decision)
            if split_name in {"validation", "oos"}:
                scored_frames.append(decision)

        row: dict[str, Any] = {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "variant_id": spec.variant_id,
            "idea_id": spec.idea_id,
            "hypothesis_ko": spec.hypothesis_ko,
            "model_key": spec.model_key,
            "feature_selector": spec.feature_selector,
            "feature_count": len(features),
            "threshold_quantile": spec.threshold_quantile,
            "threshold": threshold,
            "min_margin": spec.min_margin,
            "direction_mode": spec.direction_mode,
            "model_params_json": json.dumps(_model_params(spec), ensure_ascii=False, sort_keys=True),
            "model_classes": ",".join(CLASS_TO_NAME[int(c)] for c in model.classes_),
        }
        for split_name in ["train", "validation", "oos"]:
            for key, value in split_model_metrics[split_name].items():
                row[f"{split_name}_{key}"] = value
            for key, value in split_signal_metrics[split_name].items():
                row[f"{split_name}_{key}"] = value
        row["package_score"] = _score(split_signal_metrics["validation"], split_signal_metrics["oos"])
        row["candidate_for_mt5_probe"] = bool(
            (row["validation_signal_count"] >= 100)
            and (row["oos_signal_count"] >= 50)
            and ((row["validation_hit_rate"] or 0.0) >= 0.48)
            and ((row["oos_hit_rate"] or 0.0) >= 0.48)
        )
        row["judgment"] = _judge_variant(row)
        result_rows.append(row)

    results = pd.DataFrame(result_rows).sort_values(["package_score", "variant_id"], ascending=[False, True])
    results.to_csv(io_path(RUN_DIR / "results" / "variant_results.csv"), index=False, encoding="utf-8")
    pd.concat(scored_frames, ignore_index=True).to_parquet(
        io_path(RUN_DIR / "predictions" / "scored_validation_oos.parquet"),
        index=False,
    )

    variant_plan = pd.DataFrame(
        [
            {
                "variant_id": spec.variant_id,
                "idea_id": spec.idea_id,
                "hypothesis_ko": spec.hypothesis_ko,
                "model_key": spec.model_key,
                "feature_selector": spec.feature_selector,
                "threshold_quantile": spec.threshold_quantile,
                "min_margin": spec.min_margin,
                "direction_mode": spec.direction_mode,
                "model_params_json": json.dumps(_model_params(spec), ensure_ascii=False, sort_keys=True),
            }
            for spec in specs
        ]
    )
    variant_plan.to_csv(io_path(RUN_DIR / "variant_plan.csv"), index=False, encoding="utf-8")

    candidate_count = int(results["candidate_for_mt5_probe"].sum())
    package_judgment = (
        "candidate_compression_possible_not_runtime"
        if candidate_count > 0
        else "inconclusive_standalone_batch20_structural_scout"
    )
    best = results.iloc[0].to_dict()
    summary = {
        "stage_id": STAGE_ID,
        "run_number": RUN_NUMBER,
        "run_id": RUN_ID,
        "exploration_label": EXPLORATION_LABEL,
        "started_at_utc": started_at,
        "completed_at_utc": _utc_now(),
        "dataset_path": str(DATASET_PATH.relative_to(PROJECT_ROOT)).replace("\\", "/"),
        "dataset_sha256": dataset_hash,
        "feature_order_path": str(FEATURE_ORDER_PATH.relative_to(PROJECT_ROOT)).replace("\\", "/"),
        "feature_order_sha256": feature_hash,
        "variant_count": len(specs),
        "candidate_count": candidate_count,
        "package_judgment": package_judgment,
        "external_verification_status": "out_of_scope_by_claim_standalone_python_structural_scout",
        "standalone_boundary": {
            "stage10_11_inheritance": False,
            "stage10_11_baseline": False,
            "tier_scope": "Tier A only",
            "tier_b_status": "out_of_scope_by_claim_standalone_tier_a_only",
            "tier_ab_status": "out_of_scope_by_claim_standalone_tier_a_only",
        },
        "model_persistence": "not_persisted_batch_scout_reproducible_from_manifest",
        "best_variant": best,
        "artifacts": {
            "plan": str(SPEC_PATH.relative_to(PROJECT_ROOT)).replace("\\", "/"),
            "variant_plan": str((RUN_DIR / "variant_plan.csv").relative_to(PROJECT_ROOT)).replace("\\", "/"),
            "variant_results": str((RUN_DIR / "results" / "variant_results.csv").relative_to(PROJECT_ROOT)).replace("\\", "/"),
            "scored_predictions": str((RUN_DIR / "predictions" / "scored_validation_oos.parquet").relative_to(PROJECT_ROOT)).replace("\\", "/"),
            "summary": str((RUN_DIR / "summary.json").relative_to(PROJECT_ROOT)).replace("\\", "/"),
            "kpi_record": str((RUN_DIR / "kpi_record.json").relative_to(PROJECT_ROOT)).replace("\\", "/"),
            "report": str(REPORT_PATH.relative_to(PROJECT_ROOT)).replace("\\", "/"),
            "review": str(REVIEW_PATH.relative_to(PROJECT_ROOT)).replace("\\", "/"),
        },
    }
    _write_json(RUN_DIR / "summary.json", summary)
    _write_json(
        RUN_DIR / "kpi_record.json",
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "kpi_scope": "standalone_python_batch20_structural_scout",
            "variant_count": len(specs),
            "candidate_count": candidate_count,
            "package_judgment": package_judgment,
            "best_variant": {
                "variant_id": best["variant_id"],
                "validation_signal_count": best["validation_signal_count"],
                "validation_hit_rate": best["validation_hit_rate"],
                "oos_signal_count": best["oos_signal_count"],
                "oos_hit_rate": best["oos_hit_rate"],
                "package_score": best["package_score"],
            },
            "tier_records": {
                "tier_a_separate": "completed",
                "tier_b_separate": "out_of_scope_by_claim_standalone_tier_a_only",
                "tier_ab_combined": "out_of_scope_by_claim_standalone_tier_a_only",
            },
            "external_verification_status": "out_of_scope_by_claim_standalone_python_structural_scout",
        },
    )
    _write_json(
        RUN_DIR / "run_manifest.json",
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
        "command": "python stage_pipelines/stage12/extratrees_standalone_batch20.py",
            "dataset_path": str(DATASET_PATH.relative_to(PROJECT_ROOT)).replace("\\", "/"),
            "dataset_sha256": dataset_hash,
            "feature_order_path": str(FEATURE_ORDER_PATH.relative_to(PROJECT_ROOT)).replace("\\", "/"),
            "feature_order_sha256": feature_hash,
            "variant_count": len(specs),
            "variant_ids": [spec.variant_id for spec in specs],
            "standalone_boundary": summary["standalone_boundary"],
            "external_verification_status": summary["external_verification_status"],
            "created_at_utc": summary["completed_at_utc"],
        },
    )
    _write_reports(summary, results, specs)
    _update_ledgers(summary, results)
    _update_idea_registry(results)
    _update_selection_status(summary, results)
    _update_workspace_state(summary)
    _update_current_working_state(summary)
    _update_changelog(summary)
    return summary


if __name__ == "__main__":
    payload = run()
    print(json.dumps(payload, ensure_ascii=False, indent=2, default=_json_default))
