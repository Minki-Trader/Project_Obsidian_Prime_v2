from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, log_loss
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


LABEL_ORDER = [0, 1, 2]
LABEL_NAMES = {0: "short", 1: "flat", 2: "long"}
REQUIRED_IDENTITY_COLUMNS = ["timestamp", "symbol", "split", "label", "label_class"]


@dataclass(frozen=True)
class BaselineTrainingConfig:
    model_family: str = "sklearn_logistic_regression_multiclass"
    scaler: str = "standard_scaler_train_split_only"
    imputation: str = "none_finite_required"
    random_seed: int = 7
    max_iter: int = 2000
    class_weight: str | None = None


def class_distribution(values: pd.Series) -> dict[str, int]:
    counts = values.astype("int64").value_counts().to_dict()
    return {LABEL_NAMES[label]: int(counts.get(label, 0)) for label in LABEL_ORDER}


def load_feature_order(path: str | bytes | "os.PathLike[str]") -> list[str]:
    with open(path, "r", encoding="utf-8") as handle:
        features = [line.strip() for line in handle if line.strip()]
    if not features:
        raise RuntimeError("Feature order file is empty.")
    if len(features) != len(set(features)):
        raise RuntimeError("Feature order contains duplicate names.")
    return features


def validate_model_input_frame(frame: pd.DataFrame, feature_order: list[str]) -> None:
    missing_identity = sorted(set(REQUIRED_IDENTITY_COLUMNS).difference(frame.columns))
    missing_features = sorted(set(feature_order).difference(frame.columns))
    if missing_identity:
        raise RuntimeError(f"Model input is missing identity columns: {missing_identity}")
    if missing_features:
        raise RuntimeError(f"Model input is missing feature columns: {missing_features}")

    split_values = set(frame["split"].astype(str).unique())
    required_splits = {"train", "validation", "oos"}
    missing_splits = sorted(required_splits.difference(split_values))
    if missing_splits:
        raise RuntimeError(f"Model input is missing required splits: {missing_splits}")

    label_values = set(frame["label_class"].astype("int64").unique())
    unexpected_labels = sorted(label_values.difference(LABEL_ORDER))
    if unexpected_labels:
        raise RuntimeError(f"Model input has unexpected label classes: {unexpected_labels}")

    feature_values = frame.loc[:, feature_order].to_numpy(dtype="float64", copy=False)
    if not np.isfinite(feature_values).all():
        raise RuntimeError("Model input contains NaN or infinite feature values.")

    timestamps = pd.to_datetime(frame["timestamp"], utc=True)
    if timestamps.duplicated().any():
        raise RuntimeError("Model input contains duplicate timestamps.")
    if not timestamps.is_monotonic_increasing:
        raise RuntimeError("Model input timestamps are not monotonic increasing.")


def train_baseline_model(
    frame: pd.DataFrame,
    feature_order: list[str],
    config: BaselineTrainingConfig,
) -> Pipeline:
    validate_model_input_frame(frame, feature_order)
    train_frame = frame.loc[frame["split"].astype(str).eq("train")]
    X_train = train_frame.loc[:, feature_order].to_numpy(dtype="float64", copy=False)
    y_train = train_frame["label_class"].astype("int64").to_numpy()
    missing_train_labels = sorted(set(LABEL_ORDER).difference(set(y_train)))
    if missing_train_labels:
        raise RuntimeError(f"Train split is missing label classes: {missing_train_labels}")

    classifier = LogisticRegression(
        max_iter=config.max_iter,
        random_state=config.random_seed,
        solver="lbfgs",
        class_weight=config.class_weight,
    )
    return Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("classifier", classifier),
        ]
    ).fit(X_train, y_train)


def ordered_predict_proba(model: Pipeline, values: np.ndarray) -> np.ndarray:
    classifier = model.named_steps["classifier"]
    raw = model.predict_proba(values)
    ordered = np.zeros((raw.shape[0], len(LABEL_ORDER)), dtype="float64")
    class_to_index = {int(label): index for index, label in enumerate(classifier.classes_)}
    for output_index, label in enumerate(LABEL_ORDER):
        if label in class_to_index:
            ordered[:, output_index] = raw[:, class_to_index[label]]
    return ordered


def evaluate_model(
    model: Pipeline,
    frame: pd.DataFrame,
    feature_order: list[str],
) -> tuple[dict[str, Any], pd.DataFrame]:
    validate_model_input_frame(frame, feature_order)
    prediction_parts: list[pd.DataFrame] = []
    metrics: dict[str, Any] = {}

    for split_name in ("train", "validation", "oos"):
        split_frame = frame.loc[frame["split"].astype(str).eq(split_name)].copy()
        X = split_frame.loc[:, feature_order].to_numpy(dtype="float64", copy=False)
        y_true = split_frame["label_class"].astype("int64").to_numpy()
        probabilities = ordered_predict_proba(model, X)
        y_pred = np.asarray(LABEL_ORDER, dtype="int64")[probabilities.argmax(axis=1)]

        metrics[split_name] = {
            "rows": int(len(split_frame)),
            "accuracy": float(accuracy_score(y_true, y_pred)),
            "balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)),
            "macro_f1": float(f1_score(y_true, y_pred, labels=LABEL_ORDER, average="macro")),
            "log_loss": float(log_loss(y_true, probabilities, labels=LABEL_ORDER)),
            "true_class_distribution": class_distribution(split_frame["label_class"]),
            "predicted_class_distribution": class_distribution(pd.Series(y_pred)),
            "mean_probability": {
                LABEL_NAMES[label]: float(probabilities[:, index].mean())
                for index, label in enumerate(LABEL_ORDER)
            },
        }

        prediction_parts.append(
            pd.DataFrame(
                {
                    "timestamp": pd.to_datetime(split_frame["timestamp"], utc=True).to_numpy(),
                    "split": split_name,
                    "label": split_frame["label"].astype(str).to_numpy(),
                    "label_class": y_true,
                    "predicted_label_class": y_pred,
                    "predicted_label": [LABEL_NAMES[int(value)] for value in y_pred],
                    "p_short": probabilities[:, 0],
                    "p_flat": probabilities[:, 1],
                    "p_long": probabilities[:, 2],
                }
            )
        )

    predictions = pd.concat(prediction_parts, ignore_index=True)
    probability_values = predictions[["p_short", "p_flat", "p_long"]].to_numpy(dtype="float64", copy=False)
    metrics["probability_checks"] = {
        "finite": bool(np.isfinite(probability_values).all()),
        "row_sum_max_abs_error": float(np.abs(probability_values.sum(axis=1) - 1.0).max()),
    }
    return metrics, predictions


def coefficient_importance(model: Pipeline, feature_order: list[str]) -> pd.DataFrame:
    classifier = model.named_steps["classifier"]
    coefficients = np.asarray(classifier.coef_, dtype="float64")
    rows = []
    for index, feature_name in enumerate(feature_order):
        per_class = {
            f"coef_{LABEL_NAMES[int(label)]}": float(coefficients[class_index, index])
            for class_index, label in enumerate(classifier.classes_)
        }
        abs_values = np.abs(coefficients[:, index])
        rows.append(
            {
                "feature": feature_name,
                "max_abs_coef": float(abs_values.max()),
                "mean_abs_coef": float(abs_values.mean()),
                **per_class,
            }
        )
    return pd.DataFrame(rows).sort_values(["max_abs_coef", "feature"], ascending=[False, True])
