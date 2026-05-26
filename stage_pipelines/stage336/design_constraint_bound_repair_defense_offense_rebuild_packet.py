from __future__ import annotations

import csv
import json
import math
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import (  # noqa: E402
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)


TODAY = "2026-05-26"
STAGE_ID = "336_onnx_research_packet__constraint_bound_repair_defense_offense_rebuild"
RUN_NUMBER = "run336A"
RUN_ID = "run336A_design_constraint_bound_repair_defense_offense_rebuild_packet_v1"
PARENT_STAGE_ID = "335_overfit_guard__failure_memory_constrained_research_handoff"
PARENT_RUN_ID = "run335S_review_repaired_attribution_proxy_scout_and_open_constraint_bound_research_packet_v1"
NEXT_RUN_ID = "run336B_materialize_constraint_bound_repair_defense_offense_inputs_v1"

STATUS = "completed_constraint_bound_rebuild_packet_design_no_selection"
JUDGMENT = "repair_defense_offense_rebuild_packet_designed_proxy_blocked_no_selection"
DECISION = "stage336A_constraint_bound_rebuild_packet_designed_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage336A_constraint_bound_rebuild_packet_design_no_model_training_"
    "no_threshold_retuning_no_lot_optimization_no_forward_pocket_filtering_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
PARENT_RUN_DIR = ROOT / "stages" / PARENT_STAGE_ID / "02_runs" / "run335S"
PARENT_RUN335R_DIR = ROOT / "stages" / PARENT_STAGE_ID / "02_runs" / "run335R"
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
INPUTS_DIR = STAGE_DIR / "01_inputs"
SPEC_DIR = STAGE_DIR / "00_spec"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"

DOCS = ROOT / "docs"
WORKSPACE_STATE = DOCS / "workspace" / "workspace_state.yaml"
CURRENT_STATE = DOCS / "context" / "current_working_state.md"
CHANGELOG = DOCS / "workspace" / "changelog.md"
RUN_REGISTRY = DOCS / "registers" / "run_registry.csv"
ALPHA_LEDGER = DOCS / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = DOCS / "registers" / "artifact_registry.csv"
DECISION_DOC = DOCS / "decisions" / "2026-05-26_stage336A_constraint_bound_rebuild_packet_design.md"
REPORT_DOC = REVIEWS_DIR / "run336A_constraint_bound_rebuild_packet_design.md"

STAGE336_OPENING_CONTRACT = PARENT_RUN_DIR / "stage336_opening_contract.csv"
RUN336A_DESIGN_QUEUE = PARENT_RUN_DIR / "run336A_design_queue.csv"
CONSTRAINT_REVIEW = PARENT_RUN_DIR / "constraint_packet_review.csv"
PROXY_USABILITY_REVIEW = PARENT_RUN_DIR / "proxy_scout_usability_review.csv"
PROXY_DELTA_REVIEW = PARENT_RUN_DIR / "proxy_expected_vs_mt5_delta_review.csv"
REPAIR_REVIEW = PARENT_RUN_DIR / "same_bar_attribution_repair_review.csv"
PARENT_RUNTIME_PARITY_RECEIPT = PARENT_RUN335R_DIR / "runtime_parity_receipt.json"

BRANCH_DESIGN_CSV = RUN_DIR / "constraint_bound_rebuild_branch_design_matrix.csv"
SCORING_PROXY_CONTRACT_CSV = RUN_DIR / "predeclared_scoring_and_proxy_exclusion_contract.csv"
COST_CURVE_GATE_CSV = RUN_DIR / "cost_curve_direction_gate_contract.csv"
RUNTIME_PARITY_CONTRACT_CSV = RUN_DIR / "runtime_parity_probe_contract.csv"
NEGATIVE_CONTROL_CSV = RUN_DIR / "negative_control_and_stop_condition_matrix.csv"
RUN336B_QUEUE_CSV = RUN_DIR / "run336B_materialization_queue.csv"
GATE_AUDIT_CSV = RUN_DIR / "required_gate_coverage_audit.csv"
RESULT_JUDGMENT_CSV = RUN_DIR / "result_judgment.csv"
FINAL_DECISION_JSON = RUN_DIR / "final_constraint_bound_rebuild_packet_design_decision.json"
RUN_MANIFEST_JSON = RUN_DIR / "run_manifest.json"


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return item.as_posix()


def json_ready(value: Any) -> Any:
    if isinstance(value, Path):
        return rel(value)
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    if isinstance(value, float):
        return "" if not math.isfinite(value) else f"{value:.12g}"
    return str(value)


def as_float(value: Any, default: float = math.nan) -> float:
    try:
        text = str(value).strip()
        if not text:
            return default
        number = float(text)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        raise FileNotFoundError(path)
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column, "")) for column in columns})
    return path


def write_json(path: Path, payload: Any) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def write_md(path: Path, text: str) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.strip() + "\n", encoding="utf-8-sig", newline="\n")
    return path


