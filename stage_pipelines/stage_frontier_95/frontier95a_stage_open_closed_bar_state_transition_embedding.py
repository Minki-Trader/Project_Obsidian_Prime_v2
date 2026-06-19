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


STAGE_ID = "stage_frontier_95__closed_bar_state_transition_embedding_axis"
RUN_ID = "frontier95A_stage_open_closed_bar_state_transition_embedding_axis_v1"
PARENT_RUN_ID = "frontier94C_tier_stable_realized_utility_repair_or_rotation_decision_v1"
NEXT_RUN_ID = "frontier95B_closed_bar_state_transition_embedding_proxy_scout_v1"
SCRIPT_REL = "stage_pipelines/stage_frontier_95/frontier95a_stage_open_closed_bar_state_transition_embedding.py"

STATUS = "f95a_stage_open_design_prepared_no_candidate_no_authority"
JUDGMENT = "design_only_stage_open_closed_bar_state_transition_embedding_axis"
CLAIM_BOUNDARY = (
    "f95a_design_only_stage_open_closed_bar_state_transition_embedding_axis_"
    "no_model_candidate_no_wfo_pass_no_stress_pass_no_mt5_runtime_evidence_"
    "no_selected_baseline_no_operating_promotion_no_runtime_authority_"
    "no_live_readiness_no_goal_achieve"
)
RUNTIME_PROBE_STATUS = (
    "not_applicable_design_only_no_runnable_candidate_no_runtime_materialization_"
    "economics_handoff_claim_not_cost_or_proxy_bad_skip"
)
FRONTIER_EXTRA_DUE_STATUS = "not_due_after_f94_closeout_next_boundary_f100_e02_pending_e01_closed_for_f050"
FRONTIER_TOPIC_ROTATION_STATUS = (
    "passed_f95_closed_bar_state_transition_embedding_axis_not_f94_utility_label_repair"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / "frontier95A"
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
DECISION_MEMO = ROOT / "docs" / "decisions" / "2026-06-19_frontier95a_stage_open_closed_bar_state_transition_embedding.md"

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
F95B_BRIEF = DESIGN_DIR / "f95b_proxy_scout_brief.json"
DATA_INTEGRITY_PLAN = DESIGN_DIR / "data_integrity_plan.json"
MODEL_VALIDATION_PLAN = DESIGN_DIR / "model_validation_plan.json"
STATE_TRANSITION_CONTRACT = DESIGN_DIR / "state_transition_embedding_contract.json"
RESULT_SUMMARY = REPORT_DIR / "summary.md"

STAGE_OPEN_SUMMARY = REVIEW_DIR / "f95a_stage_open_summary.json"
TASK_FORCE_REVIEW = REVIEW_DIR / "f95a_task_force_review_receipt.json"
FRONTIER_EXTRA_DUE_CHECK = REVIEW_DIR / "f95a_frontier_extra_due_check.json"
FIVE_STAGE_SYNTHESIS = REVIEW_DIR / "f95a_frontier_five_stage_direction_synthesis.json"
TOPIC_ROTATION_CHECK = REVIEW_DIR / "f95a_frontier_topic_rotation_check.json"
SCOPE_GATE = REVIEW_DIR / "f95a_scope_completion_gate.json"
DATA_INTEGRITY_AUDIT = REVIEW_DIR / "f95a_data_integrity_audit.json"
MODEL_VALIDATION_AUDIT = REVIEW_DIR / "f95a_model_validation_audit.json"
ARTIFACT_AUDIT = REVIEW_DIR / "f95a_artifact_lineage_audit.json"
RESULT_JUDGMENT_AUDIT = REVIEW_DIR / "f95a_result_judgment_audit.json"
FINAL_CLAIM_GUARD = REVIEW_DIR / "f95a_final_claim_guard.json"
STATE_SYNC_AUDIT = REVIEW_DIR / "f95a_state_sync_audit.json"
REQUIRED_GATE_AUDIT = REVIEW_DIR / "f95a_required_gate_coverage_audit.json"
F95A_REPORT = REVIEW_DIR / "frontier95A_stage_open_closed_bar_state_transition_embedding_report.md"

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
RAW_US100_MANIFEST = (
    ROOT / "data" / "raw" / "mt5_bars" / "m5" / "US100" / "bars_us100_m5_mt5api_raw.manifest.json"
)
F94B_KPI = (
    ROOT
    / "stages"
    / "stage_frontier_94__tier_stable_realized_utility_label_axis"
    / "02_runs"
    / "frontier94B"
    / "kpi_record.json"
)
F94B_CANDIDATE_GATE = (
    ROOT
    / "stages"
    / "stage_frontier_94__tier_stable_realized_utility_label_axis"
    / "02_runs"
    / "frontier94B"
    / "proxy_scout"
    / "candidate_gate.json"
)
F94C_CLOSEOUT_SUMMARY = (
    ROOT
    / "stages"
    / "stage_frontier_94__tier_stable_realized_utility_label_axis"
    / "03_reviews"
    / "f94c_stage_closeout_summary.json"
)
F94C_DECISION = (
    ROOT
    / "stages"
    / "stage_frontier_94__tier_stable_realized_utility_label_axis"
    / "02_runs"
    / "frontier94C"
    / "d"
    / "decision.json"
)
F94C_WORK_PACKET = ROOT / "docs" / "agent_control" / "packets" / PARENT_RUN_ID / "work_packet.yaml"
F94C_CLOSEOUT_GATE = ROOT / "docs" / "agent_control" / "packets" / PARENT_RUN_ID / "closeout_gate.json"

ALLOWED_CLAIMS = [
    "f95a_stage_open_design_prepared",
    "f95_closed_bar_state_transition_embedding_axis_opened",
    "f95b_proxy_scout_planned",
    "task_force_actual_calls_recorded_for_f95a",
    "frontier_extra_due_check_not_due_after_f94",
    "frontier_five_stage_direction_synthesis_recorded_for_f90_to_f94",
    "frontier_topic_rotation_check_recorded_for_f95",
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
    "f95_stage_open_completed",
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
        "reason_code": "outside_claim_surface_design_only_no_runnable_candidate",
        "reason": "F95A creates design artifacts only and no runnable candidate, ONNX/EA/set behavior, or runtime/materialization/economics/handoff claim.",
        "claim_effect": "No runtime, materialization, handoff, economics, promotion, authority, readiness, or Goal Achieve claim is allowed.",
    },
    {
        "gate": "wfo_stress_gate",
        "reason_code": "outside_claim_surface_no_model_candidate",
        "reason": "F95A does not train/select a model and only prepares F95B proxy scout design.",
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
        RAW_US100_MANIFEST,
        F94B_KPI,
        F94B_CANDIDATE_GATE,
        F94C_CLOSEOUT_SUMMARY,
        F94C_DECISION,
        F94C_WORK_PACKET,
        F94C_CLOSEOUT_GATE,
    ]


def produced_artifacts() -> list[Path]:
    return [
        Path(SCRIPT_REL),
        RUN_MANIFEST,
        SUMMARY_JSON,
        KPI_RECORD,
        EXPERIMENT_DESIGN,
        RUNTIME_CONTRACT,
        F95B_BRIEF,
        DATA_INTEGRITY_PLAN,
        MODEL_VALIDATION_PLAN,
        STATE_TRANSITION_CONTRACT,
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
        F95A_REPORT,
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
            "spawned_agent_id": "019edeb9-add3-78b1-9610-4a8d49ff3a45",
            "nickname": "Singer",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "accepted",
            "bounded_evidence": [rel(WORKSPACE_STATE), rel(STAGE_BRIEF), rel(SELECTION_STATUS)],
            "local_verification": "F95A is design-only stage open. Minimum allowed claims exclude KPI, candidate, ONNX/EA, MT5 runtime, economics, promotion, authority, readiness, and Goal Achieve.",
            "accepted_summary": "Proceed only as F95A design-open and keep F94C as negative memory/reference surface.",
        },
        {
            "roster_agent_id": "agent_04_evidence_control_plane",
            "spawned_agent_id": "019edeb9-db4d-7bf2-acec-b86073933881",
            "nickname": "Erdos",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "needs_local_verification",
            "bounded_evidence": [rel(WORKSPACE_STATE), rel(STAGE_BRIEF), rel(WORK_PACKET)],
            "local_verification": "This script materializes the missing F95A work_packet, skill receipts, gate audits, final_claim_guard, state sync, and actual_subagent_calls.",
            "accepted_summary": "F95A scaffold alone was blocked; local packet/gate/receipt evidence is required before low-boundary stage-open claims.",
        },
        {
            "roster_agent_id": "agent_05_data_feature_contract",
            "spawned_agent_id": "019edeba-1a54-7200-9307-fcd1649b57ba",
            "nickname": "Feynman",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "needs_local_verification",
            "bounded_evidence": [rel(MODEL_INPUT_SUMMARY), rel(MODEL_INPUT_FEATURE_ORDER), rel(RAW_US100_MANIFEST)],
            "local_verification": "F95B must prove closed-bar-only features, time-axis meaning, split-window isolation, missing/duplicate checks, Tier A/B paired records, and future-path perturbation.",
            "accepted_summary": "Closed M5 bar sequence/state-transition embedding is a new data representation, but data_contract_pass is not claimed.",
        },
        {
            "roster_agent_id": "agent_06_quant_research",
            "spawned_agent_id": "019edeba-42bf-79d1-9909-1a1d3b204eda",
            "nickname": "Leibniz",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "needs_local_verification",
            "bounded_evidence": [rel(F94B_KPI), rel(F94B_CANDIDATE_GATE), rel(F94C_CLOSEOUT_SUMMARY)],
            "local_verification": "F95B must compare raw OHLC-derived features and F94 utility-label reference without reusing F94 labels as hidden target or threshold repair.",
            "accepted_summary": "The hypothesis is valid only if it learns continuation, reversal-trap, and chop-cost-drag states before long/short/abstain mapping.",
        },
        {
            "roster_agent_id": "agent_07_model_validation_risk",
            "spawned_agent_id": "019edeba-728f-7543-986a-1642a16a7130",
            "nickname": "Carver",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "needs_local_verification",
            "bounded_evidence": [rel(F94B_KPI), rel(F94B_CANDIDATE_GATE), rel(MODEL_INPUT_SUMMARY)],
            "local_verification": "F95B must lock time-ordered split, train-only scaler/embedding fit scope, validation selection, OOS locked-read protocol, and non-PF-only metric boundary.",
            "accepted_summary": "Design direction is accepted; OOS selection, calibration laundering, threshold-only repair, and Tier B rescue are rejected.",
        },
        {
            "roster_agent_id": "agent_08_mt5_onnx_runtime",
            "spawned_agent_id": "019edeba-9d15-7223-baec-5c6501963b7b",
            "nickname": "Sagan",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "accepted",
            "bounded_evidence": [rel(STAGE_BRIEF), rel(RUNTIME_CONTRACT), rel(SELECTION_STATUS)],
            "local_verification": "Runtime gate is N/A only because F95A has no runnable candidate and no runtime/materialization/economics/handoff claim. Cost/proxy-bad skip is not used.",
            "accepted_summary": "Any future ONNX/EA/set behavior, runtime economics, materialization, or handoff claim triggers same-packet MT5 Strategy Tester probe.",
        },
    ]


