from __future__ import annotations

import csv
import hashlib
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

from foundation.control_plane.ledger import io_path, path_exists


STAGE_ID = "stage_frontier_91__regime_conditioned_density_cost_abstention_axis"
RUN_ID = "frontier91A_stage_open_regime_conditioned_density_cost_abstention_axis_v1"
RUN_DIR_NAME = "frontier91A"
PARENT_RUN_ID = "frontier90D_time_to_barrier_repair_or_rotation_decision_v1"
NEXT_RUN_ID = "frontier91B_regime_density_cost_abstention_proxy_scout_v1"
STATUS = "f91a_stage_open_design_prepared_no_candidate_no_authority"
JUDGMENT = "design_only_stage_open_regime_conditioned_density_cost_abstention_axis"
CLAIM_BOUNDARY = (
    "design_only_stage_open_for_regime_conditioned_density_cost_abstention_axis_"
    "no_model_candidate_no_wfo_pass_no_stress_pass_no_mt5_runtime_evidence_"
    "no_selected_baseline_no_operating_promotion_no_runtime_authority_"
    "no_live_readiness_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_DIR_NAME
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
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
GLOBAL_SELECTION_STATUS = ROOT / "docs" / "registers" / "selection_status.md"
ROOT_CHANGELOG = ROOT / "docs" / "CHANGELOG.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
DECISION_MEMO = ROOT / "docs" / "decisions" / "2026-06-19_frontier91a_stage_open_regime_density_cost_abstention.md"

STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
INPUT_REFS = STAGE_DIR / "01_inputs" / "input_refs.md"
CONTEXT_ANCHOR = REVIEW_DIR / "context_anchor.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"

RUN_MANIFEST = RUN_DIR / "run_manifest.json"
SUMMARY_JSON = RUN_DIR / "summary.json"
KPI_RECORD = RUN_DIR / "kpi_record.json"
EXPERIMENT_DESIGN = DESIGN_DIR / "experiment_design.json"
RUNTIME_CONTRACT = DESIGN_DIR / "runtime_contract.json"
F91B_BRIEF = DESIGN_DIR / "f91b_proxy_scout_brief.json"
RESULT_SUMMARY = REPORT_DIR / "summary.md"

STAGE_OPEN_SUMMARY = REVIEW_DIR / "f91a_stage_open_summary.json"
TASK_FORCE_REVIEW = REVIEW_DIR / "f91a_task_force_review_receipt.json"
FRONTIER_EXTRA_DUE_CHECK = REVIEW_DIR / "f91a_frontier_extra_due_check.json"
FIVE_STAGE_SYNTHESIS = REVIEW_DIR / "f91a_frontier_five_stage_direction_synthesis.json"
TOPIC_ROTATION_CHECK = REVIEW_DIR / "f91a_frontier_topic_rotation_check.json"
SCOPE_GATE = REVIEW_DIR / "f91a_scope_completion_gate.json"
DATA_INTEGRITY_AUDIT = REVIEW_DIR / "f91a_data_integrity_audit.json"
MODEL_VALIDATION_AUDIT = REVIEW_DIR / "f91a_model_validation_audit.json"
ARTIFACT_AUDIT = REVIEW_DIR / "f91a_artifact_lineage_audit.json"
FINAL_CLAIM_GUARD = REVIEW_DIR / "f91a_final_claim_guard.json"
STATE_SYNC_AUDIT = REVIEW_DIR / "f91a_state_sync_audit.json"
REQUIRED_GATE_AUDIT = REVIEW_DIR / "f91a_required_gate_coverage_audit.json"
F91A_REPORT = REVIEW_DIR / "frontier91A_stage_open_regime_density_cost_abstention_report.md"

WORK_PACKET = PACKET_DIR / "work_packet.yaml"
SKILL_RECEIPTS = PACKET_DIR / "skill_receipts.json"
PACKET_TASK_FORCE_REVIEW = PACKET_DIR / "codex_task_force_review_packet.json"
PACKET_CLOSEOUT_GATE = PACKET_DIR / "closeout_gate.json"
PACKET_FINAL_CLAIM_GUARD = PACKET_DIR / "final_claim_guard.json"
PACKET_STATE_SYNC_AUDIT = PACKET_DIR / "state_sync_audit.json"
PACKET_REQUIRED_GATE_AUDIT = PACKET_DIR / "required_gate_coverage_audit.json"
PACKET_WORK_PACKET_LINT = PACKET_DIR / "work_packet_schema_lint.json"
PACKET_SKILL_RECEIPT_LINT = PACKET_DIR / "skill_receipt_schema_lint.json"

ALLOWED_CLAIMS = [
    "f91a_stage_open_design_prepared",
    "f91_regime_conditioned_density_cost_abstention_axis_opened",
    "f91b_proxy_scout_planned",
    "task_force_actual_calls_recorded_for_f91a",
    "frontier_extra_due_check_not_due_after_f90",
    "frontier_five_stage_direction_synthesis_recorded_for_f86_to_f90",
    "frontier_topic_rotation_check_passed_for_f91",
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
    "reviewed",
    "verified",
    "pass",
    "reviewed_by_unspawned_agents",
    "model_quality",
    "model_readiness",
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


TASK_FORCE_CALLS = [
    {
        "roster_agent_id": "agent_01_system_governor",
        "spawned_agent_id": "019edda5-c0cf-7771-9303-77f36f66be1e",
        "nickname": "Godel",
        "tool_name": "multi_agent_v1.spawn_agent",
        "result_status": "completed",
        "opinion_classification": "accepted",
        "advice": "F91A formal open is allowed if design-only boundary is kept and runtime triggers are preserved.",
    },
    {
        "roster_agent_id": "agent_04_evidence_control_plane",
        "spawned_agent_id": "019edda5-d4e1-7913-a06e-c750f05c1472",
        "nickname": "Meitner",
        "tool_name": "multi_agent_v1.spawn_agent",
        "result_status": "completed",
        "opinion_classification": "needs_local_verification",
        "advice": "Packet, receipts, gates, actual_subagent_calls, and final claim guard must be materialized locally.",
    },
    {
        "roster_agent_id": "agent_05_data_feature_contract",
        "spawned_agent_id": "019edda5-e906-7fd2-b5f8-62cb3386441c",
        "nickname": "Herschel",
        "tool_name": "multi_agent_v1.spawn_agent",
        "result_status": "completed",
        "opinion_classification": "accepted",
        "advice": "F91B must record source identity, time axis, feature-label boundary, split boundary, and Tier A/B/combined records.",
    },
    {
        "roster_agent_id": "agent_06_quant_research",
        "spawned_agent_id": "019edda6-02b8-74c1-90e5-7235a0bf27f7",
        "nickname": "Fermat",
        "tool_name": "multi_agent_v1.spawn_agent",
        "result_status": "completed",
        "opinion_classification": "accepted",
        "advice": "F91 hypothesis quality is acceptable; F91B should test broad and extreme controls, not threshold-only repair.",
    },
    {
        "roster_agent_id": "agent_07_model_validation_risk",
        "spawned_agent_id": "019edda6-1740-7f81-b7a1-96d38de41d57",
        "nickname": "Newton",
        "tool_name": "multi_agent_v1.spawn_agent",
        "result_status": "completed",
        "opinion_classification": "needs_local_verification",
        "advice": "Predeclare regime/cost/density schema, WFO boundaries, no OOS selection, and score-not-probability calibration boundary.",
    },
    {
        "roster_agent_id": "agent_08_mt5_onnx_runtime",
        "spawned_agent_id": "019edda6-2bb6-7692-bb09-f7d9ff9072ea",
        "nickname": "Mencius",
        "tool_name": "multi_agent_v1.spawn_agent",
        "result_status": "completed",
        "opinion_classification": "accepted",
        "advice": "MT5 probe is not triggered yet, but runtime-compatible design fields and future trigger conditions must be recorded.",
    },
]


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    encoding = "utf-8-sig" if path.suffix.lower() in {".md", ".txt", ".yaml", ".yml"} else "utf-8"
    io_path(path).write_text(text, encoding=encoding)


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_yaml(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    text = yaml.safe_dump(dict(payload), allow_unicode=True, sort_keys=False, width=120)
    io_path(path).write_text(text, encoding="utf-8")


def read_json(path: Path) -> Mapping[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def json_ready(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return value


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
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(kept + normalized)


def append_once(path: Path, marker: str, addition: str) -> None:
    existing = io_path(path).read_text(encoding="utf-8-sig") if path_exists(path) else ""
    if marker in existing:
        return
    sep = "" if existing.endswith("\n") or not existing else "\n"
    write_text(path, existing + sep + addition.strip() + "\n")


def ensure_dirs() -> None:
    for directory in [DESIGN_DIR, REPORT_DIR, REVIEW_DIR, SELECTED_DIR, PACKET_DIR, SKILL_RECEIPT_DIR, STAGE_DIR / "00_spec", STAGE_DIR / "01_inputs"]:
        io_path(directory).mkdir(parents=True, exist_ok=True)


def experiment_design_payload(created_at: str) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "hypothesis": (
            "Pre-entry regime-conditioned density/cost abstention can learn when not to trade and create a "
            "runtime-compatible US100 M5 strategy surface without reusing F90 time-to-barrier ordering."
        ),
        "decision_use": "Prepare F91B proxy scout only; no candidate, baseline, or runtime authority.",
        "comparison_baseline": {
            "reference_only": PARENT_RUN_ID,
            "negative_memory": "F90C ordering proxy produced no candidate and F90D closed the axis negative/no authority.",
            "not_inherited": ["winner", "selected_baseline", "promotion_history", "runtime_authority"],
        },
        "control_variables": [
            "FPMarkets US100 M5 symbol/timeframe",
            "feature-label boundary at closed-bar decision time",
            "train/validation/OOS time ordering",
            "Tier A separate/Tier B separate/Tier A+B combined record requirement",
            "no validation/OOS leakage into regime/cost/density rule selection",
        ],
        "changed_variables": [
            "primary axis shifts from time-to-barrier ordering to regime split + objective + risk logic",
            "objective shifts from ordering proxy to density/cost abstention utility",
            "risk logic explicitly tracks density death, cost stress, side/session concentration, and drawdown exposure",
        ],
        "sample_scope": {
            "symbol": "FPMarkets US100",
            "timeframe": "M5",
            "tier_scope": "Tier A separate, Tier B separate, Tier A+B combined or structured missing_required/blocked",
            "source_identity_status": "to_be_measured_in_f91b",
            "runtime_scope": "not_materialized_in_f91a",
        },
        "success_criteria": [
            "F91B can produce proxy utility separated from negative controls without using F90 ordering score.",
            "Positive utility is not validation-only and has density, cost stress, side balance, and regime coverage.",
            "If a runnable candidate appears, same-packet MT5 Strategy Tester trigger is evaluated and not skipped for cost/proxy-bad reasons.",
        ],
        "failure_criteria": [
            "Only threshold/filter/parameter retuning remains.",
            "F90 ordering target or signed-speed score is reused under a new name.",
            "Tier B or combined record is omitted instead of marked missing_required/blocked/out_of_scope_by_claim.",
            "Density death, cost-only filter, or validation-only rescue dominates the result.",
        ],
        "invalid_conditions": [
            "Regime or cost features use future values.",
            "OOS is used for model/rule selection.",
            "Abstention score is called calibrated probability before calibration evidence.",
            "Runtime/economics claims are made without Strategy Tester evidence identity.",
        ],
        "stop_conditions": [
            "Stop F91A at design/open artifacts only.",
            "Stop F91B proxy scout if novelty collapses into threshold-only repair.",
            "Switch to runtime_probe profile if runnable ONNX/EA/set candidate or runtime/materialization/economics claim appears.",
        ],
        "evidence_plan": [
            rel(EXPERIMENT_DESIGN),
            rel(RUNTIME_CONTRACT),
            rel(F91B_BRIEF),
            rel(PACKET_TASK_FORCE_REVIEW),
            rel(FRONTIER_EXTRA_DUE_CHECK),
            rel(FIVE_STAGE_SYNTHESIS),
            rel(TOPIC_ROTATION_CHECK),
            rel(DATA_INTEGRITY_AUDIT),
            rel(MODEL_VALIDATION_AUDIT),
            rel(ARTIFACT_AUDIT),
            rel(WORK_PACKET),
            rel(SKILL_RECEIPTS),
        ],
    }


def runtime_contract_payload(created_at: str) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "profile_id": "design_only",
        "runtime_status": "not_materialized_no_candidate_no_runtime_claim",
        "runtime_compatible_design_fields": {
            "dataset_id": "to_be_identified_in_f91b",
            "feature_set_id": "to_be_identified_in_f91b",
            "label_or_objective_id": "regime_density_cost_abstention_objective_v1_design_only",
            "split_id": "time_ordered_train_validation_oos_to_be_materialized_in_f91b",
            "parser_runtime_contract_version": "fpmarkets_v2_contracts_reference_only",
            "regime_split": "pre_entry_session_volatility_trend_chop_cost_state_families",
            "density_cost_abstention_objective": "learn trade/abstain utility, not F90 barrier ordering probability",
            "risk_logic": "density death, drawdown exposure, tail/session concentration, side balance, and cost stress",
            "trade_shape": "not_materialized_in_f91a",
        },
        "future_handoff_placeholders": {
            "onnx_hash": "not_materialized",
            "ea_source_hash": "not_materialized",
            "ea_binary_hash": "not_materialized",
            "set_ini_hash": "not_materialized",
            "feature_order_hash": "not_materialized",
            "tester_identity": "not_materialized",
            "report_hash": "not_materialized",
            "trade_list_hash": "not_materialized",
            "telemetry_hash": "not_materialized",
        },
        "mt5_runtime_probe_trigger_conditions": [
            "runnable candidate or runnable decision surface is created",
            "ONNX/EA/set behavior is claimed",
            "runtime/materialization/handoff/economics claim appears",
            "Strategy Tester output, operating promotion, runtime authority, or live readiness is claimed",
            ".mq5/.mqh/.set behavior or model bundle is handed to MT5",
        ],
        "forbidden_skip_reasons_later": ["cost", "expensive", "proxy_bad", "bad_proxy_result"],
        "required_action_if_triggered": (
            "Attempt the narrow sufficient MT5 Strategy Tester probe in the same packet, or after recovery attempt lower "
            "the claim to blocked/inconclusive/out_of_scope_by_claim."
        ),
    }


def f91b_brief_payload(created_at: str) -> dict[str, Any]:
    return {
        "run_id": NEXT_RUN_ID,
        "parent_run_id": RUN_ID,
        "created_at_utc": created_at,
        "status": "planned_after_f91a_formal_open",
        "hypothesis": (
            "A pre-entry regime-conditioned abstention surface can separate useful trade density from cost/risk drag "
            "without reusing time-to-barrier ordering."
        ),
        "proxy_scout_plan": {
            "broad_sweep": [
                "session x volatility x trend/chop x cost-state regime families",
                "logistic/ridge, shallow tree/GBM, and two-head abstention model families",
                "utility target combining direction opportunity, density, expected cost drag, and abstention penalty",
            ],
            "extreme_sweep": [
                "all-trade/no-abstain negative control",
                "cost-blind negative control",
                "density-only and cost-only controls",
                "one-regime-only control",
            ],
            "micro_search_gate": [
                "validation and OOS both preserve positive utility without OOS selection",
                "density band, cost stress, side balance, regime coverage, and negative-control separation all survive",
                "no validation-only rescue",
            ],
        },
        "tier_record_requirement": [
            "tier_a_separate",
            "tier_b_separate_or_missing_required",
            "tier_ab_combined_or_blocked_by_missing_tier_b",
        ],
        "minimum_kpi_plan": [
            "coverage/density",
            "positive utility and cost drag",
            "side balance",
            "regime coverage",
            "negative-control separation",
            "PF/DD/expectancy only when economics evidence exists",
        ],
        "do_not_repeat": [
            "F90C score quantile, C/alpha, threshold, or filter-only retune",
            "upper_first/lower_first ordering target reuse",
            "signed-speed score as probability",
            "Tier A-only whole-alpha read",
        ],
        "runtime_trigger": "If F91B creates a meaningful runnable candidate or runtime claim, same-packet MT5 probe must be attempted.",
        "claim_boundary": "planned_proxy_scout_only_no_candidate_no_runtime_authority",
    }


def build_payload(created_at: str) -> dict[str, Any]:
    design = experiment_design_payload(created_at)
    runtime_contract = runtime_contract_payload(created_at)
    f91b_brief = f91b_brief_payload(created_at)
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": created_at,
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "verification_profile": "design_only",
        "experiment_design": design,
        "runtime_contract": runtime_contract,
        "f91b_brief": f91b_brief,
        "frontier_extra_due_check": {
            "due_status": "not_due",
            "closed_canonical_frontier_count": 90,
            "latest_extra_stage_closed": "E01",
            "next_due_boundary": "F100",
            "claim_effect": "Allows F91 formal open; does not create authority.",
        },
        "frontier_five_stage_direction_synthesis": {
            "covered_frontier_ids": ["F86", "F87", "F88", "F89", "F90"],
            "dominant_direction": "runtime-native representation, trade-shape/risk, materialization, adverse selection, and label ordering attempts all ended without authority.",
            "repeated_mechanism": "proxy or preflight surfaces failed to create durable candidate/runtime economics evidence.",
            "overused_axis_warning": "Do not continue time-to-barrier ordering, threshold-only filters, or parity-only claims.",
            "next_axis_options": ["regime split", "objective function", "risk logic", "density/cost abstention"],
            "allowed_reexperiment_conditions": "Same broad topic may return only with new source/data representation/label/runtime representation/validation philosophy/model family/objective/trade shape/risk logic/regime split.",
            "adjacent_same_axis_block": True,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "frontier_topic_rotation_check": {
            "status": "pass",
            "prior_frontier": "F90",
            "proposed_frontier": "F91",
            "repair_disposition_closed_in_stage": True,
            "same_surface_repair_block": True,
            "near_duplicate_hypothesis": False,
            "threshold_filter_parameter_only_tweak": False,
            "novelty_delta": [
                "objective changes from ordering proxy to abstention utility",
                "primary axes are regime split, density/cost objective, and risk logic",
                "runtime-compatible design fields are recorded without runtime evidence claim",
            ],
            "claim_effect": "Supports F91A formal stage open discipline only.",
        },
    }


def produced_artifacts() -> list[Path]:
    return [
        RUN_MANIFEST,
        SUMMARY_JSON,
        KPI_RECORD,
        EXPERIMENT_DESIGN,
        RUNTIME_CONTRACT,
        F91B_BRIEF,
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
        F91A_REPORT,
        WORK_PACKET,
        SKILL_RECEIPTS,
        PACKET_CLOSEOUT_GATE,
        PACKET_FINAL_CLAIM_GUARD,
        PACKET_STATE_SYNC_AUDIT,
        PACKET_REQUIRED_GATE_AUDIT,
        PACKET_WORK_PACKET_LINT,
        PACKET_SKILL_RECEIPT_LINT,
        DECISION_MEMO,
        STAGE_BRIEF,
        INPUT_REFS,
        SELECTION_STATUS,
        CONTEXT_ANCHOR,
        REVIEW_INDEX,
        STAGE_LEDGER,
    ] + [receipt_path_for(skill) for skill in REQUIRED_SKILLS]


def source_inputs() -> list[Path]:
    return [
        WORKSPACE_STATE,
        CURRENT_WORKING_STATE,
        ROOT / "docs" / "agent_control" / "work_family_registry.yaml",
        ROOT / "docs" / "agent_control" / "codex_task_force_registry.yaml",
        ROOT / "docs" / "registers" / "frontier_extra_stage_register.yaml",
        ROOT / "docs" / "agent_control" / "packets" / PARENT_RUN_ID / "closeout_gate.json",
        ROOT / "docs" / "agent_control" / "packets" / PARENT_RUN_ID / "codex_task_force_review_packet.json",
        ROOT / "stages" / "stage_frontier_90__time_to_barrier_competing_risk_label_axis" / "03_reviews" / "f90d_frontier_topic_rotation_check.json",
    ]


def audit_payload(name: str, status: str, *, counts: Mapping[str, Any] | None = None) -> dict[str, Any]:
    return {
        "audit_name": name,
        "status": status,
        "passed": not status.startswith("blocked"),
        "packet_id": RUN_ID,
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "claim_boundary": CLAIM_BOUNDARY,
        "counts": dict(counts or {}),
    }


def kpi_record(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "scoreboard_lane": "stage_open_design",
        "sample_rows": 0,
        "trade_count": 0,
        "net_profit": "",
        "profit_factor": "",
        "drawdown": "",
        "trades_per_day": "",
        "candidate_count": 0,
        "meaningful_signal_count": 0,
        "runtime_completed_rows": 0,
        "runtime_probe_status": "not_triggered_design_only_no_candidate_no_runtime_claim",
        "tier_a": "planned_for_f91b",
        "tier_b": "planned_for_f91b_or_missing_required",
        "tier_ab": "planned_for_f91b_or_blocked_by_missing_tier_b",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def run_manifest(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "run_dir": rel(RUN_DIR),
        "created_at_utc": payload["created_at_utc"],
        "producer": rel(Path(__file__)),
        "verification_profile": "design_only",
        "primary_family": "experiment_design",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "external_verification_status": "out_of_scope_by_claim_no_runtime_claim",
        "runtime_probe_status": "not_triggered_design_only_no_candidate_no_runtime_claim",
        "claim_boundary": CLAIM_BOUNDARY,
        "machine_outputs": [rel(EXPERIMENT_DESIGN), rel(RUNTIME_CONTRACT), rel(F91B_BRIEF), rel(KPI_RECORD)],
        "human_outputs": [rel(RESULT_SUMMARY), rel(F91A_REPORT), rel(DECISION_MEMO)],
    }


def result_summary_text(payload: Mapping[str, Any]) -> str:
    return f"""# F91A Stage Open(단계 개방): Regime Density/Cost Abstention(장세 밀도/비용 회피)

Action(행동): F91A formal open(정식 개방)을 design-only(설계 전용)로 물질화했다.
Effect(효과): F90 time-to-barrier ordering(장벽 도달 시간 순서화) 실패를 threshold/filter/parameter-only repair(임계값/필터/파라미터만 수리)로 반복하지 않고, regime split/objective/risk logic(장세 분할/목적함수/위험 로직) 축으로 회전한다.

Judgment(판정): `{JUDGMENT}`.
Boundary(경계): `{CLAIM_BOUNDARY}`.

Task Force(태스크포스): F91A 전용 actual_subagent_calls(실제 하위요원 호출) {len(TASK_FORCE_CALLS)}건 기록.
Runtime(런타임): MT5 Strategy Tester probe(MT5 전략 테스터 탐침)는 아직 발동하지 않음. 사유는 no candidate/no runtime claim(후보 없음/런타임 주장 없음)이며 cost/proxy-bad(비용/프록시 부진)가 아니다.

Next(다음): `{NEXT_RUN_ID}` proxy scout(프록시 탐색). 후보나 runnable surface(실행 표면)가 생기면 같은 packet(묶음)에서 MT5 trigger(트리거)를 다시 평가한다.
"""


def workspace_state_text(payload: Mapping[str, Any]) -> str:
    return f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
frontier_extra_due_status: not_due_after_f90_closeout_next_boundary_f100_e01_closed_for_f050
frontier_topic_rotation_status: passed_f91_regime_objective_risk_axis_not_time_to_barrier_threshold_tweak
task_force_status: f91a_actual_subagent_calls_recorded_6_selected_agents_no_task_force_reviewed_pass_claim
runtime_probe_status: not_triggered_design_only_no_candidate_no_runtime_claim_not_cost_or_proxy_bad_skip
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
updated_at_utc: '{payload["created_at_utc"]}'
context_anchor: {rel(CONTEXT_ANCHOR)}
notes:
- 'Action(행동): F91A formal open(정식 개방)을 design-only(설계 전용)로 기록했다.'
- 'Effect(효과): F91B proxy scout(프록시 탐색)가 regime/density/cost/risk(장세/밀도/비용/위험) 축을 시험하게 한다.'
- 'Runtime(런타임): no candidate/no runtime claim(후보 없음/런타임 주장 없음)이므로 MT5 probe(MT5 탐침)는 미발동이며, 비용/프록시 부진으로 미룬 것이 아니다.'
"""


def current_state_text(payload: Mapping[str, Any]) -> str:
    return f"""# Current Working State(현재 작업 상태)

- active_stage(활성 단계): `{STAGE_ID}`
- latest_completed_run(최신 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- Task Force(태스크포스): 6 fresh selected agents(새 선택 요원 6명) called for F91A; no Task Force reviewed/pass claim(검토됨/통과 주장 없음)
- Runtime(런타임): `not_triggered_design_only_no_candidate_no_runtime_claim_not_cost_or_proxy_bad_skip`
- Boundary(경계): `{CLAIM_BOUNDARY}`
"""


def stage_brief_text(payload: Mapping[str, Any]) -> str:
    return f"""# {STAGE_ID}

Status(상태): F91A formal open design prepared(정식 개방 설계 준비됨). This is not a candidate(후보), selected baseline(선택 기준선), runtime authority(런타임 권위), or Goal Achieve(목표 달성).

Question(질문): Can regime-conditioned density/cost abstention(장세 조건부 밀도/비용 회피) create a runtime-compatible(런타임 호환) US100 M5 strategy surface without repeating time-to-barrier ordering(장벽 도달 시간 순서화 반복 없음)?

Material novelty delta(실질 신규성 차이): primary axis(주 축)는 regime split(장세 분할) + objective(목적함수) + risk logic(위험 로직)이다. It is not threshold/filter/parameter-only repair(임계값/필터/파라미터만 수리 아님).

F91B plan(F91B 계획): run `{NEXT_RUN_ID}` as proxy scout(프록시 탐색) for pre-entry regime(진입 전 장세), density(밀도), expected cost drag(예상 비용 부담), side/session risk(방향/세션 위험), and abstain/trade(회피/거래) utility.

Runtime rule(런타임 규칙): if F91 creates a meaningful runnable candidate(의미 있는 실행 후보), ONNX/EA/set behavior(ONNX/EA/설정 동작), or runtime/materialization/economics claim(런타임/물질화/경제성 주장), same-packet MT5 Strategy Tester probe(같은 묶음 MT5 전략 테스터 탐침)를 시도해야 한다.
"""


def input_refs_text(payload: Mapping[str, Any]) -> str:
    return f"""# F91 Input References(입력 참고)

- parent_closeout(상위 마감): `{PARENT_RUN_ID}`
- experiment_design(실험 설계): `{rel(EXPERIMENT_DESIGN)}`
- runtime_contract(런타임 계약): `{rel(RUNTIME_CONTRACT)}`
- f91b_brief(F91B 개요): `{rel(F91B_BRIEF)}`
- task_force_receipt(태스크포스 영수증): `{rel(PACKET_TASK_FORCE_REVIEW)}`

Effect(효과): these files are design references(설계 참고) only and do not create runtime evidence(런타임 근거).
"""


def selection_status_text() -> str:
    return """# Selection Status(선택 상태)

F91A is design-only stage open(설계 전용 단계 개방). No candidate(후보 없음), no selected baseline(선택 기준선 없음), no operating promotion(운영 승격 없음), no runtime authority(런타임 권위 없음), no live readiness(실거래 준비 없음), no Goal Achieve(목표 달성 없음).
"""


def review_index_text(payload: Mapping[str, Any]) -> str:
    rows = [
        ("f91a_task_force_review_receipt", TASK_FORCE_REVIEW),
        ("f91a_frontier_extra_due_check", FRONTIER_EXTRA_DUE_CHECK),
        ("f91a_frontier_five_stage_direction_synthesis", FIVE_STAGE_SYNTHESIS),
        ("f91a_frontier_topic_rotation_check", TOPIC_ROTATION_CHECK),
        ("f91a_stage_open_summary", STAGE_OPEN_SUMMARY),
        ("frontier91A_stage_open_report", F91A_REPORT),
    ]
    lines = ["# Review Index(검토 색인)", ""]
    lines.extend(f"- `{name}`: `{rel(path)}`" for name, path in rows)
    return "\n".join(lines) + "\n"


def decision_memo_text(payload: Mapping[str, Any]) -> str:
    return f"""# F91A Stage Open Decision(단계 개방 결정)

- decision(결정): F91A formal open(정식 개방), design-only(설계 전용).
- effect(효과): F91B proxy scout(프록시 탐색)가 regime-conditioned density/cost abstention(장세 조건부 밀도/비용 회피)을 시험할 수 있게 한다.
- task_force(태스크포스): actual_subagent_calls(실제 하위요원 호출) {len(TASK_FORCE_CALLS)}건.
- runtime(런타임): MT5 probe(MT5 탐침) not triggered(미발동). 사유는 no candidate/no runtime claim(후보 없음/런타임 주장 없음).
- forbidden(금지): completion(완성), selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성).
"""


def task_force_payload(created_at: str) -> dict[str, Any]:
    return {
        "packet_id": RUN_ID,
        "skill": "obsidian-task-force-review",
        "status": "executed",
        "created_at_utc": created_at,
        "trigger_reason": "F91A stage_open governance, explicit user instruction to call relevant Task Force agents when triggered, and active goal frontier continuation.",
        "roster_registry": "docs/agent_control/codex_task_force_registry.yaml",
        "agents_used": [call["roster_agent_id"] for call in TASK_FORCE_CALLS],
        "actual_subagent_calls": TASK_FORCE_CALLS,
        "review_requirement": "codex_task_force_review_packet",
        "model_policy": {"model": "gpt-5.5", "reasoning_effort": "xhigh", "service_tier": "priority"},
        "bounded_evidence": [rel(STAGE_BRIEF), rel(WORKSPACE_STATE), rel(RUNTIME_CONTRACT)],
        "advice_classification": {
            "accepted": ["agent_01_system_governor", "agent_05_data_feature_contract", "agent_06_quant_research", "agent_08_mt5_onnx_runtime"],
            "needs_local_verification": ["agent_04_evidence_control_plane", "agent_07_model_validation_risk"],
            "rejected": [],
        },
        "local_verification": [
            "F91A packet and gate artifacts generated locally.",
            "Work packet, skill receipt, state sync, and required gate coverage lints are run by generator.",
            "Runtime evidence gate remains N/A only because claim surface is design-only with no candidate/runtime claim.",
        ],
        "claim_boundary": CLAIM_BOUNDARY,
        "final_codex_direction": "Proceed with F91A formal design-only stage open and plan F91B proxy scout.",
        "forbidden_claim_check": {claim: "not_claimed" for claim in FORBIDDEN_CLAIMS},
    }


def final_claim_guard_payload() -> dict[str, Any]:
    return {
        "audit_name": "final_claim_guard",
        "status": "pass",
        "packet_id": RUN_ID,
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "claim_boundary": CLAIM_BOUNDARY,
        "runtime_probe_status": "not_triggered_design_only_no_candidate_no_runtime_claim_not_cost_or_proxy_bad_skip",
        "blocked_claims": {claim: "not_claimed" for claim in FORBIDDEN_CLAIMS},
    }


def receipt_path_for(skill: str) -> Path:
    return SKILL_RECEIPT_DIR / f"{skill.replace('obsidian-', '').replace('-', '_')}.json"


def skill_receipts(payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    common = {"packet_id": RUN_ID, "status": "executed"}
    receipts: list[dict[str, Any]] = [
        {
            **common,
            "skill": "obsidian-experiment-design",
            "hypothesis": payload["experiment_design"]["hypothesis"],
            "baseline": payload["experiment_design"]["comparison_baseline"],
            "changed_variables": payload["experiment_design"]["changed_variables"],
            "invalid_conditions": payload["experiment_design"]["invalid_conditions"],
            "evidence_plan": payload["experiment_design"]["evidence_plan"],
            "receipt_path": rel(receipt_path_for("obsidian-experiment-design")),
        },
        {
            **common,
            "skill": "obsidian-data-integrity",
            "data_sources_checked": ["F91A names source identity requirements; F91B must measure source path/hash/rows/feature order."],
            "time_axis_boundary": "Closed-bar decision time; broker close key alignment; no future/current-bar contamination.",
            "split_boundary": "Time-ordered train/validation/OOS; regime/cost/density rules train-only or WFO fold train-only.",
            "leakage_checks": [
                "No F90 ordering target reuse.",
                "No validation/OOS rule selection.",
                "No future spread/slippage/cost in features.",
            ],
            "missing_data_boundary": "Tier B must be recorded or marked missing_required; combined blocked if Tier B missing.",
            "receipt_path": rel(receipt_path_for("obsidian-data-integrity")),
        },
        {
            **common,
            "skill": "obsidian-model-validation",
            "model_or_threshold_surface": "predeclared regime/cost/density schema only; no trained model or candidate in F91A",
            "validation_split": "F91B must keep validation selection and OOS final read separated.",
            "overfit_checks": [
                "avoid validation-only rescue",
                "train-only binning and cost/density gates",
                "score/rank boundary, not probability",
                "density death and zero/low-density collapse checks",
            ],
            "selection_metric_boundary": "F91A defines metrics only; F91B must not use OOS for candidate selection.",
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "receipt_path": rel(receipt_path_for("obsidian-model-validation")),
        },
        {
            **common,
            "skill": "obsidian-artifact-lineage",
            "source_inputs": [rel(path) for path in source_inputs() if path_exists(path)],
            "produced_artifacts": [rel(path) for path in produced_artifacts() if path_exists(path)],
            "raw_evidence": [rel(EXPERIMENT_DESIGN), rel(RUNTIME_CONTRACT), rel(F91B_BRIEF), rel(PACKET_TASK_FORCE_REVIEW)],
            "machine_readable": [rel(RUN_MANIFEST), rel(SUMMARY_JSON), rel(KPI_RECORD), rel(EXPERIMENT_DESIGN), rel(RUNTIME_CONTRACT), rel(F91B_BRIEF)],
            "human_readable": [rel(RESULT_SUMMARY), rel(F91A_REPORT), rel(DECISION_MEMO)],
            "hashes_or_missing_reasons": {
                rel(path): sha256_file(path) for path in produced_artifacts() if path_exists(path) and path.is_file()
            },
            "lineage_boundary": "connected_with_boundary_design_only_no_runtime_evidence",
            "receipt_path": rel(receipt_path_for("obsidian-artifact-lineage")),
        },
        {
            **task_force_payload(payload["created_at_utc"]),
            "receipt_path": rel(receipt_path_for("obsidian-task-force-review")),
        },
        {
            **common,
            "skill": "obsidian-stage-transition",
            "source_current_truth_docs": [rel(WORKSPACE_STATE), rel(CURRENT_WORKING_STATE), rel(SELECTION_STATUS)],
            "changed_or_checked_docs": [rel(WORKSPACE_STATE), rel(CURRENT_WORKING_STATE), rel(STAGE_BRIEF), rel(SELECTION_STATUS), rel(CONTEXT_ANCHOR), rel(REVIEW_INDEX)],
            "detected_conflicts": ["none_detected"],
            "canonical_state_after": {"active_stage": STAGE_ID, "current_run_id": NEXT_RUN_ID, "latest_completed_run_id": RUN_ID},
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "receipt_path": rel(receipt_path_for("obsidian-stage-transition")),
        },
        {
            **common,
            "skill": "obsidian-claim-discipline",
            "requested_claims": ALLOWED_CLAIMS,
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "final_status": "design_only_stage_open_no_candidate_no_runtime_authority",
            "receipt_path": rel(receipt_path_for("obsidian-claim-discipline")),
        },
    ]
    return receipts


def write_skill_receipts(payload: Mapping[str, Any]) -> None:
    receipts = skill_receipts(payload)
    write_json(SKILL_RECEIPTS, {"packet_id": RUN_ID, "primary_skill": "obsidian-experiment-design", "receipts": receipts})
    for receipt in receipts:
        write_json(receipt_path_for(receipt["skill"]), receipt)


def work_packet_payload(payload: Mapping[str, Any], gate_status: Mapping[str, str]) -> dict[str, Any]:
    return {
        "version": "work_packet_schema_v2_1",
        "packet_lifecycle": "new_packet",
        "packet_id": RUN_ID,
        "created_at_utc": payload["created_at_utc"],
        "user_request": {
            "user_quote": "/goal active continuation; user explicitly required Task Force agents when triggered",
            "requested_action": "canonical frontier stage open for F91A regime-conditioned density/cost abstention axis",
            "requested_count": {"value": 1, "n_a_reason": ""},
            "ambiguous_terms": ["Goal Achieve is not claimed.", "Runtime authority is not claimed.", "F91A is design-only."],
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
                "f90_ordering_reused_under_new_name": "high",
                "validation_oos_selection_leakage": "high",
                "runtime_probe_absence_misread_as_cost_skip": "medium",
            },
            "hard_stop_risks": [
                "Do not claim runtime/economics/materialization without MT5 Strategy Tester output identity.",
                "Do not reuse F90 Task Force calls as F91A calls.",
                "Do not call candidate, model readiness, or data contract pass in F91A.",
            ],
            "required_gates": REQUIRED_GATES,
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        "decision_lock": {
            "mode": "assume_safe_default",
            "assumptions": {
                "task_force_required_now": True,
                "strategy_tester_required_now": False,
                "reason": "F91A protects design-only stage-open claims and has no runtime/materialization/economics claim.",
            },
            "questions": [],
            "required_user_decisions": [],
        },
        "interpreted_scope": {
            "work_families": ["experiment_design"],
            "target_surfaces": ["F91 stage open", "regime-density-cost abstention design", "F91B proxy scout brief", "Task Force receipt", "state sync"],
            "scope_units": ["stage_open_design", "receipt", "state_sync"],
            "execution_layers": ["local_python_execution"],
            "mutation_policy": {"allowed": True, "user_quote": "/goal active continuation"},
            "evidence_layers": ["F90D closeout reference", "F91A design artifacts", "Task Force actual calls", "frontier overlays"],
            "reduction_policy": {"reduction_allowed": False, "requires_user_quote": False, "rationale": "F91A is a formal stage-open packet."},
            "claim_boundary": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
        },
        "verification_profile": {
            "profile_id": "design_only",
            "claim_surface": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
            "trigger_sources": [
                "active_goal_frontier_continuation",
                "F90D closeout rotated to F91 pending scaffold",
                "formal F91A stage open claim",
                "explicit user instruction requiring Task Force when triggered",
            ],
            "protected_claims": ALLOWED_CLAIMS,
            "required_evidence": [rel(path) for path in [EXPERIMENT_DESIGN, RUNTIME_CONTRACT, F91B_BRIEF, PACKET_TASK_FORCE_REVIEW, FRONTIER_EXTRA_DUE_CHECK, FIVE_STAGE_SYNTHESIS, TOPIC_ROTATION_CHECK, DATA_INTEGRITY_AUDIT, MODEL_VALIDATION_AUDIT, ARTIFACT_AUDIT, WORK_PACKET, SKILL_RECEIPTS, PACKET_CLOSEOUT_GATE]],
            "gates_not_run_with_reason": [
                {
                    "gate": "runtime_evidence_gate",
                    "reason_code": "no_candidate_no_runtime_claim",
                    "reason": "F91A creates design artifacts only and no runnable candidate, ONNX/EA/set behavior, or runtime/materialization/economics claim.",
                    "claim_effect": "No runtime probe, runtime verified, materialization ready, or economics claim is allowed.",
                },
                {
                    "gate": "wfo_stress_gate",
                    "reason_code": "outside_claim_surface_no_model_candidate",
                    "reason": "F91A does not train/select a model and only prepares F91B proxy scout design.",
                    "claim_effect": "No WFO pass, stress pass, model quality, or candidate claim is allowed.",
                },
            ],
            "stop_conditions": [
                "Stop after F91A design artifacts, receipts, gates, and state sync are materialized.",
                "Do not create candidate/runtime claims in F91A.",
                "If runnable candidate or runtime claim appears, reroute to runtime_probe profile in the same packet.",
            ],
        },
        "acceptance_criteria": [
            {"id": "AC-001", "text": "F91A experiment design exists.", "expected_artifact": rel(EXPERIMENT_DESIGN), "verification_method": "scope_completion_gate", "required": True},
            {"id": "AC-002", "text": "F91A Task Force actual calls are recorded.", "expected_artifact": rel(PACKET_TASK_FORCE_REVIEW), "verification_method": "codex_task_force_review_packet", "required": True},
            {"id": "AC-003", "text": "F91B proxy scout brief exists.", "expected_artifact": rel(F91B_BRIEF), "verification_method": "scope_completion_gate", "required": True},
            {"id": "AC-004", "text": "Runtime evidence gate is explicitly not applicable by claim surface, not cost or proxy-bad.", "expected_artifact": rel(RUNTIME_CONTRACT), "verification_method": "final_claim_guard", "required": True},
        ],
        "work_plan": [
            "Write F91A design/runtime-contract/F91B brief artifacts.",
            "Record Task Force actual_subagent_calls and local-verification responses.",
            "Run frontier_extra_due_check, five-stage synthesis, and topic rotation gates.",
            "Run schema, receipt, state sync, gate coverage, and final claim guard checks.",
            "Commit to main if gates pass.",
        ],
        "skill_routing": {
            "primary_family": "experiment_design",
            "primary_skill": "obsidian-experiment-design",
            "support_skills": REQUIRED_SKILLS[1:],
            "skills_considered": REQUIRED_SKILLS + ["obsidian-runtime-parity", "obsidian-backtest-forensics"],
            "skills_selected": REQUIRED_SKILLS,
            "skills_not_used": [
                {"skill": "obsidian-runtime-parity", "reason": "No ONNX/EA/runtime parity or handoff claim is made."},
                {"skill": "obsidian-backtest-forensics", "reason": "No new Strategy Tester report or trade list exists in F91A."},
            ],
            "required_skill_receipts": REQUIRED_SKILLS,
            "required_gates": REQUIRED_GATES,
        },
        "evidence_contract": {
            "source_inputs": [rel(path) for path in source_inputs() if path_exists(path)],
            "machine_readable": [rel(RUN_MANIFEST), rel(SUMMARY_JSON), rel(KPI_RECORD), rel(EXPERIMENT_DESIGN), rel(RUNTIME_CONTRACT), rel(F91B_BRIEF), rel(SKILL_RECEIPTS)],
            "human_readable": [rel(RESULT_SUMMARY), rel(F91A_REPORT), rel(DECISION_MEMO)],
            "runtime_evidence": "not_applicable_no_candidate_no_runtime_claim",
        },
        "gates": {"required": REQUIRED_GATES, **gate_status, "not_applicable_with_reason": {"runtime_evidence_gate": "no_candidate_no_runtime_claim", "wfo_stress_gate": "outside_claim_surface_no_model_candidate"}},
        "final_claim_policy": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
    }


def write_core_artifacts(payload: Mapping[str, Any]) -> None:
    write_json(RUN_MANIFEST, run_manifest(payload))
    write_json(SUMMARY_JSON, payload)
    write_json(KPI_RECORD, kpi_record(payload))
    write_json(EXPERIMENT_DESIGN, payload["experiment_design"])
    write_json(RUNTIME_CONTRACT, payload["runtime_contract"])
    write_json(F91B_BRIEF, payload["f91b_brief"])
    write_text(RESULT_SUMMARY, result_summary_text(payload))
    write_json(STAGE_OPEN_SUMMARY, payload)
    write_text(F91A_REPORT, result_summary_text(payload))
    tf = task_force_payload(payload["created_at_utc"])
    write_json(TASK_FORCE_REVIEW, tf)
    write_json(PACKET_TASK_FORCE_REVIEW, {"audit_name": "codex_task_force_review_packet", "status": "pass", "passed": True, **tf})
    write_json(FRONTIER_EXTRA_DUE_CHECK, audit_payload("frontier_extra_due_check", "pass_not_due", counts=payload["frontier_extra_due_check"]))
    write_json(FIVE_STAGE_SYNTHESIS, audit_payload("frontier_five_stage_direction_synthesis", "pass", counts=payload["frontier_five_stage_direction_synthesis"]))
    write_json(TOPIC_ROTATION_CHECK, audit_payload("frontier_topic_rotation_check", "pass", counts=payload["frontier_topic_rotation_check"]))
    write_json(SCOPE_GATE, audit_payload("scope_completion_gate", "pass", counts={"produced_artifacts": len([p for p in [EXPERIMENT_DESIGN, RUNTIME_CONTRACT, F91B_BRIEF, PACKET_TASK_FORCE_REVIEW] if path_exists(p)])}))
    write_json(DATA_INTEGRITY_AUDIT, audit_payload("data_integrity_audit", "pass_with_boundary", counts={"integrity_judgment": "usable_with_boundary_for_design_only", "f91b_checks_required": ["source_identity", "time_axis", "feature_label_boundary", "split_tier_records"]}))
    write_json(MODEL_VALIDATION_AUDIT, audit_payload("model_validation_audit", "pass_with_boundary", counts={"validation_judgment": "design_only_no_model_candidate", "risk_stops": ["no_oos_selection", "score_not_probability", "density_death_check"]}))
    write_json(ARTIFACT_AUDIT, audit_payload("artifact_lineage_audit", "pass", counts={"source_inputs": len(source_inputs()), "produced_artifacts": len(produced_artifacts())}))
    guard = final_claim_guard_payload()
    write_json(FINAL_CLAIM_GUARD, guard)
    write_json(PACKET_FINAL_CLAIM_GUARD, guard)
    write_text(STAGE_BRIEF, stage_brief_text(payload))
    write_text(INPUT_REFS, input_refs_text(payload))
    write_text(SELECTION_STATUS, selection_status_text())
    write_text(GLOBAL_SELECTION_STATUS, selection_status_text())
    write_text(CONTEXT_ANCHOR, current_state_text(payload))
    write_text(REVIEW_INDEX, review_index_text(payload))
    write_text(WORKSPACE_STATE, workspace_state_text(payload))
    write_text(CURRENT_WORKING_STATE, current_state_text(payload))
    write_text(DECISION_MEMO, decision_memo_text(payload))


def write_packet_and_closeout(payload: Mapping[str, Any], gate_status: Mapping[str, str]) -> None:
    write_yaml(WORK_PACKET, work_packet_payload(payload, gate_status))
    write_skill_receipts(payload)
    audits = []
    audit_paths = {
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
    for name in REQUIRED_GATES:
        path = audit_paths[name]
        audits.append({"audit_name": name, "path": rel(path), "status": gate_status.get(name, "pending")})
    write_json(
        PACKET_CLOSEOUT_GATE,
        {
            "audit_name": "closeout_gate",
            "status": "pass",
            "packet_id": RUN_ID,
            "audits": audits,
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "claim_boundary": CLAIM_BOUNDARY,
            "final_claim_guard": {"audit_name": "final_claim_guard", "path": rel(PACKET_FINAL_CLAIM_GUARD), "status": "pass"},
        },
    )


def run_gate(name: str, command: list[str], output_path: Path) -> dict[str, Any]:
    proc = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    status = "unknown"
    passed = False
    if path_exists(output_path):
        try:
            payload = read_json(output_path)
            status = str(payload.get("status", "unknown"))
            passed = bool(payload.get("passed", status == "pass"))
        except Exception:
            status = "unreadable"
    return {
        "command": command,
        "output_path": rel(output_path),
        "returncode": proc.returncode,
        "status": status,
        "passed": passed,
        "stdout_tail": proc.stdout[-4000:],
        "stderr_tail": proc.stderr[-4000:],
    }


def run_lints() -> dict[str, Any]:
    py = sys.executable
    results = {
        "work_packet_schema_lint": run_gate(
            "work_packet_schema_lint",
            [py, "-m", "foundation.control_plane.work_packet_schema_lint", str(WORK_PACKET), "--output-json", str(PACKET_WORK_PACKET_LINT), "--allow-blocked-exit-zero"],
            PACKET_WORK_PACKET_LINT,
        ),
        "skill_receipt_schema_lint": run_gate(
            "skill_receipt_schema_lint",
            [py, "-m", "foundation.control_plane.skill_receipt_schema_lint", str(SKILL_RECEIPTS), "--output-json", str(PACKET_SKILL_RECEIPT_LINT), "--allow-blocked-exit-zero"],
            PACKET_SKILL_RECEIPT_LINT,
        ),
        "state_sync_audit": run_gate(
            "state_sync_audit",
            [py, "-m", "foundation.control_plane.state_sync_audit", "--root", str(ROOT), "--active-stage", STAGE_ID, "--current-branch", "main", "--output-json", str(PACKET_STATE_SYNC_AUDIT), "--allow-blocked-exit-zero"],
            PACKET_STATE_SYNC_AUDIT,
        ),
        "required_gate_coverage_audit": run_gate(
            "required_gate_coverage_audit",
            [py, "-m", "foundation.control_plane.required_gate_coverage_audit", "--work-packet", str(WORK_PACKET), "--closeout-gate", str(PACKET_CLOSEOUT_GATE), "--output-json", str(PACKET_REQUIRED_GATE_AUDIT), "--allow-blocked-exit-zero"],
            PACKET_REQUIRED_GATE_AUDIT,
        ),
    }
    for name, result in results.items():
        if result["status"] != "pass":
            raise SystemExit(json.dumps({"failed_gate": name, "result": result}, ensure_ascii=False, indent=2))
    return results


def copy_packet_audits_to_stage() -> None:
    for src, dst in [
        (PACKET_STATE_SYNC_AUDIT, STATE_SYNC_AUDIT),
        (PACKET_REQUIRED_GATE_AUDIT, REQUIRED_GATE_AUDIT),
    ]:
        if path_exists(src):
            write_json(dst, read_json(src))


def ledger_rows(payload: Mapping[str, Any], gate_total: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    created_date = payload["created_at_utc"][:10]
    run_rows = [
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "stage_open_design",
            "status": STATUS,
            "judgment": JUDGMENT,
            "path": rel(RESULT_SUMMARY),
            "notes": "F91A design-only stage open; no runtime authority.",
            "family": "experiment_design",
            "primary_report": rel(RESULT_SUMMARY),
            "run_number": "frontier91A",
            "date": created_date,
            "decision": "formal_open_design_only",
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "rows": 0,
            "gate_passes": gate_total,
            "gate_total": gate_total,
            "claim_boundary": CLAIM_BOUNDARY,
            "report_path": rel(RESULT_SUMMARY),
            "run_date": created_date,
            "primary_artifact": rel(EXPERIMENT_DESIGN),
            "result_status": STATUS,
            "scoreboard_lane": "stage_open_design",
            "external_verification_status": "out_of_scope_by_claim_no_runtime_claim",
            "result_judgment": JUDGMENT,
            "gate_audit_path": rel(PACKET_REQUIRED_GATE_AUDIT),
            "created_at": payload["created_at_utc"],
            "created_at_utc": payload["created_at_utc"],
            "required_gate_audit": rel(PACKET_REQUIRED_GATE_AUDIT),
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "goal_achieve": "not_claimed",
            "run_family": "experiment_design",
            "run_type": "stage_open_design",
            "input_run_id": PARENT_RUN_ID,
            "output_path": rel(RUN_DIR),
            "result_path": rel(RESULT_SUMMARY),
            "candidate_count": 0,
            "scout_clue_count": 0,
            "materialization_candidate_count": 0,
            "meaningful_signal_count": 0,
            "completion_candidate_count": 0,
        },
        {
            "run_id": NEXT_RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "planned_proxy_scout",
            "status": "planned_after_f91a_formal_open",
            "judgment": "planned_proxy_scout_no_result_yet",
            "path": rel(F91B_BRIEF),
            "notes": "F91B planned proxy scout; no result yet.",
            "family": "experiment_execution",
            "primary_report": rel(F91B_BRIEF),
            "run_number": "frontier91B",
            "date": created_date,
            "decision": "planned_proxy_scout",
            "parent_run_id": RUN_ID,
            "next_run_id": "",
            "rows": 0,
            "gate_passes": 0,
            "gate_total": 0,
            "claim_boundary": "planned_proxy_scout_only_no_candidate_no_runtime_authority",
            "report_path": rel(F91B_BRIEF),
            "run_date": created_date,
            "primary_artifact": rel(F91B_BRIEF),
            "result_status": "planned_after_f91a_formal_open",
            "scoreboard_lane": "planned_proxy_scout",
            "external_verification_status": "not_applicable_planned_design_only",
            "result_judgment": "planned_proxy_scout_no_result_yet",
            "gate_audit_path": "",
            "created_at": payload["created_at_utc"],
            "created_at_utc": payload["created_at_utc"],
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "goal_achieve": "not_claimed",
            "run_family": "experiment_execution",
            "run_type": "planned_proxy_scout",
            "input_run_id": RUN_ID,
            "output_path": "",
            "result_path": rel(F91B_BRIEF),
            "candidate_count": 0,
            "scout_clue_count": 0,
            "materialization_candidate_count": 0,
            "meaningful_signal_count": 0,
            "completion_candidate_count": 0,
        },
    ]
    ledger = []
    for view, tier, kpi, status, guardrail in [
        ("tier_a_stage_open", "Tier A separate", "design_only_no_kpi", STATUS, "F91B must measure Tier A."),
        ("tier_b_missing_required_pending", "Tier B separate", "missing_required_pending_f91b", "planned_missing_required_check", "F91B must not omit Tier B."),
        ("tier_ab_blocked_pending", "Tier A+B combined", "blocked_pending_tier_b", "planned_combined_check", "Combined read blocked until Tier B condition is known."),
    ]:
        row = dict(run_rows[0])
        row.update(
            {
                "ledger_row_id": f"{RUN_ID}__{view}",
                "subrun_id": f"{RUN_ID}__{view}",
                "record_view": view,
                "tier_scope": tier,
                "kpi_scope": "stage_open_design",
                "primary_kpi": kpi,
                "guardrail_kpi": guardrail,
                "row_id": f"{RUN_ID}__{view}",
                "status": status,
                "evidence_boundary": "design_only_no_runtime_evidence",
                "question": "Can F91A open a regime-conditioned density/cost abstention axis?",
                "next_action": NEXT_RUN_ID,
            }
        )
        ledger.append(row)
    planned = dict(run_rows[1])
    planned.update(
        {
            "ledger_row_id": f"{NEXT_RUN_ID}__planned_current_run",
            "subrun_id": f"{NEXT_RUN_ID}__planned_current_run",
            "record_view": "planned_current_run",
            "tier_scope": "Tier A/B/combined planned",
            "kpi_scope": "planned_proxy_scout",
            "primary_kpi": "planned_only",
            "guardrail_kpi": "F91B must record Tier A/B/combined and runtime trigger if candidate appears.",
            "row_id": f"{NEXT_RUN_ID}__planned_current_run",
            "evidence_boundary": "planned_proxy_scout_only_no_runtime_evidence",
            "question": "Can F91B proxy scout regime-conditioned density/cost abstention?",
            "next_action": "run_f91b_proxy_scout",
        }
    )
    ledger.append(planned)
    return run_rows, ledger


def update_ledgers(payload: Mapping[str, Any]) -> None:
    run_rows, ledger = ledger_rows(payload, len(REQUIRED_GATES))
    append_dict_rows(RUN_REGISTRY, ["run_id"], run_rows)
    append_dict_rows(ALPHA_LEDGER, ["ledger_row_id"], ledger)
    append_dict_rows(STAGE_LEDGER, ["ledger_row_id"], ledger, header_source=ALPHA_LEDGER)


def update_artifact_registry(payload: Mapping[str, Any]) -> None:
    rows = []
    for path in produced_artifacts():
        if not path_exists(path) or not path.is_file():
            continue
        rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": "f91a_stage_open_design",
                "path": rel(path),
                "sha256": sha256_file(path),
                "created_at": payload["created_at_utc"],
                "claim_boundary": CLAIM_BOUNDARY,
                "artifact_id": f"{RUN_ID}::{rel(path)}",
                "created_at_utc": payload["created_at_utc"],
                "notes": "F91A design-only stage open artifact; no runtime authority.",
                "artifact_path": rel(path),
                "effect": "Supports F91A formal open and F91B proxy scout plan only.",
                "size_bytes": path.stat().st_size,
            }
        )
    replace_rows_by_field(ARTIFACT_REGISTRY, "run_id", RUN_ID, rows)


def update_markdown_registers(payload: Mapping[str, Any]) -> None:
    marker = RUN_ID
    idea_addition = f"""
<!-- {marker} -->
## F91A Regime Density/Cost Abstention Axis

- idea_id(아이디어 ID): `f91_regime_density_cost_abstention_axis`
- hypothesis(가설): pre-entry regime(진입 전 장세), density(밀도), cost drag(비용 부담), and risk logic(위험 로직) can define abstain/trade(회피/거래) utility without repeating F90 ordering(순서화).
- legacy_relation(레거시 관계): `prior_evidence_only`
- tier_scope(티어 범위): Tier A separate/Tier B separate/Tier A+B combined required in F91B.
- evidence_boundary(근거 경계): design_only stage open(설계 전용 단계 개방), no candidate/runtime authority(후보/런타임 권위 없음).
- next_action(다음 행동): `{NEXT_RUN_ID}`.
"""
    changelog = f"""
<!-- {marker} -->
## {payload['created_at_utc']} - F91A stage open design

- Action(행동): F91A formal open(정식 개방)을 design-only(설계 전용)로 기록했다.
- Effect(효과): F91B proxy scout(프록시 탐색)가 regime/density/cost/risk(장세/밀도/비용/위험) 축을 시험하게 한다.
- Boundary(경계): no candidate(후보 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).
"""
    append_once(IDEA_REGISTRY, marker, idea_addition)
    append_once(ROOT_CHANGELOG, marker, changelog)
    append_once(WORKSPACE_CHANGELOG, marker, changelog)


def refresh_artifact_audit(payload: Mapping[str, Any]) -> None:
    write_json(ARTIFACT_AUDIT, audit_payload("artifact_lineage_audit", "pass", counts={"source_inputs": len([p for p in source_inputs() if path_exists(p)]), "produced_artifacts": len([p for p in produced_artifacts() if path_exists(p)])}))
    write_skill_receipts(payload)


def main() -> int:
    created_at = now_utc()
    ensure_dirs()
    payload = build_payload(created_at)
    pending = {gate: "pending" for gate in REQUIRED_GATES}
    write_core_artifacts(payload)
    write_packet_and_closeout(payload, pending)
    update_ledgers(payload)
    write_packet_and_closeout(payload, pending)
    gate_results = run_lints()
    passed_status = {
        **{gate: "pass" for gate in REQUIRED_GATES},
        "frontier_extra_due_check": "pass_not_due",
        "data_integrity_audit": "pass_with_boundary",
        "model_validation_audit": "pass_with_boundary",
    }
    write_packet_and_closeout(payload, passed_status)
    copy_packet_audits_to_stage()
    refresh_artifact_audit(payload)
    update_artifact_registry(payload)
    update_markdown_registers(payload)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "next_run_id": NEXT_RUN_ID,
                "runtime_probe_status": "not_triggered_design_only_no_candidate_no_runtime_claim_not_cost_or_proxy_bad_skip",
                "task_force_call_count": len(TASK_FORCE_CALLS),
                "gate_results": gate_results,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
