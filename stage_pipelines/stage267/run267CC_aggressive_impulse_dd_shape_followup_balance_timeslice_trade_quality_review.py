from __future__ import annotations

import csv
import json
import math
import sys
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from statistics import mean, pstdev
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
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from foundation.mt5.trade_report import pair_deals_into_trades, parse_mt5_trade_report
from stage_pipelines.stage267 import run267CB_aggressive_impulse_dd_shape_followup_mt5_executor as source_executor


STAGE_ID = source_executor.STAGE_ID
RUN_NUMBER = "run267CC"
RUN_ID = "run267CC_stage267_aggressive_impulse_dd_shape_followup_balance_timeslice_trade_quality_review_v1"
PARENT_RUN_ID = source_executor.RUN_ID
SOURCE_MATERIALIZATION_RUN_ID = source_executor.SOURCE_RUN_ID
STATUS = "run267CC_aggressive_impulse_dd_shape_followup_balance_timeslice_trade_quality_review_completed"
PARTIAL_STATUS = "run267CC_aggressive_impulse_dd_shape_followup_balance_timeslice_trade_quality_review_partial_parser_errors"
JUDGMENT = "followup_curve_timeslice_trade_quality_review_completed_no_candidate_selection"
PARTIAL_JUDGMENT = "followup_curve_timeslice_trade_quality_review_partial_parser_errors_no_candidate_selection"
CLAIM_BOUNDARY = source_executor.CLAIM_BOUNDARY
NEXT_ACTION = "run267CD_design_aggressive_impulse_dd_shape_followup_prune_or_pivot"
NEXT_ACTION_PARTIAL = "run267CC_repair_trade_report_parser_errors_before_prune_or_pivot"

STAGE_ROOT = source_executor.STAGE_ROOT
REVIEWS_ROOT = source_executor.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "aggressive_impulse_dd_shape_followup_balance_timeslice_trade_quality_review"

SOURCE_EXECUTION_RESULT_PATH = source_executor.EXECUTION_RESULT_PATH
SOURCE_KPI_SUMMARY_PATH = source_executor.KPI_SUMMARY_PATH
SOURCE_FORENSICS_PATH = source_executor.FORENSICS_PATH
SOURCE_EXECUTED_ATTEMPTS_PATH = source_executor.EXECUTED_ATTEMPTS_PATH
SOURCE_ATTEMPT_MANIFEST_PATH = source_executor.SOURCE_ATTEMPT_MANIFEST_PATH
SOURCE_VARIANT_MANIFEST_PATH = source_executor.SOURCE_VARIANT_MANIFEST_PATH
SOURCE_RUNTIME_CONTRACT_PATH = source_executor.SOURCE_RUNTIME_CONTRACT_PATH
SOURCE_EXECUTION_REPORT_PATH = source_executor.REPORT_PATH

TRADE_RECORDS_PATH = RUN_ROOT / "trade_records.csv"
TIME_SLICE_KPI_PATH = RUN_ROOT / "time_slice_kpi.csv"
CURVE_DIAGNOSTICS_PATH = RUN_ROOT / "curve_diagnostics.csv"
CANDIDATE_PERIOD_REVIEW_PATH = RUN_ROOT / "candidate_period_review.csv"
CANDIDATE_SUMMARY_PATH = RUN_ROOT / "candidate_followup_summary.csv"
PERIOD_SUMMARY_PATH = RUN_ROOT / "period_summary.csv"
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
REPORT_PATH = REVIEWS_ROOT / "stage267_run267CC_aggressive_impulse_dd_shape_followup_balance_timeslice_trade_quality_review.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267CC_aggressive_impulse_dd_shape_followup_balance_timeslice_trade_quality_review.py")

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


def absolute_repo_path(path_text: str) -> Path:
    path = Path(path_text)
    return path if path.is_absolute() else REPO_ROOT / path


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


def max_closed_balance_drawdown(rows: Sequence[Mapping[str, Any]]) -> tuple[float, float, float, float, int, float]:
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
    if net <= -120.0 or dd_pct >= 20.0:
        return "deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)"
    if net < -60.0:
        return "negative_fragile_slice(음수 취약 구간)"
    if net < 0.0:
        return "minor_negative_slice(작은 음수 구간)"
    return "measured_slice(측정 구간)"


