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
from stage_pipelines.stage_frontier_27 import frontier27b_soft_joint_satisfaction_penalty_proxy_scout as f27b
from stage_pipelines.stage_frontier_27 import frontier27c_soft_penalty_repair_or_closeout_decision as f27c
from stage_pipelines.stage_frontier_27 import materialize_frontier27a_stage_open as f27a


STAGE_ID = f27a.STAGE_ID
RUN_ID = "frontier27D_stage_closeout_soft_joint_satisfaction_penalty_v1"
RUN_NUMBER = "frontier27D"
PARENT_RUN_ID = f27c.RUN_ID
STATUS = "closed_preserved_clue_negative_memory_soft_penalty_scout_only_no_handoff"
JUDGMENT = "preserved_clue_negative_memory(보존 단서+부정 기억)"
NEXT_STAGE_ID = "stage_frontier_28__train_only_stability_gap_penalty_for_pf_dd_balance_onnx_scout"
NEXT_RUN_ID = "frontier28A_stage_open_train_only_stability_gap_penalty_pf_dd_balance_hypothesis_design_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
GROK_RECEIPT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_grok_closeout_receipt.md"
LOCAL_VERIFICATION_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_local_verification.md"
REQUIRED_GATE_AUDIT_PATH = STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md"
DECISION_PATH = Path("docs/decisions/2026-06-14_stage_frontier_27_soft_joint_satisfaction_penalty_bridge_union_onnx_scout_closeout.md")
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_27/frontier27d_stage_closeout.py")

F27A_SUMMARY = STAGE_ROOT / "02_runs" / f27a.RUN_ID / "stage_open_summary.json"
F27B_SUMMARY = STAGE_ROOT / "02_runs" / f27b.RUN_ID / "final_summary.json"
F27B_CANDIDATE_SUMMARY = STAGE_ROOT / "02_runs" / f27b.RUN_ID / "soft_penalty_union_candidate_summary.csv"
F27B_REPEAT_AUDIT = STAGE_ROOT / "02_runs" / f27b.RUN_ID / "f24b_f25b_f26b_top10_nonrepeat_audit.csv"
F27C_SUMMARY = STAGE_ROOT / "02_runs" / f27c.RUN_ID / "final_summary.json"
F27C_REPAIR_AUDIT = STAGE_ROOT / "02_runs" / f27c.RUN_ID / "repair_rejection_audit.csv"

GROK_STAGE_OPEN_PACKET = Path("docs/agent_control/grok_reviews/2026-06-14_frontier27_stage_open/small_review")
GROK_CLOSEOUT_PACKET = Path("docs/agent_control/grok_reviews/2026-06-14_frontier27_stage_closeout/small_review")

RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")
NEGATIVE_RESULT_REGISTER = Path("docs/registers/negative_result_register.md")
CHANGELOG = Path("docs/workspace/changelog.md")
WORKSPACE_STATE = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE = Path("docs/context/current_working_state.md")

PRESERVED_CLUE = f27c.PRESERVED_CLUE
NEGATIVE_MEMORY = f27c.NEGATIVE_MEMORY
NEXT_HYPOTHESIS_CLUE = f27c.NEXT_HYPOTHESIS_CLUE
REPAIR_DECISION = f27c.REPAIR_DECISION
RUNTIME_PROBE_BLOCKER = (
    "runtime_probe_ineligible_no_handoff_candidate_after_f27c_repair_decision"
    "(F27C 수리 결정 뒤 인계 후보 없어 런타임 탐침 부적격)"
)
ONNX_BLOCKER = (
    "onnx_branch_unattempted_no_handoff_candidate_after_f27c_repair_decision"
    "(F27C 수리 결정 뒤 인계 후보 없어 ONNX 미시도)"
)


def main() -> int:
    ensure_dirs()
    normalize_grok_markdown()
    created_at = utc_now()
    stage_open = read_json(F27A_SUMMARY)
    f27b_summary = read_json(F27B_SUMMARY)
    f27c_summary = read_json(F27C_SUMMARY)
    candidate_summary = pd.read_csv(io_path(F27B_CANDIDATE_SUMMARY))
    repeat_audit = pd.read_csv(io_path(F27B_REPEAT_AUDIT))
    repair_audit = pd.read_csv(io_path(F27C_REPAIR_AUDIT))
    grok = load_grok_closeout()
    local = validate_context(stage_open, f27b_summary, f27c_summary, candidate_summary, repeat_audit, repair_audit, grok)
    final = build_final(created_at, stage_open, f27b_summary, f27c_summary, candidate_summary, repeat_audit, repair_audit, grok, local)
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


