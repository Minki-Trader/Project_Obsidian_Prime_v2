from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Sequence

from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    ledger_pairs,
    ledger_path,
    ledger_status,
    upsert_csv_rows,
)


TIER_A = "Tier A"
TIER_B = "Tier B"
TIER_AB = "Tier A+B"
ROUTING_MODE_A_B_FALLBACK = "tier_a_primary_tier_b_fallback"
ROUTING_MODE_A_ONLY = "tier_a_primary_no_fallback"


def _mt5_report_paths(mt5_kpi_records: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    report_paths: dict[str, Any] = {}
    for record in mt5_kpi_records:
        report = record.get("report", {})
        if not isinstance(report, Mapping):
            continue
        record_view_key = str(record.get("record_view"))
        html_report = report.get("html_report", {})
        metrics_report = report.get("metrics", {})
        if isinstance(html_report, Mapping) and html_report.get("path"):
            report_paths[record_view_key] = html_report.get("path")
        elif isinstance(metrics_report, Mapping) and metrics_report.get("report_path"):
            report_paths[record_view_key] = metrics_report.get("report_path")
    return report_paths


def build_mt5_alpha_ledger_rows(
    *,
    run_id: str,
    stage_id: str,
    mt5_kpi_records: Sequence[Mapping[str, Any]],
    run_output_root: Path,
    external_verification_status: str,
    tier_b: str = TIER_B,
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    kpi_record_path = (run_output_root / "kpi_record.json").as_posix()
    report_paths = _mt5_report_paths(mt5_kpi_records)

    for record in mt5_kpi_records:
        record_view = str(record.get("record_view"))
        raw_metrics = record.get("metrics", {})
        metrics = raw_metrics if isinstance(raw_metrics, Mapping) else {}
        route_role = str(record.get("route_role") or "")
        is_component = route_role in {"primary_used", "fallback_used"}
        is_routed_total = route_role == "routed_total"
        is_trading_total = not is_component
        row_path = report_paths.get(record_view, kpi_record_path)
        if is_trading_total:
            primary_kpi = ledger_pairs(
                (
                    ("net_profit", metrics.get("net_profit")),
                    ("pf", metrics.get("profit_factor")),
                    ("expectancy", metrics.get("expectancy")),
                    ("trades", metrics.get("trade_count")),
                    ("win_rate", metrics.get("win_rate_percent")),
                )
            )
            if is_routed_total:
                guardrail_kpi = ledger_pairs(
                    (
                        ("a_used", metrics.get("tier_a_used_count")),
                        ("b_fallback", metrics.get("tier_b_fallback_used_count")),
                        ("no_tier_labelable", metrics.get("no_tier_labelable_rows")),
                        ("max_dd", metrics.get("max_drawdown_amount")),
                        ("recovery", metrics.get("recovery_factor")),
                        ("fill", metrics.get("fill_count")),
                        ("reject", metrics.get("reject_count")),
                        ("skip", metrics.get("skip_count")),
                    )
                )
                notes = "Actual routed total from one MT5 tester account path; not a synthetic sum."
            else:
                labelable_count = (
                    metrics.get("tier_b_fallback_labelable_rows")
                    if record.get("tier_scope") == tier_b
                    else metrics.get("tier_a_primary_labelable_rows")
                )
                guardrail_kpi = ledger_pairs(
                    (
                        ("labelable", labelable_count),
                        ("feature_ready", metrics.get("feature_ready_count")),
                        ("model_ok", metrics.get("model_ok_count")),
                        ("no_tier_labelable", metrics.get("no_tier_labelable_rows")),
                        ("max_dd", metrics.get("max_drawdown_amount")),
                        ("recovery", metrics.get("recovery_factor")),
                        ("fill", metrics.get("fill_count")),
                        ("reject", metrics.get("reject_count")),
                        ("skip", metrics.get("skip_count")),
                        ("subtypes", metrics.get("partial_context_subtype_counts")),
                    )
                )
                notes = (
                    "Tier B fallback-only standalone MT5 tester run."
                    if record.get("tier_scope") == tier_b
                    else "Tier A only standalone MT5 tester run."
                )
        else:
            primary_kpi = ledger_pairs(
                (
                    ("route_bars", metrics.get("route_bar_count")),
                    ("route_share", metrics.get("route_share")),
                    ("signals", metrics.get("signal_count")),
                    ("long", metrics.get("long_count")),
                    ("short", metrics.get("short_count")),
                    ("fills", metrics.get("fill_count")),
                )
            )
            guardrail_kpi = ledger_pairs(
                (
                    ("profit_attribution", metrics.get("profit_attribution")),
                    ("reject", metrics.get("reject_count")),
                    ("skip", metrics.get("skip_count")),
                    ("subtypes", metrics.get("partial_context_subtype_counts")),
                )
            )
            notes = (
                "Tier B partial-context fallback used component from one routed MT5 tester run."
                if route_role == "fallback_used"
                else "Tier A primary used component from one routed MT5 tester run."
            )
        if is_routed_total:
            judgment = "inconclusive_routed_total_runtime_probe"
        elif route_role == "tier_b_fallback_only_total":
            judgment = "inconclusive_tier_b_fallback_only_runtime_probe"
        elif is_trading_total:
            judgment = "inconclusive_tier_only_runtime_probe"
        else:
            judgment = "inconclusive_routed_component_runtime_probe"
        rows.append(
            {
                "ledger_row_id": f"{run_id}__{record_view}",
                "stage_id": stage_id,
                "run_id": run_id,
                "subrun_id": record_view,
                "parent_run_id": run_id,
                "record_view": record_view,
                "tier_scope": str(record.get("tier_scope")),
                "kpi_scope": "trading_risk_execution" if is_trading_total else "routed_signal_execution_usage",
                "scoreboard_lane": "runtime_probe",
                "status": ledger_status(record.get("status")),
                "judgment": judgment,
                "path": ledger_path(row_path),
                "primary_kpi": primary_kpi,
                "guardrail_kpi": guardrail_kpi,
                "external_verification_status": external_verification_status,
                "notes": notes,
            }
        )
    return rows


def build_alpha_scout_ledger_rows(
    *,
    run_id: str,
    stage_id: str,
    tier_records: Sequence[Mapping[str, Any]],
    mt5_kpi_records: Sequence[Mapping[str, Any]],
    selected_threshold_id: str,
    run_output_root: Path,
    external_verification_status: str,
    tier_a: str = TIER_A,
    tier_b: str = TIER_B,
    tier_ab: str = TIER_AB,
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    for record in tier_records:
        record_view = str(record.get("record_view"))
        raw_metrics = record.get("metrics", {})
        metrics = raw_metrics if isinstance(raw_metrics, Mapping) else {}
        row_view = f"python_{record_view}"
        rows.append(
            {
                "ledger_row_id": f"{run_id}__{row_view}",
                "stage_id": stage_id,
                "run_id": run_id,
                "subrun_id": row_view,
                "parent_run_id": run_id,
                "record_view": row_view,
                "tier_scope": str(record.get("tier_scope")),
                "kpi_scope": "signal_probability_threshold",
                "scoreboard_lane": "structural_scout",
                "status": ledger_status(record.get("status")),
                "judgment": "inconclusive_single_split_scout_payload",
                "path": ledger_path(record.get("path")),
                "primary_kpi": ledger_pairs(
                    (
                        ("rows", metrics.get("rows")),
                        ("signal_coverage", metrics.get("signal_coverage")),
                        ("signal_count", metrics.get("signal_count")),
                        ("short", metrics.get("short_count")),
                        ("long", metrics.get("long_count")),
                    )
                ),
                "guardrail_kpi": ledger_pairs(
                    (
                        ("prob_sum_err", metrics.get("probability_row_sum_max_abs_error")),
                        ("selected_threshold", selected_threshold_id),
                        ("threshold_ids", metrics.get("threshold_ids")),
                        ("subtype_counts", metrics.get("partial_context_subtype_counts")),
                    )
                ),
                "external_verification_status": "out_of_scope_by_claim",
                "notes": (
                    "Tier B partial-context fallback-only view"
                    if record.get("tier_scope") == tier_b
                    else "Tier A primary plus Tier B fallback routed Python view"
                    if record.get("tier_scope") == tier_ab
                    else "Tier A full-context primary view"
                    if record.get("tier_scope") == tier_a
                    else "Alpha scout Python decision view"
                ),
            }
        )

    rows.extend(
        build_mt5_alpha_ledger_rows(
            run_id=run_id,
            stage_id=stage_id,
            mt5_kpi_records=mt5_kpi_records,
            run_output_root=run_output_root,
            external_verification_status=external_verification_status,
            tier_b=tier_b,
        )
    )
    return rows


def materialize_alpha_runtime_run_registry_row(
    *,
    run_id: str,
    stage_id: str,
    run_registry_path: Path,
    route_coverage: Mapping[str, Any],
    mt5_kpi_records: Sequence[Mapping[str, Any]],
    run_output_root: Path,
    external_verification_status: str,
    routing_mode: str = ROUTING_MODE_A_B_FALLBACK,
    tier_a_only_prefix: str = "mt5_tier_a_only",
    tier_b_fallback_only_prefix: str = "mt5_tier_b_fallback_only",
) -> dict[str, Any]:
    by_view = {str(record.get("record_view")): record.get("metrics", {}) for record in mt5_kpi_records}
    validation = by_view.get("mt5_routed_total_validation_is", {})
    oos = by_view.get("mt5_routed_total_oos", {})
    a_validation = by_view.get(f"{tier_a_only_prefix}_validation_is", {})
    a_oos = by_view.get(f"{tier_a_only_prefix}_oos", {})
    b_validation = by_view.get(f"{tier_b_fallback_only_prefix}_validation_is", {})
    b_oos = by_view.get(f"{tier_b_fallback_only_prefix}_oos", {})
    mt5_views = (
        "tier_a_only;tier_b_fallback_only;tier_a_primary_no_fallback"
        if routing_mode == ROUTING_MODE_A_ONLY
        else "tier_a_only;tier_b_fallback_only;tier_a_primary_tier_b_fallback"
    )
    notes = ledger_pairs(
        (
            ("mt5_views", mt5_views),
            ("routing_mode", routing_mode),
            ("tier_b_fallback_rows", route_coverage.get("tier_b_fallback_rows")),
            ("tier_b_fallback_allowed_subtypes", route_coverage.get("tier_b_fallback_allowed_subtypes")),
            ("tier_b_fallback_filtered_out_rows", route_coverage.get("tier_b_fallback_filtered_out_rows")),
            ("no_tier_labelable_rows", route_coverage.get("no_tier_labelable_rows")),
            ("validation_a_only_net_profit", a_validation.get("net_profit")),
            ("validation_a_only_pf", a_validation.get("profit_factor")),
            ("validation_b_only_net_profit", b_validation.get("net_profit")),
            ("validation_b_only_pf", b_validation.get("profit_factor")),
            ("validation_net_profit", validation.get("net_profit")),
            ("validation_pf", validation.get("profit_factor")),
            ("validation_b_fallback_used", validation.get("tier_b_fallback_used_count")),
            ("oos_a_only_net_profit", a_oos.get("net_profit")),
            ("oos_a_only_pf", a_oos.get("profit_factor")),
            ("oos_b_only_net_profit", b_oos.get("net_profit")),
            ("oos_b_only_pf", b_oos.get("profit_factor")),
            ("oos_net_profit", oos.get("net_profit")),
            ("oos_pf", oos.get("profit_factor")),
            ("oos_b_fallback_used", oos.get("tier_b_fallback_used_count")),
            ("external_verification", external_verification_status),
            ("boundary", "runtime_probe_only"),
        )
    )
    row = {
        "run_id": run_id,
        "stage_id": stage_id,
        "lane": "alpha_runtime_probe",
        "status": "reviewed" if external_verification_status == "completed" else "payload_only",
        "judgment": "inconclusive_single_split_scout_mt5_routed_completed"
        if external_verification_status == "completed"
        else "inconclusive_single_split_scout_payload",
        "path": run_output_root.as_posix(),
        "notes": notes,
    }
    return upsert_csv_rows(run_registry_path, RUN_REGISTRY_COLUMNS, [row], key="run_id")


def materialize_alpha_ledgers(
    *,
    stage_run_ledger_path: Path,
    project_alpha_ledger_path: Path,
    rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    stage_payload = upsert_csv_rows(stage_run_ledger_path, ALPHA_LEDGER_COLUMNS, rows, key="ledger_row_id")
    project_payload = upsert_csv_rows(project_alpha_ledger_path, ALPHA_LEDGER_COLUMNS, rows, key="ledger_row_id")
    return {"stage_run_ledger": stage_payload, "project_alpha_run_ledger": project_payload}
