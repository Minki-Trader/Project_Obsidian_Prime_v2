from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

try:
    from foundation.pipelines import materialize_fpmarkets_v2_stage06_v2_baseline_seed as baseline
except ModuleNotFoundError:
    baseline_module_path = Path(__file__).with_name("materialize_fpmarkets_v2_stage06_v2_baseline_seed.py")
    baseline_spec = importlib.util.spec_from_file_location(
        "materialize_fpmarkets_v2_stage06_v2_baseline_seed_for_followup_pack",
        baseline_module_path,
    )
    if baseline_spec is None or baseline_spec.loader is None:
        raise RuntimeError(f"Could not load baseline seed pipeline from {baseline_module_path}")
    baseline = importlib.util.module_from_spec(baseline_spec)
    sys.modules[baseline_spec.name] = baseline
    baseline_spec.loader.exec_module(baseline)


STAGE_NAME = "06_tiered_readiness_exploration"
RUN_ID = "tier_b_followup_pack_0001"
FOLLOWUP_PACK_ID = "followup_pack_fpmarkets_v2_tier_b_0001"
FOLLOWUP_BUNDLE_ID = "bundle_fpmarkets_v2_stage06_followup_pack_0001"
FOLLOWUP_LOCAL_SPEC_REF = "stages/06_tiered_readiness_exploration/01_inputs/stage06_v2_followup_pack_local_spec.md@2026-04-22"
BASELINE_DECISION_REF = "docs/decisions/2026-04-22_stage06_v2_baseline_seed_first.md@2026-04-22"
FOLLOWUP_ADR_REF = "docs/adr/0003_tier_b_reduced_risk_experiment_charter.md@2026-04-22"

FOLLOWUP_MANIFEST_FILENAME = "followup_pack_manifest_fpmarkets_v2_tier_b_followup_pack_0001.json"
CALIBRATION_SUMMARY_FILENAME = "tier_b_calibration_fit_summary_fpmarkets_v2_tier_b_followup_pack_0001.json"
CONTROL_SUMMARY_FILENAME = "tier_b_control_sensitivity_summary_fpmarkets_v2_tier_b_followup_pack_0001.json"
ROBUSTNESS_SUMMARY_FILENAME = "tier_b_robustness_summary_fpmarkets_v2_tier_b_followup_pack_0001.json"
WEIGHT_SUMMARY_FILENAME = "tier_b_weight_verdict_summary_fpmarkets_v2_tier_b_followup_pack_0001.json"

CALIBRATION_REPORT_FILENAME = "report_fpmarkets_v2_tier_b_calibration_fit_0001.md"
CONTROL_REPORT_FILENAME = "report_fpmarkets_v2_tier_b_control_sensitivity_0001.md"
ROBUSTNESS_REPORT_FILENAME = "report_fpmarkets_v2_tier_b_robustness_0001.md"
WEIGHT_REPORT_FILENAME = "report_fpmarkets_v2_tier_b_weight_verdict_0001.md"
STAGE07_DRAFT_FILENAME = "stage07_alpha_design_draft_0001.md"
CLOSE_OPEN_DRAFT_FILENAME = "stage06_close_stage07_open_readout_draft_0001.md"

DEFAULT_OUTPUT_ROOT = Path("stages/06_tiered_readiness_exploration/02_runs/tier_b_followup_pack_0001")
DEFAULT_REVIEWS_ROOT = Path("stages/06_tiered_readiness_exploration/03_reviews")
DEFAULT_ROW_LABELS_PATH = baseline.DEFAULT_ROW_LABELS_PATH

TEMPERATURE_GRID = tuple(
    float(value)
    for value in np.concatenate(
        [
            np.linspace(0.5, 5.0, 19),
            np.linspace(6.0, 20.0, 15),
            np.asarray([25.0, 30.0, 40.0, 50.0], dtype=np.float64),
        ]
    )
)
ENTRY_THRESHOLD_GRID = (0.35, 0.40, 0.45, 0.50, 0.55)
EXPOSURE_CAP_GRID = (0.25, 0.50, 0.75)
RISK_SIZE_GRID = (0.50, 0.75, 1.00)
WEIGHT_SCENARIOS: dict[str, dict[str, float]] = {
    "equal_placeholder": {
        "msft_xnas_weight": 1.0 / 3.0,
        "nvda_xnas_weight": 1.0 / 3.0,
        "aapl_xnas_weight": 1.0 / 3.0,
    },
    "nvda_tilt_60": {
        "msft_xnas_weight": 0.20,
        "nvda_xnas_weight": 0.60,
        "aapl_xnas_weight": 0.20,
    },
    "msft_tilt_60": {
        "msft_xnas_weight": 0.60,
        "nvda_xnas_weight": 0.20,
        "aapl_xnas_weight": 0.20,
    },
    "aapl_tilt_60": {
        "msft_xnas_weight": 0.20,
        "nvda_xnas_weight": 0.20,
        "aapl_xnas_weight": 0.60,
    },
}
MISSING_PATTERN_ORDER = [
    "g3_macro_proxy",
    "g4_leader_equity|g5_breadth_extension",
    "g5_breadth_extension",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Materialize the Stage 06 additive follow-up pack without reflecting official stage decisions."
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
        help="Repo-relative output root for the follow-up pack JSON artifacts.",
    )
    parser.add_argument(
        "--reviews-root",
        default=str(DEFAULT_REVIEWS_ROOT),
        help="Repo-relative output root for rendered review and draft markdown files.",
    )
    parser.add_argument(
        "--reviewed-on",
        default=pd.Timestamp.now(tz="Asia/Seoul").date().isoformat(),
        help="Review date to stamp into the rendered reports.",
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


def _to_builtin(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _to_builtin(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_to_builtin(item) for item in value]
    if isinstance(value, tuple):
        return [_to_builtin(item) for item in value]
    if isinstance(value, (np.floating,)):
        return float(value)
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.bool_,)):
        return bool(value)
    return value


def summarize_probability_arrays(labels: np.ndarray, probabilities: np.ndarray) -> dict[str, object]:
    labels = labels.astype(np.int64, copy=False)
    probabilities = probabilities.astype(np.float64, copy=False)
    predictions = probabilities.argmax(axis=1).astype(np.int64, copy=False)
    calibration_table = pd.DataFrame(
        {
            "target_index": labels,
            "predicted_index": predictions,
            "p_short": probabilities[:, 0],
            "p_flat": probabilities[:, 1],
            "p_long": probabilities[:, 2],
        }
    )
    calibration = baseline.summarize_calibration_slice(calibration_table)
    return {
        "row_count": int(len(labels)),
        "log_loss": baseline.multiclass_log_loss(labels, probabilities),
        "macro_f1": baseline.macro_f1_score(labels, predictions),
        "balanced_accuracy": baseline.balanced_accuracy_score(labels, predictions),
        "multiclass_brier_score": baseline.multiclass_brier_score(labels, probabilities),
        "mean_max_probability": calibration["mean_max_probability"],
        "observed_top_class_accuracy": calibration["observed_top_class_accuracy"],
        "expected_calibration_error": calibration["expected_calibration_error"],
    }


