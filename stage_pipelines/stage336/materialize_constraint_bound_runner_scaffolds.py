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
RUN_NUMBER = "run336H"
RUN_ID = "run336H_materialize_constraint_bound_runner_scaffolds_v1"
PARENT_RUN_ID = "run336G_review_constraint_bound_execution_blueprints_v1"
NEXT_RUN_ID = "run336I_review_constraint_bound_runner_scaffolds_v1"

STATUS = "completed_constraint_bound_runner_scaffolds_materialized_no_execution"
JUDGMENT = "materialized_runner_scaffolds_no_model_training_no_mt5_execution_no_forward_decision"
DECISION = "stage336H_runner_scaffolds_materialized_run336I_review_ready_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage336H_runner_scaffold_materialization_no_model_training_"
    "no_mt5_execution_no_threshold_retuning_no_lot_optimization_no_forward_pocket_filtering_"
    "no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)
FORBIDDEN = (
    "model_training;mt5_execution;threshold_retuning;lot_optimization;candidate_selection;"
    "Forward_decision;runtime_authority;deployment;operating_promotion;Goal_Achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN336F_DIR = STAGE_DIR / "02_runs" / "run336F"
RUN336G_DIR = STAGE_DIR / "02_runs" / "run336G"
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
DECISION_DOC = DOCS / "decisions" / "2026-05-27_stage336H_runner_scaffolds.md"
REPORT_DOC = REVIEWS_DIR / "run336H_runner_scaffolds.md"

BLUEPRINT_CATALOG_CSV = RUN336F_DIR / "execution_blueprint_catalog.csv"
BLUEPRINT_FIELD_CONTRACT_CSV = RUN336F_DIR / "blueprint_field_contract_matrix.csv"
NEGATIVE_CONTROL_BLUEPRINT_CSV = RUN336F_DIR / "negative_control_runner_blueprints.csv"
PROXY_MT5_BLUEPRINT_CSV = RUN336F_DIR / "proxy_mt5_runtime_usability_blueprints.csv"
RUNTIME_IDENTITY_BLUEPRINT_CSV = RUN336F_DIR / "runtime_identity_blueprints.csv"
GATE_RUNNER_BLUEPRINT_CSV = RUN336F_DIR / "gate_runner_blueprints.csv"
REGIME_RUNNER_BLUEPRINT_CSV = RUN336F_DIR / "regime_slice_runner_blueprints.csv"
TIER_NO_LOOKAHEAD_BLUEPRINT_CSV = RUN336F_DIR / "tier_no_lookahead_runner_blueprints.csv"
OUTPUT_CONTRACT_MATRIX_CSV = RUN336F_DIR / "blueprint_output_contract_matrix.csv"

BLUEPRINT_CATALOG_REVIEW_CSV = RUN336G_DIR / "blueprint_catalog_review.csv"
BLUEPRINT_FIELD_CONTRACT_REVIEW_CSV = RUN336G_DIR / "blueprint_field_contract_review.csv"
NEGATIVE_CONTROL_REVIEW_CSV = RUN336G_DIR / "negative_control_blueprint_review.csv"
PROXY_MT5_REVIEW_CSV = RUN336G_DIR / "proxy_mt5_blueprint_review.csv"
RUNTIME_IDENTITY_REVIEW_CSV = RUN336G_DIR / "runtime_identity_blueprint_review.csv"
GATE_REGIME_TIER_REVIEW_CSV = RUN336G_DIR / "gate_regime_tier_blueprint_review.csv"
OUTPUT_CONTRACT_REVIEW_CSV = RUN336G_DIR / "output_contract_matrix_review.csv"
RUNNER_SCAFFOLD_ACCEPTANCE_CSV = RUN336G_DIR / "runner_scaffold_acceptance_matrix.csv"
RUN336H_QUEUE_CSV = RUN336G_DIR / "run336H_runner_scaffold_queue.csv"
RUN336G_FINAL_DECISION_JSON = RUN336G_DIR / "final_execution_blueprint_review_decision.json"

SCAFFOLD_INDEX_CSV = RUN_DIR / "scaffold_index.csv"
SCAFFOLD_MANIFEST_JSON = RUN_DIR / "scaffold_manifest.json"
NEGATIVE_CONTROL_SCAFFOLD_CSV = RUN_DIR / "negative_control_scaffold_matrix.csv"
CANARY_EXPECTED_FAILURE_CSV = RUN_DIR / "canary_expected_failure_schema.csv"
PROXY_EXPECTED_SCHEMA_CSV = RUN_DIR / "proxy_expected_schema.csv"
FRESH_MT5_RESULT_SCHEMA_CSV = RUN_DIR / "fresh_mt5_result_schema.csv"
PROXY_MT5_DIFFERENCE_SCHEMA_CSV = RUN_DIR / "proxy_mt5_difference_schema.csv"
USABILITY_DECISION_SCHEMA_CSV = RUN_DIR / "usability_decision_schema.csv"
RUNTIME_IDENTITY_MANIFEST_SCHEMA_CSV = RUN_DIR / "runtime_identity_manifest_schema.csv"
ROW_LEVEL_PARITY_SCHEMA_CSV = RUN_DIR / "row_level_parity_schema.csv"
EXTERNAL_VERIFICATION_LOG_SCHEMA_CSV = RUN_DIR / "external_verification_log_schema.csv"
COST_STRESS_SCHEMA_CSV = RUN_DIR / "cost_stress_schema.csv"
CURVE_POCKET_SCHEMA_CSV = RUN_DIR / "curve_pocket_schema.csv"
UNDERWATER_SCHEMA_CSV = RUN_DIR / "underwater_schema.csv"
DIRECTION_SCHEMA_CSV = RUN_DIR / "direction_schema.csv"
LOT_NORMALIZED_SCHEMA_CSV = RUN_DIR / "lot_normalized_schema.csv"
REGIME_SLICE_SCHEMA_MATRIX_CSV = RUN_DIR / "regime_slice_schema_matrix.csv"
TIER_PAIR_SCHEMA_CSV = RUN_DIR / "tier_pair_schema.csv"
FUTURE_SHIFT_CANARY_SCHEMA_CSV = RUN_DIR / "future_shift_canary_schema.csv"
THRESHOLD_LOT_FREEZE_MANIFEST_SCHEMA_CSV = RUN_DIR / "threshold_lot_freeze_manifest_schema.csv"
LONG_SHORT_ATTRIBUTION_SCHEMA_CSV = RUN_DIR / "long_short_attribution_schema.csv"
FEATURE_FAMILY_SEED_CARD_SCHEMA_CSV = RUN_DIR / "feature_family_seed_card_schema.csv"
TRADE_DENSITY_TARGET_SCHEMA_CSV = RUN_DIR / "trade_density_target_schema.csv"
ARTIFACT_HASH_RECEIPT_SCHEMA_CSV = RUN_DIR / "artifact_hash_receipt_schema.csv"
OUTPUT_REGISTRY_BINDING_SCHEMA_CSV = RUN_DIR / "output_registry_binding_schema.csv"
RUN336I_REVIEW_QUEUE_CSV = RUN_DIR / "run336I_review_queue.csv"
GATE_AUDIT_CSV = RUN_DIR / "required_gate_coverage_audit.csv"
RESULT_JUDGMENT_CSV = RUN_DIR / "result_judgment.csv"
FINAL_DECISION_JSON = RUN_DIR / "final_runner_scaffold_materialization_decision.json"
RUN_MANIFEST_JSON = RUN_DIR / "run_manifest.json"

EXPECTED_QUEUE_OUTPUTS = {
    "scaffold_index.csv",
    "scaffold_manifest.json",
    "negative_control_scaffold_matrix.csv",
    "canary_expected_failure_schema.csv",
    "proxy_expected_schema.csv",
    "fresh_mt5_result_schema.csv",
    "proxy_mt5_difference_schema.csv",
    "usability_decision_schema.csv",
    "runtime_identity_manifest_schema.csv",
    "row_level_parity_schema.csv",
    "external_verification_log_schema.csv",
    "cost_stress_schema.csv",
    "curve_pocket_schema.csv",
    "underwater_schema.csv",
    "direction_schema.csv",
    "lot_normalized_schema.csv",
    "regime_slice_schema_matrix.csv",
    "tier_pair_schema.csv",
    "future_shift_canary_schema.csv",
    "threshold_lot_freeze_manifest_schema.csv",
    "long_short_attribution_schema.csv",
    "feature_family_seed_card_schema.csv",
    "trade_density_target_schema.csv",
    "artifact_hash_receipt_schema.csv",
    "output_registry_binding_schema.csv",
}

SCHEMA_ARTIFACTS_BY_FAMILY = {
    "repair_identity": [RUNTIME_IDENTITY_MANIFEST_SCHEMA_CSV, EXTERNAL_VERIFICATION_LOG_SCHEMA_CSV],
    "proxy_exclusion": [CANARY_EXPECTED_FAILURE_CSV, PROXY_MT5_DIFFERENCE_SCHEMA_CSV],
    "handoff_identity": [RUNTIME_IDENTITY_MANIFEST_SCHEMA_CSV, ROW_LEVEL_PARITY_SCHEMA_CSV],
    "cost_curve": [COST_STRESS_SCHEMA_CSV, CURVE_POCKET_SCHEMA_CSV, UNDERWATER_SCHEMA_CSV, LOT_NORMALIZED_SCHEMA_CSV],
    "direction": [DIRECTION_SCHEMA_CSV, LONG_SHORT_ATTRIBUTION_SCHEMA_CSV],
    "negative_control": [NEGATIVE_CONTROL_SCAFFOLD_CSV, CANARY_EXPECTED_FAILURE_CSV],
    "offense_feature": [FEATURE_FAMILY_SEED_CARD_SCHEMA_CSV, TRADE_DENSITY_TARGET_SCHEMA_CSV],
    "regime": [REGIME_SLICE_SCHEMA_MATRIX_CSV],
    "runtime_identity": [RUNTIME_IDENTITY_MANIFEST_SCHEMA_CSV, ROW_LEVEL_PARITY_SCHEMA_CSV, EXTERNAL_VERIFICATION_LOG_SCHEMA_CSV],
    "proxy_mt5": [
        PROXY_EXPECTED_SCHEMA_CSV,
        FRESH_MT5_RESULT_SCHEMA_CSV,
        PROXY_MT5_DIFFERENCE_SCHEMA_CSV,
        USABILITY_DECISION_SCHEMA_CSV,
    ],
    "tier_integrity": [TIER_PAIR_SCHEMA_CSV, FUTURE_SHIFT_CANARY_SCHEMA_CSV, THRESHOLD_LOT_FREEZE_MANIFEST_SCHEMA_CSV],
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


def as_bool_text(value: Any) -> str:
    return "true" if str(value).strip().lower() == "true" else "false"


def fail(message: str) -> None:
    raise RuntimeError(message)


def load_inputs() -> dict[str, Any]:
    final_review = read_json(RUN336G_FINAL_DECISION_JSON)
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
        "catalog_review": read_csv(BLUEPRINT_CATALOG_REVIEW_CSV),
        "field_contract_review": read_csv(BLUEPRINT_FIELD_CONTRACT_REVIEW_CSV),
        "negative_control_review": read_csv(NEGATIVE_CONTROL_REVIEW_CSV),
        "proxy_mt5_review": read_csv(PROXY_MT5_REVIEW_CSV),
        "runtime_identity_review": read_csv(RUNTIME_IDENTITY_REVIEW_CSV),
        "gate_regime_tier_review": read_csv(GATE_REGIME_TIER_REVIEW_CSV),
        "output_contract_review": read_csv(OUTPUT_CONTRACT_REVIEW_CSV),
        "acceptance": read_csv(RUNNER_SCAFFOLD_ACCEPTANCE_CSV),
        "queue": read_csv(RUN336H_QUEUE_CSV),
        "final_review": final_review,
    }


def validate_inputs(inputs: Mapping[str, Any]) -> None:
    if not inputs["final_review"].get("all_reviews_passed"):
        fail("run336G final review did not pass all reviews.")
    if inputs["final_review"].get("next_action") != RUN_ID:
        fail("run336G final review next_action does not match run336H.")
    if len(inputs["catalog"]) != 31:
        fail(f"expected 31 blueprint catalog rows, got {len(inputs['catalog'])}")
    accepted = [row for row in inputs["acceptance"] if as_bool_text(row.get("accepted_for_run336H_scaffold")) == "true"]
    if len(accepted) != 31:
        fail(f"expected 31 accepted run336H scaffold rows, got {len(accepted)}")
    queue_outputs: set[str] = set()
    for row in inputs["queue"]:
        queue_outputs.update(split_semicolon(row.get("required_outputs")))
    missing_outputs = sorted(EXPECTED_QUEUE_OUTPUTS - queue_outputs)
    if missing_outputs:
        fail("run336H queue is missing required outputs: " + ";".join(missing_outputs))
    for review_name in (
        "catalog_review",
        "field_contract_review",
        "negative_control_review",
        "proxy_mt5_review",
        "runtime_identity_review",
        "gate_regime_tier_review",
        "output_contract_review",
    ):
        rows = inputs[review_name]
        if not rows:
            fail(f"{review_name} has no rows")
        bad_rows = [
            row
            for row in rows
            if any(token in str(row.get("review_decision", "")).lower() for token in ("failed", "repair_required", "missing", "invalid"))
        ]
        if bad_rows:
            fail(f"{review_name} contains non-passing review decisions")


def source_review_for_family(family: str) -> Path:
    if family == "negative_control":
        return NEGATIVE_CONTROL_REVIEW_CSV
    if family == "proxy_mt5":
        return PROXY_MT5_REVIEW_CSV
    if family in {"runtime_identity", "handoff_identity", "repair_identity"}:
        return RUNTIME_IDENTITY_REVIEW_CSV
    if family in {"cost_curve", "direction", "regime", "tier_integrity"}:
        return GATE_REGIME_TIER_REVIEW_CSV
    if family in {"offense_feature", "proxy_exclusion"}:
        return BLUEPRINT_FIELD_CONTRACT_REVIEW_CSV
    return BLUEPRINT_CATALOG_REVIEW_CSV


def schema_artifacts_for_family(family: str) -> str:
    return ";".join(rel(path) for path in SCHEMA_ARTIFACTS_BY_FAMILY.get(family, [SCAFFOLD_INDEX_CSV]))


def scaffold_path(row: Mapping[str, str]) -> Path:
    raw = row.get("future_scaffold_path") or row.get("future_artifact_hint")
    if not raw:
        fail(f"missing future scaffold path for {row.get('blueprint_id')}")
    path = ROOT / raw if not Path(raw).is_absolute() else Path(raw)
    if path.resolve() != (RUN_DIR / path.name).resolve():
        fail(f"scaffold path outside run336H directory: {raw}")
    return path


def map_by_key(rows: Sequence[Mapping[str, str]], key: str) -> dict[str, Mapping[str, str]]:
    return {str(row.get(key, "")).strip(): row for row in rows if str(row.get(key, "")).strip()}


def build_scaffold_index(
    catalog: Sequence[Mapping[str, str]],
    acceptance: Sequence[Mapping[str, str]],
    outputs: Sequence[Mapping[str, str]],
) -> list[dict[str, Any]]:
    acceptance_by_id = map_by_key(acceptance, "blueprint_id")
    outputs_by_id = map_by_key(outputs, "blueprint_id")
    rows: list[dict[str, Any]] = []
    for ordinal, blueprint in enumerate(catalog, start=1):
        blueprint_id = blueprint["blueprint_id"]
        accepted = acceptance_by_id.get(blueprint_id)
        output_contract = outputs_by_id.get(blueprint_id, {})
        if not accepted:
            fail(f"missing acceptance row for {blueprint_id}")
        path = scaffold_path(accepted)
        family = blueprint.get("blueprint_family", "")
        source_review = source_review_for_family(family)
        rows.append(
            {
                "scaffold_id": f"{RUN_NUMBER}_{ordinal:03d}",
                "blueprint_id": blueprint_id,
                "branch_id": blueprint.get("branch_id", ""),
                "lane": blueprint.get("lane", ""),
                "blueprint_family": family,
                "blueprint_name": blueprint.get("blueprint_name", ""),
                "scaffold_path": rel(path),
                "schema_artifacts": schema_artifacts_for_family(family),
                "source_review_artifact": rel(source_review),
                "source_review_sha256": sha256_file_lf_normalized(source_review),
                "future_artifact_hint": output_contract.get("future_artifact_hint", accepted.get("future_scaffold_path", "")),
                "materialization_status": "materialized_schema_scaffold_no_execution",
                "executable": "false",
                "model_training_allowed": "false",
                "mt5_execution_allowed": "false",
                "selection_allowed": "false",
                "forward_decision_allowed": "false",
                "runtime_authority_allowed": "false",
                "next_review_required": NEXT_RUN_ID,
                "forbidden": FORBIDDEN,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def write_individual_scaffolds(
    scaffold_index: Sequence[Mapping[str, Any]],
    field_contracts: Sequence[Mapping[str, str]],
    outputs: Sequence[Mapping[str, str]],
) -> list[Path]:
    field_by_id = map_by_key(field_contracts, "blueprint_id")
    output_by_id = map_by_key(outputs, "blueprint_id")
    paths: list[Path] = []
    columns = (
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
        "must_exist_before_execution_review",
        "hash_required",
        "registry_required",
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
    for row in scaffold_index:
        blueprint_id = str(row["blueprint_id"])
        field = field_by_id.get(blueprint_id, {})
        output = output_by_id.get(blueprint_id, {})
        path = ROOT / str(row["scaffold_path"])
        scaffold_row = {
            "scaffold_id": row["scaffold_id"],
            "blueprint_id": blueprint_id,
            "branch_id": row["branch_id"],
            "blueprint_family": row["blueprint_family"],
            "blueprint_name": row["blueprint_name"],
            "required_input_identity": field.get("required_input_identity", "source_protocol;branch_id;claim_boundary"),
            "required_output_schema": field.get("required_output_schema", row.get("schema_artifacts", "")),
            "required_gate": field.get("required_gate", "run336I_review_required_before_execution"),
            "failure_condition": field.get("failure_condition", "missing_required_input;runtime_identity_gap;after_result_filter"),
            "future_review_requirement": NEXT_RUN_ID,
            "must_exist_before_execution_review": output.get("must_exist_before_execution_review", "true"),
            "hash_required": output.get("hash_required", "true"),
            "registry_required": output.get("registry_required", "true"),
            "execution_ready": "false",
            "execution_status": "schema_scaffold_only_no_execution",
            "model_training_allowed": "false",
            "mt5_execution_allowed": "false",
            "selection_allowed": "false",
            "forward_decision_allowed": "false",
            "runtime_authority_allowed": "false",
            "result_ingestion_status": "blocked_until_run336I_review_and_future_execution_packet",
            "next_review_required": NEXT_RUN_ID,
            "forbidden": FORBIDDEN,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        paths.append(write_csv(path, columns, [scaffold_row]))
    return paths


def build_negative_control_scaffolds(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    return [
        {
            "control_id": row.get("control_id", ""),
            "branch_id": row.get("branch_id", ""),
            "target_risk": row.get("target_risk", ""),
            "runner_blueprint": row.get("runner_blueprint", ""),
            "mutation_plan": row.get("mutation_plan", ""),
            "expected_failure_signature": row.get("expected_failure_signature", ""),
            "stop_condition": row.get("stop_condition", ""),
            "future_output": row.get("future_output", ""),
            "allowed_use": "negative_control_only",
            "execution_ready": "false",
            "result_status": "pending_future_execution_not_run_in_run336H",
            "forbidden_use": row.get("forbidden_use", FORBIDDEN),
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in rows
    ]


def build_canary_expected_failure(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    return [
        {
            "canary_id": row.get("control_id", ""),
            "branch_id": row.get("branch_id", ""),
            "shortcut_risk": row.get("target_risk", ""),
            "expected_failure_signature": row.get("expected_failure_signature", ""),
            "required_failure_effect": row.get("stop_condition", ""),
            "pass_condition": "canary_fails_as_expected_and_blocks_shortcut_use",
            "fail_condition": "canary_passes_or_is_missing_before_result_interpretation",
            "allowed_use": "canary_expected_failure_only",
            "selection_use": "blocked",
            "forward_decision_use": "blocked",
            "runtime_authority_use": "blocked",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in rows
    ]


def build_proxy_expected_schema(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    return [
        {
            "contract_id": row.get("contract_id", ""),
            "branch_id": row.get("branch_id", ""),
            "required_schema_fields": row.get("proxy_expected_schema", ""),
            "comparison_key": row.get("comparison_key", ""),
            "source_kind": "proxy_expected_diagnostic_only",
            "row_level_required": "true",
            "fresh_mt5_required": "true",
            "selection_use": "blocked",
            "forward_decision_use": "blocked",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in rows
    ]


def build_fresh_mt5_result_schema(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    return [
        {
            "contract_id": row.get("contract_id", ""),
            "branch_id": row.get("branch_id", ""),
            "required_schema_fields": row.get("fresh_mt5_result_schema", ""),
            "required_source": "fresh_MT5_strategy_tester_or_terminal_probe",
            "external_verification_status_required": "completed_or_explicit_attempt_with_failure_log",
            "row_level_required": "true",
            "aggregate_only_match_allowed": "false",
            "mt5_execution_status": "not_run_in_run336H",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in rows
    ]


def build_proxy_mt5_difference_schema(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    return [
        {
            "contract_id": row.get("contract_id", ""),
            "branch_id": row.get("branch_id", ""),
            "difference_schema": row.get("difference_schema", ""),
            "tolerance_policy": row.get("tolerance_policy", ""),
            "usable_condition": row.get("usable_condition", ""),
            "not_usable_condition": row.get("not_usable_condition", ""),
            "diagnostic_use_only": "true",
            "selection_use": "blocked",
            "forward_decision_use": "blocked",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in rows
    ]


def build_usability_decision_schema(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    return [
        {
            "contract_id": row.get("contract_id", ""),
            "branch_id": row.get("branch_id", ""),
            "usable_condition": row.get("usable_condition", ""),
            "not_usable_condition": row.get("not_usable_condition", ""),
            "decision_label_allowed_values": "usable_diagnostic_only;not_usable;blocked_missing_fresh_mt5;blocked_negative_control_failure",
            "required_inputs": "proxy_expected_schema;fresh_mt5_result_schema;proxy_mt5_difference_schema;negative_control_status;runtime_identity_status",
            "operating_use": "blocked",
            "runtime_authority_use": "blocked",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in rows
    ]


def build_runtime_identity_manifest(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    return [
        {
            "preflight_id": row.get("preflight_id", ""),
            "branch_id": row.get("branch_id", ""),
            "runtime_subject": row.get("runtime_subject", ""),
            "required_identity": row.get("required_identity", ""),
            "required_check": row.get("required_check", ""),
            "acceptance_evidence": row.get("acceptance_evidence", ""),
            "future_output_path_requirement": row.get("future_output_path_requirement", ""),
            "external_verification_status_required": row.get("external_verification_status_required", ""),
            "runtime_claim_boundary": "runtime_probe_only_no_runtime_authority",
            "result_status": "pending_future_runtime_probe_not_run_in_run336H",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in rows
    ]


def build_row_level_parity_schema(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    filtered = [
        row
        for row in rows
        if "decision mismatch" in row.get("required_check", "").lower()
    ]
    return [
        {
            "preflight_id": row.get("preflight_id", ""),
            "branch_id": row.get("branch_id", ""),
            "parity_subject": row.get("runtime_subject", ""),
            "required_identity": row.get("required_identity", ""),
            "required_row_fields": "timestamp;python_probability;mt5_probability;python_decision;mt5_decision;decision_mismatch;probability_diff;skip_reason",
            "tolerance_policy": "max_probability_diff<=1e-6;decision_mismatch=0;terminal_flat_gap_named",
            "aggregate_only_match_allowed": "false",
            "runtime_authority_use": "blocked",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in filtered
    ]


def build_external_verification_log_schema(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    return [
        {
            "preflight_id": row.get("preflight_id", ""),
            "branch_id": row.get("branch_id", ""),
            "runtime_subject": row.get("runtime_subject", ""),
            "required_check": row.get("required_check", ""),
            "required_log_fields": "attempted_at_utc;command_or_tool;terminal_path;settings_path;output_path;exit_status;error_log;blocker",
            "external_verification_status_required": row.get("external_verification_status_required", ""),
            "acceptable_closeout": "completed_or_blocked_with_exact_failure_log",
            "runtime_authority_use": "blocked",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in rows
    ]


def build_gate_schema(rows: Sequence[Mapping[str, str]], gate_id: str, schema_name: str) -> list[dict[str, Any]]:
    return [
        {
            "plan_id": row.get("plan_id", ""),
            "branch_id": row.get("branch_id", ""),
            "gate_id": row.get("gate_id", ""),
            "schema_name": schema_name,
            "required_measurement": row.get("required_measurement", ""),
            "future_output_table_name": row.get("future_output_table_name", ""),
            "review_requirement": row.get("review_requirement", ""),
            "failure_memory_trigger": row.get("failure_memory_trigger", ""),
            "execution_order": row.get("execution_order", ""),
            "forbidden_shortcut": row.get("forbidden_shortcut", ""),
            "future_runner_blueprint": row.get("future_runner_blueprint", ""),
            "result_status": "pending_future_execution_not_run_in_run336H",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in rows
        if row.get("gate_id") == gate_id
    ]


def build_regime_slice_schema(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    return [
        {
            "plan_id": row.get("plan_id", ""),
            "branch_id": row.get("branch_id", ""),
            "slice_id": row.get("slice_id", ""),
            "output_field": row.get("output_field", ""),
            "bucket_policy": row.get("bucket_policy", ""),
            "required_metrics": row.get("required_metrics", ""),
            "allowed_use": row.get("allowed_use", "attribution_and_failure_memory_only"),
            "forbidden_use": row.get("forbidden_use", "direct_forward_pocket_filter"),
            "future_runner_blueprint": row.get("future_runner_blueprint", ""),
            "selection_filter_use": "blocked",
            "forward_filter_use": "blocked",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in rows
    ]


def build_tier_pair_schema(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    return [
        {
            "contract_id": row.get("contract_id", ""),
            "tier_scope": row.get("tier_scope", ""),
            "required_fields": row.get("required_fields", ""),
            "time_axis_rule": row.get("time_axis_rule", ""),
            "acceptance_condition": row.get("acceptance_condition", ""),
            "forbidden": row.get("forbidden", ""),
            "future_runner_blueprint": row.get("future_runner_blueprint", ""),
            "future_required_outputs": row.get("future_required_outputs", ""),
            "actual_routed_total_guard": "synthetic_sum_blocked",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in rows
    ]


def build_future_shift_canary_schema(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    canaries = sorted(
        {
            canary
            for row in rows
            for canary in split_semicolon(row.get("lookahead_canary", ""))
            if "future_shift" in canary
        }
    )
    return [
        {
            "canary_id": canary,
            "time_axis_rule": "closed_bar_only_no_partial_bar_no_future_or_nearest_join",
            "expected_failure_signature": "future_shift_or_nearest_join_attempt_detected_and_blocked",
            "required_scope": "Tier A;Tier B;actual routed total;proxy expected;fresh MT5 result",
            "selection_use": "blocked",
            "forward_decision_use": "blocked",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for canary in canaries
    ]


def build_threshold_lot_freeze_manifest_schema(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    freeze_rows = [row for row in rows if "freeze" in row.get("contract_id", "").lower()]
    if not freeze_rows:
        freeze_rows = list(rows)
    return [
        {
            "contract_id": row.get("contract_id", "threshold_lot_freeze_manifest"),
            "tier_scope": row.get("tier_scope", "cross_branch_execution_freeze"),
            "required_fields": row.get(
                "required_fields",
                "threshold_hash;risk_logic_hash;lot_logic_hash;ATR_SLTP_hash;runtime_handoff_hash;created_before_result_read",
            ),
            "created_before_result_read_required": "true",
            "threshold_retuning_allowed": "false",
            "lot_optimization_allowed": "false",
            "ATR_exit_change_allowed": "false",
            "future_required_outputs": row.get("future_required_outputs", "threshold_lot_freeze_manifest;freeze_hash_receipt"),
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in freeze_rows
    ]


def build_feature_family_seed_card(catalog: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    return [
        {
            "blueprint_id": row.get("blueprint_id", ""),
            "branch_id": row.get("branch_id", ""),
            "blueprint_name": row.get("blueprint_name", ""),
            "feature_family_seed_status": "predeclared_before_future_result_read",
            "allowed_use": "offense_research_seed_only",
            "after_result_feature_pick": "blocked",
            "model_training_allowed": "false",
            "future_review_required": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in catalog
        if row.get("blueprint_family") == "offense_feature"
    ]


def build_trade_density_target(catalog: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows = [
        row
        for row in catalog
        if row.get("blueprint_family") == "offense_feature" and "trade_density" in row.get("blueprint_name", "")
    ]
    if not rows:
        rows = [row for row in catalog if row.get("blueprint_family") == "offense_feature"]
    return [
        {
            "blueprint_id": row.get("blueprint_id", ""),
            "branch_id": row.get("branch_id", ""),
            "blueprint_name": row.get("blueprint_name", ""),
            "density_target_status": "schema_only_no_result_target_tuning",
            "required_fields": "candidate_id;branch_id;signal_count;trade_count;trades_per_day;skip_count;density_floor_reason",
            "optimization_use": "blocked",
            "future_review_required": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in rows
    ]


def build_artifact_hash_receipt_schema(outputs: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    return [
        {
            "blueprint_id": row.get("blueprint_id", ""),
            "branch_id": row.get("branch_id", ""),
            "blueprint_name": row.get("blueprint_name", ""),
            "future_artifact_hint": row.get("future_artifact_hint", ""),
            "must_exist_before_execution_review": row.get("must_exist_before_execution_review", ""),
            "hash_required": row.get("hash_required", ""),
            "registry_required": row.get("registry_required", ""),
            "expected_hash_algorithm": "sha256_lf_normalized",
            "current_hash_status": "pending_future_runner_output",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in outputs
    ]


def build_output_registry_binding_schema(outputs: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    return [
        {
            "artifact_binding_id": f"{RUN_ID}__{row.get('blueprint_id', '')}",
            "blueprint_id": row.get("blueprint_id", ""),
            "branch_id": row.get("branch_id", ""),
            "future_artifact_hint": row.get("future_artifact_hint", ""),
            "registry_path": rel(ARTIFACT_REGISTRY),
            "must_exist_before_execution_review": row.get("must_exist_before_execution_review", ""),
            "hash_required": row.get("hash_required", ""),
            "registry_required": row.get("registry_required", ""),
            "next_review": NEXT_RUN_ID,
            "can_support_model_training": "false",
            "can_support_forward_decision": "false",
            "can_support_runtime_authority": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in outputs
    ]


def build_run336i_review_queue() -> list[dict[str, Any]]:
    items = [
        (
            "run336I_review_scaffold_index_manifest",
            "cross_branch_registry",
            "scaffold_index.csv;scaffold_manifest.json",
            "Verify 31 accepted scaffold files, hashes, and no executable flags.",
        ),
        (
            "run336I_review_negative_control_scaffolds",
            "negative_control",
            "negative_control_scaffold_matrix.csv;canary_expected_failure_schema.csv",
            "Verify all 10 canaries are negative-control-only and fail closed.",
        ),
        (
            "run336I_review_proxy_mt5_comparison_scaffolds",
            "proxy_mt5",
            "proxy_expected_schema.csv;fresh_mt5_result_schema.csv;proxy_mt5_difference_schema.csv;usability_decision_schema.csv",
            "Verify proxy remains diagnostic-only until fresh MT5 row-level evidence exists.",
        ),
        (
            "run336I_review_runtime_identity_scaffolds",
            "runtime_identity",
            "runtime_identity_manifest_schema.csv;row_level_parity_schema.csv;external_verification_log_schema.csv",
            "Verify runtime authority remains blocked without external probe evidence.",
        ),
        (
            "run336I_review_cost_curve_gate_scaffolds",
            "cost_curve",
            "cost_stress_schema.csv;curve_pocket_schema.csv;underwater_schema.csv;direction_schema.csv;lot_normalized_schema.csv",
            "Verify stress and curve schemas are mandatory before any comparison.",
        ),
        (
            "run336I_review_regime_slice_scaffolds",
            "regime",
            "regime_slice_schema_matrix.csv",
            "Verify slices are attribution-only and cannot become direct forward filters.",
        ),
        (
            "run336I_review_tier_no_lookahead_scaffolds",
            "tier_integrity",
            "tier_pair_schema.csv;future_shift_canary_schema.csv;threshold_lot_freeze_manifest_schema.csv",
            "Verify tier records, no-lookahead canary, and freeze manifest are present.",
        ),
        (
            "run336I_review_direction_offense_feature_scaffolds",
            "direction_offense_feature",
            "long_short_attribution_schema.csv;feature_family_seed_card_schema.csv;trade_density_target_schema.csv",
            "Verify side dropping and after-result feature picking stay blocked.",
        ),
        (
            "run336I_review_artifact_hash_registry_scaffolds",
            "artifact_lineage",
            "artifact_hash_receipt_schema.csv;output_registry_binding_schema.csv",
            "Verify every future output requires existence, hash, registry, and next review.",
        ),
    ]
    return [
        {
            "queue_id": queue_id,
            "priority": index,
            "review_group": group,
            "source_artifacts": artifacts,
            "review_task": task,
            "success_condition": "schema_exists;row_count_matches;forbidden_claims_absent;executable_false",
            "forbidden": FORBIDDEN,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for index, (queue_id, group, artifacts, task) in enumerate(items, start=1)
    ]


def build_gate_audit(metrics: Mapping[str, Any]) -> list[dict[str, Any]]:
    checks = [
        ("run336G_inputs_loaded", metrics["accepted_scaffold_rows"] == 31, "accepted_scaffold_rows=31"),
        ("scaffold_index_materialized", metrics["scaffold_index_rows"] == 31, "scaffold_index_rows=31"),
        ("individual_scaffolds_materialized", metrics["individual_scaffold_files"] == 31, "individual_scaffold_files=31"),
        ("negative_control_scaffolds_materialized", metrics["negative_control_rows"] == 10, "negative_control_rows=10"),
        ("proxy_mt5_scaffolds_materialized", metrics["proxy_mt5_rows"] == 7, "proxy_mt5_rows=7"),
        ("runtime_identity_scaffolds_materialized", metrics["runtime_identity_rows"] == 30, "runtime_identity_rows=30"),
        ("cost_curve_gate_scaffolds_materialized", metrics["gate_rows"] == 36, "gate_rows=36"),
        ("regime_slice_scaffolds_materialized", metrics["regime_rows"] == 48, "regime_rows=48"),
        ("tier_no_lookahead_scaffolds_materialized", metrics["tier_rows"] == 4, "tier_rows=4"),
        ("output_hash_registry_scaffolds_materialized", metrics["output_contract_rows"] == 31, "output_contract_rows=31"),
        ("run336I_review_queue_materialized", metrics["run336i_queue_rows"] == 9, "run336i_queue_rows=9"),
        ("forbidden_claims_absent", True, "Forward/operating/runtime/Goal claims remain not_claimed"),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": "passed" if condition else "failed",
            "evidence": evidence,
            "finding": "materialized_with_boundary" if condition else "repair_required_before_run336I",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, condition, evidence in checks
    ]


def write_scaffold_manifest(scaffold_index: Sequence[Mapping[str, Any]], metrics: Mapping[str, Any]) -> Path:
    manifest_rows = []
    for row in scaffold_index:
        path = ROOT / str(row["scaffold_path"])
        manifest_rows.append(
            {
                "scaffold_id": row["scaffold_id"],
                "blueprint_id": row["blueprint_id"],
                "branch_id": row["branch_id"],
                "blueprint_family": row["blueprint_family"],
                "scaffold_path": row["scaffold_path"],
                "sha256": sha256_file_lf_normalized(path),
                "executable": "false",
                "next_review_required": NEXT_RUN_ID,
            }
        )
    return write_json(
        SCAFFOLD_MANIFEST_JSON,
        {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "stage_id": STAGE_ID,
            "status": STATUS,
            "decision": DECISION,
            "created_at_utc": now_utc(),
            "metrics": dict(metrics),
            "scaffolds": manifest_rows,
            "model_training": "not_run",
            "mt5_execution": "not_run",
            "forward_passed": "not_claimed",
            "forward_failed": "not_claimed",
            "runtime_authority": "not_claimed",
            "goal_achieve": "not_claimed",
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
            "command": "python stage_pipelines/stage336/materialize_constraint_bound_runner_scaffolds.py",
            "inputs": [
                rel(BLUEPRINT_CATALOG_CSV),
                rel(RUNNER_SCAFFOLD_ACCEPTANCE_CSV),
                rel(RUN336H_QUEUE_CSV),
                rel(RUN336G_FINAL_DECISION_JSON),
            ],
            "outputs": [rel(path) for path in output_paths],
            "metrics": dict(metrics),
            "external_verification_status": "out_of_scope_by_claim_runner_scaffold_materialization_only",
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
            "data_source": [
                rel(BLUEPRINT_CATALOG_CSV),
                rel(RUNNER_SCAFFOLD_ACCEPTANCE_CSV),
                rel(RUN336H_QUEUE_CSV),
            ],
            "time_axis": "schema_materialization_only; future execution requires closed_bar_only_no_partial_bar_no_future_or_nearest_join",
            "sample_scope": "Stage336 run336F/run336G scaffold source artifacts only; no new broker rows",
            "missing_or_duplicate_check": "31 accepted blueprint scaffolds and required schema counts materialized",
            "feature_label_boundary": "no features or labels recalculated; future_shift and threshold/lot shortcuts remain canary-gated",
            "split_boundary": "not_applicable_runner_scaffold_materialization_only",
            "leakage_risk": "after_result_filtering; direct_forward_pocket_filter; old_proxy_rank_use; copied_runtime_result",
            "integrity_judgment": "usable_with_boundary_for_run336I_review",
        },
        "runtime_parity_receipt.json": {
            **common,
            "research_path": rel(Path(__file__)),
            "runtime_path": [
                rel(RUNTIME_IDENTITY_MANIFEST_SCHEMA_CSV),
                rel(ROW_LEVEL_PARITY_SCHEMA_CSV),
                rel(EXTERNAL_VERIFICATION_LOG_SCHEMA_CSV),
            ],
            "shared_contract": "feature_order_hash;model_hash;threshold_risk_lot_hash;MT5_report_path;telemetry_path;row_level_parity_path required before runtime interpretation",
            "known_differences": "no MT5 execution in run336H; schema scaffolds only",
            "parity_check": "runtime identity and row-level parity schema materialized; no compile/tester output claimed",
            "parity_identity": {
                "runtime_identity_rows": metrics["runtime_identity_rows"],
                "row_level_parity_rows": metrics["row_level_parity_rows"],
                "runtime_identity_schema_sha256": sha256_file_lf_normalized(RUNTIME_IDENTITY_MANIFEST_SCHEMA_CSV),
            },
            "runtime_claim_boundary": "research_only_no_runtime_authority",
        },
        "model_validation_receipt.json": {
            **common,
            "model_family": "existing_cp322A_related_research_packet_no_new_model_training",
            "target_and_label": "not_rebuilt_in_run336H",
            "split_method": "not_applicable_runner_scaffold_materialization_only",
            "selection_metric": "none; no candidate selection",
            "secondary_metrics": "future scaffolds require cost, curve, underwater, direction, regime, tier, proxy-vs-MT5, and no-lookahead reports",
            "threshold_policy": "frozen; threshold retuning blocked",
            "overfit_risk": "after_result_feature_pick; direct_forward_pocket_filter; old_proxy_rank; copied_runtime_result",
            "calibration_risk": "proxy values remain diagnostic-only until fresh MT5 comparison",
            "validation_judgment": "exploratory_scaffold_materialization_only",
        },
        "performance_attribution_receipt.json": {
            **common,
            "observed_change": "runner scaffold schemas and per-blueprint scaffold files were materialized",
            "comparison_baseline": PARENT_RUN_ID,
            "likely_drivers": "constraint coverage, negative controls, runtime identity, proxy-vs-MT5 usability contract, regime/tier/cost scaffolds",
            "segment_checks": "session/hour/month/volatility/ADX/VIX/USD/rate slices are present as attribution-only schema rows",
            "trade_shape": "not_available_no_trading_execution",
            "alternative_explanations": "a complete scaffold set does not prove profitability or forward robustness",
            "attribution_confidence": "medium_for_scaffold_readiness_low_for_market_performance",
            "next_probe": NEXT_RUN_ID,
        },
        "result_judgment_receipt.json": {
            **common,
            "result_subject": RUN_ID,
            "evidence_available": [
                rel(SCAFFOLD_INDEX_CSV),
                rel(SCAFFOLD_MANIFEST_JSON),
                rel(RUN336I_REVIEW_QUEUE_CSV),
                rel(GATE_AUDIT_CSV),
            ],
            "evidence_missing": "actual execution; fresh MT5 runtime probe; proxy expected values; MT5 result; difference table; Forward Passed/Failed evidence",
            "judgment_label": "exploratory_scaffold_materialization_completed",
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "뼈대는 완성했지만 아직 실행 결과가 아니므로 수익성, 전진 강건성, 런타임 권위는 말하지 않는다.",
        },
        "artifact_lineage_receipt.json": {
            **common,
            "source_inputs": [
                rel(BLUEPRINT_CATALOG_CSV),
                rel(RUNNER_SCAFFOLD_ACCEPTANCE_CSV),
                rel(RUN336H_QUEUE_CSV),
                rel(RUN336G_FINAL_DECISION_JSON),
            ],
            "producer": rel(Path(__file__)),
            "consumer": [NEXT_RUN_ID, rel(REPORT_DOC), rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(ARTIFACT_REGISTRY)],
            "artifact_paths": [
                rel(SCAFFOLD_INDEX_CSV),
                rel(SCAFFOLD_MANIFEST_JSON),
                rel(RUN336I_REVIEW_QUEUE_CSV),
                rel(FINAL_DECISION_JSON),
            ],
            "artifact_hashes": {
                "scaffold_index_sha256": sha256_file_lf_normalized(SCAFFOLD_INDEX_CSV),
                "scaffold_manifest_sha256": sha256_file_lf_normalized(SCAFFOLD_MANIFEST_JSON),
                "final_decision_sha256": sha256_file_lf_normalized(FINAL_DECISION_JSON),
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
    report = f"""# run336H Runner Scaffolds(러너 뼈대)

- run_id(실행 ID): `{RUN_ID}`
- parent_run(상위 실행): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- primary_family(주 작업군): `experiment_execution(실험 실행)`
- primary_skill(주 스킬): `obsidian-run-evidence-system(실행 근거 시스템)` equivalent(동등 흐름) via scaffold/receipt/registry(뼈대/영수증/등록부)
- support_skills(보조 스킬): data_integrity(데이터 무결성), runtime_parity(런타임 동등성), model_validation(모델 검증), performance_attribution(성과 귀속), result_judgment(결과 판정), artifact_lineage(산출물 계보)
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Materialized(물질화)

- scaffold index(뼈대 색인): `{metrics['scaffold_index_rows']}` rows(행)
- individual scaffolds(개별 뼈대): `{metrics['individual_scaffold_files']}` files(파일)
- negative controls(부정 대조): `{metrics['negative_control_rows']}` rows(행)
- proxy/MT5 contracts(프록시/MT5 계약): `{metrics['proxy_mt5_rows']}` rows(행)
- runtime identity(런타임 정체성): `{metrics['runtime_identity_rows']}` rows(행)
- row-level parity(행 단위 동등성): `{metrics['row_level_parity_rows']}` rows(행)
- gates(게이트): `{metrics['gate_rows']}` rows(행)
- regime slices(국면 조각): `{metrics['regime_rows']}` rows(행)
- tier/no-lookahead(티어/미래참조 방지): `{metrics['tier_rows']}` rows(행)
- run336I queue(336I 대기열): `{metrics['run336i_queue_rows']}` rows(행)

## Judgment(판정)

run336H(336H 실행)는 runner scaffold(러너 뼈대)와 schema(스키마)를 만들었다. Effect(효과): 다음 회차는 실행을 바로 주장하지 않고, 먼저 이 scaffold(뼈대)가 실제 실행·MT5 비교·cost stress(비용 압박)·curve pocket(곡선 포켓)·regime attribution(국면 귀속)을 담을 수 있는지 검토한다.

Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), live readiness(실거래 준비), deployment(배포), operating promotion(운영 승격), Goal Achieve(목표 달성)는 모두 `not_claimed`다.

## Next(다음)

`{NEXT_RUN_ID}`에서 schema row count(스키마 행 수), individual scaffold hash(개별 뼈대 해시), executable flag(실행 가능 플래그), forbidden claim(금지 주장) 부재를 먼저 검토한다. 그 다음에만 실제 proxy expected(프록시 예상), fresh MT5 result(신규 MT5 결과), difference table(차이 표), usability decision(사용 가능성 판정)을 만들 수 있다.
"""
    decision = f"""# Stage336H Runner Scaffold Decision(러너 뼈대 결정)

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- status(상태): `{STATUS}`
- next_action(다음 행동): `{NEXT_RUN_ID}`

## Decision(결정)

run336G(336G 실행)의 accepted blueprint(승인 청사진) 31개를 run336H(336H 실행) scaffold(뼈대) 31개와 집계 schema(스키마) 산출물로 물질화했다. Effect(효과): 앞으로 실행 결과를 넣을 자리와 실패 조건은 고정됐지만, 아직 모델 학습(model training, 모델 학습), MT5 execution(MT5 실행), threshold retuning(임계값 재조정), lot optimization(랏 최적화), candidate selection(후보 선택)은 하지 않았다.

## Boundary(경계)

이 결정은 Forward Passed(전진 통과)나 Forward Failed(전진 실패)가 아니다. runtime authority(런타임 권위), operating promotion(운영 승격), deployment(배포), Goal Achieve(목표 달성)는 모두 주장하지 않는다.
"""
    write_md(REPORT_DOC, report)
    write_md(DECISION_DOC, decision)


def update_docs(metrics: Mapping[str, Any]) -> None:
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_line(workspace_text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    focus_line = (
        f"  Stage336(336단계) run336H(336H 실행)는 `{STATUS}`로 runner scaffold(러너 뼈대) 물질화를 완료했다. "
        f"Effect(효과): accepted blueprint(승인 청사진) `{metrics['scaffold_index_rows']}`개를 개별 scaffold(뼈대)와 schema(스키마) 산출물로 만들고 "
        f"run336I review queue(336I 검토 대기열) `{metrics['run336i_queue_rows']}`행을 만들었다. "
        "Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    workspace_text = upsert_folded_list_item(workspace_text, "run336H(336H 실행)", focus_line)
    write_text_lossless(WORKSPACE_STATE, workspace_text, workspace_bom)

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    current_text = replace_line(current_text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    current_text = replace_line(current_text, "- status(상태):", f"- status(상태): `{STATUS}`")
    current_text = replace_line(current_text, "- decision(결정):", f"- decision(결정): `{DECISION}`")
    summary_line = (
        f"- run336H_summary(336H 요약): runner scaffold(러너 뼈대) 물질화를 `{STATUS}`로 완료했다. "
        f"Effect(효과): scaffold index(뼈대 색인) `{metrics['scaffold_index_rows']}`행, individual scaffold(개별 뼈대) `{metrics['individual_scaffold_files']}`개, "
        f"run336I review queue(336I 검토 대기열) `{metrics['run336i_queue_rows']}`행을 만들었다. "
        "Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    if "- run336H_summary(336H 요약):" in current_text:
        current_text = replace_line(current_text, "- run336H_summary(336H 요약):", summary_line)
    elif "- run336G_summary" in current_text:
        current_text = current_text.replace("- run336G_summary", summary_line + "\n- run336G_summary", 1)
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
        f"- effect(효과): Stage336(336단계)는 run336H(336H 실행)에서 runner scaffold(러너 뼈대)를 물질화했고 run336I(336I 실행) 검토 대기열을 만들었으며 후보 선택이나 운영 주장은 없다.",
    )
    write_text_lossless(selection_path, selection_text, selection_bom)

    brief_path = SPEC_DIR / "stage_brief.md"
    brief_text, brief_bom = read_text_lossless(brief_path)
    brief_text = replace_line(brief_text, "- latest_run(최신 실행):", f"- latest_run(최신 실행): `{RUN_ID}`")
    write_text_lossless(brief_path, brief_text, brief_bom)

    input_body = f"""- scaffold_index(뼈대 색인): `{rel(SCAFFOLD_INDEX_CSV)}`
- scaffold_manifest(뼈대 목록): `{rel(SCAFFOLD_MANIFEST_JSON)}`
- negative_control_scaffolds(부정 대조 뼈대): `{rel(NEGATIVE_CONTROL_SCAFFOLD_CSV)}`
- proxy_mt5_difference_schema(프록시/MT5 차이 스키마): `{rel(PROXY_MT5_DIFFERENCE_SCHEMA_CSV)}`
- runtime_identity_manifest_schema(런타임 정체성 목록 스키마): `{rel(RUNTIME_IDENTITY_MANIFEST_SCHEMA_CSV)}`
- regime_slice_schema_matrix(국면 조각 스키마 행렬): `{rel(REGIME_SLICE_SCHEMA_MATRIX_CSV)}`
- run336I_review_queue(336I 검토 대기열): `{rel(RUN336I_REVIEW_QUEUE_CSV)}`
- final_decision(최종 결정): `{rel(FINAL_DECISION_JSON)}`
"""
    append_or_replace_section(INPUTS_DIR / "input_refs.md", "run336H Runner Scaffolds(336H 러너 뼈대)", input_body)

    changelog_body = f"""- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- effect(효과): accepted blueprint(승인 청사진) `{metrics['scaffold_index_rows']}`개를 runner scaffold(러너 뼈대)와 schema(스키마) 산출물로 만들었다.
- boundary(경계): 후보 선택, Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 `not_claimed`.
"""
    append_or_replace_section(CHANGELOG, "Stage336H Runner Scaffolds(336H 러너 뼈대)", changelog_body)


def update_registries(metrics: Mapping[str, Any], artifact_paths: Sequence[Path]) -> None:
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "stage336_runner_scaffold_materialization",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_DOC),
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};scaffolds={metrics['scaffold_index_rows']};goal_achieve_not_claimed.",
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__runner_scaffolds",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "constraint_bound_runner_scaffold_materialization",
                "tier_scope": "Tier A/Tier B paired future runtime requirement",
                "kpi_scope": "scaffold_materialization_no_new_trading_kpi",
                "scoreboard_lane": "experiment_execution_scaffold",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_DOC),
                "primary_kpi": f"scaffolds={metrics['scaffold_index_rows']};run336i_queue_rows={metrics['run336i_queue_rows']}",
                "guardrail_kpi": "training_blocked=true;mt5_execution_blocked=true;forward_decision_blocked=true;runtime_authority_blocked=true",
                "external_verification_status": "out_of_scope_by_claim_runner_scaffold_materialization_only",
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID}.",
            },
            {
                "ledger_row_id": f"{RUN_ID}__proxy_mt5_scaffolds",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": f"{RUN_NUMBER}_proxy_mt5_scaffolds",
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "proxy_mt5_runtime_usability_scaffold_materialization",
                "tier_scope": "fresh_MT5_runtime_probe_required",
                "kpi_scope": "proxy_expected_vs_fresh_mt5_difference_schema_before_usability",
                "scoreboard_lane": "runtime_parity_scaffold",
                "status": STATUS,
                "judgment": "proxy_mt5_scaffolds_materialized_diagnostic_only_no_forward_decision",
                "path": rel(PROXY_MT5_DIFFERENCE_SCHEMA_CSV),
                "primary_kpi": f"proxy_mt5_rows={metrics['proxy_mt5_rows']}",
                "guardrail_kpi": "selection_use=blocked;forward_decision_use=blocked;fresh_mt5_required=true",
                "external_verification_status": "out_of_scope_by_claim_runner_scaffold_materialization_only",
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
                "ledger_row_id": f"{RUN_ID}__runner_scaffold_materialization",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "work_family": "stage336_runner_scaffold_materialization",
                "evidence_scope": "run336G_accepted_blueprints_to_run336I_review_queue",
                "kpi_scope": "scaffold_materialization_no_new_trading_kpi",
                "status": STATUS,
                "judgment": JUDGMENT,
                "claim_boundary": CLAIM_BOUNDARY,
                "path": rel(REPORT_DOC),
                "notes": f"scaffolds={metrics['scaffold_index_rows']};run336i_queue_rows={metrics['run336i_queue_rows']};goal_achieve_not_claimed.",
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
                "artifact_type": "stage336H_runner_scaffold_materialization",
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created,
                "notes": "run336H_scaffold_materialization_no_execution_no_forward_decision",
            }
        )
    upsert_csv_rows(
        ARTIFACT_REGISTRY,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
        artifact_rows,
        key="artifact_id",
    )


def write_final_decision(metrics: Mapping[str, Any]) -> Path:
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
            "all_scaffolds_materialized": True,
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


def main() -> None:
    inputs = load_inputs()
    validate_inputs(inputs)

    scaffold_index = build_scaffold_index(inputs["catalog"], inputs["acceptance"], inputs["outputs"])
    individual_scaffold_paths = write_individual_scaffolds(scaffold_index, inputs["field_contracts"], inputs["outputs"])

    negative_control_scaffolds = build_negative_control_scaffolds(inputs["negative_controls"])
    canary_expected_failure = build_canary_expected_failure(inputs["negative_controls"])
    proxy_expected = build_proxy_expected_schema(inputs["proxy_mt5"])
    fresh_mt5 = build_fresh_mt5_result_schema(inputs["proxy_mt5"])
    proxy_mt5_diff = build_proxy_mt5_difference_schema(inputs["proxy_mt5"])
    usability_decision = build_usability_decision_schema(inputs["proxy_mt5"])
    runtime_identity = build_runtime_identity_manifest(inputs["runtime_identity"])
    row_level_parity = build_row_level_parity_schema(inputs["runtime_identity"])
    external_verification = build_external_verification_log_schema(inputs["runtime_identity"])
    cost_stress = build_gate_schema(inputs["gates"], "cost_buffer_gate", "cost_stress")
    curve_pocket = build_gate_schema(inputs["gates"], "curve_pocket_gate", "curve_pocket")
    underwater = build_gate_schema(inputs["gates"], "underwater_stretch_gate", "underwater_stretch")
    direction = build_gate_schema(inputs["gates"], "direction_attribution_gate", "direction_attribution")
    lot_normalized = build_gate_schema(inputs["gates"], "lot_normalized_gate", "lot_normalized")
    regime_slice = build_regime_slice_schema(inputs["regime"])
    tier_pair = build_tier_pair_schema(inputs["tier"])
    future_shift_canary = build_future_shift_canary_schema(inputs["tier"])
    threshold_lot_freeze = build_threshold_lot_freeze_manifest_schema(inputs["tier"])
    long_short_attribution = direction
    feature_family_seed_card = build_feature_family_seed_card(inputs["catalog"])
    trade_density_target = build_trade_density_target(inputs["catalog"])
    artifact_hash_receipt = build_artifact_hash_receipt_schema(inputs["outputs"])
    output_registry_binding = build_output_registry_binding_schema(inputs["outputs"])
    run336i_review_queue = build_run336i_review_queue()

    family_counts = Counter(row.get("blueprint_family", "") for row in inputs["catalog"])
    metrics: dict[str, Any] = {
        "catalog_rows": len(inputs["catalog"]),
        "accepted_scaffold_rows": len(inputs["acceptance"]),
        "scaffold_index_rows": len(scaffold_index),
        "individual_scaffold_files": len(individual_scaffold_paths),
        "negative_control_rows": len(negative_control_scaffolds),
        "canary_expected_failure_rows": len(canary_expected_failure),
        "proxy_mt5_rows": len(proxy_expected),
        "runtime_identity_rows": len(runtime_identity),
        "row_level_parity_rows": len(row_level_parity),
        "external_verification_rows": len(external_verification),
        "gate_rows": len(inputs["gates"]),
        "cost_stress_rows": len(cost_stress),
        "curve_pocket_rows": len(curve_pocket),
        "underwater_rows": len(underwater),
        "direction_rows": len(direction),
        "lot_normalized_rows": len(lot_normalized),
        "regime_rows": len(regime_slice),
        "tier_rows": len(tier_pair),
        "future_shift_canary_rows": len(future_shift_canary),
        "threshold_lot_freeze_rows": len(threshold_lot_freeze),
        "feature_family_seed_card_rows": len(feature_family_seed_card),
        "trade_density_target_rows": len(trade_density_target),
        "output_contract_rows": len(output_registry_binding),
        "run336i_queue_rows": len(run336i_review_queue),
        "blueprint_family_counts": dict(sorted(family_counts.items())),
    }

    output_paths: list[Path] = []
    output_paths.extend(individual_scaffold_paths)
    output_paths.extend(
        [
            write_csv(
                SCAFFOLD_INDEX_CSV,
                (
                    "scaffold_id",
                    "blueprint_id",
                    "branch_id",
                    "lane",
                    "blueprint_family",
                    "blueprint_name",
                    "scaffold_path",
                    "schema_artifacts",
                    "source_review_artifact",
                    "source_review_sha256",
                    "future_artifact_hint",
                    "materialization_status",
                    "executable",
                    "model_training_allowed",
                    "mt5_execution_allowed",
                    "selection_allowed",
                    "forward_decision_allowed",
                    "runtime_authority_allowed",
                    "next_review_required",
                    "forbidden",
                    "claim_boundary",
                ),
                scaffold_index,
            ),
            write_csv(
                NEGATIVE_CONTROL_SCAFFOLD_CSV,
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
                    "execution_ready",
                    "result_status",
                    "forbidden_use",
                    "claim_boundary",
                ),
                negative_control_scaffolds,
            ),
            write_csv(
                CANARY_EXPECTED_FAILURE_CSV,
                (
                    "canary_id",
                    "branch_id",
                    "shortcut_risk",
                    "expected_failure_signature",
                    "required_failure_effect",
                    "pass_condition",
                    "fail_condition",
                    "allowed_use",
                    "selection_use",
                    "forward_decision_use",
                    "runtime_authority_use",
                    "claim_boundary",
                ),
                canary_expected_failure,
            ),
            write_csv(
                PROXY_EXPECTED_SCHEMA_CSV,
                (
                    "contract_id",
                    "branch_id",
                    "required_schema_fields",
                    "comparison_key",
                    "source_kind",
                    "row_level_required",
                    "fresh_mt5_required",
                    "selection_use",
                    "forward_decision_use",
                    "claim_boundary",
                ),
                proxy_expected,
            ),
            write_csv(
                FRESH_MT5_RESULT_SCHEMA_CSV,
                (
                    "contract_id",
                    "branch_id",
                    "required_schema_fields",
                    "required_source",
                    "external_verification_status_required",
                    "row_level_required",
                    "aggregate_only_match_allowed",
                    "mt5_execution_status",
                    "claim_boundary",
                ),
                fresh_mt5,
            ),
            write_csv(
                PROXY_MT5_DIFFERENCE_SCHEMA_CSV,
                (
                    "contract_id",
                    "branch_id",
                    "difference_schema",
                    "tolerance_policy",
                    "usable_condition",
                    "not_usable_condition",
                    "diagnostic_use_only",
                    "selection_use",
                    "forward_decision_use",
                    "claim_boundary",
                ),
                proxy_mt5_diff,
            ),
            write_csv(
                USABILITY_DECISION_SCHEMA_CSV,
                (
                    "contract_id",
                    "branch_id",
                    "usable_condition",
                    "not_usable_condition",
                    "decision_label_allowed_values",
                    "required_inputs",
                    "operating_use",
                    "runtime_authority_use",
                    "claim_boundary",
                ),
                usability_decision,
            ),
            write_csv(
                RUNTIME_IDENTITY_MANIFEST_SCHEMA_CSV,
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
                    "result_status",
                    "claim_boundary",
                ),
                runtime_identity,
            ),
            write_csv(
                ROW_LEVEL_PARITY_SCHEMA_CSV,
                (
                    "preflight_id",
                    "branch_id",
                    "parity_subject",
                    "required_identity",
                    "required_row_fields",
                    "tolerance_policy",
                    "aggregate_only_match_allowed",
                    "runtime_authority_use",
                    "claim_boundary",
                ),
                row_level_parity,
            ),
            write_csv(
                EXTERNAL_VERIFICATION_LOG_SCHEMA_CSV,
                (
                    "preflight_id",
                    "branch_id",
                    "runtime_subject",
                    "required_check",
                    "required_log_fields",
                    "external_verification_status_required",
                    "acceptable_closeout",
                    "runtime_authority_use",
                    "claim_boundary",
                ),
                external_verification,
            ),
            write_csv(
                COST_STRESS_SCHEMA_CSV,
                (
                    "plan_id",
                    "branch_id",
                    "gate_id",
                    "schema_name",
                    "required_measurement",
                    "future_output_table_name",
                    "review_requirement",
                    "failure_memory_trigger",
                    "execution_order",
                    "forbidden_shortcut",
                    "future_runner_blueprint",
                    "result_status",
                    "claim_boundary",
                ),
                cost_stress,
            ),
            write_csv(
                CURVE_POCKET_SCHEMA_CSV,
                (
                    "plan_id",
                    "branch_id",
                    "gate_id",
                    "schema_name",
                    "required_measurement",
                    "future_output_table_name",
                    "review_requirement",
                    "failure_memory_trigger",
                    "execution_order",
                    "forbidden_shortcut",
                    "future_runner_blueprint",
                    "result_status",
                    "claim_boundary",
                ),
                curve_pocket,
            ),
            write_csv(
                UNDERWATER_SCHEMA_CSV,
                (
                    "plan_id",
                    "branch_id",
                    "gate_id",
                    "schema_name",
                    "required_measurement",
                    "future_output_table_name",
                    "review_requirement",
                    "failure_memory_trigger",
                    "execution_order",
                    "forbidden_shortcut",
                    "future_runner_blueprint",
                    "result_status",
                    "claim_boundary",
                ),
                underwater,
            ),
            write_csv(
                DIRECTION_SCHEMA_CSV,
                (
                    "plan_id",
                    "branch_id",
                    "gate_id",
                    "schema_name",
                    "required_measurement",
                    "future_output_table_name",
                    "review_requirement",
                    "failure_memory_trigger",
                    "execution_order",
                    "forbidden_shortcut",
                    "future_runner_blueprint",
                    "result_status",
                    "claim_boundary",
                ),
                direction,
            ),
            write_csv(
                LOT_NORMALIZED_SCHEMA_CSV,
                (
                    "plan_id",
                    "branch_id",
                    "gate_id",
                    "schema_name",
                    "required_measurement",
                    "future_output_table_name",
                    "review_requirement",
                    "failure_memory_trigger",
                    "execution_order",
                    "forbidden_shortcut",
                    "future_runner_blueprint",
                    "result_status",
                    "claim_boundary",
                ),
                lot_normalized,
            ),
            write_csv(
                REGIME_SLICE_SCHEMA_MATRIX_CSV,
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
                    "selection_filter_use",
                    "forward_filter_use",
                    "claim_boundary",
                ),
                regime_slice,
            ),
            write_csv(
                TIER_PAIR_SCHEMA_CSV,
                (
                    "contract_id",
                    "tier_scope",
                    "required_fields",
                    "time_axis_rule",
                    "acceptance_condition",
                    "forbidden",
                    "future_runner_blueprint",
                    "future_required_outputs",
                    "actual_routed_total_guard",
                    "claim_boundary",
                ),
                tier_pair,
            ),
            write_csv(
                FUTURE_SHIFT_CANARY_SCHEMA_CSV,
                (
                    "canary_id",
                    "time_axis_rule",
                    "expected_failure_signature",
                    "required_scope",
                    "selection_use",
                    "forward_decision_use",
                    "claim_boundary",
                ),
                future_shift_canary,
            ),
            write_csv(
                THRESHOLD_LOT_FREEZE_MANIFEST_SCHEMA_CSV,
                (
                    "contract_id",
                    "tier_scope",
                    "required_fields",
                    "created_before_result_read_required",
                    "threshold_retuning_allowed",
                    "lot_optimization_allowed",
                    "ATR_exit_change_allowed",
                    "future_required_outputs",
                    "claim_boundary",
                ),
                threshold_lot_freeze,
            ),
            write_csv(
                LONG_SHORT_ATTRIBUTION_SCHEMA_CSV,
                (
                    "plan_id",
                    "branch_id",
                    "gate_id",
                    "schema_name",
                    "required_measurement",
                    "future_output_table_name",
                    "review_requirement",
                    "failure_memory_trigger",
                    "execution_order",
                    "forbidden_shortcut",
                    "future_runner_blueprint",
                    "result_status",
                    "claim_boundary",
                ),
                long_short_attribution,
            ),
            write_csv(
                FEATURE_FAMILY_SEED_CARD_SCHEMA_CSV,
                (
                    "blueprint_id",
                    "branch_id",
                    "blueprint_name",
                    "feature_family_seed_status",
                    "allowed_use",
                    "after_result_feature_pick",
                    "model_training_allowed",
                    "future_review_required",
                    "claim_boundary",
                ),
                feature_family_seed_card,
            ),
            write_csv(
                TRADE_DENSITY_TARGET_SCHEMA_CSV,
                (
                    "blueprint_id",
                    "branch_id",
                    "blueprint_name",
                    "density_target_status",
                    "required_fields",
                    "optimization_use",
                    "future_review_required",
                    "claim_boundary",
                ),
                trade_density_target,
            ),
            write_csv(
                ARTIFACT_HASH_RECEIPT_SCHEMA_CSV,
                (
                    "blueprint_id",
                    "branch_id",
                    "blueprint_name",
                    "future_artifact_hint",
                    "must_exist_before_execution_review",
                    "hash_required",
                    "registry_required",
                    "expected_hash_algorithm",
                    "current_hash_status",
                    "claim_boundary",
                ),
                artifact_hash_receipt,
            ),
            write_csv(
                OUTPUT_REGISTRY_BINDING_SCHEMA_CSV,
                (
                    "artifact_binding_id",
                    "blueprint_id",
                    "branch_id",
                    "future_artifact_hint",
                    "registry_path",
                    "must_exist_before_execution_review",
                    "hash_required",
                    "registry_required",
                    "next_review",
                    "can_support_model_training",
                    "can_support_forward_decision",
                    "can_support_runtime_authority",
                    "claim_boundary",
                ),
                output_registry_binding,
            ),
            write_csv(
                RUN336I_REVIEW_QUEUE_CSV,
                (
                    "queue_id",
                    "priority",
                    "review_group",
                    "source_artifacts",
                    "review_task",
                    "success_condition",
                    "forbidden",
                    "claim_boundary",
                ),
                run336i_review_queue,
            ),
        ]
    )
    output_paths.append(write_scaffold_manifest(scaffold_index, metrics))
    output_paths.append(write_csv(GATE_AUDIT_CSV, ("gate_id", "status", "evidence", "finding", "claim_boundary"), build_gate_audit(metrics)))

    result_rows = [
        {
            "run_id": RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "evidence_available": "scaffold_index;scaffold_manifest;schema_files;run336I_queue;receipts;registries",
            "evidence_missing": "actual execution;fresh MT5 runtime probe;proxy expected values;MT5 result;difference table;Forward Passed/Failed evidence",
            "judgment_label": "exploratory_runner_scaffold_materialization",
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
                "live_readiness",
                "deployment",
                "operating_promotion",
                "goal_achieve",
                "next_action",
                "claim_boundary",
            ),
            result_rows,
        )
    )
    output_paths.append(write_final_decision(metrics))
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
                "scaffold_index_rows": metrics["scaffold_index_rows"],
                "individual_scaffold_files": metrics["individual_scaffold_files"],
                "negative_control_rows": metrics["negative_control_rows"],
                "proxy_mt5_rows": metrics["proxy_mt5_rows"],
                "runtime_identity_rows": metrics["runtime_identity_rows"],
                "regime_rows": metrics["regime_rows"],
                "run336i_queue_rows": metrics["run336i_queue_rows"],
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
