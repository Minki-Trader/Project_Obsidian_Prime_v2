from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from stage_pipelines.stage12 import batch20_top_mt5_support as _support

globals().update({name: getattr(_support, name) for name in dir(_support) if not name.startswith("__")})


def run(args: argparse.Namespace) -> dict[str, Any]:
    run_output_root = Path(args.run_output_root)
    for folder in ("models", "predictions", "mt5", "reports"):
        io(run_output_root / folder).mkdir(parents=True, exist_ok=True)
    io(STAGE_ROOT / "03_reviews").mkdir(parents=True, exist_ok=True)
    io(STAGE_ROOT / "04_selected").mkdir(parents=True, exist_ok=True)

    source_variant = load_source_variant()
    feature_order = load_feature_order(Path(args.feature_order_path))
    feature_hash = mt5.ordered_hash(feature_order)
    if feature_hash != FEATURE_ORDER_HASH:
        raise RuntimeError(f"Feature order hash mismatch: {feature_hash} != {FEATURE_ORDER_HASH}")
    frame = pd.read_parquet(io(Path(args.model_input_path)))
    validate_model_input_frame(frame, feature_order)
    if "label_class" not in frame.columns:
        raise RuntimeError("model input is missing label_class")

    train = frame.loc[frame["split"].astype(str).eq("train")].copy()
    validation = frame.loc[frame["split"].astype(str).eq("validation")].copy()
    oos = frame.loc[frame["split"].astype(str).eq("oos")].copy()
    model = ExtraTreesClassifier(**source_variant["model_params"])
    model.fit(train.loc[:, feature_order].to_numpy(dtype="float64", copy=False), train["label_class"].astype("int64").to_numpy())
    if [int(value) for value in model.classes_] != [int(value) for value in LABEL_ORDER]:
        raise RuntimeError(f"Model class order mismatch: {model.classes_}")

    threshold = float(source_variant["threshold"])
    rule = mt5.threshold_rule_from_values(
        threshold_id=f"{SOURCE_VARIANT_ID}_q{float(source_variant['threshold_quantile']):.2f}",
        short_threshold=threshold,
        long_threshold=threshold,
        min_margin=float(source_variant["min_margin"]),
    )
    onnx_path = run_output_root / f"models/{SOURCE_VARIANT_ID}.onnx"
    onnx_export = mt5.export_sklearn_to_onnx_zipmap_disabled(model, onnx_path, feature_count=len(feature_order))
    parity_values = validation.loc[:, feature_order].to_numpy(dtype="float64", copy=False)[: max(1, min(args.parity_rows, len(validation)))]
    onnx_parity = mt5.check_onnxruntime_probability_parity(model, onnx_path, parity_values)

    validation_probs = probability_matrix(model, validation.loc[:, feature_order].to_numpy(dtype="float64", copy=False))
    oos_probs = probability_matrix(model, oos.loc[:, feature_order].to_numpy(dtype="float64", copy=False))
    validation_decisions = decision_frame(validation, validation_probs, threshold, "validation")
    oos_decisions = decision_frame(oos, oos_probs, threshold, "oos")
    python_metrics = {"validation": signal_metrics(validation_decisions), "oos": signal_metrics(oos_decisions)}
    runtime_decision_path = run_output_root / "predictions/runtime_decisions.parquet"
    pd.concat([validation_decisions, oos_decisions], ignore_index=True).to_parquet(io(runtime_decision_path), index=False)

    common_files_root = Path(args.common_files_root)
    terminal_data_root = Path(args.terminal_data_root)
    tester_profile_root = Path(args.tester_profile_root)
    common_copies = [mt5.copy_to_common_files(common_files_root, onnx_path, common_ref("models", onnx_path.name))]
    split_specs = {
        "validation_is": ("validation", validation, *split_date_range(frame, "validation")),
        "oos": ("oos", oos, *split_date_range(frame, "oos")),
    }
    attempts: list[dict[str, Any]] = []
    feature_matrices: dict[str, Any] = {}
    for split_label, (_source_split, split_frame, from_date, to_date) in split_specs.items():
        matrix_path = run_output_root / "mt5" / f"tier_a_only_{split_label}_feature_matrix.csv"
        matrix_payload = mt5.export_mt5_feature_matrix_csv(split_frame, feature_order, matrix_path)
        feature_matrices[split_label] = matrix_payload
        common_copies.append(mt5.copy_to_common_files(common_files_root, matrix_path, common_ref("features", matrix_path.name)))
        attempt = materialize_attempt(
            run_output_root=run_output_root,
            split_name=split_label,
            local_onnx_path=onnx_path,
            local_feature_matrix_path=matrix_path,
            rule=rule,
            feature_count=len(feature_order),
            feature_order_hash=feature_hash,
            from_date=from_date,
            to_date=to_date,
            max_hold_bars=args.max_hold_bars,
        )
        attempt["feature_matrix"] = matrix_payload
        attempts.append(attempt)

    compile_payload: dict[str, Any] | None = None
    execution_results: list[dict[str, Any]] = []
    if args.attempt_mt5:
        for attempt in attempts:
            for key in ("common_telemetry_path", "common_summary_path"):
                output = common_files_root / Path(str(attempt[key]))
                if path_exists(output):
                    io(output).unlink()
            mt5.remove_existing_mt5_report_artifacts(terminal_data_root, attempt)
        compile_payload = mt5.compile_mql5_ea(Path(args.metaeditor_path), mt5.EA_SOURCE_PATH, run_output_root / "mt5/mt5_compile.log")
        if compile_payload["status"] == "completed":
            for attempt in attempts:
                result = mt5.run_mt5_tester(
                    Path(args.terminal_path),
                    Path(attempt["ini"]["path"]),
                    set_path=Path(attempt["set"]["path"]),
                    tester_profile_set_path=tester_profile_root / EA_TESTER_SET_NAME,
                    tester_profile_ini_path=tester_profile_root / tester_profile_ini_name(str(attempt["split"])),
                    timeout_seconds=args.mt5_timeout_seconds,
                )
                result["tier"] = attempt["tier"]
                result["split"] = attempt["split"]
                result["attempt_role"] = attempt["attempt_role"]
                result["record_view_prefix"] = attempt["record_view_prefix"]
                result["ini_path"] = attempt["ini"]["path"]
                result["runtime_outputs"] = mt5.wait_for_mt5_runtime_outputs(common_files_root, attempt, timeout_seconds=args.runtime_output_timeout_seconds)
                if result["runtime_outputs"]["status"] != "completed":
                    result["status"] = "blocked"
                execution_results.append(result)

    report_records = (
        mt5.collect_mt5_strategy_report_artifacts(
            terminal_data_root=terminal_data_root,
            run_output_root=run_output_root,
            attempts=attempts,
        )
        if args.attempt_mt5
        else []
    )
    mt5.attach_mt5_report_metrics(execution_results, report_records)
    mt5_records = mt5.build_mt5_kpi_records(execution_results)
    route_coverage = {
        "by_split": {
            "validation": {"tier_a_primary_rows": int(len(validation)), "routed_labelable_rows": int(len(validation))},
            "oos": {"tier_a_primary_rows": int(len(oos)), "routed_labelable_rows": int(len(oos))},
        },
        "no_tier_by_split": {"validation": 0, "oos": 0},
        "tier_b_fallback_by_split_subtype": {},
    }
    mt5_records = mt5.enrich_mt5_kpi_records_with_route_coverage(mt5_records, route_coverage)
    runtime_completed = bool(args.attempt_mt5) and len(execution_results) == len(attempts) and all(result.get("status") == "completed" for result in execution_results)
    report_completed = len(mt5_records) >= len(attempts) and all(record.get("status") == "completed" for record in mt5_records)
    external_status = "completed" if runtime_completed and report_completed else "blocked" if args.attempt_mt5 else "out_of_scope_by_claim"
    judgment = "inconclusive_run03d_top_variant_mt5_runtime_probe_completed" if external_status == "completed" else "blocked_run03d_top_variant_mt5_runtime_probe"

    summary_path = run_output_root / "summary.json"
    ledger_payload = update_ledgers(run_output_root, mt5_records, execution_results, external_status, summary_path)
    manifest = {
        "identity": {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "exploration_label": EXPLORATION_LABEL,
            "lane": "standalone_batch20_top_mt5_runtime_probe",
            "status": "reviewed" if external_status == "completed" else "blocked",
            "judgment": judgment,
        },
        "source": {
            "run_id": SOURCE_RUN_ID,
            "variant_id": SOURCE_VARIANT_ID,
            "variant_result_path": rel(SOURCE_RUN_ROOT / "results/variant_results.csv"),
            "stage10_11_inheritance": False,
            "stage10_11_baseline": False,
        },
        "model": {
            "family": MODEL_FAMILY,
            "params": source_variant["model_params"],
            "threshold": threshold,
            "threshold_quantile": source_variant["threshold_quantile"],
            "feature_count": len(feature_order),
            "feature_order_hash": feature_hash,
        },
        "python_metrics": python_metrics,
        "onnx_parity": onnx_parity,
        "mt5": {
            "attempted": bool(args.attempt_mt5),
            "external_verification_status": external_status,
            "compile": compile_payload,
            "execution_results": execution_results,
            "strategy_tester_reports": report_records,
            "kpi_records": mt5_records,
            "attempts": attempts,
            "tester_identity": {
                "symbol": "US100",
                "period": "M5",
                "model": 4,
                "deposit": 500,
                "leverage": "1:100",
                "fixed_lot": 0.1,
                "max_hold_bars": int(args.max_hold_bars),
            },
        },
        "artifacts": {
            "onnx": {"path": rel(onnx_path), "sha256": sha256_file(onnx_path), **onnx_export},
            "runtime_decisions": {"path": rel(runtime_decision_path), "sha256": sha256_file(runtime_decision_path)},
            "feature_matrices": feature_matrices,
            "common_copies": common_copies,
            "runtime_module_hashes": mt5.mt5_runtime_module_hashes(),
        },
        "tier_records": {
            "tier_a_separate": "completed" if external_status == "completed" else external_status,
            "tier_b_separate": "out_of_scope_by_claim_standalone_tier_a_only",
            "tier_ab_combined": "out_of_scope_by_claim_standalone_tier_a_only",
        },
        "boundary": "runtime_probe_only_not_alpha_quality_not_live_readiness_not_operating_promotion",
    }
    kpi = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "source_variant_id": SOURCE_VARIANT_ID,
        "python_metrics": python_metrics,
        "onnx_parity": onnx_parity,
        "mt5_records": mt5_records,
        "execution_results": execution_results,
        "external_verification_status": external_status,
        "judgment": judgment,
        "boundary": manifest["boundary"],
    }
    summary = {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "source_variant_id": SOURCE_VARIANT_ID,
        "status": "reviewed" if external_status == "completed" else "blocked",
        "judgment": judgment,
        "external_verification_status": external_status,
        "stage10_11_inheritance": False,
        "stage10_11_baseline": False,
        "python_metrics": python_metrics,
        "onnx_parity": onnx_parity,
        "mt5_kpi_records": mt5_records,
        "ledger_payload": ledger_payload,
        "manifest_path": rel(run_output_root / "run_manifest.json"),
        "kpi_record_path": rel(run_output_root / "kpi_record.json"),
        "result_summary_path": rel(run_output_root / "reports/result_summary.md"),
    }
    write_json(run_output_root / "run_manifest.json", manifest)
    write_json(run_output_root / "kpi_record.json", kpi)
    write_json(summary_path, summary)
    write_reports(run_output_root, source_variant, python_metrics, onnx_parity, mt5_records, external_status)
    update_selection_status(source_variant, mt5_records, external_status)
    update_current_truth(source_variant, mt5_records, external_status, summary_path)
    return {
        "run_id": RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "source_variant_id": SOURCE_VARIANT_ID,
        "external_verification_status": external_status,
        "onnx_parity_passed": onnx_parity.get("passed"),
        "mt5_kpi_record_count": len(mt5_records),
        "summary_path": rel(summary_path),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run MT5 probe for Stage12 RUN03D top ExtraTrees variant.")
    parser.add_argument("--model-input-path", default=str(DEFAULT_MODEL_INPUT_PATH))
    parser.add_argument("--feature-order-path", default=str(DEFAULT_FEATURE_ORDER_PATH))
    parser.add_argument("--run-output-root", default=str(RUN_ROOT))
    parser.add_argument("--common-files-root", default=str(DEFAULT_COMMON_FILES_ROOT))
    parser.add_argument("--terminal-data-root", default=str(DEFAULT_TERMINAL_DATA_ROOT))
    parser.add_argument("--tester-profile-root", default=str(DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-path", default=r"C:\Program Files\MetaTrader 5\terminal64.exe")
    parser.add_argument("--metaeditor-path", default=r"C:\Program Files\MetaTrader 5\MetaEditor64.exe")
    parser.add_argument("--max-hold-bars", type=int, default=12)
    parser.add_argument("--parity-rows", type=int, default=128)
    parser.add_argument("--attempt-mt5", action="store_true")
    parser.add_argument("--mt5-timeout-seconds", type=int, default=300)
    parser.add_argument("--runtime-output-timeout-seconds", type=int, default=600)
    return parser.parse_args()


def main() -> int:
    payload = run(parse_args())
    print(json.dumps(mt5._json_ready(payload), ensure_ascii=False, indent=2))
    return 0 if payload.get("onnx_parity_passed") else 1


if __name__ == "__main__":
    raise SystemExit(main())
