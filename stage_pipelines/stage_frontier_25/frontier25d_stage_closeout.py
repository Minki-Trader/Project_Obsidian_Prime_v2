from __future__ import annotations

import hashlib
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b
from stage_pipelines.stage_frontier_25 import frontier25b_bridge_archetype_preselection_proxy_scout as f25b
from stage_pipelines.stage_frontier_25 import frontier25c_bridge_archetype_repair_or_closeout_decision as f25c
from stage_pipelines.stage_frontier_25 import materialize_frontier25a_stage_open as f25a


STAGE_ID = f25a.STAGE_ID
RUN_ID = "frontier25D_stage_closeout_bridge_archetype_preselection_v1"
RUN_NUMBER = "frontier25D"
PARENT_RUN_ID = f25c.RUN_ID
STATUS = "closed_preserved_clue_negative_memory_bridge_archetype_preselection_scout_no_handoff"
JUDGMENT = "preserved_clue_negative_memory(보존 단서+부정 기억)"
NEXT_STAGE_ID = "stage_frontier_26__joint_micro_satisfaction_before_bridge_union_onnx_scout"
NEXT_RUN_ID = "frontier26A_stage_open_joint_micro_satisfaction_bridge_union_hypothesis_design_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
GROK_RECEIPT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_grok_closeout_receipt.md"
LOCAL_VERIFICATION_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_local_verification.md"
REQUIRED_GATE_AUDIT_PATH = STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md"
DECISION_PATH = Path("docs/decisions/2026-06-14_stage_frontier_25_bridge_archetype_preselection_onnx_scout_closeout.md")
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_25/frontier25d_stage_closeout.py")

F25A_SUMMARY = STAGE_ROOT / "02_runs" / f25a.RUN_ID / "stage_open_summary.json"
F25B_SUMMARY = STAGE_ROOT / "02_runs" / f25b.RUN_ID / "final_summary.json"
F25B_CANDIDATES = STAGE_ROOT / "02_runs" / f25b.RUN_ID / "archetype_candidate_summary.csv"
F25C_SUMMARY = STAGE_ROOT / "02_runs" / f25c.RUN_ID / "final_summary.json"
F25C_AUDIT = STAGE_ROOT / "02_runs" / f25c.RUN_ID / "repair_feasibility_audit.csv"

GROK_STAGE_OPEN_PACKET = Path("docs/agent_control/grok_reviews/2026-06-14_frontier25_stage_open/small_review")
GROK_CLOSEOUT_PACKET = Path("docs/agent_control/grok_reviews/2026-06-14_frontier25_stage_closeout/small_review")

RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")
CHANGELOG = Path("docs/workspace/changelog.md")
WORKSPACE_STATE = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE = Path("docs/context/current_working_state.md")

PRESERVED_CLUE = f25c.PRESERVED_CLUE
NEGATIVE_MEMORY = f25c.NEGATIVE_MEMORY
RUNTIME_PROBE_BLOCKER = (
    "runtime_probe_ineligible_no_handoff_candidate_after_f25c_repair_decision"
    "(F25C 수리 결정 뒤 인계 후보 없어 런타임 탐침 부적격)"
)
ONNX_BLOCKER = (
    "onnx_branch_unattempted_no_handoff_candidate_after_f25c_repair_decision"
    "(F25C 수리 결정 뒤 인계 후보 없어 ONNX 미시도)"
)
NEXT_HYPOTHESIS_CLUE = (
    "train_joint_micro_satisfaction_before_bridge_union_reference_only"
    "(학습 전용 미세 구간 합동 충족 뒤 연결 합집합 참조 단서)"
)


