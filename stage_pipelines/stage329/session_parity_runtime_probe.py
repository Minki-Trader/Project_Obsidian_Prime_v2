from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import shutil
import subprocess
import sys
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


STAGE_ID = "329_onnx_rebuild__live_feature_control"
RUN_ID = "run329E_session_parity_forward_signal_payload_and_mt5_runtime_probe_v1"
RUN_NUMBER = "run329E"
PARENT_RUN_ID = "run329D_forward_holdout_score_replay_without_threshold_retuning_v1"
EXPLORATION_LABEL = "stage329_Runtime__SessionParityForwardProbe"

STATUS_COMPLETED = "completed_session_parity_runtime_probe_no_candidate_selection"
STATUS_PARTIAL = "partial_session_parity_runtime_probe_completed_subset_no_candidate_selection"
STATUS_BLOCKED = "blocked_session_parity_runtime_probe_no_completed_mt5_runtime"
JUDGMENT_COMPLETED = "runtime_probe_completed_research_only_no_goal_achieve"
JUDGMENT_BLOCKED = "runtime_probe_blocked_requires_runtime_repair_no_goal_achieve"
DECISION_COMPLETED = "stage329E_mt5_runtime_probe_evidence_available_review_required_no_selection"
DECISION_BLOCKED = "stage329E_mt5_runtime_probe_blocked_no_forward_pass_fail_judgment"
NEXT_COMPLETED = "run329F_forward_mt5_kpi_regime_cost_curve_review"
NEXT_PARTIAL = "run329E_continue_remaining_runtime_probe_or_repair"
NEXT_BLOCKED = "repair_stage329E_runtime_probe_blocker_then_rerun"
CLAIM_BOUNDARY = (
    "research_development_only_session_parity_mt5_runtime_probe_no_threshold_retuning_"
    "no_selected_candidate_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)
COMMON_ROOT = "Project_Obsidian_Prime_v2/stage329/run329E_session_parity_runtime_probe"
SPLIT_LABEL = "forward_old_session_parity"
MAX_HOLD_BARS = 12

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
FEATURE_MATRIX_DIR = RUN_DIR / "feature_matrices"
MT5_DIR = RUN_DIR / "mt5"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
RUN329B_DIR = STAGE_DIR / "02_runs" / "run329B"
RUN329C_DIR = STAGE_DIR / "02_runs" / "run329C"
RUN329D_DIR = STAGE_DIR / "02_runs" / "run329D"
FEATURE_FRAME_DIR = RUN329B_DIR / "feature_frames"
FEATURE_ORDER_DIR = RUN329B_DIR / "feature_orders"
QUEUE_PATH = RUN329C_DIR / "forward_replay_candidate_queue.csv"
FORWARD_SCORE_SUMMARY = RUN329D_DIR / "forward_score_summary.csv"
PREDICTION_DIR = RUN329D_DIR / "predictions"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-26_stage329E_session_parity_runtime_probe.md"


def os_path(path: Path) -> Path:
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
    return os_path(path).exists()


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with os_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def json_ready(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): json_ready(val) for key, val in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, Path):
        return value.as_posix()
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    if isinstance(value, np.bool_):
        return bool(value)
    return value


def write_text(path: Path, text: str, encoding: str = "utf-8") -> Path:
    os_path(path.parent).mkdir(parents=True, exist_ok=True)
    os_path(path).write_bytes(text.encode(encoding))
    return path


def write_md(path: Path, text: str) -> Path:
    return write_text(path, text.strip() + "\n", encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> Path:
    return write_text(path, json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n")


def write_csv(path: Path, fieldnames: Sequence[str], rows: Iterable[Mapping[str, Any]]) -> Path:
    os_path(path.parent).mkdir(parents=True, exist_ok=True)
    with os_path(path).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})
    return path


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path_exists(path):
        return [], []
    with os_path(path).open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def upsert_csv(path: Path, keys: Sequence[str], new_rows: Sequence[Mapping[str, Any]]) -> None:
    fieldnames, rows = read_csv_rows(path)
    for row in new_rows:
        for name in row:
            if name not in fieldnames:
                fieldnames.append(name)
    if not fieldnames and new_rows:
        fieldnames = list(new_rows[0].keys())

    def key_of(row: Mapping[str, Any]) -> tuple[str, ...]:
        return tuple(str(row.get(key, "")) for key in keys)

    replacements = {key_of(row): {name: str(row.get(name, "")) for name in fieldnames} for row in new_rows}
    output: list[dict[str, str]] = []
    seen: set[tuple[str, ...]] = set()
    for row in rows:
        row_key = key_of(row)
        if row_key in replacements:
            output.append(replacements[row_key])
            seen.add(row_key)
        else:
            output.append({name: str(row.get(name, "")) for name in fieldnames})
    for row_key, row in replacements.items():
        if row_key not in seen:
            output.append(row)
    write_csv(path, fieldnames, output)


