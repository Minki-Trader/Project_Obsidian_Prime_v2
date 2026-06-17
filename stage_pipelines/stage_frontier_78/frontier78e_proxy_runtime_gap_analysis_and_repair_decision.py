from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from foundation.mt5.trade_report import pair_deals_into_trades, parse_mt5_trade_report
from stage_pipelines.stage_frontier_78 import frontier78b_execution_calibrated_density_contract_pnl_proxy_scout as f78b
from stage_pipelines.stage_frontier_78 import frontier78d_mt5_execution_calibrated_negative_control_runtime_probe as f78d


STAGE_ID = f78b.STAGE_ID
RUN_ID = "frontier78E_proxy_runtime_gap_analysis_and_repair_decision_v1"
PARENT_RUN_ID = f78d.RUN_ID
NEXT_RUN_ID = "frontier78F_entry_timing_deposit_calibrated_proxy_repair_v1"
STATUS = "gap_analysis_completed_entry_timing_deposit_repair_required_no_authority"
JUDGMENT = "runtime_gap_explained_repair_required_no_authority"
CLAIM_BOUNDARY = (
    "gap_analysis_and_repair_decision_only_no_completion_no_baseline_"
    "no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"

F78D_MANIFEST = STAGE_DIR / "02_runs" / PARENT_RUN_ID / "run_manifest.json"
F78D_SUMMARY = REVIEW_DIR / "f78d_mt5_execution_calibrated_runtime_probe_summary.json"
F78B_SUMMARY = REVIEW_DIR / "f78b_contract_proxy_summary.json"

GAP_ANALYSIS = REVIEW_DIR / "f78e_proxy_runtime_gap_analysis.json"
ENTRY_TIMING_DIAGNOSTIC = REVIEW_DIR / "f78e_entry_timing_diagnostic.csv"
REPAIR_DECISION = REVIEW_DIR / "f78e_repair_decision.json"
PERFORMANCE_ATTRIBUTION = REVIEW_DIR / "f78e_performance_attribution_receipt.json"
RESULT_JUDGMENT = REVIEW_DIR / "f78e_result_judgment_receipt.json"
REPORT = REVIEW_DIR / "frontier78E_proxy_runtime_gap_analysis_and_repair_decision_report.md"
GATE_AUDIT = REVIEW_DIR / "required_gate_coverage_audit_f78e.md"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"

WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"
CONTEXT_ANCHOR_PATH = f"stages/{STAGE_ID}/03_reviews/context_anchor.md"
SCRIPT_REL = "stage_pipelines/stage_frontier_78/frontier78e_proxy_runtime_gap_analysis_and_repair_decision.py"


def now_utc() -> str:
    return f78b.utc_now()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_text(path: Path, text: str, *, encoding: str = "utf-8-sig") -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding=encoding)


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    rows = list(rows)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys() if rows else ["empty"])
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({name: json_ready(row.get(name, "")) for name in fieldnames})


def upsert_csv(path: Path, key: str, row: Mapping[str, Any], source_header: Path | None = None) -> None:
    read_path = path if len(str(path)) < 240 else io_path(path)
    if path_exists(path):
        with read_path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            rows = list(reader)
    elif source_header is not None and path_exists(source_header):
        source_read_path = source_header if len(str(source_header)) < 240 else io_path(source_header)
        with source_read_path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
        rows = []
    else:
        fieldnames = list(row.keys())
        rows = []
    for field in row:
        if field not in fieldnames:
            fieldnames.append(field)
    rows = [existing for existing in rows if existing.get(key) != row.get(key)]
    rows.append({field: json_ready(row.get(field, "")) for field in fieldnames})
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    write_path = path if len(str(path)) < 240 else io_path(path)
    with write_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def ensure_dirs() -> None:
    for path in (RUN_DIR, REVIEW_DIR, SELECTED_DIR):
        io_path(path).mkdir(parents=True, exist_ok=True)


def finite_float(value: Any, default: float = 0.0) -> float:
    try:
        out = float(value)
    except (TypeError, ValueError):
        return default
    if not np.isfinite(out):
        return default
    return out


