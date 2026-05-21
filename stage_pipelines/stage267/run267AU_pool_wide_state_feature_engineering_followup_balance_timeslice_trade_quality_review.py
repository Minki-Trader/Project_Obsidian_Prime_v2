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
from stage_pipelines.stage267 import run267AS_pool_wide_state_feature_engineering_followup_materialization as materializer
from stage_pipelines.stage267 import run267AT_pool_wide_state_feature_engineering_followup_mt5_executor as source_executor


STAGE_ID = source_executor.STAGE_ID
RUN_NUMBER = "run267AU"
RUN_ID = "run267AU_stage267_pool_wide_state_feature_engineering_followup_balance_timeslice_trade_quality_review_v1"
PARENT_RUN_ID = source_executor.RUN_ID
SOURCE_MATERIALIZATION_RUN_ID = materializer.RUN_ID
STATUS = "run267AU_pool_wide_state_feature_engineering_followup_balance_timeslice_trade_quality_review_completed"
PARTIAL_STATUS = "run267AU_pool_wide_state_feature_engineering_followup_balance_timeslice_trade_quality_review_partial_parser_errors"
JUDGMENT = "diagnostic_curve_timeslice_trade_quality_review_completed_no_candidate_selection"
PARTIAL_JUDGMENT = "diagnostic_review_partial_parser_errors_no_candidate_selection"
CLAIM_BOUNDARY = source_executor.CLAIM_BOUNDARY
NEXT_ACTION = "run267AV_design_pool_wide_state_feature_engineering_followup_or_adapter_branch_from_run267AU_review"
NEXT_ACTION_PARTIAL = "run267AU_repair_pool_wide_state_feature_engineering_followup_trade_report_parser_errors"

STAGE_ROOT = source_executor.STAGE_ROOT
REVIEWS_ROOT = source_executor.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "pool_wide_state_feature_engineering_followup_balance_timeslice_trade_quality_review"

SOURCE_EXECUTION_RESULT_PATH = source_executor.EXECUTION_RESULT_PATH
SOURCE_KPI_SUMMARY_PATH = source_executor.KPI_SUMMARY_PATH
SOURCE_FORENSICS_PATH = source_executor.FORENSICS_PATH
SOURCE_EXECUTED_ATTEMPTS_PATH = source_executor.EXECUTED_ATTEMPTS_PATH
SOURCE_VARIANT_MANIFEST_PATH = source_executor.SOURCE_VARIANT_MANIFEST_PATH
SOURCE_RUNTIME_CONTRACT_PATH = source_executor.SOURCE_RUNTIME_CONTRACT_PATH
SOURCE_EXECUTION_REPORT_PATH = source_executor.REPORT_PATH
BASE_KPI_PATH = STAGE_ROOT / "02_runs" / "run267B" / "historical_2024" / "mt5_kpi_summary.csv"
BASE_CURVE_PATH = STAGE_ROOT / "02_runs" / "run267B" / "historical_2024" / "balance_curve_diagnostics.csv"

TRADE_RECORDS_PATH = RUN_ROOT / "trade_records.csv"
TIME_SLICE_KPI_PATH = RUN_ROOT / "time_slice_kpi.csv"
CURVE_DIAGNOSTICS_PATH = RUN_ROOT / "curve_diagnostics.csv"
CANDIDATE_FOLLOWUP_REVIEW_PATH = RUN_ROOT / "candidate_followup_profile_review.csv"
CANDIDATE_SUMMARY_PATH = RUN_ROOT / "candidate_balance_timeslice_summary.csv"
FOLLOWUP_PROFILE_SUMMARY_PATH = RUN_ROOT / "followup_profile_balance_timeslice_summary.csv"
NEGATIVE_SLICE_PATH = RUN_ROOT / "negative_slice_summary.csv"
TIER_DUPLICATE_REVIEW_PATH = RUN_ROOT / "tier_duplicate_review.csv"
PARSER_CHECKS_PATH = RUN_ROOT / "parser_checks.csv"
PARSER_ERRORS_PATH = RUN_ROOT / "parser_errors.csv"
REVIEW_RESULT_PATH = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267AU_pool_wide_state_feature_engineering_followup_balance_timeslice_trade_quality_review.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267AU_pool_wide_state_feature_engineering_followup_balance_timeslice_trade_quality_review.py")

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
CANDIDATE_ORDER = ("s264_aih", "s264_lc", "s262_lih", "s264_aia", "s258_stc")


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
        return "thin_slice(얇은 구간)"
    if net <= -160.0 or dd_pct >= 30.0:
        return "deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)"
    if net < -80.0:
        return "negative_fragile_slice(음수 취약 구간)"
    if net < 0.0:
        return "minor_negative_slice(작은 음수 구간)"
    return "measured_slice(측정 구간)"


