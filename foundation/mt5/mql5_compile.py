from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from foundation.control_plane.ledger import io_path, path_exists
from foundation.mt5.runtime_artifacts import REPO_ROOT, sha256_file


METAEDITOR_LOG_MAX_PATH_CHARS = 240


def metaeditor_command_log_path(log_path: Path) -> Path:
    resolved = log_path.resolve()
    if len(str(resolved)) <= METAEDITOR_LOG_MAX_PATH_CHARS:
        return log_path
    digest = hashlib.sha256(str(resolved).encode("utf-8")).hexdigest()[:16]
    return Path(tempfile.gettempdir()) / "obsidian_prime_mt5_compile" / f"compile_{digest}.log"


def _decode_log(raw_log: bytes) -> str:
    for encoding in ("utf-16", "utf-8-sig", "cp949"):
        try:
            return raw_log.decode(encoding)
        except UnicodeDecodeError:
            continue
    return raw_log.decode("utf-8", errors="ignore")


def _find_metaeditor_log(actual_log_path: Path) -> tuple[Path, str]:
    if path_exists(actual_log_path):
        return actual_log_path, _decode_log(io_path(actual_log_path).read_bytes())

    extensionless_log = actual_log_path.with_suffix("")
    if path_exists(extensionless_log):
        return extensionless_log, _decode_log(io_path(extensionless_log).read_bytes())

    parent = actual_log_path.parent
    if not path_exists(parent):
        return actual_log_path, ""

    prefixes = {
        actual_log_path.stem.lower(),
        actual_log_path.stem.lower()[:8],
        actual_log_path.stem.lower()[:6],
        actual_log_path.stem.lower()[:5],
    }
    candidates: list[Path] = []
    for name in os.listdir(io_path(parent)):
        lower_name = name.lower()
        if not any(lower_name.startswith(prefix) for prefix in prefixes if prefix):
            continue
        candidate = parent / name
        if io_path(candidate).is_file():
            candidates.append(candidate)
    if not candidates:
        for name in os.listdir(io_path(parent)):
            candidate = parent / name
            if io_path(candidate).is_file() and io_path(candidate).stat().st_size <= 2 * 1024 * 1024:
                candidates.append(candidate)
    for candidate in sorted(candidates, key=lambda item: io_path(item).stat().st_mtime, reverse=True):
        text = _decode_log(io_path(candidate).read_bytes())
        if "Result:" in text or "error" in text.lower():
            return candidate, text
    return actual_log_path, ""


def compile_mql5_ea(metaeditor_path: Path, source_path: Path, log_path: Path) -> dict[str, Any]:
    command_log_path = metaeditor_command_log_path(log_path)
    command = [str(metaeditor_path), f"/compile:{source_path.resolve()}", f"/log:{command_log_path.resolve()}"]
    if not path_exists(metaeditor_path):
        return {
            "status": "blocked",
            "command": command,
            "returncode": None,
            "log_path": log_path.as_posix(),
            "command_log_path": command_log_path.as_posix(),
            "blocker": "metaeditor_missing",
        }
    io_path(log_path.parent).mkdir(parents=True, exist_ok=True)
    io_path(command_log_path.parent).mkdir(parents=True, exist_ok=True)
    for stale_log_path in {log_path, command_log_path}:
        if path_exists(stale_log_path):
            io_path(stale_log_path).unlink()

    proc = subprocess.run(command, cwd=REPO_ROOT, text=True, capture_output=True, timeout=120)
    actual_log_path, log_text = _find_metaeditor_log(command_log_path)

    lowered = log_text.lower()
    zero_errors = "0 errors" in lowered or "0 error" in lowered or "0 error(s)" in lowered
    has_error = "error" in lowered and not zero_errors
    completed = (proc.returncode == 0 or zero_errors) and not has_error
    final_log_path = actual_log_path
    if path_exists(actual_log_path) and actual_log_path.resolve() != log_path.resolve():
        shutil.copy2(io_path(actual_log_path), io_path(log_path))
        final_log_path = log_path
    return {
        "status": "completed" if completed else "blocked",
        "command": command,
        "returncode": proc.returncode,
        "stdout": proc.stdout[-2000:],
        "stderr": proc.stderr[-2000:],
        "log_path": final_log_path.as_posix(),
        "command_log_path": command_log_path.as_posix(),
        "actual_log_path": actual_log_path.as_posix(),
        "log_sha256": sha256_file(final_log_path) if path_exists(final_log_path) else None,
    }
