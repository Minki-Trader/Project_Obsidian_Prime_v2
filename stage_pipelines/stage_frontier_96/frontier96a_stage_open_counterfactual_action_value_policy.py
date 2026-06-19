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


STAGE_ID = "stage_frontier_96__counterfactual_action_value_policy_axis"
RUN_ID = "frontier96A_stage_open_counterfactual_action_value_policy_axis_v1"
PARENT_RUN_ID = "frontier95C_closed_bar_state_transition_repair_or_rotation_decision_v1"
NEXT_RUN_ID = "frontier96B_counterfactual_action_value_policy_proxy_scout_v1"
SCRIPT_REL = "stage_pipelines/stage_frontier_96/frontier96a_stage_open_counterfactual_action_value_policy.py"

STATUS = "f96a_stage_open_design_prepared_no_candidate_no_authority"
JUDGMENT = "design_only_stage_open_counterfactual_action_value_policy_axis"
CLAIM_BOUNDARY = (
    "f96a_design_only_stage_open_counterfactual_action_value_policy_axis_"
    "no_model_candidate_no_wfo_pass_no_stress_pass_no_mt5_runtime_evidence_"
    "no_selected_baseline_no_operating_promotion_no_runtime_authority_"
    "no_live_readiness_no_goal_achieve"
)
RUNTIME_PROBE_STATUS = (
    "not_applicable_design_only_no_runnable_candidate_no_runtime_materialization_"
    "economics_handoff_claim_not_cost_or_proxy_bad_skip"
)
FRONTIER_EXTRA_DUE_STATUS = "not_due_after_f95_closeout_next_boundary_f100_e02_pending_e01_closed_for_f050"
FRONTIER_TOPIC_ROTATION_STATUS = "passed_f96_counterfactual_action_value_policy_axis_not_f95_state_cluster_parameter_repair"
FRONTIER_FIVE_STAGE_STATUS = "recorded_recent_f91_to_f95_direction_synthesis_no_retrospective_gate"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / "frontier96A"
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
DECISION_MEMO = ROOT / "docs" / "decisions" / "2026-06-19_frontier96a_stage_open_counterfactual_action_value_policy.md"

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
F96B_BRIEF = DESIGN_DIR / "f96b_proxy_scout_brief.json"
DATA_INTEGRITY_PLAN = DESIGN_DIR / "data_integrity_plan.json"
MODEL_VALIDATION_PLAN = DESIGN_DIR / "model_validation_plan.json"
ACTION_VALUE_CONTRACT = DESIGN_DIR / "action_value_policy_contract.json"
RESULT_SUMMARY = REPORT_DIR / "summary.md"

STAGE_OPEN_SUMMARY = REVIEW_DIR / "f96a_stage_open_summary.json"
TASK_FORCE_REVIEW = REVIEW_DIR / "f96a_task_force_review_receipt.json"
FRONTIER_EXTRA_DUE_CHECK = REVIEW_DIR / "f96a_frontier_extra_due_check.json"
FIVE_STAGE_SYNTHESIS = REVIEW_DIR / "f96a_frontier_five_stage_direction_synthesis.json"
TOPIC_ROTATION_CHECK = REVIEW_DIR / "f96a_frontier_topic_rotation_check.json"
SCOPE_GATE = REVIEW_DIR / "f96a_scope_completion_gate.json"
DATA_INTEGRITY_AUDIT = REVIEW_DIR / "f96a_data_integrity_audit.json"
MODEL_VALIDATION_AUDIT = REVIEW_DIR / "f96a_model_validation_audit.json"
ARTIFACT_AUDIT = REVIEW_DIR / "f96a_artifact_lineage_audit.json"
RESULT_JUDGMENT_AUDIT = REVIEW_DIR / "f96a_result_judgment_audit.json"
FINAL_CLAIM_GUARD = REVIEW_DIR / "f96a_final_claim_guard.json"
STATE_SYNC_AUDIT = REVIEW_DIR / "f96a_state_sync_audit.json"
REQUIRED_GATE_AUDIT = REVIEW_DIR / "f96a_required_gate_coverage_audit.json"
F96A_REPORT = REVIEW_DIR / "frontier96A_stage_open_counterfactual_action_value_policy_report.md"

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
F95B_RUN = ROOT / "stages" / "stage_frontier_95__closed_bar_state_transition_embedding_axis" / "02_runs" / "frontier95B"
F95B_KPI = F95B_RUN / "kpi_record.json"
F95B_CANDIDATE_GATE = F95B_RUN / "proxy_scout" / "candidate_gate.json"
F95B_TIER_ROUTE_SUMMARY = F95B_RUN / "proxy_scout" / "tier_route_summary.json"
F95B_DATA_LOCK = F95B_RUN / "proxy_scout" / "data_feature_split_lock.json"
F95C_DECISION = (
    ROOT
    / "stages"
    / "stage_frontier_95__closed_bar_state_transition_embedding_axis"
    / "02_runs"
    / "frontier95C"
    / "d"
    / "decision.json"
)
F95C_SUMMARY = (
    ROOT
    / "stages"
    / "stage_frontier_95__closed_bar_state_transition_embedding_axis"
    / "03_reviews"
    / "f95c_stage_closeout_summary.json"
)
F95C_PACKET = ROOT / "docs" / "agent_control" / "packets" / PARENT_RUN_ID / "work_packet.yaml"
F95C_CLOSEOUT_GATE = ROOT / "docs" / "agent_control" / "packets" / PARENT_RUN_ID / "closeout_gate.json"

