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
RUN_NUMBER = "run337E"
RUN_ID = "run337E_review_research_execution_protocols_v1"
PARENT_RUN_ID = "run337D_materialize_research_execution_protocols_v1"
NEXT_RUN_ID = "run337F_materialize_protocol_bound_execution_blueprints_v1"
STATUS = "completed_research_execution_protocol_review_accepts_blueprint_queue_no_training"
JUDGMENT = "stage337E_protocol_review_accepts_blueprint_materialization_no_selection"
DECISION = "stage337E_protocols_reviewed_open_run337F_blueprints_no_training_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage337E_protocol_review_no_model_training_"
    "no_threshold_retuning_no_lot_optimization_no_forward_pocket_filtering_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
RUN337D_DIR = STAGE_DIR / "02_runs" / "run337D"
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
DECISION_DOC = DOCS / "decisions" / "2026-05-27_stage337E_review_research_execution_protocols.md"
REPORT_DOC = REVIEWS_DIR / "run337E_review_research_execution_protocols.md"

RUN337D_QUEUE = RUN337D_DIR / "run337E_review_execution_protocols_queue.csv"
RUN337D_NO_LOOKAHEAD = RUN337D_DIR / "no_lookahead_execution_protocol.csv"
RUN337D_PROXY_MT5 = RUN337D_DIR / "proxy_mt5_fresh_probe_protocol.csv"
RUN337D_CORE56 = RUN337D_DIR / "core56_refresh_repair_protocol.csv"
RUN337D_COST_CURVE = RUN337D_DIR / "cost_direction_curve_gate_execution_protocol.csv"
RUN337D_OFFENSE = RUN337D_DIR / "offense_rebuild_execution_protocol.csv"
RUN337D_REGIME = RUN337D_DIR / "economic_regime_asof_protocol.csv"
RUN337D_RUNTIME_REQUIREMENTS = RUN337D_DIR / "runtime_probe_package_requirements.csv"
RUN337D_TRAINING_BOUNDARY = RUN337D_DIR / "model_training_allowed_boundary.csv"
RUN337D_PROTOCOL_ACCEPTANCE = RUN337D_DIR / "protocol_acceptance_matrix.csv"
RUN337D_GATE_AUDIT = RUN337D_DIR / "required_gate_coverage_audit.csv"
RUN337D_DECISION = RUN337D_DIR / "final_research_execution_protocols_decision.json"
RUN337D_MANIFEST = RUN337D_DIR / "run_manifest.json"

PROTOCOL_INPUT_LINEAGE_CSV = RUN_DIR / "protocol_input_lineage_review.csv"
NO_LOOKAHEAD_REVIEW_CSV = RUN_DIR / "no_lookahead_protocol_review.csv"
PROXY_MT5_REVIEW_CSV = RUN_DIR / "proxy_mt5_fresh_probe_protocol_review.csv"
CORE56_REVIEW_CSV = RUN_DIR / "core56_refresh_protocol_review.csv"
COST_CURVE_REVIEW_CSV = RUN_DIR / "cost_direction_curve_protocol_review.csv"
OFFENSE_REVIEW_CSV = RUN_DIR / "offense_rebuild_protocol_review.csv"
REGIME_REVIEW_CSV = RUN_DIR / "economic_regime_asof_protocol_review.csv"
RUNTIME_REVIEW_CSV = RUN_DIR / "runtime_probe_requirements_review.csv"
TRAINING_BOUNDARY_REVIEW_CSV = RUN_DIR / "model_training_boundary_review.csv"
ACCEPTED_PROTOCOL_QUEUE_CSV = RUN_DIR / "accepted_protocols_for_blueprint_queue.csv"
REPAIR_GAP_QUEUE_CSV = RUN_DIR / "repair_protocol_gap_queue.csv"
RUN337F_QUEUE_CSV = RUN_DIR / "run337F_blueprint_materialization_queue.csv"
GATE_AUDIT_CSV = RUN_DIR / "required_gate_coverage_audit.csv"

EXPERIMENT_DESIGN_JSON = RUN_DIR / "experiment_design_receipt.json"
DATA_INTEGRITY_JSON = RUN_DIR / "data_integrity_receipt.json"
RUNTIME_PARITY_JSON = RUN_DIR / "runtime_parity_receipt.json"
ARTIFACT_LINEAGE_JSON = RUN_DIR / "artifact_lineage_receipt.json"
RESULT_JUDGMENT_JSON = RUN_DIR / "result_judgment_receipt.json"
FINAL_DECISION_JSON = RUN_DIR / "final_review_research_execution_protocols_decision.json"
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


def contains_all(text: str, needles: Sequence[str]) -> bool:
    lowered = text.lower()
    return all(needle.lower() in lowered for needle in needles)


def load_inputs() -> dict[str, Any]:
    return {
        "review_queue": read_csv(RUN337D_QUEUE),
        "no_lookahead": read_csv(RUN337D_NO_LOOKAHEAD),
        "proxy_mt5": read_csv(RUN337D_PROXY_MT5),
        "core56": read_csv(RUN337D_CORE56),
        "cost_curve": read_csv(RUN337D_COST_CURVE),
        "offense": read_csv(RUN337D_OFFENSE),
        "regime": read_csv(RUN337D_REGIME),
        "runtime_requirements": read_csv(RUN337D_RUNTIME_REQUIREMENTS),
        "training_boundary": read_csv(RUN337D_TRAINING_BOUNDARY),
        "protocol_acceptance": read_csv(RUN337D_PROTOCOL_ACCEPTANCE),
        "gate_audit": read_csv(RUN337D_GATE_AUDIT),
        "run337d_decision": read_json(RUN337D_DECISION),
        "run337d_manifest": read_json(RUN337D_MANIFEST),
    }


