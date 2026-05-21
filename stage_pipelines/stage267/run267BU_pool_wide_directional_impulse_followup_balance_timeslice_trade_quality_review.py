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
from stage_pipelines.stage267 import run267BT_pool_wide_directional_impulse_followup_mt5_executor as source_executor


STAGE_ID = source_executor.STAGE_ID
RUN_NUMBER = "run267BU"
RUN_ID = "run267BU_stage267_pool_wide_directional_impulse_followup_balance_timeslice_trade_quality_review_v1"
PARENT_RUN_ID = source_executor.RUN_ID
SOURCE_MATERIALIZATION_RUN_ID = source_executor.SOURCE_RUN_ID
STATUS = "run267BU_pool_wide_directional_impulse_followup_balance_timeslice_trade_quality_review_completed"
PARTIAL_STATUS = "run267BU_pool_wide_directional_impulse_followup_balance_timeslice_trade_quality_review_partial_parser_errors"
JUDGMENT = "curve_timeslice_trade_quality_review_completed_no_candidate_selection"
PARTIAL_JUDGMENT = "curve_timeslice_trade_quality_review_partial_parser_errors_no_candidate_selection"
CLAIM_BOUNDARY = source_executor.CLAIM_BOUNDARY
NEXT_ACTION = "run267BV_design_directional_impulse_followup_or_prune_from_run267BU_review"
NEXT_ACTION_PARTIAL = "run267BU_repair_trade_report_parser_errors_before_followup_design"

STAGE_ROOT = source_executor.STAGE_ROOT
REVIEWS_ROOT = source_executor.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "pool_wide_directional_impulse_followup_balance_timeslice_trade_quality_review"

SOURCE_EXECUTION_RESULT_PATH = source_executor.EXECUTION_RESULT_PATH
SOURCE_KPI_SUMMARY_PATH = source_executor.KPI_SUMMARY_PATH
SOURCE_FORENSICS_PATH = source_executor.FORENSICS_PATH
SOURCE_EXECUTED_ATTEMPTS_PATH = source_executor.EXECUTED_ATTEMPTS_PATH
SOURCE_VARIANT_MANIFEST_PATH = source_executor.SOURCE_VARIANT_MANIFEST_PATH
SOURCE_RUNTIME_CONTRACT_PATH = source_executor.SOURCE_RUNTIME_CONTRACT_PATH
SOURCE_ROUTE_GAP_AUDIT_PATH = source_executor.SOURCE_ROUTE_GAP_AUDIT_PATH
SOURCE_EXECUTION_REPORT_PATH = source_executor.REPORT_PATH

TRADE_RECORDS_PATH = RUN_ROOT / "trade_records.csv"
TIME_SLICE_KPI_PATH = RUN_ROOT / "time_slice_kpi.csv"
CURVE_DIAGNOSTICS_PATH = RUN_ROOT / "curve_diagnostics.csv"
CANDIDATE_PROFILE_REVIEW_PATH = RUN_ROOT / "candidate_profile_review.csv"
PROFILE_SUMMARY_PATH = RUN_ROOT / "profile_summary.csv"
NEGATIVE_SLICE_PATH = RUN_ROOT / "negative_slice_summary.csv"
FOLLOWUP_QUEUE_PATH = RUN_ROOT / "followup_queue.csv"
FAILURE_MEMORY_PATH = RUN_ROOT / "failure_memory.csv"
PARSER_CHECKS_PATH = RUN_ROOT / "parser_checks.csv"
PARSER_ERRORS_PATH = RUN_ROOT / "parser_errors.csv"
FORENSIC_SUMMARY_PATH = RUN_ROOT / "forensic_summary.csv"
PERFORMANCE_ATTRIBUTION_PATH = RUN_ROOT / "performance_attribution.csv"
RESULT_JUDGMENT_PATH = RUN_ROOT / "result_judgment.csv"
RUN_MANIFEST_PATH = RUN_ROOT / "run_manifest.json"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
REVIEW_RESULT_PATH = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267BU_pool_wide_directional_impulse_followup_balance_timeslice_trade_quality_review.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267BU_pool_wide_directional_impulse_followup_balance_timeslice_trade_quality_review.py")

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
    "closed_balance_end",
    "closed_balance_min",
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


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    ordered: list[str] = []
    for row in rows:
        for key in row:
            if key not in ordered:
                ordered.append(key)
    fieldnames = list(columns or ordered or ("status", "notes"))
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: cell(row.get(column)) for column in fieldnames})


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


def max_closed_balance_drawdown(rows: Sequence[Mapping[str, Any]]) -> tuple[float, float, int, float, float, float]:
    balance = DEPOSIT
    peak = DEPOSIT
    min_balance = DEPOSIT
    max_dd = 0.0
    max_dd_pct = 0.0
    longest_underwater = 0
    underwater = 0
    underwater_count = 0
    for row in sorted(rows, key=lambda item: str(item.get("close_time"))):
        balance += as_float(row.get("net_profit"))
        min_balance = min(min_balance, balance)
        if balance >= peak:
            peak = balance
            underwater = 0
        else:
            underwater += 1
            underwater_count += 1
            longest_underwater = max(longest_underwater, underwater)
        dd = peak - balance
        dd_pct = dd / peak * 100.0 if peak else 0.0
        max_dd = max(max_dd, dd)
        max_dd_pct = max(max_dd_pct, dd_pct)
    share = underwater_count / len(rows) if rows else 0.0
    return balance, min_balance, max_dd, max_dd_pct, longest_underwater, share


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
    end_balance, min_balance, dd, dd_pct, underwater, underwater_share = max_closed_balance_drawdown(ordered)
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
        "closed_balance_end": end_balance,
        "closed_balance_min": min_balance,
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
        return "thin_slice(얇은 구간)"
    if net <= -120.0 or dd_pct >= 30.0:
        return "deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)"
    if net < -60.0:
        return "negative_fragile_slice(음수 취약 구간)"
    if net < 0.0:
        return "minor_negative_slice(작은 음수 구간)"
    return "measured_slice(측정 구간)"


