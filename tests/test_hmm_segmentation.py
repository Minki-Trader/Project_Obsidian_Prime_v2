from __future__ import annotations

import numpy as np
import pandas as pd

from foundation.models.hmm_segmentation import (
    HMMVariantSpec,
    fit_hmm_variant,
    state_quality_read,
    state_sequence_frame,
    state_summary_frame,
    transition_read,
)


def _toy_hmm_frame(rows: int = 120) -> pd.DataFrame:
    rng = np.random.default_rng(22)
    x1 = np.r_[rng.normal(-1.0, 0.12, rows // 3), rng.normal(0.0, 0.12, rows // 3), rng.normal(1.0, 0.12, rows // 3)]
    x2 = np.r_[rng.normal(0.8, 0.10, rows // 3), rng.normal(0.0, 0.10, rows // 3), rng.normal(0.8, 0.10, rows // 3)]
    labels = np.where(x1 < -0.4, 0, np.where(x1 > 0.4, 2, 1))
    return pd.DataFrame(
        {
            "timestamp": pd.date_range("2024-01-01", periods=rows, freq="5min", tz="UTC"),
            "symbol": "US100",
            "split": ["train"] * 72 + ["validation"] * 24 + ["oos"] * 24,
            "label": [str(value) for value in labels],
            "label_class": labels,
            "future_log_return_12": x1 / 100.0,
            "x1": x1,
            "x2": x2,
        }
    )


def test_hmm_state_sequence_and_summary_are_stable() -> None:
    frame = _toy_hmm_frame()
    spec = HMMVariantSpec(
        variant_id="unit",
        idea_id="unit",
        description="unit",
        feature_names=("x1", "x2"),
        n_components=3,
        n_iter=100,
        random_state=22,
    )

    model = fit_hmm_variant(frame, ["x1", "x2"], spec)
    sequence = state_sequence_frame(model, frame, tier_scope="Tier A", record_view="tier_a_separate")
    summary = state_summary_frame(sequence)
    quality = state_quality_read(summary, n_components=3)
    transitions = transition_read(model)

    assert len(sequence) == len(frame)
    assert sequence["hidden_state"].nunique() == 3
    assert set(summary["split"]) == {"train", "validation", "oos"}
    assert quality["by_split"]["train"]["state_count"] == 3
    assert transitions["self_transition_mean"] >= 0.0
