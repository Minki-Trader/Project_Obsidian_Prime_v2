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
RUN_NUMBER = "run337G"
RUN_ID = "run337G_review_protocol_bound_execution_blueprints_v1"
PARENT_RUN_ID = "run337F_materialize_protocol_bound_execution_blueprints_v1"
NEXT_RUN_ID = "run337H_materialize_reviewed_execution_packages_v1"
STATUS = "completed_protocol_bound_execution_blueprint_review_accepts_package_queue_no_training"
JUDGMENT = "stage337G_blueprints_reviewed_accept_package_materialization_no_selection"
DECISION = "stage337G_blueprints_reviewed_open_run337H_packages_no_training_no_mt5_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage337G_blueprint_review_no_model_training_no_mt5_execution_"
    "no_threshold_retuning_no_lot_optimization_no_forward_pocket_filtering_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
RUN337F_DIR = STAGE_DIR / "02_runs" / "run337F"
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
DECISION_DOC = DOCS / "decisions" / "2026-05-27_stage337G_review_protocol_bound_execution_blueprints.md"
REPORT_DOC = REVIEWS_DIR / "run337G_review_protocol_bound_execution_blueprints.md"

RUN337F_QUEUE = RUN337F_DIR / "run337G_blueprint_review_queue.csv"
RUN337F_LINEAGE = RUN337F_DIR / "blueprint_source_lineage_review.csv"
RUN337F_NO_LOOKAHEAD = RUN337F_DIR / "no_lookahead_harness_blueprint.csv"
RUN337F_NO_LOOKAHEAD_SCHEMA = RUN337F_DIR / "no_lookahead_harness_schema.json"
RUN337F_PROXY_EXPECTED = RUN337F_DIR / "proxy_expected_schema_blueprint.csv"
RUN337F_MT5_PROBE = RUN337F_DIR / "mt5_runtime_probe_package_blueprint.csv"
RUN337F_PROXY_DIFF_SCHEMA = RUN337F_DIR / "proxy_mt5_difference_schema.json"
RUN337F_CORE56 = RUN337F_DIR / "core56_repair_blueprint.csv"
RUN337F_CORE56_SCHEMA = RUN337F_DIR / "core56_asof_join_schema.json"
RUN337F_COST_CURVE = RUN337F_DIR / "cost_direction_curve_extraction_blueprint.csv"
RUN337F_COST_CURVE_SCHEMA = RUN337F_DIR / "cost_direction_curve_report_schema.json"
RUN337F_OFFENSE = RUN337F_DIR / "offense_branch_blueprint.csv"
RUN337F_REGIME = RUN337F_DIR / "economic_regime_asof_source_blueprint.csv"
RUN337F_REGIME_SCHEMA = RUN337F_DIR / "economic_regime_slice_schema.json"
RUN337F_RUNTIME = RUN337F_DIR / "runtime_probe_package_blueprint.csv"
RUN337F_ACCEPTANCE = RUN337F_DIR / "blueprint_acceptance_matrix.csv"
RUN337F_GATE_AUDIT = RUN337F_DIR / "required_gate_coverage_audit.csv"
RUN337F_DECISION = RUN337F_DIR / "final_protocol_bound_execution_blueprints_decision.json"
RUN337F_MANIFEST = RUN337F_DIR / "run_manifest.json"

SOURCE_LINEAGE_REVIEW_CSV = RUN_DIR / "blueprint_review_source_lineage.csv"
NO_LOOKAHEAD_REVIEW_CSV = RUN_DIR / "no_lookahead_harness_blueprint_review.csv"
PROXY_MT5_REVIEW_CSV = RUN_DIR / "proxy_mt5_blueprint_review.csv"
CORE56_REVIEW_CSV = RUN_DIR / "core56_repair_blueprint_review.csv"
COST_CURVE_REVIEW_CSV = RUN_DIR / "cost_direction_curve_extraction_blueprint_review.csv"
OFFENSE_REVIEW_CSV = RUN_DIR / "offense_branch_blueprint_review.csv"
REGIME_REVIEW_CSV = RUN_DIR / "economic_regime_asof_blueprint_review.csv"
RUNTIME_REVIEW_CSV = RUN_DIR / "runtime_probe_package_blueprint_review.csv"
CLAIM_REVIEW_CSV = RUN_DIR / "claim_boundary_review.csv"
ACCEPTED_BLUEPRINT_QUEUE_CSV = RUN_DIR / "accepted_blueprints_for_package_queue.csv"
REPAIR_GAP_QUEUE_CSV = RUN_DIR / "repair_blueprint_gap_queue.csv"
RUN337H_QUEUE_CSV = RUN_DIR / "run337H_package_materialization_queue.csv"
GATE_AUDIT_CSV = RUN_DIR / "required_gate_coverage_audit.csv"

EXPERIMENT_DESIGN_JSON = RUN_DIR / "experiment_design_receipt.json"
DATA_INTEGRITY_JSON = RUN_DIR / "data_integrity_receipt.json"
RUNTIME_PARITY_JSON = RUN_DIR / "runtime_parity_receipt.json"
ARTIFACT_LINEAGE_JSON = RUN_DIR / "artifact_lineage_receipt.json"
RESULT_JUDGMENT_JSON = RUN_DIR / "result_judgment_receipt.json"
FINAL_DECISION_JSON = RUN_DIR / "final_review_protocol_bound_execution_blueprints_decision.json"
RUN_MANIFEST_JSON = RUN_DIR / "run_manifest.json"


SOURCE_INPUTS: tuple[Path, ...] = (
    RUN337F_QUEUE,
    RUN337F_LINEAGE,
    RUN337F_NO_LOOKAHEAD,
    RUN337F_NO_LOOKAHEAD_SCHEMA,
    RUN337F_PROXY_EXPECTED,
    RUN337F_MT5_PROBE,
    RUN337F_PROXY_DIFF_SCHEMA,
    RUN337F_CORE56,
    RUN337F_CORE56_SCHEMA,
    RUN337F_COST_CURVE,
    RUN337F_COST_CURVE_SCHEMA,
    RUN337F_OFFENSE,
    RUN337F_REGIME,
    RUN337F_REGIME_SCHEMA,
    RUN337F_RUNTIME,
    RUN337F_ACCEPTANCE,
    RUN337F_GATE_AUDIT,
    RUN337F_DECISION,
    RUN337F_MANIFEST,
)


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


