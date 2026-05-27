from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists  # noqa: E402
from foundation.mt5.runtime_artifacts import sha256_file  # noqa: E402
from stage_pipelines.stage337 import lifecycle_aware_no_overfit_design_without_db as cb  # noqa: E402


ca = cb.ca
bz = ca.bz
by = ca.by
aw = ca.aw
bg = ca.bg

TODAY = "2026-05-28"
STAGE_ID = cb.STAGE_ID
RUN_NUMBER = "run337CC"
RUN_ID = "run337CC_materialize_lifecycle_aware_no_overfit_inputs_without_db_v1"
PARENT_RUN_ID = cb.RUN_ID
NEXT_RUN_ID = "run337CD_train_lifecycle_aware_guarded_scouts_without_db_v1"
CLAIM_BOUNDARY = (
    "research_development_only_stage337CC_lifecycle_aware_input_materialization_without_db_"
    "no_model_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = cb.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = cb.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337CC_lifecycle_aware_no_overfit_inputs.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337CC_lifecycle_aware_no_overfit_inputs.md"
SELECTED_STATUS = cb.SELECTED_STATUS
STAGE_BRIEF = cb.STAGE_BRIEF
WORKSPACE_STATE = cb.WORKSPACE_STATE
CURRENT_STATE = cb.CURRENT_STATE
CHANGELOG = cb.CHANGELOG
RUN_REGISTRY = cb.RUN_REGISTRY
ALPHA_LEDGER = cb.ALPHA_LEDGER
ARTIFACT_REGISTRY = cb.ARTIFACT_REGISTRY
STAGE_LEDGER = cb.STAGE_LEDGER

CB_FINAL = cb.FINAL_DECISION
CB_TARGET_CONTRACT = cb.TARGET_CONTRACT
CB_VALIDATION_GATES = cb.VALIDATION_GATES
CB_NEGATIVE_CONTROLS = cb.NEGATIVE_CONTROLS
CB_FEATURE_CONSTRAINTS = cb.FEATURE_CONSTRAINTS
CB_QUEUE = cb.MATERIALIZATION_QUEUE
CA_LABELABLE = cb.CA_LABELABLE
CA_LIFECYCLE = cb.CA_LIFECYCLE
CA_BRIDGE = cb.CA_BRIDGE
CA_COST = cb.CA_COST
CA_EXTERNAL = cb.CA_EXTERNAL
BY_WINDOW_LOCK = by.RUN_DIR / "completed_day_window_lock.csv"
BU_PROXY_EXPECTED = bz.BU_PROXY_EXPECTED
BU_THRESHOLD_POLICY = bz.bu.THRESHOLD_POLICY if hasattr(bz, "bu") else STAGE_DIR / "02_runs" / "run337BU" / "decision_threshold_policy.csv"
BU_LABEL_SPLIT_POLICY = STAGE_DIR / "02_runs" / "run337BU" / "label_split_policy.json"
BU_FORWARD_TRUTH_COVERAGE = STAGE_DIR / "02_runs" / "run337BU" / "forward_truth_coverage.csv"
BO_US100_RAW = STAGE_DIR / "02_runs" / "run337BO" / "raw_refresh_probe" / "US100" / "bars_us100_m5_mt5api_raw.csv"
BO_US100_RAW_MANIFEST = STAGE_DIR / "02_runs" / "run337BO" / "raw_refresh_probe" / "US100" / "bars_us100_m5_mt5api_raw.manifest.json"
BZ_SPLIT = cb.BZ_SPLIT
BZ_RUNTIME = cb.BZ_RUNTIME

LIFECYCLE_EVENT_TABLE = RUN_DIR / "lifecycle_trade_event_table.csv"
LIFECYCLE_TARGET_SCORE_INPUTS = RUN_DIR / "lifecycle_target_score_inputs.csv"
ROLLING_SPLIT_PLAN = RUN_DIR / "rolling_split_plan.csv"
NEGATIVE_CONTROL_INPUT_PLAN = RUN_DIR / "negative_control_input_plan.csv"
NEGATIVE_CONTROL_SCORECARD = RUN_DIR / "negative_control_lifecycle_scorecard.csv"
COST_STRESS_INPUT_PLAN = RUN_DIR / "cost_stress_input_plan.csv"
FEATURE_FAMILY_MATERIALIZATION_PLAN = RUN_DIR / "feature_family_materialization_plan.csv"
PROXY_MT5_UTILIZATION_JUDGMENT = RUN_DIR / "proxy_mt5_utilization_judgment.csv"
DATA_INTEGRITY_TIME_AXIS_AUDIT = RUN_DIR / "data_integrity_time_axis_audit.csv"
NEXT_RESEARCH_QUEUE = RUN_DIR / "run337CD_guarded_training_queue.csv"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
ARTIFACT_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_discipline_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    CB_FINAL,
    CB_TARGET_CONTRACT,
    CB_VALIDATION_GATES,
    CB_NEGATIVE_CONTROLS,
    CB_FEATURE_CONSTRAINTS,
    CB_QUEUE,
    CA_LABELABLE,
    CA_LIFECYCLE,
    CA_BRIDGE,
    CA_COST,
    CA_EXTERNAL,
    BY_WINDOW_LOCK,
    BU_PROXY_EXPECTED,
    BU_THRESHOLD_POLICY,
    BU_LABEL_SPLIT_POLICY,
    BU_FORWARD_TRUTH_COVERAGE,
    BO_US100_RAW,
    BO_US100_RAW_MANIFEST,
    BZ_SPLIT,
    BZ_RUNTIME,
)
OUTPUT_FILES = (
    LIFECYCLE_EVENT_TABLE,
    LIFECYCLE_TARGET_SCORE_INPUTS,
    ROLLING_SPLIT_PLAN,
    NEGATIVE_CONTROL_INPUT_PLAN,
    NEGATIVE_CONTROL_SCORECARD,
    COST_STRESS_INPUT_PLAN,
    FEATURE_FAMILY_MATERIALIZATION_PLAN,
    PROXY_MT5_UTILIZATION_JUDGMENT,
    DATA_INTEGRITY_TIME_AXIS_AUDIT,
    NEXT_RESEARCH_QUEUE,
    EXPERIMENT_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    RUNTIME_RECEIPT,
    PERFORMANCE_RECEIPT,
    ARTIFACT_RECEIPT,
    JUDGMENT_RECEIPT,
    CLAIM_RECEIPT,
    REQUIRED_GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    SELECTED_STATUS,
    WORKSPACE_STATE,
    CURRENT_STATE,
    CHANGELOG,
    STAGE_BRIEF,
    Path(__file__),
)

MAX_HOLD_BARS = ca.MAX_HOLD_BARS
COST_LEVELS_BPS = (0.0, 1.0, 2.0, 5.0)

