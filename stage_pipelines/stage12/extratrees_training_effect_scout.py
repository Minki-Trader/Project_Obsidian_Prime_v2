from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from stage_pipelines.stage12 import extratrees_training_effect_support as _support

globals().update({name: getattr(_support, name) for name in dir(_support) if not name.startswith("__")})


def run_stage12_extratrees_training_effect_scout(
    *,
    model_input_path: Path,
    feature_order_path: Path,
    tier_b_reference_model_input_path: Path,
    tier_b_reference_feature_order_path: Path,
    raw_root: Path,
    training_summary_path: Path,
    run_output_root: Path,
    run_id: str,
    run_number: str,
    session_slice_id: str,
    max_hold_bars: int,
    rank_quantile: float,
    tier_a_min_margin: float,
    tier_b_min_margin: float,
    parity_rows: int,
) -> dict[str, Any]:
    if max_hold_bars != 9:
        raise RuntimeError("RUN03A keeps max_hold_bars fixed at 9 for model-family comparison.")

    config = ExtraTreesTrainingConfig()
    tier_a_feature_order = scout.load_feature_order(feature_order_path)
    tier_a_feature_hash = scout.ordered_hash(tier_a_feature_order)
    if tier_a_feature_hash != scout.FEATURE_ORDER_HASH:
        raise RuntimeError(f"Feature order hash mismatch: {tier_a_feature_hash} != {scout.FEATURE_ORDER_HASH}")

    reference_tier_b_features = scout.load_feature_order(tier_b_reference_feature_order_path)
    tier_b_feature_order = list(scout.TIER_B_CORE_FEATURE_ORDER)
    missing_core = sorted(set(tier_b_feature_order).difference(reference_tier_b_features))
    if missing_core:
        raise RuntimeError(f"Tier B core feature order is missing reference features: {missing_core}")
    tier_b_feature_hash = scout.ordered_hash(tier_b_feature_order)

    label_threshold = scout.load_label_threshold(training_summary_path)
    tier_a_frame = pd.read_parquet(_io_path(model_input_path))
    tier_a_frame["timestamp"] = pd.to_datetime(tier_a_frame["timestamp"], utc=True)
    tier_a_frame["route_role"] = scout.ROUTE_ROLE_A_PRIMARY
    tier_a_frame["partial_context_subtype"] = "Tier_A_full_context"
    tier_a_frame["missing_feature_group_mask"] = "none"
    tier_a_frame["available_feature_group_mask"] = "macro|constituent|basket"
    tier_a_frame["tier_a_primary_available"] = True
    tier_a_frame["tier_a_full_feature_ready"] = True
    tier_a_frame["tier_b_core_ready"] = True

    tier_b_context = scout.build_tier_b_partial_context_frames(
        raw_root=raw_root,
        tier_a_frame=tier_a_frame,
        tier_a_feature_order=tier_a_feature_order,
        tier_b_feature_order=tier_b_feature_order,
        label_threshold=label_threshold,
        label_spec=fwd18_label_spec(),
    )
    tier_b_training_frame = tier_b_context["tier_b_training_frame"]
    tier_b_frame = tier_b_context["tier_b_fallback_frame"]
    no_tier_frame = tier_b_context["no_tier_frame"]
    route_coverage_base = tier_b_context["summary"]

    _io_path(run_output_root).mkdir(parents=True, exist_ok=True)
    models_root = run_output_root / "models"
    predictions_root = run_output_root / "predictions"
    sweeps_root = run_output_root / "sweeps"
    reports_root = run_output_root / "reports"
    _io_path(models_root).mkdir(parents=True, exist_ok=True)
    _io_path(predictions_root).mkdir(parents=True, exist_ok=True)
    _io_path(sweeps_root).mkdir(parents=True, exist_ok=True)

    tier_a_model = train_extratrees_model(tier_a_frame, tier_a_feature_order, config)
    tier_b_model = train_extratrees_model(tier_b_training_frame, tier_b_feature_order, config)
    model_metrics = {
        "tier_a": classification_metrics(tier_a_model, tier_a_frame, tier_a_feature_order),
        "tier_b": classification_metrics(tier_b_model, tier_b_training_frame, tier_b_feature_order),
    }

    session_slice = scout.session_slice_payload(session_slice_id)
    tier_a_session = scout.apply_session_slice(tier_a_frame, session_slice)
    tier_b_session = scout.apply_session_slice(tier_b_frame, session_slice)
    no_tier_session = scout.apply_session_slice(no_tier_frame, session_slice)

    tier_a_prob_session = probability_frame(tier_a_model, tier_a_session, tier_a_feature_order)
    tier_b_prob_session = probability_frame(tier_b_model, tier_b_session, tier_b_feature_order)
    tier_a_rule = quantile_rule(
        tier_a_prob_session,
        quantile=rank_quantile,
        min_margin=tier_a_min_margin,
        prefix="tier_a",
    )
    tier_b_rule = quantile_rule(
        tier_b_prob_session,
        quantile=rank_quantile,
        min_margin=tier_b_min_margin,
        prefix="tier_b",
    )
    selected = selected_threshold_id(
        tier_a_rule=tier_a_rule,
        tier_b_rule=tier_b_rule,
        max_hold_bars=max_hold_bars,
        session_slice_id=session_slice_id,
    )

    tier_a_context = apply_context_gate(tier_a_prob_session)
    tier_b_context_eval = apply_context_gate(tier_b_prob_session)
    no_tier_context = apply_context_gate(no_tier_session) if not no_tier_session.empty else no_tier_session.copy()
    route_coverage = scout.build_eval_route_coverage_summary(
        base_summary=route_coverage_base,
        tier_a_eval_frame=tier_a_context,
        tier_b_eval_frame=tier_b_context_eval,
        no_tier_eval_frame=no_tier_context,
        session_slice=session_slice,
    )
    route_coverage["context_gate"] = "di_spread_abs_lte8_adx_lte25"
    route_coverage["note"] = "Session and context filtered structural scout rows; no MT5 PnL."

    tier_a_predictions = build_rank_prediction_frame(tier_a_context, tier_a_rule)
    tier_b_predictions = build_rank_prediction_frame(tier_b_context_eval, tier_b_rule)
    tier_a_predictions[scout.TIER_COLUMN] = scout.TIER_A
    tier_b_predictions[scout.TIER_COLUMN] = scout.TIER_B
    tier_a_predictions["feature_count"] = len(tier_a_feature_order)
    tier_b_predictions["feature_count"] = len(tier_b_feature_order)
    tier_a_predictions["feature_order_hash"] = tier_a_feature_hash
    tier_b_predictions["feature_order_hash"] = tier_b_feature_hash
    combined_predictions = pd.concat([tier_a_predictions, tier_b_predictions], ignore_index=True)

    paths = {
        "tier_a_separate": predictions_root / "tier_a_separate_predictions.parquet",
        "tier_b_separate": predictions_root / "tier_b_separate_predictions.parquet",
        "tier_ab_combined": predictions_root / "tier_ab_combined_predictions.parquet",
        "tier_a_predictions": predictions_root / "tier_a_predictions.parquet",
        "tier_b_predictions": predictions_root / "tier_b_predictions.parquet",
        "no_tier_route_rows": predictions_root / "no_tier_route_rows.parquet",
        "route_coverage_summary": predictions_root / "route_coverage_summary.json",
    }
    tier_a_predictions.to_parquet(_io_path(paths["tier_a_separate"]), index=False)
    tier_b_predictions.to_parquet(_io_path(paths["tier_b_separate"]), index=False)
    combined_predictions.to_parquet(_io_path(paths["tier_ab_combined"]), index=False)
    tier_a_predictions.to_parquet(_io_path(paths["tier_a_predictions"]), index=False)
    tier_b_predictions.to_parquet(_io_path(paths["tier_b_predictions"]), index=False)
    no_tier_context.to_parquet(_io_path(paths["no_tier_route_rows"]), index=False)
    write_json(paths["route_coverage_summary"], route_coverage)

    sweep_a = rank_quantile_sweep(tier_a_prob_session, tier_name=scout.TIER_A)
    sweep_b = rank_quantile_sweep(tier_b_prob_session, tier_name=scout.TIER_B)
    sweep_combined = pd.concat([sweep_a, sweep_b], ignore_index=True)
    sweep_paths = {
        "tier_a": sweeps_root / "rank_quantile_sweep_tier_a.csv",
        "tier_b": sweeps_root / "rank_quantile_sweep_tier_b.csv",
        "combined": sweeps_root / "rank_quantile_sweep_combined.csv",
    }
    sweep_a.to_csv(_io_path(sweep_paths["tier_a"]), index=False)
    sweep_b.to_csv(_io_path(sweep_paths["tier_b"]), index=False)
    sweep_combined.to_csv(_io_path(sweep_paths["combined"]), index=False)

    tier_records = {
        "tier_a_separate": {"tier_scope": scout.TIER_A, "metrics": signal_metrics(tier_a_predictions)},
        "tier_b_separate": {"tier_scope": scout.TIER_B, "metrics": signal_metrics(tier_b_predictions)},
        "tier_ab_combined": {"tier_scope": scout.TIER_AB, "metrics": signal_metrics(combined_predictions)},
    }

    tier_a_model_path = models_root / "tier_a_extratrees_58_model.joblib"
    tier_b_model_path = models_root / "tier_b_extratrees_core42_model.joblib"
    tier_a_feature_order_path = models_root / "tier_a_58_feature_order.txt"
    tier_b_feature_order_path = models_root / "tier_b_core42_feature_order.txt"
    joblib.dump(tier_a_model, _io_path(tier_a_model_path))
    joblib.dump(tier_b_model, _io_path(tier_b_model_path))
    _io_path(tier_a_feature_order_path).write_text("\n".join(tier_a_feature_order) + "\n", encoding="utf-8")
    _io_path(tier_b_feature_order_path).write_text("\n".join(tier_b_feature_order) + "\n", encoding="utf-8")

    tier_a_onnx_path = models_root / "tier_a_extratrees_58_model.onnx"
    tier_b_onnx_path = models_root / "tier_b_extratrees_core42_model.onnx"
    tier_a_onnx_export = scout.export_sklearn_to_onnx_zipmap_disabled(
        tier_a_model,
        tier_a_onnx_path,
        feature_count=len(tier_a_feature_order),
    )
    tier_b_onnx_export = scout.export_sklearn_to_onnx_zipmap_disabled(
        tier_b_model,
        tier_b_onnx_path,
        feature_count=len(tier_b_feature_order),
    )
    tier_a_parity_values = tier_a_session.loc[:, tier_a_feature_order].to_numpy(dtype="float64", copy=False)[
        : max(1, min(parity_rows, len(tier_a_session)))
    ]
    tier_b_parity_values = tier_b_session.loc[:, tier_b_feature_order].to_numpy(dtype="float64", copy=False)[
        : max(1, min(parity_rows, len(tier_b_session)))
    ]
    tier_a_onnx_parity = scout.check_onnxruntime_probability_parity(tier_a_model, tier_a_onnx_path, tier_a_parity_values)
    tier_b_onnx_parity = scout.check_onnxruntime_probability_parity(tier_b_model, tier_b_onnx_path, tier_b_parity_values)
    onnx_parity = {
        "passed": bool(tier_a_onnx_parity["passed"] and tier_b_onnx_parity["passed"]),
        "tier_a": tier_a_onnx_parity,
        "tier_b": tier_b_onnx_parity,
    }

    ledger_rows = build_python_ledger_rows(
        run_id=run_id,
        tier_records=tier_records,
        selected_threshold=selected,
        predictions_root=predictions_root,
    )
    ledger_payload = alpha_run_ledgers.materialize_alpha_ledgers(
        stage_run_ledger_path=STAGE_RUN_LEDGER_PATH,
        project_alpha_ledger_path=PROJECT_ALPHA_LEDGER_PATH,
        rows=ledger_rows,
    )
    run_registry_payload = materialize_run_registry_row(
        run_id=run_id,
        run_output_root=run_output_root,
        combined_metrics=tier_records["tier_ab_combined"]["metrics"],
        selected_threshold=selected,
    )

    stage_docs = materialize_stage_docs(
        run_id=run_id,
        run_output_root=run_output_root,
        selected_threshold=selected,
        tier_records=tier_records,
    )

    artifacts = [
        {"role": "tier_a_extratrees_model", "path": tier_a_model_path.as_posix(), "format": "joblib", "sha256": scout.sha256_file(tier_a_model_path)},
        {"role": "tier_b_extratrees_model", "path": tier_b_model_path.as_posix(), "format": "joblib", "sha256": scout.sha256_file(tier_b_model_path)},
        {"role": "tier_a_feature_order", "path": tier_a_feature_order_path.as_posix(), "format": "txt", "sha256": scout.sha256_file(tier_a_feature_order_path)},
        {"role": "tier_b_feature_order", "path": tier_b_feature_order_path.as_posix(), "format": "txt", "sha256": scout.sha256_file(tier_b_feature_order_path)},
        {"role": "tier_a_onnx_model", **tier_a_onnx_export, "format": "onnx"},
        {"role": "tier_b_onnx_model", **tier_b_onnx_export, "format": "onnx"},
        {"role": "onnx_probability_parity", "parity": onnx_parity},
        {"role": "tier_a_predictions", "path": paths["tier_a_predictions"].as_posix(), "format": "parquet", "sha256": scout.sha256_file(paths["tier_a_predictions"])},
        {"role": "tier_b_predictions", "path": paths["tier_b_predictions"].as_posix(), "format": "parquet", "sha256": scout.sha256_file(paths["tier_b_predictions"])},
        {"role": "tier_ab_combined_predictions", "path": paths["tier_ab_combined"].as_posix(), "format": "parquet", "sha256": scout.sha256_file(paths["tier_ab_combined"])},
        {"role": "route_coverage_summary", "path": paths["route_coverage_summary"].as_posix(), "format": "json", "sha256": scout.sha256_file(paths["route_coverage_summary"])},
        {"role": "rank_quantile_sweep_tier_a", "path": sweep_paths["tier_a"].as_posix(), "format": "csv", "sha256": scout.sha256_file(sweep_paths["tier_a"])},
        {"role": "rank_quantile_sweep_tier_b", "path": sweep_paths["tier_b"].as_posix(), "format": "csv", "sha256": scout.sha256_file(sweep_paths["tier_b"])},
        {"role": "rank_quantile_sweep_combined", "path": sweep_paths["combined"].as_posix(), "format": "csv", "sha256": scout.sha256_file(sweep_paths["combined"])},
        {"role": "stage_run_ledger", **ledger_payload["stage_run_ledger"]},
        {"role": "project_alpha_run_ledger", **ledger_payload["project_alpha_run_ledger"]},
        {"role": "project_run_registry", **run_registry_payload},
        {"role": "stage_docs", "paths": stage_docs},
    ]

    manifest = {
        "identity": {
            "run_id": run_id,
            "run_number": run_number,
            "stage_id": STAGE_ID,
            "exploration_label": EXPLORATION_LABEL,
            "model_family": MODEL_FAMILY,
            "lane": "alpha_model_family_challenger",
            "scoreboard_lane": "structural_scout",
            "status": "completed_payload",
            "judgment": "inconclusive_extratrees_structural_scout_payload",
        },
        "hypothesis": (
            "ExtraTrees can produce a different fwd18 inverse-rank context probability surface than "
            "Stage 10 LogReg and Stage 11 LightGBM while the label, split, session, context, and hold stay fixed."
        ),
        "comparison_references": {
            "stage10": RUN01Y_REFERENCE,
            "stage11": RUN02Z_REFERENCE,
        },
        "experiment_design": {
            "decision_use": "Decide whether a non-LightGBM model-family surface deserves an MT5 runtime_probe.",
            "control_variables": {
                "symbol": "US100",
                "timeframe": "M5",
                "label": "label_v1_fwd18_m5_logret_train_q33_3class",
                "split": "split_v1_calendar_train_20220901_20241231_val_20250101_20250930_oos_20251001_20260413",
                "session_slice_id": session_slice_id,
                "context_gate": "abs(di_spread_14)<=8 and adx_14<=25",
                "decision_mode": "inverse_rank",
                "max_hold_bars": max_hold_bars,
            },
            "changed_variables": {"model_family": MODEL_FAMILY},
            "success_criteria": "Enough validation and OOS structural signals with non-fragile directional hit rates.",
            "failure_criteria": "Too few signals or validation/OOS hit rates that do not support an MT5 runtime_probe.",
            "invalid_conditions": "Feature hash mismatch, missing split, non-finite features, or ONNX parity failure.",
            "stop_conditions": "No operating or promotion claim without MT5 Strategy Tester evidence.",
        },
        "data_integrity": {
            "data_source": model_input_path.as_posix(),
            "time_axis": "broker-derived bar close timestamp normalized as UTC for Python artifacts",
            "sample_scope": "Tier A 58-feature full-context and Tier B core42 partial-context rows in fwd18 split v1",
            "split_boundary": "train < 2025-01-01; validation 2025-01-01..2025-09-30; OOS >= 2025-10-01",
            "feature_label_boundary": "features are closed-bar inputs; fwd18 label uses future close only as target",
            "leakage_risk": "validation-selected rank thresholds can overfit; this run is structural only",
            "data_hash_or_identity": {
                "tier_a_model_input_sha256": scout.sha256_file(model_input_path),
                "tier_a_feature_order_hash": tier_a_feature_hash,
                "tier_b_feature_order_hash": tier_b_feature_hash,
            },
            "integrity_judgment": "usable_with_boundary",
        },
        "model_validation": {
            "model_family": MODEL_FAMILY,
            "target_and_label": "3-class short/flat/long fwd18 log-return label",
            "split_method": "fixed chronological train/validation/OOS",
            "selection_metric": "validation rank quantile threshold with structural directional hit read",
            "secondary_metrics": ["macro_f1", "balanced_accuracy", "signal_count", "signal_coverage", "OOS hit_rate"],
            "threshold_policy": "rank quantile q0.96, inverse signal, context filtered",
            "overfit_risk": "threshold and context inherited from Stage 11; model-family testing still adds multiple-testing risk",
            "calibration_risk": "ExtraTrees probabilities are used as ranks, not calibrated probabilities",
            "comparison_baseline": RUN02Z_REFERENCE["run_id"],
            "validation_judgment": "exploratory",
        },
        "environment_reproducibility": {
            "execution_environment": "local Windows PowerShell with repository Python environment",
            "dependency_surface": "sklearn, pandas, numpy, pyarrow, joblib, skl2onnx, onnxruntime",
            "entry_command": "python stage_pipelines/stage12/extratrees_training_effect_scout.py",
            "local_assumptions": "raw MT5 CSVs and processed fwd18 model input already exist in workspace",
            "clean_checkout_status": "reproducible_with_setup",
            "recovery_instruction": "regenerate fwd18 model input artifacts before rerunning if processed data is missing",
            "reproducibility_judgment": "reproducible_with_setup",
        },
        "threshold": {
            "rank_quantile": rank_quantile,
            "tier_a_rule": scout.threshold_rule_payload(tier_a_rule),
            "tier_b_rule": scout.threshold_rule_payload(tier_b_rule),
            "selected_threshold_id": selected,
            "decision_mode": "inverse",
            "context_gate": "di_spread_abs_lte8_adx_lte25",
        },
        "route_coverage": route_coverage,
        "model_metrics": model_metrics,
        "tier_records": tier_records,
        "onnx_probability_parity": onnx_parity,
        "external_verification_status": "out_of_scope_by_claim",
        "artifacts": artifacts,
        "result_judgment": {
            "result_subject": "Stage 12 RUN03A ExtraTrees fwd18 inverse-rank context structural scout",
            "evidence_available": "Python predictions, model metrics, ONNX parity, rank sweeps, ledgers",
            "evidence_missing": "MT5 Strategy Tester output and trading-risk execution KPI",
            "judgment_label": "inconclusive_extratrees_structural_scout_payload",
            "claim_boundary": "new model training effect observed structurally; no runtime or operating claim",
            "next_condition": "run a narrow MT5 runtime_probe only if the structural read is worth external verification",
            "user_explanation_hook": "새 모델은 학습됐지만 아직 거래 실행 효과는 보지 않았다.",
        },
    }
    kpi_record = {
        "run_id": run_id,
        "stage_id": STAGE_ID,
        "scoreboard_lane": "structural_scout",
        "kpi_scope": "model_training_signal_probability_rank_context",
        "model_metrics": model_metrics,
        "signal": tier_records,
        "threshold": manifest["threshold"],
        "route_coverage": route_coverage,
        "onnx_probability_parity": onnx_parity,
        "external_verification_status": "out_of_scope_by_claim",
        "judgment": manifest["result_judgment"],
    }

    manifest_path = run_output_root / "run_manifest.json"
    kpi_path = run_output_root / "kpi_record.json"
    summary_path = run_output_root / "summary.json"
    result_summary_path = reports_root / "result_summary.md"
    write_json(manifest_path, manifest)
    write_json(kpi_path, kpi_record)
    summary = {
        "run_id": run_id,
        "stage_id": STAGE_ID,
        "status": "completed_payload",
        "judgment": "inconclusive_extratrees_structural_scout_payload",
        "selected_threshold_id": selected,
        "model_family": MODEL_FAMILY,
        "model_metrics": model_metrics,
        "tier_records": tier_records,
        "onnx_probability_parity": onnx_parity,
        "external_verification_status": "out_of_scope_by_claim",
        "paths": {
            "run_manifest": manifest_path.as_posix(),
            "kpi_record": kpi_path.as_posix(),
            "summary": summary_path.as_posix(),
            "result_summary": result_summary_path.as_posix(),
            **stage_docs,
        },
    }
    write_json(summary_path, summary)
    write_result_summary(
        result_summary_path,
        run_id=run_id,
        selected_threshold=selected,
        model_metrics=model_metrics,
        tier_records=tier_records,
        onnx_parity=onnx_parity,
    )

    return {
        "status": "ok",
        "run_id": run_id,
        "stage_id": STAGE_ID,
        "selected_threshold_id": selected,
        "summary_path": summary_path.as_posix(),
        "result_summary_path": result_summary_path.as_posix(),
        "manifest_path": manifest_path.as_posix(),
        "kpi_path": kpi_path.as_posix(),
        "combined_signal_metrics": tier_records["tier_ab_combined"]["metrics"],
        "onnx_probability_parity": onnx_parity,
        "external_verification_status": "out_of_scope_by_claim",
    }


def main() -> int:
    args = parse_args()
    payload = run_stage12_extratrees_training_effect_scout(
        model_input_path=Path(args.model_input_path),
        feature_order_path=Path(args.feature_order_path),
        tier_b_reference_model_input_path=Path(args.tier_b_reference_model_input_path),
        tier_b_reference_feature_order_path=Path(args.tier_b_reference_feature_order_path),
        raw_root=Path(args.raw_root),
        training_summary_path=Path(args.training_summary_path),
        run_output_root=Path(args.run_output_root),
        run_id=args.run_id,
        run_number=args.run_number,
        session_slice_id=args.session_slice_id,
        max_hold_bars=args.max_hold_bars,
        rank_quantile=args.rank_quantile,
        tier_a_min_margin=args.tier_a_min_margin,
        tier_b_min_margin=args.tier_b_min_margin,
        parity_rows=args.parity_rows,
    )
    print(json.dumps(scout._json_ready(payload), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
