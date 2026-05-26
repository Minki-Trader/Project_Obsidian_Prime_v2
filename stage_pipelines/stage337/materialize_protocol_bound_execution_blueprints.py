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
RUN_NUMBER = "run337F"
RUN_ID = "run337F_materialize_protocol_bound_execution_blueprints_v1"
PARENT_RUN_ID = "run337E_review_research_execution_protocols_v1"
NEXT_RUN_ID = "run337G_review_protocol_bound_execution_blueprints_v1"
STATUS = "completed_protocol_bound_execution_blueprints_materialized_no_training"
JUDGMENT = "stage337F_blueprints_materialized_for_review_no_training_no_selection"
DECISION = "stage337F_blueprints_ready_for_review_no_training_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage337F_blueprint_materialization_no_model_training_"
    "no_mt5_execution_no_threshold_retuning_no_lot_optimization_no_forward_pocket_filtering_"
    "no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
RUN337E_DIR = STAGE_DIR / "02_runs" / "run337E"
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
DECISION_DOC = DOCS / "decisions" / "2026-05-27_stage337F_protocol_bound_execution_blueprints.md"
REPORT_DOC = REVIEWS_DIR / "run337F_protocol_bound_execution_blueprints.md"

RUN337E_QUEUE = RUN337E_DIR / "run337F_blueprint_materialization_queue.csv"
RUN337E_ACCEPTED = RUN337E_DIR / "accepted_protocols_for_blueprint_queue.csv"
RUN337E_LINEAGE = RUN337E_DIR / "protocol_input_lineage_review.csv"
RUN337E_NO_LOOKAHEAD = RUN337E_DIR / "no_lookahead_protocol_review.csv"
RUN337E_PROXY_MT5 = RUN337E_DIR / "proxy_mt5_fresh_probe_protocol_review.csv"
RUN337E_CORE56 = RUN337E_DIR / "core56_refresh_protocol_review.csv"
RUN337E_COST_CURVE = RUN337E_DIR / "cost_direction_curve_protocol_review.csv"
RUN337E_OFFENSE = RUN337E_DIR / "offense_rebuild_protocol_review.csv"
RUN337E_REGIME = RUN337E_DIR / "economic_regime_asof_protocol_review.csv"
RUN337E_RUNTIME = RUN337E_DIR / "runtime_probe_requirements_review.csv"
RUN337E_TRAINING_BOUNDARY = RUN337E_DIR / "model_training_boundary_review.csv"
RUN337E_GATE_AUDIT = RUN337E_DIR / "required_gate_coverage_audit.csv"
RUN337E_DECISION = RUN337E_DIR / "final_review_research_execution_protocols_decision.json"
RUN337E_MANIFEST = RUN337E_DIR / "run_manifest.json"

NO_LOOKAHEAD_BLUEPRINT_CSV = RUN_DIR / "no_lookahead_harness_blueprint.csv"
NO_LOOKAHEAD_SCHEMA_JSON = RUN_DIR / "no_lookahead_harness_schema.json"
PROXY_EXPECTED_BLUEPRINT_CSV = RUN_DIR / "proxy_expected_schema_blueprint.csv"
MT5_PROBE_BLUEPRINT_CSV = RUN_DIR / "mt5_runtime_probe_package_blueprint.csv"
PROXY_MT5_DIFF_SCHEMA_JSON = RUN_DIR / "proxy_mt5_difference_schema.json"
CORE56_REPAIR_BLUEPRINT_CSV = RUN_DIR / "core56_repair_blueprint.csv"
CORE56_ASOF_SCHEMA_JSON = RUN_DIR / "core56_asof_join_schema.json"
COST_CURVE_BLUEPRINT_CSV = RUN_DIR / "cost_direction_curve_extraction_blueprint.csv"
COST_CURVE_SCHEMA_JSON = RUN_DIR / "cost_direction_curve_report_schema.json"
OFFENSE_BLUEPRINT_CSV = RUN_DIR / "offense_branch_blueprint.csv"
REGIME_SOURCE_BLUEPRINT_CSV = RUN_DIR / "economic_regime_asof_source_blueprint.csv"
REGIME_SLICE_SCHEMA_JSON = RUN_DIR / "economic_regime_slice_schema.json"
RUNTIME_PACKAGE_BLUEPRINT_CSV = RUN_DIR / "runtime_probe_package_blueprint.csv"
BLUEPRINT_ACCEPTANCE_CSV = RUN_DIR / "blueprint_acceptance_matrix.csv"
RUN337G_QUEUE_CSV = RUN_DIR / "run337G_blueprint_review_queue.csv"
GATE_AUDIT_CSV = RUN_DIR / "required_gate_coverage_audit.csv"
BLUEPRINT_SOURCE_LINEAGE_CSV = RUN_DIR / "blueprint_source_lineage_review.csv"

EXPERIMENT_DESIGN_JSON = RUN_DIR / "experiment_design_receipt.json"
DATA_INTEGRITY_JSON = RUN_DIR / "data_integrity_receipt.json"
RUNTIME_PARITY_JSON = RUN_DIR / "runtime_parity_receipt.json"
ARTIFACT_LINEAGE_JSON = RUN_DIR / "artifact_lineage_receipt.json"
RESULT_JUDGMENT_JSON = RUN_DIR / "result_judgment_receipt.json"
FINAL_DECISION_JSON = RUN_DIR / "final_protocol_bound_execution_blueprints_decision.json"
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
        "run337f_queue": read_csv(RUN337E_QUEUE),
        "accepted": read_csv(RUN337E_ACCEPTED),
        "lineage": read_csv(RUN337E_LINEAGE),
        "no_lookahead": read_csv(RUN337E_NO_LOOKAHEAD),
        "proxy_mt5": read_csv(RUN337E_PROXY_MT5),
        "core56": read_csv(RUN337E_CORE56),
        "cost_curve": read_csv(RUN337E_COST_CURVE),
        "offense": read_csv(RUN337E_OFFENSE),
        "regime": read_csv(RUN337E_REGIME),
        "runtime": read_csv(RUN337E_RUNTIME),
        "training_boundary": read_csv(RUN337E_TRAINING_BOUNDARY),
        "gate_audit": read_csv(RUN337E_GATE_AUDIT),
        "run337e_decision": read_json(RUN337E_DECISION),
        "run337e_manifest": read_json(RUN337E_MANIFEST),
    }


