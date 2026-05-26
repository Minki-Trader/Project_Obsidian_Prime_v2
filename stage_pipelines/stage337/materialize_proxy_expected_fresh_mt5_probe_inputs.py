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
RUN_NUMBER = "run337L"
RUN_ID = "run337L_materialize_proxy_expected_fresh_mt5_probe_inputs_v1"
PARENT_RUN_ID = "run337K_review_runner_scaffolds_v1"
NEXT_RUN_ID = "run337M_review_proxy_expected_fresh_mt5_probe_inputs_v1"
STATUS = "completed_proxy_expected_fresh_mt5_probe_inputs_materialized_no_mt5_execution"
JUDGMENT = "stage337L_proxy_mt5_input_packages_materialized_for_review_no_execution_no_selection"
DECISION = "stage337L_proxy_mt5_inputs_ready_for_run337M_review_no_training_no_mt5_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage337L_proxy_mt5_input_materialization_no_model_training_"
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
RUN337K_DIR = STAGE_DIR / "02_runs" / "run337K"
RUN337J_DIR = STAGE_DIR / "02_runs" / "run337J"
RUN337H_DIR = STAGE_DIR / "02_runs" / "run337H"
RUN337B_DIR = STAGE_DIR / "02_runs" / "run337B"
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
DECISION_DOC = DOCS / "decisions" / "2026-05-27_stage337L_proxy_mt5_probe_inputs.md"
REPORT_DOC = REVIEWS_DIR / "run337L_proxy_expected_fresh_mt5_probe_inputs.md"

RUN337K_QUEUE_CSV = RUN337K_DIR / "run337L_proxy_mt5_input_materialization_queue.csv"
RUN337K_ACCEPTED_CSV = RUN337K_DIR / "accepted_scaffolds_for_run337L_materialization.csv"
RUN337K_DECISION_JSON = RUN337K_DIR / "final_runner_scaffold_review_decision.json"
RUN337K_MANIFEST_JSON = RUN337K_DIR / "run_manifest.json"
RUN337K_GATE_AUDIT_CSV = RUN337K_DIR / "required_gate_coverage_audit.csv"

NO_LOOKAHEAD_SCAFFOLD_CSV = RUN337J_DIR / "no_lookahead_runner_scaffold.csv"
PROXY_MT5_SCAFFOLD_CSV = RUN337J_DIR / "proxy_mt5_runner_scaffold.csv"
RUNTIME_SCAFFOLD_CSV = RUN337J_DIR / "runtime_probe_runner_scaffold.csv"
CORE56_SCAFFOLD_CSV = RUN337J_DIR / "core56_asof_runner_scaffold.csv"
COST_CURVE_SCAFFOLD_CSV = RUN337J_DIR / "cost_direction_curve_runner_scaffold.csv"
REGIME_SCAFFOLD_CSV = RUN337J_DIR / "economic_regime_asof_runner_scaffold.csv"
CLAIM_GUARD_SCAFFOLD_CSV = RUN337J_DIR / "claim_guard_runner_scaffold.csv"
PACKAGE_INDEX_SCAFFOLD_CSV = RUN337J_DIR / "package_index_runner_scaffold.csv"

NO_LOOKAHEAD_PACKAGE_CSV = RUN337H_DIR / "no_lookahead_canary_harness_package_spec.csv"
PROXY_MT5_PACKAGE_CSV = RUN337H_DIR / "proxy_mt5_fresh_probe_package_spec.csv"
RUNTIME_PACKAGE_CSV = RUN337H_DIR / "runtime_probe_package_spec.csv"
CORE56_PACKAGE_CSV = RUN337H_DIR / "core56_asof_repair_package_spec.csv"
COST_CURVE_PACKAGE_CSV = RUN337H_DIR / "cost_direction_curve_extraction_package_spec.csv"
REGIME_PACKAGE_CSV = RUN337H_DIR / "economic_regime_asof_join_package_spec.csv"
CLAIM_GUARD_PACKAGE_CSV = RUN337H_DIR / "claim_guard_blocker_package_spec.csv"
PACKAGE_INDEX_CSV = RUN337H_DIR / "package_manifest_index.csv"

RUN337B_PROXY_EXPECTED_CSV = RUN337B_DIR / "proxy_expected_signal_values.csv"
RUN337B_MT5_OBSERVED_CSV = RUN337B_DIR / "mt5_runtime_probe_observed_values.csv"
RUN337B_PROXY_DIFF_CSV = RUN337B_DIR / "proxy_mt5_difference_report.csv"
RUN337B_USABILITY_CSV = RUN337B_DIR / "proxy_mt5_usability_decision.csv"

SOURCE_INPUTS: tuple[Path, ...] = (
    RUN337K_QUEUE_CSV,
    RUN337K_ACCEPTED_CSV,
    RUN337K_DECISION_JSON,
    RUN337K_MANIFEST_JSON,
    RUN337K_GATE_AUDIT_CSV,
    NO_LOOKAHEAD_SCAFFOLD_CSV,
    PROXY_MT5_SCAFFOLD_CSV,
    RUNTIME_SCAFFOLD_CSV,
    CORE56_SCAFFOLD_CSV,
    COST_CURVE_SCAFFOLD_CSV,
    REGIME_SCAFFOLD_CSV,
    CLAIM_GUARD_SCAFFOLD_CSV,
    PACKAGE_INDEX_SCAFFOLD_CSV,
    NO_LOOKAHEAD_PACKAGE_CSV,
    PROXY_MT5_PACKAGE_CSV,
    RUNTIME_PACKAGE_CSV,
    CORE56_PACKAGE_CSV,
    COST_CURVE_PACKAGE_CSV,
    REGIME_PACKAGE_CSV,
    CLAIM_GUARD_PACKAGE_CSV,
    PACKAGE_INDEX_CSV,
    RUN337B_PROXY_EXPECTED_CSV,
    RUN337B_MT5_OBSERVED_CSV,
    RUN337B_PROXY_DIFF_CSV,
    RUN337B_USABILITY_CSV,
)

SOURCE_LINEAGE_CSV = RUN_DIR / "source_lineage_index.csv"
NO_LOOKAHEAD_GUARDS_CSV = RUN_DIR / "no_lookahead_pre_execution_guards.csv"
PROXY_EXPECTED_TEMPLATE_CSV = RUN_DIR / "proxy_expected_result_template.csv"
PROXY_SOURCE_MANIFEST_JSON = RUN_DIR / "proxy_expected_source_identity_manifest.json"
FRESH_MT5_HANDOFF_PACKAGE_CSV = RUN_DIR / "fresh_mt5_probe_handoff_package.csv"
MT5_EXECUTION_MANIFEST_JSON = RUN_DIR / "mt5_probe_execution_manifest.json"
MT5_HANDOFF_PREFLIGHT_CSV = RUN_DIR / "mt5_probe_handoff_precheck.csv"
MT5_TESTER_INPUT_MANIFEST_CSV = RUN_DIR / "mt5_tester_input_manifest.csv"
DIFFERENCE_CONTRACT_CSV = RUN_DIR / "proxy_mt5_difference_runner_contract.csv"
USABILITY_CONTRACT_CSV = RUN_DIR / "usability_decision_runner_contract.csv"
CORE56_HANDOFF_PACKAGE_CSV = RUN_DIR / "core56_asof_source_handoff_package.csv"
COST_CURVE_EXTRACTOR_PACKAGE_CSV = RUN_DIR / "cost_direction_curve_extractor_package.csv"
REGIME_SOURCE_INVENTORY_CSV = RUN_DIR / "regime_asof_source_inventory.csv"
RUNTIME_IDENTITY_PREFLIGHT_CSV = RUN_DIR / "runtime_identity_preflight_package.csv"
CLAIM_OUTPUT_REGISTRY_BINDING_CSV = RUN_DIR / "claim_boundary_output_registry_binding.csv"
RUN337M_QUEUE_CSV = RUN_DIR / "run337M_proxy_mt5_input_review_queue.csv"
GATE_AUDIT_CSV = RUN_DIR / "required_gate_coverage_audit.csv"
RESULT_JUDGMENT_CSV = RUN_DIR / "result_judgment.csv"

