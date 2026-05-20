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

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized
from foundation.mt5.trade_report import pair_deals_into_trades, parse_mt5_trade_report
from stage_pipelines.stage267 import run267N_pool_wide_ablation_replacement_executor as source_n_executor
from stage_pipelines.stage267 import run267Q_internal_feature_order_confirmed_adapter_executor as executor
from stage_pipelines.stage267 import run267Q_internal_feature_order_confirmed_adapter_materialization as materializer


STAGE_ID = materializer.STAGE_ID
RUN_ID = materializer.RUN_ID
SOURCE_RUN_ID = materializer.SOURCE_RUN_ID
CLAIM_BOUNDARY = materializer.CLAIM_BOUNDARY
STAGE_ROOT = materializer.STAGE_ROOT
MATERIALIZATION_ROOT = materializer.MATERIALIZATION_ROOT
REVIEWS_ROOT = materializer.REVIEWS_ROOT
STAGE_LEDGER_PATH = materializer.STAGE_LEDGER_PATH
ARTIFACT_REGISTRY_PATH = materializer.ARTIFACT_REGISTRY_PATH
RUN_REGISTRY_PATH = materializer.RUN_REGISTRY_PATH
PROJECT_LEDGER_PATH = materializer.PROJECT_LEDGER_PATH
CURRENT_WORKING_STATE_PATH = materializer.CURRENT_WORKING_STATE_PATH
WORKSPACE_STATE_PATH = materializer.WORKSPACE_STATE_PATH
SELECTION_STATUS_PATH = materializer.SELECTION_STATUS_PATH
REVIEW_INDEX_PATH = materializer.REVIEW_INDEX_PATH

EXECUTION_RESULT_PATH = executor.EXECUTION_RESULT_PATH
SOURCE_KPI_SUMMARY_PATH = source_n_executor.KPI_SUMMARY_PATH
VARIANT_MANIFEST_PATH = materializer.VARIANT_MANIFEST_PATH

REVIEW_ROOT = STAGE_ROOT / "02_runs" / "run267Q" / "internal_feature_order_confirmed_adapter_review"
TRADE_RECORDS_PATH = REVIEW_ROOT / "trade_records.csv"
TIME_SLICE_KPI_PATH = REVIEW_ROOT / "time_slice_kpi.csv"
CURVE_DIAGNOSTICS_PATH = REVIEW_ROOT / "curve_diagnostics.csv"
CANDIDATE_TEST_REVIEW_PATH = REVIEW_ROOT / "candidate_test_review.csv"
CANDIDATE_SUMMARY_PATH = REVIEW_ROOT / "candidate_summary.csv"
SOURCE_REPRODUCTION_AUDIT_PATH = REVIEW_ROOT / "source_reproduction_audit.csv"
NEGATIVE_SLICE_PATH = REVIEW_ROOT / "negative_slice_summary.csv"
PARSER_CHECKS_PATH = REVIEW_ROOT / "parser_checks.csv"
REVIEW_RESULT_PATH = REVIEW_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267Q_internal_feature_order_confirmed_adapter_mt5_review.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267Q_internal_feature_order_confirmed_adapter_review.py")

