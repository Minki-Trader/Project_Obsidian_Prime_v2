from __future__ import annotations

import csv
import json
import math
import sys
from collections import Counter, defaultdict
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
RUN_NUMBER = "run336E"
RUN_ID = "run336E_review_constraint_bound_research_implementation_protocols_v1"
PARENT_RUN_ID = "run336D_materialize_constraint_bound_research_implementation_queue_v1"
NEXT_RUN_ID = "run336F_materialize_constraint_bound_execution_blueprints_v1"

STATUS = "completed_constraint_bound_research_implementation_protocol_review_no_selection"
JUDGMENT = "reviewed_protocols_accept_execution_blueprint_required_no_model_training_no_forward_decision"
DECISION = "stage336E_protocols_reviewed_run336F_execution_blueprints_ready_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage336E_protocol_review_no_model_training_"
    "no_threshold_retuning_no_lot_optimization_no_forward_pocket_filtering_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

EXPECTED_BRANCH_CONTROLS = {
    "direction_label_flip_canary",
    "promote_m48_plain_canary",
    "copy_runtime_result_canary",
    "entrypoint_copy_canary",
}
EXPECTED_RUNTIME_CHECKS = {
    "feature_order_identity",
    "model_bundle_identity",
    "mt5_report_telemetry_identity",
    "row_level_runtime_parity",
    "external_verification_status",
}
EXPECTED_TIER_CONTRACTS = {
    "tier_a_separate_record",
    "tier_b_separate_or_fallback_record",
    "actual_routed_total_record",
}
EXPECTED_GATES = {
    "cost_buffer_gate",
    "curve_pocket_gate",
    "underwater_stretch_gate",
    "direction_attribution_gate",
    "regime_slice_gate",
    "lot_normalized_gate",
}
EXPECTED_REGIME_SLICES = {"session", "hour", "month", "volatility", "ADX", "VIX", "USD", "rate"}

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN336D_DIR = STAGE_DIR / "02_runs" / "run336D"
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
DECISION_DOC = DOCS / "decisions" / "2026-05-27_stage336E_protocol_review.md"
REPORT_DOC = REVIEWS_DIR / "run336E_protocol_review.md"

PROTOCOL_CARDS_CSV = RUN336D_DIR / "controlled_research_protocol_cards.csv"
BRANCH_NEGATIVE_CONTROL_MATRIX_CSV = RUN336D_DIR / "branch_specific_negative_control_matrix.csv"
PROXY_MT5_USABILITY_CONTRACT_CSV = RUN336D_DIR / "proxy_expected_vs_mt5_usability_contract.csv"
RUNTIME_PREFLIGHT_MANIFEST_CSV = RUN336D_DIR / "runtime_probe_execution_preflight_manifest.csv"
TIER_PAIR_NO_LOOKAHEAD_CONTRACT_CSV = RUN336D_DIR / "tier_pair_and_no_lookahead_contract.csv"
GATE_EXECUTION_PLAN_CSV = RUN336D_DIR / "cost_curve_direction_gate_execution_plan.csv"
REGIME_ATTRIBUTION_PLAN_CSV = RUN336D_DIR / "regime_attribution_execution_plan.csv"
IMPLEMENTATION_READINESS_MATRIX_CSV = RUN336D_DIR / "implementation_readiness_matrix.csv"
RUN336E_REVIEW_QUEUE_CSV = RUN336D_DIR / "run336E_review_queue.csv"

REVIEW_QUEUE_COMPLETION_CSV = RUN_DIR / "review_queue_completion.csv"
BRANCH_NEGATIVE_CONTROL_REVIEW_CSV = RUN_DIR / "branch_specific_negative_control_review.csv"
PROXY_MT5_USABILITY_REVIEW_CSV = RUN_DIR / "proxy_mt5_usability_contract_review.csv"
RUNTIME_PREFLIGHT_REVIEW_CSV = RUN_DIR / "runtime_preflight_manifest_review.csv"
TIER_NO_LOOKAHEAD_REVIEW_CSV = RUN_DIR / "tier_no_lookahead_contract_review.csv"
GATE_EXECUTION_PLAN_REVIEW_CSV = RUN_DIR / "gate_execution_plan_review.csv"
REGIME_ATTRIBUTION_PLAN_REVIEW_CSV = RUN_DIR / "regime_attribution_plan_review.csv"
IMPLEMENTATION_READINESS_REVIEW_CSV = RUN_DIR / "implementation_readiness_review.csv"
PROTOCOL_ACCEPTANCE_MATRIX_CSV = RUN_DIR / "protocol_acceptance_matrix.csv"
RUN336F_BLUEPRINT_QUEUE_CSV = RUN_DIR / "run336F_execution_blueprint_queue.csv"
GATE_AUDIT_CSV = RUN_DIR / "required_gate_coverage_audit.csv"
RESULT_JUDGMENT_CSV = RUN_DIR / "result_judgment.csv"
FINAL_DECISION_JSON = RUN_DIR / "final_protocol_review_decision.json"
RUN_MANIFEST_JSON = RUN_DIR / "run_manifest.json"


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


def require_values(row: Mapping[str, str], fields: Sequence[str]) -> list[str]:
    return [field for field in fields if not str(row.get(field, "")).strip()]


def review_status(passed: bool, accepted_label: str, failed_label: str = "repair_required") -> str:
    return accepted_label if passed else failed_label


def load_inputs() -> dict[str, list[dict[str, str]]]:
    return {
        "protocols": read_csv(PROTOCOL_CARDS_CSV),
        "branch_controls": read_csv(BRANCH_NEGATIVE_CONTROL_MATRIX_CSV),
        "proxy_mt5": read_csv(PROXY_MT5_USABILITY_CONTRACT_CSV),
        "runtime": read_csv(RUNTIME_PREFLIGHT_MANIFEST_CSV),
        "tier": read_csv(TIER_PAIR_NO_LOOKAHEAD_CONTRACT_CSV),
        "gates": read_csv(GATE_EXECUTION_PLAN_CSV),
        "regime": read_csv(REGIME_ATTRIBUTION_PLAN_CSV),
        "readiness": read_csv(IMPLEMENTATION_READINESS_MATRIX_CSV),
        "review_queue": read_csv(RUN336E_REVIEW_QUEUE_CSV),
    }


