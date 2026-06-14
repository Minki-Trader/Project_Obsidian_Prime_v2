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
from stage_pipelines.stage_frontier_29 import frontier29b_train_only_loss_concentration_veto_proxy_scout as f29b
from stage_pipelines.stage_frontier_29 import frontier29c_loss_concentration_veto_repair_or_closeout_decision as f29c
from stage_pipelines.stage_frontier_29 import materialize_frontier29a_stage_open as f29a


STAGE_ID = f29a.STAGE_ID
RUN_ID = "frontier29D_stage_closeout_loss_concentration_veto_v1"
RUN_NUMBER = "frontier29D"
PARENT_RUN_ID = f29c.RUN_ID
STATUS = "closed_preserved_clue_negative_memory_loss_concentration_veto_scout_zero_no_handoff"
JUDGMENT = "preserved_clue_negative_memory(보존 단서+부정 기억)"
NEXT_STAGE_ID = "stage_frontier_30__train_density_preserving_selector_before_loss_veto_or_exit_shape_pivot_onnx_scout"
NEXT_RUN_ID = "frontier30A_stage_open_train_density_preserving_selector_or_exit_shape_pivot_hypothesis_design_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
GROK_RECEIPT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_grok_closeout_receipt.md"
LOCAL_VERIFICATION_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_local_verification.md"
REQUIRED_GATE_AUDIT_PATH = STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md"
DECISION_PATH = Path("docs/decisions/2026-06-14_stage_frontier_29_loss_concentration_veto_closeout.md")
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_29/frontier29d_stage_closeout.py")

F29A_SUMMARY = STAGE_ROOT / "02_runs" / f29a.RUN_ID / "stage_open_summary.json"
F29B_SUMMARY = STAGE_ROOT / "02_runs" / f29b.RUN_ID / "final_summary.json"
F29B_CANDIDATE_SUMMARY = STAGE_ROOT / "02_runs" / f29b.RUN_ID / "loss_veto_candidate_summary.csv"
F29C_SUMMARY = STAGE_ROOT / "02_runs" / f29c.RUN_ID / "final_summary.json"
F29C_REPAIR_AUDIT = STAGE_ROOT / "02_runs" / f29c.RUN_ID / "repair_rejection_audit.csv"
GROK_STAGE_OPEN_PACKET = Path("docs/agent_control/grok_reviews/2026-06-14_frontier29_stage_open/small_review")
GROK_CLOSEOUT_PACKET = Path("docs/agent_control/grok_reviews/2026-06-14_frontier29_stage_closeout/small_review")

RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")
NEGATIVE_RESULT_REGISTER = Path("docs/registers/negative_result_register.md")
CHANGELOG = Path("docs/workspace/changelog.md")
WORKSPACE_STATE = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE = Path("docs/context/current_working_state.md")

PRESERVED_CLUE = f29c.PRESERVED_CLUE
NEGATIVE_MEMORY = f29c.NEGATIVE_MEMORY
NEXT_HYPOTHESIS_CLUE = f29c.NEXT_HYPOTHESIS_CLUE
RUNTIME_PROBE_BLOCKER = "runtime_probe_ineligible_no_handoff_candidate_after_f29c_repair_decision"
ONNX_BLOCKER = "onnx_branch_unattempted_no_handoff_candidate_after_f29c_repair_decision"


def main() -> int:
    ensure_dirs()
    normalize_grok_markdown()
    created_at = utc_now()
    f29a_summary = read_json(F29A_SUMMARY)
    f29b_summary = read_json(F29B_SUMMARY)
    f29c_summary = read_json(F29C_SUMMARY)
    candidate_summary = pd.read_csv(io_path(F29B_CANDIDATE_SUMMARY))
    repair_audit = pd.read_csv(io_path(F29C_REPAIR_AUDIT))
    grok = load_grok_closeout()
    local = validate_context(f29a_summary, f29b_summary, f29c_summary, candidate_summary, repair_audit, grok)
    final = build_final(created_at, f29a_summary, f29b_summary, f29c_summary, candidate_summary, repair_audit, grok, local)
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
    lowered = output.lower()
    accepted = (
        "verdict: accepted" in lowered
        and "closeout_class_ok: yes" in lowered
        and "repair_rejection_ok: yes" in lowered
        and "runtime_probe_status_ok: yes" in lowered
        and "next_clue_ok: yes" in lowered
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
        "classification": "accepted_with_local_count_reconciliation" if accepted else "needs_local_verification",
        "accepted": accepted,
        "count_discrepancy_flag": "168/177" in output and "7/11" in output,
        "output_excerpt": output[:3600],
    }


