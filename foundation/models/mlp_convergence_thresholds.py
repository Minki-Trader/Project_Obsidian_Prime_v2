from __future__ import annotations

from typing import Any, Iterable, Mapping, Sequence

import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline

from foundation.models.mlp_characteristics import PROBABILITY_COLUMNS


SPLITS = ("train", "validation", "oos")


def training_history_table(
    model: Pipeline,
    *,
    scope: str,
    warning_messages: Sequence[str] = (),
) -> pd.DataFrame:
    classifier = model.named_steps["classifier"]
    losses = list(float(value) for value in getattr(classifier, "loss_curve_", ()))
    validation_scores = list(float(value) for value in getattr(classifier, "validation_scores_", ()))
    row_count = max(len(losses), len(validation_scores), int(getattr(classifier, "n_iter_", 0)))
    rows: list[dict[str, Any]] = []
    for index in range(row_count):
        rows.append(
            {
                "scope": scope,
                "iteration": index + 1,
                "loss": losses[index] if index < len(losses) else np.nan,
                "validation_score": validation_scores[index] if index < len(validation_scores) else np.nan,
                "warning_count": len(warning_messages),
            }
        )
    return pd.DataFrame(rows)


def training_history_summary(
    model: Pipeline,
    *,
    scope: str,
    warning_messages: Sequence[str] = (),
) -> dict[str, Any]:
    classifier = model.named_steps["classifier"]
    losses = np.asarray(getattr(classifier, "loss_curve_", ()), dtype="float64")
    validation_scores = np.asarray(getattr(classifier, "validation_scores_", ()), dtype="float64")
    n_iter = int(getattr(classifier, "n_iter_", len(losses)))
    max_iter = int(getattr(classifier, "max_iter", n_iter))
    tail = losses[-10:] if len(losses) >= 10 else losses
    tail_slope = float(np.polyfit(np.arange(len(tail)), tail, 1)[0]) if len(tail) >= 2 else np.nan
    hit_max_iter = bool(n_iter >= max_iter)
    stopped_before_max_iter = bool(n_iter < max_iter)
    warning_count = len(warning_messages)
    if warning_count:
        convergence_label = "warning_observed"
    elif hit_max_iter:
        convergence_label = "max_iter_reached"
    elif stopped_before_max_iter and len(validation_scores):
        convergence_label = "early_stopping_triggered"
    elif stopped_before_max_iter:
        convergence_label = "stopped_before_max_iter"
    else:
        convergence_label = "inconclusive_stop_shape"
    return {
        "scope": scope,
        "n_iter": n_iter,
        "max_iter": max_iter,
        "stopped_before_max_iter": stopped_before_max_iter,
        "hit_max_iter": hit_max_iter,
        "loss_first": _finite_or_none(losses[0] if len(losses) else np.nan),
        "loss_last": _finite_or_none(losses[-1] if len(losses) else np.nan),
        "loss_min": _finite_or_none(np.nanmin(losses) if len(losses) else np.nan),
        "loss_drop_abs": _finite_or_none(losses[0] - losses[-1] if len(losses) else np.nan),
        "loss_drop_ratio": _finite_or_none((losses[0] - losses[-1]) / abs(losses[0]) if len(losses) and losses[0] else np.nan),
        "loss_tail_delta": _finite_or_none(tail[0] - tail[-1] if len(tail) >= 2 else np.nan),
        "loss_tail_slope": _finite_or_none(tail_slope),
        "validation_score_first": _finite_or_none(validation_scores[0] if len(validation_scores) else np.nan),
        "validation_score_last": _finite_or_none(validation_scores[-1] if len(validation_scores) else np.nan),
        "validation_score_best": _finite_or_none(np.nanmax(validation_scores) if len(validation_scores) else np.nan),
        "validation_best_gap_last": _finite_or_none(
            np.nanmax(validation_scores) - validation_scores[-1] if len(validation_scores) else np.nan
        ),
        "best_validation_score_attr": _finite_or_none(float(getattr(classifier, "best_validation_score_", np.nan))),
        "early_stopping": bool(getattr(classifier, "early_stopping", False)),
        "tol": float(getattr(classifier, "tol", np.nan)),
        "n_iter_no_change": int(getattr(classifier, "n_iter_no_change", 0)),
        "warning_count": warning_count,
        "warning_messages": list(warning_messages),
        "convergence_label": convergence_label,
    }


