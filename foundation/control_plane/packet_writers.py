from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from foundation.mt5.runtime_artifacts import sha256_file, write_json


def materialize_manifest_and_kpi(
    output_root: Path,
    *,
    manifest_payload: Mapping[str, Any],
    kpi_payload: Mapping[str, Any],
) -> dict[str, Any]:
    manifest_path = output_root / "run_manifest.json"
    kpi_path = output_root / "kpi_record.json"
    write_json(manifest_path, manifest_payload)
    write_json(kpi_path, kpi_payload)
    return {
        "run_manifest": {"path": manifest_path.as_posix(), "sha256": sha256_file(manifest_path)},
        "kpi_record": {"path": kpi_path.as_posix(), "sha256": sha256_file(kpi_path)},
    }