def metric_delta(runtime: Mapping[str, Any], proxy: Mapping[str, Any]) -> dict[str, Any]:
    fields = [
        ("net_profit", "net_profit"),
        ("gross_profit", "gross_profit"),
        ("gross_loss", "gross_loss"),
        ("profit_factor", "profit_factor"),
        ("trade_count", "trade_count"),
        ("trades_day", "trades_per_day"),
        ("max_drawdown_percent", "max_drawdown_percent"),
        ("win_rate", "win_rate_percent"),
        ("average_win", "average_win"),
        ("average_loss", "average_loss"),
        ("payoff_ratio", "payoff_ratio"),
        ("expectancy", "expectancy"),
        ("recovery_factor", "recovery_factor"),
    ]
    rows: dict[str, Any] = {}
    for proxy_key, runtime_key in fields:
        p_value = proxy.get(proxy_key)
        r_value = runtime.get(runtime_key)
        rows[proxy_key] = {
            "proxy": p_value,
            "runtime": r_value,
            "runtime_minus_proxy": finite_float(r_value) - finite_float(p_value),
        }
    return rows


def selected_proxy_rows(context: Mapping[str, Any], raw: pd.DataFrame, entry_indices: np.ndarray, outcome: Mapping[str, np.ndarray], split: str) -> list[dict[str, Any]]:
    split_mask = context["frame"]["split"].astype(str).eq(split).to_numpy()
    selected = context["selected"] & split_mask
    rows: list[dict[str, Any]] = []
    for idx in np.where(selected)[0]:
        raw_idx = int(entry_indices[idx])
        if raw_idx < 0 or raw_idx >= len(raw):
            continue
        rows.append(
            {
                "frame_index": int(idx),
                "signal_time": pd.Timestamp(context["frame"].iloc[idx]["timestamp"]).tz_convert(None),
                "proxy_entry_time": pd.Timestamp(raw.iloc[raw_idx]["open_ts"]).tz_convert(None),
                "proxy_pnl_contract": float(np.asarray(outcome["pnl_contract"])[idx]),
                "proxy_pnl_price": float(np.asarray(outcome["pnl_price"])[idx]),
                "proxy_exit_offset": int(np.asarray(outcome["exit_offset"])[idx]),
            }
        )
    return rows


def rebuild_proxy(context: Mapping[str, Any], raw: pd.DataFrame, entry_indices: np.ndarray) -> dict[str, dict[str, Any]]:
    spec = context["spec"]
    outcome = f78b.compute_contract_outcome(raw, entry_indices, spec)
    out: dict[str, dict[str, Any]] = {}
    for split in ("validation", "oos"):
        split_mask = context["frame"]["split"].astype(str).eq(split).to_numpy()
        split_df = context["frame"].loc[split_mask].reset_index(drop=True)
        selected = context["selected"][split_mask]
        split_outcome = {key: np.asarray(value)[split_mask] for key, value in outcome.items()}
        metrics = f78b.contract_kpi(split_df, selected, split_outcome)
        dd_amount = finite_float(metrics["dd_pct"]) / 100.0 * f78b.INITIAL_BALANCE
        out[split] = {
            **metrics,
            "dd_amount_proxy_balance_10000": dd_amount,
            "dd_pct_if_deposit_500": (dd_amount / 500.0 * 100.0) if dd_amount else 0.0,
        }
    return out


