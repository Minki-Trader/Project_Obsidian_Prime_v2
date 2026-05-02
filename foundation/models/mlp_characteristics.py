from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Sequence

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, log_loss
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from foundation.models.baseline_training import LABEL_NAMES, LABEL_ORDER, validate_model_input_frame
from foundation.models.onnx_bridge import ordered_sklearn_probabilities


PROBABILITY_COLUMNS = ("p_short", "p_flat", "p_long")


@dataclass(frozen=True)
class MlpVariantSpec:
    variant_id: str
    idea_id: str
    description: str
    hidden_layer_sizes: tuple[int, ...]
    activation: str = "relu"
    alpha: float = 0.001
    learning_rate_init: float = 0.001
    max_iter: int = 160
    n_iter_no_change: int = 12
    validation_fraction: float = 0.12
    random_state: int = 1307

    def payload(self) -> dict[str, Any]:
        return asdict(self)


def default_mlp_characteristic_specs() -> list[MlpVariantSpec]:
    return [
        MlpVariantSpec(
            variant_id="v01_small_relu_l2",
            idea_id="small_relu_capacity",
            description="Small single hidden layer ReLU shape.",
            hidden_layer_sizes=(32,),
            activation="relu",
            alpha=0.001,
            random_state=1307,
        ),
        MlpVariantSpec(
            variant_id="v02_wide_relu_l2",
            idea_id="wide_relu_capacity",
            description="Wider single hidden layer ReLU shape.",
            hidden_layer_sizes=(96,),
            activation="relu",
            alpha=0.001,
            random_state=1308,
        ),
        MlpVariantSpec(
            variant_id="v03_deep_relu_l2",
            idea_id="two_layer_relu_shape",
            description="Two hidden layer ReLU shape.",
            hidden_layer_sizes=(64, 32),
            activation="relu",
            alpha=0.001,
            random_state=1309,
        ),
        MlpVariantSpec(
            variant_id="v04_tanh_medium_l2",
            idea_id="tanh_activation_shape",
            description="Tanh activation with medium capacity.",
            hidden_layer_sizes=(64,),
            activation="tanh",
            alpha=0.001,
            random_state=1310,
        ),
        MlpVariantSpec(
            variant_id="v05_regularized_relu",
            idea_id="relu_regularization_shape",
            description="Medium ReLU with stronger L2 regularization.",
            hidden_layer_sizes=(64,),
            activation="relu",
            alpha=0.01,
            random_state=1311,
        ),
    ]


def build_mlp_pipeline(spec: MlpVariantSpec) -> Pipeline:
    classifier = MLPClassifier(
        hidden_layer_sizes=spec.hidden_layer_sizes,
        activation=spec.activation,
        solver="adam",
        alpha=float(spec.alpha),
        batch_size=512,
        learning_rate="adaptive",
        learning_rate_init=float(spec.learning_rate_init),
        max_iter=int(spec.max_iter),
        random_state=int(spec.random_state),
        tol=1e-4,
        n_iter_no_change=int(spec.n_iter_no_change),
        early_stopping=True,
        validation_fraction=float(spec.validation_fraction),
    )
    return Pipeline([("scaler", StandardScaler()), ("classifier", classifier)])


def fit_mlp_variant(frame: pd.DataFrame, feature_order: Sequence[str], spec: MlpVariantSpec) -> Pipeline:
    feature_names = list(feature_order)
    validate_model_input_frame(frame, feature_names)
    train_frame = frame.loc[frame["split"].astype(str).eq("train")]
    X_train = train_frame.loc[:, feature_names].to_numpy(dtype="float64", copy=False)
    y_train = train_frame["label_class"].astype("int64").to_numpy()
    missing_train_labels = sorted(set(LABEL_ORDER).difference(set(y_train)))
    if missing_train_labels:
        raise RuntimeError(f"Train split is missing label classes: {missing_train_labels}")
    return build_mlp_pipeline(spec).fit(X_train, y_train)


def probability_frame(model: Pipeline, frame: pd.DataFrame, feature_order: Sequence[str]) -> pd.DataFrame:
    feature_names = list(feature_order)
    values = frame.loc[:, feature_names].to_numpy(dtype="float64", copy=False)
    probabilities = ordered_sklearn_probabilities(model, values)
    payload = pd.DataFrame(
        {
            "timestamp": pd.to_datetime(frame["timestamp"], utc=True).to_numpy(),
            "split": frame["split"].astype(str).to_numpy(),
            "label_class": frame["label_class"].astype("int64").to_numpy(),
            "p_short": probabilities[:, 0],
            "p_flat": probabilities[:, 1],
            "p_long": probabilities[:, 2],
        }
    )
    if "partial_context_subtype" in frame.columns:
        payload["partial_context_subtype"] = frame["partial_context_subtype"].astype(str).to_numpy()
    return payload


