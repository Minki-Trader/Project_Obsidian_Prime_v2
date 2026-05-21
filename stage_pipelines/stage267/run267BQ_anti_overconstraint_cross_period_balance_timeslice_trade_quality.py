from __future__ import annotations

import csv
import json
import math
import sys
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
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
from stage_pipelines.stage267 import run267BO_aggressive_second_tranche_cross_period_mt5_executor as mt5_executor
from stage_pipelines.stage267 import run267BP_state_acceleration_zero_trade_gap_classification as gap_classifier


STAGE_ID = gap_classifier.STAGE_ID
RUN_NUMBER = "run267BQ"
RUN_ID = "run267BQ_stage267_anti_overconstraint_cross_period_balance_timeslice_trade_quality_v1"
PARENT_RUN_ID = gap_classifier.RUN_ID
SOURCE_MT5_RUN_ID = mt5_executor.RUN_ID
STATUS = "run267BQ_anti_overconstraint_cross_period_balance_timeslice_trade_quality_review_completed"
JUDGMENT = "cross_period_curve_trade_quality_review_completed_no_candidate_selection"
CLAIM_BOUNDARY = gap_classifier.CLAIM_BOUNDARY
NEXT_ACTION = "run267BR_design_anti_overconstraint_cross_period_followup_or_prune"

STAGE_ROOT = gap_classifier.STAGE_ROOT
REVIEWS_ROOT = gap_classifier.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "anti_overconstraint_cross_period_balance_timeslice_trade_quality"

SOURCE_GAP_CLASSIFICATION_PATH = gap_classifier.GAP_CLASSIFICATION_PATH
SOURCE_PERFORMANCE_ATTRIBUTION_PATH = gap_classifier.PERFORMANCE_ATTRIBUTION_PATH
SOURCE_FORENSIC_GAP_RECEIPT_PATH = gap_classifier.FORENSIC_GAP_RECEIPT_PATH
SOURCE_MT5_EXECUTION_RESULT_PATH = mt5_executor.EXECUTION_RESULT_PATH
SOURCE_MT5_KPI_SUMMARY_PATH = mt5_executor.KPI_SUMMARY_PATH
SOURCE_MT5_FORENSICS_PATH = mt5_executor.FORENSICS_PATH
SOURCE_BP_REPORT_PATH = gap_classifier.REPORT_PATH

TRADE_RECORDS_PATH = RUN_ROOT / "trade_records.csv"
TIME_SLICE_KPI_PATH = RUN_ROOT / "time_slice_kpi.csv"
CURVE_DIAGNOSTICS_PATH = RUN_ROOT / "curve_diagnostics.csv"
CROSS_PERIOD_SUMMARY_PATH = RUN_ROOT / "cross_period_summary.csv"
NEGATIVE_SLICE_PATH = RUN_ROOT / "negative_slice_summary.csv"
PARSER_CHECKS_PATH = RUN_ROOT / "parser_checks.csv"
EXCLUDED_GAP_ATTEMPTS_PATH = RUN_ROOT / "excluded_gap_attempts.csv"
RESULT_JUDGMENT_PATH = RUN_ROOT / "result_judgment.csv"
RUN_MANIFEST_PATH = RUN_ROOT / "run_manifest.json"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267BQ_anti_overconstraint_cross_period_balance_timeslice_trade_quality.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267BQ_anti_overconstraint_cross_period_balance_timeslice_trade_quality.py")

STAGE_LEDGER_PATH = gap_classifier.STAGE_LEDGER_PATH
PROJECT_LEDGER_PATH = gap_classifier.PROJECT_LEDGER_PATH
RUN_REGISTRY_PATH = gap_classifier.RUN_REGISTRY_PATH
ARTIFACT_REGISTRY_PATH = gap_classifier.ARTIFACT_REGISTRY_PATH
CURRENT_WORKING_STATE_PATH = gap_classifier.CURRENT_WORKING_STATE_PATH
WORKSPACE_STATE_PATH = gap_classifier.WORKSPACE_STATE_PATH
SELECTION_STATUS_PATH = gap_classifier.SELECTION_STATUS_PATH
REVIEW_INDEX_PATH = gap_classifier.REVIEW_INDEX_PATH

STAGE_LEDGER_COLUMNS = gap_classifier.STAGE_LEDGER_COLUMNS
ARTIFACT_COLUMNS = gap_classifier.ARTIFACT_COLUMNS

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


def absolutize(path_text: str) -> Path:
    path = Path(path_text)
    return path if path.is_absolute() else REPO_ROOT / path


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


