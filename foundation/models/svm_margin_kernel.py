from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Sequence

import numpy as np
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, log_loss
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC, SVC

from foundation.models.baseline_training import LABEL_NAMES, LABEL_ORDER, validate_model_input_frame
from foundation.models.onnx_bridge import ordered_sklearn_probabilities


PROBABILITY_COLUMNS = ("p_short", "p_flat", "p_long")


@dataclass(frozen=True)
class SvmVariantSpec:
    variant_id: str
    idea_id: str
    description: str
    kernel: str
    c_value: float
    gamma: str | float = "scale"
    calibrated_linear: bool = False
    max_iter: int = 5000
    random_state: int = 1405

    def payload(self) -> dict[str, Any]:
        return asdict(self)


def default_svm_margin_kernel_specs() -> list[SvmVariantSpec]:
    return [
        SvmVariantSpec(
            variant_id="v01_linear_margin_c025",
            idea_id="linear_margin_regularized",
            description="Regularized linear SVM margin read.",
            kernel="linear",
            c_value=0.25,
            calibrated_linear=True,
            random_state=1405,
        ),
        SvmVariantSpec(
            variant_id="v02_linear_margin_c100",
            idea_id="linear_margin_less_regularized",
            description="Less-regularized linear SVM margin boundary read.",
            kernel="linear",
            c_value=1.0,
            calibrated_linear=True,
            random_state=1406,
        ),
        SvmVariantSpec(
            variant_id="v03_rbf_kernel_c050_scale",
            idea_id="rbf_kernel_geometry",
            description="RBF kernel probability and margin shape read.",
            kernel="rbf",
            c_value=0.5,
            gamma="scale",
            random_state=1407,
        ),
        SvmVariantSpec(
            variant_id="v04_sigmoid_boundary_c050_scale",
            idea_id="sigmoid_kernel_boundary",
            description="Sigmoid kernel failure-boundary read.",
            kernel="sigmoid",
            c_value=0.5,
            gamma="scale",
            random_state=1408,
        ),
    ]


def build_svm_pipeline(spec: SvmVariantSpec) -> Pipeline:
    if spec.calibrated_linear:
        estimator = LinearSVC(
            C=float(spec.c_value),
            class_weight="balanced",
            max_iter=int(spec.max_iter),
            random_state=int(spec.random_state),
        )
        classifier = CalibratedClassifierCV(estimator=estimator, cv=3)
    else:
        classifier = SVC(
            C=float(spec.c_value),
            kernel=str(spec.kernel),
            gamma=spec.gamma,
            probability=True,
            class_weight="balanced",
            cache_size=512,
            decision_function_shape="ovr",
            random_state=int(spec.random_state),
        )
    return Pipeline([("scaler", StandardScaler()), ("classifier", classifier)])


def stratified_train_sample(
    frame: pd.DataFrame,
    *,
    rows_per_class: int = 2000,
    random_state: int = 1405,
) -> pd.DataFrame:
    train_frame = frame.loc[frame["split"].astype(str).eq("train")].copy()
    samples: list[pd.DataFrame] = []
    for label, group in train_frame.groupby("label_class", sort=True):
        count = min(int(rows_per_class), len(group))
        samples.append(group.sample(n=count, random_state=int(random_state) + int(label)))
    return pd.concat(samples, ignore_index=True).sort_values("timestamp").reset_index(drop=True)


def fit_svm_variant(
    frame: pd.DataFrame,
    feature_order: Sequence[str],
    spec: SvmVariantSpec,
    *,
    rows_per_class: int = 2000,
) -> tuple[Pipeline, dict[str, Any]]:
    feature_names = list(feature_order)
    validate_model_input_frame(frame, feature_names)
    train_sample = stratified_train_sample(
        frame,
        rows_per_class=rows_per_class,
        random_state=int(spec.random_state),
    )
    X_train = train_sample.loc[:, feature_names].to_numpy(dtype="float64", copy=False)
    y_train = train_sample["label_class"].astype("int64").to_numpy()
    missing = sorted(set(LABEL_ORDER).difference(set(y_train)))
    if missing:
        raise RuntimeError(f"Train sample is missing label classes: {missing}")
    model = build_svm_pipeline(spec).fit(X_train, y_train)
    sample_info = {
        "train_sample_rows": int(len(train_sample)),
        "rows_per_class_cap": int(rows_per_class),
        "class_counts": {str(k): int(v) for k, v in train_sample["label_class"].value_counts().sort_index().items()},
    }
    return model, sample_info


def _decision_values(model: Pipeline, values: np.ndarray) -> np.ndarray | None:
    if not hasattr(model, "decision_function"):
        return None
    try:
        raw = np.asarray(model.decision_function(values), dtype="float64")
    except Exception:
        return None
    if raw.ndim == 1:
        raw = raw.reshape(-1, 1)
    return raw


def probability_frame(model: Pipeline, frame: pd.DataFrame, feature_order: Sequence[str]) -> pd.DataFrame:
    feature_names = list(feature_order)
    values = frame.loc[:, feature_names].to_numpy(dtype="float64", copy=False)
    probabilities = ordered_sklearn_probabilities(model, values)
    sorted_probabilities = np.sort(probabilities, axis=1)
    probability_margin = sorted_probabilities[:, -1] - sorted_probabilities[:, -2]
    decision = _decision_values(model, values)
    if decision is None or decision.shape[1] < 2:
        decision_margin = np.full(len(probabilities), np.nan, dtype="float64")
    else:
        sorted_decision = np.sort(decision, axis=1)
        decision_margin = sorted_decision[:, -1] - sorted_decision[:, -2]
    payload = pd.DataFrame(
        {
            "timestamp": pd.to_datetime(frame["timestamp"], utc=True).to_numpy(),
            "split": frame["split"].astype(str).to_numpy(),
            "label_class": frame["label_class"].astype("int64").to_numpy(),
            "p_short": probabilities[:, 0],
            "p_flat": probabilities[:, 1],
            "p_long": probabilities[:, 2],
            "probability_margin": probability_margin,
            "decision_margin": decision_margin,
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
            "mean_probability_margin": float(split["probability_margin"].mean()) if len(split) else None,
            "mean_decision_margin": float(split["decision_margin"].mean(skipna=True)) if len(split) else None,
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
            "probability_margin_mean": float(split["probability_margin"].mean()),
            "decision_margin_mean": float(split["decision_margin"].mean(skipna=True)),
        }
    return payload


def classifier_training_diagnostics(model: Pipeline) -> dict[str, Any]:
    classifier = model.named_steps["classifier"]
    payload: dict[str, Any] = {
        "classifier_type": type(classifier).__name__,
        "classes": [int(value) for value in classifier.classes_],
    }
    if isinstance(classifier, SVC):
        payload.update(
            {
                "kernel": str(classifier.kernel),
                "c_value": float(classifier.C),
                "gamma": classifier.gamma,
                "support_vectors": int(classifier.support_vectors_.shape[0]),
                "n_support": [int(value) for value in classifier.n_support_],
                "probability": bool(classifier.probability),
            }
        )
    elif isinstance(classifier, CalibratedClassifierCV):
        payload.update(
            {
                "calibrated_linear": True,
                "calibration_cv": int(classifier.cv),
                "estimator_type": type(classifier.estimator).__name__,
            }
        )
    return payload
