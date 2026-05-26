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
RUN_NUMBER = "run337I"
RUN_ID = "run337I_review_materialized_execution_packages_v1"
PARENT_RUN_ID = "run337H_materialize_reviewed_execution_packages_v1"
NEXT_RUN_ID = "run337J_materialize_runner_scaffolds_v1"
STATUS = "completed_materialized_execution_package_review_accepts_runner_scaffold_queue_no_training_no_mt5"
JUDGMENT = "stage337I_packages_reviewed_accept_runner_scaffold_materialization_no_selection"
DECISION = "stage337I_packages_reviewed_open_run337J_runner_scaffolds_no_training_no_mt5_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage337I_package_review_no_model_training_no_mt5_execution_"
    "no_threshold_retuning_no_lot_optimization_no_forward_pocket_filtering_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
RUN337H_DIR = STAGE_DIR / "02_runs" / "run337H"
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
DECISION_DOC = DOCS / "decisions" / "2026-05-27_stage337I_review_materialized_execution_packages.md"
REPORT_DOC = REVIEWS_DIR / "run337I_review_materialized_execution_packages.md"

RUN337H_QUEUE = RUN337H_DIR / "run337I_package_review_queue.csv"
RUN337H_SOURCE_LINEAGE = RUN337H_DIR / "package_source_lineage_review.csv"
RUN337H_NO_LOOKAHEAD = RUN337H_DIR / "no_lookahead_canary_harness_package_spec.csv"
RUN337H_NO_LOOKAHEAD_CONTRACT = RUN337H_DIR / "no_lookahead_canary_harness_contract.json"
RUN337H_PROXY_MT5 = RUN337H_DIR / "proxy_mt5_fresh_probe_package_spec.csv"
RUN337H_PROXY_MT5_CONTRACT = RUN337H_DIR / "proxy_mt5_fresh_probe_output_contract.json"
RUN337H_CORE56 = RUN337H_DIR / "core56_asof_repair_package_spec.csv"
RUN337H_CORE56_CONTRACT = RUN337H_DIR / "core56_asof_repair_contract.json"
RUN337H_COST_CURVE = RUN337H_DIR / "cost_direction_curve_extraction_package_spec.csv"
RUN337H_COST_CURVE_CONTRACT = RUN337H_DIR / "cost_direction_curve_extraction_contract.json"
RUN337H_OFFENSE = RUN337H_DIR / "offense_branch_thesis_package_spec.csv"
RUN337H_REGIME = RUN337H_DIR / "economic_regime_asof_join_package_spec.csv"
RUN337H_REGIME_CONTRACT = RUN337H_DIR / "economic_regime_asof_join_contract.json"
RUN337H_RUNTIME = RUN337H_DIR / "runtime_probe_package_spec.csv"
RUN337H_RUNTIME_CONTRACT = RUN337H_DIR / "runtime_probe_package_contract.json"
RUN337H_CLAIM_GUARD = RUN337H_DIR / "claim_guard_blocker_package_spec.csv"
RUN337H_BLOCKER_MATRIX = RUN337H_DIR / "package_blocker_matrix.csv"
RUN337H_INDEX = RUN337H_DIR / "package_manifest_index.csv"
RUN337H_ACCEPTANCE = RUN337H_DIR / "package_acceptance_matrix.csv"
RUN337H_GATE_AUDIT = RUN337H_DIR / "required_gate_coverage_audit.csv"
RUN337H_DECISION = RUN337H_DIR / "final_reviewed_execution_packages_decision.json"
RUN337H_MANIFEST = RUN337H_DIR / "run_manifest.json"

PACKAGE_REVIEW_SOURCE_LINEAGE_CSV = RUN_DIR / "package_review_source_lineage.csv"
NO_LOOKAHEAD_PACKAGE_REVIEW_CSV = RUN_DIR / "no_lookahead_package_review.csv"
PROXY_MT5_PACKAGE_REVIEW_CSV = RUN_DIR / "proxy_mt5_package_review.csv"
CORE56_PACKAGE_REVIEW_CSV = RUN_DIR / "core56_package_review.csv"
COST_CURVE_PACKAGE_REVIEW_CSV = RUN_DIR / "cost_direction_curve_package_review.csv"
OFFENSE_PACKAGE_REVIEW_CSV = RUN_DIR / "offense_package_review.csv"
REGIME_PACKAGE_REVIEW_CSV = RUN_DIR / "economic_regime_package_review.csv"
RUNTIME_PACKAGE_REVIEW_CSV = RUN_DIR / "runtime_package_review.csv"
CLAIM_GUARD_PACKAGE_REVIEW_CSV = RUN_DIR / "claim_guard_package_review.csv"
PACKAGE_INDEX_REVIEW_CSV = RUN_DIR / "package_index_review.csv"
ACCEPTED_PACKAGES_CSV = RUN_DIR / "accepted_packages_for_runner_scaffold_queue.csv"
REPAIR_GAP_QUEUE_CSV = RUN_DIR / "repair_package_gap_queue.csv"
RUN337J_QUEUE_CSV = RUN_DIR / "run337J_runner_scaffold_materialization_queue.csv"
GATE_AUDIT_CSV = RUN_DIR / "required_gate_coverage_audit.csv"

EXPERIMENT_DESIGN_JSON = RUN_DIR / "experiment_design_receipt.json"
DATA_INTEGRITY_JSON = RUN_DIR / "data_integrity_receipt.json"
RUNTIME_PARITY_JSON = RUN_DIR / "runtime_parity_receipt.json"
ARTIFACT_LINEAGE_JSON = RUN_DIR / "artifact_lineage_receipt.json"
RESULT_JUDGMENT_JSON = RUN_DIR / "result_judgment_receipt.json"
FINAL_DECISION_JSON = RUN_DIR / "final_review_materialized_execution_packages_decision.json"
RUN_MANIFEST_JSON = RUN_DIR / "run_manifest.json"


