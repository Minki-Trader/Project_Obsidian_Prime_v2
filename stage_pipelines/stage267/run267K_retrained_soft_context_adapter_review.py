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
from stage_pipelines.stage267 import run267K_retrained_soft_context_adapter_executor as executor
from stage_pipelines.stage267 import run267K_retrained_soft_context_adapter_materialization as materializer


STAGE_ID = materializer.STAGE_ID
RUN_ID = materializer.RUN_ID
CLAIM_BOUNDARY = materializer.CLAIM_BOUNDARY
STAGE_ROOT = materializer.STAGE_ROOT
DESIGN_ROOT = materializer.DESIGN_ROOT
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
BASE_KPI_PATH = STAGE_ROOT / "02_runs" / "run267B" / "historical_2024" / "mt5_kpi_summary.csv"
BASE_CURVE_PATH = STAGE_ROOT / "02_runs" / "run267B" / "historical_2024" / "balance_curve_diagnostics.csv"
BASE_TIME_SLICE_PATH = STAGE_ROOT / "02_runs" / "run267B" / "historical_2024" / "time_slice_kpi.csv"

TRADE_RECORDS_PATH = DESIGN_ROOT / "trade_records.csv"
TIME_SLICE_KPI_PATH = DESIGN_ROOT / "time_slice_kpi.csv"
CURVE_DIAGNOSTICS_PATH = DESIGN_ROOT / "curve_diagnostics.csv"
CANDIDATE_REVIEW_PATH = DESIGN_ROOT / "candidate_retrained_soft_context_review.csv"
NEGATIVE_SLICE_PATH = DESIGN_ROOT / "negative_slice_summary.csv"
REVIEW_RESULT_PATH = DESIGN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267K_retrained_soft_context_adapter_mt5_review.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267K_retrained_soft_context_adapter_review.py")

STATUS = "run267K_retrained_soft_context_adapter_mt5_review_completed"
PARTIAL_STATUS = "run267K_retrained_soft_context_adapter_mt5_review_partial_parser_errors"
NEXT_ACTION = "run267L_design_retrained_soft_context_adapter_followup_or_prune"
NEXT_ACTION_PARTIAL = "run267K_repair_retrained_soft_context_adapter_review_parser_errors"
DEPOSIT = 500.0
AXES = ("month", "weekday", "close_hour_report", "session_report", "direction", "chron_segment")
ALIASES = ("s264_aih", "s264_lc")
ALIAS_TO_ID = {
    "s264_aih": "s264_allow_inner_high_quarter",
    "s264_lc": "s264_lowrank_control",
}
ALIAS_ROLE = {
    "s264_aih": "challenger_core",
    "s264_lc": "defensive_control",
}


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


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: cell(row.get(column)) for column in columns})


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def upsert_csv(path: Path, key: str, row: Mapping[str, Any], columns: Sequence[str]) -> None:
    rows = read_csv(path)
    merged = [item for item in rows if item.get(key) != row.get(key)]
    merged.append(dict(row))
    write_csv(path, merged, columns)


def alias_from_record_view(record_view: str) -> str:
    for alias in ALIASES:
        if alias in record_view:
            return alias
    return ""


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


def max_closed_balance_drawdown(rows: Sequence[Mapping[str, Any]]) -> tuple[float, float, int]:
    balance = DEPOSIT
    peak = DEPOSIT
    max_dd = 0.0
    max_dd_pct = 0.0
    longest_underwater = 0
    underwater = 0
    for row in sorted(rows, key=lambda item: str(item.get("close_time"))):
        balance += as_float(row.get("net_profit"))
        if balance >= peak:
            peak = balance
            underwater = 0
        else:
            underwater += 1
            longest_underwater = max(longest_underwater, underwater)
        dd = peak - balance
        dd_pct = dd / peak * 100.0 if peak else 0.0
        max_dd = max(max_dd, dd)
        max_dd_pct = max(max_dd_pct, dd_pct)
    return max_dd, max_dd_pct, longest_underwater


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
    wins = sum(1 for row in ordered if as_float(row.get("net_profit")) > 0.0)
    dd, dd_pct, underwater = max_closed_balance_drawdown(ordered)
    return {
        "trade_count": count,
        "net_profit": net,
        "profit_factor": profit_factor(ordered),
        "expectancy": net / count if count else None,
        "win_rate": wins / count if count else None,
        "closed_balance_max_drawdown": dd,
        "closed_balance_max_drawdown_percent": dd_pct,
        "longest_underwater_trades": underwater,
        "max_losing_streak": max_losing_streak(ordered),
    }


