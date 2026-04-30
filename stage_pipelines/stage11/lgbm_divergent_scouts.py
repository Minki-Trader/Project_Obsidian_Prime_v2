from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from stage_pipelines.stage11 import lgbm_divergent_support as _support

globals().update({name: getattr(_support, name) for name in dir(_support) if not name.startswith("__")})


def run_one_spec(
    *,
    spec: DivergentSpec,
    source_run_root: Path,
    run_root: Path,
    attempt_mt5: bool,
    common_files_root: Path,
    terminal_data_root: Path,
    tester_profile_root: Path,
    terminal_path: Path,
    metaeditor_path: Path,
) -> dict[str, Any]:
    run_output_root = run_root / spec.run_id
    context = scout.build_run_context(
        stage_id=STAGE_ID,
        stage_number=11,
        run_number=spec.run_number,
        run_id=spec.run_id,
        exploration_label=spec.exploration_label,
        output_root=run_output_root,
        common_run_root=f"Project_Obsidian_Prime_v2/stage11/{spec.run_id}",
        common_files_root=common_files_root,
        terminal_data_root=terminal_data_root,
        tester_profile_root=tester_profile_root,
    )
    predictions_root = run_output_root / "predictions"
    models_root = run_output_root / "models"
    mt5_root = run_output_root / "mt5"
    reports_root = run_output_root / "reports"
    _io_path(run_output_root).mkdir(parents=True, exist_ok=True)

    source_summary = read_json(source_run_root / "summary.json")
    base_route_coverage = source_summary["route_coverage"]
    tier_a_source = pd.read_parquet(_io_path(source_run_root / "predictions" / "tier_a_predictions.parquet"))
    tier_b_source = pd.read_parquet(_io_path(source_run_root / "predictions" / "tier_b_predictions.parquet"))

    tier_a_rule = build_rule(tier_a_source, spec=spec, tier_prefix="tier_a", quantile=spec.tier_a_quantile, margin=spec.tier_a_margin)
    tier_b_rule = build_rule(tier_b_source, spec=spec, tier_prefix="tier_b", quantile=spec.tier_b_quantile, margin=spec.tier_b_margin)
    threshold_id = selected_threshold_id(spec, tier_a_rule, tier_b_rule)

    split_specs = {"validation_is": ("2025.01.01", "2025.10.01"), "oos": ("2025.10.01", "2026.04.14")}
    source_tier_a_onnx = source_run_root / "models" / "tier_a_lgbm_58_model.onnx"
    source_tier_b_onnx = source_run_root / "models" / "tier_b_lgbm_core42_model.onnx"
    tier_a_onnx_path = models_root / source_tier_a_onnx.name
    tier_b_onnx_path = models_root / source_tier_b_onnx.name
    source_tier_a_order = source_run_root / "models" / "tier_a_58_feature_order.txt"
    source_tier_b_order = source_run_root / "models" / "tier_b_core42_feature_order.txt"
    tier_a_feature_order_path = models_root / source_tier_a_order.name
    tier_b_feature_order_path = models_root / source_tier_b_order.name
    model_copies = [
        copy_artifact(source_tier_a_onnx, tier_a_onnx_path),
        copy_artifact(source_tier_b_onnx, tier_b_onnx_path),
        copy_artifact(source_tier_a_order, tier_a_feature_order_path),
        copy_artifact(source_tier_b_order, tier_b_feature_order_path),
    ]
    tier_a_feature_order = scout.load_feature_order(_io_path(tier_a_feature_order_path))
    tier_b_feature_order = scout.load_feature_order(_io_path(tier_b_feature_order_path))
    tier_a_feature_hash = scout.ordered_hash(tier_a_feature_order)
    tier_b_feature_hash = scout.ordered_hash(tier_b_feature_order)

    common_copies = [
        scout.copy_to_common_files(common_files_root, tier_a_onnx_path, scout.common_ref("models", tier_a_onnx_path.name, context=context)),
        scout.copy_to_common_files(common_files_root, tier_b_onnx_path, scout.common_ref("models", tier_b_onnx_path.name, context=context)),
    ]
    matrix_records: list[dict[str, Any]] = []
    allowed_by_tier_split: dict[str, dict[str, set[str]]] = {"tier_a": {}, "tier_b": {}}
    mt5_attempts: list[dict[str, Any]] = []
    for split_name, (from_date, to_date) in split_specs.items():
        source_tier_a_matrix = source_run_root / "mt5" / f"tier_a_{split_name}_feature_matrix.csv"
        source_tier_b_matrix = source_run_root / "mt5" / f"tier_b_{split_name}_feature_matrix.csv"
        tier_a_matrix_path = mt5_root / f"tier_a_{split_name}_feature_matrix.csv"
        tier_b_matrix_path = mt5_root / f"tier_b_{split_name}_feature_matrix.csv"
        tier_a_matrix = write_matrix_for_variant(
            source_path=source_tier_a_matrix,
            destination_path=tier_a_matrix_path,
            context_gate=spec.context_gate,
        )
        tier_b_matrix = write_matrix_for_variant(
            source_path=source_tier_b_matrix,
            destination_path=tier_b_matrix_path,
            context_gate=spec.context_gate,
        )
        allowed_by_tier_split["tier_a"][split_name] = set(tier_a_matrix.pop("allowed_timestamps"))
        allowed_by_tier_split["tier_b"][split_name] = set(tier_b_matrix.pop("allowed_timestamps"))
        matrix_records.extend(
            [
                {"tier": scout.TIER_A, "split": split_name, **tier_a_matrix},
                {"tier": scout.TIER_B, "split": split_name, **tier_b_matrix},
            ]
        )
        common_copies.append(scout.copy_to_common_files(common_files_root, tier_a_matrix_path, scout.common_ref("features", tier_a_matrix_path.name, context=context)))
        common_copies.append(scout.copy_to_common_files(common_files_root, tier_b_matrix_path, scout.common_ref("features", tier_b_matrix_path.name, context=context)))
        mt5_attempts.append(
            scout.materialize_mt5_routed_attempt_files(
                run_output_root=run_output_root,
                split_name=split_name,
                primary_onnx_path=tier_a_onnx_path,
                primary_feature_matrix_path=tier_a_matrix_path,
                primary_feature_count=len(tier_a_feature_order),
                primary_feature_order_hash=tier_a_feature_hash,
                fallback_onnx_path=tier_b_onnx_path,
                fallback_feature_matrix_path=tier_b_matrix_path,
                fallback_feature_count=len(tier_b_feature_order),
                fallback_feature_order_hash=tier_b_feature_hash,
                rule=tier_a_rule,
                fallback_rule=tier_b_rule,
                max_hold_bars=RUN01Y_REFERENCE["max_hold_bars"],
                fallback_enabled=True,
                from_date=from_date,
                to_date=to_date,
                context=context,
            )
        )

    tier_a_context_allowed = allowed_by_tier_split["tier_a"] if spec.context_gate else None
    tier_b_context_allowed = allowed_by_tier_split["tier_b"] if spec.context_gate else None
    tier_a_predictions = recompute_predictions(filter_predictions_for_context(tier_a_source, allowed_by_split=tier_a_context_allowed), tier_a_rule)
    tier_b_predictions = recompute_predictions(filter_predictions_for_context(tier_b_source, allowed_by_split=tier_b_context_allowed), tier_b_rule)
    predictions = pd.concat([tier_a_predictions, tier_b_predictions], ignore_index=True)
    _io_path(predictions_root).mkdir(parents=True, exist_ok=True)
    tier_a_predictions_path = predictions_root / "tier_a_predictions.parquet"
    tier_b_predictions_path = predictions_root / "tier_b_predictions.parquet"
    combined_predictions_path = predictions_root / "tier_ab_combined_predictions.parquet"
    tier_a_predictions.to_parquet(_io_path(tier_a_predictions_path), index=False)
    tier_b_predictions.to_parquet(_io_path(tier_b_predictions_path), index=False)
    predictions.to_parquet(_io_path(combined_predictions_path), index=False)

    tier_views = scout.build_tier_prediction_views(predictions)
    tier_outputs = scout.materialize_tier_prediction_views(tier_views, predictions_root)
    tier_records = scout.build_paired_tier_records(
        tier_views,
        run_id=spec.run_id,
        stage_id=STAGE_ID,
        base_path=predictions_root,
        kpi_scope=f"signal_probability_{spec.mode}",
        scoreboard_lane="structural_scout",
        external_verification_status="out_of_scope_by_claim",
    )
    route_coverage = build_route_coverage(
        base_summary=base_route_coverage,
        tier_a_predictions=tier_a_predictions,
        tier_b_predictions=tier_b_predictions,
        spec=spec,
    )
    python_ledger_rows = run02a.build_python_alpha_ledger_rows(
        run_id=spec.run_id,
        tier_records=tier_records,
        selected_threshold_id=threshold_id,
        model_family=MODEL_FAMILY,
    )
    for row in python_ledger_rows:
        row["kpi_scope"] = f"signal_probability_{spec.mode}"
        row["judgment"] = f"inconclusive_{spec.mode}_payload"

    compile_payload: dict[str, Any] | None = None
    mt5_execution_results: list[dict[str, Any]] = []
    if attempt_mt5:
        for attempt in mt5_attempts:
            for output_key in ("common_telemetry_path", "common_summary_path"):
                output_path = common_files_root / Path(str(attempt[output_key]))
                if scout._path_exists(output_path):
                    _io_path(output_path).unlink()
            scout.remove_existing_mt5_report_artifacts(terminal_data_root, attempt, context=context)
        compile_payload = scout.compile_mql5_ea(metaeditor_path, scout.EA_SOURCE_PATH, mt5_root / "mt5_compile.log")
        if compile_payload.get("status") == "completed":
            for attempt in mt5_attempts:
                try:
                    result = scout.run_mt5_tester(
                        terminal_path,
                        Path(attempt["ini"]["path"]),
                        set_path=Path(attempt["set"]["path"]),
                        tester_profile_set_path=tester_profile_root / scout.EA_TESTER_SET_NAME,
                        tester_profile_ini_path=tester_profile_root / scout.mt5_short_profile_ini_name(attempt["tier"], attempt["split"], context=context),
                        timeout_seconds=300,
                    )
                except Exception as exc:  # pragma: no cover - external MT5 boundary
                    result = {"status": "blocked", "blocker": "mt5_tester_exception", "error": repr(exc)}
                result["tier"] = attempt["tier"]
                result["split"] = attempt["split"]
                result["routing_mode"] = attempt["routing_mode"]
                result["ini_path"] = attempt["ini"]["path"]
                result["runtime_outputs"] = (
                    scout.wait_for_mt5_runtime_outputs(common_files_root, attempt, timeout_seconds=180)
                    if result.get("status") == "completed"
                    else scout.validate_mt5_runtime_outputs(common_files_root, attempt)
                )
                if result["runtime_outputs"]["status"] != "completed":
                    result["status"] = "blocked"
                mt5_execution_results.append(result)

    mt5_report_records = (
        scout.collect_mt5_strategy_report_artifacts(
            terminal_data_root=terminal_data_root,
            run_output_root=run_output_root,
            attempts=mt5_attempts,
            context=context,
        )
        if attempt_mt5
        else []
    )
    scout.attach_mt5_report_metrics(mt5_execution_results, mt5_report_records)
    mt5_kpi_records = scout.build_mt5_kpi_records(mt5_execution_results)
    mt5_kpi_records = scout.enrich_mt5_kpi_records_with_route_coverage(mt5_kpi_records, route_coverage)
    expected_mt5_count = len(mt5_attempts) * 3
    mt5_runtime_completed = bool(mt5_execution_results) and all(item.get("status") == "completed" for item in mt5_execution_results)
    mt5_reports_completed = len(mt5_kpi_records) >= expected_mt5_count and all(item.get("status") == "completed" for item in mt5_kpi_records)
    external_status = "completed" if mt5_runtime_completed and mt5_reports_completed else "blocked" if attempt_mt5 else "out_of_scope_by_claim"

    mt5_ledger_rows = run02a.build_mt5_alpha_ledger_rows(
        run_id=spec.run_id,
        mt5_kpi_records=mt5_kpi_records,
        run_output_root=run_output_root,
        external_verification_status=external_status,
    )
    ledger_rows = [*python_ledger_rows, *mt5_ledger_rows]
    ledger_payload = run02a.materialize_ledgers(ledger_rows)
    registry_payload = materialize_run_registry_row(
        spec=spec,
        run_output_root=run_output_root,
        route_coverage=route_coverage,
        tier_records=tier_records,
        mt5_kpi_records=mt5_kpi_records,
        external_verification_status=external_status,
    )

    manifest_path = run_output_root / "run_manifest.json"
    kpi_path = run_output_root / "kpi_record.json"
    summary_path = run_output_root / "summary.json"
    result_summary_path = reports_root / "result_summary.md"
    decision_surface = {
        "decision_surface_id": spec.decision_surface_id,
        "source_run_id": SOURCE_RUN_ID,
        "variant_mode": spec.mode,
        "context_gate": spec.context_gate,
        "tier_a_rule": scout.threshold_rule_payload(tier_a_rule),
        "tier_b_rule": scout.threshold_rule_payload(tier_b_rule),
        "selected_threshold_id": threshold_id,
        "selection_scope": "validation_quantile_then_mt5_routed_probe",
    }
    manifest = {
        "identity": {
            "run_id": spec.run_id,
            "run_number": spec.run_number,
            "stage_id": STAGE_ID,
            "exploration_label": spec.exploration_label,
            "idea_id": spec.idea_id,
            "model_family": MODEL_FAMILY,
            "status": "reviewed_payload",
            "judgment": f"inconclusive_{spec.mode}_mt5_runtime_probe_completed"
            if external_status == "completed"
            else f"inconclusive_{spec.mode}_payload",
        },
        "hypothesis": spec.hypothesis,
        "legacy_relation": "none",
        "tier_scope": "mixed_tier_a_tier_b",
        "broad_sweep": {
            "variant": spec.mode,
            "allowed_side": spec.allowed_side,
            "tier_a_quantile": spec.tier_a_quantile,
            "tier_b_quantile": spec.tier_b_quantile,
            "tier_a_margin": spec.tier_a_margin,
            "tier_b_margin": spec.tier_b_margin,
            "context_gate": spec.context_gate,
        },
        "extreme_sweep": "Single-side variants disable the opposite direction with threshold 1.0; high-confidence variants use upper probability quantiles and larger margins.",
        "micro_search_gate": "Only consider fine search if routed validation and OOS both stop the RUN02A/RUN02B drawdown pattern.",
        "wfo_plan": "explicit_exception_single_window_runtime_probe_first; WFO deferred until a structurally different idea is worth hardening.",
        "failure_memory": "If weak, preserve as negative evidence and reopen only with new label, model family, or context feature.",
        "evidence_boundary": "runtime_probe_only_not_alpha_quality",
        "comparison_reference": RUN01Y_REFERENCE,
        "source_run_id": SOURCE_RUN_ID,
        "decision_surface": decision_surface,
        "route_coverage": route_coverage,
        "tier_records": tier_records,
        "artifacts": [
            {"role": "source_run_manifest", "path": (source_run_root / "run_manifest.json").as_posix(), "sha256": scout.sha256_file(source_run_root / "run_manifest.json")},
            {"role": "tier_a_predictions", "path": tier_a_predictions_path.as_posix(), "format": "parquet", "sha256": scout.sha256_file(tier_a_predictions_path)},
            {"role": "tier_b_predictions", "path": tier_b_predictions_path.as_posix(), "format": "parquet", "sha256": scout.sha256_file(tier_b_predictions_path)},
            {"role": "tier_ab_combined_predictions", "path": combined_predictions_path.as_posix(), "format": "parquet", "sha256": scout.sha256_file(combined_predictions_path)},
            {"role": "copied_models_and_feature_orders", "copies": model_copies},
            {"role": "feature_matrices", "matrices": matrix_records},
            {"role": "mt5_attempts", "attempts": mt5_attempts},
            {"role": "mt5_common_file_copies", "copies": common_copies},
            {"role": "mt5_compile", "compile": compile_payload},
            {"role": "mt5_execution_results", "execution_results": mt5_execution_results},
            {"role": "mt5_strategy_tester_reports", "reports": mt5_report_records},
            {"role": "mt5_runtime_module_hashes", "modules": scout.mt5_runtime_module_hashes()},
            {"role": "tier_prediction_views", "views": tier_outputs},
            {"role": "stage_run_ledger", **ledger_payload["stage_run_ledger"]},
            {"role": "project_alpha_run_ledger", **ledger_payload["project_alpha_run_ledger"]},
            {"role": "project_run_registry", **registry_payload},
        ],
        "mt5": {
            "attempted": bool(attempt_mt5),
            "attempt_policy": "routed_only",
            "compile": compile_payload,
            "execution_results": mt5_execution_results,
            "strategy_tester_reports": mt5_report_records,
            "kpi_records": mt5_kpi_records,
            "runtime_completed": mt5_runtime_completed,
            "reports_completed": mt5_reports_completed,
        },
        "external_verification_status": external_status,
        "boundary": "divergent_runtime_probe_only_not_alpha_quality",
    }
    kpi = {
        "run_id": spec.run_id,
        "stage_id": STAGE_ID,
        "scoreboard_lane": "runtime_probe",
        "kpi_scope": f"signal_probability_{spec.mode}_trading_risk_execution",
        "decision_surface": decision_surface,
        "signal": {"tier_records": tier_records},
        "routing": {"route_coverage": route_coverage, "mt5_kpi_records": mt5_kpi_records},
        "mt5": manifest["mt5"],
        "external_verification_status": external_status,
        "boundary": manifest["boundary"],
    }
    summary = {
        "run_id": spec.run_id,
        "stage_id": STAGE_ID,
        "idea_id": spec.idea_id,
        "status": "reviewed_payload",
        "judgment": manifest["identity"]["judgment"],
        "selected_threshold_id": threshold_id,
        "decision_surface": decision_surface,
        "tier_records": tier_records,
        "mt5_attempted": bool(attempt_mt5),
        "mt5_execution_results": mt5_execution_results,
        "mt5_kpi_records": mt5_kpi_records,
        "ledger_rows": ledger_rows,
        "ledger_payload": ledger_payload,
        "run_registry_payload": registry_payload,
        "external_verification_status": external_status,
        "boundary": manifest["boundary"],
    }
    write_json(manifest_path, manifest)
    write_json(kpi_path, kpi)
    write_json(summary_path, summary)
    write_result_summary(
        path=result_summary_path,
        spec=spec,
        threshold_id=threshold_id,
        tier_records=tier_records,
        mt5_kpi_records=mt5_kpi_records,
        external_status=external_status,
    )

    artifact_scout_label = (
        "salvage-extension LGBM scout" if spec.run_number in {"run02Q", "run02R", "run02S"} else "divergent LGBM scout"
    )
    artifact_rows = [
        {
            "artifact_id": f"stage11_{spec.run_number}_manifest",
            "type": "run_manifest",
            "path": manifest_path.as_posix(),
            "status": "local_generated_reviewed",
            "notes": f"Stage 11 {spec.run_number} {artifact_scout_label}; manifest_sha256 {scout.sha256_file(manifest_path)}; boundary runtime_probe only",
        },
        {
            "artifact_id": f"stage11_{spec.run_number}_kpi_record",
            "type": "kpi_record",
            "path": kpi_path.as_posix(),
            "status": "local_generated_reviewed",
            "notes": f"Stage 11 {spec.run_number} KPI record; kpi_sha256 {scout.sha256_file(kpi_path)}; routed-only MT5 runtime_probe",
        },
        {
            "artifact_id": f"stage11_{spec.run_number}_result_summary",
            "type": "result_summary",
            "path": result_summary_path.as_posix(),
            "status": "local_generated_reviewed",
            "notes": f"Stage 11 {spec.run_number} result summary; summary_sha256 {scout.sha256_file(result_summary_path)}",
        },
    ]
    artifact_payload = append_artifact_rows(artifact_rows)
    return {
        "run_id": spec.run_id,
        "run_number": spec.run_number,
        "idea_id": spec.idea_id,
        "external_verification_status": external_status,
        "summary_path": summary_path.as_posix(),
        "result_summary_path": result_summary_path.as_posix(),
        "mt5_kpi_records": mt5_kpi_records,
        "artifact_payload": artifact_payload,
    }


def main() -> int:
    args = parse_args()
    unknown = [key for key in args.variants if key not in SPECS]
    if unknown:
        raise SystemExit(f"Unknown variants: {unknown}; available={sorted(SPECS)}")
    results = []
    for key in args.variants:
        results.append(
            run_one_spec(
                spec=SPECS[key],
                source_run_root=Path(args.source_run_root),
                run_root=Path(args.run_root),
                attempt_mt5=bool(args.attempt_mt5),
                common_files_root=Path(args.common_files_root),
                terminal_data_root=Path(args.terminal_data_root),
                tester_profile_root=Path(args.tester_profile_root),
                terminal_path=Path(args.terminal_path),
                metaeditor_path=Path(args.metaeditor_path),
            )
        )
    print(json.dumps(scout._json_ready({"status": "ok", "results": results}), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
