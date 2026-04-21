from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

import numpy as np
import pandas as pd

try:
    from foundation.pipelines.materialize_fpmarkets_v2_dataset import (
        DATASET_ID,
        EXPECTED_FEATURE_ORDER_HASH,
        FEATURE_ORDER,
        PARSER_VERSION,
        build_feature_frame,
    )
    from foundation.pipelines.materialize_fpmarkets_v2_tiered_readiness_scorecard import SCORECARD_ID
except ModuleNotFoundError:
    dataset_module_path = Path(__file__).with_name("materialize_fpmarkets_v2_dataset.py")
    dataset_spec = importlib.util.spec_from_file_location(
        "materialize_fpmarkets_v2_dataset_for_stage06_baseline_seed",
        dataset_module_path,
    )
    if dataset_spec is None or dataset_spec.loader is None:
        raise RuntimeError(f"Could not load dataset materializer from {dataset_module_path}")
    dataset_module = importlib.util.module_from_spec(dataset_spec)
    sys.modules[dataset_spec.name] = dataset_module
    dataset_spec.loader.exec_module(dataset_module)
    DATASET_ID = dataset_module.DATASET_ID
    EXPECTED_FEATURE_ORDER_HASH = dataset_module.EXPECTED_FEATURE_ORDER_HASH
    FEATURE_ORDER = dataset_module.FEATURE_ORDER
    PARSER_VERSION = dataset_module.PARSER_VERSION
    build_feature_frame = dataset_module.build_feature_frame

    scorecard_module_path = Path(__file__).with_name("materialize_fpmarkets_v2_tiered_readiness_scorecard.py")
    scorecard_spec = importlib.util.spec_from_file_location(
        "materialize_fpmarkets_v2_tiered_readiness_scorecard_for_stage06_baseline_seed",
        scorecard_module_path,
    )
    if scorecard_spec is None or scorecard_spec.loader is None:
        raise RuntimeError(f"Could not load scorecard materializer from {scorecard_module_path}")
    scorecard_module = importlib.util.module_from_spec(scorecard_spec)
    sys.modules[scorecard_spec.name] = scorecard_module
    scorecard_spec.loader.exec_module(scorecard_module)
    SCORECARD_ID = scorecard_module.SCORECARD_ID


STAGE_NAME = "06_tiered_readiness_exploration"
RUN_ID = "tier_b_offline_eval_0001"
BASELINE_SEED_ID = "baseline_seed_fpmarkets_v2_tier_b_offline_eval_0001"
REPORT_ID = "report_fpmarkets_v2_tier_b_offline_evaluation_0001"
MODEL_FAMILY_ID = "gaussian_nb_3class_tier_a_seed_0001"
FIT_LANE = "strict_tier_a_only"
LOCAL_SPEC_REF = "stages/06_tiered_readiness_exploration/01_inputs/stage06_v2_baseline_seed_local_spec.md@2026-04-22"
DECISION_REF = "docs/decisions/2026-04-22_stage06_v2_baseline_seed_first.md@2026-04-22"
ADR_REF = "docs/adr/0003_tier_b_reduced_risk_experiment_charter.md@2026-04-22"

MANIFEST_FILENAME = "baseline_seed_manifest_fpmarkets_v2_tier_b_offline_eval_0001.json"
PROBABILITY_FILENAME = "baseline_probability_table_fpmarkets_v2_tier_b_offline_eval_0001.parquet"
SUMMARY_FILENAME = "baseline_evaluation_summary_fpmarkets_v2_tier_b_offline_eval_0001.json"
CALIBRATION_FILENAME = "baseline_calibration_read_fpmarkets_v2_tier_b_offline_eval_0001.json"
DEFAULT_OUTPUT_ROOT = Path("stages/06_tiered_readiness_exploration/02_runs/tier_b_offline_eval_0001")
DEFAULT_REPORT_PATH = Path(
    "stages/06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tier_b_offline_evaluation_0001.md"
)
DEFAULT_ROW_LABELS_PATH = Path(
    "stages/06_tiered_readiness_exploration/02_runs/tiered_readiness_scorecard_0001/"
    "readiness_row_labels_fpmarkets_v2_tiered_readiness_0001.parquet"
)