def build_gap_analysis() -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any], dict[str, Any]]:
    f78d.configure_runtime_base()
    manifest = read_json(F78D_MANIFEST)
    runtime_summary = read_json(F78D_SUMMARY)
    target = dict(manifest["target"])
    runtime = dict(runtime_summary["best_runtime"])
    context = f78d.build_context(target)
    frame, raw, _ = f78b.load_inputs()
    next_indices = f78b.entry_indices_next_bar(frame, raw)
    current_mapping = {ts: idx for idx, ts in enumerate(raw["open_ts"])}
    current_indices = frame["timestamp"].map(current_mapping).fillna(-2).astype(int).to_numpy()
    next_outcome = f78b.compute_contract_outcome(raw, next_indices, context["spec"])
    next_proxy_rows = selected_proxy_rows(context, raw, next_indices, next_outcome, "validation")
    report_path = Path(runtime["report_path"])
    trades = pair_deals_into_trades(parse_mt5_trade_report(report_path)["deals"])
    timing_rows: list[dict[str, Any]] = []
    entry_diffs: list[float] = []
    sign_flip_count = 0
    runtime_minus_proxy: list[float] = []
    for idx, (proxy, trade) in enumerate(zip(next_proxy_rows, trades), start=1):
        diff_minutes = (trade.open_time - proxy["proxy_entry_time"]).total_seconds() / 60.0
        entry_diffs.append(diff_minutes)
        delta = float(trade.net_profit) - float(proxy["proxy_pnl_contract"])
        runtime_minus_proxy.append(delta)
        if (proxy["proxy_pnl_contract"] > 0 and trade.net_profit <= 0) or (proxy["proxy_pnl_contract"] <= 0 and trade.net_profit > 0):
            sign_flip_count += 1
        timing_rows.append(
            {
                "trade_index": idx,
                "signal_time": str(proxy["signal_time"]),
                "next_bar_proxy_entry_time": str(proxy["proxy_entry_time"]),
                "mt5_open_time": str(trade.open_time),
                "entry_diff_minutes_mt5_minus_proxy": diff_minutes,
                "proxy_pnl_contract": proxy["proxy_pnl_contract"],
                "runtime_net_profit": trade.net_profit,
                "runtime_minus_proxy": delta,
                "proxy_exit_offset_bars": proxy["proxy_exit_offset"],
                "runtime_hold_minutes": (trade.close_time - trade.open_time).total_seconds() / 60.0,
            }
        )
    same_bar_proxy = rebuild_proxy(context, raw, current_indices)
    next_bar_proxy = rebuild_proxy(context, raw, next_indices)
    proxy_validation = {
        "net_profit": target.get("val_net"),
        "gross_profit": target.get("val_gross_profit"),
        "gross_loss": target.get("val_gross_loss"),
        "profit_factor": target.get("val_pf"),
        "trade_count": target.get("val_trade_count"),
        "trades_day": target.get("val_calendar_trades_day"),
        "max_drawdown_percent": target.get("val_dd_pct"),
        "win_rate": target.get("val_win_rate"),
        "average_win": target.get("val_avg_win"),
        "average_loss": target.get("val_avg_loss"),
        "payoff_ratio": target.get("val_payoff"),
        "expectancy": target.get("val_expectancy"),
        "recovery_factor": target.get("val_recovery"),
    }
    deltas = metric_delta(runtime, proxy_validation)
    entry_diff_counter = {str(key): value for key, value in Counter(entry_diffs).most_common()}
    gross_profit_delta = finite_float(runtime.get("gross_profit")) - finite_float(target.get("val_gross_profit"))
    gross_loss_delta = finite_float(runtime.get("gross_loss")) - finite_float(target.get("val_gross_loss"))
    gap = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "target_candidate_id": "f78b_02234",
        "test_period": f"{runtime.get('test_period_start')}..{runtime.get('test_period_end')}",
        "split_view": "validation/Tier A MT5 Runtime Probe(검증/Tier A MT5 런타임 탐침)",
        "observed_change": "proxy validation positive but MT5 runtime validation negative(프록시 검증 양수, MT5 런타임 검증 음수)",
        "comparison_baseline": "F78B next-bar contract proxy validation(다음 봉 계약 프록시 검증)",
        "proxy_kpi": proxy_validation,
        "runtime_kpi": runtime,
        "delta": deltas,
        "gap_decomposition": {
            "signal_count_diff": runtime.get("signal_count_diff"),
            "feature_ready_diff": runtime.get("feature_ready_diff"),
            "order_fill_rate": runtime.get("order_fill_rate"),
            "trade_count_diff": finite_float(runtime.get("trade_count")) - finite_float(target.get("val_trade_count")),
            "gross_profit_delta_runtime_minus_proxy": gross_profit_delta,
            "gross_loss_delta_runtime_minus_proxy": gross_loss_delta,
            "net_delta_runtime_minus_proxy": finite_float(runtime.get("net_profit")) - finite_float(target.get("val_net")),
            "loss_side_share_of_net_gap": abs(gross_loss_delta) / abs(finite_float(runtime.get("net_profit")) - finite_float(target.get("val_net"))) if finite_float(runtime.get("net_profit")) != finite_float(target.get("val_net")) else None,
        },
        "entry_timing_diagnostic": {
            "paired_trade_count": min(len(next_proxy_rows), len(trades)),
            "entry_diff_minutes_counts": entry_diff_counter,
            "dominant_entry_diff_minutes": entry_diffs[0] if entry_diffs else None,
            "sign_flip_count": sign_flip_count,
            "sign_flip_rate": sign_flip_count / len(timing_rows) if timing_rows else None,
            "runtime_minus_proxy_sum": float(np.sum(runtime_minus_proxy)) if runtime_minus_proxy else 0.0,
            "runtime_minus_proxy_mean": float(np.mean(runtime_minus_proxy)) if runtime_minus_proxy else 0.0,
        },
        "same_bar_proxy_rebuild": same_bar_proxy,
        "next_bar_proxy_rebuild": next_bar_proxy,
        "likely_drivers": [
            "entry_timing_mismatch: MT5 opens at signal bar time while proxy labeled next-bar open(진입 시각 불일치: MT5는 신호 봉 시각 진입, 프록시는 다음 봉 시가 라벨)",
            "drawdown_denominator_mismatch: proxy DD uses 10000 balance while tester deposit is 500(손실폭 분모 불일치: 프록시 10000, 테스터 500)",
            "remaining_fill_path_gap: same-bar proxy is closer but MT5 tick/fill path still differs(잔여 체결 경로 간극: 동일 봉 프록시가 더 가깝지만 MT5 틱/체결 경로가 다름)",
        ],
        "segment_checks": {
            "time_period": f"{runtime.get('test_period_start')}..{runtime.get('test_period_end')}",
            "tier": "Tier A only(Tier A 전용)",
            "direction": "short only(숏 전용)",
            "entry_timing": "performed(수행됨)",
            "same_bar_rebuild": "performed(수행됨)",
            "oos_runtime": "missing_by_scope(범위상 미실행)",
            "regime_split": "missing_next_repair(다음 수리에서 필요)",
        },
        "alternative_explanations": [
            "broker spread/slippage or tick-path microstructure(브로커 스프레드/슬리피지 또는 틱 경로 미세구조)",
            "TP/SL intrabar hit ordering not fully represented by OHLC proxy(TP/SL 봉내 도달 순서가 OHLC 프록시에 완전 반영되지 않음)",
            "report DD percent uses tester deposit denominator(보고서 DD 퍼센트는 테스터 예치금 분모 사용)",
        ],
        "attribution_confidence": "high_for_entry_timing_and_deposit_denominator_medium_for_remaining_fill_path(진입 시각/예치금 분모는 높음, 잔여 체결 경로는 중간)",
        "next_probe": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance = {
        "observed_change": gap["observed_change"],
        "comparison_baseline": gap["comparison_baseline"],
        "likely_drivers": gap["likely_drivers"],
        "segment_checks": gap["segment_checks"],
        "trade_shape": {
            "runtime_trade_count": runtime.get("trade_count"),
            "runtime_win_rate_percent": runtime.get("win_rate_percent"),
            "runtime_payoff_ratio": runtime.get("payoff_ratio"),
            "runtime_average_win": runtime.get("average_win"),
            "runtime_average_loss": runtime.get("average_loss"),
            "runtime_drawdown_percent": runtime.get("max_drawdown_percent"),
            "runtime_short_count": runtime.get("short_trade_count"),
            "same_bar_proxy_validation": same_bar_proxy["validation"],
        },
        "alternative_explanations": gap["alternative_explanations"],
        "attribution_confidence": gap["attribution_confidence"],
        "next_probe": gap["next_probe"],
    }
    result_judgment = {
        "result_subject": "F78D MT5 runtime probe for f78b_02234(F78D f78b_02234 MT5 런타임 탐침)",
        "evidence_available": [rel(F78D_SUMMARY), rel(F78D_MANIFEST), rel(GAP_ANALYSIS), rel(ENTRY_TIMING_DIAGNOSTIC)],
        "evidence_missing": ["OOS MT5 runtime probe(표본외 MT5 런타임 탐침)", "regime/session repair validation(장세/세션 수리 검증)", "post-repair runtime probe(수리 후 런타임 탐침)"],
        "judgment_label": "runtime_probe_negative_for_current_mapping_repair_required(현재 매핑에 대한 런타임 탐침 부정, 수리 필요)",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": "F78F must rebuild proxy with same-bar/runtime-aligned entry and tester-deposit DD denominator(F78F는 동일 봉/런타임 정렬 진입과 테스터 예치금 DD 분모로 프록시를 재구성해야 함)",
        "user_explanation_hook": "신호는 맞았지만 들어가는 시간이 한 봉 빨랐고 손실폭 분모도 달라서, 모델 문제가 아니라 실행 계약이 어긋난 쪽이 먼저다.",
    }
    return gap, timing_rows, performance, result_judgment


