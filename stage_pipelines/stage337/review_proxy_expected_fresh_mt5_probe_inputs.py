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
RUN_NUMBER = "run337M"
RUN_ID = "run337M_review_proxy_expected_fresh_mt5_probe_inputs_v1"
PARENT_RUN_ID = "run337L_materialize_proxy_expected_fresh_mt5_probe_inputs_v1"
NEXT_RUN_ID = "run337N_attempt_fresh_mt5_runtime_probe_or_block_v1"
STATUS = "completed_proxy_expected_fresh_mt5_probe_input_review_accepts_runtime_probe_attempt_queue_no_training_no_mt5"
JUDGMENT = "stage337M_inputs_reviewed_open_run337N_runtime_probe_attempt_no_selection"
DECISION = "stage337M_proxy_mt5_inputs_reviewed_accept_runtime_probe_attempt_queue_no_training_no_mt5_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage337M_proxy_mt5_input_review_no_model_training_"
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
RUN337L_DIR = STAGE_DIR / "02_runs" / "run337L"
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
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
DECISION_DOC = DOCS / "decisions" / "2026-05-27_stage337M_review_proxy_mt5_probe_inputs.md"
REPORT_DOC = REVIEWS_DIR / "run337M_review_proxy_expected_fresh_mt5_probe_inputs.md"

SOURCE_LINEAGE_CSV = RUN337L_DIR / "source_lineage_index.csv"
NO_LOOKAHEAD_GUARDS_CSV = RUN337L_DIR / "no_lookahead_pre_execution_guards.csv"
PROXY_EXPECTED_TEMPLATE_CSV = RUN337L_DIR / "proxy_expected_result_template.csv"
PROXY_SOURCE_MANIFEST_JSON = RUN337L_DIR / "proxy_expected_source_identity_manifest.json"
FRESH_MT5_HANDOFF_PACKAGE_CSV = RUN337L_DIR / "fresh_mt5_probe_handoff_package.csv"
MT5_EXECUTION_MANIFEST_JSON = RUN337L_DIR / "mt5_probe_execution_manifest.json"
MT5_HANDOFF_PREFLIGHT_CSV = RUN337L_DIR / "mt5_probe_handoff_precheck.csv"
MT5_TESTER_INPUT_MANIFEST_CSV = RUN337L_DIR / "mt5_tester_input_manifest.csv"
DIFFERENCE_CONTRACT_CSV = RUN337L_DIR / "proxy_mt5_difference_runner_contract.csv"
USABILITY_CONTRACT_CSV = RUN337L_DIR / "usability_decision_runner_contract.csv"
CORE56_HANDOFF_PACKAGE_CSV = RUN337L_DIR / "core56_asof_source_handoff_package.csv"
COST_CURVE_EXTRACTOR_PACKAGE_CSV = RUN337L_DIR / "cost_direction_curve_extractor_package.csv"
REGIME_SOURCE_INVENTORY_CSV = RUN337L_DIR / "regime_asof_source_inventory.csv"
RUNTIME_IDENTITY_PREFLIGHT_CSV = RUN337L_DIR / "runtime_identity_preflight_package.csv"
CLAIM_OUTPUT_REGISTRY_BINDING_CSV = RUN337L_DIR / "claim_boundary_output_registry_binding.csv"
RUN337M_QUEUE_CSV = RUN337L_DIR / "run337M_proxy_mt5_input_review_queue.csv"
RUN337L_GATE_AUDIT_CSV = RUN337L_DIR / "required_gate_coverage_audit.csv"
RUN337L_RESULT_JUDGMENT_CSV = RUN337L_DIR / "result_judgment.csv"
RUN337L_DECISION_JSON = RUN337L_DIR / "final_proxy_mt5_probe_input_materialization_decision.json"
RUN337L_MANIFEST_JSON = RUN337L_DIR / "run_manifest.json"

SOURCE_INPUTS: tuple[Path, ...] = (
    SOURCE_LINEAGE_CSV,
    NO_LOOKAHEAD_GUARDS_CSV,
    PROXY_EXPECTED_TEMPLATE_CSV,
    PROXY_SOURCE_MANIFEST_JSON,
    FRESH_MT5_HANDOFF_PACKAGE_CSV,
    MT5_EXECUTION_MANIFEST_JSON,
    MT5_HANDOFF_PREFLIGHT_CSV,
    MT5_TESTER_INPUT_MANIFEST_CSV,
    DIFFERENCE_CONTRACT_CSV,
    USABILITY_CONTRACT_CSV,
    CORE56_HANDOFF_PACKAGE_CSV,
    COST_CURVE_EXTRACTOR_PACKAGE_CSV,
    REGIME_SOURCE_INVENTORY_CSV,
    RUNTIME_IDENTITY_PREFLIGHT_CSV,
    CLAIM_OUTPUT_REGISTRY_BINDING_CSV,
    RUN337M_QUEUE_CSV,
    RUN337L_GATE_AUDIT_CSV,
    RUN337L_RESULT_JUDGMENT_CSV,
    RUN337L_DECISION_JSON,
    RUN337L_MANIFEST_JSON,
)

INPUT_ARTIFACT_REVIEW_CSV = RUN_DIR / "input_artifact_lineage_review.csv"
RUN337M_QUEUE_REVIEW_CSV = RUN_DIR / "run337M_input_review_queue_review.csv"
PACKAGE_FAMILY_REVIEW_CSV = RUN_DIR / "package_family_input_review.csv"
NO_LOOKAHEAD_REVIEW_CSV = RUN_DIR / "no_lookahead_guard_review.csv"
PROXY_TEMPLATE_REVIEW_CSV = RUN_DIR / "proxy_expected_template_review.csv"
FRESH_MT5_HANDOFF_REVIEW_CSV = RUN_DIR / "fresh_mt5_handoff_review.csv"
MT5_PREFLIGHT_REVIEW_CSV = RUN_DIR / "mt5_probe_preflight_review.csv"
TESTER_MANIFEST_REVIEW_CSV = RUN_DIR / "mt5_tester_manifest_review.csv"
DIFFERENCE_USABILITY_REVIEW_CSV = RUN_DIR / "proxy_mt5_difference_usability_review.csv"
CORE56_HANDOFF_REVIEW_CSV = RUN_DIR / "core56_asof_handoff_review.csv"
COST_CURVE_REVIEW_CSV = RUN_DIR / "cost_direction_curve_extractor_review.csv"
REGIME_INVENTORY_REVIEW_CSV = RUN_DIR / "regime_asof_source_inventory_review.csv"
RUNTIME_IDENTITY_REVIEW_CSV = RUN_DIR / "runtime_identity_preflight_review.csv"
CLAIM_BOUNDARY_REVIEW_CSV = RUN_DIR / "claim_boundary_output_registry_review.csv"
ACCEPTED_INPUTS_CSV = RUN_DIR / "accepted_inputs_for_runtime_probe_attempt.csv"
REPAIR_GAP_QUEUE_CSV = RUN_DIR / "repair_input_gap_queue.csv"
RUN337N_QUEUE_CSV = RUN_DIR / "run337N_fresh_mt5_runtime_probe_attempt_queue.csv"
GATE_AUDIT_CSV = RUN_DIR / "required_gate_coverage_audit.csv"
RESULT_JUDGMENT_CSV = RUN_DIR / "result_judgment.csv"

