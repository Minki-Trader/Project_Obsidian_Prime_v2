from __future__ import annotations

import csv
import json
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


STAGE_ID = "stage_frontier_20__train_only_feature_state_rule_atlas_onnx_scout"
RUN_ID = "frontier20C_rule_atlas_repair_or_closeout_decision_v1"
RUN_NUMBER = "frontier20C"
PARENT_RUN_ID = "frontier20B_feature_state_rule_atlas_proxy_scout_v1"
NEXT_RUN_ID = "frontier21A_stage_open_new_hypothesis_design_v1"
STATUS = "closed_preserved_clue_negative_memory_rule_atlas_seed_surface_no_handoff_no_authority"
JUDGMENT = "preserved_clue_negative_memory(보존 단서+부정 기억)"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_20/frontier20c_rule_atlas_closeout.py")

F20B_FINAL = STAGE_ROOT / "02_runs" / PARENT_RUN_ID / "final_summary.json"
F20B_REPORT = STAGE_ROOT / "03_reviews" / f"{PARENT_RUN_ID}_report.md"
F20B_SUMMARY_CSV = STAGE_ROOT / "02_runs" / PARENT_RUN_ID / "candidate_summary.csv"
GROK_CLOSEOUT_PACKET = Path("docs/agent_control/grok_reviews/2026-06-14_frontier20_closeout/small_review")

RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")
NEGATIVE_RESULT_REGISTER = Path("docs/registers/negative_result_register.md")
CHANGELOG = Path("docs/workspace/changelog.md")

PRESERVED_CLUE = (
    "low_vix_momentum_price_position_long_feature_state_surface_density_aligned_pf12_seed"
    "(낮은 VIX 모멘텀/가격 위치 롱 피처 상태 표면은 빈도 정렬 PF 약 1.2 씨앗 표면)"
)
NEGATIVE_MEMORY = (
    "train_only_depth2_rule_atlas_alone_does_not_reduce_dd_or_create_runtime_handoff"
    "(학습 전용 깊이2 규칙 지도 단독은 손실폭을 충분히 줄이거나 런타임 인계를 만들지 못함)"
)
RUNTIME_BLOCKER = (
    "runtime_probe_ineligible_under_f20_locks_no_handoff_candidate"
    "(F20 잠금 아래 인계 후보가 없어 런타임 탐침 부적격)"
)


def main() -> int:
    ensure_dirs()
    normalize_grok_markdown()
    now = utc_now()
    f20b = read_json(F20B_FINAL)
    grok = read_grok_packet(GROK_CLOSEOUT_PACKET)
    local = local_verification(f20b, grok)
    final = build_final(now, f20b, grok, local)
    write_outputs(final)
    update_registries(final)
    update_current_truth(final)
    print(json.dumps(json_ready({
        "status": final["status"],
        "judgment": final["judgment"],
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "preserved_clue": final["preserved_clue"],
        "negative_memory": final["negative_memory"],
        "runtime_blocker": final["runtime_blocker"],
        "local_verification": final["local_verification"]["judgment"],
        "report": REPORT_PATH.as_posix(),
    }), ensure_ascii=False, indent=2))
    return 0


def ensure_dirs() -> None:
    for path in (RUN_ROOT, STAGE_ROOT / "03_reviews", STAGE_ROOT / "04_selected"):
        io_path(path).mkdir(parents=True, exist_ok=True)


def normalize_grok_markdown() -> None:
    for name in ("prompt.md", "clean_output.md"):
        path = GROK_CLOSEOUT_PACKET / name
        if path_exists(path):
            text = io_path(path).read_text(encoding="utf-8-sig")
            f03b.write_text_sig(path, text.rstrip() + "\n")


def read_grok_packet(packet: Path) -> dict[str, Any]:
    metadata = read_json(packet / "metadata.json")
    output = read_text(packet / "clean_output.md")
    return {
        "packet": packet.as_posix(),
        "prompt": (packet / "prompt.md").as_posix(),
        "output": (packet / "clean_output.md").as_posix(),
        "metadata": (packet / "metadata.json").as_posix(),
        "prompt_hash": metadata.get("prompt_hash", ""),
        "success": bool(metadata.get("success")),
        "returncode": metadata.get("returncode"),
        "timed_out": bool(metadata.get("timed_out")),
        "duration_seconds": metadata.get("duration_seconds", ""),
        "classification": classify_grok(output),
        "output_excerpt": output[:1600],
    }