def read_text_lossless(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    return raw.decode("utf-8-sig"), raw.startswith(b"\xef\xbb\xbf")


def write_text_lossless(path: Path, text: str, had_bom: bool) -> None:
    io_path(path).write_text(text, encoding="utf-8-sig" if had_bom else "utf-8", newline="\n")


def replace_line(text: str, prefix: str, new_line: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = new_line
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + new_line + "\n"


def insert_after_once(text: str, anchor: str, marker: str, body: str) -> str:
    if marker in text:
        return text
    index = text.find(anchor)
    if index == -1:
        return text.rstrip() + "\n" + body.strip() + "\n"
    insertion = index + len(anchor)
    return text[:insertion] + body + text[insertion:]


def append_once(path: Path, header: str, body: str) -> None:
    text, had_bom = read_text_lossless(path)
    if header in text:
        return
    write_text_lossless(path, text.rstrip() + "\n\n" + header + "\n\n" + body.strip() + "\n", had_bom)


def load_inputs() -> dict[str, list[dict[str, str]]]:
    return {
        "opening_contract": read_csv(STAGE336_OPENING_CONTRACT),
        "design_queue": read_csv(RUN336A_DESIGN_QUEUE),
        "constraints": read_csv(CONSTRAINT_REVIEW),
        "proxy_usability": read_csv(PROXY_USABILITY_REVIEW),
        "proxy_delta": read_csv(PROXY_DELTA_REVIEW),
        "repair_review": read_csv(REPAIR_REVIEW),
    }


def constraint_ids(rows: Sequence[Mapping[str, Any]]) -> list[str]:
    return [str(row.get("constraint_id", "")).strip() for row in rows if str(row.get("constraint_id", "")).strip()]


def build_branch_design(constraints: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    all_constraints = ";".join(constraint_ids(constraints))
    return [
        {
            "branch_id": "repair_proxy_exclusion_handoff_contract",
            "lane": "repair",
            "branch_role": "fix handoff and proxy boundary before any score work",
            "source_constraints": "predeclare_exact_join_repair_gate;predeclare_proxy_selection_block",
            "seed_or_clue": "same_bar_attribution_repair_reviewed;old_proxy_rejected",
            "materialization_action": "build repaired attribution identity manifest and proxy-null rank schema",
            "required_outputs": "same_bar_repair_identity;proxy_exclusion_manifest;branch_metric_schema",
            "required_gates": all_constraints,
            "negative_controls": "future_shift_join_canary;old_proxy_rank_canary",
            "stop_conditions": "any_trade_timestamp_mutation;any_old_proxy_rank_use",
            "runtime_requirement": "no MT5 authority claim; future runtime probe must include telemetry/report identity",
            "selection_eligible": "false",
            "next_run_use": "run336B_materialization_input",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "branch_id": "defense_cost_curve_underwater_gate",
            "lane": "defense",
            "branch_role": "make cost and curve fragility mandatory before branch comparison",
            "source_constraints": "predeclare_cost_buffer_gate;predeclare_curve_underwater_gate",
            "seed_or_clue": "cost_fragility;underwater_stretch",
            "materialization_action": "prebuild cost+0.25/0.5/1/2 and rolling5/10/20/50 pocket templates",
            "required_outputs": "cost_stress_matrix;rolling_pocket_matrix;underwater_stretch_report",
            "required_gates": all_constraints,
            "negative_controls": "zero_cost_only_canary;forward_pocket_filter_canary",
            "stop_conditions": "cost_plus_2_failure_hidden;calendar_pocket_direct_filter_detected",
            "runtime_requirement": "future MT5 report must expose trade list and equity curve source",
            "selection_eligible": "false",
            "next_run_use": "run336B_materialization_input",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "branch_id": "defense_direction_symmetry_negative_control",
            "lane": "defense",
            "branch_role": "prevent side cherry-pick after observed long/short asymmetry",
            "source_constraints": "predeclare_direction_symmetry_gate",
            "seed_or_clue": "direction_asymmetry_without_side_routing_authority",
            "materialization_action": "require long/short attribution before side routing or side exclusion is considered",
            "required_outputs": "long_short_attribution;side_specific_failure_memory;side_drop_rejection_note",
            "required_gates": all_constraints,
            "negative_controls": "drop_shorts_after_loss_canary;direction_label_flip_canary",
            "stop_conditions": "side_removed_without_predeclared_failure;side_rule_changed_after_result",
            "runtime_requirement": "future probe must report long/short counts, PnL, DD, expectancy separately",
            "selection_eligible": "false",
            "next_run_use": "run336B_materialization_input",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "branch_id": "offense_m48_plain_density_quality_seed",
            "lane": "offense",
            "branch_role": "use m48_plain as clue only, not a candidate",
            "source_constraints": "predeclare_best_clue_seed_boundary;predeclare_proxy_selection_block",
            "seed_or_clue": "m48_plain_rf_best_research_clue",
            "materialization_action": "turn best clue into feature-family and trade-density questions with independent validation requirements",
            "required_outputs": "feature_family_seed_card;trade_density_target;independent_validation_contract",
            "required_gates": all_constraints,
            "negative_controls": "promote_m48_plain_canary;copy_runtime_result_canary",
            "stop_conditions": "m48_plain_promoted;run335R_profit_reused_as_selection_score",
            "runtime_requirement": "future branch must have fresh MT5 probe or explicit blocked evidence",
            "selection_eligible": "false",
            "next_run_use": "run336B_materialization_input",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "branch_id": "offense_cost_buffer_feature_interaction_seed",
            "lane": "offense",
            "branch_role": "search for robust edge sources that survive costs without tuning to the forward pocket",
            "source_constraints": "predeclare_cost_buffer_gate;predeclare_curve_underwater_gate;predeclare_direction_symmetry_gate",
            "seed_or_clue": "cost_buffer_feature_interaction",
            "materialization_action": "predeclare interaction families across volatility, ADX, VIX, USD, rate and session regimes",
            "required_outputs": "interaction_family_matrix;regime_slice_plan;cost_survival_acceptance",
            "required_gates": all_constraints,
            "negative_controls": "single_regime_overfit_canary;after_result_feature_pick_canary",
            "stop_conditions": "one_regime_only_profit_source;feature_family_selected_after_seeing_forward_result",
            "runtime_requirement": "future MT5 probe must publish regime and session/hour slices",
            "selection_eligible": "false",
            "next_run_use": "run336B_materialization_input",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "branch_id": "runtime_parity_probe_bridge_contract",
            "lane": "runtime",
            "branch_role": "force Python/ONNX/MT5 identity before runtime claims",
            "source_constraints": all_constraints,
            "seed_or_clue": "run335K_run335N_runtime_parity_lessons",
            "materialization_action": "predeclare feature order, bundle hash, report, telemetry, and row-level parity requirements",
            "required_outputs": "runtime_handoff_manifest;row_level_parity_schema;external_verification_status",
            "required_gates": all_constraints,
            "negative_controls": "compile_only_authority_canary;entrypoint_copy_canary",
            "stop_conditions": "runtime_authority_without_tester_output;missing_telemetry_identity",
            "runtime_requirement": "MT5 tester output and telemetry are required for any future runtime_probe claim",
            "selection_eligible": "false",
            "next_run_use": "run336B_materialization_input",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_proxy_contract(proxy_rows: Sequence[Mapping[str, str]], proxy_delta_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    delta_by_dimension = {str(row.get("dimension")): row for row in proxy_delta_rows}
    rows: list[dict[str, Any]] = []
    for item in proxy_rows:
        dimension = str(item.get("dimension"))
        delta = delta_by_dimension.get(dimension, {})
        rows.append(
            {
                "contract_id": f"proxy_exclusion_{dimension}",
                "dimension": dimension,
                "rank_use": "blocked",
                "forward_decision_use": "blocked",
                "diagnostic_use": "allowed_with_boundary",
                "old_proxy_block_reason": item.get("old_proxy_block_reason", "repeated_aggregate_context_only_not_branch_specific"),
                "old_proxy_unique_values": delta.get("old_proxy_unique_values", ""),
                "mt5_runtime_unique_values": delta.get("mt5_runtime_unique_values", ""),
                "mean_abs_delta_vs_mt5": delta.get("old_proxy_mean_abs_delta_vs_mt5", ""),
                "required_rebuild_grain": "branch;attempt;bar;trade",
                "acceptance_evidence": "fresh branch-grain metric plus MT5 comparison before rank use",
                "forbidden_use": "retrofit_proxy_to_mt5_profit;selection_use_before_review;Forward_decision_from_proxy",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    rows.append(
        {
            "contract_id": "score_input_allowlist",
            "dimension": "overall_scoring",
            "rank_use": "allowed_only_after_run336B_contract_materialization",
            "forward_decision_use": "blocked_until_fresh_MT5_probe",
            "diagnostic_use": "allowed_with_boundary",
            "old_proxy_block_reason": "old_proxy_expected_values_not_selection_usable",
            "old_proxy_unique_values": "",
            "mt5_runtime_unique_values": "",
            "mean_abs_delta_vs_mt5": "",
            "required_rebuild_grain": "predeclared non-forward-pocket feature family;Tier A and Tier B records;runtime identity",
            "acceptance_evidence": "future run must publish scoring feature list before seeing forward result",
            "forbidden_use": "threshold_retune;lot_optimization;calendar_forward_pocket_filter",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )
    return rows


def build_gate_contract() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "cost_buffer_gate",
            "scope": "all_future_branches",
            "required_measurement": "cost_plus_0_25;cost_plus_0_5;cost_plus_1_0;cost_plus_2_0",
            "acceptance_boundary": "report full stress curve before any comparison; do not tune spread/slippage after result",
            "failure_memory_trigger": "profit survives only at zero or tiny cost",
            "forbidden_shortcut": "ignore_cost_stress;change_lot_to_hide_cost",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "curve_pocket_gate",
            "scope": "all_future_branches",
            "required_measurement": "rolling5;rolling10;rolling20;rolling50 worst pocket",
            "acceptance_boundary": "report curve pocket before selection; direct calendar pocket filter is forbidden",
            "failure_memory_trigger": "one pocket dominates net/PF or breaks recovery",
            "forbidden_shortcut": "drop_forward_calendar_dates",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "underwater_stretch_gate",
            "scope": "all_future_branches",
            "required_measurement": "max underwater stretch;recovery factor;drawdown duration",
            "acceptance_boundary": "underwater stretch must be named with net/PF, not hidden behind headline profit",
            "failure_memory_trigger": "long unrecovered pocket or recovery collapse",
            "forbidden_shortcut": "read_profit_without_drawdown_duration",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "direction_attribution_gate",
            "scope": "all_future_branches",
            "required_measurement": "long count;short count;long PnL;short PnL;side DD;side expectancy",
            "acceptance_boundary": "side routing change requires predeclared side-specific failure evidence",
            "failure_memory_trigger": "one side carries loss while total is masked",
            "forbidden_shortcut": "drop_losing_side_after_result",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "regime_slice_gate",
            "scope": "all_future_branches",
            "required_measurement": "session;hour;month;volatility;ADX;VIX;USD;rate regime slices",
            "acceptance_boundary": "slices explain behavior but cannot be direct forward pocket filters",
            "failure_memory_trigger": "single slice explains most profit or loss",
            "forbidden_shortcut": "pick_profitable_slice_after_result",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "lot_normalized_gate",
            "scope": "all_future_branches",
            "required_measurement": "lot-normalized net;expectancy;DD;cost stress",
            "acceptance_boundary": "lot changes cannot be used as optimization or repair",
            "failure_memory_trigger": "headline profit depends on sizing rather than signal",
            "forbidden_shortcut": "lot_optimization",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_runtime_contract() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "feature_order_identity",
            "runtime_subject": "Python parser to ONNX to MT5 input vector",
            "required_identity": "58 feature order hash and closed-bar timing",
            "required_check": "feature count, order hash, finite input audit, all-or-skip reason codes",
            "acceptance_evidence": "row-level snapshot and hash in future runtime probe",
            "forbidden": "feature_order_change_without_new_artifact;partial_bar_input",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "model_bundle_identity",
            "runtime_subject": "ONNX bundle and adapter package",
            "required_identity": "model hash;adapter hash;threshold/risk/lot config hash",
            "required_check": "Python ONNX inference equals MT5 ONNX output within tolerance",
            "acceptance_evidence": "future parity CSV with probability and decision columns",
            "forbidden": "silent_model_swap;threshold_retuning",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "mt5_report_telemetry_identity",
            "runtime_subject": "Strategy Tester report and terminal file output",
            "required_identity": "report path;telemetry path;tester period;spread;commission;deposit;symbol;timeframe",
            "required_check": "parseable trade list, equity curve, skips/rejects, and settings",
            "acceptance_evidence": "MT5 report and telemetry manifest in future run",
            "forbidden": "runtime_authority_from_compile_only;missing_report_identity",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "row_level_runtime_parity",
            "runtime_subject": "research signal versus MT5 decision",
            "required_identity": "timestamp;decision;probability;direction;skip reason",
            "required_check": "decision mismatch count, max probability diff, terminal flat gap",
            "acceptance_evidence": "row-level parity report before runtime claim",
            "forbidden": "aggregate_only_parity_claim",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "external_verification_status",
            "runtime_subject": "future branch claims requiring MT5",
            "required_identity": "completed;blocked;out_of_scope_by_claim;not_applicable",
            "required_check": "attempt command or exact blocker recorded",
            "acceptance_evidence": "run_manifest external_verification_status field",
            "forbidden": "repeat_missing_external_check_as_reviewed",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_negative_controls() -> list[dict[str, Any]]:
    controls = [
        ("future_shift_join_canary", "lookahead_join", "force any nearest/future timestamp repair to fail", "future or nearest trade key appears", "block run and repair attribution logic"),
        ("old_proxy_rank_canary", "proxy_overfit", "assert old proxy expected values never enter rank or Forward decision", "old proxy column used as score input", "block score packet"),
        ("forward_pocket_filter_canary", "calendar_overfit", "reject direct filter on known forward weak pocket", "calendar pocket becomes branch rule", "move to invalid setup"),
        ("threshold_retune_canary", "threshold_overfit", "record threshold before result and reject changes after result", "threshold changed after forward read", "block candidate read"),
        ("lot_optimization_canary", "sizing_overfit", "keep lot logic fixed unless a separate predeclared sizing stage exists", "lot altered to improve KPI", "block operating claim"),
        ("drop_shorts_after_loss_canary", "side_cherry_pick", "require side failure evidence before any side exclusion", "short side removed after observed loss", "block side routing"),
        ("single_regime_overfit_canary", "regime_cherry_pick", "require all regime slices and a negative-control slice", "only profitable regime retained", "block selection"),
        ("compile_only_authority_canary", "runtime_parity_gap", "reject compile-only runtime authority", "MetaEditor compile used as tester substitute", "block runtime claim"),
        ("zero_cost_only_canary", "cost_fragility", "require nonzero cost stress before positive judgment", "positive only under zero added cost", "mark failure memory"),
        ("after_result_feature_pick_canary", "feature_selection_leakage", "feature families must be declared before forward/runtime result", "feature family chosen after KPI", "block branch"),
    ]
    return [
        {
            "control_id": control_id,
            "target_risk": target_risk,
            "test_design": test_design,
            "expected_failure_signature": expected_failure_signature,
            "stop_condition": stop_condition,
            "applies_to_branches": "all_stage336_future_branches",
            "repair_action": "document failure memory before any retry",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for control_id, target_risk, test_design, expected_failure_signature, stop_condition in controls
    ]


def build_run336b_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "materialize_branch_spec_cards",
            "priority": 1,
            "source_artifact": rel(BRANCH_DESIGN_CSV),
            "task": "Materialize branch spec cards for repair, defense, offense, and runtime lanes.",
            "success_condition": "each branch has source constraints, outputs, controls, and forbidden shortcuts",
            "forbidden": "model_training;candidate_selection;threshold_retuning",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "materialize_proxy_exclusion_inputs",
            "priority": 2,
            "source_artifact": rel(SCORING_PROXY_CONTRACT_CSV),
            "task": "Create score-input allowlist and proxy exclusion manifests.",
            "success_condition": "old proxy expected values are absent from branch scoring inputs",
            "forbidden": "retrofit_proxy_to_mt5_profit;proxy_rank_use",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "materialize_cost_curve_gate_templates",
            "priority": 3,
            "source_artifact": rel(COST_CURVE_GATE_CSV),
            "task": "Build reusable Stage336 gate templates for cost, curve, underwater, side, regime, and lot-normalized reporting.",
            "success_condition": "future branch outputs cannot be reviewed without all gate tables",
            "forbidden": "direct_forward_pocket_filter;lot_optimization",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "materialize_runtime_parity_preflight",
            "priority": 4,
            "source_artifact": rel(RUNTIME_PARITY_CONTRACT_CSV),
            "task": "Create runtime parity preflight schema for future Python/ONNX/MT5 probes.",
            "success_condition": "future runtime probe must include row-level parity and external verification status",
            "forbidden": "runtime_authority_without_tester_output;entrypoint_copy_for_parameter_only_change",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "materialize_negative_control_matrix",
            "priority": 5,
            "source_artifact": rel(NEGATIVE_CONTROL_CSV),
            "task": "Convert canaries and stop conditions into materialized checklists.",
            "success_condition": "lookahead, proxy, threshold, lot, side, regime, and runtime authority canaries are enforceable",
            "forbidden": "skip_negative_control_after_good_kpi",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "materialize_regime_slice_schema",
            "priority": 6,
            "source_artifact": rel(COST_CURVE_GATE_CSV),
            "task": "Predeclare session, hour, month, volatility, ADX, VIX, USD, and rate regime slice output schema.",
            "success_condition": "future branches report all slices without selecting on forward pocket",
            "forbidden": "pick_profitable_slice_after_result",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_gate_audit(metrics: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "stage336_opening_inputs_loaded",
            "status": "passed" if metrics["opening_contract_rows"] == 3 and metrics["design_queue_rows"] == 4 else "failed",
            "evidence": rel(STAGE336_OPENING_CONTRACT),
            "finding": f"opening_contract_rows={metrics['opening_contract_rows']};design_queue_rows={metrics['design_queue_rows']}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "all_six_constraints_wired",
            "status": "passed" if metrics["constraints_accepted"] == 6 else "failed",
            "evidence": rel(CONSTRAINT_REVIEW),
            "finding": f"constraints_accepted={metrics['constraints_accepted']}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "proxy_selection_block_carried_forward",
            "status": "passed" if metrics["proxy_selection_usable_rows"] == 0 else "failed",
            "evidence": rel(SCORING_PROXY_CONTRACT_CSV),
            "finding": f"proxy_dimensions={metrics['proxy_contract_rows']};selection_usable_rows={metrics['proxy_selection_usable_rows']}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "same_bar_repair_boundary_carried_forward",
            "status": "passed" if metrics["repair_remaining_missing"] == 0 and metrics["repair_invalid_rows"] == 0 else "failed",
            "evidence": rel(REPAIR_REVIEW),
            "finding": f"accepted_repair_rows={metrics['accepted_repair_rows']};remaining_missing={metrics['repair_remaining_missing']};invalid_rows={metrics['repair_invalid_rows']}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "repair_defense_offense_runtime_balance",
            "status": "passed" if metrics["branch_rows"] == 6 and metrics["lane_count"] == 4 else "failed",
            "evidence": rel(BRANCH_DESIGN_CSV),
            "finding": f"branch_rows={metrics['branch_rows']};lane_count={metrics['lane_count']}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "runtime_parity_contract_predeclared",
            "status": "passed" if metrics["runtime_contract_rows"] >= 5 else "failed",
            "evidence": rel(RUNTIME_PARITY_CONTRACT_CSV),
            "finding": f"runtime_contract_rows={metrics['runtime_contract_rows']}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "negative_controls_predeclared",
            "status": "passed" if metrics["negative_control_rows"] >= 10 else "failed",
            "evidence": rel(NEGATIVE_CONTROL_CSV),
            "finding": f"negative_control_rows={metrics['negative_control_rows']}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "forbidden_claims_absent",
            "status": "passed",
            "evidence": rel(RESULT_JUDGMENT_CSV),
            "finding": "candidate selection, Forward Passed/Failed, runtime authority, live readiness, deployment, operating promotion, Goal Achieve all not_claimed",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def write_receipts(metrics: Mapping[str, Any]) -> list[Path]:
    receipts = {
        "data_integrity_receipt.json": {
            "run_id": RUN_ID,
            "data_source": [
                rel(STAGE336_OPENING_CONTRACT),
                rel(CONSTRAINT_REVIEW),
                rel(PROXY_USABILITY_REVIEW),
                rel(REPAIR_REVIEW),
            ],
            "time_axis": "MT5 server-time and FPMarkets broker-clock contracts preserved; run336A performs design only and creates no new bar data.",
            "sample_scope": "Stage335S reviewed evidence from post-OOS runtime diagnostic artifacts; no new training, threshold, lot, or forward pocket filtering.",
            "missing_or_duplicate_check": f"same_bar_repair_remaining_missing={metrics['repair_remaining_missing']};design does not create raw rows.",
            "feature_label_boundary": "No feature, label, model, or score computation is performed; future feature families must be declared before forward/runtime read.",
            "split_boundary": "research design only; future validation and MT5 probe must keep Tier A/Tier B records separate.",
            "leakage_risk": "old proxy rank use, direct forward pocket filtering, after-result feature picking, and future timestamp repair are explicitly blocked.",
            "data_hash_or_identity": {
                "stage336_opening_contract": sha256_file_lf_normalized(STAGE336_OPENING_CONTRACT),
                "constraint_review": sha256_file_lf_normalized(CONSTRAINT_REVIEW),
                "proxy_usability_review": sha256_file_lf_normalized(PROXY_USABILITY_REVIEW),
                "repair_review": sha256_file_lf_normalized(REPAIR_REVIEW),
            },
            "integrity_judgment": "usable_with_boundary",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "runtime_parity_receipt.json": {
            "run_id": RUN_ID,
            "research_path": rel(Path(__file__)),
            "runtime_path": [rel(PARENT_RUNTIME_PARITY_RECEIPT), rel(RUNTIME_PARITY_CONTRACT_CSV)],
            "shared_contract": "future branches must preserve feature order, model/bundle identity, threshold/risk/lot identity, MT5 report identity, telemetry identity, and row-level parity.",
            "known_differences": "run336A is a design run and does not execute MT5 or claim runtime authority.",
            "parity_check": "contract predeclared; no new tester output generated in this run.",
            "parity_identity": {
                "parent_run": PARENT_RUN_ID,
                "next_run": NEXT_RUN_ID,
                "runtime_contract_rows": metrics["runtime_contract_rows"],
            },
            "runtime_claim_boundary": "research_only_runtime_contract_no_runtime_authority",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "performance_attribution_receipt.json": {
            "run_id": RUN_ID,
            "observed_change": "Stage335 constraints converted into a balanced repair/defense/offense/runtime rebuild packet design.",
            "comparison_baseline": "run335S stage336 opening contract and accepted six constraints.",
            "likely_drivers": "proxy repeated aggregate risk, cost fragility, curve pocket risk, direction asymmetry, attribution repair boundary, and best clue seed boundary.",
            "segment_checks": "predeclared future checks cover session, hour, month, volatility, ADX, VIX, USD, rate, long/short, cost, underwater, and curve pockets.",
            "trade_shape": "no new trades; trade-shape evidence remains future required output.",
            "alternative_explanations": "design completeness does not prove signal quality or forward robustness.",
            "attribution_confidence": "medium_for_protocol_design_only",
            "next_probe": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "artifact_lineage_receipt.json": {
            "run_id": RUN_ID,
            "source_inputs": [
                rel(PARENT_RUN_DIR),
                rel(PARENT_RUN335R_DIR),
            ],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [
                rel(BRANCH_DESIGN_CSV),
                rel(SCORING_PROXY_CONTRACT_CSV),
                rel(COST_CURVE_GATE_CSV),
                rel(RUNTIME_PARITY_CONTRACT_CSV),
                rel(NEGATIVE_CONTROL_CSV),
                rel(RUN336B_QUEUE_CSV),
            ],
            "artifact_hashes": "registered in docs/registers/artifact_registry.csv after generation",
            "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_generated_run_artifacts",
            "lineage_judgment": "connected_with_boundary",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "result_judgment_receipt.json": {
            "run_id": RUN_ID,
            "result_subject": "Stage336A constraint-bound repair/defense/offense rebuild packet design",
            "evidence_available": "branch design matrix, proxy exclusion contract, gate contract, runtime parity contract, negative controls, run336B queue",
            "evidence_missing": "new model training, future MT5 runtime probe, selected candidate, Forward Passed/Failed evidence, live readiness evidence",
            "judgment_label": "exploratory",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "이번 실행은 다음 연구가 밟으면 안 되는 길을 잠그고, 필요한 탐침 입력을 만든 설계 완료다.",
        },
    }
    return [write_json(RUN_DIR / name, payload) for name, payload in receipts.items()]


def write_reports(metrics: Mapping[str, Any]) -> list[Path]:
    report = f"""
# Stage336A Constraint-Bound Rebuild Packet Design(336A단계 제약 기반 재구성 묶음 설계)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- parent_run(부모 실행): `{PARENT_RUN_ID}`
- next_action(다음 행동): `{NEXT_RUN_ID}`

## What Changed(변경 내용)

Stage335S(335S 실행)의 accepted constraints(승인 제약) `{metrics['constraints_accepted']}`개를 Stage336(336단계) 연구 설계로 배선했다.
효과(effect, 효과)는 다음 실행이 model training(모델 학습), threshold retuning(임계값 재조정), lot optimization(로트 최적화), direct forward pocket filtering(직접 전진 포켓 필터링)을 먼저 하지 못하게 하는 것이다.

## Designed Outputs(설계 산출물)

- branch design(분기 설계): `{metrics['branch_rows']}` rows(행)
- proxy exclusion contract(프록시 차단 계약): `{metrics['proxy_contract_rows']}` rows(행)
- cost/curve/direction gate(비용/곡선/방향 게이트): `{metrics['gate_contract_rows']}` rows(행)
- runtime parity contract(런타임 동등성 계약): `{metrics['runtime_contract_rows']}` rows(행)
- negative controls(부정 대조): `{metrics['negative_control_rows']}` rows(행)
- run336B queue(336B 대기열): `{metrics['run336b_queue_rows']}` rows(행)

## Judgment(판정)

This is exploratory design(탐색 설계) only. Proxy(프록시)는 selection(선택)과 Forward decision(전진 판정)에 계속 blocked(차단)이다.
Forward Passed(전진 통과), Forward Failed(전진 실패), runtime authority(런타임 권위), live readiness(실거래 준비), deployment(배포), Goal Achieve(목표 달성)는 주장하지 않는다.

## Next(다음)

`{NEXT_RUN_ID}`에서 이 설계를 실제 materialization inputs(물질화 입력)로 바꾼다.
"""
    decision_doc = f"""
# Stage336A Decision(336A단계 결정): Constraint-Bound Rebuild Packet Design(제약 기반 재구성 묶음 설계)

- decision(결정): `{DECISION}`
- result_subject(판정 대상): Stage336A constraint-bound repair/defense/offense rebuild packet design(제약 기반 수리/방어/공격 재구성 묶음 설계)
- evidence_available(사용 근거): branch design(분기 설계), proxy exclusion contract(프록시 차단 계약), gate contract(게이트 계약), runtime parity contract(런타임 동등성 계약), negative control matrix(부정 대조 행렬)
- evidence_missing(부족 근거): model training(모델 학습), MT5 runtime probe(MT5 런타임 탐침), selected candidate(선택 후보), Forward Passed/Failed(전진 통과/실패)
- judgment_label(판정 라벨): `exploratory`
- next_condition(다음 조건): `{NEXT_RUN_ID}`

효과(effect, 효과): Stage336A(336A 실행)는 좋은 ONNX(온엑스)를 골랐다고 말하지 않는다. 대신 다음 연구가 과적합(overfit, 과적합), proxy misuse(프록시 오용), runtime parity gap(런타임 동등성 공백)을 다시 만들지 못하도록 사전 계약을 만든다.

Boundary(경계): `{CLAIM_BOUNDARY}`
"""
    return [write_md(REPORT_DOC, report), write_md(DECISION_DOC, decision_doc)]


def update_docs(metrics: Mapping[str, Any]) -> None:
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_line(workspace_text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    workspace_text = replace_line(workspace_text, "updated_on:", f"updated_on: '{TODAY}'")
    focus_body = (
        "  Stage336(336단계) run336A(336A 실행)는 "
        f"`{STATUS}`로 constraint-bound rebuild packet design(제약 기반 재구성 묶음 설계)을 완료했다. "
        f"Effect(효과): constraints(제약) `{metrics['constraints_accepted']}`개, branch design(분기 설계) `{metrics['branch_rows']}`개, "
        f"negative controls(부정 대조) `{metrics['negative_control_rows']}`개를 만들고 `{NEXT_RUN_ID}`로 넘긴다. "
        "Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    workspace_text = insert_after_once(
        workspace_text,
        "current_focus:\n",
        "run336A(336A 실행)",
        f"- >-\n{focus_body}\n",
    )
    write_text_lossless(WORKSPACE_STATE, workspace_text.rstrip() + "\n", workspace_bom)

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    current_text = replace_line(current_text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    current_text = replace_line(current_text, "- status(상태):", f"- status(상태): `{STATUS}`")
    current_text = replace_line(current_text, "- decision(결정):", f"- decision(결정): `{DECISION}`")
    run_summary = (
        f"- run336A_summary(336A 요약): constraint-bound rebuild packet design(제약 기반 재구성 묶음 설계)을 "
        f"`{STATUS}`로 완료했다. Effect(효과): branch design(분기 설계) `{metrics['branch_rows']}`개, "
        f"proxy exclusion contract(프록시 차단 계약) `{metrics['proxy_contract_rows']}`행, "
        f"runtime parity contract(런타임 동등성 계약) `{metrics['runtime_contract_rows']}`행을 만들고 `{NEXT_RUN_ID}`로 넘긴다. "
        "Forward Passed/Failed(전진 통과/실패)와 Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    current_text = insert_after_once(
        current_text,
        f"- decision(결정): `{DECISION}`\n",
        "run336A_summary(336A 요약)",
        run_summary,
    )
    write_text_lossless(CURRENT_STATE, current_text.rstrip() + "\n", current_bom)

    selection_path = SELECTED_DIR / "selection_status.md"
    selection_text, selection_bom = read_text_lossless(selection_path)
    selection_text = replace_line(selection_text, "- latest_design(최신 설계):", f"- latest_design(최신 설계): `{RUN_ID}`")
    selection_text = replace_line(selection_text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    selection_text = replace_line(selection_text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_RUN_ID}`")
    selection_text = replace_line(selection_text, "- latest_review(최신 검토):", f"- latest_review(최신 검토): `{RUN_ID}`")
    selection_text = replace_line(
        selection_text,
        "- effect(효과):",
        "- effect(효과): Stage336(336단계)는 run336A(336A 실행) 설계를 통해 수리/방어/공격/런타임 계약을 물질화 대기열로 넘겼으며 후보 선택이나 운영 주장은 없다.",
    )
    write_text_lossless(selection_path, selection_text.rstrip() + "\n", selection_bom)

    brief_path = SPEC_DIR / "stage_brief.md"
    brief_text, brief_bom = read_text_lossless(brief_path)
    brief_text = replace_line(brief_text, "- latest_run(최신 실행):", f"- latest_run(최신 실행): `{RUN_ID}`")
    write_text_lossless(brief_path, brief_text.rstrip() + "\n", brief_bom)

    input_refs_path = INPUTS_DIR / "input_refs.md"
    input_refs_text, input_refs_bom = read_text_lossless(input_refs_path)
    section = f"""

## run336A Outputs(336A 산출물)

- branch_design(분기 설계): `{rel(BRANCH_DESIGN_CSV)}`
- proxy_exclusion_contract(프록시 차단 계약): `{rel(SCORING_PROXY_CONTRACT_CSV)}`
- cost_curve_direction_gate_contract(비용/곡선/방향 게이트 계약): `{rel(COST_CURVE_GATE_CSV)}`
- runtime_parity_probe_contract(런타임 동등성 탐침 계약): `{rel(RUNTIME_PARITY_CONTRACT_CSV)}`
- negative_control_matrix(부정 대조 행렬): `{rel(NEGATIVE_CONTROL_CSV)}`
- run336B_queue(336B 대기열): `{rel(RUN336B_QUEUE_CSV)}`
"""
    input_refs_text = insert_after_once(
        input_refs_text,
        "- run336A_design_queue(336A 설계 대기열): `stages/335_overfit_guard__failure_memory_constrained_research_handoff/02_runs/run335S/run336A_design_queue.csv`\n",
        "run336A Outputs(336A 산출물)",
        section,
    )
    write_text_lossless(input_refs_path, input_refs_text.rstrip() + "\n", input_refs_bom)

    append_once(
        CHANGELOG,
        "## 2026-05-26 Stage336A Constraint-Bound Rebuild Packet Design(336A 제약 기반 재구성 묶음 설계)",
        f"""
- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- effect(효과): constraints(제약) `{metrics['constraints_accepted']}`개를 repair/defense/offense/runtime(수리/방어/공격/런타임) 설계와 negative control(부정 대조)로 배선했다.
- boundary(경계): Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 `not_claimed`.
""",
    )


def update_registers(outputs: Sequence[Path], metrics: Mapping[str, Any]) -> None:
    run_registry_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "stage336_constraint_bound_rebuild_packet_design",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_DOC),
        "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};branch_rows={metrics['branch_rows']};goal_achieve_not_claimed.",
    }
    upsert_csv_rows(RUN_REGISTRY, RUN_REGISTRY_COLUMNS, [run_registry_row], key="run_id")

    alpha_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__design_packet",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": RUN_NUMBER,
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "constraint_bound_rebuild_packet_design",
            "tier_scope": "paired_tier_required_by_future_contract",
            "kpi_scope": "design_only_no_new_trading_kpi",
            "scoreboard_lane": "experiment_design",
            "status": STATUS,
            "judgment": JUDGMENT,
            "path": rel(REPORT_DOC),
            "primary_kpi": f"branch_rows={metrics['branch_rows']};constraints_accepted={metrics['constraints_accepted']}",
            "guardrail_kpi": f"negative_controls={metrics['negative_control_rows']};proxy_selection_usable_rows={metrics['proxy_selection_usable_rows']}",
            "external_verification_status": "out_of_scope_by_claim_design_only",
            "notes": f"decision={DECISION};next_action={NEXT_RUN_ID}.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__repair_lane_contract",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "repair_lane",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "repair_lane_design",
            "tier_scope": "out_of_scope_by_claim_design_only",
            "kpi_scope": "repair_contract_no_trading_kpi",
            "scoreboard_lane": "repair",
            "status": STATUS,
            "judgment": "repair_proxy_exclusion_contract_designed",
            "path": rel(BRANCH_DESIGN_CSV),
            "primary_kpi": f"accepted_repair_rows={metrics['accepted_repair_rows']}",
            "guardrail_kpi": f"repair_remaining_missing={metrics['repair_remaining_missing']};repair_invalid_rows={metrics['repair_invalid_rows']}",
            "external_verification_status": "out_of_scope_by_claim_design_only",
            "notes": "same_bar_attribution_only;future_or_nearest_shift_blocked.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__defense_offense_runtime_contract",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "defense_offense_runtime",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "defense_offense_runtime_design",
            "tier_scope": "paired_tier_required_by_future_contract",
            "kpi_scope": "gate_contract_no_new_trading_kpi",
            "scoreboard_lane": "defense_offense_runtime",
            "status": STATUS,
            "judgment": "cost_curve_direction_runtime_controls_predeclared",
            "path": rel(COST_CURVE_GATE_CSV),
            "primary_kpi": f"gate_contract_rows={metrics['gate_contract_rows']};runtime_contract_rows={metrics['runtime_contract_rows']}",
            "guardrail_kpi": f"forbidden_claims_absent=true;negative_controls={metrics['negative_control_rows']}",
            "external_verification_status": "out_of_scope_by_claim_design_only",
            "notes": "no_model_training;no_threshold_retuning;no_lot_optimization;no_goal_achieve.",
        },
    ]
    upsert_csv_rows(ALPHA_LEDGER, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")

    stage_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__constraint_bound_rebuild_packet_design",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "work_family": "constraint_bound_repair_defense_offense_rebuild_design",
            "evidence_scope": "stage335S_constraints_proxy_repair_review_to_stage336_design",
            "kpi_scope": "design_only_no_new_trading_kpi",
            "status": STATUS,
            "judgment": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "path": rel(REPORT_DOC),
            "notes": f"branch_rows={metrics['branch_rows']};negative_controls={metrics['negative_control_rows']};next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
            "decision": DECISION,
        }
    ]
    upsert_csv_rows(
        STAGE_LEDGER,
        (
            "ledger_row_id",
            "stage_id",
            "run_id",
            "work_family",
            "evidence_scope",
            "kpi_scope",
            "status",
            "judgment",
            "claim_boundary",
            "path",
            "notes",
            "decision",
        ),
        stage_rows,
        key="ledger_row_id",
    )

    artifact_rows = []
    created = now_utc()
    for path in outputs:
        if not path_exists(path):
            continue
        artifact_rows.append(
            {
                "artifact_id": f"{RUN_ID}__{path.stem}",
                "artifact_type": "stage336A_constraint_bound_rebuild_design",
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created,
                "notes": "run336A_design_no_selection_no_forward_decision",
            }
        )
    upsert_csv_rows(
        ARTIFACT_REGISTRY,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
        artifact_rows,
        key="artifact_id",
    )


def main() -> int:
    inputs = load_inputs()
    branch_rows = build_branch_design(inputs["constraints"])
    proxy_contract_rows = build_proxy_contract(inputs["proxy_usability"], inputs["proxy_delta"])
    gate_contract_rows = build_gate_contract()
    runtime_contract_rows = build_runtime_contract()
    negative_control_rows = build_negative_controls()
    queue_rows = build_run336b_queue()

    accepted_repair_rows = sum(int(as_float(row.get("accepted_same_bar_repair_count"), 0.0)) for row in inputs["repair_review"])
    repair_remaining_missing = sum(
        int(as_float(row.get("remaining_missing_open_or_feature_join_count"), 0.0)) for row in inputs["repair_review"]
    )
    repair_invalid_rows = sum(int(as_float(row.get("invalid_same_bar_repair_count"), 0.0)) for row in inputs["repair_review"])
    proxy_selection_usable_rows = sum(1 for row in inputs["proxy_usability"] if str(row.get("scout_selection_usable", "")).lower() == "true")
    metrics = {
        "opening_contract_rows": len(inputs["opening_contract"]),
        "design_queue_rows": len(inputs["design_queue"]),
        "constraints_accepted": sum(1 for row in inputs["constraints"] if row.get("review_decision") == "accepted_for_stage336_opening"),
        "accepted_repair_rows": accepted_repair_rows,
        "repair_remaining_missing": repair_remaining_missing,
        "repair_invalid_rows": repair_invalid_rows,
        "proxy_selection_usable_rows": proxy_selection_usable_rows,
        "branch_rows": len(branch_rows),
        "lane_count": len({row["lane"] for row in branch_rows}),
        "proxy_contract_rows": len(proxy_contract_rows),
        "gate_contract_rows": len(gate_contract_rows),
        "runtime_contract_rows": len(runtime_contract_rows),
        "negative_control_rows": len(negative_control_rows),
        "run336b_queue_rows": len(queue_rows),
    }
    audit_rows = build_gate_audit(metrics)
    failed_gates = [row["gate_id"] for row in audit_rows if row["status"] != "passed"]
    result_rows = [
        {
            "run_id": RUN_ID,
            "status": STATUS if not failed_gates else "blocked_stage336A_gate_failure",
            "judgment": JUDGMENT if not failed_gates else "stage336A_design_gate_failure_requires_repair",
            "decision": DECISION if not failed_gates else "stage336A_design_blocked_gate_failure",
            "evidence_available": "branch_design;proxy_exclusion_contract;cost_curve_gate_contract;runtime_parity_contract;negative_control_matrix;run336B_queue",
            "evidence_missing": "new model training;MT5 runtime probe;selected candidate;Forward Passed/Failed evidence;live readiness evidence",
            "judgment_label": "exploratory" if not failed_gates else "blocked",
            "forward_passed": "not_claimed",
            "forward_failed": "not_claimed",
            "runtime_authority": "not_claimed",
            "goal_achieve": "not_claimed",
            "next_action": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]

    outputs = [
        write_csv(
            BRANCH_DESIGN_CSV,
            (
                "branch_id",
                "lane",
                "branch_role",
                "source_constraints",
                "seed_or_clue",
                "materialization_action",
                "required_outputs",
                "required_gates",
                "negative_controls",
                "stop_conditions",
                "runtime_requirement",
                "selection_eligible",
                "next_run_use",
                "claim_boundary",
            ),
            branch_rows,
        ),
        write_csv(
            SCORING_PROXY_CONTRACT_CSV,
            (
                "contract_id",
                "dimension",
                "rank_use",
                "forward_decision_use",
                "diagnostic_use",
                "old_proxy_block_reason",
                "old_proxy_unique_values",
                "mt5_runtime_unique_values",
                "mean_abs_delta_vs_mt5",
                "required_rebuild_grain",
                "acceptance_evidence",
                "forbidden_use",
                "claim_boundary",
            ),
            proxy_contract_rows,
        ),
        write_csv(
            COST_CURVE_GATE_CSV,
            (
                "gate_id",
                "scope",
                "required_measurement",
                "acceptance_boundary",
                "failure_memory_trigger",
                "forbidden_shortcut",
                "claim_boundary",
            ),
            gate_contract_rows,
        ),
        write_csv(
            RUNTIME_PARITY_CONTRACT_CSV,
            (
                "contract_id",
                "runtime_subject",
                "required_identity",
                "required_check",
                "acceptance_evidence",
                "forbidden",
                "claim_boundary",
            ),
            runtime_contract_rows,
        ),
        write_csv(
            NEGATIVE_CONTROL_CSV,
            (
                "control_id",
                "target_risk",
                "test_design",
                "expected_failure_signature",
                "stop_condition",
                "applies_to_branches",
                "repair_action",
                "claim_boundary",
            ),
            negative_control_rows,
        ),
        write_csv(
            RUN336B_QUEUE_CSV,
            ("queue_id", "priority", "source_artifact", "task", "success_condition", "forbidden", "claim_boundary"),
            queue_rows,
        ),
        write_csv(GATE_AUDIT_CSV, ("gate_id", "status", "evidence", "finding", "claim_boundary"), audit_rows),
        write_csv(
            RESULT_JUDGMENT_CSV,
            (
                "run_id",
                "status",
                "judgment",
                "decision",
                "evidence_available",
                "evidence_missing",
                "judgment_label",
                "forward_passed",
                "forward_failed",
                "runtime_authority",
                "goal_achieve",
                "next_action",
                "claim_boundary",
            ),
            result_rows,
        ),
        write_json(
            FINAL_DECISION_JSON,
            {
                "run_id": RUN_ID,
                "parent_run_id": PARENT_RUN_ID,
                "status": STATUS if not failed_gates else "blocked_stage336A_gate_failure",
                "judgment": JUDGMENT if not failed_gates else "stage336A_design_gate_failure_requires_repair",
                "decision": DECISION if not failed_gates else "stage336A_design_blocked_gate_failure",
                "metrics": metrics,
                "failed_gates": failed_gates,
                "next_action": NEXT_RUN_ID,
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "runtime_authority": "not_claimed",
                "goal_achieve": "not_claimed",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RUN_MANIFEST_JSON,
            {
                "run_id": RUN_ID,
                "run_number": RUN_NUMBER,
                "stage_id": STAGE_ID,
                "parent_run_id": PARENT_RUN_ID,
                "created_at_utc": now_utc(),
                "producer": rel(Path(__file__)),
                "source_inputs": [
                    rel(STAGE336_OPENING_CONTRACT),
                    rel(RUN336A_DESIGN_QUEUE),
                    rel(CONSTRAINT_REVIEW),
                    rel(PROXY_USABILITY_REVIEW),
                    rel(PROXY_DELTA_REVIEW),
                    rel(REPAIR_REVIEW),
                    rel(PARENT_RUNTIME_PARITY_RECEIPT),
                ],
                "outputs": [
                    rel(BRANCH_DESIGN_CSV),
                    rel(SCORING_PROXY_CONTRACT_CSV),
                    rel(COST_CURVE_GATE_CSV),
                    rel(RUNTIME_PARITY_CONTRACT_CSV),
                    rel(NEGATIVE_CONTROL_CSV),
                    rel(RUN336B_QUEUE_CSV),
                    rel(GATE_AUDIT_CSV),
                    rel(RESULT_JUDGMENT_CSV),
                    rel(FINAL_DECISION_JSON),
                ],
                "status": STATUS if not failed_gates else "blocked_stage336A_gate_failure",
                "decision": DECISION if not failed_gates else "stage336A_design_blocked_gate_failure",
                "external_verification_status": "out_of_scope_by_claim_design_only",
                "next_action": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
    ]
    outputs.extend(write_receipts(metrics))
    outputs.extend(write_reports(metrics))
    if failed_gates:
        print(json.dumps({"run_id": RUN_ID, "failed_gates": failed_gates}, ensure_ascii=False, indent=2))
        return 2

    update_docs(metrics)
    outputs.extend(
        [
            WORKSPACE_STATE,
            CURRENT_STATE,
            CHANGELOG,
            SELECTED_DIR / "selection_status.md",
            SPEC_DIR / "stage_brief.md",
            INPUTS_DIR / "input_refs.md",
        ]
    )
    update_registers(outputs, metrics)
    outputs.extend([RUN_REGISTRY, ALPHA_LEDGER, STAGE_LEDGER, ARTIFACT_REGISTRY])
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "decision": DECISION,
                "constraints_accepted": metrics["constraints_accepted"],
                "branch_rows": metrics["branch_rows"],
                "proxy_selection_usable_rows": metrics["proxy_selection_usable_rows"],
                "negative_control_rows": metrics["negative_control_rows"],
                "next_action": NEXT_RUN_ID,
                "forward_passed": "not_claimed",
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
