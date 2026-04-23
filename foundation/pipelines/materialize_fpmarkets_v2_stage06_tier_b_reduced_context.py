from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

try:
    from foundation.pipelines.materialize_fpmarkets_v2_dataset import (
        DATASET_ID,
        EXPECTED_FEATURE_ORDER_HASH,
        PARSER_VERSION,
        build_feature_frame,
    )
    from foundation.pipelines.materialize_fpmarkets_v2_tiered_readiness_scorecard import SCORECARD_ID
    from foundation.pipelines.materialize_fpmarkets_v2_stage06_v2_baseline_seed import (
        DATA_SPLIT_ORDER,
        HOLDOUT_END_UTC,
        HOLDOUT_START_UTC,
        PROBABILITY_COLUMNS,
        REPORTING_LANE_ORDER,
        TARGET_LABEL_ORDER,
        TRAIN_END_UTC,
        TRAIN_START_UTC,
        VALIDATION_END_UTC,
        VALIDATION_START_UTC,
        _fs_path,
        _write_text,
        assign_data_split,
        assign_target_label,
        fit_gaussian_nb,
        load_row_labels,
        predict_gaussian_nb,
        sha256_file,
        summarize_calibration_slice,
        summarize_probability_slice,
    )
except ModuleNotFoundError:
    dataset_module_path = Path(__file__).with_name("materialize_fpmarkets_v2_dataset.py")
    dataset_spec = importlib.util.spec_from_file_location(
        "materialize_fpmarkets_v2_dataset_for_stage06_reduced_context",
        dataset_module_path,
    )
    if dataset_spec is None or dataset_spec.loader is None:
        raise RuntimeError(f"Could not load dataset materializer from {dataset_module_path}")
    dataset_module = importlib.util.module_from_spec(dataset_spec)
    sys.modules[dataset_spec.name] = dataset_module
    dataset_spec.loader.exec_module(dataset_module)
    DATASET_ID = dataset_module.DATASET_ID
    EXPECTED_FEATURE_ORDER_HASH = dataset_module.EXPECTED_FEATURE_ORDER_HASH
    PARSER_VERSION = dataset_module.PARSER_VERSION
    build_feature_frame = dataset_module.build_feature_frame

    scorecard_module_path = Path(__file__).with_name("materialize_fpmarkets_v2_tiered_readiness_scorecard.py")
    scorecard_spec = importlib.util.spec_from_file_location(
        "materialize_fpmarkets_v2_tiered_readiness_scorecard_for_stage06_reduced_context",
        scorecard_module_path,
    )
    if scorecard_spec is None or scorecard_spec.loader is None:
        raise RuntimeError(f"Could not load scorecard materializer from {scorecard_module_path}")
    scorecard_module = importlib.util.module_from_spec(scorecard_spec)
    sys.modules[scorecard_spec.name] = scorecard_module
    scorecard_spec.loader.exec_module(scorecard_module)
    SCORECARD_ID = scorecard_module.SCORECARD_ID

    baseline_module_path = Path(__file__).with_name("materialize_fpmarkets_v2_stage06_v2_baseline_seed.py")
    baseline_spec = importlib.util.spec_from_file_location(
        "materialize_fpmarkets_v2_stage06_v2_baseline_seed_for_reduced_context",
        baseline_module_path,
    )
    if baseline_spec is None or baseline_spec.loader is None:
        raise RuntimeError(f"Could not load baseline seed materializer from {baseline_module_path}")
    baseline_module = importlib.util.module_from_spec(baseline_spec)
    sys.modules[baseline_spec.name] = baseline_module
    baseline_spec.loader.exec_module(baseline_module)
    DATA_SPLIT_ORDER = baseline_module.DATA_SPLIT_ORDER
    HOLDOUT_END_UTC = baseline_module.HOLDOUT_END_UTC
    HOLDOUT_START_UTC = baseline_module.HOLDOUT_START_UTC
    PROBABILITY_COLUMNS = baseline_module.PROBABILITY_COLUMNS
    REPORTING_LANE_ORDER = baseline_module.REPORTING_LANE_ORDER
    TARGET_LABEL_ORDER = baseline_module.TARGET_LABEL_ORDER
    TRAIN_END_UTC = baseline_module.TRAIN_END_UTC
    TRAIN_START_UTC = baseline_module.TRAIN_START_UTC
    VALIDATION_END_UTC = baseline_module.VALIDATION_END_UTC
    VALIDATION_START_UTC = baseline_module.VALIDATION_START_UTC
    _fs_path = baseline_module._fs_path
    _write_text = baseline_module._write_text
    assign_data_split = baseline_module.assign_data_split
    assign_target_label = baseline_module.assign_target_label
    fit_gaussian_nb = baseline_module.fit_gaussian_nb
    load_row_labels = baseline_module.load_row_labels
    predict_gaussian_nb = baseline_module.predict_gaussian_nb
    sha256_file = baseline_module.sha256_file
    summarize_calibration_slice = baseline_module.summarize_calibration_slice
    summarize_probability_slice = baseline_module.summarize_probability_slice


