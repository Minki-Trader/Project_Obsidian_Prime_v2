from __future__ import annotations

import csv
import json
import math
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, path_exists
from foundation.mt5.strategy_report import (
    _Mt5ReportTableParser,
    extract_mt5_strategy_report_metrics,
    parse_report_number,
    read_text_best_effort,
)


STAGE_ID = "stage_frontier_67__count_parity_not_pnl_parity_runtime_economics_crosswalk"
RUN_ID = "frontier67C_runtime_native_order_intent_economics_v1"
F66_STAGE_ID = "stage_frontier_66__runtime_probe_backfill_gap_audit_frontier02_to_64"
F66_RUN_ID = "frontier66C_proxy_signal_mt5_backfill_v1"
F66_RUN_ROOT = ROOT / "stages" / F66_STAGE_ID / "02_runs" / F66_RUN_ID
F67_STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = F67_STAGE_ROOT / "02_runs" / RUN_ID
REVIEWS_ROOT = F67_STAGE_ROOT / "03_reviews"

ATTEMPTS_JSON = F66_RUN_ROOT / "frontier66_proxy_signal_mt5_attempts.json"
RUNTIME_ROWS = ROOT / "stages" / F66_STAGE_ID / "03_reviews" / "frontier66_proxy_signal_runtime_rows_review.csv"
F67B_ROWS = REVIEWS_ROOT / "frontier67B_config_parity_rows_review.csv"
EXECUTION_RESULT_JSON = F66_RUN_ROOT / "frontier66_proxy_signal_mt5_execution_result.json"
REPORT_ROOT = F66_RUN_ROOT / "mt5" / "reports"

ROWS_CSV = RUN_ROOT / "frontier67C_runtime_native_order_intent_rows.csv"
SUMMARY_JSON = RUN_ROOT / "frontier67C_runtime_native_order_intent_summary.json"
REPORT_MD = REVIEWS_ROOT / "frontier67C_runtime_native_order_intent_economics_report.md"
REVIEW_ROWS_CSV = REVIEWS_ROOT / "frontier67C_runtime_native_order_intent_rows_review.csv"
REVIEW_SUMMARY_JSON = REVIEWS_ROOT / "frontier67C_runtime_native_order_intent_summary_review.json"

