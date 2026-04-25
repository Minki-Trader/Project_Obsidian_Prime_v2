from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "foundation" / "pipelines" / "audit_stage05_feature_integrity.py"


def load_audit_module():
    module_name = "audit_stage05_feature_integrity"
    spec = importlib.util.spec_from_file_location(module_name, MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module spec from {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


class Stage05FeatureIntegrityAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_audit_module()

    def _feature_frame(self) -> pd.DataFrame:
        rows = {
            "timestamp": pd.to_datetime(["2025-01-02T16:35:00Z", "2025-01-02T16:40:00Z"], utc=True),
            "symbol": ["US100", "US100"],
        }
        for index, feature_name in enumerate(self.module.FEATURE_ORDER, start=1):
            rows[feature_name] = [float(index), float(index) + 0.5]
        return pd.DataFrame(rows)

    def _training_frame(self) -> pd.DataFrame:
        frame = self._feature_frame()
        frame["future_timestamp"] = frame["timestamp"] + pd.Timedelta(minutes=60)
        frame["future_log_return_12"] = [0.001, -0.002]
        frame["label"] = ["long", "short"]
        frame["label_class"] = [2, 0]
        frame["label_id"] = ["label_v1", "label_v1"]
        frame["split"] = ["train", "validation"]
        frame["split_id"] = ["split_v1", "split_v1"]
        frame["horizon_bars"] = [12, 12]
        frame["horizon_minutes"] = [60, 60]
        return frame

    def test_identity_schema_accepts_expected_feature_hash_and_columns(self) -> None:
        feature_frame = self._feature_frame()
        training_frame = self._training_frame()
        dataset_summary = {
            "selected_rows": len(feature_frame),
            "feature_count": len(self.module.FEATURE_ORDER),
            "feature_order_hash": self.module.EXPECTED_FEATURE_ORDER_HASH,
        }
        training_summary = {
            "rows": len(training_frame),
            "feature_order_hash": self.module.EXPECTED_FEATURE_ORDER_HASH,
        }
        model_summary = {
            "rows": len(training_frame),
            "included_feature_order_hash": self.module.EXPECTED_FEATURE_ORDER_HASH,
            "included_feature_count": len(self.module.FEATURE_ORDER),
        }

        audit = self.module.audit_identity_schema(
            feature_frame,
            training_frame,
            training_frame.copy(),
            dataset_summary,
            training_summary,
            model_summary,
        )

        self.assertEqual(audit["status"], "pass")
        self.assertEqual(audit["feature_order_hash"], self.module.EXPECTED_FEATURE_ORDER_HASH)

    def test_train_threshold_uses_train_split_only(self) -> None:
        frame = self._training_frame()
        frame.loc[0, "future_log_return_12"] = 0.01
        frame.loc[1, "future_log_return_12"] = 100.0

        threshold = self.module.compute_train_threshold_from_frame(frame)

        self.assertEqual(threshold, 0.01)

    def test_formula_audit_compares_exported_float32_surface(self) -> None:
        stored = self._feature_frame()
        recomputed = self._feature_frame()
        stored.loc[0, "ema50_ema200_diff"] = pd.Series([1000.123456], dtype="float32").iloc[0]
        recomputed.loc[0, "ema50_ema200_diff"] = 1000.123456

        audit = self.module.audit_feature_formula(
            stored,
            recomputed,
            {"target_id": "unit"},
            float_tolerance=1e-5,
        )

        self.assertEqual(audit["status"], "pass")

    def test_external_timestamp_alignment_reports_missing_exact_match(self) -> None:
        selected = pd.Series(pd.to_datetime(["2025-01-02T16:35:00Z", "2025-01-02T16:40:00Z"], utc=True))
        source = {
            "AAPL": pd.Series(pd.to_datetime(["2025-01-02T16:35:00Z"], utc=True)),
            "MSFT": pd.Series(pd.to_datetime(["2025-01-02T16:35:00Z", "2025-01-02T16:40:00Z"], utc=True)),
        }

        audit = self.module.audit_external_timestamp_alignment(selected, source)

        self.assertEqual(audit["status"], "fail")
        self.assertEqual(audit["missing_counts"]["AAPL"], 1)
        self.assertEqual(audit["missing_counts"]["MSFT"], 0)

    def test_dst_conversion_samples_pass(self) -> None:
        audit = self.module.audit_dst_conversion_samples()

        self.assertEqual(audit["status"], "pass")
        self.assertEqual(audit["samples"][0]["event_utc"], "2022-08-01T13:35:00+00:00")


if __name__ == "__main__":
    unittest.main()
