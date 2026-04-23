from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "foundation" / "pipelines" / "materialize_fpmarkets_v2_stage07_tier_b_dual_verdict.py"
RAW_ROOT = REPO_ROOT / "data" / "raw" / "mt5_bars" / "m5"
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


def load_module(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module spec from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


class Stage07DualVerdictTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_module("materialize_fpmarkets_v2_stage07_tier_b_dual_verdict", MODULE_PATH)

    def write_weights_csv(
        self,
        path: Path,
        *,
        overrides: dict[str, dict[str, float]] | None = None,
        extra_columns: dict[str, float] | None = None,
    ) -> None:
        overrides = overrides or {}
        rows = []
        for month in pd.period_range("2022-08", "2026-04", freq="M").astype(str):
            row = {
                "month": month,
                "msft_xnas_weight": 1.0 / 3.0,
                "nvda_xnas_weight": 1.0 / 3.0,
                "aapl_xnas_weight": 1.0 / 3.0,
            }
            row.update(overrides.get(month, {}))
            if extra_columns:
                row.update(extra_columns)
            rows.append(row)
        pd.DataFrame(rows).to_csv(path, index=False)

    def test_valid_user_weight_csv_materializes_keep_and_yes_verdict(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            weights_path = temp_root / "real_weights.csv"
            self.write_weights_csv(
                weights_path,
                overrides={
                    "2022-09": {
                        "msft_xnas_weight": 0.55,
                        "nvda_xnas_weight": 0.25,
                        "aapl_xnas_weight": 0.20,
                    },
                    "2025-09": {
                        "msft_xnas_weight": 0.25,
                        "nvda_xnas_weight": 0.55,
                        "aapl_xnas_weight": 0.20,
                    },
                },
            )

            outputs = self.module.materialize_dual_verdict(
                raw_root=RAW_ROOT,
                weights_path=weights_path,
                weights_version_label="test_real_weights_v1",
                row_labels_path=ROW_LABELS_PATH,
                baseline_summary_path=BASELINE_SUMMARY_PATH,
                output_root=temp_root / "02_runs" / "tier_b_dual_verdict_0001",
                reviews_root=temp_root / "03_reviews",
                reviewed_on="2026-04-23",
            )

            self.assertTrue(Path(outputs["manifest_path"]).exists())
            self.assertTrue(Path(outputs["evaluation_path"]).exists())
            self.assertTrue(Path(outputs["control_path"]).exists())
            self.assertTrue(Path(outputs["verdict_path"]).exists())
            self.assertTrue(Path(outputs["report_path"]).exists())
            self.assertTrue(Path(outputs["decision_path"]).exists())

            self.assertEqual(outputs["weights_version"], "test_real_weights_v1")
            self.assertEqual(
                outputs["evaluation_summary"]["weights_source_status"],
                self.module.VALIDATED_WEIGHTS_SOURCE_STATUS,
            )
            self.assertEqual(outputs["verdict_summary"]["separate_lane_verdict"], "keep")
            self.assertEqual(outputs["verdict_summary"]["mt5_candidate_verdict"], "yes")
            self.assertGreater(
                outputs["verdict_summary"]["decision_boundary"]["holdout_positive_proxy_config_count"],
                0,
            )
            self.assertLess(
                outputs["verdict_summary"]["decision_boundary"]["observed_holdout_tier_b_log_loss"],
                outputs["verdict_summary"]["decision_boundary"]["stage06_full_baseline_holdout_tier_b_log_loss"],
            )
            self.assertIn(
                "weight-neutral",
                outputs["evaluation_summary"]["active_surface"]["weights_surface_note"],
            )

            report_text = Path(outputs["report_path"]).read_text(encoding="utf-8-sig")
            self.assertIn("MT5 feasibility candidate", report_text)
            self.assertNotIn("simulated execution", report_text)
            self.assertNotIn("operating promotion", report_text)
            self.assertNotIn("runtime approval", report_text)

    def test_invalid_weight_month_coverage_raises_blocked_error(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            weights_path = Path(temp_dir) / "broken_weights.csv"
            rows = [
                {
                    "month": "2022-08",
                    "msft_xnas_weight": 0.5,
                    "nvda_xnas_weight": 0.3,
                    "aapl_xnas_weight": 0.2,
                }
            ]
            pd.DataFrame(rows).to_csv(weights_path, index=False)

            with self.assertRaises(self.module.BlockedWeightsError) as context:
                self.module.materialize_dual_verdict(
                    raw_root=RAW_ROOT,
                    weights_path=weights_path,
                    weights_version_label=None,
                    row_labels_path=ROW_LABELS_PATH,
                    baseline_summary_path=BASELINE_SUMMARY_PATH,
                    output_root=Path(temp_dir) / "02_runs" / "tier_b_dual_verdict_0001",
                    reviews_root=Path(temp_dir) / "03_reviews",
                    reviewed_on="2026-04-23",
                )

            self.assertEqual(context.exception.reason_code, "weights_month_coverage_invalid")
            self.assertIn("blocked", context.exception.message)
