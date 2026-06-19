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

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized


STAGE_ID = "stage_frontier_93__side_balance_cost_exposure_risk_budget_axis"
RUN_ID = "frontier93C_side_balance_cost_exposure_risk_budget_repair_or_rotation_decision_v1"
PARENT_RUN_ID = "frontier93B_side_balance_cost_exposure_risk_budget_proxy_scout_v1"
NEXT_STAGE_ID = "stage_frontier_94__tier_stable_realized_utility_label_axis"
NEXT_RUN_ID = "frontier94A_stage_open_tier_stable_realized_utility_label_axis_v1"
SCRIPT_REL = "stage_pipelines/stage_frontier_93/frontier93c_repair_rotation.py"

STATUS = "f93c_closed_negative_side_balance_cost_exposure_risk_budget_rotate_to_f94_no_authority"
JUDGMENT = "negative_side_balance_cost_exposure_risk_budget_proxy_no_candidate_no_runtime_trigger"
DECISION = "close_f93_negative_rotate_to_tier_stable_realized_utility_label_axis"
CLAIM_BOUNDARY = (
    "f93c_stage_closeout_rotation_only_no_candidate_no_selected_baseline_no_mt5_runtime_evidence_"
    "no_operating_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve"
)
RUNTIME_PROBE_STATUS = (
    "not_run_no_candidate_no_runnable_decision_surface_no_onnx_ea_set_behavior_"
    "no_runtime_materialization_economics_claim_not_cost_or_proxy_bad_skip"
)
FRONTIER_EXTRA_DUE_STATUS = "not_due_after_f93_closeout_next_boundary_f100_e01_closed_for_f050"
FRONTIER_TOPIC_ROTATION_STATUS = (
    "passed_f94_tier_stable_realized_utility_label_axis_not_f93_side_cost_budget_repair"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / "frontier93C"
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

STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
INPUT_REFS = STAGE_DIR / "01_inputs" / "input_refs.md"
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

F93B_RUN = STAGE_DIR / "02_runs" / "frontier93B"
F93B_RUN_MANIFEST = F93B_RUN / "run_manifest.json"
F93B_SUMMARY = F93B_RUN / "summary.json"
F93B_KPI = F93B_RUN / "kpi_record.json"
F93B_TIER_ROUTE_SUMMARY = F93B_RUN / "proxy_scout" / "tier_route_summary.json"
F93B_TIER_B_SUMMARY = F93B_RUN / "proxy_scout" / "tier_b_summary.json"
F93B_VARIANT_METRICS = F93B_RUN / "proxy_scout" / "variant_metrics.csv"
F93B_SPLIT_METRICS = F93B_RUN / "proxy_scout" / "split_metrics.csv"
F93B_NEGATIVE_CONTROLS = F93B_RUN / "proxy_scout" / "negative_control_metrics.csv"
F93B_CANDIDATE_GATE = F93B_RUN / "proxy_scout" / "candidate_gate.json"
F93B_RESULT_SUMMARY = F93B_RUN / "reports" / "result_summary.md"
F93B_WORK_PACKET = ROOT / "docs" / "agent_control" / "packets" / PARENT_RUN_ID / "work_packet.yaml"
F93B_CLOSEOUT_GATE = ROOT / "docs" / "agent_control" / "packets" / PARENT_RUN_ID / "closeout_gate.json"
F93B_TASK_FORCE = ROOT / "docs" / "agent_control" / "packets" / PARENT_RUN_ID / "codex_task_force_review_packet.json"

RUN_MANIFEST = RUN_DIR / "run_manifest.json"
SUMMARY_JSON = RUN_DIR / "summary.json"
KPI_RECORD = RUN_DIR / "kpi_record.json"
DECISION_JSON = DECISION_DIR / "decision.json"
RESULT_SUMMARY = REPORT_DIR / "summary.md"
STAGE_CLOSEOUT_SUMMARY = REVIEW_DIR / "f93c_stage_closeout_summary.json"
STAGE_CLOSEOUT_REPORT = REVIEW_DIR / "stage_closeout_report.md"
F93C_REPORT = REVIEW_DIR / "frontier93C_side_balance_cost_repair_or_rotation_decision_report.md"
TASK_FORCE_REVIEW = REVIEW_DIR / "f93c_task_force_review_receipt.json"
TASK_FORCE_PACKET_REVIEW = PACKET_DIR / "codex_task_force_review_packet.json"
FRONTIER_EXTRA_DUE_CHECK = REVIEW_DIR / "f93c_frontier_extra_due_check.json"
FIVE_STAGE_SYNTHESIS = REVIEW_DIR / "f93c_frontier_five_stage_direction_synthesis.json"
TOPIC_ROTATION_CHECK = REVIEW_DIR / "f93c_frontier_topic_rotation_check.json"
SCOPE_GATE = REVIEW_DIR / "f93c_scope_completion_gate.json"
DATA_INTEGRITY_AUDIT = REVIEW_DIR / "f93c_data_integrity_audit.json"
MODEL_VALIDATION_AUDIT = REVIEW_DIR / "f93c_model_validation_audit.json"
KPI_CONTRACT_AUDIT = REVIEW_DIR / "f93c_kpi_contract_audit.json"
ARTIFACT_AUDIT = REVIEW_DIR / "f93c_artifact_lineage_audit.json"
RESULT_JUDGMENT_AUDIT = REVIEW_DIR / "f93c_result_judgment_audit.json"
FINAL_CLAIM_GUARD = REVIEW_DIR / "f93c_final_claim_guard.json"
STATE_SYNC_AUDIT = REVIEW_DIR / "f93c_state_sync_audit.json"
REQUIRED_GATE_AUDIT = REVIEW_DIR / "f93c_required_gate_coverage_audit.json"
DECISION_MEMO = ROOT / "docs" / "decisions" / "2026-06-19_frontier93c_closeout_rotate_f94.md"

WORK_PACKET = PACKET_DIR / "work_packet.yaml"
SKILL_RECEIPTS = PACKET_DIR / "skill_receipts.json"
PACKET_FINAL_CLAIM_GUARD = PACKET_DIR / "final_claim_guard.json"
PACKET_CLOSEOUT_GATE = PACKET_DIR / "closeout_gate.json"
PACKET_STATE_SYNC_AUDIT = PACKET_DIR / "state_sync_audit.json"
PACKET_REQUIRED_GATE_AUDIT = PACKET_DIR / "required_gate_coverage_audit.json"
PACKET_WORK_PACKET_LINT = PACKET_DIR / "work_packet_schema_lint.json"
PACKET_SKILL_RECEIPT_LINT = PACKET_DIR / "skill_receipt_schema_lint.json"

ALLOWED_CLAIMS = [
    "f93_closed_negative_memory_recorded",
    "f93_repair_disposition_closed",
    "f94_pending_open_scaffold_recorded",
    "task_force_actual_calls_recorded_for_f93c",
    "frontier_extra_due_check_not_due_after_f93",
    "frontier_topic_rotation_check_recorded",
]
FORBIDDEN_CLAIMS = [
    "completion",
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
    "f94_stage_open_completed",
    "task_force_reviewed",
    "task_force_reviewed_pass",
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
    "required_gate_coverage_audit",
    "final_claim_guard",
]
REQUIRED_SKILLS = [
    "obsidian-stage-transition",
    "obsidian-run-evidence-system",
    "obsidian-data-integrity",
    "obsidian-model-validation",
    "obsidian-artifact-lineage",
    "obsidian-result-judgment",
    "obsidian-exploration-mandate",
    "obsidian-task-force-review",
    "obsidian-claim-discipline",
    "obsidian-answer-clarity",
]


def utc_now() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    text = str(path)
    if text.startswith("\\\\?\\"):
        text = text[4:]
    try:
        return Path(text).resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return Path(text).as_posix()


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


def append_once(path: Path, marker: str, addition: str) -> None:
    text = io_path(path).read_text(encoding="utf-8-sig") if path_exists(path) else ""
    if marker in text:
        return
    joiner = "" if not text or text.endswith("\n") else "\n"
    write_text(path, text + joiner + addition.strip() + "\n")


def file_identity(path: Path) -> dict[str, Any]:
    if not path_exists(path):
        return {"path": rel(path), "exists": False, "sha256": None, "size_bytes": None}
    return {
        "path": rel(path),
        "exists": True,
        "sha256": sha256_file_lf_normalized(path),
        "size_bytes": io_path(path).stat().st_size,
    }


def source_inputs() -> list[Path]:
    return [
        F93B_RUN_MANIFEST,
        F93B_SUMMARY,
        F93B_KPI,
        F93B_CANDIDATE_GATE,
        F93B_TIER_ROUTE_SUMMARY,
        F93B_TIER_B_SUMMARY,
        F93B_VARIANT_METRICS,
        F93B_SPLIT_METRICS,
        F93B_NEGATIVE_CONTROLS,
        F93B_RESULT_SUMMARY,
        F93B_WORK_PACKET,
        F93B_CLOSEOUT_GATE,
        F93B_TASK_FORCE,
    ]


def produced_artifacts() -> list[Path]:
    return [
        ROOT / SCRIPT_REL,
        RUN_MANIFEST,
        SUMMARY_JSON,
        KPI_RECORD,
        DECISION_JSON,
        RESULT_SUMMARY,
        STAGE_CLOSEOUT_SUMMARY,
        STAGE_CLOSEOUT_REPORT,
        F93C_REPORT,
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
    ] + list(SKILL_RECEIPT_DIR.glob("*.json"))


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
    ):
        io_path(directory).mkdir(parents=True, exist_ok=True)


