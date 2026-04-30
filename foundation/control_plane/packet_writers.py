from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd

from foundation.alpha.decision_views import TIER_A, TIER_AB, TIER_B, select_threshold_from_sweep
from foundation.control_plane import alpha_run_ledgers

from foundation.mt5.runtime_artifacts import sha256_file, write_json


def build_alpha_run_manifest_payload(
    *,
    run_id: str,
    run_number: str,
    stage_id: str,
    exploration_label: str,
    input_refs: Mapping[str, Any],
    artifacts: Sequence[Mapping[str, Any]],
    threshold_selection: Mapping[str, Any],
    tier_records: Sequence[Mapping[str, Any]],
    onnx_parity: Mapping[str, Any],
    external_verification_status: str = "out_of_scope_by_claim",
    model_family: str = "sklearn_logistic_regression_multiclass",
    lane: str = "single_split_scout",
    scoreboard_lane: str = "structural_scout",
) -> dict[str, Any]:
    return {
        "identity": {
            "run_id": run_id,
            "run_number": run_number,
            "stage_id": stage_id,
            "exploration_label": exploration_label,
            "lane": lane,
            "scoreboard_lane": scoreboard_lane,
            "model_family": model_family,
        },
        "inputs": dict(input_refs),
        "artifacts": list(artifacts),
        "threshold": dict(threshold_selection),
        "tier_pair_records": list(tier_records),
        "onnx_probability_parity": dict(onnx_parity),
        "external_verification_status": external_verification_status,
        "judgment_boundary": {
            "status": "payload_generated_not_reviewed",
            "claim": "single_split_scout_payload_only",
            "not_claimed": [
                "alpha_quality",
                "live_readiness",
                "runtime_authority_expansion",
                "operating_promotion",
            ],
        },
    }


