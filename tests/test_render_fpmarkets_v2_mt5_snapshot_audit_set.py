from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "foundation" / "parity" / "render_fpmarkets_v2_mt5_snapshot_audit_set.py"


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

    def _base_mt5_request(self) -> dict[str, str]:
        return {
            "target_windows_utc": "",
            "common_files_output_path": "Common\\Files\\runtime_parity.jsonl",
            "window_start_utc": "2026-01-01T00:00:00Z",
            "dataset_id": "dataset_id",
            "fixture_set_id": "fixture_set_id",
            "bundle_id": "bundle_id",
            "target_runtime_id": "runtime_id",
            "report_id": "report_id",
            "parser_version": "parser_version",
            "parser_contract_version": "parser_contract_version",
            "feature_contract_version": "feature_contract_version",
            "runtime_contract_version": "runtime_contract_version",
            "feature_order_hash": "feature_order_hash",
        }

    def test_broader_request_splits_target_windows_across_multiple_inputs(self) -> None:
        mt5_request = self._base_mt5_request()
        mt5_request["target_windows_utc"] = ";".join(
            f"2026-01-01T00:{minute:02d}:00Z"
            for minute in range(33)
        )

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

    def test_render_set_raises_when_target_windows_need_more_than_four_chunks(self) -> None:
        mt5_request = self._base_mt5_request()
        forced_windows = [
            f"2026-01-01T00:{minute:02d}:00Z"
            for minute in range(45)
        ]
        mt5_request["target_windows_utc"] = ";".join(forced_windows)

        with self.assertRaisesRegex(RuntimeError, "maximum supported is 4"):
            self.module.render_set(mt5_request)
