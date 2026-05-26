from __future__ import annotations

import csv
import json
import math
import sys
from collections import Counter
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


TODAY = "2026-05-27"
STAGE_ID = "336_onnx_research_packet__constraint_bound_repair_defense_offense_rebuild"
RUN_NUMBER = "run336F"
RUN_ID = "run336F_materialize_constraint_bound_execution_blueprints_v1"
PARENT_RUN_ID = "run336E_review_constraint_bound_research_implementation_protocols_v1"
NEXT_RUN_ID = "run336G_review_constraint_bound_execution_blueprints_v1"

STATUS = "completed_constraint_bound_execution_blueprints_materialized_no_selection"
JUDGMENT = "materialized_execution_blueprints_no_model_training_no_mt5_execution_no_forward_decision"
DECISION = "stage336F_execution_blueprints_materialized_run336G_review_ready_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage336F_execution_blueprint_materialization_no_model_training_"
    "no_threshold_retuning_no_lot_optimization_no_forward_pocket_filtering_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN336D_DIR = STAGE_DIR / "02_runs" / "run336D"
RUN336E_DIR = STAGE_DIR / "02_runs" / "run336E"
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
SPEC_DIR = STAGE_DIR / "00_spec"
INPUTS_DIR = STAGE_DIR / "01_inputs"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"

DOCS = ROOT / "docs"
WORKSPACE_STATE = DOCS / "workspace" / "workspace_state.yaml"
CURRENT_STATE = DOCS / "context" / "current_working_state.md"
CHANGELOG = DOCS / "workspace" / "changelog.md"
RUN_REGISTRY = DOCS / "registers" / "run_registry.csv"
ALPHA_LEDGER = DOCS / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = DOCS / "registers" / "artifact_registry.csv"
DECISION_DOC = DOCS / "decisions" / "2026-05-27_stage336F_execution_blueprints.md"
REPORT_DOC = REVIEWS_DIR / "run336F_execution_blueprints.md"

RUN336F_QUEUE_CSV = RUN336E_DIR / "run336F_execution_blueprint_queue.csv"
PROTOCOL_ACCEPTANCE_MATRIX_CSV = RUN336E_DIR / "protocol_acceptance_matrix.csv"
BRANCH_CONTROL_REVIEW_CSV = RUN336E_DIR / "branch_specific_negative_control_review.csv"
PROXY_MT5_REVIEW_CSV = RUN336E_DIR / "proxy_mt5_usability_contract_review.csv"
RUNTIME_PREFLIGHT_REVIEW_CSV = RUN336E_DIR / "runtime_preflight_manifest_review.csv"
TIER_NO_LOOKAHEAD_REVIEW_CSV = RUN336E_DIR / "tier_no_lookahead_contract_review.csv"
GATE_REVIEW_CSV = RUN336E_DIR / "gate_execution_plan_review.csv"
REGIME_REVIEW_CSV = RUN336E_DIR / "regime_attribution_plan_review.csv"
READINESS_REVIEW_CSV = RUN336E_DIR / "implementation_readiness_review.csv"

RUN336D_GATE_PLAN_CSV = RUN336D_DIR / "cost_curve_direction_gate_execution_plan.csv"
RUN336D_REGIME_PLAN_CSV = RUN336D_DIR / "regime_attribution_execution_plan.csv"
RUN336D_PROXY_MT5_CONTRACT_CSV = RUN336D_DIR / "proxy_expected_vs_mt5_usability_contract.csv"
RUN336D_RUNTIME_PREFLIGHT_CSV = RUN336D_DIR / "runtime_probe_execution_preflight_manifest.csv"
RUN336D_TIER_CONTRACT_CSV = RUN336D_DIR / "tier_pair_and_no_lookahead_contract.csv"

BLUEPRINT_CATALOG_CSV = RUN_DIR / "execution_blueprint_catalog.csv"
BLUEPRINT_FIELD_CONTRACT_CSV = RUN_DIR / "blueprint_field_contract_matrix.csv"
NEGATIVE_CONTROL_BLUEPRINT_CSV = RUN_DIR / "negative_control_runner_blueprints.csv"
PROXY_MT5_BLUEPRINT_CSV = RUN_DIR / "proxy_mt5_runtime_usability_blueprints.csv"
RUNTIME_IDENTITY_BLUEPRINT_CSV = RUN_DIR / "runtime_identity_blueprints.csv"
GATE_RUNNER_BLUEPRINT_CSV = RUN_DIR / "gate_runner_blueprints.csv"
REGIME_RUNNER_BLUEPRINT_CSV = RUN_DIR / "regime_slice_runner_blueprints.csv"
TIER_NO_LOOKAHEAD_BLUEPRINT_CSV = RUN_DIR / "tier_no_lookahead_runner_blueprints.csv"
OUTPUT_CONTRACT_MATRIX_CSV = RUN_DIR / "blueprint_output_contract_matrix.csv"
RUN336G_REVIEW_QUEUE_CSV = RUN_DIR / "run336G_review_queue.csv"
GATE_AUDIT_CSV = RUN_DIR / "required_gate_coverage_audit.csv"
RESULT_JUDGMENT_CSV = RUN_DIR / "result_judgment.csv"
FINAL_DECISION_JSON = RUN_DIR / "final_execution_blueprint_materialization_decision.json"
RUN_MANIFEST_JSON = RUN_DIR / "run_manifest.json"

REQUIRED_NO_ACTIONS = (
    "model_training",
    "threshold_retuning",
    "lot_optimization",
    "candidate_selection",
    "Forward_Passed",
    "runtime_authority",
    "direct_forward_pocket_filter",
)

BLUEPRINT_FAMILY_BY_NAME = {
    "same_bar_repair_identity_manifest_builder": "repair_identity",
    "proxy_null_rank_validator": "proxy_exclusion",
    "handoff_identity_diff_template": "handoff_identity",
    "cost_stress_runner": "cost_curve",
    "rolling_curve_pocket_runner": "cost_curve",
    "underwater_stretch_runner": "cost_curve",
    "lot_normalized_view_builder": "cost_curve",
    "long_short_attribution_runner": "direction",
    "direction_label_flip_canary_runner": "negative_control",
    "side_drop_rejection_validator": "direction",
    "feature_family_seed_card_builder": "offense_feature",
    "trade_density_target_runner": "offense_feature",
    "m48_clue_promotion_canary_runner": "negative_control",
    "copy_runtime_result_canary_runner": "negative_control",
    "interaction_family_matrix_builder": "offense_feature",
    "regime_slice_runner": "regime",
    "cost_survival_validator": "cost_curve",
    "after_result_feature_pick_canary_runner": "negative_control",
    "runtime_handoff_manifest_builder": "runtime_identity",
    "row_level_parity_schema_builder": "runtime_identity",
    "tester_telemetry_manifest_validator": "runtime_identity",
    "proxy_mt5_diff_table_builder": "proxy_mt5",
    "branch_specific_canary_runner_matrix": "negative_control",
    "negative_control_binding_audit": "negative_control",
    "proxy_expected_table_schema": "proxy_mt5",
    "fresh_mt5_runtime_probe_result_schema": "proxy_mt5",
    "difference_table_schema": "proxy_mt5",
    "usability_decision_template": "proxy_mt5",
    "tier_pair_record_runner": "tier_integrity",
    "future_shift_join_canary_runner": "negative_control",
    "threshold_lot_freeze_manifest_builder": "tier_integrity",
}


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return io_path(item).resolve().relative_to(io_path(ROOT).resolve()).as_posix()
    except ValueError:
        return item.as_posix()


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return "" if not math.isfinite(value) else f"{value:.12g}"
    if isinstance(value, (dict, list, tuple, set)):
        return json.dumps(sorted(value) if isinstance(value, set) else value, ensure_ascii=False, sort_keys=True)
    return str(value)


