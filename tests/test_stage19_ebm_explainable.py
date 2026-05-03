from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


@unittest.skipIf(importlib.util.find_spec("interpret") is None, "interpret package is not installed")
class Stage19EbmExplainableTests(unittest.TestCase):
    def test_ebm_probability_frame_and_term_importance(self) -> None:
        from foundation.models.ebm_explainable import (
            EbmVariantSpec,
            fit_ebm_variant,
            probability_frame,
            shape_read,
            term_importance_frame,
        )

        rows = 120
        feature_order = ["feature_a", "feature_b", "feature_c"]
        frame = pd.DataFrame(
            {
                "timestamp": pd.date_range("2024-01-01", periods=rows, freq="5min", tz="UTC"),
                "symbol": "US100",
                "split": ["train"] * 72 + ["validation"] * 24 + ["oos"] * 24,
                "label": ["short", "flat", "long", "flat"] * 30,
                "label_class": ([0, 1, 2, 1] * 30),
                "feature_a": np.linspace(-1.0, 1.0, rows),
                "feature_b": np.sin(np.linspace(0.0, 8.0, rows)),
                "feature_c": np.cos(np.linspace(0.0, 5.0, rows)),
            }
        )
        spec = EbmVariantSpec(
            variant_id="unit_ebm",
            idea_id="unit",
            description="Unit EBM",
            max_bins=16,
            interactions=0,
            outer_bags=1,
            learning_rate=0.05,
            max_rounds=20,
            early_stopping_rounds=5,
            min_samples_leaf=2,
            random_state=19,
        )

        model, sample = fit_ebm_variant(frame, feature_order, spec)
        probabilities = probability_frame(model, frame, feature_order)
        importance = term_importance_frame(model, feature_order)
        read = shape_read(importance)

        self.assertEqual(sample["feature_count"], 3)
        self.assertEqual(len(probabilities), rows)
        self.assertLess(float(np.abs(probabilities[["p_short", "p_flat", "p_long"]].sum(axis=1) - 1.0).max()), 1e-12)
        self.assertEqual(read["term_count"], 3)
        self.assertIn("gain_share", importance.columns)

    def test_ebm_main_effect_onnx_export_matches_probability(self) -> None:
        from foundation.models.ebm_explainable import EbmVariantSpec, fit_ebm_variant
        from foundation.models.ebm_onnx import check_ebm_onnx_probability_parity, export_ebm_main_effects_to_onnx

        rows = 120
        feature_order = ["feature_a", "feature_b", "feature_c"]
        frame = pd.DataFrame(
            {
                "timestamp": pd.date_range("2024-01-01", periods=rows, freq="5min", tz="UTC"),
                "symbol": "US100",
                "split": ["train"] * 72 + ["validation"] * 24 + ["oos"] * 24,
                "label": ["short", "flat", "long", "flat"] * 30,
                "label_class": ([0, 1, 2, 1] * 30),
                "feature_a": np.linspace(-1.0, 1.0, rows),
                "feature_b": np.sin(np.linspace(0.0, 8.0, rows)),
                "feature_c": np.cos(np.linspace(0.0, 5.0, rows)),
            }
        )
        spec = EbmVariantSpec(
            variant_id="unit_ebm_onnx",
            idea_id="unit",
            description="Unit EBM ONNX",
            max_bins=16,
            interactions=0,
            outer_bags=1,
            learning_rate=0.05,
            max_rounds=20,
            early_stopping_rounds=5,
            min_samples_leaf=2,
            random_state=29,
        )
        model, _sample = fit_ebm_variant(frame, feature_order, spec)

        output_path = ROOT / "stages/19_model_family_challenge__ebm_explainable_boosting_shape/02_runs/unit_ebm_onnx_test/model.onnx"
        export_ebm_main_effects_to_onnx(model, output_path, feature_count=len(feature_order))
        parity = check_ebm_onnx_probability_parity(
            model,
            output_path,
            frame.loc[:, feature_order].to_numpy(dtype="float64"),
            tolerance=1.0e-3,
        )

        self.assertTrue(parity["passed"], parity)

    def test_ebm_score_table_export_matches_probability(self) -> None:
        from foundation.models.ebm_explainable import EbmVariantSpec, fit_ebm_variant
        from foundation.models.ebm_score_table import (
            check_ebm_score_table_probability_parity,
            export_ebm_main_effect_score_table,
        )

        rows = 120
        feature_order = ["feature_a", "feature_b", "feature_c"]
        frame = pd.DataFrame(
            {
                "timestamp": pd.date_range("2024-01-01", periods=rows, freq="5min", tz="UTC"),
                "symbol": "US100",
                "split": ["train"] * 72 + ["validation"] * 24 + ["oos"] * 24,
                "label": ["short", "flat", "long", "flat"] * 30,
                "label_class": ([0, 1, 2, 1] * 30),
                "feature_a": np.linspace(-1.0, 1.0, rows),
                "feature_b": np.sin(np.linspace(0.0, 8.0, rows)),
                "feature_c": np.cos(np.linspace(0.0, 5.0, rows)),
            }
        )
        spec = EbmVariantSpec(
            variant_id="unit_ebm_table",
            idea_id="unit",
            description="Unit EBM score table",
            max_bins=16,
            interactions=0,
            outer_bags=1,
            learning_rate=0.05,
            max_rounds=20,
            early_stopping_rounds=5,
            min_samples_leaf=2,
            random_state=39,
        )
        model, _sample = fit_ebm_variant(frame, feature_order, spec)

        output_path = ROOT / "stages/19_model_family_challenge__ebm_explainable_boosting_shape/02_runs/unit_ebm_table_test/model_score_table.csv"
        export_ebm_main_effect_score_table(model, output_path, feature_count=len(feature_order))
        parity = check_ebm_score_table_probability_parity(
            model,
            output_path,
            frame.loc[:, feature_order].to_numpy(dtype="float64"),
            feature_count=len(feature_order),
        )

        self.assertTrue(parity["passed"], parity)


if __name__ == "__main__":
    unittest.main()