TRAIN_START_UTC = pd.Timestamp("2022-09-01T00:00:00Z")
TRAIN_END_UTC = pd.Timestamp("2024-12-31T23:55:00Z")
VALIDATION_START_UTC = pd.Timestamp("2025-01-01T00:00:00Z")
VALIDATION_END_UTC = pd.Timestamp("2025-08-31T23:55:00Z")
HOLDOUT_START_UTC = pd.Timestamp("2025-09-01T00:00:00Z")
HOLDOUT_END_UTC = pd.Timestamp("2026-04-13T23:55:00Z")

TARGET_LABEL_ORDER = ["short", "flat", "long"]
TARGET_TO_INDEX = {label: index for index, label in enumerate(TARGET_LABEL_ORDER)}
PROBABILITY_COLUMNS = ["p_short", "p_flat", "p_long"]
TARGET_VALUE_COLUMNS = ["future_log_return_1"]
REPORTING_LANE_ORDER = ["strict_tier_a", "tier_b_exploration"]
DATA_SPLIT_ORDER = ["train", "validation", "holdout"]
CALIBRATION_BIN_EDGES = (0.0, 0.4, 0.5, 0.6, 0.7, 0.8, 1.0000001)


@dataclass(frozen=True)
class GaussianNaiveBayesModel:
    class_prior: np.ndarray
    means: np.ndarray
    variances: np.ndarray


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Materialize the first Stage 06 v2-native baseline seed and Tier B offline evaluation report."
    )
    parser.add_argument(
        "--raw-root",
        default="data/raw/mt5_bars/m5",
        help="Repo-relative root containing raw M5 MT5 bar exports.",
    )
    parser.add_argument(
        "--row-labels-path",
        default=str(DEFAULT_ROW_LABELS_PATH),
        help="Repo-relative readiness row-label parquet produced by scorecard_0001.",
    )
    parser.add_argument(
        "--output-root",
        default=str(DEFAULT_OUTPUT_ROOT),
        help="Repo-relative output root for the baseline seed artifacts.",
    )
    parser.add_argument(
        "--report-path",
        default=str(DEFAULT_REPORT_PATH),
        help="Repo-relative output path for the rendered offline evaluation report.",
    )
    parser.add_argument(
        "--reviewed-on",
        default=pd.Timestamp.now(tz="Asia/Seoul").date().isoformat(),
        help="Review date to stamp into the rendered report.",
    )
    return parser.parse_args()


