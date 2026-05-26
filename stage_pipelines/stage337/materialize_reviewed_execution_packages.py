from __future__ import annotations

import csv
import json
import math
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


TODAY = "2026-05-27"
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
SOURCE_STAGE_ID = "336_onnx_research_packet__constraint_bound_repair_defense_offense_rebuild"
RUN_NUMBER = "run337H"
RUN_ID = "run337H_materialize_reviewed_execution_packages_v1"
PARENT_RUN_ID = "run337G_review_protocol_bound_execution_blueprints_v1"
NEXT_RUN_ID = "run337I_review_materialized_execution_packages_v1"
STATUS = "completed_reviewed_execution_packages_materialized_no_training_no_mt5"
JUDGMENT = "stage337H_packages_materialized_for_review_no_selection"
DECISION = "stage337H_packages_ready_for_review_no_training_no_mt5_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage337H_package_materialization_no_model_training_no_mt5_execution_"
    "no_threshold_retuning_no_lot_optimization_no_forward_pocket_filtering_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
RUN337F_DIR = STAGE_DIR / "02_runs" / "run337F"
RUN337G_DIR = STAGE_DIR / "02_runs" / "run337G"
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
DECISION_DOC = DOCS / "decisions" / "2026-05-27_stage337H_materialize_reviewed_execution_packages.md"
REPORT_DOC = REVIEWS_DIR / "run337H_materialize_reviewed_execution_packages.md"

RUN337G_QUEUE = RUN337G_DIR / "run337H_package_materialization_queue.csv"
RUN337G_ACCEPTED = RUN337G_DIR / "accepted_blueprints_for_package_queue.csv"
RUN337G_SOURCE_LINEAGE = RUN337G_DIR / "blueprint_review_source_lineage.csv"
RUN337G_NO_LOOKAHEAD_REVIEW = RUN337G_DIR / "no_lookahead_harness_blueprint_review.csv"
RUN337G_PROXY_MT5_REVIEW = RUN337G_DIR / "proxy_mt5_blueprint_review.csv"
RUN337G_CORE56_REVIEW = RUN337G_DIR / "core56_repair_blueprint_review.csv"
RUN337G_COST_CURVE_REVIEW = RUN337G_DIR / "cost_direction_curve_extraction_blueprint_review.csv"
RUN337G_OFFENSE_REVIEW = RUN337G_DIR / "offense_branch_blueprint_review.csv"
RUN337G_REGIME_REVIEW = RUN337G_DIR / "economic_regime_asof_blueprint_review.csv"
RUN337G_RUNTIME_REVIEW = RUN337G_DIR / "runtime_probe_package_blueprint_review.csv"
RUN337G_CLAIM_REVIEW = RUN337G_DIR / "claim_boundary_review.csv"
RUN337G_REPAIR_GAPS = RUN337G_DIR / "repair_blueprint_gap_queue.csv"
RUN337G_GATE_AUDIT = RUN337G_DIR / "required_gate_coverage_audit.csv"
RUN337G_DECISION = RUN337G_DIR / "final_review_protocol_bound_execution_blueprints_decision.json"
RUN337G_MANIFEST = RUN337G_DIR / "run_manifest.json"

RUN337F_NO_LOOKAHEAD = RUN337F_DIR / "no_lookahead_harness_blueprint.csv"
RUN337F_NO_LOOKAHEAD_SCHEMA = RUN337F_DIR / "no_lookahead_harness_schema.json"
RUN337F_PROXY_EXPECTED = RUN337F_DIR / "proxy_expected_schema_blueprint.csv"
RUN337F_MT5_PROBE = RUN337F_DIR / "mt5_runtime_probe_package_blueprint.csv"
RUN337F_PROXY_DIFF_SCHEMA = RUN337F_DIR / "proxy_mt5_difference_schema.json"
RUN337F_CORE56 = RUN337F_DIR / "core56_repair_blueprint.csv"
RUN337F_CORE56_SCHEMA = RUN337F_DIR / "core56_asof_join_schema.json"
RUN337F_COST_CURVE = RUN337F_DIR / "cost_direction_curve_extraction_blueprint.csv"
RUN337F_COST_CURVE_SCHEMA = RUN337F_DIR / "cost_direction_curve_report_schema.json"
RUN337F_OFFENSE = RUN337F_DIR / "offense_branch_blueprint.csv"
RUN337F_REGIME = RUN337F_DIR / "economic_regime_asof_source_blueprint.csv"
RUN337F_REGIME_SCHEMA = RUN337F_DIR / "economic_regime_slice_schema.json"
RUN337F_RUNTIME = RUN337F_DIR / "runtime_probe_package_blueprint.csv"

PACKAGE_SOURCE_LINEAGE_CSV = RUN_DIR / "package_source_lineage_review.csv"
NO_LOOKAHEAD_PACKAGE_CSV = RUN_DIR / "no_lookahead_canary_harness_package_spec.csv"
NO_LOOKAHEAD_CONTRACT_JSON = RUN_DIR / "no_lookahead_canary_harness_contract.json"
PROXY_MT5_PACKAGE_CSV = RUN_DIR / "proxy_mt5_fresh_probe_package_spec.csv"
PROXY_MT5_CONTRACT_JSON = RUN_DIR / "proxy_mt5_fresh_probe_output_contract.json"
CORE56_PACKAGE_CSV = RUN_DIR / "core56_asof_repair_package_spec.csv"
CORE56_CONTRACT_JSON = RUN_DIR / "core56_asof_repair_contract.json"
COST_CURVE_PACKAGE_CSV = RUN_DIR / "cost_direction_curve_extraction_package_spec.csv"
COST_CURVE_CONTRACT_JSON = RUN_DIR / "cost_direction_curve_extraction_contract.json"
OFFENSE_PACKAGE_CSV = RUN_DIR / "offense_branch_thesis_package_spec.csv"
REGIME_PACKAGE_CSV = RUN_DIR / "economic_regime_asof_join_package_spec.csv"
REGIME_CONTRACT_JSON = RUN_DIR / "economic_regime_asof_join_contract.json"
RUNTIME_PACKAGE_CSV = RUN_DIR / "runtime_probe_package_spec.csv"
RUNTIME_CONTRACT_JSON = RUN_DIR / "runtime_probe_package_contract.json"
CLAIM_GUARD_PACKAGE_CSV = RUN_DIR / "claim_guard_blocker_package_spec.csv"
BLOCKER_MATRIX_CSV = RUN_DIR / "package_blocker_matrix.csv"
PACKAGE_INDEX_CSV = RUN_DIR / "package_manifest_index.csv"
PACKAGE_ACCEPTANCE_CSV = RUN_DIR / "package_acceptance_matrix.csv"
RUN337I_QUEUE_CSV = RUN_DIR / "run337I_package_review_queue.csv"
GATE_AUDIT_CSV = RUN_DIR / "required_gate_coverage_audit.csv"

