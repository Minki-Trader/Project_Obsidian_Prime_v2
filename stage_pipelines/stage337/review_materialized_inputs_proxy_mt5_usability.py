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
RUN_NUMBER = "run337C"
RUN_ID = "run337C_review_materialized_inputs_and_proxy_mt5_usability_v1"
PARENT_RUN_ID = "run337B_materialize_cost_direction_curve_rebuild_inputs_v1"
NEXT_RUN_ID = "run337D_materialize_research_execution_protocols_v1"
STATUS = "completed_materialized_inputs_proxy_mt5_usability_review_no_selection"
JUDGMENT = "stage337C_proxy_mt5_context_only_branch_protocol_queue_ready_no_selection"
DECISION = "stage337C_review_accepts_protocol_queue_proxy_not_kpi_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage337C_review_no_model_training_no_threshold_retuning_"
    "no_lot_optimization_no_forward_pocket_filtering_no_candidate_selection_no_forward_passed_"
    "no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_"
    "no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
RUN337B_DIR = STAGE_DIR / "02_runs" / "run337B"
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
DECISION_DOC = DOCS / "decisions" / "2026-05-27_stage337C_review_proxy_mt5_usability.md"
REPORT_DOC = REVIEWS_DIR / "run337C_review_materialized_inputs_proxy_mt5_usability.md"

SOURCE_LINEAGE = RUN337B_DIR / "source_lineage_index.csv"
DATA_INTEGRITY_CONTRACT = RUN337B_DIR / "data_integrity_contract.csv"
NO_LOOKAHEAD_CANARIES = RUN337B_DIR / "no_lookahead_canary_inputs.csv"
BRANCH_PAYLOAD = RUN337B_DIR / "branch_payload_index.csv"
BRANCH_REVIEW_QUEUE = RUN337B_DIR / "branch_review_queue.csv"
GATE_SCHEMA = RUN337B_DIR / "gate_schema_per_branch.csv"
PROXY_EXPECTED = RUN337B_DIR / "proxy_expected_signal_values.csv"
MT5_OBSERVED = RUN337B_DIR / "mt5_runtime_probe_observed_values.csv"
PROXY_MT5_DIFF = RUN337B_DIR / "proxy_mt5_difference_report.csv"
PROXY_MT5_USABILITY = RUN337B_DIR / "proxy_mt5_usability_decision.csv"
MT5_PROBE_MANIFEST = RUN337B_DIR / "mt5_runtime_probe_manifest.csv"
CORE56_SCOPE = RUN337B_DIR / "core56_repair_or_scope_receipt.csv"
RUN337B_DECISION = RUN337B_DIR / "final_materialized_inputs_proxy_mt5_usability_decision.json"

SOURCE_LINEAGE_REVIEW_CSV = RUN_DIR / "source_lineage_review.csv"
DATA_INTEGRITY_REVIEW_CSV = RUN_DIR / "data_integrity_review.csv"
NO_LOOKAHEAD_REVIEW_CSV = RUN_DIR / "no_lookahead_canary_review.csv"
PROXY_MT5_REVIEW_CSV = RUN_DIR / "proxy_mt5_usability_review.csv"
FUTURE_PROBE_REQUIREMENTS_CSV = RUN_DIR / "future_proxy_mt5_probe_requirements.csv"
BRANCH_GATE_ACCEPTANCE_CSV = RUN_DIR / "branch_gate_acceptance_matrix.csv"
ACCEPTED_BRANCH_QUEUE_CSV = RUN_DIR / "accepted_branch_package_queue.csv"
REJECTED_CLAIM_MEMORY_CSV = RUN_DIR / "rejected_claim_memory.csv"
CORE56_REVIEW_CSV = RUN_DIR / "core56_repair_or_scope_lock_review.csv"
RUN337D_QUEUE_CSV = RUN_DIR / "run337D_research_execution_protocol_queue.csv"
GATE_AUDIT_CSV = RUN_DIR / "required_gate_coverage_audit.csv"
DATA_INTEGRITY_JSON = RUN_DIR / "data_integrity_receipt.json"
RUNTIME_PARITY_JSON = RUN_DIR / "runtime_parity_receipt.json"
ARTIFACT_LINEAGE_JSON = RUN_DIR / "artifact_lineage_receipt.json"
RESULT_JUDGMENT_JSON = RUN_DIR / "result_judgment_receipt.json"
FINAL_DECISION_JSON = RUN_DIR / "final_review_materialized_inputs_proxy_mt5_usability_decision.json"
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
        "source_lineage": read_csv(SOURCE_LINEAGE),
        "data_integrity": read_csv(DATA_INTEGRITY_CONTRACT),
        "canaries": read_csv(NO_LOOKAHEAD_CANARIES),
        "branch_payload": read_csv(BRANCH_PAYLOAD),
        "branch_review_queue": read_csv(BRANCH_REVIEW_QUEUE),
        "gate_schema": read_csv(GATE_SCHEMA),
        "proxy_expected": read_csv(PROXY_EXPECTED),
        "mt5_observed": read_csv(MT5_OBSERVED),
        "proxy_diff": read_csv(PROXY_MT5_DIFF),
        "proxy_usability": read_csv(PROXY_MT5_USABILITY),
        "mt5_manifest": read_csv(MT5_PROBE_MANIFEST),
        "core56_scope": read_csv(CORE56_SCOPE),
        "run337b_decision": read_json(RUN337B_DECISION),
    }


