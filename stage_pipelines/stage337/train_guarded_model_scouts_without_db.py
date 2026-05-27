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

from foundation.models.baseline_training import LABEL_NAMES, LABEL_ORDER
from foundation.models.decision_surface import ThresholdRule, apply_threshold_rule
from foundation.models.onnx_bridge import (
    check_onnxruntime_probability_parity,
    export_sklearn_to_onnx_zipmap_disabled,
    ordered_hash,
    ordered_sklearn_probabilities,
    sha256_file,
)
from stage_pipelines.stage337 import materialize_stale_lag_guarded_model_scout_inputs_without_db as bt


aw = bt.aw
bg = bt.bg

TODAY = "2026-05-28"
STAGE_ID = bt.STAGE_ID
RUN_NUMBER = "run337BU"
RUN_ID = "run337BU_train_guarded_model_scouts_without_db_v1"
PARENT_RUN_ID = bt.RUN_ID
NEXT_RUN_ID = "run337BV_execute_model_scout_mt5_runtime_probe_without_db_v1"
STATUS = "completed_stage337BU_guarded_model_scouts_trained_proxy_expected_materialized_mt5_probe_queued_no_selection"
JUDGMENT = "python_and_onnx_scout_models_materialized_proxy_forward_diagnostics_ready_mt5_runtime_comparison_missing"
DECISION = "stage337BU_open_run337BV_model_scout_mt5_runtime_probe"
CLAIM_BOUNDARY = (
    "research_development_only_stage337BU_guarded_model_scout_training_without_db_"
    "no_forward_selection_no_threshold_tuning_no_candidate_selection_no_forward_passed_no_forward_failed_"
    "no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = bt.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MODEL_DIR = RUN_DIR / "models"
ONNX_DIR = RUN_DIR / "onnx"
PREDICTION_DIR = RUN_DIR / "predictions"
REVIEWS_DIR = bt.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337BU_guarded_model_scout_training.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337BU_guarded_model_scout_training.md"
SELECTED_STATUS = bt.SELECTED_STATUS
STAGE_BRIEF = bt.STAGE_BRIEF
WORKSPACE_STATE = bt.WORKSPACE_STATE
CURRENT_STATE = bt.CURRENT_STATE
CHANGELOG = bt.CHANGELOG
RUN_REGISTRY = bt.RUN_REGISTRY
ALPHA_LEDGER = bt.ALPHA_LEDGER
ARTIFACT_REGISTRY = bt.ARTIFACT_REGISTRY
STAGE_LEDGER = bt.STAGE_LEDGER

BT_DIR = STAGE_DIR / "02_runs" / "run337BT"
BQ_DIR = STAGE_DIR / "02_runs" / "run337BQ"
BO_DIR = STAGE_DIR / "02_runs" / "run337BO"
BT_FINAL = BT_DIR / "final_decision.json"
BT_PACKAGES = BT_DIR / "scout_input_package_matrix.csv"
BT_BRANCH_CONTRACTS = BT_DIR / "scout_branch_contracts.csv"
BT_NEGATIVE_CONTROLS = BT_DIR / "negative_control_matrix.csv"
BT_NO_OVERFIT_GATES = BT_DIR / "no_overfit_gate_matrix.csv"
BT_PROXY_CONTRACT = BT_DIR / "proxy_mt5_comparison_contract.csv"
BT_TRAINING_PLAN = BT_DIR / "guarded_training_plan.csv"
BT_QUEUE = BT_DIR / "run337BU_train_guarded_model_scouts_queue.csv"
BT_GATE_AUDIT = BT_DIR / "required_gate_coverage_audit.csv"
BQ_RUNTIME_MANIFEST = BQ_DIR / "mt5_runtime_parity_package" / "runtime_parity_package_manifest.json"
FORWARD_US100_RAW = BO_DIR / "raw_refresh_probe" / "US100" / "bars_us100_m5_mt5api_raw.csv"

MODEL_INPUT_PATH = ROOT / "data" / "processed" / "model_inputs" / "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58" / "model_input_dataset.parquet"
MODEL_INPUT_FEATURE_ORDER = ROOT / "data" / "processed" / "model_inputs" / "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58" / "model_input_feature_order.txt"
TRAINING_SUMMARY = ROOT / "data" / "processed" / "training_datasets" / "label_v1_fwd12_split_v1_proxyw58" / "training_dataset_summary.json"
LABEL_CONTRACT_DOC = ROOT / "docs" / "contracts" / "training_label_split_contract_fpmarkets_v2.md"

LABEL_SPLIT_POLICY = RUN_DIR / "label_split_policy.json"
MODEL_INPUT_COMPATIBILITY = RUN_DIR / "model_input_compatibility.csv"
TRAINED_MODEL_MANIFEST = RUN_DIR / "trained_model_manifest.csv"
MODEL_METRICS = RUN_DIR / "model_metrics.csv"
THRESHOLD_POLICY = RUN_DIR / "decision_threshold_policy.csv"
DECISION_SCORECARD = RUN_DIR / "decision_scorecard.csv"
FORWARD_TRUTH_COVERAGE = RUN_DIR / "forward_truth_coverage.csv"
PROXY_EXPECTED_FORWARD = RUN_DIR / "proxy_expected_forward_predictions.csv"
ONNX_PARITY = RUN_DIR / "onnxruntime_parity_matrix.csv"
NEGATIVE_CONTROL_RESULTS = RUN_DIR / "negative_control_results.csv"
MT5_RUNTIME_PROBE_PACKAGE = RUN_DIR / "mt5_runtime_probe_package.csv"
RUN337BV_QUEUE = RUN_DIR / "run337BV_model_scout_mt5_runtime_probe_queue.csv"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
ARTIFACT_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    BT_FINAL,
    BT_PACKAGES,
    BT_BRANCH_CONTRACTS,
    BT_NEGATIVE_CONTROLS,
    BT_NO_OVERFIT_GATES,
    BT_PROXY_CONTRACT,
    BT_TRAINING_PLAN,
    BT_QUEUE,
    BT_GATE_AUDIT,
    BQ_RUNTIME_MANIFEST,
    FORWARD_US100_RAW,
    MODEL_INPUT_PATH,
    MODEL_INPUT_FEATURE_ORDER,
    TRAINING_SUMMARY,
    LABEL_CONTRACT_DOC,
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
    NEGATIVE_CONTROL_RESULTS,
    MT5_RUNTIME_PROBE_PACKAGE,
    RUN337BV_QUEUE,
    EXPERIMENT_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    RUNTIME_RECEIPT,
    ARTIFACT_RECEIPT,
    JUDGMENT_RECEIPT,
    REQUIRED_GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
)

