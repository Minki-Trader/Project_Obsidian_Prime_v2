from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from foundation.parity.runtime_pack_paths import DEFAULT_MT5_REQUEST, resolve_runtime_pack_paths


DEFAULT_TERMINAL_PATH = Path(r"C:\Program Files\MetaTrader 5\terminal64.exe")
CONFLICTING_GAME_PROCESS_NAMES = (
    "League of Legends.exe",
    "LeagueClient.exe",
    "LeagueClientUx.exe",
    "LeagueClientUxRender.exe",
    "RiotClientServices.exe",
    "RiotClientUx.exe",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run the v2-native MT5 runtime parity audit tester, "
            "then import, compare, and render the runtime parity artifacts for the resolved pack."
        )
    )
    parser.add_argument(
        "--mt5-request",
        default=str(DEFAULT_MT5_REQUEST),
        help="Repo-relative path to the MT5 request JSON.",
    )
    parser.add_argument(
        "--tester-ini",
        default=None,
        help="Repo-relative path to the MT5 Strategy Tester ini.",
    )
    parser.add_argument(
        "--terminal-path",
        default=str(DEFAULT_TERMINAL_PATH),
        help="Path to terminal64.exe.",
    )
    parser.add_argument(
        "--common-root",
        default=None,
        help="Optional override for the MT5 Common Files root.",
    )
    parser.add_argument(
        "--python-snapshot",
        default=None,
        help="Repo-relative Python snapshot path.",
    )
    parser.add_argument(
        "--mt5-snapshot",
        default=None,
        help="Repo-relative imported MT5 snapshot path.",
    )
    parser.add_argument(
        "--comparison-json",
        default=None,
        help="Repo-relative comparison summary path.",
    )
    parser.add_argument(
        "--report-path",
        default=None,
        help="Repo-relative rendered report path.",
    )
    parser.add_argument(
        "--reviewed-on",
        default=None,
        help="Optional explicit review date for the rendered report.",
    )
    parser.add_argument(
        "--tolerance",
        type=float,
        default=1e-5,
        help="Absolute tolerance for ready-row feature comparisons.",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=900,
        help="Maximum tester runtime before giving up.",
    )
    parser.add_argument(
        "--wait-seconds",
        type=int,
        default=120,
        help="Maximum time to wait for the Common Files JSONL after the tester exits.",
    )
    parser.add_argument(
        "--force-close-terminal",
        action="store_true",
        help="Force-close running terminal64.exe before the tester launch.",
    )
    parser.add_argument(
        "--allow-conflicting-games",
        action="store_true",
        help="Allow the MT5 tester launch even when League or Riot game processes are already running.",
    )
    parser.add_argument(
        "--skip-after",
        action="store_true",
        help="Run the MT5 tester only; skip the import/compare/render chain.",
    )
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def default_common_root() -> Path:
    appdata = os.environ.get("APPDATA")
    if not appdata:
        raise RuntimeError("APPDATA is not available; pass --common-root explicitly.")
    return Path(appdata) / "MetaQuotes" / "Terminal" / "Common" / "Files"


def list_running_process_rows(image_name: str) -> list[str]:
    result = subprocess.run(
        ["tasklist", "/FI", f"IMAGENAME eq {image_name}", "/FO", "CSV", "/NH"],
        capture_output=True,
        text=True,
        check=True,
    )
    rows = []
    for raw_line in result.stdout.splitlines():
        line = raw_line.strip()
        if not line or "No tasks are running" in line:
            continue
        if image_name.lower() not in line.lower():
            continue
        rows.append(line)
    return rows


def list_running_terminal_rows() -> list[str]:
    return list_running_process_rows("terminal64.exe")


def list_running_conflicting_game_rows() -> list[str]:
    rows: list[str] = []
    for image_name in CONFLICTING_GAME_PROCESS_NAMES:
        rows.extend(list_running_process_rows(image_name))
    return rows


def ensure_no_conflicting_games(allow_conflicting_games: bool) -> list[str]:
    running = list_running_conflicting_game_rows()
    if not running:
        return []
    if allow_conflicting_games:
        return running
    running_text = "\n".join(running)
    raise RuntimeError(
        "League or Riot game processes are already running. "
        "Close the game client first or rerun with --allow-conflicting-games.\n"
        f"running_process_rows:\n{running_text}"
    )


def ensure_terminal_ready(force_close_terminal: bool) -> list[str]:
    running = list_running_terminal_rows()
    if not running:
        return []
    if not force_close_terminal:
        raise RuntimeError(
            "terminal64.exe is already running. Close it first or rerun with --force-close-terminal."
        )
    subprocess.run(["taskkill", "/F", "/IM", "terminal64.exe"], check=True, capture_output=True, text=True)
    time.sleep(1.0)
    return running


def unlink_if_exists(path: Path) -> None:
    if path.exists():
        path.unlink()


def wait_for_file(path: Path, timeout_seconds: int) -> None:
    deadline = time.time() + timeout_seconds
    last_size = -1
    stable_hits = 0
    while time.time() < deadline:
        if path.exists():
            size = path.stat().st_size
            if size > 0:
                if size == last_size:
                    stable_hits += 1
                else:
                    stable_hits = 0
                    last_size = size
                if stable_hits >= 2:
                    return
        time.sleep(1.0)
    raise RuntimeError(f"Timed out waiting for MT5 snapshot output: {path}")


