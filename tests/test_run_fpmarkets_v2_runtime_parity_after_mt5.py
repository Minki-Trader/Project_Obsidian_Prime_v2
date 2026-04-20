from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "foundation" / "parity" / "run_fpmarkets_v2_runtime_parity_after_mt5.py"


def load_module():
    module_name = "run_fpmarkets_v2_runtime_parity_after_mt5"
    spec = importlib.util.spec_from_file_location(module_name, MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module spec from {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


class RunRuntimeParityAfterMt5Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_module()

    def test_run_step_parses_clean_json_stdout(self) -> None:
        completed = subprocess.CompletedProcess(args=["dummy"], returncode=0, stdout='{"status":"ok"}', stderr="")
        with patch.object(self.module.subprocess, "run", return_value=completed):
            parsed = self.module.run_step(["dummy"], cwd=REPO_ROOT)

        self.assertEqual(parsed["status"], "ok")

    def test_run_step_rejects_noisy_stdout_for_json_parse(self) -> None:
        completed = subprocess.CompletedProcess(
            args=["dummy"],
            returncode=0,
            stdout='noise before payload\n{"status":"ok"}',
            stderr="",
        )
        with patch.object(self.module.subprocess, "run", return_value=completed):
            with self.assertRaises(json.JSONDecodeError):
                self.module.run_step(["dummy"], cwd=REPO_ROOT)

    def test_main_calls_steps_in_order_with_expected_arguments(self) -> None:
        resolved = SimpleNamespace(
            mt5_request_path=Path("stages/03_runtime_parity_closure/02_runs/runtime_pack/mt5_request.json"),
            stage_name="03_runtime_parity_closure",
            mt5_request={
                "common_files_output_path": "obsidian/common/runtime_snapshot.jsonl",
                "repo_import_path": "stages/03_runtime_parity_closure/02_runs/runtime_pack/mt5_snapshot.jsonl",
            },
            python_snapshot_path=Path("stages/03_runtime_parity_closure/02_runs/runtime_pack/python_snapshot.json"),
            mt5_snapshot_path=Path("stages/03_runtime_parity_closure/02_runs/runtime_pack/mt5_snapshot.jsonl"),
            comparison_json_path=Path("stages/03_runtime_parity_closure/02_runs/runtime_pack/comparison.json"),
            report_path=Path("stages/03_runtime_parity_closure/03_reviews/runtime_report.md"),
        )
        args = SimpleNamespace(
            mt5_request=str(resolved.mt5_request_path),
            python_snapshot=str(resolved.python_snapshot_path),
            comparison_json=str(resolved.comparison_json_path),
            mt5_snapshot=str(resolved.mt5_snapshot_path),
            report_path=str(resolved.report_path),
            common_root="C:/mt5/common",
            source_path="C:/mt5/common/obsidian/common/runtime_snapshot.jsonl",
            skip_import=False,
            tolerance=1e-5,
            reviewed_on="2026-04-20",
        )

        subprocess_results = [
            subprocess.CompletedProcess(args=["import"], returncode=0, stdout='{"step":"import"}', stderr=""),
            subprocess.CompletedProcess(args=["compare"], returncode=0, stdout='{"step":"compare"}', stderr=""),
            subprocess.CompletedProcess(args=["render"], returncode=0, stdout='{"step":"render"}', stderr=""),
        ]

        with (
            patch.object(self.module, "parse_args", return_value=args),
            patch.object(self.module, "resolve_runtime_pack_paths", return_value=resolved),
            patch.object(self.module.subprocess, "run", side_effect=subprocess_results) as mock_run,
            patch("builtins.print") as mock_print,
        ):
            result = self.module.main()

        self.assertEqual(result, 0)
        self.assertEqual(mock_run.call_count, 3)

        import_call = mock_run.call_args_list[0].args[0]
        compare_call = mock_run.call_args_list[1].args[0]
        render_call = mock_run.call_args_list[2].args[0]

        self.assertEqual(import_call[1], "foundation/parity/import_fpmarkets_v2_mt5_snapshot_audit.py")
        self.assertIn("--common-root", import_call)
        self.assertIn("--source-path", import_call)

        self.assertEqual(compare_call[1], "foundation/parity/compare_fpmarkets_v2_runtime_parity.py")
        self.assertIn("--tolerance", compare_call)

        self.assertEqual(render_call[1], "foundation/parity/render_fpmarkets_v2_runtime_parity_report.py")
        self.assertIn("--reviewed-on", render_call)

        output = json.loads(mock_print.call_args.args[0])
        self.assertEqual(output["import_summary"]["step"], "import")
        self.assertEqual(output["compare_summary"]["step"], "compare")
        self.assertEqual(output["render_summary"]["step"], "render")

    def test_main_propagates_step_failure(self) -> None:
        resolved = SimpleNamespace(
            mt5_request_path=Path("stages/03_runtime_parity_closure/02_runs/runtime_pack/mt5_request.json"),
            stage_name="03_runtime_parity_closure",
            mt5_request={"common_files_output_path": "obsidian/common/runtime_snapshot.jsonl", "repo_import_path": "x"},
            python_snapshot_path=Path("python_snapshot.json"),
            mt5_snapshot_path=Path("mt5_snapshot.jsonl"),
            comparison_json_path=Path("comparison.json"),
            report_path=Path("report.md"),
        )
        args = SimpleNamespace(
            mt5_request=str(resolved.mt5_request_path),
            python_snapshot=str(resolved.python_snapshot_path),
            comparison_json=str(resolved.comparison_json_path),
            mt5_snapshot=str(resolved.mt5_snapshot_path),
            report_path=str(resolved.report_path),
            common_root=None,
            source_path=None,
            skip_import=False,
            tolerance=1e-5,
            reviewed_on=None,
        )

        with (
            patch.object(self.module, "parse_args", return_value=args),
            patch.object(self.module, "resolve_runtime_pack_paths", return_value=resolved),
            patch.object(
                self.module.subprocess,
                "run",
                side_effect=subprocess.CalledProcessError(returncode=2, cmd=["import"]),
            ),
        ):
            with self.assertRaises(subprocess.CalledProcessError):
                self.module.main()


if __name__ == "__main__":
    unittest.main()