def contains_all(text: str, needles: Sequence[str]) -> bool:
    lowered = text.lower()
    return all(needle.lower() in lowered for needle in needles)


def row_count_or_keys(path: Path) -> str:
    if not path_exists(path):
        return ""
    if path.suffix.lower() == ".csv":
        return str(len(read_csv(path)))
    if path.suffix.lower() == ".json":
        return ";".join(sorted(read_json(path).keys()))
    return ""


def load_inputs() -> dict[str, Any]:
    return {
        "queue": read_csv(RUN337F_QUEUE),
        "source_lineage": read_csv(RUN337F_LINEAGE),
        "no_lookahead": read_csv(RUN337F_NO_LOOKAHEAD),
        "no_lookahead_schema": read_json(RUN337F_NO_LOOKAHEAD_SCHEMA),
        "proxy_expected": read_csv(RUN337F_PROXY_EXPECTED),
        "mt5_probe": read_csv(RUN337F_MT5_PROBE),
        "proxy_diff_schema": read_json(RUN337F_PROXY_DIFF_SCHEMA),
        "core56": read_csv(RUN337F_CORE56),
        "core56_schema": read_json(RUN337F_CORE56_SCHEMA),
        "cost_curve": read_csv(RUN337F_COST_CURVE),
        "cost_curve_schema": read_json(RUN337F_COST_CURVE_SCHEMA),
        "offense": read_csv(RUN337F_OFFENSE),
        "regime": read_csv(RUN337F_REGIME),
        "regime_schema": read_json(RUN337F_REGIME_SCHEMA),
        "runtime": read_csv(RUN337F_RUNTIME),
        "acceptance": read_csv(RUN337F_ACCEPTANCE),
        "gate_audit": read_csv(RUN337F_GATE_AUDIT),
        "decision": read_json(RUN337F_DECISION),
        "manifest": read_json(RUN337F_MANIFEST),
    }


def review_status(ok: bool) -> str:
    return "accepted_for_run337H_package_materialization" if ok else "repair_required_before_run337H"


