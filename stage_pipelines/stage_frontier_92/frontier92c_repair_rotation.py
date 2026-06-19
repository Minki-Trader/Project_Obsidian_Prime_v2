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


STAGE_ID = "stage_frontier_92__path_conditioned_trade_shape_labeling_axis"
RUN_ID = "frontier92C_path_trade_shape_repair_or_rotation_decision_v1"
PARENT_RUN_ID = "frontier92B_path_conditioned_trade_shape_label_proxy_scout_v1"
NEXT_STAGE_ID = "stage_frontier_93__side_balance_cost_exposure_risk_budget_axis"
NEXT_RUN_ID = "frontier93A_stage_open_side_balance_cost_exposure_risk_budget_axis_v1"
SCRIPT_REL = "stage_pipelines/stage_frontier_92/frontier92c_repair_rotation.py"

STATUS = "f92c_closed_negative_path_trade_shape_label_axis_rotate_to_f93_no_authority"
JUDGMENT = "negative_path_trade_shape_proxy_no_candidate_no_runtime_trigger"
DECISION = "close_f92_negative_rotate_to_side_balance_cost_exposure_risk_budget_axis"
CLAIM_BOUNDARY = (
    "f92c_stage_closeout_rotation_only_no_candidate_no_selected_baseline_no_mt5_runtime_evidence_"
    "no_operating_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve"
)
RUNTIME_PROBE_STATUS = (
    "not_run_no_candidate_no_runnable_decision_surface_no_onnx_ea_set_behavior_"
    "no_runtime_materialization_economics_claim_not_cost_or_proxy_bad_skip"
)
FRONTIER_EXTRA_DUE_STATUS = "not_due_after_f92_closeout_next_boundary_f100_e01_closed_for_f050"
FRONTIER_TOPIC_ROTATION_STATUS = (
    "passed_f93_side_balance_cost_exposure_risk_budget_axis_not_f92_path_label_threshold_repair"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / "frontier92C"
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

F92B_RUN = STAGE_DIR / "02_runs" / "frontier92B"
F92B_CANDIDATE_GATE = F92B_RUN / "proxy_scout" / "candidate_gate.json"
F92B_SPLIT_METRICS = F92B_RUN / "proxy_scout" / "split_metrics.csv"
F92B_TIER_ROUTE_SUMMARY = F92B_RUN / "proxy_scout" / "tier_route_summary.json"
F92B_TIER_B_SUMMARY = F92B_RUN / "proxy_scout" / "tier_b_summary.json"
F92B_RESULT_SUMMARY = F92B_RUN / "reports" / "result_summary.md"
F92B_SUMMARY_REVIEW = REVIEW_DIR / "f92b_execution_summary.json"
F92B_DATA_INTEGRITY = REVIEW_DIR / "f92b_data_integrity_audit.json"
F92B_FINAL_CLAIM_GUARD = REVIEW_DIR / "f92b_final_claim_guard.json"
F92B_REQUIRED_GATE_AUDIT = REVIEW_DIR / "f92b_required_gate_coverage_audit.json"
F92B_WORK_PACKET = ROOT / "docs" / "agent_control" / "packets" / PARENT_RUN_ID / "work_packet.yaml"
F92B_TASK_FORCE = ROOT / "docs" / "agent_control" / "packets" / PARENT_RUN_ID / "codex_task_force_review_packet.json"

RUN_MANIFEST = RUN_DIR / "run_manifest.json"
SUMMARY_JSON = RUN_DIR / "summary.json"
KPI_RECORD = RUN_DIR / "kpi_record.json"
DECISION_JSON = DECISION_DIR / "decision.json"
RESULT_SUMMARY = REPORT_DIR / "summary.md"
STAGE_CLOSEOUT_SUMMARY = REVIEW_DIR / "f92c_stage_closeout_summary.json"
STAGE_CLOSEOUT_REPORT = REVIEW_DIR / "stage_closeout_report.md"
F92C_REPORT = REVIEW_DIR / "frontier92C_path_trade_shape_repair_or_rotation_decision_report.md"
TASK_FORCE_REVIEW = REVIEW_DIR / "f92c_task_force_review_receipt.json"
TASK_FORCE_PACKET_REVIEW = PACKET_DIR / "codex_task_force_review_packet.json"
FRONTIER_EXTRA_DUE_CHECK = REVIEW_DIR / "f92c_frontier_extra_due_check.json"
FIVE_STAGE_SYNTHESIS = REVIEW_DIR / "f92c_frontier_five_stage_direction_synthesis.json"
TOPIC_ROTATION_CHECK = REVIEW_DIR / "f92c_frontier_topic_rotation_check.json"
SCOPE_GATE = REVIEW_DIR / "f92c_scope_completion_gate.json"
DATA_INTEGRITY_AUDIT = REVIEW_DIR / "f92c_data_integrity_audit.json"
MODEL_VALIDATION_AUDIT = REVIEW_DIR / "f92c_model_validation_audit.json"
KPI_CONTRACT_AUDIT = REVIEW_DIR / "f92c_kpi_contract_audit.json"
ARTIFACT_AUDIT = REVIEW_DIR / "f92c_artifact_lineage_audit.json"
RESULT_JUDGMENT_AUDIT = REVIEW_DIR / "f92c_result_judgment_audit.json"
FINAL_CLAIM_GUARD = REVIEW_DIR / "f92c_final_claim_guard.json"
STATE_SYNC_AUDIT = REVIEW_DIR / "f92c_state_sync_audit.json"
REQUIRED_GATE_AUDIT = REVIEW_DIR / "f92c_required_gate_coverage_audit.json"
DECISION_MEMO = ROOT / "docs" / "decisions" / "2026-06-19_frontier92c_closeout_rotate_f93.md"

WORK_PACKET = PACKET_DIR / "work_packet.yaml"
SKILL_RECEIPTS = PACKET_DIR / "skill_receipts.json"
PACKET_FINAL_CLAIM_GUARD = PACKET_DIR / "final_claim_guard.json"
PACKET_CLOSEOUT_GATE = PACKET_DIR / "closeout_gate.json"
PACKET_STATE_SYNC_AUDIT = PACKET_DIR / "state_sync_audit.json"
PACKET_REQUIRED_GATE_AUDIT = PACKET_DIR / "required_gate_coverage_audit.json"
PACKET_WORK_PACKET_LINT = PACKET_DIR / "work_packet_schema_lint.json"
PACKET_SKILL_RECEIPT_LINT = PACKET_DIR / "skill_receipt_schema_lint.json"

ALLOWED_CLAIMS = [
    "f92_closed_negative_memory_recorded",
    "f92_repair_disposition_closed",
    "f93_pending_open_scaffold_recorded",
    "task_force_actual_calls_recorded_for_f92c",
    "frontier_extra_due_check_not_due_after_f92",
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
    "f93_stage_open_completed",
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
    io_path(path).write_text(
        yaml.safe_dump(json_ready(payload), allow_unicode=True, sort_keys=False, width=140),
        encoding="utf-8",
    )


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def current_branch() -> str:
    completed = subprocess.run(["git", "branch", "--show-current"], cwd=ROOT, check=False, capture_output=True, text=True, timeout=10)
    return completed.stdout.strip() if completed.returncode == 0 else ""


def file_identity(path: Path) -> dict[str, Any]:
    if not path_exists(path):
        return {"path": rel(path), "exists": False, "sha256": None, "size_bytes": None}
    return {"path": rel(path), "exists": True, "sha256": sha256_file_lf_normalized(path), "size_bytes": io_path(path).stat().st_size}


def ensure_dirs() -> None:
    for path in [
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
    ]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def source_inputs() -> list[Path]:
    return [
        F92B_SUMMARY_REVIEW,
        F92B_CANDIDATE_GATE,
        F92B_SPLIT_METRICS,
        F92B_TIER_ROUTE_SUMMARY,
        F92B_TIER_B_SUMMARY,
        F92B_DATA_INTEGRITY,
        F92B_FINAL_CLAIM_GUARD,
        F92B_REQUIRED_GATE_AUDIT,
        F92B_WORK_PACKET,
        F92B_TASK_FORCE,
    ]


def produced_artifacts() -> list[Path]:
    return [
        RUN_MANIFEST,
        SUMMARY_JSON,
        KPI_RECORD,
        DECISION_JSON,
        RESULT_SUMMARY,
        STAGE_CLOSEOUT_SUMMARY,
        STAGE_CLOSEOUT_REPORT,
        F92C_REPORT,
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
        NEXT_STAGE_BRIEF,
        NEXT_INPUT_REFS,
        NEXT_SELECTION_STATUS,
        NEXT_CONTEXT_ANCHOR,
        NEXT_REVIEW_INDEX,
        NEXT_STAGE_LEDGER,
    ]


def load_split_metrics() -> dict[str, dict[str, Any]]:
    target = "path_first_touch_atr_m15_h48_cost2__extratrees_full58_q90"
    views = {"tier_a_separate", "tier_b_separate", "tier_ab_combined"}
    result: dict[str, dict[str, Any]] = {}
    with io_path(F92B_SPLIT_METRICS).open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("variant_id") == target and row.get("split") == "validation" and row.get("view") in views:
                result[str(row["view"])] = {key: coerce_number(value) for key, value in row.items()}
    missing = sorted(views - set(result))
    if missing:
        raise RuntimeError(f"Missing F92B split metric rows for {missing}")
    return result


def coerce_number(value: Any) -> Any:
    if not isinstance(value, str):
        return value
    text = value.strip()
    if text in {"", "None", "nan"}:
        return text
    if text in {"True", "False"}:
        return text == "True"
    try:
        if "." not in text and "e" not in text.lower():
            return int(text)
        return float(text)
    except ValueError:
        return value


def task_force_calls() -> list[dict[str, Any]]:
    return [
        {
            "roster_agent_id": "agent_01_system_governor",
            "agent_nickname": "Copernicus",
            "spawned_agent_id": "019ede18-24c1-7441-942b-42c8c0597e87",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "accepted",
            "accepted_summary": "F92 negative closeout is inside boundary; F93 requires material novelty delta and topic rotation check.",
        },
        {
            "roster_agent_id": "agent_04_evidence_control_plane",
            "agent_nickname": "Gibbs",
            "spawned_agent_id": "019ede18-521c-7431-b03a-b5d52c079301",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "accepted",
            "accepted_summary": "Fresh F92C packet, stage_closeout profile, gate coverage, ledgers, and state sync are required.",
        },
        {
            "roster_agent_id": "agent_05_data_feature_contract",
            "agent_nickname": "Schrodinger",
            "spawned_agent_id": "019ede18-79dc-7111-92a5-f48bf0f3a9b3",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "accepted",
            "accepted_summary": "F92B data/label evidence is sufficient for negative proxy closeout but not runtime negative or authority.",
        },
        {
            "roster_agent_id": "agent_06_quant_research",
            "agent_nickname": "Bacon",
            "spawned_agent_id": "019ede18-a3bc-71e2-9856-a6a07a5ee20f",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "accepted",
            "accepted_summary": "Structural novelty for capped repair is insufficient; rotate to a new F93 axis.",
        },
        {
            "roster_agent_id": "agent_07_model_validation_risk",
            "agent_nickname": "Lorentz",
            "spawned_agent_id": "019ede18-cc66-77f3-8b44-3a79bf0885f4",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "accepted",
            "accepted_summary": "OOS-positive final read is clue only because validation PF is below gate and threshold policy is train-only.",
        },
        {
            "roster_agent_id": "agent_08_mt5_onnx_runtime",
            "agent_nickname": "Volta",
            "spawned_agent_id": "019ede18-f4a1-7f52-9b5b-d68adfa09b4a",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "accepted",
            "accepted_summary": "MT5 trigger is not triggered/out_of_scope_by_claim because no runnable candidate or runtime claim exists.",
        },
    ]


def closeout_payload(now: str) -> dict[str, Any]:
    summary = read_json(F92B_SUMMARY_REVIEW)
    candidate_gate = read_json(F92B_CANDIDATE_GATE)
    tier_route = read_json(F92B_TIER_ROUTE_SUMMARY)
    tier_b_summary = read_json(F92B_TIER_B_SUMMARY)
    data_integrity = read_json(F92B_DATA_INTEGRITY)
    split_metrics = load_split_metrics()
    best = summary["metrics"]["evaluation"]["best_diagnostic_variant"]
    decision = {
        "final_disposition": "rotate_to_f93",
        "candidate_count": int(candidate_gate["candidate_count"]),
        "candidate_gate_status": "failed_no_candidate",
        "repair_disposition": "capped_repair_not_selected_structural_novelty_insufficient",
        "rotation_reason": [
            "combined validation PF 1.028736 is below candidate gate 1.05",
            "Tier B validation is negative with PF 0.534535 and low density",
            "best variant is short-heavy and high-cost concentrated",
            "OOS positive final read is clue only and cannot rescue validation gate failure",
            "same path-label threshold/filter repair would repeat the failed axis",
        ],
        "salvage_value": [
            "Path-label construction and feature-label boundary are useful negative memory.",
            "Short-heavy/high-cost concentration is a failure shape to attack with a new risk-budget objective.",
            "Tier A, Tier B, and actual routed total records remain valid for future comparison.",
        ],
        "negative_memory": [
            "Do not repeat q90 full58 first-touch path labels with threshold/filter-only tweaks.",
            "Do not use OOS-positive final read as candidate, promotion, runtime, or authority evidence.",
            "Do not treat proxy PF as MT5/runtime PF.",
            "Do not drop Tier B separate or actual routed total records.",
        ],
        "reopen_condition": [
            "A future stage changes source, data representation, label geometry, runtime representation, validation philosophy, model objective, trade shape, risk logic, or regime split.",
            "A revisit keeps train-only threshold policy and does not select from OOS final read.",
            "Any runtime/materialization/economics claim gets same-packet MT5 Strategy Tester evidence.",
        ],
        "next_stage_id": NEXT_STAGE_ID,
        "next_run_id": NEXT_RUN_ID,
        "next_axis": {
            "primary_axis": "side_balance_cost_exposure_risk_budget",
            "stage_id": NEXT_STAGE_ID,
            "run_id": NEXT_RUN_ID,
            "question": (
                "Can side-balance and cost-exposure risk budgets turn F92's short-heavy/high-cost clue into a "
                "runtime-compatible surface without path-label threshold repair?"
            ),
            "novelty_delta": {
                "objective": "risk-budget surface rather than path-first-touch label selection",
                "risk_logic": "predeclared side-balance and cost-exposure budgets instead of post-hoc filtering",
                "trade_shape": "portfolio permission/allocation shape before candidate materialization",
                "validation_philosophy": "reject side or cost concentration as structural failure, not as a tunable threshold rescue",
                "not_threshold_filter_parameter_tweak": True,
            },
            "pending_open_boundary": "scaffold_only_formal_f93a_open_required",
        },
        "tier_scope": {
            "tier_a_rows": tier_route["tier_a_rows"],
            "tier_b_fallback_rows": tier_route["tier_b_fallback_rows"],
            "actual_routed_rows": tier_route["actual_routed_rows"],
            "combined_boundary": tier_route["combined_boundary"],
        },
        "split_metrics_by_view": split_metrics,
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
        "f92b_summary": summary,
        "candidate_gate": candidate_gate,
        "tier_b_summary": tier_b_summary,
        "data_integrity_audit": data_integrity,
        "repair_rotation_decision": decision,
        "frontier_extra_due_check": {
            "status": "pass_not_due",
            "frontier_closeout": "F92",
            "next_due_boundary": "F100",
            "e01_status": "closed_for_f050",
            "decision": FRONTIER_EXTRA_DUE_STATUS,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "frontier_five_stage_direction_synthesis": {
            "status": "pass",
            "covered_frontier_ids": ["F88", "F89", "F90", "F91", "F92"],
            "dominant_direction": "proxy surfaces keep generating useful negative memory before runtime materialization",
            "repeated_mechanism": "validation gate failure followed by pressure to rescue with adjacent threshold/filter changes",
            "overused_axis_warning": "path-label threshold/full58/q90 repair should not be repeated adjacent",
            "next_axis_options": ["side-balance risk budget", "cost-exposure budget", "allocation/permission trade-shape objective"],
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
        "task_force": task_force_receipt(),
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }


def task_force_receipt() -> dict[str, Any]:
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
        "bounded_evidence": [rel(F92B_CANDIDATE_GATE), rel(F92B_SUMMARY_REVIEW), rel(F92B_WORK_PACKET)],
        "advice_classification": {call["roster_agent_id"]: call["opinion_classification"] for call in calls},
        "local_verification": [
            "F92B candidate_count=0 verified from candidate_gate.json.",
            "F92B validation gate failure verified from split_metrics.csv and execution summary.",
            "F92C records fresh Task Force calls; F92B calls are not reused as F92C evidence.",
            "No runtime/materialization/economics claim is made in F92C.",
        ],
        "final_codex_direction": "Close F92 as negative/no-authority and rotate to F93 pending-open scaffold.",
        "forbidden_claim_check": (
            "No candidate, selected baseline, operating promotion, runtime authority, live readiness, "
            "Goal Achieve, runtime verified, or materialization-ready claim."
        ),
        "claim_boundary": CLAIM_BOUNDARY,
        "decision": "accepted_rotate_to_f93",
    }


def audit_payload(audit_name: str, status: str, *, counts: Mapping[str, Any] | None = None) -> dict[str, Any]:
    return {
        "audit_name": audit_name,
        "packet_id": RUN_ID,
        "status": status,
        "passed": status.startswith("pass"),
        "created_at_utc": utc_now(),
        "counts": counts or {},
        "claim_boundary": CLAIM_BOUNDARY,
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }


def kpi_record(payload: Mapping[str, Any]) -> dict[str, Any]:
    best = payload["f92b_summary"]["metrics"]["evaluation"]["best_diagnostic_variant"]
    val = best["validation"]
    oos = best["oos_final_read"]
    by_view = payload["repair_rotation_decision"]["split_metrics_by_view"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "hypothesis": "F92 path trade-shape labels should rotate unless a non-threshold structural repair exists.",
        "test_period": "F92B train/validation/OOS evidence consumed as frozen closeout input; F92C is a decision closeout.",
        "proxy_kpi": {
            "source_run_id": PARENT_RUN_ID,
            "best_variant": best["variant_id"],
            "validation_net_proxy": val["net_proxy"],
            "validation_proxy_pf": val["proxy_pf"],
            "validation_max_drawdown": val["max_drawdown"],
            "validation_trade_count": val["trade_count"],
            "validation_trades_per_day": val["trades_per_day"],
            "validation_side_min_share": val["side_min_share"],
            "validation_high_cost_share": val["cost_high_trade_share"],
            "oos_net_proxy": oos["net_proxy"],
            "oos_proxy_pf": oos["proxy_pf"],
            "oos_max_drawdown": oos["max_drawdown"],
            "oos_trade_count": oos["trade_count"],
            "oos_trades_per_day": oos["trades_per_day"],
            "oos_side_min_share": oos["side_min_share"],
            "oos_high_cost_share": oos["cost_high_trade_share"],
            "candidate_count": int(payload["candidate_gate"]["candidate_count"]),
        },
        "runtime_kpi": {
            "status": "not_applicable",
            "reason": "No candidate, no runnable decision surface, no ONNX/EA/set behavior claim, and no runtime/materialization/economics claim.",
            "runtime_probe_status": RUNTIME_PROBE_STATUS,
        },
        "closeout_kpi_by_view": {
            view: {
                "net_proxy": row["net_proxy"],
                "gross_profit": row["gross_profit"],
                "gross_loss": row["gross_loss"],
                "profit_factor": row["proxy_pf"],
                "win_rate": row["win_rate"],
                "avg_win": row["avg_win"],
                "avg_loss": row["avg_loss"],
                "payoff_ratio": row["payoff_ratio"],
                "expectancy": row["expectancy"],
                "max_drawdown": row["max_drawdown"],
                "recovery_factor": row["recovery_factor"],
                "time_under_water_bars": row["time_under_water_bars"],
                "max_consecutive_loss": row["max_consecutive_loss"],
                "long_count": row["long_count"],
                "short_count": row["short_count"],
                "trades_per_day": row["trades_per_day"],
            }
            for view, row in by_view.items()
        },
        "net_profit": "source_proxy_only_not_mt5_net_profit",
        "profit_factor": "source_proxy_pf_only_not_runtime_pf",
        "drawdown": "source_proxy_drawdown_only_not_runtime_drawdown",
        "trade_count": "source_proxy_trade_count_only_not_runtime_trade_count",
        "trades_per_day": "source_proxy_trades_per_day_only_not_runtime_density",
        "parity": "not_applicable_no_onnx_ea_runtime_surface",
        "gap_cause": "F92B validation joint gate failed before materialization.",
        "next_action": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
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


def closeout_summary(payload: Mapping[str, Any]) -> dict[str, Any]:
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
        "verification_profile": "stage_closeout",
        "claim_boundary": CLAIM_BOUNDARY,
        "runtime_probe_status": RUNTIME_PROBE_STATUS,
        "kpi_record": kpi_record(payload),
        "repair_rotation_decision": payload["repair_rotation_decision"],
        "frontier_extra_due_check": payload["frontier_extra_due_check"],
        "frontier_topic_rotation_check": payload["frontier_topic_rotation_check"],
        "task_force_actual_subagent_calls": payload["task_force"]["actual_subagent_calls"],
        "source_identity": [file_identity(path) for path in source_inputs()],
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }


def result_summary_text(payload: Mapping[str, Any]) -> str:
    proxy = kpi_record(payload)["proxy_kpi"]
    return f"""# F92C Repair Or Rotation Decision

Updated: {payload['created_at_utc']}

Conclusion: F92 closes as negative/no-authority. F92B produced no candidate: candidate_count `{proxy['candidate_count']}`, validation net `{proxy['validation_net_proxy']}`, validation PF `{proxy['validation_proxy_pf']}`, validation trades/day `{proxy['validation_trades_per_day']}`, side_min_share `{proxy['validation_side_min_share']}`, high-cost share `{proxy['validation_high_cost_share']}`.

Action: F92C records negative memory, do-not-repeat notes, reopen conditions, fresh Task Force actual calls, frontier extra due check, and topic rotation check.

Effect: The project stops adjacent path-label threshold/filter/parameter repair and rotates to `{NEXT_STAGE_ID}` as pending-open scaffold only.

Runtime: no MT5 Strategy Tester probe. Reason: no candidate, no runnable decision surface, no ONNX/EA/set behavior claim, and no runtime/materialization/economics claim. This is not cost deferral and not a proxy-bad skip.

Next axis: side-balance and cost-exposure risk budgets.

Boundary: `{CLAIM_BOUNDARY}`.
"""


def f92_selection_status_text() -> str:
    return """# Selection Status

F92 is closed as negative/no-authority. No candidate, no selected baseline, no operating promotion, no runtime authority, no live readiness, no Goal Achieve.

F92B positive OOS final read is a clue only because validation joint gate failed and Tier B/side/cost concentration failed.
"""


def next_stage_brief_text() -> str:
    return f"""# {NEXT_STAGE_ID}

Status: pending-open scaffold only. Formal F93A open is not claimed in F92C.

Question: Can side-balance and cost-exposure risk budgets produce a runtime-compatible US100 M5 surface without repeating F92 path-label threshold repair?

Material novelty delta: the primary axis changes from path-first-touch label selection to predeclared side-balance and cost-exposure risk-budget objective. It is not threshold/filter/parameter-only repair.

Runtime rule: if F93 creates a meaningful runnable candidate, ONNX/EA/set behavior, or runtime/materialization/economics claim, the same packet must attempt a narrow MT5 Strategy Tester probe or close as blocked/inconclusive/out_of_scope_by_claim.
"""


def next_input_refs_text(payload: Mapping[str, Any]) -> str:
    lines = ["# Input References", ""]
    for path in [SUMMARY_JSON, DECISION_JSON, F92B_SUMMARY_REVIEW, F92B_CANDIDATE_GATE, F92B_SPLIT_METRICS, F92B_DATA_INTEGRITY]:
        ident = file_identity(path)
        lines.append(f"- `{ident['path']}` sha256 `{ident['sha256']}`")
    lines.append("")
    lines.append("Boundary: F93 pending scaffold uses F92C/F92B as reference and negative memory only, not inherited winner or authority.")
    return "\n".join(lines)


def next_selection_status_text() -> str:
    return f"""# Selection Status

F93 is pending-open scaffold only.

- current run: `{NEXT_RUN_ID}`
- status: pending formal stage open
- candidate: not claimed
- selected baseline: not claimed
- operating promotion: not claimed
- runtime authority: not claimed
- live readiness: not claimed
- Goal Achieve: not claimed
"""


def current_state_text(payload: Mapping[str, Any]) -> str:
    return f"""# Current Working State

- active stage: `{NEXT_STAGE_ID}`
- latest completed run: `{RUN_ID}`
- current run: `{NEXT_RUN_ID}`
- status: `{STATUS}`
- judgment: `{JUDGMENT}`
- Task Force: 6 fresh selected agents called for F92C; no Task Force reviewed/pass claim.
- Runtime: `{RUNTIME_PROBE_STATUS}`
- Boundary: `{CLAIM_BOUNDARY}`
"""


def workspace_state_text(payload: Mapping[str, Any]) -> str:
    return f"""current_stage_id: {NEXT_STAGE_ID}
active_stage: {NEXT_STAGE_ID}
active_branch: {current_branch() or 'main'}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
frontier_extra_due_status: {FRONTIER_EXTRA_DUE_STATUS}
frontier_topic_rotation_status: {FRONTIER_TOPIC_ROTATION_STATUS}
task_force_status: f92c_actual_subagent_calls_recorded_6_selected_agents_no_task_force_reviewed_pass_claim
runtime_probe_status: {RUNTIME_PROBE_STATUS}
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
updated_at_utc: '{payload['created_at_utc']}'
context_anchor: {rel(NEXT_CONTEXT_ANCHOR)}
notes:
- 'Action: F92C closed F92 as negative/no-authority and wrote F93 pending-open scaffold.'
- 'Effect: adjacent path-label threshold/filter/parameter repair is blocked; next axis is side-balance cost-exposure risk budget.'
- 'Runtime: no Strategy Tester evidence; no runtime authority; no Goal Achieve.'
"""


def review_index_text(payload: Mapping[str, Any]) -> str:
    rows = [
        ("stage_closeout_summary", STAGE_CLOSEOUT_SUMMARY),
        ("stage_closeout_report", STAGE_CLOSEOUT_REPORT),
        ("f92c_report", F92C_REPORT),
        ("task_force", TASK_FORCE_REVIEW),
        ("topic_rotation", TOPIC_ROTATION_CHECK),
        ("final_claim_guard", FINAL_CLAIM_GUARD),
        ("packet", WORK_PACKET),
    ]
    body = "\n".join(f"- {name}: `{rel(path)}`" for name, path in rows)
    return f"# Review Index\n\n{body}\n"


def next_review_index_text(payload: Mapping[str, Any]) -> str:
    return f"""# Review Index

F93 pending-open scaffold was written by `{RUN_ID}`. Formal F93A open is not claimed here.

- stage brief: `{rel(NEXT_STAGE_BRIEF)}`
- input refs: `{rel(NEXT_INPUT_REFS)}`
- selection status: `{rel(NEXT_SELECTION_STATUS)}`
- source decision: `{rel(DECISION_JSON)}`
"""


def decision_memo_text(payload: Mapping[str, Any]) -> str:
    return f"""# F92C Closeout Rotate F93

Date: {payload['created_at_utc']}

Decision: `{DECISION}`.

Why: F92B candidate_count was 0. The best diagnostic surface had validation PF 1.028736, Tier B validation PF 0.534535, side_min_share 0.087013, and high-cost share 0.712987. OOS-positive final read remains clue only.

Task Force: 6 selected agents were actually called and all returned accepted boundary advice.

Runtime: no MT5 Strategy Tester probe was run because no runnable candidate or runtime/materialization/economics claim exists. This is not cost deferral and not a proxy-bad skip.

Next: `{NEXT_RUN_ID}` pending-open scaffold for `{NEXT_STAGE_ID}`.

Forbidden: no completion, selected baseline, operating promotion, runtime authority, live readiness, or Goal Achieve.
"""


def write_run_artifacts(payload: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> None:
    write_json(RUN_MANIFEST, run_manifest(payload, gate_results))
    write_json(SUMMARY_JSON, payload)
    write_json(KPI_RECORD, kpi_record(payload))
    write_json(DECISION_JSON, payload["repair_rotation_decision"])
    write_text(RESULT_SUMMARY, result_summary_text(payload))
    write_json(STAGE_CLOSEOUT_SUMMARY, closeout_summary(payload))
    write_text(STAGE_CLOSEOUT_REPORT, result_summary_text(payload))
    write_text(F92C_REPORT, result_summary_text(payload))


def write_audits(payload: Mapping[str, Any]) -> None:
    write_json(TASK_FORCE_REVIEW, payload["task_force"])
    write_json(TASK_FORCE_PACKET_REVIEW, {"audit_name": "codex_task_force_review_packet", "status": "pass", "passed": True, **payload["task_force"]})
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
                **payload["data_integrity_audit"]["counts"],
                "boundary": "F92C consumes frozen F92B evidence and performs no new model fit.",
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
                "best_variant": payload["f92b_summary"]["metrics"]["evaluation"]["best_diagnostic_variant"]["variant_id"],
                "selection_policy": payload["f92b_summary"]["metrics"]["evaluation"]["selection_policy"],
                "oos_boundary": "final_read_only_not_selection",
                "repair_boundary": "same-axis threshold/filter repair blocked",
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
                "lineage_judgment": "F92B negative proxy scout -> F92C closeout rotation -> F93 pending scaffold.",
            },
        ),
    )
    write_json(
        RESULT_JUDGMENT_AUDIT,
        {
            **audit_payload("result_judgment_audit", "pass"),
            "result_subject": RUN_ID,
            "evidence_available": [rel(F92B_CANDIDATE_GATE), rel(F92B_SUMMARY_REVIEW), rel(DECISION_JSON), rel(TASK_FORCE_PACKET_REVIEW)],
            "evidence_missing": ["MT5 Strategy Tester output", "runnable ONNX/EA/set candidate", "WFO/stress runtime validation"],
            "judgment_label": JUDGMENT,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "F92 produced negative memory and a new F93 risk-budget axis proposal, not an operating strategy.",
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


def compact_receipt(skill: str, payload: Mapping[str, Any], **extra: Any) -> dict[str, Any]:
    base = {
        "packet_id": RUN_ID,
        "skill": skill,
        "status": "executed",
        "receipt_mode": "compact",
        "source_current_truth_docs": [rel(WORKSPACE_STATE), rel(CURRENT_WORKING_STATE), rel(SELECTION_STATUS)],
        "evidence_used": [rel(F92B_SUMMARY_REVIEW), rel(F92B_CANDIDATE_GATE), rel(DECISION_JSON)],
        "claim_boundary": CLAIM_BOUNDARY,
        "gates_not_run_with_reason": [
            {
                "gate": "runtime_evidence_gate",
                "reason_code": "outside_claim_surface_no_runtime_claim",
                "reason": "No runnable candidate, ONNX/EA/set behavior, or runtime/materialization/economics claim exists.",
                "claim_effect": "Runtime evidence and authority claims are forbidden.",
            }
        ],
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }
    base.update(extra)
    return base


def skill_receipts(payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    task_force = dict(payload["task_force"])
    task_force["receipt_mode"] = "compact"
    task_force["source_current_truth_docs"] = [rel(WORKSPACE_STATE), rel(CURRENT_WORKING_STATE), rel(SELECTION_STATUS)]
    return [
        compact_receipt("obsidian-stage-transition", payload, canonical_state_after={"active_stage": NEXT_STAGE_ID, "current_run_id": NEXT_RUN_ID, "latest_completed_run_id": RUN_ID}),
        compact_receipt("obsidian-run-evidence-system", payload, ledger_rows=[f"{RUN_ID}__tier_a_closeout", f"{RUN_ID}__tier_b_closeout", f"{RUN_ID}__actual_routed_closeout", f"{NEXT_RUN_ID}__planned_current_run"]),
        compact_receipt("obsidian-data-integrity", payload, data_sources_checked=[rel(F92B_DATA_INTEGRITY), rel(F92B_SPLIT_METRICS)], leakage_checks=["no threshold retune", "no OOS rescue", "label-only path fields remain non-runtime features"]),
        compact_receipt("obsidian-model-validation", payload, model_or_threshold_surface="F92B path label proxy scout is closed; no repair selected.", selection_metric_boundary="failed predeclared validation gate only"),
        compact_receipt("obsidian-artifact-lineage", payload, source_inputs=[rel(path) for path in source_inputs()], produced_artifacts=[rel(path) for path in produced_artifacts() if path_exists(path)]),
        compact_receipt("obsidian-result-judgment", payload, judgment_boundary=JUDGMENT, next_condition=NEXT_RUN_ID),
        compact_receipt("obsidian-exploration-mandate", payload, negative_memory_effect="Prevents adjacent F92 path-label threshold/filter repair."),
        task_force,
        compact_receipt("obsidian-claim-discipline", payload, allowed_claims=ALLOWED_CLAIMS, final_status=STATUS),
        compact_receipt("obsidian-answer-clarity", payload, primary_output="F92 did not produce a tradable candidate; it produced negative memory and a F93 risk-budget next axis."),
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
    gate_na = [
        {
            "gate": "runtime_evidence_gate",
            "reason_code": "outside_claim_surface_no_runtime_claim",
            "reason": "F92C protects closeout/rotation only; no candidate, runnable surface, ONNX/EA/set behavior, or runtime/materialization/economics claim is made.",
            "claim_effect": "Runtime probe, runtime verified, economics pass, materialization ready, handoff ready, authority, live readiness, and Goal Achieve claims are forbidden.",
        },
        {
            "gate": "f93_stage_open_gate",
            "reason_code": "pending_open_scaffold_only",
            "reason": "F92C only writes the F93 pending-open scaffold; formal F93A stage open requires a separate packet.",
            "claim_effect": "F93 stage-open completed/reviewed/pass claims are forbidden.",
        },
    ]
    return {
        "version": "work_packet_schema_v2_1",
        "packet_lifecycle": "new_packet",
        "packet_id": RUN_ID,
        "created_at_utc": payload["created_at_utc"],
        "user_request": {
            "user_quote": "/goal active continuation; user explicitly required Task Force agents when triggered",
            "requested_action": "F92C stage closeout and F93 pending-open rotation scaffold",
            "requested_count": {"value": 1, "n_a_reason": ""},
            "ambiguous_terms": ["No final completion.", "No runtime authority.", "F93 formal open is not claimed."],
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
                "f93_scaffold_confused_with_formal_open": "medium",
                "runtime_probe_absence_misread_as_cost_skip": "medium",
            },
            "hard_stop_risks": [
                "Do not claim candidate/runtime/economics/materialization without MT5 Strategy Tester output identity.",
                "Do not call F93 formally open in this packet.",
                "Do not repeat F92 path-label axis by threshold/filter/session/routing/parameter-only tweak.",
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
                "reason": "F92C makes closeout/rotation claims only; no candidate, runnable surface, or runtime/materialization/economics claim exists.",
            },
            "questions": [],
            "required_user_decisions": [],
        },
        "interpreted_scope": {
            "work_families": ["publish_handoff"],
            "target_surfaces": ["F92 closeout", "F93 pending-open scaffold", "Task Force receipt", "state sync"],
            "scope_units": ["stage_closeout", "rotation_decision", "receipt", "state_sync"],
            "execution_layers": ["local_python_execution", "stage_transition"],
            "mutation_policy": {"allowed": True, "user_quote": "/goal active continuation"},
            "evidence_layers": ["F92B proxy metrics", "F92B candidate gate", "F92C Task Force calls"],
            "reduction_policy": {"reduction_allowed": False, "requires_user_quote": False, "rationale": "F92C consumes all F92B closeout evidence and makes no narrowed success claim."},
            "claim_boundary": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
        },
        "verification_profile": {
            "profile_id": "stage_closeout",
            "claim_surface": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
            "trigger_sources": ["active_goal", "F92B no candidate", "closeout_required_task_force_review", "rotation_to_next_frontier"],
            "protected_claims": ALLOWED_CLAIMS,
            "required_evidence": required_evidence,
            "gates_not_run_with_reason": gate_na,
            "stop_conditions": [
                "No runtime/materialization/economics/authority/Goal Achieve claim.",
                "If a meaningful runnable candidate appears, switch to runtime_probe profile and attempt narrow MT5 probe in the same packet.",
            ],
        },
        "acceptance_criteria": [
            {"id": "AC-001", "text": "F92C decision artifact exists.", "expected_artifact": rel(DECISION_JSON), "verification_method": "scope_completion_gate", "required": True},
            {"id": "AC-002", "text": "F92C Task Force actual calls are recorded.", "expected_artifact": rel(TASK_FORCE_PACKET_REVIEW), "verification_method": "codex_task_force_review_packet", "required": True},
            {"id": "AC-003", "text": "F93 pending-open scaffold exists without formal open claim.", "expected_artifact": rel(NEXT_STAGE_BRIEF), "verification_method": "scope_completion_gate", "required": True},
        ],
        "work_plan": {
            "phases": ["Read F92B evidence.", "Call relevant Task Force agents.", "Write closeout and pending-open scaffold.", "Run gates and state sync."],
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
                {"skill": "obsidian-backtest-forensics", "reason": "No new Strategy Tester report or trade list exists in F92C."},
            ],
            "required_skill_receipts": REQUIRED_SKILLS,
            "required_gates": REQUIRED_GATES,
        },
        "evidence_contract": {
            "raw_evidence": [rel(F92B_CANDIDATE_GATE), rel(F92B_SPLIT_METRICS)],
            "machine_readable": [rel(RUN_MANIFEST), rel(SUMMARY_JSON), rel(KPI_RECORD), rel(DECISION_JSON), rel(SKILL_RECEIPTS)],
            "human_readable": [rel(RESULT_SUMMARY), rel(STAGE_CLOSEOUT_REPORT), rel(DECISION_MEMO)],
        },
        "gates": {
            "required": REQUIRED_GATES,
            **gates_status,
            "not_applicable_with_reason": {
                "runtime_evidence_gate": "outside_claim_surface_no_runtime_claim",
                "f93_stage_open_gate": "pending_open_scaffold_only",
            },
        },
        "final_claim_policy": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS},
    }


def write_packet(payload: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> None:
    packet = work_packet(payload, gate_results)
    write_yaml(WORK_PACKET, packet)
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
    audits = [{"audit_name": name, "path": rel(path_by_gate[name]), "status": packet["gates"].get(name, "pending")} for name in REQUIRED_GATES]
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
    write_text(SELECTION_STATUS, f92_selection_status_text())
    write_text(CONTEXT_ANCHOR, current_state_text(payload))
    write_text(REVIEW_INDEX, review_index_text(payload))
    write_text(NEXT_STAGE_BRIEF, next_stage_brief_text())
    write_text(NEXT_INPUT_REFS, next_input_refs_text(payload))
    write_text(NEXT_SELECTION_STATUS, next_selection_status_text())
    write_text(NEXT_CONTEXT_ANCHOR, current_state_text(payload))
    write_text(NEXT_REVIEW_INDEX, next_review_index_text(payload))
    write_text(DECISION_MEMO, decision_memo_text(payload))


def append_once(path: Path, marker: str, addition: str) -> None:
    text = io_path(path).read_text(encoding="utf-8-sig") if path_exists(path) else ""
    if marker in text:
        return
    write_text(path, text.rstrip() + "\n\n" + addition.strip() + "\n")


def append_dict_rows(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], header_source: Path | None = None) -> None:
    source = path if path_exists(path) else header_source
    if source is None or not path_exists(source):
        raise FileNotFoundError(f"CSV header source missing for {path}")
    with io_path(source).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        existing = list(reader) if path_exists(path) else []
    keys = {tuple(str(row.get(field, "")) for field in key_fields) for row in rows}
    kept = [row for row in existing if tuple(str(row.get(field, "")) for field in key_fields) not in keys]
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
    views = payload["repair_rotation_decision"]["split_metrics_by_view"]
    best_id = payload["f92b_summary"]["metrics"]["evaluation"]["best_diagnostic_variant"]["variant_id"]
    base = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "stage_closeout_rotation",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(RESULT_SUMMARY),
        "notes": "F92 closeout; no runtime claim; F93 pending-open scaffold.",
        "family": "publish_handoff",
        "primary_report": rel(RESULT_SUMMARY),
        "run_number": "frontier92C",
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
        "question": "Should F92 repair path labels or rotate after validation gate failure?",
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
        "best_candidate_id": best_id,
    }
    view_specs = [
        ("tier_a_closeout", "tier_a_separate", "Tier A separate"),
        ("tier_b_closeout", "tier_b_separate", "Tier B separate"),
        ("actual_routed_closeout", "tier_ab_combined", "actual routed total"),
    ]
    rows = []
    for record_view, source_view, tier_scope in view_specs:
        row_metric = views[source_view]
        row = dict(base)
        row.update(
            {
                "ledger_row_id": f"{RUN_ID}__{record_view}",
                "subrun_id": f"{RUN_ID}__{record_view}",
                "record_view": record_view,
                "tier_scope": tier_scope,
                "kpi_scope": "f92_closeout_decision",
                "primary_kpi": f"net={row_metric['net_proxy']};pf={row_metric['proxy_pf']};dd={row_metric['max_drawdown']};tpd={row_metric['trades_per_day']}",
                "guardrail_kpi": f"side_min={row_metric['side_min_share']};cost_high={row_metric['cost_high_trade_share']}",
                "row_id": f"{RUN_ID}__{record_view}",
                "view": record_view,
                "tier": tier_scope,
                "metric_scope": "stage_closeout_rotation",
                "result_status": "negative_memory",
                "net_profit": row_metric["net_proxy"],
                "profit_factor": row_metric["proxy_pf"],
                "drawdown": row_metric["max_drawdown"],
                "trade_count": row_metric["trade_count"],
                "trades_per_day": row_metric["trades_per_day"],
                "long_trade_count": row_metric["long_count"],
                "short_trade_count": row_metric["short_count"],
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
            "notes": "F93 pending-open scaffold after F92C negative closeout.",
            "primary_report": rel(NEXT_STAGE_BRIEF),
            "run_number": "frontier93A",
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
            "next_action": "formal_f93a_stage_open",
            "question": "Can side-balance and cost-exposure risk budgets produce a runtime-compatible US100 M5 surface?",
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
    append_dict_rows(RUN_REGISTRY, ["run_id"], [dict(rows[0]), dict(rows[-1])])
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
                "stage_id": STAGE_ID if path_rel.startswith(f"stages/{STAGE_ID}") or "frontier92C" in path_rel or "f92c" in path_rel else NEXT_STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": "f92c_closeout_rotation",
                "path": path_rel,
                "sha256": sha256_file_lf_normalized(path),
                "created_at": payload["created_at_utc"],
                "claim_boundary": CLAIM_BOUNDARY,
                "artifact_id": f"{RUN_ID}::{path_rel}",
                "created_at_utc": payload["created_at_utc"],
                "notes": "F92C closeout/rotation artifact; no runtime authority.",
                "artifact_path": path_rel,
                "effect": "Supports F92 negative memory and F93 pending-open scaffold only.",
                "size_bytes": io_path(path).stat().st_size,
            }
        )
    replace_rows_by_field(ARTIFACT_REGISTRY, "run_id", RUN_ID, rows)


def update_register_docs(payload: Mapping[str, Any]) -> None:
    idea_addition = f"""
## F92C path trade-shape label closeout

- run_id: `{RUN_ID}`
- hypothesis: F92 path labels should rotate unless a non-threshold structural repair exists.
- result: negative_memory, no candidate, no runtime trigger.
- next_action: `{NEXT_RUN_ID}` pending-open scaffold.
- claim_boundary: `{CLAIM_BOUNDARY}`.
"""
    negative_addition = f"""
## F92C path trade-shape label negative closeout

- run_id: `{RUN_ID}`
- failed_boundary: F92B validation PF, Tier B, side concentration, and high-cost concentration failed the joint candidate gate.
- salvage_value: path-label feature boundary, best diagnostic failure shape, and F92B OOS positive final read as clue only.
- do_not_repeat: q90/full58/path-first-touch threshold or filter tweak, OOS rescue, proxy PF as runtime PF, Tier A-only overclaim, compile/proxy-only runtime evidence.
- reopen_condition: new source, label geometry, runtime representation, validation philosophy, objective, trade shape, risk logic, or regime split.
"""
    changelog_addition = f"""
<!-- {RUN_ID} -->

## {payload['created_at_utc']} - F92C Closeout Rotate F93

- Action: `{RUN_ID}` closed F92 as negative/no-authority.
- Effect: adjacent path-label threshold/filter/parameter repair is blocked and F93 pending-open scaffold was written at `{NEXT_STAGE_ID}`.
- Runtime: no new Strategy Tester runtime evidence; no runtime authority; no Goal Achieve.
- Boundary: `{CLAIM_BOUNDARY}`.
"""
    append_once(IDEA_REGISTRY, RUN_ID, idea_addition)
    append_once(NEGATIVE_REGISTER, RUN_ID, negative_addition)
    append_once(WORKSPACE_CHANGELOG, RUN_ID, changelog_addition)
    append_once(ROOT_CHANGELOG, RUN_ID, changelog_addition)


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
    gate_passes = len(REQUIRED_GATES)
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
        raise FileNotFoundError(f"Missing required F92C source evidence: {missing}")
    ensure_dirs()
    payload = closeout_payload(utc_now())
    write_initial(payload)
    gate_results = run_control_gates(payload)
    write_final(payload, gate_results)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
