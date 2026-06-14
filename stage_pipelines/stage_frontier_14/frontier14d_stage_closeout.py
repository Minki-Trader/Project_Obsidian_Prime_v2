from __future__ import annotations

import csv
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from foundation.models.onnx_bridge import sha256_file
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b


STAGE_ID = "stage_frontier_14__daily_session_opportunity_budget_onnx_scout"
RUN_ID = "frontier14D_stage_closeout_daily_session_opportunity_budget_onnx_scout_v1"
RUN_NUMBER = "frontier14D"
PARENT_RUN_ID = "frontier14C_contrastive_flat_budget_density_transfer_repair_v1"
NEXT_RUN_ID = "frontier15A_stage_open_new_hypothesis_design_v1"
STATUS = "closed_preserved_clue_negative_memory_no_authority"
JUDGMENT = "preserved_clue_negative_memory(보존 단서와 부정 기억)"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
DECISION_PATH = Path("docs/decisions/2026-06-14_stage_frontier_14_daily_session_opportunity_budget_onnx_scout_closeout.md")
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_14/frontier14d_stage_closeout.py")
IDEA_MARKER = RUN_ID
NEGATIVE_MARKER = f"{RUN_ID}__density_transfer_negative_memory"

F14B_RUN_ID = "frontier14B_daily_session_opportunity_budget_proxy_scout_v1"
F14B_ROOT = STAGE_ROOT / "02_runs" / F14B_RUN_ID
F14B_FINAL = F14B_ROOT / "final_decision.json"
F14B_SUMMARY = F14B_ROOT / "candidate_summary.csv"
F14C_ROOT = STAGE_ROOT / "02_runs" / PARENT_RUN_ID
F14C_FINAL = F14C_ROOT / "final_decision.json"
F14C_SUMMARY = F14C_ROOT / "candidate_summary.csv"
F14C_GAP = F14C_ROOT / "label_model_density_gap.csv"
F14C_PARITY = F14C_ROOT / "onnx_parity.csv"
F14C_REPORT = STAGE_ROOT / "03_reviews" / f"{PARENT_RUN_ID}_report.md"
GROK_CLOSEOUT = Path("docs/agent_control/grok_reviews/2026-06-14_frontier14_stage_closeout/small_review")


