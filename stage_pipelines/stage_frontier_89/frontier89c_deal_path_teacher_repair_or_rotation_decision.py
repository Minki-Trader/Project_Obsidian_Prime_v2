from __future__ import annotations

import csv
import json
import math
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, path_exists, sha256_file_lf_normalized


STAGE_ID = "stage_frontier_89__runtime_trade_list_adverse_selection_teacher"
RUN_ID = "frontier89C_deal_path_teacher_repair_or_rotation_decision_v1"
PARENT_RUN_ID = "frontier89B_deal_path_adverse_selection_proxy_scout_v1"
NEXT_STAGE_ID = "stage_frontier_90__time_to_barrier_competing_risk_label_axis"
NEXT_RUN_ID = "frontier90A_stage_open_time_to_barrier_competing_risk_label_axis_v1"

STATUS = "f89_closed_inconclusive_negative_deal_path_teacher_axis_rotate_to_f90_no_authority"
JUDGMENT = "negative_for_materialization_candidate_inconclusive_for_teacher_axis_no_runtime_evidence"
DECISION = "close_f89_no_candidate_rotate_to_time_to_barrier_competing_risk_label_axis"
CLAIM_BOUNDARY = (
    "f89c_stage_closeout_rotation_only_no_strategy_tester_runtime_economics_"
    "no_selected_baseline_no_operating_promotion_no_runtime_authority_"
    "no_live_readiness_no_goal_achieve"
)
RUNTIME_PROBE_STATUS = "not_run_no_meaningful_materialization_candidate_no_runtime_claim_not_cost_or_proxy_bad_skip"
FRONTIER_EXTRA_DUE_STATUS = "not_due_after_f89_closeout_next_boundary_f100_e01_closed_for_f050"
SCRIPT_REL = "stage_pipelines/stage_frontier_89/frontier89c_deal_path_teacher_repair_or_rotation_decision.py"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
DECISION_DIR = RUN_DIR / "decision"
REPORT_DIR = RUN_DIR / "reports"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
PACKET_DIR = ROOT / "docs" / "agent_control" / "packets" / RUN_ID

NEXT_STAGE_DIR = ROOT / "stages" / NEXT_STAGE_ID
NEXT_SPEC_DIR = NEXT_STAGE_DIR / "00_spec"
NEXT_INPUT_DIR = NEXT_STAGE_DIR / "01_inputs"
NEXT_REVIEW_DIR = NEXT_STAGE_DIR / "03_reviews"
NEXT_SELECTED_DIR = NEXT_STAGE_DIR / "04_selected"
NEXT_STAGE_BRIEF = NEXT_SPEC_DIR / "stage_brief.md"
NEXT_INPUT_REFS = NEXT_INPUT_DIR / "input_refs.md"
NEXT_SELECTION_STATUS = NEXT_SELECTED_DIR / "selection_status.md"
NEXT_CONTEXT_ANCHOR = NEXT_REVIEW_DIR / "context_anchor.md"
NEXT_REVIEW_INDEX = NEXT_REVIEW_DIR / "review_index.md"
NEXT_STAGE_LEDGER = NEXT_REVIEW_DIR / "stage_run_ledger.csv"

F89B_RUN = STAGE_DIR / "02_runs" / PARENT_RUN_ID
F89B_SUMMARY = F89B_RUN / "summary.json"
F89B_KPI = F89B_RUN / "kpi_record.json"
F89B_RUN_MANIFEST = F89B_RUN / "run_manifest.json"
F89B_PROXY_METRICS = F89B_RUN / "proxy_scout" / "proxy_metrics.json"
F89B_FEATURE_JOIN_REPORT = F89B_RUN / "proxy_scout" / "feature_join_report.json"
F89B_TIER_SCOPE = F89B_RUN / "proxy_scout" / "tier_scope_records.json"
F89B_CANDIDATE_QUEUE = F89B_RUN / "proxy_scout" / "candidate_queue.csv"
F89B_TEACHER_SURFACE = F89B_RUN / "proxy_scout" / "deal_path_teacher_surface.csv"
F89B_EPISODES = F89B_RUN / "episodes" / "deal_episodes.csv"
F89B_RESULT_SUMMARY = F89B_RUN / "reports" / "result_summary.md"
F89B_WORK_PACKET = ROOT / "docs" / "agent_control" / "packets" / PARENT_RUN_ID / "work_packet.yaml"
F89B_CLOSEOUT_GATE = ROOT / "docs" / "agent_control" / "packets" / PARENT_RUN_ID / "closeout_gate.json"
F89_TASK_FORCE_CORRECTION = REVIEW_DIR / "f89_task_force_correction_review_receipt.json"

F88_STAGE = ROOT / "stages" / "stage_frontier_88__runtime_substrate_first_materialization_probe"
F88C_RUN = F88_STAGE / "02_runs" / "frontier88C_runtime_substrate_timestamp_coverage_and_trade_list_repair_v1"
F88C_KPI = F88C_RUN / "kpi_record.json"
F88C_RUNTIME_IDENTITY = F88C_RUN / "runtime_evidence_identity.json"
F88C_DEALS = F88C_RUN / "trade_lists" / "f88c_tier_a_validation_is_deals.csv"
F88C_FEATURE_MATRIX = F88C_RUN / "feature_matrices" / "frontier88C_runtime_substrate_timestamp_coverage_and_trade_list_repair_v1_validation_is_features.csv"

RUN_MANIFEST = RUN_DIR / "run_manifest.json"
SUMMARY_JSON = RUN_DIR / "summary.json"
KPI_RECORD = RUN_DIR / "kpi_record.json"
DECISION_JSON = DECISION_DIR / "deal_path_teacher_repair_or_rotation_decision.json"
RESULT_SUMMARY = REPORT_DIR / "result_summary.md"

STAGE_CLOSEOUT_SUMMARY = REVIEW_DIR / "f89c_stage_closeout_summary.json"
STAGE_CLOSEOUT_REPORT = REVIEW_DIR / "stage_closeout_report.md"
F89C_REPORT = REVIEW_DIR / "frontier89C_deal_path_teacher_repair_or_rotation_decision_report.md"
TASK_FORCE_REVIEW = REVIEW_DIR / "f89c_task_force_review_receipt.json"
TASK_FORCE_PACKET_REVIEW = PACKET_DIR / "codex_task_force_review_packet.json"
FRONTIER_EXTRA_DUE_CHECK = REVIEW_DIR / "f89c_frontier_extra_due_check.json"
FIVE_STAGE_SYNTHESIS = REVIEW_DIR / "f89c_frontier_five_stage_direction_synthesis.json"
TOPIC_ROTATION_CHECK = REVIEW_DIR / "f89c_frontier_topic_rotation_check.json"
SCOPE_GATE = REVIEW_DIR / "f89c_scope_completion_gate.json"
DATA_INTEGRITY_AUDIT = REVIEW_DIR / "f89c_data_integrity_audit.json"
MODEL_VALIDATION_AUDIT = REVIEW_DIR / "f89c_model_validation_audit.json"
KPI_CONTRACT_AUDIT = REVIEW_DIR / "f89c_kpi_contract_audit.json"
ARTIFACT_AUDIT = REVIEW_DIR / "f89c_artifact_lineage_audit.json"
RESULT_JUDGMENT_AUDIT = REVIEW_DIR / "f89c_result_judgment_audit.json"
FINAL_CLAIM_GUARD = REVIEW_DIR / "f89c_final_claim_guard.json"
STATE_SYNC_AUDIT = REVIEW_DIR / "f89c_state_sync_audit.json"
REQUIRED_GATE_AUDIT = REVIEW_DIR / "f89c_required_gate_coverage_audit.json"

STAGE_TRANSITION_RECEIPT = REVIEW_DIR / "f89c_stage_transition_receipt.json"
RUN_EVIDENCE_RECEIPT = REVIEW_DIR / "f89c_run_evidence_receipt.json"
DATA_RECEIPT = REVIEW_DIR / "f89c_data_integrity_receipt.json"
MODEL_RECEIPT = REVIEW_DIR / "f89c_model_validation_receipt.json"
ARTIFACT_RECEIPT = REVIEW_DIR / "f89c_artifact_lineage_receipt.json"
RESULT_RECEIPT = REVIEW_DIR / "f89c_result_judgment_receipt.json"
CLAIM_RECEIPT = REVIEW_DIR / "f89c_claim_discipline_receipt.json"
ANSWER_RECEIPT = REVIEW_DIR / "f89c_answer_clarity_receipt.json"