def read_text_lossless(path: Path) -> tuple[str, bool]:
    raw = os_path(path).read_bytes()
    had_bom = raw.startswith(b"\xef\xbb\xbf")
    return raw.decode("utf-8-sig"), had_bom


def write_text_lossless(path: Path, text: str, had_bom: bool) -> Path:
    return write_text(path, text, encoding="utf-8-sig" if had_bom else "utf-8")


def replace_prefix_line(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text.rstrip() + "\n" + replacement + "\n"


def append_if_missing(path: Path, marker: str, entry: str) -> Path:
    text, had_bom = read_text_lossless(path) if path_exists(path) else ("", False)
    if marker in text:
        return path
    text = text.rstrip() + "\n\n" + entry.strip() + "\n"
    return write_text_lossless(path, text, had_bom)


def mt5_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return f"{value:.12g}"
    return str(value)


def write_set(path: Path, values: Mapping[str, Any]) -> dict[str, Any]:
    lines = ["; generated_by=stage_pipelines.stage329.session_parity_runtime_probe"]
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
    return [line.strip() for line in os_path(path).read_text(encoding="utf-8").splitlines() if line.strip()]


def load_queue() -> list[dict[str, str]]:
    _, rows = read_csv_rows(QUEUE_PATH)
    if not rows:
        raise RuntimeError(f"empty forward replay candidate queue: {QUEUE_PATH}")
    return rows


def prediction_path(slug: str) -> Path:
    return PREDICTION_DIR / f"{slug}_old_session_parity_score.parquet"


def tester_dates(timestamps: pd.Series) -> tuple[str, str]:
    start = pd.to_datetime(timestamps, utc=True).min().date()
    end = pd.to_datetime(timestamps, utc=True).max().date() + timedelta(days=1)
    return start.strftime("%Y.%m.%d"), end.strftime("%Y.%m.%d")


def export_feature_matrix_csv(
    frame: pd.DataFrame,
    features: Sequence[str],
    output_path: Path,
) -> dict[str, Any]:
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
    output = pd.concat(
        [output, pd.DataFrame(values.astype("float32"), columns=list(features))],
        axis=1,
    )
    os_path(output_path.parent).mkdir(parents=True, exist_ok=True)
    output.to_csv(os_path(output_path), index=False, encoding="utf-8", float_format="%.10g", lineterminator="\n")
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
    os_path(destination.parent).mkdir(parents=True, exist_ok=True)
    shutil.copy2(os_path(local_path), os_path(destination))
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
    for row in load_queue():
        slug = row["artifact_slug"]
        candidate_id = row["candidate_id"]
        feature_set_id = row["feature_set_id"]
        features = load_feature_order(feature_set_id)
        frame = pd.read_parquet(os_path(FEATURE_FRAME_DIR / f"{feature_set_id}.parquet"))
        frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
        prediction = pd.read_parquet(os_path(prediction_path(slug)))
        prediction["timestamp"] = pd.to_datetime(prediction["timestamp"], utc=True)
        timestamps = pd.Index(prediction["timestamp"])
        view_frame = frame.loc[frame["timestamp"].isin(timestamps)].copy()
        view_frame = view_frame.sort_values("timestamp").reset_index(drop=True)
        prediction = prediction.sort_values("timestamp").reset_index(drop=True)
        if len(view_frame) != len(prediction):
            raise RuntimeError(f"{slug} feature/prediction row mismatch: {len(view_frame)} != {len(prediction)}")
        if not view_frame["timestamp"].reset_index(drop=True).equals(prediction["timestamp"].reset_index(drop=True)):
            raise RuntimeError(f"{slug} feature/prediction timestamp mismatch")

        feature_csv = FEATURE_MATRIX_DIR / f"{slug}_old_session_parity_features.csv"
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
        threshold = float(row["decision_threshold"])
        attempt_name = f"{slug}_sp"
        telemetry = f"{COMMON_ROOT}/telemetry/{attempt_name}_telemetry.csv"
        summary = f"{COMMON_ROOT}/telemetry/{attempt_name}_summary.csv"
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
            "InpFeatureOrderHash": ordered_hash(features),
            "InpFallbackEnabled": "false",
            "InpFallbackFeatureCsvPath": feature_common_path,
            "InpFallbackFeatureCount": len(features),
            "InpFallbackModelPath": model_common_path,
            "InpFallbackModelId": f"{RUN_ID}_{slug}_onnx",
            "InpFallbackModelBackend": "onnx",
            "InpFallbackFeatureOrderHash": ordered_hash(features),
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
            "InpMagic": 3290100 + len(attempts),
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
                "model_id": row["model_id"],
                "tier": TIER_A,
                "split": SPLIT_LABEL,
                "attempt_role": "session_parity_tier_only_total",
                "record_view_prefix": f"mt5_{slug}_session_parity",
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
                "decision_surface_mapping": "stage329D_pred_nonflat_and_probability_margin>=threshold_reproduced_as_min_margin_only",
                "routing_mode": "tier_a_primary_no_fallback",
                "signal_policy": "old_session_parity ONNX probabilities with fixed train-only margin threshold; no forward retuning",
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
            os_path(path).unlink()


def terminal_runtime_output_snapshot(
    common_files_root: Path,
    attempt: Mapping[str, Any],
    *,
    status: str,
    wait_status: str,
) -> dict[str, Any]:
    telemetry_path = common_files_root / Path(str(attempt["common_telemetry_path"]))
    summary_path = common_files_root / Path(str(attempt["common_summary_path"]))
    return {
        "telemetry_path": str(telemetry_path),
        "summary_path": str(summary_path),
        "telemetry_exists": path_exists(telemetry_path),
        "summary_exists": path_exists(summary_path),
        "status": status,
        "wait_status": wait_status,
    }


def detect_running_terminal_processes(terminal_path: Path) -> dict[str, Any]:
    command = [
        "powershell",
        "-NoProfile",
        "-Command",
        (
            "$ErrorActionPreference='SilentlyContinue'; "
            "Get-CimInstance Win32_Process -Filter \"name = 'terminal64.exe'\" | "
            "Select-Object ProcessId,ExecutablePath,CommandLine | ConvertTo-Json -Compress"
        ),
    ]
    try:
        proc = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=10)
    except Exception as exc:  # pragma: no cover - host process inspection boundary
        return {
            "status": "detection_failed",
            "command": command,
            "error_type": type(exc).__name__,
            "error": str(exc),
            "processes": [],
        }

    raw = proc.stdout.strip()
    rows: list[Any]
    if not raw:
        rows = []
    else:
        try:
            parsed = json.loads(raw)
            rows = parsed if isinstance(parsed, list) else [parsed]
        except json.JSONDecodeError:
            return {
                "status": "detection_failed",
                "command": command,
                "returncode": proc.returncode,
                "stdout": proc.stdout,
                "stderr": proc.stderr,
                "processes": [],
            }

    target = str(terminal_path).lower()
    processes: list[dict[str, Any]] = []
    matching: list[dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, Mapping):
            continue
        item = {
            "process_id": row.get("ProcessId"),
            "executable_path": row.get("ExecutablePath"),
            "command_line": row.get("CommandLine"),
        }
        processes.append(item)
        executable = str(item.get("executable_path") or "").lower()
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
            tester_profile_ini_path = tester_profile_root / f"opv2_s329e_{attempt['attempt_name']}.ini"
            if terminal_process_probe.get("status") == "running":
                result = {
                    "status": "blocked",
                    "command": [
                        str(terminal_path),
                        *terminal_extra_args,
                        f"/config:{tester_profile_ini_path}",
                    ],
                    "returncode": None,
                    "blocker": "terminal_already_running_config_not_applied",
                    "blocker_explanation": (
                        "An already running terminal64.exe process can absorb a /config launch "
                        "without starting the requested strategy tester configuration."
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
                except Exception as exc:  # pragma: no cover - external MT5 defensive boundary
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
    kpi_records = build_mt5_kpi_records(execution_results)
    return {
        "compile": compile_payload,
        "terminal_process_probe": terminal_process_probe,
        "terminal_extra_args": list(terminal_extra_args),
        "execution_results": execution_results,
        "strategy_tester_reports": report_records,
        "mt5_kpi_records": kpi_records,
    }


def classify(
    attempts: Sequence[dict[str, Any]],
    executed_attempts: Sequence[dict[str, Any]],
    execution_result: Mapping[str, Any],
    materialize_only: bool,
) -> tuple[str, str, str, str]:
    if materialize_only:
        return STATUS_BLOCKED, "materialized_only_no_external_runtime_execution", DECISION_BLOCKED, NEXT_BLOCKED
    execution_results = list(execution_result.get("execution_results", []))
    completed = sum(1 for row in execution_results if row.get("status") == "completed")
    if completed <= 0:
        return STATUS_BLOCKED, JUDGMENT_BLOCKED, DECISION_BLOCKED, NEXT_BLOCKED
    if completed < len(attempts) or len(executed_attempts) < len(attempts):
        return STATUS_PARTIAL, JUDGMENT_COMPLETED, DECISION_COMPLETED, NEXT_PARTIAL
    return STATUS_COMPLETED, JUDGMENT_COMPLETED, DECISION_COMPLETED, NEXT_COMPLETED


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


def runtime_blockers(execution_result: Mapping[str, Any]) -> list[str]:
    blockers = {
        str(row.get("blocker"))
        for row in execution_result.get("execution_results", [])
        if row.get("blocker")
    }
    return sorted(blockers)


def copy_runtime_telemetry_artifacts(common_files_root: Path, attempts: Sequence[dict[str, Any]]) -> list[Path]:
    telemetry_dir = RUN_DIR / "mt5" / "telemetry"
    os_path(telemetry_dir).mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []
    artifacts: list[Path] = []
    for attempt in attempts:
        for kind, key in (("telemetry", "common_telemetry_path"), ("summary", "common_summary_path")):
            source = common_files_root / Path(str(attempt[key]))
            destination = telemetry_dir / f"{attempt['attempt_name']}_{kind}.csv"
            row = {
                "attempt_name": attempt["attempt_name"],
                "artifact_kind": kind,
                "source_path": str(source),
                "repo_path": rel(destination),
                "status": "missing",
                "sha256": "",
            }
            if path_exists(source):
                shutil.copy2(os_path(source), os_path(destination))
                row["status"] = "copied"
                row["sha256"] = sha256_file(destination)
                artifacts.append(destination)
            rows.append(row)
    manifest = RUN_DIR / "mt5_runtime_telemetry_artifacts.csv"
    write_csv(manifest, ["attempt_name", "artifact_kind", "source_path", "repo_path", "status", "sha256"], rows)
    return [manifest, *artifacts]


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
    matrix_path = RUN_DIR / "session_parity_feature_matrix_manifest.csv"
    write_csv(
        matrix_path,
        [
            "candidate_id",
            "artifact_slug",
            "feature_set_id",
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
            "common_feature_path",
            "common_model_path",
        ],
        matrix_rows,
    )
    artifacts.append(matrix_path)

    attempt_path = RUN_DIR / "mt5_probe_attempts.json"
    write_json(attempt_path, list(all_attempts))
    artifacts.append(attempt_path)
    execution_path = RUN_DIR / "execution_result.json"
    write_json(execution_path, execution_result)
    artifacts.append(execution_path)
    summary_path = RUN_DIR / "mt5_runtime_probe_summary.csv"
    rows = summary_rows(all_attempts, execution_result)
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
        rows,
    )
    artifacts.append(summary_path)
    kpi_path = RUN_DIR / "mt5_kpi_records.json"
    write_json(kpi_path, execution_result.get("mt5_kpi_records", []))
    artifacts.append(kpi_path)
    telemetry_artifacts = copy_runtime_telemetry_artifacts(Path(args.common_files_root), all_attempts)
    artifacts.extend(telemetry_artifacts)

    runtime_receipt = RUN_DIR / "runtime_parity_receipt.json"
    completed_count = sum(1 for row in execution_result.get("execution_results", []) if row.get("status") == "completed")
    blockers = runtime_blockers(execution_result)
    write_json(
        runtime_receipt,
        {
            "research_path": rel(Path(__file__)),
            "runtime_path": rel(mt5.EA_SOURCE_PATH),
            "shared_contract": {
                "model": "run329C ONNX candidates",
                "feature_input": "run329B feature order, run329D old_session_parity timestamps",
                "decision_surface": "Stage329D nonflat prediction and fixed margin threshold mapped to MT5 min_margin only",
                "risk_lot": "fixed lot 0.1, max hold 12 bars, no ATR SLTP, no model risk sizing",
            },
            "known_differences": [
                "MT5 tester skips bars not present in the session-parity feature CSV.",
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
    artifacts.append(runtime_receipt)

    backtest_receipt = RUN_DIR / "backtest_forensics_receipt.json"
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
                "spread": "broker tester setting, not overwritten by run329E",
                "commission": "broker tester setting, not overwritten by run329E",
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
    artifacts.append(backtest_receipt)

    result_path = RUN_DIR / "result_judgment.csv"
    write_csv(
        result_path,
        ["run_id", "status", "judgment", "decision", "goal_achieve", "next_action", "claim_boundary"],
        [
            {
                "run_id": RUN_ID,
                "status": status,
                "judgment": judgment,
                "decision": decision,
                "goal_achieve": "not_claimed",
                "next_action": next_action,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    artifacts.append(result_path)

    gate_path = RUN_DIR / "required_gate_coverage_audit.csv"
    write_csv(
        gate_path,
        ["gate_name", "status", "evidence_path", "effect"],
        [
            {
                "gate_name": "runtime_parity(런타임 동등성)",
                "status": "completed" if completed_count else "blocked",
                "evidence_path": rel(runtime_receipt),
                "effect": "Python/ONNX(파이썬/온엑스) 점수에서 MT5 RuntimeProbeEA(런타임 탐침 EA) 입력으로 넘어가는지 확인한다.",
            },
            {
                "gate_name": "backtest_forensics(백테스트 포렌식)",
                "status": "usable_with_boundary" if completed_count else "blocked",
                "evidence_path": rel(backtest_receipt),
                "effect": "tester identity(테스터 정체성), report path(보고서 경로), cost assumption(비용 가정)을 성공 주장과 분리한다.",
            },
            {
                "gate_name": "artifact_lineage(산출물 계보)",
                "status": "passed",
                "evidence_path": rel(RUN_DIR / "artifact_lineage_receipt.json"),
                "effect": "run329B/run329C/run329D 입력과 run329E MT5 산출물을 연결한다.",
            },
            {
                "gate_name": "result_judgment(결과 판정)",
                "status": "passed_no_goal_achieve",
                "evidence_path": rel(result_path),
                "effect": "runtime_probe(런타임 탐침)를 runtime_authority(런타임 권위)나 Goal Achieve(목표 달성)로 올리지 않는다.",
            },
        ],
    )
    artifacts.append(gate_path)

    lineage_path = RUN_DIR / "artifact_lineage_receipt.json"
    lineage_artifacts = list(dict.fromkeys([*artifacts, Path(__file__)]))
    write_json(
        lineage_path,
        {
            "source_inputs": [
                rel(QUEUE_PATH),
                rel(FEATURE_FRAME_DIR),
                rel(RUN329C_DIR / "onnx"),
                rel(PREDICTION_DIR),
                rel(FORWARD_SCORE_SUMMARY),
            ],
            "producer": rel(Path(__file__)),
            "consumer": next_action,
            "artifact_paths": [rel(path) for path in lineage_artifacts if path_exists(path)],
            "artifact_hashes": {rel(path): sha256_file(path) for path in lineage_artifacts if path_exists(path) and os_path(path).is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(ARTIFACT_REGISTRY), rel(STAGE_LEDGER)],
            "availability": "tracked_repo_artifacts_plus_local_common_files_copies",
            "lineage_judgment": "connected_with_runtime_probe_boundary",
        },
    )
    artifacts.append(lineage_path)

    manifest_path = RUN_DIR / "run_manifest.json"
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
            "goal_achieve": "not_claimed",
            "planned_attempt_count": len(all_attempts),
            "executed_attempt_count": len(executed_attempts),
            "completed_attempt_count": completed_count,
            "runtime_blockers": blockers,
            "terminal_process_probe_status": execution_result.get("terminal_process_probe", {}).get("status", ""),
            "terminal_extra_args": execution_result.get("terminal_extra_args", []),
            "execution_scope": {"start_index": int(args.start_index), "limit": args.limit},
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    artifacts.append(manifest_path)
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
    rows = summary_rows(json.loads(os_path(RUN_DIR / "mt5_probe_attempts.json").read_text(encoding="utf-8")), execution_result)
    completed_count = sum(1 for row in rows if row["tester_status"] == "completed" and row["runtime_status"] == "completed")
    blockers = ", ".join(runtime_blockers(execution_result)) or "none"
    table = markdown_attempt_table(rows)
    report = REVIEWS_DIR / "run329E_session_parity_runtime_probe.md"
    write_md(
        report,
        f"""
# run329E Session Parity Runtime Probe(329E 세션 동등 런타임 탐침)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{status}`
- judgment(판정): `{judgment}`
- selected_candidate(선택 후보): `none`
- goal_achieve(목표 달성): `not_claimed`
- blockers(차단 사유): `{blockers}`

## Scope(범위)

run329E(329E 실행)는 run329D(329D 실행)의 old_session_parity(기존 세션 동등) prediction(예측) timestamp(타임스탬프)를 그대로 써서 MT5(`MetaTrader 5`, 메타트레이더5) RuntimeProbeEA(런타임 탐침 EA) 입력을 만들었다.

Effect(효과): 새 threshold(임계값), 새 decision rule(판단 규칙), 새 lot/risk optimization(랏/위험 최적화)을 만들지 않고, Python/ONNX(파이썬/온엑스) 점수가 MT5 RuntimeProbeEA(런타임 탐침 EA)에서 읽히는지 확인한다.

## Attempt Summary(시도 요약)

{table}

## Boundary(경계)

- completed_attempt_count(완료 시도 수): `{completed_count}`
- runtime_authority(런타임 권위): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- Forward Passed(전진 통과): `not_claimed`
- effect(효과): tester output(테스터 출력)이 있더라도 다음 run329F(329F 실행)에서 KPI(핵심 성과 지표), curve pocket(곡선 포켓), regime/cost slice(국면/비용 구간)를 다시 판독해야 한다.

`{CLAIM_BOUNDARY}`

## Next(다음)

`{next_action}`
""",
    )
    final_report = REVIEWS_DIR / "final_stage329E_decision_report.md"
    write_md(
        final_report,
        f"""
# Stage329E Final Decision(329E 최종 판정)

- decision(결정): `{decision}`
- status(상태): `{status}`
- judgment(판정): `{judgment}`
- completed_attempt_count(완료 시도 수): `{completed_count}`
- blockers(차단 사유): `{blockers}`
- selected_candidate(선택 후보): `none`
- goal_achieve(목표 달성): `not_claimed`
- effect(효과): run329E(329E 실행)는 runtime probe(런타임 탐침) 단계다. 수익성이나 forward pass(전진 통과)를 아직 닫지 않는다.
- next_action(다음 행동): `{next_action}`
""",
    )
    write_md(
        DECISION_DOC,
        f"""
# 2026-05-26 Stage329E Session Parity Runtime Probe Decision(329E 세션 동등 런타임 탐침 결정)

- status(상태): `{status}`
- judgment(판정): `{judgment}`
- decision(결정): `{decision}`
- effect(효과): old_session_parity(기존 세션 동등) 입력을 MT5 RuntimeProbeEA(런타임 탐침 EA)에 넘기는 외부 검증을 시도했다.
- goal_achieve(목표 달성): `not_claimed`
- blockers(차단 사유): `{blockers}`
- next_action(다음 행동): `{next_action}`
""",
    )
    return [*artifacts, report, final_report, DECISION_DOC]


def update_selection_status(status: str, judgment: str, next_action: str) -> Path:
    selection = SELECTED_DIR / "selection_status.md"
    _, matrix_rows = read_csv_rows(RUN_DIR / "session_parity_feature_matrix_manifest.csv")
    queue = ", ".join(row["candidate_id"] for row in matrix_rows)
    return write_md(
        selection,
        f"""
# Stage329 Selection Status(329단계 선택 상태)

- selected_candidate(선택 후보): `none`
- cp322A_status(cp322A 상태): `research_artifact_preserved_not_forward_authority`
- source_feature_frame_queue(원천 피처 프레임 대기열): `core56_no_top3_weight_features, macro48_no_equity_breadth_or_top3, us100_technical42_no_external`
- research_onnx_status(연구 온엑스 상태): `session_parity_mt5_runtime_probe_attempted_not_runtime_authority`
- forward_replay_queue(전진 재생 대기열): `{queue}`
- forward_score_replay_status(전진 점수 재생 상태): `completed_forward_holdout_score_replay_without_threshold_retuning`
- session_parity_runtime_probe_status(세션 동등 런타임 탐침 상태): `{status}`
- session_parity_runtime_probe_judgment(세션 동등 런타임 탐침 판정): `{judgment}`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{next_action}`
- effect(효과): MT5/runtime(메타트레이더5/런타임) 검증은 시작했지만, 아직 후보 선택이나 forward passed(전진 통과) 판정은 없다.
""",
    )


def update_current_truth(status: str, judgment: str, next_action: str) -> list[Path]:
    updated: list[Path] = []
    workspace = WORKSPACE_STATE
    text, had_bom = read_text_lossless(workspace)
    text = replace_prefix_line(text, "current_run_id:", f"current_run_id: {RUN_ID}")
    focus = (
        "- >-\n"
        f"  Stage329(329단계) run329E(329E 실행) session parity runtime probe(세션 동등 런타임 탐침)를 `{status}`로 기록했다. "
        "Effect(효과): old_session_parity(기존 세션 동등) 입력을 MT5 RuntimeProbeEA(런타임 탐침 EA)에 넘겼지만 Goal Achieve(목표 달성)는 없다.\n"
    )
    if "Stage329(329단계) run329E(329E 실행)" not in text:
        text = text.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    write_text_lossless(workspace, text, had_bom)
    updated.append(workspace)

    current = CURRENT_STATE
    text, had_bom = read_text_lossless(current)
    replacements = {
        "- current_packet(": f"- current_packet(현재 작업 묶음): `{STAGE_ID}_v5`",
        "- current_run(": f"- current_run(현재 실행): `{RUN_ID}`",
        "- active_stage(": f"- active_stage(활성 단계): `{STAGE_ID}`",
        "- selected_research_baseline(": "- selected_research_baseline(선택 연구 기준선): `none`",
        "- source_stage(": "- source_stage(원천 단계): `329_onnx_rebuild__live_feature_control`",
        "- target_surface(": "- target_surface(목표 표면): `session_parity_mt5_runtime_probe`",
        "- adapter_under_review(": "- adapter_under_review(검토 중 어댑터): `none`",
        "- status(": f"- status(상태): `{status}`",
        "- decision(": f"- decision(판정): `{judgment}`",
        "- next_action(": f"- next_action(다음 행동): `{next_action}`",
        "- claim_boundary(": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    }
    for prefix, replacement in replacements.items():
        text = replace_prefix_line(text, prefix, replacement)
    summary = (
        f"- run329E_summary(329E 요약): session parity runtime probe(세션 동등 런타임 탐침)를 `{status}`로 기록했다. "
        "Effect(효과): run329D(329D 실행)의 old_session_parity(기존 세션 동등) 신호를 MT5 RuntimeProbeEA(런타임 탐침 EA) 입력으로 물질화하고 외부 검증을 시도했지만, selected candidate(선택 후보), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 없다."
    )
    if "run329E_summary(329E 요약)" not in text:
        text = text.replace(f"- decision(판정): `{judgment}`\n", f"- decision(판정): `{judgment}`\n{summary}\n", 1)
    write_text_lossless(current, text, had_bom)
    updated.append(current)

    append_if_missing(
        CHANGELOG,
        "Stage329E Session Parity Runtime Probe",
        f"""
## 2026-05-26 - Stage329E Session Parity Runtime Probe(329E 세션 동등 런타임 탐침)

- run329E(329E 실행): run329D(329D 실행)의 old_session_parity(기존 세션 동등) prediction(예측)을 MT5 RuntimeProbeEA(런타임 탐침 EA) 입력으로 만들고 외부 실행을 시도했다.
- status(상태): `{status}`
- judgment(판정): `{judgment}`
- effect(효과): runtime probe(런타임 탐침)까지만 주장하고, selected candidate(선택 후보), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.
""",
    )
    updated.append(CHANGELOG)
    return updated


def update_registers(generated_at_utc: str, status: str, judgment: str, decision: str, next_action: str, artifacts: Sequence[Path]) -> None:
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
                "path": rel(REVIEWS_DIR / "run329E_session_parity_runtime_probe.md"),
                "notes": "session_parity_mt5_runtime_probe;no_threshold_retuning;goal_achieve_not_claimed.",
            }
        ],
    )
    upsert_csv(
        ALPHA_LEDGER,
        ["ledger_row_id"],
        [
            {
                "ledger_row_id": f"{RUN_ID}__session_parity_runtime_probe",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "session_parity_runtime_probe",
                "tier_scope": "forward old-session parity",
                "kpi_scope": "mt5_runtime_probe_and_tester_output",
                "scoreboard_lane": "runtime_parity",
                "status": status,
                "judgment": judgment,
                "path": rel(REVIEWS_DIR / "run329E_session_parity_runtime_probe.md"),
                "primary_kpi": "completed_mt5_runtime_attempt_count",
                "guardrail_kpi": "no_threshold_retuning;selected_candidate=none;goal_achieve_not_claimed",
                "external_verification_status": "completed_or_blocked_recorded_in_run_manifest",
                "notes": f"decision={decision};next_action={next_action}.",
            }
        ],
    )
    upsert_csv(
        STAGE_LEDGER,
        ["row_id"],
        [
            {
                "row_id": f"{RUN_ID}__session_parity_runtime_probe",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "session_parity_runtime_probe(세션 동등 런타임 탐침)",
                "tier_scope": "forward old-session parity(전진 기존 세션 동등)",
                "scoreboard": "mt5_runtime_probe_and_forensics(MT5 런타임 탐침과 포렌식)",
                "status": status,
                "judgment": judgment,
                "evidence_boundary": CLAIM_BOUNDARY,
                "report_path": rel(REVIEWS_DIR / "run329E_session_parity_runtime_probe.md"),
                "notes": "no_candidate_selected;goal_achieve_not_claimed.",
                "decision": decision,
            }
        ],
    )
    artifact_rows: list[dict[str, Any]] = []
    for artifact in artifacts:
        if not path_exists(artifact) or os_path(artifact).is_dir():
            continue
        artifact_rows.append(
            {
                "artifact_id": f"{RUN_ID}__{artifact.stem}".replace("-", "_"),
                "artifact_type": artifact.suffix.lstrip(".") or "file",
                "path": rel(artifact),
                "sha256": sha256_file(artifact),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": generated_at_utc,
                "notes": status,
            }
        )
    upsert_csv(ARTIFACT_REGISTRY, ["artifact_id", "run_id"], artifact_rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
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
        os_path(directory).mkdir(parents=True, exist_ok=True)

    common_files_root = Path(args.common_files_root)
    terminal_path = Path(args.terminal_path)
    metaeditor_path = Path(args.metaeditor_path)
    terminal_data_root = Path(args.terminal_data_root)
    tester_profile_root = Path(args.tester_profile_root)

    all_attempts, matrix_rows, materialized_artifacts = build_materialized_attempts(common_files_root)
    executed_attempts = selected_attempts(all_attempts, args.start_index, args.limit)
    if args.materialize_only:
        execution_result: dict[str, Any] = {
            "compile": {"status": "not_attempted_materialize_only"},
            "execution_results": [],
            "strategy_tester_reports": [],
            "mt5_kpi_records": [],
        }
    else:
        execution_result = execute_attempts(
            executed_attempts,
            terminal_path=terminal_path,
            metaeditor_path=metaeditor_path,
            terminal_data_root=terminal_data_root,
            common_files_root=common_files_root,
            tester_profile_root=tester_profile_root,
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
    artifacts.append(update_selection_status(status, judgment, next_action))
    artifacts.extend(update_current_truth(status, judgment, next_action))
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
                "goal_achieve": "not_claimed",
                "next_action": next_action,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