def normalize_grok_markdown() -> None:
    for name in ("prompt.md", "clean_output.md"):
        path = GROK_CLOSEOUT_PACKET / name
        if path_exists(path):
            text = io_path(path).read_text(encoding="utf-8-sig")
            f03b.write_text_sig(path, text.rstrip() + "\n")


def load_grok_closeout() -> dict[str, Any]:
    metadata = read_json(GROK_CLOSEOUT_PACKET / "metadata.json")
    output = read_text(GROK_CLOSEOUT_PACKET / "clean_output.md")
    lower = output.lower()
    accepted = (
        "verdict" in lower
        and "accepted" in lower
        and "closeout_class_ok" in lower
        and "repair_rejection_ok" in lower
        and "runtime_probe_status_ok" in lower
        and "next_clue_ok" in lower
    )
    return {
        "packet": GROK_CLOSEOUT_PACKET.as_posix(),
        "prompt": (GROK_CLOSEOUT_PACKET / "prompt.md").as_posix(),
        "clean_output": (GROK_CLOSEOUT_PACKET / "clean_output.md").as_posix(),
        "metadata": (GROK_CLOSEOUT_PACKET / "metadata.json").as_posix(),
        "prompt_hash": metadata.get("prompt_hash", ""),
        "success": bool(metadata.get("success")),
        "returncode": metadata.get("returncode"),
        "timed_out": bool(metadata.get("timed_out")),
        "unexpected_top_level_artifacts": metadata.get("unexpected_top_level_artifacts", []),
        "classification": "accepted_preserved_clue_negative_memory_closeout(수용, 보존 단서+부정 기억 마감)" if accepted else "needs_local_verification(로컬 검증 필요)",
        "accepted": accepted,
        "output_excerpt": output[:2600],
    }


def validate_context(
    stage_open: dict[str, Any],
    f27b_summary: dict[str, Any],
    f27c_summary: dict[str, Any],
    candidate_summary: pd.DataFrame,
    repeat_audit: pd.DataFrame,
    repair_audit: pd.DataFrame,
    grok: dict[str, Any],
) -> dict[str, Any]:
    workspace = read_text(WORKSPACE_STATE)
    checks = {
        "workspace_current_stage_frontier27": f"current_stage_id: {STAGE_ID}" in workspace,
        "workspace_next_or_current_frontier27d": f"next_run_id: {RUN_ID}" in workspace or f"current_run_id: {RUN_ID}" in workspace,
        "stage_open_parent_matches": stage_open.get("run_id") == f27a.RUN_ID,
        "f27b_parent_matches": f27b_summary.get("run_id") == f27b.RUN_ID,
        "f27b_full_micro_pool": int(f27b_summary.get("soft_micro_pool_rows", -1)) == 80,
        "f27b_union_surface_restored": int(f27b_summary.get("soft_union_candidate_rows", -1)) == 234,
        "f27b_broad_envelope_ledger_truth": int(f27b_summary.get("broad_scout_envelope_rows", -1)) == 205,
        "f27b_scout_19_seed_handoff_zero": int(f27b_summary.get("scout_clue_rows", -1)) == 19
        and int(f27b_summary.get("seed_surface_rows", -1)) == 0
        and int(f27b_summary.get("handoff_candidate_rows", -1)) == 0,
        "f27b_repeat_top10_zero": int(f27b_summary.get("top10_f24b_overlap_count", -1)) == 0
        and int(f27b_summary.get("top10_f25b_overlap_count", -1)) == 0
        and int(f27b_summary.get("top10_f26b_overlap_count", -1)) == 0,
        "f27c_parent_matches": f27c_summary.get("run_id") == f27c.RUN_ID,
        "f27c_next_closeout_matches": f27c_summary.get("next_run_id") == RUN_ID,
        "f27c_preserved_clue_matches": f27c_summary.get("preserved_clue") == PRESERVED_CLUE,
        "f27c_negative_memory_matches": f27c_summary.get("negative_memory") == NEGATIVE_MEMORY,
        "candidate_summary_present": not candidate_summary.empty,
        "repeat_audit_present": not repeat_audit.empty,
        "repair_audit_present": not repair_audit.empty,
        "grok_closeout_success": grok["success"] and grok["returncode"] == 0 and not grok["timed_out"],
        "grok_closeout_accepted": grok["accepted"],
        "grok_stage_open_packet_present": path_exists(GROK_STAGE_OPEN_PACKET / "metadata.json"),
        "grok_no_unexpected_top_level_artifacts": not grok["unexpected_top_level_artifacts"],
    }
    return {
        "checks": checks,
        "judgment": "pass_closeout_ready(마감 준비 통과)" if all(checks.values()) else "needs_manual_review(수동 검토 필요)",
    }