def nonflat_threshold(prob_frame: pd.DataFrame, quantile: float) -> float:
    validation = prob_frame.loc[prob_frame["split"].astype(str).eq("validation")]
    if validation.empty:
        raise RuntimeError("Validation split is empty; cannot select non-flat threshold.")
    confidence = validation.loc[:, ["p_short", "p_long"]].max(axis=1)
    return float(np.quantile(confidence.to_numpy(dtype="float64"), float(quantile)))


def threshold_decisions(prob_frame: pd.DataFrame, threshold: float) -> np.ndarray:
    p_short = prob_frame["p_short"].to_numpy(dtype="float64")
    p_long = prob_frame["p_long"].to_numpy(dtype="float64")
    decision = np.full(len(prob_frame), 1, dtype="int64")
    short_ok = (p_short >= p_long) & (p_short >= threshold)
    long_ok = (p_long > p_short) & (p_long >= threshold)
    decision[short_ok] = 0
    decision[long_ok] = 2
    return decision


def split_decision_metrics(prob_frame: pd.DataFrame, threshold: float) -> dict[str, Any]:
    metrics: dict[str, Any] = {}
    for split_name in ("train", "validation", "oos"):
        split = prob_frame.loc[prob_frame["split"].astype(str).eq(split_name)].copy()
        decision = threshold_decisions(split, threshold)
        labels = split["label_class"].astype("int64").to_numpy()
        signals = decision != 1
        probabilities = split.loc[:, list(PROBABILITY_COLUMNS)].to_numpy(dtype="float64", copy=False)
        predicted = np.asarray(LABEL_ORDER, dtype="int64")[probabilities.argmax(axis=1)]
        metrics[split_name] = {
            "rows": int(len(split)),
            "accuracy": float(accuracy_score(labels, predicted)) if len(split) else None,
            "balanced_accuracy": float(balanced_accuracy_score(labels, predicted)) if len(split) else None,
            "macro_f1": float(f1_score(labels, predicted, labels=LABEL_ORDER, average="macro")) if len(split) else None,
            "log_loss": float(log_loss(labels, probabilities, labels=LABEL_ORDER)) if len(split) else None,
            "signal_count": int(signals.sum()),
            "short_count": int((decision == 0).sum()),
            "long_count": int((decision == 2).sum()),
            "signal_coverage": float(signals.mean()) if len(split) else None,
            "directional_correct_count": int((decision[signals] == labels[signals]).sum()) if signals.any() else 0,
            "directional_hit_rate": float((decision[signals] == labels[signals]).mean()) if signals.any() else None,
            "mean_probability": {
                LABEL_NAMES[label]: float(probabilities[:, index].mean()) if len(split) else None
                for index, label in enumerate(LABEL_ORDER)
            },
        }
    probability_values = prob_frame.loc[:, list(PROBABILITY_COLUMNS)].to_numpy(dtype="float64", copy=False)
    metrics["probability_checks"] = {
        "finite": bool(np.isfinite(probability_values).all()),
        "row_sum_max_abs_error": float(np.abs(probability_values.sum(axis=1) - 1.0).max()) if len(probability_values) else 0.0,
    }
    return metrics


def probability_shape_metrics(prob_frame: pd.DataFrame) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    for split_name in ("train", "validation", "oos"):
        split = prob_frame.loc[prob_frame["split"].astype(str).eq(split_name)]
        values = split.loc[:, list(PROBABILITY_COLUMNS)].to_numpy(dtype="float64", copy=False)
        if not len(values):
            payload[split_name] = {"rows": 0}
            continue
        clipped = np.clip(values, 1e-12, 1.0)
        entropy = -(clipped * np.log(clipped)).sum(axis=1)
        nonflat = values[:, [0, 2]].max(axis=1)
        payload[split_name] = {
            "rows": int(len(values)),
            "mean_entropy": float(entropy.mean()),
            "mean_max_probability": float(values.max(axis=1).mean()),
            "nonflat_p50": float(np.quantile(nonflat, 0.50)),
            "nonflat_p90": float(np.quantile(nonflat, 0.90)),
            "flat_mean": float(values[:, 1].mean()),
        }
    return payload


def classifier_training_diagnostics(model: Pipeline) -> dict[str, Any]:
    classifier = model.named_steps["classifier"]
    return {
        "classes": [int(value) for value in classifier.classes_],
        "n_iter": int(classifier.n_iter_),
        "loss": float(classifier.loss_),
        "best_validation_score": float(getattr(classifier, "best_validation_score_", np.nan)),
        "hidden_layer_sizes": tuple(int(value) for value in classifier.hidden_layer_sizes),
        "activation": str(classifier.activation),
        "alpha": float(classifier.alpha),
        "learning_rate_init": float(classifier.learning_rate_init),
        "early_stopping": bool(classifier.early_stopping),
    }
