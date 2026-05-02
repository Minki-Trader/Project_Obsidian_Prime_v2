from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

from foundation.models.baseline_training import LABEL_NAMES, LABEL_ORDER, validate_model_input_frame


SPLITS = ("train", "validation", "oos")


@dataclass(frozen=True)
class GeometryAuditConfig:
    outlier_z: float = 3.0
    saturation_z: float = 5.0
    top_feature_count: int = 20
    high_correlation_threshold: float = 0.90


def fit_train_scaler(frame: pd.DataFrame, feature_order: Sequence[str]) -> StandardScaler:
    features = list(feature_order)
    validate_model_input_frame(frame, features)
    train = frame.loc[frame["split"].astype(str).eq("train"), features]
    return StandardScaler().fit(train.to_numpy(dtype="float64", copy=False))


def scaled_values(frame: pd.DataFrame, feature_order: Sequence[str], scaler: StandardScaler) -> np.ndarray:
    return scaler.transform(frame.loc[:, list(feature_order)].to_numpy(dtype="float64", copy=False))


def _split_frame(frame: pd.DataFrame, split_name: str) -> pd.DataFrame:
    return frame.loc[frame["split"].astype(str).eq(split_name)].copy()


def split_geometry_summary(
    frame: pd.DataFrame,
    feature_order: Sequence[str],
    scaler: StandardScaler,
    config: GeometryAuditConfig = GeometryAuditConfig(),
) -> tuple[pd.DataFrame, pd.DataFrame]:
    summary_rows: list[dict[str, Any]] = []
    feature_rows: list[dict[str, Any]] = []
    features = list(feature_order)
    for split_name in SPLITS:
        split = _split_frame(frame, split_name)
        values = scaled_values(split, features, scaler)
        abs_values = np.abs(values)
        split_means = values.mean(axis=0)
        split_stds = values.std(axis=0)
        outlier_rates = (abs_values >= config.outlier_z).mean(axis=0)
        saturation_rates = (abs_values >= config.saturation_z).mean(axis=0)
        summary_rows.append(
            {
                "split": split_name,
                "rows": int(len(split)),
                "feature_count": int(len(features)),
                "mean_abs_z_mean": float(np.abs(split_means).mean()),
                "mean_abs_z_max": float(np.abs(split_means).max()),
                "std_ratio_mean": float(split_stds.mean()),
                "std_ratio_max": float(split_stds.max()),
                "outlier_rate_mean": float(outlier_rates.mean()),
                "outlier_rate_max": float(outlier_rates.max()),
                "saturation_rate_mean": float(saturation_rates.mean()),
                "saturation_rate_max": float(saturation_rates.max()),
            }
        )
        for index, feature in enumerate(features):
            feature_rows.append(
                {
                    "split": split_name,
                    "feature": feature,
                    "mean_z": float(split_means[index]),
                    "abs_mean_z": float(abs(split_means[index])),
                    "std_ratio": float(split_stds[index]),
                    "outlier_rate": float(outlier_rates[index]),
                    "saturation_rate": float(saturation_rates[index]),
                }
            )
    feature_table = pd.DataFrame(feature_rows).sort_values(
        ["split", "abs_mean_z", "outlier_rate", "feature"],
        ascending=[True, False, False, True],
    )
    return pd.DataFrame(summary_rows), feature_table