def _fs_path(path: Path) -> str | Path:
    resolved = path.resolve()
    path_text = str(resolved)
    if sys.platform != "win32":
        return resolved
    if path_text.startswith("\\\\?\\"):
        return path_text
    if path_text.startswith("\\\\"):
        return "\\\\?\\UNC\\" + path_text.lstrip("\\")
    return "\\\\?\\" + path_text


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(_fs_path(path), "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _write_text(path: Path, text: str, *, bom: bool = False) -> None:
    encoding = "utf-8-sig" if bom else "utf-8"
    with open(_fs_path(path), "w", encoding=encoding, newline="\n") as handle:
        handle.write(text)


def load_row_labels(path: Path) -> pd.DataFrame:
    row_labels = pd.read_parquet(_fs_path(path))
    required_columns = {
        "timestamp",
        "readiness_tier",
        "reporting_lane",
        "missing_groups",
        "missing_symbols",
    }
    missing = required_columns.difference(row_labels.columns)
    if missing:
        raise RuntimeError(f"Row-label artifact {path} is missing columns: {sorted(missing)}")
    row_labels = row_labels.copy()
    row_labels["timestamp"] = pd.to_datetime(row_labels["timestamp"], utc=True)
    if row_labels["timestamp"].duplicated().any():
        raise RuntimeError(f"Duplicate timestamps detected in row-label artifact {path}")
    return row_labels


def assign_data_split(timestamp: pd.Timestamp) -> str | None:
    if TRAIN_START_UTC <= timestamp <= TRAIN_END_UTC:
        return "train"
    if VALIDATION_START_UTC <= timestamp <= VALIDATION_END_UTC:
        return "validation"
    if HOLDOUT_START_UTC <= timestamp <= HOLDOUT_END_UTC:
        return "holdout"
    return None


def assign_target_label(value: float, *, q33: float, q67: float) -> str:
    if value <= q33:
        return "short"
    if value >= q67:
        return "long"
    return "flat"


def build_model_frame(frame: pd.DataFrame, row_labels: pd.DataFrame) -> pd.DataFrame:
    merged = frame[["timestamp", "close", *FEATURE_ORDER]].merge(
        row_labels[["timestamp", "readiness_tier", "reporting_lane", "missing_groups", "missing_symbols"]],
        on="timestamp",
        how="left",
        validate="one_to_one",
    )
    if merged["readiness_tier"].isna().any():
        missing_count = int(merged["readiness_tier"].isna().sum())
        raise RuntimeError(f"Could not align {missing_count} dataset rows to readiness row labels.")

    merged["future_log_return_1"] = np.log(merged["close"].shift(-1) / merged["close"])
    merged["data_split"] = merged["timestamp"].map(assign_data_split)
    merged["fit_lane"] = FIT_LANE
    merged["row_pre_imputation_nan_count"] = merged[FEATURE_ORDER].isna().sum(axis=1).astype("int64")
    merged["row_received_imputation"] = merged["row_pre_imputation_nan_count"].gt(0)
    return merged


def training_mask(frame: pd.DataFrame) -> pd.Series:
    return (
        frame["data_split"].eq("train")
        & frame["readiness_tier"].eq("tier_a")
        & frame["future_log_return_1"].notna()
    )


def eligible_output_mask(frame: pd.DataFrame) -> pd.Series:
    evaluation_split = frame["data_split"].isin(("validation", "holdout"))
    evaluation_lane = frame["readiness_tier"].isin(("tier_a", "tier_b"))
    train_fit_rows = frame["data_split"].eq("train") & frame["readiness_tier"].eq("tier_a")
    return (train_fit_rows | (evaluation_split & evaluation_lane)) & frame["future_log_return_1"].notna()


def fit_gaussian_nb(features: np.ndarray, labels: np.ndarray) -> GaussianNaiveBayesModel:
    class_prior = []
    means = []
    variances = []
    for class_index in range(len(TARGET_LABEL_ORDER)):
        class_mask = labels == class_index
        class_features = features[class_mask]
        if class_features.size == 0:
            raise RuntimeError(f"No training rows were available for class index {class_index}.")
        class_prior.append(float(class_mask.mean()))
        means.append(class_features.mean(axis=0))
        variances.append(np.maximum(class_features.var(axis=0), 1e-9))
    return GaussianNaiveBayesModel(
        class_prior=np.asarray(class_prior, dtype=np.float64),
        means=np.asarray(means, dtype=np.float64),
        variances=np.asarray(variances, dtype=np.float64),
    )


def predict_gaussian_nb(model: GaussianNaiveBayesModel, features: np.ndarray) -> np.ndarray:
    log_probs = []
    for class_index in range(len(TARGET_LABEL_ORDER)):
        diff = features - model.means[class_index]
        log_likelihood = -0.5 * np.sum(
            np.log(2.0 * np.pi * model.variances[class_index]) + (diff * diff) / model.variances[class_index],
            axis=1,
        )
        log_probs.append(np.log(model.class_prior[class_index]) + log_likelihood)
    stacked = np.column_stack(log_probs)
    max_log = np.max(stacked, axis=1, keepdims=True)
    probs = np.exp(stacked - max_log)
    probs /= probs.sum(axis=1, keepdims=True)
    return probs


def macro_f1_score(labels: np.ndarray, predictions: np.ndarray) -> float:
    scores = []
    for class_index in range(len(TARGET_LABEL_ORDER)):
        true_positive = float(np.sum((labels == class_index) & (predictions == class_index)))
        false_positive = float(np.sum((labels != class_index) & (predictions == class_index)))
        false_negative = float(np.sum((labels == class_index) & (predictions != class_index)))
        precision = true_positive / (true_positive + false_positive) if (true_positive + false_positive) else 0.0
        recall = true_positive / (true_positive + false_negative) if (true_positive + false_negative) else 0.0
        if precision + recall == 0:
            scores.append(0.0)
        else:
            scores.append(2.0 * precision * recall / (precision + recall))
    return float(np.mean(scores))


def balanced_accuracy_score(labels: np.ndarray, predictions: np.ndarray) -> float:
    recalls = []
    for class_index in range(len(TARGET_LABEL_ORDER)):
        support = float(np.sum(labels == class_index))
        if support == 0:
            recalls.append(0.0)
            continue
        true_positive = float(np.sum((labels == class_index) & (predictions == class_index)))
        recalls.append(true_positive / support)
    return float(np.mean(recalls))


def multiclass_log_loss(labels: np.ndarray, probabilities: np.ndarray) -> float:
    eps = 1e-12
    picked = probabilities[np.arange(len(labels)), labels]
    return float(-np.mean(np.log(np.clip(picked, eps, 1.0))))


def multiclass_brier_score(labels: np.ndarray, probabilities: np.ndarray) -> float:
    truth = np.zeros_like(probabilities)
    truth[np.arange(len(labels)), labels] = 1.0
    return float(np.mean(np.sum((probabilities - truth) ** 2, axis=1)))


def _class_balance(labels: np.ndarray) -> dict[str, int]:
    return {
        label: int(np.sum(labels == index)) for index, label in enumerate(TARGET_LABEL_ORDER)
    }


def summarize_probability_slice(probability_table: pd.DataFrame) -> dict[str, object]:
    labels = probability_table["target_index"].to_numpy(dtype=np.int64, copy=False)
    probabilities = probability_table[PROBABILITY_COLUMNS].to_numpy(dtype=np.float64, copy=False)
    predictions = probability_table["predicted_index"].to_numpy(dtype=np.int64, copy=False)
    received_imputation = probability_table["row_received_imputation"].to_numpy(dtype=bool, copy=False)
    pre_nan_count = probability_table["row_pre_imputation_nan_count"].to_numpy(dtype=np.int64, copy=False)
    return {
        "row_count": int(len(probability_table)),
        "class_balance": _class_balance(labels),
        "predicted_balance": _class_balance(predictions),
        "log_loss": multiclass_log_loss(labels, probabilities),
        "macro_f1": macro_f1_score(labels, predictions),
        "balanced_accuracy": balanced_accuracy_score(labels, predictions),
        "multiclass_brier_score": multiclass_brier_score(labels, probabilities),
        "mean_max_probability": float(probabilities.max(axis=1).mean()),
        "rows_with_imputation": int(received_imputation.sum()),
        "mean_missing_feature_count": float(pre_nan_count.mean()),
    }


def summarize_calibration_slice(probability_table: pd.DataFrame) -> dict[str, object]:
    max_probability = probability_table[PROBABILITY_COLUMNS].to_numpy(dtype=np.float64, copy=False).max(axis=1)
    target_index = probability_table["target_index"].to_numpy(dtype=np.int64, copy=False)
    predicted_index = probability_table["predicted_index"].to_numpy(dtype=np.int64, copy=False)
    hit = (target_index == predicted_index).astype(np.float64)

    bins = []
    weighted_gap = 0.0
    for start, end in zip(CALIBRATION_BIN_EDGES[:-1], CALIBRATION_BIN_EDGES[1:], strict=True):
        if math.isclose(end, CALIBRATION_BIN_EDGES[-1]):
            mask = (max_probability >= start) & (max_probability <= 1.0)
        else:
            mask = (max_probability >= start) & (max_probability < end)
        if not mask.any():
            continue
        mean_confidence = float(max_probability[mask].mean())
        observed_accuracy = float(hit[mask].mean())
        gap = abs(mean_confidence - observed_accuracy)
        count = int(mask.sum())
        weighted_gap += gap * count
        bins.append(
            {
                "bin_start": float(start),
                "bin_end": float(min(end, 1.0)),
                "row_count": count,
                "mean_confidence": mean_confidence,
                "observed_accuracy": observed_accuracy,
                "abs_gap": float(gap),
            }
        )
    row_count = int(len(probability_table))
    return {
        "row_count": row_count,
        "expected_calibration_error": float(weighted_gap / row_count) if row_count else 0.0,
        "mean_max_probability": float(max_probability.mean()) if row_count else 0.0,
        "observed_top_class_accuracy": float(hit.mean()) if row_count else 0.0,
        "bins": bins,
    }


def build_probability_table(frame: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, float]]:
    train_rows = training_mask(frame)
    train_returns = frame.loc[train_rows, "future_log_return_1"]
    if train_returns.empty:
        raise RuntimeError("No Tier A training rows were available for the Stage 06 v2 baseline seed.")

    q33 = float(train_returns.quantile(0.33))
    q67 = float(train_returns.quantile(0.67))

    model_frame = frame.copy()
    model_frame["target_label"] = model_frame["future_log_return_1"].map(
        lambda value: assign_target_label(value, q33=q33, q67=q67) if pd.notna(value) else None
    )
    model_frame["target_index"] = model_frame["target_label"].map(TARGET_TO_INDEX)

    train_feature_means = model_frame.loc[train_rows, FEATURE_ORDER].mean()
    feature_matrix = model_frame[FEATURE_ORDER].fillna(train_feature_means)

    model = fit_gaussian_nb(
        feature_matrix.loc[train_rows].to_numpy(dtype=np.float64, copy=False),
        model_frame.loc[train_rows, "target_index"].to_numpy(dtype=np.int64, copy=False),
    )

    eligible_rows = eligible_output_mask(model_frame)
    eligible_table = model_frame.loc[
        eligible_rows,
        [
            "timestamp",
            "readiness_tier",
            "reporting_lane",
            "data_split",
            "fit_lane",
            "missing_groups",
            "missing_symbols",
            "future_log_return_1",
            "row_pre_imputation_nan_count",
            "row_received_imputation",
            "target_label",
            "target_index",
        ],
    ].copy()

    probabilities = predict_gaussian_nb(
        model,
        feature_matrix.loc[eligible_rows].to_numpy(dtype=np.float64, copy=False),
    )
    for column_name, column_values in zip(PROBABILITY_COLUMNS, probabilities.T, strict=True):
        eligible_table[column_name] = column_values.astype(np.float64)

    predicted_index = probabilities.argmax(axis=1)
    eligible_table["predicted_index"] = predicted_index.astype(np.int64)
    eligible_table["predicted_label"] = [TARGET_LABEL_ORDER[index] for index in predicted_index]
    eligible_table["symbol"] = "US100"
    eligible_table["row_used_for_fit"] = (
        eligible_table["data_split"].eq("train") & eligible_table["readiness_tier"].eq("tier_a")
    )

    ordered_columns = [
        "timestamp",
        "symbol",
        "data_split",
        "fit_lane",
        "readiness_tier",
        "reporting_lane",
        "missing_groups",
        "missing_symbols",
        "row_used_for_fit",
        "row_received_imputation",
        "row_pre_imputation_nan_count",
        "future_log_return_1",
        "target_label",
        "predicted_label",
        *PROBABILITY_COLUMNS,
        "target_index",
        "predicted_index",
    ]
    eligible_table = eligible_table[ordered_columns].sort_values("timestamp").reset_index(drop=True)
    return eligible_table, {"q33": q33, "q67": q67}


