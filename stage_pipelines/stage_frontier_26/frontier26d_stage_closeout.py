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
from stage_pipelines.stage_frontier_26 import frontier26b_joint_micro_satisfaction_proxy_scout as f26b
from stage_pipelines.stage_frontier_26 import frontier26c_joint_micro_repair_or_closeout_decision as f26c
from stage_pipelines.stage_frontier_26 import materialize_frontier26a_stage_open as f26a


STAGE_ID = f26a.STAGE_ID
RUN_ID = "frontier26D_stage_closeout_joint_micro_satisfaction_v1"
RUN_NUMBER = "frontier26D"
PARENT_RUN_ID = f26c.RUN_ID
STATUS = "closed_invalid_setup_joint_micro_gate_union_collapse_no_handoff"
JUDGMENT = "invalid_setup(무효 설정)"
NEXT_STAGE_ID = "stage_frontier_27__soft_joint_satisfaction_penalty_bridge_union_onnx_scout"
NEXT_RUN_ID = "frontier27A_stage_open_soft_joint_satisfaction_penalty_bridge_union_hypothesis_design_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
GROK_RECEIPT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_grok_closeout_receipt.md"
LOCAL_VERIFICATION_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_local_verification.md"
REQUIRED_GATE_AUDIT_PATH = STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md"
DECISION_PATH = Path("docs/decisions/2026-06-14_stage_frontier_26_joint_micro_satisfaction_before_bridge_union_onnx_scout_closeout.md")
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_26/frontier26d_stage_closeout.py")

F26A_SUMMARY = STAGE_ROOT / "02_runs" / f26a.RUN_ID / "stage_open_summary.json"
F26B_SUMMARY = STAGE_ROOT / "02_runs" / f26b.RUN_ID / "final_summary.json"
F26B_MICRO_AUDIT = STAGE_ROOT / "02_runs" / f26b.RUN_ID / "micro_joint_pass_audit.csv"
F26B_REJECTION_AUDIT = STAGE_ROOT / "02_runs" / f26b.RUN_ID / "joint_union_rejection_audit.csv"
F26C_SUMMARY = STAGE_ROOT / "02_runs" / f26c.RUN_ID / "final_summary.json"
F26C_REPAIR_AUDIT = STAGE_ROOT / "02_runs" / f26c.RUN_ID / "repair_rejection_audit.csv"

GROK_STAGE_OPEN_PACKET = Path("docs/agent_control/grok_reviews/2026-06-14_frontier26_stage_open/small_review")
GROK_CLOSEOUT_PACKET = Path("docs/agent_control/grok_reviews/2026-06-14_frontier26_stage_closeout/small_review")
GROK_CLOSEOUT_RETRY_PACKET = Path("docs/agent_control/grok_reviews/2026-06-14_frontier26_stage_closeout/small_review_retry")

RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")
CHANGELOG = Path("docs/workspace/changelog.md")
WORKSPACE_STATE = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE = Path("docs/context/current_working_state.md")

INVALID_SETUP = f26c.INVALID_SETUP
PRESERVED_CLUE = f26c.PRESERVED_CLUE
NEGATIVE_MEMORY = f26c.NEGATIVE_MEMORY
NEXT_HYPOTHESIS_CLUE = f26c.NEXT_HYPOTHESIS_CLUE
RUNTIME_PROBE_BLOCKER = (
    "runtime_probe_ineligible_no_handoff_candidate_after_f26c_invalid_setup_decision"
    "(F26C 무효 설정 결정 뒤 인계 후보 없어 런타임 탐침 부적격)"
)
ONNX_BLOCKER = (
    "onnx_branch_unattempted_no_handoff_candidate_after_f26c_invalid_setup_decision"
    "(F26C 무효 설정 결정 뒤 인계 후보 없어 ONNX 미시도)"
)


