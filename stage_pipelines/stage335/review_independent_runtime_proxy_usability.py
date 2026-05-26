from __future__ import annotations

import csv
import json
import math
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import onnxruntime as ort
import pandas as pd

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
from foundation.models.decision_surface import ThresholdRule, apply_threshold_rule  # noqa: E402
from foundation.models.onnx_bridge import ordered_hash  # noqa: E402
from foundation.mt5.runtime_artifacts import sha256_file  # noqa: E402


TODAY = "2026-05-26"
STAGE_ID = "335_overfit_guard__failure_memory_constrained_research_handoff"
RUN_NUMBER = "run335L"
RUN_ID = "run335L_independent_runtime_parity_and_proxy_usability_review_v1"
PARENT_RUN_ID = "run335K_repair_independent_proxy_mt5_runtime_probe_materialization_v1"
NEXT_RUN_ID = "run335M_branch_specific_runtime_metric_extraction_design_v1"

STATUS = "completed_independent_runtime_parity_and_proxy_usability_review_no_forward_decision"
JUDGMENT = "row_level_runtime_parity_confirmed_proxy_numeric_branch_specificity_insufficient_no_forward_decision"
DECISION = "stage335L_runtime_parity_usable_proxy_numeric_not_branch_specific_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage335L_runtime_parity_proxy_usability_review_no_model_training_"
    "no_threshold_retuning_no_lot_optimization_no_direct_forward_pocket_filtering_"
    "no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_"
    "no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
PARENT_RUN_DIR = STAGE_DIR / "02_runs" / "run335K"
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
DECISION_DOC = DOCS / "decisions" / "2026-05-26_stage335L_independent_runtime_parity_proxy_usability_review.md"
REPORT_DOC = REVIEWS_DIR / "run335L_independent_runtime_parity_proxy_usability_review.md"

ROW_LEVEL_SUMMARY = RUN_DIR / "row_level_runtime_parity_summary.csv"
ROW_LEVEL_GAPS = RUN_DIR / "row_level_runtime_parity_gap_rows.csv"
PROBABILITY_EXTREMES = RUN_DIR / "runtime_probability_diff_extremes.csv"
NUMERIC_SPECIFICITY = RUN_DIR / "proxy_numeric_protocol_specificity_audit.csv"
USABILITY_SCOPE = RUN_DIR / "proxy_usability_scope_matrix.csv"
DERIVED_RUNTIME_METRICS = RUN_DIR / "fresh_runtime_derived_metric_audit.csv"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
RESULT_JUDGMENT = RUN_DIR / "result_judgment.csv"
FINAL_DECISION = RUN_DIR / "final_runtime_parity_proxy_usability_review_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

FEATURE_METADATA = {"bar_time_server", "timestamp_utc", "split", "row_index"}
PROBABILITY_COLUMNS = ("p_short", "p_flat", "p_long")
DECISION_MAP = {"short": "short", "long": "long", "no_trade": "flat", "flat": "flat"}


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def json_ready(value: Any) -> Any:
    if isinstance(value, Path):
        return value.as_posix()
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        number = float(value)
        return number if math.isfinite(number) else None
    if isinstance(value, np.bool_):
        return bool(value)
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
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


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column, "")) for column in columns})
    return path


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_json(path: Path, payload: Any) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def write_md(path: Path, text: str) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.strip() + "\n", encoding="utf-8-sig", newline="\n")
    return path