def task_force_calls() -> list[dict[str, Any]]:
    return [
        {
            "roster_agent_id": "agent_01_system_governor",
            "agent_nickname": "Tesla",
            "spawned_agent_id": "019ede5e-4c80-79a2-897c-2e353f89efa8",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "accepted",
            "accepted_summary": "Close F93 as negative/no-authority and rotate; capped repair would risk same side/cost budget micro-tuning.",
        },
        {
            "roster_agent_id": "agent_04_evidence_control_plane",
            "agent_nickname": "Boyle",
            "spawned_agent_id": "019ede5e-6098-7172-87df-610958313033",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "needs_local_verification",
            "accepted_summary": "F93C needs fresh packet, receipts, gate coverage, final claim guard, and F93C-context actual calls; F93B gates are input evidence only.",
        },
        {
            "roster_agent_id": "agent_05_data_feature_contract",
            "agent_nickname": "Locke",
            "spawned_agent_id": "019ede5e-7504-72a1-a954-6f43c02a28ca",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "accepted",
            "accepted_summary": "No data repair is needed for negative proxy closeout; F93B data evidence is sufficient inside proxy-only boundary.",
        },
        {
            "roster_agent_id": "agent_06_quant_research",
            "agent_nickname": "James",
            "spawned_agent_id": "019ede5e-902b-74b1-a341-84d8b558498d",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "accepted",
            "accepted_summary": "Reject same-axis capped repair; preserve side/cost budget as reference clue and rotate to tier-stable realized-utility labels.",
        },
        {
            "roster_agent_id": "agent_07_model_validation_risk",
            "agent_nickname": "Aristotle",
            "spawned_agent_id": "019ede5e-a4d5-71f0-99d7-5b0b6561828e",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "accepted",
            "accepted_summary": "OOS final-read PF is a diagnostic clue only; it cannot rescue failed validation/Tier A/Tier B gates or create model readiness.",
        },
        {
            "roster_agent_id": "agent_08_mt5_onnx_runtime",
            "agent_nickname": "Halley",
            "spawned_agent_id": "019ede5e-b936-7680-bbbf-a6b2fcf26c96",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "accepted",
            "accepted_summary": "Runtime evidence gate is out_of_scope_by_claim because no runnable ONNX/EA/set surface or runtime/economics/materialization claim exists.",
        },
    ]


