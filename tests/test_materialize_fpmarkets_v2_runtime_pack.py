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
HELPER_MANIFEST_PATH = (
    REPO_ROOT
    / "stages"
    / "05_exploration_kernel_freeze"
    / "01_inputs"
    / "first_bound_runtime_helper_fixture_manifest_0001.json"
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

    def test_helper_manifest_meets_frozen_stage05_constraints(self) -> None:
        manifest = json.loads(HELPER_MANIFEST_PATH.read_text(encoding="utf-8"))
        summary = self.module.validate_helper_manifest(manifest)

        self.assertEqual(summary["fixture_count"], 8)
        self.assertEqual(summary["ready_count"], 6)
        self.assertEqual(summary["negative_count"], 2)
        self.assertGreaterEqual(summary["distinct_month_count_ny"], 6)
        self.assertGreaterEqual(summary["distinct_weekday_count_ny"], 3)
        self.assertEqual(summary["utc_offsets_present"], [-300, -240])
        self.assertEqual(summary["bucket_counts"]["regular_cash_session"], 1)
        self.assertEqual(summary["bucket_counts"]["cash_close_boundary_1555"], 1)
        self.assertEqual(summary["bucket_counts"]["cash_close_boundary_1600"], 1)
        self.assertEqual(summary["bucket_counts"]["dst_sensitive_utc4"], 1)
        self.assertEqual(summary["bucket_counts"]["dst_sensitive_utc5"], 1)
        self.assertEqual(summary["bucket_counts"]["full_external_alignment"], 1)
        self.assertEqual(summary["bucket_counts"]["negative_cash_open_missing_equities"], 1)
        self.assertEqual(summary["bucket_counts"]["negative_off_hours_post_close"], 1)

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

    def test_helper_profile_shared_builder_matches_helper_manifest_timestamps(self) -> None:
        expected_manifest = json.loads(HELPER_MANIFEST_PATH.read_text(encoding="utf-8"))
        expected_timestamps = {
            fixture["fixture_id"]: fixture["timestamp_utc"] for fixture in expected_manifest["fixtures"]
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            output_root = Path(temp_dir)
            self.module.materialize_runtime_pack(
                profile_name="helper_0001",
                raw_root=RAW_ROOT,
                output_root=output_root,
                selection_manifest_path=HELPER_MANIFEST_PATH,
                inventory_path=output_root / "helper_inventory.md",
            )
            actual_bindings = json.loads(
                (output_root / "fixture_bindings_fpmarkets_v2_runtime_helper_0001.json").read_text(
                    encoding="utf-8"
                )
            )

        actual_timestamps = {
            fixture_id: payload["timestamp_utc"]
            for fixture_id, payload in actual_bindings["fixtures"].items()
        }
        self.assertEqual(actual_timestamps, expected_timestamps)

    def test_broader_0003_profile_excludes_active_broader_0002_timestamps(self) -> None:
        source_manifest = json.loads(BROADER_MANIFEST_PATH.read_text(encoding="utf-8"))
        source_timestamps = {
            fixture["timestamp_utc"]
            for fixture in source_manifest["fixtures"]
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            output_root = Path(temp_dir) / "runtime_broader_pack_0003"
            manifest_path = Path(temp_dir) / "third_bound_runtime_broader_fixture_manifest_0003.json"
            inventory_path = Path(temp_dir) / "third_bound_runtime_broader_fixture_inventory.md"
            summary = self.module.materialize_runtime_pack(
                profile_name="broader_0003",
                raw_root=RAW_ROOT,
                output_root=output_root,
                selection_manifest_path=manifest_path,
                inventory_path=inventory_path,
                force_reselect=True,
            )
            actual_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

        actual_timestamps = {
            fixture["timestamp_utc"]
            for fixture in actual_manifest["fixtures"]
        }
        self.assertFalse(actual_timestamps.intersection(source_timestamps))
        self.assertEqual(
            actual_manifest["excluded_source_fixture_set_id"],
            "fixture_fpmarkets_v2_runtime_broader_0002",
        )
        self.assertEqual(
            actual_manifest["excluded_source_selection_manifest_ref"],
            "stages/05_exploration_kernel_freeze/01_inputs/second_bound_runtime_broader_fixture_manifest_0002.json",
        )
        self.assertIn("excluded_source_selection_manifest_path", summary["generated_paths"])
