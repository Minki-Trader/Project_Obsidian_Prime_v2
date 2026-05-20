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

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized
from foundation.mt5.trade_report import pair_deals_into_trades, parse_mt5_trade_report
from stage_pipelines.stage267 import run267N_pool_wide_ablation_replacement_executor as source_executor
from stage_pipelines.stage267 import run267N_pool_wide_ablation_replacement_materialization as source_materializer


STAGE_ID = source_materializer.STAGE_ID
SOURCE_RUN_ID = source_materializer.RUN_ID
RUN_NUMBER = "run267O"
RUN_ID = "run267O_stage267_pool_wide_balance_timeslice_trade_quality_review_v1"
STATUS = "run267O_pool_wide_balance_timeslice_trade_quality_review_completed"
PARTIAL_STATUS = "run267O_pool_wide_balance_timeslice_trade_quality_review_partial_parser_errors"
NEXT_ACTION = "run267P_pool_wide_internal_feature_order_confirmation_and_adapter_design"
NEXT_ACTION_PARTIAL = "run267O_repair_pool_wide_trade_report_parser_errors"
CLAIM_BOUNDARY = source_materializer.CLAIM_BOUNDARY

STAGE_ROOT = source_materializer.STAGE_ROOT
REVIEWS_ROOT = source_materializer.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "pool_wide_balance_timeslice_trade_quality_review"
SOURCE_ROOT = source_materializer.MATERIALIZATION_ROOT

SOURCE_EXECUTION_RESULT_PATH = source_executor.EXECUTION_RESULT_PATH
SOURCE_KPI_DELTA_PATH = SOURCE_ROOT / "kpi_delta_review.csv"
SOURCE_KPI_SUMMARY_PATH = source_executor.KPI_SUMMARY_PATH
SOURCE_FORENSICS_PATH = source_executor.FORENSICS_PATH
BASE_KPI_PATH = STAGE_ROOT / "02_runs" / "run267B" / "historical_2024" / "mt5_kpi_summary.csv"
BASE_CURVE_PATH = STAGE_ROOT / "02_runs" / "run267B" / "historical_2024" / "balance_curve_diagnostics.csv"

TRADE_RECORDS_PATH = RUN_ROOT / "trade_records.csv"
TIME_SLICE_KPI_PATH = RUN_ROOT / "time_slice_kpi.csv"
CURVE_DIAGNOSTICS_PATH = RUN_ROOT / "curve_diagnostics.csv"
CANDIDATE_TEST_REVIEW_PATH = RUN_ROOT / "candidate_test_review.csv"
CANDIDATE_SUMMARY_PATH = RUN_ROOT / "candidate_balance_timeslice_summary.csv"
TEST_AXIS_SUMMARY_PATH = RUN_ROOT / "test_axis_balance_timeslice_summary.csv"
NEGATIVE_SLICE_PATH = RUN_ROOT / "negative_slice_summary.csv"
PARSER_CHECKS_PATH = RUN_ROOT / "parser_checks.csv"
REVIEW_RESULT_PATH = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267O_pool_wide_balance_timeslice_trade_quality_review.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267O_pool_wide_balance_timeslice_trade_quality_review.py")

STAGE_LEDGER_PATH = source_materializer.STAGE_LEDGER_PATH
PROJECT_LEDGER_PATH = source_materializer.PROJECT_LEDGER_PATH
RUN_REGISTRY_PATH = source_materializer.RUN_REGISTRY_PATH
ARTIFACT_REGISTRY_PATH = source_materializer.ARTIFACT_REGISTRY_PATH
CURRENT_WORKING_STATE_PATH = source_materializer.CURRENT_WORKING_STATE_PATH
WORKSPACE_STATE_PATH = source_materializer.WORKSPACE_STATE_PATH
SELECTION_STATUS_PATH = source_materializer.SELECTION_STATUS_PATH
REVIEW_INDEX_PATH = source_materializer.REVIEW_INDEX_PATH

DEPOSIT = 500.0
AXES = ("month", "weekday", "close_hour_report", "session_report", "direction", "chron_segment")


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
        return int(float(value))
    except (TypeError, ValueError):
        return default


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


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


def upsert_csv(path: Path, key: str, row: Mapping[str, Any], columns: Sequence[str]) -> None:
    rows = read_csv(path)
    merged = [item for item in rows if item.get(key) != row.get(key)]
    merged.append(dict(row))
    write_csv(path, merged, columns)


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
    ordered = sorted(rows, key=lambda item: str(item.get("close_time")))
    for row in ordered:
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
    share = underwater_count / len(ordered) if ordered else 0.0
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
    if net <= -150.0 or dd_pct >= 30.0:
        return "deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)"
    if net < -50.0:
        return "negative_fragile_slice(음수 취약 구간)"
    if net < 0.0:
        return "minor_negative_slice(소폭 음수 구간)"
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
    if equity_dd >= 31.0 or worst_month_net <= -160.0:
        return "dd_or_month_hole_uncomfortable(손실폭 또는 월별 구멍 불편)"
    if trades >= 250 and net >= 300.0 and pf >= 1.18 and equity_dd <= 24.0 and positive_month_ratio >= 0.5:
        return "constructive_curve_watch_not_selection(건설적 곡선 관찰, 선택 아님)"
    if net > 0.0 and pf > 1.05 and equity_dd < 31.0:
        return "mixed_constructive_needs_more_pressure(혼합 건설적, 추가 압박 필요)"
    return "mixed_or_fragile(혼합 또는 취약)"