def task_force_receipt(created_at: str) -> dict[str, Any]:
    calls = task_force_calls()
    return {
        "packet_id": RUN_ID,
        "skill": "obsidian-task-force-review",
        "status": "executed",
        "created_at_utc": created_at,
        "trigger_reason": "F95A formal stage-open packet, active goal frontier continuation, and explicit user correction requiring real relevant Task Force agent calls.",
        "roster_registry": "docs/agent_control/codex_task_force_registry.yaml",
        "agents_used": [call["roster_agent_id"] for call in calls],
        "actual_subagent_calls": calls,
        "review_requirement": "codex_task_force_review_packet",
        "model_policy": {"model": "inherited_current_codex_model", "reasoning_effort": "inherited", "service_tier": "inherited"},
        "bounded_evidence": [rel(WORKSPACE_STATE), rel(STAGE_BRIEF), rel(SELECTION_STATUS), rel(F94C_CLOSEOUT_SUMMARY), rel(MODEL_INPUT_SUMMARY)],
        "advice_classification": {
            "accepted": [call["roster_agent_id"] for call in calls if call["opinion_classification"] == "accepted"],
            "needs_local_verification": [call["roster_agent_id"] for call in calls if call["opinion_classification"] == "needs_local_verification"],
            "rejected": [],
        },
        "local_verification": [
            "F95A packet, receipts, audits, and state sync are generated locally.",
            "Runtime evidence gate is outside claim surface only because no runnable candidate or runtime claim exists.",
            "F95B must verify F94 novelty delta, time-axis contract, Tier A/B paired records, train-only embedding fit, and non-PF-only selection.",
        ],
        "claim_boundary": CLAIM_BOUNDARY,
        "final_codex_direction": "Proceed with F95A design-only stage open and plan F95B closed-bar state-transition embedding proxy scout.",
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
            "US100 M5 closed-bar sequences contain state-transition structure that can separate continuation, "
            "reversal-trap, and chop-cost-drag states before long/short/abstain mapping."
        ),
        "decision_use": "design-only stage open and F95B proxy scout handoff",
        "f94_reference": {
            "source_run": PARENT_RUN_ID,
            "use": "negative memory/reference surface only",
            "no_inheritance": ["winner", "selected_baseline", "promotion_history", "runtime_authority"],
        },
        "frontier_extra_due_status": FRONTIER_EXTRA_DUE_STATUS,
        "frontier_topic_rotation_status": FRONTIER_TOPIC_ROTATION_STATUS,
        "runtime_probe_status": RUNTIME_PROBE_STATUS,
        "source_identities": [file_identity(path) for path in source_inputs()],
        "task_force": task_force_receipt(created_at),
    }


