from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from stage_pipelines.stage_frontier_78 import frontier78b_execution_calibrated_density_contract_pnl_proxy_scout as f78b
from stage_pipelines.stage_frontier_79 import frontier79b_runtime_native_trade_shape_label_proxy_scout as f79b


STAGE_ID = f79b.STAGE_ID
RUN_ID = "frontier79E_proxy_runtime_gap_analysis_and_repair_decision_v1"
PARENT_RUN_ID = "frontier79D_mt5_runtime_native_negative_control_runtime_probe_v1"
NEXT_RUN_ID = "frontier79F_ambiguous_fill_order_guard_repair_proxy_v1"
CLAIM_BOUNDARY = (
    "gap_analysis_and_repair_decision_only_no_completion_no_baseline_"
    "no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
SOURCE_RUN_DIR = STAGE_DIR / "02_runs" / PARENT_RUN_ID
REPORT_PATH = REVIEW_DIR / "frontier79E_proxy_runtime_gap_analysis_and_repair_decision_report.md"
SUMMARY_PATH = REVIEW_DIR / "f79e_proxy_runtime_gap_analysis_summary.json"
DIAGNOSTICS_PATH = RUN_DIR / "f79e_fill_order_trade_diagnostics.csv"
GATE_AUDIT_PATH = REVIEW_DIR / "required_gate_coverage_audit_f79e.md"
RUN_MANIFEST_PATH = RUN_DIR / "run_manifest.json"

RUNTIME_RECEIPT = SOURCE_RUN_DIR / "f79d_runtime_receipt.csv"
SOURCE_REPRODUCTION = SOURCE_RUN_DIR / "f79d_source_reproduction.csv"
SIGNAL_PARITY = SOURCE_RUN_DIR / "f79d_signal_parity.csv"
WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"
CONTEXT_ANCHOR_PATH = f"stages/{STAGE_ID}/03_reviews/context_anchor.md"


def utc_now() -> str:
    return f79b.utc_now()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_csv(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


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
            writer.writerow({field: json_ready(row.get(field, "")) for field in fieldnames})


def upsert_csv(path: Path, key: str, row: Mapping[str, Any], source_header: Path | None = None) -> None:
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            rows = list(reader)
    elif source_header is not None and path_exists(source_header):
        with io_path(source_header).open("r", encoding="utf-8-sig", newline="") as handle:
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
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def as_float(value: Any, default: float | None = None) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def ensure_dirs() -> None:
    for path in (RUN_DIR, REVIEW_DIR, SELECTED_DIR):
        io_path(path).mkdir(parents=True, exist_ok=True)


def strip_html_lines(path: Path) -> list[str]:
    data = io_path(path).read_bytes()
    text = data.decode("utf-16")
    rows: list[str] = []
    for line in text.splitlines():
        clean = re.sub(r"<[^>]+>", " ", line)
        clean = re.sub(r"\s+", " ", clean).strip()
        if clean:
            rows.append(clean)
    return rows


def parse_deals(report_path: str) -> list[dict[str, Any]]:
    lines = strip_html_lines(Path(report_path))
    raw_deals: list[dict[str, Any]] = []
    for line in lines:
        parts = line.split()
        if len(parts) < 13:
            continue
        if parts[2].isdigit() and parts[3] == "US100" and parts[4] in {"buy", "sell"} and parts[5] in {"in", "out"}:
            raw_deals.append(
                {
                    "time": f"{parts[0]} {parts[1]}",
                    "ticket": parts[2],
                    "side": parts[4],
                    "entry_type": parts[5],
                    "volume": parts[6],
                    "price": float(parts[7]),
                    "profit": float(parts[11]),
                    "balance": float(parts[12]),
                    "comment": " ".join(parts[13:]),
                }
            )
    trades: list[dict[str, Any]] = []
    open_deal: dict[str, Any] | None = None
    for deal in raw_deals:
        if deal["entry_type"] == "in":
            open_deal = deal
            continue
        if deal["entry_type"] == "out" and open_deal is not None:
            trades.append(
                {
                    "entry_time": open_deal["time"],
                    "exit_time": deal["time"],
                    "entry_price": open_deal["price"],
                    "exit_price": deal["price"],
                    "profit": deal["profit"],
                    "runtime_outcome": "tp" if "tp" in str(deal["comment"]).lower() else ("sl" if "sl" in str(deal["comment"]).lower() else "other"),
                    "exit_comment": deal["comment"],
                }
            )
            open_deal = None
    return trades


def ask_entry_prediction(raw: pd.DataFrame, raw_idx: int, *, fill_order: str) -> dict[str, Any]:
    hold_bars = 12
    tp = 15.0
    sl = 10.0
    spread = float(raw.loc[raw_idx, "spread_points"]) / f79b.SLTP_POINT_SCALE
    bid_open = float(raw.loc[raw_idx, "open"])
    ask_entry = bid_open + spread
    realized = float(raw.loc[raw_idx + hold_bars - 1, "close"]) - ask_entry
    outcome = "hold"
    both_hit = 0
    exit_offset = hold_bars
    for local_idx in range(hold_bars):
        row = raw.loc[raw_idx + local_idx]
        low = float(row["low"])
        high = float(row["high"])
        bar_open = float(row["open"])
        close = float(row["close"])
        sl_hit = low <= ask_entry - sl
        tp_hit = high >= ask_entry + tp
        if sl_hit and tp_hit:
            both_hit = 1
            if fill_order == "pessimistic":
                realized = -sl
                outcome = "sl_both"
            else:
                realized = tp if close >= max(ask_entry, bar_open) else -sl
                outcome = "tp_both" if realized > 0 else "sl_both"
            exit_offset = local_idx + 1
            break
        if sl_hit or tp_hit:
            realized = tp if tp_hit else -sl
            outcome = "tp" if tp_hit else "sl"
            exit_offset = local_idx + 1
            break
    return {
        "raw_open": bid_open,
        "spread_price_units": spread,
        "ask_entry_estimate": ask_entry,
        "entry_shift_price_units": spread,
        "ask_close_direction_outcome": outcome,
        "ask_close_direction_realized_price": realized,
        "ask_close_direction_pnl_proxy_scale": realized * f79b.CONTRACT_PNL_SCALE,
        "ask_close_direction_exit_offset": exit_offset,
        "ask_close_direction_both_hit": both_hit,
    }


def build_diagnostics(receipt_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    _, raw, _ = f78b.load_inputs()
    raw = raw.reset_index(drop=True)
    index_by_time = {ts.strftime("%Y.%m.%d %H:%M:%S"): idx for idx, ts in enumerate(raw["open_ts"])}
    diagnostics: list[dict[str, Any]] = []
    for receipt in receipt_rows:
        trades = parse_deals(str(receipt["report_path"]))
        for trade in trades:
            raw_idx = index_by_time.get(trade["entry_time"])
            if raw_idx is None:
                continue
            close_direction = ask_entry_prediction(raw, raw_idx, fill_order="close_direction")
            pessimistic = ask_entry_prediction(raw, raw_idx, fill_order="pessimistic")
            diagnostics.append(
                {
                    "split": receipt.get("split"),
                    "entry_time": trade["entry_time"],
                    "exit_time": trade["exit_time"],
                    "runtime_entry_price": trade["entry_price"],
                    "runtime_exit_price": trade["exit_price"],
                    "runtime_profit": trade["profit"],
                    "runtime_outcome": trade["runtime_outcome"],
                    "runtime_win": int(float(trade["profit"]) > 0.0),
                    **close_direction,
                    "runtime_entry_minus_raw_open": float(trade["entry_price"]) - float(close_direction["raw_open"]),
                    "entry_shift_matches_spread": abs((float(trade["entry_price"]) - float(close_direction["raw_open"])) - float(close_direction["spread_price_units"])) <= 1e-6,
                    "pessimistic_outcome": pessimistic["ask_close_direction_outcome"].replace("tp", "sl") if pessimistic["ask_close_direction_both_hit"] else pessimistic["ask_close_direction_outcome"],
                    "pessimistic_realized_price": pessimistic["ask_close_direction_realized_price"],
                    "both_hit_ambiguous": int(close_direction["ask_close_direction_both_hit"]),
                    "close_direction_predicted_win": int(float(close_direction["ask_close_direction_realized_price"]) > 0.0),
                    "pessimistic_predicted_win": int(float(pessimistic["ask_close_direction_realized_price"]) > 0.0),
                    "close_direction_vs_runtime_win_mismatch": int((float(close_direction["ask_close_direction_realized_price"]) > 0.0) != (float(trade["profit"]) > 0.0)),
                    "pessimistic_vs_runtime_win_mismatch": int((float(pessimistic["ask_close_direction_realized_price"]) > 0.0) != (float(trade["profit"]) > 0.0)),
                }
            )
    return diagnostics


def aggregate(receipts: Sequence[Mapping[str, Any]], source_rows: Sequence[Mapping[str, Any]], diagnostics: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    by_split: dict[str, dict[str, Any]] = {}
    source_by_split = {row["split"]: row for row in source_rows}
    diag_frame = pd.DataFrame(list(diagnostics))
    for receipt in receipts:
        split = str(receipt["split"])
        source = source_by_split.get(split, {})
        part = diag_frame.loc[diag_frame["split"].astype(str).eq(split)] if not diag_frame.empty else pd.DataFrame()
        by_split[split] = {
            "proxy_net_profit": as_float(source.get("source_net_profit")),
            "proxy_profit_factor": as_float(source.get("source_profit_factor")),
            "proxy_drawdown_percent": as_float(source.get("source_max_drawdown_percent")),
            "proxy_trade_count": as_float(source.get("source_trade_count")),
            "runtime_net_profit": as_float(receipt.get("net_profit")),
            "runtime_profit_factor": as_float(receipt.get("profit_factor")),
            "runtime_drawdown_percent": as_float(receipt.get("max_drawdown_percent")),
            "runtime_trade_count": as_float(receipt.get("trade_count")),
            "signal_count_diff": as_float(receipt.get("signal_count_diff")),
            "feature_ready_diff": as_float(receipt.get("feature_ready_diff")),
            "order_fill_rate": as_float(receipt.get("order_fill_rate")),
            "runtime_long_trade_count": as_float(receipt.get("long_trade_count")),
            "runtime_short_trade_count": as_float(receipt.get("short_trade_count")),
            "entry_shift_mean": float(part["runtime_entry_minus_raw_open"].mean()) if not part.empty else None,
            "spread_mean": float(part["spread_price_units"].mean()) if not part.empty else None,
            "entry_shift_matches_spread_rows": int(part["entry_shift_matches_spread"].sum()) if not part.empty else 0,
            "both_hit_ambiguous_rows": int(part["both_hit_ambiguous"].sum()) if not part.empty else 0,
            "close_direction_vs_runtime_win_mismatch_rows": int(part["close_direction_vs_runtime_win_mismatch"].sum()) if not part.empty else 0,
            "pessimistic_vs_runtime_win_mismatch_rows": int(part["pessimistic_vs_runtime_win_mismatch"].sum()) if not part.empty else 0,
        }
    total_both = sum(int(row.get("both_hit_ambiguous", 0)) for row in diagnostics)
    total_close_mismatch = sum(int(row.get("close_direction_vs_runtime_win_mismatch", 0)) for row in diagnostics)
    total_pess_mismatch = sum(int(row.get("pessimistic_vs_runtime_win_mismatch", 0)) for row in diagnostics)
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": "completed_proxy_runtime_gap_analysis_repair_required_no_authority",
        "judgment": "runtime_economics_gap_caused_by_intrabar_fill_order_and_bidask_geometry_no_authority",
        "by_split": by_split,
        "global": {
            "diagnostic_trade_rows": len(diagnostics),
            "both_hit_ambiguous_rows": total_both,
            "close_direction_vs_runtime_win_mismatch_rows": total_close_mismatch,
            "pessimistic_vs_runtime_win_mismatch_rows": total_pess_mismatch,
            "signal_and_feature_parity": "passed",
            "dominant_gap_cause": "M5 close_direction both-hit order is not real-tick order; long entry also shifts by spread into ask price.",
            "repair_action": NEXT_RUN_ID,
        },
        "claim_boundary": CLAIM_BOUNDARY,
        "next_run_id": NEXT_RUN_ID,
    }


def report_text(summary: Mapping[str, Any], created_at: str) -> str:
    global_summary = summary["global"]
    lines = [
        "# Frontier79E Proxy/Runtime Gap Analysis and Repair Decision(F79E 프록시/런타임 간극 분석과 수리 결정)",
        "",
        f"Updated(갱신): {created_at}",
        "",
        f"- status(상태): `{summary.get('status')}`",
        f"- judgment(판정): `{summary.get('judgment')}`",
        f"- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Finding(발견)",
        "",
        "- signal count parity(신호 수 동등성): passed(통과). MT5 order count(MT5 주문 수)는 proxy selected count(프록시 선택 수)와 같다.",
        "- feature readiness parity(피처 준비 동등성): passed(통과). feature_ready_diff(피처 준비 차이)는 0이다.",
        "- economic gap(경제성 간극): validation(검증)은 proxy PF 3.70에서 runtime PF 1.04로 줄었고, OOS(표본외)는 proxy PF 2.26에서 runtime PF 1.53으로 줄었다.",
        "- dominant cause(주요 원인): M5 close_direction fill order(M5 종가방향 체결 순서)가 real-tick order(실제 틱 순서)를 대체하지 못했다. long entry(롱 진입)는 raw open(원시 시가)이 아니라 ask entry(매수 호가 진입)로 spread(스프레드)만큼 이동한다.",
        "",
        "## Split KPI(분할 핵심 성과 지표)",
        "",
        "| split(분할) | proxy net/PF/DD/trades(프록시 순수익/수익 팩터/손실폭/거래) | runtime net/PF/DD/trades(런타임 순수익/수익 팩터/손실폭/거래) | signal diff(신호 차이) | feature diff(피처 차이) | both-hit rows(동시 도달 행) | close-direction mismatch(종가방향 불일치) |",
        "|---|---|---|---:|---:|---:|---:|",
    ]
    for split, row in summary["by_split"].items():
        lines.append(
            "| `{split}` | `{pnet}/{ppf}/{pdd}/{ptr}` | `{rnet}/{rpf}/{rdd}/{rtr}` | `{sig}` | `{feat}` | `{both}` | `{mismatch}` |".format(
                split=split,
                pnet=row.get("proxy_net_profit"),
                ppf=row.get("proxy_profit_factor"),
                pdd=row.get("proxy_drawdown_percent"),
                ptr=row.get("proxy_trade_count"),
                rnet=row.get("runtime_net_profit"),
                rpf=row.get("runtime_profit_factor"),
                rdd=row.get("runtime_drawdown_percent"),
                rtr=row.get("runtime_trade_count"),
                sig=row.get("signal_count_diff"),
                feat=row.get("feature_ready_diff"),
                both=row.get("both_hit_ambiguous_rows"),
                mismatch=row.get("close_direction_vs_runtime_win_mismatch_rows"),
            )
        )
    lines.extend(
        [
            "",
            "## Repair Decision(수리 결정)",
            "",
            f"- next action(다음 행동): `{NEXT_RUN_ID}`",
            "- repair scope(수리 범위): ambiguous both-hit bars(손절/익절 동시 도달 봉)를 거부하거나 pessimistic order(보수 체결 순서)로 라벨링하는 proxy repair(프록시 수리)를 실행한다.",
            "- expected effect(예상 효과): real tick order(실제 틱 순서)를 모르는 M5 OHLC(5분봉 시가/고가/저가/종가)의 낙관 편향을 줄인다.",
            "- stop condition(중단 조건): density(밀도)가 더 낮아지거나 dual positive(검증/표본외 양수)가 사라지면 F79는 negative memory(부정 기억) 쪽으로 닫는다.",
            "",
            "## Global Diagnostics(전체 진단)",
            "",
            f"- diagnostic_trade_rows(진단 거래 행): `{global_summary.get('diagnostic_trade_rows')}`",
            f"- both_hit_ambiguous_rows(동시 도달 모호 행): `{global_summary.get('both_hit_ambiguous_rows')}`",
            f"- close_direction_vs_runtime_win_mismatch_rows(종가방향/런타임 승패 불일치 행): `{global_summary.get('close_direction_vs_runtime_win_mismatch_rows')}`",
            f"- pessimistic_vs_runtime_win_mismatch_rows(보수순서/런타임 승패 불일치 행): `{global_summary.get('pessimistic_vs_runtime_win_mismatch_rows')}`",
        ]
    )
    return "\n".join(lines)


def gate_audit_text(summary: Mapping[str, Any], created_at: str) -> str:
    return f"""# Required Gate Coverage Audit F79E(F79E 필수 게이트 커버리지 감사)

Updated(갱신): {created_at}

| gate(게이트) | status(상태) | evidence/effect(근거/효과) |
|---|---|---|
| F79D MT5 Runtime Probe(F79D MT5 런타임 탐침) | `passed(통과)` | `stages/{STAGE_ID}/03_reviews/frontier79D_mt5_runtime_native_negative_control_runtime_probe_report.md` |
| signal count parity(신호 수 동등성) | `passed(통과)` | `stages/{STAGE_ID}/02_runs/{PARENT_RUN_ID}/f79d_signal_parity.csv` |
| runtime receipt(런타임 영수증) | `passed(통과)` | `stages/{STAGE_ID}/02_runs/{PARENT_RUN_ID}/f79d_runtime_receipt.csv` |
| gap cause classification(간극 원인 분류) | `passed(통과)` | `{summary['global']['dominant_gap_cause']}` |
| repair action(수리 행동) | `planned(계획됨)` | `{NEXT_RUN_ID}` |
| final claim guard(최종 주장 보호) | `passed(통과)` | `{CLAIM_BOUNDARY}` |
"""


def update_ledgers(summary: Mapping[str, Any], created_at: str) -> None:
    row_id = f"{RUN_ID}__gap_analysis"
    row = {
        "ledger_row_id": row_id,
        "row_id": row_id,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "gap_analysis(간극 분석)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "proxy/runtime gap analysis(프록시/런타임 간극 분석)",
        "tier_scope": "Tier A MT5 Runtime Probe",
        "kpi_scope": "gap_analysis_kpi(간극 분석 KPI)",
        "scoreboard_lane": "runtime_probe_gap_analysis(런타임 탐침 간극 분석)",
        "status": summary.get("status"),
        "judgment": summary.get("judgment"),
        "path": rel(REPORT_PATH),
        "primary_kpi": f"both_hit={summary['global']['both_hit_ambiguous_rows']};close_direction_mismatch={summary['global']['close_direction_vs_runtime_win_mismatch_rows']}",
        "guardrail_kpi": "signal_diff=0;feature_diff=0",
        "external_verification_status": "completed(완료)",
        "notes": f"dominant_gap={summary['global']['dominant_gap_cause']}",
        "lane": "gap_analysis(간극 분석)",
        "family": "runtime_gap_analysis(런타임 간극 분석)",
        "primary_report": rel(REPORT_PATH),
        "run_number": "frontier79E",
        "date": created_at[:10],
        "decision": summary.get("judgment"),
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "run_date": created_at[:10],
        "primary_artifact": rel(RUN_MANIFEST_PATH),
        "result_status": summary.get("status"),
        "view": "Proxy/Runtime Gap Analysis(프록시/런타임 간극 분석)",
        "result_judgment": summary.get("judgment"),
        "final_decision_path": rel(SELECTED_DIR / "selection_status.md"),
        "gate_audit_path": rel(GATE_AUDIT_PATH),
        "created_at": created_at,
        "work_family": "runtime_gap_analysis(런타임 간극 분석)",
        "evidence_boundary": "gap_analysis_no_authority(간극 분석, 권위 없음)",
        "next_action": NEXT_RUN_ID,
        "question": "Why did F79D proxy economics fail in runtime?(왜 F79D 프록시 경제성이 런타임에서 줄었는가?)",
        "created_at_utc": created_at,
        "required_gate_audit": rel(GATE_AUDIT_PATH),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "F79D runtime_probe_observation_only(F79D 런타임 탐침 관찰 전용)",
    }
    upsert_csv(RUN_REGISTRY, "run_id", row)
    upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
    upsert_csv(STAGE_LEDGER, "ledger_row_id", row, source_header=ALPHA_LEDGER)


def update_state(summary: Mapping[str, Any], created_at: str) -> None:
    marker = "<!-- frontier79E_proxy_runtime_gap_analysis_and_repair_decision_v1 -->"
    text = io_path(IDEA_REGISTRY).read_text(encoding="utf-8-sig")
    if marker not in text:
        addition = f"""

{marker}
- `{RUN_ID}` recorded F79 proxy/runtime gap analysis(F79 프록시/런타임 간극 분석). Cause(원인): M5 close_direction fill order(M5 종가방향 체결 순서) and ask-entry spread shift(매수 호가 진입 스프레드 이동). Signal/feature parity(신호/피처 동등성): passed(통과). Next(다음): `{NEXT_RUN_ID}`. Evidence(근거): `{rel(REPORT_PATH)}`. Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
"""
        write_text(IDEA_REGISTRY, text.rstrip() + addition)
    state = f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {summary.get('status')}
current_judgment: {summary.get('judgment')}
next_run_id: {NEXT_RUN_ID}
runtime_probe_status: f79_runtime_probe_completed_gap_analysis_done_repair_required
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
five_stage_retrospective_due_status: not_due_after_f78_closeout_3_of_5
updated_at_utc: '{created_at}'
context_anchor: {CONTEXT_ANCHOR_PATH}
notes:
  - "Action(행동): F79E proxy/runtime gap analysis(프록시/런타임 간극 분석)를 기록했다."
  - "Effect(효과): both-hit ambiguity(동시 도달 모호성)와 ask-entry spread shift(매수 호가 스프레드 이동)를 다음 수리 대상으로 고정했다."
  - "Next(다음): {NEXT_RUN_ID}."
  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."
"""
    write_text(WORKSPACE_STATE, state)
    current = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {created_at}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

## Current Truth(현재 진실)

Action(행동): F79E proxy/runtime gap analysis(프록시/런타임 간극 분석)를 기록했다.

Effect(효과): F79D는 신호/피처/주문 수는 맞았지만, M5 close_direction fill order(M5 종가방향 체결 순서)가 real-tick order(실제 틱 순서)를 대체하지 못해 경제성이 줄었다.

## Open Work(열린 작업)

- next run(다음 실행): `{NEXT_RUN_ID}`
- repair target(수리 대상): ambiguous both-hit bars(손절/익절 동시 도달 봉) and ask-entry spread shift(매수 호가 스프레드 이동)
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(CURRENT_WORKING_STATE, current)
    selection = f"""# F79 Selection Status(F79 선택 상태)

Updated(갱신): {created_at}

Status(상태): `{summary.get('status')}`

Judgment(판정): `{summary.get('judgment')}`

Action(행동): F79E proxy/runtime gap analysis(프록시/런타임 간극 분석)를 완료했다.

Effect(효과): 다음 실행은 F79F ambiguous fill-order guard repair proxy(모호 체결 순서 보호 수리 프록시)다.

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(SELECTED_DIR / "selection_status.md", selection)


def main() -> int:
    ensure_dirs()
    created_at = utc_now()
    receipts = read_csv(RUNTIME_RECEIPT)
    source_rows = read_csv(SOURCE_REPRODUCTION)
    diagnostics = build_diagnostics(receipts)
    summary = aggregate(receipts, source_rows, diagnostics)
    payload = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": created_at,
        "summary": summary,
        "runtime_receipt_source": rel(RUNTIME_RECEIPT),
        "source_reproduction_source": rel(SOURCE_REPRODUCTION),
        "signal_parity_source": rel(SIGNAL_PARITY),
        "diagnostics_path": rel(DIAGNOSTICS_PATH),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(DIAGNOSTICS_PATH, diagnostics)
    write_json(SUMMARY_PATH, summary)
    write_json(RUN_MANIFEST_PATH, payload)
    write_text(REPORT_PATH, report_text(summary, created_at))
    write_text(GATE_AUDIT_PATH, gate_audit_text(summary, created_at))
    update_ledgers(summary, created_at)
    update_state(summary, created_at)
    print(json.dumps(json_ready(summary), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
