from __future__ import annotations

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
from stage_pipelines.stage_frontier_32 import frontier32b_executable_sl_tp_path_proxy_scout as f32b
from stage_pipelines.stage_frontier_32 import frontier32c_executable_sl_tp_mapping_repair_or_closeout_decision as f32c


STAGE_ID = f32c.STAGE_ID
RUN_ID = "frontier32D_stage_closeout_executable_sl_tp_mapping_v1"
RUN_NUMBER = "frontier32D"
PARENT_RUN_ID = f32c.RUN_ID
STATUS = "closed_negative_memory_executable_sl_tp_mapping_path_proxy_failed_no_runtime_authority"
JUDGMENT = "negative_memory(F32 실행 가능한 손절/익절 매핑 경로 프록시 실패)"
NEXT_STAGE_ID = "stage_frontier_33__path_native_exit_label_or_mfe_mae_surface_for_density_edge_onnx_scout"
NEXT_RUN_ID = "frontier33A_stage_open_path_native_exit_label_or_mfe_mae_surface_hypothesis_design_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
GROK_RECEIPT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_grok_closeout_receipt.md"
LOCAL_VERIFICATION_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_local_verification.md"
REQUIRED_GATE_AUDIT_PATH = STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md"
DECISION_PATH = Path("docs/decisions/2026-06-14_stage_frontier_32_executable_sl_tp_mapping_closeout.md")
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_32/frontier32d_stage_closeout.py")

F32A_SUMMARY = STAGE_ROOT / "02_runs" / f32b.f32a.RUN_ID / "stage_open_summary.json"
F32B_SUMMARY = STAGE_ROOT / "02_runs" / f32b.RUN_ID / "final_summary.json"
F32B_CANDIDATE_SUMMARY = STAGE_ROOT / "02_runs" / f32b.RUN_ID / "path_candidate_summary.csv"
F32C_SUMMARY = STAGE_ROOT / "02_runs" / f32c.RUN_ID / "final_summary.json"
GROK_CLOSEOUT_PACKET = f32c.GROK_CLOSEOUT_PACKET

RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")
NEGATIVE_RESULT_REGISTER = Path("docs/registers/negative_result_register.md")
CHANGELOG = Path("docs/workspace/changelog.md")
WORKSPACE_STATE = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE = Path("docs/context/current_working_state.md")


