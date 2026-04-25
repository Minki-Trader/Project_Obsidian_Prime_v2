from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "foundation" / "pipelines" / "materialize_training_label_split_dataset.py"
FEATURES_PATH = (
    REPO_ROOT
    / "data"
    / "processed"
    / "datasets"
    / "dataset_fpmarkets_v2_us100_m5_20220901_20260413_cashopen_fullcash_valid_freeze01"
    / "features.parquet"
)
SOURCE_SUMMARY_PATH = FEATURES_PATH.with_name("dataset_summary.json")
RAW_ROOT = REPO_ROOT / "data" / "raw" / "mt5_bars" / "m5"


def load_training_module():
    module_name = "materialize_training_label_split_dataset"
    spec = importlib.util.spec_from_file_location(module_name, MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module spec from {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


class MaterializeTrainingLabelSplitDatasetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_training_module()

    def test_label_candidates_use_exact_future_timestamp_not_next_valid_row(self) -> None:
        spec = self.module.TrainingLabelSplitSpec()
        features = pd.DataFrame(
            {
                "timestamp": pd.to_datetime(
                    [
                        "2025-01-02T16:35:00Z",
                        "2025-01-02T16:40:00Z",
                        "2025-01-02T22:05:00Z",
                    ],
                    utc=True,
                ),
                "symbol": ["US100", "US100", "US100"],
                "minutes_from_cash_open": [5.0, 10.0, 335.0],
            }
        )
        raw = pd.DataFrame(
            {
                "timestamp": pd.to_datetime(
                    [
                        "2025-01-02T16:35:00Z",
                        "2025-01-02T17:35:00Z",
                        "2025-01-02T16:40:00Z",
                        "2025-01-02T17:45:00Z",
                        "2025-01-02T22:05:00Z",
                        "2025-01-02T23:05:00Z",
                    ],
                    utc=True,
                ),
                "close": [100.0, 101.0, 200.0, 220.0, 300.0, 330.0],
            }
        )

        labelable = self.module.build_label_candidates(features, raw, spec)

        self.assertEqual(len(labelable), 1)
        self.assertEqual(
            pd.Timestamp(labelable.iloc[0]["future_timestamp"]),
            pd.Timestamp("2025-01-02T17:35:00Z"),
        )

    def test_build_training_dataset_matches_stage03_default_counts(self) -> None:
        features = self.module.load_feature_dataset(FEATURES_PATH)
        raw = self.module.load_us100_close_series(RAW_ROOT)
        training, summary = self.module.build_training_dataset(
            features,
            raw,
            self.module.TrainingLabelSplitSpec(),
        )

        self.assertEqual(len(training), 46650)
        self.assertEqual(summary["split_summary"]["train"]["rows"], 29222)
        self.assertEqual(summary["split_summary"]["validation"]["rows"], 9844)
        self.assertEqual(summary["split_summary"]["oos"]["rows"], 7584)
        self.assertAlmostEqual(summary["threshold_log_return"], 0.001277833051854688, places=15)
        self.assertEqual(summary["split_summary"]["train"]["class_distribution"]["flat"], 9643)

    def test_materialize_training_dataset_writes_summary_and_manifests(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_root = Path(temp_dir) / "training"
            run_root = Path(temp_dir) / "run"
            payload = self.module.materialize_training_label_split_dataset(
                source_dataset_id=self.module.DEFAULT_SOURCE_DATASET_ID,
                training_dataset_id=self.module.DEFAULT_TRAINING_DATASET_ID,
                features_path=FEATURES_PATH,
                source_summary_path=SOURCE_SUMMARY_PATH,
                raw_root=RAW_ROOT,
                output_root=output_root,
                run_output_root=run_root,
            )

            summary = json.loads(Path(payload["training_dataset_summary_path"]).read_text(encoding="utf-8"))
            manifest = json.loads((run_root / "run_manifest.json").read_text(encoding="utf-8"))

            self.assertEqual(summary["training_dataset_id"], self.module.DEFAULT_TRAINING_DATASET_ID)
            self.assertEqual(summary["rows"], 46650)
            self.assertEqual(summary["class_id_map"], {"short": 0, "flat": 1, "long": 2})
            self.assertEqual(manifest["external_verification_status"], "not_applicable")