SOURCE_INPUTS: tuple[Path, ...] = (
    RUN337H_QUEUE,
    RUN337H_SOURCE_LINEAGE,
    RUN337H_NO_LOOKAHEAD,
    RUN337H_NO_LOOKAHEAD_CONTRACT,
    RUN337H_PROXY_MT5,
    RUN337H_PROXY_MT5_CONTRACT,
    RUN337H_CORE56,
    RUN337H_CORE56_CONTRACT,
    RUN337H_COST_CURVE,
    RUN337H_COST_CURVE_CONTRACT,
    RUN337H_OFFENSE,
    RUN337H_REGIME,
    RUN337H_REGIME_CONTRACT,
    RUN337H_RUNTIME,
    RUN337H_RUNTIME_CONTRACT,
    RUN337H_CLAIM_GUARD,
    RUN337H_BLOCKER_MATRIX,
    RUN337H_INDEX,
    RUN337H_ACCEPTANCE,
    RUN337H_GATE_AUDIT,
    RUN337H_DECISION,
    RUN337H_MANIFEST,
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
        "queue": read_csv(RUN337H_QUEUE),
        "source_lineage": read_csv(RUN337H_SOURCE_LINEAGE),
        "no_lookahead": read_csv(RUN337H_NO_LOOKAHEAD),
        "no_lookahead_contract": read_json(RUN337H_NO_LOOKAHEAD_CONTRACT),
        "proxy_mt5": read_csv(RUN337H_PROXY_MT5),
        "proxy_mt5_contract": read_json(RUN337H_PROXY_MT5_CONTRACT),
        "core56": read_csv(RUN337H_CORE56),
        "core56_contract": read_json(RUN337H_CORE56_CONTRACT),
        "cost_curve": read_csv(RUN337H_COST_CURVE),
        "cost_curve_contract": read_json(RUN337H_COST_CURVE_CONTRACT),
        "offense": read_csv(RUN337H_OFFENSE),
        "regime": read_csv(RUN337H_REGIME),
        "regime_contract": read_json(RUN337H_REGIME_CONTRACT),
        "runtime": read_csv(RUN337H_RUNTIME),
        "runtime_contract": read_json(RUN337H_RUNTIME_CONTRACT),
        "claim_guard": read_csv(RUN337H_CLAIM_GUARD),
        "blocker_matrix": read_csv(RUN337H_BLOCKER_MATRIX),
        "package_index": read_csv(RUN337H_INDEX),
        "acceptance": read_csv(RUN337H_ACCEPTANCE),
        "gate_audit": read_csv(RUN337H_GATE_AUDIT),
        "decision": read_json(RUN337H_DECISION),
        "manifest": read_json(RUN337H_MANIFEST),
    }


def review_status(ok: bool) -> str:
    return "accepted_for_run337J_runner_scaffold_materialization" if ok else "repair_required_before_run337J"


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
                "allowed_use": "run337I package review and run337J runner scaffold queue only",
                "forbidden_use": "model training, MT5 execution, candidate selection, Forward Passed, runtime authority, Goal Achieve",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def closed_flags(rows: Sequence[Mapping[str, str]]) -> bool:
    return all(
        row.get("execution_allowed") == "false"
        and row.get("training_allowed") == "false"
        and row.get("mt5_execution_allowed") == "false"
        for row in rows
    )


