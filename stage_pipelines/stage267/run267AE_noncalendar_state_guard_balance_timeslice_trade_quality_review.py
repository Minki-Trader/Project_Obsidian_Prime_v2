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

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    path_exists,
    read_csv_rows,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from foundation.mt5.trade_report import pair_deals_into_trades, parse_mt5_trade_report
from stage_pipelines.stage267 import run267AD_noncalendar_state_guard_score_table_mt5_executor as source_executor


STAGE_ID = source_executor.STAGE_ID
RUN_ID = "run267AE_stage267_noncalendar_state_guard_balance_timeslice_trade_quality_review_v1"
RUN_NUMBER = "run267AE"
PARENT_RUN_ID = source_executor.RUN_ID
STATUS = "run267AE_noncalendar_state_guard_balance_timeslice_trade_quality_review_completed"
PARTIAL_STATUS = "run267AE_noncalendar_state_guard_balance_timeslice_trade_quality_review_partial_parser_errors"
JUDGMENT = "diagnostic_curve_timeslice_trade_quality_review_completed_no_candidate_selection"
PARTIAL_JUDGMENT = "diagnostic_review_partial_parser_errors_no_candidate_selection"
CLAIM_BOUNDARY = source_executor.CLAIM_BOUNDARY
NEXT_ACTION = "run267AF_noncalendar_state_guard_followup_or_prune_design"
NEXT_ACTION_PARTIAL = "run267AE_repair_noncalendar_state_guard_trade_report_parser_errors"

STAGE_ROOT = source_executor.STAGE_ROOT
REVIEWS_ROOT = source_executor.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "noncalendar_state_guard_balance_timeslice_trade_quality_review"

SOURCE_EXECUTION_RESULT_PATH = source_executor.EXECUTION_RESULT_PATH
SOURCE_KPI_SUMMARY_PATH = source_executor.KPI_SUMMARY_PATH
SOURCE_FORENSICS_PATH = source_executor.FORENSICS_PATH
SOURCE_EXECUTED_ATTEMPTS_PATH = source_executor.EXECUTED_ATTEMPTS_PATH

TRADE_RECORDS_PATH = RUN_ROOT / "trade_records.csv"
TIME_SLICE_KPI_PATH = RUN_ROOT / "time_slice_kpi.csv"
CURVE_DIAGNOSTICS_PATH = RUN_ROOT / "curve_diagnostics.csv"
CANDIDATE_TEST_REVIEW_PATH = RUN_ROOT / "candidate_test_review.csv"
CANDIDATE_SUMMARY_PATH = RUN_ROOT / "candidate_balance_timeslice_summary.csv"
GUARD_AXIS_SUMMARY_PATH = RUN_ROOT / "guard_axis_balance_timeslice_summary.csv"
NEGATIVE_SLICE_PATH = RUN_ROOT / "negative_slice_summary.csv"
PARSER_CHECKS_PATH = RUN_ROOT / "parser_checks.csv"
PARSER_ERRORS_PATH = RUN_ROOT / "parser_errors.csv"
TIER_DUPLICATE_REVIEW_PATH = RUN_ROOT / "tier_duplicate_review.csv"
REVIEW_RESULT_PATH = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267AE_noncalendar_state_guard_balance_timeslice_trade_quality_review.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267AE_noncalendar_state_guard_balance_timeslice_trade_quality_review.py")

STAGE_LEDGER_PATH = source_executor.STAGE_LEDGER_PATH
PROJECT_LEDGER_PATH = source_executor.PROJECT_LEDGER_PATH
RUN_REGISTRY_PATH = source_executor.RUN_REGISTRY_PATH
ARTIFACT_REGISTRY_PATH = source_executor.ARTIFACT_REGISTRY_PATH
CURRENT_WORKING_STATE_PATH = source_executor.CURRENT_WORKING_STATE_PATH
WORKSPACE_STATE_PATH = source_executor.WORKSPACE_STATE_PATH
SELECTION_STATUS_PATH = source_executor.SELECTION_STATUS_PATH
REVIEW_INDEX_PATH = source_executor.REVIEW_INDEX_PATH

STAGE_LEDGER_COLUMNS = source_executor.STAGE_LEDGER_COLUMNS
ARTIFACT_COLUMNS = source_executor.ARTIFACT_COLUMNS

DEPOSIT = 500.0
AXES = ("month", "weekday", "close_hour_report", "session_report", "direction", "chron_segment")
METRIC_COLUMNS = (
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
)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.relative_to(REPO_ROOT).as_posix()
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


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
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


def write_text(path: Path, text: str) -> None:
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
    underwater = 0
    underwater_count = 0
    for row in sorted(rows, key=lambda item: str(item.get("close_time"))):
        balance += as_float(row.get("net_profit"))
        if balance >= peak:
            peak = balance
            underwater = 0
        else:
            underwater += 1
            underwater_count += 1
            longest_underwater = max(longest_underwater, underwater)
        drawdown = peak - balance
        drawdown_pct = drawdown / peak * 100.0 if peak else 0.0
        max_dd = max(max_dd, drawdown)
        max_dd_pct = max(max_dd_pct, drawdown_pct)
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
    drawdown, drawdown_pct, underwater, underwater_share = max_closed_balance_drawdown(ordered)
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
        "closed_balance_max_drawdown": drawdown,
        "closed_balance_max_drawdown_percent": drawdown_pct,
        "longest_underwater_trades": underwater,
        "underwater_trade_share": underwater_share,
        "max_losing_streak": max_losing_streak(ordered),
        "recovery_factor_closed": net / drawdown if drawdown else None,
    }


def slice_read(item: Mapping[str, Any]) -> str:
    net = as_float(item.get("net_profit"))
    pf = as_float(item.get("profit_factor"))
    trades = as_int(item.get("trade_count"))
    drawdown_pct = as_float(item.get("closed_balance_max_drawdown_percent"))
    if trades < 3:
        return "too_thin_to_read"
    if net < 0.0 and drawdown_pct >= 18.0:
        return "negative_deep_drawdown_slice"
    if net < 0.0:
        return "negative_slice"
    if pf >= 1.4 and net > 0.0:
        return "constructive_slice"
    return "mixed_slice"


