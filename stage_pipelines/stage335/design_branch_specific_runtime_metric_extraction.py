from __future__ import annotations

import csv
import hashlib
import json
import math
import re
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

TODAY = "2026-05-26"
STAGE_ID = "335_overfit_guard__failure_memory_constrained_research_handoff"
RUN_NUMBER = "run335M"
RUN_ID = "run335M_branch_specific_runtime_metric_extraction_design_v1"
PARENT_RUN_ID = "run335L_independent_runtime_parity_and_proxy_usability_review_v1"
NEXT_RUN_ID = "run335N_materialize_branch_specific_runtime_metric_extractors_v1"

STATUS = "completed_branch_specific_runtime_metric_extraction_design_no_forward_decision"
JUDGMENT = "branch_specific_metric_extraction_contract_ready_trade_ledger_materialization_required_no_forward_decision"
DECISION = "stage335M_branch_specific_metric_extraction_contract_ready_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage335M_branch_specific_runtime_metric_extraction_design_no_model_training_"
    "no_threshold_retuning_no_lot_optimization_no_direct_forward_pocket_filtering_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
RUN335D_DIR = STAGE_DIR / "02_runs" / "run335D"
RUN335F_DIR = STAGE_DIR / "02_runs" / "run335F"
RUN335K_DIR = STAGE_DIR / "02_runs" / "run335K"
RUN335L_DIR = STAGE_DIR / "02_runs" / "run335L"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
INPUT_REFS = STAGE_DIR / "01_inputs" / "input_refs.md"

DOCS = ROOT / "docs"
WORKSPACE_STATE = DOCS / "workspace" / "workspace_state.yaml"
CURRENT_STATE = DOCS / "context" / "current_working_state.md"
CHANGELOG = DOCS / "workspace" / "changelog.md"
RUN_REGISTRY = DOCS / "registers" / "run_registry.csv"
ALPHA_LEDGER = DOCS / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = DOCS / "registers" / "artifact_registry.csv"
DECISION_DOC = DOCS / "decisions" / "2026-05-26_stage335M_branch_specific_runtime_metric_extraction_design.md"
REPORT_DOC = REVIEWS_DIR / "run335M_branch_specific_runtime_metric_extraction_design.md"

SCHEMA_CSV = RUN_DIR / "branch_specific_metric_schema.csv"
CONTRACT_CSV = RUN_DIR / "branch_runtime_metric_extraction_contract.csv"
SOURCE_AUDIT_CSV = RUN_DIR / "metric_source_availability_audit.csv"
LOOKAHEAD_CSV = RUN_DIR / "lookahead_bias_rejection_matrix.csv"
QUEUE_CSV = RUN_DIR / "run335N_metric_materialization_queue.csv"
PARSER_AUDIT_CSV = RUN_DIR / "mt5_report_parser_feasibility_audit.csv"
GATE_AUDIT_CSV = RUN_DIR / "required_gate_coverage_audit.csv"
RESULT_JUDGMENT_CSV = RUN_DIR / "result_judgment.csv"
FINAL_DECISION_JSON = RUN_DIR / "final_branch_specific_runtime_metric_extraction_design_decision.json"
RUN_MANIFEST_JSON = RUN_DIR / "run_manifest.json"


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


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
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    if isinstance(value, float):
        return "" if not math.isfinite(value) else f"{value:.12g}"
    return str(value)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column, "")) for column in columns})
    return path


def write_json(path: Path, payload: Any) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return path


def write_md(path: Path, text: str) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.strip() + "\n", encoding="utf-8-sig", newline="\n")
    return path


