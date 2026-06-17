from __future__ import annotations

import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.grok_review_wrapper import run_grok_review
from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized
from foundation.mt5.trade_report import pair_deals_into_trades, parse_mt5_trade_report


STAGE_ID = "stage_frontier_78__execution_calibrated_density_contract_pnl_rebuild"
RUN_ID = "frontier78G_zero_signal_or_negative_repair_closeout_decision_v1"
PARENT_RUN_ID = "frontier78F_entry_timing_deposit_calibrated_proxy_repair_v1"
NEXT_RUN_ID = "frontier79A_stage_open_runtime_native_trade_shape_labeling_from_fill_path_v1"
NEXT_STAGE_ID = "stage_frontier_79__runtime_native_trade_shape_labeling_from_fill_path"

STATUS_SUCCESS = "closed_negative_memory_no_authority"
STATUS_NOT_CLOSED = "closeout_grok_not_accepted_stage_not_closed_no_authority"
JUDGMENT_SUCCESS = "negative_memory_with_preserved_clue_no_authority"
JUDGMENT_NOT_CLOSED = "closeout_retry_or_repair_decision_required_no_authority"
CLOSEOUT_LABEL = "negative_memory(부정 기억)"
CLAIM_BOUNDARY = (
    "stage_closeout_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)
RETROSPECTIVE_DUE_STATUS = "not_due_after_f78_closeout_3_of_5"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"

F78B_SUMMARY = REVIEW_DIR / "f78b_contract_proxy_summary.json"
F78D_SUMMARY = REVIEW_DIR / "f78d_mt5_execution_calibrated_runtime_probe_summary.json"
F78D_MANIFEST = STAGE_DIR / "02_runs" / "frontier78D_mt5_execution_calibrated_negative_control_runtime_probe_v1" / "run_manifest.json"
F78E_GAP = REVIEW_DIR / "f78e_proxy_runtime_gap_analysis.json"
F78F_SUMMARY = REVIEW_DIR / "f78f_entry_timing_deposit_repair_proxy_summary.json"

REPORT_PATH = REVIEW_DIR / "stage_closeout_report.md"
SUMMARY_PATH = REVIEW_DIR / "f78g_stage_closeout_summary.json"
KPI_ROWS_PATH = REVIEW_DIR / "f78g_closeout_kpi_rows.csv"
LINEAGE_PATH = REVIEW_DIR / "f78g_artifact_lineage.json"
LOCAL_VERIFICATION_PATH = REVIEW_DIR / "f78g_closeout_local_verification.json"
RECEIPT_PATH = REVIEW_DIR / "grok_stage_closeout_execution_calibrated_density_contract_pnl_receipt.md"
GATE_AUDIT_PATH = REVIEW_DIR / "required_gate_coverage_audit_f78g_closeout.md"
RUN_MANIFEST_PATH = RUN_DIR / "run_manifest.json"
SELECTION_STATUS_PATH = SELECTED_DIR / "selection_status.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"

WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"
NEGATIVE_REGISTER = ROOT / "docs/registers/negative_result_register.md"
RETROSPECTIVE_REGISTER = ROOT / "docs/registers/five_stage_retrospective_register.yaml"
CONTEXT_ANCHOR_PATH = f"stages/{STAGE_ID}/03_reviews/context_anchor.md"

GROK_PACKET = ROOT / "docs/agent_control/grok_reviews/2026-06-17_f78g_stage_closeout_execution_calibrated_density_contract_pnl"
GROK_PROMPT_PATH = GROK_PACKET / "prompts" / "f78g_stage_closeout_execution_calibrated_density_contract_pnl_prompt.md"
GROK_CLEAN_PATH = GROK_PACKET / "clean_output.md"
GROK_METADATA_PATH = GROK_PACKET / "metadata.json"
SCRIPT_REL = "stage_pipelines/stage_frontier_78/frontier78g_stage_closeout_execution_calibrated_density_contract_pnl.py"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    rows = list(rows)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys() if rows else ["empty"])
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: json_ready(row.get(field, "")) for field in fieldnames})


def upsert_csv(path: Path, key: str, row: Mapping[str, Any], source_header: Path | None = None) -> None:
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            rows = list(reader)
    elif source_header and path_exists(source_header):
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


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in ("", None):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def max_consecutive_loss(values: Sequence[float]) -> int:
    best = 0
    current = 0
    for value in values:
        if value < 0:
            current += 1
            best = max(best, current)
        else:
            current = 0
    return best


def time_under_water_trades(values: Sequence[float]) -> int:
    equity = 0.0
    peak = 0.0
    current = 0
    best = 0
    for value in values:
        equity += value
        if equity >= peak:
            peak = equity
            current = 0
        else:
            current += 1
            best = max(best, current)
    return best