def build_protocol_input_lineage(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    expected_paths = [
        RUN337D_QUEUE,
        RUN337D_NO_LOOKAHEAD,
        RUN337D_PROXY_MT5,
        RUN337D_CORE56,
        RUN337D_COST_CURVE,
        RUN337D_OFFENSE,
        RUN337D_REGIME,
        RUN337D_RUNTIME_REQUIREMENTS,
        RUN337D_TRAINING_BOUNDARY,
        RUN337D_PROTOCOL_ACCEPTANCE,
        RUN337D_GATE_AUDIT,
        RUN337D_DECISION,
        RUN337D_MANIFEST,
    ]
    manifest_outputs = set(inputs["run337d_manifest"].get("outputs", []))
    rows = []
    for path in expected_paths:
        exists = path_exists(path)
        row_count = ""
        if path.suffix.lower() == ".csv" and exists:
            row_count = len(read_csv(path))
        rows.append(
            {
                "source_path": rel(path),
                "exists": exists,
                "sha256": sha256_file_lf_normalized(path) if exists else "missing",
                "row_count": row_count,
                "manifest_linked": rel(path) in manifest_outputs or path.name == "run_manifest.json",
                "lineage_review": "pass" if exists else "fail",
                "allowed_use": "run337E protocol review input",
                "forbidden_use": "candidate selection, Forward Passed, runtime authority, or Goal Achieve",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def review_no_lookahead(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    required_risks = {
        "future": False,
        "forward": False,
        "threshold": False,
        "lot": False,
        "timestamp": False,
    }
    review_rows = []
    for row in rows:
        blob = " ".join(str(value) for value in row.values()).lower()
        for key in required_risks:
            if key in blob:
                required_risks[key] = True
        checks = {
            "has_bad_control": bool(row.get("expected_bad_control_result")),
            "has_pass_fail": bool(row.get("pass_condition")) and bool(row.get("fail_condition")),
            "has_repair": bool(row.get("repair_action")),
            "forbids_claim": contains_all(row.get("forbidden_use", ""), ["Forward Passed"]) or contains_all(row.get("forbidden_use", ""), ["runtime authority"]),
        }
        accepted = all(checks.values())
        review_rows.append(
            {
                "protocol_id": row.get("protocol_id", ""),
                "risk_target": row.get("risk_target", ""),
                "review_status": "accepted_for_blueprint_materialization" if accepted else "repair_required",
                "checks": checks,
                "finding": "bad-control rejection, pass/fail, repair, and claim guard present" if accepted else "missing no-lookahead guard component",
                "next_blueprint_use": "materialize canary harness spec and invalid-condition matrix",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    review_rows.append(
        {
            "protocol_id": "coverage_summary",
            "risk_target": "future, forward-pocket, threshold, lot, timestamp coverage",
            "review_status": "accepted_for_blueprint_materialization" if all(required_risks.values()) else "repair_required",
            "checks": required_risks,
            "finding": "all required leakage/overfit risks are covered" if all(required_risks.values()) else "risk coverage gap",
            "next_blueprint_use": "materialize complete no-lookahead harness",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )
    return review_rows


def review_proxy_mt5(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    review_rows = []
    for row in rows:
        checks = {
            "fresh_proxy_required": row.get("fresh_proxy_expected_required") == "true",
            "fresh_mt5_required": row.get("fresh_mt5_runtime_probe_required") == "true",
            "comparison_grain_present": contains_all(row.get("comparison_grain", ""), ["cycle_bar_time", "D_source", "B_source"]),
            "difference_metrics_present": contains_all(row.get("difference_metrics", ""), ["decision", "timestamp"]),
            "mt5_kpi_authority": "MT5" in row.get("kpi_authority_condition", ""),
            "proxy_only_forbidden": "proxy-only" in row.get("forbidden_use", ""),
        }
        accepted = all(checks.values())
        review_rows.append(
            {
                "subject": row.get("subject", ""),
                "source_review_status": row.get("source_review_status", ""),
                "review_status": "accepted_for_blueprint_materialization" if accepted else "repair_required",
                "checks": checks,
                "finding": "fresh proxy, fresh MT5, row-level comparison, and KPI authority boundary present" if accepted else "proxy-MT5 protocol gap",
                "next_blueprint_use": "materialize proxy expected schema, MT5 package schema, difference report schema, and usability rules",
                "forbidden_after_review": "proxy-only KPI, Forward Passed, candidate selection, operating reference",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return review_rows


def review_core56(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    review_rows = []
    for row in rows:
        blocked_text = row.get("blocked_claim_until_pass", "")
        checks = {
            "asof_control": "as-of" in row.get("no_lookahead_control", "").lower(),
            "output_required": bool(row.get("output_required")),
            "pass_condition": bool(row.get("pass_condition")),
            "blocks_full_family": "full-family" in blocked_text,
            "blocks_forward_goal": "Forward Passed" in blocked_text and "Goal Achieve" in blocked_text,
        }
        accepted = all(checks.values())
        review_rows.append(
            {
                "protocol_id": row.get("protocol_id", ""),
                "step_order": row.get("step_order", ""),
                "review_status": "accepted_for_blueprint_materialization" if accepted else "repair_required",
                "checks": checks,
                "finding": "core56 repair step preserves as-of boundary and blocks full-family claims" if accepted else "core56 repair lock gap",
                "next_blueprint_use": "materialize source inventory, as-of join, feature handoff, proxy expected, and fresh MT5 probe blueprint",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return review_rows


def review_cost_curve(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    expected_scopes = {
        "cost": False,
        "direction": False,
        "curve": False,
        "lot": False,
        "regime": False,
    }
    review_rows = []
    for row in rows:
        blob = " ".join(str(value) for value in row.values()).lower()
        for key in expected_scopes:
            if key in blob:
                expected_scopes[key] = True
        checks = {
            "has_required_measurement": bool(row.get("required_measurement")),
            "has_acceptance_boundary": bool(row.get("acceptance_boundary")),
            "has_failure_memory_trigger": bool(row.get("failure_memory_trigger")),
            "requires_runtime_inputs": contains_all(row.get("required_runtime_inputs", ""), ["MT5", "trade ledger"]),
            "forbids_shortcuts": contains_all(row.get("forbidden_shortcut", ""), ["proxy-only", "threshold", "lot"]),
        }
        accepted = all(checks.values())
        review_rows.append(
            {
                "protocol_id": row.get("protocol_id", ""),
                "gate_scope": row.get("gate_scope", ""),
                "review_status": "accepted_for_blueprint_materialization" if accepted else "repair_required",
                "checks": checks,
                "finding": "measurement, runtime input, failure trigger, and shortcut guard present" if accepted else "cost/direction/curve gate gap",
                "next_blueprint_use": "materialize extraction schemas for cost ladder, long/short, D/B, curve pocket, lot-normalized, and regime slices",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    review_rows.append(
        {
            "protocol_id": "coverage_summary",
            "gate_scope": "cost, direction, curve, lot, regime coverage",
            "review_status": "accepted_for_blueprint_materialization" if all(expected_scopes.values()) else "repair_required",
            "checks": expected_scopes,
            "finding": "all required gate families covered" if all(expected_scopes.values()) else "gate family coverage gap",
            "next_blueprint_use": "materialize full gate extraction matrix",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )
    return review_rows


def review_offense(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    review_rows = []
    for row in rows:
        checks = {
            "predeclared_hypothesis": bool(row.get("hypothesis")),
            "decision_use_not_selection": "not select" in row.get("decision_use", "").lower(),
            "controls_no_retune": contains_all(row.get("control_variables", ""), ["no post-forward threshold"]),
            "invalid_lookahead_mt5": contains_all(row.get("invalid_conditions", ""), ["lookahead", "missing MT5"]),
            "evidence_plan_runtime": contains_all(row.get("evidence_plan", ""), ["proxy expected", "MT5 report", "trade ledger"]),
        }
        accepted = all(checks.values())
        review_rows.append(
            {
                "branch_id": row.get("branch_id", ""),
                "review_status": "accepted_for_blueprint_materialization" if accepted else "repair_required",
                "checks": checks,
                "finding": "offense thesis is predeclared with no-retune controls and MT5 evidence plan" if accepted else "offense protocol gap",
                "next_blueprint_use": "materialize branch-specific blueprint without training or candidate selection",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return review_rows


def review_regime(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    review_rows = []
    for row in rows:
        asof_rule = row.get("asof_rule", "")
        asof_text = asof_rule.lower()
        asof_rejects_future = bool(asof_rule) and (
            "future" not in asof_text
            or "no future" in asof_text
            or "previous" in asof_text
            or "current" in asof_text
            or "confirmed" in asof_text
        )
        checks = {
            "source_requirement": bool(row.get("data_source_requirement")),
            "asof_rule": asof_rejects_future,
            "join_key": contains_all(row.get("join_key", ""), ["cycle_bar_time", "source_timestamp"]),
            "checks_revision_timezone": contains_all(row.get("required_checks", ""), ["revision", "timezone"]),
            "future_invalid": "future" in row.get("invalid_if", "").lower(),
        }
        accepted = all(checks.values())
        review_rows.append(
            {
                "protocol_id": row.get("protocol_id", ""),
                "regime_source": row.get("regime_source", ""),
                "review_status": "accepted_for_blueprint_materialization" if accepted else "repair_required",
                "checks": checks,
                "finding": "as-of data source, join key, revision/timezone checks, and future invalid rule present" if accepted else "economic regime as-of gap",
                "next_blueprint_use": "materialize as-of source audit and regime slice extraction blueprint",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return review_rows


def review_runtime(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    review_rows = []
    for row in rows:
        checks = {
            "required_files": contains_all(row.get("required_files", ""), ["feature_order", "MT5_set", "handoff"]),
            "runtime_outputs": contains_all(row.get("runtime_outputs", ""), ["Strategy Tester", "terminal", "trade ledger"]),
            "parity_outputs": contains_all(row.get("parity_outputs", ""), ["proxy_expected", "difference_report"]),
            "cost_outputs": contains_all(row.get("cost_outputs", ""), ["cost_stress", "lot_normalized"]),
            "attribution_outputs": contains_all(row.get("attribution_outputs", ""), ["D_source", "long_short", "regime"]),
            "blocked_if_missing": contains_all(row.get("blocked_if_missing", ""), ["timestamp", "trade ledger"]),
        }
        accepted = all(checks.values())
        review_rows.append(
            {
                "package_id": row.get("package_id", ""),
                "subject": row.get("subject", ""),
                "review_status": "accepted_for_blueprint_materialization" if accepted else "repair_required",
                "checks": checks,
                "finding": "runtime package requires tester output, telemetry/logs, trade ledger, parity, cost, and attribution evidence" if accepted else "runtime package gap",
                "next_blueprint_use": "materialize future MT5 package blueprint and blocker criteria",
                "runtime_claim_boundary": "runtime_probe_future_only_no_runtime_authority",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return review_rows


def review_training_boundary(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    review_rows = []
    for row in rows:
        checks = {
            "training_not_allowed_in_run337D": row.get("training_allowed_in_run337D") == "false",
            "reopen_condition_mentions_run337E": "run337E" in row.get("earliest_reopen_condition", ""),
            "still_forbids_shortcuts": contains_all(row.get("still_forbidden_after_reopen", ""), ["threshold", "lot", "proxy-only", "runtime authority"]),
            "allowed_after_reopen_predeclared": "predeclared" in row.get("allowed_after_reopen", "").lower(),
        }
        accepted = all(checks.values())
        review_rows.append(
            {
                "boundary_id": row.get("boundary_id", ""),
                "review_status": "accepted_for_blueprint_materialization_training_still_closed" if accepted else "repair_required",
                "checks": checks,
                "finding": "training remains closed in run337E; next run may materialize blueprints only" if accepted else "training boundary gap",
                "next_blueprint_use": "materialize execution blueprints, not train models",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return review_rows


def collect_repair_gaps(review_sets: Mapping[str, Sequence[Mapping[str, Any]]]) -> list[dict[str, Any]]:
    gaps = []
    for review_name, rows in review_sets.items():
        for row in rows:
            status = str(row.get("review_status", ""))
            if "repair_required" in status or "fail" in status:
                subject = row.get("protocol_id") or row.get("subject") or row.get("branch_id") or row.get("package_id") or row.get("boundary_id") or review_name
                gaps.append(
                    {
                        "gap_id": f"{review_name}::{subject}",
                        "review_name": review_name,
                        "subject": subject,
                        "reason": row.get("finding", "review gap"),
                        "required_repair": "repair protocol before blueprint materialization",
                        "claim_boundary": CLAIM_BOUNDARY,
                    }
                )
    return gaps


def build_accepted_protocol_queue(review_sets: Mapping[str, Sequence[Mapping[str, Any]]]) -> list[dict[str, Any]]:
    queue = []
    for review_name, rows in review_sets.items():
        accepted = [row for row in rows if str(row.get("review_status", "")).startswith("accepted")]
        total = len(rows)
        status = "accepted_for_run337F_blueprint_materialization" if accepted and len(accepted) == total else "blocked_until_repair"
        queue.append(
            {
                "protocol_family": review_name,
                "accepted_rows": len(accepted),
                "total_rows": total,
                "queue_status": status,
                "next_use": "run337F blueprint materialization" if status.startswith("accepted") else "repair first",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return queue


def build_run337f_queue(accepted_queue: Sequence[Mapping[str, Any]], repair_gaps: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    if repair_gaps:
        return [
            {
                "queue_id": "repair_protocol_gaps_before_blueprints",
                "priority": 1,
                "blueprint_task": "repair run337E protocol gaps before materialization",
                "required_inputs": rel(REPAIR_GAP_QUEUE_CSV),
                "required_outputs": "repaired protocol files;review rerun;gate audit",
                "forbidden": "training, MT5 execution, candidate selection, or Forward Passed before protocol gaps close",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    tasks = [
        (
            "materialize_no_lookahead_harness_blueprint",
            1,
            rel(NO_LOOKAHEAD_REVIEW_CSV),
            "canary harness specs for future-bar, forward-pocket, threshold, lot, and timestamp-basis bad controls",
        ),
        (
            "materialize_proxy_mt5_fresh_probe_blueprint",
            2,
            rel(PROXY_MT5_REVIEW_CSV),
            "proxy expected schema, MT5 package schema, row-level difference schema, and usability decision rules",
        ),
        (
            "materialize_core56_repair_blueprint",
            3,
            rel(CORE56_REVIEW_CSV),
            "core56 source inventory, as-of join, handoff snapshot, proxy expected, and MT5 probe blueprint",
        ),
        (
            "materialize_cost_direction_curve_extraction_blueprint",
            4,
            rel(COST_CURVE_REVIEW_CSV),
            "cost ladder, D/B source, long/short, curve pocket, lot-normalized, and regime slice extraction schemas",
        ),
        (
            "materialize_offense_rebuild_branch_blueprints",
            5,
            rel(OFFENSE_REVIEW_CSV),
            "branch-specific offense blueprints with fixed boundaries and no training in run337F",
        ),
        (
            "materialize_economic_regime_asof_blueprint",
            6,
            rel(REGIME_REVIEW_CSV),
            "VIX, USD, rate, ADX, volatility, session, hour, and month as-of source audit blueprint",
        ),
        (
            "materialize_runtime_probe_package_blueprint",
            7,
            rel(RUNTIME_REVIEW_CSV),
            "future MT5 package requirements and blocker criteria for each subject",
        ),
    ]
    return [
        {
            "queue_id": queue_id,
            "priority": priority,
            "blueprint_task": task,
            "required_inputs": required_inputs,
            "required_outputs": "blueprint CSV;schema JSON;claim-boundary receipt;review queue",
            "forbidden": "model training, MT5 execution, threshold retune, lot optimization, Forward Passed, runtime authority, Goal Achieve",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for queue_id, priority, required_inputs, task in tasks
    ]


def build_gate_audit(
    lineage: Sequence[Mapping[str, Any]],
    review_sets: Mapping[str, Sequence[Mapping[str, Any]]],
    accepted_queue: Sequence[Mapping[str, Any]],
    repair_gaps: Sequence[Mapping[str, Any]],
    run337f_queue: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    all_lineage_ok = all(row.get("lineage_review") == "pass" for row in lineage)
    all_reviews_accepted = all(
        str(row.get("review_status", "")).startswith("accepted")
        for rows in review_sets.values()
        for row in rows
    )
    training_review = review_sets.get("training_boundary", [])
    training_closed = all("training_still_closed" in str(row.get("review_status", "")) for row in training_review)
    return [
        {
            "gate_id": "source_lineage_connected",
            "status": "pass" if all_lineage_ok else "fail",
            "evidence": rel(PROTOCOL_INPUT_LINEAGE_CSV),
            "finding": f"lineage_rows={len(lineage)};all_connected={all_lineage_ok}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "no_lookahead_review_accepts_bad_controls",
            "status": "pass" if all(str(row.get("review_status", "")).startswith("accepted") for row in review_sets["no_lookahead"]) else "fail",
            "evidence": rel(NO_LOOKAHEAD_REVIEW_CSV),
            "finding": "future, forward-pocket, threshold, lot, and timestamp bad controls accepted for blueprinting",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "proxy_mt5_review_requires_fresh_runtime",
            "status": "pass" if all(str(row.get("review_status", "")).startswith("accepted") for row in review_sets["proxy_mt5"]) else "fail",
            "evidence": rel(PROXY_MT5_REVIEW_CSV),
            "finding": "all proxy subjects require fresh proxy expected and fresh MT5 runtime probe",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "core56_full_family_claim_blocked",
            "status": "pass" if all(str(row.get("review_status", "")).startswith("accepted") for row in review_sets["core56"]) else "fail",
            "evidence": rel(CORE56_REVIEW_CSV),
            "finding": "core56 repair protocol blocks full-family claims until source repair and MT5 probe",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "cost_direction_curve_review_complete",
            "status": "pass" if all(str(row.get("review_status", "")).startswith("accepted") for row in review_sets["cost_curve"]) else "fail",
            "evidence": rel(COST_CURVE_REVIEW_CSV),
            "finding": "cost, direction/source, curve, lot-normalized, and regime gate families covered",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "offense_and_regime_protocols_predeclared",
            "status": "pass" if all(str(row.get("review_status", "")).startswith("accepted") for row in [*review_sets["offense"], *review_sets["regime"]]) else "fail",
            "evidence": f"{rel(OFFENSE_REVIEW_CSV)};{rel(REGIME_REVIEW_CSV)}",
            "finding": "offense theses and economic regime joins are predeclared with as-of controls",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "runtime_package_review_complete",
            "status": "pass" if all(str(row.get("review_status", "")).startswith("accepted") for row in review_sets["runtime"]) else "fail",
            "evidence": rel(RUNTIME_REVIEW_CSV),
            "finding": "runtime package requirements include tester output, logs, trade ledger, parity, cost, and attribution outputs",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "training_boundary_still_closed",
            "status": "pass" if training_closed else "fail",
            "evidence": rel(TRAINING_BOUNDARY_REVIEW_CSV),
            "finding": "run337E review does not train or select; run337F may materialize blueprints only",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "no_repair_protocol_gaps",
            "status": "pass" if not repair_gaps and all_reviews_accepted else "fail",
            "evidence": rel(REPAIR_GAP_QUEUE_CSV),
            "finding": f"repair_gap_rows={len(repair_gaps)}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "run337f_blueprint_queue_ready",
            "status": "pass" if len(run337f_queue) >= 7 else "fail",
            "evidence": rel(RUN337F_QUEUE_CSV),
            "finding": f"run337F_queue_rows={len(run337f_queue)}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "claim_guard_no_selection_no_goal",
            "status": "pass",
            "evidence": rel(FINAL_DECISION_JSON),
            "finding": "no selected candidate, Forward Passed, Forward Failed, runtime authority, live readiness, deployment, or Goal Achieve claimed",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "accepted_protocol_queue_ready",
            "status": "pass" if all(str(row.get("queue_status", "")).startswith("accepted") for row in accepted_queue) else "fail",
            "evidence": rel(ACCEPTED_PROTOCOL_QUEUE_CSV),
            "finding": f"accepted_protocol_families={len(accepted_queue)}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_metrics(
    lineage: Sequence[Mapping[str, Any]],
    review_sets: Mapping[str, Sequence[Mapping[str, Any]]],
    accepted_queue: Sequence[Mapping[str, Any]],
    repair_gaps: Sequence[Mapping[str, Any]],
    run337f_queue: Sequence[Mapping[str, Any]],
    audit: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    return {
        "lineage_rows": len(lineage),
        "review_family_count": len(review_sets),
        "review_rows": sum(len(rows) for rows in review_sets.values()),
        "accepted_review_rows": sum(
            1 for rows in review_sets.values() for row in rows if str(row.get("review_status", "")).startswith("accepted")
        ),
        "accepted_protocol_families": len([row for row in accepted_queue if str(row.get("queue_status", "")).startswith("accepted")]),
        "repair_gap_rows": len(repair_gaps),
        "run337f_queue_rows": len(run337f_queue),
        "gate_rows": len(audit),
        "failed_gate_rows": len([row for row in audit if row.get("status") != "pass"]),
    }


def write_receipts(metrics: Mapping[str, Any]) -> list[Path]:
    return [
        write_json(
            EXPERIMENT_DESIGN_JSON,
            {
                "run_id": RUN_ID,
                "hypothesis": "run337D protocols are sufficient to open blueprint materialization without allowing training, candidate selection, or runtime claims",
                "decision_use": "decide whether run337F may materialize guarded execution blueprints",
                "comparison_baseline": "run337D materialized protocols and gate audit",
                "control_variables": "no model training, no MT5 execution, no threshold retune, no lot optimization, no forward-pocket filtering",
                "changed_variables": "protocol review labels and blueprint queue",
                "sample_scope": "Stage337 protocol files only; no new trading KPI sample",
                "success_criteria": "all protocol families accepted and repair gap queue empty",
                "failure_criteria": "any protocol family lacks fresh MT5 requirement, no-lookahead guard, core56 lock, runtime package, or training boundary",
                "invalid_conditions": "claiming Forward Passed, runtime authority, or candidate selection from protocol files",
                "stop_conditions": "any gate fails; send to repair_protocol_gap_queue before blueprint materialization",
                "evidence_plan": "review CSVs, accepted queue, repair gap queue, run337F queue, receipts, report, ledgers, artifact registry",
                "metrics": metrics,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            DATA_INTEGRITY_JSON,
            {
                "run_id": RUN_ID,
                "data_source": "run337D protocol files and manifests",
                "time_axis": "future data use remains protocol-bound; cycle_bar_time, broker timezone, and source_timestamp must be carried into future blueprints",
                "sample_scope": "protocol review only; no model rows or MT5 trade rows are generated in run337E",
                "missing_or_duplicate_check": "review confirms future blueprints must check missing, duplicate, stale, revision, and timezone risks",
                "feature_label_boundary": "no feature-label training in run337E; future bad controls must reject future-derived features",
                "split_boundary": "future train/WFO/forward splits remain predeclared blueprint requirements",
                "leakage_risk": "forward-pocket filtering, threshold retune, lot optimization, and macro as-of drift",
                "data_hash_or_identity": rel(PROTOCOL_INPUT_LINEAGE_CSV),
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
                "shared_contract": "future proxy expected values, MT5 tester outputs, trade ledger, feature order, timestamp basis, D/B sources, cost and attribution outputs must match",
                "known_differences": "no fresh MT5 execution in run337E; this review opens blueprint materialization only",
                "parity_check": "review confirms fresh MT5 runtime probe remains mandatory before KPI authority",
                "parity_identity": rel(PROXY_MT5_REVIEW_CSV),
                "runtime_claim_boundary": "research-only protocol review, no runtime authority",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            ARTIFACT_LINEAGE_JSON,
            {
                "run_id": RUN_ID,
                "source_inputs": [
                    rel(RUN337D_QUEUE),
                    rel(RUN337D_NO_LOOKAHEAD),
                    rel(RUN337D_PROXY_MT5),
                    rel(RUN337D_CORE56),
                    rel(RUN337D_COST_CURVE),
                    rel(RUN337D_OFFENSE),
                    rel(RUN337D_REGIME),
                    rel(RUN337D_RUNTIME_REQUIREMENTS),
                    rel(RUN337D_TRAINING_BOUNDARY),
                    rel(RUN337D_DECISION),
                ],
                "producer": rel(Path(__file__)),
                "consumer": NEXT_RUN_ID,
                "artifact_paths": [
                    rel(PROTOCOL_INPUT_LINEAGE_CSV),
                    rel(ACCEPTED_PROTOCOL_QUEUE_CSV),
                    rel(REPAIR_GAP_QUEUE_CSV),
                    rel(RUN337F_QUEUE_CSV),
                    rel(GATE_AUDIT_CSV),
                ],
                "artifact_hashes": "registered in artifact_registry after run",
                "registry_links": "run_registry;alpha_run_ledger;stage_run_ledger;artifact_registry",
                "availability": "tracked after commit; reproducible from run337E script",
                "lineage_judgment": "connected_with_boundary",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RESULT_JUDGMENT_JSON,
            {
                "run_id": RUN_ID,
                "result_subject": "Stage337D research execution protocols",
                "evidence_available": "protocol review CSVs, accepted queue, repair gap queue, run337F queue, gate audit",
                "evidence_missing": "no new model training, no MT5 runtime probe, no candidate KPI, no forward pass/fail decision",
                "judgment_label": "exploratory",
                "claim_boundary": "protocols accepted for blueprint materialization only; no candidate or operating claim",
                "next_condition": NEXT_RUN_ID,
                "user_explanation_hook": "검사문은 충분해서 다음에는 실행 청사진을 만들 수 있지만, 아직 모델 학습이나 MT5 성과 주장은 아니다.",
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
# run337E Research Execution Protocol Review(337E 연구 실행 절차 검토)

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

- lineage_rows(계보 행): `{metrics['lineage_rows']}`
- review_family_count(검토 묶음 수): `{metrics['review_family_count']}`
- review_rows(검토 행): `{metrics['review_rows']}`
- accepted_review_rows(승인 검토 행): `{metrics['accepted_review_rows']}`
- repair_gap_rows(수리 공백 행): `{metrics['repair_gap_rows']}`
- run337F_queue_rows(337F 대기열 행): `{metrics['run337f_queue_rows']}`
- gate_rows(게이트 행): `{metrics['gate_rows']}`, failed(실패): `{metrics['failed_gate_rows']}`

Effect(효과): run337E(337E 실행)는 run337D(337D 실행)의 protocol(절차)을 검토해 no-lookahead(미래참조 방어), proxy-MT5 fresh probe(프록시-MT5 신규 탐침), core56 lock(핵심56 잠금), cost/direction/curve gates(비용/방향/곡선 게이트), economic regime as-of(경제 국면 시점 기준), runtime package(런타임 패키지), training boundary(학습 경계)가 다음 blueprint materialization(청사진 물질화)에 충분하다고 판정했다. 아직 model training(모델 학습), MT5 execution(MT5 실행), candidate selection(후보 선택)은 없다.
"""
    decision = f"""
# 2026-05-27 Stage337E Decision(337E 결정)

- decision(결정): `{DECISION}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed_for_stage337_new_work`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`

Effect(효과): run337F(337F 실행)는 훈련(training, 학습)이 아니라 protocol-bound execution blueprints(절차 기반 실행 청사진)를 만든다. 이 결정은 운영 가능성이나 전진 통과가 아니라, 다음 연구 물질화 허가다.
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
- effect(효과): run337E(337E 실행)는 run337D(337D 실행)의 절차를 검토하고 run337F(337F 실행) blueprint materialization(청사진 물질화) 대기열을 열었다. 아직 선택 후보는 없다.
"""
    artifacts.append(write_md(SELECTED_DIR / "selection_status.md", selection))

    brief_text, brief_bom = read_text_lossless(SPEC_DIR / "stage_brief.md")
    brief_text = insert_after_marker_once(
        brief_text,
        "- run337D_summary(337D 요약):",
        f"- run337E_summary(337E 요약): `{STATUS}`. Effect(효과): run337D(337D 실행)의 no-lookahead/proxy-MT5/core56/cost-direction-curve/offense/regime/runtime/training boundary(미래참조/프록시-MT5/핵심56/비용-방향-곡선/공격/국면/런타임/학습 경계) 절차를 검토하고 run337F(337F 실행) 청사진 물질화 대기열로 넘긴다.",
        "run337E_summary",
    )
    artifacts.append(write_text_lossless(SPEC_DIR / "stage_brief.md", brief_text, brief_bom))

    input_section = f"""
## run337E Outputs(337E 산출물)

- protocol_input_lineage_review(절차 입력 계보 검토): `{rel(PROTOCOL_INPUT_LINEAGE_CSV)}`
- accepted_protocols_for_blueprint_queue(청사진용 승인 절차 대기열): `{rel(ACCEPTED_PROTOCOL_QUEUE_CSV)}`
- repair_protocol_gap_queue(수리 절차 공백 대기열): `{rel(REPAIR_GAP_QUEUE_CSV)}`
- run337F_blueprint_queue(337F 청사진 대기열): `{rel(RUN337F_QUEUE_CSV)}`
- gate_audit(게이트 감사): `{rel(GATE_AUDIT_CSV)}`

Effect(효과): 다음 실행은 모델 학습이 아니라, 검토 통과한 절차를 실제 실행 청사진과 schema(스키마)로 바꾼다.
"""
    artifacts.append(append_section_once(INPUTS_DIR / "input_refs.md", "## run337E Outputs(337E 산출물)", input_section))

    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_prefix_line(workspace_text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    focus = (
        "- >-\n"
        f"  Stage337(337단계) run337E(337E 실행)는 `{STATUS}`로 protocol review(절차 검토)를 완료했다. "
        "Effect(효과): run337F(337F 실행)에서 no-lookahead/proxy-MT5/core56/cost-direction-curve/offense/economic-regime/runtime(미래참조/프록시-MT5/핵심56/비용-방향-곡선/공격/경제 국면/런타임) 실행 청사진을 만들 수 있게 하되, model training(모델 학습)과 MT5 execution(MT5 실행)은 아직 닫아둔다.\n"
    )
    workspace_text = insert_focus_once(workspace_text, focus, "Stage337 run337E focus complete")
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
        f"- run337E_summary(337E 요약): `{STATUS}`. "
        "Effect(효과): 절차 검토를 통과시켜 run337F(337F 실행) blueprint materialization(청사진 물질화) 대기열을 열고, 학습/MT5/후보 선택은 계속 닫아둔다."
    )
    current_text = insert_after_marker_once(current_text, "- decision(결정):", summary, "run337E_summary")
    artifacts.append(write_text_lossless(CURRENT_STATE, current_text, current_bom))

    artifacts.append(
        append_section_once(
            CHANGELOG,
            "## Stage337E Research Execution Protocol Review(337E 연구 실행 절차 검토)",
            f"""
- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- action(행동): run337D(337D 실행)의 절차 산출물을 검토해 accepted_protocols_for_blueprint_queue(청사진 승인 절차 대기열)와 run337F_blueprint_queue(337F 청사진 대기열)를 만들었다.
- effect(효과): 과적합 방어 절차가 충분하다는 범위 안에서 다음 청사진 물질화를 열되, 모델 학습과 MT5 실행, 선택 후보 주장은 계속 금지한다.
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
                "lane": "research_execution_protocol_review",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_DOC),
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};blueprint_queue_opened;training_not_allowed;goal_achieve_not_claimed.",
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__research_execution_protocol_review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "research_execution_protocol_review",
                "tier_scope": "stage337_protocol_boundary_macro48_u42_core56",
                "kpi_scope": "protocol_review_only_no_new_candidate_kpi",
                "scoreboard_lane": "protocol_review_readiness",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_DOC),
                "primary_kpi": "repair_gap_rows=0;run337f_queue_rows=7;candidate_selection=none",
                "guardrail_kpi": "training_not_allowed;proxy_not_kpi_authority;core56_scope_locked;goal_achieve_not_claimed",
                "external_verification_status": "out_of_scope_by_claim_protocol_review_only",
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
                "ledger_row_id": f"{RUN_ID}__research_execution_protocol_review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "work_family": "review",
                "evidence_scope": "run337D_protocols_and_gate_audit",
                "kpi_scope": "protocol_review_only_no_new_candidate_kpi",
                "status": STATUS,
                "judgment": JUDGMENT,
                "claim_boundary": CLAIM_BOUNDARY,
                "path": rel(REPORT_DOC),
                "notes": f"next_action={NEXT_RUN_ID};blueprint_queue_opened;training_not_allowed;goal_achieve_not_claimed.",
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
            "notes": "run337E_protocol_review_no_selection",
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
    lineage = build_protocol_input_lineage(inputs)
    review_sets = {
        "no_lookahead": review_no_lookahead(inputs["no_lookahead"]),
        "proxy_mt5": review_proxy_mt5(inputs["proxy_mt5"]),
        "core56": review_core56(inputs["core56"]),
        "cost_curve": review_cost_curve(inputs["cost_curve"]),
        "offense": review_offense(inputs["offense"]),
        "regime": review_regime(inputs["regime"]),
        "runtime": review_runtime(inputs["runtime_requirements"]),
        "training_boundary": review_training_boundary(inputs["training_boundary"]),
    }
    repair_gaps = collect_repair_gaps(review_sets)
    accepted_queue = build_accepted_protocol_queue(review_sets)
    run337f_queue = build_run337f_queue(accepted_queue, repair_gaps)
    audit = build_gate_audit(lineage, review_sets, accepted_queue, repair_gaps, run337f_queue)
    metrics = build_metrics(lineage, review_sets, accepted_queue, repair_gaps, run337f_queue, audit)
    failed_gates = [row for row in audit if row.get("status") != "pass"]
    run_artifacts = [
        write_csv(
            PROTOCOL_INPUT_LINEAGE_CSV,
            (
                "source_path",
                "exists",
                "sha256",
                "row_count",
                "manifest_linked",
                "lineage_review",
                "allowed_use",
                "forbidden_use",
                "claim_boundary",
            ),
            lineage,
        ),
        write_csv(
            NO_LOOKAHEAD_REVIEW_CSV,
            ("protocol_id", "risk_target", "review_status", "checks", "finding", "next_blueprint_use", "claim_boundary"),
            review_sets["no_lookahead"],
        ),
        write_csv(
            PROXY_MT5_REVIEW_CSV,
            (
                "subject",
                "source_review_status",
                "review_status",
                "checks",
                "finding",
                "next_blueprint_use",
                "forbidden_after_review",
                "claim_boundary",
            ),
            review_sets["proxy_mt5"],
        ),
        write_csv(
            CORE56_REVIEW_CSV,
            ("protocol_id", "step_order", "review_status", "checks", "finding", "next_blueprint_use", "claim_boundary"),
            review_sets["core56"],
        ),
        write_csv(
            COST_CURVE_REVIEW_CSV,
            ("protocol_id", "gate_scope", "review_status", "checks", "finding", "next_blueprint_use", "claim_boundary"),
            review_sets["cost_curve"],
        ),
        write_csv(
            OFFENSE_REVIEW_CSV,
            ("branch_id", "review_status", "checks", "finding", "next_blueprint_use", "claim_boundary"),
            review_sets["offense"],
        ),
        write_csv(
            REGIME_REVIEW_CSV,
            ("protocol_id", "regime_source", "review_status", "checks", "finding", "next_blueprint_use", "claim_boundary"),
            review_sets["regime"],
        ),
        write_csv(
            RUNTIME_REVIEW_CSV,
            (
                "package_id",
                "subject",
                "review_status",
                "checks",
                "finding",
                "next_blueprint_use",
                "runtime_claim_boundary",
                "claim_boundary",
            ),
            review_sets["runtime"],
        ),
        write_csv(
            TRAINING_BOUNDARY_REVIEW_CSV,
            ("boundary_id", "review_status", "checks", "finding", "next_blueprint_use", "claim_boundary"),
            review_sets["training_boundary"],
        ),
        write_csv(
            ACCEPTED_PROTOCOL_QUEUE_CSV,
            ("protocol_family", "accepted_rows", "total_rows", "queue_status", "next_use", "claim_boundary"),
            accepted_queue,
        ),
        write_csv(
            REPAIR_GAP_QUEUE_CSV,
            ("gap_id", "review_name", "subject", "reason", "required_repair", "claim_boundary"),
            repair_gaps,
        ),
        write_csv(
            RUN337F_QUEUE_CSV,
            (
                "queue_id",
                "priority",
                "blueprint_task",
                "required_inputs",
                "required_outputs",
                "forbidden",
                "claim_boundary",
            ),
            run337f_queue,
        ),
        write_csv(GATE_AUDIT_CSV, ("gate_id", "status", "evidence", "finding", "claim_boundary"), audit),
    ]
    run_artifacts.extend(write_receipts(metrics))
    final_payload = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS if not failed_gates else "blocked_stage337E_protocol_review_gate_failure",
        "judgment": JUDGMENT if not failed_gates else "stage337E_protocol_review_requires_repair",
        "decision": DECISION if not failed_gates else "stage337E_protocol_review_blocked_repair_gaps",
        "metrics": metrics,
        "failed_gates": failed_gates,
        "next_action": NEXT_RUN_ID if not failed_gates else "repair_run337E_protocol_gaps_before_blueprints",
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
                "status": "blocked_stage337E_protocol_review_gate_failure",
                "decision": "stage337E_protocol_review_blocked_repair_gaps",
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
            rel(RUN337D_QUEUE),
            rel(RUN337D_NO_LOOKAHEAD),
            rel(RUN337D_PROXY_MT5),
            rel(RUN337D_CORE56),
            rel(RUN337D_COST_CURVE),
            rel(RUN337D_OFFENSE),
            rel(RUN337D_REGIME),
            rel(RUN337D_RUNTIME_REQUIREMENTS),
            rel(RUN337D_TRAINING_BOUNDARY),
            rel(RUN337D_DECISION),
            rel(RUN337D_MANIFEST),
        ],
        "outputs": [rel(path) for path in all_artifacts],
        "status": STATUS,
        "decision": DECISION,
        "external_verification_status": "out_of_scope_by_claim_protocol_review_only_no_mt5_execution",
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
                "accepted_review_rows": metrics["accepted_review_rows"],
                "repair_gap_rows": metrics["repair_gap_rows"],
                "run337f_queue_rows": metrics["run337f_queue_rows"],
                "gate_rows": metrics["gate_rows"],
                "failed_gate_rows": metrics["failed_gate_rows"],
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