def build_source_lineage_review() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in SOURCE_INPUTS:
        exists = path_exists(path)
        rows.append(
            {
                "source_path": rel(path),
                "exists": exists,
                "sha256": sha256_file_lf_normalized(path) if exists else "",
                "row_count_or_keys": row_count_or_keys(path) if exists else "",
                "review_status": "accepted_for_review" if exists else "missing_required_input",
                "allowed_use": "run337G blueprint review and run337H package materialization queue only",
                "forbidden_use": "model training, MT5 execution, candidate selection, Forward Passed, runtime authority, Goal Achieve",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def review_no_lookahead(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = inputs["no_lookahead"]
    schema = inputs["no_lookahead_schema"]
    required_bad_controls = ["future_bar", "forward_pocket_filter", "threshold_retune", "lot_optimization", "timestamp_basis"]
    present_controls = ";".join(row.get("source_protocol_id", "") for row in rows)
    schema_controls = schema.get("bad_control_families", [])
    checks = [
        ("row_count", len(rows) >= 5),
        ("schema_must_fail_to_pass", schema.get("must_fail_to_pass") is True),
        ("bad_control_families", all(item in schema_controls and item in present_controls for item in required_bad_controls)),
        (
            "required_assertions",
            all(contains_all(row.get("required_assertions", ""), ["rejected", "repair", "no candidate", "no Forward"]) for row in rows),
        ),
        ("forbidden_selection", all("selection" in row.get("forbidden", "").lower() for row in rows)),
    ]
    ok = all(value for _, value in checks)
    return [
        {
            "review_id": "no_lookahead_harness_completeness",
            "source_artifact": rel(RUN337F_NO_LOOKAHEAD),
            "schema_artifact": rel(RUN337F_NO_LOOKAHEAD_SCHEMA),
            "review_scope": "future-bar, forward-pocket, threshold, lot, timestamp-basis canaries",
            "checks": ";".join(f"{name}={value}" for name, value in checks),
            "review_status": review_status(ok),
            "finding": f"harness_rows={len(rows)};bad_controls={','.join(required_bad_controls)}",
            "next_use": "run337H can materialize bad-control harness package if accepted",
            "blocked_if": "any canary lacks must-fail detector, repair route, or selection claim guard",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def review_proxy_mt5(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    proxy = inputs["proxy_expected"]
    mt5 = inputs["mt5_probe"]
    diff_schema = inputs["proxy_diff_schema"]
    proxy_subjects = {row.get("subject", "") for row in proxy}
    mt5_subjects = {row.get("subject", "") for row in mt5}
    required_proxy_columns = [
        "candidate_id",
        "cycle_bar_time",
        "score",
        "decision",
        "direction",
        "D_source",
        "B_source",
        "D_plus_B",
        "threshold_id",
        "feature_hash",
        "model_hash",
        "timestamp_basis",
        "source_row_hash",
    ]
    required_diff_columns = [
        "candidate_id",
        "subject",
        "cycle_bar_time",
        "proxy_decision",
        "mt5_decision",
        "decision_match",
        "direction_match",
        "D_source_match",
        "B_source_match",
        "score_abs_diff",
        "timestamp_basis_status",
        "usability_label",
    ]
    required_mt5_files = ["EA", "include module hash", "ONNX", "adapter manifest", "feature order", "set file", "tester ini", "handoff snapshot"]
    checks = [
        ("proxy_subject_rows", len(proxy) >= 5),
        ("mt5_subject_rows", len(mt5) >= 5),
        ("subject_match", proxy_subjects == mt5_subjects and len(proxy_subjects) >= 5),
        ("proxy_required_columns", all(contains_all(row.get("required_output_columns", ""), required_proxy_columns) for row in proxy)),
        ("mt5_required_files", all(contains_all(row.get("required_files", ""), required_mt5_files) for row in mt5)),
        ("diff_schema_required_columns", all(column in diff_schema.get("required_columns", []) for column in required_diff_columns)),
        ("kpi_authority_blocked", "not_authoritative" in str(diff_schema.get("kpi_authority", ""))),
        ("fresh_mt5_required", all("no MT5 execution until reviewed" in row.get("execution_boundary", "") for row in mt5)),
    ]
    ok = all(value for _, value in checks)
    return [
        {
            "review_id": "proxy_mt5_fresh_probe_blueprint_completeness",
            "source_artifact": f"{rel(RUN337F_PROXY_EXPECTED)};{rel(RUN337F_MT5_PROBE)}",
            "schema_artifact": rel(RUN337F_PROXY_DIFF_SCHEMA),
            "review_scope": "fresh proxy expected values, MT5 probe package, row-level difference, usability decision",
            "checks": ";".join(f"{name}={value}" for name, value in checks),
            "review_status": review_status(ok),
            "finding": f"subjects={','.join(sorted(proxy_subjects))};diff_required_columns={len(required_diff_columns)}",
            "next_use": "run337H can materialize proxy expected and MT5 runtime probe package specs if accepted",
            "blocked_if": "proxy/MT5 subject mismatch, missing identity columns, or KPI authority claim without MT5 trade ledger",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def review_core56(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = inputs["core56"]
    schema = inputs["core56_schema"]
    required_artifacts = [
        "source_inventory.csv",
        "asof_join_contract.json",
        "feature_handoff_snapshot.csv",
        "proxy_expected_values.csv",
        "fresh_mt5_probe_package.csv",
    ]
    required_schema_columns = ["target_cycle_bar_time", "source_timestamp", "source_sha256", "future_join_flag"]
    checks = [
        ("row_count", len(rows) >= 5),
        ("required_artifacts", all(contains_all(row.get("required_artifacts", ""), required_artifacts) for row in rows)),
        ("full_family_block", all("full-family" in row.get("blocked_claims", "") for row in rows)),
        ("asof_guard", all("must not read later" in row.get("asof_guard", "") for row in rows)),
        ("schema_columns", all(column in schema.get("required_columns", []) for column in required_schema_columns)),
        ("schema_future_invalid", "future_join_flag=true" in schema.get("invalid_if", "")),
    ]
    ok = all(value for _, value in checks)
    return [
        {
            "review_id": "core56_repair_blueprint_completeness",
            "source_artifact": rel(RUN337F_CORE56),
            "schema_artifact": rel(RUN337F_CORE56_SCHEMA),
            "review_scope": "core56 source inventory, as-of join, handoff snapshot, proxy expected, fresh MT5 package",
            "checks": ";".join(f"{name}={value}" for name, value in checks),
            "review_status": review_status(ok),
            "finding": f"core56_rows={len(rows)};schema_columns={len(schema.get('required_columns', []))}",
            "next_use": "run337H can materialize core56 repair package specs if accepted",
            "blocked_if": "full-family claim opens before as-of repair and fresh runtime probe package",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def review_cost_curve(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = inputs["cost_curve"]
    schema = inputs["cost_curve_schema"]
    required_reports = [
        "cost_stress_report",
        "spread_slippage_stress_report",
        "long_short_attribution",
        "D_B_source_attribution",
        "curve_pocket_report",
        "lot_normalized_report",
        "regime_slice_report",
    ]
    required_outputs = [f"{name}.csv" for name in required_reports]
    required_metrics = ["net", "PF", "expectancy", "maxDD", "recovery", "trades_per_day", "worst_pocket", "underwater_stretch"]
    reports = schema.get("reports", {})
    checks = [
        ("row_count", len(rows) >= 5),
        ("required_outputs", all(contains_all(row.get("required_outputs", ""), required_outputs) for row in rows)),
        ("minimum_metrics", all(contains_all(row.get("minimum_metrics", ""), required_metrics) for row in rows)),
        ("schema_reports", all(name in reports for name in required_reports)),
        ("no_retune_forbidden", all(contains_all(row.get("forbidden", ""), ["threshold retune", "lot optimization", "forward-pocket"]) for row in rows)),
    ]
    ok = all(value for _, value in checks)
    return [
        {
            "review_id": "cost_direction_curve_extraction_blueprint_completeness",
            "source_artifact": rel(RUN337F_COST_CURVE),
            "schema_artifact": rel(RUN337F_COST_CURVE_SCHEMA),
            "review_scope": "cost stress, spread/slippage, D/B, long/short, curve pocket, lot-normalized, regime reports",
            "checks": ";".join(f"{name}={value}" for name, value in checks),
            "review_status": review_status(ok),
            "finding": f"cost_curve_rows={len(rows)};schema_reports={len(reports)}",
            "next_use": "run337H can materialize cost/direction/curve extraction package specs if accepted",
            "blocked_if": "any report family is absent while net/PF/DD/curve claims are made",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def review_offense(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = inputs["offense"]
    controls = ["no-lookahead harness", "fixed threshold", "fixed risk/lot", "no forward-pocket"]
    checks = [
        ("row_count", len(rows) >= 4),
        ("training_closed", all(row.get("training_allowed") == "false" for row in rows)),
        ("required_controls", all(contains_all(row.get("required_controls", ""), controls) for row in rows)),
        ("evidence_before_training", all("run337G blueprint review" in row.get("required_evidence_before_training", "") for row in rows)),
        ("forbidden_claims", all(contains_all(row.get("forbidden", ""), ["training", "candidate", "runtime authority", "Goal Achieve"]) for row in rows)),
    ]
    ok = all(value for _, value in checks)
    return [
        {
            "review_id": "offense_branch_blueprint_training_boundary",
            "source_artifact": rel(RUN337F_OFFENSE),
            "schema_artifact": "",
            "review_scope": "offense branches remain predeclared, training-closed, and guard-bound",
            "checks": ";".join(f"{name}={value}" for name, value in checks),
            "review_status": review_status(ok),
            "finding": f"offense_rows={len(rows)};training_allowed_values={','.join(sorted({row.get('training_allowed', '') for row in rows}))}",
            "next_use": "run337H can materialize offense thesis packages only, not train models",
            "blocked_if": "any branch opens training or candidate selection without reviewed controls",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def review_regime(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = inputs["regime"]
    schema = inputs["regime_schema"]
    required_families = ["VIX", "USD", "rate", "ADX", "volatility", "session", "hour", "month"]
    required_columns = ["source_timestamp", "asof_status", "session", "hour", "month", "volatility", "ADX", "VIX", "USD", "rate"]
    checks = [
        ("row_count", len(rows) >= 6),
        ("source_identity", all(contains_all(row.get("required_source_identity", ""), ["source_timestamp", "source_sha256", "timezone", "revision_policy"]) for row in rows)),
        ("asof_join_rule", all("source_timestamp <= target_cycle_bar_time" in row.get("asof_join_rule", "") for row in rows)),
        ("required_checks", all(contains_all(row.get("required_checks", ""), ["missing", "duplicate", "stale", "revision", "timezone"]) for row in rows)),
        ("schema_slice_families", all(item in schema.get("slice_families", []) for item in required_families)),
        ("schema_columns", all(column in schema.get("required_columns", []) for column in required_columns)),
    ]
    ok = all(value for _, value in checks)
    return [
        {
            "review_id": "economic_regime_asof_blueprint_completeness",
            "source_artifact": rel(RUN337F_REGIME),
            "schema_artifact": rel(RUN337F_REGIME_SCHEMA),
            "review_scope": "VIX, USD, rate, ADX, volatility, session, hour, month as-of slices",
            "checks": ";".join(f"{name}={value}" for name, value in checks),
            "review_status": review_status(ok),
            "finding": f"regime_rows={len(rows)};slice_families={','.join(schema.get('slice_families', []))}",
            "next_use": "run337H can materialize economic regime as-of join package specs if accepted",
            "blocked_if": "future or revised macro/source value enters a forward explanation",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def review_runtime(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = inputs["runtime"]
    required_files = ["EA", "include module hash", "model/ONNX", "adapter manifest", "feature order", "set file", "tester ini", "handoff snapshot"]
    preflight = ["feature order hash", "threshold identity", "risk identity", "lot identity", "symbol/timeframe", "broker session", "data latest timestamp"]
    runtime_outputs = ["Strategy Tester report", "terminal log", "trade ledger", "telemetry", "tester settings identity"]
    stress_outputs = ["cost stress", "spread/slippage stress", "lot-normalized", "D/B attribution", "long/short", "regime slices", "curve pockets"]
    checks = [
        ("row_count", len(rows) >= 5),
        ("required_files", all(contains_all(row.get("required_files", ""), required_files) for row in rows)),
        ("preflight_checks", all(contains_all(row.get("preflight_checks", ""), preflight) for row in rows)),
        ("runtime_outputs", all(contains_all(row.get("runtime_outputs", ""), runtime_outputs) for row in rows)),
        ("stress_outputs", all(contains_all(row.get("stress_outputs", ""), stress_outputs) for row in rows)),
        ("runtime_authority_blocked", all("no_runtime_authority" in row.get("runtime_claim_boundary", "") for row in rows)),
    ]
    ok = all(value for _, value in checks)
    return [
        {
            "review_id": "runtime_probe_package_blueprint_completeness",
            "source_artifact": rel(RUN337F_RUNTIME),
            "schema_artifact": "",
            "review_scope": "runtime package preflight, MT5 outputs, comparison outputs, stress outputs, blocker criteria",
            "checks": ";".join(f"{name}={value}" for name, value in checks),
            "review_status": review_status(ok),
            "finding": f"runtime_rows={len(rows)};subjects={','.join(sorted({row.get('subject', '') for row in rows}))}",
            "next_use": "run337H can materialize runtime probe package specs if accepted; no MT5 execution yet",
            "blocked_if": "runtime package lacks preflight identity, tester output, trade ledger, or blocker criteria",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def review_claim_boundary(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    acceptance = inputs["acceptance"]
    gates = inputs["gate_audit"]
    decision = inputs["decision"]
    manifest = inputs["manifest"]
    checks = [
        ("run337F_acceptance_all_accepted", all(row.get("acceptance_status") == "accepted_for_review" for row in acceptance)),
        ("run337F_gates_all_pass", all(row.get("status") == "pass" for row in gates)),
        ("selected_candidate_none", decision.get("selected_candidate") == "none"),
        ("forward_passed_not_claimed", decision.get("forward_passed") == "not_claimed"),
        ("forward_failed_not_claimed", str(decision.get("forward_failed", "")).startswith("not_claimed")),
        ("runtime_authority_not_claimed", decision.get("runtime_authority") == "not_claimed"),
        ("goal_achieve_not_claimed", decision.get("goal_achieve") == "not_claimed"),
        ("model_training_not_run", decision.get("model_training") == "not_run"),
        ("mt5_execution_not_run", decision.get("mt5_execution") == "not_run"),
        ("manifest_points_to_run337G", manifest.get("next_action") == RUN_ID),
    ]
    ok = all(value for _, value in checks)
    return [
        {
            "review_id": "claim_boundary_review",
            "source_artifact": f"{rel(RUN337F_ACCEPTANCE)};{rel(RUN337F_GATE_AUDIT)};{rel(RUN337F_DECISION)};{rel(RUN337F_MANIFEST)}",
            "schema_artifact": "",
            "review_scope": "claim guard, no training, no MT5 execution, no selection, no Forward decision, no runtime authority",
            "checks": ";".join(f"{name}={value}" for name, value in checks),
            "review_status": review_status(ok),
            "finding": "run337F remains blueprint-only and review-only; no operating or forward claim was promoted",
            "next_use": "run337H may materialize package specs if accepted",
            "blocked_if": "any candidate, Forward, runtime authority, or Goal Achieve claim appears",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_accepted_queue(review_sets: Mapping[str, Sequence[Mapping[str, Any]]]) -> list[dict[str, Any]]:
    package_map = {
        "no_lookahead": ("materialize_no_lookahead_canary_harness_package", "bad control harness package specs"),
        "proxy_mt5": ("materialize_proxy_expected_and_mt5_probe_package_specs", "proxy expected plus fresh MT5 package specs"),
        "core56": ("materialize_core56_asof_repair_package_specs", "core56 as-of repair package specs"),
        "cost_curve": ("materialize_cost_direction_curve_extraction_package_specs", "cost/direction/curve extraction package specs"),
        "offense": ("materialize_offense_branch_thesis_package_specs", "offense thesis package specs without training"),
        "regime": ("materialize_economic_regime_asof_join_package_specs", "economic regime as-of join package specs"),
        "runtime": ("materialize_runtime_probe_package_specs", "runtime probe package specs without MT5 execution"),
        "claim_boundary": ("materialize_claim_guard_and_blocker_package_specs", "claim guard and blocker package specs"),
    }
    rows: list[dict[str, Any]] = []
    for family, review_rows in review_sets.items():
        accepted = all(str(row.get("review_status", "")).startswith("accepted") for row in review_rows)
        next_task, package_scope = package_map[family]
        rows.append(
            {
                "blueprint_family": family,
                "accepted_rows": sum(1 for row in review_rows if str(row.get("review_status", "")).startswith("accepted")),
                "total_rows": len(review_rows),
                "queue_status": "accepted_for_run337H_package_materialization" if accepted else "blocked_for_repair",
                "next_task": next_task,
                "package_scope": package_scope,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_repair_gap_queue(review_sets: Mapping[str, Sequence[Mapping[str, Any]]]) -> list[dict[str, Any]]:
    gaps: list[dict[str, Any]] = []
    for family, review_rows in review_sets.items():
        for row in review_rows:
            if not str(row.get("review_status", "")).startswith("accepted"):
                gaps.append(
                    {
                        "gap_id": f"{family}_{row.get('review_id', 'unknown')}",
                        "blueprint_family": family,
                        "source_artifact": row.get("source_artifact", ""),
                        "finding": row.get("finding", ""),
                        "repair_required": row.get("blocked_if", ""),
                        "next_action": "repair_run337F_blueprint_or_schema_before_package_materialization",
                        "claim_boundary": CLAIM_BOUNDARY,
                    }
                )
    return gaps


def build_run337h_queue(accepted_queue: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, row in enumerate(accepted_queue, start=1):
        if row.get("queue_status") != "accepted_for_run337H_package_materialization":
            continue
        rows.append(
            {
                "queue_id": row.get("next_task", ""),
                "priority": index,
                "blueprint_family": row.get("blueprint_family", ""),
                "required_review_input": rel(ACCEPTED_BLUEPRINT_QUEUE_CSV),
                "required_source_artifacts": "run337F blueprints and run337G review CSVs",
                "required_outputs": "package manifest;schema contract;blocker criteria;claim-boundary receipt;run337I review queue",
                "forbidden": "model training, MT5 execution, threshold retune, lot optimization, forward-pocket filtering, candidate selection, Forward Passed, runtime authority, Goal Achieve",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_gate_audit(
    source_lineage: Sequence[Mapping[str, Any]],
    review_sets: Mapping[str, Sequence[Mapping[str, Any]]],
    accepted_queue: Sequence[Mapping[str, Any]],
    repair_gaps: Sequence[Mapping[str, Any]],
    run337h_queue: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    source_ok = all(row.get("review_status") == "accepted_for_review" for row in source_lineage)
    family_ok = {
        family: all(str(row.get("review_status", "")).startswith("accepted") for row in rows)
        for family, rows in review_sets.items()
    }
    accepted_ok = all(row.get("queue_status") == "accepted_for_run337H_package_materialization" for row in accepted_queue)
    return [
        {
            "gate_id": "source_lineage_connected",
            "status": "pass" if source_ok and len(source_lineage) >= len(SOURCE_INPUTS) else "fail",
            "evidence": rel(SOURCE_LINEAGE_REVIEW_CSV),
            "finding": f"source_rows={len(source_lineage)};all_present={source_ok}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "no_lookahead_blueprint_review_accepted",
            "status": "pass" if family_ok["no_lookahead"] else "fail",
            "evidence": rel(NO_LOOKAHEAD_REVIEW_CSV),
            "finding": "bad-control harness covers five no-lookahead risk families",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "proxy_mt5_blueprint_review_accepted",
            "status": "pass" if family_ok["proxy_mt5"] else "fail",
            "evidence": rel(PROXY_MT5_REVIEW_CSV),
            "finding": "proxy expected, fresh MT5 package, and row-level difference schema accepted",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "core56_repair_blueprint_review_accepted",
            "status": "pass" if family_ok["core56"] else "fail",
            "evidence": rel(CORE56_REVIEW_CSV),
            "finding": "core56 full-family claims remain blocked until as-of repair and fresh runtime package",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "cost_direction_curve_blueprint_review_accepted",
            "status": "pass" if family_ok["cost_curve"] else "fail",
            "evidence": rel(COST_CURVE_REVIEW_CSV),
            "finding": "cost, spread/slippage, direction/source, curve, lot-normalized, and regime reports accepted",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "offense_blueprint_training_closed",
            "status": "pass" if family_ok["offense"] else "fail",
            "evidence": rel(OFFENSE_REVIEW_CSV),
            "finding": "offense branches are package-spec only and training-closed",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "economic_regime_asof_blueprint_review_accepted",
            "status": "pass" if family_ok["regime"] else "fail",
            "evidence": rel(REGIME_REVIEW_CSV),
            "finding": "VIX, USD, rate, ADX, volatility, session, hour, month as-of slices accepted",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "runtime_probe_package_review_accepted",
            "status": "pass" if family_ok["runtime"] else "fail",
            "evidence": rel(RUNTIME_REVIEW_CSV),
            "finding": "runtime package specs remain probe-only with no runtime authority",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "claim_boundary_review_passed",
            "status": "pass" if family_ok["claim_boundary"] else "fail",
            "evidence": rel(CLAIM_REVIEW_CSV),
            "finding": "no training, MT5 execution, selection, Forward decision, runtime authority, or Goal Achieve claimed",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "accepted_blueprint_queue_ready",
            "status": "pass" if accepted_ok and len(accepted_queue) >= 8 else "fail",
            "evidence": rel(ACCEPTED_BLUEPRINT_QUEUE_CSV),
            "finding": f"accepted_blueprint_families={len(accepted_queue)}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "repair_gap_queue_empty",
            "status": "pass" if not repair_gaps else "fail",
            "evidence": rel(REPAIR_GAP_QUEUE_CSV),
            "finding": f"repair_gap_rows={len(repair_gaps)}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "run337H_package_materialization_queue_ready",
            "status": "pass" if len(run337h_queue) >= 8 else "fail",
            "evidence": rel(RUN337H_QUEUE_CSV),
            "finding": f"run337H_queue_rows={len(run337h_queue)}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "claim_guard_no_selection_no_goal",
            "status": "pass",
            "evidence": rel(FINAL_DECISION_JSON),
            "finding": "run337G is review-only and opens package materialization only",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_metrics(
    source_lineage: Sequence[Mapping[str, Any]],
    review_sets: Mapping[str, Sequence[Mapping[str, Any]]],
    accepted_queue: Sequence[Mapping[str, Any]],
    repair_gaps: Sequence[Mapping[str, Any]],
    run337h_queue: Sequence[Mapping[str, Any]],
    audit: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    return {
        "source_lineage_rows": len(source_lineage),
        "review_family_count": len(review_sets),
        "review_rows": sum(len(rows) for rows in review_sets.values()),
        "accepted_review_rows": sum(
            1 for rows in review_sets.values() for row in rows if str(row.get("review_status", "")).startswith("accepted")
        ),
        "accepted_blueprint_families": len(
            [row for row in accepted_queue if row.get("queue_status") == "accepted_for_run337H_package_materialization"]
        ),
        "repair_gap_rows": len(repair_gaps),
        "run337h_queue_rows": len(run337h_queue),
        "gate_rows": len(audit),
        "failed_gate_rows": len([row for row in audit if row.get("status") != "pass"]),
    }


def write_receipts(metrics: Mapping[str, Any]) -> list[Path]:
    return [
        write_json(
            EXPERIMENT_DESIGN_JSON,
            {
                "run_id": RUN_ID,
                "hypothesis": "run337F protocol-bound blueprints are complete enough to open package materialization without training or MT5 execution",
                "decision_use": "decide whether run337H may materialize package specs for no-lookahead, proxy-MT5, core56, cost/curve, offense, regime, runtime, and claim guards",
                "comparison_baseline": "run337F blueprints, schemas, acceptance matrix, gate audit, final decision, and manifest",
                "control_variables": "no model training, no MT5 execution, no threshold retune, no lot optimization, no forward-pocket filtering, no candidate selection",
                "changed_variables": "blueprint review labels, repair gap queue, and run337H package materialization queue",
                "sample_scope": "blueprint and schema artifacts only; no trading KPI sample or runtime execution",
                "success_criteria": "all blueprint families accepted, repair gap queue empty, and run337H package queue ready",
                "failure_criteria": "any blueprint lacks no-lookahead guard, proxy-MT5 identity, core56 as-of guard, cost/curve report scope, runtime blocker, or claim boundary",
                "invalid_conditions": "using run337G review to claim Forward Passed, runtime authority, candidate selection, or operating readiness",
                "stop_conditions": "any gate fails; repair blueprint gap before package materialization",
                "evidence_plan": "review CSVs, accepted queue, repair gap queue, run337H queue, receipts, final decision, ledgers, artifact registry",
                "metrics": metrics,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            DATA_INTEGRITY_JSON,
            {
                "run_id": RUN_ID,
                "data_source": "run337F blueprint and schema artifacts",
                "time_axis": "future executable packages must carry cycle_bar_time, source_timestamp, broker timezone, timestamp basis, and as-of join status",
                "sample_scope": "blueprint review only; no new US100 M5 bars, no model rows, and no MT5 trade rows are consumed",
                "missing_or_duplicate_check": "review requires future packages to expose missing, duplicate, stale, revision, timezone, and future join checks",
                "feature_label_boundary": "no labels or model fit; no-lookahead harness must reject future-derived controls before package execution",
                "split_boundary": "future train/WFO/forward split remains closed until reviewed package specs are complete",
                "leakage_risk": "future-bar feature use, forward-pocket filtering, threshold retune, lot optimization, timestamp-basis drift, and macro revision drift",
                "data_hash_or_identity": rel(SOURCE_LINEAGE_REVIEW_CSV),
                "integrity_judgment": "usable_with_boundary",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RUNTIME_PARITY_JSON,
            {
                "run_id": RUN_ID,
                "research_path": rel(Path(__file__)),
                "runtime_path": rel(RUNTIME_REVIEW_CSV),
                "shared_contract": "feature order, threshold, risk, lot, timestamp basis, proxy expected values, MT5 observed values, tester report, trade ledger, D/B source, cost stress, and regime slices must match before KPI authority",
                "known_differences": "run337G does not execute MT5 and does not generate proxy observed values; it reviews package prerequisites only",
                "parity_check": "runtime package blueprint review confirms fresh MT5 probe and row-level proxy-MT5 difference remain mandatory",
                "parity_identity": rel(PROXY_MT5_REVIEW_CSV),
                "runtime_claim_boundary": "research-only blueprint review, no runtime authority",
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
                    rel(SOURCE_LINEAGE_REVIEW_CSV),
                    rel(ACCEPTED_BLUEPRINT_QUEUE_CSV),
                    rel(REPAIR_GAP_QUEUE_CSV),
                    rel(RUN337H_QUEUE_CSV),
                    rel(GATE_AUDIT_CSV),
                ],
                "artifact_hashes": "registered in artifact_registry after run",
                "registry_links": "run_registry;alpha_run_ledger;stage_run_ledger;artifact_registry",
                "availability": "tracked after commit; reproducible from run337G script",
                "lineage_judgment": "connected_with_boundary",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RESULT_JUDGMENT_JSON,
            {
                "run_id": RUN_ID,
                "result_subject": "Stage337F protocol-bound execution blueprints",
                "evidence_available": "blueprint review CSVs, accepted queue, repair gap queue, run337H queue, gate audit",
                "evidence_missing": "no package files yet, no model training, no MT5 execution, no proxy expected values, no MT5 observed values, no candidate KPI",
                "judgment_label": "exploratory",
                "claim_boundary": "blueprints are accepted for package materialization only; no candidate, Forward decision, or runtime authority",
                "next_condition": NEXT_RUN_ID,
                "user_explanation_hook": "청사진은 검토를 통과했지만 아직 실행 패키지 자체는 만들지 않았다. 다음 단계는 패키지 명세를 물질화하는 일이다.",
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
# run337G Protocol-Bound Execution Blueprint Review(337G 절차 기반 실행 청사진 검토)

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

## Review Result(검토 결과)

- source_lineage_rows(원천 계보 행): `{metrics['source_lineage_rows']}`
- review_family_count(검토 묶음 수): `{metrics['review_family_count']}`
- review_rows(검토 행): `{metrics['review_rows']}`
- accepted_review_rows(승인 검토 행): `{metrics['accepted_review_rows']}`
- accepted_blueprint_families(승인 청사진 묶음): `{metrics['accepted_blueprint_families']}`
- repair_gap_rows(수리 공백 행): `{metrics['repair_gap_rows']}`
- run337H_queue_rows(337H 대기열 행): `{metrics['run337h_queue_rows']}`
- gate_rows(게이트 행): `{metrics['gate_rows']}`, failed(실패): `{metrics['failed_gate_rows']}`

Effect(효과): run337G(337G 실행)는 run337F(337F 실행)의 청사진을 검토해 no-lookahead(미래참조 방어), proxy-MT5(프록시-MT5), core56(핵심56), cost/direction/curve(비용/방향/곡선), offense(공격), economic regime as-of(경제 국면 시점 기준), runtime package(런타임 패키지), claim guard(주장 방어)를 run337H(337H 실행) package materialization(패키지 물질화) 대기열로 보낸다. 아직 model training(모델 학습), MT5 execution(MT5 실행), candidate selection(후보 선택)은 없다.
"""
    decision = f"""
# 2026-05-27 Stage337G Decision(337G 결정)

- decision(결정): `{DECISION}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed_for_stage337_new_work`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`

Effect(효과): 다음 run337H(337H 실행)는 reviewed execution package specs(검토된 실행 패키지 명세)를 물질화한다. 이 결정은 학습 허가, MT5 실행 결과, Forward 판정, 운영 승격이 아니다.
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
- effect(효과): run337G(337G 실행)는 run337F(337F 실행) 청사진을 검토하고 run337H(337H 실행) 패키지 물질화 대기열로 넘겼다. 아직 선택 후보는 없다.
"""
    artifacts.append(write_md(SELECTED_DIR / "selection_status.md", selection))

    brief_text, brief_bom = read_text_lossless(SPEC_DIR / "stage_brief.md")
    brief_text = replace_prefix_line(brief_text, "- latest_run(최신 실행):", f"- latest_run(최신 실행): `{RUN_ID}`")
    brief_text = insert_after_marker_once(
        brief_text,
        "- run337F_summary(337F 요약):",
        f"- run337G_summary(337G 요약): `{STATUS}`. Effect(효과): run337F(337F 실행) 청사진을 검토해 8개 blueprint family(청사진 묶음)를 run337H(337H 실행) package materialization(패키지 물질화) 대기열로 넘긴다.",
        "run337G_summary",
    )
    artifacts.append(write_text_lossless(SPEC_DIR / "stage_brief.md", brief_text, brief_bom))

    input_section = f"""
- blueprint_review_source_lineage(청사진 검토 원천 계보): `{rel(SOURCE_LINEAGE_REVIEW_CSV)}`
- no_lookahead_harness_blueprint_review(미래참조 방어 청사진 검토): `{rel(NO_LOOKAHEAD_REVIEW_CSV)}`
- proxy_mt5_blueprint_review(프록시-MT5 청사진 검토): `{rel(PROXY_MT5_REVIEW_CSV)}`
- core56_repair_blueprint_review(핵심56 수리 청사진 검토): `{rel(CORE56_REVIEW_CSV)}`
- cost_direction_curve_extraction_blueprint_review(비용/방향/곡선 추출 청사진 검토): `{rel(COST_CURVE_REVIEW_CSV)}`
- offense_branch_blueprint_review(공격 분기 청사진 검토): `{rel(OFFENSE_REVIEW_CSV)}`
- economic_regime_asof_blueprint_review(경제 국면 시점 기준 청사진 검토): `{rel(REGIME_REVIEW_CSV)}`
- runtime_probe_package_blueprint_review(런타임 탐침 패키지 청사진 검토): `{rel(RUNTIME_REVIEW_CSV)}`
- accepted_blueprints_for_package_queue(패키지용 승인 청사진 대기열): `{rel(ACCEPTED_BLUEPRINT_QUEUE_CSV)}`
- run337H_queue(337H 대기열): `{rel(RUN337H_QUEUE_CSV)}`

Effect(효과): 다음 실행은 이 검토 결과를 근거로 실제 package spec(패키지 명세)을 만들되, 학습과 MT5 실행은 계속 닫아둔다.
"""
    artifacts.append(append_section_once(INPUTS_DIR / "input_refs.md", "## run337G Outputs(337G 산출물)", input_section))

    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_prefix_line(workspace_text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    focus = (
        "- >-\n"
        f"  Stage337 run337G focus complete: Stage337(337단계) run337G(337G 실행)는 `{STATUS}`로 protocol-bound execution blueprint review(절차 기반 실행 청사진 검토)를 완료했다. "
        "Effect(효과): run337H(337H 실행) package materialization(패키지 물질화) 대기열을 열었지만 model training(모델 학습), MT5 execution(MT5 실행), candidate selection(후보 선택)은 아직 닫아둔다.\n"
    )
    workspace_text = insert_focus_once(workspace_text, focus, "Stage337 run337G focus complete")
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
        f"- run337G_summary(337G 요약): `{STATUS}`. "
        "Effect(효과): 8개 청사진 묶음을 검토 승인하고 run337H(337H 실행) 패키지 물질화 대기열로 넘기며, 학습/MT5/후보 선택은 계속 닫아둔다."
    )
    current_text = insert_after_marker_once(current_text, "- decision(결정):", summary, "run337G_summary")
    artifacts.append(write_text_lossless(CURRENT_STATE, current_text, current_bom))

    artifacts.append(
        append_section_once(
            CHANGELOG,
            "## Stage337G Protocol-Bound Execution Blueprint Review(337G 절차 기반 실행 청사진 검토)",
            f"""
- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- action(행동): run337F(337F 실행)의 청사진과 스키마를 검토해 run337H(337H 실행) 패키지 물질화 대기열을 만들었다.
- effect(효과): no-lookahead/proxy-MT5/core56/cost-direction-curve/offense/regime/runtime/claim-guard(미래참조/프록시-MT5/핵심56/비용-방향-곡선/공격/국면/런타임/주장 방어) 패키지 명세 생성을 열었다.
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
                "lane": "protocol_bound_execution_blueprint_review",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_DOC),
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};blueprints_reviewed;training_not_allowed;mt5_not_executed;goal_achieve_not_claimed.",
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__protocol_bound_execution_blueprint_review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "protocol_bound_execution_blueprint_review",
                "tier_scope": "stage337_blueprint_boundary_macro48_u42_core56",
                "kpi_scope": "blueprint_review_only_no_new_candidate_kpi",
                "scoreboard_lane": "blueprint_review_readiness",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_DOC),
                "primary_kpi": "accepted_blueprint_families=8;run337h_queue_rows=8;candidate_selection=none",
                "guardrail_kpi": "training_not_allowed;mt5_not_executed;runtime_authority_not_claimed;goal_achieve_not_claimed",
                "external_verification_status": "out_of_scope_by_claim_blueprint_review_only",
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
                "ledger_row_id": f"{RUN_ID}__protocol_bound_execution_blueprint_review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "work_family": "result_judgment",
                "evidence_scope": "run337F_protocol_bound_execution_blueprints",
                "kpi_scope": "blueprint_review_only_no_new_candidate_kpi",
                "status": STATUS,
                "judgment": JUDGMENT,
                "claim_boundary": CLAIM_BOUNDARY,
                "path": rel(REPORT_DOC),
                "notes": f"next_action={NEXT_RUN_ID};blueprints_reviewed;training_not_allowed;mt5_not_executed;goal_achieve_not_claimed.",
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
            "notes": "run337G_protocol_bound_blueprint_review_no_selection",
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
    source_lineage = build_source_lineage_review()
    review_sets = {
        "no_lookahead": review_no_lookahead(inputs),
        "proxy_mt5": review_proxy_mt5(inputs),
        "core56": review_core56(inputs),
        "cost_curve": review_cost_curve(inputs),
        "offense": review_offense(inputs),
        "regime": review_regime(inputs),
        "runtime": review_runtime(inputs),
        "claim_boundary": review_claim_boundary(inputs),
    }
    accepted_queue = build_accepted_queue(review_sets)
    repair_gaps = build_repair_gap_queue(review_sets)
    run337h_queue = build_run337h_queue(accepted_queue)
    audit = build_gate_audit(source_lineage, review_sets, accepted_queue, repair_gaps, run337h_queue)
    metrics = build_metrics(source_lineage, review_sets, accepted_queue, repair_gaps, run337h_queue, audit)
    failed_gates = [row for row in audit if row.get("status") != "pass"]

    run_artifacts = [
        write_csv(
            SOURCE_LINEAGE_REVIEW_CSV,
            ("source_path", "exists", "sha256", "row_count_or_keys", "review_status", "allowed_use", "forbidden_use", "claim_boundary"),
            source_lineage,
        ),
        write_csv(
            NO_LOOKAHEAD_REVIEW_CSV,
            (
                "review_id",
                "source_artifact",
                "schema_artifact",
                "review_scope",
                "checks",
                "review_status",
                "finding",
                "next_use",
                "blocked_if",
                "claim_boundary",
            ),
            review_sets["no_lookahead"],
        ),
        write_csv(
            PROXY_MT5_REVIEW_CSV,
            (
                "review_id",
                "source_artifact",
                "schema_artifact",
                "review_scope",
                "checks",
                "review_status",
                "finding",
                "next_use",
                "blocked_if",
                "claim_boundary",
            ),
            review_sets["proxy_mt5"],
        ),
        write_csv(
            CORE56_REVIEW_CSV,
            (
                "review_id",
                "source_artifact",
                "schema_artifact",
                "review_scope",
                "checks",
                "review_status",
                "finding",
                "next_use",
                "blocked_if",
                "claim_boundary",
            ),
            review_sets["core56"],
        ),
        write_csv(
            COST_CURVE_REVIEW_CSV,
            (
                "review_id",
                "source_artifact",
                "schema_artifact",
                "review_scope",
                "checks",
                "review_status",
                "finding",
                "next_use",
                "blocked_if",
                "claim_boundary",
            ),
            review_sets["cost_curve"],
        ),
        write_csv(
            OFFENSE_REVIEW_CSV,
            (
                "review_id",
                "source_artifact",
                "schema_artifact",
                "review_scope",
                "checks",
                "review_status",
                "finding",
                "next_use",
                "blocked_if",
                "claim_boundary",
            ),
            review_sets["offense"],
        ),
        write_csv(
            REGIME_REVIEW_CSV,
            (
                "review_id",
                "source_artifact",
                "schema_artifact",
                "review_scope",
                "checks",
                "review_status",
                "finding",
                "next_use",
                "blocked_if",
                "claim_boundary",
            ),
            review_sets["regime"],
        ),
        write_csv(
            RUNTIME_REVIEW_CSV,
            (
                "review_id",
                "source_artifact",
                "schema_artifact",
                "review_scope",
                "checks",
                "review_status",
                "finding",
                "next_use",
                "blocked_if",
                "claim_boundary",
            ),
            review_sets["runtime"],
        ),
        write_csv(
            CLAIM_REVIEW_CSV,
            (
                "review_id",
                "source_artifact",
                "schema_artifact",
                "review_scope",
                "checks",
                "review_status",
                "finding",
                "next_use",
                "blocked_if",
                "claim_boundary",
            ),
            review_sets["claim_boundary"],
        ),
        write_csv(
            ACCEPTED_BLUEPRINT_QUEUE_CSV,
            ("blueprint_family", "accepted_rows", "total_rows", "queue_status", "next_task", "package_scope", "claim_boundary"),
            accepted_queue,
        ),
        write_csv(
            REPAIR_GAP_QUEUE_CSV,
            ("gap_id", "blueprint_family", "source_artifact", "finding", "repair_required", "next_action", "claim_boundary"),
            repair_gaps,
        ),
        write_csv(
            RUN337H_QUEUE_CSV,
            (
                "queue_id",
                "priority",
                "blueprint_family",
                "required_review_input",
                "required_source_artifacts",
                "required_outputs",
                "forbidden",
                "claim_boundary",
            ),
            run337h_queue,
        ),
        write_csv(GATE_AUDIT_CSV, ("gate_id", "status", "evidence", "finding", "claim_boundary"), audit),
    ]
    run_artifacts.extend(write_receipts(metrics))
    final_payload = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS if not failed_gates else "blocked_stage337G_blueprint_review_gate_failure",
        "judgment": JUDGMENT if not failed_gates else "stage337G_blueprint_review_requires_repair",
        "decision": DECISION if not failed_gates else "stage337G_blueprint_review_blocked_gate_failure",
        "metrics": metrics,
        "failed_gates": failed_gates,
        "next_action": NEXT_RUN_ID if not failed_gates else "repair_run337F_blueprint_gaps_before_package_materialization",
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
                "status": "blocked_stage337G_blueprint_review_gate_failure",
                "decision": "stage337G_blueprint_review_blocked_gate_failure",
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
        "external_verification_status": "out_of_scope_by_claim_blueprint_review_only_no_mt5_execution",
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
                "accepted_blueprint_families": metrics["accepted_blueprint_families"],
                "repair_gap_rows": metrics["repair_gap_rows"],
                "run337H_queue_rows": metrics["run337h_queue_rows"],
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
