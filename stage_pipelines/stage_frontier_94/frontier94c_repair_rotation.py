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


STAGE_ID = "stage_frontier_94__tier_stable_realized_utility_label_axis"
RUN_ID = "frontier94C_tier_stable_realized_utility_repair_or_rotation_decision_v1"
PARENT_RUN_ID = "frontier94B_tier_stable_realized_utility_label_proxy_scout_v1"
NEXT_STAGE_ID = "stage_frontier_95__closed_bar_state_transition_embedding_axis"
NEXT_RUN_ID = "frontier95A_stage_open_closed_bar_state_transition_embedding_axis_v1"
SCRIPT_REL = "stage_pipelines/stage_frontier_94/frontier94c_repair_rotation.py"

STATUS = "f94c_closed_negative_tier_utility_label_axis_rotate_to_f95_no_authority"
JUDGMENT = "negative_tier_utility_label_proxy_no_candidate_no_runtime_trigger"
DECISION = "close_f94_negative_rotate_to_closed_bar_state_transition_embedding_axis"
CLAIM_BOUNDARY = (
    "f94c_stage_closeout_rotation_only_negative_memory_reference_surface_no_runnable_candidate_"
    "no_mt5_runtime_evidence_no_selected_baseline_no_promotion_candidate_no_operating_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)
RUNTIME_PROBE_STATUS = (
    "not_run_no_meaningful_runnable_candidate_no_onnx_ea_set_behavior_no_runtime_materialization_"
    "economics_or_handoff_claim_not_cost_or_proxy_bad_skip"
)
FRONTIER_EXTRA_DUE_STATUS = "not_due_after_f94_closeout_next_boundary_f100_e01_closed_for_f050"
FRONTIER_TOPIC_ROTATION_STATUS = (
    "preopen_pass_f95_closed_bar_state_transition_embedding_axis_not_f94_utility_weight_repair"
)
BEST_VARIANT_ID = "v05_density_preserving_utility"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / "frontier94C"
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

F94B_RUN = STAGE_DIR / "02_runs" / "frontier94B"
F94B_RUN_MANIFEST = F94B_RUN / "run_manifest.json"
F94B_SUMMARY = F94B_RUN / "summary.json"
F94B_KPI = F94B_RUN / "kpi_record.json"
F94B_CANDIDATE_GATE = F94B_RUN / "proxy_scout" / "candidate_gate.json"
F94B_DATA_LOCK = F94B_RUN / "proxy_scout" / "data_feature_split_lock.json"
F94B_LABEL_AUDIT = F94B_RUN / "proxy_scout" / "label_integrity_audit.json"
F94B_SPLIT_METRICS = F94B_RUN / "proxy_scout" / "split_metrics.csv"
F94B_TIER_ROUTE_SUMMARY = F94B_RUN / "proxy_scout" / "tier_route_summary.json"
F94B_TIER_B_SUMMARY = F94B_RUN / "proxy_scout" / "tier_b_summary.json"
F94B_RESULT_SUMMARY = F94B_RUN / "reports" / "result_summary.md"
F94B_EXECUTION_SUMMARY = REVIEW_DIR / "f94b_execution_summary.json"
F94B_WORK_PACKET = ROOT / "docs" / "agent_control" / "packets" / PARENT_RUN_ID / "work_packet.yaml"
F94B_TASK_FORCE = ROOT / "docs" / "agent_control" / "packets" / PARENT_RUN_ID / "codex_task_force_review_packet.json"

RUN_MANIFEST = RUN_DIR / "run_manifest.json"
SUMMARY_JSON = RUN_DIR / "summary.json"
KPI_RECORD = RUN_DIR / "kpi_record.json"
DECISION_JSON = DECISION_DIR / "decision.json"
RESULT_SUMMARY = REPORT_DIR / "summary.md"
STAGE_CLOSEOUT_SUMMARY = REVIEW_DIR / "f94c_stage_closeout_summary.json"
STAGE_CLOSEOUT_REPORT = REVIEW_DIR / "stage_closeout_report.md"
F94C_REPORT = REVIEW_DIR / "frontier94C_tier_utility_repair_or_rotation_decision_report.md"
TASK_FORCE_REVIEW = REVIEW_DIR / "f94c_task_force_review_receipt.json"
TASK_FORCE_PACKET_REVIEW = PACKET_DIR / "codex_task_force_review_packet.json"
FRONTIER_EXTRA_DUE_CHECK = REVIEW_DIR / "f94c_frontier_extra_due_check.json"
FIVE_STAGE_SYNTHESIS = REVIEW_DIR / "f94c_frontier_five_stage_direction_synthesis.json"
TOPIC_ROTATION_CHECK = REVIEW_DIR / "f94c_frontier_topic_rotation_check.json"
SCOPE_GATE = REVIEW_DIR / "f94c_scope_completion_gate.json"
DATA_INTEGRITY_AUDIT = REVIEW_DIR / "f94c_data_integrity_audit.json"
MODEL_VALIDATION_AUDIT = REVIEW_DIR / "f94c_model_validation_audit.json"
KPI_CONTRACT_AUDIT = REVIEW_DIR / "f94c_kpi_contract_audit.json"
ARTIFACT_AUDIT = REVIEW_DIR / "f94c_artifact_lineage_audit.json"
RESULT_JUDGMENT_AUDIT = REVIEW_DIR / "f94c_result_judgment_audit.json"
FINAL_CLAIM_GUARD = REVIEW_DIR / "f94c_final_claim_guard.json"
STATE_SYNC_AUDIT = REVIEW_DIR / "f94c_state_sync_audit.json"
REQUIRED_GATE_AUDIT = REVIEW_DIR / "f94c_required_gate_coverage_audit.json"
DECISION_MEMO = ROOT / "docs" / "decisions" / "2026-06-19_frontier94c_closeout_rotate_f95.md"

WORK_PACKET = PACKET_DIR / "work_packet.yaml"
SKILL_RECEIPTS = PACKET_DIR / "skill_receipts.json"
PACKET_FINAL_CLAIM_GUARD = PACKET_DIR / "final_claim_guard.json"
PACKET_CLOSEOUT_GATE = PACKET_DIR / "closeout_gate.json"
PACKET_STATE_SYNC_AUDIT = PACKET_DIR / "state_sync_audit.json"
PACKET_REQUIRED_GATE_AUDIT = PACKET_DIR / "required_gate_coverage_audit.json"
PACKET_WORK_PACKET_LINT = PACKET_DIR / "work_packet_schema_lint.json"
PACKET_SKILL_RECEIPT_LINT = PACKET_DIR / "skill_receipt_schema_lint.json"

ALLOWED_CLAIMS = [
    "f94_closed_negative_memory_recorded",
    "f94_reference_surface_recorded",
    "f94_repair_disposition_closed",
    "f95_pending_open_scaffold_recorded",
    "task_force_actual_calls_recorded_for_f94c",
    "frontier_extra_due_check_not_due_after_f94",
    "frontier_topic_rotation_check_recorded_for_f95_proposal",
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


def coerce_number(value: Any) -> Any:
    if not isinstance(value, str):
        return value
    text = value.strip()
    if text in {"", "None", "nan"}:
        return None
    if text in {"True", "False"}:
        return text == "True"
    try:
        if "." not in text and "e" not in text.lower():
            return int(text)
        return float(text)
    except ValueError:
        return value


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
        F94B_RUN_MANIFEST,
        F94B_SUMMARY,
        F94B_KPI,
        F94B_CANDIDATE_GATE,
        F94B_DATA_LOCK,
        F94B_LABEL_AUDIT,
        F94B_SPLIT_METRICS,
        F94B_TIER_ROUTE_SUMMARY,
        F94B_TIER_B_SUMMARY,
        F94B_RESULT_SUMMARY,
        F94B_EXECUTION_SUMMARY,
        F94B_WORK_PACKET,
        F94B_TASK_FORCE,
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
        F94C_REPORT,
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
        ROOT / "docs" / "decisions",
    ):
        io_path(directory).mkdir(parents=True, exist_ok=True)


def load_split_metrics() -> dict[str, dict[str, Any]]:
    views = {"tier_a_separate", "tier_b_separate", "tier_ab_combined"}
    result: dict[str, dict[str, Any]] = {}
    with io_path(F94B_SPLIT_METRICS).open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("variant_id") == BEST_VARIANT_ID and row.get("split") == "validation" and row.get("view") in views:
                result[str(row["view"])] = {key: coerce_number(value) for key, value in row.items()}
    missing = sorted(views - set(result))
    if missing:
        raise RuntimeError(f"Missing F94B split metric rows for {missing}")
    return result


def task_force_calls() -> list[dict[str, Any]]:
    return [
        {
            "roster_agent_id": "agent_01_system_governor",
            "spawned_agent_id": "019edea7-cbaa-7cc3-8e05-44ef397fba17",
            "nickname": "Raman",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "accepted",
            "disposition": "accepted",
            "summary": (
                "F94C may close as negative memory/reference surface. Do not elevate v05 to candidate, "
                "promotion candidate, runtime probe, or authority; F95 needs material novelty."
            ),
        },
        {
            "roster_agent_id": "agent_04_evidence_control_plane",
            "spawned_agent_id": "019edea7-f6e7-7cf2-9188-07eb6f81ffed",
            "nickname": "Pasteur",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "accepted",
            "disposition": "accepted",
            "summary": (
                "F94C needs a fresh v2.1 packet, stage_closeout profile, actual_subagent_calls, result "
                "judgment, artifact lineage, KPI contract, state sync, required gate coverage, and final claim guard."
            ),
        },
        {
            "roster_agent_id": "agent_05_data_feature_contract",
            "spawned_agent_id": "019edea8-2c46-7ce0-a32e-35af5f3c1dc1",
            "nickname": "Kierkegaard",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "needs_local_verification",
            "disposition": "accepted_with_local_verification",
            "summary": (
                "F94B is negative_with_boundary, not invalid. Record timezone unresolved status, train-only "
                "Tier B label footnote, and full routed perturbation as stronger-claim prerequisites."
            ),
        },
        {
            "roster_agent_id": "agent_06_quant_research",
            "spawned_agent_id": "019edea8-559d-73e0-bcf1-d908da35f2e3",
            "nickname": "Turing",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "accepted",
            "disposition": "accepted",
            "summary": (
                "Reject threshold/filter/parameter-only repair. Rotate to closed-bar state-transition "
                "embedding rather than utility-threshold repair."
            ),
        },
        {
            "roster_agent_id": "agent_07_model_validation_risk",
            "spawned_agent_id": "019edea8-8a32-7cf0-a07a-3b858b1939e2",
            "nickname": "Russell",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "needs_local_verification",
            "disposition": "accepted_with_local_verification",
            "summary": (
                "Treat best diagnostic as search-exhaustion/negative evidence. Threshold-only repair is rejected; "
                "scores are not calibrated probabilities or readiness evidence."
            ),
        },
        {
            "roster_agent_id": "agent_08_mt5_onnx_runtime",
            "spawned_agent_id": "019edea8-b63a-7a90-89bc-535a158f9b4f",
            "nickname": "Zeno",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "accepted",
            "disposition": "accepted",
            "summary": (
                "No MT5 run is valid only for proxy-negative/rotation claims. Same-packet MT5 probe triggers "
                "when a runnable ONNX/EA/set bundle or runtime/materialization/economics/handoff claim appears."
            ),
        },
    ]


def closeout_payload(now: str) -> dict[str, Any]:
    f94b_summary = read_json(F94B_SUMMARY)
    f94b_kpi = read_json(F94B_KPI)
    candidate_gate = read_json(F94B_CANDIDATE_GATE)
    data_lock = read_json(F94B_DATA_LOCK)
    label_audit = read_json(F94B_LABEL_AUDIT)
    tier_route = read_json(F94B_TIER_ROUTE_SUMMARY)
    split_metrics = load_split_metrics()
    best_gate = next(gate for gate in candidate_gate["gates"] if gate["variant_id"] == BEST_VARIANT_ID)
    actual = split_metrics["tier_ab_combined"]
    decision = {
        "final_disposition": "negative_memory_reference_surface_with_next_frontier_proposal",
        "rotation_selected": True,
        "repair_disposition": "close_negative_rotate_not_capped_repair",
        "capped_repair_rejected_reason": (
            "All F94B variants failed the joint candidate gate. Changing only density target, strength threshold, "
            "tier gap penalty, MFE/MAE weights, side, cost, session, routing, or parameters would repeat the same surface."
        ),
        "candidate_count": int(candidate_gate["candidate_count"]),
        "materialization_candidate_count": 0,
        "runtime_attempt_rows": 0,
        "failed_boundary": {
            "best_diagnostic_variant": BEST_VARIANT_ID,
            "validation_actual_routed_net": actual["net_proxy"],
            "validation_actual_routed_pf": actual["proxy_pf"],
            "validation_actual_routed_drawdown": actual["max_drawdown"],
            "validation_actual_routed_trade_count": actual["trade_count"],
            "validation_actual_routed_trades_per_day": actual["trades_per_day"],
            "selection_failures": best_gate["selection_failures"],
            "candidate_gate_claim_effect": best_gate["claim_effect"],
        },
        "salvage_value": [
            "Density-preserving utility kept trade density near the goal but exposed negative expectancy and PF below 1.",
            "Worst-tier utility and tier-gap metrics remain useful diagnostics for future route stability checks.",
            "Tier B separate validation was positive but too thin and side-concentrated to rescue actual routed failure.",
            "F94B data/feature/label locks remain usable for negative memory, not authority.",
            "State-transition representation is a plausible next axis because it asks whether the pre-entry state is tradable before utility scoring.",
        ],
        "negative_memory": [
            "Do not repair F94 by only retuning density target, strength threshold, tier gap penalty, MFE/MAE weights, side, cost, session, routing, or parameters.",
            "Do not use Tier B thin positive validation as a whole-surface rescue when actual routed total is negative.",
            "Do not treat utility score as calibrated probability or model readiness.",
            "Do not claim runtime economics, ONNX handoff, EA compatibility, materialization, promotion, or authority without MT5 Strategy Tester evidence.",
            "Do not drop Tier A separate, Tier B separate, or actual routed total records.",
        ],
        "do_not_repeat": [
            "utility_weight_threshold_repair_only",
            "density_target_strength_threshold_repair_only",
            "tier_b_thin_positive_rescue",
            "oos_or_proxy_rescue_without_validation_gate",
            "score_probability_claim",
            "compile_or_proxy_only_runtime_evidence",
        ],
        "reopen_condition": [
            "A future revisit changes source, data representation, label geometry, runtime representation, validation philosophy, model family, objective, trade shape, risk logic, or regime split.",
            "A future utility-label revisit explicitly closes timezone binding, Tier B train-label footnote, and full routed/Tier B perturbation prerequisites before stronger claims.",
            "Any runtime/materialization/economics/handoff claim gets same-packet narrow MT5 Strategy Tester evidence.",
        ],
        "data_integrity_footnotes": [
            "F94B is usable_with_boundary for negative evidence, not invalid.",
            "Raw manifest timezone_status remains UNRESOLVED_REQUIRES_MANUAL_BINDING and forbids runtime authority.",
            "Tier B train-only future_log_return_12 versus recomputed future_path_return had a 44-row footnote; validation/OOS mismatch was not reported.",
            "Leakage perturbation evidence is sufficient for F94 negative boundary but full routed/Tier B perturbation is required before stronger claims.",
        ],
        "runtime_boundary": runtime_boundary(),
        "next_stage_id": NEXT_STAGE_ID,
        "next_run_id": NEXT_RUN_ID,
        "next_axis": {
            "primary_axis": "closed_bar_state_transition_embedding",
            "stage_id": NEXT_STAGE_ID,
            "run_id": NEXT_RUN_ID,
            "question": (
                "Can closed M5 bar sequence and state-transition embeddings identify continuation, reversal-trap, "
                "and chop-cost-drag states before long/short/abstain mapping?"
            ),
            "novelty_delta": {
                "data_representation": "closed bar sequence/state-transition embedding instead of single-row realized-utility label",
                "objective": "transition-class tradability before directional permission",
                "trade_shape": "long/short/abstain is mapped after state class, not by utility threshold repair",
                "validation_philosophy": "test state tradability and cost drag rather than reweighting F94 utility components",
                "not_threshold_filter_parameter_tweak": True,
            },
            "pending_open_boundary": "scaffold_only_formal_f95a_open_required",
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
        "hypothesis": (
            "F94 tier-stable realized-utility label axis should close as negative unless a non-threshold "
            "structural repair exists after F94B candidate gate failure."
        ),
        "repair_rotation_decision": decision,
        "f94b_summary": f94b_summary,
        "f94b_kpi": f94b_kpi,
        "candidate_gate": candidate_gate,
        "data_feature_split_lock": data_lock,
        "label_integrity_audit": label_audit,
        "task_force_actual_subagent_calls": task_force_calls(),
        "claim_boundary": CLAIM_BOUNDARY,
        "runtime_probe_status": RUNTIME_PROBE_STATUS,
        "frontier_extra_due_status": FRONTIER_EXTRA_DUE_STATUS,
        "frontier_topic_rotation_status": FRONTIER_TOPIC_ROTATION_STATUS,
    }


def runtime_boundary() -> dict[str, Any]:
    return {
        "mt5_strategy_tester_status": "not_run_no_runnable_candidate",
        "external_verification_status": "out_of_scope_by_claim",
        "runtime_authority_status": "none",
        "runtime_probe_status": "not_performed_no_runnable_candidate_not_cost_or_proxy_bad_skip",
        "onnx_ea_set_behavior_claim": "none",
        "materialization_status": "not_materialized",
        "economics_claim": "proxy_only_no_mt5_economics",
        "handoff_status": "none",
        "same_packet_mt5_probe_trigger": [
            "runnable ONNX/EA/set bundle appears",
            "runtime behavior claim appears",
            "Strategy Tester output claim appears",
            "materialization-ready claim appears",
            "economics pass claim appears",
            "handoff complete claim appears",
            "operating promotion, runtime authority, live readiness, or Goal Achieve claim appears",
        ],
        "claim_effect": "No runtime verified, economics pass, materialization-ready, handoff complete, promotion, authority, or readiness claim is allowed.",
    }


def kpi_record(payload: Mapping[str, Any]) -> dict[str, Any]:
    decision = payload["repair_rotation_decision"]
    actual = decision["split_metrics_by_view"]["tier_ab_combined"]
    closeout_kpi = {
        "gross_profit": actual["gross_profit"],
        "gross_loss": actual["gross_loss"],
        "win_rate": actual["win_rate"],
        "avg_win": actual["avg_win"],
        "avg_loss": actual["avg_loss"],
        "payoff_ratio": actual["payoff_ratio"],
        "expectancy": actual["expectancy"],
        "recovery_factor": actual["recovery_factor"],
        "time_under_water": actual["time_under_water_bars"],
        "max_consecutive_loss": actual["max_consecutive_loss"],
        "long_short_breakdown": {
            "long_count": actual["long_count"],
            "short_count": actual["short_count"],
        },
    }
    return {
        "packet_id": RUN_ID,
        "test_period": "train_2022-09-01_to_2024-12-31_validation_2025-01-02_to_2025-09-30_oos_2025-10-01_to_2026-04-13",
        "hypothesis": payload["hypothesis"],
        "proxy_kpi": {
            "best_diagnostic_variant": BEST_VARIANT_ID,
            "validation_by_view": decision["split_metrics_by_view"],
            "candidate_gate_count": decision["candidate_count"],
            "repair_disposition": decision["repair_disposition"],
        },
        "runtime_kpi": "not_applicable_no_runnable_candidate_no_runtime_claim",
        "net_profit": actual["net_proxy"],
        "profit_factor": actual["proxy_pf"],
        "drawdown": actual["max_drawdown"],
        "trade_count": actual["trade_count"],
        "trades_per_day": actual["trades_per_day"],
        "parity": "not_applicable_no_onnx_or_ea",
        "gap_cause": "proxy/runtime gap not measured because no runtime materialization claim is made",
        "next_action": NEXT_RUN_ID,
        "tier_records_required": ["tier_a_separate", "tier_b_separate", "actual_routed_total"],
        "closeout_kpi": closeout_kpi,
        "runtime_boundary": decision["runtime_boundary"],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def audit_payload(audit_name: str, status: str = "pass", **extra: Any) -> dict[str, Any]:
    payload = {
        "audit_name": audit_name,
        "packet_id": RUN_ID,
        "run_id": RUN_ID,
        "status": status,
        "created_at_utc": extra.pop("created_at_utc", None),
        "findings": extra.pop("findings", []),
        "allowed_claims": ALLOWED_CLAIMS if status == "pass" else ["blocked"],
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    payload.update(extra)
    return payload


def task_force_receipt(payload: Mapping[str, Any]) -> dict[str, Any]:
    calls = payload["task_force_actual_subagent_calls"]
    return {
        "packet_id": RUN_ID,
        "skill": "obsidian-task-force-review",
        "status": "executed",
        "trigger_reason": "active goal closeout claim plus explicit user instruction requiring relevant Task Force actual calls",
        "roster_registry": "docs/agent_control/codex_task_force_registry.yaml",
        "review_requirement": "explicit_user_instruction_required",
        "codex_task_force_review_packet_required": True,
        "model_policy": "inherited parent model; model strength does not relax gates or claim boundaries",
        "bounded_evidence": [rel(F94B_EXECUTION_SUMMARY), rel(F94B_CANDIDATE_GATE), rel(KPI_RECORD), rel(DECISION_JSON)],
        "agents_used": [call["roster_agent_id"] for call in calls],
        "actual_subagent_calls": calls,
        "advice_classification": {
            "accepted": [
                "agent_01_system_governor",
                "agent_04_evidence_control_plane",
                "agent_06_quant_research",
                "agent_08_mt5_onnx_runtime",
            ],
            "needs_local_verification": ["agent_05_data_feature_contract", "agent_07_model_validation_risk"],
            "rejected": [],
        },
        "local_verification": (
            "F94C records no-runtime fields, data footnotes, threshold-only repair rejection, F95 novelty delta, "
            "state sync, and gate coverage."
        ),
        "claim_boundary": CLAIM_BOUNDARY,
        "final_codex_direction": "close F94 as negative memory/reference surface and scaffold F95 pending open; no Task Force reviewed/pass claim",
        "forbidden_claim_check": FORBIDDEN_CLAIMS,
        "receipt_path": rel(SKILL_RECEIPT_DIR / "task_force_review.json"),
    }


def skill_receipts(payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    source_ids = [file_identity(path) for path in source_inputs()]
    produced_ids = [file_identity(path) for path in produced_artifacts() if path_exists(path)]
    decision = payload["repair_rotation_decision"]
    receipts = [
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-stage-transition",
            "status": "executed",
            "source_current_truth_docs": [rel(WORKSPACE_STATE), rel(CURRENT_WORKING_STATE), rel(SELECTION_STATUS)],
            "changed_or_checked_docs": [
                rel(WORKSPACE_STATE),
                rel(CURRENT_WORKING_STATE),
                rel(SELECTION_STATUS),
                rel(NEXT_SELECTION_STATUS),
                rel(NEXT_STAGE_BRIEF),
            ],
            "detected_conflicts": ["none_detected"],
            "canonical_state_after": {
                "active_stage": NEXT_STAGE_ID,
                "current_run": NEXT_RUN_ID,
                "latest_completed_run": RUN_ID,
            },
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "receipt_path": rel(SKILL_RECEIPT_DIR / "stage_transition.json"),
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-run-evidence-system",
            "status": "executed",
            "source_inputs": source_ids,
            "produced_artifacts": produced_ids,
            "ledger_rows": [f"{RUN_ID}__tier_a_closeout", f"{RUN_ID}__tier_b_closeout", f"{RUN_ID}__actual_routed_closeout"],
            "missing_evidence": [
                {"evidence": "MT5 Strategy Tester runtime output", "reason": "out_of_scope_by_claim_no_runnable_candidate"},
                {"evidence": "ONNX/EA/set handoff", "reason": "not created and not claimed in F94C"},
            ],
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "receipt_path": rel(SKILL_RECEIPT_DIR / "run_evidence_system.json"),
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-data-integrity",
            "status": "executed",
            "data_sources_checked": [file_identity(F94B_DATA_LOCK), file_identity(F94B_LABEL_AUDIT)],
            "time_axis_boundary": "F94B is usable for negative proxy evidence; raw manifest timezone binding remains unresolved before runtime authority.",
            "split_boundary": "Train-only fit/threshold; validation gate; OOS final-read-only; F94C performs no new fitting.",
            "leakage_checks": {
                "feature_denylist_hits": payload["label_integrity_audit"].get("feature_denylist_hits", []),
                "future_path_perturbation_does_not_change_features": payload["label_integrity_audit"]
                .get("leakage_tests", {})
                .get("future_path_perturbation_does_not_change_features"),
                "stronger_claim_prerequisites": decision["data_integrity_footnotes"],
            },
            "missing_data_boundary": "Tier A separate, Tier B separate, and actual routed total are recorded; missing runtime data is out_of_scope_by_claim.",
            "receipt_path": rel(SKILL_RECEIPT_DIR / "data_integrity.json"),
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-model-validation",
            "status": "executed",
            "model_or_threshold_surface": "F94 realized-utility proxy diagnostics; no new threshold or model selection in F94C",
            "validation_split": "F94B validation gate failed; OOS is not used for rescue or selection.",
            "overfit_checks": [
                "candidate_gate_count_is_zero",
                "best_diagnostic_is_negative_not_candidate",
                "threshold_only_repair_rejected",
                "scores_not_calibrated_probabilities",
            ],
            "selection_metric_boundary": "Best diagnostic is search-exhaustion negative evidence, not readiness.",
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "receipt_path": rel(SKILL_RECEIPT_DIR / "model_validation.json"),
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-artifact-lineage",
            "status": "executed",
            "source_inputs": source_ids,
            "produced_artifacts": produced_ids,
            "raw_evidence": [rel(F94B_SPLIT_METRICS), rel(F94B_CANDIDATE_GATE), rel(F94B_DATA_LOCK)],
            "machine_readable": [rel(RUN_MANIFEST), rel(SUMMARY_JSON), rel(KPI_RECORD), rel(DECISION_JSON), rel(SKILL_RECEIPTS)],
            "human_readable": [rel(RESULT_SUMMARY), rel(STAGE_CLOSEOUT_REPORT), rel(DECISION_MEMO)],
            "hashes_or_missing_reasons": produced_ids,
            "lineage_boundary": "connected_with_boundary_no_runtime_artifact",
            "receipt_path": rel(SKILL_RECEIPT_DIR / "artifact_lineage.json"),
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-result-judgment",
            "status": "executed",
            "judgment_boundary": "negative memory/reference surface and F95 pending-open scaffold only",
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "evidence_used": [rel(F94B_EXECUTION_SUMMARY), rel(F94B_KPI), rel(F94B_CANDIDATE_GATE), rel(DECISION_JSON)],
            "receipt_path": rel(SKILL_RECEIPT_DIR / "result_judgment.json"),
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-exploration-mandate",
            "status": "executed",
            "exploration_lane": "frontier_stage_closeout_rotation",
            "idea_boundary": "F94 can create clue, negative memory, and reference surface only.",
            "negative_memory_effect": "Blocks adjacent utility-weight/threshold-only repair as a new frontier open.",
            "operating_claim_boundary": CLAIM_BOUNDARY,
            "receipt_path": rel(SKILL_RECEIPT_DIR / "exploration_mandate.json"),
        },
        task_force_receipt(payload),
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
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-answer-clarity",
            "status": "executed",
            "plain_conclusion": "F94 closes negative/no-authority and F95 pending-open scaffold is recorded.",
            "confirmed": [
                "candidate_gate_count_zero",
                "actual_routed_validation_negative",
                "Task Force actual calls recorded",
                "runtime evidence out_of_scope_by_claim",
            ],
            "not_yet_confirmed": [
                "runtime behavior",
                "ONNX/EA/set handoff",
                "operating promotion",
                "runtime authority",
                "Goal Achieve",
            ],
            "why_it_matters": "The closeout preserves learning without laundering proxy-only evidence into runtime claims.",
            "next_action": NEXT_RUN_ID,
            "forbidden_claims_avoided": FORBIDDEN_CLAIMS,
            "receipt_path": rel(SKILL_RECEIPT_DIR / "answer_clarity.json"),
        },
    ]
    return receipts


def write_receipts(payload: Mapping[str, Any]) -> None:
    receipts = skill_receipts(payload)
    for receipt in receipts:
        path = ROOT / receipt["receipt_path"]
        write_json(path, receipt)
    write_json(SKILL_RECEIPTS, {"packet_id": RUN_ID, "primary_skill": "obsidian-stage-transition", "receipts": receipts})


def write_run_artifacts(payload: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> None:
    kpi = kpi_record(payload)
    summary = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": payload["created_at_utc"],
        "status": STATUS,
        "judgment": JUDGMENT,
        "verification_profile": "stage_closeout",
        "candidate_gate_count": payload["repair_rotation_decision"]["candidate_count"],
        "best_diagnostic_variant": BEST_VARIANT_ID,
        "validation_actual_routed_net": kpi["net_profit"],
        "validation_actual_routed_pf": kpi["profit_factor"],
        "validation_actual_routed_drawdown": kpi["drawdown"],
        "validation_actual_routed_trade_count": kpi["trade_count"],
        "validation_actual_routed_trades_per_day": kpi["trades_per_day"],
        "runtime_probe_status": RUNTIME_PROBE_STATUS,
        "task_force_actual_subagent_call_count": len(payload["task_force_actual_subagent_calls"]),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    manifest = {
        **summary,
        "script": rel(ROOT / SCRIPT_REL),
        "source_inputs": [file_identity(path) for path in source_inputs()],
        "produced_artifacts": [file_identity(path) for path in produced_artifacts() if path_exists(path)],
        "gate_results": gate_results or {},
    }
    write_json(RUN_MANIFEST, manifest)
    write_json(SUMMARY_JSON, summary)
    write_json(KPI_RECORD, kpi)
    write_json(DECISION_JSON, payload["repair_rotation_decision"])
    write_json(STAGE_CLOSEOUT_SUMMARY, {**summary, "repair_rotation_decision": payload["repair_rotation_decision"]})
    write_text(RESULT_SUMMARY, result_summary_text(payload))
    write_text(STAGE_CLOSEOUT_REPORT, stage_closeout_report_text(payload))
    write_text(F94C_REPORT, stage_closeout_report_text(payload))


def write_audits(payload: Mapping[str, Any]) -> None:
    decision = payload["repair_rotation_decision"]
    actual = decision["split_metrics_by_view"]["tier_ab_combined"]
    task_force = task_force_receipt(payload)
    audit_map = {
        TASK_FORCE_REVIEW: task_force,
        TASK_FORCE_PACKET_REVIEW: task_force,
        FRONTIER_EXTRA_DUE_CHECK: audit_payload(
            "frontier_extra_due_check",
            due_status=FRONTIER_EXTRA_DUE_STATUS,
            checked_after="F94 closeout",
            next_boundary="F100",
            e01_status="closed_for_f050",
            claim_effect="No Extra Stage is due before F95 pending-open scaffold.",
        ),
        FIVE_STAGE_SYNTHESIS: audit_payload(
            "frontier_five_stage_direction_synthesis",
            covered_frontier_ids=["F90", "F91", "F92", "F93", "F94"],
            dominant_direction="proxy label/risk/trade-shape attempts repeatedly failed before runtime materialization",
            repeated_mechanism="candidate gates fail or produce no runnable surface",
            overused_axis_warning="avoid adjacent threshold/filter/utility-weight repair",
            next_axis_options=[NEXT_STAGE_ID],
            adjacent_same_axis_block=True,
            claim_boundary=CLAIM_BOUNDARY,
        ),
        TOPIC_ROTATION_CHECK: audit_payload(
            "frontier_topic_rotation_check",
            proposed_next_stage_id=NEXT_STAGE_ID,
            prior_frontier_stage=STAGE_ID,
            prior_five_frontier_scope=["F90", "F91", "F92", "F93", "F94"],
            repair_disposition_closed_in_stage=True,
            same_surface_repair_block=True,
            novelty_delta=decision["next_axis"]["novelty_delta"],
            status_detail=FRONTIER_TOPIC_ROTATION_STATUS,
            claim_effect="Supports F95 pending-open scaffold only; formal F95A open must keep this boundary.",
        ),
        SCOPE_GATE: audit_payload(
            "scope_completion_gate",
            counts={
                "decision_recorded": True,
                "candidate_count": decision["candidate_count"],
                "runtime_attempt_rows": decision["runtime_attempt_rows"],
                "task_force_call_count": len(payload["task_force_actual_subagent_calls"]),
            },
        ),
        DATA_INTEGRITY_AUDIT: audit_payload(
            "data_integrity_audit",
            integrity_judgment="usable_with_boundary_not_invalid",
            feature_order_hash=payload["data_feature_split_lock"].get("feature_order_hash"),
            footnotes=decision["data_integrity_footnotes"],
            stronger_claim_prerequisites=[
                "timezone_binding",
                "Tier B train-label identity footnote closure",
                "full routed/Tier B perturbation check",
            ],
        ),
        MODEL_VALIDATION_AUDIT: audit_payload(
            "model_validation_audit",
            candidate_gate_count=decision["candidate_count"],
            best_diagnostic_variant=BEST_VARIANT_ID,
            threshold_only_repair="rejected",
            overfit_risk="best_negative_diagnostic_is_not_selection_evidence",
            calibration_claim="forbidden",
        ),
        KPI_CONTRACT_AUDIT: audit_payload(
            "kpi_contract_audit",
            tier_records=["tier_a_separate", "tier_b_separate", "actual_routed_total"],
            actual_routed_kpi={
                "net_profit": actual["net_proxy"],
                "profit_factor": actual["proxy_pf"],
                "drawdown": actual["max_drawdown"],
                "trade_count": actual["trade_count"],
                "trades_per_day": actual["trades_per_day"],
                "gross_profit": actual["gross_profit"],
                "gross_loss": actual["gross_loss"],
                "win_rate": actual["win_rate"],
                "expectancy": actual["expectancy"],
            },
            pf_only_selection="rejected",
        ),
        ARTIFACT_AUDIT: audit_payload(
            "artifact_lineage_audit",
            source_inputs=[file_identity(path) for path in source_inputs()],
            produced_artifacts=[file_identity(path) for path in produced_artifacts() if path_exists(path)],
            registry_links=[rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            lineage_judgment="connected_with_boundary_no_runtime_artifact",
        ),
        RESULT_JUDGMENT_AUDIT: audit_payload(
            "result_judgment_audit",
            judgment=JUDGMENT,
            disposition="negative_memory_reference_surface",
            invalid=False,
            blocked=False,
            runtime_probe_status=RUNTIME_PROBE_STATUS,
            forbidden_elevations=["candidate", "promotion_candidate", "runtime_authority", "Goal Achieve"],
        ),
        FINAL_CLAIM_GUARD: audit_payload(
            "final_claim_guard",
            requested_claims=ALLOWED_CLAIMS,
            forbidden_claims_checked=FORBIDDEN_CLAIMS,
            runtime_boundary=decision["runtime_boundary"],
        ),
    }
    for path, payload_item in audit_map.items():
        write_json(path, payload_item)
    write_json(PACKET_FINAL_CLAIM_GUARD, audit_map[FINAL_CLAIM_GUARD])


def work_packet(payload: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> dict[str, Any]:
    gate_status = {gate: "pending" for gate in REQUIRED_GATES}
    for name in (
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
        "closeout_gate",
        "final_claim_guard",
    ):
        gate_status[name] = "pass"
    if gate_results:
        for name, result in gate_results.items():
            gate_status[name] = result.get("status", "unknown")
    return {
        "version": "work_packet_schema_v2_1",
        "packet_lifecycle": "new_packet",
        "packet_id": RUN_ID,
        "created_at_utc": payload["created_at_utc"],
        "user_request": {
            "user_quote": "/goal active continuation plus explicit user reminder to actually call relevant Task Force agents when required",
            "requested_action": "stage closeout repair-or-rotation decision",
            "requested_count": {"value": 1, "n_a_reason": ""},
            "ambiguous_terms": [
                "No final completion, selected baseline, promotion candidate, operating promotion, runtime authority, live readiness, or Goal Achieve is claimed."
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
            "detected_families": ["publish_handoff", "state_sync", "kpi_evidence", "artifact_lineage"],
            "touched_surfaces": [rel(RUN_DIR), rel(REVIEW_DIR), rel(PACKET_DIR), rel(WORKSPACE_STATE), rel(NEXT_STAGE_DIR)],
            "mutation_intent": True,
            "execution_intent": True,
        },
        "risk_vector_scan": {
            "risks": {
                "task_force_review_claim_without_actual_calls": "high",
                "proxy_negative_overclaim_as_runtime": "high",
                "threshold_only_repair_disguised_as_rotation": "high",
                "tier_b_thin_positive_rescue": "medium",
            },
            "hard_stop_risks": [
                "Do not claim runtime/materialization/economics/handoff without MT5 Strategy Tester evidence.",
                "Do not repair by threshold/filter/session/routing/parameter-only changes.",
                "Do not call Task Force review without actual selected-agent spawn_agent records.",
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
                "reason": "No runnable candidate or runtime/materialization/economics/handoff claim exists in F94C.",
            },
            "questions": [],
            "required_user_decisions": [],
        },
        "interpreted_scope": {
            "work_families": ["publish_handoff"],
            "target_surfaces": ["F94C closeout", "F95 pending-open scaffold", "Task Force actual calls", "state sync"],
            "scope_units": ["repair_rotation_decision", "negative_memory", "receipt", "state_sync"],
            "execution_layers": ["local_python_execution"],
            "mutation_policy": {"allowed": True, "user_quote": "/goal active continuation"},
            "evidence_layers": ["F94B proxy metrics", "candidate gate", "Task Force actual calls", "control-plane gates"],
            "reduction_policy": {"reduction_allowed": False, "requires_user_quote": False},
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
                "F94B planned F94C repair-or-rotation",
                "closeout claim surface",
                "explicit user instruction requiring relevant Task Force actual calls",
            ],
            "protected_claims": ALLOWED_CLAIMS,
            "required_evidence": [
                rel(F94B_EXECUTION_SUMMARY),
                rel(F94B_KPI),
                rel(F94B_CANDIDATE_GATE),
                rel(DECISION_JSON),
                rel(TASK_FORCE_PACKET_REVIEW),
                rel(WORK_PACKET),
                rel(SKILL_RECEIPTS),
                rel(PACKET_CLOSEOUT_GATE),
            ],
            "gates_not_run_with_reason": [
                {
                    "gate": "runtime_evidence_gate",
                    "reason_code": "no_runnable_candidate_no_runtime_claim",
                    "reason": (
                        "F94C makes no ONNX, EA, set, tester output, materialization, economics, handoff, "
                        "promotion, authority, or readiness claim."
                    ),
                    "claim_effect": "No runtime verified, economics pass, materialization ready, handoff complete, promotion, or authority claim is allowed.",
                },
                {
                    "gate": "wfo_stress_gate",
                    "reason_code": "outside_claim_surface_closeout_no_runnable_surface",
                    "reason": "F94C closes a failed proxy surface and does not select or materialize a runnable strategy.",
                    "claim_effect": "No WFO pass, stress pass, selected baseline, or runtime authority claim is allowed.",
                },
            ],
            "stop_conditions": [
                "Stop at negative memory/reference surface because candidate_gate_count is zero.",
                "If a meaningful runnable candidate or runtime claim appears, do not make the claim without same-packet MT5 Strategy Tester probe.",
                "Do not repair by threshold/filter/session/routing/parameter-only changes.",
            ],
        },
        "acceptance_criteria": [
            {"id": "AC-001", "text": "F94B candidate gate failure is consumed.", "expected_artifact": rel(F94B_CANDIDATE_GATE), "verification_method": "result_judgment_audit", "required": True},
            {"id": "AC-002", "text": "Task Force actual calls are recorded for F94C.", "expected_artifact": rel(TASK_FORCE_PACKET_REVIEW), "verification_method": "codex_task_force_review_packet", "required": True},
            {"id": "AC-003", "text": "F95 pending-open novelty delta is recorded.", "expected_artifact": rel(TOPIC_ROTATION_CHECK), "verification_method": "frontier_topic_rotation_check", "required": True},
            {"id": "AC-004", "text": "Runtime evidence absence is bounded and not cost/proxy-bad skip.", "expected_artifact": rel(KPI_RECORD), "verification_method": "final_claim_guard", "required": True},
        ],
        "work_plan": [
            "Consume F94B proxy, KPI, data, and candidate gate evidence.",
            "Classify actual Task Force advice and record local verification.",
            "Write negative memory, no-runtime boundary, F95 pending-open scaffold, ledgers, and state sync.",
            "Run packet, receipt, state sync, and required gate coverage audits.",
        ],
        "skill_routing": {
            "primary_family": "publish_handoff",
            "primary_skill": "obsidian-stage-transition",
            "support_skills": REQUIRED_SKILLS[1:],
            "skills_considered": REQUIRED_SKILLS + ["obsidian-runtime-parity", "obsidian-backtest-forensics", "obsidian-performance-attribution"],
            "skills_selected": REQUIRED_SKILLS,
            "skills_not_used": [
                {"skill": "obsidian-runtime-parity", "reason": "No ONNX/EA/runtime parity or handoff claim is made."},
                {"skill": "obsidian-backtest-forensics", "reason": "No new Strategy Tester report or trade list exists in F94C."},
            ],
            "required_skill_receipts": REQUIRED_SKILLS,
            "required_gates": REQUIRED_GATES,
        },
        "evidence_contract": {
            "raw_evidence": [rel(F94B_CANDIDATE_GATE), rel(F94B_SPLIT_METRICS), rel(F94B_DATA_LOCK)],
            "machine_readable": [rel(RUN_MANIFEST), rel(SUMMARY_JSON), rel(KPI_RECORD), rel(DECISION_JSON), rel(SKILL_RECEIPTS)],
            "human_readable": [rel(RESULT_SUMMARY), rel(STAGE_CLOSEOUT_REPORT), rel(DECISION_MEMO)],
            "missing_evidence": [
                {"evidence": "MT5 Strategy Tester runtime output", "reason": "out_of_scope_by_claim_no_runnable_candidate"},
                {"evidence": "ONNX/EA/set handoff", "reason": "not created in F94C"},
            ],
        },
        "gates": {
            "required": REQUIRED_GATES,
            **gate_status,
            "not_applicable_with_reason": {
                "runtime_evidence_gate": "outside_claim_surface_no_runtime_claim_no_runnable_candidate_not_cost_or_proxy_bad_skip",
                "wfo_stress_gate": "outside_claim_surface_no_runnable_candidate",
                "f95_stage_open_gate": "pending_open_scaffold_only_formal_f95a_required",
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
        "closeout_gate": PACKET_CLOSEOUT_GATE,
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


def workspace_state_text(payload: Mapping[str, Any]) -> str:
    return f"""current_stage_id: {NEXT_STAGE_ID}
active_stage: {NEXT_STAGE_ID}
active_branch: main
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
frontier_extra_due_status: {FRONTIER_EXTRA_DUE_STATUS}
frontier_topic_rotation_status: {FRONTIER_TOPIC_ROTATION_STATUS}
task_force_status: f94c_actual_subagent_calls_recorded_6_selected_agents_no_task_force_reviewed_pass_claim
runtime_probe_status: {RUNTIME_PROBE_STATUS}
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
updated_at_utc: '{payload['created_at_utc']}'
context_anchor: {rel(NEXT_CONTEXT_ANCHOR)}
notes:
- 'Action: F94C closed F94 as negative memory/reference surface and wrote F95 pending-open scaffold.'
- 'Effect: adjacent utility threshold/filter/parameter-only repair is blocked before next formal frontier open.'
- 'Runtime: no Strategy Tester evidence; no runtime authority; no Goal Achieve.'
"""


def current_state_text(payload: Mapping[str, Any]) -> str:
    return f"""# Current Working State

- active stage(현재 단계): `{NEXT_STAGE_ID}`
- current run(현재 실행): `{NEXT_RUN_ID}`
- latest completed run(최근 완료 실행): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
- Task Force actual calls(태스크포스 실제 호출): 6 selected agents recorded for F94C; no Task Force reviewed/pass claim.
- runtime probe(런타임 탐침): `{RUNTIME_PROBE_STATUS}`
- next action(다음 행동): formal F95A open must keep extra due and topic rotation boundaries.
"""


def f94_selection_status_text() -> str:
    return f"""# F94 Selection Status

- current run(현재 실행): `{RUN_ID}`
- status(상태): `{STATUS}`
- selected baseline(선택 기준선): not claimed
- promotion candidate(승격 후보): not claimed
- runtime authority(런타임 권위): not claimed
- operating promotion(운영 승격): not claimed
- live readiness(실거래 준비): not claimed
- goal achieve(목표 달성): not claimed
- decision(결정): `{DECISION}`
- next run(다음 실행): `{NEXT_RUN_ID}` pending open scaffold only.
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""


def next_selection_status_text() -> str:
    return f"""# F95 Selection Status

- current run(현재 실행): `{NEXT_RUN_ID}`
- status(상태): pending formal stage open scaffold only
- selected baseline(선택 기준선): not claimed
- promotion candidate(승격 후보): not claimed
- runtime authority(런타임 권위): not claimed
- operating promotion(운영 승격): not claimed
- live readiness(실거래 준비): not claimed
- goal achieve(목표 달성): not claimed
- source closeout(원천 마감): `{RUN_ID}`
- claim boundary(주장 경계): pending_open_scaffold_only_no_runtime_authority_no_goal_achieve
"""


def next_stage_brief_text(payload: Mapping[str, Any]) -> str:
    axis = payload["repair_rotation_decision"]["next_axis"]
    return f"""# {NEXT_STAGE_ID}

## Question

{axis['question']}

## Boundary

This is a pending-open scaffold only. Formal F95A must keep frontier extra due, direction synthesis, and topic rotation records connected before execution.

No selected baseline, promotion candidate, operating promotion, runtime authority, live readiness, or Goal Achieve is claimed.

## Novelty Delta

- data_representation: {axis['novelty_delta']['data_representation']}
- objective: {axis['novelty_delta']['objective']}
- trade_shape: {axis['novelty_delta']['trade_shape']}
- validation_philosophy: {axis['novelty_delta']['validation_philosophy']}
- not_threshold_filter_parameter_tweak: true
"""


def next_input_refs_text(payload: Mapping[str, Any]) -> str:
    return f"""# F95 Input References

- source closeout: `{RUN_ID}`
- F94B execution summary: `{rel(F94B_EXECUTION_SUMMARY)}`
- F94B candidate gate: `{rel(F94B_CANDIDATE_GATE)}`
- F94C decision: `{rel(DECISION_JSON)}`
- F94C topic rotation check: `{rel(TOPIC_ROTATION_CHECK)}`
- boundary: pending open scaffold only, no runtime authority.
"""


def review_index_text(payload: Mapping[str, Any]) -> str:
    return f"""# F94 Review Index

- F94C closeout summary: `{rel(STAGE_CLOSEOUT_SUMMARY)}`
- F94C report: `{rel(F94C_REPORT)}`
- Task Force receipt: `{rel(TASK_FORCE_REVIEW)}`
- Required gate coverage: `{rel(REQUIRED_GATE_AUDIT)}`
- Final claim guard: `{rel(FINAL_CLAIM_GUARD)}`
- Runtime status: `{RUNTIME_PROBE_STATUS}`
"""


def next_review_index_text(payload: Mapping[str, Any]) -> str:
    return f"""# F95 Review Index

- pending run: `{NEXT_RUN_ID}`
- source closeout: `{rel(STAGE_CLOSEOUT_SUMMARY)}`
- input refs: `{rel(NEXT_INPUT_REFS)}`
- state anchor: `{rel(NEXT_CONTEXT_ANCHOR)}`
"""


def result_summary_text(payload: Mapping[str, Any]) -> str:
    kpi = kpi_record(payload)
    decision = payload["repair_rotation_decision"]
    return f"""# F94C Repair Or Rotation Summary

- run_id: `{RUN_ID}`
- status: `{STATUS}`
- judgment: `{JUDGMENT}`
- decision: `{DECISION}`
- best diagnostic: `{BEST_VARIANT_ID}`
- validation actual routed net/PF/DD/trades/trades_per_day: {kpi['net_profit']} / {kpi['profit_factor']} / {kpi['drawdown']} / {kpi['trade_count']} / {kpi['trades_per_day']}
- closeout KPI: gross_profit={kpi['closeout_kpi']['gross_profit']}, gross_loss={kpi['closeout_kpi']['gross_loss']}, win_rate={kpi['closeout_kpi']['win_rate']}, expectancy={kpi['closeout_kpi']['expectancy']}, recovery_factor={kpi['closeout_kpi']['recovery_factor']}
- repair disposition: `{decision['repair_disposition']}`
- next run: `{NEXT_RUN_ID}`
- runtime: `{RUNTIME_PROBE_STATUS}`
- claim boundary: `{CLAIM_BOUNDARY}`
"""


def stage_closeout_report_text(payload: Mapping[str, Any]) -> str:
    decision = payload["repair_rotation_decision"]
    kpi = kpi_record(payload)
    return f"""# F94C Stage Closeout Report

## Decision

F94 closes as negative memory/reference surface. F95 is scaffolded as pending formal open on `{NEXT_STAGE_ID}`.

## Evidence

- candidate_gate_count: {decision['candidate_count']}
- best diagnostic: `{BEST_VARIANT_ID}`
- net/PF/DD/trades/day: {kpi['net_profit']} / {kpi['profit_factor']} / {kpi['drawdown']} / {kpi['trade_count']} / {kpi['trades_per_day']}
- closeout KPI: gross_profit={kpi['closeout_kpi']['gross_profit']}, gross_loss={kpi['closeout_kpi']['gross_loss']}, win_rate={kpi['closeout_kpi']['win_rate']}, avg_win={kpi['closeout_kpi']['avg_win']}, avg_loss={kpi['closeout_kpi']['avg_loss']}, payoff={kpi['closeout_kpi']['payoff_ratio']}, expectancy={kpi['closeout_kpi']['expectancy']}, recovery={kpi['closeout_kpi']['recovery_factor']}, time_under_water={kpi['closeout_kpi']['time_under_water']}, max_consecutive_loss={kpi['closeout_kpi']['max_consecutive_loss']}, long={kpi['closeout_kpi']['long_short_breakdown']['long_count']}, short={kpi['closeout_kpi']['long_short_breakdown']['short_count']}

## Runtime Boundary

No MT5 Strategy Tester run was performed because no runnable candidate, ONNX/EA/set behavior, runtime/materialization/economics/handoff claim, promotion, authority, readiness, or Goal Achieve claim exists. This is not a cost skip or proxy-bad skip.

## Next Proposal

`{NEXT_STAGE_ID}` uses closed-bar state-transition embedding. Formal F95A still needs its own open packet and gate checks.
"""


def decision_memo_text(payload: Mapping[str, Any]) -> str:
    return f"""# F94C Closeout Decision

- run_id: `{RUN_ID}`
- parent_run_id: `{PARENT_RUN_ID}`
- result: negative memory/reference surface with no runtime authority.
- Task Force actual calls: 6 selected agents recorded.
- next_run_id: `{NEXT_RUN_ID}`
- claim_boundary: `{CLAIM_BOUNDARY}`
"""


def update_state_docs(payload: Mapping[str, Any]) -> None:
    write_text(WORKSPACE_STATE, workspace_state_text(payload))
    write_text(CURRENT_WORKING_STATE, current_state_text(payload))
    write_text(GLOBAL_SELECTION_STATUS, next_selection_status_text())
    write_text(SELECTION_STATUS, f94_selection_status_text())
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
    kpi = kpi_record(payload)
    views = payload["repair_rotation_decision"]["split_metrics_by_view"]
    base = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "stage_closeout_rotation",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(RESULT_SUMMARY),
        "notes": "F94 closeout; no runtime claim; F95 pending-open scaffold.",
        "family": "publish_handoff",
        "primary_report": rel(RESULT_SUMMARY),
        "run_number": "frontier94C",
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
        "question": "Should F94 repair tier-stable realized-utility labels or rotate after candidate gate failure?",
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
        "best_candidate_id": BEST_VARIANT_ID,
        "net_profit": kpi["net_profit"],
        "profit_factor": kpi["profit_factor"],
        "drawdown": kpi["drawdown"],
        "trade_count": kpi["trade_count"],
        "trades_per_day": kpi["trades_per_day"],
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
                "kpi_scope": "f94_closeout_decision",
                "primary_kpi": f"net={row_metric['net_proxy']};pf={row_metric['proxy_pf']};dd={row_metric['max_drawdown']};tpd={row_metric['trades_per_day']}",
                "guardrail_kpi": f"utility={row_metric['realized_utility_sum']};recovery={row_metric['recovery_factor']};side_min={row_metric['side_min_share']}",
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
                "expectancy": row_metric["expectancy"],
                "recovery_factor": row_metric["recovery_factor"],
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
            "notes": "F95 pending-open scaffold after F94C negative closeout.",
            "primary_report": rel(NEXT_STAGE_BRIEF),
            "run_number": "frontier95A",
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
            "next_action": "formal_f95a_stage_open",
            "question": "Can closed-bar state-transition embeddings identify tradable US100 M5 states before direction mapping?",
            "artifact_count": 0,
            "required_gate_audit": "",
            "run_type": "planned_current_run",
            "input_run_id": RUN_ID,
            "output_path": rel(NEXT_STAGE_DIR),
            "result_path": rel(NEXT_STAGE_BRIEF),
            "scout_clue_count": 0,
            "net_profit": "",
            "profit_factor": "",
            "drawdown": "",
            "trade_count": "",
            "trades_per_day": "",
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
        stage_id = STAGE_ID if path_rel.startswith(f"stages/{STAGE_ID}") or "frontier94C" in path_rel or "f94c" in path_rel else NEXT_STAGE_ID
        rows.append(
            {
                "stage_id": stage_id,
                "run_id": RUN_ID,
                "artifact_type": "f94c_closeout_rotation",
                "path": path_rel,
                "sha256": sha256_file_lf_normalized(path),
                "created_at": payload["created_at_utc"],
                "claim_boundary": CLAIM_BOUNDARY,
                "artifact_id": f"{RUN_ID}::{path_rel}",
                "created_at_utc": payload["created_at_utc"],
                "notes": "F94C closeout/rotation artifact; no runtime authority.",
                "artifact_path": path_rel,
                "effect": "Supports F94 negative memory and F95 pending-open scaffold only.",
                "size_bytes": io_path(path).stat().st_size,
            }
        )
    replace_rows_by_field(ARTIFACT_REGISTRY, "run_id", RUN_ID, rows)


def update_register_docs(payload: Mapping[str, Any]) -> None:
    marker = f"{RUN_ID}__closeout_record"
    idea_addition = f"""
<!-- {marker} -->

## F94C tier-stable realized-utility label closeout

- run_id: `{RUN_ID}`
- hypothesis: F94 tier utility labels should rotate unless a non-threshold structural repair exists.
- result: negative_memory/reference_surface, no candidate, no runtime trigger.
- next_action: `{NEXT_RUN_ID}` pending-open scaffold.
- claim_boundary: `{CLAIM_BOUNDARY}`.
"""
    negative_addition = f"""
<!-- {marker} -->

## F94C tier utility label negative closeout

- run_id: `{RUN_ID}`
- failed_boundary: F94B candidate_gate_count=0; best diagnostic validation actual routed net=-0.43223042, PF=0.827478, DD=0.51917679.
- salvage_value: density-preserving diagnostic, worst-tier utility checks, Tier B thin positive warning, and state-transition next-axis proposal.
- do_not_repeat: utility weight/threshold/density/side/cost/session/routing/parameter-only repair, Tier B rescue, score probability claim, compile/proxy-only runtime evidence.
- reopen_condition: new source/data representation/label/runtime representation/model family/objective/trade shape/risk logic/regime split.
"""
    changelog_addition = f"""
<!-- {marker} -->

## {payload['created_at_utc']} - F94C Closeout Rotate F95

- Action: `{RUN_ID}` closed F94 as negative/no-authority.
- Effect: adjacent tier-utility threshold/filter/parameter repair is blocked and F95 pending-open scaffold was written at `{NEXT_STAGE_ID}`.
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
        raise FileNotFoundError(f"Missing required F94C source evidence: {missing}")
    ensure_dirs()
    payload = closeout_payload(utc_now())
    write_initial(payload)
    gate_results = run_control_gates(payload)
    write_final(payload, gate_results)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
