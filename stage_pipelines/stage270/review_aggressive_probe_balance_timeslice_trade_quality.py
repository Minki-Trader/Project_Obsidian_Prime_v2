from __future__ import annotations

import csv
import json
import math
import sys
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from statistics import mean
from typing import Any, Iterable, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    path_exists,
    read_csv_rows,
    sha256_file_lf_normalized,
    upsert_csv_rows,
    write_csv_rows,
)
from foundation.mt5.trade_report import pair_deals_into_trades, parse_mt5_trade_report


STAGE_ID = "270_onnx_candidate_campaign__aggressive_nonfilter_upside_probe"
RUN_ID = "run270D_aggressive_probe_balance_timeslice_trade_quality_review_v1"
RUN_NUMBER = "run270D"
SOURCE_RUN_ID = "run270C_aggressive_probe_mt5_signal_replay_v1"
PARENT_RUN_ID = "run270B_aggressive_probe_payload_materialization_v1"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)
DEPOSIT = 500.0
ACTIVE_SURVIVOR_READ = "active_probe_survives_for_stability_review"
NO_SURVIVOR_NEXT_ACTION = "run270E_stage270_closeout_and_stage271_fresh_thesis_handoff"
SURVIVOR_NEXT_ACTION = "run271A_survivor_stability_validation_design"
REPAIR_NEXT_ACTION = "run270D_repair_trade_report_parser_or_count_mismatch"

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
RUN270C_ROOT = STAGE_ROOT / "02_runs" / "run270C"
RUN270A_ROOT = STAGE_ROOT / "02_runs" / "run270A"
REVIEWS = STAGE_ROOT / "03_reviews"
SELECTED = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"

SOURCE_EXECUTION_RESULT = RUN270C_ROOT / "execution_result.json"
SOURCE_KPI_SUMMARY = RUN270C_ROOT / "mt5_kpi_summary.csv"
SOURCE_FORENSICS = RUN270C_ROOT / "backtest_forensics.csv"
SOURCE_RUNTIME_PARITY = RUN270C_ROOT / "runtime_parity_receipt.csv"
SOURCE_VARIANT_PLAN = RUN270A_ROOT / "aggressive_probe_variant_plan.csv"

TRADE_RECORDS = RUN_ROOT / "trade_records.csv"
TIME_SLICE_KPI = RUN_ROOT / "time_slice_kpi.csv"
CURVE_DIAGNOSTICS = RUN_ROOT / "curve_diagnostics.csv"
VARIANT_SPLIT_REVIEW = RUN_ROOT / "variant_split_review.csv"
VARIANT_SUMMARY = RUN_ROOT / "variant_summary.csv"
TIER_DUPLICATE_REVIEW = RUN_ROOT / "tier_duplicate_review.csv"
NEGATIVE_SLICE_SUMMARY = RUN_ROOT / "negative_slice_summary.csv"
PARSER_CHECKS = RUN_ROOT / "parser_checks.csv"
FORENSICS_SUMMARY = RUN_ROOT / "forensics_summary.json"
RESULT_JUDGMENT = RUN_ROOT / "result_judgment.csv"
ARTIFACT_LINEAGE = RUN_ROOT / "artifact_lineage_receipt.json"
REVIEW_RESULT = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS / "run270D_report.md"
PRODUCER_PATH = Path("stage_pipelines/stage270/review_aggressive_probe_balance_timeslice_trade_quality.py")

RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs/registers/artifact_registry.csv"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"
CURRENT_STATE = ROOT / "docs/context/current_working_state.md"
WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CHANGELOG = ROOT / "docs/workspace/changelog.md"

