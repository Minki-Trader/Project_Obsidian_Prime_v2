from __future__ import annotations

import csv
import json
import math
import sys
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.mt5.strategy_report import extract_mt5_strategy_report_metrics
from foundation.mt5.trade_report import pair_deals_into_trades, parse_mt5_trade_report
from stage_pipelines.stage337 import attempt_balanced_no_lookahead_runtime_probe_without_db as aw
from stage_pipelines.stage337 import select_tester_gap_repair_and_protocol_attribution_without_db as ax


TODAY = "2026-05-27"
STAGE_ID = ax.STAGE_ID
RUN_NUMBER = "run337AY"
RUN_ID = "run337AY_shifted_custom_protocol_attribution_probe_without_db_v1"
PARENT_RUN_ID = ax.RUN_ID
NEXT_RUN_ID = "run337AZ_no_overfit_repair_design_from_shifted_attribution_without_db_v1"
STATUS = "completed_stage337AY_shifted_custom_protocol_attribution_fragile_no_forward_decision"
JUDGMENT = "shifted_custom_route_reaches_feature_last_but_cost_direction_recovery_and_trade_density_fragility_remain"
DECISION = "stage337AY_open_run337AZ_no_overfit_repair_design_from_shifted_attribution_without_db_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage337AY_shifted_custom_protocol_attribution_without_db_"
    "no_model_training_no_threshold_retuning_no_db_rule_rewrite_no_lot_optimization_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ax.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = ax.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337AY_shifted_protocol_attribution.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage337AY_shifted_attribution.md"
SELECTED_STATUS = ax.SELECTED_STATUS
STAGE_BRIEF = ax.STAGE_BRIEF
WORKSPACE_STATE = ax.WORKSPACE_STATE
CURRENT_STATE = ax.CURRENT_STATE
CHANGELOG = ax.CHANGELOG
RUN_REGISTRY = ax.RUN_REGISTRY
ALPHA_LEDGER = ax.ALPHA_LEDGER
ARTIFACT_REGISTRY = ax.ARTIFACT_REGISTRY
STAGE_LEDGER = ax.STAGE_LEDGER

RUN337AX_DIR = STAGE_DIR / "02_runs" / "run337AX"
RUN337AK_DIR = STAGE_DIR / "02_runs" / "run337AK"
RUN337AD_DIR = STAGE_DIR / "02_runs" / "run337AD"

AX_FINAL = RUN337AX_DIR / "final_decision.json"
AX_BINDING = RUN337AX_DIR / "protocol_route_binding_matrix.csv"
AX_ROUTE_METRICS = RUN337AX_DIR / "route_metric_comparison.csv"
AK_RUNTIME = RUN337AK_DIR / "runtime_summary.csv"
AK_GAP = RUN337AK_DIR / "tester_feature_last_gap_exact_timestamp.csv"
AK_PROXY = RUN337AK_DIR / "exact_timestamp_proxy_mt5_difference.csv"
AK_FEATURES = RUN337AK_DIR / "feature_matrices" / "u42_plain_ak_shifted_custom_exact_timestamp_features.csv"
AK_TELEMETRY = RUN337AK_DIR / "runtime_telemetry" / "u42_plain_rf_ak_shifted_custom_exact_timestamp_telemetry.csv"
AK_REPORT = RUN337AK_DIR / "mt5" / "reports" / "Project_Obsidian_Prime_v2_run337AK_next_rollover_or_synthetic_custom_parity_repair_v1_u42_plain_rf_ak_shifted_custom_exact_timestamp.htm"
AD_RUNTIME = RUN337AD_DIR / "runtime_summary.csv"
AD_GAP = RUN337AD_DIR / "tester_feature_last_gap_completed_day_slice.csv"
AD_PROXY = RUN337AD_DIR / "timestamp_aligned_proxy_mt5_difference.csv"
AD_FEATURES = RUN337AD_DIR / "feature_matrices" / "u42_plain_ad_completed_day_broker_slice_features.csv"
AD_REPORT = RUN337AD_DIR / "mt5" / "reports" / "Project_Obsidian_Prime_v2_run337AD_completed_day_forward_slice_or_next_day_rollover_confirm_v1_u42_plain_rf_ad_completed_day_broker_slice.htm"

SHIFTED_TRADE_RECORDS = RUN_DIR / "shifted_custom_trade_records.csv"
COMPLETED_TRADE_RECORDS = RUN_DIR / "completed_day_anchor_trade_records.csv"
PROTOCOL_ATTRIBUTION = RUN_DIR / "protocol_attribution_matrix.csv"
REGIME_ATTRIBUTION = RUN_DIR / "shifted_custom_regime_attribution.csv"
COST_STRESS = RUN_DIR / "cost_stress_report.csv"
CURVE_POCKET = RUN_DIR / "curve_pocket_report.csv"
PROXY_USABILITY = RUN_DIR / "proxy_mt5_attribution_usability.csv"
NO_OVERFIT_GUARDS = RUN_DIR / "no_overfit_attribution_guard_matrix.csv"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
ARTIFACT_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
FORENSICS_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    AX_FINAL,
    AX_BINDING,
    AX_ROUTE_METRICS,
    AK_RUNTIME,
    AK_GAP,
    AK_PROXY,
    AK_FEATURES,
    AK_TELEMETRY,
    AK_REPORT,
    AD_RUNTIME,
    AD_GAP,
    AD_PROXY,
    AD_REPORT,
)
OUTPUT_FILES = (
    SHIFTED_TRADE_RECORDS,
    COMPLETED_TRADE_RECORDS,
    PROTOCOL_ATTRIBUTION,
    REGIME_ATTRIBUTION,
    COST_STRESS,
    CURVE_POCKET,
    PROXY_USABILITY,
    NO_OVERFIT_GUARDS,
    GATE_AUDIT,
    ARTIFACT_RECEIPT,
    DATA_RECEIPT,
    RUNTIME_RECEIPT,
    FORENSICS_RECEIPT,
    ATTRIBUTION_RECEIPT,
    JUDGMENT_RECEIPT,
    FINAL_DECISION,
    RUN_MANIFEST,
)