EXPERIMENT_DESIGN_JSON = RUN_DIR / "experiment_design_receipt.json"
DATA_INTEGRITY_JSON = RUN_DIR / "data_integrity_receipt.json"
RUNTIME_PARITY_JSON = RUN_DIR / "runtime_parity_receipt.json"
ARTIFACT_LINEAGE_JSON = RUN_DIR / "artifact_lineage_receipt.json"
RESULT_JUDGMENT_JSON = RUN_DIR / "result_judgment_receipt.json"
FINAL_DECISION_JSON = RUN_DIR / "final_proxy_mt5_probe_input_materialization_decision.json"
RUN_MANIFEST_JSON = RUN_DIR / "run_manifest.json"

SUBJECT_DIMENSIONS = ("feature_ready_count", "model_ok_count", "long_count", "short_count", "flat_count")


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return io_path(item).resolve().relative_to(io_path(ROOT).resolve()).as_posix()
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


def split_semicolon(value: Any) -> list[str]:
    return [item.strip() for item in str(value or "").split(";") if item.strip()]


def load_inputs() -> dict[str, Any]:
    return {
        "parent_decision": read_json(RUN337K_DECISION_JSON),
        "parent_manifest": read_json(RUN337K_MANIFEST_JSON),
        "parent_gates": read_csv(RUN337K_GATE_AUDIT_CSV),
        "queue": read_csv(RUN337K_QUEUE_CSV),
        "accepted": read_csv(RUN337K_ACCEPTED_CSV),
        "no_lookahead_scaffold": read_csv(NO_LOOKAHEAD_SCAFFOLD_CSV),
        "proxy_scaffold": read_csv(PROXY_MT5_SCAFFOLD_CSV),
        "runtime_scaffold": read_csv(RUNTIME_SCAFFOLD_CSV),
        "core56_scaffold": read_csv(CORE56_SCAFFOLD_CSV),
        "cost_scaffold": read_csv(COST_CURVE_SCAFFOLD_CSV),
        "regime_scaffold": read_csv(REGIME_SCAFFOLD_CSV),
        "claim_scaffold": read_csv(CLAIM_GUARD_SCAFFOLD_CSV),
        "package_index_scaffold": read_csv(PACKAGE_INDEX_SCAFFOLD_CSV),
        "no_lookahead_package": read_csv(NO_LOOKAHEAD_PACKAGE_CSV),
        "proxy_package": read_csv(PROXY_MT5_PACKAGE_CSV),
        "runtime_package": read_csv(RUNTIME_PACKAGE_CSV),
        "core56_package": read_csv(CORE56_PACKAGE_CSV),
        "cost_package": read_csv(COST_CURVE_PACKAGE_CSV),
        "regime_package": read_csv(REGIME_PACKAGE_CSV),
        "claim_package": read_csv(CLAIM_GUARD_PACKAGE_CSV),
        "package_index": read_csv(PACKAGE_INDEX_CSV),
        "prior_proxy": read_csv(RUN337B_PROXY_EXPECTED_CSV),
        "prior_mt5": read_csv(RUN337B_MT5_OBSERVED_CSV),
        "prior_diff": read_csv(RUN337B_PROXY_DIFF_CSV),
        "prior_usability": read_csv(RUN337B_USABILITY_CSV),
    }


def validate_inputs(inputs: Mapping[str, Any]) -> None:
    parent = inputs["parent_decision"]
    manifest = inputs["parent_manifest"]
    if parent.get("next_action") != RUN_ID or manifest.get("next_action") != RUN_ID:
        raise RuntimeError("run337K does not point to run337L.")
    if parent.get("status") != "completed_runner_scaffold_review_accepts_run337L_materialization_no_training_no_mt5":
        raise RuntimeError("run337K status is not accepted materialization.")
    if parent.get("model_training") != "not_run" or parent.get("mt5_execution") != "not_run":
        raise RuntimeError("parent unexpectedly opened training or MT5 execution.")
    if parent.get("goal_achieve") != "not_claimed":
        raise RuntimeError("parent unexpectedly claimed Goal Achieve.")
    if any(row.get("status") != "pass" for row in inputs["parent_gates"]):
        raise RuntimeError("run337K has failed gate rows.")
    if len(inputs["queue"]) != 9:
        raise RuntimeError(f"expected run337L queue 9 rows, got {len(inputs['queue'])}")
    accepted = [row for row in inputs["accepted"] if row.get("accepted_for_run337L") == "true"]
    if len(accepted) != 9:
        raise RuntimeError(f"expected 9 accepted scaffold families, got {len(accepted)}")
    expected_counts = {
        "no_lookahead_package": 5,
        "proxy_package": 5,
        "runtime_package": 5,
        "core56_package": 5,
        "cost_package": 5,
        "regime_package": 6,
        "claim_package": 11,
        "prior_proxy": 20,
        "prior_mt5": 20,
        "prior_diff": 4,
        "prior_usability": 5,
    }
    for key, expected in expected_counts.items():
        actual = len(inputs[key])
        if actual != expected:
            raise RuntimeError(f"{key} expected {expected} rows, got {actual}")


