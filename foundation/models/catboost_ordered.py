from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd
from catboost import CatBoostClassifier

from foundation.models.baseline_training import LABEL_ORDER, validate_model_input_frame
from foundation.models.onnx_bridge import ordered_sklearn_probabilities
from foundation.models.xgboost_boosting import (
    PROBABILITY_COLUMNS,
    characteristic_score,
    nonflat_threshold,
    probability_shape_metrics,
    split_decision_metrics,
)


@dataclass(frozen=True)
class CatBoostVariantSpec:
    variant_id: str
    idea_id: str
    description: str
    iterations: int
    depth: int
    learning_rate: float
    l2_leaf_reg: float
    random_strength: float
    bootstrap_type: str = "Bayesian"
    bagging_temperature: float | None = 1.0
    subsample: float | None = None
    boosting_type: str = "Ordered"
    grow_policy: str = "SymmetricTree"
    random_seed: int = 1812
    sample_weight_policy: str = "none"

    def payload(self) -> dict[str, Any]:
        return asdict(self)


def default_stage18_catboost_variants() -> list[CatBoostVariantSpec]:
    return [
        CatBoostVariantSpec(
            variant_id="v01_ordered_depth3_bayesian",
            idea_id="ordered_symmetric_depth3_bayesian",
            description="Ordered boosting, symmetric depth three trees, Bayesian bootstrap.",
            iterations=90,
            depth=3,
            learning_rate=0.040,
            l2_leaf_reg=6.0,
            random_strength=0.50,
            bagging_temperature=1.0,
            random_seed=1812,
        ),
        CatBoostVariantSpec(
            variant_id="v02_ordered_depth4_strong_l2",
            idea_id="ordered_symmetric_depth4_strong_regularization",
            description="Ordered boosting with deeper symmetric trees and stronger L2.",
            iterations=110,
            depth=4,
            learning_rate=0.030,
            l2_leaf_reg=10.0,
            random_strength=0.80,
            bagging_temperature=0.8,
            random_seed=1813,
        ),
        CatBoostVariantSpec(
            variant_id="v03_ordered_depth2_high_random_strength",
            idea_id="ordered_shallow_random_strength",
            description="Shallow ordered trees with high random strength to reveal calibration cliffs.",
            iterations=120,
            depth=2,
            learning_rate=0.035,
            l2_leaf_reg=5.0,
            random_strength=2.0,
            bagging_temperature=1.4,
            random_seed=1814,
        ),
        CatBoostVariantSpec(
            variant_id="v04_ordered_bernoulli_depth3",
            idea_id="ordered_bernoulli_density_pressure",
            description="Ordered boosting with Bernoulli bootstrap and moderate depth.",
            iterations=100,
            depth=3,
            learning_rate=0.035,
            l2_leaf_reg=8.0,
            random_strength=0.70,
            bootstrap_type="Bernoulli",
            bagging_temperature=None,
            subsample=0.72,
            random_seed=1815,
        ),
        CatBoostVariantSpec(
            variant_id="v05_plain_depth3_control",
            idea_id="plain_boosting_control",
            description="Plain boosting control with symmetric trees under the same feature contract.",
            iterations=95,
            depth=3,
            learning_rate=0.040,
            l2_leaf_reg=7.0,
            random_strength=0.60,
            bootstrap_type="Bayesian",
            bagging_temperature=1.0,
            boosting_type="Plain",
            random_seed=1816,
        ),
    ]


def _sample_weights(labels: np.ndarray, policy: str) -> np.ndarray | None:
    if policy != "balanced_classes":
        return None
    counts = {label: max(1, int((labels == label).sum())) for label in LABEL_ORDER}
    total = float(len(labels))
    return np.asarray([total / (len(LABEL_ORDER) * counts[int(label)]) for label in labels], dtype="float64")


def build_catboost_classifier(spec: CatBoostVariantSpec) -> CatBoostClassifier:
    params: dict[str, Any] = {
        "loss_function": "MultiClass",
        "eval_metric": "MultiClass",
        "iterations": int(spec.iterations),
        "depth": int(spec.depth),
        "learning_rate": float(spec.learning_rate),
        "l2_leaf_reg": float(spec.l2_leaf_reg),
        "random_strength": float(spec.random_strength),
        "bootstrap_type": str(spec.bootstrap_type),
        "boosting_type": str(spec.boosting_type),
        "grow_policy": str(spec.grow_policy),
        "random_seed": int(spec.random_seed),
        "allow_writing_files": False,
        "verbose": False,
        "thread_count": 2,
    }
    if spec.bootstrap_type == "Bayesian" and spec.bagging_temperature is not None:
        params["bagging_temperature"] = float(spec.bagging_temperature)
    if spec.bootstrap_type == "Bernoulli" and spec.subsample is not None:
        params["subsample"] = float(spec.subsample)
    return CatBoostClassifier(**params)


def fit_catboost_variant(
    frame: pd.DataFrame,
    feature_order: Sequence[str],
    spec: CatBoostVariantSpec,
) -> tuple[CatBoostClassifier, dict[str, Any]]:
    features = list(feature_order)
    validate_model_input_frame(frame, features)
    train = frame.loc[frame["split"].astype(str).eq("train")].copy()
    values = train.loc[:, features]
    labels = train["label_class"].astype("int64").to_numpy()
    missing = sorted(set(LABEL_ORDER).difference(set(labels)))
    if missing:
        raise RuntimeError(f"Train split is missing label classes: {missing}")
    model = build_catboost_classifier(spec)
    weights = _sample_weights(labels, spec.sample_weight_policy)
    model.fit(values, labels, sample_weight=weights)
    return model, {
        "train_rows": int(len(train)),
        "feature_count": int(len(features)),
        "class_counts": {str(k): int(v) for k, v in train["label_class"].value_counts().sort_index().items()},
        "sample_weight_policy": spec.sample_weight_policy,
    }


def probability_frame(model: CatBoostClassifier, frame: pd.DataFrame, feature_order: Sequence[str]) -> pd.DataFrame:
    values = frame.loc[:, list(feature_order)]
    probabilities = ordered_sklearn_probabilities(model, values.to_numpy(dtype="float64", copy=False))
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


def feature_importance_frame(model: CatBoostClassifier, feature_order: Sequence[str]) -> pd.DataFrame:
    values = np.asarray(model.get_feature_importance(type="PredictionValuesChange"), dtype="float64")
    total = float(np.abs(values).sum()) or 1.0
    rows = [
        {"feature": feature, "gain": float(value), "gain_share": float(abs(value) / total)}
        for feature, value in zip(feature_order, values, strict=True)
    ]
    return pd.DataFrame(rows).sort_values(["gain_share", "feature"], ascending=[False, True])


def selected_spec(selected: Mapping[str, Any]) -> CatBoostVariantSpec:
    return CatBoostVariantSpec(**dict(selected["spec"]))