def threshold_feasibility_table(
    prob_frame: pd.DataFrame,
    *,
    scope: str,
    quantiles: Sequence[float],
    margins: Sequence[float],
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for quantile, margin in _threshold_grid(prob_frame, quantiles, margins):
        threshold = nonflat_confidence_quantile(prob_frame, quantile)
        threshold_key = threshold_id(quantile, margin)
        for split_name in SPLITS:
            split = prob_frame.loc[prob_frame["split"].astype(str).eq(split_name)]
            metrics = decision_metrics(split, threshold=threshold, min_margin=margin)
            rows.append(
                {
                    "scope": scope,
                    "threshold_id": threshold_key,
                    "threshold_quantile": float(quantile),
                    "threshold_value": threshold,
                    "tier_a_threshold_value": np.nan,
                    "tier_b_threshold_value": np.nan,
                    "min_margin": float(margin),
                    "split": split_name,
                    **metrics,
                }
            )
    return pd.DataFrame(rows)


def routed_threshold_feasibility_table(
    *,
    tier_a_prob_frame: pd.DataFrame,
    tier_b_fallback_prob_frame: pd.DataFrame,
    scope: str,
    quantiles: Sequence[float],
    margins: Sequence[float],
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for quantile, margin in _threshold_grid(tier_a_prob_frame, quantiles, margins):
        threshold_key = threshold_id(quantile, margin)
        tier_a_threshold = nonflat_confidence_quantile(tier_a_prob_frame, quantile)
        tier_b_threshold = nonflat_confidence_quantile(tier_b_fallback_prob_frame, quantile)
        for split_name in SPLITS:
            tier_a_split = tier_a_prob_frame.loc[tier_a_prob_frame["split"].astype(str).eq(split_name)]
            tier_b_split = tier_b_fallback_prob_frame.loc[tier_b_fallback_prob_frame["split"].astype(str).eq(split_name)]
            metrics = combine_decision_metrics(
                decision_metrics(tier_a_split, threshold=tier_a_threshold, min_margin=margin),
                decision_metrics(tier_b_split, threshold=tier_b_threshold, min_margin=margin),
            )
            rows.append(
                {
                    "scope": scope,
                    "threshold_id": threshold_key,
                    "threshold_quantile": float(quantile),
                    "threshold_value": np.nan,
                    "tier_a_threshold_value": tier_a_threshold,
                    "tier_b_threshold_value": tier_b_threshold,
                    "min_margin": float(margin),
                    "split": split_name,
                    **metrics,
                }
            )
    return pd.DataFrame(rows)


def threshold_summary(detail: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for (scope, threshold_key), group in detail.groupby(["scope", "threshold_id"], sort=True):
        by_split = {str(row["split"]): row for row in group.to_dict(orient="records")}
        validation = by_split.get("validation", {})
        oos = by_split.get("oos", {})
        rows.append(
            {
                "scope": scope,
                "threshold_id": threshold_key,
                "threshold_quantile": validation.get("threshold_quantile"),
                "min_margin": validation.get("min_margin"),
                "validation_signal_count": validation.get("signal_count"),
                "validation_signal_coverage": validation.get("signal_coverage"),
                "validation_directional_hit_rate": validation.get("directional_hit_rate"),
                "oos_signal_count": oos.get("signal_count"),
                "oos_signal_coverage": oos.get("signal_coverage"),
                "oos_directional_hit_rate": oos.get("directional_hit_rate"),
                "density_label": density_label(
                    validation.get("signal_coverage"),
                    oos.get("signal_coverage"),
                ),
            }
        )
    return pd.DataFrame(rows)


def representative_threshold_rows(summary: pd.DataFrame, threshold_key: str = "q90_m000") -> pd.DataFrame:
    exact = summary.loc[summary["threshold_id"].astype(str).eq(threshold_key)]
    if not exact.empty:
        return exact.copy()
    return summary.sort_values(["scope", "threshold_quantile", "min_margin"]).groupby("scope", as_index=False).head(1)


def nonflat_confidence_quantile(prob_frame: pd.DataFrame, quantile: float) -> float:
    validation = prob_frame.loc[prob_frame["split"].astype(str).eq("validation")]
    if validation.empty:
        raise RuntimeError("Validation split is empty; cannot derive threshold feasibility grid.")
    confidence = validation.loc[:, ["p_short", "p_long"]].max(axis=1).to_numpy(dtype="float64", copy=False)
    return float(np.quantile(confidence, float(quantile)))


def decision_metrics(prob_frame: pd.DataFrame, *, threshold: float, min_margin: float) -> dict[str, Any]:
    if prob_frame.empty:
        return _empty_metrics()
    probabilities = prob_frame.loc[:, list(PROBABILITY_COLUMNS)].to_numpy(dtype="float64", copy=False)
    p_short = probabilities[:, 0]
    p_long = probabilities[:, 2]
    confidence = np.maximum(p_short, p_long)
    margin = np.abs(p_short - p_long)
    decision = np.full(len(prob_frame), 1, dtype="int64")
    short_ok = (p_short >= p_long) & (p_short >= threshold) & (margin >= min_margin)
    long_ok = (p_long > p_short) & (p_long >= threshold) & (margin >= min_margin)
    decision[short_ok] = 0
    decision[long_ok] = 2
    labels = prob_frame["label_class"].astype("int64").to_numpy()
    signals = decision != 1
    correct = (decision[signals] == labels[signals]) if signals.any() else np.asarray([], dtype=bool)
    clipped = np.clip(probabilities, 1e-12, 1.0)
    entropy = -(clipped * np.log(clipped)).sum(axis=1)
    return {
        "rows": int(len(prob_frame)),
        "signal_count": int(signals.sum()),
        "signal_coverage": float(signals.mean()),
        "short_count": int((decision == 0).sum()),
        "long_count": int((decision == 2).sum()),
        "directional_correct_count": int(correct.sum()) if len(correct) else 0,
        "directional_hit_rate": float(correct.mean()) if len(correct) else np.nan,
        "mean_signal_confidence": float(confidence[signals].mean()) if signals.any() else np.nan,
        "mean_signal_margin": float(margin[signals].mean()) if signals.any() else np.nan,
        "mean_entropy": float(entropy.mean()),
        "probability_row_sum_max_abs_error": float(np.abs(probabilities.sum(axis=1) - 1.0).max()),
    }


def combine_decision_metrics(*metrics: Mapping[str, Any]) -> dict[str, Any]:
    rows = int(sum(int(item.get("rows", 0) or 0) for item in metrics))
    signal_count = int(sum(int(item.get("signal_count", 0) or 0) for item in metrics))
    short_count = int(sum(int(item.get("short_count", 0) or 0) for item in metrics))
    long_count = int(sum(int(item.get("long_count", 0) or 0) for item in metrics))
    correct = int(sum(int(item.get("directional_correct_count", 0) or 0) for item in metrics))
    return {
        "rows": rows,
        "signal_count": signal_count,
        "signal_coverage": float(signal_count / rows) if rows else np.nan,
        "short_count": short_count,
        "long_count": long_count,
        "directional_correct_count": correct,
        "directional_hit_rate": float(correct / signal_count) if signal_count else np.nan,
        "mean_signal_confidence": _weighted_mean(metrics, "mean_signal_confidence", "signal_count"),
        "mean_signal_margin": _weighted_mean(metrics, "mean_signal_margin", "signal_count"),
        "mean_entropy": _weighted_mean(metrics, "mean_entropy", "rows"),
        "probability_row_sum_max_abs_error": max(
            float(item.get("probability_row_sum_max_abs_error") or 0.0) for item in metrics
        ),
    }


def density_label(validation_coverage: Any, oos_coverage: Any) -> str:
    validation = _as_float(validation_coverage)
    oos = _as_float(oos_coverage)
    if validation is None or oos is None:
        return "inconclusive_density"
    if min(validation, oos) < 0.005:
        return "dry_density"
    if validation > 0.35:
        return "flooded_density"
    if 0.02 <= validation <= 0.20 and oos >= 0.01:
        return "usable_density_band"
    return "watch_density_band"


def threshold_id(quantile: float, margin: float) -> str:
    return f"q{int(round(float(quantile) * 100)):02d}_m{int(round(float(margin) * 1000)):03d}"


def _threshold_grid(prob_frame: pd.DataFrame, quantiles: Sequence[float], margins: Sequence[float]) -> Iterable[tuple[float, float]]:
    _ = prob_frame
    for quantile in quantiles:
        for margin in margins:
            yield float(quantile), float(margin)


def _weighted_mean(metrics: Sequence[Mapping[str, Any]], value_key: str, weight_key: str) -> float:
    numerator = 0.0
    denominator = 0.0
    for item in metrics:
        value = _as_float(item.get(value_key))
        weight = _as_float(item.get(weight_key))
        if value is None or weight is None or weight <= 0:
            continue
        numerator += value * weight
        denominator += weight
    return float(numerator / denominator) if denominator else np.nan


def _finite_or_none(value: Any) -> float | None:
    numeric = _as_float(value)
    return numeric if numeric is not None else None


def _as_float(value: Any) -> float | None:
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return None
    if not np.isfinite(numeric):
        return None
    return numeric


def _empty_metrics() -> dict[str, Any]:
    return {
        "rows": 0,
        "signal_count": 0,
        "signal_coverage": np.nan,
        "short_count": 0,
        "long_count": 0,
        "directional_correct_count": 0,
        "directional_hit_rate": np.nan,
        "mean_signal_confidence": np.nan,
        "mean_signal_margin": np.nan,
        "mean_entropy": np.nan,
        "probability_row_sum_max_abs_error": 0.0,
    }