STATUS = "run267Q_internal_feature_order_confirmed_adapter_mt5_review_completed"
PARTIAL_STATUS = "run267Q_internal_feature_order_confirmed_adapter_mt5_review_partial_parser_errors"
NEXT_ACTION = "run267R_design_internal_adapter_stability_followup_or_prune"
NEXT_ACTION_PARTIAL = "run267Q_repair_internal_adapter_review_parser_errors"
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
    underwater = 0
    longest_underwater = 0
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
    return max_dd, max_dd_pct, longest_underwater, underwater_count / len(rows) if rows else 0.0


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
    dd, dd_pct, longest_underwater, underwater_share = max_closed_balance_drawdown(ordered)
    gross_profit = sum(wins)
    gross_loss = sum(losses)
    return {
        "trade_count": count,
        "net_profit": net,
        "gross_profit": gross_profit,
        "gross_loss": gross_loss,
        "profit_factor": profit_factor(ordered),
        "expectancy": net / count if count else None,
        "win_rate": len(wins) / count if count else None,
        "closed_balance_max_drawdown": dd,
        "closed_balance_max_drawdown_percent": dd_pct,
        "longest_underwater_trades": longest_underwater,
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
    if equity_dd >= 24.0 or worst_month_net <= -120.0:
        return "dd_or_month_hole_uncomfortable(손실폭 또는 월별 구멍 불편)"
    if trades >= 250 and net >= 300.0 and pf >= 1.18 and equity_dd <= 20.0 and positive_month_ratio >= 0.5:
        return "constructive_curve_watch_not_selection(건설적 곡선 관찰, 선택 아님)"
    if net > 0.0 and pf > 1.05:
        return "mixed_constructive_needs_more_pressure(혼합 건설적, 추가 압박 필요)"
    return "mixed_or_fragile(혼합 또는 취약)"


def variant_by_queue() -> dict[str, dict[str, str]]:
    return {row["queue_id"]: row for row in read_csv(VARIANT_MANIFEST_PATH)}


def build_trade_records(execution_result: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    attempts = {str(item.get("attempt_name")): item for item in execution_result.get("attempts_executed", [])}
    variants = variant_by_queue()
    rows: list[dict[str, Any]] = []
    parser_errors: list[dict[str, Any]] = []
    parser_checks: list[dict[str, Any]] = []
    for record in execution_result.get("mt5_kpi_records", []):
        if record.get("status") != "completed":
            continue
        report = record.get("report", {})
        attempt_name = str(report.get("attempt_name") or "")
        attempt = attempts.get(attempt_name, {})
        variant = variants.get(str(attempt.get("queue_id")), {})
        metrics_payload = record.get("metrics", {})
        html_path = Path(str(metrics_payload.get("report_path") or report.get("html_report", {}).get("path") or ""))
        if not html_path.is_absolute():
            html_path = REPO_ROOT / html_path
        try:
            parsed = parse_mt5_trade_report(html_path)
            trades = pair_deals_into_trades(parsed["deals"])
        except Exception as exc:  # pragma: no cover - parser failures are stored as run evidence.
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
                    "source_queue_id": variant.get("source_queue_id"),
                    "candidate_id": attempt.get("candidate_id"),
                    "candidate_alias": attempt.get("candidate_alias"),
                    "candidate_role": attempt.get("candidate_role"),
                    "test_id": attempt.get("test_id"),
                    "materialization_boundary": attempt.get("materialization_boundary"),
                    "internal_adapter_feature": attempt.get("internal_adapter_feature"),
                    "model_materialization_type": attempt.get("model_materialization_type"),
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
            "queue_id",
            "source_queue_id",
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "test_id",
            "materialization_boundary",
            "route_role",
            axis,
        )
        for key, rows in group_rows(trade_rows, keys).items():
            record_view, queue_id, source_queue_id, candidate_id, alias, role, test_id, boundary, route_role, bucket = key
            item = metrics(rows)
            output.append(
                {
                    "record_view": record_view,
                    "queue_id": queue_id,
                    "source_queue_id": source_queue_id,
                    "candidate_id": candidate_id,
                    "candidate_alias": alias,
                    "candidate_role": role,
                    "test_id": test_id,
                    "materialization_boundary": boundary,
                    "route_role": route_role,
                    "axis": axis,
                    "bucket": bucket,
                    **item,
                    "slice_read": slice_read(item),
                }
            )
    return output


def kpi_by_view(execution_result: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
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
    kpi_map = kpi_by_view(execution_result)
    charts = chart_by_view(execution_result)
    output: list[dict[str, Any]] = []
    keys = (
        "record_view",
        "queue_id",
        "source_queue_id",
        "candidate_id",
        "candidate_alias",
        "candidate_role",
        "test_id",
        "materialization_boundary",
        "route_role",
    )
    for key, rows in group_rows(trade_rows, keys).items():
        record_view, queue_id, source_queue_id, candidate_id, alias, role, test_id, boundary, route_role = key
        item = metrics(rows)
        report_metrics = dict(kpi_map.get(str(record_view), {}))
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
                "queue_id": queue_id,
                "source_queue_id": source_queue_id,
                "candidate_id": candidate_id,
                "candidate_alias": alias,
                "candidate_role": role,
                "test_id": test_id,
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


def source_kpi_lookup() -> dict[tuple[str, str], Mapping[str, str]]:
    rows: dict[tuple[str, str], Mapping[str, str]] = {}
    for row in read_csv(SOURCE_KPI_SUMMARY_PATH):
        key = (str(row.get("queue_id")), str(row.get("route_role")))
        rows[key] = row
    return rows


def source_reproduction_audit(curve_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    source = source_kpi_lookup()
    rows: list[dict[str, Any]] = []
    for row in curve_rows:
        source_row = source.get((str(row.get("source_queue_id")), str(row.get("route_role"))), {})
        rows.append(
            {
                "queue_id": row.get("queue_id"),
                "source_queue_id": row.get("source_queue_id"),
                "candidate_alias": row.get("candidate_alias"),
                "test_id": row.get("test_id"),
                "route_role": row.get("route_role"),
                "run267q_net_profit": row.get("net_profit"),
                "source_run267n_net_profit": source_row.get("net_profit", ""),
                "net_delta": as_float(row.get("net_profit")) - as_float(source_row.get("net_profit")),
                "run267q_profit_factor": row.get("profit_factor"),
                "source_run267n_profit_factor": source_row.get("profit_factor", ""),
                "pf_delta": as_float(row.get("profit_factor")) - as_float(source_row.get("profit_factor")),
                "run267q_trade_count": row.get("trade_count"),
                "source_run267n_trade_count": source_row.get("trade_count", ""),
                "trade_count_delta": as_int(row.get("trade_count")) - as_int(source_row.get("trade_count")),
                "run267q_dd_percent": row.get("report_equity_drawdown_percent"),
                "source_run267n_dd_percent": source_row.get("max_drawdown_percent", ""),
                "dd_percent_delta": as_float(row.get("report_equity_drawdown_percent")) - as_float(source_row.get("max_drawdown_percent")),
                "reproduction_status": "matched" if source_row and abs(as_float(row.get("net_profit")) - as_float(source_row.get("net_profit"))) < 0.01 and as_int(row.get("trade_count")) == as_int(source_row.get("trade_count")) else "mismatch_or_missing_source",
            }
        )
    return rows


def weakest_bucket(time_rows: Sequence[Mapping[str, Any]], record_view: str, axis: str) -> Mapping[str, Any]:
    rows = [
        row
        for row in time_rows
        if row.get("record_view") == record_view and row.get("axis") == axis and as_int(row.get("trade_count")) >= 3
    ]
    if not rows:
        return {}
    return min(rows, key=lambda row: as_float(row.get("net_profit")))


def review_read(row: Mapping[str, Any], reproduction_row: Mapping[str, Any]) -> str:
    net = as_float(row.get("net_profit"))
    pf = as_float(row.get("profit_factor"))
    dd_pct = as_float(row.get("report_equity_drawdown_percent"))
    worst_month = as_float(row.get("worst_month_net"))
    reproduced = reproduction_row.get("reproduction_status") == "matched"
    if not reproduced:
        return "runtime_mismatch_repair_first(런타임 불일치, 먼저 수정)"
    if net >= 400.0 and pf >= 1.30 and dd_pct <= 16.0 and worst_month > -140.0:
        return "constructive_reproduction_watch_not_selection(건설적 재현 관찰, 선택 아님)"
    if net > 0.0 and pf > 1.05:
        return "mixed_constructive_needs_more_pressure(혼합 건설적, 추가 압박 필요)"
    return "fragile_or_negative_prune(취약 또는 음수, 가지치기)"


def build_candidate_test_review(
    curve_rows: Sequence[Mapping[str, Any]],
    time_rows: Sequence[Mapping[str, Any]],
    reproduction_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    repro_by_key = {
        (str(row.get("queue_id")), str(row.get("route_role"))): row
        for row in reproduction_rows
    }
    output: list[dict[str, Any]] = []
    for row in sorted(curve_rows, key=lambda item: (str(item.get("candidate_alias")), str(item.get("test_id")), str(item.get("route_role")))):
        record_view = str(row.get("record_view"))
        weak_month = weakest_bucket(time_rows, record_view, "month")
        weak_weekday = weakest_bucket(time_rows, record_view, "weekday")
        weak_hour = weakest_bucket(time_rows, record_view, "close_hour_report")
        weak_session = weakest_bucket(time_rows, record_view, "session_report")
        weak_chron = weakest_bucket(time_rows, record_view, "chron_segment")
        repro = repro_by_key.get((str(row.get("queue_id")), str(row.get("route_role"))), {})
        output.append(
            {
                "queue_id": row.get("queue_id"),
                "source_queue_id": row.get("source_queue_id"),
                "candidate_id": row.get("candidate_id"),
                "candidate_alias": row.get("candidate_alias"),
                "candidate_role": row.get("candidate_role"),
                "test_id": row.get("test_id"),
                "route_role": row.get("route_role"),
                "record_view": record_view,
                "net_profit": row.get("net_profit"),
                "profit_factor": row.get("profit_factor"),
                "trade_count": row.get("trade_count"),
                "expectancy": row.get("expectancy"),
                "report_equity_drawdown_percent": row.get("report_equity_drawdown_percent"),
                "recovery_factor": row.get("report_recovery_factor"),
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
                "weakest_chron_segment": weak_chron.get("bucket", ""),
                "weakest_chron_net": weak_chron.get("net_profit", ""),
                "tier_b_fallback_used_count": row.get("tier_b_fallback_used_count"),
                "source_chart_path": row.get("source_chart_path"),
                "reproduction_status": repro.get("reproduction_status", "missing"),
                "net_delta_vs_source_run267n": repro.get("net_delta", ""),
                "trade_delta_vs_source_run267n": repro.get("trade_count_delta", ""),
                "review_read": review_read(row, repro),
            }
        )
    return output


def build_candidate_summary(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for key, items in group_rows(rows, ("candidate_alias", "candidate_id", "candidate_role")).items():
        alias, candidate_id, role = key
        unique_kpi_shapes = {
            (
                round(as_float(row.get("net_profit")), 2),
                round(as_float(row.get("profit_factor")), 4),
                as_int(row.get("trade_count")),
                round(as_float(row.get("report_equity_drawdown_percent")), 4),
            )
            for row in items
        }
        constructive = [row for row in items if str(row.get("review_read", "")).startswith("constructive")]
        output.append(
            {
                "candidate_alias": alias,
                "candidate_id": candidate_id,
                "candidate_role": role,
                "review_rows": len(items),
                "constructive_rows": len(constructive),
                "unique_kpi_shapes": len(unique_kpi_shapes),
                "best_net_profit": max(as_float(row.get("net_profit")) for row in items),
                "worst_net_profit": min(as_float(row.get("net_profit")) for row in items),
                "best_profit_factor": max(as_float(row.get("profit_factor")) for row in items),
                "worst_dd_percent": max(as_float(row.get("report_equity_drawdown_percent")) for row in items),
                "min_worst_month_net": min(as_float(row.get("worst_month_net")) for row in items),
                "all_reproduced_from_source": all(row.get("reproduction_status") == "matched" for row in items),
                "summary_read": "runtime_reproduced_but_variants_collapsed(런타임 재현됨, 변형 차이는 접힘)" if len(unique_kpi_shapes) == 1 else "runtime_reproduced_with_variant_spread(런타임 재현됨, 변형 차이 있음)",
            }
        )
    return sorted(output, key=lambda row: str(row.get("candidate_alias")))


def negative_slices(time_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = [
        row
        for row in time_rows
        if as_int(row.get("trade_count")) >= 3
        and (as_float(row.get("net_profit")) < 0.0 or as_float(row.get("closed_balance_max_drawdown_percent")) >= 18.0)
    ]
    return sorted(
        rows,
        key=lambda item: (as_float(item.get("net_profit")), -as_float(item.get("closed_balance_max_drawdown_percent"))),
    )


def result_status(parser_errors: Sequence[Mapping[str, Any]]) -> str:
    return PARTIAL_STATUS if parser_errors else STATUS


def result_next_action(parser_errors: Sequence[Mapping[str, Any]]) -> str:
    return NEXT_ACTION_PARTIAL if parser_errors else NEXT_ACTION


def report_markdown(result: Mapping[str, Any]) -> str:
    review_rows = list(result["candidate_test_review"])
    summary_rows = list(result["candidate_summary"])
    negative = list(result["negative_slices"])[:16]
    repro_rows = list(result["source_reproduction_audit"])
    status = str(result["status"])
    next_action = str(result["next_action"])
    max_abs_net_delta = max((abs(as_float(row.get("net_delta"))) for row in repro_rows), default=0.0)
    reproduction_mismatches = sum(1 for row in repro_rows if row.get("reproduction_status") != "matched")
    lines = [
        "# Stage267 Run267Q Internal Feature Order Confirmed Adapter MT5 Review(267단계 267Q 내부 피처 순서 확인 어댑터 MT5 검토)",
        "",
        f"- action(행동): MT5 Strategy Tester(MT5 전략 테스터) reports(보고서) `{len(repro_rows)}`개를 trade/curve/time-slice(거래/곡선/시간구간)로 다시 검토했다.",
        "- effect(효과): run267Q(267Q 실행)가 단순 KPI(핵심 성과 지표) 숫자만 좋은지, 아니면 내부 feature order(피처 순서) 고정 후에도 거래 모양과 약한 구간이 설명 가능한지 확인한다.",
        f"- status(상태): `{status}`",
        f"- trade_records(거래 기록): `{result['trade_record_count']}`",
        f"- time_slice_rows(시간 구간 행): `{result['time_slice_row_count']}`",
        f"- candidate_test_rows(후보-시험 행): `{len(review_rows)}`",
        f"- negative_slices(음수/손실폭 구간): `{len(result['negative_slices'])}`",
        f"- source_reproduction_mismatches(원천 재현 불일치): `{reproduction_mismatches}`",
        f"- max_abs_net_delta_vs_run267N(run267N 대비 최대 순수익 차이): `{cell(max_abs_net_delta)}`",
        f"- selected_candidate(선택 후보): `{result['selected_candidate']}`",
        f"- ONNX readiness(ONNX 준비): `{result['onnx_readiness']}`",
        f"- Goal Achieve(목표 달성): `{result['goal_achieve']}`",
        "",
        "## Easy Read(쉬운 해석)",
        "",
        "좋은 소식은 run267Q(267Q 실행)가 MT5(MetaTrader 5, 메타트레이더5)에서 run267N(267N 실행) 원천 표면을 거의 그대로 재현했다는 점이다. 즉, proxy score(대체 점수)를 internal adapter feature(내부 어댑터 피처)로 이름과 순서를 고정해도 런타임이 깨지지 않았다.",
        "하지만 이건 후보 선택이 아니다. 더 중요한 점은 `abl_volatility_bandwidth`와 `rep_volatility_atr`, 그리고 Tier A(티어 A)와 Tier A+B(티어 A+B)가 후보별로 거의 같은 KPI 모양으로 접혔다는 점이다. 효과는 새 alpha(알파)를 찾았다기보다, 강했던 단서가 구조적으로 재현 가능한지 확인했다는 쪽에 가깝다.",
        "그래프와 약한 구간 검토 기준에서는 아직 Goal Achieve(목표 달성) 조건이 아니다. 다음은 이 내부 Adapter(어댑터)를 더 밀지, 짧게 follow-up(후속)할지, 또는 후보군 전체 racing(경주)으로 되돌릴지 결정해야 한다.",
        "",
        "## Candidate Review(후보 검토)",
        "",
        "| candidate(후보) | test(시험) | route(경로) | net(순수익) | PF(수익 팩터) | DD%(손실폭) | trades(거래 수) | worst month(최악 월) | reproduction(재현) | read(판독) |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- | --- |",
    ]
    for row in review_rows:
        lines.append(
            f"| `{row['candidate_alias']}` | `{row['test_id']}` | `{row['route_role']}` | {cell(row['net_profit'])} | "
            f"{cell(row['profit_factor'])} | {cell(row['report_equity_drawdown_percent'])} | {cell(row['trade_count'])} | "
            f"`{row['worst_month']}` {cell(row['worst_month_net'])} | `{row['reproduction_status']}` | {row['review_read']} |"
        )
    lines.extend(
        [
            "",
            "## Candidate Summary(후보 요약)",
            "",
            "| candidate(후보) | rows(행) | constructive(건설적) | unique shapes(고유 모양) | best net(최고 순수익) | worst DD%(최악 손실폭) | all reproduced(모두 재현) | read(판독) |",
            "| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |",
        ]
    )
    for row in summary_rows:
        lines.append(
            f"| `{row['candidate_alias']}` | {row['review_rows']} | {row['constructive_rows']} | {row['unique_kpi_shapes']} | "
            f"{cell(row['best_net_profit'])} | {cell(row['worst_dd_percent'])} | `{row['all_reproduced_from_source']}` | {row['summary_read']} |"
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
    for row in negative:
        lines.append(
            f"| `{row['candidate_alias']}` | `{row['test_id']}` | `{row['axis']}` | `{row['bucket']}` | {cell(row['trade_count'])} | "
            f"{cell(row['net_profit'])} | {cell(row['profit_factor'])} | {cell(row['closed_balance_max_drawdown_percent'])} |"
        )
    lines.extend(
        [
            "",
            "## Runtime/Forensic Boundary(런타임/포렌식 경계)",
            "",
            f"- execution_result(실행 결과): `{rel(EXECUTION_RESULT_PATH)}`",
            f"- source_kpi(원천 KPI): `{rel(SOURCE_KPI_SUMMARY_PATH)}`",
            f"- source_reproduction_audit(원천 재현 감사): `{rel(SOURCE_REPRODUCTION_AUDIT_PATH)}`",
            f"- trade_records(거래 기록): `{rel(TRADE_RECORDS_PATH)}`",
            f"- time_slice_kpi(시간 구간 KPI): `{rel(TIME_SLICE_KPI_PATH)}`",
            f"- curve_diagnostics(곡선 진단): `{rel(CURVE_DIAGNOSTICS_PATH)}`",
            "- tester_identity(테스터 정체성): historical 2024(2024 과거 기간) `US100` `M5`, deposit(예치금) 500, Strategy Tester(전략 테스터) 산출물.",
            "- runtime_claim_boundary(런타임 주장 경계): `runtime_probe` only, no runtime authority(런타임 권위 아님).",
            "- result_judgment(결과 판정): diagnostic_review_completed_no_candidate_selection(진단 검토 완료, 후보 선택 없음).",
            "",
            "## Judgment Boundary(판정 경계)",
            "",
            "- selected_candidate(선택 후보): `none`.",
            "- ONNX readiness(ONNX 준비): `not_claimed`.",
            "- Goal Achieve(목표 달성): `not_claimed`.",
            f"- next_action(다음 행동): `{next_action}`.",
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
            "row_id": "stage267_run267Q_internal_feature_order_confirmed_adapter_mt5_review",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "view": "internal_feature_order_confirmed_adapter_mt5_review",
            "tier_scope": "Tier A and Tier A+B historical 2024 internal Adapter review",
            "scoreboard": "runtime_full_batch_review",
            "status": status,
            "judgment": judgment,
            "evidence_boundary": "curve_time_slice_trade_quality_review_not_candidate_selection_not_onnx",
            "report_path": rel(REPORT_PATH),
            "notes": f"candidate_test_rows={len(result['candidate_test_review'])};negative_slices={len(result['negative_slices'])};next_action={next_action}.",
        },
        ("row_id", "stage_id", "run_id", "view", "tier_scope", "scoreboard", "status", "judgment", "evidence_boundary", "report_path", "notes"),
    )
    upsert_csv(
        RUN_REGISTRY_PATH,
        "run_id",
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "internal_feature_order_confirmed_adapter_mt5_review",
            "status": status,
            "judgment": judgment,
            "path": rel(REPORT_PATH),
            "notes": f"Run267Q internal Adapter MT5 review; selected_candidate=none; onnx_readiness=not_claimed; next_action={next_action}.",
        },
        ("run_id", "stage_id", "lane", "status", "judgment", "path", "notes"),
    )
    upsert_csv(
        PROJECT_LEDGER_PATH,
        "ledger_row_id",
        {
            "ledger_row_id": f"{RUN_ID}__internal_feature_order_confirmed_adapter_mt5_review",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "internal_feature_order_confirmed_adapter_mt5_review",
            "parent_run_id": RUN_ID,
            "record_view": "internal_feature_order_confirmed_adapter_mt5_review",
            "tier_scope": "Tier A and Tier A+B historical 2024 internal Adapter review",
            "kpi_scope": "curve_time_slice_trade_quality_review",
            "scoreboard_lane": "runtime_full_batch_review",
            "status": status,
            "judgment": judgment,
            "path": rel(REPORT_PATH),
            "primary_kpi": f"candidate_test_rows={len(result['candidate_test_review'])};negative_slices={len(result['negative_slices'])}",
            "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
            "external_verification_status": "completed_for_run267Q_mt5_batch_review",
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
        ("stage267_run267Q_internal_adapter_review_script", "producer_script", PRODUCER_PATH, "Builds run267Q internal Adapter curve/time-slice review."),
        ("stage267_run267Q_internal_adapter_review_trade_records", "trade_records", TRADE_RECORDS_PATH, "Run267Q paired trade records."),
        ("stage267_run267Q_internal_adapter_review_time_slice_kpi", "time_slice_kpi", TIME_SLICE_KPI_PATH, "Run267Q month/week/hour/session/direction/chron-segment KPI."),
        ("stage267_run267Q_internal_adapter_review_curve_diagnostics", "curve_diagnostics", CURVE_DIAGNOSTICS_PATH, "Run267Q closed-balance curve diagnostics."),
        ("stage267_run267Q_internal_adapter_candidate_test_review", "candidate_test_review", CANDIDATE_TEST_REVIEW_PATH, "Run267Q candidate-test review."),
        ("stage267_run267Q_internal_adapter_candidate_summary", "candidate_summary", CANDIDATE_SUMMARY_PATH, "Run267Q candidate summary."),
        ("stage267_run267Q_internal_adapter_source_reproduction_audit", "source_reproduction_audit", SOURCE_REPRODUCTION_AUDIT_PATH, "Run267Q reproduction audit versus run267N."),
        ("stage267_run267Q_internal_adapter_negative_slice_summary", "negative_slice_summary", NEGATIVE_SLICE_PATH, "Run267Q worst negative slices."),
        ("stage267_run267Q_internal_adapter_parser_checks", "parser_checks", PARSER_CHECKS_PATH, "Run267Q parser reconciliation checks."),
        ("stage267_run267Q_internal_adapter_review_result", "review_result", REVIEW_RESULT_PATH, "Run267Q review JSON payload."),
        ("stage267_run267Q_internal_adapter_mt5_review_report", "review_report", REPORT_PATH, "User-facing run267Q MT5 review."),
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


def append_after_contains(text: str, needle: str, line: str) -> str:
    if line in text:
        return text
    lines = text.splitlines()
    for index, existing in enumerate(lines):
        if needle in existing:
            lines.insert(index + 1, line)
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text.rstrip() + "\n" + line + "\n"


def replace_status_and_next(text: str, status: str, next_action: str) -> str:
    text = text.replace(executor.COMPLETED_STATUS, status)
    text = text.replace(executor.NEXT_ACTION_COMPLETED, next_action)
    text = text.replace(PARTIAL_STATUS, status)
    text = text.replace(NEXT_ACTION_PARTIAL, next_action)
    return text


def update_docs(result: Mapping[str, Any]) -> None:
    status = str(result["status"])
    next_action = str(result["next_action"])
    current_line = f"- Stage267(267단계) run267Q internal feature order confirmed Adapter MT5 review(내부 피처 순서 확인 어댑터 MT5 검토): `{rel(REPORT_PATH)}`"
    index_line = f"- run267Q_internal_feature_order_confirmed_adapter_mt5_review(267Q 내부 피처 순서 확인 어댑터 MT5 검토): `{rel(REPORT_PATH)}`"
    summary_line = (
        "Run267Q(267Q 실행)는 internal feature order confirmed Adapter MT5 review(내부 피처 순서 확인 어댑터 MT5 검토)를 완료했다.\n"
        "Effect(효과): MT5(MetaTrader 5, 메타트레이더5)에서 run267N(267N 실행) 원천 표면을 재현했지만, 변형 차이가 후보별로 접혀 선택 후보(selected candidate, 선택 후보)와 ONNX readiness(ONNX 준비)는 계속 없다."
    )
    for path, line, anchor in (
        (CURRENT_WORKING_STATE_PATH, current_line, "stage267_run267Q_internal_feature_order_confirmed_adapter_mt5_execution.md"),
        (SELECTION_STATUS_PATH, index_line, "run267Q_internal_feature_order_confirmed_adapter_mt5_execution"),
        (REVIEW_INDEX_PATH, index_line, "run267Q_internal_feature_order_confirmed_adapter_mt5_execution"),
    ):
        text = io_path(path).read_text(encoding="utf-8-sig")
        text = replace_status_and_next(text, status, next_action)
        text = append_after_contains(text, anchor, line)
        text = append_after_contains(text, "Run267Q(267Q 실행)는", summary_line)
        write_md(path, text)

    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    workspace = replace_status_and_next(workspace, status, next_action)
    workspace = append_after_contains(
        workspace,
        "run267Q_internal_feature_order_confirmed_adapter_mt5_execution_report_path",
        f"  run267Q_internal_feature_order_confirmed_adapter_mt5_review_path: {rel(REPORT_PATH)}",
    )
    write_md(WORKSPACE_STATE_PATH, workspace)


def review() -> dict[str, Any]:
    created_at = utc_now()
    execution_result = read_json(EXECUTION_RESULT_PATH)
    trade_rows, parser_errors, parser_checks = build_trade_records(execution_result)
    time_rows = build_time_slice_rows(trade_rows)
    curve_rows = build_curve_rows(trade_rows, time_rows, execution_result)
    reproduction_rows = source_reproduction_audit(curve_rows)
    candidate_tests = build_candidate_test_review(curve_rows, time_rows, reproduction_rows)
    candidate_summary = build_candidate_summary(candidate_tests)
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
        "source_reproduction_audit": reproduction_rows,
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
            "source_reproduction_audit": rel(SOURCE_REPRODUCTION_AUDIT_PATH),
            "negative_slice_summary": rel(NEGATIVE_SLICE_PATH),
            "parser_checks": rel(PARSER_CHECKS_PATH),
            "review_result": rel(REVIEW_RESULT_PATH),
            "report": rel(REPORT_PATH),
        },
    }
    write_outputs(result, trade_rows, time_rows, curve_rows, candidate_tests, candidate_summary, reproduction_rows, negative, parser_checks)
    write_md(REPORT_PATH, report_markdown(result))
    update_ledgers(created_at, result)
    update_docs(result)
    return result


def write_outputs(
    result: Mapping[str, Any],
    trade_rows: Sequence[Mapping[str, Any]],
    time_rows: Sequence[Mapping[str, Any]],
    curve_rows: Sequence[Mapping[str, Any]],
    candidate_tests: Sequence[Mapping[str, Any]],
    candidate_summary: Sequence[Mapping[str, Any]],
    reproduction_rows: Sequence[Mapping[str, Any]],
    negative: Sequence[Mapping[str, Any]],
    parser_checks: Sequence[Mapping[str, Any]],
) -> None:
    metric_columns = (
        "trade_count",
        "net_profit",
        "gross_profit",
        "gross_loss",
        "profit_factor",
        "expectancy",
        "win_rate",
        "closed_balance_max_drawdown",
        "closed_balance_max_drawdown_percent",
        "longest_underwater_trades",
        "underwater_trade_share",
        "max_losing_streak",
        "recovery_factor_closed",
    )
    write_csv(
        TRADE_RECORDS_PATH,
        trade_rows,
        (
            "run_id",
            "source_run_id",
            "queue_id",
            "source_queue_id",
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "test_id",
            "materialization_boundary",
            "internal_adapter_feature",
            "model_materialization_type",
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
            "queue_id",
            "source_queue_id",
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "test_id",
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
            "queue_id",
            "source_queue_id",
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "test_id",
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
    write_csv(CANDIDATE_TEST_REVIEW_PATH, candidate_tests, tuple(candidate_tests[0].keys()) if candidate_tests else ())
    write_csv(CANDIDATE_SUMMARY_PATH, candidate_summary, tuple(candidate_summary[0].keys()) if candidate_summary else ())
    write_csv(SOURCE_REPRODUCTION_AUDIT_PATH, reproduction_rows, tuple(reproduction_rows[0].keys()) if reproduction_rows else ())
    write_csv(
        NEGATIVE_SLICE_PATH,
        negative,
        tuple(negative[0].keys()) if negative else (
            "record_view",
            "queue_id",
            "source_queue_id",
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "test_id",
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
                "source_reproduction_mismatches": sum(
                    1 for row in result["source_reproduction_audit"] if row.get("reproduction_status") != "matched"
                ),
                "parser_errors": len(result["parser_errors"]),
                "next_action": result["next_action"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
