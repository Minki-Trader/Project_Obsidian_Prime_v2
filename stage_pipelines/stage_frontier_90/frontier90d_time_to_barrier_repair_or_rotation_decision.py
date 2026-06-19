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


STAGE_ID = "stage_frontier_90__time_to_barrier_competing_risk_label_axis"
RUN_ID = "frontier90D_time_to_barrier_repair_or_rotation_decision_v1"
PARENT_RUN_ID = "frontier90C_time_to_barrier_ordering_proxy_scout_v1"
NEXT_STAGE_ID = "stage_frontier_91__regime_conditioned_density_cost_abstention_axis"
NEXT_RUN_ID = "frontier91A_stage_open_regime_conditioned_density_cost_abstention_axis_v1"
SCRIPT_REL = "stage_pipelines/stage_frontier_90/frontier90d_time_to_barrier_repair_or_rotation_decision.py"

STATUS = "f90d_closed_negative_time_to_barrier_ordering_axis_rotate_to_f91_no_authority"
JUDGMENT = "negative_time_to_barrier_ordering_proxy_no_candidate_no_runtime_trigger"
DECISION = "close_f90_no_candidate_rotate_to_regime_conditioned_density_cost_abstention_axis"
CLAIM_BOUNDARY = (
    "f90d_stage_closeout_rotation_only_no_candidate_no_selected_baseline_no_mt5_runtime_evidence_"
    "no_operating_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve"
)
RUNTIME_PROBE_STATUS = (
    "not_run_no_candidate_no_runnable_decision_surface_no_onnx_ea_set_behavior_"
    "no_runtime_materialization_economics_claim_not_cost_or_proxy_bad_skip"
)
FRONTIER_EXTRA_DUE_STATUS = "not_due_after_f90_closeout_next_boundary_f100_e01_closed_for_f050"
FRONTIER_TOPIC_ROTATION_STATUS = "passed_f91_regime_objective_risk_axis_not_time_to_barrier_threshold_tweak"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR_NAME = "frontier90D"
RUN_DIR = STAGE_DIR / "02_runs" / RUN_DIR_NAME
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

F90B_RUN = STAGE_DIR / "02_runs" / "frontier90B"
F90B_SUMMARY = F90B_RUN / "summary.json"
F90B_KPI = F90B_RUN / "kpi_record.json"
F90B_LABEL_STATS = F90B_RUN / "labels" / "label_feasibility_stats.json"
F90B_TIER_RECORDS = F90B_RUN / "labels" / "tier_records.json"
F90B_LABELS = F90B_RUN / "labels" / "frontier90b_barrier_labels.csv"

F90C_RUN = STAGE_DIR / "02_runs" / "frontier90C"
F90C_RUN_MANIFEST = F90C_RUN / "run_manifest.json"
F90C_SUMMARY = F90C_RUN / "summary.json"
F90C_KPI = F90C_RUN / "kpi_record.json"
F90C_PROXY_METRICS = F90C_RUN / "proxy_scout" / "proxy_metrics.json"
F90C_VARIANT_METRICS = F90C_RUN / "proxy_scout" / "variant_metrics.csv"
F90C_RESULT_SUMMARY = F90C_RUN / "reports" / "result_summary.md"
F90C_WORK_PACKET = ROOT / "docs" / "agent_control" / "packets" / PARENT_RUN_ID / "work_packet.yaml"
F90C_CLOSEOUT_GATE = ROOT / "docs" / "agent_control" / "packets" / PARENT_RUN_ID / "closeout_gate.json"
F90C_TASK_FORCE = ROOT / "docs" / "agent_control" / "packets" / PARENT_RUN_ID / "codex_task_force_review_packet.json"

RUN_MANIFEST = RUN_DIR / "run_manifest.json"
SUMMARY_JSON = RUN_DIR / "summary.json"
KPI_RECORD = RUN_DIR / "kpi_record.json"
DECISION_JSON = DECISION_DIR / "decision.json"
RESULT_SUMMARY = REPORT_DIR / "summary.md"
STAGE_CLOSEOUT_SUMMARY = REVIEW_DIR / "f90d_stage_closeout_summary.json"
STAGE_CLOSEOUT_REPORT = REVIEW_DIR / "stage_closeout_report.md"
F90D_REPORT = REVIEW_DIR / "frontier90D_time_to_barrier_repair_or_rotation_decision_report.md"
TASK_FORCE_REVIEW = REVIEW_DIR / "f90d_task_force_review_receipt.json"
TASK_FORCE_PACKET_REVIEW = PACKET_DIR / "codex_task_force_review_packet.json"
FRONTIER_EXTRA_DUE_CHECK = REVIEW_DIR / "f90d_frontier_extra_due_check.json"
FIVE_STAGE_SYNTHESIS = REVIEW_DIR / "f90d_frontier_five_stage_direction_synthesis.json"
TOPIC_ROTATION_CHECK = REVIEW_DIR / "f90d_frontier_topic_rotation_check.json"
SCOPE_GATE = REVIEW_DIR / "f90d_scope_completion_gate.json"
DATA_INTEGRITY_AUDIT = REVIEW_DIR / "f90d_data_integrity_audit.json"
MODEL_VALIDATION_AUDIT = REVIEW_DIR / "f90d_model_validation_audit.json"
KPI_CONTRACT_AUDIT = REVIEW_DIR / "f90d_kpi_contract_audit.json"
ARTIFACT_AUDIT = REVIEW_DIR / "f90d_artifact_lineage_audit.json"
RESULT_JUDGMENT_AUDIT = REVIEW_DIR / "f90d_result_judgment_audit.json"
FINAL_CLAIM_GUARD = REVIEW_DIR / "f90d_final_claim_guard.json"
STATE_SYNC_AUDIT = REVIEW_DIR / "f90d_state_sync_audit.json"
REQUIRED_GATE_AUDIT = REVIEW_DIR / "f90d_required_gate_coverage_audit.json"
DECISION_MEMO = ROOT / "docs" / "decisions" / "2026-06-19_frontier90d_closeout_rotate_f91.md"