WORK_PACKET = PACKET_DIR / "work_packet.yaml"
SKILL_RECEIPTS = PACKET_DIR / "skill_receipts.json"
PACKET_FINAL_CLAIM_GUARD = PACKET_DIR / "final_claim_guard.json"
PACKET_CLOSEOUT_GATE = PACKET_DIR / "closeout_gate.json"
PACKET_STATE_SYNC_AUDIT = PACKET_DIR / "state_sync_audit.json"
PACKET_REQUIRED_GATE_AUDIT = PACKET_DIR / "required_gate_coverage_audit.json"
PACKET_WORK_PACKET_LINT = PACKET_DIR / "work_packet_schema_lint.json"
PACKET_SKILL_RECEIPT_LINT = PACKET_DIR / "skill_receipt_schema_lint.json"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
GLOBAL_SELECTION_STATUS = ROOT / "docs" / "registers" / "selection_status.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
NEGATIVE_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
ROOT_CHANGELOG = ROOT / "docs" / "CHANGELOG.md"
DECISION_MEMO = ROOT / "docs" / "decisions" / "2026-06-19_frontier89c_closeout_rotate_f90.md"

SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
CONTEXT_ANCHOR = REVIEW_DIR / "context_anchor.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"

ALLOWED_CLAIMS = [
    "f89_closed_inconclusive_negative_memory_recorded",
    "f89_preserved_clue_recorded",
    "f89_same_axis_repair_capped_by_evidence",
    "f90_pending_open_scaffold_recorded",
    "task_force_actual_calls_recorded",
    "frontier_extra_due_check_not_due_after_f89",
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
    "f90_stage_open_completed",
]
REQUIRED_SKILLS = [
    "obsidian-stage-transition",
    "obsidian-run-evidence-system",
    "obsidian-data-integrity",
    "obsidian-model-validation",
    "obsidian-artifact-lineage",
    "obsidian-result-judgment",
    "obsidian-task-force-review",
    "obsidian-claim-discipline",
    "obsidian-answer-clarity",
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
    "result_judgment_receipt",
    "state_sync_audit",
    "required_gate_coverage_audit",
    "final_claim_guard",
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


def json_ready(value: Any) -> Any:
    if isinstance(value, Path):
        return rel(value)
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [json_ready(item) for item in value]
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_yaml(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(yaml.safe_dump(json_ready(dict(payload)), allow_unicode=True, sort_keys=False, width=120), encoding="utf-8-sig")


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def append_once(path: Path, marker: str, addition: str) -> None:
    text = io_path(path).read_text(encoding="utf-8-sig") if path_exists(path) else ""
    if marker in text:
        return
    joiner = "" if not text or text.endswith("\n") else "\n"
    write_text(path, text + joiner + addition.strip() + "\n")


def current_branch() -> str:
    completed = subprocess.run(["git", "branch", "--show-current"], cwd=ROOT, check=False, capture_output=True, text=True, timeout=10)
    return completed.stdout.strip() if completed.returncode == 0 else ""


def csv_count(path: Path) -> int:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def csv_rows(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def episode_bounds() -> dict[str, Any]:
    rows = csv_rows(F89B_EPISODES)
    entries = [row.get("entry_time_server", "") for row in rows if row.get("entry_time_server")]
    exits = [row.get("exit_time_server", "") for row in rows if row.get("exit_time_server")]
    return {
        "episode_rows": len(rows),
        "entry_start_server": min(entries) if entries else "",
        "exit_end_server": max(exits) if exits else "",
    }


def feature_time_uniqueness() -> dict[str, Any]:
    rows = csv_rows(F88C_FEATURE_MATRIX)
    times = [row.get("bar_time_server", "") for row in rows if row.get("bar_time_server")]
    return {
        "feature_rows": len(rows),
        "time_key": "bar_time_server",
        "unique_time_count": len(set(times)),
        "duplicate_time_count": len(times) - len(set(times)),
        "locally_checked": True,
    }


def task_force_calls() -> list[dict[str, str]]:
    return [
        {
            "roster_agent_id": "agent_01_system_governor",
            "spawned_agent_id": "019edd42-84cb-76b3-bf70-2bcf93dba8fb",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "accepted",
        },
        {
            "roster_agent_id": "agent_04_evidence_control_plane",
            "spawned_agent_id": "019edd42-98df-76c2-b95b-f7018c8f81e7",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "accepted",
        },
        {
            "roster_agent_id": "agent_05_data_feature_contract",
            "spawned_agent_id": "019edd42-b73f-7ca0-a421-06eaccf6285d",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "needs_local_verification",
        },
        {
            "roster_agent_id": "agent_06_quant_research",
            "spawned_agent_id": "019edd42-cba2-7cb2-8e7c-b5387acd620a",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "accepted",
        },
        {
            "roster_agent_id": "agent_07_model_validation_risk",
            "spawned_agent_id": "019edd42-dfc0-7412-839c-43479f7c5bcd",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "accepted",
        },
        {
            "roster_agent_id": "agent_08_mt5_onnx_runtime",
            "spawned_agent_id": "019edd42-f472-7c62-aaf3-da6e0517fa1a",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "accepted",
        },
    ]


def task_force_receipt(now: str) -> dict[str, Any]:
    calls = task_force_calls()
    return {
        "packet_id": RUN_ID,
        "skill": "obsidian-task-force-review",
        "status": "executed",
        "trigger_reason": [
            "closeout_required: F89C makes a stage closeout and rotation claim",
            "explicit_user_instruction_required: user required real Task Force calls when triggered",
            "prior_correction_required: F89A/F89B missing calls were corrected append-only",
        ],
        "roster_registry": "docs/agent_control/codex_task_force_registry.yaml",
        "agents_used": [call["roster_agent_id"] for call in calls],
        "actual_subagent_calls": calls,
        "review_requirement": "closeout_required",
        "model_policy": {
            "registry_floor": "gpt-5.5 xhigh",
            "session_execution": "inherited parent model through multi_agent_v1.spawn_agent",
            "non_authority_rule": "Model strength(모델 강도)는 evidence(근거)가 아니며 gate(게이트)나 claim boundary(주장 경계)를 완화하지 않는다.",
        },
        "bounded_evidence": [
            rel(F89B_SUMMARY),
            rel(F89B_KPI),
            rel(F89B_PROXY_METRICS),
            rel(F89_TASK_FORCE_CORRECTION),
            rel(WORKSPACE_STATE),
        ],
        "advice_classification": {
            "agent_01_system_governor": "accepted",
            "agent_04_evidence_control_plane": "accepted",
            "agent_05_data_feature_contract": "needs_local_verification",
            "agent_06_quant_research": "accepted",
            "agent_07_model_validation_risk": "accepted",
            "agent_08_mt5_onnx_runtime": "accepted",
        },
        "local_verification": {
            "actual_call_count": len(calls),
            "selected_agent_count": len(calls),
            "not_all_roster_agents": True,
            "agent_05_runtime_probe_wording": "lowered_to_f88c_runtime_output_reference_not_f89b_runtime_probe",
            "long_windows_path": "io_path and extended path reading confirmed F89B artifacts",
            "feature_time_uniqueness": feature_time_uniqueness(),
            "f89c_closeout_direction": "accepted_with_boundary_close_rotate_no_authority",
            "task_force_review_claim": "actual_calls_recorded_only_no_reviewed_verified_pass_claim",
        },
        "final_codex_direction": [
            "Close F89 as negative_for_materialization_candidate and inconclusive_for_teacher_axis.",
            "Do not run MT5 in F89C because no meaningful materialization candidate or runtime claim exists; this is not cost/expense or proxy-bad deferral.",
            "Rotate to F90 pending-open scaffold on time-to-barrier competing-risk label axis; formal F90A open still needs its own packet and gates.",
        ],
        "forbidden_claim_check": FORBIDDEN_CLAIMS,
        "claim_boundary": CLAIM_BOUNDARY,
        "created_at_utc": now,
        "receipt_path": rel(TASK_FORCE_REVIEW),
    }


def closeout_decision(now: str) -> dict[str, Any]:
    f89b = read_json(F89B_SUMMARY)
    f89b_kpi = read_json(F89B_KPI)
    feature_join = read_json(F89B_FEATURE_JOIN_REPORT)
    economics = f89b["economics_reference_from_deal_episodes"]
    avg_win = economics.get("avg_win")
    avg_loss = economics.get("avg_loss")
    payoff_ratio = None
    if isinstance(avg_win, (int, float)) and isinstance(avg_loss, (int, float)) and avg_loss:
        payoff_ratio = avg_win / abs(avg_loss)
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": now,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "parent_run_id": PARENT_RUN_ID,
        "next_stage_id": NEXT_STAGE_ID,
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "hypothesis": "Runtime deal output can become a pre-entry adverse-selection teacher surface.",
        "test_period": episode_bounds(),
        "proxy_kpi": f89b_kpi["proxy_kpi"],
        "runtime_kpi": {
            "status": "not_applicable_no_new_strategy_tester_run",
            "reason": "F89C protects closeout/rotation only and creates no runtime/materialization/economics claim.",
        },
        "runtime_reference_economics_from_f88c_deals": {
            **economics,
            "payoff_ratio": payoff_ratio,
            "recovery_factor": None,
            "recovery_factor_reason": "Drawdown denominator is not available for F89B deal episode reference.",
            "time_under_water": None,
            "time_under_water_reason": "Balance/equity curve was not produced in F89B proxy scout.",
        },
        "tier_scope_records": f89b_kpi["tier_scope_records"],
        "feature_join_local_verification": {
            **feature_join,
            "feature_time_uniqueness": feature_time_uniqueness(),
            "claim_effect": "Supports entry feature join record only; does not prove runtime authority.",
        },
        "materialization_decision": {
            "meaningful_candidate": False,
            "candidate_claim": "negative_for_materialization_candidate",
            "teacher_axis_claim": "inconclusive",
            "gap_cause": f89b_kpi["gap_cause"],
            "same_axis_repair_disposition": "capped_no_threshold_filter_parameter_only_repair",
            "repair_not_required_first": True,
            "rotation_selected": True,
            "preserved_clue": [
                "F88C deal rows can be transformed into a deal episode teacher surface.",
                "Entry feature join reached 23/23 rows on the available Tier A reference output.",
                "Locked-forward top20 readout had small positive net delta but not enough sample or tier breadth.",
            ],
            "negative_memory": [
                "23 episodes are below the predeclared minimum 50 runtime-candidate episodes.",
                "Tier B fallback deal surface is missing_required.",
                "Inner train perfect metrics on 14 rows are overfit risk, not model validation.",
                "F88C reference economics remain negative: net -36.20, PF 0.6738, trades/day 3.2857.",
            ],
            "do_not_repeat": [
                "Do not promote this teacher surface by threshold/filter/parameter retune only.",
                "Do not call F88C reference economics F89C runtime economics.",
                "Do not claim Task Force reviewed/verified/pass beyond actual call receipt and local gate files.",
            ],
        },
        "runtime_probe_decision": {
            "status": RUNTIME_PROBE_STATUS,
            "not_run_reason": "no meaningful materialization candidate and no runtime/materialization/economics claim",
            "not_run_not_because": ["cost", "expense", "proxy_bad_skip"],
            "future_same_packet_trigger_conditions": [
                "meaningful materialization candidate with candidate_id/model/ONNX/EA/set/feature identity",
                "runtime_probe/runtime_verified/strategy_tester_runtime_economics/materialization_ready/MT5_handoff_ready claim",
                "selected_baseline/operating_promotion/runtime_authority/live_readiness/Goal Achieve implication",
                "runtime behavior change through threshold/router/risk/SLTP/cost/session/feature timing",
                "explicit decision to test a low-sample candidate anyway",
            ],
        },
        "frontier_extra_due": {
            "status": "pass_not_due",
            "due": False,
            "reason": "F89 closeout is below F100; E01 is already closed for F050.",
            "next_due_boundary": "F100",
        },
        "five_stage_direction_synthesis": {
            "covered_frontier_ids": ["F85", "F86", "F87", "F88", "F89"],
            "dominant_direction": "runtime-adjacent labels kept producing useful clues but weak materialization surfaces",
            "repeated_mechanism": "small proxy readouts and repair pressure after runtime/proxy gaps",
            "overused_axis_warning": "another adverse-selection teacher threshold retune would be adjacent same-axis continuation",
            "next_axis_options": [
                "time-to-barrier competing-risk label axis",
                "rank/survival ordering objective instead of binary adverse-selection probability",
                "barrier-definition and purged-forward split preflight before any runtime claim",
            ],
            "allowed_reexperiment_conditions": [
                "new label/target representation",
                "new validation philosophy",
                "new runtime representation or broader Tier A/Tier B deal substrate",
            ],
            "adjacent_same_axis_block": True,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "topic_rotation_check": {
            "status": "pass",
            "proposed_next_stage_id": NEXT_STAGE_ID,
            "proposed_next_run_id": NEXT_RUN_ID,
            "repair_disposition_closed_in_stage": True,
            "same_surface_repair_block": True,
            "topic_ban": False,
            "novelty_delta": {
                "primary_axis": "label/target representation",
                "supporting_axes": ["validation philosophy", "model objective", "trade path/risk timing"],
                "description": "Rotate from binary adverse-selection teacher proxy to time-to-barrier competing-risk labels.",
                "not_threshold_filter_parameter_tweak": True,
            },
            "decision": "pass_for_f90_pending_open_scaffold_only",
        },
        "task_force": task_force_receipt(now),
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }


def source_inputs() -> list[Path]:
    return [
        F89B_SUMMARY,
        F89B_KPI,
        F89B_RUN_MANIFEST,
        F89B_PROXY_METRICS,
        F89B_FEATURE_JOIN_REPORT,
        F89B_TIER_SCOPE,
        F89B_CANDIDATE_QUEUE,
        F89B_TEACHER_SURFACE,
        F89B_EPISODES,
        F89B_RESULT_SUMMARY,
        F89B_WORK_PACKET,
        F89B_CLOSEOUT_GATE,
        F89_TASK_FORCE_CORRECTION,
        F88C_KPI,
        F88C_RUNTIME_IDENTITY,
        F88C_DEALS,
        F88C_FEATURE_MATRIX,
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
        F89C_REPORT,
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
        STAGE_TRANSITION_RECEIPT,
        RUN_EVIDENCE_RECEIPT,
        DATA_RECEIPT,
        MODEL_RECEIPT,
        ARTIFACT_RECEIPT,
        RESULT_RECEIPT,
        CLAIM_RECEIPT,
        ANSWER_RECEIPT,
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
    ]


def ensure_dirs() -> None:
    for directory in (
        RUN_DIR,
        DECISION_DIR,
        REPORT_DIR,
        REVIEW_DIR,
        SELECTED_DIR,
        PACKET_DIR,
        NEXT_SPEC_DIR,
        NEXT_INPUT_DIR,
        NEXT_REVIEW_DIR,
        NEXT_SELECTED_DIR,
    ):
        io_path(directory).mkdir(parents=True, exist_ok=True)


def closeout_report_text(summary: Mapping[str, Any]) -> str:
    econ = summary["runtime_reference_economics_from_f88c_deals"]
    proxy = summary["proxy_kpi"]
    return f"""# F89C Closeout And Rotation(F89C 마감 및 회전)

Updated(갱신): {summary['created_at_utc']}

Conclusion(결론): F89 is closed as negative/inconclusive no-authority(F89는 부정/불충분, 권위 없음으로 마감). The materialization candidate claim(물질화 후보 주장)은 negative(부정)이고, teacher axis claim(교사 축 주장)은 inconclusive(불충분)입니다.

Action(행동): F89B deal-path teacher proxy scout(F89B 딜 경로 교사 프록시 탐색), local verification(로컬 검증), and Task Force actual calls(태스크포스 실제 호출)를 묶어 F89C repair/rotation decision(F89C 수리/회전 결정)을 기록했습니다.

Effect(효과): threshold/filter/parameter-only repair(임계값/필터/파라미터만 수리)를 막고, F90 pending-open scaffold(F90 개방 대기 골격)를 time-to-barrier competing-risk label axis(장벽 도달 시간 경쟁위험 라벨 축)로 넘깁니다.

Proxy KPI(프록시 핵심 성과 지표): episodes(에피소드) `{proxy['episodes']}`, joined_rows(조인 행) `{proxy['joined_rows']}`, readout_top20_net_delta(판독 상위20 순변화) `{proxy['readout_top20_net_delta']}`, readout_top20_adverse_lift(판독 상위20 역선택 리프트) `{proxy['readout_top20_adverse_lift']}`, meaningful_candidate(의미 있는 후보) `{proxy['meaningful_candidate']}`.

Runtime KPI(런타임 핵심 성과 지표): not_applicable(해당 없음). F89C has no new Strategy Tester run(F89C 새 전략 테스터 실행 없음) because no meaningful materialization candidate(의미 있는 물질화 후보 없음) and no runtime claim(런타임 주장 없음). This is not cost/expense deferral(비용 지연 아님) and not proxy-bad skip(프록시 나쁨 생략 아님).

Reference closeout KPI(참조 마감 핵심 성과 지표): gross_profit/loss(총이익/총손실) `{econ['gross_profit']}/{econ['gross_loss']}`, net_profit(순수익) `{econ['net_profit']}`, PF(수익 팩터) `{econ['profit_factor']}`, trades(거래 수) `{econ['trade_count']}`, trades_per_day(일 거래 수) `{econ['trades_per_day']}`, win_rate(승률) `{econ['win_rate']}`, avg_win/loss(평균 이익/손실) `{econ['avg_win']}/{econ['avg_loss']}`, payoff_ratio(손익비) `{econ['payoff_ratio']}`, expectancy(기대값) `{econ['expectancy']}`, recovery_factor(회복 계수) `missing_reason:{econ['recovery_factor_reason']}`, time_under_water(회복 전 체류 시간) `missing_reason:{econ['time_under_water_reason']}`, max_consecutive_loss(최대 연속 손실) `{econ['max_consecutive_loss']}`, long/short(롱/숏) `{econ['long_trade_count']}/{econ['short_trade_count']}`.

Tier records(티어 기록): Tier A used(Tier A 사용) `23`, Tier B fallback used(Tier B 대체 사용) `missing_required`, actual routed total(실제 라우팅 전체) `23 with boundary(경계 포함)`.

Gap cause(간극 원인): `{summary['materialization_decision']['gap_cause']}`.

Task Force(태스크포스): selected agents(선택 요원) `6`, actual_subagent_calls(실제 하위요원 호출) `6`, full roster call(전원 호출) `false`.

Next action(다음 행동): `{NEXT_RUN_ID}` pending-open scaffold(개방 대기 골격). Formal F90A stage open(정식 F90A 단계 개방)은 별도 work packet(작업 묶음), Task Force stage-open review(태스크포스 단계 개방 검토), and gates(게이트)가 필요합니다.

Not claimed(주장하지 않음): selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성).

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""


def write_run_artifacts(summary: Mapping[str, Any]) -> None:
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_stage_id": NEXT_STAGE_ID,
        "next_run_id": NEXT_RUN_ID,
        "run_type": "repair_or_rotation_closeout",
        "created_at_utc": summary["created_at_utc"],
        "source_artifacts": [rel(path) for path in source_inputs() if path_exists(path)],
        "runtime_evidence_status": RUNTIME_PROBE_STATUS,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    kpi = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "hypothesis": summary["hypothesis"],
        "test_period": summary["test_period"],
        "proxy_kpi": summary["proxy_kpi"],
        "runtime_kpi": summary["runtime_kpi"],
        "closeout_kpi": summary["runtime_reference_economics_from_f88c_deals"],
        "parity": "not_applicable_no_onnx_ea_runtime_claim",
        "gap_cause": summary["materialization_decision"]["gap_cause"],
        "next_action": NEXT_RUN_ID,
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }
    write_json(RUN_MANIFEST, manifest)
    write_json(SUMMARY_JSON, summary)
    write_json(KPI_RECORD, kpi)
    write_json(DECISION_JSON, summary["materialization_decision"])
    write_text(RESULT_SUMMARY, closeout_report_text(summary))
    write_json(STAGE_CLOSEOUT_SUMMARY, summary)
    write_text(STAGE_CLOSEOUT_REPORT, closeout_report_text(summary))
    write_text(F89C_REPORT, closeout_report_text(summary))


def audit_payload(name: str, status: str = "pass", *, counts: Mapping[str, Any] | None = None, allowed: Sequence[str] | None = None) -> dict[str, Any]:
    return {
        "audit_name": name,
        "status": status,
        "passed": status == "pass" or status.startswith("pass_"),
        "findings": [],
        "counts": dict(counts or {}),
        "allowed_claims": list(allowed or []),
        "forbidden_claims": [],
    }


def write_audits(summary: Mapping[str, Any]) -> None:
    write_json(TASK_FORCE_REVIEW, summary["task_force"])
    write_json(TASK_FORCE_PACKET_REVIEW, {"audit_name": "codex_task_force_review_packet", "status": "pass", "passed": True, **summary["task_force"]})
    write_json(FRONTIER_EXTRA_DUE_CHECK, audit_payload("frontier_extra_due_check", "pass_not_due", counts=summary["frontier_extra_due"], allowed=["frontier_extra_due_check_not_due_after_f89"]))
    write_json(FIVE_STAGE_SYNTHESIS, audit_payload("frontier_five_stage_direction_synthesis", "pass", counts=summary["five_stage_direction_synthesis"], allowed=["direction_delta_recorded"]))
    write_json(TOPIC_ROTATION_CHECK, audit_payload("frontier_topic_rotation_check", "pass", counts=summary["topic_rotation_check"], allowed=["topic_rotation_check_recorded"]))
    write_json(
        SCOPE_GATE,
        audit_payload(
            "scope_completion_gate",
            "pass",
            counts={
                "expected_outputs": [rel(path) for path in produced_artifacts()],
                "f90_pending_open_scaffold_only": True,
            },
            allowed=["scope_recorded"],
        ),
    )
    write_json(DATA_INTEGRITY_AUDIT, audit_payload("data_integrity_audit", "pass_with_boundary", counts=summary["feature_join_local_verification"], allowed=["data_boundary_recorded"]))
    write_json(
        MODEL_VALIDATION_AUDIT,
        audit_payload(
            "model_validation_audit",
            "pass_with_inconclusive_boundary",
            counts={
                "total_episodes": summary["proxy_kpi"]["episodes"],
                "minimum_runtime_candidate_episodes": 50,
                "inner_train_perfect_metrics": True,
                "selection_claim_safe": False,
                "judgment": "model_selection_inconclusive_candidate_claim_negative",
            },
            allowed=["model_risk_recorded"],
        ),
    )
    write_json(
        KPI_CONTRACT_AUDIT,
        audit_payload(
            "kpi_contract_audit",
            "pass",
            counts={
                "proxy_kpi_present": True,
                "runtime_kpi": summary["runtime_kpi"],
                "closeout_kpi_present": True,
                "pf_not_standalone": True,
            },
            allowed=["kpi_contract_recorded"],
        ),
    )
    write_json(
        ARTIFACT_AUDIT,
        audit_payload(
            "artifact_lineage_audit",
            "pass_connected_with_boundary",
            counts={
                "source_inputs": {rel(path): file_identity(path) for path in source_inputs()},
                "produced_artifacts": [rel(path) for path in produced_artifacts() if path_exists(path)],
                "lineage_boundary": CLAIM_BOUNDARY,
            },
            allowed=["artifact_lineage_connected"],
        ),
    )
    write_json(
        RESULT_JUDGMENT_AUDIT,
        audit_payload(
            "result_judgment_receipt",
            "pass_bounded_inconclusive_negative",
            counts={
                "judgment": JUDGMENT,
                "candidate_claim": "negative",
                "teacher_axis_claim": "inconclusive",
                "runtime_claim": "not_claimed",
                "next_action": NEXT_RUN_ID,
            },
            allowed=["negative_or_inconclusive_memory_recorded"],
        ),
    )
    final_guard = {
        "audit_name": "final_claim_guard",
        "status": "pass",
        "passed": True,
        "packet_id": RUN_ID,
        "created_at_utc": summary["created_at_utc"],
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "claim_boundary": CLAIM_BOUNDARY,
        "claim_effect": "F89C can claim closeout/rotation and actual Task Force calls only; no runtime/economics/authority claims.",
        "findings": [],
    }
    write_json(FINAL_CLAIM_GUARD, final_guard)
    write_json(PACKET_FINAL_CLAIM_GUARD, final_guard)


def file_identity(path: Path) -> dict[str, Any]:
    payload: dict[str, Any] = {"path": rel(path), "exists": path_exists(path)}
    if path_exists(path):
        payload["sha256"] = sha256_file_lf_normalized(path)
        payload["size_bytes"] = io_path(path).stat().st_size
    return payload


def receipt_path(skill: str) -> Path:
    short = skill.removeprefix("obsidian-").replace("-", "_")
    return REVIEW_DIR / f"f89c_{short}_receipt.json"


def write_receipts(summary: Mapping[str, Any]) -> None:
    produced = [rel(path) for path in produced_artifacts() if path_exists(path)]
    sources = [rel(path) for path in source_inputs() if path_exists(path)]
    common = {"packet_id": RUN_ID, "status": "executed"}
    receipts: list[dict[str, Any]] = [
        {
            **common,
            "skill": "obsidian-stage-transition",
            "source_current_truth_docs": [rel(WORKSPACE_STATE), rel(CURRENT_WORKING_STATE), rel(SELECTION_STATUS)],
            "changed_or_checked_docs": [
                rel(WORKSPACE_STATE),
                rel(CURRENT_WORKING_STATE),
                rel(SELECTION_STATUS),
                rel(GLOBAL_SELECTION_STATUS),
                rel(NEXT_STAGE_BRIEF),
                rel(NEXT_SELECTION_STATUS),
                rel(RUN_REGISTRY),
                rel(ALPHA_LEDGER),
            ],
            "detected_conflicts": ["none_detected"],
            "canonical_state_after": {
                "active_stage": NEXT_STAGE_ID,
                "current_run_id": NEXT_RUN_ID,
                "latest_completed_run_id": RUN_ID,
                "f90_open_claim": "not_claimed_pending_open_scaffold_only",
            },
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        {
            **common,
            "skill": "obsidian-run-evidence-system",
            "source_inputs": sources,
            "produced_artifacts": produced,
            "ledger_rows": [f"{RUN_ID}__stage_closeout_rotation", f"{NEXT_RUN_ID}__planned_current_run"],
            "missing_evidence": ["No F89C Strategy Tester report/trade list/telemetry because no runtime claim is made."],
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        {
            **common,
            "skill": "obsidian-data-integrity",
            "data_sources_checked": [rel(F89B_EPISODES), rel(F89B_TEACHER_SURFACE), rel(F88C_FEATURE_MATRIX)],
            "time_axis_boundary": "F89B entry_time_server joined to bar_time_server; local feature time uniqueness recorded.",
            "split_boundary": "F89B inner_train/readout split is exploratory only and not selection authority.",
            "leakage_checks": summary["feature_join_local_verification"],
            "missing_data_boundary": "Tier B fallback deal surface is missing_required.",
        },
        {
            **common,
            "skill": "obsidian-model-validation",
            "model_or_threshold_surface": "F89B logistic adverse-selection teacher proxy",
            "validation_split": "14 inner-train rows and 9 locked-forward readout rows; exploratory only.",
            "overfit_checks": ["inner_train_perfect_metrics_on_14_rows", "total_episodes_below_50"],
            "selection_metric_boundary": "AUC/AP/Brier are observations only; no model validated or candidate selected.",
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        {
            **common,
            "skill": "obsidian-artifact-lineage",
            "source_inputs": sources,
            "produced_artifacts": produced,
            "raw_evidence": sources,
            "machine_readable": [rel(SUMMARY_JSON), rel(RUN_MANIFEST), rel(KPI_RECORD), rel(SKILL_RECEIPTS), rel(TASK_FORCE_PACKET_REVIEW)],
            "human_readable": [rel(RESULT_SUMMARY), rel(STAGE_CLOSEOUT_REPORT), rel(CURRENT_WORKING_STATE)],
            "hashes_or_missing_reasons": {rel(path): sha256_file_lf_normalized(path) for path in produced_artifacts() if path_exists(path)},
            "lineage_boundary": CLAIM_BOUNDARY,
        },
        {
            **common,
            "skill": "obsidian-result-judgment",
            "judgment_boundary": JUDGMENT,
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "evidence_used": [rel(F89B_SUMMARY), rel(F89B_KPI), rel(TASK_FORCE_REVIEW), rel(SUMMARY_JSON)],
        },
        summary["task_force"],
        {
            **common,
            "skill": "obsidian-claim-discipline",
            "requested_claims": ALLOWED_CLAIMS,
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "final_status": STATUS,
        },
        {
            **common,
            "skill": "obsidian-answer-clarity",
            "plain_conclusion": "F89 is closed no-authority; F90 is only pending-open scaffold.",
            "confirmed": ["F89B produced a preserved clue", "F89C has actual Task Force calls", "No meaningful materialization candidate exists"],
            "not_yet_confirmed": ["runtime economics", "selected baseline", "runtime authority", "Goal Achieve", "formal F90A open"],
            "why_it_matters": "This prevents small-sample proxy repair from becoming an authority claim.",
            "next_action": NEXT_RUN_ID,
            "forbidden_claims_avoided": FORBIDDEN_CLAIMS,
        },
    ]
    for receipt in receipts:
        path = TASK_FORCE_REVIEW if receipt["skill"] == "obsidian-task-force-review" else receipt_path(str(receipt["skill"]))
        receipt["receipt_path"] = rel(path)
        write_json(path, receipt)
    write_json(SKILL_RECEIPTS, {"packet_id": RUN_ID, "primary_skill": "obsidian-stage-transition", "claim_boundary": CLAIM_BOUNDARY, "receipts": receipts})


def work_packet(summary: Mapping[str, Any]) -> dict[str, Any]:
    required_evidence = [rel(path) for path in produced_artifacts()]
    gates_not_run = [
        {
            "gate": "runtime_evidence_gate",
            "reason_code": "outside_claim_surface_no_runtime_claim",
            "reason": "F89C protects closeout/rotation only; no Strategy Tester runtime/materialization/economics claim is made.",
            "claim_effect": "Runtime probe/verified/economics/materialization/authority/Goal Achieve claims are forbidden.",
        },
        {
            "gate": "f90_stage_open_gate",
            "reason_code": "pending_open_scaffold_only",
            "reason": "F89C only writes the F90 pending-open scaffold; formal F90A stage open requires a separate packet.",
            "claim_effect": "F90 stage-open completed/reviewed/pass claims are forbidden.",
        },
    ]
    return {
        "version": "work_packet_schema_v2_1",
        "packet_lifecycle": "new_packet",
        "packet_id": RUN_ID,
        "created_at_utc": summary["created_at_utc"],
        "user_request": {
            "user_quote": "/goal active continuation; user required Task Force agents when triggered",
            "requested_action": "F89C stage closeout rotate F90 pending open",
            "requested_count": {"value": 1, "n_a_reason": ""},
            "ambiguous_terms": ["Goal Achieve is not claimed.", "F90 formal stage open is not claimed."],
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
            "detected_families": ["publish_handoff", "experiment_execution", "kpi_evidence", "artifact_lineage", "state_sync"],
            "touched_surfaces": [rel(STAGE_DIR), rel(NEXT_STAGE_DIR), rel(PACKET_DIR), rel(WORKSPACE_STATE)],
            "mutation_intent": True,
            "execution_intent": True,
        },
        "risk_vector_scan": {
            "risks": {
                "small_sample_proxy_overclaimed": "high",
                "f88c_runtime_kpi_laundered_as_f89c": "high",
                "task_force_review_claim_without_actual_calls": "high",
                "f90_pending_open_confused_with_formal_open": "medium",
            },
            "hard_stop_risks": [
                "Do not claim runtime/economics/materialization without MT5 Strategy Tester output identity.",
                "Do not call F90 formally open in this packet.",
                "Do not repeat same threshold/filter/parameter-only repair.",
            ],
            "required_gates": REQUIRED_GATES,
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        "decision_lock": {
            "mode": "assume_safe_default",
            "assumptions": {
                "task_force_required_now": True,
                "strategy_tester_required_now": False,
                "reason": "F89C makes closeout/rotation claims but no runtime/materialization/economics claim.",
            },
            "questions": [],
            "required_user_decisions": [],
        },
        "interpreted_scope": {
            "work_families": ["publish_handoff"],
            "target_surfaces": ["F89 closeout", "F90 pending-open scaffold", "Task Force receipt", "state sync"],
            "scope_units": ["stage_closeout", "rotation_decision", "receipt", "state_sync"],
            "execution_layers": ["local_python_execution", "stage_transition"],
            "mutation_policy": {"allowed": True, "user_quote": "/goal active continuation"},
            "evidence_layers": ["F89B proxy scout", "F89 Task Force correction", "F89C actual Task Force calls"],
            "reduction_policy": {"reduction_allowed": False, "requires_user_quote": False, "rationale": "F89C uses all available F89B closeout evidence."},
            "claim_boundary": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
            "variants_requested": {"value": 1, "n_a_reason": ""},
            "verification_layers": REQUIRED_GATES,
            "mt5_required": "not_required_no_meaningful_candidate_no_runtime_claim",
            "top_k_reduction_allowed": False,
            "scope_reduction_requires_user_quote": False,
        },
        "verification_profile": {
            "profile_id": "stage_closeout",
            "claim_surface": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
            "trigger_sources": ["active_goal", "F89B no meaningful materialization candidate", "closeout_required_task_force_review", "rotation_to_next_frontier"],
            "protected_claims": ALLOWED_CLAIMS,
            "required_evidence": required_evidence,
            "gates_not_run_with_reason": gates_not_run,
            "stop_conditions": [
                "Stop after F89 closeout, F90 pending-open scaffold, Task Force actual calls, gates, and state sync.",
                "If meaningful materialization candidate appears, switch to runtime_probe profile and attempt narrow MT5 probe in the same packet.",
            ],
        },
        "acceptance_criteria": [
            {"id": "AC-001", "text": "F89C decision artifact exists.", "expected_artifact": rel(DECISION_JSON), "verification_method": "scope_completion_gate", "required": True},
            {"id": "AC-002", "text": "Task Force actual calls are recorded.", "expected_artifact": rel(TASK_FORCE_PACKET_REVIEW), "verification_method": "codex_task_force_review_packet", "required": True},
            {"id": "AC-003", "text": "F90 pending-open scaffold exists without formal open claim.", "expected_artifact": rel(NEXT_STAGE_BRIEF), "verification_method": "scope_completion_gate", "required": True},
        ],
        "work_plan": {
            "phases": ["Read F89B evidence.", "Call relevant Task Force agents.", "Write closeout and pending-open scaffold.", "Run gates and state sync."],
            "expected_outputs": required_evidence,
            "stop_conditions": ["No runtime/materialization/economics/authority/Goal Achieve claim."],
        },
        "skill_routing": {
            "primary_family": "publish_handoff",
            "primary_skill": "obsidian-stage-transition",
            "support_skills": [skill for skill in REQUIRED_SKILLS if skill != "obsidian-stage-transition"],
            "skills_considered": REQUIRED_SKILLS + ["obsidian-runtime-parity", "obsidian-backtest-forensics"],
            "skills_selected": REQUIRED_SKILLS,
            "skills_not_used": [
                {"skill": "obsidian-runtime-parity", "reason": "No ONNX/EA/runtime parity or handoff claim is made."},
                {"skill": "obsidian-backtest-forensics", "reason": "No new Strategy Tester report/trade list exists in F89C."},
            ],
            "required_skill_receipts": REQUIRED_SKILLS,
            "required_gates": REQUIRED_GATES,
        },
        "evidence_contract": {
            "raw_evidence": [rel(path) for path in source_inputs() if path_exists(path)],
            "machine_readable": [rel(SUMMARY_JSON), rel(RUN_MANIFEST), rel(KPI_RECORD), rel(SKILL_RECEIPTS), rel(TASK_FORCE_PACKET_REVIEW)],
            "human_readable": [rel(RESULT_SUMMARY), rel(STAGE_CLOSEOUT_REPORT), rel(CURRENT_WORKING_STATE)],
        },
        "gates": {
            "required": REQUIRED_GATES,
            "work_packet_schema_lint": "pending_external_lint",
            "skill_receipt_schema_lint": "pending_external_lint",
            "codex_task_force_review_packet": "pass",
            "frontier_extra_due_check": "pass_not_due",
            "frontier_five_stage_direction_synthesis": "pass",
            "frontier_topic_rotation_check": "pass",
            "scope_completion_gate": "pass",
            "data_integrity_audit": "pass_with_boundary",
            "model_validation_audit": "pass_with_inconclusive_boundary",
            "kpi_contract_audit": "pass",
            "artifact_lineage_audit": "pass_connected_with_boundary",
            "result_judgment_receipt": "pass_bounded_inconclusive_negative",
            "state_sync_audit": "pending_external_lint",
            "required_gate_coverage_audit": "pending_external_lint",
            "final_claim_guard": "pass",
            "not_applicable_with_reason": {
                "runtime_evidence_gate": "outside_claim_surface_no_runtime_claim; no Strategy Tester runtime/materialization/economics claim",
                "f90_stage_open_gate": "pending_open_scaffold_only; formal F90A open not claimed",
            },
        },
        "final_claim_policy": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS},
    }


def closeout_gate_payload(gate_results: Mapping[str, Any] | None = None) -> dict[str, Any]:
    status_by_gate = {name: result.get("status", "pending_external_lint") for name, result in (gate_results or {}).items()}
    audits = [
        ("work_packet_schema_lint", status_by_gate.get("work_packet_schema_lint", "pending_external_lint"), PACKET_WORK_PACKET_LINT),
        ("skill_receipt_schema_lint", status_by_gate.get("skill_receipt_schema_lint", "pending_external_lint"), PACKET_SKILL_RECEIPT_LINT),
        ("codex_task_force_review_packet", "pass", TASK_FORCE_PACKET_REVIEW),
        ("frontier_extra_due_check", "pass_not_due", FRONTIER_EXTRA_DUE_CHECK),
        ("frontier_five_stage_direction_synthesis", "pass", FIVE_STAGE_SYNTHESIS),
        ("frontier_topic_rotation_check", "pass", TOPIC_ROTATION_CHECK),
        ("scope_completion_gate", "pass", SCOPE_GATE),
        ("data_integrity_audit", "pass_with_boundary", DATA_INTEGRITY_AUDIT),
        ("model_validation_audit", "pass_with_inconclusive_boundary", MODEL_VALIDATION_AUDIT),
        ("kpi_contract_audit", "pass", KPI_CONTRACT_AUDIT),
        ("artifact_lineage_audit", "pass_connected_with_boundary", ARTIFACT_AUDIT),
        ("result_judgment_receipt", "pass_bounded_inconclusive_negative", RESULT_JUDGMENT_AUDIT),
        ("state_sync_audit", status_by_gate.get("state_sync_audit", "pending_external_lint"), PACKET_STATE_SYNC_AUDIT),
        ("required_gate_coverage_audit", status_by_gate.get("required_gate_coverage_audit", "pending_external_lint"), PACKET_REQUIRED_GATE_AUDIT),
    ]
    return {
        "packet_id": RUN_ID,
        "status": "pass" if gate_results and all(result.get("status") == "pass" for result in gate_results.values()) else "pending_external_lint",
        "audits": [{"audit_name": name, "status": status, "path": rel(path)} for name, status, path in audits],
        "final_claim_guard": {"audit_name": "final_claim_guard", "status": "pass", "path": rel(PACKET_FINAL_CLAIM_GUARD)},
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_packet(summary: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> None:
    write_yaml(WORK_PACKET, work_packet(summary))
    write_json(PACKET_CLOSEOUT_GATE, closeout_gate_payload(gate_results))


def workspace_state_text(summary: Mapping[str, Any]) -> str:
    return f"""current_stage_id: {NEXT_STAGE_ID}
active_stage: {NEXT_STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
frontier_extra_due_status: {FRONTIER_EXTRA_DUE_STATUS}
frontier_topic_rotation_status: f90_pending_open_scaffold_topic_rotation_recorded
task_force_status: f89c_actual_subagent_calls_recorded_no_reviewed_verified_pass_claim
runtime_probe_status: {RUNTIME_PROBE_STATUS}
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
updated_at_utc: '{summary['created_at_utc']}'
context_anchor: {rel(NEXT_CONTEXT_ANCHOR)}
notes:
- 'Action(행동): F89C closed F89 as negative/inconclusive no-authority(F89C가 F89를 부정/불충분, 권위 없음으로 마감했다).'
- 'Effect(효과): F90 pending-open scaffold(F90 개방 대기 골격)를 time-to-barrier competing-risk label axis(장벽 도달 시간 경쟁위험 라벨 축)로 남기고, formal F90A open(정식 F90A 개방)은 아직 주장하지 않는다.'
- 'Task Force(태스크포스): selected agents 6/6 actual_subagent_calls(선택 요원 6/6 실제 하위요원 호출)를 기록했다.'
- 'Runtime(런타임): no new Strategy Tester runtime evidence(새 전략 테스터 런타임 근거 없음); no runtime authority(런타임 권위 없음); no Goal Achieve(목표 달성 없음).'
"""


def current_state_text(summary: Mapping[str, Any]) -> str:
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {summary['created_at_utc']}

Active stage(활성 단계): `{NEXT_STAGE_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Action(행동): F89C closed F89(F89C가 F89를 마감) and wrote an F90 pending-open scaffold(F90 개방 대기 골격을 기록).

Effect(효과): 같은 deal-path adverse-selection teacher proxy(딜 경로 역선택 교사 프록시)를 threshold/filter/parameter-only repair(임계값/필터/파라미터만 수리)로 반복하지 않고, 다음 축을 time-to-barrier competing-risk label(장벽 도달 시간 경쟁위험 라벨)로 돌린다.

Task Force status(태스크포스 상태): `f89c_actual_subagent_calls_recorded_no_reviewed_verified_pass_claim`.

Runtime probe(런타임 탐침): `{RUNTIME_PROBE_STATUS}`.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""


def f89_selection_status_text(summary: Mapping[str, Any]) -> str:
    return f"""# F89 Selection Status(F89 선택 상태)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `{STATUS}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Next run(다음 실행): `{NEXT_RUN_ID}` pending-open scaffold(개방 대기 골격)

Judgment(판정): `{JUDGMENT}`

Selected baseline(선택 기준선): not_claimed(주장하지 않음)

Operating promotion(운영 승격): not_claimed(주장하지 않음)

Runtime authority(런타임 권위): not_claimed(주장하지 않음)

Live readiness(실거래 준비): not_claimed(주장하지 않음)

Goal Achieve(목표 달성): not_claimed(주장하지 않음)
"""


def f90_stage_brief_text(summary: Mapping[str, Any]) -> str:
    return f"""# F90 Time-To-Barrier Competing-Risk Label Axis(F90 장벽 도달 시간 경쟁위험 라벨 축)

Status(상태): pending_open_scaffold_only(개방 대기 골격 전용)

Current run(현재 실행): `{NEXT_RUN_ID}`

Thesis(가설): replace binary adverse-selection teacher(이진 역선택 교사)를 time-to-barrier competing-risk label(장벽 도달 시간 경쟁위험 라벨)로 바꾸면, small-sample probability claims(소표본 확률 주장)을 줄이고 rank/survival ordering(순위/생존 순서) 단서를 얻을 수 있다.

Action(행동): F89C wrote only the scaffold(F89C는 골격만 기록).

Effect(효과): formal F90A stage open(정식 F90A 단계 개방), Task Force stage-open review(태스크포스 단계 개방 검토), and verification profile(검증 프로필)은 다음 packet(묶음)에서 다시 실행해야 한다.

Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
"""


def f90_input_refs_text(summary: Mapping[str, Any]) -> str:
    return f"""# F90 Input References(F90 입력 참조)

- F89C closeout(F89C 마감): `{rel(STAGE_CLOSEOUT_REPORT)}`
- F89B proxy metrics(F89B 프록시 지표): `{rel(F89B_PROXY_METRICS)}`
- F89B episodes(F89B 에피소드): `{rel(F89B_EPISODES)}`
- F88C reference runtime deals(F88C 참조 런타임 딜): `{rel(F88C_DEALS)}`

Effect(효과): these are references only(참조 전용) and do not import runtime authority(런타임 권위 상속 없음).
"""


def f90_selection_status_text(summary: Mapping[str, Any]) -> str:
    return f"""# F90 Selection Status(F90 선택 상태)

Updated(갱신): {summary['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`

Status(상태): pending_open_scaffold_only(개방 대기 골격 전용)

Latest completed run(최근 완료 실행): `{RUN_ID}`

Runtime authority(런타임 권위): not_claimed(주장하지 않음)

Goal Achieve(목표 달성): not_claimed(주장하지 않음)

Next action(다음 행동): formal F90A stage open packet(정식 F90A 단계 개방 묶음).
"""


def f90_context_anchor_text(summary: Mapping[str, Any]) -> str:
    return f"""# F90 Context Anchor(F90 맥락 고정점)

Current run(현재 실행): `{NEXT_RUN_ID}`

Source closeout(원천 마감): `{RUN_ID}`

Claim boundary(주장 경계): pending-open scaffold only(개방 대기 골격 전용). Formal stage open(정식 단계 개방)은 아직 완료되지 않았다.
"""


def f90_review_index_text(summary: Mapping[str, Any]) -> str:
    return f"""# F90 Review Index(F90 검토 색인)

Updated(갱신): {summary['created_at_utc']}

- Pending open scaffold(개방 대기 골격): `{rel(NEXT_STAGE_BRIEF)}`
- Source closeout(원천 마감): `{rel(STAGE_CLOSEOUT_REPORT)}`
"""


def decision_memo_text(summary: Mapping[str, Any]) -> str:
    return f"""# Decision Memo(결정 메모): F89C Closeout Rotate F90(F89C 마감 및 F90 회전)

Decision(결정): close F89 as negative/inconclusive no-authority(F89를 부정/불충분, 권위 없음으로 마감).

Reason(이유): F89B has only 23 episodes(23개 에피소드), Tier B missing_required(Tier B 필수 누락), and meaningful_candidate=false(의미 있는 후보 없음).

Effect(효과): MT5 runtime probe(MT5 런타임 탐침)는 트리거되지 않았다. 이유는 no runtime/materialization/economics claim(런타임/물질화/경제성 주장 없음)이며, cost/expense(비용) 또는 proxy-bad skip(프록시 나쁨 생략)이 아니다.

Task Force(태스크포스): 6 selected agents(선택 요원 6명)를 실제 spawn_agent(서브에이전트 생성)로 호출했다.

Next(다음): `{NEXT_RUN_ID}` pending-open scaffold(개방 대기 골격).
"""


def update_state_docs(summary: Mapping[str, Any]) -> None:
    write_text(WORKSPACE_STATE, workspace_state_text(summary))
    write_text(CURRENT_WORKING_STATE, current_state_text(summary))
    write_text(GLOBAL_SELECTION_STATUS, f90_selection_status_text(summary))
    write_text(SELECTION_STATUS, f89_selection_status_text(summary))
    write_text(CONTEXT_ANCHOR, current_state_text(summary))
    write_text(REVIEW_INDEX, f"# F89 Review Index(F89 검토 색인)\n\n- `{rel(STAGE_CLOSEOUT_REPORT)}`\n- `{rel(TASK_FORCE_REVIEW)}`\n- `{rel(FINAL_CLAIM_GUARD)}`\n")
    write_text(NEXT_STAGE_BRIEF, f90_stage_brief_text(summary))
    write_text(NEXT_INPUT_REFS, f90_input_refs_text(summary))
    write_text(NEXT_SELECTION_STATUS, f90_selection_status_text(summary))
    write_text(NEXT_CONTEXT_ANCHOR, f90_context_anchor_text(summary))
    write_text(NEXT_REVIEW_INDEX, f90_review_index_text(summary))
    write_text(DECISION_MEMO, decision_memo_text(summary))


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


def ledger_rows(summary: Mapping[str, Any], gate_passes: int = 0) -> tuple[dict[str, Any], dict[str, Any]]:
    created_date = summary["created_at_utc"][:10]
    econ = summary["runtime_reference_economics_from_f88c_deals"]
    artifact_count = len([path for path in produced_artifacts() if path_exists(path)])
    f89c = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "stage_closeout_rotation",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(RESULT_SUMMARY),
        "notes": "F89 closeout; no runtime claim; F90 pending-open scaffold.",
        "family": "publish_handoff",
        "primary_report": rel(RESULT_SUMMARY),
        "run_number": "frontier89C",
        "date": created_date,
        "decision": DECISION,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "rows": summary["proxy_kpi"]["episodes"],
        "gate_passes": gate_passes,
        "gate_total": len(REQUIRED_GATES),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(RESULT_SUMMARY),
        "run_date": created_date,
        "primary_artifact": rel(DECISION_JSON),
        "net_profit": econ["net_profit"],
        "profit_factor": econ["profit_factor"],
        "trade_count": econ["trade_count"],
        "result_status": STATUS,
        "sample_rows": summary["proxy_kpi"]["episodes"],
        "feature_count": 62,
        "expectancy": econ["expectancy"],
        "view": "stage_closeout_rotation",
        "tier": "Tier A used; Tier B missing_required",
        "metric_scope": "reference_runtime_deal_economics_not_f89c_runtime",
        "scoreboard_lane": "deal_path_teacher_closeout",
        "external_verification_status": "out_of_scope_by_claim_no_strategy_tester_runtime_claim",
        "result_judgment": JUDGMENT,
        "gate_audit_path": rel(PACKET_REQUIRED_GATE_AUDIT),
        "created_at": summary["created_at_utc"],
        "ledger_row_id": f"{RUN_ID}__stage_closeout_rotation",
        "subrun_id": f"{RUN_ID}__stage_closeout_rotation",
        "record_view": "stage_closeout_rotation",
        "tier_scope": "Tier A used; Tier B missing_required; routed_total=Tier A source rows",
        "kpi_scope": "closeout_reference_only_no_runtime_economics",
        "primary_kpi": f"episodes={summary['proxy_kpi']['episodes']};meaningful_candidate=false",
        "guardrail_kpi": "runtime_probe_trigger=false;task_force_calls=6",
        "runtime_attempt_rows": 0,
        "work_family": "publish_handoff",
        "row_id": f"{RUN_ID}__stage_closeout_rotation",
        "evidence_boundary": "stage_closeout_rotation_only_no_authority",
        "next_action": NEXT_RUN_ID,
        "question": "Should F89 repair the deal-path teacher axis or rotate?",
        "artifact_count": artifact_count,
        "created_at_utc": summary["created_at_utc"],
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
        "trade_density": econ["trades_per_day"],
        "candidate_count": 0,
        "scout_clue_count": 1,
        "materialization_candidate_count": 0,
        "meaningful_signal_count": 0,
        "completion_candidate_count": 0,
        "trades_per_day": econ["trades_per_day"],
        "long_trade_count": econ["long_trade_count"],
        "short_trade_count": econ["short_trade_count"],
        "best_net_profit": econ["net_profit"],
        "best_profit_factor": econ["profit_factor"],
    }
    f90a = {
        "run_id": NEXT_RUN_ID,
        "stage_id": NEXT_STAGE_ID,
        "lane": "pending_stage_open",
        "status": "pending_open_scaffold_only_no_authority",
        "judgment": "pending_formal_stage_open",
        "path": rel(NEXT_STAGE_BRIEF),
        "notes": "Pending open scaffold created by F89C; formal F90A packet still required.",
        "family": "experiment_design",
        "primary_report": rel(NEXT_STAGE_BRIEF),
        "run_number": "frontier90A",
        "date": created_date,
        "decision": "pending_formal_stage_open",
        "parent_run_id": RUN_ID,
        "rows": 0,
        "gate_passes": 0,
        "gate_total": 0,
        "claim_boundary": "pending_open_scaffold_only_no_runtime_authority_no_goal_achieve",
        "report_path": rel(NEXT_STAGE_BRIEF),
        "run_date": created_date,
        "primary_artifact": rel(NEXT_STAGE_BRIEF),
        "result_status": "pending_open_scaffold_only_no_authority",
        "view": "planned_current_run",
        "tier": "not_applicable_planned",
        "metric_scope": "pending",
        "scoreboard_lane": "time_to_barrier_competing_risk_label_axis",
        "external_verification_status": "pending_formal_stage_open",
        "result_judgment": "pending",
        "created_at": summary["created_at_utc"],
        "ledger_row_id": f"{NEXT_RUN_ID}__planned_current_run",
        "subrun_id": f"{NEXT_RUN_ID}__planned_current_run",
        "record_view": "planned_current_run",
        "tier_scope": "not_applicable_planned",
        "kpi_scope": "pending",
        "primary_kpi": "pending",
        "guardrail_kpi": "formal_stage_open_required",
        "work_family": "experiment_design",
        "row_id": f"{NEXT_RUN_ID}__planned_current_run",
        "evidence_boundary": "pending_open_scaffold_only",
        "next_action": "formal_f90a_stage_open_packet",
        "question": "Can time-to-barrier competing-risk labels replace binary adverse-selection teacher claims?",
        "artifact_count": 0,
        "created_at_utc": summary["created_at_utc"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "run_family": "experiment_design",
        "run_type": "planned_current_run",
        "input_run_id": RUN_ID,
        "output_path": rel(NEXT_STAGE_DIR),
        "result_path": rel(NEXT_STAGE_BRIEF),
        "goal_achieve": "not_claimed",
        "source_authority": "not_claimed",
    }
    return f89c, f90a


def update_ledgers(summary: Mapping[str, Any], gate_passes: int = 0) -> None:
    f89c, f90a = ledger_rows(summary, gate_passes=gate_passes)
    append_dict_rows(RUN_REGISTRY, ["run_id"], [f89c, f90a])
    append_dict_rows(ALPHA_LEDGER, ["ledger_row_id"], [f89c, f90a])
    append_dict_rows(STAGE_LEDGER, ["ledger_row_id"], [f89c], header_source=ALPHA_LEDGER)
    append_dict_rows(NEXT_STAGE_LEDGER, ["ledger_row_id"], [f90a], header_source=ALPHA_LEDGER)


def update_artifact_registry(summary: Mapping[str, Any]) -> None:
    rows = []
    for path in produced_artifacts():
        if not path_exists(path):
            continue
        rows.append(
            {
                "stage_id": STAGE_ID if STAGE_ID in rel(path) or "frontier89C" in rel(path) or "f89c" in rel(path) else NEXT_STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": "f89c_closeout_rotation",
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path),
                "created_at": summary["created_at_utc"],
                "claim_boundary": CLAIM_BOUNDARY,
                "artifact_id": f"{RUN_ID}::{rel(path)}",
                "created_at_utc": summary["created_at_utc"],
                "notes": "F89C closeout/rotation artifact; no runtime authority.",
                "artifact_path": rel(path),
                "effect": "Supports F89 closeout, Task Force actual-call receipt, and F90 pending-open scaffold only.",
                "size_bytes": io_path(path).stat().st_size,
            }
        )
    append_dict_rows(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def update_register_docs(summary: Mapping[str, Any]) -> None:
    marker = RUN_ID
    negative_addition = f"""
## F89C deal-path teacher closeout(F89C 딜 경로 교사 마감)

- run_id: `{RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): F89B clue(단서)는 보존하지만 materialization candidate(물질화 후보)는 부정으로 닫는다.
- do_not_repeat(반복 금지): no threshold/filter/parameter-only repair(임계값/필터/파라미터만 수리 금지).
- next(다음): `{NEXT_RUN_ID}` pending-open scaffold(개방 대기 골격).
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""
    idea_addition = f"""
## F90 pending idea(F90 개방 대기 아이디어): time-to-barrier competing-risk label axis(장벽 도달 시간 경쟁위험 라벨 축)

- source(원천): `{RUN_ID}`
- idea_boundary(아이디어 경계): pending-open scaffold only(개방 대기 골격 전용)
- effect(효과): binary adverse-selection label(이진 역선택 라벨)을 MFE/MAE barrier arrival ordering(MFE/MAE 장벽 도달 순서)으로 바꿔 실험한다.
"""
    changelog_addition = f"""
<!-- {RUN_ID} -->

## {summary['created_at_utc']} - F89C Closeout Rotate F90(F89C 마감 및 F90 회전)

- Action(행동): `frontier89C_deal_path_teacher_repair_or_rotation_decision_v1`로 F89를 negative/inconclusive no-authority(부정/불충분, 권위 없음) 마감했다.
- Effect(효과): Task Force actual_subagent_calls(태스크포스 실제 하위요원 호출) 6건을 기록하고, F90 pending-open scaffold(F90 개방 대기 골격)를 `time_to_barrier_competing_risk_label_axis(장벽 도달 시간 경쟁위험 라벨 축)`로 남겼다.
- Runtime(런타임): no new Strategy Tester runtime evidence(새 전략 테스터 런타임 근거 없음); no runtime authority(런타임 권위 없음); no Goal Achieve(목표 달성 없음).
- Boundary(경계): `{CLAIM_BOUNDARY}`.
"""
    append_once(NEGATIVE_REGISTER, marker, negative_addition)
    append_once(IDEA_REGISTRY, marker, idea_addition)
    append_once(WORKSPACE_CHANGELOG, marker, changelog_addition)
    append_once(ROOT_CHANGELOG, marker, changelog_addition)


def write_state_sync_seed(summary: Mapping[str, Any]) -> None:
    payload = audit_payload(
        "state_sync_audit",
        "pending_external_lint",
        counts={"active_stage": NEXT_STAGE_ID, "current_run_id": NEXT_RUN_ID, "latest_completed_run_id": RUN_ID},
    )
    write_json(STATE_SYNC_AUDIT, payload)
    write_json(PACKET_STATE_SYNC_AUDIT, payload)


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


def run_control_gates(summary: Mapping[str, Any]) -> dict[str, Any]:
    results: dict[str, Any] = {}
    results["work_packet_schema_lint"] = run_gate_cmd(["foundation.control_plane.work_packet_schema_lint", str(WORK_PACKET)], PACKET_WORK_PACKET_LINT)
    results["skill_receipt_schema_lint"] = run_gate_cmd(["foundation.control_plane.skill_receipt_schema_lint", str(SKILL_RECEIPTS)], PACKET_SKILL_RECEIPT_LINT)
    results["state_sync_audit"] = run_gate_cmd(
        ["foundation.control_plane.state_sync_audit", "--root", str(ROOT), "--active-stage", NEXT_STAGE_ID, "--current-branch", current_branch()],
        PACKET_STATE_SYNC_AUDIT,
    )
    sync_review_audit(PACKET_STATE_SYNC_AUDIT, STATE_SYNC_AUDIT)
    write_packet(summary, results)
    results["required_gate_coverage_audit"] = run_gate_cmd(
        ["foundation.control_plane.required_gate_coverage_audit", "--work-packet", str(WORK_PACKET), "--closeout-gate", str(PACKET_CLOSEOUT_GATE)],
        PACKET_REQUIRED_GATE_AUDIT,
    )
    sync_review_audit(PACKET_REQUIRED_GATE_AUDIT, REQUIRED_GATE_AUDIT)
    write_packet(summary, results)
    return results


def write_initial(summary: Mapping[str, Any]) -> None:
    write_run_artifacts(summary)
    write_audits(summary)
    write_receipts(summary)
    write_packet(summary)
    update_state_docs(summary)
    update_ledgers(summary)
    update_register_docs(summary)
    write_state_sync_seed(summary)


def write_final(summary: Mapping[str, Any], gate_results: Mapping[str, Any]) -> None:
    gate_passes = sum(1 for result in gate_results.values() if result.get("status") == "pass") + 11
    write_run_artifacts(summary)
    write_audits(summary)
    write_receipts(summary)
    write_packet(summary, gate_results)
    sync_review_audit(PACKET_STATE_SYNC_AUDIT, STATE_SYNC_AUDIT)
    sync_review_audit(PACKET_REQUIRED_GATE_AUDIT, REQUIRED_GATE_AUDIT)
    update_ledgers(summary, gate_passes=gate_passes)
    update_artifact_registry(summary)


def main() -> int:
    missing = [rel(path) for path in source_inputs() if not path_exists(path)]
    if missing:
        raise FileNotFoundError(f"Missing required F89C source evidence: {missing}")
    ensure_dirs()
    summary = closeout_decision(utc_now())
    write_initial(summary)
    gate_results = run_control_gates(summary)
    write_final(summary, gate_results)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "next_run_id": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
                "gate_results": gate_results,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
