from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Sequence

from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    ledger_pairs,
    ledger_path,
    ledger_status,
    upsert_csv_rows,
)


TIER_A = "Tier A"
TIER_B = "Tier B"
TIER_AB = "Tier A+B"


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
        metrics = record.get("metrics", {})
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


def materialize_alpha_ledgers(
    *,
    stage_run_ledger_path: Path,
    project_alpha_ledger_path: Path,
    rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    stage_payload = upsert_csv_rows(stage_run_ledger_path, ALPHA_LEDGER_COLUMNS, rows, key="ledger_row_id")
    project_payload = upsert_csv_rows(project_alpha_ledger_path, ALPHA_LEDGER_COLUMNS, rows, key="ledger_row_id")
    return {"stage_run_ledger": stage_payload, "project_alpha_run_ledger": project_payload}
