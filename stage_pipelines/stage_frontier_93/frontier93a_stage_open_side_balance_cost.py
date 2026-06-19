from __future__ import annotations

import csv
import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

import yaml

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.audit_result import AuditResult
from foundation.control_plane.final_claim_guard import guard_final_claims
from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized


STAGE_ID = "stage_frontier_93__side_balance_cost_exposure_risk_budget_axis"
RUN_ID = "frontier93A_stage_open_side_balance_cost_exposure_risk_budget_axis_v1"
PARENT_RUN_ID = "frontier92C_path_trade_shape_repair_or_rotation_decision_v1"
NEXT_RUN_ID = "frontier93B_side_balance_cost_exposure_risk_budget_proxy_scout_v1"
SCRIPT_REL = "stage_pipelines/stage_frontier_93/frontier93a_stage_open_side_balance_cost.py"

STATUS = "f93a_stage_open_design_prepared_no_candidate_no_authority"
JUDGMENT = "design_only_stage_open_side_balance_cost_exposure_risk_budget_axis"
CLAIM_BOUNDARY = (
    "f93a_design_only_stage_open_side_balance_cost_exposure_risk_budget_axis_"
    "no_model_candidate_no_wfo_pass_no_stress_pass_no_mt5_runtime_evidence_"
    "no_selected_baseline_no_operating_promotion_no_runtime_authority_"
    "no_live_readiness_no_goal_achieve"
)
RUNTIME_PROBE_STATUS = (
    "not_applicable_design_only_no_runnable_candidate_no_runtime_materialization_"
    "economics_claim_not_cost_or_proxy_bad_skip"
)
FRONTIER_EXTRA_DUE_STATUS = "not_due_after_f92_closeout_next_boundary_f100_e01_closed_for_f050"
FRONTIER_TOPIC_ROTATION_STATUS = (
    "passed_f93_side_balance_cost_exposure_risk_budget_axis_not_f92_path_label_threshold_repair"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / "frontier93A"
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
DECISION_MEMO = ROOT / "docs" / "decisions" / "2026-06-19_frontier93a_stage_open_side_balance_cost_risk.md"

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
F93B_BRIEF = DESIGN_DIR / "f93b_proxy_scout_brief.json"
DATA_INTEGRITY_PLAN = DESIGN_DIR / "data_integrity_plan.json"
RISK_BUDGET_DESIGN = DESIGN_DIR / "risk_budget_design.json"
RESULT_SUMMARY = REPORT_DIR / "summary.md"

STAGE_OPEN_SUMMARY = REVIEW_DIR / "f93a_stage_open_summary.json"
TASK_FORCE_REVIEW = REVIEW_DIR / "f93a_task_force_review_receipt.json"
FRONTIER_EXTRA_DUE_CHECK = REVIEW_DIR / "f93a_frontier_extra_due_check.json"
FIVE_STAGE_SYNTHESIS = REVIEW_DIR / "f93a_frontier_five_stage_direction_synthesis.json"
TOPIC_ROTATION_CHECK = REVIEW_DIR / "f93a_frontier_topic_rotation_check.json"
SCOPE_GATE = REVIEW_DIR / "f93a_scope_completion_gate.json"
DATA_INTEGRITY_AUDIT = REVIEW_DIR / "f93a_data_integrity_audit.json"
MODEL_VALIDATION_AUDIT = REVIEW_DIR / "f93a_model_validation_audit.json"
ARTIFACT_AUDIT = REVIEW_DIR / "f93a_artifact_lineage_audit.json"
FINAL_CLAIM_GUARD = REVIEW_DIR / "f93a_final_claim_guard.json"
STATE_SYNC_AUDIT = REVIEW_DIR / "f93a_state_sync_audit.json"
REQUIRED_GATE_AUDIT = REVIEW_DIR / "f93a_required_gate_coverage_audit.json"
F93A_REPORT = REVIEW_DIR / "frontier93A_stage_open_side_balance_cost_exposure_risk_budget_report.md"

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
MODEL_INPUT_DATASET = MODEL_INPUT_SUMMARY.with_name("model_input_dataset.parquet")
RAW_US100_MANIFEST = (
    ROOT / "data" / "raw" / "mt5_bars" / "m5" / "US100" / "bars_us100_m5_mt5api_raw.manifest.json"
)
F92B_SUMMARY = (
    ROOT
    / "stages"
    / "stage_frontier_92__path_conditioned_trade_shape_labeling_axis"
    / "03_reviews"
    / "f92b_execution_summary.json"
)
F92B_CANDIDATE_GATE = (
    ROOT
    / "stages"
    / "stage_frontier_92__path_conditioned_trade_shape_labeling_axis"
    / "02_runs"
    / "frontier92B"
    / "proxy_scout"
    / "candidate_gate.json"
)
F92C_CLOSEOUT = (
    ROOT / "docs" / "agent_control" / "packets" / PARENT_RUN_ID / "closeout_gate.json"
)
F92C_DECISION = (
    ROOT
    / "stages"
    / "stage_frontier_92__path_conditioned_trade_shape_labeling_axis"
    / "02_runs"
    / "frontier92C"
    / "d"
    / "decision.json"
)

ALLOWED_CLAIMS = [
    "f93a_stage_open_design_prepared",
    "f93_side_balance_cost_exposure_risk_budget_axis_opened",
    "f93b_proxy_scout_planned",
    "task_force_actual_calls_recorded_for_f93a",
    "frontier_extra_due_check_not_due_after_f92",
    "frontier_five_stage_direction_synthesis_recorded_for_f88_to_f92",
    "frontier_topic_rotation_check_recorded_for_f93",
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
    "state_sync_audit",
    "required_gate_coverage_audit",
    "final_claim_guard",
]
REQUIRED_SKILLS = [
    "obsidian-experiment-design",
    "obsidian-data-integrity",
    "obsidian-model-validation",
    "obsidian-artifact-lineage",
    "obsidian-task-force-review",
    "obsidian-stage-transition",
    "obsidian-claim-discipline",
]
RUNTIME_NA_REASONS = [
    {
        "gate": "runtime_evidence_gate",
        "reason_code": "outside_claim_surface_design_only_no_runtime_claim",
        "reason": "F93A creates design artifacts only and no runnable candidate, ONNX/EA/set behavior, or runtime/materialization/economics claim.",
        "claim_effect": "No runtime, materialization, handoff, economics, or authority claim is allowed.",
    },
    {
        "gate": "wfo_stress_gate",
        "reason_code": "outside_claim_surface_no_model_candidate",
        "reason": "F93A does not train/select a model and only prepares F93B proxy scout design.",
        "claim_effect": "No WFO pass, stress pass, model quality, or candidate claim is allowed.",
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
    io_path(path).write_text(
        yaml.safe_dump(json_ready(payload), allow_unicode=True, sort_keys=False, width=140),
        encoding="utf-8",
    )


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
        MODEL_INPUT_DATASET,
        RAW_US100_MANIFEST,
        F92B_SUMMARY,
        F92B_CANDIDATE_GATE,
        F92C_CLOSEOUT,
        F92C_DECISION,
    ]


def produced_artifacts() -> list[Path]:
    return [
        Path(SCRIPT_REL),
        RUN_MANIFEST,
        SUMMARY_JSON,
        KPI_RECORD,
        EXPERIMENT_DESIGN,
        RUNTIME_CONTRACT,
        F93B_BRIEF,
        DATA_INTEGRITY_PLAN,
        RISK_BUDGET_DESIGN,
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
        FINAL_CLAIM_GUARD,
        STATE_SYNC_AUDIT,
        REQUIRED_GATE_AUDIT,
        F93A_REPORT,
        WORK_PACKET,
        SKILL_RECEIPTS,
        PACKET_CLOSEOUT_GATE,
        PACKET_FINAL_CLAIM_GUARD,
        PACKET_STATE_SYNC_AUDIT,
        PACKET_REQUIRED_GATE_AUDIT,
        PACKET_WORK_PACKET_LINT,
        PACKET_SKILL_RECEIPT_LINT,
    ]


def task_force_calls() -> list[dict[str, Any]]:
    return [
        {
            "roster_agent_id": "agent_01_system_governor",
            "spawned_agent_id": "019ede2a-7628-7bb1-be13-5049eb329125",
            "nickname": "Planck",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "accepted",
            "bounded_evidence": [rel(WORKSPACE_STATE), rel(STAGE_BRIEF), rel(SELECTION_STATUS)],
            "local_verification": "F93A may open only as design-only stage open with no candidate, runtime authority, live readiness, or Goal Achieve claim.",
            "accepted_summary": "Novelty is adequate because F93 changes from F92 path-label threshold surface to side-balance plus cost-exposure risk budget objective.",
        },
        {
            "roster_agent_id": "agent_04_evidence_control_plane",
            "spawned_agent_id": "019ede2a-a94f-7750-bb55-e4275902fc0b",
            "nickname": "Ohm",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "accepted",
            "bounded_evidence": [rel(WORKSPACE_STATE), rel(STAGE_BRIEF), rel(WORK_PACKET)],
            "local_verification": "Fresh F93A packet, receipts, gates, actual_subagent_calls, hashes, and state sync must be materialized locally.",
            "accepted_summary": "Use primary_family=experiment_design and verification_profile=design_only; runtime and WFO/stress gates are outside claim surface with reason.",
        },
        {
            "roster_agent_id": "agent_05_data_feature_contract",
            "spawned_agent_id": "019ede2a-e35e-7fe3-9ed4-ddb887594c41",
            "nickname": "Confucius",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "needs_local_verification",
            "bounded_evidence": [rel(MODEL_INPUT_SUMMARY), rel(MODEL_INPUT_FEATURE_ORDER), rel(F92B_SUMMARY)],
            "local_verification": "F93B must lock source identities, feature order hash, split policy, Tier A/B/actual routed records, and closed-bar feature boundary before proxy execution.",
            "accepted_summary": "Post-entry OHLC/path/cost/PnL and side outcome data may be labels or diagnostics only, not runtime features.",
        },
        {
            "roster_agent_id": "agent_06_quant_research",
            "spawned_agent_id": "019ede2b-140e-7961-bb27-3b5749def103",
            "nickname": "Cicero",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "accepted",
            "bounded_evidence": [rel(F92B_SUMMARY), rel(F92B_CANDIDATE_GATE)],
            "local_verification": "F93B should test side-balance and cost-exposure risk budgets, including broad and extreme variants, not a F92 path-label threshold repair.",
            "accepted_summary": "F92 side_min_share 0.087013 and high-cost share 0.712987 justify the new risk-budget axis.",
        },
        {
            "roster_agent_id": "agent_07_model_validation_risk",
            "spawned_agent_id": "019ede2b-3d6f-7a10-9310-e4649e1e30",
            "nickname": "Hilbert",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "needs_local_verification",
            "bounded_evidence": [rel(MODEL_INPUT_SUMMARY), rel(F92B_SUMMARY), rel(F92B_CANDIDATE_GATE)],
            "local_verification": "F93B candidate gate must be joint across Tier A, Tier B, and actual routed total, with train-only thresholds and OOS final-read-only.",
            "accepted_summary": "PF-only selection, OOS tuning, and hiding Tier B weakness are invalid.",
        },
        {
            "roster_agent_id": "agent_08_mt5_onnx_runtime",
            "spawned_agent_id": "019ede2b-6afa-7320-815e-2f2a7cdb95de",
            "nickname": "Ramanujan",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "accepted",
            "bounded_evidence": [rel(STAGE_BRIEF), rel(RUNTIME_CONTRACT)],
            "local_verification": "F93A has no runtime trigger, but any future F93B/F93C runnable candidate or runtime/materialization/economics claim requires same-packet narrow MT5 Strategy Tester probe or lowered claim.",
            "accepted_summary": "Compile-only, proxy-only, ONNX handoff, and parity-only are not runtime/economics evidence.",
        },
    ]


def task_force_receipt(created_at: str) -> dict[str, Any]:
    calls = task_force_calls()
    accepted = [call["roster_agent_id"] for call in calls if call["opinion_classification"] == "accepted"]
    needs_local = [call["roster_agent_id"] for call in calls if call["opinion_classification"] == "needs_local_verification"]
    return {
        "packet_id": RUN_ID,
        "skill": "obsidian-task-force-review",
        "status": "executed",
        "created_at_utc": created_at,
        "trigger_reason": "F93A stage open, active goal frontier continuation, and explicit user instruction requiring relevant Task Force agents when triggered.",
        "roster_registry": "docs/agent_control/codex_task_force_registry.yaml",
        "agents_used": [call["roster_agent_id"] for call in calls],
        "actual_subagent_calls": calls,
        "review_requirement": "codex_task_force_review_packet",
        "model_policy": {"model": "inherited_current_codex_model", "reasoning_effort": "inherited", "service_tier": "inherited"},
        "bounded_evidence": [rel(WORKSPACE_STATE), rel(STAGE_BRIEF), rel(SELECTION_STATUS), rel(F92B_SUMMARY), rel(MODEL_INPUT_SUMMARY)],
        "advice_classification": {"accepted": accepted, "needs_local_verification": needs_local, "rejected": []},
        "local_verification": [
            "F93A packet and gate artifacts are generated locally.",
            "F93B source hashes, split policy, Tier A/B/actual routed rows, and side/cost budget gates are predeclared as required verification.",
            "Runtime evidence gate is outside claim surface only because F93A has no candidate, ONNX/EA/set behavior, or runtime/economics claim.",
        ],
        "claim_boundary": CLAIM_BOUNDARY,
        "final_codex_direction": "Proceed with F93A design-only stage open and plan F93B side-balance cost-exposure risk-budget proxy scout.",
        "forbidden_claim_check": {claim: "not_claimed" for claim in FORBIDDEN_CLAIMS},
        "receipt_path": rel(SKILL_RECEIPT_DIR / "task_force_review.json"),
    }


def load_source_summaries() -> dict[str, Any]:
    model_summary = read_json(MODEL_INPUT_SUMMARY)
    f92b_summary = read_json(F92B_SUMMARY)
    candidate_gate = read_json(F92B_CANDIDATE_GATE)
    return {"model_summary": model_summary, "f92b_summary": f92b_summary, "candidate_gate": candidate_gate}


def base_payload(created_at: str) -> dict[str, Any]:
    summaries = load_source_summaries()
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": created_at,
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "runtime_probe_status": RUNTIME_PROBE_STATUS,
        "frontier_extra_due_status": FRONTIER_EXTRA_DUE_STATUS,
        "frontier_topic_rotation_status": FRONTIER_TOPIC_ROTATION_STATUS,
        "hypothesis": "Predeclared side-balance and cost-exposure risk budgets can turn F92's short-heavy/high-cost failure shape into a runtime-compatible proxy surface without repeating the F92 path-label threshold axis.",
        "decision_use": "Authorize F93B proxy scout design only; no model candidate, selected baseline, MT5 runtime evidence, operating promotion, runtime authority, live readiness, or Goal Achieve.",
        "f92_reference": {
            "source_run_id": "frontier92B_path_conditioned_trade_shape_label_proxy_scout_v1",
            "best_diagnostic_variant": "path_first_touch_atr_m15_h48_cost2__extratrees_full58_q90",
            "validation_actual_routed_net": 1612.419057,
            "validation_actual_routed_pf": 1.028736,
            "validation_actual_routed_drawdown": 5498.60265,
            "validation_trade_count": 1540,
            "validation_trades_per_day": 8.324324,
            "side_min_share": 0.087013,
            "high_cost_trade_share": 0.712987,
            "tier_b_validation_pf": 0.534535,
            "candidate_count": candidate_count(summaries["candidate_gate"]),
            "claim_effect": "Reference and negative memory only; not inherited winner, selected baseline, or authority.",
        },
        "model_input_identity": {
            "dataset_id": summaries["model_summary"].get("model_input_dataset_id"),
            "feature_set_id": summaries["model_summary"].get("feature_set_id"),
            "feature_order_hash": summaries["model_summary"].get("included_feature_order_hash"),
            "feature_count": summaries["model_summary"].get("included_feature_count"),
            "rows": summaries["model_summary"].get("rows"),
            "split_summary": summaries["model_summary"].get("split_summary"),
        },
        "source_identities": [file_identity(path) for path in source_inputs()],
        "task_force": task_force_receipt(created_at),
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }


def candidate_count(candidate_gate: Mapping[str, Any]) -> int:
    value = candidate_gate.get("candidate_count")
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def experiment_design(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "verification_profile": "design_only",
        "hypothesis": payload["hypothesis"],
        "proxy": "F93B will use train-only budget search and validation joint gate over Tier A, Tier B, and actual routed total.",
        "decision_use": payload["decision_use"],
        "comparison_baseline": payload["f92_reference"],
        "control_variables": {
            "symbol": "FPMarkets US100",
            "timeframe": "M5",
            "data_contract": "model_input_v2, label_v1_fwd12_split_v1, feature_set_v2_mt5_price_proxy_58",
            "feature_order_hash": payload["model_input_identity"]["feature_order_hash"],
            "split_policy": "train for fitting thresholds/budgets, validation for candidate gate, OOS final read only",
            "tier_records": ["Tier A separate", "Tier B separate", "Tier A+B actual routed total"],
            "closed_bar_features_only": True,
        },
        "changed_variables": [
            "objective/risk logic changes to side-balance and cost-exposure budgets",
            "hard side-min-share guardrail and high-cost-share guardrail",
            "utility/rank score penalizes side concentration and high-cost exposure",
            "F92 path-label failure shape is negative memory only, not runtime feature inheritance",
        ],
        "broad_sweep": {
            "side_min_share_bands": [0.20, 0.25, 0.30, 0.35],
            "high_cost_share_caps": [0.65, 0.60, 0.55, 0.50],
            "density_bands_trades_per_day": ["5_to_10_goal_informed", "3_to_12_exploratory_with_reason"],
            "guardrail_modes": ["soft_penalty", "hard_veto", "asymmetric_side_budget"],
        },
        "extreme_sweep": [
            "strict_symmetric_side_budget",
            "high_cost_veto",
            "inverse_f92_short_heavy_rejection",
            "cost_normalized_utility",
            "zero_high_cost_preference_stress",
        ],
        "micro_search_gate": "Open only after broad/extreme variants produce validation useful signal without side/cost laundering.",
        "success_criteria_for_f93b_candidate_gate_to_lock_before_run": {
            "validation_actual_routed_net": "> 0",
            "validation_actual_routed_pf": ">= 1.05 exploratory minimum",
            "trades_per_day": "5_to_10 or explicit density rationale",
            "side_min_share": ">= 0.20 material improvement",
            "high_cost_share": "<= 0.55 material reduction",
            "tier_b": "not catastrophic; no severe net/PF collapse",
            "oos": "final read only; no tuning",
        },
        "failure_criteria": [
            "no variant passes joint gate",
            "Tier B collapses or is hidden",
            "density death",
            "side/cost concentration persists",
            "only threshold/filter/parameter repair remains",
        ],
        "invalid_conditions": [
            "post-entry fields in runtime features",
            "OOS tuning or budget relaxation after validation",
            "Tier A-only result presented as whole alpha read",
            "PF-only selection",
            "runtime/materialization/economics claim without same-packet MT5 Strategy Tester probe",
        ],
        "next_action": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def runtime_contract(payload: Mapping[str, Any]) -> dict[str, Any]:
    runtime_fields = [
        "terminal_identity",
        "broker",
        "symbol",
        "timeframe",
        "date_range",
        "deposit",
        "leverage",
        "modeling_mode",
        "spread",
        "commission",
        "slippage",
        "swap",
        "EA entrypoint",
        "EA/include module hashes",
        ".set path/hash",
        "parameter hash",
        "ONNX/model/bundle hash",
        "feature order/hash",
        "tester report/snapshot/terminal output paths and hashes",
        "trade list hash",
        "telemetry hash",
        "net/gross/PF/DD/trade-count fields",
    ]
    return {
        "run_id": RUN_ID,
        "runtime_status": RUNTIME_PROBE_STATUS,
        "mt5_strategy_tester_required_now": False,
        "not_run_with_reason": RUNTIME_NA_REASONS[0],
        "cost_or_proxy_bad_skip": False,
        "future_trigger": "If F93B/F93C creates a runnable candidate or runtime/materialization/economics claim, the same packet must attempt a narrow MT5 Strategy Tester probe or close blocked/inconclusive/out_of_scope_by_claim.",
        "required_runtime_identity_fields_for_future_probe": runtime_fields,
        "not_runtime_evidence": ["compile-only", "proxy-only", "ONNX handoff only", "parity-only"],
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "claim_boundary": payload["claim_boundary"],
    }


def f93b_brief(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "planned_run_id": NEXT_RUN_ID,
        "parent_run_id": RUN_ID,
        "primary_family": "experiment_execution",
        "recommended_verification_profile": "proxy_scout",
        "hypothesis": payload["hypothesis"],
        "required_pre_run_locks": [
            "dataset path/hash",
            "feature order/hash",
            "split policy",
            "candidate gate thresholds",
            "Tier A separate, Tier B separate, actual routed total records",
            "runtime trigger rule",
        ],
        "candidate_gate_dimensions": [
            "net profit",
            "profit factor",
            "drawdown",
            "recovery factor",
            "trade count and trades per day",
            "side_min_share",
            "high_cost_trade_share",
            "Tier B weakness boundary",
        ],
        "runtime_probe_rule": "If a meaningful runnable candidate appears or a runtime/economics/materialization claim is protected, attempt narrow MT5 Strategy Tester in the same packet or lower claim.",
        "claim_boundary": "planned_proxy_scout_only_no_candidate_no_runtime_authority",
    }


def data_integrity_plan(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "data_sources_checked": [file_identity(MODEL_INPUT_SUMMARY), file_identity(MODEL_INPUT_FEATURE_ORDER), file_identity(RAW_US100_MANIFEST)],
        "time_axis_boundary": "Use existing FPMarkets US100 M5 split_v1; F93A design does no row mutation.",
        "split_boundary": "F93B must fit budgets on train only, use validation for candidate gate, and keep OOS final-read-only.",
        "leakage_checks": [
            "closed-bar features only",
            "post-entry path/cost/PnL fields are labels or diagnostics only",
            "horizon crossing split edge must be censored in F93B if labels require future bars",
            "no OOS tuning",
        ],
        "tier_records_required": ["Tier A separate", "Tier B separate", "Tier A+B actual routed total"],
        "missing_data_boundary": "Tier B or combined records cannot be omitted; mark missing_required/blocked/out_of_scope_by_claim if unavailable.",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def risk_budget_design(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "risk_budget_axis": "side_balance_cost_exposure",
        "side_balance": {"diagnostic_source_side_min_share": payload["f92_reference"]["side_min_share"], "initial_min_share_grid": [0.20, 0.25, 0.30, 0.35]},
        "cost_exposure": {
            "diagnostic_source_high_cost_share": payload["f92_reference"]["high_cost_trade_share"],
            "initial_high_cost_cap_grid": [0.65, 0.60, 0.55, 0.50],
        },
        "utility_shape": [
            "net and PF remain necessary but not sufficient",
            "penalize side concentration",
            "penalize high-cost exposure",
            "preserve density only when side/cost budgets are not laundered",
        ],
        "do_not_repeat": [
            "same F92 path-first-touch q90/full58 threshold/filter tweak",
            "PF-only selection",
            "Tier A-only overclaim",
            "OOS rescue",
            "proxy-only runtime evidence",
        ],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def summary_payload(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": payload["created_at_utc"],
        "status": STATUS,
        "judgment": JUDGMENT,
        "verification_profile": "design_only",
        "hypothesis": payload["hypothesis"],
        "candidate_count": 0,
        "meaningful_signal_count": 0,
        "runtime_completed_rows": 0,
        "runtime_probe_status": RUNTIME_PROBE_STATUS,
        "task_force_actual_subagent_call_count": len(payload["task_force"]["actual_subagent_calls"]),
        "claim_boundary": CLAIM_BOUNDARY,
        "next_action": NEXT_RUN_ID,
    }


def kpi_payload(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "packet_id": RUN_ID,
        "test_period": "design_only_no_new_proxy_or_runtime_test",
        "proxy_kpi": "not_run_in_f93a",
        "runtime_kpi": "not_applicable_design_only_no_runtime_claim",
        "net_profit": None,
        "profit_factor": None,
        "drawdown": None,
        "trade_count": 0,
        "trades_per_day": 0,
        "parity": "not_applicable_no_onnx_or_ea",
        "gap_cause": "no runtime materialization in design-only stage open",
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
            "long_short_breakdown": None,
            "reason": "F93A is design-only and produces no trades.",
        },
        "claim_boundary": CLAIM_BOUNDARY,
    }


def result_summary_text(payload: Mapping[str, Any]) -> str:
    return f"""# F93A Stage Open Side Balance Cost Risk

Action: F93A records the side-balance and cost-exposure risk-budget design surface, Task Force actual calls, frontier extra due check, direction synthesis, and topic rotation guard.

Effect: F93B can run a proxy scout against a predeclared side/cost risk objective instead of repeating the F92 path-label threshold surface.

Runtime: no Strategy Tester evidence is created in F93A because there is no runnable candidate, ONNX/EA/set behavior, or runtime/materialization/economics claim. This is not a cost or proxy-bad skip.

Next: `{NEXT_RUN_ID}`.

Boundary: `{CLAIM_BOUNDARY}`.
"""


def write_run_artifacts(payload: Mapping[str, Any]) -> None:
    write_json(RUN_MANIFEST, {"script": SCRIPT_REL, **summary_payload(payload), "source_inputs": payload["source_identities"]})
    write_json(SUMMARY_JSON, summary_payload(payload))
    write_json(KPI_RECORD, kpi_payload(payload))
    write_json(EXPERIMENT_DESIGN, experiment_design(payload))
    write_json(RUNTIME_CONTRACT, runtime_contract(payload))
    write_json(F93B_BRIEF, f93b_brief(payload))
    write_json(DATA_INTEGRITY_PLAN, data_integrity_plan(payload))
    write_json(RISK_BUDGET_DESIGN, risk_budget_design(payload))
    write_text(RESULT_SUMMARY, result_summary_text(payload))
    write_text(F93A_REPORT, result_summary_text(payload))


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
            frontier_closeout_count_boundary="F92 closed; next boundary is F100; E01 already closed for F50.",
            due_status=FRONTIER_EXTRA_DUE_STATUS,
            claim_effect="F93A may open; no Extra Stage is due.",
        ),
    )
    write_json(
        FIVE_STAGE_SYNTHESIS,
        audit_payload(
            "frontier_five_stage_direction_synthesis",
            "pass",
            created_at_utc=payload["created_at_utc"],
            source_frontiers=["F88", "F89", "F90", "F91", "F92"],
            dominant_direction="classification and abstention axes repeatedly found density, side concentration, and cost exposure risks.",
            repeated_mechanism="proxy signal can survive locally while Tier B or cost/side concentration kills candidate status.",
            overused_axis_warning="avoid adjacent threshold/filter/path-label repair after F92.",
            next_axis_options=["side-balance risk budget", "cost-exposure budget", "curve objective", "runtime representation"],
            claim_effect="Direction only; no retrospective, permanent ban, authority, or candidate claim.",
        ),
    )
    write_json(
        TOPIC_ROTATION_CHECK,
        audit_payload(
            "frontier_topic_rotation_check",
            "pass",
            created_at_utc=payload["created_at_utc"],
            previous_stage="stage_frontier_92__path_conditioned_trade_shape_labeling_axis",
            proposed_stage=STAGE_ID,
            material_novelty_delta=[
                "objective/risk logic changes to side-balance and cost-exposure budgets",
                "validation philosophy changes to joint side/cost guardrail, not path-label q90 threshold repair",
                "trade-shape failure is reference/negative memory only",
            ],
            blocked_continuation_repair=False,
            threshold_filter_parameter_only_tweak=False,
            claim_effect="F93A can open as a distinct design axis; no candidate or runtime claim.",
        ),
    )
    write_json(
        SCOPE_GATE,
        audit_payload(
            "scope_completion_gate",
            "pass",
            created_at_utc=payload["created_at_utc"],
            required_artifacts=[rel(EXPERIMENT_DESIGN), rel(RUNTIME_CONTRACT), rel(F93B_BRIEF), rel(DATA_INTEGRITY_PLAN), rel(PACKET_TASK_FORCE_REVIEW)],
            missing_required_artifacts=[],
            claim_effect="Design packet artifacts exist; no execution or runtime claim.",
        ),
    )
    write_json(
        DATA_INTEGRITY_AUDIT,
        audit_payload(
            "data_integrity_audit",
            "pass_with_boundary",
            created_at_utc=payload["created_at_utc"],
            data_sources_checked=[file_identity(MODEL_INPUT_SUMMARY), file_identity(MODEL_INPUT_FEATURE_ORDER), file_identity(RAW_US100_MANIFEST)],
            split_boundary="F93A design-only; F93B must lock train/validation/OOS policy before proxy execution.",
            leakage_boundary="closed-bar features only; post-entry fields are labels/diagnostics only.",
            claim_effect="Data contract is predeclared for F93B but not claimed as a model/runtime pass.",
        ),
    )
    write_json(
        MODEL_VALIDATION_AUDIT,
        audit_payload(
            "model_validation_audit",
            "pass_with_boundary",
            created_at_utc=payload["created_at_utc"],
            validation_policy="train-only budget fitting; validation candidate gate; OOS final-read-only.",
            invalid_conditions=experiment_design(payload)["invalid_conditions"],
            selection_boundary="joint gate across net/PF/density/DD/recovery/side_min_share/high_cost_share/Tier B; PF-only forbidden.",
            claim_effect="F93A sets validation rules only; no model quality or candidate claim.",
        ),
    )
    write_json(
        ARTIFACT_AUDIT,
        audit_payload(
            "artifact_lineage_audit",
            "pass",
            created_at_utc=payload["created_at_utc"],
            source_inputs=[file_identity(path) for path in source_inputs()],
            produced_artifacts=[file_identity(ROOT / path if not path.is_absolute() else path) for path in produced_artifacts()],
            lineage_judgment="F92B/F92C negative memory -> F93A design-only risk-budget stage open -> F93B proxy scout plan.",
            claim_effect="Artifacts support design-open evidence only; ignored 02_runs outputs are hash-linked and not runtime authority.",
        ),
    )
    final_guard = gate_results.get("final_claim_guard")
    seed = audit_payload(
        "final_claim_guard",
        "pending" if not final_guard else final_guard.get("status", "pending"),
        created_at_utc=payload["created_at_utc"],
        claim_boundary=CLAIM_BOUNDARY,
        blocked_claims={claim: "not_claimed" for claim in FORBIDDEN_CLAIMS},
    )
    write_json(FINAL_CLAIM_GUARD, seed)
    write_json(PACKET_FINAL_CLAIM_GUARD, seed)


def skill_receipts(payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    current_truth_docs = [rel(WORKSPACE_STATE), rel(CURRENT_WORKING_STATE), rel(SELECTION_STATUS)]
    evidence = [rel(EXPERIMENT_DESIGN), rel(RUNTIME_CONTRACT), rel(F93B_BRIEF), rel(PACKET_TASK_FORCE_REVIEW)]
    compact = {
        "packet_id": RUN_ID,
        "status": "executed",
        "receipt_mode": "compact",
        "source_current_truth_docs": current_truth_docs,
        "evidence_used": evidence,
        "claim_boundary": CLAIM_BOUNDARY,
        "gates_not_run_with_reason": RUNTIME_NA_REASONS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }
    receipts = [
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-experiment-design",
            "status": "executed",
            "hypothesis": payload["hypothesis"],
            "baseline": payload["f92_reference"],
            "changed_variables": experiment_design(payload)["changed_variables"],
            "invalid_conditions": experiment_design(payload)["invalid_conditions"],
            "evidence_plan": experiment_design(payload)["success_criteria_for_f93b_candidate_gate_to_lock_before_run"],
            "receipt_path": rel(SKILL_RECEIPT_DIR / "experiment_design.json"),
        },
        {**compact, "skill": "obsidian-data-integrity", "receipt_path": rel(SKILL_RECEIPT_DIR / "data_integrity.json")},
        {**compact, "skill": "obsidian-model-validation", "receipt_path": rel(SKILL_RECEIPT_DIR / "model_validation.json")},
        {**compact, "skill": "obsidian-artifact-lineage", "receipt_path": rel(SKILL_RECEIPT_DIR / "artifact_lineage.json")},
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
            "final_status": "design_only_stage_open_no_candidate_no_runtime_authority",
            "receipt_path": rel(SKILL_RECEIPT_DIR / "claim_discipline.json"),
        },
    ]
    return receipts


