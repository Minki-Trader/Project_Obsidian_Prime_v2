from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
MODEL_MODULE_PATH = REPO_ROOT / "foundation" / "models" / "baseline_training.py"
PIPELINE_MODULE_PATH = REPO_ROOT / "foundation" / "pipelines" / "run_stage07_baseline_training_smoke.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module spec from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class Stage07BaselineTrainingSmokeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.model_module = load_module("baseline_training", MODEL_MODULE_PATH)
        cls.pipeline_module = load_module("run_stage07_baseline_training_smoke", PIPELINE_MODULE_PATH)

    def _frame(self) -> pd.DataFrame:
        rows = []
        timestamps = pd.date_range("2025-01-02T16:35:00Z", periods=12, freq="5min")
        splits = ["train"] * 6 + ["validation"] * 3 + ["oos"] * 3
        labels = [0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2]
        for index, timestamp in enumerate(timestamps):
            label = labels[index]
            rows.append(
                {
                    "timestamp": timestamp,
                    "symbol": "US100",
                    "split": splits[index],
                    "label": self.model_module.LABEL_NAMES[label],
                    "label_class": label,
                    "f1": float(label) + index * 0.01,
                    "f2": float(index % 3) - 0.5,
                }
            )
        return pd.DataFrame(rows)

    def test_evaluate_model_returns_fixed_probability_order(self) -> None:
        frame = self._frame()
        feature_order = ["f1", "f2"]
        config = self.model_module.BaselineTrainingConfig(max_iter=200)

        model = self.model_module.train_baseline_model(frame, feature_order, config)
        metrics, predictions = self.model_module.evaluate_model(model, frame, feature_order)

        self.assertEqual(list(predictions.columns[-3:]), ["p_short", "p_flat", "p_long"])
        self.assertTrue(metrics["probability_checks"]["finite"])
        self.assertLess(metrics["probability_checks"]["row_sum_max_abs_error"], 1e-12)

    def test_pipeline_writes_training_smoke_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            input_path = root / "model_input.parquet"
            summary_path = root / "model_input_summary.json"
            feature_order_path = root / "feature_order.txt"
            stage06_path = root / "stage06_report.json"
            run_root = root / "run"

            self._frame().to_parquet(input_path, index=False)
            summary_path.write_text(json.dumps({"rows": 12}), encoding="utf-8")
            feature_order_path.write_text("f1\nf2\n", encoding="utf-8")
            stage06_path.write_text(
                json.dumps(
                    {
                        "runtime_state": "runtime_authority",
                        "external_verification_status": "completed",
                    }
                ),
                encoding="utf-8",
            )

            original_hash = self.pipeline_module.FEATURE_ORDER_HASH
            self.pipeline_module.FEATURE_ORDER_HASH = self.pipeline_module.ordered_hash(["f1", "f2"])
            try:
                payload = self.pipeline_module.run_stage07_baseline_training_smoke(
                    model_input_path=input_path,
                    model_input_summary_path=summary_path,
                    feature_order_path=feature_order_path,
                    stage06_report_path=stage06_path,
                    run_output_root=run_root,
                    random_seed=7,
                    max_iter=200,
                )
            finally:
                self.pipeline_module.FEATURE_ORDER_HASH = original_hash

            self.assertEqual(payload["status"], "ok")
            self.assertTrue((run_root / "model.joblib").exists())
            self.assertTrue((run_root / "run_manifest.json").exists())
            self.assertTrue((run_root / "kpi_record.json").exists())
            manifest = json.loads((run_root / "model_artifact_manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["probability_output_order"], ["p_short", "p_flat", "p_long"])


if __name__ == "__main__":
    unittest.main()
