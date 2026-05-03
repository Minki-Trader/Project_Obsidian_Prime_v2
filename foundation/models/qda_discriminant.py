from __future__ import annotations

import warnings
from dataclasses import asdict, dataclass
from typing import Any, Sequence

import numpy as np
import pandas as pd
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, log_loss
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from foundation.models.baseline_training import LABEL_NAMES, LABEL_ORDER, validate_model_input_frame
from foundation.models.onnx_bridge import ordered_sklearn_probabilities


PROBABILITY_COLUMNS = ("p_short", "p_flat", "p_long")


@dataclass(frozen=True)
class QdaRunSpec:
    run_number: str
    run_id: str
    variant_id: str
    idea_id: str
    description: str
    reg_param: float
    priors: tuple[float, float, float] | None = None
    tol: float = 0.0001
    rows_per_class: int = 600
    tier_a_feature_mode: str = "full58"
    random_state: int = 1800

    def payload(self) -> dict[str, Any]:
        payload = asdict(self)
        if self.priors is not None:
            payload["priors"] = list(self.priors)
        return payload


def default_stage16_qda_specs() -> list[QdaRunSpec]:
    equal_priors = (1.0 / 3.0, 1.0 / 3.0, 1.0 / 3.0)
    return [
        QdaRunSpec(
            run_number="run08A",
            run_id="run08A_qda_near_raw_covariance_empirical_priors_characterization_v1",
            variant_id="v01_near_raw_covariance_empirical_priors",
            idea_id="near_raw_class_covariance_shape",
            description="QDA with near-raw class covariance and empirical class priors.",
            reg_param=0.001,
            random_state=1801,
        ),
        QdaRunSpec(
            run_number="run08B",
            run_id="run08B_qda_near_raw_balanced_priors_characterization_v1",
            variant_id="v02_near_raw_balanced_priors",
            idea_id="class_prior_policy_shape",
            description="QDA with equal class priors and near-raw covariance.",
            reg_param=0.001,
            priors=equal_priors,
            random_state=1802,
        ),
        QdaRunSpec(
            run_number="run08C",
            run_id="run08C_qda_micro_regularization003_characterization_v1",
            variant_id="v03_micro_regularization003",
            idea_id="micro_regularization_floor",
            description="QDA with tiny covariance regularization.",
            reg_param=0.003,
            random_state=1803,
        ),
        QdaRunSpec(
            run_number="run08D",
            run_id="run08D_qda_light_regularization010_characterization_v1",
            variant_id="v04_light_regularization010",
            idea_id="light_regularization_shape",
            description="QDA with light covariance regularization.",
            reg_param=0.01,
            random_state=1804,
        ),
        QdaRunSpec(
            run_number="run08E",
            run_id="run08E_qda_lda_anchor_regularization050_characterization_v1",
            variant_id="v05_lda_anchor_regularization050",
            idea_id="lda_shrinkage_anchor_transfer",
            description="QDA near the Stage15 LDA light shrinkage clue.",
            reg_param=0.05,
            random_state=1805,
        ),
        QdaRunSpec(
            run_number="run08F",
            run_id="run08F_qda_moderate_regularization150_characterization_v1",
            variant_id="v06_moderate_regularization150",
            idea_id="moderate_regularization_shape",
            description="QDA with stronger covariance regularization.",
            reg_param=0.15,
            random_state=1806,
        ),
        QdaRunSpec(
            run_number="run08G",
            run_id="run08G_qda_small_sample300_characterization_v1",
            variant_id="v07_small_sample300_reg050",
            idea_id="small_sample_covariance_fragility",
            description="QDA with fewer train rows per class under the anchor regularization.",
            reg_param=0.05,
            rows_per_class=300,
            random_state=1807,
        ),
        QdaRunSpec(
            run_number="run08H",
            run_id="run08H_qda_large_sample1200_characterization_v1",
            variant_id="v08_large_sample1200_reg050",
            idea_id="larger_sample_covariance_stability",
            description="QDA with more train rows per class under the anchor regularization.",
            reg_param=0.05,
            rows_per_class=1200,
            random_state=1808,
        ),
        QdaRunSpec(
            run_number="run08I",
            run_id="run08I_qda_core42_feature_geometry_characterization_v1",
            variant_id="v09_core42_feature_geometry_reg050",
            idea_id="core_feature_covariance_geometry",
            description="QDA on the core price/session feature surface.",
            reg_param=0.05,
            tier_a_feature_mode="core42",
            random_state=1809,
        ),
        QdaRunSpec(
            run_number="run08J",
            run_id="run08J_qda_external16_feature_geometry_characterization_v1",
            variant_id="v10_external16_feature_geometry_reg050",
            idea_id="external_context_covariance_geometry",
            description="QDA on macro and mega-cap proxy context features.",
            reg_param=0.05,
            tier_a_feature_mode="external16",
            random_state=1810,
        ),
    ]