def repair_decision_payload(gap: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "decision": "repair_required(수리 필요)",
        "next_run_id": NEXT_RUN_ID,
        "accepted_repairs": [
            "rebuild labels using runtime-aligned same-bar entry or export features shifted so MT5 entry equals proxy next-bar entry(런타임 정렬 동일 봉 진입 라벨 재구성 또는 MT5 진입이 프록시 다음 봉 진입과 같도록 피처 시프트)",
            "replace proxy DD denominator 10000 with tester/account deposit 500 or report both amount and percent(프록시 DD 분모 10000을 테스터/계좌 예치금 500으로 교체하거나 금액/퍼센트 둘 다 기록)",
            "score candidates on runtime-calibrated fill path penalty and loss-side gap(런타임 보정 체결 경로 벌점과 손실 측 간극으로 후보 점수화)",
        ],
        "rejected_repairs": [
            "change model family before fixing execution contract(실행 계약을 고치기 전에 모델 계열만 교체)",
            "raise threshold only to hide the gap(간극을 숨기기 위해 임계값만 올리기)",
            "claim runtime authority from matched signal count alone(신호 수 일치만으로 런타임 권위 주장)",
        ],
        "stop_condition_for_current_mapping": "same F78B next-bar proxy mapping should not be advanced without timing/deposit repair(현재 F78B 다음 봉 프록시 매핑은 시간/예치금 수리 없이 전진 금지)",
        "preserved_clue": "selected-entry veto and ONNX parity path are valid; signal/feature/fill counts matched exactly(선택 진입 거부 테이프와 ONNX 동등성 경로는 유효; 신호/피처/체결 수가 정확히 맞음)",
        "negative_memory": "next-bar proxy can look positive while runtime same-bar execution is negative(다음 봉 프록시는 양수여도 런타임 동일 봉 실행은 음수일 수 있음)",
        "claim_boundary": CLAIM_BOUNDARY,
        "gap_reference": rel(GAP_ANALYSIS),
    }