STAGE_NAME = "06_tiered_readiness_exploration"
RUN_ID = "tier_b_reduced_context_0001"
REDUCED_CONTEXT_ID = "reduced_context_model_fpmarkets_v2_tier_b_0001"
REPORT_ID = "report_fpmarkets_v2_tier_b_reduced_context_0001"
MODEL_FAMILY_ID = "gaussian_nb_3class_tier_b_reduced_context_keep42_0001"
FIT_LANE = "strict_tier_a_only_reduced_context_keep42"
LOCAL_SPEC_REF = "stages/06_tiered_readiness_exploration/01_inputs/stage06_tier_b_reduced_context_local_spec.md@2026-04-22"
SCHEMA_REF = "stages/06_tiered_readiness_exploration/01_inputs/stage06_tier_b_safe_feature_schema_draft_0001.md@2026-04-22"
ANCHOR_REF = "stages/06_tiered_readiness_exploration/03_reviews/note_fpmarkets_v2_tier_b_reduced_context_model_anchor_0001.md@2026-04-22"
BASELINE_SUMMARY_REF = (
    "stages/06_tiered_readiness_exploration/02_runs/tier_b_offline_eval_0001/"
    "baseline_evaluation_summary_fpmarkets_v2_tier_b_offline_eval_0001.json"
)
DECISION_REF = "docs/decisions/2026-04-22_stage06_v2_baseline_seed_first.md@2026-04-22"
ADR_REF = "docs/adr/0003_tier_b_reduced_risk_experiment_charter.md@2026-04-22"

MANIFEST_FILENAME = "reduced_context_manifest_fpmarkets_v2_tier_b_reduced_context_0001.json"
PROBABILITY_FILENAME = "reduced_context_probability_table_fpmarkets_v2_tier_b_reduced_context_0001.parquet"
SUMMARY_FILENAME = "reduced_context_evaluation_summary_fpmarkets_v2_tier_b_reduced_context_0001.json"
CALIBRATION_FILENAME = "reduced_context_calibration_read_fpmarkets_v2_tier_b_reduced_context_0001.json"
DEFAULT_OUTPUT_ROOT = Path("stages/06_tiered_readiness_exploration/02_runs/tier_b_reduced_context_0001")
DEFAULT_REPORT_PATH = Path(
    "stages/06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tier_b_reduced_context_0001.md"
)
DEFAULT_ROW_LABELS_PATH = Path(
    "stages/06_tiered_readiness_exploration/02_runs/tiered_readiness_scorecard_0001/"
    "readiness_row_labels_fpmarkets_v2_tiered_readiness_0001.parquet"
)
DEFAULT_BASELINE_SUMMARY_PATH = Path(BASELINE_SUMMARY_REF)

