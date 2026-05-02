from __future__ import annotations

import hashlib
import json
import os
import shutil
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from foundation.models.onnx_bridge import ordered_hash
from foundation.mt5.strategy_report import extract_mt5_strategy_report_metrics


REPO_ROOT = Path(__file__).resolve().parents[2]
EA_SOURCE_PATH = Path("foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5")
EA_EXPERT_PATH = "Project_Obsidian_Prime_v2\\foundation\\mt5\\ObsidianPrimeV2_RuntimeProbeEA.ex5"
EA_TESTER_SET_NAME = "ObsidianPrimeV2_RuntimeProbeEA.set"

_io_path = io_path
_path_exists = path_exists
_json_ready = json_ready


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_file_lf_normalized(path: Path) -> str:
    raw = io_path(path).read_bytes()
    return hashlib.sha256(raw.replace(b"\r\n", b"\n")).hexdigest()


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), indent=2), encoding="utf-8")


def mt5_runtime_module_hashes() -> list[dict[str, Any]]:
    include_root = REPO_ROOT / "foundation" / "mt5" / "include" / "ObsidianPrime"
    paths = [REPO_ROOT / EA_SOURCE_PATH]
    if path_exists(include_root):
        paths.extend(sorted(include_root.glob("*.mqh")))
    modules: list[dict[str, Any]] = []
    for path in paths:
        if not path_exists(path):
            modules.append({"path": path.relative_to(REPO_ROOT).as_posix(), "status": "missing", "sha256": None})
            continue
        modules.append(
            {
                "path": path.relative_to(REPO_ROOT).as_posix(),
                "status": "present",
                "sha256": sha256_file(path),
            }
        )
    return modules


def validate_feature_matrix(frame: pd.DataFrame, feature_order: Sequence[str]) -> np.ndarray:
    missing = [name for name in feature_order if name not in frame.columns]
    if missing:
        raise ValueError(f"Feature frame is missing feature columns: {missing}")
    matrix = frame.loc[:, list(feature_order)].to_numpy(dtype="float64", copy=False)
    if matrix.ndim != 2 or matrix.shape[1] != len(feature_order):
        raise ValueError("Feature matrix shape does not match feature order.")
    if not np.isfinite(matrix).all():
        raise ValueError("Feature matrix contains NaN or infinite values.")
    return matrix


def export_mt5_feature_matrix_csv(
    frame: pd.DataFrame,
    feature_order: Sequence[str],
    output_path: Path,
    *,
    timestamp_column: str = "timestamp",
    metadata_columns: Sequence[str] = (),
) -> dict[str, Any]:
    matrix = validate_feature_matrix(frame, feature_order)
    payload = pd.DataFrame()
    if timestamp_column in frame.columns:
        timestamps = pd.to_datetime(frame[timestamp_column], utc=True)
        payload["bar_time_server"] = timestamps.dt.strftime("%Y.%m.%d %H:%M:%S").to_numpy()
        payload["timestamp_utc"] = timestamps.dt.strftime("%Y-%m-%dT%H:%M:%SZ").to_numpy()
    if "split" in frame.columns:
        payload["split"] = frame["split"].astype(str).to_numpy()
    for name in metadata_columns:
        if name in frame.columns and name not in payload.columns:
            payload[name] = frame[name].astype(str).to_numpy()
    payload["row_index"] = np.arange(len(frame), dtype="int64")
    feature_frame = pd.DataFrame(matrix.astype("float32"), columns=list(feature_order))
    payload = pd.concat([payload, feature_frame], axis=1)
    io_path(output_path.parent).mkdir(parents=True, exist_ok=True)
    payload.to_csv(io_path(output_path), index=False, encoding="utf-8", float_format="%.10g")
    return {
        "path": output_path.as_posix(),
        "sha256": sha256_file(output_path),
        "rows": int(len(payload)),
        "feature_count": int(len(feature_order)),
        "feature_order_hash": ordered_hash(feature_order),
        "format": "csv_float32_ordered_features",
        "metadata_columns": [name for name in metadata_columns if name in frame.columns],
    }


