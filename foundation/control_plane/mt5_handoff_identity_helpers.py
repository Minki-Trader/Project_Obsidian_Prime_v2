from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from typing import Any, Mapping, Sequence

from foundation.control_plane.ledger import io_path, json_ready


def path_text(payload: Any) -> str:
    if isinstance(payload, Mapping):
        return str(payload.get("path") or "")
    return str(payload or "")


def hash_text(payload: Any) -> str:
    if isinstance(payload, Mapping):
        return str(payload.get("sha256") or "")
    return ""


def resolve_path(root: Path, path_text_value: str) -> Path | None:
    if not path_text_value:
        return None
    path = Path(path_text_value)
    return path if path.is_absolute() else root / path


def exists(path: Path) -> bool:
    return io_path(path).exists()


def under_root(root: Path, path: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def rel(root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def parse_key_value_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in io_path(path).read_text(encoding="utf-8-sig").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith(";") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def basename(value: Any) -> str:
    return Path(str(value or "").replace("\\", "/")).name


def float_close(left: Any, right: Any, *, tolerance: float = 1e-9) -> bool:
    left_value = as_float(left)
    right_value = as_float(right)
    return left_value is not None and right_value is not None and math.isclose(left_value, right_value, abs_tol=tolerance)


def as_float(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def nested(payload: Mapping[str, Any] | None, keys: Sequence[str]) -> Any:
    current: Any = payload
    for key in keys:
        if not isinstance(current, Mapping):
            return None
        current = current.get(key)
    return current


def paths_same(left: Any, right: Any) -> bool:
    left_text = str(left or "")
    right_text = str(right or "")
    if not left_text or not right_text:
        return False
    try:
        return Path(left_text).resolve() == Path(right_text).resolve()
    except OSError:
        left_norm = left_text.replace("\\", "/")
        right_norm = right_text.replace("\\", "/")
        return left_norm.endswith(right_norm) or right_norm.endswith(left_norm)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_markdown(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8-sig")


def write_matrix_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    columns = (
        "attempt_name",
        "check_type",
        "passed",
        "path",
        "expected_sha256",
        "actual_sha256",
        "failed_checks",
        "claim_boundary",
    )
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})