def main() -> int:
    ensure_dirs()
    created_at = utc_now()
    stage_open = read_json(F25A_SUMMARY)
    f25b_summary = read_json(F25B_SUMMARY)
    f25c_summary = read_json(F25C_SUMMARY)
    f25b_candidates = pd.read_csv(io_path(F25B_CANDIDATES))
    f25c_audit = pd.read_csv(io_path(F25C_AUDIT))
    grok = load_grok_closeout()
    local = validate_context(stage_open, f25b_summary, f25c_summary, f25b_candidates, f25c_audit, grok)
    final = build_final(created_at, stage_open, f25b_summary, f25c_summary, f25b_candidates, f25c_audit, grok, local)
    write_outputs(final)
    update_registries(final)
    update_current_truth(final)
    print(json.dumps(json_ready({
        "status": final["status"],
        "judgment": final["judgment"],
        "run_id": RUN_ID,
        "preserved_clue": final["preserved_clue"],
        "negative_memory": final["negative_memory"],
        "runtime_probe_blocker": final["runtime_probe_blocker"],
        "onnx_blocker": final["onnx_blocker"],
        "grok_classification": final["grok_closeout"]["classification"],
        "next_run_id": final["next_run_id"],
        "report": REPORT_PATH.as_posix(),
    }), ensure_ascii=False, indent=2))
    return 0


def ensure_dirs() -> None:
    for path in (RUN_ROOT, STAGE_ROOT / "03_reviews", STAGE_ROOT / "04_selected", DECISION_PATH.parent):
        io_path(path).mkdir(parents=True, exist_ok=True)


def load_grok_closeout() -> dict[str, Any]:
    meta_path = GROK_CLOSEOUT_PACKET / "metadata.json"
    output_path = GROK_CLOSEOUT_PACKET / "clean_output.md"
    prompt_path = GROK_CLOSEOUT_PACKET / "prompt.md"
    metadata = read_json(meta_path)
    clean_output = read_text(output_path)
    lower = clean_output.lower()
    accepted = "accepted" in lower and "out_of_scope_by_claim" in lower
    needs_local = "needs_local_verification" in lower or "frontier25d" in lower
    if accepted and needs_local:
        classification = "accepted_with_local_verification_completed(수용, 로컬 검증 완료)"
    elif accepted:
        classification = "accepted(수용)"
    else:
        classification = "needs_local_verification(로컬 검증 필요)"
    return {
        "packet": GROK_CLOSEOUT_PACKET.as_posix(),
        "prompt": prompt_path.as_posix(),
        "clean_output": output_path.as_posix(),
        "metadata": meta_path.as_posix(),
        "prompt_hash": metadata.get("prompt_hash", ""),
        "success": bool(metadata.get("success")),
        "returncode": metadata.get("returncode"),
        "timed_out": metadata.get("timed_out"),
        "classification": classification,
        "accepted": accepted,
        "needs_local_verification": needs_local,
        "output_excerpt": clean_output[:2000],
    }


def validate_context(
    stage_open: dict[str, Any],
    f25b_summary: dict[str, Any],
    f25c_summary: dict[str, Any],
    f25b_candidates: pd.DataFrame,
    f25c_audit: pd.DataFrame,
    grok: dict[str, Any],
) -> dict[str, Any]:
    workspace = read_text(WORKSPACE_STATE)
    checks = {
        "workspace_current_stage_frontier25": f"current_stage_id: {STAGE_ID}" in workspace,
        "workspace_next_or_current_frontier25d": f"next_run_id: {RUN_ID}" in workspace or f"current_run_id: {RUN_ID}" in workspace,
        "stage_open_parent_matches": stage_open.get("run_id") == f25a.RUN_ID,
        "f25b_zero_seed": int(f25b_summary.get("seed_surface_rows", -1)) == 0,
        "f25b_zero_handoff": int(f25b_summary.get("handoff_candidate_rows", -1)) == 0,
        "f25b_nonrepeat_top10": int(f25b_summary.get("top10_f24b_overlap_count", -1)) == 0,
        "f25c_parent_matches": f25c_summary.get("run_id") == PARENT_RUN_ID,
        "f25c_next_closeout_matches": f25c_summary.get("next_run_id") == RUN_ID,
        "f25c_preserved_matches": f25c_summary.get("preserved_clue") == PRESERVED_CLUE,
        "f25c_negative_matches": f25c_summary.get("negative_memory") == NEGATIVE_MEMORY,
        "f25b_candidate_table_present": not f25b_candidates.empty,
        "f25c_audit_present": not f25c_audit.empty,
        "grok_closeout_success": grok["success"] and grok["accepted"],
        "grok_stage_open_packet_present": path_exists(GROK_STAGE_OPEN_PACKET / "metadata.json"),
        "grok_closeout_packet_present": path_exists(GROK_CLOSEOUT_PACKET / "metadata.json"),
    }
    return {
        "checks": checks,
        "judgment": "pass_closeout_ready(마감 준비 통과)" if all(checks.values()) else "needs_manual_review(수동 검토 필요)",
    }