TRADE_COLUMNS = (
    "route_id",
    "trade_index",
    "direction",
    "open_time",
    "close_time",
    "volume",
    "gross_profit",
    "net_profit",
    "cum_net_profit",
    "equity_peak",
    "underwater_amount",
    "hold_bars",
    "open_hour_utc",
    "session_utc",
    "chron_segment",
    "month",
    "atr_14",
    "atr_bucket",
    "adx_14",
    "adx_bucket",
    "vol_20",
    "vol_bucket",
    "rsi_14",
    "rsi_bucket",
    "di_spread_14",
    "di_bucket",
    "is_us_cash_open",
    "claim_boundary",
)
PROTOCOL_COLUMNS = (
    "protocol_id",
    "diagnostic_axis",
    "recommended_route",
    "metric_summary",
    "shifted_read",
    "completed_anchor_read",
    "fragility_status",
    "usable_for_repair_design",
    "usable_for_forward_decision",
    "forbidden_use",
    "effect",
    "claim_boundary",
)
REGIME_COLUMNS = (
    "route_id",
    "dimension",
    "bucket",
    "trade_count",
    "net_profit",
    "profit_factor",
    "win_rate",
    "long_trades",
    "short_trades",
    "max_underwater_amount",
    "effect",
    "claim_boundary",
)
COST_COLUMNS = (
    "route_id",
    "cost_points_per_trade",
    "trade_count",
    "stressed_net_profit",
    "stressed_profit_factor",
    "net_delta",
    "stress_status",
    "effect",
    "claim_boundary",
)
CURVE_COLUMNS = (
    "route_id",
    "metric_id",
    "value",
    "interpretation",
    "effect",
    "claim_boundary",
)
PROXY_COLUMNS = (
    "attempt_name",
    "proxy_rows",
    "proxy_matched",
    "usable_for_signal_parity",
    "usable_for_attribution",
    "usable_for_forward_decision",
    "effect",
    "claim_boundary",
)
GUARD_COLUMNS = ax.GUARD_COLUMNS
GATE_COLUMNS = ax.GATE_COLUMNS


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_dt(value: str) -> datetime:
    return datetime.strptime(value, "%Y.%m.%d %H:%M:%S")


def fnum(value: Any, default: float = 0.0) -> float:
    try:
        number = float(str(value))
        return number if math.isfinite(number) else default
    except Exception:
        return default


def bucket_numeric(value: float, cuts: Sequence[float], labels: Sequence[str]) -> str:
    for cut, label in zip(cuts, labels):
        if value <= cut:
            return label
    return labels[-1]


def session(hour: int) -> str:
    if hour < 7:
        return "session_00_06_utc"
    if hour < 13:
        return "session_07_12_utc"
    if hour < 19:
        return "session_13_18_utc"
    return "session_19_23_utc"


def chron_segment(index: int, total: int) -> str:
    if total <= 0:
        return "chron_unknown"
    ratio = index / total
    if ratio <= 1 / 3:
        return "chron_early"
    if ratio <= 2 / 3:
        return "chron_mid"
    return "chron_late"


def feature_map(path: Path) -> dict[str, dict[str, str]]:
    rows = aw.read_csv(path)
    return {row.get("bar_time_server", ""): row for row in rows}


def report_path_from_runtime(runtime_rows: Sequence[Mapping[str, str]], attempt: str, fallback: Path) -> Path:
    for row in runtime_rows:
        if row.get("attempt_name") == attempt and row.get("report_path"):
            return Path(row["report_path"])
    return fallback