def build_qda_pipeline(spec: QdaRunSpec) -> Pipeline:
    classifier = QuadraticDiscriminantAnalysis(
        priors=list(spec.priors) if spec.priors is not None else None,
        reg_param=float(spec.reg_param),
        store_covariance=True,
        tol=float(spec.tol),
    )
    return Pipeline([("scaler", StandardScaler()), ("classifier", classifier)])


def stratified_train_sample(frame: pd.DataFrame, *, rows_per_class: int, random_state: int) -> pd.DataFrame:
    train_frame = frame.loc[frame["split"].astype(str).eq("train")].copy()
    samples: list[pd.DataFrame] = []
    for label, group in train_frame.groupby("label_class", sort=True):
        count = min(int(rows_per_class), len(group))
        samples.append(group.sample(n=count, random_state=int(random_state) + int(label)))
    return pd.concat(samples, ignore_index=True).sort_values("timestamp").reset_index(drop=True)


def fit_qda_variant(
    frame: pd.DataFrame,
    feature_order: Sequence[str],
    spec: QdaRunSpec,
) -> tuple[Pipeline, dict[str, Any]]:
    feature_names = list(feature_order)
    validate_model_input_frame(frame, feature_names)
    train_sample = stratified_train_sample(
        frame,
        rows_per_class=spec.rows_per_class,
        random_state=int(spec.random_state),
    )
    values = train_sample.loc[:, feature_names].to_numpy(dtype="float64", copy=False)
    labels = train_sample["label_class"].astype("int64").to_numpy()
    missing = sorted(set(LABEL_ORDER).difference(set(labels)))
    if missing:
        raise RuntimeError(f"Train sample is missing label classes: {missing}")
    model = build_qda_pipeline(spec)
    with warnings.catch_warnings(record=True) as captured:
        warnings.simplefilter("always")
        model.fit(values, labels)
    sample_info = {
        "train_sample_rows": int(len(train_sample)),
        "rows_per_class_cap": int(spec.rows_per_class),
        "feature_count": int(len(feature_names)),
        "class_counts": {str(k): int(v) for k, v in train_sample["label_class"].value_counts().sort_index().items()},
        "fit_warnings": [str(item.message) for item in captured],
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
    short_prob = prob_frame["p_short"].to_numpy(dtype="float64")
    long_prob = prob_frame["p_long"].to_numpy(dtype="float64")
    decision = np.full(len(prob_frame), 1, dtype="int64")
    short_ok = (short_prob >= long_prob) & (short_prob >= threshold)
    long_ok = (long_prob > short_prob) & (long_prob >= threshold)
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
    classifier: QuadraticDiscriminantAnalysis = model.named_steps["classifier"]
    covariance_diagnostics: dict[str, Any] = {}
    covariances = getattr(classifier, "covariance_", [])
    for label, covariance in zip(classifier.classes_, covariances):
        values = np.asarray(covariance, dtype="float64")
        eigenvalues = np.linalg.eigvalsh(values)
        positive = eigenvalues[eigenvalues > 1e-12]
        covariance_diagnostics[LABEL_NAMES[int(label)]] = {
            "min_eigenvalue": float(eigenvalues.min()) if len(eigenvalues) else None,
            "max_eigenvalue": float(eigenvalues.max()) if len(eigenvalues) else None,
            "positive_rank": int(len(positive)),
            "condition_number_positive": float(positive.max() / positive.min()) if len(positive) else None,
        }
    return {
        "classifier_type": type(classifier).__name__,
        "reg_param": float(classifier.reg_param),
        "tol": float(classifier.tol),
        "priors": [float(value) for value in classifier.priors_],
        "classes": [int(value) for value in classifier.classes_],
        "covariance_diagnostics": covariance_diagnostics,
    }


def shape_score(result: dict[str, Any]) -> float:
    metrics = result.get("metrics", {})
    shape = result.get("probability_shape", {})
    validation = metrics.get("validation", {})
    oos = metrics.get("oos", {})
    val_cov = float(validation.get("signal_coverage") or 0.0)
    oos_cov = float(oos.get("signal_coverage") or 0.0)
    val_entropy = float(shape.get("validation", {}).get("mean_entropy") or 0.0)
    oos_entropy = float(shape.get("oos", {}).get("mean_entropy") or 0.0)
    val_margin = float(shape.get("validation", {}).get("probability_margin_mean") or 0.0)
    oos_margin = float(shape.get("oos", {}).get("probability_margin_mean") or 0.0)
    density = 1.0 - min(abs(val_cov - 0.10) / 0.10, 1.0)
    density_stability = 1.0 - min(abs(val_cov - oos_cov) / 0.18, 1.0)
    entropy_stability = 1.0 - min(abs(val_entropy - oos_entropy) / 0.18, 1.0)
    margin_presence = min((val_margin + oos_margin) / 0.16, 1.0)
    margin_stability = 1.0 - min(abs(val_margin - oos_margin) / 0.08, 1.0)
    return float(
        0.25 * density
        + 0.25 * density_stability
        + 0.20 * entropy_stability
        + 0.20 * margin_presence
        + 0.10 * margin_stability
    )