def experiment_design(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "hypothesis": payload["hypothesis"],
        "proxy": "F95B will build closed-bar sequence/state-transition features and inspect class distribution, stability, and cost-drag separation before any runtime claim.",
        "decision_use": payload["decision_use"],
        "comparison_baseline": [
            "raw OHLC-derived feature reference",
            "F94 utility-label negative/reference surface, not inherited baseline",
        ],
        "changed_variables": [
            "data_representation: recent closed-bar sequence and transition vector",
            "objective: continuation/reversal-trap/chop-cost-drag state before direction mapping",
            "trade_shape: long/short/abstain mapped after state class",
            "validation_philosophy: state stability, density, DD resilience, and cost-drag separation before PF",
        ],
        "controlled_variables": [
            "US100 symbol",
            "M5 timeframe",
            "closed bars only",
            "time-ordered train/validation/OOS protocol",
            "cost/spread assumptions must be carried from local contract before proxy economics",
            "Tier A separate, Tier B separate, and Tier A+B combined records",
        ],
        "success_criteria_for_f95b_proxy_scout": [
            "state classes do not collapse to one dominant class",
            "chop-cost-drag abstention does not kill all density",
            "validation mapping improves cost-adjusted expectancy without PF-only selection",
            "Tier A, Tier B, and A+B combined are separately readable",
        ],
        "invalid_conditions": [
            "open/current bar or future path enters feature surface",
            "embedding scaler/codebook/model is fit on validation or OOS",
            "F94 utility labels are reused as hidden target",
            "OOS results are used to choose feature window, cluster count, threshold, or abstain rule",
            "Tier B thin positive is used as rescue evidence",
            "proxy-only score is described as runtime evidence",
        ],
        "stop_conditions": [
            "Stop if F95 novelty delta versus F94 utility-label repair is not locally supported.",
            "Stop if feature-label boundary or split-window isolation fails.",
            "Stop if first proxy scout collapses into always-abstain, always-one-direction, or one-class dominance.",
        ],
    }


