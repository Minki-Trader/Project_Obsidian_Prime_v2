from __future__ import annotations

import csv
import hashlib
import json
import math
import subprocess
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Mapping, Sequence

from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    ledger_pairs,
    upsert_csv_rows,
)


ROOT = Path(__file__).resolve().parents[2]
RUN_REGISTRY_PATH = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_ALPHA_LEDGER_PATH = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
WORKSPACE_STATE_PATH = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE_PATH = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG_PATH = ROOT / "docs" / "workspace" / "changelog.md"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return io_path(path).resolve().relative_to(io_path(ROOT).resolve()).as_posix()


def active_branch() -> str:
    return subprocess.check_output(["git", "branch", "--show-current"], cwd=io_path(ROOT), text=True).strip()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames = list(columns or (rows[0].keys() if rows else ()))
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: "" if row.get(column) is None else row.get(column) for column in fieldnames})


def numeric(value: Any, default: float = 0.0) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


def profit_factor(values: Sequence[float]) -> float | None:
    gross_profit = sum(value for value in values if value > 0)
    gross_loss = -sum(value for value in values if value < 0)
    if gross_loss <= 0:
        return None if gross_profit <= 0 else 999.0
    return gross_profit / gross_loss


def split_dates(frame: Any, split_name: str) -> tuple[str, str]:
    split = frame.loc[frame["split"].astype(str).eq(split_name)].copy()
    if split.empty:
        raise RuntimeError(f"empty split: {split_name}")
    timestamps = split["timestamp"]
    start = timestamps.min().strftime("%Y.%m.%d")
    end = (timestamps.max() + timedelta(days=1)).strftime("%Y.%m.%d")
    return start, end


def upsert_run_rows(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, rows, key="run_id")


def upsert_alpha_rows(path: Path, rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return upsert_csv_rows(path, ALPHA_LEDGER_COLUMNS, rows, key="ledger_row_id")


__all__ = [
    "ALPHA_LEDGER_COLUMNS",
    "RUN_REGISTRY_COLUMNS",
    "CHANGELOG_PATH",
    "CURRENT_WORKING_STATE_PATH",
    "PROJECT_ALPHA_LEDGER_PATH",
    "ROOT",
    "RUN_REGISTRY_PATH",
    "WORKSPACE_STATE_PATH",
    "active_branch",
    "io_path",
    "json_ready",
    "ledger_pairs",
    "numeric",
    "profit_factor",
    "read_json",
    "rel",
    "sha256_file",
    "split_dates",
    "upsert_alpha_rows",
    "upsert_run_rows",
    "utc_now",
    "write_csv",
    "write_json",
    "write_md",
]