def build_evaluation_summary(probability_table: pd.DataFrame, *, row_labels_path: str) -> dict[str, object]:
    summary = {
        "dataset_id": DATASET_ID,
        "scorecard_id": SCORECARD_ID,
        "baseline_seed_id": BASELINE_SEED_ID,
        "report_id": REPORT_ID,
        "model_family_id": MODEL_FAMILY_ID,
        "produced_by_stage": STAGE_NAME,
        "parser_version": PARSER_VERSION,
        "feature_order_hash": EXPECTED_FEATURE_ORDER_HASH,
        "row_labels_path": row_labels_path,
        "local_spec_ref": LOCAL_SPEC_REF,
        "decision_ref": DECISION_REF,
        "adr_ref": ADR_REF,
        "fit_lane": FIT_LANE,
        "probability_output_order": PROBABILITY_COLUMNS,
        "splits": {},
    }
    for split_name in DATA_SPLIT_ORDER:
        split_payload: dict[str, object] = {}
        split_table = probability_table.loc[probability_table["data_split"].eq(split_name)].copy()
        if split_table.empty:
            summary["splits"][split_name] = split_payload
            continue
        for lane_name in REPORTING_LANE_ORDER:
            lane_table = split_table.loc[split_table["reporting_lane"].eq(lane_name)].copy()
            if lane_table.empty:
                continue
            split_payload[lane_name] = summarize_probability_slice(lane_table)
        if split_name in {"validation", "holdout"}:
            split_payload["mixed_info_only"] = summarize_probability_slice(split_table)
        summary["splits"][split_name] = split_payload
    return summary


