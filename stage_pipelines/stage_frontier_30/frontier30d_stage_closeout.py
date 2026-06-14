from __future__ import annotations

import hashlib
import json
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
from stage_pipelines.stage_frontier_30 import frontier30b_train_density_preserving_preselector_before_loss_veto_proxy_scout as f30b
from stage_pipelines.stage_frontier_30 import frontier30c_density_preserving_preselector_repair_or_closeout_decision as f30c


STAGE_ID = f30c.STAGE_ID
RUN_ID = "frontier30D_stage_closeout_density_preserving_preselector_v1"
RUN_NUMBER = "frontier30D"
PARENT_RUN_ID = f30c.RUN_ID
STATUS = "closed_preserved_clue_negative_memory_density_preselector_scout_only_no_handoff"
JUDGMENT = "preserved_clue_negative_memory(보존 단서+부정 기억)"
NEXT_STAGE_ID = "stage_frontier_31__exit_shape_pivot_for_density_preserved_source_scout_pf_lift_onnx_scout"
NEXT_RUN_ID = "frontier31A_stage_open_exit_shape_pivot_for_density_preserved_source_scout_pf_lift_hypothesis_design_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
GROK_RECEIPT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_grok_closeout_receipt.md"
LOCAL_VERIFICATION_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_local_verification.md"
REQUIRED_GATE_AUDIT_PATH = STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md"
DECISION_PATH = Path("docs/decisions/2026-06-14_stage_frontier_30_density_preselector_closeout.md")
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_30/frontier30d_stage_closeout.py")

F30A_SUMMARY = STAGE_ROOT / "02_runs" / f30b.f30a.RUN_ID / "stage_open_summary.json"
F30B_SUMMARY = STAGE_ROOT / "02_runs" / f30b.RUN_ID / "final_summary.json"
F30B_CANDIDATE_SUMMARY = STAGE_ROOT / "02_runs" / f30b.RUN_ID / "density_preselector_candidate_summary.csv"
F30C_SUMMARY = STAGE_ROOT / "02_runs" / f30c.RUN_ID / "final_summary.json"
F30C_REPAIR_AUDIT = STAGE_ROOT / "02_runs" / f30c.RUN_ID / "repair_rejection_audit.csv"
GROK_STAGE_OPEN_PACKET = Path("docs/agent_control/grok_reviews/2026-06-14_frontier30_stage_open/small_review")
GROK_CLOSEOUT_PACKET = Path("docs/agent_control/grok_reviews/2026-06-14_frontier30_stage_closeout/small_review")
GROK_CLOSEOUT_RETRY_PACKET = Path("docs/agent_control/grok_reviews/2026-06-14_frontier30_stage_closeout/small_review_retry")

RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")
NEGATIVE_RESULT_REGISTER = Path("docs/registers/negative_result_register.md")
CHANGELOG = Path("docs/workspace/changelog.md")
WORKSPACE_STATE = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE = Path("docs/context/current_working_state.md")

PRESERVED_CLUE = f30c.PRESERVED_CLUE
NEGATIVE_MEMORY = f30c.NEGATIVE_MEMORY
NEXT_HYPOTHESIS_CLUE = f30c.NEXT_HYPOTHESIS_CLUE
RUNTIME_PROBE_STATUS = "runtime_probe_out_of_scope_by_claim_scout_only_no_handoff"
ONNX_BLOCKER = "onnx_branch_unattempted_no_handoff_candidate_after_f30c_repair_decision"


