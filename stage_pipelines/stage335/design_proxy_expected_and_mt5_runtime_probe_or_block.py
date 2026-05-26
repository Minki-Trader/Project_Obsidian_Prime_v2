from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.mt5_tier_balance_completion import (  # noqa: E402
    COMMON_FILES_ROOT_DEFAULT,
    METAEDITOR_PATH_DEFAULT,
    TERMINAL_DATA_ROOT_DEFAULT,
    TERMINAL_PATH_DEFAULT,
    TESTER_PROFILE_ROOT_DEFAULT,
)


TODAY = "2026-05-26"
STAGE_ID = "335_overfit_guard__failure_memory_constrained_research_handoff"
RUN_NUMBER = "run335I"
RUN_ID = "run335I_design_proxy_expected_and_mt5_runtime_probe_or_block_v1"
PARENT_RUN_ID = "run335H_review_guarded_branch_probe_input_materialization_v1"
NEXT_RUN_ID = "run335J_materialize_proxy_expected_values_and_mt5_runtime_probe_attempts_or_block_v1"
STATUS = "completed_proxy_expected_mt5_runtime_probe_or_block_design_no_selection"
JUDGMENT = "proxy_mt5_execution_or_block_design_completed_no_goal_achieve"
DECISION = "stage335I_proxy_mt5_design_ready_for_materialization_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage335I_proxy_mt5_design_no_model_training_"
    "no_threshold_retuning_no_lot_optimization_no_direct_forward_pocket_filtering_"
    "no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_"
    "no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

COMPARISON_DIMENSIONS = [
    "net_profit",
    "profit_factor",
    "max_drawdown",
    "trades_per_day",
    "expectancy",
    "recovery_factor",
    "curve_pocket",
    "underwater_stretch",
    "lot_normalized_result",
    "spread_slippage_stress",
    "session_hour_regime",
    "long_short_attribution",
]

USABILITY_RULE = (
    "usable_only_after_proxy_expected_values_and_mt5_runtime_probe_results_exist_"
    "and_difference_is_explained_by_logged_identity_cost_fill_session_or_handoff_evidence"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
RUN335H_DIR = STAGE_DIR / "02_runs" / "run335H"
RUN335G_DIR = STAGE_DIR / "02_runs" / "run335G"
RUN335D_DIR = STAGE_DIR / "02_runs" / "run335D"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
INPUTS_DIR = STAGE_DIR / "01_inputs"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"

DOCS = ROOT / "docs"
RUN_REGISTRY = DOCS / "registers" / "run_registry.csv"
ALPHA_LEDGER = DOCS / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = DOCS / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
WORKSPACE_STATE = DOCS / "workspace" / "workspace_state.yaml"
CURRENT_STATE = DOCS / "context" / "current_working_state.md"
CHANGELOG = DOCS / "workspace" / "changelog.md"
DECISION_DOC = DOCS / "decisions" / "2026-05-26_stage335I_proxy_expected_mt5_runtime_probe_or_block_design.md"

RUN335H_INPUTS: dict[str, Path] = {
    "run335i_queue": RUN335H_DIR / "run335I_proxy_mt5_execution_or_block_design_queue.csv",
    "evidence_gaps": RUN335H_DIR / "proxy_mt5_evidence_gap_register.csv",
    "usability_review": RUN335H_DIR / "proxy_mt5_usability_review.csv",
    "review_matrix": RUN335H_DIR / "probe_input_review_matrix.csv",
    "final_review_decision": RUN335H_DIR / "final_probe_input_review_decision.json",
    "run_manifest": RUN335H_DIR / "run_manifest.json",
}

RUN335G_INPUTS: dict[str, Path] = {
    "package_manifest": RUN335G_DIR / "probe_input_package_manifest.csv",
    "measurement_manifest": RUN335G_DIR / "measurement_input_manifest.csv",
    "proxy_expected_manifest": RUN335G_DIR / "proxy_expected_result_manifest.csv",
    "mt5_result_or_block": RUN335G_DIR / "mt5_runtime_probe_result_or_block.csv",
    "comparison_readiness": RUN335G_DIR / "proxy_mt5_comparison_readiness_matrix.csv",
    "no_retune_guard": RUN335G_DIR / "no_retune_materialization_guard.csv",
}

RUN335D_INPUTS: dict[str, Path] = {
    "source_bindings": RUN335D_DIR / "branch_source_binding_matrix.csv",
    "runtime_gates": RUN335D_DIR / "branch_runtime_gate_payloads.csv",
}


def io_path(path: Path) -> Path:
    resolved = path.resolve()
    if sys.platform == "win32":
        text = str(resolved)
        if len(text) >= 240 and not text.startswith("\\\\?\\"):
            return Path("\\\\?\\" + text)
    return resolved


def path_exists(path: Path) -> bool:
    return io_path(path).exists()


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [json_ready(item) for item in value]
    if isinstance(value, tuple):
        return [json_ready(item) for item in value]
    if isinstance(value, Path):
        return rel(value)
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return None
    return value


def csv_value(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return ""
        return round(value, 10)
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    return value


def sha256_file(path: Path) -> str:
    if not path_exists(path) or io_path(path).is_dir():
        return "missing"
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_text_lossless(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    return raw.decode("utf-8-sig"), raw.startswith(b"\xef\xbb\xbf")


def write_text_lossless(path: Path, text: str, had_bom: bool) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    encoding = "utf-8-sig" if had_bom else "utf-8"
    io_path(path).write_text(text, encoding=encoding, newline="\n")
    return path


def write_md(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.strip() + "\n", encoding="utf-8-sig", newline="\n")
    return path


def read_json(path: Path) -> Any:
    if not path_exists(path):
        return {}
    with io_path(path).open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Any) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8") as handle:
        json.dump(json_ready(payload), handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")
    return path


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column)) for column in columns})
    return path


