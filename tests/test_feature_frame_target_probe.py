from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "foundation" / "collectors" / "feature_frame_target_probe.py"
RAW_ROOT = REPO_ROOT / "data" / "raw" / "mt5_bars" / "m5"


def load_probe_module():
    module_name = "feature_frame_target_probe"
    spec = importlib.util.spec_from_file_location(module_name, MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module spec from {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


class FeatureFrameTargetProbeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_probe_module()
        cls.payload = cls.module.analyze_feature_frame_target(RAW_ROOT)

    def test_selected_target_prefers_practical_full_cash_days(self) -> None:
        selected = self.payload["selected_target"]
        self.assertEqual(selected["target_id"], "practical_start_full_cash_day_valid_rows_only")
        self.assertEqual(selected["start_utc"], "2022-09-01T00:00:00+00:00")
        self.assertEqual(selected["day_scope"], "full_cash_session_days_only")
        self.assertEqual(selected["session_scope"], "cash_open_rows_only")
        self.assertEqual(selected["row_scope"], "valid_row_only")

    def test_selected_target_counts_are_stable(self) -> None:
        selected = self.payload["selected_target"]
        self.assertEqual(selected["rows"], 54439)
        self.assertEqual(selected["ny_day_count"], 887)
        self.assertEqual(selected["full_cash_day_count"], 890)
        self.assertEqual(selected["excluded_partial_cash_days"], 40)
        self.assertEqual(selected["excluded_partial_day_valid_rows"], 252)

    def test_candidate_order_preserves_broader_scopes_as_non_dead(self) -> None:
        candidate_ids = [candidate["target_id"] for candidate in self.payload["candidate_targets"]]
        self.assertEqual(
            candidate_ids,
            [
                "full_window_valid_rows_only",
                "practical_start_valid_rows_only",
                "practical_start_cash_open_valid_rows_only",
                "practical_start_full_cash_day_valid_rows_only",
            ],
        )
        rows_by_id = {candidate["target_id"]: candidate["rows"] for candidate in self.payload["candidate_targets"]}
        self.assertGreater(rows_by_id["practical_start_valid_rows_only"], rows_by_id["practical_start_cash_open_valid_rows_only"])
        self.assertGreater(
            rows_by_id["practical_start_cash_open_valid_rows_only"],
            rows_by_id["practical_start_full_cash_day_valid_rows_only"],
        )

    def test_probe_marks_external_verification_not_applicable(self) -> None:
        self.assertEqual(self.payload["external_verification_status"], "not_applicable")
        self.assertEqual(self.payload["judgment_class"], "positive")
        self.assertEqual(self.payload["parity_level"], "P1_dataset_feature_aligned")
