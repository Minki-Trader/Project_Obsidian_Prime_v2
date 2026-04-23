from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
AFTER_MT5_MODULE_PATH = REPO_ROOT / "foundation" / "parity" / "run_fpmarkets_v2_runtime_parity_after_mt5.py"
NATIVE_MODULE_PATH = REPO_ROOT / "foundation" / "parity" / "run_fpmarkets_v2_runtime_parity_native.py"


def load_module(module_name: str, module_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module spec from {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RuntimeParityOrchestratorStepTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.after_mt5_module = load_module("run_fpmarkets_v2_runtime_parity_after_mt5", AFTER_MT5_MODULE_PATH)
        cls.native_module = load_module("run_fpmarkets_v2_runtime_parity_native", NATIVE_MODULE_PATH)

    def test_after_mt5_run_step_reads_last_stdout_line_as_json(self) -> None:
        noisy_stdout = "log line before json\nanother diagnostic line\n{\"status\": \"ok\", \"step\": \"compare\"}\n"

        with patch.object(self.after_mt5_module.subprocess, "run") as mocked_run:
            mocked_run.return_value.stdout = noisy_stdout
            mocked_run.return_value.stderr = "warning: sample stderr line\n"

            summary = self.after_mt5_module.run_step(
                ["python", "dummy_script.py"],
                cwd=REPO_ROOT,
                step_id="compare",
            )

        self.assertEqual(summary["status"], "ok")
        self.assertEqual(summary["step"], "compare")

    def test_native_run_json_step_prefers_summary_json_file_when_provided(self) -> None:
        expected = {"status": "ok", "step": "after", "source": "summary_json"}

        def fake_run(cmd, **kwargs):
            summary_path = None
            if "--summary-json" in cmd:
                summary_path = Path(cmd[cmd.index("--summary-json") + 1])
            if summary_path is None:
                raise AssertionError("--summary-json argument was not passed")
            summary_path.parent.mkdir(parents=True, exist_ok=True)
            summary_path.write_text(json.dumps(expected), encoding="utf-8")

            class Result:
                stdout = "noise line\nnot json\n"
                stderr = ""

            return Result()

        with tempfile.TemporaryDirectory() as temp_dir:
            summary_path = Path(temp_dir) / "child_summary.json"
            with patch.object(self.native_module.subprocess, "run", side_effect=fake_run):
                summary = self.native_module.run_json_step(
                    ["python", "dummy_after.py"],
                    cwd=REPO_ROOT,
                    step_id="after",
                    summary_json_path=summary_path,
                )

        self.assertEqual(summary, expected)

    def test_after_mt5_run_step_decode_error_contains_step_and_diagnostics(self) -> None:
        with patch.object(self.after_mt5_module.subprocess, "run") as mocked_run:
            mocked_run.return_value.stdout = "diag line 1\nthis is not json\n"
            mocked_run.return_value.stderr = "trace stderr\n"

            with self.assertRaises(RuntimeError) as context:
                self.after_mt5_module.run_step(
                    ["python", "broken_child.py"],
                    cwd=REPO_ROOT,
                    step_id="import",
                )

        message = str(context.exception)
        self.assertIn("[import]", message)
        self.assertIn("stderr_tail", message)
        self.assertIn("stdout_tail", message)


if __name__ == "__main__":
    unittest.main()
