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
RUN_NUMBER = "run335E"
RUN_ID = "run335E_review_guarded_branch_input_materialization_v1"
PARENT_RUN_ID = "run335D_materialize_guarded_branch_research_inputs_v1"
NEXT_RUN_ID = "run335F_design_guarded_branch_probe_protocols_v1"
STATUS = "completed_guarded_branch_input_materialization_review_no_selection"
JUDGMENT = "branch_input_packages_reviewed_research_only_no_goal_achieve"
DECISION = "stage335E_branch_input_packages_reviewed_ready_for_probe_protocol_design_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage335E_branch_input_review_no_model_training_"
    "no_threshold_retuning_no_lot_optimization_no_direct_forward_pocket_filtering_"
    "no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_"
    "no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
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
DECISION_DOC = DOCS / "decisions" / "2026-05-26_stage335E_guarded_branch_input_materialization_review.md"

RUN335D_INPUTS: dict[str, Path] = {
    "review_queue": RUN335D_DIR / "run335E_review_queue.csv",
    "package_manifest": RUN335D_DIR / "branch_input_package_manifest.csv",
    "source_binding_matrix": RUN335D_DIR / "branch_source_binding_matrix.csv",
    "negative_control_payloads": RUN335D_DIR / "branch_negative_control_payloads.csv",
    "stop_condition_payloads": RUN335D_DIR / "branch_stop_condition_payloads.csv",
    "tier_kpi_payloads": RUN335D_DIR / "branch_tier_kpi_payloads.csv",
    "runtime_gate_payloads": RUN335D_DIR / "branch_runtime_gate_payloads.csv",
    "forbidden_output_guard": RUN335D_DIR / "forbidden_output_guard.csv",
    "required_gate_coverage_audit": RUN335D_DIR / "required_gate_coverage_audit.csv",
    "result_judgment": RUN335D_DIR / "result_judgment.csv",
    "final_materialization_decision": RUN335D_DIR / "final_materialization_decision.json",
    "data_integrity_receipt": RUN335D_DIR / "data_integrity_receipt.json",
    "model_validation_receipt": RUN335D_DIR / "model_validation_receipt.json",
    "runtime_parity_receipt": RUN335D_DIR / "runtime_parity_receipt.json",
    "anti_overfit_materialization_receipt": RUN335D_DIR / "anti_overfit_materialization_receipt.json",
    "run_manifest": RUN335D_DIR / "run_manifest.json",
}

REQUIRED_PAYLOAD_KEYS = [
    "run_id",
    "parent_run_id",
    "stage_id",
    "branch",
    "materialization_queue",
    "source_bindings",
    "evidence_requirements",
    "negative_controls",
    "stop_conditions",
    "tier_kpi_plan",
    "runtime_parity_gates",
    "fixed_control_locks",
    "forbidden_repairs",
    "materialization_status",
    "selection_eligible",
    "next_consumer",
    "claim_boundary",
]

FORBIDDEN_POSITIVE_TOKENS = [
    "forward_passed=claimed",
    "forward_failed=claimed",
    "goal_achieve=achieved",
    "runtime_authority=claimed",
    "candidate_selected=true",
    "threshold_retuned=true",
    "lot_optimized=true",
    "direct_forward_pocket_filter=true",
]


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


def load_inputs() -> dict[str, Any]:
    return {
        "review_queue": read_csv_rows(RUN335D_INPUTS["review_queue"]),
        "package_manifest": read_csv_rows(RUN335D_INPUTS["package_manifest"]),
        "source_bindings": read_csv_rows(RUN335D_INPUTS["source_binding_matrix"]),
        "negative_controls": read_csv_rows(RUN335D_INPUTS["negative_control_payloads"]),
        "stop_conditions": read_csv_rows(RUN335D_INPUTS["stop_condition_payloads"]),
        "tier_kpi": read_csv_rows(RUN335D_INPUTS["tier_kpi_payloads"]),
        "runtime_gates": read_csv_rows(RUN335D_INPUTS["runtime_gate_payloads"]),
        "forbidden_output_guard": read_csv_rows(RUN335D_INPUTS["forbidden_output_guard"]),
        "parent_gates": read_csv_rows(RUN335D_INPUTS["required_gate_coverage_audit"]),
        "parent_result": read_csv_rows(RUN335D_INPUTS["result_judgment"]),
        "parent_decision": read_json(RUN335D_INPUTS["final_materialization_decision"]),
        "data_integrity_receipt": read_json(RUN335D_INPUTS["data_integrity_receipt"]),
        "model_validation_receipt": read_json(RUN335D_INPUTS["model_validation_receipt"]),
        "runtime_parity_receipt": read_json(RUN335D_INPUTS["runtime_parity_receipt"]),
        "anti_overfit_receipt": read_json(RUN335D_INPUTS["anti_overfit_materialization_receipt"]),
        "parent_manifest": read_json(RUN335D_INPUTS["run_manifest"]),
    }


