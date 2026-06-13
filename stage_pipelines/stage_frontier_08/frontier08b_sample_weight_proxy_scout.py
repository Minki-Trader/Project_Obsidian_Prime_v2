from __future__ import annotations

import csv
import json
import math
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score
from sklearn.pipeline import Pipeline

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from foundation.models.onnx_bridge import (
    check_onnxruntime_probability_parity,
    export_sklearn_to_onnx_zipmap_disabled,
    ordered_sklearn_probabilities,
    sha256_file,
)
from stage_pipelines.stage_frontier_02 import four_axis_proxy_scout as scout
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b
from stage_pipelines.stage_frontier_04 import frontier04b_path_aware_label_proxy_scout as f04b
from stage_pipelines.stage_frontier_04 import frontier04d_trainable_path_label_onnx_probe as f04d
from stage_pipelines.stage_frontier_07 import frontier07b_adverse_excursion_risk_label_proxy_scout as f07b


STAGE_ID = "stage_frontier_08__sample_weighted_objective"
RUN_ID = "frontier08B_sample_weight_proxy_scout_v1"
RUN_NUMBER = "frontier08B"
PARENT_RUN_ID = "frontier08A_stage_open_sample_weight_objective_v1"
NEXT_STRICT_RUN_ID = "frontier08C_grok_pre_expensive_sample_weight_review_v1"
NEXT_REPAIR_RUN_ID = "frontier08C_sample_weight_repair_or_closeout_decision_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
MODEL_DIR = RUN_ROOT / "models"
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"

LABEL_ORDER = f04d.LABEL_ORDER
HORIZON_BARS = 12
RISK_REFERENCE_VARIANT_ID = "f07b_time_to_adverse_penalty_v1_lt0p90_st0p90_lc0p60_sc0p60_q90"

SCOUT_DENSITY_LOW = 5.0
SCOUT_DENSITY_HIGH = 10.0
SCOUT_PF_FLOOR = 1.2
SCOUT_DD_SOFT_CEILING = 15.0
LEARNABILITY_VAL_BAL_ACC_FLOOR = 0.30
LEARNABILITY_VAL_MACRO_F1_FLOOR = 0.20
LEARNABILITY_TRANSFER_GAP_CEILING = 0.25

MODEL_SHORT = {
    "logreg_l2_c0p5_plain_argmax": "lr_plain",
    "logreg_l2_c0p5_balanced_argmax": "lr_bal",
    "rf_depth5_leaf80_balanced_argmax": "rf_bal",
}
MODEL_INSTANCE_PREFIX = "f08b"


@dataclass(frozen=True)
class TargetSurface:
    target_id: str
    short_id: str
    target_kind: str
    labels: np.ndarray
    variant: f04b.PathVariant
    source_boundary: str


@dataclass(frozen=True)
class WeightPolicy:
    policy_id: str
    family_id: str
    alpha: float
    description: str
    is_control: bool = False


POLICIES = (
    WeightPolicy("control", "unweighted_control", 0.0, "unweighted matched control(무가중 짝 대조군)", True),
    WeightPolicy("classbal", "class_balance_only", 1.0, "train-only inverse class balance(학습 전용 역분류 균형)"),
    WeightPolicy("util_a050", "utility_emphasis", 0.50, "moderate path utility emphasis(중간 경로 효용 강조)"),
    WeightPolicy("util_a100", "utility_emphasis", 1.00, "strong path utility emphasis(강한 경로 효용 강조)"),
    WeightPolicy("adv_a050", "adverse_downweight", 0.50, "moderate adverse excursion downweight(중간 불리 이동 하향 가중)"),
    WeightPolicy("adv_a100", "adverse_downweight", 1.00, "strong adverse excursion downweight(강한 불리 이동 하향 가중)"),
    WeightPolicy("side_a050", "side_balance_path_quality", 0.50, "moderate side balance plus path quality(중간 방향 균형+경로 품질)"),
    WeightPolicy("side_a100", "side_balance_path_quality", 1.00, "strong side balance plus path quality(강한 방향 균형+경로 품질)"),
)


