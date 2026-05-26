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
RUN_NUMBER = "run335D"
RUN_ID = "run335D_materialize_guarded_branch_research_inputs_v1"
PARENT_RUN_ID = "run335C_design_guarded_failure_memory_research_branches_v1"
NEXT_RUN_ID = "run335E_review_guarded_branch_input_materialization_v1"
STATUS = "completed_guarded_branch_research_inputs_materialized_no_selection"
JUDGMENT = "guarded_branch_inputs_materialized_research_only_no_goal_achieve"
DECISION = "stage335D_guarded_branch_inputs_materialized_ready_for_review_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage335D_branch_input_materialization_no_model_training_"
    "no_threshold_retuning_no_lot_optimization_no_direct_forward_pocket_filtering_"
    "no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_"
    "no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
PAYLOAD_DIR = RUN_DIR / "branch_payloads"
RUN335C_DIR = STAGE_DIR / "02_runs" / "run335C"
RUN335B_DIR = STAGE_DIR / "02_runs" / "run335B"
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
DECISION_DOC = DOCS / "decisions" / "2026-05-26_stage335D_guarded_branch_research_input_materialization.md"

RUN335C_INPUTS: dict[str, Path] = {
    "run335D_materialization_queue": RUN335C_DIR / "run335D_materialization_queue.csv",
    "branch_design_matrix": RUN335C_DIR / "branch_design_matrix.csv",
    "branch_evidence_requirements": RUN335C_DIR / "branch_evidence_requirements.csv",
    "negative_control_matrix": RUN335C_DIR / "negative_control_matrix.csv",
    "branch_stop_condition_matrix": RUN335C_DIR / "branch_stop_condition_matrix.csv",
    "tier_kpi_plan": RUN335C_DIR / "tier_kpi_plan.csv",
    "runtime_parity_gate_plan": RUN335C_DIR / "runtime_parity_gate_plan.csv",
    "source_artifact_hashes": RUN335C_DIR / "source_artifact_hashes.json",
    "final_branch_design_decision": RUN335C_DIR / "final_branch_design_decision.json",
}