def validate_context(
    f29a_summary: dict[str, Any],
    f29b_summary: dict[str, Any],
    f29c_summary: dict[str, Any],
    candidate_summary: pd.DataFrame,
    repair_audit: pd.DataFrame,
    grok: dict[str, Any],
) -> dict[str, Any]:
    workspace = read_text(WORKSPACE_STATE)
    diagnosis = f29c_summary["diagnosis"]
    checks = {
        "workspace_current_frontier29c": f"current_run_id: {f29c.RUN_ID}" in workspace,
        "f29a_grok_stage_open_accepted": f29a_summary.get("grok", {}).get("classification", "").startswith("accepted"),
        "f29a_joinability_234": int(f29a_summary.get("joinability", {}).get("joinable_candidate_rows", -1)) == 234,
        "f29b_no_scout_seed_handoff": int(f29b_summary.get("scout_clue_rows", -1)) == 0
        and int(f29b_summary.get("seed_surface_rows", -1)) == 0
        and int(f29b_summary.get("handoff_candidate_rows", -1)) == 0,
        "f29b_selected_rows_match": len(candidate_summary) == int(f29b_summary.get("selected_veto_rows", -1)),
        "f29c_repair_rejected": f29c_summary.get("repair_decision") == "reject_repair_and_closeout",
        "f29c_valid_repair_zero": int(diagnosis.get("valid_train_loss_repair_opportunity_rows", -1)) == 0,
        "f29c_authoritative_counts_reconciled": int(diagnosis.get("dd_ready_pf_blocked_rows", -1)) == 7
        and int(diagnosis.get("would_require_posthoc_contract_edit_rows", -1)) == 11,
        "repair_audit_rows_match": len(repair_audit) == int(diagnosis.get("selected_veto_rows", -1)),
        "grok_closeout_success": grok["success"] and grok["returncode"] == 0 and not grok["timed_out"],
        "grok_closeout_accepted": grok["accepted"],
        "grok_count_discrepancy_reconciled": grok["count_discrepancy_flag"]
        and int(diagnosis.get("dd_ready_pf_blocked_rows", -1)) == 7
        and int(diagnosis.get("would_require_posthoc_contract_edit_rows", -1)) == 11,
        "grok_no_unexpected_top_level_artifacts": not grok["unexpected_top_level_artifacts"],
    }
    return {
        "checks": checks,
        "judgment": "pass_closeout_ready_with_local_count_reconciliation" if all(checks.values()) else "needs_manual_review",
        "authoritative_local_counts": {
            "dd_ready_pf_blocked_rows": diagnosis.get("dd_ready_pf_blocked_rows"),
            "would_require_posthoc_contract_edit_rows": diagnosis.get("would_require_posthoc_contract_edit_rows"),
        },
        "grok_prompt_stale_counts": {
            "dd_ready_pf_blocked_rows": 168,
            "would_require_posthoc_contract_edit_rows": 177,
        },
    }


