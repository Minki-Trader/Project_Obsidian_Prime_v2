from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "foundation" / "parity" / "stage06_runtime_parity.py"


def load_stage06_module():
    module_name = "stage06_runtime_parity"
    spec = importlib.util.spec_from_file_location(module_name, MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module spec from {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


class Stage06RuntimeParityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_stage06_module()

    def _ready_row(self, fixture_id: str = "regular") -> dict:
        features = {feature: float(index) for index, feature in enumerate(self.module.FEATURE_ORDER, start=1)}
        return {
            **self.module._base_identity(),
            "fixture_id": fixture_id,
            "fixture_type": "regular_cash_session",
            "row_ready": True,
            "features": features,
        }

    def test_compare_snapshot_rows_passes_identical_ready_fixture(self) -> None:
        row = self._ready_row()

        result = self.module.compare_snapshot_rows([row], [row.copy()], tolerance=1e-5)

        self.assertEqual(result["status"], "pass")
        self.assertEqual(result["compared_fixture_count"], 1)

    def test_compare_snapshot_rows_blocks_when_mt5_snapshot_missing(self) -> None:
        row = self._ready_row()

        result = self.module.compare_snapshot_rows([row], [], tolerance=1e-5)

        self.assertEqual(result["status"], "blocked")
        self.assertIn("mt5_snapshot_missing", result["failures"])

    def test_compare_snapshot_rows_detects_feature_tolerance_failure(self) -> None:
        python_row = self._ready_row()
        mt5_row = self._ready_row()
        mt5_row["features"]["log_return_1"] += 0.01

        result = self.module.compare_snapshot_rows([python_row], [mt5_row], tolerance=1e-5)

        self.assertEqual(result["status"], "fail")
        self.assertIn("regular:log_return_1_abs_diff_over_tolerance", result["failures"])

    def test_compare_snapshot_rows_accepts_mt5_named_feature_array(self) -> None:
        python_row = self._ready_row()
        mt5_row = self._ready_row()
        mt5_row["features"] = [
            {"index": index, "name": feature, "value": value}
            for index, (feature, value) in enumerate(python_row["features"].items())
        ]

        result = self.module.compare_snapshot_rows([python_row], [mt5_row], tolerance=1e-5)

        self.assertEqual(result["status"], "pass")

    def test_negative_fixture_requires_non_ready_mt5_row(self) -> None:
        python_row = self._ready_row("negative")
        python_row["fixture_type"] = "negative_required_missing_input"
        python_row["row_ready"] = False
        mt5_row = python_row.copy()
        mt5_row["row_ready"] = True

        result = self.module.compare_snapshot_rows([python_row], [mt5_row], tolerance=1e-5)

        self.assertEqual(result["status"], "fail")
        self.assertIn("negative:row_ready_mismatch", result["failures"])

    def test_event_time_payload_converts_broker_clock_key(self) -> None:
        payload = self.module._event_time_payload(pd.Timestamp("2022-09-01T16:40:00Z"))

        self.assertEqual(payload["timestamp_event_utc"], "2022-09-01T13:40:00+00:00")
        self.assertEqual(payload["timestamp_ny"], "2022-09-01T09:40:00-04:00")


if __name__ == "__main__":
    unittest.main()