def build_calibration_read(probability_table: pd.DataFrame) -> dict[str, object]:
    payload = {
        "baseline_seed_id": BASELINE_SEED_ID,
        "report_id": REPORT_ID,
        "model_family_id": MODEL_FAMILY_ID,
        "calibration_mode": "read_only",
        "confidence_column": "max_probability",
        "bin_edges": [float(min(edge, 1.0)) for edge in CALIBRATION_BIN_EDGES],
        "splits": {},
    }
    for split_name in DATA_SPLIT_ORDER:
        split_table = probability_table.loc[probability_table["data_split"].eq(split_name)].copy()
        if split_table.empty:
            payload["splits"][split_name] = {}
            continue
        split_payload: dict[str, object] = {}
        for lane_name in REPORTING_LANE_ORDER:
            lane_table = split_table.loc[split_table["reporting_lane"].eq(lane_name)].copy()
            if lane_table.empty:
                continue
            split_payload[lane_name] = summarize_calibration_slice(lane_table)
        if split_name in {"validation", "holdout"}:
            split_payload["mixed_info_only"] = summarize_calibration_slice(split_table)
        payload["splits"][split_name] = split_payload
    return payload


def build_manifest(
    *,
    row_labels_path: str,
    thresholds: dict[str, float],
    probability_table: pd.DataFrame,
) -> dict[str, object]:
    train_table = probability_table.loc[probability_table["row_used_for_fit"]].copy()
    return {
        "dataset_id": DATASET_ID,
        "scorecard_id": SCORECARD_ID,
        "baseline_seed_id": BASELINE_SEED_ID,
        "report_id": REPORT_ID,
        "model_family_id": MODEL_FAMILY_ID,
        "produced_by_stage": STAGE_NAME,
        "parser_version": PARSER_VERSION,
        "feature_order_hash": EXPECTED_FEATURE_ORDER_HASH,
        "row_labels_path": row_labels_path,
        "local_spec_ref": LOCAL_SPEC_REF,
        "decision_ref": DECISION_REF,
        "adr_ref": ADR_REF,
        "fit_lane": FIT_LANE,
        "model_type": "gaussian_naive_bayes",
        "class_order": TARGET_LABEL_ORDER,
        "probability_output_order": PROBABILITY_COLUMNS,
        "imputation_policy": "train_mean_fill_for_missing_features_before_inference_only",
        "frame_source": "build_feature_frame() rebuilt under the current parser identity because features.parquet excludes Tier B rows",
        "train_window": {
            "start": TRAIN_START_UTC.isoformat(),
            "end_inclusive": TRAIN_END_UTC.isoformat(),
            "readiness_tier": "tier_a",
            "row_count": int(len(train_table)),
        },
        "validation_window": {
            "start": VALIDATION_START_UTC.isoformat(),
            "end_inclusive": VALIDATION_END_UTC.isoformat(),
        },
        "holdout_window": {
            "start": HOLDOUT_START_UTC.isoformat(),
            "end_inclusive": HOLDOUT_END_UTC.isoformat(),
        },
        "label_rule": {
            "future_target": "future_log_return_1",
            "q33": thresholds["q33"],
            "q67": thresholds["q67"],
            "rule": "x <= q33 -> short; q33 < x < q67 -> flat; x >= q67 -> long",
        },
    }