ACTIVE_FEATURES = [
    "log_return_1",
    "log_return_3",
    "hl_range",
    "close_open_ratio",
    "gap_percent",
    "close_prev_close_ratio",
    "return_zscore_20",
    "hl_zscore_50",
    "return_1_over_atr_14",
    "close_ema20_ratio",
    "close_ema50_ratio",
    "ema9_ema20_diff",
    "ema20_ema50_diff",
    "ema50_ema200_diff",
    "ema20_ema50_spread_zscore_50",
    "sma50_sma200_ratio",
    "rsi_14",
    "rsi_50",
    "rsi_14_slope_3",
    "rsi_14_minus_50",
    "stoch_kd_diff",
    "stochrsi_kd_diff",
    "ppo_hist_12_26_9",
    "roc_12",
    "trix_15",
    "atr_14",
    "atr_50",
    "atr_14_over_atr_50",
    "bollinger_width_20",
    "bb_position_20",
    "bb_squeeze",
    "historical_vol_20",
    "historical_vol_5_over_20",
    "adx_14",
    "di_spread_14",
    "supertrend_10_3",
    "vortex_indicator",
    "overnight_return",
    "is_us_cash_open",
    "minutes_from_cash_open",
    "is_first_30m_after_open",
    "is_last_30m_before_cash_close",
]
CONDITIONAL_FEATURES = [
    "vix_change_1",
    "vix_zscore_20",
    "us10yr_change_1",
    "us10yr_zscore_20",
    "usdx_change_1",
    "usdx_zscore_20",
]
DROPPED_FEATURES = [
    "nvda_xnas_log_return_1",
    "aapl_xnas_log_return_1",
    "msft_xnas_log_return_1",
    "amzn_xnas_log_return_1",
    "mega8_equal_return_1",
    "top3_weighted_return_1",
    "mega8_pos_breadth_1",
    "mega8_dispersion_5",
    "us100_minus_mega8_equal_return_1",
    "us100_minus_top3_weighted_return_1",
]
SUBTYPE_ORDER = ["b_eq_dark", "b_macro_late", "b_residual_sparse"]
TARGET_TO_INDEX = {label: index for index, label in enumerate(TARGET_LABEL_ORDER)}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Materialize the first Stage 06 Tier B reduced-context model artifacts."
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
        "--baseline-summary-path",
        default=str(DEFAULT_BASELINE_SUMMARY_PATH),
        help="Repo-relative baseline evaluation summary used for info-only comparison.",
    )
    parser.add_argument(
        "--output-root",
        default=str(DEFAULT_OUTPUT_ROOT),
        help="Repo-relative output root for the reduced-context artifacts.",
    )
    parser.add_argument(
        "--report-path",
        default=str(DEFAULT_REPORT_PATH),
        help="Repo-relative output path for the rendered reduced-context report.",
    )
    parser.add_argument(
        "--reviewed-on",
        default=pd.Timestamp.now(tz="Asia/Seoul").date().isoformat(),
        help="Review date to stamp into the rendered report.",
    )
    return parser.parse_args()


def load_baseline_summary(path: Path) -> dict[str, object]:
    with open(_fs_path(path), "r", encoding="utf-8") as handle:
        return json.load(handle)


def assign_tier_b_subtype_tag(*, readiness_tier: str, missing_groups: str) -> str | None:
    if readiness_tier != "tier_b":
        return None
    if missing_groups == "g4_leader_equity|g5_breadth_extension":
        return "b_eq_dark"
    if missing_groups == "g3_macro_proxy":
        return "b_macro_late"
    return "b_residual_sparse"


def build_model_frame(frame: pd.DataFrame, row_labels: pd.DataFrame) -> pd.DataFrame:
    merged = frame[["timestamp", "close", *ACTIVE_FEATURES]].merge(
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
    merged["row_pre_imputation_nan_count"] = merged[ACTIVE_FEATURES].isna().sum(axis=1).astype("int64")
    merged["row_received_imputation"] = merged["row_pre_imputation_nan_count"].gt(0)
    merged["tier_b_subtype_tag"] = [
        assign_tier_b_subtype_tag(readiness_tier=tier, missing_groups=groups)
        for tier, groups in zip(
            merged["readiness_tier"].astype(str).tolist(),
            merged["missing_groups"].fillna("").astype(str).tolist(),
            strict=True,
        )
    ]
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


def build_probability_table(frame: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, float]]:
    train_rows = training_mask(frame)
    train_returns = frame.loc[train_rows, "future_log_return_1"]
    if train_returns.empty:
        raise RuntimeError("No Tier A training rows were available for the reduced-context pass.")

    q33 = float(train_returns.quantile(0.33))
    q67 = float(train_returns.quantile(0.67))

    model_frame = frame.copy()
    model_frame["target_label"] = model_frame["future_log_return_1"].map(
        lambda value: assign_target_label(value, q33=q33, q67=q67) if pd.notna(value) else None
    )
    model_frame["target_index"] = model_frame["target_label"].map(TARGET_TO_INDEX)

    train_feature_means = model_frame.loc[train_rows, ACTIVE_FEATURES].mean()
    feature_matrix = model_frame[ACTIVE_FEATURES].fillna(train_feature_means)

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
            "missing_groups",
            "missing_symbols",
            "tier_b_subtype_tag",
            "data_split",
            "fit_lane",
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
        "tier_b_subtype_tag",
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


