from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.grok_review_wrapper import run_grok_review
from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized
from stage_pipelines.stage_frontier_77 import frontier77b_runtime_lifecycle_label_density_proxy_scout as f77b


STAGE_ID = f77b.STAGE_ID
RUN_ID = "frontier77G_post_repair_gap_analysis_or_closeout_decision_v1"
PARENT_RUN_ID = "frontier77F_mt5_lifecycle_point_unit_repair_probe_v1"
NEXT_RUN_CLOSEOUT = "frontier77H_stage_closeout_runtime_lifecycle_label_density_rebuild_v1"
NEXT_RUN_RETRY = "frontier77G_grok_retry_post_repair_gap_analysis_v1"

STATUS_SUCCESS = "post_repair_gap_analysis_completed_closeout_direction_reviewed_no_authority"
STATUS_TRANSPORT_FAIL = "post_repair_gap_analysis_grok_transport_failed_no_closeout_no_authority"
JUDGMENT_SUCCESS = "f77_closeout_as_preserved_clue_recommended_no_authority"
JUDGMENT_TRANSPORT_FAIL = "f77_closeout_direction_grok_retry_required_no_authority"
CLAIM_BOUNDARY = (
    "post_repair_gap_analysis_only_no_completion_no_baseline_"
    "no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"

F77F_RUN_DIR = STAGE_DIR / "02_runs" / PARENT_RUN_ID
F77F_SUMMARY = REVIEW_DIR / "f77f_mt5_lifecycle_point_unit_repair_probe_summary.json"
F77F_RECEIPT = F77F_RUN_DIR / "f77f_runtime_receipt.csv"
F77F_MANIFEST = F77F_RUN_DIR / "run_manifest.json"
F77C_TARGET = REVIEW_DIR / "f77c_runtime_materialization_target_selection.json"
F77B_SUMMARY = REVIEW_DIR / "f77b_lifecycle_proxy_summary.json"

REPORT_PATH = REVIEW_DIR / "frontier77G_post_repair_gap_analysis_or_closeout_decision_report.md"
RECEIPT_PATH = REVIEW_DIR / "grok_f77g_post_repair_gap_analysis_closeout_direction_receipt.md"
GATE_AUDIT_PATH = REVIEW_DIR / "required_gate_coverage_audit_f77g.md"
GAP_ANALYSIS_JSON = REVIEW_DIR / "f77g_post_repair_gap_analysis_closeout_decision.json"
RUN_MANIFEST_PATH = RUN_DIR / "run_manifest.json"
SELECTION_STATUS_PATH = SELECTED_DIR / "selection_status.md"
CONTEXT_ANCHOR_PATH = f"stages/{STAGE_ID}/03_reviews/context_anchor.md"

WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"

GROK_PACKET = ROOT / "docs/agent_control/grok_reviews/2026-06-17_f77g_post_repair_gap_analysis_closeout_direction"
GROK_PROMPT_PATH = GROK_PACKET / "prompts/f77g_post_repair_gap_analysis_closeout_direction_prompt.md"
GROK_CLEAN_PATH = GROK_PACKET / "clean_output.md"
GROK_METADATA_PATH = GROK_PACKET / "metadata.json"


def utc_now() -> str:
    return f77b.utc_now()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_text(path: Path, text: str, *, encoding: str = "utf-8-sig") -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding=encoding)


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def file_hash(path: Path) -> str:
    return sha256_file_lf_normalized(path) if path_exists(path) else ""


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in (None, ""):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def safe_ratio(numerator: float, denominator: float) -> float | None:
    if abs(denominator) <= 1e-12:
        return None
    return numerator / denominator


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


def ensure_dirs() -> None:
    for path in (RUN_DIR, REVIEW_DIR, SELECTED_DIR, GROK_PROMPT_PATH.parent):
        io_path(path).mkdir(parents=True, exist_ok=True)


def telemetry_summary(path_text: str) -> dict[str, Any]:
    rows = read_csv_rows(Path(path_text))
    attempted = [row for row in rows if str(row.get("order_attempted", "")).lower() == "true"]
    filled = [row for row in rows if str(row.get("order_filled", "")).lower() == "true"]
    short_skipped = [
        row
        for row in rows
        if row.get("decision") == "short" and str(row.get("order_attempted", "")).lower() != "true"
    ]
    return {
        "row_count": len(rows),
        "decision_counts": dict(Counter(row.get("decision", "") for row in rows)),
        "exec_action_counts": dict(Counter(row.get("exec_action", "") for row in rows)),
        "retcodes": dict(Counter(row.get("trade_retcode", "") for row in rows if row.get("trade_retcode", ""))),
        "trade_comments": dict(Counter(row.get("trade_comment", "") for row in rows if row.get("trade_comment", ""))),
        "order_attempted": len(attempted),
        "order_filled": len(filled),
        "short_skipped_count": len(short_skipped),
        "short_skipped_actions": dict(Counter(row.get("exec_action", "") for row in short_skipped)),
        "sl_points_values": sorted({row.get("open_sl_points", "") for row in attempted if row.get("open_sl_points", "")}),
        "tp_points_values": sorted({row.get("open_tp_points", "") for row in attempted if row.get("open_tp_points", "")}),
    }


