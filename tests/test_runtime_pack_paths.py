from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "foundation" / "parity" / "runtime_pack_paths.py"


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

    def _write_request(self, stage_name: str, repo_import_path: str) -> Path:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        run_root = Path(temp_dir.name) / "stages" / stage_name / "02_runs" / "runtime_pack_test"
        run_root.mkdir(parents=True, exist_ok=True)
        (run_root / "mt5_tester_runtime_pack_test.ini").write_text("[tester]\n", encoding="utf-8")
        request_path = run_root / "mt5_snapshot_request_test.json"
        request_path.write_text(
            json.dumps(
                {
                    "fixture_set_id": "fixture_test_0001",
                    "bundle_id": "bundle_test_0001",
                    "report_id": "report_test_0001",
                    "repo_import_path": repo_import_path,
                    "common_files_output_path": "snapshot_test.jsonl",
                }
            ),
            encoding="utf-8",
        )
        return request_path

    def test_resolves_paths_and_stage_name(self) -> None:
        stage_name = "03_runtime_parity_closure"
        request_path = self._write_request(
            stage_name,
            f"stages/{stage_name}/02_runs/runtime_pack_test/mt5_snapshot.jsonl",
        )

        resolved = self.module.resolve_runtime_pack_paths(request_path)

        self.assertEqual(resolved.stage_name, stage_name)
        self.assertEqual(
            resolved.mt5_snapshot_path.as_posix(),
            f"stages/{stage_name}/02_runs/runtime_pack_test/mt5_snapshot.jsonl",
        )
        self.assertIsNotNone(resolved.tester_ini_path)
        self.assertTrue(resolved.tester_ini_path.as_posix().endswith("mt5_tester_runtime_pack_test.ini"))

    def test_rejects_repo_import_path_escape(self) -> None:
        request_path = self._write_request("03_runtime_parity_closure", "../outside.jsonl")

        with self.assertRaises(RuntimeError) as context:
            self.module.resolve_runtime_pack_paths(request_path)

        self.assertIn("escapes allowed root", str(context.exception))
