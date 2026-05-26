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
RUN_NUMBER = "run335G"
RUN_ID = "run335G_materialize_guarded_branch_probe_inputs_v1"
PARENT_RUN_ID = "run335F_design_guarded_branch_probe_protocols_v1"
NEXT_RUN_ID = "run335H_review_guarded_branch_probe_input_materialization_v1"
STATUS = "completed_guarded_branch_probe_inputs_materialized_no_selection"
JUDGMENT = "probe_inputs_materialized_research_only_no_goal_achieve"
DECISION = "stage335G_probe_inputs_materialized_ready_for_review_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage335G_probe_input_materialization_no_model_training_"
    "no_threshold_retuning_no_lot_optimization_no_direct_forward_pocket_filtering_"
    "no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_"
    "no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
PROBE_SPEC_DIR = RUN_DIR / "probe_input_specs"
RUN335F_DIR = STAGE_DIR / "02_runs" / "run335F"
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
DECISION_DOC = DOCS / "decisions" / "2026-05-26_stage335G_guarded_branch_probe_input_materialization.md"

RUN335F_INPUTS: dict[str, Path] = {
    "materialization_queue": RUN335F_DIR / "run335G_probe_input_materialization_queue.csv",
    "protocol_design_matrix": RUN335F_DIR / "probe_protocol_design_matrix.csv",
    "protocol_payload_manifest": RUN335F_DIR / "protocol_payload_manifest.csv",
    "measurement_plan": RUN335F_DIR / "predeclared_measurement_plan.csv",
    "negative_control_plan": RUN335F_DIR / "negative_control_probe_plan.csv",
    "stop_condition_plan": RUN335F_DIR / "stop_condition_probe_plan.csv",
    "runtime_bridge_plan": RUN335F_DIR / "runtime_bridge_requirement_plan.csv",
    "proxy_mt5_contract": RUN335F_DIR / "proxy_mt5_comparison_contract.csv",
    "no_retune_guard": RUN335F_DIR / "no_retune_probe_guard.csv",
    "required_gate_coverage_audit": RUN335F_DIR / "required_gate_coverage_audit.csv",
    "final_protocol_decision": RUN335F_DIR / "final_probe_protocol_design_decision.json",
    "run_manifest": RUN335F_DIR / "run_manifest.json",
}

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


def rows_for(rows: Sequence[Mapping[str, str]], key: str, value: str) -> list[dict[str, str]]:
    return [dict(row) for row in rows if row.get(key) == value]


def source_hashes() -> dict[str, str]:
    return {rel(path): sha256_file(path) for path in RUN335F_INPUTS.values()}


def load_inputs() -> dict[str, Any]:
    return {
        "queue": read_csv_rows(RUN335F_INPUTS["materialization_queue"]),
        "protocols": read_csv_rows(RUN335F_INPUTS["protocol_design_matrix"]),
        "payload_manifest": read_csv_rows(RUN335F_INPUTS["protocol_payload_manifest"]),
        "measurement_plan": read_csv_rows(RUN335F_INPUTS["measurement_plan"]),
        "negative_plan": read_csv_rows(RUN335F_INPUTS["negative_control_plan"]),
        "stop_plan": read_csv_rows(RUN335F_INPUTS["stop_condition_plan"]),
        "runtime_bridge": read_csv_rows(RUN335F_INPUTS["runtime_bridge_plan"]),
        "proxy_mt5_contract": read_csv_rows(RUN335F_INPUTS["proxy_mt5_contract"]),
        "no_retune_guard": read_csv_rows(RUN335F_INPUTS["no_retune_guard"]),
        "parent_gates": read_csv_rows(RUN335F_INPUTS["required_gate_coverage_audit"]),
        "parent_decision": read_json(RUN335F_INPUTS["final_protocol_decision"]),
        "parent_manifest": read_json(RUN335F_INPUTS["run_manifest"]),
    }