EXPERIMENT_DESIGN_JSON = RUN_DIR / "experiment_design_receipt.json"
DATA_INTEGRITY_JSON = RUN_DIR / "data_integrity_receipt.json"
RUNTIME_PARITY_JSON = RUN_DIR / "runtime_parity_receipt.json"
ARTIFACT_LINEAGE_JSON = RUN_DIR / "artifact_lineage_receipt.json"
RESULT_JUDGMENT_JSON = RUN_DIR / "result_judgment_receipt.json"
FINAL_DECISION_JSON = RUN_DIR / "final_reviewed_execution_packages_decision.json"
RUN_MANIFEST_JSON = RUN_DIR / "run_manifest.json"


SOURCE_INPUTS: tuple[Path, ...] = (
    RUN337G_QUEUE,
    RUN337G_ACCEPTED,
    RUN337G_SOURCE_LINEAGE,
    RUN337G_NO_LOOKAHEAD_REVIEW,
    RUN337G_PROXY_MT5_REVIEW,
    RUN337G_CORE56_REVIEW,
    RUN337G_COST_CURVE_REVIEW,
    RUN337G_OFFENSE_REVIEW,
    RUN337G_REGIME_REVIEW,
    RUN337G_RUNTIME_REVIEW,
    RUN337G_CLAIM_REVIEW,
    RUN337G_REPAIR_GAPS,
    RUN337G_GATE_AUDIT,
    RUN337G_DECISION,
    RUN337G_MANIFEST,
    RUN337F_NO_LOOKAHEAD,
    RUN337F_NO_LOOKAHEAD_SCHEMA,
    RUN337F_PROXY_EXPECTED,
    RUN337F_MT5_PROBE,
    RUN337F_PROXY_DIFF_SCHEMA,
    RUN337F_CORE56,
    RUN337F_CORE56_SCHEMA,
    RUN337F_COST_CURVE,
    RUN337F_COST_CURVE_SCHEMA,
    RUN337F_OFFENSE,
    RUN337F_REGIME,
    RUN337F_REGIME_SCHEMA,
    RUN337F_RUNTIME,
)


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


def contains_all(text: str, needles: Sequence[str]) -> bool:
    lowered = text.lower()
    return all(needle.lower() in lowered for needle in needles)


def row_count_or_keys(path: Path) -> str:
    if not path_exists(path):
        return ""
    if path.suffix.lower() == ".csv":
        return str(len(read_csv(path)))
    if path.suffix.lower() == ".json":
        return ";".join(sorted(read_json(path).keys()))
    return ""


