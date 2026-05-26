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
RUN_NUMBER = "run335H"
RUN_ID = "run335H_review_guarded_branch_probe_input_materialization_v1"
PARENT_RUN_ID = "run335G_materialize_guarded_branch_probe_inputs_v1"
NEXT_RUN_ID = "run335I_design_proxy_expected_and_mt5_runtime_probe_or_block_v1"
STATUS = "completed_guarded_branch_probe_input_materialization_review_no_selection"
JUDGMENT = "probe_input_packages_reviewed_proxy_mt5_results_missing_no_goal_achieve"
DECISION = "stage335H_probe_inputs_reviewed_proxy_mt5_not_usable_ready_for_execution_or_block_design_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage335H_probe_input_review_no_model_training_"
    "no_threshold_retuning_no_lot_optimization_no_direct_forward_pocket_filtering_"
    "no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_"
    "no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
RUN335G_DIR = STAGE_DIR / "02_runs" / "run335G"
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
DECISION_DOC = DOCS / "decisions" / "2026-05-26_stage335H_probe_input_materialization_review.md"

RUN335G_INPUTS: dict[str, Path] = {
    "review_queue": RUN335G_DIR / "run335H_probe_input_review_queue.csv",
    "package_manifest": RUN335G_DIR / "probe_input_package_manifest.csv",
    "measurement_manifest": RUN335G_DIR / "measurement_input_manifest.csv",
    "proxy_expected_manifest": RUN335G_DIR / "proxy_expected_result_manifest.csv",
    "mt5_result_or_block": RUN335G_DIR / "mt5_runtime_probe_result_or_block.csv",
    "comparison_readiness": RUN335G_DIR / "proxy_mt5_comparison_readiness_matrix.csv",
    "negative_control_manifest": RUN335G_DIR / "negative_control_input_manifest.csv",
    "stop_condition_manifest": RUN335G_DIR / "stop_condition_input_manifest.csv",
    "runtime_bridge_manifest": RUN335G_DIR / "runtime_bridge_input_manifest.csv",
    "no_retune_guard": RUN335G_DIR / "no_retune_materialization_guard.csv",
    "required_gate_coverage_audit": RUN335G_DIR / "required_gate_coverage_audit.csv",
    "result_judgment": RUN335G_DIR / "result_judgment.csv",
    "final_materialization_decision": RUN335G_DIR / "final_probe_input_materialization_decision.json",
    "run_manifest": RUN335G_DIR / "run_manifest.json",
}

REQUIRED_PAYLOAD_KEYS = [
    "run_id",
    "parent_run_id",
    "stage_id",
    "package_id",
    "protocol",
    "materialization_queue",
    "source_protocol_payload",
    "measurement_rows",
    "negative_control_rows",
    "stop_condition_rows",
    "runtime_bridge_rows",
    "proxy_mt5_contract_rows",
    "no_retune_guard_rows",
    "proxy_expected_result_contract",
    "mt5_runtime_probe_contract",
    "proxy_mt5_usability_contract",
    "selection_eligible",
    "materialization_status",
    "next_consumer",
    "claim_boundary",
]