def build_review_row(
    family: str,
    source_artifact: Path,
    contract_artifact: Path | str,
    review_scope: str,
    checks: Sequence[tuple[str, bool]],
    finding: str,
    next_use: str,
    blocked_if: str,
) -> dict[str, Any]:
    ok = all(value for _, value in checks)
    return {
        "review_id": f"{family}_package_review",
        "package_family": family,
        "source_artifact": rel(source_artifact),
        "contract_artifact": rel(contract_artifact) if contract_artifact else "",
        "review_scope": review_scope,
        "checks": ";".join(f"{name}={value}" for name, value in checks),
        "review_status": review_status(ok),
        "finding": finding,
        "next_use": next_use,
        "blocked_if": blocked_if,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def review_no_lookahead(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = inputs["no_lookahead"]
    contract = inputs["no_lookahead_contract"]
    checks = [
        ("row_count", len(rows) >= 5),
        ("closed_flags", closed_flags(rows)),
        ("must_fail", all(row.get("must_fail_to_pass") == "true" for row in rows) and contract.get("must_fail_to_pass") is True),
        ("expected_outputs", all(contains_all(row.get("expected_outputs", ""), ["bad_control_result.csv", "invalid_condition_matrix.csv", "repair_receipt.json"]) for row in rows)),
        ("blocker_criteria", all(contains_all(row.get("blocker_criteria", ""), ["training", "proxy", "MT5", "scorecard"]) for row in rows)),
        ("contract_execution_closed", contract.get("execution_allowed") is False),
    ]
    return [
        build_review_row(
            "no_lookahead",
            RUN337H_NO_LOOKAHEAD,
            RUN337H_NO_LOOKAHEAD_CONTRACT,
            "canary harness package specs reject future-bar, forward-pocket, threshold, lot, and timestamp-basis bad controls",
            checks,
            f"package_rows={len(rows)};contract_bad_controls={len(contract.get('bad_control_families', []))}",
            "run337J may materialize no-lookahead runner scaffold specs only",
            "any canary lacks must-fail output, repair receipt, or closed execution flags",
        )
    ]


def review_proxy_mt5(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = inputs["proxy_mt5"]
    contract = inputs["proxy_mt5_contract"]
    required_identity = ["threshold_id", "feature_hash", "model_hash", "timestamp_basis", "source_row_hash"]
    checks = [
        ("row_count", len(rows) >= 5),
        ("closed_flags", closed_flags(rows)),
        ("proxy_identity_outputs", all(contains_all(row.get("proxy_required_outputs", ""), required_identity) for row in rows)),
        ("mt5_required_files", all(contains_all(row.get("mt5_required_files", ""), ["EA", "ONNX", "adapter", "feature order", "set file", "tester ini", "handoff"]) for row in rows)),
        ("comparison_outputs", all(contains_all(row.get("comparison_outputs", ""), ["proxy_expected", "mt5_observed", "row_level_difference", "usability"]) for row in rows)),
        ("not_usable_for_kpi", all("not_usable_for_kpi" in row.get("usability_decision", "") for row in rows)),
        ("contract_identity", all(item in contract.get("required_identity", []) for item in required_identity)),
        ("kpi_authority_blocked", "not_authoritative" in contract.get("kpi_authority", "")),
    ]
    return [
        build_review_row(
            "proxy_mt5",
            RUN337H_PROXY_MT5,
            RUN337H_PROXY_MT5_CONTRACT,
            "proxy expected and fresh MT5 probe package specs retain identity, row-level difference, and usability boundary",
            checks,
            f"subjects={','.join(sorted({row.get('subject','') for row in rows}))}",
            "run337J may materialize proxy-MT5 runner scaffold specs only",
            "proxy package is used as KPI authority before fresh MT5 trade ledger and row-level difference review",
        )
    ]


def review_core56(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = inputs["core56"]
    contract = inputs["core56_contract"]
    checks = [
        ("row_count", len(rows) >= 5),
        ("closed_flags", closed_flags(rows)),
        ("required_artifacts", all(contains_all(row.get("required_artifacts", ""), ["source_inventory", "asof_join", "feature_handoff", "proxy_expected", "fresh_mt5"]) for row in rows)),
        ("full_family_block", all("full-family" in row.get("blocked_claims", "") for row in rows)),
        ("asof_guard", all("must not read later" in row.get("asof_guard", "") for row in rows)),
        ("contract_future_invalid", "future_join_flag" in contract.get("invalid_if", "")),
        ("contract_full_family_block", "blocked_until" in contract.get("full_family_claims", "")),
    ]
    return [
        build_review_row(
            "core56",
            RUN337H_CORE56,
            RUN337H_CORE56_CONTRACT,
            "core56 as-of repair package keeps source inventory, join audit, handoff, proxy, and fresh runtime package locked",
            checks,
            f"package_rows={len(rows)};join_keys={len(contract.get('join_keys', []))}",
            "run337J may materialize core56 repair runner scaffold specs only",
            "core56 full-family claim opens before as-of repair and fresh runtime package review",
        )
    ]


def review_cost_curve(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = inputs["cost_curve"]
    contract = inputs["cost_curve_contract"]
    required_outputs = [
        "cost_stress_report.csv",
        "spread_slippage_stress_report.csv",
        "long_short_attribution.csv",
        "D_B_source_attribution.csv",
        "curve_pocket_report.csv",
        "lot_normalized_report.csv",
        "regime_slice_report.csv",
    ]
    checks = [
        ("row_count", len(rows) >= 5),
        ("closed_flags", closed_flags(rows)),
        ("required_outputs", all(contains_all(row.get("required_outputs", ""), required_outputs) for row in rows)),
        ("minimum_metrics", all(contains_all(row.get("minimum_metrics", ""), ["net", "PF", "expectancy", "maxDD", "recovery", "trades_per_day"]) for row in rows)),
        ("contract_reports", all(report in contract.get("reports", {}) for report in [name.removesuffix(".csv") for name in required_outputs])),
        ("claim_boundary_rule", "blocked" in contract.get("claim_boundary_rule", "")),
    ]
    return [
        build_review_row(
            "cost_curve",
            RUN337H_COST_CURVE,
            RUN337H_COST_CURVE_CONTRACT,
            "cost, spread/slippage, direction/source, curve pocket, lot-normalized, and regime extraction package specs",
            checks,
            f"package_rows={len(rows)};contract_reports={len(contract.get('reports', {}))}",
            "run337J may materialize cost/direction/curve runner scaffold specs only",
            "any net/PF/DD/curve claim is made before all report groups are materialized and reviewed",
        )
    ]


def review_offense(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = inputs["offense"]
    checks = [
        ("row_count", len(rows) >= 4),
        ("execution_closed", all(row.get("execution_allowed") == "false" and row.get("mt5_execution_allowed") == "false" for row in rows)),
        ("training_closed", all(row.get("training_allowed") == "false" for row in rows)),
        ("required_controls", all(contains_all(row.get("required_controls", ""), ["no-lookahead", "fixed threshold", "fixed risk/lot", "no forward-pocket"]) for row in rows)),
        ("expected_outputs", all(contains_all(row.get("expected_outputs", ""), ["feature_thesis_card", "data_boundary_contract", "wfo_split_contract", "proxy_mt5_package_reference"]) for row in rows)),
    ]
    return [
        build_review_row(
            "offense",
            RUN337H_OFFENSE,
            "",
            "offense branch thesis package specs remain pre-training and guard-bound",
            checks,
            f"branches={','.join(sorted({row.get('branch_id','') for row in rows}))}",
            "run337J may materialize offense thesis runner scaffold specs only",
            "offense package opens model training or candidate selection before guard evidence review",
        )
    ]


def review_regime(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = inputs["regime"]
    contract = inputs["regime_contract"]
    checks = [
        ("row_count", len(rows) >= 6),
        ("closed_flags", closed_flags(rows)),
        ("source_identity", all(contains_all(row.get("required_source_identity", ""), ["source_timestamp", "source_sha256", "timezone", "revision_policy"]) for row in rows)),
        ("asof_rule", all("source_timestamp <= target_cycle_bar_time" in row.get("asof_join_rule", "") for row in rows)),
        ("expected_outputs", all(contains_all(row.get("expected_outputs", ""), ["source_inventory", "asof_join", "slice_report", "revision_policy"]) for row in rows)),
        ("contract_slice_families", all(item in contract.get("slice_families", []) for item in ["VIX", "USD", "rate", "ADX", "volatility", "session", "hour", "month"])),
        ("contract_asof_rule", "source_timestamp <= cycle_bar_time" in contract.get("asof_rule", "")),
    ]
    return [
        build_review_row(
            "regime",
            RUN337H_REGIME,
            RUN337H_REGIME_CONTRACT,
            "economic regime as-of join package specs keep source identity, revision policy, and future-join blockers",
            checks,
            f"package_rows={len(rows)};slice_families={','.join(contract.get('slice_families', []))}",
            "run337J may materialize economic regime runner scaffold specs only",
            "future or revised macro/source value is used to explain forward profit",
        )
    ]


def review_runtime(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = inputs["runtime"]
    contract = inputs["runtime_contract"]
    checks = [
        ("row_count", len(rows) >= 5),
        ("closed_flags", closed_flags(rows)),
        ("runtime_claim_boundary", all("no_runtime_authority" in row.get("runtime_claim_boundary", "") for row in rows)),
        ("required_files", all(contains_all(row.get("required_files", ""), ["EA", "model/ONNX", "adapter", "feature order", "set file", "tester ini", "handoff"]) for row in rows)),
        ("runtime_outputs", all(contains_all(row.get("runtime_outputs", ""), ["Strategy Tester", "terminal log", "trade ledger", "telemetry", "settings"]) for row in rows)),
        ("stress_outputs", all(contains_all(row.get("stress_outputs", ""), ["cost stress", "spread/slippage", "lot-normalized", "D/B", "regime", "curve"]) for row in rows)),
        ("contract_execution_closed", contract.get("execution_allowed") is False and contract.get("mt5_execution_allowed") is False),
        ("contract_runtime_authority_blocked", contract.get("runtime_authority") == "not_claimed"),
    ]
    return [
        build_review_row(
            "runtime",
            RUN337H_RUNTIME,
            RUN337H_RUNTIME_CONTRACT,
            "runtime probe package specs keep file identity, preflight, tester outputs, comparison outputs, and stress outputs probe-only",
            checks,
            f"subjects={','.join(sorted({row.get('subject','') for row in rows}))}",
            "run337J may materialize runtime runner scaffold specs only, no MT5 execution",
            "runtime package is treated as runtime authority before tester output and row-level parity",
        )
    ]


def review_claim_guard(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = inputs["claim_guard"]
    blockers = inputs["blocker_matrix"]
    required_blockers = ["model_training", "mt5_execution", "threshold_retune", "lot_optimization", "forward_pocket_filtering", "candidate_selection", "forward_passed", "runtime_authority", "goal_achieve"]
    checks = [
        ("row_count", len(rows) >= 10 and len(blockers) >= 10),
        ("required_blockers", all(any(row.get("blocker_id") == blocker for row in blockers) for blocker in required_blockers)),
        ("claim_status_not_claimed", all(row.get("claim_status") == "not_claimed" for row in blockers)),
        ("closed_flags", closed_flags(blockers)),
        ("required_response", all("stop_claim" in row.get("required_response", "") for row in blockers)),
    ]
    return [
        build_review_row(
            "claim_boundary",
            RUN337H_CLAIM_GUARD,
            RUN337H_BLOCKER_MATRIX,
            "claim guard package blocks training, MT5 execution, retune, selection, Forward claim, runtime authority, and Goal Achieve",
            checks,
            f"blocker_rows={len(blockers)};required_blockers={len(required_blockers)}",
            "run337J may materialize claim guard scaffold specs only",
            "any blocked claim is promoted from package specs",
        )
    ]


def review_package_index(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    index = inputs["package_index"]
    acceptance = inputs["acceptance"]
    decision = inputs["decision"]
    manifest = inputs["manifest"]
    expected = {"no_lookahead", "proxy_mt5", "core56", "cost_curve", "offense", "regime", "runtime", "claim_boundary"}
    checks = [
        ("index_rows", {row.get("package_family") for row in index} == expected),
        ("acceptance_rows", {row.get("package_family") for row in acceptance} == expected),
        ("index_execution_closed", all(row.get("execution_allowed") == "false" and row.get("training_allowed") == "false" and row.get("mt5_execution_allowed") == "false" for row in index)),
        ("acceptance_status", all(row.get("acceptance_status") == "accepted_for_run337I_package_review" for row in acceptance)),
        ("decision_no_claims", decision.get("selected_candidate") == "none" and decision.get("forward_passed") == "not_claimed" and decision.get("runtime_authority") == "not_claimed" and decision.get("goal_achieve") == "not_claimed"),
        ("decision_no_execution", decision.get("model_training") == "not_run" and decision.get("mt5_execution") == "not_run"),
        ("manifest_next_action", manifest.get("next_action") == RUN_ID),
    ]
    return [
        build_review_row(
            "package_index",
            RUN337H_INDEX,
            RUN337H_ACCEPTANCE,
            "package index, acceptance matrix, final decision, and manifest claim boundary",
            checks,
            f"index_rows={len(index)};acceptance_rows={len(acceptance)}",
            "run337J may materialize runner scaffold queue if all package families pass",
            "package index opens execution, MT5, training, candidate selection, or operating claims",
        )
    ]


def build_review_sets(inputs: Mapping[str, Any]) -> dict[str, list[dict[str, Any]]]:
    return {
        "no_lookahead": review_no_lookahead(inputs),
        "proxy_mt5": review_proxy_mt5(inputs),
        "core56": review_core56(inputs),
        "cost_curve": review_cost_curve(inputs),
        "offense": review_offense(inputs),
        "regime": review_regime(inputs),
        "runtime": review_runtime(inputs),
        "claim_boundary": review_claim_guard(inputs),
        "package_index": review_package_index(inputs),
    }


def build_accepted_queue(review_sets: Mapping[str, Sequence[Mapping[str, Any]]]) -> list[dict[str, Any]]:
    next_tasks = {
        "no_lookahead": ("materialize_no_lookahead_runner_scaffold", "no-lookahead canary harness runner scaffold"),
        "proxy_mt5": ("materialize_proxy_mt5_runner_scaffold", "proxy expected and fresh MT5 probe runner scaffold"),
        "core56": ("materialize_core56_runner_scaffold", "core56 as-of repair runner scaffold"),
        "cost_curve": ("materialize_cost_direction_curve_runner_scaffold", "cost/direction/curve extraction runner scaffold"),
        "offense": ("materialize_offense_branch_runner_scaffold", "offense thesis runner scaffold without training"),
        "regime": ("materialize_regime_asof_runner_scaffold", "economic regime as-of runner scaffold"),
        "runtime": ("materialize_runtime_probe_runner_scaffold", "runtime probe runner scaffold without MT5 execution"),
        "claim_boundary": ("materialize_claim_guard_runner_scaffold", "claim guard runner scaffold"),
        "package_index": ("materialize_package_index_runner_scaffold", "package index and claim boundary runner scaffold"),
    }
    rows: list[dict[str, Any]] = []
    for family, review_rows in review_sets.items():
        accepted = all(str(row.get("review_status", "")).startswith("accepted") for row in review_rows)
        task, scope = next_tasks[family]
        rows.append(
            {
                "package_family": family,
                "accepted_rows": sum(1 for row in review_rows if str(row.get("review_status", "")).startswith("accepted")),
                "total_rows": len(review_rows),
                "queue_status": "accepted_for_run337J_runner_scaffold_materialization" if accepted else "blocked_for_repair",
                "next_task": task,
                "runner_scope": scope,
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
                        "package_family": family,
                        "source_artifact": row.get("source_artifact", ""),
                        "finding": row.get("finding", ""),
                        "repair_required": row.get("blocked_if", ""),
                        "next_action": "repair_run337H_package_spec_before_runner_scaffold",
                        "claim_boundary": CLAIM_BOUNDARY,
                    }
                )
    return gaps


def build_run337j_queue(accepted_queue: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, row in enumerate(accepted_queue, start=1):
        if row.get("queue_status") != "accepted_for_run337J_runner_scaffold_materialization":
            continue
        rows.append(
            {
                "queue_id": row.get("next_task", ""),
                "priority": index,
                "package_family": row.get("package_family", ""),
                "required_review_input": rel(ACCEPTED_PACKAGES_CSV),
                "required_source_artifacts": "run337H package specs and run337I review CSVs",
                "required_outputs": "runner scaffold manifest;preflight checklist;blocked execution command;claim-boundary receipt;run337K review queue",
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
    run337j_queue: Sequence[Mapping[str, Any]],
    inputs: Mapping[str, Any],
) -> list[dict[str, Any]]:
    source_ok = all(row.get("review_status") == "accepted_for_review" for row in source_lineage)
    h_gate_ok = all(row.get("status") == "pass" for row in inputs["gate_audit"])
    h_accept_ok = all(row.get("acceptance_status") == "accepted_for_run337I_package_review" for row in inputs["acceptance"])
    family_ok = {
        family: all(str(row.get("review_status", "")).startswith("accepted") for row in rows)
        for family, rows in review_sets.items()
    }
    accepted_ok = all(row.get("queue_status") == "accepted_for_run337J_runner_scaffold_materialization" for row in accepted_queue)
    return [
        {
            "gate_id": "source_lineage_connected",
            "status": "pass" if source_ok and len(source_lineage) >= len(SOURCE_INPUTS) else "fail",
            "evidence": rel(PACKAGE_REVIEW_SOURCE_LINEAGE_CSV),
            "finding": f"source_rows={len(source_lineage)};all_present={source_ok}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "run337H_package_inputs_accepted",
            "status": "pass" if h_gate_ok and h_accept_ok else "fail",
            "evidence": f"{rel(RUN337H_GATE_AUDIT)};{rel(RUN337H_ACCEPTANCE)}",
            "finding": f"run337H_gates_pass={h_gate_ok};package_acceptance={h_accept_ok}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        *[
            {
                "gate_id": f"{family}_package_review_accepted",
                "status": "pass" if family_ok[family] else "fail",
                "evidence": {
                    "no_lookahead": rel(NO_LOOKAHEAD_PACKAGE_REVIEW_CSV),
                    "proxy_mt5": rel(PROXY_MT5_PACKAGE_REVIEW_CSV),
                    "core56": rel(CORE56_PACKAGE_REVIEW_CSV),
                    "cost_curve": rel(COST_CURVE_PACKAGE_REVIEW_CSV),
                    "offense": rel(OFFENSE_PACKAGE_REVIEW_CSV),
                    "regime": rel(REGIME_PACKAGE_REVIEW_CSV),
                    "runtime": rel(RUNTIME_PACKAGE_REVIEW_CSV),
                    "claim_boundary": rel(CLAIM_GUARD_PACKAGE_REVIEW_CSV),
                    "package_index": rel(PACKAGE_INDEX_REVIEW_CSV),
                }[family],
                "finding": f"{family}_accepted={family_ok[family]}",
                "claim_boundary": CLAIM_BOUNDARY,
            }
            for family in [
                "no_lookahead",
                "proxy_mt5",
                "core56",
                "cost_curve",
                "offense",
                "regime",
                "runtime",
                "claim_boundary",
                "package_index",
            ]
        ],
        {
            "gate_id": "accepted_packages_queue_ready",
            "status": "pass" if accepted_ok and len(accepted_queue) >= 9 else "fail",
            "evidence": rel(ACCEPTED_PACKAGES_CSV),
            "finding": f"accepted_package_families={len(accepted_queue)};accepted={accepted_ok}",
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
            "gate_id": "run337J_runner_scaffold_queue_ready",
            "status": "pass" if len(run337j_queue) >= 9 else "fail",
            "evidence": rel(RUN337J_QUEUE_CSV),
            "finding": f"run337J_queue_rows={len(run337j_queue)}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "claim_guard_no_execution_no_goal",
            "status": "pass",
            "evidence": rel(FINAL_DECISION_JSON),
            "finding": "package review opens scaffold materialization only; no model training, MT5 execution, selection, Forward claim, runtime authority, or Goal Achieve",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_metrics(
    source_lineage: Sequence[Mapping[str, Any]],
    review_sets: Mapping[str, Sequence[Mapping[str, Any]]],
    accepted_queue: Sequence[Mapping[str, Any]],
    repair_gaps: Sequence[Mapping[str, Any]],
    run337j_queue: Sequence[Mapping[str, Any]],
    audit: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    return {
        "source_lineage_rows": len(source_lineage),
        "review_family_count": len(review_sets),
        "review_rows": sum(len(rows) for rows in review_sets.values()),
        "accepted_review_rows": sum(1 for rows in review_sets.values() for row in rows if str(row.get("review_status", "")).startswith("accepted")),
        "accepted_package_families": len([row for row in accepted_queue if row.get("queue_status") == "accepted_for_run337J_runner_scaffold_materialization"]),
        "repair_gap_rows": len(repair_gaps),
        "run337j_queue_rows": len(run337j_queue),
        "gate_rows": len(audit),
        "failed_gate_rows": len([row for row in audit if row.get("status") != "pass"]),
    }


def write_receipts(metrics: Mapping[str, Any]) -> list[Path]:
    return [
        write_json(
            EXPERIMENT_DESIGN_JSON,
            {
                "run_id": RUN_ID,
                "hypothesis": "run337H package specs are complete enough to open runner scaffold materialization without training or MT5 execution",
                "decision_use": "decide whether run337J may materialize non-executing runner scaffolds for package families",
                "comparison_baseline": "run337H package specs, contracts, blocker matrix, acceptance matrix, final decision, and manifest",
                "control_variables": "no model training, no MT5 execution, no threshold retune, no lot optimization, no forward-pocket filtering, no candidate selection",
                "changed_variables": "package review labels, accepted package queue, repair gap queue, and runner scaffold materialization queue",
                "sample_scope": "package review only; no trading KPI sample, model fit, or MT5 trade rows",
                "success_criteria": "all package families accepted, repair gap queue empty, and run337J runner scaffold queue ready",
                "failure_criteria": "missing package family, open execution flag, missing identity contract, or weak blocker matrix",
                "invalid_conditions": "using package review to claim Forward Passed, runtime authority, candidate selection, live readiness, or Goal Achieve",
                "stop_conditions": "any gate fails; repair package spec before runner scaffold materialization",
                "evidence_plan": "review CSVs, accepted queue, repair gap queue, run337J queue, gate audit, receipts, final decision, ledgers, artifact registry",
                "metrics": metrics,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            DATA_INTEGRITY_JSON,
            {
                "run_id": RUN_ID,
                "data_source": "run337H package specs and contracts",
                "time_axis": "future scaffolds must preserve cycle_bar_time, source_timestamp, broker timezone, timestamp basis, as-of status, and source_row_hash",
                "sample_scope": "package review only; no new US100 M5 bars are consumed",
                "missing_or_duplicate_check": "future scaffolds must expose missing, duplicate, stale, revision, timezone, and future join checks before execution",
                "feature_label_boundary": "no labels or fit; no-lookahead canary package must reject future-derived feature paths before any later runner can execute",
                "split_boundary": "future train/WFO/forward split remains closed until scaffold review and later execution packages are accepted",
                "leakage_risk": "future-bar features, forward-pocket selection, threshold retune, lot optimization, timestamp drift, macro revision drift",
                "data_hash_or_identity": rel(PACKAGE_REVIEW_SOURCE_LINEAGE_CSV),
                "integrity_judgment": "usable_with_boundary",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RUNTIME_PARITY_JSON,
            {
                "run_id": RUN_ID,
                "research_path": rel(Path(__file__)),
                "runtime_path": rel(RUNTIME_PACKAGE_REVIEW_CSV),
                "shared_contract": "feature order, threshold, risk, lot, timestamp basis, proxy expected, MT5 observed, tester report, trade ledger, D/B source, cost stress, and regime slices must match before KPI authority",
                "known_differences": "run337I reviews package specs only; no MT5 execution and no proxy/MT5 observed values are produced",
                "parity_check": "runtime package review keeps fresh MT5 probe and row-level proxy-MT5 difference mandatory for later scaffold review",
                "parity_identity": rel(PROXY_MT5_PACKAGE_REVIEW_CSV),
                "runtime_claim_boundary": "package_review_only_no_runtime_authority",
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
                    rel(PACKAGE_REVIEW_SOURCE_LINEAGE_CSV),
                    rel(ACCEPTED_PACKAGES_CSV),
                    rel(REPAIR_GAP_QUEUE_CSV),
                    rel(RUN337J_QUEUE_CSV),
                    rel(GATE_AUDIT_CSV),
                ],
                "artifact_hashes": "registered in artifact_registry after run",
                "registry_links": "run_registry;alpha_run_ledger;stage_run_ledger;artifact_registry",
                "availability": "tracked after commit; reproducible from run337I script",
                "lineage_judgment": "connected_with_boundary",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RESULT_JUDGMENT_JSON,
            {
                "run_id": RUN_ID,
                "result_subject": "materialized execution package specs",
                "evidence_available": "package review CSVs, accepted queue, repair gap queue, run337J queue, gate audit",
                "evidence_missing": "no runner scaffolds yet, no model training, no MT5 execution, no proxy expected values, no MT5 observed values, no candidate KPI",
                "judgment_label": "exploratory",
                "claim_boundary": "packages are accepted for runner scaffold materialization only; no candidate, Forward decision, or runtime authority",
                "next_condition": NEXT_RUN_ID,
                "user_explanation_hook": "패키지 명세는 검토를 통과했지만 아직 실행 러너가 생긴 것은 아니다. 다음 단계는 비실행 러너 뼈대를 만드는 일이다.",
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
# run337I Materialized Execution Package Review(337I 물질화된 실행 패키지 검토)

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
- accepted_package_families(승인 패키지 묶음): `{metrics['accepted_package_families']}`
- repair_gap_rows(수리 공백 행): `{metrics['repair_gap_rows']}`
- run337J_queue_rows(337J 대기열 행): `{metrics['run337j_queue_rows']}`
- gate_rows(게이트 행): `{metrics['gate_rows']}`, failed(실패): `{metrics['failed_gate_rows']}`

Effect(효과): run337I(337I 실행)는 run337H(337H 실행)의 package spec(패키지 명세)을 검토해 9개 runner scaffold(러너 뼈대) 물질화 대기열을 만들었다. 아직 model training(모델 학습), MT5 execution(MT5 실행), candidate selection(후보 선택)은 없다.
"""
    decision = f"""
# 2026-05-27 Stage337I Decision(337I 결정)

- decision(결정): `{DECISION}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed_for_stage337_new_work`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`

Effect(효과): 다음 run337J(337J 실행)는 non-executing runner scaffold(비실행 러너 뼈대)를 물질화한다. 이 결정은 학습 허가, MT5 실행 결과, Forward 판정, 운영 승격이 아니다.
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
- effect(효과): run337I(337I 실행)는 materialized package specs(물질화된 패키지 명세)를 검토하고 run337J(337J 실행) 러너 뼈대 물질화 대기열로 넘겼다. 아직 선택 후보는 없다.
"""
    artifacts.append(write_md(SELECTED_DIR / "selection_status.md", selection))

    brief_text, brief_bom = read_text_lossless(SPEC_DIR / "stage_brief.md")
    brief_text = replace_prefix_line(brief_text, "- latest_run(최신 실행):", f"- latest_run(최신 실행): `{RUN_ID}`")
    brief_text = insert_after_marker_once(
        brief_text,
        "- run337H_summary(337H 요약):",
        f"- run337I_summary(337I 요약): `{STATUS}`. Effect(효과): run337H(337H 실행)의 8개 패키지 묶음을 검토하고 run337J(337J 실행) runner scaffold(러너 뼈대) 물질화 대기열로 넘긴다.",
        "run337I_summary",
    )
    artifacts.append(write_text_lossless(SPEC_DIR / "stage_brief.md", brief_text, brief_bom))

    input_section = f"""
- package_review_source_lineage(패키지 검토 원천 계보): `{rel(PACKAGE_REVIEW_SOURCE_LINEAGE_CSV)}`
- no_lookahead_package_review(미래참조 방어 패키지 검토): `{rel(NO_LOOKAHEAD_PACKAGE_REVIEW_CSV)}`
- proxy_mt5_package_review(프록시-MT5 패키지 검토): `{rel(PROXY_MT5_PACKAGE_REVIEW_CSV)}`
- core56_package_review(핵심56 패키지 검토): `{rel(CORE56_PACKAGE_REVIEW_CSV)}`
- cost_direction_curve_package_review(비용/방향/곡선 패키지 검토): `{rel(COST_CURVE_PACKAGE_REVIEW_CSV)}`
- offense_package_review(공격 패키지 검토): `{rel(OFFENSE_PACKAGE_REVIEW_CSV)}`
- economic_regime_package_review(경제 국면 패키지 검토): `{rel(REGIME_PACKAGE_REVIEW_CSV)}`
- runtime_package_review(런타임 패키지 검토): `{rel(RUNTIME_PACKAGE_REVIEW_CSV)}`
- claim_guard_package_review(주장 방어 패키지 검토): `{rel(CLAIM_GUARD_PACKAGE_REVIEW_CSV)}`
- accepted_packages_for_runner_scaffold_queue(러너 뼈대용 승인 패키지 대기열): `{rel(ACCEPTED_PACKAGES_CSV)}`
- run337J_queue(337J 대기열): `{rel(RUN337J_QUEUE_CSV)}`

Effect(효과): 다음 실행은 이 검토 결과를 근거로 비실행 runner scaffold(러너 뼈대)를 만든다.
"""
    artifacts.append(append_section_once(INPUTS_DIR / "input_refs.md", "## run337I Outputs(337I 산출물)", input_section))

    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_prefix_line(workspace_text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    focus = (
        "- >-\n"
        f"  Stage337 run337I focus complete: Stage337(337단계) run337I(337I 실행)는 `{STATUS}`로 materialized execution package review(물질화된 실행 패키지 검토)를 완료했다. "
        "Effect(효과): run337J(337J 실행) runner scaffold materialization(러너 뼈대 물질화) 대기열을 열었지만 model training(모델 학습), MT5 execution(MT5 실행), candidate selection(후보 선택)은 아직 닫아둔다.\n"
    )
    workspace_text = insert_focus_once(workspace_text, focus, "Stage337 run337I focus complete")
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
        f"- run337I_summary(337I 요약): `{STATUS}`. "
        "Effect(효과): 패키지 명세를 검토 승인하고 run337J(337J 실행) 러너 뼈대 대기열로 넘기며, 학습/MT5/후보 선택은 계속 닫아둔다."
    )
    current_text = insert_after_marker_once(current_text, "- decision(결정):", summary, "run337I_summary")
    artifacts.append(write_text_lossless(CURRENT_STATE, current_text, current_bom))

    artifacts.append(
        append_section_once(
            CHANGELOG,
            "## Stage337I Materialized Execution Package Review(337I 물질화된 실행 패키지 검토)",
            f"""
- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- action(행동): run337H(337H 실행)의 package spec(패키지 명세)을 검토하고 run337J(337J 실행) runner scaffold(러너 뼈대) 물질화 대기열을 만들었다.
- effect(효과): 다음 실행은 실제 실행 전 단계의 러너 뼈대만 만들 수 있고, 학습과 MT5 실행은 계속 닫힌다.
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
                "lane": "materialized_execution_package_review",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_DOC),
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};packages_reviewed;training_not_allowed;mt5_not_executed;goal_achieve_not_claimed.",
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__materialized_execution_package_review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "materialized_execution_package_review",
                "tier_scope": "stage337_package_boundary_macro48_u42_core56",
                "kpi_scope": "package_review_only_no_new_candidate_kpi",
                "scoreboard_lane": "runner_scaffold_readiness",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_DOC),
                "primary_kpi": "accepted_package_families=9;run337j_queue_rows=9;candidate_selection=none",
                "guardrail_kpi": "training_not_allowed;mt5_not_executed;runtime_authority_not_claimed;goal_achieve_not_claimed",
                "external_verification_status": "out_of_scope_by_claim_package_review_only",
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
                "ledger_row_id": f"{RUN_ID}__materialized_execution_package_review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "work_family": "result_judgment",
                "evidence_scope": "run337H_reviewed_execution_packages",
                "kpi_scope": "package_review_only_no_new_candidate_kpi",
                "status": STATUS,
                "judgment": JUDGMENT,
                "claim_boundary": CLAIM_BOUNDARY,
                "path": rel(REPORT_DOC),
                "notes": f"next_action={NEXT_RUN_ID};packages_reviewed;training_not_allowed;mt5_not_executed;goal_achieve_not_claimed.",
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
            "notes": "run337I_materialized_execution_package_review_no_selection",
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


REVIEW_COLUMNS = (
    "review_id",
    "package_family",
    "source_artifact",
    "contract_artifact",
    "review_scope",
    "checks",
    "review_status",
    "finding",
    "next_use",
    "blocked_if",
    "claim_boundary",
)


def main() -> int:
    generated_at = now_utc()
    inputs = load_inputs()
    source_lineage = build_source_lineage_review()
    review_sets = build_review_sets(inputs)
    accepted_queue = build_accepted_queue(review_sets)
    repair_gaps = build_repair_gap_queue(review_sets)
    run337j_queue = build_run337j_queue(accepted_queue)
    audit = build_gate_audit(source_lineage, review_sets, accepted_queue, repair_gaps, run337j_queue, inputs)
    metrics = build_metrics(source_lineage, review_sets, accepted_queue, repair_gaps, run337j_queue, audit)
    failed_gates = [row for row in audit if row.get("status") != "pass"]

    run_artifacts = [
        write_csv(
            PACKAGE_REVIEW_SOURCE_LINEAGE_CSV,
            ("source_path", "exists", "sha256", "row_count_or_keys", "review_status", "allowed_use", "forbidden_use", "claim_boundary"),
            source_lineage,
        ),
        write_csv(NO_LOOKAHEAD_PACKAGE_REVIEW_CSV, REVIEW_COLUMNS, review_sets["no_lookahead"]),
        write_csv(PROXY_MT5_PACKAGE_REVIEW_CSV, REVIEW_COLUMNS, review_sets["proxy_mt5"]),
        write_csv(CORE56_PACKAGE_REVIEW_CSV, REVIEW_COLUMNS, review_sets["core56"]),
        write_csv(COST_CURVE_PACKAGE_REVIEW_CSV, REVIEW_COLUMNS, review_sets["cost_curve"]),
        write_csv(OFFENSE_PACKAGE_REVIEW_CSV, REVIEW_COLUMNS, review_sets["offense"]),
        write_csv(REGIME_PACKAGE_REVIEW_CSV, REVIEW_COLUMNS, review_sets["regime"]),
        write_csv(RUNTIME_PACKAGE_REVIEW_CSV, REVIEW_COLUMNS, review_sets["runtime"]),
        write_csv(CLAIM_GUARD_PACKAGE_REVIEW_CSV, REVIEW_COLUMNS, review_sets["claim_boundary"]),
        write_csv(PACKAGE_INDEX_REVIEW_CSV, REVIEW_COLUMNS, review_sets["package_index"]),
        write_csv(
            ACCEPTED_PACKAGES_CSV,
            ("package_family", "accepted_rows", "total_rows", "queue_status", "next_task", "runner_scope", "claim_boundary"),
            accepted_queue,
        ),
        write_csv(
            REPAIR_GAP_QUEUE_CSV,
            ("gap_id", "package_family", "source_artifact", "finding", "repair_required", "next_action", "claim_boundary"),
            repair_gaps,
        ),
        write_csv(
            RUN337J_QUEUE_CSV,
            (
                "queue_id",
                "priority",
                "package_family",
                "required_review_input",
                "required_source_artifacts",
                "required_outputs",
                "forbidden",
                "claim_boundary",
            ),
            run337j_queue,
        ),
        write_csv(GATE_AUDIT_CSV, ("gate_id", "status", "evidence", "finding", "claim_boundary"), audit),
    ]
    run_artifacts.extend(write_receipts(metrics))
    final_payload = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS if not failed_gates else "blocked_stage337I_package_review_gate_failure",
        "judgment": JUDGMENT if not failed_gates else "stage337I_package_review_requires_repair",
        "decision": DECISION if not failed_gates else "stage337I_package_review_blocked_gate_failure",
        "metrics": metrics,
        "failed_gates": failed_gates,
        "next_action": NEXT_RUN_ID if not failed_gates else "repair_run337H_package_specs_before_runner_scaffold",
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
                "status": "blocked_stage337I_package_review_gate_failure",
                "decision": "stage337I_package_review_blocked_gate_failure",
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
        "external_verification_status": "out_of_scope_by_claim_package_review_only_no_mt5_execution",
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
                "accepted_package_families": metrics["accepted_package_families"],
                "repair_gap_rows": metrics["repair_gap_rows"],
                "run337J_queue_rows": metrics["run337j_queue_rows"],
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