def curve_read(item: Mapping[str, Any], report_metrics: Mapping[str, Any], month_rows: Sequence[Mapping[str, Any]]) -> str:
    equity_dd = as_float(report_metrics.get("equity_drawdown_maximal_percent") or item.get("closed_balance_max_drawdown_percent"))
    pf = as_float(item.get("profit_factor"))
    net = as_float(item.get("net_profit"))
    trades = as_int(item.get("trade_count"))
    negative_months = [row for row in month_rows if as_float(row.get("net_profit")) < 0.0]
    worst_month_net = min((as_float(row.get("net_profit")) for row in month_rows), default=0.0)
    positive_month_ratio = (len(month_rows) - len(negative_months)) / len(month_rows) if month_rows else 0.0
    if net <= 0.0 or pf <= 1.0:
        return "fragile_or_negative_no_extension(취약 또는 음수, 확장 금지)"
    if equity_dd >= 24.0 or worst_month_net <= -180.0:
        return "headline_good_but_hole_uncomfortable(대표 숫자는 좋지만 구멍 불편)"
    if trades >= 285 and net >= 1000.0 and pf >= 1.55 and equity_dd <= 19.0 and positive_month_ratio >= 0.58:
        return "constructive_curve_watch_not_selection(건설적 곡선 관찰, 선택 아님)"
    if trades >= 260 and net >= 800.0 and pf >= 1.40 and equity_dd < 24.0:
        return "mixed_constructive_needs_more_pressure(혼합 건설적, 추가 압박 필요)"
    return "mixed_or_fragile(혼합 또는 취약)"


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
        except Exception as exc:  # pragma: no cover - persisted as run evidence.
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
            rows.append(
                {
                    "run_id": RUN_ID,
                    "source_run_id": PARENT_RUN_ID,
                    "queue_id": attempt.get("queue_id"),
                    "candidate_id": attempt.get("candidate_id"),
                    "candidate_alias": attempt.get("candidate_alias"),
                    "candidate_role": attempt.get("candidate_role"),
                    "source_test_id": attempt.get("source_test_id"),
                    "source_queue_id": attempt.get("source_queue_id"),
                    "state_profile": attempt.get("state_profile"),
                    "followup_profile": attempt.get("followup_profile"),
                    "pressure_group": attempt.get("pressure_group"),
                    "model_materialization_type": attempt.get("model_materialization_type"),
                    "materialization_boundary": "pool_wide_state_feature_engineering_followup_pressure_not_retrained",
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
            "tier_scope",
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "source_test_id",
            "source_queue_id",
            "state_profile",
            "followup_profile",
            "pressure_group",
            "materialization_boundary",
            "route_role",
            axis,
        )
        for key, rows in group_rows(trade_rows, keys).items():
            (
                record_view,
                tier_scope,
                candidate_id,
                alias,
                role,
                test_id,
                source_queue_id,
                state_profile,
                followup_profile,
                pressure_group,
                boundary,
                route_role,
                bucket,
            ) = key
            item = metrics(rows)
            output.append(
                {
                    "record_view": record_view,
                    "tier_scope": tier_scope,
                    "candidate_id": candidate_id,
                    "candidate_alias": alias,
                    "candidate_role": role,
                    "source_test_id": test_id,
                    "source_queue_id": source_queue_id,
                    "state_profile": state_profile,
                    "followup_profile": followup_profile,
                    "pressure_group": pressure_group,
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
        "source_test_id",
        "source_queue_id",
        "state_profile",
        "followup_profile",
        "pressure_group",
        "materialization_boundary",
        "route_role",
    )
    for key, rows in group_rows(trade_rows, keys).items():
        (
            record_view,
            tier_scope,
            candidate_id,
            alias,
            role,
            test_id,
            source_queue_id,
            state_profile,
            followup_profile,
            pressure_group,
            boundary,
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
        output.append(
            {
                "record_view": record_view,
                "tier_scope": tier_scope,
                "candidate_id": candidate_id,
                "candidate_alias": alias,
                "candidate_role": role,
                "source_test_id": test_id,
                "source_queue_id": source_queue_id,
                "state_profile": state_profile,
                "followup_profile": followup_profile,
                "pressure_group": pressure_group,
                "materialization_boundary": boundary,
                "route_role": route_role,
                **item,
                "report_equity_drawdown_percent": as_float(report_metrics.get("equity_drawdown_maximal_percent")),
                "report_balance_drawdown_percent": as_float(report_metrics.get("balance_drawdown_maximal_percent")),
                "report_recovery_factor": as_float(report_metrics.get("recovery_factor")),
                "tier_b_fallback_used_count": as_int(report_metrics.get("tier_b_fallback_used_count")),
                "tier_b_fallback_order_fill_count": as_int(report_metrics.get("tier_b_fallback_order_fill_count")),
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
                "curve_read": curve_read(item, report_metrics, month_slices),
            }
        )
    return output


def base_kpi_by_alias() -> dict[str, Mapping[str, Any]]:
    rows: dict[str, Mapping[str, Any]] = {}
    for row in read_csv(BASE_KPI_PATH):
        if row.get("route_role") not in {"routed_total", "routed_total_duplicate_boundary"}:
            continue
        record_view = str(row.get("record_view", ""))
        for alias in CANDIDATE_ORDER:
            if alias in record_view:
                rows[alias] = row
                break
    return rows


def base_curve_by_alias() -> dict[str, Mapping[str, Any]]:
    rows: dict[str, Mapping[str, Any]] = {}
    for row in read_csv(BASE_CURVE_PATH):
        alias = str(row.get("candidate_alias") or "")
        if alias:
            rows[alias] = row
    return rows


def worst_slice_for(curve_row: Mapping[str, Any], time_rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    related = [
        row
        for row in time_rows
        if row.get("record_view") == curve_row.get("record_view")
        and as_int(row.get("trade_count")) >= 3
        and row.get("axis") in {"month", "weekday", "session_report", "chron_segment"}
    ]
    return min(related, key=lambda row: as_float(row.get("net_profit"))) if related else {}


def fragility_flags(curve: Mapping[str, Any], worst_slice: Mapping[str, Any]) -> str:
    flags: list[str] = []
    if as_float(curve.get("report_equity_drawdown_percent")) >= 20.0:
        flags.append("dd_watch(손실폭 관찰)")
    if as_float(curve.get("worst_month_net")) <= -120.0:
        flags.append("month_hole(월별 구멍)")
    if as_float(worst_slice.get("net_profit")) <= -160.0:
        flags.append("deep_slice_hole(깊은 구간 구멍)")
    if as_int(curve.get("trade_count")) < 280:
        flags.append("trade_count_watch(거래 수 관찰)")
    if as_float(curve.get("profit_factor")) < 1.50:
        flags.append("pf_watch(수익 팩터 관찰)")
    if not flags:
        flags.append("no_major_flag_in_this_review(이번 검토 주요 경고 없음)")
    return ";".join(flags)


def decision_read(curve: Mapping[str, Any], worst_slice: Mapping[str, Any]) -> str:
    read = str(curve.get("curve_read"))
    flags = fragility_flags(curve, worst_slice)
    if "hole" in flags:
        return "headline_or_mixed_with_slice_hole_no_selection"
    if read == "constructive_curve_watch_not_selection":
        return "constructive_followup_watch_no_selection"
    if read == "mixed_constructive_needs_more_pressure":
        return "mixed_constructive_needs_wider_pressure"
    return "diagnostic_only_or_prune_pressure"


def build_candidate_followup_review(
    curve_rows: Sequence[Mapping[str, Any]],
    time_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    base_kpi = base_kpi_by_alias()
    base_curve = base_curve_by_alias()
    output: list[dict[str, Any]] = []
    for curve in curve_rows:
        if curve.get("tier_scope") != "Tier A":
            continue
        alias = str(curve.get("candidate_alias"))
        worst = worst_slice_for(curve, time_rows)
        base = base_kpi.get(alias, {})
        base_curve_row = base_curve.get(alias, {})
        output.append(
            {
                "candidate_id": curve.get("candidate_id"),
                "candidate_alias": alias,
                "candidate_role": curve.get("candidate_role"),
                "source_test_id": curve.get("source_test_id"),
                "source_queue_id": curve.get("source_queue_id"),
                "state_profile": curve.get("state_profile"),
                "followup_profile": curve.get("followup_profile"),
                "pressure_group": curve.get("pressure_group"),
                "record_view": curve.get("record_view"),
                "net_profit": curve.get("net_profit"),
                "base_2024_net_profit": base.get("net_profit", ""),
                "net_delta_vs_base_2024": as_float(curve.get("net_profit")) - as_float(base.get("net_profit")),
                "profit_factor": curve.get("profit_factor"),
                "base_2024_profit_factor": base.get("profit_factor", ""),
                "pf_delta_vs_base_2024": as_float(curve.get("profit_factor")) - as_float(base.get("profit_factor")),
                "trade_count": curve.get("trade_count"),
                "base_2024_trade_count": base.get("trade_count", ""),
                "trade_delta_vs_base_2024": as_float(curve.get("trade_count")) - as_float(base.get("trade_count")),
                "expectancy": curve.get("expectancy"),
                "report_equity_drawdown_percent": curve.get("report_equity_drawdown_percent"),
                "base_2024_max_drawdown_percent": base.get("max_drawdown_percent", ""),
                "dd_delta_vs_base_2024": as_float(curve.get("report_equity_drawdown_percent")) - as_float(base.get("max_drawdown_percent")),
                "recovery_factor": curve.get("report_recovery_factor"),
                "base_2024_recovery_factor": base.get("recovery_factor", ""),
                "positive_month_ratio": curve.get("positive_month_ratio"),
                "negative_month_count": curve.get("negative_month_count"),
                "worst_month": curve.get("worst_month"),
                "worst_month_net": curve.get("worst_month_net"),
                "best_month": curve.get("best_month"),
                "best_month_net": curve.get("best_month_net"),
                "chron_early_net": curve.get("chron_early_net"),
                "chron_mid_net": curve.get("chron_mid_net"),
                "chron_late_net": curve.get("chron_late_net"),
                "worst_slice_axis": worst.get("axis", ""),
                "worst_slice_bucket": worst.get("bucket", ""),
                "worst_slice_net": worst.get("net_profit", ""),
                "worst_slice_trade_count": worst.get("trade_count", ""),
                "base_curve_grade": base_curve_row.get("curve_grade", ""),
                "base_curve_read": base_curve_row.get("curve_read", ""),
                "source_chart_path": curve.get("source_chart_path"),
                "fragility_flags": fragility_flags(curve, worst),
                "curve_read": curve.get("curve_read"),
                "decision_read": decision_read(curve, worst),
                "selection_boundary": "not_candidate_selection(후보 선택 아님)",
            }
        )
    return sorted(
        output,
        key=lambda row: (
            0 if row.get("decision_read") == "constructive_followup_watch_no_selection" else 1,
            1 if "hole" in str(row.get("fragility_flags")) else 0,
            -as_float(row.get("net_profit")),
            as_float(row.get("report_equity_drawdown_percent")),
        ),
    )


def build_candidate_summary(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for (candidate_id, alias, role), grouped in group_rows(rows, ("candidate_id", "candidate_alias", "candidate_role")).items():
        constructive = [row for row in grouped if row.get("decision_read") == "constructive_followup_watch_no_selection"]
        mixed = [row for row in grouped if row.get("decision_read") == "mixed_constructive_needs_wider_pressure"]
        holes = [row for row in grouped if "hole" in str(row.get("fragility_flags"))]
        net_values = [as_float(row.get("net_profit")) for row in grouped]
        dd_values = [as_float(row.get("report_equity_drawdown_percent")) for row in grouped]
        worst_months = [as_float(row.get("worst_month_net")) for row in grouped]
        if constructive and not holes:
            summary_read = "candidate_followup_watch_no_selection(후보 후속 관찰, 선택 아님)"
        elif constructive or mixed:
            summary_read = "candidate_mixed_watch_needs_wider_pressure(혼합 관찰, 더 넓은 압박 필요)"
        elif holes:
            summary_read = "candidate_has_slice_holes_no_selection(구간 구멍 있음, 선택 아님)"
        else:
            summary_read = "candidate_diagnostic_or_prune_pressure(진단 또는 가지치기 압박)"
        output.append(
            {
                "candidate_id": candidate_id,
                "candidate_alias": alias,
                "candidate_role": role,
                "tier_a_test_count": len(grouped),
                "constructive_watch_count": len(constructive),
                "mixed_watch_count": len(mixed),
                "slice_hole_flag_count": len(holes),
                "net_profit_mean": mean(net_values) if net_values else None,
                "net_profit_min": min(net_values) if net_values else None,
                "net_profit_max": max(net_values) if net_values else None,
                "equity_drawdown_percent_worst": max(dd_values) if dd_values else None,
                "worst_month_net_min": min(worst_months) if worst_months else None,
                "summary_read": summary_read,
            }
        )
    return sorted(output, key=lambda row: (-as_int(row.get("constructive_watch_count")), -as_float(row.get("net_profit_mean"))))


def build_followup_profile_summary(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for (profile, pressure_group), grouped in group_rows(rows, ("followup_profile", "pressure_group")).items():
        net_values = [as_float(row.get("net_profit")) for row in grouped]
        dd_values = [as_float(row.get("report_equity_drawdown_percent")) for row in grouped]
        holes = [row for row in grouped if "hole" in str(row.get("fragility_flags"))]
        constructive = [row for row in grouped if row.get("decision_read") == "constructive_followup_watch_no_selection"]
        best = max(grouped, key=lambda row: as_float(row.get("net_profit")))
        output.append(
            {
                "followup_profile": profile,
                "pressure_group": pressure_group,
                "candidate_count": len({row.get("candidate_alias") for row in grouped}),
                "test_count": len(grouped),
                "constructive_watch_count": len(constructive),
                "slice_hole_flag_count": len(holes),
                "net_profit_mean": mean(net_values) if net_values else None,
                "net_profit_min": min(net_values) if net_values else None,
                "net_profit_max": max(net_values) if net_values else None,
                "equity_drawdown_percent_worst": max(dd_values) if dd_values else None,
                "best_candidate_alias": best.get("candidate_alias"),
                "best_net_profit": best.get("net_profit"),
                "profile_read": "profile_watch_no_selection(프로필 관찰, 선택 아님)" if constructive and not holes else "profile_needs_pressure_or_prune(압박 또는 가지치기 필요)",
            }
        )
    return sorted(output, key=lambda row: (-as_int(row.get("constructive_watch_count")), -as_float(row.get("net_profit_mean"))))


def negative_slices(time_rows: Sequence[Mapping[str, Any]], limit: int = 120) -> list[dict[str, Any]]:
    rows = [
        dict(row)
        for row in time_rows
        if row.get("tier_scope") == "Tier A" and as_float(row.get("net_profit")) < 0.0 and as_int(row.get("trade_count")) >= 3
    ]
    return sorted(rows, key=lambda row: (as_float(row.get("net_profit")), -as_int(row.get("trade_count"))))[:limit]


def build_tier_duplicate_review(curve_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    grouped = group_rows(curve_rows, ("candidate_alias", "state_profile", "followup_profile"))
    for (alias, state_profile, followup_profile), rows in sorted(grouped.items()):
        tier_a = next((row for row in rows if row.get("tier_scope") == "Tier A"), None)
        routed = next((row for row in rows if row.get("tier_scope") == "Tier A+B"), None)
        if not tier_a or not routed:
            output.append(
                {
                    "candidate_alias": alias,
                    "state_profile": state_profile,
                    "followup_profile": followup_profile,
                    "tier_pair_present": False,
                    "net_profit_delta_tier_ab_minus_tier_a": "",
                    "trade_count_delta_tier_ab_minus_tier_a": "",
                    "fallback_used_count": "",
                    "audit_status": "missing_pair(쌍 누락)",
                    "interpretation": "inspect_pair(쌍 확인 필요)",
                }
            )
            continue
        net_delta = as_float(routed.get("net_profit")) - as_float(tier_a.get("net_profit"))
        trade_delta = as_int(routed.get("trade_count")) - as_int(tier_a.get("trade_count"))
        fallback_used = as_int(routed.get("tier_b_fallback_used_count"))
        duplicate = abs(net_delta) < 1e-9 and trade_delta == 0 and fallback_used == 0
        output.append(
            {
                "candidate_alias": alias,
                "state_profile": state_profile,
                "followup_profile": followup_profile,
                "tier_pair_present": True,
                "tier_a_record_view": tier_a.get("record_view"),
                "routed_record_view": routed.get("record_view"),
                "net_profit_delta_tier_ab_minus_tier_a": net_delta,
                "trade_count_delta_tier_ab_minus_tier_a": trade_delta,
                "fallback_used_count": fallback_used,
                "audit_status": "duplicate_boundary_confirmed(중복 경계 확인)" if duplicate else "tier_pair_differs(티어 쌍 차이)",
                "interpretation": "not_routed_fallback_evidence(라우팅 대체 근거 아님)" if duplicate else "inspect_pair(쌍 확인 필요)",
            }
        )
    return output


def forensics_summary(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    statuses = sorted({str(row.get("tester_status")) for row in rows if row.get("tester_status")})
    report_statuses = sorted({str(row.get("report_status")) for row in rows if row.get("report_status")})
    return {
        "row_count": len(rows),
        "terminal_count": len({str(row.get("terminal")) for row in rows if row.get("terminal")}),
        "tester_statuses": statuses,
        "report_statuses": report_statuses,
        "symbols": sorted({str(row.get("symbol")) for row in rows if row.get("symbol")}),
        "timeframes": sorted({str(row.get("timeframe")) for row in rows if row.get("timeframe")}),
        "deposits": sorted({str(row.get("deposit")) for row in rows if row.get("deposit")}),
        "leverages": sorted({str(row.get("leverage")) for row in rows if row.get("leverage")}),
        "models": sorted({str(row.get("model")) for row in rows if row.get("model")}),
        "from_dates": sorted({str(row.get("from_date")) for row in rows if row.get("from_date")}),
        "to_dates": sorted({str(row.get("to_date")) for row in rows if row.get("to_date")}),
        "cost_assumption_boundary": "MT5 tester broker-history costs; no separate cost authority claimed(MT5 테스터 브로커 이력 비용 조건, 별도 비용 권위 주장 없음)",
        "backtest_judgment": "usable_with_boundary(경계부 사용 가능)" if rows and statuses == ["completed"] and report_statuses == ["completed"] else "inconclusive(불충분)",
    }


def result_status(parser_errors: Sequence[Mapping[str, Any]], parser_checks: Sequence[Mapping[str, Any]]) -> str:
    mismatches = [row for row in parser_checks if row.get("parser_status") != "matched"]
    return PARTIAL_STATUS if parser_errors or mismatches else STATUS


def result_judgment(status: str) -> str:
    return JUDGMENT if status == STATUS else PARTIAL_JUDGMENT


def result_next_action(status: str) -> str:
    return NEXT_ACTION if status == STATUS else NEXT_ACTION_PARTIAL


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


def update_workspace_state_text(text: str, result: Mapping[str, Any]) -> str:
    status = str(result["status"])
    next_action = str(result["next_action"])
    path_key = "run267AU_pool_wide_state_feature_engineering_followup_balance_timeslice_trade_quality_review_report_path"
    lines = text.splitlines()
    output: list[str] = []
    in_stage267 = False
    inserted_path = path_key in text
    focus_inserted = False
    focus_block = [
        "- >-",
        f"  Stage267(267단계) run267AU(267AU 실행) pool-wide state feature engineering follow-up balance/time-slice/trade-quality review(후보군 전체 상태 피처 엔지니어링 후속 잔액/시간구간/거래품질 검토) `{status}`. Effect(효과): run267AT(267AT 실행)의 16개 MT5(MetaTrader 5, 메타트레이더5) 보고서를 거래 단위로 다시 읽어 curve(곡선), weak slice(약한 구간), trade quality(거래 품질) 판단을 만들었고 selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.",
    ]
    for line in lines:
        if line.startswith("current_run_id:"):
            output.append(f"current_run_id: {RUN_ID}")
            continue
        if line == "current_focus:" and not focus_inserted:
            output.append(line)
            output.extend(focus_block)
            focus_inserted = True
            continue
        if line.startswith("stage267_baseline_candidate_racing_protocol:"):
            in_stage267 = True
            output.append(line)
            continue
        if in_stage267 and line and not line.startswith(" ") and not line.startswith("#"):
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
                output.append(f"  next_action: {next_action}")
                continue
            if "run267AT_pool_wide_state_feature_engineering_followup_mt5_execution_report_path" in stripped and not inserted_path:
                output.append(line)
                output.append(f"  {path_key}: {rel(REPORT_PATH)}")
                inserted_path = True
                continue
        output.append(line)
    if in_stage267 and not inserted_path:
        output.append(f"  {path_key}: {rel(REPORT_PATH)}")
    return "\n".join(output) + "\n"


def update_current_truth_docs(result: Mapping[str, Any]) -> None:
    status = str(result["status"])
    next_action = str(result["next_action"])
    report_line = f"- run267AU_pool_wide_state_feature_engineering_followup_balance_timeslice_trade_quality_review(267AU 후보군 전체 상태 피처 엔지니어링 후속 잔액/시간구간/거래품질 검토): `{rel(REPORT_PATH)}`"
    latest_line = (
        f"- latest_mt5_review(최신 MT5 검토): run267AU(267AU 실행) trade records(거래 기록) `{result['trade_record_count']}`, "
        f"candidate-followup rows(후보-후속 행) `{len(result['candidate_followup_review'])}`, "
        f"watch rows(관찰 행) `{result['watch_rows']}`, negative Tier A slices(음수 Tier A 구간) `{len(result['negative_slices'])}`, "
        f"report(보고서) `{rel(REPORT_PATH)}`."
    )
    closing_block = "\n".join(
        [
            "Run267AU(267AU 실행)는 run267AT(267AT 실행)의 pool-wide state feature engineering follow-up MT5 reports(후보군 전체 상태 피처 엔지니어링 후속 MT5 보고서)를 거래 단위로 다시 읽었다.",
            "Effect(효과): headline KPI(대표 핵심 성과 지표)만 보지 않고 balance/equity curve(잔액/평가금 곡선), weak slice(약한 구간), trade quality(거래 품질)를 다음 연구 입력으로 고정했다.",
            "Boundary(경계): selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.",
        ]
    )
    for path in (CURRENT_WORKING_STATE_PATH, SELECTION_STATUS_PATH, REVIEW_INDEX_PATH):
        text = io_path(path).read_text(encoding="utf-8-sig")
        if path == CURRENT_WORKING_STATE_PATH:
            text = replace_line_prefix(text, "- status(상태):", f"- status(상태): `{status}`")
            text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{next_action}`")
            text = replace_line_prefix(text, "- next_run(다음 실행):", f"- next_run(다음 실행): `{next_action}`")
            text = replace_line_prefix(text, "- adapter_under_review(검토 중 어댑터):", "- adapter_under_review(검토 중 어댑터): `pool_wide_state_feature_engineering_followup_balance_timeslice_trade_quality_review`")
            text = append_after_contains(text, "stage267_run267AT_pool_wide_state_feature_engineering_followup_mt5_execution.md", report_line)
            text = append_after_contains(text, "## Current Next Action", latest_line)
        else:
            if path == SELECTION_STATUS_PATH:
                text = replace_line_prefix(text, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{status}`")
            if path == REVIEW_INDEX_PATH:
                text = replace_line_prefix(text, "- status(상태):", f"- status(상태): `{status}`")
            text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{next_action}`")
            text = append_after_contains(text, "stage267_run267AT_pool_wide_state_feature_engineering_followup_mt5_execution.md", report_line)
        text = append_block_once(text, "Run267AU(267AU 실행)는 run267AT", closing_block)
        write_md(path, text)
    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    write_md(WORKSPACE_STATE_PATH, update_workspace_state_text(workspace, result))


def update_ledgers(created_at: str, result: Mapping[str, Any]) -> None:
    status = str(result["status"])
    judgment = str(result["judgment"])
    next_action = str(result["next_action"])
    upsert_csv_rows(
        STAGE_LEDGER_PATH,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": "stage267_run267AU_pool_wide_state_feature_engineering_followup_balance_timeslice_trade_quality_review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "pool_wide_state_feature_engineering_followup_balance_timeslice_trade_quality_review",
                "tier_scope": "Tier A primary read plus Tier A+B duplicate boundary",
                "scoreboard": "trade_shape_curve_time_slice_review",
                "status": status,
                "judgment": judgment,
                "evidence_boundary": "diagnostic_curve_timeslice_trade_quality_review_no_candidate_selection_no_onnx",
                "report_path": rel(REPORT_PATH),
                "notes": (
                    f"trade_records={result['trade_record_count']};"
                    f"candidate_followup_rows={len(result['candidate_followup_review'])};"
                    f"negative_slices={len(result['negative_slices'])};"
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
                "lane": "baseline_candidate_racing_pool_wide_state_feature_engineering_followup_balance_timeslice_trade_quality_review",
                "status": status,
                "judgment": judgment,
                "path": rel(REPORT_PATH),
                "notes": (
                    "Run267AU follow-up MT5 curve/time-slice/trade-quality review from run267AT reports; "
                    f"selected_candidate=none; onnx_readiness=not_claimed; goal_achieve=not_claimed; next_action={next_action}."
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
                "ledger_row_id": f"{RUN_ID}__pool_wide_state_feature_engineering_followup_balance_timeslice_trade_quality_review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": "pool_wide_state_feature_engineering_followup_balance_timeslice_trade_quality_review",
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "pool_wide_state_feature_engineering_followup_balance_timeslice_trade_quality_review",
                "tier_scope": "Tier A primary read plus Tier A+B duplicate boundary",
                "kpi_scope": "curve_time_slice_trade_quality_trade_shape_review",
                "scoreboard_lane": "trade_shape_curve_time_slice_review",
                "status": status,
                "judgment": judgment,
                "path": rel(REPORT_PATH),
                "primary_kpi": (
                    f"trade_records={result['trade_record_count']};"
                    f"candidate_followup_rows={len(result['candidate_followup_review'])};"
                    f"watch_rows={result['watch_rows']};negative_slices={len(result['negative_slices'])}"
                ),
                "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
                "external_verification_status": "completed_for_run267AT_mt5_report_review",
                "notes": f"Next action: {next_action}.",
            }
        ],
        key="ledger_row_id",
    )
    entries = (
        ("stage267_run267AU_review_script", "producer_script", PRODUCER_PATH, "Builds run267AU follow-up curve/time-slice/trade-quality review."),
        ("stage267_run267AU_source_execution_result", "source_execution_result", SOURCE_EXECUTION_RESULT_PATH, "Source run267AT execution result."),
        ("stage267_run267AU_source_kpi_summary", "source_kpi_summary", SOURCE_KPI_SUMMARY_PATH, "Source run267AT KPI summary."),
        ("stage267_run267AU_source_forensics", "source_forensics", SOURCE_FORENSICS_PATH, "Source run267AT backtest forensics."),
        ("stage267_run267AU_source_attempts", "source_attempt_manifest", SOURCE_EXECUTED_ATTEMPTS_PATH, "Source run267AT executed attempts."),
        ("stage267_run267AU_trade_records", "trade_records", TRADE_RECORDS_PATH, "Run267AU paired trade records from run267AT reports."),
        ("stage267_run267AU_time_slice_kpi", "time_slice_kpi", TIME_SLICE_KPI_PATH, "Run267AU month/weekday/hour/session/direction/chron-segment KPI."),
        ("stage267_run267AU_curve_diagnostics", "curve_diagnostics", CURVE_DIAGNOSTICS_PATH, "Run267AU closed-balance curve diagnostics."),
        ("stage267_run267AU_candidate_followup_review", "candidate_followup_review", CANDIDATE_FOLLOWUP_REVIEW_PATH, "Run267AU candidate follow-up profile curve and weak-slice review."),
        ("stage267_run267AU_candidate_summary", "candidate_summary", CANDIDATE_SUMMARY_PATH, "Run267AU candidate balance/time-slice summary."),
        ("stage267_run267AU_followup_profile_summary", "followup_profile_summary", FOLLOWUP_PROFILE_SUMMARY_PATH, "Run267AU follow-up profile summary."),
        ("stage267_run267AU_negative_slice_summary", "negative_slice_summary", NEGATIVE_SLICE_PATH, "Run267AU worst negative Tier A slices."),
        ("stage267_run267AU_tier_duplicate_review", "audit_matrix", TIER_DUPLICATE_REVIEW_PATH, "Run267AU Tier A versus Tier A+B duplicate boundary."),
        ("stage267_run267AU_parser_checks", "parser_checks", PARSER_CHECKS_PATH, "Run267AU parser reconciliation checks."),
        ("stage267_run267AU_parser_errors", "parser_errors", PARSER_ERRORS_PATH, "Run267AU parser errors."),
        ("stage267_run267AU_review_result", "review_result", REVIEW_RESULT_PATH, "Run267AU review JSON payload."),
        ("stage267_run267AU_review_report", "review_report", REPORT_PATH, "User-facing run267AU balance/time-slice/trade-quality review."),
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


def top_rows(rows: Sequence[Mapping[str, Any]], limit: int = 12) -> list[Mapping[str, Any]]:
    return list(rows[:limit])


def fmt(value: Any) -> str:
    return f"{as_float(value):.2f}"


def report_markdown(result: Mapping[str, Any]) -> str:
    candidate_rows = result["candidate_followup_review"]
    candidate_summary = result["candidate_summary"]
    profile_summary = result["followup_profile_summary"]
    negative = result["negative_slices"][:14]
    forensic = result["forensics_summary"]
    lines = [
        "# Stage267 Run267AU Pool-wide State Feature Engineering Follow-up Balance/Time-Slice/Trade-Quality Review(267단계 267AU 후보군 전체 상태 피처 엔지니어링 후속 잔액/시간구간/거래품질 검토)",
        "",
        f"- action(행동): run267AT(267AT 실행)의 `{len(result['parser_checks'])}`개 MT5(MetaTrader 5, 메타트레이더5) report(보고서)를 trade list(거래 목록) 단위로 다시 읽었다.",
        "- effect(효과): headline KPI(대표 핵심 성과 지표)만 보지 않고 balance/equity curve(잔액/평가금 곡선), weak slice(약한 구간), trade quality(거래 품질)를 같이 본다.",
        f"- status(상태): `{result['status']}`",
        f"- judgment(판정): `{result['judgment']}`",
        f"- trade_records(거래 기록): `{result['trade_record_count']}`",
        f"- candidate_followup_rows(후보-후속 행): `{len(candidate_rows)}`",
        f"- watch_rows(관찰 행): `{result['watch_rows']}`",
        f"- negative_tier_a_slices(음수 Tier A 구간): `{len(result['negative_slices'])}`",
        f"- parser_errors(파서 오류): `{len(result['parser_errors'])}`",
        "- selected_candidate(선택 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Easy Read(쉬운 설명)",
        "",
        "run267AT(267AT 실행)의 숫자는 전체적으로 좋아 보인다. 하지만 이 단계의 질문은 '누가 제일 큰 숫자인가'가 아니다.",
        "Effect(효과): 후보별로 어느 월, 어느 요일, 어느 세션, 어느 순서 구간에서 깨지는지 확인해서 다음 run267AV(267AV 실행)의 설계 재료로 쓴다.",
        "",
        "Tier A+B(Tier A+B 합산)는 이번에도 duplicate boundary(중복 경계)다.",
        "Effect(효과): 실제 fallback routing(대체 라우팅) 강건성으로 과장하지 않고, Tier A(티어 A) 결과가 반복됐는지 확인하는 감사 근거로만 둔다.",
        "",
        "## Candidate Follow-up Watchlist(후보 후속 관찰 목록)",
        "",
        "| rank(순위) | candidate(후보) | role(역할) | followup_profile(후속 프로필) | net profit(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭) | worst month(최악 월) | worst slice(최악 구간) | read(판독) |",
        "| ---: | --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- | --- |",
    ]
    for index, row in enumerate(top_rows(candidate_rows), start=1):
        lines.append(
            f"| {index} | `{row.get('candidate_alias')}` | `{row.get('candidate_role')}` | `{row.get('followup_profile')}` | "
            f"{fmt(row.get('net_profit'))} | {fmt(row.get('profit_factor'))} | {as_int(row.get('trade_count'))} | "
            f"{fmt(row.get('report_equity_drawdown_percent'))} | `{row.get('worst_month')}` {fmt(row.get('worst_month_net'))} | "
            f"`{row.get('worst_slice_axis')}`/`{row.get('worst_slice_bucket')}` {fmt(row.get('worst_slice_net'))} | `{row.get('decision_read')}` |"
        )
    lines.extend(
        [
            "",
            "## Candidate Summary(후보 요약)",
            "",
            "| candidate(후보) | role(역할) | tests(시험 수) | watch(관찰) | mixed(혼합) | holes(구멍) | net mean(평균 순수익) | net min(최소 순수익) | worst DD%(최악 손실폭) | worst month net(최악 월 순수익) | read(판독) |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for row in candidate_summary:
        lines.append(
            f"| `{row.get('candidate_alias')}` | `{row.get('candidate_role')}` | {as_int(row.get('tier_a_test_count'))} | "
            f"{as_int(row.get('constructive_watch_count'))} | {as_int(row.get('mixed_watch_count'))} | "
            f"{as_int(row.get('slice_hole_flag_count'))} | {fmt(row.get('net_profit_mean'))} | {fmt(row.get('net_profit_min'))} | "
            f"{fmt(row.get('equity_drawdown_percent_worst'))} | {fmt(row.get('worst_month_net_min'))} | `{row.get('summary_read')}` |"
        )
    lines.extend(
        [
            "",
            "## Follow-up Profile Summary(후속 프로필 요약)",
            "",
            "| followup_profile(후속 프로필) | pressure_group(압박 그룹) | candidates(후보 수) | watch(관찰) | holes(구멍) | net mean(평균 순수익) | net min(최소 순수익) | worst DD%(최악 손실폭) | best candidate(최고 후보) | read(판독) |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |",
        ]
    )
    for row in profile_summary:
        lines.append(
            f"| `{row.get('followup_profile')}` | `{row.get('pressure_group')}` | {as_int(row.get('candidate_count'))} | "
            f"{as_int(row.get('constructive_watch_count'))} | {as_int(row.get('slice_hole_flag_count'))} | "
            f"{fmt(row.get('net_profit_mean'))} | {fmt(row.get('net_profit_min'))} | {fmt(row.get('equity_drawdown_percent_worst'))} | "
            f"`{row.get('best_candidate_alias')}` | `{row.get('profile_read')}` |"
        )
    lines.extend(
        [
            "",
            "## Worst Tier A Slices(최악 Tier A 구간)",
            "",
            "| candidate(후보) | followup_profile(후속 프로필) | axis(축) | bucket(구간) | net profit(순수익) | trades(거래 수) | read(판독) |",
            "| --- | --- | --- | --- | ---: | ---: | --- |",
        ]
    )
    for row in negative:
        lines.append(
            f"| `{row.get('candidate_alias')}` | `{row.get('followup_profile')}` | `{row.get('axis')}` | `{row.get('bucket')}` | "
            f"{fmt(row.get('net_profit'))} | {as_int(row.get('trade_count'))} | `{row.get('slice_read')}` |"
        )
    lines.extend(
        [
            "",
            "## Forensics Boundary(포렌식 경계)",
            "",
            f"- tester_identity(테스터 정체성): terminal count(터미널 수) `{forensic['terminal_count']}`, symbol(심볼) `{';'.join(forensic['symbols'])}`, timeframe(시간프레임) `{';'.join(forensic['timeframes'])}`, date range(날짜 범위) `{';'.join(forensic['from_dates'])}` to `{';'.join(forensic['to_dates'])}`.",
            f"- trade_evidence(거래 근거): trade records(거래 기록) `{result['trade_record_count']}`, parser checks(파서 확인) `{len(result['parser_checks'])}`.",
            f"- cost_assumptions(비용 가정): `{forensic['cost_assumption_boundary']}`.",
            f"- backtest_judgment(백테스트 판정): `{forensic['backtest_judgment']}`.",
            "",
            "## Attribution(성과 귀속)",
            "",
            "- observed_change(관찰 변화): run267AS/run267AT(267AS/267AT 실행)의 follow-up pressure(후속 압박) 변형들이 2024 구간에서 양수 KPI(핵심 성과 지표)를 만들었다.",
            "- comparison_baseline(비교 기준): run267B historical 2024(2024 과거 압박) MT5 KPI(MT5 핵심 성과 지표)와 curve diagnostics(곡선 진단).",
            "- likely_drivers(가능 동인): retraining(재학습)이 아니라 state feature score table extension(상태 피처 점수표 확장)과 pressure term(압박 항) 변화다.",
            "- alternative_explanations(대체 설명): 2024 단일 기간 적합, duplicate Tier A+B boundary(중복 Tier A+B 경계), score table(점수표) 확장에 따른 우연 적합 가능성이 남아 있다.",
            "- attribution_confidence(귀속 신뢰도): `medium_for_2024_diagnostic_only(2024 진단 한정 중간)`.",
            "",
            "## Artifact Lineage(산출물 계보)",
            "",
            f"- source_inputs(원천 입력): `{rel(SOURCE_EXECUTION_RESULT_PATH)}`, `{rel(SOURCE_KPI_SUMMARY_PATH)}`, `{rel(SOURCE_FORENSICS_PATH)}`, `{rel(SOURCE_VARIANT_MANIFEST_PATH)}`, `{rel(SOURCE_RUNTIME_CONTRACT_PATH)}`.",
            f"- source_report(원천 보고서): `{rel(SOURCE_EXECUTION_REPORT_PATH)}`.",
            f"- producer(생산자): `{rel(PRODUCER_PATH)}`.",
            f"- consumer(소비자): `{result['next_action']}`.",
            f"- artifact_paths(산출물 경로): `{rel(TRADE_RECORDS_PATH)}`, `{rel(TIME_SLICE_KPI_PATH)}`, `{rel(CURVE_DIAGNOSTICS_PATH)}`, `{rel(REVIEW_RESULT_PATH)}`.",
            "- lineage_judgment(계보 판정): `connected_with_boundary(경계부 연결)`.",
            "",
            "## Boundary(경계)",
            "",
            "- positive_claim(긍정 주장): `none(없음)`.",
            "- selected_candidate(선택 후보): `none`.",
            "- ONNX readiness(ONNX 준비): `not_claimed`.",
            "- Goal Achieve(목표 달성): `not_claimed`.",
            "- missing_required(필수 누락): broader period pressure(더 넓은 기간 압박), Adapter follow-up(어댑터 후속), true fallback/routed robustness(실제 대체 라우팅 강건성), ONNX parity(ONNX 동등성).",
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
    candidate_review = build_candidate_followup_review(curve_rows, time_rows)
    candidate_summary = build_candidate_summary(candidate_review)
    profile_summary = build_followup_profile_summary(candidate_review)
    negative = negative_slices(time_rows)
    tier_duplicate_review = build_tier_duplicate_review(curve_rows)
    status = result_status(parser_errors, parser_checks)
    judgment = result_judgment(status)
    next_action = result_next_action(status)
    watch_rows = sum(
        1
        for row in candidate_review
        if row.get("decision_read") in {"constructive_followup_watch_no_selection", "mixed_constructive_needs_wider_pressure"}
    )
    result = {
        "status": status,
        "judgment": judgment,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_run_id": PARENT_RUN_ID,
        "source_materialization_run_id": SOURCE_MATERIALIZATION_RUN_ID,
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "trade_record_count": len(trade_rows),
        "time_slice_row_count": len(time_rows),
        "curve_row_count": len(curve_rows),
        "candidate_followup_review": candidate_review,
        "candidate_summary": candidate_summary,
        "followup_profile_summary": profile_summary,
        "negative_slices": negative,
        "tier_duplicate_review": tier_duplicate_review,
        "parser_errors": parser_errors,
        "parser_checks": parser_checks,
        "forensics_summary": forensics_summary(forensics_rows),
        "watch_rows": watch_rows,
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": next_action,
        "outputs": {
            "trade_records": rel(TRADE_RECORDS_PATH),
            "time_slice_kpi": rel(TIME_SLICE_KPI_PATH),
            "curve_diagnostics": rel(CURVE_DIAGNOSTICS_PATH),
            "candidate_followup_review": rel(CANDIDATE_FOLLOWUP_REVIEW_PATH),
            "candidate_summary": rel(CANDIDATE_SUMMARY_PATH),
            "followup_profile_summary": rel(FOLLOWUP_PROFILE_SUMMARY_PATH),
            "negative_slice_summary": rel(NEGATIVE_SLICE_PATH),
            "tier_duplicate_review": rel(TIER_DUPLICATE_REVIEW_PATH),
            "parser_checks": rel(PARSER_CHECKS_PATH),
            "parser_errors": rel(PARSER_ERRORS_PATH),
            "review_result": rel(REVIEW_RESULT_PATH),
            "report": rel(REPORT_PATH),
        },
        "sources": {
            "execution_result": rel(SOURCE_EXECUTION_RESULT_PATH),
            "kpi_summary": rel(SOURCE_KPI_SUMMARY_PATH),
            "forensics": rel(SOURCE_FORENSICS_PATH),
            "executed_attempts": rel(SOURCE_EXECUTED_ATTEMPTS_PATH),
            "variant_manifest": rel(SOURCE_VARIANT_MANIFEST_PATH),
            "runtime_contract": rel(SOURCE_RUNTIME_CONTRACT_PATH),
            "base_kpi": rel(BASE_KPI_PATH),
            "base_curve": rel(BASE_CURVE_PATH),
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
            "source_test_id",
            "source_queue_id",
            "state_profile",
            "followup_profile",
            "pressure_group",
            "model_materialization_type",
            "materialization_boundary",
            "record_view",
            "attempt_name",
            "tier_scope",
            "route_role",
            "split",
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
            "tier_scope",
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "source_test_id",
            "source_queue_id",
            "state_profile",
            "followup_profile",
            "pressure_group",
            "materialization_boundary",
            "route_role",
            "axis",
            "bucket",
            *METRIC_COLUMNS,
            "slice_read",
        ),
    )
    write_csv(
        CURVE_DIAGNOSTICS_PATH,
        curve_rows,
        (
            "record_view",
            "tier_scope",
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "source_test_id",
            "source_queue_id",
            "state_profile",
            "followup_profile",
            "pressure_group",
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
    write_csv(CANDIDATE_FOLLOWUP_REVIEW_PATH, candidate_review, tuple(candidate_review[0].keys()) if candidate_review else ())
    write_csv(CANDIDATE_SUMMARY_PATH, candidate_summary, tuple(candidate_summary[0].keys()) if candidate_summary else ())
    write_csv(FOLLOWUP_PROFILE_SUMMARY_PATH, profile_summary, tuple(profile_summary[0].keys()) if profile_summary else ())
    write_csv(NEGATIVE_SLICE_PATH, negative, tuple(negative[0].keys()) if negative else ())
    write_csv(TIER_DUPLICATE_REVIEW_PATH, tier_duplicate_review, tuple(tier_duplicate_review[0].keys()) if tier_duplicate_review else ())
    write_csv(
        PARSER_CHECKS_PATH,
        parser_checks,
        ("attempt_name", "record_view", "tier_scope", "report_path", "expected_trade_count", "parsed_trade_count", "trade_count_delta", "parser_status"),
    )
    write_csv(PARSER_ERRORS_PATH, parser_errors, ("attempt_name", "report_path", "error"))
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
                "candidate_followup_rows": len(result["candidate_followup_review"]),
                "watch_rows": result["watch_rows"],
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