def build_baseline_comparison(
    summary: dict[str, object],
    *,
    baseline_summary: dict[str, object],
) -> dict[str, object]:
    comparison: dict[str, object] = {}
    for split_name in ("validation", "holdout"):
        current_split = summary["splits"].get(split_name, {})
        baseline_split = baseline_summary.get("splits", {}).get(split_name, {})
        split_payload: dict[str, object] = {}
        for lane_name in REPORTING_LANE_ORDER:
            current_metrics = current_split.get(lane_name)
            baseline_metrics = baseline_split.get(lane_name)
            if current_metrics is None or baseline_metrics is None:
                continue
            split_payload[lane_name] = {
                "log_loss_delta_vs_full_baseline": float(current_metrics["log_loss"] - baseline_metrics["log_loss"]),
                "macro_f1_delta_vs_full_baseline": float(current_metrics["macro_f1"] - baseline_metrics["macro_f1"]),
                "balanced_accuracy_delta_vs_full_baseline": float(
                    current_metrics["balanced_accuracy"] - baseline_metrics["balanced_accuracy"]
                ),
                "multiclass_brier_score_delta_vs_full_baseline": float(
                    current_metrics["multiclass_brier_score"] - baseline_metrics["multiclass_brier_score"]
                ),
            }
        comparison[split_name] = split_payload
    return comparison


def build_tier_b_subtype_summary(probability_table: pd.DataFrame) -> dict[str, object]:
    payload: dict[str, object] = {}
    for split_name in ("validation", "holdout"):
        split_table = probability_table.loc[
            probability_table["data_split"].eq(split_name) & probability_table["reporting_lane"].eq("tier_b_exploration")
        ].copy()
        subtype_payload: dict[str, object] = {}
        if split_table.empty:
            payload[split_name] = subtype_payload
            continue
        for subtype_tag in SUBTYPE_ORDER:
            subtype_table = split_table.loc[split_table["tier_b_subtype_tag"].eq(subtype_tag)].copy()
            if subtype_table.empty:
                continue
            metrics = summarize_probability_slice(subtype_table)
            metrics["row_share_within_tier_b"] = float(len(subtype_table) / len(split_table))
            subtype_payload[subtype_tag] = metrics
        payload[split_name] = subtype_payload
    return payload