def temperature_scale_probabilities(probabilities: np.ndarray, temperature: float) -> np.ndarray:
    if temperature <= 0:
        raise RuntimeError(f"Temperature must stay positive, got {temperature}")
    logits = np.log(np.clip(probabilities.astype(np.float64, copy=False), 1e-12, 1.0)) / temperature
    logits -= logits.max(axis=1, keepdims=True)
    scaled = np.exp(logits)
    scaled /= scaled.sum(axis=1, keepdims=True)
    return scaled


def fit_temperature_for_slice(probability_table: pd.DataFrame) -> dict[str, object]:
    if probability_table.empty:
        raise RuntimeError("Calibration fit requested on an empty probability slice.")
    labels = probability_table["target_index"].to_numpy(dtype=np.int64, copy=False)
    probabilities = probability_table[baseline.PROBABILITY_COLUMNS].to_numpy(dtype=np.float64, copy=False)
    best_temperature = 1.0
    best_log_loss = baseline.multiclass_log_loss(labels, probabilities)
    for candidate in TEMPERATURE_GRID:
        scaled = temperature_scale_probabilities(probabilities, candidate)
        candidate_log_loss = baseline.multiclass_log_loss(labels, scaled)
        if candidate_log_loss < best_log_loss:
            best_temperature = float(candidate)
            best_log_loss = float(candidate_log_loss)
    return {
        "temperature": float(best_temperature),
        "objective": "validation_multiclass_log_loss",
        "fit_row_count": int(len(probability_table)),
        "fit_metrics": summarize_probability_arrays(
            labels,
            temperature_scale_probabilities(probabilities, best_temperature),
        ),
    }


def build_calibration_fit_summary(probability_table: pd.DataFrame) -> dict[str, object]:
    candidate_specs: dict[str, dict[str, object]] = {
        "identity_read_only": {
            "temperature": 1.0,
            "fit_split": None,
            "fit_lane": None,
            "fit_row_count": 0,
            "objective": "read_only",
        }
    }
    for lane_name in baseline.REPORTING_LANE_ORDER:
        fit_table = probability_table.loc[
            probability_table["data_split"].eq("validation") & probability_table["reporting_lane"].eq(lane_name)
        ].copy()
        candidate_name = f"{lane_name}_temperature_fit"
        candidate_specs[candidate_name] = {
            **fit_temperature_for_slice(fit_table),
            "fit_split": "validation",
            "fit_lane": lane_name,
        }

    evaluation: dict[str, dict[str, dict[str, object]]] = {}
    for split_name in ("validation", "holdout"):
        split_payload: dict[str, dict[str, object]] = {}
        split_table = probability_table.loc[probability_table["data_split"].eq(split_name)].copy()
        for lane_name in baseline.REPORTING_LANE_ORDER:
            lane_table = split_table.loc[split_table["reporting_lane"].eq(lane_name)].copy()
            if lane_table.empty:
                continue
            labels = lane_table["target_index"].to_numpy(dtype=np.int64, copy=False)
            base_probabilities = lane_table[baseline.PROBABILITY_COLUMNS].to_numpy(dtype=np.float64, copy=False)
            lane_payload: dict[str, object] = {}
            for candidate_name, spec in candidate_specs.items():
                scaled = temperature_scale_probabilities(base_probabilities, float(spec["temperature"]))
                lane_payload[candidate_name] = summarize_probability_arrays(labels, scaled)
            split_payload[lane_name] = lane_payload
        evaluation[split_name] = split_payload

    tier_b_holdout = evaluation["holdout"]["tier_b_exploration"]
    tier_a_holdout = evaluation["holdout"]["strict_tier_a"]
    draft_takeaway = {
        "tier_b_reuse_check": (
            "tier_b_temperature_fit improves holdout log_loss and expected_calibration_error over "
            "strict_tier_a_temperature_fit on tier_b_exploration"
            if (
                tier_b_holdout["tier_b_exploration_temperature_fit"]["log_loss"]
                < tier_b_holdout["strict_tier_a_temperature_fit"]["log_loss"]
                and tier_b_holdout["tier_b_exploration_temperature_fit"]["expected_calibration_error"]
                < tier_b_holdout["strict_tier_a_temperature_fit"]["expected_calibration_error"]
            )
            else "tier_b_reuse_check_inconclusive"
        ),
        "tier_a_calibration_takeaway": (
            "strict_tier_a_temperature_fit improves the strict_tier_a holdout calibration read without changing class prediction order"
            if tier_a_holdout["strict_tier_a_temperature_fit"]["log_loss"]
            < tier_a_holdout["identity_read_only"]["log_loss"]
            else "strict_tier_a_followup_not_improved"
        ),
    }
    return {
        "dataset_id": baseline.DATASET_ID,
        "scorecard_id": baseline.SCORECARD_ID,
        "baseline_seed_id": baseline.BASELINE_SEED_ID,
        "followup_pack_id": FOLLOWUP_PACK_ID,
        "report_id": "report_fpmarkets_v2_tier_b_calibration_fit_0001",
        "model_family_id": baseline.MODEL_FAMILY_ID,
        "produced_by_stage": STAGE_NAME,
        "parser_version": baseline.PARSER_VERSION,
        "feature_order_hash": baseline.EXPECTED_FEATURE_ORDER_HASH,
        "local_spec_ref": FOLLOWUP_LOCAL_SPEC_REF,
        "decision_ref": BASELINE_DECISION_REF,
        "adr_ref": FOLLOWUP_ADR_REF,
        "temperature_grid": list(TEMPERATURE_GRID),
        "fit_candidates": _to_builtin(candidate_specs),
        "evaluation": _to_builtin(evaluation),
        "draft_takeaway": draft_takeaway,
    }


def apply_lane_specific_temperature(probability_table: pd.DataFrame, calibration_summary: dict[str, object]) -> pd.DataFrame:
    lane_temperatures = {
        lane_name: float(
            calibration_summary["fit_candidates"][f"{lane_name}_temperature_fit"]["temperature"]
        )
        for lane_name in baseline.REPORTING_LANE_ORDER
    }
    adjusted = probability_table.copy()
    for lane_name, temperature in lane_temperatures.items():
        lane_mask = adjusted["reporting_lane"].eq(lane_name)
        lane_probabilities = adjusted.loc[lane_mask, baseline.PROBABILITY_COLUMNS].to_numpy(dtype=np.float64, copy=False)
        scaled = temperature_scale_probabilities(lane_probabilities, temperature)
        for column_name, values in zip(baseline.PROBABILITY_COLUMNS, scaled.T, strict=True):
            adjusted.loc[lane_mask, column_name] = values
        adjusted.loc[lane_mask, "predicted_index"] = scaled.argmax(axis=1).astype(np.int64)
    adjusted["predicted_index"] = adjusted["predicted_index"].astype(np.int64)
    adjusted["predicted_label"] = [
        baseline.TARGET_LABEL_ORDER[index] for index in adjusted["predicted_index"].to_list()
    ]
    return adjusted


