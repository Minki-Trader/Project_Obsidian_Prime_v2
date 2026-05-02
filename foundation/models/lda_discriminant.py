from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Sequence

import numpy as np
import pandas as pd
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, log_loss
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from foundation.models.baseline_training import LABEL_NAMES, LABEL_ORDER, validate_model_input_frame
from foundation.models.onnx_bridge import ordered_sklearn_probabilities


PROBABILITY_COLUMNS = ("p_short", "p_flat", "p_long")


@dataclass(frozen=True)
class LdaRunSpec:
    run_number: str
    run_id: str
    variant_id: str
    idea_id: str
    description: str
    solver: str
    shrinkage: str | float | None = None
    priors: tuple[float, float, float] | None = None
    tol: float = 0.0001
    random_state: int = 1500

    def payload(self) -> dict[str, Any]:
        payload = asdict(self)
        if self.priors is not None:
            payload["priors"] = list(self.priors)
        return payload


def default_stage15_lda_specs() -> list[LdaRunSpec]:
    return [
        LdaRunSpec(
            run_number="run06A",
            run_id="run06A_lda_svd_empirical_priors_runtime_probe_v1",
            variant_id="v01_svd_empirical_priors",
            idea_id="svd_empirical_prior_geometry",
            description="SVD LDA with empirical class priors.",
            solver="svd",
            random_state=1501,
        ),
        LdaRunSpec(
            run_number="run06B",
            run_id="run06B_lda_svd_balanced_priors_runtime_probe_v1",
            variant_id="v02_svd_balanced_priors",
            idea_id="prior_sensitivity",
            description="SVD LDA with equal class priors.",
            solver="svd",
            priors=(1.0 / 3.0, 1.0 / 3.0, 1.0 / 3.0),
            random_state=1502,
        ),
        LdaRunSpec(
            run_number="run06C",
            run_id="run06C_lda_svd_rank_tolerant_runtime_probe_v1",
            variant_id="v03_svd_rank_tolerant",
            idea_id="rank_tolerance_sensitivity",
            description="SVD LDA with looser singular-value tolerance.",
            solver="svd",
            tol=0.01,
            random_state=1503,
        ),
        LdaRunSpec(
            run_number="run06D",
            run_id="run06D_lda_lsqr_no_shrinkage_runtime_probe_v1",
            variant_id="v04_lsqr_no_shrinkage",
            idea_id="least_squares_covariance_raw",
            description="LSQR LDA without covariance shrinkage.",
            solver="lsqr",
            shrinkage=None,
            random_state=1504,
        ),
        LdaRunSpec(
            run_number="run06E",
            run_id="run06E_lda_lsqr_auto_shrinkage_runtime_probe_v1",
            variant_id="v05_lsqr_auto_shrinkage",
            idea_id="least_squares_auto_shrinkage",
            description="LSQR LDA with automatic covariance shrinkage.",
            solver="lsqr",
            shrinkage="auto",
            random_state=1505,
        ),
        LdaRunSpec(
            run_number="run06F",
            run_id="run06F_lda_lsqr_shrinkage020_runtime_probe_v1",
            variant_id="v06_lsqr_shrinkage020",
            idea_id="least_squares_light_shrinkage",
            description="LSQR LDA with light fixed covariance shrinkage.",
            solver="lsqr",
            shrinkage=0.20,
            random_state=1506,
        ),
        LdaRunSpec(
            run_number="run06G",
            run_id="run06G_lda_lsqr_shrinkage080_runtime_probe_v1",
            variant_id="v07_lsqr_shrinkage080",
            idea_id="least_squares_heavy_shrinkage",
            description="LSQR LDA with heavy fixed covariance shrinkage.",
            solver="lsqr",
            shrinkage=0.80,
            random_state=1507,
        ),
        LdaRunSpec(
            run_number="run06H",
            run_id="run06H_lda_eigen_light_shrinkage_runtime_probe_v1",
            variant_id="v08_eigen_shrinkage005",
            idea_id="eigen_light_shrinkage",
            description="Eigen LDA with minimal stable covariance shrinkage.",
            solver="eigen",
            shrinkage=0.05,
            random_state=1508,
        ),
        LdaRunSpec(
            run_number="run06I",
            run_id="run06I_lda_eigen_auto_shrinkage_runtime_probe_v1",
            variant_id="v09_eigen_auto_shrinkage",
            idea_id="eigen_auto_shrinkage",
            description="Eigen LDA with automatic covariance shrinkage.",
            solver="eigen",
            shrinkage="auto",
            random_state=1509,
        ),
        LdaRunSpec(
            run_number="run06J",
            run_id="run06J_lda_eigen_balanced_shrinkage050_runtime_probe_v1",
            variant_id="v10_eigen_balanced_shrinkage050",
            idea_id="eigen_prior_and_shrinkage_combo",
            description="Eigen LDA with equal priors and medium covariance shrinkage.",
            solver="eigen",
            shrinkage=0.50,
            priors=(1.0 / 3.0, 1.0 / 3.0, 1.0 / 3.0),
            random_state=1510,
        ),
    ]