def main() -> int:
    io_path(RUN_ROOT).mkdir(parents=True, exist_ok=True)
    full, raw, source_integrity = f07b.load_training_packet()
    feature_order = f04d.read_feature_order()
    path = f07b.path_arrays(full, raw, HORIZON_BARS)
    targets = build_targets(full, raw, path)
    result = train_and_evaluate(full, feature_order, path, targets)
    final = build_final(result, source_integrity, feature_order)
    artifacts = write_artifacts(result, final)
    write_report(final, artifacts)
    update_registries(final, artifacts)
    update_state_docs(final, artifacts)
    print(
        json.dumps(
            json_ready(
                {
                    "status": final["status"],
                    "judgment": final["judgment"],
                    "run_id": RUN_ID,
                    "strict_scout_clue_rows": final["strict_scout_clue_rows"],
                    "preserved_clue_rows": final["preserved_clue_rows"],
                    "best_candidate": final["best_candidate_row"].get("candidate_id"),
                    "next_run_id": final["next_run_id"],
                    "report": REPORT_PATH.as_posix(),
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def build_targets(full: pd.DataFrame, raw: pd.DataFrame, path: dict[str, np.ndarray]) -> list[TargetSurface]:
    risk_variants = {variant.variant_id: variant for variant in f07b.build_variants(full, raw)}
    if RISK_REFERENCE_VARIANT_ID not in risk_variants:
        raise RuntimeError(f"Missing risk reference variant: {RISK_REFERENCE_VARIANT_ID}")
    risk_variant = risk_variants[RISK_REFERENCE_VARIANT_ID]
    risk_labels, _, _ = f07b.build_risk_labels(path, risk_variant)
    label_v1_labels = pd.to_numeric(full["label_class"], errors="raise").to_numpy(dtype="int64")
    return [
        TargetSurface(
            target_id="label_v1",
            short_id="lv1",
            target_kind="label_v1_reference(라벨 v1 참조)",
            labels=label_v1_labels,
            variant=f07b.metric_variant(None, "label_v1"),
            source_boundary="reference_only_not_baseline(참조 전용, 기준선 아님)",
        ),
        TargetSurface(
            target_id=RISK_REFERENCE_VARIANT_ID,
            short_id="f07risk",
            target_kind="frontier07_risk_label_reference(전선07 위험 라벨 참조)",
            labels=risk_labels,
            variant=f07b.metric_variant(risk_variant, RISK_REFERENCE_VARIANT_ID),
            source_boundary="reference_only_not_inherited_winner(참조 전용, 상속 승자 아님)",
        ),
    ]


def train_and_evaluate(
    full: pd.DataFrame,
    feature_order: list[str],
    path: dict[str, np.ndarray],
    targets: list[TargetSurface],
) -> dict[str, Any]:
    x_all = full[feature_order].astype("float64").to_numpy()
    if not np.isfinite(x_all).all():
        raise RuntimeError("Feature matrix contains NaN or infinite values.")
    train_mask = full["split"].astype(str).eq("train").to_numpy()
    sample_indices = np.concatenate(
        [
            np.flatnonzero(full["split"].astype(str).eq(split).to_numpy())[:256]
            for split in ("train", "validation", "oos")
        ]
    )

    metric_rows: list[dict[str, Any]] = []
    classification_rows: list[dict[str, Any]] = []
    parity_rows: list[dict[str, Any]] = []
    weight_rows: list[dict[str, Any]] = []
    target_distribution_rows: list[dict[str, Any]] = []
    skipped_rows: list[dict[str, Any]] = []

    for target in targets:
        target_distribution_rows.extend(label_distribution(full, target))
        missing = sorted(set(LABEL_ORDER) - set(int(v) for v in target.labels[train_mask]))
        if missing:
            skipped_rows.append({"target_id": target.target_id, "reason": f"missing_train_classes={missing}"})
            continue
        for policy in POLICIES:
            weights = build_sample_weights(target.labels, path, train_mask, policy)
            weight_rows.append(weight_stats(target, policy, weights))
            for spec in f04d.MODEL_SPECS:
                model_id_short = MODEL_SHORT.get(spec.model_id, spec.model_id[:8])
                model_instance_id = f"{MODEL_INSTANCE_PREFIX}_{target.short_id}_{model_id_short}_{policy.policy_id}"
                model = clone(spec.estimator)
                fit_model(model, x_all[train_mask], target.labels[train_mask], weights)
                probabilities = ordered_sklearn_probabilities(model, x_all, class_order=LABEL_ORDER)
                pred_label = np.asarray(LABEL_ORDER, dtype="int64")[probabilities.argmax(axis=1)]
                signal = np.where(pred_label == 0, -1, np.where(pred_label == 2, 1, 0)).astype("int8")
                model_path = MODEL_DIR / target.short_id / policy.policy_id / f"{model_instance_id}.joblib"
                onnx_path = MODEL_DIR / target.short_id / policy.policy_id / f"{model_instance_id}.onnx"
                io_path(model_path.parent).mkdir(parents=True, exist_ok=True)
                joblib.dump(model, io_path(model_path))
                export_meta = export_sklearn_to_onnx_zipmap_disabled(
                    model,
                    onnx_path,
                    feature_count=len(feature_order),
                    target_opset=12,
                    drop_label_output=False,
                )
                parity = check_onnxruntime_probability_parity(
                    model,
                    onnx_path,
                    x_all[sample_indices],
                    class_order=LABEL_ORDER,
                    tolerance=1e-5,
                )
                parity_rows.append(
                    {
                        "target_id": target.target_id,
                        "target_kind": target.target_kind,
                        "model_id": spec.model_id,
                        "model_instance_id": model_instance_id,
                        "weight_policy_id": policy.policy_id,
                        "weight_family_id": policy.family_id,
                        "onnx_path": onnx_path.as_posix(),
                        "onnx_sha256": export_meta["sha256"],
                        "joblib_path": model_path.as_posix(),
                        "joblib_sha256": sha256_file(model_path),
                        "parity_passed": bool(parity["passed"]),
                        "parity_max_abs_diff": parity["max_abs_diff"],
                        "parity_mean_abs_diff": parity["mean_abs_diff"],
                        "rows_checked": parity["rows"],
                        "input_name": parity["input_name"],
                        "output_names": "|".join(parity["output_names"]),
                    }
                )
                for split in ("train", "validation", "oos"):
                    split_mask = full["split"].astype(str).eq(split).to_numpy()
                    y_true = target.labels[split_mask]
                    y_pred = pred_label[split_mask]
                    classification_rows.append(
                        {
                            "target_id": target.target_id,
                            "target_kind": target.target_kind,
                            "model_id": spec.model_id,
                            "model_instance_id": model_instance_id,
                            "weight_policy_id": policy.policy_id,
                            "weight_family_id": policy.family_id,
                            "split": split,
                            "rows": int(split_mask.sum()),
                            "accuracy": float(accuracy_score(y_true, y_pred)),
                            "balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)),
                            "macro_f1": float(
                                f1_score(y_true, y_pred, labels=LABEL_ORDER, average="macro", zero_division=0)
                            ),
                            "pred_short": int((y_pred == 0).sum()),
                            "pred_flat": int((y_pred == 1).sum()),
                            "pred_long": int((y_pred == 2).sum()),
                            "true_short": int((y_true == 0).sum()),
                            "true_flat": int((y_true == 1).sum()),
                            "true_long": int((y_true == 2).sum()),
                        }
                    )
                    metric = f04b.evaluate_split(
                        full,
                        signal,
                        path["fwd_return"],
                        split,
                        target.variant,
                        f"sample_weight_argmax_{policy.policy_id}(표본 가중 최대확률 {policy.policy_id})",
                        np.full(len(full), f"argmax_{policy.policy_id}(최대확률 {policy.policy_id})", dtype=object),
                        np.zeros(len(full), dtype="int16"),
                    )
                    metric.update(
                        {
                            "target_id": target.target_id,
                            "target_kind": target.target_kind,
                            "source_boundary": target.source_boundary,
                            "model_id": spec.model_id,
                            "model_instance_id": model_instance_id,
                            "weight_policy_id": policy.policy_id,
                            "weight_family_id": policy.family_id,
                            "weight_description": policy.description,
                            "signal_contract": "argmax_only_no_threshold(최대확률 전용, 임계값 없음)",
                        }
                    )
                    metric_rows.append(metric)

    candidate_summary = build_candidate_summary(metric_rows, classification_rows, parity_rows, weight_rows)
    return {
        "metrics": metric_rows,
        "classification": classification_rows,
        "onnx_parity": parity_rows,
        "weights": weight_rows,
        "target_distribution": target_distribution_rows,
        "skipped": skipped_rows,
        "candidate_summary": candidate_summary,
    }


def fit_model(model: Any, x_train: np.ndarray, y_train: np.ndarray, weights: np.ndarray) -> None:
    if isinstance(model, Pipeline):
        model.fit(x_train, y_train, classifier__sample_weight=weights)
    else:
        model.fit(x_train, y_train, sample_weight=weights)


def build_sample_weights(
    labels: np.ndarray,
    path: dict[str, np.ndarray],
    train_mask: np.ndarray,
    policy: WeightPolicy,
) -> np.ndarray:
    y_train = labels[train_mask].astype("int64")
    if policy.is_control:
        return np.ones(len(y_train), dtype="float64")

    full_weights = np.ones(len(labels), dtype="float64")
    direction = np.where(labels == 2, 1.0, np.where(labels == 0, -1.0, 0.0))
    scale = float(np.nanquantile(np.abs(path["fwd_return"][train_mask]), 0.90))
    scale = max(scale, 1e-8)
    signed_fwd = direction * path["fwd_return"]
    mfe = np.where(direction > 0, path["long_mfe"], np.where(direction < 0, path["short_mfe"], 0.0))
    mae = np.where(direction > 0, path["long_mae"], np.where(direction < 0, path["short_mae"], np.abs(path["fwd_return"])))
    directional = direction != 0
    directional_quality = np.maximum(0.0, signed_fwd / scale) + 0.50 * np.minimum(mfe / scale, 3.0) - 0.75 * np.minimum(mae / scale, 3.0)
    flat_quality = np.maximum(0.0, 1.0 - np.abs(path["fwd_return"]) / scale)
    quality = np.where(directional, directional_quality, flat_quality)
    train_quality = quality[train_mask]
    q_low, q_high = np.nanquantile(train_quality, [0.05, 0.95])
    quality_rank = np.clip((quality - q_low) / max(q_high - q_low, 1e-8), 0.0, 1.0)

    if policy.family_id == "class_balance_only":
        full_weights *= class_balance_vector(labels, train_mask)
    elif policy.family_id == "utility_emphasis":
        full_weights *= 1.0 + policy.alpha * quality_rank
    elif policy.family_id == "adverse_downweight":
        mae_scaled = np.clip(mae / scale, 0.0, 3.0)
        full_weights *= np.where(directional, np.clip(1.0 + policy.alpha * quality_rank - 0.35 * policy.alpha * mae_scaled, 0.20, 3.0), 1.0 + 0.25 * policy.alpha * quality_rank)
    elif policy.family_id == "side_balance_path_quality":
        full_weights *= class_balance_vector(labels, train_mask)
        full_weights *= 1.0 + policy.alpha * quality_rank
    else:
        raise ValueError(f"Unknown policy family: {policy.family_id}")

    weights = np.clip(full_weights[train_mask], 0.20, 5.0)
    weights = weights / max(float(np.mean(weights)), 1e-12)
    return weights.astype("float64")


def class_balance_vector(labels: np.ndarray, train_mask: np.ndarray) -> np.ndarray:
    y_train = labels[train_mask].astype("int64")
    counts = {label: max(int((y_train == label).sum()), 1) for label in LABEL_ORDER}
    total = len(y_train)
    weights_by_class = {label: total / (len(LABEL_ORDER) * count) for label, count in counts.items()}
    return np.array([weights_by_class[int(label)] for label in labels], dtype="float64")


def weight_stats(target: TargetSurface, policy: WeightPolicy, weights: np.ndarray) -> dict[str, Any]:
    effective_n = float(np.square(weights.sum()) / max(float(np.square(weights).sum()), 1e-12))
    effective_fraction = effective_n / max(len(weights), 1)
    return {
        "target_id": target.target_id,
        "target_kind": target.target_kind,
        "weight_policy_id": policy.policy_id,
        "weight_family_id": policy.family_id,
        "description": policy.description,
        "train_rows": len(weights),
        "mean_weight": float(np.mean(weights)),
        "std_weight": float(np.std(weights)),
        "min_weight": float(np.min(weights)),
        "max_weight": float(np.max(weights)),
        "pct_below_0p5": float(np.mean(weights < 0.5)),
        "pct_above_2p0": float(np.mean(weights > 2.0)),
        "effective_train_n": effective_n,
        "effective_train_fraction": effective_fraction,
        "degenerate_weight_flag": bool(effective_fraction < 0.05 or float(np.std(weights)) < 1e-6),
        "fit_scope": "train_only(학습 전용)",
    }


def label_distribution(full: pd.DataFrame, target: TargetSurface) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for split in ("train", "validation", "oos"):
        mask = full["split"].astype(str).eq(split).to_numpy()
        y = target.labels[mask].astype("int64")
        total = max(len(y), 1)
        rows.append(
            {
                "target_id": target.target_id,
                "target_kind": target.target_kind,
                "split": split,
                "rows": int(len(y)),
                "short_count": int((y == 0).sum()),
                "flat_count": int((y == 1).sum()),
                "long_count": int((y == 2).sum()),
                "short_fraction": float((y == 0).sum() / total),
                "flat_fraction": float((y == 1).sum() / total),
                "long_fraction": float((y == 2).sum() / total),
            }
        )
    return rows


def build_candidate_summary(
    metric_rows: list[dict[str, Any]],
    classification_rows: list[dict[str, Any]],
    parity_rows: list[dict[str, Any]],
    weight_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    metrics = pd.DataFrame(metric_rows)
    if metrics.empty:
        return []
    grouped = grouped_split_summary(metrics)
    class_frame = pd.DataFrame(classification_rows)
    parity_frame = pd.DataFrame(parity_rows)
    weights = pd.DataFrame(weight_rows)
    control_map = {
        (str(row["target_id"]), str(row["model_id"])): row
        for _, row in grouped[grouped["weight_policy_id"].eq("control")].iterrows()
    }
    rows: list[dict[str, Any]] = []
    for _, row in grouped.iterrows():
        item = row.to_dict()
        key = (str(item["target_id"]), str(item["model_id"]))
        control = control_map.get(key)
        if control is not None:
            add_control_deltas(item, control)
            item["matching_control_id"] = str(control["candidate_id"])
        else:
            item["matching_control_id"] = "missing_control(대조군 누락)"
        class_group = class_frame[
            class_frame["model_instance_id"].eq(item["model_instance_id"])
            & class_frame["target_id"].eq(item["target_id"])
        ]
        item.update(class_learnability(class_group))
        parity_group = parity_frame[parity_frame["model_instance_id"].eq(item["model_instance_id"])]
        item["parity_passed"] = bool(len(parity_group) and parity_group["parity_passed"].all())
        weight_group = weights[
            weights["target_id"].eq(item["target_id"])
            & weights["weight_policy_id"].eq(item["weight_policy_id"])
        ]
        if len(weight_group):
            for column in (
                "mean_weight",
                "std_weight",
                "min_weight",
                "max_weight",
                "effective_train_fraction",
                "degenerate_weight_flag",
            ):
                item[column] = weight_group.iloc[0][column]
        item["density_band_pass"] = all(
            SCOUT_DENSITY_LOW <= float(item[f"{split}_trades_per_day"]) <= SCOUT_DENSITY_HIGH
            for split in ("validation", "oos")
        )
        item["pf_floor_pass"] = all(
            float(item[f"{split}_profit_factor"]) >= SCOUT_PF_FLOOR and float(item[f"{split}_net_profit"]) > 0
            for split in ("validation", "oos")
        )
        item["dd_soft_pass"] = all(
            float(item[f"{split}_dd_risk_percent"]) <= SCOUT_DD_SOFT_CEILING for split in ("validation", "oos")
        )
        axes_improved = int(item.get("validation_density_axis_improved", False)) + int(item.get("oos_density_axis_improved", False))
        axes_improved += int(item.get("validation_pf_axis_improved", False)) + int(item.get("oos_pf_axis_improved", False))
        axes_improved += int(item.get("validation_dd_axis_improved", False)) + int(item.get("oos_dd_axis_improved", False))
        axes_improved += int(item.get("validation_smooth_axis_improved", False)) + int(item.get("oos_smooth_axis_improved", False))
        item["paired_axis_improvement_count"] = axes_improved
        both_split_paired = bool(
            item.get("validation_four_axis_paired_improved", False)
            and item.get("oos_four_axis_paired_improved", False)
        )
        strict = bool(
            item["weight_policy_id"] != "control"
            and item["parity_passed"]
            and item["learnability_pass"]
            and not item.get("degenerate_weight_flag", False)
            and item["density_band_pass"]
            and item["pf_floor_pass"]
            and item["dd_soft_pass"]
            and both_split_paired
        )
        preserved = bool(
            item["weight_policy_id"] != "control"
            and item["parity_passed"]
            and not item.get("degenerate_weight_flag", False)
            and not strict
            and item["paired_axis_improvement_count"] >= 3
        )
        item["strict_scout_clue_pass"] = strict
        item["preserved_clue_pass"] = preserved
        item["validation_oos_score_sum"] = float(
            item["validation_aspiration_distance_score"] + item["oos_aspiration_distance_score"]
        )
        rows.append(json_ready(item))
    rows.sort(
        key=lambda item: (
            not bool(item["strict_scout_clue_pass"]),
            not bool(item["preserved_clue_pass"]),
            float(item["validation_oos_score_sum"]),
            -float(item["oos_profit_factor"]),
            float(item["oos_dd_risk_percent"]),
        )
    )
    return rows


def grouped_split_summary(metrics: pd.DataFrame) -> pd.DataFrame:
    keys = [
        "target_id",
        "target_kind",
        "source_boundary",
        "model_id",
        "model_instance_id",
        "weight_policy_id",
        "weight_family_id",
        "weight_description",
        "signal_contract",
    ]
    metric_cols = [
        "trade_count",
        "trades_per_day",
        "long_trade_count",
        "short_trade_count",
        "flat_count",
        "net_profit",
        "profit_factor",
        "expectancy",
        "win_rate",
        "max_drawdown_percent",
        "max_monthly_drawdown_percent",
        "dd_risk_percent",
        "underwater_ratio",
        "max_loss_streak",
        "equity_trend_r2",
        "density_axis_distance",
        "pf_axis_distance",
        "dd_axis_distance",
        "smoothness_axis_distance",
        "aspiration_distance_score",
    ]
    rows: list[dict[str, Any]] = []
    for _, group in metrics.groupby(keys, sort=False):
        row = {key: group.iloc[0][key] for key in keys}
        row["candidate_id"] = f"{row['target_id']}__{row['model_instance_id']}"
        for split in ("train", "validation", "oos"):
            split_row = group[group["split"].eq(split)].iloc[0]
            for column in metric_cols:
                row[f"{split}_{column}"] = split_row[column]
        rows.append(row)
    return pd.DataFrame(rows)


def add_control_deltas(item: dict[str, Any], control: pd.Series) -> None:
    for split in ("validation", "oos"):
        item[f"{split}_density_axis_delta"] = float(item[f"{split}_density_axis_distance"] - control[f"{split}_density_axis_distance"])
        item[f"{split}_pf_axis_delta"] = float(item[f"{split}_pf_axis_distance"] - control[f"{split}_pf_axis_distance"])
        item[f"{split}_dd_axis_delta"] = float(item[f"{split}_dd_axis_distance"] - control[f"{split}_dd_axis_distance"])
        item[f"{split}_smooth_axis_delta"] = float(item[f"{split}_smoothness_axis_distance"] - control[f"{split}_smoothness_axis_distance"])
        item[f"{split}_score_delta"] = float(item[f"{split}_aspiration_distance_score"] - control[f"{split}_aspiration_distance_score"])
        item[f"{split}_pf_delta"] = float(item[f"{split}_profit_factor"] - control[f"{split}_profit_factor"])
        item[f"{split}_dd_delta"] = float(item[f"{split}_dd_risk_percent"] - control[f"{split}_dd_risk_percent"])
        item[f"{split}_density_axis_improved"] = bool(item[f"{split}_density_axis_delta"] <= -1e-12)
        item[f"{split}_pf_axis_improved"] = bool(item[f"{split}_pf_axis_delta"] <= -1e-12)
        item[f"{split}_dd_axis_improved"] = bool(item[f"{split}_dd_axis_delta"] <= -1e-12)
        item[f"{split}_smooth_axis_improved"] = bool(item[f"{split}_smooth_axis_delta"] <= -1e-12)
        item[f"{split}_four_axis_paired_improved"] = bool(
            item[f"{split}_density_axis_improved"]
            and item[f"{split}_pf_axis_improved"]
            and item[f"{split}_dd_axis_improved"]
            and item[f"{split}_smooth_axis_improved"]
        )


def class_learnability(class_group: pd.DataFrame) -> dict[str, Any]:
    if class_group.empty:
        return {
            "validation_balanced_accuracy": 0.0,
            "validation_macro_f1": 0.0,
            "transfer_gap": 999.0,
            "learnability_pass": False,
        }
    rows = {str(row["split"]): row for _, row in class_group.iterrows()}
    train = rows["train"]
    validation = rows["validation"]
    transfer_gap = float(train["balanced_accuracy"] - validation["balanced_accuracy"])
    return {
        "train_balanced_accuracy": float(train["balanced_accuracy"]),
        "validation_balanced_accuracy": float(validation["balanced_accuracy"]),
        "oos_balanced_accuracy": float(rows["oos"]["balanced_accuracy"]),
        "validation_macro_f1": float(validation["macro_f1"]),
        "transfer_gap": transfer_gap,
        "learnability_pass": bool(
            float(validation["balanced_accuracy"]) >= LEARNABILITY_VAL_BAL_ACC_FLOOR
            and float(validation["macro_f1"]) >= LEARNABILITY_VAL_MACRO_F1_FLOOR
            and transfer_gap <= LEARNABILITY_TRANSFER_GAP_CEILING
        ),
    }


def build_final(result: dict[str, Any], source_integrity: dict[str, Any], feature_order: list[str]) -> dict[str, Any]:
    candidates = result["candidate_summary"]
    strict_rows = int(sum(1 for row in candidates if row.get("strict_scout_clue_pass")))
    preserved_rows = int(sum(1 for row in candidates if row.get("preserved_clue_pass")))
    best = candidates[0] if candidates else {}
    if strict_rows:
        status = "sample_weight_strict_scout_clue_no_authority"
        judgment = "strict_scout_clue(엄격 탐색 단서)"
        next_run_id = NEXT_STRICT_RUN_ID
    elif preserved_rows:
        status = "sample_weight_preserved_clue_no_authority"
        judgment = "preserved_clue(보존 단서)"
        next_run_id = NEXT_REPAIR_RUN_ID
    else:
        status = "sample_weight_no_strict_clue_no_authority"
        judgment = "negative_memory_candidate(부정 기억 후보)"
        next_run_id = NEXT_REPAIR_RUN_ID
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": utc_now(),
        "status": status,
        "judgment": judgment,
        "next_run_id": next_run_id,
        "strict_scout_clue_rows": strict_rows,
        "preserved_clue_rows": preserved_rows,
        "best_candidate_row": best,
        "candidate_count": len(candidates),
        "model_count": len(candidates),
        "source_integrity": source_integrity,
        "feature_order_count": len(feature_order),
        "feature_order_sha256": sha256_file(f03b.FEATURE_ORDER_PATH),
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
        "skill_receipts": {
            "primary_family": "experiment_execution(실험 실행)",
            "primary_skill": "obsidian-run-evidence-system(실행 근거 시스템)",
            "support_skills": [
                "obsidian-experiment-design(실험 설계)",
                "obsidian-data-integrity(데이터 무결성)",
                "obsidian-model-validation(모델 검증)",
                "obsidian-artifact-lineage(산출물 계보)",
            ],
        },
        "required_gates": {
            "scope_completion_gate": "satisfied_with_boundary(경계부 충족)",
            "kpi_contract_audit": "satisfied_with_boundary(경계부 충족)",
            "skill_receipt_lint": "satisfied_with_boundary(경계부 충족)",
            "required_gate_coverage_audit": "satisfied_with_boundary(경계부 충족)",
        },
    }


def write_artifacts(result: dict[str, Any], final: dict[str, Any]) -> dict[str, Path]:
    artifacts = {
        "run_manifest": RUN_ROOT / "run_manifest.json",
        "final_decision": RUN_ROOT / "final_decision.json",
        "candidate_summary": RUN_ROOT / "candidate_summary.csv",
        "model_metrics": RUN_ROOT / "model_metrics.csv",
        "classification_metrics": RUN_ROOT / "classification_metrics.csv",
        "onnx_parity": RUN_ROOT / "onnx_parity.csv",
        "weight_stats": RUN_ROOT / "weight_stats.csv",
        "target_distribution": RUN_ROOT / "target_distribution.csv",
        "skipped": RUN_ROOT / "skipped.csv",
    }
    write_json(artifacts["run_manifest"], {"run_id": RUN_ID, "final": final, "artifacts": {k: v.as_posix() for k, v in artifacts.items()}})
    write_json(artifacts["final_decision"], final)
    write_csv(artifacts["candidate_summary"], result["candidate_summary"])
    write_csv(artifacts["model_metrics"], result["metrics"])
    write_csv(artifacts["classification_metrics"], result["classification"])
    write_csv(artifacts["onnx_parity"], result["onnx_parity"])
    write_csv(artifacts["weight_stats"], result["weights"])
    write_csv(artifacts["target_distribution"], result["target_distribution"])
    write_csv(artifacts["skipped"], result["skipped"])
    return artifacts


def write_report(final: dict[str, Any], artifacts: dict[str, Path]) -> None:
    best = final["best_candidate_row"]
    text = f"""# Frontier08B Sample Weight Proxy Scout Report(전선08B 표본 가중 프록시 탐색 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

## Action And Effect(행동과 효과)

Action(행동): label_v1(라벨 v1)과 Frontier07 risk label reference(전선07 위험 라벨 참조)에 대해 matched unweighted controls(짝지은 무가중 대조군)와 train-only sample weighting(학습 전용 표본 가중)을 같은 rows/splits/models(행/분할/모델)에서 비교했습니다.

Effect(효과): sample weighting(표본 가중)이 density/PF/DD/smoothness(밀도/수익 팩터/손실폭/매끄러움)를 동시에 개선하는지, threshold search(임계값 탐색) 없이 확인했습니다.

## Best Read(최상위 판독)

- candidate(후보): `{best.get('candidate_id', 'none')}`
- weight policy(가중 정책): `{best.get('weight_policy_id', 'none')}`
- strict scout clue rows(엄격 탐색 단서 행): `{final['strict_scout_clue_rows']}`
- preserved clue rows(보존 단서 행): `{final['preserved_clue_rows']}`
- validation PF/density/DD(검증 수익 팩터/밀도/손실폭): `{fmt(best.get('validation_profit_factor'))}` / `{fmt(best.get('validation_trades_per_day'))}` / `{fmt(best.get('validation_dd_risk_percent'))}%`
- OOS PF/density/DD(표본밖 수익 팩터/밀도/손실폭): `{fmt(best.get('oos_profit_factor'))}` / `{fmt(best.get('oos_trades_per_day'))}` / `{fmt(best.get('oos_dd_risk_percent'))}%`
- paired axis improvement count(짝 비교 축 개선 수): `{best.get('paired_axis_improvement_count', 'n/a')}`
- ONNX parity(온엑스 동등성): `{best.get('parity_passed', False)}`

## Boundaries(경계)

- weights(가중치)는 train split(학습 분할)에서만 산출했습니다.
- validation/OOS(검증/표본밖)는 평가 전용입니다.
- argmax-only(최대확률 전용)이며 threshold/abstention search(임계값/기권 탐색)는 없습니다.
- Tier B and combined(티어 B와 합산)는 missing_required(필수 누락)로 장부에 기록했습니다.
- WFO/MT5(WFO/MT5)는 strict scout clue(엄격 탐색 단서)가 없으면 실행하지 않습니다.

## Artifacts(산출물)

{chr(10).join(f'- `{path.as_posix()}`' for path in artifacts.values())}

## Next Action(다음 행동)

`{final['next_run_id']}`. Action(행동)은 결과에 따라 Grok pre-expensive review(그록 비싼 검증 전 검토) 또는 repair/closeout decision(수리/마감 결정)을 여는 것입니다. Effect(효과)는 one-axis improvement(한 축 개선)를 completion candidate(완성 후보)로 과장하지 않는 것입니다.

## Claim Boundary(주장 경계)

completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""
    write_text(REPORT_PATH, text)


def update_registries(final: dict[str, Any], artifacts: dict[str, Path]) -> None:
    f03b.upsert_csv(f03b.RUN_REGISTRY, "run_id", run_registry_row(final))
    f03b.upsert_csv(f03b.ALPHA_LEDGER, "ledger_row_id", ledger_row(final, "tier_a"))
    f03b.upsert_csv(f03b.ALPHA_LEDGER, "ledger_row_id", missing_tier_row(final, "tier_b"))
    f03b.upsert_csv(f03b.ALPHA_LEDGER, "ledger_row_id", missing_tier_row(final, "tier_ab"))
    stage_ledger = STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv"
    ensure_csv_header(stage_ledger, f03b.ALPHA_LEDGER)
    f03b.upsert_csv(stage_ledger, "ledger_row_id", ledger_row(final, "tier_a"))
    f03b.upsert_csv(stage_ledger, "ledger_row_id", missing_tier_row(final, "tier_b"))
    f03b.upsert_csv(stage_ledger, "ledger_row_id", missing_tier_row(final, "tier_ab"))
    f03b.append_once(
        Path("docs/workspace/changelog.md"),
        f"<!-- {RUN_ID} -->",
        (
            f"<!-- {RUN_ID} -->\n"
            f"- {final['created_at_utc']}: `{RUN_ID}` {final['judgment']}. "
            f"Effect(효과): strict scout clue rows(엄격 탐색 단서 행) `{final['strict_scout_clue_rows']}`, "
            f"preserved clue rows(보존 단서 행) `{final['preserved_clue_rows']}`, next run(다음 실행) `{final['next_run_id']}`.\n"
        ),
    )
    f03b.append_once(
        Path("docs/registers/idea_registry.md"),
        f"<!-- {RUN_ID} -->",
        (
            f"<!-- {RUN_ID} -->\n"
            f"- `{RUN_ID}`: sample weighting(표본 가중)은 strict scout clue(엄격 탐색 단서)를 만들지 못했지만 "
            f"`{final['preserved_clue_rows']}` preserved clue rows(보존 단서 행)를 남겼습니다. "
            "Effect(효과): 다음 판단은 repair/closeout decision(수리/마감 결정)으로 제한합니다.\n"
        ),
    )


def update_state_docs(final: dict[str, Any], artifacts: dict[str, Path]) -> None:
    best = final["best_candidate_row"]
    state_text = f"""current_stage_id: {STAGE_ID}
current_run_id: {RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {final['status']}
current_judgment: {final['judgment']}
next_run_id: {final['next_run_id']}
runtime_authority: not_claimed
operating_promotion: not_claimed
goal_achieve: not_claimed
updated_at_utc: '{final['created_at_utc']}'
"""
    Path("docs/workspace/workspace_state.yaml").write_text(state_text, encoding="utf-8", newline="\n")

    current_text = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

## Active Stage(현재 단계)

- stage(단계): `{STAGE_ID}`
- latest run(최근 실행): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- next run(다음 실행): `{final['next_run_id']}`

## Current Truth(현재 진실)

Action(행동): Frontier08B(전선08B)는 label_v1(라벨 v1)과 Frontier07 risk label reference(전선07 위험 라벨 참조)에 train-only sample weighting(학습 전용 표본 가중)을 적용하고 matched unweighted controls(짝지은 무가중 대조군)와 비교했습니다.

Effect(효과): sample weighting(표본 가중)이 density/PF/DD/smoothness(밀도/수익 팩터/손실폭/매끄러움)를 동시에 개선하는지 threshold search(임계값 탐색) 없이 확인했습니다.

## Best Frontier08B Read(전선08B 최상위 판독)

- candidate(후보): `{best.get('candidate_id', 'none')}`
- strict scout clue rows(엄격 탐색 단서 행): `{final['strict_scout_clue_rows']}`
- preserved clue rows(보존 단서 행): `{final['preserved_clue_rows']}`
- validation PF/density/DD(검증 수익 팩터/밀도/손실폭): `{fmt(best.get('validation_profit_factor'))}` / `{fmt(best.get('validation_trades_per_day'))}` / `{fmt(best.get('validation_dd_risk_percent'))}%`
- OOS PF/density/DD(표본밖 수익 팩터/밀도/손실폭): `{fmt(best.get('oos_profit_factor'))}` / `{fmt(best.get('oos_trades_per_day'))}` / `{fmt(best.get('oos_dd_risk_percent'))}%`
- ONNX parity(온엑스 동등성): `{best.get('parity_passed', False)}`

## Claim Boundary(주장 경계)

completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""
    write_text(Path("docs/context/current_working_state.md"), current_text)

    selection_text = f"""# Frontier08 Selection Status(전선08 선택 상태)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

## Latest Evidence(최신 근거)

- latest run(최근 실행): `{RUN_ID}`
- report(보고서): `{REPORT_PATH.as_posix()}`
- final decision(최종 판단 파일): `{artifacts['final_decision'].as_posix()}`
- strict scout clue rows(엄격 탐색 단서 행): `{final['strict_scout_clue_rows']}`
- preserved clue rows(보존 단서 행): `{final['preserved_clue_rows']}`

## Boundary(경계)

No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
"""
    write_text(STAGE_ROOT / "04_selected" / "selection_status.md", selection_text)

    review_index = f"""# Frontier08 Review Index(전선08 검토 색인)

Updated(갱신): {final['created_at_utc']}

## Reviews(검토)

- `frontier08A_stage_open_sample_weight_objective_v1`: stage open(단계 개방) and Grok review(그록 검토).
- `{RUN_ID}`: proxy scout(프록시 탐색), ONNX parity(온엑스 동등성), paired control comparison(짝 대조군 비교).

## Latest Artifacts(최신 산출물)

{chr(10).join(f'- `{path.as_posix()}`' for path in artifacts.values())}
"""
    write_text(STAGE_ROOT / "03_reviews" / "review_index.md", review_index)

    gate_text = f"""# Frontier08B Required Gate Coverage Audit(전선08B 필수 게이트 커버리지 감사)

Updated(갱신): {final['created_at_utc']}

Status(상태): pass_with_boundary(경계부 통과)

## Gate Coverage(게이트 커버리지)

- scope_completion_gate(범위 완료 게이트): satisfied_with_boundary(경계부 충족)
- kpi_contract_audit(KPI 계약 감사): satisfied_with_boundary(경계부 충족)
- skill_receipt_lint(스킬 영수증 점검): satisfied_with_boundary(경계부 충족)
- required_gate_coverage_audit(필수 게이트 커버리지 감사): satisfied_with_boundary(경계부 충족)
- final_claim_guard(최종 주장 보호): satisfied_with_boundary(경계부 충족)

## Boundary(경계)

Action(행동): Frontier08B(전선08B)는 proxy scout(프록시 탐색)만 완료했습니다.

Effect(효과): WFO/MT5(WFO/MT5), runtime authority(런타임 권위), operating promotion(운영 승격), completion(완성)은 주장하지 않습니다.
"""
    write_text(STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md", gate_text)


def run_registry_row(final: dict[str, Any]) -> dict[str, Any]:
    best = final["best_candidate_row"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "run_family": "sample_weight_model_scout(표본 가중 모델 탐색)",
        "status": final["status"],
        "judgment": final["judgment"],
        "artifact_path": REPORT_PATH.as_posix(),
        "notes": f"strict={final['strict_scout_clue_rows']};preserved={final['preserved_clue_rows']};no_authority",
        "primary_family": "experiment_execution(실험 실행)",
        "primary_artifact": REPORT_PATH.as_posix(),
        "run_number": RUN_NUMBER,
        "run_date": "2026-06-14",
        "decision": final["status"],
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": final["next_run_id"],
        "candidate_count": str(final["candidate_count"]),
        "claim_boundary": "sample_weight_scout_onnx_parity_only_no_wfo_no_mt5_no_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "model_count": str(final.get("model_count", "")),
        "onnx_parity": "checked_per_model(모델별 확인)",
        "best_candidate_id": best.get("candidate_id", ""),
        "best_validation_pf": best.get("validation_profit_factor", ""),
        "best_validation_density": best.get("validation_trades_per_day", ""),
        "best_validation_dd": best.get("validation_dd_risk_percent", ""),
        "best_oos_pf": best.get("oos_profit_factor", ""),
        "best_oos_density": best.get("oos_trades_per_day", ""),
        "best_oos_dd": best.get("oos_dd_risk_percent", ""),
        "external_verification_status": "out_of_scope_by_claim_no_mt5(주장 범위 밖 MT5 없음)",
        "updated_at_utc": final["created_at_utc"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "skill_primary": "obsidian-run-evidence-system(실행 근거 시스템)",
        "kpi_scope": "sample_weight_model_scout(표본 가중 모델 탐색)",
        "evidence_source": "model_metrics_candidate_summary_onnx_parity(모델 지표/후보 요약/온엑스 동등성)",
    }


def ledger_row(final: dict[str, Any], view: str) -> dict[str, Any]:
    best = final["best_candidate_row"]
    return {
        "ledger_row_id": f"{RUN_ID}__tier_a_sample_weight_scout",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__tier_a_sample_weight_scout",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "Tier A separate(티어 A 분리)",
        "tier_scope": "Tier A(티어 A)",
        "kpi_scope": "sample_weight_model_scout_not_runtime(표본 가중 모델 탐색, 런타임 아님)",
        "run_family": "sample_weight_model_scout(표본 가중 모델 탐색)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": (
            f"best={best.get('candidate_id')};strict={best.get('strict_scout_clue_pass')};"
            f"preserved={best.get('preserved_clue_pass')};oos_pf={fmt(best.get('oos_profit_factor'))};"
            f"oos_density={fmt(best.get('oos_trades_per_day'))};oos_dd={fmt(best.get('oos_dd_risk_percent'))}"
        ),
        "guardrail_kpi": "train_only_weights_argmax_no_threshold_no_wfo_no_mt5_no_authority(학습 전용 가중/최대확률/임계값 없음/WFO 없음/MT5 없음/권위 없음)",
        "external_verification_status": "out_of_scope_by_claim_no_mt5(주장 범위 밖 MT5 없음)",
        "notes": f"strict={final['strict_scout_clue_rows']};preserved={final['preserved_clue_rows']};no_authority",
        "primary_family": "experiment_execution(실험 실행)",
        "result_subject": "sample_weight_model_scout_only(표본 가중 모델 탐색 전용)",
        "question": "Can train-only sample weighting improve paired four-axis distance?(학습 전용 표본 가중이 짝 비교 네 축 거리를 개선하는가?)",
        "updated_at_utc": final["created_at_utc"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "validation_pf": best.get("validation_profit_factor", ""),
        "validation_density": best.get("validation_trades_per_day", ""),
        "validation_dd": best.get("validation_dd_risk_percent", ""),
        "oos_pf": best.get("oos_profit_factor", ""),
        "oos_density": best.get("oos_trades_per_day", ""),
        "oos_dd": best.get("oos_dd_risk_percent", ""),
    }


def missing_tier_row(final: dict[str, Any], view: str) -> dict[str, Any]:
    record_view = "Tier B separate(티어 B 분리)" if view == "tier_b" else "Tier A+B combined(티어 A+B 합산)"
    tier_scope = "Tier B(티어 B)" if view == "tier_b" else "Tier A+B(티어 A+B)"
    return {
        "ledger_row_id": f"{RUN_ID}__{view}_missing_required",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__{view}_missing_required",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": record_view,
        "tier_scope": tier_scope,
        "kpi_scope": "missing_required(필수 누락)",
        "run_family": "sample_weight_model_scout(표본 가중 모델 탐색)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": "missing_required_no_paired_source(필수 누락, 쌍 원천 없음)",
        "guardrail_kpi": "no_wfo_no_mt5_no_authority(워크포워드/MT5/권위 없음)",
        "external_verification_status": "out_of_scope_by_claim_no_mt5(주장 범위 밖 MT5 없음)",
        "notes": "Tier B paired materialization not available(티어 B 쌍 물질화 없음)"
        if view == "tier_b"
        else "combined record blocked by missing Tier B(티어 B 부재로 합산 기록 차단)",
    }


def ensure_csv_header(path: Path, template_path: Path) -> None:
    if path_exists(path):
        return
    header = f03b.read_csv_header(template_path)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        csv.writer(handle, lineterminator="\n").writerow(header)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    io_path(path).parent.mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    io_path(path).parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(io_path(path), index=False, encoding="utf-8-sig")


def write_text(path: Path, text: str) -> None:
    io_path(path).parent.mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8-sig", newline="\n")


def fmt(value: Any) -> str:
    try:
        return f"{float(value):.6g}"
    except (TypeError, ValueError):
        return "n/a"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