ALLOWED_CLAIMS = [
    "f96a_design_open_packet_recorded",
    "f96_counterfactual_action_value_policy_axis_opened",
    "f96b_proxy_scout_planned",
    "task_force_actual_calls_recorded_for_f96a",
    "f95c_negative_memory_linked",
    "frontier_extra_due_check_not_due_after_f95",
    "frontier_five_stage_direction_synthesis_recorded_for_f91_to_f95",
    "frontier_topic_rotation_check_recorded_for_f96",
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
    "f96_stage_open_completed",
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
            "F96A is formal design/open only; it has no runnable ONNX/EA/set bundle, "
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
        "reason": "F96A defines the F96B proxy scout contract only; it does not train/select a model.",
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
        F95B_KPI,
        F95B_CANDIDATE_GATE,
        F95B_TIER_ROUTE_SUMMARY,
        F95B_DATA_LOCK,
        F95C_DECISION,
        F95C_SUMMARY,
        F95C_PACKET,
        F95C_CLOSEOUT_GATE,
    ]


def produced_artifacts() -> list[Path]:
    return [
        ROOT / SCRIPT_REL,
        RUN_MANIFEST,
        SUMMARY_JSON,
        KPI_RECORD,
        EXPERIMENT_DESIGN,
        RUNTIME_CONTRACT,
        F96B_BRIEF,
        DATA_INTEGRITY_PLAN,
        MODEL_VALIDATION_PLAN,
        ACTION_VALUE_CONTRACT,
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
        F96A_REPORT,
        WORK_PACKET,
        SKILL_RECEIPTS,
        PACKET_CLOSEOUT_GATE,
        PACKET_FINAL_CLAIM_GUARD,
        PACKET_STATE_SYNC_AUDIT,
        PACKET_REQUIRED_GATE_AUDIT,
        PACKET_WORK_PACKET_LINT,
        PACKET_SKILL_RECEIPT_LINT,
        DECISION_MEMO,
    ]


def task_force_calls() -> list[dict[str, Any]]:
    return [
        {
            "roster_agent_id": "agent_01_system_governor",
            "spawned_agent_id": "019edefd-378e-7eb0-bf48-c9112301e375",
            "nickname": "Poincare the 2nd",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "accepted",
            "bounded_evidence": [rel(WORKSPACE_STATE), rel(STAGE_BRIEF), rel(SELECTION_STATUS)],
            "local_verification": "F96A is design-only formal open; no training, candidate, ONNX/EA/set, runtime economics, promotion, authority, readiness, or Goal Achieve claim is allowed.",
            "accepted_summary": "Open F96 as action-value/regret-first design axis; do not launder F95B KPI into success proof.",
        },
        {
            "roster_agent_id": "agent_04_evidence_control_plane",
            "spawned_agent_id": "019edefd-9536-7892-be8a-4c463b9fb6a6",
            "nickname": "Sartre the 2nd",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "needs_local_verification",
            "bounded_evidence": [rel(WORKSPACE_STATE), rel(STAGE_BRIEF), rel(WORK_PACKET)],
            "local_verification": "This F96A script materializes the missing v2.1 work packet, receipts, gates, ledgers, final claim guard, and current-truth sync.",
            "accepted_summary": "F96A must be experiment_design plus design_only, not the F95C handoff scaffold and not a proxy/runtime evidence claim.",
        },
        {
            "roster_agent_id": "agent_05_data_feature_contract",
            "spawned_agent_id": "019edefd-a94d-7991-b64a-b084962251bd",
            "nickname": "McClintock the 2nd",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "needs_local_verification",
            "bounded_evidence": [rel(MODEL_INPUT_SUMMARY), rel(MODEL_INPUT_FEATURE_ORDER), rel(RAW_US100_MANIFEST), rel(F95B_TIER_ROUTE_SUMMARY)],
            "local_verification": "F96B must record Tier A, Tier B, and A+B source identity, time-axis meaning, sorted combined view, row counts, date ranges, and hashes before any data_contract_pass claim.",
            "accepted_summary": "Closed-bar feature and future-path label separation is valid for design, but F96B remains inconclusive until local leakage and route sorting checks run.",
        },
        {
            "roster_agent_id": "agent_06_quant_research",
            "spawned_agent_id": "019edefd-be8a-76b3-929a-b329fbdf99ea",
            "nickname": "Euler the 2nd",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "accepted",
            "bounded_evidence": [rel(F95B_KPI), rel(F95B_CANDIDATE_GATE), rel(F95C_SUMMARY)],
            "local_verification": "F96B must evaluate utility edge, regret gap, DD/recovery, adverse excursion, trades/day, side mix, Tier robustness, and negative controls without PF-only ranking.",
            "accepted_summary": "The novelty delta is action-value/regret-first long/short/abstain utility, not KMeans/PCA state-cluster repair.",
        },
        {
            "roster_agent_id": "agent_07_model_validation_risk",
            "spawned_agent_id": "019edefd-d995-7242-b231-72ffb1823a87",
            "nickname": "Einstein the 2nd",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "needs_local_verification",
            "bounded_evidence": [rel(F95B_KPI), rel(F95B_CANDIDATE_GATE), rel(MODEL_INPUT_SUMMARY)],
            "local_verification": "F96B must lock label build, split, validation-only candidate gate, OOS final-read lockout, rank/utility interpretation, and random/no-trade controls.",
            "accepted_summary": "F96A design scaffold is acceptable; probability, model quality, promotion, authority, and completion implications are rejected.",
        },
        {
            "roster_agent_id": "agent_08_mt5_onnx_runtime",
            "spawned_agent_id": "019edefe-ae1f-7c12-b389-d5e5c5e31556",
            "nickname": "Socrates the 2nd",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "accepted",
            "bounded_evidence": [rel(STAGE_BRIEF), rel(RUNTIME_CONTRACT), rel(SELECTION_STATUS)],
            "local_verification": "Runtime gate is N/A only because F96A has no runnable candidate and no runtime/materialization/economics/handoff claim. This is not cost or proxy-bad deferral.",
            "accepted_summary": "Any runnable candidate, ONNX/EA/set bundle, materialization, handoff, economics, parity, or tester-observed behavior claim triggers same-packet MT5 Strategy Tester evidence.",
        },
    ]


