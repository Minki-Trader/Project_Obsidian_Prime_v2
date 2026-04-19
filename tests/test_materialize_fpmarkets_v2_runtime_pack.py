from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "foundation" / "parity" / "materialize_fpmarkets_v2_runtime_pack.py"
RAW_ROOT = REPO_ROOT / "data" / "raw" / "mt5_bars" / "m5"
BROADER_MANIFEST_PATH = (
    REPO_ROOT
    / "stages"
    / "05_exploration_kernel_freeze"
    / "01_inputs"
    / "second_bound_runtime_broader_fixture_manifest_0002.json"
)
STAGE03_BINDINGS_PATH = (
    REPO_ROOT
    / "stages"
    / "03_runtime_parity_closure"
    / "02_runs"
    / "runtime_parity_pack_0001"
    / "fixture_bindings_fpmarkets_v2_runtime_minimum_0001.json"
)


def load_materialize_module():
    module_name = "materialize_fpmarkets_v2_runtime_pack"
    spec = importlib.util.spec_from_file_location(module_name, MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module spec from {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


class RuntimePackMaterializationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_materialize_module()

    def test_current_broader_manifest_meets_frozen_stage05_constraints(self) -> None:
        manifest = json.loads(BROADER_MANIFEST_PATH.read_text(encoding="utf-8"))
        summary = self.module.validate_broader_manifest(manifest)

        self.assertEqual(summary["fixture_count"], 24)
        self.assertEqual(summary["ready_count"], 16)
        self.assertEqual(summary["negative_count"], 8)
        self.assertGreaterEqual(summary["distinct_month_count_ny"], 6)
        self.assertGreaterEqual(summary["distinct_weekday_count_ny"], 3)
        self.assertEqual(summary["utc_offsets_present"], [-300, -240])
        self.assertEqual(summary["bucket_counts"]["cash_close_boundary_1555"], 2)
        self.assertEqual(summary["bucket_counts"]["cash_close_boundary_1600"], 2)
        self.assertEqual(summary["bucket_counts"]["dst_sensitive_utc4"], 2)
        self.assertEqual(summary["bucket_counts"]["dst_sensitive_utc5"], 2)
        self.assertEqual(summary["bucket_counts"]["negative_off_hours_pre_open"], 2)
        self.assertEqual(summary["bucket_counts"]["negative_off_hours_post_close"], 2)

    def test_minimum_profile_shared_builder_matches_existing_stage03_fixture_timestamps(self) -> None:
        expected_bindings = json.loads(STAGE03_BINDINGS_PATH.read_text(encoding="utf-8"))
        expected_timestamps = {
            fixture_id: payload["timestamp_utc"]
            for fixture_id, payload in expected_bindings["fixtures"].items()
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            output_root = Path(temp_dir)
            self.module.materialize_runtime_pack(
                profile_name="minimum_0001",
                raw_root=RAW_ROOT,
                output_root=output_root,
            )
            actual_bindings = json.loads(
                (output_root / "fixture_bindings_fpmarkets_v2_runtime_minimum_0001.json").read_text(
                    encoding="utf-8"
                )
            )

        actual_timestamps = {
            fixture_id: payload["timestamp_utc"]
            for fixture_id, payload in actual_bindings["fixtures"].items()
        }
        self.assertEqual(actual_timestamps, expected_timestamps)
