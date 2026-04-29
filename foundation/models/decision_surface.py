from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd

from foundation.models.baseline_training import LABEL_NAMES


PROBABILITY_COLUMNS = ["p_short", "p_flat", "p_long"]
DECISION_CLASS_NO_TRADE = -1
DECISION_LABEL_NO_TRADE = "no_trade"


@dataclass(frozen=True)
class ThresholdRule:
    threshold_id: str = "short045_long045_margin005"
    short_threshold: float = 0.45
    long_threshold: float = 0.45
    min_margin: float = 0.05


def _threshold_id(short_threshold: float, long_threshold: float, min_margin: float) -> str:
    return f"short{short_threshold:.3f}_long{long_threshold:.3f}_margin{min_margin:.3f}"


def threshold_rule_payload(rule: ThresholdRule) -> dict[str, Any]:
    return {
        "threshold_id": rule.threshold_id,
        "short_threshold": rule.short_threshold,
        "long_threshold": rule.long_threshold,
        "min_margin": rule.min_margin,
    }


def threshold_rule_from_values(
    *,
    short_threshold: float,
    long_threshold: float,
    min_margin: float,
    threshold_id: str | None = None,
) -> ThresholdRule:
    return ThresholdRule(
        threshold_id=threshold_id or _threshold_id(short_threshold, long_threshold, min_margin),
        short_threshold=float(short_threshold),
        long_threshold=float(long_threshold),
        min_margin=float(min_margin),
    )


def validate_threshold_rule(rule: ThresholdRule) -> None:
    values = {
        "short_threshold": rule.short_threshold,
        "long_threshold": rule.long_threshold,
        "min_margin": rule.min_margin,
    }
    for name, value in values.items():
        if not np.isfinite(value):
            raise ValueError(f"{name} must be finite.")
    if not 0.0 <= rule.short_threshold <= 1.0:
        raise ValueError("short_threshold must be in [0, 1].")
    if not 0.0 <= rule.long_threshold <= 1.0:
        raise ValueError("long_threshold must be in [0, 1].")
    if rule.min_margin < 0.0:
        raise ValueError("min_margin must be non-negative.")


def probability_matrix(probabilities: pd.DataFrame | np.ndarray) -> np.ndarray:
    if isinstance(probabilities, pd.DataFrame):
        missing = [name for name in PROBABILITY_COLUMNS if name not in probabilities.columns]
        if missing:
            raise ValueError(f"Probability frame is missing columns: {missing}")
        matrix = probabilities.loc[:, PROBABILITY_COLUMNS].to_numpy(dtype="float64", copy=False)
    else:
        matrix = np.asarray(probabilities, dtype="float64")
    if matrix.ndim != 2 or matrix.shape[1] != len(PROBABILITY_COLUMNS):
        raise ValueError(f"Expected probability matrix shape [n, 3], got {matrix.shape}.")
    if not np.isfinite(matrix).all():
        raise ValueError("Probability matrix contains NaN or infinite values.")
    return matrix


def apply_threshold_rule(probabilities: pd.DataFrame | np.ndarray, rule: ThresholdRule) -> pd.DataFrame:
    validate_threshold_rule(rule)
    matrix = probability_matrix(probabilities)
    rows: list[dict[str, Any]] = []
    for p_short, p_flat, p_long in matrix:
        short_margin = float(p_short - max(p_flat, p_long))
        long_margin = float(p_long - max(p_flat, p_short))
        short_pass = bool(p_short >= rule.short_threshold and short_margin >= rule.min_margin)
        long_pass = bool(p_long >= rule.long_threshold and long_margin >= rule.min_margin)

        if short_pass and not long_pass:
            decision_class = 0
            decision_label = LABEL_NAMES[0]
            decision_probability = float(p_short)
            decision_margin = short_margin
        elif long_pass and not short_pass:
            decision_class = 2
            decision_label = LABEL_NAMES[2]
            decision_probability = float(p_long)
            decision_margin = long_margin
        elif short_pass and long_pass and p_short != p_long:
            decision_class = 0 if p_short > p_long else 2
            decision_label = LABEL_NAMES[decision_class]
            decision_probability = float(max(p_short, p_long))
            decision_margin = float(abs(p_short - p_long))
        else:
            decision_class = DECISION_CLASS_NO_TRADE
            decision_label = DECISION_LABEL_NO_TRADE
            decision_probability = float(max(p_short, p_flat, p_long))
            decision_margin = float(max(short_margin, long_margin))

        rows.append(
            {
                "threshold_id": rule.threshold_id,
                "p_short": float(p_short),
                "p_flat": float(p_flat),
                "p_long": float(p_long),
                "decision_label_class": decision_class,
                "decision_label": decision_label,
                "decision_probability": decision_probability,
                "decision_margin": decision_margin,
                "short_margin": short_margin,
                "long_margin": long_margin,
            }
        )
    return pd.DataFrame(rows)