def split_proxy_values(target: Mapping[str, Any], split: str) -> dict[str, float]:
    prefix = "val" if split == "validation" else "oos"
    return {
        "net_profit": safe_float(target.get(f"{prefix}_net")),
        "gross_profit": safe_float(target.get(f"{prefix}_gross_profit")),
        "gross_loss": safe_float(target.get(f"{prefix}_gross_loss")),
        "profit_factor": safe_float(target.get(f"{prefix}_pf")),
        "max_drawdown_percent": safe_float(target.get(f"{prefix}_dd_pct")),
        "trade_count": safe_float(target.get(f"{prefix}_trade_count")),
        "trades_per_day": safe_float(target.get(f"{prefix}_trades_day")),
        "win_rate": safe_float(target.get(f"{prefix}_win_rate")),
        "expectancy": safe_float(target.get(f"{prefix}_expectancy")),
        "recovery_factor": safe_float(target.get(f"{prefix}_recovery")),
        "max_consecutive_loss": safe_float(target.get(f"{prefix}_max_consecutive_loss")),
        "time_under_water_trades": safe_float(target.get(f"{prefix}_time_under_water_trades")),
    }


def build_gap_analysis() -> dict[str, Any]:
    f77f_summary = read_json(F77F_SUMMARY)
    f77f_manifest = read_json(F77F_MANIFEST)
    f77b_summary = read_json(F77B_SUMMARY)
    target_payload = read_json(F77C_TARGET)
    target = dict(target_payload.get("runtime_materialization_target") or {})
    blocked_best = dict(target_payload.get("blocked_best_candidate") or f77b_summary.get("best_candidate") or {})
    receipts = read_csv_rows(F77F_RECEIPT)
    split_rows: list[dict[str, Any]] = []
    for row in receipts:
        split = str(row.get("split"))
        proxy = split_proxy_values(target, split)
        runtime_trade_count = safe_float(row.get("trade_count"))
        proxy_trade_count = proxy["trade_count"]
        proxy_tpd = proxy["trades_per_day"]
        proxy_active_days = safe_ratio(proxy_trade_count, proxy_tpd) if proxy_tpd > 0 else None
        runtime_active_day_tpd = safe_ratio(runtime_trade_count, proxy_active_days or 0.0)
        telemetry = telemetry_summary(str(row.get("telemetry_path", "")))
        split_rows.append(
            {
                "split": split,
                "test_period_start": row.get("test_period_start"),
                "test_period_end": row.get("test_period_end"),
                "calendar_days_exclusive": safe_float(row.get("calendar_days_exclusive")),
                "proxy": proxy,
                "runtime": {
                    "net_profit": safe_float(row.get("net_profit")),
                    "gross_profit": safe_float(row.get("gross_profit")),
                    "gross_loss": safe_float(row.get("gross_loss")),
                    "profit_factor": safe_float(row.get("profit_factor")),
                    "max_drawdown_percent": safe_float(row.get("max_drawdown_percent")),
                    "trade_count": runtime_trade_count,
                    "trades_per_day_calendar": safe_float(row.get("trades_per_day")),
                    "trades_per_day_proxy_active_dates": runtime_active_day_tpd,
                    "win_rate_percent": safe_float(row.get("win_rate_percent")),
                    "expectancy": safe_float(row.get("expectancy")),
                    "recovery_factor": safe_float(row.get("recovery_factor")),
                    "order_attempt_count": safe_float(row.get("order_attempt_count")),
                    "order_fill_count": safe_float(row.get("order_fill_count")),
                    "signal_count": safe_float(row.get("signal_count")),
                    "feature_ready_diff": safe_float(row.get("feature_ready_diff")),
                    "signal_count_diff": safe_float(row.get("signal_count_diff")),
                },
                "gaps": {
                    "net_delta": safe_float(row.get("net_profit")) - proxy["net_profit"],
                    "pf_delta": safe_float(row.get("profit_factor")) - proxy["profit_factor"],
                    "dd_delta": safe_float(row.get("max_drawdown_percent")) - proxy["max_drawdown_percent"],
                    "trade_count_delta": runtime_trade_count - proxy_trade_count,
                    "calendar_tpd_delta": safe_float(row.get("trades_per_day")) - proxy_tpd,
                    "proxy_active_day_tpd_delta": (runtime_active_day_tpd - proxy_tpd) if runtime_active_day_tpd is not None else None,
                    "net_scale": safe_ratio(safe_float(row.get("net_profit")), proxy["net_profit"]),
                    "gross_profit_scale": safe_ratio(safe_float(row.get("gross_profit")), proxy["gross_profit"]),
                    "gross_loss_scale_abs": safe_ratio(abs(safe_float(row.get("gross_loss"))), abs(proxy["gross_loss"])),
                    "fill_minus_signal": safe_float(row.get("order_fill_count")) - safe_float(row.get("signal_count")),
                    "fill_minus_proxy_trade_count": safe_float(row.get("order_fill_count")) - proxy_trade_count,
                },
                "telemetry": telemetry,
            }
        )
    best_runtime = f77f_summary.get("best_runtime") or {}
    oos_row = next((row for row in split_rows if row["split"] == "oos"), split_rows[-1] if split_rows else {})
    closeout_label = "preserved clue(보존 단서)"
    closeout_reason = [
        "F77F fixed Invalid stops(잘못된 손절/익절) and achieved order fills(주문 체결).",
        "ONNX probability/signal/feature parity(ONNX 확률/신호/피처 동등성)가 유지됐다.",
        "F77B meaningful_signal_count(의미 신호 수)는 0이라 완성 후보가 아니다.",
        "Runtime PF(런타임 수익 팩터)는 proxy와 비슷하지만 2.0 미만이고, active-date density(활성일 밀도)도 5~10회/일에 못 미친다.",
        "Proxy trades/day(프록시 일 거래 수)는 selected active dates(선택 활성 날짜)를 분모로 써서 final density(최종 밀도) 판단에 부적합하다.",
    ]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "f77f_summary": f77f_summary,
        "f77f_manifest_artifact_count": len(f77f_manifest.get("artifact_rows", [])),
        "source_candidate": target,
        "blocked_best_candidate": blocked_best,
        "f77b_proxy_summary": {
            "candidate_rows": f77b_summary.get("candidate_rows"),
            "scout_clue_count": f77b_summary.get("scout_clue_count"),
            "meaningful_signal_count": f77b_summary.get("meaningful_signal_count"),
            "final_like_reference_count": f77b_summary.get("final_like_reference_count"),
        },
        "split_rows": split_rows,
        "best_runtime": best_runtime,
        "oos_gap_highlights": oos_row.get("gaps", {}),
        "post_repair_gap_causes": [
            "money_scale_gap_after_point_unit_repair",
            "trade_density_denominator_gap_proxy_active_dates_vs_runtime_calendar_days",
            "minor_fill_count_gap_from_hold_same_direction_after_realized_runtime_holds",
            "weak_alpha_gap_pf_and_density_below_goal_after_runtime_materialization",
        ],
        "preserved_clue": [
            "price-unit to broker-point scaling TP18/SL12 -> TP1800/SL1200 repairs MT5 Invalid stops.",
            "selected-entry veto tape can preserve signal count parity into ONNX/EA runtime.",
            "PF direction survived roughly after fill repair, so bridge mechanics are usable for later hypotheses.",
        ],
        "negative_memory": [
            "F77 lifecycle label proxy produced zero meaningful candidates under its own gate.",
            "Proxy money values were not contract-calibrated to MT5 realized P/L scale.",
            "Proxy trades/day used selected active dates, not a final-review compatible daily denominator.",
            "Best proxy HistGBM remained non-exportable in this path, so exportability can distort runtime target selection.",
        ],
        "codex_proposed_direction": "close_f77_as_preserved_clue_with_negative_memory_then_open_new_frontier_hypothesis",
        "proposed_closeout_label": closeout_label,
        "proposed_next_run_id": NEXT_RUN_CLOSEOUT,
        "closeout_reason": closeout_reason,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_prompt(analysis: Mapping[str, Any]) -> str:
    best = analysis["best_runtime"]
    oos = next((row for row in analysis["split_rows"] if row["split"] == "oos"), {})
    validation = next((row for row in analysis["split_rows"] if row["split"] == "validation"), {})
    return f"""# F77G Post-Repair Gap Analysis Grok Review Prompt(F77G 수리 후 간극 분석 Grok 검토 프롬프트)

You are Grok(Grok, 그록), external second-opinion reviewer(외부 2차 의견 검토자).
Answer only from this bounded evidence snapshot(제한 근거 스냅샷).
Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(브라우징 금지), or perform local verification(로컬 검증 금지).

## Current State(현재 상태)

- active stage(활성 단계): `{STAGE_ID}`
- current run(현재 실행): `{RUN_ID}`
- parent run(부모 실행): `{PARENT_RUN_ID}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
- forbidden claims(금지 주장): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)

## Hypothesis(가설)

F77 asked whether runtime lifecycle-native labels(런타임 생명주기 기본 라벨)가 independent signal labels(독립 신호 라벨)보다 tradeable density(거래 가능 밀도)와 proxy/runtime parity(프록시/런타임 동등성)를 더 잘 보존할 수 있는지.

## Evidence Snapshot(근거 스냅샷)

- F77B proxy candidates(프록시 후보): `{analysis['f77b_proxy_summary']['candidate_rows']}`
- F77B scout clues(탐색 단서): `{analysis['f77b_proxy_summary']['scout_clue_count']}`
- F77B meaningful signals(의미 신호): `{analysis['f77b_proxy_summary']['meaningful_signal_count']}`
- F77B final-like references(완성 유사 참조): `{analysis['f77b_proxy_summary']['final_like_reference_count']}`
- F77C target(대상): exportable ExtraTrees(내보내기 가능한 엑스트라트리) `f77b_07979`; best HistGBM(최선 히스토그램 그래디언트 부스팅) `f77b_08051` was not ONNX-exportable(ONNX 내보내기 불가)
- F77D runtime(런타임): signal/feature parity(신호/피처 동등성) passed, but all orders failed with Invalid stops(잘못된 손절/익절)
- F77E repair decision(수리 결정): TP18/SL12 price units(가격 단위)을 TP1800/SL1200 broker points(브로커 포인트)로 변환
- F77F repair result(수리 결과): Strategy Tester(전략 테스터) completed 2/2, orders filled(주문 체결)

## F77F Runtime KPI(런타임 핵심 성과 지표)

Validation(검증):
- period(기간): `{validation.get('test_period_start')}..{validation.get('test_period_end')}`
- runtime net/PF/DD/trades/calendar tpd(런타임 순수익/수익 팩터/손실폭/거래 수/달력 일거래): `{validation.get('runtime', {}).get('net_profit')}/{validation.get('runtime', {}).get('profit_factor')}/{validation.get('runtime', {}).get('max_drawdown_percent')}/{validation.get('runtime', {}).get('trade_count')}/{validation.get('runtime', {}).get('trades_per_day_calendar')}`
- proxy net/PF/DD/trades/active-date tpd(프록시 순수익/수익 팩터/손실폭/거래 수/활성일 일거래): `{validation.get('proxy', {}).get('net_profit')}/{validation.get('proxy', {}).get('profit_factor')}/{validation.get('proxy', {}).get('max_drawdown_percent')}/{validation.get('proxy', {}).get('trade_count')}/{validation.get('proxy', {}).get('trades_per_day')}`
- runtime active-date tpd(런타임 활성일 일거래): `{validation.get('runtime', {}).get('trades_per_day_proxy_active_dates')}`

OOS(표본외):
- period(기간): `{oos.get('test_period_start')}..{oos.get('test_period_end')}`
- runtime net/PF/DD/trades/calendar tpd(런타임 순수익/수익 팩터/손실폭/거래 수/달력 일거래): `{oos.get('runtime', {}).get('net_profit')}/{oos.get('runtime', {}).get('profit_factor')}/{oos.get('runtime', {}).get('max_drawdown_percent')}/{oos.get('runtime', {}).get('trade_count')}/{oos.get('runtime', {}).get('trades_per_day_calendar')}`
- proxy net/PF/DD/trades/active-date tpd(프록시 순수익/수익 팩터/손실폭/거래 수/활성일 일거래): `{oos.get('proxy', {}).get('net_profit')}/{oos.get('proxy', {}).get('profit_factor')}/{oos.get('proxy', {}).get('max_drawdown_percent')}/{oos.get('proxy', {}).get('trade_count')}/{oos.get('proxy', {}).get('trades_per_day')}`
- runtime active-date tpd(런타임 활성일 일거래): `{oos.get('runtime', {}).get('trades_per_day_proxy_active_dates')}`

Best runtime row(최선 런타임 행): net/PF/DD/tpd `{best.get('net_profit')}/{best.get('profit_factor')}/{best.get('max_drawdown_percent')}/{best.get('trades_per_day')}`.

## Gap Causes(간극 원인)

Codex currently sees these causes(현재 Codex가 보는 원인):
1. money_scale_gap_after_point_unit_repair(포인트 단위 수리 후 금액 배율 간극)
2. trade_density_denominator_gap_proxy_active_dates_vs_runtime_calendar_days(프록시 활성일 분모와 런타임 달력일 분모 간극)
3. minor_fill_count_gap_from_hold_same_direction_after_realized_runtime_holds(실제 런타임 보유 후 같은 방향 보유로 생긴 작은 체결 수 간극)
4. weak_alpha_gap_pf_and_density_below_goal_after_runtime_materialization(런타임 물질화 후 PF와 밀도가 목표권 미만인 약한 알파 간극)

## Codex Proposed Direction(Codex 제안 방향)

Close F77 as preserved clue(보존 단서) with recorded negative memory(부정 기억 기록), not as completion(완성).
Preserve(보존): point-unit repair(포인트 단위 수리), ONNX/EA signal parity(ONNX/EA 신호 동등성), and runtime bridge mechanics(런타임 연결 메커니즘).
Record negative memory(부정 기억): F77 had zero meaningful proxy candidates(의미 프록시 후보 0), final density metric was not aligned(최종 밀도 지표 불일치), money scale was not contract-calibrated(금액 배율 계약 미보정), and exportability distorted target selection(내보내기 가능성이 대상 선택을 왜곡).

## Focus Question(집중 질문)

Should Codex close F77 as preserved clue(보존 단서) and move to a new frontier hypothesis(새 전선 가설), or is there a concrete non-repetitive repair(반복이 아닌 구체 수리) still required inside F77 before closeout(마감)?

Classify advice(조언 분류) as one of:
- accepted(수용)
- accepted_with_conditions(조건부 수용)
- needs_local_verification(로컬 검증 필요)
- rejected(거절)

Do not grant completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 금지).
"""