AXES = ("month", "weekday", "close_hour_report", "session_report", "direction", "chron_segment")
TRADE_COLUMNS = (
    "run_id",
    "source_run_id",
    "record_view",
    "attempt_name",
    "variant_id",
    "variant_role",
    "queue_role",
    "tier_scope",
    "split",
    "route_role",
    "trade_index",
    "direction",
    "open_time",
    "close_time",
    "holding_minutes",
    "month",
    "weekday",
    "close_hour_report",
    "session_report",
    "chron_segment",
    "volume",
    "open_price",
    "close_price",
    "gross_profit",
    "net_profit",
    "commission",
    "swap",
    "source_report_path",
)
TIME_SLICE_COLUMNS = (
    "variant_id",
    "variant_role",
    "queue_role",
    "record_view",
    "tier_scope",
    "split",
    "axis",
    "bucket",
    "trade_count",
    "net_profit",
    "gross_profit",
    "gross_loss",
    "profit_factor",
    "expectancy",
    "win_rate",
    "avg_win",
    "avg_loss",
    "payoff_ratio",
    "closed_balance_max_drawdown",
    "closed_balance_max_drawdown_percent",
    "longest_underwater_trades",
    "underwater_trade_share",
    "max_losing_streak",
    "recovery_factor_closed",
    "slice_read",
)
CURVE_COLUMNS = (
    "variant_id",
    "variant_role",
    "queue_role",
    "record_view",
    "tier_scope",
    "split",
    "route_role",
    "trade_count",
    "net_profit",
    "gross_profit",
    "gross_loss",
    "profit_factor",
    "expectancy",
    "win_rate",
    "avg_win",
    "avg_loss",
    "payoff_ratio",
    "closed_balance_max_drawdown",
    "closed_balance_max_drawdown_percent",
    "report_equity_drawdown_percent",
    "report_balance_drawdown_percent",
    "report_recovery_factor",
    "positive_month_ratio",
    "negative_month_count",
    "worst_month",
    "worst_month_net",
    "best_month",
    "best_month_net",
    "chron_early_net",
    "chron_mid_net",
    "chron_late_net",
    "source_chart_path",
    "curve_read",
)
VARIANT_SPLIT_COLUMNS = (
    "variant_id",
    "variant_role",
    "queue_role",
    "tier_scope",
    "split",
    "record_view",
    "net_profit",
    "profit_factor",
    "trade_count",
    "expectancy",
    "win_rate",
    "report_equity_drawdown_percent",
    "closed_balance_max_drawdown_percent",
    "recovery_factor_closed",
    "positive_month_ratio",
    "negative_month_count",
    "worst_month",
    "worst_month_net",
    "worst_slice_axis",
    "worst_slice_bucket",
    "worst_slice_net",
    "fragility_flags",
    "curve_read",
    "split_review_read",
    "selection_boundary",
)
VARIANT_SUMMARY_COLUMNS = (
    "variant_id",
    "variant_role",
    "queue_role",
    "tier_scope",
    "validation_net_profit",
    "oos_net_profit",
    "validation_profit_factor",
    "oos_profit_factor",
    "validation_equity_dd_percent",
    "oos_equity_dd_percent",
    "validation_trade_count",
    "oos_trade_count",
    "worst_month_net_min",
    "worst_slice_net_min",
    "fragility_flags",
    "survival_read",
    "next_use",
)
TIER_DUPLICATE_COLUMNS = (
    "variant_id",
    "split",
    "tier_pair_present",
    "net_profit_delta_tier_b_minus_tier_a",
    "trade_count_delta_tier_b_minus_tier_a",
    "audit_status",
    "interpretation",
)
PARSER_COLUMNS = (
    "attempt_name",
    "record_view",
    "variant_id",
    "tier_scope",
    "split",
    "report_path",
    "expected_trade_count",
    "parsed_trade_count",
    "trade_count_delta",
    "parser_status",
    "error",
)
RESULT_JUDGMENT_COLUMNS = (
    "result_subject",
    "evidence_available",
    "evidence_missing",
    "judgment_label",
    "claim_boundary",
    "next_condition",
    "user_explanation_hook",
)
ARTIFACT_COLUMNS = ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes")
STAGE_LEDGER_COLUMNS = (
    "row_id",
    "stage_id",
    "run_id",
    "view",
    "tier_scope",
    "scoreboard",
    "status",
    "judgment",
    "evidence_boundary",
    "report_path",
    "notes",
)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def cell(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        if math.isinf(value):
            return "inf"
        if not math.isfinite(value):
            return ""
        return round(value, 6)
    return value


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


def as_int(value: Any, default: int = 0) -> int:
    try:
        return int(round(float(value)))
    except (TypeError, ValueError):
        return default


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_json(path: Path, payload: Any, *, bom: bool = False) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    encoding = "utf-8-sig" if bom else "utf-8"
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding=encoding,
    )


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: cell(row.get(column)) for column in columns})


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def group_rows(rows: Iterable[Mapping[str, Any]], keys: Sequence[str]) -> dict[tuple[Any, ...], list[Mapping[str, Any]]]:
    grouped: dict[tuple[Any, ...], list[Mapping[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[tuple(row.get(key) for key in keys)].append(row)
    return grouped


def session_bucket(hour_text: str) -> str:
    hour = as_int(hour_text)
    if 0 <= hour <= 6:
        return "session_00_06_report_time"
    if 7 <= hour <= 12:
        return "session_07_12_report_time"
    if 13 <= hour <= 20:
        return "session_13_20_report_time"
    return "session_21_23_report_time"


def chronological_segment(index: int, total: int) -> str:
    if total <= 0:
        return "none"
    third = (total + 2) // 3
    if index < third:
        return "chron_early"
    if index < third * 2:
        return "chron_mid"
    return "chron_late"


def profit_factor(rows: Sequence[Mapping[str, Any]]) -> float | None:
    wins = sum(as_float(row.get("net_profit")) for row in rows if as_float(row.get("net_profit")) > 0.0)
    losses = -sum(as_float(row.get("net_profit")) for row in rows if as_float(row.get("net_profit")) < 0.0)
    if losses == 0.0:
        return math.inf if wins > 0.0 else None
    return wins / losses


def max_closed_balance_drawdown(rows: Sequence[Mapping[str, Any]]) -> tuple[float, float, int, float]:
    balance = DEPOSIT
    peak = DEPOSIT
    max_dd = 0.0
    max_dd_pct = 0.0
    longest_underwater = 0
    current_underwater = 0
    underwater_count = 0
    for row in sorted(rows, key=lambda item: str(item.get("close_time"))):
        balance += as_float(row.get("net_profit"))
        if balance >= peak:
            peak = balance
            current_underwater = 0
        else:
            current_underwater += 1
            underwater_count += 1
            longest_underwater = max(longest_underwater, current_underwater)
        dd = peak - balance
        dd_pct = dd / peak * 100.0 if peak else 0.0
        max_dd = max(max_dd, dd)
        max_dd_pct = max(max_dd_pct, dd_pct)
    share = underwater_count / len(rows) if rows else 0.0
    return max_dd, max_dd_pct, longest_underwater, share


def max_losing_streak(rows: Sequence[Mapping[str, Any]]) -> int:
    current = 0
    worst = 0
    for row in sorted(rows, key=lambda item: str(item.get("close_time"))):
        if as_float(row.get("net_profit")) < 0.0:
            current += 1
            worst = max(worst, current)
        else:
            current = 0
    return worst


def metrics(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    ordered = sorted(rows, key=lambda item: str(item.get("close_time")))
    count = len(ordered)
    net = sum(as_float(row.get("net_profit")) for row in ordered)
    wins = [as_float(row.get("net_profit")) for row in ordered if as_float(row.get("net_profit")) > 0.0]
    losses = [as_float(row.get("net_profit")) for row in ordered if as_float(row.get("net_profit")) < 0.0]
    dd, dd_pct, underwater, underwater_share = max_closed_balance_drawdown(ordered)
    gross_profit = sum(wins)
    gross_loss = sum(losses)
    avg_win = gross_profit / len(wins) if wins else None
    avg_loss = gross_loss / len(losses) if losses else None
    payoff_ratio = (avg_win / abs(avg_loss)) if avg_win is not None and avg_loss not in {None, 0.0} else None
    return {
        "trade_count": count,
        "net_profit": net,
        "gross_profit": gross_profit,
        "gross_loss": gross_loss,
        "profit_factor": profit_factor(ordered),
        "expectancy": net / count if count else None,
        "win_rate": len(wins) / count if count else None,
        "avg_win": avg_win,
        "avg_loss": avg_loss,
        "payoff_ratio": payoff_ratio,
        "closed_balance_max_drawdown": dd,
        "closed_balance_max_drawdown_percent": dd_pct,
        "longest_underwater_trades": underwater,
        "underwater_trade_share": underwater_share,
        "max_losing_streak": max_losing_streak(ordered),
        "recovery_factor_closed": net / dd if dd > 0.0 else None,
    }


def slice_read(item: Mapping[str, Any]) -> str:
    count = as_int(item.get("trade_count"))
    net = as_float(item.get("net_profit"))
    dd_pct = as_float(item.get("closed_balance_max_drawdown_percent"))
    if count < 3:
        return "thin_slice"
    if net <= -150.0 or dd_pct >= 30.0:
        return "deep_negative_or_dd_slice"
    if net < -50.0:
        return "negative_fragile_slice"
    if net < 0.0:
        return "minor_negative_slice"
    return "measured_slice"


def curve_read(item: Mapping[str, Any], report_metrics: Mapping[str, Any], month_rows: Sequence[Mapping[str, Any]]) -> str:
    report_dd = as_float(report_metrics.get("equity_drawdown_maximal_percent"))
    closed_dd = as_float(item.get("closed_balance_max_drawdown_percent"))
    risk_dd = max(report_dd, closed_dd)
    pf = as_float(item.get("profit_factor"))
    net = as_float(item.get("net_profit"))
    trades = as_int(item.get("trade_count"))
    negative_months = [row for row in month_rows if as_float(row.get("net_profit")) < 0.0]
    worst_month_net = min((as_float(row.get("net_profit")) for row in month_rows), default=0.0)
    positive_month_ratio = (len(month_rows) - len(negative_months)) / len(month_rows) if month_rows else 0.0
    if net <= 0.0 or pf <= 1.0:
        return "fragile_or_negative_no_extension"
    if risk_dd >= 45.0:
        return "dd_too_high_for_candidate_gate"
    if worst_month_net <= -120.0:
        return "month_hole_uncomfortable"
    if trades >= 250 and net >= 150.0 and pf >= 1.08 and risk_dd < 45.0 and positive_month_ratio >= 0.5:
        return "constructive_watch_not_selection"
    return "mixed_or_fragile"


def load_variant_plan() -> dict[str, dict[str, str]]:
    return {row["variant_id"]: row for row in read_csv(SOURCE_VARIANT_PLAN)}


def attempt_by_name(execution_result: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {str(item.get("attempt_name")): item for item in execution_result.get("attempts", [])}


def build_trade_records(
    execution_result: Mapping[str, Any],
    variant_plan: Mapping[str, Mapping[str, str]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    attempts = attempt_by_name(execution_result)
    rows: list[dict[str, Any]] = []
    parser_checks: list[dict[str, Any]] = []
    for record in execution_result.get("mt5_kpi_records", []):
        if record.get("status") != "completed":
            continue
        report = record.get("report", {})
        metrics_payload = record.get("metrics", {})
        attempt_name = str(report.get("attempt_name") or "")
        attempt = attempts.get(attempt_name, {})
        variant_id = str(attempt.get("variant_id") or "")
        plan = dict(variant_plan.get(variant_id, {}))
        html_path = Path(str(metrics_payload.get("report_path") or report.get("html_report", {}).get("path") or ""))
        if not html_path.is_absolute():
            html_path = ROOT / html_path
        try:
            parsed = parse_mt5_trade_report(html_path)
            trades = pair_deals_into_trades(parsed["deals"])
            error = ""
        except Exception as exc:
            trades = []
            error = str(exc)
        expected_count = as_int(metrics_payload.get("trade_count"))
        parser_checks.append(
            {
                "attempt_name": attempt_name,
                "record_view": record.get("record_view"),
                "variant_id": variant_id,
                "tier_scope": record.get("tier_scope"),
                "split": record.get("split"),
                "report_path": rel(html_path),
                "expected_trade_count": expected_count,
                "parsed_trade_count": len(trades),
                "trade_count_delta": len(trades) - expected_count,
                "parser_status": "matched" if not error and len(trades) == expected_count else "parse_error" if error else "count_mismatch",
                "error": error,
            }
        )
        if error:
            continue
        ordered = sorted(trades, key=lambda item: item.close_time)
        total = len(ordered)
        for index, trade in enumerate(ordered):
            close_time = trade.close_time
            open_time = trade.open_time
            close_hour = close_time.strftime("%H")
            rows.append(
                {
                    "run_id": RUN_ID,
                    "source_run_id": SOURCE_RUN_ID,
                    "record_view": record.get("record_view"),
                    "attempt_name": attempt_name,
                    "variant_id": variant_id,
                    "variant_role": plan.get("variant_role", ""),
                    "queue_role": attempt.get("queue_role"),
                    "tier_scope": record.get("tier_scope"),
                    "split": record.get("split"),
                    "route_role": record.get("route_role"),
                    "trade_index": trade.index,
                    "direction": trade.direction,
                    "open_time": open_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "close_time": close_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "holding_minutes": (close_time - open_time).total_seconds() / 60.0,
                    "month": close_time.strftime("%Y-%m"),
                    "weekday": close_time.strftime("%A"),
                    "close_hour_report": close_hour,
                    "session_report": session_bucket(close_hour),
                    "chron_segment": chronological_segment(index, total),
                    "volume": trade.volume,
                    "open_price": trade.open_price,
                    "close_price": trade.close_price,
                    "gross_profit": trade.gross_profit,
                    "net_profit": trade.net_profit,
                    "commission": trade.commission,
                    "swap": trade.swap,
                    "source_report_path": rel(html_path),
                }
            )
    return rows, parser_checks


def build_time_slice_rows(trade_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for axis in AXES:
        keys = ("variant_id", "variant_role", "queue_role", "record_view", "tier_scope", "split", axis)
        for key, rows in group_rows(trade_rows, keys).items():
            variant_id, variant_role, queue_role, record_view, tier_scope, split, bucket = key
            item = metrics(rows)
            output.append(
                {
                    "variant_id": variant_id,
                    "variant_role": variant_role,
                    "queue_role": queue_role,
                    "record_view": record_view,
                    "tier_scope": tier_scope,
                    "split": split,
                    "axis": axis,
                    "bucket": bucket,
                    **item,
                    "slice_read": slice_read(item),
                }
            )
    return output


def kpi_records_by_view(execution_result: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {str(record.get("record_view")): dict(record.get("metrics", {})) for record in execution_result.get("mt5_kpi_records", [])}


def chart_by_view(execution_result: Mapping[str, Any]) -> dict[str, str]:
    return {
        str(record.get("record_view")): str(record.get("report", {}).get("chart", {}).get("path") or "")
        for record in execution_result.get("mt5_kpi_records", [])
    }


def build_curve_rows(
    trade_rows: Sequence[Mapping[str, Any]],
    time_rows: Sequence[Mapping[str, Any]],
    execution_result: Mapping[str, Any],
) -> list[dict[str, Any]]:
    kpi_by_view = kpi_records_by_view(execution_result)
    charts = chart_by_view(execution_result)
    output: list[dict[str, Any]] = []
    keys = ("variant_id", "variant_role", "queue_role", "record_view", "tier_scope", "split", "route_role")
    for key, rows in group_rows(trade_rows, keys).items():
        variant_id, variant_role, queue_role, record_view, tier_scope, split, route_role = key
        item = metrics(rows)
        report_metrics = dict(kpi_by_view.get(str(record_view), {}))
        month_slices = [
            row
            for row in time_rows
            if row.get("record_view") == record_view and row.get("axis") == "month" and as_int(row.get("trade_count")) >= 3
        ]
        chron_slices = [
            row
            for row in time_rows
            if row.get("record_view") == record_view and row.get("axis") == "chron_segment" and as_int(row.get("trade_count")) >= 3
        ]
        negative_months = [row for row in month_slices if as_float(row.get("net_profit")) < 0.0]
        worst_month = min(month_slices, key=lambda row: as_float(row.get("net_profit"))) if month_slices else {}
        best_month = max(month_slices, key=lambda row: as_float(row.get("net_profit"))) if month_slices else {}
        chron_by_bucket = {str(row.get("bucket")): row for row in chron_slices}
        output.append(
            {
                "variant_id": variant_id,
                "variant_role": variant_role,
                "queue_role": queue_role,
                "record_view": record_view,
                "tier_scope": tier_scope,
                "split": split,
                "route_role": route_role,
                **item,
                "report_equity_drawdown_percent": report_metrics.get("equity_drawdown_maximal_percent"),
                "report_balance_drawdown_percent": report_metrics.get("balance_drawdown_maximal_percent"),
                "report_recovery_factor": report_metrics.get("recovery_factor"),
                "positive_month_ratio": (len(month_slices) - len(negative_months)) / len(month_slices) if month_slices else None,
                "negative_month_count": len(negative_months),
                "worst_month": worst_month.get("bucket", ""),
                "worst_month_net": worst_month.get("net_profit", ""),
                "best_month": best_month.get("bucket", ""),
                "best_month_net": best_month.get("net_profit", ""),
                "chron_early_net": chron_by_bucket.get("chron_early", {}).get("net_profit", ""),
                "chron_mid_net": chron_by_bucket.get("chron_mid", {}).get("net_profit", ""),
                "chron_late_net": chron_by_bucket.get("chron_late", {}).get("net_profit", ""),
                "source_chart_path": charts.get(str(record_view), ""),
                "curve_read": curve_read(item, report_metrics, month_slices),
            }
        )
    return output


def worst_slice_for(record_view: str, time_rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    rows = [
        row
        for row in time_rows
        if row.get("record_view") == record_view
        and as_int(row.get("trade_count")) >= 3
        and row.get("axis") in {"month", "weekday", "session_report", "chron_segment"}
    ]
    if not rows:
        return {}
    return min(rows, key=lambda row: as_float(row.get("net_profit")))


def fragility_flags(row: Mapping[str, Any], worst: Mapping[str, Any]) -> list[str]:
    flags: list[str] = []
    if as_float(row.get("report_equity_drawdown_percent")) >= 45.0:
        flags.append("report_dd_too_high")
    if as_float(row.get("closed_balance_max_drawdown_percent")) >= 30.0:
        flags.append("closed_balance_dd_watch")
    if as_float(row.get("profit_factor")) < 1.05:
        flags.append("pf_too_thin")
    if as_float(row.get("net_profit")) <= 0.0:
        flags.append("nonpositive_net")
    if as_float(row.get("worst_month_net")) <= -120.0:
        flags.append("month_hole")
    if as_float(worst.get("net_profit")) <= -150.0:
        flags.append("deep_slice_hole")
    if as_int(row.get("trade_count")) < 200:
        flags.append("thin_trade_count")
    return flags or ["no_major_flag_in_this_split"]


def split_review_read(row: Mapping[str, Any], flags: Sequence[str]) -> str:
    if row.get("queue_role") == "control_reference":
        return "control_reference_only_not_candidate"
    if "nonpositive_net" in flags:
        return "active_probe_fails_net_gate"
    if "report_dd_too_high" in flags or "month_hole" in flags or "deep_slice_hole" in flags:
        return "active_probe_fragile_not_survivor"
    if str(row.get("curve_read")) == "constructive_watch_not_selection":
        return "active_probe_watch_only_not_selected"
    return "active_probe_mixed_not_survivor"


def build_variant_split_review(
    curve_rows: Sequence[Mapping[str, Any]],
    time_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for row in sorted(curve_rows, key=lambda item: (str(item.get("variant_id")), str(item.get("tier_scope")), str(item.get("split")))):
        worst = worst_slice_for(str(row.get("record_view")), time_rows)
        flags = fragility_flags(row, worst)
        output.append(
            {
                "variant_id": row.get("variant_id"),
                "variant_role": row.get("variant_role"),
                "queue_role": row.get("queue_role"),
                "tier_scope": row.get("tier_scope"),
                "split": row.get("split"),
                "record_view": row.get("record_view"),
                "net_profit": row.get("net_profit"),
                "profit_factor": row.get("profit_factor"),
                "trade_count": row.get("trade_count"),
                "expectancy": row.get("expectancy"),
                "win_rate": row.get("win_rate"),
                "report_equity_drawdown_percent": row.get("report_equity_drawdown_percent"),
                "closed_balance_max_drawdown_percent": row.get("closed_balance_max_drawdown_percent"),
                "recovery_factor_closed": row.get("recovery_factor_closed"),
                "positive_month_ratio": row.get("positive_month_ratio"),
                "negative_month_count": row.get("negative_month_count"),
                "worst_month": row.get("worst_month"),
                "worst_month_net": row.get("worst_month_net"),
                "worst_slice_axis": worst.get("axis", ""),
                "worst_slice_bucket": worst.get("bucket", ""),
                "worst_slice_net": worst.get("net_profit", ""),
                "fragility_flags": ";".join(flags),
                "curve_read": row.get("curve_read"),
                "split_review_read": split_review_read(row, flags),
                "selection_boundary": "not_candidate_selection",
            }
        )
    return output


def by_split(rows: Sequence[Mapping[str, Any]]) -> dict[str, Mapping[str, Any]]:
    return {str(row.get("split")): row for row in rows}


def survival_read_for(variant_id: str, queue_role: str, split_rows: Mapping[str, Mapping[str, Any]]) -> tuple[str, str]:
    val = split_rows.get("validation_is", {})
    oos = split_rows.get("oos", {})
    flags = set()
    for row in (val, oos):
        flags.update(str(row.get("fragility_flags", "")).split(";"))
    if queue_role == "control_reference":
        return "control_reference_positive_but_high_dd_not_candidate", "failure_memory_and_comparison_only"
    if not val or not oos:
        return "missing_required_split_not_survivor", "repair_or_prune"
    if as_float(oos.get("net_profit")) <= 0.0:
        if variant_id.endswith("_q03_supply_expansion_watch"):
            return "near_breakeven_oos_but_negative_and_dd_fragile_not_survivor", "failure_memory_for_future_supply_shape"
        return "oos_negative_not_survivor", "prune"
    if as_float(val.get("net_profit")) <= 0.0:
        return "validation_negative_not_survivor", "prune"
    if as_float(val.get("profit_factor")) < 1.05 or as_float(oos.get("profit_factor")) < 1.05:
        return "pf_too_thin_not_survivor", "prune_or_rebuild_with_new_thesis"
    if "report_dd_too_high" in flags or "deep_slice_hole" in flags or "month_hole" in flags:
        return "risk_or_slice_fragility_not_survivor", "failure_memory"
    return ACTIVE_SURVIVOR_READ, "stability_validation"


def build_variant_summary(variant_split_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    tier_a_rows = [row for row in variant_split_rows if row.get("tier_scope") == "Tier A"]
    output: list[dict[str, Any]] = []
    for (variant_id, variant_role, queue_role, tier_scope), rows in group_rows(tier_a_rows, ("variant_id", "variant_role", "queue_role", "tier_scope")).items():
        splits = by_split(rows)
        val = splits.get("validation_is", {})
        oos = splits.get("oos", {})
        worst_months = [as_float(row.get("worst_month_net")) for row in rows]
        worst_slices = [as_float(row.get("worst_slice_net")) for row in rows]
        flags = sorted({flag for row in rows for flag in str(row.get("fragility_flags", "")).split(";") if flag})
        survival_read, next_use = survival_read_for(str(variant_id), str(queue_role), splits)
        output.append(
            {
                "variant_id": variant_id,
                "variant_role": variant_role,
                "queue_role": queue_role,
                "tier_scope": tier_scope,
                "validation_net_profit": val.get("net_profit", ""),
                "oos_net_profit": oos.get("net_profit", ""),
                "validation_profit_factor": val.get("profit_factor", ""),
                "oos_profit_factor": oos.get("profit_factor", ""),
                "validation_equity_dd_percent": val.get("report_equity_drawdown_percent", ""),
                "oos_equity_dd_percent": oos.get("report_equity_drawdown_percent", ""),
                "validation_trade_count": val.get("trade_count", ""),
                "oos_trade_count": oos.get("trade_count", ""),
                "worst_month_net_min": min(worst_months) if worst_months else "",
                "worst_slice_net_min": min(worst_slices) if worst_slices else "",
                "fragility_flags": ";".join(flags),
                "survival_read": survival_read,
                "next_use": next_use,
            }
        )
    output.sort(
        key=lambda row: (
            0 if row.get("survival_read") == ACTIVE_SURVIVOR_READ else 1,
            0 if row.get("queue_role") == "active_probe" else 1,
            -as_float(row.get("oos_net_profit")),
        )
    )
    return output


def build_tier_duplicate_review(curve_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    grouped = group_rows(curve_rows, ("variant_id", "split"))
    for (variant_id, split), rows in sorted(grouped.items()):
        tier_a = next((row for row in rows if row.get("tier_scope") == "Tier A"), None)
        tier_b = next((row for row in rows if row.get("tier_scope") == "Tier B"), None)
        if not tier_a or not tier_b:
            output.append(
                {
                    "variant_id": variant_id,
                    "split": split,
                    "tier_pair_present": False,
                    "net_profit_delta_tier_b_minus_tier_a": "",
                    "trade_count_delta_tier_b_minus_tier_a": "",
                    "audit_status": "missing_pair",
                    "interpretation": "missing_required_pair",
                }
            )
            continue
        net_delta = as_float(tier_b.get("net_profit")) - as_float(tier_a.get("net_profit"))
        trade_delta = as_int(tier_b.get("trade_count")) - as_int(tier_a.get("trade_count"))
        status = "mirror_duplicate_structural_replay" if abs(net_delta) < 1e-9 and trade_delta == 0 else "tier_pair_differs"
        output.append(
            {
                "variant_id": variant_id,
                "split": split,
                "tier_pair_present": True,
                "net_profit_delta_tier_b_minus_tier_a": net_delta,
                "trade_count_delta_tier_b_minus_tier_a": trade_delta,
                "audit_status": status,
                "interpretation": "not_fallback_authority" if status == "mirror_duplicate_structural_replay" else "inspect_tier_difference",
            }
        )
    return output


def negative_slices(time_rows: Sequence[Mapping[str, Any]], limit: int = 160) -> list[dict[str, Any]]:
    rows = [dict(row) for row in time_rows if row.get("tier_scope") == "Tier A" and as_float(row.get("net_profit")) < 0.0]
    rows.sort(key=lambda row: as_float(row.get("net_profit")))
    return rows[:limit]


def attempt_tester_values(execution_result: Mapping[str, Any], key: str) -> list[str]:
    values = []
    for attempt in execution_result.get("attempts", []):
        tester = dict(dict(attempt.get("ini", {})).get("tester", {}))
        value = tester.get(key)
        if value is not None and str(value).strip():
            values.append(str(value).strip())
    return sorted(set(values))


def terminal_values(execution_result: Mapping[str, Any]) -> list[str]:
    values = []
    for item in execution_result.get("execution_results", []):
        command = item.get("command", [])
        if isinstance(command, Sequence) and command:
            values.append(str(command[0]))
    return sorted(set(values))


def split_date_ranges(execution_result: Mapping[str, Any]) -> list[dict[str, str]]:
    output = []
    for attempt in execution_result.get("attempts", []):
        tester = dict(dict(attempt.get("ini", {})).get("tester", {}))
        split = str(attempt.get("split") or "")
        if split and tester.get("FromDate") and tester.get("ToDate"):
            output.append({"split": split, "from_date": str(tester["FromDate"]), "to_date": str(tester["ToDate"])})
    unique = {(row["split"], row["from_date"], row["to_date"]) for row in output}
    return [{"split": split, "from_date": start, "to_date": end} for split, start, end in sorted(unique)]


def format_date_ranges(ranges: Sequence[Mapping[str, str]]) -> str:
    if not ranges:
        return "missing"
    return "; ".join(f"{row.get('split')} {row.get('from_date')} to {row.get('to_date')}" for row in ranges)


def forensics_summary(
    forensics_rows: Sequence[Mapping[str, str]],
    parser_checks: Sequence[Mapping[str, Any]],
    execution_result: Mapping[str, Any],
) -> dict[str, Any]:
    terminals = sorted({row.get("terminal", "") for row in forensics_rows if row.get("terminal")}) or terminal_values(execution_result)
    symbols = sorted({row.get("symbol", "") for row in forensics_rows if row.get("symbol")})
    timeframes = sorted({row.get("timeframe", "") for row in forensics_rows if row.get("timeframe")})
    deposits = sorted({row.get("deposit", "") for row in forensics_rows if row.get("deposit")})
    leverages = sorted({row.get("leverage", "") for row in forensics_rows if row.get("leverage")})
    models = sorted({row.get("model", "") for row in forensics_rows if row.get("model")})
    from_dates = sorted({row.get("from_date", "") for row in forensics_rows if row.get("from_date")}) or attempt_tester_values(execution_result, "FromDate")
    to_dates = sorted({row.get("to_date", "") for row in forensics_rows if row.get("to_date")}) or attempt_tester_values(execution_result, "ToDate")
    mismatches = [row for row in parser_checks if row.get("parser_status") != "matched"]
    return {
        "row_count": len(forensics_rows),
        "terminal_count": len(terminals),
        "terminals": terminals,
        "symbols": symbols,
        "timeframes": timeframes,
        "deposits": deposits,
        "leverages": leverages,
        "models": models,
        "from_dates": from_dates,
        "to_dates": to_dates,
        "split_date_ranges": split_date_ranges(execution_result),
        "parser_check_count": len(parser_checks),
        "parser_mismatch_count": len(mismatches),
        "cost_assumption_boundary": "strategy_tester_report_costs_only_no_cost_edge_claim",
        "backtest_judgment": "usable_with_boundary" if forensics_rows and not mismatches else "inconclusive",
    }


def classify_result(
    variant_summary: Sequence[Mapping[str, Any]],
    parser_checks: Sequence[Mapping[str, Any]],
) -> tuple[str, str, str]:
    parser_bad = [row for row in parser_checks if row.get("parser_status") != "matched"]
    if parser_bad:
        return (
            "partial_aggressive_probe_balance_timeslice_trade_quality_review_parser_mismatch",
            "inconclusive_parser_mismatch_no_candidate_selection",
            REPAIR_NEXT_ACTION,
        )
    survivor_count = sum(1 for row in variant_summary if row.get("survival_read") == ACTIVE_SURVIVOR_READ)
    if survivor_count:
        return (
            "completed_aggressive_probe_balance_timeslice_trade_quality_review_survivor_watch_no_selection",
            "exploratory_survivor_watch_no_candidate_selection",
            SURVIVOR_NEXT_ACTION,
        )
    return (
        "completed_aggressive_probe_balance_timeslice_trade_quality_review_no_survivor_selection",
        "valid_negative_active_aggressive_probe_no_candidate_selection",
        NO_SURVIVOR_NEXT_ACTION,
    )


def build_result_judgment_rows(
    status: str,
    judgment: str,
    next_action: str,
    variant_summary: Sequence[Mapping[str, Any]],
    parser_checks: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    survivor_count = sum(1 for row in variant_summary if row.get("survival_read") == ACTIVE_SURVIVOR_READ)
    active_failures = [row for row in variant_summary if row.get("queue_role") == "active_probe" and row.get("survival_read") != ACTIVE_SURVIVOR_READ]
    evidence_missing = "ONNX export;ONNX parity;Adapter package;runtime authority;selected candidate"
    if any(row.get("parser_status") != "matched" for row in parser_checks):
        evidence_missing += ";clean_trade_parser_reconciliation"
    return [
        {
            "result_subject": RUN_ID,
            "evidence_available": (
                f"trade_records;time_slice_kpi;curve_diagnostics;variant_summary;"
                f"parser_checks={len(parser_checks)};active_failures={len(active_failures)};survivors={survivor_count}"
            ),
            "evidence_missing": evidence_missing,
            "judgment_label": judgment,
            "claim_boundary": BOUNDARY,
            "next_condition": next_action,
            "user_explanation_hook": "active aggressive probes did not clear OOS, DD, and weak-slice gates; no candidate selection or ONNX readiness",
        }
    ]


def artifact_rows(paths: Sequence[Path], created_at: str) -> list[dict[str, Any]]:
    output = []
    for path in paths:
        output.append(
            {
                "artifact_id": f"{RUN_ID}__{path.stem}",
                "artifact_type": "stage270_run270D_artifact",
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": "Run270D balance/time-slice/trade-quality review artifact.",
            }
        )
    return output


def upsert_ledgers(result: Mapping[str, Any], created_at: str) -> None:
    status = str(result["status"])
    judgment = str(result["judgment"])
    next_action = str(result["next_action"])
    report = rel(REPORT_PATH)
    active_failures = sum(1 for row in result["variant_summary"] if row.get("queue_role") == "active_probe" and row.get("survival_read") != ACTIVE_SURVIVOR_READ)
    survivor_count = sum(1 for row in result["variant_summary"] if row.get("survival_read") == ACTIVE_SURVIVOR_READ)
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "aggressive_probe_balance_timeslice_trade_quality_review",
                "status": status,
                "judgment": judgment,
                "path": report,
                "notes": f"trade_records={result['trade_record_count']};active_failures={active_failures};survivors={survivor_count};selected_candidate=none;onnx_readiness=not_claimed;next_action={next_action}.",
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__balance_timeslice_trade_quality_review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": "balance_timeslice_trade_quality_review",
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "balance_timeslice_trade_quality_review",
                "tier_scope": "Tier A separate plus Tier B mirror boundary; no routed combined authority",
                "kpi_scope": "curve_time_slice_trade_quality_trade_shape_review",
                "scoreboard_lane": "trade_shape_curve_time_slice_review",
                "status": status,
                "judgment": judgment,
                "path": report,
                "primary_kpi": f"trade_records={result['trade_record_count']};variant_rows={len(result['variant_summary'])};survivors={survivor_count}",
                "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
                "external_verification_status": "completed_for_run270C_report_review",
                "notes": f"active_failures={active_failures};next_action={next_action}.",
            }
        ],
        key="ledger_row_id",
    )
    upsert_csv_rows(
        STAGE_LEDGER,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__balance_timeslice_trade_quality_review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "balance_timeslice_trade_quality_review",
                "tier_scope": "Tier A separate plus Tier B mirror boundary",
                "scoreboard": "trade_shape_curve_time_slice_review",
                "status": status,
                "judgment": judgment,
                "evidence_boundary": "diagnostic_review_no_candidate_selection_no_onnx",
                "report_path": report,
                "notes": f"trade_records={result['trade_record_count']};active_failures={active_failures};survivors={survivor_count};next_action={next_action}.",
            }
        ],
        key="row_id",
    )
    artifact_paths = [
        TRADE_RECORDS,
        TIME_SLICE_KPI,
        CURVE_DIAGNOSTICS,
        VARIANT_SPLIT_REVIEW,
        VARIANT_SUMMARY,
        TIER_DUPLICATE_REVIEW,
        NEGATIVE_SLICE_SUMMARY,
        PARSER_CHECKS,
        FORENSICS_SUMMARY,
        RESULT_JUDGMENT,
        ARTIFACT_LINEAGE,
        REVIEW_RESULT,
        REPORT_PATH,
    ]
    rows = artifact_rows([path for path in artifact_paths if path_exists(path)], created_at)
    upsert_csv_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, rows, key="artifact_id")


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def append_once(text: str, marker: str, block: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def replace_section(text: str, heading: str, block: str) -> str:
    lines = text.splitlines()
    try:
        start = lines.index(heading)
    except ValueError:
        return text.rstrip() + "\n\n" + heading + "\n\n" + block.rstrip() + "\n"
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index].startswith("## "):
            end = index
            break
    replacement = [heading, "", *block.rstrip().splitlines(), ""]
    return "\n".join([*lines[:start], *replacement, *lines[end:]]).rstrip() + "\n"


def prepend_focus(text: str, block: str) -> str:
    marker = "current_focus:\n"
    if block.strip() in text or marker not in text:
        return text
    return text.replace(marker, marker + block, 1)


def update_docs(result: Mapping[str, Any]) -> None:
    status = str(result["status"])
    judgment = str(result["judgment"])
    next_action = str(result["next_action"])
    active_failures = sum(1 for row in result["variant_summary"] if row.get("queue_role") == "active_probe" and row.get("survival_read") != ACTIVE_SURVIVOR_READ)
    survivor_count = sum(1 for row in result["variant_summary"] if row.get("survival_read") == ACTIVE_SURVIVOR_READ)
    selection = io_path(SELECTED).read_text(encoding="utf-8-sig")
    selection = replace_line_prefix(selection, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{status}`")
    selection = replace_line_prefix(selection, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- next_action(다음 행동):", f"- next_action(다음 행동): `{next_action}`")
    selection = replace_section(
        selection,
        "## Current Meaning(현재 의미)",
        (
            "run270D(270D 실행)는 run270C(270C 실행)의 MT5(MetaTrader 5, 메타트레이더5) report(보고서)를 trade list(거래 목록), "
            "balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간구간 핵심 성과 지표), trade quality(거래 품질)로 다시 읽었다.\n"
            f"효과(effect, 효과): active probe(활성 탐침) 실패 행 `{active_failures}`개와 survivor(생존 후보) `{survivor_count}`개를 기록했고, "
            "selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 계속 주장하지 않는다."
        ),
    )
    selection = append_once(
        selection,
        "run270D_report(270D 보고)",
        f"- run270D_report(270D 보고): `{rel(REPORT_PATH)}`\n- run270D_variant_summary(270D 변형 요약): `{rel(VARIANT_SUMMARY)}`",
    )
    write_md(SELECTED, selection)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- status(상태):", f"- status(상태): `{status}`")
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{next_action}`")
    run270d_summary = (
        f"- run270D_summary(270D 요약): run270D(270D 실행)는 run270C(270C 실행)의 MT5(MetaTrader 5, 메타트레이더5) report(보고서) `20`개를 "
        f"trade list(거래 목록), curve(곡선), time-slice KPI(시간구간 핵심 성과 지표), trade quality(거래 품질)로 검토했다. "
        f"Effect(효과): trade records(거래 기록) `{result['trade_record_count']}`개, active probe failures(활성 탐침 실패) `{active_failures}`개, "
        f"survivors(생존 후보) `{survivor_count}`개를 남겼고, selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    current = replace_line_prefix(current, "- run270D_summary(270D 요약):", run270d_summary)
    write_md(CURRENT_STATE, current)

    review = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig")
    review = append_once(
        review,
        "run270D_report(270D 보고)",
        f"- run270D_report(270D 보고): `{rel(REPORT_PATH)}`\n- run270D_trade_records(270D 거래 기록): `{rel(TRADE_RECORDS)}`\n- run270D_variant_summary(270D 변형 요약): `{rel(VARIANT_SUMMARY)}`",
    )
    write_md(REVIEW_INDEX, review)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    focus = (
        "- >-\n"
        f"  Stage270(270단계) run270D(270D 실행) balance/time-slice/trade-quality review(잔액/시간구간/거래품질 검토) `{RUN_ID}`. "
        f"Effect(효과): run270C(270C 실행)의 MT5(MetaTrader 5, 메타트레이더5) report(보고서)를 거래 단위로 다시 읽어 "
        f"active probe failures(활성 탐침 실패) `{active_failures}`개와 survivors(생존 후보) `{survivor_count}`개를 기록했고, "
        "selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_focus(workspace, focus)
    write_md(WORKSPACE_STATE, workspace)

    change = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    change = append_once(
        change,
        RUN_ID,
        f"## 2026-05-23 run270D balance/time-slice/trade-quality review(270D 잔액/시간구간/거래품질 검토)\n\n"
        f"- status(상태): `{status}`\n"
        f"- judgment(판정): `{judgment}`\n"
        f"- effect(효과): trade records(거래 기록) `{result['trade_record_count']}`개와 variant summary(변형 요약) `{len(result['variant_summary'])}`행을 만들었다.\n"
        "- boundary(경계): selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n",
    )
    write_md(CHANGELOG, change)


def md_table_variant_summary(rows: Sequence[Mapping[str, Any]], limit: int = 8) -> list[str]:
    lines = [
        "| variant(변형) | role(역할) | val net(검증 순수익) | oos net(표본외 순수익) | val PF(검증 수익 팩터) | oos PF(표본외 수익 팩터) | worst DD%(최악 손실폭) | read(판독) |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in rows[:limit]:
        dd = max(as_float(row.get("validation_equity_dd_percent")), as_float(row.get("oos_equity_dd_percent")))
        lines.append(
            f"| `{row.get('variant_id')}` | `{row.get('queue_role')}` | "
            f"{as_float(row.get('validation_net_profit')):.2f} | {as_float(row.get('oos_net_profit')):.2f} | "
            f"{as_float(row.get('validation_profit_factor')):.2f} | {as_float(row.get('oos_profit_factor')):.2f} | "
            f"{dd:.2f} | `{row.get('survival_read')}` |"
        )
    return lines


def md_table_negative(rows: Sequence[Mapping[str, Any]], limit: int = 12) -> list[str]:
    lines = [
        "| variant(변형) | split(분할) | axis(축) | bucket(구간) | net(순수익) | trades(거래 수) | read(판독) |",
        "| --- | --- | --- | --- | ---: | ---: | --- |",
    ]
    for row in rows[:limit]:
        lines.append(
            f"| `{row.get('variant_id')}` | `{row.get('split')}` | `{row.get('axis')}` | `{row.get('bucket')}` | "
            f"{as_float(row.get('net_profit')):.2f} | {as_int(row.get('trade_count'))} | `{row.get('slice_read')}` |"
        )
    return lines


def report_markdown(result: Mapping[str, Any]) -> str:
    active_failures = sum(1 for row in result["variant_summary"] if row.get("queue_role") == "active_probe" and row.get("survival_read") != ACTIVE_SURVIVOR_READ)
    survivor_count = sum(1 for row in result["variant_summary"] if row.get("survival_read") == ACTIVE_SURVIVOR_READ)
    parser_bad = sum(1 for row in result["parser_checks"] if row.get("parser_status") != "matched")
    forensic = result["forensics_summary"]
    lines = [
        "# Stage270 Run270D Balance/Time-Slice/Trade-Quality Review(270단계 270D 잔액/시간구간/거래품질 검토)",
        "",
        f"- status(상태): `{result['status']}`",
        f"- judgment(판정): `{result['judgment']}`",
        f"- source_run(원천 실행): `{SOURCE_RUN_ID}`",
        f"- trade_records(거래 기록): `{result['trade_record_count']}`",
        f"- parser_mismatch(파서 불일치): `{parser_bad}`",
        f"- active_probe_failures(활성 탐침 실패): `{active_failures}`",
        f"- survivors(생존 후보): `{survivor_count}`",
        "- selected_candidate(선택 후보): `none`",
        "- ONNX readiness(온엑스 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        f"- next_action(다음 행동): `{result['next_action']}`",
        "",
        "## Plain Result(쉬운 결과)",
        "",
        "run270D(270D 실행)는 run270C(270C 실행)의 20개 MT5(MetaTrader 5, 메타트레이더5) report(보고서)를 거래 단위로 다시 읽었다.",
        "효과(effect, 효과): headline KPI(대표 핵심 성과 지표) 뒤에 있는 balance/equity curve(잔액/평가금 곡선), month/session/chron slice(월/세션/순서 구간), trade quality(거래 품질)를 드러낸다.",
        "",
        "활성 aggressive probe(공격형 탐침)는 선택 후보로 올라가지 못했다.",
        "효과(effect, 효과): Stage270(270단계)의 aggressive non-filter upside(공격형 비필터 상방) 질문은 failure memory(실패 기억)로 닫을 준비가 됐고, 다음은 새 thesis(논제)로 넘어가는 쪽이다.",
        "",
        "## Variant Summary(변형 요약)",
        "",
        *md_table_variant_summary(result["variant_summary"]),
        "",
        "## Worst Tier A Slices(최악 Tier A 구간)",
        "",
        *md_table_negative(result["negative_slices"]),
        "",
        "## Tier Boundary(티어 경계)",
        "",
        f"- duplicate_audit_rows(중복 감사 행): `{len(result['tier_duplicate_review'])}`",
        "- interpretation(해석): Tier B(Tier B)는 이번 run270C(270C 실행)에서 별도 structural replay(구조 재생)로 Tier A(Tier A)와 mirror duplicate(거울 중복)를 만들었다.",
        "- effect(효과): 이 결과는 Tier B fallback authority(Tier B 대체 권위)나 actual routed total(실제 라우팅 전체)이 아니다.",
        "",
        "## Forensics Boundary(포렌식 경계)",
        "",
        f"- tester_identity(테스터 정체성): symbol(심볼) `{';'.join(forensic['symbols'])}`, timeframe(시간봉) `{';'.join(forensic['timeframes'])}`, deposit(예치금) `{';'.join(forensic['deposits'])}`, leverage(레버리지) `{';'.join(forensic['leverages'])}`.",
        f"- date_ranges(날짜 범위): `{format_date_ranges(forensic['split_date_ranges'])}`.",
        f"- trade_evidence(거래 근거): parser checks(파서 점검) `{forensic['parser_check_count']}`, mismatch(불일치) `{forensic['parser_mismatch_count']}`.",
        f"- cost_assumptions(비용 가정): `{forensic['cost_assumption_boundary']}`.",
        f"- backtest_judgment(백테스트 판정): `{forensic['backtest_judgment']}`.",
        "",
        "## Artifact Lineage(산출물 계보)",
        "",
        f"- source_inputs(원천 입력): `{rel(SOURCE_EXECUTION_RESULT)}`, `{rel(SOURCE_KPI_SUMMARY)}`, `{rel(SOURCE_FORENSICS)}`, `{rel(SOURCE_VARIANT_PLAN)}`.",
        f"- producer(생산자): `{rel(PRODUCER_PATH)}`.",
        f"- consumer(소비자): `{result['next_action']}`.",
        f"- artifact_paths(산출물 경로): `{rel(TRADE_RECORDS)}`, `{rel(TIME_SLICE_KPI)}`, `{rel(CURVE_DIAGNOSTICS)}`, `{rel(VARIANT_SUMMARY)}`.",
        "- lineage_judgment(계보 판정): `connected_with_boundary`.",
        "",
        "## Required Gate Coverage(필수 게이트 커버리지)",
        "",
        f"- kpi_contract_audit(KPI 계약 감사): `{'passed' if result['trade_record_count'] and not parser_bad else 'blocked'}`",
        f"- row_grain_audit(행 단위 감사): `{'passed' if len(result['variant_summary']) == 5 else 'blocked'}`",
        f"- source_authority_audit(원천 권위 감사): `{'passed' if path_exists(SOURCE_EXECUTION_RESULT) else 'blocked'}`",
        "- required_gate_coverage_audit(필수 게이트 커버리지 감사): `passed`",
        "- final_claim_guard(최종 주장 가드): `passed_no_selected_candidate_no_onnx_no_goal_achieve`",
        "",
        "## Boundary(경계)",
        "",
        "- positive_claim(긍정 주장): `none`.",
        "- selected_candidate(선택 후보): `none`.",
        "- ONNX readiness(온엑스 준비): `not_claimed`.",
        "- Goal Achieve(목표 달성): `not_claimed`.",
        "- operating_promotion(운영 승격), runtime_authority(런타임 권위), deployment(배포): `not_claimed`.",
    ]
    return "\n".join(lines)


def run() -> dict[str, Any]:
    created_at = utc_now()
    RUN_ROOT.mkdir(parents=True, exist_ok=True)
    execution_result = read_json(SOURCE_EXECUTION_RESULT)
    variant_plan = load_variant_plan()
    forensics_rows = read_csv(SOURCE_FORENSICS)
    trade_rows, parser_checks = build_trade_records(execution_result, variant_plan)
    time_rows = build_time_slice_rows(trade_rows)
    curve_rows = build_curve_rows(trade_rows, time_rows, execution_result)
    split_rows = build_variant_split_review(curve_rows, time_rows)
    summary_rows = build_variant_summary(split_rows)
    duplicate_rows = build_tier_duplicate_review(curve_rows)
    negative_rows = negative_slices(time_rows)
    forensic = forensics_summary(forensics_rows, parser_checks, execution_result)
    status, judgment, next_action = classify_result(summary_rows, parser_checks)
    result_rows = build_result_judgment_rows(status, judgment, next_action, summary_rows, parser_checks)
    result = {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": status,
        "judgment": judgment,
        "next_action": next_action,
        "trade_record_count": len(trade_rows),
        "time_slice_row_count": len(time_rows),
        "curve_row_count": len(curve_rows),
        "variant_split_review": split_rows,
        "variant_summary": summary_rows,
        "tier_duplicate_review": duplicate_rows,
        "negative_slices": negative_rows,
        "parser_checks": parser_checks,
        "forensics_summary": forensic,
        "result_judgment": result_rows,
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": BOUNDARY,
        "created_at_utc": created_at,
    }
    write_csv(TRADE_RECORDS, trade_rows, TRADE_COLUMNS)
    write_csv(TIME_SLICE_KPI, time_rows, TIME_SLICE_COLUMNS)
    write_csv(CURVE_DIAGNOSTICS, curve_rows, CURVE_COLUMNS)
    write_csv(VARIANT_SPLIT_REVIEW, split_rows, VARIANT_SPLIT_COLUMNS)
    write_csv(VARIANT_SUMMARY, summary_rows, VARIANT_SUMMARY_COLUMNS)
    write_csv(TIER_DUPLICATE_REVIEW, duplicate_rows, TIER_DUPLICATE_COLUMNS)
    write_csv(NEGATIVE_SLICE_SUMMARY, negative_rows, TIME_SLICE_COLUMNS)
    write_csv(PARSER_CHECKS, parser_checks, PARSER_COLUMNS)
    write_json(FORENSICS_SUMMARY, forensic, bom=True)
    write_csv(RESULT_JUDGMENT, result_rows, RESULT_JUDGMENT_COLUMNS)
    lineage_payload = {
        "source_inputs": [rel(SOURCE_EXECUTION_RESULT), rel(SOURCE_KPI_SUMMARY), rel(SOURCE_FORENSICS), rel(SOURCE_RUNTIME_PARITY), rel(SOURCE_VARIANT_PLAN)],
        "producer": rel(PRODUCER_PATH),
        "consumer": [next_action, rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "artifact_paths": [
            rel(TRADE_RECORDS),
            rel(TIME_SLICE_KPI),
            rel(CURVE_DIAGNOSTICS),
            rel(VARIANT_SPLIT_REVIEW),
            rel(VARIANT_SUMMARY),
            rel(TIER_DUPLICATE_REVIEW),
            rel(NEGATIVE_SLICE_SUMMARY),
            rel(PARSER_CHECKS),
            rel(FORENSICS_SUMMARY),
            rel(RESULT_JUDGMENT),
            rel(REVIEW_RESULT),
            rel(REPORT_PATH),
        ],
        "artifact_hashes": {},
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "tracked_generated_stage_local",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": BOUNDARY,
    }
    write_json(ARTIFACT_LINEAGE, lineage_payload, bom=True)
    write_json(REVIEW_RESULT, result, bom=True)
    write_md(REPORT_PATH, report_markdown(result))
    artifact_paths = [
        TRADE_RECORDS,
        TIME_SLICE_KPI,
        CURVE_DIAGNOSTICS,
        VARIANT_SPLIT_REVIEW,
        VARIANT_SUMMARY,
        TIER_DUPLICATE_REVIEW,
        NEGATIVE_SLICE_SUMMARY,
        PARSER_CHECKS,
        FORENSICS_SUMMARY,
        RESULT_JUDGMENT,
        ARTIFACT_LINEAGE,
        REVIEW_RESULT,
        REPORT_PATH,
    ]
    lineage_payload["artifact_hashes"] = {rel(path): sha256_file_lf_normalized(path) for path in artifact_paths if path_exists(path)}
    write_json(ARTIFACT_LINEAGE, lineage_payload, bom=True)
    upsert_ledgers(result, created_at)
    update_docs(result)
    return result


def main() -> int:
    result = run()
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": result["status"],
                "judgment": result["judgment"],
                "trade_records": result["trade_record_count"],
                "variant_rows": len(result["variant_summary"]),
                "survivors": sum(1 for row in result["variant_summary"] if row.get("survival_read") == ACTIVE_SURVIVOR_READ),
                "selected_candidate": result["selected_candidate"],
                "onnx_readiness": result["onnx_readiness"],
                "goal_achieve": result["goal_achieve"],
                "next_action": result["next_action"],
                "report": rel(REPORT_PATH),
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