def _tail_lines(text: str, count: int = 20) -> str:
    lines = [line for line in text.splitlines() if line.strip()]
    if not lines:
        return "<empty>"
    return "\n".join(lines[-count:])


def _load_step_summary_from_stdout(*, stdout: str, stderr: str, step_id: str) -> dict[str, Any]:
    lines = [line.strip() for line in stdout.splitlines() if line.strip()]
    if not lines:
        raise RuntimeError(
            f"[{step_id}] Missing structured summary on stdout. "
            f"stderr_tail:\n{_tail_lines(stderr)}\nstdout_tail:\n{_tail_lines(stdout)}"
        )
    try:
        return json.loads(lines[-1])
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"[{step_id}] Failed to decode structured summary JSON from stdout last line: {exc}. "
            f"stderr_tail:\n{_tail_lines(stderr)}\nstdout_tail:\n{_tail_lines(stdout)}"
        ) from exc


def run_json_step(
    args: list[str],
    cwd: Path,
    *,
    step_id: str,
    summary_json_path: Path | None = None,
) -> dict[str, Any]:
    cmd = list(args)
    if summary_json_path is not None:
        cmd.extend(["--summary-json", str(summary_json_path)])

    result = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=True,
    )
    if summary_json_path is not None:
        if not summary_json_path.exists():
            raise RuntimeError(
                f"[{step_id}] --summary-json output was not created: {summary_json_path}. "
                f"stderr_tail:\n{_tail_lines(result.stderr)}\nstdout_tail:\n{_tail_lines(result.stdout)}"
            )
        return load_json(summary_json_path)
    return _load_step_summary_from_stdout(stdout=result.stdout, stderr=result.stderr, step_id=step_id)


def main() -> int:
    args = parse_args()
    repo_root = Path.cwd()
    resolved_paths = resolve_runtime_pack_paths(
        Path(args.mt5_request),
        python_snapshot_path=Path(args.python_snapshot) if args.python_snapshot else None,
        mt5_snapshot_path=Path(args.mt5_snapshot) if args.mt5_snapshot else None,
        comparison_json_path=Path(args.comparison_json) if args.comparison_json else None,
        report_path=Path(args.report_path) if args.report_path else None,
        tester_ini_path=Path(args.tester_ini) if args.tester_ini else None,
    )
    mt5_request_path = resolved_paths.mt5_request_path
    tester_ini_path = resolved_paths.tester_ini_path
    terminal_path = Path(args.terminal_path)

    if not terminal_path.exists():
        raise RuntimeError(f"terminal64.exe was not found: {terminal_path}")
    if tester_ini_path is None:
        raise RuntimeError(
            "Could not resolve a single tester ini from the MT5 request pack. Pass --tester-ini explicitly."
        )
    if not tester_ini_path.exists():
        raise RuntimeError(f"Tester ini was not found: {tester_ini_path}")

    mt5_request = resolved_paths.mt5_request
    common_root = Path(args.common_root) if args.common_root else default_common_root()
    common_output_path = common_root / mt5_request["common_files_output_path"]
    repo_snapshot_path = resolved_paths.mt5_snapshot_path

    common_output_path.parent.mkdir(parents=True, exist_ok=True)
    repo_snapshot_path.parent.mkdir(parents=True, exist_ok=True)

    unlink_if_exists(common_output_path)
    unlink_if_exists(repo_snapshot_path)

    running_games_before = ensure_no_conflicting_games(args.allow_conflicting_games)
    running_before = ensure_terminal_ready(args.force_close_terminal)

    subprocess.run(
        [str(terminal_path), f"/config:{tester_ini_path.resolve()}"],
        cwd=repo_root,
        check=True,
        timeout=args.timeout_seconds,
    )
    wait_for_file(common_output_path, args.wait_seconds)

    after_summary: dict[str, Any] | None = None
    if not args.skip_after:
        runner_cmd = [
            sys.executable,
            "foundation/parity/run_fpmarkets_v2_runtime_parity_after_mt5.py",
            "--mt5-request",
            str(mt5_request_path),
            "--python-snapshot",
            str(resolved_paths.python_snapshot_path),
            "--mt5-snapshot",
            str(resolved_paths.mt5_snapshot_path),
            "--comparison-json",
            str(resolved_paths.comparison_json_path),
            "--report-path",
            str(resolved_paths.report_path),
            "--tolerance",
            str(args.tolerance),
        ]
        if args.common_root:
            runner_cmd.extend(["--common-root", args.common_root])
        if args.reviewed_on:
            runner_cmd.extend(["--reviewed-on", args.reviewed_on])
        with tempfile.TemporaryDirectory(prefix="runtime_parity_native_after_") as temp_dir:
            after_summary = run_json_step(
                runner_cmd,
                cwd=repo_root,
                step_id="after",
                summary_json_path=Path(temp_dir) / "after_summary.json",
            )

    print(
        json.dumps(
            {
                "status": "ok",
                "stage_name": resolved_paths.stage_name,
                "tester_ini_path": str(tester_ini_path.resolve()),
                "terminal_path": str(terminal_path.resolve()),
                "common_output_path": str(common_output_path.resolve()),
                "repo_snapshot_path": str(repo_snapshot_path.resolve()),
                "force_close_terminal": args.force_close_terminal,
                "allow_conflicting_games": args.allow_conflicting_games,
                "running_conflicting_game_rows_before_launch": running_games_before,
                "running_terminal_rows_before_launch": running_before,
                "after_summary": after_summary,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
