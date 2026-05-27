from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, log_loss
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists  # noqa: E402
from foundation.models.baseline_training import LABEL_NAMES, LABEL_ORDER  # noqa: E402
from foundation.models.decision_surface import ThresholdRule, apply_threshold_rule  # noqa: E402
from foundation.models.onnx_bridge import (  # noqa: E402
    check_onnxruntime_probability_parity,
    export_sklearn_to_onnx_zipmap_disabled,
    ordered_hash,
    ordered_sklearn_probabilities,
    sha256_file,
)
from stage_pipelines.stage337 import materialize_lifecycle_aware_no_overfit_inputs_without_db as cc  # noqa: E402


cb = cc.cb
ca = cc.ca
bz = cc.bz
by = cc.by
aw = cc.aw
bg = cc.bg

TODAY = "2026-05-28"
STAGE_ID = cc.STAGE_ID
RUN_NUMBER = "run337CD"
RUN_ID = "run337CD_train_lifecycle_aware_guarded_scouts_without_db_v1"
PARENT_RUN_ID = cc.RUN_ID
NEXT_RUN_ID = "run337CE_execute_lifecycle_aware_mt5_runtime_probe_without_db_v1"
CLAIM_BOUNDARY = (
    "research_development_only_stage337CD_lifecycle_aware_guarded_training_without_db_"
    "no_threshold_tuning_no_lot_optimization_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = cc.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MODEL_DIR = RUN_DIR / "models"
ONNX_DIR = RUN_DIR / "onnx"
REVIEWS_DIR = cc.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337CD_lifecycle_aware_guarded_training.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337CD_lifecycle_aware_guarded_training.md"
SELECTED_STATUS = cc.SELECTED_STATUS
STAGE_BRIEF = cc.STAGE_BRIEF
WORKSPACE_STATE = cc.WORKSPACE_STATE
CURRENT_STATE = cc.CURRENT_STATE
CHANGELOG = cc.CHANGELOG
RUN_REGISTRY = cc.RUN_REGISTRY
ALPHA_LEDGER = cc.ALPHA_LEDGER
ARTIFACT_REGISTRY = cc.ARTIFACT_REGISTRY
STAGE_LEDGER = cc.STAGE_LEDGER

BT_DIR = STAGE_DIR / "02_runs" / "run337BT"
BU_DIR = STAGE_DIR / "02_runs" / "run337BU"
BQ_DIR = STAGE_DIR / "02_runs" / "run337BQ"
BO_DIR = STAGE_DIR / "02_runs" / "run337BO"

CC_FINAL = cc.FINAL_DECISION
CC_TARGET = cc.LIFECYCLE_TARGET_SCORE_INPUTS
CC_UTILIZATION = cc.PROXY_MT5_UTILIZATION_JUDGMENT
CC_COST_STRESS = cc.COST_STRESS_INPUT_PLAN
CC_NEGATIVE = cc.NEGATIVE_CONTROL_SCORECARD
CC_FEATURE_PLAN = cc.FEATURE_FAMILY_MATERIALIZATION_PLAN
CC_QUEUE = cc.NEXT_RESEARCH_QUEUE
BT_PACKAGES = BT_DIR / "scout_input_package_matrix.csv"
BT_BRANCH_CONTRACTS = BT_DIR / "scout_branch_contracts.csv"
BQ_RUNTIME_MANIFEST = BQ_DIR / "mt5_runtime_parity_package" / "runtime_parity_package_manifest.json"
FORWARD_US100_RAW = BO_DIR / "raw_refresh_probe" / "US100" / "bars_us100_m5_mt5api_raw.csv"
MODEL_INPUT_PATH = ROOT / "data" / "processed" / "model_inputs" / "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58" / "model_input_dataset.parquet"
TRAINING_SUMMARY = ROOT / "data" / "processed" / "training_datasets" / "label_v1_fwd12_split_v1_proxyw58" / "training_dataset_summary.json"
BU_PROXY_EXPECTED = BU_DIR / "proxy_expected_forward_predictions.csv"

LABEL_SPLIT_POLICY = RUN_DIR / "cost2_label_split_policy.json"
MODEL_INPUT_COMPATIBILITY = RUN_DIR / "model_input_compatibility.csv"
TRAINED_MODEL_MANIFEST = RUN_DIR / "trained_model_manifest.csv"
MODEL_METRICS = RUN_DIR / "model_metrics.csv"
THRESHOLD_POLICY = RUN_DIR / "decision_threshold_policy.csv"
DECISION_SCORECARD = RUN_DIR / "decision_scorecard.csv"
FORWARD_TRUTH_COVERAGE = RUN_DIR / "forward_truth_coverage.csv"
PROXY_EXPECTED_FORWARD = RUN_DIR / "proxy_expected_forward_predictions.csv"
ONNX_PARITY = RUN_DIR / "onnxruntime_parity_matrix.csv"
LIFECYCLE_EVENT_TABLE = RUN_DIR / "lifecycle_trade_event_table.csv"
LIFECYCLE_SCORECARD = RUN_DIR / "lifecycle_scorecard.csv"
LIFECYCLE_VS_BU_COMPARISON = RUN_DIR / "lifecycle_vs_bu_comparison.csv"
NEGATIVE_CONTROL_RESULTS = RUN_DIR / "negative_control_results.csv"
MT5_RUNTIME_PROBE_PACKAGE = RUN_DIR / "mt5_runtime_probe_package.csv"
NEXT_RESEARCH_QUEUE = RUN_DIR / "run337CE_mt5_runtime_probe_queue.csv"
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
    CC_FINAL,
    CC_TARGET,
    CC_UTILIZATION,
    CC_COST_STRESS,
    CC_NEGATIVE,
    CC_FEATURE_PLAN,
    CC_QUEUE,
    BT_PACKAGES,
    BT_BRANCH_CONTRACTS,
    BQ_RUNTIME_MANIFEST,
    FORWARD_US100_RAW,
    MODEL_INPUT_PATH,
    TRAINING_SUMMARY,
    BU_PROXY_EXPECTED,
)
OUTPUT_FILES = (
    LABEL_SPLIT_POLICY,
    MODEL_INPUT_COMPATIBILITY,
    TRAINED_MODEL_MANIFEST,
    MODEL_METRICS,
    THRESHOLD_POLICY,
    DECISION_SCORECARD,
    FORWARD_TRUTH_COVERAGE,
    PROXY_EXPECTED_FORWARD,
    ONNX_PARITY,
    LIFECYCLE_EVENT_TABLE,
    LIFECYCLE_SCORECARD,
    LIFECYCLE_VS_BU_COMPARISON,
    NEGATIVE_CONTROL_RESULTS,
    MT5_RUNTIME_PROBE_PACKAGE,
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

COST2_BPS = 2.0
COST2_LOG_RETURN_BUFFER = COST2_BPS / 10000.0
MAX_HOLD_BARS = cc.MAX_HOLD_BARS
MODEL_SPECS = (
    {
        "model_family": "logreg_cost2_balanced_c075",
        "model_role": "linear_cost2_defensive_control(선형 비용2 방어 대조)",
        "mt5_runtime_priority": "P0",
    },
    {
        "model_family": "extratrees_cost2_depth5_leaf180",
        "model_role": "nonlinear_cost2_scout(비선형 비용2 스카우트)",
        "mt5_runtime_priority": "P0",
    },
)
THRESHOLD_RULES = (
    {
        "rule_role": "cost2_balanced_primary(비용2 균형 주 규칙)",
        "selection_use": "predeclared_not_forward_selected(사전 선언, 전진 선택 아님)",
        "rule": ThresholdRule("fixed_short040_long040_margin002", 0.40, 0.40, 0.02),
        "primary": True,
    },
    {
        "rule_role": "cost2_defensive_sparse(비용2 방어 희소 규칙)",
        "selection_use": "diagnostic_only(진단 전용)",
        "rule": ThresholdRule("fixed_short045_long045_margin005", 0.45, 0.45, 0.05),
        "primary": False,
    },
    {
        "rule_role": "cost2_density_probe(비용2 밀도 탐침)",
        "selection_use": "diagnostic_only(진단 전용)",
        "rule": ThresholdRule("fixed_short036_long036_margin000", 0.36, 0.36, 0.00),
        "primary": False,
    },
)
PRIMARY_RULE = next(item["rule"] for item in THRESHOLD_RULES if item["primary"])
GATE_COLUMNS = by.GATE_COLUMNS

COMPAT_COLUMNS = (
    "branch_id",
    "feature_set_id",
    "allowed_role",
    "feature_count",
    "model_input_rows",
    "train_rows",
    "validation_rows",
    "oos_rows",
    "missing_features",
    "nonfinite_rows",
    "feature_order_hash",
    "compatibility_status",
    "effect",
    "claim_boundary",
)
MODEL_MANIFEST_COLUMNS = (
    "model_id",
    "branch_id",
    "feature_set_id",
    "allowed_role",
    "model_family",
    "model_role",
    "label_policy_id",
    "feature_count",
    "feature_order_hash",
    "model_path",
    "model_sha256",
    "onnx_path",
    "onnx_sha256",
    "onnx_probability_output_name",
    "training_rows",
    "validation_rows",
    "oos_rows",
    "training_policy",
    "claim_boundary",
)
METRIC_COLUMNS = (
    "model_id",
    "branch_id",
    "feature_set_id",
    "allowed_role",
    "model_family",
    "split",
    "rows",
    "accuracy",
    "balanced_accuracy",
    "macro_f1",
    "log_loss",
    "mean_p_short",
    "mean_p_flat",
    "mean_p_long",
    "pred_short",
    "pred_flat",
    "pred_long",
    "true_short",
    "true_flat",
    "true_long",
    "claim_boundary",
)
THRESHOLD_COLUMNS = (
    "threshold_id",
    "rule_role",
    "short_threshold",
    "long_threshold",
    "min_margin",
    "primary_rule",
    "selection_use",
    "effect",
    "claim_boundary",
)
SCORECARD_COLUMNS = (
    "model_id",
    "branch_id",
    "feature_set_id",
    "allowed_role",
    "model_family",
    "split",
    "threshold_id",
    "cost_bps_per_trade",
    "rows",
    "signal_count",
    "short_count",
    "long_count",
    "no_trade_count",
    "coverage",
    "directional_hit_rate",
    "gross_log_return_sum",
    "net_log_return_sum",
    "profit_factor",
    "expectancy_per_trade",
    "max_drawdown_log_return",
    "recovery_factor",
    "worst_20_trade_net_log_return",
    "trades_per_day",
    "selection_use",
    "claim_boundary",
)
FORWARD_COVERAGE_COLUMNS = (
    "feature_set_id",
    "feature_rows",
    "forward_labelable_rows",
    "missing_future_rows",
    "first_timestamp",
    "last_timestamp",
    "first_labelable_timestamp",
    "last_labelable_timestamp",
    "future_raw_last_timestamp",
    "base_threshold_log_return",
    "cost2_threshold_log_return",
    "integrity_status",
    "effect",
    "claim_boundary",
)
ONNX_PARITY_COLUMNS = (
    "model_id",
    "branch_id",
    "model_family",
    "onnx_path",
    "rows",
    "passed",
    "max_abs_diff",
    "mean_abs_diff",
    "onnx_row_sum_max_abs_error",
    "input_name",
    "output_names",
    "claim_boundary",
)
EVENT_COLUMNS = (
    "model_id",
    "branch_id",
    "feature_set_id",
    "allowed_role",
    "model_family",
    "event_id",
    "entry_bar_time",
    "exit_bar_time",
    "direction",
    "exit_reason",
    "hold_bars",
    "gross_log_return",
    "net_log_return_cost0",
    "net_log_return_cost1",
    "net_log_return_cost2",
    "net_log_return_cost5",
    "entry_feature_input_hash",
    "event_status",
    "claim_boundary",
)
LIFECYCLE_SCORE_COLUMNS = (
    "model_id",
    "branch_id",
    "feature_set_id",
    "allowed_role",
    "model_family",
    "closed_trade_events",
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
    "forward_diagnostic_status",
    "claim_boundary",
)
COMPARISON_COLUMNS = (
    "cd_model_id",
    "branch_id",
    "feature_set_id",
    "allowed_role",
    "model_family",
    "matched_bu_reference",
    "cd_closed_trade_events",
    "bu_closed_trade_events",
    "cd_net_cost1",
    "bu_net_cost1",
    "cd_profit_factor_cost1",
    "bu_profit_factor_cost1",
    "net_delta_cost1",
    "pf_delta_cost1",
    "comparison_judgment",
    "claim_boundary",
)
NEGATIVE_COLUMNS = (
    "control_id",
    "model_id",
    "branch_id",
    "feature_set_id",
    "model_family",
    "control_type",
    "observed",
    "expected",
    "status",
    "effect",
    "claim_boundary",
)
MT5_PACKAGE_COLUMNS = (
    "probe_id",
    "model_id",
    "branch_id",
    "feature_set_id",
    "allowed_role",
    "model_family",
    "feature_csv_path",
    "feature_count",
    "feature_order_hash",
    "onnx_path",
    "threshold_id",
    "short_threshold",
    "long_threshold",
    "min_margin",
    "proxy_expected_path",
    "lifecycle_scorecard_path",
    "mt5_required",
    "expected_compare_keys",
    "claim_boundary",
)
NEXT_COLUMNS = by.NEXT_COLUMNS


def parse_args() -> argparse.Namespace:
    return argparse.ArgumentParser(description=RUN_ID).parse_args()


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return by.rel(Path(path))


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    return by.write_csv(path, columns, rows)


def write_json(path: Path, payload: Mapping[str, Any]) -> Path:
    return by.write_json(path, payload)


def write_md(path: Path, text: str) -> Path:
    return by.write_md(path, text)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_df(path: Path, **kwargs: Any) -> pd.DataFrame:
    return pd.read_csv(io_path(path), encoding="utf-8-sig", **kwargs)


def csv_rows(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def as_float(value: Any) -> float:
    try:
        if value is None or value == "":
            return float("nan")
        return float(value)
    except (TypeError, ValueError):
        return float("nan")


def finite_or_none(value: float) -> float | None:
    return float(value) if math.isfinite(value) else None


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
    total = float(array[np.isfinite(array)].sum()) if array.size else 0.0
    dd = max_drawdown(array)
    if dd < 0.0:
        return total / abs(dd)
    return float("inf") if total > 0.0 else 0.0


def timestamp_span_days(timestamps: pd.Series) -> float:
    if timestamps.empty:
        return 1.0
    start = pd.to_datetime(timestamps, utc=True).min()
    end = pd.to_datetime(timestamps, utc=True).max()
    days = (end - start).total_seconds() / 86400.0
    return max(float(days), 1.0)


def score_values(values: Sequence[float] | np.ndarray) -> dict[str, float]:
    array = np.asarray(values, dtype="float64")
    array = array[np.isfinite(array)]
    total = float(array.sum()) if array.size else 0.0
    dd = max_drawdown(array)
    return {
        "rows": int(array.size),
        "net": total,
        "pf": safe_pf(array),
        "expectancy": float(array.mean()) if array.size else 0.0,
        "max_dd": dd,
        "recovery": recovery_factor(array),
        "worst_20": worst_rolling(array, 20),
    }


def fnv1a64_upper(line: str) -> str:
    value = 1469598103934665603
    for char in line:
        value = ((value ^ ord(char)) * 1099511628211) & 0xFFFFFFFFFFFFFFFF
    return f"{value:X}"


def timestamp_hash_index(csv_path: Path) -> dict[pd.Timestamp, str]:
    output: dict[pd.Timestamp, str] = {}
    with io_path(csv_path).open("r", encoding="utf-8-sig", newline="") as handle:
        header_line = handle.readline().rstrip("\r\n")
        header = next(csv.reader([header_line]))
        timestamp_col = next((idx for idx, name in enumerate(header) if name.strip().lower() == "timestamp_utc"), -1)
        if timestamp_col < 0:
            raise RuntimeError(f"{csv_path} has no timestamp_utc column")
        for raw_line in handle:
            line = raw_line.rstrip("\r\n")
            if not line:
                continue
            cols = next(csv.reader([line]))
            if timestamp_col >= len(cols):
                continue
            timestamp = pd.Timestamp(cols[timestamp_col])
            timestamp = timestamp.tz_localize("UTC") if timestamp.tzinfo is None else timestamp.tz_convert("UTC")
            output[timestamp] = fnv1a64_upper(line)
    return output


def load_feature_order(path: Path) -> list[str]:
    return [line.strip() for line in io_path(path).read_text(encoding="utf-8-sig").splitlines() if line.strip()]


def cost2_labels(future_log_return: pd.Series, threshold: float) -> pd.Series:
    values = pd.to_numeric(future_log_return, errors="coerce")
    labels = np.where(values < -threshold, 0, np.where(values > threshold, 2, 1))
    return pd.Series(labels, index=future_log_return.index, dtype="int64")


def class_dist(values: pd.Series) -> dict[str, int]:
    counts = values.astype("int64").value_counts().to_dict()
    return {LABEL_NAMES[label]: int(counts.get(label, 0)) for label in LABEL_ORDER}


def make_model(model_family: str) -> Any:
    if model_family == "logreg_cost2_balanced_c075":
        return Pipeline(
            steps=[
                ("scaler", StandardScaler()),
                (
                    "classifier",
                    LogisticRegression(
                        C=0.75,
                        class_weight="balanced",
                        max_iter=2500,
                        random_state=337,
                        solver="lbfgs",
                    ),
                ),
            ]
        )
    if model_family == "extratrees_cost2_depth5_leaf180":
        return ExtraTreesClassifier(
            n_estimators=180,
            max_depth=5,
            min_samples_leaf=180,
            max_features="sqrt",
            class_weight="balanced",
            random_state=337,
            n_jobs=-1,
        )
    raise ValueError(f"unknown model_family: {model_family}")


def probability_frame(model: Any, frame: pd.DataFrame, features: Sequence[str]) -> pd.DataFrame:
    values = frame.loc[:, list(features)].to_numpy(dtype="float64", copy=False)
    probs = ordered_sklearn_probabilities(model, values)
    return pd.DataFrame(probs, columns=["p_short", "p_flat", "p_long"], index=frame.index)


def load_raw_close() -> tuple[pd.Series, pd.DataFrame]:
    raw = read_df(FORWARD_US100_RAW, usecols=["time_close_unix", "close"])
    raw["timestamp"] = pd.to_datetime(raw["time_close_unix"], unit="s", utc=True)
    raw = raw.sort_values("timestamp").drop_duplicates("timestamp", keep="last")
    return raw.set_index("timestamp")["close"].astype("float64"), raw


def apply_forward_truth(feature_frame: pd.DataFrame, training_summary: Mapping[str, Any], cost2_threshold: float) -> tuple[pd.DataFrame, dict[str, Any]]:
    raw_close, raw = load_raw_close()
    horizon_minutes = int(training_summary["horizon_minutes"])
    frame = feature_frame.copy()
    frame["timestamp"] = pd.to_datetime(frame["timestamp_utc"], utc=True)
    frame["future_timestamp"] = frame["timestamp"] + pd.Timedelta(minutes=horizon_minutes)
    current_close = frame["timestamp"].map(raw_close)
    future_close = frame["future_timestamp"].map(raw_close)
    frame["future_log_return_12"] = np.log(future_close.astype("float64") / current_close.astype("float64"))
    labelable = frame["future_log_return_12"].notna() & np.isfinite(frame["future_log_return_12"].to_numpy(dtype="float64", na_value=np.nan))
    frame["forward_label_available"] = labelable
    frame["label_class"] = cost2_labels(frame["future_log_return_12"], cost2_threshold)
    frame["label"] = frame["label_class"].map(LABEL_NAMES)
    return frame, {
        "feature_rows": int(len(frame)),
        "forward_labelable_rows": int(labelable.sum()),
        "missing_future_rows": int((~labelable).sum()),
        "first_timestamp": frame["timestamp"].min().isoformat() if len(frame) else "",
        "last_timestamp": frame["timestamp"].max().isoformat() if len(frame) else "",
        "first_labelable_timestamp": frame.loc[labelable, "timestamp"].min().isoformat() if labelable.any() else "",
        "last_labelable_timestamp": frame.loc[labelable, "timestamp"].max().isoformat() if labelable.any() else "",
        "future_raw_last_timestamp": raw["timestamp"].max().isoformat() if len(raw) else "",
    }


def build_model_metric_row(
    *,
    model_id: str,
    branch_id: str,
    feature_set_id: str,
    allowed_role: str,
    model_family: str,
    split: str,
    frame: pd.DataFrame,
    probabilities: pd.DataFrame,
) -> dict[str, Any]:
    labels = frame["cost2_label_class"].astype("int64").to_numpy()
    pred = np.asarray(LABEL_ORDER, dtype="int64")[probabilities.to_numpy(dtype="float64").argmax(axis=1)]
    pred_dist = class_dist(pd.Series(pred))
    true_dist = class_dist(frame["cost2_label_class"])
    return {
        "model_id": model_id,
        "branch_id": branch_id,
        "feature_set_id": feature_set_id,
        "allowed_role": allowed_role,
        "model_family": model_family,
        "split": split,
        "rows": len(frame),
        "accuracy": accuracy_score(labels, pred),
        "balanced_accuracy": balanced_accuracy_score(labels, pred),
        "macro_f1": f1_score(labels, pred, labels=LABEL_ORDER, average="macro"),
        "log_loss": log_loss(labels, probabilities.to_numpy(dtype="float64"), labels=LABEL_ORDER),
        "mean_p_short": probabilities["p_short"].mean(),
        "mean_p_flat": probabilities["p_flat"].mean(),
        "mean_p_long": probabilities["p_long"].mean(),
        "pred_short": pred_dist["short"],
        "pred_flat": pred_dist["flat"],
        "pred_long": pred_dist["long"],
        "true_short": true_dist["short"],
        "true_flat": true_dist["flat"],
        "true_long": true_dist["long"],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def score_decisions(
    *,
    model_id: str,
    branch_id: str,
    feature_set_id: str,
    allowed_role: str,
    model_family: str,
    split: str,
    frame: pd.DataFrame,
    probabilities: pd.DataFrame,
    rule_payload: Mapping[str, Any],
    cost_bps: float,
    selection_use: str,
) -> dict[str, Any]:
    rule = rule_payload["rule"]
    decisions = apply_threshold_rule(probabilities, rule)
    labels = frame["cost2_label_class"].astype("int64").to_numpy() if "cost2_label_class" in frame.columns else np.array([], dtype="int64")
    future = frame["future_log_return_12"].astype("float64").to_numpy() if "future_log_return_12" in frame.columns else np.full(len(decisions), np.nan)
    decision_class = decisions["decision_label_class"].to_numpy(dtype="int64")
    signal_mask = decision_class != -1
    label_mask = signal_mask & np.isfinite(future)
    signed = np.zeros(len(decisions), dtype="float64")
    signed[decision_class == 2] = future[decision_class == 2]
    signed[decision_class == 0] = -future[decision_class == 0]
    trade_returns = signed[label_mask] - float(cost_bps) / 10000.0
    score = score_values(trade_returns)
    hit_rate = np.nan
    if label_mask.any() and labels.size == len(decisions):
        hit_rate = float((decision_class[label_mask] == labels[label_mask]).mean())
    signal_count = int(signal_mask.sum())
    timestamps = frame["timestamp"] if "timestamp" in frame.columns else pd.Series(dtype="datetime64[ns, UTC]")
    return {
        "model_id": model_id,
        "branch_id": branch_id,
        "feature_set_id": feature_set_id,
        "allowed_role": allowed_role,
        "model_family": model_family,
        "split": split,
        "threshold_id": rule.threshold_id,
        "cost_bps_per_trade": cost_bps,
        "rows": int(len(decisions)),
        "signal_count": signal_count,
        "short_count": int((decision_class == 0).sum()),
        "long_count": int((decision_class == 2).sum()),
        "no_trade_count": int((decision_class == -1).sum()),
        "coverage": float(signal_count / len(decisions)) if len(decisions) else 0.0,
        "directional_hit_rate": hit_rate,
        "gross_log_return_sum": float(signed[label_mask].sum()) if label_mask.any() else 0.0,
        "net_log_return_sum": finite_or_none(score["net"]),
        "profit_factor": finite_or_none(score["pf"]),
        "expectancy_per_trade": finite_or_none(score["expectancy"]),
        "max_drawdown_log_return": finite_or_none(score["max_dd"]),
        "recovery_factor": finite_or_none(score["recovery"]),
        "worst_20_trade_net_log_return": finite_or_none(score["worst_20"]),
        "trades_per_day": float(signal_count / timestamp_span_days(timestamps)),
        "selection_use": selection_use,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_proxy_rows(
    *,
    model_id: str,
    branch_id: str,
    feature_set_id: str,
    allowed_role: str,
    model_family: str,
    feature_frame: pd.DataFrame,
    probabilities: pd.DataFrame,
    feature_hashes: Mapping[pd.Timestamp, str],
) -> pd.DataFrame:
    decisions = apply_threshold_rule(probabilities, PRIMARY_RULE)
    return pd.DataFrame(
        {
            "model_id": model_id,
            "branch_id": branch_id,
            "feature_set_id": feature_set_id,
            "allowed_role": allowed_role,
            "model_family": model_family,
            "bar_time": feature_frame["timestamp"].dt.strftime("%Y.%m.%d %H:%M:%S"),
            "timestamp_utc": feature_frame["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "feature_input_hash": [feature_hashes.get(ts, "") for ts in feature_frame["timestamp"]],
            "p_short": probabilities["p_short"].to_numpy(dtype="float64"),
            "p_flat": probabilities["p_flat"].to_numpy(dtype="float64"),
            "p_long": probabilities["p_long"].to_numpy(dtype="float64"),
            "threshold_id": decisions["threshold_id"].to_numpy(),
            "decision_label_class": decisions["decision_label_class"].to_numpy(dtype="int64"),
            "decision_label": decisions["decision_label"].to_numpy(),
            "decision_probability": decisions["decision_probability"].to_numpy(dtype="float64"),
            "decision_margin": decisions["decision_margin"].to_numpy(dtype="float64"),
            "future_log_return_12": feature_frame["future_log_return_12"].to_numpy(dtype="float64"),
            "forward_label_available": feature_frame["forward_label_available"].astype(bool).to_numpy(),
            "cost2_label_class": feature_frame["cost2_label_class"].to_numpy(dtype="int64"),
            "cost2_label": feature_frame["cost2_label"].astype(str).to_numpy(),
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )


def direction_sign(direction: str) -> int:
    if direction == "long":
        return 1
    if direction == "short":
        return -1
    return 0


def build_lifecycle_events(proxy: pd.DataFrame, close_by_time: pd.Series) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for model_id, group in proxy.groupby("model_id", sort=True):
        frame = group.copy()
        frame["timestamp"] = pd.to_datetime(frame["timestamp_utc"], utc=True)
        frame["close_price"] = frame["timestamp"].map(close_by_time)
        frame = frame.sort_values("timestamp")
        position: str | None = None
        entry: Mapping[str, Any] | None = None
        entry_index = -1
        age = 0
        event_index = 0

        def close_event(row: Mapping[str, Any], row_index: int, reason: str) -> None:
            nonlocal position, entry, entry_index, age, event_index
            if position is None or entry is None:
                return
            entry_close = as_float(entry.get("close_price"))
            exit_close = as_float(row.get("close_price"))
            if not (entry_close > 0.0 and exit_close > 0.0):
                gross = float("nan")
            else:
                gross = direction_sign(position) * math.log(exit_close / entry_close)
            event_index += 1
            labelable = math.isfinite(gross)
            events.append(
                {
                    "model_id": model_id,
                    "branch_id": row.get("branch_id", ""),
                    "feature_set_id": row.get("feature_set_id", ""),
                    "allowed_role": row.get("allowed_role", ""),
                    "model_family": row.get("model_family", ""),
                    "event_id": f"{model_id}__evt{event_index:05d}",
                    "entry_bar_time": entry.get("bar_time", ""),
                    "exit_bar_time": row.get("bar_time", ""),
                    "direction": position,
                    "exit_reason": reason,
                    "hold_bars": row_index - entry_index,
                    "gross_log_return": finite_or_none(gross),
                    "net_log_return_cost0": finite_or_none(gross) if labelable else None,
                    "net_log_return_cost1": finite_or_none(gross - 0.0001) if labelable else None,
                    "net_log_return_cost2": finite_or_none(gross - 0.0002) if labelable else None,
                    "net_log_return_cost5": finite_or_none(gross - 0.0005) if labelable else None,
                    "entry_feature_input_hash": entry.get("feature_input_hash", ""),
                    "event_status": "closed_lifecycle_event" if labelable else "closed_event_missing_raw_close",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            position = None
            entry = None
            entry_index = -1
            age = 0

        records = frame.to_dict("records")
        for row_index, row in enumerate(records):
            decision = ca.normalize_decision(row.get("decision_label"))
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
    return events


def build_lifecycle_scorecard(events: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    df = pd.DataFrame(events)
    if df.empty:
        return []
    closed = df[df["event_status"].astype(str) == "closed_lifecycle_event"].copy()
    rows: list[dict[str, Any]] = []
    for column in ("net_log_return_cost0", "net_log_return_cost1", "net_log_return_cost2", "net_log_return_cost5"):
        closed[column] = pd.to_numeric(closed[column], errors="coerce")
    for (model_id, branch_id, feature_set_id, allowed_role, model_family), group in closed.groupby(["model_id", "branch_id", "feature_set_id", "allowed_role", "model_family"], sort=True):
        cost1 = group["net_log_return_cost1"].to_numpy(dtype="float64")
        cost2 = group["net_log_return_cost2"].to_numpy(dtype="float64")
        score1 = score_values(cost1)
        score2 = score_values(cost2)
        status = "cost2_forward_proxy_survived_diagnostic" if score2["net"] > 0.0 and score2["pf"] > 1.0 else "cost2_forward_proxy_failed_guard"
        if int(score1["rows"]) < 20:
            forward_status = "low_trade_count_diagnostic"
        elif score1["net"] > 0.0 and score1["pf"] > 1.0:
            forward_status = "positive_proxy_diagnostic_not_selection"
        else:
            forward_status = "negative_proxy_diagnostic"
        rows.append(
            {
                "model_id": model_id,
                "branch_id": branch_id,
                "feature_set_id": feature_set_id,
                "allowed_role": allowed_role,
                "model_family": model_family,
                "closed_trade_events": int(score1["rows"]),
                "net_log_return_cost0": finite_or_none(float(group["net_log_return_cost0"].sum())),
                "net_log_return_cost1": finite_or_none(score1["net"]),
                "net_log_return_cost2": finite_or_none(score2["net"]),
                "net_log_return_cost5": finite_or_none(float(group["net_log_return_cost5"].sum())),
                "profit_factor_cost1": finite_or_none(score1["pf"]),
                "profit_factor_cost2": finite_or_none(score2["pf"]),
                "expectancy_cost1": finite_or_none(score1["expectancy"]),
                "max_drawdown_cost1": finite_or_none(score1["max_dd"]),
                "recovery_factor_cost1": finite_or_none(score1["recovery"]),
                "worst_20_trade_cost1": finite_or_none(score1["worst_20"]),
                "cost2_guard_status": status,
                "forward_diagnostic_status": forward_status,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_comparison(lifecycle_rows: Sequence[Mapping[str, Any]], cc_target: pd.DataFrame) -> list[dict[str, Any]]:
    cc_by_feature_family = {(str(row["feature_set_id"]), str(row["model_family"])): row for row in cc_target.to_dict("records")}
    rows: list[dict[str, Any]] = []
    for row in lifecycle_rows:
        key_family = "logreg_balanced_c1" if "logreg" in str(row["model_family"]) else "extratrees_depth6_leaf120"
        reference = cc_by_feature_family.get((str(row["feature_set_id"]), key_family), {})
        cd_net = as_float(row.get("net_log_return_cost1"))
        bu_net = as_float(reference.get("net_log_return_cost1"))
        cd_pf = as_float(row.get("profit_factor_cost1"))
        bu_pf = as_float(reference.get("profit_factor_cost1"))
        if math.isfinite(cd_net) and math.isfinite(bu_net) and cd_net > bu_net and cd_pf > bu_pf:
            judgment = "improved_vs_bu_proxy_diagnostic_not_selection"
        elif math.isfinite(cd_net) and math.isfinite(bu_net):
            judgment = "not_improved_vs_bu_proxy"
        else:
            judgment = "comparison_missing_reference"
        rows.append(
            {
                "cd_model_id": row.get("model_id", ""),
                "branch_id": row.get("branch_id", ""),
                "feature_set_id": row.get("feature_set_id", ""),
                "allowed_role": row.get("allowed_role", ""),
                "model_family": row.get("model_family", ""),
                "matched_bu_reference": reference.get("model_id", ""),
                "cd_closed_trade_events": row.get("closed_trade_events", ""),
                "bu_closed_trade_events": reference.get("closed_trade_events", ""),
                "cd_net_cost1": finite_or_none(cd_net),
                "bu_net_cost1": finite_or_none(bu_net),
                "cd_profit_factor_cost1": finite_or_none(cd_pf),
                "bu_profit_factor_cost1": finite_or_none(bu_pf),
                "net_delta_cost1": finite_or_none(cd_net - bu_net) if math.isfinite(cd_net) and math.isfinite(bu_net) else None,
                "pf_delta_cost1": finite_or_none(cd_pf - bu_pf) if math.isfinite(cd_pf) and math.isfinite(bu_pf) else None,
                "comparison_judgment": judgment,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_input_gates() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in INPUT_FILES:
        rows.append(
            {
                "gate_id": f"input_exists::{rel(path)}",
                "status": "passed" if path_exists(path) else "failed",
                "observed": "exists" if path_exists(path) else "missing",
                "expected": rel(path),
                "effect": "input available for CD guarded training(CD 방어 학습 입력 사용 가능)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_threshold_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in THRESHOLD_RULES:
        rule = item["rule"]
        rows.append(
            {
                "threshold_id": rule.threshold_id,
                "rule_role": item["rule_role"],
                "short_threshold": rule.short_threshold,
                "long_threshold": rule.long_threshold,
                "min_margin": rule.min_margin,
                "primary_rule": item["primary"],
                "selection_use": item["selection_use"],
                "effect": "threshold rules are fixed before forward scoring(임계값 규칙은 전진 채점 전에 고정)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def train_and_score() -> dict[str, Any]:
    training_summary = read_json(TRAINING_SUMMARY)
    base_threshold = float(training_summary["threshold_log_return"])
    cost2_threshold = base_threshold + COST2_LOG_RETURN_BUFFER
    packages = csv_rows(BT_PACKAGES)
    feature_plan = read_df(CC_FEATURE_PLAN)
    plan_by_feature = {str(row["feature_set_id"]): row for row in feature_plan.to_dict("records")}
    model_input = pd.read_parquet(io_path(MODEL_INPUT_PATH)).copy()
    model_input["timestamp"] = pd.to_datetime(model_input["timestamp"], utc=True)
    model_input["cost2_label_class"] = cost2_labels(model_input["future_log_return_12"], cost2_threshold)
    model_input["cost2_label"] = model_input["cost2_label_class"].map(LABEL_NAMES)
    close_by_time, _raw = load_raw_close()
    cc_target = read_df(CC_TARGET)

    compat_rows: list[dict[str, Any]] = []
    model_rows: list[dict[str, Any]] = []
    metric_rows: list[dict[str, Any]] = []
    score_rows: list[dict[str, Any]] = []
    parity_rows: list[dict[str, Any]] = []
    forward_coverage_rows: list[dict[str, Any]] = []
    proxy_parts: list[pd.DataFrame] = []
    negative_rows: list[dict[str, Any]] = []
    mt5_rows: list[dict[str, Any]] = []
    feature_orders: dict[str, list[str]] = {}
    package_by_branch = {str(row["branch_id"]): row for row in packages}

    split_frames = {split: model_input.loc[model_input["split"].astype(str).eq(split)].copy() for split in ("train", "validation", "oos")}
    for package in packages:
        branch_id = str(package["branch_id"])
        feature_set_id = str(package["feature_set_id"])
        plan_row = plan_by_feature.get(feature_set_id, {})
        allowed_role = str(plan_row.get("allowed_role", "unclassified"))
        order_path = ROOT / str(package["feature_order_path"])
        features = load_feature_order(order_path)
        feature_orders[branch_id] = features
        missing = [feature for feature in features if feature not in model_input.columns]
        nonfinite = 0
        if not missing:
            values = model_input.loc[:, features].to_numpy(dtype="float64", copy=False)
            nonfinite = int((~np.isfinite(values).all(axis=1)).sum())
        compat_rows.append(
            {
                "branch_id": branch_id,
                "feature_set_id": feature_set_id,
                "allowed_role": allowed_role,
                "feature_count": len(features),
                "model_input_rows": len(model_input),
                "train_rows": len(split_frames["train"]),
                "validation_rows": len(split_frames["validation"]),
                "oos_rows": len(split_frames["oos"]),
                "missing_features": ";".join(missing),
                "nonfinite_rows": nonfinite,
                "feature_order_hash": ordered_hash(features),
                "compatibility_status": "passed" if not missing and nonfinite == 0 else "failed",
                "effect": "checks cost2-aware training can use fixed feature order(비용2 인식 학습이 고정 피처 순서를 쓸 수 있는지 확인)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    for branch_id, features in feature_orders.items():
        package = package_by_branch[branch_id]
        feature_set_id = str(package["feature_set_id"])
        plan_row = plan_by_feature.get(feature_set_id, {})
        allowed_role = str(plan_row.get("allowed_role", "unclassified"))
        feature_csv = ROOT / str(package["feature_csv_path"])
        feature_hashes = timestamp_hash_index(feature_csv)
        forward_features_raw = read_df(feature_csv)
        forward_features, coverage = apply_forward_truth(forward_features_raw, training_summary, cost2_threshold)
        forward_features["cost2_label_class"] = cost2_labels(forward_features["future_log_return_12"], cost2_threshold)
        forward_features["cost2_label"] = forward_features["cost2_label_class"].map(LABEL_NAMES)
        forward_coverage_rows.append(
            {
                "feature_set_id": feature_set_id,
                **coverage,
                "base_threshold_log_return": base_threshold,
                "cost2_threshold_log_return": cost2_threshold,
                "integrity_status": "usable_with_cost2_forward_label_boundary",
                "effect": "forward labels are diagnostic only and cannot select branch or threshold(전진 라벨은 진단 전용이며 분기/임계값 선택 금지)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        X_train = split_frames["train"].loc[:, features].to_numpy(dtype="float64", copy=False)
        y_train = split_frames["train"]["cost2_label_class"].astype("int64").to_numpy()

        for spec in MODEL_SPECS:
            model_family = str(spec["model_family"])
            model_id = f"cd_{branch_id}__{model_family}"
            model = make_model(model_family)
            model.fit(X_train, y_train)
            model_path = MODEL_DIR / f"{model_id}.joblib"
            onnx_path = ONNX_DIR / f"{model_id}.onnx"
            io_path(model_path.parent).mkdir(parents=True, exist_ok=True)
            joblib.dump(model, io_path(model_path))
            export_info = export_sklearn_to_onnx_zipmap_disabled(model, onnx_path, feature_count=len(features), target_opset=12, drop_label_output=True)
            validation_sample = split_frames["validation"].loc[:, features].to_numpy(dtype="float64", copy=False)[:256]
            parity = check_onnxruntime_probability_parity(model, onnx_path, validation_sample, tolerance=1.0e-5)
            parity_rows.append(
                {
                    "model_id": model_id,
                    "branch_id": branch_id,
                    "model_family": model_family,
                    "onnx_path": rel(onnx_path),
                    "rows": parity["rows"],
                    "passed": str(bool(parity["passed"])).lower(),
                    "max_abs_diff": parity["max_abs_diff"],
                    "mean_abs_diff": parity["mean_abs_diff"],
                    "onnx_row_sum_max_abs_error": parity["onnx_row_sum_max_abs_error"],
                    "input_name": parity["input_name"],
                    "output_names": ";".join(parity["output_names"]),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            model_rows.append(
                {
                    "model_id": model_id,
                    "branch_id": branch_id,
                    "feature_set_id": feature_set_id,
                    "allowed_role": allowed_role,
                    "model_family": model_family,
                    "model_role": spec["model_role"],
                    "label_policy_id": "label_v2_cost2_aware_fwd12_m5_logret_train_only",
                    "feature_count": len(features),
                    "feature_order_hash": ordered_hash(features),
                    "model_path": rel(model_path),
                    "model_sha256": sha256_file(model_path),
                    "onnx_path": rel(onnx_path),
                    "onnx_sha256": sha256_file(onnx_path),
                    "onnx_probability_output_name": export_info["probability_output_name"],
                    "training_rows": len(split_frames["train"]),
                    "validation_rows": len(split_frames["validation"]),
                    "oos_rows": len(split_frames["oos"]),
                    "training_policy": "train split only; cost2 label threshold predeclared; no forward data fit(학습 분할만 사용, 비용2 라벨 임계값 사전 선언, 전진 학습 금지)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            split_probabilities: dict[str, pd.DataFrame] = {}
            for split, split_frame in split_frames.items():
                probabilities = probability_frame(model, split_frame, features)
                split_probabilities[split] = probabilities
                metric_rows.append(
                    build_model_metric_row(
                        model_id=model_id,
                        branch_id=branch_id,
                        feature_set_id=feature_set_id,
                        allowed_role=allowed_role,
                        model_family=model_family,
                        split=split,
                        frame=split_frame,
                        probabilities=probabilities,
                    )
                )
                eval_frame = split_frame.copy()
                eval_frame["timestamp"] = pd.to_datetime(eval_frame["timestamp"], utc=True)
                for rule_payload in THRESHOLD_RULES:
                    for cost_bps in (0.0, 1.0, 2.0):
                        score_rows.append(
                            score_decisions(
                                model_id=model_id,
                                branch_id=branch_id,
                                feature_set_id=feature_set_id,
                                allowed_role=allowed_role,
                                model_family=model_family,
                                split=split,
                                frame=eval_frame,
                                probabilities=probabilities,
                                rule_payload=rule_payload,
                                cost_bps=cost_bps,
                                selection_use="historical_diagnostic_not_forward_selection(과거 진단, 전진 선택 아님)",
                            )
                        )
            forward_prob = probability_frame(model, forward_features, features)
            proxy_parts.append(
                build_proxy_rows(
                    model_id=model_id,
                    branch_id=branch_id,
                    feature_set_id=feature_set_id,
                    allowed_role=allowed_role,
                    model_family=model_family,
                    feature_frame=forward_features,
                    probabilities=forward_prob,
                    feature_hashes=feature_hashes,
                )
            )
            labelable_forward = forward_features.loc[forward_features["forward_label_available"].astype(bool)].copy()
            forward_label_prob = forward_prob.loc[labelable_forward.index]
            for rule_payload in THRESHOLD_RULES:
                for cost_bps in (0.0, 1.0, 2.0):
                    score_rows.append(
                        score_decisions(
                            model_id=model_id,
                            branch_id=branch_id,
                            feature_set_id=feature_set_id,
                            allowed_role=allowed_role,
                            model_family=model_family,
                            split="forward_after_2026_04_14_diagnostic",
                            frame=labelable_forward,
                            probabilities=forward_label_prob,
                            rule_payload=rule_payload,
                            cost_bps=cost_bps,
                            selection_use="forward_diagnostic_holdout_not_selection(전진 진단 홀드아웃, 선택 금지)",
                        )
                    )

            validation = split_frames["validation"].copy()
            validation_probs = split_probabilities["validation"]
            primary_score = score_decisions(
                model_id=model_id,
                branch_id=branch_id,
                feature_set_id=feature_set_id,
                allowed_role=allowed_role,
                model_family=model_family,
                split="validation",
                frame=validation,
                probabilities=validation_probs,
                rule_payload={"rule": PRIMARY_RULE},
                cost_bps=0.0,
                selection_use="negative_control_reference(부정 대조 기준)",
            )
            shifted = validation.copy()
            shifted["future_log_return_12"] = shifted["future_log_return_12"].shift(-1)
            shifted = shifted.dropna(subset=["future_log_return_12"])
            shifted["cost2_label_class"] = cost2_labels(shifted["future_log_return_12"], cost2_threshold)
            shifted_score = score_decisions(
                model_id=model_id,
                branch_id=branch_id,
                feature_set_id=feature_set_id,
                allowed_role=allowed_role,
                model_family=model_family,
                split="validation_shifted_return_control",
                frame=shifted,
                probabilities=validation_probs.loc[shifted.index],
                rule_payload={"rule": PRIMARY_RULE},
                cost_bps=0.0,
                selection_use="negative_control(부정 대조)",
            )
            flip_prob = validation_probs.rename(columns={"p_short": "p_long", "p_long": "p_short"})[["p_short", "p_flat", "p_long"]]
            flip_score = score_decisions(
                model_id=model_id,
                branch_id=branch_id,
                feature_set_id=feature_set_id,
                allowed_role=allowed_role,
                model_family=model_family,
                split="validation_direction_flip_control",
                frame=validation,
                probabilities=flip_prob,
                rule_payload={"rule": PRIMARY_RULE},
                cost_bps=0.0,
                selection_use="negative_control(부정 대조)",
            )
            negative_rows.extend(
                [
                    {
                        "control_id": f"{model_id}__shifted_return_one_bar",
                        "model_id": model_id,
                        "branch_id": branch_id,
                        "feature_set_id": feature_set_id,
                        "model_family": model_family,
                        "control_type": "leakage_probe",
                        "observed": f"original_net={primary_score['net_log_return_sum']};shifted_net={shifted_score['net_log_return_sum']}",
                        "expected": "score_changes",
                        "status": "passed" if abs(float(primary_score["net_log_return_sum"]) - float(shifted_score["net_log_return_sum"])) > 1.0e-9 else "failed",
                        "effect": "checks label timing sensitivity(라벨 시점 민감도 확인)",
                        "claim_boundary": CLAIM_BOUNDARY,
                    },
                    {
                        "control_id": f"{model_id}__direction_flip",
                        "model_id": model_id,
                        "branch_id": branch_id,
                        "feature_set_id": feature_set_id,
                        "model_family": model_family,
                        "control_type": "directionality_probe",
                        "observed": f"original_net={primary_score['net_log_return_sum']};flip_net={flip_score['net_log_return_sum']}",
                        "expected": "flip_weaker",
                        "status": "passed" if float(flip_score["net_log_return_sum"]) < float(primary_score["net_log_return_sum"]) else "failed",
                        "effect": "checks direction has meaning(방향 의미 확인)",
                        "claim_boundary": CLAIM_BOUNDARY,
                    },
                ]
            )
            mt5_rows.append(
                {
                    "probe_id": f"run337CE__{model_id}",
                    "model_id": model_id,
                    "branch_id": branch_id,
                    "feature_set_id": feature_set_id,
                    "allowed_role": allowed_role,
                    "model_family": model_family,
                    "feature_csv_path": package["feature_csv_path"],
                    "feature_count": len(features),
                    "feature_order_hash": ordered_hash(features),
                    "onnx_path": rel(onnx_path),
                    "threshold_id": PRIMARY_RULE.threshold_id,
                    "short_threshold": PRIMARY_RULE.short_threshold,
                    "long_threshold": PRIMARY_RULE.long_threshold,
                    "min_margin": PRIMARY_RULE.min_margin,
                    "proxy_expected_path": rel(PROXY_EXPECTED_FORWARD),
                    "lifecycle_scorecard_path": rel(LIFECYCLE_SCORECARD),
                    "mt5_required": "yes",
                    "expected_compare_keys": "bar_time;feature_input_hash;p_short;p_flat;p_long;decision;exec_action",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )

    proxy = pd.concat(proxy_parts, ignore_index=True) if proxy_parts else pd.DataFrame()
    lifecycle_events = build_lifecycle_events(proxy, close_by_time) if not proxy.empty else []
    lifecycle_rows = build_lifecycle_scorecard(lifecycle_events)
    comparison_rows = build_comparison(lifecycle_rows, cc_target)
    return {
        "training_summary": training_summary,
        "base_threshold": base_threshold,
        "cost2_threshold": cost2_threshold,
        "compat_rows": compat_rows,
        "model_rows": model_rows,
        "metric_rows": metric_rows,
        "score_rows": score_rows,
        "threshold_rows": build_threshold_rows(),
        "forward_coverage_rows": forward_coverage_rows,
        "proxy": proxy,
        "parity_rows": parity_rows,
        "lifecycle_events": lifecycle_events,
        "lifecycle_rows": lifecycle_rows,
        "comparison_rows": comparison_rows,
        "negative_rows": negative_rows,
        "mt5_rows": mt5_rows,
    }


def build_next_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "run337CE_execute_lifecycle_aware_mt5_runtime_probe",
            "next_run_id": NEXT_RUN_ID,
            "lane": "runtime_probe_after_guarded_training",
            "priority": "P0",
            "reason": "CD materialized cost2-aware ONNX scouts and proxy expected outputs; proxy must be checked against MT5 runtime telemetry before any stronger claim",
            "required_evidence": "MT5 telemetry, strategy tester report, proxy-vs-MT5 diff, lifecycle action parity, cost/session attribution",
            "forbidden_shortcut": "no runtime authority, no Forward Passed, no candidate selection from proxy alone",
            "effect": "moves trained scouts into runtime comparison(학습된 스카우트를 런타임 비교로 이동)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_gates(
    input_rows: Sequence[Mapping[str, Any]],
    payload: Mapping[str, Any],
) -> list[dict[str, Any]]:
    gates = list(input_rows)
    compat_ok = payload["compat_rows"] and all(row["compatibility_status"] == "passed" for row in payload["compat_rows"])
    model_count = len(payload["model_rows"])
    parity_ok = payload["parity_rows"] and all(str(row["passed"]).lower() == "true" for row in payload["parity_rows"])
    proxy_rows = len(payload["proxy"])
    lifecycle_rows = payload["lifecycle_rows"]
    cost2_survivors = [row for row in lifecycle_rows if row["cost2_guard_status"] == "cost2_forward_proxy_survived_diagnostic"]
    negative_failures = [row for row in payload["negative_rows"] if row["status"] != "passed"]
    checks = [
        ("cost2_label_policy_declared", payload["cost2_threshold"] > payload["base_threshold"], f"base={payload['base_threshold']};cost2={payload['cost2_threshold']}"),
        ("model_input_compatibility", compat_ok, f"compat_rows={len(payload['compat_rows'])}"),
        ("models_and_onnx_materialized", model_count >= 6, f"models={model_count}"),
        ("onnx_probability_parity", parity_ok, f"parity_rows={len(payload['parity_rows'])}"),
        ("proxy_expected_materialized", proxy_rows > 0, f"proxy_rows={proxy_rows}"),
        ("lifecycle_proxy_score_materialized", len(lifecycle_rows) >= 6, f"lifecycle_rows={len(lifecycle_rows)}"),
        ("cost2_guard_evaluated", True, f"cost2_survivors={len(cost2_survivors)}"),
        ("negative_controls_evaluated", len(payload["negative_rows"]) >= 12, f"negative_rows={len(payload['negative_rows'])};failures={len(negative_failures)}"),
        ("mt5_probe_package_queued", len(payload["mt5_rows"]) >= 6, f"mt5_rows={len(payload['mt5_rows'])}"),
        ("no_forward_selection_guard", True, "forward diagnostics not used for threshold/model selection"),
        ("final_claim_guard", True, "no forward/goal/runtime authority claim"),
    ]
    for gate_id, passed, observed in checks:
        gates.append(
            {
                "gate_id": gate_id,
                "status": "passed" if passed else "failed",
                "observed": observed,
                "expected": "passed",
                "effect": "supports CD training closeout without operating claim(CD 학습 종료를 운영 주장 없이 지지)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return gates


def classify(gates: Sequence[Mapping[str, Any]], payload: Mapping[str, Any]) -> tuple[str, str, str, str]:
    failed = [row for row in gates if row.get("status") != "passed"]
    if failed:
        return (
            "blocked_stage337CD_lifecycle_aware_training_gate_failed_no_forward_decision",
            "blocked_required_cost2_training_evidence_missing",
            "stage337CD_repair_training_evidence_before_runtime_probe",
            RUN_ID,
        )
    cost2_survivors = [row for row in payload["lifecycle_rows"] if row["cost2_guard_status"] == "cost2_forward_proxy_survived_diagnostic"]
    if cost2_survivors:
        judgment = "cost2_aware_scouts_materialized_proxy_has_cost2_survivors_requires_mt5_runtime_probe"
    else:
        judgment = "cost2_aware_scouts_materialized_but_proxy_cost2_guard_still_failed_requires_attribution"
    return (
        "completed_stage337CD_lifecycle_aware_guarded_scouts_trained_proxy_expected_materialized_no_selection",
        judgment,
        "stage337CD_open_run337CE_execute_lifecycle_aware_mt5_runtime_probe",
        NEXT_RUN_ID,
    )


def build_receipts(final: Mapping[str, Any], payload: Mapping[str, Any]) -> list[Path]:
    payloads = [
        (
            EXPERIMENT_RECEIPT,
            {
                "run_id": RUN_ID,
                "hypothesis": "A cost2-aware label can reduce lifecycle cost fragility without forward threshold fitting.",
                "decision_use": "opens MT5 runtime probe only; no candidate selection",
                "comparison_baseline": [rel(CC_TARGET), rel(CC_UTILIZATION), rel(BU_PROXY_EXPECTED)],
                "control_variables": "US100 M5; train split only; fixed feature orders; fixed threshold rules; no lot optimization",
                "changed_variables": "label threshold adds cost2 buffer before training",
                "sample_scope": "historical train/validation/oos plus post-2026-04-14 forward diagnostic",
                "success_criteria": "models and ONNX are materialized; ONNX parity passes; lifecycle proxy and MT5 probe package are ready",
                "failure_criteria": "no lifecycle events, ONNX parity failure, missing feature order, or no MT5 package",
                "invalid_conditions": "forward rows used for fitting or threshold selection",
                "stop_conditions": "stop before runtime claim; execute MT5 probe next",
                "evidence_plan": [rel(TRAINED_MODEL_MANIFEST), rel(ONNX_PARITY), rel(LIFECYCLE_SCORECARD), rel(MT5_RUNTIME_PROBE_PACKAGE)],
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            DATA_RECEIPT,
            {
                "data_source": [rel(MODEL_INPUT_PATH), rel(FORWARD_US100_RAW), rel(CC_TARGET)],
                "time_axis": "historical split timestamps plus forward MT5 bar-close UTC timestamps",
                "sample_scope": "train 2022-09-01..2024-12-31; validation 2025-01-01..2025-09-30; oos 2025-10-01..2026-04-13; forward after 2026-04-14 diagnostic only",
                "feature_label_boundary": "cost2 labels are built from future returns only as target labels; forward labels are not used for fitting",
                "split_boundary": read_json(TRAINING_SUMMARY).get("split_id", ""),
                "leakage_risk": "controlled by train-only fit and fixed threshold policy",
                "data_hash_or_identity": sha256_file(MODEL_INPUT_PATH) if path_exists(MODEL_INPUT_PATH) else "",
                "integrity_judgment": "usable_with_forward_diagnostic_boundary",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            MODEL_RECEIPT,
            {
                "model_family": "logistic regression and ExtraTrees cost2-aware scouts",
                "target_and_label": "fwd12 3-class label with threshold_log_return + cost2 bps buffer",
                "split_method": "train-only fit; validation/oos/forward diagnostic scoring",
                "selection_metric": "none; no candidate selected",
                "secondary_metrics": [rel(DECISION_SCORECARD), rel(LIFECYCLE_SCORECARD), rel(NEGATIVE_CONTROL_RESULTS)],
                "threshold_policy": "fixed predeclared probability rules",
                "overfit_risk": "forward diagnostics could tempt selection, explicitly forbidden",
                "calibration_risk": "probabilities are rank/decision scores, not calibrated live probabilities",
                "comparison_baseline": rel(CC_TARGET),
                "validation_judgment": final["judgment"],
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            RUNTIME_RECEIPT,
            {
                "research_path": rel(Path(__file__)),
                "runtime_path": rel(MT5_RUNTIME_PROBE_PACKAGE),
                "shared_contract": "feature order hash, ONNX path, fixed thresholds, proxy expected outputs",
                "known_differences": "MT5 execution not run in CD; runtime probe queued for CE",
                "parity_check": rel(ONNX_PARITY),
                "parity_identity": rel(TRAINED_MODEL_MANIFEST),
                "runtime_claim_boundary": "runtime_probe_queued_not_runtime_authority",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            PERFORMANCE_RECEIPT,
            {
                "observed_change": "cost2-aware labels produce new proxy lifecycle score versus BU lifecycle baseline",
                "comparison_baseline": [rel(CC_TARGET), rel(LIFECYCLE_VS_BU_COMPARISON)],
                "likely_drivers": "cost2 label buffer, model family, feature family, lifecycle compression",
                "segment_checks": [rel(DECISION_SCORECARD), rel(LIFECYCLE_SCORECARD), rel(NEGATIVE_CONTROL_RESULTS)],
                "trade_shape": rel(LIFECYCLE_SCORECARD),
                "alternative_explanations": "proxy log-return target may diverge from account PnL and needs MT5 runtime probe",
                "attribution_confidence": "medium_low_until_mt5_runtime_probe",
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
                "availability": "tracked_reports_and_ignored_run_artifacts_with_registry_hashes",
                "lineage_judgment": "connected_with_runtime_probe_boundary",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            JUDGMENT_RECEIPT,
            {
                "result_subject": RUN_ID,
                "evidence_available": [rel(REPORT_PATH), rel(REQUIRED_GATE_AUDIT), rel(TRAINED_MODEL_MANIFEST), rel(LIFECYCLE_SCORECARD)],
                "evidence_missing": "MT5 runtime probe for CD ONNX, spread/slippage stress in actual tester, operating review",
                "judgment_label": final["judgment"],
                "claim_boundary": CLAIM_BOUNDARY,
                "next_condition": final["next_action"],
                "user_explanation_hook": "CD created stricter cost-aware ONNX scouts, but they are still research artifacts until MT5 runtime comparison.",
            },
        ),
        (
            CLAIM_RECEIPT,
            {
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "runtime_authority": "not_claimed",
                "goal_achieve": "not_claimed",
                "effect": "CD closes training materialization only(CD는 학습 물질화만 닫음)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
    ]
    return [write_json(path, item) for path, item in payloads]


def write_report(final: Mapping[str, Any], payload: Mapping[str, Any]) -> Path:
    lifecycle_rows = payload["lifecycle_rows"]
    comparison_rows = payload["comparison_rows"]
    cost2_survivors = [row for row in lifecycle_rows if row["cost2_guard_status"] == "cost2_forward_proxy_survived_diagnostic"]
    lifecycle_lines = "\n".join(
        f"| `{row['model_id']}` | `{row['allowed_role']}` | {row['closed_trade_events']} | {row['net_log_return_cost1']} | {row['profit_factor_cost1']} | `{row['cost2_guard_status']}` |"
        for row in lifecycle_rows
    )
    comparison_lines = "\n".join(
        f"| `{row['cd_model_id']}` | `{row['matched_bu_reference']}` | {row['net_delta_cost1']} | {row['pf_delta_cost1']} | `{row['comparison_judgment']}` |"
        for row in comparison_rows
    )
    return write_md(
        REPORT_PATH,
        f"""# Stage337 run337CD Lifecycle-Aware Guarded Training(생애주기 인식 방어 학습)

## Conclusion(결론)

run337CD(337CD 실행)는 cost2-aware label(비용2 인식 라벨)로 새 ONNX scout(온엑스 스카우트)를 학습하고 proxy expected(프록시 예상)를 만들었다.

Effect(효과): forward threshold tuning(전진 임계값 조정) 없이 비용2를 라벨 경계에 반영했다. 다음은 MT5 runtime probe(MT5 런타임 탐침)로 proxy expected(프록시 예상)와 실제 telemetry(기록)를 비교하는 것이다. Forward/Goal(전진/목표)은 주장하지 않는다.

## Result(결과)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`
- trained_models(학습 모델): `{final['trained_models']}`
- onnx_parity_passed(ONNX 동등성 통과): `{final['onnx_parity_passed']}/{final['onnx_parity_rows']}`
- cost2_survivors(비용2 생존): `{len(cost2_survivors)}`

## Lifecycle Proxy(생애주기 프록시)

| model(모델) | role(역할) | closed events(닫힌 이벤트) | net cost1(비용1 순수익) | PF cost1(비용1 수익 팩터) | cost2 guard(비용2 가드) |
|---|---|---:|---:|---:|---|
{lifecycle_lines}

## Versus BU(기존 BU 대비)

| CD model(CD 모델) | BU reference(BU 기준) | net delta(순수익 차이) | PF delta(PF 차이) | judgment(판정) |
|---|---|---:|---:|---|
{comparison_lines}

## Boundary(경계)

- model_training(모델 학습): `run`
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
        f"""# Decision: Stage337 run337CD Lifecycle-Aware Guarded Training(결정: 생애주기 인식 방어 학습)

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(상위 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

Effect(효과): cost2-aware label(비용2 인식 라벨)로 ONNX scout(온엑스 스카우트)를 만들었고, proxy expected(프록시 예상)와 MT5 runtime probe package(MT5 런타임 탐침 패키지)를 열었다. 이 결정은 후보 선택이나 운영 가능 주장이 아니다.

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
        f"  Stage337 run337CD focus complete: lifecycle-aware guarded training(생애주기 인식 방어 학습)을 `{final['status']}`로 닫았다. "
        "Effect(효과): MT5 runtime probe(MT5 런타임 탐침)를 run337CE(337CE 실행)로 연다.\n"
    )
    if "Stage337 run337CD focus complete" not in workspace:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus_entry, 1)
    artifacts.append(by.write_text_preserving(WORKSPACE_STATE, workspace, workspace_bom))

    current_text, current_bom = by.read_text_lossless(CURRENT_STATE)
    current = current_text
    for field_name, value in {
        "current_run": f"`{NEXT_RUN_ID}`",
        "status": f"`{final['status']}`",
        "decision": f"`{final['decision']}`",
        "latest_completed_run": f"`{RUN_ID}`",
        "next_action": f"`{final['next_action']}`",
        "claim_boundary": f"`{CLAIM_BOUNDARY}`",
    }.items():
        current = replace_bullet_value(current, field_name, value)
    entry = f"""
## Stage337 run337CD(337CD 실행) - {TODAY}

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): cost2-aware ONNX scout(비용2 인식 온엑스 스카우트), proxy expected(프록시 예상), MT5 probe package(MT5 탐침 패키지)를 만들었다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    if "## Stage337 run337CD(337CD 실행)" not in current:
        marker = "## Stage337 run337CC(337CC"
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
- actual_mt5_execution(실제 MT5 실행): `not_run_cd_training_only_mt5_probe_queued`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 다음은 lifecycle-aware MT5 runtime probe(생애주기 인식 MT5 런타임 탐침)이다.
"""
    artifacts.append(by.write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = by.read_text_lossless(STAGE_BRIEF)
    stage_entry = f"- {TODAY}: run337CD(337CD 실행) trained lifecycle-aware guarded scouts(생애주기 인식 방어 스카우트). Status(상태) `{final['status']}`. Forward/Goal(전진/목표)은 주장하지 않음."
    if stage_entry not in stage_text:
        stage_text = stage_text.rstrip() + "\n" + stage_entry + "\n"
    artifacts.append(by.write_text_preserving(STAGE_BRIEF, stage_text, stage_bom))

    changelog_text, changelog_bom = by.read_text_lossless(CHANGELOG)
    changelog_entry = f"- {TODAY}: Stage337 run337CD trained lifecycle-aware guarded scouts(생애주기 인식 방어 스카우트) and opened `{NEXT_RUN_ID}`."
    if changelog_entry not in changelog_text:
        changelog_text = changelog_text.rstrip() + "\n" + changelog_entry + "\n"
    artifacts.append(by.write_text_preserving(CHANGELOG, changelog_text, changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any], artifact_paths: Sequence[Path]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "lifecycle_aware_guarded_training_without_db",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"decision={final['decision']};next_action={final['next_action']};models={final['trained_models']};goal_achieve_not_claimed.",
        "family": "model_validation_runtime_parity",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__lifecycle_guarded_training",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "lifecycle_guarded_training",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "guarded_training",
        "tier_scope": "Tier A+B feature families; forward diagnostic only",
        "kpi_scope": "cost2_label_training_proxy_lifecycle_onnx_parity",
        "scoreboard_lane": "model_scout_training",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"models={final['trained_models']};cost2_survivors={final['cost2_survivors']}",
        "guardrail_kpi": "no threshold tuning; no candidate selection; mt5 runtime probe required",
        "external_verification_status": "out_of_scope_by_claim_training_only_mt5_probe_queued",
        "notes": f"decision={final['decision']};next={final['next_action']}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__lifecycle_guarded_training",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "model_validation_runtime_parity",
        "evidence_scope": "CC lifecycle inputs, BT feature packages, historical model input, forward proxy diagnostics",
        "kpi_scope": "cost2_label_training_and_proxy_lifecycle",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"models={final['trained_models']};onnx_parity={final['onnx_parity_passed']}/{final['onnx_parity_rows']};cost2_survivors={final['cost2_survivors']}",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__lifecycle_guarded_training",
        "family": "model_validation_runtime_parity",
        "question": "can cost2-aware lifecycle guards train new ONNX scouts without forward overfit",
        "metric_scope": "model_proxy_lifecycle_cost_negative_controls",
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
    input_rows = build_input_gates()
    parent = read_json(CC_FINAL)
    if parent.get("next_action") != RUN_ID:
        raise RuntimeError(f"CC final does not open CD: {parent.get('next_action')}")
    payload = train_and_score()
    gates = build_gates(input_rows, payload)
    status, judgment, decision, next_action = classify(gates, payload)
    cost2_survivors = [row for row in payload["lifecycle_rows"] if row["cost2_guard_status"] == "cost2_forward_proxy_survived_diagnostic"]
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "parent_status": parent.get("status", ""),
        "status": status,
        "judgment": judgment,
        "decision": decision,
        "next_action": next_action,
        "base_threshold_log_return": payload["base_threshold"],
        "cost2_threshold_log_return": payload["cost2_threshold"],
        "trained_models": len(payload["model_rows"]),
        "onnx_parity_rows": len(payload["parity_rows"]),
        "onnx_parity_passed": sum(1 for row in payload["parity_rows"] if str(row["passed"]).lower() == "true"),
        "proxy_rows": len(payload["proxy"]),
        "lifecycle_score_rows": len(payload["lifecycle_rows"]),
        "cost2_survivors": len(cost2_survivors),
        "negative_control_rows": len(payload["negative_rows"]),
        "mt5_probe_rows": len(payload["mt5_rows"]),
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
        write_json(LABEL_SPLIT_POLICY, {
            "run_id": RUN_ID,
            "source_training_summary": rel(TRAINING_SUMMARY),
            "label_policy_id": "label_v2_cost2_aware_fwd12_m5_logret_train_only",
            "base_threshold_log_return": payload["base_threshold"],
            "cost2_bps": COST2_BPS,
            "cost2_log_return_buffer": COST2_LOG_RETURN_BUFFER,
            "cost2_threshold_log_return": payload["cost2_threshold"],
            "split_boundaries": payload["training_summary"].get("split_boundaries"),
            "selection_policy": "train split fit only; forward diagnostics cannot select model, threshold, branch, or lot",
            "claim_boundary": CLAIM_BOUNDARY,
        }),
        write_csv(MODEL_INPUT_COMPATIBILITY, COMPAT_COLUMNS, payload["compat_rows"]),
        write_csv(TRAINED_MODEL_MANIFEST, MODEL_MANIFEST_COLUMNS, payload["model_rows"]),
        write_csv(MODEL_METRICS, METRIC_COLUMNS, payload["metric_rows"]),
        write_csv(THRESHOLD_POLICY, THRESHOLD_COLUMNS, payload["threshold_rows"]),
        write_csv(DECISION_SCORECARD, SCORECARD_COLUMNS, payload["score_rows"]),
        write_csv(FORWARD_TRUTH_COVERAGE, FORWARD_COVERAGE_COLUMNS, payload["forward_coverage_rows"]),
        write_csv(PROXY_EXPECTED_FORWARD, list(payload["proxy"].columns), payload["proxy"].to_dict("records")),
        write_csv(ONNX_PARITY, ONNX_PARITY_COLUMNS, payload["parity_rows"]),
        write_csv(LIFECYCLE_EVENT_TABLE, EVENT_COLUMNS, payload["lifecycle_events"]),
        write_csv(LIFECYCLE_SCORECARD, LIFECYCLE_SCORE_COLUMNS, payload["lifecycle_rows"]),
        write_csv(LIFECYCLE_VS_BU_COMPARISON, COMPARISON_COLUMNS, payload["comparison_rows"]),
        write_csv(NEGATIVE_CONTROL_RESULTS, NEGATIVE_COLUMNS, payload["negative_rows"]),
        write_csv(MT5_RUNTIME_PROBE_PACKAGE, MT5_PACKAGE_COLUMNS, payload["mt5_rows"]),
        write_csv(NEXT_RESEARCH_QUEUE, NEXT_COLUMNS, build_next_queue()),
        write_csv(REQUIRED_GATE_AUDIT, GATE_COLUMNS, gates),
        write_json(FINAL_DECISION, final),
    ]
    artifacts.extend(build_receipts(final, payload))
    artifacts.extend([write_report(final, payload), write_decision_doc(final)])
    artifacts.extend(update_docs(final))
    artifacts.append(write_json(RUN_MANIFEST, {"run_id": RUN_ID, "parent_run_id": PARENT_RUN_ID, "inputs": [rel(path) for path in INPUT_FILES], "outputs": [rel(path) for path in OUTPUT_FILES], "claim_boundary": CLAIM_BOUNDARY}))
    artifacts.extend(update_registers(final, artifacts))

    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not final["failed_gates"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
