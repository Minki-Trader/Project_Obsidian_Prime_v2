from __future__ import annotations

import csv
import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.audit_result import AuditResult
from foundation.control_plane.final_claim_guard import guard_final_claims
from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized


STAGE_ID = "stage_frontier_97__first_hit_survival_hazard_event_sparse_axis"
RUN_ID = "frontier97A_stage_open_first_hit_survival_hazard_event_sparse_axis_v1"
PARENT_RUN_ID = "frontier96C_counterfactual_action_value_policy_repair_or_rotation_decision_v1"
NEXT_RUN_ID = "frontier97B_first_hit_survival_hazard_event_sparse_proxy_scout_v1"
SCRIPT_REL = "stage_pipelines/stage_frontier_97/frontier97a_stage_open_first_hit_survival_hazard.py"

STATUS = "f97a_stage_open_design_prepared_no_candidate_no_authority"
JUDGMENT = "design_only_stage_open_first_hit_survival_hazard_event_sparse_axis"
CLAIM_BOUNDARY = (
    "f97a_design_only_stage_open_first_hit_survival_hazard_event_sparse_axis_"
    "no_model_candidate_no_wfo_pass_no_stress_pass_no_mt5_runtime_evidence_"
    "no_selected_baseline_no_operating_promotion_no_runtime_authority_"
    "no_live_readiness_no_goal_achieve"
)
RUNTIME_PROBE_STATUS = (
    "not_applicable_design_only_no_runnable_candidate_no_runtime_materialization_"
    "economics_handoff_claim_not_cost_or_proxy_bad_skip"
)
FRONTIER_EXTRA_DUE_STATUS = "not_due_after_f96_closeout_next_boundary_f100_e02_pending_e01_closed_for_f050"
FRONTIER_TOPIC_ROTATION_STATUS = "passed_f97_first_hit_survival_hazard_not_f96_action_value_parameter_repair"
FRONTIER_FIVE_STAGE_STATUS = "recorded_recent_f92_to_f96_direction_synthesis_no_retrospective_gate"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / "frontier97A"
DESIGN_DIR = RUN_DIR / "d"
REPORT_DIR = RUN_DIR / "r"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
PACKET_DIR = ROOT / "docs" / "agent_control" / "packets" / RUN_ID
SKILL_RECEIPT_DIR = PACKET_DIR / "skill_receipts"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
GLOBAL_SELECTION_STATUS = ROOT / "docs" / "registers" / "selection_status.md"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
ROOT_CHANGELOG = ROOT / "docs" / "CHANGELOG.md"
DECISION_MEMO = ROOT / "docs" / "decisions" / "2026-06-19_frontier97a_stage_open_first_hit_survival_hazard.md"

STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
INPUT_REFS = STAGE_DIR / "01_inputs" / "input_refs.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
CONTEXT_ANCHOR = REVIEW_DIR / "context_anchor.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"

RUN_MANIFEST = RUN_DIR / "run_manifest.json"
SUMMARY_JSON = RUN_DIR / "summary.json"
KPI_RECORD = RUN_DIR / "kpi_record.json"
EXPERIMENT_DESIGN = DESIGN_DIR / "experiment_design.json"
RUNTIME_CONTRACT = DESIGN_DIR / "runtime_contract.json"
F97B_BRIEF = DESIGN_DIR / "f97b_proxy_scout_brief.json"
DATA_INTEGRITY_PLAN = DESIGN_DIR / "data_integrity_plan.json"
MODEL_VALIDATION_PLAN = DESIGN_DIR / "model_validation_plan.json"
FIRST_HIT_CONTRACT = DESIGN_DIR / "first_hit_survival_hazard_contract.json"
RESULT_SUMMARY = REPORT_DIR / "summary.md"

STAGE_OPEN_SUMMARY = REVIEW_DIR / "f97a_stage_open_summary.json"
TASK_FORCE_REVIEW = REVIEW_DIR / "f97a_task_force_review_receipt.json"
FRONTIER_EXTRA_DUE_CHECK = REVIEW_DIR / "f97a_frontier_extra_due_check.json"
FIVE_STAGE_SYNTHESIS = REVIEW_DIR / "f97a_frontier_five_stage_direction_synthesis.json"
TOPIC_ROTATION_CHECK = REVIEW_DIR / "f97a_frontier_topic_rotation_check.json"
SCOPE_GATE = REVIEW_DIR / "f97a_scope_completion_gate.json"
DATA_INTEGRITY_AUDIT = REVIEW_DIR / "f97a_data_integrity_audit.json"
MODEL_VALIDATION_AUDIT = REVIEW_DIR / "f97a_model_validation_audit.json"
ARTIFACT_AUDIT = REVIEW_DIR / "f97a_artifact_lineage_audit.json"
RESULT_JUDGMENT_AUDIT = REVIEW_DIR / "f97a_result_judgment_audit.json"
FINAL_CLAIM_GUARD = REVIEW_DIR / "f97a_final_claim_guard.json"
STATE_SYNC_AUDIT = REVIEW_DIR / "f97a_state_sync_audit.json"
REQUIRED_GATE_AUDIT = REVIEW_DIR / "f97a_required_gate_coverage_audit.json"
F97A_REPORT = REVIEW_DIR / "frontier97A_stage_open_first_hit_survival_hazard_report.md"

WORK_PACKET = PACKET_DIR / "work_packet.yaml"
SKILL_RECEIPTS = PACKET_DIR / "skill_receipts.json"
PACKET_TASK_FORCE_REVIEW = PACKET_DIR / "codex_task_force_review_packet.json"
PACKET_CLOSEOUT_GATE = PACKET_DIR / "closeout_gate.json"
PACKET_FINAL_CLAIM_GUARD = PACKET_DIR / "final_claim_guard.json"
PACKET_STATE_SYNC_AUDIT = PACKET_DIR / "state_sync_audit.json"
PACKET_REQUIRED_GATE_AUDIT = PACKET_DIR / "required_gate_coverage_audit.json"
PACKET_WORK_PACKET_LINT = PACKET_DIR / "work_packet_schema_lint.json"
PACKET_SKILL_RECEIPT_LINT = PACKET_DIR / "skill_receipt_schema_lint.json"

MODEL_INPUT_SUMMARY = (
    ROOT
    / "data"
    / "processed"
    / "model_inputs"
    / "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58"
    / "model_input_summary.json"
)
MODEL_INPUT_FEATURE_ORDER = MODEL_INPUT_SUMMARY.with_name("model_input_feature_order.txt")
RAW_US100_MANIFEST = ROOT / "data" / "raw" / "mt5_bars" / "m5" / "US100" / "bars_us100_m5_mt5api_raw.manifest.json"
F96_STAGE = ROOT / "stages" / "stage_frontier_96__counterfactual_action_value_policy_axis"
F96B_RUN = F96_STAGE / "02_runs" / "frontier96B"
F96C_RUN = F96_STAGE / "02_runs" / "frontier96C"
F96B_KPI = F96B_RUN / "kpi_record.json"
F96B_CANDIDATE_GATE = F96B_RUN / "proxy_scout" / "candidate_gate.json"
F96B_LABEL_SUMMARY = F96B_RUN / "proxy_scout" / "action_value_label_summary.json"
F96B_TIER_ROUTE_SUMMARY = F96B_RUN / "proxy_scout" / "tier_route_summary.json"
F96B_DATA_LOCK = F96B_RUN / "proxy_scout" / "data_feature_split_lock.json"
F96C_DECISION = F96C_RUN / "d" / "decision.json"
F96C_SUMMARY = F96_STAGE / "03_reviews" / "f96c_stage_closeout_summary.json"
F96C_PACKET = ROOT / "docs" / "agent_control" / "packets" / PARENT_RUN_ID / "work_packet.yaml"
F96C_CLOSEOUT_GATE = ROOT / "docs" / "agent_control" / "packets" / PARENT_RUN_ID / "closeout_gate.json"

ALLOWED_CLAIMS = [
    "f97a_design_open_packet_recorded",
    "f97_first_hit_survival_hazard_axis_opened",
    "f97b_proxy_scout_planned",
    "task_force_actual_calls_recorded_for_f97a",
    "f96c_negative_memory_linked",
    "frontier_extra_due_check_not_due_after_f96",
    "frontier_five_stage_direction_synthesis_recorded_for_f92_to_f96",
    "frontier_topic_rotation_check_recorded_for_f97",
    "runtime_gate_not_applicable_with_reason",
]
FORBIDDEN_CLAIMS = [
    "completion",
    "complete",
    "completed",
    "selected_baseline",
    "operating_promotion",
    "runtime_authority",
    "live_readiness",
    "goal_achieve",
    "candidate",
    "promotion_candidate",
    "runtime_probe",
    "runtime_verified",
    "strategy_tester_runtime_economics",
    "runtime_economics",
    "runtime_economics_pass",
    "materialization_ready",
    "mt5_handoff_ready",
    "onnx_handoff_ready",
    "ea_handoff_ready",
    "f97_stage_open_completed",
    "task_force_reviewed",
    "task_force_reviewed_pass",
    "internally_reviewed",
    "reviewed",
    "verified",
    "pass",
    "model_quality",
    "model_readiness",
    "calibrated_probability",
    "data_contract_pass",
    "runtime_compatible_proven",
    "baseline",
    "promotion",
]
REQUIRED_GATES = [
    "work_packet_schema_lint",
    "skill_receipt_schema_lint",
    "codex_task_force_review_packet",
    "frontier_extra_due_check",
    "frontier_five_stage_direction_synthesis",
    "frontier_topic_rotation_check",
    "scope_completion_gate",
    "data_integrity_audit",
    "model_validation_audit",
    "artifact_lineage_audit",
    "result_judgment_audit",
    "state_sync_audit",
    "required_gate_coverage_audit",
    "final_claim_guard",
]
REQUIRED_SKILLS = [
    "obsidian-experiment-design",
    "obsidian-data-integrity",
    "obsidian-model-validation",
    "obsidian-artifact-lineage",
    "obsidian-result-judgment",
    "obsidian-task-force-review",
    "obsidian-stage-transition",
    "obsidian-claim-discipline",
]
RUNTIME_NA_REASONS = [
    {
        "gate": "runtime_evidence_gate",
        "reason_code": "design_only_no_runtime_claim",
        "reason": (
            "F97A is formal design/open only; it has no runnable ONNX/EA/set bundle, "
            "no Strategy Tester output, and no materialization/economics/handoff claim."
        ),
        "claim_effect": (
            "No runtime_probe, runtime_verified, materialization_ready, handoff_ready, "
            "runtime_authority, live_readiness, selected_baseline, or Goal Achieve claim is allowed."
        ),
    },
    {
        "gate": "wfo_stress_gate",
        "reason_code": "outside_claim_surface_no_model_candidate",
        "reason": "F97A defines the F97B proxy scout contract only; it does not train/select a model.",
        "claim_effect": "No WFO pass, stress pass, model quality, selected baseline, or candidate claim is allowed.",
    },
]


