from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Any

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from foundation.parity.runtime_pack_paths import DEFAULT_MT5_REQUEST, resolve_runtime_pack_paths


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Import the MT5 feature snapshot audit JSONL from Common Files into the resolved runtime parity pack folder."
    )
    parser.add_argument(
        "--mt5-request",
        default=str(DEFAULT_MT5_REQUEST),
        help="Repo-relative path to the MT5 request pack JSON.",
    )
    parser.add_argument(
        "--common-root",
        default=None,
        help="Optional override for the MT5 Common Files root. Defaults to %%APPDATA%%/MetaQuotes/Terminal/Common/Files.",
    )
    parser.add_argument(
        "--source-path",
        default=None,
        help="Optional explicit source JSONL path. Overrides the path derived from the MT5 request.",
    )
    parser.add_argument(
        "--destination-path",
        default=None,
        help="Optional explicit destination JSONL path. Overrides the path derived from the MT5 request.",
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


def ensure_path_within_common_root(path: Path, *, common_root: Path, field_name: str) -> Path:
    resolved_common_root = common_root.resolve()
    resolved_path = path.resolve()
    try:
        resolved_path.relative_to(resolved_common_root)
    except ValueError as exc:
        raise RuntimeError(
            f"{field_name} escapes common_root {resolved_common_root}: {path}"
        ) from exc
    return resolved_path


def main() -> int:
    args = parse_args()
    mt5_request_path = Path(args.mt5_request)
    resolved_paths = resolve_runtime_pack_paths(mt5_request_path)
    mt5_request = resolved_paths.mt5_request
    common_root = Path(args.common_root) if args.common_root else default_common_root()
    source_path = Path(args.source_path) if args.source_path else common_root / mt5_request["common_files_output_path"]
    destination_path = (
        Path(args.destination_path) if args.destination_path else resolved_paths.mt5_snapshot_path
    )
    source_path = ensure_path_within_common_root(
        source_path,
        common_root=common_root,
        field_name="source_path",
    )
    destination_path = resolve_runtime_pack_paths(
        mt5_request_path, mt5_snapshot_path=destination_path
    ).mt5_snapshot_path

    if not source_path.exists():
        raise RuntimeError(f"MT5 snapshot audit source file does not exist yet: {source_path}")

    destination_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_path, destination_path)

    print(
        json.dumps(
            {
                "status": "ok",
                "source_path": str(source_path.resolve()),
                "destination_path": str(destination_path.resolve()),
                "copied_bytes": source_path.stat().st_size,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