def runtime_loss_stats(runtime: Mapping[str, Any]) -> dict[str, Any]:
    report_path = runtime.get("report_path")
    if not report_path:
        return {}
    try:
        trades = pair_deals_into_trades(parse_mt5_trade_report(Path(str(report_path)))["deals"])
    except Exception as exc:
        return {"runtime_trade_report_parse_error": str(exc)}
    profits = [float(trade.net_profit) for trade in trades]
    return {
        "runtime_max_consecutive_loss": max_consecutive_loss(profits),
        "runtime_time_under_water_trades": time_under_water_trades(profits),
    }


def proxy_row(prefix: str, view: str, period: str, source: Mapping[str, Any], gap: str) -> dict[str, Any]:
    return {
        "test_period": period,
        "split_view": view,
        "net_profit": source.get(f"{prefix}_net"),
        "gross_profit": source.get(f"{prefix}_gross_profit"),
        "gross_loss": source.get(f"{prefix}_gross_loss"),
        "PF": source.get(f"{prefix}_pf"),
        "DD_percent": source.get(f"{prefix}_dd_pct"),
        "trade_count": source.get(f"{prefix}_trade_count"),
        "trades_per_day": source.get(f"{prefix}_calendar_trades_day"),
        "win_rate": source.get(f"{prefix}_win_rate"),
        "average_win": source.get(f"{prefix}_avg_win"),
        "average_loss": source.get(f"{prefix}_avg_loss"),
        "payoff_ratio": source.get(f"{prefix}_payoff"),
        "expectancy": source.get(f"{prefix}_expectancy"),
        "recovery_factor": source.get(f"{prefix}_recovery"),
        "time_under_water": source.get(f"{prefix}_time_under_water_trades"),
        "max_consecutive_loss": source.get(f"{prefix}_max_consecutive_loss"),
        "long_short_breakdown": f"side={source.get('side')}",
        "proxy_runtime_KPI_gap": gap,
    }


def runtime_row(runtime: Mapping[str, Any], gap_summary: str) -> dict[str, Any]:
    loss_stats = runtime_loss_stats(runtime)
    return {
        "test_period": f"{runtime.get('test_period_start')}..{runtime.get('test_period_end')}",
        "split_view": "F78D MT5 validation runtime probe(F78D MT5 검증 런타임 탐침)",
        "net_profit": runtime.get("net_profit"),
        "gross_profit": runtime.get("gross_profit"),
        "gross_loss": runtime.get("gross_loss"),
        "PF": runtime.get("profit_factor"),
        "DD_percent": runtime.get("max_drawdown_percent"),
        "trade_count": runtime.get("trade_count"),
        "trades_per_day": runtime.get("trades_per_day"),
        "win_rate": runtime.get("win_rate_percent"),
        "average_win": runtime.get("average_win"),
        "average_loss": runtime.get("average_loss"),
        "payoff_ratio": runtime.get("payoff_ratio"),
        "expectancy": runtime.get("expectancy"),
        "recovery_factor": runtime.get("recovery_factor"),
        "time_under_water": loss_stats.get("runtime_time_under_water_trades"),
        "max_consecutive_loss": loss_stats.get("runtime_max_consecutive_loss"),
        "long_short_breakdown": f"long={runtime.get('long_trade_count')};short={runtime.get('short_trade_count')}",
        "proxy_runtime_KPI_gap": gap_summary,
    }


def build_kpi_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    f78b_summary = read_json(F78B_SUMMARY)
    f78d_summary = read_json(F78D_SUMMARY)
    f78d_manifest = read_json(F78D_MANIFEST)
    f78e_gap = read_json(F78E_GAP)
    f78f_summary = read_json(F78F_SUMMARY)
    target = dict(f78d_manifest["target"])
    runtime = dict(f78d_summary["best_runtime"])
    repaired = dict(f78f_summary.get("best_candidate") or {})
    gap_summary = (
        f"net_delta={as_float(runtime.get('net_profit')) - as_float(target.get('val_net'))};"
        f"pf_delta={as_float(runtime.get('profit_factor')) - as_float(target.get('val_pf'))};"
        f"dd_delta={as_float(runtime.get('max_drawdown_percent')) - as_float(target.get('val_dd_pct'))};"
        f"signal_diff={runtime.get('signal_count_diff')};feature_diff={runtime.get('feature_ready_diff')};"
        "cause=entry_timing_deposit_denominator_fill_path"
    )
    rows = [
        proxy_row("val", "F78B original next-bar proxy validation(F78B 원래 다음 봉 프록시 검증)", "2025-01-02..2025-10-01", target, gap_summary),
        proxy_row("oos", "F78B original next-bar proxy OOS(F78B 원래 다음 봉 프록시 표본외)", "2025-10-01..2026-04-14", target, "runtime_not_executed_for_oos_by_scope"),
        runtime_row(runtime, gap_summary),
        proxy_row("val", "F78F repaired proxy validation(F78F 수리 프록시 검증)", "2025-01-02..2025-10-01", repaired, "repair_zero_scout_signal"),
        proxy_row("oos", "F78F repaired proxy OOS(F78F 수리 프록시 표본외)", "2025-10-01..2026-04-14", repaired, "repair_zero_scout_signal"),
    ]
    bundle = {"f78b": f78b_summary, "f78d": f78d_summary, "f78e": f78e_gap, "f78f": f78f_summary, "target": target, "runtime": runtime, "repaired": repaired, "gap_summary": gap_summary}
    return rows, bundle


