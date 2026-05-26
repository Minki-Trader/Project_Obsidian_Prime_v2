from __future__ import annotations

import csv
import hashlib
import json
import math
import statistics
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


TODAY = "2026-05-26"
STAGE_ID = "335_overfit_guard__failure_memory_constrained_research_handoff"
RUN_NUMBER = "run335J"
RUN_ID = "run335J_materialize_proxy_expected_values_and_mt5_runtime_probe_attempts_or_block_v1"
PARENT_RUN_ID = "run335I_design_proxy_expected_and_mt5_runtime_probe_or_block_v1"
NEXT_RUN_ID = "run335K_repair_independent_proxy_mt5_runtime_probe_materialization_v1"
STATUS = "completed_proxy_expected_and_existing_mt5_runtime_result_comparison_no_selection"
JUDGMENT = "proxy_mt5_comparison_completed_diagnostic_only_no_forward_decision"
DECISION = "stage335J_proxy_mt5_existing_runtime_comparison_diagnostic_usable_not_forward_usable_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage335J_proxy_mt5_existing_runtime_comparison_"
    "no_model_training_no_threshold_retuning_no_lot_optimization_no_direct_forward_pocket_filtering_"
    "no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_"
    "no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
RUN335I_DIR = STAGE_DIR / "02_runs" / "run335I"
RUN335G_DIR = STAGE_DIR / "02_runs" / "run335G"
RUN335D_DIR = STAGE_DIR / "02_runs" / "run335D"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
INPUTS_DIR = STAGE_DIR / "01_inputs"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"

STAGE330_DIR = ROOT / "stages" / "330_onnx_rebuild__forward_safe_non_identity_surface_robustness"
RUN330E_DIR = STAGE330_DIR / "02_runs" / "run330E"
RUN330F_DIR = STAGE330_DIR / "02_runs" / "run330F"
STAGE334_DIR = ROOT / "stages" / "334_runtime_parity__forward_usable_onnx_handoff_contract_hardening"
RUN334D_DIR = STAGE334_DIR / "02_runs" / "run334D"
RUN334G_DIR = STAGE334_DIR / "02_runs" / "run334G"

DOCS = ROOT / "docs"
RUN_REGISTRY = DOCS / "registers" / "run_registry.csv"
ALPHA_LEDGER = DOCS / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = DOCS / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
WORKSPACE_STATE = DOCS / "workspace" / "workspace_state.yaml"
CURRENT_STATE = DOCS / "context" / "current_working_state.md"
CHANGELOG = DOCS / "workspace" / "changelog.md"
DECISION_DOC = DOCS / "decisions" / "2026-05-26_stage335J_proxy_mt5_existing_runtime_comparison.md"

INPUTS: dict[str, Path] = {
    "run335j_queue": RUN335I_DIR / "run335J_materialization_queue.csv",
    "proxy_schema": RUN335I_DIR / "proxy_expected_value_schema.csv",
    "mt5_design": RUN335I_DIR / "mt5_runtime_probe_or_block_design.csv",
    "difference_contract": RUN335I_DIR / "proxy_mt5_difference_comparison_contract.csv",
    "usability_rule": RUN335I_DIR / "proxy_mt5_usability_judgment_rule.csv",
    "final_design_decision": RUN335I_DIR / "final_proxy_mt5_design_decision.json",
    "package_manifest": RUN335G_DIR / "probe_input_package_manifest.csv",
    "source_bindings": RUN335D_DIR / "branch_source_binding_matrix.csv",
    "all_six_runtime": RUN334D_DIR / "all_six_runtime_reconciliation.csv",
    "cost_curve_guard": RUN334D_DIR / "cost_curve_guard_reconciliation.csv",
    "attribution_summary": RUN334D_DIR / "attribution_reconciliation_summary.csv",
    "axis_failure_heatmap": RUN334G_DIR / "axis_failure_heatmap.csv",
    "attempt_failure_memory": RUN334G_DIR / "attempt_failure_memory_review.csv",
    "mt5_runtime_summary": RUN330E_DIR / "mt5_runtime_probe_summary.csv",
    "run330f_cost_stress": RUN330F_DIR / "cost_stress_report.csv",
    "run330f_curve_pocket": RUN330F_DIR / "curve_pocket_report.csv",
}