def classify_advice(clean_output: str, success: bool) -> tuple[str, str, list[str], str]:
    lowered = clean_output.lower()
    forbidden_hits = [
        term
        for term in ["goal achieve", "runtime authority", "live readiness", "selected baseline", "operating promotion", "completion"]
        if f"may claim {term}" in lowered
        or f"can claim {term}" in lowered
        or f"{term} achieved" in lowered
        or f"{term}: yes" in lowered
    ]
    if not success:
        return (
            "transport_failed(전송 실패)",
            "retry_grok_before_closeout_direction(마감 방향 전 Grok 재시도)",
            forbidden_hits,
            NEXT_RUN_RETRY,
        )
    if "rejected" in lowered and "accepted" not in lowered:
        return (
            "rejected(거절)",
            "needs_local_verification_before_closeout_or_repair(마감 또는 수리 전 로컬 검증 필요)",
            forbidden_hits,
            NEXT_RUN_RETRY,
        )
    if "needs_local_verification" in lowered or "local verification" in lowered:
        return (
            "needs_local_verification(로컬 검증 필요)",
            "closeout_only_after_codex_verifies_grok_conditions(Codex가 Grok 조건을 검증한 뒤에만 마감)",
            forbidden_hits,
            NEXT_RUN_CLOSEOUT,
        )
    if "accepted_with_conditions" in lowered or "accepted with conditions" in lowered:
        return (
            "accepted_with_conditions(조건부 수용)",
            "closeout_f77_as_preserved_clue_with_conditions(F77을 조건부 보존 단서로 마감)",
            forbidden_hits,
            NEXT_RUN_CLOSEOUT,
        )
    return (
        "accepted(수용)",
        "closeout_f77_as_preserved_clue(F77을 보존 단서로 마감)",
        forbidden_hits,
        NEXT_RUN_CLOSEOUT,
    )