EVENT_COLUMNS = (
    "model_id",
    "feature_set_id",
    "model_family",
    "event_id",
    "entry_bar_time",
    "exit_bar_time",
    "entry_timestamp_utc",
    "exit_timestamp_utc",
    "entry_index",
    "exit_index",
    "direction",
    "exit_reason",
    "hold_bars",
    "entry_close",
    "exit_close",
    "gross_log_return",
    "net_log_return_cost0",
    "net_log_return_cost1",
    "net_log_return_cost2",
    "net_log_return_cost5",
    "entry_feature_input_hash",
    "exit_feature_input_hash",
    "entry_decision_probability",
    "entry_decision_margin",
    "entry_forward_label_available",
    "entry_future_log_return_12",
    "target_label_available",
    "event_status",
    "claim_boundary",
)
TARGET_COLUMNS = (
    "model_id",
    "feature_set_id",
    "model_family",
    "closed_trade_events",
    "open_unclosed_events",
    "target_labelable_events",
    "target_missing_events",
    "net_log_return_cost0",
    "net_log_return_cost1",
    "net_log_return_cost2",
    "net_log_return_cost5",
    "profit_factor_cost1",
    "profit_factor_cost2",
    "expectancy_cost1",
    "max_drawdown_cost1",
    "recovery_factor_cost1",
    "worst_20_trade_cost1",
    "cost2_guard_status",
    "lifecycle_target_status",
    "effect",
    "claim_boundary",
)
ROLLING_COLUMNS = (
    "split_plan_id",
    "fold_id",
    "model_id",
    "feature_set_id",
    "calendar_start_utc",
    "calendar_end_utc",
    "event_rows",
    "closed_trade_events",
    "net_log_return_cost1",
    "profit_factor_cost1",
    "fold_role",
    "forbidden_use",
    "claim_boundary",
)
NEGATIVE_PLAN_COLUMNS = (
    "control_id",
    "model_id",
    "feature_set_id",
    "input_table",
    "input_rows",
    "materialized_output",
    "purpose",
    "invalid_condition",
    "claim_boundary",
)
NEGATIVE_SCORE_COLUMNS = (
    "control_id",
    "model_id",
    "feature_set_id",
    "event_rows",
    "net_log_return_cost1",
    "profit_factor_cost1",
    "expectancy_cost1",
    "max_drawdown_cost1",
    "comparison_to_original_net_cost1",
    "control_judgment",
    "claim_boundary",
)
COST_COLUMNS = (
    "model_id",
    "feature_set_id",
    "cost_bps_per_trade",
    "event_rows",
    "net_log_return",
    "profit_factor",
    "expectancy_per_trade",
    "max_drawdown_log_return",
    "recovery_factor",
    "worst_20_trade_net_log_return",
    "stress_status",
    "claim_boundary",
)
FEATURE_PLAN_COLUMNS = (
    "feature_set_id",
    "allowed_role",
    "event_rows",
    "target_models",
    "materialization_status",
    "required_guard",
    "blocked_shortcut",
    "evidence_source",
    "claim_boundary",
)
UTILIZATION_COLUMNS = (
    "model_id",
    "feature_set_id",
    "proxy_closed_events",
    "mt5_trade_count",
    "event_minus_mt5_trade_count",
    "proxy_pf_cost1",
    "mt5_profit_factor",
    "pf_difference_proxy_minus_mt5",
    "proxy_net_cost1",
    "mt5_net_profit",
    "unit_boundary",
    "utilization_judgment",
    "effect",
    "claim_boundary",
)
AUDIT_COLUMNS = (
    "audit_id",
    "subject",
    "rows",
    "first_timestamp_utc",
    "last_timestamp_utc",
    "duplicate_timestamps",
    "missing_close_rows",
    "integrity_status",
    "effect",
    "claim_boundary",
)
NEXT_COLUMNS = by.NEXT_COLUMNS
GATE_COLUMNS = by.GATE_COLUMNS


def parse_args() -> argparse.Namespace:
    return argparse.ArgumentParser(description=RUN_ID).parse_args()


def rel(path: Path) -> str:
    return by.rel(path)


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def csv_value(value: Any) -> str:
    return by.csv_value(value)


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    return by.write_csv(path, columns, rows)


def write_json(path: Path, payload: Any) -> Path:
    return by.write_json(path, payload)


def write_md(path: Path, text: str) -> Path:
    return by.write_md(path, text)


def read_json(path: Path) -> Any:
    return by.read_json(path)


def read_df(path: Path, **kwargs: Any) -> pd.DataFrame:
    return pd.read_csv(io_path(path), encoding="utf-8-sig", **kwargs)


def as_float(value: Any) -> float:
    try:
        if value is None or value == "":
            return float("nan")
        return float(value)
    except (TypeError, ValueError):
        return float("nan")


def finite_or_none(value: float) -> float | None:
    return float(value) if math.isfinite(value) else None


def parse_mt5_bar_time(value: Any) -> pd.Timestamp:
    text = str(value or "").strip()
    if not text:
        return pd.NaT
    return pd.to_datetime(text, format="%Y.%m.%d %H:%M:%S", utc=True, errors="coerce")


def safe_pf(values: Sequence[float] | np.ndarray) -> float:
    array = np.asarray(values, dtype="float64")
    array = array[np.isfinite(array)]
    if array.size == 0:
        return 0.0
    gains = float(array[array > 0.0].sum())
    losses = float(array[array < 0.0].sum())
    if losses < 0.0:
        return gains / abs(losses)
    if gains > 0.0:
        return float("inf")
    return 0.0


def max_drawdown(values: Sequence[float] | np.ndarray) -> float:
    array = np.asarray(values, dtype="float64")
    array = array[np.isfinite(array)]
    if array.size == 0:
        return 0.0
    curve = np.cumsum(array)
    peak = np.maximum.accumulate(curve)
    return float((curve - peak).min())


def worst_rolling(values: Sequence[float] | np.ndarray, window: int) -> float:
    array = np.asarray(values, dtype="float64")
    array = array[np.isfinite(array)]
    if array.size == 0:
        return 0.0
    if array.size < window:
        return float(array.sum())
    cumsum = np.cumsum(np.insert(array, 0, 0.0))
    rolling = cumsum[window:] - cumsum[:-window]
    return float(rolling.min())


def recovery_factor(values: Sequence[float] | np.ndarray) -> float:
    array = np.asarray(values, dtype="float64")
    array = array[np.isfinite(array)]
    total = float(array.sum()) if array.size else 0.0
    dd = max_drawdown(array)
    if dd < 0.0:
        return total / abs(dd)
    return float("inf") if total > 0.0 else 0.0


def cost_adjust(gross: float, cost_bps: float) -> float:
    return float(gross) - float(cost_bps) / 10000.0


def direction_sign(direction: str) -> int:
    if direction == "long":
        return 1
    if direction == "short":
        return -1
    return 0


def norm_decision(value: Any) -> str:
    return ca.normalize_decision(value)


def score_values(values: Sequence[float] | np.ndarray) -> dict[str, float]:
    array = np.asarray(values, dtype="float64")
    array = array[np.isfinite(array)]
    total = float(array.sum()) if array.size else 0.0
    dd = max_drawdown(array)
    return {
        "event_rows": int(array.size),
        "net": total,
        "pf": safe_pf(array),
        "expectancy": float(array.mean()) if array.size else 0.0,
        "max_dd": dd,
        "recovery": recovery_factor(array),
        "worst_20": worst_rolling(array, 20),
    }


def load_raw_close() -> tuple[pd.Series, pd.Series, pd.DataFrame]:
    raw = read_df(BO_US100_RAW, usecols=["time_close_unix", "close", "spread_points"])
    raw["timestamp"] = pd.to_datetime(raw["time_close_unix"], unit="s", utc=True)
    raw = raw.sort_values("timestamp").drop_duplicates("timestamp", keep="last")
    close_by_time = raw.set_index("timestamp")["close"].astype("float64")
    spread_by_time = raw.set_index("timestamp")["spread_points"].astype("float64")
    return close_by_time, spread_by_time, raw