CLAIM_BOUNDARY = (
    "runtime_native_order_intent_observation_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def as_float(value: Any) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    try:
        number = float(text)
    except ValueError:
        return None
    if not math.isfinite(number):
        return None
    return number


def as_int(value: Any) -> int | None:
    number = as_float(value)
    return None if number is None else int(round(number))


def ratio(numerator: float | int | None, denominator: float | int | None) -> float | None:
    if numerator is None or denominator in {None, 0, 0.0}:
        return None
    return float(numerator) / float(denominator)


def key(stage_num: Any, split: Any) -> tuple[str, str]:
    return str(stage_num), str(split)


def attempt_by_name(execution_result: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(row.get("attempt_name")): row
        for row in execution_result.get("execution_results", [])
        if row.get("attempt_name")
    }


def report_path_for_attempt(attempt: dict[str, Any]) -> Path:
    report_name = str(((attempt.get("ini") or {}).get("tester") or {}).get("Report") or "")
    return REPORT_ROOT / f"{report_name}.htm"


def _deal_header(row: list[str]) -> bool:
    labels = set(row)
    return {"커미션", "스왑", "수익"}.issubset(labels) or {"Commission", "Swap", "Profit"}.issubset(labels)


def _deal_value(row: dict[str, str], *keys: str) -> str:
    for key_name in keys:
        if key_name in row:
            return row.get(key_name, "")
    return ""


def extract_deal_metrics(report_path: Path) -> dict[str, Any]:
    text, encoding = read_text_best_effort(report_path)
    parser = _Mt5ReportTableParser()
    parser.feed(text)

    header: list[str] | None = None
    deal_rows: list[dict[str, str]] = []
    for parsed_row in parser.rows:
        if _deal_header(parsed_row):
            header = parsed_row
            continue
        if header is None or len(parsed_row) != len(header):
            continue
        row = dict(zip(header, parsed_row, strict=True))
        deal_type = _deal_value(row, "종류", "Type")
        if deal_type == "balance":
            continue
        if _deal_value(row, "거래", "Deal") and deal_type:
            deal_rows.append(row)

    commission = sum(parse_report_number(_deal_value(row, "커미션", "Commission")) or 0.0 for row in deal_rows)
    swap = sum(parse_report_number(_deal_value(row, "스왑", "Swap")) or 0.0 for row in deal_rows)
    profit = sum(parse_report_number(_deal_value(row, "수익", "Profit")) or 0.0 for row in deal_rows)
    in_count = sum(1 for row in deal_rows if _deal_value(row, "방향", "Direction") == "in")
    out_count = sum(1 for row in deal_rows if _deal_value(row, "방향", "Direction") == "out")
    return {
        "deal_table_encoding": encoding,
        "deal_row_count": len(deal_rows),
        "deal_in_count": in_count,
        "deal_out_count": out_count,
        "deal_commission_sum": commission,
        "deal_swap_sum": swap,
        "deal_profit_sum": profit,
        "deal_cost_sum": commission + swap,
    }


def summarize_numbers(values: Iterable[float | None]) -> dict[str, Any]:
    clean = sorted(float(value) for value in values if value is not None and math.isfinite(float(value)))
    if not clean:
        return {"count": 0}
    return {
        "count": len(clean),
        "min": clean[0],
        "p25": quantile(clean, 0.25),
        "median": statistics.median(clean),
        "p75": quantile(clean, 0.75),
        "max": clean[-1],
    }


def quantile(values: list[float], q: float) -> float | None:
    if not values:
        return None
    if len(values) == 1:
        return values[0]
    position = (len(values) - 1) * q
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return values[lower]
    return values[lower] + (values[upper] - values[lower]) * (position - lower)


def counter_payload(values: Iterable[Any]) -> dict[str, int]:
    return dict(sorted(Counter("missing" if value in {None, ""} else str(value) for value in values).items()))


def classify_conversion(row: dict[str, Any]) -> str:
    fill_rate = row.get("order_fill_rate")
    trade_to_signal = row.get("trade_to_signal_ratio")
    if fill_rate is not None and fill_rate < 0.99:
        return "fill_rejection_or_partial_fill"
    if trade_to_signal is None:
        return "missing_signal_or_trade_count"
    if trade_to_signal < 0.20:
        return "heavy_lifecycle_compression_lt20pct"
    if trade_to_signal < 0.50:
        return "moderate_lifecycle_compression_20_to_50pct"
    return "loose_lifecycle_compression_gte50pct"


def classify_economics(row: dict[str, Any]) -> str:
    pf = row.get("profit_factor")
    dd = row.get("max_drawdown_percent")
    net_per_signal = row.get("net_per_signal")
    if pf is None or dd is None:
        return "missing_runtime_economics"
    if pf >= 2.0 and dd <= 10.0:
        return "pf_ge2_dd_le10"
    if pf >= 2.0 and dd > 10.0:
        return "pf_ge2_but_dd_gt10"
    if net_per_signal is not None and net_per_signal > 0:
        return "positive_net_per_signal_but_pf_or_dd_fail"
    return "negative_net_per_signal_or_pf_dd_fail"


def build_rows() -> list[dict[str, Any]]:
    attempts = read_json(ATTEMPTS_JSON)
    runtime_by_key = {key(row.get("stage_num"), row.get("split")): row for row in read_csv(RUNTIME_ROWS)}
    config_by_key = {key(row.get("stage_num"), row.get("split")): row for row in read_csv(F67B_ROWS)}
    execution_by_attempt = attempt_by_name(read_json(EXECUTION_RESULT_JSON))

    rows: list[dict[str, Any]] = []
    for attempt in attempts:
        row_key = key(attempt.get("stage_num"), attempt.get("split"))
        runtime_row = runtime_by_key.get(row_key, {})
        config_row = config_by_key.get(row_key, {})
        execution_row = execution_by_attempt.get(str(attempt.get("attempt_name")), {})
        last_summary = ((execution_row.get("runtime_outputs") or {}).get("last_summary") or {})
        report_path = report_path_for_attempt(attempt)
        report_metrics = extract_mt5_strategy_report_metrics(report_path)
        deal_metrics = extract_deal_metrics(report_path)

        signal_count = as_int(runtime_row.get("mt5_signal_count") or attempt.get("expected_signal_count"))
        order_attempt_count = as_int(last_summary.get("order_attempt_count") or runtime_row.get("order_attempt_count"))
        order_fill_count = as_int(last_summary.get("order_fill_count") or runtime_row.get("order_fill_count"))
        trade_count = as_int(report_metrics.get("trade_count") or runtime_row.get("trade_count"))
        deal_count = as_int(report_metrics.get("deal_count") or deal_metrics.get("deal_row_count"))
        net_profit = as_float(report_metrics.get("net_profit") or runtime_row.get("net_profit"))
        gross_profit = as_float(report_metrics.get("gross_profit"))
        gross_loss = as_float(report_metrics.get("gross_loss"))
        winning_trade_count = as_int(report_metrics.get("winning_trade_count"))
        losing_trade_count = as_int(report_metrics.get("losing_trade_count"))
        average_win = ratio(gross_profit, winning_trade_count)
        average_loss = ratio(gross_loss, losing_trade_count)
        payoff_ratio = ratio(average_win, abs(average_loss) if average_loss is not None else None)
        net_reconciled = None
        if net_profit is not None:
            net_reconciled = net_profit - (
                deal_metrics["deal_profit_sum"] + deal_metrics["deal_commission_sum"] + deal_metrics["deal_swap_sum"]
            )

        output_row: dict[str, Any] = {
            "stage_num": str(attempt.get("stage_num") or ""),
            "stage_id": str(attempt.get("stage_id") or ""),
            "candidate_id": str(attempt.get("candidate_id") or ""),
            "split": str(attempt.get("split") or ""),
            "attempt_name": str(attempt.get("attempt_name") or ""),
            "report_path": str(report_path.relative_to(ROOT)).replace("\\", "/"),
            "telemetry_path": str(((execution_row.get("runtime_outputs") or {}).get("telemetry_path") or "")),
            "summary_path": str(((execution_row.get("runtime_outputs") or {}).get("summary_path") or "")),
            "max_hold_bars": config_row.get("max_hold_bars", ""),
            "atr_sltp_enabled": config_row.get("atr_sltp_enabled", ""),
            "atr_stop_multiplier": config_row.get("atr_stop_multiplier", ""),
            "atr_take_profit_multiplier": config_row.get("atr_take_profit_multiplier", ""),
            "signal_count": signal_count,
            "expected_signal_count": as_int(attempt.get("expected_signal_count")),
            "signal_count_diff": as_int(runtime_row.get("signal_count_diff")),
            "long_count": as_int(last_summary.get("long_count") or attempt.get("expected_long_count")),
            "short_count": as_int(last_summary.get("short_count") or attempt.get("expected_short_count")),
            "flat_count": as_int(last_summary.get("flat_count")),
            "order_attempt_count": order_attempt_count,
            "order_fill_count": order_fill_count,
            "trade_count": trade_count,
            "deal_count": deal_count,
            "deal_in_count": deal_metrics["deal_in_count"],
            "deal_out_count": deal_metrics["deal_out_count"],
            "order_fill_rate": ratio(order_fill_count, order_attempt_count),
            "order_attempt_to_signal_ratio": ratio(order_attempt_count, signal_count),
            "trade_to_signal_ratio": ratio(trade_count, signal_count),
            "deal_to_order_fill_ratio": ratio(deal_count, order_fill_count),
            "deal_minus_order_fill": None
            if deal_count is None or order_fill_count is None
            else deal_count - order_fill_count,
            "deal_count_equals_2x_trade": "true" if deal_count is not None and trade_count is not None and deal_count == trade_count * 2 else "false",
            "order_fill_equals_deal_count": "true" if order_fill_count is not None and deal_count is not None and order_fill_count == deal_count else "false",
            "net_profit": net_profit,
            "gross_profit": gross_profit,
            "gross_loss": gross_loss,
            "deal_profit_sum": deal_metrics["deal_profit_sum"],
            "deal_commission_sum": deal_metrics["deal_commission_sum"],
            "deal_swap_sum": deal_metrics["deal_swap_sum"],
            "deal_cost_sum": deal_metrics["deal_cost_sum"],
            "net_reconciliation_error": net_reconciled,
            "profit_factor": as_float(report_metrics.get("profit_factor")),
            "expectancy": as_float(report_metrics.get("expectancy")),
            "win_rate_percent": as_float(report_metrics.get("win_rate_percent")),
            "average_win": average_win,
            "average_loss": average_loss,
            "payoff_ratio": payoff_ratio,
            "recovery_factor": as_float(report_metrics.get("recovery_factor")),
            "max_drawdown_amount": as_float(report_metrics.get("max_drawdown_amount")),
            "max_drawdown_percent": as_float(report_metrics.get("max_drawdown_percent")),
            "short_trade_count": as_int(report_metrics.get("short_trade_count")),
            "long_trade_count": as_int(report_metrics.get("long_trade_count")),
            "net_per_signal": ratio(net_profit, signal_count),
            "net_per_order_fill": ratio(net_profit, order_fill_count),
            "net_per_trade": ratio(net_profit, trade_count),
            "swap_per_trade": ratio(deal_metrics["deal_swap_sum"], trade_count),
            "dd_per_trade": ratio(as_float(report_metrics.get("max_drawdown_percent")), trade_count),
            "report_metric_status": report_metrics.get("status"),
            "deal_table_encoding": deal_metrics["deal_table_encoding"],
            "runtime_summary_status": (execution_row.get("runtime_outputs") or {}).get("status", ""),
            "last_skip_reason": last_summary.get("last_skip_reason", ""),
            "conversion_read": "",
            "economics_read": "",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        output_row["conversion_read"] = classify_conversion(output_row)
        output_row["economics_read"] = classify_economics(output_row)
        rows.append(output_row)
    return rows


def group_counts(rows: list[dict[str, Any]], key_name: str) -> dict[str, dict[str, Any]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[str(row.get(key_name) or "missing")].append(row)
    output: dict[str, dict[str, Any]] = {}
    for group, group_rows in sorted(groups.items()):
        output[group] = {
            "rows": len(group_rows),
            "net_profit_sum": sum(float(row.get("net_profit") or 0.0) for row in group_rows),
            "swap_sum": sum(float(row.get("deal_swap_sum") or 0.0) for row in group_rows),
            "trade_count_sum": sum(int(row.get("trade_count") or 0) for row in group_rows),
            "signal_count_sum": sum(int(row.get("signal_count") or 0) for row in group_rows),
            "trade_to_signal_ratio_summary": summarize_numbers(row.get("trade_to_signal_ratio") for row in group_rows),
            "profit_factor_summary": summarize_numbers(row.get("profit_factor") for row in group_rows),
            "max_drawdown_percent_summary": summarize_numbers(row.get("max_drawdown_percent") for row in group_rows),
            "conversion_reads": counter_payload(row.get("conversion_read") for row in group_rows),
            "economics_reads": counter_payload(row.get("economics_read") for row in group_rows),
        }
    return output


def build_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    total_signals = sum(int(row.get("signal_count") or 0) for row in rows)
    total_order_attempts = sum(int(row.get("order_attempt_count") or 0) for row in rows)
    total_order_fills = sum(int(row.get("order_fill_count") or 0) for row in rows)
    total_trades = sum(int(row.get("trade_count") or 0) for row in rows)
    total_deals = sum(int(row.get("deal_count") or 0) for row in rows)
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_attempts": str(ATTEMPTS_JSON.relative_to(ROOT)).replace("\\", "/"),
        "source_runtime_rows": str(RUNTIME_ROWS.relative_to(ROOT)).replace("\\", "/"),
        "source_config_rows": str(F67B_ROWS.relative_to(ROOT)).replace("\\", "/"),
        "row_count": len(rows),
        "report_completed_rows": sum(1 for row in rows if row.get("report_metric_status") == "completed"),
        "runtime_summary_completed_rows": sum(1 for row in rows if row.get("runtime_summary_status") == "completed"),
        "total_signal_count": total_signals,
        "total_order_attempt_count": total_order_attempts,
        "total_order_fill_count": total_order_fills,
        "total_trade_count": total_trades,
        "total_deal_count": total_deals,
        "overall_order_fill_rate": ratio(total_order_fills, total_order_attempts),
        "overall_trade_to_signal_ratio": ratio(total_trades, total_signals),
        "overall_order_attempt_to_signal_ratio": ratio(total_order_attempts, total_signals),
        "deal_count_equals_2x_trade_rows": sum(1 for row in rows if row.get("deal_count_equals_2x_trade") == "true"),
        "order_fill_equals_deal_count_rows": sum(1 for row in rows if row.get("order_fill_equals_deal_count") == "true"),
        "deal_minus_order_fill_positive_rows": sum(1 for row in rows if float(row.get("deal_minus_order_fill") or 0.0) > 0.0),
        "deal_minus_order_fill_positive_sum": sum(float(row.get("deal_minus_order_fill") or 0.0) for row in rows if float(row.get("deal_minus_order_fill") or 0.0) > 0.0),
        "commission_nonzero_rows": sum(1 for row in rows if abs(float(row.get("deal_commission_sum") or 0.0)) > 1e-9),
        "swap_nonzero_rows": sum(1 for row in rows if abs(float(row.get("deal_swap_sum") or 0.0)) > 1e-9),
        "deal_commission_sum_total": sum(float(row.get("deal_commission_sum") or 0.0) for row in rows),
        "deal_swap_sum_total": sum(float(row.get("deal_swap_sum") or 0.0) for row in rows),
        "deal_profit_sum_total": sum(float(row.get("deal_profit_sum") or 0.0) for row in rows),
        "net_profit_sum_total": sum(float(row.get("net_profit") or 0.0) for row in rows),
        "max_abs_net_reconciliation_error": max(abs(float(row.get("net_reconciliation_error") or 0.0)) for row in rows),
        "positive_net_rows": sum(1 for row in rows if float(row.get("net_profit") or 0.0) > 0),
        "profit_factor_ge2_rows": sum(1 for row in rows if float(row.get("profit_factor") or 0.0) >= 2.0),
        "drawdown_gt10_rows": sum(1 for row in rows if float(row.get("max_drawdown_percent") or 0.0) > 10.0),
        "trade_to_signal_ratio_summary": summarize_numbers(row.get("trade_to_signal_ratio") for row in rows),
        "order_attempt_to_signal_ratio_summary": summarize_numbers(row.get("order_attempt_to_signal_ratio") for row in rows),
        "net_per_signal_summary": summarize_numbers(row.get("net_per_signal") for row in rows),
        "net_per_trade_summary": summarize_numbers(row.get("net_per_trade") for row in rows),
        "swap_per_trade_summary": summarize_numbers(row.get("swap_per_trade") for row in rows),
        "conversion_reads": counter_payload(row.get("conversion_read") for row in rows),
        "economics_reads": counter_payload(row.get("economics_read") for row in rows),
        "by_split": group_counts(rows, "split"),
        "by_max_hold_bars": group_counts(rows, "max_hold_bars"),
        "by_atr_sltp_enabled": group_counts(rows, "atr_sltp_enabled"),
        "runtime_gap_cause_read": "lifecycle_trade_compression_plus_tester_side_exit_deals_plus_report_level_swap_cost_not_config_identity_drift",
        "next_action": "run_narrow_f67_mt5_runtime_probe_with_explicit_cost_identity_and_order_intent_receipt_before_closeout",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    columns = [
        "stage_num",
        "stage_id",
        "candidate_id",
        "split",
        "attempt_name",
        "report_path",
        "telemetry_path",
        "summary_path",
        "max_hold_bars",
        "atr_sltp_enabled",
        "atr_stop_multiplier",
        "atr_take_profit_multiplier",
        "signal_count",
        "expected_signal_count",
        "signal_count_diff",
        "long_count",
        "short_count",
        "flat_count",
        "order_attempt_count",
        "order_fill_count",
        "trade_count",
        "deal_count",
        "deal_in_count",
        "deal_out_count",
        "order_fill_rate",
        "order_attempt_to_signal_ratio",
        "trade_to_signal_ratio",
        "deal_to_order_fill_ratio",
        "deal_minus_order_fill",
        "deal_count_equals_2x_trade",
        "order_fill_equals_deal_count",
        "net_profit",
        "gross_profit",
        "gross_loss",
        "deal_profit_sum",
        "deal_commission_sum",
        "deal_swap_sum",
        "deal_cost_sum",
        "net_reconciliation_error",
        "profit_factor",
        "expectancy",
        "win_rate_percent",
        "average_win",
        "average_loss",
        "payoff_ratio",
        "recovery_factor",
        "max_drawdown_amount",
        "max_drawdown_percent",
        "short_trade_count",
        "long_trade_count",
        "net_per_signal",
        "net_per_order_fill",
        "net_per_trade",
        "swap_per_trade",
        "dd_per_trade",
        "report_metric_status",
        "deal_table_encoding",
        "runtime_summary_status",
        "last_skip_reason",
        "conversion_read",
        "economics_read",
        "claim_boundary",
    ]
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: "" if row.get(column) is None else row.get(column) for column in columns})


def fmt(value: Any) -> str:
    if value is None:
        return "missing"
    if isinstance(value, float):
        return f"{value:.4f}"
    return str(value)


def build_report(summary: dict[str, Any]) -> str:
    trade_signal = summary["trade_to_signal_ratio_summary"]
    net_signal = summary["net_per_signal_summary"]
    return f"""# F67C Runtime Native Order Intent Economics(F67C 런타임 기반 주문 의도 경제성)

- stage_id(단계 ID): `{STAGE_ID}`
- run_id(실행 ID): `{RUN_ID}`
- source_attempts(원천 시도 목록): `{summary['source_attempts']}`
- source_runtime_rows(원천 런타임 행): `{summary['source_runtime_rows']}`
- source_config_rows(원천 설정 행): `{summary['source_config_rows']}`
- row_count(행 수): `{summary['row_count']}`
- claim_boundary(주장 경계): `{summary['claim_boundary']}`

## Read(판독)

Action(행동): F66 MT5 runtime probe(F66 MT5 런타임 탐침) `64`개를 report deal table(보고서 거래 표), runtime summary(런타임 요약), F67B config rows(F67B 설정 행)와 결합했다.

Effect(효과): signal count parity(신호 수 동등성)가 order/trade economics(주문/거래 경제성)로 전이되는지, 그리고 explicit cost identity missing(명시 비용 정체성 누락)이 실제 비용 0인지 report-only cost(보고서 전용 비용)인지 분리했다.

- report_completed_rows(보고서 완료 행): `{summary['report_completed_rows']}/{summary['row_count']}`
- runtime_summary_completed_rows(런타임 요약 완료 행): `{summary['runtime_summary_completed_rows']}/{summary['row_count']}`
- total_signal_count(총 신호 수): `{summary['total_signal_count']}`
- total_order_fill_count(총 주문 체결 수): `{summary['total_order_fill_count']}`
- total_trade_count(총 거래 수): `{summary['total_trade_count']}`
- overall_trade_to_signal_ratio(전체 거래/신호 비율): `{fmt(summary['overall_trade_to_signal_ratio'])}`
- trade_to_signal_ratio median(거래/신호 비율 중앙값): `{fmt(trade_signal.get('median'))}`
- net_per_signal median(신호당 순손익 중앙값): `{fmt(net_signal.get('median'))}`

## Cost Identity Reinforcement(비용 정체성 보강)

- commission_nonzero_rows(커미션 0 아님 행): `{summary['commission_nonzero_rows']}/{summary['row_count']}`
- swap_nonzero_rows(스왑 0 아님 행): `{summary['swap_nonzero_rows']}/{summary['row_count']}`
- deal_commission_sum_total(거래 커미션 합계): `{fmt(summary['deal_commission_sum_total'])}`
- deal_swap_sum_total(거래 스왑 합계): `{fmt(summary['deal_swap_sum_total'])}`
- max_abs_net_reconciliation_error(순손익 재계산 최대 오차): `{fmt(summary['max_abs_net_reconciliation_error'])}`

## Runtime Economics(런타임 경제성)

- net_profit_sum_total(순손익 합계): `{fmt(summary['net_profit_sum_total'])}`
- positive_net_rows(순손익 양수 행): `{summary['positive_net_rows']}/{summary['row_count']}`
- profit_factor_ge2_rows(수익 팩터 2 이상 행): `{summary['profit_factor_ge2_rows']}/{summary['row_count']}`
- drawdown_gt10_rows(손실폭 10 초과 행): `{summary['drawdown_gt10_rows']}/{summary['row_count']}`
- deal_count_equals_2x_trade_rows(거래 표 딜 수=거래 수*2 행): `{summary['deal_count_equals_2x_trade_rows']}/{summary['row_count']}`
- order_fill_equals_deal_count_rows(주문 체결 수=거래 표 딜 수 행): `{summary['order_fill_equals_deal_count_rows']}/{summary['row_count']}`
- deal_minus_order_fill_positive_rows(거래 표 딜 수가 런타임 주문 체결 수보다 큰 행): `{summary['deal_minus_order_fill_positive_rows']}/{summary['row_count']}`
- deal_minus_order_fill_positive_sum(초과 딜 수 합계): `{fmt(summary['deal_minus_order_fill_positive_sum'])}`

## Conversion Reads(전환 판독)

```json
{json.dumps(summary['conversion_reads'], ensure_ascii=False, indent=2)}
```

## Economics Reads(경제성 판독)

```json
{json.dumps(summary['economics_reads'], ensure_ascii=False, indent=2)}
```

## Group Reads(그룹 판독)

```json
{json.dumps({'by_split': summary['by_split'], 'by_max_hold_bars': summary['by_max_hold_bars'], 'by_atr_sltp_enabled': summary['by_atr_sltp_enabled']}, ensure_ascii=False, indent=2)}
```

## Gap Cause Read(간극 원인 판독)

runtime_gap_cause_read(런타임 간극 원인 판독): `{summary['runtime_gap_cause_read']}`.

This is an observation only(관찰 전용). F67 closeout(마감) still requires(여전히 필요) a narrow MT5 Runtime Probe(좁은 MT5 런타임 탐침) with explicit cost identity(명시 비용 정체성), order intent receipt(주문 의도 영수증), and proxy/runtime KPI gap(프록시/런타임 KPI 간극).

## Next Action(다음 행동)

`{summary['next_action']}`
"""


def main() -> int:
    if not path_exists(ATTEMPTS_JSON):
        raise FileNotFoundError(ATTEMPTS_JSON)
    rows = build_rows()
    summary = build_summary(rows)
    io_path(RUN_ROOT).mkdir(parents=True, exist_ok=True)
    io_path(REVIEWS_ROOT).mkdir(parents=True, exist_ok=True)
    write_csv(ROWS_CSV, rows)
    write_csv(REVIEW_ROWS_CSV, rows)
    io_path(SUMMARY_JSON).write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    io_path(REVIEW_SUMMARY_JSON).write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    io_path(REPORT_MD).write_text(build_report(summary), encoding="utf-8-sig")
    print(json.dumps({"run_id": RUN_ID, "row_count": len(rows), "report": str(REPORT_MD)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