def _format_class_balance(class_balance: dict[str, int]) -> str:
    return ", ".join(f"{label}={class_balance[label]}" for label in TARGET_LABEL_ORDER)


def _metric_row(split_name: str, lane_name: str, metrics: dict[str, object]) -> str:
    return (
        f"| {split_name} | {lane_name} | {metrics['row_count']} | {_format_class_balance(metrics['class_balance'])} | "
        f"{metrics['log_loss']:.6f} | {metrics['macro_f1']:.6f} | {metrics['balanced_accuracy']:.6f} | "
        f"{metrics['multiclass_brier_score']:.6f} | {metrics['rows_with_imputation']} | {metrics['mean_missing_feature_count']:.3f} |"
    )


def _calibration_line(split_name: str, lane_name: str, calibration: dict[str, object]) -> str:
    return (
        f"- `{split_name}` / `{lane_name}`: `ece={calibration['expected_calibration_error']:.6f}`, "
        f"`mean_max_probability={calibration['mean_max_probability']:.6f}`, "
        f"`observed_top_class_accuracy={calibration['observed_top_class_accuracy']:.6f}`"
    )


def render_report(
    *,
    manifest: dict[str, object],
    evaluation_summary: dict[str, object],
    calibration_read: dict[str, object],
    reviewed_on: str,
) -> str:
    lines = [
        "# Stage 06 First v2 Baseline Seed Review (Stage 06 첫 v2 기준선 시드 리뷰)",
        "",
        "## Identity (식별 정보)",
        f"- reviewed_on: `{reviewed_on}`",
        f"- stage: `{STAGE_NAME}`",
        f"- baseline_seed_id: `{BASELINE_SEED_ID}`",
        f"- report_id: `{REPORT_ID}`",
        f"- model_family_id: `{MODEL_FAMILY_ID}`",
        f"- local_spec_ref: `{LOCAL_SPEC_REF}`",
        f"- decision_ref: `{DECISION_REF}`",
        "",
        "## Boundary Read (경계 판독)",
        "- this pass keeps the current strict `Tier A (엄격 준비)` runtime rule unchanged and still treats `Tier B (부분 준비)` as `offline-only (오프라인 전용)` exploration work",
        "- no `reduced-risk runtime family (축소위험 런타임 계열)`, no `simulated execution (가상 실행)`, and no `operating promotion (운영 승격)` are materialized here",
        "- no legacy `model (모델)`, `threshold (임계값)`, or `calibration (보정)` artifact is inherited in this `v2-native baseline seed (v2 고유 기준선 시드)` pass",
        "- the model is fit on `Tier A (엄격 준비)` train rows only and evaluates `strict_tier_a (엄격 Tier A)` and `tier_b_exploration (Tier B 탐색)` on separate `reporting lanes (보고 레인)`",
        "",
        "## Label And Split Rule (라벨 및 분할 규칙)",
        f"- train window (학습 구간): `{manifest['train_window']['start']}` -> `{manifest['train_window']['end_inclusive']}` on `Tier A (엄격 준비)` only",
        f"- validation window (검증 구간): `{manifest['validation_window']['start']}` -> `{manifest['validation_window']['end_inclusive']}`",
        f"- holdout window (보류 평가 구간): `{manifest['holdout_window']['start']}` -> `{manifest['holdout_window']['end_inclusive']}`",
        f"- label rule (라벨 규칙): `q33={manifest['label_rule']['q33']:.12f}`, `q67={manifest['label_rule']['q67']:.12f}`, `{manifest['label_rule']['rule']}`",
        "- imputation policy (대치 규칙): missing features are filled with `Tier A train mean (Tier A 학습 평균)` before inference only",
        "",
        "## KPI Summary (핵심 지표 요약)",
        "| split (분할) | lane (레인) | row_count (행 수) | class_balance (클래스 분포) | log_loss (로그 손실) | macro_f1 (매크로 F1) | balanced_accuracy (균형 정확도) | multiclass_brier_score (다중분류 브라이어 점수) | imputed_rows (대치 행 수) | mean_missing_feature_count (평균 누락 특성 수) |",
        "| --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]

    for split_name in DATA_SPLIT_ORDER:
        split_payload = evaluation_summary["splits"].get(split_name, {})
        for lane_name in REPORTING_LANE_ORDER:
            metrics = split_payload.get(lane_name)
            if metrics is None:
                continue
            lines.append(_metric_row(split_name, lane_name, metrics))

    lines.extend(
        [
            "",
            "## Mixed Aggregate Info-Only (혼합 집계 정보용)",
        ]
    )
    for split_name in ("validation", "holdout"):
        mixed_metrics = evaluation_summary["splits"].get(split_name, {}).get("mixed_info_only")
        if mixed_metrics is None:
            continue
        lines.append(
            f"- `{split_name}`: row_count (행 수) `{mixed_metrics['row_count']}`, "
            f"log_loss (로그 손실) `{mixed_metrics['log_loss']:.6f}`, "
            f"macro_f1 (매크로 F1) `{mixed_metrics['macro_f1']:.6f}`, "
            f"balanced_accuracy (균형 정확도) `{mixed_metrics['balanced_accuracy']:.6f}`, "
            f"multiclass_brier_score (다중분류 브라이어 점수) `{mixed_metrics['multiclass_brier_score']:.6f}`"
        )

    lines.extend(
        [
            "",
            "## Calibration Read (보정 판독)",
        ]
    )
    for split_name in ("validation", "holdout"):
        split_payload = calibration_read["splits"].get(split_name, {})
        for lane_name in (*REPORTING_LANE_ORDER, "mixed_info_only"):
            calibration = split_payload.get(lane_name)
            if calibration is None:
                continue
            lines.append(_calibration_line(split_name, lane_name, calibration))

    lines.extend(
        [
            "",
            "## Notes (메모)",
            "- the first `Tier B offline evaluation report (Tier B 오프라인 평가 보고서)` now exists, but it remains a `stage-local read (단계 로컬 판독)` rather than a `promotion read (승격 판독)`",
            "- the first `calibration read (보정 판독)` is descriptive only; this pass does not fit a new `calibration model (보정 모델)`",
            "- a later packet must still decide whether the next narrow step is a `threshold read (임계값 판독)` or a `calibration fit (보정 적합)` follow-up",
        ]
    )
    return "\n".join(lines) + "\n"


def write_outputs(
    *,
    output_root: Path,
    report_path: Path,
    row_labels_path: Path,
    probability_table: pd.DataFrame,
    thresholds: dict[str, float],
    reviewed_on: str,
) -> dict[str, object]:
    output_root.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    manifest_path = output_root / MANIFEST_FILENAME
    probability_path = output_root / PROBABILITY_FILENAME
    summary_path = output_root / SUMMARY_FILENAME
    calibration_path = output_root / CALIBRATION_FILENAME

    manifest = build_manifest(
        row_labels_path=row_labels_path.as_posix(),
        thresholds=thresholds,
        probability_table=probability_table,
    )
    evaluation_summary = build_evaluation_summary(probability_table, row_labels_path=row_labels_path.as_posix())
    calibration_read = build_calibration_read(probability_table)
    report_text = render_report(
        manifest=manifest,
        evaluation_summary=evaluation_summary,
        calibration_read=calibration_read,
        reviewed_on=reviewed_on,
    )

    _write_text(manifest_path, json.dumps(manifest, indent=2))
    probability_table.to_parquet(_fs_path(probability_path), index=False)
    _write_text(summary_path, json.dumps(evaluation_summary, indent=2))
    _write_text(calibration_path, json.dumps(calibration_read, indent=2))
    _write_text(report_path, report_text, bom=True)

    return {
        "manifest_path": manifest_path.as_posix(),
        "probability_path": probability_path.as_posix(),
        "summary_path": summary_path.as_posix(),
        "calibration_path": calibration_path.as_posix(),
        "report_path": report_path.as_posix(),
        "manifest_sha256": sha256_file(manifest_path),
        "probability_sha256": sha256_file(probability_path),
        "summary_sha256": sha256_file(summary_path),
        "calibration_sha256": sha256_file(calibration_path),
        "report_sha256": sha256_file(report_path),
        "manifest": manifest,
        "evaluation_summary": evaluation_summary,
        "calibration_read": calibration_read,
    }


def main() -> int:
    args = parse_args()
    raw_root = Path(args.raw_root)
    row_labels_path = Path(args.row_labels_path)
    output_root = Path(args.output_root)
    report_path = Path(args.report_path)

    frame, _ = build_feature_frame(raw_root)
    row_labels = load_row_labels(row_labels_path)
    model_frame = build_model_frame(frame, row_labels)
    probability_table, thresholds = build_probability_table(model_frame)
    outputs = write_outputs(
        output_root=output_root,
        report_path=report_path,
        row_labels_path=row_labels_path,
        probability_table=probability_table,
        thresholds=thresholds,
        reviewed_on=args.reviewed_on,
    )

    payload = {
        "status": "ok",
        "dataset_id": DATASET_ID,
        "scorecard_id": SCORECARD_ID,
        "baseline_seed_id": BASELINE_SEED_ID,
        "report_id": REPORT_ID,
        "output_root": str(output_root.resolve()),
        "report_path": str(report_path.resolve()),
        "train_row_count": outputs["manifest"]["train_window"]["row_count"],
        "validation_tier_a_rows": outputs["evaluation_summary"]["splits"]["validation"]["strict_tier_a"]["row_count"],
        "validation_tier_b_rows": outputs["evaluation_summary"]["splits"]["validation"]["tier_b_exploration"]["row_count"],
        "holdout_tier_a_rows": outputs["evaluation_summary"]["splits"]["holdout"]["strict_tier_a"]["row_count"],
        "holdout_tier_b_rows": outputs["evaluation_summary"]["splits"]["holdout"]["tier_b_exploration"]["row_count"],
        "thresholds": thresholds,
        "hashes": {
            "manifest_sha256": outputs["manifest_sha256"],
            "probability_sha256": outputs["probability_sha256"],
            "summary_sha256": outputs["summary_sha256"],
            "calibration_sha256": outputs["calibration_sha256"],
            "report_sha256": outputs["report_sha256"],
        },
    }
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