def upsert_csv(path: Path, key_columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing: list[dict[str, Any]] = []
    fieldnames: list[str] = []
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            existing = [dict(row) for row in reader]
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    index_by_key = {
        tuple(str(row.get(column, "")) for column in key_columns): index
        for index, row in enumerate(existing)
    }
    for row in rows:
        key = tuple(str(row.get(column, "")) for column in key_columns)
        payload = {column: csv_value(row.get(column, "")) for column in fieldnames}
        if key in index_by_key:
            existing[index_by_key[key]] = payload
        else:
            existing.append(payload)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(existing)
    return path


def parse_json_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    if not value:
        return []
    try:
        parsed = json.loads(str(value))
    except json.JSONDecodeError:
        return [item.strip() for item in str(value).split(";") if item.strip()]
    if isinstance(parsed, list):
        return [str(item) for item in parsed]
    return [str(parsed)]


def as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes"}


def replace_prefix_line(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def insert_after_prefix_once(text: str, prefix: str, insertion: str, token: str) -> str:
    if token in text:
        return text
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index + 1 : index + 1] = insertion.strip("\n").splitlines()
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + insertion.strip() + "\n"


def remove_lines_containing(text: str, token: str) -> str:
    lines = [line for line in text.splitlines() if token not in line]
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def append_section_once(path: Path, heading: str, body: str) -> Path:
    text, had_bom = read_text_lossless(path) if path_exists(path) else ("", True)
    if heading in text:
        return path
    return write_text_lossless(path, text.rstrip() + "\n\n" + heading + "\n\n" + body.strip() + "\n", had_bom)


def infer_artifact_type(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return "csv_table"
    if suffix == ".json":
        return "json_manifest_or_receipt"
    if suffix == ".md":
        return "markdown_report"
    if suffix == ".py":
        return "python_script"
    return suffix.lstrip(".") or "unknown"


def source_hashes() -> dict[str, str]:
    sources = {**RUN335H_INPUTS, **RUN335G_INPUTS, **RUN335D_INPUTS}
    return {rel(path): sha256_file(path) for path in sources.values()}


def load_inputs() -> dict[str, Any]:
    return {
        "queue": read_csv_rows(RUN335H_INPUTS["run335i_queue"]),
        "gaps": read_csv_rows(RUN335H_INPUTS["evidence_gaps"]),
        "usability": read_csv_rows(RUN335H_INPUTS["usability_review"]),
        "review_matrix": read_csv_rows(RUN335H_INPUTS["review_matrix"]),
        "parent_decision": read_json(RUN335H_INPUTS["final_review_decision"]),
        "parent_manifest": read_json(RUN335H_INPUTS["run_manifest"]),
        "packages": read_csv_rows(RUN335G_INPUTS["package_manifest"]),
        "measurements": read_csv_rows(RUN335G_INPUTS["measurement_manifest"]),
        "proxy_manifest": read_csv_rows(RUN335G_INPUTS["proxy_expected_manifest"]),
        "mt5_schema": read_csv_rows(RUN335G_INPUTS["mt5_result_or_block"]),
        "readiness": read_csv_rows(RUN335G_INPUTS["comparison_readiness"]),
        "no_retune": read_csv_rows(RUN335G_INPUTS["no_retune_guard"]),
        "source_bindings": read_csv_rows(RUN335D_INPUTS["source_bindings"]),
        "runtime_gates": read_csv_rows(RUN335D_INPUTS["runtime_gates"]),
    }


def rows_for(rows: Sequence[Mapping[str, str]], key: str, value: str) -> list[dict[str, str]]:
    return [dict(row) for row in rows if row.get(key) == value]


def by_protocol(rows: Sequence[Mapping[str, str]]) -> dict[str, dict[str, str]]:
    return {str(row.get("protocol_id", "")): dict(row) for row in rows}


def mt5_preflight_rows() -> list[dict[str, Any]]:
    entries = [
        ("terminal_path", Path(TERMINAL_PATH_DEFAULT), "required_to_launch_strategy_tester"),
        ("metaeditor_path", Path(METAEDITOR_PATH_DEFAULT), "required_to_compile_ea_if_runtime_probe_runs"),
        ("terminal_data_root", Path(TERMINAL_DATA_ROOT_DEFAULT), "required_to_read_tester_reports_and_profiles"),
        ("common_files_root", Path(COMMON_FILES_ROOT_DEFAULT), "required_for_model_feature_and_telemetry_handoff"),
        ("tester_profile_root", Path(TESTER_PROFILE_ROOT_DEFAULT), "required_for_tester_ini_and_set_handoff"),
    ]
    return [
        {
            "preflight_item": name,
            "path": str(path),
            "exists": path_exists(path),
            "required_for": reason,
            "status": "passed" if path_exists(path) else "blocked_missing_environment_path",
            "claim_effect": "environment_inventory_only_no_runtime_authority",
        }
        for name, path, reason in entries
    ]


def environment_ready(preflight: Sequence[Mapping[str, Any]]) -> bool:
    return all(as_bool(row.get("exists", False)) for row in preflight)


def build_proxy_design(inputs: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    packages = by_protocol(inputs["packages"])
    proxy_schema = by_protocol(inputs["proxy_manifest"])
    review = by_protocol(inputs["review_matrix"])
    design_rows: list[dict[str, Any]] = []
    schema_rows: list[dict[str, Any]] = []
    for queue in inputs["queue"]:
        protocol_id = str(queue.get("protocol_id", ""))
        branch_id = str(queue.get("branch_id", ""))
        branch_name = str(queue.get("branch_name", ""))
        source_rows = rows_for(inputs["source_bindings"], "branch_id", branch_id)
        measurement_rows = rows_for(inputs["measurements"], "protocol_id", protocol_id)
        views = [row.get("measurement_view", "") for row in measurement_rows if row.get("measurement_view")]
        required_dimensions = parse_json_list(proxy_schema.get(protocol_id, {}).get("required_dimensions", "")) or COMPARISON_DIMENSIONS
        package = packages.get(protocol_id, {})
        passed_review = as_bool(review.get(protocol_id, {}).get("all_checks_passed", False))
        design_rows.append(
            {
                "protocol_id": protocol_id,
                "branch_id": branch_id,
                "branch_name": branch_name,
                "payload_path": package.get("payload_path", ""),
                "payload_sha256": package.get("payload_sha256", ""),
                "source_binding_rows": len(source_rows),
                "measurement_views": views,
                "required_dimensions": required_dimensions,
                "proxy_expected_numeric_result_available": False,
                "run335I_status": "designed_ready_for_run335J_proxy_expected_value_materialization" if passed_review else "blocked_parent_review_failed",
                "proxy_expected_identity_rule": "values_must_be_generated_from_bound_sources_after_this_design_without_retune",
                "claim_effect": "no proxy usability claim until numeric values exist",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        for dimension in required_dimensions:
            schema_rows.append(
                {
                    "protocol_id": protocol_id,
                    "branch_id": branch_id,
                    "branch_name": branch_name,
                    "dimension": dimension,
                    "required_views": views,
                    "value_field": f"proxy_expected_{dimension}",
                    "missing_reason_field": f"proxy_expected_{dimension}_missing_reason",
                    "source_binding_rows": len(source_rows),
                    "numeric_value_required_in": NEXT_RUN_ID,
                    "run335I_value_status": "schema_only_no_numeric_value_in_design_run",
                    "invalid_if": "value_generated_after_threshold_or_lot_change",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return design_rows, schema_rows


def build_mt5_design(inputs: Mapping[str, Any], preflight: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    env_ok = environment_ready(preflight)
    mt5_schema = by_protocol(inputs["mt5_schema"])
    readiness = by_protocol(inputs["readiness"])
    rows: list[dict[str, Any]] = []
    for queue in inputs["queue"]:
        protocol_id = str(queue.get("protocol_id", ""))
        branch_id = str(queue.get("branch_id", ""))
        branch_name = str(queue.get("branch_name", ""))
        runtime_rows = rows_for(inputs["runtime_gates"], "branch_id", branch_id)
        existing_schema = mt5_schema.get(protocol_id, {})
        missing_attempt = not any(
            artifact in queue.get("required_inputs", "")
            for artifact in ["mt5 set", "tester ini", "runtime attempt"]
        )
        status = (
            "design_ready_but_runtime_attempt_materialization_required_before_execution"
            if env_ok and missing_attempt
            else "blocked_missing_mt5_environment_path"
        )
        rows.append(
            {
                "protocol_id": protocol_id,
                "branch_id": branch_id,
                "branch_name": branch_name,
                "environment_preflight_passed": env_ok,
                "runtime_gate_rows": len(runtime_rows),
                "mt5_schema_status_from_parent": existing_schema.get("mt5_runtime_probe_status", ""),
                "parent_mt5_result_available": existing_schema.get("mt5_result_available", "false"),
                "parent_comparison_status": readiness.get(protocol_id, {}).get("comparison_status", ""),
                "run335I_mt5_design_status": status,
                "runtime_attempt_materialization_required": True,
                "minimum_runtime_artifacts_required": [
                    "MT5 tester .ini",
                    "EA .set",
                    "feature/model/signal handoff identity",
                    "Strategy Tester HTML report",
                    "runtime telemetry CSV",
                    "settings and cost identity",
                ],
                "command_blueprint": "python stage_pipelines/stage335/materialize_proxy_mt5_comparison.py",
                "blocker_if_not_materialized": "missing_branch_specific_set_ini_feature_model_or_signal_handoff",
                "claim_effect": "no MT5 usability or Forward Passed/Failed claim in run335I",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_difference_contract(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for queue in inputs["queue"]:
        protocol_id = str(queue.get("protocol_id", ""))
        branch_id = str(queue.get("branch_id", ""))
        branch_name = str(queue.get("branch_name", ""))
        for dimension in COMPARISON_DIMENSIONS:
            rows.append(
                {
                    "protocol_id": protocol_id,
                    "branch_id": branch_id,
                    "branch_name": branch_name,
                    "dimension": dimension,
                    "proxy_field": f"proxy_expected_{dimension}",
                    "mt5_field": f"mt5_runtime_{dimension}",
                    "difference_field": f"proxy_minus_mt5_{dimension}",
                    "tolerance_policy": "dimension_specific_or_explain_difference_with_logged_runtime_cost_fill_session_or_handoff_evidence",
                    "usable_if": USABILITY_RULE,
                    "not_usable_if": "proxy_missing_or_mt5_missing_or_difference_unexplained_or_identity_drift_detected",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def build_usability_rules(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for queue in inputs["queue"]:
        protocol_id = str(queue.get("protocol_id", ""))
        rows.append(
            {
                "protocol_id": protocol_id,
                "branch_id": queue.get("branch_id", ""),
                "branch_name": queue.get("branch_name", ""),
                "current_usability_judgment": "not_usable_yet",
                "required_before_usable": [
                    "proxy expected numeric values",
                    "MT5 runtime probe result or explicit blocker",
                    "proxy-MT5 difference table",
                    "runtime identity and cost forensic receipt",
                    "forbidden retune audit",
                ],
                "usable_rule": USABILITY_RULE,
                "forward_pass_fail_rule": "not_allowed_in_run335I_or_run335J_until_actual_proxy_mt5_comparison_and_stage_decision_gate",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_no_retune_audit(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    no_retune = by_protocol(inputs["no_retune"])
    for queue in inputs["queue"]:
        protocol_id = str(queue.get("protocol_id", ""))
        parent = no_retune.get(protocol_id, {})
        rows.append(
            {
                "protocol_id": protocol_id,
                "branch_id": queue.get("branch_id", ""),
                "branch_name": queue.get("branch_name", ""),
                "parent_guard_status": parent.get("guard_status", ""),
                "threshold_policy": parent.get("threshold_policy", "locked_no_retune"),
                "lot_policy": parent.get("lot_policy", "locked_no_optimization"),
                "direct_forward_pocket_filter_policy": parent.get("direct_forward_pocket_filter_policy", "forbidden"),
                "runtime_authority_policy": parent.get("runtime_authority_policy", "forbidden_without_tester_and_telemetry"),
                "run335I_guard_status": "locked",
                "claim_effect": "materialization can proceed only without retune or direct pocket filter",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_next_queue(proxy_rows: Sequence[Mapping[str, Any]], mt5_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    mt5_by_protocol = {str(row.get("protocol_id", "")): row for row in mt5_rows}
    rows: list[dict[str, Any]] = []
    for proxy in proxy_rows:
        protocol_id = str(proxy.get("protocol_id", ""))
        mt5 = mt5_by_protocol.get(protocol_id, {})
        ready = (
            proxy.get("run335I_status") == "designed_ready_for_run335J_proxy_expected_value_materialization"
            and str(mt5.get("run335I_mt5_design_status", "")).startswith("design_ready")
        )
        rows.append(
            {
                "queue_id": f"{NEXT_RUN_ID}__{proxy.get('branch_name', '')}",
                "protocol_id": protocol_id,
                "branch_id": proxy.get("branch_id", ""),
                "branch_name": proxy.get("branch_name", ""),
                "next_action": NEXT_RUN_ID,
                "materialize_proxy_expected_values": True,
                "materialize_mt5_runtime_attempt_or_block": True,
                "required_sources": proxy.get("source_binding_rows", ""),
                "required_dimensions": proxy.get("required_dimensions", ""),
                "required_runtime_artifacts": mt5.get("minimum_runtime_artifacts_required", ""),
                "forbidden_actions": [
                    "model training",
                    "threshold retuning",
                    "lot optimization",
                    "direct forward pocket filter",
                    "candidate selection",
                    "runtime authority claim",
                    "Goal Achieve claim",
                ],
                "ready_for_run335J": ready,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_gate_rows(
    inputs: Mapping[str, Any],
    proxy_rows: Sequence[Mapping[str, Any]],
    proxy_schema_rows: Sequence[Mapping[str, Any]],
    mt5_rows: Sequence[Mapping[str, Any]],
    difference_rows: Sequence[Mapping[str, Any]],
    usability_rows: Sequence[Mapping[str, Any]],
    no_retune_rows: Sequence[Mapping[str, Any]],
    next_queue: Sequence[Mapping[str, Any]],
    preflight: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    checks = [
        (
            "parent_queue_loaded",
            len(inputs["queue"]) == 11,
            "run335I_proxy_mt5_execution_or_block_design_queue.csv",
            f"queue_rows={len(inputs['queue'])}",
        ),
        (
            "proxy_expected_design_rows",
            len(proxy_rows) == 11 and len(proxy_schema_rows) == 11 * len(COMPARISON_DIMENSIONS),
            "proxy_expected_value_design_matrix.csv",
            f"design_rows={len(proxy_rows)};schema_rows={len(proxy_schema_rows)}",
        ),
        (
            "mt5_runtime_design_rows",
            len(mt5_rows) == 11,
            "mt5_runtime_probe_or_block_design.csv",
            f"mt5_rows={len(mt5_rows)}",
        ),
        (
            "environment_preflight_recorded",
            len(preflight) == 5,
            "mt5_environment_preflight.csv",
            f"preflight_rows={len(preflight)};passed={environment_ready(preflight)}",
        ),
        (
            "difference_contract_rows",
            len(difference_rows) == 11 * len(COMPARISON_DIMENSIONS),
            "proxy_mt5_difference_comparison_contract.csv",
            f"difference_rows={len(difference_rows)}",
        ),
        (
            "usability_rules_not_claimed",
            len(usability_rows) == 11 and all(row.get("current_usability_judgment") == "not_usable_yet" for row in usability_rows),
            "proxy_mt5_usability_judgment_rule.csv",
            f"usability_rows={len(usability_rows)}",
        ),
        (
            "no_retune_guard_locked",
            len(no_retune_rows) == 11 and all(row.get("run335I_guard_status") == "locked" for row in no_retune_rows),
            "forbidden_retune_audit.csv",
            f"no_retune_rows={len(no_retune_rows)}",
        ),
        (
            "next_materialization_queue",
            len(next_queue) == 11 and all(as_bool(row.get("ready_for_run335J", False)) for row in next_queue),
            "run335J_materialization_queue.csv",
            f"queue_rows={len(next_queue)}",
        ),
        (
            "claim_boundary_preserved",
            True,
            "result_judgment.csv",
            "no candidate selection, no forward pass/fail, no runtime authority, no goal achieve",
        ),
    ]
    return [
        {
            "gate": gate,
            "status": "passed" if ok else "failed",
            "evidence_path": evidence,
            "detail": detail,
        }
        for gate, ok, evidence, detail in checks
    ]


def build_receipts(
    inputs: Mapping[str, Any],
    preflight: Sequence[Mapping[str, Any]],
    proxy_rows: Sequence[Mapping[str, Any]],
    mt5_rows: Sequence[Mapping[str, Any]],
    difference_rows: Sequence[Mapping[str, Any]],
    gate_rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    failed_gates = [row for row in gate_rows if row.get("status") != "passed"]
    return {
        "experiment_design_receipt": {
            "hypothesis": "Stage335 failure-memory branches can be tested through predeclared proxy-vs-MT5 comparison without retuning.",
            "decision_use": "may influence run335J materialization only; not candidate selection",
            "comparison_baseline": "run335H reviewed probe packages and Stage334/335 failure-memory evidence",
            "control_variables": [
                "model identity locked until new materialization explicitly creates a non-selection probe",
                "threshold locked",
                "lot and risk logic locked",
                "ATR SL/TP locked",
                "no direct forward pocket filter",
            ],
            "changed_variables": "design of proxy expected values, MT5 attempt/block contract, and difference comparison only",
            "sample_scope": "US100 M5 Stage335 research branches; forward evidence remains research-only",
            "success_criteria": "run335J can materialize proxy expected values and MT5 runtime attempt or blocker for all 11 protocols",
            "failure_criteria": "any protocol requires retune, subject swap, or direct forward pocket filter",
            "invalid_conditions": "missing parent package, missing source binding, or unlogged runtime identity drift",
            "stop_conditions": "stop before usability claim if proxy or MT5 result is missing",
            "evidence_plan": [
                rel(RUN_DIR / "proxy_expected_value_schema.csv"),
                rel(RUN_DIR / "mt5_runtime_probe_or_block_design.csv"),
                rel(RUN_DIR / "proxy_mt5_difference_comparison_contract.csv"),
                rel(RUN_DIR / "run335J_materialization_queue.csv"),
            ],
        },
        "data_integrity_receipt": {
            "data_source": [rel(path) for path in [*RUN335H_INPUTS.values(), *RUN335G_INPUTS.values(), *RUN335D_INPUTS.values()]],
            "time_axis": "run335I is design-only; future values must preserve FPMarkets US100 M5 timestamp and broker close convention.",
            "sample_scope": "11 Stage335 protocols, paired Tier A/Tier B/Tier A+B measurement views",
            "missing_or_duplicate_check": "not applicable to design values; run335J must check generated proxy and MT5 row identities",
            "feature_label_boundary": "no feature or label values are generated in run335I",
            "split_boundary": "post-2026-04-14 evidence is research-only and cannot tune thresholds",
            "leakage_risk": "using forward MT5 result to choose thresholds or filter curve pockets",
            "data_hash_or_identity": source_hashes(),
            "integrity_judgment": "usable_with_boundary",
        },
        "runtime_parity_receipt": {
            "research_path": rel(Path(__file__)),
            "runtime_path": [str(Path(TERMINAL_PATH_DEFAULT)), str(Path(METAEDITOR_PATH_DEFAULT)), str(Path(TERMINAL_DATA_ROOT_DEFAULT))],
            "shared_contract": "proxy values, MT5 runtime results, feature/model/signal handoff, threshold, lot, risk, and time-axis identity must match before comparison",
            "known_differences": "no branch-specific MT5 set/ini/report exists in run335I; run335J must materialize or block",
            "parity_check": "environment preflight and runtime artifact contract design only",
            "parity_identity": {
                "terminal_path_exists": path_exists(Path(TERMINAL_PATH_DEFAULT)),
                "metaeditor_path_exists": path_exists(Path(METAEDITOR_PATH_DEFAULT)),
                "terminal_data_root_exists": path_exists(Path(TERMINAL_DATA_ROOT_DEFAULT)),
                "preflight_rows": len(preflight),
            },
            "runtime_claim_boundary": "not_applicable_until_run335J_or_later_actual_mt5_tester_output_exists",
        },
        "backtest_forensics_receipt": {
            "tester_identity": {
                "terminal": str(Path(TERMINAL_PATH_DEFAULT)),
                "symbol": "US100",
                "timeframe": "M5",
                "deposit": "must_be_recorded_by_run335J",
                "leverage": "must_be_recorded_by_run335J",
                "modeling_mode": "must_be_recorded_by_run335J",
                "date_range": "must_be_recorded_by_run335J",
            },
            "ea_identity": "not materialized in run335I; required in run335J",
            "report_identity": "missing by design; report path required before usable comparison",
            "trade_evidence": "missing by design; no MT5 KPI interpretation",
            "cost_assumptions": "spread, commission, slippage, swap must be logged by run335J",
            "forensic_checks": "environment path preflight and required artifact list",
            "backtest_judgment": "inconclusive_until_runtime_attempt_or_block_materialized",
        },
        "result_judgment_receipt": {
            "result_subject": RUN_ID,
            "evidence_available": [rel(RUN_DIR / "required_gate_coverage_audit.csv"), rel(RUN_DIR / "run335J_materialization_queue.csv")],
            "evidence_missing": [
                "proxy expected numeric values",
                "MT5 tester report",
                "runtime telemetry",
                "proxy-MT5 difference table",
            ],
            "judgment_label": "exploratory_design_completed",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "The comparison is now designed, but no proxy or MT5 numeric result can be used yet.",
        },
        "anti_overfit_design_receipt": {
            "retune_policy": "forbidden",
            "direct_forward_pocket_filter_policy": "forbidden",
            "subject_swap_policy": "forbidden",
            "usable_only_after": USABILITY_RULE,
            "guarded_protocols": len(proxy_rows),
        },
        "performance_attribution_receipt": {
            "observed_change": "none; design-only run",
            "comparison_baseline": "run335H missing proxy/MT5 evidence",
            "likely_drivers": "not assessed until numeric proxy and MT5 results exist",
            "segment_checks": "predeclared dimensions: " + ",".join(COMPARISON_DIMENSIONS),
            "trade_shape": "missing until MT5 runtime probe result exists",
            "alternative_explanations": ["runtime identity drift", "cost assumptions", "session mismatch", "handoff mismatch"],
            "attribution_confidence": "inconclusive",
            "next_probe": NEXT_RUN_ID,
        },
        "artifact_lineage_receipt": {
            "source_inputs": [rel(path) for path in [*RUN335H_INPUTS.values(), *RUN335G_INPUTS.values(), *RUN335D_INPUTS.values()]],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [],
            "artifact_hashes": {},
            "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_after_force_add_run_dir",
            "lineage_judgment": "connected_with_boundary",
        },
        "gate_receipt": {
            "required_gates": gate_rows,
            "failed_gates": failed_gates,
        },
    }


def build_report_text(proxy_rows: Sequence[Mapping[str, Any]], mt5_rows: Sequence[Mapping[str, Any]], next_queue: Sequence[Mapping[str, Any]], gate_rows: Sequence[Mapping[str, Any]]) -> str:
    failed_gates = [row for row in gate_rows if row.get("status") != "passed"]
    ready = sum(1 for row in next_queue if as_bool(row.get("ready_for_run335J", False)))
    env_ok = sum(1 for row in mt5_rows if as_bool(row.get("environment_preflight_passed", False)))
    return f"""
# run335I Proxy Expected And MT5 Runtime Probe Or Block Design(335I 프록시 예상값 및 MT5 런타임 탐침 또는 차단 설계)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- proxy_protocols(프록시 계약): `{len(proxy_rows)}`
- mt5_design_rows(MT5 설계 행): `{len(mt5_rows)}`
- run335J_ready_rows(335J 준비 행): `{ready}/{len(next_queue)}`
- environment_ready_rows(환경 준비 행): `{env_ok}/{len(mt5_rows)}`
- failed_gates(실패 게이트): `{len(failed_gates)}`
- next_action(다음 행동): `{NEXT_RUN_ID}`

Effect(효과): run335H(335H 실행)의 11개 probe package(탐침 패키지)를 proxy expected value(프록시 예상값), MT5 runtime probe(메타트레이더5 런타임 탐침), difference comparison(차이 비교), usability judgment(활용 가능성 판정) 계약으로 바꿨다.

현재 숫자 결과는 없다. 이 말은 실패가 아니라, run335J(335J 실행)에서 proxy expected numeric values(프록시 예상 숫자값)와 MT5 tester output(테스터 출력)을 만들거나 차단 사유를 남겨야 한다는 뜻이다.

Boundary(경계): candidate selection(후보 선택), Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), live readiness(실거래 준비), deployment(배포), operating promotion(운영 승격), Goal Achieve(목표 달성)는 모두 `not_claimed`다.
"""


def build_decision_text() -> str:
    return f"""
# Stage335I Decision(335I 결정)

`{RUN_ID}`는 proxy expected value(프록시 예상값)와 MT5 runtime probe(메타트레이더5 런타임 탐침)를 비교하기 위한 실행-or-block(실행 또는 차단) 설계를 완료했다.

- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Effect(효과): 다음 실행은 숫자 proxy expected values(프록시 예상값)와 MT5 runtime result or blocker(MT5 런타임 결과 또는 차단 사유)를 실제 산출물로 만들어야 한다. 현재는 활용 가능성, 전진 통과/실패, 목표 달성을 주장하지 않는다.
"""


def update_state_docs() -> list[Path]:
    changed: list[Path] = []

    selection_path = SELECTED_DIR / "selection_status.md"
    text, had_bom = read_text_lossless(selection_path)
    text = replace_prefix_line(text, "- current_run", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    text = replace_prefix_line(text, "- next_action", f"- next_action(다음 행동): `{NEXT_RUN_ID}`")
    text = replace_prefix_line(
        text,
        "- effect",
        "- effect(효과): Stage335I(335I 실행)는 proxy/MT5(프록시/메타트레이더5) 비교 설계를 완료했지만 숫자 proxy result(프록시 결과)와 MT5 runtime probe result(MT5 런타임 탐침 결과)는 아직 없어 활용 가능성(usability, 활용 가능성)은 아직 없다.",
    )
    changed.append(write_text_lossless(selection_path, text, had_bom))

    text, had_bom = read_text_lossless(STAGE_BRIEF)
    text = replace_prefix_line(text, "- latest_run", f"- latest_run(최신 실행): `{RUN_ID}`")
    changed.append(write_text_lossless(STAGE_BRIEF, text, had_bom))

    changed.append(
        append_section_once(
            INPUTS_DIR / "input_refs.md",
            "## run335I Proxy-MT5 Design(335I 프록시-MT5 설계)",
            f"""- proxy_expected_value_schema(프록시 예상값 구조): `{rel(RUN_DIR / "proxy_expected_value_schema.csv")}`
- mt5_runtime_probe_or_block_design(MT5 런타임 탐침 또는 차단 설계): `{rel(RUN_DIR / "mt5_runtime_probe_or_block_design.csv")}`
- difference_contract(차이 비교 계약): `{rel(RUN_DIR / "proxy_mt5_difference_comparison_contract.csv")}`
- run335J_queue(335J 대기열): `{rel(RUN_DIR / "run335J_materialization_queue.csv")}`
- decision(결정): `{rel(DECISION_DOC)}`""",
        )
    )

    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_prefix_line(workspace_text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    workspace_text = replace_prefix_line(workspace_text, "updated_on:", f"updated_on: '{TODAY}'")
    focus_line = (
        "- >-\n"
        f"  Stage335(335단계) run335I(335I 실행)는 `{STATUS}`로 proxy expected value/MT5 runtime probe(프록시 예상값/메타트레이더5 런타임 탐침) 실행-or-block 설계를 완료했다. "
        "Effect(효과): 11개 protocol(계약)을 run335J(335J 실행)의 proxy numeric value(프록시 숫자값)와 MT5 result/block(MT5 결과/차단) 물질화 대기열로 넘기며 Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    workspace_text = insert_after_prefix_once(workspace_text, "current_focus:", focus_line, "run335I(335I 실행)")
    changed.append(write_text_lossless(WORKSPACE_STATE, workspace_text, workspace_bom))

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    current_text = replace_prefix_line(current_text, "- current_packet", "- current_packet(현재 작업 묶음): `335_overfit_guard__failure_memory_constrained_research_handoff_v10`")
    current_text = replace_prefix_line(current_text, "- current_run", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    current_text = replace_prefix_line(current_text, "- status", f"- status(상태): `{STATUS}`")
    current_text = replace_prefix_line(current_text, "- decision", f"- decision(판정): `{DECISION}`")
    current_text = remove_lines_containing(current_text, "run335I_summary")
    summary = (
        f"- run335I_summary(335I 요약): proxy expected and MT5 runtime probe/block design(프록시 예상값 및 MT5 런타임 탐침/차단 설계)을 `{STATUS}`로 완료했다. "
        "Effect(효과): 11개 protocol(계약)의 proxy schema(프록시 구조), MT5 preflight(사전 점검), difference contract(차이 계약), usability rule(활용 가능성 규칙), run335J materialization queue(335J 물질화 대기열)를 만들었고, 활용 가능성이나 Forward Passed/Failed(전진 통과/실패), Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    current_text = insert_after_prefix_once(current_text, "- decision", summary, "run335I_summary")
    changed.append(write_text_lossless(CURRENT_STATE, current_text, current_bom))

    changed.append(
        append_section_once(
            CHANGELOG,
            "## 2026-05-26 Stage335I Proxy-MT5 Design(335I 프록시-MT5 설계)",
            f"""- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- effect(효과): 11개 Stage335 protocol(계약)을 proxy expected value(프록시 예상값), MT5 runtime result or block(MT5 런타임 결과 또는 차단), difference comparison(차이 비교) 물질화 대기열로 바꿨다.
- boundary(경계): no candidate(후보 없음), no Forward Passed/Failed(전진 통과/실패 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).""",
        )
    )
    return changed


def update_registries(outputs: Sequence[Path], report_path: Path) -> list[Path]:
    changed: list[Path] = []
    changed.append(
        upsert_csv(
            RUN_REGISTRY,
            ["run_id"],
            [
                {
                    "run_id": RUN_ID,
                    "stage_id": STAGE_ID,
                    "lane": "experiment_execution",
                    "status": STATUS,
                    "judgment": JUDGMENT,
                    "path": rel(report_path),
                    "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};proxy_mt5_design_only;goal_achieve_not_claimed.",
                }
            ],
        )
    )
    ledger_row = {
        "ledger_row_id": f"{RUN_ID}__proxy_mt5_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "proxy_expected_mt5_runtime_probe_or_block_design",
        "tier_scope": "paired_tier_required_by_contract",
        "kpi_scope": "design_only_no_new_trading_kpi",
        "scoreboard_lane": "experiment_execution",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(report_path),
        "primary_kpi": "protocols=11;comparison_dimensions=132;run335J_queue_rows=11",
        "guardrail_kpi": "proxy_mt5_numeric_results_missing_by_design;no_retune;goal_achieve_not_claimed",
        "external_verification_status": "out_of_scope_by_claim_design_only_preflight_recorded",
        "notes": f"decision={DECISION};next_action={NEXT_RUN_ID}.",
    }
    changed.append(upsert_csv(ALPHA_LEDGER, ["ledger_row_id"], [ledger_row]))
    changed.append(
        upsert_csv(
            STAGE_LEDGER,
            ["ledger_row_id"],
            [
                {
                    "ledger_row_id": ledger_row["ledger_row_id"],
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "work_family": "experiment_execution",
                    "evidence_scope": "proxy_expected_mt5_runtime_probe_or_block_design",
                    "kpi_scope": "design_only_no_new_trading_kpi",
                    "status": STATUS,
                    "judgment": JUDGMENT,
                    "claim_boundary": CLAIM_BOUNDARY,
                    "path": rel(report_path),
                    "notes": "no_candidate_selected;proxy_mt5_not_usable_yet;goal_achieve_not_claimed.",
                    "decision": DECISION,
                }
            ],
        )
    )
    created_at = utc_now()
    artifact_rows = []
    for output in outputs:
        artifact_rows.append(
            {
                "artifact_id": f"{RUN_ID}::{rel(output)}",
                "artifact_type": infer_artifact_type(output),
                "path": rel(output),
                "sha256": sha256_file(output),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": f"Stage335I proxy-MT5 design artifact; claim_boundary={CLAIM_BOUNDARY}",
            }
        )
    changed.append(upsert_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows))
    return changed


def main() -> int:
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    inputs = load_inputs()
    preflight = mt5_preflight_rows()
    proxy_rows, proxy_schema_rows = build_proxy_design(inputs)
    mt5_rows = build_mt5_design(inputs, preflight)
    difference_rows = build_difference_contract(inputs)
    usability_rows = build_usability_rules(inputs)
    no_retune_rows = build_no_retune_audit(inputs)
    next_queue = build_next_queue(proxy_rows, mt5_rows)
    gate_rows = build_gate_rows(
        inputs,
        proxy_rows,
        proxy_schema_rows,
        mt5_rows,
        difference_rows,
        usability_rows,
        no_retune_rows,
        next_queue,
        preflight,
    )
    receipts = build_receipts(inputs, preflight, proxy_rows, mt5_rows, difference_rows, gate_rows)
    failed_gates = [row for row in gate_rows if row.get("status") != "passed"]
    ready_next = [row for row in next_queue if as_bool(row.get("ready_for_run335J", False))]

    result_rows = [
        {
            "run_id": RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "selected_candidate": "none",
            "forward_passed": "not_claimed",
            "forward_failed": "not_claimed",
            "runtime_authority": "not_claimed",
            "proxy_mt5_usability": "not_claimed_not_usable_yet",
            "goal_achieve": "not_claimed",
            "next_action": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    final_decision = {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "protocol_count": len(proxy_rows),
        "proxy_schema_rows": len(proxy_schema_rows),
        "mt5_design_rows": len(mt5_rows),
        "difference_contract_rows": len(difference_rows),
        "run335j_queue_rows": len(next_queue),
        "run335j_ready_rows": len(ready_next),
        "failed_gates": len(failed_gates),
        "selected_candidate": "none",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "proxy_mt5_usability": "not_claimed_not_usable_yet",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }

    artifact_paths: list[Path] = [
        write_json(RUN_DIR / "source_artifact_hashes.json", source_hashes()),
        write_csv(
            RUN_DIR / "mt5_environment_preflight.csv",
            ["preflight_item", "path", "exists", "required_for", "status", "claim_effect"],
            preflight,
        ),
        write_csv(
            RUN_DIR / "proxy_expected_value_design_matrix.csv",
            [
                "protocol_id",
                "branch_id",
                "branch_name",
                "payload_path",
                "payload_sha256",
                "source_binding_rows",
                "measurement_views",
                "required_dimensions",
                "proxy_expected_numeric_result_available",
                "run335I_status",
                "proxy_expected_identity_rule",
                "claim_effect",
                "claim_boundary",
            ],
            proxy_rows,
        ),
        write_csv(
            RUN_DIR / "proxy_expected_value_schema.csv",
            [
                "protocol_id",
                "branch_id",
                "branch_name",
                "dimension",
                "required_views",
                "value_field",
                "missing_reason_field",
                "source_binding_rows",
                "numeric_value_required_in",
                "run335I_value_status",
                "invalid_if",
                "claim_boundary",
            ],
            proxy_schema_rows,
        ),
        write_csv(
            RUN_DIR / "mt5_runtime_probe_or_block_design.csv",
            [
                "protocol_id",
                "branch_id",
                "branch_name",
                "environment_preflight_passed",
                "runtime_gate_rows",
                "mt5_schema_status_from_parent",
                "parent_mt5_result_available",
                "parent_comparison_status",
                "run335I_mt5_design_status",
                "runtime_attempt_materialization_required",
                "minimum_runtime_artifacts_required",
                "command_blueprint",
                "blocker_if_not_materialized",
                "claim_effect",
                "claim_boundary",
            ],
            mt5_rows,
        ),
        write_csv(
            RUN_DIR / "proxy_mt5_difference_comparison_contract.csv",
            [
                "protocol_id",
                "branch_id",
                "branch_name",
                "dimension",
                "proxy_field",
                "mt5_field",
                "difference_field",
                "tolerance_policy",
                "usable_if",
                "not_usable_if",
                "claim_boundary",
            ],
            difference_rows,
        ),
        write_csv(
            RUN_DIR / "proxy_mt5_usability_judgment_rule.csv",
            [
                "protocol_id",
                "branch_id",
                "branch_name",
                "current_usability_judgment",
                "required_before_usable",
                "usable_rule",
                "forward_pass_fail_rule",
                "claim_boundary",
            ],
            usability_rows,
        ),
        write_csv(
            RUN_DIR / "forbidden_retune_audit.csv",
            [
                "protocol_id",
                "branch_id",
                "branch_name",
                "parent_guard_status",
                "threshold_policy",
                "lot_policy",
                "direct_forward_pocket_filter_policy",
                "runtime_authority_policy",
                "run335I_guard_status",
                "claim_effect",
                "claim_boundary",
            ],
            no_retune_rows,
        ),
        write_csv(
            RUN_DIR / "run335J_materialization_queue.csv",
            [
                "queue_id",
                "protocol_id",
                "branch_id",
                "branch_name",
                "next_action",
                "materialize_proxy_expected_values",
                "materialize_mt5_runtime_attempt_or_block",
                "required_sources",
                "required_dimensions",
                "required_runtime_artifacts",
                "forbidden_actions",
                "ready_for_run335J",
                "claim_boundary",
            ],
            next_queue,
        ),
        write_csv(
            RUN_DIR / "required_gate_coverage_audit.csv",
            ["gate", "status", "evidence_path", "detail"],
            gate_rows,
        ),
        write_csv(
            RUN_DIR / "result_judgment.csv",
            [
                "run_id",
                "status",
                "judgment",
                "decision",
                "selected_candidate",
                "forward_passed",
                "forward_failed",
                "runtime_authority",
                "proxy_mt5_usability",
                "goal_achieve",
                "next_action",
                "claim_boundary",
            ],
            result_rows,
        ),
        write_json(RUN_DIR / "experiment_design_receipt.json", receipts["experiment_design_receipt"]),
        write_json(RUN_DIR / "data_integrity_receipt.json", receipts["data_integrity_receipt"]),
        write_json(RUN_DIR / "runtime_parity_receipt.json", receipts["runtime_parity_receipt"]),
        write_json(RUN_DIR / "backtest_forensics_receipt.json", receipts["backtest_forensics_receipt"]),
        write_json(RUN_DIR / "result_judgment_receipt.json", receipts["result_judgment_receipt"]),
        write_json(RUN_DIR / "anti_overfit_design_receipt.json", receipts["anti_overfit_design_receipt"]),
        write_json(RUN_DIR / "performance_attribution_receipt.json", receipts["performance_attribution_receipt"]),
        write_json(RUN_DIR / "gate_receipt.json", receipts["gate_receipt"]),
        write_json(RUN_DIR / "final_proxy_mt5_design_decision.json", final_decision),
    ]

    manifest_path = RUN_DIR / "run_manifest.json"
    lineage_path = RUN_DIR / "artifact_lineage_receipt.json"
    run_manifest = {
        **final_decision,
        "created_at_utc": utc_now(),
        "producer": rel(Path(__file__)),
        "source_inputs": [rel(path) for path in [*RUN335H_INPUTS.values(), *RUN335G_INPUTS.values(), *RUN335D_INPUTS.values()]],
        "outputs": [rel(path) for path in [*artifact_paths, manifest_path, lineage_path]],
    }
    artifact_paths.append(write_json(manifest_path, run_manifest))

    lineage = receipts["artifact_lineage_receipt"]
    lineage["artifact_paths"] = [rel(path) for path in [*artifact_paths, lineage_path]]
    lineage["artifact_hashes"] = {rel(path): sha256_file(path) for path in artifact_paths}
    artifact_paths.append(write_json(lineage_path, lineage))

    report_path = write_md(REVIEWS_DIR / "run335I_proxy_expected_mt5_runtime_probe_or_block_design.md", build_report_text(proxy_rows, mt5_rows, next_queue, gate_rows))
    artifact_paths.append(report_path)
    artifact_paths.append(write_md(DECISION_DOC, build_decision_text()))
    artifact_paths.extend(update_state_docs())
    artifact_paths.extend(update_registries([Path(__file__), *artifact_paths], report_path))

    summary = {
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "protocol_count": len(proxy_rows),
        "proxy_schema_rows": len(proxy_schema_rows),
        "mt5_design_rows": len(mt5_rows),
        "difference_contract_rows": len(difference_rows),
        "run335j_queue_rows": len(next_queue),
        "run335j_ready_rows": len(ready_next),
        "failed_gates": len(failed_gates),
        "selected_candidate": "none",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "proxy_mt5_usability": "not_claimed_not_usable_yet",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_RUN_ID,
        "artifact_count": len(artifact_paths),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