def max_closed_balance_drawdown(rows: Sequence[Mapping[str, Any]]) -> tuple[float, float, int, float, float]:
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
    return max_dd, max_dd_pct, longest_underwater, share, min_balance


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
    dd, dd_pct, underwater, underwater_share, min_balance = max_closed_balance_drawdown(ordered)
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
        "min_closed_balance": min_balance,
    }


def slice_read(row: Mapping[str, Any]) -> str:
    count = as_int(row.get("trade_count"))
    net = as_float(row.get("net_profit"))
    dd_pct = as_float(row.get("closed_balance_max_drawdown_percent"))
    if count < 3:
        return "thin_slice(얇은 구간)"
    if net <= -250.0 or dd_pct >= 35.0:
        return "deep_negative_or_dd_slice(깊은 손실 또는 손실폭 구간)"
    if net < -120.0:
        return "negative_fragile_slice(손실 취약 구간)"
    if net < 0.0:
        return "minor_negative_slice(작은 손실 구간)"
    return "measured_slice(측정 구간)"


def curve_read(curve: Mapping[str, Any]) -> str:
    net = as_float(curve.get("net_profit"))
    pf = as_float(curve.get("profit_factor"))
    dd_pct = max(as_float(curve.get("closed_balance_max_drawdown_percent")), as_float(curve.get("report_drawdown_percent")))
    positive_month_ratio = as_float(curve.get("positive_month_ratio"))
    worst_month_net = as_float(curve.get("worst_month_net"))
    if net <= 0.0 or pf <= 1.0:
        return "fragile_or_negative_no_extension(취약 또는 음수, 확장 금지)"
    if pf <= 1.10 or dd_pct >= 25.0 or worst_month_net <= -250.0:
        return "positive_but_uncomfortable_holes(양수지만 불편한 구멍)"
    if pf >= 1.50 and dd_pct <= 15.0 and positive_month_ratio >= 0.55:
        return "constructive_watch_not_selection(건설적 관찰, 선택 아님)"
    return "mixed_needs_trade_quality_review(혼합, 거래 품질 검토 필요)"


def decision_read(curve: Mapping[str, Any]) -> str:
    read = str(curve.get("curve_read", ""))
    if read.startswith("constructive"):
        return "watch_more_pressure_no_selection(추가 압박 관찰, 선택 아님)"
    if read.startswith("positive_but_uncomfortable"):
        return "fragile_watch_or_prune(취약 관찰 또는 가지치기)"
    if read.startswith("fragile_or_negative"):
        return "prune_or_redesign_surface(가지치기 또는 표면 재설계)"
    return "diagnostic_only(진단 전용)"


def eligible_attempts(gap_rows: Sequence[Mapping[str, Any]]) -> list[Mapping[str, Any]]:
    return [
        row
        for row in gap_rows
        if row.get("variant_id") == "anti_overconstraint_prune"
        and row.get("classification") == "completed_runtime_kpi"
        and row.get("next_probe") == "include_in_run267BQ_balance_timeslice_trade_quality_review"
    ]