def main() -> int:
    ensure_dirs()
    normalize_grok_markdown()
    created_at = utc_now()
    f30a_summary = read_json(F30A_SUMMARY)
    f30b_summary = read_json(F30B_SUMMARY)
    f30c_summary = read_json(F30C_SUMMARY)
    candidate_summary = pd.read_csv(io_path(F30B_CANDIDATE_SUMMARY))
    repair_audit = pd.read_csv(io_path(F30C_REPAIR_AUDIT))
    grok = load_grok_closeout()
    local = validate_context(f30a_summary, f30b_summary, f30c_summary, candidate_summary, repair_audit, grok)
    final = build_final(created_at, f30a_summary, f30b_summary, f30c_summary, candidate_summary, repair_audit, grok, local)
    write_outputs(final)
    update_registries(final)
    update_current_truth(final)
    print(json.dumps(json_ready({
        "status": final["status"],
        "judgment": final["judgment"],
        "run_id": RUN_ID,
        "preserved_clue": final["preserved_clue"],
        "negative_memory": final["negative_memory"],
        "runtime_probe_status": final["runtime_probe_status"],
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
    initial_metadata = read_json(GROK_CLOSEOUT_PACKET / "metadata.json")
    initial_output = read_text(GROK_CLOSEOUT_PACKET / "clean_output.md")
    retry_metadata = read_json(GROK_CLOSEOUT_RETRY_PACKET / "metadata.json")
    retry_output = read_text(GROK_CLOSEOUT_RETRY_PACKET / "clean_output.md")
    lowered = retry_output.lower()
    accepted = (
        "verdict:** accepted" in lowered or "verdict: accepted" in lowered
    ) and (
        "closeout_class_ok:** yes" in lowered or "closeout_class_ok: yes" in lowered
    ) and (
        "repair_rejection_ok:** yes" in lowered or "repair_rejection_ok: yes" in lowered
    ) and (
        "runtime_probe_status_ok:** yes" in lowered or "runtime_probe_status_ok: yes" in lowered
    ) and (
        "next_clue_ok:** yes" in lowered or "next_clue_ok: yes" in lowered
    )
    return {
        "initial_packet": GROK_CLOSEOUT_PACKET.as_posix(),
        "initial_success": bool(initial_metadata.get("success")),
        "initial_format_missing": "verdict" not in initial_output.lower(),
        "retry_packet": GROK_CLOSEOUT_RETRY_PACKET.as_posix(),
        "prompt": (GROK_CLOSEOUT_RETRY_PACKET / "prompt.md").as_posix(),
        "clean_output": (GROK_CLOSEOUT_RETRY_PACKET / "clean_output.md").as_posix(),
        "metadata": (GROK_CLOSEOUT_RETRY_PACKET / "metadata.json").as_posix(),
        "prompt_hash": retry_metadata.get("prompt_hash", ""),
        "success": bool(retry_metadata.get("success")),
        "returncode": retry_metadata.get("returncode"),
        "timed_out": bool(retry_metadata.get("timed_out")),
        "unexpected_top_level_artifacts": retry_metadata.get("unexpected_top_level_artifacts", []),
        "classification": "accepted_retry_after_initial_format_miss" if accepted else "needs_local_verification",
        "accepted": accepted,
        "output_excerpt": retry_output[:3600],
    }


def validate_context(
    f30a_summary: dict[str, Any],
    f30b_summary: dict[str, Any],
    f30c_summary: dict[str, Any],
    candidate_summary: pd.DataFrame,
    repair_audit: pd.DataFrame,
    grok: dict[str, Any],
) -> dict[str, Any]:
    workspace = read_text(WORKSPACE_STATE)
    diagnosis = f30c_summary["diagnosis"]
    checks = {
        "workspace_current_frontier30c_or_frontier30d": f"current_run_id: {f30c.RUN_ID}" in workspace
        or f"current_run_id: {RUN_ID}" in workspace,
        "workspace_next_run_frontier30d_or_frontier31a": f"next_run_id: {RUN_ID}" in workspace
        or f"next_run_id: {NEXT_RUN_ID}" in workspace,
        "f30a_grok_stage_open_accepted": f30a_summary.get("grok", {}).get("classification", "").startswith("accepted"),
        "f30a_exit_shape_reference_only": f30a_summary.get("locks", {}).get("exit_shape_pivot_role") == "reference_fallback_only_not_active_changed_variable",
        "f30b_scout_only_no_seed_handoff": int(f30b_summary.get("scout_clue_rows", -1)) == 5
        and int(f30b_summary.get("seed_surface_rows", -1)) == 0
        and int(f30b_summary.get("handoff_candidate_rows", -1)) == 0,
        "f30b_veto_branch_scout_zero": int(f30b_summary.get("veto_branch_scout_rows", -1)) == 0,
        "f30b_candidate_rows_match": len(candidate_summary) == int(f30b_summary.get("candidate_rows", -1)),
        "f30c_repair_rejected": f30c_summary.get("repair_decision") == "reject_repair_and_closeout",
        "f30c_valid_repair_zero": int(diagnosis.get("valid_train_density_repair_opportunity_rows", -1)) == 0,
        "f30c_seed_handoff_zero": int(diagnosis.get("seed_surface_rows", -1)) == 0
        and int(diagnosis.get("handoff_candidate_rows", -1)) == 0,
        "repair_audit_rows_match": len(repair_audit) == int(diagnosis.get("candidate_rows", -1)),
        "grok_retry_success": grok["success"] and grok["returncode"] == 0 and not grok["timed_out"],
        "grok_retry_accepted": grok["accepted"],
        "grok_no_unexpected_top_level_artifacts": not grok["unexpected_top_level_artifacts"],
        "runtime_probe_no_handoff": f30c_summary.get("runtime_probe_status") == RUNTIME_PROBE_STATUS,
        "onnx_unattempted_no_handoff": f30c_summary.get("onnx_status") == ONNX_BLOCKER,
    }
    return {
        "checks": checks,
        "judgment": "pass_closeout_ready_with_grok_retry" if all(checks.values()) else "needs_manual_review",
        "grok_initial_boundary": "transport_success_but_format_missing_not_used_as_authoritative_verdict",
    }


def build_final(
    created_at: str,
    f30a_summary: dict[str, Any],
    f30b_summary: dict[str, Any],
    f30c_summary: dict[str, Any],
    candidate_summary: pd.DataFrame,
    repair_audit: pd.DataFrame,
    grok: dict[str, Any],
    local: dict[str, Any],
) -> dict[str, Any]:
    if local["judgment"] != "pass_closeout_ready_with_grok_retry":
        raise RuntimeError(f"Frontier30D closeout local checks failed: {json.dumps(local, ensure_ascii=False)}")
    best_forward = f30b_summary.get("best_forward_readonly_candidate", {})
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
        "runtime_probe_status": RUNTIME_PROBE_STATUS,
        "onnx_blocker": ONNX_BLOCKER,
        "f30a_summary": {
            "status": f30a_summary.get("status"),
            "judgment": f30a_summary.get("judgment"),
            "grok_classification": f30a_summary.get("grok", {}).get("classification"),
            "active_changed_variable": f30a_summary.get("locks", {}).get("active_changed_variable"),
        },
        "f30b_summary": {
            "status": f30b_summary.get("status"),
            "judgment": f30b_summary.get("judgment"),
            "source_rows": f30b_summary.get("source_rows"),
            "preselected_source_rows": f30b_summary.get("preselected_source_rows"),
            "candidate_rows": f30b_summary.get("candidate_rows"),
            "density_bridge_rows": f30b_summary.get("density_bridge_rows"),
            "scout_clue_rows": f30b_summary.get("scout_clue_rows"),
            "seed_surface_rows": f30b_summary.get("seed_surface_rows"),
            "handoff_candidate_rows": f30b_summary.get("handoff_candidate_rows"),
            "source_branch_scout_rows": f30b_summary.get("source_branch_scout_rows"),
            "veto_branch_scout_rows": f30b_summary.get("veto_branch_scout_rows"),
            "best_forward_readonly_candidate_id": f30b_summary.get("best_forward_readonly_candidate_id"),
            "best_forward_readonly_candidate": best_forward,
        },
        "f30c_summary": {
            "status": f30c_summary.get("status"),
            "judgment": f30c_summary.get("judgment"),
            "repair_decision": f30c_summary.get("repair_decision"),
            "diagnosis": f30c_summary.get("diagnosis", {}),
        },
        "candidate_summary_rows": int(len(candidate_summary)),
        "repair_audit_rows": int(len(repair_audit)),
        "grok_closeout": grok,
        "local_verification": local,
        "result_boundary": "stage_closeout_preserved_clue_negative_memory_no_wfo_no_mt5_no_onnx_no_authority",
        "claim_boundary": {claim: "not_claimed" for claim in f03b.FORBIDDEN_CLAIMS},
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
        F30A_SUMMARY,
        F30B_SUMMARY,
        F30B_CANDIDATE_SUMMARY,
        F30C_SUMMARY,
        F30C_REPAIR_AUDIT,
        GROK_CLOSEOUT_RETRY_PACKET / "metadata.json",
        GROK_CLOSEOUT_RETRY_PACKET / "clean_output.md",
        RUN_ROOT / "final_closeout_summary.json",
        REPORT_PATH,
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
        "claim_boundary": final["claim_boundary"],
    }


def update_registries(final: dict[str, Any]) -> None:
    f03b.upsert_csv(RUN_REGISTRY, "run_id", run_registry_row(final))
    for row in ledger_rows(final):
        f03b.upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
        f30b.f30a.upsert_csv_io(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", row)
    f03b.append_once(CHANGELOG, RUN_ID, changelog_entry(final))
    f03b.append_once(IDEA_REGISTRY, RUN_ID, idea_registry_entry(final))
    f03b.append_once(NEGATIVE_RESULT_REGISTER, RUN_ID, negative_register_entry(final))


def run_registry_row(final: dict[str, Any]) -> dict[str, Any]:
    f30b_summary = final["f30b_summary"]
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
        "primary_kpi": f"candidate={f30b_summary['candidate_rows']};scout={f30b_summary['scout_clue_rows']};seed={f30b_summary['seed_surface_rows']};handoff={f30b_summary['handoff_candidate_rows']}",
        "guardrail_kpi": "closeout_preserved_clue_negative_memory_no_wfo_no_mt5_no_authority",
        "external_verification_status": final["runtime_probe_status"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "result_path": REPORT_PATH.as_posix(),
    }


def ledger_rows(final: dict[str, Any]) -> list[dict[str, Any]]:
    f30b_summary = final["f30b_summary"]
    primary = {
        "ledger_row_id": f"{RUN_ID}__stage_closeout",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__stage_closeout",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "stage_closeout(단계 마감)",
        "tier_scope": "Tier A(티어 A)",
        "kpi_scope": "stage_closeout_no_runtime(단계 마감, 런타임 아님)",
        "scoreboard_lane": "stage_closeout(단계 마감)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": f"candidate={f30b_summary['candidate_rows']};scout={f30b_summary['scout_clue_rows']};seed={f30b_summary['seed_surface_rows']};handoff={f30b_summary['handoff_candidate_rows']}",
        "guardrail_kpi": "preserved_clue_negative_memory_no_wfo_no_mt5_no_authority",
        "external_verification_status": final["runtime_probe_status"],
        "notes": f"next={final['next_run_id']};preserved={final['preserved_clue']};negative={final['negative_memory']}",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "run_family": "stage_closeout(단계 마감)",
    }
    return [primary]


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
        f"next_stage_id: {NEXT_STAGE_ID}",
        f"next_run_id: {NEXT_RUN_ID}",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "goal_achieve: not_claimed",
        f"updated_at_utc: '{final['created_at_utc']}'",
        "",
    ])


def report_text(final: dict[str, Any]) -> str:
    b = final["f30b_summary"]
    c = final["f30c_summary"]["diagnosis"]
    best = b["best_forward_readonly_candidate"]
    return f"""# Frontier30D Stage Closeout Report(전선30D 단계 마감 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Action(행동): F30(전선30) train-only density-preserving preselector(학습 전용 밀도 보존 사전 선택기) 가설을 preserved clue + negative memory(보존 단서+부정 기억)로 closeout(마감)했습니다.

Effect(효과): preselector(사전 선택기)는 source branch scout(원천 분기 탐색) `5`개를 회복했지만 seed/handoff(씨앗/인계)는 `0/0`이고, veto branch scout(차단 분기 탐색)는 `0`개라 MT5/ONNX/WFO(MT5/온엑스/워크포워드 최적화)는 실행하지 않았습니다.

Preserved clue(보존 단서): `{final['preserved_clue']}`

Negative memory(부정 기억): `{final['negative_memory']}`

F30B source/preselected/candidate(전선30B 원천/사전 선택/후보): `{b['source_rows']}` / `{b['preselected_source_rows']}` / `{b['candidate_rows']}`

F30B density/scout/seed/handoff(전선30B 밀도/탐색/씨앗/인계): `{b['density_bridge_rows']}` / `{b['scout_clue_rows']}` / `{b['seed_surface_rows']}` / `{b['handoff_candidate_rows']}`

Best read-only forward candidate(최상 읽기 전용 전진 후보): `{b['best_forward_readonly_candidate_id']}` with validation/OOS PF-density-DD(검증/표본외 수익 팩터-밀도-손실폭) `{fmt(best.get('validation_profit_factor'))}/{fmt(best.get('validation_trades_per_day'))}/{fmt(best.get('validation_dd_risk'))}` and `{fmt(best.get('oos_profit_factor'))}/{fmt(best.get('oos_trades_per_day'))}/{fmt(best.get('oos_dd_risk'))}`.

F30C diagnosis(전선30C 진단): near_seed_pf_band(씨앗 근접 PF 구간) `{c['near_seed_pf_band_rows']}`, scout_pf_blocked_seed(탐색 PF 부족 씨앗 차단) `{c['scout_pf_blocked_seed_rows']}`, valid repair(유효 수리) `{c['valid_train_density_repair_opportunity_rows']}`.

Grok closeout classification(그록 마감 분류): `{final['grok_closeout']['classification']}`.

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

ONNX blocker(ONNX 차단 사유): `{final['onnx_blocker']}`

Next hypothesis clue(다음 가설 단서): `{final['next_hypothesis_clue']}`

Next action(다음 행동): `{final['next_run_id']}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def grok_receipt(final: dict[str, Any]) -> str:
    grok = final["grok_closeout"]
    return f"""# Frontier30D Grok Closeout Receipt(전선30D 그록 마감 영수증)

Initial packet(초기 묶음): `{grok['initial_packet']}`

Initial result(초기 결과): transport success(전송 성공) `{grok['initial_success']}`, format missing(형식 누락) `{grok['initial_format_missing']}`. 이 결과는 authoritative verdict(권위 판정)로 쓰지 않았습니다.

Retry packet(재시도 묶음): `{grok['retry_packet']}`

Prompt(프롬프트): `{grok['prompt']}`

Clean output(정리 출력): `{grok['clean_output']}`

Metadata(메타데이터): `{grok['metadata']}`

Classification(분류): `{grok['classification']}`

Accepted advice(수용 조언): closeout class(마감 분류), repair rejection(수리 거절), runtime probe out-of-scope(런타임 탐침 범위 밖), ONNX unattempted(온엑스 미시도), next clue(다음 단서)를 수용했습니다.

Rejected advice(거절 조언): forward read-only best(읽기 전용 전진 최상)를 baseline/promotion/handoff(기준선/승격/인계)로 승격하는 경로를 거절했습니다.

Local verification(로컬 검증): `{final['local_verification']['judgment']}`
"""


def local_verification_text(final: dict[str, Any]) -> str:
    rows = [f"- {key}: `{value}`" for key, value in final["local_verification"]["checks"].items()]
    return f"""# Frontier30D Local Verification(전선30D 로컬 검증)

Judgment(판정): `{final['local_verification']['judgment']}`

{chr(10).join(rows)}

Effect(효과): Grok(그록) 재시도 verdict(판정)를 로컬 파일, 장부, 후보 수치와 대조한 뒤에만 closeout(마감)을 기록했습니다.
"""


def required_gate_audit(final: dict[str, Any]) -> str:
    b = final["f30b_summary"]
    c = final["f30c_summary"]["diagnosis"]
    return f"""# Frontier30 Required Gate Coverage Audit(전선30 필수 게이트 커버리지 감사)

- stage_open_grok_gate(단계 개방 그록 게이트): `{GROK_STAGE_OPEN_PACKET.as_posix()}` recorded(기록)
- proxy_gate(프록시 게이트): `{f30b.RUN_ID}` produced density/scout/seed/handoff(밀도/탐색/씨앗/인계) `{b['density_bridge_rows']}/{b['scout_clue_rows']}/{b['seed_surface_rows']}/{b['handoff_candidate_rows']}`
- repair_decision_gate(수리 결정 게이트): `{f30c.RUN_ID}` recorded valid_train_density_repair_opportunity_rows(유효 학습 밀도 수리 기회 행) `{c['valid_train_density_repair_opportunity_rows']}`
- stage_closeout_grok_gate(단계 마감 그록 게이트): retry packet(재시도 묶음) `{GROK_CLOSEOUT_RETRY_PACKET.as_posix()}` classification(분류) `{final['grok_closeout']['classification']}`
- closeout_gate(마감 게이트): `{final['judgment']}` with report(보고서) `{REPORT_PATH.as_posix()}`
- runtime_probe_gate(런타임 탐침 게이트): `{final['runtime_probe_status']}`
- onnx_gate(ONNX 게이트): `{final['onnx_blocker']}`
- tier_pair_record_gate(티어 쌍 기록 게이트): Tier B(티어 B)는 F30B에서 missing_required(필수 누락), Tier A+B(티어 A+B)는 out_of_scope_by_claim(주장 범위 밖)
- final_claim_guard(최종 주장 방어): runtime authority/operating promotion/Goal Achieve(런타임 권위/운영 승격/목표 달성) not_claimed(주장 없음)
"""


def preserved_clue_text(final: dict[str, Any]) -> str:
    b = final["f30b_summary"]
    return f"""# Frontier30 Preserved Clue(전선30 보존 단서)

Preserved clue(보존 단서): `{final['preserved_clue']}`

Evidence(근거): F30B(전선30B)는 train-only preselector(학습 전용 사전 선택기)로 source branch scout(원천 분기 탐색) `{b['source_branch_scout_rows']}`개를 회복했습니다.

Use boundary(사용 경계): reference only(참조 전용). This is not baseline/promotion/runtime authority(기준선/승격/런타임 권위 아님).
"""


def negative_memory_text(final: dict[str, Any]) -> str:
    b = final["f30b_summary"]
    c = final["f30c_summary"]["diagnosis"]
    return f"""# Frontier30 Negative Memory(전선30 부정 기억)

Negative memory(부정 기억): `{final['negative_memory']}`

Why failed(실패 이유): veto branch scout(차단 분기 탐색)는 `{b['veto_branch_scout_rows']}`개이고 seed/handoff(씨앗/인계)는 `{b['seed_surface_rows']}/{b['handoff_candidate_rows']}`개였습니다.

Repair result(수리 결과): valid_train_density_repair_opportunity_rows(유효 학습 밀도 수리 기회 행) `{c['valid_train_density_repair_opportunity_rows']}`.

Do not repeat(반복 금지): F30 안에서 exit-shape pivot(청산 형태 전환)을 켜거나 F29 threshold(임계값)를 완화해 scout(탐색)를 seed/handoff(씨앗/인계)로 과장하지 않습니다.
"""


def selection_status(final: dict[str, Any]) -> str:
    return f"""# Frontier30 Selection Status(전선30 선택 상태)

Updated(갱신): {final['created_at_utc']}

Selection(선택): no selected baseline/completion/promotion/runtime authority(선택 기준선/완성/승격/런타임 권위 없음).

Stage closeout(단계 마감): `{RUN_ID}`

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Preserved clue(보존 단서): `{final['preserved_clue']}`

Negative memory(부정 기억): `{final['negative_memory']}`

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

ONNX blocker(ONNX 차단 사유): `{final['onnx_blocker']}`

Next action(다음 행동): `{final['next_run_id']}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 not_claimed(주장 없음)입니다.
"""


def decision_text(final: dict[str, Any]) -> str:
    return f"""# Decision(결정): Close Frontier30 Density Preserving Preselector Scout(전선30 밀도 보존 사전 선택기 탐색 마감)

Date(날짜): 2026-06-14

Decision(결정): Close(마감) `{STAGE_ID}` as preserved_clue_negative_memory(보존 단서+부정 기억).

Effect(효과): train-only density preselector(학습 전용 밀도 사전 선택기)는 일부 scout(탐색)를 회복했지만 seed/handoff(씨앗/인계)를 만들지 못했으므로, 다음 frontier(전선)는 exit-shape pivot(청산 형태 전환) 단서로 넘어갑니다.

Preserved clue(보존 단서): `{final['preserved_clue']}`

Negative memory(부정 기억): `{final['negative_memory']}`

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

ONNX blocker(ONNX 차단): `{final['onnx_blocker']}`

Next run(다음 실행): `{final['next_run_id']}`
"""


def current_working_state(final: dict[str, Any]) -> str:
    b = final["f30b_summary"]
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

## Active Stage(현재 단계)

- stage(단계): `{STAGE_ID}`
- latest run(최근 실행): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- next stage(다음 단계): `{NEXT_STAGE_ID}`
- next run(다음 실행): `{NEXT_RUN_ID}`

## Current Truth(현재 진실)

Action(행동): F30(전선30)을 train-only density-preserving preselector(학습 전용 밀도 보존 사전 선택기) scout(탐색)으로 닫았습니다.

Effect(효과): source/preselected/candidate(원천/사전 선택/후보) `234/160/245`, density/scout/seed/handoff(밀도/탐색/씨앗/인계) `{b['density_bridge_rows']}/{b['scout_clue_rows']}/{b['seed_surface_rows']}/{b['handoff_candidate_rows']}`를 근거로, 다음 전선은 exit-shape pivot(청산 형태 전환) 단서로 넘어갑니다.

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

ONNX blocker(ONNX 차단 사유): `{final['onnx_blocker']}`

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def changelog_entry(final: dict[str, Any]) -> str:
    b = final["f30b_summary"]
    return (
        f"- {final['created_at_utc']}: `{RUN_ID}` closed Frontier30 density-preserving preselector scout(전선30 밀도 보존 사전 선택기 탐색 마감). "
        f"Effect(효과): scout={b['scout_clue_rows']}, seed={b['seed_surface_rows']}, handoff={b['handoff_candidate_rows']}, next=`{NEXT_RUN_ID}`.\n"
    )


def idea_registry_entry(final: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR30-TRAIN-DENSITY-PRESERVING-PRESELECTOR-BEFORE-LOSS-VETO-ONNX-SCOUT`: `{RUN_ID}` closed with preserved clue(보존 단서) `{final['preserved_clue']}` and negative memory(부정 기억) `{final['negative_memory']}`. "
        "Effect(효과): next frontier clue(다음 전선 단서)는 exit-shape pivot(청산 형태 전환)입니다.\n"
    )


def negative_register_entry(final: dict[str, Any]) -> str:
    return (
        f"- `{RUN_ID}`: {final['negative_memory']} | Evidence(근거): F30B scout/seed/handoff(전선30B 탐색/씨앗/인계) "
        f"{final['f30b_summary']['scout_clue_rows']}/{final['f30b_summary']['seed_surface_rows']}/{final['f30b_summary']['handoff_candidate_rows']}; "
        f"valid repair(유효 수리) {final['f30c_summary']['diagnosis']['valid_train_density_repair_opportunity_rows']}.\n"
    )


def artifact_identity(path: Path) -> dict[str, str]:
    return {"path": path.as_posix(), "sha256": sha256_io(path) if path_exists(path) else "missing"}


def sha256_io(path: Path) -> str:
    return hashlib.sha256(io_path(path).read_bytes()).hexdigest()


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def fmt(value: Any) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return "NA"
    return f"{number:.3f}"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
