from __future__ import annotations

import argparse
import importlib.util
import sys
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "foundation" / "parity" / "import_fpmarkets_v2_mt5_snapshot_audit.py"
def load_module():
    module_name = "import_fpmarkets_v2_mt5_snapshot_audit"
    spec = importlib.util.spec_from_file_location(module_name, MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module spec from {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


class ImportMt5SnapshotAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_module()

    def _write_request(self, root: Path, stage_name: str) -> Path:
        run_root = root / "stages" / stage_name / "02_runs" / "runtime_pack_test"
        run_root.mkdir(parents=True, exist_ok=True)
        request_path = run_root / "mt5_snapshot_request_test.json"
        request_path.write_text(
            json.dumps(
                {
                    "fixture_set_id": "fixture_test_0001",
                    "bundle_id": "bundle_test_0001",
                    "report_id": "report_test_0001",
                    "repo_import_path": f"stages/{stage_name}/02_runs/runtime_pack_test/mt5_snapshot.jsonl",
                    "common_files_output_path": "snapshot_test.jsonl",
                }
            ),
            encoding="utf-8",
        )
        return request_path

    def test_rejects_destination_path_escape(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            request_path = self._write_request(temp_root, "03_runtime_parity_closure")
            common_root = Path(temp_dir) / "common"
            common_root.mkdir(parents=True, exist_ok=True)
            source_path = common_root / "snapshot.jsonl"
            source_path.write_text('{"status":"ok"}\n', encoding="utf-8")
            args = argparse.Namespace(
                mt5_request=str(request_path),
                common_root=str(common_root),
                source_path=str(source_path),
                destination_path="../outside.jsonl",
            )

            with mock.patch.object(self.module, "parse_args", return_value=args):
                with self.assertRaises(RuntimeError) as context:
                    self.module.main()

        self.assertIn("escapes allowed root", str(context.exception))
