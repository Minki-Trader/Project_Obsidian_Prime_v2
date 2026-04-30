from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from stage_pipelines.stage12 import extratrees_standalone_mt5_support as _support

globals().update({name: getattr(_support, name) for name in dir(_support) if not name.startswith("__")})


def run(args: argparse.Namespace) -> dict[str, Any]:
    mt5.configure_run_identity(
        run_number=RUN_NUMBER,
        run_id=RUN_ID,
        exploration_label=EXPLORATION_LABEL,
        common_run_root=COMMON_RUN_ROOT,
        stage_id=STAGE_ID,
    )
    run_output_root = Path(args.run_output_root)
    for path in (
        run_output_root / "models",
        run_output_root / "predictions",
        run_output_root / "mt5",
        run_output_root / "reports",
        STAGE_ROOT / "03_reviews",
        STAGE_ROOT / "04_selected",
    ):
        io(path).mkdir(parents=True, exist_ok=True)

    source_summary = load_json(SOURCE_RUN_ROOT / "summary.json")
    source_threshold = load_json(SOURCE_RUN_ROOT / "threshold_rule.json")
    require_standalone_source(source_summary, source_threshold)

    feature_order = load_feature_order(args.feature_order_path)
    feature_hash = mt5.ordered_hash(feature_order)
    if feature_hash != FEATURE_ORDER_HASH:
        raise RuntimeError(f"Feature order hash mismatch: {feature_hash} != {FEATURE_ORDER_HASH}")

    frame = pd.read_parquet(io(Path(args.model_input_path)))
    validate_model_input_frame(frame, feature_order)
    model = joblib.load(io(SOURCE_RUN_ROOT / "models/model.joblib"))
    if [int(value) for value in model.classes_] != [int(value) for value in LABEL_ORDER]:
        raise RuntimeError(f"Model class order mismatch: {model.classes_}")

    threshold = float(source_threshold["nonflat_confidence_threshold"])
    rule = mt5.threshold_rule_from_values(
        threshold_id=f"standalone_nonflat_q90_short{threshold:.6f}_long{threshold:.6f}_margin0",
        short_threshold=threshold,
        long_threshold=threshold,
        min_margin=0.0,
    )

    onnx_path = run_output_root / "models/run03B_extratrees_standalone.onnx"
    onnx_export = mt5.export_sklearn_to_onnx_zipmap_disabled(
        model,
        onnx_path,
        feature_count=len(feature_order),
    )

    validation_frame = frame.loc[frame["split"].astype(str).eq("validation")].copy()
    oos_frame = frame.loc[frame["split"].astype(str).eq("oos")].copy()
    validation_values = validation_frame.loc[:, feature_order].to_numpy(dtype="float64", copy=False)
    oos_values = oos_frame.loc[:, feature_order].to_numpy(dtype="float64", copy=False)
    parity_values = validation_values[: max(1, min(args.parity_rows, len(validation_values)))]
    onnx_parity = mt5.check_onnxruntime_probability_parity(model, onnx_path, parity_values)

    validation_probs = mt5.ordered_sklearn_probabilities(model, validation_values)
    oos_probs = mt5.ordered_sklearn_probabilities(model, oos_values)
    python_metrics = {
        "validation": decision_metrics(validation_frame, validation_probs, threshold),
        "oos": decision_metrics(oos_frame, oos_probs, threshold),
    }
    runtime_decisions = pd.concat(
        [
            build_runtime_decision_frame(validation_frame, validation_probs, threshold, "validation"),
            build_runtime_decision_frame(oos_frame, oos_probs, threshold, "oos"),
        ],
        ignore_index=True,
    )
    runtime_decision_path = run_output_root / "predictions/runtime_decisions.parquet"
    runtime_decisions.to_parquet(io(runtime_decision_path), index=False)

    common_files_root = Path(args.common_files_root)
    terminal_data_root = Path(args.terminal_data_root)
    tester_profile_root = Path(args.tester_profile_root)
    common_copies = [
        mt5.copy_to_common_files(common_files_root, onnx_path, common_ref("models", onnx_path.name))
    ]
    split_specs = {
        "validation_is": ("validation", *split_date_range(frame, "validation")),
        "oos": ("oos", *split_date_range(frame, "oos")),
    }
    attempts: list[dict[str, Any]] = []
    feature_matrices: dict[str, dict[str, Any]] = {}
    for split_label, (source_split, from_date, to_date) in split_specs.items():
        split_frame = frame.loc[frame["split"].astype(str).eq(source_split)].copy()
        matrix_path = run_output_root / "mt5" / f"tier_a_only_{split_label}_feature_matrix.csv"
        matrix_payload = mt5.export_mt5_feature_matrix_csv(split_frame, feature_order, matrix_path)
        feature_matrices[split_label] = matrix_payload
        common_copies.append(
            mt5.copy_to_common_files(common_files_root, matrix_path, common_ref("features", matrix_path.name))
        )
        attempt = materialize_stage12_mt5_attempt(
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
    mt5_execution_results: list[dict[str, Any]] = []
    if args.attempt_mt5:
        for attempt in attempts:
            for common_output_key in ("common_telemetry_path", "common_summary_path"):
                output_path = common_files_root / Path(str(attempt[common_output_key]))
                if path_exists(output_path):
                    io(output_path).unlink()
            mt5.remove_existing_mt5_report_artifacts(terminal_data_root, attempt)
        compile_payload = mt5.compile_mql5_ea(
            Path(args.metaeditor_path),
            mt5.EA_SOURCE_PATH,
            run_output_root / "mt5/mt5_compile.log",
        )
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
                result["runtime_outputs"] = mt5.wait_for_mt5_runtime_outputs(
                    common_files_root,
                    attempt,
                    timeout_seconds=args.runtime_output_timeout_seconds,
                )
                if result["runtime_outputs"]["status"] != "completed":
                    result["status"] = "blocked"
                mt5_execution_results.append(result)

    mt5_report_records = (
        mt5.collect_mt5_strategy_report_artifacts(
            terminal_data_root=terminal_data_root,
            run_output_root=run_output_root,
            attempts=attempts,
        )
        if args.attempt_mt5
        else []
    )
    mt5.attach_mt5_report_metrics(mt5_execution_results, mt5_report_records)
    mt5_kpi_records = mt5.build_mt5_kpi_records(mt5_execution_results)
    route_coverage = {
        "by_split": {
            "validation": {"tier_a_primary_rows": int(len(validation_frame)), "routed_labelable_rows": int(len(validation_frame))},
            "oos": {"tier_a_primary_rows": int(len(oos_frame)), "routed_labelable_rows": int(len(oos_frame))},
        },
        "no_tier_by_split": {"validation": 0, "oos": 0},
        "tier_b_fallback_by_split_subtype": {},
    }
    mt5_kpi_records = mt5.enrich_mt5_kpi_records_with_route_coverage(mt5_kpi_records, route_coverage)
    mt5_module_hashes = mt5.mt5_runtime_module_hashes()
    expected_kpi_count = len(attempts)
    runtime_completed = bool(args.attempt_mt5) and len(mt5_execution_results) == len(attempts) and all(
        result.get("status") == "completed" for result in mt5_execution_results
    )
    report_completed = len(mt5_kpi_records) >= expected_kpi_count and all(
        record.get("status") == "completed" for record in mt5_kpi_records
    )
    external_status = (
        "completed"
        if runtime_completed and report_completed
        else "blocked"
        if args.attempt_mt5
        else "out_of_scope_by_claim"
    )

    artifacts = [
        {"role": "source_run03b_model", "path": rel(SOURCE_RUN_ROOT / "models/model.joblib"), "sha256": sha256_file(SOURCE_RUN_ROOT / "models/model.joblib")},
        {"role": "stage12_extratrees_onnx", **onnx_export, "format": "onnx"},
        {"role": "runtime_decisions", "path": rel(runtime_decision_path), "sha256": sha256_file(runtime_decision_path)},
        {"role": "mt5_attempts", "attempts": attempts},
        {"role": "mt5_common_file_copies", "copies": common_copies},
        {"role": "mt5_feature_matrices", "matrices": feature_matrices},
        {"role": "mt5_runtime_module_hashes", "modules": mt5_module_hashes},
        {"role": "mt5_strategy_tester_reports", "reports": mt5_report_records},
    ]
    manifest = {
        "identity": {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "exploration_label": EXPLORATION_LABEL,
            "lane": "standalone_mt5_runtime_probe",
            "scoreboard_lane": "runtime_probe",
            "model_family": MODEL_FAMILY,
            "status": "reviewed" if external_status == "completed" else "blocked",
            "judgment": (
                "inconclusive_standalone_extratrees_mt5_runtime_probe_completed"
                if external_status == "completed"
                else "blocked_standalone_extratrees_mt5_runtime_probe"
            ),
        },
        "source_python_run": {
            "run_id": SOURCE_RUN_ID,
            "path": rel(SOURCE_RUN_ROOT),
            "standalone_scope": True,
            "stage10_11_inheritance": False,
        },
        "experiment_design": {
            "hypothesis": "RUN03B standalone ExtraTrees can be checked in MT5 without Stage 10/11 thresholds, sessions, contexts, or comparison baselines.",
            "decision_use": "Observe standalone trading-risk execution behavior, not promotion.",
            "comparison_baseline": None,
            "control_variables": {
                "symbol": "US100",
                "timeframe": "M5",
                "dataset": MODEL_INPUT_DATASET_ID,
                "feature_set": FEATURE_SET_ID,
                "label": "label_v1_fwd12_m5_logret_train_q33_3class",
            },
            "changed_variables": {"runtime_handoff": "ONNX plus MT5 RuntimeProbeEA"},
            "invalid_conditions": "ONNX parity failure, MT5 compile failure, terminal run failure, or runtime telemetry missing",
        },
        "non_inheritance_guardrail": {
            "stage10_threshold_used": False,
            "stage10_session_slice_used": False,
            "stage11_lightgbm_surface_used": False,
            "stage11_fwd18_inverse_context_used": False,
            "comparison_reference_used": False,
        },
        "threshold_rule": {
            "source_method": THRESHOLD_METHOD,
            "source_threshold": source_threshold,
            "mt5_surface": mt5.threshold_rule_payload(rule),
        },
        "onnx_parity": onnx_parity,
        "mt5": {
            "attempted": bool(args.attempt_mt5),
            "external_verification_status": external_status,
            "compile": compile_payload,
            "execution_results": mt5_execution_results,
            "strategy_tester_reports": mt5_report_records,
            "kpi_records": mt5_kpi_records,
            "attempts": attempts,
            "tester_defaults": {
                "symbol": "US100",
                "period": "M5",
                "model": 4,
                "deposit": 500,
                "leverage": "1:100",
                "fixed_lot": 0.1,
                "max_hold_bars": int(args.max_hold_bars),
                "max_concurrent_positions": 1,
            },
        },
        "tier_records": {
            "tier_a_separate": {"status": "attempted", "record_views": ["mt5_tier_a_only_validation_is", "mt5_tier_a_only_oos"]},
            "tier_b_separate": {"status": "not_produced", "judgment": "out_of_scope_by_claim_standalone_tier_a_only"},
            "tier_ab_combined": {"status": "not_produced", "judgment": "out_of_scope_by_claim_standalone_tier_a_only"},
        },
        "artifacts": artifacts,
        "boundary": "standalone MT5 runtime_probe only; not alpha quality, live readiness, runtime authority expansion, or operating promotion",
    }
    kpi = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "kpi_scope": "standalone_mt5_runtime_probe",
        "source_python_metrics": python_metrics,
        "onnx_parity": onnx_parity,
        "mt5": {
            "scoreboard_lane": "runtime_probe",
            "external_verification_status": external_status,
            "kpi_records": mt5_kpi_records,
            "execution_results": mt5_execution_results,
            "strategy_tester_reports": mt5_report_records,
        },
        "judgment": manifest["identity"]["judgment"],
        "boundary": manifest["boundary"],
    }
    manifest_path = run_output_root / "run_manifest.json"
    kpi_path = run_output_root / "kpi_record.json"
    summary_path = run_output_root / "summary.json"
    write_json(manifest_path, manifest)
    write_json(kpi_path, kpi)
    ledger_payload = update_ledgers_and_registry(
        run_output_root=run_output_root,
        mt5_kpi_records=mt5_kpi_records,
        execution_results=mt5_execution_results,
        external_status=external_status,
        summary_path=summary_path,
    )
    summary = {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "source_python_run_id": SOURCE_RUN_ID,
        "status": manifest["identity"]["status"],
        "judgment": manifest["identity"]["judgment"],
        "standalone_scope": True,
        "stage10_11_inheritance": False,
        "comparison_baseline": None,
        "external_verification_status": external_status,
        "onnx_parity": onnx_parity,
        "python_runtime_decision_metrics": python_metrics,
        "mt5_kpi_records": mt5_kpi_records,
        "mt5_execution_results": mt5_execution_results,
        "ledger_payload": ledger_payload,
        "manifest_path": rel(manifest_path),
        "kpi_record_path": rel(kpi_path),
        "result_summary_path": rel(run_output_root / "reports/result_summary.md"),
        "boundary": manifest["boundary"],
    }
    write_json(summary_path, summary)
    write_stage12_docs(
        external_status=external_status,
        threshold=threshold,
        python_metrics=python_metrics,
        onnx_parity=onnx_parity,
        mt5_kpi_records=mt5_kpi_records,
        compile_payload=compile_payload,
        run_output_root=run_output_root,
        summary_path=summary_path,
    )
    update_current_truth_docs(
        external_status=external_status,
        threshold=threshold,
        python_metrics=python_metrics,
        mt5_kpi_records=mt5_kpi_records,
        run_output_root=run_output_root,
        summary_path=summary_path,
    )
    return {
        "status": "ok" if onnx_parity.get("passed") else "failed",
        "run_id": RUN_ID,
        "external_verification_status": external_status,
        "onnx_parity_passed": onnx_parity.get("passed"),
        "summary_path": rel(summary_path),
        "mt5_kpi_record_count": len(mt5_kpi_records),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Stage 12 standalone ExtraTrees MT5 runtime probe.")
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
    return 0 if payload["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