MODEL_SPECS = (
    {
        "model_family": "logreg_balanced_c1",
        "model_role": "linear_defensive_control(선형 방어 대조)",
        "mt5_runtime_priority": "P0",
    },
    {
        "model_family": "extratrees_depth6_leaf120",
        "model_role": "nonlinear_offense_probe(비선형 공격 탐침)",
        "mt5_runtime_priority": "P0",
    },
)
THRESHOLD_RULES = (
    {
        "rule_role": "balanced_primary(균형 주 규칙)",
        "selection_use": "predeclared_primary_not_forward_selected(사전선언 주 규칙, 전진 선택 아님)",
        "rule": ThresholdRule("fixed_short040_long040_margin002", 0.40, 0.40, 0.02),
        "primary": True,
    },
    {
        "rule_role": "defensive_sparse(방어 희소 규칙)",
        "selection_use": "diagnostic_only(진단 전용)",
        "rule": ThresholdRule("fixed_short045_long045_margin005", 0.45, 0.45, 0.05),
        "primary": False,
    },
    {
        "rule_role": "aggressive_density(공격 밀도 규칙)",
        "selection_use": "diagnostic_only(진단 전용)",
        "rule": ThresholdRule("fixed_short036_long036_margin000", 0.36, 0.36, 0.00),
        "primary": False,
    },
)
PRIMARY_RULE = next(item["rule"] for item in THRESHOLD_RULES if item["primary"])
GATE_COLUMNS = bt.GATE_COLUMNS

COMPAT_COLUMNS = (
    "branch_id",
    "feature_set_id",
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
    "model_family",
    "model_role",
    "feature_count",
    "feature_order_hash",
    "model_path",
    "model_sha256",
    "onnx_path",
    "onnx_sha256",
    "onnx_probability_output_name",
    "mt5_runtime_priority",
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
    "threshold_log_return",
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
NEGATIVE_COLUMNS = (
    "control_id",
    "branch_id",
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
    "mt5_required",
    "expected_compare_keys",
    "claim_boundary",
)
QUEUE_COLUMNS = (
    "queue_id",
    "next_run_id",
    "probe_package",
    "must_execute",
    "must_compare",
    "must_reject_if",
    "expected_outputs",
    "priority",
    "effect",
    "claim_boundary",
)


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return aw.rel(Path(path))


def parse_args() -> argparse.Namespace:
    return argparse.ArgumentParser(description=RUN_ID).parse_args()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(aw.io_path(path).read_text(encoding="utf-8-sig"))


def read_rows(path: Path) -> list[dict[str, str]]:
    _, rows = aw.read_csv_table(path, prefer_head=False)
    return rows


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    aw.io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with aw.io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})
    return path


def write_json(path: Path, payload: Mapping[str, Any]) -> Path:
    return aw.write_json(path, payload)


def pass_fail(ok: bool) -> str:
    return "passed" if ok else "failed"


def finite_float(value: Any) -> float:
    number = float(value)
    return number if math.isfinite(number) else 0.0


def safe_pf(returns: np.ndarray) -> float:
    wins = returns[returns > 0.0].sum()
    losses = returns[returns < 0.0].sum()
    if losses == 0.0:
        return float("inf") if wins > 0.0 else 0.0
    return float(wins / abs(losses))


def max_drawdown(values: np.ndarray) -> float:
    if values.size == 0:
        return 0.0
    curve = np.cumsum(values)
    peak = np.maximum.accumulate(curve)
    dd = curve - peak
    return float(dd.min()) if dd.size else 0.0


def worst_rolling(values: np.ndarray, window: int) -> float:
    if values.size == 0:
        return 0.0
    if values.size < window:
        return float(values.sum())
    kernel = np.ones(window)
    rolling = np.convolve(values, kernel, mode="valid")
    return float(rolling.min()) if rolling.size else 0.0


def timestamp_span_days(timestamps: pd.Series) -> float:
    if timestamps.empty:
        return 0.0
    start = pd.to_datetime(timestamps, utc=True).min()
    end = pd.to_datetime(timestamps, utc=True).max()
    days = (end - start).total_seconds() / 86400.0
    return max(float(days), 1.0)


def mql_time_text(value: str) -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    if "T" in text:
        parsed = pd.Timestamp(text)
        if parsed.tzinfo is not None:
            parsed = parsed.tz_convert("UTC")
        return parsed.strftime("%Y.%m.%d %H:%M:%S")
    if "-" in text[:10]:
        parsed = pd.Timestamp(text)
        return parsed.strftime("%Y.%m.%d %H:%M:%S")
    return text


def fnv1a64_upper(line: str) -> str:
    value = 1469598103934665603
    for char in line:
        value = ((value ^ ord(char)) * 1099511628211) & 0xFFFFFFFFFFFFFFFF
    return f"{value:X}"


def timestamp_hash_index(csv_path: Path) -> dict[pd.Timestamp, str]:
    output: dict[pd.Timestamp, str] = {}
    with aw.io_path(csv_path).open("r", encoding="utf-8-sig", newline="") as handle:
        header_line = handle.readline().rstrip("\r\n")
        header = next(csv.reader([header_line]))
        timestamp_col = next((idx for idx, name in enumerate(header) if name.strip().lower() == "timestamp_utc"), -1)
        if timestamp_col < 0:
            timestamp_col = next((idx for idx, name in enumerate(header) if name.strip().lower() == "bar_time_server"), -1)
        if timestamp_col < 0:
            raise RuntimeError(f"{csv_path} has no timestamp column")
        for raw_line in handle:
            line = raw_line.rstrip("\r\n")
            if not line:
                continue
            cols = next(csv.reader([line]))
            if timestamp_col >= len(cols):
                continue
            timestamp = pd.Timestamp(cols[timestamp_col])
            if timestamp.tzinfo is None:
                timestamp = timestamp.tz_localize("UTC")
            else:
                timestamp = timestamp.tz_convert("UTC")
            output[timestamp] = fnv1a64_upper(line)
    return output


def load_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if not aw.path_exists(path)]
    if missing:
        raise FileNotFoundError(f"missing run337BU inputs: {missing}")
    bt_final = read_json(BT_FINAL)
    if bt_final.get("next_action") != RUN_ID:
        raise RuntimeError(f"run337BT final does not open run337BU: {bt_final.get('next_action')}")
    training_summary = read_json(TRAINING_SUMMARY)
    return {
        "bt_final": bt_final,
        "bt_packages": read_rows(BT_PACKAGES),
        "bt_branch_contracts": read_rows(BT_BRANCH_CONTRACTS),
        "bt_negative_controls": read_rows(BT_NEGATIVE_CONTROLS),
        "bt_gates": read_rows(BT_GATE_AUDIT),
        "bt_queue": read_rows(BT_QUEUE),
        "bq_runtime_manifest": read_json(BQ_RUNTIME_MANIFEST),
        "training_summary": training_summary,
        "model_input": pd.read_parquet(aw.io_path(MODEL_INPUT_PATH)),
    }