def build_evaluation_summary(
    probability_table: pd.DataFrame,
    *,
    row_labels_path: str,
    baseline_summary: dict[str, object],
) -> dict[str, object]:
    summary = {
        "dataset_id": DATASET_ID,
        "scorecard_id": SCORECARD_ID,
        "reduced_context_id": REDUCED_CONTEXT_ID,
        "report_id": REPORT_ID,
        "model_family_id": MODEL_FAMILY_ID,
        "produced_by_stage": STAGE_NAME,
        "parser_version": PARSER_VERSION,
        "feature_order_hash": EXPECTED_FEATURE_ORDER_HASH,
        "row_labels_path": row_labels_path,
        "baseline_summary_ref": BASELINE_SUMMARY_REF,
        "local_spec_ref": LOCAL_SPEC_REF,
        "schema_ref": SCHEMA_REF,
        "anchor_ref": ANCHOR_REF,
        "decision_ref": DECISION_REF,
        "adr_ref": ADR_REF,
        "fit_lane": FIT_LANE,
        "probability_output_order": PROBABILITY_COLUMNS,
        "feature_schema": {
            "active_feature_count": len(ACTIVE_FEATURES),
            "conditional_feature_count": len(CONDITIONAL_FEATURES),
            "dropped_feature_count": len(DROPPED_FEATURES),
            "active_feature_names": ACTIVE_FEATURES,
            "conditional_feature_names": CONDITIONAL_FEATURES,
            "dropped_feature_names": DROPPED_FEATURES,
        },
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

    summary["comparison_to_full_baseline_seed"] = build_baseline_comparison(
        summary,
        baseline_summary=baseline_summary,
    )
    summary["tier_b_subtype_info_only"] = build_tier_b_subtype_summary(probability_table)
    return summary


def build_calibration_read(probability_table: pd.DataFrame) -> dict[str, object]:
    payload = {
        "reduced_context_id": REDUCED_CONTEXT_ID,
        "report_id": REPORT_ID,
        "model_family_id": MODEL_FAMILY_ID,
        "calibration_mode": "read_only",
        "confidence_column": "max_probability",
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
        "reduced_context_id": REDUCED_CONTEXT_ID,
        "report_id": REPORT_ID,
        "model_family_id": MODEL_FAMILY_ID,
        "produced_by_stage": STAGE_NAME,
        "parser_version": PARSER_VERSION,
        "feature_order_hash": EXPECTED_FEATURE_ORDER_HASH,
        "row_labels_path": row_labels_path,
        "baseline_summary_ref": BASELINE_SUMMARY_REF,
        "local_spec_ref": LOCAL_SPEC_REF,
        "schema_ref": SCHEMA_REF,
        "anchor_ref": ANCHOR_REF,
        "decision_ref": DECISION_REF,
        "adr_ref": ADR_REF,
        "fit_lane": FIT_LANE,
        "model_type": "gaussian_naive_bayes",
        "class_order": TARGET_LABEL_ORDER,
        "probability_output_order": PROBABILITY_COLUMNS,
        "active_feature_names": ACTIVE_FEATURES,
        "conditional_feature_names": CONDITIONAL_FEATURES,
        "dropped_feature_names": DROPPED_FEATURES,
        "subtype_tag_order": SUBTYPE_ORDER,
        "imputation_policy": "train_mean_fill_for_active_features_before_inference_only",
        "frame_source": "build_feature_frame() rebuilt under the current parser identity and restricted to the first shared Tier B-safe active feature set",
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


def _delta_line(split_name: str, lane_name: str, deltas: dict[str, object]) -> str:
    return (
        f"- `{split_name}` / `{lane_name}`: "
        f"`delta_log_loss={deltas['log_loss_delta_vs_full_baseline']:.6f}`, "
        f"`delta_macro_f1={deltas['macro_f1_delta_vs_full_baseline']:.6f}`, "
        f"`delta_balanced_accuracy={deltas['balanced_accuracy_delta_vs_full_baseline']:.6f}`, "
        f"`delta_brier={deltas['multiclass_brier_score_delta_vs_full_baseline']:.6f}`"
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
        "# Stage 06 First Tier B Reduced-Context Model Review (Stage 06 첫 Tier B 축약 문맥 모델 검토)",
        "",
        "## Identity (식별 정보)",
        f"- reviewed_on: `{reviewed_on}`",
        f"- stage: `{STAGE_NAME}`",
        f"- reduced_context_id: `{REDUCED_CONTEXT_ID}`",
        f"- report_id: `{REPORT_ID}`",
        f"- model_family_id: `{MODEL_FAMILY_ID}`",
        f"- local_spec_ref: `{LOCAL_SPEC_REF}`",
        f"- schema_ref: `{SCHEMA_REF}`",
        f"- anchor_ref: `{ANCHOR_REF}`",
        "",
        "## Boundary Read (경계 판독)",
        "- this pass materializes the first shared `Tier B reduced-context model (Tier B 공용 축약 문맥 모델)` while keeping all meaning `offline-only (오프라인 전용)`",
        "- no `Stage 07 open (Stage 07 개시)`, no `simulated execution (가상 실행)`, no `MT5 path (MT5 경로)`, and no `operating promotion (운영 승격)` meaning is claimed here",
        "- the current `strict Tier A runtime rule (엄격 Tier A 런타임 규칙)` remains unchanged",
        "- the first shared reduced-context active set uses `42` `keep (유지)` features only and keeps all `conditional (조건부)` macro features out of this pass",
        "",
        "## Feature Schema (피처 스키마)",
        f"- active feature count (활성 피처 수): `{len(ACTIVE_FEATURES)}`",
        f"- conditional feature count (조건부 피처 수): `{len(CONDITIONAL_FEATURES)}`",
        f"- dropped feature count (제외 피처 수): `{len(DROPPED_FEATURES)}`",
        f"- deferred macro family (보류 매크로 계열): `{', '.join(CONDITIONAL_FEATURES)}`",
        f"- dropped external family (제외 외부 계열): `{', '.join(DROPPED_FEATURES)}`",
        "",
        "## KPI Summary (핵심 지표 요약)",
        "| split (분할) | lane (레인) | row_count (행 수) | class_balance (클래스 분포) | log_loss (로그 손실) | macro_f1 (매크로 F1) | balanced_accuracy (균형 정확도) | multiclass_brier_score (다중분류 브라이어 점수) | imputed_rows (대치 행 수) | mean_missing_feature_count (평균 누락 피처 수) |",
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
            "## Comparison To Full Baseline Seed (전체 기준선 시드 대비 비교)",
        ]
    )
    for split_name in ("validation", "holdout"):
        split_payload = evaluation_summary["comparison_to_full_baseline_seed"].get(split_name, {})
        for lane_name in REPORTING_LANE_ORDER:
            deltas = split_payload.get(lane_name)
            if deltas is None:
                continue
            lines.append(_delta_line(split_name, lane_name, deltas))

    lines.extend(
        [
            "",
            "## Tier B Subtype Info-Only (Tier B 하위유형 정보용)",
        ]
    )
    for split_name in ("validation", "holdout"):
        subtype_payload = evaluation_summary["tier_b_subtype_info_only"].get(split_name, {})
        for subtype_tag in SUBTYPE_ORDER:
            metrics = subtype_payload.get(subtype_tag)
            if metrics is None:
                continue
            lines.append(
                f"- `{split_name}` / `{subtype_tag}`: "
                f"`row_count={metrics['row_count']}`, "
                f"`row_share_within_tier_b={metrics['row_share_within_tier_b']:.6f}`, "
                f"`log_loss={metrics['log_loss']:.6f}`, "
                f"`macro_f1={metrics['macro_f1']:.6f}`, "
                f"`balanced_accuracy={metrics['balanced_accuracy']:.6f}`"
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
            "- this report is a `Stage 06 local read (Stage 06 로컬 판독)` only and does not update `workspace_state.yaml`, `current_working_state.md`, or the active `selection_status.md` by itself",
            "- the first shared reduced-context model answers whether the `keep=42` feature surface is worth carrying forward before any optional `macro-aware (매크로 인지)` variant is opened",
            "- any later threshold policy, control search, simulated execution, or `MT5` feasibility read still needs a separate explicit decision layer",
        ]
    )
    return "\n".join(lines) + "\n"