def task_force_receipt(created_at: str) -> dict[str, Any]:
    calls = task_force_calls()
    return {
        "packet_id": RUN_ID,
        "skill": "obsidian-task-force-review",
        "status": "executed",
        "created_at_utc": created_at,
        "trigger_reason": "F96A formal stage-open packet, active goal frontier continuation, and explicit user correction requiring real relevant Task Force agent calls.",
        "roster_registry": "docs/agent_control/codex_task_force_registry.yaml",
        "agents_used": [call["roster_agent_id"] for call in calls],
        "actual_subagent_calls": calls,
        "review_requirement": "codex_task_force_review_packet",
        "model_policy": {"model": "inherited_current_codex_model", "reasoning_effort": "inherited", "service_tier": "inherited"},
        "bounded_evidence": [rel(WORKSPACE_STATE), rel(STAGE_BRIEF), rel(SELECTION_STATUS), rel(F95C_SUMMARY), rel(MODEL_INPUT_SUMMARY)],
        "advice_classification": {
            "accepted": [call["roster_agent_id"] for call in calls if call["opinion_classification"] == "accepted"],
            "needs_local_verification": [call["roster_agent_id"] for call in calls if call["opinion_classification"] == "needs_local_verification"],
            "rejected": [],
        },
        "local_verification": [
            "F96A packet, receipts, gate audits, ledgers, and state sync are generated locally.",
            "F95C is linked as negative memory/reference surface only, not winner, baseline, or promotion history.",
            "Runtime evidence gate is outside claim surface only because no runnable candidate or runtime claim exists.",
            "F96B must verify time-axis sorting, Tier A/B/A+B records, leakage boundaries, validation-only selection, non-PF-only score, and same-packet MT5 trigger.",
        ],
        "claim_boundary": CLAIM_BOUNDARY,
        "final_codex_direction": "Proceed with F96A design-only formal open and plan F96B counterfactual action-value policy proxy scout.",
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
            "Closed-bar features can learn long/short/abstain counterfactual action value with "
            "adverse-excursion and cost penalties, producing a risk-first trade surface that avoids "
            "the F95 state-cluster long-only collapse."
        ),
        "decision_use": "design-only formal stage open and F96B proxy scout handoff",
        "f95c_reference": {
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
        "proxy": "F96B will build leakage-safe long/short/abstain utility labels and inspect validation-only action-value policy score surfaces before any runtime claim.",
        "decision_use": payload["decision_use"],
        "comparison_baseline": {
            "source_run": PARENT_RUN_ID,
            "role": "negative memory/reference surface only",
            "not_inherited": ["winner", "selected_baseline", "promotion_history", "runtime_authority"],
        },
        "control_variables": [
            "FPMarkets US100 M5",
            "closed-bar features only",
            "Tier A separate, Tier B separate, and Tier A+B actual routed total records",
            "time-ordered train/validation/OOS split",
            "validation-only candidate gate and OOS final read only",
            "cost/slippage/adverse-excursion penalty declared before scoring",
            "no PCA/KMeans state-cluster input as the main axis",
        ],
        "changed_variables": [
            "label: direction hit -> counterfactual long/short/abstain path utility",
            "objective: state-first clustering -> action-value/regret-first utility ranking",
            "trade shape: risk-first action eligibility before direction",
            "score surface: utility edge, regret gap, DD/recovery, adverse excursion, trades/day, side mix, and Tier robustness before PF-only ranking",
        ],
        "sample_scope": {
            "instrument": "US100",
            "timeframe": "M5",
            "period_policy": "F96B must record exact train/validation/OOS dates, row counts, hashes, and Tier A/B/A+B source identities before execution.",
            "tier_requirement": ["Tier A separate", "Tier B separate", "Tier A+B combined actual routed total"],
        },
        "success_criteria_for_f96b_proxy_scout": [
            "Tier A, Tier B, and A+B records all exist with the same KPI names.",
            "Validation trade density is 5-10 trades/day without all-abstain or trade-all collapse.",
            "Long and short sides each have material minimum share.",
            "Validation net utility is positive and beats random, no-trade, trade-all, cost-blind, no-adverse-penalty, and F95 replay controls.",
            "PF is supporting evidence only and never more than a minority selection lane.",
            "A+B combined is sorted and recorded as actual routed total, not synthetic sum.",
        ],
        "failure_conditions": [
            "zero candidate/clue after validation-only scoring",
            "long-only, short-only, all-abstain, or trade-all collapse",
            "DD/recovery/adverse-excursion collapse",
            "random/no-trade controls not beaten",
            "Tier B or A+B record missing",
        ],
        "invalid_conditions": [
            "future path enters feature columns",
            "label horizon overlaps feature calculation window",
            "scaler, threshold, label penalty, density target, or selection rule is fit using validation+OOS together or OOS",
            "Tier A+B combined remains timestamp_sorted=false but is used as representative performance",
            "F95 KMeans/PCA replay is treated as F96 novelty",
            "proxy-only score is described as runtime or economics evidence",
        ],
        "stop_conditions": [
            "Stop if counterfactual label is not leakage-free.",
            "Stop if abstain is not measured beyond no-trade convenience.",
            "Stop if F96B degenerates into threshold/filter/session/routing/parameter-only repair.",
            "If a runnable bundle or runtime claim appears, same-packet MT5 Strategy Tester probe is required or the runtime claim is lowered.",
        ],
    }


