from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from stage_pipelines.stage11 import lgbm_rank_threshold_support as _support

globals().update({name: getattr(_support, name) for name in dir(_support) if not name.startswith("__")})


def run_stage11_lgbm_rank_threshold_scout(
    *,
    source_run_root: Path,
    run_output_root: Path,
    run_id: str,
    run_number: str,
    exploration_label: str,
    source_run_id: str,
    decision_surface_id: str,
    selection_policy: str,
    run_registry_lane: str,
    judgment_prefix: str,
    hypothesis: str,
    max_hold_bars: int,
    session_slice_id: str,
    tier_a_quantile: float,
    tier_a_min_margin: float,
    tier_b_quantile: float,
    tier_b_min_margin: float,
    invert_decisions: bool,
    context_gate: str | None,
    routed_fallback_enabled: bool,
    attempt_mt5: bool,
    common_files_root: Path,
    terminal_data_root: Path,
    tester_profile_root: Path,
    terminal_path: Path,
    metaeditor_path: Path,
) -> dict[str, Any]:
    if max_hold_bars != RUN01Y_REFERENCE["max_hold_bars"]:
        raise RuntimeError("Rank threshold scout keeps run01Y max_hold_bars fixed for threshold-only comparison.")
    if session_slice_id not in scout.SESSION_SLICE_DEFINITIONS:
        raise RuntimeError(f"Unknown session slice id: {session_slice_id}")
    routing_mode = scout.ROUTING_MODE_A_B_FALLBACK if routed_fallback_enabled else scout.ROUTING_MODE_A_ONLY

    scout.configure_run_identity(
        run_number=run_number,
        run_id=run_id,
        exploration_label=exploration_label,
        common_run_root=f"Project_Obsidian_Prime_v2/stage11/{run_id}",
        stage_id=STAGE_ID,
    )
    _io_path(run_output_root).mkdir(parents=True, exist_ok=True)
    predictions_root = run_output_root / "predictions"
    sweeps_root = run_output_root / "sweeps"
    models_root = run_output_root / "models"
    mt5_root = run_output_root / "mt5"
    reports_root = run_output_root / "reports"

    source_summary = read_json(source_run_root / "summary.json")
    base_route_coverage = source_summary["route_coverage"]
    split_specs = {
        "validation_is": ("2025.01.01", "2025.10.01"),
        "oos": ("2025.10.01", "2026.04.14"),
    }
    tier_a_source = pd.read_parquet(_io_path(source_run_root / "predictions" / "tier_a_predictions.parquet"))
    tier_b_source = pd.read_parquet(_io_path(source_run_root / "predictions" / "tier_b_predictions.parquet"))
    tier_a_allowed_by_split = {
        split_name: allowed_timestamps_from_feature_matrix(
            source_run_root / "mt5" / f"tier_a_{split_name}_feature_matrix.csv",
            context_gate,
        )
        for split_name in split_specs
    }
    tier_b_allowed_by_split = {
        split_name: allowed_timestamps_from_feature_matrix(
            source_run_root / "mt5" / f"tier_b_{split_name}_feature_matrix.csv",
            context_gate,
        )
        for split_name in split_specs
    }

    tier_a_rule = quantile_rule(
        tier_a_source,
        split_name="validation",
        quantile=tier_a_quantile,
        min_margin=tier_a_min_margin,
        prefix="tier_a",
    )
    tier_b_rule = quantile_rule(
        tier_b_source,
        split_name="validation",
        quantile=tier_b_quantile,
        min_margin=tier_b_min_margin,
        prefix="tier_b",
    )
    selected_threshold_id = (
        f"a_{tier_a_rule.threshold_id}__b_{tier_b_rule.threshold_id}"
        f"__hold{max_hold_bars}__slice_{session_slice_id}__model_lgbm_rank_target"
        f"{'_inverse' if invert_decisions else ''}"
        f"{'__ctx_' + context_gate if context_gate else ''}"
    )

    tier_a_predictions = recompute_predictions(tier_a_source, tier_a_rule, invert_decisions=invert_decisions)
    tier_b_predictions = recompute_predictions(tier_b_source, tier_b_rule, invert_decisions=invert_decisions)
    if context_gate is not None:
        tier_a_predictions = divergent.filter_predictions_for_context(
            tier_a_predictions,
            allowed_by_split=tier_a_allowed_by_split,
        )
        tier_b_predictions = divergent.filter_predictions_for_context(
            tier_b_predictions,
            allowed_by_split=tier_b_allowed_by_split,
        )
    predictions = pd.concat([tier_a_predictions, tier_b_predictions], ignore_index=True)
    route_coverage = (
        scout.build_eval_route_coverage_summary(
            base_summary=base_route_coverage,
            tier_a_eval_frame=tier_a_predictions,
            tier_b_eval_frame=tier_b_predictions,
            no_tier_eval_frame=tier_a_predictions.iloc[0:0].copy(),
            session_slice=None,
        )
        if context_gate is not None
        else base_route_coverage
    )

    _io_path(predictions_root).mkdir(parents=True, exist_ok=True)
    tier_a_predictions_path = predictions_root / "tier_a_predictions.parquet"
    tier_b_predictions_path = predictions_root / "tier_b_predictions.parquet"
    combined_predictions_path = predictions_root / "tier_ab_combined_predictions.parquet"
    tier_a_predictions.to_parquet(_io_path(tier_a_predictions_path), index=False)
    tier_b_predictions.to_parquet(_io_path(tier_b_predictions_path), index=False)
    predictions.to_parquet(_io_path(combined_predictions_path), index=False)

    _io_path(sweeps_root).mkdir(parents=True, exist_ok=True)
    quantiles = (0.80, 0.85, 0.90, 0.94, 0.96, 0.98, 0.99)
    margins = (0.00, 0.02, 0.05, 0.08, 0.12)
    tier_a_sweep = quantile_sweep(tier_a_source, tier_name=scout.TIER_A, quantiles=quantiles, margins=margins, invert_decisions=invert_decisions)
    tier_b_sweep = quantile_sweep(tier_b_source, tier_name=scout.TIER_B, quantiles=quantiles, margins=margins, invert_decisions=invert_decisions)
    tier_a_sweep_path = sweeps_root / "rank_quantile_sweep_tier_a.csv"
    tier_b_sweep_path = sweeps_root / "rank_quantile_sweep_tier_b.csv"
    combined_sweep_path = sweeps_root / "rank_quantile_sweep_combined.csv"
    tier_a_sweep.to_csv(_io_path(tier_a_sweep_path), index=False)
    tier_b_sweep.to_csv(_io_path(tier_b_sweep_path), index=False)
    pd.concat([tier_a_sweep, tier_b_sweep], ignore_index=True).to_csv(_io_path(combined_sweep_path), index=False)

    tier_views = scout.build_tier_prediction_views(predictions)
    tier_outputs = scout.materialize_tier_prediction_views(tier_views, predictions_root)
    tier_records = scout.build_paired_tier_records(
        tier_views,
        run_id=run_id,
        stage_id=STAGE_ID,
        base_path=predictions_root,
        kpi_scope="signal_probability_rank_target_threshold",
        scoreboard_lane="structural_scout",
        external_verification_status="out_of_scope_by_claim",
    )
    python_ledger_rows = run02a.build_python_alpha_ledger_rows(
        run_id=run_id,
        tier_records=tier_records,
        selected_threshold_id=selected_threshold_id,
        model_family=MODEL_FAMILY,
    )
    for row in python_ledger_rows:
        row["kpi_scope"] = "signal_probability_rank_target_threshold"
        row["judgment"] = "inconclusive_lgbm_rank_threshold_payload"

    source_tier_a_onnx = source_run_root / "models" / "tier_a_lgbm_58_model.onnx"
    source_tier_b_onnx = source_run_root / "models" / "tier_b_lgbm_core42_model.onnx"
    tier_a_onnx_path = models_root / source_tier_a_onnx.name
    tier_b_onnx_path = models_root / source_tier_b_onnx.name
    model_copies = [
        copy_artifact(source_tier_a_onnx, tier_a_onnx_path),
        copy_artifact(source_tier_b_onnx, tier_b_onnx_path),
    ]
    source_tier_a_order = source_run_root / "models" / "tier_a_58_feature_order.txt"
    source_tier_b_order = source_run_root / "models" / "tier_b_core42_feature_order.txt"
    tier_a_feature_order_path = models_root / source_tier_a_order.name
    tier_b_feature_order_path = models_root / source_tier_b_order.name
    model_copies.extend(
        [
            copy_artifact(source_tier_a_order, tier_a_feature_order_path),
            copy_artifact(source_tier_b_order, tier_b_feature_order_path),
        ]
    )
    tier_a_feature_order = scout.load_feature_order(_io_path(tier_a_feature_order_path))
    tier_b_feature_order = scout.load_feature_order(_io_path(tier_b_feature_order_path))
    tier_a_feature_hash = scout.ordered_hash(tier_a_feature_order)
    tier_b_feature_hash = scout.ordered_hash(tier_b_feature_order)

    mt5_attempts: list[dict[str, Any]] = []
    common_copies: list[dict[str, Any]] = []
    _io_path(mt5_root).mkdir(parents=True, exist_ok=True)
    common_copies.append(scout.copy_to_common_files(common_files_root, tier_a_onnx_path, scout.common_ref("models", tier_a_onnx_path.name)))
    common_copies.append(scout.copy_to_common_files(common_files_root, tier_b_onnx_path, scout.common_ref("models", tier_b_onnx_path.name)))

    copied_feature_matrices: list[dict[str, Any]] = []
    for split_name, (from_date, to_date) in split_specs.items():
        source_tier_a_matrix = source_run_root / "mt5" / f"tier_a_{split_name}_feature_matrix.csv"
        source_tier_b_matrix = source_run_root / "mt5" / f"tier_b_{split_name}_feature_matrix.csv"
        tier_a_matrix_path = mt5_root / source_tier_a_matrix.name
        tier_b_matrix_path = mt5_root / source_tier_b_matrix.name
        copied_feature_matrices.extend(
            [
                {"tier": scout.TIER_A, "split": split_name, **copy_or_filter_feature_matrix(source_tier_a_matrix, tier_a_matrix_path, context_gate)},
                {"tier": scout.TIER_B, "split": split_name, **copy_or_filter_feature_matrix(source_tier_b_matrix, tier_b_matrix_path, context_gate)},
            ]
        )
        common_copies.append(scout.copy_to_common_files(common_files_root, tier_a_matrix_path, scout.common_ref("features", tier_a_matrix_path.name)))
        common_copies.append(scout.copy_to_common_files(common_files_root, tier_b_matrix_path, scout.common_ref("features", tier_b_matrix_path.name)))
        attempt = scout.materialize_mt5_routed_attempt_files(
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
            invert_signal=bool(invert_decisions),
            fallback_invert_signal=bool(invert_decisions),
            max_hold_bars=max_hold_bars,
            fallback_enabled=bool(routed_fallback_enabled),
            from_date=from_date,
            to_date=to_date,
        )
        mt5_attempts.append(attempt)

    compile_payload: dict[str, Any] | None = None
    mt5_execution_results: list[dict[str, Any]] = []
    if attempt_mt5:
        for attempt in mt5_attempts:
            for common_output_key in ("common_telemetry_path", "common_summary_path"):
                output_path = common_files_root / Path(str(attempt[common_output_key]))
                if scout._path_exists(output_path):
                    _io_path(output_path).unlink()
            scout.remove_existing_mt5_report_artifacts(terminal_data_root, attempt)
        compile_payload = scout.compile_mql5_ea(metaeditor_path, scout.EA_SOURCE_PATH, mt5_root / "mt5_compile.log")
        if compile_payload["status"] == "completed":
            for attempt in mt5_attempts:
                try:
                    result = scout.run_mt5_tester(
                        terminal_path,
                        Path(attempt["ini"]["path"]),
                        set_path=Path(attempt["set"]["path"]),
                        tester_profile_set_path=tester_profile_root / scout.EA_TESTER_SET_NAME,
                        tester_profile_ini_path=tester_profile_root / scout.mt5_short_profile_ini_name(attempt["tier"], attempt["split"]),
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
        )
        if attempt_mt5
        else []
    )
    scout.attach_mt5_report_metrics(mt5_execution_results, mt5_report_records)
    mt5_kpi_records = scout.build_mt5_kpi_records(mt5_execution_results)
    mt5_kpi_records = scout.enrich_mt5_kpi_records_with_route_coverage(mt5_kpi_records, route_coverage)
    expected_mt5_kpi_record_count = sum(
        3 if attempt.get("routing_mode") == scout.ROUTING_MODE_A_B_FALLBACK else 2 for attempt in mt5_attempts
    )
    mt5_runtime_completed = bool(mt5_execution_results) and all(item.get("status") == "completed" for item in mt5_execution_results)
    mt5_reports_completed = len(mt5_kpi_records) >= expected_mt5_kpi_record_count and all(
        item.get("status") == "completed" for item in mt5_kpi_records
    )
    external_status = (
        "completed"
        if mt5_runtime_completed and mt5_reports_completed
        else "blocked"
        if attempt_mt5
        else "out_of_scope_by_claim"
    )

    mt5_ledger_rows = run02a.build_mt5_alpha_ledger_rows(
        run_id=run_id,
        mt5_kpi_records=mt5_kpi_records,
        run_output_root=run_output_root,
        external_verification_status=external_status,
    )
    ledger_rows = [*python_ledger_rows, *mt5_ledger_rows]
    ledger_payload = run02a.materialize_ledgers(ledger_rows)
    run_registry_payload = materialize_run_registry_row(
        run_id=run_id,
        run_output_root=run_output_root,
        route_coverage=route_coverage,
        tier_records=tier_records,
        external_verification_status=external_status,
        mt5_kpi_records=mt5_kpi_records,
        decision_surface_id=decision_surface_id,
        lane=run_registry_lane,
        judgment_prefix=judgment_prefix,
        invert_decisions=bool(invert_decisions),
        context_gate=context_gate,
        session_slice_id=session_slice_id,
        routing_mode=routing_mode,
    )

    manifest_path = run_output_root / "run_manifest.json"
    kpi_path = run_output_root / "kpi_record.json"
    summary_path = run_output_root / "summary.json"
    result_summary_path = reports_root / "result_summary.md"
    artifacts = [
        {"role": "source_run_manifest", "path": (source_run_root / "run_manifest.json").as_posix(), "sha256": scout.sha256_file(source_run_root / "run_manifest.json")},
        {"role": "tier_a_predictions", "path": tier_a_predictions_path.as_posix(), "format": "parquet", "sha256": scout.sha256_file(tier_a_predictions_path)},
        {"role": "tier_b_predictions", "path": tier_b_predictions_path.as_posix(), "format": "parquet", "sha256": scout.sha256_file(tier_b_predictions_path)},
        {"role": "tier_ab_combined_predictions", "path": combined_predictions_path.as_posix(), "format": "parquet", "sha256": scout.sha256_file(combined_predictions_path)},
        {"role": "tier_a_rank_quantile_sweep", "path": tier_a_sweep_path.as_posix(), "format": "csv", "sha256": scout.sha256_file(tier_a_sweep_path)},
        {"role": "tier_b_rank_quantile_sweep", "path": tier_b_sweep_path.as_posix(), "format": "csv", "sha256": scout.sha256_file(tier_b_sweep_path)},
        {"role": "combined_rank_quantile_sweep", "path": combined_sweep_path.as_posix(), "format": "csv", "sha256": scout.sha256_file(combined_sweep_path)},
        {"role": "copied_source_models_and_feature_orders", "copies": model_copies},
        {"role": "copied_feature_matrices", "copies": copied_feature_matrices},
        {"role": "mt5_attempts", "attempts": mt5_attempts},
        {"role": "mt5_common_file_copies", "copies": common_copies},
        {"role": "mt5_compile", "compile": compile_payload},
        {"role": "mt5_execution_results", "execution_results": mt5_execution_results},
        {"role": "mt5_strategy_tester_reports", "reports": mt5_report_records},
        {"role": "mt5_runtime_module_hashes", "modules": scout.mt5_runtime_module_hashes()},
        {"role": "tier_prediction_views", "views": tier_outputs},
        {"role": "stage_run_ledger", **ledger_payload["stage_run_ledger"]},
        {"role": "project_alpha_run_ledger", **ledger_payload["project_alpha_run_ledger"]},
        {"role": "project_run_registry", **run_registry_payload},
    ]
    decision_surface = {
        "decision_surface_id": decision_surface_id,
        "selection_policy": selection_policy,
        "source_run_id": source_run_id,
        "decision_direction_mode": "inverse" if invert_decisions else "normal",
        "context_gate": context_gate,
        "tier_a_rule": scout.threshold_rule_payload(tier_a_rule),
        "tier_b_rule": scout.threshold_rule_payload(tier_b_rule),
        "selected_threshold_id": selected_threshold_id,
        "broad_sweep": {
            "quantiles": list(quantiles),
            "margins": list(margins),
            "selection_scope": "validation_only",
            "mt5_attempt_policy": routing_mode,
            "invert_decisions": bool(invert_decisions),
        },
    }
    manifest = {
        "identity": {
            "run_id": run_id,
            "run_number": run_number,
            "stage_id": STAGE_ID,
            "exploration_label": exploration_label,
            "model_family": MODEL_FAMILY,
            "status": "reviewed_payload",
            "judgment": (
                f"inconclusive_{judgment_prefix}_mt5_runtime_probe_completed"
                if external_status == "completed"
                else f"inconclusive_{judgment_prefix}_payload"
            ),
        },
        "hypothesis": hypothesis,
        "comparison_reference": RUN01Y_REFERENCE,
        "source_run_id": source_run_id,
        "decision_surface": decision_surface,
        "route_coverage": route_coverage,
        "tier_records": tier_records,
        "artifacts": artifacts,
        "mt5": {
            "attempted": bool(attempt_mt5),
            "attempt_policy": routing_mode,
            "fallback_enabled": bool(routed_fallback_enabled),
            "compile": compile_payload,
            "execution_results": mt5_execution_results,
            "strategy_tester_reports": mt5_report_records,
            "kpi_records": mt5_kpi_records,
            "runtime_completed": mt5_runtime_completed,
            "reports_completed": mt5_reports_completed,
        },
        "external_verification_status": external_status,
        "boundary": "lgbm_rank_threshold_runtime_probe_only_not_alpha_quality",
    }
    kpi = {
        "run_id": run_id,
        "stage_id": STAGE_ID,
        "scoreboard_lane": "runtime_probe",
        "kpi_scope": "signal_probability_rank_target_threshold_trading_risk_execution",
        "decision_surface": decision_surface,
        "signal": {"tier_records": tier_records},
        "routing": {"route_coverage": route_coverage, "mt5_kpi_records": mt5_kpi_records},
        "mt5": manifest["mt5"],
        "external_verification_status": external_status,
        "boundary": manifest["boundary"],
    }
    summary = {
        "run_id": run_id,
        "stage_id": STAGE_ID,
        "status": "reviewed_payload",
        "judgment": manifest["identity"]["judgment"],
        "selected_threshold_id": selected_threshold_id,
        "decision_surface": decision_surface,
        "tier_records": tier_records,
        "mt5_attempted": bool(attempt_mt5),
        "mt5_execution_results": mt5_execution_results,
        "mt5_kpi_records": mt5_kpi_records,
        "ledger_rows": ledger_rows,
        "ledger_payload": ledger_payload,
        "run_registry_payload": run_registry_payload,
        "external_verification_status": external_status,
        "boundary": manifest["boundary"],
    }
    write_json(manifest_path, manifest)
    write_json(kpi_path, kpi)
    write_json(summary_path, summary)
    write_result_summary(
        path=result_summary_path,
        run_id=run_id,
        run_number=run_number,
        source_run_id=source_run_id,
        decision_direction_mode="inverse" if invert_decisions else "normal",
        context_gate=context_gate,
        selected_threshold_id=selected_threshold_id,
        tier_records=tier_records,
        mt5_kpi_records=mt5_kpi_records,
        external_status=external_status,
        routing_mode=routing_mode,
    )

    return {
        "status": "ok",
        "run_id": run_id,
        "run_output_root": run_output_root.as_posix(),
        "selected_threshold_id": selected_threshold_id,
        "external_verification_status": external_status,
        "mt5_attempted": bool(attempt_mt5),
        "mt5_kpi_records": mt5_kpi_records,
        "summary_path": summary_path.as_posix(),
        "manifest_path": manifest_path.as_posix(),
        "kpi_path": kpi_path.as_posix(),
        "result_summary_path": result_summary_path.as_posix(),
        "ledger_payload": ledger_payload,
        "run_registry_payload": run_registry_payload,
    }