def compute_proxy_control_metrics(
    probability_table: pd.DataFrame,
    *,
    entry_threshold: float,
    exposure_cap: float,
    risk_size_multiplier: float,
) -> dict[str, object]:
    direction_probability = probability_table[["p_short", "p_long"]].max(axis=1).to_numpy(dtype=np.float64, copy=False)
    predicted_label = probability_table["predicted_label"]
    direction_sign = np.where(
        predicted_label.eq("long"),
        1.0,
        np.where(predicted_label.eq("short"), -1.0, 0.0),
    )
    active_mask = (predicted_label != "flat").to_numpy(dtype=bool, copy=False) & (direction_probability >= entry_threshold)
    exposure = np.minimum(direction_probability, exposure_cap) * risk_size_multiplier
    signed_exposure = direction_sign * exposure * active_mask.astype(np.float64)
    future_log_return = probability_table["future_log_return_1"].to_numpy(dtype=np.float64, copy=False)
    proxy_log_returns = signed_exposure * future_log_return
    cumulative = np.cumsum(proxy_log_returns)
    running_peak = np.maximum.accumulate(np.maximum(cumulative, 0.0))
    max_drawdown = float(np.max(running_peak - cumulative)) if len(cumulative) else 0.0
    active_count = int(active_mask.sum())
    active_values = proxy_log_returns[active_mask]
    return {
        "entry_threshold": float(entry_threshold),
        "exposure_cap": float(exposure_cap),
        "risk_size_multiplier": float(risk_size_multiplier),
        "active_rows": active_count,
        "participation_rate": float(active_mask.mean()) if len(active_mask) else 0.0,
        "mean_abs_exposure": float(np.abs(signed_exposure).mean()) if len(signed_exposure) else 0.0,
        "proxy_log_return_sum": float(proxy_log_returns.sum()),
        "proxy_return_pct": float(math.exp(proxy_log_returns.sum()) - 1.0),
        "proxy_mean_log_return": float(proxy_log_returns.mean()) if len(proxy_log_returns) else 0.0,
        "active_mean_log_return": float(active_values.mean()) if active_count else 0.0,
        "active_hit_rate": float((active_values > 0.0).mean()) if active_count else 0.0,
        "proxy_max_drawdown": max_drawdown,
    }


def build_control_sensitivity_summary(
    probability_table: pd.DataFrame,
    calibration_summary: dict[str, object],
) -> dict[str, object]:
    adjusted = apply_lane_specific_temperature(probability_table, calibration_summary)
    splits: dict[str, dict[str, object]] = {}
    for split_name in ("validation", "holdout"):
        split_payload: dict[str, object] = {}
        split_table = adjusted.loc[adjusted["data_split"].eq(split_name)].copy()
        for lane_name in baseline.REPORTING_LANE_ORDER:
            lane_table = split_table.loc[split_table["reporting_lane"].eq(lane_name)].copy()
            if lane_table.empty:
                continue
            rows = []
            for entry_threshold in ENTRY_THRESHOLD_GRID:
                for exposure_cap in EXPOSURE_CAP_GRID:
                    for risk_size_multiplier in RISK_SIZE_GRID:
                        rows.append(
                            compute_proxy_control_metrics(
                                lane_table,
                                entry_threshold=entry_threshold,
                                exposure_cap=exposure_cap,
                                risk_size_multiplier=risk_size_multiplier,
                            )
                        )
            rows = sorted(
                rows,
                key=lambda item: (
                    item["proxy_log_return_sum"],
                    -item["proxy_max_drawdown"],
                    -item["participation_rate"],
                ),
                reverse=True,
            )
            best = rows[0]
            positive_configs = sum(1 for item in rows if item["proxy_log_return_sum"] > 0.0)
            if positive_configs == 0:
                control_read = "no positive offline proxy control configuration appeared on this slice"
            elif best["participation_rate"] < 0.02:
                control_read = "positive offline proxy control configurations appeared, but only on sparse low-participation slices"
            else:
                control_read = "positive offline proxy control configurations appeared on a non-trivial participation slice"
            split_payload[lane_name] = {
                "config_rows": rows,
                "draft_findings": {
                    "positive_config_count": int(positive_configs),
                    "best_proxy_config": best,
                    "control_read": control_read,
                },
            }
        splits[split_name] = split_payload
    return {
        "dataset_id": baseline.DATASET_ID,
        "scorecard_id": baseline.SCORECARD_ID,
        "baseline_seed_id": baseline.BASELINE_SEED_ID,
        "followup_pack_id": FOLLOWUP_PACK_ID,
        "report_id": "report_fpmarkets_v2_tier_b_control_sensitivity_0001",
        "model_family_id": baseline.MODEL_FAMILY_ID,
        "produced_by_stage": STAGE_NAME,
        "local_spec_ref": FOLLOWUP_LOCAL_SPEC_REF,
        "decision_ref": BASELINE_DECISION_REF,
        "entry_threshold_grid": list(ENTRY_THRESHOLD_GRID),
        "exposure_cap_grid": list(EXPOSURE_CAP_GRID),
        "risk_size_grid": list(RISK_SIZE_GRID),
        "probability_source": "lane_specific_temperature_fit",
        "splits": _to_builtin(splits),
    }


