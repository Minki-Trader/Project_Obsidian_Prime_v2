from __future__ import annotations

import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


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

    def test_main_raises_when_source_file_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            missing_source = Path(tmpdir) / "missing.jsonl"
            destination = Path(tmpdir) / "imports" / "snapshot.jsonl"
            args = SimpleNamespace(
                mt5_request="ignored.json",
                common_root=None,
                source_path=str(missing_source),
                destination_path=str(destination),
            )
            resolved = SimpleNamespace(
                mt5_request={"common_files_output_path": "unused/from/request.jsonl"},
                mt5_snapshot_path=destination,
            )

            with (
                patch.object(self.module, "parse_args", return_value=args),
                patch.object(self.module, "resolve_runtime_pack_paths", return_value=resolved),
            ):
                with self.assertRaises(RuntimeError):
                    self.module.main()

    def test_main_propagates_destination_copy_validation_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            source = Path(tmpdir) / "source.jsonl"
            source.write_text('{"ok": true}\n', encoding="utf-8")
            destination = Path(tmpdir) / "invalid" / "snapshot.jsonl"
            args = SimpleNamespace(
                mt5_request="ignored.json",
                common_root=str(Path(tmpdir) / "common"),
                source_path=str(source),
                destination_path=str(destination),
            )
            resolved = SimpleNamespace(
                mt5_request={"common_files_output_path": "unused/from/request.jsonl"},
                mt5_snapshot_path=destination,
            )

            with (
                patch.object(self.module, "parse_args", return_value=args),
                patch.object(self.module, "resolve_runtime_pack_paths", return_value=resolved),
                patch.object(shutil, "copy2", side_effect=OSError("destination path validation failed")),
            ):
                with self.assertRaises(OSError):
                    self.module.main()

    def test_main_copies_source_and_emits_consistent_summary_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            source = Path(tmpdir) / "source.jsonl"
            payload = '{"fixture":"f1"}\n'
            source.write_text(payload, encoding="utf-8")
            destination = Path(tmpdir) / "imports" / "snapshot.jsonl"

            args = SimpleNamespace(
                mt5_request="ignored.json",
                common_root=str(Path(tmpdir) / "common"),
                source_path=str(source),
                destination_path=str(destination),
            )
            resolved = SimpleNamespace(
                mt5_request={"common_files_output_path": "unused/from/request.jsonl"},
                mt5_snapshot_path=destination,
            )

            with (
                patch.object(self.module, "parse_args", return_value=args),
                patch.object(self.module, "resolve_runtime_pack_paths", return_value=resolved),
                patch("builtins.print") as mock_print,
            ):
                result = self.module.main()

            self.assertEqual(result, 0)
            self.assertTrue(destination.exists())
            self.assertEqual(destination.read_text(encoding="utf-8"), payload)

            summary = json.loads(mock_print.call_args.args[0])
            self.assertEqual(summary["status"], "ok")
            self.assertEqual(summary["source_path"], str(source.resolve()))
            self.assertEqual(summary["destination_path"], str(destination.resolve()))
            self.assertEqual(summary["copied_bytes"], source.stat().st_size)


if __name__ == "__main__":
    unittest.main()
