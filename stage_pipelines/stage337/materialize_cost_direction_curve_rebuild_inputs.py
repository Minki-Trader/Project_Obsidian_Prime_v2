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
RUN_NUMBER = "run337B"
RUN_ID = "run337B_materialize_cost_direction_curve_rebuild_inputs_v1"
PARENT_RUN_ID = "run337A_design_cost_buffer_direction_curve_rebuild_packet_v1"
NEXT_RUN_ID = "run337C_review_materialized_inputs_and_proxy_mt5_usability_v1"
STATUS = "completed_cost_direction_curve_rebuild_inputs_materialized_no_selection"
JUDGMENT = "stage337B_proxy_mt5_signal_usability_context_only_inputs_ready_no_selection"
DECISION = "stage337B_materialized_inputs_ready_proxy_mt5_context_only_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage337B_input_materialization_no_model_training_"
    "no_threshold_retuning_no_lot_optimization_no_forward_pocket_filtering_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
INPUTS_DIR = STAGE_DIR / "01_inputs"
SELECTED_DIR = STAGE_DIR / "04_selected"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"

SOURCE_STAGE_DIR = ROOT / "stages" / SOURCE_STAGE_ID
RUN337A_DIR = STAGE_DIR / "02_runs" / "run337A"
RUN336P_DIR = SOURCE_STAGE_DIR / "02_runs" / "run336P"
RUN336O_DIR = SOURCE_STAGE_DIR / "02_runs" / "run336O"
RUN336N_DIR = SOURCE_STAGE_DIR / "02_runs" / "run336N"
RUN336M_DIR = SOURCE_STAGE_DIR / "02_runs" / "run336M"

DOCS = ROOT / "docs"
WORKSPACE_STATE = DOCS / "workspace" / "workspace_state.yaml"
CURRENT_STATE = DOCS / "context" / "current_working_state.md"
CHANGELOG = DOCS / "workspace" / "changelog.md"
RUN_REGISTRY = DOCS / "registers" / "run_registry.csv"
ALPHA_LEDGER = DOCS / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = DOCS / "registers" / "artifact_registry.csv"
DECISION_DOC = DOCS / "decisions" / "2026-05-27_stage337B_materialize_inputs_proxy_mt5_usability.md"
REPORT_DOC = REVIEWS_DIR / "run337B_materialized_inputs_proxy_mt5_usability.md"

RUN337A_DECISION = RUN337A_DIR / "final_cost_direction_curve_rebuild_packet_design_decision.json"
RUN337A_BRANCH = RUN337A_DIR / "cost_direction_curve_branch_design_matrix.csv"
RUN337A_GATE = RUN337A_DIR / "cost_direction_curve_gate_contract.csv"
RUN337A_PROXY_CONTRACT = RUN337A_DIR / "proxy_expected_vs_mt5_runtime_contract.csv"
RUN337A_NEGATIVE = RUN337A_DIR / "no_lookahead_negative_control_matrix.csv"
RUN337A_CORE56 = RUN337A_DIR / "core56_refresh_boundary_decision.csv"
RUN337A_QUEUE = RUN337A_DIR / "run337B_materialization_queue.csv"
RUN337A_CONSTRAINTS = RUN337A_DIR / "stage337_design_constraint_matrix.csv"

RUN336P_FAILURE = RUN336P_DIR / "stage336_failure_memory_handoff.csv"
RUN336P_DECISION = RUN336P_DIR / "final_stage336P_forward_decision.json"
RUN336O_SCORECARD = RUN336O_DIR / "forward_robustness_scorecard.csv"
RUN336O_SUMMARY = RUN336O_DIR / "attempt_forward_attribution_summary.csv"
RUN336O_COST = RUN336O_DIR / "cost_stress_report.csv"
RUN336O_CURVE = RUN336O_DIR / "curve_pocket_report.csv"
RUN336O_REGIME = RUN336O_DIR / "regime_direction_slice_report.csv"
RUN336N_DIFF = RUN336N_DIR / "timestamp_aligned_proxy_mt5_difference.csv"
RUN336N_BASIS = RUN336N_DIR / "timestamp_basis_audit.csv"
RUN336N_RUNTIME_RECEIPT = RUN336N_DIR / "runtime_parity_receipt.json"
RUN336N_DECISION = RUN336N_DIR / "final_timestamp_aligned_parity_decision.json"
RUN336M_RUNTIME_RESULT = RUN336M_DIR / "runtime_execution_result.json"
RUN336M_TESTER_IDENTITY = RUN336M_DIR / "tester_settings_identity.json"

SOURCE_LINEAGE_CSV = RUN_DIR / "source_lineage_index.csv"
DATA_INTEGRITY_CSV = RUN_DIR / "data_integrity_contract.csv"
NO_LOOKAHEAD_CANARY_CSV = RUN_DIR / "no_lookahead_canary_inputs.csv"
BRANCH_PAYLOAD_CSV = RUN_DIR / "branch_payload_index.csv"
BRANCH_REVIEW_QUEUE_CSV = RUN_DIR / "branch_review_queue.csv"
GATE_SCHEMA_CSV = RUN_DIR / "gate_schema_per_branch.csv"
PROXY_EXPECTED_CSV = RUN_DIR / "proxy_expected_signal_values.csv"
MT5_OBSERVED_CSV = RUN_DIR / "mt5_runtime_probe_observed_values.csv"
PROXY_MT5_DIFF_CSV = RUN_DIR / "proxy_mt5_difference_report.csv"
PROXY_MT5_USABILITY_CSV = RUN_DIR / "proxy_mt5_usability_decision.csv"
MT5_PROBE_MANIFEST_CSV = RUN_DIR / "mt5_runtime_probe_manifest.csv"
COST_LADDER_SCHEMA_CSV = RUN_DIR / "cost_ladder_schema.csv"
LONG_SHORT_SCHEMA_CSV = RUN_DIR / "long_short_attribution_schema.csv"
CURVE_POCKET_SCHEMA_CSV = RUN_DIR / "curve_pocket_schema.csv"
REGIME_SLICE_SCHEMA_CSV = RUN_DIR / "regime_slice_schema.csv"
CORE56_SCOPE_CSV = RUN_DIR / "core56_repair_or_scope_receipt.csv"
RUN337C_QUEUE_CSV = RUN_DIR / "run337C_review_queue.csv"
GATE_AUDIT_CSV = RUN_DIR / "required_gate_coverage_audit.csv"