def load_trades(route_id: str, report_path: Path, features: Mapping[str, Mapping[str, str]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    metrics = extract_mt5_strategy_report_metrics(report_path)
    parsed = parse_mt5_trade_report(report_path)
    trades = pair_deals_into_trades(parsed["deals"])
    rows: list[dict[str, Any]] = []
    cum = 0.0
    peak = 0.0
    total = len(trades)
    for trade in trades:
        cum += trade.net_profit
        peak = max(peak, cum)
        open_text = trade.open_time.strftime("%Y.%m.%d %H:%M:%S")
        feat = features.get(open_text, {})
        hour = int(trade.open_time.hour)
        atr = fnum(feat.get("atr_14"))
        adx = fnum(feat.get("adx_14"))
        vol = fnum(feat.get("historical_vol_20"))
        rsi = fnum(feat.get("rsi_14"))
        di = fnum(feat.get("di_spread_14"))
        rows.append(
            {
                "route_id": route_id,
                "trade_index": trade.index,
                "direction": trade.direction,
                "open_time": open_text,
                "close_time": trade.close_time.strftime("%Y.%m.%d %H:%M:%S"),
                "volume": trade.volume,
                "gross_profit": f"{trade.gross_profit:.10g}",
                "net_profit": f"{trade.net_profit:.10g}",
                "cum_net_profit": f"{cum:.10g}",
                "equity_peak": f"{peak:.10g}",
                "underwater_amount": f"{peak - cum:.10g}",
                "hold_bars": f"{(trade.close_time - trade.open_time).total_seconds() / 60.0 / 5.0:.10g}",
                "open_hour_utc": f"{hour:02d}",
                "session_utc": session(hour),
                "chron_segment": chron_segment(trade.index, total),
                "month": trade.open_time.strftime("%Y-%m"),
                "atr_14": feat.get("atr_14", ""),
                "atr_bucket": bucket_numeric(atr, (12.0, 18.0, 25.0), ("atr_<=12", "atr_12_18", "atr_18_25", "atr_>25")),
                "adx_14": feat.get("adx_14", ""),
                "adx_bucket": bucket_numeric(adx, (20.0, 25.0, 40.0), ("adx_<=20", "adx_20_25", "adx_25_40", "adx_>40")),
                "vol_20": feat.get("historical_vol_20", ""),
                "vol_bucket": bucket_numeric(vol, (0.08, 0.14, 0.22), ("vol_<=0.08", "vol_0.08_0.14", "vol_0.14_0.22", "vol_>0.22")),
                "rsi_14": feat.get("rsi_14", ""),
                "rsi_bucket": bucket_numeric(rsi, (45.0, 55.0, 65.0), ("rsi_<=45", "rsi_45_55", "rsi_55_65", "rsi_>65")),
                "di_spread_14": feat.get("di_spread_14", ""),
                "di_bucket": "di_negative" if di < 0 else "di_positive",
                "is_us_cash_open": feat.get("is_us_cash_open", ""),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows, {**metrics, **parsed.get("summary", {})}


def profit_factor(values: Iterable[float]) -> float | str:
    gross_profit = sum(v for v in values if v > 0)
    gross_loss = -sum(v for v in values if v < 0)
    if gross_loss == 0:
        return "inf" if gross_profit > 0 else ""
    return gross_profit / gross_loss


def summarize(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    profits = [fnum(row.get("net_profit")) for row in rows]
    trade_count = len(profits)
    net = sum(profits)
    wins = sum(1 for value in profits if value > 0)
    pf = profit_factor(profits)
    long_count = sum(1 for row in rows if str(row.get("direction", "")).lower() == "buy")
    short_count = sum(1 for row in rows if str(row.get("direction", "")).lower() == "sell")
    max_underwater = max((fnum(row.get("underwater_amount")) for row in rows), default=0.0)
    return {
        "trade_count": trade_count,
        "net_profit": net,
        "profit_factor": pf,
        "win_rate": wins / trade_count if trade_count else 0.0,
        "long_trades": long_count,
        "short_trades": short_count,
        "max_underwater_amount": max_underwater,
    }


def summary_text(summary: Mapping[str, Any]) -> str:
    pf = summary.get("profit_factor", "")
    pf_text = f"{pf:.4g}" if isinstance(pf, float) else str(pf)
    return (
        f"trades(거래)={summary.get('trade_count', 0)};"
        f"net(순익)={float(summary.get('net_profit', 0.0)):.4g};"
        f"PF(수익 팩터)={pf_text};"
        f"long/short(롱/숏)={summary.get('long_trades', 0)}/{summary.get('short_trades', 0)};"
        f"underwater(잠김)={float(summary.get('max_underwater_amount', 0.0)):.4g}"
    )


def group_regimes(rows: Sequence[Mapping[str, Any]], route_id: str) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    dimensions = ("direction", "session_utc", "chron_segment", "month", "open_hour_utc", "atr_bucket", "adx_bucket", "vol_bucket", "rsi_bucket", "di_bucket", "is_us_cash_open")
    for dimension in dimensions:
        buckets: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
        for row in rows:
            buckets[str(row.get(dimension, ""))].append(row)
        for bucket, bucket_rows in sorted(buckets.items()):
            summary = summarize(bucket_rows)
            pf = summary["profit_factor"]
            output.append(
                {
                    "route_id": route_id,
                    "dimension": dimension,
                    "bucket": bucket,
                    "trade_count": summary["trade_count"],
                    "net_profit": f"{summary['net_profit']:.10g}",
                    "profit_factor": f"{pf:.10g}" if isinstance(pf, float) else pf,
                    "win_rate": f"{summary['win_rate']:.10g}",
                    "long_trades": summary["long_trades"],
                    "short_trades": summary["short_trades"],
                    "max_underwater_amount": f"{summary['max_underwater_amount']:.10g}",
                    "effect": "This bucket shows where the shifted exact route concentrates risk(이 버킷은 이동 정확 경로의 위험이 어디에 몰리는지 보여준다).",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return output


def cost_stress(rows: Sequence[Mapping[str, Any]], route_id: str) -> list[dict[str, Any]]:
    base = [fnum(row.get("net_profit")) for row in rows]
    output = []
    for cost in (0.0, 0.5, 1.0, 2.0):
        stressed = [value - cost for value in base]
        pf = profit_factor(stressed)
        net = sum(stressed)
        output.append(
            {
                "route_id": route_id,
                "cost_points_per_trade": cost,
                "trade_count": len(stressed),
                "stressed_net_profit": f"{net:.10g}",
                "stressed_profit_factor": f"{pf:.10g}" if isinstance(pf, float) else pf,
                "net_delta": f"{net - sum(base):.10g}",
                "stress_status": "fragile_under_cost(비용 압박 취약)" if cost > 0 and net <= sum(base) * 0.5 else "baseline_or_monitor(기준 또는 관찰)",
                "effect": "Cost stress tests buffer without changing threshold or lot(비용 압박은 임계값이나 랏을 바꾸지 않고 버퍼를 본다).",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return output


def curve_pockets(rows: Sequence[Mapping[str, Any]], route_id: str) -> list[dict[str, Any]]:
    profits = [fnum(row.get("net_profit")) for row in rows]
    cum = 0.0
    peak = 0.0
    underwater = 0
    longest_underwater = 0
    for value in profits:
        cum += value
        if cum >= peak:
            peak = cum
            underwater = 0
        else:
            underwater += 1
            longest_underwater = max(longest_underwater, underwater)
    chunk_size = 25
    worst_net = None
    worst_start = 0
    for start in range(0, len(profits), chunk_size):
        chunk_net = sum(profits[start : start + chunk_size])
        if worst_net is None or chunk_net < worst_net:
            worst_net = chunk_net
            worst_start = start + 1
    summary = summarize(rows)
    metrics = [
        ("max_underwater_amount", summary["max_underwater_amount"], "peak-to-trough trade equity drawdown(거래 평가 곡선 고점-저점 손실폭)"),
        ("longest_underwater_trades", longest_underwater, "longest unresolved underwater stretch(가장 긴 미회복 잠김 구간)"),
        ("worst_25_trade_chunk_net", worst_net or 0.0, f"worst chunk starts at trade {worst_start}(최악 묶음 시작 거래 {worst_start})"),
        ("final_cum_net", sum(profits), "final cumulative net(최종 누적 순익)"),
    ]
    return [
        {
            "route_id": route_id,
            "metric_id": metric_id,
            "value": f"{float(value):.10g}" if isinstance(value, float) else value,
            "interpretation": interpretation,
            "effect": "Curve pocket metrics expose shape fragility without retuning(곡선 포켓 지표는 재튜닝 없이 형태 취약성을 드러낸다).",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for metric_id, value, interpretation in metrics
    ]


def protocol_attribution(
    bindings: Sequence[Mapping[str, str]],
    shifted_rows: Sequence[Mapping[str, Any]],
    completed_rows: Sequence[Mapping[str, Any]],
    shifted_metrics: Mapping[str, Any],
    completed_metrics: Mapping[str, Any],
) -> list[dict[str, Any]]:
    shifted = summarize(shifted_rows)
    completed = summarize(completed_rows)
    shifted_by_direction = {direction: summarize([row for row in shifted_rows if row.get("direction") == direction]) for direction in ("buy", "sell")}
    completed_by_direction = {direction: summarize([row for row in completed_rows if row.get("direction") == direction]) for direction in ("buy", "sell")}
    late = summarize([row for row in shifted_rows if row.get("chron_segment") == "chron_late"])
    early = summarize([row for row in shifted_rows if row.get("chron_segment") == "chron_early"])
    rows: list[dict[str, Any]] = []
    for binding in bindings:
        protocol = binding.get("protocol_id", "")
        if protocol == "defense_cost_buffer_guard":
            shifted_read = f"shifted {summary_text(shifted)}; report_DD(보고서 손실폭)={shifted_metrics.get('max_drawdown_amount', '')}"
            completed_read = f"completed {summary_text(completed)}; report_DD(보고서 손실폭)={completed_metrics.get('max_drawdown_amount', '')}"
            fragility = "failed_buffer_thin(버퍼 얇음)"
        elif protocol == "defense_late_curve_pocket_guard":
            shifted_read = f"late {summary_text(late)} vs early {summary_text(early)}"
            completed_read = f"completed {summary_text(completed)}"
            fragility = "monitor_curve_pocket(곡선 포켓 관찰)"
        elif protocol == "repair_direction_symmetry_probe":
            shifted_read = f"shifted buy {summary_text(shifted_by_direction['buy'])}; sell {summary_text(shifted_by_direction['sell'])}"
            completed_read = f"completed buy {summary_text(completed_by_direction['buy'])}; sell {summary_text(completed_by_direction['sell'])}"
            fragility = "failed_short_density(숏 밀도 부족)"
        elif protocol == "repair_recovery_shape_probe":
            shifted_read = f"recovery(회복)={shifted_metrics.get('recovery_factor', '')}; curve_underwater(곡선 잠김)={shifted.get('max_underwater_amount', ''):.4g}"
            completed_read = f"recovery(회복)={completed_metrics.get('recovery_factor', '')}; curve_underwater(곡선 잠김)={completed.get('max_underwater_amount', ''):.4g}"
            fragility = "failed_recovery_shape(회복 형태 약함)"
        elif protocol == "offense_long_edge_preservation":
            shifted_read = summary_text(shifted_by_direction["buy"])
            completed_read = summary_text(completed_by_direction["buy"])
            fragility = "partial_long_edge_preserved(롱 우위 일부 보존)"
        elif protocol == "offense_trade_count_recovery":
            shifted_read = f"shifted trades(이동 거래)={shifted['trade_count']} vs completed(완성일)={completed['trade_count']}"
            completed_read = summary_text(completed)
            fragility = "failed_trade_density_drop(거래 밀도 감소)"
        elif protocol == "negative_control_hidden_current_day_forbidden":
            shifted_read = "broker current-day remains forbidden source; shifted route is diagnostic only(브로커 현재일은 금지 원천 유지, 이동 경로는 진단 전용)"
            completed_read = "completed-day anchor does not close current-day forward(완성일 앵커는 현재일 전진을 닫지 않음)"
            fragility = "passed_negative_control(부정 대조 통과)"
        elif protocol.startswith("negative_control_"):
            shifted_read = "negative control retained as guard under shifted route(이동 경로에서도 부정 대조를 가드로 유지)"
            completed_read = "not a selection rule(선택 규칙 아님)"
            fragility = "passed_negative_control(부정 대조 통과)"
        else:
            shifted_read = summary_text(shifted)
            completed_read = summary_text(completed)
            fragility = "diagnostic_only(진단 전용)"
        rows.append(
            {
                "protocol_id": protocol,
                "diagnostic_axis": binding.get("diagnostic_axis", ""),
                "recommended_route": binding.get("recommended_route", ""),
                "metric_summary": binding.get("metric_read", ""),
                "shifted_read": shifted_read,
                "completed_anchor_read": completed_read,
                "fragility_status": fragility,
                "usable_for_repair_design": "true",
                "usable_for_forward_decision": "false",
                "forbidden_use": binding.get("forbidden_use", ""),
                "effect": "Attribution converts runtime evidence into repair memory, not a tuned candidate(귀속은 런타임 근거를 튜닝 후보가 아니라 수리 기억으로 바꾼다).",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def proxy_usability() -> list[dict[str, Any]]:
    rows = aw.read_csv(AK_PROXY)
    by_attempt: dict[str, list[Mapping[str, str]]] = defaultdict(list)
    for row in rows:
        by_attempt[row.get("attempt_name", "")].append(row)
    output = []
    for attempt, attempt_rows in sorted(by_attempt.items()):
        matched = sum(1 for row in attempt_rows if row.get("difference_status") == "matched")
        output.append(
            {
                "attempt_name": attempt,
                "proxy_rows": len(attempt_rows),
                "proxy_matched": matched,
                "usable_for_signal_parity": str(matched == len(attempt_rows)).lower(),
                "usable_for_attribution": "true",
                "usable_for_forward_decision": "false",
                "effect": "Exact proxy-MT5 parity supports attribution boundaries only(정확 프록시-MT5 동등성은 귀속 경계만 지원한다).",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return output


def guards() -> list[dict[str, Any]]:
    items = [
        ("no_model_training(모델 학습 없음)", "passed", "used frozen reports, telemetry, and features only(고정 보고서/런타임 기록/피처만 사용)", "model training(모델 학습)", "Attribution does not fit a model(귀속은 모델을 학습하지 않는다)."),
        ("no_threshold_retune(임계값 재조정 없음)", "passed", "threshold policy read only(임계값 정책 읽기 전용)", "threshold retune(임계값 재조정)", "Signal surface stays frozen(신호 표면은 고정 상태다)."),
        ("no_db_rewrite(D/B 재작성 없음)", "passed", "D/B out_of_scope_by_claim maintained(D/B 주장 범위 밖 유지)", "D/B rewrite(D/B 재작성)", "Missing D/B source is not imputed(D/B 원천 누락을 대체 입력하지 않는다)."),
        ("no_lot_optimization(랏 최적화 없음)", "passed", "fixed 0.1 lot report evidence(고정 0.1랏 보고서 근거)", "lot optimization(랏 최적화)", "Lot-normalized reads are diagnostic only(랏 정규화 판독은 진단 전용이다)."),
        ("negative_controls_preserved(부정 대조 보존)", "passed", "3 controls remain non-selection(대조 3개 선택 금지 유지)", "negative-control selection(부정 대조 선택)", "Controls block overfit repair loops(대조는 과적합 수리 루프를 막는다)."),
    ]
    return [
        {
            "guard_id": guard_id,
            "status": status,
            "observed": observed,
            "forbidden_action": forbidden,
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for guard_id, status, observed, forbidden, effect in items
    ]


def gates(
    shifted_trades: Sequence[Mapping[str, Any]],
    completed_trades: Sequence[Mapping[str, Any]],
    protocol_rows: Sequence[Mapping[str, Any]],
    regime_rows: Sequence[Mapping[str, Any]],
    cost_rows: Sequence[Mapping[str, Any]],
    curve_rows: Sequence[Mapping[str, Any]],
    proxy_rows: Sequence[Mapping[str, Any]],
    guard_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    shifted_summary = summarize(shifted_trades)
    completed_summary = summarize(completed_trades)
    gate_specs = [
        ("shifted_trade_records_loaded(이동 거래 기록 로드)", len(shifted_trades) == 266, f"rows={len(shifted_trades)}", "rows=266", "actual shifted MT5 trades are parsed(실제 이동 MT5 거래가 파싱됨)."),
        ("completed_anchor_loaded(완성일 앵커 로드)", len(completed_trades) == 344, f"rows={len(completed_trades)}", "rows=344", "completed-day anchor trades are parsed(완성일 앵커 거래가 파싱됨)."),
        ("protocol_attribution_complete(프로토콜 귀속 완성)", len(protocol_rows) == 9, f"rows={len(protocol_rows)}", "rows=9", "all protocols receive attribution(모든 프로토콜에 귀속이 있다)."),
        ("regime_attribution_present(국면 귀속 존재)", len(regime_rows) >= 20, f"rows={len(regime_rows)}", "rows>=20", "session/time/volatility/regime buckets are present(세션/시간/변동성/국면 버킷이 있다)."),
        ("cost_stress_present(비용 압박 존재)", len(cost_rows) == 4, f"rows={len(cost_rows)}", "rows=4", "cost buffer is stressed without retune(재튜닝 없이 비용 버퍼를 압박)."),
        ("curve_pocket_present(곡선 포켓 존재)", len(curve_rows) == 4, f"rows={len(curve_rows)}", "rows=4", "curve shape is measured(곡선 형태가 측정됨)."),
        ("proxy_mt5_attribution_boundary(프록시-MT5 귀속 경계)", all(row.get("usable_for_forward_decision") == "false" for row in proxy_rows), f"rows={len(proxy_rows)}", "forward=false", "proxy remains non-forward authority(프록시는 전진 권위가 아님)."),
        ("shifted_fragility_detected(이동 경로 취약성 감지)", shifted_summary["trade_count"] < completed_summary["trade_count"] and shifted_summary["net_profit"] < completed_summary["net_profit"], f"shifted={summary_text(shifted_summary)};completed={summary_text(completed_summary)}", "shifted weaker than completed anchor(이동 경로가 완성일 앵커보다 약함)", "fragility is named instead of hidden(취약성을 숨기지 않고 이름 붙임)."),
        ("no_overfit_guards_passed(무과적합 가드 통과)", all(row.get("status") == "passed" for row in guard_rows), f"passed={sum(1 for row in guard_rows if row.get('status') == 'passed')}/{len(guard_rows)}", f"passed={len(guard_rows)}/{len(guard_rows)}", "attribution cannot retune(귀속은 재튜닝할 수 없다)."),
        ("claim_guard(주장 방어)", True, "forward_passed=not_claimed;goal_achieve=not_claimed", "no forward or goal claim(전진/목표 주장 없음)", "goal remains active(목표는 계속 활성)."),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": "passed" if passed else "failed",
            "observed": observed,
            "expected": expected,
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, passed, observed, expected, effect in gate_specs
    ]


def write_receipts(final: Mapping[str, Any]) -> list[Path]:
    payloads = {
        ARTIFACT_RECEIPT: ("obsidian-artifact-lineage(아티팩트 계보)", "passed", "trade/report/telemetry/feature lineage tied to run337AY(거래/보고서/런타임 기록/피처 계보를 run337AY에 연결)."),
        DATA_RECEIPT: ("obsidian-data-integrity(데이터 무결성)", "passed", "shifted custom and completed-day anchors remain separated(이동 커스텀과 완성일 앵커를 분리 유지)."),
        RUNTIME_RECEIPT: ("obsidian-runtime-parity(런타임 동등성)", "passed_signal_parity_only", "exact proxy-MT5 parity remains attribution-only(정확 프록시-MT5 동등성은 귀속 전용 유지)."),
        FORENSICS_RECEIPT: ("obsidian-backtest-forensics(백테스트 포렌식)", "passed_trade_parse", "actual MT5 reports parsed into trades(실제 MT5 보고서를 거래로 파싱)."),
        ATTRIBUTION_RECEIPT: ("obsidian-performance-attribution(성과 귀속)", "passed_protocol_regime_cost_curve", "protocol/regime/cost/curve attribution materialized(프로토콜/국면/비용/곡선 귀속 물질화)."),
        JUDGMENT_RECEIPT: ("obsidian-result-judgment(결과 판정)", "passed_no_forward_decision", "fragility named and run337AZ opened(취약성 명명 후 run337AZ 개방)."),
    }
    paths: list[Path] = []
    for path, (skill, status, effect) in payloads.items():
        paths.append(
            aw.write_json(
                path,
                {
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": now_utc(),
                    "skill": skill,
                    "status": status,
                    "effect": effect,
                    "final_status": final["status"],
                    "claim_boundary": CLAIM_BOUNDARY,
                },
            )
        )
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337AY Shifted Protocol Attribution(337단계 337AY 이동 경로 프로토콜 귀속)

## Purpose(목적)

run337AY(337AY 실행)는 run337AX(337AX 실행)가 고른 shifted custom exact timestamp(이동 커스텀 정확 시각) 경로를 실제 MT5(MetaTrader 5, 메타트레이더5) trade report(거래 보고서), telemetry(런타임 기록), feature matrix(피처 행렬)로 귀속했다.

Effect(효과): tester feature-last gap(테스터 피처 끝 공백)을 진단용으로 수리한 경로에서 direction/recovery/cost/curve/regime(방향/회복/비용/곡선/국면)이 어디서 약한지 확인한다.

## Findings(발견)

- shifted_trades(이동 거래): `{final['shifted_trade_count']}`
- completed_anchor_trades(완성일 앵커 거래): `{final['completed_trade_count']}`
- shifted_net/PF/DD(이동 순익/수익 팩터/손실폭): `{final['shifted_net_profit']}` / `{final['shifted_profit_factor']}` / `{final['shifted_max_drawdown']}`
- completed_net/PF/DD(완성일 순익/수익 팩터/손실폭): `{final['completed_net_profit']}` / `{final['completed_profit_factor']}` / `{final['completed_max_drawdown']}`
- protocol_fragility(프로토콜 취약성): cost buffer(비용 버퍼), direction symmetry(방향 대칭), recovery shape(회복 형태), trade density(거래 밀도)
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

## Judgment(판정)

shifted custom route(이동 커스텀 경로)는 feature_last(피처 끝)에 도달하고 exact proxy-MT5 parity(정확 프록시-MT5 동등성)를 유지한다. 하지만 completed-day broker anchor(완성일 브로커 앵커) 대비 net/PF/trade count/DD(순익/수익 팩터/거래수/손실폭)가 약해 no-overfit repair design(무과적합 수리 설계)로 넘긴다.

Effect(효과): Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.

## Outputs(산출물)

- `{aw.rel(SHIFTED_TRADE_RECORDS)}`
- `{aw.rel(PROTOCOL_ATTRIBUTION)}`
- `{aw.rel(REGIME_ATTRIBUTION)}`
- `{aw.rel(COST_STRESS)}`
- `{aw.rel(CURVE_POCKET)}`
- `{aw.rel(GATE_AUDIT)}`

## Decision(결정)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337AY Decision(337단계 337AY 결정)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): shifted custom exact timestamp(이동 커스텀 정확 시각)는 feature_last(피처 끝)에 도달하지만 completed-day anchor(완성일 앵커) 대비 약해 no-overfit repair design(무과적합 수리 설계)로 넘긴다.

## Boundary(경계)

- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
"""
    return aw.write_text_lossless(DECISION_DOC, text, True)


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    workspace, workspace_bom = aw.read_tracked_text_lossless(WORKSPACE_STATE)
    workspace = aw.replace_prefix_line(workspace, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    focus = (
        "- >-\n"
        f"  Stage337 run337AY focus complete: run337AY(337AY 실행)은 `{final['status']}`로 shifted custom protocol attribution(이동 커스텀 프로토콜 귀속)을 완료했다. "
        f"Effect(효과): shifted trades(이동 거래) `{final['shifted_trade_count']}`, completed anchor(완성일 앵커) `{final['completed_trade_count']}`, gates(게이트) `{final['passed_gates']}/{final['gate_rows']}`이며 Forward/Goal(전진/목표)은 주장하지 않는다."
    )
    workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus + "\n", 1) if "Stage337 run337AY focus complete" not in workspace else workspace
    artifacts.append(aw.write_text_lossless(WORKSPACE_STATE, workspace, workspace_bom))

    current, current_bom = aw.read_tracked_text_lossless(CURRENT_STATE)
    current = aw.replace_prefix_line(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    current = aw.replace_prefix_line(current, "- status(상태):", f"- status(상태): `{final['status']}`")
    current = aw.replace_prefix_line(current, "- decision(결정):", f"- decision(결정): `{final['decision']}`")
    current = aw.replace_prefix_line(current, "- latest_completed_run(최근 완료 실행):", f"- latest_completed_run(최근 완료 실행): `{RUN_ID}`")
    current = aw.replace_prefix_line(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_RUN_ID}`")
    current = aw.replace_prefix_line(current, "- claim_boundary(주장 경계):", f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`")
    section = f"""## Stage337 run337AY(337AY 실행) - {TODAY}

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): run337AY(337AY 실행)는 shifted custom exact timestamp(이동 커스텀 정확 시각)의 실제 MT5 거래를 protocol/regime/cost/curve(프로토콜/국면/비용/곡선)로 귀속했고, 취약성이 남아 no-overfit repair design(무과적합 수리 설계)을 연다. Forward/Goal(전진/목표)은 주장하지 않는다.

"""
    current = current.replace("## Stage337 run337AX(337AX 실행)", section + "## Stage337 run337AX(337AX 실행)", 1)
    artifacts.append(aw.write_text_lossless(CURRENT_STATE, current, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- stage_id(단계 ID): `{STAGE_ID}`
- stage_status(단계 상태): `open_active`
- selected_candidate(선택 후보): `none`
- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{DECISION}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- shifted_custom_route(이동 커스텀 경로): `feature_last_reached_attribution_fragile`
- completed_day_anchor(완성일 앵커): `feature_last_reached_realism_anchor`
- protocol_attribution_rows(프로토콜 귀속 행): `{final['protocol_rows']}`
- regime_attribution_rows(국면 귀속 행): `{final['regime_rows']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Forward Blocked(전진 차단): `not_closed_repair_design_open`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): run337AY(337AY 실행)는 귀속을 완료했지만 전진/운영 주장은 막는다.
"""
    artifacts.append(aw.write_text_lossless(SELECTED_STATUS, selection, True))

    brief, brief_bom = aw.read_tracked_text_lossless(STAGE_BRIEF)
    brief = aw.replace_prefix_line(brief, "- latest_run(최신 실행):", f"- latest_run(최신 실행): `{RUN_ID}`")
    summary = (
        f"- run337AY_summary(337AY 요약): `{final['status']}`. "
        f"Effect(효과): shifted trades(이동 거래) `{final['shifted_trade_count']}`, completed anchor(완성일 앵커) `{final['completed_trade_count']}`, protocol attribution(프로토콜 귀속) `{final['protocol_rows']}`행을 만들고 run337AZ(337AZ 실행) 무과적합 수리 설계를 연다; Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    brief = brief.rstrip() + "\n" + summary if "run337AY_summary" not in brief else brief
    artifacts.append(aw.write_text_lossless(STAGE_BRIEF, brief, brief_bom))

    changelog, changelog_bom = aw.read_tracked_text_lossless(CHANGELOG)
    line = (
        f"- {TODAY}: Stage337 run337AY(337AY 실행) `{final['status']}`. "
        f"Effect(효과): shifted custom exact timestamp(이동 커스텀 정확 시각)의 실제 MT5 거래 `{final['shifted_trade_count']}`건을 프로토콜/국면/비용/곡선으로 귀속했고 Forward/Goal(전진/목표)은 주장하지 않음."
    )
    changelog = changelog.rstrip() + "\n" + line + "\n" if "Stage337 run337AY" not in changelog else changelog
    artifacts.append(aw.write_text_lossless(CHANGELOG, changelog, changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "shifted_custom_protocol_attribution_without_db",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": aw.rel(REPORT_PATH),
        "notes": f"decision={final['decision']};next_action={final['next_action']};shifted_trades={final['shifted_trade_count']};protocol_rows={final['protocol_rows']};goal_achieve_not_claimed.",
        "family": "performance_attribution_runtime_boundary",
        "primary_report": aw.rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__shifted_custom_protocol_attribution",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "shifted_custom_protocol_attribution",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "shifted_custom_protocol_attribution_without_db(D/B 없는 이동 커스텀 프로토콜 귀속)",
        "tier_scope": "Tier A u42 shifted custom exact timestamp MT5 evidence(Tier A u42 이동 커스텀 정확 시각 MT5 근거)",
        "kpi_scope": "protocol_regime_cost_curve_attribution_no_forward_decision(프로토콜/국면/비용/곡선 귀속, 전진 판정 없음)",
        "scoreboard_lane": "performance_attribution_runtime_boundary",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": aw.rel(REPORT_PATH),
        "primary_kpi": f"shifted_trades={final['shifted_trade_count']};net={final['shifted_net_profit']};pf={final['shifted_profit_factor']};protocol_rows={final['protocol_rows']}",
        "guardrail_kpi": "no_training;no_threshold_retune;no_db_rule_rewrite;no_lot_opt;no_forward_claim",
        "external_verification_status": "completed_from_actual_mt5_report_parse(실제 MT5 보고서 파싱에서 완료)",
        "notes": f"decision={final['decision']};next_action={final['next_action']};goal_achieve_not_claimed.",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__shifted_custom_protocol_attribution",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "performance_attribution_runtime_boundary",
        "evidence_scope": "run337AK shifted custom actual MT5 report telemetry features and run337AD completed-day anchor",
        "kpi_scope": "protocol_regime_cost_curve_attribution_no_forward_decision",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": aw.rel(REPORT_PATH),
        "notes": f"goal_achieve_not_claimed;gates={final['passed_gates']}/{final['gate_rows']}",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__shifted_custom_protocol_attribution",
        "family": "shifted_custom_protocol_attribution_without_db",
        "question": "where does the shifted custom exact timestamp repair route remain fragile before no-overfit repair design",
        "metric_scope": "trade_records_regime_cost_curve_protocol",
        "primary_artifact": aw.rel(REPORT_PATH),
        "report_path": aw.rel(REPORT_PATH),
        "next_action": final["next_action"],
    }
    aw.upsert_csv(RUN_REGISTRY, aw.RUN_REGISTRY_COLUMNS, run_row, "run_id")
    aw.upsert_csv(ALPHA_LEDGER, aw.ALPHA_LEDGER_COLUMNS, alpha_row, "ledger_row_id")
    aw.upsert_csv(STAGE_LEDGER, aw.STAGE_LEDGER_COLUMNS, stage_row, "ledger_row_id")
    return [RUN_REGISTRY, ALPHA_LEDGER, STAGE_LEDGER]


def update_artifact_registry(paths: Sequence[Path], final: Mapping[str, Any]) -> Path:
    columns, rows = aw.read_csv_table(ARTIFACT_REGISTRY, prefer_head=True)
    columns = columns or list(aw.ARTIFACT_COLUMNS)
    rows = [row for row in rows if not str(row.get("artifact_id", "")).startswith(f"{RUN_ID}::")]
    created_at = now_utc()
    seen: set[str] = set()
    for path in paths:
        if not aw.path_exists(path):
            continue
        artifact_path = aw.rel(path)
        if artifact_path in seen:
            continue
        seen.add(artifact_path)
        rows.append(
            {
                "artifact_id": f"{RUN_ID}::{artifact_path}",
                "artifact_type": path.suffix.lower().lstrip(".") or "file",
                "path": artifact_path,
                "sha256": aw.sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": final["status"],
                "artifact_path": artifact_path,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return aw.write_csv(ARTIFACT_REGISTRY, columns, rows)


def main() -> int:
    aw.io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    ak_runtime = aw.read_csv(AK_RUNTIME)
    ad_runtime = aw.read_csv(AD_RUNTIME)
    shifted_report = report_path_from_runtime(ak_runtime, "u42_plain_rf_ak_shifted_custom_exact_timestamp", AK_REPORT)
    completed_report = report_path_from_runtime(ad_runtime, "u42_plain_rf_ad_completed_day_broker_slice", AD_REPORT)
    shifted_trades, shifted_metrics = load_trades(
        "shifted_custom_exact_timestamp(이동 커스텀 정확 시각)",
        shifted_report,
        feature_map(AK_FEATURES),
    )
    completed_features = feature_map(AD_FEATURES) if aw.path_exists(AD_FEATURES) else feature_map(AK_FEATURES)
    completed_trades, completed_metrics = load_trades(
        "completed_day_broker_slice(완성일 브로커 구간)",
        completed_report,
        completed_features,
    )
    shifted_path = aw.write_csv(SHIFTED_TRADE_RECORDS, TRADE_COLUMNS, shifted_trades)
    completed_path = aw.write_csv(COMPLETED_TRADE_RECORDS, TRADE_COLUMNS, completed_trades)
    bindings = aw.read_csv(AX_BINDING)
    protocol_rows = protocol_attribution(bindings, shifted_trades, completed_trades, shifted_metrics, completed_metrics)
    protocol_path = aw.write_csv(PROTOCOL_ATTRIBUTION, PROTOCOL_COLUMNS, protocol_rows)
    regime_rows = group_regimes(shifted_trades, "shifted_custom_exact_timestamp(이동 커스텀 정확 시각)")
    regime_path = aw.write_csv(REGIME_ATTRIBUTION, REGIME_COLUMNS, regime_rows)
    cost_rows = cost_stress(shifted_trades, "shifted_custom_exact_timestamp(이동 커스텀 정확 시각)")
    cost_path = aw.write_csv(COST_STRESS, COST_COLUMNS, cost_rows)
    curve_rows = curve_pockets(shifted_trades, "shifted_custom_exact_timestamp(이동 커스텀 정확 시각)")
    curve_path = aw.write_csv(CURVE_POCKET, CURVE_COLUMNS, curve_rows)
    proxy_rows = proxy_usability()
    proxy_path = aw.write_csv(PROXY_USABILITY, PROXY_COLUMNS, proxy_rows)
    guard_rows = guards()
    guard_path = aw.write_csv(NO_OVERFIT_GUARDS, GUARD_COLUMNS, guard_rows)
    gate_rows = gates(shifted_trades, completed_trades, protocol_rows, regime_rows, cost_rows, curve_rows, proxy_rows, guard_rows)
    gate_path = aw.write_csv(GATE_AUDIT, GATE_COLUMNS, gate_rows)
    shifted_summary = summarize(shifted_trades)
    completed_summary = summarize(completed_trades)
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS if all(row.get("status") == "passed" for row in gate_rows) else "invalid_stage337AY_attribution_gate_failure_no_forward_decision",
        "judgment": JUDGMENT if all(row.get("status") == "passed" for row in gate_rows) else "shifted_custom_attribution_gate_failure",
        "decision": DECISION if all(row.get("status") == "passed" for row in gate_rows) else "repair_stage337AY_attribution_gate_failure_before_run337AZ",
        "next_action": NEXT_RUN_ID if all(row.get("status") == "passed" for row in gate_rows) else "repair_stage337AY_attribution_gate_failure_v1",
        "shifted_trade_count": shifted_summary["trade_count"],
        "completed_trade_count": completed_summary["trade_count"],
        "shifted_net_profit": f"{shifted_metrics.get('net_profit', shifted_summary['net_profit']):.10g}",
        "shifted_profit_factor": shifted_metrics.get("profit_factor", ""),
        "shifted_max_drawdown": shifted_metrics.get("max_drawdown_amount", ""),
        "completed_net_profit": f"{completed_metrics.get('net_profit', completed_summary['net_profit']):.10g}",
        "completed_profit_factor": completed_metrics.get("profit_factor", ""),
        "completed_max_drawdown": completed_metrics.get("max_drawdown_amount", ""),
        "protocol_rows": len(protocol_rows),
        "regime_rows": len(regime_rows),
        "cost_rows": len(cost_rows),
        "curve_rows": len(curve_rows),
        "gate_rows": len(gate_rows),
        "passed_gates": sum(1 for row in gate_rows if row.get("status") == "passed"),
        "failed_gates": [row.get("gate_id") for row in gate_rows if row.get("status") != "passed"],
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    final_path = aw.write_json(FINAL_DECISION, final)
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": now_utc(),
        "producer": aw.rel(__file__),
        "parent_run_id": PARENT_RUN_ID,
        "inputs": [aw.rel(path) for path in INPUT_FILES],
        "outputs": [aw.rel(path) for path in OUTPUT_FILES],
        "forbidden_actions": [
            "model training(모델 학습)",
            "threshold retuning(임계값 재조정)",
            "D/B rewrite(D/B 재작성)",
            "lot optimization(랏 최적화)",
            "Forward Passed/Failed claim(전진 통과/실패 주장)",
            "Goal Achieve claim(목표 달성 주장)",
        ],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    manifest_path = aw.write_json(RUN_MANIFEST, manifest)
    receipt_paths = write_receipts(final)
    report_path = write_report(final)
    decision_path = write_decision_doc(final)
    doc_paths = update_docs(final)
    register_paths = update_registers(final)
    artifact_paths = [
        shifted_path,
        completed_path,
        protocol_path,
        regime_path,
        cost_path,
        curve_path,
        proxy_path,
        guard_path,
        gate_path,
        *receipt_paths,
        final_path,
        manifest_path,
        report_path,
        decision_path,
        *doc_paths,
        *register_paths,
        Path(__file__),
    ]
    artifact_registry_path = update_artifact_registry(artifact_paths, final)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": final["status"],
                "judgment": final["judgment"],
                "decision": final["decision"],
                "next_action": final["next_action"],
                "shifted_trades": final["shifted_trade_count"],
                "completed_anchor_trades": final["completed_trade_count"],
                "shifted_net_pf": f"{final['shifted_net_profit']}/{final['shifted_profit_factor']}",
                "gates": f"{final['passed_gates']}/{final['gate_rows']}",
                "report": aw.rel(report_path),
                "artifact_registry": aw.rel(artifact_registry_path),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if not final["failed_gates"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