def build_alpha_kpi_record_payload(
    *,
    run_id: str,
    stage_id: str,
    threshold_sweep: pd.DataFrame,
    threshold_sweeps: Mapping[str, pd.DataFrame] | None = None,
    tier_records: Sequence[Mapping[str, Any]],
    onnx_parity: Mapping[str, Any],
    mt5_kpi_records: Sequence[Mapping[str, Any]] | None = None,
    primary_tier: str = TIER_A,
    fallback_tier: str = TIER_B,
) -> dict[str, Any]:
    best = select_threshold_from_sweep(threshold_sweep) if not threshold_sweep.empty else {}
    mt5_kpi_records = list(mt5_kpi_records or [])
    return {
        "run_id": run_id,
        "stage_id": stage_id,
        "scoreboard_lane": "runtime_probe",
        "kpi_scope": "signal_probability_threshold_trading_risk_execution",
        "signal": {
            "tier_pair_records": [
                {
                    "record_view": record.get("record_view"),
                    "tier_scope": record.get("tier_scope"),
                    "signal_count": record.get("metrics", {}).get("signal_count"),
                    "short_count": record.get("metrics", {}).get("short_count"),
                    "long_count": record.get("metrics", {}).get("long_count"),
                    "signal_coverage": record.get("metrics", {}).get("signal_coverage"),
                }
                for record in tier_records
            ],
        },
        "probability": {
            "onnx_probability_parity_passed": onnx_parity.get("passed"),
            "onnx_probability_max_abs_diff": onnx_parity.get("max_abs_diff"),
            "row_sum_guardrail": [
                {
                    "record_view": record.get("record_view"),
                    "tier_scope": record.get("tier_scope"),
                    "probability_row_sum_max_abs_error": record.get("metrics", {}).get("probability_row_sum_max_abs_error"),
                }
                for record in tier_records
            ],
        },
        "threshold": {
            "selection_scope": "validation_is_routed_tier_a_primary_tier_b_fallback_only",
            "selected_threshold_id": best.get("threshold_id"),
            "directional_hit_rate": best.get("directional_hit_rate"),
            "coverage": best.get("coverage"),
            "sweeps": {
                view: {
                    "rows": int(len(sweep)),
                    "best": select_threshold_from_sweep(sweep) if not sweep.empty else {},
                }
                for view, sweep in (threshold_sweeps or {"tier_ab_combined": threshold_sweep}).items()
            },
        },
        "routing": {
            "routing_mode": "tier_a_primary_tier_b_fallback",
            "primary_tier": primary_tier,
            "fallback_tier": fallback_tier,
            "route_source_required": True,
            "fallback_reason_required": True,
            "records": [
                {
                    "record_view": record.get("record_view"),
                    "tier_scope": record.get("tier_scope"),
                    "split": record.get("split"),
                    "route_role": record.get("route_role"),
                    "aggregation": record.get("metrics", {}).get("aggregation"),
                    "profit_attribution": record.get("metrics", {}).get("profit_attribution"),
                    "route_bar_count": record.get("metrics", {}).get("route_bar_count"),
                    "route_share": record.get("metrics", {}).get("route_share"),
                    "partial_context_subtype_counts": record.get("metrics", {}).get("partial_context_subtype_counts"),
                    "no_tier_labelable_rows": record.get("metrics", {}).get("no_tier_labelable_rows"),
                    "routed_labelable_rows": record.get("metrics", {}).get("routed_labelable_rows"),
                }
                for record in mt5_kpi_records
            ],
        },
        "trading": [
            {
                "record_view": record.get("record_view"),
                "tier_scope": record.get("tier_scope"),
                "split": record.get("split"),
                "net_profit": record.get("metrics", {}).get("net_profit"),
                "profit_factor": record.get("metrics", {}).get("profit_factor"),
                "expectancy": record.get("metrics", {}).get("expectancy"),
                "trade_count": record.get("metrics", {}).get("trade_count"),
                "win_rate_percent": record.get("metrics", {}).get("win_rate_percent"),
            }
            for record in mt5_kpi_records
        ],
        "risk": [
            {
                "record_view": record.get("record_view"),
                "tier_scope": record.get("tier_scope"),
                "split": record.get("split"),
                "max_drawdown_amount": record.get("metrics", {}).get("max_drawdown_amount"),
                "max_drawdown_percent": record.get("metrics", {}).get("max_drawdown_percent"),
                "recovery_factor": record.get("metrics", {}).get("recovery_factor"),
            }
            for record in mt5_kpi_records
        ],
        "execution": [
            {
                "record_view": record.get("record_view"),
                "tier_scope": record.get("tier_scope"),
                "split": record.get("split"),
                "fill_count": record.get("metrics", {}).get("fill_count"),
                "reject_count": record.get("metrics", {}).get("reject_count"),
                "skip_count": record.get("metrics", {}).get("skip_count"),
                "fill_rate": record.get("metrics", {}).get("fill_rate"),
            }
            for record in mt5_kpi_records
        ],
        "judgment_read": {
            "judgment": "inconclusive_single_split_scout_mt5_routed_completed" if mt5_kpi_records else "inconclusive_payload_only",
            "boundary": "runtime_probe only; not live readiness, runtime authority expansion, or operating promotion.",
            "mt5_record_count": len(mt5_kpi_records),
        },
        "tier_pair_records": list(tier_records),
    }


def materialize_manifest_and_kpi(
    output_root: Path,
    *,
    manifest_payload: Mapping[str, Any],
    kpi_payload: Mapping[str, Any],
) -> dict[str, Any]:
    manifest_path = output_root / "run_manifest.json"
    kpi_path = output_root / "kpi_record.json"
    write_json(manifest_path, manifest_payload)
    write_json(kpi_path, kpi_payload)
    return {
        "run_manifest": {"path": manifest_path.as_posix(), "sha256": sha256_file(manifest_path)},
        "kpi_record": {"path": kpi_path.as_posix(), "sha256": sha256_file(kpi_path)},
    }