def build_source_lineage() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in SOURCE_INPUTS:
        exists = path_exists(path)
        rows.append(
            {
                "source_path": rel(path),
                "exists": exists,
                "sha256": sha256_file_lf_normalized(path) if exists else "",
                "role": "run337L input materialization source",
                "consumer": RUN_ID,
                "availability": "tracked_or_source_artifact_present" if exists else "missing",
                "lineage_judgment": "connected_with_boundary" if exists else "blocked_missing_source",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def prior_proxy_map(rows: Sequence[Mapping[str, str]]) -> dict[tuple[str, str], Mapping[str, str]]:
    return {(row.get("attempt_name", ""), row.get("dimension", "")): row for row in rows}


def prior_mt5_map(rows: Sequence[Mapping[str, str]]) -> dict[tuple[str, str], Mapping[str, str]]:
    return {(row.get("attempt_name", ""), row.get("dimension", "")): row for row in rows}


def build_no_lookahead_guards(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for package in inputs["no_lookahead_package"]:
        rows.append(
            {
                "guard_id": package.get("source_harness_id", ""),
                "package_id": package.get("package_id", ""),
                "required_inputs": package.get("required_inputs", ""),
                "expected_outputs": package.get("expected_outputs", ""),
                "must_fail_to_pass": package.get("must_fail_to_pass", ""),
                "blocker_criteria": package.get("blocker_criteria", ""),
                "repair_route": package.get("repair_route", ""),
                "materialized_status": "pending_run337M_review_no_execution",
                "execution_allowed": "false",
                "model_training_allowed": "false",
                "mt5_execution_allowed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_proxy_expected_template(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    proxy_by_key = prior_proxy_map(inputs["prior_proxy"])
    mt5_by_key = prior_mt5_map(inputs["prior_mt5"])
    rows: list[dict[str, Any]] = []
    for package in inputs["proxy_package"]:
        subject = package.get("subject", "")
        for dimension in SUBJECT_DIMENSIONS:
            prior_proxy = proxy_by_key.get((subject, dimension), {})
            prior_mt5 = mt5_by_key.get((subject, dimension), {})
            has_prior = bool(prior_proxy)
            rows.append(
                {
                    "template_id": f"{subject}_{dimension}_proxy_expected_template",
                    "subject": subject,
                    "dimension": dimension,
                    "required_input_identity": package.get("proxy_required_inputs", ""),
                    "required_output_fields": package.get("proxy_required_outputs", ""),
                    "prior_context_proxy_value": prior_proxy.get("proxy_expected_value", ""),
                    "prior_context_mt5_value": prior_mt5.get("mt5_runtime_value", ""),
                    "prior_context_source": rel(RUN337B_PROXY_EXPECTED_CSV) if has_prior else "",
                    "prior_context_use": "signal_sanity_context_only_not_kpi_authority" if has_prior else "none_core56_refresh_required",
                    "current_expected_value_status": "pending_future_proxy_materialization_after_run337M_review",
                    "timestamp_basis_required": prior_proxy.get("timestamp_basis", "closed_bar_cycle_bar_time_required"),
                    "row_level_required": "true",
                    "fresh_mt5_required": "true",
                    "selection_use": "blocked",
                    "forward_decision_use": "blocked",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def build_proxy_source_manifest(proxy_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    subjects = sorted({str(row.get("subject", "")) for row in proxy_rows})
    return {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "subjects": subjects,
        "template_rows": len(proxy_rows),
        "source_context": {
            "prior_proxy_expected": rel(RUN337B_PROXY_EXPECTED_CSV),
            "prior_mt5_observed": rel(RUN337B_MT5_OBSERVED_CSV),
            "prior_difference": rel(RUN337B_PROXY_DIFF_CSV),
            "prior_usability": rel(RUN337B_USABILITY_CSV),
        },
        "source_hashes": {
            "prior_proxy_expected": sha256_file_lf_normalized(RUN337B_PROXY_EXPECTED_CSV),
            "prior_mt5_observed": sha256_file_lf_normalized(RUN337B_MT5_OBSERVED_CSV),
            "prior_difference": sha256_file_lf_normalized(RUN337B_PROXY_DIFF_CSV),
            "prior_usability": sha256_file_lf_normalized(RUN337B_USABILITY_CSV),
        },
        "current_value_status": "templates_only_no_new_proxy_values_no_mt5_execution",
        "allowed_use": "input identity and signal sanity context only",
        "forbidden_use": "KPI authority, Forward decision, candidate selection, runtime authority, Goal Achieve",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_fresh_mt5_handoff_package(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for package in inputs["runtime_package"]:
        subject = package.get("subject", "")
        rows.append(
            {
                "handoff_id": f"{subject}_fresh_mt5_handoff_package",
                "subject": subject,
                "required_files": package.get("required_files", ""),
                "preflight_checks": package.get("preflight_checks", ""),
                "runtime_outputs": package.get("runtime_outputs", ""),
                "comparison_outputs": package.get("comparison_outputs", ""),
                "stress_outputs": package.get("stress_outputs", ""),
                "blocked_if_missing": package.get("blocked_if_missing", ""),
                "runtime_claim_boundary": "runtime_probe_input_only_no_runtime_authority",
                "execution_status": "not_run_in_run337L",
                "external_verification_status": "out_of_scope_by_claim_input_materialization_only",
                "next_review_required": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_mt5_execution_manifest(handoff_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "subjects": [row.get("subject", "") for row in handoff_rows],
        "symbol": "US100",
        "timeframe": "M5",
        "forward_window_start": "2026-04-14",
        "forward_window_end_policy": "latest_available_at_future_execution_preflight",
        "execution_status": "not_run_in_run337L",
        "execution_command_created": False,
        "would_be_future_command": "python stage_pipelines/stage337/attempt_fresh_mt5_runtime_probe_or_block.py --input-run run337M",
        "required_before_execution": [
            "run337M materialized input review",
            "no-lookahead guards accepted",
            "runtime identity preflight accepted",
            "fresh broker data inventory accepted",
            "claim boundary output registry binding accepted",
        ],
        "forbidden": FORBIDDEN,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_mt5_handoff_precheck(handoff_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in handoff_rows:
        subject = str(row.get("subject", ""))
        rows.append(
            {
                "precheck_id": f"{subject}_mt5_handoff_precheck",
                "subject": subject,
                "required_runtime_identity": "EA_hash;include_hash;model_or_surface_spec;adapter_manifest;feature_order;set_file;tester_ini;handoff_snapshot",
                "required_data_identity": "US100_M5_broker_data;latest_timestamp;gap_duplicate_report;timezone;session_contract",
                "required_freeze_identity": "threshold_hash;risk_logic_hash;lot_logic_hash;ATR_SLTP_hash;feature_order_hash",
                "required_outputs": row.get("runtime_outputs", ""),
                "if_missing_status": "blocked_before_mt5_execution",
                "execution_status": "not_run_in_run337L",
                "next_review_required": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_tester_input_manifest(handoff_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "manifest_id": f"{row.get('subject', '')}_tester_input_manifest",
            "subject": row.get("subject", ""),
            "symbol": "US100",
            "timeframe": "M5",
            "date_range_start": "2026-04-14",
            "date_range_end": "latest_available_at_future_execution_preflight",
            "broker_data_requirement": "FPMarkets_US100_M5_broker_data_gap_duplicate_timezone_check_required",
            "tester_mode_requirement": "fresh_MT5_strategy_tester_or_exact_blocker",
            "spread_slippage_requirement": "base_cost_and_predeclared_stress_no_after_result_tuning",
            "feature_freeze_requirement": "closed_bar_only_no_future_or_nearest_join",
            "threshold_lot_freeze_requirement": "threshold_risk_lot_ATR_SLTP_hash_precedes_result_read",
            "execution_status": "not_run_in_run337L",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in handoff_rows
    ]


def build_difference_contract(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    diff_by_subject = {row.get("attempt_name", ""): row for row in inputs["prior_diff"]}
    rows: list[dict[str, Any]] = []
    for package in inputs["proxy_package"]:
        subject = package.get("subject", "")
        prior = diff_by_subject.get(subject, {})
        rows.append(
            {
                "contract_id": f"{subject}_proxy_mt5_difference_contract",
                "subject": subject,
                "comparison_key": "subject;cycle_bar_time;dimension;timestamp_basis;source_row_hash",
                "required_proxy_input": rel(PROXY_EXPECTED_TEMPLATE_CSV),
                "required_mt5_input": rel(FRESH_MT5_HANDOFF_PACKAGE_CSV),
                "required_output": f"{subject}_proxy_mt5_row_level_difference.csv",
                "tolerance_policy": "decision_exact;direction_exact;score_numeric_tolerance_1e-6;aggregate_match_not_enough",
                "prior_context_dimensions_compared": prior.get("dimensions_compared", ""),
                "prior_context_mismatched_dimensions": prior.get("mismatched_dimensions", ""),
                "prior_context_judgment": prior.get("difference_judgment", "not_tested_core56_refresh_required"),
                "current_status": "contract_materialized_pending_fresh_values",
                "selection_use": "blocked",
                "forward_decision_use": "blocked",
                "runtime_authority_use": "blocked",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_usability_contract(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    prior_by_subject = {row.get("subject", ""): row for row in inputs["prior_usability"]}
    rows: list[dict[str, Any]] = []
    for package in inputs["proxy_package"]:
        subject = package.get("subject", "")
        prior = prior_by_subject.get(subject, {})
        rows.append(
            {
                "contract_id": f"{subject}_usability_decision_contract",
                "subject": subject,
                "required_inputs": f"{rel(PROXY_EXPECTED_TEMPLATE_CSV)};{rel(FRESH_MT5_HANDOFF_PACKAGE_CSV)};{rel(DIFFERENCE_CONTRACT_CSV)}",
                "usable_condition": "fresh_mt5_report_exists;trade_ledger_exists;row_level_difference_review_passes;cost_curve_regime_extractors_pass;claim_boundary_passes",
                "not_usable_condition": "missing_runtime_output;row_level_mismatch;aggregate_only_match;feature_handoff_gap;cost_curve_fragility;core56_asof_gap",
                "prior_usability_label": prior.get("usability_label", "not_usable_until_core56_refresh_and_mt5_probe"),
                "allowed_use": "signal sanity and runtime handoff debugging after review",
                "forbidden_use": "KPI authority, Forward Passed/Failed, candidate selection, operating reference, runtime authority",
                "current_status": "contract_materialized_pending_run337M_review",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_core56_package(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "package_id": row.get("package_id", ""),
            "step_order": row.get("step_order", ""),
            "source_protocol_id": row.get("source_protocol_id", ""),
            "required_artifacts": row.get("required_artifacts", ""),
            "asof_guard": row.get("asof_guard", ""),
            "blocked_claims": row.get("blocked_claims", ""),
            "expected_outputs": row.get("expected_outputs", ""),
            "current_status": "source_handoff_package_materialized_pending_run337M_review",
            "execution_allowed": "false",
            "training_allowed": "false",
            "mt5_execution_allowed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in inputs["core56_package"]
    ]


def build_cost_curve_package(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "package_id": row.get("package_id", ""),
            "source_protocol_id": row.get("source_protocol_id", ""),
            "gate_scope": row.get("gate_scope", ""),
            "required_extractors": row.get("required_extractors", ""),
            "required_outputs": row.get("required_outputs", ""),
            "minimum_metrics": row.get("minimum_metrics", ""),
            "failure_memory_trigger": row.get("failure_memory_trigger", ""),
            "current_status": "extractor_package_materialized_pending_run337M_review",
            "execution_allowed": "false",
            "training_allowed": "false",
            "mt5_execution_allowed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in inputs["cost_package"]
    ]


def build_regime_inventory(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "package_id": row.get("package_id", ""),
            "source_protocol_id": row.get("source_protocol_id", ""),
            "regime_source": row.get("regime_source", ""),
            "required_source_identity": row.get("required_source_identity", ""),
            "asof_join_rule": row.get("asof_join_rule", ""),
            "required_checks": row.get("required_checks", ""),
            "slice_outputs": row.get("slice_outputs", ""),
            "expected_outputs": row.get("expected_outputs", ""),
            "current_status": "source_inventory_materialized_pending_run337M_review",
            "selection_filter_use": "blocked",
            "forward_filter_use": "blocked",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in inputs["regime_package"]
    ]


def build_runtime_identity_preflight(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for package in inputs["runtime_package"]:
        subject = package.get("subject", "")
        rows.append(
            {
                "preflight_id": f"{subject}_runtime_identity_preflight",
                "subject": subject,
                "required_files": package.get("required_files", ""),
                "preflight_checks": package.get("preflight_checks", ""),
                "required_runtime_outputs": package.get("runtime_outputs", ""),
                "required_comparison_outputs": package.get("comparison_outputs", ""),
                "required_stress_outputs": package.get("stress_outputs", ""),
                "runtime_claim_boundary": "runtime_probe_input_only_no_runtime_authority",
                "current_status": "materialized_pending_run337M_review",
                "execution_allowed": "false",
                "mt5_execution_allowed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    rows.append(
        {
            "preflight_id": "package_index_runtime_binding",
            "subject": "package_index",
            "required_files": rel(PACKAGE_INDEX_CSV),
            "preflight_checks": "package_index;acceptance_matrix;blocker_matrix;run337K_decision;run337K_manifest",
            "required_runtime_outputs": "output_registry_binding;hash_receipt;run_manifest",
            "required_comparison_outputs": "review_queue_binding",
            "required_stress_outputs": "not_applicable",
            "runtime_claim_boundary": "package_index_only_no_runtime_authority",
            "current_status": "materialized_pending_run337M_review",
            "execution_allowed": "false",
            "mt5_execution_allowed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )
    return rows


def build_claim_output_registry_binding(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in inputs["claim_package"]:
        rows.append(
            {
                "blocker_id": row.get("blocker_id", ""),
                "blocked_condition": row.get("blocked_condition", ""),
                "required_response": row.get("required_response", ""),
                "claim_status": "not_claimed",
                "output_binding_required": "true",
                "execution_allowed": "false",
                "training_allowed": "false",
                "mt5_execution_allowed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_run337m_queue() -> list[dict[str, Any]]:
    items = [
        ("review_no_lookahead_pre_execution_guards", rel(NO_LOOKAHEAD_GUARDS_CSV), "no_lookahead"),
        ("review_proxy_expected_template_and_source_identity", f"{rel(PROXY_EXPECTED_TEMPLATE_CSV)};{rel(PROXY_SOURCE_MANIFEST_JSON)}", "proxy_mt5"),
        ("review_fresh_mt5_handoff_package", f"{rel(FRESH_MT5_HANDOFF_PACKAGE_CSV)};{rel(MT5_EXECUTION_MANIFEST_JSON)};{rel(MT5_HANDOFF_PREFLIGHT_CSV)};{rel(MT5_TESTER_INPUT_MANIFEST_CSV)}", "runtime"),
        ("review_proxy_mt5_difference_usability_contract", f"{rel(DIFFERENCE_CONTRACT_CSV)};{rel(USABILITY_CONTRACT_CSV)}", "proxy_mt5"),
        ("review_core56_asof_source_handoff_package", rel(CORE56_HANDOFF_PACKAGE_CSV), "core56"),
        ("review_cost_direction_curve_extractor_package", rel(COST_CURVE_EXTRACTOR_PACKAGE_CSV), "cost_curve"),
        ("review_regime_asof_source_inventory", rel(REGIME_SOURCE_INVENTORY_CSV), "regime"),
        ("review_runtime_identity_preflight_package", rel(RUNTIME_IDENTITY_PREFLIGHT_CSV), "runtime"),
        ("review_claim_boundary_output_registry_binding", rel(CLAIM_OUTPUT_REGISTRY_BINDING_CSV), "claim_boundary"),
    ]
    return [
        {
            "queue_id": queue_id,
            "priority": index,
            "package_family": family,
            "required_inputs": inputs,
            "review_task": "verify materialized inputs, source identity, no-lookahead guard, runtime parity boundary, and claim boundary",
            "required_decision": "accept_for_future_mt5_attempt_or_route_repair_gap",
            "forbidden": "model training, MT5 execution, threshold retune, lot optimization, forward-pocket filtering, candidate selection, Forward Passed, runtime authority, Goal Achieve",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for index, (queue_id, inputs, family) in enumerate(items, start=1)
    ]


def build_gate_audit(
    source_lineage: Sequence[Mapping[str, Any]],
    no_lookahead: Sequence[Mapping[str, Any]],
    proxy_template: Sequence[Mapping[str, Any]],
    handoff: Sequence[Mapping[str, Any]],
    difference: Sequence[Mapping[str, Any]],
    usability: Sequence[Mapping[str, Any]],
    core56: Sequence[Mapping[str, Any]],
    cost_curve: Sequence[Mapping[str, Any]],
    regime: Sequence[Mapping[str, Any]],
    runtime: Sequence[Mapping[str, Any]],
    claim_binding: Sequence[Mapping[str, Any]],
    queue: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    return [
        {"gate_id": "source_lineage_connected", "status": "pass" if all(row.get("exists") is True for row in source_lineage) else "fail", "evidence": rel(SOURCE_LINEAGE_CSV), "finding": f"source_rows={len(source_lineage)}", "claim_boundary": CLAIM_BOUNDARY},
        {"gate_id": "parent_run337K_completed", "status": "pass", "evidence": rel(RUN337K_DECISION_JSON), "finding": "run337K accepted run337L materialization", "claim_boundary": CLAIM_BOUNDARY},
        {"gate_id": "no_lookahead_guards_materialized", "status": "pass" if len(no_lookahead) == 5 else "fail", "evidence": rel(NO_LOOKAHEAD_GUARDS_CSV), "finding": f"guard_rows={len(no_lookahead)}", "claim_boundary": CLAIM_BOUNDARY},
        {"gate_id": "proxy_expected_templates_materialized", "status": "pass" if len(proxy_template) == 25 else "fail", "evidence": rel(PROXY_EXPECTED_TEMPLATE_CSV), "finding": f"proxy_template_rows={len(proxy_template)}", "claim_boundary": CLAIM_BOUNDARY},
        {"gate_id": "fresh_mt5_handoff_materialized", "status": "pass" if len(handoff) == 5 else "fail", "evidence": rel(FRESH_MT5_HANDOFF_PACKAGE_CSV), "finding": f"handoff_rows={len(handoff)};mt5_execution=not_run", "claim_boundary": CLAIM_BOUNDARY},
        {"gate_id": "difference_usability_contracts_materialized", "status": "pass" if len(difference) == 5 and len(usability) == 5 else "fail", "evidence": f"{rel(DIFFERENCE_CONTRACT_CSV)};{rel(USABILITY_CONTRACT_CSV)}", "finding": f"difference_rows={len(difference)};usability_rows={len(usability)}", "claim_boundary": CLAIM_BOUNDARY},
        {"gate_id": "core56_asof_handoff_materialized", "status": "pass" if len(core56) == 5 else "fail", "evidence": rel(CORE56_HANDOFF_PACKAGE_CSV), "finding": f"core56_rows={len(core56)}", "claim_boundary": CLAIM_BOUNDARY},
        {"gate_id": "cost_curve_extractor_materialized", "status": "pass" if len(cost_curve) == 5 else "fail", "evidence": rel(COST_CURVE_EXTRACTOR_PACKAGE_CSV), "finding": f"cost_curve_rows={len(cost_curve)}", "claim_boundary": CLAIM_BOUNDARY},
        {"gate_id": "regime_asof_inventory_materialized", "status": "pass" if len(regime) == 6 else "fail", "evidence": rel(REGIME_SOURCE_INVENTORY_CSV), "finding": f"regime_rows={len(regime)}", "claim_boundary": CLAIM_BOUNDARY},
        {"gate_id": "runtime_identity_preflight_materialized", "status": "pass" if len(runtime) == 6 else "fail", "evidence": rel(RUNTIME_IDENTITY_PREFLIGHT_CSV), "finding": f"runtime_preflight_rows={len(runtime)}", "claim_boundary": CLAIM_BOUNDARY},
        {"gate_id": "claim_output_registry_binding_materialized", "status": "pass" if len(claim_binding) == 11 else "fail", "evidence": rel(CLAIM_OUTPUT_REGISTRY_BINDING_CSV), "finding": f"claim_binding_rows={len(claim_binding)}", "claim_boundary": CLAIM_BOUNDARY},
        {"gate_id": "run337M_review_queue_ready", "status": "pass" if len(queue) == 9 else "fail", "evidence": rel(RUN337M_QUEUE_CSV), "finding": f"run337M_queue_rows={len(queue)}", "claim_boundary": CLAIM_BOUNDARY},
        {"gate_id": "final_claim_guard", "status": "pass", "evidence": rel(FINAL_DECISION_JSON), "finding": "no model training, no MT5 execution, no Forward decision, no runtime authority, no Goal Achieve", "claim_boundary": CLAIM_BOUNDARY},
    ]


def build_metrics(**tables: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    audit = tables["audit"]
    proxy_rows = tables["proxy_template"]
    subject_counts = Counter(str(row.get("subject", "")) for row in proxy_rows)
    return {
        "source_lineage_rows": len(tables["source_lineage"]),
        "no_lookahead_guard_rows": len(tables["no_lookahead"]),
        "proxy_expected_template_rows": len(proxy_rows),
        "fresh_mt5_handoff_rows": len(tables["handoff"]),
        "mt5_handoff_precheck_rows": len(tables["mt5_precheck"]),
        "tester_input_manifest_rows": len(tables["tester_manifest"]),
        "difference_contract_rows": len(tables["difference"]),
        "usability_contract_rows": len(tables["usability"]),
        "core56_handoff_rows": len(tables["core56"]),
        "cost_curve_extractor_rows": len(tables["cost_curve"]),
        "regime_inventory_rows": len(tables["regime"]),
        "runtime_identity_preflight_rows": len(tables["runtime"]),
        "claim_binding_rows": len(tables["claim_binding"]),
        "run337m_queue_rows": len(tables["queue"]),
        "gate_rows": len(audit),
        "failed_gate_rows": len([row for row in audit if row.get("status") != "pass"]),
        "proxy_subject_counts": dict(sorted(subject_counts.items())),
    }


def write_receipts(metrics: Mapping[str, Any]) -> list[Path]:
    return [
        write_json(
            EXPERIMENT_DESIGN_JSON,
            {
                "run_id": RUN_ID,
                "hypothesis": "proxy expected and fresh MT5 probe inputs can be materialized with no execution and no after-result tuning",
                "decision_use": "open run337M review queue before any future MT5 runtime attempt",
                "control_variables": "no model training, no MT5 execution, no threshold retune, no lot optimization, no forward-pocket filtering, no candidate selection",
                "changed_variables": "input templates, handoff package, difference/usability contract, runtime preflight, review queue",
                "success_criteria": "all input packages materialized, run337M queue ready, failed gates zero",
                "invalid_conditions": "using templates or prior context values as KPI authority, Forward Passed/Failed, runtime authority, or Goal Achieve",
                "metrics": metrics,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            DATA_INTEGRITY_JSON,
            {
                "run_id": RUN_ID,
                "data_source": "run337K accepted scaffold queue, run337J scaffolds, run337H package specs, and run337B prior proxy/MT5 context",
                "time_axis": "future runtime must use closed US100 M5 cycle_bar_time; prior Stage337B context used timestamp-aligned feature rows intersecting MT5 cycle rows",
                "sample_scope": "input materialization only; no new broker bars and no trade rows consumed",
                "missing_or_duplicate_check": "deferred to future broker-data preflight; this run checks source artifact presence and row counts",
                "feature_label_boundary": "proxy templates and no-lookahead guards block future-bar, forward-pocket, threshold, and lot after-result shortcuts",
                "split_boundary": "post-2026-04-14 forward probe remains future execution; no training or WFO split changes in run337L",
                "leakage_risk": "after-result pocket filtering, stale core56 as-of join, proxy-only selection, aggregate-only proxy-MT5 match",
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
                "runtime_path": rel(FRESH_MT5_HANDOFF_PACKAGE_CSV),
                "shared_contract": "feature order, model/ONNX spec, adapter manifest, threshold, risk, lot, ATR SL/TP, symbol/timeframe, broker session, timestamp basis, tester output, telemetry, trade ledger, proxy expected, row-level difference, and usability decision",
                "known_differences": "run337L creates input packages only; no Strategy Tester output, terminal log, trade ledger, or row-level fresh comparison exists",
                "parity_check": "runtime identity preflight and difference contract materialized for run337M review",
                "parity_identity": rel(RUNTIME_IDENTITY_PREFLIGHT_CSV),
                "runtime_claim_boundary": "input_materialization_only_no_runtime_authority",
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
                    rel(PROXY_EXPECTED_TEMPLATE_CSV),
                    rel(FRESH_MT5_HANDOFF_PACKAGE_CSV),
                    rel(DIFFERENCE_CONTRACT_CSV),
                    rel(USABILITY_CONTRACT_CSV),
                    rel(RUN337M_QUEUE_CSV),
                    rel(FINAL_DECISION_JSON),
                ],
                "artifact_hashes": "registered in artifact_registry after run",
                "registry_links": "run_registry;alpha_run_ledger;stage_run_ledger;artifact_registry",
                "availability": "tracked after commit; reproducible from run337L script",
                "lineage_judgment": "connected_with_boundary",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RESULT_JUDGMENT_JSON,
            {
                "run_id": RUN_ID,
                "result_subject": "proxy expected and fresh MT5 probe input materialization",
                "evidence_available": "input templates, runtime handoff package, difference/usability contracts, runtime identity preflight, claim-boundary binding, gate audit",
                "evidence_missing": "fresh MT5 runtime result, Strategy Tester report, terminal log, trade ledger, row-level fresh comparison, KPI usability review",
                "judgment_label": "exploratory",
                "claim_boundary": "inputs are materialized for review only; no candidate, Forward decision, runtime authority, live readiness, or Goal Achieve",
                "next_condition": NEXT_RUN_ID,
                "user_explanation_hook": "이번 실행은 비교에 필요한 입력 묶음을 만든 것이며, 실제 MT5 결과와 활용성 판정은 다음 검토와 실행 이후에만 말할 수 있다.",
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
# run337L Proxy Expected Fresh MT5 Probe Inputs(337L 프록시 예상값/신규 MT5 탐침 입력)

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

## Materialized Inputs(물질화 입력)

- proxy_expected_template_rows(프록시 예상값 템플릿 행): `{metrics['proxy_expected_template_rows']}`
- fresh_mt5_handoff_rows(신규 MT5 인계 행): `{metrics['fresh_mt5_handoff_rows']}`
- difference_contract_rows(차이 계약 행): `{metrics['difference_contract_rows']}`
- usability_contract_rows(활용성 계약 행): `{metrics['usability_contract_rows']}`
- cost_curve_extractor_rows(비용/곡선 추출 행): `{metrics['cost_curve_extractor_rows']}`
- regime_inventory_rows(국면 원천 목록 행): `{metrics['regime_inventory_rows']}`
- run337M_queue_rows(337M 대기열 행): `{metrics['run337m_queue_rows']}`
- gate_rows(게이트 행): `{metrics['gate_rows']}`, failed(실패): `{metrics['failed_gate_rows']}`

Action(행동): proxy expected template(프록시 예상값 템플릿), fresh MT5 probe handoff package(신규 메타트레이더5 탐침 인계 패키지), row-level difference contract(행 단위 차이 계약), usability decision contract(활용성 판정 계약)를 만들었다.

Effect(효과): run337M(337M 실행)에서 이 입력 묶음을 검토할 수 있다. 이번 실행은 MT5 execution(MT5 실행), model training(모델 학습), candidate selection(후보 선택), Forward decision(전진 판정)을 열지 않았다.
"""
    decision = f"""
# 2026-05-27 Stage337L Decision(337L 결정)

- decision(결정): `{DECISION}`
- status(상태): `{STATUS}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- selected_candidate(선택 후보): `none`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`

Action(행동): run337L(337L 실행)는 run337K(337K 실행)가 승인한 9개 입력 물질화 작업을 산출물로 만들었다.

Effect(효과): 다음 단계는 run337M(337M 실행) 검토다. 실제 fresh MT5 runtime probe(신규 메타트레이더5 런타임 탐침) 실행과 KPI(핵심 성과 지표) 활용성 판정은 아직 없다.
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
- effect(효과): run337L(337L 실행)는 proxy expected/fresh MT5 input materialization(프록시 예상값/신규 메타트레이더5 입력 물질화)을 완료하고 run337M(337M 실행) 검토 대기열로 넘겼다. 아직 선택 후보는 없다.
"""
    artifacts.append(write_md(SELECTED_DIR / "selection_status.md", selection))

    brief_text, brief_bom = read_text_lossless(SPEC_DIR / "stage_brief.md")
    brief_text = replace_prefix_line(brief_text, "- latest_run(최신 실행):", f"- latest_run(최신 실행): `{RUN_ID}`")
    brief_text = insert_after_marker_once(
        brief_text,
        "- run337K_summary(337K 요약):",
        f"- run337L_summary(337L 요약): `{STATUS}`. Effect(효과): proxy expected template(프록시 예상값 템플릿) `{metrics['proxy_expected_template_rows']}`행, fresh MT5 handoff(신규 메타트레이더5 인계) `{metrics['fresh_mt5_handoff_rows']}`행, run337M review queue(337M 검토 대기열) `{metrics['run337m_queue_rows']}`행을 만들었다.",
        "run337L_summary(337L 요약)",
    )
    artifacts.append(write_text_lossless(SPEC_DIR / "stage_brief.md", brief_text, brief_bom))

    input_section = f"""
- proxy_expected_template(프록시 예상값 템플릿): `{rel(PROXY_EXPECTED_TEMPLATE_CSV)}`
- proxy_source_manifest(프록시 원천 목록): `{rel(PROXY_SOURCE_MANIFEST_JSON)}`
- fresh_mt5_handoff_package(신규 MT5 인계 패키지): `{rel(FRESH_MT5_HANDOFF_PACKAGE_CSV)}`
- difference_contract(차이 계약): `{rel(DIFFERENCE_CONTRACT_CSV)}`
- usability_contract(활용성 계약): `{rel(USABILITY_CONTRACT_CSV)}`
- runtime_identity_preflight(런타임 정체성 사전점검): `{rel(RUNTIME_IDENTITY_PREFLIGHT_CSV)}`
- run337M_queue(337M 대기열): `{rel(RUN337M_QUEUE_CSV)}`

Effect(효과): 다음 실행은 입력 묶음이 실제 fresh MT5 runtime probe(신규 메타트레이더5 런타임 탐침) 시도로 넘어가도 되는지 검토한다.
"""
    artifacts.append(append_section_once(INPUTS_DIR / "input_refs.md", "## run337L Outputs(337L 산출물)", input_section))

    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_prefix_line(workspace_text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    focus = (
        "- >-\n"
        f"  Stage337 run337L focus complete: Stage337(337단계) run337L(337L 실행)는 `{STATUS}`로 proxy expected/fresh MT5 input materialization(프록시 예상값/신규 메타트레이더5 입력 물질화)을 완료했다. "
        "Effect(효과): run337M(337M 실행) 검토 대기열을 열었지만 model training(모델 학습), MT5 execution(MT5 실행), candidate selection(후보 선택)은 아직 닫아둔다.\n"
    )
    workspace_text = insert_focus_once(workspace_text, focus, "Stage337 run337L focus complete")
    artifacts.append(write_text_lossless(WORKSPACE_STATE, workspace_text, workspace_bom))

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    replacements = {
        "- current_run(현재 실행):": f"- current_run(현재 실행): `{NEXT_RUN_ID}`",
        "- status(상태):": f"- status(상태): `{STATUS}`",
        "- decision(결정):": f"- decision(결정): `{DECISION}`",
        "- next_action(다음 행동):": f"- next_action(다음 행동): `{NEXT_RUN_ID}`",
    }
    for prefix, new_line in replacements.items():
        current_text = replace_prefix_line(current_text, prefix, new_line)
    summary = (
        f"- run337L_summary(337L 요약): `{STATUS}`. "
        "Effect(효과): proxy expected/fresh MT5 input package(프록시 예상값/신규 메타트레이더5 입력 패키지)를 만들고 run337M(337M 실행) 검토로 넘기며, MT5 실행/학습/후보 선택은 계속 닫아둔다."
    )
    current_text = insert_after_marker_once(current_text, "- run337K_summary(337K 요약):", summary, "run337L_summary(337L 요약)")
    artifacts.append(write_text_lossless(CURRENT_STATE, current_text, current_bom))

    artifacts.append(
        append_section_once(
            CHANGELOG,
            "## Stage337L Proxy MT5 Input Materialization(337L 프록시-MT5 입력 물질화)",
            f"""
- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- action(행동): proxy expected template(프록시 예상값 템플릿), fresh MT5 handoff package(신규 메타트레이더5 인계 패키지), difference/usability contract(차이/활용성 계약)를 만들었다.
- effect(효과): run337M(337M 실행) 검토 대기열 `{metrics['run337m_queue_rows']}`행을 열었고, MT5 execution(MT5 실행), Forward decision(전진 판정), runtime authority(런타임 권위)는 주장하지 않는다.
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
                "lane": "proxy_mt5_input_materialization",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_DOC),
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};training_not_allowed;mt5_not_executed;goal_achieve_not_claimed.",
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__proxy_mt5_input_materialization",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "proxy_mt5_input_materialization",
                "tier_scope": "stage337_package_boundary_macro48_u42_core56",
                "kpi_scope": "input_materialization_only_no_new_candidate_kpi",
                "scoreboard_lane": "runtime_parity_readiness",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_DOC),
                "primary_kpi": "proxy_expected_template_rows=25;fresh_mt5_handoff_rows=5;run337m_queue_rows=9",
                "guardrail_kpi": "training_not_allowed;mt5_not_executed;runtime_authority_not_claimed;goal_achieve_not_claimed",
                "external_verification_status": "out_of_scope_by_claim_input_materialization_only",
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
                "ledger_row_id": f"{RUN_ID}__proxy_mt5_input_materialization",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "work_family": "runtime_parity_input_materialization",
                "evidence_scope": "run337K_accepted_scaffolds_to_run337M_review_queue",
                "kpi_scope": "input_materialization_only_no_new_candidate_kpi",
                "status": STATUS,
                "judgment": JUDGMENT,
                "claim_boundary": CLAIM_BOUNDARY,
                "path": rel(REPORT_DOC),
                "notes": f"next_action={NEXT_RUN_ID};proxy_mt5_inputs_materialized;mt5_not_executed;goal_achieve_not_claimed.",
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
            "notes": "run337L_proxy_mt5_input_materialization_no_execution_no_selection",
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
    no_lookahead = build_no_lookahead_guards(inputs)
    proxy_template = build_proxy_expected_template(inputs)
    proxy_manifest = build_proxy_source_manifest(proxy_template)
    handoff = build_fresh_mt5_handoff_package(inputs)
    mt5_manifest = build_mt5_execution_manifest(handoff)
    mt5_precheck = build_mt5_handoff_precheck(handoff)
    tester_manifest = build_tester_input_manifest(handoff)
    difference = build_difference_contract(inputs)
    usability = build_usability_contract(inputs)
    core56 = build_core56_package(inputs)
    cost_curve = build_cost_curve_package(inputs)
    regime = build_regime_inventory(inputs)
    runtime = build_runtime_identity_preflight(inputs)
    claim_binding = build_claim_output_registry_binding(inputs)
    queue = build_run337m_queue()
    audit = build_gate_audit(source_lineage, no_lookahead, proxy_template, handoff, difference, usability, core56, cost_curve, regime, runtime, claim_binding, queue)
    metrics = build_metrics(
        source_lineage=source_lineage,
        no_lookahead=no_lookahead,
        proxy_template=proxy_template,
        handoff=handoff,
        mt5_precheck=mt5_precheck,
        tester_manifest=tester_manifest,
        difference=difference,
        usability=usability,
        core56=core56,
        cost_curve=cost_curve,
        regime=regime,
        runtime=runtime,
        claim_binding=claim_binding,
        queue=queue,
        audit=audit,
    )
    failed_gates = [row for row in audit if row.get("status") != "pass"]

    run_artifacts = [
        write_csv(SOURCE_LINEAGE_CSV, ("source_path", "exists", "sha256", "role", "consumer", "availability", "lineage_judgment", "claim_boundary"), source_lineage),
        write_csv(NO_LOOKAHEAD_GUARDS_CSV, ("guard_id", "package_id", "required_inputs", "expected_outputs", "must_fail_to_pass", "blocker_criteria", "repair_route", "materialized_status", "execution_allowed", "model_training_allowed", "mt5_execution_allowed", "claim_boundary"), no_lookahead),
        write_csv(PROXY_EXPECTED_TEMPLATE_CSV, ("template_id", "subject", "dimension", "required_input_identity", "required_output_fields", "prior_context_proxy_value", "prior_context_mt5_value", "prior_context_source", "prior_context_use", "current_expected_value_status", "timestamp_basis_required", "row_level_required", "fresh_mt5_required", "selection_use", "forward_decision_use", "claim_boundary"), proxy_template),
        write_json(PROXY_SOURCE_MANIFEST_JSON, proxy_manifest),
        write_csv(FRESH_MT5_HANDOFF_PACKAGE_CSV, ("handoff_id", "subject", "required_files", "preflight_checks", "runtime_outputs", "comparison_outputs", "stress_outputs", "blocked_if_missing", "runtime_claim_boundary", "execution_status", "external_verification_status", "next_review_required", "claim_boundary"), handoff),
        write_json(MT5_EXECUTION_MANIFEST_JSON, mt5_manifest),
        write_csv(MT5_HANDOFF_PREFLIGHT_CSV, ("precheck_id", "subject", "required_runtime_identity", "required_data_identity", "required_freeze_identity", "required_outputs", "if_missing_status", "execution_status", "next_review_required", "claim_boundary"), mt5_precheck),
        write_csv(MT5_TESTER_INPUT_MANIFEST_CSV, ("manifest_id", "subject", "symbol", "timeframe", "date_range_start", "date_range_end", "broker_data_requirement", "tester_mode_requirement", "spread_slippage_requirement", "feature_freeze_requirement", "threshold_lot_freeze_requirement", "execution_status", "claim_boundary"), tester_manifest),
        write_csv(DIFFERENCE_CONTRACT_CSV, ("contract_id", "subject", "comparison_key", "required_proxy_input", "required_mt5_input", "required_output", "tolerance_policy", "prior_context_dimensions_compared", "prior_context_mismatched_dimensions", "prior_context_judgment", "current_status", "selection_use", "forward_decision_use", "runtime_authority_use", "claim_boundary"), difference),
        write_csv(USABILITY_CONTRACT_CSV, ("contract_id", "subject", "required_inputs", "usable_condition", "not_usable_condition", "prior_usability_label", "allowed_use", "forbidden_use", "current_status", "claim_boundary"), usability),
        write_csv(CORE56_HANDOFF_PACKAGE_CSV, ("package_id", "step_order", "source_protocol_id", "required_artifacts", "asof_guard", "blocked_claims", "expected_outputs", "current_status", "execution_allowed", "training_allowed", "mt5_execution_allowed", "claim_boundary"), core56),
        write_csv(COST_CURVE_EXTRACTOR_PACKAGE_CSV, ("package_id", "source_protocol_id", "gate_scope", "required_extractors", "required_outputs", "minimum_metrics", "failure_memory_trigger", "current_status", "execution_allowed", "training_allowed", "mt5_execution_allowed", "claim_boundary"), cost_curve),
        write_csv(REGIME_SOURCE_INVENTORY_CSV, ("package_id", "source_protocol_id", "regime_source", "required_source_identity", "asof_join_rule", "required_checks", "slice_outputs", "expected_outputs", "current_status", "selection_filter_use", "forward_filter_use", "claim_boundary"), regime),
        write_csv(RUNTIME_IDENTITY_PREFLIGHT_CSV, ("preflight_id", "subject", "required_files", "preflight_checks", "required_runtime_outputs", "required_comparison_outputs", "required_stress_outputs", "runtime_claim_boundary", "current_status", "execution_allowed", "mt5_execution_allowed", "claim_boundary"), runtime),
        write_csv(CLAIM_OUTPUT_REGISTRY_BINDING_CSV, ("blocker_id", "blocked_condition", "required_response", "claim_status", "output_binding_required", "execution_allowed", "training_allowed", "mt5_execution_allowed", "claim_boundary"), claim_binding),
        write_csv(RUN337M_QUEUE_CSV, ("queue_id", "priority", "package_family", "required_inputs", "review_task", "required_decision", "forbidden", "claim_boundary"), queue),
        write_csv(GATE_AUDIT_CSV, ("gate_id", "status", "evidence", "finding", "claim_boundary"), audit),
        write_csv(
            RESULT_JUDGMENT_CSV,
            ("result_subject", "evidence_available", "evidence_missing", "judgment_label", "claim_boundary", "next_condition"),
            [
                {
                    "result_subject": "run337L proxy expected fresh MT5 input materialization",
                    "evidence_available": f"{rel(PROXY_EXPECTED_TEMPLATE_CSV)};{rel(FRESH_MT5_HANDOFF_PACKAGE_CSV)};{rel(DIFFERENCE_CONTRACT_CSV)};{rel(USABILITY_CONTRACT_CSV)};{rel(RUN337M_QUEUE_CSV)}",
                    "evidence_missing": "fresh MT5 runtime result;Strategy Tester report;terminal log;trade ledger;row-level fresh comparison;KPI usability review",
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
        "status": STATUS if not failed_gates else "blocked_stage337L_input_materialization_gate_failure",
        "judgment": JUDGMENT if not failed_gates else "stage337L_input_materialization_requires_repair",
        "decision": DECISION if not failed_gates else "stage337L_input_materialization_blocked_gate_failure",
        "metrics": metrics,
        "failed_gates": failed_gates,
        "next_action": NEXT_RUN_ID if not failed_gates else "repair_run337L_inputs_before_review",
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
                "status": "blocked_stage337L_input_materialization_gate_failure",
                "decision": "stage337L_input_materialization_blocked_gate_failure",
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
        "external_verification_status": "out_of_scope_by_claim_input_materialization_only_no_mt5_execution",
        "next_action": NEXT_RUN_ID,
        "model_training": "not_run",
        "mt5_execution": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed_for_stage337_new_work",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
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
                "proxy_expected_template_rows": metrics["proxy_expected_template_rows"],
                "fresh_mt5_handoff_rows": metrics["fresh_mt5_handoff_rows"],
                "run337M_queue_rows": metrics["run337m_queue_rows"],
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