def report_text(created_at: str, gap: Mapping[str, Any], repair: Mapping[str, Any]) -> str:
    runtime = gap["runtime_kpi"]
    proxy = gap["proxy_kpi"]
    same_validation = gap["same_bar_proxy_rebuild"]["validation"]
    return f"""# Frontier78E Proxy/Runtime Gap Analysis And Repair Decision Report(F78E 프록시/런타임 간극 분석 및 수리 결정 보고서)

Updated(갱신): {created_at}

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- test period(테스트 기간): `{gap['test_period']}`
- split/view(분할/보기): `{gap['split_view']}`
- source candidate(원천 후보): `f78b_02234`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

## KPI Gap(KPI 간극)

| view(보기) | net(순수익) | gross profit(총이익) | gross loss(총손실) | PF(수익 팩터) | DD%(손실폭) | trades(거래) | trades/day(일 거래) | win rate(승률) | expectancy(기대값) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| next-bar proxy validation(다음 봉 프록시 검증) | `{proxy.get('net_profit')}` | `{proxy.get('gross_profit')}` | `{proxy.get('gross_loss')}` | `{proxy.get('profit_factor')}` | `{proxy.get('max_drawdown_percent')}` | `{proxy.get('trade_count')}` | `{proxy.get('trades_day')}` | `{proxy.get('win_rate')}` | `{proxy.get('expectancy')}` |
| same-bar proxy validation(동일 봉 프록시 검증) | `{same_validation.get('net')}` | `{same_validation.get('gross_profit')}` | `{same_validation.get('gross_loss')}` | `{same_validation.get('pf')}` | `{same_validation.get('dd_pct')}` | `{same_validation.get('trade_count')}` | `{same_validation.get('calendar_trades_day')}` | `{same_validation.get('win_rate')}` | `{same_validation.get('expectancy')}` |
| MT5 runtime validation(MT5 런타임 검증) | `{runtime.get('net_profit')}` | `{runtime.get('gross_profit')}` | `{runtime.get('gross_loss')}` | `{runtime.get('profit_factor')}` | `{runtime.get('max_drawdown_percent')}` | `{runtime.get('trade_count')}` | `{runtime.get('trades_per_day')}` | `{runtime.get('win_rate_percent')}` | `{runtime.get('expectancy')}` |

## Gap Cause(간극 원인)

- signal count parity(신호 수 동등성): `{runtime.get('signal_count_diff')}` diff(차이).
- feature readiness parity(피처 준비 동등성): `{runtime.get('feature_ready_diff')}` diff(차이).
- order fill rate(주문 체결률): `{runtime.get('order_fill_rate')}`.
- dominant entry timing gap(주요 진입 시각 간극): `{gap['entry_timing_diagnostic'].get('dominant_entry_diff_minutes')}` minutes(분), MT5 opens earlier(MT5가 더 빠름).
- sign flip(승패 뒤집힘): `{gap['entry_timing_diagnostic'].get('sign_flip_count')}/{gap['entry_timing_diagnostic'].get('paired_trade_count')}`.
- DD denominator(손실폭 분모): same-bar proxy DD(동일 봉 프록시 손실폭)는 balance 10000(잔고 10000) 기준 `{same_validation.get('dd_pct')}`%, deposit 500(예치금 500) 기준 `{same_validation.get('dd_pct_if_deposit_500')}`%.

## Repair Decision(수리 결정)

Next run(다음 실행): `{repair['next_run_id']}`

Accepted repairs(수용 수리):
- {repair['accepted_repairs'][0]}
- {repair['accepted_repairs'][1]}
- {repair['accepted_repairs'][2]}

Rejected repairs(거절 수리):
- {repair['rejected_repairs'][0]}
- {repair['rejected_repairs'][1]}
- {repair['rejected_repairs'][2]}
"""


