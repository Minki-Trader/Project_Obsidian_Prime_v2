from __future__ import annotations

import csv
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
from stage_pipelines.stage_frontier_31 import frontier31b_return_space_exit_shape_proxy_scout as f31b
from stage_pipelines.stage_frontier_31 import frontier31c_return_space_exit_shape_repair_or_closeout_decision as f31c


STAGE_ID = f31c.STAGE_ID
RUN_ID = "frontier31D_stage_closeout_return_space_exit_shape_v1"
RUN_NUMBER = "frontier31D"
PARENT_RUN_ID = f31c.RUN_ID
STATUS = "closed_preserved_clue_return_space_exit_shape_handoff_surface_executable_mapping_required"
JUDGMENT = "preserved_clue_negative_memory(보존 단서+부정 기억)"
NEXT_STAGE_ID = "stage_frontier_32__executable_sl_tp_mapping_for_return_space_exit_shape_handoff_surface_onnx_scout"
NEXT_RUN_ID = "frontier32A_stage_open_executable_sl_tp_mapping_for_return_space_exit_shape_handoff_surface_hypothesis_design_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
GROK_RECEIPT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_grok_closeout_receipt.md"
LOCAL_VERIFICATION_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_local_verification.md"
REQUIRED_GATE_AUDIT_PATH = STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md"
DECISION_PATH = Path("docs/decisions/2026-06-14_stage_frontier_31_return_space_exit_shape_closeout.md")
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_31/frontier31d_stage_closeout.py")

F31A_SUMMARY = STAGE_ROOT / "02_runs" / f31b.f31a.RUN_ID / "stage_open_summary.json"
F31B_SUMMARY = STAGE_ROOT / "02_runs" / f31b.RUN_ID / "final_summary.json"
F31B_CANDIDATE_SUMMARY = STAGE_ROOT / "02_runs" / f31b.RUN_ID / "return_space_exit_shape_candidate_summary.csv"
F31C_SUMMARY = STAGE_ROOT / "02_runs" / f31c.RUN_ID / "final_summary.json"
F31C_MAPPING_QUEUE = STAGE_ROOT / "02_runs" / f31c.RUN_ID / "executable_mapping_queue.csv"
F31C_TOP_MAPPING_QUEUE = STAGE_ROOT / "02_runs" / f31c.RUN_ID / "top_executable_mapping_queue.csv"
GROK_STAGE_OPEN_PACKET = Path("docs/agent_control/grok_reviews/2026-06-14_frontier31_stage_open/small_review")
GROK_CLOSEOUT_PACKET = Path("docs/agent_control/grok_reviews/2026-06-14_frontier31_stage_closeout/small_review")

RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")
NEGATIVE_RESULT_REGISTER = Path("docs/registers/negative_result_register.md")
CHANGELOG = Path("docs/workspace/changelog.md")
WORKSPACE_STATE = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE = Path("docs/context/current_working_state.md")

PRESERVED_CLUE = f31c.PRESERVED_CLUE
NEGATIVE_MEMORY = f31c.NEGATIVE_MEMORY
NEXT_HYPOTHESIS_CLUE = f31c.NEXT_HYPOTHESIS_CLUE
RUNTIME_PROBE_STATUS = f31c.RUNTIME_PROBE_STATUS
ONNX_BLOCKER = f31c.ONNX_BLOCKER


def main() -> int:
    ensure_dirs()
    normalize_grok_markdown()
    created_at = utc_now()
    f31a_summary = read_json(F31A_SUMMARY)
    f31b_summary = read_json(F31B_SUMMARY)
    f31c_summary = read_json(F31C_SUMMARY)
    candidate_summary = pd.read_csv(io_path(F31B_CANDIDATE_SUMMARY))
    mapping_queue = pd.read_csv(io_path(F31C_MAPPING_QUEUE))
    top_mapping_queue = pd.read_csv(io_path(F31C_TOP_MAPPING_QUEUE))
    grok = load_grok_closeout()
    local = validate_context(
        f31a_summary,
        f31b_summary,
        f31c_summary,
        candidate_summary,
        mapping_queue,
        top_mapping_queue,
        grok,
    )
    final = build_final(
        created_at,
        f31a_summary,
        f31b_summary,
        f31c_summary,
        candidate_summary,
        mapping_queue,
        top_mapping_queue,
        grok,
        local,
    )
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
        "next_stage_id": NEXT_STAGE_ID,
        "next_run_id": NEXT_RUN_ID,
        "report": REPORT_PATH.as_posix(),
    }), ensure_ascii=False, indent=2))
    return 0


