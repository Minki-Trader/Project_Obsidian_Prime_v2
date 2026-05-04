from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

from foundation.models.baseline_training import LABEL_ORDER, validate_model_input_frame


@dataclass(frozen=True)
class HMMVariantSpec:
    variant_id: str
    idea_id: str
    description: str
    feature_names: tuple[str, ...]
    n_components: int
    covariance_type: str = "diag"
    n_iter: int = 250
    tol: float = 1.0e-3
    random_state: int = 220
    min_covar: float = 1.0e-3


@dataclass
class HMMStateModel:
    spec: HMMVariantSpec
    scaler: StandardScaler
    model: Any


def fit_hmm_variant(frame: pd.DataFrame, feature_order: Sequence[str], spec: HMMVariantSpec) -> HMMStateModel:
    from hmmlearn.hmm import GaussianHMM

    validate_model_input_frame(frame, list(feature_order))
    missing = sorted(set(spec.feature_names).difference(frame.columns))
    if missing:
        raise RuntimeError(f"HMM variant {spec.variant_id} is missing features: {missing}")
    train = frame.loc[frame["split"].astype(str).eq("train")].sort_values("timestamp")
    values = train.loc[:, list(spec.feature_names)].to_numpy(dtype="float64", copy=False)
    if len(values) < max(50, spec.n_components * 20):
        raise RuntimeError(f"HMM variant {spec.variant_id} has too few train rows: {len(values)}")
    scaler = StandardScaler().fit(values)
    scaled = scaler.transform(values)
    model = GaussianHMM(
        n_components=spec.n_components,
        covariance_type=spec.covariance_type,
        n_iter=spec.n_iter,
        tol=spec.tol,
        random_state=spec.random_state,
        min_covar=spec.min_covar,
    ).fit(scaled, lengths=[len(scaled)])
    return HMMStateModel(spec=spec, scaler=scaler, model=model)


def predict_hidden_states(state_model: HMMStateModel, frame: pd.DataFrame) -> np.ndarray:
    source = frame.sort_values("timestamp")
    values = source.loc[:, list(state_model.spec.feature_names)].to_numpy(dtype="float64", copy=False)
    scaled = state_model.scaler.transform(values)
    return np.asarray(state_model.model.predict(scaled), dtype="int64")


def state_sequence_frame(
    state_model: HMMStateModel,
    frame: pd.DataFrame,
    *,
    tier_scope: str,
    record_view: str,
) -> pd.DataFrame:
    source = frame.sort_values("timestamp").copy()
    states = predict_hidden_states(state_model, source)
    out = source.loc[:, ["timestamp", "symbol", "split", "label_class", "future_log_return_12"]].copy()
    out["tier_scope"] = tier_scope
    out["record_view"] = record_view
    out["hidden_state"] = states
    out["hidden_state_label"] = [f"s{int(value)}" for value in states]
    return out


def state_summary_frame(sequence: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for (split, state), group in sequence.groupby(["split", "hidden_state"], dropna=False):
        labels = group["label_class"].astype("int64")
        counts = labels.value_counts().to_dict()
        rows.append(
            {
                "split": str(split),
                "hidden_state": int(state),
                "rows": int(len(group)),
                "share": float(len(group) / max(1, int((sequence["split"].astype(str) == str(split)).sum()))),
                "future_return_mean": float(group["future_log_return_12"].mean()),
                "future_return_std": float(group["future_log_return_12"].std(ddof=0)),
                "future_return_q05": float(group["future_log_return_12"].quantile(0.05)),
                "future_return_q95": float(group["future_log_return_12"].quantile(0.95)),
                "short_count": int(counts.get(0, 0)),
                "flat_count": int(counts.get(1, 0)),
                "long_count": int(counts.get(2, 0)),
                "dominant_label": int(labels.mode().iloc[0]) if len(labels) else None,
            }
        )
    return pd.DataFrame(rows).sort_values(["split", "hidden_state"]).reset_index(drop=True)


def state_quality_read(summary: pd.DataFrame, *, n_components: int) -> dict[str, Any]:
    by_split: dict[str, Any] = {}
    for split in ("train", "validation", "oos"):
        part = summary.loc[summary["split"].astype(str).eq(split)]
        if part.empty:
            by_split[split] = {"state_count": 0, "min_share": 0.0, "risk_separation": 0.0}
            continue
        means = part["future_return_mean"].astype("float64")
        by_split[split] = {
            "state_count": int(part["hidden_state"].nunique()),
            "min_share": float(part["share"].min()),
            "max_share": float(part["share"].max()),
            "risk_separation": float(means.max() - means.min()),
            "worst_state": int(part.sort_values("future_return_mean").iloc[0]["hidden_state"]),
            "best_state": int(part.sort_values("future_return_mean").iloc[-1]["hidden_state"]),
        }
    validation = summary.loc[summary["split"].astype(str).eq("validation"), ["hidden_state", "future_return_mean"]]
    oos = summary.loc[summary["split"].astype(str).eq("oos"), ["hidden_state", "future_return_mean"]]
    merged = validation.merge(oos, on="hidden_state", suffixes=("_validation", "_oos"))
    gap = (
        float(np.abs(merged["future_return_mean_validation"] - merged["future_return_mean_oos"]).mean())
        if not merged.empty
        else None
    )
    collapse = any(by_split[split]["state_count"] < n_components or by_split[split]["min_share"] < 0.03 for split in by_split)
    score = (
        by_split["validation"]["risk_separation"]
        + by_split["oos"]["risk_separation"]
        - (gap or 0.0)
        - (0.01 if collapse else 0.0)
    )
    return {
        "by_split": by_split,
        "validation_oos_mean_gap": gap,
        "collapsed": bool(collapse),
        "quality_score": float(score),
    }


def transition_read(state_model: HMMStateModel) -> dict[str, Any]:
    matrix = np.asarray(state_model.model.transmat_, dtype="float64")
    return {
        "self_transition_mean": float(np.diag(matrix).mean()),
        "self_transition_min": float(np.diag(matrix).min()),
        "self_transition_max": float(np.diag(matrix).max()),
        "matrix": matrix.tolist(),
    }


def default_stage22_hmm_variants(feature_names: Sequence[str]) -> list[HMMVariantSpec]:
    features = tuple(feature_names)
    compact = tuple(name for name in features if name not in {"vix_change_1", "us10yr_change_1", "usdx_change_1"})
    return [
        HMMVariantSpec(
            variant_id="v01_core17_3state_diag",
            idea_id="hmm_state_count_3",
            description="3-state HMM over volatility/session/trend core features.",
            feature_names=features,
            n_components=3,
            random_state=220,
        ),
        HMMVariantSpec(
            variant_id="v02_core17_4state_diag",
            idea_id="hmm_state_count_4",
            description="4-state HMM over volatility/session/trend core features.",
            feature_names=features,
            n_components=4,
            random_state=221,
        ),
        HMMVariantSpec(
            variant_id="v03_core17_5state_diag",
            idea_id="hmm_state_count_5",
            description="5-state HMM over volatility/session/trend core features.",
            feature_names=features,
            n_components=5,
            random_state=222,
        ),
        HMMVariantSpec(
            variant_id="v04_compact14_4state_diag",
            idea_id="hmm_compact_macro_removed",
            description="4-state HMM with compact local volatility/trend/session features.",
            feature_names=compact,
            n_components=4,
            random_state=223,
        ),
    ]
