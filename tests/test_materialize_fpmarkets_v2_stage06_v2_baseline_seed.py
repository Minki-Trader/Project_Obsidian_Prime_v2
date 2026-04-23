from __future__ import annotations

import importlib.util
import json
import math
import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = (
    REPO_ROOT / "foundation" / "pipelines" / "materialize_fpmarkets_v2_stage06_v2_baseline_seed.py"
)
DATASET_MODULE_PATH = REPO_ROOT / "foundation" / "pipelines" / "materialize_fpmarkets_v2_dataset.py"
ROW_LABELS_PATH = (
    REPO_ROOT
    / "stages"
    / "06_tiered_readiness_exploration"
    / "02_runs"
    / "tiered_readiness_scorecard_0001"
    / "readiness_row_labels_fpmarkets_v2_tiered_readiness_0001.parquet"
)
RAW_ROOT = REPO_ROOT / "data" / "raw" / "mt5_bars" / "m5"

_CACHE: dict[str, object] = {}


def load_module(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module spec from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def load_stage06_module():
    return load_module("materialize_fpmarkets_v2_stage06_v2_baseline_seed", MODULE_PATH)


def load_dataset_module():
    return load_module("materialize_fpmarkets_v2_dataset_for_stage06_baseline_seed_tests", DATASET_MODULE_PATH)


def get_cached_outputs():
    if "outputs" not in _CACHE:
        dataset_module = load_dataset_module()
        stage06_module = load_stage06_module()
        frame, _ = dataset_module.build_feature_frame(RAW_ROOT)
        row_labels = stage06_module.load_row_labels(ROW_LABELS_PATH)
        model_frame = stage06_module.build_model_frame(frame, row_labels)
        probability_table, thresholds = stage06_module.build_probability_table(model_frame)
        evaluation_summary = stage06_module.build_evaluation_summary(
            probability_table,
            row_labels_path=ROW_LABELS_PATH.as_posix(),
        )
        calibration_read = stage06_module.build_calibration_read(probability_table)
        _CACHE["module"] = stage06_module
        _CACHE["probability_table"] = probability_table
        _CACHE["thresholds"] = thresholds
        _CACHE["evaluation_summary"] = evaluation_summary
        _CACHE["calibration_read"] = calibration_read
    return _CACHE


class LabelBoundaryUnitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_stage06_module()

    def test_target_label_includes_q33_and_q67_edges(self) -> None:
        self.assertEqual(self.module.assign_target_label(-1.0, q33=-1.0, q67=2.0), "short")
        self.assertEqual(self.module.assign_target_label(2.0, q33=-1.0, q67=2.0), "long")
        self.assertEqual(self.module.assign_target_label(0.5, q33=-1.0, q67=2.0), "flat")

    def test_data_split_boundaries_are_inclusive(self) -> None:
        self.assertEqual(
            self.module.assign_data_split(pd.Timestamp("2024-12-31T23:55:00Z")),
            "train",
        )
        self.assertEqual(
            self.module.assign_data_split(pd.Timestamp("2025-08-31T23:55:00Z")),
            "validation",
        )
        self.assertEqual(
            self.module.assign_data_split(pd.Timestamp("2026-04-13T23:55:00Z")),
            "holdout",
        )


class FitLaneUnitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cache = get_cached_outputs()
        cls.module = cache["module"]
        cls.probability_table = cache["probability_table"]

    def test_fit_lane_uses_train_tier_a_only(self) -> None:
        fit_rows = self.probability_table.loc[self.probability_table["row_used_for_fit"]]
        self.assertTrue((fit_rows["data_split"] == "train").all())
        self.assertTrue((fit_rows["readiness_tier"] == "tier_a").all())

        non_fit_train_tier_b = self.probability_table.loc[
            self.probability_table["data_split"].eq("train")
            & self.probability_table["readiness_tier"].eq("tier_b")
        ]
        self.assertTrue(non_fit_train_tier_b.empty)


class Stage06BaselineIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cache = get_cached_outputs()
        cls.module = cache["module"]
        cls.probability_table = cache["probability_table"]
        cls.thresholds = cache["thresholds"]
        cls.evaluation_summary = cache["evaluation_summary"]
        cls.calibration_read = cache["calibration_read"]

    def test_real_data_thresholds_and_lane_counts_match_expected_values(self) -> None:
        self.assertTrue(math.isclose(self.thresholds["q33"], -0.00035087247936272335, rel_tol=0, abs_tol=1e-15))
        self.assertTrue(math.isclose(self.thresholds["q67"], 0.0004049556640609367, rel_tol=0, abs_tol=1e-15))

        validation = self.evaluation_summary["splits"]["validation"]
        holdout = self.evaluation_summary["splits"]["holdout"]

        self.assertEqual(validation["strict_tier_a"]["row_count"], 10618)
        self.assertEqual(validation["tier_b_exploration"]["row_count"], 15866)
        self.assertEqual(holdout["strict_tier_a"]["row_count"], 10144)
        self.assertEqual(holdout["tier_b_exploration"]["row_count"], 17978)

    def test_integration_write_outputs_materializes_expected_files_and_report_text(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            output_root = temp_root / "tier_b_offline_eval_0001"
            report_path = temp_root / "report.md"
            outputs = self.module.write_outputs(
                output_root=output_root,
                report_path=report_path,
                row_labels_path=ROW_LABELS_PATH,
                probability_table=self.probability_table,
                thresholds=self.thresholds,
                reviewed_on="2026-04-22",
            )

            probability_frame = pd.read_parquet(outputs["probability_path"])
            self.assertEqual(
                list(probability_frame.columns),
                [
                    "timestamp",
                    "symbol",
                    "data_split",
                    "fit_lane",
                    "readiness_tier",
                    "reporting_lane",
                    "missing_groups",
                    "missing_symbols",
                    "row_used_for_fit",
                    "row_received_imputation",
                    "row_pre_imputation_nan_count",
                    "future_log_return_1",
                    "target_label",
                    "predicted_label",
                    "p_short",
                    "p_flat",
                    "p_long",
                    "target_index",
                    "predicted_index",
                ],
            )

            summary_payload = json.loads(Path(outputs["summary_path"]).read_text(encoding="utf-8"))
            self.assertAlmostEqual(
                summary_payload["splits"]["holdout"]["tier_b_exploration"]["log_loss"],
                1.9636202232302509,
                places=6,
            )
            self.assertAlmostEqual(
                summary_payload["splits"]["holdout"]["tier_b_exploration"]["macro_f1"],
                0.3364373934357654,
                places=6,
            )

            calibration_payload = json.loads(Path(outputs["calibration_path"]).read_text(encoding="utf-8"))
            self.assertIn("expected_calibration_error", calibration_payload["splits"]["holdout"]["tier_b_exploration"])

            report_text = Path(outputs["report_path"]).read_text(encoding="utf-8-sig")
            self.assertIn("Stage 06 First v2 Baseline Seed Review", report_text)
            self.assertIn("no legacy `model", report_text)
            self.assertIn("Mixed Aggregate Info-Only", report_text)