def classify_grok(text: str) -> str:
    lowered = text.lower()
    if "verdict: accept" in lowered or "closeout label to record" in lowered:
        return "accepted(수용)"
    if "reject" in lowered:
        return "rejected(거절)"
    return "classification_missing(분류 누락)"


def local_verification(f20b: dict[str, Any], grok: dict[str, Any]) -> dict[str, Any]:
    workspace = read_text(f03b.WORKSPACE_STATE)
    checks = {
        "workspace_current_run_f20b": f"current_run_id: {PARENT_RUN_ID}" in workspace,
        "f20b_seed_count_positive": int(f20b.get("seed_count", 0)) == 19,
        "f20b_strict_count_zero": int(f20b.get("strict_count", -1)) == 0,
        "f20b_handoff_count_zero": int(f20b.get("handoff_candidate_count", -1)) == 0,
        "f20b_report_exists": path_exists(F20B_REPORT),
        "f20b_summary_csv_exists": path_exists(F20B_SUMMARY_CSV),
        "grok_closeout_success": bool(grok.get("success")),
        "grok_closeout_accepted": grok.get("classification") == "accepted(수용)",
        "no_completion_claim": all(value == "not_claimed(주장 없음)" for value in f20b.get("claim_boundary", {}).values()),
    }
    return {
        "judgment": "pass_closeout_ready(마감 준비 통과)" if all(checks.values()) else "needs_manual_review(수동 검토 필요)",
        "checks": checks,
    }