def build_robustness_summary(probability_table: pd.DataFrame) -> dict[str, object]:
    tier_b_table = probability_table.loc[probability_table["reporting_lane"].eq("tier_b_exploration")].copy()
    pattern_metrics: dict[str, list[dict[str, object]]] = {}
    month_metrics: dict[str, list[dict[str, object]]] = {}
    for split_name in ("validation", "holdout"):
        split_table = tier_b_table.loc[tier_b_table["data_split"].eq(split_name)].copy()
        pattern_rows = []
        total_rows = int(len(split_table))
        for missing_groups in MISSING_PATTERN_ORDER:
            pattern_table = split_table.loc[split_table["missing_groups"].eq(missing_groups)].copy()
            if pattern_table.empty:
                continue
            metrics = baseline.summarize_probability_slice(pattern_table)
            pattern_rows.append(
                {
                    "missing_groups": missing_groups,
                    "row_share": float(len(pattern_table) / total_rows) if total_rows else 0.0,
                    **metrics,
                }
            )
        pattern_metrics[split_name] = pattern_rows

        split_table["month"] = pd.to_datetime(split_table["timestamp"], utc=True).dt.strftime("%Y-%m")
        month_rows = []
        for month, month_table in split_table.groupby("month", sort=True):
            if len(month_table) < 500:
                continue
            metrics = baseline.summarize_probability_slice(month_table)
            month_rows.append({"month": month, **metrics})
        month_metrics[split_name] = month_rows

    holdout_patterns = pattern_metrics["holdout"]
    dominant_pattern = max(holdout_patterns, key=lambda item: item["row_count"]) if holdout_patterns else None
    draft_evidence_read = {
        "observed_missing_pattern_count": {
            split_name: int(len(pattern_metrics[split_name])) for split_name in ("validation", "holdout")
        },
        "dominant_holdout_pattern": dominant_pattern["missing_groups"] if dominant_pattern else None,
        "dominant_holdout_pattern_share": dominant_pattern["row_share"] if dominant_pattern else 0.0,
        "stage05_carry_forward_read": (
            "current broader_0002 + helper_0001 + broader_0003 evidence remains sufficient for continued offline Tier B exploration, "
            "but the follow-up pack still does not authorize MT5-path work or operating promotion"
        ),
    }
    return {
        "dataset_id": baseline.DATASET_ID,
        "scorecard_id": baseline.SCORECARD_ID,
        "baseline_seed_id": baseline.BASELINE_SEED_ID,
        "followup_pack_id": FOLLOWUP_PACK_ID,
        "report_id": "report_fpmarkets_v2_tier_b_robustness_0001",
        "model_family_id": baseline.MODEL_FAMILY_ID,
        "produced_by_stage": STAGE_NAME,
        "local_spec_ref": FOLLOWUP_LOCAL_SPEC_REF,
        "decision_ref": BASELINE_DECISION_REF,
        "pattern_metrics": _to_builtin(pattern_metrics),
        "month_metrics": _to_builtin(month_metrics),
        "draft_evidence_read": draft_evidence_read,
    }


def apply_weight_scenario(frame: pd.DataFrame, scenario_weights: dict[str, float]) -> pd.DataFrame:
    adjusted = frame.copy()
    adjusted["msft_xnas_weight"] = float(scenario_weights["msft_xnas_weight"])
    adjusted["nvda_xnas_weight"] = float(scenario_weights["nvda_xnas_weight"])
    adjusted["aapl_xnas_weight"] = float(scenario_weights["aapl_xnas_weight"])
    adjusted["top3_weighted_return_1"] = (
        adjusted["msft_xnas_weight"] * adjusted["msft_simple_return_1"]
        + adjusted["nvda_xnas_weight"] * adjusted["nvda_simple_return_1"]
        + adjusted["aapl_xnas_weight"] * adjusted["aapl_simple_return_1"]
    )
    adjusted["us100_minus_top3_weighted_return_1"] = adjusted["us100_simple_return_1"] - adjusted["top3_weighted_return_1"]
    return adjusted


def build_weight_verdict_summary(frame: pd.DataFrame, row_labels: pd.DataFrame) -> dict[str, object]:
    scenario_rows = []
    holdout_tier_b_log_losses = []
    holdout_tier_b_briers = []
    holdout_tier_b_macro_f1 = []
    for scenario_name, scenario_weights in WEIGHT_SCENARIOS.items():
        scenario_frame = apply_weight_scenario(frame, scenario_weights)
        scenario_model_frame = baseline.build_model_frame(scenario_frame, row_labels)
        scenario_probability_table, scenario_thresholds = baseline.build_probability_table(scenario_model_frame)
        scenario_summary = baseline.build_evaluation_summary(
            scenario_probability_table,
            row_labels_path=DEFAULT_ROW_LABELS_PATH.as_posix(),
        )
        tier_b_holdout = scenario_summary["splits"]["holdout"]["tier_b_exploration"]
        holdout_tier_b_log_losses.append(float(tier_b_holdout["log_loss"]))
        holdout_tier_b_briers.append(float(tier_b_holdout["multiclass_brier_score"]))
        holdout_tier_b_macro_f1.append(float(tier_b_holdout["macro_f1"]))
        scenario_rows.append(
            {
                "scenario_name": scenario_name,
                "weights": scenario_weights,
                "label_thresholds": scenario_thresholds,
                "validation": {
                    lane_name: scenario_summary["splits"]["validation"][lane_name]
                    for lane_name in baseline.REPORTING_LANE_ORDER
                },
                "holdout": {
                    lane_name: scenario_summary["splits"]["holdout"][lane_name]
                    for lane_name in baseline.REPORTING_LANE_ORDER
                },
            }
        )

    spread = {
        "tier_b_holdout_log_loss_spread": float(max(holdout_tier_b_log_losses) - min(holdout_tier_b_log_losses)),
        "tier_b_holdout_brier_spread": float(max(holdout_tier_b_briers) - min(holdout_tier_b_briers)),
        "tier_b_holdout_macro_f1_spread": float(max(holdout_tier_b_macro_f1) - min(holdout_tier_b_macro_f1)),
    }
    return {
        "dataset_id": baseline.DATASET_ID,
        "scorecard_id": baseline.SCORECARD_ID,
        "baseline_seed_id": baseline.BASELINE_SEED_ID,
        "followup_pack_id": FOLLOWUP_PACK_ID,
        "report_id": "report_fpmarkets_v2_tier_b_weight_verdict_0001",
        "model_family_id": baseline.MODEL_FAMILY_ID,
        "weights_version": "foundation/config/top3_monthly_weights_fpmarkets_v2.csv@2026-04-16 (placeholder_equal_weight)",
        "scenario_rows": _to_builtin(scenario_rows),
        "spread_summary": spread,
        "draft_verdict": {
            "offline_screen_sufficient": bool(spread["tier_b_holdout_log_loss_spread"] < 0.02),
            "real_weight_rerun_required_before_simulated_or_mt5": True,
            "verdict_text": (
                "placeholder weights look stable enough for Stage 06 offline screening because the coarse tilt scenarios keep Tier B holdout metrics in a narrow band, "
                "but a real-weight rerun still remains required before any simulated execution, MT5-path expansion, or operating promotion claim"
            ),
        },
    }