def ensure_dirs() -> None:
    for path in (RUN_ROOT, STAGE_ROOT / "03_reviews", STAGE_ROOT / "04_selected", DECISION_PATH.parent):
        io_path(path).mkdir(parents=True, exist_ok=True)


def normalize_grok_markdown() -> None:
    for name in ("input_prompt.md", "prompt.md", "clean_output.md"):
        path = GROK_CLOSEOUT_PACKET / name
        if path_exists(path):
            text = io_path(path).read_text(encoding="utf-8-sig")
            f03b.write_text_sig(path, text.rstrip() + "\n")


def load_grok_closeout() -> dict[str, Any]:
    metadata = read_json(GROK_CLOSEOUT_PACKET / "metadata.json")
    output = read_text(GROK_CLOSEOUT_PACKET / "clean_output.md")
    lowered = output.lower()
    accepted = (
        ("verdict:** accepted" in lowered or "verdict: accepted" in lowered)
        and ("closeout_class_ok:** yes" in lowered or "closeout_class_ok: yes" in lowered)
        and ("repair_decision_ok:** yes" in lowered or "repair_decision_ok: yes" in lowered)
        and ("runtime_probe_status_ok:** yes" in lowered or "runtime_probe_status_ok: yes" in lowered)
        and ("next_clue_ok:** yes" in lowered or "next_clue_ok: yes" in lowered)
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
        "classification": "accepted_preserved_clue_closeout" if accepted else "needs_local_verification",
        "accepted": accepted,
        "output_excerpt": output[:3600],
    }


def validate_context(
    f31a_summary: dict[str, Any],
    f31b_summary: dict[str, Any],
    f31c_summary: dict[str, Any],
    candidate_summary: pd.DataFrame,
    mapping_queue: pd.DataFrame,
    top_mapping_queue: pd.DataFrame,
    grok: dict[str, Any],
) -> dict[str, Any]:
    workspace = read_text(WORKSPACE_STATE)
    diagnosis = f31c_summary["diagnosis"]
    checks = {
        "workspace_current_frontier31c_or_frontier31d": f"current_run_id: {f31c.RUN_ID}" in workspace
        or f"current_run_id: {RUN_ID}" in workspace,
        "workspace_next_run_frontier31d_or_frontier32a": f"next_run_id: {RUN_ID}" in workspace
        or f"next_run_id: {NEXT_RUN_ID}" in workspace,
        "f31a_grok_stage_open_accepted": f31a_summary.get("grok", {}).get("classification", "").startswith("accepted"),
        "f31b_handoff_surface_present": int(f31b_summary.get("handoff_candidate_rows", -1)) == 16,
        "f31b_realistic_handoff_rows_present": int(f31b_summary.get("realistic_handoff_candidate_rows", -1)) == 16,
        "f31b_executable_rows_zero": int(f31b_summary.get("executable_handoff_candidate_rows", -1)) == 0,
        "f31b_best_candidate_f31b_0013": f31b_summary.get("best_forward_readonly_candidate_id") == "f31b_0013",
        "f31c_repair_queue_decision": f31c_summary.get("repair_decision")
        == "preserve_handoff_surface_and_queue_executable_mapping_repair",
        "f31c_mapping_queue_rows": int(diagnosis.get("mapping_queue_rows", -1)) == 16,
        "f31c_top_six_rows": int(diagnosis.get("top_six_repair_seed_rows", -1)) == 6,
        "candidate_summary_rows_match": len(candidate_summary) == int(f31b_summary.get("summary_rows", -1)),
        "mapping_queue_rows_match": len(mapping_queue) == int(diagnosis.get("mapping_queue_rows", -1)),
        "top_mapping_queue_rows_match": len(top_mapping_queue) == 6,
        "mapping_queue_head_matches_best_forward": bool(len(mapping_queue))
        and str(mapping_queue.iloc[0]["candidate_id"]) == str(f31b_summary.get("best_forward_readonly_candidate_id", "")),
        "mapping_queue_all_runtime_blocked_now": bool(len(mapping_queue))
        and (~mapping_queue["runtime_attempt_allowed_now"].astype(bool)).all(),
        "grok_closeout_success": grok["success"] and grok["returncode"] == 0 and not grok["timed_out"],
        "grok_closeout_accepted": grok["accepted"],
        "grok_no_unexpected_top_level_artifacts": not grok["unexpected_top_level_artifacts"],
        "runtime_probe_status_matches_closeout": f31c_summary.get("runtime_probe_status") == RUNTIME_PROBE_STATUS,
        "onnx_blocker_matches_closeout": f31c_summary.get("onnx_blocker") == ONNX_BLOCKER,
    }
    return {
        "checks": checks,
        "judgment": "pass_closeout_ready_with_grok" if all(checks.values()) else "needs_manual_review",
        "tier_b_boundary": "Tier B missing_required recorded in F31B ledger; F31 closeout remains Tier A proxy only.",
    }


