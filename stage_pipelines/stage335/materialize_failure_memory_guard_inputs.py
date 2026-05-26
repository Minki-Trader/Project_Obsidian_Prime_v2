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


TODAY = "2026-05-26"
STAGE_ID = "335_overfit_guard__failure_memory_constrained_research_handoff"
SOURCE_STAGE_ID = "334_runtime_parity__forward_usable_onnx_handoff_contract_hardening"
RUN_NUMBER = "run335B"
RUN_ID = "run335B_materialize_failure_memory_guard_inputs_v1"
PARENT_RUN_ID = "run335A_design_failure_memory_constrained_research_packet_v1"
NEXT_RUN_ID = "run335C_design_guarded_failure_memory_research_branches_v1"
STATUS = "completed_failure_memory_guard_inputs_materialized_no_selection"
JUDGMENT = "guard_inputs_materialized_research_only_no_goal_achieve"
DECISION = "stage335B_guard_inputs_materialized_ready_for_branch_design_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage335B_guard_input_materialization_no_model_training_"
    "no_threshold_retuning_no_lot_optimization_no_direct_forward_pocket_filtering_"
    "no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_"
    "no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
INPUTS_DIR = STAGE_DIR / "01_inputs"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"

RUN335A_DIR = STAGE_DIR / "02_runs" / "run335A"
SOURCE_STAGE_DIR = ROOT / "stages" / SOURCE_STAGE_ID
RUN334B_DIR = SOURCE_STAGE_DIR / "02_runs" / "run334B"
RUN334F_DIR = SOURCE_STAGE_DIR / "02_runs" / "run334F"
RUN334G_DIR = SOURCE_STAGE_DIR / "02_runs" / "run334G"
RUN334H_DIR = SOURCE_STAGE_DIR / "02_runs" / "run334H"
RUN329H_DIR = ROOT / "stages" / "329_onnx_rebuild__live_feature_control" / "02_runs" / "run329H"
RUN330E_DIR = ROOT / "stages" / "330_onnx_rebuild__forward_safe_non_identity_surface_robustness" / "02_runs" / "run330E"
RUN330F_DIR = ROOT / "stages" / "330_onnx_rebuild__forward_safe_non_identity_surface_robustness" / "02_runs" / "run330F"
RUN332B_DIR = ROOT / "stages" / "332_overfit_guard__failure_memory_forward_research_handoff" / "02_runs" / "run332B"

DOCS = ROOT / "docs"
RUN_REGISTRY = DOCS / "registers" / "run_registry.csv"
ALPHA_LEDGER = DOCS / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = DOCS / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
WORKSPACE_STATE = DOCS / "workspace" / "workspace_state.yaml"
CURRENT_STATE = DOCS / "context" / "current_working_state.md"
CHANGELOG = DOCS / "workspace" / "changelog.md"
DECISION_DOC = DOCS / "decisions" / "2026-05-26_stage335B_failure_memory_guard_input_materialization.md"

RUN335A_CONTRACT = RUN335A_DIR / "next_materialization_contract.csv"
RUN335A_PROTOCOL = RUN335A_DIR / "research_protocol_queue.csv"
RUN335A_NEGATIVE = RUN335A_DIR / "negative_control_plan.csv"
RUN335A_TIER_CONTRACT = RUN335A_DIR / "split_and_tier_reporting_contract.csv"
RUN335A_RUNTIME_BRIDGE = RUN335A_DIR / "runtime_parity_requirement_bridge.csv"
RUN335A_NO_RETUNE = RUN335A_DIR / "anti_overfit_design_receipt.json"

RUN332B_REFRESH_MANIFEST = RUN332B_DIR / "raw_refresh_probe_manifest.json"
RUN332B_REFRESH_CSV = RUN332B_DIR / "raw_refresh_probe" / "US100" / "bars_us100_m5_mt5api_raw.csv"
RUN330E_FEATURE_MANIFEST = RUN330E_DIR / "raw_forward_feature_matrix_manifest.csv"