def build_final(
    created_at: str,
    stage_open: dict[str, Any],
    f25b_summary: dict[str, Any],
    f25c_summary: dict[str, Any],
    f25b_candidates: pd.DataFrame,
    f25c_audit: pd.DataFrame,
    grok: dict[str, Any],
    local: dict[str, Any],
) -> dict[str, Any]:
    if local["judgment"] != "pass_closeout_ready(마감 준비 통과)":
        raise RuntimeError(f"Frontier25D closeout local checks failed: {json.dumps(local, ensure_ascii=False)}")
    best_f25b = json_ready(f25b_summary.get("best_archetype", {}))
    best_gap = json_ready(f25c_summary.get("best_gap_archetype", {}))
    return {
        "created_at_utc": created_at,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "next_stage_id": NEXT_STAGE_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "preserved_clue": PRESERVED_CLUE,
        "negative_memory": NEGATIVE_MEMORY,
        "runtime_probe_blocker": RUNTIME_PROBE_BLOCKER,
        "onnx_blocker": ONNX_BLOCKER,
        "next_hypothesis_clue": NEXT_HYPOTHESIS_CLUE,
        "stage_open": {
            "status": stage_open.get("status"),
            "judgment": stage_open.get("judgment"),
            "grok_classification": stage_open.get("grok", {}).get("classification", ""),
        },
        "f25b_summary": {
            "status": f25b_summary.get("status"),
            "judgment": f25b_summary.get("judgment"),
            "eligible_micro_rows": f25b_summary.get("eligible_micro_rows"),
            "archetype_candidate_rows": f25b_summary.get("archetype_candidate_rows"),
            "density_bridge_rows": f25b_summary.get("density_bridge_rows"),
            "scout_clue_rows": f25b_summary.get("scout_clue_rows"),
            "seed_surface_rows": f25b_summary.get("seed_surface_rows"),
            "handoff_candidate_rows": f25b_summary.get("handoff_candidate_rows"),
            "top10_f24b_overlap_count": f25b_summary.get("top10_f24b_overlap_count"),
            "best_archetype_id": f25b_summary.get("best_archetype_id"),
        },
        "f25c_summary": {
            "status": f25c_summary.get("status"),
            "judgment": f25c_summary.get("judgment"),
            "repair_decision": f25c_summary.get("repair_decision"),
            "pf_ready_dd_blocked_rows": f25c_summary.get("diagnosis", {}).get("pf_ready_dd_blocked_rows"),
            "dd_ready_pf_blocked_rows": f25c_summary.get("diagnosis", {}).get("dd_ready_pf_blocked_rows"),
            "scout_not_seed_rows": f25c_summary.get("diagnosis", {}).get("scout_not_seed_rows"),
        },
        "best_f25b_archetype": best_f25b,
        "best_gap_archetype": best_gap,
        "candidate_rows": int(len(f25b_candidates)),
        "repair_audit_rows": int(len(f25c_audit)),
        "grok_closeout": grok,
        "local_verification": local,
        "result_boundary": (
            "stage_closeout_preserved_clue_negative_memory_no_wfo_no_mt5_no_runtime_authority"
            "(단계 마감 보존 단서+부정 기억, WFO/MT5/런타임 권위 없음)"
        ),
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(final: dict[str, Any]) -> None:
    write_json(RUN_ROOT / "final_closeout_summary.json", final)
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(final))
    f03b.write_text_sig(REPORT_PATH, report_text(final))
    f03b.write_text_sig(GROK_RECEIPT_PATH, grok_receipt(final))
    f03b.write_text_sig(LOCAL_VERIFICATION_PATH, local_verification_text(final))
    f03b.write_text_sig(REQUIRED_GATE_AUDIT_PATH, required_gate_audit(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "preserved_clue.md", preserved_clue_text(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "negative_memory.md", negative_memory_text(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(final))
    f03b.write_text_sig(DECISION_PATH, decision_text(final))


def run_manifest(final: dict[str, Any]) -> dict[str, Any]:
    artifacts = [
        SCRIPT_PATH,
        F25A_SUMMARY,
        F25B_SUMMARY,
        F25B_CANDIDATES,
        F25C_SUMMARY,
        F25C_AUDIT,
        GROK_STAGE_OPEN_PACKET / "metadata.json",
        GROK_CLOSEOUT_PACKET / "metadata.json",
        GROK_RECEIPT_PATH,
        REPORT_PATH,
        REQUIRED_GATE_AUDIT_PATH,
        STAGE_ROOT / "04_selected" / "preserved_clue.md",
        STAGE_ROOT / "04_selected" / "negative_memory.md",
    ]
    return {
        "identity": {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_stage_id": final["next_stage_id"],
            "next_run_id": final["next_run_id"],
            "created_at_utc": final["created_at_utc"],
        },
        "artifacts": [artifact_identity(path) for path in artifacts],
        "closeout": {
            "status": final["status"],
            "judgment": final["judgment"],
            "preserved_clue": final["preserved_clue"],
            "negative_memory": final["negative_memory"],
            "runtime_probe_blocker": final["runtime_probe_blocker"],
            "onnx_blocker": final["onnx_blocker"],
        },
        "grok": {
            "stage_open_packet": GROK_STAGE_OPEN_PACKET.as_posix(),
            "stage_closeout_packet": GROK_CLOSEOUT_PACKET.as_posix(),
            "closeout_classification": final["grok_closeout"]["classification"],
        },
        "compatibility": {"schema_version": "frontier25d_stage_closeout_v1", "mismatch_policy": "fail_fast(빠른 실패)"},
        "claim_boundary": final["claim_boundary"],
    }


def report_text(final: dict[str, Any]) -> str:
    best = final["best_f25b_archetype"]
    gap = final["best_gap_archetype"]
    f25b_summary = final["f25b_summary"]
    f25c_summary = final["f25c_summary"]
    return f"""# Frontier25D Stage Closeout Report(전선25D 단계 마감 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Action(행동): F25(전선25) DD-headroom-first bridge archetype preselection(손실폭 여유 우선 연결 원형 사전 선택) 가설을 closeout(마감)했습니다.

Effect(효과): F25B/F25C(전선25B/C)의 proxy(프록시) 결과를 preserved clue(보존 단서)와 negative memory(부정 기억)로 닫고, runtime/ONNX(런타임/ONNX)는 인계 후보가 없어 부적격으로 고정합니다.

Preserved clue(보존 단서): `{final['preserved_clue']}`

Negative memory(부정 기억): `{final['negative_memory']}`

Runtime probe blocker(런타임 탐침 차단 사유): `{final['runtime_probe_blocker']}`

ONNX blocker(ONNX 차단 사유): `{final['onnx_blocker']}`

F25B density/scout/seed/handoff(전선25B 빈도/탐색/씨앗/인계): `{f25b_summary['density_bridge_rows']}` / `{f25b_summary['scout_clue_rows']}` / `{f25b_summary['seed_surface_rows']}` / `{f25b_summary['handoff_candidate_rows']}`

F25C bottleneck(전선25C 병목): PF-ready/DD-blocked(수익 팩터 충족/손실폭 차단) `{f25c_summary['pf_ready_dd_blocked_rows']}`, DD-ready/PF-blocked(손실폭 충족/수익 팩터 차단) `{f25c_summary['dd_ready_pf_blocked_rows']}`

Best F25B archetype(최상 전선25B 원형): `{f25b_summary['best_archetype_id']}` with validation/OOS PF-density-DD(검증/표본외 수익 팩터-빈도-손실폭) `{fmt(best.get('validation_profit_factor'))}/{fmt(best.get('validation_trades_per_day'))}/{fmt(best.get('validation_dd_risk'))}` and `{fmt(best.get('oos_profit_factor'))}/{fmt(best.get('oos_trades_per_day'))}/{fmt(best.get('oos_dd_risk'))}`.

Closest seed-gap archetype(씨앗 간격 최저 원형): `{gap.get('archetype_id', '')}` with forward min PF/max DD(전방 최소 수익 팩터/최대 손실폭) `{fmt(gap.get('forward_min_pf'))}` / `{fmt(gap.get('forward_max_dd'))}`.

Grok closeout classification(그록 마감 분류): `{final['grok_closeout']['classification']}`

Next hypothesis clue(다음 가설 단서): `{final['next_hypothesis_clue']}`

Next action(다음 행동): `{final['next_run_id']}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def grok_receipt(final: dict[str, Any]) -> str:
    grok = final["grok_closeout"]
    return f"""# Frontier25D Grok Closeout Receipt(전선25D 그록 마감 영수증)

Trigger reason(트리거 이유): stage closeout(단계 마감)은 Grok review(그록 검토)가 필요했습니다.

Packet(묶음): `{grok['packet']}`

Prompt(프롬프트): `{grok['prompt']}`

Clean output(정리 출력): `{grok['clean_output']}`

Metadata(메타데이터): `{grok['metadata']}`

Prompt hash(프롬프트 해시): `{grok['prompt_hash']}`

Transport success(전송 성공): `{grok['success']}`, returncode(반환 코드) `{grok['returncode']}`, timed_out(시간 초과) `{grok['timed_out']}`

Codex classification(Codex 분류): `{grok['classification']}`

Accepted advice(수용 조언): closeout class(마감 분류)는 preserved_clue + negative_memory(보존 단서+부정 기억), MT5 runtime probe skip(MT5 런타임 탐침 생략)는 out_of_scope_by_claim(주장 범위 밖), F25D materialization(전선25D 물질화)은 로컬 검증 뒤 수행.

Local verification(로컬 검증): `{final['local_verification']['judgment']}`
"""


def local_verification_text(final: dict[str, Any]) -> str:
    rows = []
    for key, value in final["local_verification"]["checks"].items():
        rows.append(f"- {key}: `{value}`")
    return f"""# Frontier25D Local Verification(전선25D 로컬 검증)

Judgment(판정): `{final['local_verification']['judgment']}`

{chr(10).join(rows)}

Effect(효과): Grok(그록) 조언을 자동 실행하지 않고, local files/registers/artifacts(로컬 파일/장부/산출물)로 재검증한 뒤 closeout(마감)했습니다.
"""


def required_gate_audit(final: dict[str, Any]) -> str:
    return f"""# Frontier25 Required Gate Coverage Audit(전선25 필수 게이트 커버리지 감사)

- stage_open_grok_gate(단계 개방 그록 게이트): `{GROK_STAGE_OPEN_PACKET.as_posix()}` recorded(기록)
- proxy_gate(프록시 게이트): `{f25b.RUN_ID}` produced density/scout/seed/handoff(빈도/탐색/씨앗/인계) `{final['f25b_summary']['density_bridge_rows']}/{final['f25b_summary']['scout_clue_rows']}/{final['f25b_summary']['seed_surface_rows']}/{final['f25b_summary']['handoff_candidate_rows']}`
- repair_decision_gate(수리 결정 게이트): `{f25c.RUN_ID}` recorded repair decision(수리 결정 기록) `{final['f25c_summary']['repair_decision']}`
- stage_closeout_grok_gate(단계 마감 그록 게이트): `{GROK_CLOSEOUT_PACKET.as_posix()}` classification(분류) `{final['grok_closeout']['classification']}`
- closeout_gate(마감 게이트): `{final['judgment']}` with report(보고서) `{REPORT_PATH.as_posix()}`
- runtime_probe_gate(런타임 탐침 게이트): `{final['runtime_probe_blocker']}`
- onnx_gate(ONNX 게이트): `{final['onnx_blocker']}`
- tier_pair_record_gate(티어 쌍 기록 게이트): Tier A/Tier B/Tier A+B rows(티어 A/B/A+B 행) written(기록)
- final_claim_guard(최종 주장 방어): runtime authority/operating promotion/Goal Achieve(런타임 권위/운영 승격/목표 달성) not_claimed(주장 없음)
"""


def preserved_clue_text(final: dict[str, Any]) -> str:
    best = final["best_f25b_archetype"]
    return f"""# Frontier25 Preserved Clue(전선25 보존 단서)

Preserved clue(보존 단서): `{final['preserved_clue']}`

Evidence(근거): F25B(전선25B)는 F24B top10 overlap(F24B 상위10 중복) 0개로 non-repeat scout surface(비반복 탐색 표면)를 만들었습니다. density/scout/seed/handoff(빈도/탐색/씨앗/인계)는 `{final['f25b_summary']['density_bridge_rows']}/{final['f25b_summary']['scout_clue_rows']}/{final['f25b_summary']['seed_surface_rows']}/{final['f25b_summary']['handoff_candidate_rows']}`였습니다.

Best scout clue(최상 탐색 단서): `{final['f25b_summary']['best_archetype_id']}` with validation/OOS PF-density-DD(검증/표본외 수익 팩터-빈도-손실폭) `{fmt(best.get('validation_profit_factor'))}/{fmt(best.get('validation_trades_per_day'))}/{fmt(best.get('validation_dd_risk'))}` and `{fmt(best.get('oos_profit_factor'))}/{fmt(best.get('oos_trades_per_day'))}/{fmt(best.get('oos_dd_risk'))}`.

Use boundary(사용 경계): reference only(참조 전용). This is not baseline/promotion/runtime authority(기준선/승격/런타임 권위 아님).
"""


def negative_memory_text(final: dict[str, Any]) -> str:
    gap = final["best_gap_archetype"]
    return f"""# Frontier25 Negative Memory(전선25 부정 기억)

Negative memory(부정 기억): `{final['negative_memory']}`

Why failed(실패 이유): F25B/F25C(전선25B/C)는 seed/handoff(씨앗/인계)를 만들지 못했습니다. Closest seed-gap archetype(씨앗 간격 최저 원형) `{gap.get('archetype_id', '')}` had forward min PF/max DD(전방 최소 수익 팩터/최대 손실폭) `{fmt(gap.get('forward_min_pf'))}` / `{fmt(gap.get('forward_max_dd'))}`, so it still exceeded the 18% seed DD cap(씨앗 손실폭 상한).

Bottleneck(병목): PF-ready/DD-blocked(수익 팩터 충족/손실폭 차단) `{final['f25c_summary']['pf_ready_dd_blocked_rows']}`, DD-ready/PF-blocked(손실폭 충족/수익 팩터 차단) `{final['f25c_summary']['dd_ready_pf_blocked_rows']}`.

Do not repeat(반복 금지): Do not continue F25 by adding validation/OOS-targeted capped filters(검증/표본외 표적 상한 필터) to these archetypes. That would lower claim quality(주장 품질 저하) and repeat repair pressure(수리 압력 반복).
"""


def selection_status(final: dict[str, Any]) -> str:
    return f"""# Frontier25 Selection Status(전선25 선택 상태)

Updated(갱신): {final['created_at_utc']}

Selection(선택): no selected baseline/completion/promotion/runtime authority(선택 기준선/완성/승격/런타임 권위 없음).

Stage closeout(단계 마감): `{RUN_ID}`

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Preserved clue(보존 단서): `{final['preserved_clue']}`

Negative memory(부정 기억): `{final['negative_memory']}`

Runtime probe blocker(런타임 탐침 차단 사유): `{final['runtime_probe_blocker']}`

ONNX blocker(ONNX 차단 사유): `{final['onnx_blocker']}`

Next action(다음 행동): `{final['next_run_id']}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 not_claimed(주장 없음)입니다.
"""


def decision_text(final: dict[str, Any]) -> str:
    return f"""# Decision: Close Frontier25 Bridge Archetype Preselection ONNX Scout(결정: 전선25 연결 원형 사전 선택 ONNX 탐색 마감)

Date(날짜): 2026-06-14

Decision(결정): Close F25(전선25)를 preserved_clue + negative_memory(보존 단서+부정 기억)로 닫습니다.

Effect(효과): F25(전선25)에서 completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)를 주장하지 않고, 다음 frontier(다음 전선)를 새 가설로 시작합니다.

Preserved clue(보존 단서): `{final['preserved_clue']}`

Negative memory(부정 기억): `{final['negative_memory']}`

Next run(다음 실행): `{final['next_run_id']}`
"""


def update_registries(final: dict[str, Any]) -> None:
    f03b.upsert_csv(RUN_REGISTRY, "run_id", run_registry_row(final))
    for row in ledger_rows(final):
        f03b.upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
        f03b.upsert_csv(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", row)
    f03b.append_once(CHANGELOG, RUN_ID, changelog_entry(final))
    f03b.append_once(IDEA_REGISTRY, RUN_ID, idea_registry_entry(final))


def run_registry_row(final: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "stage_closeout(단계 마감)",
        "family": "publish_handoff(게시/인계)",
        "work_family": "publish_handoff(게시/인계)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"preserved={final['preserved_clue']};negative={final['negative_memory']};next={final['next_run_id']}",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": final["next_run_id"],
        "claim_boundary": final["result_boundary"],
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": final["created_at_utc"],
        "primary_kpi": f"scout={final['f25b_summary']['scout_clue_rows']};seed={final['f25b_summary']['seed_surface_rows']};handoff={final['f25b_summary']['handoff_candidate_rows']}",
        "guardrail_kpi": "closeout_no_wfo_no_mt5_no_authority(마감, WFO/MT5/권위 없음)",
        "external_verification_status": final["runtime_probe_blocker"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "result_path": REPORT_PATH.as_posix(),
    }


def ledger_rows(final: dict[str, Any]) -> list[dict[str, Any]]:
    primary = {
        "ledger_row_id": f"{RUN_ID}__tier_a_stage_closeout",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__tier_a_stage_closeout",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "Tier A separate(티어 A 분리)",
        "tier_scope": "Tier A(티어 A)",
        "kpi_scope": "stage_closeout_preserved_clue_negative_memory_not_runtime(단계 마감 보존 단서+부정 기억, 런타임 아님)",
        "scoreboard_lane": "stage_closeout(단계 마감)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": f"scout={final['f25b_summary']['scout_clue_rows']};seed={final['f25b_summary']['seed_surface_rows']};handoff={final['f25b_summary']['handoff_candidate_rows']}",
        "guardrail_kpi": "no_wfo_no_mt5_no_runtime_authority(WFO/MT5/런타임 권위 없음)",
        "external_verification_status": final["runtime_probe_blocker"],
        "notes": f"{final['preserved_clue']};{final['negative_memory']};{final['onnx_blocker']}",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "run_family": "stage_closeout(단계 마감)",
    }
    tier_b = {
        **primary,
        "ledger_row_id": f"{RUN_ID}__tier_b_missing_required",
        "subrun_id": f"{RUN_ID}__tier_b_missing_required",
        "record_view": "Tier B separate(티어 B 분리)",
        "tier_scope": "Tier B(티어 B)",
        "kpi_scope": "missing_required(필수 누락)",
        "primary_kpi": "missing_required_no_tier_b_model_input(필수 누락, Tier B 모델 입력 없음)",
        "guardrail_kpi": "no_tier_b_claim(티어 B 주장 없음)",
        "external_verification_status": "not_applicable_stage_closeout_no_mt5(단계 마감이라 MT5 없음)",
        "notes": "Tier B source absent(Tier B 원천 없음)",
    }
    combined = {
        **primary,
        "ledger_row_id": f"{RUN_ID}__tier_ab_combined_out_of_scope",
        "subrun_id": f"{RUN_ID}__tier_ab_combined_out_of_scope",
        "record_view": "Tier A+B combined(티어 A+B 합산)",
        "tier_scope": "Tier A+B(티어 A+B)",
        "kpi_scope": "out_of_scope_by_claim(주장 범위 밖)",
        "primary_kpi": "out_of_scope_by_claim_no_combined_source(주장 범위 밖, 합산 원천 없음)",
        "guardrail_kpi": "no_synthetic_combined_claim(합성 합산 주장 없음)",
        "external_verification_status": "not_applicable_stage_closeout_no_mt5(단계 마감이라 MT5 없음)",
        "notes": "Combined source absent(합산 원천 없음)",
    }
    return [primary, tier_b, combined]


def changelog_entry(final: dict[str, Any]) -> str:
    return (
        f"- {final['created_at_utc']}: `{RUN_ID}` closed Frontier25(전선25 마감). "
        f"Effect(효과): preserved clue(보존 단서) `{final['preserved_clue']}` and negative memory(부정 기억) `{final['negative_memory']}` recorded; next run(다음 실행) `{final['next_run_id']}`.\n"
    )


def idea_registry_entry(final: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR25-BRIDGE-ARCHETYPE-PRESELECTION-ONNX-SCOUT`: `{RUN_ID}` closed as preserved_clue + negative_memory(보존 단서+부정 기억). "
        f"Effect(효과): do not repeat validation-targeted repair(검증 표적 수리 반복 금지); next clue(다음 단서) `{final['next_hypothesis_clue']}`.\n"
    )


def update_current_truth(final: dict[str, Any]) -> None:
    io_path(WORKSPACE_STATE).write_text(workspace_state(final), encoding="utf-8-sig")
    f03b.write_text_sig(CURRENT_WORKING_STATE, current_working_state(final))


def workspace_state(final: dict[str, Any]) -> str:
    return "\n".join([
        f"current_stage_id: {STAGE_ID}",
        f"current_run_id: {RUN_ID}",
        f"latest_completed_run_id: {RUN_ID}",
        f"current_status: {final['status']}",
        f"current_judgment: {final['judgment']}",
        f"next_stage_id: {final['next_stage_id']}",
        f"next_run_id: {final['next_run_id']}",
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
- next stage(다음 단계): `{final['next_stage_id']}`
- next run(다음 실행): `{final['next_run_id']}`

## Current Truth(현재 진실)

Action(행동): F25(전선25) DD-headroom-first bridge archetype preselection(손실폭 여유 우선 연결 원형 사전 선택)을 closeout(마감)했습니다.

Effect(효과): F25(전선25)는 non-repeat scout clue(비반복 탐색 단서)를 보존하고, seed/handoff(씨앗/인계) 실패를 negative memory(부정 기억)로 남깁니다.

Preserved clue(보존 단서): `{final['preserved_clue']}`

Negative memory(부정 기억): `{final['negative_memory']}`

Runtime probe blocker(런타임 탐침 차단 사유): `{final['runtime_probe_blocker']}`

ONNX blocker(ONNX 차단 사유): `{final['onnx_blocker']}`

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def artifact_identity(path: Path) -> dict[str, str]:
    return {"path": path.as_posix(), "sha256": sha256_io(path) if path_exists(path) else "pending_or_missing(대기 또는 누락)"}


def sha256_io(path: Path) -> str:
    h = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


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
        return "NA"
    if not math.isfinite(number):
        return "NA"
    return f"{number:.6g}"


if __name__ == "__main__":
    raise SystemExit(main())
