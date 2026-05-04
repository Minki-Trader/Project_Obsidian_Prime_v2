from __future__ import annotations

import numpy as np
import pandas as pd

from foundation.models.gam_additive import (
    GamVariantSpec,
    fit_gam_variant,
    probability_frame,
    shape_read,
    smooth_shape_frame,
)


def _toy_frame() -> pd.DataFrame:
    rng = np.random.default_rng(20)
    rows = 180
    x0 = rng.normal(size=rows)
    x1 = rng.normal(size=rows)
    labels = np.where(x0 > 0.7, 2, np.where(x0 < -0.7, 0, 1))
    return pd.DataFrame(
        {
            "timestamp": pd.date_range("2024-01-01", periods=rows, freq="5min", tz="UTC"),
            "symbol": ["US100"] * rows,
            "split": ["train"] * 120 + ["validation"] * 30 + ["oos"] * 30,
            "label": labels.astype("int64"),
            "label_class": labels.astype("int64"),
            "f0": x0,
            "f1": x1,
        }
    )


def test_gam_one_vs_rest_probability_frame_has_project_columns() -> None:
    frame = _toy_frame()
    spec = GamVariantSpec(
        variant_id="toy",
        idea_id="toy",
        description="toy",
        feature_names=("f0", "f1"),
        n_splines=5,
        lam=1.0,
        max_iter=20,
        max_train_rows_per_class=25,
    )

    models, sample = fit_gam_variant(frame, ["f0", "f1"], spec)
    probabilities = probability_frame(models, frame, spec.feature_names)

    assert sample["feature_count"] == 2
    assert list(probabilities.columns) == [
        "timestamp",
        "split",
        "label_class",
        "p_short",
        "p_flat",
        "p_long",
        "probability_margin",
    ]
    np.testing.assert_allclose(probabilities[["p_short", "p_flat", "p_long"]].sum(axis=1), 1.0, atol=1e-10)


def test_gam_smooth_shape_read_records_terms() -> None:
    frame = _toy_frame()
    spec = GamVariantSpec(
        variant_id="toy",
        idea_id="toy",
        description="toy",
        feature_names=("f0", "f1"),
        n_splines=5,
        lam=1.0,
        max_iter=20,
        max_train_rows_per_class=25,
    )

    models, _ = fit_gam_variant(frame, ["f0", "f1"], spec)
    shape = smooth_shape_frame(models, spec, grid_points=12)
    read = shape_read(shape)

    assert set(shape["side"]) == {"short", "long"}
    assert read["term_count"] == 2
    assert len(read["top_terms"]) >= 1