def materialize_alpha_scout_run_outputs(
    *,
    run_id: str,
    run_number: str,
    stage_id: str,
    exploration_label: str,
    run_output_root: Path,
    reports_root: Path,
    model_input_path: Path,
    feature_order_path: Path,
    stage07_model_path: Path,
    tier_b_model_input_path: Path,
    tier_b_feature_order_path: Path,
    tier_a_model_path: Path,
    tier_b_model_path: Path,
    tier_a_predictions_path: Path,
    tier_b_predictions_path: Path,
    no_tier_route_path: Path,
    route_coverage_path: Path,
    combined_predictions_path: Path,
    tier_b_feature_order_path_run: Path,
    threshold_sweep_path: Path,
    threshold_sweep_paths: Mapping[str, Path],
    tier_a_onnx_export: Mapping[str, Any],
    tier_b_onnx_export: Mapping[str, Any],
    tier_outputs: Mapping[str, Any],
    model_input_dataset_id: str,
    feature_set_id: str,
    tier_b_model_input_dataset_id: str,
    tier_b_feature_set_id: str,
    tier_b_partial_context_dataset_id: str,
    tier_b_partial_context_feature_set_id: str,
    tier_b_partial_context_policy_id: str,
    tier_a_feature_order: Sequence[str],
    tier_b_feature_order: Sequence[str],
    tier_a_feature_hash: str,
    tier_b_feature_hash: str,
    route_coverage: Mapping[str, Any],
    threshold_selection: Mapping[str, Any],
    threshold_sweep: pd.DataFrame,
    threshold_sweeps: Mapping[str, pd.DataFrame],
    tier_records: Sequence[Mapping[str, Any]],
    onnx_parity: Mapping[str, Any],
    mt5_attempts: Sequence[Mapping[str, Any]],
    common_copies: Sequence[Mapping[str, Any]],
    mt5_report_records: Sequence[Mapping[str, Any]],
    mt5_kpi_records: Sequence[Mapping[str, Any]],
    mt5_module_hashes: Sequence[Mapping[str, Any]],
    compile_payload: Mapping[str, Any] | None,
    mt5_execution_results: Sequence[Mapping[str, Any]],
    attempt_mt5: bool,
    max_hold_bars: int,
    routed_fallback_enabled: bool,
    routing_mode: str,
    routing_detail: str,
    allowed_fallback_subtypes: Sequence[str],
    session_slice_id: str | None,
    tier_a_predictions_count: int,
    tier_b_predictions_count: int,
    no_tier_eval_count: int,
    tier_a_rule: Any,
    tier_b_rule: Any,
    stage_run_ledger_path: Path,
    project_alpha_ledger_path: Path,
    run_registry_path: Path,
    tier_a_only_prefix: str = "mt5_tier_a_only",
    tier_b_fallback_only_prefix: str = "mt5_tier_b_fallback_only",
    tier_a: str = TIER_A,
    tier_b: str = TIER_B,
    tier_ab: str = TIER_AB,
) -> dict[str, Any]:
    artifacts: list[dict[str, Any]] = [
        {"role": "tier_a_sklearn_model", "path": tier_a_model_path.as_posix(), "format": "joblib", "sha256": sha256_file(tier_a_model_path)},
        {"role": "tier_b_sklearn_model", "path": tier_b_model_path.as_posix(), "format": "joblib", "sha256": sha256_file(tier_b_model_path)},
        {"role": "tier_a_predictions", "path": tier_a_predictions_path.as_posix(), "format": "parquet", "sha256": sha256_file(tier_a_predictions_path)},
        {"role": "tier_b_predictions", "path": tier_b_predictions_path.as_posix(), "format": "parquet", "sha256": sha256_file(tier_b_predictions_path)},
        {"role": "no_tier_route_rows", "path": no_tier_route_path.as_posix(), "format": "parquet", "sha256": sha256_file(no_tier_route_path)},
        {"role": "route_coverage_summary", "path": route_coverage_path.as_posix(), "format": "json", "sha256": sha256_file(route_coverage_path)},
        {"role": "combined_predictions", "path": combined_predictions_path.as_posix(), "format": "parquet", "sha256": sha256_file(combined_predictions_path)},
        {"role": "tier_b_core42_feature_order", "path": tier_b_feature_order_path_run.as_posix(), "format": "txt", "sha256": sha256_file(tier_b_feature_order_path_run)},
        {"role": "threshold_sweep", "path": threshold_sweep_path.as_posix(), "format": "csv", "sha256": sha256_file(threshold_sweep_path)},
        *[
            {
                "role": f"threshold_sweep_{view_name}",
                "path": path.as_posix(),
                "format": "csv",
                "sha256": sha256_file(path),
            }
            for view_name, path in threshold_sweep_paths.items()
        ],
        {"role": "tier_a_onnx_model", **dict(tier_a_onnx_export), "format": "onnx"},
        {"role": "tier_b_onnx_model", **dict(tier_b_onnx_export), "format": "onnx"},
        {"role": "mt5_attempts", "attempts": list(mt5_attempts)},
        {"role": "mt5_common_file_copies", "copies": list(common_copies)},
        {"role": "mt5_runtime_module_hashes", "modules": list(mt5_module_hashes)},
        {"role": "mt5_strategy_tester_reports", "reports": list(mt5_report_records)},
        {"role": "tier_prediction_views", "views": dict(tier_outputs)},
    ]
    input_refs = {
        "tier_a": {
            "model_input_dataset_id": model_input_dataset_id,
            "feature_set_id": feature_set_id,
            "model_input_path": model_input_path.as_posix(),
            "model_input_sha256": sha256_file(model_input_path),
            "feature_order_path": feature_order_path.as_posix(),
            "feature_order_sha256": sha256_file(feature_order_path),
            "feature_count": len(tier_a_feature_order),
            "feature_order_hash": tier_a_feature_hash,
            "source_model_path": stage07_model_path.as_posix(),
            "source_model_sha256": sha256_file(stage07_model_path),
        },
        "tier_b": {
            "model_input_dataset_id": tier_b_partial_context_dataset_id,
            "feature_set_id": tier_b_partial_context_feature_set_id,
            "model_input_path": "materialized_in_run_from_raw_feature_frame_and_label_contract",
            "model_input_sha256": None,
            "feature_order_path": tier_b_feature_order_path_run.as_posix(),
            "feature_order_sha256": sha256_file(tier_b_feature_order_path_run),
            "feature_count": len(tier_b_feature_order),
            "feature_order_hash": tier_b_feature_hash,
            "policy_id": tier_b_partial_context_policy_id,
            "boundary": "partial-context fallback surface; Stage04 56-feature quarantine artifact is a reference only",
            "route_coverage": dict(route_coverage),
            "stage04_quarantine_reference": {
                "model_input_dataset_id": tier_b_model_input_dataset_id,
                "feature_set_id": tier_b_feature_set_id,
                "model_input_path": tier_b_model_input_path.as_posix(),
                "model_input_sha256": sha256_file(tier_b_model_input_path),
                "feature_order_path": tier_b_feature_order_path.as_posix(),
                "feature_order_sha256": sha256_file(tier_b_feature_order_path),
            },
        },
    }
    expected_mt5_kpi_record_count = sum(
        3 if attempt.get("routing_mode") == "tier_a_primary_tier_b_fallback" else 1 for attempt in mt5_attempts
    )
    mt5_runtime_completed = bool(mt5_execution_results) and all(item["status"] == "completed" for item in mt5_execution_results)
    mt5_reports_completed = len(mt5_kpi_records) >= expected_mt5_kpi_record_count and all(
        item.get("status") == "completed" for item in mt5_kpi_records
    )
    external_status = "completed" if mt5_runtime_completed and mt5_reports_completed else (
        "blocked" if attempt_mt5 else "out_of_scope_by_claim"
    )
    ledger_rows = alpha_run_ledgers.build_alpha_scout_ledger_rows(
        run_id=run_id,
        stage_id=stage_id,
        tier_records=tier_records,
        mt5_kpi_records=mt5_kpi_records,
        selected_threshold_id=str(threshold_selection["threshold_id"]),
        run_output_root=run_output_root,
        external_verification_status=external_status,
        tier_a=tier_a,
        tier_b=tier_b,
        tier_ab=tier_ab,
    )
    ledger_payload = alpha_run_ledgers.materialize_alpha_ledgers(
        stage_run_ledger_path=stage_run_ledger_path,
        project_alpha_ledger_path=project_alpha_ledger_path,
        rows=ledger_rows,
    )
    run_registry_payload = alpha_run_ledgers.materialize_alpha_runtime_run_registry_row(
        run_id=run_id,
        stage_id=stage_id,
        run_registry_path=run_registry_path,
        route_coverage=route_coverage,
        mt5_kpi_records=mt5_kpi_records,
        run_output_root=run_output_root,
        external_verification_status=external_status,
        routing_mode=routing_mode,
        tier_a_only_prefix=tier_a_only_prefix,
        tier_b_fallback_only_prefix=tier_b_fallback_only_prefix,
    )
    artifacts.extend(
        [
            {"role": "stage_run_ledger", **ledger_payload["stage_run_ledger"]},
            {"role": "project_alpha_run_ledger", **ledger_payload["project_alpha_run_ledger"]},
            {"role": "project_run_registry", **run_registry_payload},
        ]
    )
    manifest = build_alpha_run_manifest_payload(
        run_id=run_id,
        run_number=run_number,
        stage_id=stage_id,
        exploration_label=exploration_label,
        input_refs=input_refs,
        artifacts=artifacts,
        threshold_selection=threshold_selection,
        tier_records=tier_records,
        onnx_parity=onnx_parity,
        external_verification_status=external_status,
    )
    manifest["routing_design"] = {
        "routing_mode": routing_detail,
        "primary_tier": tier_a,
        "fallback_enabled": bool(routed_fallback_enabled),
        "fallback_tier": tier_b if routed_fallback_enabled else None,
        "fallback_policy_id": tier_b_partial_context_policy_id if routed_fallback_enabled else "out_of_scope_by_claim",
        "fallback_allowed_subtypes": list(allowed_fallback_subtypes) if allowed_fallback_subtypes else None,
        "route_coverage": dict(route_coverage),
    }
    manifest["mt5"] = {
        "attempted": bool(attempt_mt5),
        "compile": compile_payload,
        "execution_results": list(mt5_execution_results),
        "strategy_tester_reports": list(mt5_report_records),
        "kpi_records": list(mt5_kpi_records),
        "module_hashes": list(mt5_module_hashes),
        "tester_defaults": {
            "symbol": "US100",
            "period": "M5",
            "model": 4,
            "deposit": 500,
            "leverage": "1:100",
            "fixed_lot": 0.1,
            "max_hold_bars": int(max_hold_bars),
            "max_concurrent_positions": 1,
        },
    }
    kpi = build_alpha_kpi_record_payload(
        run_id=run_id,
        stage_id=stage_id,
        threshold_sweep=threshold_sweep,
        threshold_sweeps=threshold_sweeps,
        tier_records=tier_records,
        onnx_parity=onnx_parity,
        mt5_kpi_records=mt5_kpi_records,
        primary_tier=tier_a,
        fallback_tier=tier_b,
    )
    kpi["threshold"]["selected_threshold_id"] = threshold_selection["threshold_id"]
    kpi["threshold"]["actual_selection"] = dict(threshold_selection)
    kpi["routing"]["routing_mode"] = routing_detail
    kpi["routing"]["fallback_enabled"] = bool(routed_fallback_enabled)
    kpi["routing"]["route_coverage_design"] = dict(route_coverage)
    kpi["mt5"] = {
        "scoreboard_lane": "runtime_probe",
        "external_verification_status": external_status,
        "compile": compile_payload,
        "execution_results": list(mt5_execution_results),
        "strategy_tester_reports": list(mt5_report_records),
        "kpi_records": list(mt5_kpi_records),
        "attempt_count": len(mt5_attempts),
    }
    payload_paths = materialize_manifest_and_kpi(run_output_root, manifest_payload=manifest, kpi_payload=kpi)
    summary_path = run_output_root / "summary.json"
    result_summary_path = reports_root / "result_summary.md"
    summary = {
        "run_id": run_id,
        "stage_id": stage_id,
        "status": "completed_payload" if onnx_parity["passed"] else "invalid_payload",
        "judgment": "inconclusive_single_split_scout_payload"
        if external_status != "completed"
        else "inconclusive_single_split_scout_mt5_routed_completed",
        "selected_threshold": dict(threshold_selection),
        "tier_records": list(tier_records),
        "onnx_parity": dict(onnx_parity),
        "external_verification_status": external_status,
        "mt5_attempted": bool(attempt_mt5),
        "mt5_execution_results": list(mt5_execution_results),
        "mt5_kpi_records": list(mt5_kpi_records),
        "ledger_rows": ledger_rows,
        "ledger_payload": ledger_payload,
        "run_registry_payload": run_registry_payload,
        "boundary": "single_split_scout only; not alpha quality, live readiness, runtime authority expansion, or operating promotion",
    }
    write_json(summary_path, summary)
    result_summary_path.parent.mkdir(parents=True, exist_ok=True)
    mt5_records_by_view = {str(record.get("record_view")): record for record in mt5_kpi_records}

    def result_metric(record_view: str, metric_name: str) -> Any:
        record = mt5_records_by_view.get(record_view, {})
        return record.get("metrics", {}).get(metric_name)

    routed_view_label = "Tier A+B routed total" if routed_fallback_enabled else "Tier A-only routed total"
    result_summary_lines = [
        f"# Stage {stage_id} {run_number} Alpha Scout",
        "",
        f"- run_id: `{run_id}`",
        f"- selected threshold: `{threshold_selection['threshold_id']}`",
        f"- Tier A rule: `{tier_a_rule.threshold_id}`",
        f"- Tier B fallback rule: `{tier_b_rule.threshold_id}`",
        f"- routed fallback enabled: `{bool(routed_fallback_enabled)}`",
        f"- Tier B fallback allowed subtypes: `{list(allowed_fallback_subtypes) if allowed_fallback_subtypes else 'all'}`",
        f"- session slice: `{session_slice_id or 'full'}`",
        f"- max hold bars: `{int(max_hold_bars)}`",
        f"- external verification status: `{external_status}`",
        f"- Tier A rows: `{tier_a_predictions_count}`",
        f"- Tier B fallback rows: `{tier_b_predictions_count}`",
        f"- no-tier labelable rows: `{no_tier_eval_count}`",
        f"- MT5 KPI records: `{len(mt5_kpi_records)}`",
        f"- MT5 comparison views: `Tier A only`, `Tier B fallback-only`, `{routed_view_label}`",
        f"- Tier B fallback subtype counts: `{route_coverage.get('tier_b_fallback_by_subtype', {})}`",
        "",
        "## Validation IS",
        "",
        f"- Tier A only net profit: `{result_metric('mt5_tier_a_only_validation_is', 'net_profit')}`",
        f"- Tier A only profit factor: `{result_metric('mt5_tier_a_only_validation_is', 'profit_factor')}`",
        f"- Tier B fallback-only net profit: `{result_metric('mt5_tier_b_fallback_only_validation_is', 'net_profit')}`",
        f"- Tier B fallback-only profit factor: `{result_metric('mt5_tier_b_fallback_only_validation_is', 'profit_factor')}`",
        f"- Routed net profit: `{result_metric('mt5_routed_total_validation_is', 'net_profit')}`",
        f"- Routed profit factor: `{result_metric('mt5_routed_total_validation_is', 'profit_factor')}`",
        f"- Routed Tier A used: `{result_metric('mt5_routed_total_validation_is', 'tier_a_used_count')}`",
        f"- Routed Tier B fallback used: `{result_metric('mt5_routed_total_validation_is', 'tier_b_fallback_used_count')}`",
        "",
        "## OOS",
        "",
        f"- Tier A only net profit: `{result_metric('mt5_tier_a_only_oos', 'net_profit')}`",
        f"- Tier A only profit factor: `{result_metric('mt5_tier_a_only_oos', 'profit_factor')}`",
        f"- Tier B fallback-only net profit: `{result_metric('mt5_tier_b_fallback_only_oos', 'net_profit')}`",
        f"- Tier B fallback-only profit factor: `{result_metric('mt5_tier_b_fallback_only_oos', 'profit_factor')}`",
        f"- Routed net profit: `{result_metric('mt5_routed_total_oos', 'net_profit')}`",
        f"- Routed profit factor: `{result_metric('mt5_routed_total_oos', 'profit_factor')}`",
        f"- Routed Tier A used: `{result_metric('mt5_routed_total_oos', 'tier_a_used_count')}`",
        f"- Routed Tier B fallback used: `{result_metric('mt5_routed_total_oos', 'tier_b_fallback_used_count')}`",
        "",
        "## Boundary",
        "",
        "single_split_scout only; not alpha quality, live readiness, runtime authority expansion, or operating promotion.",
        "",
    ]
    result_summary_path.write_text("\n".join(result_summary_lines), encoding="utf-8-sig")

    return {
        "status": "ok" if onnx_parity["passed"] else "failed",
        "run_id": run_id,
        "run_output_root": run_output_root.as_posix(),
        "threshold_id": str(threshold_selection["threshold_id"]),
        "onnx_parity": dict(onnx_parity),
        "external_verification_status": external_status,
        "mt5_attempted": attempt_mt5,
        "payload_paths": payload_paths,
        "summary_path": summary_path.as_posix(),
        "result_summary_path": result_summary_path.as_posix(),
        "ledger_payload": ledger_payload,
        "run_registry_payload": run_registry_payload,
    }