def mt5_record_by_attempt(execution_result: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    output: dict[str, Mapping[str, Any]] = {}
    for record in execution_result.get("mt5_kpi_records", []):
        attempt_name = str(record.get("report", {}).get("attempt_name") or "")
        if attempt_name:
            output[attempt_name] = record
    return output


def build_trade_records(
    gap_rows: Sequence[Mapping[str, Any]],
    execution_result: Mapping[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    records = mt5_record_by_attempt(execution_result)
    trade_rows: list[dict[str, Any]] = []
    parser_checks: list[dict[str, Any]] = []
    for attempt in eligible_attempts(gap_rows):
        attempt_name = str(attempt.get("attempt_name"))
        record = records.get(attempt_name)
        if not record:
            parser_checks.append({"attempt_name": attempt_name, "parser_status": "missing_kpi_record"})
            continue
        metrics_payload = record.get("metrics", {})
        report_path = absolutize(str(metrics_payload.get("report_path") or attempt.get("report_path") or ""))
        parsed = parse_mt5_trade_report(report_path)
        trades = pair_deals_into_trades(parsed["deals"])
        expected = as_int(metrics_payload.get("trade_count") or attempt.get("report_trade_count"))
        parser_checks.append(
            {
                "attempt_name": attempt_name,
                "record_view": record.get("record_view"),
                "period_id": attempt.get("period_id"),
                "target_period": attempt.get("target_period"),
                "report_path": rel(report_path),
                "expected_trade_count": expected,
                "parsed_deal_count": len(parsed["deals"]),
                "parsed_trade_count": len(trades),
                "trade_count_delta": len(trades) - expected,
                "parser_status": "matched" if len(trades) == expected else "count_mismatch",
            }
        )
        ordered = sorted(trades, key=lambda item: item.close_time)
        total = len(ordered)
        for index, trade in enumerate(ordered):
            close_time = trade.close_time
            open_time = trade.open_time
            close_hour = close_time.strftime("%H")
            trade_rows.append(
                {
                    "run_id": RUN_ID,
                    "source_run_id": SOURCE_MT5_RUN_ID,
                    "source_gap_run_id": PARENT_RUN_ID,
                    "attempt_name": attempt_name,
                    "record_view": record.get("record_view"),
                    "queue_id": attempt.get("queue_id"),
                    "candidate_id": attempt.get("candidate_id"),
                    "candidate_alias": attempt.get("candidate_alias"),
                    "candidate_role": attempt.get("candidate_role"),
                    "variant_id": attempt.get("variant_id"),
                    "target_period": attempt.get("target_period"),
                    "period_id": attempt.get("period_id"),
                    "source_first_tranche_attempt_name": attempt.get("source_first_tranche_attempt_name"),
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
                    "source_report_path": rel(report_path),
                }
            )
    return trade_rows, parser_checks


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
            "target_period",
            "period_id",
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
                target_period,
                period_id,
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
                    "target_period": target_period,
                    "period_id": period_id,
                    "route_role": route_role,
                    "axis": axis,
                    "bucket": bucket,
                    **item,
                    "slice_read": slice_read(item),
                }
            )
    return output


def report_metrics_by_view(execution_result: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
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
    report_metrics = report_metrics_by_view(execution_result)
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
        "target_period",
        "period_id",
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
            target_period,
            period_id,
            route_role,
        ) = key
        item = metrics(rows)
        month_rows = [
            row
            for row in time_rows
            if row.get("record_view") == record_view and row.get("axis") == "month" and as_int(row.get("trade_count")) >= 3
        ]
        chron_rows = [
            row
            for row in time_rows
            if row.get("record_view") == record_view and row.get("axis") == "chron_segment" and as_int(row.get("trade_count")) >= 3
        ]
        negative_months = [row for row in month_rows if as_float(row.get("net_profit")) < 0.0]
        worst_month = min(month_rows, key=lambda row: as_float(row.get("net_profit")), default={})
        best_month = max(month_rows, key=lambda row: as_float(row.get("net_profit")), default={})
        chron_by_bucket = {str(row.get("bucket")): row for row in chron_rows}
        metric_payload = report_metrics.get(str(record_view), {})
        row = {
            "record_view": record_view,
            "attempt_name": attempt_name,
            "tier_scope": tier_scope,
            "candidate_id": candidate_id,
            "candidate_alias": alias,
            "candidate_role": role,
            "variant_id": variant_id,
            "target_period": target_period,
            "period_id": period_id,
            "route_role": route_role,
            **item,
            "report_equity_drawdown_percent": metric_payload.get("equity_drawdown_maximal_percent"),
            "report_balance_drawdown_percent": metric_payload.get("balance_drawdown_maximal_percent"),
            "report_drawdown_percent": metric_payload.get("max_drawdown_percent"),
            "report_recovery_factor": metric_payload.get("recovery_factor"),
            "positive_month_ratio": (len(month_rows) - len(negative_months)) / len(month_rows) if month_rows else 0.0,
            "negative_month_count": len(negative_months),
            "worst_month": worst_month.get("bucket", ""),
            "worst_month_net": worst_month.get("net_profit", ""),
            "best_month": best_month.get("bucket", ""),
            "best_month_net": best_month.get("net_profit", ""),
            "chron_early_net": chron_by_bucket.get("chron_early", {}).get("net_profit", ""),
            "chron_mid_net": chron_by_bucket.get("chron_mid", {}).get("net_profit", ""),
            "chron_late_net": chron_by_bucket.get("chron_late", {}).get("net_profit", ""),
            "source_chart_path": charts.get(str(record_view), ""),
        }
        row["curve_read"] = curve_read(row)
        row["decision_read"] = decision_read(row)
        output.append(row)
    return sorted(output, key=lambda row: str(row.get("target_period")))


def build_cross_period_summary(curve_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = sorted(curve_rows, key=lambda row: str(row.get("target_period")))
    by_period = {str(row.get("target_period")): row for row in rows}
    base = by_period.get("2023H2")
    output: list[dict[str, Any]] = []
    for row in rows:
        net_delta = as_float(row.get("net_profit")) - as_float(base.get("net_profit")) if base else 0.0
        pf_delta = as_float(row.get("profit_factor")) - as_float(base.get("profit_factor")) if base else 0.0
        dd_delta = as_float(row.get("closed_balance_max_drawdown_percent")) - as_float(base.get("closed_balance_max_drawdown_percent")) if base else 0.0
        output.append(
            {
                "candidate_id": row.get("candidate_id"),
                "candidate_alias": row.get("candidate_alias"),
                "variant_id": row.get("variant_id"),
                "target_period": row.get("target_period"),
                "period_id": row.get("period_id"),
                "trade_count": row.get("trade_count"),
                "net_profit": row.get("net_profit"),
                "profit_factor": row.get("profit_factor"),
                "expectancy": row.get("expectancy"),
                "closed_balance_max_drawdown_percent": row.get("closed_balance_max_drawdown_percent"),
                "report_drawdown_percent": row.get("report_drawdown_percent"),
                "positive_month_ratio": row.get("positive_month_ratio"),
                "worst_month": row.get("worst_month"),
                "worst_month_net": row.get("worst_month_net"),
                "chron_early_net": row.get("chron_early_net"),
                "chron_mid_net": row.get("chron_mid_net"),
                "chron_late_net": row.get("chron_late_net"),
                "net_delta_vs_2023h2": net_delta,
                "pf_delta_vs_2023h2": pf_delta,
                "dd_pct_delta_vs_2023h2": dd_delta,
                "curve_read": row.get("curve_read"),
                "decision_read": row.get("decision_read"),
            }
        )
    return output


def negative_slices(time_rows: Sequence[Mapping[str, Any]], limit: int = 18) -> list[dict[str, Any]]:
    rows = [
        dict(row)
        for row in time_rows
        if as_float(row.get("net_profit")) < 0.0 and as_int(row.get("trade_count")) >= 3
    ]
    return sorted(rows, key=lambda row: (as_float(row.get("net_profit")), -as_int(row.get("trade_count"))))[:limit]


def result_judgment_rows(summary_rows: Sequence[Mapping[str, Any]], negative_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    fragile = [row for row in summary_rows if str(row.get("decision_read")).startswith("fragile") or str(row.get("decision_read")).startswith("prune")]
    return [
        {"field": "run_status", "value": STATUS, "judgment": JUDGMENT, "evidence": f"period_rows={len(summary_rows)}"},
        {"field": "cross_period_fragility", "value": len(fragile), "judgment": "uncomfortable_holes_present", "evidence": f"negative_slices={len(negative_rows)}"},
        {"field": "selected_candidate", "value": "none", "judgment": "not_selected", "evidence": "balance_timeslice_trade_quality_not_strong_enough"},
        {"field": "selected_research_baseline", "value": "none", "judgment": "not_selected", "evidence": "research_pool_still_racing"},
        {"field": "onnx_readiness", "value": "not_claimed", "judgment": "not_ready", "evidence": "goal_gate_not_met"},
        {"field": "goal_achieve", "value": "not_claimed", "judgment": "not_claimed", "evidence": "full_objective_not_met"},
        {"field": "next_action", "value": NEXT_ACTION, "judgment": "design_followup_or_prune", "evidence": "cross_period_review_completed"},
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


def prepend_current_focus(text: str, focus_block: str) -> str:
    marker = "current_focus:\n"
    if focus_block.strip() in text or marker not in text:
        return text
    return text.replace(marker, marker + focus_block, 1)


def update_stage267_workspace_block(text: str, *, report_entry: str) -> str:
    lines = text.splitlines()
    output: list[str] = []
    in_stage267 = False
    inserted_report = report_entry.strip() in text
    for line in lines:
        if line.startswith("current_run_id:"):
            output.append(f"current_run_id: {RUN_ID}")
            continue
        if line.startswith("stage267_baseline_candidate_racing_protocol:"):
            in_stage267 = True
            output.append(line)
            continue
        if in_stage267 and line and not line.startswith(" ") and not line.startswith("#"):
            if not inserted_report:
                output.append(report_entry)
                inserted_report = True
            in_stage267 = False
        if in_stage267:
            stripped = line.strip()
            if stripped.startswith("status:"):
                output.append(f"  status: {STATUS}")
                continue
            if stripped.startswith("current_run_id:"):
                output.append(f"  current_run_id: {RUN_ID}")
                continue
            if stripped.startswith("last_completed_run_id:"):
                output.append(f"  last_completed_run_id: {RUN_ID}")
                continue
            if stripped.startswith("next_action:"):
                if not inserted_report:
                    output.append(report_entry)
                    inserted_report = True
                output.append(f"  next_action: {NEXT_ACTION}")
                continue
        output.append(line)
    if in_stage267 and not inserted_report:
        output.append(report_entry)
    return "\n".join(output) + "\n"


def update_current_truth_docs(result: Mapping[str, Any]) -> None:
    report_line = f"- run267BQ_anti_overconstraint_cross_period_balance_timeslice_trade_quality(267BQ 과제약 제거 확장 기간 잔액/시간구간/거래품질): `{rel(REPORT_PATH)}`"
    block = "\n".join(
        [
            "Run267BQ(267BQ 실행)는 run267BP(267BP 실행)에서 남긴 3개 anti_overconstraint_prune(과제약 제거) 완료 행을 거래 목록(trade list, 거래 목록)으로 다시 읽었다.",
            f"Effect(효과): trade records(거래 기록) `{result['trade_record_count']}`개, time-slice rows(시간 구간 행) `{result['time_slice_row_count']}`개, negative slices(음수 구간) `{result['negative_slice_count']}`개를 만들었고, 확장 기간 안정성이 아직 불편함을 기록했다.",
            "Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준선), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.",
        ]
    )
    for path in (CURRENT_WORKING_STATE_PATH, SELECTION_STATUS_PATH, REVIEW_INDEX_PATH):
        text = io_path(path).read_text(encoding="utf-8-sig")
        text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
        text = replace_line_prefix(text, "- status(상태):", f"- status(상태): `{STATUS}`")
        text = replace_line_prefix(text, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
        text = replace_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
        text = replace_line_prefix(text, "- next_run(다음 실행):", f"- next_run(다음 실행): `{NEXT_ACTION}`")
        text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
        text = replace_line_prefix(
            text,
            "- adapter_under_review(검토 중 어댑터):",
            "- adapter_under_review(검토 중 어댑터): `anti_overconstraint_cross_period_balance_timeslice_trade_quality`",
        )
        text = append_after_contains(text, "stage267_run267BP_state_acceleration_zero_trade_gap_classification.md", report_line)
        text = append_block_once(text, "Run267BQ(267BQ 실행)는", block)
        write_md(path, text)
    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    focus = (
        "- >-\n"
        f"  Stage267(267단계) run267BQ(267BQ 실행) anti-overconstraint cross-period balance/time-slice/trade-quality review(과제약 제거 확장 기간 잔액/시간구간/거래품질 검토) `{STATUS}`. "
        "Effect(효과): 2023H2 강세와 2025H1/2025H2 약화를 거래 목록(trade list, 거래 목록), 월/요일/시간/세션 구간, closed balance curve(폐쇄 잔액 곡선)로 분해했고 selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_current_focus(workspace, focus)
    workspace = update_stage267_workspace_block(
        workspace,
        report_entry=f"  run267BQ_anti_overconstraint_cross_period_balance_timeslice_trade_quality_report_path: {rel(REPORT_PATH)}",
    )
    write_md(WORKSPACE_STATE_PATH, workspace)


def update_ledgers_and_artifacts(created_at: str, result: Mapping[str, Any]) -> None:
    notes = (
        f"trade_records={result['trade_record_count']};summary_rows={len(result['cross_period_summary'])};"
        f"negative_slices={result['negative_slice_count']};next_action={NEXT_ACTION};selected_candidate=none."
    )
    stage_row = {
        "row_id": "stage267_run267BQ_anti_overconstraint_cross_period_balance_timeslice_trade_quality",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "anti_overconstraint_cross_period_balance_timeslice_trade_quality",
        "tier_scope": "Tier A anti_overconstraint cross-period review; Tier B and actual routed total blocked until true fallback manifest exists",
        "scoreboard": "balance_timeslice_trade_quality_cross_period",
        "status": STATUS,
        "judgment": JUDGMENT,
        "evidence_boundary": "trade_list_curve_timeslice_review_no_candidate_selection_no_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": notes,
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "baseline_candidate_racing_anti_overconstraint_cross_period_balance_timeslice_trade_quality",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": notes,
    }
    project_row = {
        "ledger_row_id": f"{RUN_ID}__anti_overconstraint_cross_period_balance_timeslice_trade_quality",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "anti_overconstraint_cross_period_balance_timeslice_trade_quality",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "anti_overconstraint_cross_period_balance_timeslice_trade_quality",
        "tier_scope": "Tier A anti_overconstraint cross-period review; true fallback blocked",
        "kpi_scope": "balance_curve_time_slice_trade_quality",
        "scoreboard_lane": "cross_period_trade_quality_review",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"trade_records={result['trade_record_count']};negative_slices={result['negative_slice_count']}",
        "guardrail_kpi": "selected_candidate=none;selected_research_baseline=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
        "external_verification_status": "completed_for_run267BO_trade_report_review",
        "notes": f"Next action: {NEXT_ACTION}.",
    }
    upsert_csv_rows(STAGE_LEDGER_PATH, STAGE_LEDGER_COLUMNS, [stage_row], key="row_id")
    upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [run_row], key="run_id")
    upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [project_row], key="ledger_row_id")
    entries = (
        ("stage267_run267BQ_producer", "producer_script", PRODUCER_PATH, "Builds anti_overconstraint cross-period balance/time-slice/trade-quality review."),
        ("stage267_run267BQ_source_gap_classification", "source_gap_classification", SOURCE_GAP_CLASSIFICATION_PATH, "Source run267BP gap classification."),
        ("stage267_run267BQ_source_performance_attribution", "source_performance_attribution", SOURCE_PERFORMANCE_ATTRIBUTION_PATH, "Source run267BP attribution."),
        ("stage267_run267BQ_source_mt5_execution_result", "source_execution_result", SOURCE_MT5_EXECUTION_RESULT_PATH, "Source run267BO execution result."),
        ("stage267_run267BQ_trade_records", "trade_records", TRADE_RECORDS_PATH, "Run267BQ parsed trade records."),
        ("stage267_run267BQ_time_slice_kpi", "time_slice_kpi", TIME_SLICE_KPI_PATH, "Run267BQ time-slice KPI."),
        ("stage267_run267BQ_curve_diagnostics", "curve_diagnostics", CURVE_DIAGNOSTICS_PATH, "Run267BQ curve diagnostics."),
        ("stage267_run267BQ_cross_period_summary", "cross_period_summary", CROSS_PERIOD_SUMMARY_PATH, "Run267BQ cross-period summary."),
        ("stage267_run267BQ_negative_slice_summary", "negative_slice_summary", NEGATIVE_SLICE_PATH, "Run267BQ negative slice summary."),
        ("stage267_run267BQ_parser_checks", "parser_checks", PARSER_CHECKS_PATH, "Run267BQ parser checks."),
        ("stage267_run267BQ_excluded_gap_attempts", "excluded_gap_attempts", EXCLUDED_GAP_ATTEMPTS_PATH, "Run267BQ excluded zero-trade gap attempts."),
        ("stage267_run267BQ_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Run267BQ result judgment."),
        ("stage267_run267BQ_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run267BQ run manifest."),
        ("stage267_run267BQ_lineage", "lineage", LINEAGE_PATH, "Run267BQ lineage."),
        ("stage267_run267BQ_report", "review_report", REPORT_PATH, "User-facing run267BQ report."),
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
    existing = read_csv_rows(ARTIFACT_REGISTRY_PATH)
    replacement_ids = {row["artifact_id"] for row in rows}
    merged = [row for row in existing if row.get("artifact_id") not in replacement_ids]
    merged.extend(rows)
    write_csv(ARTIFACT_REGISTRY_PATH, merged, ARTIFACT_COLUMNS)


def result_markdown(result: Mapping[str, Any]) -> str:
    summary = result["cross_period_summary"]
    negative = result["negative_slices"][:12]
    excluded = result["excluded_gap_attempts"]
    lines = [
        "# Stage267 run267BQ Anti-overconstraint Cross-period Balance/Time-slice/Trade-quality Review(과제약 제거 확장 기간 잔액/시간구간/거래품질 검토)",
        "",
        "## Summary(요약)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- source_gap_run(원천 공백 실행): `{PARENT_RUN_ID}`",
        f"- source_mt5_run(원천 MT5 실행): `{SOURCE_MT5_RUN_ID}`",
        f"- status(상태): `{STATUS}`",
        f"- trade_records(거래 기록): `{result['trade_record_count']}`",
        f"- time_slice_rows(시간 구간 행): `{result['time_slice_row_count']}`",
        f"- negative_slices(음수 구간): `{result['negative_slice_count']}`",
        "- selected_candidate(선택 후보): `none`",
        "- selected_research_baseline(선택 연구 기준선): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "Action(행동): run267BP(267BP 실행)에서 usable(사용 가능)로 분류된 anti_overconstraint_prune(과제약 제거) 3개 기간을 trade list(거래 목록)로 다시 읽었다.",
        "Effect(효과): 2023H2의 강한 headline KPI(겉 핵심 성과 지표)가 2025H1/2025H2에서도 덜 깨지는지 월/요일/시간/세션/방향/초중후반 구간으로 확인한다.",
        "",
        "## Cross-period Summary(확장 기간 요약)",
        "",
        "| period(기간) | trades(거래) | net(순수익) | PF(수익 팩터) | expectancy(기대값) | closed DD%(폐쇄 손실폭 %) | worst month(최악 월) | read(판독) |",
        "| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for row in summary:
        lines.append(
            "| `{period}` | {trades} | {net} | {pf} | {exp} | {dd} | `{worst}` {worst_net} | `{read}` |".format(
                period=row.get("target_period", ""),
                trades=cell(row.get("trade_count")),
                net=cell(row.get("net_profit")),
                pf=cell(row.get("profit_factor")),
                exp=cell(row.get("expectancy")),
                dd=cell(row.get("closed_balance_max_drawdown_percent")),
                worst=row.get("worst_month", ""),
                worst_net=cell(row.get("worst_month_net")),
                read=row.get("curve_read", ""),
            )
        )
    lines.extend(
        [
            "",
            "## Worst Negative Slices(최악 음수 구간)",
            "",
            "| period(기간) | axis(축) | bucket(구간) | trades(거래) | net(순수익) | DD%(손실폭 %) |",
            "| --- | --- | --- | ---: | ---: | ---: |",
        ]
    )
    for row in negative:
        lines.append(
            "| `{period}` | `{axis}` | `{bucket}` | {trades} | {net} | {dd} |".format(
                period=row.get("target_period", ""),
                axis=row.get("axis", ""),
                bucket=row.get("bucket", ""),
                trades=cell(row.get("trade_count")),
                net=cell(row.get("net_profit")),
                dd=cell(row.get("closed_balance_max_drawdown_percent")),
            )
        )
    if not negative:
        lines.append("| `none` |  |  |  |  |  |")
    lines.extend(
        [
            "",
            "## Excluded Gap Attempts(제외 공백 시도)",
            "",
            "| attempt(시도) | variant(변형) | period(기간) | reason(이유) |",
            "| --- | --- | --- | --- |",
        ]
    )
    for row in excluded:
        lines.append(
            "| `{attempt}` | `{variant}` | `{period}` | `{reason}` |".format(
                attempt=row.get("attempt_name", ""),
                variant=row.get("variant_id", ""),
                period=row.get("target_period", ""),
                reason=row.get("classification", ""),
            )
        )
    if not excluded:
        lines.append("| `none` |  |  |  |")
    lines.extend(
        [
            "",
            "## Boundary(경계)",
            "",
            "- 이 실행은 balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질) 진단이다.",
            "- 2023H2가 좋아도 2025H1/2025H2 약화와 음수 구간을 숨기지 않는다.",
            "- candidate selection(후보 선택), selected research baseline(선택 연구 기준선), ONNX conversion(ONNX 변환), Goal Achieve(목표 달성)는 주장하지 않는다.",
            "",
            "## Artifacts(산출물)",
            "",
            f"- trade_records(거래 기록): `{rel(TRADE_RECORDS_PATH)}`",
            f"- time_slice_kpi(시간 구간 KPI): `{rel(TIME_SLICE_KPI_PATH)}`",
            f"- curve_diagnostics(곡선 진단): `{rel(CURVE_DIAGNOSTICS_PATH)}`",
            f"- cross_period_summary(확장 기간 요약): `{rel(CROSS_PERIOD_SUMMARY_PATH)}`",
            f"- negative_slice_summary(음수 구간 요약): `{rel(NEGATIVE_SLICE_PATH)}`",
            f"- next_action(다음 행동): `{NEXT_ACTION}`",
        ]
    )
    return "\n".join(lines)


def run() -> dict[str, Any]:
    created_at = utc_now()
    gap_rows = read_csv(SOURCE_GAP_CLASSIFICATION_PATH)
    execution_result = read_json(SOURCE_MT5_EXECUTION_RESULT_PATH)
    trade_rows, parser_checks = build_trade_records(gap_rows, execution_result)
    time_rows = build_time_slice_rows(trade_rows)
    curve_rows = build_curve_rows(trade_rows, time_rows, execution_result)
    summary_rows = build_cross_period_summary(curve_rows)
    negative_rows = negative_slices(time_rows)
    excluded_rows = [row for row in gap_rows if row.get("classification") != "completed_runtime_kpi"]
    judgment_rows = result_judgment_rows(summary_rows, negative_rows)
    result = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_mt5_run_id": SOURCE_MT5_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "trade_record_count": len(trade_rows),
        "time_slice_row_count": len(time_rows),
        "curve_row_count": len(curve_rows),
        "negative_slice_count": len(negative_rows),
        "excluded_gap_attempt_count": len(excluded_rows),
        "cross_period_summary": summary_rows,
        "negative_slices": negative_rows,
        "excluded_gap_attempts": excluded_rows,
        "parser_checks": parser_checks,
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "sources": {
            "gap_classification": rel(SOURCE_GAP_CLASSIFICATION_PATH),
            "performance_attribution": rel(SOURCE_PERFORMANCE_ATTRIBUTION_PATH),
            "forensic_gap_receipt": rel(SOURCE_FORENSIC_GAP_RECEIPT_PATH),
            "mt5_execution_result": rel(SOURCE_MT5_EXECUTION_RESULT_PATH),
            "mt5_kpi_summary": rel(SOURCE_MT5_KPI_SUMMARY_PATH),
            "mt5_forensics": rel(SOURCE_MT5_FORENSICS_PATH),
            "bp_report": rel(SOURCE_BP_REPORT_PATH),
        },
        "outputs": {
            "trade_records": rel(TRADE_RECORDS_PATH),
            "time_slice_kpi": rel(TIME_SLICE_KPI_PATH),
            "curve_diagnostics": rel(CURVE_DIAGNOSTICS_PATH),
            "cross_period_summary": rel(CROSS_PERIOD_SUMMARY_PATH),
            "negative_slice_summary": rel(NEGATIVE_SLICE_PATH),
            "parser_checks": rel(PARSER_CHECKS_PATH),
            "excluded_gap_attempts": rel(EXCLUDED_GAP_ATTEMPTS_PATH),
            "result_judgment": rel(RESULT_JUDGMENT_PATH),
            "run_manifest": rel(RUN_MANIFEST_PATH),
            "lineage": rel(LINEAGE_PATH),
            "report": rel(REPORT_PATH),
        },
    }
    write_csv(
        TRADE_RECORDS_PATH,
        trade_rows,
        (
            "run_id",
            "source_run_id",
            "source_gap_run_id",
            "attempt_name",
            "record_view",
            "queue_id",
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "variant_id",
            "target_period",
            "period_id",
            "source_first_tranche_attempt_name",
            "tier_scope",
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
            "gross_profit",
            "net_profit",
            "commission",
            "swap",
            "source_report_path",
        ),
    )
    write_csv(
        TIME_SLICE_KPI_PATH,
        time_rows,
        (
            "record_view",
            "attempt_name",
            "tier_scope",
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "variant_id",
            "target_period",
            "period_id",
            "route_role",
            "axis",
            "bucket",
            *METRIC_COLUMNS,
            "min_closed_balance",
            "slice_read",
        ),
    )
    write_csv(
        CURVE_DIAGNOSTICS_PATH,
        curve_rows,
        (
            "record_view",
            "attempt_name",
            "tier_scope",
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "variant_id",
            "target_period",
            "period_id",
            "route_role",
            *METRIC_COLUMNS,
            "min_closed_balance",
            "report_equity_drawdown_percent",
            "report_balance_drawdown_percent",
            "report_drawdown_percent",
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
            "decision_read",
        ),
    )
    write_csv(CROSS_PERIOD_SUMMARY_PATH, summary_rows, tuple(summary_rows[0].keys()) if summary_rows else ("status",))
    write_csv(NEGATIVE_SLICE_PATH, negative_rows, tuple(negative_rows[0].keys()) if negative_rows else ("status",))
    write_csv(PARSER_CHECKS_PATH, parser_checks, tuple(parser_checks[0].keys()) if parser_checks else ("status",))
    write_csv(EXCLUDED_GAP_ATTEMPTS_PATH, excluded_rows, tuple(excluded_rows[0].keys()) if excluded_rows else ("status",))
    write_csv(RESULT_JUDGMENT_PATH, judgment_rows, ("field", "value", "judgment", "evidence"))
    write_json(RUN_MANIFEST_PATH, result)
    write_json(
        LINEAGE_PATH,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "source_mt5_run_id": SOURCE_MT5_RUN_ID,
            "sources": result["sources"],
            "outputs": result["outputs"],
            "lineage_judgment": "connected_with_trade_list_curve_timeslice_boundary",
        },
    )
    write_md(REPORT_PATH, result_markdown(result))
    update_ledgers_and_artifacts(created_at, result)
    update_current_truth_docs(result)
    return result


def main() -> int:
    result = run()
    print(
        json.dumps(
            {
                "status": result["status"],
                "trade_records": result["trade_record_count"],
                "time_slice_rows": result["time_slice_row_count"],
                "curve_rows": result["curve_row_count"],
                "negative_slices": result["negative_slice_count"],
                "excluded_gap_attempts": result["excluded_gap_attempt_count"],
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