def build_final(
    created_at: str,
    f29a_summary: dict[str, Any],
    f29b_summary: dict[str, Any],
    f29c_summary: dict[str, Any],
    candidate_summary: pd.DataFrame,
    repair_audit: pd.DataFrame,
    grok: dict[str, Any],
    local: dict[str, Any],
) -> dict[str, Any]:
    if local["judgment"] != "pass_closeout_ready_with_local_count_reconciliation":
        raise RuntimeError(f"Frontier29D closeout local checks failed: {json.dumps(local, ensure_ascii=False)}")
    best_forward = f29b_summary.get("best_forward_readonly_candidate", {})
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
        "runtime_probe_blocker": RUNTIME_PROBE_BLOCKER,
        "onnx_blocker": ONNX_BLOCKER,
        "f29a_summary": {
            "status": f29a_summary.get("status"),
            "judgment": f29a_summary.get("judgment"),
            "joinable_candidate_rows": f29a_summary.get("joinability", {}).get("joinable_candidate_rows"),
            "grok_classification": f29a_summary.get("grok", {}).get("classification"),
        },
        "f29b_summary": {
            "status": f29b_summary.get("status"),
            "judgment": f29b_summary.get("judgment"),
            "source_candidate_rows": f29b_summary.get("source_candidate_rows"),
            "screened_rule_rows": f29b_summary.get("screened_rule_rows"),
            "selected_veto_rows": f29b_summary.get("selected_veto_rows"),
            "density_bridge_rows": f29b_summary.get("density_bridge_rows"),
            "scout_clue_rows": f29b_summary.get("scout_clue_rows"),
            "seed_surface_rows": f29b_summary.get("seed_surface_rows"),
            "handoff_candidate_rows": f29b_summary.get("handoff_candidate_rows"),
            "best_forward_readonly_candidate_id": f29b_summary.get("best_forward_readonly_candidate_id"),
            "best_forward_readonly_candidate": best_forward,
        },
        "f29c_summary": {
            "status": f29c_summary.get("status"),
            "judgment": f29c_summary.get("judgment"),
            "repair_decision": f29c_summary.get("repair_decision"),
            "diagnosis": f29c_summary.get("diagnosis", {}),
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
        F29A_SUMMARY,
        F29B_SUMMARY,
        F29B_CANDIDATE_SUMMARY,
        F29C_SUMMARY,
        F29C_REPAIR_AUDIT,
        GROK_STAGE_OPEN_PACKET / "metadata.json",
        GROK_CLOSEOUT_PACKET / "metadata.json",
        GROK_RECEIPT_PATH,
        LOCAL_VERIFICATION_PATH,
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
            "local_count_reconciliation": final["local_verification"]["authoritative_local_counts"],
        },
        "claim_boundary": final["claim_boundary"],
    }