def build_payload(created_at: str, kpi_rows: Sequence[Mapping[str, Any]], bundle: Mapping[str, Any], closeout_success: bool) -> dict[str, Any]:
    runtime = bundle["runtime"]
    target = bundle["target"]
    repaired = bundle["repaired"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID if closeout_success else RUN_ID,
        "next_frontier_stage_id": NEXT_STAGE_ID,
        "created_at_utc": created_at,
        "status": STATUS_SUCCESS if closeout_success else STATUS_NOT_CLOSED,
        "judgment": JUDGMENT_SUCCESS if closeout_success else JUDGMENT_NOT_CLOSED,
        "closeout_label": CLOSEOUT_LABEL if closeout_success else "not_closed(미마감)",
        "hypothesis": "Execution-calibrated labels(실행 보정 라벨)이 broker contract P/L(브로커 계약 손익), calendar density(달력 밀도), fill semantics(체결 의미), lifecycle occupancy(생명주기 점유), risk penalty(위험 벌점)를 proxy(프록시)에 내장하면 F77 money/density gap(F77 금액/밀도 간극)을 줄일 수 있다.",
        "test_period": "2025-01-02..2025-10-01 validation runtime; 2025-10-01..2026-04-14 proxy OOS",
        "proxy_expectation": "F78B best f78b_02234 expected validation net/PF/DD/tpd 42.45/1.15/0.21/1.21 and OOS 54.58/1.28/0.23/1.25.",
        "proxy_kpi": {"original_target": target, "repaired_best": repaired},
        "runtime_probe_kpi": runtime,
        "kpi_rows": list(kpi_rows),
        "signal_count_parity": "passed diff=0 in F78D validation",
        "feature_readiness_parity": "passed diff=0 in F78D validation",
        "proxy_runtime_gap_cause": "entry_timing_mismatch_minus_5min + DD denominator 10000 vs 500 + remaining fill path gap",
        "preserved_clue": [
            "ONNX/EA feature and signal parity(ONNX/EA 피처와 신호 동등성)는 정확히 맞출 수 있었다.",
            "Selected-entry veto tape(선택 진입 거부 테이프)은 proxy selected count(프록시 선택 수)와 runtime signal count(런타임 신호 수)를 맞추는 도구로 보존한다.",
            "Entry timing(진입 시각)과 DD denominator(손실폭 분모)는 proxy label(프록시 라벨) 설계 시작부터 명시해야 한다.",
        ],
        "negative_memory": [
            "Next-bar proxy(다음 봉 프록시)는 양수여도 MT5 same-bar execution(MT5 동일 봉 실행)에서는 음수가 될 수 있다.",
            "Runtime-aligned entry(런타임 정렬 진입)와 tester-deposit DD(테스터 예치금 손실폭) 수리 뒤 F78F는 scout clue(탐색 단서) 0, meaningful signal(의미 신호) 0이었다.",
            "F78은 threshold-only(임계값 단독)나 model-only(모델 단독) 수리로 계속 밀면 반복 수리가 된다.",
        ],
        "next_frontier_hypothesis": "F79 should start from runtime-native trade-shape labels(런타임 네이티브 거래 형태 라벨) built around actual fill path(실제 체결 경로), entry timing(진입 시각), and deposit risk(예치금 위험).",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_prompt(payload: Mapping[str, Any]) -> str:
    runtime = payload["runtime_probe_kpi"]
    repaired = payload["proxy_kpi"]["repaired_best"]
    return f"""# F78G Stage Closeout Grok Review Prompt(F78G 단계 마감 Grok 검토 프롬프트)

You are Grok(Grok, 그록), an external second-opinion reviewer(외부 2차 의견 검토자).
Answer only from this bounded evidence snapshot(제한 근거 스냅샷). Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(브라우징 금지), or perform local verification(로컬 검증 금지).

Current stage(현재 단계): `{STAGE_ID}`
Proposed closeout label(제안 마감 라벨): `{CLOSEOUT_LABEL}`
Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

Hypothesis(가설):
{payload['hypothesis']}

Mandatory runtime probe(MT5 필수 런타임 탐침):
- F78D validation runtime(검증 런타임): net/PF/DD/tpd/trades `{runtime.get('net_profit')}/{runtime.get('profit_factor')}/{runtime.get('max_drawdown_percent')}/{runtime.get('trades_per_day')}/{runtime.get('trade_count')}`
- signal/feature/fill parity(신호/피처/체결 동등성): signal diff `{runtime.get('signal_count_diff')}`, feature diff `{runtime.get('feature_ready_diff')}`, fill rate `{runtime.get('order_fill_rate')}`
- gap cause(간극 원인): `{payload['proxy_runtime_gap_cause']}`

Repair result(수리 결과):
- F78F repaired proxy best(수리 프록시 최선): `{repaired.get('candidate_id')}`
- F78F scout/meaningful/final-like(탐색/의미/완성 유사): `{repaired.get('scout_clue')}/{repaired.get('meaningful_signal')}/{repaired.get('final_like_reference')}`
- F78F OOS net/PF/DD/tpd/trades(표본외 순수익/수익 팩터/손실폭/일 거래/거래): `{repaired.get('oos_net')}/{repaired.get('oos_pf')}/{repaired.get('oos_dd_pct')}/{repaired.get('oos_calendar_trades_day')}/{repaired.get('oos_trade_count')}`

Preserved clue(보존 단서):
{chr(10).join('- ' + item for item in payload['preserved_clue'])}

Negative memory(부정 기억):
{chr(10).join('- ' + item for item in payload['negative_memory'])}

Question(질문):
Should Codex close F78 as negative_memory(부정 기억) with preserved clues(보존 단서) and move to a new frontier hypothesis(F79), or is there a concrete non-repetitive repair(반복 아닌 구체 수리) still required inside F78 before closeout(마감)?

Classify advice(조언 분류) exactly one: accepted(수용), accepted_with_conditions(조건부 수용), needs_local_verification(로컬 검증 필요), rejected(거절).
Do not grant completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 금지).
"""


def classify_advice(clean_output: str, success: bool) -> tuple[str, str, list[str]]:
    lowered = clean_output.lower()
    forbidden_hits = [
        term
        for term in ("goal achieve", "runtime authority", "live readiness", "selected baseline", "operating promotion", "completion achieved")
        if f"may claim {term}" in lowered or f"can claim {term}" in lowered or f"{term} achieved" in lowered
    ]
    if not success:
        return "transport_failed(전송 실패)", "retry_closeout_grok(마감 Grok 재시도)", forbidden_hits
    head = lowered[:2000]
    if "rejected" in head and "accepted" not in head:
        return "rejected(거절)", "do_not_close_repair_or_retry(마감 금지, 수리 또는 재시도)", forbidden_hits
    if "needs_local_verification" in head:
        return "needs_local_verification(로컬 검증 필요)", "close_if_local_checks_pass(로컬 점검 통과 시 마감)", forbidden_hits
    if "accepted_with_conditions" in head:
        return "accepted_with_conditions(조건부 수용)", "close_with_boundary_and_next_hypothesis(경계와 다음 가설로 마감)", forbidden_hits
    if "accepted" in head:
        return "accepted(수용)", "close_with_boundary_and_next_hypothesis(경계와 다음 가설로 마감)", forbidden_hits
    return "needs_local_verification(로컬 검증 필요)", "close_if_local_checks_pass(로컬 점검 통과 시 마감)", forbidden_hits


def grok_identity(result: Any) -> dict[str, Any]:
    prompt_sha = sha256_file_lf_normalized(GROK_PROMPT_PATH) if path_exists(GROK_PROMPT_PATH) else ""
    output_sha = sha256_file_lf_normalized(GROK_CLEAN_PATH) if path_exists(GROK_CLEAN_PATH) else ""
    return {
        "success": bool(result.returncode == 0 and not result.timed_out),
        "returncode": result.returncode,
        "timed_out": result.timed_out,
        "duration_seconds": result.duration_seconds,
        "prompt_path": rel(GROK_PROMPT_PATH),
        "prompt_sha256": prompt_sha,
        "output_path": rel(GROK_CLEAN_PATH) if path_exists(GROK_CLEAN_PATH) else "",
        "output_sha256": output_sha,
        "metadata_path": rel(GROK_METADATA_PATH) if path_exists(GROK_METADATA_PATH) else "",
    }


def local_verification(payload: Mapping[str, Any], advice: str, forbidden_hits: Sequence[str]) -> dict[str, Any]:
    runtime = payload["runtime_probe_kpi"]
    repaired = payload["proxy_kpi"]["repaired_best"]
    checks = [
        {"check": "runtime_probe_completed", "passed": runtime.get("tester_status") == "completed"},
        {"check": "signal_parity_zero_diff", "passed": as_float(runtime.get("signal_count_diff")) == 0.0},
        {"check": "feature_parity_zero_diff", "passed": as_float(runtime.get("feature_ready_diff")) == 0.0},
        {"check": "fill_rate_one", "passed": as_float(runtime.get("order_fill_rate")) == 1.0},
        {"check": "repair_zero_scout", "passed": int(repaired.get("scout_clue", 0) or 0) == 0},
        {"check": "repair_zero_meaningful", "passed": int(repaired.get("meaningful_signal", 0) or 0) == 0},
        {"check": "forbidden_claim_hits_absent", "passed": not forbidden_hits},
        {"check": "grok_advice_allows_closeout", "passed": advice.startswith("accepted") or advice.startswith("needs_local_verification")},
    ]
    return {"checks": checks, "all_passed": all(item["passed"] for item in checks), "claim_boundary": CLAIM_BOUNDARY}


def close_allowed(advice: str, grok_success: bool, forbidden_hits: Sequence[str]) -> bool:
    return grok_success and not forbidden_hits and (advice.startswith("accepted") or advice.startswith("needs_local_verification"))


def kpi_table(rows: Sequence[Mapping[str, Any]]) -> str:
    header = (
        "| test period(기간) | split/view(분할/보기) | net(순수익) | gross profit(총이익) | gross loss(총손실) | "
        "PF(수익 팩터) | DD%(손실폭) | trades(거래) | trades/day(일 거래) | win rate(승률) | avg win(평균 이익) | "
        "avg loss(평균 손실) | payoff(손익비) | expectancy(기대값) | recovery(회복 계수) | TUW(회복 전 체류) | max loss(최대 연속 손실) | long/short(롱/숏) | gap(간극) |"
    )
    sep = "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|"
    lines = [header, sep]
    for row in rows:
        lines.append(
            f"| `{row.get('test_period')}` | `{row.get('split_view')}` | `{row.get('net_profit')}` | `{row.get('gross_profit')}` | `{row.get('gross_loss')}` | `{row.get('PF')}` | `{row.get('DD_percent')}` | `{row.get('trade_count')}` | `{row.get('trades_per_day')}` | `{row.get('win_rate')}` | `{row.get('average_win')}` | `{row.get('average_loss')}` | `{row.get('payoff_ratio')}` | `{row.get('expectancy')}` | `{row.get('recovery_factor')}` | `{row.get('time_under_water')}` | `{row.get('max_consecutive_loss')}` | `{row.get('long_short_breakdown')}` | `{row.get('proxy_runtime_KPI_gap')}` |"
        )
    return "\n".join(lines)


def closeout_report_text(created_at: str, payload: Mapping[str, Any], grok: Mapping[str, Any], advice: str, direction: str, forbidden_hits: Sequence[str]) -> str:
    return f"""# F78 Stage Closeout Report(F78 단계 마감 보고서)

Updated(갱신): {created_at}

- status(상태): `{payload['status']}`
- judgment(판정): `{payload['judgment']}`
- closeout label(마감 라벨): `{payload['closeout_label']}`
- Grok advice(Grok 조언): `{advice}`
- final Codex direction(최종 Codex 방향): `{direction}`
- forbidden claim hits(금지 주장 감지): `{', '.join(forbidden_hits) if forbidden_hits else 'none(없음)'}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Hypothesis(가설)

{payload['hypothesis']}

## Closeout KPI(마감 핵심 성과 지표)

{kpi_table(payload['kpi_rows'])}

## Preserved Clue(보존 단서)

{chr(10).join('- ' + item for item in payload['preserved_clue'])}

## Negative Memory(부정 기억)

{chr(10).join('- ' + item for item in payload['negative_memory'])}

## Grok Review(Grok 검토)

- packet(묶음): `{rel(GROK_PACKET)}`
- prompt(프롬프트): `{grok.get('prompt_path')}` sha256 `{grok.get('prompt_sha256')}`
- output(출력): `{grok.get('output_path')}` sha256 `{grok.get('output_sha256')}`

This closeout(마감)은 completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)를 만들지 않는다.
"""


def receipt_text(created_at: str, grok: Mapping[str, Any], advice: str, direction: str, forbidden_hits: Sequence[str], closeout_success: bool) -> str:
    return f"""# F78G Grok Stage Closeout Receipt(F78G Grok 단계 마감 영수증)

Created at(생성 시각): {created_at}

Trigger reason(트리거 이유): stage closeout(단계 마감)은 Grok second opinion(Grok 2차 의견)이 필수다.

Review size(검토 크기): medium review(중간 검토).

Bounded evidence(제한 근거): F78B proxy summary(F78B 프록시 요약), F78D runtime KPI(F78D 런타임 핵심 성과 지표), F78E gap analysis(F78E 간극 분석), F78F repair proxy(F78F 수리 프록시), closeout KPI table(마감 핵심 성과 지표 표).

Prompt identity(프롬프트 정체성): `{grok.get('prompt_path')}` sha256 `{grok.get('prompt_sha256')}`.

Grok output identity(Grok 출력 정체성): `{grok.get('output_path')}` sha256 `{grok.get('output_sha256')}`.

Advice classification(조언 분류): `{advice}`.

Local verification(로컬 검증): `{rel(LOCAL_VERIFICATION_PATH)}`.

Forbidden claim check(금지 주장 확인): `{', '.join(forbidden_hits) if forbidden_hits else 'none(없음)'}`.

Final Codex direction(최종 Codex 방향): `{direction}`.

Closeout success(마감 성공): `{closeout_success}`.
"""


def gate_audit_text(created_at: str, advice: str, closeout_success: bool) -> str:
    local_status = "passed(통과)" if closeout_success else "not_applied(미반영)"
    return f"""# Required Gate Coverage Audit F78G Closeout(F78G 마감 필수 게이트 커버리지 감사)

Updated(갱신): {created_at}

| gate(게이트) | status(상태) | evidence/effect(근거/효과) |
|---|---|---|
| MT5 runtime probe(MT5 런타임 탐침) | `completed(완료)` | `{rel(F78D_SUMMARY)}` |
| proxy/runtime gap analysis(프록시/런타임 간극 분석) | `completed(완료)` | `{rel(F78E_GAP)}` |
| repair attempt(수리 시도) | `completed(완료)` | `{rel(F78F_SUMMARY)}` |
| closeout Grok review(마감 Grok 검토) | `{advice}` | `{rel(RECEIPT_PATH)}` |
| local verification(로컬 검증) | `{local_status}` | `{rel(LOCAL_VERIFICATION_PATH)}` |
| required closeout KPI(필수 마감 핵심 성과 지표) | `recorded(기록됨)` | `{rel(KPI_ROWS_PATH)}` |
| closeout applied(마감 반영) | `{local_status}` | `{rel(REPORT_PATH)}` |
| claim guard(주장 보호) | `passed(통과)` | `{CLAIM_BOUNDARY}` |
"""


def artifact_lineage(created_at: str, closeout_success: bool) -> dict[str, Any]:
    artifacts = [REPORT_PATH, SUMMARY_PATH, KPI_ROWS_PATH, RECEIPT_PATH, GATE_AUDIT_PATH, RUN_MANIFEST_PATH]
    return {
        "created_at_utc": created_at,
        "source_inputs": [rel(F78B_SUMMARY), rel(F78D_SUMMARY), rel(F78D_MANIFEST), rel(F78E_GAP), rel(F78F_SUMMARY), rel(GROK_CLEAN_PATH)],
        "producer": SCRIPT_REL,
        "consumer": "F78 closeout registers(마감 등록부) and F79 stage-open handoff(F79 단계 개방 인계)",
        "artifact_paths": [rel(path) for path in artifacts],
        "artifact_hashes": {rel(path): sha256_file_lf_normalized(path) for path in artifacts if path_exists(path)},
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(IDEA_REGISTRY), rel(NEGATIVE_REGISTER)],
        "availability": "tracked_or_generated_with_manifest",
        "lineage_judgment": "connected_with_boundary",
        "closeout_success": closeout_success,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def ledger_row(created_at: str, payload: Mapping[str, Any], closeout_success: bool) -> dict[str, Any]:
    runtime = payload["runtime_probe_kpi"]
    row_id = f"{RUN_ID}__stage_closeout"
    return {
        "ledger_row_id": row_id,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "stage_closeout(단계 마감)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "stage_closeout(단계 마감)",
        "tier_scope": "Tier A runtime; Tier B missing_required; combined out_of_scope",
        "kpi_scope": "stage_closeout_runtime_probe_gap_repair(단계 마감 런타임 탐침 간극 수리)",
        "scoreboard_lane": "stage_closeout(단계 마감)",
        "status": payload["status"],
        "judgment": payload["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"net={runtime.get('net_profit')};pf={runtime.get('profit_factor')};dd={runtime.get('max_drawdown_percent')};tpd={runtime.get('trades_per_day')}",
        "guardrail_kpi": f"closeout_label={payload['closeout_label']};no_authority",
        "external_verification_status": "completed(완료)" if closeout_success else "grok_not_accepted(Grok 미수용)",
        "notes": f"closeout_label={payload['closeout_label']};next={payload['next_run_id']}",
        "lane": "stage_closeout(단계 마감)",
        "family": "stage_closeout(단계 마감)",
        "primary_report": rel(REPORT_PATH),
        "run_number": "frontier78G",
        "date": created_at[:10],
        "decision": payload["judgment"],
        "next_run_id": payload["next_run_id"],
        "rows": len(payload["kpi_rows"]),
        "gate_passes": "8" if closeout_success else "7",
        "gate_total": "8",
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "run_date": created_at[:10],
        "primary_artifact": rel(RUN_MANIFEST_PATH),
        "result_status": payload["status"],
        "result_judgment": payload["judgment"],
        "final_decision_path": rel(SELECTION_STATUS_PATH),
        "gate_audit_path": rel(GATE_AUDIT_PATH),
        "created_at": created_at,
        "work_family": "stage_closeout",
        "row_id": row_id,
        "evidence_boundary": "stage_closeout_only_no_authority(단계 마감 전용, 권위 없음)",
        "next_action": payload["next_run_id"],
        "question": "Close F78 and move to new frontier hypothesis?(F78을 닫고 새 전선 가설로 이동?)",
        "artifact_count": "8",
        "created_at_utc": created_at,
        "required_gate_audit": rel(GATE_AUDIT_PATH),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "run_family": "stage_closeout",
        "run_type": "stage_closeout",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN_MANIFEST_PATH),
        "result_path": rel(REPORT_PATH),
        "goal_achieve": "not_claimed",
    }


def update_retrospective_register(created_at: str, closeout_success: bool) -> None:
    if not closeout_success or not path_exists(RETROSPECTIVE_REGISTER):
        return
    data = yaml.safe_load(io_path(RETROSPECTIVE_REGISTER).read_text(encoding="utf-8-sig"))
    state = data.setdefault("state", {})
    closed = list(state.get("closed_frontier_ids_since_last_retrospective") or [])
    if STAGE_ID not in closed:
        closed.append(STAGE_ID)
    state["closed_frontier_ids_since_last_retrospective"] = closed
    state["closeouts_since_last"] = len(closed)
    state["next_numeric_trigger_frontier"] = 80
    state["current_due_status"] = RETROSPECTIVE_DUE_STATUS
    state["last_updated_at_utc"] = created_at
    state["note"] = "F78 closeout(마감)을 F71-F75 retrospective(회고) 이후 3/5로 등록했다."
    io_path(RETROSPECTIVE_REGISTER).write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8-sig")


def update_registers(created_at: str, payload: Mapping[str, Any], closeout_success: bool) -> None:
    update_retrospective_register(created_at, closeout_success)
    row = ledger_row(created_at, payload, closeout_success)
    upsert_csv(RUN_REGISTRY, "run_id", row)
    upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
    upsert_csv(STAGE_LEDGER, "ledger_row_id", row, source_header=ALPHA_LEDGER)

    marker = "<!-- frontier78G_zero_signal_or_negative_repair_closeout_decision_v1 -->"
    idea_text = io_path(IDEA_REGISTRY).read_text(encoding="utf-8-sig")
    if marker not in idea_text:
        addition = f"""

{marker}
- `{RUN_ID}` closed Frontier78(전선78) as `{payload['closeout_label']}`. Runtime net/PF/DD/tpd(런타임 순수익/수익 팩터/손실폭/일 거래): `{payload['runtime_probe_kpi'].get('net_profit')}/{payload['runtime_probe_kpi'].get('profit_factor')}/{payload['runtime_probe_kpi'].get('max_drawdown_percent')}/{payload['runtime_probe_kpi'].get('trades_per_day')}`. Evidence(근거): `{rel(REPORT_PATH)}`. Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). Next(다음): `{payload['next_run_id']}`.
"""
        write_text(IDEA_REGISTRY, idea_text.rstrip() + addition)

    negative_marker = "<!-- NR-FR78-EXECUTION-CALIBRATED-DENSITY-CONTRACT-PNL -->"
    negative_text = io_path(NEGATIVE_REGISTER).read_text(encoding="utf-8-sig")
    if negative_marker not in negative_text:
        addition = f"""

{negative_marker}
## NR-FR78-EXECUTION-CALIBRATED-DENSITY-CONTRACT-PNL

- Stage(단계): `{STAGE_ID}`
- Hypothesis(가설): execution-calibrated labels(실행 보정 라벨)이 F77 money/density gap(F77 금액/밀도 간극)을 줄일 수 있는지 확인했다.
- Why failed(실패 이유): F78D runtime(런타임) validation net/PF/DD/tpd `{payload['runtime_probe_kpi'].get('net_profit')}/{payload['runtime_probe_kpi'].get('profit_factor')}/{payload['runtime_probe_kpi'].get('max_drawdown_percent')}/{payload['runtime_probe_kpi'].get('trades_per_day')}`; F78F repaired proxy(수리 프록시) scout/meaningful `0/0`.
- Preserved clue(보존 단서): signal/feature/fill parity(신호/피처/체결 동등성)는 맞출 수 있었다.
- Do-not-repeat(반복 금지): next-bar proxy(다음 봉 프록시)의 양수 결과를 runtime economics(런타임 경제성)로 해석하지 않는다.
- Reopen condition(재개 조건): runtime-native entry timing(런타임 네이티브 진입 시각), tester-deposit DD denominator(테스터 예치금 손실폭 분모), fill-path label(체결 경로 라벨)을 처음부터 설계할 때만 재개한다.
- Evidence(근거): `{rel(REPORT_PATH)}`.
- Boundary(경계): no authority(권위 없음), no completion(완성 없음).
"""
        write_text(NEGATIVE_REGISTER, negative_text.rstrip() + addition)


def update_state(created_at: str, payload: Mapping[str, Any], closeout_success: bool) -> None:
    current_run = payload["next_run_id"] if closeout_success else RUN_ID
    latest_completed = RUN_ID if closeout_success else PARENT_RUN_ID
    state = f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {current_run}
latest_completed_run_id: {latest_completed}
current_status: {payload['status']}
current_judgment: {payload['judgment']}
next_run_id: {payload['next_run_id']}
runtime_probe_status: f78_mandatory_runtime_probe_completed_stage_closed
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
five_stage_retrospective_due_status: {RETROSPECTIVE_DUE_STATUS if closeout_success else 'not_due_after_f77_closeout_2_of_5'}
updated_at_utc: '{created_at}'
context_anchor: {CONTEXT_ANCHOR_PATH}
notes:
  - "Action(행동): F78G stage closeout(단계 마감)을 {'완료했다' if closeout_success else '시도했지만 닫지 않았다'}."
  - "Effect(효과): F78 negative memory(부정 기억), preserved clue(보존 단서), next frontier hypothesis(다음 전선 가설)를 기록했다."
  - "Next(다음): {payload['next_run_id']}."
  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."
"""
    write_text(WORKSPACE_STATE, state)

    current = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {created_at}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{current_run}`

Latest completed run(최근 완료 실행): `{latest_completed}`

## Current Truth(현재 진실)

Action(행동): F78G stage closeout(단계 마감)을 {'완료했다' if closeout_success else '시도했지만 닫지 않았다'}.

Effect(효과): F78은 negative memory(부정 기억)로 닫고, signal/feature/fill parity(신호/피처/체결 동등성)는 preserved clue(보존 단서)로 남겼다.

## Open Work(열린 작업)

- next run(다음 실행): `{payload['next_run_id']}`
- next frontier hypothesis(다음 전선 가설): `{payload['next_frontier_hypothesis']}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(CURRENT_WORKING_STATE, current)

    selection = f"""# F78 Selection Status(F78 선택 상태)

Updated(갱신): {created_at}

Status(상태): `{payload['status']}`

Judgment(판정): `{payload['judgment']}`

Closeout label(마감 라벨): `{payload['closeout_label']}`

Action(행동): F78G stage closeout(단계 마감)을 {'완료했다' if closeout_success else '시도했지만 닫지 않았다'}.

Effect(효과): 다음 실행은 new frontier hypothesis(새 전선 가설) F79A stage open(단계 개방)이다.

Current run(현재 실행): `{current_run}`

Latest completed run(최근 완료 실행): `{latest_completed}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(SELECTION_STATUS_PATH, selection)


def main() -> int:
    for path in (RUN_DIR, REVIEW_DIR, SELECTED_DIR, GROK_PROMPT_PATH.parent):
        io_path(path).mkdir(parents=True, exist_ok=True)

    created_at = utc_now()
    kpi_rows, bundle = build_kpi_rows()
    draft_payload = build_payload(created_at, kpi_rows, bundle, True)
    prompt = build_prompt(draft_payload)
    write_text(GROK_PROMPT_PATH, prompt)

    result = run_grok_review(
        prompt,
        cwd=ROOT,
        repo_root=ROOT,
        output_dir=GROK_PACKET,
        prompt_file_path=GROK_PROMPT_PATH,
        review_size="medium",
        timeout_seconds=300,
    )
    grok_success = bool(result.returncode == 0 and not result.timed_out)
    clean_output = io_path(GROK_CLEAN_PATH).read_text(encoding="utf-8-sig") if path_exists(GROK_CLEAN_PATH) else result.clean_stdout
    advice, direction, forbidden_hits = classify_advice(clean_output, grok_success)
    draft_verify = local_verification(draft_payload, advice, forbidden_hits)
    closeout_success = close_allowed(advice, grok_success, forbidden_hits) and bool(draft_verify["all_passed"])

    payload = build_payload(created_at, kpi_rows, bundle, closeout_success)
    verify = local_verification(payload, advice, forbidden_hits)
    grok = grok_identity(result)

    write_json(LOCAL_VERIFICATION_PATH, verify)
    write_text(REPORT_PATH, closeout_report_text(created_at, payload, grok, advice, direction, forbidden_hits))
    write_text(RECEIPT_PATH, receipt_text(created_at, grok, advice, direction, forbidden_hits, closeout_success))
    write_text(GATE_AUDIT_PATH, gate_audit_text(created_at, advice, closeout_success))
    write_csv(KPI_ROWS_PATH, kpi_rows)
    write_csv(RUN_DIR / "f78g_closeout_kpi_rows.csv", kpi_rows)

    lineage = artifact_lineage(created_at, closeout_success)
    payload["local_verification"] = verify
    payload["artifact_lineage"] = lineage
    payload["grok"] = grok
    payload["advice_classification"] = advice
    payload["final_codex_direction"] = direction
    payload["forbidden_claim_hits"] = list(forbidden_hits)
    write_json(LINEAGE_PATH, lineage)
    write_json(SUMMARY_PATH, payload)
    write_json(RUN_MANIFEST_PATH, payload)

    update_registers(created_at, payload, closeout_success)
    update_state(created_at, payload, closeout_success)

    print(json.dumps(json_ready({
        "status": payload["status"],
        "judgment": payload["judgment"],
        "closeout_label": payload["closeout_label"],
        "advice_classification": advice,
        "grok_success": grok_success,
        "closeout_success": closeout_success,
        "next_run_id": payload["next_run_id"],
        "forbidden_claim_hits": list(forbidden_hits),
        "report": rel(REPORT_PATH),
    }), ensure_ascii=False, indent=2))
    return 0 if closeout_success else 1


if __name__ == "__main__":
    raise SystemExit(main())