def build_followup_manifest(
    *,
    row_labels_path: Path,
    calibration_summary: dict[str, object],
    control_summary: dict[str, object],
    robustness_summary: dict[str, object],
    weight_summary: dict[str, object],
) -> dict[str, object]:
    return {
        "dataset_id": baseline.DATASET_ID,
        "scorecard_id": baseline.SCORECARD_ID,
        "baseline_seed_id": baseline.BASELINE_SEED_ID,
        "followup_pack_id": FOLLOWUP_PACK_ID,
        "bundle_id": FOLLOWUP_BUNDLE_ID,
        "produced_by_stage": STAGE_NAME,
        "parser_version": baseline.PARSER_VERSION,
        "feature_order_hash": baseline.EXPECTED_FEATURE_ORDER_HASH,
        "row_labels_path": row_labels_path.as_posix(),
        "local_spec_ref": FOLLOWUP_LOCAL_SPEC_REF,
        "decision_ref": BASELINE_DECISION_REF,
        "adr_ref": FOLLOWUP_ADR_REF,
        "included_artifacts": {
            "calibration_fit_summary": CALIBRATION_SUMMARY_FILENAME,
            "control_sensitivity_summary": CONTROL_SUMMARY_FILENAME,
            "robustness_summary": ROBUSTNESS_SUMMARY_FILENAME,
            "weight_verdict_summary": WEIGHT_SUMMARY_FILENAME,
            "calibration_report": CALIBRATION_REPORT_FILENAME,
            "control_report": CONTROL_REPORT_FILENAME,
            "robustness_report": ROBUSTNESS_REPORT_FILENAME,
            "weight_report": WEIGHT_REPORT_FILENAME,
            "stage07_design_draft": STAGE07_DRAFT_FILENAME,
            "close_open_readout_draft": CLOSE_OPEN_DRAFT_FILENAME,
        },
        "fitted_temperatures": {
            lane_name: calibration_summary["fit_candidates"][f"{lane_name}_temperature_fit"]["temperature"]
            for lane_name in baseline.REPORTING_LANE_ORDER
        },
        "control_grid": {
            "entry_threshold": list(ENTRY_THRESHOLD_GRID),
            "exposure_cap": list(EXPOSURE_CAP_GRID),
            "risk_size_multiplier": list(RISK_SIZE_GRID),
        },
        "robustness_patterns": {
            split_name: [item["missing_groups"] for item in robustness_summary["pattern_metrics"][split_name]]
            for split_name in ("validation", "holdout")
        },
        "weight_scenarios": list(WEIGHT_SCENARIOS.keys()),
        "draft_boundary_note": (
            "this additive follow-up pack does not update workspace_state.yaml, current_working_state.md, or selection_status.md and therefore does not reflect an official Stage 06 or Stage 07 decision"
        ),
        "carry_forward_contract_boundary": (
            "strict Tier A runtime rule unchanged; Tier B remains separate offline exploration only; no simulated execution, MT5-path work, or operating promotion is materialized here"
        ),
        "key_reads": {
            "tier_b_holdout_identity_log_loss": calibration_summary["evaluation"]["holdout"]["tier_b_exploration"]["identity_read_only"]["log_loss"],
            "tier_b_holdout_calibrated_log_loss": calibration_summary["evaluation"]["holdout"]["tier_b_exploration"]["tier_b_exploration_temperature_fit"]["log_loss"],
            "tier_b_holdout_control_positive_config_count": control_summary["splits"]["holdout"]["tier_b_exploration"]["draft_findings"]["positive_config_count"],
            "weight_log_loss_spread": weight_summary["spread_summary"]["tier_b_holdout_log_loss_spread"],
        },
    }


def _format_prob_metric_line(label: str, metrics: dict[str, object]) -> str:
    return (
        f"- `{label}`: `row_count={metrics['row_count']}`, `log_loss={metrics['log_loss']:.6f}`, "
        f"`multiclass_brier_score={metrics['multiclass_brier_score']:.6f}`, "
        f"`ece={metrics['expected_calibration_error']:.6f}`, "
        f"`mean_max_probability={metrics['mean_max_probability']:.6f}`, "
        f"`observed_top_class_accuracy={metrics['observed_top_class_accuracy']:.6f}`"
    )


def render_calibration_report(calibration_summary: dict[str, object], reviewed_on: str) -> str:
    candidate_lines = []
    for candidate_name in (
        "identity_read_only",
        "strict_tier_a_temperature_fit",
        "tier_b_exploration_temperature_fit",
    ):
        candidate = calibration_summary["fit_candidates"][candidate_name]
        candidate_lines.append(
            f"- `{candidate_name}`: `temperature={candidate['temperature']:.6f}`, "
            f"`fit_split={candidate['fit_split']}`, `fit_lane={candidate['fit_lane']}`, "
            f"`fit_row_count={candidate['fit_row_count']}`"
        )

    holdout_tier_b = calibration_summary["evaluation"]["holdout"]["tier_b_exploration"]
    holdout_tier_a = calibration_summary["evaluation"]["holdout"]["strict_tier_a"]
    lines = [
        "# Stage 06 Tier B Calibration Fit Follow-Up (Stage 06 Tier B 보정 적합 후속)",
        "",
        "## Identity (식별 정보)",
        f"- reviewed_on: `{reviewed_on}`",
        f"- stage: `{STAGE_NAME}`",
        f"- baseline_seed_id: `{baseline.BASELINE_SEED_ID}`",
        f"- followup_pack_id: `{FOLLOWUP_PACK_ID}`",
        f"- local_spec_ref: `{FOLLOWUP_LOCAL_SPEC_REF}`",
        "",
        "## Boundary Read (경계 판독)",
        "- this pass fits separate `temperature scaling (온도 스케일링)` candidates on `validation (검증)` only and keeps all meaning `offline-only (오프라인 전용)`",
        "- no `runtime family (런타임 계열)`, no `simulated execution (가상 실행)`, and no `MT5 path (MT5 경로)` work is materialized here",
        "- class ordering stays `[p_short, p_flat, p_long]`; temperature scaling changes confidence only, not the class-order contract (계약)",
        "",
        "## Candidate Fits (후보 적합)",
        *candidate_lines,
        "",
        "## Holdout Read (보류 평가 판독)",
        _format_prob_metric_line("holdout / strict_tier_a / identity_read_only", holdout_tier_a["identity_read_only"]),
        _format_prob_metric_line(
            "holdout / strict_tier_a / strict_tier_a_temperature_fit",
            holdout_tier_a["strict_tier_a_temperature_fit"],
        ),
        _format_prob_metric_line("holdout / tier_b_exploration / identity_read_only", holdout_tier_b["identity_read_only"]),
        _format_prob_metric_line(
            "holdout / tier_b_exploration / strict_tier_a_temperature_fit",
            holdout_tier_b["strict_tier_a_temperature_fit"],
        ),
        _format_prob_metric_line(
            "holdout / tier_b_exploration / tier_b_exploration_temperature_fit",
            holdout_tier_b["tier_b_exploration_temperature_fit"],
        ),
        "",
        "## Draft Takeaway (초안 해석)",
        f"- tier_b_reuse_check: `{calibration_summary['draft_takeaway']['tier_b_reuse_check']}`",
        f"- tier_a_calibration_takeaway: `{calibration_summary['draft_takeaway']['tier_a_calibration_takeaway']}`",
        "",
        "## Notes (메모)",
        "- this report is a `follow-up artifact (후속 산출물)` only and does not update the official `selection_status (선정 상태)` or open Stage 07 by itself",
        "- the separate `Tier B calibration fit (Tier B 보정 적합)` now exists, but any later threshold or runtime meaning still needs a separate decision layer (결정 레이어)",
    ]
    return "\n".join(lines) + "\n"