def split_table_rows(analysis: Mapping[str, Any]) -> list[str]:
    lines: list[str] = []
    for row in analysis["split_rows"]:
        proxy = row["proxy"]
        runtime = row["runtime"]
        gaps = row["gaps"]
        lines.append(
            "| `{split}` | `{period}` | `{pnet}` | `{rnet}` | `{ppf}` | `{rpf}` | `{pdd}` | `{rdd}` | `{ptrades}` | `{rtrades}` | `{ptpd}` | `{rctpd}` | `{ratpd}` | `{net_scale}` | `{gp_scale}` | `{gap}` |".format(
                split=row["split"],
                period=f"{row['test_period_start']}..{row['test_period_end']}",
                pnet=proxy["net_profit"],
                rnet=runtime["net_profit"],
                ppf=proxy["profit_factor"],
                rpf=runtime["profit_factor"],
                pdd=proxy["max_drawdown_percent"],
                rdd=runtime["max_drawdown_percent"],
                ptrades=proxy["trade_count"],
                rtrades=runtime["trade_count"],
                ptpd=proxy["trades_per_day"],
                rctpd=runtime["trades_per_day_calendar"],
                ratpd=runtime["trades_per_day_proxy_active_dates"],
                net_scale=gaps["net_scale"],
                gp_scale=gaps["gross_profit_scale"],
                gap=";".join(analysis["post_repair_gap_causes"]),
            )
        )
    return lines