def curve_read(item: Mapping[str, Any], report_metrics: Mapping[str, Any], month_rows: Sequence[Mapping[str, Any]]) -> str:
    net = as_float(item.get("net_profit"))
    pf = as_float(item.get("profit_factor"))
    equity_dd = as_float(report_metrics.get("equity_drawdown_maximal_percent") or item.get("closed_balance_max_drawdown_percent"))
    trades = as_int(item.get("trade_count"))
    negative_months = [row for row in month_rows if as_float(row.get("net_profit")) < 0.0]
    worst_month_net = min((as_float(row.get("net_profit")) for row in month_rows), default=0.0)
    positive_month_ratio = (len(month_rows) - len(negative_months)) / len(month_rows) if month_rows else 0.0
    if net <= 0.0 or pf <= 1.0:
        return "fragile_or_negative_no_extension"
    if equity_dd >= 30.0 or worst_month_net <= -180.0:
        return "dd_or_month_hole_uncomfortable"
    if trades >= 300 and net >= 900.0 and pf >= 1.35 and equity_dd <= 22.0 and positive_month_ratio >= 0.5:
        return "constructive_curve_watch_not_selection"
    if trades >= 250 and net >= 500.0 and pf >= 1.18 and equity_dd < 30.0:
        return "mixed_constructive_needs_more_pressure"
    return "mixed_or_fragile"