def read_text_lossless(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    return raw.decode("utf-8-sig"), raw.startswith(b"\xef\xbb\xbf")


def write_text_lossless(path: Path, text: str, had_bom: bool) -> None:
    io_path(path).write_text(text, encoding="utf-8-sig" if had_bom else "utf-8", newline="\n")


def replace_line(text: str, prefix: str, new_line: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = new_line
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text.rstrip() + "\n" + new_line + "\n"


def append_or_replace_section(path: Path, header: str, body: str) -> None:
    text, had_bom = read_text_lossless(path)
    section = f"\n## {header}\n\n{body.strip()}\n"
    pattern = re.compile(rf"\n## {re.escape(header)}\n.*?(?=\n## |\Z)", re.S)
    if pattern.search(text):
        text = pattern.sub(section.rstrip(), text)
    else:
        text = text.rstrip() + section
    write_text_lossless(path, text.rstrip() + "\n", had_bom)


def sha256_bytes(path: Path) -> str:
    return hashlib.sha256(io_path(path).read_bytes()).hexdigest()


METRIC_SCHEMA: list[dict[str, str]] = [
    {
        "metric_id": "trade_ledger",
        "metric_family": "runtime_trade_identity",
        "definition": "One row per MT5 closed trade/deal with open time, close time, side, volume, price, commission, swap, profit, and report identity.",
        "source_required": "run335K MT5 HTML report deal/trade table",
        "join_key": "attempt_name plus ticket or close_time nearest telemetry bar",
        "time_axis": "MT5 broker server time; never future shifted",
        "branch_specific_rule": "All branch metrics must derive from this ledger instead of repeated aggregate proxy values.",
        "lookahead_guard": "Do not filter after seeing profit; only join predeclared branch axes.",
        "output_grain": "attempt_name x trade_id",
        "usable_for": "branch-specific KPI, attribution, curve, cost stress",
        "not_usable_for": "candidate selection without run335N materialization and review",
        "missing_policy": "blocked_for_branch_specific_forward_judgment",
    },
    {
        "metric_id": "headline_kpi",
        "metric_family": "profitability_and_risk",
        "definition": "Net profit, profit factor, trade count, expectancy, max drawdown, and recovery factor recomputed or reconciled per attempt.",
        "source_required": "MT5 report summary plus parsed trade ledger",
        "join_key": "attempt_name",
        "time_axis": "full run335K forward runtime interval",
        "branch_specific_rule": "Report every branch against the same fixed attempts; no branch may reuse a single repeated proxy value as proof.",
        "lookahead_guard": "No threshold, lot, or side change after KPI is seen.",
        "output_grain": "branch_name x attempt_name",
        "usable_for": "runtime metric comparison and failure-memory prioritization",
        "not_usable_for": "Forward Passed or Goal Achieve alone",
        "missing_policy": "name_missing_dimension_and_continue_no_positive_claim",
    },
    {
        "metric_id": "trades_per_day",
        "metric_family": "activity_density",
        "definition": "Closed trades divided by elapsed calendar days and active market-session days, with both denominators recorded.",
        "source_required": "parsed trade ledger plus first/last telemetry cycle",
        "join_key": "attempt_name",
        "time_axis": "closed trade time and telemetry bar time",
        "branch_specific_rule": "Compute per branch only after branch scope is explicit; do not infer density from aggregate proxy.",
        "lookahead_guard": "No post-outcome date trimming.",
        "output_grain": "branch_name x attempt_name",
        "usable_for": "trade-density adequacy diagnostics",
        "not_usable_for": "lot or threshold optimization",
        "missing_policy": "blocked_for_trade_density_claim",
    },
    {
        "metric_id": "direction_attribution",
        "metric_family": "long_short_attribution",
        "definition": "Net, PF, expectancy, count, drawdown contribution, and streak by long and short side while retaining combined total.",
        "source_required": "parsed trade ledger side/type field",
        "join_key": "attempt_name plus side",
        "time_axis": "closed trade sequence",
        "branch_specific_rule": "Long and short may be diagnosed separately but cannot be dropped to create a candidate.",
        "lookahead_guard": "No side drop, side flip, or side-specific threshold retune.",
        "output_grain": "branch_name x attempt_name x side plus combined",
        "usable_for": "direction fragility attribution",
        "not_usable_for": "side-filtered selection",
        "missing_policy": "blocked_for_direction_claim",
    },
    {
        "metric_id": "curve_pocket",
        "metric_family": "curve_quality",
        "definition": "Worst rolling trade window, worst equity pocket, pocket length, and recovery after pocket.",
        "source_required": "parsed trade ledger ordered by close time",
        "join_key": "attempt_name plus trade sequence",
        "time_axis": "closed trade order; optional telemetry bar join",
        "branch_specific_rule": "Use predeclared rolling windows; do not choose calendar windows after seeing damage.",
        "lookahead_guard": "No direct forward pocket exclusion.",
        "output_grain": "branch_name x attempt_name x rolling_window",
        "usable_for": "curve stability and pocket failure memory",
        "not_usable_for": "date/month/hour veto without timestamp-safe predeclared feature design",
        "missing_policy": "blocked_for_curve_pocket_claim",
    },
    {
        "metric_id": "underwater_stretch",
        "metric_family": "drawdown_path",
        "definition": "Bars/trades spent below prior equity high, longest underwater stretch, drawdown depth, and recovery length.",
        "source_required": "parsed trade/equity sequence; report chart only as secondary visual",
        "join_key": "attempt_name plus trade sequence",
        "time_axis": "closed trade order and telemetry bar time",
        "branch_specific_rule": "Compute sequence metrics from runtime evidence, not proxy aggregates.",
        "lookahead_guard": "No stopping after favorable recovery only.",
        "output_grain": "branch_name x attempt_name",
        "usable_for": "drawdown and recovery quality diagnosis",
        "not_usable_for": "declaring runtime authority",
        "missing_policy": "blocked_for_underwater_claim",
    },
    {
        "metric_id": "cost_stress",
        "metric_family": "spread_slippage_stress",
        "definition": "Reprice each trade under predeclared extra spread and slippage grids, then recompute net/PF/DD and pocket metrics.",
        "source_required": "trade ledger with side, volume, entry, exit, point value, and lot",
        "join_key": "attempt_name plus trade_id",
        "time_axis": "trade open and close time",
        "branch_specific_rule": "Apply identical stress grid to every branch and attempt.",
        "lookahead_guard": "No stress grid picked after outcomes.",
        "output_grain": "branch_name x attempt_name x stress_grid",
        "usable_for": "cost fragility diagnosis",
        "not_usable_for": "spread/slippage optimized retune",
        "missing_policy": "blocked_for_cost_stress_claim",
    },
    {
        "metric_id": "lot_normalized",
        "metric_family": "position_size_normalization",
        "definition": "Profit, loss, expectancy, and DD normalized by executed lot and by one-lot equivalent where possible.",
        "source_required": "trade ledger executed volume plus report profit",
        "join_key": "attempt_name plus trade_id",
        "time_axis": "closed trade sequence",
        "branch_specific_rule": "Normalize for interpretation only; never optimize lot.",
        "lookahead_guard": "No lot change or scale fitting.",
        "output_grain": "branch_name x attempt_name",
        "usable_for": "separating edge shape from lot scale",
        "not_usable_for": "lot optimization",
        "missing_policy": "blocked_for_lot_normalized_claim",
    },
    {
        "metric_id": "session_hour_regime",
        "metric_family": "regime_attribution",
        "definition": "Trade and signal attribution by session, hour, month, volatility, ADX, VIX, USD, and rate-regime bins.",
        "source_required": "trade ledger joined to telemetry and predeclared feature/regime columns",
        "join_key": "attempt_name plus entry bar time",
        "time_axis": "entry bar close/server time",
        "branch_specific_rule": "Regime bins are explanatory slices, not outcome-chosen filters.",
        "lookahead_guard": "No calendar or regime exclusion after seeing results.",
        "output_grain": "branch_name x attempt_name x predeclared_regime_bin",
        "usable_for": "macro/state attribution and overfit diagnosis",
        "not_usable_for": "post-hoc regime filter selection",
        "missing_policy": "blocked_for_regime_claim",
    },
    {
        "metric_id": "runtime_identity",
        "metric_family": "runtime_parity",
        "definition": "Feature, model, set, telemetry, report, row-level probability, and decision identity for each attempt.",
        "source_required": "run335K handoff manifest and run335L parity summary",
        "join_key": "attempt_name",
        "time_axis": "feature row and telemetry cycle bar time",
        "branch_specific_rule": "Branch metrics are accepted only if runtime identity remains unchanged.",
        "lookahead_guard": "No silent handoff, threshold, or feature-order change.",
        "output_grain": "attempt_name",
        "usable_for": "runtime parity gate",
        "not_usable_for": "runtime authority without fresh reviewed output",
        "missing_policy": "blocked_for_runtime_claim",
    },
    {
        "metric_id": "subject_boundary",
        "metric_family": "negative_control",
        "definition": "Reject cp322A-exact or subject-swap evidence when the report/model/handoff identity differs.",
        "source_required": "run335D payloads, run335F protocols, run335K runtime identities",
        "join_key": "branch_name plus attempt_name",
        "time_axis": "not_applicable_identity_gate",
        "branch_specific_rule": "Control branches cannot be promoted; they test boundary discipline.",
        "lookahead_guard": "No positive inference from mismatched subject.",
        "output_grain": "branch_name x attempt_name",
        "usable_for": "boundary enforcement",
        "not_usable_for": "candidate selection",
        "missing_policy": "blocked_for_subject_boundary_claim",
    },
    {
        "metric_id": "tier_view",
        "metric_family": "tier_scope",
        "definition": "Tier A separate, Tier B separate or fallback, and routed total records where data exists.",
        "source_required": "telemetry active_tier and branch protocol measurement plan",
        "join_key": "attempt_name plus tier",
        "time_axis": "telemetry cycle bar time",
        "branch_specific_rule": "Tier A and Tier B must be labeled separately before combined interpretation.",
        "lookahead_guard": "No Tier B omission when claim needs paired tier evidence.",
        "output_grain": "branch_name x attempt_name x tier_scope",
        "usable_for": "paired tier exploration discipline",
        "not_usable_for": "overstating Tier A as full system",
        "missing_policy": "missing_required_or_out_of_scope_by_claim",
    },
]


BRANCH_METRIC_MAP: dict[str, list[str]] = {
    "cost_spread_slippage_grid_guard": [
        "trade_ledger",
        "headline_kpi",
        "cost_stress",
        "lot_normalized",
        "curve_pocket",
    ],
    "curve_noncalendar_state_holdout": [
        "trade_ledger",
        "curve_pocket",
        "underwater_stretch",
        "session_hour_regime",
        "headline_kpi",
    ],
    "direction_symmetry_no_side_drop": [
        "trade_ledger",
        "direction_attribution",
        "headline_kpi",
        "curve_pocket",
    ],
    "drawdown_underwater_recovery_quality": [
        "trade_ledger",
        "underwater_stretch",
        "curve_pocket",
        "headline_kpi",
    ],
    "regime_predeclared_macro_state": [
        "trade_ledger",
        "session_hour_regime",
        "direction_attribution",
        "headline_kpi",
    ],
    "runtime_identity_strict_handoff": [
        "runtime_identity",
        "trade_ledger",
        "headline_kpi",
    ],
    "cp322a_exact_blocker_control": [
        "subject_boundary",
        "runtime_identity",
        "trade_ledger",
    ],
    "cost_curve_drawdown_interaction_guard": [
        "trade_ledger",
        "cost_stress",
        "curve_pocket",
        "underwater_stretch",
        "lot_normalized",
    ],
    "regime_direction_interaction_guard": [
        "trade_ledger",
        "session_hour_regime",
        "direction_attribution",
        "curve_pocket",
    ],
    "subject_swap_negative_control": [
        "subject_boundary",
        "runtime_identity",
        "direction_attribution",
    ],
    "null_adjacent_period_control": [
        "subject_boundary",
        "trade_ledger",
        "headline_kpi",
        "curve_pocket",
        "session_hour_regime",
    ],
}


def schema_by_id() -> dict[str, dict[str, str]]:
    return {row["metric_id"]: row for row in METRIC_SCHEMA}


def json_loads_safe(value: str) -> Any:
    try:
        return json.loads(value)
    except Exception:
        return value


def build_contract_rows(protocols: Sequence[Mapping[str, str]], comparison_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    comparison_by_branch = {row.get("branch_name", ""): row for row in comparison_rows}
    schemas = schema_by_id()
    rows: list[dict[str, Any]] = []
    for protocol in protocols:
        branch_name = protocol.get("branch_name", "")
        branch_id = protocol.get("branch_id", "")
        comparison = comparison_by_branch.get(branch_name, {})
        dimensions = json_loads_safe(comparison.get("comparison_dimensions", "[]"))
        for metric_id in BRANCH_METRIC_MAP.get(branch_name, ["trade_ledger", "headline_kpi", "runtime_identity"]):
            schema = schemas[metric_id]
            if metric_id == "cost_stress":
                extraction_method = "parse_trade_ledger_then_apply_predeclared_spread_slippage_grid"
                required_runtime_source = "trade_ledger_with_side_volume_entry_exit_profit"
            elif metric_id in {"curve_pocket", "underwater_stretch"}:
                extraction_method = "order_closed_trades_then_compute_predeclared_rolling_curve_and_underwater_windows"
                required_runtime_source = "trade_ledger_or_structured_equity_curve"
            elif metric_id == "session_hour_regime":
                extraction_method = "join_trade_entry_time_to_telemetry_and_predeclared_feature_regime_bins"
                required_runtime_source = "trade_ledger_plus_runtime_telemetry_plus_feature_matrix"
            elif metric_id == "direction_attribution":
                extraction_method = "group_parsed_trade_ledger_by_long_short_and_combined_total"
                required_runtime_source = "trade_ledger_side_field"
            elif metric_id == "runtime_identity":
                extraction_method = "reuse_run335L_row_level_parity_and_handoff_hashes"
                required_runtime_source = "run335L_parity_summary_and_run335K_handoff_manifest"
            elif metric_id == "subject_boundary":
                extraction_method = "compare_branch_subject_to_report_model_set_identity_and_reject_mismatches"
                required_runtime_source = "run335D_payloads_run335F_protocols_run335K_runtime_identity"
            elif metric_id == "tier_view":
                extraction_method = "split_telemetry_and_trade_join_by_active_tier_or_mark_missing_required"
                required_runtime_source = "runtime_telemetry_active_tier_and_trade_join"
            else:
                extraction_method = "parse_or_reconcile_mt5_report_summary_with_trade_ledger"
                required_runtime_source = schema["source_required"]
            rows.append(
                {
                    "protocol_id": protocol.get("protocol_id", ""),
                    "branch_id": branch_id,
                    "branch_name": branch_name,
                    "metric_id": metric_id,
                    "metric_family": schema["metric_family"],
                    "required_runtime_source": required_runtime_source,
                    "extraction_method": extraction_method,
                    "comparison_dimensions_from_run335F": dimensions,
                    "branch_specific_acceptance_rule": "metric_value_must_vary_by_branch_or_be_explicitly_identity_wide; repeated_aggregate_proxy_is_context_only",
                    "no_retune_rule": "model_threshold_lot_risk_stop_target_feature_order_and_handoff_remain_fixed",
                    "lookahead_guard": schema["lookahead_guard"],
                    "selection_eligible": "false",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def build_source_audit(attempt_rows: Sequence[Mapping[str, str]], protocols: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    report_paths = [Path(str(row.get("report_path", ""))) for row in read_csv_rows(RUN335K_DIR / "mt5_fresh_runtime_probe_summary.csv")]
    existing_reports = [path for path in report_paths if str(path) and io_path(path).exists()]
    telemetry_files = list(io_path(RUN335K_DIR / "runtime_telemetry").glob("*_telemetry.csv"))
    feature_files = list(io_path(RUN335K_DIR / "feature_matrices").glob("*_features.csv"))
    html_count = len(existing_reports)
    telemetry_count = len(telemetry_files)
    feature_count = len(feature_files)
    branch_count = len(protocols)
    attempt_count = len(attempt_rows)
    return [
        {
            "source_id": "run335F_protocol_design",
            "availability": "available",
            "path": rel(RUN335F_DIR / "probe_protocol_design_matrix.csv"),
            "row_count_or_count": branch_count,
            "supports_metrics": "branch list, branch intent, no-retune contract",
            "branch_specific_status": "available_design_only",
            "missing_or_repair_needed": "none",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "source_id": "run335D_branch_payloads",
            "availability": "available",
            "path": rel(RUN335D_DIR / "branch_input_package_manifest.csv"),
            "row_count_or_count": len(read_csv_rows(RUN335D_DIR / "branch_input_package_manifest.csv")),
            "supports_metrics": "failure axes, subject boundary, negative controls",
            "branch_specific_status": "available_design_only",
            "missing_or_repair_needed": "none",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "source_id": "run335K_mt5_html_reports",
            "availability": "available_with_parser_needed" if html_count == attempt_count else "partial_or_missing",
            "path": rel(RUN335K_DIR / "mt5" / "reports"),
            "row_count_or_count": html_count,
            "supports_metrics": "trade ledger, headline KPI, curve, cost stress, lot-normalized result",
            "branch_specific_status": "not_materialized_yet",
            "missing_or_repair_needed": "run335N_parse_html_trade_deal_ledger",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "source_id": "run335K_runtime_telemetry",
            "availability": "available",
            "path": rel(RUN335K_DIR / "runtime_telemetry"),
            "row_count_or_count": telemetry_count,
            "supports_metrics": "row-level signal, probability, active tier, entry-time join context",
            "branch_specific_status": "available_for_join_not_trade_pnl",
            "missing_or_repair_needed": "join_to_parsed_trade_ledger",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "source_id": "run335K_feature_matrices",
            "availability": "available",
            "path": rel(RUN335K_DIR / "feature_matrices"),
            "row_count_or_count": feature_count,
            "supports_metrics": "feature/regime bin joins and feature-order identity",
            "branch_specific_status": "available_for_predeclared_regime_join",
            "missing_or_repair_needed": "document_exact_regime_columns_in_run335N",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "source_id": "run335L_row_level_runtime_parity",
            "availability": "available",
            "path": rel(RUN335L_DIR / "row_level_runtime_parity_summary.csv"),
            "row_count_or_count": len(read_csv_rows(RUN335L_DIR / "row_level_runtime_parity_summary.csv")),
            "supports_metrics": "runtime identity gate and probability/decision parity",
            "branch_specific_status": "usable_as_identity_gate",
            "missing_or_repair_needed": "none_for_signal_parity; still not numeric branch KPI",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "source_id": "structured_trade_ledger_csv",
            "availability": "missing",
            "path": rel(RUN_DIR / "run335N_expected_trade_ledgers"),
            "row_count_or_count": 0,
            "supports_metrics": "all branch-specific numeric KPI and cost/curve attribution",
            "branch_specific_status": "required_missing",
            "missing_or_repair_needed": "materialize_in_run335N_before_any_forward_decision",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "source_id": "structured_equity_curve_csv",
            "availability": "missing_or_derivable",
            "path": rel(RUN_DIR / "run335N_expected_equity_curves"),
            "row_count_or_count": 0,
            "supports_metrics": "underwater stretch and curve pocket",
            "branch_specific_status": "required_missing",
            "missing_or_repair_needed": "derive_from_trade_ledger_or_report_if_supported",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_lookahead_rows(protocols: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    base = [
        (
            "no_outcome_chosen_date_window",
            "date/month/hour/pocket windows cannot be selected after seeing runtime profit",
            "use predeclared rolling trade windows and predeclared session/hour/regime bins only",
        ),
        (
            "no_threshold_or_margin_retune",
            "score threshold and D/B surface cannot move after new data is observed",
            "all extraction rows carry fixed-threshold identity and no-retune rule",
        ),
        (
            "no_lot_or_cost_grid_optimization",
            "lot and spread/slippage grid cannot be chosen to rescue KPI",
            "cost grid is predeclared and applied uniformly to all branches/attempts",
        ),
        (
            "no_side_drop",
            "long or short cannot be removed because one side is weak",
            "direction report always includes long, short, and combined total",
        ),
        (
            "no_subject_swap",
            "positive result from nonmatching report/model/handoff cannot prove cp322A exact or another subject",
            "subject boundary metric rejects mismatch and marks control-only",
        ),
        (
            "no_proxy_aggregate_promotion",
            "repeated aggregate proxy numbers cannot stand in for branch-specific runtime outcome",
            "run335N must parse trade ledger and recompute branch metrics",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for protocol in protocols:
        for guard_id, rejected_path, enforcement in base:
            rows.append(
                {
                    "branch_id": protocol.get("branch_id", ""),
                    "branch_name": protocol.get("branch_name", ""),
                    "guard_id": guard_id,
                    "rejected_bias_path": rejected_path,
                    "enforcement": enforcement,
                    "materialization_check": "run335N_metric_tables_must_include_guard_columns_before_interpretation",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def report_for_attempt(attempt_name: str, summary_rows: Sequence[Mapping[str, str]]) -> Path | None:
    for row in summary_rows:
        if row.get("attempt_name") == attempt_name and row.get("report_path"):
            return Path(row["report_path"])
    return None


def count_text(path: Path, patterns: Sequence[str]) -> dict[str, int]:
    if not path or not io_path(path).exists():
        return {pattern: 0 for pattern in patterns}
    raw = io_path(path).read_text(encoding="utf-16", errors="ignore")
    if not raw.strip():
        raw = io_path(path).read_text(encoding="utf-8", errors="ignore")
    low = raw.lower()
    return {pattern: low.count(pattern.lower()) for pattern in patterns}


def build_parser_audit(summary_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in summary_rows:
        attempt_name = row.get("attempt_name", "")
        report_path = Path(row.get("report_path", "")) if row.get("report_path") else None
        exists = bool(report_path and io_path(report_path).exists())
        patterns = ["<tr", "<td", "Deals", "Orders", "거래", "주문", "Balance", "잔고", "Equity", "Profit", "수익"]
        counts = count_text(report_path, patterns) if exists and report_path else {}
        if exists and (counts.get("<tr", 0) and (counts.get("거래", 0) or counts.get("주문", 0) or counts.get("Deals", 0) or counts.get("Orders", 0))):
            feasibility = "parser_feasible_report_contains_structured_rows_and_trade_tokens"
        elif exists:
            feasibility = "report_exists_parser_structure_requires_manual_probe"
        else:
            feasibility = "report_missing"
        rows.append(
            {
                "attempt_name": attempt_name,
                "artifact_slug": row.get("artifact_slug", ""),
                "report_path": rel(report_path) if report_path else "",
                "report_exists": exists,
                "html_sha256": sha256_bytes(report_path) if exists and report_path else "",
                "html_tr_token_count": counts.get("<tr", 0),
                "html_td_token_count": counts.get("<td", 0),
                "deals_token_count": counts.get("Deals", 0),
                "orders_token_count": counts.get("Orders", 0),
                "korean_trade_token_count": counts.get("거래", 0),
                "korean_order_token_count": counts.get("주문", 0),
                "balance_token_count": counts.get("Balance", 0),
                "korean_balance_token_count": counts.get("잔고", 0),
                "equity_token_count": counts.get("Equity", 0),
                "profit_token_count": counts.get("Profit", 0),
                "korean_profit_token_count": counts.get("수익", 0),
                "parser_feasibility": feasibility,
                "next_action": "run335N_parse_mt5_html_trade_deal_ledger_v1",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_queue_rows(protocols: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    common_tasks = [
        (
            1,
            "parse_mt5_html_trade_deal_ledger_v1",
            "Parse the six run335K MT5 HTML reports into one normalized trade/deal ledger.",
            "stages/335_overfit_guard__failure_memory_constrained_research_handoff/02_runs/run335N/runtime_trade_ledger.csv",
            "No metric interpretation if ticket/time/side/volume/profit fields are absent.",
        ),
        (
            2,
            "join_trade_ledger_to_runtime_telemetry_v1",
            "Join closed trades to runtime telemetry by attempt and nearest valid entry/close bar without future shifting.",
            "stages/335_overfit_guard__failure_memory_constrained_research_handoff/02_runs/run335N/trade_telemetry_join_audit.csv",
            "Reject joins that require future bars or ambiguous duplicate timestamps.",
        ),
        (
            3,
            "compute_branch_metric_tables_v1",
            "Emit branch x attempt headline KPI, trade density, direction, and tier tables from structured runtime evidence.",
            "stages/335_overfit_guard__failure_memory_constrained_research_handoff/02_runs/run335N/branch_runtime_metric_matrix.csv",
            "Repeated aggregate proxy values remain context only.",
        ),
        (
            4,
            "compute_cost_slippage_stress_from_trade_ledger_v1",
            "Apply predeclared extra spread/slippage grids to each parsed trade and recompute net/PF/DD.",
            "stages/335_overfit_guard__failure_memory_constrained_research_handoff/02_runs/run335N/cost_stress_metric_matrix.csv",
            "No stress grid may be chosen from the realized outcome.",
        ),
        (
            5,
            "compute_curve_underwater_recovery_v1",
            "Compute worst rolling pockets, underwater stretches, and recovery quality from trade/equity sequence.",
            "stages/335_overfit_guard__failure_memory_constrained_research_handoff/02_runs/run335N/curve_pocket_underwater_matrix.csv",
            "No calendar pocket exclusion or cherry-picked window.",
        ),
        (
            6,
            "compute_regime_direction_slices_v1",
            "Join trade entries to session/hour/month/volatility/ADX/VIX/USD/rate-regime bins and long/short groups.",
            "stages/335_overfit_guard__failure_memory_constrained_research_handoff/02_runs/run335N/regime_direction_slice_matrix.csv",
            "Regime bins explain, they do not filter or retune.",
        ),
        (
            7,
            "emit_protocol_specific_proxy_mt5_difference_v1",
            "Compare branch-specific runtime metrics to proxy/context expectations with difference direction.",
            "stages/335_overfit_guard__failure_memory_constrained_research_handoff/02_runs/run335N/protocol_specific_proxy_mt5_difference.csv",
            "Usable only as diagnostic comparison, not pass/fail decision by itself.",
        ),
        (
            8,
            "negative_control_subject_boundary_recheck_v1",
            "Recheck cp322A exact blocker, subject swap, and adjacent-period controls against runtime identity.",
            "stages/335_overfit_guard__failure_memory_constrained_research_handoff/02_runs/run335N/negative_control_subject_boundary_audit.csv",
            "Any subject mismatch blocks positive inference.",
        ),
        (
            9,
            "write_run335N_decision_pack_v1",
            "Close run335N with gate audit, result judgment, reports, ledgers, and no Goal Achieve unless operational gate is truly met.",
            "stages/335_overfit_guard__failure_memory_constrained_research_handoff/03_reviews/run335N_branch_specific_runtime_metric_materialization.md",
            "Forward Passed/Failed remains unclaimed unless all required evidence exists.",
        ),
    ]
    rows: list[dict[str, Any]] = []
    branch_names = [row.get("branch_name", "") for row in protocols]
    for priority, task_id, action, expected_output, blocker_policy in common_tasks:
        rows.append(
            {
                "queue_id": f"run335N_q{priority:02d}_{task_id}",
                "priority": priority,
                "task_id": task_id,
                "scope": "all_attempts_all_protocols" if priority <= 2 else ",".join(branch_names),
                "action": action,
                "expected_output": expected_output,
                "acceptance_gate": "output_exists_with_nonempty_rows_and_claim_boundary",
                "blocker_policy": blocker_policy,
                "no_retune_guard": "no_model_training_no_threshold_change_no_lot_change_no_feature_order_change",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_gate_rows(
    protocol_rows: Sequence[Mapping[str, str]],
    contract_rows: Sequence[Mapping[str, Any]],
    source_rows: Sequence[Mapping[str, Any]],
    parser_rows: Sequence[Mapping[str, Any]],
    queue_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    missing_structured_sources = [row for row in source_rows if str(row.get("availability")) in {"missing", "missing_or_derivable"}]
    parser_existing = sum(1 for row in parser_rows if str(row.get("report_exists")) == "True" or row.get("report_exists") is True)
    return [
        {
            "gate_id": "source_run335L_proxy_gap_loaded",
            "status": "passed",
            "evidence": rel(RUN335L_DIR / "proxy_numeric_protocol_specificity_audit.csv"),
            "finding": "numeric proxy is repeated aggregate and cannot decide branch-specific forward robustness",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "protocol_count_preserved",
            "status": "passed" if len(protocol_rows) == 11 else "failed",
            "evidence": rel(RUN335F_DIR / "probe_protocol_design_matrix.csv"),
            "finding": f"protocol_count={len(protocol_rows)}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "branch_specific_metric_contract_created",
            "status": "passed" if contract_rows else "failed",
            "evidence": rel(CONTRACT_CSV),
            "finding": f"contract_rows={len(contract_rows)}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "mt5_report_parser_feasibility_named",
            "status": "passed_with_boundary" if parser_existing else "failed",
            "evidence": rel(PARSER_AUDIT_CSV),
            "finding": f"reports_existing={parser_existing}; parser still materialized in run335N",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "structured_trade_ledger_gap_named",
            "status": "passed_with_boundary" if missing_structured_sources else "failed",
            "evidence": rel(SOURCE_AUDIT_CSV),
            "finding": "structured trade/equity ledger missing is explicitly queued, so no positive forward claim is made",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "lookahead_bias_rejection_matrix_created",
            "status": "passed",
            "evidence": rel(LOOKAHEAD_CSV),
            "finding": "date/hour/regime/side/stress/subject post-hoc bias paths are rejected before materialization",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "run335N_materialization_queue_created",
            "status": "passed" if len(queue_rows) >= 8 else "failed",
            "evidence": rel(QUEUE_CSV),
            "finding": f"queue_rows={len(queue_rows)}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "no_retune_no_selection_no_goal_achieve",
            "status": "passed",
            "evidence": rel(RESULT_JUDGMENT_CSV),
            "finding": "model/threshold/lot/risk/handoff are unchanged; no Forward Passed/Failed and no Goal Achieve",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def write_receipts(outputs: Sequence[Path], metrics: Mapping[str, Any]) -> list[Path]:
    common = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "outputs": [rel(path) for path in outputs],
        "metrics": dict(metrics),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    receipts = {
        "experiment_design_receipt.json": {
            **common,
            "hypothesis": "Branch-specific runtime extraction can replace repeated aggregate proxy values with auditable MT5-derived metrics.",
            "decision_use": "Authorize run335N extractor materialization and prevent forward pass/fail claims until structured trade metrics exist.",
            "comparison_baseline": "run335L row-level parity plus repeated aggregate numeric proxy audit.",
            "control_variables": "ONNX, feature order, threshold, D/B surface, risk, lot, ATR SL/TP, and runtime handoff remain fixed.",
            "changed_variables": "measurement extraction schema and materialization queue only.",
            "success_criteria": "All 11 protocols receive branch-specific metric contracts and no-retune/lookahead guards.",
            "failure_criteria": "Any branch needs post-outcome filter, threshold change, or missing source is hidden.",
            "invalid_conditions": "HTML report absent, ambiguous timestamp join, subject mismatch, or parsed trade ledger missing for a numeric claim.",
            "stop_conditions": "Stop at design boundary; materialize extractors in run335N before interpretation.",
            "evidence_plan": [rel(SCHEMA_CSV), rel(CONTRACT_CSV), rel(QUEUE_CSV), rel(GATE_AUDIT_CSV)],
        },
        "runtime_parity_receipt.json": {
            **common,
            "research_path": rel(Path("stage_pipelines/stage335/design_branch_specific_runtime_metric_extraction.py")),
            "runtime_path": rel(RUN335K_DIR / "mt5"),
            "shared_contract": "fixed feature/model/threshold/risk/handoff identity from run335K and run335L row-level parity.",
            "known_differences": "Numeric proxy values are repeated aggregate context only; trade ledger is not yet materialized.",
            "parity_check": "run335L row-level probability and decision parity reused as identity gate.",
            "runtime_claim_boundary": "runtime_probe_design_only_no_runtime_authority",
        },
        "data_integrity_receipt.json": {
            **common,
            "data_source": "run335K MT5 reports, telemetry, feature matrices, run335F protocols, run335D payloads, run335L parity audit.",
            "time_axis": "MT5 broker server time; trade entry/close times join to telemetry without future shifting.",
            "sample_scope": "US100 M5 run335K fresh runtime attempts for six non-identity surfaces and 11 Stage335 protocols.",
            "feature_label_boundary": "No model training or label use occurs; regime joins are explanatory and predeclared.",
            "split_boundary": "Forward runtime evidence only, research-development interpretation boundary.",
            "leakage_risk": "Post-hoc date/hour/regime/side exclusion or using repeated proxy aggregate as branch result.",
            "integrity_judgment": "usable_with_boundary_design_only_trade_ledger_missing_until_run335N",
        },
        "artifact_lineage_receipt.json": {
            **common,
            "source_inputs": [
                rel(RUN335F_DIR / "probe_protocol_design_matrix.csv"),
                rel(RUN335F_DIR / "proxy_mt5_comparison_contract.csv"),
                rel(RUN335D_DIR / "branch_input_package_manifest.csv"),
                rel(RUN335K_DIR / "mt5_fresh_runtime_probe_summary.csv"),
                rel(RUN335L_DIR / "proxy_numeric_protocol_specificity_audit.csv"),
            ],
            "producer": "python stage_pipelines/stage335/design_branch_specific_runtime_metric_extraction.py",
            "consumer": NEXT_RUN_ID,
            "availability": "tracked_design_outputs_plus_ignored_run_dir_force_added",
            "lineage_judgment": "connected_with_boundary_trade_ledger_not_yet_materialized",
        },
        "result_judgment_receipt.json": {
            **common,
            "result_subject": "run335M branch-specific runtime metric extraction design",
            "evidence_available": [rel(SCHEMA_CSV), rel(CONTRACT_CSV), rel(SOURCE_AUDIT_CSV), rel(QUEUE_CSV)],
            "evidence_missing": "Structured parsed trade ledger and branch-specific runtime KPI tables are still pending run335N.",
            "judgment_label": "exploratory_design_completed_no_forward_decision",
            "next_condition": "run335N must parse MT5 reports and emit branch-specific metric matrices before forward interpretation.",
        },
    }
    receipt_paths: list[Path] = []
    for name, payload in receipts.items():
        path = RUN_DIR / name
        write_json(path, payload)
        receipt_paths.append(path)
    return receipt_paths


def write_reports(metrics: Mapping[str, Any]) -> None:
    report = f"""
# Run335M Branch-Specific Runtime Metric Extraction Design(335M 분기별 런타임 지표 추출 설계)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- decision(판정): `{DECISION}`
- branch_count(분기 수): `{metrics['branch_count']}`
- contract_rows(계약 행): `{metrics['contract_rows']}`
- parser_report_count(파서 보고서 수): `{metrics['parser_report_count']}`
- queue_rows(대기열 행): `{metrics['queue_rows']}`
- next_action(다음 행동): `{NEXT_RUN_ID}`

## Judgment(판정)

run335M(335M 실행)은 run335L(335L 실행)의 핵심 한계인 repeated aggregate proxy(반복 집계 프록시)를 분기별 런타임 지표(runtime metric, 실행 지표) 계약으로 바꿨다.

Effect(효과): 다음 run335N(335N 실행)은 MT5 HTML report(HTML 보고서), telemetry(기록), feature matrix(피처 행렬)를 구조화해서 trade ledger(거래 장부), cost stress(비용 압박), curve pocket(곡선 포켓), underwater stretch(수중 구간), long/short attribution(롱/숏 귀속), regime attribution(국면 귀속)을 실제 분기별 표로 만들 수 있다.

## Evidence(근거)

- metric_schema(지표 구조): `{rel(SCHEMA_CSV)}`
- extraction_contract(추출 계약): `{rel(CONTRACT_CSV)}`
- source_audit(원천 감사): `{rel(SOURCE_AUDIT_CSV)}`
- parser_feasibility(파서 가능성): `{rel(PARSER_AUDIT_CSV)}`
- lookahead_rejection(미래정보 편향 거절): `{rel(LOOKAHEAD_CSV)}`
- run335N_queue(335N 대기열): `{rel(QUEUE_CSV)}`
- gate_audit(게이트 감사): `{rel(GATE_AUDIT_CSV)}`
- result_judgment(결과 판정): `{rel(RESULT_JUDGMENT_CSV)}`

## Boundary(경계)

이 실행은 설계와 계약이다. 모델(model, 모델), threshold(임계값), lot(로트), risk logic(위험 로직), feature order(피처 순서), runtime handoff(런타임 인계)는 바꾸지 않았다.

Forward Passed(전진 통과), Forward Failed(전진 실패), runtime authority(런타임 권위), live readiness(실거래 준비), deployment(배포), operating promotion(운영 승격), Goal Achieve(목표 달성)는 모두 `not_claimed`다.
"""
    write_md(REPORT_DOC, report)
    decision = f"""
# Decision(판정): Stage335M Branch-Specific Runtime Metric Extraction Design(분기별 런타임 지표 추출 설계)

`{RUN_ID}`은 branch-specific metric extraction contract(분기별 지표 추출 계약)를 완료했다.

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- contract_rows(계약 행): `{metrics['contract_rows']}`
- source_audit_rows(원천 감사 행): `{metrics['source_rows']}`
- parser_report_count(파서 보고서 수): `{metrics['parser_report_count']}`
- run335N_queue_rows(335N 대기열 행): `{metrics['queue_rows']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`

Effect(효과): run335L(335L 실행)에서 반복 집계였던 proxy numeric value(프록시 숫자값)를 더 이상 분기별 판정 근거로 쓰지 않고, run335N(335N 실행)의 구조화된 MT5 trade ledger(거래 장부)와 branch metric matrix(분기 지표 행렬)로 넘어간다.
"""
    write_md(DECISION_DOC, decision)


def update_workspace_documents(metrics: Mapping[str, Any]) -> None:
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_line(workspace_text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    focus_line = (
        "  Stage335(335단계) run335M(335M 실행)는 "
        f"`{STATUS}`로 branch-specific runtime metric extraction contract(분기별 런타임 지표 추출 계약)를 완료했다. "
        f"Effect(효과): contract rows(계약 행) `{metrics['contract_rows']}`개, parser feasibility rows(파서 가능성 행) "
        f"`{metrics['parser_report_count']}`개, run335N queue(335N 대기열) `{metrics['queue_rows']}`개를 만들고 "
        "Forward Passed/Failed(전진 통과/실패)와 Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    if "run335M(335M 실행)" not in workspace_text:
        workspace_text = workspace_text.replace("current_focus:\n", f"current_focus:\n- >-\n{focus_line}\n", 1)
    write_text_lossless(WORKSPACE_STATE, workspace_text, workspace_bom)

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    current_text = replace_line(current_text, "- current_packet", "- current_packet(현재 작업 묶음): `335_overfit_guard__failure_memory_constrained_research_handoff_v14`")
    current_text = replace_line(current_text, "- current_run", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    current_text = replace_line(current_text, "- status", f"- status(상태): `{STATUS}`")
    current_text = replace_line(current_text, "- decision", f"- decision(판정): `{DECISION}`")
    summary_line = (
        f"- run335M_summary(335M 요약): branch-specific runtime metric extraction design(분기별 런타임 지표 추출 설계)을 "
        f"`{STATUS}`로 완료했다. Effect(효과): contract rows(계약 행) `{metrics['contract_rows']}`개와 "
        f"run335N materialization queue(335N 물질화 대기열) `{metrics['queue_rows']}`개를 만들어 repeated aggregate proxy(반복 집계 프록시)를 "
        "분기별 forward judgment(전진 판정) 근거로 쓰는 경로를 차단했다."
    )
    if "run335M_summary(335M 요약)" not in current_text:
        current_text = current_text.replace("- run335L_summary", summary_line + "\n- run335L_summary", 1)
    write_text_lossless(CURRENT_STATE, current_text, current_bom)

    selection_text, selection_bom = read_text_lossless(SELECTED_DIR / "selection_status.md")
    selection_text = replace_line(selection_text, "- latest_design", f"- latest_design(최신 설계): `{RUN_ID}`")
    selection_text = replace_line(selection_text, "- current_run", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    selection_text = replace_line(selection_text, "- next_action", f"- next_action(다음 행동): `{NEXT_RUN_ID}`")
    selection_text = replace_line(
        selection_text,
        "- effect",
        "- effect(효과): Stage335M(335M 실행)은 분기별 runtime metric extraction contract(런타임 지표 추출 계약)를 만들었고, structured trade ledger(구조화 거래 장부)가 run335N(335N 실행)에서 나오기 전까지 Forward Passed/Failed(전진 통과/실패)와 Goal Achieve(목표 달성)를 주장하지 않는다.",
    )
    selection_text = replace_line(selection_text, "- latest_review", f"- latest_review(최신 검토): `{RUN_ID}`")
    write_text_lossless(SELECTED_DIR / "selection_status.md", selection_text, selection_bom)

    brief_text, brief_bom = read_text_lossless(STAGE_BRIEF)
    brief_text = replace_line(brief_text, "- latest_run", f"- latest_run(최신 실행): `{RUN_ID}`")
    write_text_lossless(STAGE_BRIEF, brief_text, brief_bom)

    input_body = f"""
- branch_specific_metric_schema(분기별 지표 구조): `{rel(SCHEMA_CSV)}`
- branch_runtime_metric_extraction_contract(분기별 런타임 지표 추출 계약): `{rel(CONTRACT_CSV)}`
- metric_source_availability_audit(지표 원천 가용성 감사): `{rel(SOURCE_AUDIT_CSV)}`
- mt5_report_parser_feasibility_audit(MT5 보고서 파서 가능성 감사): `{rel(PARSER_AUDIT_CSV)}`
- lookahead_bias_rejection_matrix(미래정보 편향 거절 행렬): `{rel(LOOKAHEAD_CSV)}`
- run335N_metric_materialization_queue(335N 지표 물질화 대기열): `{rel(QUEUE_CSV)}`
- decision(결정): `{rel(DECISION_DOC)}`
"""
    append_or_replace_section(INPUT_REFS, "run335M Branch-Specific Metric Extraction Design(335M 분기별 지표 추출 설계)", input_body)

    changelog_body = f"""
- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- effect(효과): branch-specific metric contract(분기별 지표 계약) `{metrics['contract_rows']}`개와 run335N queue(335N 대기열) `{metrics['queue_rows']}`개를 만들었다.
- boundary(경계): structured trade ledger(구조화 거래 장부)가 아직 없으므로 Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 `not_claimed`.
"""
    append_or_replace_section(CHANGELOG, "2026-05-26 Stage335M Branch-Specific Metric Extraction Design(335M 분기별 지표 추출 설계)", changelog_body)


def update_registers(outputs: Sequence[Path], metrics: Mapping[str, Any]) -> None:
    report_rel = rel(REPORT_DOC)
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "stage335_branch_specific_runtime_metric_extraction_design",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": report_rel,
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__branch_specific_metric_contract",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "branch_specific_runtime_metric_extraction_design",
                "tier_scope": "Tier A/Tier B paired measurement contract",
                "kpi_scope": "metric_contract_only_no_new_trading_kpi",
                "scoreboard_lane": "runtime_metric_extraction_repair",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": report_rel,
                "primary_kpi": f"contract_rows={metrics['contract_rows']};queue_rows={metrics['queue_rows']}",
                "guardrail_kpi": "no_retune;lookahead_rejected;forward_passed_not_claimed;goal_achieve_not_claimed",
                "external_verification_status": "design_only_reuses_run335K_reports_no_new_mt5",
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
                "ledger_row_id": f"{RUN_ID}__branch_specific_runtime_metric_contract",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "work_family": "runtime_metric_extraction_design",
                "evidence_scope": "run335K_mt5_reports_telemetry_features_and_run335L_proxy_gap",
                "kpi_scope": "design_only_no_new_trading_kpi",
                "status": STATUS,
                "judgment": JUDGMENT,
                "claim_boundary": CLAIM_BOUNDARY,
                "path": report_rel,
                "notes": f"contract_rows={metrics['contract_rows']};queue_rows={metrics['queue_rows']};structured_trade_ledger_pending.",
                "decision": f"{DECISION};next_action={NEXT_RUN_ID}",
            }
        ],
        key="ledger_row_id",
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{path.stem}",
            "artifact_type": "stage335_branch_specific_runtime_metric_extraction_design",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": now_utc(),
            "notes": "design_output_no_retune_no_forward_decision",
        }
        for path in outputs
    ]
    upsert_csv_rows(
        ARTIFACT_REGISTRY,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
        artifact_rows,
        key="artifact_id",
    )


def main() -> int:
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)

    protocols = read_csv_rows(RUN335F_DIR / "probe_protocol_design_matrix.csv")
    comparisons = read_csv_rows(RUN335F_DIR / "proxy_mt5_comparison_contract.csv")
    attempts = read_csv_rows(RUN335K_DIR / "independent_handoff_attempt_manifest.csv")
    runtime_summary = read_csv_rows(RUN335K_DIR / "mt5_fresh_runtime_probe_summary.csv")

    schema_rows = METRIC_SCHEMA
    contract_rows = build_contract_rows(protocols, comparisons)
    source_rows = build_source_audit(attempts, protocols)
    parser_rows = build_parser_audit(runtime_summary)
    lookahead_rows = build_lookahead_rows(protocols)
    queue_rows = build_queue_rows(protocols)
    gate_rows = build_gate_rows(protocols, contract_rows, source_rows, parser_rows, queue_rows)
    result_rows = [
        {
            "run_id": RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "evidence_available": "schema;contract;source_audit;parser_feasibility;lookahead_rejection;run335N_queue",
            "evidence_missing": "parsed_trade_ledger;branch_runtime_metric_matrix;cost_stress_matrix;curve_underwater_matrix",
            "forward_passed": "not_claimed",
            "forward_failed": "not_claimed",
            "runtime_authority": "not_claimed",
            "goal_achieve": "not_claimed",
            "next_action": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]

    write_csv(
        SCHEMA_CSV,
        [
            "metric_id",
            "metric_family",
            "definition",
            "source_required",
            "join_key",
            "time_axis",
            "branch_specific_rule",
            "lookahead_guard",
            "output_grain",
            "usable_for",
            "not_usable_for",
            "missing_policy",
        ],
        schema_rows,
    )
    write_csv(
        CONTRACT_CSV,
        [
            "protocol_id",
            "branch_id",
            "branch_name",
            "metric_id",
            "metric_family",
            "required_runtime_source",
            "extraction_method",
            "comparison_dimensions_from_run335F",
            "branch_specific_acceptance_rule",
            "no_retune_rule",
            "lookahead_guard",
            "selection_eligible",
            "claim_boundary",
        ],
        contract_rows,
    )
    write_csv(
        SOURCE_AUDIT_CSV,
        [
            "source_id",
            "availability",
            "path",
            "row_count_or_count",
            "supports_metrics",
            "branch_specific_status",
            "missing_or_repair_needed",
            "claim_boundary",
        ],
        source_rows,
    )
    write_csv(
        PARSER_AUDIT_CSV,
        [
            "attempt_name",
            "artifact_slug",
            "report_path",
            "report_exists",
            "html_sha256",
            "html_tr_token_count",
            "html_td_token_count",
            "deals_token_count",
            "orders_token_count",
            "korean_trade_token_count",
            "korean_order_token_count",
            "balance_token_count",
            "korean_balance_token_count",
            "equity_token_count",
            "profit_token_count",
            "korean_profit_token_count",
            "parser_feasibility",
            "next_action",
            "claim_boundary",
        ],
        parser_rows,
    )
    write_csv(
        LOOKAHEAD_CSV,
        [
            "branch_id",
            "branch_name",
            "guard_id",
            "rejected_bias_path",
            "enforcement",
            "materialization_check",
            "claim_boundary",
        ],
        lookahead_rows,
    )
    write_csv(
        QUEUE_CSV,
        [
            "queue_id",
            "priority",
            "task_id",
            "scope",
            "action",
            "expected_output",
            "acceptance_gate",
            "blocker_policy",
            "no_retune_guard",
            "claim_boundary",
        ],
        queue_rows,
    )
    write_csv(GATE_AUDIT_CSV, ["gate_id", "status", "evidence", "finding", "claim_boundary"], gate_rows)
    write_csv(
        RESULT_JUDGMENT_CSV,
        [
            "run_id",
            "status",
            "judgment",
            "decision",
            "evidence_available",
            "evidence_missing",
            "forward_passed",
            "forward_failed",
            "runtime_authority",
            "goal_achieve",
            "next_action",
            "claim_boundary",
        ],
        result_rows,
    )

    outputs = [SCHEMA_CSV, CONTRACT_CSV, SOURCE_AUDIT_CSV, PARSER_AUDIT_CSV, LOOKAHEAD_CSV, QUEUE_CSV, GATE_AUDIT_CSV, RESULT_JUDGMENT_CSV]
    metrics = {
        "branch_count": len(protocols),
        "schema_rows": len(schema_rows),
        "contract_rows": len(contract_rows),
        "source_rows": len(source_rows),
        "parser_report_count": sum(1 for row in parser_rows if row.get("report_exists") is True),
        "lookahead_rows": len(lookahead_rows),
        "queue_rows": len(queue_rows),
        "gate_rows": len(gate_rows),
    }
    receipts = write_receipts(outputs, metrics)
    outputs.extend(receipts)
    write_reports(metrics)
    outputs.extend([REPORT_DOC, DECISION_DOC])

    write_json(
        FINAL_DECISION_JSON,
        {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "metrics": metrics,
            "forward_passed": "not_claimed",
            "forward_failed": "not_claimed",
            "runtime_authority": "not_claimed",
            "goal_achieve": "not_claimed",
            "next_action": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    outputs.append(FINAL_DECISION_JSON)
    write_json(
        RUN_MANIFEST_JSON,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "parent_run_id": PARENT_RUN_ID,
            "stage_id": STAGE_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "command": "python stage_pipelines/stage335/design_branch_specific_runtime_metric_extraction.py",
            "artifacts": [rel(path) for path in outputs],
            "metrics": metrics,
            "selected_candidate": "none",
            "forward_passed": "not_claimed",
            "forward_failed": "not_claimed",
            "runtime_authority": "not_claimed",
            "goal_achieve": "not_claimed",
            "next_action": NEXT_RUN_ID,
            "generated_at_utc": now_utc(),
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    outputs.append(RUN_MANIFEST_JSON)

    update_workspace_documents(metrics)
    update_registers(outputs, metrics)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "decision": DECISION,
                "branch_count": metrics["branch_count"],
                "contract_rows": metrics["contract_rows"],
                "parser_report_count": metrics["parser_report_count"],
                "queue_rows": metrics["queue_rows"],
                "forward_passed": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_RUN_ID,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