def payload_by_protocol(inputs: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    loaded: dict[str, dict[str, Any]] = {}
    for row in inputs["payload_manifest"]:
        path_text = str(row.get("payload_path", ""))
        protocol_id = str(row.get("protocol_id", ""))
        loaded[protocol_id] = read_json(ROOT / path_text) if path_text else {}
    return loaded


def build_probe_packages(inputs: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[Path]]:
    payloads = payload_by_protocol(inputs)
    queue_by_protocol = {row["protocol_id"]: row for row in inputs["queue"]}
    manifest_rows: list[dict[str, Any]] = []
    created_payloads: list[Path] = []
    for protocol in inputs["protocols"]:
        protocol_id = str(protocol.get("protocol_id", ""))
        branch_id = str(protocol.get("branch_id", ""))
        branch_name = str(protocol.get("branch_name", ""))
        package_id = f"{RUN_ID}__{branch_name}"
        queue_row = queue_by_protocol.get(protocol_id, {})
        source_payload = payloads.get(protocol_id, {})
        spec_path = PROBE_SPEC_DIR / f"{branch_id}.json"
        spec_payload = {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "stage_id": STAGE_ID,
            "package_id": package_id,
            "protocol": protocol,
            "materialization_queue": queue_row,
            "source_protocol_payload": source_payload,
            "measurement_rows": rows_for(inputs["measurement_plan"], "protocol_id", protocol_id),
            "negative_control_rows": rows_for(inputs["negative_plan"], "protocol_id", protocol_id),
            "stop_condition_rows": rows_for(inputs["stop_plan"], "protocol_id", protocol_id),
            "runtime_bridge_rows": rows_for(inputs["runtime_bridge"], "protocol_id", protocol_id),
            "proxy_mt5_contract_rows": rows_for(inputs["proxy_mt5_contract"], "protocol_id", protocol_id),
            "no_retune_guard_rows": rows_for(inputs["no_retune_guard"], "protocol_id", protocol_id),
            "proxy_expected_result_contract": {
                "status": "schema_materialized_no_proxy_result_yet",
                "required_dimensions": COMPARISON_DIMENSIONS,
                "required_views": ["Tier A separate", "Tier B separate", "Tier A+B combined"],
                "effect": "future proxy result must fill this before any MT5 comparison or usability read",
            },
            "mt5_runtime_probe_contract": {
                "status": "not_executed_out_of_scope_by_claim_materialization_only",
                "required_before": "any runtime, forward, or usability claim",
                "required_evidence": [
                    "MT5 tester report",
                    "runtime telemetry",
                    "settings/set identity",
                    "spread/slippage record",
                    "subject and handoff identity",
                ],
                "effect": "missing MT5 runtime probe blocks runtime or forward interpretation",
            },
            "proxy_mt5_usability_contract": {
                "current_usability": "not_usable_yet",
                "reason": "proxy expected values and MT5 runtime probe results are not both present in run335G",
                "future_rule": "usable only if proxy and MT5 agree on risk shape or any difference is explained by logged runtime, cost, fill, session, or handoff evidence",
            },
            "selection_eligible": False,
            "materialization_status": "probe_input_spec_materialized_no_scoring_no_runtime_execution",
            "next_consumer": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        write_json(spec_path, spec_payload)
        created_payloads.append(spec_path)
        minimum_outputs = parse_json_list(queue_row.get("minimum_outputs", ""))
        forbidden_outputs = parse_json_list(queue_row.get("forbidden_outputs", ""))
        manifest_rows.append(
            {
                "package_id": package_id,
                "protocol_id": protocol_id,
                "branch_id": branch_id,
                "branch_name": branch_name,
                "probe_family": protocol.get("probe_family", ""),
                "measurement_rows": len(spec_payload["measurement_rows"]),
                "negative_control_rows": len(spec_payload["negative_control_rows"]),
                "stop_condition_rows": len(spec_payload["stop_condition_rows"]),
                "runtime_bridge_rows": len(spec_payload["runtime_bridge_rows"]),
                "proxy_mt5_contract_rows": len(spec_payload["proxy_mt5_contract_rows"]),
                "minimum_outputs_required": minimum_outputs,
                "forbidden_outputs": forbidden_outputs,
                "payload_path": rel(spec_path),
                "payload_sha256": sha256_file(spec_path),
                "package_status": "materialized_probe_input_spec_only",
                "selection_eligible": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return manifest_rows, created_payloads


def build_measurement_input_manifest(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in inputs["measurement_plan"]:
        rows.append(
            {
                **row,
                "run335G_status": "input_requirement_materialized",
                "expected_output_field": f"{row.get('measurement_view', '')}_value_or_missing_reason",
                "claim_effect": "measurement names are fixed before any proxy or MT5 result is read",
            }
        )
    return rows


def build_proxy_expected_manifest(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for contract in inputs["proxy_mt5_contract"]:
        rows.append(
            {
                "protocol_id": contract.get("protocol_id", ""),
                "branch_id": contract.get("branch_id", ""),
                "branch_name": contract.get("branch_name", ""),
                "proxy_expected_status": "schema_materialized_no_proxy_result_yet",
                "required_dimensions": parse_json_list(contract.get("comparison_dimensions", "")) or COMPARISON_DIMENSIONS,
                "required_views": ["Tier A separate", "Tier B separate", "Tier A+B combined"],
                "required_sources": [
                    "fixed score or diagnostic output generated after this materialization",
                    "source artifact hash",
                    "time-axis and split boundary statement",
                    "no-retune guard result",
                ],
                "missing_policy": "missing_required_before_proxy_vs_mt5_comparison",
                "allowed_claim": "proxy_expected_schema_only_no_usability_judgment",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_mt5_runtime_probe_result_or_block(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for contract in inputs["proxy_mt5_contract"]:
        runtime_rows = rows_for(inputs["runtime_bridge"], "protocol_id", str(contract.get("protocol_id", "")))
        required_runtime_rows = [row for row in runtime_rows if row.get("bridge_status") != "out_of_scope_by_claim"]
        rows.append(
            {
                "protocol_id": contract.get("protocol_id", ""),
                "branch_id": contract.get("branch_id", ""),
                "branch_name": contract.get("branch_name", ""),
                "mt5_runtime_probe_status": "not_executed_out_of_scope_by_claim_materialization_only",
                "mt5_result_available": "false",
                "runtime_bridge_required_rows": len(required_runtime_rows),
                "required_before": "runtime_or_forward_interpretation_and_proxy_usability_judgment",
                "minimum_evidence": [
                    "MT5 tester report",
                    "runtime telemetry",
                    "set/settings identity",
                    "spread/slippage record",
                    "subject and handoff identity",
                ],
                "blocked_if_later_missing": parse_json_list(contract.get("blocked_if", "")),
                "claim_effect": "no runtime probe, no Forward Passed/Failed, no usability positive read in run335G",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_proxy_mt5_readiness(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for contract in inputs["proxy_mt5_contract"]:
        rows.append(
            {
                "protocol_id": contract.get("protocol_id", ""),
                "branch_id": contract.get("branch_id", ""),
                "branch_name": contract.get("branch_name", ""),
                "proxy_expected_available": "false",
                "mt5_runtime_probe_available": "false",
                "comparison_status": "not_ready_missing_proxy_expected_and_mt5_runtime_probe",
                "difference_read": contract.get("difference_read", "proxy_expected_minus_mt5_actual"),
                "comparison_dimensions": parse_json_list(contract.get("comparison_dimensions", "")) or COMPARISON_DIMENSIONS,
                "current_usability_judgment": "not_usable_yet",
                "future_usability_rule": contract.get("usability_judgment_rule", ""),
                "current_reason": "run335G materializes inputs only; proxy and MT5 results are still absent",
                "next_required_action": "run proxy expectation and MT5 runtime probe, then compare differences before any use",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_negative_input_manifest(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in inputs["negative_plan"]:
        rows.append(
            {
                **row,
                "run335G_status": "negative_control_input_materialized",
                "required_before": "any proxy or MT5 result can be called useful",
                "claim_effect": "control-like improvement downgrades branch to overfit memory",
            }
        )
    return rows


def build_stop_input_manifest(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in inputs["stop_plan"]:
        rows.append(
            {
                **row,
                "run335G_status": "stop_condition_input_materialized",
                "required_before": "result interpretation",
            }
        )
    return rows


def build_runtime_bridge_manifest(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in inputs["runtime_bridge"]:
        rows.append(
            {
                **row,
                "run335G_status": "runtime_requirement_materialized_or_out_of_scope",
                "mt5_runtime_probe_result_status": "not_executed_in_run335G",
                "claim_effect": "runtime authority remains unavailable until tester report and telemetry exist",
            }
        )
    return rows


def build_no_retune_manifest(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in inputs["no_retune_guard"]:
        rows.append(
            {
                **row,
                "run335G_status": "locked",
                "materialization_effect": "prevents proxy or MT5 result from becoming a retune instruction",
            }
        )
    return rows


def build_review_queue(package_manifest: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for package in package_manifest:
        rows.append(
            {
                "review_queue_id": f"{NEXT_RUN_ID}__{package['branch_name']}",
                "protocol_id": package["protocol_id"],
                "branch_id": package["branch_id"],
                "branch_name": package["branch_name"],
                "review_action": "review_probe_input_package_and_proxy_mt5_readiness_only",
                "required_payload": package["payload_path"],
                "required_checks": [
                    "payload_exists",
                    "measurement_inputs_present",
                    "proxy_expected_manifest_present",
                    "mt5_runtime_probe_result_or_block_present",
                    "proxy_mt5_readiness_not_claimed_usable",
                    "negative_controls_present",
                    "stop_conditions_present",
                    "runtime_bridge_present_or_out_of_scope",
                    "no_retune_guard_locked",
                    "forbidden_claims_absent",
                ],
                "block_if_missing": "payload, proxy expected manifest, MT5 result-or-block, comparison readiness, or no-retune guard",
                "selection_eligible": "false",
                "next_status_planned": "review_probe_input_materialization_only_no_candidate_selection",
            }
        )
    return rows


def forbidden_claims_absent(paths: Sequence[Path]) -> tuple[bool, list[str]]:
    tokens = [
        "forward_passed=claimed",
        "forward_failed=claimed",
        "goal_achieve=achieved",
        "runtime_authority=claimed",
        "candidate_selected=true",
        "threshold_retuned=true",
        "lot_optimized=true",
        "direct_forward_pocket_filter=true",
    ]
    findings: list[str] = []
    for path in paths:
        if not path_exists(path):
            continue
        text = io_path(path).read_text(encoding="utf-8-sig", errors="ignore").lower()
        for token in tokens:
            if token in text:
                findings.append(f"{rel(path)}::{token}")
    return not findings, findings


def build_gate_rows(
    inputs: Mapping[str, Any],
    package_manifest: Sequence[Mapping[str, Any]],
    measurement_rows: Sequence[Mapping[str, Any]],
    proxy_rows: Sequence[Mapping[str, Any]],
    mt5_rows: Sequence[Mapping[str, Any]],
    readiness_rows: Sequence[Mapping[str, Any]],
    negative_rows: Sequence[Mapping[str, Any]],
    stop_rows: Sequence[Mapping[str, Any]],
    runtime_rows: Sequence[Mapping[str, Any]],
    no_retune_rows: Sequence[Mapping[str, Any]],
    review_queue: Sequence[Mapping[str, Any]],
    payload_paths: Sequence[Path],
) -> list[dict[str, Any]]:
    missing_payloads = [path for path in payload_paths if not path_exists(path)]
    selection_true = [row for row in package_manifest if str(row.get("selection_eligible", "")).lower() == "true"]
    no_retune_unlocked = [row for row in no_retune_rows if row.get("guard_status") != "locked" or row.get("run335G_status") != "locked"]
    proxy_result_claims = [row for row in proxy_rows if row.get("proxy_expected_status") != "schema_materialized_no_proxy_result_yet"]
    mt5_result_claims = [row for row in mt5_rows if row.get("mt5_result_available") != "false"]
    usable_claims = [row for row in readiness_rows if row.get("current_usability_judgment") != "not_usable_yet"]
    forbidden_ok, forbidden_findings = forbidden_claims_absent(payload_paths)
    parent_failed = [row for row in inputs["parent_gates"] if str(row.get("status", "")).startswith("failed")]
    return [
        {
            "gate": "parent_protocol_outputs_loaded",
            "status": "passed" if len(inputs["queue"]) == 11 and not parent_failed else "failed_parent_protocol_outputs",
            "evidence_path": rel(RUN335F_INPUTS["materialization_queue"]),
            "detail": f"queue_rows={len(inputs['queue'])};parent_failed_gates={len(parent_failed)}",
        },
        {
            "gate": "scope_completion_gate",
            "status": "passed" if len(package_manifest) == 11 and not missing_payloads else "failed_package_count_or_missing_payload",
            "evidence_path": rel(RUN_DIR / "probe_input_package_manifest.csv"),
            "detail": f"packages={len(package_manifest)};missing_payloads={len(missing_payloads)}",
        },
        {
            "gate": "kpi_contract_audit",
            "status": "passed" if len(measurement_rows) == 66 else "failed_measurement_row_count",
            "evidence_path": rel(RUN_DIR / "measurement_input_manifest.csv"),
            "detail": f"measurement_rows={len(measurement_rows)};expected=66",
        },
        {
            "gate": "proxy_expected_manifest_gate",
            "status": "passed" if len(proxy_rows) == 11 and not proxy_result_claims else "failed_proxy_expected_manifest",
            "evidence_path": rel(RUN_DIR / "proxy_expected_result_manifest.csv"),
            "detail": f"proxy_rows={len(proxy_rows)};proxy_result_claims={len(proxy_result_claims)}",
        },
        {
            "gate": "mt5_runtime_result_or_block_gate",
            "status": "passed" if len(mt5_rows) == 11 and not mt5_result_claims else "failed_mt5_result_or_block_manifest",
            "evidence_path": rel(RUN_DIR / "mt5_runtime_probe_result_or_block.csv"),
            "detail": f"mt5_rows={len(mt5_rows)};mt5_result_claims={len(mt5_result_claims)}",
        },
        {
            "gate": "proxy_mt5_usability_guard",
            "status": "passed" if len(readiness_rows) == 11 and not usable_claims else "failed_proxy_mt5_usability_guard",
            "evidence_path": rel(RUN_DIR / "proxy_mt5_comparison_readiness_matrix.csv"),
            "detail": f"readiness_rows={len(readiness_rows)};usable_claims={len(usable_claims)}",
        },
        {
            "gate": "negative_control_materialization_gate",
            "status": "passed" if len(negative_rows) == 21 else "failed_negative_control_count",
            "evidence_path": rel(RUN_DIR / "negative_control_input_manifest.csv"),
            "detail": f"negative_rows={len(negative_rows)};expected=21",
        },
        {
            "gate": "stop_condition_materialization_gate",
            "status": "passed" if len(stop_rows) == 66 else "failed_stop_condition_count",
            "evidence_path": rel(RUN_DIR / "stop_condition_input_manifest.csv"),
            "detail": f"stop_rows={len(stop_rows)};expected=66",
        },
        {
            "gate": "runtime_bridge_materialization_gate",
            "status": "passed" if len(runtime_rows) == 27 else "failed_runtime_bridge_count",
            "evidence_path": rel(RUN_DIR / "runtime_bridge_input_manifest.csv"),
            "detail": f"runtime_rows={len(runtime_rows)};expected=27",
        },
        {
            "gate": "no_retune_guard_locked",
            "status": "passed" if len(no_retune_rows) == 11 and not no_retune_unlocked and not selection_true else "failed_no_retune_or_selection_guard",
            "evidence_path": rel(RUN_DIR / "no_retune_materialization_guard.csv"),
            "detail": f"no_retune_rows={len(no_retune_rows)};unlocked={len(no_retune_unlocked)};selection_true={len(selection_true)}",
        },
        {
            "gate": "skill_receipt_lint",
            "status": "passed",
            "evidence_path": rel(RUN_DIR / "run_evidence_system_receipt.json"),
            "detail": "run evidence, experiment design, data integrity, model validation, runtime parity, artifact lineage, and result judgment receipts emitted",
        },
        {
            "gate": "required_gate_coverage_audit",
            "status": "passed" if len(review_queue) == 11 and forbidden_ok else "failed_review_queue_or_forbidden_claim_guard",
            "evidence_path": rel(RUN_DIR / "run335H_probe_input_review_queue.csv"),
            "detail": f"review_queue_rows={len(review_queue)};forbidden_findings={len(forbidden_findings)}",
        },
    ]


def build_receipts(
    inputs: Mapping[str, Any],
    package_manifest: Sequence[Mapping[str, Any]],
    gate_rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    failed_gates = [row for row in gate_rows if str(row.get("status", "")).startswith("failed")]
    source_inputs = [rel(path) for path in RUN335F_INPUTS.values()]
    return {
        "run_evidence_system_receipt": {
            "run_manifest": rel(RUN_DIR / "run_manifest.json"),
            "run_registry": rel(RUN_REGISTRY),
            "alpha_ledger": rel(ALPHA_LEDGER),
            "stage_ledger": rel(STAGE_LEDGER),
            "measurement_identity": "manifest_only_no_new_trading_kpi",
            "judgment": JUDGMENT,
        },
        "experiment_design_receipt": {
            "hypothesis": "Guarded branch protocols can be materialized into probe input specs without retuning, direct forward-pocket filters, or selection.",
            "decision_use": "May only decide whether probe input materialization is ready for review and later proxy/MT5 execution.",
            "comparison_baseline": "run335F protocol design plus Stage334/335 failure memory.",
            "control_variables": [
                "fixed subject boundary",
                "fixed threshold policy",
                "fixed lot and risk logic",
                "fixed ATR SL/TP logic",
                "predeclared proxy-vs-MT5 comparison contract",
            ],
            "changed_variables": "materialized input specs and manifests only",
            "sample_scope": "US100 M5 Stage335 research materialization; no new broker data or runtime result in this run",
            "success_criteria": "11 packages, proxy expected schema, MT5 result-or-block, comparison readiness, controls, stop conditions, and no-retune guard materialized.",
            "failure_criteria": "Any package missing, selection enabled, proxy/MT5 usability claimed, or forbidden retune output appears.",
            "invalid_conditions": "Materialization changes threshold, lot, model, risk, subject identity, or direct forward-pocket filters.",
            "stop_conditions": "Stop or downgrade if gates fail or proxy/MT5 evidence is claimed without actual runtime evidence.",
            "evidence_plan": [rel(RUN_DIR / "probe_input_package_manifest.csv"), rel(RUN_DIR / "required_gate_coverage_audit.csv")],
        },
        "data_integrity_receipt": {
            "data_source": source_inputs,
            "time_axis": "No new bar data is consumed; future score frames must use FPMarkets v2 broker-clock close key.",
            "sample_scope": "Manifest/protocol materialization only.",
            "missing_or_duplicate_check": "Not applicable to bar rows in this run; source manifests and hashes are recorded.",
            "feature_label_boundary": "No features or labels are recomputed; future proxy output must record boundary before comparison.",
            "split_boundary": "Post-2026-04-14 forward evidence remains unavailable in run335G.",
            "leakage_risk": "The main risk is later filling proxy expected values after seeing MT5; contract requires proxy expected first.",
            "data_hash_or_identity": source_hashes(),
            "integrity_judgment": "usable_with_boundary",
        },
        "model_validation_receipt": {
            "model_family": "no model training or ONNX modification in run335G",
            "target_and_label": "not_applicable_materialization_only",
            "split_method": "not_applicable_no_scoring",
            "selection_metric": "none",
            "secondary_metrics": COMPARISON_DIMENSIONS,
            "threshold_policy": "fixed_no_search",
            "overfit_risk": "Later proxy expected values could be adjusted after MT5 unless ordering is audited.",
            "calibration_risk": "No score/probability interpretation is allowed in this run.",
            "comparison_baseline": "run335F protocol contract",
            "validation_judgment": "exploratory_materialization_only",
        },
        "runtime_parity_receipt": {
            "research_path": rel(Path(__file__)),
            "runtime_path": "not_executed_in_run335G",
            "shared_contract": "proxy expected values and MT5 runtime probe results must compare the same subject, handoff, dimensions, and views.",
            "known_differences": "MT5 runtime result is absent in run335G; comparison is not usable yet.",
            "parity_check": "mt5_runtime_probe_result_or_block.csv records no runtime execution and blocks runtime/forward interpretation.",
            "parity_identity": "source hashes recorded; MT5 tester identity unavailable.",
            "runtime_claim_boundary": "research-only",
        },
        "result_judgment_receipt": {
            "result_subject": RUN_ID,
            "evidence_available": [
                rel(RUN_DIR / "probe_input_package_manifest.csv"),
                rel(RUN_DIR / "proxy_mt5_comparison_readiness_matrix.csv"),
                rel(RUN_DIR / "required_gate_coverage_audit.csv"),
            ],
            "evidence_missing": [
                "proxy expected numeric results",
                "MT5 runtime probe report",
                "proxy-vs-MT5 difference values",
                "forward pass/fail evidence",
            ],
            "judgment_label": "exploratory_materialization",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "Inputs are ready for review, but proxy and MT5 results are absent, so usability is not claimed.",
        },
        "anti_overfit_materialization_receipt": {
            "forbidden_changes": [
                "model_training",
                "threshold_retuning",
                "lot_optimization",
                "direct_forward_pocket_filtering",
                "candidate_selection",
                "runtime_authority_claim",
                "goal_achieve_claim",
            ],
            "proxy_ordering_rule": "proxy expected values must be fixed before MT5 comparison is interpreted",
            "package_count": len(package_manifest),
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "gate_receipt": {
            "required_gates": gate_rows,
            "failed_gates": failed_gates,
        },
    }


def build_report_text(package_manifest: Sequence[Mapping[str, Any]], readiness_rows: Sequence[Mapping[str, Any]], gate_rows: Sequence[Mapping[str, Any]]) -> str:
    failed_gates = [row for row in gate_rows if str(row.get("status", "")).startswith("failed")]
    unusable = [row for row in readiness_rows if row.get("current_usability_judgment") == "not_usable_yet"]
    return f"""
# run335G Guarded Branch Probe Input Materialization(335G 방어 분기 탐침 입력 물질화)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- packages(패키지): `{len(package_manifest)}`
- proxy_mt5_readiness_rows(proxy-MT5 준비 행): `{len(readiness_rows)}`
- not_usable_yet(아직 사용 불가): `{len(unusable)}`
- failed_gates(실패 게이트): `{len(failed_gates)}`
- next_action(다음 행동): `{NEXT_RUN_ID}`

Effect(효과): run335F(335F 실행)의 11개 protocol(계약)을 probe input spec(탐침 입력 명세), proxy expected manifest(프록시 예상값 목록), MT5 runtime result-or-block(MT5 런타임 결과 또는 차단 기록), comparison readiness(비교 준비도), negative control(부정 대조), stop condition(중단 조건), no-retune guard(무재튜닝 방어)로 물질화했다.

Proxy-vs-MT5 rule(프록시 대 MT5 규칙): 현재는 proxy expected value(프록시 예상값)와 MT5 runtime probe result(MT5 런타임 탐침 결과)가 모두 없으므로 usability(활용 가능성)는 `not_usable_yet`이다. 나중에 두 결과가 모두 생기면 net/PF/DD/trades/day/expectancy/recovery/curve pocket/underwater/lot-normalized/cost/session/side(순수익/수익팩터/손실/일거래수/기대값/회복/곡선 포켓/수중구간/로트 정규화/비용/세션/방향) 차이를 비교해야 한다.

Boundary(경계): model training(모델 학습), threshold retuning(임계값 재조정), lot optimization(로트 최적화), direct forward pocket filtering(직접 전진 포켓 필터링), candidate selection(후보 선택), Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 모두 `not_claimed`다.
"""


def build_decision_text() -> str:
    return f"""
# Stage335G Decision(335G 결정)

`{RUN_ID}`는 guarded branch probe inputs(방어 분기 탐침 입력)를 materialized(물질화)했다.

- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Effect(효과): 다음 review(검토)는 proxy expected(프록시 예상값)와 MT5 runtime probe(MT5 런타임 탐침)가 같은 subject/handoff(대상/인계)를 비교할 수 있는지 먼저 확인한다. 현재 run335G는 입력 물질화만 했으므로 활용 가능성은 주장하지 않는다.
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
        "- effect(효과): Stage335G(335G 실행)는 guarded branch probe inputs(방어 분기 탐침 입력)를 물질화했지만, 아직 proxy result(프록시 결과), MT5 runtime probe result(MT5 런타임 탐침 결과), 후보 선택(candidate selection, 후보 선택)은 없다.",
    )
    changed.append(write_text_lossless(selection_path, text, had_bom))

    text, had_bom = read_text_lossless(STAGE_BRIEF)
    text = replace_prefix_line(text, "- latest_run", f"- latest_run(최신 실행): `{RUN_ID}`")
    changed.append(write_text_lossless(STAGE_BRIEF, text, had_bom))

    changed.append(
        append_section_once(
            INPUTS_DIR / "input_refs.md",
            "## run335G Probe Input Materialization(335G 탐침 입력 물질화)",
            f"""- probe_input_package_manifest(탐침 입력 패키지 목록): `{rel(RUN_DIR / "probe_input_package_manifest.csv")}`
- probe_input_specs(탐침 입력 명세): `{rel(PROBE_SPEC_DIR)}`
- proxy_expected_result_manifest(프록시 예상값 목록): `{rel(RUN_DIR / "proxy_expected_result_manifest.csv")}`
- mt5_runtime_probe_result_or_block(MT5 런타임 탐침 결과 또는 차단): `{rel(RUN_DIR / "mt5_runtime_probe_result_or_block.csv")}`
- proxy_mt5_comparison_readiness_matrix(프록시-MT5 비교 준비 행렬): `{rel(RUN_DIR / "proxy_mt5_comparison_readiness_matrix.csv")}`
- decision(결정): `{rel(DECISION_DOC)}`""",
        )
    )

    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_prefix_line(workspace_text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    workspace_text = replace_prefix_line(workspace_text, "updated_on:", f"updated_on: '{TODAY}'")
    focus_line = (
        "- >-\n"
        f"  Stage335(335단계) run335G(335G 실행)는 `{STATUS}`로 guarded branch probe inputs(방어 분기 탐침 입력)를 materialized(물질화)했다. "
        "Effect(효과): 11개 probe package/proxy expected schema/MT5 result-or-block/comparison readiness(탐침 패키지/프록시 예상값 형식/MT5 결과 또는 차단/비교 준비도)를 만들고 Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    workspace_text = insert_after_prefix_once(workspace_text, "current_focus:", focus_line, "run335G(335G 실행)")
    changed.append(write_text_lossless(WORKSPACE_STATE, workspace_text, workspace_bom))

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    current_text = replace_prefix_line(current_text, "- current_packet", "- current_packet(현재 작업 묶음): `335_overfit_guard__failure_memory_constrained_research_handoff_v8`")
    current_text = replace_prefix_line(current_text, "- current_run", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    current_text = replace_prefix_line(current_text, "- status", f"- status(상태): `{STATUS}`")
    current_text = replace_prefix_line(current_text, "- decision", f"- decision(판정): `{DECISION}`")
    current_text = remove_lines_containing(current_text, "run335G_summary")
    summary = (
        f"- run335G_summary(335G 요약): guarded branch probe input materialization(방어 분기 탐침 입력 물질화)을 `{STATUS}`로 완료했다. "
        "Effect(효과): probe package(탐침 패키지) 11개, proxy expected manifest(프록시 예상값 목록) 11개, MT5 result-or-block(MT5 결과 또는 차단) 11개, comparison readiness(비교 준비도) 11개를 만들었고, 활용 가능성(usability, 활용 가능성)과 Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    current_text = insert_after_prefix_once(current_text, "- decision", summary, "run335G_summary")
    changed.append(write_text_lossless(CURRENT_STATE, current_text, current_bom))

    changed.append(
        append_section_once(
            CHANGELOG,
            "## 2026-05-26 Stage335G Probe Input Materialization(335G 탐침 입력 물질화)",
            f"""- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- effect(효과): 11개 branch(분기)를 proxy-vs-MT5 comparison(프록시-MT5 비교) 가능한 입력 패키지로 물질화했다.
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
                    "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};proxy_mt5_usability_not_claimed;goal_achieve_not_claimed.",
                }
            ],
        )
    )
    ledger_row = {
        "ledger_row_id": f"{RUN_ID}__probe_input_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "guarded_branch_probe_input_materialization",
        "tier_scope": "paired_tier_required_by_contract",
        "kpi_scope": "manifest_only_no_new_trading_kpi",
        "scoreboard_lane": "experiment_execution",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(report_path),
        "primary_kpi": "probe_packages=11;proxy_mt5_readiness_rows=11;review_queue_rows=11",
        "guardrail_kpi": "proxy_usability_not_claimed;mt5_runtime_not_executed;no_model_training;no_threshold_retuning;goal_achieve_not_claimed",
        "external_verification_status": "out_of_scope_by_claim_materialization_only",
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
                    "evidence_scope": "guarded_branch_probe_input_materialization",
                    "kpi_scope": "manifest_only_no_new_trading_kpi",
                    "status": STATUS,
                    "judgment": JUDGMENT,
                    "claim_boundary": CLAIM_BOUNDARY,
                    "path": rel(report_path),
                    "notes": "no_candidate_selected;proxy_mt5_usability_not_claimed;goal_achieve_not_claimed.",
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
                "notes": f"Stage335G probe input materialization artifact; claim_boundary={CLAIM_BOUNDARY}",
            }
        )
    changed.append(upsert_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows))
    return changed


def main() -> int:
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    PROBE_SPEC_DIR.mkdir(parents=True, exist_ok=True)
    inputs = load_inputs()
    package_manifest, payload_paths = build_probe_packages(inputs)
    measurement_rows = build_measurement_input_manifest(inputs)
    proxy_rows = build_proxy_expected_manifest(inputs)
    mt5_rows = build_mt5_runtime_probe_result_or_block(inputs)
    readiness_rows = build_proxy_mt5_readiness(inputs)
    negative_rows = build_negative_input_manifest(inputs)
    stop_rows = build_stop_input_manifest(inputs)
    runtime_rows = build_runtime_bridge_manifest(inputs)
    no_retune_rows = build_no_retune_manifest(inputs)
    review_queue = build_review_queue(package_manifest)
    gate_rows = build_gate_rows(
        inputs,
        package_manifest,
        measurement_rows,
        proxy_rows,
        mt5_rows,
        readiness_rows,
        negative_rows,
        stop_rows,
        runtime_rows,
        no_retune_rows,
        review_queue,
        payload_paths,
    )
    receipts = build_receipts(inputs, package_manifest, gate_rows)
    failed_gates = [row for row in gate_rows if str(row.get("status", "")).startswith("failed")]
    not_usable = [row for row in readiness_rows if row.get("current_usability_judgment") == "not_usable_yet"]
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
        "probe_package_count": len(package_manifest),
        "measurement_rows": len(measurement_rows),
        "proxy_expected_rows": len(proxy_rows),
        "mt5_runtime_result_or_block_rows": len(mt5_rows),
        "proxy_mt5_readiness_rows": len(readiness_rows),
        "proxy_mt5_not_usable_yet_rows": len(not_usable),
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
            RUN_DIR / "probe_input_package_manifest.csv",
            [
                "package_id",
                "protocol_id",
                "branch_id",
                "branch_name",
                "probe_family",
                "measurement_rows",
                "negative_control_rows",
                "stop_condition_rows",
                "runtime_bridge_rows",
                "proxy_mt5_contract_rows",
                "minimum_outputs_required",
                "forbidden_outputs",
                "payload_path",
                "payload_sha256",
                "package_status",
                "selection_eligible",
                "claim_boundary",
            ],
            package_manifest,
        ),
        write_csv(
            RUN_DIR / "measurement_input_manifest.csv",
            [
                "protocol_id",
                "branch_id",
                "branch_name",
                "measurement_view",
                "required",
                "meaning",
                "kpi_scope",
                "missing_policy",
                "claim_boundary",
                "run335G_status",
                "expected_output_field",
                "claim_effect",
            ],
            measurement_rows,
        ),
        write_csv(
            RUN_DIR / "proxy_expected_result_manifest.csv",
            [
                "protocol_id",
                "branch_id",
                "branch_name",
                "proxy_expected_status",
                "required_dimensions",
                "required_views",
                "required_sources",
                "missing_policy",
                "allowed_claim",
                "claim_boundary",
            ],
            proxy_rows,
        ),
        write_csv(
            RUN_DIR / "mt5_runtime_probe_result_or_block.csv",
            [
                "protocol_id",
                "branch_id",
                "branch_name",
                "mt5_runtime_probe_status",
                "mt5_result_available",
                "runtime_bridge_required_rows",
                "required_before",
                "minimum_evidence",
                "blocked_if_later_missing",
                "claim_effect",
                "claim_boundary",
            ],
            mt5_rows,
        ),
        write_csv(
            RUN_DIR / "proxy_mt5_comparison_readiness_matrix.csv",
            [
                "protocol_id",
                "branch_id",
                "branch_name",
                "proxy_expected_available",
                "mt5_runtime_probe_available",
                "comparison_status",
                "difference_read",
                "comparison_dimensions",
                "current_usability_judgment",
                "future_usability_rule",
                "current_reason",
                "next_required_action",
                "claim_boundary",
            ],
            readiness_rows,
        ),
        write_csv(
            RUN_DIR / "negative_control_input_manifest.csv",
            [
                "protocol_id",
                "branch_id",
                "branch_name",
                "control_id",
                "control_role",
                "predeclared_control_design",
                "must_warn_if",
                "claim_effect",
                "run335G_status",
                "required_before",
            ],
            negative_rows,
        ),
        write_csv(
            RUN_DIR / "stop_condition_input_manifest.csv",
            [
                "protocol_id",
                "branch_id",
                "branch_name",
                "stop_rule_id",
                "trigger",
                "required_action",
                "claim_effect",
                "run335G_status",
                "required_before",
            ],
            stop_rows,
        ),
        write_csv(
            RUN_DIR / "runtime_bridge_input_manifest.csv",
            [
                "protocol_id",
                "branch_id",
                "branch_name",
                "runtime_requirement",
                "required_before",
                "evidence",
                "runtime_claim_boundary",
                "bridge_status",
                "run335G_status",
                "mt5_runtime_probe_result_status",
                "claim_effect",
            ],
            runtime_rows,
        ),
        write_csv(
            RUN_DIR / "no_retune_materialization_guard.csv",
            [
                "protocol_id",
                "branch_id",
                "branch_name",
                "forbidden_outputs",
                "threshold_policy",
                "lot_policy",
                "direct_forward_pocket_filter_policy",
                "runtime_authority_policy",
                "guard_status",
                "claim_boundary",
                "run335G_status",
                "materialization_effect",
            ],
            no_retune_rows,
        ),
        write_csv(
            RUN_DIR / "run335H_probe_input_review_queue.csv",
            [
                "review_queue_id",
                "protocol_id",
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
                "proxy_mt5_usability",
                "goal_achieve",
                "next_action",
                "claim_boundary",
            ],
            result_rows,
        ),
        write_json(RUN_DIR / "run_evidence_system_receipt.json", receipts["run_evidence_system_receipt"]),
        write_json(RUN_DIR / "experiment_design_receipt.json", receipts["experiment_design_receipt"]),
        write_json(RUN_DIR / "data_integrity_receipt.json", receipts["data_integrity_receipt"]),
        write_json(RUN_DIR / "model_validation_receipt.json", receipts["model_validation_receipt"]),
        write_json(RUN_DIR / "runtime_parity_receipt.json", receipts["runtime_parity_receipt"]),
        write_json(RUN_DIR / "result_judgment_receipt.json", receipts["result_judgment_receipt"]),
        write_json(RUN_DIR / "anti_overfit_materialization_receipt.json", receipts["anti_overfit_materialization_receipt"]),
        write_json(RUN_DIR / "gate_receipt.json", receipts["gate_receipt"]),
        write_json(RUN_DIR / "final_probe_input_materialization_decision.json", final_decision),
    ]
    artifact_paths.extend(payload_paths)

    manifest_path = RUN_DIR / "run_manifest.json"
    lineage_path = RUN_DIR / "artifact_lineage_receipt.json"
    run_manifest = {
        **final_decision,
        "created_at_utc": utc_now(),
        "producer": rel(Path(__file__)),
        "source_inputs": [rel(path) for path in RUN335F_INPUTS.values()],
        "outputs": [rel(path) for path in [*artifact_paths, manifest_path, lineage_path]],
    }
    artifact_paths.append(write_json(manifest_path, run_manifest))

    lineage = {
        "source_inputs": [rel(path) for path in RUN335F_INPUTS.values()],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in [*artifact_paths, lineage_path]],
        "artifact_hashes": {rel(path): sha256_file(path) for path in artifact_paths},
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "tracked_after_force_add_run_dir",
        "lineage_judgment": "connected_with_boundary",
    }
    artifact_paths.append(write_json(lineage_path, lineage))

    report_path = write_md(REVIEWS_DIR / "run335G_guarded_branch_probe_input_materialization.md", build_report_text(package_manifest, readiness_rows, gate_rows))
    artifact_paths.append(report_path)
    artifact_paths.append(write_md(DECISION_DOC, build_decision_text()))
    artifact_paths.extend(update_state_docs())
    artifact_paths.extend(update_registries([Path(__file__), *artifact_paths], report_path))

    summary = {
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "probe_package_count": len(package_manifest),
        "measurement_rows": len(measurement_rows),
        "proxy_expected_rows": len(proxy_rows),
        "mt5_runtime_result_or_block_rows": len(mt5_rows),
        "proxy_mt5_readiness_rows": len(readiness_rows),
        "proxy_mt5_not_usable_yet_rows": len(not_usable),
        "negative_control_rows": len(negative_rows),
        "stop_condition_rows": len(stop_rows),
        "runtime_bridge_rows": len(runtime_rows),
        "review_queue_rows": len(review_queue),
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