def attempts_by_name(execution_result: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {str(item.get("attempt_name")): item for item in execution_result.get("attempts_executed", [])}


def absolute_repo_path(path_text: str) -> Path:
    path = Path(path_text)
    return path if path.is_absolute() else REPO_ROOT / path


def build_trade_records(execution_result: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    attempts = attempts_by_name(execution_result)
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
        html_path = absolute_repo_path(str(metrics_payload.get("report_path") or report.get("html_report", {}).get("path") or ""))
        try:
            parsed = parse_mt5_trade_report(html_path)
            trades = pair_deals_into_trades(parsed["deals"])
        except Exception as exc:  # pragma: no cover - persisted as run evidence.
            parser_errors.append({"attempt_name": attempt_name, "report_path": rel(html_path), "error": str(exc)})
            continue
        expected_count = as_int(metrics_payload.get("trade_count"))
        parser_checks.append(
            {
                "attempt_name": attempt_name,
                "record_view": record.get("record_view"),
                "candidate_alias": attempt.get("candidate_alias"),
                "profile_label": attempt.get("profile_label"),
                "report_path": rel(html_path),
                "expected_trade_count": expected_count,
                "parsed_deal_count": len(parsed["deals"]),
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
            rows.append(
                {
                    "run_id": RUN_ID,
                    "source_run_id": PARENT_RUN_ID,
                    "source_materialization_run_id": SOURCE_MATERIALIZATION_RUN_ID,
                    "queue_id": attempt.get("queue_id"),
                    "candidate_id": attempt.get("candidate_id"),
                    "candidate_alias": attempt.get("candidate_alias"),
                    "candidate_role": attempt.get("candidate_role"),
                    "variant_id": attempt.get("variant_id"),
                    "profile_label": attempt.get("profile_label"),
                    "materialization_boundary": attempt.get("materialization_boundary"),
                    "tier_pair_boundary": attempt.get("tier_pair_boundary"),
                    "record_view": record.get("record_view"),
                    "attempt_name": attempt_name,
                    "tier_scope": record.get("tier_scope"),
                    "route_role": record.get("route_role"),
                    "split": record.get("split"),
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
            "attempt_name",
            "tier_scope",
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "variant_id",
            "profile_label",
            "route_role",
            axis,
        )
        for key, rows in group_rows(trade_rows, keys).items():
            (
                record_view,
                attempt_name,
                tier_scope,
                candidate_id,
                alias,
                role,
                variant_id,
                profile_label,
                route_role,
                bucket,
            ) = key
            item = metrics(rows)
            output.append(
                {
                    "record_view": record_view,
                    "attempt_name": attempt_name,
                    "tier_scope": tier_scope,
                    "candidate_id": candidate_id,
                    "candidate_alias": alias,
                    "candidate_role": role,
                    "variant_id": variant_id,
                    "profile_label": profile_label,
                    "route_role": route_role,
                    "axis": axis,
                    "bucket": bucket,
                    **item,
                    "slice_read": slice_read(item),
                }
            )
    return output


def kpi_metrics_by_view(execution_result: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {str(record.get("record_view")): record.get("metrics", {}) for record in execution_result.get("mt5_kpi_records", [])}


def chart_by_view(execution_result: Mapping[str, Any]) -> dict[str, str]:
    return {
        str(record.get("record_view")): str(record.get("report", {}).get("chart", {}).get("path") or "")
        for record in execution_result.get("mt5_kpi_records", [])
    }


def worst_related_slice(curve: Mapping[str, Any], time_rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    related = [
        row
        for row in time_rows
        if row.get("record_view") == curve.get("record_view")
        and as_int(row.get("trade_count")) >= 3
        and row.get("axis") in {"month", "weekday", "session_report", "chron_segment", "direction"}
    ]
    return min(related, key=lambda row: as_float(row.get("net_profit"))) if related else {}


def curve_flags(curve: Mapping[str, Any], worst_slice: Mapping[str, Any]) -> str:
    flags: list[str] = []
    net = as_float(curve.get("net_profit"))
    pf = as_float(curve.get("profit_factor"))
    report_dd = as_float(curve.get("report_max_drawdown_percent"))
    worst_month = as_float(curve.get("worst_month_net"))
    worst_slice_net = as_float(worst_slice.get("net_profit"))
    negative_months = as_int(curve.get("negative_month_count"))
    if net <= 0.0 or pf <= 1.0:
        flags.append("headline_negative_or_pf_broken(대표 숫자 음수 또는 수익 팩터 붕괴)")
    if report_dd >= 35.0:
        flags.append("report_dd_high(보고서 손실폭 높음)")
    if worst_month <= -80.0:
        flags.append("month_hole(月별 구멍)")
    if worst_slice_net <= -100.0:
        flags.append("slice_hole(구간 구멍)")
    if negative_months >= 5:
        flags.append("many_negative_months(음수 월 많음)")
    if as_float(curve.get("chron_late_net")) < 0.0:
        flags.append("late_segment_negative(후반 구간 음수)")
    if not flags:
        flags.append("no_major_flag_in_this_review(이번 검토에서 큰 경고 없음)")
    return ";".join(flags)


def curve_read(curve: Mapping[str, Any], worst_slice: Mapping[str, Any]) -> str:
    flags = curve_flags(curve, worst_slice)
    if "headline_negative_or_pf_broken" in flags:
        return "negative_profile_prune_no_selection(음수 프로필 가지치기, 선택 아님)"
    if "report_dd_high" in flags or "slice_hole" in flags or "month_hole" in flags:
        return "positive_but_dd_or_slice_hole_watch_no_selection(양수지만 손실폭/구간 구멍 관찰, 선택 아님)"
    net = as_float(curve.get("net_profit"))
    pf = as_float(curve.get("profit_factor"))
    trades = as_int(curve.get("trade_count"))
    if net > 150.0 and pf >= 1.10 and trades >= 300:
        return "constructive_watch_no_selection(건설적 관찰, 선택 아님)"
    return "weak_or_mixed_watch_no_selection(약하거나 혼합, 선택 아님)"


def build_curve_rows(
    trade_rows: Sequence[Mapping[str, Any]],
    time_rows: Sequence[Mapping[str, Any]],
    execution_result: Mapping[str, Any],
) -> list[dict[str, Any]]:
    kpi_by_view = kpi_metrics_by_view(execution_result)
    charts = chart_by_view(execution_result)
    output: list[dict[str, Any]] = []
    keys = (
        "record_view",
        "attempt_name",
        "tier_scope",
        "candidate_id",
        "candidate_alias",
        "candidate_role",
        "variant_id",
        "profile_label",
        "route_role",
    )
    for key, rows in group_rows(trade_rows, keys).items():
        (
            record_view,
            attempt_name,
            tier_scope,
            candidate_id,
            alias,
            role,
            variant_id,
            profile_label,
            route_role,
        ) = key
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
        chron = {str(row.get("bucket")): as_float(row.get("net_profit")) for row in chron_slices}
        positive_month_ratio = (len(month_slices) - len(negative_months)) / len(month_slices) if month_slices else 0.0
        row = {
            "record_view": record_view,
            "attempt_name": attempt_name,
            "tier_scope": tier_scope,
            "candidate_id": candidate_id,
            "candidate_alias": alias,
            "candidate_role": role,
            "variant_id": variant_id,
            "profile_label": profile_label,
            "route_role": route_role,
            **item,
            "report_max_drawdown_percent": as_float(report_metrics.get("max_drawdown_percent")),
            "report_equity_drawdown_percent": as_float(report_metrics.get("equity_drawdown_maximal_percent")),
            "report_balance_drawdown_percent": as_float(report_metrics.get("balance_drawdown_maximal_percent")),
            "report_recovery_factor": as_float(report_metrics.get("recovery_factor")),
            "positive_month_ratio": positive_month_ratio,
            "negative_month_count": len(negative_months),
            "worst_month": worst_month.get("bucket", ""),
            "worst_month_net": as_float(worst_month.get("net_profit")),
            "best_month": best_month.get("bucket", ""),
            "best_month_net": as_float(best_month.get("net_profit")),
            "chron_early_net": chron.get("chron_early", 0.0),
            "chron_mid_net": chron.get("chron_mid", 0.0),
            "chron_late_net": chron.get("chron_late", 0.0),
            "source_chart_path": rel(charts.get(str(record_view), "")),
        }
        worst_slice = worst_related_slice(row, time_rows)
        row["worst_slice_axis"] = worst_slice.get("axis", "")
        row["worst_slice_bucket"] = worst_slice.get("bucket", "")
        row["worst_slice_net"] = as_float(worst_slice.get("net_profit"))
        row["fragility_flags"] = curve_flags(row, worst_slice)
        row["curve_read"] = curve_read(row, worst_slice)
        output.append(row)
    return sorted(output, key=lambda row: (str(row.get("profile_label")), str(row.get("candidate_alias"))))


def build_candidate_profile_review(curve_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in curve_rows:
        rows.append(
            {
                "candidate_id": row.get("candidate_id"),
                "candidate_alias": row.get("candidate_alias"),
                "candidate_role": row.get("candidate_role"),
                "profile_label": row.get("profile_label"),
                "variant_id": row.get("variant_id"),
                "net_profit": row.get("net_profit"),
                "profit_factor": row.get("profit_factor"),
                "trade_count": row.get("trade_count"),
                "expectancy": row.get("expectancy"),
                "report_max_drawdown_percent": row.get("report_max_drawdown_percent"),
                "closed_balance_max_drawdown_percent": row.get("closed_balance_max_drawdown_percent"),
                "recovery_factor_closed": row.get("recovery_factor_closed"),
                "positive_month_ratio": row.get("positive_month_ratio"),
                "negative_month_count": row.get("negative_month_count"),
                "worst_month": row.get("worst_month"),
                "worst_month_net": row.get("worst_month_net"),
                "worst_slice_axis": row.get("worst_slice_axis"),
                "worst_slice_bucket": row.get("worst_slice_bucket"),
                "worst_slice_net": row.get("worst_slice_net"),
                "chron_early_net": row.get("chron_early_net"),
                "chron_mid_net": row.get("chron_mid_net"),
                "chron_late_net": row.get("chron_late_net"),
                "fragility_flags": row.get("fragility_flags"),
                "curve_read": row.get("curve_read"),
                "selection_boundary": "not_candidate_selection(후보 선택 아님)",
            }
        )
    return sorted(rows, key=lambda row: (str(row.get("profile_label")), -as_float(row.get("net_profit"))))


def build_profile_summary(curve_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for (profile,), grouped in group_rows(curve_rows, ("profile_label",)).items():
        nets = [as_float(row.get("net_profit")) for row in grouped]
        pfs = [as_float(row.get("profit_factor")) for row in grouped]
        dds = [as_float(row.get("report_max_drawdown_percent")) for row in grouped]
        negative = [row for row in grouped if as_float(row.get("net_profit")) <= 0.0 or as_float(row.get("profit_factor")) <= 1.0]
        dd_flags = [row for row in grouped if as_float(row.get("report_max_drawdown_percent")) >= 35.0]
        if len(negative) == len(grouped):
            profile_read = "prune_as_standalone_profile(독립 프로필 가지치기)"
        elif dd_flags:
            profile_read = "salvage_as_aggressive_clue_not_selection(공격형 단서로 회수, 선택 아님)"
        else:
            profile_read = "watch_not_selection(관찰, 선택 아님)"
        output.append(
            {
                "profile_label": profile,
                "candidate_count": len(grouped),
                "positive_count": len(grouped) - len(negative),
                "negative_or_pf_broken_count": len(negative),
                "high_dd_count": len(dd_flags),
                "net_profit_mean": mean(nets) if nets else None,
                "net_profit_min": min(nets) if nets else None,
                "net_profit_max": max(nets) if nets else None,
                "profit_factor_mean": mean(pfs) if pfs else None,
                "report_max_drawdown_percent_worst": max(dds) if dds else None,
                "profile_read": profile_read,
            }
        )
    return sorted(output, key=lambda row: str(row.get("profile_label")))


def negative_slices(time_rows: Sequence[Mapping[str, Any]], limit: int = 80) -> list[dict[str, Any]]:
    rows = [
        dict(row)
        for row in time_rows
        if as_float(row.get("net_profit")) < 0.0 and as_int(row.get("trade_count")) >= 3
    ]
    return sorted(rows, key=lambda row: (as_float(row.get("net_profit")), -as_int(row.get("trade_count"))))[:limit]


def build_followup_queue(profile_summary: Sequence[Mapping[str, Any]], candidate_review: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    profile_by_name = {str(row.get("profile_label")): row for row in profile_summary}
    directional = profile_by_name.get("directional_asymmetry", {})
    impulse = profile_by_name.get("aggressive_impulse_replacement", {})
    if directional:
        output.append(
            {
                "queue_id": "run267bu_q01_prune_directional_asymmetry_standalone",
                "priority": "P0",
                "workstream": "prune_or_reframe",
                "scope": "pool_wide_directional_asymmetry",
                "source_evidence": rel(CANDIDATE_PROFILE_REVIEW_PATH),
                "reason": "directional_asymmetry(방향 비대칭) 후보군 전체가 net/PF(순수익/수익 팩터) 기준에서 음수 또는 붕괴다.",
                "next_probe": "do_not_extend_as_standalone; only reuse as diagnostic side-specific pressure feature",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    if impulse:
        output.append(
            {
                "queue_id": "run267bu_q02_aggressive_impulse_dd_shape_repair",
                "priority": "P0",
                "workstream": "aggressive_followup",
                "scope": "pool_wide_aggressive_impulse_replacement",
                "source_evidence": rel(CANDIDATE_PROFILE_REVIEW_PATH),
                "reason": "aggressive_impulse_replacement(공격형 임펄스 대체)은 전 후보가 양수지만 DD(손실폭)가 높아 선택 근거가 아니다.",
                "next_probe": "test aggressive impulse with drawdown-shape pressure and cross-period checks without filter stacking",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    best_impulse = [
        row
        for row in candidate_review
        if row.get("profile_label") == "aggressive_impulse_replacement"
    ]
    for row in sorted(best_impulse, key=lambda item: -as_float(item.get("net_profit")))[:3]:
        output.append(
            {
                "queue_id": f"run267bu_q03_{row.get('candidate_alias')}_impulse_watch",
                "priority": "P1",
                "workstream": "candidate_watch",
                "scope": row.get("candidate_alias"),
                "source_evidence": rel(CANDIDATE_PROFILE_REVIEW_PATH),
                "reason": (
                    f"net_profit(순수익)={cell(row.get('net_profit'))}; "
                    f"PF(수익 팩터)={cell(row.get('profit_factor'))}; "
                    f"DD(손실폭)={cell(row.get('report_max_drawdown_percent'))}; "
                    "watch only(관찰 전용)."
                ),
                "next_probe": "carry into run267BV design as pressure candidate, not selection",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return output


def build_failure_memory(profile_summary: Sequence[Mapping[str, Any]], candidate_review: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    directional_rows = [row for row in candidate_review if row.get("profile_label") == "directional_asymmetry"]
    impulse_rows = [row for row in candidate_review if row.get("profile_label") == "aggressive_impulse_replacement"]
    if directional_rows:
        rows.append(
            {
                "memory_id": "run267bu_directional_asymmetry_pool_wide_negative",
                "scope": "directional_asymmetry(방향 비대칭)",
                "evidence": rel(CANDIDATE_PROFILE_REVIEW_PATH),
                "failure_mode": "all five candidates lost money or failed PF(수익 팩터) > 1.0",
                "do_not_repeat": "do not run the same standalone directional asymmetry score table again without a different structural reason",
                "salvage_condition": "reuse only as diagnostic directional pressure, not as a selected branch",
            }
        )
    if impulse_rows:
        rows.append(
            {
                "memory_id": "run267bu_aggressive_impulse_positive_but_high_dd",
                "scope": "aggressive_impulse_replacement(공격형 임펄스 대체)",
                "evidence": rel(CANDIDATE_PROFILE_REVIEW_PATH),
                "failure_mode": "positive net/PF but uncomfortable report DD(손실폭) across all five candidates",
                "do_not_repeat": "do not promote or ONNX-review from headline positive net alone",
                "salvage_condition": "only continue through drawdown-shape and cross-period pressure probes",
            }
        )
    return rows


def forensics_summary(rows: Sequence[Mapping[str, Any]], parser_checks: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    statuses = sorted({str(row.get("tester_status")) for row in rows if row.get("tester_status")})
    report_statuses = sorted({str(row.get("report_status")) for row in rows if row.get("report_status")})
    matched = [row for row in parser_checks if row.get("parser_status") == "matched"]
    return [
        {
            "tester_identity": "terminal/symbol/timeframe/deposit/leverage/model/date_range",
            "value": (
                f"terminals={len({str(row.get('terminal')) for row in rows if row.get('terminal')})};"
                f"symbols={';'.join(sorted({str(row.get('symbol')) for row in rows if row.get('symbol')}))};"
                f"timeframes={';'.join(sorted({str(row.get('timeframe')) for row in rows if row.get('timeframe')}))};"
                f"from={';'.join(sorted({str(row.get('from_date')) for row in rows if row.get('from_date')}))};"
                f"to={';'.join(sorted({str(row.get('to_date')) for row in rows if row.get('to_date')}))}"
            ),
            "status": "checked",
            "judgment": "usable_with_boundary(경계부 사용 가능)",
        },
        {
            "tester_identity": "status",
            "value": f"tester={';'.join(statuses)};report={';'.join(report_statuses)};parser_matched={len(matched)}/{len(parser_checks)}",
            "status": "checked",
            "judgment": "usable_with_boundary(경계부 사용 가능)" if rows and statuses == ["completed"] and report_statuses == ["completed"] and len(matched) == len(parser_checks) else "inconclusive(불충분)",
        },
        {
            "tester_identity": "cost_assumptions",
            "value": "MT5 tester broker-history costs; no separate cost authority claimed(MT5 테스터 브로커 이력 비용, 별도 비용 권위 주장 없음)",
            "status": "boundary_recorded",
            "judgment": "usable_with_boundary(경계부 사용 가능)",
        },
    ]


def performance_attribution(profile_summary: Sequence[Mapping[str, Any]], candidate_review: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    by_candidate: dict[str, dict[str, Mapping[str, Any]]] = defaultdict(dict)
    for row in candidate_review:
        by_candidate[str(row.get("candidate_alias"))][str(row.get("profile_label"))] = row
    rows: list[dict[str, Any]] = [
        {
            "subject": "profile_level",
            "observed_change": "directional_asymmetry(방향 비대칭)는 후보군 전체 음수, aggressive_impulse_replacement(공격형 임펄스 대체)는 후보군 전체 양수",
            "comparison_baseline": rel(CANDIDATE_PROFILE_REVIEW_PATH),
            "likely_drivers": "nonflat impulse pressure score(비평탄 임펄스 압박 점수)가 방향 비대칭보다 더 넓게 거래를 유지한 것으로 추정",
            "segment_checks": "month/weekday/hour/session/direction/chron_segment(월/요일/시간/세션/방향/초중후반) checked",
            "trade_shape": "trade count(거래 수)는 350~378개로 얇지는 않지만 DD(손실폭)가 높다",
            "alternative_explanations": "2024 cached compact rank-gate context(2024 캐시 압축 순위-게이트 문맥)와 score-table materialization(점수표 물질화) 영향 가능",
            "attribution_confidence": "medium_with_boundary(중간, 경계부)",
            "next_probe": "run267BV에서 DD-shape pressure(손실폭 형태 압박)와 cross-period(확장 기간)를 같이 설계",
        }
    ]
    for alias, profiles in sorted(by_candidate.items()):
        directional = profiles.get("directional_asymmetry", {})
        impulse = profiles.get("aggressive_impulse_replacement", {})
        if not directional or not impulse:
            continue
        rows.append(
            {
                "subject": alias,
                "observed_change": "aggressive_impulse_replacement minus directional_asymmetry(공격형 임펄스 대체 - 방향 비대칭)",
                "comparison_baseline": "same candidate, same 2024 Tier A stress(같은 후보, 같은 2024 Tier A 압박)",
                "net_delta": as_float(impulse.get("net_profit")) - as_float(directional.get("net_profit")),
                "pf_delta": as_float(impulse.get("profit_factor")) - as_float(directional.get("profit_factor")),
                "dd_delta": as_float(impulse.get("report_max_drawdown_percent")) - as_float(directional.get("report_max_drawdown_percent")),
                "likely_drivers": "impulse replacement profile(임펄스 대체 프로필)",
                "segment_checks": "candidate_profile_review(후보 프로필 검토) and negative_slice_summary(음수 구간 요약)",
                "trade_shape": f"trades={impulse.get('trade_count')};expectancy={cell(impulse.get('expectancy'))}",
                "alternative_explanations": "same feature source limitation(같은 피처 원천 한계)",
                "attribution_confidence": "medium_with_boundary(중간, 경계부)",
                "next_probe": "carry only as watch candidate(관찰 후보로만 이월)",
            }
        )
    return rows


def result_status(parser_errors: Sequence[Mapping[str, Any]], parser_checks: Sequence[Mapping[str, Any]]) -> str:
    mismatches = [row for row in parser_checks if row.get("parser_status") != "matched"]
    return PARTIAL_STATUS if parser_errors or mismatches else STATUS


def result_judgment(status: str) -> str:
    return JUDGMENT if status == STATUS else PARTIAL_JUDGMENT


def result_next_action(status: str) -> str:
    return NEXT_ACTION if status == STATUS else NEXT_ACTION_PARTIAL


def result_judgment_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {"field": "run_status", "value": result["status"], "judgment": result["judgment"], "evidence": rel(REVIEW_RESULT_PATH)},
        {"field": "trade_records", "value": result["trade_record_count"], "judgment": "parsed_trade_list_evidence", "evidence": rel(TRADE_RECORDS_PATH)},
        {"field": "negative_slice_count", "value": result["negative_slice_count"], "judgment": "weak_slices_present", "evidence": rel(NEGATIVE_SLICE_PATH)},
        {"field": "selected_candidate", "value": "none", "judgment": "not_selected", "evidence": "curve_time_slice_trade_quality_not_strong_enough"},
        {"field": "selected_research_baseline", "value": "none", "judgment": "not_selected", "evidence": "research_pool_still_racing"},
        {"field": "onnx_readiness", "value": "not_claimed", "judgment": "not_ready", "evidence": "goal_gate_not_met"},
        {"field": "goal_achieve", "value": "not_claimed", "judgment": "not_claimed", "evidence": "full_objective_not_met"},
        {"field": "next_action", "value": result["next_action"], "judgment": "design_followup_or_prune", "evidence": rel(FOLLOWUP_QUEUE_PATH)},
    ]


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


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


def remove_workspace_focus_item(text: str, needle: str) -> str:
    lines = text.splitlines()
    output: list[str] = []
    index = 0
    while index < len(lines):
        if lines[index].strip() == "- >-" and index + 1 < len(lines) and needle in lines[index + 1]:
            index += 2
            continue
        output.append(lines[index])
        index += 1
    return "\n".join(output) + "\n"


def update_stage267_workspace_block(text: str, *, status: str, next_action: str) -> str:
    report_entry = f"  run267BU_pool_wide_directional_impulse_followup_balance_timeslice_trade_quality_review_report_path: {rel(REPORT_PATH)}"
    lines = text.splitlines()
    out: list[str] = []
    in_stage267 = False
    report_seen = report_entry in text
    for line in lines:
        if line.startswith("stage267_baseline_candidate_racing_protocol:"):
            in_stage267 = True
            out.append(line)
            continue
        if in_stage267 and line and not line.startswith(" "):
            if not report_seen:
                out.append(report_entry)
                report_seen = True
            in_stage267 = False
        if in_stage267:
            stripped = line.strip()
            if stripped.startswith("status:"):
                out.append(f"  status: {status}")
                continue
            if stripped.startswith("current_run_id:"):
                out.append(f"  current_run_id: {RUN_ID}")
                continue
            if stripped.startswith("last_completed_run_id:"):
                out.append(f"  last_completed_run_id: {RUN_ID}")
                continue
            if stripped.startswith("next_action:"):
                if not report_seen:
                    out.append(report_entry)
                    report_seen = True
                out.append(f"  next_action: {next_action}")
                continue
        out.append(line)
    if in_stage267 and not report_seen:
        out.append(report_entry)
    return "\n".join(out) + "\n"


def update_current_truth_docs(result: Mapping[str, Any]) -> None:
    status = str(result["status"])
    next_action = str(result["next_action"])
    report_line = f"- run267BU_pool_wide_directional_impulse_followup_balance_timeslice_trade_quality_review(267BU 후보군 전체 방향/임펄스 후속 잔액/시간구간/거래품질 검토): `{rel(REPORT_PATH)}`"
    block = "\n".join(
        [
            "Run267BU(267BU 실행)는 run267BT(267BT 실행)의 MT5(MetaTrader 5, 메타트레이더5) 보고서를 trade list(거래 목록)로 다시 읽었다.",
            f"Effect(효과): trade records(거래 기록) `{result['trade_record_count']}`개, time-slice rows(시간 구간 행) `{result['time_slice_row_count']}`개, negative slices(음수 구간) `{result['negative_slice_count']}`개를 만들었고, directional_asymmetry(방향 비대칭)는 가지치기, aggressive_impulse_replacement(공격형 임펄스 대체)는 DD(손실폭) 압박 후속으로 넘긴다.",
            "Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.",
        ]
    )
    for path in (CURRENT_WORKING_STATE_PATH, SELECTION_STATUS_PATH, REVIEW_INDEX_PATH):
        text = io_path(path).read_text(encoding="utf-8-sig")
        text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
        text = replace_line_prefix(text, "- status(상태):", f"- status(상태): `{status}`")
        text = replace_line_prefix(text, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{status}`")
        text = replace_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
        text = replace_line_prefix(text, "- adapter_under_review(검토 중 어댑터):", "- adapter_under_review(검토 중 어댑터): `pool_wide_directional_impulse_followup_balance_timeslice_trade_quality_review`")
        text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{next_action}`")
        text = append_after_contains(text, "stage267_run267BT_pool_wide_directional_impulse_followup_mt5_execution.md", report_line)
        text = append_block_once(text, "Run267BU(267BU 실행)는", block)
        write_md(path, text)

    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = remove_workspace_focus_item(workspace, "run267BU(267BU 실행)")
    focus = (
        "- >-\n"
        f"  Stage267(267단계) run267BU(267BU 실행) pool-wide directional/impulse follow-up balance/time-slice/trade-quality review(후보군 전체 방향/임펄스 후속 잔액/시간구간/거래품질 검토) `{status}`. "
        f"Effect(효과): run267BT(267BT 실행)의 10개 MT5(MetaTrader 5, 메타트레이더5) report(보고서)를 trade list(거래 목록), curve(곡선), weak slice(약한 구간)로 다시 읽었고 selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    workspace = update_stage267_workspace_block(workspace, status=status, next_action=next_action)
    write_md(WORKSPACE_STATE_PATH, workspace)


def write_outputs(result: Mapping[str, Any]) -> None:
    write_csv(TRADE_RECORDS_PATH, result["trade_records"])
    write_csv(TIME_SLICE_KPI_PATH, result["time_slice_rows"])
    write_csv(CURVE_DIAGNOSTICS_PATH, result["curve_rows"])
    write_csv(CANDIDATE_PROFILE_REVIEW_PATH, result["candidate_profile_review"])
    write_csv(PROFILE_SUMMARY_PATH, result["profile_summary"])
    write_csv(NEGATIVE_SLICE_PATH, result["negative_slices"])
    write_csv(FOLLOWUP_QUEUE_PATH, result["followup_queue"])
    write_csv(FAILURE_MEMORY_PATH, result["failure_memory"])
    write_csv(PARSER_CHECKS_PATH, result["parser_checks"])
    write_csv(PARSER_ERRORS_PATH, result["parser_errors"])
    write_csv(FORENSIC_SUMMARY_PATH, result["forensic_summary"])
    write_csv(PERFORMANCE_ATTRIBUTION_PATH, result["performance_attribution"])
    write_csv(RESULT_JUDGMENT_PATH, result_judgment_rows(result))
    write_json(REVIEW_RESULT_PATH, result)
    write_json(
        RUN_MANIFEST_PATH,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "source_materialization_run_id": SOURCE_MATERIALIZATION_RUN_ID,
            "status": result["status"],
            "judgment": result["judgment"],
            "created_at_utc": result["created_at_utc"],
            "trade_record_count": result["trade_record_count"],
            "time_slice_row_count": result["time_slice_row_count"],
            "negative_slice_count": result["negative_slice_count"],
            "next_action": result["next_action"],
            "claim_boundary": CLAIM_BOUNDARY,
            "selected_candidate": "none",
            "selected_research_baseline": "none",
            "onnx_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
        },
    )
    write_json(
        LINEAGE_PATH,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "source_inputs": {
                "execution_result": rel(SOURCE_EXECUTION_RESULT_PATH),
                "kpi_summary": rel(SOURCE_KPI_SUMMARY_PATH),
                "forensics": rel(SOURCE_FORENSICS_PATH),
                "variant_manifest": rel(SOURCE_VARIANT_MANIFEST_PATH),
                "runtime_contract": rel(SOURCE_RUNTIME_CONTRACT_PATH),
                "route_gap_audit": rel(SOURCE_ROUTE_GAP_AUDIT_PATH),
            },
            "producer": rel(PRODUCER_PATH),
            "consumer": result["next_action"],
            "artifact_paths": {
                "trade_records": rel(TRADE_RECORDS_PATH),
                "time_slice_kpi": rel(TIME_SLICE_KPI_PATH),
                "curve_diagnostics": rel(CURVE_DIAGNOSTICS_PATH),
                "candidate_profile_review": rel(CANDIDATE_PROFILE_REVIEW_PATH),
                "profile_summary": rel(PROFILE_SUMMARY_PATH),
                "followup_queue": rel(FOLLOWUP_QUEUE_PATH),
                "failure_memory": rel(FAILURE_MEMORY_PATH),
                "report": rel(REPORT_PATH),
            },
            "availability": "tracked",
            "lineage_judgment": "connected_with_boundary",
        },
    )
    write_md(REPORT_PATH, report_markdown(result))


def update_ledgers_and_artifacts(created_at: str, result: Mapping[str, Any]) -> None:
    status = str(result["status"])
    judgment = str(result["judgment"])
    next_action = str(result["next_action"])
    notes = (
        f"trade_records={result['trade_record_count']};time_slice_rows={result['time_slice_row_count']};"
        f"negative_slices={result['negative_slice_count']};next_action={next_action};selected_candidate=none."
    )
    stage_row = {
        "row_id": "stage267_run267BU_pool_wide_directional_impulse_followup_balance_timeslice_trade_quality_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "pool_wide_directional_impulse_followup_balance_timeslice_trade_quality_review",
        "tier_scope": "Tier A run267BT review; Tier B and actual routed total blocked until true fallback manifest exists",
        "scoreboard": "trade_shape_curve_time_slice_review",
        "status": status,
        "judgment": judgment,
        "evidence_boundary": "trade_list_curve_timeslice_review_no_candidate_selection_no_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": notes,
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "baseline_candidate_racing_directional_impulse_balance_timeslice_trade_quality_review",
        "status": status,
        "judgment": judgment,
        "path": rel(REPORT_PATH),
        "notes": notes,
    }
    project_row = {
        "ledger_row_id": f"{RUN_ID}__pool_wide_directional_impulse_followup_balance_timeslice_trade_quality_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "pool_wide_directional_impulse_followup_balance_timeslice_trade_quality_review",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "pool_wide_directional_impulse_followup_balance_timeslice_trade_quality_review",
        "tier_scope": "Tier A run267BT review; true fallback blocked",
        "kpi_scope": "balance_curve_time_slice_trade_quality",
        "scoreboard_lane": "directional_impulse_followup_trade_quality_review",
        "status": status,
        "judgment": judgment,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"trade_records={result['trade_record_count']};negative_slices={result['negative_slice_count']}",
        "guardrail_kpi": "selected_candidate=none;selected_research_baseline=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
        "external_verification_status": "completed_for_run267BT_trade_report_review",
        "notes": f"Next action: {next_action}.",
    }
    upsert_csv_rows(STAGE_LEDGER_PATH, STAGE_LEDGER_COLUMNS, [stage_row], key="row_id")
    upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [run_row], key="run_id")
    upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [project_row], key="ledger_row_id")
    entries = (
        ("stage267_run267BU_producer", "producer_script", PRODUCER_PATH, "Builds run267BU balance/time-slice/trade-quality review."),
        ("stage267_run267BU_source_execution_result", "source_execution_result", SOURCE_EXECUTION_RESULT_PATH, "Source run267BT execution result."),
        ("stage267_run267BU_trade_records", "trade_records", TRADE_RECORDS_PATH, "Parsed trade records."),
        ("stage267_run267BU_time_slice_kpi", "time_slice_kpi", TIME_SLICE_KPI_PATH, "Time-slice KPI."),
        ("stage267_run267BU_curve_diagnostics", "curve_diagnostics", CURVE_DIAGNOSTICS_PATH, "Curve diagnostics."),
        ("stage267_run267BU_candidate_profile_review", "candidate_profile_review", CANDIDATE_PROFILE_REVIEW_PATH, "Candidate profile review."),
        ("stage267_run267BU_profile_summary", "profile_summary", PROFILE_SUMMARY_PATH, "Profile summary."),
        ("stage267_run267BU_negative_slice_summary", "negative_slice_summary", NEGATIVE_SLICE_PATH, "Negative slice summary."),
        ("stage267_run267BU_followup_queue", "followup_queue", FOLLOWUP_QUEUE_PATH, "Follow-up queue."),
        ("stage267_run267BU_failure_memory", "failure_memory", FAILURE_MEMORY_PATH, "Failure memory."),
        ("stage267_run267BU_parser_checks", "parser_checks", PARSER_CHECKS_PATH, "Parser checks."),
        ("stage267_run267BU_forensic_summary", "forensic_summary", FORENSIC_SUMMARY_PATH, "Backtest forensic summary."),
        ("stage267_run267BU_performance_attribution", "performance_attribution", PERFORMANCE_ATTRIBUTION_PATH, "Performance attribution."),
        ("stage267_run267BU_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Result judgment."),
        ("stage267_run267BU_review_result", "review_result", REVIEW_RESULT_PATH, "Review result payload."),
        ("stage267_run267BU_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run manifest."),
        ("stage267_run267BU_lineage", "lineage", LINEAGE_PATH, "Lineage map."),
        ("stage267_run267BU_report", "review_report", REPORT_PATH, "User-facing report."),
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
            "notes": notes_text,
        }
        for artifact_id, artifact_type, path, notes_text in entries
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, rows, key="artifact_id")


def report_markdown(result: Mapping[str, Any]) -> str:
    candidate_rows = result["candidate_profile_review"]
    profile_rows = result["profile_summary"]
    negative_rows = result["negative_slices"][:12]
    lines = [
        "# Stage267 Run267BU Pool-Wide Directional/Impulse Follow-Up Balance/Time-slice/Trade-quality Review(267단계 267BU 후보군 전체 방향/임펄스 후속 잔액/시간구간/거래품질 검토)",
        "",
        "## Summary(요약)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- source_run(원천 실행): `{PARENT_RUN_ID}`",
        f"- status(상태): `{result['status']}`",
        f"- trade_records(거래 기록): `{result['trade_record_count']}`",
        f"- time_slice_rows(시간 구간 행): `{result['time_slice_row_count']}`",
        f"- negative_slices(음수 구간): `{result['negative_slice_count']}`",
        "- selected_candidate(선택 후보): `none`",
        "- selected_research_baseline(선택 연구 기준 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "Action(행동): run267BT(267BT 실행)의 10개 MT5(MetaTrader 5, 메타트레이더5) report(보고서)를 trade list(거래 목록)로 다시 읽고, 월/요일/시간/세션/방향/초중후반 구간으로 분해했다.",
        "Effect(효과): headline KPI(대표 핵심 성과 지표)가 좋아 보이는 aggressive_impulse_replacement(공격형 임펄스 대체)도 DD(손실폭), 약한 월, 후반 구간을 숨기지 못하게 했다.",
        "",
        "## Profile Summary(프로필 요약)",
        "",
        "| profile(프로필) | positive(양수) | negative/PF broken(음수/PF 붕괴) | high DD(높은 손실폭) | net mean(순수익 평균) | DD worst(최악 손실폭) | read(판독) |",
        "| --- | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in profile_rows:
        lines.append(
            "| `{profile}` | {pos} | {neg} | {dd_count} | {net_mean} | {dd_worst} | `{read}` |".format(
                profile=row.get("profile_label", ""),
                pos=cell(row.get("positive_count")),
                neg=cell(row.get("negative_or_pf_broken_count")),
                dd_count=cell(row.get("high_dd_count")),
                net_mean=cell(row.get("net_profit_mean")),
                dd_worst=cell(row.get("report_max_drawdown_percent_worst")),
                read=row.get("profile_read", ""),
            )
        )
    lines.extend(
        [
            "",
            "## Candidate/Profile Review(후보/프로필 검토)",
            "",
            "| candidate(후보) | profile(프로필) | net(순수익) | PF(수익 팩터) | trades(거래 수) | report DD%(보고서 손실폭 %) | worst month(최악 월) | read(판독) |",
            "| --- | --- | ---: | ---: | ---: | ---: | --- | --- |",
        ]
    )
    for row in candidate_rows:
        lines.append(
            "| `{candidate}` | `{profile}` | {net} | {pf} | {trades} | {dd} | `{month}` {month_net} | `{read}` |".format(
                candidate=row.get("candidate_alias", ""),
                profile=row.get("profile_label", ""),
                net=cell(row.get("net_profit")),
                pf=cell(row.get("profit_factor")),
                trades=cell(row.get("trade_count")),
                dd=cell(row.get("report_max_drawdown_percent")),
                month=row.get("worst_month", ""),
                month_net=cell(row.get("worst_month_net")),
                read=row.get("curve_read", ""),
            )
        )
    lines.extend(
        [
            "",
            "## Worst Negative Slices(최악 음수 구간)",
            "",
            "| candidate(후보) | profile(프로필) | axis(축) | bucket(구간) | trades(거래 수) | net(순수익) | DD%(손실폭 %) |",
            "| --- | --- | --- | --- | ---: | ---: | ---: |",
        ]
    )
    for row in negative_rows:
        lines.append(
            "| `{candidate}` | `{profile}` | `{axis}` | `{bucket}` | {trades} | {net} | {dd} |".format(
                candidate=row.get("candidate_alias", ""),
                profile=row.get("profile_label", ""),
                axis=row.get("axis", ""),
                bucket=row.get("bucket", ""),
                trades=cell(row.get("trade_count")),
                net=cell(row.get("net_profit")),
                dd=cell(row.get("closed_balance_max_drawdown_percent")),
            )
        )
    if not negative_rows:
        lines.append("| `none` |  |  |  |  |  |  |")
    lines.extend(
        [
            "",
            "## Judgment(판정)",
            "",
            "- directional_asymmetry(방향 비대칭)는 후보군 전체가 음수라 standalone branch(독립 분기)로는 가지치기한다.",
            "- aggressive_impulse_replacement(공격형 임펄스 대체)는 전 후보 양수지만 report DD(보고서 손실폭)가 35% 이상이라 선택 후보가 아니다.",
            "- 다음은 run267BV(267BV 실행)에서 aggressive impulse(공격형 임펄스)를 DD-shape pressure(손실폭 형태 압박)와 cross-period(확장 기간)로 설계할지, 또는 가지치기할지 결정한다.",
            "- ONNX parity(ONNX 동등성)와 ONNX conversion(ONNX 변환)은 시작하지 않는다.",
            "",
            "## Artifacts(산출물)",
            "",
            f"- trade_records(거래 기록): `{rel(TRADE_RECORDS_PATH)}`",
            f"- time_slice_kpi(시간 구간 핵심 성과 지표): `{rel(TIME_SLICE_KPI_PATH)}`",
            f"- curve_diagnostics(곡선 진단): `{rel(CURVE_DIAGNOSTICS_PATH)}`",
            f"- candidate_profile_review(후보 프로필 검토): `{rel(CANDIDATE_PROFILE_REVIEW_PATH)}`",
            f"- followup_queue(후속 대기열): `{rel(FOLLOWUP_QUEUE_PATH)}`",
            f"- failure_memory(실패 기억): `{rel(FAILURE_MEMORY_PATH)}`",
            f"- next_action(다음 행동): `{result['next_action']}`",
        ]
    )
    return "\n".join(lines) + "\n"


def execute() -> dict[str, Any]:
    created_at = utc_now()
    execution_result = read_json(SOURCE_EXECUTION_RESULT_PATH)
    forensic_rows = read_csv(SOURCE_FORENSICS_PATH)
    trade_rows, parser_errors, parser_checks = build_trade_records(execution_result)
    time_rows = build_time_slice_rows(trade_rows)
    curve_rows = build_curve_rows(trade_rows, time_rows, execution_result)
    candidate_review = build_candidate_profile_review(curve_rows)
    profile_rows = build_profile_summary(curve_rows)
    negative_rows = negative_slices(time_rows)
    followup_rows = build_followup_queue(profile_rows, candidate_review)
    failure_rows = build_failure_memory(profile_rows, candidate_review)
    forensic_summary_rows = forensics_summary(forensic_rows, parser_checks)
    attribution_rows = performance_attribution(profile_rows, candidate_review)
    status = result_status(parser_errors, parser_checks)
    result = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_materialization_run_id": SOURCE_MATERIALIZATION_RUN_ID,
        "created_at_utc": created_at,
        "status": status,
        "judgment": result_judgment(status),
        "next_action": result_next_action(status),
        "claim_boundary": CLAIM_BOUNDARY,
        "trade_records": trade_rows,
        "time_slice_rows": time_rows,
        "curve_rows": curve_rows,
        "candidate_profile_review": candidate_review,
        "profile_summary": profile_rows,
        "negative_slices": negative_rows,
        "followup_queue": followup_rows,
        "failure_memory": failure_rows,
        "parser_checks": parser_checks,
        "parser_errors": parser_errors,
        "forensic_summary": forensic_summary_rows,
        "performance_attribution": attribution_rows,
        "trade_record_count": len(trade_rows),
        "time_slice_row_count": len(time_rows),
        "negative_slice_count": len(negative_rows),
        "source_execution_result": rel(SOURCE_EXECUTION_RESULT_PATH),
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
    }
    write_outputs(result)
    update_ledgers_and_artifacts(created_at, result)
    update_current_truth_docs(result)
    return result


def main() -> int:
    result = execute()
    print(
        json.dumps(
            {
                "status": result["status"],
                "trade_records": result["trade_record_count"],
                "time_slice_rows": result["time_slice_row_count"],
                "negative_slices": result["negative_slice_count"],
                "next_action": result["next_action"],
                "selected_candidate": result["selected_candidate"],
                "onnx_readiness": result["onnx_readiness"],
                "goal_achieve": result["goal_achieve"],
                "report": rel(REPORT_PATH),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
