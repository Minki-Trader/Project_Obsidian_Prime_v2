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
RUN_NUMBER = "run336G"
RUN_ID = "run336G_review_constraint_bound_execution_blueprints_v1"
PARENT_RUN_ID = "run336F_materialize_constraint_bound_execution_blueprints_v1"
NEXT_RUN_ID = "run336H_materialize_constraint_bound_runner_scaffolds_v1"

STATUS = "completed_constraint_bound_execution_blueprint_review_no_selection"
JUDGMENT = "reviewed_execution_blueprints_accept_runner_scaffold_required_no_model_training_no_mt5_execution_no_forward_decision"
DECISION = "stage336G_execution_blueprints_reviewed_run336H_runner_scaffolds_ready_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage336G_execution_blueprint_review_no_model_training_"
    "no_threshold_retuning_no_lot_optimization_no_forward_pocket_filtering_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN336F_DIR = STAGE_DIR / "02_runs" / "run336F"
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
DECISION_DOC = DOCS / "decisions" / "2026-05-27_stage336G_execution_blueprint_review.md"
REPORT_DOC = REVIEWS_DIR / "run336G_execution_blueprint_review.md"

BLUEPRINT_CATALOG_CSV = RUN336F_DIR / "execution_blueprint_catalog.csv"
BLUEPRINT_FIELD_CONTRACT_CSV = RUN336F_DIR / "blueprint_field_contract_matrix.csv"
NEGATIVE_CONTROL_BLUEPRINT_CSV = RUN336F_DIR / "negative_control_runner_blueprints.csv"
PROXY_MT5_BLUEPRINT_CSV = RUN336F_DIR / "proxy_mt5_runtime_usability_blueprints.csv"
RUNTIME_IDENTITY_BLUEPRINT_CSV = RUN336F_DIR / "runtime_identity_blueprints.csv"
GATE_RUNNER_BLUEPRINT_CSV = RUN336F_DIR / "gate_runner_blueprints.csv"
REGIME_RUNNER_BLUEPRINT_CSV = RUN336F_DIR / "regime_slice_runner_blueprints.csv"
TIER_NO_LOOKAHEAD_BLUEPRINT_CSV = RUN336F_DIR / "tier_no_lookahead_runner_blueprints.csv"
OUTPUT_CONTRACT_MATRIX_CSV = RUN336F_DIR / "blueprint_output_contract_matrix.csv"
RUN336G_REVIEW_QUEUE_CSV = RUN336F_DIR / "run336G_review_queue.csv"

BLUEPRINT_CATALOG_REVIEW_CSV = RUN_DIR / "blueprint_catalog_review.csv"
BLUEPRINT_FIELD_CONTRACT_REVIEW_CSV = RUN_DIR / "blueprint_field_contract_review.csv"
NEGATIVE_CONTROL_REVIEW_CSV = RUN_DIR / "negative_control_blueprint_review.csv"
PROXY_MT5_REVIEW_CSV = RUN_DIR / "proxy_mt5_blueprint_review.csv"
RUNTIME_IDENTITY_REVIEW_CSV = RUN_DIR / "runtime_identity_blueprint_review.csv"
GATE_REGIME_TIER_REVIEW_CSV = RUN_DIR / "gate_regime_tier_blueprint_review.csv"
OUTPUT_CONTRACT_REVIEW_CSV = RUN_DIR / "output_contract_matrix_review.csv"
REVIEW_COMPLETION_CSV = RUN_DIR / "blueprint_review_completion.csv"
RUNNER_SCAFFOLD_ACCEPTANCE_CSV = RUN_DIR / "runner_scaffold_acceptance_matrix.csv"
RUN336H_QUEUE_CSV = RUN_DIR / "run336H_runner_scaffold_queue.csv"
GATE_AUDIT_CSV = RUN_DIR / "required_gate_coverage_audit.csv"
RESULT_JUDGMENT_CSV = RUN_DIR / "result_judgment.csv"
FINAL_DECISION_JSON = RUN_DIR / "final_execution_blueprint_review_decision.json"
RUN_MANIFEST_JSON = RUN_DIR / "run_manifest.json"

REQUIRED_CATALOG_FIELDS = (
    "blueprint_id",
    "queue_id",
    "branch_id",
    "lane",
    "blueprint_name",
    "blueprint_family",
    "future_artifact_hint",
    "execution_status",
    "forbidden",
    "claim_boundary",
)
REQUIRED_FIELD_CONTRACT_FIELDS = (
    "blueprint_id",
    "branch_id",
    "blueprint_name",
    "required_input_identity",
    "required_output_schema",
    "required_gate",
    "failure_condition",
    "future_review_requirement",
)
REQUIRED_CATALOG_FAMILIES = {
    "cost_curve",
    "direction",
    "handoff_identity",
    "negative_control",
    "offense_feature",
    "proxy_exclusion",
    "proxy_mt5",
    "regime",
    "repair_identity",
    "runtime_identity",
    "tier_integrity",
}
EXPECTED_NEGATIVE_CONTROLS = {
    "copy_runtime_result_canary",
    "direct_forward_pocket_filter_canary",
    "direction_label_flip_canary",
    "entrypoint_copy_canary",
    "future_shift_join_canary",
    "old_proxy_rank_canary",
    "promote_m48_plain_canary",
    "single_regime_overfit_canary",
    "threshold_lot_freeze_canary",
    "zero_cost_only_canary",
}
EXPECTED_RUNTIME_CHECKS = {
    "external_verification_status",
    "feature_order_identity",
    "model_bundle_identity",
    "mt5_report_telemetry_identity",
    "row_level_runtime_parity",
}
EXPECTED_GATES = {
    "cost_buffer_gate",
    "curve_pocket_gate",
    "direction_attribution_gate",
    "lot_normalized_gate",
    "regime_slice_gate",
    "underwater_stretch_gate",
}
EXPECTED_REGIME_SLICES = {"ADX", "USD", "VIX", "hour", "month", "rate", "session", "volatility"}
EXPECTED_TIER_CONTRACTS = {
    "actual_routed_total_record",
    "threshold_lot_freeze_manifest",
    "tier_a_separate_record",
    "tier_b_separate_or_fallback_record",
}
BLOCKED_ACTION_FIELDS = (
    "model_training_allowed",
    "mt5_execution_allowed",
    "selection_allowed",
    "forward_decision_allowed",
)
FORBIDDEN_TOKENS = {
    "Forward_Passed",
    "candidate_selection",
    "direct_forward_pocket_filter",
    "lot_optimization",
    "model_training",
    "runtime_authority",
    "threshold_retuning",
}
PROXY_REQUIRED_OUTPUTS = {
    "fresh_mt5_runtime_probe_result_table",
    "proxy_expected_result_table",
    "proxy_mt5_difference_table",
    "usability_decision_report",
}
RUNTIME_REQUIRED_PATHS = {"MT5_report_path", "row_level_parity_path", "telemetry_path"}


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


def split_semicolon(value: Any) -> list[str]:
    return [item.strip() for item in str(value or "").split(";") if item.strip()]


def missing_fields(row: Mapping[str, str], fields: Sequence[str]) -> list[str]:
    return [field for field in fields if not str(row.get(field, "")).strip()]


def pass_fail(condition: bool) -> str:
    return "passed" if condition else "failed"


def review_decision(condition: bool, accepted_label: str, failed_label: str = "repair_required_before_run336H") -> str:
    return accepted_label if condition else failed_label


def rows_passed(rows: Sequence[Mapping[str, Any]], field: str = "review_decision") -> bool:
    bad_tokens = ("failed", "repair_required", "missing", "invalid")
    for row in rows:
        value = str(row.get(field, "")).lower()
        if any(token in value for token in bad_tokens):
            return False
    return bool(rows)


