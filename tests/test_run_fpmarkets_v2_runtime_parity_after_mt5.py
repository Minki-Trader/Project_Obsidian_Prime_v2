from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
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
            parsed = self.module.run_step(["dummy"], cwd=REPO_ROOT, step_id="dummy")

        self.assertEqual(parsed["status"], "ok")

    def test_run_step_prefers_summary_json_when_provided(self) -> None:
        expected = {"status": "ok", "step": "compare", "source": "summary_json"}

        def fake_run(cmd, **kwargs):
            summary_path = Path(cmd[cmd.index("--summary-json") + 1])
            summary_path.parent.mkdir(parents=True, exist_ok=True)
            summary_path.write_text(json.dumps(expected), encoding="utf-8")
            return subprocess.CompletedProcess(args=cmd, returncode=0, stdout="noise before json\n", stderr="")

        with tempfile.TemporaryDirectory() as temp_dir:
            summary_path = Path(temp_dir) / "compare_summary.json"
            with patch.object(self.module.subprocess, "run", side_effect=fake_run):
                parsed = self.module.run_step(
                    ["python", "dummy_script.py"],
                    cwd=REPO_ROOT,
                    step_id="compare",
                    summary_json_path=summary_path,
                )

        self.assertEqual(parsed, expected)

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
            summary_json=None,
        )
        step_summaries = [
            {"step": "import"},
            {"step": "compare"},
            {"step": "render"},
        ]

        with (
            patch.object(self.module, "parse_args", return_value=args),
            patch.object(self.module, "resolve_runtime_pack_paths", return_value=resolved),
            patch.object(self.module, "run_step", side_effect=step_summaries) as mock_run_step,
            patch("builtins.print") as mock_print,
        ):
            result = self.module.main()

        self.assertEqual(result, 0)
        self.assertEqual(mock_run_step.call_count, 3)

        import_call = mock_run_step.call_args_list[0]
        compare_call = mock_run_step.call_args_list[1]
        render_call = mock_run_step.call_args_list[2]

        import_cmd = import_call.args[0]
        compare_cmd = compare_call.args[0]
        render_cmd = render_call.args[0]

        self.assertEqual(import_call.kwargs["step_id"], "import")
        self.assertEqual(import_call.kwargs["summary_json_path"].name, "import_summary.json")
        self.assertEqual(import_cmd[1], "foundation/parity/import_fpmarkets_v2_mt5_snapshot_audit.py")
        self.assertIn("--common-root", import_cmd)
        self.assertIn("--source-path", import_cmd)

        self.assertEqual(compare_call.kwargs["step_id"], "compare")
        self.assertEqual(compare_call.kwargs["summary_json_path"].name, "compare_summary.json")
        self.assertEqual(compare_cmd[1], "foundation/parity/compare_fpmarkets_v2_runtime_parity.py")
        self.assertIn("--tolerance", compare_cmd)

        self.assertEqual(render_call.kwargs["step_id"], "render")
        self.assertEqual(render_call.kwargs["summary_json_path"].name, "render_summary.json")
        self.assertEqual(render_cmd[1], "foundation/parity/render_fpmarkets_v2_runtime_parity_report.py")
        self.assertIn("--reviewed-on", render_cmd)

        output = json.loads(mock_print.call_args.args[0])
        self.assertEqual(output["import_summary"]["step"], "import")
        self.assertEqual(output["compare_summary"]["step"], "compare")
        self.assertEqual(output["render_summary"]["step"], "render")

    def test_main_propagates_step_failure(self) -> None:
        resolved = SimpleNamespace(
            mt5_request_path=Path("stages/03_runtime_parity_closure/02_runs/runtime_pack/mt5_request.json"),
            stage_name="03_runtime_parity_closure",
            mt5_request={
                "common_files_output_path": "obsidian/common/runtime_snapshot.jsonl",
                "repo_import_path": "stages/03_runtime_parity_closure/02_runs/runtime_pack/mt5_snapshot.jsonl",
            },
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
            summary_json=None,
        )

        with (
            patch.object(self.module, "parse_args", return_value=args),
            patch.object(self.module, "resolve_runtime_pack_paths", return_value=resolved),
            patch.object(self.module, "run_step", side_effect=RuntimeError("step failed")),
        ):
            with self.assertRaises(RuntimeError):
                self.module.main()


if __name__ == "__main__":
    unittest.main()