def attempts_by_name(execution_result: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {str(item.get("attempt_name")): item for item in execution_result.get("attempts_executed", [])}


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
                "target_period": attempt.get("target_period"),
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
                    "attempt_name": attempt_name,
                    "record_view": record.get("record_view"),
                    "queue_id": attempt.get("queue_id"),
                    "candidate_id": attempt.get("candidate_id"),
                    "candidate_alias": attempt.get("candidate_alias"),
                    "candidate_role": attempt.get("candidate_role"),
                    "variant_id": attempt.get("variant_id"),
                    "source_variant_id": attempt.get("source_variant_id"),
                    "profile_label": attempt.get("profile_label"),
                    "target_period": attempt.get("target_period"),
                    "split": attempt.get("split"),
                    "tier_scope": record.get("tier_scope"),
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
            "source_variant_id",
            "profile_label",
            "target_period",
            "route_role",
            axis,
        )
        for key, grouped in group_rows(trade_rows, keys).items():
            (
                record_view,
                attempt_name,
                tier_scope,
                candidate_id,
                alias,
                role,
                variant_id,
                source_variant_id,
                profile_label,
                target_period,
                route_role,
                bucket,
            ) = key
            item = metrics(grouped)
            output.append(
                {
                    "record_view": record_view,
                    "attempt_name": attempt_name,
                    "tier_scope": tier_scope,
                    "candidate_id": candidate_id,
                    "candidate_alias": alias,
                    "candidate_role": role,
                    "variant_id": variant_id,
                    "source_variant_id": source_variant_id,
                    "profile_label": profile_label,
                    "target_period": target_period,
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
    closed_dd = as_float(curve.get("closed_balance_max_drawdown_percent"))
    worst_month = as_float(curve.get("worst_month_net"))
    worst_slice_net = as_float(worst_slice.get("net_profit"))
    if net <= 0.0 or pf <= 1.0:
        flags.append("headline_negative_or_pf_broken(대표 숫자 음수 또는 수익 팩터 붕괴)")
    if max(report_dd, closed_dd) >= 15.0:
        flags.append("dd_watch_ge15(손실폭 15% 이상 관찰)")
    if worst_month <= -100.0:
        flags.append("month_hole(월별 구멍)")
    if worst_slice_net <= -100.0:
        flags.append("slice_hole(구간 구멍)")
    if as_float(curve.get("chron_late_net")) < 0.0:
        flags.append("late_segment_negative(후반 구간 음수)")
    if as_float(curve.get("positive_month_ratio")) < 0.50:
        flags.append("low_positive_month_ratio(양수 월 비율 낮음)")
    if not flags:
        flags.append("no_major_flag_in_this_review(이번 검토 큰 경고 없음)")
    return ";".join(flags)


def curve_read(curve: Mapping[str, Any], worst_slice: Mapping[str, Any]) -> str:
    flags = curve_flags(curve, worst_slice)
    if "headline_negative_or_pf_broken" in flags:
        return "prune_or_redesign_no_selection(가지치기 또는 재설계, 선택 아님)"
    if "dd_watch_ge15" in flags or "month_hole" in flags or "slice_hole" in flags or "late_segment_negative" in flags:
        return "positive_but_shape_watch_no_selection(양수지만 형태 관찰, 선택 아님)"
    if as_float(curve.get("profit_factor")) >= 1.55 and as_float(curve.get("positive_month_ratio")) >= 0.60:
        return "constructive_watch_no_selection(건설적 관찰, 선택 아님)"
    return "mixed_watch_no_selection(혼합 관찰, 선택 아님)"


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
        "source_variant_id",
        "profile_label",
        "target_period",
        "route_role",
    )
    for key, grouped in group_rows(trade_rows, keys).items():
        (
            record_view,
            attempt_name,
            tier_scope,
            candidate_id,
            alias,
            role,
            variant_id,
            source_variant_id,
            profile_label,
            target_period,
            route_role,
        ) = key
        item = metrics(grouped)
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
        worst_month = min(month_slices, key=lambda row: as_float(row.get("net_profit")), default={})
        best_month = max(month_slices, key=lambda row: as_float(row.get("net_profit")), default={})
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
            "source_variant_id": source_variant_id,
            "profile_label": profile_label,
            "target_period": target_period,
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
    return sorted(output, key=lambda row: (str(row.get("candidate_alias")), str(row.get("target_period"))))


def build_candidate_period_review(curve_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "candidate_id": row.get("candidate_id"),
            "candidate_alias": row.get("candidate_alias"),
            "candidate_role": row.get("candidate_role"),
            "profile_label": row.get("profile_label"),
            "target_period": row.get("target_period"),
            "variant_id": row.get("variant_id"),
            "source_variant_id": row.get("source_variant_id"),
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
        for row in sorted(curve_rows, key=lambda item: (str(item.get("candidate_alias")), str(item.get("target_period"))))
    ]


def candidate_read(rows: Sequence[Mapping[str, Any]]) -> str:
    nets = [as_float(row.get("net_profit")) for row in rows]
    pfs = [as_float(row.get("profit_factor")) for row in rows]
    dds = [max(as_float(row.get("report_max_drawdown_percent")), as_float(row.get("closed_balance_max_drawdown_percent"))) for row in rows]
    late_values = [as_float(row.get("chron_late_net")) for row in rows]
    if any(net <= 0.0 for net in nets) or min(pfs or [0.0]) <= 1.0:
        return "broken_or_negative_prune_no_selection(깨짐 또는 음수, 선택 아님)"
    if len(rows) < 2:
        return "single_period_followup_dd_watch_no_selection(단일 기간 후속 관찰, 선택 아님)"
    if max(dds or [0.0]) >= 15.0 or any(value < 0.0 for value in late_values):
        return "positive_but_dd_or_late_watch_no_selection(양수지만 손실폭/후반 관찰, 선택 아님)"
    if min(pfs or [0.0]) >= 1.55 and max(dds or [0.0]) <= 13.0:
        return "strongest_watch_for_next_design_no_selection(다음 설계 관찰 우선, 선택 아님)"
    return "constructive_but_needs_more_pressure_no_selection(건설적이나 추가 압박 필요, 선택 아님)"


def build_candidate_summary(curve_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for (alias,), grouped in group_rows(curve_rows, ("candidate_alias",)).items():
        nets = [as_float(row.get("net_profit")) for row in grouped]
        pfs = [as_float(row.get("profit_factor")) for row in grouped]
        dds = [max(as_float(row.get("report_max_drawdown_percent")), as_float(row.get("closed_balance_max_drawdown_percent"))) for row in grouped]
        trades = [as_int(row.get("trade_count")) for row in grouped]
        worst_row = min(grouped, key=lambda row: as_float(row.get("net_profit")))
        best_row = max(grouped, key=lambda row: as_float(row.get("net_profit")))
        output.append(
            {
                "candidate_alias": alias,
                "candidate_id": grouped[0].get("candidate_id"),
                "candidate_role": grouped[0].get("candidate_role"),
                "period_count": len(grouped),
                "positive_period_count": sum(1 for net in nets if net > 0.0),
                "total_net_profit": sum(nets),
                "mean_net_profit": mean(nets) if nets else None,
                "net_profit_std": pstdev(nets) if len(nets) > 1 else 0.0,
                "min_profit_factor": min(pfs) if pfs else None,
                "mean_profit_factor": mean(pfs) if pfs else None,
                "worst_dd_percent": max(dds) if dds else None,
                "total_trades": sum(trades),
                "min_period_trades": min(trades) if trades else None,
                "worst_period": worst_row.get("target_period"),
                "worst_period_net": worst_row.get("net_profit"),
                "best_period": best_row.get("target_period"),
                "best_period_net": best_row.get("net_profit"),
                "late_negative_period_count": sum(1 for row in grouped if as_float(row.get("chron_late_net")) < 0.0),
                "candidate_read": candidate_read(grouped),
                "selection_boundary": "watch_or_followup_only_no_selection(관찰 또는 후속만, 선택 아님)",
            }
        )
    return sorted(output, key=lambda row: (-as_float(row.get("total_net_profit")), as_float(row.get("worst_dd_percent"))))


def build_period_summary(curve_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for (period,), grouped in group_rows(curve_rows, ("target_period",)).items():
        nets = [as_float(row.get("net_profit")) for row in grouped]
        pfs = [as_float(row.get("profit_factor")) for row in grouped]
        dds = [max(as_float(row.get("report_max_drawdown_percent")), as_float(row.get("closed_balance_max_drawdown_percent"))) for row in grouped]
        weakest = min(grouped, key=lambda row: as_float(row.get("net_profit")))
        output.append(
            {
                "target_period": period,
                "candidate_count": len(grouped),
                "positive_candidate_count": sum(1 for net in nets if net > 0.0),
                "total_net_profit": sum(nets),
                "mean_net_profit": mean(nets) if nets else None,
                "mean_profit_factor": mean(pfs) if pfs else None,
                "worst_dd_percent": max(dds) if dds else None,
                "weakest_candidate": weakest.get("candidate_alias"),
                "weakest_candidate_net": weakest.get("net_profit"),
                "period_read": "dd_watch_period(손실폭 관찰 기간)" if max(dds or [0.0]) >= 15.0 else "constructive_period_watch(건설적 기간 관찰)",
            }
        )
    return sorted(output, key=lambda row: str(row.get("target_period")))


def negative_slices(time_rows: Sequence[Mapping[str, Any]], limit: int = 80) -> list[dict[str, Any]]:
    rows = [
        dict(row)
        for row in time_rows
        if as_float(row.get("net_profit")) < 0.0 and as_int(row.get("trade_count")) >= 3
    ]
    return sorted(rows, key=lambda row: (as_float(row.get("net_profit")), -as_int(row.get("trade_count"))))[:limit]


def build_followup_queue(candidate_summary: Sequence[Mapping[str, Any]], period_summary: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    best_stability = sorted(candidate_summary, key=lambda row: (as_float(row.get("worst_dd_percent")), -as_float(row.get("total_net_profit"))))
    worst_dd = sorted(candidate_summary, key=lambda row: -as_float(row.get("worst_dd_percent")))
    if best_stability:
        row = best_stability[0]
        rows.append(
            {
                "queue_id": f"run267cc_q01_{row.get('candidate_alias')}_best_relative_stability_review",
                "priority": "P0",
                "workstream": "aggressive_followup_boundary",
                "candidate_alias": row.get("candidate_alias"),
                "reason": "lowest worst DD among positive follow-up aggressive impulse rows(양수 후속 행 중 최저 최악 손실폭)",
                "next_probe": "do not deepen automatically; decide prune, pivot, or one final bounded repair",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    if worst_dd:
        row = worst_dd[0]
        rows.append(
            {
                "queue_id": f"run267cc_q02_{row.get('candidate_alias')}_worst_dd_prune_watch",
                "priority": "P0",
                "workstream": "prune_or_pivot_watch",
                "candidate_alias": row.get("candidate_alias"),
                "reason": "highest worst DD among follow-up rows(후속 행 중 최악 손실폭 최고)",
                "next_probe": "prefer prune or pivot unless negative-slice review shows a structurally useful clue",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    dd_watch_candidates = [row for row in candidate_summary if as_float(row.get("worst_dd_percent")) >= 15.0]
    if len(dd_watch_candidates) == len(candidate_summary) and candidate_summary:
        rows.append(
            {
                "queue_id": "run267cc_q03_all_followup_rows_dd_watch_branch_boundary",
                "priority": "P0",
                "workstream": "branch_boundary",
                "reason": "all follow-up candidates remain at or above 15% worst DD(모든 후속 후보가 최악 손실폭 15% 이상)",
                "next_probe": "stop this repair loop unless run267CD defines one sharply bounded final check",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_failure_memory(candidate_summary: Sequence[Mapping[str, Any]], period_summary: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    high_dd_candidates = [row for row in candidate_summary if as_float(row.get("worst_dd_percent")) >= 15.0]
    rows: list[dict[str, Any]] = [
        {
            "memory_id": "run267cc_headline_positive_not_selection",
            "scope": "aggressive_impulse_replacement_followup(공격형 임펄스 대체 후속)",
            "evidence": rel(CANDIDATE_SUMMARY_PATH),
            "failure_mode": "both follow-up candidates are positive in 2025H2, but this is still a narrow P0 repair slice and Tier B routed evidence is blocked",
            "do_not_repeat": "do not claim selected candidate, research baseline, ONNX readiness, or goal achievement from headline positives",
            "salvage_condition": "use only for run267CD design with curve zoom, DD-shape, and weak-slice checks",
        }
    ]
    if high_dd_candidates:
        rows.append(
            {
                "memory_id": "run267cc_dd_watch_candidates",
                "scope": ";".join(str(row.get("candidate_alias")) for row in high_dd_candidates),
                "evidence": rel(CANDIDATE_SUMMARY_PATH),
                "failure_mode": "worst DD at or above 15 percent in at least one period",
                "do_not_repeat": "do not chase net profit with only threshold or filter stacking",
                "salvage_condition": "continue only if curve shape and weak-period behavior remain acceptable under broader pressure",
            }
        )
    if any(str(row.get("target_period")) == "2025H2" and str(row.get("period_read")).startswith("dd_watch") for row in period_summary):
        rows.append(
            {
                "memory_id": "run267cc_2025h2_dd_watch",
                "scope": "2025H2",
                "evidence": rel(PERIOD_SUMMARY_PATH),
                "failure_mode": "2025H2 shows the most visible DD watch pressure in the aggressive impulse profile",
                "do_not_repeat": "do not micro-tune only 2025H2 loss without broader candidate comparison",
                "salvage_condition": "compare against candidate summaries and negative slices before any next branch",
            }
        )
    return rows


def forensic_summary(rows: Sequence[Mapping[str, Any]], parser_checks: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
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


def performance_attribution(candidate_summary: Sequence[Mapping[str, Any]], period_summary: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = [
        {
            "subject": "profile_level",
            "observed_change": "aggressive impulse follow-up rows are all positive, but DD and period shape remain the gating issue",
            "comparison_baseline": rel(SOURCE_KPI_SUMMARY_PATH),
            "likely_drivers": "nonflat impulse replacement score appears to preserve trade frequency across adjacent periods",
            "segment_checks": "month/weekday/hour/session/direction/chron_segment checked for 2025H2 follow-up rows",
            "trade_shape": "trade count remains broad enough for a review, but drawdown watch exists in 2025H2 and high-net candidates",
            "alternative_explanations": "same aggressive profile and Tier A-only boundary; no true fallback or Adapter final structure yet",
            "attribution_confidence": "medium_with_boundary(중간, 경계부)",
            "next_probe": NEXT_ACTION,
        }
    ]
    for row in candidate_summary:
        rows.append(
            {
                "subject": row.get("candidate_alias"),
                "observed_change": f"total_net={cell(row.get('total_net_profit'))};min_pf={cell(row.get('min_profit_factor'))};worst_dd={cell(row.get('worst_dd_percent'))}",
                "comparison_baseline": "same follow-up branch across candidate aliases in 2025H2",
                "likely_drivers": "candidate-specific response to aggressive impulse replacement",
                "segment_checks": "candidate_period_review and negative_slice_summary",
                "trade_shape": f"total_trades={row.get('total_trades')};min_period_trades={row.get('min_period_trades')}",
                "alternative_explanations": "period sample and score-table materialization effects",
                "attribution_confidence": "medium_with_boundary(중간, 경계부)",
                "next_probe": "carry as watch only; no selected baseline",
            }
        )
    for row in period_summary:
        rows.append(
            {
                "subject": row.get("target_period"),
                "observed_change": f"period_total_net={cell(row.get('total_net_profit'))};worst_dd={cell(row.get('worst_dd_percent'))}",
                "comparison_baseline": "other adjacent periods in run267CC",
                "likely_drivers": "market-period interaction with aggressive impulse replacement",
                "segment_checks": "period_summary and negative_slice_summary",
                "trade_shape": f"candidate_count={row.get('candidate_count')};weakest_candidate={row.get('weakest_candidate')}",
                "alternative_explanations": "period-specific volatility or tester sample shape",
                "attribution_confidence": "medium_with_boundary(중간, 경계부)",
                "next_probe": "avoid single-period micro repair; compare candidate-level curve shape",
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
    dd_watch = [row for row in result["candidate_summary"] if as_float(row.get("worst_dd_percent")) >= 15.0]
    return [
        {"field": "run_status", "value": result["status"], "judgment": result["judgment"], "evidence": rel(REVIEW_RESULT_PATH)},
        {"field": "trade_records", "value": result["trade_record_count"], "judgment": "parsed_trade_list_evidence", "evidence": rel(TRADE_RECORDS_PATH)},
        {"field": "negative_slice_count", "value": result["negative_slice_count"], "judgment": "weak_slices_present", "evidence": rel(NEGATIVE_SLICE_PATH)},
        {"field": "dd_watch_candidate_count", "value": len(dd_watch), "judgment": "not_selection_ready", "evidence": rel(CANDIDATE_SUMMARY_PATH)},
        {"field": "selected_candidate", "value": "none", "judgment": "not_selected", "evidence": "curve_time_slice_trade_quality_not_sufficient_for_selection"},
        {"field": "selected_research_baseline", "value": "none", "judgment": "not_selected", "evidence": "research_pool_still_racing"},
        {"field": "onnx_readiness", "value": "not_claimed", "judgment": "not_ready", "evidence": "goal_gate_not_met"},
        {"field": "goal_achieve", "value": "not_claimed", "judgment": "not_claimed", "evidence": "full_objective_not_met"},
        {"field": "next_action", "value": result["next_action"], "judgment": "design_followup_or_prune", "evidence": rel(FOLLOWUP_QUEUE_PATH)},
    ]


def report_markdown(result: Mapping[str, Any]) -> str:
    candidate_rows = result["candidate_summary"]
    period_rows = result["period_summary"]
    period_review = result["candidate_period_review"]
    negative_rows = result["negative_slices"][:12]
    lines = [
        "# Stage267 Run267CC Aggressive Impulse Follow-up Balance/Time-slice/Trade-quality Review(267단계 267CC 공격형 임펄스 후속 잔액/시간구간/거래품질 검토)",
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
        "Action(행동): run267CB(267CB 실행)의 2개 MT5(MetaTrader 5, 메타트레이더5) report(보고서)를 trade list(거래 목록)로 다시 읽고, s264_aih/s258_stc의 2025H2 후속 형태를 분해했다.",
        "Effect(효과): headline KPI(대표 핵심 성과 지표)가 모두 양수여도 DD(drawdown, 손실폭), 약한 월, 후반 구간, 시간 구간 구멍을 숨기지 않는다.",
        "",
        "## Candidate Summary(후보 요약)",
        "",
        "| candidate(후보) | total net(총 순수익) | min PF(최저 수익 팩터) | worst DD%(최악 손실폭 %) | trades(거래 수) | worst period(최악 기간) | read(판독) |",
        "| --- | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for row in candidate_rows:
        lines.append(
            "| `{candidate}` | {net} | {pf} | {dd} | {trades} | `{period}` {period_net} | `{read}` |".format(
                candidate=row.get("candidate_alias", ""),
                net=cell(row.get("total_net_profit")),
                pf=cell(row.get("min_profit_factor")),
                dd=cell(row.get("worst_dd_percent")),
                trades=cell(row.get("total_trades")),
                period=row.get("worst_period", ""),
                period_net=cell(row.get("worst_period_net")),
                read=row.get("candidate_read", ""),
            )
        )
    lines.extend(
        [
            "",
            "## Period Summary(기간 요약)",
            "",
            "| period(기간) | total net(총 순수익) | mean PF(평균 수익 팩터) | worst DD%(최악 손실폭 %) | weakest candidate(가장 약한 후보) | read(판독) |",
            "| --- | ---: | ---: | ---: | --- | --- |",
        ]
    )
    for row in period_rows:
        lines.append(
            "| `{period}` | {net} | {pf} | {dd} | `{weak}` {weak_net} | `{read}` |".format(
                period=row.get("target_period", ""),
                net=cell(row.get("total_net_profit")),
                pf=cell(row.get("mean_profit_factor")),
                dd=cell(row.get("worst_dd_percent")),
                weak=row.get("weakest_candidate", ""),
                weak_net=cell(row.get("weakest_candidate_net")),
                read=row.get("period_read", ""),
            )
        )
    lines.extend(
        [
            "",
            "## Candidate/Period Review(후보/기간 검토)",
            "",
            "| candidate(후보) | period(기간) | net(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭 %) | worst month(최악 월) | curve read(곡선 판독) |",
            "| --- | --- | ---: | ---: | ---: | ---: | --- | --- |",
        ]
    )
    for row in period_review:
        lines.append(
            "| `{candidate}` | `{period}` | {net} | {pf} | {trades} | {dd} | `{month}` {month_net} | `{read}` |".format(
                candidate=row.get("candidate_alias", ""),
                period=row.get("target_period", ""),
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
            "| candidate(후보) | period(기간) | axis(축) | bucket(구간) | trades(거래 수) | net(순수익) | DD%(손실폭 %) |",
            "| --- | --- | --- | --- | ---: | ---: | ---: |",
        ]
    )
    for row in negative_rows:
        lines.append(
            "| `{candidate}` | `{period}` | `{axis}` | `{bucket}` | {trades} | {net} | {dd} |".format(
                candidate=row.get("candidate_alias", ""),
                period=row.get("target_period", ""),
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
            "## Judgment Boundary(판정 경계)",
            "",
            "- run267CC(267CC 실행)는 review evidence(검토 근거)이며 candidate selection(후보 선택)이 아니다.",
            "- all-positive(전부 양수) 결과는 좋은 단서지만, 두 후보 모두 DD watch(손실폭 관찰)에 걸리면 repair loop(수리 반복)를 길게 끌지 않는다.",
            "- ONNX parity(ONNX 동등성)와 ONNX conversion(ONNX 변환)은 시작하지 않는다.",
            "",
            "## Artifacts(산출물)",
            "",
            f"- trade_records(거래 기록): `{rel(TRADE_RECORDS_PATH)}`",
            f"- time_slice_kpi(시간 구간 KPI): `{rel(TIME_SLICE_KPI_PATH)}`",
            f"- curve_diagnostics(곡선 진단): `{rel(CURVE_DIAGNOSTICS_PATH)}`",
            f"- candidate_period_review(후보 기간 검토): `{rel(CANDIDATE_PERIOD_REVIEW_PATH)}`",
            f"- candidate_summary(후보 요약): `{rel(CANDIDATE_SUMMARY_PATH)}`",
            f"- period_summary(기간 요약): `{rel(PERIOD_SUMMARY_PATH)}`",
            f"- followup_queue(후속 대기열): `{rel(FOLLOWUP_QUEUE_PATH)}`",
            f"- failure_memory(실패 기억): `{rel(FAILURE_MEMORY_PATH)}`",
            f"- next_action(다음 행동): `{result['next_action']}`",
        ]
    )
    return "\n".join(lines) + "\n"


def result_payload() -> dict[str, Any]:
    created_at = utc_now()
    execution_result = read_json(SOURCE_EXECUTION_RESULT_PATH)
    forensic_rows = read_csv(SOURCE_FORENSICS_PATH)
    trade_rows, parser_errors, parser_checks = build_trade_records(execution_result)
    time_rows = build_time_slice_rows(trade_rows)
    curve_rows = build_curve_rows(trade_rows, time_rows, execution_result)
    candidate_period = build_candidate_period_review(curve_rows)
    candidate_summary = build_candidate_summary(curve_rows)
    period_summary = build_period_summary(curve_rows)
    negative_rows = negative_slices(time_rows)
    followup_rows = build_followup_queue(candidate_summary, period_summary)
    failure_rows = build_failure_memory(candidate_summary, period_summary)
    forensic_rows_out = forensic_summary(forensic_rows, parser_checks)
    attribution_rows = performance_attribution(candidate_summary, period_summary)
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
        "candidate_period_review": candidate_period,
        "candidate_summary": candidate_summary,
        "period_summary": period_summary,
        "negative_slices": negative_rows,
        "followup_queue": followup_rows,
        "failure_memory": failure_rows,
        "parser_checks": parser_checks,
        "parser_errors": parser_errors,
        "forensic_summary": forensic_rows_out,
        "performance_attribution": attribution_rows,
        "trade_record_count": len(trade_rows),
        "time_slice_row_count": len(time_rows),
        "curve_row_count": len(curve_rows),
        "negative_slice_count": len(negative_rows),
        "source_execution_result": rel(SOURCE_EXECUTION_RESULT_PATH),
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
    }
    return result


def write_outputs(result: Mapping[str, Any]) -> None:
    write_csv(TRADE_RECORDS_PATH, result["trade_records"])
    write_csv(TIME_SLICE_KPI_PATH, result["time_slice_rows"])
    write_csv(CURVE_DIAGNOSTICS_PATH, result["curve_rows"])
    write_csv(CANDIDATE_PERIOD_REVIEW_PATH, result["candidate_period_review"])
    write_csv(CANDIDATE_SUMMARY_PATH, result["candidate_summary"])
    write_csv(PERIOD_SUMMARY_PATH, result["period_summary"])
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
            "curve_row_count": result["curve_row_count"],
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
                "executed_attempts": rel(SOURCE_EXECUTED_ATTEMPTS_PATH),
                "source_attempt_manifest": rel(SOURCE_ATTEMPT_MANIFEST_PATH),
                "source_variant_manifest": rel(SOURCE_VARIANT_MANIFEST_PATH),
                "source_runtime_contract": rel(SOURCE_RUNTIME_CONTRACT_PATH),
                "execution_report": rel(SOURCE_EXECUTION_REPORT_PATH),
            },
            "producer": rel(PRODUCER_PATH),
            "consumer": result["next_action"],
            "artifact_paths": {
                "trade_records": rel(TRADE_RECORDS_PATH),
                "time_slice_kpi": rel(TIME_SLICE_KPI_PATH),
                "curve_diagnostics": rel(CURVE_DIAGNOSTICS_PATH),
                "candidate_period_review": rel(CANDIDATE_PERIOD_REVIEW_PATH),
                "candidate_summary": rel(CANDIDATE_SUMMARY_PATH),
                "period_summary": rel(PERIOD_SUMMARY_PATH),
                "followup_queue": rel(FOLLOWUP_QUEUE_PATH),
                "failure_memory": rel(FAILURE_MEMORY_PATH),
                "report": rel(REPORT_PATH),
            },
            "availability": "tracked",
            "lineage_judgment": "connected_with_boundary",
        },
    )
    write_md(REPORT_PATH, report_markdown(result))


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


def prepend_current_focus(text: str, focus_block: str) -> str:
    marker = "current_focus:\n"
    if focus_block.strip() in text or marker not in text:
        return text
    return text.replace(marker, marker + focus_block, 1)


def update_stage267_workspace_block(text: str, *, status: str, next_action: str, report_entry: str) -> str:
    lines = text.splitlines()
    output: list[str] = []
    in_stage267 = False
    report_seen = report_entry.strip() in text
    for line in lines:
        if line.startswith("current_run_id:"):
            output.append(f"current_run_id: {RUN_ID}")
            continue
        if line.startswith("stage267_baseline_candidate_racing_protocol:"):
            in_stage267 = True
            output.append(line)
            continue
        if in_stage267 and line and not line.startswith(" ") and not line.startswith("#"):
            if not report_seen:
                output.append(report_entry)
                report_seen = True
            in_stage267 = False
        if in_stage267:
            stripped = line.strip()
            if stripped.startswith("status:"):
                output.append(f"  status: {status}")
                continue
            if stripped.startswith("current_run_id:"):
                output.append(f"  current_run_id: {RUN_ID}")
                continue
            if stripped.startswith("last_completed_run_id:"):
                output.append(f"  last_completed_run_id: {RUN_ID}")
                continue
            if stripped.startswith("next_action:"):
                if not report_seen:
                    output.append(report_entry)
                    report_seen = True
                output.append(f"  next_action: {next_action}")
                continue
        output.append(line)
    if in_stage267 and not report_seen:
        output.append(report_entry)
    return "\n".join(output) + "\n"


def update_current_truth_docs(result: Mapping[str, Any]) -> None:
    status = str(result["status"])
    next_action = str(result["next_action"])
    report_line = f"- run267CC_aggressive_impulse_dd_shape_followup_balance_timeslice_trade_quality_review(267CC 공격형 임펄스 손실폭 형태 후속 잔액/시간구간/거래품질 검토): `{rel(REPORT_PATH)}`"
    block = "\n".join(
        [
            "Run267CC(267CC 실행)는 run267CB(267CB 실행)의 2개 MT5(MetaTrader 5, 메타트레이더5) 보고서를 trade list(거래 목록)로 다시 읽었다.",
            f"Effect(효과): trade records(거래 기록) `{result['trade_record_count']}`개, time-slice rows(시간 구간 행) `{result['time_slice_row_count']}`개, negative slices(음수 구간) `{result['negative_slice_count']}`개를 만들고 후보별 후속 DD-shape(손실폭 형태)를 다음 설계 입력으로 고정했다.",
            "Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.",
        ]
    )
    for path in (CURRENT_WORKING_STATE_PATH, SELECTION_STATUS_PATH, REVIEW_INDEX_PATH):
        text = io_path(path).read_text(encoding="utf-8-sig")
        text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
        text = replace_line_prefix(text, "- status(상태):", f"- status(상태): `{status}`")
        text = replace_line_prefix(text, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{status}`")
        text = replace_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
        text = replace_line_prefix(text, "- adapter_under_review(검토 중 어댑터):", "- adapter_under_review(검토 중 어댑터): `aggressive_impulse_dd_shape_followup_balance_timeslice_trade_quality_review`")
        text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{next_action}`")
        text = append_after_contains(text, "stage267_run267CB_aggressive_impulse_dd_shape_followup_mt5_execution.md", report_line)
        text = append_block_once(text, "Run267CC(267CC 실행)는", block)
        write_md(path, text)

    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    focus = (
        "- >-\n"
        f"  Stage267(267단계) run267CC(267CC 실행) aggressive impulse DD-shape follow-up balance/time-slice/trade-quality review(공격형 임펄스 손실폭 형태 후속 잔액/시간구간/거래품질 검토) `{status}`. "
        f"Effect(효과): run267CB(267CB 실행)의 2개 MT5(MetaTrader 5, 메타트레이더5) report(보고서)를 trade list(거래 목록), curve(곡선), weak slice(약한 구간)로 다시 읽었고 selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_current_focus(workspace, focus)
    workspace = update_stage267_workspace_block(
        workspace,
        status=status,
        next_action=next_action,
        report_entry=f"  run267CC_aggressive_impulse_dd_shape_followup_balance_timeslice_trade_quality_review_report_path: {rel(REPORT_PATH)}",
    )
    write_md(WORKSPACE_STATE_PATH, workspace)


def update_ledgers_and_artifacts(created_at: str, result: Mapping[str, Any]) -> None:
    status = str(result["status"])
    judgment = str(result["judgment"])
    next_action = str(result["next_action"])
    notes = (
        f"trade_records={result['trade_record_count']};time_slice_rows={result['time_slice_row_count']};"
        f"negative_slices={result['negative_slice_count']};next_action={next_action};selected_candidate=none."
    )
    stage_row = {
        "row_id": "stage267_run267CC_aggressive_impulse_dd_shape_followup_balance_timeslice_trade_quality_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "aggressive_impulse_dd_shape_followup_balance_timeslice_trade_quality_review",
        "tier_scope": "Tier A run267CB review; Tier B and actual routed total blocked until true fallback manifest exists",
        "scoreboard": "trade_shape_curve_time_slice_followup_review",
        "status": status,
        "judgment": judgment,
        "evidence_boundary": "trade_list_curve_timeslice_review_no_candidate_selection_no_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": notes,
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "baseline_candidate_racing_aggressive_impulse_followup_balance_timeslice_trade_quality_review",
        "status": status,
        "judgment": judgment,
        "path": rel(REPORT_PATH),
        "notes": notes,
    }
    project_row = {
        "ledger_row_id": f"{RUN_ID}__aggressive_impulse_dd_shape_followup_balance_timeslice_trade_quality_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "aggressive_impulse_dd_shape_followup_balance_timeslice_trade_quality_review",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "aggressive_impulse_dd_shape_followup_balance_timeslice_trade_quality_review",
        "tier_scope": "Tier A run267CB review; true fallback blocked",
        "kpi_scope": "balance_curve_time_slice_trade_quality",
        "scoreboard_lane": "aggressive_impulse_followup_trade_quality_review",
        "status": status,
        "judgment": judgment,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"trade_records={result['trade_record_count']};negative_slices={result['negative_slice_count']}",
        "guardrail_kpi": "selected_candidate=none;selected_research_baseline=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
        "external_verification_status": "completed_for_run267CB_trade_report_review",
        "notes": f"Next action: {next_action}.",
    }
    upsert_csv_rows(STAGE_LEDGER_PATH, STAGE_LEDGER_COLUMNS, [stage_row], key="row_id")
    upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [run_row], key="run_id")
    upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [project_row], key="ledger_row_id")
    entries = (
        ("stage267_run267CC_producer", "producer_script", PRODUCER_PATH, "Builds run267CC aggressive impulse follow-up balance/time-slice/trade-quality review."),
        ("stage267_run267CC_source_execution_result", "source_execution_result", SOURCE_EXECUTION_RESULT_PATH, "Source run267CB execution result."),
        ("stage267_run267CC_trade_records", "trade_records", TRADE_RECORDS_PATH, "Parsed trade records."),
        ("stage267_run267CC_time_slice_kpi", "time_slice_kpi", TIME_SLICE_KPI_PATH, "Time-slice KPI."),
        ("stage267_run267CC_curve_diagnostics", "curve_diagnostics", CURVE_DIAGNOSTICS_PATH, "Curve diagnostics."),
        ("stage267_run267CC_candidate_period_review", "candidate_period_review", CANDIDATE_PERIOD_REVIEW_PATH, "Candidate-period review."),
        ("stage267_run267CC_candidate_summary", "candidate_summary", CANDIDATE_SUMMARY_PATH, "Candidate follow-up summary."),
        ("stage267_run267CC_period_summary", "period_summary", PERIOD_SUMMARY_PATH, "Period summary."),
        ("stage267_run267CC_negative_slice_summary", "negative_slice_summary", NEGATIVE_SLICE_PATH, "Negative slice summary."),
        ("stage267_run267CC_followup_queue", "followup_queue", FOLLOWUP_QUEUE_PATH, "Follow-up queue."),
        ("stage267_run267CC_failure_memory", "failure_memory", FAILURE_MEMORY_PATH, "Failure memory."),
        ("stage267_run267CC_parser_checks", "parser_checks", PARSER_CHECKS_PATH, "Parser checks."),
        ("stage267_run267CC_forensic_summary", "forensic_summary", FORENSIC_SUMMARY_PATH, "Backtest forensic summary."),
        ("stage267_run267CC_performance_attribution", "performance_attribution", PERFORMANCE_ATTRIBUTION_PATH, "Performance attribution."),
        ("stage267_run267CC_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Result judgment."),
        ("stage267_run267CC_review_result", "review_result", REVIEW_RESULT_PATH, "Review result payload."),
        ("stage267_run267CC_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run manifest."),
        ("stage267_run267CC_lineage", "lineage", LINEAGE_PATH, "Lineage map."),
        ("stage267_run267CC_report", "review_report", REPORT_PATH, "User-facing report."),
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


def execute() -> dict[str, Any]:
    result = result_payload()
    write_outputs(result)
    update_ledgers_and_artifacts(str(result["created_at_utc"]), result)
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
                "curve_rows": result["curve_row_count"],
                "negative_slices": result["negative_slice_count"],
                "selected_candidate": result["selected_candidate"],
                "selected_research_baseline": result["selected_research_baseline"],
                "onnx_readiness": result["onnx_readiness"],
                "goal_achieve": result["goal_achieve"],
                "next_action": result["next_action"],
                "report": rel(REPORT_PATH),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