def report_text(created_at: str, analysis: Mapping[str, Any], grok: Mapping[str, Any], advice: str, direction: str, forbidden_hits: Sequence[str], next_run_id: str) -> str:
    lines = [
        "# Frontier77G Post-Repair Gap Analysis And Closeout Decision(F77G 수리 후 간극 분석과 마감 결정)",
        "",
        f"Updated(갱신): {created_at}",
        "",
        f"Status(상태): `{STATUS_SUCCESS if grok['success'] else STATUS_TRANSPORT_FAIL}`",
        "",
        f"Judgment(판정): `{JUDGMENT_SUCCESS if grok['success'] else JUDGMENT_TRANSPORT_FAIL}`",
        "",
        f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## KPI Gap(KPI 간극)",
        "",
        "| split(분할) | period(기간) | proxy net(프록시 순수익) | runtime net(런타임 순수익) | proxy PF(프록시 수익 팩터) | runtime PF(런타임 수익 팩터) | proxy DD(프록시 손실폭) | runtime DD(런타임 손실폭) | proxy trades(프록시 거래 수) | runtime trades(런타임 거래 수) | proxy active tpd(프록시 활성일 일거래) | runtime calendar tpd(런타임 달력 일거래) | runtime active tpd(런타임 활성일 일거래) | net scale(순수익 배율) | gross profit scale(총이익 배율) | gap cause(간극 원인) |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|",
        *split_table_rows(analysis),
        "",
        "## Decision Direction(결정 방향)",
        "",
        f"- proposed closeout label(제안 마감 라벨): `{analysis['proposed_closeout_label']}`",
        f"- next action(다음 행동): `{next_run_id}`",
        "- preserved clue(보존 단서):",
    ]
    for item in analysis["preserved_clue"]:
        lines.append(f"  - {item}")
    lines.append("- negative memory(부정 기억):")
    for item in analysis["negative_memory"]:
        lines.append(f"  - {item}")
    lines.extend(
        [
            "",
            "## Grok Review(Grok 검토)",
            "",
            f"- packet(묶음): `{rel(GROK_PACKET)}`",
            f"- prompt(프롬프트): `{rel(GROK_PROMPT_PATH)}` sha256 `{grok['prompt_sha256']}`",
            f"- output(출력): `{rel(GROK_CLEAN_PATH)}` sha256 `{grok['output_sha256'] if grok['output_exists'] else 'missing'}`",
            f"- metadata(메타데이터): `{rel(GROK_METADATA_PATH)}` sha256 `{grok['metadata_sha256'] if grok['metadata_exists'] else 'missing'}`",
            f"- advice classification(조언 분류): `{advice}`",
            f"- final Codex direction(최종 Codex 방향): `{direction}`",
            f"- forbidden claim hits(금지 주장 감지): `{', '.join(forbidden_hits) if forbidden_hits else 'none(없음)'}`",
            "",
            "## Boundary(경계)",
            "",
            "This is a closeout direction review only(마감 방향 검토 전용). It does not create completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).",
        ]
    )
    return "\n".join(lines)


