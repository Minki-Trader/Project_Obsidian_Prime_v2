from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

from foundation.control_plane.ledger import io_path


DEFAULT_STAGE_IDS = (
    "10_alpha_scout__default_split_model_threshold_scan",
    "11_alpha_robustness__wfo_label_horizon_sensitivity",
    "12_model_family_challenge__extratrees_training_effect",
)


@dataclass(frozen=True)
class ArchiveResult:
    manifest: dict[str, Any]
    zip_path: Path
    manifest_path: Path


def build_stage_work_archive(
    root: Path | str = Path("."),
    *,
    archive_id: str = "kpi_rebuild_preclean_stage10_12_v1",
    stage_ids: Sequence[str] = DEFAULT_STAGE_IDS,
    zip_path: Path | str | None = None,
    manifest_path: Path | str | None = None,
    created_at_utc: str | None = None,
) -> ArchiveResult:
    root_path = Path(root).resolve()
    created_at = created_at_utc or datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    archive_root = root_path / "data/snapshots/archives" / archive_id
    archive_zip = Path(zip_path) if zip_path is not None else archive_root / "stage10_12_prior_work.zip"
    manifest_file = (
        Path(manifest_path)
        if manifest_path is not None
        else root_path / "docs/agent_control/packets/kpi_rebuild_inventory_v1/archive_manifest.json"
    )
    if not archive_zip.is_absolute():
        archive_zip = root_path / archive_zip
    if not manifest_file.is_absolute():
        manifest_file = root_path / manifest_file

    source_dirs = [root_path / "stages" / stage_id for stage_id in stage_ids]
    _assert_safe_paths(root_path, [*source_dirs, archive_zip, manifest_file])

    files = _collect_files(source_dirs)
    archive_records = _archive_files(root_path, archive_zip, files)
    manifest = {
        "archive_id": archive_id,
        "created_at_utc": created_at,
        "status": "archived_snapshot_created",
        "archive_strategy": "zip_plus_manifest; original_paths_preserved",
        "zip_path": _rel(root_path, archive_zip),
        "manifest_path": _rel(root_path, manifest_file),
        "source_stage_ids": list(stage_ids),
        "source_dirs": [_rel(root_path, path) for path in source_dirs],
        "file_count": len(archive_records),
        "size_bytes": sum(int(record["size_bytes"]) for record in archive_records),
        "zip_sha256": _sha256_file(archive_zip),
        "lineage_boundary": "archive snapshot only; does not certify KPI completeness or MT5 performance",
        "visibility_policy": {
            "archive_zip_is_under_gitignored_data_snapshots": True,
            "original_paths_preserved_for_existing_ledgers": True,
            "optional_local_hidden_attribute": True,
        },
        "files": archive_records,
    }
    _write_json(manifest_file, manifest)
    return ArchiveResult(manifest=manifest, zip_path=archive_zip, manifest_path=manifest_file)


def _collect_files(source_dirs: Sequence[Path]) -> list[Path]:
    files: list[Path] = []
    for source_dir in source_dirs:
        if not io_path(source_dir).exists():
            raise FileNotFoundError(source_dir)
        files.extend(path for path in source_dir.rglob("*") if path.is_file())
    return sorted(files, key=lambda path: path.as_posix())


def _archive_files(root: Path, zip_path: Path, files: Sequence[Path]) -> list[dict[str, Any]]:
    io_path(zip_path.parent).mkdir(parents=True, exist_ok=True)
    records: list[dict[str, Any]] = []
    with zipfile.ZipFile(io_path(zip_path), "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for path in files:
            relative = _rel(root, path)
            archive.write(io_path(path), arcname=relative)
            records.append(
                {
                    "path": relative,
                    "size_bytes": io_path(path).stat().st_size,
                    "sha256": _sha256_file(path),
                }
            )
    return records


def _assert_safe_paths(root: Path, paths: Sequence[Path]) -> None:
    root_resolved = root.resolve()
    for path in paths:
        resolved = path.resolve()
        try:
            resolved.relative_to(root_resolved)
        except ValueError as exc:
            raise ValueError(f"path escapes workspace: {resolved}") from exc


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _rel(root: Path, path: Path) -> str:
    return path.resolve().relative_to(root).as_posix()


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Archive Stage 10-12 work as a ZIP plus manifest snapshot.")
    parser.add_argument("--root", default=".", help="Repository root.")
    parser.add_argument("--archive-id", default="kpi_rebuild_preclean_stage10_12_v1")
    parser.add_argument("--created-at-utc", default=None)
    args = parser.parse_args(argv)

    result = build_stage_work_archive(args.root, archive_id=args.archive_id, created_at_utc=args.created_at_utc)
    print(
        json.dumps(
            {
                "archive_id": result.manifest["archive_id"],
                "zip_path": result.manifest["zip_path"],
                "manifest_path": result.manifest["manifest_path"],
                "file_count": result.manifest["file_count"],
                "size_bytes": result.manifest["size_bytes"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