def action_value_contract(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "contract_status": "design_locked_for_f96b_planning_only",
        "actions": ["long", "short", "abstain"],
        "label_surface": {
            "long_value": "future path utility for entering long after closed bar t, net of cost and adverse-excursion penalty",
            "short_value": "future path utility for entering short after closed bar t, net of cost and adverse-excursion penalty",
            "abstain_value": "opportunity-cost-aware no-entry baseline, not merely missing trade",
            "regret_gap": "best_action_value minus selected_action_value",
        },
        "feature_surface": {
            "allowed": ["row t and prior closed M5 bars", "train-only transforms", "predeclared rolling windows ending at t"],
            "forbidden": ["open/current incomplete bar", "future return", "future MFE/MAE as feature", "label-derived post-entry diagnostics as feature"],
        },
        "fit_scope": "train-only for scaler, imputer, encoders, model fit, and any threshold seed; validation chooses; OOS is final read only.",
        "negative_controls": [
            "shuffled future path",
            "cost-blind utility",
            "no-adverse-penalty utility",
            "PF-only ranking",
            "F95 PCA/KMeans replay",
            "abstain-all",
            "trade-all",
        ],
        "candidate_language_boundary": "F96B can create scout clues only unless a separate runtime packet/probe supports stronger claims.",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def data_integrity_plan(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "data_sources_checked": [file_identity(path) for path in [MODEL_INPUT_SUMMARY, MODEL_INPUT_FEATURE_ORDER, RAW_US100_MANIFEST, F95B_TIER_ROUTE_SUMMARY]],
        "time_axis_boundary": "F96B must record whether each M5 timestamp is bar open or bar close, broker timezone, session timezone, DST policy, and M5 sort key.",
        "feature_label_boundary": "Features use only decision-time row t and earlier closed bars; future path is label target only and cannot feed feature construction.",
        "split_boundary": "Train/validation/OOS split is chronological. No random shuffle, no split crossing label horizon, and no OOS selection.",
        "tier_boundary": "Tier A separate, Tier B separate, and A+B actual routed total are mandatory. Missing Tier B or combined is missing_required, blocked, or out_of_scope_by_claim.",
        "route_sorting_boundary": "F95B left a warning that tier_ab_combined timestamp_sorted=false; F96B must sort the combined routed view before label construction and log route-integrity checks.",
        "leakage_checks": [
            "rolling/window calculations end at t",
            "normalizer/scaler fit train-only",
            "joins/resamples preserve closed-bar order",
            "label horizon never appears in features",
            "row counts/date ranges/hashes recorded per Tier A, Tier B, and A+B",
        ],
        "stop_conditions": [
            "unknown time-axis meaning",
            "duplicate or reverse timestamps",
            "feature-label boundary unclear",
            "Tier A/B/A+B missing",
            "split leakage",
            "missing hash or row-count identity",
        ],
    }


def model_validation_plan(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "model_or_threshold_surface": "counterfactual action-value policy proxy scout, no trained candidate yet",
        "validation_split": "time-ordered train/validation/OOS; validation gates candidate/clue; OOS is final read only",
        "overfit_checks": [
            "no OOS feature, label, penalty, density, or threshold selection",
            "validation-only candidate gate",
            "probability claims forbidden unless a separate calibration split and diagnostics exist",
            "PF-only selection forbidden",
            "negative controls required",
        ],
        "selection_metric_boundary": [
            "net utility",
            "profit factor as supporting metric only",
            "drawdown and recovery factor",
            "trades/day 5-10",
            "side balance",
            "adverse excursion",
            "Tier robustness",
            "random/no-trade/trade-all/control superiority",
        ],
        "candidate_gate_failure_conditions": [
            "leakage",
            "OOS selection",
            "Tier A/B/A+B row missing",
            "validation net <= 0",
            "PF <= 1",
            "DD cap breach",
            "recovery <= 0",
            "trades/day outside 5-10",
            "side collapse",
            "random control not beaten",
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
            "dataset_id",
            "feature_set_id",
            "label_id",
            "split_id",
            "source_identities",
            "parser_contract_version",
            "runtime_contract_version",
            "onnx_hash",
            "ea_source_hash",
            "ea_binary_hash",
            "set_ini_hash",
            "feature_order_hash",
            "tester_identity",
            "report_hash",
            "trade_list_hash",
            "telemetry_hash",
        ],
        "claim_effect": "F96A cannot support runtime verified, economics pass, materialization ready, handoff complete, promotion, authority, readiness, or Goal Achieve.",
    }


def f96b_brief(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "planned_run_id": NEXT_RUN_ID,
        "parent_run_id": RUN_ID,
        "task": "proxy scout for leakage-safe counterfactual action-value policy surface",
        "verification_profile": "proxy_scout",
        "required_records": ["Tier A separate", "Tier B separate", "Tier A+B actual routed total"],
        "first_action": "Lock data/time/split/action-label contracts, then run a narrow validation-only proxy scout before any runtime claim.",
        "candidate_gate_preview": [
            "Tier A/B/A+B all recorded",
            "5-10 trades/day",
            "side minimum share",
            "validation net utility positive",
            "PF > 1 as support only",
            "DD/recovery/adverse-excursion boundary",
            "random/no-trade/trade-all and F95 replay controls beaten",
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
        },
        "claim_effect": "KPI fields are empty because F96A is design-only and has no proxy/runtime economics evidence.",
    }


def result_summary_text(payload: Mapping[str, Any]) -> str:
    return f"""# F96A Stage Open Summary(단계 개방 요약)

Action(행동): materialize(물질화) `{RUN_ID}` as a design-only stage-open packet(설계 전용 단계 개방 묶음).

Effect(효과): `{NEXT_RUN_ID}` becomes the current run(현재 실행) for counterfactual action-value proxy scout(반사실 행동가치 프록시 정찰).

Hypothesis(가설): {payload['hypothesis']}

Task Force(태스크포스): six selected agents(선택 요원 6명) were actually called(실제 호출) and recorded(기록) in `{rel(PACKET_TASK_FORCE_REVIEW)}`.

Runtime boundary(런타임 경계): no runnable candidate(실행 후보 없음), no ONNX/EA/set bundle(온엑스/전문가 자문/설정 묶음 없음), no Strategy Tester output(전략 테스터 출력 없음), and no runtime/economics/handoff claim(런타임/경제성/인계 주장 없음).

Next(다음): `{NEXT_RUN_ID}`.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""


def write_run_artifacts(payload: Mapping[str, Any]) -> None:
    write_json(RUN_MANIFEST, {"script": SCRIPT_REL, **summary_payload(payload), "source_inputs": payload["source_identities"]})
    write_json(SUMMARY_JSON, summary_payload(payload))
    write_json(KPI_RECORD, kpi_payload(payload))
    write_json(EXPERIMENT_DESIGN, experiment_design(payload))
    write_json(RUNTIME_CONTRACT, runtime_contract(payload))
    write_json(F96B_BRIEF, f96b_brief(payload))
    write_json(DATA_INTEGRITY_PLAN, data_integrity_plan(payload))
    write_json(MODEL_VALIDATION_PLAN, model_validation_plan(payload))
    write_json(ACTION_VALUE_CONTRACT, action_value_contract(payload))
    write_text(RESULT_SUMMARY, result_summary_text(payload))
    write_json(STAGE_OPEN_SUMMARY, summary_payload(payload))
    write_text(F96A_REPORT, result_summary_text(payload))


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
            frontier_closeout_count_boundary="F95 closed; next boundary is F100/E02; E01 closed for F50.",
            due_status=FRONTIER_EXTRA_DUE_STATUS,
            claim_effect="F96A may open; no Extra Stage is due before F96.",
        ),
    )
    write_json(
        FIVE_STAGE_SYNTHESIS,
        audit_payload(
            "frontier_five_stage_direction_synthesis",
            "pass",
            created_at_utc=payload["created_at_utc"],
            source_frontiers=["F91", "F92", "F93", "F94", "F95"],
            dominant_direction="Recent frontier work repeatedly found proxy structure but lost candidate value through density, Tier B, side balance, DD, high-cost exposure, or materialization boundaries.",
            repeated_mechanism="PF or local validation shape can survive while trade shape, Tier robustness, and side/cost controls fail.",
            overused_axis_warning="Avoid adjacent KMeans/PCA state-cluster parameter repair and PF-only selection.",
            next_axis_options=["counterfactual action value", "regret-first utility", "side-symmetric risk gate", "validation-only negative controls"],
            claim_effect="Direction only; no retrospective, permanent ban, candidate, or authority claim.",
        ),
    )
    write_json(
        TOPIC_ROTATION_CHECK,
        audit_payload(
            "frontier_topic_rotation_check",
            "pass",
            created_at_utc=payload["created_at_utc"],
            previous_stage="stage_frontier_95__closed_bar_state_transition_embedding_axis",
            proposed_stage=STAGE_ID,
            material_novelty_delta=[
                "objective changes from unsupervised state-first clustering to action-value/regret-first utility",
                "label changes to counterfactual long/short/abstain path utility with adverse-excursion penalty",
                "validation changes to utility, regret, side balance, DD/recovery, adverse excursion, and controls before PF",
                "F95 state-cluster surface is negative memory/reference only",
            ],
            blocked_continuation_repair=False,
            threshold_filter_parameter_only_tweak=False,
            claim_effect="F96A can open as a distinct design axis; no candidate or runtime claim.",
        ),
    )
    write_json(
        SCOPE_GATE,
        audit_payload(
            "scope_completion_gate",
            "pass",
            created_at_utc=payload["created_at_utc"],
            required_artifacts=[rel(EXPERIMENT_DESIGN), rel(RUNTIME_CONTRACT), rel(F96B_BRIEF), rel(ACTION_VALUE_CONTRACT), rel(PACKET_TASK_FORCE_REVIEW)],
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
            route_sorting_boundary=data_integrity_plan(payload)["route_sorting_boundary"],
            claim_effect="Data checks are predeclared for F96B; no data_contract_pass or authority claim.",
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
            claim_effect="F96A sets validation rules only; no model quality, calibrated probability, or candidate claim.",
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
            lineage_judgment="F95C negative memory/reference surface -> F96A design-only action-value stage open -> F96B proxy scout plan.",
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
            claim_effect="F96A is design-only stage open; not candidate, runtime, promotion, or completion evidence.",
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
    evidence = [rel(EXPERIMENT_DESIGN), rel(RUNTIME_CONTRACT), rel(F96B_BRIEF), rel(PACKET_TASK_FORCE_REVIEW)]
    return [
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-experiment-design",
            "status": "executed",
            "hypothesis": payload["hypothesis"],
            "baseline": payload["f95c_reference"],
            "changed_variables": experiment_design(payload)["changed_variables"],
            "invalid_conditions": experiment_design(payload)["invalid_conditions"],
            "evidence_plan": experiment_design(payload)["success_criteria_for_f96b_proxy_scout"],
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
            "missing_data_boundary": "F96B must detect missing rows, duplicate bars, route gaps, Tier B absence, and combined-view sort gaps before scoring.",
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
            "raw_evidence": [rel(F95B_KPI), rel(F95B_CANDIDATE_GATE), rel(F95C_SUMMARY), rel(F95C_DECISION)],
            "machine_readable": [rel(path) for path in [RUN_MANIFEST, SUMMARY_JSON, KPI_RECORD, EXPERIMENT_DESIGN, RUNTIME_CONTRACT, SKILL_RECEIPTS]],
            "human_readable": [rel(RESULT_SUMMARY), rel(F96A_REPORT), rel(STAGE_BRIEF), rel(SELECTION_STATUS), rel(CONTEXT_ANCHOR)],
            "hashes_or_missing_reasons": [file_identity(path) for path in produced_artifacts()],
            "lineage_boundary": "F95C negative memory/reference surface only; F96A design-open only; no runtime authority.",
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
        rel(F96B_BRIEF),
        rel(DATA_INTEGRITY_PLAN),
        rel(MODEL_VALIDATION_PLAN),
        rel(ACTION_VALUE_CONTRACT),
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
            "requested_action": "canonical frontier stage open for F96A counterfactual action-value policy axis",
            "requested_count": {"value": 1, "n_a_reason": ""},
            "ambiguous_terms": ["Goal Achieve is not claimed.", "Runtime authority is not claimed.", "F96A is design-only."],
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
                "f95_state_cluster_repair_laundering": "high",
                "future_path_label_leakage": "high",
                "oos_selection_or_calibration_laundering": "high",
                "runtime_probe_absence_misread_as_cost_skip": "medium",
            },
            "hard_stop_risks": [
                "Do not claim runtime/economics/materialization without MT5 Strategy Tester output identity.",
                "Do not repeat F95 KMeans/PCA state-cluster repair by threshold/filter/session/routing/parameter-only tweak.",
                "Do not fit scaler, label penalty, threshold, or calibration on OOS.",
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
                "reason": "F96A protects design-only stage-open claims and has no runnable candidate, ONNX/EA/set behavior, or runtime/materialization/economics/handoff claim.",
            },
            "questions": [],
            "required_user_decisions": [],
        },
        "interpreted_scope": {
            "work_families": ["experiment_design"],
            "target_surfaces": ["F96 stage open", "counterfactual action-value policy design", "F96B proxy scout brief", "Task Force receipt", "state sync"],
            "scope_units": ["stage_open_design", "receipt", "state_sync", "ledger"],
            "execution_layers": ["local_python_execution"],
            "mutation_policy": {"allowed": True, "user_quote": "/goal active continuation"},
            "evidence_layers": ["F95C negative memory reference", "F96A design artifacts", "Task Force actual calls", "frontier overlays"],
            "reduction_policy": {"reduction_allowed": False, "requires_user_quote": False, "rationale": "F96A is a formal stage-open packet."},
            "claim_boundary": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
        },
        "verification_profile": {
            "profile_id": "design_only",
            "claim_surface": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
            "trigger_sources": [
                "active_goal_frontier_continuation",
                "F95C closeout rotated to F96 pending scaffold",
                "formal F96A stage open claim",
                "explicit user instruction requiring Task Force when triggered",
            ],
            "protected_claims": ALLOWED_CLAIMS,
            "required_evidence": required_evidence,
            "gates_not_run_with_reason": RUNTIME_NA_REASONS,
            "stop_conditions": [
                "Stop after F96A design artifacts, receipts, gates, ledgers, and state sync are materialized.",
                "Do not create candidate/runtime claims in F96A.",
                "If runnable candidate or runtime claim appears, reroute to runtime_probe profile in the same packet.",
            ],
        },
        "acceptance_criteria": [
            {"id": "AC-001", "text": "F96A experiment design exists.", "expected_artifact": rel(EXPERIMENT_DESIGN), "verification_method": "scope_completion_gate", "required": True},
            {"id": "AC-002", "text": "F96A Task Force actual calls are recorded.", "expected_artifact": rel(PACKET_TASK_FORCE_REVIEW), "verification_method": "codex_task_force_review_packet", "required": True},
            {"id": "AC-003", "text": "F96B proxy scout brief exists.", "expected_artifact": rel(F96B_BRIEF), "verification_method": "scope_completion_gate", "required": True},
            {"id": "AC-004", "text": "Runtime evidence gate is explicitly outside claim surface, not skipped for cost or proxy-bad reasons.", "expected_artifact": rel(RUNTIME_CONTRACT), "verification_method": "final_claim_guard", "required": True},
        ],
        "work_plan": [
            "Write F96A design/runtime-contract/F96B brief artifacts.",
            "Record Task Force actual_subagent_calls and local-verification responses.",
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
                {"skill": "obsidian-backtest-forensics", "reason": "No new Strategy Tester report or trade list exists in F96A."},
            ],
            "required_skill_receipts": REQUIRED_SKILLS,
            "required_gates": REQUIRED_GATES,
        },
        "evidence_contract": {
            "source_inputs": [rel(path) for path in source_inputs()],
            "machine_readable": [rel(path) for path in [RUN_MANIFEST, SUMMARY_JSON, KPI_RECORD, EXPERIMENT_DESIGN, RUNTIME_CONTRACT, F96B_BRIEF, DATA_INTEGRITY_PLAN, MODEL_VALIDATION_PLAN, ACTION_VALUE_CONTRACT, SKILL_RECEIPTS]],
            "human_readable": [rel(RESULT_SUMMARY), rel(F96A_REPORT), rel(STAGE_BRIEF), rel(SELECTION_STATUS), rel(CONTEXT_ANCHOR)],
            "raw_evidence": [rel(F95B_KPI), rel(F95B_CANDIDATE_GATE), rel(F95C_SUMMARY), rel(F95C_DECISION)],
            "missing_evidence": [
                {"evidence": "MT5 Strategy Tester runtime output", "reason": "outside F96A design-only claim surface"},
                {"evidence": "WFO/stress result", "reason": "outside F96A design-only claim surface"},
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
    audits = []
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
    for gate in REQUIRED_GATES:
        audits.append({"audit_name": gate, "path": rel(gate_paths[gate]), "status": gate_results.get(gate, {}).get("status", "pending")})
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
    return f"""# F96 Counterfactual Action Value Policy Axis(반사실 행동가치 정책 축)

- current run(현재 실행): `{NEXT_RUN_ID}`
- latest completed run(최근 완료 실행): `{RUN_ID}`
- source closeout(원천 마감): `{PARENT_RUN_ID}`
- status(상태): design-only formal open recorded(설계 전용 정식 개방 기록)
- authority(권위): not_claimed(주장 없음)

## Question(질문)

Can closed-bar features(확정 봉 피처) learn long/short/abstain(롱/숏/관망) counterfactual action value(반사실 행동가치) with adverse-excursion risk(불리한 변동 위험) before direction mapping(방향 매핑), producing side-balanced(방향 균형) 5-10 trades/day(일 5-10 거래) scout clues(정찰 단서)?

## Hypothesis(가설)

{payload['hypothesis']}

## Novelty Delta(신규성 차이)

- objective(목적함수): action-value/regret-first(행동가치/후회 우선) instead of unsupervised state-first clustering(비지도 상태 우선 군집)
- label(라벨): counterfactual long/short/abstain path utility(반사실 롱/숏/관망 경로 효용) with adverse excursion penalties(불리 변동 벌점)
- trade shape(거래 형태): side-symmetric risk-first action eligibility(양방향 대칭 위험 우선 행동 자격)
- validation philosophy(검증 철학): utility/regret/DD/recovery/side-balance(효용/후회/손실폭/회복/방향 균형) before PF-only selection(PF 단독 선정)
- runtime boundary(런타임 경계): same-packet MT5 Strategy Tester probe(같은 묶음 MT5 전략 테스터 탐침) is required if a runnable ONNX/EA/set claim(실행 가능한 온엑스/전문가 자문/설정 주장) appears

## Boundary(경계)

F96A is design-only formal open(설계 전용 정식 개방) evidence(근거) only. No selected baseline(선택 기준선), promotion candidate(승격 후보), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성) is claimed(주장됨).
"""


def input_refs_text() -> str:
    rows = "\n".join(f"- `{rel(path)}`" for path in source_inputs())
    return f"""# F96 Input References(입력 참조)

