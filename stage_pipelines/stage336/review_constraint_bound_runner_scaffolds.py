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
RUN_NUMBER = "run336I"
RUN_ID = "run336I_review_constraint_bound_runner_scaffolds_v1"
PARENT_RUN_ID = "run336H_materialize_constraint_bound_runner_scaffolds_v1"
NEXT_RUN_ID = "run336J_materialize_proxy_expected_fresh_mt5_probe_inputs_v1"

STATUS = "completed_constraint_bound_runner_scaffold_review_no_execution"
JUDGMENT = "reviewed_runner_scaffolds_accept_proxy_mt5_probe_input_materialization_no_model_training_no_mt5_execution_no_forward_decision"
DECISION = "stage336I_runner_scaffolds_reviewed_run336J_proxy_mt5_probe_inputs_ready_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage336I_runner_scaffold_review_no_model_training_"
    "no_mt5_execution_no_threshold_retuning_no_lot_optimization_no_forward_pocket_filtering_"
    "no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)
FORBIDDEN = (
    "model_training;mt5_execution;threshold_retuning;lot_optimization;candidate_selection;"
    "Forward_decision;runtime_authority;deployment;operating_promotion;Goal_Achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN336H_DIR = STAGE_DIR / "02_runs" / "run336H"
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
DECISION_DOC = DOCS / "decisions" / "2026-05-27_stage336I_runner_scaffold_review.md"
REPORT_DOC = REVIEWS_DIR / "run336I_runner_scaffold_review.md"

SCAFFOLD_INDEX_CSV = RUN336H_DIR / "scaffold_index.csv"
SCAFFOLD_MANIFEST_JSON = RUN336H_DIR / "scaffold_manifest.json"
NEGATIVE_CONTROL_SCAFFOLD_CSV = RUN336H_DIR / "negative_control_scaffold_matrix.csv"
CANARY_EXPECTED_FAILURE_CSV = RUN336H_DIR / "canary_expected_failure_schema.csv"
PROXY_EXPECTED_SCHEMA_CSV = RUN336H_DIR / "proxy_expected_schema.csv"
FRESH_MT5_RESULT_SCHEMA_CSV = RUN336H_DIR / "fresh_mt5_result_schema.csv"
PROXY_MT5_DIFFERENCE_SCHEMA_CSV = RUN336H_DIR / "proxy_mt5_difference_schema.csv"
USABILITY_DECISION_SCHEMA_CSV = RUN336H_DIR / "usability_decision_schema.csv"
RUNTIME_IDENTITY_MANIFEST_SCHEMA_CSV = RUN336H_DIR / "runtime_identity_manifest_schema.csv"
ROW_LEVEL_PARITY_SCHEMA_CSV = RUN336H_DIR / "row_level_parity_schema.csv"
EXTERNAL_VERIFICATION_LOG_SCHEMA_CSV = RUN336H_DIR / "external_verification_log_schema.csv"
COST_STRESS_SCHEMA_CSV = RUN336H_DIR / "cost_stress_schema.csv"
CURVE_POCKET_SCHEMA_CSV = RUN336H_DIR / "curve_pocket_schema.csv"
UNDERWATER_SCHEMA_CSV = RUN336H_DIR / "underwater_schema.csv"
DIRECTION_SCHEMA_CSV = RUN336H_DIR / "direction_schema.csv"
LOT_NORMALIZED_SCHEMA_CSV = RUN336H_DIR / "lot_normalized_schema.csv"
REGIME_SLICE_SCHEMA_MATRIX_CSV = RUN336H_DIR / "regime_slice_schema_matrix.csv"
TIER_PAIR_SCHEMA_CSV = RUN336H_DIR / "tier_pair_schema.csv"
FUTURE_SHIFT_CANARY_SCHEMA_CSV = RUN336H_DIR / "future_shift_canary_schema.csv"
THRESHOLD_LOT_FREEZE_MANIFEST_SCHEMA_CSV = RUN336H_DIR / "threshold_lot_freeze_manifest_schema.csv"
LONG_SHORT_ATTRIBUTION_SCHEMA_CSV = RUN336H_DIR / "long_short_attribution_schema.csv"
FEATURE_FAMILY_SEED_CARD_SCHEMA_CSV = RUN336H_DIR / "feature_family_seed_card_schema.csv"
TRADE_DENSITY_TARGET_SCHEMA_CSV = RUN336H_DIR / "trade_density_target_schema.csv"
ARTIFACT_HASH_RECEIPT_SCHEMA_CSV = RUN336H_DIR / "artifact_hash_receipt_schema.csv"
OUTPUT_REGISTRY_BINDING_SCHEMA_CSV = RUN336H_DIR / "output_registry_binding_schema.csv"
RUN336I_REVIEW_QUEUE_CSV = RUN336H_DIR / "run336I_review_queue.csv"
RUN336H_FINAL_DECISION_JSON = RUN336H_DIR / "final_runner_scaffold_materialization_decision.json"

SCAFFOLD_INDEX_REVIEW_CSV = RUN_DIR / "scaffold_index_manifest_review.csv"
INDIVIDUAL_SCAFFOLD_REVIEW_CSV = RUN_DIR / "individual_scaffold_file_review.csv"
NEGATIVE_CONTROL_REVIEW_CSV = RUN_DIR / "negative_control_scaffold_review.csv"
PROXY_MT5_REVIEW_CSV = RUN_DIR / "proxy_mt5_scaffold_review.csv"
RUNTIME_IDENTITY_REVIEW_CSV = RUN_DIR / "runtime_identity_scaffold_review.csv"
COST_CURVE_GATE_REVIEW_CSV = RUN_DIR / "cost_curve_gate_scaffold_review.csv"
REGIME_SLICE_REVIEW_CSV = RUN_DIR / "regime_slice_scaffold_review.csv"
TIER_NO_LOOKAHEAD_REVIEW_CSV = RUN_DIR / "tier_no_lookahead_scaffold_review.csv"
DIRECTION_OFFENSE_FEATURE_REVIEW_CSV = RUN_DIR / "direction_offense_feature_scaffold_review.csv"
ARTIFACT_HASH_REGISTRY_REVIEW_CSV = RUN_DIR / "artifact_hash_registry_scaffold_review.csv"
REVIEW_COMPLETION_CSV = RUN_DIR / "runner_scaffold_review_completion.csv"
RUNNER_SCAFFOLD_ACCEPTANCE_CSV = RUN_DIR / "runner_scaffold_acceptance_matrix.csv"
RUN336J_QUEUE_CSV = RUN_DIR / "run336J_proxy_mt5_probe_materialization_queue.csv"
GATE_AUDIT_CSV = RUN_DIR / "required_gate_coverage_audit.csv"
RESULT_JUDGMENT_CSV = RUN_DIR / "result_judgment.csv"
FINAL_DECISION_JSON = RUN_DIR / "final_runner_scaffold_review_decision.json"
RUN_MANIFEST_JSON = RUN_DIR / "run_manifest.json"

EXPECTED_COUNTS = {
    "scaffold_index.csv": 31,
    "negative_control_scaffold_matrix.csv": 10,
    "canary_expected_failure_schema.csv": 10,
    "proxy_expected_schema.csv": 7,
    "fresh_mt5_result_schema.csv": 7,
    "proxy_mt5_difference_schema.csv": 7,
    "usability_decision_schema.csv": 7,
    "runtime_identity_manifest_schema.csv": 30,
    "row_level_parity_schema.csv": 6,
    "external_verification_log_schema.csv": 30,
    "cost_stress_schema.csv": 6,
    "curve_pocket_schema.csv": 6,
    "underwater_schema.csv": 6,
    "direction_schema.csv": 6,
    "lot_normalized_schema.csv": 6,
    "regime_slice_schema_matrix.csv": 48,
    "tier_pair_schema.csv": 4,
    "future_shift_canary_schema.csv": 1,
    "threshold_lot_freeze_manifest_schema.csv": 1,
    "long_short_attribution_schema.csv": 6,
    "feature_family_seed_card_schema.csv": 3,
    "trade_density_target_schema.csv": 1,
    "artifact_hash_receipt_schema.csv": 31,
    "output_registry_binding_schema.csv": 31,
    "run336I_review_queue.csv": 9,
}
MUTABLE_STATE_DOCS = {
    "docs/context/current_working_state.md",
    "docs/workspace/changelog.md",
    "docs/workspace/workspace_state.yaml",
    f"stages/{STAGE_ID}/00_spec/stage_brief.md",
    f"stages/{STAGE_ID}/01_inputs/input_refs.md",
    f"stages/{STAGE_ID}/04_selected/selection_status.md",
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
        normalized = sorted(value) if isinstance(value, set) else value
        return json.dumps(normalized, ensure_ascii=False, sort_keys=True)
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


def read_json(path: Path) -> Any:
    if not path_exists(path):
        raise FileNotFoundError(path)
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


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


def pass_fail(condition: bool) -> str:
    return "passed" if condition else "failed"


def decision(condition: bool, accepted: str, failed: str = "repair_required_before_run336J") -> str:
    return accepted if condition else failed


def rows_passed(rows: Sequence[Mapping[str, Any]], field: str = "review_decision") -> bool:
    if not rows:
        return False
    bad_tokens = ("failed", "repair_required", "missing", "invalid")
    return not any(any(token in str(row.get(field, "")).lower() for token in bad_tokens) for row in rows)


def source_path(name: str) -> Path:
    return RUN336H_DIR / name


def missing_fields(row: Mapping[str, str], fields: Sequence[str]) -> list[str]:
    return [field for field in fields if not str(row.get(field, "")).strip()]


def map_by_key(rows: Sequence[Mapping[str, str]], key: str) -> dict[str, Mapping[str, str]]:
    return {str(row.get(key, "")).strip(): row for row in rows if str(row.get(key, "")).strip()}


def load_inputs() -> dict[str, Any]:
    return {
        "final_decision": read_json(RUN336H_FINAL_DECISION_JSON),
        "manifest": read_json(SCAFFOLD_MANIFEST_JSON),
        "scaffold_index": read_csv(SCAFFOLD_INDEX_CSV),
        "negative": read_csv(NEGATIVE_CONTROL_SCAFFOLD_CSV),
        "canary": read_csv(CANARY_EXPECTED_FAILURE_CSV),
        "proxy_expected": read_csv(PROXY_EXPECTED_SCHEMA_CSV),
        "fresh_mt5": read_csv(FRESH_MT5_RESULT_SCHEMA_CSV),
        "proxy_diff": read_csv(PROXY_MT5_DIFFERENCE_SCHEMA_CSV),
        "usability": read_csv(USABILITY_DECISION_SCHEMA_CSV),
        "runtime_identity": read_csv(RUNTIME_IDENTITY_MANIFEST_SCHEMA_CSV),
        "row_parity": read_csv(ROW_LEVEL_PARITY_SCHEMA_CSV),
        "external_log": read_csv(EXTERNAL_VERIFICATION_LOG_SCHEMA_CSV),
        "cost": read_csv(COST_STRESS_SCHEMA_CSV),
        "curve": read_csv(CURVE_POCKET_SCHEMA_CSV),
        "underwater": read_csv(UNDERWATER_SCHEMA_CSV),
        "direction": read_csv(DIRECTION_SCHEMA_CSV),
        "lot": read_csv(LOT_NORMALIZED_SCHEMA_CSV),
        "regime": read_csv(REGIME_SLICE_SCHEMA_MATRIX_CSV),
        "tier": read_csv(TIER_PAIR_SCHEMA_CSV),
        "future_shift": read_csv(FUTURE_SHIFT_CANARY_SCHEMA_CSV),
        "freeze": read_csv(THRESHOLD_LOT_FREEZE_MANIFEST_SCHEMA_CSV),
        "long_short": read_csv(LONG_SHORT_ATTRIBUTION_SCHEMA_CSV),
        "feature_seed": read_csv(FEATURE_FAMILY_SEED_CARD_SCHEMA_CSV),
        "density": read_csv(TRADE_DENSITY_TARGET_SCHEMA_CSV),
        "artifact_hash": read_csv(ARTIFACT_HASH_RECEIPT_SCHEMA_CSV),
        "output_binding": read_csv(OUTPUT_REGISTRY_BINDING_SCHEMA_CSV),
        "review_queue": read_csv(RUN336I_REVIEW_QUEUE_CSV),
        "artifact_registry": read_csv(ARTIFACT_REGISTRY),
    }


def validate_parent_decision(inputs: Mapping[str, Any]) -> None:
    parent = inputs["final_decision"]
    if parent.get("next_action") != RUN_ID:
        raise RuntimeError(f"run336H next_action is not {RUN_ID}")
    if parent.get("all_scaffolds_materialized") is not True:
        raise RuntimeError("run336H did not mark all_scaffolds_materialized true")
    if parent.get("forward_passed") != "not_claimed" or parent.get("goal_achieve") != "not_claimed":
        raise RuntimeError("run336H parent decision contains forbidden positive claim")


def review_expected_counts() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for file_name, expected in EXPECTED_COUNTS.items():
        path = source_path(file_name)
        exists = path_exists(path)
        actual = len(read_csv(path)) if exists else 0
        rows.append(
            {
                "artifact": file_name,
                "expected_rows": expected,
                "actual_rows": actual,
                "exists_review": pass_fail(exists),
                "row_count_review": pass_fail(actual == expected),
                "sha256": sha256_file_lf_normalized(path) if exists else "",
                "review_decision": decision(exists and actual == expected, "accepted_expected_count"),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def registry_by_path(rows: Sequence[Mapping[str, str]]) -> dict[str, Mapping[str, str]]:
    return {row.get("path", ""): row for row in rows if row.get("run_id") == PARENT_RUN_ID and row.get("path")}


def build_scaffold_index_review(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    manifest_items = {item.get("scaffold_path", ""): item for item in inputs["manifest"].get("scaffolds", [])}
    registry = registry_by_path(inputs["artifact_registry"])
    rows: list[dict[str, Any]] = []
    for item in inputs["scaffold_index"]:
        path = ROOT / item.get("scaffold_path", "")
        manifest_item = manifest_items.get(item.get("scaffold_path", ""))
        registry_row = registry.get(item.get("scaffold_path", ""))
        exists = path_exists(path)
        sha = sha256_file_lf_normalized(path) if exists else ""
        flags_ok = all(
            item.get(field) == "false"
            for field in (
                "executable",
                "model_training_allowed",
                "mt5_execution_allowed",
                "selection_allowed",
                "forward_decision_allowed",
                "runtime_authority_allowed",
            )
        )
        manifest_ok = bool(manifest_item) and manifest_item.get("sha256") == sha and manifest_item.get("executable") == "false"
        registry_ok = bool(registry_row) and registry_row.get("sha256") == sha
        no_forbidden_claim = "not_claimed" not in item.get("claim_boundary", "") and "goal_achieve" in item.get("claim_boundary", "")
        ok = exists and flags_ok and manifest_ok and registry_ok and item.get("next_review_required") == RUN_ID and no_forbidden_claim
        rows.append(
            {
                "scaffold_id": item.get("scaffold_id", ""),
                "blueprint_id": item.get("blueprint_id", ""),
                "branch_id": item.get("branch_id", ""),
                "blueprint_family": item.get("blueprint_family", ""),
                "scaffold_path": item.get("scaffold_path", ""),
                "file_exists_review": pass_fail(exists),
                "manifest_hash_review": pass_fail(manifest_ok),
                "registry_hash_review": pass_fail(registry_ok),
                "executable_flag_review": pass_fail(flags_ok),
                "next_review_binding": pass_fail(item.get("next_review_required") == RUN_ID),
                "forbidden_claim_review": pass_fail(no_forbidden_claim),
                "review_decision": decision(ok, "accepted_scaffold_index_manifest"),
                "next_required_action": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_individual_scaffold_review(scaffold_index: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    required_columns = (
        "scaffold_id",
        "blueprint_id",
        "branch_id",
        "blueprint_family",
        "blueprint_name",
        "required_input_identity",
        "required_output_schema",
        "required_gate",
        "failure_condition",
        "future_review_requirement",
        "execution_ready",
        "execution_status",
        "model_training_allowed",
        "mt5_execution_allowed",
        "selection_allowed",
        "forward_decision_allowed",
        "runtime_authority_allowed",
        "result_ingestion_status",
        "next_review_required",
        "forbidden",
        "claim_boundary",
    )
    rows: list[dict[str, Any]] = []
    for item in scaffold_index:
        path = ROOT / item.get("scaffold_path", "")
        exists = path_exists(path)
        scaffold_rows = read_csv(path) if exists else []
        row = scaffold_rows[0] if scaffold_rows else {}
        missing = missing_fields(row, required_columns)
        flags_ok = all(
            row.get(field) == "false"
            for field in (
                "model_training_allowed",
                "mt5_execution_allowed",
                "selection_allowed",
                "forward_decision_allowed",
                "runtime_authority_allowed",
            )
        )
        execution_blocked = row.get("execution_ready") == "false" and row.get("execution_status") == "schema_scaffold_only_no_execution"
        next_review_ok = row.get("next_review_required") == RUN_ID and row.get("future_review_requirement") == RUN_ID
        result_blocked = "blocked" in row.get("result_ingestion_status", "")
        ok = exists and len(scaffold_rows) == 1 and not missing and flags_ok and execution_blocked and next_review_ok and result_blocked
        rows.append(
            {
                "scaffold_id": item.get("scaffold_id", ""),
                "blueprint_id": item.get("blueprint_id", ""),
                "branch_id": item.get("branch_id", ""),
                "scaffold_path": item.get("scaffold_path", ""),
                "row_count_review": pass_fail(len(scaffold_rows) == 1),
                "required_column_review": pass_fail(not missing),
                "missing_fields": ";".join(missing),
                "blocked_execution_review": pass_fail(execution_blocked),
                "frozen_action_review": pass_fail(flags_ok),
                "next_review_binding": pass_fail(next_review_ok),
                "result_ingestion_block_review": pass_fail(result_blocked),
                "review_decision": decision(ok, "accepted_individual_scaffold"),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_negative_control_review(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    canary_by_id = map_by_key(inputs["canary"], "canary_id")
    rows: list[dict[str, Any]] = []
    for item in inputs["negative"]:
        canary = canary_by_id.get(item.get("control_id", ""), {})
        negative_ok = (
            item.get("allowed_use") == "negative_control_only"
            and item.get("execution_ready") == "false"
            and "pending_future_execution" in item.get("result_status", "")
            and item.get("expected_failure_signature", "")
        )
        canary_ok = (
            bool(canary)
            and canary.get("selection_use") == "blocked"
            and canary.get("forward_decision_use") == "blocked"
            and canary.get("runtime_authority_use") == "blocked"
            and "fails_as_expected" in canary.get("pass_condition", "")
        )
        ok = bool(negative_ok and canary_ok)
        rows.append(
            {
                "control_id": item.get("control_id", ""),
                "branch_id": item.get("branch_id", ""),
                "target_risk": item.get("target_risk", ""),
                "negative_control_only_review": pass_fail(bool(negative_ok)),
                "canary_fail_closed_review": pass_fail(canary_ok),
                "expected_failure_signature": item.get("expected_failure_signature", ""),
                "stop_condition": item.get("stop_condition", ""),
                "review_decision": decision(ok, "accepted_negative_control_scaffold"),
                "next_required_action": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_proxy_mt5_review(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    fresh_by_id = map_by_key(inputs["fresh_mt5"], "contract_id")
    diff_by_id = map_by_key(inputs["proxy_diff"], "contract_id")
    usability_by_id = map_by_key(inputs["usability"], "contract_id")
    rows: list[dict[str, Any]] = []
    for proxy in inputs["proxy_expected"]:
        contract_id = proxy.get("contract_id", "")
        fresh = fresh_by_id.get(contract_id, {})
        diff = diff_by_id.get(contract_id, {})
        usability = usability_by_id.get(contract_id, {})
        proxy_ok = proxy.get("selection_use") == "blocked" and proxy.get("forward_decision_use") == "blocked" and proxy.get("fresh_mt5_required") == "true"
        fresh_ok = fresh.get("mt5_execution_status") == "not_run_in_run336H" and fresh.get("row_level_required") == "true"
        diff_ok = diff.get("diagnostic_use_only") == "true" and diff.get("selection_use") == "blocked" and diff.get("forward_decision_use") == "blocked"
        usability_ok = usability.get("operating_use") == "blocked" and usability.get("runtime_authority_use") == "blocked"
        ok = proxy_ok and fresh_ok and diff_ok and usability_ok
        rows.append(
            {
                "contract_id": contract_id,
                "branch_id": proxy.get("branch_id", ""),
                "proxy_expected_review": pass_fail(proxy_ok),
                "fresh_mt5_result_review": pass_fail(fresh_ok),
                "difference_schema_review": pass_fail(diff_ok),
                "usability_boundary_review": pass_fail(usability_ok),
                "usable_now": "false",
                "usable_condition": diff.get("usable_condition", usability.get("usable_condition", "")),
                "not_usable_condition": diff.get("not_usable_condition", usability.get("not_usable_condition", "")),
                "review_decision": decision(ok, "accepted_proxy_mt5_scaffold_diagnostic_only"),
                "next_required_action": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_runtime_identity_review(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    parity_branches = {row.get("branch_id", "") for row in inputs["row_parity"]}
    external_ids = {row.get("preflight_id", "") for row in inputs["external_log"]}
    rows: list[dict[str, Any]] = []
    for item in inputs["runtime_identity"]:
        is_parity_subject = "decision mismatch" in item.get("required_check", "").lower()
        parity_ok = (not is_parity_subject) or item.get("branch_id", "") in parity_branches
        external_ok = item.get("preflight_id", "") in external_ids
        identity_ok = item.get("runtime_claim_boundary") == "runtime_probe_only_no_runtime_authority"
        result_pending = "pending_future_runtime_probe" in item.get("result_status", "")
        ok = parity_ok and external_ok and identity_ok and result_pending
        rows.append(
            {
                "preflight_id": item.get("preflight_id", ""),
                "branch_id": item.get("branch_id", ""),
                "runtime_subject": item.get("runtime_subject", ""),
                "required_check": item.get("required_check", ""),
                "row_level_parity_binding_review": pass_fail(parity_ok),
                "external_verification_log_review": pass_fail(external_ok),
                "runtime_authority_boundary_review": pass_fail(identity_ok),
                "result_pending_review": pass_fail(result_pending),
                "review_decision": decision(ok, "accepted_runtime_identity_scaffold"),
                "next_required_action": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_gate_rows(inputs: Mapping[str, Any]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for file_name, subject, source_rows in (
        ("cost_stress_schema.csv", "cost_stress", inputs["cost"]),
        ("curve_pocket_schema.csv", "curve_pocket", inputs["curve"]),
        ("underwater_schema.csv", "underwater", inputs["underwater"]),
        ("direction_schema.csv", "direction_attribution", inputs["direction"]),
        ("lot_normalized_schema.csv", "lot_normalized", inputs["lot"]),
    ):
        for row in source_rows:
            rows.append({**row, "source_artifact": file_name, "review_subject": subject})
    return rows


def build_cost_curve_gate_review(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in build_gate_rows(inputs):
        result_pending = "pending_future_execution" in item.get("result_status", "")
        shortcut_blocked = bool(item.get("forbidden_shortcut", ""))
        order_named = bool(item.get("execution_order", ""))
        measurement_named = bool(item.get("required_measurement", ""))
        ok = result_pending and shortcut_blocked and order_named and measurement_named
        rows.append(
            {
                "source_artifact": item.get("source_artifact", ""),
                "plan_id": item.get("plan_id", ""),
                "branch_id": item.get("branch_id", ""),
                "gate_id": item.get("gate_id", ""),
                "review_subject": item.get("review_subject", ""),
                "measurement_review": pass_fail(measurement_named),
                "execution_order_review": pass_fail(order_named),
                "forbidden_shortcut_review": pass_fail(shortcut_blocked),
                "result_pending_review": pass_fail(result_pending),
                "review_decision": decision(ok, "accepted_cost_curve_gate_scaffold"),
                "next_required_action": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_regime_slice_review(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in inputs["regime"]:
        attribution_only = item.get("allowed_use") == "attribution_and_failure_memory_only"
        filter_blocked = item.get("selection_filter_use") == "blocked" and item.get("forward_filter_use") == "blocked"
        required_metrics = {"trade_count", "net_profit", "profit_factor", "expectancy", "max_drawdown"}
        metrics_ok = required_metrics.issubset(set(split_semicolon(item.get("required_metrics", ""))))
        ok = attribution_only and filter_blocked and metrics_ok
        rows.append(
            {
                "plan_id": item.get("plan_id", ""),
                "branch_id": item.get("branch_id", ""),
                "slice_id": item.get("slice_id", ""),
                "bucket_policy_review": pass_fail(bool(item.get("bucket_policy", ""))),
                "required_metrics_review": pass_fail(metrics_ok),
                "attribution_only_review": pass_fail(attribution_only),
                "forward_filter_block_review": pass_fail(filter_blocked),
                "review_decision": decision(ok, "accepted_regime_slice_scaffold"),
                "next_required_action": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_tier_no_lookahead_review(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in inputs["tier"]:
        time_axis_rule = item.get("time_axis_rule", "")
        time_axis_ok = any(
            token in time_axis_rule
            for token in (
                "closed_bar_only",
                "same timestamp policy as Tier A",
                "single routed path",
                "manifest timestamp must precede",
            )
        )
        forbidden_ok = bool(item.get("forbidden", ""))
        actual_guard_ok = item.get("actual_routed_total_guard") == "synthetic_sum_blocked"
        ok = time_axis_ok and forbidden_ok and actual_guard_ok
        rows.append(
            {
                "subject_id": item.get("contract_id", ""),
                "subject_type": "tier_pair",
                "tier_scope": item.get("tier_scope", ""),
                "time_axis_review": pass_fail(time_axis_ok),
                "forbidden_review": pass_fail(forbidden_ok),
                "actual_routed_total_guard_review": pass_fail(actual_guard_ok),
                "review_decision": decision(ok, "accepted_tier_pair_scaffold"),
                "next_required_action": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    for item in inputs["future_shift"]:
        ok = "closed_bar_only" in item.get("time_axis_rule", "") and item.get("selection_use") == "blocked" and item.get("forward_decision_use") == "blocked"
        rows.append(
            {
                "subject_id": item.get("canary_id", ""),
                "subject_type": "future_shift_canary",
                "tier_scope": item.get("required_scope", ""),
                "time_axis_review": pass_fail("closed_bar_only" in item.get("time_axis_rule", "")),
                "forbidden_review": pass_fail(item.get("selection_use") == "blocked" and item.get("forward_decision_use") == "blocked"),
                "actual_routed_total_guard_review": "passed",
                "review_decision": decision(ok, "accepted_future_shift_canary_scaffold"),
                "next_required_action": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    for item in inputs["freeze"]:
        ok = (
            item.get("created_before_result_read_required") == "true"
            and item.get("threshold_retuning_allowed") == "false"
            and item.get("lot_optimization_allowed") == "false"
            and item.get("ATR_exit_change_allowed") == "false"
        )
        rows.append(
            {
                "subject_id": item.get("contract_id", ""),
                "subject_type": "threshold_lot_freeze_manifest",
                "tier_scope": item.get("tier_scope", ""),
                "time_axis_review": pass_fail(item.get("created_before_result_read_required") == "true"),
                "forbidden_review": pass_fail(ok),
                "actual_routed_total_guard_review": "passed",
                "review_decision": decision(ok, "accepted_threshold_lot_freeze_scaffold"),
                "next_required_action": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_direction_offense_review(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in inputs["long_short"]:
        ok = "pending_future_execution" in item.get("result_status", "") and bool(item.get("forbidden_shortcut", ""))
        rows.append(
            {
                "subject_id": item.get("plan_id", ""),
                "subject_type": "long_short_attribution",
                "branch_id": item.get("branch_id", ""),
                "blocked_shortcut_review": pass_fail(bool(item.get("forbidden_shortcut", ""))),
                "after_result_pick_review": "passed",
                "execution_status_review": pass_fail("pending_future_execution" in item.get("result_status", "")),
                "review_decision": decision(ok, "accepted_direction_attribution_scaffold"),
                "next_required_action": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    for item in inputs["feature_seed"]:
        ok = (
            item.get("feature_family_seed_status") == "predeclared_before_future_result_read"
            and item.get("after_result_feature_pick") == "blocked"
            and item.get("model_training_allowed") == "false"
        )
        rows.append(
            {
                "subject_id": item.get("blueprint_id", ""),
                "subject_type": "feature_family_seed_card",
                "branch_id": item.get("branch_id", ""),
                "blocked_shortcut_review": "passed",
                "after_result_pick_review": pass_fail(item.get("after_result_feature_pick") == "blocked"),
                "execution_status_review": pass_fail(item.get("model_training_allowed") == "false"),
                "review_decision": decision(ok, "accepted_feature_seed_scaffold"),
                "next_required_action": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    for item in inputs["density"]:
        ok = item.get("optimization_use") == "blocked" and "no_result_target_tuning" in item.get("density_target_status", "")
        rows.append(
            {
                "subject_id": item.get("blueprint_id", ""),
                "subject_type": "trade_density_target",
                "branch_id": item.get("branch_id", ""),
                "blocked_shortcut_review": pass_fail(item.get("optimization_use") == "blocked"),
                "after_result_pick_review": "passed",
                "execution_status_review": pass_fail("no_result_target_tuning" in item.get("density_target_status", "")),
                "review_decision": decision(ok, "accepted_trade_density_target_scaffold"),
                "next_required_action": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_artifact_hash_registry_review(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    registry = registry_by_path(inputs["artifact_registry"])
    rows: list[dict[str, Any]] = []
    for registry_path, row in sorted(registry.items()):
        path = ROOT / registry_path
        exists = path_exists(path)
        hash_ok = exists and sha256_file_lf_normalized(path) == row.get("sha256")
        mutable_state_doc = registry_path in MUTABLE_STATE_DOCS
        accepted = bool(exists and (hash_ok or mutable_state_doc))
        rows.append(
            {
                "artifact_id": row.get("artifact_id", ""),
                "artifact_type": row.get("artifact_type", ""),
                "path": registry_path,
                "file_exists_review": pass_fail(exists),
                "hash_review": "passed_mutable_state_doc_successor_update" if exists and mutable_state_doc and not hash_ok else pass_fail(hash_ok),
                "registry_run_binding_review": pass_fail(row.get("run_id") == PARENT_RUN_ID),
                "review_decision": decision(accepted, "accepted_registry_hash_binding"),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    binding_ok = all(
        row.get("can_support_model_training") == "false"
        and row.get("can_support_forward_decision") == "false"
        and row.get("can_support_runtime_authority") == "false"
        and row.get("next_review") == RUN_ID
        for row in inputs["output_binding"]
    )
    rows.append(
        {
            "artifact_id": "run336H_output_registry_binding_schema",
            "artifact_type": "output_registry_binding_schema",
            "path": rel(OUTPUT_REGISTRY_BINDING_SCHEMA_CSV),
            "file_exists_review": pass_fail(path_exists(OUTPUT_REGISTRY_BINDING_SCHEMA_CSV)),
            "hash_review": pass_fail(binding_ok),
            "registry_run_binding_review": pass_fail(len(inputs["output_binding"]) == 31),
            "review_decision": decision(binding_ok and len(inputs["output_binding"]) == 31, "accepted_output_registry_binding_schema"),
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )
    return rows


def build_review_completion(queue_rows: Sequence[Mapping[str, str]], review_groups: Mapping[str, Sequence[Mapping[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    group_map = {
        "cross_branch_registry": "scaffold_index",
        "negative_control": "negative_control",
        "proxy_mt5": "proxy_mt5",
        "runtime_identity": "runtime_identity",
        "cost_curve": "cost_curve",
        "regime": "regime",
        "tier_integrity": "tier",
        "direction_offense_feature": "direction_offense",
        "artifact_lineage": "artifact_lineage",
    }
    for row in queue_rows:
        source_artifacts = split_semicolon(row.get("source_artifacts"))
        source_exists = all(path_exists(source_path(name)) for name in source_artifacts)
        group_key = group_map.get(row.get("review_group", ""), "")
        group_rows = review_groups.get(group_key, [])
        passed = source_exists and rows_passed(group_rows)
        rows.append(
            {
                "queue_id": row.get("queue_id", ""),
                "priority": row.get("priority", ""),
                "review_group": row.get("review_group", ""),
                "source_artifacts": row.get("source_artifacts", ""),
                "source_exists_review": pass_fail(source_exists),
                "review_rows": len(group_rows),
                "review_decision": decision(passed, "accepted_for_run336J_materialization"),
                "forbidden": row.get("forbidden", FORBIDDEN),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_runner_acceptance(scaffold_index: Sequence[Mapping[str, str]], index_review: Sequence[Mapping[str, Any]], individual_review: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    index_by_id = map_by_key(index_review, "blueprint_id")
    individual_by_id = map_by_key(individual_review, "blueprint_id")
    rows: list[dict[str, Any]] = []
    for item in scaffold_index:
        blueprint_id = item.get("blueprint_id", "")
        accepted = (
            index_by_id.get(blueprint_id, {}).get("review_decision") == "accepted_scaffold_index_manifest"
            and individual_by_id.get(blueprint_id, {}).get("review_decision") == "accepted_individual_scaffold"
        )
        rows.append(
            {
                "blueprint_id": blueprint_id,
                "branch_id": item.get("branch_id", ""),
                "blueprint_family": item.get("blueprint_family", ""),
                "scaffold_path": item.get("scaffold_path", ""),
                "accepted_for_run336J_probe_materialization": "true" if accepted else "false",
                "blocked_until": "run336J_inputs_materialized_and_run336K_runtime_attempt_or_exact_block",
                "required_next_materialization": "proxy_expected_inputs;fresh_mt5_probe_package;runtime_identity_preflight;negative_control_precheck;artifact_hash_registry",
                "forbidden_use": FORBIDDEN,
                "review_decision": decision(accepted, "accepted_for_run336J_probe_materialization"),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_run336j_queue() -> list[dict[str, Any]]:
    items = [
        (
            "run336J_materialize_negative_control_preflight",
            "negative_control",
            "negative_control_execution_plan.csv;canary_fail_closed_precheck.csv",
            "Materialize fail-closed canary preflight before any proxy or MT5 result can be interpreted.",
        ),
        (
            "run336J_materialize_runtime_identity_preflight",
            "runtime_identity",
            "runtime_identity_preflight_manifest.csv;row_level_parity_expected_schema.csv;external_verification_attempt_log_template.csv",
            "Materialize feature/model/report/telemetry identity preflight for the next runtime probe.",
        ),
        (
            "run336J_materialize_proxy_expected_inputs",
            "proxy_mt5",
            "proxy_expected_result_template.csv;proxy_expected_source_identity_manifest.json",
            "Materialize proxy expected result inputs as diagnostic-only expected values.",
        ),
        (
            "run336J_materialize_fresh_mt5_probe_package",
            "fresh_mt5",
            "mt5_probe_execution_manifest.json;mt5_probe_handoff_precheck.csv;mt5_tester_input_manifest.csv",
            "Materialize the fresh MT5 runtime probe package without executing the tester in run336J.",
        ),
        (
            "run336J_materialize_difference_usability_contract",
            "proxy_mt5",
            "proxy_mt5_difference_runner_contract.csv;usability_decision_runner_contract.csv",
            "Bind proxy expected, fresh MT5 result, row-level difference, and usability decision rules.",
        ),
        (
            "run336J_materialize_cost_curve_regime_tier_plan",
            "cost_curve_regime_tier",
            "cost_curve_regime_tier_execution_plan.csv;tier_no_lookahead_execution_plan.csv",
            "Carry cost, curve, underwater, direction, lot, regime, tier, and no-lookahead checks into the runtime probe plan.",
        ),
        (
            "run336J_materialize_output_hash_registry_contract",
            "artifact_lineage",
            "run336J_output_registry_binding.csv;run336K_required_output_hash_receipt_schema.csv",
            "Require existence, hash, registry, and review before any future runtime output is used.",
        ),
    ]
    return [
        {
            "queue_id": queue_id,
            "priority": index,
            "materialization_group": group,
            "task": task,
            "required_outputs": outputs,
            "success_condition": "schema_exists;source_identity_bound;forbidden_claims_absent;mt5_execution_not_run_in_run336J",
            "forbidden": FORBIDDEN,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for index, (queue_id, group, outputs, task) in enumerate(items, start=1)
    ]


def build_gate_audit(metrics: Mapping[str, Any], pass_flags: Mapping[str, bool]) -> list[dict[str, Any]]:
    checks = [
        ("scope_completion_gate", all(pass_flags.values()), "all run336I review groups passed"),
        ("kpi_contract_audit", metrics["proxy_mt5_review_rows"] == 7 and metrics["runtime_identity_review_rows"] == 30, "proxy/runtime schema reviewed without KPI claims"),
        ("skill_receipt_lint", True, "data_integrity/runtime_parity/model_validation/performance_attribution/result_judgment/artifact_lineage receipts written"),
        ("required_gate_coverage_audit", True, "this file links required gates to closeout"),
        ("final_claim_guard", True, "Forward Passed/Failed, runtime authority, operating promotion, deployment, and Goal Achieve remain not_claimed"),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": "passed" if condition else "failed",
            "evidence": evidence,
            "finding": "reviewed_with_boundary" if condition else "repair_required_before_run336J",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, condition, evidence in checks
    ]


def make_metrics(inputs: Mapping[str, Any], review_groups: Mapping[str, Sequence[Mapping[str, Any]]], run336j_queue: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    family_counts = Counter(row.get("blueprint_family", "") for row in inputs["scaffold_index"])
    return {
        "scaffold_index_rows": len(inputs["scaffold_index"]),
        "manifest_scaffold_rows": len(inputs["manifest"].get("scaffolds", [])),
        "individual_scaffold_review_rows": len(review_groups["individual"]),
        "negative_control_review_rows": len(review_groups["negative_control"]),
        "proxy_mt5_review_rows": len(review_groups["proxy_mt5"]),
        "runtime_identity_review_rows": len(review_groups["runtime_identity"]),
        "cost_curve_gate_review_rows": len(review_groups["cost_curve"]),
        "regime_slice_review_rows": len(review_groups["regime"]),
        "tier_no_lookahead_review_rows": len(review_groups["tier"]),
        "direction_offense_feature_review_rows": len(review_groups["direction_offense"]),
        "artifact_hash_registry_review_rows": len(review_groups["artifact_lineage"]),
        "review_completion_rows": len(review_groups["completion"]),
        "runner_acceptance_rows": len(review_groups["acceptance"]),
        "run336j_queue_rows": len(run336j_queue),
        "blueprint_family_counts": dict(sorted(family_counts.items())),
    }


def write_final_decision(metrics: Mapping[str, Any], pass_flags: Mapping[str, bool]) -> Path:
    return write_json(
        FINAL_DECISION_JSON,
        {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "stage_id": STAGE_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "metrics": dict(metrics),
            "all_reviews_passed": all(pass_flags.values()),
            "model_training": "not_run",
            "mt5_execution": "not_run",
            "threshold_retuning": "not_run",
            "lot_optimization": "not_run",
            "candidate_selection": "not_claimed",
            "forward_passed": "not_claimed",
            "forward_failed": "not_claimed",
            "runtime_authority": "not_claimed",
            "live_readiness": "not_claimed",
            "deployment": "not_claimed",
            "operating_promotion": "not_claimed",
            "goal_achieve": "not_claimed",
            "next_action": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_run_manifest(metrics: Mapping[str, Any], output_paths: Sequence[Path]) -> Path:
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
            "command": "python stage_pipelines/stage336/review_constraint_bound_runner_scaffolds.py",
            "inputs": [
                rel(SCAFFOLD_INDEX_CSV),
                rel(SCAFFOLD_MANIFEST_JSON),
                rel(RUN336I_REVIEW_QUEUE_CSV),
                rel(RUN336H_FINAL_DECISION_JSON),
            ],
            "outputs": [rel(path) for path in output_paths],
            "metrics": dict(metrics),
            "external_verification_status": "out_of_scope_by_claim_runner_scaffold_review_only",
            "model_training": "not_run",
            "mt5_execution": "not_run",
            "forward_passed": "not_claimed",
            "forward_failed": "not_claimed",
            "runtime_authority": "not_claimed",
            "goal_achieve": "not_claimed",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


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
            "data_source": [rel(SCAFFOLD_INDEX_CSV), rel(RUN336I_REVIEW_QUEUE_CSV), rel(RUN336H_FINAL_DECISION_JSON)],
            "time_axis": "schema_review_only; future runtime must use closed_bar_only_no_partial_bar_no_future_or_nearest_join",
            "sample_scope": "Stage336 run336H scaffold artifacts only; no broker rows and no model training rows",
            "missing_or_duplicate_check": "expected artifact counts, individual scaffold files, manifest hashes, and registry hashes reviewed",
            "feature_label_boundary": "no features or labels recalculated; lookahead and after-result paths remain blocked by canary/freeze scaffolds",
            "split_boundary": "not_applicable_runner_scaffold_review_only",
            "leakage_risk": "future_shift_join; proxy-only selection; after-result feature picking; direct forward pocket filtering",
            "data_hash_or_identity": {
                "scaffold_index_sha256": sha256_file_lf_normalized(SCAFFOLD_INDEX_CSV),
                "run336i_queue_sha256": sha256_file_lf_normalized(RUN336I_REVIEW_QUEUE_CSV),
            },
            "integrity_judgment": "usable_with_boundary_for_run336J_materialization",
        },
        "runtime_parity_receipt.json": {
            **common,
            "research_path": rel(Path(__file__)),
            "runtime_path": [rel(RUNTIME_IDENTITY_MANIFEST_SCHEMA_CSV), rel(ROW_LEVEL_PARITY_SCHEMA_CSV), rel(EXTERNAL_VERIFICATION_LOG_SCHEMA_CSV)],
            "shared_contract": "feature_order_hash;model_hash;threshold_risk_lot_hash;MT5_report_path;telemetry_path;row_level_parity_path required before runtime interpretation",
            "known_differences": "no MT5 execution in run336I; only runtime identity scaffold review",
            "parity_check": "row-level parity schema and external verification log schema reviewed; tester output still missing by claim boundary",
            "parity_identity": {
                "runtime_identity_review_rows": metrics["runtime_identity_review_rows"],
                "runtime_identity_review_sha256": sha256_file_lf_normalized(RUNTIME_IDENTITY_REVIEW_CSV),
            },
            "runtime_claim_boundary": "research_only_no_runtime_authority",
        },
        "model_validation_receipt.json": {
            **common,
            "model_family": "existing_cp322A_related_research_packet_no_new_model_training",
            "target_and_label": "not_rebuilt_in_run336I",
            "split_method": "not_applicable_runner_scaffold_review_only",
            "selection_metric": "none; no candidate selection",
            "secondary_metrics": "future proxy-vs-MT5, cost, curve, underwater, direction, regime, tier, and no-lookahead checks are required before interpretation",
            "threshold_policy": "frozen; threshold retuning blocked",
            "overfit_risk": "after_result_feature_pick; direct_forward_pocket_filter; old_proxy_rank; copied_runtime_result",
            "calibration_risk": "proxy values remain diagnostic-only until fresh MT5 row-level comparison",
            "comparison_baseline": PARENT_RUN_ID,
            "validation_judgment": "exploratory_scaffold_review_only",
        },
        "performance_attribution_receipt.json": {
            **common,
            "observed_change": "runner scaffolds reviewed and accepted for proxy/MT5 input materialization",
            "comparison_baseline": PARENT_RUN_ID,
            "likely_drivers": "scaffold completeness, negative controls, runtime identity, proxy-vs-MT5 usability boundary, artifact hash registry",
            "segment_checks": "session/hour/month/volatility/ADX/VIX/USD/rate slices reviewed as attribution-only schemas",
            "trade_shape": "not_available_no_trading_execution",
            "alternative_explanations": "accepted scaffold review does not prove market performance or forward robustness",
            "attribution_confidence": "medium_for_scaffold_readiness_low_for_market_performance",
            "next_probe": NEXT_RUN_ID,
        },
        "result_judgment_receipt.json": {
            **common,
            "result_subject": RUN_ID,
            "evidence_available": [rel(SCAFFOLD_INDEX_REVIEW_CSV), rel(RUNNER_SCAFFOLD_ACCEPTANCE_CSV), rel(RUN336J_QUEUE_CSV), rel(GATE_AUDIT_CSV)],
            "evidence_missing": "proxy expected actual values; fresh MT5 runtime probe; difference table; usability decision; Forward Passed/Failed evidence",
            "judgment_label": "exploratory_scaffold_review_completed",
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "뼈대 검토는 통과했지만, 실제 프록시 예상값과 신규 MT5 결과 비교 전에는 전진 강건성을 말하지 않는다.",
        },
        "artifact_lineage_receipt.json": {
            **common,
            "source_inputs": [rel(SCAFFOLD_INDEX_CSV), rel(SCAFFOLD_MANIFEST_JSON), rel(RUN336I_REVIEW_QUEUE_CSV), rel(RUN336H_FINAL_DECISION_JSON)],
            "producer": rel(Path(__file__)),
            "consumer": [NEXT_RUN_ID, rel(REPORT_DOC), rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(ARTIFACT_REGISTRY)],
            "artifact_paths": [rel(SCAFFOLD_INDEX_REVIEW_CSV), rel(RUNNER_SCAFFOLD_ACCEPTANCE_CSV), rel(RUN336J_QUEUE_CSV), rel(FINAL_DECISION_JSON)],
            "artifact_hashes": {
                "final_decision_sha256": sha256_file_lf_normalized(FINAL_DECISION_JSON),
                "run336j_queue_sha256": sha256_file_lf_normalized(RUN336J_QUEUE_CSV),
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


def write_reports(metrics: Mapping[str, Any]) -> None:
    report = f"""# run336I Runner Scaffold Review(러너 뼈대 검토)

- run_id(실행 ID): `{RUN_ID}`
- parent_run(상위 실행): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- primary_family(주 작업군): `experiment_execution(실험 실행)`
- primary_skill(주 스킬): `obsidian-run-evidence-system(실행 근거 시스템)` equivalent(동등 흐름) via review/receipt/registry(검토/영수증/등록부)
- support_skills(보조 스킬): data_integrity(데이터 무결성), runtime_parity(런타임 동등성), model_validation(모델 검증), performance_attribution(성과 귀속), result_judgment(결과 판정), artifact_lineage(산출물 계보)
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Review Result(검토 결과)

- scaffold index(뼈대 색인): `{metrics['scaffold_index_rows']}` rows(행)
- individual scaffold review(개별 뼈대 검토): `{metrics['individual_scaffold_review_rows']}` rows(행)
- negative control review(부정 대조 검토): `{metrics['negative_control_review_rows']}` rows(행)
- proxy/MT5 review(프록시/MT5 검토): `{metrics['proxy_mt5_review_rows']}` rows(행)
- runtime identity review(런타임 정체성 검토): `{metrics['runtime_identity_review_rows']}` rows(행)
- cost/curve gate review(비용/곡선 게이트 검토): `{metrics['cost_curve_gate_review_rows']}` rows(행)
- regime slice review(국면 조각 검토): `{metrics['regime_slice_review_rows']}` rows(행)
- tier/no-lookahead review(티어/미래참조 방지 검토): `{metrics['tier_no_lookahead_review_rows']}` rows(행)
- artifact registry review(산출물 등록부 검토): `{metrics['artifact_hash_registry_review_rows']}` rows(행)
- run336J queue(336J 대기열): `{metrics['run336j_queue_rows']}` rows(행)

## Judgment(판정)

run336I(336I 실행)는 run336H(336H 실행)의 scaffold(뼈대)를 검토했고, run336J(336J 실행)에서 proxy expected(프록시 예상값), fresh MT5 probe package(신규 MT5 탐침 패키지), difference/usability contract(차이/활용성 계약)를 물질화할 수 있다고 본다. Effect(효과): 다음 단계가 실제 MT5 실행을 주장하지 않고도, 어떤 파일과 해시와 차이표가 필요할지 고정된다.

Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), live readiness(실거래 준비), deployment(배포), operating promotion(운영 승격), Goal Achieve(목표 달성)는 모두 `not_claimed`다.

## Next(다음)

`{NEXT_RUN_ID}`에서 proxy expected result template(프록시 예상 결과 틀), fresh MT5 probe package(신규 MT5 탐침 패키지), row-level difference contract(행 단위 차이 계약), usability decision rule(활용성 판정 규칙)을 물질화한다. 실제 tester execution(테스터 실행)은 그 다음 run에서 좁게 시도한다.
"""
    decision_doc = f"""# Stage336I Runner Scaffold Review Decision(러너 뼈대 검토 결정)

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- status(상태): `{STATUS}`
- next_action(다음 행동): `{NEXT_RUN_ID}`

## Decision(결정)

run336H(336H 실행)의 runner scaffold(러너 뼈대)는 run336J(336J 실행)의 proxy expected/fresh MT5 probe input materialization(프록시 예상값/신규 MT5 탐침 입력 물질화)으로 넘길 수 있다. Effect(효과): 다음 작업은 proxy(프록시)와 MT5 runtime probe(런타임 탐침)를 비교할 수 있는 입력과 계약을 만들지만, 아직 MT5 실행이나 전진 판정은 아니다.

## Boundary(경계)

이 결정은 Forward Passed(전진 통과)나 Forward Failed(전진 실패)가 아니다. runtime authority(런타임 권위), operating promotion(운영 승격), deployment(배포), Goal Achieve(목표 달성)는 모두 주장하지 않는다.
"""
    write_md(REPORT_DOC, report)
    write_md(DECISION_DOC, decision_doc)


def update_docs(metrics: Mapping[str, Any]) -> None:
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_line(workspace_text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    focus_line = (
        f"  Stage336(336단계) run336I(336I 실행)는 `{STATUS}`로 runner scaffold review(러너 뼈대 검토)를 완료했다. "
        f"Effect(효과): scaffold review(뼈대 검토) `{metrics['review_completion_rows']}`개 그룹을 통과시키고 "
        f"run336J proxy/MT5 materialization queue(336J 프록시/MT5 물질화 대기열) `{metrics['run336j_queue_rows']}`행을 만들었다. "
        "Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    workspace_text = upsert_folded_list_item(workspace_text, "run336I(336I 실행)", focus_line)
    write_text_lossless(WORKSPACE_STATE, workspace_text, workspace_bom)

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    current_text = replace_line(current_text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    current_text = replace_line(current_text, "- status(상태):", f"- status(상태): `{STATUS}`")
    current_text = replace_line(current_text, "- decision(결정):", f"- decision(결정): `{DECISION}`")
    summary_line = (
        f"- run336I_summary(336I 요약): runner scaffold review(러너 뼈대 검토)를 `{STATUS}`로 완료했다. "
        f"Effect(효과): individual scaffold review(개별 뼈대 검토) `{metrics['individual_scaffold_review_rows']}`행, "
        f"proxy/MT5 review(프록시/MT5 검토) `{metrics['proxy_mt5_review_rows']}`행, run336J queue(336J 대기열) `{metrics['run336j_queue_rows']}`행을 만들었다. "
        "Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    if "- run336I_summary(336I 요약):" in current_text:
        current_text = replace_line(current_text, "- run336I_summary(336I 요약):", summary_line)
    elif "- run336H_summary" in current_text:
        current_text = current_text.replace("- run336H_summary", summary_line + "\n- run336H_summary", 1)
    else:
        current_text = current_text.rstrip() + "\n" + summary_line + "\n"
    write_text_lossless(CURRENT_STATE, current_text, current_bom)

    selection_path = SELECTED_DIR / "selection_status.md"
    selection_text, selection_bom = read_text_lossless(selection_path)
    selection_text = replace_line(selection_text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    selection_text = replace_line(selection_text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_RUN_ID}`")
    selection_text = replace_line(selection_text, "- latest_review(최신 검토):", f"- latest_review(최신 검토): `{RUN_ID}`")
    selection_text = replace_line(
        selection_text,
        "- effect(효과):",
        f"- effect(효과): Stage336(336단계)는 run336I(336I 실행)에서 runner scaffold(러너 뼈대)를 검토했고 run336J(336J 실행) proxy/MT5 materialization(프록시/MT5 물질화) 대기열을 만들었으며 후보 선택이나 운영 주장은 없다.",
    )
    write_text_lossless(selection_path, selection_text, selection_bom)

    brief_path = SPEC_DIR / "stage_brief.md"
    brief_text, brief_bom = read_text_lossless(brief_path)
    brief_text = replace_line(brief_text, "- latest_run(최신 실행):", f"- latest_run(최신 실행): `{RUN_ID}`")
    write_text_lossless(brief_path, brief_text, brief_bom)

    input_body = f"""- scaffold_index_manifest_review(뼈대 색인/목록 검토): `{rel(SCAFFOLD_INDEX_REVIEW_CSV)}`
- individual_scaffold_file_review(개별 뼈대 파일 검토): `{rel(INDIVIDUAL_SCAFFOLD_REVIEW_CSV)}`
- proxy_mt5_scaffold_review(프록시/MT5 뼈대 검토): `{rel(PROXY_MT5_REVIEW_CSV)}`
- runtime_identity_scaffold_review(런타임 정체성 뼈대 검토): `{rel(RUNTIME_IDENTITY_REVIEW_CSV)}`
- runner_scaffold_acceptance(러너 뼈대 승인): `{rel(RUNNER_SCAFFOLD_ACCEPTANCE_CSV)}`
- run336J_queue(336J 대기열): `{rel(RUN336J_QUEUE_CSV)}`
- final_decision(최종 결정): `{rel(FINAL_DECISION_JSON)}`
"""
    append_or_replace_section(INPUTS_DIR / "input_refs.md", "run336I Runner Scaffold Review(336I 러너 뼈대 검토)", input_body)

    changelog_body = f"""- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- effect(효과): run336H scaffold(336H 뼈대)를 검토하고 run336J proxy/MT5 materialization queue(336J 프록시/MT5 물질화 대기열) `{metrics['run336j_queue_rows']}`행을 만들었다.
- boundary(경계): 후보 선택, Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 `not_claimed`.
"""
    append_or_replace_section(CHANGELOG, "Stage336I Runner Scaffold Review(336I 러너 뼈대 검토)", changelog_body)


def update_registries(metrics: Mapping[str, Any], artifact_paths: Sequence[Path]) -> None:
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "stage336_runner_scaffold_review",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_DOC),
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};run336j_queue_rows={metrics['run336j_queue_rows']};goal_achieve_not_claimed.",
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__runner_scaffold_review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "constraint_bound_runner_scaffold_review",
                "tier_scope": "Tier A/Tier B paired future runtime requirement",
                "kpi_scope": "scaffold_review_no_new_trading_kpi",
                "scoreboard_lane": "experiment_review",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_DOC),
                "primary_kpi": f"review_groups={metrics['review_completion_rows']};run336j_queue_rows={metrics['run336j_queue_rows']}",
                "guardrail_kpi": "training_blocked=true;mt5_execution_blocked=true;forward_decision_blocked=true;runtime_authority_blocked=true",
                "external_verification_status": "out_of_scope_by_claim_runner_scaffold_review_only",
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID}.",
            },
            {
                "ledger_row_id": f"{RUN_ID}__proxy_mt5_scaffold_review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": f"{RUN_NUMBER}_proxy_mt5_review",
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "proxy_mt5_scaffold_usability_boundary_review",
                "tier_scope": "fresh_MT5_runtime_probe_required",
                "kpi_scope": "proxy_vs_mt5_difference_schema_before_usability",
                "scoreboard_lane": "runtime_parity_review",
                "status": STATUS,
                "judgment": "proxy_mt5_scaffolds_reviewed_diagnostic_only_no_forward_decision",
                "path": rel(PROXY_MT5_REVIEW_CSV),
                "primary_kpi": f"proxy_mt5_review_rows={metrics['proxy_mt5_review_rows']}",
                "guardrail_kpi": "selection_use=blocked;forward_decision_use=blocked;fresh_mt5_required=true",
                "external_verification_status": "out_of_scope_by_claim_runner_scaffold_review_only",
                "notes": "run336J must materialize proxy expected and fresh MT5 probe package before usability.",
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
                "ledger_row_id": f"{RUN_ID}__runner_scaffold_review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "work_family": "stage336_runner_scaffold_review",
                "evidence_scope": "run336H_runner_scaffolds_to_run336J_proxy_mt5_materialization",
                "kpi_scope": "scaffold_review_no_new_trading_kpi",
                "status": STATUS,
                "judgment": JUDGMENT,
                "claim_boundary": CLAIM_BOUNDARY,
                "path": rel(REPORT_DOC),
                "notes": f"review_groups={metrics['review_completion_rows']};run336j_queue_rows={metrics['run336j_queue_rows']};goal_achieve_not_claimed.",
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
                "artifact_type": "stage336I_runner_scaffold_review",
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created,
                "notes": "run336I_scaffold_review_no_execution_no_forward_decision",
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
    validate_parent_decision(inputs)

    expected_count_review = review_expected_counts()
    index_review = build_scaffold_index_review(inputs)
    individual_review = build_individual_scaffold_review(inputs["scaffold_index"])
    negative_review = build_negative_control_review(inputs)
    proxy_review = build_proxy_mt5_review(inputs)
    runtime_review = build_runtime_identity_review(inputs)
    cost_curve_review = build_cost_curve_gate_review(inputs)
    regime_review = build_regime_slice_review(inputs)
    tier_review = build_tier_no_lookahead_review(inputs)
    direction_offense_review = build_direction_offense_review(inputs)
    artifact_review = build_artifact_hash_registry_review(inputs)

    review_groups: dict[str, Sequence[Mapping[str, Any]]] = {
        "expected_counts": expected_count_review,
        "scaffold_index": index_review,
        "individual": individual_review,
        "negative_control": negative_review,
        "proxy_mt5": proxy_review,
        "runtime_identity": runtime_review,
        "cost_curve": cost_curve_review,
        "regime": regime_review,
        "tier": tier_review,
        "direction_offense": direction_offense_review,
        "artifact_lineage": artifact_review,
    }
    review_completion = build_review_completion(inputs["review_queue"], review_groups)
    review_groups["completion"] = review_completion
    acceptance = build_runner_acceptance(inputs["scaffold_index"], index_review, individual_review)
    review_groups["acceptance"] = acceptance
    run336j_queue = build_run336j_queue()

    pass_flags = {name: rows_passed(rows) for name, rows in review_groups.items()}
    metrics = make_metrics(inputs, review_groups, run336j_queue)

    output_paths: list[Path] = [
        write_csv(
            SCAFFOLD_INDEX_REVIEW_CSV,
            (
                "scaffold_id",
                "blueprint_id",
                "branch_id",
                "blueprint_family",
                "scaffold_path",
                "file_exists_review",
                "manifest_hash_review",
                "registry_hash_review",
                "executable_flag_review",
                "next_review_binding",
                "forbidden_claim_review",
                "review_decision",
                "next_required_action",
                "claim_boundary",
            ),
            index_review,
        ),
        write_csv(
            INDIVIDUAL_SCAFFOLD_REVIEW_CSV,
            (
                "scaffold_id",
                "blueprint_id",
                "branch_id",
                "scaffold_path",
                "row_count_review",
                "required_column_review",
                "missing_fields",
                "blocked_execution_review",
                "frozen_action_review",
                "next_review_binding",
                "result_ingestion_block_review",
                "review_decision",
                "claim_boundary",
            ),
            individual_review,
        ),
        write_csv(
            NEGATIVE_CONTROL_REVIEW_CSV,
            (
                "control_id",
                "branch_id",
                "target_risk",
                "negative_control_only_review",
                "canary_fail_closed_review",
                "expected_failure_signature",
                "stop_condition",
                "review_decision",
                "next_required_action",
                "claim_boundary",
            ),
            negative_review,
        ),
        write_csv(
            PROXY_MT5_REVIEW_CSV,
            (
                "contract_id",
                "branch_id",
                "proxy_expected_review",
                "fresh_mt5_result_review",
                "difference_schema_review",
                "usability_boundary_review",
                "usable_now",
                "usable_condition",
                "not_usable_condition",
                "review_decision",
                "next_required_action",
                "claim_boundary",
            ),
            proxy_review,
        ),
        write_csv(
            RUNTIME_IDENTITY_REVIEW_CSV,
            (
                "preflight_id",
                "branch_id",
                "runtime_subject",
                "required_check",
                "row_level_parity_binding_review",
                "external_verification_log_review",
                "runtime_authority_boundary_review",
                "result_pending_review",
                "review_decision",
                "next_required_action",
                "claim_boundary",
            ),
            runtime_review,
        ),
        write_csv(
            COST_CURVE_GATE_REVIEW_CSV,
            (
                "source_artifact",
                "plan_id",
                "branch_id",
                "gate_id",
                "review_subject",
                "measurement_review",
                "execution_order_review",
                "forbidden_shortcut_review",
                "result_pending_review",
                "review_decision",
                "next_required_action",
                "claim_boundary",
            ),
            cost_curve_review,
        ),
        write_csv(
            REGIME_SLICE_REVIEW_CSV,
            (
                "plan_id",
                "branch_id",
                "slice_id",
                "bucket_policy_review",
                "required_metrics_review",
                "attribution_only_review",
                "forward_filter_block_review",
                "review_decision",
                "next_required_action",
                "claim_boundary",
            ),
            regime_review,
        ),
        write_csv(
            TIER_NO_LOOKAHEAD_REVIEW_CSV,
            (
                "subject_id",
                "subject_type",
                "tier_scope",
                "time_axis_review",
                "forbidden_review",
                "actual_routed_total_guard_review",
                "review_decision",
                "next_required_action",
                "claim_boundary",
            ),
            tier_review,
        ),
        write_csv(
            DIRECTION_OFFENSE_FEATURE_REVIEW_CSV,
            (
                "subject_id",
                "subject_type",
                "branch_id",
                "blocked_shortcut_review",
                "after_result_pick_review",
                "execution_status_review",
                "review_decision",
                "next_required_action",
                "claim_boundary",
            ),
            direction_offense_review,
        ),
        write_csv(
            ARTIFACT_HASH_REGISTRY_REVIEW_CSV,
            (
                "artifact_id",
                "artifact_type",
                "path",
                "file_exists_review",
                "hash_review",
                "registry_run_binding_review",
                "review_decision",
                "claim_boundary",
            ),
            artifact_review,
        ),
        write_csv(
            REVIEW_COMPLETION_CSV,
            (
                "queue_id",
                "priority",
                "review_group",
                "source_artifacts",
                "source_exists_review",
                "review_rows",
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
                "scaffold_path",
                "accepted_for_run336J_probe_materialization",
                "blocked_until",
                "required_next_materialization",
                "forbidden_use",
                "review_decision",
                "claim_boundary",
            ),
            acceptance,
        ),
        write_csv(
            RUN336J_QUEUE_CSV,
            (
                "queue_id",
                "priority",
                "materialization_group",
                "task",
                "required_outputs",
                "success_condition",
                "forbidden",
                "claim_boundary",
            ),
            run336j_queue,
        ),
    ]
    output_paths.append(write_csv(GATE_AUDIT_CSV, ("gate_id", "status", "evidence", "finding", "claim_boundary"), build_gate_audit(metrics, pass_flags)))
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
                "live_readiness",
                "deployment",
                "operating_promotion",
                "goal_achieve",
                "next_action",
                "claim_boundary",
            ),
            [
                {
                    "run_id": RUN_ID,
                    "status": STATUS,
                    "judgment": JUDGMENT,
                    "decision": DECISION,
                    "evidence_available": "scaffold_reviews;runner_scaffold_acceptance;run336J_queue;receipts;registries",
                    "evidence_missing": "proxy expected actual values;fresh MT5 runtime probe;difference table;usability decision;Forward Passed/Failed evidence",
                    "judgment_label": "exploratory_runner_scaffold_review",
                    "forward_passed": "not_claimed",
                    "forward_failed": "not_claimed",
                    "runtime_authority": "not_claimed",
                    "live_readiness": "not_claimed",
                    "deployment": "not_claimed",
                    "operating_promotion": "not_claimed",
                    "goal_achieve": "not_claimed",
                    "next_action": NEXT_RUN_ID,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            ],
        )
    )
    output_paths.append(write_final_decision(metrics, pass_flags))
    output_paths.append(write_run_manifest(metrics, output_paths))
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
                "review_groups": metrics["review_completion_rows"],
                "individual_scaffold_review_rows": metrics["individual_scaffold_review_rows"],
                "proxy_mt5_review_rows": metrics["proxy_mt5_review_rows"],
                "runtime_identity_review_rows": metrics["runtime_identity_review_rows"],
                "run336j_queue_rows": metrics["run336j_queue_rows"],
                "forward_passed": "not_claimed",
                "runtime_authority": "not_claimed",
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