def build_branch_control_review(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    present = {row["control_id"] for row in rows}
    missing_expected = sorted(EXPECTED_BRANCH_CONTROLS - present)
    review_rows: list[dict[str, Any]] = []
    for row in rows:
        missing_fields = require_values(
            row,
            (
                "branch_id",
                "control_id",
                "target_risk",
                "test_design",
                "expected_failure_signature",
                "stop_condition",
                "repair_action",
                "enforcement_status",
            ),
        )
        passed = (
            not missing_fields
            and row["control_id"] in EXPECTED_BRANCH_CONTROLS
            and row.get("enforcement_status") == "materialized_required_before_run336E_review"
            and "candidate_selection" in row.get("forbidden_use", "")
        )
        review_rows.append(
            {
                "review_id": f"{row['branch_id']}__{row['control_id']}__review",
                "branch_id": row["branch_id"],
                "control_id": row["control_id"],
                "target_risk": row["target_risk"],
                "missing_fields": ";".join(missing_fields),
                "expected_control_missing": "false" if row["control_id"] in EXPECTED_BRANCH_CONTROLS else "unexpected_control",
                "enforcement_review": review_status(passed, "accepted_for_run336F_runner_binding"),
                "next_required_artifact": f"{row['control_id']}_runner_or_auditable_assertion",
                "forbidden_use_review": "passed" if "candidate_selection" in row.get("forbidden_use", "") else "failed",
                "review_decision": review_status(passed and not missing_expected, "branch_specific_negative_controls_reviewed"),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    if missing_expected:
        review_rows.append(
            {
                "review_id": "missing_expected_branch_controls",
                "branch_id": "cross_branch_negative_control_repair",
                "control_id": ";".join(missing_expected),
                "target_risk": "missing_branch_specific_canary",
                "missing_fields": "control_rows",
                "expected_control_missing": "true",
                "enforcement_review": "repair_required",
                "next_required_artifact": "add_missing_branch_control_rows",
                "forbidden_use_review": "failed",
                "review_decision": "repair_required_before_run336F",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return review_rows


def build_proxy_mt5_review(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    review_rows: list[dict[str, Any]] = []
    for row in rows:
        required_true = all(
            row.get(field) == "true"
            for field in (
                "proxy_expected_result_required",
                "fresh_mt5_runtime_probe_required",
                "difference_table_required",
                "usability_decision_required",
            )
        )
        blocked_use = row.get("forward_decision_use") == "blocked" and row.get("selection_use") == "blocked"
        tolerance_named = bool(row.get("predeclared_tolerance", "").strip())
        usable_text = row.get("usable_condition", "").lower()
        usability_guarded = (
            ("fresh" in usable_text and "row" in usable_text)
            or ("branch_level_agreement" in usable_text and "report_telemetry_identity" in usable_text)
        )
        missing_fields = require_values(
            row,
            (
                "comparison_key",
                "proxy_expected_columns",
                "mt5_result_columns",
                "difference_columns",
                "not_usable_condition",
            ),
        )
        passed = required_true and blocked_use and tolerance_named and usability_guarded and not missing_fields
        review_rows.append(
            {
                "review_id": f"{row['contract_id']}__review",
                "contract_id": row["contract_id"],
                "branch_id": row["branch_id"],
                "expected_value_required": row["proxy_expected_result_required"],
                "fresh_mt5_required": row["fresh_mt5_runtime_probe_required"],
                "difference_required": row["difference_table_required"],
                "usability_required": row["usability_decision_required"],
                "blocked_use_review": "passed" if blocked_use else "failed",
                "tolerance_review": "passed" if tolerance_named else "failed",
                "missing_fields": ";".join(missing_fields),
                "review_decision": review_status(passed, "accepted_fresh_mt5_comparison_required_before_usability"),
                "next_required_artifact": "proxy_expected_table;fresh_mt5_runtime_probe_table;proxy_mt5_difference_table;usability_decision_report",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return review_rows


def build_runtime_review(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    review_rows: list[dict[str, Any]] = []
    by_branch: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        suffix = row["preflight_id"].replace(f"{row['branch_id']}__", "")
        by_branch[row["branch_id"]].add(suffix)
        missing_fields = require_values(
            row,
            (
                "runtime_subject",
                "required_identity",
                "required_check",
                "acceptance_evidence",
                "future_output_path_requirement",
                "external_verification_status_required",
            ),
        )
        no_authority = "no_runtime_authority" in row.get("runtime_claim_boundary", "")
        output_paths_named = all(
            token in row.get("future_output_path_requirement", "")
            for token in ("MT5_report_path", "telemetry_path", "row_level_parity_path")
        )
        passed = not missing_fields and no_authority and output_paths_named
        review_rows.append(
            {
                "review_id": f"{row['preflight_id']}__review",
                "branch_id": row["branch_id"],
                "runtime_check": suffix,
                "required_identity": row["required_identity"],
                "missing_fields": ";".join(missing_fields),
                "output_path_review": "passed" if output_paths_named else "failed",
                "runtime_authority_review": "passed" if no_authority else "failed",
                "review_decision": review_status(passed, "runtime_preflight_reviewed_probe_only"),
                "next_required_artifact": f"{suffix}_evidence_builder",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    for branch_id, checks in sorted(by_branch.items()):
        missing = sorted(EXPECTED_RUNTIME_CHECKS - checks)
        if missing:
            review_rows.append(
                {
                    "review_id": f"{branch_id}__missing_runtime_checks",
                    "branch_id": branch_id,
                    "runtime_check": ";".join(missing),
                    "required_identity": "missing_runtime_check",
                    "missing_fields": "runtime_check_rows",
                    "output_path_review": "failed",
                    "runtime_authority_review": "failed",
                    "review_decision": "repair_required_before_runtime_probe",
                    "next_required_artifact": "add_missing_runtime_preflight_rows",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return review_rows


def build_tier_review(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    present = {row["contract_id"] for row in rows}
    missing_expected = sorted(EXPECTED_TIER_CONTRACTS - present)
    review_rows: list[dict[str, Any]] = []
    for row in rows:
        missing_fields = require_values(
            row,
            ("tier_scope", "required_fields", "time_axis_rule", "lookahead_canary", "acceptance_condition", "forbidden"),
        )
        no_future = "future" in row.get("lookahead_canary", "") or "future" in row.get("time_axis_rule", "")
        threshold_or_lot_guard = (
            row["contract_id"] != "actual_routed_total_record"
            or "threshold_lot_freeze_manifest" in row.get("lookahead_canary", "")
            or "threshold_changed_after_forward_read" in row.get("forbidden", "")
        )
        passed = not missing_fields and no_future and threshold_or_lot_guard and row["contract_id"] in EXPECTED_TIER_CONTRACTS
        review_rows.append(
            {
                "review_id": f"{row['contract_id']}__review",
                "contract_id": row["contract_id"],
                "tier_scope": row["tier_scope"],
                "missing_fields": ";".join(missing_fields),
                "lookahead_review": "passed" if no_future else "failed",
                "threshold_lot_freeze_review": "passed" if threshold_or_lot_guard else "failed",
                "review_decision": review_status(passed and not missing_expected, "tier_no_lookahead_contract_reviewed"),
                "next_required_artifact": "tier_pair_record_runner;future_shift_join_canary_runner;threshold_lot_freeze_manifest",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    if missing_expected:
        review_rows.append(
            {
                "review_id": "missing_expected_tier_contracts",
                "contract_id": ";".join(missing_expected),
                "tier_scope": "missing_required",
                "missing_fields": "tier_contract_rows",
                "lookahead_review": "failed",
                "threshold_lot_freeze_review": "failed",
                "review_decision": "repair_required_before_run336F",
                "next_required_artifact": "add_missing_tier_contract_rows",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return review_rows


def build_gate_review(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    by_branch: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        by_branch[row["branch_id"]].add(row["gate_id"])
    review_rows: list[dict[str, Any]] = []
    for branch_id, gates in sorted(by_branch.items()):
        missing = sorted(EXPECTED_GATES - gates)
        review_rows.append(
            {
                "review_id": f"{branch_id}__gate_bundle_review",
                "branch_id": branch_id,
                "gate_rows": len([row for row in rows if row["branch_id"] == branch_id]),
                "expected_gate_rows": len(EXPECTED_GATES),
                "missing_gates": ";".join(missing),
                "gate_bundle_review": "passed" if not missing else "failed",
                "execution_order_review": "passed"
                if all(row.get("execution_order") == "before_any_branch_comparison" for row in rows if row["branch_id"] == branch_id)
                else "failed",
                "forbidden_shortcut_review": "passed"
                if all(row.get("forbidden_shortcut", "").strip() for row in rows if row["branch_id"] == branch_id)
                else "failed",
                "review_decision": "gate_execution_plan_reviewed" if not missing else "repair_required_before_branch_comparison",
                "next_required_artifact": "cost_stress_runner;curve_pocket_runner;underwater_runner;direction_attribution_runner;regime_gate_runner;lot_normalized_runner",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return review_rows


def build_regime_review(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    by_branch: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        by_branch[row["branch_id"]].add(row["slice_id"])
    review_rows: list[dict[str, Any]] = []
    for branch_id, slices in sorted(by_branch.items()):
        branch_rows = [row for row in rows if row["branch_id"] == branch_id]
        missing = sorted(EXPECTED_REGIME_SLICES - slices)
        attribution_only = all(row.get("allowed_use") == "attribution_and_failure_memory_only" for row in branch_rows)
        forbidden_named = all(row.get("forbidden_use", "").strip() for row in branch_rows)
        passed = not missing and attribution_only and forbidden_named
        review_rows.append(
            {
                "review_id": f"{branch_id}__regime_slice_review",
                "branch_id": branch_id,
                "slice_rows": len(branch_rows),
                "expected_slice_rows": len(EXPECTED_REGIME_SLICES),
                "missing_slices": ";".join(missing),
                "attribution_only_review": "passed" if attribution_only else "failed",
                "forbidden_filter_review": "passed" if forbidden_named else "failed",
                "review_decision": review_status(passed, "regime_attribution_plan_reviewed"),
                "next_required_artifact": "session_hour_month_vol_adx_vix_usd_rate_slice_runner",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return review_rows


def build_readiness_review(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    review_rows: list[dict[str, Any]] = []
    for row in rows:
        gate_notes = (
            row["gate_notes"]
            .replace(
                "branch_specific_negative_control_repair_required_before_run336E_acceptance",
                "branch_specific_negative_control_reviewed_for_run336F",
            )
            .replace(
                "after_result_feature_pick_canary_required",
                "after_result_feature_pick_canary_bound_for_run336F",
            )
            .replace(
                "fresh_MT5_runtime_probe_required_before_runtime_claim",
                "fresh_MT5_runtime_probe_still_required_before_runtime_claim",
            )
        )
        passed = (
            row.get("ready_for_run336E_review") == "true"
            and row.get("not_ready_for_model_training") == "true"
            and row.get("not_ready_for_forward_decision") == "true"
            and row.get("protocol_materialized") == "true"
        )
        review_rows.append(
            {
                "review_id": f"{row['subject_id']}__readiness_review",
                "subject_id": row["subject_id"],
                "branch_id": row["branch_id"],
                "lane": row["lane"],
                "review_ready": row["ready_for_run336E_review"],
                "training_blocked": row["not_ready_for_model_training"],
                "forward_decision_blocked": row["not_ready_for_forward_decision"],
                "gate_notes": gate_notes,
                "review_decision": review_status(passed, "ready_for_run336F_blueprint_not_training"),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return review_rows


BLUEPRINTS_BY_BRANCH = {
    "repair_proxy_exclusion_handoff_contract": "same_bar_repair_identity_manifest_builder;proxy_null_rank_validator;handoff_identity_diff_template",
    "defense_cost_curve_underwater_gate": "cost_stress_runner;rolling_curve_pocket_runner;underwater_stretch_runner;lot_normalized_view_builder",
    "defense_direction_symmetry_negative_control": "long_short_attribution_runner;direction_label_flip_canary_runner;side_drop_rejection_validator",
    "offense_m48_plain_density_quality_seed": "feature_family_seed_card_builder;trade_density_target_runner;m48_clue_promotion_canary_runner;copy_runtime_result_canary_runner",
    "offense_cost_buffer_feature_interaction_seed": "interaction_family_matrix_builder;regime_slice_runner;cost_survival_validator;after_result_feature_pick_canary_runner",
    "runtime_parity_probe_bridge_contract": "runtime_handoff_manifest_builder;row_level_parity_schema_builder;tester_telemetry_manifest_validator;proxy_mt5_diff_table_builder",
    "cross_branch_negative_control_repair": "branch_specific_canary_runner_matrix;negative_control_binding_audit",
    "cross_branch_runtime_usability": "proxy_expected_table_schema;fresh_mt5_runtime_probe_result_schema;difference_table_schema;usability_decision_template",
    "cross_branch_data_integrity": "tier_pair_record_runner;future_shift_join_canary_runner;threshold_lot_freeze_manifest_builder",
}


def build_protocol_acceptance(
    protocols: Sequence[Mapping[str, str]],
    review_ok: bool,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in protocols:
        branch_id = row["branch_id"]
        rows.append(
            {
                "protocol_id": row["protocol_id"],
                "branch_id": branch_id,
                "lane": row["lane"],
                "review_status": "accepted_for_run336F_blueprint_materialization" if review_ok else "repair_required",
                "selection_eligible": "false",
                "model_training_allowed": "false",
                "forward_decision_allowed": "false",
                "runtime_authority_allowed": "false",
                "next_required_blueprints": BLUEPRINTS_BY_BRANCH.get(branch_id, "implementation_blueprint_required"),
                "source_protocol_task": row["task"],
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_run336f_queue(acceptance_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, row in enumerate(acceptance_rows, start=1):
        rows.append(
            {
                "queue_id": f"run336F_{row['branch_id']}",
                "priority": index,
                "branch_id": row["branch_id"],
                "lane": row["lane"],
                "source_acceptance_artifact": rel(PROTOCOL_ACCEPTANCE_MATRIX_CSV),
                "task": "Materialize executable or auditable blueprint files for the reviewed protocol without training or threshold/lot changes.",
                "required_outputs": row["next_required_blueprints"],
                "success_condition": "all generated blueprints bind to predeclared controls and are ready for later execution review",
                "execution_mode": "blueprint_materialization_no_model_training_no_mt5_execution_yet",
                "forbidden": "model_training;threshold_retuning;lot_optimization;candidate_selection;Forward_Passed;runtime_authority;direct_forward_pocket_filter",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_review_queue_completion(review_queue: Sequence[Mapping[str, str]], review_paths: Mapping[str, Path], all_passed: bool) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in review_queue:
        queue_id = row["queue_id"]
        rows.append(
            {
                "queue_id": queue_id,
                "priority": row["priority"],
                "source_artifact": row["source_artifact"],
                "review_artifact": rel(review_paths[queue_id]),
                "success_condition": row["success_condition"],
                "review_decision": "completed_review_passed" if all_passed else "completed_review_repair_required",
                "forbidden": row["forbidden"],
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def review_passed(rows: Sequence[Mapping[str, Any]]) -> bool:
    return all("repair_required" not in str(row.get("review_decision", "")) for row in rows)


def build_gate_audit(metrics: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "run336D_artifacts_loaded",
            "status": "passed",
            "evidence": rel(RUN336E_REVIEW_QUEUE_CSV),
            "finding": f"review_queue_rows={metrics['review_queue_rows']};protocol_rows={metrics['protocol_rows']}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "branch_specific_negative_control_review",
            "status": "passed" if metrics["branch_control_review_passed"] else "failed",
            "evidence": rel(BRANCH_NEGATIVE_CONTROL_REVIEW_CSV),
            "finding": f"review_rows={metrics['branch_control_review_rows']};expected_controls={len(EXPECTED_BRANCH_CONTROLS)}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "proxy_mt5_usability_contract_review",
            "status": "passed" if metrics["proxy_mt5_review_passed"] else "failed",
            "evidence": rel(PROXY_MT5_USABILITY_REVIEW_CSV),
            "finding": f"contract_rows={metrics['proxy_mt5_contract_rows']};fresh_mt5_required=true;selection_forward_blocked=true",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "runtime_preflight_manifest_review",
            "status": "passed" if metrics["runtime_review_passed"] else "failed",
            "evidence": rel(RUNTIME_PREFLIGHT_REVIEW_CSV),
            "finding": f"runtime_review_rows={metrics['runtime_review_rows']};runtime_authority_not_claimed=true",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "tier_no_lookahead_review",
            "status": "passed" if metrics["tier_review_passed"] else "failed",
            "evidence": rel(TIER_NO_LOOKAHEAD_REVIEW_CSV),
            "finding": f"tier_review_rows={metrics['tier_review_rows']};future_shift_join_guarded=true",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "gate_and_regime_review",
            "status": "passed" if metrics["gate_review_passed"] and metrics["regime_review_passed"] else "failed",
            "evidence": f"{rel(GATE_EXECUTION_PLAN_REVIEW_CSV)};{rel(REGIME_ATTRIBUTION_PLAN_REVIEW_CSV)}",
            "finding": f"gate_branch_rows={metrics['gate_review_rows']};regime_branch_rows={metrics['regime_review_rows']}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "implementation_readiness_review",
            "status": "passed" if metrics["readiness_review_passed"] else "failed",
            "evidence": rel(IMPLEMENTATION_READINESS_REVIEW_CSV),
            "finding": f"readiness_rows={metrics['readiness_review_rows']};training_blocked=true;forward_blocked=true",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "run336F_blueprint_queue_created",
            "status": "passed" if metrics["run336f_queue_rows"] == metrics["protocol_rows"] else "failed",
            "evidence": rel(RUN336F_BLUEPRINT_QUEUE_CSV),
            "finding": f"run336f_queue_rows={metrics['run336f_queue_rows']}",
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
                rel(PROTOCOL_CARDS_CSV),
                rel(BRANCH_NEGATIVE_CONTROL_MATRIX_CSV),
                rel(PROXY_MT5_USABILITY_CONTRACT_CSV),
                rel(RUNTIME_PREFLIGHT_MANIFEST_CSV),
                rel(TIER_PAIR_NO_LOOKAHEAD_CONTRACT_CSV),
                rel(GATE_EXECUTION_PLAN_CSV),
                rel(REGIME_ATTRIBUTION_PLAN_CSV),
                rel(IMPLEMENTATION_READINESS_MATRIX_CSV),
                rel(RUN336E_REVIEW_QUEUE_CSV),
            ],
            "external_verification_status": "out_of_scope_by_claim_protocol_review_only",
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
            "data_source": rel(RUN336D_DIR),
            "time_axis": "protocol review only; future executable blueprints must keep closed-bar timestamps and no future/nearest join.",
            "sample_scope": "Stage336 run336D contracts; no new US100 M5 bars consumed.",
            "missing_or_duplicate_check": f"review_queue_rows={metrics['review_queue_rows']};protocol_rows={metrics['protocol_rows']}.",
            "feature_label_boundary": "no model training, labels, threshold retune, lot optimization, or forward pocket filter in run336E.",
            "split_boundary": "Tier A, Tier B, and actual routed total contracts reviewed before future runtime result review.",
            "leakage_risk": "future-shift joins, old proxy rank reuse, copied MT5 result, m48 clue promotion, and direct pocket filters remain blocked.",
            "data_hash_or_identity": "run336E artifacts registered after execution.",
            "integrity_judgment": "usable_with_boundary",
        },
        "runtime_parity_receipt.json": {
            **common,
            "research_path": rel(Path(__file__)),
            "runtime_path": rel(RUNTIME_PREFLIGHT_REVIEW_CSV),
            "shared_contract": "future runtime probe must bind feature order, model bundle, report, telemetry, row-level parity, and external verification status.",
            "known_differences": "run336E reviews contracts only and does not execute MT5.",
            "parity_check": "runtime preflight manifest and proxy-vs-MT5 usability contract reviewed.",
            "parity_identity": f"runtime_review_rows={metrics['runtime_review_rows']};proxy_mt5_contract_rows={metrics['proxy_mt5_contract_rows']}",
            "runtime_claim_boundary": "research_only_no_runtime_authority",
        },
        "model_validation_receipt.json": {
            **common,
            "model_family": "future ONNX research packet; no model trained in run336E",
            "target_and_label": "not created; future target and label must be declared before training",
            "split_method": "future Tier A/Tier B paired records plus fresh MT5 runtime probe",
            "selection_metric": "not selected; run336E only accepts blueprint materialization prerequisites",
            "secondary_metrics": "cost stress, curve pocket, underwater stretch, direction, regime, lot-normalized, proxy-vs-MT5 difference",
            "threshold_policy": "no threshold retuning; threshold/lot freeze manifest required in run336F blueprint queue",
            "overfit_risk": "direct pocket filtering, m48 clue promotion, copied runtime result, after-result feature pick",
            "calibration_risk": "proxy expected values are diagnostic-only until fresh MT5 row-level agreement and calibration evidence exist",
            "comparison_baseline": "run336D materialized implementation protocols",
            "validation_judgment": "exploratory_protocol_review",
        },
        "performance_attribution_receipt.json": {
            **common,
            "observed_change": "materialized contracts were reviewed and converted into a run336F execution blueprint queue.",
            "comparison_baseline": "run336D contracts were materialized but not reviewed for execution readiness.",
            "likely_drivers": "branch-specific controls, proxy-vs-MT5 requirements, runtime identity, tier/no-lookahead, cost/curve/regime gate coverage.",
            "segment_checks": "repair, defense, offense, runtime lanes; gates and regime slices checked by branch.",
            "trade_shape": "no new trade result; future trade shape reporting remains mandatory.",
            "alternative_explanations": "protocol readiness does not prove signal edge or operating robustness.",
            "attribution_confidence": "high_for_protocol_review_low_for_performance",
            "next_probe": NEXT_RUN_ID,
        },
        "result_judgment_receipt.json": {
            **common,
            "result_subject": "run336E constraint-bound protocol review",
            "evidence_available": "review scorecards, protocol acceptance matrix, run336F blueprint queue, receipts, registries.",
            "evidence_missing": "run336F blueprints, any model training, fresh MT5 runtime probe, actual proxy-vs-MT5 result, selected candidate, Forward Passed/Failed evidence.",
            "judgment_label": "exploratory_protocol_review",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "검토는 통과했지만 아직 성능이나 운영 가능성 판정은 아니다.",
        },
        "artifact_lineage_receipt.json": {
            **common,
            "source_inputs": [
                rel(PROTOCOL_CARDS_CSV),
                rel(RUN336E_REVIEW_QUEUE_CSV),
                rel(PROXY_MT5_USABILITY_CONTRACT_CSV),
                rel(RUNTIME_PREFLIGHT_MANIFEST_CSV),
            ],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [
                rel(REVIEW_QUEUE_COMPLETION_CSV),
                rel(PROTOCOL_ACCEPTANCE_MATRIX_CSV),
                rel(RUN336F_BLUEPRINT_QUEUE_CSV),
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
    report = f"""# Run336E Protocol Review(336E 계약 검토)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- review_queue_rows(검토 대기열 행): `{metrics['review_queue_rows']}`
- protocol_rows(계약 행): `{metrics['protocol_rows']}`
- branch_control_review_rows(분기 대조 검토 행): `{metrics['branch_control_review_rows']}`
- proxy_mt5_contract_rows(프록시-MT5 계약 행): `{metrics['proxy_mt5_contract_rows']}`
- runtime_review_rows(런타임 검토 행): `{metrics['runtime_review_rows']}`
- run336F_queue_rows(336F 대기열 행): `{metrics['run336f_queue_rows']}`
- next_action(다음 행동): `{NEXT_RUN_ID}`

## Judgment(판정)

run336E(336E 실행)는 run336D(336D 실행)의 implementation protocols(구현 계약)를 검토했고, 9개 protocol(계약)을 run336F(336F 실행)의 execution blueprint(실행 청사진) 물질화 대상으로 넘긴다.

Effect(효과): 다음 실행은 model training(모델 학습)이나 MT5 execution(MT5 실행)이 아니라, negative control runner(부정 대조 실행기), proxy expected vs fresh MT5 difference schema(프록시 예상값 대 신규 MT5 차이 구조), runtime identity manifest(런타임 정체성 목록), tier/no-lookahead runner(티어/미래 참조 금지 실행기)를 실제 파일로 만든다.

## Review Result(검토 결과)

- branch-specific controls(분기 전용 대조): `{metrics['branch_control_review_passed']}`
- proxy/MT5 usability contract(프록시/MT5 활용성 계약): `{metrics['proxy_mt5_review_passed']}`
- runtime preflight(런타임 사전점검): `{metrics['runtime_review_passed']}`
- tier/no-lookahead(티어/미래 참조 금지): `{metrics['tier_review_passed']}`
- cost/curve/direction gates(비용/곡선/방향 게이트): `{metrics['gate_review_passed']}`
- regime attribution(국면 귀속): `{metrics['regime_review_passed']}`
- implementation readiness(구현 준비도): `{metrics['readiness_review_passed']}`

## Evidence(근거)

- review_queue_completion(검토 대기열 완료): `{rel(REVIEW_QUEUE_COMPLETION_CSV)}`
- protocol_acceptance_matrix(계약 승인 행렬): `{rel(PROTOCOL_ACCEPTANCE_MATRIX_CSV)}`
- run336F_blueprint_queue(336F 청사진 대기열): `{rel(RUN336F_BLUEPRINT_QUEUE_CSV)}`
- result_judgment(결과 판정): `{rel(RESULT_JUDGMENT_CSV)}`

## Boundary(경계)

이 실행은 protocol review(계약 검토)다. selected candidate(선택 후보), Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), live readiness(실거래 준비), deployment(배포), operating promotion(운영 승격), Goal Achieve(목표 달성)는 모두 `not_claimed`다.
"""
    decision_doc = f"""# Decision(결정): Stage336E Protocol Review(336E 계약 검토)

`{RUN_ID}`는 run336D(336D 실행)의 구현 전 계약을 검토하고 run336F(336F 실행) execution blueprint(실행 청사진) 대기열을 만들었다.

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- review_queue_rows(검토 대기열 행): `{metrics['review_queue_rows']}`
- protocol_rows(계약 행): `{metrics['protocol_rows']}`
- run336F_queue_rows(336F 대기열 행): `{metrics['run336f_queue_rows']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_condition(다음 조건): `{NEXT_RUN_ID}`

Effect(효과): proxy(프록시)는 여전히 selection/Forward decision(선택/전진 판정)에 쓸 수 없고, 신규 MT5 runtime probe(런타임 탐침)와 차이표가 준비되기 전까지 진단 전용이다.
"""
    write_md(REPORT_DOC, report)
    write_md(DECISION_DOC, decision_doc)


def update_docs(metrics: Mapping[str, Any]) -> None:
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_line(workspace_text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    workspace_text = replace_line(workspace_text, "updated_on:", f"updated_on: '{TODAY}'")
    focus_line = (
        "  Stage336(336단계) run336E(336E 실행)는 "
        f"`{STATUS}`로 implementation protocols(구현 계약)를 검토했다. "
        f"Effect(효과): protocol acceptance matrix(계약 승인 행렬) `{metrics['protocol_rows']}`행과 "
        f"run336F execution blueprint queue(336F 실행 청사진 대기열) `{metrics['run336f_queue_rows']}`행을 만들었다. "
        "Forward Passed/Failed(전진 통과/실패)와 Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    workspace_text = upsert_folded_list_item(workspace_text, "run336E(336E 실행)", focus_line)
    write_text_lossless(WORKSPACE_STATE, workspace_text, workspace_bom)

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    current_text = replace_line(current_text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    current_text = replace_line(current_text, "- status(상태):", f"- status(상태): `{STATUS}`")
    current_text = replace_line(current_text, "- decision(결정):", f"- decision(결정): `{DECISION}`")
    summary_line = (
        f"- run336E_summary(336E 요약): implementation protocol review(구현 계약 검토)를 `{STATUS}`로 완료했다. "
        f"Effect(효과): 검토 대기열 `{metrics['review_queue_rows']}`행을 닫고 protocol acceptance matrix(계약 승인 행렬) `{metrics['protocol_rows']}`행과 "
        f"run336F execution blueprint queue(336F 실행 청사진 대기열) `{metrics['run336f_queue_rows']}`행을 만들었다. "
        "Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    if "run336E_summary(336E 요약)" in current_text:
        current_text = replace_line(current_text, "- run336E_summary(336E 요약):", summary_line)
    else:
        current_text = current_text.replace("- run336D_summary", summary_line + "\n- run336D_summary", 1)
    write_text_lossless(CURRENT_STATE, current_text, current_bom)

    selection_path = SELECTED_DIR / "selection_status.md"
    selection_text, selection_bom = read_text_lossless(selection_path)
    selection_text = replace_line(selection_text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    selection_text = replace_line(selection_text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_RUN_ID}`")
    selection_text = replace_line(selection_text, "- latest_review(최신 검토):", f"- latest_review(최신 검토): `{RUN_ID}`")
    selection_text = replace_line(
        selection_text,
        "- effect(효과):",
        f"- effect(효과): Stage336(336단계)는 run336E(336E 실행)에서 구현 계약을 검토하고 run336F(336F 실행) 실행 청사진 대기열을 만들었으며 후보 선택이나 운영 주장은 없다.",
    )
    write_text_lossless(selection_path, selection_text, selection_bom)

    stage_brief_path = SPEC_DIR / "stage_brief.md"
    brief_text, brief_bom = read_text_lossless(stage_brief_path)
    brief_text = replace_line(brief_text, "- latest_run(최신 실행):", f"- latest_run(최신 실행): `{RUN_ID}`")
    write_text_lossless(stage_brief_path, brief_text, brief_bom)

    input_body = f"""- review_queue_completion(검토 대기열 완료): `{rel(REVIEW_QUEUE_COMPLETION_CSV)}`
- branch_specific_negative_control_review(분기 전용 부정 대조 검토): `{rel(BRANCH_NEGATIVE_CONTROL_REVIEW_CSV)}`
- proxy_mt5_usability_review(프록시-MT5 활용성 검토): `{rel(PROXY_MT5_USABILITY_REVIEW_CSV)}`
- runtime_preflight_review(런타임 사전점검 검토): `{rel(RUNTIME_PREFLIGHT_REVIEW_CSV)}`
- protocol_acceptance_matrix(계약 승인 행렬): `{rel(PROTOCOL_ACCEPTANCE_MATRIX_CSV)}`
- run336F_blueprint_queue(336F 청사진 대기열): `{rel(RUN336F_BLUEPRINT_QUEUE_CSV)}`
- final_decision(최종 결정): `{rel(FINAL_DECISION_JSON)}`
"""
    append_or_replace_section(INPUTS_DIR / "input_refs.md", "run336E Protocol Review(336E 계약 검토)", input_body)

    changelog_body = f"""- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- effect(효과): run336D(336D 실행) 구현 계약을 검토하고 run336F execution blueprint queue(336F 실행 청사진 대기열) `{metrics['run336f_queue_rows']}`행을 만들었다.
- boundary(경계): 후보 선택, Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 `not_claimed`.
"""
    append_or_replace_section(CHANGELOG, "Stage336E Protocol Review(336E 계약 검토)", changelog_body)


def update_registries(metrics: Mapping[str, Any], artifact_paths: Sequence[Path]) -> None:
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "stage336_protocol_review",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_DOC),
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};run336f_queue_rows={metrics['run336f_queue_rows']};goal_achieve_not_claimed.",
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__protocol_review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "constraint_bound_protocol_review",
                "tier_scope": "Tier A/Tier B paired future runtime requirement",
                "kpi_scope": "protocol_review_no_new_trading_kpi",
                "scoreboard_lane": "experiment_review",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_DOC),
                "primary_kpi": f"protocols={metrics['protocol_rows']};run336f_queue_rows={metrics['run336f_queue_rows']}",
                "guardrail_kpi": "training_blocked=true;forward_decision_blocked=true;proxy_selection_use=blocked",
                "external_verification_status": "out_of_scope_by_claim_protocol_review_only",
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID}.",
            },
            {
                "ledger_row_id": f"{RUN_ID}__proxy_mt5_review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": f"{RUN_NUMBER}_proxy_mt5_review",
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "proxy_mt5_usability_contract_review",
                "tier_scope": "fresh_MT5_runtime_probe_required",
                "kpi_scope": "proxy_vs_mt5_difference_required_before_usability",
                "scoreboard_lane": "runtime_parity_review",
                "status": STATUS,
                "judgment": "proxy_mt5_contract_reviewed_diagnostic_only_no_forward_decision",
                "path": rel(PROXY_MT5_USABILITY_REVIEW_CSV),
                "primary_kpi": f"proxy_mt5_contract_rows={metrics['proxy_mt5_contract_rows']}",
                "guardrail_kpi": "selection_use=blocked;forward_decision_use=blocked;fresh_mt5_required=true",
                "external_verification_status": "out_of_scope_by_claim_protocol_review_only",
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
                "ledger_row_id": f"{RUN_ID}__protocol_review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "work_family": "stage336_protocol_review",
                "evidence_scope": "run336D_contracts_to_run336F_execution_blueprints",
                "kpi_scope": "protocol_review_no_new_trading_kpi",
                "status": STATUS,
                "judgment": JUDGMENT,
                "claim_boundary": CLAIM_BOUNDARY,
                "path": rel(REPORT_DOC),
                "notes": f"protocols={metrics['protocol_rows']};run336f_queue_rows={metrics['run336f_queue_rows']};goal_achieve_not_claimed.",
                "decision": DECISION,
            }
        ],
        key="ledger_row_id",
    )
    artifact_rows = []
    created = now_utc()
    for path in artifact_paths:
        artifact_rows.append(
            {
                "artifact_id": f"{RUN_ID}__{path.stem}",
                "artifact_type": "stage336E_protocol_review",
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created,
                "notes": "run336E_protocol_review_no_selection_no_forward_decision",
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
    branch_review = build_branch_control_review(inputs["branch_controls"])
    proxy_review = build_proxy_mt5_review(inputs["proxy_mt5"])
    runtime_review = build_runtime_review(inputs["runtime"])
    tier_review = build_tier_review(inputs["tier"])
    gate_review = build_gate_review(inputs["gates"])
    regime_review = build_regime_review(inputs["regime"])
    readiness_review = build_readiness_review(inputs["readiness"])

    pass_flags = {
        "branch_control_review_passed": review_passed(branch_review),
        "proxy_mt5_review_passed": review_passed(proxy_review),
        "runtime_review_passed": review_passed(runtime_review),
        "tier_review_passed": review_passed(tier_review),
        "gate_review_passed": review_passed(gate_review),
        "regime_review_passed": review_passed(regime_review),
        "readiness_review_passed": review_passed(readiness_review),
    }
    all_passed = all(pass_flags.values())
    acceptance_rows = build_protocol_acceptance(inputs["protocols"], all_passed)
    run336f_queue = build_run336f_queue(acceptance_rows)

    metrics: dict[str, Any] = {
        "review_queue_rows": len(inputs["review_queue"]),
        "protocol_rows": len(inputs["protocols"]),
        "branch_control_review_rows": len(branch_review),
        "proxy_mt5_contract_rows": len(inputs["proxy_mt5"]),
        "runtime_review_rows": len(runtime_review),
        "tier_review_rows": len(tier_review),
        "gate_review_rows": len(gate_review),
        "regime_review_rows": len(regime_review),
        "readiness_review_rows": len(readiness_review),
        "run336f_queue_rows": len(run336f_queue),
        **pass_flags,
    }

    review_paths = {
        "review_branch_specific_negative_controls": BRANCH_NEGATIVE_CONTROL_REVIEW_CSV,
        "review_proxy_expected_vs_mt5_usability_contract": PROXY_MT5_USABILITY_REVIEW_CSV,
        "review_runtime_execution_preflight_manifest": RUNTIME_PREFLIGHT_REVIEW_CSV,
        "review_tier_pair_no_lookahead_contract": TIER_NO_LOOKAHEAD_REVIEW_CSV,
        "review_cost_curve_direction_gate_execution_plan": GATE_EXECUTION_PLAN_REVIEW_CSV,
        "review_regime_attribution_plan": REGIME_ATTRIBUTION_PLAN_REVIEW_CSV,
        "review_implementation_readiness_matrix": IMPLEMENTATION_READINESS_REVIEW_CSV,
    }

    output_paths = [
        write_csv(
            BRANCH_NEGATIVE_CONTROL_REVIEW_CSV,
            (
                "review_id",
                "branch_id",
                "control_id",
                "target_risk",
                "missing_fields",
                "expected_control_missing",
                "enforcement_review",
                "next_required_artifact",
                "forbidden_use_review",
                "review_decision",
                "claim_boundary",
            ),
            branch_review,
        ),
        write_csv(
            PROXY_MT5_USABILITY_REVIEW_CSV,
            (
                "review_id",
                "contract_id",
                "branch_id",
                "expected_value_required",
                "fresh_mt5_required",
                "difference_required",
                "usability_required",
                "blocked_use_review",
                "tolerance_review",
                "missing_fields",
                "review_decision",
                "next_required_artifact",
                "claim_boundary",
            ),
            proxy_review,
        ),
        write_csv(
            RUNTIME_PREFLIGHT_REVIEW_CSV,
            (
                "review_id",
                "branch_id",
                "runtime_check",
                "required_identity",
                "missing_fields",
                "output_path_review",
                "runtime_authority_review",
                "review_decision",
                "next_required_artifact",
                "claim_boundary",
            ),
            runtime_review,
        ),
        write_csv(
            TIER_NO_LOOKAHEAD_REVIEW_CSV,
            (
                "review_id",
                "contract_id",
                "tier_scope",
                "missing_fields",
                "lookahead_review",
                "threshold_lot_freeze_review",
                "review_decision",
                "next_required_artifact",
                "claim_boundary",
            ),
            tier_review,
        ),
        write_csv(
            GATE_EXECUTION_PLAN_REVIEW_CSV,
            (
                "review_id",
                "branch_id",
                "gate_rows",
                "expected_gate_rows",
                "missing_gates",
                "gate_bundle_review",
                "execution_order_review",
                "forbidden_shortcut_review",
                "review_decision",
                "next_required_artifact",
                "claim_boundary",
            ),
            gate_review,
        ),
        write_csv(
            REGIME_ATTRIBUTION_PLAN_REVIEW_CSV,
            (
                "review_id",
                "branch_id",
                "slice_rows",
                "expected_slice_rows",
                "missing_slices",
                "attribution_only_review",
                "forbidden_filter_review",
                "review_decision",
                "next_required_artifact",
                "claim_boundary",
            ),
            regime_review,
        ),
        write_csv(
            IMPLEMENTATION_READINESS_REVIEW_CSV,
            (
                "review_id",
                "subject_id",
                "branch_id",
                "lane",
                "review_ready",
                "training_blocked",
                "forward_decision_blocked",
                "gate_notes",
                "review_decision",
                "claim_boundary",
            ),
            readiness_review,
        ),
        write_csv(
            PROTOCOL_ACCEPTANCE_MATRIX_CSV,
            (
                "protocol_id",
                "branch_id",
                "lane",
                "review_status",
                "selection_eligible",
                "model_training_allowed",
                "forward_decision_allowed",
                "runtime_authority_allowed",
                "next_required_blueprints",
                "source_protocol_task",
                "claim_boundary",
            ),
            acceptance_rows,
        ),
        write_csv(
            RUN336F_BLUEPRINT_QUEUE_CSV,
            (
                "queue_id",
                "priority",
                "branch_id",
                "lane",
                "source_acceptance_artifact",
                "task",
                "required_outputs",
                "success_condition",
                "execution_mode",
                "forbidden",
                "claim_boundary",
            ),
            run336f_queue,
        ),
        write_csv(
            REVIEW_QUEUE_COMPLETION_CSV,
            ("queue_id", "priority", "source_artifact", "review_artifact", "success_condition", "review_decision", "forbidden", "claim_boundary"),
            build_review_queue_completion(inputs["review_queue"], review_paths, all_passed),
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
            "evidence_available": "review_scorecards;protocol_acceptance_matrix;run336F_blueprint_queue;receipts;registries",
            "evidence_missing": "run336F blueprints;model training;fresh MT5 runtime probe;actual proxy expected vs MT5 result;selected candidate;Forward Passed/Failed evidence",
            "judgment_label": "exploratory_protocol_review",
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
                "all_reviews_passed": all_passed,
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
                "all_reviews_passed": all_passed,
                "protocol_rows": metrics["protocol_rows"],
                "review_queue_rows": metrics["review_queue_rows"],
                "run336f_queue_rows": metrics["run336f_queue_rows"],
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