def build_final(
    created_at: str,
    stage_open: dict[str, Any],
    f27b_summary: dict[str, Any],
    f27c_summary: dict[str, Any],
    candidate_summary: pd.DataFrame,
    repeat_audit: pd.DataFrame,
    repair_audit: pd.DataFrame,
    grok: dict[str, Any],
    local: dict[str, Any],
) -> dict[str, Any]:
    if local["judgment"] != "pass_closeout_ready(마감 준비 통과)":
        raise RuntimeError(f"Frontier27D closeout local checks failed: {json.dumps(local, ensure_ascii=False)}")
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
        "next_hypothesis_clue": NEXT_HYPOTHESIS_CLUE,
        "repair_decision": REPAIR_DECISION,
        "runtime_probe_blocker": RUNTIME_PROBE_BLOCKER,
        "onnx_blocker": ONNX_BLOCKER,
        "stage_open": {
            "status": stage_open.get("status"),
            "judgment": stage_open.get("judgment"),
            "grok_classification": stage_open.get("grok", {}).get("classification", ""),
        },
        "f27b_summary": {
            "status": f27b_summary.get("status"),
            "judgment": f27b_summary.get("judgment"),
            "soft_micro_pool_rows": f27b_summary.get("soft_micro_pool_rows"),
            "soft_micro_construction_pool_rows": f27b_summary.get("soft_micro_construction_pool_rows"),
            "soft_union_candidate_rows": f27b_summary.get("soft_union_candidate_rows"),
            "broad_scout_envelope_rows": f27b_summary.get("broad_scout_envelope_rows"),
            "density_bridge_rows": f27b_summary.get("density_bridge_rows"),
            "scout_clue_rows": f27b_summary.get("scout_clue_rows"),
            "seed_surface_rows": f27b_summary.get("seed_surface_rows"),
            "handoff_candidate_rows": f27b_summary.get("handoff_candidate_rows"),
            "best_soft_union_id": f27b_summary.get("best_soft_union_id"),
            "top10_f24b_overlap_count": f27b_summary.get("top10_f24b_overlap_count"),
            "top10_f25b_overlap_count": f27b_summary.get("top10_f25b_overlap_count"),
            "top10_f26b_overlap_count": f27b_summary.get("top10_f26b_overlap_count"),
            "best_soft_union": f27b_summary.get("best_soft_union", {}),
        },
        "f27c_summary": {
            "status": f27c_summary.get("status"),
            "judgment": f27c_summary.get("judgment"),
            "repair_decision": f27c_summary.get("repair_decision"),
            "preserved_clue": f27c_summary.get("preserved_clue"),
            "negative_memory": f27c_summary.get("negative_memory"),
        },
        "candidate_summary_rows": int(len(candidate_summary)),
        "repeat_audit_rows": int(len(repeat_audit)),
        "repair_audit_rows": int(len(repair_audit)),
        "grok_closeout": grok,
        "local_verification": local,
        "result_boundary": "stage_closeout_preserved_clue_negative_memory_no_wfo_no_mt5_no_runtime_authority(단계 마감 보존 단서+부정 기억, WFO/MT5/런타임 권위 없음)",
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
        F27A_SUMMARY,
        F27B_SUMMARY,
        F27B_CANDIDATE_SUMMARY,
        F27B_REPEAT_AUDIT,
        F27C_SUMMARY,
        F27C_REPAIR_AUDIT,
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
            "next_stage_id": NEXT_STAGE_ID,
            "next_run_id": NEXT_RUN_ID,
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
        "compatibility": {"schema_version": "frontier27d_stage_closeout_v1", "mismatch_policy": "fail_fast(빠른 실패)"},
        "claim_boundary": final["claim_boundary"],
    }