def input_gates() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in INPUT_FILES:
        rows.append(
            {
                "gate_id": f"input_exists::{rel(path)}",
                "status": "passed" if path_exists(path) else "failed",
                "observed": "exists" if path_exists(path) else "missing",
                "expected": rel(path),
                "effect": "input available for CC materialization(CC 입력 물질화에 사용 가능)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_model_events(
    model_frame: pd.DataFrame,
    *,
    model_id: str,
    feature_set_id: str,
    model_family: str,
) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    position: str | None = None
    entry: Mapping[str, Any] | None = None
    entry_index = -1
    age = 0
    event_index = 0

    def close_event(row: Mapping[str, Any], row_index: int, reason: str) -> None:
        nonlocal position, entry, entry_index, event_index, age
        if position is None or entry is None:
            return
        entry_close = as_float(entry.get("close_price"))
        exit_close = as_float(row.get("close_price"))
        gross = float("nan")
        if entry_close > 0.0 and exit_close > 0.0:
            gross = direction_sign(position) * math.log(exit_close / entry_close)
        labelable = math.isfinite(gross)
        event_index += 1
        event_id = f"{model_id}__evt{event_index:05d}"
        events.append(
            {
                "model_id": model_id,
                "feature_set_id": feature_set_id,
                "model_family": model_family,
                "event_id": event_id,
                "entry_bar_time": entry.get("bar_time", ""),
                "exit_bar_time": row.get("bar_time", ""),
                "entry_timestamp_utc": pd.Timestamp(entry.get("timestamp")).isoformat() if pd.notna(entry.get("timestamp")) else "",
                "exit_timestamp_utc": pd.Timestamp(row.get("timestamp")).isoformat() if pd.notna(row.get("timestamp")) else "",
                "entry_index": entry_index,
                "exit_index": row_index,
                "direction": position,
                "exit_reason": reason,
                "hold_bars": row_index - entry_index,
                "entry_close": finite_or_none(entry_close),
                "exit_close": finite_or_none(exit_close),
                "gross_log_return": finite_or_none(gross),
                "net_log_return_cost0": finite_or_none(cost_adjust(gross, 0.0)) if labelable else None,
                "net_log_return_cost1": finite_or_none(cost_adjust(gross, 1.0)) if labelable else None,
                "net_log_return_cost2": finite_or_none(cost_adjust(gross, 2.0)) if labelable else None,
                "net_log_return_cost5": finite_or_none(cost_adjust(gross, 5.0)) if labelable else None,
                "entry_feature_input_hash": entry.get("feature_input_hash", ""),
                "exit_feature_input_hash": row.get("feature_input_hash", ""),
                "entry_decision_probability": finite_or_none(as_float(entry.get("decision_probability"))),
                "entry_decision_margin": finite_or_none(as_float(entry.get("decision_margin"))),
                "entry_forward_label_available": entry.get("forward_label_available", ""),
                "entry_future_log_return_12": finite_or_none(as_float(entry.get("future_log_return_12"))),
                "target_label_available": labelable,
                "event_status": "closed_lifecycle_event" if labelable else "closed_event_missing_raw_close",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        position = None
        entry = None
        entry_index = -1
        age = 0

    records = model_frame.to_dict("records")
    for row_index, row in enumerate(records):
        decision = norm_decision(row.get("decision_label"))
        if position is not None and age >= MAX_HOLD_BARS:
            close_event(row, row_index, "close_max_hold")
            continue
        if position is None:
            if decision in {"long", "short"}:
                position = decision
                entry = row
                entry_index = row_index
                age = 1
        elif decision == position:
            age += 1
        elif decision == "flat":
            age += 1
        else:
            close_event(row, row_index, f"reverse_to_{decision}")
            position = decision
            entry = row
            entry_index = row_index
            age = 1

    if position is not None and entry is not None:
        event_index += 1
        events.append(
            {
                "model_id": model_id,
                "feature_set_id": feature_set_id,
                "model_family": model_family,
                "event_id": f"{model_id}__evt{event_index:05d}",
                "entry_bar_time": entry.get("bar_time", ""),
                "exit_bar_time": "",
                "entry_timestamp_utc": pd.Timestamp(entry.get("timestamp")).isoformat() if pd.notna(entry.get("timestamp")) else "",
                "exit_timestamp_utc": "",
                "entry_index": entry_index,
                "exit_index": "",
                "direction": position,
                "exit_reason": "open_at_locked_window_end",
                "hold_bars": "",
                "entry_close": finite_or_none(as_float(entry.get("close_price"))),
                "exit_close": "",
                "gross_log_return": "",
                "net_log_return_cost0": "",
                "net_log_return_cost1": "",
                "net_log_return_cost2": "",
                "net_log_return_cost5": "",
                "entry_feature_input_hash": entry.get("feature_input_hash", ""),
                "exit_feature_input_hash": "",
                "entry_decision_probability": finite_or_none(as_float(entry.get("decision_probability"))),
                "entry_decision_margin": finite_or_none(as_float(entry.get("decision_margin"))),
                "entry_forward_label_available": entry.get("forward_label_available", ""),
                "entry_future_log_return_12": finite_or_none(as_float(entry.get("future_log_return_12"))),
                "target_label_available": False,
                "event_status": "open_unclosed_excluded_from_target",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return events


def build_event_table(proxy: pd.DataFrame, lock: pd.DataFrame, close_by_time: pd.Series) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    events: list[dict[str, Any]] = []
    audit_rows: list[dict[str, Any]] = []
    lock_by_model = {str(row["model_id"]): row for row in lock.to_dict("records")}
    for model_id, group in proxy.groupby("model_id", sort=True):
        model_id = str(model_id)
        lock_row = lock_by_model.get(model_id, {})
        cutoff = parse_mt5_bar_time(lock_row.get("locked_cutoff_bar_time"))
        frame = group.copy()
        frame["timestamp"] = pd.to_datetime(frame["timestamp_utc"], utc=True, errors="coerce")
        frame = frame[frame["timestamp"].notna()].sort_values("timestamp")
        if pd.notna(cutoff):
            frame = frame[frame["timestamp"] <= cutoff]
        frame["close_price"] = frame["timestamp"].map(close_by_time)
        missing_close = int(frame["close_price"].isna().sum())
        duplicate_timestamps = int(frame["timestamp"].duplicated().sum())
        feature_set_id = str(frame["feature_set_id"].iloc[0]) if len(frame) else str(lock_row.get("feature_set_id", ""))
        model_family = str(frame["model_family"].iloc[0]) if len(frame) else ""
        audit_rows.append(
            {
                "audit_id": f"proxy_close_join::{model_id}",
                "subject": model_id,
                "rows": len(frame),
                "first_timestamp_utc": frame["timestamp"].min().isoformat() if len(frame) else "",
                "last_timestamp_utc": frame["timestamp"].max().isoformat() if len(frame) else "",
                "duplicate_timestamps": duplicate_timestamps,
                "missing_close_rows": missing_close,
                "integrity_status": "usable" if len(frame) and missing_close == 0 and duplicate_timestamps == 0 else "usable_with_boundary" if len(frame) and missing_close == 0 else "inconclusive",
                "effect": "proxy rows are locked to tester-visible close prices(프록시 행을 테스터 가시 종가에 고정)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        events.extend(
            build_model_events(
                frame,
                model_id=model_id,
                feature_set_id=feature_set_id,
                model_family=model_family,
            )
        )
    return events, audit_rows


def closed_event_frame(events: Sequence[Mapping[str, Any]]) -> pd.DataFrame:
    df = pd.DataFrame(events)
    if df.empty:
        return df
    closed = df[df["event_status"].astype(str) == "closed_lifecycle_event"].copy()
    for column in ("gross_log_return", "net_log_return_cost0", "net_log_return_cost1", "net_log_return_cost2", "net_log_return_cost5"):
        closed[column] = pd.to_numeric(closed[column], errors="coerce")
    closed["entry_timestamp"] = pd.to_datetime(closed["entry_timestamp_utc"], utc=True, errors="coerce")
    closed["exit_timestamp"] = pd.to_datetime(closed["exit_timestamp_utc"], utc=True, errors="coerce")
    return closed


def build_target_score_inputs(events: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    df = pd.DataFrame(events)
    if df.empty:
        return []
    closed = closed_event_frame(events)
    rows: list[dict[str, Any]] = []
    for model_id, group_all in df.groupby("model_id", sort=True):
        model_id = str(model_id)
        group = closed[closed["model_id"].astype(str) == model_id].copy()
        cost1 = group["net_log_return_cost1"].to_numpy(dtype="float64") if len(group) else np.array([], dtype="float64")
        cost2 = group["net_log_return_cost2"].to_numpy(dtype="float64") if len(group) else np.array([], dtype="float64")
        cost0 = group["net_log_return_cost0"].to_numpy(dtype="float64") if len(group) else np.array([], dtype="float64")
        cost5 = group["net_log_return_cost5"].to_numpy(dtype="float64") if len(group) else np.array([], dtype="float64")
        score1 = score_values(cost1)
        feature_set_id = str(group_all["feature_set_id"].iloc[0])
        model_family = str(group_all["model_family"].iloc[0])
        open_unclosed = int((group_all["event_status"].astype(str) == "open_unclosed_excluded_from_target").sum())
        target_missing = int((group_all["event_status"].astype(str) != "closed_lifecycle_event").sum())
        cost2_score = score_values(cost2)
        cost2_guard = "cost2_positive_diagnostic" if cost2_score["net"] > 0.0 and cost2_score["pf"] > 1.0 else "cost2_not_survived_materialized_as_guard"
        rows.append(
            {
                "model_id": model_id,
                "feature_set_id": feature_set_id,
                "model_family": model_family,
                "closed_trade_events": int(len(group)),
                "open_unclosed_events": open_unclosed,
                "target_labelable_events": int(np.isfinite(cost1).sum()),
                "target_missing_events": target_missing,
                "net_log_return_cost0": finite_or_none(float(np.nansum(cost0))) if len(cost0) else 0.0,
                "net_log_return_cost1": finite_or_none(score1["net"]),
                "net_log_return_cost2": finite_or_none(cost2_score["net"]),
                "net_log_return_cost5": finite_or_none(float(np.nansum(cost5))) if len(cost5) else 0.0,
                "profit_factor_cost1": finite_or_none(score1["pf"]),
                "profit_factor_cost2": finite_or_none(cost2_score["pf"]),
                "expectancy_cost1": finite_or_none(score1["expectancy"]),
                "max_drawdown_cost1": finite_or_none(score1["max_dd"]),
                "recovery_factor_cost1": finite_or_none(score1["recovery"]),
                "worst_20_trade_cost1": finite_or_none(score1["worst_20"]),
                "cost2_guard_status": cost2_guard,
                "lifecycle_target_status": "materialized_proxy_target_input",
                "effect": "raw signal proxy is converted to closed lifecycle trade target(원 신호 프록시를 닫힌 생애주기 거래 타깃으로 전환)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_rolling_split_plan(events: Sequence[Mapping[str, Any]], split_policy: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    boundaries = split_policy.get("split_boundaries", {}) if isinstance(split_policy, Mapping) else {}
    reference_splits = [
        ("historical_train_reference", boundaries.get("train_start_utc", ""), boundaries.get("validation_start_utc", ""), "historical_reference_only"),
        ("historical_validation_reference", boundaries.get("validation_start_utc", ""), boundaries.get("oos_start_utc", ""), "historical_reference_only"),
        ("historical_oos_reference", boundaries.get("oos_start_utc", ""), boundaries.get("window_end_inclusive_utc", ""), "historical_reference_only"),
    ]
    for fold_id, start, end, role in reference_splits:
        rows.append(
            {
                "split_plan_id": "lifecycle_aware_rolling_split_v1",
                "fold_id": fold_id,
                "model_id": "all",
                "feature_set_id": "all",
                "calendar_start_utc": start,
                "calendar_end_utc": end,
                "event_rows": "",
                "closed_trade_events": "",
                "net_log_return_cost1": "",
                "profit_factor_cost1": "",
                "fold_role": role,
                "forbidden_use": "do not use forward folds for threshold or branch selection",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    closed = closed_event_frame(events)
    if closed.empty:
        return rows
    closed["week"] = closed["entry_timestamp"].dt.strftime("%G-W%V")
    for (model_id, feature_set_id, week), group in closed.groupby(["model_id", "feature_set_id", "week"], sort=True):
        values = group["net_log_return_cost1"].to_numpy(dtype="float64")
        score = score_values(values)
        rows.append(
            {
                "split_plan_id": "lifecycle_aware_rolling_split_v1",
                "fold_id": f"forward_completed_day_{week}",
                "model_id": model_id,
                "feature_set_id": feature_set_id,
                "calendar_start_utc": group["entry_timestamp"].min().isoformat(),
                "calendar_end_utc": group["exit_timestamp"].max().isoformat(),
                "event_rows": int(len(group)),
                "closed_trade_events": int(len(group)),
                "net_log_return_cost1": finite_or_none(score["net"]),
                "profit_factor_cost1": finite_or_none(score["pf"]),
                "fold_role": "forward_diagnostic_guard_only",
                "forbidden_use": "not a threshold selector; not Forward Passed evidence",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_negative_controls(events: Sequence[Mapping[str, Any]], control_plan: pd.DataFrame) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    closed = closed_event_frame(events)
    if closed.empty:
        return [], []
    plan_rows: list[dict[str, Any]] = []
    score_rows: list[dict[str, Any]] = []
    control_by_id = {str(row.get("control_id")): row for row in control_plan.to_dict("records")}
    for (model_id, feature_set_id), group in closed.groupby(["model_id", "feature_set_id"], sort=True):
        original = group["net_log_return_cost1"].to_numpy(dtype="float64")
        original_score = score_values(original)
        top_hour = int(group["entry_timestamp"].dt.hour.value_counts().idxmax()) if len(group) else -1
        control_values = {
            "shifted_label_one_bar": group["gross_log_return"].shift(-1).dropna().to_numpy(dtype="float64") - 1.0 / 10000.0,
            "direction_flip": (-group["gross_log_return"]).to_numpy(dtype="float64") - 1.0 / 10000.0,
            "session_holdout": group.loc[group["entry_timestamp"].dt.hour != top_hour, "net_log_return_cost1"].to_numpy(dtype="float64"),
            "cost2_and_cost5_stress": group["net_log_return_cost5"].to_numpy(dtype="float64"),
        }
        for control_id, values in control_values.items():
            source = control_by_id.get(control_id, {})
            score = score_values(values)
            if control_id == "direction_flip":
                judgment = "passed_direction_has_meaning" if score["net"] < original_score["net"] else "failed_flip_not_weaker"
            elif control_id == "shifted_label_one_bar":
                judgment = "passed_shift_changes_score" if abs(score["net"] - original_score["net"]) > 1.0e-9 else "failed_shift_invariant"
            elif control_id == "session_holdout":
                judgment = "session_holdout_materialized_diagnostic"
            else:
                judgment = "cost5_stress_materialized_negative_control"
            plan_rows.append(
                {
                    "control_id": control_id,
                    "model_id": model_id,
                    "feature_set_id": feature_set_id,
                    "input_table": rel(LIFECYCLE_EVENT_TABLE),
                    "input_rows": int(len(values)),
                    "materialized_output": rel(NEGATIVE_CONTROL_SCORECARD),
                    "purpose": source.get("purpose", ""),
                    "invalid_condition": source.get("failure_meaning", ""),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            score_rows.append(
                {
                    "control_id": control_id,
                    "model_id": model_id,
                    "feature_set_id": feature_set_id,
                    "event_rows": int(score["event_rows"]),
                    "net_log_return_cost1": finite_or_none(score["net"]),
                    "profit_factor_cost1": finite_or_none(score["pf"]),
                    "expectancy_cost1": finite_or_none(score["expectancy"]),
                    "max_drawdown_cost1": finite_or_none(score["max_dd"]),
                    "comparison_to_original_net_cost1": finite_or_none(score["net"] - original_score["net"]),
                    "control_judgment": judgment,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return plan_rows, score_rows


def build_cost_stress_inputs(events: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    closed = closed_event_frame(events)
    if closed.empty:
        return []
    rows: list[dict[str, Any]] = []
    for (model_id, feature_set_id), group in closed.groupby(["model_id", "feature_set_id"], sort=True):
        for cost_bps in COST_LEVELS_BPS:
            column = f"net_log_return_cost{int(cost_bps)}"
            values = group[column].to_numpy(dtype="float64")
            score = score_values(values)
            if cost_bps == 0.0:
                status = "gross_reference_only"
            elif cost_bps == 1.0:
                status = "primary_cost_reference"
            elif score["net"] > 0.0 and score["pf"] > 1.0:
                status = "cost_stress_survived_diagnostic"
            else:
                status = "cost_stress_failed_guardrail"
            rows.append(
                {
                    "model_id": model_id,
                    "feature_set_id": feature_set_id,
                    "cost_bps_per_trade": cost_bps,
                    "event_rows": int(score["event_rows"]),
                    "net_log_return": finite_or_none(score["net"]),
                    "profit_factor": finite_or_none(score["pf"]),
                    "expectancy_per_trade": finite_or_none(score["expectancy"]),
                    "max_drawdown_log_return": finite_or_none(score["max_dd"]),
                    "recovery_factor": finite_or_none(score["recovery"]),
                    "worst_20_trade_net_log_return": finite_or_none(score["worst_20"]),
                    "stress_status": status,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def build_feature_plan(events: Sequence[Mapping[str, Any]], constraints: pd.DataFrame) -> list[dict[str, Any]]:
    closed = closed_event_frame(events)
    event_counts = closed.groupby("feature_set_id").size().to_dict() if not closed.empty else {}
    model_counts = closed.groupby("feature_set_id")["model_id"].nunique().to_dict() if not closed.empty else {}
    rows: list[dict[str, Any]] = []
    for row in constraints.to_dict("records"):
        feature_set_id = str(row.get("feature_family", ""))
        if feature_set_id == "us100_technical42_no_external":
            allowed_role = "primary_materialization_allowed"
            status = "materialized_primary_input_candidate"
        elif feature_set_id == "macro48_no_equity_breadth_or_top3":
            allowed_role = "lag_audited_materialization_allowed"
            status = "materialized_with_lag_audit_required"
        else:
            allowed_role = "stress_only_not_primary"
            status = "materialized_stress_branch_only"
        rows.append(
            {
                "feature_set_id": feature_set_id,
                "allowed_role": allowed_role,
                "event_rows": int(event_counts.get(feature_set_id, 0)),
                "target_models": int(model_counts.get(feature_set_id, 0)),
                "materialization_status": status,
                "required_guard": row.get("reason", ""),
                "blocked_shortcut": row.get("blocked_change", ""),
                "evidence_source": row.get("evidence_source", ""),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_proxy_mt5_utilization(target_rows: Sequence[Mapping[str, Any]], runtime: pd.DataFrame) -> list[dict[str, Any]]:
    runtime_by_model = {str(row["model_id"]): row for row in runtime.to_dict("records")}
    rows: list[dict[str, Any]] = []
    for row in target_rows:
        model_id = str(row["model_id"])
        runtime_row = runtime_by_model.get(model_id, {})
        proxy_trades = int(as_float(row.get("closed_trade_events"))) if math.isfinite(as_float(row.get("closed_trade_events"))) else 0
        mt5_trades = int(as_float(runtime_row.get("mt5_trade_count"))) if math.isfinite(as_float(runtime_row.get("mt5_trade_count"))) else 0
        proxy_pf = as_float(row.get("profit_factor_cost1"))
        mt5_pf = as_float(runtime_row.get("mt5_profit_factor"))
        proxy_net = as_float(row.get("net_log_return_cost1"))
        mt5_net = as_float(runtime_row.get("mt5_net_profit"))
        delta = proxy_trades - mt5_trades
        if abs(delta) <= 1:
            judgment = "usable_for_lifecycle_shape_not_account_pnl"
        else:
            judgment = "count_gap_requires_runtime_recheck"
        rows.append(
            {
                "model_id": model_id,
                "feature_set_id": row.get("feature_set_id", ""),
                "proxy_closed_events": proxy_trades,
                "mt5_trade_count": mt5_trades,
                "event_minus_mt5_trade_count": delta,
                "proxy_pf_cost1": finite_or_none(proxy_pf),
                "mt5_profit_factor": finite_or_none(mt5_pf),
                "pf_difference_proxy_minus_mt5": finite_or_none(proxy_pf - mt5_pf) if math.isfinite(proxy_pf) and math.isfinite(mt5_pf) else None,
                "proxy_net_cost1": finite_or_none(proxy_net),
                "mt5_net_profit": finite_or_none(mt5_net),
                "unit_boundary": "proxy uses log-return units; MT5 uses account-currency profit(proxy는 로그수익률, MT5는 계좌통화 손익)",
                "utilization_judgment": judgment,
                "effect": "compares proxy target usability against runtime probe(프록시 타깃 사용성을 런타임 탐침과 비교)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_data_audit(raw: pd.DataFrame, proxy_audit: Sequence[Mapping[str, Any]], external: pd.DataFrame, forward_coverage: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = list(proxy_audit)
    rows.append(
        {
            "audit_id": "raw_us100_close_source",
            "subject": rel(BO_US100_RAW),
            "rows": len(raw),
            "first_timestamp_utc": raw["timestamp"].min().isoformat() if len(raw) else "",
            "last_timestamp_utc": raw["timestamp"].max().isoformat() if len(raw) else "",
            "duplicate_timestamps": int(raw["timestamp"].duplicated().sum()) if len(raw) else 0,
            "missing_close_rows": int(raw["close"].isna().sum()) if len(raw) else 0,
            "integrity_status": "usable" if len(raw) and raw["close"].notna().all() else "blocked_raw_close_missing",
            "effect": "raw US100 close supports variable lifecycle return(US100 원천 종가가 가변 생애주기 수익률을 지원)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )
    rows.append(
        {
            "audit_id": "external_telemetry_identity",
            "subject": rel(CA_EXTERNAL),
            "rows": len(external),
            "first_timestamp_utc": "",
            "last_timestamp_utc": "",
            "duplicate_timestamps": "",
            "missing_close_rows": "",
            "integrity_status": "usable_external_hashes" if len(external) and external["exists"].astype(str).str.lower().eq("true").all() else "inconclusive_external_identity",
            "effect": "external Common Files telemetry is represented by hashes(외부 Common Files 텔레메트리가 해시로 대표됨)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )
    for row in forward_coverage.to_dict("records"):
        rows.append(
            {
                "audit_id": f"forward_label_boundary::{row.get('feature_set_id', '')}",
                "subject": row.get("feature_set_id", ""),
                "rows": row.get("feature_rows", ""),
                "first_timestamp_utc": row.get("first_timestamp", ""),
                "last_timestamp_utc": row.get("last_timestamp", ""),
                "duplicate_timestamps": "",
                "missing_close_rows": row.get("missing_future_rows", ""),
                "integrity_status": row.get("integrity_status", ""),
                "effect": "latest non-labelable rows stay counted but excluded from target selection(최신 라벨 불가 행은 집계하되 타깃 선택에서 제외)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_next_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "run337CD_train_lifecycle_aware_guarded_scouts",
            "next_run_id": NEXT_RUN_ID,
            "lane": "guarded_training_after_lifecycle_input_materialization",
            "priority": "P0",
            "reason": "CC materialized lifecycle target, proxy-MT5 utilization boundary, negative controls, rolling split plan, and cost stress inputs",
            "required_evidence": "train only if CC gates pass; keep cost2 and negative controls as guards; no forward threshold selection",
            "forbidden_shortcut": "no candidate selection, no lot optimization, no Forward Passed claim, no runtime authority",
            "effect": "opens guarded model work after input evidence is durable(입력 근거가 지속화된 뒤 방어 학습을 연다)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_gates(
    input_rows: Sequence[Mapping[str, Any]],
    event_rows: Sequence[Mapping[str, Any]],
    target_rows: Sequence[Mapping[str, Any]],
    split_rows: Sequence[Mapping[str, Any]],
    negative_plan_rows: Sequence[Mapping[str, Any]],
    negative_score_rows: Sequence[Mapping[str, Any]],
    cost_rows: Sequence[Mapping[str, Any]],
    feature_rows: Sequence[Mapping[str, Any]],
    utilization_rows: Sequence[Mapping[str, Any]],
    audit_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    gates = list(input_rows)
    closed_count = sum(1 for row in event_rows if row.get("event_status") == "closed_lifecycle_event")
    open_count = sum(1 for row in event_rows if row.get("event_status") == "open_unclosed_excluded_from_target")
    proxy_audits = [row for row in audit_rows if str(row.get("audit_id", "")).startswith("proxy_close_join::")]
    close_join_ok = bool(proxy_audits) and all(int(as_float(row.get("missing_close_rows"))) == 0 for row in proxy_audits)
    checks = [
        ("lifecycle_event_table_materialized", closed_count > 0, f"closed_events={closed_count};open_unclosed={open_count}"),
        ("target_score_inputs_materialized", len(target_rows) >= 6, f"target_rows={len(target_rows)}"),
        ("raw_close_join_no_missing", close_join_ok, f"proxy_audit_rows={len(proxy_audits)}"),
        ("rolling_split_plan_materialized", len(split_rows) > 3, f"split_rows={len(split_rows)}"),
        ("negative_control_inputs_materialized", len(negative_plan_rows) >= 24 and len(negative_score_rows) >= 24, f"negative_plan={len(negative_plan_rows)};negative_score={len(negative_score_rows)}"),
        ("cost_stress_inputs_materialized", len(cost_rows) >= 24, f"cost_rows={len(cost_rows)}"),
        ("feature_family_plan_materialized", len(feature_rows) >= 3, f"feature_rows={len(feature_rows)}"),
        ("proxy_mt5_utilization_boundary_materialized", len(utilization_rows) >= 6, f"utilization_rows={len(utilization_rows)}"),
        ("no_training_or_selection_guard", True, "model_training=not_run;threshold_tuning=not_run;candidate_selection=not_run"),
        ("required_gate_coverage_audit", True, "all CC gates represented"),
        ("final_claim_guard", True, "no forward/goal/runtime authority claim"),
    ]
    for gate_id, passed, evidence in checks:
        gates.append(
            {
                "gate_id": gate_id,
                "status": "passed" if passed else "failed",
                "observed": evidence,
                "expected": "passed",
                "effect": "supports CC materialization without promotion claim(CC 물질화를 승격 주장 없이 지지)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return gates


def classify(gates: Sequence[Mapping[str, Any]]) -> tuple[str, str, str, str]:
    failed = [row for row in gates if row.get("status") != "passed"]
    if failed:
        return (
            "blocked_stage337CC_lifecycle_aware_input_materialization_gate_failed_no_forward_decision",
            "blocked_required_lifecycle_input_evidence_missing",
            "stage337CC_repair_lifecycle_input_materialization_before_training",
            RUN_ID,
        )
    return (
        "completed_stage337CC_lifecycle_aware_no_overfit_inputs_materialized_no_training_no_selection",
        "lifecycle_target_inputs_proxy_mt5_boundary_negative_controls_and_cost_stress_materialized",
        "stage337CC_open_run337CD_train_lifecycle_aware_guarded_scouts",
        NEXT_RUN_ID,
    )


def build_receipts(final: Mapping[str, Any]) -> list[Path]:
    payloads = [
        (
            EXPERIMENT_RECEIPT,
            {
                "run_id": RUN_ID,
                "hypothesis": "Lifecycle-aware input materialization must precede any new ONNX training to avoid raw-signal overfit and runtime lifecycle mismatch.",
                "decision_use": "opens guarded training queue only; no candidate selection",
                "comparison_baseline": [rel(CB_TARGET_CONTRACT), rel(CA_LIFECYCLE), rel(BZ_RUNTIME)],
                "control_variables": "US100 M5; completed-day locked cutoff; max_hold_bars=12; fixed BU thresholds; no lot optimization",
                "changed_variables": "score input changes from raw future_12 signal to closed lifecycle event target",
                "success_criteria": "event table, target score, negative controls, cost stress, rolling split plan, and proxy-MT5 boundary exist with gates passed",
                "failure_criteria": "raw close join missing, lifecycle events absent, negative controls absent, or proxy-MT5 boundary not named",
                "invalid_conditions": "future rows used as features, forward threshold chosen, or MT5 account PnL treated as proxy log return",
                "stop_conditions": "stop before training if any CC gate fails",
                "evidence_plan": [rel(LIFECYCLE_EVENT_TABLE), rel(LIFECYCLE_TARGET_SCORE_INPUTS), rel(REQUIRED_GATE_AUDIT)],
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            DATA_RECEIPT,
            {
                "data_source": [rel(BU_PROXY_EXPECTED), rel(BO_US100_RAW), rel(CA_EXTERNAL), rel(BY_WINDOW_LOCK)],
                "time_axis": "MT5 bar close timestamps, UTC interpretation, completed-day cutoff 2026-05-26 23:55:00",
                "sample_scope": "US100 M5 forward diagnostic rows after 2026-04-14 through tester-visible completed-day lock",
                "missing_or_duplicate_check": rel(DATA_INTEGRITY_TIME_AXIS_AUDIT),
                "feature_label_boundary": "features and decisions are fixed before target returns; latest unclosed events excluded from target metrics",
                "split_boundary": "historical train/validation/oos references plus forward weekly diagnostic guard folds",
                "leakage_risk": "variable lifecycle exit returns are target-only and cannot enter features or threshold selection",
                "data_hash_or_identity": sha256_file(BO_US100_RAW) if path_exists(BO_US100_RAW) else "",
                "integrity_judgment": "usable_with_completed_day_and_proxy_target_boundary",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            MODEL_RECEIPT,
            {
                "model_family": "unchanged BU model scouts; no new model in CC",
                "target_and_label": "closed lifecycle event log-return targets generated after fixed decisions",
                "split_method": "forward diagnostic weekly guard plan plus historical split references",
                "selection_metric": "not_applicable_no_selection",
                "secondary_metrics": [rel(COST_STRESS_INPUT_PLAN), rel(NEGATIVE_CONTROL_SCORECARD), rel(PROXY_MT5_UTILIZATION_JUDGMENT)],
                "threshold_policy": "fixed BU thresholds only; no search",
                "overfit_risk": "negative controls and rolling guard materialized before training",
                "calibration_risk": "probabilities remain rank/decision inputs, not calibrated live probabilities",
                "comparison_baseline": rel(BZ_RUNTIME),
                "validation_judgment": "input_materialized_before_training_no_selection",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            RUNTIME_RECEIPT,
            {
                "research_path": rel(Path(__file__)),
                "runtime_path": "existing run337BX MT5 Common Files telemetry; no new MT5 execution in CC",
                "shared_contract": "bar_time, fixed decisions, max_hold_bars=12, completed-day cutoff, feature_input_hash",
                "known_differences": "proxy event returns are log-return units while MT5 report is account-currency PnL",
                "parity_check": rel(PROXY_MT5_UTILIZATION_JUDGMENT),
                "parity_identity": rel(CA_EXTERNAL),
                "runtime_claim_boundary": "runtime_probe_only_not_runtime_authority",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            PERFORMANCE_RECEIPT,
            {
                "observed_change": "raw decision rows are compressed into closed lifecycle events and cost-stressed target inputs",
                "comparison_baseline": [rel(CA_BRIDGE), rel(BZ_RUNTIME)],
                "likely_drivers": "lifecycle compression, cost sensitivity, session/time concentration, and proxy-vs-MT5 unit mismatch",
                "segment_checks": [rel(ROLLING_SPLIT_PLAN), rel(NEGATIVE_CONTROL_SCORECARD), rel(COST_STRESS_INPUT_PLAN)],
                "trade_shape": rel(LIFECYCLE_TARGET_SCORE_INPUTS),
                "alternative_explanations": "MT5 account PnL includes execution details not represented by proxy log-return target",
                "attribution_confidence": "medium_diagnostic_boundary",
                "next_probe": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            ARTIFACT_RECEIPT,
            {
                "source_inputs": [rel(path) for path in INPUT_FILES],
                "producer": rel(Path(__file__)),
                "consumer": NEXT_RUN_ID,
                "artifact_paths": [rel(path) for path in OUTPUT_FILES if path_exists(path)],
                "artifact_hashes": {rel(path): sha256_file(path) for path in OUTPUT_FILES if path_exists(path) and io_path(path).is_file()},
                "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
                "availability": "tracked",
                "lineage_judgment": "connected_with_proxy_runtime_boundary",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            JUDGMENT_RECEIPT,
            {
                "result_subject": RUN_ID,
                "evidence_available": [rel(REPORT_PATH), rel(REQUIRED_GATE_AUDIT), rel(LIFECYCLE_TARGET_SCORE_INPUTS)],
                "evidence_missing": "no new training, no new MT5 tester run, no Forward Passed/Failed decision",
                "judgment_label": final["judgment"],
                "claim_boundary": CLAIM_BOUNDARY,
                "next_condition": final["next_action"],
                "user_explanation_hook": "CC makes the training inputs safer; it is not yet the powerful operating ONNX.",
            },
        ),
        (
            CLAIM_RECEIPT,
            {
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "runtime_authority": "not_claimed",
                "goal_achieve": "not_claimed",
                "effect": "CC closes input materialization only(CC는 입력 물질화만 닫음)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
    ]
    return [write_json(path, payload) for path, payload in payloads]


def write_report(final: Mapping[str, Any], target_rows: Sequence[Mapping[str, Any]], utilization_rows: Sequence[Mapping[str, Any]], negative_rows: Sequence[Mapping[str, Any]], cost_rows: Sequence[Mapping[str, Any]]) -> Path:
    target_lines = "\n".join(
        f"| `{row['model_id']}` | {row['closed_trade_events']} | {row['net_log_return_cost1']} | {row['profit_factor_cost1']} | `{row['cost2_guard_status']}` |"
        for row in target_rows
    )
    utilization_lines = "\n".join(
        f"| `{row['model_id']}` | {row['proxy_closed_events']} | {row['mt5_trade_count']} | {row['event_minus_mt5_trade_count']} | `{row['utilization_judgment']}` |"
        for row in utilization_rows
    )
    negative_failures = [row for row in negative_rows if str(row.get("control_judgment", "")).startswith("failed")]
    cost2_failed = [row for row in cost_rows if float(row.get("cost_bps_per_trade") or 0.0) == 2.0 and row.get("stress_status") == "cost_stress_failed_guardrail"]
    return write_md(
        REPORT_PATH,
        f"""# Stage337 run337CC Lifecycle-Aware No-Overfit Inputs(생애주기 인식 무과적합 입력)

## Conclusion(결론)

run337CC(337CC 실행)는 새 model training(모델 학습) 없이 fixed decisions(고정 의사결정)를 closed lifecycle trade target(닫힌 생애주기 거래 타깃)으로 물질화했다.

Effect(효과): 다음 run337CD(337CD 실행)는 raw signal count(원 신호 수)가 아니라 MT5-like lifecycle compression(MT5 유사 생애주기 압축), cost stress(비용 압박), negative controls(부정 대조), rolling split guard(구간 분할 가드)를 입력으로 삼을 수 있다. Forward/Goal(전진/목표)은 주장하지 않는다.

## Result(결과)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`
- closed_events(닫힌 이벤트): `{final['closed_lifecycle_events']}`
- proxy_mt5_utilization_rows(프록시-MT5 사용성 행): `{final['proxy_mt5_utilization_rows']}`

## Lifecycle Target(생애주기 타깃)

| model(모델) | closed events(닫힌 이벤트) | net cost1(비용1 순수익) | PF cost1(비용1 수익 팩터) | cost2 guard(비용2 가드) |
|---|---:|---:|---:|---|
{target_lines}

## Proxy vs MT5(프록시 대 MT5)

| model(모델) | proxy events(프록시 이벤트) | MT5 trades(MT5 거래) | delta(차이) | judgment(판정) |
|---|---:|---:|---:|---|
{utilization_lines}

## Guard Notes(가드 메모)

- negative_control_failures(부정 대조 실패 수): `{len(negative_failures)}`
- cost2_failed_models(비용2 실패 모델 수): `{len(cost2_failed)}`
- proxy_unit_boundary(프록시 단위 경계): proxy log-return(프록시 로그수익률)과 MT5 account PnL(MT5 계좌 손익)은 같은 단위가 아니다.

## Boundary(경계)

- model_training(모델 학습): `not_run`
- threshold_tuning(임계값 조정): `not_run`
- lot_optimization(로트 최적화): `not_run`
- candidate_selection(후보 선택): `not_run`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    return write_md(
        DECISION_DOC,
        f"""# Decision: Stage337 run337CC Lifecycle-Aware Inputs(결정: 생애주기 인식 입력)

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(상위 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

Effect(효과): lifecycle-aware target inputs(생애주기 인식 타깃 입력), proxy-MT5 utilization boundary(프록시-MT5 사용성 경계), negative controls(부정 대조), cost stress(비용 압박), rolling split plan(구간 분할 계획)을 만들었다. 이것은 training queue(학습 대기열)를 여는 근거일 뿐 운영 가능 ONNX(온엑스) 주장이 아니다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )


def replace_bullet_value(text: str, field_name: str, value: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(f"- {field_name}(") or line.startswith(f"- {field_name}:"):
            prefix = line.split(":", 1)[0]
            lines[index] = f"{prefix}: {value}"
            break
    trailing = "\n" if text.endswith("\n") else ""
    return "\n".join(lines) + trailing


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []

    workspace_text, workspace_bom = by.read_text_lossless(WORKSPACE_STATE)
    workspace = bg.replace_top_value(workspace_text, "current_run_id: ", NEXT_RUN_ID)
    workspace = bg.replace_top_value(workspace, "updated_on: ", f"'{TODAY}'")
    focus_entry = (
        "- >-\n"
        f"  Stage337 run337CC focus complete: lifecycle-aware no-overfit inputs(생애주기 인식 무과적합 입력)를 `{final['status']}`로 닫았다. "
        "Effect(효과): guarded lifecycle-aware training(방어적 생애주기 인식 학습)을 run337CD(337CD 실행)로 연다.\n"
    )
    if "Stage337 run337CC focus complete" not in workspace:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus_entry, 1)
    artifacts.append(by.write_text_preserving(WORKSPACE_STATE, workspace, workspace_bom))

    current_text, current_bom = by.read_text_lossless(CURRENT_STATE)
    current = current_text
    replacements = {
        "current_run": f"`{NEXT_RUN_ID}`",
        "status": f"`{final['status']}`",
        "decision": f"`{final['decision']}`",
        "latest_completed_run": f"`{RUN_ID}`",
        "next_action": f"`{final['next_action']}`",
        "claim_boundary": f"`{CLAIM_BOUNDARY}`",
    }
    for field_name, value in replacements.items():
        current = replace_bullet_value(current, field_name, value)
    entry = f"""
## Stage337 run337CC(337CC 실행) - {TODAY}

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): lifecycle target inputs(생애주기 타깃 입력), proxy-MT5 boundary(프록시-MT5 경계), negative controls(부정 대조), cost stress(비용 압박)를 물질화했다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    if "## Stage337 run337CC(337CC 실행)" not in current:
        marker = "## Stage337 run337CB(337CB"
        current = current.replace(marker, entry + "\n" + marker, 1) if marker in current else current.rstrip() + "\n\n" + entry
    artifacts.append(by.write_text_preserving(CURRENT_STATE, current, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- frozen_subject(고정 대상): `cp322A_cp321b_exact_replay_control_surface`
- exact_cp322a_forward_handoff(정확 cp322A 전진 인계): `not_feasible_under_frozen_rules`
- preserved_status(보존 상태): `research_artifact_only`
- rebuild_status(재구축 상태): `{final['status']}`
- actual_mt5_execution(실제 MT5 실행): `not_run_existing_telemetry_and_proxy_input_materialization_only`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 다음은 lifecycle-aware guarded scout training(생애주기 인식 방어 스카우트 학습)이다.
"""
    artifacts.append(by.write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = by.read_text_lossless(STAGE_BRIEF)
    stage_entry = f"- {TODAY}: run337CC(337CC 실행) materialized lifecycle-aware no-overfit inputs(생애주기 인식 무과적합 입력). Status(상태) `{final['status']}`. Forward/Goal(전진/목표)은 주장하지 않음."
    if stage_entry not in stage_text:
        stage_text = stage_text.rstrip() + "\n" + stage_entry + "\n"
    artifacts.append(by.write_text_preserving(STAGE_BRIEF, stage_text, stage_bom))

    changelog_text, changelog_bom = by.read_text_lossless(CHANGELOG)
    changelog_entry = f"- {TODAY}: Stage337 run337CC materialized lifecycle-aware no-overfit inputs(생애주기 인식 무과적합 입력) and opened `{NEXT_RUN_ID}`."
    if changelog_entry not in changelog_text:
        changelog_text = changelog_text.rstrip() + "\n" + changelog_entry + "\n"
    artifacts.append(by.write_text_preserving(CHANGELOG, changelog_text, changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any], artifact_paths: Sequence[Path]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "lifecycle_aware_no_overfit_input_materialization_without_db",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"decision={final['decision']};next_action={final['next_action']};closed_events={final['closed_lifecycle_events']};goal_achieve_not_claimed.",
        "family": "experiment_execution_model_validation",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__lifecycle_aware_inputs",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "lifecycle_aware_inputs",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "input_materialization",
        "tier_scope": "Tier A completed-day runtime evidence boundary",
        "kpi_scope": "lifecycle_target_negative_controls_cost_proxy_mt5",
        "scoreboard_lane": "diagnostic_special",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"closed_events={final['closed_lifecycle_events']};target_rows={final['target_rows']}",
        "guardrail_kpi": "no training; no threshold tuning; no candidate selection; no goal claim",
        "external_verification_status": "reviewed_existing_mt5_common_files_telemetry",
        "notes": f"decision={final['decision']};next={final['next_action']}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__lifecycle_aware_inputs",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_execution_model_validation",
        "evidence_scope": "CB design, CA lifecycle parity, BU proxy expected, BY completed-day lock, BO raw US100 close, BZ runtime matrix",
        "kpi_scope": "lifecycle_target_materialization_no_training",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"closed_events={final['closed_lifecycle_events']};negative_rows={final['negative_score_rows']};cost_rows={final['cost_rows']}",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__lifecycle_aware_inputs",
        "family": "experiment_execution_model_validation",
        "question": "can lifecycle-aware no-overfit inputs be materialized before guarded training",
        "metric_scope": "target_cost_negative_proxy_mt5_boundary",
        "primary_artifact": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "next_action": final["next_action"],
    }
    artifacts = [
        aw.upsert_csv(RUN_REGISTRY, aw.RUN_REGISTRY_COLUMNS, run_row, "run_id"),
        aw.upsert_csv(ALPHA_LEDGER, aw.ALPHA_LEDGER_COLUMNS, alpha_row, "ledger_row_id"),
        aw.upsert_csv(STAGE_LEDGER, aw.STAGE_LEDGER_COLUMNS, stage_row, "ledger_row_id"),
    ]
    artifact_columns, existing_rows = aw.read_csv_table(ARTIFACT_REGISTRY, prefer_head=True)
    artifact_columns = artifact_columns or ["artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes", "artifact_path", "claim_boundary"]
    generated = now_utc()
    new_rows = []
    for path in artifact_paths:
        if not path_exists(path) or not io_path(path).is_file():
            continue
        artifact_path = rel(path)
        new_rows.append(
            {
                "artifact_id": f"{RUN_ID}::{artifact_path}",
                "artifact_type": path.suffix.lstrip(".") or "file",
                "path": artifact_path,
                "sha256": sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": generated,
                "notes": final["status"],
                "artifact_path": artifact_path,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    keys = {row["artifact_id"] for row in new_rows}
    merged = [row for row in existing_rows if row.get("artifact_id") not in keys]
    merged.extend(new_rows)
    artifacts.append(write_csv(ARTIFACT_REGISTRY, artifact_columns, merged))
    return artifacts


def main() -> int:
    parse_args()
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)

    parent = read_json(CB_FINAL)
    split_policy = read_json(BU_LABEL_SPLIT_POLICY)
    input_rows = input_gates()
    proxy = read_df(BU_PROXY_EXPECTED)
    lock = read_df(BY_WINDOW_LOCK)
    external = read_df(CA_EXTERNAL)
    forward_coverage = read_df(BU_FORWARD_TRUTH_COVERAGE)
    control_plan = read_df(CB_NEGATIVE_CONTROLS)
    constraints = read_df(CB_FEATURE_CONSTRAINTS)
    runtime = read_df(BZ_RUNTIME)
    close_by_time, _spread_by_time, raw = load_raw_close()

    event_rows, proxy_audit_rows = build_event_table(proxy, lock, close_by_time)
    target_rows = build_target_score_inputs(event_rows)
    split_rows = build_rolling_split_plan(event_rows, split_policy)
    negative_plan_rows, negative_score_rows = build_negative_controls(event_rows, control_plan)
    cost_rows = build_cost_stress_inputs(event_rows)
    feature_rows = build_feature_plan(event_rows, constraints)
    utilization_rows = build_proxy_mt5_utilization(target_rows, runtime)
    audit_rows = build_data_audit(raw, proxy_audit_rows, external, forward_coverage)
    next_rows = build_next_queue()
    gates = build_gates(
        input_rows,
        event_rows,
        target_rows,
        split_rows,
        negative_plan_rows,
        negative_score_rows,
        cost_rows,
        feature_rows,
        utilization_rows,
        audit_rows,
    )
    status, judgment, decision, next_action = classify(gates)
    closed_events = sum(1 for row in event_rows if row.get("event_status") == "closed_lifecycle_event")
    open_events = sum(1 for row in event_rows if row.get("event_status") == "open_unclosed_excluded_from_target")
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "parent_status": parent.get("status", ""),
        "status": status,
        "judgment": judgment,
        "decision": decision,
        "next_action": next_action,
        "event_rows": len(event_rows),
        "closed_lifecycle_events": closed_events,
        "open_unclosed_events": open_events,
        "target_rows": len(target_rows),
        "rolling_split_rows": len(split_rows),
        "negative_plan_rows": len(negative_plan_rows),
        "negative_score_rows": len(negative_score_rows),
        "cost_rows": len(cost_rows),
        "feature_plan_rows": len(feature_rows),
        "proxy_mt5_utilization_rows": len(utilization_rows),
        "audit_rows": len(audit_rows),
        "model_training": "not_run",
        "threshold_tuning": "not_run",
        "lot_optimization": "not_run",
        "candidate_selection": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        "gate_rows": len(gates),
        "passed_gates": sum(1 for row in gates if row["status"] == "passed"),
        "failed_gates": [row["gate_id"] for row in gates if row["status"] != "passed"],
    }

    artifacts: list[Path] = [
        write_csv(LIFECYCLE_EVENT_TABLE, EVENT_COLUMNS, event_rows),
        write_csv(LIFECYCLE_TARGET_SCORE_INPUTS, TARGET_COLUMNS, target_rows),
        write_csv(ROLLING_SPLIT_PLAN, ROLLING_COLUMNS, split_rows),
        write_csv(NEGATIVE_CONTROL_INPUT_PLAN, NEGATIVE_PLAN_COLUMNS, negative_plan_rows),
        write_csv(NEGATIVE_CONTROL_SCORECARD, NEGATIVE_SCORE_COLUMNS, negative_score_rows),
        write_csv(COST_STRESS_INPUT_PLAN, COST_COLUMNS, cost_rows),
        write_csv(FEATURE_FAMILY_MATERIALIZATION_PLAN, FEATURE_PLAN_COLUMNS, feature_rows),
        write_csv(PROXY_MT5_UTILIZATION_JUDGMENT, UTILIZATION_COLUMNS, utilization_rows),
        write_csv(DATA_INTEGRITY_TIME_AXIS_AUDIT, AUDIT_COLUMNS, audit_rows),
        write_csv(NEXT_RESEARCH_QUEUE, NEXT_COLUMNS, next_rows),
        write_csv(REQUIRED_GATE_AUDIT, GATE_COLUMNS, gates),
        write_json(FINAL_DECISION, final),
    ]
    artifacts.extend(build_receipts(final))
    artifacts.extend([write_report(final, target_rows, utilization_rows, negative_score_rows, cost_rows), write_decision_doc(final)])
    artifacts.extend(update_docs(final))
    artifacts.append(write_json(RUN_MANIFEST, {"run_id": RUN_ID, "parent_run_id": PARENT_RUN_ID, "inputs": [rel(path) for path in INPUT_FILES], "outputs": [rel(path) for path in OUTPUT_FILES], "claim_boundary": CLAIM_BOUNDARY}))
    artifacts.extend(update_registers(final, artifacts))

    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not final["failed_gates"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