def write_outputs(
    *,
    output_root: Path,
    report_path: Path,
    row_labels_path: Path,
    baseline_summary: dict[str, object],
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
    evaluation_summary = build_evaluation_summary(
        probability_table,
        row_labels_path=row_labels_path.as_posix(),
        baseline_summary=baseline_summary,
    )
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
    baseline_summary_path = Path(args.baseline_summary_path)
    output_root = Path(args.output_root)
    report_path = Path(args.report_path)

    frame, _ = build_feature_frame(raw_root)
    row_labels = load_row_labels(row_labels_path)
    baseline_summary = load_baseline_summary(baseline_summary_path)
    model_frame = build_model_frame(frame, row_labels)
    probability_table, thresholds = build_probability_table(model_frame)
    outputs = write_outputs(
        output_root=output_root,
        report_path=report_path,
        row_labels_path=row_labels_path,
        baseline_summary=baseline_summary,
        probability_table=probability_table,
        thresholds=thresholds,
        reviewed_on=args.reviewed_on,
    )

    holdout_tier_b = outputs["evaluation_summary"]["splits"]["holdout"]["tier_b_exploration"]
    holdout_delta = outputs["evaluation_summary"]["comparison_to_full_baseline_seed"]["holdout"]["tier_b_exploration"]
    payload = {
        "status": "ok",
        "dataset_id": DATASET_ID,
        "scorecard_id": SCORECARD_ID,
        "reduced_context_id": REDUCED_CONTEXT_ID,
        "report_id": REPORT_ID,
        "output_root": str(output_root.resolve()),
        "report_path": str(report_path.resolve()),
        "active_feature_count": len(ACTIVE_FEATURES),
        "conditional_feature_count": len(CONDITIONAL_FEATURES),
        "dropped_feature_count": len(DROPPED_FEATURES),
        "train_row_count": outputs["manifest"]["train_window"]["row_count"],
        "holdout_tier_b_log_loss": holdout_tier_b["log_loss"],
        "holdout_tier_b_macro_f1": holdout_tier_b["macro_f1"],
        "holdout_tier_b_delta_log_loss_vs_full_baseline": holdout_delta["log_loss_delta_vs_full_baseline"],
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