def copy_to_common_files(common_files_root: Path, local_path: Path, common_path: str) -> dict[str, Any]:
    destination = common_files_root / Path(common_path)
    io_path(destination.parent).mkdir(parents=True, exist_ok=True)
    shutil.copy2(io_path(local_path), io_path(destination))
    return {
        "source": local_path.as_posix(),
        "common_path": common_path,
        "absolute_path": destination.as_posix(),
        "sha256": sha256_file(destination),
    }


def report_name_from_attempt(attempt: Mapping[str, Any], *, run_id: str | None = None) -> str:
    tester = attempt.get("ini", {}).get("tester", {})
    report_name = tester.get("Report")
    if not report_name:
        stem = f"{str(attempt['tier']).lower().replace(' ', '_').replace('+', 'ab')}_{attempt['split']}"
        report_name = f"Project_Obsidian_Prime_v2_{run_id or 'unknown_run'}_{stem}"
    return str(report_name)


def remove_existing_mt5_report_artifacts(
    terminal_data_root: Path,
    attempt: Mapping[str, Any],
    *,
    run_id: str | None = None,
) -> None:
    report_name = report_name_from_attempt(attempt, run_id=run_id)
    for suffix in (".htm", ".html", ".png"):
        path = terminal_data_root / f"{report_name}{suffix}"
        if path_exists(path):
            io_path(path).unlink()


def collect_mt5_strategy_report_artifacts(
    *,
    terminal_data_root: Path,
    run_output_root: Path,
    attempts: Sequence[Mapping[str, Any]],
    run_id: str | None = None,
) -> list[dict[str, Any]]:
    reports_root = run_output_root / "mt5" / "reports"
    io_path(reports_root).mkdir(parents=True, exist_ok=True)
    for existing_name in os.listdir(io_path(reports_root)):
        if not existing_name.startswith("Project_Obsidian_Prime_v2_"):
            continue
        existing = reports_root / existing_name
        existing_io = io_path(existing)
        if existing_io.is_file():
            existing_io.unlink()
    records: list[dict[str, Any]] = []
    for attempt in attempts:
        report_name = report_name_from_attempt(attempt, run_id=run_id)
        record: dict[str, Any] = {
            "attempt_name": attempt.get("attempt_name"),
            "tier": attempt["tier"],
            "split": attempt["split"],
            "report_name": report_name,
            "status": "missing",
        }
        html_source = next(
            (
                path
                for path in (terminal_data_root / f"{report_name}{suffix}" for suffix in (".htm", ".html"))
                if path_exists(path)
            ),
            None,
        )
        if html_source is not None:
            html_destination = reports_root / html_source.name
            shutil.copy2(io_path(html_source), io_path(html_destination))
            record["html_report"] = {
                "source_path": html_source.as_posix(),
                "path": html_destination.as_posix(),
                "sha256": sha256_file(html_destination),
            }
            record["metrics"] = extract_mt5_strategy_report_metrics(html_destination)
            record["status"] = record["metrics"]["status"]

        chart_source = terminal_data_root / f"{report_name}.png"
        if path_exists(chart_source):
            chart_destination = reports_root / chart_source.name
            shutil.copy2(io_path(chart_source), io_path(chart_destination))
            record["chart"] = {
                "source_path": chart_source.as_posix(),
                "path": chart_destination.as_posix(),
                "sha256": sha256_file(chart_destination),
            }
        records.append(record)
    return records


def attach_mt5_report_metrics(
    execution_results: list[dict[str, Any]],
    report_records: Sequence[Mapping[str, Any]],
) -> None:
    records_by_attempt = {
        record.get("attempt_name"): record
        for record in report_records
        if record.get("attempt_name")
    }
    records_by_key = {(record.get("tier"), record.get("split")): record for record in report_records}
    for result in execution_results:
        report_record = records_by_attempt.get(result.get("attempt_name"))
        if report_record is None:
            report_record = records_by_key.get((result.get("tier"), result.get("split")))
        if report_record is not None:
            result["strategy_tester_report"] = dict(report_record)