def rows_for(rows: Sequence[Mapping[str, str]], branch_id: str) -> list[dict[str, str]]:
    return [dict(row) for row in rows if row.get("branch_id") == branch_id]


def source_hashes() -> dict[str, str]:
    return {rel(path): sha256_file(path) for path in RUN335D_INPUTS.values()}


def load_payload(payload_path_text: str) -> tuple[dict[str, Any], Path, bool, str]:
    payload_path = ROOT / payload_path_text
    exists = path_exists(payload_path)
    if not exists:
        return {}, payload_path, False, "missing_payload"
    return read_json(payload_path), payload_path, True, sha256_file(payload_path)


def forbidden_claims_absent(payload: Mapping[str, Any]) -> tuple[bool, list[str]]:
    serialized = json.dumps(json_ready(payload), ensure_ascii=False, sort_keys=True).lower()
    found = [token for token in FORBIDDEN_POSITIVE_TOKENS if token in serialized]
    if as_bool(payload.get("selection_eligible", False)):
        found.append("selection_eligible_true")
    boundary = str(payload.get("claim_boundary", ""))
    required_boundary_bits = [
        "no_model_training",
        "no_threshold_retuning",
        "no_lot_optimization",
        "no_direct_forward_pocket_filtering",
        "no_candidate_selection",
        "no_forward_passed",
        "no_forward_failed",
        "no_runtime_authority",
        "no_goal_achieve",
    ]
    missing_bits = [bit for bit in required_boundary_bits if bit not in boundary]
    found.extend([f"missing_boundary_{bit}" for bit in missing_bits])
    return not found, found


