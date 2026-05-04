from __future__ import annotations

import numpy as np
import pandas as pd

from foundation.models.elasticnet_logistic import (
    ElasticNetLogisticVariantSpec,
    coefficient_frame,
    coefficient_shape_read,
    default_stage21_elasticnet_variants,
    fit_elasticnet_variant,
    probability_frame,
    sign_overlap_read,
)


def _toy_frame(rows: int = 90) -> pd.DataFrame:
    rng = np.random.default_rng(21)
    x1 = np.linspace(-2.0, 2.0, rows)
    x2 = rng.normal(0.0, 0.5, rows)
    labels = np.where(x1 < -0.55, 0, np.where(x1 > 0.55, 2, 1))
    frame = pd.DataFrame(
        {
            "timestamp": pd.date_range("2024-01-01", periods=rows, freq="5min", tz="UTC"),
            "symbol": "US100",
            "split": ["train"] * 60 + ["validation"] * 15 + ["oos"] * 15,
            "label": [str(value) for value in labels],
            "label_class": labels,
            "x1": x1,
            "x2": x2,
            "x3": rng.normal(0.0, 0.2, rows),
        }
    )
    return frame


def test_elasticnet_probability_frame_uses_project_probability_order() -> None:
    frame = _toy_frame()
    spec = ElasticNetLogisticVariantSpec(
        variant_id="unit",
        idea_id="unit",
        description="unit",
        feature_names=("x1", "x2", "x3"),
        c_value=0.8,
        l1_ratio=0.35,
        max_iter=20000,
        tol=1.0e-2,
        random_state=210,
    )

    model, sample = fit_elasticnet_variant(frame, ["x1", "x2", "x3"], spec)
    probabilities = probability_frame(model, frame, spec.feature_names)

    assert sample["feature_count"] == 3
    assert list(probabilities.columns[:6]) == ["timestamp", "split", "label_class", "p_short", "p_flat", "p_long"]
    assert np.allclose(probabilities[["p_short", "p_flat", "p_long"]].sum(axis=1), 1.0)


def test_coefficient_read_and_sign_overlap_are_stable() -> None:
    frame = _toy_frame()
    spec = ElasticNetLogisticVariantSpec(
        variant_id="unit",
        idea_id="unit",
        description="unit",
        feature_names=("x1", "x2", "x3"),
        c_value=0.8,
        l1_ratio=0.35,
        max_iter=20000,
        tol=1.0e-2,
        random_state=211,
    )
    model, _ = fit_elasticnet_variant(frame, ["x1", "x2", "x3"], spec)
    coefficients = coefficient_frame(model, spec.feature_names)
    read = coefficient_shape_read(coefficients)
    overlap = sign_overlap_read(coefficients, coefficients)

    assert read["feature_count"] == 3
    assert read["nonzero_feature_count"] >= 1
    assert overlap["same_dominant_sign_share"] == 1.0


def test_default_stage21_variants_include_tier_b_and_full_context() -> None:
    full = ["x1", "x2", "x3", "macro"]
    tier_b = ["x1", "x2", "x3"]

    variants = default_stage21_elasticnet_variants(full_feature_order=full, tier_b_feature_order=tier_b)

    assert any(variant.tier_b_compatible for variant in variants)
    assert any(not variant.tier_b_compatible for variant in variants)
    assert all(0.0 < variant.l1_ratio < 1.0 for variant in variants)