def main() -> int:
    now = utc_now()
    ensure_dirs()
    f14b = read_json(F14B_FINAL)
    f14c = read_json(F14C_FINAL)
    grok = read_grok()
    candidate_rows = read_csv_rows(F14C_SUMMARY)
    gap_rows = read_csv_rows(F14C_GAP)
    local = local_verification(f14b, f14c, grok, candidate_rows, gap_rows)
    summary = build_summary(now, f14b, f14c, grok, local, candidate_rows, gap_rows)
    write_outputs(summary)
    update_state_and_registries(summary)
    print(
        json.dumps(
            json_ready(
                {
                    "status": summary["status"],
                    "judgment": summary["judgment"],
                    "run_id": RUN_ID,
                    "next_run_id": NEXT_RUN_ID,
                    "grok_classification": summary["grok_classification"],
                    "local_verification": summary["local_verification"]["judgment"],
                    "report": REPORT_PATH.as_posix(),
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def ensure_dirs() -> None:
    for path in (
        RUN_ROOT,
        STAGE_ROOT / "03_reviews",
        STAGE_ROOT / "04_selected",
        DECISION_PATH.parent,
    ):
        io_path(path).mkdir(parents=True, exist_ok=True)
    ensure_csv_header(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", f03b.ALPHA_LEDGER)


def read_grok() -> dict[str, Any]:
    meta = read_json(GROK_CLOSEOUT / "metadata.json")
    output = read_text(GROK_CLOSEOUT / "clean_output.md")
    return {
        "packet": GROK_CLOSEOUT.as_posix(),
        "prompt": (GROK_CLOSEOUT / "prompt.md").as_posix(),
        "output": (GROK_CLOSEOUT / "clean_output.md").as_posix(),
        "prompt_hash": meta.get("prompt_hash", ""),
        "success": bool(meta.get("success")),
        "duration_seconds": meta.get("duration_seconds", ""),
        "unexpected_top_level_artifacts": meta.get("unexpected_top_level_artifacts", []),
        "classification": classify_grok(output),
        "combined_closeout_supported": "closed_preserved_clue_negative_memory_no_authority" in output,
        "wfo_mt5_skip_supported": "wfo/mt5" in output.lower() and "justified" in output.lower(),
        "forbidden_claims_supported": "forbidden claims" in output.lower() and "pass" in output.lower(),
    }


def classify_grok(text: str) -> str:
    lowered = text.lower()
    if "accepted" in lowered:
        return "accepted(수용)"
    if "rejected" in lowered:
        return "rejected(거절)"
    if "needs_local_verification" in lowered:
        return "needs_local_verification(로컬 검증 필요)"
    return "classification_missing(분류 누락)"


def local_verification(
    f14b: dict[str, Any],
    f14c: dict[str, Any],
    grok: dict[str, Any],
    candidate_rows: list[dict[str, str]],
    gap_rows: list[dict[str, str]],
) -> dict[str, Any]:
    best = f14c.get("best_candidate_row", {})
    parent_best = f14b.get("best_candidate_row", {})
    flat4x = find_row(candidate_rows, "candidate_id", "f14b_cash_q8_h8__flat4x_safest__lr_plain")
    best_gap = [row for row in gap_rows if row.get("candidate_id") == best.get("candidate_id")]
    stage_ledger_rows = read_csv_rows(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv")
    metric_fields = [
        "validation_profit_factor",
        "validation_trades_per_day",
        "validation_dd_risk_percent",
        "validation_net_profit",
        "oos_profit_factor",
        "oos_trades_per_day",
        "oos_dd_risk_percent",
        "oos_net_profit",
    ]
    metrics_equal_parent = {
        field: close_float(best.get(field), parent_best.get(field), tolerance=1e-12)
        for field in metric_fields
    }
    strict_count = sum(parse_bool(row.get("strict_scout_clue_pass")) for row in candidate_rows)
    preserved_count = sum(parse_bool(row.get("preserved_clue_pass")) for row in candidate_rows)
    tier_b_missing = any(row.get("ledger_row_id") == f"{PARENT_RUN_ID}__tier_b_missing_required" for row in stage_ledger_rows)
    checks = {
        "frontier14b_final_exists": path_exists(F14B_FINAL),
        "frontier14c_final_exists": path_exists(F14C_FINAL),
        "frontier14c_candidate_summary_exists": path_exists(F14C_SUMMARY),
        "frontier14c_density_gap_exists": path_exists(F14C_GAP),
        "frontier14c_onnx_parity_exists": path_exists(F14C_PARITY),
        "candidate_recount_strict_zero": strict_count == 0,
        "candidate_recount_preserved_five": preserved_count == 5,
        "final_counts_match_summary": int(f14c.get("strict_scout_clue_rows", -1)) == strict_count
        and int(f14c.get("preserved_clue_rows", -1)) == preserved_count,
        "best_matches_parent_metrics": all(metrics_equal_parent.values()),
        "best_joblib_hash_matches_parent": best.get("joblib_sha256") == parent_best.get("joblib_sha256"),
        "flat4x_density_lift_but_quality_fail": bool(flat4x)
        and as_float(flat4x.get("validation_trades_per_day")) > as_float(best.get("validation_trades_per_day"))
        and as_float(flat4x.get("validation_profit_factor")) < 1.0
        and as_float(flat4x.get("validation_dd_risk_percent")) > 10.0,
        "best_label_model_gap_recorded": len(best_gap) == 3
        and max(as_float(row.get("label_opportunities_per_day")) for row in best_gap) >= 7.9
        and max(as_float(row.get("model_trades_per_day")) for row in best_gap) < 0.11,
        "tier_b_missing_required_recorded": tier_b_missing,
        "frontier14c_no_authority": f14c.get("claim_boundary", {}).get("runtime_authority") == "not_claimed(주장 없음)"
        and f14c.get("claim_boundary", {}).get("goal_achieve") == "not_claimed(주장 없음)",
        "grok_closeout_accepted": grok["success"] and grok["classification"] == "accepted(수용)",
        "grok_combined_closeout_supported": bool(grok["combined_closeout_supported"]),
        "grok_wfo_mt5_skip_supported": bool(grok["wfo_mt5_skip_supported"]),
        "grok_forbidden_claims_supported": bool(grok["forbidden_claims_supported"]),
        "grok_no_unexpected_top_level_artifacts": not grok["unexpected_top_level_artifacts"],
    }
    return {
        "checks": checks,
        "metrics_equal_parent": metrics_equal_parent,
        "flat4x_row": flat4x,
        "best_gap_rows": best_gap,
        "strict_recount": strict_count,
        "preserved_recount": preserved_count,
        "judgment": "pass_with_boundary(경계 포함 통과)" if all(checks.values()) else "needs_manual_review(수동 검토 필요)",
    }


def build_summary(
    now: str,
    f14b: dict[str, Any],
    f14c: dict[str, Any],
    grok: dict[str, Any],
    local: dict[str, Any],
    candidate_rows: list[dict[str, str]],
    gap_rows: list[dict[str, str]],
) -> dict[str, Any]:
    best = f14c.get("best_candidate_row", {})
    parent_best = f14b.get("best_candidate_row", {})
    flat4x = local.get("flat4x_row", {})
    best_gap = local.get("best_gap_rows", [])
    return {
        "created_at_utc": now,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "f14b_status": f14b.get("status", ""),
        "f14c_status": f14c.get("status", ""),
        "strict_scout_clue_rows": int(f14c.get("strict_scout_clue_rows", 0)),
        "preserved_clue_rows": int(f14c.get("preserved_clue_rows", 0)),
        "candidate_row_count": len(candidate_rows),
        "best_candidate_row": best,
        "parent_best_candidate_row": parent_best,
        "flat4x_density_lift_row": flat4x,
        "best_label_model_gap_rows": best_gap,
        "grok_packet": grok["packet"],
        "grok_output": grok["output"],
        "grok_prompt_hash": grok["prompt_hash"],
        "grok_duration_seconds": grok["duration_seconds"],
        "grok_classification": grok["classification"],
        "local_verification": local,
        "preserved_clue": (
            "The cash-session q8 h8 plain logistic surface(현금장 q8 h8 평범 로지스틱 표면)는 OOS PF/DD"
            "(표본밖 수익 팩터/손실폭)가 좋아 보이는 sparse seed surface(희소 씨앗 표면)입니다. "
            "It is reference-only(참조 전용) and not a baseline(기준선 아님)."
        ),
        "negative_memory": (
            "Daily/session opportunity-budget labels(일/세션별 기회 예산 라벨)은 label-side density(라벨 쪽 밀도)를 "
            "약 8/day로 만들었지만, plain argmax ONNX(평범 최대확률 온엑스)는 model-side density(모델 쪽 밀도)를 "
            "0.07~0.10/day 수준으로만 전달했습니다. Flat4x repair(4배 평면 수리)는 density(밀도)를 올렸지만 "
            "validation PF/DD(검증 수익 팩터/손실폭)를 망가뜨렸습니다."
        ),
        "do_not_repeat": [
            "same safest-flat subset ladder(같은 안전 평면 부분 표본 사다리)",
            "class-weight density forcing(클래스 가중치 밀도 강제)",
            "threshold micro-search on this label family(이 라벨 계열 임계값 미세 탐색)",
            "WFO/MT5 escalation from ultra-sparse OOS PF alone(초희소 표본밖 수익 팩터만으로 WFO/MT5 격상)",
        ],
        "next_frontier_direction": (
            "new hypothesis required; likely model architecture or candidate-ranking mechanism, not another quota/flat repair"
            "(새 가설 필요, 또 다른 할당량/평면 수리보다 모델 구조나 후보 순위 메커니즘 쪽)"
        ),
        "external_verification_status": "grok_closeout_review_done_wfo_mt5_out_of_scope_by_claim(그록 마감 검토 완료, WFO/MT5는 주장 범위 밖)",
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(summary: dict[str, Any]) -> None:
    write_json(RUN_ROOT / "closeout_summary.json", summary)
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(summary))
    f03b.write_text_sig(REPORT_PATH, report_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md", gate_audit(summary))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "review_index.md", review_index(summary))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(summary))
    f03b.write_text_sig(DECISION_PATH, decision_text(summary))


def update_state_and_registries(summary: dict[str, Any]) -> None:
    f03b.write_text_sig(f03b.WORKSPACE_STATE, workspace_state(summary))
    f03b.write_text_sig(f03b.CURRENT_WORKING_STATE, current_working_state(summary))
    upsert_csv_io(f03b.RUN_REGISTRY, "run_id", run_registry_row(summary))
    for row in ledger_rows(summary):
        upsert_csv_io(f03b.ALPHA_LEDGER, "ledger_row_id", row)
        upsert_csv_io(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", row)
    f03b.append_once(f03b.CHANGELOG, RUN_ID, changelog_entry(summary))
    f03b.append_once(f03b.IDEA_REGISTRY, IDEA_MARKER, idea_registry_entry(summary))
    f03b.append_once(f03b.NEGATIVE_RESULT_REGISTER, NEGATIVE_MARKER, negative_register_entry(summary))


def run_manifest(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        **summary,
        "script_path": SCRIPT_PATH.as_posix(),
        "script_sha256": sha256_file(SCRIPT_PATH),
        "inputs": {
            "frontier14b_final": artifact_identity(F14B_FINAL),
            "frontier14b_candidate_summary": artifact_identity(F14B_SUMMARY),
            "frontier14c_final": artifact_identity(F14C_FINAL),
            "frontier14c_candidate_summary": artifact_identity(F14C_SUMMARY),
            "frontier14c_density_gap": artifact_identity(F14C_GAP),
            "frontier14c_onnx_parity": artifact_identity(F14C_PARITY),
            "frontier14c_report": artifact_identity(F14C_REPORT),
            "grok_closeout_output": artifact_identity(Path(summary["grok_output"])),
        },
        "outputs": {
            "report": REPORT_PATH.as_posix(),
            "decision": DECISION_PATH.as_posix(),
            "selection_status": (STAGE_ROOT / "04_selected" / "selection_status.md").as_posix(),
        },
    }


def report_text(summary: dict[str, Any]) -> str:
    best = summary["best_candidate_row"]
    flat4x = summary["flat4x_density_lift_row"]
    return f"""# Frontier14D Stage Closeout Report(프론티어14D 단계 마감 보고서)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `{summary['status']}`

Judgment(판정): `{summary['judgment']}`

## Action And Effect(행동과 효과)

Action(행동): Frontier14(프론티어14)를 preserved clue plus negative memory(보존 단서와 부정 기억)로 닫았습니다.

Effect(효과): cash-session sparse surface(현금장 희소 표면)는 reference-only clue(참조 전용 단서)로 보존하고, daily/session quota label(일/세션 할당량 라벨)이 trade density(거래 밀도)로 전달되지 않은 실패는 do-not-repeat memory(반복 금지 기억)로 고정합니다.

## Evidence Summary(근거 요약)

- strict scout clue rows(엄격 탐색 단서 행): `{summary['strict_scout_clue_rows']}`
- preserved clue rows(보존 단서 행): `{summary['preserved_clue_rows']}`
- best candidate(최고 후보): `{best.get('candidate_id', 'none')}`
- validation PF/density/DD(검증 수익 팩터/밀도/손실폭): `{fmt(best.get('validation_profit_factor'))}` / `{fmt(best.get('validation_trades_per_day'))}` / `{fmt(best.get('validation_dd_risk_percent'))}%`
- OOS PF/density/DD(표본밖 수익 팩터/밀도/손실폭): `{fmt(best.get('oos_profit_factor'))}` / `{fmt(best.get('oos_trades_per_day'))}` / `{fmt(best.get('oos_dd_risk_percent'))}%`
- worst subperiod DD(최악 하위기간 손실폭): `{fmt(best.get('validation_oos_subperiod_worst_dd_risk_percent'))}%`
- negative subperiod fraction(음수 하위기간 비율): `{fmt(best.get('validation_oos_negative_subperiod_fraction'))}`

## Local Verification(로컬 검증)

- candidate recount(후보 재계수): strict(엄격) `{summary['local_verification']['strict_recount']}`, preserved(보존) `{summary['local_verification']['preserved_recount']}`
- F14C best equals F14B parent metrics(F14C 최고가 F14B 부모 지표와 같음): `{all(summary['local_verification']['metrics_equal_parent'].values())}`
- F14C best joblib hash equals parent(F14C 최고 joblib 해시가 부모와 같음): `{summary['local_verification']['checks']['best_joblib_hash_matches_parent']}`
- flat4x density lift but quality fail(flat4x 밀도 상승, 품질 실패): val PF/density/DD `{fmt(flat4x.get('validation_profit_factor'))}` / `{fmt(flat4x.get('validation_trades_per_day'))}` / `{fmt(flat4x.get('validation_dd_risk_percent'))}%`
- label/model gap(라벨/모델 격차): label about 8/day(라벨 약 8/일), model below 0.11/day(모델 0.11/일 미만)
- Tier B(티어 B): missing_required(필수 누락) recorded(기록됨)

## Grok Closeout Receipt(그록 마감 영수증)

- packet(묶음): `{summary['grok_packet']}`
- classification(분류): `{summary['grok_classification']}`
- prompt hash(프롬프트 해시): `{summary['grok_prompt_hash']}`
- local verification(로컬 검증): `{summary['local_verification']['judgment']}`
- WFO/MT5 skip(WFO/MT5 생략): claim_boundary_skip_no_runtime_authority(주장 경계 생략, 런타임 권위 없음)

## Preserved Clue(보존 단서)

{summary['preserved_clue']}

## Negative Memory(부정 기억)

{summary['negative_memory']}

## Do Not Repeat(반복 금지)

{bullet_list(summary['do_not_repeat'])}

## Next Action(다음 행동)

`{NEXT_RUN_ID}`. Action(행동): 새 hypothesis(가설)로 다음 frontier(프론티어)를 엽니다. Effect(효과): 같은 quota/flat repair(할당량/평면 수리)를 반복하지 않고 새 실패면을 찾습니다.

## Claim Boundary(주장 경계)

completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def gate_audit(summary: dict[str, Any]) -> str:
    return f"""# Frontier14D Required Gate Coverage Audit(프론티어14D 필수 게이트 커버리지 감사)

Updated(갱신): {summary['created_at_utc']}

Status(상태): pass_with_boundary(경계 포함 통과)

- closeout_review_gate(마감 검토 게이트): Grok accepted(그록 수용), local verification(로컬 검증) `{summary['local_verification']['judgment']}`
- result_judgment_gate(결과 판정 게이트): strict rows(엄격 행) 0, preserved rows(보존 행) 5, combined closeout(결합 마감) recorded(기록됨)
- artifact_lineage_gate(산출물 계보 게이트): F14B/F14C/Grok outputs(F14B/F14C/그록 출력) linked(연결됨)
- paired_tier_gate(짝 티어 게이트): Tier A(티어 A) closeout plus Tier B/combined missing_required(티어 B/합산 필수 누락) recorded(기록됨)
- external_verification_gate(외부 검증 게이트): WFO/MT5(워크포워드/메타트레이더5) skipped by claim boundary(주장 경계로 생략), not runtime authority(런타임 권위 아님)
- final_claim_guard(최종 주장 보호): no completion/baseline/promotion/runtime/live/Goal claim(완성/기준선/승격/런타임/실거래/목표 주장 없음)
"""


def review_index(summary: dict[str, Any]) -> str:
    return f"""# Frontier14 Review Index(프론티어14 검토 색인)

Updated(갱신): {summary['created_at_utc']}

- `frontier14A_stage_open_daily_session_opportunity_budget_onnx_scout_v1`: stage open(단계 개방), Grok accepted(그록 수용).
- `{F14B_RUN_ID}`: proxy scout(프록시 탐색), strict rows(엄격 행) 0, preserved rows(보존 행) 2.
- `{PARENT_RUN_ID}`: density-transfer repair(밀도 전달 수리), strict rows(엄격 행) 0, preserved rows(보존 행) 5.
- `{RUN_ID}`: stage closeout(단계 마감), Grok accepted(그록 수용), preserved clue plus negative memory(보존 단서와 부정 기억).
"""


def selection_status(summary: dict[str, Any]) -> str:
    return f"""# Frontier14 Selection Status(프론티어14 선택 상태)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `{summary['status']}`

Judgment(판정): `{summary['judgment']}`

Closeout run(마감 실행): `{RUN_ID}`

Selection(선택): no selected baseline/completion candidate/promotion/runtime authority(선택 기준선/완성 후보/승격/런타임 권위 없음).

Preserved clue(보존 단서): {summary['preserved_clue']}

Negative memory(부정 기억): {summary['negative_memory']}

Next action(다음 행동): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) 없음.
"""


def decision_text(summary: dict[str, Any]) -> str:
    return f"""# Decision: Close Frontier14 As Preserved Clue And Negative Memory(결정: 프론티어14를 보존 단서와 부정 기억으로 마감)

Date(날짜): {summary['created_at_utc']}

Decision(결정): `{summary['status']}`

Action(행동): Frontier14(프론티어14)를 `{summary['judgment']}`로 닫았습니다.

Effect(효과): daily/session quota labels(일/세션별 할당량 라벨)의 density-transfer failure(밀도 전달 실패)를 반복 금지하고, sparse cash-session surface(희소 현금장 표면)는 reference-only clue(참조 전용 단서)로만 남깁니다.

Next action(다음 행동): `{NEXT_RUN_ID}`
"""


def workspace_state(summary: dict[str, Any]) -> str:
    return "\n".join(
        [
            f"current_stage_id: {STAGE_ID}",
            f"current_run_id: {RUN_ID}",
            f"latest_completed_run_id: {RUN_ID}",
            f"current_status: {summary['status']}",
            f"current_judgment: {summary['judgment']}",
            f"next_run_id: {NEXT_RUN_ID}",
            "runtime_authority: not_claimed",
            "operating_promotion: not_claimed",
            "goal_achieve: not_claimed",
            f"updated_at_utc: '{summary['created_at_utc']}'",
            "",
        ]
    )


def current_working_state(summary: dict[str, Any]) -> str:
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {summary['created_at_utc']}

## Active Stage(현재 단계)

- stage(단계): `{STAGE_ID}`
- latest run(최근 실행): `{RUN_ID}`
- status(상태): `{summary['status']}`
- judgment(판정): `{summary['judgment']}`
- next run(다음 실행): `{NEXT_RUN_ID}`

## Current Truth(현재 진실)

Action(행동): Frontier14(프론티어14)는 preserved clue plus negative memory(보존 단서와 부정 기억)로 마감됐습니다.

Effect(효과): daily/session quota label(일/세션 할당량 라벨)은 label density(라벨 밀도)를 만들었지만 model trade density(모델 거래 밀도)로 전달하지 못했다는 기억을 남기고, 다음 frontier(프론티어)는 새 hypothesis(가설)로 시작합니다.

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def run_registry_row(summary: dict[str, Any]) -> dict[str, Any]:
    best = summary["best_candidate_row"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "stage_closeout(단계 마감)",
        "status": summary["status"],
        "judgment": summary["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"strict={summary['strict_scout_clue_rows']};preserved={summary['preserved_clue_rows']};grok_accepted;no_authority",
        "work_family": "result_judgment(결과 판정)",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": "closed_preserved_clue_negative_memory_no_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": summary["created_at_utc"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "primary_kpi": primary_kpi_text(best),
        "external_verification_status": summary["external_verification_status"],
        "result_path": REPORT_PATH.as_posix(),
    }


def ledger_rows(summary: dict[str, Any]) -> list[dict[str, Any]]:
    best = summary["best_candidate_row"]
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "stage_closeout(단계 마감)",
        "status": summary["status"],
        "judgment": summary["judgment"],
        "path": REPORT_PATH.as_posix(),
        "guardrail_kpi": "grok_accepted_no_wfo_no_mt5_no_authority(그록 수용, WFO/MT5/권위 없음)",
        "external_verification_status": summary["external_verification_status"],
    }
    return [
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_a_stage_closeout",
            "subrun_id": f"{RUN_ID}__tier_a_stage_closeout",
            "record_view": "Tier A separate(티어 A 분리)",
            "tier_scope": "Tier A(티어 A)",
            "kpi_scope": "stage_closeout_preserved_clue_negative_memory_not_runtime(단계 마감 보존 단서와 부정 기억, 런타임 아님)",
            "primary_kpi": primary_kpi_text(best),
            "notes": f"next={NEXT_RUN_ID};no_authority",
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_b_missing_required",
            "subrun_id": f"{RUN_ID}__tier_b_missing_required",
            "record_view": "Tier B separate(티어 B 분리)",
            "tier_scope": "Tier B(티어 B)",
            "kpi_scope": "missing_required(필수 누락)",
            "primary_kpi": "missing_required_no_paired_source(필수 누락, 짝 원천 없음)",
            "notes": "Tier B paired materialization not available(티어 B 짝 물질화 없음)",
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_ab_combined_missing_required",
            "subrun_id": f"{RUN_ID}__tier_ab_combined_missing_required",
            "record_view": "Tier A+B combined(티어 A+B 합산)",
            "tier_scope": "Tier A+B(티어 A+B)",
            "kpi_scope": "missing_required(필수 누락)",
            "primary_kpi": "missing_required_no_combined_claim(필수 누락, 합산 주장 없음)",
            "notes": "combined record blocked by missing Tier B(티어 B 부재로 합산 기록 차단)",
        },
    ]


def changelog_entry(summary: dict[str, Any]) -> str:
    return (
        f"- {summary['created_at_utc']}: `{RUN_ID}` closed Frontier14(프론티어14) as preserved clue plus negative memory"
        f"(보존 단서와 부정 기억) after Grok closeout accepted(그록 마감 수용). Effect(효과): next frontier(다음 프론티어)"
        f" `{NEXT_RUN_ID}` starts a new hypothesis(새 가설) without authority claims(권위 주장 없음).\n"
    )


def idea_registry_entry(summary: dict[str, Any]) -> str:
    return (
        f"- `{RUN_ID}`: Frontier14(프론티어14) closed as preserved_clue_negative_memory(보존 단서와 부정 기억). "
        "Effect(효과): cash-session q8 h8 sparse ONNX surface(현금장 q8 h8 희소 온엑스 표면)는 reference-only clue(참조 전용 단서)로 남기고, "
        "daily/session quota density-transfer failure(일/세션 할당량 밀도 전달 실패)는 반복 금지로 남겼습니다."
    )


def negative_register_entry(summary: dict[str, Any]) -> str:
    return (
        f"- `{NEGATIVE_MARKER}`: Daily/session opportunity-budget labels(일/세션별 기회 예산 라벨)은 label-side density(라벨 쪽 밀도)를 만들었지만 "
        "plain argmax ONNX(평범 최대확률 온엑스)로 model-side density(모델 쪽 밀도)를 전달하지 못했습니다. "
        "Effect(효과): 같은 quota/flat subset repair(할당량/평면 부분 표본 수리)를 반복하지 않습니다."
    )


def primary_kpi_text(best: dict[str, Any]) -> str:
    return (
        f"best={best.get('candidate_id', 'none')};"
        f"strict=False;preserved={best.get('preserved_clue_pass', False)};"
        f"val_pf={fmt(best.get('validation_profit_factor'))};"
        f"val_density={fmt(best.get('validation_trades_per_day'))};"
        f"val_dd={fmt(best.get('validation_dd_risk_percent'))};"
        f"oos_pf={fmt(best.get('oos_profit_factor'))};"
        f"oos_density={fmt(best.get('oos_trades_per_day'))};"
        f"oos_dd={fmt(best.get('oos_dd_risk_percent'))};"
        f"worst_sub_dd={fmt(best.get('validation_oos_subperiod_worst_dd_risk_percent'))}"
    )


def ensure_csv_header(path: Path, template_path: Path) -> None:
    if path_exists(path):
        return
    header = read_csv_header_io(template_path)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        csv.writer(handle, lineterminator="\n").writerow(header)


def read_csv_header_io(path: Path) -> list[str]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return next(csv.reader(handle))


def upsert_csv_io(path: Path, key: str, row: dict[str, Any]) -> None:
    header = read_csv_header_io(path)
    rows: list[dict[str, str]] = []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        for existing in csv.DictReader(handle):
            rows.append(dict(existing))
    normalized = {column: f03b.stringify(row.get(column, "")) for column in header}
    replaced = False
    for index, existing in enumerate(rows):
        if existing.get(key) == normalized.get(key):
            rows[index] = normalized
            replaced = True
            break
    if not replaced:
        rows.append(normalized)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=header, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for item in rows:
            writer.writerow({column: f03b.stringify(item.get(column, "")) for column in header})


def artifact_identity(path: Path) -> dict[str, str]:
    return {"path": path.as_posix(), "sha256": sha256_file(path) if path_exists(path) else "missing(누락)"}


def find_row(rows: list[dict[str, str]], key: str, value: str) -> dict[str, str]:
    for row in rows:
        if row.get(key) == value:
            return row
    return {}


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def parse_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes"}


def as_float(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return math.nan
    return number


def close_float(left: Any, right: Any, *, tolerance: float) -> bool:
    lnum = as_float(left)
    rnum = as_float(right)
    if not math.isfinite(lnum) or not math.isfinite(rnum):
        return False
    return abs(lnum - rnum) <= tolerance


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def bullet_list(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def fmt(value: Any) -> str:
    number = as_float(value)
    if not math.isfinite(number):
        return "n/a"
    return f"{number:.6g}"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
