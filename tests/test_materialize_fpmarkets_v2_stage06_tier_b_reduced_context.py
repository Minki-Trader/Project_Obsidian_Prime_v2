from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = (
    REPO_ROOT / "foundation" / "pipelines" / "materialize_fpmarkets_v2_stage06_tier_b_reduced_context.py"
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
BASELINE_SUMMARY_PATH = (
    REPO_ROOT
    / "stages"
    / "06_tiered_readiness_exploration"
    / "02_runs"
    / "tier_b_offline_eval_0001"
    / "baseline_evaluation_summary_fpmarkets_v2_tier_b_offline_eval_0001.json"
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
    return load_module("materialize_fpmarkets_v2_stage06_tier_b_reduced_context", MODULE_PATH)


def load_dataset_module():
    return load_module("materialize_fpmarkets_v2_dataset_for_stage06_reduced_context_tests", DATASET_MODULE_PATH)


def get_cached_outputs():
    if "outputs" not in _CACHE:
        dataset_module = load_dataset_module()
        stage06_module = load_stage06_module()
        frame, _ = dataset_module.build_feature_frame(RAW_ROOT)
        row_labels = stage06_module.load_row_labels(ROW_LABELS_PATH)
        baseline_summary = stage06_module.load_baseline_summary(BASELINE_SUMMARY_PATH)
        model_frame = stage06_module.build_model_frame(frame, row_labels)
        probability_table, thresholds = stage06_module.build_probability_table(model_frame)
        evaluation_summary = stage06_module.build_evaluation_summary(
            probability_table,
            row_labels_path=ROW_LABELS_PATH.as_posix(),
            baseline_summary=baseline_summary,
        )
        calibration_read = stage06_module.build_calibration_read(probability_table)
        _CACHE["module"] = stage06_module
        _CACHE["probability_table"] = probability_table
        _CACHE["thresholds"] = thresholds
        _CACHE["evaluation_summary"] = evaluation_summary
        _CACHE["calibration_read"] = calibration_read
        _CACHE["baseline_summary"] = baseline_summary
    return _CACHE


class ReducedContextSchemaUnitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_stage06_module()

    def test_schema_counts_match_draft(self) -> None:
        self.assertEqual(len(self.module.ACTIVE_FEATURES), 42)
        self.assertEqual(len(self.module.CONDITIONAL_FEATURES), 6)
        self.assertEqual(len(self.module.DROPPED_FEATURES), 10)

    def test_subtype_tag_mapping_stays_reporting_only(self) -> None:
        self.assertEqual(
            self.module.assign_tier_b_subtype_tag(
                readiness_tier="tier_b",
                missing_groups="g4_leader_equity|g5_breadth_extension",
            ),
            "b_eq_dark",
        )
        self.assertEqual(
            self.module.assign_tier_b_subtype_tag(
                readiness_tier="tier_b",
                missing_groups="g3_macro_proxy",
            ),
            "b_macro_late",
        )
        self.assertIsNone(
            self.module.assign_tier_b_subtype_tag(
                readiness_tier="tier_a",
                missing_groups="",
            )
        )


class ReducedContextIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cache = get_cached_outputs()
        cls.module = cache["module"]
        cls.probability_table = cache["probability_table"]
        cls.thresholds = cache["thresholds"]
        cls.evaluation_summary = cache["evaluation_summary"]
        cls.calibration_read = cache["calibration_read"]
        cls.baseline_summary = cache["baseline_summary"]

    def assert_metric_close(self, actual: float, expected: float, *, tolerance: float = 1e-6) -> None:
        self.assertLessEqual(abs(actual - expected), tolerance)

    def test_probability_table_carries_subtype_tag_and_expected_row_counts(self) -> None:
        self.assertIn("tier_b_subtype_tag", self.probability_table.columns)
        validation = self.evaluation_summary["splits"]["validation"]
        holdout = self.evaluation_summary["splits"]["holdout"]
        self.assertEqual(validation["strict_tier_a"]["row_count"], 10618)
        self.assertEqual(validation["tier_b_exploration"]["row_count"], 15866)
        self.assertEqual(holdout["strict_tier_a"]["row_count"], 10144)
        self.assertEqual(holdout["tier_b_exploration"]["row_count"], 17978)

    def test_real_data_holdout_tier_b_improves_over_full_baseline(self) -> None:
        holdout_tier_b = self.evaluation_summary["splits"]["holdout"]["tier_b_exploration"]
        holdout_delta = self.evaluation_summary["comparison_to_full_baseline_seed"]["holdout"]["tier_b_exploration"]
        self.assert_metric_close(holdout_tier_b["log_loss"], 1.5035784272328496)
        self.assert_metric_close(holdout_tier_b["macro_f1"], 0.3728357269186551)
        self.assert_metric_close(holdout_tier_b["balanced_accuracy"], 0.3718663890063581)
        self.assert_metric_close(holdout_tier_b["multiclass_brier_score"], 0.6585876376762716)
        self.assert_metric_close(holdout_delta["log_loss_delta_vs_full_baseline"], -0.46004179599740125)
        self.assert_metric_close(holdout_delta["macro_f1_delta_vs_full_baseline"], 0.03639874367485054)

    def test_real_data_subtype_breakdown_matches_expected_pattern(self) -> None:
        validation_subtypes = self.evaluation_summary["tier_b_subtype_info_only"]["validation"]
        holdout_subtypes = self.evaluation_summary["tier_b_subtype_info_only"]["holdout"]
        self.assert_metric_close(validation_subtypes["b_eq_dark"]["row_share_within_tier_b"], 0.8641119374763645)
        self.assert_metric_close(validation_subtypes["b_eq_dark"]["log_loss"], 1.8192341032135278)
        self.assert_metric_close(holdout_subtypes["b_eq_dark"]["row_share_within_tier_b"], 0.9054399822004673)
        self.assert_metric_close(holdout_subtypes["b_eq_dark"]["log_loss"], 1.4807601271478656)
        self.assert_metric_close(holdout_subtypes["b_macro_late"]["log_loss"], 1.7226901306789324)

    def test_write_outputs_materializes_expected_files_and_report_text(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            output_root = temp_root / "tier_b_reduced_context_0001"
            report_path = temp_root / "report.md"
            outputs = self.module.write_outputs(
                output_root=output_root,
                report_path=report_path,
                row_labels_path=ROW_LABELS_PATH,
                baseline_summary=self.baseline_summary,
                probability_table=self.probability_table,
                thresholds=self.thresholds,
                reviewed_on="2026-04-22",
            )

            probability_frame = pd.read_parquet(outputs["probability_path"])
            self.assertIn("tier_b_subtype_tag", probability_frame.columns)

            summary_payload = json.loads(Path(outputs["summary_path"]).read_text(encoding="utf-8"))
            self.assertIn("comparison_to_full_baseline_seed", summary_payload)
            self.assertIn("tier_b_subtype_info_only", summary_payload)

            calibration_payload = json.loads(Path(outputs["calibration_path"]).read_text(encoding="utf-8"))
            self.assertIn("expected_calibration_error", calibration_payload["splits"]["holdout"]["tier_b_exploration"])

            report_text = Path(outputs["report_path"]).read_text(encoding="utf-8-sig")
            self.assertIn("Stage 06 First Tier B Reduced-Context Model Review", report_text)
            self.assertIn("Comparison To Full Baseline Seed", report_text)
            self.assertIn("Tier B Subtype Info-Only", report_text)