def class_centroid_summary(
    frame: pd.DataFrame,
    feature_order: Sequence[str],
    scaler: StandardScaler,
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    features = list(feature_order)
    for split_name in SPLITS:
        split = _split_frame(frame, split_name)
        values = scaled_values(split, features, scaler)
        labels = split["label_class"].astype("int64").to_numpy()
        centroids: dict[int, np.ndarray] = {}
        for label in LABEL_ORDER:
            mask = labels == label
            if mask.any():
                centroids[label] = values[mask].mean(axis=0)
        for left, right in combinations(LABEL_ORDER, 2):
            if left not in centroids or right not in centroids:
                continue
            distance = np.linalg.norm(centroids[left] - centroids[right])
            rows.append(
                {
                    "split": split_name,
                    "left_label": LABEL_NAMES[left],
                    "right_label": LABEL_NAMES[right],
                    "centroid_distance": float(distance),
                    "feature_count": int(len(features)),
                }
            )
    return pd.DataFrame(rows)


def correlation_pair_summary(
    frame: pd.DataFrame,
    feature_order: Sequence[str],
    scaler: StandardScaler,
    config: GeometryAuditConfig = GeometryAuditConfig(),
) -> pd.DataFrame:
    features = list(feature_order)
    train = _split_frame(frame, "train")
    values = scaled_values(train, features, scaler)
    std = values.std(axis=0)
    valid_indices = np.flatnonzero(std > 1e-12)
    if len(valid_indices) < 2:
        return pd.DataFrame(columns=["left_feature", "right_feature", "correlation", "abs_correlation"])
    values = values[:, valid_indices]
    valid_features = [features[index] for index in valid_indices]
    corr = np.corrcoef(values, rowvar=False)
    rows: list[dict[str, Any]] = []
    for left_index in range(len(valid_features)):
        for right_index in range(left_index + 1, len(valid_features)):
            value = float(corr[left_index, right_index])
            if not np.isfinite(value):
                continue
            if abs(value) < config.high_correlation_threshold:
                continue
            rows.append(
                {
                    "left_feature": valid_features[left_index],
                    "right_feature": valid_features[right_index],
                    "correlation": value,
                    "abs_correlation": abs(value),
                }
            )
    return pd.DataFrame(rows).sort_values(["abs_correlation", "left_feature"], ascending=[False, True])


def common_feature_tier_gap_summary(
    tier_a_frame: pd.DataFrame,
    tier_b_fallback_frame: pd.DataFrame,
    common_features: Sequence[str],
    scaler: StandardScaler,
    config: GeometryAuditConfig = GeometryAuditConfig(),
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    features = list(common_features)
    for split_name in ("validation", "oos"):
        a_split = _split_frame(tier_a_frame, split_name)
        b_split = _split_frame(tier_b_fallback_frame, split_name)
        a_values = scaled_values(a_split, features, scaler)
        b_values = scaled_values(b_split, features, scaler)
        a_mean = a_values.mean(axis=0)
        b_mean = b_values.mean(axis=0)
        delta = b_mean - a_mean
        rows.append(
            {
                "split": split_name,
                "common_feature_count": int(len(features)),
                "tier_a_rows": int(len(a_split)),
                "tier_b_fallback_rows": int(len(b_split)),
                "mean_abs_z_gap": float(np.abs(delta).mean()),
                "max_abs_z_gap": float(np.abs(delta).max()),
                "tier_b_outlier_rate_mean": float((np.abs(b_values) >= config.outlier_z).mean()),
                "tier_b_saturation_rate_mean": float((np.abs(b_values) >= config.saturation_z).mean()),
            }
        )
    return pd.DataFrame(rows)


def table_payload(table: pd.DataFrame, *, limit: int | None = None) -> list[dict[str, Any]]:
    frame = table.head(limit).copy() if limit else table.copy()
    return frame.replace({np.nan: None}).to_dict(orient="records")


def audit_input_geometry(
    *,
    tier_a_frame: pd.DataFrame,
    tier_a_feature_order: Sequence[str],
    tier_b_fallback_frame: pd.DataFrame,
    tier_b_feature_order: Sequence[str],
    config: GeometryAuditConfig = GeometryAuditConfig(),
) -> dict[str, Any]:
    tier_a_scaler = fit_train_scaler(tier_a_frame, tier_a_feature_order)
    tier_a_summary, tier_a_features = split_geometry_summary(tier_a_frame, tier_a_feature_order, tier_a_scaler, config)
    tier_a_centroids = class_centroid_summary(tier_a_frame, tier_a_feature_order, tier_a_scaler)
    tier_a_corr = correlation_pair_summary(tier_a_frame, tier_a_feature_order, tier_a_scaler, config)

    common_features = [feature for feature in tier_b_feature_order if feature in set(tier_a_feature_order)]
    common_scaler = fit_train_scaler(tier_a_frame, common_features)
    tier_gap = common_feature_tier_gap_summary(
        tier_a_frame,
        tier_b_fallback_frame,
        common_features,
        common_scaler,
        config,
    )
    return {
        "config": config.__dict__,
        "tier_a_summary": tier_a_summary,
        "tier_a_top_feature_drift": tier_a_features,
        "tier_a_class_centroids": tier_a_centroids,
        "tier_a_high_correlation_pairs": tier_a_corr,
        "tier_gap_summary": tier_gap,
        "payload": {
            "tier_a_summary": table_payload(tier_a_summary),
            "tier_a_top_feature_drift": table_payload(tier_a_features, limit=config.top_feature_count),
            "tier_a_class_centroids": table_payload(tier_a_centroids),
            "tier_a_high_correlation_pairs": table_payload(tier_a_corr, limit=config.top_feature_count),
            "tier_gap_summary": table_payload(tier_gap),
        },
    }