def main() -> int:
    args = parse_args()
    payload = run_stage11_lgbm_rank_threshold_scout(
        source_run_root=Path(args.source_run_root),
        run_output_root=Path(args.run_output_root),
        run_id=args.run_id,
        run_number=args.run_number,
        exploration_label=args.exploration_label,
        source_run_id=args.source_run_id,
        decision_surface_id=args.decision_surface_id,
        selection_policy=args.selection_policy,
        run_registry_lane=args.run_registry_lane,
        judgment_prefix=args.judgment_prefix,
        hypothesis=args.hypothesis,
        max_hold_bars=args.max_hold_bars,
        session_slice_id=args.session_slice_id,
        tier_a_quantile=args.tier_a_quantile,
        tier_a_min_margin=args.tier_a_min_margin,
        tier_b_quantile=args.tier_b_quantile,
        tier_b_min_margin=args.tier_b_min_margin,
        invert_decisions=bool(args.invert_decisions),
        context_gate=args.context_gate,
        routed_fallback_enabled=not bool(args.disable_routed_fallback),
        attempt_mt5=bool(args.attempt_mt5),
        common_files_root=Path(args.common_files_root),
        terminal_data_root=Path(args.terminal_data_root),
        tester_profile_root=Path(args.tester_profile_root),
        terminal_path=Path(args.terminal_path),
        metaeditor_path=Path(args.metaeditor_path),
    )
    print(json.dumps(scout._json_ready(payload), indent=2))
    return 0 if payload["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