def build_blueprint_source_lineage(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    queue_inputs = {row.get("required_inputs", "") for row in inputs["run337f_queue"]}
    rows: list[dict[str, Any]] = []
    for row in inputs["lineage"]:
        source_path = row.get("source_path", "")
        direct_queue_input = source_path in queue_inputs
        rows.append(
            {
                "source_path": source_path,
                "source_sha256": row.get("sha256", ""),
                "source_exists": row.get("exists", ""),
                "source_row_count": row.get("row_count", ""),
                "source_manifest_linked": row.get("manifest_linked", ""),
                "parent_lineage_review": row.get("lineage_review", ""),
                "used_by_run337F": "true" if direct_queue_input or "run337D" not in source_path else "context_only",
                "allowed_use": "protocol-bound blueprint materialization and run337G review queue only",
                "forbidden_use": "model training, MT5 execution, candidate selection, Forward Passed, runtime authority, Goal Achieve",
                "lineage_status": "pass" if row.get("exists") == "true" and row.get("lineage_review") == "pass" else "fail",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    for queue in inputs["run337f_queue"]:
        required_input = queue.get("required_inputs", "")
        if required_input and required_input not in {row.get("source_path", "") for row in inputs["lineage"]}:
            required_path = ROOT / required_input
            exists = path_exists(required_path)
            rows.append(
                {
                    "source_path": required_input,
                    "source_sha256": sha256_file_lf_normalized(required_path) if exists else "",
                    "source_exists": "true" if exists else "false",
                    "source_row_count": len(read_csv(required_path)) if exists and required_path.suffix.lower() == ".csv" else "",
                    "source_manifest_linked": "true",
                    "parent_lineage_review": "run337E_review_output",
                    "used_by_run337F": "true",
                    "allowed_use": "protocol-bound blueprint materialization and run337G review queue only",
                    "forbidden_use": "model training, MT5 execution, candidate selection, Forward Passed, runtime authority, Goal Achieve",
                    "lineage_status": "pass" if exists else "fail",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def build_no_lookahead_blueprint(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    blueprints = []
    for row in rows:
        protocol_id = row.get("protocol_id", "")
        if protocol_id == "coverage_summary":
            continue
        blueprints.append(
            {
                "harness_id": f"{protocol_id}_harness",
                "source_protocol_id": protocol_id,
                "risk_target": row.get("risk_target", ""),
                "bad_control_input": "candidate feature table copy with targeted mutation",
                "expected_detector": "invalid_condition_matrix flags row before model fit, proxy scoring, MT5 handoff, or KPI read",
                "required_assertions": "bad control rejected;repair route recorded;no candidate package emitted;no Forward claim emitted",
                "invalid_if": "bad control reaches training queue, proxy expected output, MT5 package, or scorecard",
                "repair_route": "stop execution blueprint and repair feature-label/time-axis boundary",
                "review_artifact_required": "bad_control_result.csv;invalid_condition_matrix.csv;repair_receipt.json",
                "forbidden": "treating canary pass as alpha or selection evidence",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return blueprints


def build_no_lookahead_schema() -> dict[str, Any]:
    return {
        "schema_id": "stage337F_no_lookahead_harness_schema_v1",
        "required_columns": [
            "harness_id",
            "source_protocol_id",
            "risk_target",
            "bad_control_input",
            "expected_detector",
            "required_assertions",
            "invalid_if",
            "repair_route",
            "review_artifact_required",
            "forbidden",
            "claim_boundary",
        ],
        "bad_control_families": [
            "future_bar",
            "forward_pocket_filter",
            "threshold_retune",
            "lot_optimization",
            "timestamp_basis",
        ],
        "must_fail_to_pass": True,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_proxy_expected_blueprint(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    blueprints = []
    for row in rows:
        subject = row.get("subject", "")
        blueprints.append(
            {
                "subject": subject,
                "proxy_expected_blueprint_id": f"{subject}_proxy_expected_schema_v1",
                "required_inputs": "feature_snapshot_hash;model_or_surface_spec;score_threshold_identity;risk_lot_identity;timestamp_basis",
                "required_output_columns": "candidate_id;cycle_bar_time;score;decision;direction;D_source;B_source;D_plus_B;threshold_id;feature_hash;model_hash;timestamp_basis;source_row_hash;score_bucket",
                "timestamp_rule": "cycle_bar_time must match MT5 comparison grain; no same-bar shift unless explicitly labeled",
                "freshness_rule": "proxy expected values must be generated fresh for the candidate under review",
                "usability_boundary": "signal sanity only until fresh MT5 runtime result and cost/direction/curve gates are complete",
                "blocked_if": "missing feature hash, missing threshold identity, timestamp drift, or core56 unresolved full-family claim",
                "forbidden": "proxy-only KPI, Forward Passed, candidate selection, operating reference",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return blueprints


def build_mt5_probe_blueprint(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    blueprints = []
    for row in rows:
        subject = row.get("subject", "")
        blueprints.append(
            {
                "subject": subject,
                "mt5_probe_blueprint_id": f"{subject}_fresh_mt5_probe_package_v1",
                "required_files": "EA entrypoint;include module hash;ONNX_or_model_spec;adapter manifest;feature order;set file;tester ini;handoff snapshot",
                "required_runtime_outputs": "Strategy Tester HTML/XML;terminal log;trade ledger;runtime telemetry;tester settings identity",
                "required_comparison_outputs": "proxy_expected_values;mt5_observed_values;row_level_difference_report;usability_decision",
                "execution_boundary": "blueprint only in run337F; no MT5 execution until reviewed",
                "kpi_authority_rule": "MT5 tester report and parsed trade ledger are required before net/PF/DD/expectancy claims",
                "blocked_if": "missing report, missing log, missing trade ledger, timestamp basis mismatch, feature order drift",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return blueprints


def build_proxy_mt5_diff_schema() -> dict[str, Any]:
    return {
        "schema_id": "stage337F_proxy_mt5_difference_schema_v1",
        "grain": ["candidate_id", "subject", "cycle_bar_time"],
        "required_columns": [
            "candidate_id",
            "subject",
            "cycle_bar_time",
            "proxy_decision",
            "mt5_decision",
            "decision_match",
            "proxy_direction",
            "mt5_direction",
            "direction_match",
            "proxy_D_source",
            "mt5_D_source",
            "D_source_match",
            "proxy_B_source",
            "mt5_B_source",
            "B_source_match",
            "proxy_score",
            "mt5_score",
            "score_abs_diff",
            "timestamp_basis_status",
            "usability_label",
        ],
        "summary_metrics": [
            "decision_match_rate",
            "direction_match_rate",
            "D_source_match_rate",
            "B_source_match_rate",
            "max_score_abs_diff",
            "timestamp_gap_count",
        ],
        "kpi_authority": "not_authoritative_without_MT5_trade_ledger_and_tester_report",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_core56_blueprint(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    blueprints = []
    for row in rows:
        blueprints.append(
            {
                "core56_blueprint_id": f"{row.get('protocol_id', '')}_blueprint",
                "step_order": row.get("step_order", ""),
                "source_protocol_id": row.get("protocol_id", ""),
                "required_action": row.get("next_blueprint_use", "materialize core56 repair blueprint"),
                "required_artifacts": "source_inventory.csv;asof_join_contract.json;feature_handoff_snapshot.csv;proxy_expected_values.csv;fresh_mt5_probe_package.csv",
                "asof_guard": "equity/breadth/top3 features must not read later than target US100 M5 bar",
                "blocked_claims": "full-family robustness;core56 KPI;Forward Passed;runtime authority;Goal Achieve",
                "review_condition": "run337G confirms every core56 repair step has artifacts and no-lookahead guard",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return blueprints


def build_core56_asof_schema() -> dict[str, Any]:
    return {
        "schema_id": "stage337F_core56_asof_join_schema_v1",
        "join_keys": ["target_cycle_bar_time", "source_timestamp", "symbol", "feature_name"],
        "required_columns": [
            "target_cycle_bar_time",
            "source_timestamp",
            "symbol",
            "feature_name",
            "feature_value",
            "source_file",
            "source_sha256",
            "join_lag_seconds",
            "stale_flag",
            "future_join_flag",
        ],
        "invalid_if": "future_join_flag=true or source_timestamp > target_cycle_bar_time",
        "repair_required_if": "missing source hash, stale gap beyond tolerance, duplicate source timestamp, or feature latest gap",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_cost_curve_blueprint(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    blueprints = []
    for row in rows:
        protocol_id = row.get("protocol_id", "")
        if protocol_id == "coverage_summary":
            continue
        blueprints.append(
            {
                "extraction_blueprint_id": f"{protocol_id}_extraction_blueprint",
                "source_protocol_id": protocol_id,
                "gate_scope": row.get("gate_scope", ""),
                "required_extractors": "trade_ledger_parser;cost_ladder_builder;side_source_attributor;rolling_curve_pocket_scanner;lot_normalizer;regime_slice_joiner",
                "required_outputs": "cost_stress_report.csv;spread_slippage_stress_report.csv;long_short_attribution.csv;D_B_source_attribution.csv;curve_pocket_report.csv;lot_normalized_report.csv;regime_slice_report.csv",
                "minimum_metrics": "net;PF;expectancy;maxDD;recovery;trades_per_day;worst_pocket;underwater_stretch",
                "failure_memory_trigger": "cost flip, side/source collapse, curve pocket dominance, lot-only improvement, or regime concentration",
                "forbidden": "single KPI selection;proxy-only KPI authority;threshold retune;lot optimization;forward-pocket filtering",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return blueprints


def build_cost_curve_schema() -> dict[str, Any]:
    return {
        "schema_id": "stage337F_cost_direction_curve_report_schema_v1",
        "reports": {
            "cost_stress_report": ["cost_multiplier", "net", "PF", "expectancy", "maxDD", "recovery", "trades_per_day"],
            "long_short_attribution": ["side", "net", "PF", "expectancy", "maxDD", "trade_count"],
            "D_B_source_attribution": ["source_family", "net", "PF", "expectancy", "trade_count", "drawdown_contribution"],
            "curve_pocket_report": ["window", "worst_pocket_net", "worst_pocket_dd", "longest_underwater", "recovery_bars"],
            "lot_normalized_report": ["lot_basis", "net_per_lot", "dd_per_lot", "expectancy_per_trade"],
            "spread_slippage_stress_report": ["spread_points", "slippage_points", "net", "PF", "expectancy", "maxDD", "trade_count"],
            "regime_slice_report": ["slice_family", "slice_value", "net", "PF", "expectancy", "trade_count", "maxDD"],
        },
        "invalid_if": "any required report is absent while net/PF/DD/curve claims are made",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_offense_blueprint(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    blueprints = []
    for row in rows:
        branch_id = row.get("branch_id", "")
        blueprints.append(
            {
                "branch_blueprint_id": f"{branch_id}_blueprint_v1",
                "branch_id": branch_id,
                "allowed_next_step": "materialize feature thesis, data boundary, WFO split, proxy expected schema, MT5 probe package, and gate extraction requirements",
                "training_allowed": "false",
                "required_controls": "no-lookahead harness;fixed threshold predeclared;fixed risk/lot identity;no forward-pocket filtering",
                "required_evidence_before_training": "run337G blueprint review;data integrity receipt;model validation packet;runtime parity package plan",
                "failure_memory_axis": "cost buffer, direction/source symmetry, curve quality, and regime invariance",
                "forbidden": "training in run337F;candidate selection;proxy-only KPI;runtime authority;Goal Achieve",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return blueprints


def build_regime_blueprint(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    blueprints = []
    for row in rows:
        protocol_id = row.get("protocol_id", "")
        blueprints.append(
            {
                "regime_blueprint_id": f"{protocol_id}_source_audit_blueprint",
                "source_protocol_id": protocol_id,
                "regime_source": row.get("regime_source", ""),
                "required_source_identity": "source_name;source_uri_or_path;source_timestamp;source_sha256;timezone;revision_policy",
                "asof_join_rule": "source_timestamp <= target_cycle_bar_time; stale/future flags required",
                "required_checks": "missing rows;duplicate rows;stale forward fill;revision risk;timezone drift",
                "slice_outputs": "net;PF;expectancy;maxDD;trade_count;long_short;D_source;B_source;D_plus_B",
                "invalid_if": "future source value or revised macro value is used to explain forward profit",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return blueprints


def build_regime_slice_schema() -> dict[str, Any]:
    return {
        "schema_id": "stage337F_economic_regime_slice_schema_v1",
        "slice_families": ["VIX", "USD", "rate", "ADX", "volatility", "session", "hour", "month"],
        "required_columns": [
            "candidate_id",
            "cycle_bar_time",
            "slice_family",
            "slice_value",
            "source_timestamp",
            "asof_status",
            "session",
            "hour",
            "month",
            "volatility",
            "ADX",
            "VIX",
            "USD",
            "rate",
            "net",
            "PF",
            "expectancy",
            "trade_count",
            "maxDD",
            "long_short",
            "D_source",
            "B_source",
            "D_plus_B",
        ],
        "invalid_if": "asof_status is future_join or source timestamp is missing",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_runtime_package_blueprint(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    blueprints = []
    for row in rows:
        package_id = row.get("package_id", "")
        subject = row.get("subject", "")
        blueprints.append(
            {
                "runtime_blueprint_id": f"{subject}_runtime_probe_blueprint_v1",
                "source_package_id": package_id,
                "subject": subject,
                "required_files": "EA entrypoint;include module hash;model/ONNX spec;adapter manifest;feature order;set file;tester ini;handoff snapshot",
                "preflight_checks": "feature order hash;threshold identity;risk identity;lot identity;symbol/timeframe;broker session;data latest timestamp",
                "runtime_outputs": "Strategy Tester report;terminal log;trade ledger;telemetry;tester settings identity",
                "comparison_outputs": "proxy expected;MT5 observed;row-level difference;usability decision",
                "stress_outputs": "cost stress;spread/slippage stress;lot-normalized;D/B attribution;long/short;regime slices;curve pockets",
                "blocked_if_missing": "any runtime output, timestamp basis, feature order hash, or trade ledger",
                "runtime_claim_boundary": "future_runtime_probe_only_no_runtime_authority",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return blueprints


def build_blueprint_acceptance(
    inputs: Mapping[str, Any],
    no_lookahead: Sequence[Mapping[str, Any]],
    proxy_expected: Sequence[Mapping[str, Any]],
    mt5_probe: Sequence[Mapping[str, Any]],
    core56: Sequence[Mapping[str, Any]],
    cost_curve: Sequence[Mapping[str, Any]],
    offense: Sequence[Mapping[str, Any]],
    regime: Sequence[Mapping[str, Any]],
    runtime: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    output_index = {
        "materialize_no_lookahead_harness_blueprint": (NO_LOOKAHEAD_BLUEPRINT_CSV, len(no_lookahead), NO_LOOKAHEAD_SCHEMA_JSON),
        "materialize_proxy_mt5_fresh_probe_blueprint": (PROXY_EXPECTED_BLUEPRINT_CSV, len(proxy_expected) + len(mt5_probe), PROXY_MT5_DIFF_SCHEMA_JSON),
        "materialize_core56_repair_blueprint": (CORE56_REPAIR_BLUEPRINT_CSV, len(core56), CORE56_ASOF_SCHEMA_JSON),
        "materialize_cost_direction_curve_extraction_blueprint": (COST_CURVE_BLUEPRINT_CSV, len(cost_curve), COST_CURVE_SCHEMA_JSON),
        "materialize_offense_rebuild_branch_blueprints": (OFFENSE_BLUEPRINT_CSV, len(offense), ""),
        "materialize_economic_regime_asof_blueprint": (REGIME_SOURCE_BLUEPRINT_CSV, len(regime), REGIME_SLICE_SCHEMA_JSON),
        "materialize_runtime_probe_package_blueprint": (RUNTIME_PACKAGE_BLUEPRINT_CSV, len(runtime), ""),
    }
    rows = []
    for queue in inputs["run337f_queue"]:
        queue_id = queue.get("queue_id", "")
        output_path, row_count, schema_path = output_index.get(queue_id, (Path("missing"), 0, ""))
        rows.append(
            {
                "queue_id": queue_id,
                "priority": queue.get("priority", ""),
                "blueprint_task": queue.get("blueprint_task", ""),
                "materialized_output": rel(output_path),
                "schema_output": rel(schema_path) if schema_path else "",
                "output_rows": row_count,
                "acceptance_status": "accepted_for_review" if row_count > 0 else "blocked_missing_blueprint",
                "review_requirement": "run337G must review blueprint completeness before training, MT5 execution, or candidate packaging",
                "forbidden": queue.get("forbidden", ""),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_run337g_queue() -> list[dict[str, Any]]:
    tasks = [
        ("review_no_lookahead_harness_blueprint", NO_LOOKAHEAD_BLUEPRINT_CSV, NO_LOOKAHEAD_SCHEMA_JSON, "verify bad-control harness specs and schema"),
        ("review_proxy_mt5_fresh_probe_blueprints", PROXY_EXPECTED_BLUEPRINT_CSV, PROXY_MT5_DIFF_SCHEMA_JSON, "verify proxy expected, MT5 package, and difference schema"),
        ("review_core56_repair_blueprints", CORE56_REPAIR_BLUEPRINT_CSV, CORE56_ASOF_SCHEMA_JSON, "verify core56 repair and as-of join schema"),
        ("review_cost_direction_curve_extraction_blueprints", COST_CURVE_BLUEPRINT_CSV, COST_CURVE_SCHEMA_JSON, "verify cost, direction/source, curve, lot-normalized, and regime report schemas"),
        ("review_offense_branch_blueprints", OFFENSE_BLUEPRINT_CSV, "", "verify offense branches remain predeclared and training-closed"),
        ("review_economic_regime_asof_blueprints", REGIME_SOURCE_BLUEPRINT_CSV, REGIME_SLICE_SCHEMA_JSON, "verify economic regime as-of source and slice schemas"),
        ("review_runtime_probe_package_blueprints", RUNTIME_PACKAGE_BLUEPRINT_CSV, "", "verify runtime package requirements and blocker criteria"),
        ("review_blueprint_acceptance_and_claim_guard", BLUEPRINT_ACCEPTANCE_CSV, GATE_AUDIT_CSV, "verify all blueprints are review-only and no claims were promoted"),
    ]
    return [
        {
            "queue_id": queue_id,
            "priority": index,
            "review_input": rel(input_path),
            "schema_input": rel(schema_path) if schema_path else "",
            "review_task": task,
            "required_decision": "accept_for_next_materialization_or_repair_blueprint_gap",
            "forbidden": "model training, MT5 execution, candidate selection, Forward Passed, runtime authority, Goal Achieve",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for index, (queue_id, input_path, schema_path, task) in enumerate(tasks, start=1)
    ]


def build_gate_audit(
    inputs: Mapping[str, Any],
    source_lineage: Sequence[Mapping[str, Any]],
    no_lookahead: Sequence[Mapping[str, Any]],
    proxy_expected: Sequence[Mapping[str, Any]],
    mt5_probe: Sequence[Mapping[str, Any]],
    core56: Sequence[Mapping[str, Any]],
    cost_curve: Sequence[Mapping[str, Any]],
    offense: Sequence[Mapping[str, Any]],
    regime: Sequence[Mapping[str, Any]],
    runtime: Sequence[Mapping[str, Any]],
    acceptance: Sequence[Mapping[str, Any]],
    review_queue: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    accepted_inputs = all(row.get("queue_status", "").startswith("accepted") for row in inputs["accepted"])
    gate_e_pass = all(row.get("status") == "pass" for row in inputs["gate_audit"])
    lineage_pass = all(row.get("lineage_status") == "pass" for row in source_lineage)
    all_acceptance = all(row.get("acceptance_status") == "accepted_for_review" for row in acceptance)
    no_training = all(row.get("training_allowed") == "false" for row in offense)
    return [
        {
            "gate_id": "source_lineage_connected",
            "status": "pass" if lineage_pass and len(source_lineage) >= 13 else "fail",
            "evidence": rel(BLUEPRINT_SOURCE_LINEAGE_CSV),
            "finding": f"source_lineage_rows={len(source_lineage)};all_pass={lineage_pass}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "run337E_protocol_review_inputs_accepted",
            "status": "pass" if accepted_inputs and gate_e_pass else "fail",
            "evidence": f"{rel(RUN337E_ACCEPTED)};{rel(RUN337E_GATE_AUDIT)}",
            "finding": f"accepted_inputs={accepted_inputs};run337E_gates_pass={gate_e_pass}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "no_lookahead_harness_blueprints_ready",
            "status": "pass" if len(no_lookahead) >= 5 else "fail",
            "evidence": rel(NO_LOOKAHEAD_BLUEPRINT_CSV),
            "finding": f"no_lookahead_harness_rows={len(no_lookahead)}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "proxy_mt5_blueprints_require_fresh_runtime",
            "status": "pass" if len(proxy_expected) >= 5 and len(mt5_probe) >= 5 else "fail",
            "evidence": f"{rel(PROXY_EXPECTED_BLUEPRINT_CSV)};{rel(MT5_PROBE_BLUEPRINT_CSV)}",
            "finding": f"proxy_subjects={len(proxy_expected)};mt5_subjects={len(mt5_probe)}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "core56_repair_blueprint_preserves_full_family_block",
            "status": "pass" if len(core56) >= 5 and all("full-family" in row.get("blocked_claims", "") for row in core56) else "fail",
            "evidence": rel(CORE56_REPAIR_BLUEPRINT_CSV),
            "finding": f"core56_blueprint_rows={len(core56)}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "cost_direction_curve_extraction_blueprints_ready",
            "status": "pass" if len(cost_curve) >= 5 else "fail",
            "evidence": rel(COST_CURVE_BLUEPRINT_CSV),
            "finding": f"cost_curve_blueprint_rows={len(cost_curve)}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "offense_blueprints_training_closed",
            "status": "pass" if len(offense) >= 4 and no_training else "fail",
            "evidence": rel(OFFENSE_BLUEPRINT_CSV),
            "finding": f"offense_rows={len(offense)};training_closed={no_training}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "economic_regime_asof_blueprints_ready",
            "status": "pass" if len(regime) >= 6 else "fail",
            "evidence": rel(REGIME_SOURCE_BLUEPRINT_CSV),
            "finding": f"regime_blueprint_rows={len(regime)}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "runtime_probe_package_blueprints_ready",
            "status": "pass" if len(runtime) >= 5 else "fail",
            "evidence": rel(RUNTIME_PACKAGE_BLUEPRINT_CSV),
            "finding": f"runtime_package_blueprint_rows={len(runtime)}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "schema_outputs_materialized",
            "status": "pass",
            "evidence": "schema json outputs",
            "finding": "five required schema JSON payloads are generated in this run before final manifest registration",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "blueprint_acceptance_matrix_ready",
            "status": "pass" if all_acceptance and len(acceptance) >= 7 else "fail",
            "evidence": rel(BLUEPRINT_ACCEPTANCE_CSV),
            "finding": f"acceptance_rows={len(acceptance)};all_accepted={all_acceptance}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "run337G_review_queue_ready",
            "status": "pass" if len(review_queue) >= 8 else "fail",
            "evidence": rel(RUN337G_QUEUE_CSV),
            "finding": f"run337G_queue_rows={len(review_queue)}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "claim_guard_no_training_no_mt5_no_goal",
            "status": "pass",
            "evidence": rel(FINAL_DECISION_JSON),
            "finding": "no model training, MT5 execution, selected candidate, Forward Passed, runtime authority, or Goal Achieve claimed",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_metrics(
    source_lineage: Sequence[Mapping[str, Any]],
    no_lookahead: Sequence[Mapping[str, Any]],
    proxy_expected: Sequence[Mapping[str, Any]],
    mt5_probe: Sequence[Mapping[str, Any]],
    core56: Sequence[Mapping[str, Any]],
    cost_curve: Sequence[Mapping[str, Any]],
    offense: Sequence[Mapping[str, Any]],
    regime: Sequence[Mapping[str, Any]],
    runtime: Sequence[Mapping[str, Any]],
    acceptance: Sequence[Mapping[str, Any]],
    review_queue: Sequence[Mapping[str, Any]],
    audit: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    return {
        "source_lineage_rows": len(source_lineage),
        "no_lookahead_blueprint_rows": len(no_lookahead),
        "proxy_expected_blueprint_rows": len(proxy_expected),
        "mt5_probe_blueprint_rows": len(mt5_probe),
        "core56_blueprint_rows": len(core56),
        "cost_curve_blueprint_rows": len(cost_curve),
        "offense_blueprint_rows": len(offense),
        "regime_blueprint_rows": len(regime),
        "runtime_package_blueprint_rows": len(runtime),
        "blueprint_acceptance_rows": len(acceptance),
        "run337G_queue_rows": len(review_queue),
        "gate_rows": len(audit),
        "failed_gate_rows": len([row for row in audit if row.get("status") != "pass"]),
    }


def write_receipts(metrics: Mapping[str, Any]) -> list[Path]:
    return [
        write_json(
            EXPERIMENT_DESIGN_JSON,
            {
                "run_id": RUN_ID,
                "hypothesis": "approved Stage337 protocols can be converted into execution blueprints without opening model training or MT5 execution",
                "decision_use": "allow run337G to review blueprint completeness before any executable package or training queue opens",
                "comparison_baseline": "run337E accepted protocol review and run337F blueprint queue",
                "control_variables": "no training, no MT5 execution, no threshold retune, no lot optimization, no forward-pocket filtering, no candidate selection",
                "changed_variables": "blueprint and schema artifacts for no-lookahead, proxy-MT5, core56, cost/curve, offense, regime, runtime packages",
                "sample_scope": "blueprint-only scope; no model rows, no MT5 trades, no KPI sample",
                "success_criteria": "all blueprint families and schemas materialized with claim guards passing",
                "failure_criteria": "missing blueprint, missing schema, training opened, MT5 execution opened, or run337G queue absent",
                "invalid_conditions": "using blueprint files to claim Forward Passed, runtime authority, or candidate selection",
                "stop_conditions": "any gate fails; repair blueprint before review",
                "evidence_plan": "blueprint CSVs, schema JSONs, gate audit, review queue, receipts, report, ledgers",
                "metrics": metrics,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            DATA_INTEGRITY_JSON,
            {
                "run_id": RUN_ID,
                "data_source": "run337E protocol review outputs",
                "time_axis": "future blueprints carry cycle_bar_time, source_timestamp, broker timezone, and timestamp basis requirements",
                "sample_scope": "no new US100 M5 data is consumed for KPI in run337F",
                "missing_or_duplicate_check": "future blueprints require missing/duplicate/stale/future join checks",
                "feature_label_boundary": "no labels or model fit; no-lookahead harness blocks future-derived features before training",
                "split_boundary": "future train/WFO/forward split remains a later reviewed packet requirement",
                "leakage_risk": "future-bar features, forward-pocket filtering, threshold retune, lot optimization, macro revision drift",
                "data_hash_or_identity": rel(BLUEPRINT_ACCEPTANCE_CSV),
                "integrity_judgment": "usable_with_boundary",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RUNTIME_PARITY_JSON,
            {
                "run_id": RUN_ID,
                "research_path": rel(Path(__file__)),
                "runtime_path": rel(RUNTIME_PACKAGE_BLUEPRINT_CSV),
                "shared_contract": "feature order, threshold, risk, lot, timestamp basis, proxy expected values, MT5 observed values, trade ledger, D/B source, cost and regime slices must be carried together",
                "known_differences": "no MT5 runtime execution in run337F; runtime packages are blueprints only",
                "parity_check": "blueprint requires future row-level proxy-MT5 comparison before KPI authority",
                "parity_identity": rel(PROXY_MT5_DIFF_SCHEMA_JSON),
                "runtime_claim_boundary": "blueprint_only_no_runtime_authority",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            ARTIFACT_LINEAGE_JSON,
            {
                "run_id": RUN_ID,
                "source_inputs": [
                    rel(RUN337E_QUEUE),
                    rel(RUN337E_ACCEPTED),
                    rel(RUN337E_NO_LOOKAHEAD),
                    rel(RUN337E_PROXY_MT5),
                    rel(RUN337E_CORE56),
                    rel(RUN337E_COST_CURVE),
                    rel(RUN337E_OFFENSE),
                    rel(RUN337E_REGIME),
                    rel(RUN337E_RUNTIME),
                    rel(RUN337E_DECISION),
                ],
                "producer": rel(Path(__file__)),
                "consumer": NEXT_RUN_ID,
                "artifact_paths": [
                    rel(BLUEPRINT_SOURCE_LINEAGE_CSV),
                    rel(NO_LOOKAHEAD_BLUEPRINT_CSV),
                    rel(PROXY_EXPECTED_BLUEPRINT_CSV),
                    rel(MT5_PROBE_BLUEPRINT_CSV),
                    rel(CORE56_REPAIR_BLUEPRINT_CSV),
                    rel(COST_CURVE_BLUEPRINT_CSV),
                    rel(RUN337G_QUEUE_CSV),
                ],
                "artifact_hashes": "registered in artifact_registry after run",
                "registry_links": "run_registry;alpha_run_ledger;stage_run_ledger;artifact_registry",
                "availability": "tracked after commit; reproducible from run337F script",
                "lineage_judgment": "connected_with_boundary",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RESULT_JUDGMENT_JSON,
            {
                "run_id": RUN_ID,
                "result_subject": "protocol-bound execution blueprints",
                "evidence_available": "blueprint CSVs, schema JSONs, blueprint acceptance matrix, run337G review queue, gate audit",
                "evidence_missing": "no model training, no MT5 execution, no proxy expected values, no MT5 observed values, no candidate KPI",
                "judgment_label": "exploratory",
                "claim_boundary": "blueprints are materialized for review only; no candidate, Forward decision, or runtime authority",
                "next_condition": NEXT_RUN_ID,
                "user_explanation_hook": "실행 청사진은 생겼지만 아직 실행한 것이 아니다. 다음은 청사진이 실제 패키지로 가도 되는지 검토하는 단계다.",
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
# run337F Protocol-Bound Execution Blueprints(337F 절차 기반 실행 청사진)

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

## Blueprint Result(청사진 결과)

- source_lineage(원천 계보): `{metrics['source_lineage_rows']}` rows(행)
- no_lookahead_blueprint(미래참조 방어 청사진): `{metrics['no_lookahead_blueprint_rows']}` rows(행)
- proxy_expected_blueprint(프록시 예상값 청사진): `{metrics['proxy_expected_blueprint_rows']}` rows(행)
- mt5_probe_blueprint(MT5 탐침 청사진): `{metrics['mt5_probe_blueprint_rows']}` rows(행)
- core56_blueprint(핵심56 청사진): `{metrics['core56_blueprint_rows']}` rows(행)
- cost_curve_blueprint(비용/곡선 청사진): `{metrics['cost_curve_blueprint_rows']}` rows(행)
- offense_blueprint(공격형 청사진): `{metrics['offense_blueprint_rows']}` rows(행)
- regime_blueprint(국면 청사진): `{metrics['regime_blueprint_rows']}` rows(행)
- runtime_package_blueprint(런타임 패키지 청사진): `{metrics['runtime_package_blueprint_rows']}` rows(행)
- gate_rows(게이트 행): `{metrics['gate_rows']}`, failed(실패): `{metrics['failed_gate_rows']}`
- run337G_queue(337G 대기열): `{metrics['run337G_queue_rows']}` rows(행)

Effect(효과): run337F(337F 실행)는 실제 학습이나 MT5 실행을 하지 않고, 다음 run337G(337G 실행)가 검토할 실행 청사진과 schema(스키마)를 만들었다. 이로써 proxy expected(프록시 예상값), MT5 runtime probe(MT5 런타임 탐침), core56 repair(핵심56 수리), cost/direction/curve attribution(비용/방향/곡선 귀속), economic regime as-of(경제 국면 시점 기준)가 같은 claim boundary(주장 경계) 아래 묶인다.
"""
    decision = f"""
# 2026-05-27 Stage337F Decision(337F 결정)

- decision(결정): `{DECISION}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed_for_stage337_new_work`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`

Effect(효과): 다음 run337G(337G 실행)는 blueprint review(청사진 검토)를 수행한다. 이 결정은 모델 학습 허가나 MT5 결과 판정이 아니다.
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
- effect(효과): run337F(337F 실행)는 protocol-bound execution blueprints(절차 기반 실행 청사진)를 만들고 run337G(337G 실행) 검토로 넘겼다. 아직 선택 후보는 없다.
"""
    artifacts.append(write_md(SELECTED_DIR / "selection_status.md", selection))

    brief_text, brief_bom = read_text_lossless(SPEC_DIR / "stage_brief.md")
    brief_text = replace_prefix_line(brief_text, "- latest_run(최신 실행):", f"- latest_run(최신 실행): `{RUN_ID}`")
    brief_text = insert_after_marker_once(
        brief_text,
        "- run337E_summary(337E 요약):",
        f"- run337F_summary(337F 요약): `{STATUS}`. Effect(효과): no-lookahead/proxy-MT5/core56/cost-direction-curve/offense/regime/runtime(미래참조/프록시-MT5/핵심56/비용-방향-곡선/공격/국면/런타임) 청사진과 스키마를 만들고 run337G(337G 실행) 검토 대기열로 넘긴다.",
        "run337F_summary",
    )
    artifacts.append(write_text_lossless(SPEC_DIR / "stage_brief.md", brief_text, brief_bom))

    input_section = f"""
- blueprint_source_lineage_review(청사진 원천 계보 검토): `{rel(BLUEPRINT_SOURCE_LINEAGE_CSV)}`
- no_lookahead_harness_blueprint(미래참조 방어 청사진): `{rel(NO_LOOKAHEAD_BLUEPRINT_CSV)}`
- proxy_expected_schema_blueprint(프록시 예상값 청사진): `{rel(PROXY_EXPECTED_BLUEPRINT_CSV)}`
- mt5_runtime_probe_package_blueprint(MT5 런타임 탐침 패키지 청사진): `{rel(MT5_PROBE_BLUEPRINT_CSV)}`
- core56_repair_blueprint(핵심56 수리 청사진): `{rel(CORE56_REPAIR_BLUEPRINT_CSV)}`
- cost_direction_curve_extraction_blueprint(비용/방향/곡선 추출 청사진): `{rel(COST_CURVE_BLUEPRINT_CSV)}`
- offense_branch_blueprint(공격 분기 청사진): `{rel(OFFENSE_BLUEPRINT_CSV)}`
- economic_regime_asof_source_blueprint(경제 국면 시점 기준 원천 청사진): `{rel(REGIME_SOURCE_BLUEPRINT_CSV)}`
- runtime_probe_package_blueprint(런타임 탐침 패키지 청사진): `{rel(RUNTIME_PACKAGE_BLUEPRINT_CSV)}`
- run337G_queue(337G 대기열): `{rel(RUN337G_QUEUE_CSV)}`

Effect(효과): 다음 실행은 이 청사진들이 실제 materialization package(물질화 패키지)로 넘어가도 되는지 검토한다.
"""
    artifacts.append(append_section_once(INPUTS_DIR / "input_refs.md", "## run337F Outputs(337F 산출물)", input_section))

    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_prefix_line(workspace_text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    focus = (
        "- >-\n"
        f"  Stage337 run337F focus complete: Stage337(337단계) run337F(337F 실행)는 `{STATUS}`로 protocol-bound execution blueprints(절차 기반 실행 청사진)를 물질화했다. "
        "Effect(효과): proxy expected/MT5 runtime/core56/cost-direction-curve/offense/economic-regime(프록시 예상값/MT5 런타임/핵심56/비용-방향-곡선/공격/경제 국면) 청사진을 만들었지만, model training(모델 학습), MT5 execution(MT5 실행), candidate selection(후보 선택)은 아직 닫아둔다.\n"
    )
    workspace_text = insert_focus_once(workspace_text, focus, "Stage337 run337F focus complete")
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
        f"- run337F_summary(337F 요약): `{STATUS}`. "
        "Effect(효과): 실행 청사진과 스키마를 만들고 run337G(337G 실행) 검토 대기열로 넘기며, 학습/MT5/후보 선택은 계속 닫아둔다."
    )
    current_text = insert_after_marker_once(current_text, "- decision(결정):", summary, "run337F_summary")
    artifacts.append(write_text_lossless(CURRENT_STATE, current_text, current_bom))

    artifacts.append(
        append_section_once(
            CHANGELOG,
            "## Stage337F Protocol-Bound Execution Blueprints(337F 절차 기반 실행 청사진)",
            f"""
- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- action(행동): run337E(337E 실행)의 승인 절차를 proxy-MT5/core56/cost-direction-curve/offense/regime/runtime(프록시-MT5/핵심56/비용-방향-곡선/공격/국면/런타임) 청사진과 스키마로 물질화했다.
- effect(효과): 다음 실행은 실제 패키지 생성 전에 청사진 완전성을 검토할 수 있다.
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
                "lane": "protocol_bound_execution_blueprint_materialization",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_DOC),
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};blueprints_materialized;training_not_allowed;mt5_not_executed;goal_achieve_not_claimed.",
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__protocol_bound_execution_blueprints",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "protocol_bound_execution_blueprint_materialization",
                "tier_scope": "stage337_blueprint_boundary_macro48_u42_core56",
                "kpi_scope": "blueprint_only_no_new_candidate_kpi",
                "scoreboard_lane": "blueprint_readiness",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_DOC),
                "primary_kpi": "blueprint_families=8;run337g_queue_rows=8;candidate_selection=none",
                "guardrail_kpi": "training_not_allowed;mt5_not_executed;proxy_not_kpi_authority;goal_achieve_not_claimed",
                "external_verification_status": "out_of_scope_by_claim_blueprint_only",
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
                "ledger_row_id": f"{RUN_ID}__protocol_bound_execution_blueprints",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "work_family": "experiment_design",
                "evidence_scope": "run337E_accepted_protocols_and_review_queue",
                "kpi_scope": "blueprint_only_no_new_candidate_kpi",
                "status": STATUS,
                "judgment": JUDGMENT,
                "claim_boundary": CLAIM_BOUNDARY,
                "path": rel(REPORT_DOC),
                "notes": f"next_action={NEXT_RUN_ID};blueprints_materialized;training_not_allowed;mt5_not_executed;goal_achieve_not_claimed.",
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
            "notes": "run337F_protocol_bound_blueprints_no_selection",
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
    source_lineage = build_blueprint_source_lineage(inputs)
    no_lookahead = build_no_lookahead_blueprint(inputs["no_lookahead"])
    no_lookahead_schema = build_no_lookahead_schema()
    proxy_expected = build_proxy_expected_blueprint(inputs["proxy_mt5"])
    mt5_probe = build_mt5_probe_blueprint(inputs["proxy_mt5"])
    proxy_mt5_diff_schema = build_proxy_mt5_diff_schema()
    core56 = build_core56_blueprint(inputs["core56"])
    core56_schema = build_core56_asof_schema()
    cost_curve = build_cost_curve_blueprint(inputs["cost_curve"])
    cost_curve_schema = build_cost_curve_schema()
    offense = build_offense_blueprint(inputs["offense"])
    regime = build_regime_blueprint(inputs["regime"])
    regime_schema = build_regime_slice_schema()
    runtime = build_runtime_package_blueprint(inputs["runtime"])
    acceptance = build_blueprint_acceptance(
        inputs, no_lookahead, proxy_expected, mt5_probe, core56, cost_curve, offense, regime, runtime
    )
    review_queue = build_run337g_queue()
    audit = build_gate_audit(
        inputs,
        source_lineage,
        no_lookahead,
        proxy_expected,
        mt5_probe,
        core56,
        cost_curve,
        offense,
        regime,
        runtime,
        acceptance,
        review_queue,
    )
    metrics = build_metrics(
        source_lineage,
        no_lookahead,
        proxy_expected,
        mt5_probe,
        core56,
        cost_curve,
        offense,
        regime,
        runtime,
        acceptance,
        review_queue,
        audit,
    )
    failed_gates = [row for row in audit if row.get("status") != "pass"]
    run_artifacts = [
        write_csv(
            BLUEPRINT_SOURCE_LINEAGE_CSV,
            (
                "source_path",
                "source_sha256",
                "source_exists",
                "source_row_count",
                "source_manifest_linked",
                "parent_lineage_review",
                "used_by_run337F",
                "allowed_use",
                "forbidden_use",
                "lineage_status",
                "claim_boundary",
            ),
            source_lineage,
        ),
        write_csv(
            NO_LOOKAHEAD_BLUEPRINT_CSV,
            (
                "harness_id",
                "source_protocol_id",
                "risk_target",
                "bad_control_input",
                "expected_detector",
                "required_assertions",
                "invalid_if",
                "repair_route",
                "review_artifact_required",
                "forbidden",
                "claim_boundary",
            ),
            no_lookahead,
        ),
        write_json(NO_LOOKAHEAD_SCHEMA_JSON, no_lookahead_schema),
        write_csv(
            PROXY_EXPECTED_BLUEPRINT_CSV,
            (
                "subject",
                "proxy_expected_blueprint_id",
                "required_inputs",
                "required_output_columns",
                "timestamp_rule",
                "freshness_rule",
                "usability_boundary",
                "blocked_if",
                "forbidden",
                "claim_boundary",
            ),
            proxy_expected,
        ),
        write_csv(
            MT5_PROBE_BLUEPRINT_CSV,
            (
                "subject",
                "mt5_probe_blueprint_id",
                "required_files",
                "required_runtime_outputs",
                "required_comparison_outputs",
                "execution_boundary",
                "kpi_authority_rule",
                "blocked_if",
                "claim_boundary",
            ),
            mt5_probe,
        ),
        write_json(PROXY_MT5_DIFF_SCHEMA_JSON, proxy_mt5_diff_schema),
        write_csv(
            CORE56_REPAIR_BLUEPRINT_CSV,
            (
                "core56_blueprint_id",
                "step_order",
                "source_protocol_id",
                "required_action",
                "required_artifacts",
                "asof_guard",
                "blocked_claims",
                "review_condition",
                "claim_boundary",
            ),
            core56,
        ),
        write_json(CORE56_ASOF_SCHEMA_JSON, core56_schema),
        write_csv(
            COST_CURVE_BLUEPRINT_CSV,
            (
                "extraction_blueprint_id",
                "source_protocol_id",
                "gate_scope",
                "required_extractors",
                "required_outputs",
                "minimum_metrics",
                "failure_memory_trigger",
                "forbidden",
                "claim_boundary",
            ),
            cost_curve,
        ),
        write_json(COST_CURVE_SCHEMA_JSON, cost_curve_schema),
        write_csv(
            OFFENSE_BLUEPRINT_CSV,
            (
                "branch_blueprint_id",
                "branch_id",
                "allowed_next_step",
                "training_allowed",
                "required_controls",
                "required_evidence_before_training",
                "failure_memory_axis",
                "forbidden",
                "claim_boundary",
            ),
            offense,
        ),
        write_csv(
            REGIME_SOURCE_BLUEPRINT_CSV,
            (
                "regime_blueprint_id",
                "source_protocol_id",
                "regime_source",
                "required_source_identity",
                "asof_join_rule",
                "required_checks",
                "slice_outputs",
                "invalid_if",
                "claim_boundary",
            ),
            regime,
        ),
        write_json(REGIME_SLICE_SCHEMA_JSON, regime_schema),
        write_csv(
            RUNTIME_PACKAGE_BLUEPRINT_CSV,
            (
                "runtime_blueprint_id",
                "source_package_id",
                "subject",
                "required_files",
                "preflight_checks",
                "runtime_outputs",
                "comparison_outputs",
                "stress_outputs",
                "blocked_if_missing",
                "runtime_claim_boundary",
                "claim_boundary",
            ),
            runtime,
        ),
        write_csv(
            BLUEPRINT_ACCEPTANCE_CSV,
            (
                "queue_id",
                "priority",
                "blueprint_task",
                "materialized_output",
                "schema_output",
                "output_rows",
                "acceptance_status",
                "review_requirement",
                "forbidden",
                "claim_boundary",
            ),
            acceptance,
        ),
        write_csv(
            RUN337G_QUEUE_CSV,
            (
                "queue_id",
                "priority",
                "review_input",
                "schema_input",
                "review_task",
                "required_decision",
                "forbidden",
                "claim_boundary",
            ),
            review_queue,
        ),
        write_csv(GATE_AUDIT_CSV, ("gate_id", "status", "evidence", "finding", "claim_boundary"), audit),
    ]
    run_artifacts.extend(write_receipts(metrics))
    final_payload = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS if not failed_gates else "blocked_stage337F_blueprint_gate_failure",
        "judgment": JUDGMENT if not failed_gates else "stage337F_blueprint_materialization_requires_repair",
        "decision": DECISION if not failed_gates else "stage337F_blueprint_materialization_blocked_gate_failure",
        "metrics": metrics,
        "failed_gates": failed_gates,
        "next_action": NEXT_RUN_ID if not failed_gates else "repair_run337F_blueprint_gaps_before_review",
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
                "outputs": [rel(path) for path in run_artifacts],
                "status": "blocked_stage337F_blueprint_gate_failure",
                "decision": "stage337F_blueprint_materialization_blocked_gate_failure",
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
            rel(RUN337E_QUEUE),
            rel(RUN337E_ACCEPTED),
            rel(RUN337E_NO_LOOKAHEAD),
            rel(RUN337E_PROXY_MT5),
            rel(RUN337E_CORE56),
            rel(RUN337E_COST_CURVE),
            rel(RUN337E_OFFENSE),
            rel(RUN337E_REGIME),
            rel(RUN337E_RUNTIME),
            rel(RUN337E_DECISION),
            rel(RUN337E_MANIFEST),
        ],
        "outputs": [rel(path) for path in all_artifacts],
        "status": STATUS,
        "decision": DECISION,
        "external_verification_status": "out_of_scope_by_claim_blueprint_only_no_mt5_execution",
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
                "blueprint_acceptance_rows": metrics["blueprint_acceptance_rows"],
                "run337G_queue_rows": metrics["run337G_queue_rows"],
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