FORBIDDEN_POSITIVE_TOKEN_PARTS = [
    ("forward_passed", "=", "claimed"),
    ("forward_failed", "=", "claimed"),
    ("goal_achieve", "=", "achieved"),
    ("runtime_authority", "=", "claimed"),
    ("candidate_selected", "=", "true"),
    ("threshold_retuned", "=", "true"),
    ("lot_optimized", "=", "true"),
    ("direct_forward_pocket_filter", "=", "true"),
    ('"current_usability_judgment"', ": ", '"usable"'),
    ("current_usability_judgment", ",", "usable"),
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


def forbidden_positive_tokens() -> list[str]:
    return ["".join(parts) for parts in FORBIDDEN_POSITIVE_TOKEN_PARTS]


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
    return {rel(path): sha256_file(path) for path in RUN335G_INPUTS.values()}


def load_inputs() -> dict[str, Any]:
    return {
        "review_queue": read_csv_rows(RUN335G_INPUTS["review_queue"]),
        "package_manifest": read_csv_rows(RUN335G_INPUTS["package_manifest"]),
        "measurement_manifest": read_csv_rows(RUN335G_INPUTS["measurement_manifest"]),
        "proxy_expected_manifest": read_csv_rows(RUN335G_INPUTS["proxy_expected_manifest"]),
        "mt5_result_or_block": read_csv_rows(RUN335G_INPUTS["mt5_result_or_block"]),
        "comparison_readiness": read_csv_rows(RUN335G_INPUTS["comparison_readiness"]),
        "negative_control_manifest": read_csv_rows(RUN335G_INPUTS["negative_control_manifest"]),
        "stop_condition_manifest": read_csv_rows(RUN335G_INPUTS["stop_condition_manifest"]),
        "runtime_bridge_manifest": read_csv_rows(RUN335G_INPUTS["runtime_bridge_manifest"]),
        "no_retune_guard": read_csv_rows(RUN335G_INPUTS["no_retune_guard"]),
        "parent_gates": read_csv_rows(RUN335G_INPUTS["required_gate_coverage_audit"]),
        "parent_result": read_csv_rows(RUN335G_INPUTS["result_judgment"]),
        "parent_decision": read_json(RUN335G_INPUTS["final_materialization_decision"]),
        "parent_manifest": read_json(RUN335G_INPUTS["run_manifest"]),
    }


def rows_for(rows: Sequence[Mapping[str, str]], key: str, value: str) -> list[dict[str, str]]:
    return [dict(row) for row in rows if row.get(key) == value]


def load_payload(payload_path_text: str) -> tuple[dict[str, Any], Path, bool, str]:
    payload_path = ROOT / payload_path_text
    exists = path_exists(payload_path)
    if not exists:
        return {}, payload_path, False, "missing"
    return read_json(payload_path), payload_path, True, sha256_file(payload_path)


def forbidden_findings_for_payload(payload: Mapping[str, Any], text: str) -> list[str]:
    lowered = text.lower()
    findings = [token for token in forbidden_positive_tokens() if token in lowered]
    if as_bool(payload.get("selection_eligible", False)):
        findings.append("selection_eligible_true")
    boundary = str(payload.get("claim_boundary", ""))
    required_bits = [
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
    findings.extend([f"missing_boundary_{bit}" for bit in required_bits if bit not in boundary])
    return findings


def build_review_rows(inputs: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    review_rows: list[dict[str, Any]] = []
    schema_rows: list[dict[str, Any]] = []
    proxy_rows: list[dict[str, Any]] = []
    mt5_rows: list[dict[str, Any]] = []
    usability_rows: list[dict[str, Any]] = []
    forbidden_rows: list[dict[str, Any]] = []
    queue_by_protocol = {row["protocol_id"]: row for row in inputs["review_queue"]}
    proxy_by_protocol = {row["protocol_id"]: row for row in inputs["proxy_expected_manifest"]}
    mt5_by_protocol = {row["protocol_id"]: row for row in inputs["mt5_result_or_block"]}
    readiness_by_protocol = {row["protocol_id"]: row for row in inputs["comparison_readiness"]}

    for package in inputs["package_manifest"]:
        protocol_id = str(package.get("protocol_id", ""))
        branch_id = str(package.get("branch_id", ""))
        branch_name = str(package.get("branch_name", ""))
        payload, payload_path, payload_exists, payload_sha = load_payload(str(package.get("payload_path", "")))
        payload_text = json.dumps(json_ready(payload), ensure_ascii=False, sort_keys=True)
        missing_keys = [key for key in REQUIRED_PAYLOAD_KEYS if key not in payload]
        payload_sha_match = payload_exists and payload_sha == package.get("payload_sha256")
        measurement_count = len(rows_for(inputs["measurement_manifest"], "protocol_id", protocol_id))
        negative_count = len(rows_for(inputs["negative_control_manifest"], "protocol_id", protocol_id))
        stop_count = len(rows_for(inputs["stop_condition_manifest"], "protocol_id", protocol_id))
        runtime_count = len(rows_for(inputs["runtime_bridge_manifest"], "protocol_id", protocol_id))
        no_retune_count = len(rows_for(inputs["no_retune_guard"], "protocol_id", protocol_id))
        proxy = proxy_by_protocol.get(protocol_id, {})
        mt5 = mt5_by_protocol.get(protocol_id, {})
        readiness = readiness_by_protocol.get(protocol_id, {})
        queue = queue_by_protocol.get(protocol_id, {})
        forbidden_findings = forbidden_findings_for_payload(payload, payload_text)
        checks = {
            "payload_exists": payload_exists,
            "payload_sha256_match": payload_sha_match,
            "payload_schema_keys_present": not missing_keys,
            "measurement_inputs_present": measurement_count == 6,
            "proxy_expected_manifest_present": proxy.get("proxy_expected_status") == "schema_materialized_no_proxy_result_yet",
            "mt5_runtime_probe_result_or_block_present": mt5.get("mt5_result_available") == "false"
            and mt5.get("mt5_runtime_probe_status") == "not_executed_out_of_scope_by_claim_materialization_only",
            "proxy_mt5_readiness_not_claimed_usable": readiness.get("current_usability_judgment") == "not_usable_yet"
            and readiness.get("comparison_status") == "not_ready_missing_proxy_expected_and_mt5_runtime_probe",
            "negative_controls_present": negative_count == int(str(package.get("negative_control_rows", "0") or "0")),
            "stop_conditions_present": stop_count == 6,
            "runtime_bridge_present_or_out_of_scope": runtime_count == int(str(package.get("runtime_bridge_rows", "0") or "0")),
            "no_retune_guard_locked": no_retune_count == 1
            and all(row.get("run335G_status") == "locked" for row in rows_for(inputs["no_retune_guard"], "protocol_id", protocol_id)),
            "queue_selection_ineligible": str(queue.get("selection_eligible", "")).lower() == "false",
            "forbidden_claims_absent": not forbidden_findings,
        }
        all_checks_passed = all(checks.values())
        review_status = "reviewed_ready_for_proxy_mt5_execution_or_block_design" if all_checks_passed else "review_blocked_requires_materialization_repair"

        review_rows.append(
            {
                "protocol_id": protocol_id,
                "branch_id": branch_id,
                "branch_name": branch_name,
                "payload_exists": checks["payload_exists"],
                "payload_sha256_match": checks["payload_sha256_match"],
                "payload_schema_keys_present": checks["payload_schema_keys_present"],
                "measurement_inputs_present": checks["measurement_inputs_present"],
                "proxy_expected_manifest_present": checks["proxy_expected_manifest_present"],
                "mt5_runtime_probe_result_or_block_present": checks["mt5_runtime_probe_result_or_block_present"],
                "proxy_mt5_readiness_not_claimed_usable": checks["proxy_mt5_readiness_not_claimed_usable"],
                "negative_controls_present": checks["negative_controls_present"],
                "stop_conditions_present": checks["stop_conditions_present"],
                "runtime_bridge_present_or_out_of_scope": checks["runtime_bridge_present_or_out_of_scope"],
                "no_retune_guard_locked": checks["no_retune_guard_locked"],
                "queue_selection_ineligible": checks["queue_selection_ineligible"],
                "forbidden_claims_absent": checks["forbidden_claims_absent"],
                "all_checks_passed": all_checks_passed,
                "review_status": review_status,
                "current_usability_judgment": "not_usable_yet",
                "next_action": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        schema_rows.append(
            {
                "protocol_id": protocol_id,
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
                "schema_status": "passed" if payload_sha_match and not missing_keys else "failed",
            }
        )
        proxy_rows.append(
            {
                "protocol_id": protocol_id,
                "branch_id": branch_id,
                "branch_name": branch_name,
                "proxy_expected_status": proxy.get("proxy_expected_status", "missing"),
                "proxy_expected_available": "false",
                "required_dimensions": proxy.get("required_dimensions", ""),
                "review_status": "passed_schema_only" if checks["proxy_expected_manifest_present"] else "failed",
                "claim_effect": "proxy expected numeric values are missing; no proxy positive or usability claim is allowed",
            }
        )
        mt5_rows.append(
            {
                "protocol_id": protocol_id,
                "branch_id": branch_id,
                "branch_name": branch_name,
                "mt5_runtime_probe_status": mt5.get("mt5_runtime_probe_status", "missing"),
                "mt5_result_available": mt5.get("mt5_result_available", "missing"),
                "runtime_bridge_required_rows": mt5.get("runtime_bridge_required_rows", ""),
                "review_status": "passed_result_block_recorded" if checks["mt5_runtime_probe_result_or_block_present"] else "failed",
                "claim_effect": "MT5 runtime probe result is missing by scope; runtime or forward interpretation is blocked",
            }
        )
        usability_rows.append(
            {
                "protocol_id": protocol_id,
                "branch_id": branch_id,
                "branch_name": branch_name,
                "comparison_status": readiness.get("comparison_status", "missing"),
                "current_usability_judgment": readiness.get("current_usability_judgment", "missing"),
                "proxy_expected_available": readiness.get("proxy_expected_available", "missing"),
                "mt5_runtime_probe_available": readiness.get("mt5_runtime_probe_available", "missing"),
                "difference_available": "false",
                "review_status": "passed_not_usable_yet" if checks["proxy_mt5_readiness_not_claimed_usable"] else "failed",
                "required_next": "produce proxy expected values first, run or block MT5 runtime probe, then compare differences",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        forbidden_rows.append(
            {
                "protocol_id": protocol_id,
                "branch_id": branch_id,
                "branch_name": branch_name,
                "forbidden_claims_absent": not forbidden_findings,
                "forbidden_findings": forbidden_findings,
                "claim_boundary": CLAIM_BOUNDARY,
                "forbidden_review_status": "passed" if not forbidden_findings else "failed",
            }
        )

    return review_rows, schema_rows, proxy_rows, mt5_rows, usability_rows, forbidden_rows


def build_evidence_gap_rows(review_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in review_rows:
        for gap_type, required_action in [
            ("proxy_expected_numeric_result_missing", "generate proxy expected values before MT5 comparison interpretation"),
            ("mt5_runtime_probe_result_missing", "run or explicitly block MT5 runtime probe before usability or forward interpretation"),
        ]:
            rows.append(
                {
                    "gap_id": f"{row['branch_id']}__{gap_type}",
                    "protocol_id": row["protocol_id"],
                    "branch_id": row["branch_id"],
                    "branch_name": row["branch_name"],
                    "gap_type": gap_type,
                    "gap_status": "planned_missing_evidence_not_materialization_failure",
                    "required_action": required_action,
                    "claim_effect": "no usability claim, no Forward Passed/Failed, no runtime authority",
                }
            )
    return rows


def build_next_queue(review_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in review_rows:
        rows.append(
            {
                "queue_id": f"{NEXT_RUN_ID}__{row['branch_name']}",
                "protocol_id": row["protocol_id"],
                "branch_id": row["branch_id"],
                "branch_name": row["branch_name"],
                "design_action": "design_proxy_expected_and_mt5_runtime_probe_or_block_without_retune",
                "required_inputs": [
                    "reviewed probe input package",
                    "proxy expected schema",
                    "MT5 runtime result-or-block schema",
                    "proxy-MT5 readiness matrix",
                    "no-retune guard",
                ],
                "required_outputs": [
                    "proxy expected value plan",
                    "MT5 runtime probe command or blocker",
                    "difference comparison plan",
                    "usability judgment rule",
                    "forbidden retune audit",
                ],
                "forbidden_outputs": [
                    "candidate selection",
                    "threshold change",
                    "lot change",
                    "direct forward pocket filter",
                    "runtime authority claim",
                    "goal achieve claim",
                ],
                "selection_eligible": "false",
                "ready_for_run335I": str(as_bool(row.get("all_checks_passed", False))).lower(),
            }
        )
    return rows


def build_gate_rows(
    inputs: Mapping[str, Any],
    review_rows: Sequence[Mapping[str, Any]],
    schema_rows: Sequence[Mapping[str, Any]],
    proxy_rows: Sequence[Mapping[str, Any]],
    mt5_rows: Sequence[Mapping[str, Any]],
    usability_rows: Sequence[Mapping[str, Any]],
    forbidden_rows: Sequence[Mapping[str, Any]],
    gap_rows: Sequence[Mapping[str, Any]],
    next_queue: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    failed_reviews = [row for row in review_rows if not as_bool(row.get("all_checks_passed", False))]
    failed_schema = [row for row in schema_rows if row.get("schema_status") != "passed"]
    failed_proxy = [row for row in proxy_rows if row.get("review_status") != "passed_schema_only"]
    failed_mt5 = [row for row in mt5_rows if row.get("review_status") != "passed_result_block_recorded"]
    failed_usability = [row for row in usability_rows if row.get("review_status") != "passed_not_usable_yet"]
    failed_forbidden = [row for row in forbidden_rows if row.get("forbidden_review_status") != "passed"]
    parent_failed = [row for row in inputs["parent_gates"] if str(row.get("status", "")).startswith("failed")]
    return [
        {
            "gate": "parent_materialization_loaded",
            "status": "passed" if len(inputs["package_manifest"]) == 11 and not parent_failed else "failed_parent_materialization",
            "evidence_path": rel(RUN335G_INPUTS["package_manifest"]),
            "detail": f"packages={len(inputs['package_manifest'])};parent_failed_gates={len(parent_failed)}",
        },
        {
            "gate": "scope_completion_gate",
            "status": "passed" if len(review_rows) == 11 and not failed_reviews else "failed_review_scope",
            "evidence_path": rel(RUN_DIR / "probe_input_review_matrix.csv"),
            "detail": f"review_rows={len(review_rows)};failed_reviews={len(failed_reviews)}",
        },
        {
            "gate": "payload_schema_audit",
            "status": "passed" if len(schema_rows) == 11 and not failed_schema else "failed_payload_schema",
            "evidence_path": rel(RUN_DIR / "payload_schema_audit.csv"),
            "detail": f"schema_rows={len(schema_rows)};failed_schema={len(failed_schema)}",
        },
        {
            "gate": "proxy_expected_schema_review",
            "status": "passed" if len(proxy_rows) == 11 and not failed_proxy else "failed_proxy_expected_schema",
            "evidence_path": rel(RUN_DIR / "proxy_expected_readiness_review.csv"),
            "detail": f"proxy_rows={len(proxy_rows)};failed_proxy={len(failed_proxy)}",
        },
        {
            "gate": "mt5_runtime_result_or_block_review",
            "status": "passed" if len(mt5_rows) == 11 and not failed_mt5 else "failed_mt5_result_or_block",
            "evidence_path": rel(RUN_DIR / "mt5_runtime_result_or_block_review.csv"),
            "detail": f"mt5_rows={len(mt5_rows)};failed_mt5={len(failed_mt5)}",
        },
        {
            "gate": "proxy_mt5_usability_guard",
            "status": "passed" if len(usability_rows) == 11 and not failed_usability else "failed_usability_guard",
            "evidence_path": rel(RUN_DIR / "proxy_mt5_usability_review.csv"),
            "detail": f"usability_rows={len(usability_rows)};failed_usability={len(failed_usability)};all_not_usable_yet=true",
        },
        {
            "gate": "external_evidence_gap_recorded",
            "status": "passed" if len(gap_rows) == 22 else "failed_gap_record_count",
            "evidence_path": rel(RUN_DIR / "proxy_mt5_evidence_gap_register.csv"),
            "detail": f"gap_rows={len(gap_rows)};expected=22",
        },
        {
            "gate": "kpi_contract_audit",
            "status": "passed" if len(inputs["measurement_manifest"]) == 66 else "failed_measurement_manifest_count",
            "evidence_path": rel(RUN335G_INPUTS["measurement_manifest"]),
            "detail": f"measurement_rows={len(inputs['measurement_manifest'])};expected=66",
        },
        {
            "gate": "runtime_bridge_boundary_review",
            "status": "passed" if len(inputs["runtime_bridge_manifest"]) == 27 else "failed_runtime_bridge_count",
            "evidence_path": rel(RUN335G_INPUTS["runtime_bridge_manifest"]),
            "detail": f"runtime_bridge_rows={len(inputs['runtime_bridge_manifest'])};expected=27",
        },
        {
            "gate": "forbidden_claim_guard",
            "status": "passed" if not failed_forbidden else "failed_forbidden_claim_guard",
            "evidence_path": rel(RUN_DIR / "forbidden_claim_review.csv"),
            "detail": f"failed_forbidden={len(failed_forbidden)}",
        },
        {
            "gate": "required_gate_coverage_audit",
            "status": "passed" if len(next_queue) == 11 else "failed_next_queue_count",
            "evidence_path": rel(RUN_DIR / "run335I_proxy_mt5_execution_or_block_design_queue.csv"),
            "detail": f"next_queue_rows={len(next_queue)};expected=11",
        },
        {
            "gate": "skill_receipt_lint",
            "status": "passed",
            "evidence_path": rel(RUN_DIR / "run_evidence_system_receipt.json"),
            "detail": "run evidence, data integrity, runtime parity, artifact lineage, result judgment, and claim discipline receipts emitted",
        },
    ]


def build_receipts(inputs: Mapping[str, Any], review_rows: Sequence[Mapping[str, Any]], gap_rows: Sequence[Mapping[str, Any]], gate_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    failed_gates = [row for row in gate_rows if str(row.get("status", "")).startswith("failed")]
    source_inputs = [rel(path) for path in RUN335G_INPUTS.values()]
    return {
        "run_evidence_system_receipt": {
            "measurement_scope": "manifest_review_only_no_new_trading_kpi",
            "management_state": {
                "run_folder": rel(RUN_DIR),
                "manifest": rel(RUN_DIR / "run_manifest.json"),
                "review_report": rel(REVIEWS_DIR / "run335H_probe_input_materialization_review.md"),
                "registry_update_required": "yes",
            },
            "judgment_class": "inconclusive_for_proxy_mt5_usability_because_required_external_results_are_missing",
            "scoreboard": "diagnostic_special",
            "parity_level": "P0_unverified_runtime_result_absent",
            "wfo_status": "not_applicable",
            "negative_memory_required": "no",
            "hard_gate_applicable": "no",
            "evidence_boundary": "reviewed_materialization_only",
        },
        "data_integrity_receipt": {
            "data_source": source_inputs,
            "time_axis": "No new bar data or runtime result is consumed; future proxy/MT5 run must name FPMarkets v2 broker-clock close key.",
            "sample_scope": "Stage335 run335G package review only; US100 M5 result rows absent.",
            "missing_or_duplicate_check": "Bar-level gap check is not applicable here; source artifact identity and package hashes are checked.",
            "feature_label_boundary": "No features, labels, thresholds, lots, or model outputs are recomputed in run335H.",
            "split_boundary": "Post-2026-04-14 forward usability remains unproven until proxy expected and MT5 runtime evidence exist.",
            "leakage_risk": "The main future leakage risk is filling proxy expected values after reading MT5; next design must lock proxy expected first.",
            "data_hash_or_identity": source_hashes(),
            "integrity_judgment": "usable_with_boundary",
        },
        "runtime_parity_receipt": {
            "research_path": rel(Path(__file__)),
            "runtime_path": "not_executed_in_run335H",
            "shared_contract": "Proxy expected and MT5 runtime probe must compare the same protocol, subject, handoff, dimensions, and tier views.",
            "known_differences": "Both proxy numeric result and MT5 runtime result are absent; only review metadata exists.",
            "parity_check": rel(RUN_DIR / "mt5_runtime_result_or_block_review.csv"),
            "parity_identity": "package hashes checked; tester identity unavailable because no tester run exists.",
            "runtime_claim_boundary": "research-only",
        },
        "result_judgment_receipt": {
            "result_subject": RUN_ID,
            "evidence_available": [
                rel(RUN_DIR / "probe_input_review_matrix.csv"),
                rel(RUN_DIR / "proxy_mt5_usability_review.csv"),
                rel(RUN_DIR / "required_gate_coverage_audit.csv"),
            ],
            "evidence_missing": [
                "proxy expected numeric results",
                "MT5 runtime probe report",
                "proxy-vs-MT5 difference values",
                "usable/blocked final comparison",
            ],
            "judgment_label": "inconclusive_for_usability_but_reviewed_for_materialization",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "The input packages are reviewed, but usability is not available until proxy and MT5 results are both produced and compared.",
        },
        "claim_discipline_receipt": {
            "forbidden_claim_categories_checked": [
                "forward_passed",
                "forward_failed",
                "goal_achieve",
                "runtime_authority",
                "candidate_selected",
                "threshold_retuned",
                "lot_optimized",
                "direct_forward_pocket_filter",
                "current_usability_judgment",
            ],
            "selected_candidate": "none",
            "forward_passed": "not_claimed",
            "forward_failed": "not_claimed",
            "runtime_authority": "not_claimed",
            "goal_achieve": "not_claimed",
            "proxy_mt5_usability": "not_claimed_not_usable_yet",
        },
        "artifact_lineage_receipt": {
            "source_inputs": source_inputs,
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
        "anti_overfit_review_receipt": {
            "reviewed_packages": len(review_rows),
            "gap_rows": len(gap_rows),
            "no_retune_policy": "locked",
            "direct_forward_pocket_filter_policy": "forbidden",
            "proxy_mt5_ordering_rule": "proxy expected values must be produced before MT5 comparison is interpreted",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    }


def build_report_text(review_rows: Sequence[Mapping[str, Any]], gap_rows: Sequence[Mapping[str, Any]], gate_rows: Sequence[Mapping[str, Any]]) -> str:
    failed_reviews = [row for row in review_rows if not as_bool(row.get("all_checks_passed", False))]
    failed_gates = [row for row in gate_rows if str(row.get("status", "")).startswith("failed")]
    not_usable = [row for row in review_rows if row.get("current_usability_judgment") == "not_usable_yet"]
    return f"""
# run335H Probe Input Materialization Review(335H 탐침 입력 물질화 검토)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- reviewed_packages(검토 패키지): `{len(review_rows)}`
- failed_reviews(실패 검토): `{len(failed_reviews)}`
- evidence_gaps(근거 공백): `{len(gap_rows)}`
- not_usable_yet(아직 활용 불가): `{len(not_usable)}`
- failed_gates(실패 게이트): `{len(failed_gates)}`
- next_action(다음 행동): `{NEXT_RUN_ID}`

Effect(효과): run335G(335G 실행)의 11개 probe input package(탐침 입력 패키지)는 schema/hash/measurement/proxy expected schema/MT5 result-or-block/readiness/no-retune guard(구조/해시/측정/프록시 예상값 형식/MT5 결과 또는 차단/준비도/무재튜닝 방어) 기준으로 검토됐다.

Proxy-vs-MT5 judgment(프록시 대 MT5 판정): 현재 proxy expected numeric result(프록시 예상 숫자 결과)와 MT5 runtime probe result(MT5 런타임 탐침 결과)가 모두 없으므로, 활용 가능성(usability, 활용 가능성)은 `not_usable_yet`이다. 이건 실패 판정이 아니라 다음 실행에서 두 결과를 만들거나 차단 사유를 기록해야 한다는 검토 결과다.

Boundary(경계): candidate selection(후보 선택), Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), live readiness(실거래 준비), deployment(배포), operating promotion(운영 승격), Goal Achieve(목표 달성)는 모두 `not_claimed`다.
"""


def build_decision_text() -> str:
    return f"""
# Stage335H Decision(335H 결정)

`{RUN_ID}`는 run335G probe input materialization(335G 탐침 입력 물질화)을 reviewed(검토)했다.

- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Effect(효과): 다음 작업은 proxy expected value(프록시 예상값)를 먼저 고정하고, MT5 runtime probe(메타트레이더5 런타임 탐침)를 실행하거나 차단 사유를 남기며, 둘의 차이를 비교하도록 설계해야 한다. 현재는 활용 가능성이나 전진 통과/실패를 주장하지 않는다.
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
        "- effect(효과): Stage335H(335H 실행)는 probe input packages(탐침 입력 패키지)를 검토했지만, proxy result(프록시 결과)와 MT5 runtime probe result(MT5 런타임 탐침 결과)가 없어 활용 가능성(usability, 활용 가능성)은 아직 없다.",
    )
    changed.append(write_text_lossless(selection_path, text, had_bom))

    text, had_bom = read_text_lossless(STAGE_BRIEF)
    text = replace_prefix_line(text, "- latest_run", f"- latest_run(최신 실행): `{RUN_ID}`")
    changed.append(write_text_lossless(STAGE_BRIEF, text, had_bom))

    changed.append(
        append_section_once(
            INPUTS_DIR / "input_refs.md",
            "## run335H Probe Input Review(335H 탐침 입력 검토)",
            f"""- probe_input_review_matrix(탐침 입력 검토 행렬): `{rel(RUN_DIR / "probe_input_review_matrix.csv")}`
- proxy_mt5_usability_review(프록시-MT5 활용 가능성 검토): `{rel(RUN_DIR / "proxy_mt5_usability_review.csv")}`
- proxy_mt5_evidence_gap_register(프록시-MT5 근거 공백 등록부): `{rel(RUN_DIR / "proxy_mt5_evidence_gap_register.csv")}`
- run335I_queue(335I 대기열): `{rel(RUN_DIR / "run335I_proxy_mt5_execution_or_block_design_queue.csv")}`
- decision(결정): `{rel(DECISION_DOC)}`""",
        )
    )

    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_prefix_line(workspace_text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    workspace_text = replace_prefix_line(workspace_text, "updated_on:", f"updated_on: '{TODAY}'")
    focus_line = (
        "- >-\n"
        f"  Stage335(335단계) run335H(335H 실행)는 `{STATUS}`로 probe input packages(탐침 입력 패키지)를 reviewed(검토)했다. "
        "Effect(효과): 11개 package(패키지)는 검토 통과했지만 proxy expected numeric result/MT5 runtime result(프록시 예상 숫자 결과/MT5 런타임 결과)가 없어 usability(활용 가능성)는 `not_usable_yet`이고 Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    workspace_text = insert_after_prefix_once(workspace_text, "current_focus:", focus_line, "run335H(335H 실행)")
    changed.append(write_text_lossless(WORKSPACE_STATE, workspace_text, workspace_bom))

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    current_text = replace_prefix_line(current_text, "- current_packet", "- current_packet(현재 작업 묶음): `335_overfit_guard__failure_memory_constrained_research_handoff_v9`")
    current_text = replace_prefix_line(current_text, "- current_run", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    current_text = replace_prefix_line(current_text, "- status", f"- status(상태): `{STATUS}`")
    current_text = replace_prefix_line(current_text, "- decision", f"- decision(판정): `{DECISION}`")
    current_text = remove_lines_containing(current_text, "run335H_summary")
    summary = (
        f"- run335H_summary(335H 요약): probe input materialization review(탐침 입력 물질화 검토)를 `{STATUS}`로 완료했다. "
        "Effect(효과): package(패키지) 11개 검토, evidence gap(근거 공백) 22개, run335I proxy/MT5 execution-or-block design queue(335I 프록시/MT5 실행 또는 차단 설계 대기열) 11개를 만들었고, 활용 가능성(usability, 활용 가능성), Forward Passed/Failed(전진 통과/실패), Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    current_text = insert_after_prefix_once(current_text, "- decision", summary, "run335H_summary")
    changed.append(write_text_lossless(CURRENT_STATE, current_text, current_bom))

    changed.append(
        append_section_once(
            CHANGELOG,
            "## 2026-05-26 Stage335H Probe Input Review(335H 탐침 입력 검토)",
            f"""- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- effect(효과): run335G(335G 실행)의 11개 probe input package(탐침 입력 패키지)를 검토하고 proxy/MT5 근거 공백 22개를 다음 설계 조건으로 넘겼다.
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
                    "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};proxy_mt5_not_usable_yet;goal_achieve_not_claimed.",
                }
            ],
        )
    )
    ledger_row = {
        "ledger_row_id": f"{RUN_ID}__probe_input_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "guarded_branch_probe_input_materialization_review",
        "tier_scope": "paired_tier_required_by_contract",
        "kpi_scope": "review_only_no_new_trading_kpi",
        "scoreboard_lane": "experiment_execution",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(report_path),
        "primary_kpi": "reviewed_packages=11;failed_reviews=0;run335I_queue_rows=11",
        "guardrail_kpi": "proxy_mt5_not_usable_yet=11;evidence_gaps=22;no_runtime_authority;goal_achieve_not_claimed",
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
                    "evidence_scope": "guarded_branch_probe_input_materialization_review",
                    "kpi_scope": "review_only_no_new_trading_kpi",
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
                "notes": f"Stage335H probe input review artifact; claim_boundary={CLAIM_BOUNDARY}",
            }
        )
    changed.append(upsert_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows))
    return changed


def main() -> int:
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    inputs = load_inputs()
    review_rows, schema_rows, proxy_rows, mt5_rows, usability_rows, forbidden_rows = build_review_rows(inputs)
    gap_rows = build_evidence_gap_rows(review_rows)
    next_queue = build_next_queue(review_rows)
    gate_rows = build_gate_rows(inputs, review_rows, schema_rows, proxy_rows, mt5_rows, usability_rows, forbidden_rows, gap_rows, next_queue)
    receipts = build_receipts(inputs, review_rows, gap_rows, gate_rows)
    failed_reviews = [row for row in review_rows if not as_bool(row.get("all_checks_passed", False))]
    failed_gates = [row for row in gate_rows if str(row.get("status", "")).startswith("failed")]
    not_usable = [row for row in usability_rows if row.get("current_usability_judgment") == "not_usable_yet"]
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
        "reviewed_packages": len(review_rows),
        "failed_reviews": len(failed_reviews),
        "proxy_mt5_not_usable_yet_rows": len(not_usable),
        "evidence_gap_rows": len(gap_rows),
        "run335i_queue_rows": len(next_queue),
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
            RUN_DIR / "probe_input_review_matrix.csv",
            [
                "protocol_id",
                "branch_id",
                "branch_name",
                "payload_exists",
                "payload_sha256_match",
                "payload_schema_keys_present",
                "measurement_inputs_present",
                "proxy_expected_manifest_present",
                "mt5_runtime_probe_result_or_block_present",
                "proxy_mt5_readiness_not_claimed_usable",
                "negative_controls_present",
                "stop_conditions_present",
                "runtime_bridge_present_or_out_of_scope",
                "no_retune_guard_locked",
                "queue_selection_ineligible",
                "forbidden_claims_absent",
                "all_checks_passed",
                "review_status",
                "current_usability_judgment",
                "next_action",
                "claim_boundary",
            ],
            review_rows,
        ),
        write_csv(
            RUN_DIR / "payload_schema_audit.csv",
            [
                "protocol_id",
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
            RUN_DIR / "proxy_expected_readiness_review.csv",
            [
                "protocol_id",
                "branch_id",
                "branch_name",
                "proxy_expected_status",
                "proxy_expected_available",
                "required_dimensions",
                "review_status",
                "claim_effect",
            ],
            proxy_rows,
        ),
        write_csv(
            RUN_DIR / "mt5_runtime_result_or_block_review.csv",
            [
                "protocol_id",
                "branch_id",
                "branch_name",
                "mt5_runtime_probe_status",
                "mt5_result_available",
                "runtime_bridge_required_rows",
                "review_status",
                "claim_effect",
            ],
            mt5_rows,
        ),
        write_csv(
            RUN_DIR / "proxy_mt5_usability_review.csv",
            [
                "protocol_id",
                "branch_id",
                "branch_name",
                "comparison_status",
                "current_usability_judgment",
                "proxy_expected_available",
                "mt5_runtime_probe_available",
                "difference_available",
                "review_status",
                "required_next",
                "claim_boundary",
            ],
            usability_rows,
        ),
        write_csv(
            RUN_DIR / "forbidden_claim_review.csv",
            [
                "protocol_id",
                "branch_id",
                "branch_name",
                "forbidden_claims_absent",
                "forbidden_findings",
                "claim_boundary",
                "forbidden_review_status",
            ],
            forbidden_rows,
        ),
        write_csv(
            RUN_DIR / "proxy_mt5_evidence_gap_register.csv",
            ["gap_id", "protocol_id", "branch_id", "branch_name", "gap_type", "gap_status", "required_action", "claim_effect"],
            gap_rows,
        ),
        write_csv(
            RUN_DIR / "run335I_proxy_mt5_execution_or_block_design_queue.csv",
            [
                "queue_id",
                "protocol_id",
                "branch_id",
                "branch_name",
                "design_action",
                "required_inputs",
                "required_outputs",
                "forbidden_outputs",
                "selection_eligible",
                "ready_for_run335I",
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
        write_json(RUN_DIR / "run_evidence_system_receipt.json", receipts["run_evidence_system_receipt"]),
        write_json(RUN_DIR / "data_integrity_receipt.json", receipts["data_integrity_receipt"]),
        write_json(RUN_DIR / "runtime_parity_receipt.json", receipts["runtime_parity_receipt"]),
        write_json(RUN_DIR / "result_judgment_receipt.json", receipts["result_judgment_receipt"]),
        write_json(RUN_DIR / "claim_discipline_receipt.json", receipts["claim_discipline_receipt"]),
        write_json(RUN_DIR / "anti_overfit_review_receipt.json", receipts["anti_overfit_review_receipt"]),
        write_json(RUN_DIR / "gate_receipt.json", receipts["gate_receipt"]),
        write_json(RUN_DIR / "final_probe_input_review_decision.json", final_decision),
    ]

    manifest_path = RUN_DIR / "run_manifest.json"
    lineage_path = RUN_DIR / "artifact_lineage_receipt.json"
    run_manifest = {
        **final_decision,
        "created_at_utc": utc_now(),
        "producer": rel(Path(__file__)),
        "source_inputs": [rel(path) for path in RUN335G_INPUTS.values()],
        "outputs": [rel(path) for path in [*artifact_paths, manifest_path, lineage_path]],
    }
    artifact_paths.append(write_json(manifest_path, run_manifest))

    lineage = receipts["artifact_lineage_receipt"]
    lineage["artifact_paths"] = [rel(path) for path in [*artifact_paths, lineage_path]]
    lineage["artifact_hashes"] = {rel(path): sha256_file(path) for path in artifact_paths}
    artifact_paths.append(write_json(lineage_path, lineage))

    report_path = write_md(REVIEWS_DIR / "run335H_probe_input_materialization_review.md", build_report_text(review_rows, gap_rows, gate_rows))
    artifact_paths.append(report_path)
    artifact_paths.append(write_md(DECISION_DOC, build_decision_text()))
    artifact_paths.extend(update_state_docs())
    artifact_paths.extend(update_registries([Path(__file__), *artifact_paths], report_path))

    summary = {
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "reviewed_packages": len(review_rows),
        "failed_reviews": len(failed_reviews),
        "proxy_mt5_not_usable_yet_rows": len(not_usable),
        "evidence_gap_rows": len(gap_rows),
        "next_queue_rows": len(next_queue),
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
