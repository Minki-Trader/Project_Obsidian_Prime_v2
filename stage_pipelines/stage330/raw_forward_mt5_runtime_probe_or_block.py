from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import shutil
import subprocess
import sys
import time
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.mt5_kpi_records import TIER_A, build_mt5_kpi_records  # noqa: E402
from foundation.control_plane.mt5_tier_balance_completion import (  # noqa: E402
    COMMON_FILES_ROOT_DEFAULT,
    METAEDITOR_PATH_DEFAULT,
    TERMINAL_DATA_ROOT_DEFAULT,
    TERMINAL_PATH_DEFAULT,
    TESTER_PROFILE_ROOT_DEFAULT,
)
from foundation.models.onnx_bridge import ordered_hash  # noqa: E402
from foundation.mt5 import runtime_support as mt5  # noqa: E402


STAGE_ID = "330_onnx_rebuild__forward_safe_non_identity_surface_robustness"
RUN_ID = "run330E_mt5_runtime_probe_or_block_v1"
RUN_NUMBER = "run330E"
PARENT_RUN_ID = "run330D_regime_attribution_v1"
EXPLORATION_LABEL = "stage330_Runtime__RawForwardMt5ProbeOrBlock"

STATUS_COMPLETED = "completed_raw_forward_mt5_runtime_probe_no_forward_decision"
STATUS_PARTIAL = "partial_raw_forward_mt5_runtime_probe_subset_no_forward_decision"
STATUS_BLOCKED = "blocked_raw_forward_mt5_runtime_probe_no_completed_runtime"
JUDGMENT_COMPLETED = "raw_forward_runtime_probe_completed_research_only_no_goal_achieve"
JUDGMENT_BLOCKED = "raw_forward_runtime_probe_blocked_requires_runtime_repair_no_goal_achieve"
DECISION_COMPLETED = "stage330E_raw_forward_mt5_evidence_available_review_required_no_selection"
DECISION_BLOCKED = "stage330E_forward_blocked_runtime_probe_missing_no_pass_fail_judgment"
NEXT_COMPLETED = "run330F_raw_forward_mt5_kpi_regime_cost_curve_review"
NEXT_PARTIAL = "run330E_continue_remaining_raw_forward_runtime_probe_or_repair"
NEXT_BLOCKED = "repair_stage330E_runtime_probe_blocker_then_rerun"
CLAIM_BOUNDARY = (
    "research_development_only_raw_forward_mt5_runtime_probe_no_threshold_retuning_"
    "no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_"
    "no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

COMMON_ROOT = "Project_Obsidian_Prime_v2/stage330/run330E_raw_forward_mt5_runtime_probe"
SPLIT_LABEL = "forward_raw_forward"
MAX_HOLD_BARS = 12

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
FEATURE_MATRIX_DIR = RUN_DIR / "feature_matrices"
MT5_DIR = RUN_DIR / "mt5"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"

SOURCE_STAGE_DIR = ROOT / "stages" / "329_onnx_rebuild__live_feature_control"
RUN329B_DIR = SOURCE_STAGE_DIR / "02_runs" / "run329B"
RUN329C_DIR = SOURCE_STAGE_DIR / "02_runs" / "run329C"
FEATURE_FRAME_DIR = RUN329B_DIR / "feature_frames"
FEATURE_ORDER_DIR = RUN329B_DIR / "feature_orders"

RUN330B_DIR = STAGE_DIR / "02_runs" / "run330B"
RUN330D_DIR = STAGE_DIR / "02_runs" / "run330D"
SIGNAL_MANIFEST = RUN330B_DIR / "signal_payload_manifest.csv"
FIXED_SUMMARY = RUN330B_DIR / "fixed_threshold_replay_summary.csv"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-26_stage330E_raw_forward_mt5_runtime_probe_or_block.md"


def io_path(path: Path) -> Path:
    resolved = path.resolve()
    if os.name == "nt":
        text = str(resolved)
        if len(text) > 240 and not text.startswith("\\\\?\\"):
            return Path("\\\\?\\" + text)
    return resolved


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def path_exists(path: Path) -> bool:
    return io_path(path).exists()


def open_with_retry(path: Path, mode: str, **kwargs: Any):
    last_error: OSError | None = None
    for attempt in range(10):
        try:
            return open(str(io_path(path)), mode, **kwargs)
        except OSError as exc:
            last_error = exc
            if exc.errno != 22 or attempt == 9:
                raise
            time.sleep(0.2)
    raise last_error or OSError(f"failed to open {path}")


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open_with_retry(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, Path):
        return rel(value)
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if hasattr(value, "item"):
        try:
            return json_ready(value.item())
        except Exception:
            return str(value)
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return None
    return value


def csv_value(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return ""
        return round(value, 10)
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    if isinstance(value, pd.Timestamp):
        if value.tzinfo is not None:
            value = value.tz_convert("UTC").tz_localize(None)
        return value.strftime("%Y-%m-%d %H:%M:%S")
    return value


def write_text(path: Path, text: str, *, encoding: str = "utf-8") -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open_with_retry(path, "w", encoding=encoding, newline="\n") as handle:
        handle.write(text)
    return path


def write_md(path: Path, text: str) -> Path:
    return write_text(path, text.strip() + "\n", encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open_with_retry(path, "w", encoding="utf-8") as handle:
        json.dump(json_ready(payload), handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    return path


def write_csv(path: Path, columns: Sequence[str], rows: Iterable[Mapping[str, Any]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open_with_retry(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column)) for column in columns})
    return path


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with open_with_retry(path, "r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def upsert_csv(path: Path, keys: Sequence[str], new_rows: Sequence[Mapping[str, Any]]) -> None:
    rows = read_csv_rows(path)
    fieldnames: list[str] = []
    if path_exists(path):
        with open_with_retry(path, "r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.reader(handle)
            fieldnames = next(reader, [])
    for row in new_rows:
        for key in row.keys():
            if key not in fieldnames:
                fieldnames.append(key)
    if not fieldnames:
        return
    pending = {
        tuple(str(row.get(key, "")) for key in keys): {key: csv_value(value) for key, value in row.items()}
        for row in new_rows
    }
    output: list[Mapping[str, Any]] = []
    replaced: set[tuple[str, ...]] = set()
    for row in rows:
        row_key = tuple(str(row.get(key, "")) for key in keys)
        if row_key in pending:
            output.append(pending[row_key])
            replaced.add(row_key)
        else:
            output.append(row)
    for row_key, row in pending.items():
        if row_key not in replaced:
            output.append(row)
    write_csv(path, fieldnames, output)


def read_text_lossless(path: Path) -> tuple[str, bool]:
    with open_with_retry(path, "rb") as handle:
        raw = handle.read()
    return raw.decode("utf-8-sig"), raw.startswith(b"\xef\xbb\xbf")


def write_text_lossless(path: Path, text: str, had_bom: bool) -> Path:
    encoding = "utf-8-sig" if had_bom else "utf-8"
    with open_with_retry(path, "w", encoding=encoding, newline="\n") as handle:
        handle.write(text)
    return path


def replace_prefix_line(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text.rstrip() + "\n" + replacement + "\n"


def append_if_missing(path: Path, marker: str, block: str) -> Path:
    text, had_bom = read_text_lossless(path)
    if marker not in text:
        text = text.rstrip() + "\n\n" + block.strip() + "\n"
        write_text_lossless(path, text, had_bom)
    return path


def mt5_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return f"{value:.12g}"
    return str(value)


def write_set(path: Path, values: Mapping[str, Any]) -> dict[str, Any]:
    lines = ["; generated_by=stage_pipelines.stage330.raw_forward_mt5_runtime_probe_or_block"]
    lines.extend(f"{key}={mt5_value(value)}" for key, value in values.items())
    write_text(path, "\n".join(lines) + "\n")
    return {"path": rel(path), "sha256": sha256_file(path), "format": "mt5_set", "parameter_count": len(values)}


def write_ini(path: Path, values: Mapping[str, Any]) -> dict[str, Any]:
    lines = ["[Tester]"]
    lines.extend(f"{key}={mt5_value(value)}" for key, value in values.items())
    write_text(path, "\n".join(lines) + "\n")
    return {"path": rel(path), "sha256": sha256_file(path), "format": "mt5_tester_ini", "tester": dict(values)}


def load_feature_order(feature_set_id: str) -> list[str]:
    path = FEATURE_ORDER_DIR / f"{feature_set_id}_feature_order.txt"
    return [line.strip() for line in io_path(path).read_text(encoding="utf-8").splitlines() if line.strip()]


def raw_forward_queue() -> list[dict[str, Any]]:
    signal_rows = {
        (row["artifact_slug"], row["view_id"]): row
        for row in read_csv_rows(SIGNAL_MANIFEST)
        if row.get("view_id") == "raw_forward"
    }
    rows: list[dict[str, Any]] = []
    for row in read_csv_rows(FIXED_SUMMARY):
        if row.get("view_id") != "raw_forward":
            continue
        merged = dict(row)
        merged.update(signal_rows.get((row["artifact_slug"], row["view_id"]), {}))
        if not merged.get("prediction_path"):
            merged["prediction_path"] = rel(RUN330B_DIR / "predictions" / f"{row['artifact_slug']}_raw_forward_score.parquet")
        rows.append(merged)
    if not rows:
        raise RuntimeError("raw_forward queue is empty")
    return rows


def tester_dates(timestamps: pd.Series) -> tuple[str, str]:
    start = pd.to_datetime(timestamps, utc=True).min().date()
    end = pd.to_datetime(timestamps, utc=True).max().date() + timedelta(days=1)
    return start.strftime("%Y.%m.%d"), end.strftime("%Y.%m.%d")


def export_feature_matrix_csv(frame: pd.DataFrame, features: Sequence[str], output_path: Path) -> dict[str, Any]:
    missing = sorted(set(features).difference(frame.columns))
    if missing:
        raise RuntimeError(f"feature matrix missing columns: {missing}")
    values = frame.loc[:, list(features)].to_numpy(dtype="float64", copy=False)
    if not np.isfinite(values).all():
        raise RuntimeError("feature matrix contains non-finite values")
    timestamps = pd.to_datetime(frame["timestamp"], utc=True)
    output = pd.DataFrame(
        {
            "bar_time_server": timestamps.dt.strftime("%Y.%m.%d %H:%M:%S").to_numpy(),
            "timestamp_utc": timestamps.dt.strftime("%Y-%m-%dT%H:%M:%SZ").to_numpy(),
            "row_index": np.arange(len(frame), dtype="int64"),
        }
    )
    output = pd.concat([output, pd.DataFrame(values.astype("float32"), columns=list(features))], axis=1)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output.to_csv(io_path(output_path), index=False, encoding="utf-8", float_format="%.10g", lineterminator="\n")
    return {
        "path": rel(output_path),
        "sha256": sha256_file(output_path),
        "rows": int(len(output)),
        "feature_count": int(len(features)),
        "feature_order_hash": ordered_hash(features),
        "first_timestamp": timestamps.min().isoformat(),
        "last_timestamp": timestamps.max().isoformat(),
        "format": "mt5_feature_csv_bar_time_server_plus_ordered_float32_features",
    }


def copy_to_common(local_path: Path, common_files_root: Path, common_path: str) -> dict[str, Any]:
    destination = common_files_root / Path(common_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(io_path(local_path), io_path(destination))
    return {
        "source": rel(local_path),
        "common_path": common_path,
        "absolute_path": destination.as_posix(),
        "sha256": sha256_file(destination),
    }


def build_materialized_attempts(common_files_root: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[Path]]:
    attempts: list[dict[str, Any]] = []
    matrix_rows: list[dict[str, Any]] = []
    artifacts: list[Path] = []
    for row in raw_forward_queue():
        slug = row["artifact_slug"]
        candidate_id = row["candidate_id"]
        feature_set_id = row["feature_set_id"]
        model_id = row["model_id"]
        features = load_feature_order(feature_set_id)
        frame = pd.read_parquet(io_path(FEATURE_FRAME_DIR / f"{feature_set_id}.parquet"))
        frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
        prediction_path = ROOT / row["prediction_path"]
        prediction = pd.read_parquet(io_path(prediction_path))
        prediction["timestamp"] = pd.to_datetime(prediction["timestamp"], utc=True)
        view_frame = frame.loc[frame["timestamp"].isin(pd.Index(prediction["timestamp"]))].copy()
        view_frame = view_frame.sort_values("timestamp").reset_index(drop=True)
        prediction = prediction.sort_values("timestamp").reset_index(drop=True)
        if len(view_frame) != len(prediction):
            raise RuntimeError(f"{slug} feature/prediction row mismatch: {len(view_frame)} != {len(prediction)}")
        if not view_frame["timestamp"].reset_index(drop=True).equals(prediction["timestamp"].reset_index(drop=True)):
            raise RuntimeError(f"{slug} feature/prediction timestamp mismatch")

        feature_csv = FEATURE_MATRIX_DIR / f"{slug}_raw_forward_features.csv"
        feature_export = export_feature_matrix_csv(view_frame, features, feature_csv)
        artifacts.append(feature_csv)
        model_path = RUN329C_DIR / "onnx" / f"{slug}.onnx"
        if not path_exists(model_path):
            raise FileNotFoundError(model_path)
        model_common_path = f"{COMMON_ROOT}/models/{slug}.onnx"
        feature_common_path = f"{COMMON_ROOT}/features/{feature_csv.name}"
        model_copy = copy_to_common(model_path, common_files_root, model_common_path)
        feature_copy = copy_to_common(feature_csv, common_files_root, feature_common_path)
        from_date, to_date = tester_dates(view_frame["timestamp"])
        threshold = float(row.get("threshold") or row.get("decision_threshold"))
        attempt_name = f"{slug}_rf"
        telemetry = f"{COMMON_ROOT}/telemetry/{attempt_name}_telemetry.csv"
        summary = f"{COMMON_ROOT}/telemetry/{attempt_name}_summary.csv"
        feature_hash = ordered_hash(features)
        set_values = {
            "InpRunId": RUN_ID,
            "InpExplorationLabel": EXPLORATION_LABEL,
            "InpTierLabel": TIER_A,
            "InpPrimaryActiveTier": "tier_a",
            "InpSplitLabel": SPLIT_LABEL,
            "InpMainSymbol": "US100",
            "InpTimeframe": 5,
            "InpModelPath": model_common_path,
            "InpModelId": f"{RUN_ID}_{slug}_onnx",
            "InpModelBackend": "onnx",
            "InpModelUseCommonFiles": "true",
            "InpFeatureCsvPath": feature_common_path,
            "InpFeatureCount": len(features),
            "InpFeatureCsvUseCommonFiles": "true",
            "InpFeatureRequireTimestampMatch": "true",
            "InpFeatureAllowLatestFallback": "false",
            "InpFeatureStrictHeader": "true",
            "InpCsvTimestampIsBarClose": "true",
            "InpFeatureOrderHash": feature_hash,
            "InpFallbackEnabled": "false",
            "InpFallbackFeatureCsvPath": feature_common_path,
            "InpFallbackFeatureCount": len(features),
            "InpFallbackModelPath": model_common_path,
            "InpFallbackModelId": f"{RUN_ID}_{slug}_onnx",
            "InpFallbackModelBackend": "onnx",
            "InpFallbackFeatureOrderHash": feature_hash,
            "InpTelemetryCsvPath": telemetry,
            "InpSummaryCsvPath": summary,
            "InpTelemetryUseCommonFiles": "true",
            "InpShortThreshold": 0.0,
            "InpLongThreshold": 0.0,
            "InpMinMargin": threshold,
            "InpInvertSignal": "false",
            "InpFallbackShortThreshold": 0.0,
            "InpFallbackLongThreshold": 0.0,
            "InpFallbackMinMargin": threshold,
            "InpFallbackInvertSignal": "false",
            "InpAllowTrading": "true",
            "InpFixedLot": 0.1,
            "InpCloseOnFlatSignal": "false",
            "InpReverseOnOppositeSignal": "true",
            "InpCloseOnlyOnOppositeSignal": "false",
            "InpMaxHoldBars": MAX_HOLD_BARS,
            "InpMaxConcurrentPositions": 1,
            "InpReentryCooldownBars": 0,
            "InpSameDirectionReentryCooldownBars": 0,
            "InpAtrSltpEnabled": "false",
            "InpModelRiskSizingEnabled": "false",
            "InpMagic": 3300500 + len(attempts),
        }
        set_payload = write_set(MT5_DIR / f"{attempt_name}.set", set_values)
        report_name = f"Project_Obsidian_Prime_v2_{RUN_ID}_{attempt_name}"
        ini_payload = write_ini(
            MT5_DIR / f"{attempt_name}.ini",
            {
                "Expert": r"Project_Obsidian_Prime_v2\foundation\mt5\ObsidianPrimeV2_RuntimeProbeEA.ex5",
                "Symbol": "US100",
                "Period": "M5",
                "Model": 4,
                "Deposit": 500,
                "Leverage": "1:100",
                "Optimization": 0,
                "ExecutionMode": 0,
                "ForwardMode": 0,
                "UseLocal": 1,
                "UseRemote": 0,
                "UseCloud": 0,
                "ReplaceReport": 1,
                "ShutdownTerminal": 1,
                "FromDate": from_date,
                "ToDate": to_date,
                "Report": report_name,
                "ExpertParameters": mt5.EA_TESTER_SET_NAME,
            },
        )
        artifacts.extend([MT5_DIR / f"{attempt_name}.set", MT5_DIR / f"{attempt_name}.ini"])
        matrix_rows.append(
            {
                "candidate_id": candidate_id,
                "artifact_slug": slug,
                "feature_set_id": feature_set_id,
                "model_id": model_id,
                "feature_count": len(features),
                "rows": feature_export["rows"],
                "first_timestamp": feature_export["first_timestamp"],
                "last_timestamp": feature_export["last_timestamp"],
                "decision_surface_mapping": "short_threshold=0,long_threshold=0,min_margin=fixed_train_margin_threshold",
                "decision_threshold": threshold,
                "feature_matrix_path": feature_export["path"],
                "feature_matrix_sha256": feature_export["sha256"],
                "onnx_path": rel(model_path),
                "onnx_sha256": sha256_file(model_path),
                "prediction_path": row["prediction_path"],
                "prediction_sha256": row.get("prediction_sha256", ""),
                "signal_payload_path": row.get("signal_payload_path", ""),
                "signal_rows": row.get("signal_rows", ""),
                "common_feature_path": feature_common_path,
                "common_model_path": model_common_path,
            }
        )
        attempts.append(
            {
                "attempt_name": attempt_name,
                "candidate_id": candidate_id,
                "artifact_slug": slug,
                "feature_set_id": feature_set_id,
                "model_id": model_id,
                "tier": TIER_A,
                "split": SPLIT_LABEL,
                "attempt_role": "raw_forward_tier_a_no_fallback_runtime_probe",
                "record_view_prefix": f"mt5_{slug}_raw_forward",
                "set": set_payload,
                "ini": ini_payload,
                "common_telemetry_path": telemetry,
                "common_summary_path": summary,
                "feature_export": feature_export,
                "model_copy": model_copy,
                "feature_copy": feature_copy,
                "from_date": from_date,
                "to_date": to_date,
                "decision_threshold": threshold,
                "decision_surface_mapping": "stage330B_raw_forward_nonflat_prediction_and_fixed_train_margin_threshold_mapped_to_min_margin_only",
                "routing_mode": "tier_a_primary_no_fallback",
                "signal_policy": "raw_forward ONNX probabilities with fixed train-only margin threshold; no forward retuning",
            }
        )
    return attempts, matrix_rows, artifacts


def selected_attempts(attempts: Sequence[dict[str, Any]], start_index: int, limit: int | None) -> list[dict[str, Any]]:
    start = max(0, int(start_index))
    end = None if limit is None else start + max(0, int(limit))
    return list(attempts[start:end])


def clear_runtime_outputs(common_files_root: Path, attempt: Mapping[str, Any]) -> None:
    for key in ("common_telemetry_path", "common_summary_path"):
        path = common_files_root / Path(str(attempt[key]))
        if path_exists(path):
            io_path(path).unlink()


def terminal_runtime_output_snapshot(common_files_root: Path, attempt: Mapping[str, Any], *, status: str, wait_status: str) -> dict[str, Any]:
    payload = mt5.validate_mt5_runtime_outputs(common_files_root, attempt)
    payload["status"] = status
    payload["wait_status"] = wait_status
    return payload


def detect_running_terminal_processes(terminal_path: Path) -> dict[str, Any]:
    command = [
        "powershell",
        "-NoProfile",
        "-Command",
        (
            "Get-CimInstance Win32_Process -Filter \"name = 'terminal64.exe'\" | "
            "Select-Object ProcessId,ExecutablePath,CommandLine | ConvertTo-Json -Compress"
        ),
    ]
    proc = subprocess.run(command, text=True, capture_output=True, timeout=30)
    processes: list[dict[str, Any]] = []
    if proc.stdout.strip():
        parsed = json.loads(proc.stdout)
        if isinstance(parsed, dict):
            processes = [parsed]
        elif isinstance(parsed, list):
            processes = parsed
    target = str(terminal_path).lower()
    matching = []
    for item in processes:
        executable = str(item.get("ExecutablePath") or item.get("executable_path") or "").lower()
        if not executable or executable == target:
            matching.append(item)
    return {
        "status": "running" if matching else "not_running",
        "command": command,
        "returncode": proc.returncode,
        "processes": processes,
        "matching_processes": matching,
    }


def execute_attempts(
    attempts: Sequence[dict[str, Any]],
    *,
    terminal_path: Path,
    metaeditor_path: Path,
    terminal_data_root: Path,
    common_files_root: Path,
    tester_profile_root: Path,
    timeout_seconds: int,
    runtime_timeout_seconds: int,
    terminal_extra_args: Sequence[str],
) -> dict[str, Any]:
    compile_payload = mt5.compile_mql5_ea(metaeditor_path, mt5.EA_SOURCE_PATH, MT5_DIR / "mt5_compile.log")
    terminal_process_probe = detect_running_terminal_processes(terminal_path)
    execution_results: list[dict[str, Any]] = []
    if compile_payload.get("status") == "completed":
        for attempt in attempts:
            clear_runtime_outputs(common_files_root, attempt)
            mt5.remove_existing_mt5_report_artifacts(terminal_data_root, attempt, run_id=RUN_ID)
            tester_profile_ini_path = tester_profile_root / f"opv2_s330e_{attempt['attempt_name']}.ini"
            if terminal_process_probe.get("status") == "running":
                result = {
                    "status": "blocked",
                    "command": [str(terminal_path), *terminal_extra_args, f"/config:{tester_profile_ini_path}"],
                    "returncode": None,
                    "blocker": "terminal_already_running_config_not_applied",
                    "blocker_explanation": (
                        "A running terminal64.exe process can absorb a /config launch without applying the requested "
                        "strategy tester configuration. The terminal must be closed or a separate portable instance "
                        "must be used before rerun."
                    ),
                    "terminal_process_probe": terminal_process_probe,
                    "runtime_outputs": terminal_runtime_output_snapshot(
                        common_files_root,
                        attempt,
                        status="blocked",
                        wait_status="skipped_terminal_already_running",
                    ),
                }
            else:
                try:
                    result = mt5.run_mt5_tester(
                        terminal_path,
                        ROOT / str(attempt["ini"]["path"]),
                        set_path=ROOT / str(attempt["set"]["path"]),
                        tester_profile_set_path=tester_profile_root / mt5.EA_TESTER_SET_NAME,
                        tester_profile_ini_path=tester_profile_ini_path,
                        timeout_seconds=timeout_seconds,
                        terminal_extra_args=terminal_extra_args,
                    )
                except subprocess.TimeoutExpired as exc:
                    result = {
                        "status": "blocked",
                        "command": exc.cmd,
                        "returncode": None,
                        "blocker": "terminal_timeout",
                        "timeout_seconds": timeout_seconds,
                    }
                except Exception as exc:  # pragma: no cover
                    result = {
                        "status": "blocked",
                        "command": [],
                        "returncode": None,
                        "blocker": f"terminal_exception:{type(exc).__name__}",
                        "error": str(exc),
                    }
                result["runtime_outputs"] = mt5.wait_for_mt5_runtime_outputs(
                    common_files_root,
                    attempt,
                    timeout_seconds=runtime_timeout_seconds,
                    poll_seconds=2.0,
                )
                if result["runtime_outputs"].get("status") != "completed":
                    result["status"] = "blocked"
            result.update(
                {
                    "attempt_name": attempt.get("attempt_name"),
                    "candidate_id": attempt.get("candidate_id"),
                    "artifact_slug": attempt.get("artifact_slug"),
                    "feature_set_id": attempt.get("feature_set_id"),
                    "model_id": attempt.get("model_id"),
                    "tier": attempt.get("tier"),
                    "split": attempt.get("split"),
                    "attempt_role": attempt.get("attempt_role"),
                    "record_view_prefix": attempt.get("record_view_prefix"),
                    "routing_mode": attempt.get("routing_mode"),
                    "signal_policy": attempt.get("signal_policy"),
                    "ini_path": attempt.get("ini", {}).get("path"),
                    "set_path": attempt.get("set", {}).get("path"),
                }
            )
            execution_results.append(result)
    report_records = mt5.collect_mt5_strategy_report_artifacts(
        terminal_data_root=terminal_data_root,
        run_output_root=RUN_DIR,
        attempts=attempts,
        run_id=RUN_ID,
    )
    mt5.attach_mt5_report_metrics(execution_results, report_records)
    return {
        "compile": compile_payload,
        "terminal_process_probe": terminal_process_probe,
        "terminal_extra_args": list(terminal_extra_args),
        "execution_results": execution_results,
        "strategy_tester_reports": report_records,
        "mt5_kpi_records": build_mt5_kpi_records(execution_results),
    }


def classify(
    attempts: Sequence[dict[str, Any]],
    executed_attempts: Sequence[dict[str, Any]],
    execution_result: Mapping[str, Any],
    materialize_only: bool,
) -> tuple[str, str, str, str]:
    if materialize_only:
        return STATUS_BLOCKED, "materialized_only_no_external_runtime_execution", DECISION_BLOCKED, NEXT_BLOCKED
    completed = sum(1 for row in execution_result.get("execution_results", []) if row.get("status") == "completed")
    if completed <= 0:
        return STATUS_BLOCKED, JUDGMENT_BLOCKED, DECISION_BLOCKED, NEXT_BLOCKED
    if completed < len(attempts) or len(executed_attempts) < len(attempts):
        return STATUS_PARTIAL, JUDGMENT_COMPLETED, DECISION_COMPLETED, NEXT_PARTIAL
    return STATUS_COMPLETED, JUDGMENT_COMPLETED, DECISION_COMPLETED, NEXT_COMPLETED


def runtime_blockers(execution_result: Mapping[str, Any]) -> list[str]:
    blockers = {
        str(row.get("blocker"))
        for row in execution_result.get("execution_results", [])
        if row.get("blocker")
    }
    compile_status = execution_result.get("compile", {}).get("status")
    if compile_status and compile_status != "completed":
        blockers.add(f"compile_{compile_status}")
    return sorted(blockers)


def summary_rows(attempts: Sequence[dict[str, Any]], execution_result: Mapping[str, Any]) -> list[dict[str, Any]]:
    result_by_attempt = {str(row.get("attempt_name")): row for row in execution_result.get("execution_results", [])}
    rows: list[dict[str, Any]] = []
    for attempt in attempts:
        result = result_by_attempt.get(str(attempt["attempt_name"]), {})
        runtime = result.get("runtime_outputs", {})
        report = result.get("strategy_tester_report", {})
        metrics = report.get("metrics", {}) if isinstance(report, Mapping) else {}
        rows.append(
            {
                "attempt_name": attempt["attempt_name"],
                "candidate_id": attempt["candidate_id"],
                "artifact_slug": attempt["artifact_slug"],
                "feature_set_id": attempt["feature_set_id"],
                "tester_status": result.get("status", "not_attempted"),
                "runtime_status": runtime.get("status", "not_attempted"),
                "report_status": report.get("status", "not_attempted") if isinstance(report, Mapping) else "not_attempted",
                "returncode": result.get("returncode", ""),
                "blocker": result.get("blocker", ""),
                "feature_ready_count": runtime.get("last_summary", {}).get("feature_ready_count", ""),
                "model_ok_count": runtime.get("last_summary", {}).get("model_ok_count", ""),
                "order_attempt_count": runtime.get("last_summary", {}).get("order_attempt_count", ""),
                "order_fill_count": runtime.get("last_summary", {}).get("order_fill_count", ""),
                "net_profit": metrics.get("net_profit", ""),
                "profit_factor": metrics.get("profit_factor", ""),
                "trade_count": metrics.get("trade_count", ""),
                "common_summary_path": attempt["common_summary_path"],
                "common_telemetry_path": attempt["common_telemetry_path"],
                "report_name": mt5.report_name_from_attempt(attempt, run_id=RUN_ID),
            }
        )
    return rows


def copy_runtime_telemetry_artifacts(common_files_root: Path, attempts: Sequence[dict[str, Any]]) -> list[Path]:
    copied: list[Path] = []
    output_dir = RUN_DIR / "runtime_telemetry"
    output_dir.mkdir(parents=True, exist_ok=True)
    for attempt in attempts:
        for key in ("common_telemetry_path", "common_summary_path"):
            source = common_files_root / Path(str(attempt[key]))
            if path_exists(source):
                destination = output_dir / source.name
                shutil.copy2(io_path(source), io_path(destination))
                copied.append(destination)
    return copied


def write_run_artifacts(
    generated_at_utc: str,
    all_attempts: Sequence[dict[str, Any]],
    executed_attempts: Sequence[dict[str, Any]],
    matrix_rows: Sequence[dict[str, Any]],
    execution_result: Mapping[str, Any],
    status: str,
    judgment: str,
    decision: str,
    next_action: str,
    args: argparse.Namespace,
    materialized_artifacts: Sequence[Path],
) -> list[Path]:
    artifacts: list[Path] = list(materialized_artifacts)
    compile_log = MT5_DIR / "mt5_compile.log"
    if path_exists(compile_log):
        artifacts.append(compile_log)
    matrix_path = RUN_DIR / "raw_forward_feature_matrix_manifest.csv"
    artifacts.append(
        write_csv(
            matrix_path,
            [
                "candidate_id",
                "artifact_slug",
                "feature_set_id",
                "model_id",
                "feature_count",
                "rows",
                "first_timestamp",
                "last_timestamp",
                "decision_surface_mapping",
                "decision_threshold",
                "feature_matrix_path",
                "feature_matrix_sha256",
                "onnx_path",
                "onnx_sha256",
                "prediction_path",
                "prediction_sha256",
                "signal_payload_path",
                "signal_rows",
                "common_feature_path",
                "common_model_path",
            ],
            matrix_rows,
        )
    )
    attempts_path = RUN_DIR / "mt5_probe_attempts.json"
    execution_path = RUN_DIR / "execution_result.json"
    summary_path = RUN_DIR / "mt5_runtime_probe_summary.csv"
    kpi_path = RUN_DIR / "mt5_kpi_records.json"
    artifacts.extend(
        [
            write_json(attempts_path, list(all_attempts)),
            write_json(execution_path, execution_result),
            write_csv(
                summary_path,
                [
                    "attempt_name",
                    "candidate_id",
                    "artifact_slug",
                    "feature_set_id",
                    "tester_status",
                    "runtime_status",
                    "report_status",
                    "returncode",
                    "blocker",
                    "feature_ready_count",
                    "model_ok_count",
                    "order_attempt_count",
                    "order_fill_count",
                    "net_profit",
                    "profit_factor",
                    "trade_count",
                    "common_summary_path",
                    "common_telemetry_path",
                    "report_name",
                ],
                summary_rows(all_attempts, execution_result),
            ),
            write_json(kpi_path, execution_result.get("mt5_kpi_records", [])),
        ]
    )
    artifacts.extend(copy_runtime_telemetry_artifacts(Path(args.common_files_root), all_attempts))

    completed_count = sum(1 for row in execution_result.get("execution_results", []) if row.get("status") == "completed")
    blockers = runtime_blockers(execution_result)
    runtime_receipt = RUN_DIR / "runtime_parity_receipt.json"
    backtest_receipt = RUN_DIR / "backtest_forensics_receipt.json"
    result_path = RUN_DIR / "result_judgment.csv"
    gate_path = RUN_DIR / "required_gate_coverage_audit.csv"
    lineage_path = RUN_DIR / "artifact_lineage_receipt.json"
    manifest_path = RUN_DIR / "run_manifest.json"

    artifacts.append(
        write_json(
            runtime_receipt,
            {
                "research_path": rel(Path(__file__)),
                "runtime_path": rel(mt5.EA_SOURCE_PATH),
                "shared_contract": {
                    "model": "run329C ONNX candidates reused unchanged",
                    "feature_input": "run329B feature order and run330B raw_forward timestamps",
                    "decision_surface": "Stage330B fixed train-only probability margin threshold mapped to MT5 min_margin",
                    "risk_lot": "fixed lot 0.1, max hold 12 bars, no ATR SLTP, no model risk sizing",
                },
                "known_differences": [
                    "MT5 tester can only run if the configured terminal accepts the /config launch.",
                    "This is runtime_probe(런타임 탐침), not runtime_authority(런타임 권위).",
                ],
                "parity_check": rel(summary_path),
                "parity_identity": {
                    "module_hashes": mt5.mt5_runtime_module_hashes(),
                    "compile": execution_result.get("compile", {}),
                    "terminal_process_probe": execution_result.get("terminal_process_probe", {}),
                    "terminal_extra_args": execution_result.get("terminal_extra_args", []),
                    "planned_attempt_count": len(all_attempts),
                    "executed_attempt_count": len(executed_attempts),
                    "completed_attempt_count": completed_count,
                    "runtime_blockers": blockers,
                },
                "runtime_claim_boundary": "runtime_probe_research_only_no_runtime_authority",
            },
        )
    )
    artifacts.append(
        write_json(
            backtest_receipt,
            {
                "tester_identity": {
                    "terminal": str(args.terminal_path),
                    "terminal_extra_args": execution_result.get("terminal_extra_args", []),
                    "broker_terminal_data_root": str(args.terminal_data_root),
                    "terminal_process_probe": execution_result.get("terminal_process_probe", {}),
                    "symbol": "US100",
                    "timeframe": "M5",
                    "deposit": 500,
                    "leverage": "1:100",
                    "modeling_mode": "Every tick based on real ticks / MT5 model=4",
                    "date_range": sorted({f"{a['from_date']}..{a['to_date']}" for a in all_attempts}),
                },
                "ea_identity": {
                    "entrypoint": rel(mt5.EA_SOURCE_PATH),
                    "module_hashes": mt5.mt5_runtime_module_hashes(),
                    "set_files": [attempt["set"] for attempt in all_attempts],
                    "model_hashes": {row["artifact_slug"]: row["onnx_sha256"] for row in matrix_rows},
                },
                "report_identity": execution_result.get("strategy_tester_reports", []),
                "trade_evidence": execution_result.get("mt5_kpi_records", []),
                "cost_assumptions": {
                    "spread": "broker tester setting, not overwritten by run330E",
                    "commission": "broker tester setting, not overwritten by run330E",
                    "slippage": "InpDeviationPoints=default_or_set_file_value",
                    "swap": "broker tester setting",
                },
                "forensic_checks": [
                    "MetaEditor compile attempted before tester run.",
                    "Runtime telemetry and summary files are checked after tester run.",
                    "Strategy report artifacts are copied when MT5 emits them.",
                ],
                "backtest_judgment": "usable_with_boundary" if completed_count else "blocked",
            },
        )
    )
    artifacts.append(
        write_csv(
            result_path,
            [
                "run_id",
                "status",
                "judgment",
                "decision",
                "forward_passed",
                "forward_failed",
                "forward_blocked",
                "goal_achieve",
                "next_action",
                "claim_boundary",
            ],
            [
                {
                    "run_id": RUN_ID,
                    "status": status,
                    "judgment": judgment,
                    "decision": decision,
                    "forward_passed": "not_claimed",
                    "forward_failed": "not_claimed",
                    "forward_blocked": "claimed_for_this_run" if completed_count <= 0 else "not_claimed",
                    "goal_achieve": "not_claimed",
                    "next_action": next_action,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            ],
        )
    )
    artifacts.append(
        write_csv(
            gate_path,
            ["gate_name", "status", "evidence_path", "effect"],
            [
                {
                    "gate_name": "runtime_parity(런타임 동등성)",
                    "status": "completed" if completed_count else "blocked",
                    "evidence_path": rel(runtime_receipt),
                    "effect": "ONNX(온엑스), feature order(피처 순서), MT5 EA(메타트레이더5 전문가 자문) 입력 연결을 확인한다.",
                },
                {
                    "gate_name": "backtest_forensics(백테스트 포렌식)",
                    "status": "usable_with_boundary" if completed_count else "blocked",
                    "evidence_path": rel(backtest_receipt),
                    "effect": "tester identity(테스터 정체성), report path(보고서 경로), cost assumption(비용 가정)을 분리한다.",
                },
                {
                    "gate_name": "data_integrity(데이터 무결성)",
                    "status": "passed",
                    "evidence_path": rel(matrix_path),
                    "effect": "run330B raw_forward(원본 전진) timestamp(타임스탬프)와 run329B feature frame(피처 프레임)을 일치시킨다.",
                },
                {
                    "gate_name": "result_judgment(결과 판정)",
                    "status": "passed_no_goal_achieve",
                    "evidence_path": rel(result_path),
                    "effect": "Forward Passed/Failed(전진 통과/실패)와 Goal Achieve(목표 달성)를 올리지 않는다.",
                },
            ],
        )
    )
    lineage_artifacts = list(dict.fromkeys([*artifacts, Path(__file__)]))
    artifacts.append(
        write_json(
            lineage_path,
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "parent_run_id": PARENT_RUN_ID,
                "generated_at_utc": generated_at_utc,
                "source_inputs": [
                    rel(SIGNAL_MANIFEST),
                    rel(FIXED_SUMMARY),
                    rel(FEATURE_FRAME_DIR),
                    rel(FEATURE_ORDER_DIR),
                    rel(RUN329C_DIR / "onnx"),
                    rel(RUN330D_DIR / "run_manifest.json"),
                ],
                "artifact_paths": [rel(path) for path in lineage_artifacts if path_exists(path)],
                "artifact_hashes": {
                    rel(path): sha256_file(path)
                    for path in lineage_artifacts
                    if path_exists(path) and io_path(path).is_file()
                },
                "availability": "tracked_repo_artifacts_plus_local_common_files_copies",
                "lineage_judgment": "connected_with_runtime_probe_or_block_boundary",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
    )
    artifacts.append(
        write_json(
            manifest_path,
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "run_number": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "generated_at_utc": generated_at_utc,
                "status": status,
                "judgment": judgment,
                "decision": decision,
                "next_action": next_action,
                "external_verification_status": "attempted_mt5_runtime_or_block_recorded",
                "planned_attempt_count": len(all_attempts),
                "executed_attempt_count": len(executed_attempts),
                "completed_attempt_count": completed_count,
                "runtime_blockers": blockers,
                "terminal_process_probe_status": execution_result.get("terminal_process_probe", {}).get("status", ""),
                "terminal_extra_args": execution_result.get("terminal_extra_args", []),
                "execution_scope": {"start_index": int(args.start_index), "limit": args.limit},
                "selected_candidate": "none",
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "goal_achieve": "not_claimed",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
    )
    return artifacts


def markdown_attempt_table(rows: Sequence[dict[str, Any]]) -> str:
    lines = [
        "| attempt(시도) | candidate(후보) | tester(테스터) | runtime(런타임) | blocker(차단 사유) | model_ok(모델 성공) | orders(주문) | PF(수익 팩터) | trades(거래) |",
        "|---|---|---|---|---|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            "| {attempt_name} | {artifact_slug} | {tester_status} | {runtime_status} | {blocker} | {model_ok_count} | {order_fill_count} | {profit_factor} | {trade_count} |".format(
                **{key: row.get(key, "") for key in row}
            )
        )
    return "\n".join(lines)


def write_reports(status: str, judgment: str, decision: str, next_action: str, execution_result: Mapping[str, Any], artifacts: list[Path]) -> list[Path]:
    attempts = json.loads(io_path(RUN_DIR / "mt5_probe_attempts.json").read_text(encoding="utf-8"))
    rows = summary_rows(attempts, execution_result)
    completed_count = sum(1 for row in rows if row["tester_status"] == "completed" and row["runtime_status"] == "completed")
    blockers = ", ".join(runtime_blockers(execution_result)) or "none"
    final_decision = "Forward Blocked(전진 차단)" if completed_count <= 0 else "runtime_probe_evidence_available(런타임 탐침 근거 있음)"
    table = markdown_attempt_table(rows)
    report = REVIEWS_DIR / "run330E_raw_forward_mt5_runtime_probe_or_block.md"
    decision_report = REVIEWS_DIR / "final_stage330E_forward_decision_report.md"
    write_md(
        report,
        f"""
# Run330E Raw-Forward MT5 Runtime Probe Or Block(330E 원본 전진 MT5 런타임 탐침 또는 차단)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{status}`
- judgment(판정): `{judgment}`
- decision(결정): `{decision}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- blockers(차단 사유): `{blockers}`

## Scope(범위)

run330E(330E 실행)는 run330B(330B 실행)의 raw_forward(원본 전진) prediction timestamp(예측 타임스탬프), run329B(329B 실행)의 feature order(피처 순서), run329C(329C 실행)의 ONNX(온엑스)를 그대로 MT5(`MetaTrader 5`, 메타트레이더5) RuntimeProbeEA(런타임 탐침 EA) 입력으로 만든다.

Effect(효과): 새 학습, threshold retuning(임계값 재조정), D/B rule(D/B 규칙) 변경, lot optimization(로트 최적화) 없이 handoff(인계)와 tester execution(테스터 실행)만 검증한다.

## Attempt Summary(시도 요약)

{table}

## Boundary(경계)

- completed_attempt_count(완료 시도 수): `{completed_count}`
- runtime_authority(런타임 권위): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Next(다음)

`{next_action}`
""",
    )
    write_md(
        decision_report,
        f"""
# Stage330E Final Forward Decision Report(330E 최종 전진 판단 보고서)

- final_decision(최종 판단): `{final_decision}`
- status(상태): `{status}`
- judgment(판정): `{judgment}`
- completed_attempt_count(완료 시도 수): `{completed_count}`
- blockers(차단 사유): `{blockers}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Effect(효과): raw-forward MT5(원본 전진 MT5) 테스터 출력이 없으면 수익성, PF(수익 팩터), DD(낙폭), curve pocket(곡선 포켓)으로 통과/실패를 판정하지 않는다.

Next(다음): `{next_action}`
""",
    )
    write_md(
        DECISION_DOC,
        f"""
# 2026-05-26 Stage330E Raw-Forward MT5 Runtime Probe Decision(330E 원본 전진 MT5 런타임 탐침 결정)

- status(상태): `{status}`
- judgment(판정): `{judgment}`
- decision(결정): `{decision}`
- completed_attempt_count(완료 시도 수): `{completed_count}`
- blockers(차단 사유): `{blockers}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Reason(이유): raw-forward(원본 전진) handoff(인계)는 물질화했지만 MT5(메타트레이더5) external runtime check(외부 런타임 확인)는 completed_attempt_count(완료 시도 수)에만 의존한다.

Next(다음): `{next_action}`
""",
    )
    return [*artifacts, report, decision_report, DECISION_DOC]


def update_selection_status(status: str, judgment: str, next_action: str) -> Path:
    text, had_bom = read_text_lossless(SELECTION_STATUS)
    stage_status = "open_raw_forward_mt5_runtime_probe_blocked" if status == STATUS_BLOCKED else "open_raw_forward_mt5_runtime_probe_evidence_available"
    replacements = {
        "- stage_status(": f"- stage_status(단계 상태): `{stage_status}`",
        "- latest_completed_run(": f"- latest_completed_run(최신 완료 실행): `{RUN_ID if status != STATUS_BLOCKED else PARENT_RUN_ID}`",
        "- current_run(": f"- current_run(현재 실행): `{next_action}`",
        "- next_action(": f"- next_action(다음 행동): `{next_action}`",
        "- effect(": "- effect(효과): run330E(330E 실행)는 raw-forward MT5(원본 전진 MT5) 실행을 시도하거나 차단 근거를 남겼고, 선택 후보와 Forward Passed(전진 통과)는 없다.",
    }
    for prefix, replacement in replacements.items():
        text = replace_prefix_line(text, prefix, replacement)
    text = replace_prefix_line(text, "- research_onnx_status(", "- research_onnx_status(연구 온엑스 상태): `raw_forward_mt5_runtime_probe_attempted_no_selection`")
    return write_text_lossless(SELECTION_STATUS, text, had_bom)


def update_current_truth(status: str, judgment: str, next_action: str) -> list[Path]:
    updated: list[Path] = []
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_prefix_line(workspace_text, "current_run_id:", f"current_run_id: {next_action}")
    if "stage330E_raw_forward_mt5_runtime_probe:" not in workspace_text:
        workspace_text = workspace_text.rstrip() + f"""

stage330E_raw_forward_mt5_runtime_probe:
  run_id: {RUN_ID}
  status: {status}
  judgment: {judgment}
  decision: {DECISION_BLOCKED if status == STATUS_BLOCKED else DECISION_COMPLETED}
  next_action: {next_action}
  selected_candidate: none
  forward_passed: not_claimed
  forward_failed: not_claimed
  goal_achieve: not_claimed
  effect: raw_forward_mt5_runtime_probe_attempted_or_blocked_without_selection
"""
    updated.append(write_text_lossless(WORKSPACE_STATE, workspace_text, workspace_bom))

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    current_text = replace_prefix_line(current_text, "- current_run(", f"- current_run(현재 실행): `{next_action}`")
    current_text = replace_prefix_line(current_text, "- target_surface(", "- target_surface(목표 표면): `raw_forward_mt5_runtime_probe_or_block`")
    current_text = replace_prefix_line(current_text, "- status(", f"- status(상태): `{status}`")
    current_text = replace_prefix_line(current_text, "- decision(", f"- decision(판정): `{judgment}`")
    current_text = replace_prefix_line(current_text, "- next_action(", f"- next_action(다음 행동): `{next_action}`")
    summary = (
        f"- run330E_summary(330E 요약): raw-forward MT5 runtime probe(원본 전진 MT5 런타임 탐침)를 `{status}`로 기록했다. "
        "Effect(효과): threshold(임계값)과 D/B rule(D/B 규칙)은 고정했고, raw-forward MT5(원본 전진 MT5) 완료 근거 없이는 Forward Passed/Failed(전진 통과/실패)와 Goal Achieve(목표 달성)를 주장하지 않는다."
    )
    if "run330E_summary(330E 요약)" not in current_text:
        current_text = current_text.replace("- run330D_summary", summary + "\n- run330D_summary", 1)
    updated.append(write_text_lossless(CURRENT_STATE, current_text, current_bom))

    stage_block = f"""
## run330E_raw_forward_mt5_runtime_probe_summary(330E 원본 전진 MT5 런타임 탐침 요약)

- run(실행): `{RUN_ID}`
- status(상태): `{status}`
- judgment(판정): `{judgment}`
- next_action(다음 행동): `{next_action}`
- effect(효과): raw-forward(원본 전진) handoff(인계)를 MT5(메타트레이더5) 실행 입력으로 만들고, 실행이 막히면 차단 사유를 증거로 남긴다.
"""
    updated.append(append_if_missing(STAGE_BRIEF, "run330E_raw_forward_mt5_runtime_probe_summary", stage_block))
    changelog_entry = (
        f"- 2026-05-26: Stage330(330단계) `{RUN_ID}` raw-forward MT5 runtime probe(원본 전진 MT5 런타임 탐침)를 `{status}`로 기록했다. "
        "effect(효과): handoff(인계)와 tester blocker(테스터 차단 사유)를 분리했고 Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    updated.append(append_if_missing(CHANGELOG, RUN_ID, changelog_entry))
    return updated


def infer_artifact_type(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".json":
        return "json_receipt"
    if suffix == ".md":
        return "review_report"
    if suffix == ".py":
        return "pipeline_script"
    if suffix == ".set":
        return "mt5_set"
    if suffix == ".ini":
        return "mt5_ini"
    if suffix == ".log":
        return "compile_log"
    if suffix in {".yaml", ".yml"}:
        return "state_yaml"
    return "csv_report"


def update_registers(generated_at_utc: str, status: str, judgment: str, decision: str, next_action: str, artifacts: Sequence[Path]) -> None:
    report_path = REVIEWS_DIR / "run330E_raw_forward_mt5_runtime_probe_or_block.md"
    upsert_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "runtime_parity",
                "status": status,
                "judgment": judgment,
                "path": rel(report_path),
                "notes": "raw_forward_mt5_runtime_probe_or_block;no_threshold_retuning;goal_achieve_not_claimed.",
            }
        ],
    )
    upsert_csv(
        ALPHA_LEDGER,
        ["ledger_row_id"],
        [
            {
                "ledger_row_id": f"{RUN_ID}__raw_forward_runtime_probe",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "raw_forward_runtime_probe_or_block",
                "tier_scope": "latest_forward_raw_forward",
                "kpi_scope": "mt5_runtime_probe_and_tester_output_or_block",
                "scoreboard_lane": "runtime_parity",
                "status": status,
                "judgment": judgment,
                "path": rel(report_path),
                "primary_kpi": "completed_mt5_runtime_attempt_count",
                "guardrail_kpi": "no_threshold_retuning;selected_candidate=none;goal_achieve_not_claimed",
                "external_verification_status": "attempted_or_blocked_recorded_in_run_manifest",
                "notes": f"decision={decision};next_action={next_action}.",
            }
        ],
    )
    upsert_csv(
        STAGE_LEDGER,
        ["row_id"],
        [
            {
                "row_id": f"{RUN_ID}__raw_forward_runtime_probe",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "raw_forward_runtime_probe_or_block(원본 전진 런타임 탐침 또는 차단)",
                "tier_scope": "latest_forward_raw_forward(최신 전진 원본)",
                "scoreboard": "mt5_runtime_probe_and_forensics(MT5 런타임 탐침과 포렌식)",
                "status": status,
                "judgment": judgment,
                "evidence_boundary": CLAIM_BOUNDARY,
                "report_path": rel(report_path),
                "notes": "no_candidate_selection;no_forward_pass_fail;goal_achieve_not_claimed.",
                "decision": decision,
            }
        ],
    )
    artifact_rows: list[dict[str, Any]] = []
    for artifact in artifacts:
        if not path_exists(artifact) or io_path(artifact).is_dir():
            continue
        artifact_rows.append(
            {
                "artifact_id": f"{RUN_ID}__{artifact.stem}__{artifact.suffix.lstrip('.').lower() or 'file'}".replace("-", "_"),
                "artifact_type": infer_artifact_type(artifact),
                "path": rel(artifact),
                "sha256": sha256_file(artifact),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": generated_at_utc,
                "notes": "Stage330E raw-forward MT5 runtime probe or block artifact; no Forward Passed/Failed claim.",
            }
        )
    upsert_csv(ARTIFACT_REGISTRY, ["path", "run_id"], artifact_rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Stage330E raw-forward MT5 runtime probe or record a block.")
    parser.add_argument("--terminal-path", default=str(TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=str(METAEDITOR_PATH_DEFAULT))
    parser.add_argument("--terminal-data-root", default=str(TERMINAL_DATA_ROOT_DEFAULT))
    parser.add_argument("--common-files-root", default=str(COMMON_FILES_ROOT_DEFAULT))
    parser.add_argument("--tester-profile-root", default=str(TESTER_PROFILE_ROOT_DEFAULT))
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--runtime-timeout-seconds", type=int, default=180)
    parser.add_argument("--terminal-extra-arg", action="append", default=[])
    parser.add_argument("--start-index", type=int, default=0)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--materialize-only", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    generated_at_utc = utc_now()
    for directory in (RUN_DIR, FEATURE_MATRIX_DIR, MT5_DIR, REVIEWS_DIR, SELECTED_DIR):
        directory.mkdir(parents=True, exist_ok=True)

    common_files_root = Path(args.common_files_root)
    all_attempts, matrix_rows, materialized_artifacts = build_materialized_attempts(common_files_root)
    executed_attempts = selected_attempts(all_attempts, args.start_index, args.limit)
    if args.materialize_only:
        execution_result: dict[str, Any] = {
            "compile": {"status": "not_attempted_materialize_only"},
            "terminal_process_probe": {},
            "execution_results": [],
            "strategy_tester_reports": [],
            "mt5_kpi_records": [],
        }
    else:
        execution_result = execute_attempts(
            executed_attempts,
            terminal_path=Path(args.terminal_path),
            metaeditor_path=Path(args.metaeditor_path),
            terminal_data_root=Path(args.terminal_data_root),
            common_files_root=common_files_root,
            tester_profile_root=Path(args.tester_profile_root),
            timeout_seconds=int(args.timeout_seconds),
            runtime_timeout_seconds=int(args.runtime_timeout_seconds),
            terminal_extra_args=list(args.terminal_extra_arg or []),
        )
    status, judgment, decision, next_action = classify(all_attempts, executed_attempts, execution_result, args.materialize_only)
    artifacts = write_run_artifacts(
        generated_at_utc,
        all_attempts,
        executed_attempts,
        matrix_rows,
        execution_result,
        status,
        judgment,
        decision,
        next_action,
        args,
        materialized_artifacts,
    )
    artifacts = write_reports(status, judgment, decision, next_action, execution_result, artifacts)
    artifacts.extend([update_selection_status(status, judgment, next_action), *update_current_truth(status, judgment, next_action)])
    update_registers(generated_at_utc, status, judgment, decision, next_action, [*artifacts, Path(__file__)])
    print(
        json.dumps(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "status": status,
                "judgment": judgment,
                "decision": decision,
                "planned_attempt_count": len(all_attempts),
                "executed_attempt_count": len(executed_attempts),
                "completed_attempt_count": sum(1 for row in execution_result.get("execution_results", []) if row.get("status") == "completed"),
                "runtime_blockers": runtime_blockers(execution_result),
                "selected_candidate": "none",
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_action": next_action,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