def split_semicolon(value: Any) -> list[str]:
    return [item.strip() for item in str(value or "").split(";") if item.strip()]


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
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
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


def replace_line(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def append_or_replace_section(path: Path, title: str, body: str) -> None:
    text, had_bom = read_text_lossless(path)
    heading = f"## {title}"
    section = f"{heading}\n\n{body.strip()}\n"
    if heading in text:
        start = text.index(heading)
        next_start = text.find("\n## ", start + len(heading))
        if next_start == -1:
            text = text[:start].rstrip() + "\n\n" + section
        else:
            text = text[:start].rstrip() + "\n\n" + section + text[next_start:]
    else:
        text = text.rstrip() + "\n\n" + section
    write_text_lossless(path, text, had_bom)


def upsert_folded_list_item(text: str, marker: str, folded_body: str, list_header: str = "current_focus:\n") -> str:
    block = f"- >-\n{folded_body}\n"
    marker_index = text.find(marker)
    if marker_index != -1:
        start = text.rfind("- >-\n", 0, marker_index)
        next_start = text.find("\n- >-\n", marker_index)
        if start != -1:
            if next_start == -1:
                return text[:start] + block
            return text[:start] + block + text[next_start + 1 :]
    return text.replace(list_header, list_header + block, 1)


def load_inputs() -> dict[str, list[dict[str, str]]]:
    return {
        "queue": read_csv(RUN336F_QUEUE_CSV),
        "acceptance": read_csv(PROTOCOL_ACCEPTANCE_MATRIX_CSV),
        "branch_controls": read_csv(BRANCH_CONTROL_REVIEW_CSV),
        "proxy_mt5_review": read_csv(PROXY_MT5_REVIEW_CSV),
        "runtime_review": read_csv(RUNTIME_PREFLIGHT_REVIEW_CSV),
        "tier_review": read_csv(TIER_NO_LOOKAHEAD_REVIEW_CSV),
        "gate_review": read_csv(GATE_REVIEW_CSV),
        "regime_review": read_csv(REGIME_REVIEW_CSV),
        "readiness_review": read_csv(READINESS_REVIEW_CSV),
        "gate_plan": read_csv(RUN336D_GATE_PLAN_CSV),
        "regime_plan": read_csv(RUN336D_REGIME_PLAN_CSV),
        "proxy_mt5_contract": read_csv(RUN336D_PROXY_MT5_CONTRACT_CSV),
        "runtime_preflight": read_csv(RUN336D_RUNTIME_PREFLIGHT_CSV),
        "tier_contract": read_csv(RUN336D_TIER_CONTRACT_CSV),
    }


def future_artifact_hint(blueprint_name: str, branch_id: str) -> str:
    return f"stages/{STAGE_ID}/02_runs/run336H/{branch_id}__{blueprint_name}.csv"


def blueprint_purpose(name: str) -> str:
    if "proxy" in name and "mt5" in name:
        return "bind proxy expected values to fresh MT5 result and difference reporting before usability"
    if "proxy" in name:
        return "prevent old proxy or proxy-only evidence from entering rank, selection, or Forward decision"
    if "runtime" in name or "parity" in name or "telemetry" in name or "handoff" in name:
        return "bind Python, ONNX, MT5, report, telemetry, and row-level identity before runtime interpretation"
    if "canary" in name or "negative" in name:
        return "make the named overfit shortcut fail audibly before any positive result can be read"
    if "tier" in name or "future_shift" in name or "threshold_lot" in name:
        return "force paired Tier A, Tier B, actual routed total, no-lookahead, threshold freeze, and lot freeze records"
    if "cost" in name or "curve" in name or "underwater" in name or "lot_normalized" in name:
        return "force cost stress, curve pocket, underwater stretch, and lot-normalized views before comparison"
    if "regime" in name:
        return "keep session, hour, month, volatility, ADX, VIX, USD, and rate slices attribution-only"
    if "direction" in name or "side" in name or "long_short" in name:
        return "force long/short attribution and reject after-result side dropping"
    return "materialize auditable execution blueprint without training or MT5 execution"


def blueprint_inputs(name: str) -> str:
    family = BLUEPRINT_FAMILY_BY_NAME.get(name, "generic")
    if family == "proxy_mt5":
        return "proxy_expected_result_table;fresh_mt5_runtime_probe_result_table;tester_identity;feature_order_hash;model_hash;threshold_hash"
    if family == "runtime_identity":
        return "feature_order_hash;model_bundle_hash;adapter_hash;threshold_risk_lot_hash;MT5_report_path;telemetry_path;row_level_parity_path"
    if family == "negative_control":
        return "source_protocol_id;control_id;mutation_or_canary_plan;expected_failure_signature;stop_condition"
    if family == "cost_curve":
        return "trade_ledger;equity_curve;cost_grid;lot_policy;drawdown_series;branch_id"
    if family == "regime":
        return "trade_ledger;bar_timestamp;session;hour;month;volatility;ADX;VIX;USD;rate"
    if family == "tier_integrity":
        return "Tier_A_record;Tier_B_record;actual_routed_total;closed_bar_timestamp;threshold_manifest;lot_manifest"
    if family == "direction":
        return "trade_ledger;source_signal_direction;MT5_trade_direction;side_bucket;skip_reason"
    if family == "offense_feature":
        return "predeclared_feature_family;source_clue_label;trade_density_target;independent_validation_contract"
    return "source_protocol;branch_id;claim_boundary;forbidden_action_list"


def blueprint_outputs(name: str) -> str:
    family = BLUEPRINT_FAMILY_BY_NAME.get(name, "generic")
    if family == "proxy_mt5":
        return "expected_vs_mt5_difference_rows;usability_label;not_usable_reason;identity_match_flag"
    if family == "runtime_identity":
        return "runtime_identity_manifest;row_level_parity_schema;tester_report_telemetry_manifest;external_verification_status"
    if family == "negative_control":
        return "canary_result;expected_failure_observed;stop_condition_triggered;repair_note"
    if family == "cost_curve":
        return "cost_stress_matrix;curve_pocket_matrix;underwater_stretch_report;lot_normalized_result"
    if family == "regime":
        return "session_hour_month_vol_adx_vix_usd_rate_attribution_table;negative_slice_note"
    if family == "tier_integrity":
        return "Tier_A_separate;Tier_B_separate_or_missing_required;actual_routed_total;future_shift_join_result;threshold_lot_freeze_manifest"
    if family == "direction":
        return "long_short_attribution_table;direction_mismatch_report;side_drop_rejection_note"
    if family == "offense_feature":
        return "feature_family_seed_card;trade_density_target;independent_validation_contract;negative_clue_promotion_note"
    return "blueprint_output_schema;execution_precheck;review_note"


def blueprint_gate(name: str) -> str:
    family = BLUEPRINT_FAMILY_BY_NAME.get(name, "generic")
    return {
        "proxy_mt5": "proxy_expected_result_and_fresh_mt5_difference_required",
        "runtime_identity": "runtime_identity_and_row_level_parity_required",
        "negative_control": "negative_control_must_fail_on_shortcut",
        "cost_curve": "cost_curve_underwater_lot_gate_required",
        "regime": "regime_attribution_only_gate_required",
        "tier_integrity": "tier_no_lookahead_threshold_lot_freeze_required",
        "direction": "direction_attribution_and_side_drop_rejection_required",
        "offense_feature": "feature_family_declared_before_result_required",
        "repair_identity": "same_bar_repair_identity_required",
        "proxy_exclusion": "proxy_null_rank_required",
        "handoff_identity": "handoff_identity_diff_required",
    }.get(family, "manual_review_required")


def build_blueprint_catalog(queue_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for queue in queue_rows:
        for ordinal, name in enumerate(split_semicolon(queue["required_outputs"]), start=1):
            family = BLUEPRINT_FAMILY_BY_NAME.get(name, "generic")
            rows.append(
                {
                    "blueprint_id": f"{queue['branch_id']}__{name}",
                    "queue_id": queue["queue_id"],
                    "branch_id": queue["branch_id"],
                    "lane": queue["lane"],
                    "blueprint_name": name,
                    "blueprint_family": family,
                    "ordinal": ordinal,
                    "purpose": blueprint_purpose(name),
                    "future_artifact_hint": future_artifact_hint(name, queue["branch_id"]),
                    "source_acceptance_artifact": queue["source_acceptance_artifact"],
                    "execution_status": "materialized_blueprint_no_execution",
                    "model_training_allowed": "false",
                    "mt5_execution_allowed": "false",
                    "selection_allowed": "false",
                    "forward_decision_allowed": "false",
                    "forbidden": queue["forbidden"],
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def build_field_contract_rows(catalog_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in catalog_rows:
        name = str(row["blueprint_name"])
        rows.append(
            {
                "blueprint_id": row["blueprint_id"],
                "branch_id": row["branch_id"],
                "blueprint_name": name,
                "required_input_identity": blueprint_inputs(name),
                "required_output_schema": blueprint_outputs(name),
                "required_gate": blueprint_gate(name),
                "failure_condition": "missing_required_input;future_shift_join;after_result_filter;proxy_only_selection;runtime_identity_gap;threshold_or_lot_changed",
                "future_review_requirement": "run336G_must_review_before_any_execution",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_negative_control_blueprints(branch_control_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in branch_control_rows:
        control_id = row["control_id"]
        rows.append(
            {
                "control_id": control_id,
                "branch_id": row["branch_id"],
                "target_risk": row["target_risk"],
                "runner_blueprint": f"{control_id}_runner",
                "mutation_plan": f"inject_or_assert_{control_id}_shortcut_path",
                "expected_failure_signature": "shortcut attempt is detected and branch review is blocked",
                "stop_condition": "block_candidate_selection_forward_decision_and_runtime_claim",
                "source_review_decision": row["review_decision"],
                "future_output": f"stages/{STAGE_ID}/02_runs/run336H/{row['branch_id']}__{control_id}_result.csv",
                "allowed_use": "negative_control_only",
                "forbidden_use": "candidate_selection;Forward_decision;runtime_authority;after_result_repair",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    extra_controls = [
        ("future_shift_join_canary", "cross_branch_data_integrity", "lookahead_leakage"),
        ("threshold_lot_freeze_canary", "cross_branch_data_integrity", "after_result_threshold_or_lot_change"),
        ("old_proxy_rank_canary", "repair_proxy_exclusion_handoff_contract", "old_proxy_selection_leakage"),
        ("direct_forward_pocket_filter_canary", "defense_cost_curve_underwater_gate", "after_result_curve_filtering"),
        ("single_regime_overfit_canary", "offense_cost_buffer_feature_interaction_seed", "single_slice_overfit"),
        ("zero_cost_only_canary", "defense_cost_curve_underwater_gate", "cost_fragility"),
    ]
    for control_id, branch_id, target_risk in extra_controls:
        rows.append(
            {
                "control_id": control_id,
                "branch_id": branch_id,
                "target_risk": target_risk,
                "runner_blueprint": f"{control_id}_runner",
                "mutation_plan": f"force_{control_id}_shortcut_attempt",
                "expected_failure_signature": "canary detects shortcut and forces not_usable_or_repair_queue",
                "stop_condition": "block_positive_or_selection_claim",
                "source_review_decision": "carried_from_stage336D_or_stage336E_contract",
                "future_output": f"stages/{STAGE_ID}/02_runs/run336H/{branch_id}__{control_id}_result.csv",
                "allowed_use": "negative_control_only",
                "forbidden_use": "candidate_selection;Forward_decision;runtime_authority;after_result_repair",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_proxy_mt5_blueprints(contract_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in contract_rows:
        rows.append(
            {
                "contract_id": row["contract_id"],
                "branch_id": row["branch_id"],
                "proxy_expected_schema": row["proxy_expected_columns"],
                "fresh_mt5_result_schema": row["mt5_result_columns"],
                "difference_schema": row["difference_columns"],
                "comparison_key": row["comparison_key"],
                "tolerance_policy": row["predeclared_tolerance"],
                "usable_condition": row["usable_condition"],
                "not_usable_condition": row["not_usable_condition"],
                "future_required_outputs": "proxy_expected_result_table;fresh_mt5_runtime_probe_result_table;proxy_mt5_difference_table;usability_decision_report",
                "selection_use": "blocked",
                "forward_decision_use": "blocked",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_runtime_identity_blueprints(runtime_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in runtime_rows:
        rows.append(
            {
                "preflight_id": row["preflight_id"],
                "branch_id": row["branch_id"],
                "runtime_subject": row["runtime_subject"],
                "required_identity": row["required_identity"],
                "required_check": row["required_check"],
                "acceptance_evidence": row["acceptance_evidence"],
                "future_output_path_requirement": row["future_output_path_requirement"],
                "external_verification_status_required": row["external_verification_status_required"],
                "runtime_claim_boundary": "runtime_probe_only_no_runtime_authority",
                "future_required_outputs": "runtime_handoff_manifest;row_level_parity_schema;tester_report_telemetry_manifest;external_verification_log",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_gate_runner_blueprints(gate_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in gate_rows:
        rows.append(
            {
                "plan_id": row["plan_id"],
                "branch_id": row["branch_id"],
                "gate_id": row["gate_id"],
                "required_measurement": row["required_measurement"],
                "future_output_table_name": row["future_output_table_name"],
                "review_requirement": row["review_requirement"],
                "failure_memory_trigger": row["failure_memory_trigger"],
                "execution_order": row["execution_order"],
                "forbidden_shortcut": row["forbidden_shortcut"],
                "future_runner_blueprint": f"{row['gate_id']}_runner",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_regime_runner_blueprints(regime_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in regime_rows:
        rows.append(
            {
                "plan_id": row["plan_id"],
                "branch_id": row["branch_id"],
                "slice_id": row["slice_id"],
                "output_field": row["output_field"],
                "bucket_policy": row["bucket_policy"],
                "required_metrics": row["required_metrics"],
                "allowed_use": "attribution_and_failure_memory_only",
                "forbidden_use": row["forbidden_use"],
                "future_runner_blueprint": f"{row['slice_id']}_slice_runner",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_tier_blueprints(tier_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in tier_rows:
        rows.append(
            {
                "contract_id": row["contract_id"],
                "tier_scope": row["tier_scope"],
                "required_fields": row["required_fields"],
                "time_axis_rule": row["time_axis_rule"],
                "lookahead_canary": row["lookahead_canary"],
                "acceptance_condition": row["acceptance_condition"],
                "forbidden": row["forbidden"],
                "future_runner_blueprint": f"{row['contract_id']}_runner",
                "future_required_outputs": "tier_pair_record;future_shift_join_canary_result;threshold_lot_freeze_manifest",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    rows.append(
        {
            "contract_id": "threshold_lot_freeze_manifest",
            "tier_scope": "cross_branch_execution_freeze",
            "required_fields": "threshold_hash;risk_logic_hash;lot_logic_hash;ATR_SLTP_hash;runtime_handoff_hash;created_before_result_read",
            "time_axis_rule": "manifest timestamp must precede any future runtime result ingestion",
            "lookahead_canary": "threshold_lot_freeze_canary",
            "acceptance_condition": "all future execution blueprints reference this freeze manifest before result read",
            "forbidden": "threshold_changed_after_forward_read;lot_altered_to_improve_kpi;ATR_exit_changed_after_result",
            "future_runner_blueprint": "threshold_lot_freeze_manifest_builder",
            "future_required_outputs": "threshold_lot_freeze_manifest;freeze_hash_receipt",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )
    return rows


def build_output_contract_matrix(catalog_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in catalog_rows:
        rows.append(
            {
                "blueprint_id": row["blueprint_id"],
                "branch_id": row["branch_id"],
                "blueprint_name": row["blueprint_name"],
                "future_artifact_hint": row["future_artifact_hint"],
                "must_exist_before_execution_review": "true",
                "hash_required": "true",
                "registry_required": "true",
                "can_support_model_training": "false",
                "can_support_forward_decision": "false",
                "can_support_runtime_authority": "false",
                "next_review": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_run336g_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "review_execution_blueprint_catalog",
            "priority": 1,
            "source_artifact": rel(BLUEPRINT_CATALOG_CSV),
            "task": "Verify every run336F queue item has a materialized blueprint row with forbidden actions blocked.",
            "success_condition": "31 blueprint rows exist and all keep training, selection, Forward decision, and runtime authority blocked.",
            "forbidden": "missing_blueprint;model_training_allowed;forward_decision_allowed",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "review_blueprint_field_contracts",
            "priority": 2,
            "source_artifact": rel(BLUEPRINT_FIELD_CONTRACT_CSV),
            "task": "Verify each blueprint names input identity, output schema, gate, and failure condition.",
            "success_condition": "no blueprint can execute without required identities and output schemas.",
            "forbidden": "schema_free_execution;identity_free_runtime_probe",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "review_negative_control_blueprints",
            "priority": 3,
            "source_artifact": rel(NEGATIVE_CONTROL_BLUEPRINT_CSV),
            "task": "Verify branch-specific and cross-branch canaries are runnable or auditable before future result read.",
            "success_condition": "direction, clue promotion, copied result, entrypoint copy, future shift, threshold/lot, proxy rank, and pocket filter canaries are present.",
            "forbidden": "skip_canary_after_good_kpi;after_result_repair",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "review_proxy_mt5_runtime_usability_blueprints",
            "priority": 4,
            "source_artifact": rel(PROXY_MT5_BLUEPRINT_CSV),
            "task": "Verify proxy expected, fresh MT5 result, difference table, and usability template are bound together.",
            "success_condition": "proxy remains diagnostic-only until fresh MT5 row-level or branch-level identity agreement is reviewed.",
            "forbidden": "proxy_only_selection;aggregate_only_runtime_claim",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "review_runtime_identity_blueprints",
            "priority": 5,
            "source_artifact": rel(RUNTIME_IDENTITY_BLUEPRINT_CSV),
            "task": "Verify runtime identity blueprint requires feature, model, report, telemetry, parity, and external verification evidence.",
            "success_condition": "runtime authority cannot be inferred from compile-only or aggregate-only artifacts.",
            "forbidden": "runtime_authority_from_compile_only;missing_report_identity",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "review_gate_regime_tier_blueprints",
            "priority": 6,
            "source_artifact": f"{rel(GATE_RUNNER_BLUEPRINT_CSV)};{rel(REGIME_RUNNER_BLUEPRINT_CSV)};{rel(TIER_NO_LOOKAHEAD_BLUEPRINT_CSV)}",
            "task": "Verify cost, curve, direction, regime, Tier A/B, no-lookahead, and threshold/lot freeze runners are complete.",
            "success_condition": "all stress and attribution runners are ready for later execution review without turning slices into filters.",
            "forbidden": "direct_forward_pocket_filter;missing_Tier_B_record;threshold_changed_after_forward_read",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "review_output_contract_matrix",
            "priority": 7,
            "source_artifact": rel(OUTPUT_CONTRACT_MATRIX_CSV),
            "task": "Verify future artifacts require existence, hash, registry, and next review before use.",
            "success_condition": "no future output can be used without hash and registry linkage.",
            "forbidden": "unregistered_runtime_result;unhashed_proxy_result",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_gate_audit(metrics: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "run336E_queue_loaded",
            "status": "passed",
            "evidence": rel(RUN336F_QUEUE_CSV),
            "finding": f"queue_rows={metrics['queue_rows']};queue_output_tokens={metrics['queue_output_tokens']}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "blueprint_catalog_materialized",
            "status": "passed" if metrics["blueprint_rows"] == metrics["queue_output_tokens"] else "failed",
            "evidence": rel(BLUEPRINT_CATALOG_CSV),
            "finding": f"blueprint_rows={metrics['blueprint_rows']}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "blueprint_field_contracts_materialized",
            "status": "passed" if metrics["field_contract_rows"] == metrics["blueprint_rows"] else "failed",
            "evidence": rel(BLUEPRINT_FIELD_CONTRACT_CSV),
            "finding": f"field_contract_rows={metrics['field_contract_rows']}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "negative_control_blueprints_materialized",
            "status": "passed",
            "evidence": rel(NEGATIVE_CONTROL_BLUEPRINT_CSV),
            "finding": f"negative_control_rows={metrics['negative_control_rows']}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "proxy_runtime_identity_gate_blueprints_materialized",
            "status": "passed",
            "evidence": f"{rel(PROXY_MT5_BLUEPRINT_CSV)};{rel(RUNTIME_IDENTITY_BLUEPRINT_CSV)}",
            "finding": f"proxy_rows={metrics['proxy_mt5_rows']};runtime_rows={metrics['runtime_identity_rows']}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "gate_regime_tier_blueprints_materialized",
            "status": "passed",
            "evidence": f"{rel(GATE_RUNNER_BLUEPRINT_CSV)};{rel(REGIME_RUNNER_BLUEPRINT_CSV)};{rel(TIER_NO_LOOKAHEAD_BLUEPRINT_CSV)}",
            "finding": f"gate_rows={metrics['gate_runner_rows']};regime_rows={metrics['regime_runner_rows']};tier_rows={metrics['tier_rows']}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "run336G_review_queue_created",
            "status": "passed" if metrics["run336g_queue_rows"] == 7 else "failed",
            "evidence": rel(RUN336G_REVIEW_QUEUE_CSV),
            "finding": f"run336g_queue_rows={metrics['run336g_queue_rows']}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "forbidden_claims_absent",
            "status": "passed",
            "evidence": rel(RESULT_JUDGMENT_CSV),
            "finding": "selected candidate, Forward Passed/Failed, live readiness, deployment, operating promotion, runtime authority, Goal Achieve all not_claimed",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def write_run_manifest() -> Path:
    return write_json(
        RUN_MANIFEST_JSON,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "parent_run_id": PARENT_RUN_ID,
            "next_action": NEXT_RUN_ID,
            "stage_id": STAGE_ID,
            "status": STATUS,
            "decision": DECISION,
            "created_at_utc": now_utc(),
            "producer": rel(Path(__file__)),
            "source_inputs": [
                rel(RUN336F_QUEUE_CSV),
                rel(PROTOCOL_ACCEPTANCE_MATRIX_CSV),
                rel(BRANCH_CONTROL_REVIEW_CSV),
                rel(PROXY_MT5_REVIEW_CSV),
                rel(RUNTIME_PREFLIGHT_REVIEW_CSV),
                rel(TIER_NO_LOOKAHEAD_REVIEW_CSV),
                rel(GATE_REVIEW_CSV),
                rel(REGIME_REVIEW_CSV),
                rel(READINESS_REVIEW_CSV),
            ],
            "external_verification_status": "out_of_scope_by_claim_blueprint_materialization_only",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_receipts(metrics: Mapping[str, Any]) -> list[Path]:
    common = {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": now_utc(),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    receipts = {
        "data_integrity_receipt.json": {
            **common,
            "data_source": rel(RUN336E_DIR),
            "time_axis": "blueprint materialization only; future execution must use closed-bar timestamps and no future/nearest joins.",
            "sample_scope": "Stage336 run336E execution blueprint queue; no new US100 M5 bars consumed.",
            "missing_or_duplicate_check": f"queue_rows={metrics['queue_rows']};blueprint_rows={metrics['blueprint_rows']}.",
            "feature_label_boundary": "no feature execution, label creation, training, threshold retune, lot optimization, or forward pocket filter in run336F.",
            "split_boundary": "Tier A, Tier B, actual routed total, future shift canary, and threshold/lot freeze blueprint created.",
            "leakage_risk": "lookahead, old proxy rank, copied runtime result, m48 clue promotion, entrypoint copy, direct pocket filtering remain canary-bound.",
            "data_hash_or_identity": "run336F artifacts registered after execution.",
            "integrity_judgment": "usable_with_boundary",
        },
        "runtime_parity_receipt.json": {
            **common,
            "research_path": rel(Path(__file__)),
            "runtime_path": rel(RUNTIME_IDENTITY_BLUEPRINT_CSV),
            "shared_contract": "future runtime probe must bind feature order, model bundle, tester report, telemetry, row-level parity, and external verification status.",
            "known_differences": "run336F creates blueprints only and does not execute MT5.",
            "parity_check": "runtime identity, proxy-MT5 usability, and output contract blueprints materialized.",
            "parity_identity": f"runtime_identity_rows={metrics['runtime_identity_rows']};proxy_mt5_rows={metrics['proxy_mt5_rows']}",
            "runtime_claim_boundary": "research_only_no_runtime_authority",
        },
        "model_validation_receipt.json": {
            **common,
            "model_family": "future ONNX research packet; no model trained in run336F",
            "target_and_label": "not created; future target and label must be declared before training",
            "split_method": "future Tier A/Tier B paired records plus fresh MT5 runtime probe",
            "selection_metric": "not selected; run336F only materializes execution blueprints",
            "secondary_metrics": "cost stress, curve pocket, underwater stretch, direction, regime, lot-normalized, proxy-vs-MT5 difference",
            "threshold_policy": "no threshold retuning; threshold/lot freeze manifest blueprint is mandatory before future result read",
            "overfit_risk": "direct pocket filtering, m48 clue promotion, copied runtime result, after-result feature pick, old proxy rank",
            "calibration_risk": "proxy expected values remain diagnostic-only until fresh MT5 comparison and calibration evidence exist",
            "comparison_baseline": "run336E reviewed protocols",
            "validation_judgment": "exploratory_execution_blueprint_materialization",
        },
        "performance_attribution_receipt.json": {
            **common,
            "observed_change": "reviewed protocols became concrete execution blueprints and output contracts.",
            "comparison_baseline": "run336E blueprint queue was accepted but not materialized.",
            "likely_drivers": "negative controls, proxy-MT5 difference schemas, runtime identity, cost/curve/regime/tier gates.",
            "segment_checks": "repair, defense, offense, runtime lanes; gate/regime/tier families.",
            "trade_shape": "no new trade result; future trade shape reporting remains mandatory.",
            "alternative_explanations": "blueprint readiness does not prove signal edge or runtime robustness.",
            "attribution_confidence": "high_for_blueprint_materialization_low_for_performance",
            "next_probe": NEXT_RUN_ID,
        },
        "result_judgment_receipt.json": {
            **common,
            "result_subject": "run336F constraint-bound execution blueprint materialization",
            "evidence_available": "blueprint catalog, field contracts, negative controls, proxy-MT5, runtime identity, gate/regime/tier blueprints, output contract matrix, run336G review queue.",
            "evidence_missing": "run336G review, any blueprint execution, model training, fresh MT5 runtime probe, actual proxy-vs-MT5 result, selected candidate, Forward Passed/Failed evidence.",
            "judgment_label": "exploratory_blueprint_materialization",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "실행 청사진은 만들었지만 아직 성능이나 운영 가능성 판정은 아니다.",
        },
        "artifact_lineage_receipt.json": {
            **common,
            "source_inputs": [rel(RUN336F_QUEUE_CSV), rel(PROTOCOL_ACCEPTANCE_MATRIX_CSV)],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [
                rel(BLUEPRINT_CATALOG_CSV),
                rel(BLUEPRINT_FIELD_CONTRACT_CSV),
                rel(RUN336G_REVIEW_QUEUE_CSV),
            ],
            "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_after_stage_closeout",
            "lineage_judgment": "connected_with_boundary",
        },
    }
    paths: list[Path] = []
    for name, payload in receipts.items():
        path = RUN_DIR / name
        write_json(path, payload)
        paths.append(path)
    return paths


def write_reports(metrics: Mapping[str, Any]) -> None:
    report = f"""# Run336F Execution Blueprints(336F 실행 청사진)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- queue_rows(대기열 행): `{metrics['queue_rows']}`
- blueprint_rows(청사진 행): `{metrics['blueprint_rows']}`
- negative_control_rows(부정 대조 행): `{metrics['negative_control_rows']}`
- proxy_mt5_rows(프록시-MT5 행): `{metrics['proxy_mt5_rows']}`
- runtime_identity_rows(런타임 정체성 행): `{metrics['runtime_identity_rows']}`
- gate_runner_rows(게이트 실행기 행): `{metrics['gate_runner_rows']}`
- regime_runner_rows(국면 실행기 행): `{metrics['regime_runner_rows']}`
- next_action(다음 행동): `{NEXT_RUN_ID}`

## Judgment(판정)

run336F(336F 실행)는 run336E(336E 실행)의 execution blueprint queue(실행 청사진 대기열)를 실제 청사진 표로 물질화했다.

Effect(효과): 다음 run336G(336G 실행)는 청사진 자체를 검토한다. 아직 model training(모델 학습), MT5 execution(MT5 실행), candidate selection(후보 선택), Forward decision(전진 판정)은 없다.

## Evidence(근거)

- blueprint_catalog(청사진 목록): `{rel(BLUEPRINT_CATALOG_CSV)}`
- field_contracts(필드 계약): `{rel(BLUEPRINT_FIELD_CONTRACT_CSV)}`
- negative_controls(부정 대조): `{rel(NEGATIVE_CONTROL_BLUEPRINT_CSV)}`
- proxy_mt5_blueprints(프록시-MT5 청사진): `{rel(PROXY_MT5_BLUEPRINT_CSV)}`
- runtime_identity_blueprints(런타임 정체성 청사진): `{rel(RUNTIME_IDENTITY_BLUEPRINT_CSV)}`
- gate_runner_blueprints(게이트 실행기 청사진): `{rel(GATE_RUNNER_BLUEPRINT_CSV)}`
- regime_runner_blueprints(국면 실행기 청사진): `{rel(REGIME_RUNNER_BLUEPRINT_CSV)}`
- tier_no_lookahead_blueprints(티어/미래 참조 금지 청사진): `{rel(TIER_NO_LOOKAHEAD_BLUEPRINT_CSV)}`
- output_contract_matrix(출력 계약 행렬): `{rel(OUTPUT_CONTRACT_MATRIX_CSV)}`
- run336G_review_queue(336G 검토 대기열): `{rel(RUN336G_REVIEW_QUEUE_CSV)}`

## Boundary(경계)

이 실행은 blueprint materialization(청사진 물질화)이다. Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), live readiness(실거래 준비), deployment(배포), operating promotion(운영 승격), Goal Achieve(목표 달성)는 모두 `not_claimed`다.
"""
    decision_doc = f"""# Decision(결정): Stage336F Execution Blueprints(336F 실행 청사진)

`{RUN_ID}`는 run336E(336E 실행)의 9개 queue(대기열)를 31개 execution blueprint(실행 청사진) 행으로 물질화했다.

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- blueprint_rows(청사진 행): `{metrics['blueprint_rows']}`
- run336G_review_queue_rows(336G 검토 대기열 행): `{metrics['run336g_queue_rows']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_condition(다음 조건): `{NEXT_RUN_ID}`

Effect(효과): proxy(프록시), MT5(메타트레이더5), tier(티어), regime(국면), cost/curve(비용/곡선), negative control(부정 대조)이 모두 실행 전 검토 가능한 형태로 묶였다.
"""
    write_md(REPORT_DOC, report)
    write_md(DECISION_DOC, decision_doc)


def update_docs(metrics: Mapping[str, Any]) -> None:
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_line(workspace_text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    workspace_text = replace_line(workspace_text, "updated_on:", f"updated_on: '{TODAY}'")
    focus_line = (
        "  Stage336(336단계) run336F(336F 실행)는 "
        f"`{STATUS}`로 execution blueprints(실행 청사진)를 물질화했다. "
        f"Effect(효과): blueprint catalog(청사진 목록) `{metrics['blueprint_rows']}`행과 "
        f"run336G review queue(336G 검토 대기열) `{metrics['run336g_queue_rows']}`행을 만들었다. "
        "Forward Passed/Failed(전진 통과/실패)와 Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    workspace_text = upsert_folded_list_item(workspace_text, "run336F(336F 실행)", focus_line)
    write_text_lossless(WORKSPACE_STATE, workspace_text, workspace_bom)

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    current_text = replace_line(current_text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    current_text = replace_line(current_text, "- status(상태):", f"- status(상태): `{STATUS}`")
    current_text = replace_line(current_text, "- decision(결정):", f"- decision(결정): `{DECISION}`")
    summary_line = (
        f"- run336F_summary(336F 요약): execution blueprint materialization(실행 청사진 물질화)을 `{STATUS}`로 완료했다. "
        f"Effect(효과): blueprint catalog(청사진 목록) `{metrics['blueprint_rows']}`행, negative control blueprint(부정 대조 청사진) `{metrics['negative_control_rows']}`행, "
        f"run336G review queue(336G 검토 대기열) `{metrics['run336g_queue_rows']}`행을 만들었다. "
        "Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    if "run336F_summary(336F 요약)" in current_text:
        current_text = replace_line(current_text, "- run336F_summary(336F 요약):", summary_line)
    else:
        current_text = current_text.replace("- run336E_summary", summary_line + "\n- run336E_summary", 1)
    write_text_lossless(CURRENT_STATE, current_text, current_bom)

    selection_path = SELECTED_DIR / "selection_status.md"
    selection_text, selection_bom = read_text_lossless(selection_path)
    selection_text = replace_line(selection_text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    selection_text = replace_line(selection_text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_RUN_ID}`")
    selection_text = replace_line(selection_text, "- latest_review(최신 검토):", f"- latest_review(최신 검토): `{RUN_ID}`")
    selection_text = replace_line(
        selection_text,
        "- effect(효과):",
        f"- effect(효과): Stage336(336단계)는 run336F(336F 실행)에서 실행 청사진을 물질화하고 run336G(336G 실행) 검토 대기열을 만들었으며 후보 선택이나 운영 주장은 없다.",
    )
    write_text_lossless(selection_path, selection_text, selection_bom)

    brief_path = SPEC_DIR / "stage_brief.md"
    brief_text, brief_bom = read_text_lossless(brief_path)
    brief_text = replace_line(brief_text, "- latest_run(최신 실행):", f"- latest_run(최신 실행): `{RUN_ID}`")
    write_text_lossless(brief_path, brief_text, brief_bom)

    input_body = f"""- blueprint_catalog(청사진 목록): `{rel(BLUEPRINT_CATALOG_CSV)}`
- blueprint_field_contracts(청사진 필드 계약): `{rel(BLUEPRINT_FIELD_CONTRACT_CSV)}`
- negative_control_blueprints(부정 대조 청사진): `{rel(NEGATIVE_CONTROL_BLUEPRINT_CSV)}`
- proxy_mt5_blueprints(프록시-MT5 청사진): `{rel(PROXY_MT5_BLUEPRINT_CSV)}`
- runtime_identity_blueprints(런타임 정체성 청사진): `{rel(RUNTIME_IDENTITY_BLUEPRINT_CSV)}`
- gate_regime_tier_blueprints(게이트/국면/티어 청사진): `{rel(GATE_RUNNER_BLUEPRINT_CSV)}`; `{rel(REGIME_RUNNER_BLUEPRINT_CSV)}`; `{rel(TIER_NO_LOOKAHEAD_BLUEPRINT_CSV)}`
- run336G_review_queue(336G 검토 대기열): `{rel(RUN336G_REVIEW_QUEUE_CSV)}`
- final_decision(최종 결정): `{rel(FINAL_DECISION_JSON)}`
"""
    append_or_replace_section(INPUTS_DIR / "input_refs.md", "run336F Execution Blueprints(336F 실행 청사진)", input_body)

    changelog_body = f"""- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- effect(효과): execution blueprint(실행 청사진) `{metrics['blueprint_rows']}`행과 run336G review queue(336G 검토 대기열) `{metrics['run336g_queue_rows']}`행을 만들었다.
- boundary(경계): 후보 선택, Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 `not_claimed`.
"""
    append_or_replace_section(CHANGELOG, "Stage336F Execution Blueprints(336F 실행 청사진)", changelog_body)


def update_registries(metrics: Mapping[str, Any], artifact_paths: Sequence[Path]) -> None:
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "stage336_execution_blueprint_materialization",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_DOC),
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};blueprints={metrics['blueprint_rows']};goal_achieve_not_claimed.",
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__execution_blueprints",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "constraint_bound_execution_blueprint_materialization",
                "tier_scope": "Tier A/Tier B paired future runtime requirement",
                "kpi_scope": "blueprint_materialization_no_new_trading_kpi",
                "scoreboard_lane": "experiment_materialization",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_DOC),
                "primary_kpi": f"blueprints={metrics['blueprint_rows']};run336g_queue_rows={metrics['run336g_queue_rows']}",
                "guardrail_kpi": "training_blocked=true;forward_decision_blocked=true;proxy_selection_use=blocked",
                "external_verification_status": "out_of_scope_by_claim_blueprint_materialization_only",
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID}.",
            },
            {
                "ledger_row_id": f"{RUN_ID}__proxy_mt5_blueprints",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": f"{RUN_NUMBER}_proxy_mt5_blueprints",
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "proxy_mt5_runtime_usability_blueprints",
                "tier_scope": "fresh_MT5_runtime_probe_required",
                "kpi_scope": "proxy_vs_mt5_difference_schema_before_usability",
                "scoreboard_lane": "runtime_parity_blueprint",
                "status": STATUS,
                "judgment": "proxy_mt5_blueprints_materialized_diagnostic_only_no_forward_decision",
                "path": rel(PROXY_MT5_BLUEPRINT_CSV),
                "primary_kpi": f"proxy_mt5_rows={metrics['proxy_mt5_rows']}",
                "guardrail_kpi": "selection_use=blocked;forward_decision_use=blocked;fresh_mt5_required=true",
                "external_verification_status": "out_of_scope_by_claim_blueprint_materialization_only",
                "notes": "fresh MT5 result and difference table still required before usability.",
            },
        ],
        key="ledger_row_id",
    )
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
        [
            {
                "ledger_row_id": f"{RUN_ID}__execution_blueprint_materialization",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "work_family": "stage336_execution_blueprint_materialization",
                "evidence_scope": "run336E_blueprint_queue_to_run336G_review",
                "kpi_scope": "blueprint_materialization_no_new_trading_kpi",
                "status": STATUS,
                "judgment": JUDGMENT,
                "claim_boundary": CLAIM_BOUNDARY,
                "path": rel(REPORT_DOC),
                "notes": f"blueprints={metrics['blueprint_rows']};run336g_queue_rows={metrics['run336g_queue_rows']};goal_achieve_not_claimed.",
                "decision": DECISION,
            }
        ],
        key="ledger_row_id",
    )
    created = now_utc()
    artifact_rows = []
    for path in artifact_paths:
        artifact_rows.append(
            {
                "artifact_id": f"{RUN_ID}__{path.stem}",
                "artifact_type": "stage336F_execution_blueprint_materialization",
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created,
                "notes": "run336F_blueprint_materialization_no_selection_no_forward_decision",
            }
        )
    upsert_csv_rows(
        ARTIFACT_REGISTRY,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
        artifact_rows,
        key="artifact_id",
    )


def main() -> None:
    inputs = load_inputs()
    catalog_rows = build_blueprint_catalog(inputs["queue"])
    field_rows = build_field_contract_rows(catalog_rows)
    negative_rows = build_negative_control_blueprints(inputs["branch_controls"])
    proxy_rows = build_proxy_mt5_blueprints(inputs["proxy_mt5_contract"])
    runtime_rows = build_runtime_identity_blueprints(inputs["runtime_preflight"])
    gate_rows = build_gate_runner_blueprints(inputs["gate_plan"])
    regime_rows = build_regime_runner_blueprints(inputs["regime_plan"])
    tier_rows = build_tier_blueprints(inputs["tier_contract"])
    output_rows = build_output_contract_matrix(catalog_rows)
    run336g_queue = build_run336g_queue()
    queue_output_tokens = sum(len(split_semicolon(row["required_outputs"])) for row in inputs["queue"])

    family_counts = Counter(row["blueprint_family"] for row in catalog_rows)
    metrics: dict[str, Any] = {
        "queue_rows": len(inputs["queue"]),
        "queue_output_tokens": queue_output_tokens,
        "blueprint_rows": len(catalog_rows),
        "field_contract_rows": len(field_rows),
        "negative_control_rows": len(negative_rows),
        "proxy_mt5_rows": len(proxy_rows),
        "runtime_identity_rows": len(runtime_rows),
        "gate_runner_rows": len(gate_rows),
        "regime_runner_rows": len(regime_rows),
        "tier_rows": len(tier_rows),
        "output_contract_rows": len(output_rows),
        "run336g_queue_rows": len(run336g_queue),
        "blueprint_family_counts": dict(sorted(family_counts.items())),
    }

    output_paths = [
        write_csv(
            BLUEPRINT_CATALOG_CSV,
            (
                "blueprint_id",
                "queue_id",
                "branch_id",
                "lane",
                "blueprint_name",
                "blueprint_family",
                "ordinal",
                "purpose",
                "future_artifact_hint",
                "source_acceptance_artifact",
                "execution_status",
                "model_training_allowed",
                "mt5_execution_allowed",
                "selection_allowed",
                "forward_decision_allowed",
                "forbidden",
                "claim_boundary",
            ),
            catalog_rows,
        ),
        write_csv(
            BLUEPRINT_FIELD_CONTRACT_CSV,
            (
                "blueprint_id",
                "branch_id",
                "blueprint_name",
                "required_input_identity",
                "required_output_schema",
                "required_gate",
                "failure_condition",
                "future_review_requirement",
                "claim_boundary",
            ),
            field_rows,
        ),
        write_csv(
            NEGATIVE_CONTROL_BLUEPRINT_CSV,
            (
                "control_id",
                "branch_id",
                "target_risk",
                "runner_blueprint",
                "mutation_plan",
                "expected_failure_signature",
                "stop_condition",
                "source_review_decision",
                "future_output",
                "allowed_use",
                "forbidden_use",
                "claim_boundary",
            ),
            negative_rows,
        ),
        write_csv(
            PROXY_MT5_BLUEPRINT_CSV,
            (
                "contract_id",
                "branch_id",
                "proxy_expected_schema",
                "fresh_mt5_result_schema",
                "difference_schema",
                "comparison_key",
                "tolerance_policy",
                "usable_condition",
                "not_usable_condition",
                "future_required_outputs",
                "selection_use",
                "forward_decision_use",
                "claim_boundary",
            ),
            proxy_rows,
        ),
        write_csv(
            RUNTIME_IDENTITY_BLUEPRINT_CSV,
            (
                "preflight_id",
                "branch_id",
                "runtime_subject",
                "required_identity",
                "required_check",
                "acceptance_evidence",
                "future_output_path_requirement",
                "external_verification_status_required",
                "runtime_claim_boundary",
                "future_required_outputs",
                "claim_boundary",
            ),
            runtime_rows,
        ),
        write_csv(
            GATE_RUNNER_BLUEPRINT_CSV,
            (
                "plan_id",
                "branch_id",
                "gate_id",
                "required_measurement",
                "future_output_table_name",
                "review_requirement",
                "failure_memory_trigger",
                "execution_order",
                "forbidden_shortcut",
                "future_runner_blueprint",
                "claim_boundary",
            ),
            gate_rows,
        ),
        write_csv(
            REGIME_RUNNER_BLUEPRINT_CSV,
            (
                "plan_id",
                "branch_id",
                "slice_id",
                "output_field",
                "bucket_policy",
                "required_metrics",
                "allowed_use",
                "forbidden_use",
                "future_runner_blueprint",
                "claim_boundary",
            ),
            regime_rows,
        ),
        write_csv(
            TIER_NO_LOOKAHEAD_BLUEPRINT_CSV,
            (
                "contract_id",
                "tier_scope",
                "required_fields",
                "time_axis_rule",
                "lookahead_canary",
                "acceptance_condition",
                "forbidden",
                "future_runner_blueprint",
                "future_required_outputs",
                "claim_boundary",
            ),
            tier_rows,
        ),
        write_csv(
            OUTPUT_CONTRACT_MATRIX_CSV,
            (
                "blueprint_id",
                "branch_id",
                "blueprint_name",
                "future_artifact_hint",
                "must_exist_before_execution_review",
                "hash_required",
                "registry_required",
                "can_support_model_training",
                "can_support_forward_decision",
                "can_support_runtime_authority",
                "next_review",
                "claim_boundary",
            ),
            output_rows,
        ),
        write_csv(
            RUN336G_REVIEW_QUEUE_CSV,
            ("queue_id", "priority", "source_artifact", "task", "success_condition", "forbidden", "claim_boundary"),
            run336g_queue,
        ),
        write_csv(
            GATE_AUDIT_CSV,
            ("gate_id", "status", "evidence", "finding", "claim_boundary"),
            build_gate_audit(metrics),
        ),
    ]

    result_rows = [
        {
            "run_id": RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "evidence_available": "blueprint_catalog;field_contracts;negative_controls;proxy_mt5_blueprints;runtime_identity_blueprints;gate_regime_tier_blueprints;output_contract_matrix;run336G_queue",
            "evidence_missing": "run336G review;blueprint execution;model training;fresh MT5 runtime probe;actual proxy expected vs MT5 result;selected candidate;Forward Passed/Failed evidence",
            "judgment_label": "exploratory_blueprint_materialization",
            "forward_passed": "not_claimed",
            "forward_failed": "not_claimed",
            "runtime_authority": "not_claimed",
            "goal_achieve": "not_claimed",
            "next_action": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    output_paths.append(
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
        )
    )
    output_paths.append(
        write_json(
            FINAL_DECISION_JSON,
            {
                "run_id": RUN_ID,
                "parent_run_id": PARENT_RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "metrics": metrics,
                "next_action": NEXT_RUN_ID,
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "runtime_authority": "not_claimed",
                "goal_achieve": "not_claimed",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
    )
    output_paths.append(write_run_manifest())
    output_paths.extend(write_receipts(metrics))
    write_reports(metrics)
    output_paths.extend([REPORT_DOC, DECISION_DOC])
    update_docs(metrics)
    output_paths.extend(
        [
            WORKSPACE_STATE,
            CURRENT_STATE,
            CHANGELOG,
            SELECTED_DIR / "selection_status.md",
            SPEC_DIR / "stage_brief.md",
            INPUTS_DIR / "input_refs.md",
        ]
    )
    update_registries(metrics, output_paths)

    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "decision": DECISION,
                "queue_rows": metrics["queue_rows"],
                "blueprint_rows": metrics["blueprint_rows"],
                "negative_control_rows": metrics["negative_control_rows"],
                "run336g_queue_rows": metrics["run336g_queue_rows"],
                "forward_passed": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_RUN_ID,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