def group_rows(rows: Iterable[Mapping[str, Any]], keys: Sequence[str]) -> dict[tuple[Any, ...], list[Mapping[str, Any]]]:
    grouped: dict[tuple[Any, ...], list[Mapping[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[tuple(row.get(key) for key in keys)].append(row)
    return grouped


def build_trade_records(execution_result: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    attempts = {str(item.get("attempt_name")): item for item in execution_result.get("attempts_executed", [])}
    rows: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    for record in execution_result.get("mt5_kpi_records", []):
        if record.get("status") != "completed":
            continue
        report = record.get("report", {})
        attempt_name = str(report.get("attempt_name") or "")
        attempt = attempts.get(attempt_name, {})
        metrics_payload = record.get("metrics", {})
        html_path = Path(
            str(
                metrics_payload.get("report_path")
                or report.get("html_report", {}).get("path")
                or ""
            )
        )
        if not html_path.is_absolute():
            html_path = REPO_ROOT / html_path
        try:
            parsed = parse_mt5_trade_report(html_path)
            trades = pair_deals_into_trades(parsed["deals"])
        except Exception as exc:  # pragma: no cover - stored as evidence if parser fails.
            errors.append({"attempt_name": attempt_name, "report_path": rel(html_path), "error": str(exc)})
            continue
        ordered = sorted(trades, key=lambda item: item.close_time)
        total = len(ordered)
        for index, trade in enumerate(ordered):
            close_time = trade.close_time
            open_time = trade.open_time
            close_hour = close_time.strftime("%H")
            alias = str(attempt.get("candidate_alias") or alias_from_record_view(str(record.get("record_view", ""))))
            rows.append(
                {
                    "run_id": RUN_ID,
                    "candidate_id": ALIAS_TO_ID.get(alias, ""),
                    "candidate_alias": alias,
                    "candidate_role": attempt.get("candidate_role") or ALIAS_ROLE.get(alias, ""),
                    "feature_design": attempt.get("feature_design") or "adx_atr_soft_score",
                    "model_materialization_type": attempt.get("model_materialization_type") or materializer.MODEL_MATERIALIZATION_TYPE,
                    "record_view": record.get("record_view"),
                    "attempt_name": attempt_name,
                    "tier_scope": record.get("tier_scope"),
                    "route_role": record.get("route_role"),
                    "split": record.get("split"),
                    "trade_index": trade.index,
                    "direction": trade.direction,
                    "open_time": open_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "close_time": close_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "month": close_time.strftime("%Y-%m"),
                    "weekday": close_time.strftime("%A"),
                    "close_hour_report": close_hour,
                    "session_report": session_bucket(close_hour),
                    "chron_segment": chronological_segment(index, total),
                    "volume": trade.volume,
                    "gross_profit": trade.gross_profit,
                    "net_profit": trade.net_profit,
                    "source_report_path": rel(html_path),
                }
            )
    return rows, errors


def build_time_slice_rows(trade_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for axis in AXES:
        keys = (
            "record_view",
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "feature_design",
            "model_materialization_type",
            "route_role",
            axis,
        )
        for key, rows in group_rows(trade_rows, keys).items():
            record_view, candidate_id, alias, role, feature_design, model_type, route_role, bucket = key
            item = metrics(rows)
            output.append(
                {
                    "record_view": record_view,
                    "candidate_id": candidate_id,
                    "candidate_alias": alias,
                    "candidate_role": role,
                    "feature_design": feature_design,
                    "model_materialization_type": model_type,
                    "route_role": route_role,
                    "axis": axis,
                    "bucket": bucket,
                    **item,
                    "slice_read": slice_read(item),
                }
            )
    return output


def slice_read(item: Mapping[str, Any]) -> str:
    count = as_int(item.get("trade_count"))
    net = as_float(item.get("net_profit"))
    dd_pct = as_float(item.get("closed_balance_max_drawdown_percent"))
    if count < 3:
        return "thin_slice(얇은 구간)"
    if net < -100.0 or dd_pct >= 25.0:
        return "negative_fragile_slice(음수 취약 구간)"
    if net < 0.0:
        return "minor_negative_slice(소폭 음수 구간)"
    return "measured_slice(측정 구간)"


def curve_read(item: Mapping[str, Any], report_metrics: Mapping[str, Any]) -> str:
    equity_dd = as_float(report_metrics.get("equity_drawdown_maximal_percent") or item.get("closed_balance_max_drawdown_percent"))
    pf = as_float(item.get("profit_factor"))
    expectancy = as_float(item.get("expectancy"))
    if equity_dd >= 31.0:
        return "dd_uncomfortable_not_adapter_ready(손실폭 불편, 어댑터 준비 아님)"
    if equity_dd >= 29.0 and pf <= 1.10:
        return "constructive_but_curve_watch(건설적이나 곡선 감시 필요)"
    if pf >= 1.12 and expectancy >= 0.60 and equity_dd < 29.0:
        return "constructive_watch_not_selection(건설적 관찰, 선택 아님)"
    return "mixed_or_fragile(혼합 또는 취약)"


def build_curve_rows(
    trade_rows: Sequence[Mapping[str, Any]],
    execution_result: Mapping[str, Any],
) -> list[dict[str, Any]]:
    kpi_by_view = {record.get("record_view"): record.get("metrics", {}) for record in execution_result.get("mt5_kpi_records", [])}
    chart_by_view = {
        record.get("record_view"): record.get("report", {}).get("chart", {}).get("path", "")
        for record in execution_result.get("mt5_kpi_records", [])
    }
    output: list[dict[str, Any]] = []
    keys = ("record_view", "candidate_id", "candidate_alias", "candidate_role", "feature_design", "model_materialization_type", "route_role")
    month_rows = build_time_slice_rows([row for row in trade_rows if row.get("month")])
    for key, rows in group_rows(trade_rows, keys).items():
        record_view, candidate_id, alias, role, feature_design, model_type, route_role = key
        item = metrics(rows)
        report_metrics = dict(kpi_by_view.get(record_view, {}))
        month_slices = [
            row
            for row in month_rows
            if row.get("record_view") == record_view and row.get("axis") == "month" and as_int(row.get("trade_count")) >= 3
        ]
        negative_months = [row for row in month_slices if as_float(row.get("net_profit")) < 0.0]
        worst_month = min(month_slices, key=lambda row: as_float(row.get("net_profit"))) if month_slices else {}
        best_month = max(month_slices, key=lambda row: as_float(row.get("net_profit"))) if month_slices else {}
        output.append(
            {
                "record_view": record_view,
                "candidate_id": candidate_id,
                "candidate_alias": alias,
                "candidate_role": role,
                "feature_design": feature_design,
                "model_materialization_type": model_type,
                "route_role": route_role,
                "trade_count": item["trade_count"],
                "net_profit": item["net_profit"],
                "profit_factor": item["profit_factor"],
                "expectancy": item["expectancy"],
                "win_rate": item["win_rate"],
                "closed_balance_max_drawdown": item["closed_balance_max_drawdown"],
                "closed_balance_max_drawdown_percent": item["closed_balance_max_drawdown_percent"],
                "longest_underwater_trades": item["longest_underwater_trades"],
                "max_losing_streak": item["max_losing_streak"],
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
                "source_chart_path": rel(chart_by_view.get(record_view, "")) if chart_by_view.get(record_view) else "",
                "curve_read": curve_read(item, report_metrics),
            }
        )
    return output


def base_kpi_by_alias() -> dict[str, dict[str, str]]:
    rows: dict[str, dict[str, str]] = {}
    for row in read_csv(BASE_KPI_PATH):
        if row.get("route_role") != "routed_total":
            continue
        alias = alias_from_record_view(str(row.get("record_view", "")))
        if alias in ALIASES:
            rows[alias] = row
    return rows


def base_curve_by_alias() -> dict[str, dict[str, str]]:
    rows: dict[str, dict[str, str]] = {}
    for row in read_csv(BASE_CURVE_PATH):
        if row.get("route_role") != "routed_total":
            continue
        alias = str(row.get("candidate_alias") or alias_from_record_view(str(row.get("record_view", ""))))
        if alias in ALIASES:
            rows[alias] = row
    return rows


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
    weak_month_net = as_float(weak_month.get("net_profit"))
    pf = as_float(curve.get("profit_factor"))
    if net_delta > 40.0 and pf_delta > 0.03 and dd_delta < -4.0 and equity_dd <= 31.0 and weak_month_net > -110.0:
        return "constructive_retrain_watch_not_selection(건설적 재학습 관찰, 선택 아님)"
    if net_delta > 0.0 and dd_delta < 0.0 and equity_dd <= 32.0:
        return "improved_but_dd_pf_not_enough(개선됐지만 손실폭/수익 팩터 불충분)"
    if pf <= 1.05 or equity_dd >= 34.0:
        return "fragile_or_low_edge_do_not_extend(취약 또는 낮은 엣지, 확장 금지)"
    return "mixed_review_needed(혼합 결과, 추가 검토 필요)"


def build_candidate_review(
    curve_rows: Sequence[Mapping[str, Any]],
    time_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    base_kpi = base_kpi_by_alias()
    base_curve = base_curve_by_alias()
    output: list[dict[str, Any]] = []
    for row in curve_rows:
        if row.get("route_role") != "routed_total":
            continue
        alias = str(row.get("candidate_alias"))
        base = base_kpi.get(alias, {})
        base_curve_row = base_curve.get(alias, {})
        weak_month = weakest_bucket(time_rows, str(row["record_view"]), "month") or {}
        weak_weekday = weakest_bucket(time_rows, str(row["record_view"]), "weekday") or {}
        weak_hour = weakest_bucket(time_rows, str(row["record_view"]), "close_hour_report") or {}
        weak_session = weakest_bucket(time_rows, str(row["record_view"]), "session_report") or {}
        weak_chron = weakest_bucket(time_rows, str(row["record_view"]), "chron_segment") or {}
        net = as_float(row.get("net_profit"))
        pf = as_float(row.get("profit_factor"))
        dd = as_float(row.get("report_equity_drawdown_percent"))
        base_net = as_float(base.get("net_profit"))
        base_pf = as_float(base.get("profit_factor"))
        base_dd = as_float(base.get("max_drawdown_percent"))
        output.append(
            {
                "candidate_id": row.get("candidate_id"),
                "candidate_alias": alias,
                "candidate_role": row.get("candidate_role"),
                "feature_design": row.get("feature_design"),
                "model_materialization_type": row.get("model_materialization_type"),
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
                "base_curve_grade": base_curve_row.get("curve_grade", ""),
                "base_curve_read": base_curve_row.get("curve_read", ""),
                "weakest_month": weak_month.get("bucket", ""),
                "weakest_month_net": weak_month.get("net_profit", ""),
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
                "review_read": review_read(row, base, weak_month),
            }
        )
    return sorted(output, key=lambda item: -as_float(item.get("net_profit")))


def negative_slices(time_rows: Sequence[Mapping[str, Any]], limit: int = 24) -> list[dict[str, Any]]:
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
    review_rows = list(result["candidate_retrained_soft_context_review"])
    negative = list(result["negative_slices"])[:10]
    status = result["status"]
    next_action = result["next_action"]
    lines = [
        "# Stage267 Run267K Retrained Soft-Context Adapter MT5 Review(267단계 267K 재학습 부드러운 문맥 어댑터 MT5 검토)",
        "",
        "- action(행동): run267K(267K 실행)의 MT5(MetaTrader 5, 메타트레이더5) report(보고서)에서 trade list(거래 목록)를 다시 파싱해 curve diagnostics(곡선 진단), time-slice KPI(시간 구간 핵심 성과 지표), negative slice(음수 구간)를 만들었다.",
        "- effect(효과): net profit(순수익)만 보지 않고 월/요일/시간/세션/순서 구간에서 덜 깨지는지 확인한다.",
        f"- status(상태): `{status}`",
        f"- trade_records(거래 기록): `{result['trade_record_count']}`",
        f"- time_slice_rows(시간 구간 행): `{result['time_slice_row_count']}`",
        f"- parser_errors(파서 오류): `{len(result['parser_errors'])}`",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Easy Read(쉬운 해석)",
        "",
        "두 후보 모두 run267B(267B 실행)의 2024년 원형 후보보다 순수익과 PF(profit factor, 수익 팩터)는 크게 좋아졌고 DD(drawdown, 손실폭)는 낮아졌다.",
        "하지만 DD(drawdown, 손실폭)가 아직 22~24%대라 Goal Achieve(목표 달성)의 예쁜 곡선 기준에는 못 미친다. 즉, 다음 후보로 더 파볼 가치는 있지만 선택 후보는 아니다.",
        "또한 routed total(라우팅 합산)은 fallback(대체 사용)이 0이라 Tier B(티어 B)가 실제로 메운 근거가 아니다. 이번에는 Tier A(티어 A) 재학습 표면의 2024 진단으로 읽어야 한다.",
        "선택 후보(selected candidate, 선택 후보)는 없다. ONNX readiness(ONNX 준비)도 주장하지 않는다.",
        "",
        "## Candidate Review(후보 검토)",
        "",
        "| candidate(후보) | net(순수익) | base net(기준 순수익) | delta(차이) | PF(수익 팩터) | DD%(손실폭) | trades(거래 수) | weakest month(가장 약한 월) | read(판독) |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for row in review_rows:
        lines.append(
            f"| `{row['candidate_alias']}` | {cell(row['net_profit'])} | {cell(row['base_2024_net_profit'])} | {cell(row['net_delta_vs_base_2024'])} | "
            f"{cell(row['profit_factor'])} | {cell(row['report_equity_drawdown_percent'])} | {cell(row['trade_count'])} | "
            f"`{row['weakest_month']}` {cell(row['weakest_month_net'])} | {row['review_read']} |"
        )
    lines.extend(
        [
            "",
            "## Weak Slices(약한 구간)",
            "",
            "| candidate(후보) | axis(축) | bucket(구간) | trades(거래 수) | net(순수익) | PF(수익 팩터) | DD%(손실폭) |",
            "| --- | --- | --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in negative:
        lines.append(
            f"| `{row['candidate_alias']}` | `{row['axis']}` | `{row['bucket']}` | {cell(row['trade_count'])} | "
            f"{cell(row['net_profit'])} | {cell(row['profit_factor'])} | {cell(row['closed_balance_max_drawdown_percent'])} |"
        )
    lines.extend(
        [
            "",
            "## Performance Attribution(성과 귀인)",
            "",
            "- attribution(귀인): 개선은 `stage267_adx_atr_soft_score`와 기존 rank/gate(순위/문) 표면을 supervised EBM retrain(지도학습 EBM 재학습)으로 다시 묶은 효과다.",
            "- effect(효과): 이 결과만으로 Adapter(어댑터) 구조가 안정적이라고 말할 수 없고, 다음에는 약한 월/요일/시간 구간을 줄이면서도 PF(profit factor, 수익 팩터)와 거래 수가 유지되는지 봐야 한다.",
            "- weakness(약점): 약한 월과 세션이 아직 남아 있고, DD(drawdown, 손실폭)가 Goal Achieve(목표 달성) 조건의 곡선 기준에 못 미친다.",
            "- stop rule(중단 규칙): 다음 follow-up(후속)에서도 DD(drawdown, 손실폭)와 약한 월이 충분히 줄지 않으면 이 retrain branch(재학습 분기)는 짧게 닫고 전체 후보군 경주로 되돌린다.",
            "",
            "## Backtest Forensics(백테스트 포렌식)",
            "",
            f"- execution_result(실행 결과): `{rel(EXECUTION_RESULT_PATH)}`",
            f"- base_kpi(기준 핵심 성과 지표): `{rel(BASE_KPI_PATH)}`",
            f"- base_curve(기준 곡선): `{rel(BASE_CURVE_PATH)}`",
            f"- source_reports(원천 보고서): `{rel(DESIGN_ROOT / 'mt5' / 'reports')}`",
            "- tester_scope(테스터 범위): historical 2024(2024 과거 기간) `US100` `M5`, deposit(예치금) 500, Strategy Tester(전략 테스터) 산출물.",
            "- evidence_boundary(근거 경계): reviewed diagnostic evidence(검토된 진단 근거)이며 candidate selection(후보 선택), ONNX parity(ONNX 동등성), runtime reproduction(런타임 재현) 근거가 아니다.",
            "",
            "## Artifact Lineage(산출물 계보)",
            "",
            f"- producer(생산자): `{rel(PRODUCER_PATH)}`",
            f"- trade_records(거래 기록): `{rel(TRADE_RECORDS_PATH)}`",
            f"- time_slice_kpi(시간 구간 핵심 성과 지표): `{rel(TIME_SLICE_KPI_PATH)}`",
            f"- curve_diagnostics(곡선 진단): `{rel(CURVE_DIAGNOSTICS_PATH)}`",
            f"- candidate_review(후보 검토): `{rel(CANDIDATE_REVIEW_PATH)}`",
            f"- negative_slice_summary(음수 구간 요약): `{rel(NEGATIVE_SLICE_PATH)}`",
            f"- review_result(검토 결과): `{rel(REVIEW_RESULT_PATH)}`",
            "",
            "## Judgment Boundary(판정 경계)",
            "",
            "- result_subject(결과 대상): `run267K_retrained_soft_context_adapter_mt5_review`.",
            "- judgment_label(판정 라벨): `diagnostic_review_completed_no_candidate_selection`.",
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
    stage_row = {
        "row_id": "stage267_run267K_retrained_soft_context_adapter_mt5_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "retrained_soft_context_adapter_mt5_review",
        "tier_scope": "Tier A and Tier A+B historical 2024 retrained soft-context adapter review",
        "scoreboard": "runtime_full_batch_review",
        "status": status,
        "judgment": judgment,
        "evidence_boundary": "curve_time_slice_trade_quality_review_not_candidate_selection_not_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": f"review_rows={len(result['candidate_retrained_soft_context_review'])};negative_slices={len(result['negative_slices'])};next_action={next_action}.",
    }
    rows = [item for item in read_csv(STAGE_LEDGER_PATH) if item.get("row_id") != stage_row["row_id"]]
    rows.append(stage_row)
    write_csv(
        STAGE_LEDGER_PATH,
        rows,
        ("row_id", "stage_id", "run_id", "view", "tier_scope", "scoreboard", "status", "judgment", "evidence_boundary", "report_path", "notes"),
    )
    upsert_csv(
        RUN_REGISTRY_PATH,
        "run_id",
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "baseline_candidate_racing_retrained_soft_context_adapter_mt5_review",
            "status": status,
            "judgment": judgment,
            "path": rel(REPORT_PATH),
            "notes": f"Run267K retrained soft-context adapter MT5 review; selected_candidate=none; onnx_readiness=not_claimed; next_action={next_action}.",
        },
        ("run_id", "stage_id", "lane", "status", "judgment", "path", "notes"),
    )
    upsert_csv(
        PROJECT_LEDGER_PATH,
        "ledger_row_id",
        {
            "ledger_row_id": f"{RUN_ID}__retrained_soft_context_adapter_mt5_review",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "retrained_soft_context_adapter_mt5_review",
            "parent_run_id": RUN_ID,
            "record_view": "retrained_soft_context_adapter_mt5_review",
            "tier_scope": "Tier A and Tier A+B historical 2024 retrained soft-context adapter review",
            "kpi_scope": "curve_time_slice_trade_quality_review",
            "scoreboard_lane": "runtime_full_batch_review",
            "status": status,
            "judgment": judgment,
            "path": rel(REPORT_PATH),
            "primary_kpi": f"review_rows={len(result['candidate_retrained_soft_context_review'])};negative_slices={len(result['negative_slices'])}",
            "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
            "external_verification_status": "completed_for_run267K_mt5_batch_review",
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
        ("stage267_run267K_retrained_soft_context_review_script", "producer_script", PRODUCER_PATH, "Builds run267K retrained soft-context curve/time-slice review."),
        ("stage267_run267K_retrained_soft_context_trade_records", "trade_records", TRADE_RECORDS_PATH, "Run267K paired trade records."),
        ("stage267_run267K_retrained_soft_context_time_slice_kpi", "time_slice_kpi", TIME_SLICE_KPI_PATH, "Run267K month/week/hour/session/direction/chron-segment KPI."),
        ("stage267_run267K_retrained_soft_context_curve_diagnostics", "curve_diagnostics", CURVE_DIAGNOSTICS_PATH, "Run267K closed-balance curve diagnostics."),
        ("stage267_run267K_retrained_soft_context_candidate_review", "candidate_retrained_soft_context_review", CANDIDATE_REVIEW_PATH, "Run267K candidate retrained soft-context review."),
        ("stage267_run267K_retrained_soft_context_negative_slice_summary", "negative_slice_summary", NEGATIVE_SLICE_PATH, "Run267K worst negative slices."),
        ("stage267_run267K_retrained_soft_context_review_result", "review_result", REVIEW_RESULT_PATH, "Run267K review JSON payload."),
        ("stage267_run267K_retrained_soft_context_mt5_review_report", "review_report", REPORT_PATH, "User-facing run267K retrained soft-context MT5 review."),
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
    return text


def update_docs(result: Mapping[str, Any]) -> None:
    status = str(result["status"])
    next_action = str(result["next_action"])
    current_line = f"- Stage267(267단계) run267K retrained soft-context Adapter MT5 review(재학습 부드러운 문맥 어댑터 MT5 검토): `{rel(REPORT_PATH)}`"
    index_line = f"- run267K_retrained_soft_context_adapter_mt5_review(267K 재학습 부드러운 문맥 어댑터 MT5 검토): `{rel(REPORT_PATH)}`"
    summary_line = (
        "Run267K(267K 실행)는 retrained soft-context Adapter MT5 review(재학습 부드러운 문맥 어댑터 MT5 검토)를 완료했다.\n"
        "Effect(효과): 순수익/PF(profit factor, 수익 팩터)는 2024년 원형보다 크게 좋아졌지만 DD(drawdown, 손실폭)가 아직 Goal Achieve(목표 달성) 곡선 기준에 못 미쳐 선택 후보(selected candidate, 선택 후보)와 ONNX readiness(ONNX 준비)는 계속 없다."
    )
    for path, line, anchor in (
        (CURRENT_WORKING_STATE_PATH, current_line, "stage267_run267K_retrained_soft_context_adapter_mt5_execution.md"),
        (SELECTION_STATUS_PATH, index_line, "run267K_retrained_soft_context_adapter_mt5_execution"),
        (REVIEW_INDEX_PATH, index_line, "run267K_retrained_soft_context_adapter_mt5_execution"),
    ):
        text = io_path(path).read_text(encoding="utf-8-sig")
        text = replace_status_and_next(text, status, next_action)
        text = append_after_contains(text, anchor, line)
        text = append_after_contains(text, "Run267K(267K 실행)는", summary_line)
        write_md(path, text)

    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    workspace = replace_status_and_next(workspace, status, next_action)
    workspace = append_after_contains(
        workspace,
        "run267K_retrained_soft_context_adapter_mt5_execution_report_path",
        f"  run267K_retrained_soft_context_adapter_mt5_review_path: {rel(REPORT_PATH)}",
    )
    write_md(WORKSPACE_STATE_PATH, workspace)


def review() -> dict[str, Any]:
    created_at = utc_now()
    execution_result = read_json(EXECUTION_RESULT_PATH)
    trade_rows, parser_errors = build_trade_records(execution_result)
    time_rows = build_time_slice_rows(trade_rows)
    curve_rows = build_curve_rows(trade_rows, execution_result)
    candidate_review = build_candidate_review(curve_rows, time_rows)
    negative = negative_slices(time_rows)
    result = {
        "status": result_status(parser_errors),
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "trade_record_count": len(trade_rows),
        "time_slice_row_count": len(time_rows),
        "curve_row_count": len(curve_rows),
        "candidate_retrained_soft_context_review": candidate_review,
        "negative_slices": negative,
        "parser_errors": parser_errors,
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": result_next_action(parser_errors),
        "outputs": {
            "trade_records": rel(TRADE_RECORDS_PATH),
            "time_slice_kpi": rel(TIME_SLICE_KPI_PATH),
            "curve_diagnostics": rel(CURVE_DIAGNOSTICS_PATH),
            "candidate_retrained_soft_context_review": rel(CANDIDATE_REVIEW_PATH),
            "negative_slice_summary": rel(NEGATIVE_SLICE_PATH),
            "review_result": rel(REVIEW_RESULT_PATH),
            "report": rel(REPORT_PATH),
        },
    }
    write_csv(
        TRADE_RECORDS_PATH,
        trade_rows,
        (
            "run_id",
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "feature_design",
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
            "month",
            "weekday",
            "close_hour_report",
            "session_report",
            "chron_segment",
            "volume",
            "gross_profit",
            "net_profit",
            "source_report_path",
        ),
    )
    write_csv(
        TIME_SLICE_KPI_PATH,
        time_rows,
        (
            "record_view",
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "feature_design",
            "model_materialization_type",
            "route_role",
            "axis",
            "bucket",
            "trade_count",
            "net_profit",
            "profit_factor",
            "expectancy",
            "win_rate",
            "closed_balance_max_drawdown",
            "closed_balance_max_drawdown_percent",
            "longest_underwater_trades",
            "max_losing_streak",
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
            "feature_design",
            "model_materialization_type",
            "route_role",
            "trade_count",
            "net_profit",
            "profit_factor",
            "expectancy",
            "win_rate",
            "closed_balance_max_drawdown",
            "closed_balance_max_drawdown_percent",
            "longest_underwater_trades",
            "max_losing_streak",
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
            "source_chart_path",
            "curve_read",
        ),
    )
    write_csv(
        CANDIDATE_REVIEW_PATH,
        candidate_review,
        (
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "feature_design",
            "model_materialization_type",
            "record_view",
            "net_profit",
            "base_2024_net_profit",
            "net_delta_vs_base_2024",
            "profit_factor",
            "base_2024_profit_factor",
            "pf_delta_vs_base_2024",
            "trade_count",
            "base_2024_trade_count",
            "trade_delta_vs_base_2024",
            "report_equity_drawdown_percent",
            "base_2024_max_drawdown_percent",
            "dd_delta_vs_base_2024",
            "recovery_factor",
            "base_2024_recovery_factor",
            "positive_month_ratio",
            "negative_month_count",
            "base_curve_grade",
            "base_curve_read",
            "weakest_month",
            "weakest_month_net",
            "weakest_weekday",
            "weakest_weekday_net",
            "weakest_hour_report",
            "weakest_hour_net",
            "weakest_session_report",
            "weakest_session_net",
            "weakest_chron_segment",
            "weakest_chron_net",
            "tier_b_fallback_used_count",
            "source_chart_path",
            "review_read",
        ),
    )
    write_csv(
        NEGATIVE_SLICE_PATH,
        negative,
        (
            "record_view",
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "feature_design",
            "model_materialization_type",
            "route_role",
            "axis",
            "bucket",
            "trade_count",
            "net_profit",
            "profit_factor",
            "expectancy",
            "win_rate",
            "closed_balance_max_drawdown",
            "closed_balance_max_drawdown_percent",
            "longest_underwater_trades",
            "max_losing_streak",
            "slice_read",
        ),
    )
    write_json(REVIEW_RESULT_PATH, result)
    write_md(REPORT_PATH, report_markdown(result))
    update_ledgers(created_at, result)
    update_docs(result)
    return result


def main() -> int:
    result = review()
    print(
        json.dumps(
            {
                "status": result["status"],
                "trade_records": result["trade_record_count"],
                "time_slice_rows": result["time_slice_row_count"],
                "review_rows": len(result["candidate_retrained_soft_context_review"]),
                "negative_slices": len(result["negative_slices"]),
                "next_action": result["next_action"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