def report_text(final: dict[str, Any]) -> str:
    f27b_summary = final["f27b_summary"]
    best = f27b_summary.get("best_soft_union", {})
    return f"""# Frontier27D Stage Closeout Report(전선27D 단계 마감 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Action(행동): F27(전선27) soft joint satisfaction penalty before union(합집합 전 연성 합동 충족 페널티) 가설을 preserved clue + negative memory(보존 단서+부정 기억)로 closeout(마감)했습니다.

Effect(효과): soft penalty(연성 페널티)가 union surface(합집합 표면)를 복원했지만 seed/handoff(씨앗/인계)는 만들지 못했다는 경계를 기록하고, MT5/ONNX/WFO(메타트레이더5/온엑스/워크포워드 최적화)는 열지 않습니다.

Preserved clue(보존 단서): `{final['preserved_clue']}`

Negative memory(부정 기억): `{final['negative_memory']}`

Runtime probe blocker(런타임 탐침 차단 사유): `{final['runtime_probe_blocker']}`

ONNX blocker(ONNX 차단 사유): `{final['onnx_blocker']}`

F27B micro/construct/union/envelope/density/scout/seed/handoff(전선27B 미세/구성/합집합/외피/빈도/탐색/씨앗/인계): `{f27b_summary['soft_micro_pool_rows']}` / `{f27b_summary['soft_micro_construction_pool_rows']}` / `{f27b_summary['soft_union_candidate_rows']}` / `{f27b_summary['broad_scout_envelope_rows']}` / `{f27b_summary['density_bridge_rows']}` / `{f27b_summary['scout_clue_rows']}` / `{f27b_summary['seed_surface_rows']}` / `{f27b_summary['handoff_candidate_rows']}`

Best soft union(최상 연성 합집합): `{f27b_summary['best_soft_union_id']}` with validation/OOS PF-density-DD(검증/OOS 수익 팩터-빈도-손실폭) `{fmt(best.get('validation_profit_factor'))}/{fmt(best.get('validation_trades_per_day'))}/{fmt(best.get('validation_dd_risk'))}` and `{fmt(best.get('oos_profit_factor'))}/{fmt(best.get('oos_trades_per_day'))}/{fmt(best.get('oos_dd_risk'))}`.

Grok closeout classification(그록 마감 분류): `{final['grok_closeout']['classification']}`

Next hypothesis clue(다음 가설 단서): `{final['next_hypothesis_clue']}`

Next action(다음 행동): `{final['next_run_id']}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def grok_receipt(final: dict[str, Any]) -> str:
    grok = final["grok_closeout"]
    return f"""# Frontier27D Grok Closeout Receipt(전선27D 그록 마감 영수증)

Trigger reason(트리거 이유): stage closeout(단계 마감)은 Grok review(그록 검토)가 필요합니다.

Packet(묶음): `{grok['packet']}`

Prompt(프롬프트): `{grok['prompt']}`

Clean output(정리 출력): `{grok['clean_output']}`

Metadata(메타데이터): `{grok['metadata']}`

Prompt hash(프롬프트 해시): `{grok['prompt_hash']}`

Transport success(전송 성공): `{grok['success']}`, returncode(반환 코드) `{grok['returncode']}`, timed_out(시간 초과) `{grok['timed_out']}`

Codex classification(Codex 분류): `{grok['classification']}`

Accepted advice(수용 조언): preserved_clue_negative_memory closeout(보존 단서+부정 기억 마감), repair rejection(수리 거절), canonical runtime_probe_ineligible(정규 런타임 탐침 부적격), and next clue(다음 단서)를 수용했습니다.