def load_feature_order(path: Path) -> list[str]:
    return [line.strip() for line in aw.io_path(path).read_text(encoding="utf-8-sig").splitlines() if line.strip()]


def build_label_split_policy(training_summary: Mapping[str, Any]) -> dict[str, Any]:
    payload = {
        "run_id": RUN_ID,
        "label_id": training_summary.get("label_id"),
        "split_id": training_summary.get("split_id"),
        "source_training_summary": rel(TRAINING_SUMMARY),
        "source_model_input": rel(MODEL_INPUT_PATH),
        "threshold_log_return": training_summary.get("threshold_log_return"),
        "horizon_bars": training_summary.get("horizon_bars"),
        "horizon_minutes": training_summary.get("horizon_minutes"),
        "split_boundaries": training_summary.get("split_boundaries"),
        "selection_policy": "train/validation/oos may be used for diagnostics; forward after 2026-04-14 is held out from branch and threshold selection(학습/검증/OOS는 진단용, 2026-04-14 이후 전진은 분기/임계값 선택 제외)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return payload


def build_model_input_compatibility(
    packages: Sequence[Mapping[str, Any]],
    model_input: pd.DataFrame,
) -> tuple[list[dict[str, Any]], dict[str, list[str]]]:
    model_columns = set(model_input.columns)
    split_counts = model_input["split"].astype(str).value_counts().to_dict()
    feature_orders: dict[str, list[str]] = {}
    rows: list[dict[str, Any]] = []
    for package in packages:
        branch_id = str(package["branch_id"])
        feature_set_id = str(package["feature_set_id"])
        order_path = ROOT / str(package["feature_order_path"])
        features = load_feature_order(order_path)
        feature_orders[branch_id] = features
        missing = [name for name in features if name not in model_columns]
        nonfinite_rows = 0
        if not missing:
            values = model_input.loc[:, features].to_numpy(dtype="float64", copy=False)
            finite_mask = np.isfinite(values).all(axis=1)
            nonfinite_rows = int((~finite_mask).sum())
        rows.append(
            {
                "branch_id": branch_id,
                "feature_set_id": feature_set_id,
                "feature_count": len(features),
                "model_input_rows": len(model_input),
                "train_rows": int(split_counts.get("train", 0)),
                "validation_rows": int(split_counts.get("validation", 0)),
                "oos_rows": int(split_counts.get("oos", 0)),
                "missing_features": ";".join(missing),
                "nonfinite_rows": nonfinite_rows,
                "feature_order_hash": ordered_hash(features),
                "compatibility_status": "passed" if not missing and nonfinite_rows == 0 else "failed",
                "effect": "checks that forward feature packages are trainable from frozen historical inputs(전진 피처 패키지가 고정 과거 입력에서 학습 가능한지 확인)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows, feature_orders


def make_model(model_family: str) -> Any:
    if model_family == "logreg_balanced_c1":
        return Pipeline(
            steps=[
                ("scaler", StandardScaler()),
                (
                    "classifier",
                    LogisticRegression(
                        C=1.0,
                        class_weight="balanced",
                        max_iter=2000,
                        random_state=337,
                        solver="lbfgs",
                    ),
                ),
            ]
        )
    if model_family == "extratrees_depth6_leaf120":
        return ExtraTreesClassifier(
            n_estimators=140,
            max_depth=6,
            min_samples_leaf=120,
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


def class_dist(values: pd.Series) -> dict[str, int]:
    counts = values.astype("int64").value_counts().to_dict()
    return {LABEL_NAMES[label]: int(counts.get(label, 0)) for label in LABEL_ORDER}


def build_model_metric_row(
    *,
    model_id: str,
    branch_id: str,
    feature_set_id: str,
    model_family: str,
    split: str,
    frame: pd.DataFrame,
    probabilities: pd.DataFrame,
) -> dict[str, Any]:
    labels = frame["label_class"].astype("int64").to_numpy()
    pred = np.asarray(LABEL_ORDER, dtype="int64")[probabilities.to_numpy(dtype="float64").argmax(axis=1)]
    pred_dist = class_dist(pd.Series(pred))
    true_dist = class_dist(frame["label_class"])
    return {
        "model_id": model_id,
        "branch_id": branch_id,
        "feature_set_id": feature_set_id,
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


def apply_forward_truth(
    feature_frame: pd.DataFrame,
    training_summary: Mapping[str, Any],
) -> tuple[pd.DataFrame, dict[str, Any]]:
    raw = pd.read_csv(aw.io_path(FORWARD_US100_RAW), usecols=["time_close_unix", "close"])
    raw["timestamp"] = pd.to_datetime(raw["time_close_unix"], unit="s", utc=True)
    close_by_time = raw.set_index("timestamp")["close"].astype("float64")
    threshold = float(training_summary["threshold_log_return"])
    frame = feature_frame.copy()
    frame["timestamp"] = pd.to_datetime(frame["timestamp_utc"], utc=True)
    frame["future_timestamp"] = frame["timestamp"] + pd.Timedelta(minutes=int(training_summary["horizon_minutes"]))
    current_close = frame["timestamp"].map(close_by_time)
    future_close = frame["future_timestamp"].map(close_by_time)
    frame["future_log_return_12"] = np.log(future_close.astype("float64") / current_close.astype("float64"))
    labelable = frame["future_log_return_12"].notna() & np.isfinite(frame["future_log_return_12"].to_numpy(dtype="float64", na_value=np.nan))
    frame["forward_label_available"] = labelable
    frame["label_class"] = np.where(
        frame["future_log_return_12"] < -threshold,
        0,
        np.where(frame["future_log_return_12"] > threshold, 2, 1),
    )
    frame["label"] = frame["label_class"].map(LABEL_NAMES)
    coverage = {
        "feature_rows": int(len(frame)),
        "forward_labelable_rows": int(labelable.sum()),
        "missing_future_rows": int((~labelable).sum()),
        "first_timestamp": frame["timestamp"].min().isoformat() if len(frame) else "",
        "last_timestamp": frame["timestamp"].max().isoformat() if len(frame) else "",
        "first_labelable_timestamp": frame.loc[labelable, "timestamp"].min().isoformat() if labelable.any() else "",
        "last_labelable_timestamp": frame.loc[labelable, "timestamp"].max().isoformat() if labelable.any() else "",
        "future_raw_last_timestamp": raw["timestamp"].max().isoformat() if len(raw) else "",
        "threshold_log_return": threshold,
    }
    return frame, coverage


def score_decisions(
    *,
    model_id: str,
    branch_id: str,
    feature_set_id: str,
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
    labels = frame["label_class"].astype("int64").to_numpy() if "label_class" in frame.columns else np.array([], dtype="int64")
    future = frame["future_log_return_12"].astype("float64").to_numpy() if "future_log_return_12" in frame.columns else np.full(len(decisions), np.nan)
    decision_class = decisions["decision_label_class"].to_numpy(dtype="int64")
    signal_mask = decision_class != -1
    label_mask = signal_mask & np.isfinite(future)
    signed = np.zeros(len(decisions), dtype="float64")
    signed[decision_class == 2] = future[decision_class == 2]
    signed[decision_class == 0] = -future[decision_class == 0]
    trade_returns = signed[label_mask] - float(cost_bps) / 10000.0
    dd = max_drawdown(trade_returns)
    hit_rate = np.nan
    if label_mask.any() and labels.size == len(decisions):
        hit_rate = float((decision_class[label_mask] == labels[label_mask]).mean())
    signal_count = int(signal_mask.sum())
    return {
        "model_id": model_id,
        "branch_id": branch_id,
        "feature_set_id": feature_set_id,
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
        "net_log_return_sum": float(trade_returns.sum()) if trade_returns.size else 0.0,
        "profit_factor": safe_pf(trade_returns),
        "expectancy_per_trade": float(trade_returns.mean()) if trade_returns.size else 0.0,
        "max_drawdown_log_return": dd,
        "recovery_factor": float(trade_returns.sum() / abs(dd)) if dd < 0.0 else (float("inf") if trade_returns.sum() > 0.0 else 0.0),
        "worst_20_trade_net_log_return": worst_rolling(trade_returns, 20),
        "trades_per_day": float(signal_count / timestamp_span_days(frame["timestamp"] if "timestamp" in frame.columns else pd.Series(dtype="datetime64[ns, UTC]"))),
        "selection_use": selection_use,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_proxy_rows(
    *,
    model_id: str,
    branch_id: str,
    feature_set_id: str,
    model_family: str,
    feature_frame: pd.DataFrame,
    probabilities: pd.DataFrame,
    feature_hashes: Mapping[pd.Timestamp, str],
) -> pd.DataFrame:
    decisions = apply_threshold_rule(probabilities, PRIMARY_RULE)
    output = pd.DataFrame(
        {
            "model_id": model_id,
            "branch_id": branch_id,
            "feature_set_id": feature_set_id,
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
            "label_class": feature_frame["label_class"].to_numpy(dtype="int64"),
            "label": feature_frame["label"].astype(str).to_numpy(),
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )
    return output


def train_and_score(src: Mapping[str, Any], feature_orders: Mapping[str, list[str]]) -> dict[str, Any]:
    frame = src["model_input"].copy()
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    package_by_branch = {str(row["branch_id"]): row for row in src["bt_packages"]}
    metrics: list[dict[str, Any]] = []
    scorecards: list[dict[str, Any]] = []
    model_rows: list[dict[str, Any]] = []
    parity_rows: list[dict[str, Any]] = []
    negative_rows: list[dict[str, Any]] = []
    forward_coverage_rows: list[dict[str, Any]] = []
    proxy_parts: list[pd.DataFrame] = []
    mt5_rows: list[dict[str, Any]] = []

    for branch_id, features in feature_orders.items():
        package = package_by_branch[branch_id]
        feature_set_id = str(package["feature_set_id"])
        feature_csv = ROOT / str(package["feature_csv_path"])
        feature_hashes = timestamp_hash_index(feature_csv)
        forward_features = pd.read_csv(aw.io_path(feature_csv))
        forward_features, coverage = apply_forward_truth(forward_features, src["training_summary"])
        forward_coverage_rows.append(
            {
                "feature_set_id": feature_set_id,
                **coverage,
                "integrity_status": "usable_with_forward_label_boundary(전진 라벨 경계 포함 사용 가능)",
                "effect": "forward labels are diagnostic only and cannot select branch or threshold(전진 라벨은 진단 전용이며 분기/임계값 선택 금지)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

        split_frames = {split: frame.loc[frame["split"].astype(str).eq(split)].copy() for split in ("train", "validation", "oos")}
        X_train = split_frames["train"].loc[:, features].to_numpy(dtype="float64", copy=False)
        y_train = split_frames["train"]["label_class"].astype("int64").to_numpy()

        for spec in MODEL_SPECS:
            model_family = str(spec["model_family"])
            model_id = f"{branch_id}__{model_family}"
            model = make_model(model_family)
            model.fit(X_train, y_train)

            model_path = MODEL_DIR / f"{model_id}.joblib"
            onnx_path = ONNX_DIR / f"{model_id}.onnx"
            aw.io_path(model_path.parent).mkdir(parents=True, exist_ok=True)
            joblib.dump(model, aw.io_path(model_path))
            export_info = export_sklearn_to_onnx_zipmap_disabled(
                model,
                onnx_path,
                feature_count=len(features),
                target_opset=12,
                drop_label_output=True,
            )
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
                    "model_family": model_family,
                    "model_role": spec["model_role"],
                    "feature_count": len(features),
                    "feature_order_hash": ordered_hash(features),
                    "model_path": rel(model_path),
                    "model_sha256": sha256_file(model_path),
                    "onnx_path": rel(onnx_path),
                    "onnx_sha256": sha256_file(onnx_path),
                    "onnx_probability_output_name": export_info["probability_output_name"],
                    "mt5_runtime_priority": spec["mt5_runtime_priority"],
                    "training_rows": len(split_frames["train"]),
                    "validation_rows": len(split_frames["validation"]),
                    "oos_rows": len(split_frames["oos"]),
                    "training_policy": "train split only; no forward data fit(학습 분할만 사용, 전진 데이터 학습 금지)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )

            split_probabilities: dict[str, pd.DataFrame] = {}
            for split, split_frame in split_frames.items():
                probabilities = probability_frame(model, split_frame, features)
                split_probabilities[split] = probabilities
                metrics.append(
                    build_model_metric_row(
                        model_id=model_id,
                        branch_id=branch_id,
                        feature_set_id=feature_set_id,
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
                        scorecards.append(
                            score_decisions(
                                model_id=model_id,
                                branch_id=branch_id,
                                feature_set_id=feature_set_id,
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
            proxy_part = build_proxy_rows(
                model_id=model_id,
                branch_id=branch_id,
                feature_set_id=feature_set_id,
                model_family=model_family,
                feature_frame=forward_features,
                probabilities=forward_prob,
                feature_hashes=feature_hashes,
            )
            proxy_parts.append(proxy_part)
            labelable_forward = forward_features.loc[forward_features["forward_label_available"].astype(bool)].copy()
            forward_label_prob = forward_prob.loc[labelable_forward.index]
            for rule_payload in THRESHOLD_RULES:
                for cost_bps in (0.0, 1.0, 2.0):
                    scorecards.append(
                        score_decisions(
                            model_id=model_id,
                            branch_id=branch_id,
                            feature_set_id=feature_set_id,
                            model_family=model_family,
                            split="forward_after_2026_04_14_diagnostic",
                            frame=labelable_forward,
                            probabilities=forward_label_prob,
                            rule_payload=rule_payload,
                            cost_bps=cost_bps,
                            selection_use="forward_diagnostic_holdout_not_selection(전진 진단 홀드아웃, 선택 금지)",
                        )
                    )

            # Negative controls are intentionally light and bounded: they test failure signals, not new candidates.
            validation = split_frames["validation"].copy()
            validation_probs = split_probabilities["validation"]
            primary_score = score_decisions(
                model_id=model_id,
                branch_id=branch_id,
                feature_set_id=feature_set_id,
                model_family=model_family,
                split="validation",
                frame=validation,
                probabilities=validation_probs,
                rule_payload={"rule": PRIMARY_RULE},
                cost_bps=0.0,
                selection_use="negative_control_reference(부정 대조 기준)",
            )
            shuffled_features = list(reversed(features))
            shuffled_hash = ordered_hash(shuffled_features)
            negative_rows.append(
                {
                    "control_id": f"{model_id}__feature_order_reverse_hash_gate",
                    "branch_id": branch_id,
                    "model_family": model_family,
                    "control_type": "feature_order_reverse_hash_gate",
                    "observed": f"original={ordered_hash(features)};reversed={shuffled_hash}",
                    "expected": "hash_mismatch",
                    "status": "passed" if shuffled_hash != ordered_hash(features) else "failed",
                    "effect": "feature order mutation is caught before runtime(피처 순서 변형을 런타임 전 탐지)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            shifted = validation.copy()
            shifted["future_log_return_12"] = shifted["future_log_return_12"].shift(-1)
            shifted_score = score_decisions(
                model_id=model_id,
                branch_id=branch_id,
                feature_set_id=feature_set_id,
                model_family=model_family,
                split="validation_shifted_future_return_control",
                frame=shifted.dropna(subset=["future_log_return_12"]),
                probabilities=validation_probs.loc[shifted.dropna(subset=["future_log_return_12"]).index],
                rule_payload={"rule": PRIMARY_RULE},
                cost_bps=0.0,
                selection_use="negative_control(부정 대조)",
            )
            negative_rows.append(
                {
                    "control_id": f"{model_id}__timestamp_shift_profit_tripwire",
                    "branch_id": branch_id,
                    "model_family": model_family,
                    "control_type": "timestamp_shift_profit_tripwire",
                    "observed": f"original_net={primary_score['net_log_return_sum']:.8f};shifted_net={shifted_score['net_log_return_sum']:.8f}",
                    "expected": "control_is_different_not_selection_input",
                    "status": "passed" if abs(primary_score["net_log_return_sum"] - shifted_score["net_log_return_sum"]) > 1.0e-9 else "failed",
                    "effect": "timestamp shifts change payoff, so exact time binding remains necessary(시각 이동이 보상을 바꾸므로 정확한 시간 연결이 필요)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )

            mt5_rows.append(
                {
                    "probe_id": f"{model_id}__primary_threshold_mt5_probe",
                    "model_id": model_id,
                    "branch_id": branch_id,
                    "feature_set_id": feature_set_id,
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
                    "mt5_required": "true",
                    "expected_compare_keys": "bar_time;feature_input_hash;p_short;p_flat;p_long;decision_label",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )

    return {
        "model_rows": model_rows,
        "metric_rows": metrics,
        "scorecard_rows": scorecards,
        "forward_coverage_rows": forward_coverage_rows,
        "proxy_expected": pd.concat(proxy_parts, ignore_index=True) if proxy_parts else pd.DataFrame(),
        "onnx_parity_rows": parity_rows,
        "negative_rows": negative_rows,
        "mt5_rows": mt5_rows,
    }


def build_threshold_policy_rows() -> list[dict[str, Any]]:
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
                "primary_rule": str(bool(item["primary"])).lower(),
                "selection_use": item["selection_use"],
                "effect": "threshold rules are fixed before forward scoring(임계값 규칙은 전진 채점 전에 고정)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "run337BV_model_scout_mt5_runtime_probe",
            "next_run_id": NEXT_RUN_ID,
            "probe_package": rel(MT5_RUNTIME_PROBE_PACKAGE),
            "must_execute": "run MT5 RuntimeProbeEA against every P0 ONNX/feature package when tester environment is available(테스터 환경 가능 시 모든 P0 ONNX/피처 패키지를 RuntimeProbeEA로 실행)",
            "must_compare": "proxy expected vs MT5 telemetry by bar_time, feature_input_hash, probabilities, and decision(프록시 예상 대 MT5 기록을 봉 시각/해시/확률/결정으로 비교)",
            "must_reject_if": "MT5 output missing, probability mismatch, feature hash mismatch, or tester gap hides latest rows(MT5 출력 누락/확률 불일치/피처 해시 불일치/테스터 공백)",
            "expected_outputs": "mt5_runtime_telemetry;proxy_mt5_diff;strategy_report_if_trading;runtime_claim_boundary",
            "priority": "P0",
            "effect": "turns proxy-only scouts into runtime-comparable probes(프록시 전용 스카우트를 런타임 비교 가능한 탐침으로 전환)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_gates(
    src: Mapping[str, Any],
    compat_rows: Sequence[Mapping[str, Any]],
    train_result: Mapping[str, Any],
    queue_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    bt_passed = sum(1 for row in src["bt_gates"] if row.get("status") == "passed")
    compat_ok = all(row.get("compatibility_status") == "passed" for row in compat_rows)
    parity_ok = all(row.get("passed") == "true" for row in train_result["onnx_parity_rows"])
    forward_labelable = sum(int(row.get("forward_labelable_rows") or 0) for row in train_result["forward_coverage_rows"])
    specs = [
        ("bu_gate_parent_bt_loaded", src["bt_final"].get("next_action") == RUN_ID, str(src["bt_final"].get("next_action")), "run337BT opens run337BU(337BT가 337BU를 연다)"),
        ("bu_gate_parent_bt_gates_passed", bt_passed == 11 and src["bt_final"].get("passed_gates") == 11, f"bt_gates={bt_passed}", "BT gates passed(BT 게이트 통과)"),
        ("bu_gate_label_split_policy_declared", bool(src["training_summary"].get("threshold_log_return")) and bool(src["training_summary"].get("split_id")), str(src["training_summary"].get("split_id")), "label and split declared(라벨/분할 선언)"),
        ("bu_gate_feature_compatibility_passed", compat_ok, f"compat_ok={compat_ok}", "all three feature sets trainable(3개 피처 세트 학습 가능)"),
        ("bu_gate_models_trained", len(train_result["model_rows"]) == 6, f"models={len(train_result['model_rows'])}", "six fixed model scouts trained(고정 모델 스카우트 6개 학습)"),
        ("bu_gate_onnxruntime_parity_passed", parity_ok, f"onnx_parity={parity_ok}", "ONNX runtime parity passed(ONNX 런타임 동등성 통과)"),
        ("bu_gate_forward_proxy_expected_written", len(train_result["proxy_expected"]) > 0 and forward_labelable > 0, f"proxy_rows={len(train_result['proxy_expected'])};labelable={forward_labelable}", "forward proxy expected rows written(전진 프록시 예상 행 작성)"),
        ("bu_gate_negative_controls_written", len(train_result["negative_rows"]) >= 12, f"negative_rows={len(train_result['negative_rows'])}", "negative controls executed(부정 대조 실행)"),
        ("bu_gate_mt5_probe_package_written", len(train_result["mt5_rows"]) == len(train_result["model_rows"]), f"mt5_probe_rows={len(train_result['mt5_rows'])}", "MT5 runtime probe package written(MT5 런타임 탐침 패키지 작성)"),
        ("bu_gate_queue_ready", len(queue_rows) == 1 and queue_rows[0].get("next_run_id") == NEXT_RUN_ID, f"queue_rows={len(queue_rows)}", "run337BV queue ready(337BV 대기열 준비)"),
        ("bu_gate_no_forward_selection_or_goal_claim", True, "selection=not_run;forward_passed=not_claimed;goal=not_claimed", "no forbidden claim(금지 주장 없음)"),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": pass_fail(ok),
            "observed": observed,
            "expected": expected,
            "effect": "training can advance only as research scout with runtime comparison still required(학습은 런타임 비교가 필요한 연구 스카우트로만 전진)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, ok, observed, expected in specs
    ]


def count_passed(rows: Sequence[Mapping[str, Any]]) -> int:
    return sum(1 for row in rows if row.get("status") == "passed")


def report_table(score_rows: Sequence[Mapping[str, Any]]) -> str:
    filtered = [
        row
        for row in score_rows
        if row.get("split") == "forward_after_2026_04_14_diagnostic"
        and row.get("threshold_id") == PRIMARY_RULE.threshold_id
        and float(row.get("cost_bps_per_trade") or 0.0) == 1.0
    ]
    lines = [
        "| model(모델) | branch(분기) | trades(거래) | net log return(순 로그수익) | PF(수익 팩터) | DD(손실폭) |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for row in filtered:
        pf = row.get("profit_factor")
        pf_text = "inf" if isinstance(pf, float) and math.isinf(pf) else f"{float(pf):.4f}"
        lines.append(
            f"| `{row['model_family']}` | `{row['branch_id']}` | {row['signal_count']} | {float(row['net_log_return_sum']):.6f} | {pf_text} | {float(row['max_drawdown_log_return']):.6f} |"
        )
    return "\n".join(lines)


def write_report(final: Mapping[str, Any], score_rows: Sequence[Mapping[str, Any]]) -> Path:
    text = f"""# Stage337 run337BU Guarded Model Scout Training(방어 모델 스카우트 학습)

## Conclusion(결론)

run337BU(337BU 실행)는 run337BT(337BT 실행)의 guarded scout inputs(방어 스카우트 입력)를 실제 trained model scouts(학습된 모델 스카우트)와 ONNX(온엑스) 산출물로 바꿨다.

Effect(효과): technical-only(기술 전용), macro-lag(거시 지연), equity-stale(주식 낡음) 분기마다 logreg(로지스틱 회귀)와 ExtraTrees(엑스트라트리)를 학습했고, forward(전진) 구간은 diagnostic holdout(진단 홀드아웃)으로만 채점했다. MT5 runtime comparison(MT5 런타임 비교)은 다음 run337BV(337BV 실행) 필수 조건이다.

## Result(결과)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`
- trained_models(학습 모델): `{final['trained_model_rows']}`
- onnx_parity_passed(온엑스 동등성 통과): `{final['onnx_parity_passed']}/{final['onnx_parity_rows']}`
- proxy_expected_rows(프록시 예상 행): `{final['proxy_expected_rows']}`

## Forward Diagnostic(전진 진단)

Primary fixed rule(주 고정 규칙): `{PRIMARY_RULE.threshold_id}`. 이 표는 selection(선택)이 아니라 다음 MT5 probe(탐침) 우선순위와 위험 감지를 위한 진단이다.

{report_table(score_rows)}

## Boundary(경계)

- forward_selection(전진 선택): `not_run`
- threshold_tuning(임계값 조정): `not_run`
- candidate_selection(후보 선택): `not_run`
- MT5 runtime comparison(MT5 런타임 비교): `queued_not_completed`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Claim boundary(주장 경계): `{final['claim_boundary']}`
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision: Stage337 run337BU Guarded Model Scout Training(결정: 방어 모델 스카우트 학습)

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(상위 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

Effect(효과): Python/ONNX(파이썬/온엑스) scout(스카우트)는 만들어졌지만, proxy expected vs MT5 runtime(프록시 예상 대 MT5 런타임) 비교가 아직 없어 runtime authority(런타임 권위)와 Forward Passed/Failed(전진 통과/실패)는 열 수 없다.

Claim boundary(주장 경계): `{final['claim_boundary']}`
"""
    return aw.write_text_lossless(DECISION_DOC, text, True)


def build_receipts(final: Mapping[str, Any]) -> list[Path]:
    payloads: list[tuple[Path, Mapping[str, Any]]] = [
        (
            EXPERIMENT_RECEIPT,
            {
                "hypothesis": "bounded logreg and ExtraTrees scouts can expose which stale-lag feature family is worth runtime probing without selecting on forward outcome",
                "decision_use": "open MT5 runtime comparison, not candidate selection",
                "comparison_baseline": "technical-only low-stale branch and no-trade",
                "control_variables": "fixed label/split, fixed feature orders, fixed threshold rules, no forward training",
                "changed_variables": "feature family and fixed model family",
                "sample_scope": "historical train/validation/oos plus forward-after-2026-04-14 diagnostic holdout",
                "success_criteria": "ONNX parity passes and proxy expected outputs are ready for MT5 comparison",
                "failure_criteria": "ONNX parity fails, forward diagnostics are fragile, or negative controls fail",
                "invalid_conditions": "feature hash drift, timestamp mismatch, forward threshold selection, MT5 mismatch",
                "stop_conditions": "do not promote before MT5 runtime comparison",
                "evidence_plan": [rel(MODEL_METRICS), rel(DECISION_SCORECARD), rel(MT5_RUNTIME_PROBE_PACKAGE)],
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            DATA_RECEIPT,
            {
                "data_source": [rel(MODEL_INPUT_PATH), rel(BQ_RUNTIME_MANIFEST), rel(FORWARD_US100_RAW)],
                "time_axis": "closed M5 UTC bar timestamps; forward labels exact +60 minutes",
                "sample_scope": "train/validation/oos to 2026-04-13 plus forward after 2026-04-14",
                "missing_or_duplicate_check": rel(MODEL_INPUT_COMPATIBILITY),
                "feature_label_boundary": "forward labels used only for diagnostics, never fit or threshold selection",
                "split_boundary": "frozen split_v1 for training; forward is held out",
                "leakage_risk": "forward outcome selection and stale-lag context dependence",
                "data_hash_or_identity": f"model_input={sha256_file(MODEL_INPUT_PATH)};forward_raw={sha256_file(FORWARD_US100_RAW)}",
                "integrity_judgment": "usable_with_boundary",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            MODEL_RECEIPT,
            {
                "model_family": "logreg_balanced_c1;extratrees_depth6_leaf120",
                "target_and_label": "label_v1_fwd12_m5_logret_train_q33_3class",
                "split_method": "frozen chronological train/validation/oos; forward held out",
                "selection_metric": "none_in_run337BU",
                "secondary_metrics": "classification, threshold diagnostics, proxy cost stress, curve drawdown",
                "threshold_policy": "predeclared fixed threshold rules only",
                "overfit_risk": "branch/model family cherry-picking after forward diagnostics",
                "calibration_risk": "scores are ranking signals until calibration and MT5 comparison prove otherwise",
                "comparison_baseline": "technical-only branch and no-trade",
                "validation_judgment": "exploratory_runtime_probe_candidate_input",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            RUNTIME_RECEIPT,
            {
                "research_path": rel(Path(__file__)),
                "runtime_path": rel(MT5_RUNTIME_PROBE_PACKAGE),
                "shared_contract": "feature CSV, feature order hash, ONNX path, fixed threshold, proxy expected path",
                "known_differences": "MT5 RuntimeProbeEA not executed in run337BU",
                "parity_check": "onnxruntime parity completed; MT5 comparison queued",
                "parity_identity": rel(ONNX_PARITY),
                "runtime_claim_boundary": "research_only_mt5_runtime_missing",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            ARTIFACT_RECEIPT,
            {
                "source_inputs": [rel(path) for path in INPUT_FILES],
                "producer": rel(Path(__file__)),
                "consumer": NEXT_RUN_ID,
                "artifact_paths": [rel(path) for path in OUTPUT_FILES if aw.path_exists(path)],
                "artifact_hashes": "registered in artifact registry",
                "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
                "availability": "ignored_with_manifest_for_heavy_run_artifacts;tracked_reports_and_registers",
                "lineage_judgment": "connected_with_boundary",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            JUDGMENT_RECEIPT,
            {
                "result_subject": RUN_ID,
                "evidence_available": [rel(REPORT_PATH), rel(MODEL_METRICS), rel(ONNX_PARITY), rel(PROXY_EXPECTED_FORWARD)],
                "evidence_missing": "MT5 runtime probe output, strategy report, proxy-vs-MT5 diff, operating validation",
                "judgment_label": "exploratory_runtime_probe_candidate_input",
                "claim_boundary": CLAIM_BOUNDARY,
                "next_condition": NEXT_RUN_ID,
                "user_explanation_hook": "모델은 만들어졌지만 아직 MT5에서 같은 값이 나오는지 확인해야 한다.",
            },
        ),
    ]
    return [write_json(path, payload) for path, payload in payloads]


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    workspace_text, workspace_bom = aw.read_text_lossless(WORKSPACE_STATE)
    workspace = bg.replace_top_value(workspace_text, "current_run_id: ", NEXT_RUN_ID)
    workspace = bg.replace_top_value(workspace, "updated_on: ", f"'{TODAY}'")
    focus_entry = (
        "- >-\n"
        f"  Stage337 run337BU focus complete: guarded model scout training(방어 모델 스카우트 학습)을 `{final['status']}`로 닫았다. "
        "Effect(효과): Python/ONNX(파이썬/온엑스) 모델과 forward proxy expected(전진 프록시 예상)를 만들고, proxy-vs-MT5(프록시 대 MT5) 비교를 run337BV(337BV 실행)로 넘긴다.\n"
    )
    if "Stage337 run337BU focus complete" not in workspace:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus_entry, 1)
    artifacts.append(aw.write_text_lossless(WORKSPACE_STATE, workspace, workspace_bom))

    current_text, current_bom = aw.read_text_lossless(CURRENT_STATE)
    current = current_text
    replacements = {
        "- current_run(현재 실행): ": f"`{NEXT_RUN_ID}`",
        "- status(상태): ": f"`{final['status']}`",
        "- decision(결정): ": f"`{final['decision']}`",
        "- latest_completed_run(최근 완료 실행): ": f"`{RUN_ID}`",
        "- next_action(다음 행동): ": f"`{NEXT_RUN_ID}`",
        "- claim_boundary(주장 경계): ": f"`{CLAIM_BOUNDARY}`",
    }
    for prefix, value in replacements.items():
        current = bg.replace_top_value(current, prefix, value)
    entry = f"""
## Stage337 run337BU(337BU 실행) - {TODAY}

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): 방어/공격 모델 스카우트를 학습하고 ONNX(온엑스)와 proxy expected(프록시 예상)를 만들었지만, MT5 runtime comparison(MT5 런타임 비교)은 다음 실행 필수 조건으로 남겼다.
"""
    if "## Stage337 run337BU(337BU 실행)" not in current:
        marker = "## Stage337 run337BT(337BT 실행)"
        current = current.replace(marker, entry + "\n" + marker, 1) if marker in current else current.rstrip() + "\n\n" + entry
    artifacts.append(aw.write_text_lossless(CURRENT_STATE, current, current_bom))

    selection_text = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- frozen_subject(고정 대상): `cp322A_cp321b_exact_replay_control_surface`
- exact_cp322a_forward_handoff(정확 cp322A 전진 인계): `not_feasible_under_frozen_rules`
- preserved_status(보존 상태): `research_artifact_only`
- rebuild_status(재구축 상태): `{final['status']}`
- actual_mt5_execution(실제 MT5 실행): `not_run_model_probe_queued`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 다음은 proxy expected vs MT5 runtime(프록시 예상 대 MT5 런타임) 비교다.
"""
    artifacts.append(aw.write_text_lossless(SELECTED_STATUS, selection_text, True))

    stage_text, stage_bom = aw.read_text_lossless(STAGE_BRIEF)
    stage_entry = f"- {TODAY}: run337BU(337BU 실행) trained guarded model scouts(방어 모델 스카우트) and materialized proxy expected outputs(프록시 예상 출력). Status(상태) `{final['status']}`. MT5 runtime comparison(MT5 런타임 비교)은 run337BV로 넘김."
    if stage_entry not in stage_text:
        stage_text = stage_text.rstrip() + "\n" + stage_entry + "\n"
    artifacts.append(aw.write_text_lossless(STAGE_BRIEF, stage_text, stage_bom))

    changelog_text, changelog_bom = aw.read_text_lossless(CHANGELOG)
    changelog_entry = f"- {TODAY}: Stage337 run337BU trained guarded model scouts(방어 모델 스카우트) and opened run337BV(337BV 실행) for MT5 runtime comparison."
    if changelog_entry not in changelog_text:
        changelog_text = changelog_text.rstrip() + "\n" + changelog_entry + "\n"
    artifacts.append(aw.write_text_lossless(CHANGELOG, changelog_text, changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any], artifact_paths: Sequence[Path]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "guarded_model_scout_training_without_db",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"decision={final['decision']};next_action={final['next_action']};models={final['trained_model_rows']};goal_achieve_not_claimed.",
        "family": "model_validation_runtime_parity",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__guarded_model_scout_training",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "guarded_model_scout_training",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "python_onnx_proxy_expected",
        "tier_scope": "Tier A+B combined research input; no paired runtime claim yet",
        "kpi_scope": "classification_and_proxy_forward_diagnostic_no_mt5",
        "scoreboard_lane": "model_scout_training",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"trained_models={final['trained_model_rows']}",
        "guardrail_kpi": "onnx_parity_passed;mt5_runtime_missing;no_forward_selection",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={final['decision']};next={final['next_action']}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__guarded_model_scout_training",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "model_validation_runtime_parity",
        "evidence_scope": "trained scout models, ONNX parity, forward proxy expected",
        "kpi_scope": "diagnostic_no_mt5_kpi_authority",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"models={final['trained_model_rows']};proxy_rows={final['proxy_expected_rows']}",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__guarded_model_scout_training",
        "family": "model_validation_runtime_parity",
        "question": "can guarded feature families train ONNX scouts without forward selection and prepare MT5 comparison",
        "metric_scope": "classification_proxy_forward_no_mt5",
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
    artifact_columns = artifact_columns or [
        "artifact_id",
        "artifact_type",
        "path",
        "sha256",
        "stage_id",
        "run_id",
        "created_at_utc",
        "notes",
        "artifact_path",
        "claim_boundary",
    ]
    generated = now_utc()
    new_rows: list[dict[str, Any]] = []
    for path in artifact_paths:
        if not aw.path_exists(path) or not aw.io_path(path).is_file():
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
    for directory in (RUN_DIR, MODEL_DIR, ONNX_DIR, PREDICTION_DIR):
        aw.io_path(directory).mkdir(parents=True, exist_ok=True)
    src = load_inputs()
    packages = src["bt_packages"]
    label_policy = build_label_split_policy(src["training_summary"])
    compat_rows, feature_orders = build_model_input_compatibility(packages, src["model_input"])
    train_result = train_and_score(src, feature_orders)
    queue_rows = build_queue()
    gates = build_gates(src, compat_rows, train_result, queue_rows)
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "trained_model_rows": len(train_result["model_rows"]),
        "model_metric_rows": len(train_result["metric_rows"]),
        "decision_scorecard_rows": len(train_result["scorecard_rows"]),
        "forward_coverage_rows": len(train_result["forward_coverage_rows"]),
        "proxy_expected_rows": int(len(train_result["proxy_expected"])),
        "onnx_parity_rows": len(train_result["onnx_parity_rows"]),
        "onnx_parity_passed": sum(1 for row in train_result["onnx_parity_rows"] if row.get("passed") == "true"),
        "negative_control_rows": len(train_result["negative_rows"]),
        "mt5_runtime_probe_rows": len(train_result["mt5_rows"]),
        "forward_selection": "not_run",
        "threshold_tuning": "not_run",
        "candidate_selection": "not_run",
        "mt5_runtime_comparison": "queued_not_completed",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    final["gate_rows"] = len(gates)
    final["passed_gates"] = count_passed(gates)
    final["failed_gates"] = [row["gate_id"] for row in gates if row["status"] != "passed"]
    if final["failed_gates"]:
        final["status"] = "blocked_stage337BU_guarded_model_scout_training_gate_failed"
        final["judgment"] = "blocked_training_gate_failed"
        final["decision"] = "stage337BU_repair_training_inputs_before_mt5_probe"
        final["next_action"] = RUN_ID

    artifact_paths: list[Path] = [
        write_json(LABEL_SPLIT_POLICY, label_policy),
        write_csv(MODEL_INPUT_COMPATIBILITY, COMPAT_COLUMNS, compat_rows),
        write_csv(TRAINED_MODEL_MANIFEST, MODEL_MANIFEST_COLUMNS, train_result["model_rows"]),
        write_csv(MODEL_METRICS, METRIC_COLUMNS, train_result["metric_rows"]),
        write_csv(THRESHOLD_POLICY, THRESHOLD_COLUMNS, build_threshold_policy_rows()),
        write_csv(DECISION_SCORECARD, SCORECARD_COLUMNS, train_result["scorecard_rows"]),
        write_csv(FORWARD_TRUTH_COVERAGE, FORWARD_COVERAGE_COLUMNS, train_result["forward_coverage_rows"]),
        write_csv(ONNX_PARITY, ONNX_PARITY_COLUMNS, train_result["onnx_parity_rows"]),
        write_csv(NEGATIVE_CONTROL_RESULTS, NEGATIVE_COLUMNS, train_result["negative_rows"]),
        write_csv(MT5_RUNTIME_PROBE_PACKAGE, MT5_PACKAGE_COLUMNS, train_result["mt5_rows"]),
        write_csv(RUN337BV_QUEUE, QUEUE_COLUMNS, queue_rows),
        write_csv(REQUIRED_GATE_AUDIT, GATE_COLUMNS, gates),
        write_json(FINAL_DECISION, final),
    ]
    if not train_result["proxy_expected"].empty:
        train_result["proxy_expected"].to_csv(aw.io_path(PROXY_EXPECTED_FORWARD), index=False)
        artifact_paths.append(PROXY_EXPECTED_FORWARD)
    artifact_paths.extend([Path(row["model_path"]) for row in train_result["model_rows"]])
    artifact_paths.extend([Path(row["onnx_path"]) for row in train_result["model_rows"]])
    artifact_paths.extend(build_receipts(final))
    artifact_paths.append(
        write_json(
            RUN_MANIFEST,
            {
                "run_id": RUN_ID,
                "parent_run_id": PARENT_RUN_ID,
                "generated_at_utc": now_utc(),
                "inputs": [rel(path) for path in INPUT_FILES],
                "outputs": [rel(path) for path in OUTPUT_FILES],
                "model_artifacts": [row["model_path"] for row in train_result["model_rows"]],
                "onnx_artifacts": [row["onnx_path"] for row in train_result["model_rows"]],
                "external_verification_status": "out_of_scope_by_claim",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
    )
    artifact_paths.append(write_report(final, train_result["scorecard_rows"]))
    artifact_paths.append(write_decision_doc(final))
    if not final["failed_gates"]:
        artifact_paths.extend(update_docs(final))
    artifact_paths.extend(update_registers(final, artifact_paths))
    print(json.dumps(final, ensure_ascii=False, indent=2))
    return 1 if final["failed_gates"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
