from __future__ import annotations

import importlib.util
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "foundation" / "pipelines" / "materialize_feature_frame_freeze.py"
RAW_ROOT = REPO_ROOT / "data" / "raw" / "mt5_bars" / "m5"
RUN_SLOW_INTEGRATION_TESTS = os.environ.get("OBSIDIAN_RUN_SLOW_TESTS") == "1"
SLOW_INTEGRATION_SKIP_REASON = "set OBSIDIAN_RUN_SLOW_TESTS=1 to run raw-data integration tests"


def load_freeze_module():
    module_name = "materialize_feature_frame_freeze"
    spec = importlib.util.spec_from_file_location(module_name, MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module spec from {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


@unittest.skipUnless(RUN_SLOW_INTEGRATION_TESTS, SLOW_INTEGRATION_SKIP_REASON)
class MaterializeFeatureFrameFreezeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_freeze_module()
        cls.selection = cls.module.FreezeSelectionSpec(
            target_id="practical_start_full_cash_day_valid_rows_only",
            start_utc=cls.module.parse_utc_timestamp("2022-09-01T00:00:00Z"),
            row_scope="valid_row_only",
            session_scope="cash_open_rows_only",
            day_scope="full_cash_session_days_only",
        )

    def test_select_freeze_rows_matches_stage02_target_counts(self) -> None:
        frame, counts = self.module.build_feature_frame(RAW_ROOT)
        payload = self.module.select_freeze_rows(frame, counts, self.selection)["selection_summary"]

        self.assertEqual(payload["window_raw_rows"], 255001)
        self.assertEqual(payload["window_valid_rows"], 55408)
        self.assertEqual(payload["selected_rows"], 54439)
        self.assertEqual(payload["candidate_cash_open_valid_rows"], 54691)
        self.assertEqual(payload["eligible_full_cash_day_count"], 890)
        self.assertEqual(payload["selected_valid_row_ny_days"], 887)
        self.assertEqual(payload["excluded_partial_cash_days"], 40)
        self.assertEqual(payload["excluded_partial_day_valid_rows"], 252)

    def test_materialize_selected_freeze_writes_contract_summary(self) -> None:
        dataset_id = "dataset_fpmarkets_v2_us100_m5_20220901_20260413_cashopen_fullcash_valid_freeze01"
        with tempfile.TemporaryDirectory() as temp_dir:
            payload = self.module.materialize_selected_freeze(
                raw_root=RAW_ROOT,
                output_root=Path(temp_dir),
                dataset_id=dataset_id,
                selection=self.selection,
            )
            summary_path = Path(payload["artifacts"]["summary_path"])
            summary = json.loads(summary_path.read_text(encoding="utf-8"))

            self.assertEqual(summary["dataset_id"], dataset_id)
            self.assertEqual(summary["window_start"], "2022-09-01T00:00:00+00:00")
            self.assertEqual(summary["selected_rows"], 54439)
            self.assertEqual(summary["valid_rows"], 55408)
            self.assertEqual(summary["selection_session_scope"], "cash_open_rows_only")
            self.assertEqual(summary["selection_day_scope"], "full_cash_session_days_only")
            self.assertEqual(summary["feature_order_hash"], self.module.feature_order_hash())