AXIS_SOURCE_FILES: dict[str, list[tuple[str, str, Path]]] = {
    "cost_stress": [
        ("run335A_materialization_contract", "stage335A contract", RUN335A_CONTRACT),
        ("run334G_axis_failure_heatmap", "axis failure heatmap", RUN334G_DIR / "axis_failure_heatmap.csv"),
        ("run334F_cost_stress_diagnostics", "fixed no-retune cost diagnostic views", RUN334F_DIR / "diagnostic_views" / "cost_stress_diagnostic_views.csv"),
        ("run330F_cost_stress_report", "raw-forward cost stress report", RUN330F_DIR / "cost_stress_report.csv"),
    ],
    "curve_pocket": [
        ("run335A_materialization_contract", "stage335A contract", RUN335A_CONTRACT),
        ("run334G_axis_failure_heatmap", "axis failure heatmap", RUN334G_DIR / "axis_failure_heatmap.csv"),
        ("run334F_curve_pocket_diagnostics", "fixed no-retune curve diagnostic views", RUN334F_DIR / "diagnostic_views" / "curve_pocket_diagnostic_views.csv"),
        ("run330F_curve_pocket_report", "raw-forward curve pocket report", RUN330F_DIR / "curve_pocket_report.csv"),
        ("run330F_underwater_stretch_report", "raw-forward underwater stretch report", RUN330F_DIR / "underwater_stretch_report.csv"),
    ],
    "direction": [
        ("run335A_materialization_contract", "stage335A contract", RUN335A_CONTRACT),
        ("run334G_axis_failure_heatmap", "axis failure heatmap", RUN334G_DIR / "axis_failure_heatmap.csv"),
        ("run334F_direction_diagnostics", "fixed no-retune direction diagnostic views", RUN334F_DIR / "diagnostic_views" / "direction_diagnostic_views.csv"),
        ("run330F_long_short_attribution_report", "raw-forward long/short attribution report", RUN330F_DIR / "long_short_attribution_report.csv"),
    ],
    "drawdown_shape": [
        ("run335A_materialization_contract", "stage335A contract", RUN335A_CONTRACT),
        ("run334G_axis_failure_heatmap", "axis failure heatmap", RUN334G_DIR / "axis_failure_heatmap.csv"),
        ("run334F_underwater_diagnostics", "fixed no-retune underwater diagnostic views", RUN334F_DIR / "diagnostic_views" / "underwater_diagnostic_views.csv"),
        ("run330F_underwater_stretch_report", "raw-forward underwater stretch report", RUN330F_DIR / "underwater_stretch_report.csv"),
        ("run330F_curve_pocket_report", "raw-forward curve pocket report", RUN330F_DIR / "curve_pocket_report.csv"),
    ],
    "regime_slice": [
        ("run335A_materialization_contract", "stage335A contract", RUN335A_CONTRACT),
        ("run334G_axis_failure_heatmap", "axis failure heatmap", RUN334G_DIR / "axis_failure_heatmap.csv"),
        ("run334F_regime_slice_diagnostics", "fixed no-retune regime diagnostic views", RUN334F_DIR / "diagnostic_views" / "regime_slice_diagnostic_views.csv"),
        ("run330F_regime_attribution_report", "raw-forward regime attribution report", RUN330F_DIR / "regime_attribution_report.csv"),
        (
            "run330F_session_hour_month_regime_slices",
            "raw-forward session/hour/month/volatility/ADX/VIX/USD/rate slices",
            RUN330F_DIR / "session_hour_month_volatility_adx_vix_usd_rate_slices.csv",
        ),
    ],
    "runtime_parity": [
        ("run335A_runtime_parity_bridge", "stage335A runtime bridge", RUN335A_RUNTIME_BRIDGE),
        ("run334G_runtime_identity_review", "runtime identity review", RUN334G_DIR / "runtime_identity_review.csv"),
        ("run334F_runtime_identity_diagnostics", "fixed no-retune runtime identity diagnostics", RUN334F_DIR / "diagnostic_views" / "runtime_identity_diagnostic_views.csv"),
        ("run334B_source_authority_gate", "subject-separated source authority gate", RUN334B_DIR / "source_authority_gate_receipt.csv"),
        ("run334B_runtime_parity_receipt", "subject-separated runtime parity receipt", RUN334B_DIR / "runtime_parity_receipt.json"),
    ],
    "cp322a_exact_forward_handoff_missing": [
        ("run335A_materialization_contract", "stage335A contract", RUN335A_CONTRACT),
        ("run334H_failure_memory_handoff", "stage334 to stage335 failure handoff", RUN334H_DIR / "stage334_to_stage335_failure_memory_handoff.csv"),
        ("run334B_cp322a_identity_audit_manifest", "cp322A preserved identity audit manifest", RUN334B_DIR / "subject_packages" / "cp322a_preserved_identity_audit_manifest.json"),
        ("run329H_route_signal_coverage_audit", "cp322A exact route-signal coverage audit", RUN329H_DIR / "route_signal_coverage_audit.csv"),
        ("run329H_exact_handoff_feasibility_matrix", "cp322A exact handoff feasibility matrix", RUN329H_DIR / "exact_handoff_repair_feasibility_matrix.csv"),
    ],
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
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return None
    return value


def csv_value(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return ""
        return round(value, 10)
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    return value


def sha256_file(path: Path) -> str:
    if not path_exists(path):
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


def replace_prefix_line(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def insert_after_line_once(text: str, marker: str, insertion: str, token: str) -> str:
    if token in text:
        return text
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.strip() == marker:
            lines[index + 1 : index + 1] = insertion.strip("\n").splitlines()
            return "\n".join(lines) + "\n"
    return insertion.strip() + "\n" + text.rstrip() + "\n"


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


def parse_json_list(value: str) -> list[str]:
    if not value:
        return []
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        return [value]
    if isinstance(parsed, list):
        return [str(item) for item in parsed]
    return [str(parsed)]


def infer_artifact_type(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return "csv_table"
    if suffix == ".json":
        return "json_manifest_or_receipt"
    if suffix == ".md":
        return "markdown_report"
    if suffix == ".onnx":
        return "onnx_model"
    return suffix.lstrip(".") or "unknown"


def parse_timestamp(value: str) -> str:
    if not value:
        return ""
    text = str(value).strip()
    if not text:
        return ""
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        if text.isdigit():
            return datetime.fromtimestamp(int(text), tz=UTC).isoformat()
        parsed = datetime.fromisoformat(text)
        if parsed.tzinfo is None:
            return parsed.isoformat()
        return parsed.astimezone(UTC).isoformat()
    except Exception:
        return str(value)


def csv_profile(path: Path) -> dict[str, Any]:
    if not path_exists(path):
        return {
            "row_count": 0,
            "first_timestamp": "",
            "last_timestamp": "",
            "duplicate_key_count": "",
            "missing_or_duplicate_check": "blocked_missing_file",
        }
    rows = read_csv_rows(path)
    if not rows:
        return {
            "row_count": 0,
            "first_timestamp": "",
            "last_timestamp": "",
            "duplicate_key_count": 0,
            "missing_or_duplicate_check": "passed_empty_table_is_explicit",
        }
    fieldnames = list(rows[0].keys())
    time_columns = [
        "timestamp_utc",
        "timestamp",
        "bar_time_server",
        "first_timestamp",
        "last_timestamp",
        "time_open_unix",
        "time_close_unix",
    ]
    selected_time = next((column for column in time_columns if column in fieldnames), "")
    timestamps = [parse_timestamp(row.get(selected_time, "")) for row in rows] if selected_time else []
    timestamps = [value for value in timestamps if value]
    key_column = selected_time or fieldnames[0]
    keys = [str(row.get(key_column, "")) for row in rows]
    duplicate_count = len(keys) - len(set(keys))
    return {
        "row_count": len(rows),
        "first_timestamp": min(timestamps) if timestamps else "",
        "last_timestamp": max(timestamps) if timestamps else "",
        "duplicate_key_count": duplicate_count,
        "missing_or_duplicate_check": "passed_no_duplicate_key" if duplicate_count == 0 else "warning_duplicate_key_rows_present",
    }


def json_profile(path: Path) -> dict[str, Any]:
    if not path_exists(path):
        return {
            "row_count": 0,
            "first_timestamp": "",
            "last_timestamp": "",
            "duplicate_key_count": "",
            "missing_or_duplicate_check": "blocked_missing_file",
        }
    payload = read_json(path)
    if isinstance(payload, list):
        row_count = len(payload)
    elif isinstance(payload, dict):
        row_count = int(payload.get("row_count", 1))
    else:
        row_count = 1
    first_timestamp = ""
    last_timestamp = ""
    if isinstance(payload, dict):
        first_timestamp = parse_timestamp(str(payload.get("first_timestamp", payload.get("resolved_first_open_unix", ""))))
        last_timestamp = parse_timestamp(str(payload.get("last_timestamp", payload.get("resolved_last_open_unix", ""))))
    return {
        "row_count": row_count,
        "first_timestamp": first_timestamp,
        "last_timestamp": last_timestamp,
        "duplicate_key_count": "",
        "missing_or_duplicate_check": "passed_json_manifest_loaded",
    }


def artifact_profile(path: Path) -> dict[str, Any]:
    exists = path_exists(path)
    profile = {
        "row_count": 0,
        "first_timestamp": "",
        "last_timestamp": "",
        "duplicate_key_count": "",
        "missing_or_duplicate_check": "blocked_missing_file",
    }
    if exists and path.suffix.lower() == ".csv":
        profile = csv_profile(path)
    elif exists and path.suffix.lower() == ".json":
        profile = json_profile(path)
    elif exists:
        profile = {
            "row_count": 1,
            "first_timestamp": "",
            "last_timestamp": "",
            "duplicate_key_count": "",
            "missing_or_duplicate_check": "passed_file_exists_not_tabular",
        }
    return {
        "path": rel(path),
        "exists": exists,
        "artifact_type": infer_artifact_type(path),
        "sha256": sha256_file(path),
        **profile,
    }


def load_inputs() -> dict[str, Any]:
    return {
        "materialization_contract": read_csv_rows(RUN335A_CONTRACT),
        "protocol_queue": read_csv_rows(RUN335A_PROTOCOL),
        "negative_plan": read_csv_rows(RUN335A_NEGATIVE),
        "tier_contract": read_csv_rows(RUN335A_TIER_CONTRACT),
        "runtime_bridge": read_csv_rows(RUN335A_RUNTIME_BRIDGE),
        "no_retune_receipt": read_json(RUN335A_NO_RETUNE),
        "feature_manifest": read_csv_rows(RUN330E_FEATURE_MANIFEST),
        "refresh_manifest": read_json(RUN332B_REFRESH_MANIFEST),
    }


def build_source_index() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for axis, sources in AXIS_SOURCE_FILES.items():
        for source_id, role, path in sources:
            key = (axis, source_id)
            if key in seen:
                continue
            seen.add(key)
            profile = artifact_profile(path)
            rows.append(
                {
                    "failure_axis": axis,
                    "source_id": source_id,
                    "source_role": role,
                    **profile,
                    "time_axis_statement": (
                        "Source rows are review/manifest evidence. Any future score frame must use FPMarkets v2 "
                        "broker-clock close key and the session mapper before session features."
                    ),
                    "feature_label_boundary_statement": (
                        "This source may constrain future protocol design only; it does not create labels, "
                        "change features, or tune thresholds."
                    ),
                    "split_boundary": "post-2026-04-14 forward evidence is separate from train/validation/OOS freeze through 2026-04-13",
                    "leakage_risk": "post-hoc axis memory can overfit if reused as direct date/hour/regime exclusion",
                    "integrity_judgment": "usable_with_boundary" if profile["exists"] else "blocked_missing_source_file",
                }
            )
    return rows


def build_latest_forward_data_inventory(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    refresh_profile = artifact_profile(RUN332B_REFRESH_CSV)
    refresh_manifest = inputs["refresh_manifest"] if isinstance(inputs["refresh_manifest"], dict) else {}
    rows.append(
        {
            "data_source_id": "run332B_raw_refresh_probe_us100_m5",
            "path": rel(RUN332B_REFRESH_CSV),
            "exists": refresh_profile["exists"],
            "rows": refresh_profile["row_count"],
            "first_timestamp": refresh_profile["first_timestamp"] or refresh_manifest.get("first_timestamp", ""),
            "last_timestamp": refresh_profile["last_timestamp"] or refresh_manifest.get("last_timestamp", ""),
            "sha256": refresh_profile["sha256"],
            "source_manifest": rel(RUN332B_REFRESH_MANIFEST),
            "source_manifest_sha256": sha256_file(RUN332B_REFRESH_MANIFEST),
            "coverage_role": "latest_raw_forward_refresh_probe",
            "data_integrity_boundary": (
                "usable_with_manifest_repair_boundary; not enough alone for Forward Passed/Failed"
                if refresh_profile["exists"]
                else "blocked_missing_raw_refresh_probe"
            ),
        }
    )
    for feature in inputs["feature_manifest"]:
        matrix_path = ROOT / str(feature.get("feature_matrix_path", ""))
        profile = artifact_profile(matrix_path)
        rows.append(
            {
                "data_source_id": f"run330E_feature_matrix_{feature.get('artifact_slug', '')}",
                "path": rel(matrix_path),
                "exists": profile["exists"],
                "rows": profile["row_count"],
                "first_timestamp": profile["first_timestamp"] or feature.get("first_timestamp", ""),
                "last_timestamp": profile["last_timestamp"] or feature.get("last_timestamp", ""),
                "sha256": profile["sha256"],
                "source_manifest": rel(RUN330E_FEATURE_MANIFEST),
                "source_manifest_sha256": sha256_file(RUN330E_FEATURE_MANIFEST),
                "coverage_role": "existing_raw_forward_feature_frame_identity",
                "data_integrity_boundary": (
                    "usable_existing_forward_feature_frame_identity"
                    if profile["exists"] and str(feature.get("feature_matrix_sha256", "")) == profile["sha256"]
                    else "warning_or_blocked_feature_identity_mismatch"
                ),
            }
        )
    return rows


def protocol_by_axis(protocol_rows: Sequence[Mapping[str, str]]) -> dict[str, Mapping[str, str]]:
    return {str(row.get("failure_axis", "")): row for row in protocol_rows}


def negative_by_axis(negative_rows: Sequence[Mapping[str, str]]) -> dict[str, Mapping[str, str]]:
    return {str(row.get("failure_axis", "")): row for row in negative_rows}


def source_ids_for_axis(source_rows: Sequence[Mapping[str, Any]], axis: str) -> list[str]:
    return [str(row["source_id"]) for row in source_rows if row["failure_axis"] == axis]


def source_missing_for_axis(source_rows: Sequence[Mapping[str, Any]], axis: str) -> int:
    return sum(1 for row in source_rows if row["failure_axis"] == axis and not row["exists"])


def build_guard_input_manifest(inputs: Mapping[str, Any], source_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    protocols = protocol_by_axis(inputs["protocol_queue"])
    negatives = negative_by_axis(inputs["negative_plan"])
    rows: list[dict[str, Any]] = []
    for contract in inputs["materialization_contract"]:
        axis = str(contract.get("failure_axis", ""))
        materialization_id = str(contract.get("materialization_id", ""))
        protocol = protocols.get(axis, {})
        negative = negatives.get(axis, {})
        minimum = parse_json_list(str(contract.get("minimum_artifacts", "")))
        source_ids = source_ids_for_axis(source_rows, axis)
        missing_count = source_missing_for_axis(source_rows, axis)
        rows.append(
            {
                "materialization_id": materialization_id,
                "failure_axis": axis,
                "required_inputs": contract.get("required_inputs", ""),
                "source_file_index": source_ids,
                "source_file_count": len(source_ids),
                "source_missing_count": missing_count,
                "minimum_artifacts": minimum,
                "row_count_or_hash": "hash_and_row_count_recorded_in_source_file_index",
                "time_axis_statement": "future scoring must use fixed FPMarkets v2 time-axis policy; this run creates no score rows",
                "feature_label_boundary_statement": "guard input only; no feature, label, threshold, lot, model, or decision surface change",
                "missing_duplicate_check": "recorded_per_source_file; blocks if source_missing_count_gt_0",
                "forbidden_repair_check": "passed_no_threshold_lot_direct_pocket_date_hour_side_pruning",
                "negative_control_id": negative.get("control_id", ""),
                "next_probe": protocol.get("next_probe", ""),
                "allowed_output": contract.get("allowed_output", ""),
                "forbidden_output": contract.get("forbidden_output", ""),
                "guard_input_status": "materialized_ready_with_boundary" if missing_count == 0 else "blocked_missing_source",
                "decision_use": protocol.get("decision_use", ""),
            }
        )
    return rows


def build_axis_guard_requirements(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for protocol in inputs["protocol_queue"]:
        axis = str(protocol.get("failure_axis", ""))
        rows.append(
            {
                "failure_axis": axis,
                "hypothesis": f"{axis} can guide a timestamp-safe research branch without direct forward-pocket fitting.",
                "decision_use": protocol.get("decision_use", ""),
                "comparison_baseline": protocol.get("comparison_baseline", ""),
                "control_variables": protocol.get("control_variables", ""),
                "changed_variables_allowed": protocol.get("changed_variables_allowed", ""),
                "changed_variables_forbidden": protocol.get("changed_variables_forbidden", ""),
                "sample_scope": protocol.get("sample_scope", ""),
                "success_criteria": protocol.get("success_criteria", ""),
                "failure_criteria": protocol.get("failure_criteria", ""),
                "invalid_conditions": protocol.get("invalid_conditions", ""),
                "stop_conditions": protocol.get("stop_conditions", ""),
                "evidence_plan": protocol.get("evidence_plan", ""),
                "materialized_by": RUN_ID,
            }
        )
    return rows


def build_forbidden_repair_check(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    forbidden_rules = [
        ("model_training", "no new model training in run335B"),
        ("threshold_retuning", "no threshold search or calibration from Stage334/335 results"),
        ("lot_optimization", "no lot or risk optimization from failure memory"),
        ("direct_forward_pocket_filtering", "no direct date/hour/month/regime exclusion copied from failure pockets"),
        ("side_drop_or_side_threshold", "no dropping long/short side after seeing direction failure"),
        ("runtime_authority_claim", "no runtime authority without MT5 tester output and telemetry"),
        ("subject_swap", "cp322A exact cannot consume run333E or non-identity evidence as exact handoff"),
    ]
    axes = [str(row.get("failure_axis", "")) for row in inputs["materialization_contract"]]
    rows: list[dict[str, Any]] = []
    for axis in axes:
        for rule_id, rule_text in forbidden_rules:
            rows.append(
                {
                    "failure_axis": axis,
                    "forbidden_rule_id": rule_id,
                    "forbidden_rule": rule_text,
                    "check_status": "passed_for_run335B_manifest_only",
                    "effect": "run335B creates guard inputs only and cannot be used as candidate evidence",
                }
            )
    return rows


def build_fixed_control_lock_manifest() -> list[dict[str, Any]]:
    controls = [
        ("selected_candidate", "none", "selection remains none"),
        ("model_family", "unchanged", "no ONNX or model file is created"),
        ("feature_order", "unchanged", "future branch must declare feature order before scoring"),
        ("threshold_policy", "fixed_until_predeclared", "no threshold retuning in run335B"),
        ("risk_lot_logic", "fixed_until_predeclared", "no lot/risk optimization in run335B"),
        ("split_boundary", "old OOS through 2026-04-13; forward after 2026-04-14", "no random shuffle or pocket-specific split"),
        ("tier_reporting", "Tier A separate + Tier B separate + Tier A+B combined", "all later KPI rows must preserve paired tier views or record missing_required"),
        ("runtime_handoff", "identity required before runtime claim", "compile-only or Python-only parity cannot become authority"),
    ]
    return [
        {
            "control_id": control_id,
            "locked_value": locked_value,
            "effect": effect,
            "lock_status": "locked_for_run335B",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for control_id, locked_value, effect in controls
    ]


def build_tier_view_guard_matrix(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    axes = [str(row.get("failure_axis", "")) for row in inputs["materialization_contract"]]
    for axis in axes:
        for tier in inputs["tier_contract"]:
            rows.append(
                {
                    "failure_axis": axis,
                    "view": tier.get("view", ""),
                    "required": tier.get("required", ""),
                    "meaning": tier.get("meaning", ""),
                    "kpi_scope": tier.get("kpi_scope", ""),
                    "missing_policy": tier.get("missing_policy", ""),
                    "materialized_status": "required_for_future_scoring_or_runtime",
                }
            )
    return rows


def build_negative_control_guard_inputs(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in inputs["negative_plan"]:
        rows.append(
            {
                **row,
                "materialized_status": "required_for_next_branch_design",
                "pass_condition": "target thesis must separate from shuffle/adjacent/state-neutral control before candidate claim",
                "fail_condition": "if negative control improves similarly, downgrade branch to overfit memory",
            }
        )
    return rows


def build_runtime_handoff_requirement_inventory(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in inputs["runtime_bridge"]:
        rows.append(
            {
                **row,
                "source_status": "materialized_requirement_only",
                "runtime_claim_boundary": "not_applicable_until_mt5_tester_output_and_telemetry_exist",
                "run335B_effect": "keeps future runtime branch from becoming compile-only or Python-only authority",
            }
        )
    rows.append(
        {
            "requirement": "cp322a_exact_subject_boundary",
            "required_before": "any cp322A exact Forward Passed/Failed claim",
            "evidence": (
                "genuine post-2026-04-14 route-signal source; source_authority_gate="
                f"{rel(RUN334B_DIR / 'source_authority_gate_receipt.csv')}"
            ),
            "forbidden_shortcut": "run333E bridge or non-identity evidence treated as cp322A exact handoff",
            "source_status": "materialized_boundary_memory",
            "runtime_claim_boundary": "cp322A exact remains blocked unless exact handoff is proven",
            "run335B_effect": "prevents subject swap from run333E or non-identity packages",
        }
    )
    return rows


def build_gate_audit(
    source_rows: Sequence[Mapping[str, Any]],
    guard_rows: Sequence[Mapping[str, Any]],
    tier_rows: Sequence[Mapping[str, Any]],
    latest_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    source_missing = sum(1 for row in source_rows if not row["exists"])
    guard_blocked = sum(1 for row in guard_rows if str(row["guard_input_status"]).startswith("blocked"))
    refresh_exists = any(row["data_source_id"] == "run332B_raw_refresh_probe_us100_m5" and row["exists"] for row in latest_rows)
    feature_identity_rows = [row for row in latest_rows if str(row["data_source_id"]).startswith("run330E_feature_matrix_")]
    feature_identity_ok = all("usable_existing" in str(row["data_integrity_boundary"]) for row in feature_identity_rows)
    return [
        {
            "gate": "source_artifact_presence",
            "status": "passed" if source_missing == 0 else "failed",
            "evidence_path": rel(RUN_DIR / "source_file_index.csv"),
            "detail": f"missing_source_files={source_missing}",
        },
        {
            "gate": "materialization_contract_coverage",
            "status": "passed" if len(guard_rows) == 7 and guard_blocked == 0 else "failed",
            "evidence_path": rel(RUN_DIR / "guard_input_manifest.csv"),
            "detail": f"guard_rows={len(guard_rows)};blocked_rows={guard_blocked}",
        },
        {
            "gate": "latest_forward_data_boundary",
            "status": "passed_with_boundary" if refresh_exists and feature_identity_ok else "failed",
            "evidence_path": rel(RUN_DIR / "latest_forward_data_inventory.csv"),
            "detail": "raw refresh and existing forward feature identities are recorded; no Forward Passed/Failed claim",
        },
        {
            "gate": "paired_tier_contract",
            "status": "passed" if len(tier_rows) == 21 else "failed",
            "evidence_path": rel(RUN_DIR / "tier_view_guard_matrix.csv"),
            "detail": f"tier_rows={len(tier_rows)}",
        },
        {
            "gate": "forbidden_repair_guard",
            "status": "passed",
            "evidence_path": rel(RUN_DIR / "forbidden_repair_check.csv"),
            "detail": "threshold/lot/direct pocket/subject swap/runtime authority repairs are blocked",
        },
        {
            "gate": "runtime_claim_guard",
            "status": "passed",
            "evidence_path": rel(RUN_DIR / "runtime_handoff_requirement_inventory.csv"),
            "detail": "runtime requirements materialized; runtime authority not claimed",
        },
        {
            "gate": "final_claim_guard",
            "status": "passed",
            "evidence_path": rel(RUN_DIR / "result_judgment.csv"),
            "detail": "no candidate, no Forward Passed/Failed, no Goal Achieve",
        },
    ]


def build_receipts(
    source_rows: Sequence[Mapping[str, Any]],
    guard_rows: Sequence[Mapping[str, Any]],
    latest_rows: Sequence[Mapping[str, Any]],
    gate_rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    source_hashes = {str(row["path"]): row["sha256"] for row in source_rows}
    missing_sources = [row for row in source_rows if not row["exists"]]
    latest_feature_rows = [row for row in latest_rows if str(row["data_source_id"]).startswith("run330E_feature_matrix_")]
    receipts: dict[str, Any] = {}
    receipts["data_integrity_receipt"] = {
        "data_source": [
            "Stage334 failure-memory review artifacts",
            "Stage330E raw-forward feature matrix identities",
            "Stage332B raw refresh probe",
        ],
        "time_axis": (
            "Materialized artifacts are review/manifest rows. Future scoring must use FPMarkets v2 broker-clock "
            "close key plus event UTC/session mapper; run335B creates no new feature or label rows."
        ),
        "sample_scope": "US100 M5 forward research guard inputs after existing OOS boundary 2026-04-13; no new candidate sample fitted",
        "missing_or_duplicate_check": f"source_missing={len(missing_sources)}; guard_rows={len(guard_rows)}; feature_identity_rows={len(latest_feature_rows)}",
        "feature_label_boundary": "no labels, features, thresholds, lots, stops, targets, or model scores are changed",
        "split_boundary": "train/validation/OOS freeze remains through 2026-04-13; post-2026-04-14 remains forward research evidence",
        "leakage_risk": "failure memory could become leakage if copied into direct calendar/regime/pocket filters",
        "data_hash_or_identity": source_hashes,
        "integrity_judgment": "usable_with_boundary" if not missing_sources else "blocked_missing_source",
    }
    receipts["model_validation_receipt"] = {
        "model_family": "none_created_in_run335B; cp322A and non-identity memories are source artifacts only",
        "target_and_label": "not_applicable_manifest_only",
        "split_method": "fixed historical OOS boundary plus forward research evidence boundary",
        "selection_metric": "none; no candidate selection",
        "secondary_metrics": "future protocols must carry cost, curve, direction, drawdown, regime, tier, and runtime identity guards",
        "threshold_policy": "fixed/no_retune; threshold search forbidden",
        "overfit_risk": "post-hoc failure axes can overfit if used as direct forward filters",
        "calibration_risk": "not_applicable_no_scores",
        "comparison_baseline": "Stage334 failure memory, Stage330F raw-forward reports, Stage334B subject boundary, Stage329H cp322A exact block",
        "validation_judgment": "exploratory_guard_inputs_materialized_no_candidate",
    }
    receipts["runtime_parity_receipt"] = {
        "research_path": rel(Path(__file__)),
        "runtime_path": "not_touched_in_run335B",
        "shared_contract": "future runtime branch must declare feature order, model hash, threshold, handoff, tester output, and telemetry",
        "known_differences": "run335B is manifest-only; it cannot prove MT5 runtime behavior",
        "parity_check": "requirements inventory only; no MetaEditor compile, Strategy Tester, or runtime output",
        "parity_identity": {
            "runtime_requirement_inventory": rel(RUN_DIR / "runtime_handoff_requirement_inventory.csv"),
            "source_hashes": source_hashes,
        },
        "runtime_claim_boundary": "research_only_no_runtime_authority",
    }
    receipts["result_judgment_receipt"] = {
        "result_subject": RUN_ID,
        "evidence_available": [
            rel(RUN_DIR / "guard_input_manifest.csv"),
            rel(RUN_DIR / "source_file_index.csv"),
            rel(RUN_DIR / "required_gate_coverage_audit.csv"),
        ],
        "evidence_missing": "no model scores, no MT5 tester result, no forward pass/fail KPI",
        "judgment_label": "exploratory",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_RUN_ID,
        "user_explanation_hook": "Guard inputs are ready, but this is not a profitable candidate or runtime claim.",
    }
    receipts["artifact_lineage_receipt"] = {
        "source_inputs": sorted(source_hashes),
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [],
        "artifact_hashes": {},
        "registry_links": [
            rel(RUN_REGISTRY),
            rel(ALPHA_LEDGER),
            rel(STAGE_LEDGER),
            rel(ARTIFACT_REGISTRY),
        ],
        "availability": "tracked_after_commit",
        "lineage_judgment": "connected_with_boundary",
    }
    receipts["anti_overfit_materialization_receipt"] = {
        "forbidden_repairs": [
            "model_training",
            "threshold_retuning",
            "lot_optimization",
            "direct_forward_pocket_filtering",
            "date_hour_side_pruning_from_failure_memory",
            "runtime_authority_claim",
            "subject_swap",
        ],
        "guard_status": "passed_manifest_only",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    receipts["gate_receipt"] = {
        "required_gates": gate_rows,
        "failed_gates": [row for row in gate_rows if str(row["status"]).startswith("failed")],
    }
    return receipts


def build_report_text(
    source_rows: Sequence[Mapping[str, Any]],
    guard_rows: Sequence[Mapping[str, Any]],
    latest_rows: Sequence[Mapping[str, Any]],
    gate_rows: Sequence[Mapping[str, Any]],
) -> str:
    axis_list = ", ".join(row["failure_axis"] for row in guard_rows)
    failed_gates = [row for row in gate_rows if str(row["status"]).startswith("failed")]
    latest_refresh = next((row for row in latest_rows if row["data_source_id"] == "run332B_raw_refresh_probe_us100_m5"), {})
    return f"""# run335B Failure-Memory Guard Input Materialization(335B 실패 기억 방어 입력 실체화)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- source_axes(원천 축): `{axis_list}`
- source_file_rows(원천 파일 행): `{len(source_rows)}`
- guard_input_rows(방어 입력 행): `{len(guard_rows)}`
- latest_raw_refresh(최신 원본 갱신): `{latest_refresh.get("last_timestamp", "")}` / rows `{latest_refresh.get("rows", "")}`
- failed_gates(실패 게이트): `{len(failed_gates)}`
- next_action(다음 행동): `{NEXT_RUN_ID}`

Effect(효과): Stage334(334단계)의 실패 기억을 다음 연구가 소비할 수 있는 hash/row/source/gate(해시/행/원천/게이트) 입력으로 만들었다. 모델 학습(model training, 모델 학습), threshold retuning(임계값 재조정), lot optimization(로트 최적화), direct forward pocket filtering(직접 전진 포켓 필터링)은 하지 않았다.

Boundary(경계): selected candidate(선택 후보), Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 모두 `not_claimed`다.
"""


def build_decision_text() -> str:
    return f"""# Stage335B Decision(335B 결정)

`{RUN_ID}`는 failure memory guard inputs(실패 기억 방어 입력)를 materialized(실체화)했다.

- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Effect(효과): 다음 branch design(분기 설계)은 7개 실패 축을 직접 필터로 쓰지 않고, source/hash/tier/negative-control/runtime requirement(원천/해시/티어/부정 대조/런타임 요구)로 들고 가야 한다.
"""


def update_state_docs() -> list[Path]:
    changed: list[Path] = []
    selection_path = SELECTED_DIR / "selection_status.md"
    text, had_bom = read_text_lossless(selection_path)
    text = replace_prefix_line(text, "- latest_design(최신 설계):", "- latest_design(최신 설계): `run335A_design_failure_memory_constrained_research_packet_v1`")
    text = replace_prefix_line(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    text = replace_prefix_line(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_RUN_ID}`")
    text = replace_prefix_line(
        text,
        "- effect(효과):",
        "- effect(효과): Stage335B(335B 실행)는 실패 기억 guard inputs(방어 입력)를 materialized(실체화)했지만, 아직 모델 학습(model training, 모델 학습)이나 후보 선택(candidate selection, 후보 선택)은 없다.",
    )
    changed.append(write_text_lossless(selection_path, text, had_bom))

    stage_brief_path = STAGE_BRIEF
    text, had_bom = read_text_lossless(stage_brief_path)
    text = replace_prefix_line(text, "- status(상태):", "- status(상태): `open_active`")
    text = replace_prefix_line(text, "- latest_run(최신 실행):", f"- latest_run(최신 실행): `{RUN_ID}`")
    changed.append(write_text_lossless(stage_brief_path, text, had_bom))

    input_refs_path = INPUTS_DIR / "input_refs.md"
    changed.append(
        append_section_once(
            input_refs_path,
            "## run335B Guard Input Materialization(335B 방어 입력 실체화)",
            f"""- guard_input_manifest(방어 입력 목록): `{rel(RUN_DIR / "guard_input_manifest.csv")}`
- source_file_index(원천 파일 색인): `{rel(RUN_DIR / "source_file_index.csv")}`
- latest_forward_data_inventory(최신 전진 데이터 목록): `{rel(RUN_DIR / "latest_forward_data_inventory.csv")}`
- runtime_handoff_requirement_inventory(런타임 인계 요구 목록): `{rel(RUN_DIR / "runtime_handoff_requirement_inventory.csv")}`
- decision(결정): `{rel(DECISION_DOC)}`""",
        )
    )

    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_prefix_line(workspace_text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    focus_line = (
        "- >-\n"
        f"  Stage335(335단계) run335B(335B 실행)는 `{STATUS}`로 failure memory guard inputs(실패 기억 방어 입력)를 materialized(실체화)했다. "
        "Effect(효과): 7개 실패 축을 source/hash/tier/negative-control/runtime requirement(원천/해시/티어/부정 대조/런타임 요구) 입력으로 고정하고 Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    workspace_text = insert_after_line_once(workspace_text, "current_focus:", focus_line, "run335B(335B 실행)")
    changed.append(write_text_lossless(WORKSPACE_STATE, workspace_text, workspace_bom))

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    current_text = replace_prefix_line(current_text, "- current_packet(현재 작업 묶음):", "- current_packet(현재 작업 묶음): `335_overfit_guard__failure_memory_constrained_research_handoff_v3`")
    current_text = replace_prefix_line(current_text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    current_text = replace_prefix_line(current_text, "- status(상태):", f"- status(상태): `{STATUS}`")
    current_text = replace_prefix_line(current_text, "- decision(판정):", f"- decision(판정): `{DECISION}`")
    current_text = remove_lines_containing(current_text, "run335B_summary(335B 요약)")
    summary = (
        f"- run335B_summary(335B 요약): failure memory guard input materialization(실패 기억 방어 입력 실체화)을 `{STATUS}`로 완료했다. "
        "Effect(효과): 7개 실패 축의 source/hash/row/tier/negative-control/runtime requirement(원천/해시/행/티어/부정 대조/런타임 요구)을 만들었고, 선택 후보나 Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    current_text = insert_after_prefix_once(current_text, "- decision(판정):", summary, "run335B_summary")
    changed.append(write_text_lossless(CURRENT_STATE, current_text, current_bom))

    changed.append(
        append_section_once(
            CHANGELOG,
            "## 2026-05-26 Stage335B Guard Input Materialization(335B 방어 입력 실체화)",
            f"""- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- effect(효과): 7개 실패 기억 축을 다음 branch design(분기 설계)의 고정 guard input(방어 입력)으로 물질화했다.
- boundary(경계): no candidate(후보 없음), no Forward Passed/Failed(전진 통과/실패 없음), no Goal Achieve(목표 달성 없음).""",
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
                    "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
                }
            ],
        )
    )
    ledger_row = {
        "ledger_row_id": f"{RUN_ID}__guard_input_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "failure_memory_guard_input_materialization",
        "tier_scope": "paired_tier_required_by_contract",
        "kpi_scope": "manifest_only_no_new_trading_kpi",
        "scoreboard_lane": "experiment_execution",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(report_path),
        "primary_kpi": "guard_input_rows=7;source_file_rows=33;tier_rows=21",
        "guardrail_kpi": "no_model_training;no_threshold_retuning;no_lot_optimization;goal_achieve_not_claimed",
        "external_verification_status": "out_of_scope_by_claim_manifest_only",
        "notes": f"decision={DECISION};next_action={NEXT_RUN_ID}.",
    }
    changed.append(upsert_csv(ALPHA_LEDGER, ["ledger_row_id"], [ledger_row]))
    changed.append(
        upsert_csv(
            STAGE_LEDGER,
            ["ledger_row_id"],
            [
                {
                    "ledger_row_id": f"{RUN_ID}__guard_input_materialization",
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "work_family": "experiment_execution",
                    "evidence_scope": "failure_memory_guard_input_materialization",
                    "kpi_scope": "manifest_only_no_new_trading_kpi",
                    "status": STATUS,
                    "judgment": JUDGMENT,
                    "claim_boundary": CLAIM_BOUNDARY,
                    "path": rel(report_path),
                    "notes": "no_candidate_selected;goal_achieve_not_claimed.",
                    "decision": DECISION,
                }
            ],
        )
    )
    artifact_rows = []
    created_at = utc_now()
    for output in outputs:
        artifact_rows.append(
            {
                "artifact_id": f"{RUN_ID}::{output.name}",
                "artifact_type": infer_artifact_type(output),
                "path": rel(output),
                "sha256": sha256_file(output),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": f"Stage335B guard input materialization artifact; claim_boundary={CLAIM_BOUNDARY}",
            }
        )
    changed.append(upsert_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows))
    return changed


def build_outputs() -> dict[str, Any]:
    inputs = load_inputs()
    source_rows = build_source_index()
    latest_rows = build_latest_forward_data_inventory(inputs)
    guard_rows = build_guard_input_manifest(inputs, source_rows)
    axis_rows = build_axis_guard_requirements(inputs)
    forbidden_rows = build_forbidden_repair_check(inputs)
    fixed_control_rows = build_fixed_control_lock_manifest()
    tier_rows = build_tier_view_guard_matrix(inputs)
    negative_rows = build_negative_control_guard_inputs(inputs)
    runtime_rows = build_runtime_handoff_requirement_inventory(inputs)
    gate_rows = build_gate_audit(source_rows, guard_rows, tier_rows, latest_rows)
    receipts = build_receipts(source_rows, guard_rows, latest_rows, gate_rows)
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
        "selected_candidate": "none",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return {
        "source_rows": source_rows,
        "latest_rows": latest_rows,
        "guard_rows": guard_rows,
        "axis_rows": axis_rows,
        "forbidden_rows": forbidden_rows,
        "fixed_control_rows": fixed_control_rows,
        "tier_rows": tier_rows,
        "negative_rows": negative_rows,
        "runtime_rows": runtime_rows,
        "gate_rows": gate_rows,
        "receipts": receipts,
        "result_rows": result_rows,
        "final_decision": final_decision,
    }


def main() -> int:
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    outputs = build_outputs()

    artifact_paths: list[Path] = [
        write_csv(
            RUN_DIR / "source_file_index.csv",
            [
                "failure_axis",
                "source_id",
                "source_role",
                "path",
                "exists",
                "artifact_type",
                "row_count",
                "sha256",
                "first_timestamp",
                "last_timestamp",
                "duplicate_key_count",
                "missing_or_duplicate_check",
                "time_axis_statement",
                "feature_label_boundary_statement",
                "split_boundary",
                "leakage_risk",
                "integrity_judgment",
            ],
            outputs["source_rows"],
        ),
        write_csv(
            RUN_DIR / "latest_forward_data_inventory.csv",
            [
                "data_source_id",
                "path",
                "exists",
                "rows",
                "first_timestamp",
                "last_timestamp",
                "sha256",
                "source_manifest",
                "source_manifest_sha256",
                "coverage_role",
                "data_integrity_boundary",
            ],
            outputs["latest_rows"],
        ),
        write_csv(
            RUN_DIR / "guard_input_manifest.csv",
            [
                "materialization_id",
                "failure_axis",
                "required_inputs",
                "source_file_index",
                "source_file_count",
                "source_missing_count",
                "minimum_artifacts",
                "row_count_or_hash",
                "time_axis_statement",
                "feature_label_boundary_statement",
                "missing_duplicate_check",
                "forbidden_repair_check",
                "negative_control_id",
                "next_probe",
                "allowed_output",
                "forbidden_output",
                "guard_input_status",
                "decision_use",
            ],
            outputs["guard_rows"],
        ),
        write_csv(
            RUN_DIR / "axis_guard_requirements.csv",
            [
                "failure_axis",
                "hypothesis",
                "decision_use",
                "comparison_baseline",
                "control_variables",
                "changed_variables_allowed",
                "changed_variables_forbidden",
                "sample_scope",
                "success_criteria",
                "failure_criteria",
                "invalid_conditions",
                "stop_conditions",
                "evidence_plan",
                "materialized_by",
            ],
            outputs["axis_rows"],
        ),
        write_csv(
            RUN_DIR / "forbidden_repair_check.csv",
            ["failure_axis", "forbidden_rule_id", "forbidden_rule", "check_status", "effect"],
            outputs["forbidden_rows"],
        ),
        write_csv(
            RUN_DIR / "fixed_control_lock_manifest.csv",
            ["control_id", "locked_value", "effect", "lock_status", "claim_boundary"],
            outputs["fixed_control_rows"],
        ),
        write_csv(
            RUN_DIR / "tier_view_guard_matrix.csv",
            ["failure_axis", "view", "required", "meaning", "kpi_scope", "missing_policy", "materialized_status"],
            outputs["tier_rows"],
        ),
        write_csv(
            RUN_DIR / "negative_control_guard_inputs.csv",
            [
                "control_id",
                "failure_axis",
                "control_purpose",
                "control_design",
                "must_fail_or_warn_if",
                "claim_effect",
                "materialized_status",
                "pass_condition",
                "fail_condition",
            ],
            outputs["negative_rows"],
        ),
        write_csv(
            RUN_DIR / "runtime_handoff_requirement_inventory.csv",
            list(outputs["runtime_rows"][0].keys()),
            outputs["runtime_rows"],
        ),
        write_csv(
            RUN_DIR / "required_gate_coverage_audit.csv",
            ["gate", "status", "evidence_path", "detail"],
            outputs["gate_rows"],
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
                "goal_achieve",
                "next_action",
                "claim_boundary",
            ],
            outputs["result_rows"],
        ),
        write_json(RUN_DIR / "data_integrity_receipt.json", outputs["receipts"]["data_integrity_receipt"]),
        write_json(RUN_DIR / "model_validation_receipt.json", outputs["receipts"]["model_validation_receipt"]),
        write_json(RUN_DIR / "runtime_parity_receipt.json", outputs["receipts"]["runtime_parity_receipt"]),
        write_json(RUN_DIR / "result_judgment_receipt.json", outputs["receipts"]["result_judgment_receipt"]),
        write_json(RUN_DIR / "anti_overfit_materialization_receipt.json", outputs["receipts"]["anti_overfit_materialization_receipt"]),
        write_json(RUN_DIR / "gate_receipt.json", outputs["receipts"]["gate_receipt"]),
        write_json(RUN_DIR / "final_materialization_decision.json", outputs["final_decision"]),
    ]

    manifest_path = RUN_DIR / "run_manifest.json"
    lineage_path = RUN_DIR / "artifact_lineage_receipt.json"
    run_manifest = {
        **outputs["final_decision"],
        "created_at_utc": utc_now(),
        "producer": rel(Path(__file__)),
        "source_inputs": [
            rel(RUN335A_CONTRACT),
            rel(RUN335A_PROTOCOL),
            rel(RUN335A_NEGATIVE),
            rel(RUN335A_TIER_CONTRACT),
            rel(RUN335A_RUNTIME_BRIDGE),
        ],
        "outputs": [rel(path) for path in [*artifact_paths, manifest_path, lineage_path]],
    }
    manifest_path = write_json(manifest_path, run_manifest)
    artifact_paths.append(manifest_path)

    lineage = outputs["receipts"]["artifact_lineage_receipt"]
    lineage["artifact_paths"] = [rel(path) for path in [*artifact_paths, lineage_path]]
    lineage["artifact_hashes"] = {rel(path): sha256_file(path) for path in artifact_paths}
    lineage_path = write_json(lineage_path, lineage)
    artifact_paths.append(lineage_path)

    report_path = write_md(
        REVIEWS_DIR / "run335B_failure_memory_guard_input_materialization.md",
        build_report_text(outputs["source_rows"], outputs["guard_rows"], outputs["latest_rows"], outputs["gate_rows"]),
    )
    artifact_paths.append(report_path)
    artifact_paths.append(write_md(DECISION_DOC, build_decision_text()))

    artifact_paths.extend(update_state_docs())
    artifact_paths.extend(update_registries(artifact_paths, report_path))

    summary = {
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "source_file_rows": len(outputs["source_rows"]),
        "guard_input_rows": len(outputs["guard_rows"]),
        "tier_rows": len(outputs["tier_rows"]),
        "failed_gates": len([row for row in outputs["gate_rows"] if str(row["status"]).startswith("failed")]),
        "selected_candidate": "none",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_RUN_ID,
        "artifact_count": len(artifact_paths),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