def render_control_report(control_summary: dict[str, object], reviewed_on: str) -> str:
    holdout_tier_b = control_summary["splits"]["holdout"]["tier_b_exploration"]["draft_findings"]
    holdout_tier_a = control_summary["splits"]["holdout"]["strict_tier_a"]["draft_findings"]
    lines = [
        "# Stage 06 Tier B Control Sensitivity Read (Stage 06 Tier B 제어 민감도 판독)",
        "",
        "## Identity (식별 정보)",
        f"- reviewed_on: `{reviewed_on}`",
        f"- followup_pack_id: `{FOLLOWUP_PACK_ID}`",
        f"- probability_source: `{control_summary['probability_source']}`",
        "",
        "## Boundary Read (경계 판독)",
        "- this pass runs a coarse `threshold / exposure / sizing (임계값 / 노출 / 사이징)` grid as an `offline proxy (오프라인 프록시)` only",
        "- no `best alpha setting (최적 알파 설정)` is claimed; this report only asks whether the current seed is directionally fragile or stable under conservative controls",
        "",
        "## Grid (탐색 격자)",
        f"- entry_threshold (진입 임계값): `{control_summary['entry_threshold_grid']}`",
        f"- exposure_cap (노출 상한): `{control_summary['exposure_cap_grid']}`",
        f"- risk_size_multiplier (위험 사이징 배수): `{control_summary['risk_size_grid']}`",
        "",
        "## Holdout Best Proxy Configs (보류 평가 최고 프록시 구성)",
        f"- `strict_tier_a`: `{json.dumps(holdout_tier_a['best_proxy_config'], ensure_ascii=False)}`",
        f"- `tier_b_exploration`: `{json.dumps(holdout_tier_b['best_proxy_config'], ensure_ascii=False)}`",
        "",
        "## Draft Takeaway (초안 해석)",
        f"- holdout / strict_tier_a: `{holdout_tier_a['control_read']}`",
        f"- holdout / tier_b_exploration: `{holdout_tier_b['control_read']}`",
        "- the coarse control grid does not replace a later `threshold policy (임계값 정책)` or `risk policy (위험 정책)` decision",
        "",
        "## Notes (메모)",
        "- the proxy uses future `log_return_1 (로그수익률 1)` with lane-specific temperature-scaled probabilities and should not be read as a runtime PnL claim (손익 주장)",
        "- a later decision pass must still decide whether any Stage 07 control search should open, and if so on which lane (레인)",
    ]
    return "\n".join(lines) + "\n"


def render_robustness_report(robustness_summary: dict[str, object], reviewed_on: str) -> str:
    holdout_patterns = robustness_summary["pattern_metrics"]["holdout"]
    validation_patterns = robustness_summary["pattern_metrics"]["validation"]
    pattern_lines = []
    for split_name, pattern_rows in (("validation", validation_patterns), ("holdout", holdout_patterns)):
        for row in pattern_rows:
            pattern_lines.append(
                f"- `{split_name}` / `{row['missing_groups']}`: `row_count={row['row_count']}`, "
                f"`row_share={row['row_share']:.6f}`, `log_loss={row['log_loss']:.6f}`, "
                f"`macro_f1={row['macro_f1']:.6f}`, `balanced_accuracy={row['balanced_accuracy']:.6f}`"
            )

    month_lines = []
    for split_name in ("validation", "holdout"):
        top_months = robustness_summary["month_metrics"][split_name][:4]
        for row in top_months:
            month_lines.append(
                f"- `{split_name}` / `{row['month']}`: `row_count={row['row_count']}`, "
                f"`log_loss={row['log_loss']:.6f}`, `macro_f1={row['macro_f1']:.6f}`"
            )

    lines = [
        "# Stage 06 Tier B Robustness Read (Stage 06 Tier B 강건성 판독)",
        "",
        "## Identity (식별 정보)",
        f"- reviewed_on: `{reviewed_on}`",
        f"- followup_pack_id: `{FOLLOWUP_PACK_ID}`",
        "",
        "## Missing-Pattern Read (결손 패턴 판독)",
        *pattern_lines,
        "",
        "## Month Read (월별 판독)",
        *month_lines,
        "",
        "## Draft Evidence Sufficiency Read (초안 근거 충분성 판독)",
        f"- observed_missing_pattern_count: `{robustness_summary['draft_evidence_read']['observed_missing_pattern_count']}`",
        f"- dominant_holdout_pattern: `{robustness_summary['draft_evidence_read']['dominant_holdout_pattern']}`",
        f"- dominant_holdout_pattern_share: `{robustness_summary['draft_evidence_read']['dominant_holdout_pattern_share']:.6f}`",
        f"- stage05_carry_forward_read: `{robustness_summary['draft_evidence_read']['stage05_carry_forward_read']}`",
        "",
        "## Notes (메모)",
        "- the dominant Tier B missing pattern still comes from `g4_leader_equity|g5_breadth_extension`, so the current Tier B read should not be described as a fully balanced subgroup family",
        "- this report is still enough to move the open question into a durable artifact instead of leaving it as chat-only intent (채팅 전용 의도)",
    ]
    return "\n".join(lines) + "\n"


def render_weight_report(weight_summary: dict[str, object], reviewed_on: str) -> str:
    scenario_lines = []
    for row in weight_summary["scenario_rows"]:
        tier_b_holdout = row["holdout"]["tier_b_exploration"]
        scenario_lines.append(
            f"- `{row['scenario_name']}`: weights `{row['weights']}`, "
            f"`holdout_tier_b_log_loss={tier_b_holdout['log_loss']:.6f}`, "
            f"`holdout_tier_b_macro_f1={tier_b_holdout['macro_f1']:.6f}`, "
            f"`holdout_tier_b_brier={tier_b_holdout['multiclass_brier_score']:.6f}`"
        )

    lines = [
        "# Stage 06 Tier B Placeholder Weight Verdict (Stage 06 Tier B 임시 가중치 판정)",
        "",
        "## Identity (식별 정보)",
        f"- reviewed_on: `{reviewed_on}`",
        f"- followup_pack_id: `{FOLLOWUP_PACK_ID}`",
        f"- weights_version: `{weight_summary['weights_version']}`",
        "",
        "## Scenario Read (시나리오 판독)",
        *scenario_lines,
        "",
        "## Spread Summary (변동 폭 요약)",
        f"- tier_b_holdout_log_loss_spread: `{weight_summary['spread_summary']['tier_b_holdout_log_loss_spread']:.6f}`",
        f"- tier_b_holdout_brier_spread: `{weight_summary['spread_summary']['tier_b_holdout_brier_spread']:.6f}`",
        f"- tier_b_holdout_macro_f1_spread: `{weight_summary['spread_summary']['tier_b_holdout_macro_f1_spread']:.6f}`",
        "",
        "## Draft Verdict (초안 판정)",
        f"- offline_screen_sufficient: `{weight_summary['draft_verdict']['offline_screen_sufficient']}`",
        f"- real_weight_rerun_required_before_simulated_or_mt5: `{weight_summary['draft_verdict']['real_weight_rerun_required_before_simulated_or_mt5']}`",
        f"- verdict_text: `{weight_summary['draft_verdict']['verdict_text']}`",
        "",
        "## Notes (메모)",
        "- this report does not replace the contract fact that the current monthly weights file is still `placeholder (임시값)`",
        "- the read here is only that coarse offline conclusions do not swing wildly under obvious tilt scenarios (기울기 시나리오)",
    ]
    return "\n".join(lines) + "\n"