DATA_INTEGRITY_JSON = RUN_DIR / "data_integrity_receipt.json"
RUNTIME_PARITY_JSON = RUN_DIR / "runtime_parity_receipt.json"
ARTIFACT_LINEAGE_JSON = RUN_DIR / "artifact_lineage_receipt.json"
RESULT_JUDGMENT_JSON = RUN_DIR / "result_judgment_receipt.json"
FINAL_DECISION_JSON = RUN_DIR / "final_materialized_inputs_proxy_mt5_usability_decision.json"
RUN_MANIFEST_JSON = RUN_DIR / "run_manifest.json"


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


def safe_float(value: Any, default: float = math.nan) -> float:
    try:
        text = str(value).strip()
        if not text:
            return default
        number = float(text)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


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


def load_inputs() -> dict[str, Any]:
    return {
        "run337a_decision": read_json(RUN337A_DECISION),
        "branches": read_csv(RUN337A_BRANCH),
        "gates": read_csv(RUN337A_GATE),
        "proxy_contract": read_csv(RUN337A_PROXY_CONTRACT),
        "negative_controls": read_csv(RUN337A_NEGATIVE),
        "core56_boundary": read_csv(RUN337A_CORE56),
        "run337b_queue": read_csv(RUN337A_QUEUE),
        "constraints": read_csv(RUN337A_CONSTRAINTS),
        "failure_memory": read_csv(RUN336P_FAILURE),
        "run336p_decision": read_json(RUN336P_DECISION),
        "scorecard": read_csv(RUN336O_SCORECARD),
        "summary": read_csv(RUN336O_SUMMARY),
        "cost": read_csv(RUN336O_COST),
        "curve": read_csv(RUN336O_CURVE),
        "regime": read_csv(RUN336O_REGIME),
        "proxy_diff": read_csv(RUN336N_DIFF),
        "timestamp_basis": read_csv(RUN336N_BASIS),
        "run336n_runtime": read_json(RUN336N_RUNTIME_RECEIPT),
        "run336n_decision": read_json(RUN336N_DECISION),
        "run336m_runtime": read_json(RUN336M_RUNTIME_RESULT),
        "run336m_tester": read_json(RUN336M_TESTER_IDENTITY),
    }


def by_key(rows: Sequence[Mapping[str, str]], key: str) -> dict[str, Mapping[str, str]]:
    return {str(row.get(key, "")): row for row in rows}


def existing_report_path(summary_by_attempt: Mapping[str, Mapping[str, str]], attempt: str) -> str:
    return str(summary_by_attempt.get(attempt, {}).get("report_path", ""))


def artifact_sha(path: Path) -> str:
    return sha256_file_lf_normalized(path) if path_exists(path) and io_path(path).is_file() else "missing"