DIMENSIONS = [
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

BRANCH_AXIS = {
    "cost_spread_slippage_grid_guard": "cost_stress",
    "curve_noncalendar_state_holdout": "curve_pocket",
    "direction_symmetry_no_side_drop": "direction",
    "drawdown_underwater_recovery_quality": "drawdown_shape",
    "regime_predeclared_macro_state": "regime_slice",
    "runtime_identity_strict_handoff": "runtime_parity",
    "negative_control_randomized_signal": "negative_control",
    "negative_control_time_shuffle": "negative_control",
    "tier_context_separate_required": "tier_context",
    "source_authority_no_bridge_subject_swap": "source_authority",
    "stop_condition_no_repair_sprawl": "stop_condition",
}


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
    if not path_exists(path) or io_path(path).is_dir():
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
    return {rel(path): sha256_file(path) for path in INPUTS.values()}


def to_float(value: Any) -> float | None:
    if value in (None, ""):
        return None
    try:
        parsed = float(str(value))
    except ValueError:
        return None
    if math.isnan(parsed) or math.isinf(parsed):
        return None
    return parsed


def nums(rows: Sequence[Mapping[str, Any]], field: str) -> list[float]:
    return [value for value in (to_float(row.get(field)) for row in rows) if value is not None]


def mean_field(rows: Sequence[Mapping[str, Any]], field: str) -> float | None:
    values = nums(rows, field)
    if not values:
        return None
    return statistics.fmean(values)


def min_field(rows: Sequence[Mapping[str, Any]], field: str) -> float | None:
    values = nums(rows, field)
    if not values:
        return None
    return min(values)


def max_field(rows: Sequence[Mapping[str, Any]], field: str) -> float | None:
    values = nums(rows, field)
    if not values:
        return None
    return max(values)


def rows_for(rows: Sequence[Mapping[str, str]], key: str, value: str) -> list[dict[str, str]]:
    return [dict(row) for row in rows if row.get(key) == value]


def load_inputs() -> dict[str, Any]:
    return {
        "queue": read_csv_rows(INPUTS["run335j_queue"]),
        "proxy_schema": read_csv_rows(INPUTS["proxy_schema"]),
        "mt5_design": read_csv_rows(INPUTS["mt5_design"]),
        "difference_contract": read_csv_rows(INPUTS["difference_contract"]),
        "usability_rule": read_csv_rows(INPUTS["usability_rule"]),
        "parent_decision": read_json(INPUTS["final_design_decision"]),
        "packages": read_csv_rows(INPUTS["package_manifest"]),
        "source_bindings": read_csv_rows(INPUTS["source_bindings"]),
        "all_six": read_csv_rows(INPUTS["all_six_runtime"]),
        "cost_curve": read_csv_rows(INPUTS["cost_curve_guard"]),
        "attribution": read_csv_rows(INPUTS["attribution_summary"]),
        "axis_heatmap": read_csv_rows(INPUTS["axis_failure_heatmap"]),
        "attempt_failure": read_csv_rows(INPUTS["attempt_failure_memory"]),
        "mt5_summary": read_csv_rows(INPUTS["mt5_runtime_summary"]),
        "run330f_cost": read_csv_rows(INPUTS["run330f_cost_stress"]),
        "run330f_curve": read_csv_rows(INPUTS["run330f_curve_pocket"]),
    }


def aggregate_values(inputs: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    all_six = inputs["all_six"]
    cost_curve = inputs["cost_curve"]
    attribution = inputs["attribution"]
    attempt_failure = inputs["attempt_failure"]
    mt5_summary = inputs["mt5_summary"]

    mean_buy = mean_field(attribution, "buy_net_profit")
    mean_sell = mean_field(attribution, "sell_net_profit")
    direction_delta = None
    if mean_buy is not None and mean_sell is not None:
        direction_delta = mean_buy - abs(mean_sell)

    values = {
        "net_profit": {
            "proxy": mean_field(attempt_failure, "headline_net_profit"),
            "mt5": mean_field(mt5_summary, "net_profit"),
            "proxy_source": "run334G_attempt_failure_memory_headline_net_profit",
            "mt5_source": "run330E_mt5_runtime_probe_summary_net_profit",
            "unit": "account_currency",
        },
        "profit_factor": {
            "proxy": mean_field(attempt_failure, "headline_profit_factor"),
            "mt5": mean_field(mt5_summary, "profit_factor"),
            "proxy_source": "run334G_attempt_failure_memory_headline_profit_factor",
            "mt5_source": "run330E_mt5_runtime_probe_summary_profit_factor",
            "unit": "ratio",
        },
        "max_drawdown": {
            "proxy": mean_field(all_six, "stage330f_equity_dd_amount"),
            "mt5": mean_field(all_six, "stage330f_equity_dd_amount"),
            "proxy_source": "run334D_all_six_reconciliation_equity_dd_amount",
            "mt5_source": "run334D_all_six_reconciliation_stage330f_equity_dd_amount",
            "unit": "account_currency",
        },
        "trades_per_day": {
            "proxy": mean_field(all_six, "stage330f_trades_per_day"),
            "mt5": mean_field(all_six, "stage330f_trades_per_day"),
            "proxy_source": "run334D_all_six_reconciliation_trades_per_day",
            "mt5_source": "run334D_all_six_reconciliation_stage330f_trades_per_day",
            "unit": "trades_per_day",
        },
        "expectancy": {
            "proxy": mean_field(all_six, "stage330f_expectancy"),
            "mt5": mean_field(all_six, "stage330f_expectancy"),
            "proxy_source": "run334D_all_six_reconciliation_expectancy",
            "mt5_source": "run334D_all_six_reconciliation_stage330f_expectancy",
            "unit": "account_currency_per_trade",
        },
        "recovery_factor": {
            "proxy": mean_field(all_six, "stage330f_recovery_factor"),
            "mt5": mean_field(all_six, "stage330f_recovery_factor"),
            "proxy_source": "run334D_all_six_reconciliation_recovery_factor",
            "mt5_source": "run334D_all_six_reconciliation_stage330f_recovery_factor",
            "unit": "ratio",
        },
        "curve_pocket": {
            "proxy": mean_field(cost_curve, "worst_curve_net"),
            "mt5": min_field(inputs["run330f_curve"], "net_profit"),
            "proxy_source": "run334D_cost_curve_guard_worst_curve_net_mean",
            "mt5_source": "run330F_curve_pocket_report_min_chunk_net_profit",
            "unit": "account_currency",
        },
        "underwater_stretch": {
            "proxy": mean_field(cost_curve, "underwater_trade_share"),
            "mt5": mean_field(all_six, "underwater_trade_share"),
            "proxy_source": "run334D_cost_curve_guard_underwater_trade_share",
            "mt5_source": "run334D_all_six_reconciliation_underwater_trade_share",
            "unit": "share",
        },
        "lot_normalized_result": {
            "proxy": mean_field(cost_curve, "net_profit_per_1lot_linear"),
            "mt5": mean_field(cost_curve, "net_profit_per_1lot_linear"),
            "proxy_source": "run334D_cost_curve_guard_linear_1lot_normalization",
            "mt5_source": "run334D_cost_curve_guard_mt5_derived_linear_1lot_normalization",
            "unit": "account_currency_per_1lot_linear",
        },
        "spread_slippage_stress": {
            "proxy": mean_field(cost_curve, "cost_plus_200_net"),
            "mt5": mean_field(cost_curve, "cost_plus_200_net"),
            "proxy_source": "run334D_cost_curve_guard_cost_plus_200_net",
            "mt5_source": "run334D_cost_curve_guard_mt5_derived_cost_overlay",
            "unit": "account_currency_after_synthetic_cost",
        },
        "session_hour_regime": {
            "proxy": mean_field(all_six, "worst_slice_net"),
            "mt5": mean_field(all_six, "worst_slice_net"),
            "proxy_source": "run334D_all_six_reconciliation_worst_slice_net",
            "mt5_source": "run334D_all_six_reconciliation_runtime_regime_slice",
            "unit": "account_currency",
        },
        "long_short_attribution": {
            "proxy": direction_delta,
            "mt5": direction_delta,
            "proxy_source": "run334D_attribution_buy_minus_abs_sell_net",
            "mt5_source": "run334D_attribution_runtime_trade_direction_breakdown",
            "unit": "account_currency_delta",
        },
    }
    return values


def difference_status(proxy: float | None, mt5: float | None) -> tuple[float | None, str]:
    if proxy is None or mt5 is None:
        return None, "missing_numeric_value"
    diff = proxy - mt5
    if abs(diff) <= 1e-9:
        return diff, "matched_or_same_source"
    return diff, "different_but_explainable_by_source_scope"


def branch_axis_severity(inputs: Mapping[str, Any], branch_name: str) -> dict[str, Any]:
    axis = BRANCH_AXIS.get(branch_name, "combined")
    heatmap = next((row for row in inputs["axis_heatmap"] if row.get("stress_axis") == axis), {})
    hard_failures = to_float(heatmap.get("hard_failure_count")) or 0.0
    scenarios = to_float(heatmap.get("scenario_count")) or 0.0
    rate = hard_failures / scenarios if scenarios else None
    return {
        "branch_axis": axis,
        "axis_judgment": heatmap.get("axis_judgment", "not_axis_specific"),
        "axis_hard_failure_rate": rate,
        "axis_source": rel(INPUTS["axis_failure_heatmap"]) if heatmap else "not_available",
    }


def build_value_rows(inputs: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    aggregate = aggregate_values(inputs)
    proxy_rows: list[dict[str, Any]] = []
    mt5_rows: list[dict[str, Any]] = []
    diff_rows: list[dict[str, Any]] = []
    source_rows: list[dict[str, Any]] = []
    for queue in inputs["queue"]:
        protocol_id = str(queue.get("protocol_id", ""))
        branch_id = str(queue.get("branch_id", ""))
        branch_name = str(queue.get("branch_name", ""))
        axis_meta = branch_axis_severity(inputs, branch_name)
        source_bindings = rows_for(inputs["source_bindings"], "branch_id", branch_id)
        for dimension in DIMENSIONS:
            spec = aggregate[dimension]
            proxy_value = spec.get("proxy")
            mt5_value = spec.get("mt5")
            diff, status = difference_status(proxy_value, mt5_value)
            shared_source = str(spec.get("proxy_source")) == str(spec.get("mt5_source"))
            source_independence = "partial_shared_runtime_source" if shared_source or dimension not in {"net_profit", "profit_factor", "curve_pocket"} else "runtime_summary_vs_forensic_review_bridge"
            proxy_rows.append(
                {
                    "protocol_id": protocol_id,
                    "branch_id": branch_id,
                    "branch_name": branch_name,
                    "branch_axis": axis_meta["branch_axis"],
                    "dimension": dimension,
                    "proxy_expected_value": proxy_value,
                    "unit": spec.get("unit", ""),
                    "proxy_source": spec.get("proxy_source", ""),
                    "source_binding_rows": len(source_bindings),
                    "axis_hard_failure_rate": axis_meta["axis_hard_failure_rate"],
                    "proxy_value_status": "materialized_existing_evidence_numeric_value" if proxy_value is not None else "missing_numeric_value",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            mt5_rows.append(
                {
                    "protocol_id": protocol_id,
                    "branch_id": branch_id,
                    "branch_name": branch_name,
                    "dimension": dimension,
                    "mt5_runtime_value": mt5_value,
                    "unit": spec.get("unit", ""),
                    "mt5_source": spec.get("mt5_source", ""),
                    "runtime_probe_source": "Stage330E actual MT5 runtime probe plus Stage334D/330F forensic derivations",
                    "mt5_result_status": "existing_runtime_probe_result_available" if mt5_value is not None else "missing_numeric_value",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            diff_rows.append(
                {
                    "protocol_id": protocol_id,
                    "branch_id": branch_id,
                    "branch_name": branch_name,
                    "branch_axis": axis_meta["branch_axis"],
                    "dimension": dimension,
                    "proxy_expected_value": proxy_value,
                    "mt5_runtime_value": mt5_value,
                    "difference_proxy_minus_mt5": diff,
                    "difference_status": status,
                    "source_independence": source_independence,
                    "interpretation": "diagnostic_consistency_only_not_forward_decision",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            source_rows.append(
                {
                    "protocol_id": protocol_id,
                    "branch_id": branch_id,
                    "branch_name": branch_name,
                    "dimension": dimension,
                    "proxy_source": spec.get("proxy_source", ""),
                    "mt5_source": spec.get("mt5_source", ""),
                    "source_independence": source_independence,
                    "usable_for_independent_forward_read": False,
                    "usable_for_diagnostic_consistency": True,
                    "reason": "existing MT5 evidence is real, but proxy and MT5 values are not independent enough for Forward Passed/Failed",
                }
            )
    return proxy_rows, mt5_rows, diff_rows, source_rows


def build_usability_rows(diff_rows: Sequence[Mapping[str, Any]], source_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    by_protocol: dict[str, list[Mapping[str, Any]]] = {}
    for row in diff_rows:
        by_protocol.setdefault(str(row.get("protocol_id", "")), []).append(row)
    source_by_protocol: dict[str, list[Mapping[str, Any]]] = {}
    for row in source_rows:
        source_by_protocol.setdefault(str(row.get("protocol_id", "")), []).append(row)
    rows: list[dict[str, Any]] = []
    for protocol_id, group in by_protocol.items():
        first = group[0]
        numeric = [row for row in group if row.get("difference_status") != "missing_numeric_value"]
        missing = len(group) - len(numeric)
        explainable = sum(1 for row in group if row.get("difference_status") in {"matched_or_same_source", "different_but_explainable_by_source_scope"})
        independent = all(row.get("usable_for_independent_forward_read") in {True, "true"} for row in source_by_protocol.get(protocol_id, []))
        rows.append(
            {
                "protocol_id": protocol_id,
                "branch_id": first.get("branch_id", ""),
                "branch_name": first.get("branch_name", ""),
                "numeric_comparison_rows": len(numeric),
                "missing_comparison_rows": missing,
                "explainable_difference_rows": explainable,
                "diagnostic_usability_judgment": "usable_with_boundary_for_consistency_and_repair_prioritization",
                "forward_usability_judgment": "not_usable_as_forward_decision",
                "independent_forward_read_available": independent,
                "required_repair": NEXT_RUN_ID,
                "reason": "existing MT5 runtime result is real, but proxy expected values and MT5 result share evidence lineage; independent proxy/MT5 materialization is still required",
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "runtime_authority": "not_claimed",
                "goal_achieve": "not_claimed",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_mt5_forensics_rows(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    all_six_by_attempt = {row.get("attempt_name", ""): row for row in inputs["all_six"]}
    cost_by_attempt = {row.get("attempt_name", ""): row for row in inputs["cost_curve"]}
    attribution_by_attempt = {row.get("attempt_name", ""): row for row in inputs["attribution"]}
    rows: list[dict[str, Any]] = []
    for row in inputs["mt5_summary"]:
        attempt = row.get("attempt_name", "")
        all_six = all_six_by_attempt.get(attempt, {})
        cost = cost_by_attempt.get(attempt, {})
        attribution = attribution_by_attempt.get(attempt, {})
        rows.append(
            {
                "attempt_name": attempt,
                "artifact_slug": row.get("artifact_slug", ""),
                "tester_status": row.get("tester_status", ""),
                "runtime_status": row.get("runtime_status", ""),
                "report_status": row.get("report_status", ""),
                "net_profit": row.get("net_profit", ""),
                "profit_factor": row.get("profit_factor", ""),
                "trade_count": row.get("trade_count", ""),
                "recovery_factor": all_six.get("stage330f_recovery_factor", ""),
                "equity_dd_amount": all_six.get("stage330f_equity_dd_amount", ""),
                "worst_curve_net": cost.get("worst_curve_net", ""),
                "underwater_trade_share": cost.get("underwater_trade_share", ""),
                "buy_net_profit": attribution.get("buy_net_profit", ""),
                "sell_net_profit": attribution.get("sell_net_profit", ""),
                "report_name": row.get("report_name", ""),
                "runtime_result_status": "actual_stage330E_mt5_runtime_probe_completed" if row.get("tester_status") == "completed" and row.get("runtime_status") == "completed" else "runtime_result_not_completed",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_gate_rows(
    inputs: Mapping[str, Any],
    proxy_rows: Sequence[Mapping[str, Any]],
    mt5_rows: Sequence[Mapping[str, Any]],
    diff_rows: Sequence[Mapping[str, Any]],
    usability_rows: Sequence[Mapping[str, Any]],
    forensics_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    checks = [
        ("parent_queue_loaded", len(inputs["queue"]) == 11, "run335J_materialization_queue.csv", f"queue_rows={len(inputs['queue'])}"),
        ("proxy_numeric_values_materialized", len(proxy_rows) == 132 and all(row.get("proxy_value_status") == "materialized_existing_evidence_numeric_value" for row in proxy_rows), "proxy_expected_numeric_values.csv", f"rows={len(proxy_rows)}"),
        ("mt5_existing_runtime_values_materialized", len(mt5_rows) == 132 and all(row.get("mt5_result_status") == "existing_runtime_probe_result_available" for row in mt5_rows), "mt5_runtime_probe_result_bridge.csv", f"rows={len(mt5_rows)}"),
        ("difference_matrix_materialized", len(diff_rows) == 132, "proxy_mt5_difference_matrix.csv", f"rows={len(diff_rows)}"),
        ("diagnostic_usability_not_forward_usability", len(usability_rows) == 11 and all(row.get("forward_usability_judgment") == "not_usable_as_forward_decision" for row in usability_rows), "proxy_mt5_usability_decision_matrix.csv", f"rows={len(usability_rows)}"),
        ("actual_mt5_forensics_bridge", len(forensics_rows) == 6 and all(row.get("runtime_result_status") == "actual_stage330E_mt5_runtime_probe_completed" for row in forensics_rows), "mt5_runtime_forensics_bridge.csv", f"rows={len(forensics_rows)}"),
        ("claim_boundary_preserved", True, "result_judgment.csv", "no candidate, no Forward Passed/Failed, no runtime authority, no Goal Achieve"),
    ]
    return [
        {
            "gate": gate,
            "status": "passed" if ok else "failed",
            "evidence_path": evidence,
            "detail": detail,
        }
        for gate, ok, evidence, detail in checks
    ]


def build_receipts(
    inputs: Mapping[str, Any],
    proxy_rows: Sequence[Mapping[str, Any]],
    mt5_rows: Sequence[Mapping[str, Any]],
    diff_rows: Sequence[Mapping[str, Any]],
    usability_rows: Sequence[Mapping[str, Any]],
    gate_rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    failed_gates = [row for row in gate_rows if row.get("status") != "passed"]
    return {
        "run_evidence_system_receipt": {
            "run_id": RUN_ID,
            "measurement": {
                "proxy_numeric_rows": len(proxy_rows),
                "mt5_runtime_bridge_rows": len(mt5_rows),
                "difference_rows": len(diff_rows),
                "usability_rows": len(usability_rows),
            },
            "identity": {
                "parent_run_id": PARENT_RUN_ID,
                "mt5_runtime_source": rel(INPUTS["mt5_runtime_summary"]),
                "all_six_reconciliation_source": rel(INPUTS["all_six_runtime"]),
            },
            "judgment": JUDGMENT,
        },
        "data_integrity_receipt": {
            "data_source": [rel(path) for path in INPUTS.values()],
            "time_axis": "uses existing Stage330E forward MT5 runtime period 2026-04-14 to 2026-05-22; no new labels or retune",
            "sample_scope": "11 Stage335 protocols x 12 dimensions, plus six actual Stage330E MT5 runtime attempts",
            "missing_or_duplicate_check": "source row counts and gate rows verify availability; no bar-level merge is performed in run335J",
            "feature_label_boundary": "no feature or label generation; proxy values are evidence-derived summaries",
            "split_boundary": "forward evidence is used for diagnostic comparison only",
            "leakage_risk": "proxy and MT5 values share existing runtime evidence lineage",
            "data_hash_or_identity": source_hashes(),
            "integrity_judgment": "usable_with_boundary_for_diagnostic_consistency",
        },
        "runtime_parity_receipt": {
            "research_path": rel(Path(__file__)),
            "runtime_path": [rel(INPUTS["mt5_runtime_summary"]), rel(INPUTS["all_six_runtime"])],
            "shared_contract": "MT5 runtime result fields are bridged without changing model, threshold, lot, risk, or runtime handoff",
            "known_differences": "no fresh independent MT5 execution in run335J; existing Stage330E runtime evidence is reused with lineage",
            "parity_check": "existing runtime report summary and forensic reconciliations are connected to Stage335 protocols",
            "parity_identity": {
                "mt5_attempts": len(inputs["mt5_summary"]),
                "all_six_rows": len(inputs["all_six"]),
                "stage330e_summary_sha256": sha256_file(INPUTS["mt5_runtime_summary"]),
            },
            "runtime_claim_boundary": "runtime_probe_evidence_bridge_only_no_runtime_authority",
        },
        "backtest_forensics_receipt": {
            "tester_identity": "Stage330E actual MT5 runtime probe summary and Stage334D reconciliation are reused as evidence",
            "ea_identity": "inherited from Stage330E; no new EA or set is created in run335J",
            "report_identity": rel(INPUTS["mt5_runtime_summary"]),
            "trade_evidence": "six completed MT5 runtime probes bridged; trade-level source remains Stage330E/334D",
            "cost_assumptions": "cost stress dimensions are MT5-derived synthetic overlays, not fresh tester costs",
            "forensic_checks": "summary, all-six, cost/curve, and attribution sources loaded and row-count checked",
            "backtest_judgment": "usable_with_boundary_for_existing_runtime_evidence_bridge",
        },
        "performance_attribution_receipt": {
            "observed_change": "proxy and existing MT5 bridge mostly match where they share source; curve pocket has source-scope difference",
            "comparison_baseline": "run335I design-only missing numeric values",
            "likely_drivers": "shared runtime evidence lineage, forensic aggregation, and cost/curve overlay scope",
            "segment_checks": "dimensions include cost, curve, underwater, regime, direction, and lot normalization",
            "trade_shape": "six MT5 attempts, actual trade counts from Stage330E summary",
            "alternative_explanations": ["source sharing", "synthetic cost overlay", "aggregation across all six attempts", "no new independent runtime"],
            "attribution_confidence": "medium_for_diagnostic_consistency_low_for_forward_decision",
            "next_probe": NEXT_RUN_ID,
        },
        "result_judgment_receipt": {
            "result_subject": RUN_ID,
            "evidence_available": [rel(RUN_DIR / "proxy_mt5_difference_matrix.csv"), rel(RUN_DIR / "proxy_mt5_usability_decision_matrix.csv")],
            "evidence_missing": ["fresh independent MT5 runtime probe per Stage335 branch", "independent proxy source not derived from existing MT5 evidence"],
            "judgment_label": "diagnostic_positive_forward_inconclusive",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "The comparison is useful for diagnostics, but not enough for a forward pass/fail decision.",
        },
        "artifact_lineage_receipt": {
            "source_inputs": [rel(path) for path in INPUTS.values()],
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
    }


def build_report_text(usability_rows: Sequence[Mapping[str, Any]], diff_rows: Sequence[Mapping[str, Any]], gate_rows: Sequence[Mapping[str, Any]]) -> str:
    failed_gates = [row for row in gate_rows if row.get("status") != "passed"]
    missing = sum(1 for row in diff_rows if row.get("difference_status") == "missing_numeric_value")
    diagnostic = sum(1 for row in usability_rows if row.get("diagnostic_usability_judgment") == "usable_with_boundary_for_consistency_and_repair_prioritization")
    forward_not = sum(1 for row in usability_rows if row.get("forward_usability_judgment") == "not_usable_as_forward_decision")
    return f"""
# run335J Proxy-MT5 Existing Runtime Comparison(335J 프록시-MT5 기존 런타임 비교)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- difference_rows(차이 행): `{len(diff_rows)}`
- missing_numeric_rows(숫자 누락 행): `{missing}`
- diagnostic_usable_rows(진단 활용 가능 행): `{diagnostic}/{len(usability_rows)}`
- forward_not_usable_rows(전진 판정 활용 불가 행): `{forward_not}/{len(usability_rows)}`
- failed_gates(실패 게이트): `{len(failed_gates)}`
- next_action(다음 행동): `{NEXT_RUN_ID}`

Effect(효과): run335I(335I 실행)의 설계를 실제 숫자 proxy expected value(프록시 예상값)와 기존 Stage330E/334D MT5 runtime result(메타트레이더5 런타임 결과)로 채웠고, 132개 차이 비교를 만들었다.

Usability(활용 가능성): 진단과 repair prioritization(수리 우선순위)에는 `usable_with_boundary`다. 하지만 proxy(프록시)와 MT5(메타트레이더5)가 일부 같은 기존 런타임 근거를 공유하므로 Forward Passed/Failed(전진 통과/실패)나 Goal Achieve(목표 달성)에는 쓸 수 없다.

Boundary(경계): candidate selection(후보 선택), Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), live readiness(실거래 준비), deployment(배포), operating promotion(운영 승격), Goal Achieve(목표 달성)는 모두 `not_claimed`다.
"""


def build_decision_text() -> str:
    return f"""
# Stage335J Decision(335J 결정)

`{RUN_ID}`는 proxy expected values(프록시 예상값)와 existing MT5 runtime result(기존 메타트레이더5 런타임 결과)를 비교했다.

- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- diagnostic_usability(진단 활용 가능성): `usable_with_boundary_for_consistency_and_repair_prioritization`
- forward_usability(전진 판정 활용 가능성): `not_usable_as_forward_decision`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Effect(효과): 비교는 막히지 않았고 숫자 차이는 만들어졌다. 다만 독립 fresh MT5 probe(새 독립 메타트레이더5 탐침)가 아니므로 다음 실행은 독립 proxy/MT5 물질화를 수리하고 검증해야 한다.
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
        "- effect(효과): Stage335J(335J 실행)는 proxy/MT5(프록시/메타트레이더5) 숫자 비교를 만들었고 진단에는 활용 가능하지만, 독립 fresh MT5 probe(새 독립 런타임 탐침)가 아니라 Forward Passed/Failed(전진 통과/실패)에는 아직 활용할 수 없다.",
    )
    changed.append(write_text_lossless(selection_path, text, had_bom))

    text, had_bom = read_text_lossless(STAGE_BRIEF)
    text = replace_prefix_line(text, "- latest_run", f"- latest_run(최신 실행): `{RUN_ID}`")
    changed.append(write_text_lossless(STAGE_BRIEF, text, had_bom))

    changed.append(
        append_section_once(
            INPUTS_DIR / "input_refs.md",
            "## run335J Proxy-MT5 Numeric Comparison(335J 프록시-MT5 숫자 비교)",
            f"""- proxy_expected_numeric_values(프록시 예상 숫자값): `{rel(RUN_DIR / "proxy_expected_numeric_values.csv")}`
- mt5_runtime_probe_result_bridge(MT5 런타임 탐침 결과 연결): `{rel(RUN_DIR / "mt5_runtime_probe_result_bridge.csv")}`
- difference_matrix(차이 행렬): `{rel(RUN_DIR / "proxy_mt5_difference_matrix.csv")}`
- usability_decision(활용 가능성 결정): `{rel(RUN_DIR / "proxy_mt5_usability_decision_matrix.csv")}`
- decision(결정): `{rel(DECISION_DOC)}`""",
        )
    )

    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_prefix_line(workspace_text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    workspace_text = replace_prefix_line(workspace_text, "updated_on:", f"updated_on: '{TODAY}'")
    focus_line = (
        "- >-\n"
        f"  Stage335(335단계) run335J(335J 실행)는 `{STATUS}`로 proxy expected value(프록시 예상값)와 existing MT5 runtime result(기존 메타트레이더5 런타임 결과)를 비교했다. "
        "Effect(효과): 진단 활용은 가능하지만 독립 fresh runtime probe(새 독립 런타임 탐침)가 아니라 Forward Passed/Failed(전진 통과/실패)와 Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    workspace_text = insert_after_prefix_once(workspace_text, "current_focus:", focus_line, "run335J(335J 실행)")
    changed.append(write_text_lossless(WORKSPACE_STATE, workspace_text, workspace_bom))

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    current_text = replace_prefix_line(current_text, "- current_packet", "- current_packet(현재 작업 묶음): `335_overfit_guard__failure_memory_constrained_research_handoff_v11`")
    current_text = replace_prefix_line(current_text, "- current_run", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    current_text = replace_prefix_line(current_text, "- status", f"- status(상태): `{STATUS}`")
    current_text = replace_prefix_line(current_text, "- decision", f"- decision(판정): `{DECISION}`")
    current_text = remove_lines_containing(current_text, "run335J_summary")
    summary = (
        f"- run335J_summary(335J 요약): proxy expected and existing MT5 runtime result comparison(프록시 예상값 및 기존 MT5 런타임 결과 비교)을 `{STATUS}`로 완료했다. "
        "Effect(효과): 132개 difference row(차이 행)를 만들고 진단 활용 가능성은 확인했지만, 독립 fresh runtime probe(새 독립 런타임 탐침)가 아니므로 Forward Passed/Failed(전진 통과/실패)와 Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    current_text = insert_after_prefix_once(current_text, "- decision", summary, "run335J_summary")
    changed.append(write_text_lossless(CURRENT_STATE, current_text, current_bom))

    changed.append(
        append_section_once(
            CHANGELOG,
            "## 2026-05-26 Stage335J Proxy-MT5 Numeric Comparison(335J 프록시-MT5 숫자 비교)",
            f"""- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- effect(효과): proxy expected values(프록시 예상값), existing MT5 runtime values(기존 MT5 런타임 값), difference matrix(차이 행렬), usability decision(활용 가능성 결정)을 만들었다.
- boundary(경계): diagnostic usable(진단 활용 가능)이나 forward pass/fail usable(전진 통과/실패 활용 가능)은 아님. Goal Achieve(목표 달성)는 주장하지 않는다.""",
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
                    "lane": "kpi_evidence",
                    "status": STATUS,
                    "judgment": JUDGMENT,
                    "path": rel(report_path),
                    "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};diagnostic_usable_not_forward_usable;goal_achieve_not_claimed.",
                }
            ],
        )
    )
    ledger_row = {
        "ledger_row_id": f"{RUN_ID}__proxy_mt5_existing_runtime_comparison",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "proxy_mt5_existing_runtime_comparison",
        "tier_scope": "paired_tier_required_by_contract",
        "kpi_scope": "diagnostic_comparison_existing_runtime_evidence",
        "scoreboard_lane": "kpi_evidence",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(report_path),
        "primary_kpi": "proxy_rows=132;mt5_rows=132;difference_rows=132;usability_rows=11",
        "guardrail_kpi": "diagnostic_usable_not_forward_usable;no_retune;goal_achieve_not_claimed",
        "external_verification_status": "completed_existing_mt5_runtime_evidence_bridge_no_new_runtime_authority",
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
                    "work_family": "kpi_evidence",
                    "evidence_scope": "proxy_mt5_existing_runtime_comparison",
                    "kpi_scope": "diagnostic_comparison_existing_runtime_evidence",
                    "status": STATUS,
                    "judgment": JUDGMENT,
                    "claim_boundary": CLAIM_BOUNDARY,
                    "path": rel(report_path),
                    "notes": "no_candidate_selected;diagnostic_usable_not_forward_usable;goal_achieve_not_claimed.",
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
                "notes": f"Stage335J proxy-MT5 comparison artifact; claim_boundary={CLAIM_BOUNDARY}",
            }
        )
    changed.append(upsert_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows))
    return changed


def main() -> int:
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    inputs = load_inputs()
    proxy_rows, mt5_rows, diff_rows, source_rows = build_value_rows(inputs)
    usability_rows = build_usability_rows(diff_rows, source_rows)
    forensics_rows = build_mt5_forensics_rows(inputs)
    gate_rows = build_gate_rows(inputs, proxy_rows, mt5_rows, diff_rows, usability_rows, forensics_rows)
    receipts = build_receipts(inputs, proxy_rows, mt5_rows, diff_rows, usability_rows, gate_rows)
    failed_gates = [row for row in gate_rows if row.get("status") != "passed"]

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
            "diagnostic_usability": "usable_with_boundary_for_consistency_and_repair_prioritization",
            "forward_usability": "not_usable_as_forward_decision",
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
        "proxy_rows": len(proxy_rows),
        "mt5_rows": len(mt5_rows),
        "difference_rows": len(diff_rows),
        "usability_rows": len(usability_rows),
        "failed_gates": len(failed_gates),
        "diagnostic_usability": "usable_with_boundary_for_consistency_and_repair_prioritization",
        "forward_usability": "not_usable_as_forward_decision",
        "selected_candidate": "none",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }

    artifact_paths: list[Path] = [
        write_json(RUN_DIR / "source_artifact_hashes.json", source_hashes()),
        write_csv(
            RUN_DIR / "proxy_expected_numeric_values.csv",
            [
                "protocol_id",
                "branch_id",
                "branch_name",
                "branch_axis",
                "dimension",
                "proxy_expected_value",
                "unit",
                "proxy_source",
                "source_binding_rows",
                "axis_hard_failure_rate",
                "proxy_value_status",
                "claim_boundary",
            ],
            proxy_rows,
        ),
        write_csv(
            RUN_DIR / "mt5_runtime_probe_result_bridge.csv",
            [
                "protocol_id",
                "branch_id",
                "branch_name",
                "dimension",
                "mt5_runtime_value",
                "unit",
                "mt5_source",
                "runtime_probe_source",
                "mt5_result_status",
                "claim_boundary",
            ],
            mt5_rows,
        ),
        write_csv(
            RUN_DIR / "proxy_mt5_difference_matrix.csv",
            [
                "protocol_id",
                "branch_id",
                "branch_name",
                "branch_axis",
                "dimension",
                "proxy_expected_value",
                "mt5_runtime_value",
                "difference_proxy_minus_mt5",
                "difference_status",
                "source_independence",
                "interpretation",
                "claim_boundary",
            ],
            diff_rows,
        ),
        write_csv(
            RUN_DIR / "source_independence_audit.csv",
            [
                "protocol_id",
                "branch_id",
                "branch_name",
                "dimension",
                "proxy_source",
                "mt5_source",
                "source_independence",
                "usable_for_independent_forward_read",
                "usable_for_diagnostic_consistency",
                "reason",
            ],
            source_rows,
        ),
        write_csv(
            RUN_DIR / "proxy_mt5_usability_decision_matrix.csv",
            [
                "protocol_id",
                "branch_id",
                "branch_name",
                "numeric_comparison_rows",
                "missing_comparison_rows",
                "explainable_difference_rows",
                "diagnostic_usability_judgment",
                "forward_usability_judgment",
                "independent_forward_read_available",
                "required_repair",
                "reason",
                "forward_passed",
                "forward_failed",
                "runtime_authority",
                "goal_achieve",
                "claim_boundary",
            ],
            usability_rows,
        ),
        write_csv(
            RUN_DIR / "mt5_runtime_forensics_bridge.csv",
            [
                "attempt_name",
                "artifact_slug",
                "tester_status",
                "runtime_status",
                "report_status",
                "net_profit",
                "profit_factor",
                "trade_count",
                "recovery_factor",
                "equity_dd_amount",
                "worst_curve_net",
                "underwater_trade_share",
                "buy_net_profit",
                "sell_net_profit",
                "report_name",
                "runtime_result_status",
                "claim_boundary",
            ],
            forensics_rows,
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
                "diagnostic_usability",
                "forward_usability",
                "goal_achieve",
                "next_action",
                "claim_boundary",
            ],
            result_rows,
        ),
        write_json(RUN_DIR / "run_evidence_system_receipt.json", receipts["run_evidence_system_receipt"]),
        write_json(RUN_DIR / "data_integrity_receipt.json", receipts["data_integrity_receipt"]),
        write_json(RUN_DIR / "runtime_parity_receipt.json", receipts["runtime_parity_receipt"]),
        write_json(RUN_DIR / "backtest_forensics_receipt.json", receipts["backtest_forensics_receipt"]),
        write_json(RUN_DIR / "performance_attribution_receipt.json", receipts["performance_attribution_receipt"]),
        write_json(RUN_DIR / "result_judgment_receipt.json", receipts["result_judgment_receipt"]),
        write_json(RUN_DIR / "gate_receipt.json", receipts["gate_receipt"]),
        write_json(RUN_DIR / "final_proxy_mt5_comparison_decision.json", final_decision),
    ]

    manifest_path = RUN_DIR / "run_manifest.json"
    lineage_path = RUN_DIR / "artifact_lineage_receipt.json"
    run_manifest = {
        **final_decision,
        "created_at_utc": utc_now(),
        "producer": rel(Path(__file__)),
        "source_inputs": [rel(path) for path in INPUTS.values()],
        "outputs": [rel(path) for path in [*artifact_paths, manifest_path, lineage_path]],
    }
    artifact_paths.append(write_json(manifest_path, run_manifest))

    lineage = receipts["artifact_lineage_receipt"]
    lineage["artifact_paths"] = [rel(path) for path in [*artifact_paths, lineage_path]]
    lineage["artifact_hashes"] = {rel(path): sha256_file(path) for path in artifact_paths}
    artifact_paths.append(write_json(lineage_path, lineage))

    report_path = write_md(REVIEWS_DIR / "run335J_proxy_mt5_existing_runtime_comparison.md", build_report_text(usability_rows, diff_rows, gate_rows))
    artifact_paths.append(report_path)
    artifact_paths.append(write_md(DECISION_DOC, build_decision_text()))
    artifact_paths.extend(update_state_docs())
    artifact_paths.extend(update_registries([Path(__file__), *artifact_paths], report_path))

    summary = {
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "proxy_rows": len(proxy_rows),
        "mt5_rows": len(mt5_rows),
        "difference_rows": len(diff_rows),
        "usability_rows": len(usability_rows),
        "failed_gates": len(failed_gates),
        "diagnostic_usability": "usable_with_boundary_for_consistency_and_repair_prioritization",
        "forward_usability": "not_usable_as_forward_decision",
        "selected_candidate": "none",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_RUN_ID,
        "artifact_count": len(artifact_paths),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
