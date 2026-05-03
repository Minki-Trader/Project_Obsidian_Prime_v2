from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, log_loss
from xgboost import XGBClassifier

from foundation.models.baseline_training import LABEL_NAMES, LABEL_ORDER, validate_model_input_frame
from foundation.models.onnx_bridge import ordered_sklearn_probabilities


PROBABILITY_COLUMNS = ("p_short", "p_flat", "p_long")


@dataclass(frozen=True)
class XgbVariantSpec:
    variant_id: str
    idea_id: str
    description: str
    n_estimators: int
    max_depth: int
    learning_rate: float
    min_child_weight: float = 1.0
    subsample: float = 0.85
    colsample_bytree: float = 0.85
    reg_alpha: float = 0.0
    reg_lambda: float = 1.0
    gamma: float = 0.0
    booster: str = "gbtree"
    rate_drop: float | None = None
    skip_drop: float | None = None
    sample_type: str | None = None
    normalize_type: str | None = None
    one_drop: int | None = None
    random_state: int = 1901
    sample_weight_policy: str = "none"

    def payload(self) -> dict[str, Any]:
        return asdict(self)


def default_stage17_xgb_variants() -> list[XgbVariantSpec]:
    return [
        XgbVariantSpec(
            variant_id="v01_depth2_l2_subsample",
            idea_id="shallow_regularized_boosting",
            description="Shallow trees with moderate L2 regularization and subsampling.",
            n_estimators=90,
            max_depth=2,
            learning_rate=0.045,
            reg_lambda=4.0,
            random_state=1901,
        ),
        XgbVariantSpec(
            variant_id="v02_depth3_balanced_l2",
            idea_id="balanced_depth_regularized_boosting",
            description="Depth three regularized boosting with balanced class weights.",
            n_estimators=100,
            max_depth=3,
            learning_rate=0.040,
            min_child_weight=2.0,
            subsample=0.80,
            colsample_bytree=0.80,
            reg_lambda=6.0,
            random_state=1902,
            sample_weight_policy="balanced_classes",
        ),
        XgbVariantSpec(
            variant_id="v03_depth4_l1_l2_slow",
            idea_id="deeper_l1_l2_regularized_boosting",
            description="Deeper trees with slower learning and L1 plus L2 regularization.",
            n_estimators=120,
            max_depth=4,
            learning_rate=0.030,
            min_child_weight=3.0,
            subsample=0.75,
            colsample_bytree=0.75,
            reg_alpha=0.10,
            reg_lambda=8.0,
            gamma=0.02,
            random_state=1903,
        ),
        XgbVariantSpec(
            variant_id="v04_stump_sparse_l1",
            idea_id="stump_sparse_boosting",
            description="Decision stumps with sparse L1 regularization.",
            n_estimators=140,
            max_depth=1,
            learning_rate=0.050,
            min_child_weight=4.0,
            subsample=0.90,
            colsample_bytree=0.70,
            reg_alpha=0.25,
            reg_lambda=3.0,
            random_state=1904,
        ),
        XgbVariantSpec(
            variant_id="v05_conservative_childweight",
            idea_id="conservative_leaf_weight_boosting",
            description="Conservative leaf formation with heavier child weight and L2.",
            n_estimators=110,
            max_depth=3,
            learning_rate=0.035,
            min_child_weight=8.0,
            subsample=0.70,
            colsample_bytree=0.85,
            reg_lambda=10.0,
            gamma=0.05,
            random_state=1905,
        ),
    ]


def _sample_weights(labels: np.ndarray, policy: str) -> np.ndarray | None:
    if policy != "balanced_classes":
        return None
    counts = {label: max(1, int((labels == label).sum())) for label in LABEL_ORDER}
    total = float(len(labels))
    return np.asarray([total / (len(LABEL_ORDER) * counts[int(label)]) for label in labels], dtype="float64")


