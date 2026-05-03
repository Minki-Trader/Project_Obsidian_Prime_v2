from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd
from interpret.glassbox import ExplainableBoostingClassifier

from foundation.models.baseline_training import LABEL_NAMES, LABEL_ORDER, validate_model_input_frame
from foundation.models.onnx_bridge import ordered_sklearn_probabilities
from foundation.models.xgboost_boosting import (
    PROBABILITY_COLUMNS,
    characteristic_score,
    nonflat_threshold,
    probability_shape_metrics,
    split_decision_metrics,
)


@dataclass(frozen=True)
class EbmVariantSpec:
    variant_id: str
    idea_id: str
    description: str
    max_bins: int
    interactions: int
    outer_bags: int
    learning_rate: float
    max_rounds: int
    early_stopping_rounds: int
    min_samples_leaf: int
    max_interaction_bins: int = 32
    reg_alpha: float = 0.0
    reg_lambda: float = 0.0
    random_state: int = 1913
    sample_weight_policy: str = "none"

    def payload(self) -> dict[str, Any]:
        return asdict(self)


def default_stage19_ebm_variants() -> list[EbmVariantSpec]:
    return [
        EbmVariantSpec(
            variant_id="v01_main_effects_broad_bins",
            idea_id="ebm_main_effect_shape_broad_bins",
            description="Main-effect EBM with moderate bin count to expose stable univariate feature shapes.",
            max_bins=128,
            interactions=0,
            outer_bags=2,
            learning_rate=0.030,
            max_rounds=350,
            early_stopping_rounds=40,
            min_samples_leaf=8,
            random_state=1913,
        ),
        EbmVariantSpec(
            variant_id="v02_main_effects_coarse_fast",
            idea_id="ebm_main_effect_shape_coarse_fast",
            description="Coarser-bin main-effect EBM stress variant for shape saturation and density cliffs.",
            max_bins=64,
            interactions=0,
            outer_bags=2,
            learning_rate=0.050,
            max_rounds=250,
            early_stopping_rounds=35,
            min_samples_leaf=16,
            reg_lambda=0.01,
            random_state=1914,
        ),
        EbmVariantSpec(
            variant_id="v03_limited_pair_shape_probe",
            idea_id="ebm_limited_pair_interaction_shape_probe",
            description="Small interaction-budget EBM to test whether limited pair terms add a new shape axis.",
            max_bins=96,
            max_interaction_bins=16,
            interactions=4,
            outer_bags=1,
            learning_rate=0.035,
            max_rounds=180,
            early_stopping_rounds=30,
            min_samples_leaf=12,
            reg_lambda=0.02,
            random_state=1915,
        ),
    ]


def _sample_weights(labels: np.ndarray, policy: str) -> np.ndarray | None:
    if policy != "balanced_classes":
        return None
    counts = {label: max(1, int((labels == label).sum())) for label in LABEL_ORDER}
    total = float(len(labels))
    return np.asarray([total / (len(LABEL_ORDER) * counts[int(label)]) for label in labels], dtype="float64")


def build_ebm_classifier(spec: EbmVariantSpec, feature_order: Sequence[str]) -> ExplainableBoostingClassifier:
    return ExplainableBoostingClassifier(
        feature_names=list(feature_order),
        max_bins=int(spec.max_bins),
        max_interaction_bins=int(spec.max_interaction_bins),
        interactions=int(spec.interactions),
        validation_size=0.15,
        outer_bags=int(spec.outer_bags),
        inner_bags=0,
        learning_rate=float(spec.learning_rate),
        max_rounds=int(spec.max_rounds),
        early_stopping_rounds=int(spec.early_stopping_rounds),
        early_stopping_tolerance=1.0e-5,
        min_samples_leaf=int(spec.min_samples_leaf),
        reg_alpha=float(spec.reg_alpha),
        reg_lambda=float(spec.reg_lambda),
        random_state=int(spec.random_state),
        n_jobs=2,
    )


def fit_ebm_variant(
    frame: pd.DataFrame,
    feature_order: Sequence[str],
    spec: EbmVariantSpec,
) -> tuple[ExplainableBoostingClassifier, dict[str, Any]]:
    features = list(feature_order)
    validate_model_input_frame(frame, features)
    train = frame.loc[frame["split"].astype(str).eq("train")].copy()
    values = train.loc[:, features]
    labels = train["label_class"].astype("int64").to_numpy()
    missing = sorted(set(LABEL_ORDER).difference(set(labels)))
    if missing:
        raise RuntimeError(f"Train split is missing label classes: {missing}")
    model = build_ebm_classifier(spec, features)
    weights = _sample_weights(labels, spec.sample_weight_policy)
    model.fit(values, labels, sample_weight=weights)
    return model, {
        "train_rows": int(len(train)),
        "feature_count": int(len(features)),
        "class_counts": {str(k): int(v) for k, v in train["label_class"].value_counts().sort_index().items()},
        "sample_weight_policy": spec.sample_weight_policy,
    }


def probability_frame(
    model: ExplainableBoostingClassifier,
    frame: pd.DataFrame,
    feature_order: Sequence[str],
) -> pd.DataFrame:
    features = list(feature_order)
    values = frame.loc[:, features]
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


def term_importance_frame(
    model: ExplainableBoostingClassifier,
    feature_order: Sequence[str],
) -> pd.DataFrame:
    importances = np.asarray(model.term_importances("avg_weight"), dtype="float64")
    total = float(np.abs(importances).sum()) or 1.0
    rows: list[dict[str, Any]] = []
    for index, value in enumerate(importances):
        term_features = tuple(int(item) for item in model.term_features_[index])
        feature_names = [str(feature_order[item]) for item in term_features]
        scores = np.asarray(model.term_scores_[index], dtype="float64")
        class_ranges: dict[str, float] = {}
        if scores.ndim >= 2 and scores.shape[-1] == len(LABEL_ORDER):
            flattened = scores.reshape((-1, len(LABEL_ORDER)))
            for class_index, label in enumerate(LABEL_ORDER):
                values = flattened[:, class_index]
                class_ranges[f"{LABEL_NAMES[int(label)]}_range"] = float(np.nanmax(values) - np.nanmin(values))
        rows.append(
            {
                "term_index": int(index),
                "term_name": str(model.term_names_[index]),
                "feature": "+".join(feature_names),
                "term_degree": int(len(term_features)),
                "importance": float(value),
                "gain": float(value),
                "gain_share": float(abs(value) / total),
                "score_abs_max": float(np.nanmax(np.abs(scores))) if scores.size else 0.0,
                "score_std": float(np.nanstd(scores)) if scores.size else 0.0,
                **class_ranges,
            }
        )
    return pd.DataFrame(rows).sort_values(["gain_share", "feature"], ascending=[False, True])


def shape_read(importance: pd.DataFrame) -> dict[str, Any]:
    if importance.empty:
        return {
            "term_count": 0,
            "interaction_term_count": 0,
            "top10_gain_share": None,
            "interaction_gain_share": None,
            "top_terms": [],
        }
    top10 = importance.head(10).copy()
    interactions = importance.loc[importance["term_degree"].astype("int64") > 1]
    return {
        "term_count": int(len(importance)),
        "interaction_term_count": int(len(interactions)),
        "top10_gain_share": float(top10["gain_share"].sum()),
        "interaction_gain_share": float(interactions["gain_share"].sum()) if not interactions.empty else 0.0,
        "top_terms": top10.to_dict(orient="records"),
    }