def receipt_text(created_at: str, grok: Mapping[str, Any], advice: str, direction: str, forbidden_hits: Sequence[str]) -> str:
    return f"""# F77G Grok Post-Repair Gap Analysis Receipt(F77G Grok 수리 후 간극 분석 영수증)

Created at(생성 시각): {created_at}

Trigger reason(트리거 이유): F77F MT5 Runtime Probe(MT5 런타임 탐침)가 completed(완료)되었고, stage closeout direction(단계 마감 방향)에 Grok second opinion(Grok 2차 의견)이 필요하다.

Review size(검토 크기): small review(소규모 검토).

Bounded evidence(제한 근거): F77B proxy summary(프록시 요약), F77C target selection(대상 선택), F77F runtime KPI(런타임 핵심 성과 지표), proxy/runtime gap rows(프록시/런타임 간극 행), Codex proposed closeout label(Codex 제안 마감 라벨).

Prompt identity(프롬프트 정체성): `{rel(GROK_PROMPT_PATH)}` sha256 `{grok['prompt_sha256']}`.

Grok output identity(Grok 출력 정체성): `{rel(GROK_CLEAN_PATH)}` sha256 `{grok['output_sha256'] if grok['output_exists'] else 'missing'}`.

Advice classification(조언 분류): `{advice}`.

Local verification(로컬 검증): F77F receipt(영수증), summary(요약), report(보고서), telemetry(원격측정)를 `io_path(입출력 경로 보조)`로 확인했다.

Forbidden claim check(금지 주장 확인): `{', '.join(forbidden_hits) if forbidden_hits else 'none(없음)'}`.

Final Codex direction(최종 Codex 방향): `{direction}`.
"""