def build_xgb_classifier(spec: XgbVariantSpec) -> XGBClassifier:
    params: dict[str, Any] = {
        "objective": "multi:softprob",
        "num_class": len(LABEL_ORDER),
        "eval_metric": "mlogloss",
        "tree_method": "hist",
        "booster": str(spec.booster),
        "n_estimators": int(spec.n_estimators),
        "max_depth": int(spec.max_depth),
        "learning_rate": float(spec.learning_rate),
        "min_child_weight": float(spec.min_child_weight),
        "subsample": float(spec.subsample),
        "colsample_bytree": float(spec.colsample_bytree),
        "reg_alpha": float(spec.reg_alpha),
        "reg_lambda": float(spec.reg_lambda),
        "gamma": float(spec.gamma),
        "random_state": int(spec.random_state),
        "n_jobs": 2,
        "verbosity": 0,
    }
    if str(spec.booster) == "dart":
        if spec.rate_drop is not None:
            params["rate_drop"] = float(spec.rate_drop)
        if spec.skip_drop is not None:
            params["skip_drop"] = float(spec.skip_drop)
        if spec.sample_type is not None:
            params["sample_type"] = str(spec.sample_type)
        if spec.normalize_type is not None:
            params["normalize_type"] = str(spec.normalize_type)
        if spec.one_drop is not None:
            params["one_drop"] = int(spec.one_drop)
    return XGBClassifier(**params)


def fit_xgb_variant(frame: pd.DataFrame, feature_order: Sequence[str], spec: XgbVariantSpec) -> tuple[XGBClassifier, dict[str, Any]]:
    features = list(feature_order)
    validate_model_input_frame(frame, features)
    train = frame.loc[frame["split"].astype(str).eq("train")].copy()
    values = train.loc[:, features].to_numpy(dtype="float64", copy=False)
    labels = train["label_class"].astype("int64").to_numpy()
    missing = sorted(set(LABEL_ORDER).difference(set(labels)))
    if missing:
        raise RuntimeError(f"Train split is missing label classes: {missing}")
    model = build_xgb_classifier(spec)
    weights = _sample_weights(labels, spec.sample_weight_policy)
    model.fit(values, labels, sample_weight=weights)
    return model, {
        "train_rows": int(len(train)),
        "feature_count": int(len(features)),
        "class_counts": {str(k): int(v) for k, v in train["label_class"].value_counts().sort_index().items()},
        "sample_weight_policy": spec.sample_weight_policy,
    }


def probability_frame(model: XGBClassifier, frame: pd.DataFrame, feature_order: Sequence[str]) -> pd.DataFrame:
    values = frame.loc[:, list(feature_order)].to_numpy(dtype="float64", copy=False)
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


def nonflat_threshold(prob_frame: pd.DataFrame, quantile: float) -> float:
    validation = prob_frame.loc[prob_frame["split"].astype(str).eq("validation")]
    if validation.empty:
        raise RuntimeError("Validation split is empty.")
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
        }
    values = prob_frame.loc[:, list(PROBABILITY_COLUMNS)].to_numpy(dtype="float64", copy=False)
    metrics["probability_checks"] = {
        "finite": bool(np.isfinite(values).all()),
        "row_sum_max_abs_error": float(np.abs(values.sum(axis=1) - 1.0).max()) if len(values) else 0.0,
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
        }
    return payload


def feature_importance_frame(model: XGBClassifier, feature_order: Sequence[str]) -> pd.DataFrame:
    gain = model.get_booster().get_score(importance_type="gain")
    rows = []
    total_gain = float(sum(gain.values())) or 1.0
    for index, feature in enumerate(feature_order):
        key = f"f{index}"
        value = float(gain.get(key, 0.0))
        rows.append({"feature": feature, "gain": value, "gain_share": value / total_gain})
    return pd.DataFrame(rows).sort_values(["gain", "feature"], ascending=[False, True])


def characteristic_score(metrics: Mapping[str, Any], shape: Mapping[str, Any], feature_importance: pd.DataFrame) -> float:
    validation = metrics.get("validation", {})
    oos = metrics.get("oos", {})
    val_cov = float(validation.get("signal_coverage") or 0.0)
    oos_cov = float(oos.get("signal_coverage") or 0.0)
    val_margin = float(shape.get("validation", {}).get("probability_margin_mean") or 0.0)
    oos_margin = float(shape.get("oos", {}).get("probability_margin_mean") or 0.0)
    top10_share = float(feature_importance.head(10)["gain_share"].sum()) if not feature_importance.empty else 1.0
    density = 1.0 - min(abs(val_cov - 0.10) / 0.10, 1.0)
    density_stability = 1.0 - min(abs(val_cov - oos_cov) / 0.18, 1.0)
    margin_presence = min((val_margin + oos_margin) / 0.18, 1.0)
    margin_stability = 1.0 - min(abs(val_margin - oos_margin) / 0.09, 1.0)
    importance_spread = 1.0 - min(max(top10_share - 0.35, 0.0) / 0.55, 1.0)
    return float(0.25 * density + 0.25 * density_stability + 0.20 * margin_presence + 0.15 * margin_stability + 0.15 * importance_spread)