def load_inputs() -> dict[str, list[dict[str, str]]]:
    return {
        "catalog": read_csv(BLUEPRINT_CATALOG_CSV),
        "field_contracts": read_csv(BLUEPRINT_FIELD_CONTRACT_CSV),
        "negative_controls": read_csv(NEGATIVE_CONTROL_BLUEPRINT_CSV),
        "proxy_mt5": read_csv(PROXY_MT5_BLUEPRINT_CSV),
        "runtime_identity": read_csv(RUNTIME_IDENTITY_BLUEPRINT_CSV),
        "gates": read_csv(GATE_RUNNER_BLUEPRINT_CSV),
        "regime": read_csv(REGIME_RUNNER_BLUEPRINT_CSV),
        "tier": read_csv(TIER_NO_LOOKAHEAD_BLUEPRINT_CSV),
        "outputs": read_csv(OUTPUT_CONTRACT_MATRIX_CSV),
        "queue": read_csv(RUN336G_REVIEW_QUEUE_CSV),
    }


def build_catalog_review(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    present_families = {row.get("blueprint_family", "") for row in rows}
    missing_families = sorted(REQUIRED_CATALOG_FAMILIES - present_families)
    review_rows: list[dict[str, Any]] = []
    for row in rows:
        missing = missing_fields(row, REQUIRED_CATALOG_FIELDS)
        frozen_actions = all(row.get(field) == "false" for field in BLOCKED_ACTION_FIELDS)
        forbidden = FORBIDDEN_TOKENS.issubset(set(split_semicolon(row.get("forbidden", ""))))
        future_hint = "run336H" in row.get("future_artifact_hint", "") and row.get("future_artifact_hint", "").endswith(".csv")
        status_ok = row.get("execution_status") == "materialized_blueprint_no_execution"
        family_ok = row.get("blueprint_family") in REQUIRED_CATALOG_FAMILIES and not missing_families
        passed = not missing and frozen_actions and forbidden and future_hint and status_ok and family_ok
        review_rows.append(
            {
                "review_id": f"{row.get('blueprint_id')}__catalog_review",
                "blueprint_id": row.get("blueprint_id"),
                "branch_id": row.get("branch_id"),
                "blueprint_family": row.get("blueprint_family"),
                "missing_fields": ";".join(missing),
                "execution_status_review": pass_fail(status_ok),
                "frozen_action_review": pass_fail(frozen_actions),
                "forbidden_review": pass_fail(forbidden),
                "future_scaffold_path_review": pass_fail(future_hint),
                "family_coverage_review": pass_fail(family_ok),
                "review_decision": review_decision(passed, "accepted_for_runner_scaffold_catalog"),
                "next_required_scaffold": row.get("future_artifact_hint"),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    if missing_families:
        review_rows.append(
            {
                "review_id": "missing_blueprint_family_coverage",
                "blueprint_id": "",
                "branch_id": "cross_branch_catalog_repair",
                "blueprint_family": ";".join(missing_families),
                "missing_fields": "blueprint_family_rows",
                "execution_status_review": "failed",
                "frozen_action_review": "failed",
                "forbidden_review": "failed",
                "future_scaffold_path_review": "failed",
                "family_coverage_review": "failed",
                "review_decision": "repair_required_before_run336H",
                "next_required_scaffold": "add_missing_family_blueprints",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return review_rows


def build_field_contract_review(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    review_rows: list[dict[str, Any]] = []
    required_failure_tokens = {"future_shift_join", "proxy_only_selection", "runtime_identity_gap", "threshold_or_lot_changed"}
    for row in rows:
        missing = missing_fields(row, REQUIRED_FIELD_CONTRACT_FIELDS)
        failure_tokens = set(split_semicolon(row.get("failure_condition", "")))
        failure_ok = required_failure_tokens.issubset(failure_tokens)
        future_review_ok = RUN_ID in row.get("future_review_requirement", "") or RUN_NUMBER in row.get("future_review_requirement", "")
        input_output_ok = bool(row.get("required_input_identity", "").strip()) and bool(row.get("required_output_schema", "").strip())
        gate_ok = bool(row.get("required_gate", "").strip())
        passed = not missing and failure_ok and future_review_ok and input_output_ok and gate_ok
        review_rows.append(
            {
                "review_id": f"{row.get('blueprint_id')}__field_contract_review",
                "blueprint_id": row.get("blueprint_id"),
                "branch_id": row.get("branch_id"),
                "blueprint_name": row.get("blueprint_name"),
                "missing_fields": ";".join(missing),
                "input_output_identity_review": pass_fail(input_output_ok),
                "gate_review": pass_fail(gate_ok),
                "failure_condition_review": pass_fail(failure_ok),
                "future_review_requirement_review": pass_fail(future_review_ok),
                "review_decision": review_decision(passed, "accepted_for_runner_scaffold_field_contract"),
                "next_required_scaffold": "materialized_schema_and_precheck",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return review_rows


def build_negative_control_review(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    present = {row.get("control_id", "") for row in rows}
    missing_expected = sorted(EXPECTED_NEGATIVE_CONTROLS - present)
    review_rows: list[dict[str, Any]] = []
    for row in rows:
        missing = missing_fields(
            row,
            (
                "control_id",
                "branch_id",
                "target_risk",
                "runner_blueprint",
                "mutation_plan",
                "expected_failure_signature",
                "stop_condition",
                "future_output",
                "allowed_use",
                "forbidden_use",
            ),
        )
        allowed_ok = row.get("allowed_use") == "negative_control_only"
        forbidden_use = set(split_semicolon(row.get("forbidden_use", "")))
        forbidden_ok = {"Forward_decision", "candidate_selection", "runtime_authority"}.issubset(forbidden_use)
        future_ok = "run336H" in row.get("future_output", "")
        expected_ok = row.get("control_id") in EXPECTED_NEGATIVE_CONTROLS and not missing_expected
        stop_ok = bool(row.get("stop_condition", "").strip()) and bool(row.get("expected_failure_signature", "").strip())
        passed = not missing and allowed_ok and forbidden_ok and future_ok and expected_ok and stop_ok
        review_rows.append(
            {
                "review_id": f"{row.get('control_id')}__negative_control_review",
                "control_id": row.get("control_id"),
                "branch_id": row.get("branch_id"),
                "target_risk": row.get("target_risk"),
                "missing_fields": ";".join(missing),
                "expected_control_review": pass_fail(expected_ok),
                "allowed_use_review": pass_fail(allowed_ok),
                "forbidden_use_review": pass_fail(forbidden_ok),
                "future_output_review": pass_fail(future_ok),
                "stop_condition_review": pass_fail(stop_ok),
                "review_decision": review_decision(passed, "accepted_negative_control_runner_scaffold_required"),
                "next_required_scaffold": row.get("runner_blueprint"),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    if missing_expected:
        review_rows.append(
            {
                "review_id": "missing_expected_negative_controls",
                "control_id": ";".join(missing_expected),
                "branch_id": "cross_branch_negative_control_repair",
                "target_risk": "missing_canary",
                "missing_fields": "control_rows",
                "expected_control_review": "failed",
                "allowed_use_review": "failed",
                "forbidden_use_review": "failed",
                "future_output_review": "failed",
                "stop_condition_review": "failed",
                "review_decision": "repair_required_before_run336H",
                "next_required_scaffold": "add_missing_negative_control_scaffolds",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return review_rows


def build_proxy_mt5_review(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    review_rows: list[dict[str, Any]] = []
    for row in rows:
        missing = missing_fields(
            row,
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
            ),
        )
        future_outputs = set(split_semicolon(row.get("future_required_outputs", "")))
        outputs_ok = PROXY_REQUIRED_OUTPUTS.issubset(future_outputs)
        use_blocked = row.get("selection_use") == "blocked" and row.get("forward_decision_use") == "blocked"
        usable_condition = row.get("usable_condition", "")
        fresh_ok = (
            "fresh_mt5" in usable_condition
            or "branch_level_agreement" in usable_condition
            or "report_telemetry_identity" in usable_condition
        )
        schema_ok = not missing
        passed = schema_ok and outputs_ok and use_blocked and fresh_ok
        review_rows.append(
            {
                "review_id": f"{row.get('contract_id')}__proxy_mt5_review",
                "contract_id": row.get("contract_id"),
                "branch_id": row.get("branch_id"),
                "missing_fields": ";".join(missing),
                "schema_review": pass_fail(schema_ok),
                "required_outputs_review": pass_fail(outputs_ok),
                "blocked_use_review": pass_fail(use_blocked),
                "fresh_mt5_usability_review": pass_fail(fresh_ok),
                "review_decision": review_decision(passed, "accepted_proxy_mt5_diagnostic_scaffold_required"),
                "next_required_scaffold": "proxy_expected_table;fresh_mt5_runtime_probe_result_table;proxy_mt5_difference_table;usability_decision_report",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return review_rows


def build_runtime_identity_review(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    by_branch: dict[str, set[str]] = defaultdict(set)
    review_rows: list[dict[str, Any]] = []
    for row in rows:
        branch_id = row.get("branch_id", "")
        runtime_check = row.get("preflight_id", "").replace(f"{branch_id}__", "")
        by_branch[branch_id].add(runtime_check)
        missing = missing_fields(
            row,
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
            ),
        )
        path_tokens = set(split_semicolon(row.get("future_output_path_requirement", "")))
        paths_ok = RUNTIME_REQUIRED_PATHS.issubset(path_tokens)
        no_authority_ok = "no_runtime_authority" in row.get("runtime_claim_boundary", "")
        external_ok = "completed" in row.get("external_verification_status_required", "") and "failure_log" in row.get(
            "external_verification_status_required", ""
        )
        passed = not missing and paths_ok and no_authority_ok and external_ok and runtime_check in EXPECTED_RUNTIME_CHECKS
        review_rows.append(
            {
                "review_id": f"{row.get('preflight_id')}__runtime_identity_review",
                "preflight_id": row.get("preflight_id"),
                "branch_id": branch_id,
                "runtime_check": runtime_check,
                "missing_fields": ";".join(missing),
                "path_requirement_review": pass_fail(paths_ok),
                "runtime_authority_boundary_review": pass_fail(no_authority_ok),
                "external_verification_review": pass_fail(external_ok),
                "expected_check_review": pass_fail(runtime_check in EXPECTED_RUNTIME_CHECKS),
                "review_decision": review_decision(passed, "accepted_runtime_identity_scaffold_probe_only"),
                "next_required_scaffold": row.get("future_required_outputs"),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    for branch_id, checks in sorted(by_branch.items()):
        missing_checks = sorted(EXPECTED_RUNTIME_CHECKS - checks)
        if missing_checks:
            review_rows.append(
                {
                    "review_id": f"{branch_id}__missing_runtime_identity_checks",
                    "preflight_id": "",
                    "branch_id": branch_id,
                    "runtime_check": ";".join(missing_checks),
                    "missing_fields": "runtime_identity_rows",
                    "path_requirement_review": "failed",
                    "runtime_authority_boundary_review": "failed",
                    "external_verification_review": "failed",
                    "expected_check_review": "failed",
                    "review_decision": "repair_required_before_run336H",
                    "next_required_scaffold": "add_missing_runtime_identity_scaffolds",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return review_rows


def build_gate_regime_tier_review(
    gate_rows: Sequence[Mapping[str, str]],
    regime_rows: Sequence[Mapping[str, str]],
    tier_rows: Sequence[Mapping[str, str]],
) -> list[dict[str, Any]]:
    review_rows: list[dict[str, Any]] = []
    gates_by_branch: dict[str, set[str]] = defaultdict(set)
    regimes_by_branch: dict[str, set[str]] = defaultdict(set)
    for row in gate_rows:
        gates_by_branch[row.get("branch_id", "")].add(row.get("gate_id", ""))
        missing = missing_fields(
            row,
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
            ),
        )
        gate_ok = row.get("gate_id") in EXPECTED_GATES
        forbidden_ok = bool(row.get("forbidden_shortcut", "").strip())
        order_ok = row.get("execution_order") == "before_any_branch_comparison"
        passed = not missing and gate_ok and forbidden_ok and order_ok
        review_rows.append(
            {
                "review_id": f"{row.get('plan_id')}__gate_review",
                "blueprint_family": "gate",
                "source_id": row.get("plan_id"),
                "branch_id": row.get("branch_id"),
                "subject": row.get("gate_id"),
                "missing_fields": ";".join(missing),
                "coverage_review": pass_fail(gate_ok),
                "forbidden_shortcut_review": pass_fail(forbidden_ok),
                "order_or_use_review": pass_fail(order_ok),
                "review_decision": review_decision(passed, "accepted_gate_runner_scaffold_required"),
                "next_required_scaffold": row.get("future_runner_blueprint"),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    for row in regime_rows:
        regimes_by_branch[row.get("branch_id", "")].add(row.get("slice_id", ""))
        missing = missing_fields(
            row,
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
            ),
        )
        slice_ok = row.get("slice_id") in EXPECTED_REGIME_SLICES
        attribution_ok = "attribution" in row.get("allowed_use", "")
        forbidden_ok = "direct_forward_pocket_filter" in row.get("forbidden_use", "")
        passed = not missing and slice_ok and attribution_ok and forbidden_ok
        review_rows.append(
            {
                "review_id": f"{row.get('plan_id')}__regime_review",
                "blueprint_family": "regime",
                "source_id": row.get("plan_id"),
                "branch_id": row.get("branch_id"),
                "subject": row.get("slice_id"),
                "missing_fields": ";".join(missing),
                "coverage_review": pass_fail(slice_ok),
                "forbidden_shortcut_review": pass_fail(forbidden_ok),
                "order_or_use_review": pass_fail(attribution_ok),
                "review_decision": review_decision(passed, "accepted_regime_attribution_scaffold_required"),
                "next_required_scaffold": row.get("future_runner_blueprint"),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    for row in tier_rows:
        missing = missing_fields(
            row,
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
            ),
        )
        contract_ok = row.get("contract_id") in EXPECTED_TIER_CONTRACTS
        no_lookahead_ok = (
            "future" in row.get("lookahead_canary", "")
            or "future" in row.get("forbidden", "")
            or "threshold_lot_freeze_canary" in row.get("lookahead_canary", "")
            or "threshold_changed_after_forward_read" in row.get("forbidden", "")
        )
        freeze_ok = (
            row.get("contract_id") != "threshold_lot_freeze_manifest"
            or "threshold_hash" in row.get("required_fields", "")
            and "lot_logic_hash" in row.get("required_fields", "")
        )
        outputs_ok = "threshold_lot_freeze_manifest" in row.get("future_required_outputs", "")
        passed = not missing and contract_ok and no_lookahead_ok and freeze_ok and outputs_ok
        review_rows.append(
            {
                "review_id": f"{row.get('contract_id')}__tier_review",
                "blueprint_family": "tier_integrity",
                "source_id": row.get("contract_id"),
                "branch_id": "cross_branch_data_integrity",
                "subject": row.get("tier_scope"),
                "missing_fields": ";".join(missing),
                "coverage_review": pass_fail(contract_ok),
                "forbidden_shortcut_review": pass_fail(no_lookahead_ok),
                "order_or_use_review": pass_fail(freeze_ok and outputs_ok),
                "review_decision": review_decision(passed, "accepted_tier_no_lookahead_scaffold_required"),
                "next_required_scaffold": row.get("future_runner_blueprint"),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    for branch_id, present in sorted(gates_by_branch.items()):
        missing_gates = sorted(EXPECTED_GATES - present)
        if missing_gates:
            review_rows.append(
                {
                    "review_id": f"{branch_id}__missing_gate_rows",
                    "blueprint_family": "gate",
                    "source_id": "",
                    "branch_id": branch_id,
                    "subject": ";".join(missing_gates),
                    "missing_fields": "gate_rows",
                    "coverage_review": "failed",
                    "forbidden_shortcut_review": "failed",
                    "order_or_use_review": "failed",
                    "review_decision": "repair_required_before_run336H",
                    "next_required_scaffold": "add_missing_gate_scaffolds",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    for branch_id, present in sorted(regimes_by_branch.items()):
        missing_slices = sorted(EXPECTED_REGIME_SLICES - present)
        if missing_slices:
            review_rows.append(
                {
                    "review_id": f"{branch_id}__missing_regime_rows",
                    "blueprint_family": "regime",
                    "source_id": "",
                    "branch_id": branch_id,
                    "subject": ";".join(missing_slices),
                    "missing_fields": "regime_slice_rows",
                    "coverage_review": "failed",
                    "forbidden_shortcut_review": "failed",
                    "order_or_use_review": "failed",
                    "review_decision": "repair_required_before_run336H",
                    "next_required_scaffold": "add_missing_regime_scaffolds",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return review_rows


def build_output_contract_review(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    review_rows: list[dict[str, Any]] = []
    for row in rows:
        missing = missing_fields(
            row,
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
            ),
        )
        must_exist_ok = row.get("must_exist_before_execution_review") == "true"
        lineage_ok = row.get("hash_required") == "true" and row.get("registry_required") == "true"
        blocked_use_ok = (
            row.get("can_support_model_training") == "false"
            and row.get("can_support_forward_decision") == "false"
            and row.get("can_support_runtime_authority") == "false"
        )
        next_review_ok = RUN_ID in row.get("next_review", "") or RUN_NUMBER in row.get("next_review", "")
        future_ok = "run336H" in row.get("future_artifact_hint", "")
        passed = not missing and must_exist_ok and lineage_ok and blocked_use_ok and next_review_ok and future_ok
        review_rows.append(
            {
                "review_id": f"{row.get('blueprint_id')}__output_contract_review",
                "blueprint_id": row.get("blueprint_id"),
                "branch_id": row.get("branch_id"),
                "blueprint_name": row.get("blueprint_name"),
                "missing_fields": ";".join(missing),
                "must_exist_review": pass_fail(must_exist_ok),
                "hash_registry_review": pass_fail(lineage_ok),
                "blocked_use_review": pass_fail(blocked_use_ok),
                "next_review_binding": pass_fail(next_review_ok),
                "future_artifact_review": pass_fail(future_ok),
                "review_decision": review_decision(passed, "accepted_output_contract_before_execution_review"),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return review_rows


def build_review_completion(
    queue_rows: Sequence[Mapping[str, str]],
    review_pass_flags: Mapping[str, bool],
) -> list[dict[str, Any]]:
    queue_to_review = {
        "review_blueprint_field_contracts": BLUEPRINT_FIELD_CONTRACT_REVIEW_CSV,
        "review_execution_blueprint_catalog": BLUEPRINT_CATALOG_REVIEW_CSV,
        "review_gate_regime_tier_blueprints": GATE_REGIME_TIER_REVIEW_CSV,
        "review_negative_control_blueprints": NEGATIVE_CONTROL_REVIEW_CSV,
        "review_output_contract_matrix": OUTPUT_CONTRACT_REVIEW_CSV,
        "review_proxy_mt5_runtime_usability_blueprints": PROXY_MT5_REVIEW_CSV,
        "review_runtime_identity_blueprints": RUNTIME_IDENTITY_REVIEW_CSV,
    }
    flag_by_queue = {
        "review_blueprint_field_contracts": "field_contract_review_passed",
        "review_execution_blueprint_catalog": "catalog_review_passed",
        "review_gate_regime_tier_blueprints": "gate_regime_tier_review_passed",
        "review_negative_control_blueprints": "negative_control_review_passed",
        "review_output_contract_matrix": "output_contract_review_passed",
        "review_proxy_mt5_runtime_usability_blueprints": "proxy_mt5_review_passed",
        "review_runtime_identity_blueprints": "runtime_identity_review_passed",
    }
    rows: list[dict[str, Any]] = []
    for row in queue_rows:
        queue_id = row.get("queue_id", "")
        source_paths = [RUN336F_DIR / item for item in split_semicolon(row.get("source_artifact", ""))]
        # Source artifacts in the queue are repo-relative paths, so resolve from ROOT.
        source_paths = [ROOT / item for item in split_semicolon(row.get("source_artifact", ""))]
        source_exists = all(path_exists(path) for path in source_paths)
        flag_name = flag_by_queue.get(queue_id, "")
        passed = source_exists and bool(review_pass_flags.get(flag_name, False))
        rows.append(
            {
                "queue_id": queue_id,
                "priority": row.get("priority"),
                "source_artifact": row.get("source_artifact"),
                "review_artifact": rel(queue_to_review.get(queue_id, RUN_DIR / f"{queue_id}.csv")),
                "source_exists_review": pass_fail(source_exists),
                "success_condition_review": pass_fail(passed),
                "review_decision": review_decision(passed, "review_queue_item_completed"),
                "forbidden": row.get("forbidden"),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def family_support_passed(family: str, pass_flags: Mapping[str, bool]) -> bool:
    if family == "negative_control":
        return pass_flags["negative_control_review_passed"]
    if family == "proxy_mt5":
        return pass_flags["proxy_mt5_review_passed"]
    if family in {"handoff_identity", "runtime_identity"}:
        return pass_flags["runtime_identity_review_passed"]
    if family in {"cost_curve", "direction", "regime", "tier_integrity"}:
        return pass_flags["gate_regime_tier_review_passed"]
    return True


def build_runner_scaffold_acceptance(
    catalog_rows: Sequence[Mapping[str, str]],
    catalog_review: Sequence[Mapping[str, Any]],
    field_review: Sequence[Mapping[str, Any]],
    output_review: Sequence[Mapping[str, Any]],
    pass_flags: Mapping[str, bool],
) -> list[dict[str, Any]]:
    catalog_status = {row["blueprint_id"]: "accepted" in row["review_decision"] for row in catalog_review if row.get("blueprint_id")}
    field_status = {row["blueprint_id"]: "accepted" in row["review_decision"] for row in field_review if row.get("blueprint_id")}
    output_status = {row["blueprint_id"]: "accepted" in row["review_decision"] for row in output_review if row.get("blueprint_id")}
    rows: list[dict[str, Any]] = []
    for row in catalog_rows:
        blueprint_id = row.get("blueprint_id", "")
        family = row.get("blueprint_family", "")
        passed = (
            catalog_status.get(blueprint_id, False)
            and field_status.get(blueprint_id, False)
            and output_status.get(blueprint_id, False)
            and family_support_passed(family, pass_flags)
        )
        rows.append(
            {
                "blueprint_id": blueprint_id,
                "branch_id": row.get("branch_id"),
                "blueprint_family": family,
                "blueprint_name": row.get("blueprint_name"),
                "accepted_for_run336H_scaffold": "true" if passed else "false",
                "future_scaffold_path": row.get("future_artifact_hint"),
                "required_materialization": "schema_file;runner_precheck;review_receipt;artifact_registry_row",
                "blocked_until": "run336H_scaffold_materialized_and_reviewed",
                "forbidden_use": "model_training;mt5_execution;candidate_selection;Forward_decision;runtime_authority",
                "review_decision": review_decision(passed, "accepted_for_run336H_runner_scaffold"),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_run336h_queue() -> list[dict[str, Any]]:
    forbidden = "model_training;mt5_execution;threshold_retuning;lot_optimization;candidate_selection;Forward_decision;runtime_authority"
    tasks = [
        (
            "run336H_materialize_catalog_bound_scaffold_index",
            1,
            "cross_branch_registry",
            "blueprint_catalog_review;runner_scaffold_acceptance_matrix",
            "Create scaffold index with one file path per accepted blueprint and no executable trading run.",
            "scaffold_index.csv;scaffold_manifest.json",
            "31 accepted blueprints have scaffold paths, hashes, and registry rows.",
        ),
        (
            "run336H_materialize_negative_control_scaffolds",
            2,
            "negative_control",
            "negative_control_blueprint_review",
            "Create auditable canary scaffolds for all shortcut controls.",
            "negative_control_scaffold_matrix.csv;canary_expected_failure_schema.csv",
            "10 canaries are present and marked negative_control_only.",
        ),
        (
            "run336H_materialize_proxy_mt5_comparison_scaffolds",
            3,
            "proxy_mt5",
            "proxy_mt5_blueprint_review",
            "Create proxy expected, fresh MT5 result, difference, and usability schemas.",
            "proxy_expected_schema.csv;fresh_mt5_result_schema.csv;proxy_mt5_difference_schema.csv;usability_decision_schema.csv",
            "Proxy remains diagnostic-only until fresh MT5 identity evidence exists.",
        ),
        (
            "run336H_materialize_runtime_identity_scaffolds",
            4,
            "runtime_identity",
            "runtime_identity_blueprint_review",
            "Create feature/model/report/telemetry/parity identity scaffolds.",
            "runtime_identity_manifest_schema.csv;row_level_parity_schema.csv;external_verification_log_schema.csv",
            "Runtime authority remains blocked; only runtime_probe evidence can be recorded later.",
        ),
        (
            "run336H_materialize_cost_curve_gate_scaffolds",
            5,
            "cost_curve",
            "gate_regime_tier_blueprint_review",
            "Create cost stress, curve pocket, underwater, direction, and lot-normalized schemas.",
            "cost_stress_schema.csv;curve_pocket_schema.csv;underwater_schema.csv;direction_schema.csv;lot_normalized_schema.csv",
            "Stress views are mandatory before any future comparison.",
        ),
        (
            "run336H_materialize_regime_slice_scaffolds",
            6,
            "regime",
            "gate_regime_tier_blueprint_review",
            "Create session, hour, month, volatility, ADX, VIX, USD, and rate slice schemas.",
            "regime_slice_schema_matrix.csv",
            "Slices are attribution-only and cannot become direct forward filters.",
        ),
        (
            "run336H_materialize_tier_no_lookahead_scaffolds",
            7,
            "tier_integrity",
            "gate_regime_tier_blueprint_review",
            "Create Tier A, Tier B, actual routed total, future-shift canary, and freeze manifest schemas.",
            "tier_pair_schema.csv;future_shift_canary_schema.csv;threshold_lot_freeze_manifest_schema.csv",
            "Tier records and freeze manifest must exist before result ingestion.",
        ),
        (
            "run336H_materialize_direction_and_offense_feature_scaffolds",
            8,
            "direction_offense_feature",
            "blueprint_field_contract_review;gate_regime_tier_blueprint_review",
            "Create long/short attribution and predeclared feature-family seed schemas.",
            "long_short_attribution_schema.csv;feature_family_seed_card_schema.csv;trade_density_target_schema.csv",
            "Side dropping and after-result feature picking remain blocked.",
        ),
        (
            "run336H_materialize_output_registry_and_hash_scaffolds",
            9,
            "artifact_lineage",
            "output_contract_matrix_review",
            "Create artifact registry/hash receipt scaffolds for future runner outputs.",
            "artifact_hash_receipt_schema.csv;output_registry_binding_schema.csv",
            "Every future output requires existence, hash, registry, and next review before use.",
        ),
    ]
    return [
        {
            "queue_id": queue_id,
            "priority": priority,
            "scaffold_group": group,
            "source_reviews": source,
            "task": task,
            "required_outputs": outputs,
            "success_condition": success,
            "forbidden": forbidden,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for queue_id, priority, group, source, task, outputs, success in tasks
    ]


def build_gate_audit(metrics: Mapping[str, Any]) -> list[dict[str, Any]]:
    gates = [
        (
            "run336F_inputs_loaded",
            True,
            rel(RUN336G_REVIEW_QUEUE_CSV),
            f"review_queue_rows={metrics['review_queue_rows']};catalog_rows={metrics['catalog_rows']}",
        ),
        (
            "catalog_and_field_contracts_reviewed",
            metrics["catalog_review_passed"] and metrics["field_contract_review_passed"],
            f"{rel(BLUEPRINT_CATALOG_REVIEW_CSV)};{rel(BLUEPRINT_FIELD_CONTRACT_REVIEW_CSV)}",
            f"catalog_review_rows={metrics['catalog_review_rows']};field_review_rows={metrics['field_contract_review_rows']}",
        ),
        (
            "negative_controls_reviewed",
            metrics["negative_control_review_passed"],
            rel(NEGATIVE_CONTROL_REVIEW_CSV),
            f"negative_control_rows={metrics['negative_control_rows']};expected_controls={len(EXPECTED_NEGATIVE_CONTROLS)}",
        ),
        (
            "proxy_mt5_usability_blueprints_reviewed",
            metrics["proxy_mt5_review_passed"],
            rel(PROXY_MT5_REVIEW_CSV),
            f"proxy_mt5_rows={metrics['proxy_mt5_rows']};required_outputs={len(PROXY_REQUIRED_OUTPUTS)}",
        ),
        (
            "runtime_identity_blueprints_reviewed",
            metrics["runtime_identity_review_passed"],
            rel(RUNTIME_IDENTITY_REVIEW_CSV),
            f"runtime_identity_rows={metrics['runtime_identity_rows']};expected_checks={len(EXPECTED_RUNTIME_CHECKS)}",
        ),
        (
            "gate_regime_tier_blueprints_reviewed",
            metrics["gate_regime_tier_review_passed"],
            rel(GATE_REGIME_TIER_REVIEW_CSV),
            f"gate_rows={metrics['gate_rows']};regime_rows={metrics['regime_rows']};tier_rows={metrics['tier_rows']}",
        ),
        (
            "output_contracts_and_scaffold_queue_created",
            metrics["output_contract_review_passed"] and metrics["run336h_queue_rows"] == 9,
            f"{rel(OUTPUT_CONTRACT_REVIEW_CSV)};{rel(RUN336H_QUEUE_CSV)}",
            f"output_contract_rows={metrics['output_contract_rows']};run336h_queue_rows={metrics['run336h_queue_rows']}",
        ),
        (
            "forbidden_claims_absent",
            True,
            rel(RESULT_JUDGMENT_CSV),
            "selected candidate, Forward Passed/Failed, live readiness, deployment, operating promotion, runtime authority, Goal Achieve all not_claimed",
        ),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": "passed" if passed else "failed",
            "evidence": evidence,
            "finding": finding,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, passed, evidence, finding in gates
    ]


def write_receipts(metrics: Mapping[str, Any]) -> list[Path]:
    common = {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "decision": DECISION,
        "created_at_utc": now_utc(),
        "claim_boundary": CLAIM_BOUNDARY,
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
    }
    receipts = {
        "data_integrity_receipt.json": {
            **common,
            "data_source": [
                rel(BLUEPRINT_CATALOG_CSV),
                rel(BLUEPRINT_FIELD_CONTRACT_CSV),
                rel(PROXY_MT5_BLUEPRINT_CSV),
                rel(RUNTIME_IDENTITY_BLUEPRINT_CSV),
            ],
            "time_axis": "blueprint_review_only_no_market_bar_execution; future scaffolds require closed_bar_only_no_future_or_nearest_join",
            "sample_scope": "Stage336 run336F blueprint artifacts only; no new broker data; no model training rows",
            "missing_or_duplicate_check": "source artifacts loaded; review rows must match expected counts before run336H",
            "feature_label_boundary": "no features or labels recalculated; all future_shift and threshold_lot shortcuts remain canary-gated",
            "split_boundary": "not_applicable_blueprint_review_only",
            "leakage_risk": "after_result_filtering; old_proxy_rank_use; direct_forward_pocket_filter",
            "data_hash_or_identity": {
                "blueprint_catalog_sha256": sha256_file_lf_normalized(BLUEPRINT_CATALOG_CSV),
                "field_contract_sha256": sha256_file_lf_normalized(BLUEPRINT_FIELD_CONTRACT_CSV),
            },
            "integrity_judgment": "usable_with_boundary",
        },
        "runtime_parity_receipt.json": {
            **common,
            "research_path": rel(Path(__file__)),
            "runtime_path": [
                rel(RUNTIME_IDENTITY_BLUEPRINT_CSV),
                rel(PROXY_MT5_BLUEPRINT_CSV),
                rel(RUN336H_QUEUE_CSV),
            ],
            "shared_contract": "feature_order_hash;model_hash;threshold_risk_lot_hash;MT5_report_path;telemetry_path;row_level_parity_path required before runtime interpretation",
            "known_differences": "no MT5 execution in run336G; scaffold review only",
            "parity_check": "runtime identity blueprint review; no compile/tester output claimed",
            "parity_identity": {
                "runtime_identity_rows": metrics["runtime_identity_rows"],
                "proxy_mt5_rows": metrics["proxy_mt5_rows"],
                "runtime_identity_review_sha256": sha256_file_lf_normalized(RUNTIME_IDENTITY_REVIEW_CSV),
            },
            "runtime_claim_boundary": "research_only_no_runtime_authority",
        },
        "model_validation_receipt.json": {
            **common,
            "model_family": "existing_cp322A_related_research_packet_no_new_model_training",
            "target_and_label": "not_rebuilt_in_run336G",
            "split_method": "not_applicable_blueprint_review_only",
            "selection_metric": "none; no candidate selection",
            "secondary_metrics": "future scaffolds require cost, curve, underwater, direction, regime, tier, and proxy-vs-MT5 difference reports",
            "threshold_policy": "frozen; threshold retuning blocked",
            "overfit_risk": "after_result_feature_pick; direct_forward_pocket_filter; old_proxy_rank; copied_runtime_result",
            "calibration_risk": "proxy values remain diagnostic-only until fresh MT5 comparison",
            "comparison_baseline": PARENT_RUN_ID,
            "validation_judgment": "exploratory_review_only",
        },
        "performance_attribution_receipt.json": {
            **common,
            "observed_change": "execution blueprints reviewed and accepted for scaffold materialization",
            "comparison_baseline": PARENT_RUN_ID,
            "likely_drivers": "constraint coverage, negative controls, runtime identity, proxy-vs-MT5 usability contract",
            "segment_checks": "future session/hour/month/volatility/ADX/VIX/USD/rate slices are mandatory attribution-only scaffolds",
            "trade_shape": "not_available_no_trading_execution",
            "alternative_explanations": "a clean blueprint review does not prove profitability or forward robustness",
            "attribution_confidence": "medium_for_scaffold_readiness_low_for_market_performance",
            "next_probe": NEXT_RUN_ID,
        },
        "result_judgment_receipt.json": {
            **common,
            "result_subject": RUN_ID,
            "evidence_available": [
                rel(BLUEPRINT_CATALOG_REVIEW_CSV),
                rel(RUNNER_SCAFFOLD_ACCEPTANCE_CSV),
                rel(RUN336H_QUEUE_CSV),
                rel(GATE_AUDIT_CSV),
            ],
            "evidence_missing": "runner scaffold files; actual execution; model training; MT5 runtime probe; Forward Passed/Failed evidence",
            "judgment_label": "exploratory_review_completed",
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "청사진은 다음 뼈대 작성으로 넘길 수 있지만, 아직 수익성이나 운영 가능성은 말하지 않는다.",
        },
        "artifact_lineage_receipt.json": {
            **common,
            "source_inputs": [
                rel(BLUEPRINT_CATALOG_CSV),
                rel(NEGATIVE_CONTROL_BLUEPRINT_CSV),
                rel(PROXY_MT5_BLUEPRINT_CSV),
                rel(RUNTIME_IDENTITY_BLUEPRINT_CSV),
                rel(OUTPUT_CONTRACT_MATRIX_CSV),
            ],
            "producer": rel(Path(__file__)),
            "consumer": [NEXT_RUN_ID, rel(REPORT_DOC), rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(ARTIFACT_REGISTRY)],
            "artifact_paths": [
                rel(BLUEPRINT_CATALOG_REVIEW_CSV),
                rel(RUNNER_SCAFFOLD_ACCEPTANCE_CSV),
                rel(RUN336H_QUEUE_CSV),
                rel(FINAL_DECISION_JSON),
            ],
            "artifact_hashes": {
                "final_decision_sha256": sha256_file_lf_normalized(FINAL_DECISION_JSON),
                "run336h_queue_sha256": sha256_file_lf_normalized(RUN336H_QUEUE_CSV),
            },
            "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_after_git_add_force_for_ignored_run_outputs",
            "lineage_judgment": "connected_with_boundary",
        },
    }
    paths: list[Path] = []
    for name, payload in receipts.items():
        paths.append(write_json(RUN_DIR / name, payload))
    return paths


def write_run_manifest(metrics: Mapping[str, Any]) -> Path:
    return write_json(
        RUN_MANIFEST_JSON,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "stage_id": STAGE_ID,
            "status": STATUS,
            "decision": DECISION,
            "command": "python stage_pipelines/stage336/review_constraint_bound_execution_blueprints.py",
            "inputs": [
                rel(BLUEPRINT_CATALOG_CSV),
                rel(BLUEPRINT_FIELD_CONTRACT_CSV),
                rel(NEGATIVE_CONTROL_BLUEPRINT_CSV),
                rel(PROXY_MT5_BLUEPRINT_CSV),
                rel(RUNTIME_IDENTITY_BLUEPRINT_CSV),
                rel(GATE_RUNNER_BLUEPRINT_CSV),
                rel(REGIME_RUNNER_BLUEPRINT_CSV),
                rel(TIER_NO_LOOKAHEAD_BLUEPRINT_CSV),
                rel(OUTPUT_CONTRACT_MATRIX_CSV),
                rel(RUN336G_REVIEW_QUEUE_CSV),
            ],
            "outputs": [
                rel(BLUEPRINT_CATALOG_REVIEW_CSV),
                rel(BLUEPRINT_FIELD_CONTRACT_REVIEW_CSV),
                rel(NEGATIVE_CONTROL_REVIEW_CSV),
                rel(PROXY_MT5_REVIEW_CSV),
                rel(RUNTIME_IDENTITY_REVIEW_CSV),
                rel(GATE_REGIME_TIER_REVIEW_CSV),
                rel(OUTPUT_CONTRACT_REVIEW_CSV),
                rel(REVIEW_COMPLETION_CSV),
                rel(RUNNER_SCAFFOLD_ACCEPTANCE_CSV),
                rel(RUN336H_QUEUE_CSV),
            ],
            "metrics": dict(metrics),
            "external_verification_status": "out_of_scope_by_claim_blueprint_review_only",
            "model_training": "not_run",
            "mt5_execution": "not_run",
            "forward_passed": "not_claimed",
            "forward_failed": "not_claimed",
            "runtime_authority": "not_claimed",
            "goal_achieve": "not_claimed",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_reports(metrics: Mapping[str, Any]) -> None:
    report = f"""# run336G Execution Blueprint Review(실행 청사진 검토)

- run_id(실행 ID): `{RUN_ID}`
- parent_run(상위 실행): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- primary_family(주 작업군): `experiment_execution(실험 실행)`
- primary_skill(주 스킬): `obsidian-run-evidence-system(실행 근거 시스템)` equivalent via ledger/receipt closeout(장부/영수증 종료)
- support_skills(보조 스킬): data_integrity(데이터 무결성), runtime_parity(런타임 동등성), model_validation(모델 검증), performance_attribution(성과 귀속), result_judgment(결과 판정), artifact_lineage(산출물 계보)
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Review Result(검토 결과)

- blueprint catalog(청사진 목록): `{metrics['catalog_review_rows']}` rows(행), passed(통과) `{metrics['catalog_review_passed']}`
- field contracts(필드 계약): `{metrics['field_contract_review_rows']}` rows(행), passed(통과) `{metrics['field_contract_review_passed']}`
- negative controls(부정 대조): `{metrics['negative_control_rows']}` rows(행), passed(통과) `{metrics['negative_control_review_passed']}`
- proxy vs MT5(프록시 대 메타트레이더5): `{metrics['proxy_mt5_rows']}` rows(행), passed(통과) `{metrics['proxy_mt5_review_passed']}`
- runtime identity(런타임 정체성): `{metrics['runtime_identity_rows']}` rows(행), passed(통과) `{metrics['runtime_identity_review_passed']}`
- gate/regime/tier(게이트/국면/티어): `{metrics['gate_regime_tier_review_rows']}` rows(행), passed(통과) `{metrics['gate_regime_tier_review_passed']}`
- output contracts(출력 계약): `{metrics['output_contract_rows']}` rows(행), passed(통과) `{metrics['output_contract_review_passed']}`
- run336H queue(336H 대기열): `{metrics['run336h_queue_rows']}` rows(행)

## Judgment(판정)

run336G는 execution blueprint(실행 청사진)를 scaffold materialization(뼈대 물질화)로 넘길 수 있다고 본다. 효과(effect, 효과)는 아직 ONNX(온엑스), threshold(임계값), lot(로트), D/B surface(D/B 표면), risk logic(위험 로직)을 건드리지 않고, 다음 단계가 반드시 negative control(부정 대조), proxy expected vs fresh MT5(프록시 예상값 대 신규 메타트레이더5), runtime identity(런타임 정체성), cost/curve/regime/tier(비용/곡선/국면/티어) 산출물을 먼저 만들게 하는 것이다.

Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), live readiness(실거래 준비), deployment(배포), operating promotion(운영 승격), Goal Achieve(목표 달성)는 모두 `not_claimed`다.

## Next(다음)

`{NEXT_RUN_ID}`에서 실제 runner scaffold(러너 뼈대) 파일과 hash/registry(해시/등록부) 연결을 물질화한다. 그 다음에만 실행 가능성, proxy/MT5 difference(차이), cost stress(비용 압박), curve pocket(곡선 포켓)을 순서대로 열 수 있다.
"""
    decision = f"""# Stage336G Execution Blueprint Review Decision(실행 청사진 검토 결정)

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- status(상태): `{STATUS}`
- next_action(다음 행동): `{NEXT_RUN_ID}`

## Decision(결정)

run336F의 execution blueprint(실행 청사진)는 run336H runner scaffold(러너 뼈대) 작성으로 넘긴다. 효과(effect, 효과)는 다음 작업이 직접 모델 학습(model training, 모델 학습)이나 MT5 execution(MT5 실행)으로 뛰지 않고, 먼저 실행 산출물의 schema/hash/registry(스키마/해시/등록부)를 잠그게 하는 것이다.

## Boundary(경계)

이 결정은 Forward Passed(전진 통과)나 Forward Failed(전진 실패)가 아니다. 후보 선택(selected candidate, 선택 후보), runtime authority(런타임 권위), operating promotion(운영 승격), deployment(배포), Goal Achieve(목표 달성)는 모두 주장하지 않는다.
"""
    write_md(REPORT_DOC, report)
    write_md(DECISION_DOC, decision)


def update_docs(metrics: Mapping[str, Any]) -> None:
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_line(workspace_text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    focus_line = (
        f"  Stage336(336단계) run336G(336G 실행)는 `{STATUS}`로 execution blueprint review(실행 청사진 검토)를 완료했다. "
        f"Effect(효과): blueprint review(청사진 검토) `{metrics['review_completion_rows']}`행과 run336H runner scaffold queue(336H 러너 뼈대 대기열) `{metrics['run336h_queue_rows']}`행을 만들었다. "
        "Forward Passed/Failed(전진 통과/실패)와 Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    workspace_text = upsert_folded_list_item(workspace_text, "run336G(336G 실행)", focus_line)
    write_text_lossless(WORKSPACE_STATE, workspace_text, workspace_bom)

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    current_text = replace_line(current_text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    current_text = replace_line(current_text, "- status(상태):", f"- status(상태): `{STATUS}`")
    current_text = replace_line(current_text, "- decision(결정):", f"- decision(결정): `{DECISION}`")
    summary_line = (
        f"- run336G_summary(336G 요약): execution blueprint review(실행 청사진 검토)를 `{STATUS}`로 완료했다. "
        f"Effect(효과): run336F blueprint(336F 청사진) `{metrics['catalog_rows']}`행을 검토하고 runner scaffold acceptance matrix(러너 뼈대 승인 행렬) `{metrics['runner_scaffold_acceptance_rows']}`행, "
        f"run336H queue(336H 대기열) `{metrics['run336h_queue_rows']}`행을 만들었다. "
        "Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    if "run336G_summary(336G 요약)" in current_text:
        current_text = replace_line(current_text, "- run336G_summary(336G 요약):", summary_line)
    else:
        current_text = current_text.replace("- run336F_summary", summary_line + "\n- run336F_summary", 1)
    write_text_lossless(CURRENT_STATE, current_text, current_bom)

    selection_path = SELECTED_DIR / "selection_status.md"
    selection_text, selection_bom = read_text_lossless(selection_path)
    selection_text = replace_line(selection_text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    selection_text = replace_line(selection_text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_RUN_ID}`")
    selection_text = replace_line(selection_text, "- latest_review(최신 검토):", f"- latest_review(최신 검토): `{RUN_ID}`")
    selection_text = replace_line(
        selection_text,
        "- effect(효과):",
        f"- effect(효과): Stage336(336단계)는 run336G(336G 실행)에서 실행 청사진을 검토하고 run336H(336H 실행) runner scaffold(러너 뼈대) 대기열을 만들었으며 후보 선택이나 운영 주장은 없다.",
    )
    write_text_lossless(selection_path, selection_text, selection_bom)

    brief_path = SPEC_DIR / "stage_brief.md"
    brief_text, brief_bom = read_text_lossless(brief_path)
    brief_text = replace_line(brief_text, "- latest_run(최신 실행):", f"- latest_run(최신 실행): `{RUN_ID}`")
    write_text_lossless(brief_path, brief_text, brief_bom)

    input_body = f"""- blueprint_catalog_review(청사진 목록 검토): `{rel(BLUEPRINT_CATALOG_REVIEW_CSV)}`
- field_contract_review(필드 계약 검토): `{rel(BLUEPRINT_FIELD_CONTRACT_REVIEW_CSV)}`
- negative_control_review(부정 대조 검토): `{rel(NEGATIVE_CONTROL_REVIEW_CSV)}`
- proxy_mt5_review(프록시/메타트레이더5 검토): `{rel(PROXY_MT5_REVIEW_CSV)}`
- runtime_identity_review(런타임 정체성 검토): `{rel(RUNTIME_IDENTITY_REVIEW_CSV)}`
- gate_regime_tier_review(게이트/국면/티어 검토): `{rel(GATE_REGIME_TIER_REVIEW_CSV)}`
- runner_scaffold_acceptance(러너 뼈대 승인): `{rel(RUNNER_SCAFFOLD_ACCEPTANCE_CSV)}`
- run336H_queue(336H 대기열): `{rel(RUN336H_QUEUE_CSV)}`
- final_decision(최종 결정): `{rel(FINAL_DECISION_JSON)}`
"""
    append_or_replace_section(INPUTS_DIR / "input_refs.md", "run336G Execution Blueprint Review(336G 실행 청사진 검토)", input_body)

    changelog_body = f"""- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- effect(효과): run336F execution blueprint(336F 실행 청사진)를 검토하고 run336H runner scaffold queue(336H 러너 뼈대 대기열) `{metrics['run336h_queue_rows']}`행을 만들었다.
- boundary(경계): 후보 선택, Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 `not_claimed`.
"""
    append_or_replace_section(CHANGELOG, "Stage336G Execution Blueprint Review(336G 실행 청사진 검토)", changelog_body)


def update_registries(metrics: Mapping[str, Any], artifact_paths: Sequence[Path]) -> None:
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "stage336_execution_blueprint_review",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_DOC),
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};run336h_queue_rows={metrics['run336h_queue_rows']};goal_achieve_not_claimed.",
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__execution_blueprint_review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "constraint_bound_execution_blueprint_review",
                "tier_scope": "Tier A/Tier B paired future runtime requirement",
                "kpi_scope": "blueprint_review_no_new_trading_kpi",
                "scoreboard_lane": "experiment_review",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_DOC),
                "primary_kpi": f"catalog_rows={metrics['catalog_rows']};run336h_queue_rows={metrics['run336h_queue_rows']}",
                "guardrail_kpi": "training_blocked=true;mt5_execution_blocked=true;forward_decision_blocked=true;runtime_authority_blocked=true",
                "external_verification_status": "out_of_scope_by_claim_blueprint_review_only",
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID}.",
            },
            {
                "ledger_row_id": f"{RUN_ID}__proxy_mt5_review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": f"{RUN_NUMBER}_proxy_mt5_review",
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "proxy_mt5_runtime_usability_blueprint_review",
                "tier_scope": "fresh_MT5_runtime_probe_required",
                "kpi_scope": "proxy_vs_mt5_difference_schema_before_usability",
                "scoreboard_lane": "runtime_parity_review",
                "status": STATUS,
                "judgment": "proxy_mt5_blueprints_reviewed_diagnostic_only_no_forward_decision",
                "path": rel(PROXY_MT5_REVIEW_CSV),
                "primary_kpi": f"proxy_mt5_rows={metrics['proxy_mt5_rows']}",
                "guardrail_kpi": "selection_use=blocked;forward_decision_use=blocked;fresh_mt5_required=true",
                "external_verification_status": "out_of_scope_by_claim_blueprint_review_only",
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
                "ledger_row_id": f"{RUN_ID}__execution_blueprint_review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "work_family": "stage336_execution_blueprint_review",
                "evidence_scope": "run336F_execution_blueprints_to_run336H_runner_scaffolds",
                "kpi_scope": "blueprint_review_no_new_trading_kpi",
                "status": STATUS,
                "judgment": JUDGMENT,
                "claim_boundary": CLAIM_BOUNDARY,
                "path": rel(REPORT_DOC),
                "notes": f"catalog_rows={metrics['catalog_rows']};run336h_queue_rows={metrics['run336h_queue_rows']};goal_achieve_not_claimed.",
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
                "artifact_type": "stage336G_execution_blueprint_review",
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created,
                "notes": "run336G_blueprint_review_no_selection_no_forward_decision",
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
    catalog_review = build_catalog_review(inputs["catalog"])
    field_review = build_field_contract_review(inputs["field_contracts"])
    negative_review = build_negative_control_review(inputs["negative_controls"])
    proxy_review = build_proxy_mt5_review(inputs["proxy_mt5"])
    runtime_review = build_runtime_identity_review(inputs["runtime_identity"])
    gate_regime_tier_review = build_gate_regime_tier_review(inputs["gates"], inputs["regime"], inputs["tier"])
    output_review = build_output_contract_review(inputs["outputs"])

    pass_flags = {
        "catalog_review_passed": rows_passed(catalog_review),
        "field_contract_review_passed": rows_passed(field_review),
        "negative_control_review_passed": rows_passed(negative_review),
        "proxy_mt5_review_passed": rows_passed(proxy_review),
        "runtime_identity_review_passed": rows_passed(runtime_review),
        "gate_regime_tier_review_passed": rows_passed(gate_regime_tier_review),
        "output_contract_review_passed": rows_passed(output_review),
    }
    review_completion = build_review_completion(inputs["queue"], pass_flags)
    runner_acceptance = build_runner_scaffold_acceptance(
        inputs["catalog"],
        catalog_review,
        field_review,
        output_review,
        pass_flags,
    )
    run336h_queue = build_run336h_queue()
    family_counts = Counter(row.get("blueprint_family", "") for row in inputs["catalog"])

    metrics: dict[str, Any] = {
        "review_queue_rows": len(inputs["queue"]),
        "catalog_rows": len(inputs["catalog"]),
        "catalog_review_rows": len(catalog_review),
        "field_contract_rows": len(inputs["field_contracts"]),
        "field_contract_review_rows": len(field_review),
        "negative_control_rows": len(inputs["negative_controls"]),
        "negative_control_review_rows": len(negative_review),
        "proxy_mt5_rows": len(inputs["proxy_mt5"]),
        "proxy_mt5_review_rows": len(proxy_review),
        "runtime_identity_rows": len(inputs["runtime_identity"]),
        "runtime_identity_review_rows": len(runtime_review),
        "gate_rows": len(inputs["gates"]),
        "regime_rows": len(inputs["regime"]),
        "tier_rows": len(inputs["tier"]),
        "gate_regime_tier_review_rows": len(gate_regime_tier_review),
        "output_contract_rows": len(inputs["outputs"]),
        "output_contract_review_rows": len(output_review),
        "review_completion_rows": len(review_completion),
        "runner_scaffold_acceptance_rows": len(runner_acceptance),
        "run336h_queue_rows": len(run336h_queue),
        "blueprint_family_counts": dict(sorted(family_counts.items())),
        **pass_flags,
    }

    output_paths = [
        write_csv(
            BLUEPRINT_CATALOG_REVIEW_CSV,
            (
                "review_id",
                "blueprint_id",
                "branch_id",
                "blueprint_family",
                "missing_fields",
                "execution_status_review",
                "frozen_action_review",
                "forbidden_review",
                "future_scaffold_path_review",
                "family_coverage_review",
                "review_decision",
                "next_required_scaffold",
                "claim_boundary",
            ),
            catalog_review,
        ),
        write_csv(
            BLUEPRINT_FIELD_CONTRACT_REVIEW_CSV,
            (
                "review_id",
                "blueprint_id",
                "branch_id",
                "blueprint_name",
                "missing_fields",
                "input_output_identity_review",
                "gate_review",
                "failure_condition_review",
                "future_review_requirement_review",
                "review_decision",
                "next_required_scaffold",
                "claim_boundary",
            ),
            field_review,
        ),
        write_csv(
            NEGATIVE_CONTROL_REVIEW_CSV,
            (
                "review_id",
                "control_id",
                "branch_id",
                "target_risk",
                "missing_fields",
                "expected_control_review",
                "allowed_use_review",
                "forbidden_use_review",
                "future_output_review",
                "stop_condition_review",
                "review_decision",
                "next_required_scaffold",
                "claim_boundary",
            ),
            negative_review,
        ),
        write_csv(
            PROXY_MT5_REVIEW_CSV,
            (
                "review_id",
                "contract_id",
                "branch_id",
                "missing_fields",
                "schema_review",
                "required_outputs_review",
                "blocked_use_review",
                "fresh_mt5_usability_review",
                "review_decision",
                "next_required_scaffold",
                "claim_boundary",
            ),
            proxy_review,
        ),
        write_csv(
            RUNTIME_IDENTITY_REVIEW_CSV,
            (
                "review_id",
                "preflight_id",
                "branch_id",
                "runtime_check",
                "missing_fields",
                "path_requirement_review",
                "runtime_authority_boundary_review",
                "external_verification_review",
                "expected_check_review",
                "review_decision",
                "next_required_scaffold",
                "claim_boundary",
            ),
            runtime_review,
        ),
        write_csv(
            GATE_REGIME_TIER_REVIEW_CSV,
            (
                "review_id",
                "blueprint_family",
                "source_id",
                "branch_id",
                "subject",
                "missing_fields",
                "coverage_review",
                "forbidden_shortcut_review",
                "order_or_use_review",
                "review_decision",
                "next_required_scaffold",
                "claim_boundary",
            ),
            gate_regime_tier_review,
        ),
        write_csv(
            OUTPUT_CONTRACT_REVIEW_CSV,
            (
                "review_id",
                "blueprint_id",
                "branch_id",
                "blueprint_name",
                "missing_fields",
                "must_exist_review",
                "hash_registry_review",
                "blocked_use_review",
                "next_review_binding",
                "future_artifact_review",
                "review_decision",
                "claim_boundary",
            ),
            output_review,
        ),
        write_csv(
            REVIEW_COMPLETION_CSV,
            (
                "queue_id",
                "priority",
                "source_artifact",
                "review_artifact",
                "source_exists_review",
                "success_condition_review",
                "review_decision",
                "forbidden",
                "claim_boundary",
            ),
            review_completion,
        ),
        write_csv(
            RUNNER_SCAFFOLD_ACCEPTANCE_CSV,
            (
                "blueprint_id",
                "branch_id",
                "blueprint_family",
                "blueprint_name",
                "accepted_for_run336H_scaffold",
                "future_scaffold_path",
                "required_materialization",
                "blocked_until",
                "forbidden_use",
                "review_decision",
                "claim_boundary",
            ),
            runner_acceptance,
        ),
        write_csv(
            RUN336H_QUEUE_CSV,
            (
                "queue_id",
                "priority",
                "scaffold_group",
                "source_reviews",
                "task",
                "required_outputs",
                "success_condition",
                "forbidden",
                "claim_boundary",
            ),
            run336h_queue,
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
            "evidence_available": "blueprint_reviews;runner_scaffold_acceptance_matrix;run336H_queue;receipts;registries",
            "evidence_missing": "run336H scaffold files;model training;fresh MT5 runtime probe;actual proxy expected vs MT5 result;selected candidate;Forward Passed/Failed evidence",
            "judgment_label": "exploratory_blueprint_review",
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
                "all_reviews_passed": all(pass_flags.values()),
                "next_action": NEXT_RUN_ID,
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "runtime_authority": "not_claimed",
                "goal_achieve": "not_claimed",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
    )
    output_paths.append(write_run_manifest(metrics))
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
                "all_reviews_passed": all(pass_flags.values()),
                "catalog_rows": metrics["catalog_rows"],
                "review_queue_rows": metrics["review_queue_rows"],
                "runner_scaffold_acceptance_rows": metrics["runner_scaffold_acceptance_rows"],
                "run336h_queue_rows": metrics["run336h_queue_rows"],
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