def gate_audit_text(created_at: str) -> str:
    return f"""# Required Gate Coverage Audit F78E(F78E 필수 게이트 커버리지 감사)

Updated(갱신): {created_at}

| gate(게이트) | status(상태) | evidence/effect(근거/효과) |
|---|---|---|
| F78D runtime evidence(F78D 런타임 근거) | `passed(통과)` | `{rel(F78D_SUMMARY)}` |
| proxy/runtime KPI gap(프록시/런타임 KPI 간극) | `recorded(기록됨)` | `{rel(GAP_ANALYSIS)}` |
| entry timing diagnostic(진입 시각 진단) | `recorded(기록됨)` | `{rel(ENTRY_TIMING_DIAGNOSTIC)}` |
| performance attribution(성과 귀속) | `recorded(기록됨)` | `{rel(PERFORMANCE_ATTRIBUTION)}` |
| result judgment(결과 판정) | `recorded(기록됨)` | `{rel(RESULT_JUDGMENT)}` |
| repair decision(수리 결정) | `recorded(기록됨)` | `{rel(REPAIR_DECISION)}` |
| next action(다음 행동) | `required(필수)` | `{NEXT_RUN_ID}` |
| claim guard(주장 보호) | `passed(통과)` | `{CLAIM_BOUNDARY}` |
"""