def main() -> int:
    ensure_dirs()
    normalize_grok_markdown()
    created_at = utc_now()
    stage_open = read_json(F26A_SUMMARY)
    f26b_summary = read_json(F26B_SUMMARY)
    f26c_summary = read_json(F26C_SUMMARY)
    rejection_audit = pd.read_csv(io_path(F26B_REJECTION_AUDIT))
    repair_audit = pd.read_csv(io_path(F26C_REPAIR_AUDIT))
    grok = load_grok_closeout()
    local = validate_context(stage_open, f26b_summary, f26c_summary, rejection_audit, repair_audit, grok)
    final = build_final(created_at, stage_open, f26b_summary, f26c_summary, rejection_audit, repair_audit, grok, local)
    write_outputs(final)
    update_registries(final)
    update_current_truth(final)
    print(json.dumps(json_ready({
        "status": final["status"],
        "judgment": final["judgment"],
        "run_id": RUN_ID,
        "invalid_setup": final["invalid_setup"],
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
    for packet in (GROK_CLOSEOUT_PACKET, GROK_CLOSEOUT_RETRY_PACKET):
        for name in ("prompt.md", "clean_output.md"):
            path = packet / name
            if path_exists(path):
                text = io_path(path).read_text(encoding="utf-8-sig")
                f03b.write_text_sig(path, text.rstrip() + "\n")


def load_grok_closeout() -> dict[str, Any]:
    retry_meta = read_json(GROK_CLOSEOUT_RETRY_PACKET / "metadata.json")
    retry_output = read_text(GROK_CLOSEOUT_RETRY_PACKET / "clean_output.md")
    first_meta = read_json(GROK_CLOSEOUT_PACKET / "metadata.json")
    first_output = read_text(GROK_CLOSEOUT_PACKET / "clean_output.md")
    lower = retry_output.lower()
    accepted = "verdict" in lower and "accepted" in lower and "closeout_class_ok" in lower and "yes" in lower
    return {
        "packet": GROK_CLOSEOUT_RETRY_PACKET.as_posix(),
        "prompt": (GROK_CLOSEOUT_RETRY_PACKET / "prompt.md").as_posix(),
        "clean_output": (GROK_CLOSEOUT_RETRY_PACKET / "clean_output.md").as_posix(),
        "metadata": (GROK_CLOSEOUT_RETRY_PACKET / "metadata.json").as_posix(),
        "prompt_hash": retry_meta.get("prompt_hash", ""),
        "success": bool(retry_meta.get("success")),
        "returncode": retry_meta.get("returncode"),
        "timed_out": retry_meta.get("timed_out"),
        "classification": "accepted_invalid_setup_closeout(수용, 무효 설정 마감)" if accepted else "needs_local_verification(로컬 검증 필요)",
        "accepted": accepted,
        "output_excerpt": retry_output[:2000],
        "first_packet": {
            "packet": GROK_CLOSEOUT_PACKET.as_posix(),
            "success": bool(first_meta.get("success")),
            "returncode": first_meta.get("returncode"),
            "timed_out": first_meta.get("timed_out"),
            "classification": "transport_success_missing_verdict(전송 성공, 판정 누락)",
            "output_excerpt": first_output[:800],
        },
    }


def validate_context(
    stage_open: dict[str, Any],
    f26b_summary: dict[str, Any],
    f26c_summary: dict[str, Any],
    rejection_audit: pd.DataFrame,
    repair_audit: pd.DataFrame,
    grok: dict[str, Any],
) -> dict[str, Any]:
    workspace = read_text(WORKSPACE_STATE)
    checks = {
        "workspace_current_stage_frontier26": f"current_stage_id: {STAGE_ID}" in workspace,
        "workspace_next_or_current_frontier26d": f"next_run_id: {RUN_ID}" in workspace or f"current_run_id: {RUN_ID}" in workspace,
        "stage_open_parent_matches": stage_open.get("run_id") == f26a.RUN_ID,
        "f26b_zero_valid_unions": int(f26b_summary.get("joint_union_candidate_rows", -1)) == 0,
        "f26b_zero_seed_handoff": int(f26b_summary.get("seed_surface_rows", -1)) == 0
        and int(f26b_summary.get("handoff_candidate_rows", -1)) == 0,
        "f26b_three_passers_four_attempts": int(f26b_summary.get("joint_micro_pass_rows", -1)) == 3
        and int(f26b_summary.get("joint_union_attempt_rows", -1)) == 4,
        "f26c_parent_matches": f26c_summary.get("run_id") == PARENT_RUN_ID,
        "f26c_next_closeout_matches": f26c_summary.get("next_run_id") == RUN_ID,
        "f26c_invalid_setup_matches": f26c_summary.get("invalid_setup") == INVALID_SETUP,
        "f26c_repair_rejected": f26c_summary.get("repair_decision") == f26c.REPAIR_DECISION,
        "rejection_audit_present": not rejection_audit.empty,
        "repair_audit_present": not repair_audit.empty,
        "grok_closeout_retry_success": grok["success"] and grok["accepted"],
        "grok_stage_open_packet_present": path_exists(GROK_STAGE_OPEN_PACKET / "metadata.json"),
        "grok_closeout_packets_present": path_exists(GROK_CLOSEOUT_PACKET / "metadata.json")
        and path_exists(GROK_CLOSEOUT_RETRY_PACKET / "metadata.json"),
    }
    return {
        "checks": checks,
        "judgment": "pass_closeout_ready(마감 준비 통과)" if all(checks.values()) else "needs_manual_review(수동 검토 필요)",
    }


def build_final(
    created_at: str,
    stage_open: dict[str, Any],
    f26b_summary: dict[str, Any],
    f26c_summary: dict[str, Any],
    rejection_audit: pd.DataFrame,
    repair_audit: pd.DataFrame,
    grok: dict[str, Any],
    local: dict[str, Any],
) -> dict[str, Any]:
    if local["judgment"] != "pass_closeout_ready(마감 준비 통과)":
        raise RuntimeError(f"Frontier26D closeout local checks failed: {json.dumps(local, ensure_ascii=False)}")
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
        "invalid_setup": INVALID_SETUP,
        "preserved_clue": PRESERVED_CLUE,
        "negative_memory": NEGATIVE_MEMORY,
        "next_hypothesis_clue": NEXT_HYPOTHESIS_CLUE,
        "runtime_probe_blocker": RUNTIME_PROBE_BLOCKER,
        "onnx_blocker": ONNX_BLOCKER,
        "stage_open": {
            "status": stage_open.get("status"),
            "judgment": stage_open.get("judgment"),
            "grok_classification": stage_open.get("grok", {}).get("classification", ""),
        },
        "f26b_summary": {
            "status": f26b_summary.get("status"),
            "judgment": f26b_summary.get("judgment"),
            "micro_pocket_rows": f26b_summary.get("micro_pocket_rows"),
            "joint_micro_pass_rows": f26b_summary.get("joint_micro_pass_rows"),
            "joint_union_attempt_rows": f26b_summary.get("joint_union_attempt_rows"),
            "joint_union_candidate_rows": f26b_summary.get("joint_union_candidate_rows"),
            "density_bridge_rows": f26b_summary.get("density_bridge_rows"),
            "scout_clue_rows": f26b_summary.get("scout_clue_rows"),
            "seed_surface_rows": f26b_summary.get("seed_surface_rows"),
            "handoff_candidate_rows": f26b_summary.get("handoff_candidate_rows"),
            "top10_f24b_overlap_count": f26b_summary.get("top10_f24b_overlap_count"),
            "top10_f25b_overlap_count": f26b_summary.get("top10_f25b_overlap_count"),
        },
        "f26c_summary": {
            "status": f26c_summary.get("status"),
            "judgment": f26c_summary.get("judgment"),
            "repair_decision": f26c_summary.get("repair_decision"),
            "diagnosis": f26c_summary.get("diagnosis", {}),
        },
        "rejection_audit_rows": int(len(rejection_audit)),
        "repair_audit_rows": int(len(repair_audit)),
        "grok_closeout": grok,
        "local_verification": local,
        "result_boundary": (
            "stage_closeout_invalid_setup_no_wfo_no_mt5_no_runtime_authority"
            "(단계 마감 무효 설정, WFO/MT5/런타임 권위 없음)"
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
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "invalid_setup.md", invalid_setup_text(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "preserved_clue.md", preserved_clue_text(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "negative_memory.md", negative_memory_text(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(final))
    f03b.write_text_sig(DECISION_PATH, decision_text(final))


def run_manifest(final: dict[str, Any]) -> dict[str, Any]:
    artifacts = [
        SCRIPT_PATH,
        F26A_SUMMARY,
        F26B_SUMMARY,
        F26B_MICRO_AUDIT,
        F26B_REJECTION_AUDIT,
        F26C_SUMMARY,
        F26C_REPAIR_AUDIT,
        GROK_STAGE_OPEN_PACKET / "metadata.json",
        GROK_CLOSEOUT_PACKET / "metadata.json",
        GROK_CLOSEOUT_RETRY_PACKET / "metadata.json",
        GROK_RECEIPT_PATH,
        REPORT_PATH,
        REQUIRED_GATE_AUDIT_PATH,
        STAGE_ROOT / "04_selected" / "invalid_setup.md",
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
            "invalid_setup": final["invalid_setup"],
            "preserved_clue": final["preserved_clue"],
            "negative_memory": final["negative_memory"],
            "runtime_probe_blocker": final["runtime_probe_blocker"],
            "onnx_blocker": final["onnx_blocker"],
        },
        "grok": {
            "stage_open_packet": GROK_STAGE_OPEN_PACKET.as_posix(),
            "stage_closeout_packet": GROK_CLOSEOUT_PACKET.as_posix(),
            "stage_closeout_retry_packet": GROK_CLOSEOUT_RETRY_PACKET.as_posix(),
            "closeout_classification": final["grok_closeout"]["classification"],
        },
        "compatibility": {"schema_version": "frontier26d_stage_closeout_v1", "mismatch_policy": "fail_fast(빠른 실패)"},
        "claim_boundary": final["claim_boundary"],
    }


def report_text(final: dict[str, Any]) -> str:
    f26b_summary = final["f26b_summary"]
    diagnosis = final["f26c_summary"].get("diagnosis", {})
    closest = diagnosis.get("closest_union_near_miss", {})
    return f"""# Frontier26D Stage Closeout Report(전선26D 단계 마감 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Action(행동): F26(전선26) joint micro satisfaction before union(합집합 전 미세 구간 합동 충족) 가설을 invalid setup(무효 설정)으로 closeout(마감)했습니다.

Effect(효과): 경성 component gate(구성 요소 게이트)가 union surface(합집합 표면)를 붕괴시킨 것을 기록하고, gate relaxation repair(게이트 완화 수리), MT5 runtime probe(MT5 런타임 탐침), ONNX(온엑스), WFO(워크포워드 최적화)를 모두 열지 않습니다.

Invalid setup(무효 설정): `{final['invalid_setup']}`

Preserved clue(보존 단서): `{final['preserved_clue']}`

Negative memory(부정 기억): `{final['negative_memory']}`

Runtime probe blocker(런타임 탐침 차단 사유): `{final['runtime_probe_blocker']}`

ONNX blocker(ONNX 차단 사유): `{final['onnx_blocker']}`

F26B micro/pass/attempt/union/density/scout/seed/handoff(전선26B 미세/통과/시도/합집합/빈도/탐색/씨앗/인계): `{f26b_summary['micro_pocket_rows']}` / `{f26b_summary['joint_micro_pass_rows']}` / `{f26b_summary['joint_union_attempt_rows']}` / `{f26b_summary['joint_union_candidate_rows']}` / `{f26b_summary['density_bridge_rows']}` / `{f26b_summary['scout_clue_rows']}` / `{f26b_summary['seed_surface_rows']}` / `{f26b_summary['handoff_candidate_rows']}`

Closest union near miss(가장 가까운 합집합 근접 실패): `{closest.get('micro_ids', '')}` with train PF/density/DD/overlap(학습 수익 팩터/빈도/손실폭/중복) `{fmt(closest.get('train_profit_factor'))}` / `{fmt(closest.get('train_trades_per_day'))}` / `{fmt(closest.get('train_dd_risk'))}` / `{fmt(closest.get('train_overlap_ratio'))}`.

Grok closeout classification(그록 마감 분류): `{final['grok_closeout']['classification']}`

Next hypothesis clue(다음 가설 단서): `{final['next_hypothesis_clue']}`

Next action(다음 행동): `{final['next_run_id']}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def grok_receipt(final: dict[str, Any]) -> str:
    grok = final["grok_closeout"]
    first = grok["first_packet"]
    return f"""# Frontier26D Grok Closeout Receipt(전선26D 그록 마감 영수증)

Trigger reason(트리거 이유): stage closeout(단계 마감)은 Grok review(그록 검토)가 필요했습니다.

First packet(첫 묶음): `{first['packet']}` classification(분류) `{first['classification']}`.

Effect(효과): 첫 묶음은 transport success(전송 성공)이었지만 verdict(판정)가 없어서 closeout gate(마감 게이트)로 쓰지 않았습니다.

Retry packet(재시도 묶음): `{grok['packet']}`

Prompt(프롬프트): `{grok['prompt']}`

Clean output(정리 출력): `{grok['clean_output']}`

Metadata(메타데이터): `{grok['metadata']}`

Prompt hash(프롬프트 해시): `{grok['prompt_hash']}`

Transport success(전송 성공): `{grok['success']}`, returncode(반환 코드) `{grok['returncode']}`, timed_out(시간 초과) `{grok['timed_out']}`

Codex classification(Codex 분류): `{grok['classification']}`

Accepted advice(수용 조언): invalid_setup closeout(무효 설정 마감), repair rejection(수리 거절), bounded clues(제한 단서), and no MT5/ONNX/WFO/authority claim(MT5/ONNX/WFO/권위 주장 없음).

Local verification(로컬 검증): `{final['local_verification']['judgment']}`
"""


def local_verification_text(final: dict[str, Any]) -> str:
    rows = []
    for key, value in final["local_verification"]["checks"].items():
        rows.append(f"- {key}: `{value}`")
    return f"""# Frontier26D Local Verification(전선26D 로컬 검증)

Judgment(판정): `{final['local_verification']['judgment']}`

{chr(10).join(rows)}

Effect(효과): Grok(그록) 조언을 자동 실행하지 않고, local files/registers/artifacts(로컬 파일/장부/산출물)로 재검증한 뒤 closeout(마감)했습니다.
"""


def required_gate_audit(final: dict[str, Any]) -> str:
    f26b_summary = final["f26b_summary"]
    return f"""# Frontier26 Required Gate Coverage Audit(전선26 필수 게이트 커버리지 감사)

- stage_open_grok_gate(단계 개방 그록 게이트): `{GROK_STAGE_OPEN_PACKET.as_posix()}` recorded(기록)
- proxy_gate(프록시 게이트): `{f26b.RUN_ID}` produced pass/attempt/union/density/scout/seed/handoff(통과/시도/합집합/빈도/탐색/씨앗/인계) `{f26b_summary['joint_micro_pass_rows']}/{f26b_summary['joint_union_attempt_rows']}/{f26b_summary['joint_union_candidate_rows']}/{f26b_summary['density_bridge_rows']}/{f26b_summary['scout_clue_rows']}/{f26b_summary['seed_surface_rows']}/{f26b_summary['handoff_candidate_rows']}`
- repair_decision_gate(수리 결정 게이트): `{f26c.RUN_ID}` recorded repair rejection(수리 거절 기록) `{final['f26c_summary']['repair_decision']}`
- stage_closeout_grok_gate(단계 마감 그록 게이트): retry packet(재시도 묶음) `{GROK_CLOSEOUT_RETRY_PACKET.as_posix()}` classification(분류) `{final['grok_closeout']['classification']}`
- closeout_gate(마감 게이트): `{final['judgment']}` with report(보고서) `{REPORT_PATH.as_posix()}`
- runtime_probe_gate(런타임 탐침 게이트): `{final['runtime_probe_blocker']}`
- onnx_gate(ONNX 게이트): `{final['onnx_blocker']}`
- tier_pair_record_gate(티어 쌍 기록 게이트): Tier A/Tier B/Tier A+B rows(티어 A/B/A+B 행) written(기록)
- final_claim_guard(최종 주장 방어): runtime authority/operating promotion/Goal Achieve(런타임 권위/운영 승격/목표 달성) not_claimed(주장 없음)
"""


def invalid_setup_text(final: dict[str, Any]) -> str:
    f26b_summary = final["f26b_summary"]
    return f"""# Frontier26 Invalid Setup(전선26 무효 설정)

Invalid setup(무효 설정): `{final['invalid_setup']}`

Evidence(근거): F26B(전선26B)는 source micro pockets(원천 미세 구간) `{f26b_summary['micro_pocket_rows']}`개 중 joint pass(합동 통과) `{f26b_summary['joint_micro_pass_rows']}`개를 남겼고, union attempt(합집합 시도) `{f26b_summary['joint_union_attempt_rows']}`개에서 valid union(유효 합집합) `{f26b_summary['joint_union_candidate_rows']}`개를 만들었습니다.

Effect(효과): locked hypothesis(잠긴 가설)는 유효 프록시 표면을 만들지 못했으므로 WFO/MT5/ONNX(워크포워드/MT5/ONNX)로 넘기지 않습니다.
"""


def preserved_clue_text(final: dict[str, Any]) -> str:
    return f"""# Frontier26 Preserved Clue(전선26 보존 단서)

Preserved clue(보존 단서): `{final['preserved_clue']}`

Evidence(근거): three micro pockets(미세 구간 3개)는 hard joint gate(경성 합동 게이트)를 통과했습니다.

Use boundary(사용 경계): reference only(참조 전용). This is not baseline/promotion/runtime authority(기준선/승격/런타임 권위 아님).
"""


def negative_memory_text(final: dict[str, Any]) -> str:
    return f"""# Frontier26 Negative Memory(전선26 부정 기억)

Negative memory(부정 기억): `{final['negative_memory']}`

Why failed(실패 이유): hard component gate(경성 구성 게이트)는 유효 union candidate(합집합 후보)를 0개로 만들었습니다. Repair(수리)는 gate relaxation(게이트 완화)이 필요했으므로 실행하지 않았습니다.

Do not repeat(반복 금지): Do not reopen F26 by simply relaxing density/DD/overlap caps(빈도/손실폭/중복 상한을 단순 완화해 F26 재개 금지). A soft penalty version(연성 페널티 버전)은 only as new frontier hypothesis(새 전선 가설로만) 다룹니다.
"""


def selection_status(final: dict[str, Any]) -> str:
    return f"""# Frontier26 Selection Status(전선26 선택 상태)

Updated(갱신): {final['created_at_utc']}

Selection(선택): no selected baseline/completion/promotion/runtime authority(선택 기준선/완성/승격/런타임 권위 없음).

Stage closeout(단계 마감): `{RUN_ID}`

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Invalid setup(무효 설정): `{final['invalid_setup']}`

Preserved clue(보존 단서): `{final['preserved_clue']}`

Negative memory(부정 기억): `{final['negative_memory']}`

Runtime probe blocker(런타임 탐침 차단 사유): `{final['runtime_probe_blocker']}`

ONNX blocker(ONNX 차단 사유): `{final['onnx_blocker']}`

Next action(다음 행동): `{final['next_run_id']}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 not_claimed(주장 없음)입니다.
"""


def decision_text(final: dict[str, Any]) -> str:
    return f"""# Decision: Close Frontier26 Joint Micro Satisfaction ONNX Scout(결정: 전선26 미세 구간 합동 충족 ONNX 탐색 마감)

Date(날짜): 2026-06-14

Decision(결정): Close F26(전선26)를 invalid_setup(무효 설정)으로 닫습니다.

Effect(효과): F26(전선26)에서 completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)를 주장하지 않고, 다음 frontier(다음 전선)를 새 가설로 시작합니다.

Invalid setup(무효 설정): `{final['invalid_setup']}`

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
    f26b_summary = final["f26b_summary"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "stage_closeout(단계 마감)",
        "family": "publish_handoff(게시/인계)",
        "work_family": "publish_handoff(게시/인계)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"invalid={final['invalid_setup']};negative={final['negative_memory']};next={final['next_run_id']}",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": final["next_run_id"],
        "claim_boundary": final["result_boundary"],
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": final["created_at_utc"],
        "primary_kpi": f"pass={f26b_summary['joint_micro_pass_rows']};union={f26b_summary['joint_union_candidate_rows']};seed={f26b_summary['seed_surface_rows']};handoff={f26b_summary['handoff_candidate_rows']}",
        "guardrail_kpi": "closeout_invalid_setup_no_wfo_no_mt5_no_authority(마감 무효 설정, WFO/MT5/권위 없음)",
        "external_verification_status": final["runtime_probe_blocker"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "result_path": REPORT_PATH.as_posix(),
    }


def ledger_rows(final: dict[str, Any]) -> list[dict[str, Any]]:
    f26b_summary = final["f26b_summary"]
    primary = {
        "ledger_row_id": f"{RUN_ID}__tier_a_stage_closeout",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__tier_a_stage_closeout",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "Tier A separate(티어 A 분리)",
        "tier_scope": "Tier A(티어 A)",
        "kpi_scope": "stage_closeout_invalid_setup_not_runtime(단계 마감 무효 설정, 런타임 아님)",
        "scoreboard_lane": "stage_closeout(단계 마감)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": f"pass={f26b_summary['joint_micro_pass_rows']};attempt={f26b_summary['joint_union_attempt_rows']};union={f26b_summary['joint_union_candidate_rows']};seed={f26b_summary['seed_surface_rows']};handoff={f26b_summary['handoff_candidate_rows']}",
        "guardrail_kpi": "no_wfo_no_mt5_no_runtime_authority(WFO/MT5/런타임 권위 없음)",
        "external_verification_status": final["runtime_probe_blocker"],
        "notes": f"{final['invalid_setup']};{final['negative_memory']};{final['onnx_blocker']}",
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
        f"- {final['created_at_utc']}: `{RUN_ID}` closed Frontier26(전선26 마감). "
        f"Effect(효과): invalid setup(무효 설정) `{final['invalid_setup']}` and negative memory(부정 기억) `{final['negative_memory']}` recorded; next run(다음 실행) `{final['next_run_id']}`.\n"
    )


def idea_registry_entry(final: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR26-JOINT-MICRO-SATISFACTION-BEFORE-UNION-ONNX-SCOUT`: `{RUN_ID}` closed as invalid_setup(무효 설정). "
        f"Effect(효과): do not repeat hard gate relaxation repair(경성 게이트 완화 수리 반복 금지); next clue(다음 단서) `{final['next_hypothesis_clue']}`.\n"
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
    f26b_summary = final["f26b_summary"]
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

Action(행동): F26(전선26) joint micro satisfaction before union(합집합 전 미세 구간 합동 충족)을 invalid setup(무효 설정)으로 closeout(마감)했습니다.

Effect(효과): hard component gate(경성 구성 게이트)가 union surface(합집합 표면)를 0개로 붕괴시킨 것을 기록하고, repair/MT5/ONNX/WFO(수리/MT5/ONNX/WFO)를 열지 않습니다.

F26B micro/pass/attempt/union/seed/handoff(전선26B 미세/통과/시도/합집합/씨앗/인계): `{f26b_summary['micro_pocket_rows']}` / `{f26b_summary['joint_micro_pass_rows']}` / `{f26b_summary['joint_union_attempt_rows']}` / `{f26b_summary['joint_union_candidate_rows']}` / `{f26b_summary['seed_surface_rows']}` / `{f26b_summary['handoff_candidate_rows']}`

Invalid setup(무효 설정): `{final['invalid_setup']}`

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
