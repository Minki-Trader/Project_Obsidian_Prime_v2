from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "foundation" / "parity" / "render_fpmarkets_v2_mt5_snapshot_audit_set.py"
BROADER_REQUEST_PATH = (
    REPO_ROOT
    / "stages"
    / "05_exploration_kernel_freeze"
    / "02_runs"
    / "runtime_broader_pack_0002"
    / "mt5_snapshot_request_fpmarkets_v2_runtime_broader_0002.json"
)


def load_module():
    module_name = "render_fpmarkets_v2_mt5_snapshot_audit_set"
    spec = importlib.util.spec_from_file_location(module_name, MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module spec from {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


class RenderMt5SnapshotAuditSetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_module()

    def test_broader_request_splits_target_windows_across_multiple_inputs(self) -> None:
        mt5_request = self.module.load_json(BROADER_REQUEST_PATH)

        rendered = self.module.render_set(mt5_request)

        self.assertIn("InpTargetWindowsUtc=", rendered)
        self.assertIn("InpTargetWindowsUtcPart2=", rendered)
        self.assertIn("InpTargetWindowsUtcPart3=", rendered)
        self.assertIn("InpTargetWindowsUtcPart4=", rendered)

        chunk_lines = [
            line.split("=", 1)[1]
            for line in rendered.splitlines()
            if line.startswith("InpTargetWindowsUtc")
        ]
        non_empty_chunks = [chunk for chunk in chunk_lines if chunk]
        self.assertGreaterEqual(len(non_empty_chunks), 3)
        for chunk in non_empty_chunks:
            self.assertLessEqual(len(chunk), 230)