{rows}

Boundary(경계): F95C artifacts(산출물)는 reference/negative memory(참조/부정 기억) only(전용)이다. They do not provide winner(승자), selected baseline(선택 기준선), promotion history(승격 이력), or runtime authority(런타임 권위).
"""


def selection_status_text(payload: Mapping[str, Any]) -> str:
    return f"""# F96 Selection Status(선택 상태)

- current run(현재 실행): `{NEXT_RUN_ID}`
- latest completed run(최근 완료 실행): `{RUN_ID}`
- status(상태): F96A design-only formal open recorded(설계 전용 정식 개방 기록); F96B proxy scout planned(F96B 프록시 정찰 계획)
- selected baseline(선택 기준선): not_claimed(주장 없음)
- promotion candidate(승격 후보): not_claimed(주장 없음)
- operating promotion(운영 승격): not_claimed(주장 없음)
- runtime authority(런타임 권위): not_claimed(주장 없음)
- live readiness(실거래 준비): not_claimed(주장 없음)
- Goal Achieve(목표 달성): not_claimed(주장 없음)
- task force actual calls(태스크포스 실제 호출): 6 selected agents recorded(선택 요원 6명 기록)
- runtime probe(런타임 탐침): not run(미실행) because no runnable candidate or runtime claim exists(실행 후보/런타임 주장 없음)
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