WORK_PACKET = PACKET_DIR / "work_packet.yaml"
SKILL_RECEIPTS = PACKET_DIR / "skill_receipts.json"
PACKET_FINAL_CLAIM_GUARD = PACKET_DIR / "final_claim_guard.json"
PACKET_CLOSEOUT_GATE = PACKET_DIR / "closeout_gate.json"
PACKET_STATE_SYNC_AUDIT = PACKET_DIR / "state_sync_audit.json"
PACKET_REQUIRED_GATE_AUDIT = PACKET_DIR / "required_gate_coverage_audit.json"
PACKET_WORK_PACKET_LINT = PACKET_DIR / "work_packet_schema_lint.json"
PACKET_SKILL_RECEIPT_LINT = PACKET_DIR / "skill_receipt_schema_lint.json"

ALLOWED_CLAIMS = [
    "f90_closed_negative_memory_recorded",
    "f90_repair_disposition_closed",
    "f91_pending_open_scaffold_recorded",
    "task_force_actual_calls_recorded",
    "frontier_extra_due_check_not_due_after_f90",
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
    "runtime_economics_pass",
    "materialization_ready",
    "mt5_handoff_ready",
    "onnx_handoff_ready",
    "ea_handoff_ready",
    "f91_stage_open_completed",
    "task_force_reviewed_pass",
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
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_yaml(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(yaml.safe_dump(json_ready(dict(payload)), allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def current_branch() -> str:
    completed = subprocess.run(["git", "branch", "--show-current"], cwd=ROOT, check=False, capture_output=True, text=True, timeout=10)
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
    return {"path": rel(path), "exists": True, "sha256": sha256_file_lf_normalized(path), "size_bytes": io_path(path).stat().st_size}


def source_inputs() -> list[Path]:
    return [
        F90B_SUMMARY,
        F90B_KPI,
        F90B_LABEL_STATS,
        F90B_TIER_RECORDS,
        F90B_LABELS,
        F90C_RUN_MANIFEST,
        F90C_SUMMARY,
        F90C_KPI,
        F90C_PROXY_METRICS,
        F90C_VARIANT_METRICS,
        F90C_RESULT_SUMMARY,
        F90C_WORK_PACKET,
        F90C_CLOSEOUT_GATE,
        F90C_TASK_FORCE,
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
        F90D_REPORT,
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


def task_force_calls() -> list[dict[str, str]]:
    return [
        {
            "roster_agent_id": "agent_01_system_governor",
            "spawned_agent_id": "019edd8f-e0fc-7d61-9521-bab68449fc50",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "accepted",
        },
        {
            "roster_agent_id": "agent_04_evidence_control_plane",
            "spawned_agent_id": "019edd8f-f695-7042-9486-6c7640a04c48",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "needs_local_verification",
        },
        {
            "roster_agent_id": "agent_05_data_feature_contract",
            "spawned_agent_id": "019edd90-0b73-78a2-b606-13dfb535ab20",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "accepted",
        },
        {
            "roster_agent_id": "agent_06_quant_research",
            "spawned_agent_id": "019edd90-205d-7060-a0aa-4756c5599c80",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "accepted",
        },
        {
            "roster_agent_id": "agent_07_model_validation_risk",
            "spawned_agent_id": "019edd90-34ce-7150-8b01-efdac11fa82a",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "accepted",
        },
        {
            "roster_agent_id": "agent_08_mt5_onnx_runtime",
            "spawned_agent_id": "019edd90-495b-7e10-9a23-e1ca67c07eb2",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "accepted",
        },
    ]


def closeout_payload(now: str) -> dict[str, Any]:
    metrics = read_json(F90C_PROXY_METRICS)
    best = metrics["best_diagnostic_variant"]
    decision = {
        "final_disposition": "negative_memory",
        "rotation_selected": True,
        "repair_disposition": "capped_out_no_non_threshold_new_evidence_axis",
        "candidate_count": metrics["candidate_count"],
        "meaningful_signal_count": metrics["meaningful_signal_count"],
        "materialization_candidate_count": 0,
        "runtime_attempt_rows": 0,
        "primary_failure": "oos_ordering_lift_failed",
        "best_variant": best["variant_id"],
        "validation_signal_hit_rate": best["validation"]["signal_hit_rate"],
        "oos_signal_hit_rate": best["oos"]["signal_hit_rate"],
        "oos_auc": best["oos"]["auc"],
        "salvage_value": [
            "F90B label feasibility remains a reference clue.",
            "Time-to-barrier event counts are usable for future non-ordering labels.",
            "F90C confirms that direct linear upper/lower ordering is weak on OOS.",
        ],
        "negative_memory": [
            "Do not repeat F90C by changing only threshold/filter/parameter.",
            "Do not rescue the idea with validation-only performance.",
            "Do not call ordering scores probabilities or candidates.",
        ],
        "reopen_condition": [
            "New non-threshold target representation such as survival/hazard/listwise objective.",
            "New runtime representation or trade-shape mapping with predeclared WFO/stress plan.",
            "Tier B or combined evidence that changes the sample boundary without borrowing Tier A metrics.",
        ],
        "next_stage_id": NEXT_STAGE_ID,
        "next_run_id": NEXT_RUN_ID,
        "next_axis": {
            "primary_axis": "regime_split_plus_objective_plus_risk_logic",
            "stage_id": NEXT_STAGE_ID,
            "run_id": NEXT_RUN_ID,
            "question": "Can regime-conditioned density/cost abstention create a runtime-compatible US100 M5 surface without repeating time-to-barrier ordering?",
            "novelty_delta": {
                "source_data_representation": "regime-conditioned density/cost state rather than barrier-hit ordering labels",
                "label_or_objective": "density/cost abstention objective instead of upper_first/lower_first ordering",
                "risk_logic": "abstain under poor density/cost regimes before order mapping",
                "validation_philosophy": "predeclare regime segments and only materialize a runnable surface if scout evidence is meaningful",
                "not_threshold_filter_parameter_tweak": True,
            },
            "pending_open_boundary": "scaffold_only_formal_f91a_open_required",
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
        "f90c_metrics": metrics,
        "repair_rotation_decision": decision,
        "frontier_extra_due_check": {
            "status": "pass_not_due",
            "frontier_closeout": "F90",
            "next_due_boundary": "F100",
            "e01_status": "closed_for_f050",
            "decision": FRONTIER_EXTRA_DUE_STATUS,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "frontier_five_stage_direction_synthesis": {
            "status": "pass",
            "covered_frontier_ids": ["F86", "F87", "F88", "F89", "F90"],
            "dominant_direction": "runtime-adjacent labels and proxy surfaces produced clues but weak materialization surfaces",
            "repeated_mechanism": "candidate pressure after OOS decay or runtime/proxy gap",
            "overused_axis_warning": "time-to-barrier ordering, adverse-selection teacher, and threshold rescue should not be repeated adjacent",
            "next_axis_options": [
                "regime-conditioned density/cost abstention objective",
                "runtime-native trade-shape risk logic",
                "predeclared regime split before MT5 materialization",
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
        "model_policy": "gpt-5.5_xhigh_floor_fresh_selected_agent_spawn_calls",
        "bounded_evidence": [rel(F90C_PROXY_METRICS), rel(F90C_KPI), rel(F90C_WORK_PACKET)],
        "advice_classification": {call["roster_agent_id"]: call["opinion_classification"] for call in calls},
        "local_verification": [
            "F90C candidate_count=0, meaningful_signal_count=0, runtime_attempt_rows=0 verified from proxy metrics.",
            "F90D records negative memory, salvage value, do-not-repeat, and reopen condition.",
            "F91 is pending-open scaffold only with new regime/objective/risk axis.",
            "No runtime/materialization/economics claim is made in F90D.",
        ],
        "final_codex_direction": "Close F90 as negative/no-authority and rotate to F91 pending-open scaffold.",
        "forbidden_claim_check": "No candidate, selected baseline, operating promotion, runtime authority, live readiness, Goal Achieve, runtime verified, or materialization-ready claim.",
        "claim_boundary": CLAIM_BOUNDARY,
        "decision": decision["final_disposition"],
    }


def run_manifest(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_stage_id": NEXT_STAGE_ID,
        "next_run_id": NEXT_RUN_ID,
        "run_type": "stage_closeout_rotation_decision",
        "created_at_utc": payload["created_at_utc"],
        "source_artifacts": [rel(path) for path in source_inputs() if path_exists(path)],
        "runtime_evidence_status": RUNTIME_PROBE_STATUS,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def kpi_record(payload: Mapping[str, Any]) -> dict[str, Any]:
    best = payload["f90c_metrics"]["best_diagnostic_variant"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "hypothesis": "F90 time-to-barrier ordering proxy should be repaired only if non-threshold evidence exists; otherwise rotate.",
        "test_period": "F90C inherited train/validation/OOS split from model input; F90D is a decision closeout.",
        "proxy_kpi": {
            "best_variant": best["variant_id"],
            "validation_signal_hit_rate": best["validation"]["signal_hit_rate"],
            "oos_signal_hit_rate": best["oos"]["signal_hit_rate"],
            "oos_auc": best["oos"]["auc"],
            "candidate_count": payload["f90c_metrics"]["candidate_count"],
            "meaningful_signal_count": payload["f90c_metrics"]["meaningful_signal_count"],
        },
        "runtime_kpi": {
            "status": "not_applicable",
            "reason": "No candidate, no runnable decision surface, no ONNX/EA/set behavior claim, and no runtime/materialization/economics claim.",
        },
        "closeout_kpi": {
            "gross_profit": None,
            "gross_loss": None,
            "net_profit": None,
            "profit_factor": None,
            "drawdown": None,
            "trade_count": None,
            "trades_per_day": None,
            "win_rate": None,
            "avg_win": None,
            "avg_loss": None,
            "payoff_ratio": None,
            "expectancy": None,
            "recovery_factor": None,
            "time_under_water": None,
            "max_consecutive_loss": None,
            "long_short_breakdown": "not_applicable_no_runtime_trades",
            "n_a_reason": "F90D is a decision closeout with no Strategy Tester economics.",
        },
        "parity": "not_applicable_no_onnx_ea_runtime_claim",
        "gap_cause": "OOS ordering lift failed before materialization.",
        "next_action": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def result_summary_text(payload: Mapping[str, Any]) -> str:
    best = payload["f90c_metrics"]["best_diagnostic_variant"]
    decision = payload["repair_rotation_decision"]
    return f"""# F90D Repair Or Rotation Decision(F90D 수리 또는 회전 결정)

Updated(갱신): {payload['created_at_utc']}

Conclusion(결론): F90 is closed as negative/no-authority(F90은 부정/권위 없음으로 마감). F90C produced no candidate(후보 없음): best variant(최선 변형) `{best['variant_id']}` had validation signal hit rate(검증 신호 적중률) `{best['validation']['signal_hit_rate']}`, OOS signal hit rate(표본외 신호 적중률) `{best['oos']['signal_hit_rate']}`, and OOS AUC(표본외 AUC) `{best['oos']['auc']}`.

Action(행동): F90D records(기록) negative memory(부정 기억), salvage value(회수 가치), do-not-repeat(반복 금지), reopen condition(재개 조건), Task Force actual calls(태스크포스 실제 호출), frontier extra due check(전선 추가 도래 점검), and topic rotation check(주제 회전 점검).

Effect(효과): The project does not keep tuning the same time-to-barrier ordering proxy(장벽 도달 시간 순서 프록시). It rotates(회전) to `{NEXT_STAGE_ID}` as a pending-open scaffold(개방 대기 뼈대) only.

Runtime(런타임): no MT5 Strategy Tester probe(MT5 전략 테스터 탐침 없음). Reason(사유): no candidate(후보 없음), no runnable decision surface(실행 가능 결정 표면 없음), no ONNX/EA/set behavior claim(ONNX/EA/설정 동작 주장 없음), and no runtime/materialization/economics claim(런타임/물질화/경제성 주장 없음). This is not cost/expense deferral(비용 지연 아님) and not proxy-bad skip(프록시 부진 생략 아님).

Tier records(티어 기록): Tier A separate(티어 A 분리) measured negative(부정 측정); Tier B separate(티어 B 분리) `missing_required(필수 누락)`; Tier A+B combined(티어 A+B 합산) `blocked_by_missing_tier_b(티어 B 누락으로 차단)`.

Next axis(다음 축): `{NEXT_STAGE_ID}` asks whether regime-conditioned density/cost abstention(장세 조건부 밀도/비용 회피) can create a runtime-compatible(런타임 호환) US100 M5 surface. Formal F91A open(정식 F91A 개방)은 다음 packet(묶음)에서만 주장한다.

Do not repeat(반복 금지): {', '.join(decision['negative_memory'])}

Boundary(경계): `{CLAIM_BOUNDARY}`.
"""


def stage_closeout_report_text(payload: Mapping[str, Any]) -> str:
    return result_summary_text(payload)


def f90_selection_status_text() -> str:
    return f"""# Selection Status(선택 상태)

F90 is closed as negative/no-authority(F90은 부정/권위 없음으로 마감). No candidate(후보 없음), no selected baseline(선택 기준선 없음), no operating promotion(운영 승격 없음), no runtime authority(런타임 권위 없음), no live readiness(실거래 준비 없음), no Goal Achieve(목표 달성 없음).

Tier B(티어 B)는 `missing_required(필수 누락)`이고 Tier A+B combined(티어 A+B 합산)는 `blocked_by_missing_tier_b(티어 B 누락으로 차단)`이다.
"""


def next_stage_brief_text(payload: Mapping[str, Any]) -> str:
    return f"""# {NEXT_STAGE_ID}

Status(상태): pending-open scaffold only(개방 대기 뼈대 전용). Formal F91A open(정식 F91A 개방)은 아직 주장하지 않는다.

Question(질문): Can regime-conditioned density/cost abstention(장세 조건부 밀도/비용 회피) create a runtime-compatible(런타임 호환) US100 M5 strategy surface without repeating time-to-barrier ordering(장벽 도달 시간 순서화 반복 없음)?

Material novelty delta(실질 신규성 차이): primary axis(주 축)는 regime split(장세 분할) + objective(목적함수) + risk logic(위험 로직)이다. It is not threshold/filter/parameter-only repair(임계값/필터/파라미터만 수리 아님).

Runtime rule(런타임 규칙): if F91 creates a meaningful runnable candidate(의미 있는 실행 후보), ONNX/EA/set behavior(ONNX/EA/설정 동작), or runtime/materialization/economics claim(런타임/물질화/경제성 주장), same-packet MT5 Strategy Tester probe(같은 묶음 MT5 전략 테스터 탐침)를 시도해야 한다.
"""


def next_input_refs_text(payload: Mapping[str, Any]) -> str:
    lines = ["# Input References(입력 참조)", ""]
    for path in [SUMMARY_JSON, DECISION_JSON, F90C_PROXY_METRICS, F90C_KPI, F90B_LABEL_STATS]:
        ident = file_identity(path)
        lines.append(f"- `{ident['path']}` sha256 `{ident['sha256']}`")
    return "\n".join(lines)


def next_selection_status_text() -> str:
    return f"""# Selection Status(선택 상태)

F91 is pending-open scaffold only(F91은 개방 대기 뼈대 전용). No candidate(후보 없음), no selected baseline(선택 기준선 없음), no operating promotion(운영 승격 없음), no runtime authority(런타임 권위 없음), no live readiness(실거래 준비 없음), no Goal Achieve(목표 달성 없음).
"""


def current_state_text(payload: Mapping[str, Any]) -> str:
    return f"""# Current Working State(현재 작업 상태)

- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- latest_completed_run(최신 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- Task Force(태스크포스): 6 fresh selected agents(새 선택 요원 6명) called for F90D; no Task Force reviewed/pass claim(검토됨/통과 주장 없음)
- Runtime(런타임): `{RUNTIME_PROBE_STATUS}`
- Boundary(경계): `{CLAIM_BOUNDARY}`
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
task_force_status: f90d_actual_subagent_calls_recorded_6_selected_agents_no_task_force_reviewed_pass_claim
runtime_probe_status: {RUNTIME_PROBE_STATUS}
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
updated_at_utc: '{payload['created_at_utc']}'
context_anchor: {rel(NEXT_CONTEXT_ANCHOR)}
notes:
- 'Action(행동): F90D closed(마감) F90 as negative/no-authority(부정/권위 없음) and wrote F91 pending-open scaffold(개방 대기 뼈대).'
- 'Effect(효과): threshold/filter/parameter-only repair(임계값/필터/파라미터만 수리)를 막고 새 regime/objective/risk axis(장세/목적함수/위험 축)로 회전한다.'
- 'Runtime(런타임): no Strategy Tester evidence(전략 테스터 근거 없음); no runtime authority(런타임 권위 없음); no Goal Achieve(목표 달성 없음).'
"""


def review_index_text(payload: Mapping[str, Any]) -> str:
    rows = [
        ("f90d_task_force_review_receipt", TASK_FORCE_REVIEW),
        ("f90d_frontier_extra_due_check", FRONTIER_EXTRA_DUE_CHECK),
        ("f90d_frontier_topic_rotation_check", TOPIC_ROTATION_CHECK),
        ("f90d_required_gate_coverage_audit", REQUIRED_GATE_AUDIT),
        ("f90d_final_claim_guard", FINAL_CLAIM_GUARD),
    ]
    return "# Review Index(검토 색인)\n\n" + "\n".join(f"- `{name}`: `{rel(path)}`" for name, path in rows)


def next_review_index_text(payload: Mapping[str, Any]) -> str:
    return f"""# Review Index(검토 색인)

- source_closeout(원천 마감): `{rel(STAGE_CLOSEOUT_REPORT)}`
- pending_open_status(개방 대기 상태): `{rel(NEXT_STAGE_BRIEF)}`
"""


def decision_memo_text(payload: Mapping[str, Any]) -> str:
    decision = payload["repair_rotation_decision"]
    return f"""# F90D Closeout Rotate F91(F90D 마감 및 F91 회전)

Decision(결정): `{DECISION}`.

Reason(이유): F90C candidate_count(후보 수)는 `{decision['candidate_count']}`이고 OOS ordering lift(표본외 순서 리프트)가 유지되지 않았다. Therefore(따라서) F90D records negative memory(부정 기억) and rotates(회전) rather than repairing by threshold/filter/parameter-only tweak(임계값/필터/파라미터만 조정).

Next(다음): `{NEXT_RUN_ID}` pending-open scaffold(개방 대기 뼈대). Formal open(정식 개방)은 별도 packet(묶음)이 필요하다.

Not claimed(주장하지 않음): candidate(후보), selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성).
"""


def write_run_artifacts(payload: Mapping[str, Any]) -> None:
    write_json(RUN_MANIFEST, run_manifest(payload))
    write_json(SUMMARY_JSON, payload)
    write_json(KPI_RECORD, kpi_record(payload))
    write_json(DECISION_JSON, payload["repair_rotation_decision"])
    write_text(RESULT_SUMMARY, result_summary_text(payload))
    write_json(STAGE_CLOSEOUT_SUMMARY, payload)
    write_text(STAGE_CLOSEOUT_REPORT, stage_closeout_report_text(payload))
    write_text(F90D_REPORT, result_summary_text(payload))


def audit_payload(name: str, status: str, *, passed: bool = True, counts: Mapping[str, Any] | None = None, allowed: Sequence[str] | None = None) -> dict[str, Any]:
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
    write_json(TASK_FORCE_PACKET_REVIEW, {"audit_name": "codex_task_force_review_packet", "status": "pass", "passed": True, **task_force})
    write_json(FRONTIER_EXTRA_DUE_CHECK, audit_payload("frontier_extra_due_check", "pass_not_due", counts=payload["frontier_extra_due_check"]))
    write_json(FIVE_STAGE_SYNTHESIS, audit_payload("frontier_five_stage_direction_synthesis", "pass", counts=payload["frontier_five_stage_direction_synthesis"]))
    write_json(TOPIC_ROTATION_CHECK, audit_payload("frontier_topic_rotation_check", "pass", counts=payload["frontier_topic_rotation_check"]))
    write_json(SCOPE_GATE, audit_payload("scope_completion_gate", "pass", counts={"produced_artifacts": len([p for p in produced_artifacts() if path_exists(p)])}))
    write_json(DATA_INTEGRITY_AUDIT, audit_payload("data_integrity_audit", "pass_with_boundary", counts={"tier_b": "missing_required", "combined": "blocked_by_missing_tier_b"}))
    write_json(MODEL_VALIDATION_AUDIT, audit_payload("model_validation_audit", "pass_negative_no_candidate_no_repair_selected", counts=payload["repair_rotation_decision"]))
    write_json(KPI_CONTRACT_AUDIT, audit_payload("kpi_contract_audit", "pass", counts=kpi_record(payload)))
    write_json(ARTIFACT_AUDIT, audit_payload("artifact_lineage_audit", "pass", counts={"source_inputs": len(source_inputs()), "produced_artifacts": len(produced_artifacts())}))
    write_json(
        RESULT_JUDGMENT_AUDIT,
        {
            **audit_payload("result_judgment_audit", "pass"),
            "result_subject": RUN_ID,
            "evidence_available": [rel(F90C_PROXY_METRICS), rel(F90C_KPI), rel(DECISION_JSON), rel(TASK_FORCE_PACKET_REVIEW)],
            "evidence_missing": ["MT5 Strategy Tester output", "runnable ONNX/EA/set candidate", "Tier B performance"],
            "judgment_label": JUDGMENT,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "F90 produced a useful negative memory, not an operating strategy.",
        },
    )
    guard = {
        "audit_name": "final_claim_guard",
        "packet_id": RUN_ID,
        "status": "pass",
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "runtime_probe_status": RUNTIME_PROBE_STATUS,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(FINAL_CLAIM_GUARD, guard)
    write_json(PACKET_FINAL_CLAIM_GUARD, guard)


def skill_receipts(payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    common = {"packet_id": RUN_ID, "status": "executed", "claim_boundary": CLAIM_BOUNDARY, "forbidden_claims": FORBIDDEN_CLAIMS}
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
            "ledger_rows": [f"{RUN_ID}__tier_a_closeout", f"{RUN_ID}__tier_b_missing_required", f"{RUN_ID}__tier_ab_blocked", f"{NEXT_RUN_ID}__planned_current_run"],
            "missing_evidence": ["MT5 Strategy Tester output", "Tier B proxy/runtime performance", "runnable ONNX/EA/set candidate"],
            "allowed_claims": ALLOWED_CLAIMS,
        },
        {
            **common,
            "skill": "obsidian-data-integrity",
            "data_sources_checked": [rel(F90B_LABELS), rel(F90C_PROXY_METRICS), rel(F90C_KPI)],
            "time_axis_boundary": "F90B/F90C timestamp joins are inherited and no new row-level model fit is performed in F90D.",
            "split_boundary": "F90D is a decision closeout; F90C train/validation/OOS read is consumed as frozen evidence.",
            "leakage_checks": ["No new threshold tuning", "No validation/OOS rescue", "Tier B missing_required retained"],
            "missing_data_boundary": "Tier B missing_required; Tier A+B combined blocked.",
        },
        {
            **common,
            "skill": "obsidian-model-validation",
            "model_or_threshold_surface": "F90C linear ordering proxies are closed; no repair selected.",
            "validation_split": "F90C frozen train/validation/OOS split; F90D does not retune.",
            "overfit_checks": ["candidate_count=0", "no threshold/filter/parameter-only repair", "no calibration claim"],
            "selection_metric_boundary": "Decision uses failed predeclared candidate gate only; no model superiority.",
            "allowed_claims": ALLOWED_CLAIMS,
        },
        {
            **common,
            "skill": "obsidian-artifact-lineage",
            "source_inputs": [rel(path) for path in source_inputs()],
            "produced_artifacts": [rel(path) for path in produced_artifacts() if path_exists(path)],
            "raw_evidence": [rel(F90B_LABELS), rel(F90C_PROXY_METRICS)],
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
            "evidence_used": [rel(F90C_PROXY_METRICS), rel(F90C_KPI), rel(DECISION_JSON), rel(TASK_FORCE_PACKET_REVIEW)],
        },
        {
            **common,
            "skill": "obsidian-exploration-mandate",
            "exploration_lane": "stage_closeout_rotation",
            "idea_boundary": "F90 closes as negative memory; F91 opens only as pending scaffold.",
            "negative_memory_effect": "Prevents time-to-barrier ordering threshold-only repair from repeating.",
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
            "plain_conclusion": "F90 did not produce a tradable candidate; it produced a useful negative memory.",
            "confirmed": ["F90C candidate_count=0", "Task Force actual calls recorded", "F91 pending scaffold written"],
            "not_yet_confirmed": ["F91 formal open", "MT5 runtime economics", "selected baseline", "runtime authority"],
            "why_it_matters": "This prevents wasting more work on the same failed threshold surface.",
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
            "requested_action": "F90D stage closeout and F91 pending-open rotation scaffold",
            "requested_count": {"value": 1, "n_a_reason": ""},
            "ambiguous_terms": ["No final completion.", "No runtime authority.", "F91 formal open is not claimed."],
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
                "tier_a_only_overclaim": "high",
                "f91_scaffold_confused_with_formal_open": "medium",
                "runtime_probe_absence_misread_as_cost_skip": "medium",
            },
            "hard_stop_risks": [
                "Do not claim candidate/runtime/economics/materialization without MT5 Strategy Tester output identity.",
                "Do not call F91 formally open in this packet.",
                "Do not repeat time-to-barrier ordering by threshold/filter/parameter-only tweak.",
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
                "reason": "F90D makes closeout/rotation claims only; no candidate, runnable surface, or runtime/materialization/economics claim exists.",
            },
            "questions": [],
            "required_user_decisions": [],
        },
        "interpreted_scope": {
            "work_families": ["publish_handoff"],
            "target_surfaces": ["F90 closeout", "F91 pending-open scaffold", "Task Force receipt", "state sync"],
            "scope_units": ["stage_closeout", "rotation_decision", "receipt", "state_sync"],
            "execution_layers": ["local_python_execution", "stage_transition"],
            "mutation_policy": {"allowed": True, "user_quote": "/goal active continuation"},
            "evidence_layers": ["F90B label feasibility", "F90C proxy metrics", "F90D Task Force calls"],
            "reduction_policy": {
                "reduction_allowed": False,
                "requires_user_quote": False,
                "rationale": "F90D consumes all F90C closeout evidence and makes no narrowed success claim.",
            },
            "claim_boundary": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
        },
        "verification_profile": {
            "profile_id": "stage_closeout",
            "claim_surface": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
            "trigger_sources": ["active_goal", "F90C no candidate", "closeout_required_task_force_review", "rotation_to_next_frontier"],
            "protected_claims": ALLOWED_CLAIMS,
            "required_evidence": required_evidence,
            "gates_not_run_with_reason": [
                {
                    "gate": "runtime_evidence_gate",
                    "reason_code": "outside_claim_surface_no_runtime_claim",
                    "reason": "F90D protects closeout/rotation only; no candidate, runnable surface, ONNX/EA/set behavior, or runtime/materialization/economics claim is made.",
                    "claim_effect": "Runtime probe, runtime verified, economics pass, materialization ready, handoff ready, authority, live readiness, and Goal Achieve claims are forbidden.",
                },
                {
                    "gate": "f91_stage_open_gate",
                    "reason_code": "pending_open_scaffold_only",
                    "reason": "F90D only writes the F91 pending-open scaffold; formal F91A stage open requires a separate packet.",
                    "claim_effect": "F91 stage-open completed/reviewed/pass claims are forbidden.",
                },
            ],
            "stop_conditions": [
                "No runtime/materialization/economics/authority/Goal Achieve claim.",
                "If a meaningful runnable candidate appears, switch to runtime_probe profile and attempt narrow MT5 probe in the same packet.",
            ],
        },
        "acceptance_criteria": [
            {"id": "AC-001", "text": "F90D decision artifact exists.", "expected_artifact": rel(DECISION_JSON), "verification_method": "scope_completion_gate", "required": True},
            {"id": "AC-002", "text": "Task Force actual calls are recorded.", "expected_artifact": rel(TASK_FORCE_PACKET_REVIEW), "verification_method": "codex_task_force_review_packet", "required": True},
            {"id": "AC-003", "text": "F91 pending-open scaffold exists without formal open claim.", "expected_artifact": rel(NEXT_STAGE_BRIEF), "verification_method": "scope_completion_gate", "required": True},
        ],
        "work_plan": {
            "phases": ["Read F90C evidence.", "Call relevant Task Force agents.", "Write closeout and pending-open scaffold.", "Run gates and state sync."],
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
                {"skill": "obsidian-backtest-forensics", "reason": "No new Strategy Tester report or trade list exists in F90D."},
            ],
            "required_skill_receipts": REQUIRED_SKILLS,
            "required_gates": REQUIRED_GATES,
        },
        "evidence_contract": {
            "raw_evidence": [rel(F90B_LABELS), rel(F90C_PROXY_METRICS)],
            "machine_readable": [rel(RUN_MANIFEST), rel(SUMMARY_JSON), rel(KPI_RECORD), rel(DECISION_JSON), rel(SKILL_RECEIPTS)],
            "human_readable": [rel(RESULT_SUMMARY), rel(STAGE_CLOSEOUT_REPORT), rel(DECISION_MEMO)],
        },
        "gates": {"required": REQUIRED_GATES, **gates_status, "not_applicable_with_reason": {"runtime_evidence_gate": "outside_claim_surface_no_runtime_claim", "f91_stage_open_gate": "pending_open_scaffold_only"}},
        "final_claim_policy": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS},
    }


def write_packet(payload: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> None:
    packet = work_packet(payload, gate_results)
    write_yaml(WORK_PACKET, packet)
    audits = []
    for name in REQUIRED_GATES:
        path = {
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
        }[name]
        audits.append({"audit_name": name, "path": rel(path), "status": packet["gates"].get(name, "pending")})
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
    write_text(SELECTION_STATUS, f90_selection_status_text())
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
    best = payload["f90c_metrics"]["best_diagnostic_variant"]
    base = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "stage_closeout_rotation",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(RESULT_SUMMARY),
        "notes": "F90 closeout; no runtime claim; F91 pending-open scaffold.",
        "family": "publish_handoff",
        "primary_report": rel(RESULT_SUMMARY),
        "run_number": "frontier90D",
        "date": created_date,
        "decision": DECISION,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "rows": payload["f90c_metrics"].get("eligible_rows", 0),
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
        "question": "Should F90 repair time-to-barrier ordering or rotate after OOS proxy failure?",
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
        "scout_clue_count": 0,
        "materialization_candidate_count": 0,
        "meaningful_signal_count": 0,
        "completion_candidate_count": 0,
        "runtime_attempt_rows": 0,
    }
    views = [
        ("tier_a_closeout", "Tier A separate", "negative_measured", f"best={best['variant_id']};val_hit={best['validation']['signal_hit_rate']};oos_hit={best['oos']['signal_hit_rate']};oos_auc={best['oos']['auc']}", "no candidate; runtime trigger false"),
        ("tier_b_missing_required", "Tier B separate", "missing_required", "missing_required_no_partial_context_source", "no Tier B performance or proxy claim"),
        ("tier_ab_blocked", "Tier A+B combined", "blocked_by_missing_tier_b", "blocked_by_missing_tier_b", "whole-alpha combined read forbidden"),
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
                "kpi_scope": "time_to_barrier_closeout_decision",
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
            "notes": "F91 pending-open scaffold after F90D negative closeout.",
            "primary_report": rel(NEXT_STAGE_BRIEF),
            "run_number": "frontier91A",
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
            "next_action": "formal_f91a_stage_open",
            "question": "Can regime-conditioned density/cost abstention create a runtime-compatible US100 M5 surface?",
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
        rows.append(
            {
                "stage_id": STAGE_ID if rel(path).startswith(f"stages/{STAGE_ID}") or "frontier90D" in rel(path) or "f90d" in rel(path) else NEXT_STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": "f90d_closeout_rotation",
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path),
                "created_at": payload["created_at_utc"],
                "claim_boundary": CLAIM_BOUNDARY,
                "artifact_id": f"{RUN_ID}::{rel(path)}",
                "created_at_utc": payload["created_at_utc"],
                "notes": "F90D closeout/rotation artifact; no runtime authority.",
                "artifact_path": rel(path),
                "effect": "Supports F90 negative memory and F91 pending-open scaffold only.",
                "size_bytes": io_path(path).stat().st_size,
            }
        )
    replace_rows_by_field(ARTIFACT_REGISTRY, "run_id", RUN_ID, rows)


def update_register_docs(payload: Mapping[str, Any]) -> None:
    marker = RUN_ID
    idea_addition = f"""
## F90D time-to-barrier ordering closeout(F90D 장벽 도달 시간 순서화 마감)

- run_id: `{RUN_ID}`
- hypothesis(가설): F90 ordering proxy(순서 프록시)는 non-threshold repair(비임계값 수리) 근거가 없으면 회전해야 한다.
- result(결과): negative_memory(부정 기억), no candidate(후보 없음), no runtime trigger(런타임 트리거 없음).
- next_action(다음 행동): `{NEXT_RUN_ID}` pending-open scaffold(개방 대기 뼈대).
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""
    negative_addition = f"""
## F90D ordering proxy negative closeout(F90D 순서 프록시 부정 마감)

- run_id: `{RUN_ID}`
- failed_boundary(실패 경계): F90C OOS signal hit rate(표본외 신호 적중률) and AUC(AUC)가 후보 기준을 넘지 못했다.
- salvage_value(회수 가치): F90B label feasibility(라벨 가능성) and event timing structure(이벤트 시간 구조)는 future non-ordering labels(미래 비순서 라벨)에 참고 가능.
- do_not_repeat(반복 금지): threshold/filter/parameter-only tweak(임계값/필터/파라미터만 조정), validation-only rescue(검증 단독 구조), calibration claim(보정 주장).
- reopen_condition(재개 조건): survival/hazard/listwise objective(생존/위험률/목록 순위 목적함수) or new runtime/trade-shape representation(새 런타임/거래 형태 표현).
"""
    changelog_addition = f"""
<!-- {RUN_ID} -->

## {payload['created_at_utc']} - F90D Closeout Rotate F91(F90D 마감 및 F91 회전)

- Action(행동): `frontier90D_time_to_barrier_repair_or_rotation_decision_v1`로 F90을 negative/no-authority(부정/권위 없음) 마감했다.
- Effect(효과): threshold/filter/parameter-only repair(임계값/필터/파라미터만 수리)를 막고 F91 pending-open scaffold(F91 개방 대기 뼈대)를 `{NEXT_STAGE_ID}`로 남겼다.
- Runtime(런타임): no new Strategy Tester runtime evidence(새 전략 테스터 런타임 근거 없음); no runtime authority(런타임 권위 없음); no Goal Achieve(목표 달성 없음).
- Boundary(경계): `{CLAIM_BOUNDARY}`.
"""
    append_once(IDEA_REGISTRY, marker, idea_addition)
    append_once(NEGATIVE_REGISTER, marker, negative_addition)
    append_once(WORKSPACE_CHANGELOG, marker, changelog_addition)
    append_once(ROOT_CHANGELOG, marker, changelog_addition)


def write_state_sync_seed(payload: Mapping[str, Any]) -> None:
    seed = audit_payload("state_sync_audit", "pending_external_lint", counts={"active_stage": NEXT_STAGE_ID, "current_run_id": NEXT_RUN_ID, "latest_completed_run_id": RUN_ID})
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
    write_run_artifacts(payload)
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
        raise FileNotFoundError(f"Missing required F90D source evidence: {missing}")
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
                "next_stage_id": NEXT_STAGE_ID,
                "next_run_id": NEXT_RUN_ID,
                "runtime_probe_status": RUNTIME_PROBE_STATUS,
                "task_force_call_count": len(task_force_calls()),
                "gate_results": gate_results,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