def render_stage07_design_draft(
    calibration_summary: dict[str, object],
    control_summary: dict[str, object],
    robustness_summary: dict[str, object],
    weight_summary: dict[str, object],
    reviewed_on: str,
) -> str:
    lines = [
        "# Stage 07 Alpha Design Draft (Stage 07 알파 설계 초안)",
        "",
        "## Draft Status (초안 상태)",
        "- this file is a `draft (초안)` only and does not open `Stage 07 (07단계)` by itself",
        "- no `workspace_state (워크스페이스 상태)` or `selection_status (선정 상태)` reflection is performed in this pass",
        "",
        "## Inputs Used (사용 입력)",
        f"- reviewed_on: `{reviewed_on}`",
        f"- calibration_followup: `report_fpmarkets_v2_tier_b_calibration_fit_0001.md`",
        f"- control_followup: `report_fpmarkets_v2_tier_b_control_sensitivity_0001.md`",
        f"- robustness_followup: `report_fpmarkets_v2_tier_b_robustness_0001.md`",
        f"- weight_followup: `report_fpmarkets_v2_tier_b_weight_verdict_0001.md`",
        "",
        "## Draft Lane Proposal (초안 레인 제안)",
        "- `Tier A main lane (Tier A 메인 레인)`: candidate `yes` for Stage 07 alpha search because the strict Tier A line remains the only current runtime-aligned line",
        "- `Tier B separate lane (Tier B 별도 레인)`: candidate `yes`, but `offline-only (오프라인 전용)` and still separate from any MT5-path meaning",
        "- `Tier B MT5 feasibility gate (Tier B MT5 가능성 게이트)`: candidate `hold`, not opened in this pass",
        "",
        "## Draft Scoreboard (초안 점수판)",
        "- primary probabilistic metrics: `log_loss (로그 손실)`, `multiclass_brier_score (다중분류 브라이어 점수)`, `expected_calibration_error (기대 보정 오차)`",
        "- stability checks: missing-pattern split, month split, and coarse control sensitivity read",
        "- kill rule candidate: stop a Tier B branch when coarse control configurations stay negative and subgroup drift concentrates too narrowly",
        "",
        "## Draft Supporting Read (초안 보조 판독)",
        f"- tier_b_reuse_check: `{calibration_summary['draft_takeaway']['tier_b_reuse_check']}`",
        f"- holdout_tier_b_control_positive_config_count: `{control_summary['splits']['holdout']['tier_b_exploration']['draft_findings']['positive_config_count']}`",
        f"- dominant_holdout_pattern: `{robustness_summary['draft_evidence_read']['dominant_holdout_pattern']}`",
        f"- offline_screen_sufficient_under_placeholder_weights: `{weight_summary['draft_verdict']['offline_screen_sufficient']}`",
        "",
        "## Draft Guardrails (초안 가드레일)",
        "- keep `strict Tier A runtime rule (엄격 Tier A 실행 규칙)` unchanged until a later explicit exploration read changes it",
        "- do not treat this draft as permission for `simulated execution (가상 실행)` or `MT5 path (MT5 경로)` work",
        "- keep `Tier B (Tier B)` reporting separate from `Tier A (Tier A)` in all later Stage 07 artifacts",
    ]
    return "\n".join(lines) + "\n"


def render_close_open_draft(
    calibration_summary: dict[str, object],
    control_summary: dict[str, object],
    robustness_summary: dict[str, object],
    weight_summary: dict[str, object],
    reviewed_on: str,
) -> str:
    tier_b_holdout = calibration_summary["evaluation"]["holdout"]["tier_b_exploration"]
    lines = [
        "# Stage 06 Close / Stage 07 Open Readout Draft (Stage 06 종료 / Stage 07 개시 판독 초안)",
        "",
        "## Draft Status (초안 상태)",
        "- this file is a `readout draft (판독 초안)` only and does not change the active stage (활성 단계)",
        "- a later decision-only pass should either adopt, revise, or reject these lines explicitly",
        "",
        "## Evidence Added In This Pass (이번 패스 추가 근거)",
        f"- holdout_tier_b_identity_log_loss: `{tier_b_holdout['identity_read_only']['log_loss']:.6f}`",
        f"- holdout_tier_b_calibrated_log_loss: `{tier_b_holdout['tier_b_exploration_temperature_fit']['log_loss']:.6f}`",
        f"- holdout_tier_b_control_positive_config_count: `{control_summary['splits']['holdout']['tier_b_exploration']['draft_findings']['positive_config_count']}`",
        f"- weight_log_loss_spread: `{weight_summary['spread_summary']['tier_b_holdout_log_loss_spread']:.6f}`",
        f"- dominant_holdout_missing_pattern: `{robustness_summary['draft_evidence_read']['dominant_holdout_pattern']}`",
        "",
        "## Draft Verdict Candidates (초안 판정 후보)",
        "- `Tier A Stage 07 main lane (Tier A Stage 07 메인 레인)`: candidate `yes`",
        "- `Tier B Stage 07 exploration target (Tier B Stage 07 탐색 대상)`: candidate `yes`, but `separate lane (별도 레인)` only",
        "- `Tier B still offline-only (Tier B 여전히 오프라인 전용)`: candidate `yes`",
        "- `Tier B MT5 feasibility gate (Tier B MT5 가능성 게이트)`: candidate `not yet / hold`",
        "",
        "## Draft Caveats (초안 주의점)",
        "- placeholder weights still remain placeholder weights (임시 가중치는 여전히 임시 가중치임)",
        "- the control sensitivity read now shows sparse positive proxy slices, but those remain low-participation and still carry no runtime meaning (제어 민감도 판독은 희소 양수 프록시 구간을 보이지만 참여율이 낮고 런타임 의미는 없음)",
        "- this draft therefore supports further bounded exploration, not promotion (승격이 아니라 제한된 추가 탐색을 지지함)",
    ]
    return "\n".join(lines) + "\n"