def stage15_lda_covariance_stability_specs() -> list[LdaRunSpec]:
    fixed_sample_seed = 1700
    return [
        LdaRunSpec(
            run_number="run07A",
            run_id="run07A_lda_eigen_shrinkage001_stability_probe_v1",
            variant_id="v11_eigen_shrinkage001",
            idea_id="eigen_shrinkage_curve_001",
            description="Eigen LDA with very light covariance shrinkage.",
            solver="eigen",
            shrinkage=0.01,
            random_state=fixed_sample_seed,
        ),
        LdaRunSpec(
            run_number="run07B",
            run_id="run07B_lda_eigen_shrinkage003_stability_probe_v1",
            variant_id="v12_eigen_shrinkage003",
            idea_id="eigen_shrinkage_curve_003",
            description="Eigen LDA with light covariance shrinkage below the run06H anchor.",
            solver="eigen",
            shrinkage=0.03,
            random_state=fixed_sample_seed,
        ),
        LdaRunSpec(
            run_number="run07C",
            run_id="run07C_lda_eigen_shrinkage005_stability_probe_v1",
            variant_id="v13_eigen_shrinkage005",
            idea_id="eigen_shrinkage_curve_005_anchor",
            description="Eigen LDA with the run06H shrinkage value under a fixed comparison sample.",
            solver="eigen",
            shrinkage=0.05,
            random_state=fixed_sample_seed,
        ),
        LdaRunSpec(
            run_number="run07D",
            run_id="run07D_lda_eigen_shrinkage008_stability_probe_v1",
            variant_id="v14_eigen_shrinkage008",
            idea_id="eigen_shrinkage_curve_008",
            description="Eigen LDA with slightly stronger covariance shrinkage.",
            solver="eigen",
            shrinkage=0.08,
            random_state=fixed_sample_seed,
        ),
        LdaRunSpec(
            run_number="run07E",
            run_id="run07E_lda_eigen_shrinkage012_stability_probe_v1",
            variant_id="v15_eigen_shrinkage012",
            idea_id="eigen_shrinkage_curve_012",
            description="Eigen LDA with moderate covariance shrinkage.",
            solver="eigen",
            shrinkage=0.12,
            random_state=fixed_sample_seed,
        ),
        LdaRunSpec(
            run_number="run07F",
            run_id="run07F_lda_eigen_shrinkage020_stability_probe_v1",
            variant_id="v16_eigen_shrinkage020",
            idea_id="eigen_shrinkage_curve_020",
            description="Eigen LDA with stronger covariance shrinkage.",
            solver="eigen",
            shrinkage=0.20,
            random_state=fixed_sample_seed,
        ),
        LdaRunSpec(
            run_number="run07G",
            run_id="run07G_lda_lsqr_shrinkage003_stability_probe_v1",
            variant_id="v17_lsqr_shrinkage003",
            idea_id="lsqr_solver_comparison_003",
            description="LSQR LDA matched to the light eigen shrinkage point.",
            solver="lsqr",
            shrinkage=0.03,
            random_state=fixed_sample_seed,
        ),
        LdaRunSpec(
            run_number="run07H",
            run_id="run07H_lda_lsqr_shrinkage005_stability_probe_v1",
            variant_id="v18_lsqr_shrinkage005",
            idea_id="lsqr_solver_comparison_005",
            description="LSQR LDA matched to the run06H shrinkage point.",
            solver="lsqr",
            shrinkage=0.05,
            random_state=fixed_sample_seed,
        ),
        LdaRunSpec(
            run_number="run07I",
            run_id="run07I_lda_lsqr_shrinkage008_stability_probe_v1",
            variant_id="v19_lsqr_shrinkage008",
            idea_id="lsqr_solver_comparison_008",
            description="LSQR LDA matched to the stronger eigen shrinkage point.",
            solver="lsqr",
            shrinkage=0.08,
            random_state=fixed_sample_seed,
        ),
        LdaRunSpec(
            run_number="run07J",
            run_id="run07J_lda_eigen_balanced_shrinkage005_stability_probe_v1",
            variant_id="v20_eigen_balanced_shrinkage005",
            idea_id="prior_policy_at_stable_shrinkage",
            description="Eigen LDA at the light shrinkage anchor with equal class priors.",
            solver="eigen",
            shrinkage=0.05,
            priors=(1.0 / 3.0, 1.0 / 3.0, 1.0 / 3.0),
            random_state=fixed_sample_seed,
        ),
    ]


def build_lda_pipeline(spec: LdaRunSpec) -> Pipeline:
    kwargs: dict[str, Any] = {"solver": spec.solver, "tol": float(spec.tol)}
    if spec.solver in {"lsqr", "eigen"}:
        kwargs["shrinkage"] = spec.shrinkage
    if spec.priors is not None:
        kwargs["priors"] = list(spec.priors)
    classifier = LinearDiscriminantAnalysis(**kwargs)
    return Pipeline([("scaler", StandardScaler()), ("classifier", classifier)])


def stratified_train_sample(frame: pd.DataFrame, *, rows_per_class: int, random_state: int) -> pd.DataFrame:
    train_frame = frame.loc[frame["split"].astype(str).eq("train")].copy()
    samples: list[pd.DataFrame] = []
    for label, group in train_frame.groupby("label_class", sort=True):
        count = min(int(rows_per_class), len(group))
        samples.append(group.sample(n=count, random_state=int(random_state) + int(label)))
    return pd.concat(samples, ignore_index=True).sort_values("timestamp").reset_index(drop=True)


def fit_lda_variant(
    frame: pd.DataFrame,
    feature_order: Sequence[str],
    spec: LdaRunSpec,
    *,
    rows_per_class: int,
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
    model = build_lda_pipeline(spec).fit(X_train, y_train)
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
    classifier: LinearDiscriminantAnalysis = model.named_steps["classifier"]
    return {
        "classifier_type": type(classifier).__name__,
        "solver": str(classifier.solver),
        "shrinkage": getattr(classifier, "shrinkage", None),
        "priors": [float(value) for value in classifier.priors_],
        "classes": [int(value) for value in classifier.classes_],
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
