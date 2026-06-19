from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.audit_result import AuditResult
from foundation.control_plane.final_claim_guard import guard_final_claims
from foundation.control_plane.ledger import io_path


STAGE_ID = "stage_frontier_89__runtime_trade_list_adverse_selection_teacher"
PACKET_ID = "frontier89_task_force_correction_review_v1"
CURRENT_RUN_ID = "frontier89C_deal_path_teacher_repair_or_rotation_decision_v1"
LATEST_COMPLETED_RUN_ID = "frontier89B_deal_path_adverse_selection_proxy_scout_v1"
STAGE_ROOT = ROOT / "stages" / STAGE_ID
REVIEW_DIR = STAGE_ROOT / "03_reviews"
PACKET_DIR = ROOT / "docs" / "agent_control" / "packets" / PACKET_ID

CLAIM_BOUNDARY = (
    "task_force_correction_record_only_no_retroactive_reviewed_verified_pass_"
    "no_strategy_tester_runtime_economics_no_selected_baseline_no_operating_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)
ALLOWED_CLAIMS = [
    "task_force_actual_calls_recorded",
    "incorrect_not_triggered_correction_recorded",
    "current_truth_task_force_boundary_synced",
    "f89c_task_force_trigger_rule_recorded",
]
FORBIDDEN_CLAIMS = [
    "completion",
    "completed",
    "selected_baseline",
    "operating_promotion",
    "runtime_authority",
    "live_readiness",
    "goal_achieve",
    "runtime_probe",
    "runtime_verified",
    "strategy_tester_runtime_economics",
    "materialization_ready",
    "mt5_handoff_ready",
    "task_force_reviewed",
    "reviewed",
    "verified",
    "pass",
    "reviewed_by_unspawned_agents",
    "retroactive_task_force_pass",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def repo(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_yaml(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(yaml.safe_dump(payload, allow_unicode=True, sort_keys=False), encoding="utf-8-sig")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8-sig")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def run_json(cmd: list[str], output_path: Path) -> dict[str, Any]:
    completed = subprocess.run(cmd, cwd=ROOT, check=False, capture_output=True, text=True)
    if completed.returncode != 0:
        raise RuntimeError(f"{cmd} failed\nSTDOUT:\n{completed.stdout}\nSTDERR:\n{completed.stderr}")
    return load_json(output_path)


def audit_from_dict(payload: dict[str, Any]) -> AuditResult:
    return AuditResult(
        audit_name=str(payload["audit_name"]),
        status=str(payload["status"]),
        counts=payload.get("counts", {}),
        allowed_claims=tuple(payload.get("allowed_claims", ())),
        forbidden_claims=tuple(payload.get("forbidden_claims", ())),
    )


def subagent_calls() -> list[dict[str, str]]:
    return [
        {
            "roster_agent_id": "agent_01_system_governor",
            "spawned_agent_id": "019edd21-ac86-75d1-b16e-c4ffbb26759e",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "needs_local_verification",
        },
        {
            "roster_agent_id": "agent_04_evidence_control_plane",
            "spawned_agent_id": "019edd21-d62b-7d63-915b-0c68afec0e96",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "accepted",
        },
        {
            "roster_agent_id": "agent_05_data_feature_contract",
            "spawned_agent_id": "019edd21-fe70-7503-8a7c-1728ce4fdfda",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "needs_local_verification",
        },
        {
            "roster_agent_id": "agent_07_model_validation_risk",
            "spawned_agent_id": "019edd22-32c7-7a21-aa54-2584fe1e6c51",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "accepted",
        },
        {
            "roster_agent_id": "agent_08_mt5_onnx_runtime",
            "spawned_agent_id": "019edd22-5d59-7c13-9ce4-31a09c5d24ac",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "accepted",
        },
    ]


def build_task_force_receipt(now: str) -> dict[str, Any]:
    calls = subagent_calls()
    return {
        "packet_id": PACKET_ID,
        "skill": "obsidian-task-force-review",
        "status": "executed",
        "trigger_reason": [
            "explicit_user_instruction_required: user corrected missing Task Force calls",
            "roster_rule_required: agent_01_system_governor is required_for stage_open",
            "correction_surface: F89A/F89B recorded not_triggered/no actual_subagent_calls earlier",
        ],
        "roster_registry": "docs/agent_control/codex_task_force_registry.yaml",
        "agents_used": [call["roster_agent_id"] for call in calls],
        "actual_subagent_calls": calls,
        "review_requirement": "explicit_user_instruction_required",
        "model_policy": {
            "registry_floor": "gpt-5.5 xhigh",
            "session_execution": "inherited parent model through multi_agent_v1.spawn_agent",
            "non_authority_rule": "model strength is not evidence and does not relax gates or claim boundary",
        },
        "bounded_evidence": [
            "docs/agent_control/packets/frontier89A_stage_open_runtime_trade_list_adverse_selection_teacher_v1/work_packet.yaml",
            "docs/agent_control/packets/frontier89B_deal_path_adverse_selection_proxy_scout_v1/work_packet.yaml",
            "docs/workspace/workspace_state.yaml",
            "stages/stage_frontier_89__runtime_trade_list_adverse_selection_teacher/03_reviews/f89a_task_force_trigger_check.json",
            "stages/stage_frontier_89__runtime_trade_list_adverse_selection_teacher/03_reviews/f89b_task_force_trigger_check.json",
        ],
        "advice_classification": {
            "agent_01_system_governor": "needs_local_verification",
            "agent_04_evidence_control_plane": "accepted",
            "agent_05_data_feature_contract": "needs_local_verification",
            "agent_07_model_validation_risk": "accepted",
            "agent_08_mt5_onnx_runtime": "accepted",
        },
        "local_verification": {
            "actual_call_count": len(calls),
            "selected_agent_count": len(calls),
            "not_all_roster_agents": True,
            "agent_05_stale_tool_unavailable_sentence": "rejected_for_call_availability; the parent thread has the actual spawned_agent_id",
            "f89a_prior_trigger_status": "incorrect_not_triggered_for_stage_open_requirement",
            "f89b_proxy_boundary": "accepted_as_proxy_scout_only_no_runtime_candidate_no_runtime_claim",
            "task_force_review_claim": "not_claimed",
        },
        "claim_boundary": CLAIM_BOUNDARY,
        "final_codex_direction": [
            "append-only correction receipt; do not rewrite F89A/F89B into retroactive Task Force reviewed/pass",
            "F89C repair/rotation or closeout must trigger relevant Task Force agents before any reviewed/pass/closeout claim",
            "If F89C creates a meaningful materialization candidate, same-packet MT5 Strategy Tester runtime probe is required unless blocked by concrete tool/artifact condition",
        ],
        "forbidden_claim_check": FORBIDDEN_CLAIMS,
        "created_at_utc": now,
        "receipt_path": repo(REVIEW_DIR / "f89_task_force_correction_review_receipt.json"),
    }


def write_current_truth(now: str) -> None:
    workspace_state = {
        "current_stage_id": STAGE_ID,
        "active_stage": STAGE_ID,
        "current_run_id": CURRENT_RUN_ID,
        "latest_completed_run_id": LATEST_COMPLETED_RUN_ID,
        "current_status": "f89b_deal_path_teacher_proxy_scout_inconclusive_no_materialization_candidate_no_authority",
        "current_judgment": "inconclusive_small_sample_deal_path_teacher_proxy_no_runtime_candidate_no_runtime_evidence",
        "next_run_id": CURRENT_RUN_ID,
        "frontier_extra_due_status": "not_due_after_f88_closeout_next_boundary_f100_e01_closed_for_f050",
        "frontier_topic_rotation_status": "same_f89_hypothesis_lifecycle_continuation",
        "task_force_status": "correction_recorded_actual_calls_no_retroactive_review_pass",
        "runtime_probe_status": "not_run_no_meaningful_materialization_candidate_no_runtime_claim",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "updated_at_utc": now,
        "context_anchor": f"stages/{STAGE_ID}/03_reviews/context_anchor.md",
        "notes": [
            "Action(행동): F89 Task Force correction receipt(F89 태스크포스 정정 영수증)를 추가했다.",
            "Effect(효과): F89A/F89B의 이전 not_triggered(미트리거) 기록은 소급 통과가 아니라 incorrect_not_triggered correction(잘못된 미트리거 정정)으로 남긴다.",
            "Task Force(태스크포스): 5 selected agents(선택 요원 5명) actual_subagent_calls(실제 하위요원 호출)를 기록했고, Task Force reviewed/pass(태스크포스 검토됨/통과)는 주장하지 않는다.",
            "Runtime(런타임): F89B는 no meaningful materialization candidate(의미 있는 물질화 후보 없음)이므로 새 Strategy Tester runtime evidence(전략 테스터 런타임 근거)는 없고, cost/expense deferral(비용 지연)이 아니다.",
        ],
    }
    write_yaml(ROOT / "docs" / "workspace" / "workspace_state.yaml", workspace_state)

    current_working = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {now}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{CURRENT_RUN_ID}`

Latest completed run(최근 완료 실행): `{LATEST_COMPLETED_RUN_ID}`

Action(행동): F89 Task Force correction receipt(F89 태스크포스 정정 영수증)를 추가했다.

Effect(효과): F89A/F89B의 previous not_triggered(이전 미트리거) 판단은 append-only correction(추가 전용 정정)으로 낮추고, actual_subagent_calls(실제 하위요원 호출) 5건을 현재 근거로 남긴다.

Task Force status(태스크포스 상태): `correction_recorded_actual_calls_no_retroactive_review_pass`.

Runtime probe(런타임 탐침): `not_run_no_meaningful_materialization_candidate_no_runtime_claim`.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""
    write_md(ROOT / "docs" / "context" / "current_working_state.md", current_working)

    selection_status = f"""# F89 Selection Status(F89 선택 상태)

Updated(갱신): {now}

Current run(현재 실행): `{CURRENT_RUN_ID}`

Latest completed run(최근 완료 실행): `{LATEST_COMPLETED_RUN_ID}`

Status(상태): `f89b_deal_path_teacher_proxy_scout_inconclusive_no_materialization_candidate_no_authority`

Judgment(판정): `inconclusive_small_sample_deal_path_teacher_proxy_no_runtime_candidate_no_runtime_evidence`

Task Force(태스크포스): `correction_recorded_actual_calls_no_retroactive_review_pass`

Runtime probe(런타임 탐침): `not_run_no_meaningful_materialization_candidate_no_runtime_claim`

Selected baseline(선택 기준선): not_claimed(주장하지 않음)

Operating promotion(운영 승격): not_claimed(주장하지 않음)

Runtime authority(런타임 권위): not_claimed(주장하지 않음)

Live readiness(실거래 준비): not_claimed(주장하지 않음)

Goal Achieve(목표 달성): not_claimed(주장하지 않음)

Next action(다음 행동): `{CURRENT_RUN_ID}`.
"""
    write_md(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status)


def build_work_packet(now: str) -> dict[str, Any]:
    required_gates = [
        "work_packet_schema_lint",
        "skill_receipt_schema_lint",
        "codex_task_force_review_packet",
        "frontier_extra_due_check",
        "frontier_five_stage_direction_synthesis",
        "frontier_topic_rotation_check",
        "state_sync_audit",
        "required_gate_coverage_audit",
        "final_claim_guard",
    ]
    return {
        "version": "work_packet_schema_v2_1",
        "packet_lifecycle": "new_packet",
        "packet_id": PACKET_ID,
        "created_at_utc": now,
        "user_request": {
            "user_quote": "Task Force agents must be called when required; user corrected missing subagent calls.",
            "requested_action": "F89 Task Force correction receipt for missed agent calls",
            "requested_count": {"value": 1, "n_a_reason": ""},
            "ambiguous_terms": ["No final completion, runtime authority, or Goal Achieve claim."],
        },
        "current_truth": {
            "active_stage": STAGE_ID,
            "current_run": CURRENT_RUN_ID,
            "latest_completed_run": LATEST_COMPLETED_RUN_ID,
            "source_documents": [
                "docs/workspace/workspace_state.yaml",
                "docs/context/current_working_state.md",
                f"stages/{STAGE_ID}/04_selected/selection_status.md",
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "work_classification": {
            "primary_family": "state_sync",
            "detected_families": ["state_sync", "artifact_lineage", "task_force_review"],
            "touched_surfaces": [
                f"stages/{STAGE_ID}/03_reviews",
                f"docs/agent_control/packets/{PACKET_ID}",
                "docs/workspace/workspace_state.yaml",
                "docs/context/current_working_state.md",
            ],
            "mutation_intent": True,
            "execution_intent": True,
        },
        "risk_vector_scan": {
            "risks": {
                "task_force_review_claim_without_calls": "high",
                "retroactive_review_pass_laundering": "high",
                "proxy_only_laundered_as_runtime": "high",
            },
            "hard_stop_risks": [
                "Do not convert F89A/F89B into retroactive Task Force reviewed/verified/pass.",
                "Do not claim runtime/economics evidence from Task Force opinions.",
                "Do not defer a future runtime probe for cost if F89C creates a meaningful candidate.",
            ],
            "required_gates": required_gates,
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        "decision_lock": {
            "mode": "assume_safe_default",
            "assumptions": {
                "current_run_unchanged": True,
                "strategy_tester_required_now": False,
                "runtime_probe_required_now": False,
                "reason": "This packet protects a Task Force correction/status-sync claim only; F89B still has no meaningful materialization candidate.",
            },
            "questions": [],
            "required_user_decisions": [],
        },
        "interpreted_scope": {
            "work_families": ["state_sync"],
            "target_surfaces": ["F89 Task Force correction", "current truth Task Force boundary", "F89C trigger rule"],
            "scope_units": ["actual_subagent_call_record", "correction_receipt", "state_sync", "claim_boundary"],
            "execution_layers": ["local_file_materialization", "control_plane_lints"],
            "mutation_policy": {"allowed": True, "user_quote": "Task Force agents must be called when required."},
            "evidence_layers": ["subagent notifications", "roster registry", "F89A/F89B packets", "state docs"],
            "reduction_policy": {
                "reduction_allowed": True,
                "requires_user_quote": False,
                "rationale": "Only relevant roster agents were selected; all 8 agents were not needed.",
            },
            "claim_boundary": {
                "allowed_claims": ALLOWED_CLAIMS,
                "forbidden_claims": FORBIDDEN_CLAIMS,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        },
        "verification_profile": {
            "profile_id": "static_contract",
            "claim_surface": {
                "allowed_claims": ALLOWED_CLAIMS,
                "forbidden_claims": FORBIDDEN_CLAIMS,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            "trigger_sources": ["explicit_user_scope", "codex_task_force_review_overlay", "roster_agent_01_required_for_stage_open"],
            "protected_claims": ALLOWED_CLAIMS,
            "required_evidence": [
                f"stages/{STAGE_ID}/03_reviews/f89_task_force_correction_review_receipt.json",
                f"stages/{STAGE_ID}/03_reviews/f89_task_force_correction_summary.md",
                f"docs/agent_control/packets/{PACKET_ID}/skill_receipts.json",
                f"docs/agent_control/packets/{PACKET_ID}/codex_task_force_review_packet.json",
                "actual spawned_agent_id values for selected Task Force agents",
            ],
            "gates_not_run_with_reason": [
                {
                    "gate": "runtime_evidence_gate",
                    "reason_code": "outside_claim_surface_no_materialization_candidate",
                    "reason": "This correction packet makes no runtime/materialization/handoff/economics claim; F89B had no meaningful candidate.",
                    "claim_effect": "Runtime verified, economics pass, materialization-ready, authority, and Goal Achieve claims are forbidden.",
                }
            ],
            "stop_conditions": [
                "Stop after actual subagent calls, correction receipt, state sync, and control-plane lints are recorded.",
                "Do not reopen or rewrite F89A/F89B as retroactive Task Force reviewed/pass.",
                "F89C must call relevant agents before repair/rotation closeout or reviewed/pass claim.",
            ],
        },
        "acceptance_criteria": [
            {
                "id": "AC-001",
                "text": "Actual selected-agent spawn_agent calls are recorded.",
                "expected_artifact": f"stages/{STAGE_ID}/03_reviews/f89_task_force_correction_review_receipt.json",
                "verification_method": "codex_task_force_review_packet",
                "required": True,
            },
            {
                "id": "AC-002",
                "text": "Current truth states correction without retroactive review/pass.",
                "expected_artifact": "docs/workspace/workspace_state.yaml",
                "verification_method": "state_sync_audit",
                "required": True,
            },
        ],
        "work_plan": {
            "phases": [
                "Record selected Task Force actual calls.",
                "Write append-only correction receipt and summary.",
                "Sync current truth without changing current run.",
                "Run schema, receipt, state sync, gate coverage, and final claim guard.",
            ],
            "expected_outputs": [
                f"stages/{STAGE_ID}/03_reviews/f89_task_force_correction_review_receipt.json",
                f"stages/{STAGE_ID}/03_reviews/f89_task_force_correction_summary.md",
                f"docs/agent_control/packets/{PACKET_ID}/work_packet.yaml",
                f"docs/agent_control/packets/{PACKET_ID}/skill_receipts.json",
                f"docs/agent_control/packets/{PACKET_ID}/closeout_gate.json",
            ],
            "stop_conditions": ["No runtime probe in this correction packet because no runtime claim is protected."],
        },
        "skill_routing": {
            "primary_family": "state_sync",
            "primary_skill": "obsidian-stage-transition",
            "support_skills": [
                "obsidian-reentry-read",
                "obsidian-artifact-lineage",
                "obsidian-task-force-review",
                "obsidian-claim-discipline",
            ],
            "skills_considered": [
                "obsidian-stage-transition",
                "obsidian-reentry-read",
                "obsidian-artifact-lineage",
                "obsidian-task-force-review",
                "obsidian-claim-discipline",
                "obsidian-runtime-parity",
                "obsidian-backtest-forensics",
            ],
            "skills_selected": [
                "obsidian-stage-transition",
                "obsidian-reentry-read",
                "obsidian-artifact-lineage",
                "obsidian-task-force-review",
                "obsidian-claim-discipline",
            ],
            "skills_not_used": [
                {"skill": "obsidian-runtime-parity", "reason": "No runtime parity/handoff claim in correction packet."},
                {"skill": "obsidian-backtest-forensics", "reason": "No new Strategy Tester report in correction packet."},
            ],
            "required_skill_receipts": [
                "obsidian-stage-transition",
                "obsidian-reentry-read",
                "obsidian-artifact-lineage",
                "obsidian-task-force-review",
                "obsidian-claim-discipline",
            ],
            "required_gates": required_gates,
        },
        "evidence_contract": {
            "raw_evidence": [
                "subagent_notification: agent_01_system_governor",
                "subagent_notification: agent_04_evidence_control_plane",
                "subagent_notification: agent_05_data_feature_contract",
                "subagent_notification: agent_07_model_validation_risk",
                "subagent_notification: agent_08_mt5_onnx_runtime",
            ],
            "machine_readable": [
                f"stages/{STAGE_ID}/03_reviews/f89_task_force_correction_review_receipt.json",
                f"docs/agent_control/packets/{PACKET_ID}/skill_receipts.json",
            ],
            "human_readable": [
                f"stages/{STAGE_ID}/03_reviews/f89_task_force_correction_summary.md",
                "docs/context/current_working_state.md",
            ],
        },
        "gates": {
            "required": required_gates,
            "work_packet_schema_lint": "pending_external_lint",
            "skill_receipt_schema_lint": "pending_external_lint",
            "codex_task_force_review_packet": "pending_materialization",
            "frontier_extra_due_check": "existing_f89_not_due_referenced",
            "frontier_five_stage_direction_synthesis": "existing_f89_record_referenced",
            "frontier_topic_rotation_check": "existing_f89_record_referenced",
            "state_sync_audit": "pending_external_lint",
            "required_gate_coverage_audit": "pending_external_lint",
            "final_claim_guard": "pending_external_lint",
            "not_applicable_with_reason": {
                "runtime_evidence_gate": "outside claim surface; no runtime/materialization/economics claim and no meaningful candidate",
            },
        },
        "final_claim_policy": {
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "claim_vocabulary_reference": "docs/agent_control/claim_vocabulary.yaml",
        },
    }


def build_receipts(now: str, produced_artifacts: list[str]) -> list[dict[str, Any]]:
    task_force_receipt = build_task_force_receipt(now)
    reentry = {
        "packet_id": PACKET_ID,
        "skill": "obsidian-reentry-read",
        "status": "executed",
        "source_current_truth_docs": [
            "AGENTS.md",
            "docs/policies/reentry_order.md",
            "docs/workspace/workspace_state.yaml",
            "docs/context/current_working_state.md",
            f"stages/{STAGE_ID}/04_selected/selection_status.md",
        ],
        "active_stage": STAGE_ID,
        "current_run": CURRENT_RUN_ID,
        "detected_conflicts": ["f89a_f89b_task_force_not_triggered_records_require_append_only_correction"],
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "receipt_path": repo(REVIEW_DIR / "f89_task_force_correction_reentry_receipt.json"),
    }
    stage_transition = {
        "packet_id": PACKET_ID,
        "skill": "obsidian-stage-transition",
        "status": "executed",
        "source_current_truth_docs": [
            "docs/workspace/workspace_state.yaml",
            "docs/context/current_working_state.md",
            f"stages/{STAGE_ID}/04_selected/selection_status.md",
        ],
        "changed_or_checked_docs": [
            "docs/workspace/workspace_state.yaml",
            "docs/context/current_working_state.md",
            f"stages/{STAGE_ID}/04_selected/selection_status.md",
            f"stages/{STAGE_ID}/03_reviews/review_index.md",
        ],
        "detected_conflicts": ["previous_task_force_not_triggered_record_lowered_by_correction"],
        "canonical_state_after": {
            "active_stage": STAGE_ID,
            "current_run_id": CURRENT_RUN_ID,
            "latest_completed_run_id": LATEST_COMPLETED_RUN_ID,
            "task_force_status": "correction_recorded_actual_calls_no_retroactive_review_pass",
            "runtime_authority": "not_claimed",
        },
        "allowed_claims": ["current_truth_task_force_boundary_synced"],
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "receipt_path": repo(REVIEW_DIR / "f89_task_force_correction_stage_transition_receipt.json"),
    }
    artifact_lineage = {
        "packet_id": PACKET_ID,
        "skill": "obsidian-artifact-lineage",
        "status": "executed",
        "source_inputs": [
            "docs/agent_control/codex_task_force_registry.yaml",
            "docs/agent_control/work_family_registry.yaml",
            "docs/policies/agent_trigger_policy.md",
            "docs/agent_control/packets/frontier89A_stage_open_runtime_trade_list_adverse_selection_teacher_v1/work_packet.yaml",
            "docs/agent_control/packets/frontier89B_deal_path_adverse_selection_proxy_scout_v1/work_packet.yaml",
        ],
        "produced_artifacts": produced_artifacts,
        "raw_evidence": ["actual_subagent_calls from multi_agent_v1.spawn_agent notifications"],
        "machine_readable": [
            f"stages/{STAGE_ID}/03_reviews/f89_task_force_correction_review_receipt.json",
            f"docs/agent_control/packets/{PACKET_ID}/skill_receipts.json",
        ],
        "human_readable": [
            f"stages/{STAGE_ID}/03_reviews/f89_task_force_correction_summary.md",
            "docs/context/current_working_state.md",
        ],
        "hashes_or_missing_reasons": [
            {"path": "docs/agent_control/codex_task_force_registry.yaml", "status": "source_read"},
            {"path": "docs/agent_control/work_family_registry.yaml", "status": "source_read"},
        ],
        "lineage_boundary": "Task Force correction evidence only; no runtime/economics or authority evidence.",
        "receipt_path": repo(REVIEW_DIR / "f89_task_force_correction_artifact_lineage_receipt.json"),
    }
    claim_discipline = {
        "packet_id": PACKET_ID,
        "skill": "obsidian-claim-discipline",
        "status": "executed",
        "requested_claims": ALLOWED_CLAIMS,
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "final_status": "correction_recorded_no_retroactive_review_pass_no_authority",
        "receipt_path": repo(REVIEW_DIR / "f89_task_force_correction_claim_discipline_receipt.json"),
    }
    return [stage_transition, reentry, artifact_lineage, task_force_receipt, claim_discipline]


def update_review_index(now: str) -> None:
    path = REVIEW_DIR / "review_index.md"
    base = (
        io_path(path).read_text(encoding="utf-8-sig")
        if io_path(path).exists()
        else "# F89 Review Index(F89 검토 색인)\n\n"
    )
    marker = "f89_task_force_correction_review_receipt.json"
    if marker in base:
        return
    addition = f"""
## Task Force Correction(태스크포스 정정) - {now}

- `stages/{STAGE_ID}/03_reviews/f89_task_force_correction_review_receipt.json`
- `stages/{STAGE_ID}/03_reviews/f89_task_force_correction_summary.md`
- `stages/{STAGE_ID}/03_reviews/f89_task_force_correction_gate.json`
- `docs/agent_control/packets/{PACKET_ID}/work_packet.yaml`
"""
    write_md(path, base.rstrip() + "\n" + addition)


def update_changelogs(now: str) -> None:
    entry = f"""<!-- {PACKET_ID} -->

## {now} - F89 Task Force Correction(F89 태스크포스 정정)

- Action(행동): F89A/F89B missed Task Force actual calls(누락된 태스크포스 실제 호출)을 append-only correction receipt(추가 전용 정정 영수증)로 기록했다.
- Effect(효과): selected agents 5/5 actual_subagent_calls(선택 요원 5/5 실제 하위요원 호출)를 남겼지만 retroactive reviewed/verified/pass(소급 검토됨/검증됨/통과)는 주장하지 않는다.
- Boundary(경계): `{CLAIM_BOUNDARY}`.
"""
    for path in [ROOT / "docs" / "workspace" / "changelog.md", ROOT / "docs" / "CHANGELOG.md"]:
        current = io_path(path).read_text(encoding="utf-8-sig") if io_path(path).exists() else ""
        if PACKET_ID not in current:
            write_md(path, entry + "\n" + current)


def main() -> int:
    now = utc_now()
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    PACKET_DIR.mkdir(parents=True, exist_ok=True)

    produced = [
        f"stages/{STAGE_ID}/03_reviews/f89_task_force_correction_review_receipt.json",
        f"stages/{STAGE_ID}/03_reviews/f89_task_force_correction_summary.md",
        f"stages/{STAGE_ID}/03_reviews/f89_task_force_correction_gate.json",
        f"docs/agent_control/packets/{PACKET_ID}/work_packet.yaml",
        f"docs/agent_control/packets/{PACKET_ID}/skill_receipts.json",
        f"docs/agent_control/packets/{PACKET_ID}/closeout_gate.json",
    ]

    write_current_truth(now)
    work_packet = build_work_packet(now)
    write_yaml(PACKET_DIR / "work_packet.yaml", work_packet)

    receipts = build_receipts(now, produced)
    for receipt in receipts:
        write_json(ROOT / receipt["receipt_path"], receipt)
    write_json(PACKET_DIR / "skill_receipts.json", {"packet_id": PACKET_ID, "primary_skill": "obsidian-stage-transition", "claim_boundary": CLAIM_BOUNDARY, "receipts": receipts})

    summary = f"""# F89 Task Force Correction(F89 태스크포스 정정)

Updated(갱신): {now}

Action(행동): F89A/F89B에서 누락된 Task Force actual_subagent_calls(태스크포스 실제 하위요원 호출)를 현재 packet(묶음)에 append-only(추가 전용)로 기록했다.

Effect(효과): 기존 not_triggered(미트리거) 판단은 retroactive pass(소급 통과)가 아니라 incorrect_not_triggered correction(잘못된 미트리거 정정)으로 남는다.

Actual calls(실제 호출): agent_01/04/05/07/08 selected agents(선택 요원) 5명.

Boundary(경계): `{CLAIM_BOUNDARY}`.

F89C trigger rule(F89C 트리거 규칙): repair/rotation closeout(수리/회전 마감) 또는 reviewed/pass(검토/통과) claim(주장)이 생기면 관련 agents(요원)를 실제 호출한다. Meaningful materialization candidate(의미 있는 물질화 후보)가 생기면 cost(비용)가 아니라 같은 packet(묶음) 안에서 MT5 Strategy Tester runtime probe(MT5 전략 테스터 런타임 탐침)를 시도한다.
"""
    write_md(REVIEW_DIR / "f89_task_force_correction_summary.md", summary)

    task_force_gate = {
        "audit_name": "codex_task_force_review_packet",
        "status": "actual_calls_recorded_no_retroactive_review_claim",
        "packet_id": PACKET_ID,
        "counts": {"selected_agents": 5, "actual_subagent_calls": 5, "full_roster_call": False},
        "allowed_claims": ["task_force_actual_calls_recorded", "incorrect_not_triggered_correction_recorded"],
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(REVIEW_DIR / "f89_task_force_correction_gate.json", task_force_gate)
    write_json(PACKET_DIR / "codex_task_force_review_packet.json", task_force_gate)

    update_review_index(now)
    update_changelogs(now)

    work_packet_lint = run_json(
        [
            "python",
            "-m",
            "foundation.control_plane.work_packet_schema_lint",
            str(PACKET_DIR / "work_packet.yaml"),
            "--output-json",
            str(PACKET_DIR / "work_packet_schema_lint.json"),
        ],
        PACKET_DIR / "work_packet_schema_lint.json",
    )
    skill_lint = run_json(
        [
            "python",
            "-m",
            "foundation.control_plane.skill_receipt_schema_lint",
            str(PACKET_DIR / "skill_receipts.json"),
            "--output-json",
            str(PACKET_DIR / "skill_receipt_schema_lint.json"),
        ],
        PACKET_DIR / "skill_receipt_schema_lint.json",
    )
    state_sync = run_json(
        [
            "python",
            "-m",
            "foundation.control_plane.state_sync_audit",
            "--root",
            ".",
            "--output-json",
            str(PACKET_DIR / "state_sync_audit.json"),
        ],
        PACKET_DIR / "state_sync_audit.json",
    )

    closeout_gate = {
        "packet_id": PACKET_ID,
        "status": "recorded_with_lowered_claim_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "audits": [
            {"audit_name": "work_packet_schema_lint", "status": work_packet_lint["status"], "path": repo(PACKET_DIR / "work_packet_schema_lint.json")},
            {"audit_name": "skill_receipt_schema_lint", "status": skill_lint["status"], "path": repo(PACKET_DIR / "skill_receipt_schema_lint.json")},
            {"audit_name": "codex_task_force_review_packet", "status": task_force_gate["status"], "path": repo(PACKET_DIR / "codex_task_force_review_packet.json")},
            {"audit_name": "frontier_extra_due_check", "status": "pass_not_due_existing_f89", "path": f"stages/{STAGE_ID}/03_reviews/f89b_frontier_extra_due_check.json"},
            {"audit_name": "frontier_five_stage_direction_synthesis", "status": "pass_existing_f89", "path": f"stages/{STAGE_ID}/03_reviews/f89b_frontier_five_stage_direction_synthesis.json"},
            {"audit_name": "frontier_topic_rotation_check", "status": "pass_existing_f89", "path": f"stages/{STAGE_ID}/03_reviews/f89b_frontier_topic_rotation_check.json"},
            {"audit_name": "state_sync_audit", "status": state_sync["status"], "path": repo(PACKET_DIR / "state_sync_audit.json")},
            {"audit_name": "required_gate_coverage_audit", "status": "pending", "path": repo(PACKET_DIR / "required_gate_coverage_audit.json")},
        ],
        "final_claim_guard": {
            "audit_name": "final_claim_guard",
            "status": "pending",
            "path": repo(PACKET_DIR / "final_claim_guard.json"),
        },
    }
    write_json(PACKET_DIR / "closeout_gate.json", closeout_gate)

    gate_coverage = run_json(
        [
            "python",
            "-m",
            "foundation.control_plane.required_gate_coverage_audit",
            "--work-packet",
            str(PACKET_DIR / "work_packet.yaml"),
            "--closeout-gate",
            str(PACKET_DIR / "closeout_gate.json"),
            "--output-json",
            str(PACKET_DIR / "required_gate_coverage_audit.json"),
        ],
        PACKET_DIR / "required_gate_coverage_audit.json",
    )
    closeout_gate["audits"][-1]["status"] = gate_coverage["status"]

    tf_audit = AuditResult(
        audit_name="codex_task_force_review_packet",
        status=task_force_gate["status"],
        counts=task_force_gate["counts"],
        allowed_claims=tuple(task_force_gate["allowed_claims"]),
        forbidden_claims=tuple(FORBIDDEN_CLAIMS),
    )
    final_claim_guard = guard_final_claims(
        requested_claims=ALLOWED_CLAIMS,
        audit_results=[
            audit_from_dict(work_packet_lint),
            audit_from_dict(skill_lint),
            audit_from_dict(state_sync),
            audit_from_dict(gate_coverage),
            tf_audit,
        ],
    ).to_dict()
    write_json(PACKET_DIR / "final_claim_guard.json", final_claim_guard)
    write_json(REVIEW_DIR / "f89_task_force_correction_final_claim_guard.json", final_claim_guard)

    closeout_gate["final_claim_guard"] = {
        "audit_name": "final_claim_guard",
        "status": final_claim_guard["status"],
        "path": repo(PACKET_DIR / "final_claim_guard.json"),
    }
    write_json(PACKET_DIR / "closeout_gate.json", closeout_gate)

    write_json(REVIEW_DIR / "f89_task_force_correction_required_gate_coverage_audit.json", gate_coverage)
    write_json(REVIEW_DIR / "f89_task_force_correction_state_sync_audit.json", state_sync)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