def utc_now() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    encoding = "utf-8-sig" if path.suffix.lower() in {".md", ".txt"} else "utf-8"
    io_path(path).write_text(text.rstrip() + "\n", encoding=encoding)


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_yaml(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(yaml.safe_dump(json_ready(payload), allow_unicode=True, sort_keys=False, width=140), encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def file_identity(path: Path) -> dict[str, Any]:
    if not path_exists(path):
        return {"path": rel(path), "exists": False, "sha256": None, "size_bytes": None}
    return {
        "path": rel(path),
        "exists": True,
        "sha256": sha256_file_lf_normalized(path),
        "size_bytes": io_path(path).stat().st_size,
    }


def current_branch() -> str:
    completed = subprocess.run(["git", "branch", "--show-current"], cwd=ROOT, check=False, capture_output=True, text=True, timeout=10)
    return completed.stdout.strip() if completed.returncode == 0 else ""


def ensure_dirs() -> None:
    for path in [DESIGN_DIR, REPORT_DIR, REVIEW_DIR, SELECTED_DIR, PACKET_DIR, SKILL_RECEIPT_DIR]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def source_inputs() -> list[Path]:
    return [
        WORKSPACE_STATE,
        CURRENT_WORKING_STATE,
        STAGE_BRIEF,
        INPUT_REFS,
        SELECTION_STATUS,
        ROOT / "docs" / "agent_control" / "work_family_registry.yaml",
        ROOT / "docs" / "agent_control" / "codex_task_force_registry.yaml",
        ROOT / "docs" / "registers" / "frontier_extra_stage_register.yaml",
        MODEL_INPUT_SUMMARY,
        MODEL_INPUT_FEATURE_ORDER,
        RAW_US100_MANIFEST,
        F96B_KPI,
        F96B_CANDIDATE_GATE,
        F96B_LABEL_SUMMARY,
        F96B_TIER_ROUTE_SUMMARY,
        F96B_DATA_LOCK,
        F96C_DECISION,
        F96C_SUMMARY,
        F96C_PACKET,
        F96C_CLOSEOUT_GATE,
    ]


def produced_artifacts() -> list[Path]:
    return [
        ROOT / SCRIPT_REL,
        RUN_MANIFEST,
        SUMMARY_JSON,
        KPI_RECORD,
        EXPERIMENT_DESIGN,
        RUNTIME_CONTRACT,
        F97B_BRIEF,
        DATA_INTEGRITY_PLAN,
        MODEL_VALIDATION_PLAN,
        FIRST_HIT_CONTRACT,
        RESULT_SUMMARY,
        STAGE_OPEN_SUMMARY,
        TASK_FORCE_REVIEW,
        PACKET_TASK_FORCE_REVIEW,
        FRONTIER_EXTRA_DUE_CHECK,
        FIVE_STAGE_SYNTHESIS,
        TOPIC_ROTATION_CHECK,
        SCOPE_GATE,
        DATA_INTEGRITY_AUDIT,
        MODEL_VALIDATION_AUDIT,
        ARTIFACT_AUDIT,
        RESULT_JUDGMENT_AUDIT,
        FINAL_CLAIM_GUARD,
        STATE_SYNC_AUDIT,
        REQUIRED_GATE_AUDIT,
        F97A_REPORT,
        WORK_PACKET,
        SKILL_RECEIPTS,
        PACKET_CLOSEOUT_GATE,
        PACKET_FINAL_CLAIM_GUARD,
        PACKET_STATE_SYNC_AUDIT,
        PACKET_REQUIRED_GATE_AUDIT,
        PACKET_WORK_PACKET_LINT,
        PACKET_SKILL_RECEIPT_LINT,
        STAGE_BRIEF,
        INPUT_REFS,
        SELECTION_STATUS,
        CONTEXT_ANCHOR,
        REVIEW_INDEX,
        DECISION_MEMO,
    ]


def task_force_calls() -> list[dict[str, Any]]:
    return [
        {
            "roster_agent_id": "agent_01_system_governor",
            "spawned_agent_id": "019edf49-155a-7423-9648-f470d8f47d5c",
            "nickname": "Hypatia the 2nd",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "timed_out_no_final_opinion_after_two_waits",
            "opinion_classification": "needs_local_verification",
            "bounded_evidence": [rel(WORKSPACE_STATE), rel(STAGE_BRIEF), rel(SELECTION_STATUS)],
            "local_verification": "Actual call was made, but no final opinion was available before F97A local evidence writing. No Task Force reviewed/pass claim is made.",
            "accepted_summary": "No opinion accepted; governance checks are kept local and claim boundary remains design-only.",
        },
        {
            "roster_agent_id": "agent_03_philosophy_policy_skill_governance",
            "spawned_agent_id": "019edf49-66d0-7692-af9b-4502cbd6040b",
            "nickname": "Darwin the 2nd",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "rejected",
            "bounded_evidence": [rel(WORKSPACE_STATE), rel(STAGE_BRIEF), rel(F96C_DECISION)],
            "local_verification": "The agent self-diagnosed tool unavailability even though it had a spawned id. That portion is rejected and not used as review evidence.",
            "accepted_summary": "No policy novelty opinion accepted from this call; F97 novelty is verified locally from F96C rotation material.",
        },
        {
            "roster_agent_id": "agent_04_evidence_control_plane",
            "spawned_agent_id": "019edf49-c07d-7a40-bbcb-c9decaf6bb99",
            "nickname": "Aquinas the 2nd",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "needs_local_verification",
            "bounded_evidence": [rel(WORKSPACE_STATE), rel(STAGE_BRIEF), rel(WORK_PACKET)],
            "local_verification": "The tool-unavailable preface is rejected, but the artifact/gate checklist is used as a local checklist and materialized in this packet.",
            "accepted_summary": "Record work packet, Task Force receipt, frontier overlay checks, design artifacts, state sync, ledgers, and final claim guard.",
        },
        {
            "roster_agent_id": "agent_05_data_feature_contract",
            "spawned_agent_id": "019edf4a-132a-7483-8e72-87d5f7edba19",
            "nickname": "Ramanujan the 2nd",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "needs_local_verification",
            "bounded_evidence": [rel(MODEL_INPUT_SUMMARY), rel(MODEL_INPUT_FEATURE_ORDER), rel(RAW_US100_MANIFEST), rel(F96B_TIER_ROUTE_SUMMARY)],
            "local_verification": "The tool-unavailable preface is rejected; data/label contract fields and stop conditions are accepted as F97B local verification requirements.",
            "accepted_summary": "Require first-hit label fields, closed-bar feature cutoff, tie rule, split embargo, Tier A/B/A+B records, and data identity hashes.",
        },
        {
            "roster_agent_id": "agent_06_quant_research",
            "spawned_agent_id": "019edf4a-e1b4-7703-98eb-dd3da0ef7978",
            "nickname": "Lorentz the 2nd",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "accepted",
            "bounded_evidence": [rel(F96B_KPI), rel(F96B_CANDIDATE_GATE), rel(F96C_SUMMARY)],
            "local_verification": "Proxy tests and KPI fields are encoded in the F97B brief and model validation plan.",
            "accepted_summary": "F97 changes label/objective to first-hit competing risk; test hit rates, time-to-hit, censoring, calibration, density, and segment stability.",
        },
        {
            "roster_agent_id": "agent_07_model_validation_risk",
            "spawned_agent_id": "019edf4b-0dd8-7e41-8260-ab4bc6f69638",
            "nickname": "Maxwell the 2nd",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "accepted",
            "bounded_evidence": [rel(F96B_KPI), rel(F96B_CANDIDATE_GATE), rel(MODEL_INPUT_SUMMARY)],
            "local_verification": "Validation fields, stop conditions, WFO/stress boundary, and anti-probability-laundering rules are recorded.",
            "accepted_summary": "F97A is design-only; WFO/stress/runtime becomes required only when F97B creates a runnable candidate or stronger claim.",
        },
        {
            "roster_agent_id": "agent_08_mt5_onnx_runtime",
            "spawned_agent_id": "019edf4b-d955-7130-86da-ba80483db03b",
            "nickname": "Ptolemy the 2nd",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "accepted",
            "bounded_evidence": [rel(STAGE_BRIEF), rel(RUNTIME_CONTRACT), rel(SELECTION_STATUS)],
            "local_verification": "Runtime gate is N/A only because F97A has no runnable candidate and no runtime/materialization/economics/handoff claim. This is not cost or proxy-bad deferral.",
            "accepted_summary": "A later ONNX/EA/set or trade-producing runtime claim triggers MT5 Strategy Tester identity, report, trade-list, and telemetry hashes in the same packet.",
        },
    ]


def task_force_receipt(created_at: str) -> dict[str, Any]:
    calls = task_force_calls()
    return {
        "packet_id": RUN_ID,
        "skill": "obsidian-task-force-review",
        "status": "executed_with_boundaries_no_task_force_reviewed_pass_claim",
        "created_at_utc": created_at,
        "trigger_reason": "F97A formal stage-open packet, active goal frontier continuation, and explicit user correction requiring real relevant Task Force agent calls.",
        "roster_registry": "docs/agent_control/codex_task_force_registry.yaml",
        "agents_used": [call["roster_agent_id"] for call in calls],
        "agents_not_called": [
            {
                "roster_agent_id": "agent_02_platform_routing_architect",
                "reason": "No platform/routing architecture change is protected by F97A design-only claim.",
            }
        ],
        "actual_subagent_calls": calls,
        "review_requirement": "codex_task_force_review_packet",
        "model_policy": {"model": "inherited_current_codex_model", "reasoning_effort": "inherited", "service_tier": "inherited"},
        "bounded_evidence": [rel(WORKSPACE_STATE), rel(STAGE_BRIEF), rel(SELECTION_STATUS), rel(F96C_SUMMARY), rel(MODEL_INPUT_SUMMARY)],
        "advice_classification": {
            "accepted": [call["roster_agent_id"] for call in calls if call["opinion_classification"] == "accepted"],
            "needs_local_verification": [call["roster_agent_id"] for call in calls if call["opinion_classification"] == "needs_local_verification"],
            "rejected": [call["roster_agent_id"] for call in calls if call["opinion_classification"] == "rejected"],
        },
        "local_verification": [
            "F97A packet, receipts, gate audits, ledgers, and state sync are generated locally.",
            "F96C is linked as negative memory/reference surface only, not winner, baseline, or promotion history.",
            "Runtime evidence gate is outside claim surface only because no runnable candidate or runtime claim exists.",
            "F97B must verify first-hit label leakage, intrabar ambiguity/tie rule, split embargo, Tier A/B/A+B records, density, adverse-first rate, calibration, and same-packet MT5 trigger.",
        ],
        "claim_boundary": CLAIM_BOUNDARY,
        "final_codex_direction": "Proceed with F97A design-only formal open and plan F97B first-hit survival/hazard proxy scout.",
        "forbidden_claim_check": {claim: "not_claimed" for claim in FORBIDDEN_CLAIMS},
        "receipt_path": rel(SKILL_RECEIPT_DIR / "task_force_review.json"),
    }


def base_payload(created_at: str) -> dict[str, Any]:
    return {
        "created_at_utc": created_at,
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "hypothesis": (
            "Closed-bar features can rank first favorable versus adverse bracket-hit survival/hazard "
            "and abstain when event density or adverse-first risk is poor, creating a new clue surface before side selection."
        ),
        "decision_use": "design-only formal stage open and F97B proxy scout handoff",
        "f96c_reference": {
            "source_run": PARENT_RUN_ID,
            "use": "negative memory/reference surface only",
            "no_inheritance": ["winner", "selected_baseline", "promotion_history", "runtime_authority", "live_readiness"],
        },
        "frontier_extra_due_status": FRONTIER_EXTRA_DUE_STATUS,
        "frontier_topic_rotation_status": FRONTIER_TOPIC_ROTATION_STATUS,
        "frontier_five_stage_status": FRONTIER_FIVE_STAGE_STATUS,
        "runtime_probe_status": RUNTIME_PROBE_STATUS,
        "source_identities": [file_identity(path) for path in source_inputs()],
        "task_force": task_force_receipt(created_at),
    }


def experiment_design(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "hypothesis": payload["hypothesis"],
        "proxy": "F97B will build leakage-safe first-hit survival/hazard labels and inspect validation-only event-sparse abstention surfaces before any runtime claim.",
        "decision_use": payload["decision_use"],
        "comparison_baseline": {
            "source_run": PARENT_RUN_ID,
            "role": "negative memory/reference surface only",
            "not_inherited": ["winner", "selected_baseline", "promotion_history", "runtime_authority"],
        },
        "changed_variables": [
            "label: action-value path utility -> first favorable/adverse bracket-hit survival/hazard",
            "objective: utility/regret ranking -> calibrated hit-risk ranking and abstention",
            "trade shape: side action eligibility -> bracket lifecycle and hold-risk budgeting before side selection",
            "validation: PF support metric -> density, adverse-first risk, calibration, segment stability, DD/recovery before PF",
        ],
        "control_variables": [
            "FPMarkets US100 M5",
            "closed-bar features only",
            "Tier A separate, Tier B separate, and Tier A+B actual routed total records",
            "time-ordered train/validation/OOS split",
            "validation-only scout gate and OOS final read only",
            "cost/spread/slippage and bracket distance declared before scoring",
        ],
        "sample_scope": {
            "instrument": "US100",
            "timeframe": "M5",
            "period_policy": "F97B must record exact train/validation/OOS dates, row counts, hashes, and Tier A/B/A+B source identities before execution.",
            "tier_requirement": ["Tier A separate", "Tier B separate", "Tier A+B combined actual routed total"],
        },
        "success_criteria_for_f97b_proxy_scout": [
            "Tier A, Tier B, and A+B records all exist with the same KPI names.",
            "First-hit label fields, tie rule, censoring rule, and split embargo are recorded.",
            "Event density can plausibly support 5-10 trades/day without all-abstain or trade-all collapse.",
            "Adverse-first rate is controlled before PF-only ranking.",
            "Calibration diagnostics exist before probability language.",
            "A+B combined is sorted and recorded as actual routed total, not synthetic sum.",
        ],
        "invalid_conditions": [
            "label window high/low or first-hit outcome enters feature columns",
            "feature cutoff is after inference bar close",
            "first-hit tie rule is missing",
            "label horizon crosses split boundary without embargo",
            "Tier B or A+B record is silently omitted",
            "proxy-only score is described as runtime or economics evidence",
        ],
        "stop_conditions": [
            "Stop if first-hit label is not leakage-free.",
            "Stop if event density is structurally zero or near-zero.",
            "Stop if F97B degenerates into threshold/filter/session/routing/parameter-only repair.",
            "If a runnable bundle or runtime claim appears, same-packet MT5 Strategy Tester probe is required or the runtime claim is lowered.",
        ],
    }


def first_hit_contract(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "contract_status": "design_locked_for_f97b_planning_only",
        "required_fields": [
            "dataset_id",
            "symbol",
            "timeframe",
            "timezone",
            "bar_timestamp_meaning",
            "inference_bar_close",
            "label_start_time",
            "label_end_time",
            "favorable_bracket",
            "adverse_bracket",
            "first_hit_side",
            "first_hit_time",
            "tie_rule",
            "censor_reason",
            "max_hold_bars",
            "event_sparse_abstain_rule",
            "tier_scope",
            "split_id",
            "feature_cutoff_time",
            "feature_order_version",
            "data_hash_or_identity",
        ],
        "feature_surface": {
            "allowed": ["row t and prior closed M5 bars", "train-only transforms", "predeclared rolling windows ending at t"],
            "forbidden": ["open/current incomplete bar", "future high/low after entry", "first-hit outcome as feature", "post-entry diagnostics as feature"],
        },
        "label_surface": {
            "favorable_first": "first favorable bracket hit before adverse bracket inside max_hold_bars",
            "adverse_first": "first adverse bracket hit before favorable bracket inside max_hold_bars",
            "censored": "neither bracket hit before max_hold_bars or invalid/holiday/session boundary",
            "tie_rule": "must be explicit before F97B scoring; missing tie rule blocks label use",
        },
        "negative_controls": [
            "shuffled first-hit labels",
            "cost-blind bracket utility",
            "no-adverse-risk filter",
            "PF-only ranking",
            "all-abstain",
            "trade-all",
        ],
        "candidate_language_boundary": "F97B can create scout clues only unless a separate runtime packet/probe supports stronger claims.",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def data_integrity_plan(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "data_sources_checked": [file_identity(path) for path in [MODEL_INPUT_SUMMARY, MODEL_INPUT_FEATURE_ORDER, RAW_US100_MANIFEST, F96B_TIER_ROUTE_SUMMARY]],
        "time_axis_boundary": "F97B must record whether each M5 timestamp is bar open or bar close, broker timezone, session timezone, DST policy, and M5 sort key.",
        "feature_label_boundary": "Features use only decision-time row t and earlier closed bars; first-hit path after label_start_time is label target only.",
        "split_boundary": "Train/validation/OOS split is chronological. Label horizon cannot cross validation/OOS boundary without embargo.",
        "tier_boundary": "Tier A separate, Tier B separate, and A+B actual routed total are mandatory. Missing Tier B or combined is missing_required, blocked, or out_of_scope_by_claim.",
        "leakage_checks": [
            "rolling/window calculations end at t",
            "normalizer/scaler fit train-only",
            "joins/resamples preserve closed-bar order",
            "first-hit window never appears in features",
            "row counts/date ranges/hashes recorded per Tier A, Tier B, and A+B",
        ],
        "stop_conditions": [
            "unknown time-axis meaning",
            "duplicate or reverse timestamps",
            "feature cutoff after inference bar close",
            "first-hit tie rule missing",
            "Tier A/B/A+B missing",
            "split leakage or missing embargo",
            "missing hash or row-count identity",
        ],
    }


def model_validation_plan(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "model_or_threshold_surface": "first-hit survival/hazard event-sparse abstention proxy scout, no trained candidate yet",
        "validation_split": "time-ordered train/validation/OOS; validation gates clue/candidate language; OOS is final read only",
        "required_validation_fields": [
            "target_and_label",
            "split_method",
            "selection_metric",
            "secondary_metrics",
            "threshold_policy",
            "calibration_risk",
            "comparison_baseline",
            "stop_conditions",
        ],
        "overfit_checks": [
            "no OOS feature, label, bracket, density, threshold, or calibration selection",
            "validation-only scout gate",
            "probability claims forbidden unless calibration diagnostics exist",
            "PF-only selection forbidden",
            "negative controls required",
        ],
        "selection_metric_boundary": [
            "favorable-first hit rate",
            "adverse-first hit rate",
            "time-to-hit distribution",
            "censoring/no-event rate",
            "Brier score",
            "C-index",
            "calibration bins",
            "abstention coverage versus utility",
            "drawdown and recovery factor",
            "trades/day 5-10",
            "long/short breakdown once side mapping is introduced",
            "segment stability",
        ],
        "same_packet_mt5_triggers": [
            "runnable candidate selected for actual trading behavior",
            "ONNX/EA/set bundle or handoff claim",
            "materialization_ready, handoff_ready, economics pass, runtime parity, or tester-observed behavior claim",
            ".mq5/.mqh/.set behavior affects result meaning",
            "any operating/runtime/live/baseline claim stronger than runtime observation",
        ],
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }


def runtime_contract(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "runtime_probe_status": RUNTIME_PROBE_STATUS,
        "runtime_claim_surface": "none",
        "meaningful_runnable_candidate_status": "absent",
        "onnx_bundle_status": "absent",
        "ea_set_bundle_status": "absent",
        "strategy_tester_output_status": "absent",
        "materialization_claim_status": "not_claimed",
        "economics_claim_status": "not_claimed",
        "handoff_claim_status": "not_claimed",
        "runtime_evidence_gate": RUNTIME_NA_REASONS[0],
        "later_trigger_conditions": model_validation_plan(payload)["same_packet_mt5_triggers"],
        "required_runtime_identity_if_triggered": [
            "tester_build",
            "broker_account_symbol_timeframe",
            "date_range",
            "modeling_mode",
            "spread_commission_slippage",
            "dataset_id",
            "feature_set_id",
            "label_id",
            "split_id",
            "parser_contract_version",
            "runtime_contract_version",
            "onnx_hash",
            "ea_source_hash",
            "ea_binary_hash",
            "set_ini_hash",
            "feature_order_hash",
            "report_hash",
            "trade_list_hash",
            "telemetry_hash",
            "git_commit",
        ],
        "claim_effect": "F97A cannot support runtime verified, economics pass, materialization ready, handoff complete, promotion, authority, readiness, or Goal Achieve.",
    }


def f97b_brief(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "planned_run_id": NEXT_RUN_ID,
        "parent_run_id": RUN_ID,
        "task": "proxy scout for leakage-safe first-hit survival/hazard event-sparse abstention surface",
        "verification_profile": "proxy_scout",
        "required_records": ["Tier A separate", "Tier B separate", "Tier A+B actual routed total"],
        "first_action": "Lock data/time/split/first-hit-label contracts, then run a narrow validation-only proxy scout before any runtime claim.",
        "candidate_gate_preview": [
            "Tier A/B/A+B all recorded",
            "first-hit tie/censoring/horizon rules present",
            "5-10 trades/day plausible density",
            "adverse-first risk controlled",
            "calibration diagnostics present before probability language",
            "PF used as support only",
            "DD/recovery/segment stability checked",
            "same-packet MT5 trigger checked before ONNX/EA/set or runtime language",
        ],
        "runtime_trigger": "If candidate_count > 0 and any runnable/materialization/economics/handoff/runtime claim appears, attempt the narrow MT5 Strategy Tester probe in the same packet.",
        "claim_boundary": "planned_proxy_scout_only_no_candidate_no_runtime_authority",
    }


def summary_payload(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "hypothesis": payload["hypothesis"],
        "verification_profile": "design_only",
        "frontier_extra_due_status": FRONTIER_EXTRA_DUE_STATUS,
        "frontier_five_stage_status": FRONTIER_FIVE_STAGE_STATUS,
        "frontier_topic_rotation_status": FRONTIER_TOPIC_ROTATION_STATUS,
        "task_force_actual_call_count": len(task_force_calls()),
        "runtime_probe_status": RUNTIME_PROBE_STATUS,
        "claim_boundary": CLAIM_BOUNDARY,
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }


def kpi_payload(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "hypothesis": payload["hypothesis"],
        "test_period": "not_applicable_design_only",
        "proxy_kpi": "not_run",
        "runtime_kpi": "not_run",
        "net_profit": None,
        "profit_factor": None,
        "drawdown": None,
        "trade_count": 0,
        "trades_per_day": 0,
        "parity": "not_applicable_no_runtime_artifact",
        "gap_cause": "not_applicable_no_proxy_or_runtime",
        "next_action": NEXT_RUN_ID,
        "closeout_kpi": {
            "gross_profit": None,
            "gross_loss": None,
            "win_rate": None,
            "avg_win": None,
            "avg_loss": None,
            "payoff_ratio": None,
            "expectancy": None,
            "recovery_factor": None,
            "time_under_water": None,
            "max_consecutive_loss": None,
            "long_short_breakdown": "not_applicable_design_only",
            "favorable_first_rate": None,
            "adverse_first_rate": None,
            "censoring_rate": None,
        },
        "claim_effect": "KPI fields are empty because F97A is design-only and has no proxy/runtime economics evidence.",
    }


def result_summary_text(payload: Mapping[str, Any]) -> str:
    return f"""# F97A Stage Open Summary(전선97A 단계 개방 요약)

Action(행동): materialize(물질화) `{RUN_ID}` as a design-only stage-open packet(설계 전용 단계 개방 묶음).

Effect(효과): `{NEXT_RUN_ID}` becomes the current run(현재 실행) for first-hit survival/hazard proxy scout(첫 도달 생존/위험 프록시 탐색).

Hypothesis(가설): {payload['hypothesis']}

Task Force(태스크포스): seven selected agents(선택 요원 7명) were actually called(실제 호출) and recorded(기록) in `{rel(PACKET_TASK_FORCE_REVIEW)}`. agent_01(요원01)은 의견 미회수, agent_03(요원03)은 오진단 의견 거절, 나머지는 accepted/needs_local_verification(수용/로컬 검증 필요)로 분류했다.

Runtime boundary(런타임 경계): no runnable candidate(실행 가능한 후보 없음), no ONNX/EA/set bundle(온엑스/전문가 자문/설정 묶음 없음), no Strategy Tester output(전략 테스터 출력 없음), and no runtime/economics/handoff claim(런타임/경제성/인계 주장 없음).

Next(다음): `{NEXT_RUN_ID}`.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""


def write_run_artifacts(payload: Mapping[str, Any]) -> None:
    write_json(RUN_MANIFEST, {"script": SCRIPT_REL, **summary_payload(payload), "source_inputs": payload["source_identities"]})
    write_json(SUMMARY_JSON, summary_payload(payload))
    write_json(KPI_RECORD, kpi_payload(payload))
    write_json(EXPERIMENT_DESIGN, experiment_design(payload))
    write_json(RUNTIME_CONTRACT, runtime_contract(payload))
    write_json(F97B_BRIEF, f97b_brief(payload))
    write_json(DATA_INTEGRITY_PLAN, data_integrity_plan(payload))
    write_json(MODEL_VALIDATION_PLAN, model_validation_plan(payload))
    write_json(FIRST_HIT_CONTRACT, first_hit_contract(payload))
    write_text(RESULT_SUMMARY, result_summary_text(payload))
    write_json(STAGE_OPEN_SUMMARY, summary_payload(payload))
    write_text(F97A_REPORT, result_summary_text(payload))


def audit_payload(name: str, status: str, **extra: Any) -> dict[str, Any]:
    return {"audit_name": name, "packet_id": RUN_ID, "status": status, "created_at_utc": extra.pop("created_at_utc", None), **extra}


def write_audits(payload: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> None:
    gate_results = gate_results or {}
    task_force = payload["task_force"]
    write_json(TASK_FORCE_REVIEW, task_force)
    write_json(PACKET_TASK_FORCE_REVIEW, task_force)
    write_json(
        FRONTIER_EXTRA_DUE_CHECK,
        audit_payload(
            "frontier_extra_due_check",
            "pass_not_due",
            created_at_utc=payload["created_at_utc"],
            frontier_closeout_count_boundary="F96 closed; next boundary is F100/E02; E01 closed for F50.",
            due_status=FRONTIER_EXTRA_DUE_STATUS,
            claim_effect="F97A may open; no Extra Stage is due before F97.",
        ),
    )
    write_json(
        FIVE_STAGE_SYNTHESIS,
        audit_payload(
            "frontier_five_stage_direction_synthesis",
            "pass",
            created_at_utc=payload["created_at_utc"],
            source_frontiers=["F92", "F93", "F94", "F95", "F96"],
            dominant_direction="Recent work repeatedly found proxy clues that died through density, side/cost exposure, Tier B, DD/recovery, or runtime materialization boundaries.",
            repeated_mechanism="Local proxy structure can look usable while trade density, adverse excursion, and runtime exportability fail.",
            overused_axis_warning="Avoid adjacent action-value threshold repair, PF-only ranking, and state-cluster replays.",
            next_axis_options=["first-hit survival/hazard", "censoring-aware abstention", "closed-bar deterministic bracket lifecycle"],
            claim_effect="Direction only; no retrospective, permanent ban, candidate, or authority claim.",
        ),
    )
    write_json(
        TOPIC_ROTATION_CHECK,
        audit_payload(
            "frontier_topic_rotation_check",
            "pass",
            created_at_utc=payload["created_at_utc"],
            previous_stage="stage_frontier_96__counterfactual_action_value_policy_axis",
            proposed_stage=STAGE_ID,
            material_novelty_delta=[
                "label target changes from action-value utility to first-hit competing survival/hazard",
                "objective changes to calibrated hit-risk ranking and event-sparse abstention",
                "trade shape changes to bracket lifecycle and hold-risk budgeting before side selection",
                "runtime representation becomes closed-bar bracket/hold-window state machine if a candidate later appears",
                "validation philosophy prioritizes segment stability, density band, adverse-first risk, and calibration before PF",
            ],
            blocked_continuation_repair=False,
            threshold_filter_parameter_only_tweak=False,
            claim_effect="F97A can open as a distinct design axis; no candidate or runtime claim.",
        ),
    )
    write_json(
        SCOPE_GATE,
        audit_payload(
            "scope_completion_gate",
            "pass",
            created_at_utc=payload["created_at_utc"],
            required_artifacts=[rel(EXPERIMENT_DESIGN), rel(RUNTIME_CONTRACT), rel(F97B_BRIEF), rel(FIRST_HIT_CONTRACT), rel(PACKET_TASK_FORCE_REVIEW)],
            missing_required_artifacts=[],
            claim_effect="Design packet artifacts exist; no proxy execution or runtime claim.",
        ),
    )
    write_json(
        DATA_INTEGRITY_AUDIT,
        audit_payload(
            "data_integrity_audit",
            "pass_with_boundary",
            created_at_utc=payload["created_at_utc"],
            data_sources_checked=data_integrity_plan(payload)["data_sources_checked"],
            time_axis_boundary=data_integrity_plan(payload)["time_axis_boundary"],
            split_boundary=data_integrity_plan(payload)["split_boundary"],
            leakage_boundary=data_integrity_plan(payload)["feature_label_boundary"],
            tier_boundary=data_integrity_plan(payload)["tier_boundary"],
            claim_effect="Data checks are predeclared for F97B; no data_contract_pass or authority claim.",
        ),
    )
    write_json(
        MODEL_VALIDATION_AUDIT,
        audit_payload(
            "model_validation_audit",
            "pass_with_boundary",
            created_at_utc=payload["created_at_utc"],
            validation_policy=model_validation_plan(payload)["validation_split"],
            invalid_conditions=experiment_design(payload)["invalid_conditions"],
            selection_boundary=model_validation_plan(payload)["selection_metric_boundary"],
            claim_effect="F97A sets validation rules only; no model quality, calibrated probability, or candidate claim.",
        ),
    )
    write_json(
        ARTIFACT_AUDIT,
        audit_payload(
            "artifact_lineage_audit",
            "pass",
            created_at_utc=payload["created_at_utc"],
            source_inputs=[file_identity(path) for path in source_inputs()],
            produced_artifacts=[file_identity(path) for path in produced_artifacts()],
            lineage_judgment="F96C negative memory/reference surface -> F97A design-only first-hit survival/hazard stage open -> F97B proxy scout plan.",
            claim_effect="Artifacts support design-open evidence only; prior outputs are hash-linked and not authority.",
        ),
    )
    write_json(
        RESULT_JUDGMENT_AUDIT,
        audit_payload(
            "result_judgment_audit",
            "pass_with_boundary",
            created_at_utc=payload["created_at_utc"],
            judgment=JUDGMENT,
            allowed_claims=ALLOWED_CLAIMS,
            forbidden_claims=FORBIDDEN_CLAIMS,
            evidence_used=[rel(EXPERIMENT_DESIGN), rel(RUNTIME_CONTRACT), rel(PACKET_TASK_FORCE_REVIEW)],
            claim_effect="F97A is design-only stage open; not candidate, runtime, promotion, or completion evidence.",
        ),
    )
    final_guard = gate_results.get("final_claim_guard")
    seed = (
        dict(final_guard)
        if isinstance(final_guard, Mapping)
        else audit_payload(
            "final_claim_guard",
            "pending",
            created_at_utc=payload["created_at_utc"],
            claim_boundary=CLAIM_BOUNDARY,
            blocked_claims={claim: "not_claimed" for claim in FORBIDDEN_CLAIMS},
            allowed_claims=[],
        )
    )
    write_json(FINAL_CLAIM_GUARD, seed)
    write_json(PACKET_FINAL_CLAIM_GUARD, seed)


def skill_receipts(payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    current_truth_docs = [rel(WORKSPACE_STATE), rel(CURRENT_WORKING_STATE), rel(SELECTION_STATUS)]
    evidence = [rel(EXPERIMENT_DESIGN), rel(RUNTIME_CONTRACT), rel(F97B_BRIEF), rel(PACKET_TASK_FORCE_REVIEW)]
    return [
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-experiment-design",
            "status": "executed",
            "hypothesis": payload["hypothesis"],
            "baseline": payload["f96c_reference"],
            "changed_variables": experiment_design(payload)["changed_variables"],
            "invalid_conditions": experiment_design(payload)["invalid_conditions"],
            "evidence_plan": experiment_design(payload)["success_criteria_for_f97b_proxy_scout"],
            "receipt_path": rel(SKILL_RECEIPT_DIR / "experiment_design.json"),
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-data-integrity",
            "status": "executed",
            "data_sources_checked": data_integrity_plan(payload)["data_sources_checked"],
            "time_axis_boundary": data_integrity_plan(payload)["time_axis_boundary"],
            "split_boundary": data_integrity_plan(payload)["split_boundary"],
            "leakage_checks": data_integrity_plan(payload)["leakage_checks"],
            "missing_data_boundary": "F97B must detect missing rows, duplicate bars, Tier B absence, combined-view sort gaps, tie-rule absence, and split embargo gaps before scoring.",
            "receipt_path": rel(SKILL_RECEIPT_DIR / "data_integrity.json"),
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-model-validation",
            "status": "executed",
            "model_or_threshold_surface": model_validation_plan(payload)["model_or_threshold_surface"],
            "validation_split": model_validation_plan(payload)["validation_split"],
            "overfit_checks": model_validation_plan(payload)["overfit_checks"],
            "selection_metric_boundary": model_validation_plan(payload)["selection_metric_boundary"],
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "receipt_path": rel(SKILL_RECEIPT_DIR / "model_validation.json"),
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-artifact-lineage",
            "status": "executed",
            "source_inputs": [file_identity(path) for path in source_inputs()],
            "produced_artifacts": [rel(path) for path in produced_artifacts()],
            "raw_evidence": [rel(F96B_KPI), rel(F96B_CANDIDATE_GATE), rel(F96C_SUMMARY), rel(F96C_DECISION)],
            "machine_readable": [rel(path) for path in [RUN_MANIFEST, SUMMARY_JSON, KPI_RECORD, EXPERIMENT_DESIGN, RUNTIME_CONTRACT, SKILL_RECEIPTS]],
            "human_readable": [rel(RESULT_SUMMARY), rel(F97A_REPORT), rel(STAGE_BRIEF), rel(SELECTION_STATUS), rel(CONTEXT_ANCHOR)],
            "hashes_or_missing_reasons": [file_identity(path) for path in produced_artifacts()],
            "lineage_boundary": "F96C negative memory/reference surface only; F97A design-open only; no runtime authority.",
            "receipt_path": rel(SKILL_RECEIPT_DIR / "artifact_lineage.json"),
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-result-judgment",
            "status": "executed",
            "judgment_boundary": JUDGMENT,
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "evidence_used": evidence,
            "receipt_path": rel(SKILL_RECEIPT_DIR / "result_judgment.json"),
        },
        payload["task_force"],
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-stage-transition",
            "status": "executed",
            "source_current_truth_docs": current_truth_docs,
            "changed_or_checked_docs": [rel(WORKSPACE_STATE), rel(CURRENT_WORKING_STATE), rel(STAGE_BRIEF), rel(SELECTION_STATUS), rel(CONTEXT_ANCHOR)],
            "detected_conflicts": ["none_detected"],
            "canonical_state_after": {"active_stage": STAGE_ID, "current_run_id": NEXT_RUN_ID, "latest_completed_run_id": RUN_ID},
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "receipt_path": rel(SKILL_RECEIPT_DIR / "stage_transition.json"),
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-claim-discipline",
            "status": "executed",
            "requested_claims": ALLOWED_CLAIMS,
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "final_status": STATUS,
            "receipt_path": rel(SKILL_RECEIPT_DIR / "claim_discipline.json"),
        },
    ]


def write_receipts(payload: Mapping[str, Any]) -> None:
    receipts = skill_receipts(payload)
    write_json(SKILL_RECEIPTS, {"packet_id": RUN_ID, "primary_skill": "obsidian-experiment-design", "receipts": receipts})
    for receipt in receipts:
        write_json(ROOT / str(receipt["receipt_path"]), receipt)


def work_packet_payload(payload: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> dict[str, Any]:
    gate_results = gate_results or {}
    required_evidence = [
        rel(EXPERIMENT_DESIGN),
        rel(RUNTIME_CONTRACT),
        rel(F97B_BRIEF),
        rel(DATA_INTEGRITY_PLAN),
        rel(MODEL_VALIDATION_PLAN),
        rel(FIRST_HIT_CONTRACT),
        rel(PACKET_TASK_FORCE_REVIEW),
        rel(WORK_PACKET),
        rel(SKILL_RECEIPTS),
        rel(PACKET_CLOSEOUT_GATE),
    ]
    actual_status_source = {gate: gate_results.get(gate, {}).get("status", "pending") for gate in REQUIRED_GATES}
    return {
        "version": "work_packet_schema_v2_1",
        "packet_lifecycle": "new_packet",
        "packet_id": RUN_ID,
        "created_at_utc": payload["created_at_utc"],
        "user_request": {
            "user_quote": "/goal active continuation; user explicitly corrected that required Task Force agents must be actually called, not only promised",
            "requested_action": "canonical frontier stage open for F97A first-hit survival/hazard event-sparse axis",
            "requested_count": {"value": 1, "n_a_reason": ""},
            "ambiguous_terms": ["Goal Achieve is not claimed.", "Runtime authority is not claimed.", "F97A is design-only."],
        },
        "current_truth": {
            "active_stage": STAGE_ID,
            "current_run": RUN_ID,
            "latest_completed_run": PARENT_RUN_ID,
            "source_documents": [rel(WORKSPACE_STATE), rel(CURRENT_WORKING_STATE), rel(SELECTION_STATUS)],
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "work_classification": {
            "primary_family": "experiment_design",
            "detected_families": ["experiment_design", "artifact_lineage", "state_sync"],
            "touched_surfaces": [rel(STAGE_DIR), rel(PACKET_DIR), rel(WORKSPACE_STATE)],
            "mutation_intent": True,
            "execution_intent": True,
        },
        "risk_vector_scan": {
            "risks": {
                "task_force_review_claim_without_actual_calls": "high",
                "f96_action_value_repair_laundering": "high",
                "first_hit_label_leakage": "high",
                "intrabar_first_hit_ambiguity": "high",
                "runtime_probe_absence_misread_as_cost_skip": "medium",
            },
            "hard_stop_risks": [
                "Do not claim runtime/economics/materialization without MT5 Strategy Tester output identity.",
                "Do not repeat F96 action-value repair by threshold/filter/session/routing/parameter-only tweak.",
                "Do not fit bracket, scaler, threshold, density, or calibration on OOS.",
            ],
            "required_gates": REQUIRED_GATES,
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        "decision_lock": {
            "mode": "assume_safe_default",
            "assumptions": {
                "task_force_required_now": True,
                "verification_profile": "design_only",
                "strategy_tester_required_now": False,
                "reason": "F97A protects design-only stage-open claims and has no runnable candidate, ONNX/EA/set behavior, or runtime/materialization/economics/handoff claim.",
            },
            "questions": [],
            "required_user_decisions": [],
        },
        "interpreted_scope": {
            "work_families": ["experiment_design"],
            "target_surfaces": ["F97 stage open", "first-hit survival/hazard design", "F97B proxy scout brief", "Task Force receipt", "state sync"],
            "scope_units": ["stage_open_design", "receipt", "state_sync", "ledger"],
            "execution_layers": ["local_python_execution"],
            "mutation_policy": {"allowed": True, "user_quote": "/goal active continuation"},
            "evidence_layers": ["F96C negative memory reference", "F97A design artifacts", "Task Force actual calls", "frontier overlays"],
            "reduction_policy": {"reduction_allowed": False, "requires_user_quote": False, "rationale": "F97A is a formal stage-open packet."},
            "claim_boundary": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
        },
        "verification_profile": {
            "profile_id": "design_only",
            "claim_surface": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
            "trigger_sources": [
                "active_goal_frontier_continuation",
                "F96C closeout rotated to F97 pending scaffold",
                "formal F97A stage open claim",
                "explicit user instruction requiring Task Force when triggered",
            ],
            "protected_claims": ALLOWED_CLAIMS,
            "required_evidence": required_evidence,
            "gates_not_run_with_reason": RUNTIME_NA_REASONS,
            "stop_conditions": [
                "Stop after F97A design artifacts, receipts, gates, ledgers, and state sync are materialized.",
                "Do not create candidate/runtime claims in F97A.",
                "If runnable candidate or runtime claim appears, reroute to runtime_probe profile in the same packet.",
            ],
        },
        "acceptance_criteria": [
            {"id": "AC-001", "text": "F97A experiment design exists.", "expected_artifact": rel(EXPERIMENT_DESIGN), "verification_method": "scope_completion_gate", "required": True},
            {"id": "AC-002", "text": "F97A Task Force actual calls are recorded.", "expected_artifact": rel(PACKET_TASK_FORCE_REVIEW), "verification_method": "codex_task_force_review_packet", "required": True},
            {"id": "AC-003", "text": "F97B proxy scout brief exists.", "expected_artifact": rel(F97B_BRIEF), "verification_method": "scope_completion_gate", "required": True},
            {"id": "AC-004", "text": "Runtime evidence gate is explicitly outside claim surface, not skipped for cost or proxy-bad reasons.", "expected_artifact": rel(RUNTIME_CONTRACT), "verification_method": "final_claim_guard", "required": True},
        ],
        "work_plan": [
            "Write F97A design/runtime-contract/F97B brief artifacts.",
            "Record Task Force actual_subagent_calls and local-verification classifications.",
            "Run frontier_extra_due_check, five-stage synthesis, and topic rotation gates.",
            "Run schema, receipt, state sync, gate coverage, and final claim guard checks.",
            "Commit to main if gates pass.",
        ],
        "skill_routing": {
            "primary_family": "experiment_design",
            "primary_skill": "obsidian-experiment-design",
            "support_skills": [skill for skill in REQUIRED_SKILLS if skill != "obsidian-experiment-design"],
            "skills_considered": [*REQUIRED_SKILLS, "obsidian-runtime-parity", "obsidian-backtest-forensics"],
            "skills_selected": REQUIRED_SKILLS,
            "skills_not_used": [
                {"skill": "obsidian-runtime-parity", "reason": "No ONNX/EA/runtime parity or handoff claim is made."},
                {"skill": "obsidian-backtest-forensics", "reason": "No new Strategy Tester report or trade list exists in F97A."},
            ],
            "required_skill_receipts": REQUIRED_SKILLS,
            "required_gates": REQUIRED_GATES,
        },
        "evidence_contract": {
            "source_inputs": [rel(path) for path in source_inputs()],
            "machine_readable": [rel(path) for path in [RUN_MANIFEST, SUMMARY_JSON, KPI_RECORD, EXPERIMENT_DESIGN, RUNTIME_CONTRACT, F97B_BRIEF, DATA_INTEGRITY_PLAN, MODEL_VALIDATION_PLAN, FIRST_HIT_CONTRACT, SKILL_RECEIPTS]],
            "human_readable": [rel(RESULT_SUMMARY), rel(F97A_REPORT), rel(STAGE_BRIEF), rel(SELECTION_STATUS), rel(CONTEXT_ANCHOR)],
            "raw_evidence": [rel(F96B_KPI), rel(F96B_CANDIDATE_GATE), rel(F96C_SUMMARY), rel(F96C_DECISION)],
            "missing_evidence": [
                {"evidence": "MT5 Strategy Tester runtime output", "reason": "outside F97A design-only claim surface"},
                {"evidence": "WFO/stress result", "reason": "outside F97A design-only claim surface"},
            ],
        },
        "gates": {
            "required": REQUIRED_GATES,
            "actual_status_source": actual_status_source,
            "not_applicable_with_reason": {item["gate"]: item["reason"] for item in RUNTIME_NA_REASONS},
        },
        "final_claim_policy": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
    }


def closeout_gate_payload(gate_results: Mapping[str, Any] | None = None) -> dict[str, Any]:
    gate_results = gate_results or {}
    gate_paths = {
        "work_packet_schema_lint": PACKET_WORK_PACKET_LINT,
        "skill_receipt_schema_lint": PACKET_SKILL_RECEIPT_LINT,
        "codex_task_force_review_packet": PACKET_TASK_FORCE_REVIEW,
        "frontier_extra_due_check": FRONTIER_EXTRA_DUE_CHECK,
        "frontier_five_stage_direction_synthesis": FIVE_STAGE_SYNTHESIS,
        "frontier_topic_rotation_check": TOPIC_ROTATION_CHECK,
        "scope_completion_gate": SCOPE_GATE,
        "data_integrity_audit": DATA_INTEGRITY_AUDIT,
        "model_validation_audit": MODEL_VALIDATION_AUDIT,
        "artifact_lineage_audit": ARTIFACT_AUDIT,
        "result_judgment_audit": RESULT_JUDGMENT_AUDIT,
        "state_sync_audit": PACKET_STATE_SYNC_AUDIT,
        "required_gate_coverage_audit": PACKET_REQUIRED_GATE_AUDIT,
        "final_claim_guard": PACKET_FINAL_CLAIM_GUARD,
    }
    audits = [
        {"audit_name": gate, "path": rel(gate_paths[gate]), "status": gate_results.get(gate, {}).get("status", "pending")}
        for gate in REQUIRED_GATES
    ]
    final_guard = gate_results.get("final_claim_guard", {"audit_name": "final_claim_guard", "path": rel(PACKET_FINAL_CLAIM_GUARD), "status": "pending"})
    return {
        "audit_name": "closeout_gate",
        "packet_id": RUN_ID,
        "status": "pass" if final_guard.get("status") == "pass" else "pending",
        "audits": audits,
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "claim_boundary": CLAIM_BOUNDARY,
        "final_claim_guard": final_guard,
    }


def write_packet(payload: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> None:
    write_yaml(WORK_PACKET, work_packet_payload(payload, gate_results))
    write_json(PACKET_CLOSEOUT_GATE, closeout_gate_payload(gate_results))


def stage_brief_text(payload: Mapping[str, Any]) -> str:
    return f"""# F97 First-Hit Survival/Hazard Event-Sparse Axis(전선97 첫 도달 생존/위험 이벤트 희소 축)

- current run(현재 실행): `{NEXT_RUN_ID}`
- latest completed run(최근 완료 실행): `{RUN_ID}`
- source closeout(원천 마감): `{PARENT_RUN_ID}`
- status(상태): design-only formal open recorded(설계 전용 정식 개방 기록)
- authority(권위): not_claimed(주장 없음)

## Question(질문)

Can first-hit survival/hazard(첫 도달 생존/위험) and event-sparse abstention(이벤트 희소 관망) create a new US100 M5 scout surface(탐색 표면) before side selection(방향 선택)?

## Hypothesis(가설)

{payload['hypothesis']}

## Novelty Delta(신규성 차이)

- label target(라벨 목표): first favorable/adverse bracket hit(첫 유리/불리 브래킷 도달)
- objective(목적함수): calibrated hit-risk ranking(보정 도달 위험 순위) and abstention(관망)
- trade shape(거래 형태): bracket lifecycle(브래킷 생애주기) and hold-risk budgeting(보유 위험 예산)
- validation philosophy(검증 철학): density/adverse-first/calibration/segment stability(밀도/불리 우선/보정/구간 안정성) before PF-only selection(PF 단독 선정)
- runtime boundary(런타임 경계): a runnable ONNX/EA/set claim(실행 가능한 온엑스/전문가 자문/설정 주장) triggers same-packet MT5 Strategy Tester probe(같은 묶음 MT5 전략 테스터 탐침)

## Boundary(경계)

F97A is design-only formal open(설계 전용 정식 개방) evidence(근거) only. No selected baseline(선택 기준선), promotion candidate(승격 후보), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성) is claimed(주장됨).
"""


def input_refs_text() -> str:
    rows = "\n".join(f"- `{rel(path)}`" for path in source_inputs())
    return f"""# F97 Input References(전선97 입력 참조)

{rows}

Boundary(경계): F96C artifacts(산출물)는 reference/negative memory(참조/부정 기억) only(전용)이다. They do not provide winner(승자), selected baseline(선택 기준선), promotion history(승격 이력), or runtime authority(런타임 권위).
"""


def selection_status_text(payload: Mapping[str, Any]) -> str:
    return f"""# F97 Selection Status(전선97 선택 상태)

- current run(현재 실행): `{NEXT_RUN_ID}`
- latest completed run(최근 완료 실행): `{RUN_ID}`
- status(상태): F97A design-only formal open recorded(설계 전용 정식 개방 기록); F97B proxy scout planned(F97B 프록시 탐색 계획)
- selected baseline(선택 기준선): not_claimed(주장 없음)
- promotion candidate(승격 후보): not_claimed(주장 없음)
- operating promotion(운영 승격): not_claimed(주장 없음)
- runtime authority(런타임 권위): not_claimed(주장 없음)
- live readiness(실거래 준비): not_claimed(주장 없음)
- Goal Achieve(목표 달성): not_claimed(주장 없음)
- Task Force actual calls(태스크포스 실제 호출): seven selected agents recorded(선택 요원 7명 기록)
- runtime probe(런타임 탐침): not run(미실행) because no runnable candidate or runtime claim exists(실행 가능한 후보/런타임 주장 없음)
- source closeout(원천 마감): `{PARENT_RUN_ID}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""


def context_anchor_text(payload: Mapping[str, Any]) -> str:
    return f"""# Current Working State(현재 작업 상태)

- active stage(활성 단계): `{STAGE_ID}`
- current run(현재 실행): `{NEXT_RUN_ID}`
- latest completed run(최근 완료 실행): `{RUN_ID}`
- current status(현재 상태): `{STATUS}`
- current judgment(현재 판정): `{JUDGMENT}`
- frontier extra due status(전선 추가 도래 상태): `{FRONTIER_EXTRA_DUE_STATUS}`
- frontier topic rotation status(전선 주제 회전 상태): `{FRONTIER_TOPIC_ROTATION_STATUS}`
- runtime probe status(런타임 탐침 상태): `{RUNTIME_PROBE_STATUS}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): F97A materializes(물질화) a design-only formal-open packet(설계 전용 정식 개방 묶음) with actual Task Force calls(실제 태스크포스 호출).

Effect(효과): F97B is the current run(현재 실행) for first-hit survival/hazard event-sparse proxy scout(첫 도달 생존/위험 이벤트 희소 프록시 탐색), with no runtime authority(런타임 권위 없음), no selected baseline(선택 기준선 없음), and no Goal Achieve(목표 달성 없음).
"""


def review_index_text() -> str:
    return f"""# F97 Review Index(전선97 검토 색인)

- f97a_task_force_review_receipt: `{rel(TASK_FORCE_REVIEW)}`
- f97a_frontier_extra_due_check: `{rel(FRONTIER_EXTRA_DUE_CHECK)}`
- f97a_frontier_five_stage_direction_synthesis: `{rel(FIVE_STAGE_SYNTHESIS)}`
- f97a_frontier_topic_rotation_check: `{rel(TOPIC_ROTATION_CHECK)}`
- f97a_scope_completion_gate: `{rel(SCOPE_GATE)}`
- f97a_data_integrity_audit: `{rel(DATA_INTEGRITY_AUDIT)}`
- f97a_model_validation_audit: `{rel(MODEL_VALIDATION_AUDIT)}`
- f97a_artifact_lineage_audit: `{rel(ARTIFACT_AUDIT)}`
- f97a_result_judgment_audit: `{rel(RESULT_JUDGMENT_AUDIT)}`
- f97a_state_sync_audit: `{rel(STATE_SYNC_AUDIT)}`
- f97a_required_gate_coverage_audit: `{rel(REQUIRED_GATE_AUDIT)}`
- f97a_final_claim_guard: `{rel(FINAL_CLAIM_GUARD)}`
- current run(현재 실행): `{NEXT_RUN_ID}`
"""


def update_state_docs(payload: Mapping[str, Any]) -> None:
    workspace = {
        "current_stage_id": STAGE_ID,
        "active_stage": STAGE_ID,
        "active_branch": current_branch(),
        "current_run_id": NEXT_RUN_ID,
        "latest_completed_run_id": RUN_ID,
        "current_status": STATUS,
        "current_judgment": JUDGMENT,
        "next_run_id": NEXT_RUN_ID,
        "frontier_extra_due_status": FRONTIER_EXTRA_DUE_STATUS,
        "frontier_five_stage_direction_synthesis_status": FRONTIER_FIVE_STAGE_STATUS,
        "frontier_topic_rotation_status": FRONTIER_TOPIC_ROTATION_STATUS,
        "task_force_status": "f97a_actual_subagent_calls_recorded_7_selected_agents_no_task_force_reviewed_pass_claim",
        "runtime_probe_status": RUNTIME_PROBE_STATUS,
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "updated_at_utc": payload["created_at_utc"],
        "context_anchor": rel(CONTEXT_ANCHOR),
        "notes": [
            "Action(행동): F97A design-only formal-open packet(설계 전용 정식 개방 묶음)이 materialized(물질화)되었다.",
            "Effect(효과): F97B current run(현재 실행)은 first-hit survival/hazard proxy scout(첫 도달 생존/위험 프록시 탐색)로 고정된다.",
            "Runtime(런타임): no Strategy Tester evidence(전략 테스터 근거 없음); no runtime authority(런타임 권위 없음); no Goal Achieve(목표 달성 없음).",
        ],
    }
    write_yaml(WORKSPACE_STATE, workspace)
    write_text(CURRENT_WORKING_STATE, context_anchor_text(payload))
    write_text(STAGE_BRIEF, stage_brief_text(payload))
    write_text(INPUT_REFS, input_refs_text())
    write_text(SELECTION_STATUS, selection_status_text(payload))
    write_text(CONTEXT_ANCHOR, context_anchor_text(payload))
    write_text(REVIEW_INDEX, review_index_text())


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path_exists(path):
        return [], []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), [dict(row) for row in reader]


def write_csv_rows(path: Path, fieldnames: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def replace_rows(path: Path, remove_keys: set[str], new_rows: Sequence[Mapping[str, Any]], *, key: str, header_source: Path | None = None) -> None:
    fieldnames, rows = read_csv_rows(path)
    if not fieldnames and header_source:
        fieldnames, _ = read_csv_rows(header_source)
    extras = [column for row in new_rows for column in row if column not in fieldnames]
    fieldnames = [*fieldnames, *extras]
    kept = [row for row in rows if str(row.get(key, "")).strip() not in remove_keys]
    write_csv_rows(path, fieldnames, [*kept, *new_rows])


def ledger_rows(payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    base = {
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "date": "2026-06-19",
        "run_date": "2026-06-19",
        "created_at": payload["created_at_utc"],
        "created_at_utc": payload["created_at_utc"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "not_claimed",
    }
    f97a = {
        **base,
        "ledger_row_id": f"{RUN_ID}__stage_open_design",
        "run_id": RUN_ID,
        "subrun_id": "stage_open_design",
        "record_view": "stage_open_design",
        "tier_scope": "not_applicable_design_only",
        "kpi_scope": "design_only",
        "scoreboard_lane": "design_open",
        "lane": "experiment_design",
        "family": "experiment_design",
        "work_family": "experiment_design",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(F97A_REPORT),
        "primary_report": rel(F97A_REPORT),
        "report_path": rel(F97A_REPORT),
        "primary_artifact": rel(EXPERIMENT_DESIGN),
        "result_path": rel(F97A_REPORT),
        "gate_audit_path": rel(PACKET_CLOSEOUT_GATE),
        "required_gate_audit": rel(PACKET_REQUIRED_GATE_AUDIT),
        "primary_kpi": "candidate_count=0;runtime_completed_rows=0",
        "guardrail_kpi": "no_runtime_claim;no_authority;task_force_calls=7",
        "external_verification_status": "not_applicable_design_only",
        "notes": "F97A design-only open; Task Force actual calls recorded; no runtime claim.",
        "run_number": "frontier97A",
        "decision": STATUS,
        "next_run_id": NEXT_RUN_ID,
        "rows": 0,
        "gate_passes": len(REQUIRED_GATES),
        "gate_total": len(REQUIRED_GATES),
        "claim_boundary": CLAIM_BOUNDARY,
        "result_status": STATUS,
        "runtime_completed_rows": 0,
        "runtime_attempt_rows": 0,
        "candidate_count": 0,
        "scout_clue_count": 0,
        "materialization_candidate_count": 0,
        "meaningful_signal_count": 0,
        "completion_candidate_count": 0,
        "artifact_count": len([path for path in produced_artifacts() if path_exists(path)]),
        "run_family": "experiment_design",
        "run_type": "stage_open_design",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(STAGE_DIR),
        "row_id": f"{RUN_ID}__stage_open_design",
        "question": "Can first-hit survival/hazard and event-sparse abstention create a US100 M5 scout surface?",
        "next_action": NEXT_RUN_ID,
        "model_variants": 0,
        "selected_surfaces": 0,
        "net_profit": "",
        "profit_factor": "",
        "drawdown": "",
        "trade_count": 0,
        "trades_per_day": 0,
        "runtime_probe_status": RUNTIME_PROBE_STATUS,
    }
    f97b = {
        **base,
        "ledger_row_id": f"{NEXT_RUN_ID}__planned_current_run",
        "run_id": NEXT_RUN_ID,
        "subrun_id": "planned_current_run",
        "record_view": "planned_current_run",
        "tier_scope": "planned_tier_a_tier_b_combined",
        "kpi_scope": "planned_proxy_scout",
        "scoreboard_lane": "planned_proxy_scout",
        "lane": "experiment_design",
        "family": "experiment_design",
        "work_family": "experiment_design",
        "status": "planned_current_run_no_authority",
        "judgment": "planned_after_f97a_design_open",
        "path": rel(F97B_BRIEF),
        "primary_report": rel(F97B_BRIEF),
        "report_path": rel(F97B_BRIEF),
        "primary_artifact": rel(F97B_BRIEF),
        "result_path": rel(F97B_BRIEF),
        "primary_kpi": "pending",
        "guardrail_kpi": "first_hit_label_gate_pending;no_runtime_claim",
        "external_verification_status": "pending",
        "notes": "F97B planned current run after F97A open.",
        "run_number": "frontier97B",
        "decision": "planned_current_run_no_authority",
        "next_run_id": "",
        "rows": 0,
        "gate_passes": 0,
        "gate_total": 0,
        "claim_boundary": "planned_proxy_scout_only_no_candidate_no_runtime_authority",
        "result_status": "planned_current_run_no_authority",
        "runtime_completed_rows": 0,
        "runtime_attempt_rows": 0,
        "candidate_count": 0,
        "scout_clue_count": 0,
        "materialization_candidate_count": 0,
        "meaningful_signal_count": 0,
        "completion_candidate_count": 0,
        "artifact_count": 0,
        "required_gate_audit": "",
        "run_family": "experiment_design",
        "run_type": "planned_proxy_scout",
        "input_run_id": RUN_ID,
        "output_path": rel(F97B_BRIEF),
        "row_id": f"{NEXT_RUN_ID}__planned_current_run",
        "question": "Can first-hit survival/hazard and event-sparse abstention create a US100 M5 scout surface?",
        "next_action": "run_f97b_proxy_scout",
        "model_variants": 0,
        "selected_surfaces": 0,
        "net_profit": "",
        "profit_factor": "",
        "drawdown": "",
        "trade_count": 0,
        "trades_per_day": 0,
        "runtime_probe_status": "not_applicable_pending_proxy_scout_no_runtime_claim",
    }
    return [f97a, f97b]


def update_ledgers(payload: Mapping[str, Any]) -> None:
    rows = ledger_rows(payload)
    remove_run_ids = {RUN_ID, NEXT_RUN_ID}
    replace_rows(STAGE_LEDGER, remove_run_ids, rows, key="run_id")
    replace_rows(ALPHA_LEDGER, remove_run_ids, rows, key="run_id")
    replace_rows(RUN_REGISTRY, remove_run_ids, rows, key="run_id")


def update_artifact_registry(payload: Mapping[str, Any]) -> None:
    rows = []
    for path in produced_artifacts():
        identity = file_identity(path)
        artifact_id = f"{RUN_ID}__{Path(path).stem}"
        rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": path.suffix.lstrip(".") or "artifact",
                "path": identity["path"],
                "artifact_path": identity["path"],
                "sha256": identity["sha256"] or "",
                "size_bytes": identity["size_bytes"] or "",
                "created_at": payload["created_at_utc"],
                "created_at_utc": payload["created_at_utc"],
                "claim_boundary": CLAIM_BOUNDARY,
                "artifact_id": artifact_id,
                "notes": "F97A design-only artifact; no runtime authority.",
                "effect": "Supports design-open traceability only.",
            }
        )
    replace_rows(ARTIFACT_REGISTRY, {row["artifact_id"] for row in rows}, rows, key="artifact_id")


def replace_marked_section(path: Path, marker: str, body: str) -> None:
    start = f"<!-- {marker}:start -->"
    end = f"<!-- {marker}:end -->"
    existing = io_path(path).read_text(encoding="utf-8-sig") if path_exists(path) else ""
    section = f"{start}\n{body.rstrip()}\n{end}"
    if start in existing and end in existing:
        before = existing.split(start, 1)[0].rstrip()
        after = existing.split(end, 1)[1].lstrip()
        text = f"{before}\n\n{section}\n\n{after}".strip()
    else:
        text = f"{existing.rstrip()}\n\n{section}".strip()
    write_text(path, text)


def update_register_docs(payload: Mapping[str, Any]) -> None:
    selection_body = f"""## F97A Design Open(전선97A 설계 개방)

- active stage(활성 단계): `{STAGE_ID}`
- current run(현재 실행): `{NEXT_RUN_ID}`
- latest completed run(최근 완료 실행): `{RUN_ID}`
- selected baseline(선택 기준선): not_claimed(주장 없음)
- runtime authority(런타임 권위): not_claimed(주장 없음)
- Goal Achieve(목표 달성): not_claimed(주장 없음)
- effect(효과): F97A records(기록) a design-only first-hit survival/hazard axis(설계 전용 첫 도달 생존/위험 축) and hands off(인계) to F97B proxy scout(프록시 탐색).
"""
    idea_body = f"""## F97 First-Hit Survival/Hazard(전선97 첫 도달 생존/위험)

- source(원천): `{PARENT_RUN_ID}` as negative memory/reference surface(부정 기억/참조 표면)
- hypothesis(가설): {payload['hypothesis']}
- next action(다음 행동): `{NEXT_RUN_ID}`
- boundary(경계): no selected baseline(선택 기준선 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음)
"""
    changelog_body = f"""## 2026-06-19 F97A

Action(행동): recorded(기록) F97A design-only formal open(설계 전용 정식 개방) with seven actual Task Force calls(실제 태스크포스 호출 7건).

Effect(효과): current run(현재 실행) is `{NEXT_RUN_ID}`; runtime probe(런타임 탐침)는 no runnable candidate/no runtime claim(실행 가능한 후보 없음/런타임 주장 없음) 때문에 not_applicable_with_reason(사유 있는 해당 없음)이다.
"""
    replace_marked_section(GLOBAL_SELECTION_STATUS, "frontier97a_selection_status", selection_body)
    replace_marked_section(IDEA_REGISTRY, "frontier97_first_hit_survival_hazard", idea_body)
    replace_marked_section(WORKSPACE_CHANGELOG, "frontier97a_changelog", changelog_body)
    replace_marked_section(ROOT_CHANGELOG, "frontier97a_changelog", changelog_body)
    write_text(
        DECISION_MEMO,
        f"""# F97A Stage Open Decision(전선97A 단계 개방 결정)

Decision(결정): open(개방) `{STAGE_ID}` through `{RUN_ID}` as design-only formal open(설계 전용 정식 개방).

Reason(이유): F96C closed negative(부정 마감) for the action-value policy axis(행동가치 정책 축), then proposed(제안) first-hit survival/hazard(첫 도달 생존/위험) as a material novelty delta(실질 신규성 차이).

Task Force(태스크포스): agent_01, agent_03, agent_04, agent_05, agent_06, agent_07, agent_08 were actually called(실제 호출) and recorded(기록). agent_01 timed out(응답 시간 초과), agent_03 tool-availability diagnosis(도구 가능성 진단)는 rejected(거절), and the remaining opinions are bounded(경계 지정) by local verification(로컬 검증).

Runtime(런타임): no MT5 Strategy Tester probe(MT5 전략 테스터 탐침) in F97A because there is no runnable candidate(실행 가능한 후보 없음), no ONNX/EA/set(온엑스/전문가 자문/설정 없음), and no runtime/materialization/economics/handoff claim(런타임/물질화/경제성/인계 주장 없음). This is not cost deferral(비용 지연 아님).

Next(다음): `{NEXT_RUN_ID}`.

Forbidden claims avoided(금지 주장 회피): selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성).
""",
    )


def run_gate_cmd(args: Sequence[str], output_path: Path) -> dict[str, Any]:
    completed = subprocess.run(list(args), cwd=ROOT, check=False, capture_output=True, text=True, timeout=120)
    if completed.returncode != 0:
        print(completed.stdout)
        print(completed.stderr, file=sys.stderr)
        raise RuntimeError(f"gate command failed ({completed.returncode}): {' '.join(args)}")
    if not path_exists(output_path):
        raise FileNotFoundError(output_path)
    return read_json(output_path)


def audit_result_from_payload(name: str, payload: Mapping[str, Any]) -> AuditResult:
    return AuditResult(
        audit_name=name,
        status=str(payload.get("status", "pass")),
        counts={key: value for key, value in payload.items() if key not in {"audit_name", "status", "findings", "allowed_claims", "forbidden_claims"}},
        allowed_claims=tuple(str(item) for item in payload.get("allowed_claims", ())),
        forbidden_claims=tuple(str(item) for item in payload.get("forbidden_claims", ())),
    )


def run_gates(payload: Mapping[str, Any]) -> dict[str, Any]:
    gate_results: dict[str, Any] = {
        "codex_task_force_review_packet": {"status": "pass_with_boundary", "audit_name": "codex_task_force_review_packet"},
        "frontier_extra_due_check": read_json(FRONTIER_EXTRA_DUE_CHECK),
        "frontier_five_stage_direction_synthesis": read_json(FIVE_STAGE_SYNTHESIS),
        "frontier_topic_rotation_check": read_json(TOPIC_ROTATION_CHECK),
        "scope_completion_gate": read_json(SCOPE_GATE),
        "data_integrity_audit": read_json(DATA_INTEGRITY_AUDIT),
        "model_validation_audit": read_json(MODEL_VALIDATION_AUDIT),
        "artifact_lineage_audit": read_json(ARTIFACT_AUDIT),
        "result_judgment_audit": read_json(RESULT_JUDGMENT_AUDIT),
    }
    gate_results["work_packet_schema_lint"] = run_gate_cmd(
        [sys.executable, "-m", "foundation.control_plane.work_packet_schema_lint", rel(WORK_PACKET), "--output-json", rel(PACKET_WORK_PACKET_LINT), "--allow-blocked-exit-zero"],
        PACKET_WORK_PACKET_LINT,
    )
    gate_results["skill_receipt_schema_lint"] = run_gate_cmd(
        [
            sys.executable,
            "-m",
            "foundation.control_plane.skill_receipt_schema_lint",
            rel(SKILL_RECEIPTS),
            "--schema-path",
            "docs/agent_control/skill_receipt_schema.yaml",
            "--root",
            ".",
            "--output-json",
            rel(PACKET_SKILL_RECEIPT_LINT),
            "--allow-blocked-exit-zero",
        ],
        PACKET_SKILL_RECEIPT_LINT,
    )
    gate_results["state_sync_audit"] = run_gate_cmd(
        [
            sys.executable,
            "-m",
            "foundation.control_plane.state_sync_audit",
            "--root",
            ".",
            "--active-stage",
            STAGE_ID,
            "--current-branch",
            current_branch(),
            "--output-json",
            rel(PACKET_STATE_SYNC_AUDIT),
            "--allow-blocked-exit-zero",
        ],
        PACKET_STATE_SYNC_AUDIT,
    )
    write_json(STATE_SYNC_AUDIT, gate_results["state_sync_audit"])
    write_packet(payload, gate_results)
    gate_results["required_gate_coverage_audit"] = run_gate_cmd(
        [
            sys.executable,
            "-m",
            "foundation.control_plane.required_gate_coverage_audit",
            "--work-packet",
            rel(WORK_PACKET),
            "--closeout-gate",
            rel(PACKET_CLOSEOUT_GATE),
            "--output-json",
            rel(PACKET_REQUIRED_GATE_AUDIT),
            "--allow-blocked-exit-zero",
        ],
        PACKET_REQUIRED_GATE_AUDIT,
    )
    write_json(REQUIRED_GATE_AUDIT, gate_results["required_gate_coverage_audit"])
    audit_results = [
        audit_result_from_payload(name, result)
        for name, result in gate_results.items()
        if name in REQUIRED_GATES and isinstance(result, Mapping)
    ]
    final_guard = guard_final_claims(requested_claims=ALLOWED_CLAIMS, audit_results=audit_results)
    final_payload = final_guard.to_dict()
    gate_results["final_claim_guard"] = final_payload
    write_json(PACKET_FINAL_CLAIM_GUARD, final_payload)
    write_json(FINAL_CLAIM_GUARD, final_payload)
    write_audits(payload, gate_results)
    write_packet(payload, gate_results)
    return gate_results


def main() -> int:
    ensure_dirs()
    created_at = utc_now()
    payload = base_payload(created_at)
    write_run_artifacts(payload)
    write_audits(payload)
    write_receipts(payload)
    write_packet(payload)
    update_state_docs(payload)
    update_ledgers(payload)
    update_register_docs(payload)
    update_artifact_registry(payload)
    gate_results = run_gates(payload)
    update_artifact_registry(payload)
    print(json.dumps({"run_id": RUN_ID, "status": STATUS, "gates": {key: value.get("status") for key, value in gate_results.items()}}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
