from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


DEFAULT_TERMINAL_PATH = Path(r"C:\Program Files\MetaTrader 5\terminal64.exe")
DEFAULT_MT5_REQUEST = Path(
    "stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/"
    "mt5_snapshot_request_fpmarkets_v2_runtime_minimum_0001.json"
)
DEFAULT_TESTER_INI = Path(
    "stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/"
    "mt5_tester_runtime_parity_pack_0001.ini"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run the v2-native MT5 runtime parity audit tester, "
            "then import, compare, and render the Stage 03 parity artifacts."
        )
    )
    parser.add_argument(
        "--mt5-request",
        default=str(DEFAULT_MT5_REQUEST),
        help="Repo-relative path to the MT5 request JSON.",
    )
    parser.add_argument(
        "--tester-ini",
        default=str(DEFAULT_TESTER_INI),
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
        default="stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/python_snapshot_fpmarkets_v2_runtime_minimum_0001.json",
        help="Repo-relative Python snapshot path.",
    )
    parser.add_argument(
        "--mt5-snapshot",
        default="stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/mt5_feature_snapshot_audit_fpmarkets_v2_runtime_minimum_0001.jsonl",
        help="Repo-relative imported MT5 snapshot path.",
    )
    parser.add_argument(
        "--comparison-json",
        default="stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/runtime_parity_comparison_fpmarkets_v2_runtime_minimum_0001.json",
        help="Repo-relative comparison summary path.",
    )
    parser.add_argument(
        "--report-path",
        default="stages/03_runtime_parity_closure/03_reviews/report_fpmarkets_v2_runtime_parity_0001.md",
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


def list_running_terminal_rows() -> list[str]:
    result = subprocess.run(
        ["tasklist", "/FI", "IMAGENAME eq terminal64.exe", "/FO", "CSV", "/NH"],
        capture_output=True,
        text=True,
        check=True,
    )
    rows = []
    for raw_line in result.stdout.splitlines():
        line = raw_line.strip()
        if not line or "No tasks are running" in line:
            continue
        if "terminal64.exe" not in line.lower():
            continue
        rows.append(line)
    return rows


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


def run_json_step(args: list[str], cwd: Path) -> dict[str, Any]:
    result = subprocess.run(
        args,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=True,
    )
    stdout = result.stdout.strip()
    if not stdout:
        return {}
    return json.loads(stdout)


def main() -> int:
    args = parse_args()
    repo_root = Path.cwd()
    mt5_request_path = Path(args.mt5_request)
    tester_ini_path = Path(args.tester_ini)
    terminal_path = Path(args.terminal_path)

    if not terminal_path.exists():
        raise RuntimeError(f"terminal64.exe was not found: {terminal_path}")
    if not tester_ini_path.exists():
        raise RuntimeError(f"Tester ini was not found: {tester_ini_path}")

    mt5_request = load_json(mt5_request_path)
    common_root = Path(args.common_root) if args.common_root else default_common_root()
    common_output_path = common_root / mt5_request["common_files_output_path"]
    repo_snapshot_path = Path(args.mt5_snapshot)

    common_output_path.parent.mkdir(parents=True, exist_ok=True)
    repo_snapshot_path.parent.mkdir(parents=True, exist_ok=True)

    unlink_if_exists(common_output_path)
    unlink_if_exists(repo_snapshot_path)

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
            args.mt5_request,
            "--python-snapshot",
            args.python_snapshot,
            "--mt5-snapshot",
            args.mt5_snapshot,
            "--comparison-json",
            args.comparison_json,
            "--report-path",
            args.report_path,
            "--tolerance",
            str(args.tolerance),
        ]
        if args.common_root:
            runner_cmd.extend(["--common-root", args.common_root])
        if args.reviewed_on:
            runner_cmd.extend(["--reviewed-on", args.reviewed_on])
        after_summary = run_json_step(runner_cmd, cwd=repo_root)

    print(
        json.dumps(
            {
                "status": "ok",
                "tester_ini_path": str(tester_ini_path.resolve()),
                "terminal_path": str(terminal_path.resolve()),
                "common_output_path": str(common_output_path.resolve()),
                "repo_snapshot_path": str(repo_snapshot_path.resolve()),
                "force_close_terminal": args.force_close_terminal,
                "running_terminal_rows_before_launch": running_before,
                "after_summary": after_summary,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
