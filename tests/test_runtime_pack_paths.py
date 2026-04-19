from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "foundation" / "parity" / "runtime_pack_paths.py"
STAGE03_REQUEST = Path(
    "stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/"
    "mt5_snapshot_request_fpmarkets_v2_runtime_minimum_0001.json"
)
STAGE05_REQUEST = Path(
    "stages/05_exploration_kernel_freeze/02_runs/runtime_broader_pack_0002/"
    "mt5_snapshot_request_fpmarkets_v2_runtime_broader_0002.json"
)


def load_module():
    module_name = "runtime_pack_paths"
    spec = importlib.util.spec_from_file_location(module_name, MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module spec from {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


class RuntimePackPathResolverTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_module()

    def test_stage03_request_resolves_existing_default_paths(self) -> None:
        resolved = self.module.resolve_runtime_pack_paths(STAGE03_REQUEST)

        self.assertEqual(resolved.stage_name, "03_runtime_parity_closure")
        self.assertEqual(
            resolved.python_snapshot_path.as_posix(),
            "stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/python_snapshot_fpmarkets_v2_runtime_minimum_0001.json",
        )
        self.assertEqual(
            resolved.mt5_snapshot_path.as_posix(),
            "stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/mt5_feature_snapshot_audit_fpmarkets_v2_runtime_minimum_0001.jsonl",
        )
        self.assertEqual(
            resolved.comparison_json_path.as_posix(),
            "stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/runtime_parity_comparison_fpmarkets_v2_runtime_minimum_0001.json",
        )
        self.assertEqual(
            resolved.report_path.as_posix(),
            "stages/03_runtime_parity_closure/03_reviews/report_fpmarkets_v2_runtime_parity_0001.md",
        )
        self.assertIsNotNone(resolved.tester_ini_path)
        self.assertEqual(
            resolved.tester_ini_path.as_posix(),
            "stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/mt5_tester_runtime_parity_pack_0001.ini",
        )

    def test_stage05_request_resolves_broader_pack_paths(self) -> None:
        resolved = self.module.resolve_runtime_pack_paths(STAGE05_REQUEST)

        self.assertEqual(resolved.stage_name, "05_exploration_kernel_freeze")
        self.assertEqual(
            resolved.fixture_bindings_path.as_posix(),
            "stages/05_exploration_kernel_freeze/02_runs/runtime_broader_pack_0002/fixture_bindings_fpmarkets_v2_runtime_broader_0002.json",
        )
        self.assertEqual(
            resolved.python_snapshot_path.as_posix(),
            "stages/05_exploration_kernel_freeze/02_runs/runtime_broader_pack_0002/python_snapshot_fpmarkets_v2_runtime_broader_0002.json",
        )
        self.assertEqual(
            resolved.mt5_snapshot_path.as_posix(),
            "stages/05_exploration_kernel_freeze/02_runs/runtime_broader_pack_0002/mt5_feature_snapshot_audit_fpmarkets_v2_runtime_broader_0002.jsonl",
        )
        self.assertEqual(
            resolved.comparison_json_path.as_posix(),
            "stages/05_exploration_kernel_freeze/02_runs/runtime_broader_pack_0002/runtime_parity_comparison_fpmarkets_v2_runtime_broader_0002.json",
        )
        self.assertEqual(
            resolved.report_path.as_posix(),
            "stages/05_exploration_kernel_freeze/03_reviews/report_fpmarkets_v2_runtime_broader_parity_0002.md",
        )
        self.assertIsNotNone(resolved.tester_ini_path)
        self.assertEqual(
            resolved.tester_ini_path.as_posix(),
            "stages/05_exploration_kernel_freeze/02_runs/runtime_broader_pack_0002/mt5_tester_runtime_broader_pack_0002.ini",
        )