Local verification(로컬 검증): `{final['local_verification']['judgment']}`
"""


def local_verification_text(final: dict[str, Any]) -> str:
    rows = [f"- {key}: `{value}`" for key, value in final["local_verification"]["checks"].items()]
    return f"""# Frontier27D Local Verification(전선27D 로컬 검증)

Judgment(판정): `{final['local_verification']['judgment']}`

{chr(10).join(rows)}

Effect(효과): Grok(그록) 조언을 자동 실행하지 않고 local files/registers/artifacts(로컬 파일/장부/산출물)로 재검증한 뒤 closeout(마감)했습니다.
"""


def required_gate_audit(final: dict[str, Any]) -> str:
    f27b_summary = final["f27b_summary"]
    return f"""# Frontier27 Required Gate Coverage Audit(전선27 필수 게이트 커버리지 감사)

- stage_open_grok_gate(단계 개방 그록 게이트): `{GROK_STAGE_OPEN_PACKET.as_posix()}` recorded(기록)
- proxy_gate(프록시 게이트): `{f27b.RUN_ID}` produced micro/union/scout/seed/handoff(미세/합집합/탐색/씨앗/인계) `{f27b_summary['soft_micro_pool_rows']}/{f27b_summary['soft_union_candidate_rows']}/{f27b_summary['scout_clue_rows']}/{f27b_summary['seed_surface_rows']}/{f27b_summary['handoff_candidate_rows']}`
- repair_decision_gate(수리 결정 게이트): `{f27c.RUN_ID}` recorded repair rejection(수리 거절 기록) `{final['repair_decision']}`
- stage_closeout_grok_gate(단계 마감 그록 게이트): `{GROK_CLOSEOUT_PACKET.as_posix()}` classification(분류) `{final['grok_closeout']['classification']}`
- closeout_gate(마감 게이트): `{final['judgment']}` with report(보고서) `{REPORT_PATH.as_posix()}`
- runtime_probe_gate(런타임 탐침 게이트): `{final['runtime_probe_blocker']}`
- onnx_gate(ONNX 게이트): `{final['onnx_blocker']}`
- tier_pair_record_gate(티어 쌍 기록 게이트): Tier A/Tier B/Tier A+B rows(티어 A/B/A+B 행) written(기록)
- final_claim_guard(최종 주장 방어): runtime authority/operating promotion/Goal Achieve(런타임 권위/운영 승격/목표 달성) not_claimed(주장 없음)
"""


def preserved_clue_text(final: dict[str, Any]) -> str:
    f27b_summary = final["f27b_summary"]
    return f"""# Frontier27 Preserved Clue(전선27 보존 단서)

Preserved clue(보존 단서): `{final['preserved_clue']}`

Evidence(근거): F27B(전선27B)는 full 80 micro pool(전체 80 미세 풀)에서 `{f27b_summary['soft_union_candidate_rows']}` union rows(합집합 행)와 `{f27b_summary['scout_clue_rows']}` scout rows(탐색 행)를 만들었습니다.

Use boundary(사용 경계): reference only(참조 전용). This is not baseline/promotion/runtime authority(기준선/승격/런타임 권위 아님).
"""


def negative_memory_text(final: dict[str, Any]) -> str:
    f27b_summary = final["f27b_summary"]
    return f"""# Frontier27 Negative Memory(전선27 부정 기억)

Negative memory(부정 기억): `{final['negative_memory']}`

Why failed(실패 이유): locked soft penalty rank(잠금 연성 페널티 순위)는 scout rows(탐색 행) `{f27b_summary['scout_clue_rows']}`개를 만들었지만 seed/handoff(씨앗/인계)는 `{f27b_summary['seed_surface_rows']}` / `{f27b_summary['handoff_candidate_rows']}`개로 남았습니다.

