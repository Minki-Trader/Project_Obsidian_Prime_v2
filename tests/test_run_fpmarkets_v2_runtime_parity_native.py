from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "foundation" / "parity" / "run_fpmarkets_v2_runtime_parity_native.py"


def load_module():
    module_name = "run_fpmarkets_v2_runtime_parity_native"
    spec = importlib.util.spec_from_file_location(module_name, MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module spec from {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


class RunRuntimeParityNativeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_module()

    def test_ensure_no_conflicting_games_raises_without_allow_flag(self) -> None:
        with patch.object(
            self.module,
            "list_running_conflicting_game_rows",
            return_value=['"League of Legends.exe","321"'],
        ):
            with self.assertRaises(RuntimeError):
                self.module.ensure_no_conflicting_games(allow_conflicting_games=False)

    def test_ensure_no_conflicting_games_returns_rows_when_allowed(self) -> None:
        with patch.object(
            self.module,
            "list_running_conflicting_game_rows",
            return_value=['"LeagueClientUx.exe","654"'],
        ):
            rows = self.module.ensure_no_conflicting_games(allow_conflicting_games=True)

        self.assertEqual(rows, ['"LeagueClientUx.exe","654"'])

    def test_ensure_terminal_ready_raises_without_force_close(self) -> None:
        with patch.object(self.module, "list_running_terminal_rows", return_value=['"terminal64.exe","123"']):
            with self.assertRaises(RuntimeError):
                self.module.ensure_terminal_ready(force_close_terminal=False)

    def test_ensure_terminal_ready_kills_existing_terminal_when_forced(self) -> None:
        with (
            patch.object(self.module, "list_running_terminal_rows", return_value=['"terminal64.exe","123"']),
            patch.object(self.module.subprocess, "run") as mock_run,
            patch.object(self.module.time, "sleep") as mock_sleep,
        ):
            rows = self.module.ensure_terminal_ready(force_close_terminal=True)

        self.assertEqual(rows, ['"terminal64.exe","123"'])
        self.assertEqual(mock_run.call_args.args[0], ["taskkill", "/F", "/IM", "terminal64.exe"])
        mock_sleep.assert_called_once_with(1.0)

    def test_wait_for_file_returns_after_stable_nonzero_size(self) -> None:
        fake_path = MagicMock()
        fake_path.exists.side_effect = [False, True, True, True]
        stat_result = SimpleNamespace(st_size=17)
        fake_path.stat.side_effect = [stat_result, stat_result, stat_result]

        with (
            patch.object(self.module.time, "time", side_effect=[0.0, 0.0, 0.1, 0.2, 0.3, 0.4]),
            patch.object(self.module.time, "sleep"),
        ):
            self.module.wait_for_file(fake_path, timeout_seconds=5)

    def test_wait_for_file_raises_on_timeout(self) -> None:
        fake_path = MagicMock()
        fake_path.exists.return_value = False

        with (
            patch.object(self.module.time, "time", side_effect=[0.0, 0.5, 1.1]),
            patch.object(self.module.time, "sleep"),
        ):
            with self.assertRaises(RuntimeError):
                self.module.wait_for_file(fake_path, timeout_seconds=1)

    def test_main_skip_after_omits_after_chain_but_runs_tester(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            terminal_path = tmp / "terminal64.exe"
            tester_ini = tmp / "mt5_tester_runtime.ini"
            terminal_path.write_text("exe", encoding="utf-8")
            tester_ini.write_text("[Tester]", encoding="utf-8")

            resolved = SimpleNamespace(
                mt5_request_path=tmp / "mt5_request.json",
                stage_name="03_runtime_parity_closure",
                mt5_request={
                    "common_files_output_path": "obsidian/common/runtime_snapshot.jsonl",
                },
                tester_ini_path=tester_ini,
                python_snapshot_path=tmp / "python_snapshot.json",
                mt5_snapshot_path=tmp / "mt5_snapshot.jsonl",
                comparison_json_path=tmp / "comparison.json",
                report_path=tmp / "report.md",
            )
            args = SimpleNamespace(
                mt5_request=str(resolved.mt5_request_path),
                tester_ini=str(tester_ini),
                terminal_path=str(terminal_path),
                common_root=str(tmp / "common"),
                python_snapshot=str(resolved.python_snapshot_path),
                mt5_snapshot=str(resolved.mt5_snapshot_path),
                comparison_json=str(resolved.comparison_json_path),
                report_path=str(resolved.report_path),
                reviewed_on=None,
                tolerance=1e-5,
                timeout_seconds=45,
                wait_seconds=20,
                force_close_terminal=False,
                allow_conflicting_games=False,
                skip_after=True,
            )

            with (
                patch.object(self.module, "parse_args", return_value=args),
                patch.object(self.module, "resolve_runtime_pack_paths", return_value=resolved),
                patch.object(self.module, "ensure_no_conflicting_games", return_value=[]),
                patch.object(self.module, "ensure_terminal_ready", return_value=[]),
                patch.object(self.module, "wait_for_file") as mock_wait,
                patch.object(self.module, "run_json_step") as mock_after,
                patch.object(self.module.subprocess, "run") as mock_run,
                patch("builtins.print") as mock_print,
            ):
                rc = self.module.main()

        self.assertEqual(rc, 0)
        self.assertEqual(mock_run.call_count, 1)
        launch_cmd = mock_run.call_args.args[0]
        self.assertEqual(launch_cmd[0], str(terminal_path))
        self.assertIn(f"/config:{tester_ini.resolve()}", launch_cmd)
        mock_wait.assert_called_once()
        mock_after.assert_not_called()

        summary = json.loads(mock_print.call_args.args[0])
        self.assertEqual(summary["status"], "ok")
        self.assertIsNone(summary["after_summary"])
        self.assertEqual(summary["running_conflicting_game_rows_before_launch"], [])
        self.assertEqual(summary["running_terminal_rows_before_launch"], [])


if __name__ == "__main__":
    unittest.main()