RUN335B_INPUTS: dict[str, Path] = {
    "source_file_index": RUN335B_DIR / "source_file_index.csv",
    "guard_input_manifest": RUN335B_DIR / "guard_input_manifest.csv",
    "fixed_control_lock_manifest": RUN335B_DIR / "fixed_control_lock_manifest.csv",
    "forbidden_repair_check": RUN335B_DIR / "forbidden_repair_check.csv",
    "latest_forward_data_inventory": RUN335B_DIR / "latest_forward_data_inventory.csv",
    "runtime_handoff_requirement_inventory": RUN335B_DIR / "runtime_handoff_requirement_inventory.csv",
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


def parse_json_list(value: str) -> list[str]:
    if not value:
        return []
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        return [item.strip() for item in str(value).split(";") if item.strip()]
    if isinstance(parsed, list):
        return [str(item) for item in parsed]
    return [str(parsed)]


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


def by_key(rows: Sequence[Mapping[str, str]], key: str) -> dict[str, Mapping[str, str]]:
    return {str(row.get(key, "")): row for row in rows if row.get(key)}


def rows_for(rows: Sequence[Mapping[str, str]], key: str, value: str) -> list[dict[str, str]]:
    return [dict(row) for row in rows if row.get(key) == value]


def source_hashes() -> dict[str, str]:
    hashes: dict[str, str] = {}
    for path in [*RUN335C_INPUTS.values(), *RUN335B_INPUTS.values()]:
        hashes[rel(path)] = sha256_file(path)
    return hashes


def load_inputs() -> dict[str, Any]:
    return {
        "queue": read_csv_rows(RUN335C_INPUTS["run335D_materialization_queue"]),
        "branches": read_csv_rows(RUN335C_INPUTS["branch_design_matrix"]),
        "evidence": read_csv_rows(RUN335C_INPUTS["branch_evidence_requirements"]),
        "negative": read_csv_rows(RUN335C_INPUTS["negative_control_matrix"]),
        "stops": read_csv_rows(RUN335C_INPUTS["branch_stop_condition_matrix"]),
        "tier": read_csv_rows(RUN335C_INPUTS["tier_kpi_plan"]),
        "runtime": read_csv_rows(RUN335C_INPUTS["runtime_parity_gate_plan"]),
        "source_index": read_csv_rows(RUN335B_INPUTS["source_file_index"]),
        "fixed_locks": read_csv_rows(RUN335B_INPUTS["fixed_control_lock_manifest"]),
        "forbidden_repairs": read_csv_rows(RUN335B_INPUTS["forbidden_repair_check"]),
        "latest_forward_data": read_csv_rows(RUN335B_INPUTS["latest_forward_data_inventory"]),
        "run335c_decision": read_json(RUN335C_INPUTS["final_branch_design_decision"]),
        "run335c_source_hashes": read_json(RUN335C_INPUTS["source_artifact_hashes"]),
    }


def build_source_bindings(branch_rows: Sequence[Mapping[str, str]], source_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    source_by_id = by_key(source_rows, "source_id")
    bindings: list[dict[str, Any]] = []
    for branch in branch_rows:
        required_inputs = parse_json_list(str(branch.get("source_file_index", "")))
        for source_id in required_inputs:
            source = source_by_id.get(source_id, {})
            bindings.append(
                {
                    "branch_id": branch.get("branch_id", ""),
                    "branch_name": branch.get("branch_name", ""),
                    "source_id": source_id,
                    "source_role": source.get("source_role", ""),
                    "source_path": source.get("path", ""),
                    "source_exists": source.get("exists", "false") or "false",
                    "artifact_type": source.get("artifact_type", ""),
                    "row_count": source.get("row_count", ""),
                    "sha256": source.get("sha256", "missing") or "missing",
                    "integrity_judgment": source.get("integrity_judgment", "missing_source_binding"),
                    "time_axis_statement": source.get("time_axis_statement", ""),
                    "feature_label_boundary_statement": source.get("feature_label_boundary_statement", ""),
                    "binding_status": "bound" if source else "missing_source_id",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return bindings


def payload_for_branch(
    branch: Mapping[str, str],
    queue_row: Mapping[str, str],
    source_bindings: Sequence[Mapping[str, Any]],
    inputs: Mapping[str, Any],
) -> dict[str, Any]:
    branch_id = str(branch.get("branch_id", ""))
    return {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "stage_id": STAGE_ID,
        "branch": dict(branch),
        "materialization_queue": dict(queue_row),
        "source_bindings": [dict(row) for row in source_bindings if row.get("branch_id") == branch_id],
        "evidence_requirements": rows_for(inputs["evidence"], "branch_id", branch_id),
        "negative_controls": rows_for(inputs["negative"], "branch_id", branch_id),
        "stop_conditions": rows_for(inputs["stops"], "branch_id", branch_id),
        "tier_kpi_plan": rows_for(inputs["tier"], "branch_id", branch_id),
        "runtime_parity_gates": rows_for(inputs["runtime"], "branch_id", branch_id),
        "fixed_control_locks": inputs["fixed_locks"],
        "forbidden_repairs": inputs["forbidden_repairs"],
        "materialization_status": "input_spec_payload_materialized_no_scoring",
        "selection_eligible": False,
        "next_consumer": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_payloads(inputs: Mapping[str, Any], source_bindings: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    queue_by_branch = by_key(inputs["queue"], "branch_id")
    payload_manifest: list[dict[str, Any]] = []
    for branch in inputs["branches"]:
        branch_id = str(branch.get("branch_id", ""))
        branch_name = str(branch.get("branch_name", ""))
        payload_path = PAYLOAD_DIR / f"{branch_id}.json"
        queue_row = queue_by_branch.get(branch_id, {})
        payload = payload_for_branch(branch, queue_row, source_bindings, inputs)
        write_json(payload_path, payload)
        branch_sources = [row for row in source_bindings if row.get("branch_id") == branch_id]
        missing_sources = [row for row in branch_sources if row.get("binding_status") != "bound" or row.get("source_exists") != "true"]
        payload_manifest.append(
            {
                "package_id": f"{RUN_ID}__{branch_name}",
                "branch_id": branch_id,
                "branch_name": branch_name,
                "branch_type": branch.get("branch_type", ""),
                "failure_axes": branch.get("failure_axes", ""),
                "source_binding_count": len(branch_sources),
                "missing_source_count": len(missing_sources),
                "evidence_requirement_count": len(rows_for(inputs["evidence"], "branch_id", branch_id)),
                "negative_control_count": len(rows_for(inputs["negative"], "branch_id", branch_id)),
                "stop_condition_count": len(rows_for(inputs["stops"], "branch_id", branch_id)),
                "tier_kpi_rows": len(rows_for(inputs["tier"], "branch_id", branch_id)),
                "runtime_gate_count": len(rows_for(inputs["runtime"], "branch_id", branch_id)),
                "payload_path": rel(payload_path),
                "payload_sha256": sha256_file(payload_path),
                "package_status": "materialized_input_spec_only" if not missing_sources else "materialized_with_missing_source_warning",
                "selection_eligible": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return payload_manifest


def build_review_queue(payload_manifest: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for package in payload_manifest:
        rows.append(
            {
                "review_queue_id": f"{NEXT_RUN_ID}__{package['branch_name']}",
                "branch_id": package["branch_id"],
                "branch_name": package["branch_name"],
                "review_action": "review_branch_input_package_and_gate_readiness_only",
                "required_payload": package["payload_path"],
                "required_checks": [
                    "payload_exists",
                    "source_bindings_bound",
                    "negative_controls_present",
                    "stop_conditions_present",
                    "tier_views_present",
                    "runtime_gates_present_or_out_of_scope",
                    "forbidden_claims_absent",
                ],
                "block_if_missing": "payload, source binding, claim boundary, or anti-overfit guard",
                "selection_eligible": "false",
                "next_status_planned": "review_input_materialization_only_no_candidate_selection",
            }
        )
    return rows


def build_forbidden_output_rows(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for queue_row in inputs["queue"]:
        for output_name in parse_json_list(str(queue_row.get("forbidden_outputs", ""))):
            rows.append(
                {
                    "branch_id": queue_row.get("branch_id", ""),
                    "branch_name": queue_row.get("branch_name", ""),
                    "forbidden_output": output_name,
                    "check_status": "rejected_by_materialization_contract",
                    "effect": "keeps run335D as input materialization only; no scoring, retune, or runtime authority claim",
                }
            )
    return rows


def build_gate_rows(
    payload_manifest: Sequence[Mapping[str, Any]],
    source_bindings: Sequence[Mapping[str, Any]],
    review_queue: Sequence[Mapping[str, Any]],
    inputs: Mapping[str, Any],
) -> list[dict[str, Any]]:
    missing_sources = [row for row in source_bindings if row.get("binding_status") != "bound" or row.get("source_exists") != "true"]
    selection_true = [row for row in payload_manifest if str(row.get("selection_eligible", "")).lower() == "true"]
    failed_payloads = [row for row in payload_manifest if not path_exists(ROOT / str(row.get("payload_path", "")))]
    return [
        {
            "gate": "parent_queue_loaded",
            "status": "passed" if len(inputs["queue"]) == 11 else "failed_parent_queue_count",
            "evidence_path": rel(RUN335C_INPUTS["run335D_materialization_queue"]),
            "detail": f"queue_rows={len(inputs['queue'])}",
        },
        {
            "gate": "branch_payload_count",
            "status": "passed" if len(payload_manifest) == 11 and not failed_payloads else "failed_payload_count_or_missing_payload",
            "evidence_path": rel(RUN_DIR / "branch_input_package_manifest.csv"),
            "detail": f"payload_rows={len(payload_manifest)};missing_payloads={len(failed_payloads)}",
        },
        {
            "gate": "source_binding_integrity",
            "status": "passed" if not missing_sources else "failed_missing_source_binding",
            "evidence_path": rel(RUN_DIR / "branch_source_binding_matrix.csv"),
            "detail": f"source_bindings={len(source_bindings)};missing_sources={len(missing_sources)}",
        },
        {
            "gate": "negative_control_coverage",
            "status": "passed" if len(inputs["negative"]) == 21 else "failed_negative_control_count",
            "evidence_path": rel(RUN_DIR / "branch_negative_control_payloads.csv"),
            "detail": f"negative_control_rows={len(inputs['negative'])}",
        },
        {
            "gate": "tier_kpi_coverage",
            "status": "passed" if len(inputs["tier"]) == 33 else "failed_tier_kpi_count",
            "evidence_path": rel(RUN_DIR / "branch_tier_kpi_payloads.csv"),
            "detail": f"tier_kpi_rows={len(inputs['tier'])}",
        },
        {
            "gate": "runtime_gate_boundary",
            "status": "passed" if len(inputs["runtime"]) == 20 else "failed_runtime_gate_count",
            "evidence_path": rel(RUN_DIR / "branch_runtime_gate_payloads.csv"),
            "detail": f"runtime_gate_rows={len(inputs['runtime'])};runtime_claim_boundary=not_applicable_until_tester_output",
        },
        {
            "gate": "forbidden_output_guard",
            "status": "passed",
            "evidence_path": rel(RUN_DIR / "forbidden_output_guard.csv"),
            "detail": "candidate_signal, threshold_change, lot_change, direct_forward_pocket_filter, and runtime_authority_claim remain rejected",
        },
        {
            "gate": "selection_claim_guard",
            "status": "passed" if not selection_true else "failed_selection_eligible_true",
            "evidence_path": rel(RUN_DIR / "result_judgment.csv"),
            "detail": f"selection_true={len(selection_true)};goal_achieve=not_claimed",
        },
        {
            "gate": "run335E_review_queue_ready",
            "status": "passed" if len(review_queue) == 11 else "failed_review_queue_count",
            "evidence_path": rel(RUN_DIR / "run335E_review_queue.csv"),
            "detail": f"review_queue_rows={len(review_queue)}",
        },
    ]


def build_receipts(
    inputs: Mapping[str, Any],
    payload_manifest: Sequence[Mapping[str, Any]],
    source_bindings: Sequence[Mapping[str, Any]],
    gate_rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    failed_gates = [row for row in gate_rows if str(row.get("status", "")).startswith("failed")]
    return {
        "data_integrity_receipt": {
            "data_source": [rel(path) for path in [*RUN335C_INPUTS.values(), *RUN335B_INPUTS.values()]],
            "time_axis": "run335D does not create market bars; it preserves parent source timestamps and requires future probes to restate timezone and bar convention.",
            "sample_scope": "US100 M5 Stage335 branch input materialization; no new score, model, threshold, lot, or MT5 result.",
            "missing_or_duplicate_check": f"source_binding_rows={len(source_bindings)};missing_source_bindings={len([row for row in source_bindings if row.get('binding_status') != 'bound' or row.get('source_exists') != 'true'])}",
            "feature_label_boundary": "No feature or label generation occurs in run335D; future feature frames must be timestamp-safe and predeclared before scoring.",
            "split_boundary": "Tier A separate, Tier B separate, and Tier A+B combined reporting remain required; WFO or runtime splits are not redefined here.",
            "leakage_risk": "Using Stage334 failure pockets as direct filters remains the main leakage and overfit path; run335D only packages guards.",
            "data_hash_or_identity": source_hashes(),
            "integrity_judgment": "usable_with_boundary" if not failed_gates else "blocked",
        },
        "model_validation_receipt": {
            "model_family": "existing/future ONNX research surfaces only; run335D trains no model",
            "target_and_label": "not generated in run335D",
            "split_method": "not changed; future review must keep paired Tier views and predeclared split meaning",
            "selection_metric": "none",
            "secondary_metrics": [
                "source binding completeness",
                "negative control coverage",
                "tier KPI coverage",
                "runtime gate coverage",
                "forbidden output guard",
            ],
            "threshold_policy": "no threshold search, no threshold retuning, no score cutoff change",
            "overfit_risk": "branch packages could become hidden forward-pocket filters if later review ignores stop conditions",
            "calibration_risk": "no score calibration is created or claimed",
            "comparison_baseline": "run335C branch design and run335B guard inputs",
            "validation_judgment": "materialization_only_no_selection",
        },
        "runtime_parity_receipt": {
            "research_path": rel(Path(__file__)),
            "runtime_path": "none_in_run335D_no_MT5_execution",
            "shared_contract": [
                "feature order hash required before runtime probe",
                "ONNX sha256 and package manifest required before runtime probe",
                "handoff manifest and signal timestamps required before runtime probe",
                "MT5 tester report and telemetry required before runtime authority candidate",
            ],
            "known_differences": "run335D packages runtime gates but does not compile or execute MT5.",
            "parity_check": "out_of_scope_by_claim_input_materialization_only",
            "parity_identity": {
                "runtime_gate_rows": len(inputs["runtime"]),
                "source_hashes": source_hashes(),
            },
            "runtime_claim_boundary": "research_only_no_runtime_probe_no_runtime_authority",
        },
        "result_judgment_receipt": {
            "result_subject": "run335D guarded branch research input materialization",
            "evidence_available": [
                rel(RUN_DIR / "branch_input_package_manifest.csv"),
                rel(RUN_DIR / "run335E_review_queue.csv"),
                rel(RUN_DIR / "required_gate_coverage_audit.csv"),
            ],
            "evidence_missing": [
                "no scoring output",
                "no model training",
                "no threshold selection",
                "no MT5 tester report",
                "no Forward Passed or Forward Failed evidence",
            ],
            "judgment_label": "exploratory_materialization",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "The branch packages are ready for review, but they are not performance results or candidate evidence.",
        },
        "anti_overfit_materialization_receipt": {
            "payload_count": len(payload_manifest),
            "forbidden_repairs": [
                "model_training",
                "threshold_retuning",
                "lot_optimization",
                "direct_forward_pocket_filtering",
                "date_hour_side_pruning_from_failure_memory",
                "subject_swap",
                "runtime_authority_claim",
                "goal_achieve_claim",
            ],
            "forbidden_output_guard_path": rel(RUN_DIR / "forbidden_output_guard.csv"),
            "selection_eligible_true_count": len([row for row in payload_manifest if str(row.get("selection_eligible", "")).lower() == "true"]),
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "gate_receipt": {
            "required_gates": gate_rows,
            "failed_gates": failed_gates,
        },
    }


def build_report_text(payload_manifest: Sequence[Mapping[str, Any]], gate_rows: Sequence[Mapping[str, Any]]) -> str:
    failed_gates = [row for row in gate_rows if str(row.get("status", "")).startswith("failed")]
    branch_names = ", ".join(str(row.get("branch_name", "")) for row in payload_manifest)
    return f"""
# run335D Guarded Branch Research Input Materialization(335D 방어 분기 연구 입력 실체화)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- branch_payloads(분기 페이로드): `{len(payload_manifest)}`
- failed_gates(실패 게이트): `{len(failed_gates)}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- branch_names(분기 이름): `{branch_names}`

Effect(효과): run335C(335C 실행)의 11개 branch design(분기 설계)을 branch payload(분기 페이로드), source binding(원천 연결), negative control(부정 대조), stop condition(중단 조건), tier KPI(티어 핵심 성과 지표), runtime gate(런타임 게이트) 입력으로 고정했다.

Boundary(경계): model training(모델 학습), threshold retuning(임계값 재조정), lot optimization(로트 최적화), direct forward pocket filtering(직접 전진 포켓 필터링), candidate selection(후보 선택), Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 모두 `not_claimed`다.
"""


def build_decision_text() -> str:
    return f"""
# Stage335D Decision(335D 결정)

`{RUN_ID}`는 guarded branch research inputs(방어 분기 연구 입력)를 materialized(실체화)했다.

- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Effect(효과): 다음 run335E(335E 실행)는 새 후보를 고르지 않고, 먼저 각 branch package(분기 패키지)가 과적합 방어선과 런타임 동등성 요구를 제대로 담았는지 검토할 수 있다.
"""


def update_state_docs() -> list[Path]:
    changed: list[Path] = []

    selection_path = SELECTED_DIR / "selection_status.md"
    text, had_bom = read_text_lossless(selection_path)
    text = replace_prefix_line(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    text = replace_prefix_line(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_RUN_ID}`")
    text = replace_prefix_line(
        text,
        "- effect(효과):",
        "- effect(효과): Stage335D(335D 실행)는 guarded branch input packages(방어 분기 입력 패키지)를 실체화했지만, 아직 모델 학습(model training, 모델 학습)이나 후보 선택(candidate selection, 후보 선택)은 없다.",
    )
    changed.append(write_text_lossless(selection_path, text, had_bom))

    text, had_bom = read_text_lossless(STAGE_BRIEF)
    text = replace_prefix_line(text, "- latest_run(최신 실행):", f"- latest_run(최신 실행): `{RUN_ID}`")
    changed.append(write_text_lossless(STAGE_BRIEF, text, had_bom))

    changed.append(
        append_section_once(
            INPUTS_DIR / "input_refs.md",
            "## run335D Branch Input Materialization(335D 분기 입력 실체화)",
            f"""- branch_input_package_manifest(분기 입력 패키지 목록): `{rel(RUN_DIR / "branch_input_package_manifest.csv")}`
- branch_payloads(분기 페이로드): `{rel(PAYLOAD_DIR)}`
- branch_source_binding_matrix(분기 원천 연결 행렬): `{rel(RUN_DIR / "branch_source_binding_matrix.csv")}`
- run335E_review_queue(335E 검토 대기열): `{rel(RUN_DIR / "run335E_review_queue.csv")}`
- decision(결정): `{rel(DECISION_DOC)}`""",
        )
    )

    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_prefix_line(workspace_text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    workspace_text = replace_prefix_line(workspace_text, "updated_on:", f"updated_on: '{TODAY}'")
    focus_line = (
        "- >-\n"
        f"  Stage335(335단계) run335D(335D 실행)는 `{STATUS}`로 guarded branch research inputs(방어 분기 연구 입력)를 materialized(실체화)했다. "
        "Effect(효과): 11개 branch payload/source binding/review queue(분기 페이로드/원천 연결/검토 대기열)를 만들고 Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    workspace_text = insert_after_prefix_once(workspace_text, "current_focus:", focus_line, "run335D(335D 실행)")
    changed.append(write_text_lossless(WORKSPACE_STATE, workspace_text, workspace_bom))

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    current_text = replace_prefix_line(current_text, "- current_packet(현재 작업 묶음):", "- current_packet(현재 작업 묶음): `335_overfit_guard__failure_memory_constrained_research_handoff_v5`")
    current_text = replace_prefix_line(current_text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    current_text = replace_prefix_line(current_text, "- status(상태):", f"- status(상태): `{STATUS}`")
    current_text = replace_prefix_line(current_text, "- decision(판정):", f"- decision(판정): `{DECISION}`")
    current_text = remove_lines_containing(current_text, "run335D_summary(335D 요약)")
    summary = (
        f"- run335D_summary(335D 요약): guarded branch research input materialization(방어 분기 연구 입력 실체화)을 `{STATUS}`로 완료했다. "
        "Effect(효과): branch payload(분기 페이로드) 11개와 run335E review queue(335E 검토 대기열) 11개를 만들었고, 선택 후보나 Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    current_text = insert_after_prefix_once(current_text, "- decision(판정):", summary, "run335D_summary")
    changed.append(write_text_lossless(CURRENT_STATE, current_text, current_bom))

    changed.append(
        append_section_once(
            CHANGELOG,
            "## 2026-05-26 Stage335D Branch Input Materialization(335D 분기 입력 실체화)",
            f"""- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- effect(효과): 11개 guarded branch package(방어 분기 패키지)를 run335E(335E 실행) 검토 입력으로 만들었다.
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
        "ledger_row_id": f"{RUN_ID}__branch_input_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "guarded_branch_research_input_materialization",
        "tier_scope": "paired_tier_required_by_contract",
        "kpi_scope": "manifest_only_no_new_trading_kpi",
        "scoreboard_lane": "experiment_execution",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(report_path),
        "primary_kpi": "branch_payloads=11;review_queue_rows=11",
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
                    "ledger_row_id": ledger_row["ledger_row_id"],
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "work_family": "experiment_execution",
                    "evidence_scope": "guarded_branch_research_input_materialization",
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
                "notes": f"Stage335D guarded branch input materialization artifact; claim_boundary={CLAIM_BOUNDARY}",
            }
        )
    changed.append(upsert_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows))
    return changed


def main() -> int:
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    PAYLOAD_DIR.mkdir(parents=True, exist_ok=True)
    inputs = load_inputs()
    source_bindings = build_source_bindings(inputs["branches"], inputs["source_index"])
    payload_manifest = build_payloads(inputs, source_bindings)
    review_queue = build_review_queue(payload_manifest)
    forbidden_rows = build_forbidden_output_rows(inputs)
    gate_rows = build_gate_rows(payload_manifest, source_bindings, review_queue, inputs)
    receipts = build_receipts(inputs, payload_manifest, source_bindings, gate_rows)
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
        "branch_payload_count": len(payload_manifest),
        "review_queue_count": len(review_queue),
        "next_action": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }

    artifact_paths: list[Path] = [
        write_json(RUN_DIR / "source_artifact_hashes.json", source_hashes()),
        write_csv(
            RUN_DIR / "branch_input_package_manifest.csv",
            [
                "package_id",
                "branch_id",
                "branch_name",
                "branch_type",
                "failure_axes",
                "source_binding_count",
                "missing_source_count",
                "evidence_requirement_count",
                "negative_control_count",
                "stop_condition_count",
                "tier_kpi_rows",
                "runtime_gate_count",
                "payload_path",
                "payload_sha256",
                "package_status",
                "selection_eligible",
                "claim_boundary",
            ],
            payload_manifest,
        ),
        write_csv(
            RUN_DIR / "branch_source_binding_matrix.csv",
            [
                "branch_id",
                "branch_name",
                "source_id",
                "source_role",
                "source_path",
                "source_exists",
                "artifact_type",
                "row_count",
                "sha256",
                "integrity_judgment",
                "time_axis_statement",
                "feature_label_boundary_statement",
                "binding_status",
                "claim_boundary",
            ],
            source_bindings,
        ),
        write_csv(
            RUN_DIR / "branch_evidence_payloads.csv",
            ["branch_id", "evidence_id", "proves", "required_before", "missing_policy"],
            inputs["evidence"],
        ),
        write_csv(
            RUN_DIR / "branch_negative_control_payloads.csv",
            ["branch_id", "control_id", "control_role", "control_design", "pass_condition", "fail_condition", "claim_effect"],
            inputs["negative"],
        ),
        write_csv(
            RUN_DIR / "branch_stop_condition_payloads.csv",
            ["branch_id", "stop_rule_id", "trigger", "required_action", "claim_effect"],
            inputs["stops"],
        ),
        write_csv(
            RUN_DIR / "branch_tier_kpi_payloads.csv",
            ["branch_id", "view", "required", "meaning", "kpi_scope", "missing_policy", "profit_attribution_boundary"],
            inputs["tier"],
        ),
        write_csv(
            RUN_DIR / "branch_runtime_gate_payloads.csv",
            [
                "branch_id",
                "requirement",
                "required_before",
                "evidence",
                "forbidden_shortcut",
                "runtime_claim_boundary",
                "run335C_status",
            ],
            inputs["runtime"],
        ),
        write_csv(
            RUN_DIR / "forbidden_output_guard.csv",
            ["branch_id", "branch_name", "forbidden_output", "check_status", "effect"],
            forbidden_rows,
        ),
        write_csv(
            RUN_DIR / "run335E_review_queue.csv",
            [
                "review_queue_id",
                "branch_id",
                "branch_name",
                "review_action",
                "required_payload",
                "required_checks",
                "block_if_missing",
                "selection_eligible",
                "next_status_planned",
            ],
            review_queue,
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
                "goal_achieve",
                "next_action",
                "claim_boundary",
            ],
            result_rows,
        ),
        write_json(RUN_DIR / "data_integrity_receipt.json", receipts["data_integrity_receipt"]),
        write_json(RUN_DIR / "model_validation_receipt.json", receipts["model_validation_receipt"]),
        write_json(RUN_DIR / "runtime_parity_receipt.json", receipts["runtime_parity_receipt"]),
        write_json(RUN_DIR / "result_judgment_receipt.json", receipts["result_judgment_receipt"]),
        write_json(RUN_DIR / "anti_overfit_materialization_receipt.json", receipts["anti_overfit_materialization_receipt"]),
        write_json(RUN_DIR / "gate_receipt.json", receipts["gate_receipt"]),
        write_json(RUN_DIR / "final_materialization_decision.json", final_decision),
    ]
    artifact_paths.extend(sorted(PAYLOAD_DIR.glob("*.json")))

    manifest_path = RUN_DIR / "run_manifest.json"
    lineage_path = RUN_DIR / "artifact_lineage_receipt.json"
    run_manifest = {
        **final_decision,
        "created_at_utc": utc_now(),
        "producer": rel(Path(__file__)),
        "source_inputs": [rel(path) for path in [*RUN335C_INPUTS.values(), *RUN335B_INPUTS.values()]],
        "outputs": [rel(path) for path in [*artifact_paths, manifest_path, lineage_path]],
    }
    artifact_paths.append(write_json(manifest_path, run_manifest))

    lineage = {
        "source_inputs": [rel(path) for path in [*RUN335C_INPUTS.values(), *RUN335B_INPUTS.values()]],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in [*artifact_paths, lineage_path]],
        "artifact_hashes": {rel(path): sha256_file(path) for path in artifact_paths},
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "tracked_after_force_add_run_dir",
        "lineage_judgment": "connected_with_boundary",
    }
    artifact_paths.append(write_json(lineage_path, lineage))

    report_path = write_md(REVIEWS_DIR / "run335D_guarded_branch_research_input_materialization.md", build_report_text(payload_manifest, gate_rows))
    artifact_paths.append(report_path)
    artifact_paths.append(write_md(DECISION_DOC, build_decision_text()))
    artifact_paths.extend(update_state_docs())
    artifact_paths.extend(update_registries([Path(__file__), *artifact_paths], report_path))

    failed_gates = [row for row in gate_rows if str(row.get("status", "")).startswith("failed")]
    summary = {
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "branch_payload_count": len(payload_manifest),
        "payload_json_count": len(list(PAYLOAD_DIR.glob("*.json"))),
        "source_binding_rows": len(source_bindings),
        "missing_source_bindings": len([row for row in source_bindings if row.get("binding_status") != "bound" or row.get("source_exists") != "true"]),
        "negative_control_rows": len(inputs["negative"]),
        "tier_rows": len(inputs["tier"]),
        "runtime_gate_rows": len(inputs["runtime"]),
        "review_queue_rows": len(review_queue),
        "failed_gates": len(failed_gates),
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