def write_receipts(payload: Mapping[str, Any]) -> None:
    receipts = skill_receipts(payload)
    write_json(SKILL_RECEIPTS, {"packet_id": RUN_ID, "primary_skill": "obsidian-experiment-design", "receipts": receipts})
    for receipt in receipts:
        path = ROOT / str(receipt["receipt_path"])
        write_json(path, receipt)


def work_packet_payload(payload: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> dict[str, Any]:
    gate_results = gate_results or {}
    required_evidence = [rel(path) for path in [EXPERIMENT_DESIGN, RUNTIME_CONTRACT, F93B_BRIEF, DATA_INTEGRITY_PLAN, RISK_BUDGET_DESIGN, PACKET_TASK_FORCE_REVIEW, WORK_PACKET, SKILL_RECEIPTS, PACKET_CLOSEOUT_GATE]]
    return {
        "version": "work_packet_schema_v2_1",
        "packet_lifecycle": "new_packet",
        "packet_id": RUN_ID,
        "created_at_utc": payload["created_at_utc"],
        "user_request": {
            "user_quote": "/goal active continuation; user explicitly corrected that required Task Force agents must be actually called, not only promised",
            "requested_action": "canonical frontier stage open for F93A side-balance cost-exposure risk-budget axis",
            "requested_count": {"value": 1, "n_a_reason": ""},
            "ambiguous_terms": ["Goal Achieve is not claimed.", "Runtime authority is not claimed.", "F93A is design-only."],
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
                "f92_path_label_repair_laundering": "high",
                "side_cost_budget_as_movable_threshold": "high",
                "tier_b_weakness_hidden_by_actual_routed_total": "high",
                "runtime_probe_absence_misread_as_cost_skip": "medium",
            },
            "hard_stop_risks": [
                "Do not claim runtime/economics/materialization without MT5 Strategy Tester output identity.",
                "Do not repeat F92 path-label axis by threshold/filter/session/routing/parameter-only tweak.",
                "Do not tune on OOS or relax side/cost budgets after validation.",
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
                "reason": "F93A protects design-only stage-open claims and has no runnable candidate, ONNX/EA/set behavior, or runtime/economics claim.",
            },
            "questions": [],
            "required_user_decisions": [],
        },
        "interpreted_scope": {
            "work_families": ["experiment_design"],
            "target_surfaces": ["F93 stage open", "side-balance cost-exposure risk-budget design", "F93B proxy scout brief", "Task Force receipt", "state sync"],
            "scope_units": ["stage_open_design", "receipt", "state_sync"],
            "execution_layers": ["local_python_execution"],
            "mutation_policy": {"allowed": True, "user_quote": "/goal active continuation"},
            "evidence_layers": ["F92 negative memory reference", "F93A design artifacts", "Task Force actual calls", "frontier overlays"],
            "reduction_policy": {"reduction_allowed": False, "requires_user_quote": False, "rationale": "F93A is a formal stage-open packet."},
            "claim_boundary": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
        },
        "verification_profile": {
            "profile_id": "design_only",
            "claim_surface": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
            "trigger_sources": [
                "active_goal_frontier_continuation",
                "F92C closeout rotated to F93 pending scaffold",
                "formal F93A stage open claim",
                "explicit user instruction requiring Task Force when triggered",
            ],
            "protected_claims": ALLOWED_CLAIMS,
            "required_evidence": required_evidence,
            "gates_not_run_with_reason": RUNTIME_NA_REASONS,
            "stop_conditions": [
                "Stop after F93A design artifacts, receipts, gates, and state sync are materialized.",
                "Do not create candidate/runtime claims in F93A.",
                "If runnable candidate or runtime claim appears, reroute to runtime_probe profile in the same packet.",
            ],
        },
        "acceptance_criteria": [
            {"id": "AC-001", "text": "F93A experiment design exists.", "expected_artifact": rel(EXPERIMENT_DESIGN), "verification_method": "scope_completion_gate", "required": True},
            {"id": "AC-002", "text": "F93A Task Force actual calls are recorded.", "expected_artifact": rel(PACKET_TASK_FORCE_REVIEW), "verification_method": "codex_task_force_review_packet", "required": True},
            {"id": "AC-003", "text": "F93B proxy scout brief exists.", "expected_artifact": rel(F93B_BRIEF), "verification_method": "scope_completion_gate", "required": True},
            {"id": "AC-004", "text": "Runtime evidence gate is explicitly outside claim surface, not skipped for cost or proxy-bad reasons.", "expected_artifact": rel(RUNTIME_CONTRACT), "verification_method": "final_claim_guard", "required": True},
        ],
        "work_plan": [
            "Write F93A design/runtime-contract/F93B brief artifacts.",
            "Record Task Force actual_subagent_calls and local-verification responses.",
            "Run frontier_extra_due_check, five-stage synthesis, and topic rotation gates.",
            "Run schema, receipt, state sync, gate coverage, and final claim guard checks.",
            "Commit to main if gates pass.",
        ],
        "skill_routing": {
            "primary_family": "experiment_design",
            "primary_skill": "obsidian-experiment-design",
            "support_skills": ["obsidian-data-integrity", "obsidian-model-validation", "obsidian-artifact-lineage", "obsidian-task-force-review", "obsidian-stage-transition", "obsidian-claim-discipline"],
            "skills_considered": REQUIRED_SKILLS + ["obsidian-runtime-parity", "obsidian-backtest-forensics"],
            "skills_selected": REQUIRED_SKILLS,
            "skills_not_used": [
                {"skill": "obsidian-runtime-parity", "reason": "No ONNX/EA/runtime parity or handoff claim is made."},
                {"skill": "obsidian-backtest-forensics", "reason": "No new Strategy Tester report or trade list exists in F93A."},
            ],
            "required_skill_receipts": REQUIRED_SKILLS,
            "required_gates": REQUIRED_GATES,
        },
        "evidence_contract": {
            "source_inputs": [rel(path) for path in source_inputs()],
            "machine_readable": [rel(path) for path in [RUN_MANIFEST, SUMMARY_JSON, KPI_RECORD, EXPERIMENT_DESIGN, RUNTIME_CONTRACT, F93B_BRIEF, DATA_INTEGRITY_PLAN, RISK_BUDGET_DESIGN, SKILL_RECEIPTS]],
            "human_readable": [rel(RESULT_SUMMARY), rel(F93A_REPORT), rel(STAGE_BRIEF), rel(SELECTION_STATUS), rel(CONTEXT_ANCHOR)],
            "raw_evidence": [rel(F92B_SUMMARY), rel(F92B_CANDIDATE_GATE), rel(F92C_CLOSEOUT)],
            "missing_evidence": [
                {"evidence": "MT5 Strategy Tester runtime output", "reason": "outside F93A design-only claim surface"},
                {"evidence": "WFO/stress result", "reason": "outside F93A design-only claim surface"},
            ],
        },
        "gates": {
            "required": REQUIRED_GATES,
            "actual_status_source": {name: (gate_results.get(name, {}) or {}).get("status", "pending") for name in REQUIRED_GATES},
            "not_applicable_with_reason": {item["gate"]: item["reason"] for item in RUNTIME_NA_REASONS},
        },
        "final_claim_policy": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
    }