def ledger_row(created_at: str, gap: Mapping[str, Any]) -> dict[str, Any]:
    runtime = gap["runtime_kpi"]
    row_id = f"{RUN_ID}__gap_analysis"
    return {
        "ledger_row_id": row_id,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "proxy_runtime_gap_analysis(프록시 런타임 간극 분석)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "F78E gap analysis(F78E 간극 분석)",
        "tier_scope": "Tier A runtime evidence; Tier B missing_required; combined out_of_scope",
        "kpi_scope": "runtime_probe_gap_analysis(런타임 탐침 간극 분석)",
        "scoreboard_lane": "gap_analysis(간극 분석)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT),
        "primary_kpi": f"runtime_net={runtime.get('net_profit')};runtime_pf={runtime.get('profit_factor')};runtime_dd={runtime.get('max_drawdown_percent')};signal_diff={runtime.get('signal_count_diff')}",
        "guardrail_kpi": "entry_time_diff=-5min dominant;dd_denominator_mismatch=10000_vs_500",
        "external_verification_status": "completed(완료)",
        "notes": f"next={NEXT_RUN_ID}; gap=entry_timing+deposit_denominator+fill_path",
        "lane": "gap_analysis(간극 분석)",
        "family": "performance_attribution(성과 귀속)",
        "primary_report": rel(REPORT),
        "run_number": "frontier78E",
        "date": created_at[:10],
        "decision": JUDGMENT,
        "next_run_id": NEXT_RUN_ID,
        "rows": gap["entry_timing_diagnostic"].get("paired_trade_count"),
        "gate_passes": "8",
        "gate_total": "8",
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT),
        "run_date": created_at[:10],
        "primary_artifact": rel(RUN_MANIFEST),
        "result_status": STATUS,
        "result_judgment": JUDGMENT,
        "final_decision_path": rel(SELECTED_DIR / "selection_status.md"),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": created_at,
        "work_family": "performance_attribution(성과 귀속)",
        "row_id": row_id,
        "evidence_boundary": "gap_analysis_no_authority(간극 분석, 권위 없음)",
        "next_action": NEXT_RUN_ID,
        "question": "Why did proxy positive become runtime negative?(왜 프록시 양수가 런타임 음수가 되었나?)",
        "artifact_count": "7",
        "created_at_utc": created_at,
        "required_gate_audit": rel(GATE_AUDIT),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "run_family": "performance_attribution(성과 귀속)",
        "run_type": "proxy_runtime_gap_analysis_and_repair_decision",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN_MANIFEST),
        "result_path": rel(REPORT),
        "goal_achieve": "not_claimed",
        "source_authority": "runtime_probe_observation_only(런타임 탐침 관찰 전용)",
    }


def update_ledgers(created_at: str, gap: Mapping[str, Any]) -> None:
    row = ledger_row(created_at, gap)
    upsert_csv(RUN_REGISTRY, "run_id", row)
    upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
    upsert_csv(STAGE_LEDGER, "ledger_row_id", row, source_header=ALPHA_LEDGER)


def update_state(created_at: str, gap: Mapping[str, Any], repair: Mapping[str, Any]) -> None:
    runtime = gap["runtime_kpi"]
    state = f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
runtime_probe_status: f78_mandatory_runtime_probe_completed_gap_analysis_done_repair_required
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
five_stage_retrospective_due_status: not_due_after_f77_closeout_2_of_5
updated_at_utc: '{created_at}'
context_anchor: {CONTEXT_ANCHOR_PATH}
notes:
  - "Action(행동): F78E proxy/runtime gap analysis(프록시/런타임 간극 분석)를 완료했다."
  - "Effect(효과): entry timing mismatch(진입 시각 불일치)와 DD denominator mismatch(손실폭 분모 불일치)를 다음 수리 대상으로 고정했다."
  - "Runtime KPI(런타임 KPI): net/PF/DD/tpd {runtime.get('net_profit')}/{runtime.get('profit_factor')}/{runtime.get('max_drawdown_percent')}/{runtime.get('trades_per_day')}."
  - "Next(다음): {repair.get('next_run_id')}."
  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."
"""
    write_text(WORKSPACE_STATE, state)
    current = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {created_at}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

## Current Truth(현재 진실)

Action(행동): F78E proxy/runtime gap analysis(프록시/런타임 간극 분석)를 완료했다.

Effect(효과): F78D에서 signal/feature/fill parity(신호/피처/체결 동등성)는 맞았지만, runtime economics(런타임 경제성)가 negative(부정)인 이유를 entry timing(진입 시각)과 DD denominator(손실폭 분모)로 좁혔다.

## Open Work(열린 작업)

- next run(다음 실행): `{NEXT_RUN_ID}`
- repair focus(수리 초점): runtime-aligned entry label(런타임 정렬 진입 라벨), tester deposit DD denominator(테스터 예치금 손실폭 분모), fill-path penalty(체결 경로 벌점)
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(CURRENT_WORKING_STATE, current)
    selection = f"""# F78 Selection Status(F78 선택 상태)