def write_outputs(
    *,
    output_root: Path,
    reviews_root: Path,
    row_labels_path: Path,
    calibration_summary: dict[str, object],
    control_summary: dict[str, object],
    robustness_summary: dict[str, object],
    weight_summary: dict[str, object],
    reviewed_on: str,
) -> dict[str, object]:
    output_root.mkdir(parents=True, exist_ok=True)
    reviews_root.mkdir(parents=True, exist_ok=True)

    manifest_path = output_root / FOLLOWUP_MANIFEST_FILENAME
    calibration_path = output_root / CALIBRATION_SUMMARY_FILENAME
    control_path = output_root / CONTROL_SUMMARY_FILENAME
    robustness_path = output_root / ROBUSTNESS_SUMMARY_FILENAME
    weight_path = output_root / WEIGHT_SUMMARY_FILENAME

    calibration_report_path = reviews_root / CALIBRATION_REPORT_FILENAME
    control_report_path = reviews_root / CONTROL_REPORT_FILENAME
    robustness_report_path = reviews_root / ROBUSTNESS_REPORT_FILENAME
    weight_report_path = reviews_root / WEIGHT_REPORT_FILENAME
    stage07_draft_path = reviews_root / STAGE07_DRAFT_FILENAME
    close_open_draft_path = reviews_root / CLOSE_OPEN_DRAFT_FILENAME

    manifest = build_followup_manifest(
        row_labels_path=row_labels_path,
        calibration_summary=calibration_summary,
        control_summary=control_summary,
        robustness_summary=robustness_summary,
        weight_summary=weight_summary,
    )

    _write_text(manifest_path, json.dumps(_to_builtin(manifest), indent=2))
    _write_text(calibration_path, json.dumps(_to_builtin(calibration_summary), indent=2))
    _write_text(control_path, json.dumps(_to_builtin(control_summary), indent=2))
    _write_text(robustness_path, json.dumps(_to_builtin(robustness_summary), indent=2))
    _write_text(weight_path, json.dumps(_to_builtin(weight_summary), indent=2))

    _write_text(calibration_report_path, render_calibration_report(calibration_summary, reviewed_on), bom=True)
    _write_text(control_report_path, render_control_report(control_summary, reviewed_on), bom=True)
    _write_text(robustness_report_path, render_robustness_report(robustness_summary, reviewed_on), bom=True)
    _write_text(weight_report_path, render_weight_report(weight_summary, reviewed_on), bom=True)
    _write_text(
        stage07_draft_path,
        render_stage07_design_draft(
            calibration_summary,
            control_summary,
            robustness_summary,
            weight_summary,
            reviewed_on,
        ),
        bom=True,
    )
    _write_text(
        close_open_draft_path,
        render_close_open_draft(
            calibration_summary,
            control_summary,
            robustness_summary,
            weight_summary,
            reviewed_on,
        ),
        bom=True,
    )

    return {
        "manifest_path": manifest_path.as_posix(),
        "calibration_path": calibration_path.as_posix(),
        "control_path": control_path.as_posix(),
        "robustness_path": robustness_path.as_posix(),
        "weight_path": weight_path.as_posix(),
        "calibration_report_path": calibration_report_path.as_posix(),
        "control_report_path": control_report_path.as_posix(),
        "robustness_report_path": robustness_report_path.as_posix(),
        "weight_report_path": weight_report_path.as_posix(),
        "stage07_draft_path": stage07_draft_path.as_posix(),
        "close_open_draft_path": close_open_draft_path.as_posix(),
        "manifest_sha256": sha256_file(manifest_path),
        "calibration_sha256": sha256_file(calibration_path),
        "control_sha256": sha256_file(control_path),
        "robustness_sha256": sha256_file(robustness_path),
        "weight_sha256": sha256_file(weight_path),
        "calibration_report_sha256": sha256_file(calibration_report_path),
        "control_report_sha256": sha256_file(control_report_path),
        "robustness_report_sha256": sha256_file(robustness_report_path),
        "weight_report_sha256": sha256_file(weight_report_path),
        "stage07_draft_sha256": sha256_file(stage07_draft_path),
        "close_open_draft_sha256": sha256_file(close_open_draft_path),
        "manifest": manifest,
    }


def main() -> int:
    args = parse_args()
    raw_root = Path(args.raw_root)
    row_labels_path = Path(args.row_labels_path)
    output_root = Path(args.output_root)
    reviews_root = Path(args.reviews_root)

    frame, _ = baseline.build_feature_frame(raw_root)
    row_labels = baseline.load_row_labels(row_labels_path)
    model_frame = baseline.build_model_frame(frame, row_labels)
    probability_table, _ = baseline.build_probability_table(model_frame)

    calibration_summary = build_calibration_fit_summary(probability_table)
    control_summary = build_control_sensitivity_summary(probability_table, calibration_summary)
    robustness_summary = build_robustness_summary(probability_table)
    weight_summary = build_weight_verdict_summary(frame, row_labels)
    outputs = write_outputs(
        output_root=output_root,
        reviews_root=reviews_root,
        row_labels_path=row_labels_path,
        calibration_summary=calibration_summary,
        control_summary=control_summary,
        robustness_summary=robustness_summary,
        weight_summary=weight_summary,
        reviewed_on=args.reviewed_on,
    )

    payload = {
        "status": "ok",
        "followup_pack_id": FOLLOWUP_PACK_ID,
        "output_root": str(output_root.resolve()),
        "reviews_root": str(reviews_root.resolve()),
        "tier_b_holdout_identity_log_loss": calibration_summary["evaluation"]["holdout"]["tier_b_exploration"]["identity_read_only"]["log_loss"],
        "tier_b_holdout_calibrated_log_loss": calibration_summary["evaluation"]["holdout"]["tier_b_exploration"]["tier_b_exploration_temperature_fit"]["log_loss"],
        "tier_b_holdout_control_positive_config_count": control_summary["splits"]["holdout"]["tier_b_exploration"]["draft_findings"]["positive_config_count"],
        "tier_b_holdout_weight_log_loss_spread": weight_summary["spread_summary"]["tier_b_holdout_log_loss_spread"],
        "hashes": {
            "manifest_sha256": outputs["manifest_sha256"],
            "calibration_sha256": outputs["calibration_sha256"],
            "control_sha256": outputs["control_sha256"],
            "robustness_sha256": outputs["robustness_sha256"],
            "weight_sha256": outputs["weight_sha256"],
            "calibration_report_sha256": outputs["calibration_report_sha256"],
            "control_report_sha256": outputs["control_report_sha256"],
            "robustness_report_sha256": outputs["robustness_report_sha256"],
            "weight_report_sha256": outputs["weight_report_sha256"],
            "stage07_draft_sha256": outputs["stage07_draft_sha256"],
            "close_open_draft_sha256": outputs["close_open_draft_sha256"],
        },
    }
    print(json.dumps(_to_builtin(payload), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