EXPERIMENT_DESIGN_JSON = RUN_DIR / "experiment_design_receipt.json"
DATA_INTEGRITY_JSON = RUN_DIR / "data_integrity_receipt.json"
RUNTIME_PARITY_JSON = RUN_DIR / "runtime_parity_receipt.json"
ARTIFACT_LINEAGE_JSON = RUN_DIR / "artifact_lineage_receipt.json"
RESULT_JUDGMENT_JSON = RUN_DIR / "result_judgment_receipt.json"
FINAL_DECISION_JSON = RUN_DIR / "final_review_proxy_mt5_probe_inputs_decision.json"
RUN_MANIFEST_JSON = RUN_DIR / "run_manifest.json"

SUBJECTS = ("m48_bal_rf", "m48_plain_rf", "u42_bal_rf", "u42_plain_rf", "core56_refresh_candidate")
DIMENSIONS = ("feature_ready_count", "model_ok_count", "long_count", "short_count", "flat_count")
EXPECTED_COUNTS = {
    "source_lineage": 25,
    "no_lookahead": 5,
    "proxy_template": 25,
    "fresh_handoff": 5,
    "preflight": 5,
    "tester_manifest": 5,
    "difference_contract": 5,
    "usability_contract": 5,
    "core56_handoff": 5,
    "cost_curve": 5,
    "regime_inventory": 6,
    "runtime_identity": 6,
    "claim_boundary": 11,
    "run337m_queue": 9,
}


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


def split_paths(value: str) -> list[Path]:
    paths = []
    for item in str(value or "").split(";"):
        text = item.strip()
        if text:
            paths.append(ROOT / text)
    return paths


def load_inputs() -> dict[str, Any]:
    return {
        "source_lineage": read_csv(SOURCE_LINEAGE_CSV),
        "no_lookahead": read_csv(NO_LOOKAHEAD_GUARDS_CSV),
        "proxy_template": read_csv(PROXY_EXPECTED_TEMPLATE_CSV),
        "proxy_manifest": read_json(PROXY_SOURCE_MANIFEST_JSON),
        "fresh_handoff": read_csv(FRESH_MT5_HANDOFF_PACKAGE_CSV),
        "mt5_execution_manifest": read_json(MT5_EXECUTION_MANIFEST_JSON),
        "mt5_preflight": read_csv(MT5_HANDOFF_PREFLIGHT_CSV),
        "tester_manifest": read_csv(MT5_TESTER_INPUT_MANIFEST_CSV),
        "difference": read_csv(DIFFERENCE_CONTRACT_CSV),
        "usability": read_csv(USABILITY_CONTRACT_CSV),
        "core56": read_csv(CORE56_HANDOFF_PACKAGE_CSV),
        "cost_curve": read_csv(COST_CURVE_EXTRACTOR_PACKAGE_CSV),
        "regime": read_csv(REGIME_SOURCE_INVENTORY_CSV),
        "runtime_identity": read_csv(RUNTIME_IDENTITY_PREFLIGHT_CSV),
        "claim_boundary": read_csv(CLAIM_OUTPUT_REGISTRY_BINDING_CSV),
        "queue": read_csv(RUN337M_QUEUE_CSV),
        "run337l_gate_audit": read_csv(RUN337L_GATE_AUDIT_CSV),
        "run337l_result_judgment": read_csv(RUN337L_RESULT_JUDGMENT_CSV),
        "run337l_decision": read_json(RUN337L_DECISION_JSON),
        "run337l_manifest": read_json(RUN337L_MANIFEST_JSON),
    }


def validate_parent(inputs: Mapping[str, Any]) -> None:
    decision = inputs["run337l_decision"]
    manifest = inputs["run337l_manifest"]
    if decision.get("status") != "completed_proxy_expected_fresh_mt5_probe_inputs_materialized_no_mt5_execution":
        raise ValueError(f"unexpected run337L status: {decision.get('status')}")
    if decision.get("next_action") != RUN_ID:
        raise ValueError(f"run337L next_action does not point to {RUN_ID}: {decision.get('next_action')}")
    if decision.get("mt5_execution") != "not_run" or manifest.get("mt5_execution") != "not_run":
        raise ValueError("run337M review requires run337L to have no MT5 execution")
    if decision.get("model_training") != "not_run":
        raise ValueError("run337M review requires no model training")
    failed_parent_gates = [row for row in inputs["run337l_gate_audit"] if row.get("status") != "pass"]
    if failed_parent_gates:
        raise ValueError(f"run337L has failed gates: {failed_parent_gates}")