def build_final(
    created_at: str,
    f31a_summary: dict[str, Any],
    f31b_summary: dict[str, Any],
    f31c_summary: dict[str, Any],
    candidate_summary: pd.DataFrame,
    mapping_queue: pd.DataFrame,
    top_mapping_queue: pd.DataFrame,
    grok: dict[str, Any],
    local: dict[str, Any],
) -> dict[str, Any]:
    if local["judgment"] != "pass_closeout_ready_with_grok":
        raise RuntimeError(f"Frontier31D closeout local checks failed: {json.dumps(local, ensure_ascii=False)}")
    best_forward = f31b_summary.get("best_forward_readonly_candidate", {})
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
        "f31a_summary": {
            "status": f31a_summary.get("status"),
            "judgment": f31a_summary.get("judgment"),
            "grok_classification": f31a_summary.get("grok", {}).get("classification"),
            "active_changed_variable": f31a_summary.get("locks", {}).get("active_changed_variable"),
        },
        "f31b_summary": {
            "status": f31b_summary.get("status"),
            "judgment": f31b_summary.get("judgment"),
            "fixed_scout_rows": f31b_summary.get("fixed_scout_rows"),
            "variant_rows": f31b_summary.get("variant_rows"),
            "density_bridge_rows": f31b_summary.get("density_bridge_rows"),
            "scout_clue_rows": f31b_summary.get("scout_clue_rows"),
            "seed_surface_rows": f31b_summary.get("seed_surface_rows"),
            "handoff_candidate_rows": f31b_summary.get("handoff_candidate_rows"),
            "realistic_handoff_candidate_rows": f31b_summary.get("realistic_handoff_candidate_rows"),
            "executable_handoff_candidate_rows": f31b_summary.get("executable_handoff_candidate_rows"),
            "best_forward_readonly_candidate_id": f31b_summary.get("best_forward_readonly_candidate_id"),
            "best_forward_readonly_candidate": best_forward,
        },
        "f31c_summary": {
            "status": f31c_summary.get("status"),
            "judgment": f31c_summary.get("judgment"),
            "repair_decision": f31c_summary.get("repair_decision"),
            "diagnosis": f31c_summary.get("diagnosis", {}),
            "top_mapping_queue_candidate_ids": f31c_summary.get("top_mapping_queue_candidate_ids", []),
        },
        "candidate_summary_rows": int(len(candidate_summary)),
        "mapping_queue_rows": int(len(mapping_queue)),
        "top_mapping_queue_rows": int(len(top_mapping_queue)),
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
        F31A_SUMMARY,
        F31B_SUMMARY,
        F31B_CANDIDATE_SUMMARY,
        F31C_SUMMARY,
        F31C_MAPPING_QUEUE,
        F31C_TOP_MAPPING_QUEUE,
        GROK_CLOSEOUT_PACKET / "metadata.json",
        GROK_CLOSEOUT_PACKET / "clean_output.md",
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
        f31b.f31a.upsert_csv_io(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", row)
    f03b.append_once(CHANGELOG, RUN_ID, changelog_entry(final))
    f03b.append_once(IDEA_REGISTRY, RUN_ID, idea_registry_entry(final))
    f03b.append_once(NEGATIVE_RESULT_REGISTER, RUN_ID, negative_register_entry(final))


def run_registry_row(final: dict[str, Any]) -> dict[str, Any]:
    b = final["f31b_summary"]
    c = final["f31c_summary"]["diagnosis"]
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
        "primary_kpi": f"handoff={b['handoff_candidate_rows']};realistic={b['realistic_handoff_candidate_rows']};executable={b['executable_handoff_candidate_rows']};queue={c['mapping_queue_rows']}",
        "guardrail_kpi": "closeout_preserved_clue_no_wfo_no_mt5_no_onnx_no_authority",
        "external_verification_status": final["runtime_probe_status"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "result_path": REPORT_PATH.as_posix(),
    }


def ledger_rows(final: dict[str, Any]) -> list[dict[str, Any]]:
    b = final["f31b_summary"]
    c = final["f31c_summary"]["diagnosis"]
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
        "primary_kpi": f"handoff={b['handoff_candidate_rows']};realistic={b['realistic_handoff_candidate_rows']};queue={c['mapping_queue_rows']}",
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
    b = final["f31b_summary"]
    c = final["f31c_summary"]["diagnosis"]
    best = b["best_forward_readonly_candidate"]
    return f"""# Frontier31D Stage Closeout Report(전선31D 단계 마감 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Action(행동): F31(전선31) return-space exit-shape pivot(수익률 공간 청산 형태 전환)을 preserved clue + negative memory(보존 단서+부정 기억)로 closeout(마감)했습니다.

Effect(효과): fixed entry scout(고정 진입 탐색)에서 realistic handoff surface(현실적 인계 표면) `{b['realistic_handoff_candidate_rows']}`개를 만들었지만, executable exit representation(실행 가능한 청산 표현)이 `{b['executable_handoff_candidate_rows']}`개라 MT5/ONNX/WFO(엠티5/온엑스/워크포워드 최적화)는 실행하지 않았습니다.

Preserved clue(보존 단서): `{final['preserved_clue']}`

Negative memory(부정 기억): `{final['negative_memory']}`

F31B fixed/variant rows(전선31B 고정/변형 행): `{b['fixed_scout_rows']}` / `{b['variant_rows']}`

F31B density/scout/seed/handoff(전선31B 밀도/탐색/씨앗/인계): `{b['density_bridge_rows']}` / `{b['scout_clue_rows']}` / `{b['seed_surface_rows']}` / `{b['handoff_candidate_rows']}`

Best read-only forward candidate(최상 읽기 전용 전진 후보): `{b['best_forward_readonly_candidate_id']}` with validation/OOS PF-density-DD(검증/표본외 수익 팩터-밀도-손실폭) `{fmt(best.get('validation_profit_factor'))}/{fmt(best.get('validation_trades_per_day'))}/{fmt(best.get('validation_dd_risk'))}` and `{fmt(best.get('oos_profit_factor'))}/{fmt(best.get('oos_trades_per_day'))}/{fmt(best.get('oos_dd_risk'))}`.

F31C repair queue(전선31C 수리 큐): mapping queue(매핑 큐) `{c['mapping_queue_rows']}`, top six repair seed(상위 6개 수리 씨앗) `{c['top_six_repair_seed_rows']}`.

Grok closeout classification(그록 마감 분류): `{final['grok_closeout']['classification']}`.

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

ONNX blocker(온엑스 차단 사유): `{final['onnx_blocker']}`

Next hypothesis clue(다음 가설 단서): `{final['next_hypothesis_clue']}`

Next action(다음 행동): `{final['next_run_id']}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def grok_receipt(final: dict[str, Any]) -> str:
    grok = final["grok_closeout"]
    return f"""# Frontier31D Grok Closeout Receipt(전선31D 그록 마감 영수증)

Trigger reason(호출 이유): goal(목표)이 stage closeout(단계 마감)마다 Grok second opinion(그록 2차 의견)을 요구합니다.

Review size(검토 크기): small review(소규모 검토)

Packet(묶음): `{grok['packet']}`

Prompt(프롬프트): `{grok['prompt']}`

Clean output(정리 출력): `{grok['clean_output']}`

Metadata(메타데이터): `{grok['metadata']}`

Classification(분류): `{grok['classification']}`

Accepted advice(수용 조언): preserved clue + negative memory(보존 단서+부정 기억) closeout(마감), executable mapping repair queue(실행 매핑 수리 큐), runtime out-of-scope(런타임 범위 밖), ONNX unattempted(온엑스 미시도)를 수용했습니다.

Rejected advice(거절 조언): F31B proxy(전선31B 프록시)를 completion/baseline/promotion/runtime authority(완성/기준선/승격/런타임 권위)로 승격하는 경로는 없습니다.

Local verification(로컬 검증): `{final['local_verification']['judgment']}`
"""


def local_verification_text(final: dict[str, Any]) -> str:
    rows = [f"- {key}: `{value}`" for key, value in final["local_verification"]["checks"].items()]
    return f"""# Frontier31D Local Verification(전선31D 로컬 검증)

Judgment(판정): `{final['local_verification']['judgment']}`

{chr(10).join(rows)}

Tier boundary(티어 경계): {final['local_verification']['tier_b_boundary']}

Effect(효과): Grok(그록) 조언을 자동 실행하지 않고, 로컬 summary(요약), queue(큐), ledger(장부), runtime boundary(런타임 경계)를 대조한 뒤 closeout(마감)을 기록했습니다.
"""


def required_gate_audit(final: dict[str, Any]) -> str:
    b = final["f31b_summary"]
    c = final["f31c_summary"]["diagnosis"]
    return f"""# Frontier31 Required Gate Coverage Audit(전선31 필수 게이트 커버리지 감사)

- stage_open_grok_gate(단계 개방 그록 게이트): `{GROK_STAGE_OPEN_PACKET.as_posix()}` recorded(기록)
- proxy_gate(프록시 게이트): `{f31b.RUN_ID}` produced density/scout/seed/handoff(밀도/탐색/씨앗/인계) `{b['density_bridge_rows']}/{b['scout_clue_rows']}/{b['seed_surface_rows']}/{b['handoff_candidate_rows']}`
- repair_decision_gate(수리 결정 게이트): `{f31c.RUN_ID}` recorded mapping_queue_rows(매핑 큐 행) `{c['mapping_queue_rows']}` and executable_handoff(실행 가능 인계) `{b['executable_handoff_candidate_rows']}`
- stage_closeout_grok_gate(단계 마감 그록 게이트): `{GROK_CLOSEOUT_PACKET.as_posix()}` classification(분류) `{final['grok_closeout']['classification']}`
- closeout_gate(마감 게이트): `{final['judgment']}` with report(보고서) `{REPORT_PATH.as_posix()}`
- runtime_probe_gate(런타임 탐침 게이트): `{final['runtime_probe_status']}`
- onnx_gate(온엑스 게이트): `{final['onnx_blocker']}`
- tier_pair_record_gate(티어 쌍 기록 게이트): Tier A(티어 A) proxy(프록시) recorded(기록), Tier B(티어 B) `missing_required` in F31B ledger(전선31B 장부), Tier A+B(티어 A+B) `out_of_scope_by_claim` in F31B ledger(전선31B 장부)
- final_claim_guard(최종 주장 방어): runtime authority/operating promotion/Goal Achieve(런타임 권위/운영 승격/목표 달성)는 not_claimed(주장 없음)
"""


def preserved_clue_text(final: dict[str, Any]) -> str:
    b = final["f31b_summary"]
    best = b["best_forward_readonly_candidate"]
    return f"""# Frontier31 Preserved Clue(전선31 보존 단서)

Preserved clue(보존 단서): `{final['preserved_clue']}`

Evidence(근거): F31B(전선31B)는 realistic handoff candidate(현실적 인계 후보) `{b['realistic_handoff_candidate_rows']}`개를 만들었습니다. Best read-only forward candidate(최상 읽기 전용 전진 후보) `{b['best_forward_readonly_candidate_id']}`는 validation/OOS PF-density-DD(검증/표본외 수익 팩터-밀도-손실폭) `{fmt(best.get('validation_profit_factor'))}/{fmt(best.get('validation_trades_per_day'))}/{fmt(best.get('validation_dd_risk'))}` and `{fmt(best.get('oos_profit_factor'))}/{fmt(best.get('oos_trades_per_day'))}/{fmt(best.get('oos_dd_risk'))}`입니다.

Use boundary(사용 경계): reference only(참조 전용). This is not baseline/promotion/runtime authority(기준선/승격/런타임 권위 아님).
"""


def negative_memory_text(final: dict[str, Any]) -> str:
    b = final["f31b_summary"]
    return f"""# Frontier31 Negative Memory(전선31 부정 기억)

Negative memory(부정 기억): `{final['negative_memory']}`

Why limited(제한 이유): return-space clipping(수익률 공간 클립)은 intrabar path(봉내 경로)와 MT5 SL/TP probe(엠티5 손절/익절 탐침)를 아직 통과하지 않았습니다.

Runtime result(런타임 결과): executable handoff candidate(실행 가능 인계 후보) `{b['executable_handoff_candidate_rows']}`개.

Do not repeat(반복 금지): return-space proxy(수익률 공간 프록시)를 MT5 runtime authority(엠티5 런타임 권위)나 ONNX readiness(온엑스 준비)로 과장하지 않습니다.
"""


def selection_status(final: dict[str, Any]) -> str:
    return f"""# Frontier31 Selection Status(전선31 선택 상태)

Updated(갱신): {final['created_at_utc']}

Selection(선택): no selected baseline/completion/promotion/runtime authority(선택 기준선/완성/승격/런타임 권위 없음).

Stage closeout(단계 마감): `{RUN_ID}`

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Preserved clue(보존 단서): `{final['preserved_clue']}`

Negative memory(부정 기억): `{final['negative_memory']}`

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

ONNX blocker(온엑스 차단 사유): `{final['onnx_blocker']}`

Next action(다음 행동): `{final['next_run_id']}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 not_claimed(주장 없음)입니다.
"""


def decision_text(final: dict[str, Any]) -> str:
    return f"""# Decision(결정): Close Frontier31 Return-Space Exit Shape Scout(전선31 수익률 공간 청산 형태 탐색 마감)

Date(날짜): 2026-06-14

Decision(결정): Close(마감) `{STAGE_ID}` as preserved_clue_negative_memory(보존 단서+부정 기억).

Effect(효과): return-space exit-shape proxy(수익률 공간 청산 형태 프록시)는 강한 handoff surface(인계 표면)를 남겼지만, executable SL/TP mapping(실행 가능한 손절/익절 매핑)과 MT5 runtime probe(엠티5 런타임 탐침)는 다음 frontier(전선)로 넘깁니다.

Preserved clue(보존 단서): `{final['preserved_clue']}`

Negative memory(부정 기억): `{final['negative_memory']}`

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

ONNX blocker(온엑스 차단): `{final['onnx_blocker']}`

Next run(다음 실행): `{final['next_run_id']}`
"""


def current_working_state(final: dict[str, Any]) -> str:
    b = final["f31b_summary"]
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

Action(행동): F31(전선31)은 return-space exit-shape pivot(수익률 공간 청산 형태 전환)을 preserved clue + negative memory(보존 단서+부정 기억)로 닫았습니다.

Effect(효과): density/scout/seed/handoff(밀도/탐색/씨앗/인계) `{b['density_bridge_rows']}/{b['scout_clue_rows']}/{b['seed_surface_rows']}/{b['handoff_candidate_rows']}`와 realistic handoff(현실적 인계) `{b['realistic_handoff_candidate_rows']}`개를 보존하고, next frontier(다음 전선)는 executable SL/TP mapping(실행 가능한 손절/익절 매핑)을 다룹니다.

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

ONNX blocker(온엑스 차단 사유): `{final['onnx_blocker']}`

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def changelog_entry(final: dict[str, Any]) -> str:
    b = final["f31b_summary"]
    return (
        f"- {final['created_at_utc']}: `{RUN_ID}` closed Frontier31 return-space exit-shape scout(전선31 수익률 공간 청산 형태 탐색 마감). "
        f"Effect(효과): handoff={b['handoff_candidate_rows']}, realistic={b['realistic_handoff_candidate_rows']}, executable={b['executable_handoff_candidate_rows']}, next=`{NEXT_RUN_ID}`.\n"
    )


def idea_registry_entry(final: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR31-RETURN-SPACE-EXIT-SHAPE-PF-LIFT-ONNX-SCOUT`: `{RUN_ID}` closed with preserved clue(보존 단서) `{final['preserved_clue']}` and negative memory(부정 기억) `{final['negative_memory']}`. "
        "Effect(효과): next frontier clue(다음 전선 단서)는 executable SL/TP mapping(실행 가능한 손절/익절 매핑)입니다.\n"
    )


def negative_register_entry(final: dict[str, Any]) -> str:
    b = final["f31b_summary"]
    return (
        f"- `{RUN_ID}`: {final['negative_memory']} | Evidence(근거): F31B handoff/realistic/executable(전선31B 인계/현실적/실행 가능) "
        f"{b['handoff_candidate_rows']}/{b['realistic_handoff_candidate_rows']}/{b['executable_handoff_candidate_rows']}; "
        f"runtime_probe_status(런타임 탐침 상태) {final['runtime_probe_status']}.\n"
    )


def artifact_identity(path: Path) -> dict[str, str]:
    return {"path": path.as_posix(), "sha256": sha256_io(path) if path_exists(path) else "missing"}


def sha256_io(path: Path) -> str:
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


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
    if not math.isfinite(number):
        return "NA"
    return f"{number:.3f}"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