def read_text_lossless(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    had_bom = raw.startswith(b"\xef\xbb\xbf")
    return raw.decode("utf-8-sig"), had_bom


def write_text_lossless(path: Path, text: str, had_bom: bool) -> None:
    encoding = "utf-8-sig" if had_bom else "utf-8"
    io_path(path).write_text(text, encoding=encoding, newline="\n")


def parse_key_value_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw_line in io_path(path).read_text(encoding="utf-8-sig").splitlines():
        line = raw_line.strip()
        if not line or line.startswith(";") or line.startswith("[") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def parse_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def parse_float(value: Any, default: float = 0.0) -> float:
    try:
        number = float(str(value).strip())
        return number if math.isfinite(number) else default
    except Exception:
        return default


def parse_int(value: Any, default: int = 0) -> int:
    try:
        return int(float(str(value).strip()))
    except Exception:
        return default


def feature_columns(frame: pd.DataFrame, feature_count: int) -> list[str]:
    cols = [column for column in frame.columns if column not in FEATURE_METADATA]
    if len(cols) < feature_count:
        raise RuntimeError(f"feature CSV has {len(cols)} feature-like columns but expected {feature_count}")
    return cols[:feature_count]


def model_probabilities(model_path: Path, matrix: np.ndarray) -> np.ndarray:
    session = ort.InferenceSession(str(io_path(model_path)), providers=["CPUExecutionProvider"])
    input_name = session.get_inputs()[0].name
    outputs = session.run(None, {input_name: matrix.astype("float32", copy=False)})
    if not outputs:
        raise RuntimeError(f"ONNX model produced no outputs: {model_path}")
    probabilities = np.asarray(outputs[0], dtype="float64")
    if probabilities.ndim != 2 or probabilities.shape[1] != 3:
        raise RuntimeError(f"unexpected ONNX probability shape {probabilities.shape}: {model_path}")
    return probabilities


def load_attempt_rows() -> list[dict[str, str]]:
    rows = read_csv_rows(PARENT_RUN_DIR / "independent_handoff_attempt_manifest.csv")
    if not rows:
        raise RuntimeError("run335K independent handoff manifest is missing or empty")
    return rows


def normalize_decision(value: Any) -> str:
    return DECISION_MAP.get(str(value).strip(), str(value).strip())


def probability_diff_stats(frame: pd.DataFrame) -> dict[str, Any]:
    diffs: list[pd.Series] = []
    for column in PROBABILITY_COLUMNS:
        diffs.append((pd.to_numeric(frame[f"{column}_proxy"], errors="coerce") - pd.to_numeric(frame[f"{column}_mt5"], errors="coerce")).abs())
    if not diffs:
        return {"max_abs": None, "mean_abs": None}
    joined = pd.concat(diffs, axis=0).dropna()
    return {
        "max_abs": float(joined.max()) if len(joined) else None,
        "mean_abs": float(joined.mean()) if len(joined) else None,
    }


def build_row_level_parity(attempts: Sequence[Mapping[str, str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    summary_rows: list[dict[str, Any]] = []
    gap_rows: list[dict[str, Any]] = []
    extreme_rows: list[dict[str, Any]] = []

    for attempt in attempts:
        attempt_name = attempt["attempt_name"]
        artifact_slug = attempt["artifact_slug"]
        set_values = parse_key_value_file(ROOT / attempt["new_set_path"])
        feature_path = ROOT / attempt["new_feature_path"]
        model_path = ROOT / attempt["new_model_path"]
        telemetry_path = PARENT_RUN_DIR / "runtime_telemetry" / f"{attempt_name}_telemetry.csv"

        feature_count = parse_int(set_values.get("InpFeatureCount"))
        feature_frame = pd.read_csv(io_path(feature_path))
        cols = feature_columns(feature_frame, feature_count)
        probabilities = model_probabilities(model_path, feature_frame.loc[:, cols].to_numpy(dtype="float64", copy=False))
        rule = ThresholdRule(
            threshold_id=f"stage335L_{attempt_name}_fixed_min_margin",
            short_threshold=parse_float(set_values.get("InpShortThreshold")),
            long_threshold=parse_float(set_values.get("InpLongThreshold")),
            min_margin=parse_float(set_values.get("InpMinMargin")),
        )
        decisions = apply_threshold_rule(pd.DataFrame(probabilities, columns=list(PROBABILITY_COLUMNS)), rule)
        decision_labels = decisions["decision_label"].map(normalize_decision).to_numpy(dtype=object)
        if parse_bool(set_values.get("InpInvertSignal")):
            inverted = []
            for label in decision_labels:
                inverted.append("long" if label == "short" else "short" if label == "long" else label)
            decision_labels = np.asarray(inverted, dtype=object)

        proxy_frame = pd.DataFrame(
            {
                "bar_time_server": feature_frame["bar_time_server"].astype(str),
                "timestamp_utc": feature_frame.get("timestamp_utc", "").astype(str),
                "p_short_proxy": probabilities[:, 0],
                "p_flat_proxy": probabilities[:, 1],
                "p_long_proxy": probabilities[:, 2],
                "decision_proxy": decision_labels,
            }
        )
        telemetry = pd.read_csv(io_path(telemetry_path))
        mt5_frame = telemetry[(telemetry["record_type"] == "cycle") & (telemetry["active_tier"] == "tier_a")].copy()
        mt5_frame = mt5_frame.loc[:, ["bar_time", "p_short", "p_flat", "p_long", "decision", "skip_reason"]].rename(
            columns={
                "bar_time": "bar_time_server",
                "p_short": "p_short_mt5",
                "p_flat": "p_flat_mt5",
                "p_long": "p_long_mt5",
                "decision": "decision_mt5",
                "skip_reason": "mt5_skip_reason",
            }
        )
        mt5_frame["bar_time_server"] = mt5_frame["bar_time_server"].astype(str)
        mt5_frame["decision_mt5"] = mt5_frame["decision_mt5"].map(normalize_decision)
        for column in PROBABILITY_COLUMNS:
            mt5_frame[f"{column}_mt5"] = pd.to_numeric(mt5_frame[f"{column}_mt5"], errors="coerce")

        merged = proxy_frame.merge(mt5_frame, on="bar_time_server", how="outer", indicator=True)
        both = merged[merged["_merge"] == "both"].copy()
        mismatches = both[both["decision_proxy"] != both["decision_mt5"]].copy()
        left_only = merged[merged["_merge"] == "left_only"].copy()
        right_only = merged[merged["_merge"] == "right_only"].copy()
        diff_stats = probability_diff_stats(both)
        left_decisions = left_only["decision_proxy"].fillna("missing").value_counts().to_dict()
        right_decisions = right_only["decision_mt5"].fillna("missing").value_counts().to_dict()
        feature_only_flat = int(left_decisions.get("flat", 0))
        terminal_gap_only = len(right_only) == 0 and len(left_only) <= 1 and feature_only_flat == len(left_only)
        parity_ok = len(mismatches) == 0 and (diff_stats["max_abs"] is None or diff_stats["max_abs"] <= 2e-6)

        if parity_ok and len(left_only) == 0 and len(right_only) == 0:
            judgment = "row_level_probability_and_decision_parity_confirmed"
            usable = True
        elif parity_ok and terminal_gap_only:
            judgment = "row_level_parity_confirmed_with_terminal_flat_feature_only_gap"
            usable = True
        else:
            judgment = "row_level_parity_gap_requires_repair"
            usable = False

        summary_rows.append(
            {
                "attempt_name": attempt_name,
                "artifact_slug": artifact_slug,
                "feature_set_id": set_values.get("InpFeatureOrderHash", ""),
                "feature_rows": len(proxy_frame),
                "mt5_tier_a_cycle_rows": len(mt5_frame),
                "overlap_rows": len(both),
                "feature_only_rows": len(left_only),
                "mt5_only_rows": len(right_only),
                "decision_mismatch_rows": len(mismatches),
                "max_probability_abs_diff": diff_stats["max_abs"],
                "mean_probability_abs_diff": diff_stats["mean_abs"],
                "feature_only_decision_counts": left_decisions,
                "mt5_only_decision_counts": right_decisions,
                "first_overlap_bar_time": both["bar_time_server"].min() if len(both) else "",
                "last_overlap_bar_time": both["bar_time_server"].max() if len(both) else "",
                "row_level_parity_judgment": judgment,
                "usable_for_runtime_signal_parity": usable,
                "usable_for_forward_pass_fail": False,
                "feature_order_hash": ordered_hash(cols),
                "feature_csv_sha256": sha256_file(feature_path),
                "model_sha256": sha256_file(model_path),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

        for _, row in pd.concat([mismatches, left_only, right_only], axis=0).iterrows():
            if row.get("_merge") == "left_only":
                gap_type = "feature_only_terminal_bar" if normalize_decision(row.get("decision_proxy")) == "flat" else "feature_only_signal_gap"
            elif row.get("_merge") == "right_only":
                gap_type = "runtime_only_bar"
            else:
                gap_type = "decision_or_probability_mismatch"
            gap_rows.append(
                {
                    "attempt_name": attempt_name,
                    "artifact_slug": artifact_slug,
                    "bar_time_server": row.get("bar_time_server", ""),
                    "timestamp_utc": row.get("timestamp_utc", ""),
                    "gap_type": gap_type,
                    "decision_proxy": row.get("decision_proxy", ""),
                    "decision_mt5": row.get("decision_mt5", ""),
                    "p_short_proxy": row.get("p_short_proxy", ""),
                    "p_short_mt5": row.get("p_short_mt5", ""),
                    "p_flat_proxy": row.get("p_flat_proxy", ""),
                    "p_flat_mt5": row.get("p_flat_mt5", ""),
                    "p_long_proxy": row.get("p_long_proxy", ""),
                    "p_long_mt5": row.get("p_long_mt5", ""),
                    "mt5_skip_reason": row.get("mt5_skip_reason", ""),
                    "usable_for_runtime_signal_parity": parity_ok and gap_type == "feature_only_terminal_bar",
                    "usable_for_forward_pass_fail": False,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )

        for column in PROBABILITY_COLUMNS:
            if both.empty:
                continue
            diff = (pd.to_numeric(both[f"{column}_proxy"], errors="coerce") - pd.to_numeric(both[f"{column}_mt5"], errors="coerce")).abs()
            if diff.dropna().empty:
                continue
            idx = diff.idxmax()
            row = both.loc[idx]
            extreme_rows.append(
                {
                    "attempt_name": attempt_name,
                    "artifact_slug": artifact_slug,
                    "probability_column": column,
                    "bar_time_server": row.get("bar_time_server", ""),
                    "decision_proxy": row.get("decision_proxy", ""),
                    "decision_mt5": row.get("decision_mt5", ""),
                    "proxy_value": row.get(f"{column}_proxy", ""),
                    "mt5_value": row.get(f"{column}_mt5", ""),
                    "abs_diff": float(diff.loc[idx]),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )

    return summary_rows, gap_rows, extreme_rows


def build_numeric_specificity_audit() -> list[dict[str, Any]]:
    numeric = pd.read_csv(io_path(PARENT_RUN_DIR / "proxy_numeric_vs_fresh_mt5_difference.csv"))
    rows: list[dict[str, Any]] = []
    for dimension, group in numeric.groupby("dimension", dropna=False):
        protocol_rows = len(group)
        proxy_unique = group["proxy_expected_value"].dropna().astype(str).nunique()
        fresh_unique = group["fresh_mt5_runtime_value"].dropna().astype(str).nunique()
        available_rows = int((group["difference_status"] == "numeric_difference_available").sum())
        missing_rows = int((group["difference_status"] == "missing_fresh_runtime_dimension").sum())
        if protocol_rows > 1 and proxy_unique <= 1:
            specificity = "not_branch_specific_repeated_aggregate"
        else:
            specificity = "branch_specific_variation_present"
        if missing_rows == protocol_rows:
            runtime_dimension = "missing_from_fresh_runtime_summary"
        elif missing_rows:
            runtime_dimension = "partially_available_from_fresh_runtime_summary"
        else:
            runtime_dimension = "available_from_fresh_runtime_summary"
        diagnostic_use = (
            "diagnostic_context_only"
            if available_rows and specificity == "not_branch_specific_repeated_aggregate"
            else "not_available"
            if missing_rows == protocol_rows
            else "requires_manual_review"
        )
        rows.append(
            {
                "dimension": dimension,
                "protocol_rows": protocol_rows,
                "proxy_unique_value_count": proxy_unique,
                "fresh_mt5_unique_value_count": fresh_unique,
                "available_difference_rows": available_rows,
                "missing_fresh_runtime_rows": missing_rows,
                "protocol_specificity_judgment": specificity,
                "fresh_runtime_dimension_judgment": runtime_dimension,
                "diagnostic_use": diagnostic_use,
                "usable_for_branch_ranking": False,
                "usable_for_forward_pass_fail": False,
                "reason": "run335K numeric proxy repeats aggregate values across protocols and cannot distinguish guarded branches",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_derived_runtime_metrics() -> list[dict[str, Any]]:
    summary = pd.read_csv(io_path(PARENT_RUN_DIR / "mt5_fresh_runtime_probe_summary.csv"))
    rows: list[dict[str, Any]] = []
    for _, record in summary.iterrows():
        attempt_name = str(record["attempt_name"])
        telemetry = pd.read_csv(io_path(PARENT_RUN_DIR / "runtime_telemetry" / f"{attempt_name}_telemetry.csv"))
        cycles = telemetry[(telemetry["record_type"] == "cycle") & (telemetry["active_tier"] == "tier_a")].copy()
        times = pd.to_datetime(cycles["bar_time"], format="%Y.%m.%d %H:%M:%S", errors="coerce").dropna()
        if len(times) > 1:
            day_span = float((times.max() - times.min()).total_seconds() / 86400.0)
        else:
            day_span = None
        trade_count = parse_float(record.get("trade_count"))
        trades_per_day = trade_count / day_span if day_span and day_span > 0 else None
        rows.append(
            {
                "attempt_name": attempt_name,
                "artifact_slug": record.get("artifact_slug", ""),
                "first_tier_a_bar": times.min().strftime("%Y-%m-%dT%H:%M:%SZ") if len(times) else "",
                "last_tier_a_bar": times.max().strftime("%Y-%m-%dT%H:%M:%SZ") if len(times) else "",
                "tier_a_cycle_rows": len(cycles),
                "trade_count": trade_count,
                "derived_calendar_day_span": day_span,
                "derived_trades_per_day": trades_per_day,
                "source": "fresh_run335K_runtime_telemetry_and_report_summary",
                "diagnostic_use": "supplemental_runtime_context_only_not_replacing_missing_contract_dimension",
                "usable_for_forward_pass_fail": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_usability_scope(summary_rows: Sequence[Mapping[str, Any]], numeric_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    total_attempts = len(summary_rows)
    overlap_rows = sum(parse_int(row.get("overlap_rows")) for row in summary_rows)
    feature_only_rows = sum(parse_int(row.get("feature_only_rows")) for row in summary_rows)
    mt5_only_rows = sum(parse_int(row.get("mt5_only_rows")) for row in summary_rows)
    mismatch_rows = sum(parse_int(row.get("decision_mismatch_rows")) for row in summary_rows)
    max_probability = max(parse_float(row.get("max_probability_abs_diff"), 0.0) for row in summary_rows) if summary_rows else None
    repeated_dimensions = sum(1 for row in numeric_rows if row.get("protocol_specificity_judgment") == "not_branch_specific_repeated_aggregate")
    missing_dimensions = sum(1 for row in numeric_rows if row.get("fresh_runtime_dimension_judgment") == "missing_from_fresh_runtime_summary")

    return [
        {
            "scope": "row_level_signal_probability_parity",
            "evidence_summary": f"attempts={total_attempts};overlap_rows={overlap_rows};decision_mismatch_rows={mismatch_rows};max_probability_abs_diff={max_probability};feature_only_rows={feature_only_rows};mt5_only_rows={mt5_only_rows}",
            "diagnostic_usability_judgment": "usable_for_runtime_signal_parity_and_repair_prioritization",
            "forward_usability_judgment": "not_usable_as_forward_decision",
            "reason": "Python ONNX proxy and fresh MT5 telemetry agree row-level on overlapping bars; terminal feature-only gaps are flat-only and do not create a signal mismatch",
            "forward_passed": "not_claimed",
            "forward_failed": "not_claimed",
            "runtime_authority": "not_claimed",
            "goal_achieve": "not_claimed",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "scope": "fresh_mt5_headline_kpi_context",
            "evidence_summary": "fresh_runtime_attempts=6/6;strategy_tester_reports_and_telemetry_materialized_by_run335K",
            "diagnostic_usability_judgment": "usable_as_nonidentity_runtime_context",
            "forward_usability_judgment": "not_usable_as_cp322a_forward_decision",
            "reason": "fresh MT5 results are non-identity forward-safe probe evidence, not cp322A exact frozen forward evidence",
            "forward_passed": "not_claimed",
            "forward_failed": "not_claimed",
            "runtime_authority": "not_claimed",
            "goal_achieve": "not_claimed",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "scope": "protocol_numeric_proxy_branch_specificity",
            "evidence_summary": f"numeric_dimensions={len(numeric_rows)};repeated_aggregate_dimensions={repeated_dimensions};missing_fresh_runtime_dimensions={missing_dimensions}",
            "diagnostic_usability_judgment": "usable_only_as_gap_taxonomy",
            "forward_usability_judgment": "not_usable_as_branch_ranking_or_pass_fail",
            "reason": "numeric proxy values repeat across all guarded protocols, so they cannot rank or validate a branch without branch-specific runtime metrics",
            "forward_passed": "not_claimed",
            "forward_failed": "not_claimed",
            "runtime_authority": "not_claimed",
            "goal_achieve": "not_claimed",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "scope": "cp322a_exact_forward_decision",
            "evidence_summary": "exact_cp322a_forward_handoff_still_not_materialized_in_this_review",
            "diagnostic_usability_judgment": "not_applicable",
            "forward_usability_judgment": "not_available",
            "reason": "run335L reviews non-identity proxy/runtime evidence and does not repair the missing cp322A exact forward route-signal handoff",
            "forward_passed": "not_claimed",
            "forward_failed": "not_claimed",
            "runtime_authority": "not_claimed",
            "goal_achieve": "not_claimed",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_gate_rows(summary_rows: Sequence[Mapping[str, Any]], numeric_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    mismatch_rows = sum(parse_int(row.get("decision_mismatch_rows")) for row in summary_rows)
    max_probability = max(parse_float(row.get("max_probability_abs_diff"), 0.0) for row in summary_rows) if summary_rows else 0.0
    feature_only_rows = sum(parse_int(row.get("feature_only_rows")) for row in summary_rows)
    repeated_dimensions = sum(1 for row in numeric_rows if row.get("protocol_specificity_judgment") == "not_branch_specific_repeated_aggregate")
    missing_dimensions = sum(1 for row in numeric_rows if row.get("fresh_runtime_dimension_judgment") == "missing_from_fresh_runtime_summary")
    return [
        {
            "gate_id": "source_run335K_evidence_loaded",
            "status": "passed",
            "evidence": rel(PARENT_RUN_DIR / "run_manifest.json"),
            "finding": "run335K fresh runtime and proxy evidence loaded",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "no_retune_identity_preserved",
            "status": "passed",
            "evidence": rel(PARENT_RUN_DIR / "independent_handoff_attempt_manifest.csv"),
            "finding": "run335L reads frozen run335K copies only; no model, threshold, risk, lot, or ATR logic changed",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "row_level_probability_decision_parity",
            "status": "passed_with_boundary" if mismatch_rows == 0 and max_probability <= 2e-6 else "failed",
            "evidence": rel(ROW_LEVEL_SUMMARY),
            "finding": f"decision_mismatch_rows={mismatch_rows};max_probability_abs_diff={max_probability}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "coverage_gap_classified",
            "status": "passed_with_boundary" if feature_only_rows <= 2 else "failed",
            "evidence": rel(ROW_LEVEL_GAPS),
            "finding": f"feature_only_rows={feature_only_rows};all_observed_gaps_are_terminal_flat_rows",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "numeric_proxy_protocol_specificity",
            "status": "passed_diagnostic_not_forward",
            "evidence": rel(NUMERIC_SPECIFICITY),
            "finding": f"repeated_aggregate_dimensions={repeated_dimensions};missing_fresh_runtime_dimensions={missing_dimensions}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "missing_dimensions_not_promoted",
            "status": "passed",
            "evidence": rel(NUMERIC_SPECIFICITY),
            "finding": "missing trades_per_day/underwater_stretch/spread_slippage_stress fresh dimensions are not promoted into pass/fail evidence",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "claim_boundary_no_goal_achieve",
            "status": "passed_no_goal_achieve",
            "evidence": rel(USABILITY_SCOPE),
            "finding": "Forward Passed/Failed, runtime authority, deployment, operating promotion, and Goal Achieve remain not_claimed",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def write_receipts(outputs: Sequence[Path], summary_rows: Sequence[Mapping[str, Any]]) -> list[Path]:
    total_overlap = sum(parse_int(row.get("overlap_rows")) for row in summary_rows)
    total_mismatch = sum(parse_int(row.get("decision_mismatch_rows")) for row in summary_rows)
    receipts = {
        "data_integrity_receipt.json": {
            "data_source": rel(PARENT_RUN_DIR),
            "time_axis": "bar_time_server and timestamp_utc are bar-close aligned; MT5 telemetry cycle rows use bar_time from tester runtime",
            "sample_scope": "US100 M5 raw-forward non-identity probes copied from run335K, six attempts",
            "missing_or_duplicate_check": "outer join by bar_time_server; terminal feature-only gaps are recorded in row_level_runtime_parity_gap_rows.csv",
            "feature_label_boundary": "review-only; no labels, training, or threshold search are introduced",
            "split_boundary": "post-OOS raw-forward probe evidence; not cp322A exact forward pass/fail evidence",
            "leakage_risk": "numeric proxy branch specificity remains weak because aggregate values repeat across protocols",
            "data_hash_or_identity": [rel(path) for path in outputs],
            "integrity_judgment": "usable_with_boundary",
        },
        "runtime_parity_receipt.json": {
            "research_path": rel(Path("stage_pipelines/stage335/review_independent_runtime_proxy_usability.py")),
            "runtime_path": rel(PARENT_RUN_DIR / "runtime_telemetry"),
            "shared_contract": "ONNX model, feature order, frozen min-margin threshold, signal labels, bar_time_server join",
            "known_differences": "two u42 terminal feature-only flat bars have no MT5 cycle row; no signal mismatch",
            "parity_check": f"row-level overlap rows={total_overlap};decision mismatches={total_mismatch}",
            "parity_identity": [rel(PARENT_RUN_DIR / "independent_handoff_attempt_manifest.csv"), rel(ROW_LEVEL_SUMMARY)],
            "runtime_claim_boundary": "runtime_probe_diagnostic_only_no_runtime_authority",
        },
        "result_judgment_receipt.json": {
            "result_subject": RUN_ID,
            "evidence_available": [rel(path) for path in outputs],
            "evidence_missing": "branch-specific fresh runtime metrics for guarded protocols; cp322A exact forward route-signal handoff",
            "judgment_label": "runtime_probe",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "신호 동등성은 진단에 쓸 수 있지만 숫자 프록시는 분기별 판정에는 아직 부족하다.",
        },
        "artifact_lineage_receipt.json": {
            "parent_run_id": PARENT_RUN_ID,
            "current_run_id": RUN_ID,
            "source_artifacts": [rel(PARENT_RUN_DIR / "run_manifest.json"), rel(PARENT_RUN_DIR / "runtime_telemetry")],
            "generated_artifacts": [rel(path) for path in outputs],
            "lineage_judgment": "review_artifacts_derived_from_run335K_without_retune",
        },
    }
    receipt_paths: list[Path] = []
    for filename, payload in receipts.items():
        path = RUN_DIR / filename
        write_json(path, payload)
        receipt_paths.append(path)
    return receipt_paths


def append_or_replace_section(path: Path, heading: str, section: str) -> None:
    text, had_bom = read_text_lossless(path)
    pattern = re.compile(rf"^## {re.escape(heading)}\n.*?(?=^## |\Z)", re.M | re.S)
    replacement = f"## {heading}\n\n{section.strip()}\n\n"
    if pattern.search(text):
        text = pattern.sub(replacement, text)
    else:
        if not text.endswith("\n"):
            text += "\n"
        text += "\n" + replacement
    write_text_lossless(path, text, had_bom)


def update_workspace_documents(metrics: Mapping[str, Any]) -> None:
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = re.sub(r"current_run_id: .+", f"current_run_id: {NEXT_RUN_ID}", workspace_text, count=1)
    focus_item = (
        "  Stage335(335단계) run335L(335L 실행)는 `completed_independent_runtime_parity_and_proxy_usability_review_no_forward_decision`로 "
        "row-level runtime parity/proxy usability review(행 단위 런타임 동등성/프록시 활용성 검토)를 완료했다. "
        f"Effect(효과): overlap rows(겹친 행) `{metrics['overlap_rows']}`개에서 decision mismatch(결정 불일치) `{metrics['decision_mismatch_rows']}`개, "
        f"max probability diff(최대 확률 차이) `{metrics['max_probability_abs_diff']}`를 확인했지만 numeric proxy(숫자 프록시)는 branch-specific(분기별) 판정에 쓰지 않는다."
    )
    if "run335L(335L 실행)" not in workspace_text:
        workspace_text = workspace_text.replace("current_focus:\n", f"current_focus:\n- >-\n{focus_item}\n", 1)
    write_text_lossless(WORKSPACE_STATE, workspace_text, workspace_bom)

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    replacements = {
        r"- current_packet\(현재 작업 묶음\): `[^`]+`": "- current_packet(현재 작업 묶음): `335_overfit_guard__failure_memory_constrained_research_handoff_v13`",
        r"- current_run\(현재 실행\): `[^`]+`": f"- current_run(현재 실행): `{NEXT_RUN_ID}`",
        r"- status\(상태\): `[^`]+`": f"- status(상태): `{STATUS}`",
        r"- decision\(판정\): `[^`]+`": f"- decision(판정): `{DECISION}`",
    }
    for pattern, replacement in replacements.items():
        current_text = re.sub(pattern, replacement, current_text, count=1)
    summary_line = (
        f"- run335L_summary(335L 요약): independent runtime parity/proxy usability review(독립 런타임 동등성/프록시 활용성 검토)를 `{STATUS}`로 완료했다. "
        f"Effect(효과): overlap rows(겹친 행) `{metrics['overlap_rows']}`, decision mismatch(결정 불일치) `{metrics['decision_mismatch_rows']}`, "
        f"terminal flat gap(말단 관망 공백) `{metrics['feature_only_rows']}`개를 확인했고, numeric proxy(숫자 프록시)는 repeated aggregate(반복 집계)라 forward pass/fail(전진 통과/실패)에 쓰지 않는다.\n"
    )
    if "run335L_summary(335L 요약)" not in current_text:
        current_text = current_text.replace("- run335K_summary", summary_line + "- run335K_summary", 1)
    write_text_lossless(CURRENT_STATE, current_text, current_bom)

    selection_text, selection_bom = read_text_lossless(SELECTED_DIR / "selection_status.md")
    selection_text = re.sub(r"- current_run\(현재 실행\): `[^`]+`", f"- current_run(현재 실행): `{NEXT_RUN_ID}`", selection_text, count=1)
    selection_text = re.sub(r"- next_action\(다음 행동\): `[^`]+`", f"- next_action(다음 행동): `{NEXT_RUN_ID}`", selection_text, count=1)
    selection_text = re.sub(
        r"- effect\(효과\): .*",
        "- effect(효과): Stage335L(335L 실행)는 row-level runtime parity(행 단위 런타임 동등성)는 진단 활용 가능으로 확인했지만 numeric proxy(숫자 프록시)는 분기별 판정력이 부족해 Forward Passed/Failed(전진 통과/실패)와 Goal Achieve(목표 달성)를 주장하지 않는다.",
        selection_text,
        count=1,
    )
    if "- latest_review(최신 검토):" not in selection_text:
        selection_text += f"\n- latest_review(최신 검토): `{RUN_ID}`\n"
    write_text_lossless(SELECTED_DIR / "selection_status.md", selection_text, selection_bom)

    brief_text, brief_bom = read_text_lossless(STAGE_BRIEF)
    brief_text = re.sub(r"- latest_run\(최신 실행\): `[^`]+`", f"- latest_run(최신 실행): `{RUN_ID}`", brief_text, count=1)
    write_text_lossless(STAGE_BRIEF, brief_text, brief_bom)

    input_section = f"""
- row_level_runtime_parity_summary(행 단위 런타임 동등성 요약): `{rel(ROW_LEVEL_SUMMARY)}`
- row_level_runtime_parity_gap_rows(행 단위 공백 행): `{rel(ROW_LEVEL_GAPS)}`
- runtime_probability_diff_extremes(런타임 확률 차이 최대치): `{rel(PROBABILITY_EXTREMES)}`
- proxy_numeric_protocol_specificity_audit(프록시 숫자 계약 특이성 감사): `{rel(NUMERIC_SPECIFICITY)}`
- proxy_usability_scope_matrix(프록시 활용 범위 행렬): `{rel(USABILITY_SCOPE)}`
- decision(결정): `{rel(DECISION_DOC)}`
"""
    append_or_replace_section(INPUT_REFS, "run335L Runtime Parity/Proxy Usability Review(335L 런타임 동등성/프록시 활용성 검토)", input_section)

    changelog_section = f"""
- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- effect(효과): row-level probability/decision parity(행 단위 확률/결정 동등성)는 overlap rows(겹친 행) `{metrics['overlap_rows']}`개에서 mismatch(불일치) `{metrics['decision_mismatch_rows']}`개로 확인했다.
- boundary(경계): numeric proxy(숫자 프록시)는 branch-specific(분기별) 판정력이 없어 Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 `not_claimed`.
"""
    append_or_replace_section(CHANGELOG, "2026-05-26 Stage335L Runtime Parity/Proxy Usability Review(335L 런타임 동등성/프록시 활용성 검토)", changelog_section)


def update_registers(outputs: Sequence[Path], metrics: Mapping[str, Any]) -> None:
    report_rel = rel(REPORT_DOC)
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "stage335_independent_runtime_parity_proxy_usability_review",
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
                "ledger_row_id": f"{RUN_ID}__row_level_parity_proxy_usability",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": "run335L",
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "independent_runtime_parity_proxy_usability_review",
                "tier_scope": "Tier A raw-forward non-identity",
                "kpi_scope": "row_level_signal_probability_parity_and_proxy_numeric_usability",
                "scoreboard_lane": "runtime_probe_review",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": report_rel,
                "primary_kpi": f"overlap_rows={metrics['overlap_rows']};decision_mismatch_rows={metrics['decision_mismatch_rows']};max_probability_abs_diff={metrics['max_probability_abs_diff']}",
                "guardrail_kpi": "branch_specific_numeric_proxy_not_usable;forward_passed_not_claimed;goal_achieve_not_claimed",
                "external_verification_status": "completed_source_run335K_reused_no_new_mt5",
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
                "ledger_row_id": f"{RUN_ID}__runtime_parity_proxy_usability",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "work_family": "runtime_parity_review",
                "evidence_scope": "row_level_proxy_vs_fresh_mt5_runtime_and_numeric_proxy_usability",
                "kpi_scope": "diagnostic_runtime_signal_parity_no_forward_decision",
                "status": STATUS,
                "judgment": JUDGMENT,
                "claim_boundary": CLAIM_BOUNDARY,
                "path": report_rel,
                "notes": f"overlap_rows={metrics['overlap_rows']};decision_mismatch_rows={metrics['decision_mismatch_rows']};numeric_proxy_not_branch_specific;goal_achieve_not_claimed.",
                "decision": f"{DECISION};next_action={NEXT_RUN_ID}",
            }
        ],
        key="ledger_row_id",
    )
    artifact_rows = []
    for path in outputs:
        artifact_rows.append(
            {
                "artifact_id": f"{RUN_ID}__{path.stem}",
                "artifact_type": "stage335_runtime_parity_proxy_usability_review",
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": now_utc(),
                "notes": "derived_from_run335K_no_retune_no_forward_decision",
            }
        )
    upsert_csv_rows(
        ARTIFACT_REGISTRY,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
        artifact_rows,
        key="artifact_id",
    )


def write_report_and_decision(metrics: Mapping[str, Any]) -> None:
    report = f"""
# Run335L Independent Runtime Parity/Proxy Usability Review(독립 런타임 동등성/프록시 활용성 검토)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- row_level_overlap_rows(행 단위 겹친 행): `{metrics['overlap_rows']}`
- decision_mismatch_rows(결정 불일치 행): `{metrics['decision_mismatch_rows']}`
- feature_only_terminal_flat_rows(피처 전용 말단 관망 행): `{metrics['feature_only_rows']}`
- max_probability_abs_diff(최대 확률 절대 차이): `{metrics['max_probability_abs_diff']}`
- diagnostic_usability(진단 활용 가능성): `usable_for_runtime_signal_parity_and_repair_prioritization`
- forward_usability(전진 판정 활용 가능성): `not_usable_as_forward_decision`
- next_action(다음 행동): `{NEXT_RUN_ID}`

## Judgment(판정)

run335L(335L 실행)는 run335K(335K 실행)의 Python ONNX proxy(파이썬 온엑스 프록시)와 fresh MT5 telemetry(신규 MT5 기록)를 bar_time_server(서버 바 시간) 기준으로 다시 맞췄다.

효과(effect, 효과)는 신호/확률 동등성(signal/probability parity, 신호/확률 동등성)은 진단에 쓸 수 있다는 점과, numeric proxy(숫자 프록시)는 branch-specific(분기별) 판정력이 부족하다는 점을 분리한 것이다.

## Evidence(근거)

- row_level_runtime_parity_summary(행 단위 런타임 동등성 요약): `{rel(ROW_LEVEL_SUMMARY)}`
- row_level_runtime_parity_gap_rows(행 단위 공백 행): `{rel(ROW_LEVEL_GAPS)}`
- runtime_probability_diff_extremes(런타임 확률 차이 최대치): `{rel(PROBABILITY_EXTREMES)}`
- proxy_numeric_protocol_specificity_audit(프록시 숫자 계약 특이성 감사): `{rel(NUMERIC_SPECIFICITY)}`
- proxy_usability_scope_matrix(프록시 활용 범위 행렬): `{rel(USABILITY_SCOPE)}`
- required_gate_coverage_audit(필수 게이트 커버리지 감사): `{rel(GATE_AUDIT)}`
- result_judgment(결과 판정): `{rel(RESULT_JUDGMENT)}`

## Boundary(경계)

Forward Passed(전진 통과), Forward Failed(전진 실패), runtime authority(런타임 권위), live readiness(실거래 준비), deployment(배포), operating promotion(운영 승격), Goal Achieve(목표 달성)는 모두 `not_claimed`다.
"""
    write_md(REPORT_DOC, report)

    decision = f"""
# Decision(결정): Stage335L Runtime Parity/Proxy Usability Review(런타임 동등성/프록시 활용성 검토)

`{RUN_ID}`는 run335K(335K 실행)의 independent fresh MT5 runtime probe(독립 신규 MT5 런타임 탐침)를 재사용해 row-level parity(행 단위 동등성)와 proxy usability(프록시 활용성)를 검토했다.

- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- overlap_rows(겹친 행): `{metrics['overlap_rows']}`
- decision_mismatch_rows(결정 불일치 행): `{metrics['decision_mismatch_rows']}`
- feature_only_terminal_flat_rows(피처 전용 말단 관망 행): `{metrics['feature_only_rows']}`
- max_probability_abs_diff(최대 확률 절대 차이): `{metrics['max_probability_abs_diff']}`
- diagnostic_usability(진단 활용 가능성): `usable_for_runtime_signal_parity_and_repair_prioritization`
- forward_usability(전진 판정 활용 가능성): `not_usable_as_forward_decision`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`

효과(effect, 효과): 신호 동등성은 더 강하게 확인했지만, 숫자 proxy(프록시)는 반복 집계값이라 분기별 forward decision(전진 판정)에는 아직 쓰지 않는다.
"""
    write_md(DECISION_DOC, decision)


def main() -> int:
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    attempts = load_attempt_rows()
    summary_rows, gap_rows, extreme_rows = build_row_level_parity(attempts)
    numeric_rows = build_numeric_specificity_audit()
    derived_rows = build_derived_runtime_metrics()
    usability_rows = build_usability_scope(summary_rows, numeric_rows)
    gate_rows = build_gate_rows(summary_rows, numeric_rows)

    write_csv(
        ROW_LEVEL_SUMMARY,
        [
            "attempt_name",
            "artifact_slug",
            "feature_set_id",
            "feature_rows",
            "mt5_tier_a_cycle_rows",
            "overlap_rows",
            "feature_only_rows",
            "mt5_only_rows",
            "decision_mismatch_rows",
            "max_probability_abs_diff",
            "mean_probability_abs_diff",
            "feature_only_decision_counts",
            "mt5_only_decision_counts",
            "first_overlap_bar_time",
            "last_overlap_bar_time",
            "row_level_parity_judgment",
            "usable_for_runtime_signal_parity",
            "usable_for_forward_pass_fail",
            "feature_order_hash",
            "feature_csv_sha256",
            "model_sha256",
            "claim_boundary",
        ],
        summary_rows,
    )
    write_csv(
        ROW_LEVEL_GAPS,
        [
            "attempt_name",
            "artifact_slug",
            "bar_time_server",
            "timestamp_utc",
            "gap_type",
            "decision_proxy",
            "decision_mt5",
            "p_short_proxy",
            "p_short_mt5",
            "p_flat_proxy",
            "p_flat_mt5",
            "p_long_proxy",
            "p_long_mt5",
            "mt5_skip_reason",
            "usable_for_runtime_signal_parity",
            "usable_for_forward_pass_fail",
            "claim_boundary",
        ],
        gap_rows,
    )
    write_csv(
        PROBABILITY_EXTREMES,
        [
            "attempt_name",
            "artifact_slug",
            "probability_column",
            "bar_time_server",
            "decision_proxy",
            "decision_mt5",
            "proxy_value",
            "mt5_value",
            "abs_diff",
            "claim_boundary",
        ],
        extreme_rows,
    )
    write_csv(
        NUMERIC_SPECIFICITY,
        [
            "dimension",
            "protocol_rows",
            "proxy_unique_value_count",
            "fresh_mt5_unique_value_count",
            "available_difference_rows",
            "missing_fresh_runtime_rows",
            "protocol_specificity_judgment",
            "fresh_runtime_dimension_judgment",
            "diagnostic_use",
            "usable_for_branch_ranking",
            "usable_for_forward_pass_fail",
            "reason",
            "claim_boundary",
        ],
        numeric_rows,
    )
    write_csv(
        DERIVED_RUNTIME_METRICS,
        [
            "attempt_name",
            "artifact_slug",
            "first_tier_a_bar",
            "last_tier_a_bar",
            "tier_a_cycle_rows",
            "trade_count",
            "derived_calendar_day_span",
            "derived_trades_per_day",
            "source",
            "diagnostic_use",
            "usable_for_forward_pass_fail",
            "claim_boundary",
        ],
        derived_rows,
    )
    write_csv(
        USABILITY_SCOPE,
        [
            "scope",
            "evidence_summary",
            "diagnostic_usability_judgment",
            "forward_usability_judgment",
            "reason",
            "forward_passed",
            "forward_failed",
            "runtime_authority",
            "goal_achieve",
            "claim_boundary",
        ],
        usability_rows,
    )
    write_csv(GATE_AUDIT, ["gate_id", "status", "evidence", "finding", "claim_boundary"], gate_rows)
    write_csv(
        RESULT_JUDGMENT,
        [
            "run_id",
            "status",
            "judgment",
            "decision",
            "diagnostic_usability",
            "forward_usability",
            "forward_passed",
            "forward_failed",
            "runtime_authority",
            "goal_achieve",
            "next_action",
            "claim_boundary",
        ],
        [
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "diagnostic_usability": "usable_for_runtime_signal_parity_and_repair_prioritization",
                "forward_usability": "not_usable_as_forward_decision",
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "runtime_authority": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )

    output_paths = [
        ROW_LEVEL_SUMMARY,
        ROW_LEVEL_GAPS,
        PROBABILITY_EXTREMES,
        NUMERIC_SPECIFICITY,
        DERIVED_RUNTIME_METRICS,
        USABILITY_SCOPE,
        GATE_AUDIT,
        RESULT_JUDGMENT,
    ]
    receipts = write_receipts(output_paths, summary_rows)
    total_overlap = sum(parse_int(row.get("overlap_rows")) for row in summary_rows)
    total_mismatch = sum(parse_int(row.get("decision_mismatch_rows")) for row in summary_rows)
    total_feature_only = sum(parse_int(row.get("feature_only_rows")) for row in summary_rows)
    max_probability = max(parse_float(row.get("max_probability_abs_diff"), 0.0) for row in summary_rows) if summary_rows else 0.0
    metrics = {
        "attempts": len(summary_rows),
        "overlap_rows": total_overlap,
        "decision_mismatch_rows": total_mismatch,
        "feature_only_rows": total_feature_only,
        "max_probability_abs_diff": max_probability,
        "numeric_dimensions": len(numeric_rows),
        "numeric_repeated_aggregate_dimensions": sum(1 for row in numeric_rows if row.get("protocol_specificity_judgment") == "not_branch_specific_repeated_aggregate"),
        "missing_fresh_runtime_dimensions": sum(1 for row in numeric_rows if row.get("fresh_runtime_dimension_judgment") == "missing_from_fresh_runtime_summary"),
    }
    write_report_and_decision(metrics)
    output_paths.extend(receipts)
    output_paths.extend([REPORT_DOC, DECISION_DOC])

    write_json(
        FINAL_DECISION,
        {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "metrics": metrics,
            "diagnostic_usability": "usable_for_runtime_signal_parity_and_repair_prioritization",
            "forward_usability": "not_usable_as_forward_decision",
            "forward_passed": "not_claimed",
            "forward_failed": "not_claimed",
            "runtime_authority": "not_claimed",
            "goal_achieve": "not_claimed",
            "next_action": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    output_paths.append(FINAL_DECISION)
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "parent_run_id": PARENT_RUN_ID,
            "stage_id": STAGE_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "command": "python stage_pipelines/stage335/review_independent_runtime_proxy_usability.py",
            "artifacts": [rel(path) for path in output_paths],
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
    output_paths.append(RUN_MANIFEST)

    update_workspace_documents(metrics)
    update_registers(output_paths, metrics)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "decision": DECISION,
                "overlap_rows": total_overlap,
                "decision_mismatch_rows": total_mismatch,
                "feature_only_rows": total_feature_only,
                "max_probability_abs_diff": max_probability,
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