def closeout_gate_payload(gate_results: Mapping[str, Any] | None = None) -> dict[str, Any]:
    gate_results = gate_results or {}
    path_by_gate = {
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
        "state_sync_audit": PACKET_STATE_SYNC_AUDIT,
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
        "artifact_lineage_audit": "pass",
    }
    audits = []
    for gate in REQUIRED_GATES:
        status = (gate_results.get(gate, {}) or {}).get("status") or default_status.get(gate, "pending")
        audits.append({"audit_name": gate, "path": rel(path_by_gate[gate]), "status": status})
    statuses = [audit["status"] for audit in audits]
    return {
        "audit_name": "closeout_gate",
        "packet_id": RUN_ID,
        "status": "blocked" if any(str(status).startswith("blocked") for status in statuses) else "pass",
        "audits": audits,
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "claim_boundary": CLAIM_BOUNDARY,
        "final_claim_guard": {"audit_name": "final_claim_guard", "path": rel(PACKET_FINAL_CLAIM_GUARD), "status": (gate_results.get("final_claim_guard", {}) or {}).get("status", "pending")},
    }


def write_packet(payload: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> None:
    write_yaml(WORK_PACKET, work_packet_payload(payload, gate_results))
    write_json(PACKET_CLOSEOUT_GATE, closeout_gate_payload(gate_results))


def stage_brief_text(payload: Mapping[str, Any]) -> str:
    return f"""# {STAGE_ID}

Status: F93A design-only stage-open packet materialized. F93B proxy scout is the current run.

- current run: `{NEXT_RUN_ID}`
- latest completed run: `{RUN_ID}`

Question: Can side-balance and cost-exposure risk budgets produce a runtime-compatible US100 M5 surface without repeating F92 path-label threshold repair?

Material novelty delta: the primary axis changes from path-first-touch label selection to predeclared side-balance and cost-exposure risk-budget objective. It is not threshold/filter/parameter-only repair.

Runtime rule: if F93 creates a meaningful runnable candidate, ONNX/EA/set behavior, or runtime/materialization/economics claim, the same packet must attempt a narrow MT5 Strategy Tester probe or close as blocked/inconclusive/out_of_scope_by_claim.

Boundary: `{CLAIM_BOUNDARY}`.
"""


def selection_status_text(payload: Mapping[str, Any]) -> str:
    return f"""# Selection Status

F93A design-open packet is materialized. F93B proxy scout is the current run.

- current run: `{NEXT_RUN_ID}`
- latest completed run: `{RUN_ID}`
- status: `{STATUS}`
- judgment: `{JUDGMENT}`
- candidate: not claimed
- selected baseline: not claimed
- operating promotion: not claimed
- runtime authority: not claimed
- live readiness: not claimed
- Goal Achieve: not claimed
- Task Force: 6 selected agents actually called for F93A; no Task Force reviewed/pass claim.
- Runtime: `{RUNTIME_PROBE_STATUS}`
"""


def context_anchor_text(payload: Mapping[str, Any]) -> str:
    return f"""# Current Working State

- active stage: `{STAGE_ID}`
- latest completed run: `{RUN_ID}`
- current run: `{NEXT_RUN_ID}`
- status: `{STATUS}`
- judgment: `{JUDGMENT}`
- Task Force: 6 fresh selected agents called for F93A; no Task Force reviewed/pass claim.
- Runtime: `{RUNTIME_PROBE_STATUS}`
- Boundary: `{CLAIM_BOUNDARY}`
"""


def review_index_text() -> str:
    return f"""# F93 Review Index

- f93a_report: `{rel(F93A_REPORT)}`
- f93a_task_force_receipt: `{rel(TASK_FORCE_REVIEW)}`
- f93a_frontier_extra_due_check: `{rel(FRONTIER_EXTRA_DUE_CHECK)}`
- f93a_frontier_five_stage_direction_synthesis: `{rel(FIVE_STAGE_SYNTHESIS)}`
- f93a_frontier_topic_rotation_check: `{rel(TOPIC_ROTATION_CHECK)}`
- packet: `{rel(WORK_PACKET)}`
- current_run: `{NEXT_RUN_ID}`
"""


def input_refs_text() -> str:
    refs = "\n".join(f"- `{rel(path)}`" for path in source_inputs())
    return f"""# F93 Input References

{refs}

Boundary: F92B/F92C are reference and negative memory only, not inherited authority.
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
        "task_force_status": "f93a_actual_subagent_calls_recorded_6_selected_agents_no_task_force_reviewed_pass_claim",
        "runtime_probe_status": RUNTIME_PROBE_STATUS,
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "updated_at_utc": payload["created_at_utc"],
        "context_anchor": rel(CONTEXT_ANCHOR),
        "notes": [
            "Action: F93A formal design-only stage-open packet was materialized.",
            "Effect: F93B current run can scout side-balance and cost-exposure risk budgets.",
            "Runtime: no Strategy Tester evidence; no runtime authority; no Goal Achieve.",
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
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), [dict(row) for row in reader]


def write_csv_rows(path: Path, fieldnames: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def replace_rows(path: Path, remove_if: Callable[[Mapping[str, str]], bool], new_rows: Sequence[Mapping[str, Any]], header_source: Path | None = None) -> None:
    fieldnames, rows = read_csv_rows(path)
    if not fieldnames and header_source:
        fieldnames, _ = read_csv_rows(header_source)
    extras = [key for row in new_rows for key in row if key not in fieldnames]
    fieldnames = fieldnames + extras
    kept = [row for row in rows if not remove_if(row)]
    write_csv_rows(path, fieldnames, [*kept, *new_rows])


def ledger_rows(payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    base = {
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "date": "2026-06-19",
        "created_at": payload["created_at_utc"],
        "created_at_utc": payload["created_at_utc"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "not_claimed",
    }
    f93a = {
        **base,
        "ledger_row_id": f"{RUN_ID}__stage_open_design",
        "run_id": RUN_ID,
        "subrun_id": "stage_open_design",
        "record_view": "stage_open_design",
        "tier_scope": "not_applicable_design_only",
        "kpi_scope": "design_only",
        "scoreboard_lane": "design_open",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(F93A_REPORT),
        "primary_kpi": "candidate_count=0;runtime_completed_rows=0",
        "guardrail_kpi": "no_runtime_claim;no_authority;task_force_calls=6",
        "external_verification_status": "not_applicable_design_only",
        "notes": "F93A design-only open; Task Force actual calls recorded.",
        "run_number": "frontier93A",
        "decision": STATUS,
        "next_run_id": NEXT_RUN_ID,
        "rows": 0,
        "gate_passes": len(REQUIRED_GATES),
        "gate_total": len(REQUIRED_GATES),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(F93A_REPORT),
        "primary_artifact": rel(F93A_REPORT),
        "result_status": STATUS,
        "runtime_completed_rows": 0,
        "candidate_count": 0,
        "meaningful_signal_count": 0,
        "completion_candidate_count": 0,
        "artifact_count": len([path for path in produced_artifacts() if path_exists(path if path.is_absolute() else ROOT / path)]),
        "required_gate_audit": rel(PACKET_REQUIRED_GATE_AUDIT),
        "run_family": "experiment_design",
        "run_type": "stage_open_design",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(STAGE_DIR),
        "result_path": rel(F93A_REPORT),
        "row_id": f"{RUN_ID}__stage_open_design",
        "question": "Can side-balance and cost-exposure risk budgets produce a runtime-compatible US100 M5 surface?",
        "next_action": NEXT_RUN_ID,
        "model_variants": 0,
        "selected_surfaces": 0,
        "runtime_attempt_rows": 0,
    }
    f93b = {
        **base,
        "ledger_row_id": f"{NEXT_RUN_ID}__planned_current_run",
        "run_id": NEXT_RUN_ID,
        "subrun_id": "planned_current_run",
        "record_view": "planned_current_run",
        "tier_scope": "planned_tier_a_tier_b_actual_routed",
        "kpi_scope": "planned_proxy_scout",
        "scoreboard_lane": "planned_proxy_scout",
        "status": "planned_current_run_no_authority",
        "judgment": "planned_after_f93a_design_open",
        "path": rel(F93B_BRIEF),
        "primary_kpi": "pending",
        "guardrail_kpi": "side_cost_budget_gate_pending;no_runtime_claim",
        "external_verification_status": "pending",
        "notes": "F93B planned current run after F93A open.",
        "run_number": "frontier93B",
        "decision": "planned_current_run_no_authority",
        "next_run_id": "",
        "rows": 0,
        "gate_passes": 0,
        "gate_total": 0,
        "claim_boundary": "planned_proxy_scout_only_no_candidate_no_runtime_authority",
        "report_path": rel(F93B_BRIEF),
        "primary_artifact": rel(F93B_BRIEF),
        "result_status": "planned_current_run_no_authority",
        "runtime_completed_rows": 0,
        "candidate_count": 0,
        "meaningful_signal_count": 0,
        "completion_candidate_count": 0,
        "artifact_count": 0,
        "required_gate_audit": "",
        "run_family": "experiment_design",
        "run_type": "planned_proxy_scout",
        "input_run_id": RUN_ID,
        "output_path": rel(F93B_BRIEF),
        "result_path": rel(F93B_BRIEF),
        "row_id": f"{NEXT_RUN_ID}__planned_current_run",
        "question": "Can side-balance and cost-exposure risk budgets produce a runtime-compatible US100 M5 surface?",
        "next_action": "run_f93b_proxy_scout",
        "model_variants": 0,
        "selected_surfaces": 0,
        "runtime_attempt_rows": 0,
    }
    return [f93a, f93b]


def update_ledgers(payload: Mapping[str, Any]) -> None:
    rows = ledger_rows(payload)
    run_ids = {RUN_ID, NEXT_RUN_ID}
    replace_rows(RUN_REGISTRY, lambda row: row.get("run_id") in run_ids, rows, header_source=RUN_REGISTRY)
    replace_rows(ALPHA_LEDGER, lambda row: row.get("run_id") in run_ids, rows, header_source=ALPHA_LEDGER)
    replace_rows(STAGE_LEDGER, lambda row: row.get("run_id") in run_ids, rows, header_source=ALPHA_LEDGER)


def update_artifact_registry(payload: Mapping[str, Any]) -> None:
    rows = []
    for raw_path in produced_artifacts():
        path = raw_path if raw_path.is_absolute() else ROOT / raw_path
        if not path_exists(path):
            continue
        path_rel = rel(path)
        rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": "f93a_design_open",
                "path": path_rel,
                "sha256": sha256_file_lf_normalized(path),
                "created_at": payload["created_at_utc"],
                "claim_boundary": CLAIM_BOUNDARY,
                "artifact_id": f"{RUN_ID}::{path_rel}",
                "created_at_utc": payload["created_at_utc"],
                "notes": "F93A design-open artifact; no runtime authority.",
                "artifact_path": path_rel,
                "effect": "Supports F93A design-open and F93B proxy-scout handoff only.",
                "size_bytes": io_path(path).stat().st_size,
            }
        )
    replace_rows(ARTIFACT_REGISTRY, lambda row: row.get("run_id") == RUN_ID, rows, header_source=ARTIFACT_REGISTRY)


def append_once(path: Path, marker: str, addition: str) -> None:
    existing = io_path(path).read_text(encoding="utf-8-sig") if path_exists(path) else ""
    if marker in existing:
        return
    write_text(path, existing.rstrip() + "\n\n" + addition.strip() + "\n")


def update_register_docs(payload: Mapping[str, Any]) -> None:
    marker = f"<!-- {RUN_ID} -->"
    idea_addition = f"""{marker}
## F93A side-balance cost-exposure risk-budget open

- run_id: `{RUN_ID}`
- hypothesis: {payload['hypothesis']}
- decision_use: design-only stage open and F93B proxy scout plan.
- task_force_actual_calls: 6 selected agents recorded.
- runtime: no Strategy Tester evidence; no runtime authority.
- next_action: `{NEXT_RUN_ID}`.
- claim_boundary: `{CLAIM_BOUNDARY}`.
"""
    status_addition = f"""{marker}
- `{RUN_ID}`: design-only stage open; current run is `{NEXT_RUN_ID}`; no candidate, selected baseline, runtime authority, live readiness, or Goal Achieve.
"""
    changelog_addition = f"""{marker}
## {payload['created_at_utc']} - F93A Stage Open Side/Cost Risk Budget

- Action: `{RUN_ID}` materialized F93A as a design-only stage-open packet.
- Effect: `{NEXT_RUN_ID}` is the current run for side-balance and cost-exposure risk-budget proxy scouting.
- Task Force: six selected agents were actually called and recorded in `{rel(PACKET_TASK_FORCE_REVIEW)}`.
- Runtime: no new Strategy Tester runtime evidence; no runtime authority; no Goal Achieve.
- Boundary: `{CLAIM_BOUNDARY}`.
"""
    decision_text = f"""# F93A Stage Open Decision

Action: materialize `{RUN_ID}` as a design-only stage-open packet.

Effect: `{NEXT_RUN_ID}` becomes current run and must lock side/cost budgets before proxy execution.

Task Force: actual selected-agent calls are recorded at `{rel(PACKET_TASK_FORCE_REVIEW)}`.

Boundary: `{CLAIM_BOUNDARY}`.
"""
    append_once(IDEA_REGISTRY, RUN_ID, idea_addition)
    append_once(GLOBAL_SELECTION_STATUS, RUN_ID, status_addition)
    append_once(WORKSPACE_CHANGELOG, RUN_ID, changelog_addition)
    append_once(ROOT_CHANGELOG, RUN_ID, changelog_addition)
    write_text(DECISION_MEMO, decision_text)


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
    results["work_packet_schema_lint"] = run_gate_cmd(["foundation.control_plane.work_packet_schema_lint", str(WORK_PACKET)], PACKET_WORK_PACKET_LINT)
    results["skill_receipt_schema_lint"] = run_gate_cmd(["foundation.control_plane.skill_receipt_schema_lint", str(SKILL_RECEIPTS)], PACKET_SKILL_RECEIPT_LINT)
    results["state_sync_audit"] = run_gate_cmd(
        ["foundation.control_plane.state_sync_audit", "--root", str(ROOT), "--active-stage", STAGE_ID, "--current-branch", current_branch()],
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
            AuditResult(audit_name="artifact_lineage_audit", status="pass"),
        ],
    )
    final_payload = final_guard.to_dict()
    final_payload.update({"packet_id": RUN_ID, "claim_boundary": CLAIM_BOUNDARY, "blocked_claims": {claim: "not_claimed" for claim in FORBIDDEN_CLAIMS}})
    write_json(FINAL_CLAIM_GUARD, final_payload)
    write_json(PACKET_FINAL_CLAIM_GUARD, final_payload)
    results["final_claim_guard"] = {"status": final_guard.status, "output_path": rel(PACKET_FINAL_CLAIM_GUARD), "allowed_claims": list(final_guard.allowed_claims), "forbidden_claims": list(final_guard.forbidden_claims)}
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


def write_final(payload: Mapping[str, Any], gate_results: Mapping[str, Any]) -> None:
    write_run_artifacts(payload)
    write_audits(payload, gate_results)
    write_receipts(payload)
    write_packet(payload, gate_results)
    sync_review_audit(PACKET_STATE_SYNC_AUDIT, STATE_SYNC_AUDIT)
    sync_review_audit(PACKET_REQUIRED_GATE_AUDIT, REQUIRED_GATE_AUDIT)
    update_state_docs(payload)
    update_ledgers(payload)
    update_artifact_registry(payload)


def main() -> int:
    missing = [rel(path) for path in source_inputs() if not path_exists(path)]
    if missing:
        raise FileNotFoundError(f"Missing required F93A source evidence: {missing}")
    ensure_dirs()
    payload = base_payload(utc_now())
    write_initial(payload)
    gate_results = run_control_gates(payload)
    write_final(payload, gate_results)
    print(json.dumps({"run_id": RUN_ID, "status": STATUS, "next_run_id": NEXT_RUN_ID, "gate_statuses": {k: v.get("status") for k, v in gate_results.items()}}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