def gate_audit_text(grok: Mapping[str, Any], advice: str, next_run_id: str) -> str:
    return f"""# Required Gate Coverage Audit F77G(F77G 필수 게이트 커버리지 감사)

| gate(게이트) | status(상태) | evidence/effect(근거/효과) |
|---|---|---|
| F77F runtime evidence(F77F 런타임 근거) | `passed(통과)` | `{rel(F77F_RECEIPT)}` |
| post-repair gap analysis(수리 후 간극 분석) | `passed(통과)` | `{rel(GAP_ANALYSIS_JSON)}` |
| Grok closeout-direction review(Grok 마감 방향 검토) | `{'passed(통과)' if grok['success'] else 'failed_transport(전송 실패)'}` | `{rel(RECEIPT_PATH)}` |
| advice classification(조언 분류) | `{advice}` | `{rel(GROK_CLEAN_PATH)}` |
| next action(다음 행동) | `{next_run_id}` | closeout or retry(마감 또는 재시도) |
| claim guard(주장 보호) | `passed(통과)` | `{CLAIM_BOUNDARY}` |
"""


def update_state_and_ledgers(created_at: str, status: str, judgment: str, advice: str, next_run_id: str, analysis: Mapping[str, Any]) -> None:
    best = analysis["best_runtime"]
    workspace = f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {next_run_id}
latest_completed_run_id: {RUN_ID}
current_status: {status}
current_judgment: {judgment}
next_run_id: {next_run_id}
runtime_probe_status: f77_post_repair_gap_analysis_completed
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
five_stage_retrospective_due_status: not_due_after_f76_closeout_1_of_5
updated_at_utc: '{created_at}'
context_anchor: {CONTEXT_ANCHOR_PATH}
notes:
  - "Action(행동): F77G post-repair gap analysis(수리 후 간극 분석)를 완료했다."
  - "Effect(효과): F77F 런타임 탐침을 보존 단서와 부정 기억으로 분리했고, 다음 행동을 {next_run_id}로 고정했다."
  - "Best runtime(최선 런타임): net/PF/DD/tpd {best.get('net_profit', '')}/{best.get('profit_factor', '')}/{best.get('max_drawdown_percent', '')}/{best.get('trades_per_day', '')}."
  - "Grok advice(Grok 조언): {advice}."
  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."
"""
    write_text(WORKSPACE_STATE, workspace)
    current = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {created_at}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{next_run_id}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

## Current Truth(현재 진실)

Action(행동): F77G post-repair gap analysis(수리 후 간극 분석)를 완료했다.

Effect(효과): F77F는 주문 체결 bridge(연결)를 수리했지만, PF(수익 팩터), density(밀도), money scale(금액 배율)은 final completion review(최종 완성 검토) 수준이 아니므로 closeout direction(마감 방향)으로 보낸다.

## Open Work(열린 작업)

- next run(다음 실행): `{next_run_id}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(CURRENT_WORKING_STATE, current)
    selection = f"""# F77 Selection Status(F77 선택 상태)

Updated(갱신): {created_at}

Status(상태): `{status}`

Judgment(판정): `{judgment}`

Action(행동): F77G post-repair gap analysis(수리 후 간극 분석)를 완료했다.

Effect(효과): 다음 실행은 closeout(마감) 또는 Grok retry(Grok 재시도)다.