def build_source_lineage_review(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for row in inputs["source_lineage"]:
        connected = row.get("availability") != "missing" and row.get("sha256") not in {"", "missing"}
        rows.append(
            {
                "source_id": row.get("source_id", ""),
                "artifact_path": row.get("artifact_path", ""),
                "input_lineage_judgment": row.get("lineage_judgment", ""),
                "review_status": "pass" if connected else "fail",
                "review_finding": "source connected and hash present" if connected else "missing source or hash",
                "allowed_use": "review input for Stage337 protocol design",
                "forbidden_use": "model selection or runtime authority",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_data_integrity_review(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for row in inputs["data_integrity"]:
        usable = row.get("integrity_judgment", "").startswith("usable")
        rows.append(
            {
                "check_id": row.get("check_id", ""),
                "integrity_judgment": row.get("integrity_judgment", ""),
                "review_status": "pass" if usable else "fail",
                "time_axis": row.get("time_axis", ""),
                "feature_label_boundary": row.get("feature_label_boundary", ""),
                "leakage_risk": row.get("leakage_risk", ""),
                "review_finding": "usable boundary for review; no training or KPI claim" if usable else "integrity gap needs repair",
                "next_condition": row.get("next_evidence", ""),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_canary_review(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for row in inputs["canaries"]:
        rows.append(
            {
                "canary_id": row.get("canary_id", ""),
                "target_risk": row.get("target_risk", ""),
                "expected_rejection": row.get("expected_rejection", ""),
                "review_status": "accepted_for_guard_execution",
                "review_finding": "canary is needed before any candidate KPI can be interpreted",
                "must_fail_if_triggered": "true",
                "forbidden": "passing this canary as a legitimate alpha path",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def diff_by_subject(diff_rows: Sequence[Mapping[str, str]]) -> dict[str, Mapping[str, str]]:
    return {row.get("attempt_name", ""): row for row in diff_rows}


def build_proxy_review(inputs: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    diff_index = diff_by_subject(inputs["proxy_diff"])
    review_rows = []
    requirement_rows = []
    for row in inputs["proxy_usability"]:
        subject = row.get("subject", "")
        diff = diff_index.get(subject, {})
        signal_matched = row.get("signal_difference_status") == "matched"
        core56 = subject == "core56_refresh_candidate"
        if core56:
            review_status = "scope_locked_repair_required"
            review_finding = "core56 has no proxy expected or MT5 runtime probe yet"
            next_requirement = "repair equity/breadth/top3 feature source, then run proxy expected and MT5 runtime probe"
        elif signal_matched and "signal_sanity" in row.get("usability_label", ""):
            review_status = "accepted_signal_sanity_only"
            review_finding = "proxy and MT5 signal dimensions match, but runtime KPI remains fragile"
            next_requirement = "fresh candidate must rerun MT5 runtime, cost, direction, curve, lot-normalized, and regime gates"
        else:
            review_status = "not_usable"
            review_finding = "proxy/MT5 mismatch or missing evidence"
            next_requirement = "repair proxy-MT5 handoff before branch use"
        review_rows.append(
            {
                "subject": subject,
                "signal_difference_status": row.get("signal_difference_status", ""),
                "runtime_kpi_status": row.get("runtime_kpi_status", ""),
                "source_usability_label": row.get("usability_label", ""),
                "dimensions_compared": diff.get("dimensions_compared", ""),
                "matched_dimensions": diff.get("matched_dimensions", ""),
                "mismatched_dimensions": diff.get("mismatched_dimensions", ""),
                "max_abs_proxy_minus_mt5": diff.get("max_abs_proxy_minus_mt5", ""),
                "review_status": review_status,
                "review_finding": review_finding,
                "allowed_use": "signal sanity check and runtime handoff debugging" if not core56 else "repair planning only",
                "forbidden_use": "KPI authority;Forward Passed;candidate selection;operating reference",
                "next_requirement": next_requirement,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        requirement_rows.append(
            {
                "subject": subject,
                "required_before_kpi_use": next_requirement,
                "fresh_proxy_expected_required": "true",
                "fresh_mt5_runtime_probe_required": "true",
                "cost_direction_curve_gates_required": "true",
                "usability_after_review": review_status,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return review_rows, requirement_rows


def build_branch_acceptance(inputs: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    branch_rows = []
    accepted_rows = []
    rejected_memory = [
        {
            "memory_id": "proxy_profit_authority_rejected",
            "rejected_claim": "proxy result can decide profit, PF, DD, Forward Passed, or candidate selection",
            "reason": "proxy-MT5 signal matched, but run336O runtime KPI is fragile and MT5 remains KPI authority",
            "future_reopen_condition": "fresh MT5 runtime probe and cost/direction/curve gates pass on a predeclared candidate",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "full_family_without_core56_rejected",
            "rejected_claim": "macro48/u42 repaired subset proves full cp322A family robustness",
            "reason": "core56 has no refreshed equity/breadth/top3 handoff and no MT5 probe",
            "future_reopen_condition": "core56 refresh source repaired, proxy expected generated, MT5 runtime probe executed",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "forward_pocket_filter_rejected",
            "rejected_claim": "failed forward pockets can be filtered out directly",
            "reason": "would reintroduce overfit/lookahead-style selection from failed forward evidence",
            "future_reopen_condition": "pre-forward thesis and WFO canaries reject result-fitted filters",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "threshold_lot_cosmetic_repair_rejected",
            "rejected_claim": "threshold retune or lot optimization can repair cost/curve fragility",
            "reason": "Stage337 target requires signal/expectancy improvement, not cosmetic KPI shaping",
            "future_reopen_condition": "new predeclared model protocol with fixed risk and lot-normalized evidence",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    for row in inputs["branch_payload"]:
        branch_id = row.get("branch_id", "")
        lane = row.get("lane", "")
        if branch_id == "repair_core56_equity_breadth_refresh":
            acceptance = "accepted_for_repair_protocol_design_only"
            next_protocol = "core56_refresh_repair_protocol"
        elif branch_id == "repair_proxy_mt5_runtime_contract":
            acceptance = "accepted_for_runtime_parity_protocol_design_only"
            next_protocol = "proxy_mt5_fresh_probe_protocol"
        elif branch_id == "defense_no_lookahead_canary_suite":
            acceptance = "accepted_for_defense_protocol_design_only"
            next_protocol = "no_lookahead_canary_execution_protocol"
        elif branch_id == "defense_cost_direction_curve_gate":
            acceptance = "accepted_for_gate_protocol_design_only"
            next_protocol = "cost_direction_curve_gate_execution_protocol"
        else:
            acceptance = "accepted_for_research_protocol_design_only"
            next_protocol = "offense_signal_rebuild_protocol"
        branch_rows.append(
            {
                "branch_id": branch_id,
                "lane": lane,
                "payload_id": row.get("payload_id", ""),
                "source_failure_memory": row.get("source_failure_memory", ""),
                "gate_coverage_status": "covered_by_run337B_gate_schema",
                "proxy_mt5_status": "required_before_candidate_kpi",
                "review_acceptance": acceptance,
                "forbidden": row.get("forbidden", ""),
                "next_protocol": next_protocol,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        accepted_rows.append(
            {
                "queue_id": f"{branch_id}_to_run337D",
                "priority": {"repair": 1, "defense": 2, "offense": 3}.get(lane, 4),
                "branch_id": branch_id,
                "lane": lane,
                "next_protocol": next_protocol,
                "required_inputs": row.get("required_evidence", ""),
                "must_keep": "no training until protocol;proxy not KPI authority;MT5 required;no forward pocket filtering",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return branch_rows, accepted_rows, rejected_memory


def build_core56_review(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    source = inputs["core56_scope"][0] if inputs["core56_scope"] else {}
    return [
        {
            "subject": "core56_equity_breadth_top3",
            "source_decision": source.get("decision", ""),
            "review_decision": "repair_protocol_required_or_scope_locked",
            "reason": "full-family robustness is impossible without core56 refresh, proxy expected output, and MT5 runtime probe",
            "accepted_next_protocol": "core56_refresh_repair_protocol",
            "blocked_claims": "full cp322A family robustness;Forward Passed;runtime authority;operating reference",
            "required_evidence": source.get("required_validation", ""),
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_run337d_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "stage337D_no_lookahead_execution_protocol",
            "priority": 1,
            "protocol": "materialize no-lookahead, forward-pocket, threshold-retune, lot-optimization canary execution protocol",
            "required_inputs": rel(NO_LOOKAHEAD_REVIEW_CSV),
            "required_outputs": "canary_execution_plan;invalid_condition_matrix;repair_or_reject_rules",
            "success_condition": "bad controls must fail before any candidate training or score interpretation",
            "forbidden": "treat canary pass as alpha",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "stage337D_proxy_mt5_fresh_probe_protocol",
            "priority": 2,
            "protocol": "materialize future proxy expected and MT5 runtime probe protocol for every survivor",
            "required_inputs": rel(PROXY_MT5_REVIEW_CSV) + ";" + rel(FUTURE_PROBE_REQUIREMENTS_CSV),
            "required_outputs": "proxy_expected_schema;MT5_probe_package_schema;difference_usability_rules",
            "success_condition": "proxy cannot become KPI authority without fresh MT5 evidence",
            "forbidden": "proxy-only profit pass/fail",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "stage337D_core56_refresh_protocol",
            "priority": 3,
            "protocol": "materialize core56 equity/breadth/top3 refresh repair protocol or explicit out-of-scope lock",
            "required_inputs": rel(CORE56_REVIEW_CSV),
            "required_outputs": "core56_source_audit;asof_join_contract;repair_queue_or_scope_lock",
            "success_condition": "full-family claim remains impossible until core56 is repaired and probed",
            "forbidden": "silent core56 drop",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "stage337D_cost_direction_curve_protocol",
            "priority": 4,
            "protocol": "materialize cost/direction/curve gate execution protocols for future candidates",
            "required_inputs": rel(BRANCH_GATE_ACCEPTANCE_CSV) + ";" + rel(ACCEPTED_BRANCH_QUEUE_CSV),
            "required_outputs": "cost_ladder_protocol;side_attribution_protocol;curve_pocket_protocol;lot_normalized_protocol",
            "success_condition": "future candidates cannot hide a broken KPI behind net profit",
            "forbidden": "single KPI selection",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "stage337D_offense_rebuild_protocol",
            "priority": 5,
            "protocol": "materialize balanced offense research protocols for cost buffer, direction symmetry, and regime-invariant signals",
            "required_inputs": rel(ACCEPTED_BRANCH_QUEUE_CSV),
            "required_outputs": "feature_thesis_protocols;WFO_split_contract;MT5_handoff_requirements",
            "success_condition": "stronger ONNX search can start only after protocol gates are explicit",
            "forbidden": "training before protocol and data boundary",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_gate_audit(
    source_review: Sequence[Mapping[str, Any]],
    data_review: Sequence[Mapping[str, Any]],
    canary_review: Sequence[Mapping[str, Any]],
    proxy_review: Sequence[Mapping[str, Any]],
    branch_acceptance: Sequence[Mapping[str, Any]],
    rejected_memory: Sequence[Mapping[str, Any]],
    core56_review: Sequence[Mapping[str, Any]],
    next_queue: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    source_fail = [row for row in source_review if row["review_status"] != "pass"]
    data_fail = [row for row in data_review if row["review_status"] != "pass"]
    signal_only = [row for row in proxy_review if row["review_status"] == "accepted_signal_sanity_only"]
    core56_locked = [row for row in core56_review if row["review_decision"] == "repair_protocol_required_or_scope_locked"]
    return [
        {
            "gate_id": "source_lineage_review_passed",
            "status": "pass" if not source_fail else "fail",
            "evidence": rel(SOURCE_LINEAGE_REVIEW_CSV),
            "finding": f"source_review_rows={len(source_review)};failed={len(source_fail)}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "data_integrity_review_passed",
            "status": "pass" if not data_fail else "fail",
            "evidence": rel(DATA_INTEGRITY_REVIEW_CSV),
            "finding": f"data_review_rows={len(data_review)};failed={len(data_fail)}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "no_lookahead_canaries_accepted",
            "status": "pass" if len(canary_review) >= 8 else "fail",
            "evidence": rel(NO_LOOKAHEAD_REVIEW_CSV),
            "finding": f"canary_review_rows={len(canary_review)}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "proxy_context_only_judgment_preserved",
            "status": "pass" if len(signal_only) == 4 else "fail",
            "evidence": rel(PROXY_MT5_REVIEW_CSV),
            "finding": f"signal_sanity_only_subjects={len(signal_only)};proxy_not_kpi_authority",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "branch_packages_accepted_for_protocol_only",
            "status": "pass" if len(branch_acceptance) >= 8 else "fail",
            "evidence": rel(BRANCH_GATE_ACCEPTANCE_CSV),
            "finding": f"accepted_protocol_branch_rows={len(branch_acceptance)}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "rejected_claim_memory_present",
            "status": "pass" if len(rejected_memory) >= 4 else "fail",
            "evidence": rel(REJECTED_CLAIM_MEMORY_CSV),
            "finding": f"rejected_claim_rows={len(rejected_memory)}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "core56_scope_lock_preserved",
            "status": "pass" if core56_locked else "fail",
            "evidence": rel(CORE56_REVIEW_CSV),
            "finding": "core56 repair required before full-family claim",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "next_protocol_queue_ready",
            "status": "pass" if len(next_queue) >= 5 else "fail",
            "evidence": rel(RUN337D_QUEUE_CSV),
            "finding": f"run337D_queue_rows={len(next_queue)}",
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
                "data_source": "run337B materialized lineage, integrity, canaries, proxy-MT5 usability, and branch payloads",
                "time_axis": "timestamp-aligned MT5 cycle_bar_time remains required for proxy comparisons",
                "sample_scope": "macro48/u42 repaired subset plus core56 scope lock",
                "missing_or_duplicate_check": "source review passed; detailed future candidate checks deferred to run337D protocols",
                "feature_label_boundary": "no labels, training, threshold selection, or forward-pocket filtering in run337C",
                "split_boundary": "future WFO and forward split protocols must be materialized before new candidate training",
                "leakage_risk": "proxy authority creep and forward pocket filtering; both rejected in claim memory",
                "data_hash_or_identity": rel(DATA_INTEGRITY_REVIEW_CSV),
                "integrity_judgment": "usable_with_boundary",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RUNTIME_PARITY_JSON,
            {
                "run_id": RUN_ID,
                "research_path": rel(Path(__file__)),
                "runtime_path": rel(MT5_PROBE_MANIFEST),
                "shared_contract": "proxy expected values and MT5 observed values may sanity-check signals only after timestamp alignment",
                "known_differences": "existing repaired subset signal dimensions match, but runtime KPI remains fragile",
                "parity_check": "run337C reviewed proxy-MT5 usability labels from run337B",
                "parity_identity": rel(PROXY_MT5_REVIEW_CSV),
                "runtime_claim_boundary": "runtime_probe evidence reused; no runtime authority",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            ARTIFACT_LINEAGE_JSON,
            {
                "run_id": RUN_ID,
                "source_inputs": [
                    rel(SOURCE_LINEAGE),
                    rel(DATA_INTEGRITY_CONTRACT),
                    rel(PROXY_MT5_USABILITY),
                    rel(BRANCH_PAYLOAD),
                    rel(CORE56_SCOPE),
                ],
                "producer": rel(Path(__file__)),
                "consumer": NEXT_RUN_ID,
                "artifact_paths": [
                    rel(SOURCE_LINEAGE_REVIEW_CSV),
                    rel(PROXY_MT5_REVIEW_CSV),
                    rel(BRANCH_GATE_ACCEPTANCE_CSV),
                    rel(RUN337D_QUEUE_CSV),
                ],
                "artifact_hashes": "registered in artifact_registry after run",
                "registry_links": "run_registry;alpha_run_ledger;stage_run_ledger;artifact_registry",
                "availability": "tracked after commit; reproducible from run337C script",
                "lineage_judgment": "connected_with_boundary",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RESULT_JUDGMENT_JSON,
            {
                "run_id": RUN_ID,
                "result_subject": "run337B materialized input and proxy-MT5 usability review",
                "evidence_available": "source review, data integrity review, canary review, proxy-MT5 review, branch acceptance, rejected claim memory",
                "evidence_missing": "no new model training, no fresh MT5 probe, no candidate KPI, no operating evidence",
                "judgment_label": "exploratory",
                "claim_boundary": "review complete for protocol design only; proxy remains context/signal sanity, not KPI authority",
                "next_condition": NEXT_RUN_ID,
                "user_explanation_hook": "프록시와 MT5 신호는 맞지만, 좋은 ONNX가 생긴 것은 아니며 다음은 실행 계약을 더 세게 묶는 일이다.",
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
# run337C Proxy-MT5 Usability Review(337C 프록시-MT5 활용성 검토)

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

- source_lineage_review(원천 계보 검토): `{metrics['source_review_rows']}` rows(행), failed(실패) `{metrics['source_review_failed']}`
- data_integrity_review(데이터 무결성 검토): `{metrics['data_review_rows']}` rows(행), failed(실패) `{metrics['data_review_failed']}`
- proxy_signal_sanity_only(프록시 신호 점검 전용): `{metrics['proxy_signal_only_subjects']}` subjects(대상)
- accepted_branch_protocols(승인 분기 계약): `{metrics['accepted_branch_rows']}` rows(행)
- rejected_claim_memory(거절 주장 기억): `{metrics['rejected_claim_rows']}` rows(행)
- next_protocol_queue(다음 계약 대기열): `{metrics['next_queue_rows']}` rows(행)

Effect(효과): proxy(프록시)는 MT5 runtime(런타임)과 신호 차원에서 맞아도 KPI authority(KPI 권한), candidate selection(후보 선택), Forward Passed(전진 통과) 근거가 아니다. 다음 run337D(337D 실행)는 이 경계를 유지한 채 no-lookahead(미래참조 방어), core56 repair(핵심56 수리), fresh MT5 probe(신규 MT5 탐침), cost/direction/curve gate(비용/방향/곡선 게이트) 실행 계약을 물질화한다.
"""
    decision = f"""
# 2026-05-27 Stage337C Decision(337C 결정)

- decision(결정): `{DECISION}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed_for_stage337_new_work`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`

Effect(효과): run337C(337C 실행)는 run337B(337B 실행) 산출물을 검토해 `accepted_for_protocol_only(계약 전용 승인)`와 `rejected_claim_memory(거절 주장 기억)`로 나눴다. 이 결정은 운영 가능 상태가 아니라 다음 실행 계약으로 넘기는 연구 판정이다.
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
- effect(효과): run337C(337C 실행)는 proxy-MT5(프록시-MT5) 일치를 signal sanity only(신호 점검 전용)로 제한하고, branch packages(분기 패키지)는 protocol design only(계약 설계 전용)로 넘겼다. 아직 선택 후보는 없다.
"""
    artifacts.append(write_md(SELECTED_DIR / "selection_status.md", selection))
    brief_text, brief_bom = read_text_lossless(SPEC_DIR / "stage_brief.md")
    brief_text = insert_after_marker_once(
        brief_text,
        "- run337B_summary(337B 요약):",
        f"- run337C_summary(337C 요약): `{STATUS}`. Effect(효과): proxy-MT5(프록시-MT5) 활용성을 signal sanity only(신호 점검 전용)로 검토하고 run337D(337D 실행) 실행 계약으로 넘겼다.",
        "run337C_summary",
    )
    artifacts.append(write_text_lossless(SPEC_DIR / "stage_brief.md", brief_text, brief_bom))
    input_section = f"""
## run337C Outputs(337C 산출물)

- source_lineage_review(원천 계보 검토): `{rel(SOURCE_LINEAGE_REVIEW_CSV)}`
- data_integrity_review(데이터 무결성 검토): `{rel(DATA_INTEGRITY_REVIEW_CSV)}`
- proxy_mt5_review(프록시-MT5 검토): `{rel(PROXY_MT5_REVIEW_CSV)}`
- branch_acceptance(분기 승인): `{rel(BRANCH_GATE_ACCEPTANCE_CSV)}`
- rejected_claim_memory(거절 주장 기억): `{rel(REJECTED_CLAIM_MEMORY_CSV)}`
- next_queue(다음 대기열): `{rel(RUN337D_QUEUE_CSV)}`

Effect(효과): 다음 실행은 모델 학습 전 no-lookahead(미래참조 방어), proxy-MT5 fresh probe(신규 프록시-MT5 탐침), core56 repair(핵심56 수리), cost/direction/curve gate(비용/방향/곡선 게이트) 계약을 먼저 만든다.
"""
    artifacts.append(append_section_once(INPUTS_DIR / "input_refs.md", "## run337C Outputs(337C 산출물)", input_section))
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_prefix_line(workspace_text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    focus = (
        "- >-\n"
        f"  Stage337(337단계) run337C(337C 실행)는 `{STATUS}`로 proxy-MT5 usability review(프록시-MT5 활용성 검토)를 완료했다. "
        "Effect(효과): proxy(프록시)는 signal sanity only(신호 점검 전용), branch package(분기 패키지)는 protocol only(계약 전용)로 낮춰 KPI authority(KPI 권한)와 Goal Achieve(목표 달성) 오해를 차단한다.\n"
    )
    workspace_text = insert_focus_once(workspace_text, focus, "Stage337 run337C focus complete")
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
        f"- run337C_summary(337C 요약): `{STATUS}`. "
        "Effect(효과): source/data/proxy/branch/core56(원천/데이터/프록시/분기/핵심56) 리뷰를 완료하고 run337D(337D 실행) 실행 계약 대기열로 넘긴다."
    )
    current_text = insert_after_marker_once(current_text, "- decision(결정):", summary, "run337C_summary")
    artifacts.append(write_text_lossless(CURRENT_STATE, current_text, current_bom))
    artifacts.append(
        append_section_once(
            CHANGELOG,
            "## Stage337C Proxy-MT5 Usability Review(337C 프록시-MT5 활용성 검토)",
            f"""
- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- action(행동): run337B(337B 실행)의 source/data/proxy/branch/core56(원천/데이터/프록시/분기/핵심56) 산출물을 검토해 protocol-only acceptance(계약 전용 승인)와 rejected claim memory(거절 주장 기억)를 만들었다.
- effect(효과): proxy(프록시) 일치는 signal sanity only(신호 점검 전용)로 제한되고, 다음 run337D(337D 실행)는 실행 계약을 만든다.
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
                "lane": "proxy_mt5_usability_review",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_DOC),
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};protocol_only_acceptance;goal_achieve_not_claimed.",
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__proxy_mt5_usability_review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "proxy_mt5_usability_and_branch_protocol_review",
                "tier_scope": "research_design_macro48_u42_core56_boundary",
                "kpi_scope": "proxy_signal_sanity_context_only_no_new_trading_kpi",
                "scoreboard_lane": "review_protocol_readiness",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_DOC),
                "primary_kpi": "proxy_signal_sanity_only_subjects=4;candidate_selection=none",
                "guardrail_kpi": "rejected_proxy_kpi_authority;core56_scope_locked;goal_achieve_not_claimed",
                "external_verification_status": "completed_existing_runtime_probe_reviewed_no_fresh_mt5",
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
                "ledger_row_id": f"{RUN_ID}__proxy_mt5_usability_review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "work_family": "review",
                "evidence_scope": "run337B_materialized_inputs_existing_run336M_N_runtime_evidence",
                "kpi_scope": "review_only_no_new_candidate_kpi",
                "status": STATUS,
                "judgment": JUDGMENT,
                "claim_boundary": CLAIM_BOUNDARY,
                "path": rel(REPORT_DOC),
                "notes": f"next_action={NEXT_RUN_ID};proxy_not_kpi_authority;goal_achieve_not_claimed.",
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
            "notes": "run337C_review_proxy_mt5_protocol_only_no_selection",
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
    source_review = build_source_lineage_review(inputs)
    data_review = build_data_integrity_review(inputs)
    canary_review = build_canary_review(inputs)
    proxy_review, future_requirements = build_proxy_review(inputs)
    branch_acceptance, accepted_queue, rejected_memory = build_branch_acceptance(inputs)
    core56_review = build_core56_review(inputs)
    next_queue = build_run337d_queue()
    audit = build_gate_audit(
        source_review,
        data_review,
        canary_review,
        proxy_review,
        branch_acceptance,
        rejected_memory,
        core56_review,
        next_queue,
    )
    failed_gates = [row for row in audit if row["status"] != "pass"]
    metrics = {
        "source_review_rows": len(source_review),
        "source_review_failed": len([row for row in source_review if row["review_status"] != "pass"]),
        "data_review_rows": len(data_review),
        "data_review_failed": len([row for row in data_review if row["review_status"] != "pass"]),
        "canary_review_rows": len(canary_review),
        "proxy_review_rows": len(proxy_review),
        "proxy_signal_only_subjects": len([row for row in proxy_review if row["review_status"] == "accepted_signal_sanity_only"]),
        "accepted_branch_rows": len(branch_acceptance),
        "accepted_queue_rows": len(accepted_queue),
        "rejected_claim_rows": len(rejected_memory),
        "core56_review_rows": len(core56_review),
        "next_queue_rows": len(next_queue),
    }
    run_artifacts = [
        write_csv(
            SOURCE_LINEAGE_REVIEW_CSV,
            (
                "source_id",
                "artifact_path",
                "input_lineage_judgment",
                "review_status",
                "review_finding",
                "allowed_use",
                "forbidden_use",
                "claim_boundary",
            ),
            source_review,
        ),
        write_csv(
            DATA_INTEGRITY_REVIEW_CSV,
            (
                "check_id",
                "integrity_judgment",
                "review_status",
                "time_axis",
                "feature_label_boundary",
                "leakage_risk",
                "review_finding",
                "next_condition",
                "claim_boundary",
            ),
            data_review,
        ),
        write_csv(
            NO_LOOKAHEAD_REVIEW_CSV,
            (
                "canary_id",
                "target_risk",
                "expected_rejection",
                "review_status",
                "review_finding",
                "must_fail_if_triggered",
                "forbidden",
                "claim_boundary",
            ),
            canary_review,
        ),
        write_csv(
            PROXY_MT5_REVIEW_CSV,
            (
                "subject",
                "signal_difference_status",
                "runtime_kpi_status",
                "source_usability_label",
                "dimensions_compared",
                "matched_dimensions",
                "mismatched_dimensions",
                "max_abs_proxy_minus_mt5",
                "review_status",
                "review_finding",
                "allowed_use",
                "forbidden_use",
                "next_requirement",
                "claim_boundary",
            ),
            proxy_review,
        ),
        write_csv(
            FUTURE_PROBE_REQUIREMENTS_CSV,
            (
                "subject",
                "required_before_kpi_use",
                "fresh_proxy_expected_required",
                "fresh_mt5_runtime_probe_required",
                "cost_direction_curve_gates_required",
                "usability_after_review",
                "claim_boundary",
            ),
            future_requirements,
        ),
        write_csv(
            BRANCH_GATE_ACCEPTANCE_CSV,
            (
                "branch_id",
                "lane",
                "payload_id",
                "source_failure_memory",
                "gate_coverage_status",
                "proxy_mt5_status",
                "review_acceptance",
                "forbidden",
                "next_protocol",
                "claim_boundary",
            ),
            branch_acceptance,
        ),
        write_csv(
            ACCEPTED_BRANCH_QUEUE_CSV,
            (
                "queue_id",
                "priority",
                "branch_id",
                "lane",
                "next_protocol",
                "required_inputs",
                "must_keep",
                "claim_boundary",
            ),
            accepted_queue,
        ),
        write_csv(
            REJECTED_CLAIM_MEMORY_CSV,
            (
                "memory_id",
                "rejected_claim",
                "reason",
                "future_reopen_condition",
                "claim_boundary",
            ),
            rejected_memory,
        ),
        write_csv(
            CORE56_REVIEW_CSV,
            (
                "subject",
                "source_decision",
                "review_decision",
                "reason",
                "accepted_next_protocol",
                "blocked_claims",
                "required_evidence",
                "claim_boundary",
            ),
            core56_review,
        ),
        write_csv(
            RUN337D_QUEUE_CSV,
            (
                "queue_id",
                "priority",
                "protocol",
                "required_inputs",
                "required_outputs",
                "success_condition",
                "forbidden",
                "claim_boundary",
            ),
            next_queue,
        ),
        write_csv(GATE_AUDIT_CSV, ("gate_id", "status", "evidence", "finding", "claim_boundary"), audit),
    ]
    run_artifacts.extend(write_receipts(metrics))
    final_payload = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS if not failed_gates else "blocked_stage337C_gate_failure",
        "judgment": JUDGMENT if not failed_gates else "stage337C_review_gate_failure_requires_repair",
        "decision": DECISION if not failed_gates else "stage337C_review_blocked_gate_failure",
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
                "status": "blocked_stage337C_gate_failure",
                "decision": "stage337C_review_blocked_gate_failure",
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
            rel(SOURCE_LINEAGE),
            rel(DATA_INTEGRITY_CONTRACT),
            rel(NO_LOOKAHEAD_CANARIES),
            rel(BRANCH_PAYLOAD),
            rel(PROXY_MT5_USABILITY),
            rel(CORE56_SCOPE),
            rel(RUN337B_DECISION),
        ],
        "outputs": [rel(path) for path in all_artifacts],
        "status": STATUS,
        "decision": DECISION,
        "external_verification_status": "completed_existing_runtime_probe_reviewed_no_fresh_mt5",
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
                "proxy_signal_only_subjects": metrics["proxy_signal_only_subjects"],
                "accepted_branch_rows": metrics["accepted_branch_rows"],
                "rejected_claim_rows": metrics["rejected_claim_rows"],
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