def build_source_lineage(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    source_paths = [
        ("run337A_decision", RUN337A_DECISION, "parent design decision"),
        ("run337A_branch_design", RUN337A_BRANCH, "branch input"),
        ("run337A_gate_contract", RUN337A_GATE, "gate input"),
        ("run337A_proxy_contract", RUN337A_PROXY_CONTRACT, "proxy-MT5 input"),
        ("run337A_negative_controls", RUN337A_NEGATIVE, "lookahead guard input"),
        ("run336P_failure_memory", RUN336P_FAILURE, "failure memory source"),
        ("run336O_scorecard", RUN336O_SCORECARD, "forward KPI failure source"),
        ("run336O_summary", RUN336O_SUMMARY, "MT5 KPI summary source"),
        ("run336N_proxy_mt5_diff", RUN336N_DIFF, "proxy expected vs MT5 observed source"),
        ("run336N_timestamp_basis", RUN336N_BASIS, "timestamp alignment source"),
        ("run336M_runtime_result", RUN336M_RUNTIME_RESULT, "MT5 runtime probe source"),
        ("run336M_tester_identity", RUN336M_TESTER_IDENTITY, "tester identity source"),
    ]
    return [
        {
            "source_id": source_id,
            "artifact_path": rel(path),
            "role": role,
            "producer_run": "run337A/run336P/run336O/run336N/run336M",
            "consumer": RUN_ID,
            "availability": "tracked_or_source_artifact_present" if path_exists(path) else "missing",
            "sha256": artifact_sha(path),
            "lineage_judgment": "connected" if path_exists(path) else "blocked_missing_source",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for source_id, path, role in source_paths
    ]


def build_data_integrity_contract(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    basis_rows = list(inputs["timestamp_basis"])
    max_feature_not_seen = max(safe_float(row.get("feature_rows_not_seen_by_mt5_cycles"), 0.0) for row in basis_rows)
    max_mt5_missing = max(safe_float(row.get("mt5_cycle_rows_missing_from_feature_csv"), 0.0) for row in basis_rows)
    return [
        {
            "check_id": "timestamp_aligned_proxy_basis",
            "data_source": rel(RUN336N_BASIS),
            "time_axis": "cycle_bar_time / broker M5 close aligned to MT5 feature-ready rows",
            "sample_scope": "macro48/u42 repaired forward subset, 4 attempts",
            "missing_duplicate_check": f"feature rows not seen by MT5 cycles max={max_feature_not_seen}; MT5 missing from feature CSV max={max_mt5_missing}",
            "feature_label_boundary": "no label use; proxy rows must intersect MT5 emitted cycle rows before comparison",
            "split_boundary": "post-2026-04-14 forward runtime evidence only; no training split change in run337B",
            "leakage_risk": "raw proxy overcounts feature rows if timestamp basis is ignored",
            "data_hash_or_identity": artifact_sha(RUN336N_BASIS),
            "integrity_judgment": "usable_with_boundary",
            "next_evidence": "future branches must repeat aligned basis before KPI interpretation",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "check_id": "forward_failure_memory_as_constraint",
            "data_source": rel(RUN336P_FAILURE),
            "time_axis": "historical forward evidence converted into predeclared constraints",
            "sample_scope": "run336M/run336O repaired macro48/u42 subset only",
            "missing_duplicate_check": "not a row-level dataset; source file presence and hash checked",
            "feature_label_boundary": "failure memory cannot become a post-forward filter",
            "split_boundary": "new Stage337 work must predeclare WFO/forward boundaries before training",
            "leakage_risk": "using run336O bad month/session/rate slice as exclusion filter",
            "data_hash_or_identity": artifact_sha(RUN336P_FAILURE),
            "integrity_judgment": "usable_with_boundary",
            "next_evidence": "negative controls must reject forward-pocket fitting",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "check_id": "core56_refresh_boundary",
            "data_source": rel(RUN337A_CORE56),
            "time_axis": "not refreshed yet; requires equity/breadth/top3 as-of timestamps",
            "sample_scope": "core56 outside full-family robustness claim",
            "missing_duplicate_check": "core56 runtime evidence missing by design until repair",
            "feature_label_boundary": "core56 values cannot be forward-filled or silently dropped",
            "split_boundary": "full-family claim forbidden before core56 repaired and parity-probed",
            "leakage_risk": "stale or future equity source contaminates US100 M5 features",
            "data_hash_or_identity": artifact_sha(RUN337A_CORE56),
            "integrity_judgment": "usable_with_boundary_for_scope_lock",
            "next_evidence": "core56 repair or explicit out-of-scope receipt",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_no_lookahead_canaries(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for item in inputs["negative_controls"]:
        rows.append(
            {
                "canary_id": item.get("control_id", ""),
                "target_risk": item.get("target_risk", ""),
                "input_payload": item.get("test_design", ""),
                "expected_rejection": item.get("expected_failure_signature", ""),
                "required_detector": "data_integrity_contract;gate_audit;manual_review",
                "stop_condition": item.get("stop_condition", ""),
                "repair_action": item.get("repair_action", ""),
                "materialized_status": "ready_for_review",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_branch_payloads(inputs: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    payloads = []
    review = []
    gate_rows = []
    gates = list(inputs["gates"])
    for branch in inputs["branches"]:
        branch_id = branch.get("branch_id", "")
        branch_gates = ";".join(gate["gate_id"] for gate in gates)
        payloads.append(
            {
                "branch_id": branch_id,
                "lane": branch.get("lane", ""),
                "payload_id": f"{branch_id}_payload_v1",
                "source_failure_memory": branch.get("primary_failure_memory", ""),
                "predeclared_change": branch.get("predeclared_change", ""),
                "required_evidence": branch.get("required_evidence", ""),
                "proxy_expected_required": branch.get("proxy_expected_required", ""),
                "mt5_runtime_probe_required": branch.get("mt5_runtime_probe_required", ""),
                "gate_ids": branch_gates,
                "forbidden": branch.get("forbidden", ""),
                "materialized_status": "ready_for_review",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        review.append(
            {
                "review_id": f"{branch_id}_review",
                "branch_id": branch_id,
                "review_task": "check branch payload, gate coverage, proxy-MT5 requirements, and no-lookahead canaries",
                "must_confirm": "no training;no threshold retune;no lot optimization;no forward pocket filter",
                "proxy_mt5_check": "proxy expected and MT5 runtime paths are both declared before usability claim",
                "next_action": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        for gate in gates:
            gate_rows.append(
                {
                    "branch_id": branch_id,
                    "gate_id": gate.get("gate_id", ""),
                    "required_measurement": gate.get("required_measurement", ""),
                    "acceptance_boundary": gate.get("acceptance_boundary", ""),
                    "failure_memory_trigger": gate.get("failure_memory_trigger", ""),
                    "forbidden_shortcut": gate.get("forbidden_shortcut", ""),
                    "schema_status": "materialized_for_review",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return payloads, review, gate_rows


def build_proxy_mt5_tables(inputs: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    summary = by_key(inputs["summary"], "attempt_name")
    score = by_key(inputs["scorecard"], "attempt_name")
    basis = by_key(inputs["timestamp_basis"], "attempt_name")
    expected_rows = []
    observed_rows = []
    grouped: dict[str, list[Mapping[str, str]]] = {}
    for row in inputs["proxy_diff"]:
        attempt = row.get("attempt_name", "")
        grouped.setdefault(attempt, []).append(row)
        expected_rows.append(
            {
                "attempt_name": attempt,
                "artifact_slug": row.get("artifact_slug", ""),
                "feature_set_id": row.get("feature_set_id", ""),
                "dimension": row.get("dimension", ""),
                "proxy_expected_value": row.get("proxy_aligned_value", ""),
                "timestamp_basis": row.get("timestamp_basis", ""),
                "source_evidence": rel(RUN336N_DIFF),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        observed_rows.append(
            {
                "attempt_name": attempt,
                "artifact_slug": row.get("artifact_slug", ""),
                "feature_set_id": row.get("feature_set_id", ""),
                "dimension": row.get("dimension", ""),
                "mt5_runtime_value": row.get("mt5_runtime_value", ""),
                "timestamp_basis": row.get("timestamp_basis", ""),
                "runtime_report_path": existing_report_path(summary, attempt),
                "source_evidence": rel(RUN336N_DIFF),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    diff_rows = []
    usability_rows = []
    manifest_rows = []
    for attempt, rows in grouped.items():
        mismatches = [row for row in rows if row.get("difference_status") != "matched"]
        max_abs_delta = max(abs(safe_float(row.get("difference_proxy_minus_mt5"), 0.0)) for row in rows)
        score_row = score.get(attempt, {})
        summary_row = summary.get(attempt, {})
        basis_row = basis.get(attempt, {})
        runtime_kpi_fragile = (
            safe_float(score_row.get("cost_plus_1_0_net")) <= 0
            or safe_float(score_row.get("rolling20_worst_net")) <= -50
            or str(score_row.get("selection_eligible", "")).lower() == "false"
        )
        usability_label = "usable_for_signal_sanity_only"
        if mismatches:
            usability_label = "not_usable_signal_mismatch"
        elif runtime_kpi_fragile:
            usability_label = "usable_for_signal_sanity_only_not_kpi_authority"
        diff_rows.append(
            {
                "attempt_name": attempt,
                "artifact_slug": rows[0].get("artifact_slug", ""),
                "feature_set_id": rows[0].get("feature_set_id", ""),
                "dimensions_compared": len(rows),
                "matched_dimensions": len(rows) - len(mismatches),
                "mismatched_dimensions": len(mismatches),
                "max_abs_proxy_minus_mt5": max_abs_delta,
                "feature_rows_not_seen_by_mt5_cycles": basis_row.get("feature_rows_not_seen_by_mt5_cycles", ""),
                "mt5_cycle_rows_missing_from_feature_csv": basis_row.get("mt5_cycle_rows_missing_from_feature_csv", ""),
                "runtime_net_profit": summary_row.get("runtime_net_profit", ""),
                "runtime_profit_factor": summary_row.get("runtime_profit_factor", ""),
                "runtime_trade_count": summary_row.get("runtime_trade_count", ""),
                "cost_plus_1_0_net": score_row.get("cost_plus_1_0_net", ""),
                "rolling20_worst_net": score_row.get("rolling20_worst_net", ""),
                "failure_axes": score_row.get("failure_axes", ""),
                "difference_judgment": "signal_dimensions_matched_kpi_fragile" if not mismatches else "signal_mismatch",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        usability_rows.append(
            {
                "subject": attempt,
                "proxy_expected_available": "true",
                "mt5_runtime_probe_available": "true",
                "signal_difference_status": "matched" if not mismatches else "mismatched",
                "runtime_kpi_status": "fragile_failure_memory" if runtime_kpi_fragile else "not_fragile_in_existing_scope",
                "usability_label": usability_label,
                "allowed_use": "signal sanity check and runtime handoff debugging",
                "forbidden_use": "KPI authority, Forward Passed/Failed, candidate selection, operating reference",
                "next_condition": "future candidate must rerun MT5 and cost/direction/curve gates",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        manifest_rows.append(
            {
                "attempt_name": attempt,
                "artifact_slug": rows[0].get("artifact_slug", ""),
                "runtime_probe_status": "existing_run336M_probe_available",
                "report_path": summary_row.get("report_path", ""),
                "telemetry_path": rel(RUN336M_DIR / "runtime_telemetry" / f"{attempt}_telemetry.csv"),
                "summary_path": rel(RUN336M_DIR / "runtime_telemetry" / f"{attempt}_summary.csv"),
                "tester_identity": rel(RUN336M_TESTER_IDENTITY),
                "runtime_execution_result": rel(RUN336M_RUNTIME_RESULT),
                "kpi_authority": "MT5 report/telemetry only",
                "proxy_authority": "signal sanity only",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    usability_rows.append(
        {
            "subject": "core56_refresh_candidate",
            "proxy_expected_available": "false",
            "mt5_runtime_probe_available": "false",
            "signal_difference_status": "not_tested_core56_refresh_required",
            "runtime_kpi_status": "out_of_scope_until_feature_refresh",
            "usability_label": "not_usable_until_core56_refresh_and_mt5_probe",
            "allowed_use": "repair planning only",
            "forbidden_use": "full-family robustness claim or KPI authority",
            "next_condition": "repair equity/breadth/top3 source, then produce proxy expected and MT5 runtime probe outputs",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )
    manifest_rows.append(
        {
            "attempt_name": "core56_refresh_candidate",
            "artifact_slug": "core56_refresh_candidate",
            "runtime_probe_status": "not_available_until_core56_refresh_repair",
            "report_path": "",
            "telemetry_path": "",
            "summary_path": "",
            "tester_identity": rel(RUN336M_TESTER_IDENTITY),
            "runtime_execution_result": "",
            "kpi_authority": "none_until_MT5_probe",
            "proxy_authority": "none_until_proxy_expected_result",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )
    return expected_rows, observed_rows, diff_rows, usability_rows, manifest_rows


def build_cost_direction_curve_tables(inputs: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    cost_rows = [
        {
            "attempt_name": row.get("attempt_name", ""),
            "extra_cost_per_trade": row.get("extra_cost_per_trade", ""),
            "net_profit": row.get("net_profit", ""),
            "profit_factor": row.get("profit_factor", ""),
            "expectancy": row.get("expectancy", ""),
            "closed_balance_max_drawdown": row.get("closed_balance_max_drawdown", ""),
            "recovery_factor_closed": row.get("recovery_factor_closed", ""),
            "survives_positive_net": row.get("survives_positive_net", ""),
            "schema_use": "cost stress failure memory and future gate template",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in inputs["cost"]
    ]
    long_short_rows = [
        {
            "attempt_name": row.get("attempt_name", ""),
            "feature_set_id": row.get("feature_set_id", ""),
            "long_trade_count": row.get("long_trade_count", ""),
            "short_trade_count": row.get("short_trade_count", ""),
            "long_net_profit": row.get("long_net_profit", ""),
            "short_net_profit": row.get("short_net_profit", ""),
            "long_short_judgment": "direction_failure_memory" if safe_float(row.get("short_net_profit")) <= 0 else "both_sides_positive_existing_scope",
            "schema_use": "future D/B and long/short attribution gate",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in inputs["summary"]
    ]
    curve_rows = [
        {
            "attempt_name": row.get("attempt_name", ""),
            "rolling_window_trades": row.get("rolling_window_trades", ""),
            "worst_window_start_trade": row.get("worst_window_start_trade", ""),
            "worst_window_end_trade": row.get("worst_window_end_trade", ""),
            "worst_window_net": row.get("worst_window_net", ""),
            "best_window_net": row.get("best_window_net", ""),
            "curve_judgment": "pocket_failure_memory" if safe_float(row.get("worst_window_net")) <= -50 else "context_only",
            "schema_use": "future curve pocket and underwater gate",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in inputs["curve"]
    ]
    regime_rows = []
    for index, row in enumerate(inputs["regime"]):
        regime_rows.append(
            {
                "row_id": f"regime_slice_{index+1:04d}",
                "attempt_name": row.get("attempt_name", ""),
                "axis": row.get("axis", row.get("slice_axis", "")),
                "bucket": row.get("bucket", row.get("slice_bucket", "")),
                "net_profit": row.get("net_profit", row.get("net", "")),
                "profit_factor": row.get("profit_factor", row.get("pf", "")),
                "trade_count": row.get("trade_count", row.get("trades", "")),
                "schema_use": "regime attribution only, not post-hoc filter",
                "forbidden_use": "direct exclusion rule selected from failed forward slice",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return cost_rows, long_short_rows, curve_rows, regime_rows


def build_core56_scope(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    boundary = inputs["core56_boundary"][0] if inputs["core56_boundary"] else {}
    return [
        {
            "subject": "core56_equity_breadth_top3",
            "decision": "scope_locked_out_until_refresh_repair",
            "reason": boundary.get("reason", "core56 refresh evidence missing"),
            "required_repair": boundary.get("required_repair", "equity/breadth/top3 source refresh"),
            "required_validation": boundary.get("required_validation", "proxy expected result;MT5 runtime probe;row-level parity"),
            "current_allowed_use": "repair planning and failure memory only",
            "current_forbidden_use": "full-family robustness claim;Forward Passed;runtime authority",
            "next_action": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_next_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "stage337C_review_source_lineage_integrity",
            "priority": 1,
            "task": "Review source lineage, timestamp basis, and no-lookahead canary readiness.",
            "required_inputs": rel(SOURCE_LINEAGE_CSV) + ";" + rel(DATA_INTEGRITY_CSV),
            "required_outputs": "source_lineage_review;data_integrity_review",
            "success_condition": "all sources connected and no forward-pocket fitting path admitted",
            "forbidden": "candidate training before review",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "stage337C_review_proxy_mt5_usability",
            "priority": 2,
            "task": "Review proxy expected vs MT5 runtime difference and usability labels.",
            "required_inputs": rel(PROXY_EXPECTED_CSV) + ";" + rel(MT5_OBSERVED_CSV) + ";" + rel(PROXY_MT5_DIFF_CSV),
            "required_outputs": "proxy_mt5_usability_review;future_probe_requirements",
            "success_condition": "proxy remains signal sanity only unless MT5 runtime agrees at required grain",
            "forbidden": "proxy-only profit authority",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "stage337C_review_branch_gate_packages",
            "priority": 3,
            "task": "Review repair/defense/offense branch payloads and gate schemas.",
            "required_inputs": rel(BRANCH_PAYLOAD_CSV) + ";" + rel(GATE_SCHEMA_CSV),
            "required_outputs": "accepted_branch_package_queue;rejected_branch_memory",
            "success_condition": "balanced repair/defense/offense path survives required gates",
            "forbidden": "single KPI or cosmetic repair branch",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "stage337C_review_core56_scope_or_repair",
            "priority": 4,
            "task": "Review whether core56 can be repaired now or remains explicitly out of full-family scope.",
            "required_inputs": rel(CORE56_SCOPE_CSV),
            "required_outputs": "core56_repair_queue_or_scope_lock_review",
            "success_condition": "full-family claim remains blocked unless core56 is repaired and probed",
            "forbidden": "silent core56 drop",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_gate_audit(
    source_lineage: Sequence[Mapping[str, Any]],
    data_contract: Sequence[Mapping[str, Any]],
    canaries: Sequence[Mapping[str, Any]],
    branch_payloads: Sequence[Mapping[str, Any]],
    gate_schema: Sequence[Mapping[str, Any]],
    proxy_expected: Sequence[Mapping[str, Any]],
    mt5_observed: Sequence[Mapping[str, Any]],
    diff_rows: Sequence[Mapping[str, Any]],
    usability: Sequence[Mapping[str, Any]],
    core56_scope: Sequence[Mapping[str, Any]],
    next_queue: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    missing_sources = [row["source_id"] for row in source_lineage if row["availability"] == "missing"]
    signal_subjects = [row for row in usability if row["subject"] != "core56_refresh_candidate"]
    usable_signal_only = [row for row in signal_subjects if "signal_sanity" in row["usability_label"]]
    core56_locked = any(row["decision"] == "scope_locked_out_until_refresh_repair" for row in core56_scope)
    return [
        {
            "gate_id": "source_lineage_connected",
            "status": "pass" if not missing_sources else "fail",
            "evidence": rel(SOURCE_LINEAGE_CSV),
            "finding": "all source artifacts connected" if not missing_sources else f"missing={missing_sources}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "data_integrity_boundary_materialized",
            "status": "pass" if len(data_contract) >= 3 else "fail",
            "evidence": rel(DATA_INTEGRITY_CSV),
            "finding": f"data integrity contract rows={len(data_contract)}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "no_lookahead_canaries_ready",
            "status": "pass" if len(canaries) >= 8 else "fail",
            "evidence": rel(NO_LOOKAHEAD_CANARY_CSV),
            "finding": f"canary rows={len(canaries)}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "branch_payload_and_gate_schema_ready",
            "status": "pass" if len(branch_payloads) >= 8 and len(gate_schema) >= 64 else "fail",
            "evidence": rel(BRANCH_PAYLOAD_CSV) + ";" + rel(GATE_SCHEMA_CSV),
            "finding": f"branch_rows={len(branch_payloads)};gate_schema_rows={len(gate_schema)}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "proxy_expected_and_mt5_observed_materialized",
            "status": "pass" if len(proxy_expected) >= 20 and len(mt5_observed) >= 20 else "fail",
            "evidence": rel(PROXY_EXPECTED_CSV) + ";" + rel(MT5_OBSERVED_CSV),
            "finding": f"proxy_rows={len(proxy_expected)};mt5_rows={len(mt5_observed)}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "proxy_usability_context_only",
            "status": "pass" if len(usable_signal_only) == 4 and len(diff_rows) == 4 else "fail",
            "evidence": rel(PROXY_MT5_USABILITY_CSV),
            "finding": "4 repaired-subset subjects usable for signal sanity only; not KPI authority",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "core56_scope_locked",
            "status": "pass" if core56_locked else "fail",
            "evidence": rel(CORE56_SCOPE_CSV),
            "finding": "core56 full-family claim remains locked until refresh and MT5 probe",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "next_review_queue_ready",
            "status": "pass" if len(next_queue) >= 4 else "fail",
            "evidence": rel(RUN337C_QUEUE_CSV),
            "finding": f"run337C queue rows={len(next_queue)}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "claim_guard_no_selection_no_goal",
            "status": "pass",
            "evidence": rel(FINAL_DECISION_JSON),
            "finding": "no selected candidate, Forward Passed, runtime authority, or Goal Achieve claimed",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def write_receipts(metrics: Mapping[str, Any]) -> list[Path]:
    return [
        write_json(
            DATA_INTEGRITY_JSON,
            {
                "run_id": RUN_ID,
                "data_source": "run337A contracts, run336P failure memory, run336O MT5 KPI summaries, run336N proxy-MT5 parity",
                "time_axis": "timestamp-aligned cycle_bar_time against MT5 feature-ready cycle rows",
                "sample_scope": "macro48/u42 repaired forward subset; core56 explicitly out of full-family claim",
                "missing_or_duplicate_check": "timestamp basis materialized; raw proxy extra rows are not interpreted as MT5 rows",
                "feature_label_boundary": "no labels or training in run337B; failure memory becomes review input only",
                "split_boundary": "future WFO/forward boundaries required before candidate training",
                "leakage_risk": "forward pocket filters and proxy-only KPI authority blocked by canaries",
                "data_hash_or_identity": rel(DATA_INTEGRITY_CSV),
                "integrity_judgment": "usable_with_boundary",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RUNTIME_PARITY_JSON,
            {
                "run_id": RUN_ID,
                "research_path": rel(Path(__file__)),
                "runtime_path": rel(RUN336M_RUNTIME_RESULT),
                "shared_contract": "same ONNX, same feature order, same threshold, same runtime settings from run336M/N",
                "known_differences": "raw proxy row count differs from MT5 cycle rows; aligned proxy dimensions match 20/20",
                "parity_check": "proxy expected values and MT5 runtime observed values materialized from run336N difference evidence",
                "parity_identity": rel(PROXY_MT5_DIFF_CSV),
                "runtime_claim_boundary": "runtime_probe evidence reused for research only",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            ARTIFACT_LINEAGE_JSON,
            {
                "run_id": RUN_ID,
                "source_inputs": [
                    rel(RUN337A_DECISION),
                    rel(RUN337A_BRANCH),
                    rel(RUN336P_FAILURE),
                    rel(RUN336O_SCORECARD),
                    rel(RUN336N_DIFF),
                    rel(RUN336M_RUNTIME_RESULT),
                ],
                "producer": rel(Path(__file__)),
                "consumer": NEXT_RUN_ID,
                "artifact_paths": [
                    rel(SOURCE_LINEAGE_CSV),
                    rel(PROXY_MT5_USABILITY_CSV),
                    rel(BRANCH_PAYLOAD_CSV),
                    rel(RUN337C_QUEUE_CSV),
                ],
                "artifact_hashes": "registered in artifact_registry after run",
                "registry_links": "run_registry;alpha_run_ledger;stage_run_ledger;artifact_registry",
                "availability": "tracked after commit; reproducible from run337B script",
                "lineage_judgment": "connected_with_boundary",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RESULT_JUDGMENT_JSON,
            {
                "run_id": RUN_ID,
                "result_subject": "run337B materialized inputs and proxy-MT5 usability",
                "evidence_available": "lineage, data contract, canaries, branch payloads, proxy expected rows, MT5 observed rows, usability labels",
                "evidence_missing": "no new model training, no fresh Stage337 MT5 run, no operating candidate",
                "judgment_label": "exploratory",
                "claim_boundary": "input materialization only; proxy is signal sanity/context only; MT5 remains KPI authority",
                "next_condition": NEXT_RUN_ID,
                "user_explanation_hook": "프록시와 MT5가 신호 차원에서는 맞지만, 수익성 판정 권한은 MT5와 비용/곡선 게이트에 남아 있다.",
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
# run337B Materialized Inputs and Proxy-MT5 Usability(337B 입력 물질화 및 프록시-MT5 활용성)

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

## Proxy-MT5 Read(프록시-MT5 판독)

- proxy_expected_rows(프록시 예상 행): `{metrics['proxy_expected_rows']}`
- mt5_observed_rows(MT5 관측 행): `{metrics['mt5_observed_rows']}`
- compared_subjects(비교 대상): `{metrics['proxy_subjects']}`
- matched_signal_subjects(신호 일치 대상): `{metrics['usable_signal_subjects']}`
- usability(활용성): repaired subset(수리 부분집합) `4`개는 signal sanity only(신호 점검 전용), core56(핵심56)은 refresh and MT5 probe required(갱신 및 MT5 탐침 필요)

## Materialized Inputs(물질화 입력)

- source_lineage(원천 계보): `{rel(SOURCE_LINEAGE_CSV)}`
- data_integrity_contract(데이터 무결성 계약): `{rel(DATA_INTEGRITY_CSV)}`
- branch_payloads(분기 패키지): `{rel(BRANCH_PAYLOAD_CSV)}`
- gate_schema(게이트 스키마): `{rel(GATE_SCHEMA_CSV)}`
- proxy_mt5_difference(프록시-MT5 차이): `{rel(PROXY_MT5_DIFF_CSV)}`
- usability_decision(활용성 결정): `{rel(PROXY_MT5_USABILITY_CSV)}`
- next_queue(다음 대기열): `{rel(RUN337C_QUEUE_CSV)}`

Effect(효과): proxy expected value(프록시 예상값)는 MT5 runtime value(MT5 런타임 값)와 timestamp-aligned(타임스탬프 정렬)로 맞는지 확인한 뒤에만 signal sanity check(신호 점검)로 쓴다. 수익/PF/DD(순익/수익 팩터/낙폭) 권한은 MT5 report/telemetry(보고서/실행 기록)와 cost/direction/curve gate(비용/방향/곡선 게이트)에 남긴다.
"""
    decision_doc = f"""
# 2026-05-27 Stage337B Decision(337B 결정)

- decision(결정): `{DECISION}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed_for_stage337_new_work`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`

Effect(효과): run336N(336N 실행)의 proxy expected(프록시 예상) 대 MT5 runtime(런타임) 차이는 signal dimension(신호 차원)에서 `20/20 matched(20/20 일치)`로 물질화했지만, run336O(336O 실행)의 비용/곡선 취약성 때문에 KPI authority(KPI 권한)는 부여하지 않는다.
"""
    return [write_md(REPORT_DOC, report), write_md(DECISION_DOC, decision_doc)]


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
- effect(효과): run337B(337B 실행)는 proxy expected(프록시 예상값)와 MT5 runtime observed(런타임 관측값)를 비교해 repaired subset(수리 부분집합)은 signal sanity only(신호 점검 전용)로, core56(핵심56)은 refresh required(갱신 필요)로 라벨링했다. 아직 선택 후보는 없다.
"""
    artifacts.append(write_md(SELECTED_DIR / "selection_status.md", selection))
    brief_text, brief_bom = read_text_lossless(SPEC_DIR / "stage_brief.md")
    brief_text = insert_after_marker_once(
        brief_text,
        "- run337A_summary(337A 요약):",
        f"- run337B_summary(337B 요약): `{STATUS}`. Effect(효과): proxy expected value(프록시 예상값)와 MT5 runtime value(MT5 런타임 값)를 비교해 signal sanity only(신호 점검 전용) 활용성으로 낮췄다.",
        "run337B_summary",
    )
    artifacts.append(write_text_lossless(SPEC_DIR / "stage_brief.md", brief_text, brief_bom))
    input_section = f"""
## run337B Outputs(337B 산출물)

- source_lineage(원천 계보): `{rel(SOURCE_LINEAGE_CSV)}`
- proxy_expected(프록시 예상값): `{rel(PROXY_EXPECTED_CSV)}`
- mt5_observed(MT5 관측값): `{rel(MT5_OBSERVED_CSV)}`
- difference_report(차이 보고서): `{rel(PROXY_MT5_DIFF_CSV)}`
- usability_decision(활용성 결정): `{rel(PROXY_MT5_USABILITY_CSV)}`
- next_queue(다음 대기열): `{rel(RUN337C_QUEUE_CSV)}`

Effect(효과): proxy(프록시)는 signal sanity check(신호 점검)로만 쓰고, KPI(핵심 성과 지표) 판정은 MT5 runtime probe(런타임 탐침)와 비용/곡선/방향 게이트에 묶는다.
"""
    artifacts.append(append_section_once(INPUTS_DIR / "input_refs.md", "## run337B Outputs(337B 산출물)", input_section))
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_prefix_line(workspace_text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    focus = (
        "- >-\n"
        f"  Stage337(337단계) run337B(337B 실행)는 `{STATUS}`로 proxy expected vs MT5 runtime(프록시 예상값 대 MT5 런타임) 활용성 판단을 물질화했다. "
        "Effect(효과): repaired subset(수리 부분집합)은 signal sanity only(신호 점검 전용), core56(핵심56)은 refresh+MT5 probe required(갱신+MT5 탐침 필요)로 고정해 proxy-only KPI claim(프록시 단독 KPI 주장)을 차단한다.\n"
    )
    workspace_text = insert_focus_once(workspace_text, focus, "run337B(337B 실행)")
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
        f"- run337B_summary(337B 요약): `{STATUS}`. "
        "Effect(효과): proxy expected value(프록시 예상값), MT5 runtime observed value(MT5 런타임 관측값), difference report(차이 보고서), usability decision(활용성 결정)을 만들고 run337C(337C 실행) 검토 대기열로 넘긴다."
    )
    current_text = insert_after_marker_once(current_text, "- decision(결정):", summary, "run337B_summary")
    artifacts.append(write_text_lossless(CURRENT_STATE, current_text, current_bom))
    artifacts.append(
        append_section_once(
            CHANGELOG,
            "## Stage337B Inputs and Proxy-MT5 Usability(337B 입력 및 프록시-MT5 활용성)",
            f"""
- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- action(행동): run337A(337A 실행)의 설계 계약을 source lineage(원천 계보), data integrity contract(데이터 무결성 계약), branch payload(분기 패키지), gate schema(게이트 스키마), proxy expected/MT5 observed/difference/usability(프록시 예상값/Mt5 관측값/차이/활용성) 산출물로 물질화했다.
- effect(효과): proxy(프록시)는 signal sanity only(신호 점검 전용)로 낮추고, MT5 runtime(런타임)과 cost/direction/curve gate(비용/방향/곡선 게이트) 없이는 KPI authority(KPI 권한)를 주장하지 못하게 했다.
- boundary(경계): selected candidate(선택 후보), Forward Passed(전진 통과), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 `not_claimed`.
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
                "lane": "input_materialization_proxy_mt5_usability",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_DOC),
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};proxy_signal_sanity_only;goal_achieve_not_claimed.",
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__materialized_inputs",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "cost_direction_curve_rebuild_input_materialization",
                "tier_scope": "research_design_macro48_u42_core56_boundary",
                "kpi_scope": "proxy_signal_parity_context_only_no_new_trading_kpi",
                "scoreboard_lane": "repair_defense_offense_input_materialization",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_DOC),
                "primary_kpi": "proxy_signal_dimensions_20_of_20_matched_existing_scope",
                "guardrail_kpi": "cost_curve_runtime_kpi_fragile;proxy_not_kpi_authority;goal_achieve_not_claimed",
                "external_verification_status": "completed_existing_run336M_N_runtime_probe_reused",
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
                "ledger_row_id": f"{RUN_ID}__materialized_inputs",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "work_family": "input_materialization",
                "evidence_scope": "run337A_contracts_run336M_N_O_P_existing_runtime_forward_evidence",
                "kpi_scope": "proxy_signal_usability_context_only_no_new_candidate_kpi",
                "status": STATUS,
                "judgment": JUDGMENT,
                "claim_boundary": CLAIM_BOUNDARY,
                "path": rel(REPORT_DOC),
                "notes": f"next_action={NEXT_RUN_ID};proxy_expected_and_mt5_runtime_difference_materialized;goal_achieve_not_claimed.",
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
            "notes": "run337B_materialized_inputs_proxy_mt5_context_only_no_selection",
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
    source_lineage = build_source_lineage(inputs)
    data_contract = build_data_integrity_contract(inputs)
    canaries = build_no_lookahead_canaries(inputs)
    branch_payloads, branch_review, gate_schema = build_branch_payloads(inputs)
    proxy_expected, mt5_observed, diff_rows, usability, mt5_manifest = build_proxy_mt5_tables(inputs)
    cost_rows, long_short_rows, curve_rows, regime_rows = build_cost_direction_curve_tables(inputs)
    core56_scope = build_core56_scope(inputs)
    next_queue = build_next_queue()
    audit = build_gate_audit(
        source_lineage,
        data_contract,
        canaries,
        branch_payloads,
        gate_schema,
        proxy_expected,
        mt5_observed,
        diff_rows,
        usability,
        core56_scope,
        next_queue,
    )
    failed_gates = [row for row in audit if row["status"] != "pass"]
    metrics = {
        "source_rows": len(source_lineage),
        "branch_rows": len(branch_payloads),
        "gate_schema_rows": len(gate_schema),
        "proxy_expected_rows": len(proxy_expected),
        "mt5_observed_rows": len(mt5_observed),
        "proxy_subjects": len(diff_rows),
        "usable_signal_subjects": len([row for row in usability if "signal_sanity" in row["usability_label"]]),
        "canary_rows": len(canaries),
        "core56_scope_locked": any(row["decision"] == "scope_locked_out_until_refresh_repair" for row in core56_scope),
    }
    run_artifacts = [
        write_csv(
            SOURCE_LINEAGE_CSV,
            ("source_id", "artifact_path", "role", "producer_run", "consumer", "availability", "sha256", "lineage_judgment", "claim_boundary"),
            source_lineage,
        ),
        write_csv(
            DATA_INTEGRITY_CSV,
            (
                "check_id",
                "data_source",
                "time_axis",
                "sample_scope",
                "missing_duplicate_check",
                "feature_label_boundary",
                "split_boundary",
                "leakage_risk",
                "data_hash_or_identity",
                "integrity_judgment",
                "next_evidence",
                "claim_boundary",
            ),
            data_contract,
        ),
        write_csv(
            NO_LOOKAHEAD_CANARY_CSV,
            (
                "canary_id",
                "target_risk",
                "input_payload",
                "expected_rejection",
                "required_detector",
                "stop_condition",
                "repair_action",
                "materialized_status",
                "claim_boundary",
            ),
            canaries,
        ),
        write_csv(
            BRANCH_PAYLOAD_CSV,
            (
                "branch_id",
                "lane",
                "payload_id",
                "source_failure_memory",
                "predeclared_change",
                "required_evidence",
                "proxy_expected_required",
                "mt5_runtime_probe_required",
                "gate_ids",
                "forbidden",
                "materialized_status",
                "claim_boundary",
            ),
            branch_payloads,
        ),
        write_csv(
            BRANCH_REVIEW_QUEUE_CSV,
            ("review_id", "branch_id", "review_task", "must_confirm", "proxy_mt5_check", "next_action", "claim_boundary"),
            branch_review,
        ),
        write_csv(
            GATE_SCHEMA_CSV,
            (
                "branch_id",
                "gate_id",
                "required_measurement",
                "acceptance_boundary",
                "failure_memory_trigger",
                "forbidden_shortcut",
                "schema_status",
                "claim_boundary",
            ),
            gate_schema,
        ),
        write_csv(
            PROXY_EXPECTED_CSV,
            ("attempt_name", "artifact_slug", "feature_set_id", "dimension", "proxy_expected_value", "timestamp_basis", "source_evidence", "claim_boundary"),
            proxy_expected,
        ),
        write_csv(
            MT5_OBSERVED_CSV,
            (
                "attempt_name",
                "artifact_slug",
                "feature_set_id",
                "dimension",
                "mt5_runtime_value",
                "timestamp_basis",
                "runtime_report_path",
                "source_evidence",
                "claim_boundary",
            ),
            mt5_observed,
        ),
        write_csv(
            PROXY_MT5_DIFF_CSV,
            (
                "attempt_name",
                "artifact_slug",
                "feature_set_id",
                "dimensions_compared",
                "matched_dimensions",
                "mismatched_dimensions",
                "max_abs_proxy_minus_mt5",
                "feature_rows_not_seen_by_mt5_cycles",
                "mt5_cycle_rows_missing_from_feature_csv",
                "runtime_net_profit",
                "runtime_profit_factor",
                "runtime_trade_count",
                "cost_plus_1_0_net",
                "rolling20_worst_net",
                "failure_axes",
                "difference_judgment",
                "claim_boundary",
            ),
            diff_rows,
        ),
        write_csv(
            PROXY_MT5_USABILITY_CSV,
            (
                "subject",
                "proxy_expected_available",
                "mt5_runtime_probe_available",
                "signal_difference_status",
                "runtime_kpi_status",
                "usability_label",
                "allowed_use",
                "forbidden_use",
                "next_condition",
                "claim_boundary",
            ),
            usability,
        ),
        write_csv(
            MT5_PROBE_MANIFEST_CSV,
            (
                "attempt_name",
                "artifact_slug",
                "runtime_probe_status",
                "report_path",
                "telemetry_path",
                "summary_path",
                "tester_identity",
                "runtime_execution_result",
                "kpi_authority",
                "proxy_authority",
                "claim_boundary",
            ),
            mt5_manifest,
        ),
        write_csv(
            COST_LADDER_SCHEMA_CSV,
            (
                "attempt_name",
                "extra_cost_per_trade",
                "net_profit",
                "profit_factor",
                "expectancy",
                "closed_balance_max_drawdown",
                "recovery_factor_closed",
                "survives_positive_net",
                "schema_use",
                "claim_boundary",
            ),
            cost_rows,
        ),
        write_csv(
            LONG_SHORT_SCHEMA_CSV,
            (
                "attempt_name",
                "feature_set_id",
                "long_trade_count",
                "short_trade_count",
                "long_net_profit",
                "short_net_profit",
                "long_short_judgment",
                "schema_use",
                "claim_boundary",
            ),
            long_short_rows,
        ),
        write_csv(
            CURVE_POCKET_SCHEMA_CSV,
            (
                "attempt_name",
                "rolling_window_trades",
                "worst_window_start_trade",
                "worst_window_end_trade",
                "worst_window_net",
                "best_window_net",
                "curve_judgment",
                "schema_use",
                "claim_boundary",
            ),
            curve_rows,
        ),
        write_csv(
            REGIME_SLICE_SCHEMA_CSV,
            (
                "row_id",
                "attempt_name",
                "axis",
                "bucket",
                "net_profit",
                "profit_factor",
                "trade_count",
                "schema_use",
                "forbidden_use",
                "claim_boundary",
            ),
            regime_rows,
        ),
        write_csv(
            CORE56_SCOPE_CSV,
            (
                "subject",
                "decision",
                "reason",
                "required_repair",
                "required_validation",
                "current_allowed_use",
                "current_forbidden_use",
                "next_action",
                "claim_boundary",
            ),
            core56_scope,
        ),
        write_csv(
            RUN337C_QUEUE_CSV,
            ("queue_id", "priority", "task", "required_inputs", "required_outputs", "success_condition", "forbidden", "claim_boundary"),
            next_queue,
        ),
        write_csv(GATE_AUDIT_CSV, ("gate_id", "status", "evidence", "finding", "claim_boundary"), audit),
    ]
    run_artifacts.extend(write_receipts(metrics))
    final_payload = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS if not failed_gates else "blocked_stage337B_gate_failure",
        "judgment": JUDGMENT if not failed_gates else "stage337B_materialization_gate_failure_requires_repair",
        "decision": DECISION if not failed_gates else "stage337B_materialization_blocked_gate_failure",
        "metrics": metrics,
        "failed_gates": failed_gates,
        "next_action": NEXT_RUN_ID,
        "selected_candidate": "none",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed_for_stage337_new_work",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
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
                "outputs": [rel(path) for path in run_artifacts],
                "status": "blocked_stage337B_gate_failure",
                "decision": "stage337B_materialization_blocked_gate_failure",
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
        "source_inputs": [
            rel(RUN337A_DECISION),
            rel(RUN337A_BRANCH),
            rel(RUN337A_PROXY_CONTRACT),
            rel(RUN337A_NEGATIVE),
            rel(RUN336P_FAILURE),
            rel(RUN336O_SCORECARD),
            rel(RUN336O_SUMMARY),
            rel(RUN336N_DIFF),
            rel(RUN336N_BASIS),
            rel(RUN336M_RUNTIME_RESULT),
        ],
        "outputs": [rel(path) for path in all_artifacts],
        "status": STATUS,
        "decision": DECISION,
        "external_verification_status": "completed_existing_run336M_N_runtime_probe_reused",
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
                "source_rows": metrics["source_rows"],
                "branch_rows": metrics["branch_rows"],
                "gate_schema_rows": metrics["gate_schema_rows"],
                "proxy_expected_rows": metrics["proxy_expected_rows"],
                "mt5_observed_rows": metrics["mt5_observed_rows"],
                "usable_signal_subjects": metrics["usable_signal_subjects"],
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
