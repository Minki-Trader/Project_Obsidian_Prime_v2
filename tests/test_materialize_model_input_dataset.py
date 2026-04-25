from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "foundation" / "pipelines" / "materialize_model_input_dataset.py"
TRAINING_DATASET_PATH = (
    REPO_ROOT
    / "data"
    / "processed"
    / "training_datasets"
    / "label_v1_fwd12_split_v1"
    / "training_dataset.parquet"
)
TRAINING_SUMMARY_PATH = TRAINING_DATASET_PATH.with_name("training_dataset_summary.json")


def load_model_input_module():
    module_name = "materialize_model_input_dataset"
    spec = importlib.util.spec_from_file_location(module_name, MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module spec from {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


class MaterializeModelInputDatasetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_model_input_module()

    def _sample_training_frame(self) -> pd.DataFrame:
        rows = {
            "timestamp": pd.to_datetime(["2025-01-02T16:35:00Z", "2025-01-02T16:40:00Z"], utc=True),
            "symbol": ["US100", "US100"],
            "future_timestamp": pd.to_datetime(["2025-01-02T17:35:00Z", "2025-01-02T17:40:00Z"], utc=True),
            "future_log_return_12": [0.001, -0.001],
            "label": ["long", "short"],
            "label_class": [2, 0],
            "label_id": [self.module.TRAINING_LABEL_SPLIT_CONTRACT_VERSION, self.module.TRAINING_LABEL_SPLIT_CONTRACT_VERSION],
            "split": ["train", "validation"],
            "split_id": ["split_v1", "split_v1"],
            "horizon_bars": [12, 12],
            "horizon_minutes": [60, 60],
        }
        for index, feature_name in enumerate(self.module.FEATURE_ORDER, start=1):
            rows[feature_name] = [float(index), float(index) + 0.5]
        return pd.DataFrame(rows)

    def test_build_model_input_dataset_quarantines_placeholder_weight_features(self) -> None:
        model_input, summary = self.module.build_model_input_dataset(self._sample_training_frame())

        self.assertEqual(len(model_input), 2)
        self.assertEqual(summary["source_feature_count"], 58)
        self.assertEqual(summary["included_feature_count"], 56)
        self.assertEqual(summary["quarantined_feature_count"], 2)
        for feature_name in self.module.QUARANTINED_FEATURES:
            self.assertNotIn(feature_name, model_input.columns)
            self.assertIn(feature_name, summary["quarantined_features"])
        self.assertIn("mega8_equal_return_1", model_input.columns)
        self.assertEqual(summary["split_summary"]["train"]["rows"], 1)
        self.assertEqual(summary["split_summary"]["validation"]["rows"], 1)

    def test_missing_quarantined_source_feature_fails(self) -> None:
        frame = self._sample_training_frame().drop(columns=[self.module.QUARANTINED_FEATURES[0]])

        with self.assertRaisesRegex(RuntimeError, "Cannot quarantine missing features"):
            self.module.build_model_input_dataset(frame)

    def test_materialize_model_input_dataset_writes_manifests_from_real_stage03_dataset(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_root = Path(temp_dir) / "model_input"
            run_root = Path(temp_dir) / "run"
            payload = self.module.materialize_model_input_dataset(
                source_training_dataset_id=self.module.DEFAULT_SOURCE_TRAINING_DATASET_ID,
                model_input_dataset_id=self.module.DEFAULT_MODEL_INPUT_DATASET_ID,
                training_dataset_path=TRAINING_DATASET_PATH,
                training_summary_path=TRAINING_SUMMARY_PATH,
                output_root=output_root,
                run_output_root=run_root,
            )

            summary = json.loads(Path(payload["model_input_summary_path"]).read_text(encoding="utf-8"))
            feature_manifest = json.loads((output_root / "feature_set_manifest.json").read_text(encoding="utf-8"))
            quarantine_manifest = json.loads((output_root / "quarantine_manifest.json").read_text(encoding="utf-8"))
            materialized = pd.read_parquet(payload["model_input_dataset_path"])

            self.assertEqual(summary["rows"], 46650)
            self.assertEqual(summary["included_feature_count"], 56)
            self.assertEqual(feature_manifest["included_feature_count"], 56)
            self.assertEqual(quarantine_manifest["first_baseline_policy"], "exclude_from_model_input")
            for feature_name in self.module.QUARANTINED_FEATURES:
                self.assertNotIn(feature_name, materialized.columns)

    def test_build_model_input_dataset_58_feature_proxy_mode_restores_weight_features(self) -> None:
        model_input, summary = self.module.build_model_input_dataset(
            self._sample_training_frame(),
            mode=self.module.MODE_MT5_PRICE_PROXY_58,
        )

        self.assertEqual(len(model_input), 2)
        self.assertEqual(summary["source_feature_count"], 58)
        self.assertEqual(summary["included_feature_count"], 58)
        self.assertEqual(summary["quarantined_feature_count"], 0)
        self.assertEqual(summary["weight_source_status"], self.module.WEIGHT_PRICE_PROXY_STATUS)
        for feature_name in self.module.QUARANTINED_FEATURES:
            self.assertIn(feature_name, model_input.columns)
            self.assertIn(feature_name, summary["restored_features"])