def build_input_artifact_review() -> list[dict[str, Any]]:
    rows = []
    for path in SOURCE_INPUTS:
        exists = path_exists(path)
        rows.append(
            {
                "source_path": rel(path),
                "exists": exists,
                "sha256": sha256_file_lf_normalized(path) if exists and io_path(path).is_file() else "",
                "review_status": "pass" if exists else "fail",
                "review_finding": "source artifact exists and is hashable" if exists else "missing source artifact",
                "consumer": RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_queue_review(queue: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows = []
    for row in queue:
        required_paths = split_paths(row.get("required_inputs", ""))
        missing = [rel(path) for path in required_paths if not path_exists(path)]
        rows.append(
            {
                "queue_id": row.get("queue_id", ""),
                "package_family": row.get("package_family", ""),
                "required_input_count": len(required_paths),
                "missing_input_count": len(missing),
                "missing_inputs": ";".join(missing),
                "review_status": "pass" if not missing else "fail",
                "review_finding": "all referenced inputs exist" if not missing else "queue references missing inputs",
                "required_decision": row.get("required_decision", ""),
                "forbidden": row.get("forbidden", FORBIDDEN),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def count_status(name: str, rows: Sequence[Mapping[str, Any]], expected: int, extra_pass: bool = True) -> dict[str, Any]:
    row_count = len(rows)
    passed = row_count == expected and extra_pass
    return {
        "family_id": name,
        "row_count": row_count,
        "expected_row_count": expected,
        "review_status": "pass" if passed else "fail",
        "review_finding": "expected row count and boundary checks pass" if passed else "row count or boundary check mismatch",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_package_family_review(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    source_ok = all(row.get("exists") is True or str(row.get("exists", "")).lower() == "true" for row in inputs["source_lineage"])
    no_lookahead_ok = all(row.get("execution_allowed") == "false" and row.get("model_training_allowed") == "false" for row in inputs["no_lookahead"])
    proxy_ok = all(
        row.get("fresh_mt5_required") == "true"
        and row.get("selection_use") == "blocked"
        and row.get("forward_decision_use") == "blocked"
        for row in inputs["proxy_template"]
    )
    handoff_ok = all(row.get("execution_status") == "not_run_in_run337L" for row in inputs["fresh_handoff"])
    preflight_ok = all(row.get("if_missing_status") == "blocked_before_mt5_execution" for row in inputs["mt5_preflight"])
    tester_ok = all(
        row.get("date_range_start") == "2026-04-14"
        and row.get("execution_status") == "not_run_in_run337L"
        and "no_after_result_tuning" in row.get("spread_slippage_requirement", "")
        for row in inputs["tester_manifest"]
    )
    difference_ok = all(row.get("current_status") == "contract_materialized_pending_fresh_values" for row in inputs["difference"])
    usability_ok = all("KPI authority" in row.get("forbidden_use", "") for row in inputs["usability"])
    core56_ok = all(row.get("execution_allowed") == "false" and row.get("training_allowed") == "false" for row in inputs["core56"])
    cost_curve_ok = all(row.get("training_allowed") == "false" and row.get("mt5_execution_allowed") == "false" for row in inputs["cost_curve"])
    regime_ok = all(row.get("selection_filter_use") == "blocked" and row.get("forward_filter_use") == "blocked" for row in inputs["regime"])
    runtime_ok = all(row.get("mt5_execution_allowed") == "false" for row in inputs["runtime_identity"])
    claim_ok = all(row.get("claim_status") in {"not_claimed", "blocked"} for row in inputs["claim_boundary"])
    return [
        count_status("source_lineage", inputs["source_lineage"], EXPECTED_COUNTS["source_lineage"], source_ok),
        count_status("no_lookahead", inputs["no_lookahead"], EXPECTED_COUNTS["no_lookahead"], no_lookahead_ok),
        count_status("proxy_template", inputs["proxy_template"], EXPECTED_COUNTS["proxy_template"], proxy_ok),
        count_status("fresh_handoff", inputs["fresh_handoff"], EXPECTED_COUNTS["fresh_handoff"], handoff_ok),
        count_status("mt5_preflight", inputs["mt5_preflight"], EXPECTED_COUNTS["preflight"], preflight_ok),
        count_status("tester_manifest", inputs["tester_manifest"], EXPECTED_COUNTS["tester_manifest"], tester_ok),
        count_status("difference_contract", inputs["difference"], EXPECTED_COUNTS["difference_contract"], difference_ok),
        count_status("usability_contract", inputs["usability"], EXPECTED_COUNTS["usability_contract"], usability_ok),
        count_status("core56_handoff", inputs["core56"], EXPECTED_COUNTS["core56_handoff"], core56_ok),
        count_status("cost_curve_extractor", inputs["cost_curve"], EXPECTED_COUNTS["cost_curve"], cost_curve_ok),
        count_status("regime_inventory", inputs["regime"], EXPECTED_COUNTS["regime_inventory"], regime_ok),
        count_status("runtime_identity", inputs["runtime_identity"], EXPECTED_COUNTS["runtime_identity"], runtime_ok),
        count_status("claim_boundary", inputs["claim_boundary"], EXPECTED_COUNTS["claim_boundary"], claim_ok),
        count_status("run337m_queue", inputs["queue"], EXPECTED_COUNTS["run337m_queue"]),
    ]


def build_no_lookahead_review(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    output = []
    for row in rows:
        passed = (
            row.get("execution_allowed") == "false"
            and row.get("model_training_allowed") == "false"
            and row.get("mt5_execution_allowed") == "false"
            and bool(row.get("blocker_criteria", ""))
        )
        output.append(
            {
                "guard_id": row.get("guard_id", ""),
                "package_id": row.get("package_id", ""),
                "review_status": "pass" if passed else "fail",
                "review_finding": "guard blocks execution until explicit runtime attempt preflight" if passed else "guard boundary is incomplete",
                "repair_route": row.get("repair_route", ""),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return output


def build_proxy_template_review(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    output = []
    for subject in SUBJECTS:
        subject_rows = [row for row in rows if row.get("subject") == subject]
        dimensions = {row.get("dimension") for row in subject_rows}
        fresh_required = all(row.get("fresh_mt5_required") == "true" for row in subject_rows)
        no_selection_use = all(row.get("selection_use") == "blocked" and row.get("forward_decision_use") == "blocked" for row in subject_rows)
        status_ok = all(row.get("current_expected_value_status") == "pending_future_proxy_materialization_after_run337M_review" for row in subject_rows)
        passed = len(subject_rows) == len(DIMENSIONS) and dimensions == set(DIMENSIONS) and fresh_required and no_selection_use and status_ok
        output.append(
            {
                "subject": subject,
                "template_rows": len(subject_rows),
                "dimensions": ";".join(sorted(dimensions)),
                "review_status": "pass" if passed else "fail",
                "review_finding": "proxy expected template is review-ready but has no KPI authority" if passed else "proxy expected template is incomplete",
                "current_expected_value_status": "pending_fresh_values_after_review",
                "allowed_use": "runtime probe input comparison after fresh MT5 result exists",
                "forbidden_use": "selection;Forward decision;runtime authority",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return output


def build_fresh_handoff_review(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    output = []
    for row in rows:
        required_outputs = row.get("runtime_outputs", "")
        passed = (
            row.get("subject") in SUBJECTS
            and row.get("execution_status") == "not_run_in_run337L"
            and row.get("runtime_claim_boundary") == "runtime_probe_input_only_no_runtime_authority"
            and "Strategy Tester report" in required_outputs
            and "trade ledger" in required_outputs
        )
        output.append(
            {
                "handoff_id": row.get("handoff_id", ""),
                "subject": row.get("subject", ""),
                "review_status": "pass" if passed else "fail",
                "review_finding": "handoff can feed run337N attempt-or-block preflight" if passed else "handoff is missing runtime evidence requirements",
                "runtime_outputs_required": required_outputs,
                "stress_outputs_required": row.get("stress_outputs", ""),
                "runtime_claim_boundary": "runtime_probe_attempt_input_only_no_runtime_authority",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return output


def build_preflight_review(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    output = []
    for row in rows:
        passed = (
            row.get("execution_status") == "not_run_in_run337L"
            and row.get("if_missing_status") == "blocked_before_mt5_execution"
            and "US100_M5_broker_data" in row.get("required_data_identity", "")
            and "feature_order_hash" in row.get("required_freeze_identity", "")
        )
        output.append(
            {
                "precheck_id": row.get("precheck_id", ""),
                "subject": row.get("subject", ""),
                "review_status": "pass" if passed else "fail",
                "review_finding": "preflight blocks MT5 until runtime/data/freeze identities exist" if passed else "preflight blocker is incomplete",
                "required_runtime_identity": row.get("required_runtime_identity", ""),
                "required_data_identity": row.get("required_data_identity", ""),
                "required_freeze_identity": row.get("required_freeze_identity", ""),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return output


def build_tester_manifest_review(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    output = []
    for row in rows:
        passed = (
            row.get("symbol") == "US100"
            and row.get("timeframe") == "M5"
            and row.get("date_range_start") == "2026-04-14"
            and row.get("execution_status") == "not_run_in_run337L"
            and "no_after_result_tuning" in row.get("spread_slippage_requirement", "")
            and "closed_bar_only" in row.get("feature_freeze_requirement", "")
        )
        output.append(
            {
                "manifest_id": row.get("manifest_id", ""),
                "subject": row.get("subject", ""),
                "symbol": row.get("symbol", ""),
                "timeframe": row.get("timeframe", ""),
                "date_range_start": row.get("date_range_start", ""),
                "date_range_end": row.get("date_range_end", ""),
                "review_status": "pass" if passed else "fail",
                "review_finding": "tester manifest preserves forward-only date and no-retune cost rule" if passed else "tester manifest boundary mismatch",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return output


def build_difference_usability_review(
    difference: Sequence[Mapping[str, str]], usability: Sequence[Mapping[str, str]]
) -> list[dict[str, Any]]:
    usability_by_subject = {row.get("subject", ""): row for row in usability}
    output = []
    for row in difference:
        subject = row.get("subject", "")
        usable = usability_by_subject.get(subject, {})
        passed = (
            row.get("current_status") == "contract_materialized_pending_fresh_values"
            and row.get("selection_use") == "blocked"
            and row.get("forward_decision_use") == "blocked"
            and row.get("runtime_authority_use") == "blocked"
            and "fresh_mt5_report_exists" in usable.get("usable_condition", "")
            and "KPI authority" in usable.get("forbidden_use", "")
        )
        output.append(
            {
                "subject": subject,
                "difference_contract_id": row.get("contract_id", ""),
                "usability_contract_id": usable.get("contract_id", ""),
                "prior_context_judgment": row.get("prior_context_judgment", ""),
                "prior_usability_label": usable.get("prior_usability_label", ""),
                "review_status": "pass" if passed else "fail",
                "review_finding": "difference/usability contract blocks KPI authority until fresh row-level MT5 comparison exists" if passed else "difference/usability claim boundary mismatch",
                "next_condition": "run337N fresh MT5 output plus row-level difference review",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return output


def generic_review(
    rows: Sequence[Mapping[str, str]],
    key: str,
    expected_status: str,
    blocked_fields: Sequence[str],
    finding: str,
) -> list[dict[str, Any]]:
    output = []
    for row in rows:
        passed = row.get("current_status") == expected_status and all(row.get(field) == "false" or row.get(field) == "blocked" for field in blocked_fields)
        output.append(
            {
                "item_id": row.get(key, ""),
                "subject": row.get("subject", row.get("regime_source", row.get("source_protocol_id", ""))),
                "review_status": "pass" if passed else "fail",
                "review_finding": finding if passed else "boundary or status mismatch",
                "current_status": row.get("current_status", ""),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return output


def build_claim_boundary_review(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    output = []
    for row in rows:
        passed = row.get("execution_allowed") == "false" and row.get("training_allowed") == "false" and row.get("mt5_execution_allowed") == "false"
        output.append(
            {
                "blocker_id": row.get("blocker_id", ""),
                "blocked_condition": row.get("blocked_condition", ""),
                "claim_status": row.get("claim_status", ""),
                "review_status": "pass" if passed else "fail",
                "review_finding": "blocked claims remain blocked before runtime evidence" if passed else "claim blocker boundary mismatch",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return output


def build_accepted_inputs(queue_review: Sequence[Mapping[str, Any]], family_review: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    family_failures = [row for row in family_review if row.get("review_status") != "pass"]
    output = []
    for row in queue_review:
        accepted = row.get("review_status") == "pass" and not family_failures
        output.append(
            {
                "accepted_input_id": row.get("queue_id", ""),
                "package_family": row.get("package_family", ""),
                "accepted_for": NEXT_RUN_ID if accepted else "repair_input_gap_queue",
                "acceptance_status": "accepted" if accepted else "repair_required",
                "review_finding": "input family ready for runtime probe attempt queue" if accepted else "input family has repair gap",
                "forbidden": FORBIDDEN,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return output


def build_repair_gap_queue(*reviews: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    gaps = []
    for review_rows in reviews:
        for row in review_rows:
            if row.get("review_status") != "pass":
                gaps.append(
                    {
                        "gap_id": f"repair_{len(gaps) + 1:03d}",
                        "source_item": row.get("queue_id") or row.get("family_id") or row.get("item_id") or row.get("subject") or row.get("blocker_id", ""),
                        "finding": row.get("review_finding", "review failed"),
                        "repair_route": "repair_materialized_input_then_rerun_run337M",
                        "blocked_next_action": NEXT_RUN_ID,
                        "claim_boundary": CLAIM_BOUNDARY,
                    }
                )
    return gaps


def build_run337n_queue(
    handoff: Sequence[Mapping[str, str]],
    preflight: Sequence[Mapping[str, str]],
    tester_manifest: Sequence[Mapping[str, str]],
    difference: Sequence[Mapping[str, str]],
    usability: Sequence[Mapping[str, str]],
) -> list[dict[str, Any]]:
    preflight_by_subject = {row.get("subject", ""): row for row in preflight}
    tester_by_subject = {row.get("subject", ""): row for row in tester_manifest}
    difference_by_subject = {row.get("subject", ""): row for row in difference}
    usability_by_subject = {row.get("subject", ""): row for row in usability}
    output = []
    for row in handoff:
        subject = row.get("subject", "")
        output.append(
            {
                "attempt_id": f"{subject}_fresh_mt5_runtime_probe_attempt",
                "priority": len(output) + 1,
                "subject": subject,
                "required_handoff": rel(FRESH_MT5_HANDOFF_PACKAGE_CSV),
                "required_preflight_id": preflight_by_subject.get(subject, {}).get("precheck_id", ""),
                "tester_manifest_id": tester_by_subject.get(subject, {}).get("manifest_id", ""),
                "difference_contract_id": difference_by_subject.get(subject, {}).get("contract_id", ""),
                "usability_contract_id": usability_by_subject.get(subject, {}).get("contract_id", ""),
                "runtime_outputs_required": row.get("runtime_outputs", ""),
                "comparison_outputs_required": row.get("comparison_outputs", ""),
                "stress_outputs_required": row.get("stress_outputs", ""),
                "execution_scope": "attempt_or_block_only",
                "execution_status": "not_run_in_run337M_preflight_required_for_run337N",
                "blocked_if_missing": row.get("blocked_if_missing", ""),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return output


def build_gate_audit(
    input_artifacts: Sequence[Mapping[str, Any]],
    queue_review: Sequence[Mapping[str, Any]],
    family_review: Sequence[Mapping[str, Any]],
    no_lookahead_review: Sequence[Mapping[str, Any]],
    proxy_review: Sequence[Mapping[str, Any]],
    handoff_review: Sequence[Mapping[str, Any]],
    preflight_review: Sequence[Mapping[str, Any]],
    tester_review: Sequence[Mapping[str, Any]],
    difference_review: Sequence[Mapping[str, Any]],
    core56_review: Sequence[Mapping[str, Any]],
    cost_curve_review: Sequence[Mapping[str, Any]],
    regime_review: Sequence[Mapping[str, Any]],
    runtime_review: Sequence[Mapping[str, Any]],
    claim_review: Sequence[Mapping[str, Any]],
    run337n_queue: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    def pass_all(rows: Sequence[Mapping[str, Any]]) -> bool:
        return all(row.get("review_status") == "pass" for row in rows)

    return [
        {"gate_id": "parent_run337L_completed", "status": "pass", "evidence": rel(RUN337L_DECISION_JSON), "finding": "run337L completed and points to run337M", "claim_boundary": CLAIM_BOUNDARY},
        {"gate_id": "input_artifact_lineage_connected", "status": "pass" if pass_all(input_artifacts) else "fail", "evidence": rel(INPUT_ARTIFACT_REVIEW_CSV), "finding": f"source_inputs={len(input_artifacts)}", "claim_boundary": CLAIM_BOUNDARY},
        {"gate_id": "run337m_queue_inputs_exist", "status": "pass" if pass_all(queue_review) and len(queue_review) == 9 else "fail", "evidence": rel(RUN337M_QUEUE_REVIEW_CSV), "finding": f"queue_rows={len(queue_review)}", "claim_boundary": CLAIM_BOUNDARY},
        {"gate_id": "package_family_counts_and_boundaries", "status": "pass" if pass_all(family_review) and len(family_review) == 14 else "fail", "evidence": rel(PACKAGE_FAMILY_REVIEW_CSV), "finding": f"family_rows={len(family_review)}", "claim_boundary": CLAIM_BOUNDARY},
        {"gate_id": "no_lookahead_guard_review", "status": "pass" if pass_all(no_lookahead_review) else "fail", "evidence": rel(NO_LOOKAHEAD_REVIEW_CSV), "finding": f"guard_rows={len(no_lookahead_review)}", "claim_boundary": CLAIM_BOUNDARY},
        {"gate_id": "proxy_expected_template_review", "status": "pass" if pass_all(proxy_review) and len(proxy_review) == 5 else "fail", "evidence": rel(PROXY_TEMPLATE_REVIEW_CSV), "finding": f"subject_rows={len(proxy_review)}", "claim_boundary": CLAIM_BOUNDARY},
        {"gate_id": "fresh_mt5_handoff_review", "status": "pass" if pass_all(handoff_review) and len(handoff_review) == 5 else "fail", "evidence": rel(FRESH_MT5_HANDOFF_REVIEW_CSV), "finding": f"handoff_rows={len(handoff_review)}", "claim_boundary": CLAIM_BOUNDARY},
        {"gate_id": "runtime_preflight_review", "status": "pass" if pass_all(preflight_review) and len(preflight_review) == 5 else "fail", "evidence": rel(MT5_PREFLIGHT_REVIEW_CSV), "finding": f"preflight_rows={len(preflight_review)}", "claim_boundary": CLAIM_BOUNDARY},
        {"gate_id": "tester_manifest_forward_boundary", "status": "pass" if pass_all(tester_review) and len(tester_review) == 5 else "fail", "evidence": rel(TESTER_MANIFEST_REVIEW_CSV), "finding": f"tester_manifest_rows={len(tester_review)}", "claim_boundary": CLAIM_BOUNDARY},
        {"gate_id": "difference_usability_contract_review", "status": "pass" if pass_all(difference_review) and len(difference_review) == 5 else "fail", "evidence": rel(DIFFERENCE_USABILITY_REVIEW_CSV), "finding": f"difference_usability_rows={len(difference_review)}", "claim_boundary": CLAIM_BOUNDARY},
        {"gate_id": "core56_source_handoff_review", "status": "pass" if pass_all(core56_review) else "fail", "evidence": rel(CORE56_HANDOFF_REVIEW_CSV), "finding": f"core56_rows={len(core56_review)}", "claim_boundary": CLAIM_BOUNDARY},
        {"gate_id": "cost_curve_extractor_review", "status": "pass" if pass_all(cost_curve_review) else "fail", "evidence": rel(COST_CURVE_REVIEW_CSV), "finding": f"cost_curve_rows={len(cost_curve_review)}", "claim_boundary": CLAIM_BOUNDARY},
        {"gate_id": "regime_source_inventory_review", "status": "pass" if pass_all(regime_review) else "fail", "evidence": rel(REGIME_INVENTORY_REVIEW_CSV), "finding": f"regime_rows={len(regime_review)}", "claim_boundary": CLAIM_BOUNDARY},
        {"gate_id": "runtime_identity_preflight_review", "status": "pass" if pass_all(runtime_review) else "fail", "evidence": rel(RUNTIME_IDENTITY_REVIEW_CSV), "finding": f"runtime_rows={len(runtime_review)}", "claim_boundary": CLAIM_BOUNDARY},
        {"gate_id": "claim_boundary_output_registry_review", "status": "pass" if pass_all(claim_review) else "fail", "evidence": rel(CLAIM_BOUNDARY_REVIEW_CSV), "finding": f"claim_rows={len(claim_review)}", "claim_boundary": CLAIM_BOUNDARY},
        {"gate_id": "run337n_attempt_queue_ready", "status": "pass" if len(run337n_queue) == 5 else "fail", "evidence": rel(RUN337N_QUEUE_CSV), "finding": f"run337N_queue_rows={len(run337n_queue)}", "claim_boundary": CLAIM_BOUNDARY},
        {"gate_id": "final_claim_guard", "status": "pass", "evidence": rel(FINAL_DECISION_JSON), "finding": "no model training, no MT5 execution, no Forward decision, no runtime authority, no Goal Achieve", "claim_boundary": CLAIM_BOUNDARY},
    ]


def build_metrics(
    input_artifacts: Sequence[Mapping[str, Any]],
    queue_review: Sequence[Mapping[str, Any]],
    family_review: Sequence[Mapping[str, Any]],
    repair_gaps: Sequence[Mapping[str, Any]],
    run337n_queue: Sequence[Mapping[str, Any]],
    audit: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    return {
        "input_artifact_rows": len(input_artifacts),
        "queue_review_rows": len(queue_review),
        "package_family_review_rows": len(family_review),
        "repair_gap_rows": len(repair_gaps),
        "run337n_queue_rows": len(run337n_queue),
        "gate_rows": len(audit),
        "failed_gate_rows": sum(1 for row in audit if row.get("status") != "pass"),
    }


def write_receipts(metrics: Mapping[str, Any]) -> list[Path]:
    return [
        write_json(
            EXPERIMENT_DESIGN_JSON,
            {
                "run_id": RUN_ID,
                "primary_family": "runtime_backtest_readiness_review",
                "hypothesis": "run337L proxy expected/fresh MT5 input packages are internally consistent enough to open a fresh MT5 runtime probe attempt-or-block queue without training or retuning.",
                "controls": ["no model training", "no threshold retune", "no lot optimization", "no MT5 execution in run337M", "Forward decision blocked"],
                "success_condition": "all materialized input reviews pass and run337N attempt queue has five subject rows",
                "failure_condition": "missing input, incomplete claim boundary, or row-count mismatch routes to repair_input_gap_queue",
                "metrics": metrics,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            DATA_INTEGRITY_JSON,
            {
                "data_source": [rel(path) for path in SOURCE_INPUTS],
                "time_axis": "US100 M5 forward window starts at 2026-04-14; tester end remains latest_available_at_future_execution_preflight; closed-bar-only rule retained.",
                "sample_scope": "five Stage337 probe subjects, 25 proxy template rows, 5 MT5 handoff rows, 5 tester manifest rows.",
                "missing_or_duplicate_check": "run337M checks artifact existence and requires run337N preflight to perform broker data gap/duplicate/timezone checks before execution.",
                "feature_label_boundary": "proxy template and tester manifest require closed-bar-only and no nearest/future join; no label or KPI is created in run337M.",
                "split_boundary": "post-2026-04-14 forward probe boundary only; no training/validation split mutation.",
                "leakage_risk": "highest risk is treating prior proxy aggregate context as fresh KPI; run337M keeps it signal-sanity-only.",
                "data_hash_or_identity": f"input_artifact_rows={metrics['input_artifact_rows']}",
                "integrity_judgment": "usable_with_boundary",
            },
        ),
        write_json(
            RUNTIME_PARITY_JSON,
            {
                "research_path": rel(Path(__file__)),
                "runtime_path": rel(FRESH_MT5_HANDOFF_PACKAGE_CSV),
                "shared_contract": "feature order, model/surface identity, threshold/risk/lot/ATR freeze, timestamp basis, Strategy Tester report, terminal log, trade ledger, telemetry, row-level proxy-vs-MT5 difference.",
                "known_differences": "run337M performs review only; no MT5 tester output exists yet.",
                "parity_check": "materialized input review and run337N attempt queue creation; external runtime output remains next condition.",
                "parity_identity": f"run337L_manifest={sha256_file_lf_normalized(RUN337L_MANIFEST_JSON)}",
                "runtime_claim_boundary": "runtime_probe_attempt_queue_no_runtime_authority",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            ARTIFACT_LINEAGE_JSON,
            {
                "source_inputs": [rel(path) for path in SOURCE_INPUTS],
                "producer": rel(Path(__file__)),
                "consumer": NEXT_RUN_ID,
                "artifact_paths": [rel(RUN337N_QUEUE_CSV), rel(REPORT_DOC), rel(FINAL_DECISION_JSON)],
                "artifact_hashes": "written to artifact_registry after generation",
                "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
                "availability": "tracked",
                "lineage_judgment": "connected_with_boundary",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RESULT_JUDGMENT_JSON,
            {
                "result_subject": "run337M proxy expected fresh MT5 probe input review",
                "evidence_available": [rel(RUN337N_QUEUE_CSV), rel(GATE_AUDIT_CSV), rel(PACKAGE_FAMILY_REVIEW_CSV)],
                "evidence_missing": "fresh MT5 Strategy Tester report, terminal log, trade ledger, row-level proxy-vs-MT5 comparison, cost stress, D/B attribution, curve pocket.",
                "judgment_label": "exploratory",
                "claim_boundary": CLAIM_BOUNDARY,
                "next_condition": NEXT_RUN_ID,
                "user_explanation_hook": "입력 검토는 통과했지만 아직 MT5 실행 결과가 없어 전진 통과나 런타임 권위는 없다.",
            },
        ),
    ]


def write_reports(metrics: Mapping[str, Any]) -> list[Path]:
    report = f"""
# run337M Proxy Expected Fresh MT5 Probe Input Review(337M 프록시 예상값/신규 MT5 탐침 입력 검토)

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

## Review Metrics(검토 지표)

- input_artifact_rows(입력 산출물 행): `{metrics['input_artifact_rows']}`
- queue_review_rows(대기열 검토 행): `{metrics['queue_review_rows']}`
- package_family_review_rows(패키지군 검토 행): `{metrics['package_family_review_rows']}`
- repair_gap_rows(수리 공백 행): `{metrics['repair_gap_rows']}`
- run337N_queue_rows(337N 대기열 행): `{metrics['run337n_queue_rows']}`
- gate_rows(게이트 행): `{metrics['gate_rows']}`, failed(실패): `{metrics['failed_gate_rows']}`

Action(행동): run337L(337L 실행)의 proxy expected template(프록시 예상값 템플릿), fresh MT5 handoff package(신규 메타트레이더5 인계 패키지), difference/usability contract(차이/활용성 계약), no-lookahead guard(미래참조 방어)를 검토했다.

Effect(효과): run337N(337N 실행)의 fresh MT5 runtime probe attempt-or-block(신규 메타트레이더5 런타임 탐침 시도 또는 차단) 대기열을 열었다. 이번 실행은 MT5 execution(MT5 실행), model training(모델 학습), candidate selection(후보 선택), Forward decision(전진 판정)을 열지 않았다.
"""
    decision = f"""
# Stage337M Decision(337M 결정)

- decision(결정): `{DECISION}`
- evidence(근거): `{rel(FINAL_DECISION_JSON)}`, `{rel(GATE_AUDIT_CSV)}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- boundary(경계): `{CLAIM_BOUNDARY}`

Effect(효과): 입력 검토는 통과했지만, fresh MT5 report(신규 MT5 보고서)와 trade ledger(거래 장부)가 아직 없으므로 Forward Passed(전진 통과), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.
"""
    return [write_md(REPORT_DOC, report), write_md(DECISION_DOC, decision)]


def update_status_docs(metrics: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

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
- effect(효과): run337M(337M 실행)는 proxy expected/fresh MT5 input review(프록시 예상값/신규 메타트레이더5 입력 검토)를 완료하고 run337N(337N 실행) runtime probe attempt-or-block(런타임 탐침 시도 또는 차단) 대기열로 넘겼다. 아직 선택 후보는 없다.
"""
    artifacts.append(write_md(SELECTED_DIR / "selection_status.md", selection))

    brief_text, brief_bom = read_text_lossless(SPEC_DIR / "stage_brief.md")
    brief_text = replace_prefix_line(brief_text, "- latest_run(최신 실행):", f"- latest_run(최신 실행): `{RUN_ID}`")
    brief_text = insert_after_marker_once(
        brief_text,
        "- run337L_summary(337L 요약):",
        f"- run337M_summary(337M 요약): `{STATUS}`. Effect(효과): run337L 입력 묶음을 검토하고 run337N runtime probe attempt-or-block(런타임 탐침 시도 또는 차단) 대기열 `{metrics['run337n_queue_rows']}`행을 열었다.",
        "run337M_summary(337M 요약)",
    )
    artifacts.append(write_text_lossless(SPEC_DIR / "stage_brief.md", brief_text, brief_bom))

    input_section = f"""
- input_artifact_review(입력 산출물 검토): `{rel(INPUT_ARTIFACT_REVIEW_CSV)}`
- package_family_review(패키지군 검토): `{rel(PACKAGE_FAMILY_REVIEW_CSV)}`
- accepted_inputs(승인 입력): `{rel(ACCEPTED_INPUTS_CSV)}`
- repair_gap_queue(수리 공백 대기열): `{rel(REPAIR_GAP_QUEUE_CSV)}`
- run337N_queue(337N 대기열): `{rel(RUN337N_QUEUE_CSV)}`

Effect(효과): run337N(337N 실행)에서 실제 fresh MT5 runtime probe(신규 메타트레이더5 런타임 탐침)를 시도하거나, 사전점검 실패를 정확히 차단할 수 있다.
"""
    artifacts.append(append_section_once(INPUTS_DIR / "input_refs.md", "## run337M Outputs(337M 산출물)", input_section))

    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_prefix_line(workspace_text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    focus = (
        "- >-\n"
        f"  Stage337 run337M focus complete: Stage337(337단계) run337M(337M 실행)는 `{STATUS}`로 proxy expected/fresh MT5 input review(프록시 예상값/신규 메타트레이더5 입력 검토)를 완료했다. "
        "Effect(효과): run337N(337N 실행) fresh MT5 runtime probe attempt-or-block(신규 메타트레이더5 런타임 탐침 시도 또는 차단) 대기열을 열었지만 model training(모델 학습), MT5 execution(MT5 실행), candidate selection(후보 선택)은 아직 닫아둔다.\n"
    )
    workspace_text = insert_focus_once(workspace_text, focus, "Stage337 run337M focus complete")
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
        f"- run337M_summary(337M 요약): `{STATUS}`. "
        "Effect(효과): run337L 입력 패키지를 검토해 run337N runtime probe attempt-or-block(런타임 탐침 시도 또는 차단)으로 넘기며, MT5 실행/학습/후보 선택은 계속 닫아둔다."
    )
    current_text = insert_after_marker_once(current_text, "- run337L_summary(337L 요약):", summary, "run337M_summary(337M 요약)")
    artifacts.append(write_text_lossless(CURRENT_STATE, current_text, current_bom))

    artifacts.append(
        append_section_once(
            CHANGELOG,
            "## Stage337M Proxy MT5 Input Review(337M 프록시 MT5 입력 검토)",
            f"""
- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- action(행동): run337L(337L 실행)의 입력 산출물, queue(대기열), claim boundary(주장 경계), no-lookahead guard(미래참조 방어)를 검토했다.
- effect(효과): run337N(337N 실행) fresh MT5 runtime probe attempt-or-block(신규 메타트레이더5 런타임 탐침 시도 또는 차단) 대기열 `{metrics['run337n_queue_rows']}`행을 열었고 MT5 execution(MT5 실행), Forward decision(전진 판정), runtime authority(런타임 권위)는 주장하지 않는다.
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
                "lane": "proxy_mt5_input_review",
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
                "ledger_row_id": f"{RUN_ID}__proxy_mt5_input_review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "proxy_mt5_input_review",
                "tier_scope": "stage337_package_boundary_macro48_u42_core56",
                "kpi_scope": "input_review_only_no_new_candidate_kpi",
                "scoreboard_lane": "runtime_parity_readiness",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_DOC),
                "primary_kpi": "input_artifact_rows=20;package_family_review_rows=14;run337n_queue_rows=5",
                "guardrail_kpi": "training_not_allowed;mt5_not_executed;runtime_authority_not_claimed;goal_achieve_not_claimed",
                "external_verification_status": "out_of_scope_by_claim_input_review_only",
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
                "ledger_row_id": f"{RUN_ID}__proxy_mt5_input_review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "work_family": "runtime_parity_input_review",
                "evidence_scope": "run337L_materialized_inputs_to_run337N_runtime_probe_queue",
                "kpi_scope": "input_review_only_no_new_candidate_kpi",
                "status": STATUS,
                "judgment": JUDGMENT,
                "claim_boundary": CLAIM_BOUNDARY,
                "path": rel(REPORT_DOC),
                "notes": f"next_action={NEXT_RUN_ID};run337N_queue_opened;mt5_not_executed;goal_achieve_not_claimed.",
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
            "notes": "run337M_proxy_mt5_input_review_no_execution_no_selection",
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
    validate_parent(inputs)

    input_artifacts = build_input_artifact_review()
    queue_review = build_queue_review(inputs["queue"])
    family_review = build_package_family_review(inputs)
    no_lookahead_review = build_no_lookahead_review(inputs["no_lookahead"])
    proxy_review = build_proxy_template_review(inputs["proxy_template"])
    handoff_review = build_fresh_handoff_review(inputs["fresh_handoff"])
    preflight_review = build_preflight_review(inputs["mt5_preflight"])
    tester_review = build_tester_manifest_review(inputs["tester_manifest"])
    difference_review = build_difference_usability_review(inputs["difference"], inputs["usability"])
    core56_review = generic_review(
        inputs["core56"],
        "package_id",
        "source_handoff_package_materialized_pending_run337M_review",
        ("execution_allowed", "training_allowed", "mt5_execution_allowed"),
        "core56 handoff is materialized but remains blocked from KPI authority until refresh and runtime probe",
    )
    cost_curve_review = generic_review(
        inputs["cost_curve"],
        "package_id",
        "extractor_package_materialized_pending_run337M_review",
        ("execution_allowed", "training_allowed", "mt5_execution_allowed"),
        "cost/direction/curve extractor package is materialized and blocked from tuning",
    )
    regime_review = generic_review(
        inputs["regime"],
        "package_id",
        "source_inventory_materialized_pending_run337M_review",
        ("selection_filter_use", "forward_filter_use"),
        "regime source inventory is materialized and blocked from selection filtering",
    )
    runtime_review = generic_review(
        inputs["runtime_identity"],
        "preflight_id",
        "materialized_pending_run337M_review",
        ("execution_allowed", "mt5_execution_allowed"),
        "runtime identity preflight is materialized and does not grant runtime authority",
    )
    claim_review = build_claim_boundary_review(inputs["claim_boundary"])
    accepted_inputs = build_accepted_inputs(queue_review, family_review)
    repair_gaps = build_repair_gap_queue(
        input_artifacts,
        queue_review,
        family_review,
        no_lookahead_review,
        proxy_review,
        handoff_review,
        preflight_review,
        tester_review,
        difference_review,
        core56_review,
        cost_curve_review,
        regime_review,
        runtime_review,
        claim_review,
    )
    run337n_queue = build_run337n_queue(
        inputs["fresh_handoff"],
        inputs["mt5_preflight"],
        inputs["tester_manifest"],
        inputs["difference"],
        inputs["usability"],
    )
    audit = build_gate_audit(
        input_artifacts,
        queue_review,
        family_review,
        no_lookahead_review,
        proxy_review,
        handoff_review,
        preflight_review,
        tester_review,
        difference_review,
        core56_review,
        cost_curve_review,
        regime_review,
        runtime_review,
        claim_review,
        run337n_queue,
    )
    metrics = build_metrics(input_artifacts, queue_review, family_review, repair_gaps, run337n_queue, audit)
    failed_gates = [row for row in audit if row.get("status") != "pass"]

    run_artifacts = [
        write_csv(INPUT_ARTIFACT_REVIEW_CSV, ("source_path", "exists", "sha256", "review_status", "review_finding", "consumer", "claim_boundary"), input_artifacts),
        write_csv(RUN337M_QUEUE_REVIEW_CSV, ("queue_id", "package_family", "required_input_count", "missing_input_count", "missing_inputs", "review_status", "review_finding", "required_decision", "forbidden", "claim_boundary"), queue_review),
        write_csv(PACKAGE_FAMILY_REVIEW_CSV, ("family_id", "row_count", "expected_row_count", "review_status", "review_finding", "claim_boundary"), family_review),
        write_csv(NO_LOOKAHEAD_REVIEW_CSV, ("guard_id", "package_id", "review_status", "review_finding", "repair_route", "claim_boundary"), no_lookahead_review),
        write_csv(PROXY_TEMPLATE_REVIEW_CSV, ("subject", "template_rows", "dimensions", "review_status", "review_finding", "current_expected_value_status", "allowed_use", "forbidden_use", "claim_boundary"), proxy_review),
        write_csv(FRESH_MT5_HANDOFF_REVIEW_CSV, ("handoff_id", "subject", "review_status", "review_finding", "runtime_outputs_required", "stress_outputs_required", "runtime_claim_boundary", "claim_boundary"), handoff_review),
        write_csv(MT5_PREFLIGHT_REVIEW_CSV, ("precheck_id", "subject", "review_status", "review_finding", "required_runtime_identity", "required_data_identity", "required_freeze_identity", "claim_boundary"), preflight_review),
        write_csv(TESTER_MANIFEST_REVIEW_CSV, ("manifest_id", "subject", "symbol", "timeframe", "date_range_start", "date_range_end", "review_status", "review_finding", "claim_boundary"), tester_review),
        write_csv(DIFFERENCE_USABILITY_REVIEW_CSV, ("subject", "difference_contract_id", "usability_contract_id", "prior_context_judgment", "prior_usability_label", "review_status", "review_finding", "next_condition", "claim_boundary"), difference_review),
        write_csv(CORE56_HANDOFF_REVIEW_CSV, ("item_id", "subject", "review_status", "review_finding", "current_status", "claim_boundary"), core56_review),
        write_csv(COST_CURVE_REVIEW_CSV, ("item_id", "subject", "review_status", "review_finding", "current_status", "claim_boundary"), cost_curve_review),
        write_csv(REGIME_INVENTORY_REVIEW_CSV, ("item_id", "subject", "review_status", "review_finding", "current_status", "claim_boundary"), regime_review),
        write_csv(RUNTIME_IDENTITY_REVIEW_CSV, ("item_id", "subject", "review_status", "review_finding", "current_status", "claim_boundary"), runtime_review),
        write_csv(CLAIM_BOUNDARY_REVIEW_CSV, ("blocker_id", "blocked_condition", "claim_status", "review_status", "review_finding", "claim_boundary"), claim_review),
        write_csv(ACCEPTED_INPUTS_CSV, ("accepted_input_id", "package_family", "accepted_for", "acceptance_status", "review_finding", "forbidden", "claim_boundary"), accepted_inputs),
        write_csv(REPAIR_GAP_QUEUE_CSV, ("gap_id", "source_item", "finding", "repair_route", "blocked_next_action", "claim_boundary"), repair_gaps),
        write_csv(RUN337N_QUEUE_CSV, ("attempt_id", "priority", "subject", "required_handoff", "required_preflight_id", "tester_manifest_id", "difference_contract_id", "usability_contract_id", "runtime_outputs_required", "comparison_outputs_required", "stress_outputs_required", "execution_scope", "execution_status", "blocked_if_missing", "claim_boundary"), run337n_queue),
        write_csv(GATE_AUDIT_CSV, ("gate_id", "status", "evidence", "finding", "claim_boundary"), audit),
        write_csv(
            RESULT_JUDGMENT_CSV,
            ("result_subject", "evidence_available", "evidence_missing", "judgment_label", "claim_boundary", "next_condition"),
            [
                {
                    "result_subject": "run337M proxy expected fresh MT5 input review",
                    "evidence_available": f"{rel(INPUT_ARTIFACT_REVIEW_CSV)};{rel(PACKAGE_FAMILY_REVIEW_CSV)};{rel(RUN337N_QUEUE_CSV)}",
                    "evidence_missing": "fresh MT5 runtime result;Strategy Tester report;terminal log;trade ledger;row-level comparison;cost stress;D/B attribution;curve pocket",
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
        "status": STATUS if not failed_gates else "blocked_stage337M_input_review_gate_failure",
        "judgment": JUDGMENT if not failed_gates else "stage337M_input_review_requires_repair",
        "decision": DECISION if not failed_gates else "stage337M_input_review_blocked_gate_failure",
        "metrics": metrics,
        "failed_gates": failed_gates,
        "next_action": NEXT_RUN_ID if not failed_gates else "repair_run337M_inputs_before_runtime_probe_attempt",
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
                "status": "blocked_stage337M_input_review_gate_failure",
                "decision": "stage337M_input_review_blocked_gate_failure",
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
        "external_verification_status": "out_of_scope_by_claim_input_review_only_no_mt5_execution",
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
                "input_artifact_rows": metrics["input_artifact_rows"],
                "package_family_review_rows": metrics["package_family_review_rows"],
                "repair_gap_rows": metrics["repair_gap_rows"],
                "run337N_queue_rows": metrics["run337n_queue_rows"],
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
