from __future__ import annotations

import shutil
import subprocess
import time
from pathlib import Path
from typing import Any, Mapping

import pandas as pd

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from foundation.mt5.runtime_artifacts import REPO_ROOT, sha256_file


def run_mt5_tester(
    terminal_path: Path,
    ini_path: Path,
    *,
    set_path: Path | None = None,
    tester_profile_set_path: Path | None = None,
    tester_profile_ini_path: Path | None = None,
    timeout_seconds: int = 300,
) -> dict[str, Any]:
    execution_ini_path = ini_path
    ini_copy_payload = None
    if tester_profile_ini_path is not None:
        io_path(tester_profile_ini_path.parent).mkdir(parents=True, exist_ok=True)
        shutil.copy2(io_path(ini_path), io_path(tester_profile_ini_path))
        execution_ini_path = tester_profile_ini_path
        ini_copy_payload = {
            "source": ini_path.as_posix(),
            "destination": tester_profile_ini_path.as_posix(),
            "sha256": sha256_file(tester_profile_ini_path),
        }

    command = [str(terminal_path), f"/config:{execution_ini_path.resolve()}"]
    if not path_exists(terminal_path):
        return {
            "status": "blocked",
            "command": command,
            "returncode": None,
            "blocker": "terminal_missing",
        }
    set_copy_payload = None
    if set_path is not None and tester_profile_set_path is not None:
        io_path(tester_profile_set_path.parent).mkdir(parents=True, exist_ok=True)
        shutil.copy2(io_path(set_path), io_path(tester_profile_set_path))
        set_copy_payload = {
            "source": set_path.as_posix(),
            "destination": tester_profile_set_path.as_posix(),
            "sha256": sha256_file(tester_profile_set_path),
        }
    proc = subprocess.run(command, cwd=REPO_ROOT, text=True, capture_output=True, timeout=timeout_seconds)
    return {
        "status": "completed" if proc.returncode == 0 else "blocked",
        "command": command,
        "returncode": proc.returncode,
        "stdout": proc.stdout[-2000:],
        "stderr": proc.stderr[-2000:],
        "tester_profile_set_copy": set_copy_payload,
        "tester_profile_ini_copy": ini_copy_payload,
    }


def validate_mt5_runtime_outputs(common_files_root: Path, attempt: Mapping[str, Any]) -> dict[str, Any]:
    telemetry_path = common_files_root / Path(str(attempt["common_telemetry_path"]))
    summary_path = common_files_root / Path(str(attempt["common_summary_path"]))
    payload: dict[str, Any] = {
        "telemetry_path": telemetry_path.as_posix(),
        "summary_path": summary_path.as_posix(),
        "telemetry_exists": path_exists(telemetry_path),
        "summary_exists": path_exists(summary_path),
        "status": "blocked",
    }
    if path_exists(telemetry_path):
        payload["telemetry_sha256"] = sha256_file(telemetry_path)
    if path_exists(summary_path):
        payload["summary_sha256"] = sha256_file(summary_path)
        try:
            summary = pd.read_csv(io_path(summary_path))
            if not summary.empty:
                last = summary.iloc[-1].to_dict()
                payload["last_summary"] = json_ready(last)
                deinit_reason = str(last.get("deinit_reason", ""))
                model_ok_count = int(last.get("model_ok_count", 0) or 0)
                feature_ready_count = int(last.get("feature_ready_count", 0) or 0)
                payload["status"] = (
                    "completed"
                    if deinit_reason != "init_failed" and model_ok_count > 0 and feature_ready_count > 0
                    else "blocked"
                )
        except Exception as exc:  # pragma: no cover - defensive MT5 handoff parsing
            payload["parse_error"] = str(exc)
    return payload


def wait_for_mt5_runtime_outputs(
    common_files_root: Path,
    attempt: Mapping[str, Any],
    *,
    timeout_seconds: int = 600,
    poll_seconds: float = 2.0,
) -> dict[str, Any]:
    deadline = time.monotonic() + timeout_seconds
    latest = validate_mt5_runtime_outputs(common_files_root, attempt)
    while time.monotonic() < deadline:
        latest = validate_mt5_runtime_outputs(common_files_root, attempt)
        if latest["status"] == "completed":
            latest["wait_status"] = "completed"
            return latest
        time.sleep(poll_seconds)
    latest = validate_mt5_runtime_outputs(common_files_root, attempt)
    latest["wait_status"] = "timeout"
    latest["wait_timeout_seconds"] = timeout_seconds
    return latest