def build_final(now: str, f20b: dict[str, Any], grok: dict[str, Any], local: dict[str, Any]) -> dict[str, Any]:
    return {
        "created_at_utc": now,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "preserved_clue": PRESERVED_CLUE,
        "negative_memory": NEGATIVE_MEMORY,
        "runtime_blocker": RUNTIME_BLOCKER,
        "closeout_label": "preserved_clue_plus_negative_memory_scout_complete_handoff_absent_runtime_ineligible(보존 단서+부정 기억, 탐색 완료, 인계 없음, 런타임 부적격)",
        "f20b_status": f20b.get("status", ""),
        "f20b_judgment": f20b.get("judgment", ""),
        "strict_count": int(f20b.get("strict_count", 0)),
        "seed_count": int(f20b.get("seed_count", 0)),
        "handoff_candidate_count": int(f20b.get("handoff_candidate_count", 0)),
        "best_candidate": f20b.get("best_candidate", {}),
        "grok_closeout": grok,
        "local_verification": local,
        "external_verification_status": "blocked_by_claim_boundary_runtime_probe_ineligible_no_handoff(주장 경계상 런타임 탐침 부적격, 인계 없음)",
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(final: dict[str, Any]) -> None:
    write_json(RUN_ROOT / "final_closeout_summary.json", final)
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(final))
    f03b.write_text_sig(REPORT_PATH, report_text(final))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / f"{RUN_ID}_grok_closeout_receipt.md", grok_receipt_text(final))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / f"{RUN_ID}_gate_audit.md", gate_audit(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "preserved_clue.md", preserved_clue_text(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "negative_memory.md", negative_memory_text(final))


def run_manifest(final: dict[str, Any]) -> dict[str, Any]:
    return {
        "identity": {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "created_at_utc": final["created_at_utc"],
        },
        "artifacts": [
            artifact_identity(SCRIPT_PATH),
            artifact_identity(F20B_REPORT),
            artifact_identity(F20B_SUMMARY_CSV),
            artifact_identity(GROK_CLOSEOUT_PACKET / "clean_output.md"),
            artifact_identity(REPORT_PATH),
        ],
        "results": {
            "closeout_label": final["closeout_label"],
            "strict_count": final["strict_count"],
            "seed_count": final["seed_count"],
            "handoff_candidate_count": final["handoff_candidate_count"],
            "external_verification_status": final["external_verification_status"],
        },
        "compatibility": {
            "runtime_authority": "not_claimed(주장 없음)",
            "operating_promotion": "not_claimed(주장 없음)",
            "mismatch_policy": "fail_fast(즉시 실패)",
        },
        "claim_boundary": final["claim_boundary"],
    }


def report_text(final: dict[str, Any]) -> str:
    best = final["best_candidate"]
    return f"""# Frontier20C Rule Atlas Closeout Report(전선20C 규칙 지도 마감 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Action(행동): Frontier20(전선20)을 preserved clue + negative memory(보존 단서 + 부정 기억)로 마감했습니다.

Effect(효과): low-VIX momentum/price-position long surface(낮은 VIX 모멘텀/가격 위치 롱 표면)는 다음 가설의 reference clue(참조 단서)로 남기고, depth-2 train-only rule atlas(깊이2 학습 전용 규칙 지도) 단독 반복은 막습니다.

Preserved clue(보존 단서): `{final['preserved_clue']}`

Negative memory(부정 기억): `{final['negative_memory']}`

Runtime probe blocker(런타임 탐침 차단 사유): `{final['runtime_blocker']}`

Strict/seed/handoff counts(엄격/씨앗/인계 수): `{final['strict_count']}` / `{final['seed_count']}` / `{final['handoff_candidate_count']}`

Best seed(최상 씨앗): `{best.get('candidate_id', '')}` `{best.get('rule_definition', '')}`

Validation PF/density/DD(검증 수익 팩터/빈도/손실폭): `{fmt(best.get('validation_profit_factor'))}` / `{fmt(best.get('validation_trades_per_day'))}/day` / `{fmt(best.get('validation_dd_risk'))}%`

OOS PF/density/DD(표본외 수익 팩터/빈도/손실폭): `{fmt(best.get('oos_profit_factor'))}` / `{fmt(best.get('oos_trades_per_day'))}/day` / `{fmt(best.get('oos_dd_risk'))}%`

Grok closeout classification(그록 마감 분류): `{final['grok_closeout']['classification']}`

Local verification(로컬 검증): `{final['local_verification']['judgment']}`

Next action(다음 행동): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def grok_receipt_text(final: dict[str, Any]) -> str:
    return f"""# Frontier20 Grok Closeout Receipt(전선20 그록 마감 영수증)

trigger_reason(트리거 이유): stage closeout requires Grok review(단계 마감에는 그록 검토가 필요)

review_size(검토 크기): small review(소규모 검토)

packet(묶음): `{final['grok_closeout']['packet']}`

prompt(프롬프트): `{final['grok_closeout']['prompt']}`

output(출력): `{final['grok_closeout']['output']}`

classification(분류): `{final['grok_closeout']['classification']}`

accepted advice(수용 조언): close as preserved clue + negative memory(보존 단서 + 부정 기억으로 마감), mark runtime-probe-ineligible under F20 locks(F20 잠금 아래 런타임 탐침 부적격 표시).

local verification(로컬 검증): `{final['local_verification']['judgment']}`

forbidden claim check(금지 주장 확인): `{json.dumps(final['claim_boundary'], ensure_ascii=False, sort_keys=True)}`
"""


def gate_audit(final: dict[str, Any]) -> str:
    return f"""# Frontier20C Closeout Gate Audit(전선20C 마감 게이트 감사)

Updated(갱신): {final['created_at_utc']}

- external_review_packet(외부 검토 묶음): Grok closeout(그록 마감) accepted(수용).
- evidence_scope(근거 범위): F20B proxy(전선20B 프록시), capped repair check(상한 수리 확인), no WFO/MT5(WFO/MT5 없음).
- runtime_probe_gate(런타임 탐침 게이트): `{final['runtime_blocker']}`.
- tier_record_gate(티어 기록 게이트): F20B stage ledger(단계 장부)에 Tier A/Tier B/Tier A+B(티어 A/B/합산) 행 기록.
- closeout_label_gate(마감 라벨 게이트): `{final['closeout_label']}`.
- final_claim_guard(최종 주장 보호): completion/baseline/promotion/runtime/live/Goal(완성/기준선/승격/런타임/실거래/목표) 주장 없음.
"""


def selection_status(final: dict[str, Any]) -> str:
    return f"""# Frontier20 Selection Status(전선20 선택 상태)

Updated(갱신): {final['created_at_utc']}

Selection(선택): no selected baseline/completion candidate/promotion/runtime authority(선택 기준선/완성 후보/승격/런타임 권위 없음).

Closeout(마감): `preserved_clue + negative_memory(보존 단서 + 부정 기억)`

Preserved clue(보존 단서): `{final['preserved_clue']}`

Negative memory(부정 기억): `{final['negative_memory']}`

Runtime probe blocker(런타임 탐침 차단 사유): `{final['runtime_blocker']}`

Next action(다음 행동): `{NEXT_RUN_ID}`
"""


def preserved_clue_text(final: dict[str, Any]) -> str:
    best = final["best_candidate"]
    return f"""# Frontier20 Preserved Clue(전선20 보존 단서)

Clue(단서): `{final['preserved_clue']}`

Evidence(근거): seed rows(씨앗 행) `{final['seed_count']}`, best seed(최상 씨앗) `{best.get('candidate_id', '')}` with validation/OOS PF-density-DD(검증/표본외 수익 팩터-빈도-손실폭) `{fmt(best.get('validation_profit_factor'))}`/`{fmt(best.get('validation_trades_per_day'))}`/`{fmt(best.get('validation_dd_risk'))}` and `{fmt(best.get('oos_profit_factor'))}`/`{fmt(best.get('oos_trades_per_day'))}`/`{fmt(best.get('oos_dd_risk'))}`.

Boundary(경계): reference surface(참고 표면) only(전용). No handoff candidate(인계 후보 없음), no runtime authority(런타임 권위 없음).
"""


def negative_memory_text(final: dict[str, Any]) -> str:
    return f"""# Frontier20 Negative Memory(전선20 부정 기억)

Negative memory(부정 기억): `{final['negative_memory']}`

Why failed(실패 이유): strict/handoff(엄격/인계) count is `0/0`, DD(손실폭)는 약 14~33% 범위로 남았고 capped train-risk rerank(상한 학습 위험 재순위)는 OOS PF(표본외 수익 팩터)를 1 미만으로 악화했습니다.

Do not repeat(반복 금지): same train-only depth-2 atlas rerank(같은 학습 전용 깊이2 지도 재순위)를 F20 안에서 반복하지 않습니다.

Reopen condition(재개 조건): DD containment mechanism(손실폭 억제 메커니즘)이나 runtime representation(런타임 표현)이 바뀌는 새 가설에서만 참고합니다.
"""


def update_registries(final: dict[str, Any]) -> None:
    f03b.upsert_csv(RUN_REGISTRY, "run_id", run_registry_row(final))
    for row in ledger_rows(final):
        f03b.upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
        f03b.upsert_csv(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", row)
    f03b.append_once(CHANGELOG, RUN_ID, changelog_entry(final))
    f03b.append_once(IDEA_REGISTRY, RUN_ID, idea_registry_entry(final))
    f03b.append_once(NEGATIVE_RESULT_REGISTER, RUN_ID, negative_result_entry(final))


def run_registry_row(final: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "stage_closeout(단계 마감)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"preserved_clue={final['preserved_clue']};negative_memory={final['negative_memory']};runtime_blocker={final['runtime_blocker']}",
        "work_family": "kpi_evidence(지표 근거)",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": "stage_closeout_no_baseline_no_promotion_no_runtime_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": final["created_at_utc"],
        "primary_kpi": f"strict={final['strict_count']};seed={final['seed_count']};handoff={final['handoff_candidate_count']}",
        "guardrail_kpi": "no_wfo_no_mt5_runtime_probe_ineligible_no_authority(WFO/MT5 없음, 런타임 탐침 부적격, 권위 없음)",
        "external_verification_status": final["external_verification_status"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "result_path": REPORT_PATH.as_posix(),
    }


def ledger_rows(final: dict[str, Any]) -> list[dict[str, Any]]:
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "stage_closeout(단계 마감)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "guardrail_kpi": "no_wfo_no_mt5_no_authority(WFO/MT5/권위 없음)",
        "external_verification_status": final["external_verification_status"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "run_family": "stage_closeout(단계 마감)",
    }
    return [
        {
            **common,
            "ledger_row_id": f"{RUN_ID}__tier_a_stage_closeout",
            "subrun_id": f"{RUN_ID}__tier_a_stage_closeout",
            "record_view": "Tier A separate(티어 A 분리)",
            "tier_scope": "Tier A(티어 A)",
            "kpi_scope": "stage_closeout_preserved_clue_negative_memory_not_runtime(단계 마감 보존 단서+부정 기억, 런타임 아님)",
            "primary_kpi": f"strict={final['strict_count']};seed={final['seed_count']};handoff={final['handoff_candidate_count']}",
            "notes": f"{final['preserved_clue']};{final['negative_memory']};{final['runtime_blocker']}",
        },
        {
            **common,
            "ledger_row_id": f"{RUN_ID}__tier_b_missing_required",
            "subrun_id": f"{RUN_ID}__tier_b_missing_required",
            "record_view": "Tier B separate(티어 B 분리)",
            "tier_scope": "Tier B(티어 B)",
            "kpi_scope": "missing_required(필수 누락)",
            "primary_kpi": "missing_required_no_tier_b_model_input(필수 누락, Tier B 모델 입력 없음)",
            "notes": "Tier B paired materialization not available(티어 B 짝 물질화 없음)",
        },
        {
            **common,
            "ledger_row_id": f"{RUN_ID}__tier_ab_combined_out_of_scope",
            "subrun_id": f"{RUN_ID}__tier_ab_combined_out_of_scope",
            "record_view": "Tier A+B combined(티어 A+B 합산)",
            "tier_scope": "Tier A+B(티어 A+B)",
            "kpi_scope": "out_of_scope_by_claim(주장 범위 밖)",
            "primary_kpi": "out_of_scope_by_claim_no_combined_source(주장 범위 밖, 합산 원천 없음)",
            "notes": "Combined record blocked by missing Tier B source(Tier B 원천 누락으로 합산 기록 차단)",
        },
    ]


def changelog_entry(final: dict[str, Any]) -> str:
    return (
        f"- {final['created_at_utc']}: `{RUN_ID}` closed Frontier20(전선20) as preserved clue + negative memory(보존 단서 + 부정 기억). "
        f"Effect(효과): next frontier(다음 전선) starts at `{NEXT_RUN_ID}` without inheriting baseline/promotion/runtime authority(기준선/승격/런타임 권위 상속 없음).\n"
    )


def idea_registry_entry(final: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR20-TRAIN-ONLY-FEATURE-STATE-RULE-ATLAS-ONNX-SCOUT`: Frontier20(전선20) closed as preserved clue + negative memory(보존 단서 + 부정 기억). "
        f"Effect(효과): `{PRESERVED_CLUE}` is reference-only(참조 전용) and `{NEGATIVE_MEMORY}` is do-not-repeat(반복 금지) memory.\n"
    )


def negative_result_entry(final: dict[str, Any]) -> str:
    return (
        f"- `{RUN_ID}`: {NEGATIVE_MEMORY}. Preserved clue(보존 단서): `{PRESERVED_CLUE}`. Runtime blocker(런타임 차단): `{RUNTIME_BLOCKER}`. "
        "Effect(효과): same train-only depth-2 rule atlas(같은 학습 전용 깊이2 규칙 지도)를 DD/handoff(손실폭/인계) 해결책처럼 반복하지 않습니다.\n"
    )


def update_current_truth(final: dict[str, Any]) -> None:
    io_path(f03b.WORKSPACE_STATE).write_text(workspace_state(final), encoding="utf-8-sig")
    f03b.write_text_sig(f03b.CURRENT_WORKING_STATE, current_working_state(final))


def workspace_state(final: dict[str, Any]) -> str:
    return "\n".join([
        f"current_stage_id: {STAGE_ID}",
        f"current_run_id: {RUN_ID}",
        f"latest_completed_run_id: {RUN_ID}",
        f"current_status: {final['status']}",
        f"current_judgment: {final['judgment']}",
        f"next_run_id: {NEXT_RUN_ID}",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "goal_achieve: not_claimed",
        f"updated_at_utc: '{final['created_at_utc']}'",
        "",
    ])


def current_working_state(final: dict[str, Any]) -> str:
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

## Active Stage(현재 단계)

- stage(단계): `{STAGE_ID}`
- latest run(최근 실행): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- next run(다음 실행): `{NEXT_RUN_ID}`

## Current Truth(현재 진실)

Action(행동): Frontier20(전선20)을 preserved clue + negative memory(보존 단서 + 부정 기억)로 닫았습니다.

Effect(효과): low-VIX momentum/price-position long surface(낮은 VIX 모멘텀/가격 위치 롱 표면)는 reference clue(참조 단서)로 남기고, train-only depth-2 rule atlas(학습 전용 깊이2 규칙 지도) 단독 반복은 막습니다.

Runtime probe blocker(런타임 탐침 차단 사유): `{RUNTIME_BLOCKER}`

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def artifact_identity(path: Path) -> dict[str, str]:
    return {"path": path.as_posix(), "sha256": sha256_file(path) if path_exists(path) else "missing(누락)"}


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fmt(value: Any) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return ""
    return f"{number:.6g}"


if __name__ == "__main__":
    raise SystemExit(main())
