from __future__ import annotations

import csv
import json
import math
import shutil
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd

from foundation.control_plane.ledger import (
    io_path,
    json_ready,
    ledger_value,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def active_branch(root: Path) -> str:
    return subprocess.check_output(["git", "branch", "--show-current"], cwd=root, text=True).strip()


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    text = json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    io_path(path).write_text(text, encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: "" if row.get(column) is None else row.get(column) for column in columns})


def numeric(value: Any, default: float = 0.0) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


def metric_value(metrics: Mapping[str, Any], key: str) -> Any:
    value = metrics.get(key)
    if value is None:
        return None
    if isinstance(value, float):
        return round(value, 6)
    return value


def pf_sort_value(value: Any) -> float:
    if value is None:
        return 999999.0
    return numeric(value)


def copy_from_common(source: Path, destination: Path, root: Path) -> dict[str, Any]:
    if not io_path(source).exists():
        raise FileNotFoundError(source)
    io_path(destination.parent).mkdir(parents=True, exist_ok=True)
    shutil.copy2(io_path(source), io_path(destination))
    return {
        "source_common_path": source.as_posix(),
        "path": rel(destination, root),
        "sha256": sha256_file_lf_normalized(destination),
    }


def upsert_csv_rows_resilient(
    path: Path,
    columns: Sequence[str],
    rows: Sequence[Mapping[str, Any]],
    *,
    key: str,
) -> dict[str, Any]:
    try:
        return upsert_csv_rows(path, columns, rows, key=key)
    except OSError:
        existing: list[dict[str, str]] = []
        if path.exists():
            with path.open("r", encoding="utf-8-sig", newline="") as handle:
                existing = [dict(row) for row in csv.DictReader(handle)]
        new_keys = {str(row.get(key, "")).strip() for row in rows}
        merged: list[Mapping[str, Any]] = [row for row in existing if str(row.get(key, "")).strip() not in new_keys]
        merged.extend(dict(row) for row in rows)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
            writer.writeheader()
            for row in merged:
                writer.writerow({column: ledger_value(row.get(column, "")) for column in columns})
        return {
            "path": path.as_posix(),
            "sha256": sha256_file_lf_normalized(path),
            "hash_policy": "lf_normalized_text_register",
            "rows": len(merged),
            "upserted_rows": len(rows),
            "fallback_writer": "normal_windows_path_retry",
        }


def write_feature_csv(path: Path, frame: pd.DataFrame, root: Path) -> dict[str, Any]:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    frame.to_csv(io_path(path), index=False, lineterminator="\n")
    return {"path": rel(path, root), "rows": int(len(frame)), "sha256": sha256_file_lf_normalized(path)}


def split_dates_from_feature_csv(frame: pd.DataFrame) -> tuple[str, str]:
    timestamps = pd.to_datetime(frame["timestamp_utc"], utc=True)
    return timestamps.min().strftime("%Y.%m.%d"), (timestamps.max() + pd.Timedelta(days=1)).strftime("%Y.%m.%d")
