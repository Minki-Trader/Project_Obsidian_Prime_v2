from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "foundation" / "pipelines" / "materialize_fpmarkets_v2_stage06_followup_pack.py"
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


def load_followup_module():
    return load_module("materialize_fpmarkets_v2_stage06_followup_pack", MODULE_PATH)


def get_cached_outputs():
    if "outputs" not in _CACHE:
        module = load_followup_module()
        frame, _ = module.baseline.build_feature_frame(RAW_ROOT)
        row_labels = module.baseline.load_row_labels(ROW_LABELS_PATH)
        model_frame = module.baseline.build_model_frame(frame, row_labels)
        probability_table, _ = module.baseline.build_probability_table(model_frame)
        calibration_summary = module.build_calibration_fit_summary(probability_table)
        control_summary = module.build_control_sensitivity_summary(probability_table, calibration_summary)
        robustness_summary = module.build_robustness_summary(probability_table)
        weight_summary = module.build_weight_verdict_summary(frame, row_labels)
        _CACHE["module"] = module
        _CACHE["frame"] = frame
        _CACHE["row_labels"] = row_labels
        _CACHE["probability_table"] = probability_table
        _CACHE["calibration_summary"] = calibration_summary
        _CACHE["control_summary"] = control_summary
        _CACHE["robustness_summary"] = robustness_summary
        _CACHE["weight_summary"] = weight_summary
    return _CACHE


class CalibrationFollowupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cache = get_cached_outputs()
        cls.calibration_summary = cache["calibration_summary"]

    def test_lane_specific_temperature_fits_improve_holdout_reads(self) -> None:
        tier_b_holdout = self.calibration_summary["evaluation"]["holdout"]["tier_b_exploration"]
        tier_a_holdout = self.calibration_summary["evaluation"]["holdout"]["strict_tier_a"]

        self.assertGreater(
            tier_b_holdout["identity_read_only"]["log_loss"],
            tier_b_holdout["tier_b_exploration_temperature_fit"]["log_loss"],
        )
        self.assertGreater(
            tier_b_holdout["strict_tier_a_temperature_fit"]["log_loss"],
            tier_b_holdout["tier_b_exploration_temperature_fit"]["log_loss"],
        )
        self.assertGreater(
            tier_a_holdout["identity_read_only"]["expected_calibration_error"],
            tier_a_holdout["strict_tier_a_temperature_fit"]["expected_calibration_error"],
        )

    def test_temperature_candidates_are_not_identity(self) -> None:
        strict_tier_a_temp = self.calibration_summary["fit_candidates"]["strict_tier_a_temperature_fit"]["temperature"]
        tier_b_temp = self.calibration_summary["fit_candidates"]["tier_b_exploration_temperature_fit"]["temperature"]
        self.assertGreater(strict_tier_a_temp, 1.0)
        self.assertGreater(tier_b_temp, 1.0)


class ControlAndRobustnessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cache = get_cached_outputs()
        cls.control_summary = cache["control_summary"]
        cls.robustness_summary = cache["robustness_summary"]

    def test_holdout_tier_b_control_read_surfaces_sparse_positive_configs(self) -> None:
        finding = self.control_summary["splits"]["holdout"]["tier_b_exploration"]["draft_findings"]
        self.assertGreater(finding["positive_config_count"], 0)
        self.assertGreater(finding["best_proxy_config"]["active_rows"], 0)
        self.assertIn("sparse", finding["control_read"])

    def test_holdout_tier_b_dominant_missing_pattern_matches_expected_family(self) -> None:
        self.assertEqual(
            self.robustness_summary["draft_evidence_read"]["dominant_holdout_pattern"],
            "g4_leader_equity|g5_breadth_extension",
        )


class WeightVerdictTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cache = get_cached_outputs()
        cls.weight_summary = cache["weight_summary"]

    def test_weight_scenarios_stay_narrow_enough_for_offline_screen(self) -> None:
        self.assertEqual(len(self.weight_summary["scenario_rows"]), 4)
        self.assertTrue(self.weight_summary["draft_verdict"]["offline_screen_sufficient"])
        self.assertTrue(self.weight_summary["draft_verdict"]["real_weight_rerun_required_before_simulated_or_mt5"])
        self.assertLess(self.weight_summary["spread_summary"]["tier_b_holdout_log_loss_spread"], 0.02)


class FollowupIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cache = get_cached_outputs()
        cls.module = cache["module"]
        cls.calibration_summary = cache["calibration_summary"]
        cls.control_summary = cache["control_summary"]
        cls.robustness_summary = cache["robustness_summary"]
        cls.weight_summary = cache["weight_summary"]

    def test_write_outputs_materializes_expected_files_and_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            output_root = temp_root / "tier_b_followup_pack_0001"
            reviews_root = temp_root / "reviews"
            outputs = self.module.write_outputs(
                output_root=output_root,
                reviews_root=reviews_root,
                row_labels_path=ROW_LABELS_PATH,
                calibration_summary=self.calibration_summary,
                control_summary=self.control_summary,
                robustness_summary=self.robustness_summary,
                weight_summary=self.weight_summary,
                reviewed_on="2026-04-22",
            )

            self.assertTrue(Path(outputs["manifest_path"]).exists())
            self.assertTrue(Path(outputs["calibration_path"]).exists())
            self.assertTrue(Path(outputs["control_path"]).exists())
            self.assertTrue(Path(outputs["robustness_path"]).exists())
            self.assertTrue(Path(outputs["weight_path"]).exists())
            self.assertTrue(Path(outputs["stage07_draft_path"]).exists())
            self.assertTrue(Path(outputs["close_open_draft_path"]).exists())

            manifest_payload = json.loads(Path(outputs["manifest_path"]).read_text(encoding="utf-8"))
            self.assertEqual(manifest_payload["followup_pack_id"], "followup_pack_fpmarkets_v2_tier_b_0001")

            calibration_report_text = Path(outputs["calibration_report_path"]).read_text(encoding="utf-8-sig")
            self.assertIn("Tier B Calibration Fit Follow-Up", calibration_report_text)

            stage07_draft_text = Path(outputs["stage07_draft_path"]).read_text(encoding="utf-8-sig")
            self.assertIn("Stage 07 Alpha Design Draft", stage07_draft_text)
            self.assertIn("offline-only", stage07_draft_text)