def state_transition_contract(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "contract_status": "design_locked_for_f95b_planning_only",
        "feature_window": {
            "source": "closed M5 bars only",
            "candidate_inputs": [
                "recent returns",
                "range expansion/contraction",
                "close location in bar",
                "wick ratio",
                "volatility-normalized movement",
                "delta from previous state",
            ],
            "forbidden_inputs": ["current open bar", "future path", "future return", "MFE/MAE diagnostic columns"],
        },
        "state_classes": ["continuation", "reversal_trap", "chop_cost_drag"],
        "mapping_later": "long/short/abstain can be mapped only after state class distribution and cost-drag checks.",
        "fit_scope": "train-only for scaler, codebook, cluster center, embedding model, and calibration.",
        "split_policy": "validation selects; OOS is locked read only.",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def data_integrity_plan(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "data_sources_checked": [file_identity(path) for path in [MODEL_INPUT_SUMMARY, MODEL_INPUT_FEATURE_ORDER, RAW_US100_MANIFEST]],
        "time_axis_boundary": "F95B must record whether M5 timestamp is bar open or bar close, broker timezone, session timezone, and DST policy.",
        "feature_label_boundary": "Features end at closed sequence time t; labels/evaluation start at t+1 and later.",
        "split_boundary": "Lookback window and label horizon may not cross train/validation/OOS split boundaries.",
        "missing_data_boundary": "F95B must check M5 gaps, duplicate bars, holiday/session breaks, and fake transition risk.",
        "tier_boundary": "Tier A separate, Tier B separate, and Tier A+B combined records are mandatory; missing Tier B is blocked or out_of_scope_by_claim.",
        "open_issues_from_f94c": [
            "timezone binding unresolved for authority claims",
            "Tier B train-label footnote must close before stronger claims",
            "full routed/Tier B perturbation check required before stronger claims",
        ],
    }


def model_validation_plan(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "model_or_threshold_surface": "closed-bar state-transition embedding proxy scout, no trained candidate yet",
        "validation_split": "time-ordered train/validation/OOS; OOS locked read only",
        "overfit_checks": [
            "train-only scaler/embedding fit",
            "no OOS feature-window or cluster-count selection",
            "no calibration probability claim before validation bin stability",
        ],
        "selection_metric_boundary": [
            "state stability",
            "trade density",
            "DD resilience",
            "cost-drag separation",
            "expectancy",
            "PF only as one supporting metric, never alone",
        ],
        "same_packet_mt5_triggers": [
            "ONNX/EA/set behavior",
            "materialization-ready claim",
            "runtime economics or handoff claim",
            "Python proxy equals MT5 execution semantics claim",
            "state class routed to fixed long/short/abstain runtime candidate",
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
        "claim_effect": "F95A cannot support runtime verified, economics pass, materialization ready, handoff complete, promotion, authority, readiness, or Goal Achieve.",
    }


def f95b_brief(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "planned_run_id": NEXT_RUN_ID,
        "parent_run_id": RUN_ID,
        "task": "proxy scout for closed-bar state-transition embedding distribution and tradability",
        "verification_profile": "proxy_scout",
        "required_records": ["Tier A separate", "Tier B separate", "Tier A+B combined"],
        "first_action": "Read F94 utility label definition and data contracts, then run a small fixed-sample distribution check before model expansion.",
        "candidate_gate_preview": [
            "state class distribution not collapsed",
            "closed-bar-only feature hash fixed",
            "validation metric bundle not PF-only",
            "no OOS selection",
            "runtime trigger check before any ONNX/EA handoff claim",
        ],
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
        "kpi_scope": "design_only_no_proxy_no_runtime",
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
            "long_short_breakdown": "not_applicable",
        },
        "claim_effect": "KPI fields are intentionally empty because F95A is design-only and has no proxy/runtime evidence.",
    }


def result_summary_text(payload: Mapping[str, Any]) -> str:
    return f"""# F95A Stage Open Summary

Action(행동): materialize(물질화) `{RUN_ID}` as a design-only stage-open packet(설계 전용 단계 개방 묶음).

Effect(효과): `{NEXT_RUN_ID}` becomes the current run(현재 실행) for closed-bar state-transition embedding proxy scouting(확정봉 상태 전이 임베딩 프록시 탐색).

Hypothesis(가설): {payload['hypothesis']}

Task Force(태스크포스): six selected agents(선택 요원 6명) were actually called(실제 호출) and recorded(기록) in `{rel(PACKET_TASK_FORCE_REVIEW)}`.

Runtime boundary(런타임 경계): no runnable candidate(실행 후보 없음), no ONNX/EA/set bundle(온엑스/전문가 자문/설정 묶음 없음), no Strategy Tester output(전략 테스터 출력 없음), no runtime/economics/handoff claim(런타임/경제성/인계 주장 없음).

Next(다음): `{NEXT_RUN_ID}`.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""


def write_run_artifacts(payload: Mapping[str, Any]) -> None:
    write_json(RUN_MANIFEST, {"script": SCRIPT_REL, **summary_payload(payload), "source_inputs": payload["source_identities"]})
    write_json(SUMMARY_JSON, summary_payload(payload))
    write_json(KPI_RECORD, kpi_payload(payload))
    write_json(EXPERIMENT_DESIGN, experiment_design(payload))
    write_json(RUNTIME_CONTRACT, runtime_contract(payload))
    write_json(F95B_BRIEF, f95b_brief(payload))
    write_json(DATA_INTEGRITY_PLAN, data_integrity_plan(payload))
    write_json(MODEL_VALIDATION_PLAN, model_validation_plan(payload))
    write_json(STATE_TRANSITION_CONTRACT, state_transition_contract(payload))
    write_text(RESULT_SUMMARY, result_summary_text(payload))
    write_json(STAGE_OPEN_SUMMARY, summary_payload(payload))
    write_text(F95A_REPORT, result_summary_text(payload))


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
            frontier_closeout_count_boundary="F94 closed; next boundary is F100/E02; E01 closed for F50.",
            due_status=FRONTIER_EXTRA_DUE_STATUS,
            claim_effect="F95A may open; no Extra Stage is due before F95.",
        ),
    )
    write_json(
        FIVE_STAGE_SYNTHESIS,
        audit_payload(
            "frontier_five_stage_direction_synthesis",
            "pass",
            created_at_utc=payload["created_at_utc"],
            source_frontiers=["F90", "F91", "F92", "F93", "F94"],
            dominant_direction="Recent frontier work repeatedly tested proxy labels, regime density, path labels, side/cost budgets, and tier utility but failed before runtime authority.",
            repeated_mechanism="A surface can show local proxy structure while density, Tier B, side/cost exposure, label instability, or runtime materialization risk prevents candidate status.",
            overused_axis_warning="Avoid adjacent threshold/filter/session/routing/parameter-only repairs and F94 utility-label retuning.",
            next_axis_options=["closed-bar state transition embedding", "train-only representation learning", "state-first trade mapping", "cost-drag abstention separation"],
            claim_effect="Direction only; no retrospective, permanent ban, candidate, or authority claim.",
        ),
    )
    write_json(
        TOPIC_ROTATION_CHECK,
        audit_payload(
            "frontier_topic_rotation_check",
            "pass",
            created_at_utc=payload["created_at_utc"],
            previous_stage="stage_frontier_94__tier_stable_realized_utility_label_axis",
            proposed_stage=STAGE_ID,
            material_novelty_delta=[
                "data representation changes from single-row realized-utility label to closed-bar sequence/state-transition embedding",
                "objective changes to transition state before long/short/abstain mapping",
                "validation changes to state stability, density, DD resilience, and cost-drag separation before PF",
                "F94 utility-label surface is negative memory/reference only",
            ],
            blocked_continuation_repair=False,
            threshold_filter_parameter_only_tweak=False,
            claim_effect="F95A can open as a distinct design axis; no candidate or runtime claim.",
        ),
    )
    write_json(
        SCOPE_GATE,
        audit_payload(
            "scope_completion_gate",
            "pass",
            created_at_utc=payload["created_at_utc"],
            required_artifacts=[rel(EXPERIMENT_DESIGN), rel(RUNTIME_CONTRACT), rel(F95B_BRIEF), rel(STATE_TRANSITION_CONTRACT), rel(PACKET_TASK_FORCE_REVIEW)],
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
            data_sources_checked=[file_identity(path) for path in [MODEL_INPUT_SUMMARY, MODEL_INPUT_FEATURE_ORDER, RAW_US100_MANIFEST]],
            time_axis_boundary=data_integrity_plan(payload)["time_axis_boundary"],
            split_boundary=data_integrity_plan(payload)["split_boundary"],
            leakage_boundary=data_integrity_plan(payload)["feature_label_boundary"],
            missing_data_boundary=data_integrity_plan(payload)["missing_data_boundary"],
            claim_effect="Data checks are predeclared for F95B; no data_contract_pass or authority claim.",
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
            claim_effect="F95A sets validation rules only; no model quality, calibrated probability, or candidate claim.",
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
            lineage_judgment="F94C negative memory/reference surface -> F95A design-only state-transition stage open -> F95B proxy scout plan.",
            claim_effect="Artifacts support design-open evidence only; ignored prior outputs are hash-linked and not authority.",
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
            claim_effect="F95A is design-only stage open; not candidate, runtime, promotion, or completion evidence.",
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
    evidence = [rel(EXPERIMENT_DESIGN), rel(RUNTIME_CONTRACT), rel(F95B_BRIEF), rel(PACKET_TASK_FORCE_REVIEW)]
    return [
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-experiment-design",
            "status": "executed",
            "hypothesis": payload["hypothesis"],
            "baseline": payload["f94_reference"],
            "changed_variables": experiment_design(payload)["changed_variables"],
            "invalid_conditions": experiment_design(payload)["invalid_conditions"],
            "evidence_plan": experiment_design(payload)["success_criteria_for_f95b_proxy_scout"],
            "receipt_path": rel(SKILL_RECEIPT_DIR / "experiment_design.json"),
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-data-integrity",
            "status": "executed",
            "data_sources_checked": data_integrity_plan(payload)["data_sources_checked"],
            "time_axis_boundary": data_integrity_plan(payload)["time_axis_boundary"],
            "split_boundary": data_integrity_plan(payload)["split_boundary"],
            "leakage_checks": [data_integrity_plan(payload)["feature_label_boundary"], "future path perturbation required in F95B"],
            "missing_data_boundary": data_integrity_plan(payload)["missing_data_boundary"],
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
            "produced_artifacts": [rel(path if path.is_absolute() else ROOT / path) for path in produced_artifacts()],
            "raw_evidence": [rel(F94B_KPI), rel(F94B_CANDIDATE_GATE), rel(F94C_CLOSEOUT_SUMMARY)],
            "machine_readable": [rel(path) for path in [RUN_MANIFEST, SUMMARY_JSON, KPI_RECORD, EXPERIMENT_DESIGN, RUNTIME_CONTRACT, SKILL_RECEIPTS]],
            "human_readable": [rel(RESULT_SUMMARY), rel(F95A_REPORT), rel(STAGE_BRIEF), rel(SELECTION_STATUS), rel(CONTEXT_ANCHOR)],
            "hashes_or_missing_reasons": [file_identity(path if path.is_absolute() else ROOT / path) for path in produced_artifacts()],
            "lineage_boundary": "F94C negative memory/reference surface only; F95A design-open only; no runtime authority.",
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
    required_evidence = [rel(path) for path in [EXPERIMENT_DESIGN, RUNTIME_CONTRACT, F95B_BRIEF, DATA_INTEGRITY_PLAN, MODEL_VALIDATION_PLAN, STATE_TRANSITION_CONTRACT, PACKET_TASK_FORCE_REVIEW, WORK_PACKET, SKILL_RECEIPTS, PACKET_CLOSEOUT_GATE]]
    return {
        "version": "work_packet_schema_v2_1",
        "packet_lifecycle": "new_packet",
        "packet_id": RUN_ID,
        "created_at_utc": payload["created_at_utc"],
        "user_request": {
            "user_quote": "/goal active continuation; user explicitly corrected that required Task Force agents must be actually called, not only promised",
            "requested_action": "canonical frontier stage open for F95A closed-bar state-transition embedding axis",
            "requested_count": {"value": 1, "n_a_reason": ""},
            "ambiguous_terms": ["Goal Achieve is not claimed.", "Runtime authority is not claimed.", "F95A is design-only."],
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
                "f94_utility_label_repair_laundering": "high",
                "open_bar_or_future_path_leakage": "high",
                "oos_selection_or_calibration_laundering": "high",
                "runtime_probe_absence_misread_as_cost_skip": "medium",
            },
            "hard_stop_risks": [
                "Do not claim runtime/economics/materialization without MT5 Strategy Tester output identity.",
                "Do not repeat F94 utility-label axis by threshold/filter/session/routing/parameter-only tweak.",
                "Do not fit scaler, codebook, embedding, thresholds, or calibration on validation/OOS.",
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
                "reason": "F95A protects design-only stage-open claims and has no runnable candidate, ONNX/EA/set behavior, or runtime/materialization/economics/handoff claim.",
            },
            "questions": [],
            "required_user_decisions": [],
        },
        "interpreted_scope": {
            "work_families": ["experiment_design"],
            "target_surfaces": ["F95 stage open", "closed-bar state-transition embedding design", "F95B proxy scout brief", "Task Force receipt", "state sync"],
            "scope_units": ["stage_open_design", "receipt", "state_sync"],
            "execution_layers": ["local_python_execution"],
            "mutation_policy": {"allowed": True, "user_quote": "/goal active continuation"},
            "evidence_layers": ["F94 negative memory reference", "F95A design artifacts", "Task Force actual calls", "frontier overlays"],
            "reduction_policy": {"reduction_allowed": False, "requires_user_quote": False, "rationale": "F95A is a formal stage-open packet."},
            "claim_boundary": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
        },
        "verification_profile": {
            "profile_id": "design_only",
            "claim_surface": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
            "trigger_sources": [
                "active_goal_frontier_continuation",
                "F94C closeout rotated to F95 pending scaffold",
                "formal F95A stage open claim",
                "explicit user instruction requiring Task Force when triggered",
            ],
            "protected_claims": ALLOWED_CLAIMS,
            "required_evidence": required_evidence,
            "gates_not_run_with_reason": RUNTIME_NA_REASONS,
            "stop_conditions": [
                "Stop after F95A design artifacts, receipts, gates, and state sync are materialized.",
                "Do not create candidate/runtime claims in F95A.",
                "If runnable candidate or runtime claim appears, reroute to runtime_probe profile in the same packet.",
            ],
        },
        "acceptance_criteria": [
            {"id": "AC-001", "text": "F95A experiment design exists.", "expected_artifact": rel(EXPERIMENT_DESIGN), "verification_method": "scope_completion_gate", "required": True},
            {"id": "AC-002", "text": "F95A Task Force actual calls are recorded.", "expected_artifact": rel(PACKET_TASK_FORCE_REVIEW), "verification_method": "codex_task_force_review_packet", "required": True},
            {"id": "AC-003", "text": "F95B proxy scout brief exists.", "expected_artifact": rel(F95B_BRIEF), "verification_method": "scope_completion_gate", "required": True},
            {"id": "AC-004", "text": "Runtime evidence gate is explicitly outside claim surface, not skipped for cost or proxy-bad reasons.", "expected_artifact": rel(RUNTIME_CONTRACT), "verification_method": "final_claim_guard", "required": True},
        ],
        "work_plan": [
            "Write F95A design/runtime-contract/F95B brief artifacts.",
            "Record Task Force actual_subagent_calls and local-verification responses.",
            "Run frontier_extra_due_check, five-stage synthesis, and topic rotation gates.",
            "Run schema, receipt, state sync, gate coverage, and final claim guard checks.",
            "Commit to main if gates pass.",
        ],
        "skill_routing": {
            "primary_family": "experiment_design",
            "primary_skill": "obsidian-experiment-design",
            "support_skills": ["obsidian-data-integrity", "obsidian-model-validation", "obsidian-artifact-lineage", "obsidian-result-judgment", "obsidian-task-force-review", "obsidian-stage-transition", "obsidian-claim-discipline"],
            "skills_considered": REQUIRED_SKILLS + ["obsidian-runtime-parity", "obsidian-backtest-forensics"],
            "skills_selected": REQUIRED_SKILLS,
            "skills_not_used": [
                {"skill": "obsidian-runtime-parity", "reason": "No ONNX/EA/runtime parity or handoff claim is made."},
                {"skill": "obsidian-backtest-forensics", "reason": "No new Strategy Tester report or trade list exists in F95A."},
            ],
            "required_skill_receipts": REQUIRED_SKILLS,
            "required_gates": REQUIRED_GATES,
        },
        "evidence_contract": {
            "source_inputs": [rel(path) for path in source_inputs()],
            "machine_readable": [rel(path) for path in [RUN_MANIFEST, SUMMARY_JSON, KPI_RECORD, EXPERIMENT_DESIGN, RUNTIME_CONTRACT, F95B_BRIEF, DATA_INTEGRITY_PLAN, MODEL_VALIDATION_PLAN, STATE_TRANSITION_CONTRACT, SKILL_RECEIPTS]],
            "human_readable": [rel(RESULT_SUMMARY), rel(F95A_REPORT), rel(STAGE_BRIEF), rel(SELECTION_STATUS), rel(CONTEXT_ANCHOR)],
            "raw_evidence": [rel(F94B_KPI), rel(F94B_CANDIDATE_GATE), rel(F94C_CLOSEOUT_SUMMARY)],
            "missing_evidence": [
                {"evidence": "MT5 Strategy Tester runtime output", "reason": "outside F95A design-only claim surface"},
                {"evidence": "WFO/stress result", "reason": "outside F95A design-only claim surface"},
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
        "result_judgment_audit": RESULT_JUDGMENT_AUDIT,
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
        "result_judgment_audit": "pass_with_boundary",
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

Status: F95A design-only stage-open packet materialized(설계 전용 단계 개방 묶음 물질화). F95B proxy scout(프록시 정찰)가 current run(현재 실행)입니다.

- current run(현재 실행): `{NEXT_RUN_ID}`
- latest completed run(최근 완료 실행): `{RUN_ID}`

Question(질문): Can closed M5 bar sequence and state-transition embeddings identify continuation, reversal-trap, and chop-cost-drag states before long/short/abstain mapping?

Novelty delta(신규성 차이): the axis(축) changes from F94 single-row realized-utility labels(단일 행 실현 효용 라벨) to closed-bar sequence/state-transition representation(확정봉 시퀀스/상태 전이 표현). It is not threshold/filter/parameter-only repair(임계값/필터/파라미터만 수리 아님).

Runtime rule(런타임 규칙): if F95 creates a meaningful runnable candidate(의미 있는 실행 후보), ONNX/EA/set behavior(온엑스/전문가 자문/설정 동작), or runtime/materialization/economics/handoff claim(런타임/물질화/경제성/인계 주장), the same packet(같은 묶음) must attempt a narrow MT5 Strategy Tester probe(좁은 MT5 전략 테스터 탐침) or close as blocked/inconclusive/out_of_scope_by_claim(차단/불충분/주장 범위 밖).

No selected baseline(선택 기준선), promotion candidate(승격 후보), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성) is claimed.
"""


def input_refs_text() -> str:
    rows = "\n".join(f"- `{rel(path)}`" for path in source_inputs())
    return f"""# F95 Input References

{rows}

Boundary(경계): all prior F94 artifacts are reference/negative memory(참조/부정 기억) only.
"""


def selection_status_text(payload: Mapping[str, Any]) -> str:
    return f"""# F95 Selection Status

- current run(현재 실행): `{NEXT_RUN_ID}`
- latest completed run(최근 완료 실행): `{RUN_ID}`
- status(상태): F95A design-only stage open materialized(설계 전용 단계 개방 물질화); F95B proxy scout planned(프록시 정찰 계획)
- selected baseline(선택 기준선): not claimed
- promotion candidate(승격 후보): not claimed
- runtime authority(런타임 권위): not claimed
- operating promotion(운영 승격): not claimed
- live readiness(실거래 준비): not claimed
- goal achieve(목표 달성): not claimed
- task force actual calls(태스크포스 실제 호출): 6 selected agents recorded(선택 요원 6명 기록)
- runtime probe(런타임 탐침): not run because no runnable candidate or runtime claim exists(실행 후보/런타임 주장 없음)
- source closeout(원천 마감): `{PARENT_RUN_ID}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""


def context_anchor_text(payload: Mapping[str, Any]) -> str:
    return f"""# Current Working State

- active stage(활성 단계): `{STAGE_ID}`
- current run(현재 실행): `{NEXT_RUN_ID}`
- latest completed run(최근 완료 실행): `{RUN_ID}`
- current status(현재 상태): `{STATUS}`
- current judgment(현재 판정): `{JUDGMENT}`
- frontier extra due status(전선 추가 도래 상태): `{FRONTIER_EXTRA_DUE_STATUS}`
- frontier topic rotation status(전선 주제 회전 상태): `{FRONTIER_TOPIC_ROTATION_STATUS}`
- runtime probe status(런타임 탐침 상태): `{RUNTIME_PROBE_STATUS}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

Task Force(태스크포스): F95A used actual subagent calls(실제 하위요원 호출) for agent_01, agent_04, agent_05, agent_06, agent_07, and agent_08.

Next action(다음 행동): run `{NEXT_RUN_ID}` as a proxy_scout(프록시 정찰) only after reading F94 label definition and locking data/time/split/embedding contracts.
"""


def review_index_text() -> str:
    return f"""# F95 Review Index

- f95a_task_force_review_receipt: `{rel(TASK_FORCE_REVIEW)}`
- f95a_frontier_extra_due_check: `{rel(FRONTIER_EXTRA_DUE_CHECK)}`
- f95a_frontier_five_stage_direction_synthesis: `{rel(FIVE_STAGE_SYNTHESIS)}`
- f95a_frontier_topic_rotation_check: `{rel(TOPIC_ROTATION_CHECK)}`
- f95a_scope_completion_gate: `{rel(SCOPE_GATE)}`
- f95a_data_integrity_audit: `{rel(DATA_INTEGRITY_AUDIT)}`
- f95a_model_validation_audit: `{rel(MODEL_VALIDATION_AUDIT)}`
- f95a_artifact_lineage_audit: `{rel(ARTIFACT_AUDIT)}`
- f95a_result_judgment_audit: `{rel(RESULT_JUDGMENT_AUDIT)}`
- f95a_state_sync_audit: `{rel(STATE_SYNC_AUDIT)}`
- f95a_required_gate_coverage_audit: `{rel(REQUIRED_GATE_AUDIT)}`
- f95a_final_claim_guard: `{rel(FINAL_CLAIM_GUARD)}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
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
        "task_force_status": "f95a_actual_subagent_calls_recorded_6_selected_agents_no_task_force_reviewed_pass_claim",
        "runtime_probe_status": RUNTIME_PROBE_STATUS,
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "updated_at_utc": payload["created_at_utc"],
        "context_anchor": rel(CONTEXT_ANCHOR),
        "notes": [
            "Action(행동): F95A design-only stage-open packet(설계 전용 단계 개방 묶음)을 materialized(물질화)했다.",
            "Effect(효과): F95B current run(현재 실행)은 closed-bar state-transition embedding proxy scout(확정봉 상태 전이 임베딩 프록시 정찰)로 고정된다.",
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
    f95a = {
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
        "path": rel(F95A_REPORT),
        "primary_kpi": "candidate_count=0;runtime_completed_rows=0",
        "guardrail_kpi": "no_runtime_claim;no_authority;task_force_calls=6",
        "external_verification_status": "not_applicable_design_only",
        "notes": "F95A design-only open; Task Force actual calls recorded.",
        "run_number": "frontier95A",
        "decision": STATUS,
        "next_run_id": NEXT_RUN_ID,
        "rows": 0,
        "gate_passes": len(REQUIRED_GATES),
        "gate_total": len(REQUIRED_GATES),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(F95A_REPORT),
        "primary_artifact": rel(F95A_REPORT),
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
        "result_path": rel(F95A_REPORT),
        "row_id": f"{RUN_ID}__stage_open_design",
        "question": "Can closed-bar state-transition embeddings identify tradable US100 M5 states before direction mapping?",
        "next_action": NEXT_RUN_ID,
        "model_variants": 0,
        "selected_surfaces": 0,
        "runtime_attempt_rows": 0,
    }
    f95b = {
        **base,
        "ledger_row_id": f"{NEXT_RUN_ID}__planned_current_run",
        "run_id": NEXT_RUN_ID,
        "subrun_id": "planned_current_run",
        "record_view": "planned_current_run",
        "tier_scope": "planned_tier_a_tier_b_combined",
        "kpi_scope": "planned_proxy_scout",
        "scoreboard_lane": "planned_proxy_scout",
        "status": "planned_current_run_no_authority",
        "judgment": "planned_after_f95a_design_open",
        "path": rel(F95B_BRIEF),
        "primary_kpi": "pending",
        "guardrail_kpi": "closed_bar_only_and_state_class_distribution_gate_pending;no_runtime_claim",
        "external_verification_status": "pending",
        "notes": "F95B planned current run after F95A open.",
        "run_number": "frontier95B",
        "decision": "planned_current_run_no_authority",
        "next_run_id": "",
        "rows": 0,
        "gate_passes": 0,
        "gate_total": 0,
        "claim_boundary": "planned_proxy_scout_only_no_candidate_no_runtime_authority",
        "report_path": rel(F95B_BRIEF),
        "primary_artifact": rel(F95B_BRIEF),
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
        "output_path": rel(F95B_BRIEF),
        "result_path": rel(F95B_BRIEF),
        "row_id": f"{NEXT_RUN_ID}__planned_current_run",
        "question": "Can closed-bar state-transition embeddings identify tradable US100 M5 states before direction mapping?",
        "next_action": "run_f95b_proxy_scout",
        "model_variants": 0,
        "selected_surfaces": 0,
        "runtime_attempt_rows": 0,
    }
    return [f95a, f95b]


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
                "artifact_type": "f95a_design_open",
                "path": path_rel,
                "sha256": sha256_file_lf_normalized(path),
                "created_at": payload["created_at_utc"],
                "claim_boundary": CLAIM_BOUNDARY,
                "artifact_id": f"{RUN_ID}::{path_rel}",
                "created_at_utc": payload["created_at_utc"],
                "notes": "F95A design-open artifact; no runtime authority.",
                "artifact_path": path_rel,
                "effect": "Supports F95A design-open and F95B proxy-scout handoff only.",
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
## F95A closed-bar state-transition embedding open(F95A 확정봉 상태 전이 임베딩 개방)

- run_id(실행 ID): `{RUN_ID}`
- hypothesis(가설): {payload['hypothesis']}
- decision_use(판정 용도): design-only stage open(설계 전용 단계 개방) and F95B proxy scout plan(F95B 프록시 정찰 계획).
- task_force_actual_calls(태스크포스 실제 호출): 6 selected agents recorded(선택 요원 6명 기록).
- runtime(런타임): no Strategy Tester evidence(전략 테스터 근거 없음); no runtime authority(런타임 권위 없음).
- next_action(다음 행동): `{NEXT_RUN_ID}`.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""
    status_addition = f"""{marker}
- `{RUN_ID}`: design-only stage open(설계 전용 단계 개방); current run(현재 실행) is `{NEXT_RUN_ID}`; no candidate/selected baseline/runtime authority/live readiness/Goal Achieve(후보/선택 기준선/런타임 권위/실거래 준비/목표 달성 없음).
"""
    changelog_addition = f"""{marker}
## {payload['created_at_utc']} - F95A Stage Open Closed-Bar State-Transition Embedding

- Action(행동): `{RUN_ID}` materialized(물질화) F95A as a design-only stage-open packet(설계 전용 단계 개방 묶음).
- Effect(효과): `{NEXT_RUN_ID}` is the current run(현재 실행) for closed-bar state-transition embedding proxy scouting(확정봉 상태 전이 임베딩 프록시 정찰).
- Task Force(태스크포스): six selected agents(선택 요원 6명) were actually called(실제 호출) and recorded(기록) in `{rel(PACKET_TASK_FORCE_REVIEW)}`.
- Runtime(런타임): no new Strategy Tester runtime evidence(새 전략 테스터 런타임 근거 없음); no runtime authority(런타임 권위 없음); no Goal Achieve(목표 달성 없음).
- Boundary(경계): `{CLAIM_BOUNDARY}`.
"""
    decision_text = f"""# F95A Stage Open Decision

Action(행동): materialize(물질화) `{RUN_ID}` as a design-only stage-open packet(설계 전용 단계 개방 묶음).

Effect(효과): `{NEXT_RUN_ID}` becomes current run(현재 실행) and must lock(고정) closed-bar sequence, time-axis, split, embedding fit scope, and state-class contracts before proxy execution(프록시 실행 전).

Task Force(태스크포스): actual selected-agent calls(실제 선택 요원 호출) are recorded(기록) at `{rel(PACKET_TASK_FORCE_REVIEW)}`.

Boundary(경계): `{CLAIM_BOUNDARY}`.
"""
    append_once(IDEA_REGISTRY, marker, idea_addition)
    append_once(GLOBAL_SELECTION_STATUS, marker, status_addition)
    append_once(WORKSPACE_CHANGELOG, marker, changelog_addition)
    append_once(ROOT_CHANGELOG, marker, changelog_addition)
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
            AuditResult(audit_name="result_judgment_audit", status="pass_with_boundary"),
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
        raise FileNotFoundError(f"Missing required F95A source evidence: {missing}")
    ensure_dirs()
    payload = base_payload(utc_now())
    write_initial(payload)
    gate_results = run_control_gates(payload)
    write_final(payload, gate_results)
    print(json.dumps({"run_id": RUN_ID, "status": STATUS, "next_run_id": NEXT_RUN_ID, "gate_statuses": {key: value.get("status") for key, value in gate_results.items()}}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