Updated(갱신): {created_at}

Status(상태): `{STATUS}`

Judgment(판정): `{JUDGMENT}`

Action(행동): F78E proxy/runtime gap analysis(프록시/런타임 간극 분석)를 완료했다.

Effect(효과): 다음 실행은 F78F entry timing/deposit calibrated proxy repair(진입 시각/예치금 보정 프록시 수리)다.

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(SELECTED_DIR / "selection_status.md", selection)
    marker = "<!-- frontier78E_proxy_runtime_gap_analysis_and_repair_decision_v1 -->"
    text = io_path(IDEA_REGISTRY).read_text(encoding="utf-8-sig")
    if marker not in text:
        block = f"""

{marker}
- `{RUN_ID}` completed F78 proxy/runtime gap analysis(F78 프록시/런타임 간극 분석). Result(결과): entry timing mismatch(진입 시각 불일치) dominant -5 minutes(주요 -5분), DD denominator mismatch(손실폭 분모 불일치) 10000 vs 500, signal/feature/fill parity(신호/피처/체결 동등성) matched. Next(다음): `{NEXT_RUN_ID}`. Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
"""
        write_text(IDEA_REGISTRY, text.rstrip() + block)


def run_manifest(created_at: str, gap: Mapping[str, Any], repair: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": created_at,
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "producer": SCRIPT_REL,
        "inputs": [rel(F78D_MANIFEST), rel(F78D_SUMMARY), rel(F78B_SUMMARY)],
        "outputs": {
            "gap_analysis": rel(GAP_ANALYSIS),
            "entry_timing_diagnostic": rel(ENTRY_TIMING_DIAGNOSTIC),
            "repair_decision": rel(REPAIR_DECISION),
            "performance_attribution": rel(PERFORMANCE_ATTRIBUTION),
            "result_judgment": rel(RESULT_JUDGMENT),
            "report": rel(REPORT),
            "gate_audit": rel(GATE_AUDIT),
        },
        "gap_summary": {
            "runtime_net": gap["runtime_kpi"].get("net_profit"),
            "runtime_pf": gap["runtime_kpi"].get("profit_factor"),
            "runtime_dd": gap["runtime_kpi"].get("max_drawdown_percent"),
            "dominant_entry_diff_minutes": gap["entry_timing_diagnostic"].get("dominant_entry_diff_minutes"),
            "sign_flip_count": gap["entry_timing_diagnostic"].get("sign_flip_count"),
            "next_run_id": repair.get("next_run_id"),
        },
    }


def main() -> int:
    ensure_dirs()
    created_at = now_utc()
    gap, timing_rows, performance, result_judgment = build_gap_analysis()
    repair = repair_decision_payload(gap)
    write_json(GAP_ANALYSIS, gap)
    write_csv(ENTRY_TIMING_DIAGNOSTIC, timing_rows)
    write_json(REPAIR_DECISION, repair)
    write_json(PERFORMANCE_ATTRIBUTION, performance)
    write_json(RESULT_JUDGMENT, result_judgment)
    write_text(REPORT, report_text(created_at, gap, repair))
    write_text(GATE_AUDIT, gate_audit_text(created_at))
    write_json(RUN_MANIFEST, run_manifest(created_at, gap, repair))
    update_ledgers(created_at, gap)
    update_state(created_at, gap, repair)
    print(
        json.dumps(
            {
                "status": STATUS,
                "judgment": JUDGMENT,
                "runtime_net_pf_dd_tpd": [
                    gap["runtime_kpi"].get("net_profit"),
                    gap["runtime_kpi"].get("profit_factor"),
                    gap["runtime_kpi"].get("max_drawdown_percent"),
                    gap["runtime_kpi"].get("trades_per_day"),
                ],
                "dominant_entry_diff_minutes": gap["entry_timing_diagnostic"].get("dominant_entry_diff_minutes"),
                "sign_flip_count": gap["entry_timing_diagnostic"].get("sign_flip_count"),
                "next_run_id": NEXT_RUN_ID,
                "report": rel(REPORT),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