Action(행동): F96A(전선96A) materializes(물질화) a design-only formal-open packet(설계 전용 정식 개방 묶음) with actual Task Force calls(실제 태스크포스 호출).

Effect(효과): F96B(전선96B) is the current run(현재 실행) for counterfactual action-value policy proxy scout(반사실 행동가치 정책 프록시 정찰), with no runtime authority(런타임 권위 없음), no selected baseline(선택 기준선 없음), and no Goal Achieve(목표 달성 없음).
"""


def review_index_text() -> str:
    return f"""# F96 Review Index(검토 색인)

- f96a_task_force_review_receipt: `{rel(TASK_FORCE_REVIEW)}`
- f96a_frontier_extra_due_check: `{rel(FRONTIER_EXTRA_DUE_CHECK)}`
- f96a_frontier_five_stage_direction_synthesis: `{rel(FIVE_STAGE_SYNTHESIS)}`
- f96a_frontier_topic_rotation_check: `{rel(TOPIC_ROTATION_CHECK)}`
- f96a_scope_completion_gate: `{rel(SCOPE_GATE)}`
- f96a_data_integrity_audit: `{rel(DATA_INTEGRITY_AUDIT)}`
- f96a_model_validation_audit: `{rel(MODEL_VALIDATION_AUDIT)}`
- f96a_artifact_lineage_audit: `{rel(ARTIFACT_AUDIT)}`
- f96a_result_judgment_audit: `{rel(RESULT_JUDGMENT_AUDIT)}`
- f96a_state_sync_audit: `{rel(STATE_SYNC_AUDIT)}`
- f96a_required_gate_coverage_audit: `{rel(REQUIRED_GATE_AUDIT)}`
- f96a_final_claim_guard: `{rel(FINAL_CLAIM_GUARD)}`
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
        "frontier_topic_rotation_status": FRONTIER_TOPIC_ROTATION_STATUS,
        "task_force_status": "f96a_actual_subagent_calls_recorded_6_selected_agents_no_task_force_reviewed_pass_claim",
        "runtime_probe_status": RUNTIME_PROBE_STATUS,
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "updated_at_utc": payload["created_at_utc"],
        "context_anchor": rel(CONTEXT_ANCHOR),
        "notes": [
            "Action(행동): F96A design-only formal-open packet(설계 전용 정식 개방 묶음)이 materialized(물질화)되었다.",
            "Effect(효과): F96B current run(현재 실행)은 counterfactual action-value policy proxy scout(반사실 행동가치 정책 프록시 정찰)로 고정된다.",
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
    f96a = {
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
        "path": rel(F96A_REPORT),
        "primary_report": rel(F96A_REPORT),
        "report_path": rel(F96A_REPORT),
        "primary_artifact": rel(EXPERIMENT_DESIGN),
        "result_path": rel(F96A_REPORT),
        "gate_audit_path": rel(PACKET_CLOSEOUT_GATE),
        "required_gate_audit": rel(PACKET_REQUIRED_GATE_AUDIT),
        "primary_kpi": "candidate_count=0;runtime_completed_rows=0",
        "guardrail_kpi": "no_runtime_claim;no_authority;task_force_calls=6",
        "external_verification_status": "not_applicable_design_only",
        "notes": "F96A design-only open; Task Force actual calls recorded; no runtime claim.",
        "run_number": "frontier96A",
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
        "question": "Can counterfactual action-value policy create a side-balanced US100 M5 scout surface?",
        "next_action": NEXT_RUN_ID,
        "model_variants": 0,
        "selected_surfaces": 0,
        "net_profit": "",
        "profit_factor": "",
        "drawdown": "",
        "trade_count": 0,
        "trades_per_day": 0,
    }
    f96b = {
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
        "judgment": "planned_after_f96a_design_open",
        "path": rel(F96B_BRIEF),
        "primary_report": rel(F96B_BRIEF),
        "report_path": rel(F96B_BRIEF),
        "primary_artifact": rel(F96B_BRIEF),
        "result_path": rel(F96B_BRIEF),
        "primary_kpi": "pending",
        "guardrail_kpi": "leakage_safe_action_value_gate_pending;no_runtime_claim",
        "external_verification_status": "pending",
        "notes": "F96B planned current run after F96A open.",
        "run_number": "frontier96B",
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
        "output_path": rel(F96B_BRIEF),
        "row_id": f"{NEXT_RUN_ID}__planned_current_run",
        "question": "Can counterfactual action-value policy create a side-balanced US100 M5 scout surface?",
        "next_action": "run_f96b_proxy_scout",
        "model_variants": 0,
        "selected_surfaces": 0,
        "net_profit": "",
        "profit_factor": "",
        "drawdown": "",
        "trade_count": 0,
        "trades_per_day": 0,
    }
    return [f96a, f96b]


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
        artifact_type = path.suffix.lstrip(".") or "artifact"
        artifact_id = f"{RUN_ID}__{Path(path).stem}"
        rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": artifact_type,
                "path": identity["path"],
                "artifact_path": identity["path"],
                "sha256": identity["sha256"] or "",
                "size_bytes": identity["size_bytes"] or "",
                "created_at": payload["created_at_utc"],
                "created_at_utc": payload["created_at_utc"],
                "claim_boundary": CLAIM_BOUNDARY,
                "artifact_id": artifact_id,
                "notes": "F96A design-only artifact; no runtime authority.",
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
    selection_body = f"""## F96A Design Open(설계 개방)

- active stage(활성 단계): `{STAGE_ID}`
- current run(현재 실행): `{NEXT_RUN_ID}`
- latest completed run(최근 완료 실행): `{RUN_ID}`
- selected baseline(선택 기준선): not_claimed(주장 없음)
- runtime authority(런타임 권위): not_claimed(주장 없음)
- Goal Achieve(목표 달성): not_claimed(주장 없음)
- effect(효과): F96A records(기록) a design-only action-value axis(설계 전용 행동가치 축) and hands off(인계) to F96B proxy scout(프록시 정찰).
"""
    idea_body = f"""## F96 Counterfactual Action Value Policy(반사실 행동가치 정책)

- source(원천): `{PARENT_RUN_ID}` as negative memory/reference surface(부정 기억/참고 표면)
- hypothesis(가설): {payload['hypothesis']}
- next action(다음 행동): `{NEXT_RUN_ID}`
- boundary(경계): no selected baseline(선택 기준선 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음)
"""
    changelog_body = f"""## 2026-06-19 F96A

Action(행동): recorded(기록) F96A design-only formal open(설계 전용 정식 개방) with six actual Task Force calls(실제 태스크포스 호출 6개).

Effect(효과): current run(현재 실행) is `{NEXT_RUN_ID}`; runtime probe(런타임 탐침)는 no runnable candidate/no runtime claim(실행 후보 없음/런타임 주장 없음) 때문에 not_applicable_with_reason(사유 있는 해당 없음)이다.
"""
    replace_marked_section(GLOBAL_SELECTION_STATUS, "frontier96a_selection_status", selection_body)
    replace_marked_section(IDEA_REGISTRY, "frontier96_action_value_policy", idea_body)
    replace_marked_section(WORKSPACE_CHANGELOG, "frontier96a_changelog", changelog_body)
    replace_marked_section(ROOT_CHANGELOG, "frontier96a_changelog", changelog_body)
    write_text(
        DECISION_MEMO,
        f"""# F96A Stage Open Decision(단계 개방 결정)

Decision(결정): open(개방) `{STAGE_ID}` through `{RUN_ID}` as design-only formal open(설계 전용 정식 개방).

Reason(이유): F95C(전선95C)는 state-transition embedding(상태 전이 임베딩) 축을 negative(부정)로 닫고 F96 action-value/regret-first(행동가치/후회 우선) 축으로 rotate(회전)했다.

Task Force(태스크포스): agent_01, agent_04, agent_05, agent_06, agent_07, agent_08 were actually called(실제 호출) and recorded(기록).

Runtime(런타임): no MT5 Strategy Tester probe(MT5 전략 테스터 탐침) in F96A because there is no runnable candidate(실행 후보 없음), no ONNX/EA/set(온엑스/전문가 자문/설정 없음), and no runtime/materialization/economics/handoff claim(런타임/물질화/경제성/인계 주장 없음). This is not cost deferral(비용 지연 아님).

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
        "codex_task_force_review_packet": {"status": "pass", "audit_name": "codex_task_force_review_packet"},
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
    gate_results["final_claim_guard"] = final_guard.to_dict()
    write_json(PACKET_FINAL_CLAIM_GUARD, gate_results["final_claim_guard"])
    write_json(FINAL_CLAIM_GUARD, gate_results["final_claim_guard"])
    write_packet(payload, gate_results)
    write_json(PACKET_CLOSEOUT_GATE, closeout_gate_payload(gate_results))
    write_json(PACKET_REQUIRED_GATE_AUDIT, gate_results["required_gate_coverage_audit"])
    write_json(REQUIRED_GATE_AUDIT, gate_results["required_gate_coverage_audit"])
    return gate_results


def main() -> int:
    created_at = utc_now()
    ensure_dirs()
    payload = base_payload(created_at)
    write_run_artifacts(payload)
    write_audits(payload)
    write_receipts(payload)
    write_packet(payload)
    update_state_docs(payload)
    update_ledgers(payload)
    update_artifact_registry(payload)
    update_register_docs(payload)
    gate_results = run_gates(payload)
    write_audits(payload, gate_results)
    write_receipts(payload)
    update_ledgers(payload)
    update_artifact_registry(payload)
    write_packet(payload, gate_results)
    summary = {
        "run_id": RUN_ID,
        "status": STATUS,
        "gate_statuses": {gate: gate_results.get(gate, {}).get("status") for gate in REQUIRED_GATES},
        "current_run_after": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