def load_inputs() -> dict[str, Any]:
    return {
        "queue": read_csv(RUN337G_QUEUE),
        "accepted": read_csv(RUN337G_ACCEPTED),
        "source_lineage": read_csv(RUN337G_SOURCE_LINEAGE),
        "no_lookahead_review": read_csv(RUN337G_NO_LOOKAHEAD_REVIEW),
        "proxy_mt5_review": read_csv(RUN337G_PROXY_MT5_REVIEW),
        "core56_review": read_csv(RUN337G_CORE56_REVIEW),
        "cost_curve_review": read_csv(RUN337G_COST_CURVE_REVIEW),
        "offense_review": read_csv(RUN337G_OFFENSE_REVIEW),
        "regime_review": read_csv(RUN337G_REGIME_REVIEW),
        "runtime_review": read_csv(RUN337G_RUNTIME_REVIEW),
        "claim_review": read_csv(RUN337G_CLAIM_REVIEW),
        "repair_gaps": read_csv(RUN337G_REPAIR_GAPS),
        "gate_audit": read_csv(RUN337G_GATE_AUDIT),
        "decision": read_json(RUN337G_DECISION),
        "manifest": read_json(RUN337G_MANIFEST),
        "no_lookahead": read_csv(RUN337F_NO_LOOKAHEAD),
        "no_lookahead_schema": read_json(RUN337F_NO_LOOKAHEAD_SCHEMA),
        "proxy_expected": read_csv(RUN337F_PROXY_EXPECTED),
        "mt5_probe": read_csv(RUN337F_MT5_PROBE),
        "proxy_diff_schema": read_json(RUN337F_PROXY_DIFF_SCHEMA),
        "core56": read_csv(RUN337F_CORE56),
        "core56_schema": read_json(RUN337F_CORE56_SCHEMA),
        "cost_curve": read_csv(RUN337F_COST_CURVE),
        "cost_curve_schema": read_json(RUN337F_COST_CURVE_SCHEMA),
        "offense": read_csv(RUN337F_OFFENSE),
        "regime": read_csv(RUN337F_REGIME),
        "regime_schema": read_json(RUN337F_REGIME_SCHEMA),
        "runtime": read_csv(RUN337F_RUNTIME),
    }


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
                "package_use": "run337H reviewed execution package materialization only",
                "forbidden_use": "model training, MT5 execution, threshold retune, lot optimization, forward-pocket filtering, candidate selection, Forward Passed, runtime authority, Goal Achieve",
                "lineage_status": "pass" if exists else "fail",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_no_lookahead_package(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for row in inputs["no_lookahead"]:
        rows.append(
            {
                "package_id": f"{row.get('harness_id', '')}_package_spec",
                "package_family": "no_lookahead",
                "source_harness_id": row.get("harness_id", ""),
                "required_inputs": "candidate_feature_frame;timestamp_contract;threshold_identity;risk_lot_identity;package_claim_guard",
                "expected_outputs": "bad_control_result.csv;invalid_condition_matrix.csv;repair_receipt.json;package_claim_boundary_receipt.json",
                "must_fail_to_pass": True,
                "blocker_criteria": row.get("invalid_if", ""),
                "repair_route": row.get("repair_route", ""),
                "execution_allowed": "false",
                "training_allowed": "false",
                "mt5_execution_allowed": "false",
                "next_review": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_no_lookahead_contract(inputs: Mapping[str, Any]) -> dict[str, Any]:
    schema = inputs["no_lookahead_schema"]
    return {
        "contract_id": "stage337H_no_lookahead_canary_harness_package_contract_v1",
        "source_schema": rel(RUN337F_NO_LOOKAHEAD_SCHEMA),
        "bad_control_families": schema.get("bad_control_families", []),
        "must_fail_to_pass": True,
        "required_outputs": ["bad_control_result.csv", "invalid_condition_matrix.csv", "repair_receipt.json"],
        "invalid_if": "any bad control reaches model training, proxy scoring, MT5 handoff, KPI scorecard, or candidate package",
        "execution_allowed": False,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_proxy_mt5_package(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    mt5_by_subject = {row.get("subject", ""): row for row in inputs["mt5_probe"]}
    rows = []
    for proxy in inputs["proxy_expected"]:
        subject = proxy.get("subject", "")
        mt5 = mt5_by_subject.get(subject, {})
        rows.append(
            {
                "package_id": f"{subject}_proxy_mt5_fresh_probe_package_spec",
                "package_family": "proxy_mt5",
                "subject": subject,
                "proxy_required_inputs": proxy.get("required_inputs", ""),
                "proxy_required_outputs": proxy.get("required_output_columns", ""),
                "mt5_required_files": mt5.get("required_files", ""),
                "mt5_required_outputs": mt5.get("required_runtime_outputs", ""),
                "comparison_outputs": mt5.get("required_comparison_outputs", ""),
                "usability_decision": "not_usable_for_kpi_until_fresh_mt5_trade_ledger_and_row_level_difference_review",
                "execution_allowed": "false",
                "training_allowed": "false",
                "mt5_execution_allowed": "false",
                "next_review": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_proxy_mt5_contract(inputs: Mapping[str, Any]) -> dict[str, Any]:
    diff_schema = inputs["proxy_diff_schema"]
    return {
        "contract_id": "stage337H_proxy_mt5_fresh_probe_output_contract_v1",
        "source_schema": rel(RUN337F_PROXY_DIFF_SCHEMA),
        "grain": diff_schema.get("grain", []),
        "required_columns": diff_schema.get("required_columns", []),
        "summary_metrics": diff_schema.get("summary_metrics", []),
        "kpi_authority": diff_schema.get("kpi_authority", "not_authoritative_without_MT5_trade_ledger_and_tester_report"),
        "required_identity": ["threshold_id", "feature_hash", "model_hash", "timestamp_basis", "source_row_hash"],
        "blocked_if": "missing Strategy Tester report, terminal log, trade ledger, telemetry, feature order hash, timestamp basis, or row-level difference",
        "execution_allowed": False,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_core56_package(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for row in inputs["core56"]:
        rows.append(
            {
                "package_id": f"{row.get('core56_blueprint_id', '')}_package_spec",
                "package_family": "core56",
                "step_order": row.get("step_order", ""),
                "source_protocol_id": row.get("source_protocol_id", ""),
                "required_artifacts": row.get("required_artifacts", ""),
                "asof_guard": row.get("asof_guard", ""),
                "blocked_claims": row.get("blocked_claims", ""),
                "expected_outputs": "core56_source_inventory.csv;core56_asof_join_audit.csv;feature_handoff_snapshot.csv;core56_proxy_expected_package.csv;core56_fresh_mt5_probe_package.csv",
                "execution_allowed": "false",
                "training_allowed": "false",
                "mt5_execution_allowed": "false",
                "next_review": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_core56_contract(inputs: Mapping[str, Any]) -> dict[str, Any]:
    schema = inputs["core56_schema"]
    return {
        "contract_id": "stage337H_core56_asof_repair_contract_v1",
        "source_schema": rel(RUN337F_CORE56_SCHEMA),
        "join_keys": schema.get("join_keys", []),
        "required_columns": schema.get("required_columns", []),
        "invalid_if": schema.get("invalid_if", ""),
        "repair_required_if": schema.get("repair_required_if", ""),
        "full_family_claims": "blocked_until_source_inventory_asof_join_handoff_proxy_expected_and_fresh_mt5_probe_reviewed",
        "execution_allowed": False,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_cost_curve_package(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for row in inputs["cost_curve"]:
        rows.append(
            {
                "package_id": f"{row.get('extraction_blueprint_id', '')}_package_spec",
                "package_family": "cost_curve",
                "source_protocol_id": row.get("source_protocol_id", ""),
                "gate_scope": row.get("gate_scope", ""),
                "required_extractors": row.get("required_extractors", ""),
                "required_outputs": row.get("required_outputs", ""),
                "minimum_metrics": row.get("minimum_metrics", ""),
                "failure_memory_trigger": row.get("failure_memory_trigger", ""),
                "execution_allowed": "false",
                "training_allowed": "false",
                "mt5_execution_allowed": "false",
                "next_review": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_cost_curve_contract(inputs: Mapping[str, Any]) -> dict[str, Any]:
    schema = inputs["cost_curve_schema"]
    return {
        "contract_id": "stage337H_cost_direction_curve_extraction_contract_v1",
        "source_schema": rel(RUN337F_COST_CURVE_SCHEMA),
        "reports": schema.get("reports", {}),
        "invalid_if": schema.get("invalid_if", ""),
        "required_report_groups": sorted(schema.get("reports", {}).keys()),
        "claim_boundary_rule": "net/PF/DD/curve claims remain blocked until all reports are materialized and reviewed",
        "execution_allowed": False,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_offense_package(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for row in inputs["offense"]:
        rows.append(
            {
                "package_id": f"{row.get('branch_id', '')}_thesis_package_spec",
                "package_family": "offense",
                "branch_id": row.get("branch_id", ""),
                "allowed_next_step": row.get("allowed_next_step", ""),
                "training_allowed": "false",
                "required_controls": row.get("required_controls", ""),
                "required_evidence_before_training": row.get("required_evidence_before_training", ""),
                "failure_memory_axis": row.get("failure_memory_axis", ""),
                "expected_outputs": "feature_thesis_card.json;data_boundary_contract.json;wfo_split_contract.json;proxy_mt5_package_reference.json;gate_extraction_reference.json",
                "execution_allowed": "false",
                "mt5_execution_allowed": "false",
                "next_review": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_regime_package(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for row in inputs["regime"]:
        rows.append(
            {
                "package_id": f"{row.get('regime_blueprint_id', '')}_package_spec",
                "package_family": "regime",
                "source_protocol_id": row.get("source_protocol_id", ""),
                "regime_source": row.get("regime_source", ""),
                "required_source_identity": row.get("required_source_identity", ""),
                "asof_join_rule": row.get("asof_join_rule", ""),
                "required_checks": row.get("required_checks", ""),
                "slice_outputs": row.get("slice_outputs", ""),
                "expected_outputs": "regime_source_inventory.csv;regime_asof_join_audit.csv;regime_slice_report.csv;regime_revision_policy_receipt.json",
                "execution_allowed": "false",
                "training_allowed": "false",
                "mt5_execution_allowed": "false",
                "next_review": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_regime_contract(inputs: Mapping[str, Any]) -> dict[str, Any]:
    schema = inputs["regime_schema"]
    return {
        "contract_id": "stage337H_economic_regime_asof_join_contract_v1",
        "source_schema": rel(RUN337F_REGIME_SCHEMA),
        "slice_families": schema.get("slice_families", []),
        "required_columns": schema.get("required_columns", []),
        "invalid_if": schema.get("invalid_if", ""),
        "asof_rule": "source_timestamp <= cycle_bar_time and asof_status must not be future_join",
        "execution_allowed": False,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_runtime_package(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for row in inputs["runtime"]:
        rows.append(
            {
                "package_id": f"{row.get('runtime_blueprint_id', '')}_package_spec",
                "package_family": "runtime",
                "subject": row.get("subject", ""),
                "required_files": row.get("required_files", ""),
                "preflight_checks": row.get("preflight_checks", ""),
                "runtime_outputs": row.get("runtime_outputs", ""),
                "comparison_outputs": row.get("comparison_outputs", ""),
                "stress_outputs": row.get("stress_outputs", ""),
                "blocked_if_missing": row.get("blocked_if_missing", ""),
                "runtime_claim_boundary": "future_runtime_probe_package_spec_only_no_mt5_execution_no_runtime_authority",
                "execution_allowed": "false",
                "training_allowed": "false",
                "mt5_execution_allowed": "false",
                "next_review": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_runtime_contract(inputs: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "contract_id": "stage337H_runtime_probe_package_contract_v1",
        "source_blueprint": rel(RUN337F_RUNTIME),
        "required_file_identity": ["EA entrypoint", "include module hash", "model/ONNX spec", "adapter manifest", "feature order", "set file", "tester ini", "handoff snapshot"],
        "required_runtime_outputs": ["Strategy Tester report", "terminal log", "trade ledger", "telemetry", "tester settings identity"],
        "required_comparison_outputs": ["proxy expected", "MT5 observed", "row-level difference", "usability decision"],
        "required_stress_outputs": ["cost stress", "spread/slippage stress", "lot-normalized", "D/B attribution", "long/short", "regime slices", "curve pockets"],
        "execution_allowed": False,
        "mt5_execution_allowed": False,
        "runtime_authority": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_claim_guard_package() -> list[dict[str, Any]]:
    blockers = [
        ("model_training", "training queue or model fit opens before package review"),
        ("mt5_execution", "MT5 tester execution opens before package review"),
        ("threshold_retune", "score threshold changes without predeclared later training packet"),
        ("lot_optimization", "lot logic changes or lot-only improvement is used"),
        ("forward_pocket_filtering", "forward pocket is used as a selection filter"),
        ("candidate_selection", "candidate is selected from package specs"),
        ("forward_passed", "Forward Passed is claimed without fresh runtime and KPI attribution"),
        ("forward_failed", "Forward Failed is claimed from package specs without runtime evidence"),
        ("runtime_authority", "runtime authority is claimed before tester output and row-level parity"),
        ("goal_achieve", "Goal Achieve is claimed before operating-worthy ONNX evidence"),
        ("live_readiness", "live readiness or deployment is claimed from research package specs"),
    ]
    return [
        {
            "blocker_id": blocker_id,
            "package_family": "claim_boundary",
            "blocked_condition": condition,
            "required_response": "stop_claim_and_route_to_repair_or_runtime_evidence_review",
            "claim_status": "not_claimed",
            "execution_allowed": "false",
            "training_allowed": "false",
            "mt5_execution_allowed": "false",
            "next_review": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for blocker_id, condition in blockers
    ]


def build_package_index(package_rows: Mapping[str, Sequence[Mapping[str, Any]]]) -> list[dict[str, Any]]:
    output_paths = {
        "no_lookahead": NO_LOOKAHEAD_PACKAGE_CSV,
        "proxy_mt5": PROXY_MT5_PACKAGE_CSV,
        "core56": CORE56_PACKAGE_CSV,
        "cost_curve": COST_CURVE_PACKAGE_CSV,
        "offense": OFFENSE_PACKAGE_CSV,
        "regime": REGIME_PACKAGE_CSV,
        "runtime": RUNTIME_PACKAGE_CSV,
        "claim_boundary": CLAIM_GUARD_PACKAGE_CSV,
    }
    contract_paths = {
        "no_lookahead": NO_LOOKAHEAD_CONTRACT_JSON,
        "proxy_mt5": PROXY_MT5_CONTRACT_JSON,
        "core56": CORE56_CONTRACT_JSON,
        "cost_curve": COST_CURVE_CONTRACT_JSON,
        "offense": "",
        "regime": REGIME_CONTRACT_JSON,
        "runtime": RUNTIME_CONTRACT_JSON,
        "claim_boundary": BLOCKER_MATRIX_CSV,
    }
    rows: list[dict[str, Any]] = []
    for family, rows_for_family in package_rows.items():
        rows.append(
            {
                "package_family": family,
                "package_artifact": rel(output_paths[family]),
                "contract_artifact": rel(contract_paths[family]) if contract_paths[family] else "",
                "package_rows": len(rows_for_family),
                "execution_allowed": "false",
                "training_allowed": "false",
                "mt5_execution_allowed": "false",
                "review_required": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_acceptance_matrix(package_index: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in package_index:
        accepted = int(row.get("package_rows", 0)) > 0 and row.get("execution_allowed") == "false"
        rows.append(
            {
                "package_family": row.get("package_family", ""),
                "package_artifact": row.get("package_artifact", ""),
                "contract_artifact": row.get("contract_artifact", ""),
                "package_rows": row.get("package_rows", ""),
                "acceptance_status": "accepted_for_run337I_package_review" if accepted else "blocked_missing_package_spec",
                "review_requirement": NEXT_RUN_ID,
                "forbidden": "model training, MT5 execution, candidate selection, Forward Passed, runtime authority, Goal Achieve",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_run337i_queue(package_index: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    labels = {
        "no_lookahead": "review no-lookahead canary harness package specs",
        "proxy_mt5": "review proxy expected and fresh MT5 probe package specs",
        "core56": "review core56 as-of repair package specs",
        "cost_curve": "review cost/direction/curve extraction package specs",
        "offense": "review offense branch thesis package specs and training boundary",
        "regime": "review economic regime as-of join package specs",
        "runtime": "review runtime probe package specs and runtime blocker criteria",
        "claim_boundary": "review claim guard and blocker package specs",
    }
    rows: list[dict[str, Any]] = []
    for index, row in enumerate(package_index, start=1):
        family = row.get("package_family", "")
        rows.append(
            {
                "queue_id": f"review_{family}_package_specs",
                "priority": index,
                "package_family": family,
                "package_artifact": row.get("package_artifact", ""),
                "contract_artifact": row.get("contract_artifact", ""),
                "review_task": labels.get(family, f"review {family} package specs"),
                "required_decision": "accept_for_runner_scaffold_or_repair_package_gap",
                "forbidden": "model training, MT5 execution, candidate selection, Forward Passed, runtime authority, Goal Achieve",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    rows.append(
        {
            "queue_id": "review_package_index_and_claim_boundary",
            "priority": len(rows) + 1,
            "package_family": "package_index",
            "package_artifact": rel(PACKAGE_INDEX_CSV),
            "contract_artifact": rel(PACKAGE_ACCEPTANCE_CSV),
            "review_task": "verify package index, acceptance matrix, blocker matrix, and claim boundary",
            "required_decision": "accept_for_runner_scaffold_or_repair_package_gap",
            "forbidden": "model training, MT5 execution, candidate selection, Forward Passed, runtime authority, Goal Achieve",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )
    return rows


def build_gate_audit(
    source_lineage: Sequence[Mapping[str, Any]],
    package_rows: Mapping[str, Sequence[Mapping[str, Any]]],
    package_index: Sequence[Mapping[str, Any]],
    acceptance: Sequence[Mapping[str, Any]],
    run337i_queue: Sequence[Mapping[str, Any]],
    inputs: Mapping[str, Any],
) -> list[dict[str, Any]]:
    source_ok = all(row.get("lineage_status") == "pass" for row in source_lineage)
    g_gate_ok = all(row.get("status") == "pass" for row in inputs["gate_audit"])
    g_accepted_ok = all(row.get("queue_status") == "accepted_for_run337H_package_materialization" for row in inputs["accepted"])
    no_execution = all(
        row.get("execution_allowed") == "false" and row.get("training_allowed") == "false" and row.get("mt5_execution_allowed") == "false"
        for rows in package_rows.values()
        for row in rows
    )
    family_ready = {family: len(rows) > 0 for family, rows in package_rows.items()}
    acceptance_ok = all(row.get("acceptance_status") == "accepted_for_run337I_package_review" for row in acceptance)
    return [
        {
            "gate_id": "source_lineage_connected",
            "status": "pass" if source_ok and len(source_lineage) >= len(SOURCE_INPUTS) else "fail",
            "evidence": rel(PACKAGE_SOURCE_LINEAGE_CSV),
            "finding": f"source_rows={len(source_lineage)};all_present={source_ok}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "run337G_inputs_accepted",
            "status": "pass" if g_gate_ok and g_accepted_ok and not inputs["repair_gaps"] else "fail",
            "evidence": f"{rel(RUN337G_ACCEPTED)};{rel(RUN337G_GATE_AUDIT)};{rel(RUN337G_REPAIR_GAPS)}",
            "finding": f"run337G_gates_pass={g_gate_ok};accepted={g_accepted_ok};repair_gaps={len(inputs['repair_gaps'])}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "no_lookahead_package_ready",
            "status": "pass" if family_ready["no_lookahead"] else "fail",
            "evidence": rel(NO_LOOKAHEAD_PACKAGE_CSV),
            "finding": f"rows={len(package_rows['no_lookahead'])}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "proxy_mt5_package_ready",
            "status": "pass" if family_ready["proxy_mt5"] else "fail",
            "evidence": rel(PROXY_MT5_PACKAGE_CSV),
            "finding": f"rows={len(package_rows['proxy_mt5'])}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "core56_package_ready",
            "status": "pass" if family_ready["core56"] else "fail",
            "evidence": rel(CORE56_PACKAGE_CSV),
            "finding": f"rows={len(package_rows['core56'])}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "cost_direction_curve_package_ready",
            "status": "pass" if family_ready["cost_curve"] else "fail",
            "evidence": rel(COST_CURVE_PACKAGE_CSV),
            "finding": f"rows={len(package_rows['cost_curve'])}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "offense_package_training_closed",
            "status": "pass" if family_ready["offense"] and all(row.get("training_allowed") == "false" for row in package_rows["offense"]) else "fail",
            "evidence": rel(OFFENSE_PACKAGE_CSV),
            "finding": f"rows={len(package_rows['offense'])}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "regime_package_ready",
            "status": "pass" if family_ready["regime"] else "fail",
            "evidence": rel(REGIME_PACKAGE_CSV),
            "finding": f"rows={len(package_rows['regime'])}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "runtime_package_probe_only",
            "status": "pass" if family_ready["runtime"] and all("no_runtime_authority" in row.get("runtime_claim_boundary", "") for row in package_rows["runtime"]) else "fail",
            "evidence": rel(RUNTIME_PACKAGE_CSV),
            "finding": f"rows={len(package_rows['runtime'])}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "claim_guard_blocker_ready",
            "status": "pass" if family_ready["claim_boundary"] and len(package_rows["claim_boundary"]) >= 10 else "fail",
            "evidence": rel(CLAIM_GUARD_PACKAGE_CSV),
            "finding": f"blocker_rows={len(package_rows['claim_boundary'])}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "all_packages_execution_closed",
            "status": "pass" if no_execution else "fail",
            "evidence": rel(PACKAGE_INDEX_CSV),
            "finding": f"execution_training_mt5_closed={no_execution}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "package_acceptance_ready",
            "status": "pass" if acceptance_ok and len(acceptance) >= 8 else "fail",
            "evidence": rel(PACKAGE_ACCEPTANCE_CSV),
            "finding": f"acceptance_rows={len(acceptance)};accepted={acceptance_ok}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "run337I_review_queue_ready",
            "status": "pass" if len(run337i_queue) >= 9 else "fail",
            "evidence": rel(RUN337I_QUEUE_CSV),
            "finding": f"run337I_queue_rows={len(run337i_queue)}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "claim_guard_no_selection_no_goal",
            "status": "pass",
            "evidence": rel(FINAL_DECISION_JSON),
            "finding": "no model training, MT5 execution, candidate selection, Forward decision, runtime authority, or Goal Achieve claimed",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_metrics(
    source_lineage: Sequence[Mapping[str, Any]],
    package_rows: Mapping[str, Sequence[Mapping[str, Any]]],
    package_index: Sequence[Mapping[str, Any]],
    acceptance: Sequence[Mapping[str, Any]],
    run337i_queue: Sequence[Mapping[str, Any]],
    audit: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    return {
        "source_lineage_rows": len(source_lineage),
        "package_family_count": len(package_rows),
        "package_spec_rows": sum(len(rows) for rows in package_rows.values()),
        "package_index_rows": len(package_index),
        "package_acceptance_rows": len(acceptance),
        "accepted_package_rows": len([row for row in acceptance if row.get("acceptance_status") == "accepted_for_run337I_package_review"]),
        "run337i_queue_rows": len(run337i_queue),
        "gate_rows": len(audit),
        "failed_gate_rows": len([row for row in audit if row.get("status") != "pass"]),
    }


def write_receipts(metrics: Mapping[str, Any]) -> list[Path]:
    return [
        write_json(
            EXPERIMENT_DESIGN_JSON,
            {
                "run_id": RUN_ID,
                "hypothesis": "run337G accepted blueprints can be converted into package specs without opening training or MT5 execution",
                "decision_use": "allow run337I to review materialized package specs before any runner scaffold or execution attempt",
                "comparison_baseline": "run337G accepted blueprint queue and run337F source blueprints",
                "control_variables": "no model training, no MT5 execution, no threshold retune, no lot optimization, no forward-pocket filtering, no candidate selection",
                "changed_variables": "package spec files, output contracts, blocker matrix, package index, run337I review queue",
                "sample_scope": "package specs only; no trading KPI sample, no model fit, no MT5 trade rows",
                "success_criteria": "all eight package families materialized, execution closed, gates pass, and run337I queue is ready",
                "failure_criteria": "missing package family, missing contract, open execution flag, or missing blocker criteria",
                "invalid_conditions": "using package specs to claim Forward Passed, runtime authority, candidate selection, or Goal Achieve",
                "stop_conditions": "any gate fails; repair package spec before review",
                "evidence_plan": "package CSVs, contract JSONs, blocker matrix, acceptance matrix, run337I queue, gate audit, receipts, report, ledgers",
                "metrics": metrics,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            DATA_INTEGRITY_JSON,
            {
                "run_id": RUN_ID,
                "data_source": "run337G review outputs and run337F blueprint/schema artifacts",
                "time_axis": "future packages must carry cycle_bar_time, source_timestamp, broker timezone, timestamp basis, as-of status, and source_row_hash",
                "sample_scope": "package materialization only; no new US100 M5 bars are consumed",
                "missing_or_duplicate_check": "future packages require missing, duplicate, stale, revision, timezone, and future join checks",
                "feature_label_boundary": "no labels or fit; canary harness package must block future-derived feature use before any later execution",
                "split_boundary": "future train/WFO/forward split remains closed until package review and later materialization are accepted",
                "leakage_risk": "future-bar features, forward-pocket selection, threshold retune, lot optimization, timestamp drift, macro revision drift",
                "data_hash_or_identity": rel(PACKAGE_SOURCE_LINEAGE_CSV),
                "integrity_judgment": "usable_with_boundary",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RUNTIME_PARITY_JSON,
            {
                "run_id": RUN_ID,
                "research_path": rel(Path(__file__)),
                "runtime_path": rel(RUNTIME_PACKAGE_CSV),
                "shared_contract": "feature order, threshold, risk, lot, timestamp basis, proxy expected, MT5 observed, tester report, trade ledger, D/B source, cost stress, and regime slices must match before KPI authority",
                "known_differences": "run337H writes package specs only; no MT5 execution and no proxy/MT5 observed values are produced",
                "parity_check": "runtime package contract keeps fresh MT5 probe and row-level proxy-MT5 difference mandatory for later review",
                "parity_identity": rel(PROXY_MT5_CONTRACT_JSON),
                "runtime_claim_boundary": "package_spec_only_no_runtime_authority",
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
                    rel(PACKAGE_SOURCE_LINEAGE_CSV),
                    rel(PACKAGE_INDEX_CSV),
                    rel(PACKAGE_ACCEPTANCE_CSV),
                    rel(RUN337I_QUEUE_CSV),
                    rel(GATE_AUDIT_CSV),
                ],
                "artifact_hashes": "registered in artifact_registry after run",
                "registry_links": "run_registry;alpha_run_ledger;stage_run_ledger;artifact_registry",
                "availability": "tracked after commit; reproducible from run337H script",
                "lineage_judgment": "connected_with_boundary",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RESULT_JUDGMENT_JSON,
            {
                "run_id": RUN_ID,
                "result_subject": "reviewed execution package specs",
                "evidence_available": "package specs, contracts, blocker matrix, package index, run337I review queue, gate audit",
                "evidence_missing": "no model training, no MT5 execution, no proxy expected values, no MT5 observed values, no candidate KPI",
                "judgment_label": "exploratory",
                "claim_boundary": "package specs are materialized for review only; no candidate, Forward decision, or runtime authority",
                "next_condition": NEXT_RUN_ID,
                "user_explanation_hook": "패키지 명세는 생겼지만 아직 실행 가능한 결과는 아니다. 다음 단계는 이 명세가 실제 러너로 가도 되는지 검토하는 일이다.",
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
# run337H Reviewed Execution Packages(337H 검토된 실행 패키지 명세)

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

## Package Result(패키지 결과)

- source_lineage_rows(원천 계보 행): `{metrics['source_lineage_rows']}`
- package_family_count(패키지 묶음 수): `{metrics['package_family_count']}`
- package_spec_rows(패키지 명세 행): `{metrics['package_spec_rows']}`
- package_index_rows(패키지 색인 행): `{metrics['package_index_rows']}`
- package_acceptance_rows(패키지 승인 행): `{metrics['package_acceptance_rows']}`
- run337I_queue_rows(337I 대기열 행): `{metrics['run337i_queue_rows']}`
- gate_rows(게이트 행): `{metrics['gate_rows']}`, failed(실패): `{metrics['failed_gate_rows']}`

Effect(효과): run337H(337H 실행)는 run337G(337G 실행)가 승인한 8개 청사진 묶음을 package spec(패키지 명세), contract(계약), blocker matrix(차단 행렬), package index(패키지 색인), run337I review queue(337I 검토 대기열)로 물질화했다. 아직 model training(모델 학습), MT5 execution(MT5 실행), candidate selection(후보 선택)은 없다.
"""
    decision = f"""
# 2026-05-27 Stage337H Decision(337H 결정)

- decision(결정): `{DECISION}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed_for_stage337_new_work`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`

Effect(효과): 다음 run337I(337I 실행)는 materialized package specs(물질화된 패키지 명세)를 검토한다. 이 결정은 학습 허가, MT5 실행 결과, Forward 판정, 운영 승격이 아니다.
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
- effect(효과): run337H(337H 실행)는 reviewed execution package specs(검토된 실행 패키지 명세)를 만들고 run337I(337I 실행) 검토로 넘겼다. 아직 선택 후보는 없다.
"""
    artifacts.append(write_md(SELECTED_DIR / "selection_status.md", selection))

    brief_text, brief_bom = read_text_lossless(SPEC_DIR / "stage_brief.md")
    brief_text = replace_prefix_line(brief_text, "- latest_run(최신 실행):", f"- latest_run(최신 실행): `{RUN_ID}`")
    brief_text = insert_after_marker_once(
        brief_text,
        "- run337G_summary(337G 요약):",
        f"- run337H_summary(337H 요약): `{STATUS}`. Effect(효과): run337G(337G 실행)가 승인한 8개 청사진 묶음을 reviewed package spec(검토된 패키지 명세)과 run337I(337I 실행) 검토 대기열로 물질화한다.",
        "run337H_summary",
    )
    artifacts.append(write_text_lossless(SPEC_DIR / "stage_brief.md", brief_text, brief_bom))

    input_section = f"""
- package_source_lineage_review(패키지 원천 계보 검토): `{rel(PACKAGE_SOURCE_LINEAGE_CSV)}`
- no_lookahead_canary_harness_package_spec(미래참조 방어 패키지 명세): `{rel(NO_LOOKAHEAD_PACKAGE_CSV)}`
- proxy_mt5_fresh_probe_package_spec(프록시-MT5 신규 탐침 패키지 명세): `{rel(PROXY_MT5_PACKAGE_CSV)}`
- core56_asof_repair_package_spec(핵심56 시점 기준 수리 패키지 명세): `{rel(CORE56_PACKAGE_CSV)}`
- cost_direction_curve_extraction_package_spec(비용/방향/곡선 추출 패키지 명세): `{rel(COST_CURVE_PACKAGE_CSV)}`
- offense_branch_thesis_package_spec(공격 분기 논제 패키지 명세): `{rel(OFFENSE_PACKAGE_CSV)}`
- economic_regime_asof_join_package_spec(경제 국면 시점 기준 조인 패키지 명세): `{rel(REGIME_PACKAGE_CSV)}`
- runtime_probe_package_spec(런타임 탐침 패키지 명세): `{rel(RUNTIME_PACKAGE_CSV)}`
- package_blocker_matrix(패키지 차단 행렬): `{rel(BLOCKER_MATRIX_CSV)}`
- package_manifest_index(패키지 색인): `{rel(PACKAGE_INDEX_CSV)}`
- run337I_queue(337I 대기열): `{rel(RUN337I_QUEUE_CSV)}`

Effect(효과): 다음 실행은 이 패키지 명세들이 실제 runner scaffold(러너 뼈대)로 넘어가도 되는지 검토한다.
"""
    artifacts.append(append_section_once(INPUTS_DIR / "input_refs.md", "## run337H Outputs(337H 산출물)", input_section))

    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_prefix_line(workspace_text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    focus = (
        "- >-\n"
        f"  Stage337 run337H focus complete: Stage337(337단계) run337H(337H 실행)는 `{STATUS}`로 reviewed execution package specs(검토된 실행 패키지 명세)를 물질화했다. "
        "Effect(효과): run337I(337I 실행) package review(패키지 검토) 대기열을 열었지만 model training(모델 학습), MT5 execution(MT5 실행), candidate selection(후보 선택)은 아직 닫아둔다.\n"
    )
    workspace_text = insert_focus_once(workspace_text, focus, "Stage337 run337H focus complete")
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
        f"- run337H_summary(337H 요약): `{STATUS}`. "
        "Effect(효과): 8개 패키지 명세와 차단 행렬을 만들고 run337I(337I 실행) 검토 대기열로 넘기며, 학습/MT5/후보 선택은 계속 닫아둔다."
    )
    current_text = insert_after_marker_once(current_text, "- decision(결정):", summary, "run337H_summary")
    artifacts.append(write_text_lossless(CURRENT_STATE, current_text, current_bom))

    artifacts.append(
        append_section_once(
            CHANGELOG,
            "## Stage337H Reviewed Execution Package Materialization(337H 검토된 실행 패키지 물질화)",
            f"""
- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- action(행동): run337G(337G 실행)의 승인 청사진을 8개 package spec(패키지 명세), contract(계약), blocker matrix(차단 행렬), run337I(337I 실행) 검토 대기열로 물질화했다.
- effect(효과): 다음 실행은 실제 러너나 실행으로 가기 전 패키지 명세의 안전성을 검토할 수 있다.
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
                "lane": "reviewed_execution_package_materialization",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_DOC),
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};packages_materialized;training_not_allowed;mt5_not_executed;goal_achieve_not_claimed.",
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__reviewed_execution_packages",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "reviewed_execution_package_materialization",
                "tier_scope": "stage337_package_boundary_macro48_u42_core56",
                "kpi_scope": "package_spec_only_no_new_candidate_kpi",
                "scoreboard_lane": "package_review_readiness",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_DOC),
                "primary_kpi": "package_families=8;run337i_queue_rows=9;candidate_selection=none",
                "guardrail_kpi": "training_not_allowed;mt5_not_executed;runtime_authority_not_claimed;goal_achieve_not_claimed",
                "external_verification_status": "out_of_scope_by_claim_package_spec_only",
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
                "ledger_row_id": f"{RUN_ID}__reviewed_execution_packages",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "work_family": "artifact_materialization",
                "evidence_scope": "run337G_accepted_blueprints_and_run337F_source_blueprints",
                "kpi_scope": "package_spec_only_no_new_candidate_kpi",
                "status": STATUS,
                "judgment": JUDGMENT,
                "claim_boundary": CLAIM_BOUNDARY,
                "path": rel(REPORT_DOC),
                "notes": f"next_action={NEXT_RUN_ID};packages_materialized;training_not_allowed;mt5_not_executed;goal_achieve_not_claimed.",
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
            "notes": "run337H_reviewed_execution_packages_no_selection",
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
    source_lineage = build_source_lineage()
    package_rows = {
        "no_lookahead": build_no_lookahead_package(inputs),
        "proxy_mt5": build_proxy_mt5_package(inputs),
        "core56": build_core56_package(inputs),
        "cost_curve": build_cost_curve_package(inputs),
        "offense": build_offense_package(inputs),
        "regime": build_regime_package(inputs),
        "runtime": build_runtime_package(inputs),
        "claim_boundary": build_claim_guard_package(),
    }
    package_index = build_package_index(package_rows)
    acceptance = build_acceptance_matrix(package_index)
    run337i_queue = build_run337i_queue(package_index)
    blocker_matrix = build_claim_guard_package()
    audit = build_gate_audit(source_lineage, package_rows, package_index, acceptance, run337i_queue, inputs)
    metrics = build_metrics(source_lineage, package_rows, package_index, acceptance, run337i_queue, audit)
    failed_gates = [row for row in audit if row.get("status") != "pass"]

    run_artifacts = [
        write_csv(
            PACKAGE_SOURCE_LINEAGE_CSV,
            ("source_path", "exists", "sha256", "row_count_or_keys", "package_use", "forbidden_use", "lineage_status", "claim_boundary"),
            source_lineage,
        ),
        write_csv(
            NO_LOOKAHEAD_PACKAGE_CSV,
            (
                "package_id",
                "package_family",
                "source_harness_id",
                "required_inputs",
                "expected_outputs",
                "must_fail_to_pass",
                "blocker_criteria",
                "repair_route",
                "execution_allowed",
                "training_allowed",
                "mt5_execution_allowed",
                "next_review",
                "claim_boundary",
            ),
            package_rows["no_lookahead"],
        ),
        write_json(NO_LOOKAHEAD_CONTRACT_JSON, build_no_lookahead_contract(inputs)),
        write_csv(
            PROXY_MT5_PACKAGE_CSV,
            (
                "package_id",
                "package_family",
                "subject",
                "proxy_required_inputs",
                "proxy_required_outputs",
                "mt5_required_files",
                "mt5_required_outputs",
                "comparison_outputs",
                "usability_decision",
                "execution_allowed",
                "training_allowed",
                "mt5_execution_allowed",
                "next_review",
                "claim_boundary",
            ),
            package_rows["proxy_mt5"],
        ),
        write_json(PROXY_MT5_CONTRACT_JSON, build_proxy_mt5_contract(inputs)),
        write_csv(
            CORE56_PACKAGE_CSV,
            (
                "package_id",
                "package_family",
                "step_order",
                "source_protocol_id",
                "required_artifacts",
                "asof_guard",
                "blocked_claims",
                "expected_outputs",
                "execution_allowed",
                "training_allowed",
                "mt5_execution_allowed",
                "next_review",
                "claim_boundary",
            ),
            package_rows["core56"],
        ),
        write_json(CORE56_CONTRACT_JSON, build_core56_contract(inputs)),
        write_csv(
            COST_CURVE_PACKAGE_CSV,
            (
                "package_id",
                "package_family",
                "source_protocol_id",
                "gate_scope",
                "required_extractors",
                "required_outputs",
                "minimum_metrics",
                "failure_memory_trigger",
                "execution_allowed",
                "training_allowed",
                "mt5_execution_allowed",
                "next_review",
                "claim_boundary",
            ),
            package_rows["cost_curve"],
        ),
        write_json(COST_CURVE_CONTRACT_JSON, build_cost_curve_contract(inputs)),
        write_csv(
            OFFENSE_PACKAGE_CSV,
            (
                "package_id",
                "package_family",
                "branch_id",
                "allowed_next_step",
                "training_allowed",
                "required_controls",
                "required_evidence_before_training",
                "failure_memory_axis",
                "expected_outputs",
                "execution_allowed",
                "mt5_execution_allowed",
                "next_review",
                "claim_boundary",
            ),
            package_rows["offense"],
        ),
        write_csv(
            REGIME_PACKAGE_CSV,
            (
                "package_id",
                "package_family",
                "source_protocol_id",
                "regime_source",
                "required_source_identity",
                "asof_join_rule",
                "required_checks",
                "slice_outputs",
                "expected_outputs",
                "execution_allowed",
                "training_allowed",
                "mt5_execution_allowed",
                "next_review",
                "claim_boundary",
            ),
            package_rows["regime"],
        ),
        write_json(REGIME_CONTRACT_JSON, build_regime_contract(inputs)),
        write_csv(
            RUNTIME_PACKAGE_CSV,
            (
                "package_id",
                "package_family",
                "subject",
                "required_files",
                "preflight_checks",
                "runtime_outputs",
                "comparison_outputs",
                "stress_outputs",
                "blocked_if_missing",
                "runtime_claim_boundary",
                "execution_allowed",
                "training_allowed",
                "mt5_execution_allowed",
                "next_review",
                "claim_boundary",
            ),
            package_rows["runtime"],
        ),
        write_json(RUNTIME_CONTRACT_JSON, build_runtime_contract(inputs)),
        write_csv(
            CLAIM_GUARD_PACKAGE_CSV,
            (
                "blocker_id",
                "package_family",
                "blocked_condition",
                "required_response",
                "claim_status",
                "execution_allowed",
                "training_allowed",
                "mt5_execution_allowed",
                "next_review",
                "claim_boundary",
            ),
            package_rows["claim_boundary"],
        ),
        write_csv(
            BLOCKER_MATRIX_CSV,
            (
                "blocker_id",
                "package_family",
                "blocked_condition",
                "required_response",
                "claim_status",
                "execution_allowed",
                "training_allowed",
                "mt5_execution_allowed",
                "next_review",
                "claim_boundary",
            ),
            blocker_matrix,
        ),
        write_csv(
            PACKAGE_INDEX_CSV,
            (
                "package_family",
                "package_artifact",
                "contract_artifact",
                "package_rows",
                "execution_allowed",
                "training_allowed",
                "mt5_execution_allowed",
                "review_required",
                "claim_boundary",
            ),
            package_index,
        ),
        write_csv(
            PACKAGE_ACCEPTANCE_CSV,
            (
                "package_family",
                "package_artifact",
                "contract_artifact",
                "package_rows",
                "acceptance_status",
                "review_requirement",
                "forbidden",
                "claim_boundary",
            ),
            acceptance,
        ),
        write_csv(
            RUN337I_QUEUE_CSV,
            (
                "queue_id",
                "priority",
                "package_family",
                "package_artifact",
                "contract_artifact",
                "review_task",
                "required_decision",
                "forbidden",
                "claim_boundary",
            ),
            run337i_queue,
        ),
        write_csv(GATE_AUDIT_CSV, ("gate_id", "status", "evidence", "finding", "claim_boundary"), audit),
    ]
    run_artifacts.extend(write_receipts(metrics))
    final_payload = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS if not failed_gates else "blocked_stage337H_package_materialization_gate_failure",
        "judgment": JUDGMENT if not failed_gates else "stage337H_package_materialization_requires_repair",
        "decision": DECISION if not failed_gates else "stage337H_package_materialization_blocked_gate_failure",
        "metrics": metrics,
        "failed_gates": failed_gates,
        "next_action": NEXT_RUN_ID if not failed_gates else "repair_run337H_package_specs_before_review",
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
                "status": "blocked_stage337H_package_materialization_gate_failure",
                "decision": "stage337H_package_materialization_blocked_gate_failure",
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
        "external_verification_status": "out_of_scope_by_claim_package_spec_only_no_mt5_execution",
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
                "package_family_count": metrics["package_family_count"],
                "package_spec_rows": metrics["package_spec_rows"],
                "run337I_queue_rows": metrics["run337i_queue_rows"],
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