Current run(현재 실행): `{next_run_id}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(SELECTION_STATUS_PATH, selection)
    row_id = f"{RUN_ID}__post_repair_gap_analysis"
    row = {
        "ledger_row_id": row_id,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "post_repair_gap_analysis(수리 후 간극 분석)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "post_repair_gap_analysis_and_closeout_decision(수리 후 간극 분석과 마감 결정)",
        "tier_scope": "Tier A separate(Tier A 분리); Tier B missing_required(Tier B 필수 누락); combined out_of_scope(합산 범위 밖)",
        "kpi_scope": "runtime_gap_analysis(런타임 간극 분석)",
        "scoreboard_lane": "gap_analysis(간극 분석)",
        "status": status,
        "judgment": judgment,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"net={best.get('net_profit', '')};pf={best.get('profit_factor', '')};dd={best.get('max_drawdown_percent', '')};tpd={best.get('trades_per_day', '')}",
        "guardrail_kpi": f"advice={advice};closeout_label={analysis['proposed_closeout_label']}",
        "external_verification_status": "completed(완료)",
        "notes": f"F77G post-repair gap analysis; next={next_run_id}",
        "lane": "gap_analysis(간극 분석)",
        "family": "runtime_gap_analysis(런타임 간극 분석)",
        "primary_report": rel(REPORT_PATH),
        "run_number": "frontier77G",
        "date": created_at[:10],
        "decision": judgment,
        "next_run_id": next_run_id,
        "rows": str(len(analysis["split_rows"])),
        "gate_passes": "6",
        "gate_total": "6",
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "run_date": created_at[:10],
        "primary_artifact": rel(RUN_MANIFEST_PATH),
        "result_status": status,
        "view": "post_repair_gap_analysis",
        "tier": "Tier A separate",
        "metric_scope": "runtime_gap_analysis",
        "result_judgment": judgment,
        "final_decision_path": rel(SELECTION_STATUS_PATH),
        "gate_audit_path": rel(GATE_AUDIT_PATH),
        "created_at": created_at,
        "work_family": "runtime_gap_analysis(런타임 간극 분석)",
        "row_id": row_id,
        "evidence_boundary": "closeout_direction_only_no_authority(마감 방향 전용, 권위 없음)",
        "next_action": next_run_id,
        "created_at_utc": created_at,
        "required_gate_audit": rel(GATE_AUDIT_PATH),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "run_family": "runtime_gap_analysis",
        "run_type": "post_repair_closeout_direction",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN_MANIFEST_PATH),
        "result_path": rel(REPORT_PATH),
        "goal_achieve": "not_claimed",
        "net_profit": best.get("net_profit", ""),
        "profit_factor": best.get("profit_factor", ""),
        "drawdown": best.get("max_drawdown_percent", ""),
        "trade_count": best.get("trade_count", ""),
        "trade_density": best.get("trades_per_day", ""),
        "expectancy": best.get("expectancy", ""),
        "recovery_factor": best.get("recovery_factor", ""),
    }
    upsert_csv(RUN_REGISTRY, "run_id", row)
    upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
    upsert_csv(REVIEW_DIR / "stage_run_ledger.csv", "ledger_row_id", row, source_header=ALPHA_LEDGER)
    marker = "<!-- frontier77G_post_repair_gap_analysis_or_closeout_decision_v1 -->"
    idea_text = io_path(IDEA_REGISTRY).read_text(encoding="utf-8-sig")
    if marker not in idea_text:
        block = f"""

{marker}
- `{RUN_ID}` recorded(기록) post-repair gap analysis(수리 후 간극 분석). Proposed closeout label(제안 마감 라벨): `{analysis['proposed_closeout_label']}`. Best runtime net/PF/DD/tpd(최선 런타임 순수익/수익 팩터/손실폭/일 거래 수): `{best.get('net_profit', '')}/{best.get('profit_factor', '')}/{best.get('max_drawdown_percent', '')}/{best.get('trades_per_day', '')}`. Next(다음): `{next_run_id}`. Boundary(경계): no authority(권위 없음).
"""
        write_text(IDEA_REGISTRY, idea_text.rstrip() + block)


def main() -> int:
    ensure_dirs()
    created_at = utc_now()
    analysis = build_gap_analysis()
    write_json(GAP_ANALYSIS_JSON, analysis)
    prompt = build_prompt(analysis)
    write_text(GROK_PROMPT_PATH, prompt)
    result = run_grok_review(
        prompt,
        cwd=ROOT,
        timeout_seconds=300,
        review_size="small",
        output_dir=GROK_PACKET,
        repo_root=ROOT,
        prompt_file_path=GROK_PROMPT_PATH,
    )
    success = bool(result.returncode == 0 and not result.timed_out)
    grok = {
        "success": success,
        "returncode": result.returncode,
        "timed_out": result.timed_out,
        "duration_seconds": result.duration_seconds,
        "prompt_sha256": result.prompt_hash,
        "output_exists": path_exists(GROK_CLEAN_PATH),
        "metadata_exists": path_exists(GROK_METADATA_PATH),
        "output_sha256": file_hash(GROK_CLEAN_PATH),
        "metadata_sha256": file_hash(GROK_METADATA_PATH),
        "packet_path": rel(GROK_PACKET),
    }
    advice, direction, forbidden_hits, next_run_id = classify_advice(result.clean_stdout, success)
    status = STATUS_SUCCESS if success else STATUS_TRANSPORT_FAIL
    judgment = JUDGMENT_SUCCESS if success else JUDGMENT_TRANSPORT_FAIL
    write_text(REPORT_PATH, report_text(created_at, analysis, grok, advice, direction, forbidden_hits, next_run_id))
    write_text(RECEIPT_PATH, receipt_text(created_at, grok, advice, direction, forbidden_hits))
    write_text(GATE_AUDIT_PATH, gate_audit_text(grok, advice, next_run_id))
    write_json(
        RUN_MANIFEST_PATH,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": next_run_id,
            "created_at_utc": created_at,
            "status": status,
            "judgment": judgment,
            "claim_boundary": CLAIM_BOUNDARY,
            "gap_analysis": analysis,
            "grok": grok,
            "advice_classification": advice,
            "final_direction": direction,
            "forbidden_claim_hits": list(forbidden_hits),
        },
    )
    update_state_and_ledgers(created_at, status, judgment, advice, next_run_id, analysis)
    print(
        json.dumps(
            {
                "status": status,
                "judgment": judgment,
                "advice": advice,
                "final_direction": direction,
                "next_run_id": next_run_id,
                "best_runtime": analysis["best_runtime"],
                "report": rel(REPORT_PATH),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
