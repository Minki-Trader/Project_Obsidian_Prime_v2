from __future__ import annotations

from dataclasses import asdict, dataclass
from functools import reduce
from operator import add
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd
from pygam import LogisticGAM, s

from foundation.models.baseline_training import LABEL_NAMES, LABEL_ORDER, validate_model_input_frame
from foundation.models.xgboost_boosting import (
    PROBABILITY_COLUMNS,
    nonflat_threshold,
    probability_shape_metrics,
    split_decision_metrics,
)


@dataclass(frozen=True)
class GamVariantSpec:
    variant_id: str
    idea_id: str
    description: str
    feature_names: tuple[str, ...]
    n_splines: int
    lam: float
    max_iter: int = 80
    max_train_rows_per_class: int = 2500
    random_state: int = 2001
    tier_b_compatible: bool = True

    def payload(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["feature_names"] = list(self.feature_names)
        return payload


def default_stage20_gam_variants() -> list[GamVariantSpec]:
    core12 = (
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
    )
    core24 = (
        *core12,
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
    proxy_context20 = (
        "log_return_1",
        "return_zscore_20",
        "rsi_14",
        "bb_position_20",
        "adx_14",
        "di_spread_14",
        "minutes_from_cash_open",
        "vix_change_1",
        "vix_zscore_20",
        "us10yr_change_1",
        "us10yr_zscore_20",
        "usdx_change_1",
        "usdx_zscore_20",
        "nvda_xnas_log_return_1",
        "aapl_xnas_log_return_1",
        "msft_xnas_log_return_1",
        "amzn_xnas_log_return_1",
        "top3_weighted_return_1",
        "mega8_dispersion_5",
        "us100_minus_top3_weighted_return_1",
    )
    return [
        GamVariantSpec(
            variant_id="v01_core12_fast_smooth",
            idea_id="gam_core12_fast_smooth_shape",
            description="Twelve core technical/session features with fast low-spline smooth terms.",
            feature_names=core12,
            n_splines=6,
            lam=2.0,
            max_iter=70,
            max_train_rows_per_class=2200,
            random_state=2001,
            tier_b_compatible=True,
        ),
        GamVariantSpec(
            variant_id="v02_core24_smoother",
            idea_id="gam_core24_smoother_additive_shape",
            description="Broader Tier-B-compatible technical feature set with slightly smoother terms.",
            feature_names=core24,
            n_splines=6,
            lam=4.0,
            max_iter=80,
            max_train_rows_per_class=2000,
            random_state=2002,
            tier_b_compatible=True,
        ),
        GamVariantSpec(
            variant_id="v03_proxy_context20_tier_a",
            idea_id="gam_proxy_context20_macro_mega_shape",
            description="Tier-A-only macro and mega-cap proxy context to test whether smooth additive context dominates.",
            feature_names=proxy_context20,
            n_splines=6,
            lam=5.0,
            max_iter=80,
            max_train_rows_per_class=1800,
            random_state=2003,
            tier_b_compatible=False,
        ),
    ]


def _gam_terms(feature_count: int, n_splines: int, lam: float) -> Any:
    terms = [s(index, n_splines=int(n_splines), lam=float(lam)) for index in range(int(feature_count))]
    return reduce(add, terms)


def balanced_training_sample(
    frame: pd.DataFrame,
    *,
    max_rows_per_class: int,
    random_state: int,
) -> pd.DataFrame:
    train = frame.loc[frame["split"].astype(str).eq("train")].copy()
    parts: list[pd.DataFrame] = []
    for label in LABEL_ORDER:
        group = train.loc[train["label_class"].astype("int64").eq(int(label))]
        if group.empty:
            raise RuntimeError(f"Train split is missing label class: {label}")
        take = min(int(max_rows_per_class), len(group))
        parts.append(group.sample(n=take, random_state=int(random_state) + int(label)).sort_index())
    return pd.concat(parts, axis=0).sort_index()


def build_gam_classifier(spec: GamVariantSpec) -> LogisticGAM:
    return LogisticGAM(
        terms=_gam_terms(len(spec.feature_names), spec.n_splines, spec.lam),
        fit_intercept=True,
        max_iter=int(spec.max_iter),
        tol=1.0e-4,
        verbose=False,
    )


def fit_gam_variant(
    frame: pd.DataFrame,
    feature_order: Sequence[str],
    spec: GamVariantSpec,
) -> tuple[dict[str, LogisticGAM], dict[str, Any]]:
    features = list(spec.feature_names)
    missing = sorted(set(features).difference(set(feature_order)))
    if missing:
        raise ValueError(f"Feature set does not contain GAM features: {missing}")
    validate_model_input_frame(frame, list(feature_order))
    sample = balanced_training_sample(
        frame,
        max_rows_per_class=spec.max_train_rows_per_class,
        random_state=spec.random_state,
    )
    values = sample.loc[:, features].to_numpy(dtype="float64", copy=False)
    labels = sample["label_class"].astype("int64").to_numpy()
    short_model = build_gam_classifier(spec)
    long_model = build_gam_classifier(spec)
    short_model.fit(values, (labels == 0).astype("int64"))
    long_model.fit(values, (labels == 2).astype("int64"))
    return {"short": short_model, "long": long_model}, {
        "train_rows": int(len(sample)),
        "feature_count": int(len(features)),
        "class_counts": {str(k): int(v) for k, v in sample["label_class"].value_counts().sort_index().items()},
        "fusion_policy": "one_vs_rest_short_long_flat_reference_softmax",
    }


def _logit(probability: np.ndarray) -> np.ndarray:
    clipped = np.clip(np.asarray(probability, dtype="float64"), 1.0e-8, 1.0 - 1.0e-8)
    return np.log(clipped / (1.0 - clipped))


def probability_frame(
    models: Mapping[str, LogisticGAM],
    frame: pd.DataFrame,
    feature_names: Sequence[str],
) -> pd.DataFrame:
    features = list(feature_names)
    values = frame.loc[:, features].to_numpy(dtype="float64", copy=False)
    short_mu = np.asarray(models["short"].predict_mu(values), dtype="float64")
    long_mu = np.asarray(models["long"].predict_mu(values), dtype="float64")
    logits = np.stack([_logit(short_mu), np.zeros(len(values), dtype="float64"), _logit(long_mu)], axis=1)
    logits -= logits.max(axis=1, keepdims=True)
    exp_logits = np.exp(logits)
    probabilities = exp_logits / exp_logits.sum(axis=1, keepdims=True)
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


def smooth_shape_frame(models: Mapping[str, LogisticGAM], spec: GamVariantSpec, *, grid_points: int = 40) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for side, model in models.items():
        for index, feature in enumerate(spec.feature_names):
            grid = model.generate_X_grid(term=index, n=int(grid_points))
            partial = np.asarray(model.partial_dependence(term=index, X=grid), dtype="float64")
            rows.append(
                {
                    "side": side,
                    "feature": feature,
                    "term_index": int(index),
                    "x_min": float(np.nanmin(grid[:, index])) if len(grid) else None,
                    "x_max": float(np.nanmax(grid[:, index])) if len(grid) else None,
                    "partial_min": float(np.nanmin(partial)) if len(partial) else None,
                    "partial_max": float(np.nanmax(partial)) if len(partial) else None,
                    "partial_range": float(np.nanmax(partial) - np.nanmin(partial)) if len(partial) else 0.0,
                    "partial_std": float(np.nanstd(partial)) if len(partial) else 0.0,
                }
            )
    return pd.DataFrame(rows)


def shape_read(shape: pd.DataFrame) -> dict[str, Any]:
    if shape.empty:
        return {"term_count": 0, "top_terms": [], "top5_range_share": None}
    grouped = (
        shape.groupby("feature", as_index=False)
        .agg(partial_range=("partial_range", "max"), partial_std=("partial_std", "max"))
        .sort_values(["partial_range", "feature"], ascending=[False, True])
    )
    total = float(grouped["partial_range"].abs().sum()) or 1.0
    grouped["range_share"] = grouped["partial_range"].abs() / total
    return {
        "term_count": int(len(grouped)),
        "top5_range_share": float(grouped.head(5)["range_share"].sum()),
        "top_terms": grouped.head(10).to_dict(orient="records"),
    }


def characteristic_score(metrics: Mapping[str, Any], shape: Mapping[str, Any]) -> float:
    validation = metrics.get("validation", {}) if isinstance(metrics.get("validation"), Mapping) else {}
    oos = metrics.get("oos", {}) if isinstance(metrics.get("oos"), Mapping) else {}
    val_coverage = float(validation.get("signal_coverage") or 0.0)
    oos_coverage = float(oos.get("signal_coverage") or 0.0)
    val_hit = float(validation.get("directional_hit_rate") or 0.0)
    oos_hit = float(oos.get("directional_hit_rate") or 0.0)
    margin = float(oos.get("mean_probability_margin") or 0.0)
    top_shape = float(shape.get("top5_range_share") or 0.0)
    density_balance = 1.0 - min(1.0, abs(val_coverage - oos_coverage))
    return float(
        0.22 * val_coverage
        + 0.22 * oos_coverage
        + 0.18 * val_hit
        + 0.18 * oos_hit
        + 0.10 * margin
        + 0.06 * top_shape
        + 0.04 * density_balance
    )


def probability_quality_read(prob_frame: pd.DataFrame) -> dict[str, Any]:
    values = prob_frame.loc[:, list(PROBABILITY_COLUMNS)].to_numpy(dtype="float64", copy=False)
    predicted = np.asarray(LABEL_ORDER, dtype="int64")[values.argmax(axis=1)]
    by_split: dict[str, Any] = {}
    for split_name in ("train", "validation", "oos"):
        split = prob_frame.loc[prob_frame["split"].astype(str).eq(split_name)]
        split_values = split.loc[:, list(PROBABILITY_COLUMNS)].to_numpy(dtype="float64", copy=False)
        labels = split["label_class"].astype("int64").to_numpy()
        split_pred = predicted[split.index.to_numpy()] if len(split) else np.asarray([], dtype="int64")
        by_split[split_name] = {
            "rows": int(len(split)),
            "prediction_mix": {
                LABEL_NAMES[int(label)]: int((split_pred == int(label)).sum()) for label in LABEL_ORDER
            }
            if len(split)
            else {},
            "mean_max_probability": float(split_values.max(axis=1).mean()) if len(split) else None,
            "mean_flat_probability": float(split_values[:, 1].mean()) if len(split) else None,
            "row_sum_max_abs_error": float(np.abs(split_values.sum(axis=1) - 1.0).max()) if len(split) else 0.0,
            "label_mix": {LABEL_NAMES[int(label)]: int((labels == int(label)).sum()) for label in LABEL_ORDER}
            if len(split)
            else {},
        }
    return by_split
