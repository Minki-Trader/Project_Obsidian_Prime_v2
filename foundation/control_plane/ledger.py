from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

try:  # pragma: no cover - optional dependency shape differs by environment
    import numpy as np
except Exception:  # pragma: no cover
    np = None  # type: ignore[assignment]

try:  # pragma: no cover - optional dependency shape differs by environment
    import pandas as pd
except Exception:  # pragma: no cover
    pd = None  # type: ignore[assignment]


ALPHA_LEDGER_COLUMNS = (
    "ledger_row_id",
    "stage_id",
    "run_id",
    "subrun_id",
    "parent_run_id",
    "record_view",
    "tier_scope",
    "kpi_scope",
    "scoreboard_lane",
    "status",
    "judgment",
    "path",
    "primary_kpi",
    "guardrail_kpi",
    "external_verification_status",
    "notes",
)
RUN_REGISTRY_COLUMNS = ("run_id", "stage_id", "lane", "status", "judgment", "path", "notes")


def io_path(path: Path) -> Path:
    resolved = path.resolve()
    if sys.platform == "win32":
        text = str(resolved)
        if not text.startswith("\\\\?\\"):
            return Path("\\\\?\\" + text)
    return resolved


def path_exists(path: Path) -> bool:
    return io_path(path).exists()


def sha256_file_lf_normalized(path: Path) -> str:
    raw = io_path(path).read_bytes()
    return hashlib.sha256(raw.replace(b"\r\n", b"\n")).hexdigest()


def json_ready(value: Any) -> Any:
    if isinstance(value, Path):
        return value.as_posix()
    if pd is not None and isinstance(value, pd.Timestamp):
        return value.isoformat()
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [json_ready(item) for item in value]
    if isinstance(value, tuple):
        return [json_ready(item) for item in value]
    if np is not None and isinstance(value, np.integer):
        return int(value)
    if np is not None and isinstance(value, np.floating):
        number = float(value)
        return number if np.isfinite(number) else None
    if np is not None and isinstance(value, np.bool_):
        return bool(value)
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


def ledger_status(value: Any) -> str:
    text = str(value or "")
    return "completed" if text.startswith("completed") else text


def ledger_value(value: Any) -> str:
    if value is None:
        return "NA"
    if np is not None and isinstance(value, np.integer):
        return str(int(value))
    if isinstance(value, int):
        return str(int(value))
    if np is not None and isinstance(value, np.floating):
        number = float(value)
        if not np.isfinite(number):
            return "NA"
        if number.is_integer():
            return str(int(number))
        return f"{number:.6g}"
    if isinstance(value, float):
        if not math.isfinite(value):
            return "NA"
        if value.is_integer():
            return str(int(value))
        return f"{value:.6g}"
    if isinstance(value, (Mapping, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return str(value)


def ledger_pairs(pairs: Sequence[tuple[str, Any]]) -> str:
    return ";".join(f"{key}={ledger_value(value)}" for key, value in pairs)


def ledger_path(path: Any) -> str:
    return Path(str(path)).as_posix() if path else ""


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv_rows(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: ledger_value(row.get(column, "")) for column in columns})


def required_row_key(row: Mapping[str, Any], key: str, row_index: int) -> str:
    if key not in row:
        raise ValueError(f"row {row_index} is missing required key `{key}`")
    value = row.get(key)
    text = str(value).strip() if value is not None else ""
    if not text:
        raise ValueError(f"row {row_index} has empty required key `{key}`")
    return text


def upsert_csv_rows(
    path: Path,
    columns: Sequence[str],
    rows: Sequence[Mapping[str, Any]],
    *,
    key: str,
) -> dict[str, Any]:
    existing = read_csv_rows(path)
    new_keys = {required_row_key(row, key, index) for index, row in enumerate(rows)}
    merged = [row for row in existing if str(row.get(key, "")).strip() not in new_keys]
    merged.extend(dict(row) for row in rows)
    write_csv_rows(path, columns, merged)
    return {
        "path": path.as_posix(),
        "sha256": sha256_file_lf_normalized(path),
        "hash_policy": "lf_normalized_text_register",
        "rows": len(merged),
        "upserted_rows": len(rows),
    }