Do not repeat(반복 금지): Do not claim soft penalty surface restoration(연성 페널티 표면 복원)을 seed/handoff/completion(씨앗/인계/완성)으로 과장하지 않습니다.
"""


def selection_status(final: dict[str, Any]) -> str:
    return f"""# Frontier27 Selection Status(전선27 선택 상태)

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
    return f"""# Decision(결정): Close Frontier27 Soft Penalty Scout(전선27 연성 페널티 탐색 마감)

Date(날짜): 2026-06-14

Decision(결정): Close(마감) `{STAGE_ID}` as preserved_clue_negative_memory(보존 단서+부정 기억).

Effect(효과): union surface restoration(합집합 표면 복원)은 보존하지만 seed/handoff failure(씨앗/인계 실패)는 반복 금지 기억으로 남기고, 다음 frontier(전선)를 새 가설로 시작합니다.

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
    f03b.append_once(NEGATIVE_RESULT_REGISTER, RUN_ID, negative_register_entry(final))


def run_registry_row(final: dict[str, Any]) -> dict[str, Any]:
    f27b_summary = final["f27b_summary"]
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
        "primary_kpi": f"union={f27b_summary['soft_union_candidate_rows']};scout={f27b_summary['scout_clue_rows']};seed={f27b_summary['seed_surface_rows']};handoff={f27b_summary['handoff_candidate_rows']}",
        "guardrail_kpi": "closeout_preserved_clue_negative_memory_no_wfo_no_mt5_no_authority(마감 보존 단서+부정 기억, WFO/MT5/권위 없음)",
        "external_verification_status": final["runtime_probe_blocker"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "result_path": REPORT_PATH.as_posix(),
    }


def ledger_rows(final: dict[str, Any]) -> list[dict[str, Any]]:
    f27b_summary = final["f27b_summary"]
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
        "primary_kpi": f"micro=80;union={f27b_summary['soft_union_candidate_rows']};scout={f27b_summary['scout_clue_rows']};seed={f27b_summary['seed_surface_rows']};handoff={f27b_summary['handoff_candidate_rows']}",
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
        "notes": "Tier B source absent(티어 B 원천 없음)",
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
        f"- {final['created_at_utc']}: `{RUN_ID}` closed Frontier27(전선27 마감). "
        f"Effect(효과): preserved clue(보존 단서) `{final['preserved_clue']}` and negative memory(부정 기억) `{final['negative_memory']}` recorded; next run(다음 실행) `{final['next_run_id']}`.\n"
    )


def idea_registry_entry(final: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR27-SOFT-JOINT-SATISFACTION-PENALTY-BRIDGE-UNION-ONNX-SCOUT`: `{RUN_ID}` closed as preserved_clue_negative_memory(보존 단서+부정 기억). "
        f"Effect(효과): soft penalty union surface(연성 페널티 합집합 표면)는 보존하지만 seed/handoff(씨앗/인계) 없음으로 MT5/ONNX(메타트레이더5/온엑스)는 열지 않습니다; next clue(다음 단서) `{final['next_hypothesis_clue']}`.\n"
    )


def negative_register_entry(final: dict[str, Any]) -> str:
    return (
        f"- `{RUN_ID}`: `{final['negative_memory']}`. Preserved clue(보존 단서): `{final['preserved_clue']}`. "
        f"Runtime blocker(런타임 차단): `{final['runtime_probe_blocker']}`. ONNX blocker(ONNX 차단): `{final['onnx_blocker']}`. "
        "Effect(효과): 다음 전선은 soft penalty surface restoration(연성 페널티 표면 복원)을 seed/handoff(씨앗/인계)로 과장하지 않고 train-only stability gap(학습 전용 안정성 격차)을 새 가설로 다룹니다.\n"
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
    f27b_summary = final["f27b_summary"]
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

Action(행동): F27(전선27) soft joint satisfaction penalty before union(합집합 전 연성 합동 충족 페널티)을 preserved clue + negative memory(보존 단서+부정 기억)로 closeout(마감)했습니다.

Effect(효과): union surface(합집합 표면) 복원과 scout clue(탐색 단서)는 보존하지만 seed/handoff(씨앗/인계) 부재를 반복 금지 기억으로 남깁니다.

F27B micro/union/scout/seed/handoff(전선27B 미세/합집합/탐색/씨앗/인계): `{f27b_summary['soft_micro_pool_rows']}` / `{f27b_summary['soft_union_candidate_rows']}` / `{f27b_summary['scout_clue_rows']}` / `{f27b_summary['seed_surface_rows']}` / `{f27b_summary['handoff_candidate_rows']}`

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
        return "inf"
    return f"{number:.3f}"


if __name__ == "__main__":
    raise SystemExit(main())