def update_registries(final: dict[str, Any]) -> None:
    f03b.upsert_csv(RUN_REGISTRY, "run_id", run_registry_row(final))
    for row in ledger_rows(final):
        f03b.upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
        f03b.upsert_csv(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", row)
    f03b.append_once(CHANGELOG, RUN_ID, changelog_entry(final))
    f03b.append_once(IDEA_REGISTRY, RUN_ID, idea_registry_entry(final))
    f03b.append_once(NEGATIVE_RESULT_REGISTER, RUN_ID, negative_register_entry(final))


def run_registry_row(final: dict[str, Any]) -> dict[str, Any]:
    f29b_summary = final["f29b_summary"]
    diagnosis = final["f29c_summary"]["diagnosis"]
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
        "primary_kpi": f"selected={f29b_summary['selected_veto_rows']};scout={f29b_summary['scout_clue_rows']};seed={f29b_summary['seed_surface_rows']};handoff={f29b_summary['handoff_candidate_rows']};valid_repair={diagnosis['valid_train_loss_repair_opportunity_rows']}",
        "guardrail_kpi": "closeout_preserved_clue_negative_memory_no_wfo_no_mt5_no_onnx_no_authority",
        "external_verification_status": final["runtime_probe_blocker"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "result_path": REPORT_PATH.as_posix(),
    }


def ledger_rows(final: dict[str, Any]) -> list[dict[str, Any]]:
    f29b_summary = final["f29b_summary"]
    diagnosis = final["f29c_summary"]["diagnosis"]
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
        "primary_kpi": f"selected={f29b_summary['selected_veto_rows']};scout={f29b_summary['scout_clue_rows']};seed={f29b_summary['seed_surface_rows']};handoff={f29b_summary['handoff_candidate_rows']};valid_repair={diagnosis['valid_train_loss_repair_opportunity_rows']}",
        "guardrail_kpi": "no_wfo_no_mt5_no_onnx_no_runtime_authority(WFO/MT5/ONNX/런타임 권위 없음)",
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


def report_text(final: dict[str, Any]) -> str:
    f29b_summary = final["f29b_summary"]
    diagnosis = final["f29c_summary"]["diagnosis"]
    best = f29b_summary.get("best_forward_readonly_candidate", {})
    return f"""# Frontier29D Stage Closeout Report(전선29D 단계 마감 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Action(행동): F29(전선29) train-only loss concentration veto(학습 전용 손실 집중 차단) 가설을 preserved clue + negative memory(보존 단서 + 부정 기억)로 closeout(마감)했습니다.

Effect(효과): loss veto(손실 차단)는 density bridge(밀도 충족) 조각을 만들었지만 scout/seed/handoff(탐색/씨앗/인계)는 0개였고, MT5/ONNX/WFO(MT5/온엑스/워크포워드 최적화)는 실행하지 않았습니다.

Preserved clue(보존 단서): `{final['preserved_clue']}`

Negative memory(부정 기억): `{final['negative_memory']}`

F29B selected/density/scout/seed/handoff(전선29B 선택/밀도/탐색/씨앗/인계): `{f29b_summary['selected_veto_rows']}` / `{f29b_summary['density_bridge_rows']}` / `{f29b_summary['scout_clue_rows']}` / `{f29b_summary['seed_surface_rows']}` / `{f29b_summary['handoff_candidate_rows']}`

Best read-only forward candidate(최상 읽기 전용 전진 후보): `{f29b_summary['best_forward_readonly_candidate_id']}` with validation/OOS PF-density-DD(검증/표본외 수익 팩터-밀도-손실폭) `{fmt(best.get('validation_profit_factor'))}/{fmt(best.get('validation_trades_per_day'))}/{fmt(best.get('validation_dd_risk'))}` and `{fmt(best.get('oos_profit_factor'))}/{fmt(best.get('oos_trades_per_day'))}/{fmt(best.get('oos_dd_risk'))}`.

F29C authoritative diagnosis(전선29C 권위 진단): near_scout(탐색 근접) `{diagnosis['near_scout_rows']}`, dd_ready_pf_blocked(DD 준비+PF 차단) `{diagnosis['dd_ready_pf_blocked_rows']}`, would_require_posthoc_contract_edit(사후 계약 변경 필요) `{diagnosis['would_require_posthoc_contract_edit_rows']}`, valid repair(유효 수리) `{diagnosis['valid_train_loss_repair_opportunity_rows']}`.

Grok closeout classification(그록 마감 분류): `{final['grok_closeout']['classification']}`.

Count reconciliation(수치 정합): Grok prompt(그록 프롬프트)의 stale counts(낡은 수치) `168/177`은 closeout artifact(마감 산출물)에 쓰지 않았습니다. Local authoritative counts(로컬 권위 수치) `7/11`을 사용했습니다.

Runtime probe blocker(런타임 탐침 차단 사유): `{final['runtime_probe_blocker']}`

ONNX blocker(ONNX 차단 사유): `{final['onnx_blocker']}`

Next hypothesis clue(다음 가설 단서): `{final['next_hypothesis_clue']}`

Next action(다음 행동): `{final['next_run_id']}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def grok_receipt(final: dict[str, Any]) -> str:
    grok = final["grok_closeout"]
    return f"""# Frontier29D Grok Closeout Receipt(전선29D 그록 마감 영수증)

Packet(묶음): `{grok['packet']}`

Prompt(프롬프트): `{grok['prompt']}`

Clean output(정리 출력): `{grok['clean_output']}`

Metadata(메타데이터): `{grok['metadata']}`

Prompt hash(프롬프트 해시): `{grok['prompt_hash']}`

Transport success(전송 성공): `{grok['success']}`, returncode(반환 코드) `{grok['returncode']}`, timed_out(시간 초과) `{grok['timed_out']}`

Codex classification(코덱스 분류): `{grok['classification']}`

Accepted advice(수용 조언): preserved clue + negative memory(보존 단서 + 부정 기억), repair rejection(수리 거절), runtime_probe_ineligible(런타임 탐침 부적격), ONNX unattempted(ONNX 미시도), next clue reference-only(다음 단서 참조 전용).

Needs local verification(로컬 검증 필요): closeout prompt(마감 프롬프트)의 stale counts(낡은 수치) `168/177`을 local F29C summary(로컬 F29C 요약) `7/11`로 정합.

Local verification(로컬 검증): `{final['local_verification']['judgment']}`
"""


def local_verification_text(final: dict[str, Any]) -> str:
    lines = ["# Frontier29D Local Verification(전선29D 로컬 검증)", ""]
    lines.append(f"Judgment(판정): `{final['local_verification']['judgment']}`")
    lines.append("")
    for key, value in final["local_verification"]["checks"].items():
        lines.append(f"- {key}: `{value}`")
    lines.append("")
    lines.append(f"Authoritative local counts(권위 로컬 수치): `{final['local_verification']['authoritative_local_counts']}`")
    lines.append(f"Grok prompt stale counts(그록 프롬프트 낡은 수치): `{final['local_verification']['grok_prompt_stale_counts']}`")
    lines.append("")
    lines.append("Effect(효과): Grok(그록)의 수용 판정은 유지하되, F29D closeout(마감) 산출물은 로컬 F29C summary/report(요약/보고서)의 권위 수치만 사용합니다.")
    return "\n".join(lines) + "\n"


def required_gate_audit(final: dict[str, Any]) -> str:
    f29b_summary = final["f29b_summary"]
    diagnosis = final["f29c_summary"]["diagnosis"]
    return f"""# Frontier29 Required Gate Coverage Audit(전선29 필수 게이트 커버리지 감사)

- stage_open_grok_gate(단계 개방 그록 게이트): `{GROK_STAGE_OPEN_PACKET.as_posix()}` recorded(기록)
- proxy_gate(프록시 게이트): `{f29b.RUN_ID}` produced selected/density/scout/seed/handoff(선택/밀도/탐색/씨앗/인계) `{f29b_summary['selected_veto_rows']}/{f29b_summary['density_bridge_rows']}/{f29b_summary['scout_clue_rows']}/{f29b_summary['seed_surface_rows']}/{f29b_summary['handoff_candidate_rows']}`
- repair_decision_gate(수리 결정 게이트): `{f29c.RUN_ID}` recorded valid_train_loss_repair_opportunity_rows(유효 학습 손실 수리 기회 행) `{diagnosis['valid_train_loss_repair_opportunity_rows']}`
- stage_closeout_grok_gate(단계 마감 그록 게이트): `{GROK_CLOSEOUT_PACKET.as_posix()}` classification(분류) `{final['grok_closeout']['classification']}`
- local_reconciliation_gate(로컬 정합 게이트): stale prompt counts(낡은 프롬프트 수치) `168/177` reconciled to local counts(로컬 수치) `7/11`
- runtime_probe_gate(런타임 탐침 게이트): `{final['runtime_probe_blocker']}`
- onnx_gate(ONNX 게이트): `{final['onnx_blocker']}`
- tier_pair_record_gate(티어 쌍 기록 게이트): Tier A/Tier B/Tier A+B(티어 A/B/A+B) rows(행) written(기록)
- final_claim_guard(최종 주장 방어): runtime authority/operating promotion/Goal Achieve(런타임 권위/운영 승격/목표 달성) not_claimed(주장 없음)
"""


def preserved_clue_text(final: dict[str, Any]) -> str:
    d = final["f29c_summary"]["diagnosis"]
    return f"""# Frontier29 Preserved Clue(전선29 보존 단서)

Preserved clue(보존 단서): `{final['preserved_clue']}`

Evidence(근거): F29B(전선29B)는 density_bridge(밀도 충족) `{d['density_bridge_rows']}`개, density_dual_positive(밀도+양수) `{d['density_dual_positive_rows']}`개, near_scout(탐색 근접) `{d['near_scout_rows']}`개를 만들었습니다.

Use boundary(사용 경계): reference only(참조 전용). This is not baseline/promotion/runtime authority(기준선/승격/런타임 권위 아님).
"""


def negative_memory_text(final: dict[str, Any]) -> str:
    f29b_summary = final["f29b_summary"]
    return f"""# Frontier29 Negative Memory(전선29 부정 기억)

Negative memory(부정 기억): `{final['negative_memory']}`

Why failed(실패 이유): locked train loss veto contract(잠금 학습 손실 차단 계약) 아래 scout/seed/handoff(탐색/씨앗/인계)가 `{f29b_summary['scout_clue_rows']}` / `{f29b_summary['seed_surface_rows']}` / `{f29b_summary['handoff_candidate_rows']}`개로 남았습니다.

Do not repeat(반복 금지): validation/OOS(검증/표본외)를 보고 density/threshold(밀도/임계값)를 사후 조정하는 수리는 하지 않습니다.
"""


def selection_status(final: dict[str, Any]) -> str:
    return f"""# Frontier29 Selection Status(전선29 선택 상태)

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
    return f"""# Decision(결정): Close Frontier29 Loss Concentration Veto Scout(전선29 손실 집중 차단 탐색 마감)

Date(날짜): 2026-06-14

Decision(결정): Close(마감) `{STAGE_ID}` as preserved_clue_negative_memory(보존 단서+부정 기억).

Effect(효과): loss concentration veto(손실 집중 차단)는 참조 단서로 보존하지만 scout/seed/handoff(탐색/씨앗/인계) 0개와 수리 기회 0개를 부정 기억으로 남깁니다.

Preserved clue(보존 단서): `{final['preserved_clue']}`

Negative memory(부정 기억): `{final['negative_memory']}`

Runtime probe blocker(런타임 탐침 차단): `{final['runtime_probe_blocker']}`

ONNX blocker(ONNX 차단): `{final['onnx_blocker']}`

Next run(다음 실행): `{final['next_run_id']}`
"""


def current_working_state(final: dict[str, Any]) -> str:
    f29b_summary = final["f29b_summary"]
    diagnosis = final["f29c_summary"]["diagnosis"]
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

Action(행동): F29(전선29)를 train-only loss concentration veto(학습 전용 손실 집중 차단) scout(탐색)으로 닫았습니다.

Effect(효과): selected/scout/seed/handoff(선택/탐색/씨앗/인계) `{f29b_summary['selected_veto_rows']}/{f29b_summary['scout_clue_rows']}/{f29b_summary['seed_surface_rows']}/{f29b_summary['handoff_candidate_rows']}`와 valid repair(유효 수리) `{diagnosis['valid_train_loss_repair_opportunity_rows']}`를 근거로, 다음 전선은 density-preserving selector(밀도 보존 선택기) 또는 exit-shape pivot(청산 형태 전환) 단서로 넘어갑니다.

Runtime probe blocker(런타임 탐침 차단 사유): `{final['runtime_probe_blocker']}`

ONNX blocker(ONNX 차단 사유): `{final['onnx_blocker']}`

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def changelog_entry(final: dict[str, Any]) -> str:
    f29b_summary = final["f29b_summary"]
    return (
        f"- {final['created_at_utc']}: `{RUN_ID}` closed Frontier29(전선29 마감). "
        f"Effect(효과): selected/scout/seed/handoff(선택/탐색/씨앗/인계) counts are {f29b_summary['selected_veto_rows']}/{f29b_summary['scout_clue_rows']}/{f29b_summary['seed_surface_rows']}/{f29b_summary['handoff_candidate_rows']} and next run(다음 실행) is `{final['next_run_id']}`.\n"
    )


def idea_registry_entry(final: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR29-TRAIN-ONLY-LOSS-CONCENTRATION-VETO-PF-DD-BALANCE-ONNX-SCOUT`: `{RUN_ID}` closed as preserved_clue_negative_memory(보존 단서+부정 기억). "
        f"Effect(효과): `{final['preserved_clue']}` and `{final['negative_memory']}`.\n"
    )


def negative_register_entry(final: dict[str, Any]) -> str:
    return (
        f"- `{RUN_ID}`: `{final['negative_memory']}`. Preserved clue(보존 단서): `{final['preserved_clue']}`. "
        f"Runtime blocker(런타임 차단): `{final['runtime_probe_blocker']}`. ONNX blocker(ONNX 차단): `{final['onnx_blocker']}`. "
        f"Effect(효과): next clue(다음 단서) `{final['next_hypothesis_clue']}`.\n"
    )


def artifact_identity(path: Path) -> dict[str, str]:
    return {"path": path.as_posix(), "sha256": sha256_io(path) if path_exists(path) else "missing"}


def sha256_io(path: Path) -> str:
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fmt(value: Any) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return "NA"
    if not math.isfinite(number):
        return "NA"
    return f"{number:.3f}"


if __name__ == "__main__":
    raise SystemExit(main())