def build_trade_records(execution_result: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    attempts = {str(item.get("attempt_name")): item for item in execution_result.get("attempts_executed", [])}
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
        except Exception as exc:  # pragma: no cover - parser failures are persisted as evidence.
            parser_errors.append({"attempt_name": attempt_name, "report_path": rel(html_path), "error": str(exc)})
            continue
        expected_count = as_int(metrics_payload.get("trade_count"))
        parser_checks.append(
            {
                "attempt_name": attempt_name,
                "record_view": record.get("record_view"),
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
                    "source_run_id": SOURCE_RUN_ID,
                    "queue_id": attempt.get("queue_id"),
                    "candidate_id": attempt.get("candidate_id"),
                    "candidate_alias": attempt.get("candidate_alias"),
                    "candidate_role": attempt.get("candidate_role"),
                    "test_id": attempt.get("test_id"),
                    "test_type": attempt.get("test_type"),
                    "materialization_boundary": attempt.get("materialization_boundary"),
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
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "test_id",
            "test_type",
            "materialization_boundary",
            "route_role",
            axis,
        )
        for key, rows in group_rows(trade_rows, keys).items():
            (
                record_view,
                candidate_id,
                alias,
                role,
                test_id,
                test_type,
                boundary,
                route_role,
                bucket,
            ) = key
            item = metrics(rows)
            output.append(
                {
                    "record_view": record_view,
                    "candidate_id": candidate_id,
                    "candidate_alias": alias,
                    "candidate_role": role,
                    "test_id": test_id,
                    "test_type": test_type,
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
        "candidate_id",
        "candidate_alias",
        "candidate_role",
        "test_id",
        "test_type",
        "materialization_boundary",
        "route_role",
    )
    for key, rows in group_rows(trade_rows, keys).items():
        (
            record_view,
            candidate_id,
            alias,
            role,
            test_id,
            test_type,
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
        chron_by_bucket = {str(row.get("bucket")): row for row in chron_slices}
        output.append(
            {
                "record_view": record_view,
                "candidate_id": candidate_id,
                "candidate_alias": alias,
                "candidate_role": role,
                "test_id": test_id,
                "test_type": test_type,
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
                "source_chart_path": rel(charts.get(str(record_view), "")) if charts.get(str(record_view)) else "",
                "curve_read": curve_read(item, report_metrics, month_slices),
            }
        )
    return output


def base_kpi_by_alias() -> dict[str, dict[str, str]]:
    rows: dict[str, dict[str, str]] = {}
    for row in read_csv(BASE_KPI_PATH):
        if row.get("route_role") != "routed_total":
            continue
        record_view = str(row.get("record_view", ""))
        for alias in ("s264_aih", "s264_lc", "s262_lih", "s264_aia", "s258_stc"):
            if alias in record_view:
                rows[alias] = row
                break
    return rows


def base_curve_by_alias() -> dict[str, dict[str, str]]:
    rows: dict[str, dict[str, str]] = {}
    for row in read_csv(BASE_CURVE_PATH):
        if row.get("route_role") != "routed_total":
            continue
        alias = str(row.get("candidate_alias") or "")
        if alias:
            rows[alias] = row
    return rows


def kpi_delta_by_view() -> dict[str, dict[str, str]]:
    return {row["record_view"]: row for row in read_csv(SOURCE_KPI_DELTA_PATH)}


def weakest_bucket(time_rows: Sequence[Mapping[str, Any]], record_view: str, axis: str) -> Mapping[str, Any] | None:
    rows = [
        row
        for row in time_rows
        if row.get("record_view") == record_view and row.get("axis") == axis and as_int(row.get("trade_count")) >= 3
    ]
    if not rows:
        return None
    return min(rows, key=lambda row: as_float(row.get("net_profit")))


def review_read(curve: Mapping[str, Any], base: Mapping[str, Any], weak_month: Mapping[str, Any]) -> str:
    net_delta = as_float(curve.get("net_profit")) - as_float(base.get("net_profit"))
    pf_delta = as_float(curve.get("profit_factor")) - as_float(base.get("profit_factor"))
    dd_delta = as_float(curve.get("report_equity_drawdown_percent")) - as_float(base.get("max_drawdown_percent"))
    equity_dd = as_float(curve.get("report_equity_drawdown_percent"))
    pf = as_float(curve.get("profit_factor"))
    weak_month_net = as_float(weak_month.get("net_profit"))
    curve_label = str(curve.get("curve_read"))
    if "fragile" in curve_label or as_float(curve.get("net_profit")) <= 0.0:
        return "fragile_or_negative_failure_memory(취약 또는 음수 실패 기억)"
    if net_delta > 250.0 and pf_delta > 0.10 and dd_delta < -8.0 and equity_dd <= 24.0 and weak_month_net > -140.0:
        return "strong_curve_clue_needs_internal_confirmation(강한 곡선 단서, 내부 확인 필요)"
    if net_delta > 0.0 and dd_delta < 0.0 and pf > 1.05 and equity_dd < 31.0:
        return "constructive_but_not_adapter_ready(건설적이나 어댑터 준비 아님)"
    return "mixed_or_insufficient_curve_evidence(혼합 또는 곡선 근거 부족)"


def build_candidate_test_review(
    curve_rows: Sequence[Mapping[str, Any]],
    time_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    base_kpi = base_kpi_by_alias()
    base_curve = base_curve_by_alias()
    kpi_delta = kpi_delta_by_view()
    output: list[dict[str, Any]] = []
    for row in curve_rows:
        if row.get("route_role") != "routed_total":
            continue
        alias = str(row.get("candidate_alias"))
        base = base_kpi.get(alias, {})
        base_curve_row = base_curve.get(alias, {})
        weak_month = weakest_bucket(time_rows, str(row.get("record_view")), "month") or {}
        weak_weekday = weakest_bucket(time_rows, str(row.get("record_view")), "weekday") or {}
        weak_hour = weakest_bucket(time_rows, str(row.get("record_view")), "close_hour_report") or {}
        weak_session = weakest_bucket(time_rows, str(row.get("record_view")), "session_report") or {}
        weak_direction = weakest_bucket(time_rows, str(row.get("record_view")), "direction") or {}
        weak_chron = weakest_bucket(time_rows, str(row.get("record_view")), "chron_segment") or {}
        delta_row = kpi_delta.get(str(row.get("record_view")), {})
        net = as_float(row.get("net_profit"))
        base_net = as_float(base.get("net_profit"))
        pf = as_float(row.get("profit_factor"))
        base_pf = as_float(base.get("profit_factor"))
        dd = as_float(row.get("report_equity_drawdown_percent"))
        base_dd = as_float(base.get("max_drawdown_percent"))
        output.append(
            {
                "candidate_id": row.get("candidate_id"),
                "candidate_alias": alias,
                "candidate_role": row.get("candidate_role"),
                "test_id": row.get("test_id"),
                "test_type": row.get("test_type"),
                "materialization_boundary": row.get("materialization_boundary"),
                "record_view": row.get("record_view"),
                "net_profit": net,
                "base_2024_net_profit": base_net,
                "net_delta_vs_base_2024": net - base_net,
                "profit_factor": pf,
                "base_2024_profit_factor": base_pf,
                "pf_delta_vs_base_2024": pf - base_pf,
                "trade_count": row.get("trade_count"),
                "base_2024_trade_count": base.get("trade_count", ""),
                "trade_delta_vs_base_2024": as_float(row.get("trade_count")) - as_float(base.get("trade_count")),
                "report_equity_drawdown_percent": dd,
                "base_2024_max_drawdown_percent": base_dd,
                "dd_delta_vs_base_2024": dd - base_dd,
                "recovery_factor": row.get("report_recovery_factor"),
                "base_2024_recovery_factor": base.get("recovery_factor", ""),
                "positive_month_ratio": row.get("positive_month_ratio"),
                "negative_month_count": row.get("negative_month_count"),
                "worst_month": weak_month.get("bucket", ""),
                "worst_month_net": weak_month.get("net_profit", ""),
                "weakest_weekday": weak_weekday.get("bucket", ""),
                "weakest_weekday_net": weak_weekday.get("net_profit", ""),
                "weakest_hour_report": weak_hour.get("bucket", ""),
                "weakest_hour_net": weak_hour.get("net_profit", ""),
                "weakest_session_report": weak_session.get("bucket", ""),
                "weakest_session_net": weak_session.get("net_profit", ""),
                "weakest_direction": weak_direction.get("bucket", ""),
                "weakest_direction_net": weak_direction.get("net_profit", ""),
                "weakest_chron_segment": weak_chron.get("bucket", ""),
                "weakest_chron_net": weak_chron.get("net_profit", ""),
                "chron_early_net": row.get("chron_early_net"),
                "chron_mid_net": row.get("chron_mid_net"),
                "chron_late_net": row.get("chron_late_net"),
                "base_curve_grade": base_curve_row.get("curve_grade", ""),
                "base_curve_read": base_curve_row.get("curve_read", ""),
                "source_chart_path": row.get("source_chart_path"),
                "kpi_review_label": delta_row.get("review_label", ""),
                "curve_read": row.get("curve_read"),
                "review_read": review_read(row, base, weak_month),
            }
        )
    return sorted(output, key=lambda item: -as_float(item.get("net_profit")))


def candidate_read(rows: Sequence[Mapping[str, Any]]) -> str:
    destructive = [
        row
        for row in rows
        if "failure" in str(row.get("review_read")) or "destructive" in str(row.get("kpi_review_label"))
    ]
    strong = [row for row in rows if str(row.get("review_read")).startswith("strong_curve_clue")]
    avg_dd = mean(as_float(row.get("report_equity_drawdown_percent")) for row in rows) if rows else 0.0
    worst_month_floor = min((as_float(row.get("worst_month_net")) for row in rows), default=0.0)
    if destructive:
        return "contains_failure_memory_no_selection(실패 기억 포함, 선택 아님)"
    if len(strong) >= 2 and avg_dd <= 24.0 and worst_month_floor > -140.0:
        return "broad_constructive_watch_no_selection(넓은 건설적 관찰, 선택 아님)"
    if strong:
        return "single_axis_clue_needs_more_pressure(단일 축 단서, 추가 압박 필요)"
    return "mixed_or_fragile_no_selection(혼합 또는 취약, 선택 아님)"


def build_candidate_summary(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[str(row.get("candidate_alias"))].append(row)
    output: list[dict[str, Any]] = []
    for alias, items in sorted(grouped.items()):
        best_net = max(items, key=lambda row: as_float(row.get("net_profit")))
        worst_net = min(items, key=lambda row: as_float(row.get("net_profit")))
        strongest = [row for row in items if str(row.get("review_read")).startswith("strong_curve_clue")]
        failure = [row for row in items if "failure" in str(row.get("review_read")) or "destructive" in str(row.get("kpi_review_label"))]
        output.append(
            {
                "candidate_alias": alias,
                "candidate_id": best_net.get("candidate_id"),
                "candidate_role": best_net.get("candidate_role"),
                "test_count": len(items),
                "strong_curve_clue_count": len(strongest),
                "failure_memory_count": len(failure),
                "avg_net_profit": mean(as_float(row.get("net_profit")) for row in items),
                "avg_net_delta_vs_base_2024": mean(as_float(row.get("net_delta_vs_base_2024")) for row in items),
                "avg_profit_factor": mean(as_float(row.get("profit_factor")) for row in items),
                "avg_equity_drawdown_percent": mean(as_float(row.get("report_equity_drawdown_percent")) for row in items),
                "avg_dd_delta_vs_base_2024": mean(as_float(row.get("dd_delta_vs_base_2024")) for row in items),
                "avg_trade_count": mean(as_float(row.get("trade_count")) for row in items),
                "min_positive_month_ratio": min(as_float(row.get("positive_month_ratio")) for row in items),
                "max_negative_month_count": max(as_int(row.get("negative_month_count")) for row in items),
                "worst_month_floor": min(as_float(row.get("worst_month_net")) for row in items),
                "best_test_id": best_net.get("test_id"),
                "best_net_profit": best_net.get("net_profit"),
                "best_profit_factor": best_net.get("profit_factor"),
                "best_equity_drawdown_percent": best_net.get("report_equity_drawdown_percent"),
                "worst_test_id": worst_net.get("test_id"),
                "worst_net_profit": worst_net.get("net_profit"),
                "candidate_read": candidate_read(items),
            }
        )
    return sorted(output, key=lambda row: (-as_float(row.get("strong_curve_clue_count")), -as_float(row.get("avg_net_profit"))))


def build_test_axis_summary(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[str(row.get("test_id"))].append(row)
    output: list[dict[str, Any]] = []
    for test_id, items in sorted(grouped.items()):
        best = max(items, key=lambda row: as_float(row.get("net_profit")))
        worst = min(items, key=lambda row: as_float(row.get("net_profit")))
        output.append(
            {
                "test_id": test_id,
                "test_type": best.get("test_type"),
                "materialization_boundary": best.get("materialization_boundary"),
                "candidate_count": len(items),
                "avg_net_profit": mean(as_float(row.get("net_profit")) for row in items),
                "avg_net_delta_vs_base_2024": mean(as_float(row.get("net_delta_vs_base_2024")) for row in items),
                "avg_profit_factor": mean(as_float(row.get("profit_factor")) for row in items),
                "avg_equity_drawdown_percent": mean(as_float(row.get("report_equity_drawdown_percent")) for row in items),
                "avg_dd_delta_vs_base_2024": mean(as_float(row.get("dd_delta_vs_base_2024")) for row in items),
                "strong_curve_clue_count": sum(1 for row in items if str(row.get("review_read")).startswith("strong_curve_clue")),
                "failure_memory_count": sum(1 for row in items if "failure" in str(row.get("review_read"))),
                "best_candidate_alias": best.get("candidate_alias"),
                "best_net_profit": best.get("net_profit"),
                "worst_candidate_alias": worst.get("candidate_alias"),
                "worst_net_profit": worst.get("net_profit"),
            }
        )
    return sorted(output, key=lambda row: -as_float(row.get("avg_net_profit")))


def negative_slices(time_rows: Sequence[Mapping[str, Any]], limit: int = 80) -> list[dict[str, Any]]:
    rows = [
        row
        for row in time_rows
        if row.get("route_role") == "routed_total"
        and as_float(row.get("net_profit")) < 0.0
        and as_int(row.get("trade_count")) >= 3
    ]
    return [dict(row) for row in sorted(rows, key=lambda row: as_float(row.get("net_profit")))[:limit]]


def result_status(parser_errors: Sequence[Mapping[str, Any]]) -> str:
    return PARTIAL_STATUS if parser_errors else STATUS


def result_next_action(parser_errors: Sequence[Mapping[str, Any]]) -> str:
    return NEXT_ACTION_PARTIAL if parser_errors else NEXT_ACTION


def report_markdown(result: Mapping[str, Any]) -> str:
    candidate_summary = list(result["candidate_summary"])
    candidate_tests = list(result["candidate_test_review"])
    top_tests = sorted(candidate_tests, key=lambda row: as_float(row.get("net_profit")), reverse=True)[:12]
    weak_slices = list(result["negative_slices"])[:15]
    parser_errors = list(result["parser_errors"])
    lines = [
        "# Stage267 Run267O Pool-Wide Balance/Time-Slice/Trade-Quality Review(267단계 267O 후보군 전체 잔액/시간구간/거래품질 검토)",
        "",
        "- action(행동): run267N(267N 실행)의 48개 MT5(MetaTrader 5, 메타트레이더5) report(보고서)를 trade list(거래 목록)로 다시 파싱해 balance curve diagnostics(잔액 곡선 진단), time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질)를 만들었다.",
        "- effect(효과): net profit(순수익)만 보지 않고 월/요일/시간/세션/방향/초중후 구간에서 덜 깨지는 후보와 깨지는 축을 구분한다.",
        f"- status(상태): `{result['status']}`",
        f"- source_run(원천 실행): `{SOURCE_RUN_ID}`",
        f"- trade_records(거래 기록): `{result['trade_record_count']}`",
        f"- curve_rows(곡선 행): `{result['curve_row_count']}`",
        f"- time_slice_rows(시간 구간 행): `{result['time_slice_row_count']}`",
        f"- parser_errors(파서 오류): `{len(parser_errors)}`",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Easy Read(쉬운 해석)",
        "",
        "run267N(267N 실행)의 KPI(핵심 성과 지표) 단서는 일부 강했다. 하지만 이번 run267O(267O 실행)는 그 숫자가 곡선과 약한 구간에서도 덜 깨지는지 확인하는 단계다.",
        "결론은 아직 선택 후보(selected candidate, 선택 후보)가 없다는 것이다. 여러 변형이 2024 baseline(2024 기준)보다 좋아졌지만, 약한 월/구간, direct/proxy(직접/대체) 경계, 내부 feature order(피처 순서) 확인이 남아 있다.",
        "ONNX readiness(ONNX 준비)도 주장하지 않는다. 이번 결과는 다음 run267P(267P 실행)에서 내부 피처 확인과 Adapter(어댑터) 설계를 할 재료다.",
        "",
        "## Candidate Summary(후보 요약)",
        "",
        "| candidate(후보) | strong clues(강한 단서) | failures(실패) | avg net(평균 순수익) | avg PF(평균 수익 팩터) | avg DD%(평균 손실폭) | best test(최고 시험) | worst month floor(최악 월 바닥) | read(판독) |",
        "| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | --- |",
    ]
    for row in candidate_summary:
        lines.append(
            f"| `{row['candidate_alias']}` | {cell(row['strong_curve_clue_count'])} | {cell(row['failure_memory_count'])} | "
            f"{cell(row['avg_net_profit'])} | {cell(row['avg_profit_factor'])} | {cell(row['avg_equity_drawdown_percent'])} | "
            f"`{row['best_test_id']}` | {cell(row['worst_month_floor'])} | {row['candidate_read']} |"
        )
    lines.extend(
        [
            "",
            "## Top Candidate-Test Rows(상위 후보-시험 행)",
            "",
            "| candidate(후보) | test(시험) | net(순수익) | PF(수익 팩터) | DD%(손실폭) | trades(거래 수) | weakest month(가장 약한 월) | read(판독) |",
            "| --- | --- | ---: | ---: | ---: | ---: | --- | --- |",
        ]
    )
    for row in top_tests:
        lines.append(
            f"| `{row['candidate_alias']}` | `{row['test_id']}` | {cell(row['net_profit'])} | {cell(row['profit_factor'])} | "
            f"{cell(row['report_equity_drawdown_percent'])} | {cell(row['trade_count'])} | `{row['worst_month']}` {cell(row['worst_month_net'])} | {row['review_read']} |"
        )
    lines.extend(
        [
            "",
            "## Weak Slices(약한 구간)",
            "",
            "| candidate(후보) | test(시험) | axis(축) | bucket(구간) | trades(거래 수) | net(순수익) | PF(수익 팩터) | DD%(손실폭) |",
            "| --- | --- | --- | --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in weak_slices:
        lines.append(
            f"| `{row['candidate_alias']}` | `{row['test_id']}` | `{row['axis']}` | `{row['bucket']}` | "
            f"{cell(row['trade_count'])} | {cell(row['net_profit'])} | {cell(row['profit_factor'])} | {cell(row['closed_balance_max_drawdown_percent'])} |"
        )
    lines.extend(
        [
            "",
            "## Performance Attribution(성과 귀인)",
            "",
            "- observed_change(관측 변화): run267N(267N 실행)의 일부 proxy adapter(대체 어댑터)와 direct gate(직접 게이트) 변형은 2024 baseline(2024 기준) 대비 net profit(순수익), PF(profit factor, 수익 팩터), DD(drawdown, 손실폭)를 동시에 개선했다.",
            "- likely_drivers(가능한 원인): volatility/ATR(변동성/ATR) proxy axis(대체 축)는 여러 후보에서 손실폭을 낮췄고, `s264_lc`의 gate variant(게이트 변형)는 매우 큰 순수익 단서를 냈다.",
            "- alternative_explanations(대안 설명): proxy adapter(대체 어댑터)는 true internal feature ablation(진짜 내부 피처 제거)이 아니므로 feature order(피처 순서)와 runtime surface(런타임 표면) 확인 전에는 구조적 견고성으로 볼 수 없다.",
            "- attribution_confidence(귀인 신뢰도): `medium_to_low(중간~낮음)`. MT5 거래 목록 근거는 생겼지만 내부 피처 확인과 더 넓은 기간 검증은 남았다.",
            "",
            "## Backtest Forensics(백테스트 포렌식)",
            "",
            f"- source_execution_result(원천 실행 결과): `{rel(SOURCE_EXECUTION_RESULT_PATH)}`",
            f"- source_kpi_summary(원천 KPI 요약): `{rel(SOURCE_KPI_SUMMARY_PATH)}`",
            f"- source_forensics(원천 포렌식): `{rel(SOURCE_FORENSICS_PATH)}`",
            f"- source_reports(원천 보고서): `{rel(SOURCE_ROOT / 'mt5' / 'reports')}`",
            "- tester_scope(테스터 범위): historical 2024(2024 과거 기간) `US100` `M5`, deposit(예치금) 500, Strategy Tester(전략 테스터) 산출물.",
            "- cost_assumptions(비용 가정): spread/commission/slippage/swap(스프레드/수수료/슬리피지/스왑)는 Strategy Tester(전략 테스터)와 broker history(브로커 이력) 조건을 따른다. 별도 비용 우위를 주장하지 않는다.",
            "",
            "## Artifact Lineage(산출물 계보)",
            "",
            f"- producer(생산자): `{rel(PRODUCER_PATH)}`",
            f"- trade_records(거래 기록): `{rel(TRADE_RECORDS_PATH)}`",
            f"- time_slice_kpi(시간 구간 핵심 성과 지표): `{rel(TIME_SLICE_KPI_PATH)}`",
            f"- curve_diagnostics(곡선 진단): `{rel(CURVE_DIAGNOSTICS_PATH)}`",
            f"- candidate_test_review(후보-시험 검토): `{rel(CANDIDATE_TEST_REVIEW_PATH)}`",
            f"- candidate_summary(후보 요약): `{rel(CANDIDATE_SUMMARY_PATH)}`",
            f"- test_axis_summary(시험 축 요약): `{rel(TEST_AXIS_SUMMARY_PATH)}`",
            f"- negative_slice_summary(음수 구간 요약): `{rel(NEGATIVE_SLICE_PATH)}`",
            f"- parser_checks(파서 점검): `{rel(PARSER_CHECKS_PATH)}`",
            f"- review_result(검토 결과): `{rel(REVIEW_RESULT_PATH)}`",
            "",
            "## Judgment Boundary(판정 경계)",
            "",
            "- result_subject(결과 대상): `run267O_pool_wide_balance_timeslice_trade_quality_review`.",
            "- judgment_label(판정 라벨): `diagnostic_review_completed_no_candidate_selection`.",
            "- selected_candidate(선택 후보): `none`.",
            "- ONNX readiness(ONNX 준비): `not_claimed`.",
            "- Goal Achieve(목표 달성): `not_claimed`.",
            f"- next_action(다음 행동): `{result['next_action']}`.",
        ]
    )
    return "\n".join(lines)


def update_ledgers(created_at: str, result: Mapping[str, Any]) -> None:
    status = str(result["status"])
    next_action = str(result["next_action"])
    judgment = "diagnostic_review_completed_no_candidate_selection"
    upsert_csv(
        STAGE_LEDGER_PATH,
        "row_id",
        {
            "row_id": "stage267_run267O_pool_wide_balance_timeslice_trade_quality_review",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "view": "pool_wide_balance_timeslice_trade_quality_review",
            "tier_scope": "Tier A and Tier A+B historical 2024 pool-wide P0 MT5 review",
            "scoreboard": "trade_shape_curve_time_slice_review",
            "status": status,
            "judgment": judgment,
            "evidence_boundary": "curve_time_slice_trade_quality_review_not_candidate_selection_not_onnx",
            "report_path": rel(REPORT_PATH),
            "notes": f"candidate_test_rows={len(result['candidate_test_review'])};negative_slices={len(result['negative_slices'])};next_action={next_action};selected_candidate=none.",
        },
        ("row_id", "stage_id", "run_id", "view", "tier_scope", "scoreboard", "status", "judgment", "evidence_boundary", "report_path", "notes"),
    )
    upsert_csv(
        RUN_REGISTRY_PATH,
        "run_id",
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "baseline_candidate_racing_pool_wide_balance_timeslice_trade_quality_review",
            "status": status,
            "judgment": judgment,
            "path": rel(REPORT_PATH),
            "notes": f"Run267O balance/time-slice/trade-quality review from run267N reports; selected_candidate=none; onnx_readiness=not_claimed; next_action={next_action}.",
        },
        ("run_id", "stage_id", "lane", "status", "judgment", "path", "notes"),
    )
    upsert_csv(
        PROJECT_LEDGER_PATH,
        "ledger_row_id",
        {
            "ledger_row_id": f"{RUN_ID}__pool_wide_balance_timeslice_trade_quality_review",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "pool_wide_balance_timeslice_trade_quality_review",
            "parent_run_id": SOURCE_RUN_ID,
            "record_view": "pool_wide_balance_timeslice_trade_quality_review",
            "tier_scope": "Tier A and Tier A+B historical 2024 pool-wide P0 MT5 review",
            "kpi_scope": "curve_time_slice_trade_quality_review",
            "scoreboard_lane": "trade_shape_curve_time_slice_review",
            "status": status,
            "judgment": judgment,
            "path": rel(REPORT_PATH),
            "primary_kpi": f"candidate_test_rows={len(result['candidate_test_review'])};negative_slices={len(result['negative_slices'])}",
            "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
            "external_verification_status": "completed_for_run267N_mt5_report_review",
            "notes": f"Next action: {next_action}.",
        },
        (
            "ledger_row_id",
            "stage_id",
            "run_id",
            "subrun_id",
            "parent_run_id",
            "record_view",
            "tier_scope",
            "kpi_scope",
            "scoreboard_lane",
            "status",
            "judgment",
            "path",
            "primary_kpi",
            "guardrail_kpi",
            "external_verification_status",
            "notes",
        ),
    )
    entries = (
        ("stage267_run267O_balance_timeslice_review_script", "producer_script", PRODUCER_PATH, "Builds run267O balance/time-slice/trade-quality review."),
        ("stage267_run267O_trade_records", "trade_records", TRADE_RECORDS_PATH, "Run267O paired trade records from run267N reports."),
        ("stage267_run267O_time_slice_kpi", "time_slice_kpi", TIME_SLICE_KPI_PATH, "Run267O month/weekday/hour/session/direction/chron-segment KPI."),
        ("stage267_run267O_curve_diagnostics", "curve_diagnostics", CURVE_DIAGNOSTICS_PATH, "Run267O closed-balance curve diagnostics."),
        ("stage267_run267O_candidate_test_review", "candidate_test_review", CANDIDATE_TEST_REVIEW_PATH, "Run267O candidate-test curve and weak-slice review."),
        ("stage267_run267O_candidate_summary", "candidate_summary", CANDIDATE_SUMMARY_PATH, "Run267O candidate balance/time-slice summary."),
        ("stage267_run267O_test_axis_summary", "test_axis_summary", TEST_AXIS_SUMMARY_PATH, "Run267O test-axis summary."),
        ("stage267_run267O_negative_slice_summary", "negative_slice_summary", NEGATIVE_SLICE_PATH, "Run267O worst negative slices."),
        ("stage267_run267O_parser_checks", "parser_checks", PARSER_CHECKS_PATH, "Run267O parser reconciliation checks."),
        ("stage267_run267O_review_result", "review_result", REVIEW_RESULT_PATH, "Run267O review JSON payload."),
        ("stage267_run267O_review_report", "review_report", REPORT_PATH, "User-facing run267O balance/time-slice/trade-quality review."),
    )
    registry_rows = read_csv(ARTIFACT_REGISTRY_PATH)
    replacement = {
        artifact_id: {
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
    }
    merged = [row for row in registry_rows if row.get("artifact_id") not in replacement]
    merged.extend(replacement.values())
    write_csv(
        ARTIFACT_REGISTRY_PATH,
        merged,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
    )


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    changed = False
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            changed = True
            break
    if not changed:
        lines.append(replacement)
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def replace_existing_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            break
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def append_after_contains(text: str, needle: str, line: str) -> str:
    if line in text:
        return text
    lines = text.splitlines()
    for index, existing in enumerate(lines):
        if needle in existing:
            lines.insert(index + 1, line)
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text.rstrip() + "\n" + line + "\n"


def update_current_docs(result: Mapping[str, Any]) -> None:
    status = str(result["status"])
    next_action = str(result["next_action"])
    review_line = f"- Stage267(267단계) run267O pool-wide balance/time-slice/trade-quality review(후보군 전체 잔액/시간구간/거래품질 검토): `{rel(REPORT_PATH)}`"
    index_line = f"- run267O_pool_wide_balance_timeslice_trade_quality_review(267O 후보군 전체 잔액/시간구간/거래품질 검토): `{rel(REPORT_PATH)}`"
    summary_line = (
        "Run267O(267O 실행)는 run267N(267N 실행)의 48개 MT5(MetaTrader 5, 메타트레이더5) 보고서를 거래 단위로 다시 파싱해 balance/time-slice/trade-quality review(잔액/시간구간/거래품질 검토)를 완료했다.\n"
        "Effect(효과): 강한 KPI(핵심 성과 지표) 단서는 남겼지만 약한 월/구간과 proxy/internal feature(대체/내부 피처) 경계가 남아 선택 후보(selected candidate, 선택 후보)와 ONNX readiness(ONNX 준비)는 없다."
    )
    for path, line, anchor in (
        (CURRENT_WORKING_STATE_PATH, review_line, "stage267_run267N_pool_wide_ablation_replacement_kpi_review.md"),
        (SELECTION_STATUS_PATH, index_line, "run267N_pool_wide_ablation_replacement_kpi_review"),
        (REVIEW_INDEX_PATH, index_line, "run267N_pool_wide_ablation_replacement_kpi_review"),
    ):
        text = io_path(path).read_text(encoding="utf-8-sig")
        if path == CURRENT_WORKING_STATE_PATH:
            text = replace_existing_line_prefix(text, "- status(상태):", f"- status(상태): `{status}`")
            text = replace_existing_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_existing_line_prefix(text, "- adapter_under_review(검토 중 어댑터):", "- adapter_under_review(검토 중 어댑터): `pool_wide_balance_timeslice_trade_quality_review`")
            text = replace_existing_line_prefix(text, "- next_run(다음 실행):", f"- next_run(다음 실행): `{next_action}`")
            text = replace_existing_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{next_action}`")
        elif path == SELECTION_STATUS_PATH:
            text = replace_existing_line_prefix(text, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{status}`")
            text = replace_existing_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_existing_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = replace_existing_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{next_action}`")
        else:
            text = replace_existing_line_prefix(text, "- status(상태):", f"- status(상태): `{status}`")
            text = replace_existing_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_existing_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
        text = append_after_contains(text, anchor, line)
        text = append_after_contains(text, "Run267O(267O 실행)는", summary_line)
        if path == CURRENT_WORKING_STATE_PATH:
            text = append_after_contains(
                text,
                "## Current Next Action",
                f"- latest_mt5_review(최신 MT5 검토): run267O(267O 실행) candidate-test rows(후보-시험 행) `{len(result['candidate_test_review'])}`, negative slices(음수 구간) `{len(result['negative_slices'])}`, report(보고서) `{rel(REPORT_PATH)}`.",
            )
            text = replace_line_prefix(
                text,
                "- action(행동):",
                "- action(행동): run267O(267O 실행)는 run267N(267N 실행)의 48개 MT5(MetaTrader 5, 메타트레이더5) report(보고서)를 거래 단위로 다시 검토했다.",
            )
            text = replace_line_prefix(
                text,
                "- effect(효과):",
                "- effect(효과): 다음 작업은 내부 feature order(피처 순서)와 Adapter(어댑터) 설계 가능성을 확인해 proxy clue(대체 단서)를 구조 단서로 격상할 수 있는지 보는 것이다.",
            )
        write_md(path, text)

    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    workspace = workspace.replace(f"current_run_id: {SOURCE_RUN_ID}", f"current_run_id: {RUN_ID}")
    workspace = workspace.replace("status: run267N_pool_wide_ablation_replacement_kpi_review_completed", f"status: {status}")
    workspace = workspace.replace(f"last_completed_run_id: {SOURCE_RUN_ID}", f"last_completed_run_id: {RUN_ID}")
    workspace = workspace.replace("next_action: run267O_pool_wide_balance_timeslice_trade_quality_review", f"next_action: {next_action}")
    workspace = workspace.replace(
        "Next action(다음 행동)는 `run267O_pool_wide_balance_timeslice_trade_quality_review`이다. Effect(효과): KPI 단서를 balance/equity curve(잔액/평가금 곡선), trade quality(거래 품질), time-slice KPI(시간 구간 핵심 성과 지표)로 검토한다.",
        f"Next action(다음 행동)는 `{next_action}`이다. Effect(효과): 내부 feature order(피처 순서) 확인과 Adapter(어댑터) 설계 가능성을 검토한다.",
    )
    workspace = workspace.replace(
        "is active_run267N_pool_wide_ablation_replacement_kpi_review_completed(267N 후보군 전체 제거/대체 KPI 검토 완료, 곡선/시간구간 검토 대기 활성).",
        "is active_run267O_pool_wide_balance_timeslice_trade_quality_review_completed(267O 후보군 전체 잔액/시간구간/거래품질 검토 완료, 내부 피처 확인 대기 활성).",
    )
    focus_line = (
        "- >-\n"
        f"  Stage267(267단계) run267O(267O 실행) pool-wide balance/time-slice/trade-quality review(후보군 전체 잔액/시간구간/거래품질 검토) `{status}`. Effect(효과): run267N(267N 실행)의 48개 MT5(MetaTrader 5, 메타트레이더5) 보고서를 거래 목록, 곡선, 약한 구간으로 검토했고 selected candidate(선택 후보)나 ONNX readiness(ONNX 준비)는 주장하지 않는다."
    )
    if f"`{status}`" not in workspace:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus_line + "\n", 1)
    workspace = append_after_contains(
        workspace,
        "run267N_pool_wide_ablation_replacement_kpi_review_report_path",
        f"  run267O_pool_wide_balance_timeslice_trade_quality_review_report_path: {rel(REPORT_PATH)}",
    )
    write_md(WORKSPACE_STATE_PATH, workspace)


def review() -> dict[str, Any]:
    if not path_exists(SOURCE_EXECUTION_RESULT_PATH):
        raise FileNotFoundError(SOURCE_EXECUTION_RESULT_PATH)
    created_at = utc_now()
    execution_result = read_json(SOURCE_EXECUTION_RESULT_PATH)
    trade_rows, parser_errors, parser_checks = build_trade_records(execution_result)
    time_rows = build_time_slice_rows(trade_rows)
    curve_rows = build_curve_rows(trade_rows, time_rows, execution_result)
    candidate_tests = build_candidate_test_review(curve_rows, time_rows)
    candidate_summary = build_candidate_summary(candidate_tests)
    test_axis_summary = build_test_axis_summary(candidate_tests)
    negative = negative_slices(time_rows)
    result = {
        "status": result_status(parser_errors),
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "trade_record_count": len(trade_rows),
        "time_slice_row_count": len(time_rows),
        "curve_row_count": len(curve_rows),
        "candidate_test_review": candidate_tests,
        "candidate_summary": candidate_summary,
        "test_axis_summary": test_axis_summary,
        "negative_slices": negative,
        "parser_errors": parser_errors,
        "parser_checks": parser_checks,
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": result_next_action(parser_errors),
        "outputs": {
            "trade_records": rel(TRADE_RECORDS_PATH),
            "time_slice_kpi": rel(TIME_SLICE_KPI_PATH),
            "curve_diagnostics": rel(CURVE_DIAGNOSTICS_PATH),
            "candidate_test_review": rel(CANDIDATE_TEST_REVIEW_PATH),
            "candidate_summary": rel(CANDIDATE_SUMMARY_PATH),
            "test_axis_summary": rel(TEST_AXIS_SUMMARY_PATH),
            "negative_slice_summary": rel(NEGATIVE_SLICE_PATH),
            "parser_checks": rel(PARSER_CHECKS_PATH),
            "review_result": rel(REVIEW_RESULT_PATH),
            "report": rel(REPORT_PATH),
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
            "test_type",
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
    metric_columns = (
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
    write_csv(
        TIME_SLICE_KPI_PATH,
        time_rows,
        (
            "record_view",
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "test_id",
            "test_type",
            "materialization_boundary",
            "route_role",
            "axis",
            "bucket",
            *metric_columns,
            "slice_read",
        ),
    )
    write_csv(
        CURVE_DIAGNOSTICS_PATH,
        curve_rows,
        (
            "record_view",
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "test_id",
            "test_type",
            "materialization_boundary",
            "route_role",
            *metric_columns,
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
    write_csv(
        CANDIDATE_TEST_REVIEW_PATH,
        candidate_tests,
        tuple(candidate_tests[0].keys()) if candidate_tests else (),
    )
    write_csv(
        CANDIDATE_SUMMARY_PATH,
        candidate_summary,
        tuple(candidate_summary[0].keys()) if candidate_summary else (),
    )
    write_csv(
        TEST_AXIS_SUMMARY_PATH,
        test_axis_summary,
        tuple(test_axis_summary[0].keys()) if test_axis_summary else (),
    )
    write_csv(
        NEGATIVE_SLICE_PATH,
        negative,
        tuple(negative[0].keys()) if negative else (
            "record_view",
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "test_id",
            "test_type",
            "materialization_boundary",
            "route_role",
            "axis",
            "bucket",
            *metric_columns,
            "slice_read",
        ),
    )
    write_csv(
        PARSER_CHECKS_PATH,
        parser_checks,
        ("attempt_name", "record_view", "report_path", "expected_trade_count", "parsed_trade_count", "trade_count_delta", "parser_status"),
    )
    write_json(REVIEW_RESULT_PATH, result)
    write_md(REPORT_PATH, report_markdown(result))
    update_ledgers(created_at, result)
    update_current_docs(result)
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
                "negative_slices": len(result["negative_slices"]),
                "parser_errors": len(result["parser_errors"]),
                "next_action": result["next_action"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