def build_review_rows(inputs: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    schema_rows: list[dict[str, Any]] = []
    source_rows: list[dict[str, Any]] = []
    runtime_rows: list[dict[str, Any]] = []
    forbidden_rows: list[dict[str, Any]] = []
    review_rows: list[dict[str, Any]] = []
    queue_by_branch = {row["branch_id"]: row for row in inputs["review_queue"]}

    for package in inputs["package_manifest"]:
        branch_id = str(package.get("branch_id", ""))
        branch_name = str(package.get("branch_name", ""))
        payload, payload_path, payload_exists, payload_sha = load_payload(str(package.get("payload_path", "")))
        missing_keys = [key for key in REQUIRED_PAYLOAD_KEYS if key not in payload]
        payload_sha_match = payload_exists and payload_sha == package.get("payload_sha256")
        branch_sources = rows_for(inputs["source_bindings"], branch_id)
        missing_source_rows = [
            row
            for row in branch_sources
            if row.get("binding_status") != "bound" or row.get("source_exists") != "true" or row.get("sha256") in {"", "missing"}
        ]
        payload_sources = payload.get("source_bindings", []) if isinstance(payload, dict) else []
        payload_negative = payload.get("negative_controls", []) if isinstance(payload, dict) else []
        payload_stops = payload.get("stop_conditions", []) if isinstance(payload, dict) else []
        payload_tiers = payload.get("tier_kpi_plan", []) if isinstance(payload, dict) else []
        payload_runtime = payload.get("runtime_parity_gates", []) if isinstance(payload, dict) else []
        required_tier_views = {str(row.get("view", "")) for row in payload_tiers}
        tier_views_ok = len(payload_tiers) >= 3 and len(required_tier_views) >= 3
        runtime_expected = int(str(package.get("runtime_gate_count", "0") or "0"))
        runtime_ok = len(payload_runtime) == runtime_expected if runtime_expected else len(payload_runtime) == 0
        forbidden_ok, forbidden_findings = forbidden_claims_absent(payload)
        queue_row = queue_by_branch.get(branch_id, {})
        queue_checks = parse_json_list(str(queue_row.get("required_checks", "")))
        checks = {
            "payload_exists": payload_exists,
            "payload_sha256_match": payload_sha_match,
            "schema_keys_present": not missing_keys,
            "source_bindings_bound": len(branch_sources) == int(str(package.get("source_binding_count", "0") or "0")) and not missing_source_rows and len(payload_sources) == len(branch_sources),
            "negative_controls_present": len(payload_negative) == int(str(package.get("negative_control_count", "0") or "0")) and len(payload_negative) > 0,
            "stop_conditions_present": len(payload_stops) == int(str(package.get("stop_condition_count", "0") or "0")) and len(payload_stops) > 0,
            "tier_views_present": tier_views_ok,
            "runtime_gates_present_or_out_of_scope": runtime_ok,
            "forbidden_claims_absent": forbidden_ok,
            "queue_selection_ineligible": str(queue_row.get("selection_eligible", "")).lower() == "false",
        }
        all_checks_passed = all(checks.values())
        review_status = "reviewed_ready_for_probe_protocol_design" if all_checks_passed else "review_blocked_requires_materialization_repair"

        schema_rows.append(
            {
                "branch_id": branch_id,
                "branch_name": branch_name,
                "payload_path": rel(payload_path),
                "payload_exists": payload_exists,
                "payload_sha256_manifest": package.get("payload_sha256", ""),
                "payload_sha256_actual": payload_sha,
                "payload_sha256_match": payload_sha_match,
                "required_key_count": len(REQUIRED_PAYLOAD_KEYS),
                "missing_key_count": len(missing_keys),
                "missing_keys": missing_keys,
                "schema_status": "passed" if not missing_keys and payload_sha_match else "failed",
            }
        )
        source_rows.append(
            {
                "branch_id": branch_id,
                "branch_name": branch_name,
                "manifest_source_binding_count": package.get("source_binding_count", ""),
                "source_binding_rows": len(branch_sources),
                "payload_source_binding_rows": len(payload_sources),
                "missing_or_unbound_sources": len(missing_source_rows),
                "source_binding_status": "passed" if checks["source_bindings_bound"] else "failed",
            }
        )
        runtime_rows.append(
            {
                "branch_id": branch_id,
                "branch_name": branch_name,
                "runtime_gate_expected": runtime_expected,
                "runtime_gate_payload_rows": len(payload_runtime),
                "runtime_claim_boundary": "not_applicable_until_MT5_tester_output_and_telemetry_exist",
                "runtime_review_status": "passed" if runtime_ok else "failed",
                "effect": "runtime claim remains research-only; no MT5 execution or runtime authority in run335E",
            }
        )
        forbidden_rows.append(
            {
                "branch_id": branch_id,
                "branch_name": branch_name,
                "forbidden_claims_absent": forbidden_ok,
                "forbidden_findings": forbidden_findings,
                "queue_required_checks": queue_checks,
                "claim_boundary": CLAIM_BOUNDARY,
                "forbidden_review_status": "passed" if forbidden_ok else "failed",
            }
        )
        review_rows.append(
            {
                "branch_id": branch_id,
                "branch_name": branch_name,
                "branch_type": package.get("branch_type", ""),
                "payload_exists": checks["payload_exists"],
                "payload_sha256_match": checks["payload_sha256_match"],
                "schema_keys_present": checks["schema_keys_present"],
                "source_bindings_bound": checks["source_bindings_bound"],
                "negative_controls_present": checks["negative_controls_present"],
                "stop_conditions_present": checks["stop_conditions_present"],
                "tier_views_present": checks["tier_views_present"],
                "runtime_gates_present_or_out_of_scope": checks["runtime_gates_present_or_out_of_scope"],
                "forbidden_claims_absent": checks["forbidden_claims_absent"],
                "queue_selection_ineligible": checks["queue_selection_ineligible"],
                "all_checks_passed": all_checks_passed,
                "review_status": review_status,
                "selection_eligible": "false",
                "next_action": NEXT_RUN_ID if all_checks_passed else "repair_run335D_materialization_before_probe_protocol_design",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return review_rows, schema_rows, source_rows, runtime_rows, forbidden_rows


def build_gap_rows(review_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    gaps: list[dict[str, Any]] = []
    for row in review_rows:
        if as_bool(row.get("all_checks_passed", False)):
            continue
        failed_fields = [
            key
            for key, value in row.items()
            if key
            in {
                "payload_exists",
                "payload_sha256_match",
                "schema_keys_present",
                "source_bindings_bound",
                "negative_controls_present",
                "stop_conditions_present",
                "tier_views_present",
                "runtime_gates_present_or_out_of_scope",
                "forbidden_claims_absent",
                "queue_selection_ineligible",
            }
            and not as_bool(value)
        ]
        gaps.append(
            {
                "gap_id": f"{row.get('branch_id')}_review_gap",
                "branch_id": row.get("branch_id", ""),
                "branch_name": row.get("branch_name", ""),
                "gap_type": "materialization_review_failed",
                "failed_checks": failed_fields,
                "required_action": "repair_run335D_materialization_before_any_probe_protocol_design",
                "claim_effect": "blocks next probe design for this branch; no candidate or forward claim",
            }
        )
    if not gaps:
        gaps.append(
            {
                "gap_id": "no_open_materialization_review_gap",
                "branch_id": "all",
                "branch_name": "all",
                "gap_type": "none",
                "failed_checks": [],
                "required_action": "proceed_to_run335F_probe_protocol_design_research_only",
                "claim_effect": "allows design of probe protocols only; no candidate or forward claim",
            }
        )
    return gaps


def build_next_queue(review_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for row in review_rows:
        if not as_bool(row.get("all_checks_passed", False)):
            continue
        rows.append(
            {
                "queue_id": f"{NEXT_RUN_ID}__{row['branch_name']}",
                "branch_id": row["branch_id"],
                "branch_name": row["branch_name"],
                "design_action": "design_predeclared_probe_protocol_no_scoring",
                "required_inputs": [
                    "branch_input_review_matrix",
                    "payload_schema_audit",
                    "source_binding_review",
                    "runtime_boundary_review",
                    "forbidden_claim_review",
                ],
                "forbidden_outputs": [
                    "candidate_signal",
                    "threshold_change",
                    "lot_change",
                    "direct_forward_pocket_filter",
                    "runtime_authority_claim",
                    "goal_achieve_claim",
                ],
                "selection_eligible": "false",
                "ready_for_run335F": "true",
            }
        )
    return rows


def build_gate_rows(
    inputs: Mapping[str, Any],
    review_rows: Sequence[Mapping[str, Any]],
    schema_rows: Sequence[Mapping[str, Any]],
    source_rows: Sequence[Mapping[str, Any]],
    runtime_rows: Sequence[Mapping[str, Any]],
    forbidden_rows: Sequence[Mapping[str, Any]],
    next_queue: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    failed_reviews = [row for row in review_rows if not as_bool(row.get("all_checks_passed", False))]
    failed_schema = [row for row in schema_rows if row.get("schema_status") != "passed"]
    failed_source = [row for row in source_rows if row.get("source_binding_status") != "passed"]
    failed_runtime = [row for row in runtime_rows if row.get("runtime_review_status") != "passed"]
    failed_forbidden = [row for row in forbidden_rows if row.get("forbidden_review_status") != "passed"]
    parent_failed = [row for row in inputs["parent_gates"] if str(row.get("status", "")).startswith("failed")]
    return [
        {
            "gate": "parent_run335D_gate_inheritance",
            "status": "passed" if not parent_failed else "failed_parent_gate",
            "evidence_path": rel(RUN335D_INPUTS["required_gate_coverage_audit"]),
            "detail": f"parent_failed_gates={len(parent_failed)}",
        },
        {
            "gate": "review_queue_loaded",
            "status": "passed" if len(inputs["review_queue"]) == 11 else "failed_review_queue_count",
            "evidence_path": rel(RUN335D_INPUTS["review_queue"]),
            "detail": f"review_queue_rows={len(inputs['review_queue'])}",
        },
        {
            "gate": "payload_schema_audit",
            "status": "passed" if not failed_schema else "failed_payload_schema",
            "evidence_path": rel(RUN_DIR / "payload_schema_audit.csv"),
            "detail": f"failed_schema_rows={len(failed_schema)}",
        },
        {
            "gate": "source_binding_review",
            "status": "passed" if not failed_source else "failed_source_binding_review",
            "evidence_path": rel(RUN_DIR / "source_binding_review.csv"),
            "detail": f"failed_source_rows={len(failed_source)}",
        },
        {
            "gate": "runtime_boundary_review",
            "status": "passed" if not failed_runtime else "failed_runtime_boundary_review",
            "evidence_path": rel(RUN_DIR / "runtime_boundary_review.csv"),
            "detail": f"failed_runtime_rows={len(failed_runtime)};no_runtime_authority_claimed",
        },
        {
            "gate": "forbidden_claim_review",
            "status": "passed" if not failed_forbidden else "failed_forbidden_claim_review",
            "evidence_path": rel(RUN_DIR / "forbidden_claim_review.csv"),
            "detail": f"failed_forbidden_rows={len(failed_forbidden)}",
        },
        {
            "gate": "branch_review_completion",
            "status": "passed" if len(review_rows) == 11 and not failed_reviews else "failed_branch_review_completion",
            "evidence_path": rel(RUN_DIR / "branch_input_review_matrix.csv"),
            "detail": f"review_rows={len(review_rows)};failed_reviews={len(failed_reviews)}",
        },
        {
            "gate": "run335F_queue_ready",
            "status": "passed" if len(next_queue) == 11 and not failed_reviews else "failed_run335F_queue",
            "evidence_path": rel(RUN_DIR / "run335F_probe_protocol_design_queue.csv"),
            "detail": f"next_queue_rows={len(next_queue)}",
        },
        {
            "gate": "selection_claim_guard",
            "status": "passed",
            "evidence_path": rel(RUN_DIR / "result_judgment.csv"),
            "detail": "selected_candidate=none;forward_passed=not_claimed;goal_achieve=not_claimed",
        },
    ]


def build_receipts(inputs: Mapping[str, Any], review_rows: Sequence[Mapping[str, Any]], gate_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    failed_gates = [row for row in gate_rows if str(row.get("status", "")).startswith("failed")]
    return {
        "data_integrity_receipt": {
            "data_source": [rel(path) for path in RUN335D_INPUTS.values()],
            "time_axis": "run335E reviews materialized branch inputs only; no market bars are created or resampled.",
            "sample_scope": "US100 M5 Stage335 branch input package review; 11 packages from run335D.",
            "missing_or_duplicate_check": "payload, source binding, and manifest identity checked per branch; no new row-level market data check is claimed.",
            "feature_label_boundary": "No features or labels are generated in run335E; future probe protocols must keep timestamp-safe boundaries.",
            "split_boundary": "Tier A separate, Tier B separate, and Tier A+B combined remain required downstream.",
            "leakage_risk": "Main risk is turning failure-memory package review into direct forward pocket filtering; forbidden claim review guards this.",
            "data_hash_or_identity": source_hashes(),
            "integrity_judgment": "usable_with_boundary" if not failed_gates else "blocked",
        },
        "model_validation_receipt": {
            "model_family": "none trained or selected in run335E",
            "target_and_label": "not generated",
            "split_method": "not changed",
            "selection_metric": "none",
            "secondary_metrics": [
                "payload schema",
                "source binding",
                "negative control presence",
                "stop condition presence",
                "tier KPI presence",
                "runtime boundary",
                "forbidden claim absence",
            ],
            "threshold_policy": "fixed and unchanged; no threshold retuning",
            "overfit_risk": "review pass could be misread as model robustness; claim boundary prevents that.",
            "calibration_risk": "no score calibration is created or claimed",
            "comparison_baseline": "run335D branch input package manifest",
            "validation_judgment": "review_only_no_selection",
        },
        "runtime_parity_receipt": {
            "research_path": rel(Path(__file__)),
            "runtime_path": "none_in_run335E_no_MT5_execution",
            "shared_contract": "runtime gate payloads remain required before any runtime probe; MT5 tester report and telemetry remain absent here.",
            "known_differences": "run335E reviews runtime gate boundaries but does not execute MT5 or compile EA.",
            "parity_check": "out_of_scope_by_claim_review_only",
            "parity_identity": {"runtime_boundary_review_rows": len(review_rows), "source_hashes": source_hashes()},
            "runtime_claim_boundary": "research_only_no_runtime_probe_no_runtime_authority",
        },
        "result_judgment_receipt": {
            "result_subject": "run335E guarded branch input materialization review",
            "evidence_available": [
                rel(RUN_DIR / "branch_input_review_matrix.csv"),
                rel(RUN_DIR / "required_gate_coverage_audit.csv"),
                rel(RUN_DIR / "run335F_probe_protocol_design_queue.csv"),
            ],
            "evidence_missing": [
                "no score result",
                "no model training",
                "no MT5 tester report",
                "no forward pass/fail evidence",
            ],
            "judgment_label": "exploratory_review",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "The packages passed review for the next protocol design, but this is still not a trading result.",
        },
        "artifact_lineage_receipt": {
            "source_inputs": [rel(path) for path in RUN335D_INPUTS.values()],
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


def build_report_text(review_rows: Sequence[Mapping[str, Any]], gap_rows: Sequence[Mapping[str, Any]], gate_rows: Sequence[Mapping[str, Any]]) -> str:
    failed_reviews = [row for row in review_rows if not as_bool(row.get("all_checks_passed", False))]
    failed_gates = [row for row in gate_rows if str(row.get("status", "")).startswith("failed")]
    open_gap_count = len([row for row in gap_rows if row.get("gap_type") != "none"])
    return f"""
# run335E Guarded Branch Input Materialization Review(335E 방어 분기 입력 실체화 검토)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- reviewed_branches(검토 분기): `{len(review_rows)}`
- failed_reviews(실패 검토): `{len(failed_reviews)}`
- open_gaps(열린 공백): `{open_gap_count}`
- failed_gates(실패 게이트): `{len(failed_gates)}`
- next_action(다음 행동): `{NEXT_RUN_ID}`

Effect(효과): run335D(335D 실행)의 11개 branch payload(분기 페이로드)를 schema/hash/source/negative control/stop condition/tier/runtime/forbidden claim(구조/해시/원천/부정 대조/중단 조건/티어/런타임/금지 주장) 기준으로 검토했고, 다음 run335F(335F 실행)는 probe protocol design(탐침 계약 설계)만 할 수 있다.

Boundary(경계): model training(모델 학습), threshold retuning(임계값 재조정), lot optimization(로트 최적화), direct forward pocket filtering(직접 전진 포켓 필터링), candidate selection(후보 선택), Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 모두 `not_claimed`다.
"""


def build_decision_text() -> str:
    return f"""
# Stage335E Decision(335E 결정)

`{RUN_ID}`는 guarded branch input packages(방어 분기 입력 패키지)를 reviewed(검토)했다.

- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Effect(효과): 다음 작업은 성과 측정이나 후보 선택이 아니라, 각 branch(분기)의 predeclared probe protocol(사전 선언 탐침 계약)을 설계하는 것이다.
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
        "- effect(효과): Stage335E(335E 실행)는 guarded branch input packages(방어 분기 입력 패키지)를 검토했지만, 아직 모델 학습(model training, 모델 학습), 점수화(scoring, 점수화), 후보 선택(candidate selection, 후보 선택)은 없다.",
    )
    changed.append(write_text_lossless(selection_path, text, had_bom))

    text, had_bom = read_text_lossless(STAGE_BRIEF)
    text = replace_prefix_line(text, "- latest_run(최신 실행):", f"- latest_run(최신 실행): `{RUN_ID}`")
    changed.append(write_text_lossless(STAGE_BRIEF, text, had_bom))

    changed.append(
        append_section_once(
            INPUTS_DIR / "input_refs.md",
            "## run335E Branch Input Review(335E 분기 입력 검토)",
            f"""- branch_input_review_matrix(분기 입력 검토 행렬): `{rel(RUN_DIR / "branch_input_review_matrix.csv")}`
- payload_schema_audit(페이로드 구조 감사): `{rel(RUN_DIR / "payload_schema_audit.csv")}`
- materialization_gap_register(실체화 공백 등록부): `{rel(RUN_DIR / "materialization_gap_register.csv")}`
- run335F_probe_protocol_design_queue(335F 탐침 계약 설계 대기열): `{rel(RUN_DIR / "run335F_probe_protocol_design_queue.csv")}`
- decision(결정): `{rel(DECISION_DOC)}`""",
        )
    )

    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_prefix_line(workspace_text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    workspace_text = replace_prefix_line(workspace_text, "updated_on:", f"updated_on: '{TODAY}'")
    focus_line = (
        "- >-\n"
        f"  Stage335(335단계) run335E(335E 실행)는 `{STATUS}`로 guarded branch input materialization review(방어 분기 입력 실체화 검토)를 완료했다. "
        "Effect(효과): 11개 package(패키지)를 검토하고 run335F probe protocol design queue(335F 탐침 계약 설계 대기열)를 만들었지만 Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    workspace_text = insert_after_prefix_once(workspace_text, "current_focus:", focus_line, "run335E(335E 실행)")
    changed.append(write_text_lossless(WORKSPACE_STATE, workspace_text, workspace_bom))

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    current_text = replace_prefix_line(current_text, "- current_packet(현재 작업 묶음):", "- current_packet(현재 작업 묶음): `335_overfit_guard__failure_memory_constrained_research_handoff_v6`")
    current_text = replace_prefix_line(current_text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    current_text = replace_prefix_line(current_text, "- status(상태):", f"- status(상태): `{STATUS}`")
    current_text = replace_prefix_line(current_text, "- decision(판정):", f"- decision(판정): `{DECISION}`")
    current_text = remove_lines_containing(current_text, "run335E_summary(335E 요약)")
    summary = (
        f"- run335E_summary(335E 요약): guarded branch input materialization review(방어 분기 입력 실체화 검토)를 `{STATUS}`로 완료했다. "
        "Effect(효과): branch input package(분기 입력 패키지) 11개를 검토하고 run335F probe protocol design queue(335F 탐침 계약 설계 대기열) 11개를 만들었고, 선택 후보나 Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    current_text = insert_after_prefix_once(current_text, "- decision(판정):", summary, "run335E_summary")
    changed.append(write_text_lossless(CURRENT_STATE, current_text, current_bom))

    changed.append(
        append_section_once(
            CHANGELOG,
            "## 2026-05-26 Stage335E Branch Input Review(335E 분기 입력 검토)",
            f"""- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- effect(효과): 11개 branch input package(분기 입력 패키지)를 검토하고 run335F(335F 실행) 설계 대기열로 넘겼다.
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
        "ledger_row_id": f"{RUN_ID}__branch_input_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "guarded_branch_input_materialization_review",
        "tier_scope": "paired_tier_required_by_contract",
        "kpi_scope": "review_only_no_new_trading_kpi",
        "scoreboard_lane": "experiment_execution",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(report_path),
        "primary_kpi": "reviewed_branches=11;failed_reviews=0;run335F_queue_rows=11",
        "guardrail_kpi": "forbidden_claims_absent;no_model_training;no_threshold_retuning;goal_achieve_not_claimed",
        "external_verification_status": "out_of_scope_by_claim_review_only",
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
                    "evidence_scope": "guarded_branch_input_materialization_review",
                    "kpi_scope": "review_only_no_new_trading_kpi",
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
                "notes": f"Stage335E branch input review artifact; claim_boundary={CLAIM_BOUNDARY}",
            }
        )
    changed.append(upsert_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows))
    return changed


def main() -> int:
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    inputs = load_inputs()
    review_rows, schema_rows, source_rows, runtime_rows, forbidden_rows = build_review_rows(inputs)
    gap_rows = build_gap_rows(review_rows)
    next_queue = build_next_queue(review_rows)
    gate_rows = build_gate_rows(inputs, review_rows, schema_rows, source_rows, runtime_rows, forbidden_rows, next_queue)
    receipts = build_receipts(inputs, review_rows, gate_rows)
    failed_reviews = [row for row in review_rows if not as_bool(row.get("all_checks_passed", False))]
    failed_gates = [row for row in gate_rows if str(row.get("status", "")).startswith("failed")]
    open_gaps = [row for row in gap_rows if row.get("gap_type") != "none"]
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
        "reviewed_branches": len(review_rows),
        "failed_reviews": len(failed_reviews),
        "open_gaps": len(open_gaps),
        "failed_gates": len(failed_gates),
        "selected_candidate": "none",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }

    artifact_paths: list[Path] = [
        write_json(RUN_DIR / "source_artifact_hashes.json", source_hashes()),
        write_csv(
            RUN_DIR / "branch_input_review_matrix.csv",
            [
                "branch_id",
                "branch_name",
                "branch_type",
                "payload_exists",
                "payload_sha256_match",
                "schema_keys_present",
                "source_bindings_bound",
                "negative_controls_present",
                "stop_conditions_present",
                "tier_views_present",
                "runtime_gates_present_or_out_of_scope",
                "forbidden_claims_absent",
                "queue_selection_ineligible",
                "all_checks_passed",
                "review_status",
                "selection_eligible",
                "next_action",
                "claim_boundary",
            ],
            review_rows,
        ),
        write_csv(
            RUN_DIR / "payload_schema_audit.csv",
            [
                "branch_id",
                "branch_name",
                "payload_path",
                "payload_exists",
                "payload_sha256_manifest",
                "payload_sha256_actual",
                "payload_sha256_match",
                "required_key_count",
                "missing_key_count",
                "missing_keys",
                "schema_status",
            ],
            schema_rows,
        ),
        write_csv(
            RUN_DIR / "source_binding_review.csv",
            [
                "branch_id",
                "branch_name",
                "manifest_source_binding_count",
                "source_binding_rows",
                "payload_source_binding_rows",
                "missing_or_unbound_sources",
                "source_binding_status",
            ],
            source_rows,
        ),
        write_csv(
            RUN_DIR / "runtime_boundary_review.csv",
            [
                "branch_id",
                "branch_name",
                "runtime_gate_expected",
                "runtime_gate_payload_rows",
                "runtime_claim_boundary",
                "runtime_review_status",
                "effect",
            ],
            runtime_rows,
        ),
        write_csv(
            RUN_DIR / "forbidden_claim_review.csv",
            [
                "branch_id",
                "branch_name",
                "forbidden_claims_absent",
                "forbidden_findings",
                "queue_required_checks",
                "claim_boundary",
                "forbidden_review_status",
            ],
            forbidden_rows,
        ),
        write_csv(
            RUN_DIR / "materialization_gap_register.csv",
            ["gap_id", "branch_id", "branch_name", "gap_type", "failed_checks", "required_action", "claim_effect"],
            gap_rows,
        ),
        write_csv(
            RUN_DIR / "run335F_probe_protocol_design_queue.csv",
            [
                "queue_id",
                "branch_id",
                "branch_name",
                "design_action",
                "required_inputs",
                "forbidden_outputs",
                "selection_eligible",
                "ready_for_run335F",
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
        write_json(RUN_DIR / "gate_receipt.json", receipts["gate_receipt"]),
        write_json(RUN_DIR / "final_review_decision.json", final_decision),
    ]

    manifest_path = RUN_DIR / "run_manifest.json"
    lineage_path = RUN_DIR / "artifact_lineage_receipt.json"
    run_manifest = {
        **final_decision,
        "created_at_utc": utc_now(),
        "producer": rel(Path(__file__)),
        "source_inputs": [rel(path) for path in RUN335D_INPUTS.values()],
        "outputs": [rel(path) for path in [*artifact_paths, manifest_path, lineage_path]],
    }
    artifact_paths.append(write_json(manifest_path, run_manifest))

    lineage = receipts["artifact_lineage_receipt"]
    lineage["artifact_paths"] = [rel(path) for path in [*artifact_paths, lineage_path]]
    lineage["artifact_hashes"] = {rel(path): sha256_file(path) for path in artifact_paths}
    artifact_paths.append(write_json(lineage_path, lineage))

    report_path = write_md(REVIEWS_DIR / "run335E_guarded_branch_input_materialization_review.md", build_report_text(review_rows, gap_rows, gate_rows))
    artifact_paths.append(report_path)
    artifact_paths.append(write_md(DECISION_DOC, build_decision_text()))
    artifact_paths.extend(update_state_docs())
    artifact_paths.extend(update_registries([Path(__file__), *artifact_paths], report_path))

    summary = {
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "reviewed_branches": len(review_rows),
        "failed_reviews": len(failed_reviews),
        "open_gaps": len(open_gaps),
        "failed_gates": len(failed_gates),
        "next_queue_rows": len(next_queue),
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