def main() -> int:
    ensure_dirs()
    normalize_grok_markdown()
    created_at = utc_now()
    f32a_summary = read_json(F32A_SUMMARY)
    f32b_summary = read_json(F32B_SUMMARY)
    f32c_summary = read_json(F32C_SUMMARY)
    candidates = pd.read_csv(io_path(F32B_CANDIDATE_SUMMARY))
    grok = load_grok_closeout()
    local = validate_context(f32a_summary, f32b_summary, f32c_summary, candidates, grok)
    final = build_final(created_at, f32a_summary, f32b_summary, f32c_summary, candidates, grok, local)
    write_outputs(final)
    update_registries(final)
    update_current_truth(final)
    print(json.dumps(json_ready({
        "status": final["status"],
        "judgment": final["judgment"],
        "run_id": RUN_ID,
        "closeout_class": final["closeout_class"],
        "negative_memory": final["negative_memory"],
        "runtime_probe_status": final["runtime_probe_status"],
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
        and ("runtime_probe_status_ok:** yes" in lowered or "runtime_probe_status_ok: yes" in lowered)
        and ("mt5_deferral_ok:** yes" in lowered or "mt5_deferral_ok: yes" in lowered)
        and ("negative_memory_ok:** yes" in lowered or "negative_memory_ok: yes" in lowered)
        and ("next_hypothesis_ok:** yes" in lowered or "next_hypothesis_ok: yes" in lowered)
        and ("claim_boundary_ok:** yes" in lowered or "claim_boundary_ok: yes" in lowered)
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
        "classification": "accepted_negative_memory_closeout" if accepted else "needs_local_verification",
        "accepted": accepted,
        "output_excerpt": output[:3600],
    }


def validate_context(
    f32a_summary: dict[str, Any],
    f32b_summary: dict[str, Any],
    f32c_summary: dict[str, Any],
    candidates: pd.DataFrame,
    grok: dict[str, Any],
) -> dict[str, Any]:
    workspace = read_text(WORKSPACE_STATE)
    checks = {
        "workspace_current_frontier32c_or_frontier32d": f"current_stage_id: {STAGE_ID}" in workspace
        and (f"current_run_id: {f32c.RUN_ID}" in workspace or f"current_run_id: {RUN_ID}" in workspace),
        "workspace_next_frontier32d_or_frontier33a": f"next_run_id: {RUN_ID}" in workspace
        or f"next_run_id: {NEXT_RUN_ID}" in workspace,
        "f32a_grok_stage_open_accepted": f32a_summary.get("grok", {}).get("classification", "").startswith("accepted"),
        "f32a_lock_changed_variable": f32a_summary.get("locks", {}).get("active_changed_variable")
        == "fixed_log_return_caps_to_price_path_sl_tp_representation",
        "f32b_no_path_scout": int(f32b_summary.get("path_scout_clue_rows", -1)) == 0,
        "f32b_no_path_seed": int(f32b_summary.get("path_seed_surface_rows", -1)) == 0,
        "f32b_no_runtime_candidate": int(f32b_summary.get("runtime_probe_candidate_rows", -1)) == 0,
        "f32b_runtime_ineligible": f32b_summary.get("runtime_probe_status") == f32c.RUNTIME_PROBE_STATUS,
        "f32c_closeout_decision": f32c_summary.get("repair_decision") == f32c.REPAIR_DECISION,
        "f32c_closeout_class_negative": f32c_summary.get("closeout_class_preview") == f32c.CLOSEOUT_CLASS,
        "candidate_summary_rows_match": len(candidates) == int(f32b_summary.get("summary_rows", -1)),
        "all_candidate_runtime_flags_false": not bool(candidates["runtime_probe_candidate_flag"].astype(bool).any()),
        "grok_closeout_success": grok["success"] and grok["returncode"] == 0 and not grok["timed_out"],
        "grok_closeout_accepted": grok["accepted"],
        "grok_no_unexpected_top_level_artifacts": not grok["unexpected_top_level_artifacts"],
        "claim_boundary_not_claimed": all(value == "not_claimed" for value in f32c_summary.get("claim_boundary", {}).values()),
    }
    return {
        "checks": checks,
        "judgment": "pass_closeout_ready_with_grok" if all(checks.values()) else "needs_manual_review",
        "tier_b_boundary": "Tier B missing_required remains recorded in F32B ledger; F32 closeout is Tier A path proxy only.",
    }


def build_final(
    created_at: str,
    f32a_summary: dict[str, Any],
    f32b_summary: dict[str, Any],
    f32c_summary: dict[str, Any],
    candidates: pd.DataFrame,
    grok: dict[str, Any],
    local: dict[str, Any],
) -> dict[str, Any]:
    if local["judgment"] != "pass_closeout_ready_with_grok":
        raise RuntimeError(f"Frontier32D closeout local checks failed: {json.dumps(local, ensure_ascii=False)}")
    best = f32b_summary.get("best_path_candidate", {})
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
        "closeout_class": f32c.CLOSEOUT_CLASS,
        "negative_memory": f32c.NEGATIVE_MEMORY,
        "useful_observation": f32c.USEFUL_OBSERVATION,
        "next_hypothesis_clue": f32c.NEXT_HYPOTHESIS_CLUE,
        "runtime_probe_status": f32c.RUNTIME_PROBE_STATUS,
        "onnx_blocker": f32c.ONNX_BLOCKER,
        "f32a_summary": {
            "status": f32a_summary.get("status"),
            "judgment": f32a_summary.get("judgment"),
            "grok_classification": f32a_summary.get("grok", {}).get("classification"),
            "active_changed_variable": f32a_summary.get("locks", {}).get("active_changed_variable"),
        },
        "f32b_summary": {
            "status": f32b_summary.get("status"),
            "judgment": f32b_summary.get("judgment"),
            "queue_rows": f32b_summary.get("queue_rows"),
            "path_candidate_rows": f32b_summary.get("path_candidate_rows"),
            "path_scout_clue_rows": f32b_summary.get("path_scout_clue_rows"),
            "path_seed_surface_rows": f32b_summary.get("path_seed_surface_rows"),
            "runtime_probe_candidate_rows": f32b_summary.get("runtime_probe_candidate_rows"),
            "runtime_strict_candidate_rows": f32b_summary.get("runtime_strict_candidate_rows"),
            "best_path_candidate_id": f32b_summary.get("best_path_candidate_id"),
            "best_path_candidate": best,
        },
        "f32c_summary": {
            "status": f32c_summary.get("status"),
            "judgment": f32c_summary.get("judgment"),
            "repair_decision": f32c_summary.get("repair_decision"),
            "diagnosis": f32c_summary.get("diagnosis", {}),
        },
        "candidate_summary_rows": int(len(candidates)),
        "density_bridge_rows": int(candidates["path_density_bridge_flag"].astype(bool).sum()),
        "grok_closeout": grok,
        "local_verification": local,
        "result_boundary": "stage_closeout_negative_memory_no_wfo_no_mt5_no_onnx_no_authority",
        "claim_boundary": {claim: "not_claimed" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(final: dict[str, Any]) -> None:
    write_json(RUN_ROOT / "final_closeout_summary.json", final)
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(final))
    f03b.write_text_sig(REPORT_PATH, report_text(final))
    f03b.write_text_sig(GROK_RECEIPT_PATH, grok_receipt(final))
    f03b.write_text_sig(LOCAL_VERIFICATION_PATH, local_verification_text(final))
    f03b.write_text_sig(REQUIRED_GATE_AUDIT_PATH, required_gate_audit(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "negative_memory.md", negative_memory_text(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(final))
    f03b.write_text_sig(DECISION_PATH, decision_text(final))


def run_manifest(final: dict[str, Any]) -> dict[str, Any]:
    artifacts = [
        SCRIPT_PATH,
        F32A_SUMMARY,
        F32B_SUMMARY,
        F32B_CANDIDATE_SUMMARY,
        F32C_SUMMARY,
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
        f32b.f32a.f31d.f31b.f31a.upsert_csv_io(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", row)
    f03b.append_once(CHANGELOG, RUN_ID, changelog_entry(final))
    f03b.append_once(IDEA_REGISTRY, RUN_ID, idea_registry_entry(final))
    f03b.append_once(NEGATIVE_RESULT_REGISTER, RUN_ID, negative_register_entry(final))


def run_registry_row(final: dict[str, Any]) -> dict[str, Any]:
    b = final["f32b_summary"]
    best = b["best_path_candidate"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "stage_closeout(단계 마감)",
        "family": "publish_handoff(게시/인계)",
        "work_family": "publish_handoff(게시/인계)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"negative={final['negative_memory']};next={final['next_run_id']}",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": final["next_run_id"],
        "claim_boundary": final["result_boundary"],
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": final["created_at_utc"],
        "primary_kpi": f"path_scout={b['path_scout_clue_rows']};seed={b['path_seed_surface_rows']};runtime_candidate={b['runtime_probe_candidate_rows']};best_oos_pf={fmt(best.get('oos_profit_factor'))}",
        "guardrail_kpi": "stage_closeout_negative_memory_no_mt5_no_onnx_no_authority",
        "external_verification_status": final["runtime_probe_status"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "result_path": REPORT_PATH.as_posix(),
    }


def ledger_rows(final: dict[str, Any]) -> list[dict[str, Any]]:
    b = final["f32b_summary"]
    best = b["best_path_candidate"]
    return [{
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
        "primary_kpi": f"path_scout={b['path_scout_clue_rows']};seed={b['path_seed_surface_rows']};runtime_candidate={b['runtime_probe_candidate_rows']};best_oos_pf={fmt(best.get('oos_profit_factor'))}",
        "guardrail_kpi": "negative_memory_no_runtime_authority",
        "external_verification_status": final["runtime_probe_status"],
        "notes": f"next={final['next_run_id']};negative={final['negative_memory']}",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "run_family": "stage_closeout(단계 마감)",
    }]


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
    b = final["f32b_summary"]
    best = b["best_path_candidate"]
    return f"""# Frontier32D Stage Closeout Report(전선32D 단계 마감 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Action(행동): F32(전선32) executable SL/TP mapping(실행 가능한 손절/익절 매핑)을 negative memory(부정 기억)로 closeout(마감)했습니다.

Effect(효과): return-space handoff surface(수익률 공간 인계 표면)를 raw high/low path(원천 고가/저가 경로)로 번역하면 PF(수익 팩터)와 DD(손실폭)가 목표 근처에 남지 않는다는 실패 기억을 저장하고, 다음 stage(단계)는 path-native exit label(경로 기반 청산 라벨) 쪽 새 가설로 출발합니다.

Closeout class(마감 분류): `{final['closeout_class']}`

Negative memory(부정 기억): `{final['negative_memory']}`

Useful observation(유용 관찰): `{final['useful_observation']}`

Best path candidate(최상 경로 후보): `{b['best_path_candidate_id']}`

Best validation PF/density/DD(최상 검증 수익 팩터/밀도/손실폭): `{fmt(best.get('validation_profit_factor'))}` / `{fmt(best.get('validation_trades_per_day'))}` / `{fmt(best.get('validation_dd_risk'))}`

Best OOS PF/density/DD(최상 표본외 수익 팩터/밀도/손실폭): `{fmt(best.get('oos_profit_factor'))}` / `{fmt(best.get('oos_trades_per_day'))}` / `{fmt(best.get('oos_dd_risk'))}`

Path scout/seed/runtime candidate(경로 탐색/씨앗/런타임 후보): `{b['path_scout_clue_rows']}` / `{b['path_seed_surface_rows']}` / `{b['runtime_probe_candidate_rows']}`

Grok closeout classification(그록 마감 분류): `{final['grok_closeout']['classification']}`

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

ONNX blocker(온엑스 차단 사유): `{final['onnx_blocker']}`

Next hypothesis clue(다음 가설 단서): `{final['next_hypothesis_clue']}`

Next action(다음 행동): `{final['next_run_id']}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def grok_receipt(final: dict[str, Any]) -> str:
    grok = final["grok_closeout"]
    return f"""# Frontier32D Grok Closeout Receipt(전선32D 그록 마감 영수증)

Trigger reason(호출 이유): goal(목표)이 stage closeout(단계 마감)마다 Grok second opinion(그록 2차 의견)을 요구합니다.

Review size(검토 크기): small review(소규모 검토)

Packet(묶음): `{grok['packet']}`

Prompt(프롬프트): `{grok['prompt']}`

Clean output(정리 출력): `{grok['clean_output']}`

Metadata(메타데이터): `{grok['metadata']}`

Classification(분류): `{grok['classification']}`

Accepted advice(수용 조언): negative memory(부정 기억) closeout(마감), MT5 deferral(엠티5 지연) because no runtime candidate(런타임 후보 없음), claim boundary(주장 경계) 유지를 수용했습니다.

Rejected advice(거절 조언): F32B proxy(F32B 프록시)를 completion/baseline/promotion/runtime authority(완성/기준선/승격/런타임 권위)로 올리는 경로는 없습니다.

Local verification(로컬 검증): `{final['local_verification']['judgment']}`
"""


def local_verification_text(final: dict[str, Any]) -> str:
    rows = [f"- {key}: `{value}`" for key, value in final["local_verification"]["checks"].items()]
    return f"""# Frontier32D Local Verification(전선32D 로컬 검증)

Judgment(판정): `{final['local_verification']['judgment']}`

{chr(10).join(rows)}

Tier boundary(티어 경계): {final['local_verification']['tier_b_boundary']}

Effect(효과): Grok(그록) 조언을 자동 실행하지 않고, 로컬 summary(요약), candidate flags(후보 플래그), ledger(장부), runtime boundary(런타임 경계)를 대조한 뒤 closeout(마감)을 기록했습니다.
"""


def required_gate_audit(final: dict[str, Any]) -> str:
    b = final["f32b_summary"]
    return f"""# Frontier32 Required Gate Coverage Audit(전선32 필수 게이트 커버리지 감사)

- stage_open_grok_gate(단계 개방 그록 게이트): F32A(전선32A) Grok accepted(그록 수용)
- path_proxy_gate(경로 프록시 게이트): F32B(전선32B) path/scout/seed/runtime(경로/탐색/씨앗/런타임) `{b['path_candidate_rows']}/{b['path_scout_clue_rows']}/{b['path_seed_surface_rows']}/{b['runtime_probe_candidate_rows']}`
- repair_closeout_decision_gate(수리/마감 결정 게이트): F32C(전선32C) `{f32c.REPAIR_DECISION}`
- stage_closeout_grok_gate(단계 마감 그록 게이트): `{GROK_CLOSEOUT_PACKET.as_posix()}` classification(분류) `{final['grok_closeout']['classification']}`
- runtime_probe_gate(런타임 탐침 게이트): `{final['runtime_probe_status']}` because no runtime candidate(런타임 후보 없음)
- tier_pair_record_gate(티어 쌍 기록 게이트): Tier A(티어 A) path proxy(경로 프록시) recorded(기록), Tier B(티어 B) `missing_required`, Tier A+B(티어 A+B) `out_of_scope_by_claim` in F32B ledger(F32B 장부)
- closeout_gate(마감 게이트): `{final['judgment']}` with report(보고서) `{REPORT_PATH.as_posix()}`
- final_claim_guard(최종 주장 방어): runtime authority/operating promotion/Goal Achieve(런타임 권위/운영 승격/목표 달성)는 not_claimed(주장 없음)
"""


def negative_memory_text(final: dict[str, Any]) -> str:
    b = final["f32b_summary"]
    best = b["best_path_candidate"]
    return f"""# Frontier32 Negative Memory(전선32 부정 기억)

Negative memory(부정 기억): `{final['negative_memory']}`

Why limited(제한 이유): return-space caps(수익률 공간 한도)를 executable SL/TP path proxy(실행 가능한 손절/익절 경로 프록시)로 번역하자 path scout/seed/runtime candidate(경로 탐색/씨앗/런타임 후보)가 `{b['path_scout_clue_rows']}/{b['path_seed_surface_rows']}/{b['runtime_probe_candidate_rows']}`로 0이었습니다.

Evidence(근거): best validation/OOS PF-density-DD(최상 검증/표본외 수익 팩터-밀도-손실폭)는 `{fmt(best.get('validation_profit_factor'))}/{fmt(best.get('validation_trades_per_day'))}/{fmt(best.get('validation_dd_risk'))}` and `{fmt(best.get('oos_profit_factor'))}/{fmt(best.get('oos_trades_per_day'))}/{fmt(best.get('oos_dd_risk'))}`입니다.

Do not repeat(반복 금지): return-space proxy(수익률 공간 프록시)의 좋은 숫자를 intrabar path(봉내 경로) 또는 MT5 runtime probe(MT5 런타임 탐침) 없이 ONNX readiness(온엑스 준비)로 과장하지 않습니다.
"""


def selection_status(final: dict[str, Any]) -> str:
    return f"""# Frontier32 Selection Status(전선32 선택 상태)

Updated(갱신): {final['created_at_utc']}

Selection(선택): no selected baseline/completion/promotion/runtime authority(선택 기준선/완성/승격/런타임 권위 없음).

Stage closeout(단계 마감): `{RUN_ID}`

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Closeout class(마감 분류): `{final['closeout_class']}`

Negative memory(부정 기억): `{final['negative_memory']}`

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

Next action(다음 행동): `{final['next_run_id']}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 not_claimed(주장 없음)입니다.
"""


def decision_text(final: dict[str, Any]) -> str:
    return f"""# Decision(결정): Close Frontier32 Executable SL/TP Mapping(전선32 실행 가능한 손절/익절 매핑 마감)

Date(날짜): 2026-06-14

Decision(결정): Close(마감) `{STAGE_ID}` as negative_memory(부정 기억).

Effect(효과): F31(전선31)의 return-space handoff surface(수익률 공간 인계 표면)를 실행 가능한 SL/TP path proxy(손절/익절 경로 프록시)로 번역하는 축은 닫고, 다음 frontier(전선)는 path-native exit label(경로 기반 청산 라벨) 쪽으로 이동합니다.

Negative memory(부정 기억): `{final['negative_memory']}`

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

ONNX blocker(온엑스 차단): `{final['onnx_blocker']}`

Next run(다음 실행): `{final['next_run_id']}`
"""


def current_working_state(final: dict[str, Any]) -> str:
    b = final["f32b_summary"]
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

Action(행동): F32(전선32)를 executable SL/TP mapping(실행 가능한 손절/익절 매핑) negative memory(부정 기억)로 닫았습니다.

Effect(효과): path scout/seed/runtime candidate(경로 탐색/씨앗/런타임 후보) `{b['path_scout_clue_rows']}/{b['path_seed_surface_rows']}/{b['runtime_probe_candidate_rows']}`를 근거로 MT5 runtime probe(MT5 런타임 탐침)는 ineligible(부적격)로 남기고, 다음 stage(단계)는 path-native exit label(경로 기반 청산 라벨) 가설로 시작합니다.

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def changelog_entry(final: dict[str, Any]) -> str:
    b = final["f32b_summary"]
    return (
        f"- {final['created_at_utc']}: `{RUN_ID}` closed Frontier32 executable SL/TP mapping(전선32 실행 가능한 손절/익절 매핑). "
        f"Effect(효과): path_scout={b['path_scout_clue_rows']}, seed={b['path_seed_surface_rows']}, "
        f"runtime_candidate={b['runtime_probe_candidate_rows']}, next=`{NEXT_RUN_ID}`.\n"
    )


def idea_registry_entry(final: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR32-EXECUTABLE-SLTP-MAPPING-ONNX-SCOUT`: `{RUN_ID}` closed with negative memory(부정 기억) "
        f"`{final['negative_memory']}`. Effect(효과): next frontier clue(다음 전선 단서)는 `{final['next_hypothesis_clue']}`입니다.\n"
    )


def negative_register_entry(final: dict[str, Any]) -> str:
    b = final["f32b_summary"]
    return (
        f"- `{RUN_ID}`: {final['negative_memory']} | Evidence(근거): path_scout/seed/runtime(경로 탐색/씨앗/런타임) "
        f"{b['path_scout_clue_rows']}/{b['path_seed_surface_rows']}/{b['runtime_probe_candidate_rows']}; "
        f"runtime_probe_status(런타임 탐침 상태) {final['runtime_probe_status']}.\n"
    )


def artifact_identity(path: Path) -> dict[str, str]:
    return {"path": path.as_posix(), "sha256": f32b.sha256_io(path) if path_exists(path) else "missing"}


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
