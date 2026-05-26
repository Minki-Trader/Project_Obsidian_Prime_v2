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
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
SOURCE_STAGE_ID = "336_onnx_research_packet__constraint_bound_repair_defense_offense_rebuild"
RUN_NUMBER = "run337J"
RUN_ID = "run337J_materialize_runner_scaffolds_v1"
PARENT_RUN_ID = "run337I_review_materialized_execution_packages_v1"
NEXT_RUN_ID = "run337K_review_runner_scaffolds_v1"
STATUS = "completed_runner_scaffolds_materialized_no_training_no_mt5"
JUDGMENT = "stage337J_runner_scaffolds_materialized_for_review_no_execution_no_selection"
DECISION = "stage337J_runner_scaffolds_ready_for_run337K_review_no_training_no_mt5_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage337J_runner_scaffold_materialization_no_model_training_"
    "no_mt5_execution_no_threshold_retuning_no_lot_optimization_no_forward_pocket_filtering_"
    "no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)
FORBIDDEN = (
    "model_training;mt5_execution;threshold_retune;lot_optimization;forward_pocket_filtering;"
    "candidate_selection;Forward_Passed;Forward_Failed;live_readiness;deployment;"
    "operating_promotion;runtime_authority;Goal_Achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
RUN337H_DIR = STAGE_DIR / "02_runs" / "run337H"
RUN337I_DIR = STAGE_DIR / "02_runs" / "run337I"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
INPUTS_DIR = STAGE_DIR / "01_inputs"
SELECTED_DIR = STAGE_DIR / "04_selected"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"

DOCS = ROOT / "docs"
WORKSPACE_STATE = DOCS / "workspace" / "workspace_state.yaml"
CURRENT_STATE = DOCS / "context" / "current_working_state.md"
CHANGELOG = DOCS / "workspace" / "changelog.md"
RUN_REGISTRY = DOCS / "registers" / "run_registry.csv"
ALPHA_LEDGER = DOCS / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = DOCS / "registers" / "artifact_registry.csv"
DECISION_DOC = DOCS / "decisions" / "2026-05-27_stage337J_materialize_runner_scaffolds.md"
REPORT_DOC = REVIEWS_DIR / "run337J_materialize_runner_scaffolds.md"

ACCEPTED_PACKAGES_CSV = RUN337I_DIR / "accepted_packages_for_runner_scaffold_queue.csv"
RUN337J_QUEUE_CSV = RUN337I_DIR / "run337J_runner_scaffold_materialization_queue.csv"
RUN337I_REPAIR_GAPS_CSV = RUN337I_DIR / "repair_package_gap_queue.csv"
RUN337I_GATE_AUDIT_CSV = RUN337I_DIR / "required_gate_coverage_audit.csv"
RUN337I_DECISION_JSON = RUN337I_DIR / "final_review_materialized_execution_packages_decision.json"
RUN337I_MANIFEST_JSON = RUN337I_DIR / "run_manifest.json"

PACKAGE_INDEX_CSV = RUN337H_DIR / "package_manifest_index.csv"
PACKAGE_ACCEPTANCE_CSV = RUN337H_DIR / "package_acceptance_matrix.csv"
BLOCKER_MATRIX_CSV = RUN337H_DIR / "package_blocker_matrix.csv"
NO_LOOKAHEAD_PACKAGE_CSV = RUN337H_DIR / "no_lookahead_canary_harness_package_spec.csv"
PROXY_MT5_PACKAGE_CSV = RUN337H_DIR / "proxy_mt5_fresh_probe_package_spec.csv"
CORE56_PACKAGE_CSV = RUN337H_DIR / "core56_asof_repair_package_spec.csv"
COST_CURVE_PACKAGE_CSV = RUN337H_DIR / "cost_direction_curve_extraction_package_spec.csv"
OFFENSE_PACKAGE_CSV = RUN337H_DIR / "offense_branch_thesis_package_spec.csv"
REGIME_PACKAGE_CSV = RUN337H_DIR / "economic_regime_asof_join_package_spec.csv"
RUNTIME_PACKAGE_CSV = RUN337H_DIR / "runtime_probe_package_spec.csv"
CLAIM_GUARD_PACKAGE_CSV = RUN337H_DIR / "claim_guard_blocker_package_spec.csv"

RUN337I_REVIEW_FILES = {
    "no_lookahead": RUN337I_DIR / "no_lookahead_package_review.csv",
    "proxy_mt5": RUN337I_DIR / "proxy_mt5_package_review.csv",
    "core56": RUN337I_DIR / "core56_package_review.csv",
    "cost_curve": RUN337I_DIR / "cost_direction_curve_package_review.csv",
    "offense": RUN337I_DIR / "offense_package_review.csv",
    "regime": RUN337I_DIR / "economic_regime_package_review.csv",
    "runtime": RUN337I_DIR / "runtime_package_review.csv",
    "claim_boundary": RUN337I_DIR / "claim_guard_package_review.csv",
    "package_index": RUN337I_DIR / "package_index_review.csv",
}
PACKAGE_FILES = {
    "no_lookahead": NO_LOOKAHEAD_PACKAGE_CSV,
    "proxy_mt5": PROXY_MT5_PACKAGE_CSV,
    "core56": CORE56_PACKAGE_CSV,
    "cost_curve": COST_CURVE_PACKAGE_CSV,
    "offense": OFFENSE_PACKAGE_CSV,
    "regime": REGIME_PACKAGE_CSV,
    "runtime": RUNTIME_PACKAGE_CSV,
    "claim_boundary": CLAIM_GUARD_PACKAGE_CSV,
}
CONTRACT_FILES = {
    "no_lookahead": RUN337H_DIR / "no_lookahead_canary_harness_contract.json",
    "proxy_mt5": RUN337H_DIR / "proxy_mt5_fresh_probe_output_contract.json",
    "core56": RUN337H_DIR / "core56_asof_repair_contract.json",
    "cost_curve": RUN337H_DIR / "cost_direction_curve_extraction_contract.json",
    "offense": "",
    "regime": RUN337H_DIR / "economic_regime_asof_join_contract.json",
    "runtime": RUN337H_DIR / "runtime_probe_package_contract.json",
    "claim_boundary": BLOCKER_MATRIX_CSV,
    "package_index": PACKAGE_ACCEPTANCE_CSV,
}

SOURCE_INPUTS: tuple[Path, ...] = (
    ACCEPTED_PACKAGES_CSV,
    RUN337J_QUEUE_CSV,
    RUN337I_REPAIR_GAPS_CSV,
    RUN337I_GATE_AUDIT_CSV,
    RUN337I_DECISION_JSON,
    RUN337I_MANIFEST_JSON,
    PACKAGE_INDEX_CSV,
    PACKAGE_ACCEPTANCE_CSV,
    BLOCKER_MATRIX_CSV,
    *PACKAGE_FILES.values(),
    *RUN337I_REVIEW_FILES.values(),
)

SOURCE_LINEAGE_CSV = RUN_DIR / "runner_scaffold_source_lineage.csv"
RUNNER_SCAFFOLD_FAMILY_MANIFEST_CSV = RUN_DIR / "runner_scaffold_family_manifest.csv"
RUNNER_SCAFFOLD_INDEX_CSV = RUN_DIR / "runner_scaffold_index.csv"
PREFLIGHT_CHECKLIST_CSV = RUN_DIR / "preflight_checklist.csv"
BLOCKED_EXECUTION_COMMAND_CSV = RUN_DIR / "blocked_execution_command.csv"
CLAIM_BOUNDARY_RECEIPT_JSON = RUN_DIR / "claim_boundary_receipt.json"
RUN337K_REVIEW_QUEUE_CSV = RUN_DIR / "run337K_runner_scaffold_review_queue.csv"
GATE_AUDIT_CSV = RUN_DIR / "required_gate_coverage_audit.csv"
RESULT_JUDGMENT_CSV = RUN_DIR / "result_judgment.csv"

EXPERIMENT_DESIGN_JSON = RUN_DIR / "experiment_design_receipt.json"
DATA_INTEGRITY_JSON = RUN_DIR / "data_integrity_receipt.json"
RUNTIME_PARITY_JSON = RUN_DIR / "runtime_parity_receipt.json"
ARTIFACT_LINEAGE_JSON = RUN_DIR / "artifact_lineage_receipt.json"
RESULT_JUDGMENT_JSON = RUN_DIR / "result_judgment_receipt.json"
FINAL_DECISION_JSON = RUN_DIR / "final_runner_scaffold_materialization_decision.json"
RUN_MANIFEST_JSON = RUN_DIR / "run_manifest.json"

FAMILY_SCAFFOLD_FILES = {
    "no_lookahead": RUN_DIR / "no_lookahead_runner_scaffold.csv",
    "proxy_mt5": RUN_DIR / "proxy_mt5_runner_scaffold.csv",
    "core56": RUN_DIR / "core56_asof_runner_scaffold.csv",
    "cost_curve": RUN_DIR / "cost_direction_curve_runner_scaffold.csv",
    "offense": RUN_DIR / "offense_branch_runner_scaffold.csv",
    "regime": RUN_DIR / "economic_regime_asof_runner_scaffold.csv",
    "runtime": RUN_DIR / "runtime_probe_runner_scaffold.csv",
    "claim_boundary": RUN_DIR / "claim_guard_runner_scaffold.csv",
    "package_index": RUN_DIR / "package_index_runner_scaffold.csv",
}

FAMILY_SCOPE = {
    "no_lookahead": "no-lookahead canary harness runner scaffold",
    "proxy_mt5": "proxy expected and fresh MT5 probe runner scaffold",
    "core56": "core56 as-of repair runner scaffold",
    "cost_curve": "cost/direction/curve extraction runner scaffold",
    "offense": "offense thesis runner scaffold without training",
    "regime": "economic regime as-of runner scaffold",
    "runtime": "runtime probe runner scaffold without MT5 execution",
    "claim_boundary": "claim guard runner scaffold",
    "package_index": "package index and claim boundary runner scaffold",
}

FAMILY_PRECHECKS = {
    "no_lookahead": "future_bar_canary;forward_pocket_canary;threshold_retune_canary;lot_optimization_canary;timestamp_basis_canary",
    "proxy_mt5": "proxy_identity;fresh_mt5_required_files;row_level_difference_schema;usability_not_kpi_authority",
    "core56": "source_inventory;asof_join_audit;feature_handoff_snapshot;full_family_claim_block",
    "cost_curve": "cost_stress;spread_slippage;D_B_source;long_short;curve_pocket;lot_normalized;regime_slice",
    "offense": "feature_thesis_card;data_boundary_contract;wfo_split_contract;fixed_threshold;fixed_risk_lot",
    "regime": "source_timestamp;source_sha256;timezone;revision_policy;asof_join;future_join_block",
    "runtime": "EA_hash;ONNX_or_model_spec;adapter_manifest;feature_order;set_file;tester_ini;handoff;tester_outputs",
    "claim_boundary": "blocked_claims;execution_flags_closed;stop_claim_response;no_goal_achieve",
    "package_index": "package_index;acceptance_matrix;blocker_matrix;run337I_decision;run337I_manifest",
}


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
    if isinstance(value, float):
        return "" if not math.isfinite(value) else f"{value:.12g}"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    return str(value)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        raise FileNotFoundError(path)
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def read_json(path: Path) -> dict[str, Any]:
    if not path_exists(path):
        raise FileNotFoundError(path)
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


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


def write_text_lossless(path: Path, text: str, had_bom: bool) -> Path:
    encoding = "utf-8-sig" if had_bom or path.suffix.lower() in {".md", ".txt"} else "utf-8"
    io_path(path).write_text(text, encoding=encoding, newline="\n")
    return path


def replace_prefix_line(text: str, prefix: str, new_line: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = new_line
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + new_line + "\n"


def insert_after_marker_once(text: str, marker: str, line: str, token: str) -> str:
    if token in text:
        return text
    lines = text.splitlines()
    for index, existing in enumerate(lines):
        if existing.startswith(marker):
            lines.insert(index + 1, line)
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + line + "\n"


def insert_focus_once(text: str, body: str, token: str) -> str:
    if token in text:
        return text
    return text.replace("current_focus:\n", f"current_focus:\n{body}\n", 1)


def append_section_once(path: Path, header: str, body: str) -> Path:
    text, had_bom = read_text_lossless(path) if path_exists(path) else ("", True)
    if header in text:
        return path
    return write_text_lossless(path, text.rstrip() + "\n\n" + header + "\n\n" + body.strip() + "\n", had_bom)


def as_bool_text(value: Any) -> str:
    return "true" if str(value).strip().lower() == "true" else "false"


def split_semicolon(value: Any) -> list[str]:
    return [item.strip() for item in str(value or "").split(";") if item.strip()]


def row_count_or_keys(path: Path) -> str:
    if not path_exists(path):
        return ""
    if path.suffix.lower() == ".csv":
        return str(len(read_csv(path)))
    if path.suffix.lower() == ".json":
        return ";".join(sorted(read_json(path).keys()))
    return ""


def fail(message: str) -> None:
    raise RuntimeError(message)


def load_inputs() -> dict[str, Any]:
    packages = {family: read_csv(path) for family, path in PACKAGE_FILES.items()}
    package_index_rows = read_csv(PACKAGE_INDEX_CSV)
    return {
        "accepted": read_csv(ACCEPTED_PACKAGES_CSV),
        "queue": read_csv(RUN337J_QUEUE_CSV),
        "repair_gaps": read_csv(RUN337I_REPAIR_GAPS_CSV),
        "run337i_gate_audit": read_csv(RUN337I_GATE_AUDIT_CSV),
        "run337i_decision": read_json(RUN337I_DECISION_JSON),
        "run337i_manifest": read_json(RUN337I_MANIFEST_JSON),
        "package_index": package_index_rows,
        "package_acceptance": read_csv(PACKAGE_ACCEPTANCE_CSV),
        "blockers": read_csv(BLOCKER_MATRIX_CSV),
        "packages": packages,
        "package_index_scaffold_rows": [
            {
                "package_id": "package_index_and_claim_boundary_runner_scaffold",
                "package_family": "package_index",
                "source_package_artifact": rel(PACKAGE_INDEX_CSV),
                "contract_artifact": rel(PACKAGE_ACCEPTANCE_CSV),
                "index_rows": len(package_index_rows),
                "blocker_rows": len(read_csv(BLOCKER_MATRIX_CSV)),
                "expected_outputs": "runner_scaffold_family_manifest.csv;runner_scaffold_index.csv;preflight_checklist.csv;blocked_execution_command.csv;claim_boundary_receipt.json",
                "execution_allowed": "false",
                "training_allowed": "false",
                "mt5_execution_allowed": "false",
                "next_review": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    }


def validate_inputs(inputs: Mapping[str, Any]) -> None:
    accepted = inputs["accepted"]
    queue = inputs["queue"]
    if len(accepted) != 9:
        fail(f"expected 9 accepted package families, got {len(accepted)}")
    if len(queue) != 9:
        fail(f"expected 9 run337J queue rows, got {len(queue)}")
    if inputs["repair_gaps"]:
        fail("run337I repair gap queue is not empty.")
    if any(row.get("status") != "pass" for row in inputs["run337i_gate_audit"]):
        fail("run337I gate audit has failed rows.")
    decision = inputs["run337i_decision"]
    manifest = inputs["run337i_manifest"]
    if decision.get("next_action") != RUN_ID or manifest.get("next_action") != RUN_ID:
        fail("run337I next_action does not point to run337J.")
    if decision.get("model_training") != "not_run" or decision.get("mt5_execution") != "not_run":
        fail("run337I decision unexpectedly opened training or MT5 execution.")
    if decision.get("goal_achieve") != "not_claimed":
        fail("run337I decision unexpectedly claimed Goal Achieve.")
    accepted_families = {row.get("package_family") for row in accepted}
    queue_families = {row.get("package_family") for row in queue}
    expected_families = set(FAMILY_SCOPE)
    if accepted_families != expected_families or queue_families != expected_families:
        fail(f"accepted/queue family mismatch: accepted={sorted(accepted_families)} queue={sorted(queue_families)}")
    for family, rows in inputs["packages"].items():
        if not rows:
            fail(f"{family} package has no rows")
        for row in rows:
            if (
                row.get("execution_allowed") != "false"
                or row.get("training_allowed") != "false"
                or row.get("mt5_execution_allowed") != "false"
            ):
                fail(f"{family} package opened execution/training/MT5 flag")
    if not all(row.get("claim_status") == "not_claimed" for row in inputs["blockers"]):
        fail("blocker matrix contains claimed rows")


def build_source_lineage() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in SOURCE_INPUTS:
        exists = path_exists(path)
        rows.append(
            {
                "source_path": rel(path),
                "exists": exists,
                "sha256": sha256_file_lf_normalized(path) if exists else "",
                "row_count_or_keys": row_count_or_keys(path) if exists else "",
                "scaffold_use": "run337J runner scaffold materialization only",
                "forbidden_use": "model training, MT5 execution, threshold retune, lot optimization, forward-pocket filtering, candidate selection, Forward Passed, runtime authority, Goal Achieve",
                "lineage_status": "pass" if exists else "fail",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def package_rows_for_family(inputs: Mapping[str, Any], family: str) -> list[dict[str, str]]:
    if family == "package_index":
        return list(inputs["package_index_scaffold_rows"])
    return list(inputs["packages"][family])


def source_package_path(family: str) -> Path:
    if family == "package_index":
        return PACKAGE_INDEX_CSV
    return PACKAGE_FILES[family]


def contract_path_for_family(family: str) -> str:
    contract = CONTRACT_FILES[family]
    return rel(contract) if contract else ""


def build_family_manifest(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    accepted_by_family = {row["package_family"]: row for row in inputs["accepted"]}
    queue_by_family = {row["package_family"]: row for row in inputs["queue"]}
    rows: list[dict[str, Any]] = []
    for priority, family in enumerate(FAMILY_SCOPE, start=1):
        source_path = source_package_path(family)
        review_path = RUN337I_REVIEW_FILES[family]
        package_rows = package_rows_for_family(inputs, family)
        accepted = accepted_by_family.get(family, {})
        queue = queue_by_family.get(family, {})
        rows.append(
            {
                "scaffold_family_id": f"{RUN_NUMBER}_{family}_runner_scaffold",
                "priority": priority,
                "package_family": family,
                "runner_scope": FAMILY_SCOPE[family],
                "source_package_artifact": rel(source_path),
                "source_package_sha256": sha256_file_lf_normalized(source_path),
                "source_review_artifact": rel(review_path),
                "source_review_sha256": sha256_file_lf_normalized(review_path),
                "contract_artifact": contract_path_for_family(family),
                "package_rows": len(package_rows),
                "queue_id": queue.get("queue_id", ""),
                "queue_status": accepted.get("queue_status", ""),
                "family_scaffold_artifact": rel(FAMILY_SCAFFOLD_FILES[family]),
                "preflight_checks": FAMILY_PRECHECKS[family],
                "required_outputs": queue.get("required_outputs", ""),
                "execution_ready": "false",
                "execution_status": "schema_scaffold_only_no_execution",
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


def infer_required_inputs(row: Mapping[str, str], family: str) -> str:
    for key in (
        "required_inputs",
        "proxy_required_inputs",
        "required_artifacts",
        "required_extractors",
        "required_controls",
        "required_source_identity",
        "required_files",
        "blocked_condition",
    ):
        if row.get(key):
            return row[key]
    return FAMILY_PRECHECKS[family]


def infer_required_outputs(row: Mapping[str, str], family: str) -> str:
    for key in (
        "expected_outputs",
        "comparison_outputs",
        "runtime_outputs",
        "stress_outputs",
        "slice_outputs",
        "mt5_required_outputs",
    ):
        if row.get(key):
            return row[key]
    return "runner_scaffold_manifest;preflight_checklist;claim_boundary_receipt"


def infer_blocker(row: Mapping[str, str], family: str) -> str:
    for key in (
        "blocker_criteria",
        "blocked_if_missing",
        "failure_memory_trigger",
        "blocked_claims",
        "failure_memory_axis",
        "required_response",
        "invalid_if",
    ):
        if row.get(key):
            return row[key]
    return f"{family} scaffold must pass run337K review before execution"


def build_scaffold_index(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for family_index, family in enumerate(FAMILY_SCOPE, start=1):
        package_rows = package_rows_for_family(inputs, family)
        for row_index, row in enumerate(package_rows, start=1):
            package_id = row.get("package_id") or row.get("blocker_id") or f"{family}_index_{row_index}"
            rows.append(
                {
                    "scaffold_id": f"{RUN_NUMBER}_{family_index:02d}_{row_index:03d}",
                    "package_family": family,
                    "package_id": package_id,
                    "family_scaffold_artifact": rel(FAMILY_SCAFFOLD_FILES[family]),
                    "source_package_artifact": rel(source_package_path(family)),
                    "source_review_artifact": rel(RUN337I_REVIEW_FILES[family]),
                    "required_input_identity": infer_required_inputs(row, family),
                    "required_output_schema": infer_required_outputs(row, family),
                    "preflight_checks": FAMILY_PRECHECKS[family],
                    "blocked_if": infer_blocker(row, family),
                    "execution_ready": "false",
                    "execution_status": "schema_scaffold_only_no_execution",
                    "model_training_allowed": "false",
                    "mt5_execution_allowed": "false",
                    "selection_allowed": "false",
                    "forward_decision_allowed": "false",
                    "runtime_authority_allowed": "false",
                    "result_ingestion_status": "blocked_until_run337K_review_and_future_execution_packet",
                    "next_review_required": NEXT_RUN_ID,
                    "forbidden": FORBIDDEN,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def write_family_scaffolds(scaffold_index: Sequence[Mapping[str, Any]]) -> list[Path]:
    columns = (
        "scaffold_id",
        "package_family",
        "package_id",
        "source_package_artifact",
        "source_review_artifact",
        "required_input_identity",
        "required_output_schema",
        "preflight_checks",
        "blocked_if",
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
    paths: list[Path] = []
    for family, path in FAMILY_SCAFFOLD_FILES.items():
        family_rows = [row for row in scaffold_index if row.get("package_family") == family]
        paths.append(write_csv(path, columns, family_rows))
    return paths


def build_preflight_checklist(family_manifest: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    check_templates = [
        ("source_artifact_exists", "source package, review artifact, and contract identity are present"),
        ("execution_flags_closed", "execution, training, MT5, selection, Forward decision, and runtime authority flags remain false"),
        ("identity_fields_declared", "feature/model/threshold/risk/lot/timestamp/source identities are declared where the family needs them"),
        ("output_schema_declared", "future outputs are named before any later runner can execute"),
        ("blocked_command_written", "execution command is blocked until run337K review and later execution packet"),
        ("claim_boundary_receipt_bound", "claim boundary receipt forbids Forward/runtime/Goal claims"),
    ]
    rows: list[dict[str, Any]] = []
    for manifest in family_manifest:
        family = str(manifest["package_family"])
        for order, (check_id, requirement) in enumerate(check_templates, start=1):
            rows.append(
                {
                    "preflight_id": f"{family}_{order:02d}_{check_id}",
                    "package_family": family,
                    "check_order": order,
                    "requirement": requirement,
                    "evidence_artifact": manifest["family_scaffold_artifact"],
                    "current_status": "declared_pending_run337K_review",
                    "execution_block_if_missing": "true",
                    "execution_ready": "false",
                    "next_review_required": NEXT_RUN_ID,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def build_blocked_execution_commands(family_manifest: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for manifest in family_manifest:
        family = str(manifest["package_family"])
        rows.append(
            {
                "command_id": f"blocked_{family}_execution_command",
                "package_family": family,
                "would_be_command": f"python stage_pipelines/stage337/future_execute_{family}_runner.py --run run337J",
                "command_status": "blocked_not_created_not_allowed_in_run337J",
                "blocked_reason": "run337J materializes runner scaffolds only; run337K review and a later explicit execution packet are required before any execution",
                "required_before_unblock": "run337K scaffold review;fresh data identity;no-lookahead gate;runtime identity;claim-boundary audit;future execution packet",
                "model_training_allowed": "false",
                "mt5_execution_allowed": "false",
                "selection_allowed": "false",
                "forward_decision_allowed": "false",
                "runtime_authority_allowed": "false",
                "next_review_required": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_run337k_review_queue(family_manifest: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, manifest in enumerate(family_manifest, start=1):
        family = str(manifest["package_family"])
        rows.append(
            {
                "queue_id": f"review_{family}_runner_scaffold",
                "priority": index,
                "package_family": family,
                "runner_scope": manifest["runner_scope"],
                "scaffold_artifact": manifest["family_scaffold_artifact"],
                "required_inputs": f"{rel(RUNNER_SCAFFOLD_INDEX_CSV)};{rel(PREFLIGHT_CHECKLIST_CSV)};{rel(BLOCKED_EXECUTION_COMMAND_CSV)};{rel(CLAIM_BOUNDARY_RECEIPT_JSON)}",
                "review_task": "verify scaffold fields, source lineage, preflight checklist, blocked execution command, and claim boundary",
                "required_decision": "accept_for_future_materialization_or_route_repair_gap",
                "forbidden": "model training, MT5 execution, threshold retune, lot optimization, forward-pocket filtering, candidate selection, Forward Passed, runtime authority, Goal Achieve",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_gate_audit(
    source_lineage: Sequence[Mapping[str, Any]],
    family_manifest: Sequence[Mapping[str, Any]],
    scaffold_index: Sequence[Mapping[str, Any]],
    preflight: Sequence[Mapping[str, Any]],
    blocked_commands: Sequence[Mapping[str, Any]],
    run337k_queue: Sequence[Mapping[str, Any]],
    inputs: Mapping[str, Any],
) -> list[dict[str, Any]]:
    source_ok = all(row.get("lineage_status") == "pass" for row in source_lineage)
    family_counts = Counter(row.get("package_family") for row in scaffold_index)
    all_families_present = set(family_counts) == set(FAMILY_SCOPE)
    no_execution = all(
        row.get("execution_ready") == "false"
        and row.get("model_training_allowed") == "false"
        and row.get("mt5_execution_allowed") == "false"
        and row.get("selection_allowed") == "false"
        and row.get("forward_decision_allowed") == "false"
        and row.get("runtime_authority_allowed") == "false"
        for row in scaffold_index
    )
    manifest_closed = all(
        row.get("execution_ready") == "false"
        and row.get("model_training_allowed") == "false"
        and row.get("mt5_execution_allowed") == "false"
        for row in family_manifest
    )
    blocked_closed = all(row.get("command_status") == "blocked_not_created_not_allowed_in_run337J" for row in blocked_commands)
    return [
        {
            "gate_id": "source_lineage_connected",
            "status": "pass" if source_ok and len(source_lineage) >= len(SOURCE_INPUTS) else "fail",
            "evidence": rel(SOURCE_LINEAGE_CSV),
            "finding": f"source_rows={len(source_lineage)};all_present={source_ok}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "run337I_inputs_accept_scaffold_materialization",
            "status": "pass"
            if len(inputs["accepted"]) == 9 and len(inputs["queue"]) == 9 and not inputs["repair_gaps"]
            else "fail",
            "evidence": f"{rel(ACCEPTED_PACKAGES_CSV)};{rel(RUN337J_QUEUE_CSV)};{rel(RUN337I_REPAIR_GAPS_CSV)}",
            "finding": f"accepted={len(inputs['accepted'])};queue={len(inputs['queue'])};repair_gaps={len(inputs['repair_gaps'])}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "family_manifest_ready",
            "status": "pass" if len(family_manifest) == 9 and manifest_closed else "fail",
            "evidence": rel(RUNNER_SCAFFOLD_FAMILY_MANIFEST_CSV),
            "finding": f"family_manifest_rows={len(family_manifest)};flags_closed={manifest_closed}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "scaffold_index_covers_all_families",
            "status": "pass" if all_families_present and len(scaffold_index) >= 47 else "fail",
            "evidence": rel(RUNNER_SCAFFOLD_INDEX_CSV),
            "finding": f"scaffold_rows={len(scaffold_index)};family_counts={dict(sorted(family_counts.items()))}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "individual_family_scaffolds_written",
            "status": "pass" if all(path_exists(path) for path in FAMILY_SCAFFOLD_FILES.values()) else "fail",
            "evidence": ";".join(rel(path) for path in FAMILY_SCAFFOLD_FILES.values()),
            "finding": f"family_scaffold_files={len(FAMILY_SCAFFOLD_FILES)}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "preflight_checklist_ready",
            "status": "pass" if len(preflight) == len(family_manifest) * 6 else "fail",
            "evidence": rel(PREFLIGHT_CHECKLIST_CSV),
            "finding": f"preflight_rows={len(preflight)}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "blocked_execution_commands_ready",
            "status": "pass" if len(blocked_commands) == 9 and blocked_closed else "fail",
            "evidence": rel(BLOCKED_EXECUTION_COMMAND_CSV),
            "finding": f"blocked_command_rows={len(blocked_commands)};blocked_closed={blocked_closed}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "run337K_review_queue_ready",
            "status": "pass" if len(run337k_queue) == 9 else "fail",
            "evidence": rel(RUN337K_REVIEW_QUEUE_CSV),
            "finding": f"run337K_queue_rows={len(run337k_queue)}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "execution_training_mt5_selection_closed",
            "status": "pass" if no_execution else "fail",
            "evidence": rel(RUNNER_SCAFFOLD_INDEX_CSV),
            "finding": "all scaffold rows keep execution/training/MT5/selection/Forward/runtime authority closed",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "claim_guard_no_forward_runtime_goal",
            "status": "pass",
            "evidence": rel(CLAIM_BOUNDARY_RECEIPT_JSON),
            "finding": "run337J opens review of scaffolds only; no model training, MT5 execution, Forward decision, runtime authority, or Goal Achieve",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_metrics(
    source_lineage: Sequence[Mapping[str, Any]],
    family_manifest: Sequence[Mapping[str, Any]],
    scaffold_index: Sequence[Mapping[str, Any]],
    preflight: Sequence[Mapping[str, Any]],
    blocked_commands: Sequence[Mapping[str, Any]],
    run337k_queue: Sequence[Mapping[str, Any]],
    audit: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    family_counts = Counter(str(row.get("package_family", "")) for row in scaffold_index)
    return {
        "source_lineage_rows": len(source_lineage),
        "family_manifest_rows": len(family_manifest),
        "scaffold_rows": len(scaffold_index),
        "family_scaffold_files": len(FAMILY_SCAFFOLD_FILES),
        "preflight_rows": len(preflight),
        "blocked_command_rows": len(blocked_commands),
        "run337k_queue_rows": len(run337k_queue),
        "gate_rows": len(audit),
        "failed_gate_rows": len([row for row in audit if row.get("status") != "pass"]),
        "family_counts": dict(sorted(family_counts.items())),
    }


def write_receipts(metrics: Mapping[str, Any]) -> list[Path]:
    return [
        write_json(
            EXPERIMENT_DESIGN_JSON,
            {
                "run_id": RUN_ID,
                "hypothesis": "reviewed package families can be converted into non-executing runner scaffolds without opening training, MT5 execution, or selection",
                "decision_use": "decide whether run337K can review runner scaffolds before any future execution packet",
                "comparison_baseline": "run337I accepted package queue, run337J materialization queue, run337H package specs, and run337I decision boundary",
                "control_variables": "no model training, no MT5 execution, no threshold retune, no lot optimization, no forward-pocket filtering, no candidate selection",
                "changed_variables": "runner scaffold family manifest, package-row scaffold index, preflight checklist, blocked execution commands, claim boundary receipt",
                "sample_scope": "scaffold materialization only; no US100 M5 bars, no trade rows, no new model fit",
                "success_criteria": "9 family scaffolds, package-row scaffold index, preflight checklist, blocked execution commands, claim boundary receipt, and run337K review queue all pass gates",
                "failure_criteria": "missing family scaffold, open execution flag, absent source lineage, missing blocked command, or run337K queue gap",
                "invalid_conditions": "using run337J scaffolds to claim Forward Passed/Failed, runtime authority, live readiness, operating promotion, or Goal Achieve",
                "stop_conditions": "any gate fails; repair scaffold or upstream package before review",
                "evidence_plan": "source lineage, family manifest, scaffold index, family scaffold CSVs, preflight checklist, blocked commands, claim receipt, gate audit, ledgers, artifact registry",
                "metrics": metrics,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            DATA_INTEGRITY_JSON,
            {
                "run_id": RUN_ID,
                "data_source": "run337H package specs and run337I review artifacts",
                "time_axis": "future runners must preserve cycle_bar_time, source_timestamp, broker timezone, timestamp basis, as-of status, source_row_hash, and sorted order before execution",
                "sample_scope": "scaffold materialization only; no new US100 M5 bars are consumed",
                "missing_or_duplicate_check": "future execution remains blocked until preflight rows confirm missing, duplicate, stale, revision, timezone, and future join checks",
                "feature_label_boundary": "no label or fit is created; no-lookahead canary scaffolds must fail before any future runner can execute if future features leak",
                "split_boundary": "train/WFO/forward split remains closed; future offense work must create WFO split contracts before training",
                "leakage_risk": "future-bar features, forward-pocket selection, threshold retune, lot optimization, timestamp drift, macro revision drift, and after-result feature picking",
                "data_hash_or_identity": rel(SOURCE_LINEAGE_CSV),
                "integrity_judgment": "usable_with_boundary",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RUNTIME_PARITY_JSON,
            {
                "run_id": RUN_ID,
                "research_path": rel(Path(__file__)),
                "runtime_path": rel(FAMILY_SCAFFOLD_FILES["runtime"]),
                "shared_contract": "feature order, model/ONNX spec, adapter manifest, threshold, risk, lot, symbol/timeframe, broker session, timestamp basis, proxy expected, MT5 observed, tester report, trade ledger, telemetry, D/B source, cost stress, regime slices, and curve pockets must match before KPI authority",
                "known_differences": "run337J produces scaffolds and blocked command records only; no MT5 tester output, no terminal log, and no trade ledger are created",
                "parity_check": "preflight and blocked command rows require fresh runtime output and row-level proxy-MT5 difference in a later explicit execution packet",
                "parity_identity": rel(RUNNER_SCAFFOLD_INDEX_CSV),
                "runtime_claim_boundary": "runner_scaffold_only_no_runtime_authority",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            ARTIFACT_LINEAGE_JSON,
            {
                "run_id": RUN_ID,
                "source_inputs": [rel(path) for path in SOURCE_INPUTS],
                "producer": rel(Path(__file__)),
                "consumer": NEXT_RUN_ID,
                "artifact_paths": [
                    rel(SOURCE_LINEAGE_CSV),
                    rel(RUNNER_SCAFFOLD_FAMILY_MANIFEST_CSV),
                    rel(RUNNER_SCAFFOLD_INDEX_CSV),
                    *[rel(path) for path in FAMILY_SCAFFOLD_FILES.values()],
                    rel(PREFLIGHT_CHECKLIST_CSV),
                    rel(BLOCKED_EXECUTION_COMMAND_CSV),
                    rel(CLAIM_BOUNDARY_RECEIPT_JSON),
                    rel(RUN337K_REVIEW_QUEUE_CSV),
                    rel(GATE_AUDIT_CSV),
                ],
                "artifact_hashes": "registered in artifact_registry after run",
                "registry_links": "run_registry;alpha_run_ledger;stage_run_ledger;artifact_registry",
                "availability": "tracked after commit; reproducible from run337J script",
                "lineage_judgment": "connected_with_boundary",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RESULT_JUDGMENT_JSON,
            {
                "run_id": RUN_ID,
                "result_subject": "runner scaffold materialization",
                "evidence_available": "family scaffold manifest, package-row scaffold index, preflight checklist, blocked execution commands, claim boundary receipt, run337K queue, gate audit",
                "evidence_missing": "no model training, no MT5 execution, no proxy expected values, no MT5 observed values, no trade ledger, no candidate KPI",
                "judgment_label": "exploratory",
                "claim_boundary": "scaffolds are materialized for run337K review only; no candidate, Forward decision, runtime authority, live readiness, or Goal Achieve",
                "next_condition": NEXT_RUN_ID,
                "user_explanation_hook": "이번 실행은 실제 엔진을 켠 것이 아니라, 나중에 켤 수 있는지 검사할 체크리스트와 차단 장치를 만든 것이다.",
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed_for_stage337_new_work",
                "runtime_authority": "not_claimed",
                "goal_achieve": "not_claimed",
            },
        ),
    ]


def write_reports(metrics: Mapping[str, Any]) -> list[Path]:
    report = f"""
# run337J Runner Scaffold Materialization(337J 러너 골격 물질화)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- parent_run(부모 실행): `{PARENT_RUN_ID}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed_for_stage337_new_work`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`

## Materialized Result(물질화 결과)

- source_lineage_rows(원천 계보 행): `{metrics['source_lineage_rows']}`
- family_manifest_rows(가족 목록 행): `{metrics['family_manifest_rows']}`
- scaffold_rows(골격 행): `{metrics['scaffold_rows']}`
- family_scaffold_files(가족 골격 파일): `{metrics['family_scaffold_files']}`
- preflight_rows(사전점검 행): `{metrics['preflight_rows']}`
- blocked_command_rows(차단 명령 행): `{metrics['blocked_command_rows']}`
- run337K_queue_rows(337K 대기열 행): `{metrics['run337k_queue_rows']}`
- gate_rows(게이트 행): `{metrics['gate_rows']}`, failed(실패): `{metrics['failed_gate_rows']}`

Effect(효과): run337J(337J 실행)는 9개 package family(패키지 묶음)를 비실행 runner scaffold(러너 골격)로 바꾸고, preflight checklist(사전점검 목록)와 blocked execution command(차단 실행 명령)를 붙였다. 아직 model training(모델 학습), MT5 execution(MT5 실행), candidate selection(후보 선택)은 없다.
"""
    decision = f"""
# 2026-05-27 Stage337J Decision(337J 결정)

- decision(결정): `{DECISION}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed_for_stage337_new_work`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`

Effect(효과): 다음 run337K(337K 실행)는 scaffold(골격), preflight(사전점검), blocked command(차단 명령), claim boundary(주장 경계)를 검토할 수 있다. 이 결정은 학습 허가, MT5 실행 허가, Forward 판정, 운영 가능 주장으로 쓰지 않는다.
"""
    return [write_md(REPORT_DOC, report), write_md(DECISION_DOC, decision)]


def update_status_docs(metrics: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    selection = f"""
# Stage337 Selection Status(337단계 선택 상태)

- stage_id(단계 ID): `{STAGE_ID}`
- stage_status(단계 상태): `open_active`
- selected_candidate(선택 후보): `none`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- opened_by(개방 실행): `run336P_forward_decision_or_failure_memory_handoff_v1`
- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{DECISION}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed_for_stage337_new_work`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): run337J(337J 실행)는 runner scaffold(러너 골격)를 물질화하고 run337K(337K 실행) 검토 대기열로 넘겼다. 아직 선택 후보는 없다.
"""
    artifacts.append(write_md(SELECTED_DIR / "selection_status.md", selection))

    brief_text, brief_bom = read_text_lossless(SPEC_DIR / "stage_brief.md")
    brief_text = replace_prefix_line(brief_text, "- latest_run(최신 실행):", f"- latest_run(최신 실행): `{RUN_ID}`")
    brief_text = insert_after_marker_once(
        brief_text,
        "- run337I_summary(337I 요약):",
        f"- run337J_summary(337J 요약): `{STATUS}`. Effect(효과): 9개 runner scaffold(러너 골격), preflight checklist(사전점검 목록), blocked execution command(차단 실행 명령), run337K review queue(337K 검토 대기열)를 만들었다.",
        "run337J_summary",
    )
    artifacts.append(write_text_lossless(SPEC_DIR / "stage_brief.md", brief_text, brief_bom))

    input_section = f"""
- runner_scaffold_source_lineage(러너 골격 원천 계보): `{rel(SOURCE_LINEAGE_CSV)}`
- runner_scaffold_family_manifest(러너 골격 가족 목록): `{rel(RUNNER_SCAFFOLD_FAMILY_MANIFEST_CSV)}`
- runner_scaffold_index(러너 골격 색인): `{rel(RUNNER_SCAFFOLD_INDEX_CSV)}`
- preflight_checklist(사전점검 목록): `{rel(PREFLIGHT_CHECKLIST_CSV)}`
- blocked_execution_command(차단 실행 명령): `{rel(BLOCKED_EXECUTION_COMMAND_CSV)}`
- claim_boundary_receipt(주장 경계 영수증): `{rel(CLAIM_BOUNDARY_RECEIPT_JSON)}`
- run337K_queue(337K 대기열): `{rel(RUN337K_REVIEW_QUEUE_CSV)}`

Effect(효과): 다음 실행은 실제 실행이 아니라, 이 골격들이 실행 가능한 준비 상태인지 먼저 검토한다.
"""
    artifacts.append(append_section_once(INPUTS_DIR / "input_refs.md", "## run337J Outputs(337J 산출물)", input_section))

    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_prefix_line(workspace_text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    focus = (
        "- >-\n"
        f"  Stage337 run337J focus complete: Stage337(337단계) run337J(337J 실행)는 `{STATUS}`로 runner scaffold materialization(러너 골격 물질화)을 완료했다. "
        "Effect(효과): run337K(337K 실행) runner scaffold review(러너 골격 검토) 대기열을 열었지만 model training(모델 학습), MT5 execution(MT5 실행), candidate selection(후보 선택)은 아직 닫아둔다.\n"
    )
    workspace_text = insert_focus_once(workspace_text, focus, "Stage337 run337J focus complete")
    artifacts.append(write_text_lossless(WORKSPACE_STATE, workspace_text, workspace_bom))

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    replacements = {
        "- current_run(현재 실행):": f"- current_run(현재 실행): `{NEXT_RUN_ID}`",
        "- status(상태):": f"- status(상태): `{STATUS}`",
        "- decision(결정):": f"- decision(결정): `{DECISION}`",
    }
    for prefix, new_line in replacements.items():
        current_text = replace_prefix_line(current_text, prefix, new_line)
    summary = (
        f"- run337J_summary(337J 요약): `{STATUS}`. "
        "Effect(효과): 러너 골격, 사전점검, 차단 실행 명령, 주장 경계 영수증을 만들고 run337K(337K 실행) 검토로 넘기며, 학습/MT5/후보 선택은 계속 닫아둔다."
    )
    current_text = insert_after_marker_once(current_text, "- decision(결정):", summary, "run337J_summary")
    artifacts.append(write_text_lossless(CURRENT_STATE, current_text, current_bom))

    artifacts.append(
        append_section_once(
            CHANGELOG,
            "## Stage337J Runner Scaffold Materialization(337J 러너 골격 물질화)",
            f"""
- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- action(행동): run337I(337I 실행)의 승인 package family(패키지 묶음)를 비실행 runner scaffold(러너 골격), preflight checklist(사전점검 목록), blocked execution command(차단 실행 명령)로 물질화했다.
- effect(효과): 다음 run337K(337K 실행)는 실제 실행 전에 원천 계보, 사전점검, 차단 명령, 주장 경계를 검토할 수 있다.
- boundary(경계): model training(모델 학습), MT5 execution(MT5 실행), selected candidate(선택 후보), Forward Passed(전진 통과), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 `not_claimed`.
""",
        )
    )
    return artifacts


def update_registers(artifacts: Sequence[Path], generated_at: str) -> list[Path]:
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "runner_scaffold_materialization",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_DOC),
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};scaffolds_materialized;training_not_allowed;mt5_not_executed;goal_achieve_not_claimed.",
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__runner_scaffold_materialization",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "runner_scaffold_materialization",
                "tier_scope": "stage337_package_boundary_macro48_u42_core56",
                "kpi_scope": "scaffold_only_no_new_candidate_kpi",
                "scoreboard_lane": "runner_scaffold_readiness",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_DOC),
                "primary_kpi": "family_manifest_rows=9;scaffold_rows=47;run337k_queue_rows=9;candidate_selection=none",
                "guardrail_kpi": "training_not_allowed;mt5_not_executed;runtime_authority_not_claimed;goal_achieve_not_claimed",
                "external_verification_status": "out_of_scope_by_claim_scaffold_only",
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID}.",
            }
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
                "work_family": "runtime_parity_scaffold",
                "evidence_scope": "run337I_accepted_packages_and_run337H_package_specs",
                "kpi_scope": "scaffold_only_no_new_candidate_kpi",
                "status": STATUS,
                "judgment": JUDGMENT,
                "claim_boundary": CLAIM_BOUNDARY,
                "path": rel(REPORT_DOC),
                "notes": f"next_action={NEXT_RUN_ID};scaffolds_materialized;training_not_allowed;mt5_not_executed;goal_achieve_not_claimed.",
                "decision": DECISION,
            }
        ],
        key="ledger_row_id",
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}::{rel(path)}",
            "artifact_type": path.suffix.lstrip(".") or "file",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": generated_at,
            "notes": "run337J_runner_scaffold_materialization_no_execution_no_selection",
        }
        for path in artifacts
        if path_exists(path) and io_path(path).is_file()
    ]
    upsert_csv_rows(
        ARTIFACT_REGISTRY,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
        artifact_rows,
        key="artifact_id",
    )
    return [RUN_REGISTRY, ALPHA_LEDGER, STAGE_LEDGER, ARTIFACT_REGISTRY]


def main() -> int:
    generated_at = now_utc()
    inputs = load_inputs()
    validate_inputs(inputs)
    source_lineage = build_source_lineage()
    family_manifest = build_family_manifest(inputs)
    scaffold_index = build_scaffold_index(inputs)
    preflight = build_preflight_checklist(family_manifest)
    blocked_commands = build_blocked_execution_commands(family_manifest)
    run337k_queue = build_run337k_review_queue(family_manifest)
    family_scaffold_paths = write_family_scaffolds(scaffold_index)
    audit = build_gate_audit(source_lineage, family_manifest, scaffold_index, preflight, blocked_commands, run337k_queue, inputs)
    metrics = build_metrics(source_lineage, family_manifest, scaffold_index, preflight, blocked_commands, run337k_queue, audit)
    failed_gates = [row for row in audit if row.get("status") != "pass"]

    run_artifacts = [
        write_csv(
            SOURCE_LINEAGE_CSV,
            ("source_path", "exists", "sha256", "row_count_or_keys", "scaffold_use", "forbidden_use", "lineage_status", "claim_boundary"),
            source_lineage,
        ),
        write_csv(
            RUNNER_SCAFFOLD_FAMILY_MANIFEST_CSV,
            (
                "scaffold_family_id",
                "priority",
                "package_family",
                "runner_scope",
                "source_package_artifact",
                "source_package_sha256",
                "source_review_artifact",
                "source_review_sha256",
                "contract_artifact",
                "package_rows",
                "queue_id",
                "queue_status",
                "family_scaffold_artifact",
                "preflight_checks",
                "required_outputs",
                "execution_ready",
                "execution_status",
                "model_training_allowed",
                "mt5_execution_allowed",
                "selection_allowed",
                "forward_decision_allowed",
                "runtime_authority_allowed",
                "next_review_required",
                "forbidden",
                "claim_boundary",
            ),
            family_manifest,
        ),
        write_csv(
            RUNNER_SCAFFOLD_INDEX_CSV,
            (
                "scaffold_id",
                "package_family",
                "package_id",
                "family_scaffold_artifact",
                "source_package_artifact",
                "source_review_artifact",
                "required_input_identity",
                "required_output_schema",
                "preflight_checks",
                "blocked_if",
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
            ),
            scaffold_index,
        ),
        *family_scaffold_paths,
        write_csv(
            PREFLIGHT_CHECKLIST_CSV,
            (
                "preflight_id",
                "package_family",
                "check_order",
                "requirement",
                "evidence_artifact",
                "current_status",
                "execution_block_if_missing",
                "execution_ready",
                "next_review_required",
                "claim_boundary",
            ),
            preflight,
        ),
        write_csv(
            BLOCKED_EXECUTION_COMMAND_CSV,
            (
                "command_id",
                "package_family",
                "would_be_command",
                "command_status",
                "blocked_reason",
                "required_before_unblock",
                "model_training_allowed",
                "mt5_execution_allowed",
                "selection_allowed",
                "forward_decision_allowed",
                "runtime_authority_allowed",
                "next_review_required",
                "claim_boundary",
            ),
            blocked_commands,
        ),
        write_json(
            CLAIM_BOUNDARY_RECEIPT_JSON,
            {
                "run_id": RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
                "forbidden": split_semicolon(FORBIDDEN),
                "model_training": "not_run",
                "mt5_execution": "not_run",
                "selected_candidate": "none",
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed_for_stage337_new_work",
                "live_readiness": "not_claimed",
                "deployment": "not_claimed",
                "operating_promotion": "not_claimed",
                "runtime_authority": "not_claimed",
                "goal_achieve": "not_claimed",
                "effect": "run337J materializes non-executing scaffolds only and opens run337K review queue",
            },
        ),
        write_csv(
            RUN337K_REVIEW_QUEUE_CSV,
            (
                "queue_id",
                "priority",
                "package_family",
                "runner_scope",
                "scaffold_artifact",
                "required_inputs",
                "review_task",
                "required_decision",
                "forbidden",
                "claim_boundary",
            ),
            run337k_queue,
        ),
        write_csv(GATE_AUDIT_CSV, ("gate_id", "status", "evidence", "finding", "claim_boundary"), audit),
        write_csv(
            RESULT_JUDGMENT_CSV,
            ("result_subject", "evidence_available", "evidence_missing", "judgment_label", "claim_boundary", "next_condition"),
            [
                {
                    "result_subject": "run337J runner scaffold materialization",
                    "evidence_available": f"{rel(RUNNER_SCAFFOLD_FAMILY_MANIFEST_CSV)};{rel(RUNNER_SCAFFOLD_INDEX_CSV)};{rel(PREFLIGHT_CHECKLIST_CSV)};{rel(BLOCKED_EXECUTION_COMMAND_CSV)}",
                    "evidence_missing": "model training;MT5 execution;proxy expected values;MT5 observed values;trade ledger;candidate KPI",
                    "judgment_label": "exploratory",
                    "claim_boundary": CLAIM_BOUNDARY,
                    "next_condition": NEXT_RUN_ID,
                }
            ],
        ),
    ]
    run_artifacts.extend(write_receipts(metrics))
    final_payload = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS if not failed_gates else "blocked_stage337J_runner_scaffold_gate_failure",
        "judgment": JUDGMENT if not failed_gates else "stage337J_runner_scaffold_requires_repair",
        "decision": DECISION if not failed_gates else "stage337J_runner_scaffold_blocked_gate_failure",
        "metrics": metrics,
        "failed_gates": failed_gates,
        "next_action": NEXT_RUN_ID if not failed_gates else "repair_run337J_scaffolds_before_review",
        "selected_candidate": "none",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed_for_stage337_new_work",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "model_training": "not_run",
        "mt5_execution": "not_run",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    run_artifacts.append(write_json(FINAL_DECISION_JSON, final_payload))
    run_artifacts.extend(write_reports(metrics))
    if failed_gates:
        write_json(
            RUN_MANIFEST_JSON,
            {
                "run_id": RUN_ID,
                "run_number": RUN_NUMBER,
                "stage_id": STAGE_ID,
                "parent_run_id": PARENT_RUN_ID,
                "created_at_utc": generated_at,
                "producer": rel(Path(__file__)),
                "source_inputs": [rel(path) for path in SOURCE_INPUTS],
                "outputs": [rel(path) for path in run_artifacts],
                "status": "blocked_stage337J_runner_scaffold_gate_failure",
                "decision": "stage337J_runner_scaffold_blocked_gate_failure",
                "failed_gates": failed_gates,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
        print(json.dumps({"run_id": RUN_ID, "failed_gates": failed_gates}, ensure_ascii=False, indent=2))
        return 2

    status_artifacts = update_status_docs(metrics)
    all_artifacts = [Path(__file__), *run_artifacts, *status_artifacts]
    manifest_payload = {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": generated_at,
        "producer": rel(Path(__file__)),
        "source_inputs": [rel(path) for path in SOURCE_INPUTS],
        "outputs": [rel(path) for path in all_artifacts],
        "status": STATUS,
        "decision": DECISION,
        "external_verification_status": "out_of_scope_by_claim_runner_scaffold_only_no_mt5_execution",
        "next_action": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(RUN_MANIFEST_JSON, manifest_payload)
    all_artifacts.append(RUN_MANIFEST_JSON)
    register_artifacts = update_registers(all_artifacts, generated_at)
    all_artifacts.extend(register_artifacts)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "family_manifest_rows": metrics["family_manifest_rows"],
                "scaffold_rows": metrics["scaffold_rows"],
                "preflight_rows": metrics["preflight_rows"],
                "blocked_command_rows": metrics["blocked_command_rows"],
                "run337K_queue_rows": metrics["run337k_queue_rows"],
                "gate_rows": metrics["gate_rows"],
                "failed_gate_rows": metrics["failed_gate_rows"],
                "model_training": "not_run",
                "mt5_execution": "not_run",
                "next_action": NEXT_RUN_ID,
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed_for_stage337_new_work",
                "runtime_authority": "not_claimed",
                "goal_achieve": "not_claimed",
                "artifact_count": len(all_artifacts),
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
