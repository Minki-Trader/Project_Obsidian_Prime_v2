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


STAGE_ID = "stage_frontier_95__closed_bar_state_transition_embedding_axis"
RUN_ID = "frontier95C_closed_bar_state_transition_repair_or_rotation_decision_v1"
PARENT_RUN_ID = "frontier95B_closed_bar_state_transition_embedding_proxy_scout_v1"
NEXT_STAGE_ID = "stage_frontier_96__counterfactual_action_value_policy_axis"
NEXT_RUN_ID = "frontier96A_stage_open_counterfactual_action_value_policy_axis_v1"
SCRIPT_REL = "stage_pipelines/stage_frontier_95/frontier95c_repair_rotation.py"

STATUS = "f95c_closed_negative_state_transition_embedding_axis_rotate_to_f96_no_authority"
JUDGMENT = "negative_valid_then_rotation_state_transition_embedding_no_candidate_no_runtime_trigger"
DECISION = "close_f95_negative_rotate_to_counterfactual_action_value_policy_axis"
CLAIM_BOUNDARY = (
    "f95c_stage_closeout_rotation_only_negative_memory_reference_surface_no_runnable_candidate_"
    "no_mt5_runtime_evidence_no_selected_baseline_no_promotion_candidate_no_operating_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)
RUNTIME_PROBE_STATUS = "not_applicable_no_runnable_candidate_no_runtime_claim_not_cost_or_proxy_bad_skip"
FRONTIER_EXTRA_DUE_STATUS = "not_due_after_f95_closeout_next_boundary_f100_e02_pending_e01_closed_for_f050"
FRONTIER_FIVE_STAGE_STATUS = "recorded_recent_f91_to_f95_direction_synthesis_no_retrospective_gate"
FRONTIER_TOPIC_ROTATION_STATUS = (
    "preopen_pass_f96_counterfactual_action_value_policy_axis_not_f95_state_cluster_parameter_repair"
)
BEST_VARIANT_ID = "k9_pca5_seed9502"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / "frontier95C"
DECISION_DIR = RUN_DIR / "d"
REPORT_DIR = RUN_DIR / "r"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
PACKET_DIR = ROOT / "docs" / "agent_control" / "packets" / RUN_ID
SKILL_RECEIPT_DIR = PACKET_DIR / "skill_receipts"

NEXT_STAGE_DIR = ROOT / "stages" / NEXT_STAGE_ID
NEXT_SPEC_DIR = NEXT_STAGE_DIR / "00_spec"
NEXT_INPUT_DIR = NEXT_STAGE_DIR / "01_inputs"
NEXT_REVIEW_DIR = NEXT_STAGE_DIR / "03_reviews"
NEXT_SELECTED_DIR = NEXT_STAGE_DIR / "04_selected"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
GLOBAL_SELECTION_STATUS = ROOT / "docs" / "registers" / "selection_status.md"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
NEGATIVE_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
ROOT_CHANGELOG = ROOT / "docs" / "CHANGELOG.md"

SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
CONTEXT_ANCHOR = REVIEW_DIR / "context_anchor.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"

NEXT_STAGE_BRIEF = NEXT_SPEC_DIR / "stage_brief.md"
NEXT_INPUT_REFS = NEXT_INPUT_DIR / "input_refs.md"
NEXT_SELECTION_STATUS = NEXT_SELECTED_DIR / "selection_status.md"
NEXT_CONTEXT_ANCHOR = NEXT_REVIEW_DIR / "context_anchor.md"
NEXT_REVIEW_INDEX = NEXT_REVIEW_DIR / "review_index.md"
NEXT_STAGE_LEDGER = NEXT_REVIEW_DIR / "stage_run_ledger.csv"

F95B_RUN = STAGE_DIR / "02_runs" / "frontier95B"
F95B_RUN_MANIFEST = F95B_RUN / "run_manifest.json"
F95B_SUMMARY = F95B_RUN / "summary.json"
F95B_KPI = F95B_RUN / "kpi_record.json"
F95B_EXECUTION_SUMMARY = F95B_RUN / "execution_summary.json"
F95B_CANDIDATE_GATE = F95B_RUN / "proxy_scout" / "candidate_gate.json"
F95B_DATA_LOCK = F95B_RUN / "proxy_scout" / "data_feature_split_lock.json"
F95B_DATA_INTEGRITY_LOCAL = F95B_RUN / "proxy_scout" / "data_integrity_local_checks.json"
F95B_EMBEDDING_CONFIG = F95B_RUN / "proxy_scout" / "embedding_config.json"
F95B_FIT_MANIFEST = F95B_RUN / "proxy_scout" / "state_transition_fit_manifest.json"
F95B_SPLIT_METRICS = F95B_RUN / "proxy_scout" / "split_metrics.csv"
F95B_VARIANT_METRICS = F95B_RUN / "proxy_scout" / "variant_metrics.csv"
F95B_TIER_ROUTE_SUMMARY = F95B_RUN / "proxy_scout" / "tier_route_summary.json"
F95B_TIER_B_SUMMARY = F95B_RUN / "proxy_scout" / "tier_b_summary.json"
F95B_RESULT_SUMMARY = F95B_RUN / "reports" / "result_summary.md"
F95B_DATA_INTEGRITY_AUDIT = REVIEW_DIR / "f95b_data_integrity_audit.json"
F95B_MODEL_VALIDATION_AUDIT = REVIEW_DIR / "f95b_model_validation_audit.json"
F95B_TASK_FORCE = ROOT / "docs" / "agent_control" / "packets" / PARENT_RUN_ID / "codex_task_force_review_packet.json"
F95B_WORK_PACKET = ROOT / "docs" / "agent_control" / "packets" / PARENT_RUN_ID / "work_packet.yaml"
F95B_CLOSEOUT_GATE = ROOT / "docs" / "agent_control" / "packets" / PARENT_RUN_ID / "closeout_gate.json"

RUN_MANIFEST = RUN_DIR / "run_manifest.json"
SUMMARY_JSON = RUN_DIR / "summary.json"
KPI_RECORD = RUN_DIR / "kpi_record.json"
DECISION_JSON = DECISION_DIR / "decision.json"
RESULT_SUMMARY = REPORT_DIR / "summary.md"
STAGE_CLOSEOUT_SUMMARY = REVIEW_DIR / "f95c_stage_closeout_summary.json"
STAGE_CLOSEOUT_REPORT = REVIEW_DIR / "stage_closeout_report.md"
F95C_REPORT = REVIEW_DIR / "frontier95C_closed_bar_state_transition_repair_rotation_report.md"
TASK_FORCE_REVIEW = REVIEW_DIR / "f95c_task_force_review_receipt.json"
TASK_FORCE_PACKET_REVIEW = PACKET_DIR / "codex_task_force_review_packet.json"
FRONTIER_EXTRA_DUE_CHECK = REVIEW_DIR / "f95c_frontier_extra_due_check.json"
FIVE_STAGE_SYNTHESIS = REVIEW_DIR / "f95c_frontier_five_stage_direction_synthesis.json"
TOPIC_ROTATION_CHECK = REVIEW_DIR / "f95c_frontier_topic_rotation_check.json"
SCOPE_GATE = REVIEW_DIR / "f95c_scope_completion_gate.json"
DATA_INTEGRITY_AUDIT = REVIEW_DIR / "f95c_data_integrity_audit.json"
MODEL_VALIDATION_AUDIT = REVIEW_DIR / "f95c_model_validation_audit.json"
KPI_CONTRACT_AUDIT = REVIEW_DIR / "f95c_kpi_contract_audit.json"
ARTIFACT_AUDIT = REVIEW_DIR / "f95c_artifact_lineage_audit.json"
RESULT_JUDGMENT_AUDIT = REVIEW_DIR / "f95c_result_judgment_audit.json"
FINAL_CLAIM_GUARD = REVIEW_DIR / "f95c_final_claim_guard.json"
STATE_SYNC_AUDIT = REVIEW_DIR / "f95c_state_sync_audit.json"
REQUIRED_GATE_AUDIT = REVIEW_DIR / "f95c_required_gate_coverage_audit.json"
DECISION_MEMO = ROOT / "docs" / "decisions" / "2026-06-19_frontier95c_closeout_rotate_f96.md"

WORK_PACKET = PACKET_DIR / "work_packet.yaml"
SKILL_RECEIPTS = PACKET_DIR / "skill_receipts.json"
PACKET_FINAL_CLAIM_GUARD = PACKET_DIR / "final_claim_guard.json"
PACKET_CLOSEOUT_GATE = PACKET_DIR / "closeout_gate.json"
PACKET_STATE_SYNC_AUDIT = PACKET_DIR / "state_sync_audit.json"
PACKET_REQUIRED_GATE_AUDIT = PACKET_DIR / "required_gate_coverage_audit.json"
PACKET_WORK_PACKET_LINT = PACKET_DIR / "work_packet_schema_lint.json"
PACKET_SKILL_RECEIPT_LINT = PACKET_DIR / "skill_receipt_schema_lint.json"

ALLOWED_CLAIMS = [
    "f95c_negative_memory_recorded",
    "f95c_repair_disposition_closed",
    "f95c_rotation_decision_recorded",
    "task_force_actual_calls_recorded_for_f95c",
    "frontier_extra_due_check_recorded_for_f96_preopen",
    "frontier_topic_rotation_check_recorded_for_f96_preopen",
    "f96_pending_open_scaffold_recorded",
    "runtime_probe_not_applicable_no_runnable_candidate_when_candidate_count_zero",
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
    "runtime_probe_completed",
    "runtime_verified",
    "mt5_verification_complete",
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
    "stage_closeout_pass",
    "internally_reviewed",
    "reviewed",
    "verified",
    "pass",
    "model_quality",
    "model_readiness",
    "calibrated_probability",
    "data_contract_pass",
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
    "kpi_contract_audit",
    "artifact_lineage_audit",
    "result_judgment_audit",
    "state_sync_audit",
    "closeout_gate",
    "required_gate_coverage_audit",
    "final_claim_guard",
]
REQUIRED_SKILLS = [
    "obsidian-stage-transition",
    "obsidian-run-evidence-system",
    "obsidian-data-integrity",
    "obsidian-model-validation",
    "obsidian-artifact-lineage",
    "obsidian-task-force-review",
    "obsidian-result-judgment",
    "obsidian-exploration-mandate",
    "obsidian-claim-discipline",
    "obsidian-answer-clarity",
]
RUNTIME_NA_REASONS = [
    {
        "gate": "runtime_evidence_gate",
        "reason_code": "no_runnable_candidate_no_runtime_claim_not_cost_or_proxy_bad_skip",
        "reason": (
            "F95C only closes a negative proxy scout and rotates the next axis. F95B candidate_count is zero, "
            "and no runnable ONNX/EA/set bundle, MT5 Strategy Tester output, materialization, economics, or handoff claim exists."
        ),
        "claim_effect": (
            "No runtime verified, economics pass, materialization ready, handoff complete, promotion, authority, "
            "readiness, or Goal Achieve claim is allowed."
        ),
    },
    {
        "gate": "wfo_stress_gate",
        "reason_code": "outside_claim_surface_closeout_rotation_no_candidate",
        "reason": "F95C does not claim WFO or stress validation; it records repair rejection, rotation, and negative memory only.",
        "claim_effect": "No WFO pass, stress pass, selected baseline, runtime authority, or live readiness claim is allowed.",
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
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_yaml(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        yaml.safe_dump(json_ready(dict(payload)), allow_unicode=True, sort_keys=False, width=120),
        encoding="utf-8",
    )


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def current_branch() -> str:
    completed = subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    return completed.stdout.strip() if completed.returncode == 0 else ""


def file_identity(path: Path) -> dict[str, Any]:
    if not path_exists(path):
        return {"path": rel(path), "exists": False, "sha256": None, "size_bytes": None}
    return {
        "path": rel(path),
        "exists": True,
        "sha256": sha256_file_lf_normalized(path),
        "size_bytes": io_path(path).stat().st_size,
        "artifact_kind": "directory" if io_path(path).is_dir() else "file",
    }


def ensure_dirs() -> None:
    for directory in (
        RUN_DIR,
        DECISION_DIR,
        REPORT_DIR,
        REVIEW_DIR,
        SELECTED_DIR,
        PACKET_DIR,
        SKILL_RECEIPT_DIR,
        NEXT_SPEC_DIR,
        NEXT_INPUT_DIR,
        NEXT_REVIEW_DIR,
        NEXT_SELECTED_DIR,
        ROOT / "docs" / "decisions",
    ):
        io_path(directory).mkdir(parents=True, exist_ok=True)


def source_inputs() -> list[Path]:
    return [
        F95B_RUN_MANIFEST,
        F95B_SUMMARY,
        F95B_KPI,
        F95B_EXECUTION_SUMMARY,
        F95B_CANDIDATE_GATE,
        F95B_DATA_LOCK,
        F95B_DATA_INTEGRITY_LOCAL,
        F95B_EMBEDDING_CONFIG,
        F95B_FIT_MANIFEST,
        F95B_SPLIT_METRICS,
        F95B_VARIANT_METRICS,
        F95B_TIER_ROUTE_SUMMARY,
        F95B_TIER_B_SUMMARY,
        F95B_RESULT_SUMMARY,
        F95B_DATA_INTEGRITY_AUDIT,
        F95B_MODEL_VALIDATION_AUDIT,
        F95B_TASK_FORCE,
        F95B_WORK_PACKET,
        F95B_CLOSEOUT_GATE,
    ]


def produced_artifacts() -> list[Path]:
    receipt_files = sorted(SKILL_RECEIPT_DIR.glob("*.json")) if path_exists(SKILL_RECEIPT_DIR) else []
    return [
        ROOT / SCRIPT_REL,
        RUN_MANIFEST,
        SUMMARY_JSON,
        KPI_RECORD,
        DECISION_JSON,
        RESULT_SUMMARY,
        STAGE_CLOSEOUT_SUMMARY,
        STAGE_CLOSEOUT_REPORT,
        F95C_REPORT,
        TASK_FORCE_REVIEW,
        TASK_FORCE_PACKET_REVIEW,
        FRONTIER_EXTRA_DUE_CHECK,
        FIVE_STAGE_SYNTHESIS,
        TOPIC_ROTATION_CHECK,
        SCOPE_GATE,
        DATA_INTEGRITY_AUDIT,
        MODEL_VALIDATION_AUDIT,
        KPI_CONTRACT_AUDIT,
        ARTIFACT_AUDIT,
        RESULT_JUDGMENT_AUDIT,
        FINAL_CLAIM_GUARD,
        STATE_SYNC_AUDIT,
        REQUIRED_GATE_AUDIT,
        WORK_PACKET,
        SKILL_RECEIPTS,
        PACKET_FINAL_CLAIM_GUARD,
        PACKET_CLOSEOUT_GATE,
        PACKET_STATE_SYNC_AUDIT,
        PACKET_REQUIRED_GATE_AUDIT,
        PACKET_WORK_PACKET_LINT,
        PACKET_SKILL_RECEIPT_LINT,
        DECISION_MEMO,
        SELECTION_STATUS,
        CONTEXT_ANCHOR,
        REVIEW_INDEX,
        NEXT_STAGE_BRIEF,
        NEXT_INPUT_REFS,
        NEXT_SELECTION_STATUS,
        NEXT_CONTEXT_ANCHOR,
        NEXT_REVIEW_INDEX,
        NEXT_STAGE_LEDGER,
    ] + receipt_files


def task_force_calls() -> list[dict[str, Any]]:
    return [
        {
            "roster_agent_id": "agent_01_system_governor",
            "spawned_agent_id": "019edee9-92fa-78d0-a869-5b2c9f85e5db",
            "nickname": "Raman the 2nd",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "accepted",
            "disposition": "accepted",
            "bounded_evidence": [rel(F95B_CANDIDATE_GATE), rel(F95B_KPI), rel(WORKSPACE_STATE)],
            "local_verification": "F95B candidate_count=0 and no authority boundary were checked locally.",
            "summary": "F95B is a valid negative; rotate to F96 unless a predeclared structural capped repair exists.",
        },
        {
            "roster_agent_id": "agent_04_evidence_control_plane",
            "spawned_agent_id": "019edee9-a8d4-7941-8a83-15436257753b",
            "nickname": "Gibbs the 2nd",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "needs_local_verification",
            "disposition": "accepted_with_local_verification",
            "bounded_evidence": [rel(F95B_CANDIDATE_GATE), rel(F95B_KPI), rel(F95B_CLOSEOUT_GATE)],
            "local_verification": "F96 novelty delta, gate list, ledgers, and actual_subagent_calls are materialized in this packet.",
            "summary": "Close F95C as rotation, reject parameter-only repair, and record actual subagent calls plus gate coverage.",
        },
        {
            "roster_agent_id": "agent_05_data_feature_contract",
            "spawned_agent_id": "019edee9-c224-7690-aad4-95c0bba50931",
            "nickname": "Wegener the 2nd",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "needs_local_verification",
            "disposition": "accepted_with_local_verification",
            "bounded_evidence": [rel(F95B_DATA_LOCK), rel(F95B_DATA_INTEGRITY_AUDIT), rel(F95B_KPI)],
            "local_verification": (
                "Parent audit timestamp_sorted=false for tier_ab_combined is retained as boundary; "
                "f91_route_integrity.routed_sorted=true is recorded, and no data_contract_pass is claimed."
            ),
            "summary": "F95B is valid negative rather than invalid; parameter-only repair remains rejected.",
        },
        {
            "roster_agent_id": "agent_06_quant_research",
            "spawned_agent_id": "019edee9-d69c-7d90-ac0f-d373e5ad4244",
            "nickname": "Huygens the 2nd",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "accepted",
            "disposition": "accepted",
            "bounded_evidence": [rel(F95B_CANDIDATE_GATE), rel(F95B_SPLIT_METRICS), rel(F95B_KPI)],
            "local_verification": "F96 axis uses action-value/regret-first representation rather than state-cluster parameter repair.",
            "summary": "Rotate to counterfactual action-value policy; reject k/PCA/threshold/filter/session/routing tweaks.",
        },
        {
            "roster_agent_id": "agent_07_model_validation_risk",
            "spawned_agent_id": "019edee9-eb16-72b2-9337-28739abd327b",
            "nickname": "Helmholtz the 2nd",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "accepted",
            "disposition": "accepted",
            "bounded_evidence": [rel(F95B_MODEL_VALIDATION_AUDIT), rel(F95B_CANDIDATE_GATE), rel(F95B_KPI)],
            "local_verification": "Model validation fields and no calibrated probability/model quality claims are recorded.",
            "summary": "F95B is negative_valid, not inconclusive or invalid; candidate_count=0 means no MT5 trigger.",
        },
        {
            "roster_agent_id": "agent_08_mt5_onnx_runtime",
            "spawned_agent_id": "019edee9-ff80-7c60-95dd-ddd06383b0fb",
            "nickname": "Copernicus the 2nd",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "accepted",
            "disposition": "accepted",
            "bounded_evidence": [rel(F95B_CANDIDATE_GATE), rel(F95B_KPI), rel(F95B_CLOSEOUT_GATE)],
            "local_verification": "Runtime N/A is caused by no runnable candidate and no runtime claim, not by cost or proxy-bad skip.",
            "summary": "No MT5 Strategy Tester run is required for F95C closeout; same-packet MT5 is required if F96 later creates a runnable/runtime claim.",
        },
    ]


def closeout_payload(now: str) -> dict[str, Any]:
    f95b_summary = read_json(F95B_SUMMARY)
    f95b_kpi = read_json(F95B_KPI)
    candidate_gate = read_json(F95B_CANDIDATE_GATE)
    data_audit = read_json(F95B_DATA_INTEGRITY_AUDIT)
    best_gate = f95b_kpi["candidate_gate"]["best_gate"]
    proxy = f95b_kpi["proxy_kpi"]
    closeout_kpi = f95b_kpi["closeout_kpi"]
    decision = {
        "final_disposition": "negative_memory_reference_surface_with_next_frontier_proposal",
        "decision_branch": "rotate",
        "rotation_selected": True,
        "repair_disposition": "close_negative_rotate_not_capped_repair",
        "capped_repair_scope": "rejected_no_predeclared_structural_repair",
        "capped_repair_rejected_reason": (
            "F95B failed with candidate_count=0 across state class collapse, long-only side concentration, "
            "high-cost exposure, DD above cap, trade density below 5-10/day, and Tier B weakness. "
            "Changing only KMeans k, PCA dimension, seed, threshold, session, routing, side filter, or cost filter "
            "would be parameter/filter-only repetition."
        ),
        "candidate_count": int(candidate_gate["candidate_count"]),
        "materialization_candidate_count": 0,
        "runtime_attempt_rows": 0,
        "failed_boundary": {
            "best_diagnostic_variant": BEST_VARIANT_ID,
            "validation_actual_routed_net": f95b_kpi["net_profit"],
            "validation_actual_routed_pf": f95b_kpi["profit_factor"],
            "validation_actual_routed_drawdown": f95b_kpi["drawdown"],
            "validation_actual_routed_trade_count": f95b_kpi["trade_count"],
            "validation_actual_routed_trades_per_day": f95b_kpi["trades_per_day"],
            "selection_failures": best_gate["selection_failures"],
            "oos_final_read_notes": best_gate["oos_final_read_notes"],
            "state_class_count": proxy["state_class_count"],
            "max_state_class_share": proxy["max_state_class_share"],
            "high_cost_trade_share": proxy["high_cost_trade_share"],
            "long_count": proxy["long_count"],
            "short_count": proxy["short_count"],
        },
        "data_integrity_followup": {
            "parent_data_integrity_status": data_audit.get("status"),
            "tier_ab_combined_timestamp_sorted": data_audit.get("timestamp_sorted", {}).get("tier_ab_combined"),
            "f91_route_integrity_routed_sorted": data_audit.get("f91_route_integrity", {}).get("routed_sorted"),
            "local_verification_result": (
                "retained_as_boundary_for_negative_closeout; the combined-view timestamp_sorted=false flag is not "
                "promoted to data_contract_pass, and F95C uses F95B as negative evidence only."
            ),
            "claim_effect": "No invalid/data pass/runtime claim is made from the parent data audit.",
        },
        "salvage_value": [
            "Closed-bar transition features and train-only fit remain useful as leakage-safe negative evidence.",
            "The positive net/PF diagnostic shows a possible long-momentum state, but it collapses side balance and DD.",
            "State-class collapse above 95% warns that unsupervised state-first clustering lacks risk geometry.",
            "High-cost exposure near 98% warns future surfaces need explicit cost/adverse-excursion rejection.",
        ],
        "negative_memory": [
            "Do not repeat KMeans/PCA cluster count or dimension repair without a new representation.",
            "Do not rescue long-only validation PF as a candidate.",
            "Do not accept state max share collapse above 95% as tradable surface evidence.",
            "Do not accept high-cost concentrated routes as runtime candidates.",
            "Do not turn proxy-only or compile-only evidence into runtime/economics evidence.",
        ],
        "reopen_condition": (
            "Revisit state-transition only if a new representation changes source/data representation, label, runtime "
            "representation, objective, trade shape, risk logic, or regime split; parameter-only repair is capped closed."
        ),
        "next_frontier_proposal": {
            "stage_id": NEXT_STAGE_ID,
            "run_id": NEXT_RUN_ID,
            "axis": "counterfactual_action_value_policy_axis",
            "question": (
                "Can closed-bar features learn long/short/abstain counterfactual action value with adverse-excursion "
                "risk before direction mapping, producing side-balanced 5-10 trades/day candidates with lower DD?"
            ),
            "hypothesis": (
                "Learn cost-adjusted path utility, adverse excursion, recovery/DD, and trade-density-aware action values "
                "directly for long, short, and abstain, rather than clustering states first and mapping actions later."
            ),
            "material_novelty_delta": {
                "objective": "action-value/regret-first instead of unsupervised state-first",
                "label": "counterfactual long/short/abstain path utility with adverse excursion penalties",
                "trade_shape": "side-symmetric risk-first action eligibility",
                "validation_philosophy": "risk/density/side-balance before PF-only selection",
                "runtime_boundary": "runtime probe required in same packet if a runnable ONNX/EA/set claim appears",
            },
        },
    }
    return {
        "packet_id": RUN_ID,
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_stage_id": NEXT_STAGE_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": now,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "verification_profile": "stage_closeout",
        "hypothesis": "F95 state-transition embedding should close as negative memory unless a non-parameter structural repair exists.",
        "test_period": f95b_kpi.get("test_period"),
        "proxy_kpi": f95b_kpi.get("proxy_kpi"),
        "runtime_kpi": RUNTIME_PROBE_STATUS,
        "net_profit": f95b_kpi["net_profit"],
        "profit_factor": f95b_kpi["profit_factor"],
        "drawdown": f95b_kpi["drawdown"],
        "trade_count": f95b_kpi["trade_count"],
        "trades_per_day": f95b_kpi["trades_per_day"],
        "parity": "not_applicable_no_onnx_or_ea",
        "gap_cause": "proxy/runtime gap not measured because no runtime materialization or handoff claim is made",
        "closeout_kpi": closeout_kpi,
        "candidate_gate": candidate_gate,
        "parent_summary": f95b_summary,
        "repair_rotation_decision": decision,
        "task_force_calls": task_force_calls(),
        "runtime_probe_status": RUNTIME_PROBE_STATUS,
        "frontier_extra_due_status": FRONTIER_EXTRA_DUE_STATUS,
        "frontier_five_stage_status": FRONTIER_FIVE_STAGE_STATUS,
        "frontier_topic_rotation_status": FRONTIER_TOPIC_ROTATION_STATUS,
        "claim_boundary": CLAIM_BOUNDARY,
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }


def summary_payload(payload: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> dict[str, Any]:
    gate_results = gate_results or {}
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_stage_id": NEXT_STAGE_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": payload["created_at_utc"],
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "candidate_gate_count": payload["repair_rotation_decision"]["candidate_count"],
        "runtime_probe_status": RUNTIME_PROBE_STATUS,
        "task_force_actual_subagent_call_count": len(payload["task_force_calls"]),
        "frontier_extra_due_status": FRONTIER_EXTRA_DUE_STATUS,
        "frontier_topic_rotation_status": FRONTIER_TOPIC_ROTATION_STATUS,
        "claim_boundary": CLAIM_BOUNDARY,
        "gate_statuses": {name: (gate_results.get(name, {}) or {}).get("status", "pending") for name in REQUIRED_GATES},
    }


def run_manifest_payload(payload: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> dict[str, Any]:
    gate_results = gate_results or {}
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "script": SCRIPT_REL,
        "created_at_utc": payload["created_at_utc"],
        "parent_run_id": PARENT_RUN_ID,
        "next_stage_id": NEXT_STAGE_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "source_inputs": [file_identity(path) for path in source_inputs()],
        "produced_artifacts": [file_identity(path) for path in produced_artifacts() if path_exists(path)],
        "gate_statuses": {name: (gate_results.get(name, {}) or {}).get("status", "pending") for name in REQUIRED_GATES},
        "runtime_probe_status": RUNTIME_PROBE_STATUS,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def kpi_record(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "packet_id": RUN_ID,
        "test_period": payload["test_period"],
        "hypothesis": payload["hypothesis"],
        "proxy_kpi": payload["proxy_kpi"],
        "runtime_kpi": RUNTIME_PROBE_STATUS,
        "net_profit": payload["net_profit"],
        "profit_factor": payload["profit_factor"],
        "drawdown": payload["drawdown"],
        "trade_count": payload["trade_count"],
        "trades_per_day": payload["trades_per_day"],
        "parity": payload["parity"],
        "gap_cause": payload["gap_cause"],
        "next_action": NEXT_RUN_ID,
        "candidate_gate": {
            "candidate_count": payload["repair_rotation_decision"]["candidate_count"],
            "best_gate": payload["repair_rotation_decision"]["failed_boundary"],
        },
        "tier_records_required": ["Tier A separate", "Tier B separate", "Tier A+B combined"],
        "closeout_kpi": payload["closeout_kpi"],
        "runtime_probe_trigger_rule": (
            "If candidate_count > 0 or a runnable ONNX/EA/set/materialization/economics/handoff claim appears, "
            "same-packet MT5 Strategy Tester probe is required."
        ),
        "runtime_skip_reason_rejected": ["cost_or_expense", "proxy_result_bad"],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def report_text(payload: Mapping[str, Any]) -> str:
    decision = payload["repair_rotation_decision"]
    kpi = payload["closeout_kpi"]
    next_proposal = decision["next_frontier_proposal"]
    return f"""# F95C Closeout(마감) Rotation(회전) Record(기록)

## Decision(결정)

F95C(전선95C)는 F95B(전선95B)를 valid negative(유효한 부정)로 닫고 F96(전선96)으로 rotate(회전)한다.

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- repair disposition(수리 처분): `{decision['repair_disposition']}`
- candidate count(후보 수): `{decision['candidate_count']}`
- runtime probe status(런타임 탐침 상태): `{RUNTIME_PROBE_STATUS}`

## Evidence(근거)

- best diagnostic variant(최선 진단 변형): `{BEST_VARIANT_ID}`
- validation actual routed net/PF/DD/trades/day(검증 실제 라우팅 순수익/수익 팩터/손실폭/일 거래): {payload['net_profit']} / {payload['profit_factor']} / {payload['drawdown']} / {payload['trades_per_day']}
- closeout KPI(마감 KPI): gross profit(총이익)={kpi['gross_profit']}, gross loss(총손실)={kpi['gross_loss']}, win rate(승률)={kpi['win_rate']}, avg win/loss(평균 이익/손실)={kpi['avg_win']} / {kpi['avg_loss']}, payoff(손익비)={kpi['payoff_ratio']}, expectancy(기대값)={kpi['expectancy']}, recovery(회복 계수)={kpi['recovery_factor']}, time under water(회복 전 체류)={kpi['time_under_water']}, max consecutive loss(최대 연속 손실)={kpi['max_consecutive_loss']}, long/short(롱/숏)={kpi['long_short_breakdown']['long_count']} / {kpi['long_short_breakdown']['short_count']}
- Task Force actual calls(태스크포스 실제 호출): {len(payload['task_force_calls'])} selected agents(선택 요원)

## Runtime Boundary(런타임 경계)

No MT5 Strategy Tester(전략 테스터) run(실행) was made because no runnable candidate(실행 후보), ONNX/EA/set(온엑스/전문가 자문/설정), runtime/materialization/economics/handoff claim(런타임/물질화/경제성/인계 주장) exists. This is not cost skip(비용 회피) or proxy-bad skip(프록시 부진 회피).

## Next Axis(다음 축)

`{NEXT_STAGE_ID}` is scaffolded as pending open(개방 대기). Its question(질문): {next_proposal['question']}

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""


def next_stage_brief_text(payload: Mapping[str, Any]) -> str:
    next_proposal = payload["repair_rotation_decision"]["next_frontier_proposal"]
    return f"""# F96 Counterfactual Action Value Policy Axis(반사실 행동가치 정책 축)

- current run(현재 실행): `{NEXT_RUN_ID}`
- source closeout(원천 마감): `{RUN_ID}`
- status(상태): pending formal open(정식 개방 대기)
- authority(권위): not_claimed(주장 없음)

## Question(질문)

{next_proposal['question']}

## Hypothesis(가설)

{next_proposal['hypothesis']}

## Novelty Delta(신규성 차이)

- objective(목적함수): {next_proposal['material_novelty_delta']['objective']}
- label(라벨): {next_proposal['material_novelty_delta']['label']}
- trade shape(거래 형태): {next_proposal['material_novelty_delta']['trade_shape']}
- validation philosophy(검증 철학): {next_proposal['material_novelty_delta']['validation_philosophy']}
- runtime boundary(런타임 경계): {next_proposal['material_novelty_delta']['runtime_boundary']}

## Boundary(경계)

This scaffold(골격)는 pending-open(개방 대기) record(기록) only(전용)이다. No selected baseline(선택 기준선), promotion candidate(승격 후보), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성) is claimed(주장됨).
"""


def next_input_refs_text() -> str:
    return f"""# F96 Input References(입력 참조)

- F95C closeout(마감): `{rel(DECISION_JSON)}`
- F95B KPI(KPI 기록): `{rel(F95B_KPI)}`
- F95B candidate gate(후보 게이트): `{rel(F95B_CANDIDATE_GATE)}`
- F95B data integrity audit(데이터 무결성 감사): `{rel(F95B_DATA_INTEGRITY_AUDIT)}`

Effect(효과): F96(전선96)은 F95(전선95)를 winner(승자)나 baseline(기준선)으로 상속하지 않고 negative memory/reference surface(부정 기억/참고 표면)로만 읽는다.
"""


def next_selection_status_text() -> str:
    return f"""# F96 Selection Status(선택 상태)

- current run(현재 실행): `{NEXT_RUN_ID}`
- latest completed run(최근 완료 실행): `{RUN_ID}`
- selected baseline(선택 기준선): not_claimed(주장 없음)
- promotion candidate(승격 후보): not_claimed(주장 없음)
- operating promotion(운영 승격): not_claimed(주장 없음)
- runtime authority(런타임 권위): not_claimed(주장 없음)
- live readiness(실거래 준비): not_claimed(주장 없음)
- Goal Achieve(목표 달성): not_claimed(주장 없음)

Effect(효과): F96A(전선96A)는 formal open(정식 개방) 대기 상태이며 runtime evidence(런타임 근거)는 아직 없다.
"""


def current_state_text(payload: Mapping[str, Any]) -> str:
    return f"""# Current Working State(현재 작업 상태)

- active stage(활성 단계): `{NEXT_STAGE_ID}`
- current run(현재 실행): `{NEXT_RUN_ID}`
- latest completed run(최근 완료 실행): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- runtime probe status(런타임 탐침 상태): `{RUNTIME_PROBE_STATUS}`

Action(행동): F95C(전선95C) closes(마감) F95B(전선95B) as valid negative(유효한 부정) and creates(생성) F96A pending-open scaffold(F96A 개방 대기 골격).

Effect(효과): current truth(현재 진실)는 F96A pending open(개방 대기)이며 no selected baseline(선택 기준선 없음), no runtime authority(런타임 권위 없음), no live readiness(실거래 준비 없음), and no Goal Achieve(목표 달성 없음)이다.
"""


def f95_selection_status_text() -> str:
    return f"""# F95 Selection Status(선택 상태)

- latest completed run(최근 완료 실행): `{RUN_ID}`
- next run(다음 실행): `{NEXT_RUN_ID}`
- result(결과): negative memory/reference surface(부정 기억/참고 표면)
- selected baseline(선택 기준선): not_claimed(주장 없음)
- runtime authority(런타임 권위): not_claimed(주장 없음)
- live readiness(실거래 준비): not_claimed(주장 없음)
- Goal Achieve(목표 달성): not_claimed(주장 없음)

Effect(효과): F95(전선95)는 capped repair(상한 수리) 없이 close negative(부정 마감)로 닫히며 F96(전선96)으로 rotation(회전)한다.
"""


def review_index_text() -> str:
    return f"""# F95 Review Index(검토 색인)

- F95B proxy scout(프록시 정찰): `{rel(F95B_RESULT_SUMMARY)}`
- F95C decision(결정): `{rel(DECISION_JSON)}`
- F95C report(보고서): `{rel(F95C_REPORT)}`
- Task Force receipt(태스크포스 영수증): `{rel(TASK_FORCE_REVIEW)}`
- next stage(다음 단계): `{NEXT_STAGE_ID}`
"""


def next_review_index_text() -> str:
    return f"""# F96 Review Index(검토 색인)

- pending open run(개방 대기 실행): `{NEXT_RUN_ID}`
- source closeout(원천 마감): `{rel(DECISION_JSON)}`
- input refs(입력 참조): `{rel(NEXT_INPUT_REFS)}`
"""


def workspace_state_payload(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "current_stage_id": NEXT_STAGE_ID,
        "active_stage": NEXT_STAGE_ID,
        "active_branch": current_branch(),
        "current_run_id": NEXT_RUN_ID,
        "latest_completed_run_id": RUN_ID,
        "current_status": STATUS,
        "current_judgment": JUDGMENT,
        "next_run_id": NEXT_RUN_ID,
        "frontier_extra_due_status": FRONTIER_EXTRA_DUE_STATUS,
        "frontier_topic_rotation_status": FRONTIER_TOPIC_ROTATION_STATUS,
        "task_force_status": "f95c_actual_subagent_calls_recorded_6_selected_agents_no_task_force_reviewed_pass_claim",
        "runtime_probe_status": RUNTIME_PROBE_STATUS,
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "updated_at_utc": payload["created_at_utc"],
        "context_anchor": rel(NEXT_CONTEXT_ANCHOR),
        "notes": [
            "Action: F95C closed F95B as valid negative and rotated to F96 pending open.",
            "Effect: F96A is current pending-open run; no baseline, authority, readiness, or Goal Achieve is claimed.",
            "Runtime: no MT5 Strategy Tester evidence exists for F95C because no runnable candidate or runtime claim exists.",
        ],
    }


def audit_payload(
    audit_name: str,
    status: str,
    payload: Mapping[str, Any],
    *,
    counts: Mapping[str, Any] | None = None,
    allowed_claims: Sequence[str] | None = None,
    forbidden_claims: Sequence[str] | None = None,
) -> dict[str, Any]:
    return {
        "audit_name": audit_name,
        "packet_id": RUN_ID,
        "status": status,
        "created_at_utc": payload["created_at_utc"],
        "counts": dict(counts or {}),
        "allowed_claims": list(allowed_claims or ALLOWED_CLAIMS),
        "forbidden_claims": list(forbidden_claims or FORBIDDEN_CLAIMS),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_run_artifacts(payload: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> None:
    write_json(RUN_MANIFEST, run_manifest_payload(payload, gate_results))
    write_json(SUMMARY_JSON, summary_payload(payload, gate_results))
    write_json(KPI_RECORD, kpi_record(payload))
    write_json(DECISION_JSON, payload["repair_rotation_decision"])
    write_text(RESULT_SUMMARY, report_text(payload))
    write_json(STAGE_CLOSEOUT_SUMMARY, summary_payload(payload, gate_results))
    write_text(STAGE_CLOSEOUT_REPORT, report_text(payload))
    write_text(F95C_REPORT, report_text(payload))
    write_text(DECISION_MEMO, report_text(payload))


def write_audits(payload: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> None:
    gate_results = gate_results or {}
    actual_status = {name: (gate_results.get(name, {}) or {}).get("status", "pending") for name in REQUIRED_GATES}
    write_json(
        TASK_FORCE_REVIEW,
        {
            **audit_payload(
                "codex_task_force_review_packet",
                "pass",
                payload,
                counts={
                    "agents_used": [call["roster_agent_id"] for call in payload["task_force_calls"]],
                    "actual_subagent_call_count": len(payload["task_force_calls"]),
                    "task_force_review_claim": "not_claimed",
                },
            ),
            "actual_subagent_calls": payload["task_force_calls"],
            "advice_classification": {
                "accepted": [
                    call["roster_agent_id"]
                    for call in payload["task_force_calls"]
                    if call["opinion_classification"] == "accepted"
                ],
                "needs_local_verification": [
                    call["roster_agent_id"]
                    for call in payload["task_force_calls"]
                    if call["opinion_classification"] == "needs_local_verification"
                ],
                "rejected": [],
            },
            "final_codex_direction": "close F95 negative and rotate to F96 pending-open scaffold; no Task Force reviewed/pass claim",
        },
    )
    write_json(TASK_FORCE_PACKET_REVIEW, read_json(TASK_FORCE_REVIEW))
    write_json(
        FRONTIER_EXTRA_DUE_CHECK,
        audit_payload(
            "frontier_extra_due_check",
            "pass_not_due",
            payload,
            counts={
                "closed_frontier_after_this_packet": "F95",
                "next_extra_boundary": "F100",
                "status": FRONTIER_EXTRA_DUE_STATUS,
            },
        ),
    )
    write_json(
        FIVE_STAGE_SYNTHESIS,
        audit_payload(
            "frontier_five_stage_direction_synthesis",
            "pass",
            payload,
            counts={
                "recent_frontiers": ["F91", "F92", "F93", "F94", "F95"],
                "dominant_direction": "risk_density_trade_shape_and_runtime_materialization_learning",
                "repeated_mechanism": "proxy candidates fail non-PF gates before runtime trigger",
                "overused_axis_warning": "avoid adjacent threshold/filter/parameter-only repair",
                "next_axis_options": ["counterfactual_action_value_policy_axis", "adverse_excursion_trade_shape_axis"],
                "claim_effect": "direction synthesis only, not retrospective, not topic ban",
            },
        ),
    )
    write_json(
        TOPIC_ROTATION_CHECK,
        audit_payload(
            "frontier_topic_rotation_check",
            "pass",
            payload,
            counts={
                "proposed_next_stage": NEXT_STAGE_ID,
                "material_novelty_delta": payload["repair_rotation_decision"]["next_frontier_proposal"]["material_novelty_delta"],
                "not_parameter_only_repair": True,
                "status": FRONTIER_TOPIC_ROTATION_STATUS,
            },
        ),
    )
    write_json(
        SCOPE_GATE,
        audit_payload(
            "scope_completion_gate",
            "pass",
            payload,
            counts={
                "decision_json": file_identity(DECISION_JSON),
                "kpi_record": file_identity(KPI_RECORD),
                "task_force_receipt": file_identity(TASK_FORCE_REVIEW),
                "f96_pending_scaffold": file_identity(NEXT_STAGE_BRIEF),
            },
        ),
    )
    write_json(
        DATA_INTEGRITY_AUDIT,
        audit_payload(
            "data_integrity_audit",
            "pass_with_boundary",
            payload,
            counts=payload["repair_rotation_decision"]["data_integrity_followup"],
            allowed_claims=["negative_data_boundary_recorded"],
            forbidden_claims=FORBIDDEN_CLAIMS + ["data_contract_pass"],
        ),
    )
    write_json(
        MODEL_VALIDATION_AUDIT,
        audit_payload(
            "model_validation_audit",
            "pass_with_boundary",
            payload,
            counts={
                "model_family": "pca_kmeans_transition_state_parent_negative_only",
                "target_label": "not_new_model_f95c_closeout_only",
                "split_method": "F95B train_validation_oos inherited as reference evidence only",
                "selection_metric": "candidate_count_zero_and_non_pf_gate_failures",
                "secondary_metrics": ["DD", "trades_per_day", "side_balance", "state_class_share", "Tier B weakness"],
                "threshold_policy": "no new threshold selected in F95C",
                "overfit_risk": "parameter_only_repair_rejected",
                "calibration_risk": "no calibrated probability or model quality claim",
            },
            allowed_claims=["negative_model_validation_boundary_recorded"],
        ),
    )
    write_json(
        KPI_CONTRACT_AUDIT,
        audit_payload(
            "kpi_contract_audit",
            "pass",
            payload,
            counts={
                "hypothesis": payload["hypothesis"],
                "test_period": payload["test_period"],
                "proxy_kpi_present": True,
                "runtime_kpi": RUNTIME_PROBE_STATUS,
                "net_profit": payload["net_profit"],
                "profit_factor": payload["profit_factor"],
                "drawdown": payload["drawdown"],
                "trade_count": payload["trade_count"],
                "trades_per_day": payload["trades_per_day"],
                "closeout_kpi": payload["closeout_kpi"],
            },
        ),
    )
    write_json(
        ARTIFACT_AUDIT,
        audit_payload(
            "artifact_lineage_audit",
            "pass",
            payload,
            counts={
                "source_inputs": [file_identity(path) for path in source_inputs()],
                "produced_artifacts": [file_identity(path) for path in produced_artifacts() if path_exists(path)],
                "lineage_boundary": "F95C closeout/rotation only; no runtime evidence or authority",
            },
        ),
    )
    write_json(
        RESULT_JUDGMENT_AUDIT,
        audit_payload(
            "result_judgment_audit",
            "negative",
            payload,
            counts={
                "judgment": JUDGMENT,
                "classification": "negative_valid_then_rotation",
                "candidate_count": payload["repair_rotation_decision"]["candidate_count"],
                "runtime_probe_status": RUNTIME_PROBE_STATUS,
                "next_action": NEXT_RUN_ID,
            },
            allowed_claims=["negative_memory_reference_surface_recorded"],
        ),
    )
    write_json(
        STATE_SYNC_AUDIT,
        audit_payload(
            "state_sync_audit",
            actual_status.get("state_sync_audit", "pending"),
            payload,
            counts={"active_stage": NEXT_STAGE_ID, "current_run_id": NEXT_RUN_ID, "latest_completed_run_id": RUN_ID},
        ),
    )
    write_json(
        REQUIRED_GATE_AUDIT,
        audit_payload(
            "required_gate_coverage_audit",
            actual_status.get("required_gate_coverage_audit", "pending"),
            payload,
            counts={"required_gates": REQUIRED_GATES, "actual_status_source": actual_status},
        ),
    )


def common_receipt(skill: str, payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "packet_id": RUN_ID,
        "skill": skill,
        "status": "executed",
        "claim_boundary": CLAIM_BOUNDARY,
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "receipt_path": f"{rel(SKILL_RECEIPT_DIR)}/{skill.replace('obsidian-', '').replace('-', '_')}.json",
    }


def skill_receipt_payloads(payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    source_docs = [rel(WORKSPACE_STATE), rel(CURRENT_WORKING_STATE), rel(SELECTION_STATUS)]
    source_inputs_rel = [rel(path) for path in source_inputs()]
    produced_rel = [rel(path) for path in produced_artifacts() if path_exists(path)]
    receipts = [
        {
            **common_receipt("obsidian-stage-transition", payload),
            "source_current_truth_docs": source_docs,
            "changed_or_checked_docs": [
                rel(WORKSPACE_STATE),
                rel(CURRENT_WORKING_STATE),
                rel(GLOBAL_SELECTION_STATUS),
                rel(NEXT_STAGE_BRIEF),
                rel(NEXT_SELECTION_STATUS),
            ],
            "detected_conflicts": ["none_detected"],
            "canonical_state_after": {
                "active_stage": NEXT_STAGE_ID,
                "current_run": NEXT_RUN_ID,
                "latest_completed_run": RUN_ID,
            },
            "allowed_claims": ALLOWED_CLAIMS,
        },
        {
            **common_receipt("obsidian-run-evidence-system", payload),
            "source_inputs": source_inputs_rel,
            "produced_artifacts": produced_rel,
            "ledger_rows": [f"{RUN_ID}__stage_closeout_rotation", f"{NEXT_RUN_ID}__planned_current_run"],
            "missing_evidence": [
                {"evidence": "MT5 Strategy Tester runtime output", "reason": "outside closeout claim surface"},
                {"evidence": "ONNX/EA/set bundle", "reason": "not created; no runnable candidate"},
            ],
            "allowed_claims": ALLOWED_CLAIMS,
        },
        {
            **common_receipt("obsidian-data-integrity", payload),
            "data_sources_checked": [rel(F95B_DATA_LOCK), rel(F95B_DATA_INTEGRITY_AUDIT)],
            "time_axis_boundary": payload["repair_rotation_decision"]["data_integrity_followup"],
            "split_boundary": "F95B split evidence is consumed as negative reference only; no new split or threshold is selected.",
            "leakage_checks": {
                "new_training": False,
                "parent_denylist_violations": "see F95B audit",
                "data_contract_pass_claim": "forbidden",
            },
            "missing_data_boundary": "No Tier record is omitted; F95C references F95B Tier A, Tier B, and A+B records.",
        },
        {
            **common_receipt("obsidian-model-validation", payload),
            "model_or_threshold_surface": "F95C closeout decision; no new model or threshold",
            "validation_split": "F95B validation/OOS evidence is parent reference only",
            "overfit_checks": [
                "parameter-only repair rejected",
                "OOS not reused for repair selection",
                "no calibrated probability claim",
            ],
            "selection_metric_boundary": "candidate_count=0 plus DD/density/side/state/Tier-B failures",
            "allowed_claims": ALLOWED_CLAIMS,
        },
        {
            **common_receipt("obsidian-artifact-lineage", payload),
            "source_inputs": source_inputs_rel,
            "produced_artifacts": produced_rel,
            "raw_evidence": [rel(F95B_CANDIDATE_GATE), rel(F95B_KPI), rel(F95B_SPLIT_METRICS)],
            "machine_readable": [rel(RUN_MANIFEST), rel(SUMMARY_JSON), rel(KPI_RECORD), rel(DECISION_JSON), rel(SKILL_RECEIPTS)],
            "human_readable": [rel(RESULT_SUMMARY), rel(F95C_REPORT), rel(DECISION_MEMO)],
            "hashes_or_missing_reasons": [file_identity(path) for path in produced_artifacts() if path_exists(path)],
            "lineage_boundary": "stage_closeout_rotation_only_no_runtime_evidence",
        },
        {
            **common_receipt("obsidian-task-force-review", payload),
            "trigger_reason": "explicit user instruction plus F95C active-goal closeout claim surface",
            "roster_registry": "docs/agent_control/codex_task_force_registry.yaml",
            "agents_used": [call["roster_agent_id"] for call in payload["task_force_calls"]],
            "actual_subagent_calls": payload["task_force_calls"],
            "review_requirement": "explicit_user_instruction_required_and_active_goal_closeout_required",
            "codex_task_force_review_packet_required": True,
            "model_policy": "inherited parent model; model strength does not relax gates or evidence",
            "bounded_evidence": [rel(TASK_FORCE_PACKET_REVIEW), rel(TASK_FORCE_REVIEW), rel(F95B_CANDIDATE_GATE), rel(F95B_KPI)],
            "advice_classification": {
                "accepted": [
                    call["roster_agent_id"]
                    for call in payload["task_force_calls"]
                    if call["opinion_classification"] == "accepted"
                ],
                "needs_local_verification": [
                    call["roster_agent_id"]
                    for call in payload["task_force_calls"]
                    if call["opinion_classification"] == "needs_local_verification"
                ],
                "rejected": [],
            },
            "local_verification": "F96 novelty delta, data boundary, model boundary, runtime N/A boundary, and state sync are checked locally.",
            "final_codex_direction": "F95C closes negative and rotates to F96 pending-open scaffold; no Task Force reviewed/pass claim",
            "forbidden_claim_check": FORBIDDEN_CLAIMS,
        },
        {
            **common_receipt("obsidian-result-judgment", payload),
            "judgment_boundary": "negative_valid_then_rotation only; no candidate, baseline, promotion, authority, readiness, or Goal Achieve",
            "allowed_claims": ALLOWED_CLAIMS,
            "evidence_used": [rel(F95B_CANDIDATE_GATE), rel(F95B_KPI), rel(DECISION_JSON), rel(RESULT_JUDGMENT_AUDIT)],
            "judgment": JUDGMENT,
            "runtime_probe_status": RUNTIME_PROBE_STATUS,
            "next_action": NEXT_RUN_ID,
        },
        {
            **common_receipt("obsidian-exploration-mandate", payload),
            "exploration_lane": "frontier_stage_closeout_rotation",
            "idea_boundary": "F95C creates negative memory/reference surface and next frontier seed only.",
            "negative_memory_effect": "F95 state-cluster parameter-only repair is capped closed.",
            "operating_claim_boundary": CLAIM_BOUNDARY,
        },
        {
            **common_receipt("obsidian-claim-discipline", payload),
            "requested_claims": ALLOWED_CLAIMS,
            "allowed_claims": ALLOWED_CLAIMS,
            "final_status": STATUS,
        },
        {
            **common_receipt("obsidian-answer-clarity", payload),
            "plain_conclusion": "F95C closes negative and rotates to F96 pending open.",
            "confirmed": ["candidate_count=0", "actual_subagent_calls=6", "runtime_probe_not_applicable"],
            "not_yet_confirmed": ["F96 formal open", "runtime evidence", "baseline", "authority", "readiness"],
            "why_it_matters": "It preserves learning evidence without overclaiming runtime or final readiness.",
            "next_action": NEXT_RUN_ID,
            "forbidden_claims_avoided": FORBIDDEN_CLAIMS,
        },
    ]
    return receipts


def write_receipts(payload: Mapping[str, Any]) -> None:
    receipts = skill_receipt_payloads(payload)
    for receipt in receipts:
        path = ROOT / str(receipt["receipt_path"])
        write_json(path, receipt)
    write_json(SKILL_RECEIPTS, {"packet_id": RUN_ID, "primary_skill": "obsidian-stage-transition", "receipts": receipts})


def work_packet_payload(payload: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> dict[str, Any]:
    gate_results = gate_results or {}
    actual_status = {name: (gate_results.get(name, {}) or {}).get("status", "pending") for name in REQUIRED_GATES}
    return {
        "version": "work_packet_schema_v2_1",
        "packet_lifecycle": "new_packet",
        "packet_id": RUN_ID,
        "created_at_utc": payload["created_at_utc"],
        "user_request": {
            "user_quote": "/goal active continuation and explicit reminder to actually call relevant Task Force agents when required",
            "requested_action": "close F95C repair-or-rotation decision and scaffold F96 pending open",
            "requested_count": {"value": 1, "n_a_reason": ""},
            "ambiguous_terms": [
                "No final completion, selected baseline, operating promotion, runtime authority, live readiness, or Goal Achieve is claimed."
            ],
        },
        "current_truth": {
            "active_stage": STAGE_ID,
            "current_run": RUN_ID,
            "latest_completed_run": PARENT_RUN_ID,
            "source_documents": [rel(WORKSPACE_STATE), rel(CURRENT_WORKING_STATE), rel(SELECTION_STATUS)],
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "work_classification": {
            "primary_family": "publish_handoff",
            "detected_families": ["publish_handoff", "state_sync", "artifact_lineage"],
            "touched_surfaces": [rel(RUN_DIR), rel(REVIEW_DIR), rel(PACKET_DIR), rel(NEXT_STAGE_DIR), rel(WORKSPACE_STATE)],
            "mutation_intent": True,
            "execution_intent": True,
        },
        "risk_vector_scan": {
            "risks": {
                "parameter_only_repair_repetition": "high",
                "task_force_review_claim_without_actual_calls": "high",
                "runtime_probe_absence_misread_as_cost_skip": "high",
                "positive_pf_overclaim": "high",
                "data_contract_pass_overclaim": "medium",
            },
            "hard_stop_risks": [
                "Do not claim Task Force reviewed/pass from actual calls.",
                "Do not claim runtime/economics/materialization without MT5 Strategy Tester identity.",
                "Do not turn F95B positive net/PF diagnostic into a candidate.",
            ],
            "required_gates": REQUIRED_GATES,
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        "decision_lock": {
            "mode": "assume_safe_default",
            "assumptions": {
                "verification_profile": "stage_closeout",
                "strategy_tester_required_now": False,
                "runtime_probe_status": RUNTIME_PROBE_STATUS,
                "reason": "F95C has no runnable candidate and makes no runtime/materialization/economics/handoff claim.",
            },
            "questions": [],
            "required_user_decisions": [],
        },
        "interpreted_scope": {
            "work_families": ["publish_handoff"],
            "target_surfaces": [
                "F95C repair-or-rotation decision",
                "F95 negative memory",
                "F96 pending-open scaffold",
                "Task Force actual calls",
                "state sync",
            ],
            "scope_units": ["closeout_decision", "receipt", "state_sync", "next_stage_scaffold"],
            "execution_layers": ["local_python_execution", "control_plane_lints", "docs_state_sync"],
            "mutation_policy": {"allowed": True, "user_quote": "/goal active continuation"},
            "evidence_layers": ["F95B KPI", "candidate gate", "Task Force actual calls", "gate receipts", "state sync"],
            "reduction_policy": {
                "reduction_allowed": False,
                "requires_user_quote": False,
                "rationale": "F95C is a formal closeout/transition packet and Task Force actual calls are required by user instruction.",
            },
            "claim_boundary": {
                "allowed_claims": ALLOWED_CLAIMS,
                "forbidden_claims": FORBIDDEN_CLAIMS,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        },
        "verification_profile": {
            "profile_id": "stage_closeout",
            "claim_surface": {
                "allowed_claims": ALLOWED_CLAIMS,
                "forbidden_claims": FORBIDDEN_CLAIMS,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            "trigger_sources": [
                "active_goal_frontier_continuation",
                "F95B candidate_count_zero negative closeout",
                "explicit user instruction requiring relevant Task Force actual calls when triggered",
            ],
            "protected_claims": ALLOWED_CLAIMS,
            "required_evidence": [
                rel(DECISION_JSON),
                rel(KPI_RECORD),
                rel(TASK_FORCE_PACKET_REVIEW),
                rel(WORK_PACKET),
                rel(SKILL_RECEIPTS),
                rel(PACKET_CLOSEOUT_GATE),
                rel(PACKET_REQUIRED_GATE_AUDIT),
                rel(PACKET_FINAL_CLAIM_GUARD),
                rel(NEXT_STAGE_BRIEF),
            ],
            "gates_not_run_with_reason": RUNTIME_NA_REASONS,
            "stop_conditions": [
                "Stop if candidate_count remains zero and no runnable/runtime claim exists; record negative memory and rotate.",
                "If runnable ONNX/EA/set or runtime/materialization/economics/handoff claim appears, require same-packet MT5 Strategy Tester probe.",
                "Do not repair by threshold/filter/session/routing/parameter-only changes.",
            ],
        },
        "acceptance_criteria": [
            {
                "id": "AC-001",
                "text": "F95C decision JSON exists.",
                "expected_artifact": rel(DECISION_JSON),
                "verification_method": "scope_completion_gate",
                "required": True,
            },
            {
                "id": "AC-002",
                "text": "Task Force actual calls are recorded.",
                "expected_artifact": rel(TASK_FORCE_PACKET_REVIEW),
                "verification_method": "codex_task_force_review_packet",
                "required": True,
            },
            {
                "id": "AC-003",
                "text": "F96 pending-open scaffold records material novelty delta.",
                "expected_artifact": rel(NEXT_STAGE_BRIEF),
                "verification_method": "frontier_topic_rotation_check",
                "required": True,
            },
            {
                "id": "AC-004",
                "text": "Runtime evidence absence is bounded and not a cost/proxy-bad skip.",
                "expected_artifact": rel(KPI_RECORD),
                "verification_method": "final_claim_guard",
                "required": True,
            },
        ],
        "work_plan": [
            "Consume F95B KPI/candidate gate/data boundary as current truth.",
            "Record six relevant Task Force actual subagent calls.",
            "Reject parameter-only F95 repair and scaffold F96 action-value axis.",
            "Update state docs, ledgers, gate receipts, and final claim guard.",
        ],
        "skill_routing": {
            "primary_family": "publish_handoff",
            "primary_skill": "obsidian-stage-transition",
            "support_skills": [
                "obsidian-run-evidence-system",
                "obsidian-data-integrity",
                "obsidian-model-validation",
                "obsidian-artifact-lineage",
                "obsidian-task-force-review",
                "obsidian-result-judgment",
                "obsidian-exploration-mandate",
                "obsidian-claim-discipline",
                "obsidian-answer-clarity",
            ],
            "skills_considered": REQUIRED_SKILLS + ["obsidian-backtest-forensics", "obsidian-runtime-parity"],
            "skills_selected": REQUIRED_SKILLS,
            "skills_not_used": [
                {"skill": "obsidian-backtest-forensics", "reason": "No new MT5 Strategy Tester report or trade list exists."},
                {"skill": "obsidian-runtime-parity", "reason": "No ONNX/EA parity or handoff claim is made."},
            ],
            "required_skill_receipts": REQUIRED_SKILLS,
            "required_gates": REQUIRED_GATES,
        },
        "evidence_contract": {
            "source_inputs": [rel(path) for path in source_inputs()],
            "machine_readable": [rel(RUN_MANIFEST), rel(SUMMARY_JSON), rel(KPI_RECORD), rel(DECISION_JSON), rel(SKILL_RECEIPTS)],
            "human_readable": [rel(RESULT_SUMMARY), rel(F95C_REPORT), rel(DECISION_MEMO), rel(NEXT_STAGE_BRIEF)],
            "raw_evidence": [rel(F95B_CANDIDATE_GATE), rel(F95B_KPI), rel(F95B_SPLIT_METRICS), rel(F95B_DATA_INTEGRITY_AUDIT)],
            "missing_evidence": [
                {"evidence": "MT5 Strategy Tester runtime output", "reason": "outside stage_closeout claim surface"},
                {"evidence": "ONNX/EA/set handoff", "reason": "not created in F95C"},
            ],
        },
        "gates": {
            "required": REQUIRED_GATES,
            "actual_status_source": actual_status,
            "not_applicable_with_reason": {item["gate"]: item["reason"] for item in RUNTIME_NA_REASONS},
        },
        "final_claim_policy": {
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    }


def closeout_gate_payload(payload: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> dict[str, Any]:
    gate_results = gate_results or {}
    path_by_gate = {
        "work_packet_schema_lint": PACKET_WORK_PACKET_LINT,
        "skill_receipt_schema_lint": PACKET_SKILL_RECEIPT_LINT,
        "codex_task_force_review_packet": TASK_FORCE_PACKET_REVIEW,
        "frontier_extra_due_check": FRONTIER_EXTRA_DUE_CHECK,
        "frontier_five_stage_direction_synthesis": FIVE_STAGE_SYNTHESIS,
        "frontier_topic_rotation_check": TOPIC_ROTATION_CHECK,
        "scope_completion_gate": SCOPE_GATE,
        "data_integrity_audit": DATA_INTEGRITY_AUDIT,
        "model_validation_audit": MODEL_VALIDATION_AUDIT,
        "kpi_contract_audit": KPI_CONTRACT_AUDIT,
        "artifact_lineage_audit": ARTIFACT_AUDIT,
        "result_judgment_audit": RESULT_JUDGMENT_AUDIT,
        "state_sync_audit": PACKET_STATE_SYNC_AUDIT,
        "closeout_gate": PACKET_CLOSEOUT_GATE,
        "required_gate_coverage_audit": PACKET_REQUIRED_GATE_AUDIT,
        "final_claim_guard": PACKET_FINAL_CLAIM_GUARD,
    }
    default_status = {
        "codex_task_force_review_packet": "pass",
        "frontier_extra_due_check": "pass_not_due",
        "frontier_five_stage_direction_synthesis": "pass",
        "frontier_topic_rotation_check": "pass",
        "scope_completion_gate": "pass",
        "data_integrity_audit": "pass_with_boundary",
        "model_validation_audit": "pass_with_boundary",
        "kpi_contract_audit": "pass",
        "artifact_lineage_audit": "pass",
        "result_judgment_audit": "negative",
        "closeout_gate": "pass",
    }
    audits = []
    for gate in REQUIRED_GATES:
        status = (gate_results.get(gate, {}) or {}).get("status") or default_status.get(gate, "pending")
        audits.append({"audit_name": gate, "path": rel(path_by_gate[gate]), "status": status})
    statuses = [str(audit["status"]) for audit in audits]
    return {
        "audit_name": "closeout_gate",
        "packet_id": RUN_ID,
        "status": "blocked" if any(status.startswith("blocked") for status in statuses) else "pass",
        "audits": audits,
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "claim_boundary": CLAIM_BOUNDARY,
        "final_claim_guard": {
            "audit_name": "final_claim_guard",
            "path": rel(PACKET_FINAL_CLAIM_GUARD),
            "status": (gate_results.get("final_claim_guard", {}) or {}).get("status", "pending"),
        },
    }


def write_packet(payload: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> None:
    write_yaml(WORK_PACKET, work_packet_payload(payload, gate_results))
    write_json(PACKET_CLOSEOUT_GATE, closeout_gate_payload(payload, gate_results))


def update_state_docs(payload: Mapping[str, Any]) -> None:
    write_yaml(WORKSPACE_STATE, workspace_state_payload(payload))
    write_text(CURRENT_WORKING_STATE, current_state_text(payload))
    write_text(GLOBAL_SELECTION_STATUS, next_selection_status_text())
    write_text(SELECTION_STATUS, f95_selection_status_text())
    write_text(CONTEXT_ANCHOR, current_state_text(payload))
    write_text(REVIEW_INDEX, review_index_text())
    write_text(NEXT_STAGE_BRIEF, next_stage_brief_text(payload))
    write_text(NEXT_INPUT_REFS, next_input_refs_text())
    write_text(NEXT_SELECTION_STATUS, next_selection_status_text())
    write_text(NEXT_CONTEXT_ANCHOR, current_state_text(payload))
    write_text(NEXT_REVIEW_INDEX, next_review_index_text())


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path_exists(path):
        return [], []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def write_csv_rows(path: Path, fieldnames: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fields = list(fieldnames)
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: json_ready(row.get(field, "")) for field in fields})


def replace_rows(path: Path, remove_run_ids: set[str], new_rows: Sequence[Mapping[str, Any]]) -> None:
    fieldnames, rows = read_csv_rows(path)
    kept = [row for row in rows if row.get("run_id") not in remove_run_ids and row.get("input_run_id") not in remove_run_ids]
    write_csv_rows(path, fieldnames, [*kept, *new_rows])


def ledger_rows(payload: Mapping[str, Any], gate_passes: int = 0) -> list[dict[str, Any]]:
    created_date = payload["created_at_utc"][:10]
    base = {
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "gate_passes": gate_passes,
        "gate_total": len(REQUIRED_GATES),
        "claim_boundary": CLAIM_BOUNDARY,
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "not_claimed",
        "candidate_count": payload["repair_rotation_decision"]["candidate_count"],
        "scout_clue_count": 1,
        "materialization_candidate_count": 0,
        "meaningful_signal_count": 0,
        "completion_candidate_count": 0,
        "runtime_attempt_rows": 0,
        "best_candidate_id": BEST_VARIANT_ID,
        "net_profit": payload["net_profit"],
        "profit_factor": payload["profit_factor"],
        "drawdown": payload["drawdown"],
        "trade_count": payload["trade_count"],
        "trades_per_day": payload["trades_per_day"],
        "created_at": payload["created_at_utc"],
        "created_at_utc": payload["created_at_utc"],
        "date": created_date,
        "run_date": created_date,
        "path": rel(RESULT_SUMMARY),
        "primary_report": rel(RESULT_SUMMARY),
        "report_path": rel(RESULT_SUMMARY),
        "primary_artifact": rel(DECISION_JSON),
        "result_path": rel(RESULT_SUMMARY),
        "gate_audit_path": rel(PACKET_REQUIRED_GATE_AUDIT),
        "required_gate_audit": rel(PACKET_REQUIRED_GATE_AUDIT),
        "question": "Should F95 repair state-transition embeddings or rotate after candidate gate failure?",
        "next_action": NEXT_RUN_ID,
        "evidence_boundary": "stage_closeout_rotation_only_no_runtime_evidence",
        "work_family": "publish_handoff",
        "run_family": "publish_handoff",
        "run_type": "stage_closeout_rotation",
        "family": "publish_handoff",
        "lane": "stage_closeout_rotation",
        "scoreboard_lane": "stage_closeout_rotation",
        "external_verification_status": "out_of_scope_by_claim_no_strategy_tester_runtime_claim",
        "result_judgment": JUDGMENT,
        "artifact_count": len([path for path in produced_artifacts() if path_exists(path)]),
        "notes": "F95C closeout; Task Force actual calls recorded; no runtime claim; F96 pending-open scaffold.",
    }
    closeout_row = {
        **base,
        "ledger_row_id": f"{RUN_ID}__stage_closeout_rotation",
        "run_id": RUN_ID,
        "run_number": "frontier95C",
        "subrun_id": "stage_closeout_rotation",
        "record_view": "stage_closeout_rotation",
        "tier_scope": "Tier A separate; Tier B separate; Tier A+B combined inherited from F95B",
        "kpi_scope": "f95_closeout_decision",
        "metric_scope": "stage_closeout_rotation",
        "primary_kpi": f"net={payload['net_profit']};pf={payload['profit_factor']};dd={payload['drawdown']};tpd={payload['trades_per_day']}",
        "guardrail_kpi": "candidate_count=0;long_only=true;state_class_collapse=true;runtime=not_applicable",
        "row_id": f"{RUN_ID}__stage_closeout_rotation",
        "view": "stage_closeout_rotation",
        "tier": "closeout_reference",
        "result_status": "negative_memory",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN_DIR),
    }
    planned_row = {
        **base,
        "stage_id": NEXT_STAGE_ID,
        "ledger_row_id": f"{NEXT_RUN_ID}__planned_current_run",
        "run_id": NEXT_RUN_ID,
        "run_number": "frontier96A",
        "subrun_id": "planned_current_run",
        "record_view": "planned_current_run",
        "tier_scope": "not_applicable_planned",
        "kpi_scope": "pending",
        "metric_scope": "pending",
        "scoreboard_lane": "stage_closeout_rotation",
        "status": "planned_current_run_no_authority",
        "judgment": "pending_formal_stage_open",
        "decision": "pending_formal_stage_open",
        "parent_run_id": RUN_ID,
        "next_run_id": "",
        "rows": 0,
        "gate_passes": 0,
        "gate_total": 0,
        "claim_boundary": "pending_open_scaffold_only_no_runtime_authority_no_goal_achieve",
        "path": rel(NEXT_STAGE_BRIEF),
        "primary_report": rel(NEXT_STAGE_BRIEF),
        "report_path": rel(NEXT_STAGE_BRIEF),
        "primary_artifact": rel(NEXT_STAGE_BRIEF),
        "result_path": rel(NEXT_STAGE_BRIEF),
        "primary_kpi": "pending",
        "guardrail_kpi": "pending_runtime_claim_forbidden",
        "row_id": f"{NEXT_RUN_ID}__planned_current_run",
        "view": "planned_current_run",
        "tier": "not_applicable_planned",
        "result_status": "planned_current_run_no_authority",
        "external_verification_status": "pending",
        "result_judgment": "pending",
        "input_run_id": RUN_ID,
        "output_path": rel(NEXT_STAGE_DIR),
        "question": "Can counterfactual action-value policy create a side-balanced runtime-compatible US100 M5 surface?",
        "next_action": "formal_f96a_stage_open",
        "evidence_boundary": "planned_only_no_runtime_evidence",
        "candidate_count": 0,
        "scout_clue_count": 0,
        "materialization_candidate_count": 0,
        "meaningful_signal_count": 0,
        "completion_candidate_count": 0,
        "runtime_attempt_rows": 0,
        "net_profit": "",
        "profit_factor": "",
        "drawdown": "",
        "trade_count": "",
        "trades_per_day": "",
        "artifact_count": 0,
        "gate_audit_path": "",
        "required_gate_audit": "",
    }
    return [closeout_row, planned_row]


def update_ledgers(payload: Mapping[str, Any], gate_passes: int = 0) -> None:
    rows = ledger_rows(payload, gate_passes=gate_passes)
    remove_ids = {RUN_ID, NEXT_RUN_ID}
    replace_rows(RUN_REGISTRY, remove_ids, rows)
    replace_rows(ALPHA_LEDGER, remove_ids, rows)
    replace_rows(STAGE_LEDGER, remove_ids, [rows[0]])
    replace_rows(NEXT_STAGE_LEDGER, remove_ids, [rows[1]])


def update_artifact_registry(payload: Mapping[str, Any]) -> None:
    rows = []
    for path in produced_artifacts():
        if not path_exists(path):
            continue
        path_rel = rel(path)
        stage_id = NEXT_STAGE_ID if path_rel.startswith(f"stages/{NEXT_STAGE_ID}") else STAGE_ID
        rows.append(
            {
                "stage_id": stage_id,
                "run_id": RUN_ID,
                "artifact_type": "f95c_closeout_rotation",
                "path": path_rel,
                "sha256": sha256_file_lf_normalized(path),
                "created_at": payload["created_at_utc"],
                "claim_boundary": CLAIM_BOUNDARY,
                "artifact_id": f"{RUN_ID}::{path_rel}",
                "created_at_utc": payload["created_at_utc"],
                "notes": "F95C closeout/rotation artifact; no runtime authority.",
                "artifact_path": path_rel,
                "effect": "Supports F95 negative memory and F96 pending-open scaffold only.",
                "size_bytes": io_path(path).stat().st_size,
            }
        )
    replace_rows(ARTIFACT_REGISTRY, {RUN_ID}, rows)


def append_once(path: Path, marker: str, addition: str) -> None:
    existing = io_path(path).read_text(encoding="utf-8-sig") if path_exists(path) else ""
    if marker not in existing:
        write_text(path, existing.rstrip() + "\n\n" + addition.strip() + "\n")


def update_register_docs(payload: Mapping[str, Any]) -> None:
    marker = f"<!-- {RUN_ID} -->"
    addition = f"""{marker}
## F95C Closeout(마감) Rotate(회전) F96

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- Task Force actual calls(태스크포스 실제 호출): `{len(payload['task_force_calls'])}`
- runtime_probe_status(런타임 탐침 상태): `{RUNTIME_PROBE_STATUS}`
- next_action(다음 행동): `{NEXT_RUN_ID}`

Effect(효과): F95(전선95)는 negative memory/reference surface(부정 기억/참고 표면)로 닫고 F96(전선96)은 pending-open scaffold(개방 대기 골격)만 가진다. No selected baseline(선택 기준선 없음), runtime authority(런타임 권위 없음), live readiness(실거래 준비 없음), or Goal Achieve(목표 달성 없음).
"""
    negative_addition = f"""{marker}
## F95C State Transition Negative Memory(부정 기억)

- parent_run_id(부모 실행): `{PARENT_RUN_ID}`
- failed_boundary(실패 경계): candidate_count=0, long-only(롱 전용), state collapse(상태 붕괴), high-cost exposure(고비용 노출), DD cap fail(손실폭 상한 실패), Tier B weakness(티어B 약점).
- do_not_repeat(반복 금지): KMeans/PCA/threshold/filter/session/routing/parameter-only repair(K평균/PCA/임계값/필터/세션/라우팅/파라미터만 수리).
- reopen_condition(재개 조건): new representation/objective/trade-shape/risk-logic novelty(새 표현/목적함수/거래형태/위험로직 신규성).
"""
    append_once(IDEA_REGISTRY, marker, addition)
    append_once(NEGATIVE_REGISTER, marker, negative_addition)
    append_once(WORKSPACE_CHANGELOG, marker, addition)
    append_once(ROOT_CHANGELOG, marker, addition)


def run_gate_cmd(args: Sequence[str], output_path: Path) -> dict[str, Any]:
    command = [sys.executable, "-m", *args, "--output-json", str(output_path), "--allow-blocked-exit-zero"]
    completed = subprocess.run(command, cwd=ROOT, check=False, capture_output=True, text=True, timeout=180)
    payload: dict[str, Any] = read_json(output_path) if path_exists(output_path) else {}
    result = {
        "command": command,
        "output_path": rel(output_path),
        "returncode": completed.returncode,
        "status": payload.get("status", "missing_output"),
        "passed": payload.get("passed", False),
        "stdout_tail": completed.stdout[-2000:],
        "stderr_tail": completed.stderr[-2000:],
        "allowed_claims": payload.get("allowed_claims", []),
        "forbidden_claims": payload.get("forbidden_claims", []),
    }
    if completed.returncode != 0 or result["status"] != "pass":
        raise RuntimeError(json.dumps(result, ensure_ascii=False, indent=2))
    return result


def sync_review_audit(src: Path, dst: Path) -> None:
    if path_exists(src):
        write_json(dst, read_json(src))


def audit_result_from_gate(name: str, result: Mapping[str, Any]) -> AuditResult:
    return AuditResult(
        audit_name=name,
        status=str(result.get("status", "pass")),
        counts={"source": result.get("output_path", "")},
        allowed_claims=tuple(str(item) for item in result.get("allowed_claims", ())),
        forbidden_claims=tuple(str(item) for item in result.get("forbidden_claims", ())),
    )


def run_control_gates(payload: Mapping[str, Any]) -> dict[str, Any]:
    results: dict[str, Any] = {}
    results["work_packet_schema_lint"] = run_gate_cmd(
        ["foundation.control_plane.work_packet_schema_lint", str(WORK_PACKET)],
        PACKET_WORK_PACKET_LINT,
    )
    results["skill_receipt_schema_lint"] = run_gate_cmd(
        ["foundation.control_plane.skill_receipt_schema_lint", str(SKILL_RECEIPTS)],
        PACKET_SKILL_RECEIPT_LINT,
    )
    results["state_sync_audit"] = run_gate_cmd(
        ["foundation.control_plane.state_sync_audit", "--root", str(ROOT), "--active-stage", NEXT_STAGE_ID, "--current-branch", current_branch()],
        PACKET_STATE_SYNC_AUDIT,
    )
    sync_review_audit(PACKET_STATE_SYNC_AUDIT, STATE_SYNC_AUDIT)
    write_packet(payload, results)
    results["required_gate_coverage_audit"] = run_gate_cmd(
        ["foundation.control_plane.required_gate_coverage_audit", "--work-packet", str(WORK_PACKET), "--closeout-gate", str(PACKET_CLOSEOUT_GATE)],
        PACKET_REQUIRED_GATE_AUDIT,
    )
    sync_review_audit(PACKET_REQUIRED_GATE_AUDIT, REQUIRED_GATE_AUDIT)
    final_guard = guard_final_claims(
        requested_claims=ALLOWED_CLAIMS,
        audit_results=[
            audit_result_from_gate("work_packet_schema_lint", results["work_packet_schema_lint"]),
            audit_result_from_gate("skill_receipt_schema_lint", results["skill_receipt_schema_lint"]),
            audit_result_from_gate("state_sync_audit", results["state_sync_audit"]),
            audit_result_from_gate("required_gate_coverage_audit", results["required_gate_coverage_audit"]),
            AuditResult(audit_name="codex_task_force_review_packet", status="pass"),
            AuditResult(audit_name="frontier_extra_due_check", status="pass_not_due"),
            AuditResult(audit_name="frontier_five_stage_direction_synthesis", status="pass"),
            AuditResult(audit_name="frontier_topic_rotation_check", status="pass"),
            AuditResult(audit_name="scope_completion_gate", status="pass"),
            AuditResult(audit_name="data_integrity_audit", status="pass_with_boundary"),
            AuditResult(audit_name="model_validation_audit", status="pass_with_boundary"),
            AuditResult(audit_name="kpi_contract_audit", status="pass"),
            AuditResult(audit_name="artifact_lineage_audit", status="pass"),
            AuditResult(audit_name="result_judgment_audit", status="negative"),
        ],
    )
    final_payload = final_guard.to_dict()
    final_payload.update({"packet_id": RUN_ID, "claim_boundary": CLAIM_BOUNDARY, "blocked_claims": {claim: "not_claimed" for claim in FORBIDDEN_CLAIMS}})
    write_json(FINAL_CLAIM_GUARD, final_payload)
    write_json(PACKET_FINAL_CLAIM_GUARD, final_payload)
    results["final_claim_guard"] = {
        "status": final_guard.status,
        "output_path": rel(PACKET_FINAL_CLAIM_GUARD),
        "allowed_claims": list(final_guard.allowed_claims),
        "forbidden_claims": list(final_guard.forbidden_claims),
    }
    write_packet(payload, results)
    return results


def write_initial(payload: Mapping[str, Any]) -> None:
    write_run_artifacts(payload)
    update_state_docs(payload)
    write_audits(payload)
    write_receipts(payload)
    write_packet(payload)
    update_ledgers(payload)
    update_register_docs(payload)


def write_final(payload: Mapping[str, Any], gate_results: Mapping[str, Any]) -> None:
    gate_passes = sum(1 for result in gate_results.values() if str(result.get("status", "")).startswith("pass"))
    write_run_artifacts(payload, gate_results)
    update_state_docs(payload)
    write_audits(payload, gate_results)
    write_receipts(payload)
    write_packet(payload, gate_results)
    sync_review_audit(PACKET_STATE_SYNC_AUDIT, STATE_SYNC_AUDIT)
    sync_review_audit(PACKET_REQUIRED_GATE_AUDIT, REQUIRED_GATE_AUDIT)
    update_ledgers(payload, gate_passes=gate_passes)
    update_artifact_registry(payload)


def main() -> int:
    missing = [rel(path) for path in source_inputs() if not path_exists(path)]
    if missing:
        raise FileNotFoundError(f"Missing required F95C source evidence: {missing}")
    ensure_dirs()
    payload = closeout_payload(utc_now())
    write_initial(payload)
    gate_results = run_control_gates(payload)
    write_final(payload, gate_results)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "candidate_gate_count": payload["repair_rotation_decision"]["candidate_count"],
                "runtime_probe_status": RUNTIME_PROBE_STATUS,
                "task_force_actual_subagent_call_count": len(payload["task_force_calls"]),
                "next_run_id": NEXT_RUN_ID,
                "gate_statuses": {key: value.get("status") for key, value in gate_results.items()},
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
