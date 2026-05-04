from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from foundation.models.baseline_training import LABEL_NAMES, LABEL_ORDER, validate_model_input_frame
from foundation.models.onnx_bridge import ordered_sklearn_probabilities
from foundation.models.xgboost_boosting import (
    PROBABILITY_COLUMNS,
    nonflat_threshold,
    probability_shape_metrics,
    split_decision_metrics,
)


@dataclass(frozen=True)
class ElasticNetLogisticVariantSpec:
    variant_id: str
    idea_id: str
    description: str
    feature_names: tuple[str, ...]
    c_value: float
    l1_ratio: float
    class_weight: str | None = "balanced"
    max_iter: int = 2000
    tol: float = 1.0e-2
    random_state: int = 2101
    tier_b_compatible: bool = True

    def payload(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["feature_names"] = list(self.feature_names)
        return payload


def core24_feature_names() -> tuple[str, ...]:
    return (
        "log_return_1",
        "log_return_3",
        "return_zscore_20",
        "close_ema20_ratio",
        "rsi_14",
        "rsi_14_slope_3",
        "atr_14_over_atr_50",
        "bollinger_width_20",
        "bb_position_20",
        "adx_14",
        "di_spread_14",
        "minutes_from_cash_open",
        "hl_range",
        "close_open_ratio",
        "ema20_ema50_diff",
        "ema20_ema50_spread_zscore_50",
        "stoch_kd_diff",
        "ppo_hist_12_26_9",
        "roc_12",
        "atr_14",
        "historical_vol_20",
        "supertrend_10_3",
        "vortex_indicator",
        "is_first_30m_after_open",
    )


def default_stage21_elasticnet_variants(
    *,
    full_feature_order: Sequence[str],
    tier_b_feature_order: Sequence[str],
) -> list[ElasticNetLogisticVariantSpec]:
    full58 = tuple(full_feature_order)
    core42 = tuple(tier_b_feature_order)
    core24 = core24_feature_names()
    return [
        ElasticNetLogisticVariantSpec(
            variant_id="v01_core42_balanced_enet025",
            idea_id="elasticnet_core42_balanced_sparse_linear",
            description="Tier-B-compatible core42 sparse linear sanity with moderate L1 share.",
            feature_names=core42,
            c_value=0.35,
            l1_ratio=0.25,
            class_weight="balanced",
            random_state=2101,
            tier_b_compatible=True,
        ),
        ElasticNetLogisticVariantSpec(
            variant_id="v02_core42_sparse_enet065",
            idea_id="elasticnet_core42_high_l1_sparse_linear",
            description="Tier-B-compatible core42 high-L1 sparse sign probe.",
            feature_names=core42,
            c_value=0.18,
            l1_ratio=0.65,
            class_weight="balanced",
            random_state=2102,
            tier_b_compatible=True,
        ),
        ElasticNetLogisticVariantSpec(
            variant_id="v03_full58_context_enet035",
            idea_id="elasticnet_full58_context_linear_contrast",
            description="Tier-A-only full58 context contrast to expose whether macro and constituent features dominate.",
            feature_names=full58,
            c_value=0.25,
            l1_ratio=0.35,
            class_weight="balanced",
            random_state=2103,
            tier_b_compatible=False,
        ),
        ElasticNetLogisticVariantSpec(
            variant_id="v04_core24_very_sparse_enet080",
            idea_id="elasticnet_core24_very_sparse_direction",
            description="Compact core24 high-L1 probe for the smallest handoff-friendly sparse surface.",
            feature_names=core24,
            c_value=0.14,
            l1_ratio=0.80,
            class_weight="balanced",
            random_state=2104,
            tier_b_compatible=True,
        ),
    ]


def build_elasticnet_logistic_classifier(spec: ElasticNetLogisticVariantSpec) -> Pipeline:
    classifier = LogisticRegression(
        solver="saga",
        l1_ratio=float(spec.l1_ratio),
        C=float(spec.c_value),
        class_weight=spec.class_weight,
        max_iter=int(spec.max_iter),
        tol=float(spec.tol),
        random_state=int(spec.random_state),
    )
    return Pipeline(steps=[("scaler", StandardScaler()), ("classifier", classifier)])


def fit_elasticnet_variant(
    frame: pd.DataFrame,
    feature_order: Sequence[str],
    spec: ElasticNetLogisticVariantSpec,
) -> tuple[Pipeline, dict[str, Any]]:
    features = list(spec.feature_names)
    missing = sorted(set(features).difference(set(feature_order)))
    if missing:
        raise ValueError(f"Feature set does not contain ElasticNet Logistic features: {missing}")
    validate_model_input_frame(frame, list(feature_order))
    train = frame.loc[frame["split"].astype(str).eq("train")].copy()
    values = train.loc[:, features].to_numpy(dtype="float64", copy=False)
    labels = train["label_class"].astype("int64").to_numpy()
    missing_labels = sorted(set(LABEL_ORDER).difference(set(labels)))
    if missing_labels:
        raise RuntimeError(f"Train split is missing label classes: {missing_labels}")
    model = build_elasticnet_logistic_classifier(spec)
    model.fit(values, labels)
    return model, {
        "train_rows": int(len(train)),
        "feature_count": int(len(features)),
        "class_counts": {str(k): int(v) for k, v in train["label_class"].value_counts().sort_index().items()},
        "solver": "saga",
        "penalty": "elasticnet",
        "l1_ratio": float(spec.l1_ratio),
        "c_value": float(spec.c_value),
        "class_weight": spec.class_weight,
        "tol": float(spec.tol),
    }


def probability_frame(model: Pipeline, frame: pd.DataFrame, feature_names: Sequence[str]) -> pd.DataFrame:
    features = list(feature_names)
    values = frame.loc[:, features].to_numpy(dtype="float64", copy=False)
    probabilities = ordered_sklearn_probabilities(model, values)
    sorted_probabilities = np.sort(probabilities, axis=1)
    probability_margin = sorted_probabilities[:, -1] - sorted_probabilities[:, -2]
    payload = pd.DataFrame(
        {
            "timestamp": pd.to_datetime(frame["timestamp"], utc=True).to_numpy(),
            "split": frame["split"].astype(str).to_numpy(),
            "label_class": frame["label_class"].astype("int64").to_numpy(),
            "p_short": probabilities[:, 0],
            "p_flat": probabilities[:, 1],
            "p_long": probabilities[:, 2],
            "probability_margin": probability_margin,
        }
    )
    if "partial_context_subtype" in frame.columns:
        payload["partial_context_subtype"] = frame["partial_context_subtype"].astype(str).to_numpy()
    return payload


def coefficient_frame(model: Pipeline, feature_names: Sequence[str]) -> pd.DataFrame:
    classifier = model.named_steps["classifier"]
    coefficients = np.asarray(classifier.coef_, dtype="float64")
    rows: list[dict[str, Any]] = []
    for feature_index, feature in enumerate(feature_names):
        per_class = {
            f"coef_{LABEL_NAMES[int(label)]}": float(coefficients[class_index, feature_index])
            for class_index, label in enumerate(classifier.classes_)
        }
        values = coefficients[:, feature_index]
        abs_values = np.abs(values)
        dominant_index = int(abs_values.argmax()) if len(abs_values) else 0
        dominant_label = LABEL_NAMES[int(classifier.classes_[dominant_index])]
        rows.append(
            {
                "feature": str(feature),
                "max_abs_coef": float(abs_values.max()) if len(abs_values) else 0.0,
                "dominant_label": dominant_label,
                "dominant_sign": int(np.sign(values[dominant_index])) if len(values) else 0,
                "active_class_count": int((abs_values > 1.0e-8).sum()),
                **per_class,
            }
        )
    return pd.DataFrame(rows).sort_values(["max_abs_coef", "feature"], ascending=[False, True])


def coefficient_shape_read(coefficients: pd.DataFrame) -> dict[str, Any]:
    if coefficients.empty:
        return {"feature_count": 0, "nonzero_feature_count": 0, "top_features": []}
    nonzero = coefficients.loc[coefficients["max_abs_coef"].astype("float64") > 1.0e-8]
    total_abs = float(coefficients["max_abs_coef"].abs().sum()) or 1.0
    top10_abs_share = float(coefficients.head(10)["max_abs_coef"].abs().sum() / total_abs)
    sign_counts = (
        nonzero.groupby(["dominant_label", "dominant_sign"], dropna=False).size().reset_index(name="count").to_dict(orient="records")
    )
    return {
        "feature_count": int(len(coefficients)),
        "nonzero_feature_count": int(len(nonzero)),
        "nonzero_ratio": float(len(nonzero) / max(1, len(coefficients))),
        "top10_abs_share": top10_abs_share,
        "sign_counts": sign_counts,
        "top_features": coefficients.head(12).to_dict(orient="records"),
    }


def sign_overlap_read(tier_a_coefficients: pd.DataFrame, tier_b_coefficients: pd.DataFrame) -> dict[str, Any]:
    if tier_a_coefficients.empty or tier_b_coefficients.empty:
        return {"shared_feature_count": 0, "same_dominant_sign_share": None}
    left = tier_a_coefficients.loc[:, ["feature", "dominant_label", "dominant_sign", "max_abs_coef"]].rename(
        columns={
            "dominant_label": "tier_a_dominant_label",
            "dominant_sign": "tier_a_dominant_sign",
            "max_abs_coef": "tier_a_max_abs_coef",
        }
    )
    right = tier_b_coefficients.loc[:, ["feature", "dominant_label", "dominant_sign", "max_abs_coef"]].rename(
        columns={
            "dominant_label": "tier_b_dominant_label",
            "dominant_sign": "tier_b_dominant_sign",
            "max_abs_coef": "tier_b_max_abs_coef",
        }
    )
    merged = left.merge(right, on="feature", how="inner")
    active = merged.loc[(merged["tier_a_max_abs_coef"] > 1.0e-8) | (merged["tier_b_max_abs_coef"] > 1.0e-8)]
    if active.empty:
        share = None
    else:
        same = (
            active["tier_a_dominant_label"].astype(str).eq(active["tier_b_dominant_label"].astype(str))
            & active["tier_a_dominant_sign"].astype("int64").eq(active["tier_b_dominant_sign"].astype("int64"))
        )
        share = float(same.mean())
    return {
        "shared_feature_count": int(len(merged)),
        "active_shared_feature_count": int(len(active)),
        "same_dominant_sign_share": share,
        "top_disagreements": active.loc[
            ~(
                active["tier_a_dominant_label"].astype(str).eq(active["tier_b_dominant_label"].astype(str))
                & active["tier_a_dominant_sign"].astype("int64").eq(active["tier_b_dominant_sign"].astype("int64"))
            )
        ]
        .sort_values(["tier_a_max_abs_coef", "tier_b_max_abs_coef"], ascending=[False, False])
        .head(10)
        .to_dict(orient="records"),
    }


def characteristic_score(metrics: Mapping[str, Any], probability_shape: Mapping[str, Any], coefficients: pd.DataFrame) -> float:
    validation = metrics.get("validation", {}) if isinstance(metrics.get("validation"), Mapping) else {}
    oos = metrics.get("oos", {}) if isinstance(metrics.get("oos"), Mapping) else {}
    val_cov = float(validation.get("signal_coverage") or 0.0)
    oos_cov = float(oos.get("signal_coverage") or 0.0)
    val_hit = float(validation.get("directional_hit_rate") or 0.0)
    oos_hit = float(oos.get("directional_hit_rate") or 0.0)
    val_margin = float(probability_shape.get("validation", {}).get("probability_margin_mean") or 0.0)
    oos_margin = float(probability_shape.get("oos", {}).get("probability_margin_mean") or 0.0)
    shape = coefficient_shape_read(coefficients)
    nonzero_ratio = float(shape.get("nonzero_ratio") or 0.0)
    top10_share = float(shape.get("top10_abs_share") or 1.0)
    density_stability = 1.0 - min(abs(val_cov - oos_cov) / 0.20, 1.0)
    margin_presence = min((val_margin + oos_margin) / 0.12, 1.0)
    sparsity_band = 1.0 - min(abs(nonzero_ratio - 0.35) / 0.35, 1.0)
    concentration_penalty = 1.0 - min(max(top10_share - 0.50, 0.0) / 0.45, 1.0)
    hit_read = max(0.0, ((val_hit + oos_hit) / 2.0) - (1.0 / 3.0))
    return float(
        0.22 * val_cov
        + 0.18 * oos_cov
        + 0.18 * density_stability
        + 0.16 * margin_presence
        + 0.14 * sparsity_band
        + 0.07 * concentration_penalty
        + 0.05 * hit_read
    )


__all__ = [
    "ElasticNetLogisticVariantSpec",
    "build_elasticnet_logistic_classifier",
    "characteristic_score",
    "coefficient_frame",
    "coefficient_shape_read",
    "core24_feature_names",
    "default_stage21_elasticnet_variants",
    "fit_elasticnet_variant",
    "nonflat_threshold",
    "probability_frame",
    "probability_shape_metrics",
    "sign_overlap_read",
    "split_decision_metrics",
]