def attempt_by_name(execution_result: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {str(item.get("attempt_name")): item for item in execution_result.get("attempts_executed", [])}


def build_trade_records(execution_result: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    attempts = attempt_by_name(execution_result)
    rows: list[dict[str, Any]] = []
    parser_errors: list[dict[str, Any]] = []
    parser_checks: list[dict[str, Any]] = []
    for record in execution_result.get("mt5_kpi_records", []):
        if record.get("status") != "completed":
            continue
        report = record.get("report", {})
        attempt_name = str(report.get("attempt_name") or "")
        attempt = attempts.get(attempt_name, {})
        metrics_payload = record.get("metrics", {})
        html_path = Path(str(metrics_payload.get("report_path") or report.get("html_report", {}).get("path") or ""))
        if not html_path.is_absolute():
            html_path = REPO_ROOT / html_path
        try:
            parsed = parse_mt5_trade_report(html_path)
            trades = pair_deals_into_trades(parsed["deals"])
        except Exception as exc:  # pragma: no cover - persisted as evidence.
            parser_errors.append({"attempt_name": attempt_name, "report_path": rel(html_path), "error": str(exc)})
            continue
        expected_count = as_int(metrics_payload.get("trade_count"))
        parser_checks.append(
            {
                "attempt_name": attempt_name,
                "record_view": record.get("record_view"),
                "tier_scope": record.get("tier_scope"),
                "report_path": rel(html_path),
                "expected_trade_count": expected_count,
                "parsed_trade_count": len(trades),
                "trade_count_delta": len(trades) - expected_count,
                "parser_status": "matched" if len(trades) == expected_count else "count_mismatch",
            }
        )
        ordered = sorted(trades, key=lambda item: item.close_time)
        total = len(ordered)
        for index, trade in enumerate(ordered):
            close_time = trade.close_time
            open_time = trade.open_time
            close_hour = close_time.strftime("%H")
            test_id = attempt.get("source_test_id")
            rows.append(
                {
                    "run_id": RUN_ID,
                    "source_run_id": PARENT_RUN_ID,
                    "queue_id": attempt.get("queue_id"),
                    "candidate_id": attempt.get("candidate_id"),
                    "candidate_alias": attempt.get("candidate_alias"),
                    "candidate_role": attempt.get("candidate_role"),
                    "test_id": test_id,
                    "guard_rule_family": attempt.get("guard_rule_family"),
                    "model_materialization_type": attempt.get("model_materialization_type"),
                    "materialization_boundary": "noncalendar_state_guard_score_table_extension_not_retrained",
                    "record_view": record.get("record_view"),
                    "attempt_name": attempt_name,
                    "tier_scope": record.get("tier_scope"),
                    "route_role": record.get("route_role"),
                    "split": record.get("split"),
                    "fallback_enabled": str(attempt.get("fallback_enabled", False)).lower(),
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
                    "gross_profit": trade.gross_profit,
                    "net_profit": trade.net_profit,
                    "commission": trade.commission,
                    "swap": trade.swap,
                    "source_report_path": rel(html_path),
                }
            )
    return rows, parser_errors, parser_checks


def build_time_slice_rows(trade_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for axis in AXES:
        keys = (
            "record_view",
            "tier_scope",
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "test_id",
            "guard_rule_family",
            "materialization_boundary",
            "route_role",
            axis,
        )
        for key, rows in group_rows(trade_rows, keys).items():
            record_view, tier_scope, candidate_id, alias, role, test_id, guard_family, boundary, route_role, bucket = key
            item = metrics(rows)
            output.append(
                {
                    "record_view": record_view,
                    "tier_scope": tier_scope,
                    "candidate_id": candidate_id,
                    "candidate_alias": alias,
                    "candidate_role": role,
                    "test_id": test_id,
                    "guard_rule_family": guard_family,
                    "materialization_boundary": boundary,
                    "route_role": route_role,
                    "axis": axis,
                    "bucket": bucket,
                    **item,
                    "slice_read": slice_read(item),
                }
            )
    return output


def kpi_records_by_view(execution_result: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {str(record.get("record_view")): record.get("metrics", {}) for record in execution_result.get("mt5_kpi_records", [])}


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
    keys = (
        "record_view",
        "tier_scope",
        "candidate_id",
        "candidate_alias",
        "candidate_role",
        "test_id",
        "guard_rule_family",
        "materialization_boundary",
        "route_role",
    )
    for key, rows in group_rows(trade_rows, keys).items():
        record_view, tier_scope, candidate_id, alias, role, test_id, guard_family, boundary, route_role = key
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
                "record_view": record_view,
                "tier_scope": tier_scope,
                "candidate_id": candidate_id,
                "candidate_alias": alias,
                "candidate_role": role,
                "test_id": test_id,
                "guard_rule_family": guard_family,
                "materialization_boundary": boundary,
                "route_role": route_role,
                **item,
                "report_equity_drawdown_percent": report_metrics.get("equity_drawdown_maximal_percent"),
                "report_balance_drawdown_percent": report_metrics.get("balance_drawdown_maximal_percent"),
                "report_recovery_factor": report_metrics.get("recovery_factor"),
                "tier_b_fallback_used_count": report_metrics.get("tier_b_fallback_used_count"),
                "tier_b_fallback_order_fill_count": report_metrics.get("tier_b_fallback_order_fill_count"),
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


def negative_slices(time_rows: Sequence[Mapping[str, Any]], limit: int = 120) -> list[dict[str, Any]]:
    negative = [dict(row) for row in time_rows if row.get("tier_scope") == "Tier A" and as_float(row.get("net_profit")) < 0.0]
    negative.sort(key=lambda row: as_float(row.get("net_profit")))
    return negative[:limit]


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


def build_candidate_test_review(
    curve_rows: Sequence[Mapping[str, Any]],
    time_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for row in sorted(curve_rows, key=lambda item: (str(item.get("candidate_alias")), str(item.get("test_id")), str(item.get("tier_scope")))):
        if row.get("tier_scope") != "Tier A":
            continue
        worst = worst_slice_for(str(row.get("record_view")), time_rows)
        equity_dd = as_float(row.get("report_equity_drawdown_percent") or row.get("closed_balance_max_drawdown_percent"))
        worst_month_net = as_float(row.get("worst_month_net"))
        worst_slice_net = as_float(worst.get("net_profit"))
        curve = str(row.get("curve_read"))
        fragility_flags: list[str] = []
        if equity_dd >= 24.0:
            fragility_flags.append("dd_watch")
        if worst_month_net <= -120.0:
            fragility_flags.append("month_hole")
        if worst_slice_net <= -150.0:
            fragility_flags.append("deep_slice_hole")
        if as_int(row.get("trade_count")) < 250:
            fragility_flags.append("thin_trade_count")
        if as_float(row.get("profit_factor")) < 1.2:
            fragility_flags.append("pf_thin")
        if not fragility_flags:
            fragility_flags.append("no_major_flag_in_this_review")
        output.append(
            {
                "candidate_alias": row.get("candidate_alias"),
                "candidate_id": row.get("candidate_id"),
                "candidate_role": row.get("candidate_role"),
                "test_id": row.get("test_id"),
                "guard_rule_family": row.get("guard_rule_family"),
                "record_view": row.get("record_view"),
                "tier_scope": row.get("tier_scope"),
                "net_profit": row.get("net_profit"),
                "profit_factor": row.get("profit_factor"),
                "trade_count": row.get("trade_count"),
                "expectancy": row.get("expectancy"),
                "win_rate": row.get("win_rate"),
                "payoff_ratio": row.get("payoff_ratio"),
                "report_equity_drawdown_percent": row.get("report_equity_drawdown_percent"),
                "closed_balance_max_drawdown_percent": row.get("closed_balance_max_drawdown_percent"),
                "recovery_factor_closed": row.get("recovery_factor_closed"),
                "positive_month_ratio": row.get("positive_month_ratio"),
                "negative_month_count": row.get("negative_month_count"),
                "worst_month": row.get("worst_month"),
                "worst_month_net": row.get("worst_month_net"),
                "best_month": row.get("best_month"),
                "best_month_net": row.get("best_month_net"),
                "chron_early_net": row.get("chron_early_net"),
                "chron_mid_net": row.get("chron_mid_net"),
                "chron_late_net": row.get("chron_late_net"),
                "worst_slice_axis": worst.get("axis", ""),
                "worst_slice_bucket": worst.get("bucket", ""),
                "worst_slice_net": worst.get("net_profit", ""),
                "worst_slice_trade_count": worst.get("trade_count", ""),
                "fragility_flags": ";".join(fragility_flags),
                "curve_read": curve,
                "review_read": "watch_for_followup" if curve.startswith("constructive") else "needs_pressure_or_prune",
                "selection_boundary": "not_candidate_selection",
            }
        )
    output.sort(
        key=lambda row: (
            0 if str(row.get("curve_read")).startswith("constructive") else 1,
            -as_float(row.get("net_profit")),
        )
    )
    return output


def build_candidate_summary(candidate_tests: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    grouped = group_rows(candidate_tests, ("candidate_alias", "candidate_id", "candidate_role"))
    output: list[dict[str, Any]] = []
    for key, rows in sorted(grouped.items()):
        alias, candidate_id, role = key
        nets = [as_float(row.get("net_profit")) for row in rows]
        pfs = [as_float(row.get("profit_factor")) for row in rows]
        dds = [as_float(row.get("report_equity_drawdown_percent")) for row in rows]
        trades = [as_int(row.get("trade_count")) for row in rows]
        worst_months = [as_float(row.get("worst_month_net")) for row in rows]
        constructive = [row for row in rows if str(row.get("curve_read")).startswith("constructive")]
        deep_flags = [
            row
            for row in rows
            if "month_hole" in str(row.get("fragility_flags")) or "deep_slice_hole" in str(row.get("fragility_flags"))
        ]
        output.append(
            {
                "candidate_alias": alias,
                "candidate_id": candidate_id,
                "candidate_role": role,
                "tier_a_test_count": len(rows),
                "constructive_curve_count": len(constructive),
                "constructive_curve_share": len(constructive) / len(rows) if rows else None,
                "deep_hole_flag_count": len(deep_flags),
                "net_profit_min": min(nets) if nets else None,
                "net_profit_max": max(nets) if nets else None,
                "net_profit_mean": mean(nets) if nets else None,
                "profit_factor_min": min(pfs) if pfs else None,
                "profit_factor_max": max(pfs) if pfs else None,
                "equity_drawdown_percent_worst": max(dds) if dds else None,
                "trade_count_total": sum(trades),
                "trade_count_min": min(trades) if trades else None,
                "trade_count_max": max(trades) if trades else None,
                "worst_month_net_min": min(worst_months) if worst_months else None,
                "summary_read": "candidate_has_constructive_clues_but_not_selected" if constructive else "candidate_needs_pressure_or_prune",
            }
        )
    output.sort(key=lambda row: (-as_float(row.get("constructive_curve_count")), -as_float(row.get("net_profit_mean"))))
    return output


def build_guard_axis_summary(candidate_tests: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    grouped = group_rows(candidate_tests, ("test_id", "guard_rule_family"))
    output: list[dict[str, Any]] = []
    for key, rows in sorted(grouped.items()):
        test_id, guard_family = key
        nets = [as_float(row.get("net_profit")) for row in rows]
        dds = [as_float(row.get("report_equity_drawdown_percent")) for row in rows]
        constructive = [row for row in rows if str(row.get("curve_read")).startswith("constructive")]
        output.append(
            {
                "test_id": test_id,
                "guard_rule_family": guard_family,
                "candidate_count": len({row.get("candidate_alias") for row in rows}),
                "row_count": len(rows),
                "constructive_curve_count": len(constructive),
                "net_profit_mean": mean(nets) if nets else None,
                "net_profit_min": min(nets) if nets else None,
                "net_profit_max": max(nets) if nets else None,
                "equity_drawdown_percent_worst": max(dds) if dds else None,
                "axis_read": "useful_axis_for_followup" if constructive else "weak_axis_or_needs_rework",
            }
        )
    output.sort(key=lambda row: (-as_float(row.get("constructive_curve_count")), -as_float(row.get("net_profit_mean"))))
    return output


def build_tier_duplicate_review(curve_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    grouped = group_rows(curve_rows, ("candidate_alias", "test_id"))
    for key, rows in sorted(grouped.items()):
        ta = next((row for row in rows if row.get("tier_scope") == "Tier A"), None)
        rt = next((row for row in rows if row.get("tier_scope") == "Tier A+B"), None)
        if not ta or not rt:
            status = "missing_pair"
            net_delta: float | str = ""
            trade_delta: int | str = ""
        else:
            net_delta = as_float(rt.get("net_profit")) - as_float(ta.get("net_profit"))
            trade_delta = as_int(rt.get("trade_count")) - as_int(ta.get("trade_count"))
            status = "duplicate_due_to_fallback_disabled" if abs(net_delta) < 1e-9 and trade_delta == 0 else "tier_pair_differs"
        output.append(
            {
                "candidate_alias": key[0],
                "test_id": key[1],
                "tier_pair_present": bool(ta and rt),
                "net_profit_delta_tier_ab_minus_tier_a": net_delta,
                "trade_count_delta_tier_ab_minus_tier_a": trade_delta,
                "audit_status": status,
                "interpretation": "not_routed_fallback_evidence" if status == "duplicate_due_to_fallback_disabled" else "inspect_pair",
            }
        )
    return output


def forensics_summary(rows: Sequence[Mapping[str, str]]) -> dict[str, Any]:
    terminals = sorted({row.get("terminal", "") for row in rows if row.get("terminal")})
    symbols = sorted({row.get("symbol", "") for row in rows if row.get("symbol")})
    timeframes = sorted({row.get("timeframe", "") for row in rows if row.get("timeframe")})
    deposits = sorted({row.get("deposit", "") for row in rows if row.get("deposit")})
    leverages = sorted({row.get("leverage", "") for row in rows if row.get("leverage")})
    models = sorted({row.get("model", "") for row in rows if row.get("model")})
    from_dates = sorted({row.get("from_date", "") for row in rows if row.get("from_date")})
    to_dates = sorted({row.get("to_date", "") for row in rows if row.get("to_date")})
    statuses = sorted({row.get("tester_status", "") for row in rows if row.get("tester_status")})
    report_missing = [row.get("attempt_name", "") for row in rows if not row.get("report_path")]
    return {
        "row_count": len(rows),
        "tester_statuses": statuses,
        "terminal_count": len(terminals),
        "terminals": terminals,
        "symbols": symbols,
        "timeframes": timeframes,
        "deposits": deposits,
        "leverages": leverages,
        "models": models,
        "from_dates": from_dates,
        "to_dates": to_dates,
        "report_missing_count": len(report_missing),
        "cost_assumption_boundary": "spread_commission_slippage_follow_strategy_tester_report_no_cost_edge_claim",
        "backtest_judgment": "usable_with_boundary" if rows and not report_missing else "inconclusive",
    }


def result_status(parser_errors: Sequence[Mapping[str, Any]], parser_checks: Sequence[Mapping[str, Any]]) -> str:
    count_mismatch = [row for row in parser_checks if row.get("parser_status") != "matched"]
    return PARTIAL_STATUS if parser_errors or count_mismatch else STATUS


def result_judgment(status: str) -> str:
    return PARTIAL_JUDGMENT if status == PARTIAL_STATUS else JUDGMENT


def result_next_action(status: str) -> str:
    return NEXT_ACTION_PARTIAL if status == PARTIAL_STATUS else NEXT_ACTION


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def remove_line_prefix(text: str, prefix: str) -> str:
    return "\n".join([line for line in text.splitlines() if not line.startswith(prefix)]) + "\n"


def append_after_contains(text: str, needle: str, line: str) -> str:
    if line in text:
        return text
    lines = text.splitlines()
    for index, existing in enumerate(lines):
        if needle in existing:
            lines.insert(index + 1, line)
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + line + "\n"


def append_block_once(text: str, unique_text: str, block: str) -> str:
    if unique_text in text:
        return text
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def update_workspace_state_text(text: str, result: Mapping[str, Any]) -> str:
    status = str(result["status"])
    next_action = str(result["next_action"])
    lines = text.splitlines()
    out: list[str] = []
    in_stage267 = False
    inserted_report_path = False
    skip_current_focus_block = False
    focus_block = [
        "- >-",
        f"  Stage267(267단계) run267AE(267AE 실행) noncalendar state guard balance/time-slice/trade-quality review(비달력 상태 방어 잔액/시간구간/거래품질 검토) `{status}`. Effect(효과): run267AD(267AD 실행)의 14개 MT5(MetaTrader 5, 메타트레이더5) 보고서를 거래 목록, 곡선, 약한 구간으로 검토했고 selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.",
    ]
    focus_inserted = False
    seen_stage267_report_paths: set[str] = set()
    index = 0
    while index < len(lines):
        line = lines[index]
        next_line = lines[index + 1] if index + 1 < len(lines) else ""
        if line.startswith("current_run_id:"):
            out.append(f"current_run_id: {RUN_ID}")
            index += 1
            continue
        if line == "current_focus:" and not focus_inserted:
            out.append(line)
            out.extend(focus_block)
            focus_inserted = True
            index += 1
            continue
        if line == "- >-" and (
            ("run267AE" in next_line and "noncalendar state guard balance/time-slice/trade-quality review" in next_line)
            or ("run267AD" in next_line and "noncalendar state guard score table MT5 execution" in next_line)
            or ("Next action(다음 행동)는 `run267AD_execute_noncalendar_state_guard_score_table_mt5_batch`" in next_line)
        ):
            skip_current_focus_block = True
            index += 2
            continue
        if skip_current_focus_block:
            skip_current_focus_block = False
        if line.startswith("stage267_baseline_candidate_racing_protocol:"):
            in_stage267 = True
            out.append(line)
            index += 1
            continue
        if in_stage267 and line and not line.startswith(" ") and not line.startswith("#"):
            in_stage267 = False
        if in_stage267:
            stripped = line.strip()
            if stripped.startswith("status:"):
                out.append(f"  status: {status}")
                index += 1
                continue
            if stripped.startswith("current_run_id:"):
                out.append(f"  current_run_id: {RUN_ID}")
                index += 1
                continue
            if stripped.startswith("last_completed_run_id:"):
                out.append(f"  last_completed_run_id: {RUN_ID}")
                index += 1
                continue
            if stripped.startswith("next_action:"):
                out.append(f"  next_action: {next_action}")
                index += 1
                continue
            if (
                "run267AD_noncalendar_state_guard_score_table_mt5_execution_report_path" in stripped
                or "run267AE_noncalendar_state_guard_balance_timeslice_trade_quality_review_report_path" in stripped
            ):
                if stripped in seen_stage267_report_paths:
                    index += 1
                    continue
                seen_stage267_report_paths.add(stripped)
            if "run267AE_noncalendar_state_guard_balance_timeslice_trade_quality_review_report_path" in stripped:
                if not inserted_report_path:
                    out.append(line)
                    inserted_report_path = True
                index += 1
                continue
            if "run267AD_noncalendar_state_guard_score_table_mt5_execution_report_path" in stripped and not inserted_report_path:
                out.append(line)
                out.append(f"  run267AE_noncalendar_state_guard_balance_timeslice_trade_quality_review_report_path: {rel(REPORT_PATH)}")
                inserted_report_path = True
                index += 1
                continue
        out.append(line)
        index += 1
    if in_stage267 and not inserted_report_path:
        out.append(f"  run267AE_noncalendar_state_guard_balance_timeslice_trade_quality_review_report_path: {rel(REPORT_PATH)}")
    return "\n".join(out) + "\n"


def update_current_truth_docs(result: Mapping[str, Any]) -> None:
    status = str(result["status"])
    next_action = str(result["next_action"])
    report_line = f"- run267AE_noncalendar_state_guard_balance_timeslice_trade_quality_review(267AE 비달력 상태 방어 잔액/시간구간/거래품질 검토): `{rel(REPORT_PATH)}`"
    latest_line = (
        "- latest_mt5_review(최신 MT5 검토): run267AE(267AE 실행) "
        f"trade records(거래 기록) `{result['trade_record_count']}`, "
        f"candidate-test rows(후보-시험 행) `{len(result['candidate_test_review'])}`, "
        f"constructive curve rows(건설적 곡선 행) `{result['constructive_curve_rows']}`, "
        f"negative Tier A slices(음수 Tier A 구간) `{len(result['negative_slices'])}`, "
        f"report(보고서) `{rel(REPORT_PATH)}`."
    )
    closing_block = "\n".join(
        [
            "Run267AE(267AE 실행)는 run267AD(267AD 실행)의 noncalendar state guard score table MT5 reports(비달력 상태 방어 점수표 MT5 보고서)를 거래 단위로 다시 읽었다.",
            "Effect(효과): headline KPI(대표 핵심 성과 지표)만 보지 않고 balance/equity curve(잔액/평가금 곡선), weak slice(약한 구간), trade quality(거래 품질)를 다음 연구 입력으로 고정한다.",
            "Boundary(경계): selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`이다.",
        ]
    )
    for path in (CURRENT_WORKING_STATE_PATH, SELECTION_STATUS_PATH, REVIEW_INDEX_PATH):
        text = io_path(path).read_text(encoding="utf-8-sig")
        if path == SELECTION_STATUS_PATH:
            text = replace_line_prefix(text, "- stage_status(", f"- stage_status(단계 상태): `{status}`")
            text = remove_line_prefix(text, "- status(")
        else:
            text = replace_line_prefix(text, "- status(", f"- status(상태): `{status}`")
        text = replace_line_prefix(text, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
        if path != CURRENT_WORKING_STATE_PATH:
            text = replace_line_prefix(text, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
        text = replace_line_prefix(text, "- next_action(", f"- next_action(다음 행동): `{next_action}`")
        if path == CURRENT_WORKING_STATE_PATH:
            text = replace_line_prefix(text, "- next_run(", f"- next_run(다음 실행): `{next_action}`")
            text = replace_line_prefix(
                text,
                "- adapter_under_review(",
                "- adapter_under_review(검토 중 어댑터): `noncalendar_state_guard_balance_timeslice_trade_quality_review`",
            )
            text = replace_line_prefix(
                text,
                "- action(",
                "- action(행동): run267AE(267AE 실행)는 run267AD(267AD 실행)의 14개 noncalendar state guard MT5 reports(비달력 상태 방어 MT5 보고서)를 거래 단위로 검토했다.",
            )
            text = replace_line_prefix(
                text,
                "- effect(",
                "- effect(효과): balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간구간 핵심 성과 지표), trade quality(거래 품질)를 다음 follow-up/prune design(후속/가지치기 설계)의 입력으로 만들었다.",
            )
            text = append_after_contains(text, "stage267_run267AD_noncalendar_state_guard_score_table_mt5_execution.md", report_line)
            text = append_after_contains(text, "## Current Next Action", latest_line)
        else:
            text = append_after_contains(text, "stage267_run267AD_noncalendar_state_guard_score_table_mt5_execution.md", report_line)
        text = append_block_once(text, "Run267AE(267AE 실행)는 run267AD", closing_block)
        write_md(path, text)
    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    write_text(WORKSPACE_STATE_PATH, update_workspace_state_text(workspace, result))


def update_ledgers(created_at: str, result: Mapping[str, Any]) -> None:
    status = str(result["status"])
    judgment = str(result["judgment"])
    next_action = str(result["next_action"])
    upsert_csv_rows(
        STAGE_LEDGER_PATH,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": "stage267_run267AE_noncalendar_state_guard_balance_timeslice_trade_quality_review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "noncalendar_state_guard_balance_timeslice_trade_quality_review",
                "tier_scope": "Tier A primary read plus Tier A+B duplicate boundary",
                "scoreboard": "trade_shape_curve_time_slice_review",
                "status": status,
                "judgment": judgment,
                "evidence_boundary": "diagnostic_review_no_candidate_selection_no_onnx",
                "report_path": rel(REPORT_PATH),
                "notes": (
                    f"candidate_test_rows={len(result['candidate_test_review'])};"
                    f"negative_slices={len(result['negative_slices'])};"
                    f"parser_errors={len(result['parser_errors'])};"
                    f"next_action={next_action};selected_candidate=none."
                ),
            }
        ],
        key="row_id",
    )
    upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_candidate_racing_noncalendar_state_guard_balance_timeslice_trade_quality_review",
                "status": status,
                "judgment": judgment,
                "path": rel(REPORT_PATH),
                "notes": (
                    "Run267AE balance/time-slice/trade-quality review from run267AD MT5 reports; "
                    f"selected_candidate=none; onnx_readiness=not_claimed; next_action={next_action}."
                ),
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        PROJECT_LEDGER_PATH,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__noncalendar_state_guard_balance_timeslice_trade_quality_review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": "noncalendar_state_guard_balance_timeslice_trade_quality_review",
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "noncalendar_state_guard_balance_timeslice_trade_quality_review",
                "tier_scope": "Tier A primary read plus Tier A+B duplicate boundary",
                "kpi_scope": "curve_time_slice_trade_quality_trade_shape_review",
                "scoreboard_lane": "trade_shape_curve_time_slice_review",
                "status": status,
                "judgment": judgment,
                "path": rel(REPORT_PATH),
                "primary_kpi": (
                    f"trade_records={result['trade_record_count']};"
                    f"candidate_test_rows={len(result['candidate_test_review'])};"
                    f"constructive_rows={result['constructive_curve_rows']}"
                ),
                "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
                "external_verification_status": "completed_for_run267AD_mt5_report_review",
                "notes": f"Next action: {next_action}.",
            }
        ],
        key="ledger_row_id",
    )
    entries = (
        ("stage267_run267AE_review_script", "producer_script", PRODUCER_PATH, "Builds run267AE noncalendar state guard curve/time-slice/trade-quality review."),
        ("stage267_run267AE_source_execution_result", "source_execution_result", SOURCE_EXECUTION_RESULT_PATH, "Source run267AD execution result."),
        ("stage267_run267AE_source_kpi_summary", "source_kpi_summary", SOURCE_KPI_SUMMARY_PATH, "Source run267AD KPI summary."),
        ("stage267_run267AE_source_forensics", "source_forensics", SOURCE_FORENSICS_PATH, "Source run267AD backtest forensics."),
        ("stage267_run267AE_source_attempts", "source_attempt_manifest", SOURCE_EXECUTED_ATTEMPTS_PATH, "Source run267AD executed attempts."),
        ("stage267_run267AE_trade_records", "trade_records", TRADE_RECORDS_PATH, "Run267AE paired trade records from run267AD reports."),
        ("stage267_run267AE_time_slice_kpi", "time_slice_kpi", TIME_SLICE_KPI_PATH, "Run267AE month/weekday/hour/session/direction/chron-segment KPI."),
        ("stage267_run267AE_curve_diagnostics", "curve_diagnostics", CURVE_DIAGNOSTICS_PATH, "Run267AE closed-balance curve diagnostics."),
        ("stage267_run267AE_candidate_test_review", "candidate_test_review", CANDIDATE_TEST_REVIEW_PATH, "Run267AE candidate-test curve and weak-slice review."),
        ("stage267_run267AE_candidate_summary", "candidate_summary", CANDIDATE_SUMMARY_PATH, "Run267AE candidate balance/time-slice summary."),
        ("stage267_run267AE_guard_axis_summary", "guard_axis_summary", GUARD_AXIS_SUMMARY_PATH, "Run267AE guard-axis summary."),
        ("stage267_run267AE_negative_slice_summary", "negative_slice_summary", NEGATIVE_SLICE_PATH, "Run267AE worst negative Tier A slices."),
        ("stage267_run267AE_parser_checks", "parser_checks", PARSER_CHECKS_PATH, "Run267AE parser reconciliation checks."),
        ("stage267_run267AE_parser_errors", "parser_errors", PARSER_ERRORS_PATH, "Run267AE parser errors."),
        ("stage267_run267AE_tier_duplicate_review", "audit_matrix", TIER_DUPLICATE_REVIEW_PATH, "Run267AE Tier A versus Tier A+B duplicate boundary."),
        ("stage267_run267AE_review_result", "review_result", REVIEW_RESULT_PATH, "Run267AE review JSON payload."),
        ("stage267_run267AE_review_report", "review_report", REPORT_PATH, "User-facing run267AE balance/time-slice/trade-quality review."),
    )
    rows = [
        {
            "artifact_id": artifact_id,
            "artifact_type": artifact_type,
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "missing",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": notes,
        }
        for artifact_id, artifact_type, path, notes in entries
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, rows, key="artifact_id")


def top_rows(rows: Sequence[Mapping[str, Any]], limit: int = 10) -> list[Mapping[str, Any]]:
    return list(rows[:limit])


def report_markdown(result: Mapping[str, Any]) -> str:
    candidate_tests = result["candidate_test_review"]
    candidate_summary = result["candidate_summary"]
    negative = result["negative_slices"][:12]
    forensic = result["forensics_summary"]
    lines = [
        "# Stage267 Run267AE Noncalendar State Guard Balance/Time-Slice/Trade-Quality Review(267단계 267AE 비달력 상태 방어 잔액/시간구간/거래품질 검토)",
        "",
        f"- action(행동): run267AD(267AD 실행)의 14개 MT5(MetaTrader 5, 메타트레이더5) 보고서를 trade list(거래 목록) 단위로 다시 읽었다.",
        "- effect(효과): headline KPI(대표 핵심 성과 지표)만 보지 않고 balance/equity curve(잔액/평가금 곡선), weak slice(약한 구간), trade quality(거래 품질)를 같이 본다.",
        f"- status(상태): `{result['status']}`",
        f"- judgment(판정): `{result['judgment']}`",
        f"- trade_records(거래 기록): `{result['trade_record_count']}`",
        f"- candidate_test_rows(후보-시험 행): `{len(candidate_tests)}`",
        f"- constructive_curve_rows(건설적 곡선 행): `{result['constructive_curve_rows']}`",
        f"- negative_tier_a_slices(음수 Tier A 구간): `{len(result['negative_slices'])}`",
        f"- parser_errors(파서 오류): `{len(result['parser_errors'])}`",
        "- selected_candidate(선택 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Easy Read(쉬운 해석)",
        "",
        "run267AE(267AE 실행)는 run267AD(267AD 실행)의 좋은 숫자가 실제 곡선과 약한 구간에서도 덜 깨지는지 확인했다.",
        "Effect(효과): 다음 run267AF(267AF 실행)는 숫자 1등을 고르는 대신, 어떤 guard axis(방어 축)를 더 누르고 어떤 분기는 prune(가지치기)할지 정할 수 있다.",
        "",
        "Tier A+B(Tier A+B 합산)는 이번 묶음에서 fallback disabled(대체 비활성)라 Tier A(Tier A)와 중복이다.",
        "Effect(효과): 이 결과를 routed robustness(라우팅 견고성) 근거로 쓰지 않고, duplicate boundary(중복 경계)로만 기록한다.",
        "",
        "## Candidate-Test Watchlist(후보-시험 관찰 목록)",
        "",
        "| rank(순위) | candidate(후보) | role(역할) | test(시험) | net profit(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실률) | worst month(최악 월) | worst slice(최악 구간) | read(판독) |",
        "| ---: | --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- | --- |",
    ]
    for index, row in enumerate(top_rows(candidate_tests), start=1):
        lines.append(
            f"| {index} | `{row.get('candidate_alias')}` | `{row.get('candidate_role')}` | `{row.get('test_id')}` | "
            f"{as_float(row.get('net_profit')):.2f} | {as_float(row.get('profit_factor')):.2f} | "
            f"{as_int(row.get('trade_count'))} | {as_float(row.get('report_equity_drawdown_percent')):.2f} | "
            f"`{row.get('worst_month')}` {as_float(row.get('worst_month_net')):.2f} | "
            f"`{row.get('worst_slice_axis')}`/`{row.get('worst_slice_bucket')}` {as_float(row.get('worst_slice_net')):.2f} | "
            f"`{row.get('curve_read')}` |"
        )
    lines.extend(
        [
            "",
            "## Candidate Summary(후보 요약)",
            "",
            "| candidate(후보) | role(역할) | tests(시험 수) | constructive(건설적 수) | holes(구멍 수) | net mean(평균 순수익) | net min(최소 순수익) | worst DD%(최악 손실률) | worst month net(최악 월 순수익) | read(판독) |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for row in candidate_summary:
        lines.append(
            f"| `{row.get('candidate_alias')}` | `{row.get('candidate_role')}` | {as_int(row.get('tier_a_test_count'))} | "
            f"{as_int(row.get('constructive_curve_count'))} | {as_int(row.get('deep_hole_flag_count'))} | "
            f"{as_float(row.get('net_profit_mean')):.2f} | {as_float(row.get('net_profit_min')):.2f} | "
            f"{as_float(row.get('equity_drawdown_percent_worst')):.2f} | {as_float(row.get('worst_month_net_min')):.2f} | "
            f"`{row.get('summary_read')}` |"
        )
    lines.extend(
        [
            "",
            "## Worst Tier A Slices(최악 Tier A 구간)",
            "",
            "| candidate(후보) | test(시험) | axis(축) | bucket(구간) | net profit(순수익) | trades(거래 수) | read(판독) |",
            "| --- | --- | --- | --- | ---: | ---: | --- |",
        ]
    )
    for row in negative:
        lines.append(
            f"| `{row.get('candidate_alias')}` | `{row.get('test_id')}` | `{row.get('axis')}` | `{row.get('bucket')}` | "
            f"{as_float(row.get('net_profit')):.2f} | {as_int(row.get('trade_count'))} | `{row.get('slice_read')}` |"
        )
    lines.extend(
        [
            "",
            "## Performance Attribution(성과 귀속)",
            "",
            "- observed_change(관찰 변화): noncalendar state guard(비달력 상태 방어)는 여러 후보에서 2024 순수익을 유지하거나 키웠지만, 최악 월과 최악 구간은 여전히 후보별로 다르다.",
            "- comparison_baseline(비교 기준): run267AD(267AD 실행)의 Tier A(Tier A) MT5(MetaTrader 5, 메타트레이더5) 결과만 1차 판독으로 쓰고, Tier A+B(Tier A+B 합산)는 중복 경계로 둔다.",
            "- likely_drivers(가능 원인): guard_rule_family(방어 규칙 계열)가 특정 달력 조건이 아니라 상태 기반 진입 필터로 작동해 거래 수를 크게 줄이지 않은 점은 긍정 단서다.",
            "- segment_checks(구간 점검): month(월), weekday(요일), session(세션), hour(시간), direction(방향), chron segment(시간순 구간)를 따로 저장했다.",
            "- alternative_explanations(대안 설명): 2024 단일 historical stress(과거 스트레스) 구간의 우연 적합이나 HTML parser(HTML 파서) 해석 문제는 parser_checks(파서 점검)로만 좁게 통제했다.",
            "- attribution_confidence(귀속 신뢰도): `medium_diagnostic_only`.",
            "- next_probe(다음 탐침): run267AF(267AF 실행)에서 constructive axis(건설적 축)는 follow-up(후속)하고 deep slice hole(깊은 구간 구멍)은 prune/repair(가지치기/수리) 경계로 나눈다.",
            "",
            "## Forensics Boundary(포렌식 경계)",
            "",
            f"- tester_identity(테스터 정체성): terminal count(터미널 수) `{forensic['terminal_count']}`, symbol(심볼) `{';'.join(forensic['symbols'])}`, timeframe(시간대) `{';'.join(forensic['timeframes'])}`, date range(날짜 범위) `{';'.join(forensic['from_dates'])}` to `{';'.join(forensic['to_dates'])}`.",
            f"- trade_evidence(거래 근거): trade records(거래 기록) `{result['trade_record_count']}`, parser checks(파서 점검) `{len(result['parser_checks'])}`.",
            f"- cost_assumptions(비용 가정): `{forensic['cost_assumption_boundary']}`.",
            f"- backtest_judgment(백테스트 판정): `{forensic['backtest_judgment']}`.",
            "",
            "## Artifact Lineage(산출물 계보)",
            "",
            f"- source_inputs(원천 입력): `{rel(SOURCE_EXECUTION_RESULT_PATH)}`, `{rel(SOURCE_KPI_SUMMARY_PATH)}`, `{rel(SOURCE_FORENSICS_PATH)}`, `{rel(SOURCE_EXECUTED_ATTEMPTS_PATH)}`.",
            f"- producer(생산자): `{rel(PRODUCER_PATH)}`.",
            f"- consumer(소비자): `{result['next_action']}`.",
            f"- artifact_paths(산출물 경로): `{rel(TRADE_RECORDS_PATH)}`, `{rel(TIME_SLICE_KPI_PATH)}`, `{rel(CURVE_DIAGNOSTICS_PATH)}`, `{rel(REVIEW_RESULT_PATH)}`.",
            "- lineage_judgment(계보 판정): `connected_with_boundary`.",
            "",
            "## Boundary(경계)",
            "",
            "- positive_claim(긍정 주장): `none`.",
            "- selected_candidate(선택 후보): `none`.",
            "- ONNX readiness(ONNX 준비): `not_claimed`.",
            "- Goal Achieve(목표 달성): `not_claimed`.",
            "- missing_required(필수 누락): broader period pressure(더 넓은 기간 압박), real fallback/routed robustness(실제 대체/라우팅 견고성), Adapter follow-up(어댑터 후속).",
            f"- next_action(다음 행동): `{result['next_action']}`.",
        ]
    )
    return "\n".join(lines)


def review() -> dict[str, Any]:
    if not path_exists(SOURCE_EXECUTION_RESULT_PATH):
        raise FileNotFoundError(SOURCE_EXECUTION_RESULT_PATH)
    created_at = utc_now()
    execution_result = read_json(SOURCE_EXECUTION_RESULT_PATH)
    forensics_rows = read_csv(SOURCE_FORENSICS_PATH)
    trade_rows, parser_errors, parser_checks = build_trade_records(execution_result)
    time_rows = build_time_slice_rows(trade_rows)
    curve_rows = build_curve_rows(trade_rows, time_rows, execution_result)
    candidate_tests = build_candidate_test_review(curve_rows, time_rows)
    candidate_summary = build_candidate_summary(candidate_tests)
    guard_axis_summary = build_guard_axis_summary(candidate_tests)
    negative = negative_slices(time_rows)
    tier_duplicate_review = build_tier_duplicate_review(curve_rows)
    status = result_status(parser_errors, parser_checks)
    judgment = result_judgment(status)
    next_action = result_next_action(status)
    constructive_count = sum(1 for row in candidate_tests if str(row.get("curve_read")).startswith("constructive"))
    result = {
        "status": status,
        "judgment": judgment,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_run_id": PARENT_RUN_ID,
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "trade_record_count": len(trade_rows),
        "time_slice_row_count": len(time_rows),
        "curve_row_count": len(curve_rows),
        "candidate_test_review": candidate_tests,
        "candidate_summary": candidate_summary,
        "guard_axis_summary": guard_axis_summary,
        "negative_slices": negative,
        "tier_duplicate_review": tier_duplicate_review,
        "parser_errors": parser_errors,
        "parser_checks": parser_checks,
        "forensics_summary": forensics_summary(forensics_rows),
        "constructive_curve_rows": constructive_count,
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": next_action,
        "outputs": {
            "trade_records": rel(TRADE_RECORDS_PATH),
            "time_slice_kpi": rel(TIME_SLICE_KPI_PATH),
            "curve_diagnostics": rel(CURVE_DIAGNOSTICS_PATH),
            "candidate_test_review": rel(CANDIDATE_TEST_REVIEW_PATH),
            "candidate_summary": rel(CANDIDATE_SUMMARY_PATH),
            "guard_axis_summary": rel(GUARD_AXIS_SUMMARY_PATH),
            "negative_slice_summary": rel(NEGATIVE_SLICE_PATH),
            "parser_checks": rel(PARSER_CHECKS_PATH),
            "parser_errors": rel(PARSER_ERRORS_PATH),
            "tier_duplicate_review": rel(TIER_DUPLICATE_REVIEW_PATH),
            "review_result": rel(REVIEW_RESULT_PATH),
            "report": rel(REPORT_PATH),
        },
        "sources": {
            "execution_result": rel(SOURCE_EXECUTION_RESULT_PATH),
            "kpi_summary": rel(SOURCE_KPI_SUMMARY_PATH),
            "forensics": rel(SOURCE_FORENSICS_PATH),
            "executed_attempts": rel(SOURCE_EXECUTED_ATTEMPTS_PATH),
        },
    }
    write_csv(
        TRADE_RECORDS_PATH,
        trade_rows,
        (
            "run_id",
            "source_run_id",
            "queue_id",
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "test_id",
            "guard_rule_family",
            "model_materialization_type",
            "materialization_boundary",
            "record_view",
            "attempt_name",
            "tier_scope",
            "route_role",
            "split",
            "fallback_enabled",
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
            "gross_profit",
            "net_profit",
            "commission",
            "swap",
            "source_report_path",
        ),
    )
    time_columns = (
        "record_view",
        "tier_scope",
        "candidate_id",
        "candidate_alias",
        "candidate_role",
        "test_id",
        "guard_rule_family",
        "materialization_boundary",
        "route_role",
        "axis",
        "bucket",
        *METRIC_COLUMNS,
        "slice_read",
    )
    write_csv(TIME_SLICE_KPI_PATH, time_rows, time_columns)
    write_csv(
        CURVE_DIAGNOSTICS_PATH,
        curve_rows,
        (
            "record_view",
            "tier_scope",
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "test_id",
            "guard_rule_family",
            "materialization_boundary",
            "route_role",
            *METRIC_COLUMNS,
            "report_equity_drawdown_percent",
            "report_balance_drawdown_percent",
            "report_recovery_factor",
            "tier_b_fallback_used_count",
            "tier_b_fallback_order_fill_count",
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
        ),
    )
    write_csv(CANDIDATE_TEST_REVIEW_PATH, candidate_tests, tuple(candidate_tests[0].keys()) if candidate_tests else ())
    write_csv(CANDIDATE_SUMMARY_PATH, candidate_summary, tuple(candidate_summary[0].keys()) if candidate_summary else ())
    write_csv(GUARD_AXIS_SUMMARY_PATH, guard_axis_summary, tuple(guard_axis_summary[0].keys()) if guard_axis_summary else ())
    write_csv(NEGATIVE_SLICE_PATH, negative, tuple(negative[0].keys()) if negative else time_columns)
    write_csv(
        PARSER_CHECKS_PATH,
        parser_checks,
        ("attempt_name", "record_view", "tier_scope", "report_path", "expected_trade_count", "parsed_trade_count", "trade_count_delta", "parser_status"),
    )
    write_csv(PARSER_ERRORS_PATH, parser_errors, ("attempt_name", "report_path", "error"))
    write_csv(TIER_DUPLICATE_REVIEW_PATH, tier_duplicate_review, tuple(tier_duplicate_review[0].keys()) if tier_duplicate_review else ())
    write_json(REVIEW_RESULT_PATH, result)
    write_md(REPORT_PATH, report_markdown(result))
    update_ledgers(created_at, result)
    update_current_truth_docs(result)
    return result


def main() -> int:
    result = review()
    print(
        json.dumps(
            {
                "status": result["status"],
                "trade_records": result["trade_record_count"],
                "time_slice_rows": result["time_slice_row_count"],
                "curve_rows": result["curve_row_count"],
                "candidate_test_rows": len(result["candidate_test_review"]),
                "constructive_curve_rows": result["constructive_curve_rows"],
                "negative_slices": len(result["negative_slices"]),
                "parser_errors": len(result["parser_errors"]),
                "selected_candidate": result["selected_candidate"],
                "onnx_readiness": result["onnx_readiness"],
                "goal_achieve": result["goal_achieve"],
                "next_action": result["next_action"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