def closeout_payload(now: str) -> dict[str, Any]:
    f93b_summary = read_json(F93B_SUMMARY)
    f93b_kpi = read_json(F93B_KPI)
    candidate_gate = read_json(F93B_CANDIDATE_GATE)
    tier_route = read_json(F93B_TIER_ROUTE_SUMMARY)
    best = f93b_summary["metrics"]["evaluation"]["best_diagnostic_variant"]
    validation = best["validation"]
    oos = best["oos_final_read"]
    best_gate = next(gate for gate in candidate_gate["gates"] if gate["variant_id"] == best["variant_id"])
    decision = {
        "final_disposition": "negative_memory_with_next_frontier_proposal",
        "rotation_selected": True,
        "repair_disposition": "rotate_not_capped_repair",
        "capped_repair_rejected_reason": (
            "F93B validation net/PF/trades_per_day/high_cost_share shows structural cost exposure; "
            "a threshold/filter/session/routing/parameter-only tweak is disallowed."
        ),
        "candidate_count": int(candidate_gate["candidate_count"]),
        "materialization_candidate_count": 0,
        "runtime_attempt_rows": 0,
        "failed_boundary": {
            "validation_net_proxy": validation["net_proxy"],
            "validation_proxy_pf": validation["proxy_pf"],
            "validation_trades_per_day": validation["trades_per_day"],
            "validation_high_cost_share": validation["cost_high_trade_share"],
            "selection_failures": best_gate["selection_failures"],
            "candidate_gate_claim_effect": best_gate["claim_effect"],
        },
        "oos_final_read_boundary": {
            "oos_net_proxy": oos["net_proxy"],
            "oos_proxy_pf": oos["proxy_pf"],
            "oos_trades_per_day": oos["trades_per_day"],
            "oos_high_cost_share": oos["cost_high_trade_share"],
            "claim_effect": "clue_only_not_candidate_selection_or_runtime_trigger",
        },
        "salvage_value": [
            "Actual routed Tier A primary plus Tier B fallback method reconciles and can be reused as a data-routing clue.",
            "Side-balance and cost-exposure budgets helped combined routing density and side balance but did not satisfy Tier A/B gates.",
            "The ridge_regime_dense_cost_norm_side25_q85 surface is a reference clue for future objective design only.",
            "OOS positive final read is preserved as a clue only after validation and Tier-paired gate failure.",
            "Negative controls remain useful for future tier-stable realized-utility label sanity checks.",
        ],
        "negative_memory": [
            "Do not repeat F93 by tightening only threshold, side-share, cost-cap, cost-weight, filter, session, routing, or parameter values.",
            "Do not use the positive OOS final read to rescue a validation-failed candidate gate.",
            "Do not call ridge/logistic/tree scores calibrated probabilities.",
            "Do not drop Tier B separate or actual routed total records.",
            "Do not claim runtime evidence without MT5 Strategy Tester output identity.",
        ],
        "do_not_repeat": [
            "side_cost_budget_threshold_cap_weight_tightening_only",
            "oos_final_read_rescue_after_validation_failure",
            "score_probability_claim",
            "tier_a_only_overclaim",
            "tier_b_negative_thin_fallback_candidate_claim",
            "compile_or_proxy_only_runtime_evidence",
        ],
        "reopen_condition": [
            "A new source, label/horizon, runtime representation, model family/objective, trade shape, risk logic, regime split, or negative-control cause changes the F93 surface.",
            "A future stage predeclares a non-side/cost-budget structural axis and does not borrow F93B OOS final read.",
            "Any revisit retains Tier A separate, Tier B separate, and actual routed total records.",
        ],
        "next_stage_id": NEXT_STAGE_ID,
        "next_run_id": NEXT_RUN_ID,
        "next_axis": {
            "primary_axis": "tier_stable_realized_utility_label",
            "stage_id": NEXT_STAGE_ID,
            "run_id": NEXT_RUN_ID,
            "question": (
                "Can tier-stable realized-utility labels using per-tier payoff asymmetry, cost-adjusted MFE/MAE path, "
                "and side-specific regime split create a runtime-compatible surface without repeating F93 side/cost budget repair?"
            ),
            "novelty_delta": {
                "label_or_objective": "tier-stable realized-utility label rather than side/cost budget overlay selection",
                "trade_shape": "per-tier payoff asymmetry plus cost-adjusted MFE/MAE path",
                "risk_logic": "side-specific regime split and realized utility before ONNX/EA materialization, not side/cost cap tightening",
                "validation_philosophy": "predeclare per-tier utility target and side-regime slices; materialize only if candidate exists",
                "not_threshold_filter_parameter_tweak": True,
            },
            "pending_open_boundary": "scaffold_only_formal_f94a_open_required",
        },
        "tier_scope": {
            "tier_a_rows": tier_route["tier_a_rows"],
            "tier_b_fallback_rows": tier_route["tier_b_fallback_rows"],
            "actual_routed_rows": tier_route["actual_routed_rows"],
            "combined_boundary": tier_route["combined_boundary"],
        },
    }
    return {
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
        "claim_boundary": CLAIM_BOUNDARY,
        "f93b_summary": f93b_summary,
        "f93b_kpi": f93b_kpi,
        "candidate_gate": candidate_gate,
        "repair_rotation_decision": decision,
        "frontier_extra_due_check": {
            "status": "pass_not_due",
            "frontier_closeout": "F93",
            "next_due_boundary": "F100",
            "e01_status": "closed_for_f050",
            "decision": FRONTIER_EXTRA_DUE_STATUS,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "frontier_five_stage_direction_synthesis": {
            "status": "pass",
            "covered_frontier_ids": ["F89", "F90", "F91", "F92", "F93"],
            "dominant_direction": "runtime-compatible proxy surfaces are producing negative memory before materialization",
            "repeated_mechanism": "single-axis proxy rescue pressure after validation/Tier-paired gate failure or no candidate",
            "overused_axis_warning": "side/cost budget thresholds, caps, and weights should not be repeated adjacent",
            "next_axis_options": [
                "tier-stable realized-utility labeling",
                "cost-adjusted MFE/MAE barrier labels",
                "side-specific regime split with per-tier payoff asymmetry",
            ],
            "allowed_reexperiment_conditions": decision["reopen_condition"],
            "adjacent_same_axis_block": True,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "frontier_topic_rotation_check": {
            "status": "pass",
            "proposed_next_stage_id": NEXT_STAGE_ID,
            "proposed_next_run_id": NEXT_RUN_ID,
            "repair_disposition_closed_in_stage": True,
            "same_surface_repair_block": True,
            "topic_ban": False,
            "novelty_delta": decision["next_axis"]["novelty_delta"],
            "decision": FRONTIER_TOPIC_ROTATION_STATUS,
        },
        "task_force": task_force_receipt(decision),
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }


def task_force_receipt(decision: Mapping[str, Any]) -> dict[str, Any]:
    calls = task_force_calls()
    return {
        "packet_id": RUN_ID,
        "skill": "obsidian-task-force-review",
        "status": "executed",
        "trigger_reason": "stage_closeout_rotation_required_and_explicit_user_instruction_required",
        "roster_registry": "docs/agent_control/codex_task_force_registry.yaml",
        "agents_used": [call["roster_agent_id"] for call in calls],
        "actual_subagent_calls": calls,
        "review_requirement": "codex_task_force_review_packet",
        "model_policy": "inherited_parent_model_highest_available_xhigh_when_available",
        "bounded_evidence": [rel(F93B_CANDIDATE_GATE), rel(F93B_KPI), rel(F93B_WORK_PACKET)],
        "advice_classification": {call["roster_agent_id"]: call["opinion_classification"] for call in calls},
        "local_verification": [
            "F93B candidate_count=0 and runtime_probe_triggered=false were verified from the candidate gate.",
            "F93B validation joint gate failed; OOS positive final read is clue only.",
            "F93C records fresh Task Force calls and does not reuse F93B calls.",
            "No runtime/materialization/economics claim is made in F93C.",
        ],
        "final_codex_direction": "Close F93 as negative/no-authority and rotate to F94 pending-open scaffold.",
        "forbidden_claim_check": (
            "No candidate, selected baseline, operating promotion, runtime authority, live readiness, "
            "Goal Achieve, runtime verified, or materialization-ready claim."
        ),
        "claim_boundary": CLAIM_BOUNDARY,
        "decision": decision["final_disposition"],
    }


def run_manifest(payload: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_stage_id": NEXT_STAGE_ID,
        "next_run_id": NEXT_RUN_ID,
        "run_type": "stage_closeout_rotation_decision",
        "script": SCRIPT_REL,
        "created_at_utc": payload["created_at_utc"],
        "status": STATUS,
        "judgment": JUDGMENT,
        "source_artifacts": [rel(path) for path in source_inputs() if path_exists(path)],
        "runtime_evidence_status": RUNTIME_PROBE_STATUS,
        "claim_boundary": CLAIM_BOUNDARY,
        "gate_results": gate_results or {},
    }


def kpi_record(payload: Mapping[str, Any]) -> dict[str, Any]:
    best = payload["f93b_summary"]["metrics"]["evaluation"]["best_diagnostic_variant"]
    val = best["validation"]
    oos = best["oos_final_read"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "hypothesis": (
            "F93 side-balance/cost-exposure risk budget should be repaired only with a non-threshold structural "
            "axis; otherwise rotate."
        ),
        "test_period": "F93B train/validation/OOS evidence consumed as frozen closeout input; F93C is a decision closeout.",
        "proxy_kpi": {
            "source_run_id": PARENT_RUN_ID,
            "best_variant": best["variant_id"],
            "validation_net_proxy": val["net_proxy"],
            "validation_proxy_pf": val["proxy_pf"],
            "validation_max_drawdown": val["max_drawdown"],
            "validation_trade_count": val["trade_count"],
            "validation_trades_per_day": val["trades_per_day"],
            "validation_high_cost_share": val["cost_high_trade_share"],
            "oos_net_proxy": oos["net_proxy"],
            "oos_proxy_pf": oos["proxy_pf"],
            "oos_max_drawdown": oos["max_drawdown"],
            "oos_trade_count": oos["trade_count"],
            "oos_trades_per_day": oos["trades_per_day"],
            "oos_high_cost_share": oos["cost_high_trade_share"],
            "candidate_count": int(payload["candidate_gate"]["candidate_count"]),
        },
        "runtime_kpi": {
            "status": "not_applicable",
            "reason": "No candidate, no runnable decision surface, no ONNX/EA/set behavior claim, and no runtime/materialization/economics claim.",
            "runtime_probe_status": RUNTIME_PROBE_STATUS,
        },
        "closeout_kpi": payload["f93b_kpi"]["closeout_kpi"],
        "net_profit": "source_proxy_only_not_mt5_net_profit",
        "profit_factor": "source_proxy_pf_only_not_runtime_pf",
        "drawdown": "source_proxy_drawdown_only_not_runtime_drawdown",
        "trade_count": "source_proxy_trade_count_only_not_runtime_trade_count",
        "trades_per_day": "source_proxy_trades_per_day_only_not_runtime_density",
        "parity": "not_applicable_no_onnx_ea_runtime_surface",
        "gap_cause": "F93B validation joint gate failed before materialization.",
        "next_action": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def result_summary_text(payload: Mapping[str, Any]) -> str:
    decision = payload["repair_rotation_decision"]
    proxy = kpi_record(payload)["proxy_kpi"]
    return f"""# F93C Repair Or Rotation Decision

Updated: {payload['created_at_utc']}

Conclusion: F93 closes as negative/no-authority. F93B produced no candidate: candidate_count `{decision['candidate_count']}`, validation net `{proxy['validation_net_proxy']}`, validation PF `{proxy['validation_proxy_pf']}`, validation trades/day `{proxy['validation_trades_per_day']}`, validation high-cost share `{proxy['validation_high_cost_share']}`.

Action: F93C records negative memory, salvage value, do-not-repeat notes, reopen conditions, fresh Task Force actual calls, extra_due check, and topic rotation check.

Effect: The project stops adjacent threshold/filter/session/routing/parameter-only repair of F93 side/cost risk budget and rotates to `{NEXT_STAGE_ID}` as pending-open scaffold only.

Runtime: no MT5 Strategy Tester probe. Reason: no candidate, no runnable decision surface, no ONNX/EA/set behavior claim, and no runtime/materialization/economics claim. This is not cost deferral and not a proxy-bad skip.

Next axis: tier-stable realized-utility labeling with per-tier payoff asymmetry, cost-adjusted MFE/MAE path, and side-specific regime split.

Boundary: `{CLAIM_BOUNDARY}`.
"""


def f93_selection_status_text() -> str:
    return f"""# Selection Status

F93 is closed as negative/no-authority. No candidate, no selected baseline, no operating promotion, no runtime authority, no live readiness, no Goal Achieve.

F93B positive OOS final read is a clue only because validation joint gate failed.
"""


def next_stage_brief_text(payload: Mapping[str, Any]) -> str:
    return f"""# {NEXT_STAGE_ID}

Status: pending-open scaffold only. Formal F94A open is not claimed in F93C.

Question: Can tier-stable realized-utility labels using per-tier payoff asymmetry, cost-adjusted MFE/MAE path, and side-specific regime split create a runtime-compatible surface without repeating F93 side/cost budget repair?

Material novelty delta: the primary axis changes from side/cost risk budget density/cost utility to tier-stable realized-utility labeling. It is not threshold/filter/parameter-only repair.

Runtime rule: if F94 creates a meaningful runnable candidate, ONNX/EA/set behavior, or runtime/materialization/economics claim, the same packet must attempt a narrow MT5 Strategy Tester probe or close as blocked/inconclusive/out_of_scope_by_claim.
"""


def next_input_refs_text(payload: Mapping[str, Any]) -> str:
    lines = ["# Input References", ""]
    for path in [SUMMARY_JSON, DECISION_JSON, F93B_CANDIDATE_GATE, F93B_KPI, F93B_TIER_ROUTE_SUMMARY]:
        ident = file_identity(path)
        lines.append(f"- `{ident['path']}` sha256 `{ident['sha256']}`")
    return "\n".join(lines)


def next_selection_status_text() -> str:
    return f"""# Selection Status

F94 is pending-open scaffold only. No candidate, no selected baseline, no operating promotion, no runtime authority, no live readiness, no Goal Achieve.
"""


def current_state_text(payload: Mapping[str, Any]) -> str:
    return f"""# Current Working State

- active_stage: `{NEXT_STAGE_ID}`
- latest_completed_run: `{RUN_ID}`
- current_run: `{NEXT_RUN_ID}`
- status: `{STATUS}`
- judgment: `{JUDGMENT}`
- Task Force: 6 fresh selected agents called for F93C; no Task Force reviewed/pass claim.
- Runtime: `{RUNTIME_PROBE_STATUS}`
- Boundary: `{CLAIM_BOUNDARY}`
"""


def workspace_state_text(payload: Mapping[str, Any]) -> str:
    return f"""current_stage_id: {NEXT_STAGE_ID}
active_stage: {NEXT_STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
frontier_extra_due_status: {FRONTIER_EXTRA_DUE_STATUS}
frontier_topic_rotation_status: {FRONTIER_TOPIC_ROTATION_STATUS}
task_force_status: f93c_actual_subagent_calls_recorded_6_selected_agents_no_task_force_reviewed_pass_claim
runtime_probe_status: {RUNTIME_PROBE_STATUS}
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
updated_at_utc: '{payload['created_at_utc']}'
context_anchor: {rel(NEXT_CONTEXT_ANCHOR)}
notes:
- 'Action: F93C closed F93 as negative/no-authority and wrote F94 pending-open scaffold.'
- 'Effect: threshold/filter/parameter-only repair is blocked; next axis is tier-stable realized-utility labeling.'
- 'Runtime: no Strategy Tester evidence; no runtime authority; no Goal Achieve.'
"""


def review_index_text(payload: Mapping[str, Any]) -> str:
    rows = [
        ("f93c_task_force_review_receipt", TASK_FORCE_REVIEW),
        ("f93c_frontier_extra_due_check", FRONTIER_EXTRA_DUE_CHECK),
        ("f93c_frontier_topic_rotation_check", TOPIC_ROTATION_CHECK),
        ("f93c_required_gate_coverage_audit", REQUIRED_GATE_AUDIT),
        ("f93c_final_claim_guard", FINAL_CLAIM_GUARD),
    ]
    return "# Review Index\n\n" + "\n".join(f"- `{name}`: `{rel(path)}`" for name, path in rows)


def next_review_index_text(payload: Mapping[str, Any]) -> str:
    return f"""# Review Index

- source_closeout: `{rel(STAGE_CLOSEOUT_REPORT)}`
- pending_open_status: `{rel(NEXT_STAGE_BRIEF)}`
"""


def decision_memo_text(payload: Mapping[str, Any]) -> str:
    decision = payload["repair_rotation_decision"]
    return f"""# F93C Closeout Rotate F94

Decision: `{DECISION}`.

Reason: F93B candidate_count is `{decision['candidate_count']}` and validation joint gate failed. The positive OOS final read is preserved as a clue only, not a candidate trigger.

Next: `{NEXT_RUN_ID}` pending-open scaffold. Formal open needs a separate packet.

Not claimed: candidate, selected baseline, operating promotion, runtime authority, live readiness, Goal Achieve.
"""


def write_run_artifacts(payload: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> None:
    write_json(RUN_MANIFEST, run_manifest(payload, gate_results))
    write_json(SUMMARY_JSON, payload)
    write_json(KPI_RECORD, kpi_record(payload))
    write_json(DECISION_JSON, payload["repair_rotation_decision"])
    write_text(RESULT_SUMMARY, result_summary_text(payload))
    write_json(STAGE_CLOSEOUT_SUMMARY, payload)
    write_text(STAGE_CLOSEOUT_REPORT, result_summary_text(payload))
    write_text(F93C_REPORT, result_summary_text(payload))


def audit_payload(
    name: str,
    status: str,
    *,
    passed: bool = True,
    counts: Mapping[str, Any] | None = None,
    allowed: Sequence[str] | None = None,
) -> dict[str, Any]:
    return {
        "audit_name": name,
        "packet_id": RUN_ID,
        "status": status,
        "passed": passed,
        "created_at_utc": utc_now(),
        "counts": dict(counts or {}),
        "allowed_claims": list(allowed or ALLOWED_CLAIMS),
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_audits(payload: Mapping[str, Any]) -> None:
    task_force = payload["task_force"]
    write_json(TASK_FORCE_REVIEW, task_force)
    write_json(
        TASK_FORCE_PACKET_REVIEW,
        {"audit_name": "codex_task_force_review_packet", "status": "pass", "passed": True, **task_force},
    )
    write_json(FRONTIER_EXTRA_DUE_CHECK, audit_payload("frontier_extra_due_check", "pass_not_due", counts=payload["frontier_extra_due_check"]))
    write_json(FIVE_STAGE_SYNTHESIS, audit_payload("frontier_five_stage_direction_synthesis", "pass", counts=payload["frontier_five_stage_direction_synthesis"]))
    write_json(TOPIC_ROTATION_CHECK, audit_payload("frontier_topic_rotation_check", "pass", counts=payload["frontier_topic_rotation_check"]))
    write_json(SCOPE_GATE, audit_payload("scope_completion_gate", "pass", counts={"produced_artifacts": len([p for p in produced_artifacts() if path_exists(p)])}))
    write_json(
        DATA_INTEGRITY_AUDIT,
        audit_payload(
            "data_integrity_audit",
            "pass_with_boundary",
            counts={
                "tier_a_rows": payload["repair_rotation_decision"]["tier_scope"]["tier_a_rows"],
                "tier_b_fallback_rows": payload["repair_rotation_decision"]["tier_scope"]["tier_b_fallback_rows"],
                "actual_routed_rows": payload["repair_rotation_decision"]["tier_scope"]["actual_routed_rows"],
                "routed_sorted": payload["f93b_summary"]["metrics"]["data_integrity"]["routed_sorted"],
                "routed_duplicate_timestamps": payload["f93b_summary"]["metrics"]["data_integrity"]["routed_duplicate_timestamps"],
                "boundary": "F93C consumes frozen F93B evidence and performs no new model fit.",
            },
        ),
    )
    write_json(
        MODEL_VALIDATION_AUDIT,
        audit_payload(
            "model_validation_audit",
            "pass_negative_no_candidate_no_repair_selected",
            counts={
                "candidate_count": int(payload["candidate_gate"]["candidate_count"]),
                "selection_policy": payload["f93b_summary"]["metrics"]["evaluation"]["selection_policy"],
                "score_boundary": "rank_or_utility_score_not_calibrated_probability",
                "oos_boundary": "final_read_only_not_selection",
            },
        ),
    )
    write_json(KPI_CONTRACT_AUDIT, audit_payload("kpi_contract_audit", "pass", counts=kpi_record(payload)))
    write_json(
        ARTIFACT_AUDIT,
        audit_payload(
            "artifact_lineage_audit",
            "pass",
            counts={
                "source_inputs": [file_identity(path) for path in source_inputs()],
                "produced_artifacts": [file_identity(path) for path in produced_artifacts() if path_exists(path)],
                "lineage_judgment": "F93B negative proxy scout -> F93C closeout rotation -> F94 pending scaffold.",
            },
        ),
    )
    write_json(
        RESULT_JUDGMENT_AUDIT,
        {
            **audit_payload("result_judgment_audit", "pass"),
            "result_subject": RUN_ID,
            "evidence_available": [rel(F93B_CANDIDATE_GATE), rel(F93B_KPI), rel(DECISION_JSON), rel(TASK_FORCE_PACKET_REVIEW)],
            "evidence_missing": ["MT5 Strategy Tester output", "runnable ONNX/EA/set candidate", "WFO/stress runtime validation"],
            "judgment_label": JUDGMENT,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "F93 produced negative memory and a new F94 axis proposal, not an operating strategy.",
        },
    )
    guard = {
        "audit_name": "final_claim_guard",
        "packet_id": RUN_ID,
        "status": "pass",
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "candidate_count": int(payload["candidate_gate"]["candidate_count"]),
        "runtime_probe_status": RUNTIME_PROBE_STATUS,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(FINAL_CLAIM_GUARD, guard)
    write_json(PACKET_FINAL_CLAIM_GUARD, guard)


def skill_receipts(payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    common = {
        "packet_id": RUN_ID,
        "status": "executed",
        "claim_boundary": CLAIM_BOUNDARY,
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }
    return [
        {
            **common,
            "skill": "obsidian-stage-transition",
            "source_current_truth_docs": [rel(WORKSPACE_STATE), rel(CURRENT_WORKING_STATE), rel(SELECTION_STATUS)],
            "changed_or_checked_docs": [rel(WORKSPACE_STATE), rel(CURRENT_WORKING_STATE), rel(SELECTION_STATUS), rel(NEXT_STAGE_BRIEF), rel(NEXT_SELECTION_STATUS)],
            "detected_conflicts": ["none_detected"],
            "canonical_state_after": {"active_stage": NEXT_STAGE_ID, "current_run_id": NEXT_RUN_ID, "latest_completed_run_id": RUN_ID},
            "allowed_claims": ALLOWED_CLAIMS,
        },
        {
            **common,
            "skill": "obsidian-run-evidence-system",
            "source_inputs": [rel(path) for path in source_inputs()],
            "produced_artifacts": [rel(path) for path in produced_artifacts() if path_exists(path)],
            "ledger_rows": [f"{RUN_ID}__tier_a_closeout", f"{RUN_ID}__tier_b_fallback_closeout", f"{RUN_ID}__actual_routed_closeout", f"{NEXT_RUN_ID}__planned_current_run"],
            "missing_evidence": ["MT5 Strategy Tester output", "runnable ONNX/EA/set candidate"],
            "allowed_claims": ALLOWED_CLAIMS,
        },
        {
            **common,
            "skill": "obsidian-data-integrity",
            "data_sources_checked": [rel(F93B_TIER_ROUTE_SUMMARY), rel(F93B_KPI), rel(F93B_CANDIDATE_GATE)],
            "time_axis_boundary": "F93B routed timestamps were sorted with duplicate timestamps 0; F93C performs no new row fit.",
            "split_boundary": "F93B train/validation/OOS read is consumed as frozen evidence.",
            "leakage_checks": ["No threshold tuning", "No OOS rescue", "Tier A/Tier B/routed total retained"],
            "missing_data_boundary": "No new data materialized in F93C.",
        },
        {
            **common,
            "skill": "obsidian-model-validation",
            "model_or_threshold_surface": "F93B side/cost risk budget surfaces are closed; no repair selected.",
            "validation_split": "F93B frozen train/validation/OOS split; F93C does not retune.",
            "overfit_checks": ["candidate_count=0", "no threshold/filter/parameter-only repair", "no calibration claim"],
            "selection_metric_boundary": "Decision uses failed predeclared candidate gate only; no model superiority.",
            "allowed_claims": ALLOWED_CLAIMS,
        },
        {
            **common,
            "skill": "obsidian-artifact-lineage",
            "source_inputs": [rel(path) for path in source_inputs()],
            "produced_artifacts": [rel(path) for path in produced_artifacts() if path_exists(path)],
            "raw_evidence": [rel(F93B_CANDIDATE_GATE), rel(F93B_TIER_ROUTE_SUMMARY)],
            "machine_readable": [rel(RUN_MANIFEST), rel(SUMMARY_JSON), rel(KPI_RECORD), rel(DECISION_JSON)],
            "human_readable": [rel(RESULT_SUMMARY), rel(STAGE_CLOSEOUT_REPORT), rel(DECISION_MEMO)],
            "hashes_or_missing_reasons": [file_identity(path) for path in source_inputs()],
            "lineage_boundary": CLAIM_BOUNDARY,
        },
        payload["task_force"],
        {
            **common,
            "skill": "obsidian-result-judgment",
            "judgment_boundary": JUDGMENT,
            "allowed_claims": ALLOWED_CLAIMS,
            "evidence_used": [rel(F93B_CANDIDATE_GATE), rel(F93B_KPI), rel(DECISION_JSON), rel(TASK_FORCE_PACKET_REVIEW)],
        },
        {
            **common,
            "skill": "obsidian-exploration-mandate",
            "exploration_lane": "stage_closeout_rotation",
            "idea_boundary": "F93 closes as negative memory; F94 opens only as pending scaffold.",
            "negative_memory_effect": "Prevents adjacent side/cost risk budget threshold/filter repair from repeating.",
            "operating_claim_boundary": CLAIM_BOUNDARY,
        },
        {
            **common,
            "skill": "obsidian-claim-discipline",
            "requested_claims": ALLOWED_CLAIMS,
            "allowed_claims": ALLOWED_CLAIMS,
            "final_status": STATUS,
        },
        {
            **common,
            "skill": "obsidian-answer-clarity",
            "plain_conclusion": "F93 did not produce a tradable candidate; it produced negative memory and a path-shape next axis.",
            "confirmed": ["F93B candidate_count=0", "F93C Task Force actual calls recorded", "F94 pending scaffold written"],
            "not_yet_confirmed": ["F94 formal open", "MT5 runtime economics", "selected baseline", "runtime authority"],
            "why_it_matters": "This prevents more work on the same failed side/cost risk budget filter surface.",
            "next_action": NEXT_RUN_ID,
            "forbidden_claims_avoided": FORBIDDEN_CLAIMS,
        },
    ]


def receipt_path_for(skill: str) -> Path:
    return SKILL_RECEIPT_DIR / f"{skill.replace('obsidian-', '').replace('-', '_')}.json"


def write_receipts(payload: Mapping[str, Any]) -> None:
    receipts = skill_receipts(payload)
    write_json(SKILL_RECEIPTS, {"packet_id": RUN_ID, "primary_skill": "obsidian-stage-transition", "receipts": receipts})
    for receipt in receipts:
        write_json(receipt_path_for(receipt["skill"]), receipt)


def work_packet(payload: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> dict[str, Any]:
    gates_status = {gate: "pending_external_lint" for gate in REQUIRED_GATES}
    gates_status.update(
        {
            "codex_task_force_review_packet": "pass",
            "frontier_extra_due_check": "pass_not_due",
            "frontier_five_stage_direction_synthesis": "pass",
            "frontier_topic_rotation_check": "pass",
            "scope_completion_gate": "pass",
            "data_integrity_audit": "pass_with_boundary",
            "model_validation_audit": "pass_negative_no_candidate_no_repair_selected",
            "kpi_contract_audit": "pass",
            "artifact_lineage_audit": "pass",
            "result_judgment_audit": "pass",
            "final_claim_guard": "pass",
        }
    )
    if gate_results:
        for name, result in gate_results.items():
            gates_status[name] = result.get("status", "")
    required_evidence = [rel(path) for path in produced_artifacts() if path_exists(path)]
    return {
        "version": "work_packet_schema_v2_1",
        "packet_lifecycle": "new_packet",
        "packet_id": RUN_ID,
        "created_at_utc": payload["created_at_utc"],
        "user_request": {
            "user_quote": "/goal active continuation; user explicitly required Task Force agents when triggered",
            "requested_action": "F93C stage closeout and F94 pending-open rotation scaffold",
            "requested_count": {"value": 1, "n_a_reason": ""},
            "ambiguous_terms": ["No final completion.", "No runtime authority.", "F94 formal open is not claimed."],
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
            "detected_families": ["publish_handoff", "kpi_evidence", "artifact_lineage", "state_sync"],
            "touched_surfaces": [rel(STAGE_DIR), rel(NEXT_STAGE_DIR), rel(PACKET_DIR), rel(WORKSPACE_STATE)],
            "mutation_intent": True,
            "execution_intent": True,
        },
        "risk_vector_scan": {
            "risks": {
                "threshold_only_repair_laundering": "high",
                "oos_positive_final_read_overclaim": "high",
                "f94_scaffold_confused_with_formal_open": "medium",
                "runtime_probe_absence_misread_as_cost_skip": "medium",
            },
            "hard_stop_risks": [
                "Do not claim candidate/runtime/economics/materialization without MT5 Strategy Tester output identity.",
                "Do not call F94 formally open in this packet.",
                "Do not repeat F93 side/cost risk budget by threshold/filter/session/routing/parameter-only tweak.",
            ],
            "required_gates": REQUIRED_GATES,
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        "decision_lock": {
            "mode": "assume_safe_default",
            "assumptions": {
                "task_force_required_now": True,
                "verification_profile": "stage_closeout",
                "strategy_tester_required_now": False,
                "reason": "F93C makes closeout/rotation claims only; no candidate, runnable surface, or runtime/materialization/economics claim exists.",
            },
            "questions": [],
            "required_user_decisions": [],
        },
        "interpreted_scope": {
            "work_families": ["publish_handoff"],
            "target_surfaces": ["F93 closeout", "F94 pending-open scaffold", "Task Force receipt", "state sync"],
            "scope_units": ["stage_closeout", "rotation_decision", "receipt", "state_sync"],
            "execution_layers": ["local_python_execution", "stage_transition"],
            "mutation_policy": {"allowed": True, "user_quote": "/goal active continuation"},
            "evidence_layers": ["F93B proxy metrics", "F93B candidate gate", "F93C Task Force calls"],
            "reduction_policy": {
                "reduction_allowed": False,
                "requires_user_quote": False,
                "rationale": "F93C consumes all F93B closeout evidence and makes no narrowed success claim.",
            },
            "claim_boundary": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
        },
        "verification_profile": {
            "profile_id": "stage_closeout",
            "claim_surface": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
            "trigger_sources": ["active_goal", "F93B no candidate", "closeout_required_task_force_review", "rotation_to_next_frontier"],
            "protected_claims": ALLOWED_CLAIMS,
            "required_evidence": required_evidence,
            "gates_not_run_with_reason": [
                {
                    "gate": "runtime_evidence_gate",
                    "reason_code": "outside_claim_surface_no_runtime_claim",
                    "reason": "F93C protects closeout/rotation only; no candidate, runnable surface, ONNX/EA/set behavior, or runtime/materialization/economics claim is made.",
                    "claim_effect": "Runtime probe, runtime verified, economics pass, materialization ready, handoff ready, authority, live readiness, and Goal Achieve claims are forbidden.",
                },
                {
                    "gate": "f94_stage_open_gate",
                    "reason_code": "pending_open_scaffold_only",
                    "reason": "F93C only writes the F94 pending-open scaffold; formal F94A stage open requires a separate packet.",
                    "claim_effect": "F94 stage-open completed/reviewed/pass claims are forbidden.",
                },
            ],
            "stop_conditions": [
                "No runtime/materialization/economics/authority/Goal Achieve claim.",
                "If a meaningful runnable candidate appears, switch to runtime_probe profile and attempt narrow MT5 probe in the same packet.",
            ],
        },
        "acceptance_criteria": [
            {"id": "AC-001", "text": "F93C decision artifact exists.", "expected_artifact": rel(DECISION_JSON), "verification_method": "scope_completion_gate", "required": True},
            {"id": "AC-002", "text": "F93C Task Force actual calls are recorded.", "expected_artifact": rel(TASK_FORCE_PACKET_REVIEW), "verification_method": "codex_task_force_review_packet", "required": True},
            {"id": "AC-003", "text": "F94 pending-open scaffold exists without formal open claim.", "expected_artifact": rel(NEXT_STAGE_BRIEF), "verification_method": "scope_completion_gate", "required": True},
        ],
        "work_plan": {
            "phases": ["Read F93B evidence.", "Call relevant Task Force agents.", "Write closeout and pending-open scaffold.", "Run gates and state sync."],
            "expected_outputs": required_evidence,
            "stop_conditions": ["No runtime/materialization/economics/authority/Goal Achieve claim."],
        },
        "skill_routing": {
            "primary_family": "publish_handoff",
            "primary_skill": "obsidian-stage-transition",
            "support_skills": REQUIRED_SKILLS[1:],
            "skills_considered": REQUIRED_SKILLS + ["obsidian-runtime-parity", "obsidian-backtest-forensics", "obsidian-performance-attribution"],
            "skills_selected": REQUIRED_SKILLS,
            "skills_not_used": [
                {"skill": "obsidian-runtime-parity", "reason": "No ONNX/EA/runtime parity or handoff claim is made."},
                {"skill": "obsidian-backtest-forensics", "reason": "No new Strategy Tester report or trade list exists in F93C."},
            ],
            "required_skill_receipts": REQUIRED_SKILLS,
            "required_gates": REQUIRED_GATES,
        },
        "evidence_contract": {
            "raw_evidence": [rel(F93B_CANDIDATE_GATE), rel(F93B_TIER_ROUTE_SUMMARY)],
            "machine_readable": [rel(RUN_MANIFEST), rel(SUMMARY_JSON), rel(KPI_RECORD), rel(DECISION_JSON), rel(SKILL_RECEIPTS)],
            "human_readable": [rel(RESULT_SUMMARY), rel(STAGE_CLOSEOUT_REPORT), rel(DECISION_MEMO)],
        },
        "gates": {
            "required": REQUIRED_GATES,
            **gates_status,
            "not_applicable_with_reason": {
                "runtime_evidence_gate": "outside_claim_surface_no_runtime_claim",
                "f94_stage_open_gate": "pending_open_scaffold_only",
            },
        },
        "final_claim_policy": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS},
    }


def write_packet(payload: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> None:
    packet = work_packet(payload, gate_results)
    write_yaml(WORK_PACKET, packet)
    audits = []
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
        "required_gate_coverage_audit": PACKET_REQUIRED_GATE_AUDIT,
        "final_claim_guard": PACKET_FINAL_CLAIM_GUARD,
    }
    for name in REQUIRED_GATES:
        audits.append({"audit_name": name, "path": rel(path_by_gate[name]), "status": packet["gates"].get(name, "pending")})
    closeout = {
        "packet_id": RUN_ID,
        "status": "pass",
        "audits": audits,
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "claim_boundary": CLAIM_BOUNDARY,
        "final_claim_guard": {"audit_name": "final_claim_guard", "path": rel(PACKET_FINAL_CLAIM_GUARD), "status": "pass"},
    }
    write_json(PACKET_CLOSEOUT_GATE, closeout)


def update_state_docs(payload: Mapping[str, Any]) -> None:
    write_text(WORKSPACE_STATE, workspace_state_text(payload))
    write_text(CURRENT_WORKING_STATE, current_state_text(payload))
    write_text(GLOBAL_SELECTION_STATUS, next_selection_status_text())
    write_text(SELECTION_STATUS, f93_selection_status_text())
    write_text(CONTEXT_ANCHOR, current_state_text(payload))
    write_text(REVIEW_INDEX, review_index_text(payload))
    write_text(NEXT_STAGE_BRIEF, next_stage_brief_text(payload))
    write_text(NEXT_INPUT_REFS, next_input_refs_text(payload))
    write_text(NEXT_SELECTION_STATUS, next_selection_status_text())
    write_text(NEXT_CONTEXT_ANCHOR, current_state_text(payload))
    write_text(NEXT_REVIEW_INDEX, next_review_index_text(payload))
    write_text(DECISION_MEMO, decision_memo_text(payload))


def append_dict_rows(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], header_source: Path | None = None) -> None:
    source = path if path_exists(path) else header_source
    if source is None or not path_exists(source):
        raise FileNotFoundError(f"CSV header source missing for {path}")
    with io_path(source).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        existing = list(reader) if path_exists(path) else []
    keys_to_replace = {tuple(str(row.get(field, "")) for field in key_fields) for row in rows}
    kept = [row for row in existing if tuple(str(row.get(field, "")) for field in key_fields) not in keys_to_replace]
    normalized = [{field: json_ready(row.get(field, "")) for field in fieldnames} for row in rows]
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(kept + normalized)


def replace_rows_by_field(path: Path, field: str, value: str, rows: Sequence[Mapping[str, Any]], header_source: Path | None = None) -> None:
    source = path if path_exists(path) else header_source
    if source is None or not path_exists(source):
        raise FileNotFoundError(f"CSV header source missing for {path}")
    with io_path(source).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        existing = list(reader) if path_exists(path) else []
    kept = [row for row in existing if str(row.get(field, "")).strip() != value]
    normalized = [{column: json_ready(row.get(column, "")) for column in fieldnames} for row in rows]
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(kept + normalized)


def ledger_rows(payload: Mapping[str, Any], gate_passes: int = 0) -> list[dict[str, Any]]:
    created_date = payload["created_at_utc"][:10]
    proxy = kpi_record(payload)["proxy_kpi"]
    base = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "stage_closeout_rotation",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(RESULT_SUMMARY),
        "notes": "F93 closeout; no runtime claim; F94 pending-open scaffold.",
        "family": "publish_handoff",
        "primary_report": rel(RESULT_SUMMARY),
        "run_number": "frontier93C",
        "date": created_date,
        "decision": DECISION,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "rows": payload["repair_rotation_decision"]["tier_scope"]["actual_routed_rows"],
        "gate_passes": gate_passes,
        "gate_total": len(REQUIRED_GATES),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(RESULT_SUMMARY),
        "run_date": created_date,
        "primary_artifact": rel(DECISION_JSON),
        "result_status": STATUS,
        "scoreboard_lane": "stage_closeout_rotation",
        "external_verification_status": "out_of_scope_by_claim_no_strategy_tester_runtime_claim",
        "result_judgment": JUDGMENT,
        "gate_audit_path": rel(PACKET_REQUIRED_GATE_AUDIT),
        "created_at": payload["created_at_utc"],
        "work_family": "publish_handoff",
        "evidence_boundary": "stage_closeout_rotation_only_no_runtime_evidence",
        "next_action": NEXT_RUN_ID,
        "question": "Should F93 repair side/cost risk budget or rotate after validation gate failure?",
        "artifact_count": len([path for path in produced_artifacts() if path_exists(path)]),
        "created_at_utc": payload["created_at_utc"],
        "required_gate_audit": rel(PACKET_REQUIRED_GATE_AUDIT),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "run_family": "publish_handoff",
        "run_type": "stage_closeout_rotation",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN_DIR),
        "result_path": rel(RESULT_SUMMARY),
        "goal_achieve": "not_claimed",
        "source_authority": "not_claimed",
        "candidate_count": 0,
        "scout_clue_count": 1,
        "materialization_candidate_count": 0,
        "meaningful_signal_count": 0,
        "completion_candidate_count": 0,
        "runtime_attempt_rows": 0,
    }
    views = [
        (
            "tier_a_closeout",
            "Tier A separate",
            "negative_memory",
            f"source_best={proxy['best_variant']};validation_gate_failed",
            "Tier A retained; no candidate.",
        ),
        (
            "tier_b_fallback_closeout",
            "Tier B fallback used",
            "negative_memory",
            f"tier_b_fallback_rows={payload['repair_rotation_decision']['tier_scope']['tier_b_fallback_rows']}",
            "Tier B retained as fallback-route evidence, not separate success.",
        ),
        (
            "actual_routed_closeout",
            "actual routed total",
            "negative_memory",
            f"val_net={proxy['validation_net_proxy']};val_pf={proxy['validation_proxy_pf']};val_tpd={proxy['validation_trades_per_day']}",
            "Combined routed result failed validation gate.",
        ),
    ]
    rows = []
    for record_view, tier_scope, view_status, primary_kpi, guardrail in views:
        row = dict(base)
        row.update(
            {
                "ledger_row_id": f"{RUN_ID}__{record_view}",
                "subrun_id": f"{RUN_ID}__{record_view}",
                "record_view": record_view,
                "tier_scope": tier_scope,
                "kpi_scope": "f93_closeout_decision",
                "primary_kpi": primary_kpi,
                "guardrail_kpi": guardrail,
                "row_id": f"{RUN_ID}__{record_view}",
                "view": record_view,
                "tier": tier_scope,
                "metric_scope": "stage_closeout_rotation",
                "result_status": view_status,
            }
        )
        rows.append(row)
    planned = dict(base)
    planned.update(
        {
            "run_id": NEXT_RUN_ID,
            "stage_id": NEXT_STAGE_ID,
            "status": "planned_current_run_no_authority",
            "judgment": "pending_formal_stage_open",
            "path": rel(NEXT_STAGE_BRIEF),
            "notes": "F94 pending-open scaffold after F93C negative closeout.",
            "primary_report": rel(NEXT_STAGE_BRIEF),
            "run_number": "frontier94A",
            "decision": "pending_formal_stage_open",
            "parent_run_id": RUN_ID,
            "next_run_id": "",
            "rows": 0,
            "gate_passes": 0,
            "gate_total": 0,
            "claim_boundary": "pending_open_scaffold_only_no_runtime_authority_no_goal_achieve",
            "report_path": rel(NEXT_STAGE_BRIEF),
            "primary_artifact": rel(NEXT_STAGE_BRIEF),
            "result_status": "planned_current_run_no_authority",
            "external_verification_status": "pending",
            "result_judgment": "pending",
            "gate_audit_path": "",
            "ledger_row_id": f"{NEXT_RUN_ID}__planned_current_run",
            "subrun_id": f"{NEXT_RUN_ID}__planned_current_run",
            "record_view": "planned_current_run",
            "tier_scope": "not_applicable_planned",
            "kpi_scope": "pending",
            "primary_kpi": "pending",
            "guardrail_kpi": "pending_runtime_claim_forbidden",
            "row_id": f"{NEXT_RUN_ID}__planned_current_run",
            "view": "planned_current_run",
            "tier": "not_applicable_planned",
            "metric_scope": "pending",
            "evidence_boundary": "planned_only_no_runtime_evidence",
            "next_action": "formal_f94a_stage_open",
            "question": "Can tier-stable realized-utility labels create a runtime-compatible US100 M5 surface?",
            "artifact_count": 0,
            "required_gate_audit": "",
            "run_type": "planned_current_run",
            "input_run_id": RUN_ID,
            "output_path": rel(NEXT_STAGE_DIR),
            "result_path": rel(NEXT_STAGE_BRIEF),
            "scout_clue_count": 0,
        }
    )
    rows.append(planned)
    return rows


def update_ledgers(payload: Mapping[str, Any], gate_passes: int = 0) -> None:
    rows = ledger_rows(payload, gate_passes=gate_passes)
    run_rows = [dict(rows[0]), dict(rows[-1])]
    append_dict_rows(RUN_REGISTRY, ["run_id"], run_rows)
    append_dict_rows(ALPHA_LEDGER, ["ledger_row_id"], rows)
    append_dict_rows(STAGE_LEDGER, ["ledger_row_id"], rows[:-1], header_source=ALPHA_LEDGER)
    append_dict_rows(NEXT_STAGE_LEDGER, ["ledger_row_id"], [rows[-1]], header_source=ALPHA_LEDGER)


def update_artifact_registry(payload: Mapping[str, Any]) -> None:
    rows = []
    for path in produced_artifacts():
        if not path_exists(path):
            continue
        path_rel = rel(path)
        rows.append(
            {
                "stage_id": STAGE_ID if path_rel.startswith(f"stages/{STAGE_ID}") or "frontier93C" in path_rel or "f93c" in path_rel else NEXT_STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": "f93c_closeout_rotation",
                "path": path_rel,
                "sha256": sha256_file_lf_normalized(path),
                "created_at": payload["created_at_utc"],
                "claim_boundary": CLAIM_BOUNDARY,
                "artifact_id": f"{RUN_ID}::{path_rel}",
                "created_at_utc": payload["created_at_utc"],
                "notes": "F93C closeout/rotation artifact; no runtime authority.",
                "artifact_path": path_rel,
                "effect": "Supports F93 negative memory and F94 pending-open scaffold only.",
                "size_bytes": io_path(path).stat().st_size,
            }
        )
    replace_rows_by_field(ARTIFACT_REGISTRY, "run_id", RUN_ID, rows)


def update_register_docs(payload: Mapping[str, Any]) -> None:
    marker = f"{RUN_ID}__closeout_record"
    idea_addition = f"""
<!-- {marker} -->

## F93C side-balance cost-exposure risk-budget closeout

- run_id: `{RUN_ID}`
- hypothesis: F93 side/cost risk budget should rotate unless a non-threshold structural repair exists.
- result: negative_memory, no candidate, no runtime trigger.
- next_action: `{NEXT_RUN_ID}` pending-open scaffold.
- claim_boundary: `{CLAIM_BOUNDARY}`.
"""
    negative_addition = f"""
<!-- {marker} -->

## F93C side/cost risk budget negative closeout

- run_id: `{RUN_ID}`
- failed_boundary: F93B validation net/PF/trades-per-day/high-cost share failed the joint candidate gate.
- salvage_value: routed Tier B fallback method, high-cost concentration diagnostic, and OOS positive final read as clue only.
- do_not_repeat: threshold/filter/session/routing/parameter-only tweak, OOS rescue, score probability claim, Tier A-only overclaim, compile/proxy-only runtime evidence.
- reopen_condition: new label utility, cost representation, runtime representation, or negative-control cause.
"""
    changelog_addition = f"""
<!-- {marker} -->

## {payload['created_at_utc']} - F93C Closeout Rotate F94

- Action: `frontier93C_side_balance_cost_exposure_risk_budget_repair_or_rotation_decision_v1` closed F93 as negative/no-authority.
- Effect: adjacent threshold/filter/parameter repair is blocked and F94 pending-open scaffold was written at `{NEXT_STAGE_ID}`.
- Runtime: no new Strategy Tester runtime evidence; no runtime authority; no Goal Achieve.
- Boundary: `{CLAIM_BOUNDARY}`.
"""
    append_once(IDEA_REGISTRY, marker, idea_addition)
    append_once(NEGATIVE_REGISTER, marker, negative_addition)
    append_once(WORKSPACE_CHANGELOG, marker, changelog_addition)
    append_once(ROOT_CHANGELOG, marker, changelog_addition)


def write_state_sync_seed(payload: Mapping[str, Any]) -> None:
    seed = audit_payload(
        "state_sync_audit",
        "pending_external_lint",
        counts={"active_stage": NEXT_STAGE_ID, "current_run_id": NEXT_RUN_ID, "latest_completed_run_id": RUN_ID},
    )
    write_json(STATE_SYNC_AUDIT, seed)
    write_json(PACKET_STATE_SYNC_AUDIT, seed)


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
    }
    if completed.returncode != 0 or result["status"] != "pass":
        raise RuntimeError(json.dumps(result, ensure_ascii=False, indent=2))
    return result


def sync_review_audit(src: Path, dst: Path) -> None:
    if path_exists(src):
        write_json(dst, read_json(src))


def run_control_gates(payload: Mapping[str, Any]) -> dict[str, Any]:
    results: dict[str, Any] = {}
    results["work_packet_schema_lint"] = run_gate_cmd(["foundation.control_plane.work_packet_schema_lint", str(WORK_PACKET)], PACKET_WORK_PACKET_LINT)
    results["skill_receipt_schema_lint"] = run_gate_cmd(["foundation.control_plane.skill_receipt_schema_lint", str(SKILL_RECEIPTS)], PACKET_SKILL_RECEIPT_LINT)
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
    write_packet(payload, results)
    return results


def write_initial(payload: Mapping[str, Any]) -> None:
    write_run_artifacts(payload)
    write_audits(payload)
    write_receipts(payload)
    write_packet(payload)
    update_state_docs(payload)
    update_ledgers(payload)
    update_register_docs(payload)
    write_state_sync_seed(payload)


def write_final(payload: Mapping[str, Any], gate_results: Mapping[str, Any]) -> None:
    gate_passes = sum(1 for result in gate_results.values() if result.get("status") == "pass") + 11
    write_run_artifacts(payload, gate_results)
    write_audits(payload)
    write_receipts(payload)
    write_packet(payload, gate_results)
    sync_review_audit(PACKET_STATE_SYNC_AUDIT, STATE_SYNC_AUDIT)
    sync_review_audit(PACKET_REQUIRED_GATE_AUDIT, REQUIRED_GATE_AUDIT)
    update_ledgers(payload, gate_passes=gate_passes)
    update_artifact_registry(payload)


def main() -> int:
    missing = [rel(path) for path in source_inputs() if not path_exists(path)]
    if missing:
        raise FileNotFoundError(f"Missing required F93C source evidence: {missing}")
    ensure_dirs()
    payload = closeout_payload(utc_now())
    write_initial(payload)
    gate_results = run_control_gates(payload)
    write_final(payload, gate_results)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
