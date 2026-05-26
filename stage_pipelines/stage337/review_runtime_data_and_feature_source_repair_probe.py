from __future__ import annotations

import argparse
import csv
import json
import math
import os
import re
import shutil
import subprocess
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import MetaTrader5 as mt5_api
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, path_exists, sha256_file_lf_normalized  # noqa: E402
from foundation.mt5.runtime_artifacts import sha256_file  # noqa: E402
from stage_pipelines.stage335 import independent_proxy_mt5_probe as base  # noqa: E402


TODAY = "2026-05-27"
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
RUN_NUMBER = "run337Q"
RUN_ID = "run337Q_review_runtime_data_and_feature_source_repair_probe_v1"
PARENT_RUN_ID = "run337P_materialize_runtime_data_and_feature_source_repair_probe_v1"
NEXT_RUN_ID = "run337R_fresh_boundary_repaired_forward_attribution_and_asof_policy_review_v1"
CLAIM_BOUNDARY = (
    "research_development_only_stage337Q_tester_date_boundary_repair_review_no_model_training_"
    "no_threshold_retuning_no_lot_optimization_no_candidate_selection_no_forward_passed_no_forward_failed_"
    "no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STATUS_REPAIRED = "completed_stage337Q_tester_date_boundary_probe_reached_feature_last_no_forward_decision"
STATUS_PARTIAL = "completed_stage337Q_tester_date_boundary_probe_partial_no_forward_decision"
JUDGMENT_REPAIRED = "tester_date_boundary_repair_reaches_feature_last_proxy_mt5_parity_usable_for_next_attribution"
JUDGMENT_PARTIAL = "tester_date_boundary_gap_or_runtime_partial_requires_repair"
DECISION_REPAIRED = "stage337Q_open_run337R_boundary_repaired_forward_attribution_no_selection"
DECISION_PARTIAL = "stage337Q_open_run337R_tester_boundary_or_source_policy_repair_no_selection"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
RUN337P_DIR = STAGE_DIR / "02_runs" / "run337P"
RUN337P_ATTEMPTS = RUN337P_DIR / "repair_handoff_attempts.json"
RUN337P_RUNTIME = RUN337P_DIR / "fresh_mt5_runtime_probe_result.csv"
RUN337P_GAP = RUN337P_DIR / "tester_current_day_gap_reprobe.csv"
RUN337P_ASOF = RUN337P_DIR / "source_asof_policy_audit.csv"
MT5_DIR = RUN_DIR / "mt5"
FEATURE_COPY_DIR = RUN_DIR / "feature_matrices"
MODEL_COPY_DIR = RUN_DIR / "models"
TELEMETRY_DIR = RUN_DIR / "runtime_telemetry"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEWS_DIR / "run337Q_tester_date_boundary_repair_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage337Q_tester_date_boundary_repair_review.md"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

DEFAULT_PORTABLE_ROOT = Path(r"C:\Users\awdse\AppData\Local\ObsidianPrime\mt5_portable_run329E")
DEFAULT_TERMINAL = DEFAULT_PORTABLE_ROOT / "terminal64.exe"
DEFAULT_METAEDITOR = DEFAULT_PORTABLE_ROOT / "MetaEditor64.exe"
DEFAULT_COMMON_FILES = DEFAULT_PORTABLE_ROOT / "Common" / "Files"
DEFAULT_TESTER_PROFILE_ROOT = DEFAULT_PORTABLE_ROOT / "MQL5" / "Profiles" / "Tester"
DEFAULT_TERMINAL_DATA_ROOT = DEFAULT_PORTABLE_ROOT
TESTER_LOG = DEFAULT_PORTABLE_ROOT / "Tester" / "logs" / "20260527.log"
TESTER_AGENT_LOG = DEFAULT_PORTABLE_ROOT / "Tester" / "Agent-127.0.0.1-3000" / "logs" / "20260527.log"
TERMINAL_LOG = DEFAULT_PORTABLE_ROOT / "Logs" / "20260527.log"
COMMON_ROOT = "Project_Obsidian_Prime_v2/stage337/run337Q_tester_date_boundary_repair_probe"
ATTEMPT_NAMES = ("c56_bal_rf", "c56_plain_rf", "m48_bal_rf", "m48_plain_rf", "u42_plain_rf")
M5_SECONDS = 300


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def disk_path(path: Path) -> Path:
    resolved = path.resolve()
    if sys.platform == "win32" and len(str(resolved)) < 240:
        return resolved
    return io_path(path)


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return "" if not math.isfinite(value) else f"{value:.12g}"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    if isinstance(value, pd.Timestamp):
        return value.isoformat().replace("+00:00", "Z")
    return str(value)


def json_ready(value: Any) -> Any:
    if isinstance(value, Path):
        return rel(value)
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, pd.Timestamp):
        return value.isoformat().replace("+00:00", "Z")
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        number = float(value)
        return number if math.isfinite(number) else None
    if isinstance(value, np.bool_):
        return bool(value)
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


def write_csv(path: Path, columns: Sequence[str], rows: Iterable[Mapping[str, Any]]) -> Path:
    disk_path(path.parent).mkdir(parents=True, exist_ok=True)
    target = disk_path(path)
    if path.name == "artifact_registry.csv":
        with target.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
            writer.writeheader()
            for row in rows:
                writer.writerow({column: csv_value(row.get(column, "")) for column in columns})
        return path
    tmp = target.with_name(target.name + ".tmp")
    with tmp.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column, "")) for column in columns})
    os.replace(tmp, target)
    return path


def read_csv(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def write_md(path: Path, text: str) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")
    return path


def read_text_lossless(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    had_bom = raw.startswith(b"\xef\xbb\xbf")
    return raw.decode("utf-8-sig" if had_bom else "utf-8"), had_bom


def write_text_preserving(path: Path, text: str, had_bom: bool) -> Path:
    encoding = "utf-8-sig" if had_bom or path.suffix.lower() in {".md", ".txt"} else "utf-8"
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    with io_path(path).open("w", encoding=encoding, newline="\n") as handle:
        handle.write(normalized)
    return path


def upsert_csv(path: Path, key_columns: Sequence[str], row: Mapping[str, Any]) -> Path:
    rows: list[dict[str, str]] = []
    columns: list[str] = []
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            columns = list(reader.fieldnames or [])
            rows = [dict(item) for item in reader]
    for column in row:
        if column not in columns:
            columns.append(column)
    key = tuple(str(row.get(column, "")) for column in key_columns)
    rows = [item for item in rows if tuple(str(item.get(column, "")) for column in key_columns) != key]
    rows.append({column: csv_value(row.get(column, "")) for column in columns})
    write_csv(path, columns, rows)
    return path


def append_csv_rows(path: Path, rows: Sequence[Mapping[str, Any]]) -> Path:
    if not rows:
        return path
    existing: list[dict[str, str]] = []
    columns: list[str] = []
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            columns = list(reader.fieldnames or [])
            existing = [dict(item) for item in reader]
    for row in rows:
        for column in row:
            if column not in columns:
                columns.append(column)
    existing.extend({column: csv_value(row.get(column, "")) for column in columns} for row in rows)
    write_csv(path, columns, existing)
    return path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stage337Q tester date-boundary repair review.")
    parser.add_argument("--terminal-path", default=str(DEFAULT_TERMINAL))
    parser.add_argument("--metaeditor-path", default=str(DEFAULT_METAEDITOR))
    parser.add_argument("--common-files-root", default=str(DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-data-root", default=str(DEFAULT_TERMINAL_DATA_ROOT))
    parser.add_argument("--timeout-seconds", type=int, default=1200)
    parser.add_argument("--wait-timeout-seconds", type=int, default=240)
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--attempt-filter", default="", help="Comma-separated subset of run337P attempts.")
    return parser.parse_args()


def configure_base() -> None:
    base.TODAY = TODAY
    base.STAGE_ID = STAGE_ID
    base.RUN_NUMBER = RUN_NUMBER
    base.RUN_ID = RUN_ID
    base.PARENT_RUN_ID = PARENT_RUN_ID
    base.NEXT_RUN_ID = NEXT_RUN_ID
    base.CLAIM_BOUNDARY = CLAIM_BOUNDARY
    base.STAGE_DIR = STAGE_DIR
    base.RUN_DIR = RUN_DIR
    base.MT5_DIR = MT5_DIR
    base.FEATURE_COPY_DIR = FEATURE_COPY_DIR
    base.MODEL_COPY_DIR = MODEL_COPY_DIR
    base.TELEMETRY_DIR = TELEMETRY_DIR
    base.REVIEWS_DIR = REVIEWS_DIR
    base.DEFAULT_PORTABLE_ROOT = DEFAULT_PORTABLE_ROOT
    base.DEFAULT_TERMINAL = DEFAULT_TERMINAL
    base.DEFAULT_METAEDITOR = DEFAULT_METAEDITOR
    base.DEFAULT_COMMON_FILES = DEFAULT_COMMON_FILES
    base.DEFAULT_TESTER_PROFILE_ROOT = DEFAULT_TESTER_PROFILE_ROOT
    base.DEFAULT_TERMINAL_DATA_ROOT = DEFAULT_TERMINAL_DATA_ROOT
    base.COMMON_ROOT = COMMON_ROOT
    base.DECISION_DOC = DECISION_DOC
    base.PORTABLE_EA_SOURCE = DEFAULT_PORTABLE_ROOT / "MQL5" / "Experts" / base.mt5.EA_SOURCE_PATH
    base.PORTABLE_EA_EX5 = DEFAULT_PORTABLE_ROOT / "MQL5" / "Experts" / "Project_Obsidian_Prime_v2" / "foundation" / "mt5" / "ObsidianPrimeV2_RuntimeProbeEA.ex5"


def floor_m5(value: datetime) -> datetime:
    value = value.astimezone(UTC).replace(second=0, microsecond=0)
    return value - timedelta(minutes=value.minute % 5)


def latest_us100_close(terminal_path: Path) -> dict[str, Any]:
    ok = mt5_api.initialize(path=str(terminal_path), portable=True)
    if not ok:
        return {"status": "blocked_mt5_initialize_failed", "last_error": str(mt5_api.last_error())}
    try:
        mt5_api.symbol_select("US100", True)
        rates = mt5_api.copy_rates_from_pos("US100", mt5_api.TIMEFRAME_M5, 0, 10)
        if rates is None or len(rates) == 0:
            return {"status": "blocked_no_us100_rates", "last_error": str(mt5_api.last_error())}
        last_open = datetime.fromtimestamp(int(rates[-1]["time"]), tz=UTC)
        last_close = last_open + timedelta(seconds=M5_SECONDS)
        return {
            "status": "completed",
            "last_open_utc": last_open.isoformat().replace("+00:00", "Z"),
            "last_close_utc": last_close.isoformat().replace("+00:00", "Z"),
            "row_probe_count": int(len(rates)),
            "last_error": str(mt5_api.last_error()),
        }
    finally:
        mt5_api.shutdown()


def source_attempts(attempt_filter: str) -> list[dict[str, Any]]:
    allowed = set(ATTEMPT_NAMES)
    if attempt_filter.strip():
        requested = {item.strip() for item in attempt_filter.split(",") if item.strip()}
        unknown = requested - allowed
        if unknown:
            raise ValueError(f"Unsupported attempt_filter values: {sorted(unknown)}")
        allowed = requested
    rows = read_json(RUN337P_ATTEMPTS)
    selected: list[dict[str, Any]] = []
    for row in rows:
        if row.get("attempt_name") not in allowed:
            continue
        copied = dict(row)
        copied["model_copy"] = {"source": row.get("model_local_path", "")}
        copied["feature_export"] = {"path": row.get("feature_local_path", "")}
        copied["source_run_id"] = PARENT_RUN_ID
        copied["attempt_role"] = "stage337Q_tester_date_boundary_repair_probe_same_frozen_model_feature_threshold_risk"
        selected.append(copied)
    return selected


def target_tester_to_date(feature_latest: pd.Timestamp) -> str:
    # MT5 tester logs show ToDate=2026.05.28 became an actual test end of 2026.05.27 00:00.
    # A +2 calendar date probes that boundary without changing model, threshold, risk, or lot logic.
    return (feature_latest.date() + timedelta(days=2)).strftime("%Y.%m.%d")


def feature_timestamps(path: Path) -> pd.Series:
    frame = pd.read_csv(io_path(path), usecols=lambda column: column in {"bar_time_server", "timestamp_utc", "timestamp"})
    for column in ("timestamp_utc", "bar_time_server", "timestamp"):
        if column in frame.columns:
            return pd.to_datetime(frame[column].astype(str).str.replace(".", "-", regex=False), errors="coerce", utc=True).dropna()
    return pd.Series([], dtype="datetime64[ns, UTC]")


def feature_last_rows(attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for attempt in attempts:
        path = ROOT / str(attempt["feature_local_path"])
        timestamps = feature_timestamps(path)
        rows.append(
            {
                "attempt_name": attempt["attempt_name"],
                "feature_set_id": attempt.get("feature_set_id", ""),
                "feature_rows": int(len(timestamps)),
                "feature_first_timestamp": timestamps.min().isoformat().replace("+00:00", "Z") if len(timestamps) else "",
                "feature_last_timestamp": timestamps.max().isoformat().replace("+00:00", "Z") if len(timestamps) else "",
                "feature_csv_path": rel(path),
                "feature_csv_sha256": sha256_file(path) if path_exists(path) else "",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def rewrite_attempt_to_boundary(attempt: dict[str, Any], tester_to_date: str) -> dict[str, Any]:
    tester = dict(attempt["ini"]["tester"])
    tester["ToDate"] = tester_to_date
    tester["Report"] = f"Project_Obsidian_Prime_v2_{RUN_ID}_{attempt['attempt_name']}"
    ini_path = Path(str(attempt["ini"]["path"]))
    attempt["ini"] = base.materialize_ini_file(tester, ini_path)
    attempt["to_date"] = tester_to_date
    attempt["attempt_role"] = "stage337Q_tester_date_boundary_repair_probe_same_frozen_model_feature_threshold_risk"
    attempt["record_view_prefix"] = f"mt5_stage337Q_{attempt['artifact_slug']}"
    attempt["source_run_id"] = PARENT_RUN_ID
    attempt["repair_contract"] = "tester ToDate boundary widened only; same ONNX, feature order, threshold, risk, lot, and feature CSV"
    attempt["signal_policy"] = "same frozen ONNX and runtime settings; ToDate boundary probe only"
    return attempt


def detect_running_terminal_processes(terminal_path: Path) -> dict[str, Any]:
    command = [
        "powershell",
        "-NoProfile",
        "-Command",
        "Get-CimInstance Win32_Process -Filter \"name = 'terminal64.exe'\" | Select-Object ProcessId,ExecutablePath,CommandLine | ConvertTo-Json -Compress",
    ]
    proc = subprocess.run(command, text=True, capture_output=True, timeout=30)
    payload: dict[str, Any] = {
        "status": "detection_failed" if proc.returncode else "not_running",
        "command": command,
        "returncode": proc.returncode,
        "stdout": proc.stdout[-2000:],
        "stderr": proc.stderr[-2000:],
        "processes": [],
        "matching_processes": [],
    }
    if proc.returncode != 0 or not proc.stdout.strip():
        return payload
    try:
        parsed = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        payload["parse_error"] = str(exc)
        return payload
    processes = parsed if isinstance(parsed, list) else [parsed]
    target = str(terminal_path).lower()
    matches = [item for item in processes if str(item.get("ExecutablePath", "")).lower() == target]
    payload["processes"] = processes
    payload["matching_processes"] = matches
    payload["status"] = "running" if matches else "not_running"
    return payload


def stop_target_terminal_if_running(terminal_path: Path) -> dict[str, Any]:
    probe = detect_running_terminal_processes(terminal_path)
    stopped: list[dict[str, Any]] = []
    for match in probe.get("matching_processes", []) or []:
        pid = match.get("ProcessId")
        if not pid:
            continue
        proc = subprocess.run(
            ["powershell", "-NoProfile", "-Command", f"Stop-Process -Id {int(pid)} -Force"],
            text=True,
            capture_output=True,
            timeout=30,
        )
        stopped.append({"process_id": int(pid), "returncode": proc.returncode, "stdout": proc.stdout[-1000:], "stderr": proc.stderr[-1000:]})
    after = detect_running_terminal_processes(terminal_path)
    return {
        "before_status": probe.get("status"),
        "before_matching_processes": probe.get("matching_processes", []),
        "stopped": stopped,
        "after_status": after.get("status"),
        "after_matching_processes": after.get("matching_processes", []),
        "effect": "target portable terminal(대상 포터블 터미널)을 MT5 tester config(MT5 테스터 설정) 실행 전에 닫는다.",
    }


def log_offsets(paths: Sequence[Path]) -> dict[str, int]:
    return {path.as_posix(): (io_path(path).stat().st_size if path_exists(path) else 0) for path in paths}


def log_segment(path: Path, start: int) -> str:
    if not path_exists(path):
        return ""
    with io_path(path).open("rb") as handle:
        handle.seek(start)
        raw = handle.read()
    for encoding in ("utf-16", "utf-8-sig", "utf-8", "cp1252"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="ignore")


def tester_boundary_rows(before_offsets: Mapping[str, int], attempts: Sequence[Mapping[str, Any]], requested_to_date: str) -> list[dict[str, Any]]:
    segment = log_segment(TESTER_AGENT_LOG, int(before_offsets.get(TESTER_AGENT_LOG.as_posix(), 0)))
    if not segment:
        segment = log_segment(TESTER_LOG, int(before_offsets.get(TESTER_LOG.as_posix(), 0)))
    boundary_matches = re.findall(r"testing of .*? from (\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}) to (\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}) started", segment)
    history_matches = re.findall(r"History\s+US100: history synchronized from ([0-9.]+) to ([0-9.]+)", segment)
    tick_matches = re.findall(r"Ticks\s+US100: history ticks synchronized from ([0-9.]+) to ([0-9.]+)", segment)
    generated_matches = re.findall(r"US100,M5: ([0-9]+) ticks, ([0-9]+) bars generated", segment)
    rows: list[dict[str, Any]] = []
    for index, attempt in enumerate(attempts):
        boundary = boundary_matches[index] if index < len(boundary_matches) else ("", "")
        history = history_matches[index] if index < len(history_matches) else ("", "")
        ticks = tick_matches[index] if index < len(tick_matches) else ("", "")
        generated = generated_matches[index] if index < len(generated_matches) else ("", "")
        rows.append(
            {
                "attempt_name": attempt["attempt_name"],
                "requested_to_date": requested_to_date,
                "log_test_from": boundary[0],
                "log_test_to": boundary[1],
                "history_sync_from": history[0],
                "history_sync_to": history[1],
                "tick_sync_from": ticks[0],
                "tick_sync_to": ticks[1],
                "generated_ticks": generated[0],
                "generated_bars": generated[1],
                "source": rel(TESTER_AGENT_LOG),
                "effect": "MT5 Strategy Tester(전략 테스터)가 요청 ToDate(종료일)를 실제 어떤 테스트 종료 시간으로 해석했는지 기록한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def telemetry_last_observed(attempt_name: str, common_files_root: Path, common_telemetry_path: str) -> tuple[str, int]:
    candidates = [TELEMETRY_DIR / f"{attempt_name}_telemetry.csv"]
    if common_telemetry_path:
        candidates.append(common_files_root / Path(common_telemetry_path))
    path = next((candidate for candidate in candidates if path_exists(candidate)), None)
    if path is None:
        return "", 0
    frame = pd.read_csv(io_path(path), usecols=lambda column: column in {"record_type", "bar_time"})
    if "record_type" in frame.columns:
        frame = frame.loc[frame["record_type"].astype(str) == "cycle"]
    values = pd.to_datetime(frame["bar_time"].astype(str).str.replace(".", "-", regex=False), errors="coerce", utc=True).dropna()
    return (values.max().isoformat().replace("+00:00", "Z") if len(values) else "", int(len(values)))


def tester_gap_rows(runtime_rows: Sequence[Mapping[str, Any]], feature_rows: Sequence[Mapping[str, Any]], common_files_root: Path, latest_probe: Mapping[str, Any]) -> list[dict[str, Any]]:
    feature_by = {row["attempt_name"]: row for row in feature_rows}
    api_latest = pd.to_datetime(latest_probe.get("last_close_utc", ""), errors="coerce", utc=True)
    rows: list[dict[str, Any]] = []
    for row in runtime_rows:
        attempt = str(row.get("attempt_name", ""))
        feature_last = pd.to_datetime(feature_by.get(attempt, {}).get("feature_last_timestamp", ""), errors="coerce", utc=True)
        last_obs, telemetry_rows = telemetry_last_observed(attempt, common_files_root, str(row.get("common_telemetry_path", "")))
        last_obs_ts = pd.to_datetime(last_obs, errors="coerce", utc=True)
        if pd.isna(last_obs_ts):
            status = "tester_observed_window_missing"
        elif not pd.isna(feature_last) and last_obs_ts >= feature_last:
            status = "tester_reached_feature_last"
        else:
            status = "tester_feature_last_gap_remains"
        rows.append(
            {
                "attempt_name": attempt,
                "feature_set_id": row.get("feature_set_id", ""),
                "runtime_status": row.get("runtime_status", ""),
                "report_status": row.get("report_status", ""),
                "api_latest_us100_close_utc": "" if pd.isna(api_latest) else api_latest.isoformat().replace("+00:00", "Z"),
                "feature_last_timestamp": "" if pd.isna(feature_last) else feature_last.isoformat().replace("+00:00", "Z"),
                "tester_last_observed_bar_time": last_obs,
                "tester_to_feature_last_gap_minutes": "" if pd.isna(last_obs_ts) or pd.isna(feature_last) else (feature_last - last_obs_ts).total_seconds() / 60.0,
                "tester_to_api_latest_gap_minutes": "" if pd.isna(last_obs_ts) or pd.isna(api_latest) else (api_latest - last_obs_ts).total_seconds() / 60.0,
                "telemetry_rows": telemetry_rows,
                "last_skip_reason": row.get("last_skip_reason", ""),
                "gap_status": status,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def feature_timestamp_series(frame: pd.DataFrame) -> pd.Series:
    for column in ("timestamp_utc", "bar_time_server", "timestamp"):
        if column in frame.columns:
            return pd.to_datetime(frame[column].astype(str).str.replace(".", "-", regex=False), errors="coerce", utc=True)
    return pd.Series(pd.NaT, index=frame.index, dtype="datetime64[ns, UTC]")


def build_timestamp_aligned_proxy_rows(attempts: Sequence[Mapping[str, Any]], cutoff_by_attempt: Mapping[str, str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for attempt in attempts:
        attempt_name = str(attempt["attempt_name"])
        cutoff_ts = pd.to_datetime(str(cutoff_by_attempt.get(attempt_name, "")), errors="coerce", utc=True)
        if pd.isna(cutoff_ts):
            rows.append(
                {
                    "attempt_name": attempt_name,
                    "artifact_slug": attempt["artifact_slug"],
                    "feature_set_id": attempt["feature_set_id"],
                    "model_id": attempt["model_id"],
                    "expected_feature_ready_count": None,
                    "expected_model_ok_count": None,
                    "expected_short_count": None,
                    "expected_long_count": None,
                    "expected_flat_count": None,
                    "expected_signal_count": None,
                    "expected_signal_rate": None,
                    "expected_long_share": None,
                    "mean_p_short": None,
                    "mean_p_flat": None,
                    "mean_p_long": None,
                    "mean_probability_margin": None,
                    "max_probability_row_sum_abs_error": None,
                    "feature_order_hash": "",
                    "feature_csv_sha256": "",
                    "model_sha256": "",
                    "threshold_policy": "frozen_source_set_min_margin_no_search",
                    "proxy_source": "timestamp_aligned_unavailable_no_tester_observed_time",
                    "proxy_cutoff_utc": "",
                    "proxy_row_scope": "missing_tester_observed_time",
                    "full_feature_rows": None,
                    "timestamp_aligned_feature_rows": None,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            continue

        set_values = base.parse_key_value_file(ROOT / str(attempt["set"]["path"]))
        feature_path = ROOT / str(attempt["feature_local_path"])
        model_path = ROOT / str(attempt["model_local_path"])
        feature_count = base.parse_int(set_values.get("InpFeatureCount"))
        frame_full = pd.read_csv(io_path(feature_path))
        timestamps = feature_timestamp_series(frame_full)
        frame = frame_full.loc[timestamps <= cutoff_ts].copy()
        cols = base.feature_columns(frame_full, feature_count)
        matrix = frame.loc[:, cols].to_numpy(dtype="float64", copy=False)
        probabilities = base.model_probabilities(model_path, matrix) if len(frame) else np.empty((0, 3), dtype="float64")
        rule = base.ThresholdRule(
            threshold_id=f"stage337Q_{attempt_name}_timestamp_aligned_fixed_min_margin",
            short_threshold=base.parse_float(set_values.get("InpShortThreshold")),
            long_threshold=base.parse_float(set_values.get("InpLongThreshold")),
            min_margin=base.parse_float(set_values.get("InpMinMargin")),
        )
        decisions = base.apply_threshold_rule(pd.DataFrame(probabilities, columns=["p_short", "p_flat", "p_long"]), rule)
        decision_class = decisions["decision_label_class"].to_numpy(dtype="int64", copy=False) if len(decisions) else np.empty(0, dtype="int64")
        if base.parse_bool(set_values.get("InpInvertSignal")) and len(decision_class):
            inverted = decision_class.copy()
            inverted[decision_class == 0] = 2
            inverted[decision_class == 2] = 0
            decision_class = inverted
        short_count = int((decision_class == 0).sum())
        long_count = int((decision_class == 2).sum())
        flat_count = int((decision_class == -1).sum())
        signal_count = short_count + long_count
        prob_sum_error = float(np.abs(probabilities.sum(axis=1) - 1.0).max()) if len(probabilities) else 0.0
        sorted_probs = np.sort(probabilities, axis=1) if len(probabilities) else np.empty((0, 3), dtype="float64")
        rows.append(
            {
                "attempt_name": attempt_name,
                "artifact_slug": attempt["artifact_slug"],
                "feature_set_id": attempt["feature_set_id"],
                "model_id": attempt["model_id"],
                "expected_feature_ready_count": int(len(frame)),
                "expected_model_ok_count": int(len(frame)),
                "expected_short_count": short_count,
                "expected_long_count": long_count,
                "expected_flat_count": flat_count,
                "expected_signal_count": signal_count,
                "expected_signal_rate": signal_count / len(frame) if len(frame) else None,
                "expected_long_share": long_count / signal_count if signal_count else None,
                "mean_p_short": float(probabilities[:, 0].mean()) if len(probabilities) else None,
                "mean_p_flat": float(probabilities[:, 1].mean()) if len(probabilities) else None,
                "mean_p_long": float(probabilities[:, 2].mean()) if len(probabilities) else None,
                "mean_probability_margin": float((sorted_probs[:, -1] - sorted_probs[:, -2]).mean()) if len(probabilities) else None,
                "max_probability_row_sum_abs_error": prob_sum_error,
                "feature_order_hash": base.ordered_hash(cols),
                "feature_csv_sha256": sha256_file(feature_path),
                "model_sha256": sha256_file(model_path),
                "threshold_policy": "frozen_source_set_min_margin_no_search",
                "proxy_source": "timestamp_aligned_python_onnx_inference_cut_to_mt5_tester_last_observed_bar",
                "proxy_cutoff_utc": cutoff_ts.isoformat().replace("+00:00", "Z"),
                "proxy_row_scope": "feature_rows_at_or_before_mt5_tester_last_observed_bar",
                "full_feature_rows": int(len(frame_full)),
                "timestamp_aligned_feature_rows": int(len(frame)),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def sanitize_proxy_rows(rows: Sequence[Mapping[str, Any]], *, default_source: str) -> list[dict[str, Any]]:
    cleaned: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        existing = str(item.get("proxy_source") or "")
        item["proxy_source"] = existing if "timestamp_aligned" in existing else default_source
        item["claim_boundary"] = CLAIM_BOUNDARY
        cleaned.append(item)
    return cleaned


def sanitize_diff_rows(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    cleaned: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        item["mt5_source"] = "stage337Q_tester_date_boundary_probe_tier_a_telemetry_summary"
        item["usable_for_forward_pass_fail"] = False
        item["claim_boundary"] = CLAIM_BOUNDARY
        cleaned.append(item)
    return cleaned


def metric_summary(runtime_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in runtime_rows:
        trades = float(row.get("trade_count") or 0.0)
        net = float(row.get("net_profit") or 0.0)
        rows.append(
            {
                "attempt_name": row.get("attempt_name", ""),
                "feature_set_id": row.get("feature_set_id", ""),
                "runtime_status": row.get("runtime_status", ""),
                "report_status": row.get("report_status", ""),
                "net_profit": row.get("net_profit", ""),
                "profit_factor": row.get("profit_factor", ""),
                "trade_count": row.get("trade_count", ""),
                "expectancy": row.get("expectancy", ""),
                "recovery_factor": row.get("recovery_factor", ""),
                "max_drawdown_amount": row.get("max_drawdown_amount", ""),
                "long_trade_count": row.get("long_trade_count", ""),
                "short_trade_count": row.get("short_trade_count", ""),
                "lot_normalized_net_per_trade": (net / trades) if trades else "",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def asof_policy_review_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path_exists(RUN337P_ASOF):
        return rows
    for row in read_csv(RUN337P_ASOF):
        over = int(float(row.get("rows_over_max_age") or 0))
        latest_age = float(row.get("latest_row_asof_age_minutes") or 0)
        feature_set = row.get("feature_set_id", "")
        symbol = row.get("required_symbol", "")
        if over > 0 and feature_set == "core56_no_top3_weight_features" and symbol not in {"VIX", "US10YR", "USDX"}:
            judgment = "session_bridge_requires_review_not_forward_authority"
            effect = "equity source(주식 원천)는 cash session(현금장) 밖에서 오래된 값으로 이어져 probe(탐침)는 가능하지만 forward authority(전진 권위)는 아니다."
        elif over > 0:
            judgment = "macro_source_lag_requires_session_aware_review"
            effect = "macro source(거시 원천)는 일부 구간에서 허용 나이를 넘겨 source policy(원천 정책) 리뷰가 필요하다."
        else:
            judgment = "asof_age_within_probe_boundary"
            effect = "latest as-of age(최신 시점 기준 나이)는 탐침 경계 안에서 사용 가능하다."
        rows.append(
            {
                "feature_set_id": feature_set,
                "required_symbol": symbol,
                "latest_row_asof_age_minutes": latest_age,
                "rows_over_max_age": over,
                "source_policy_judgment": judgment,
                "usable_for_runtime_probe": True,
                "usable_for_forward_pass_fail": False,
                "effect": effect,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def classify(runtime_rows: Sequence[Mapping[str, Any]], gap_rows: Sequence[Mapping[str, Any]], aligned_diff_rows: Sequence[Mapping[str, Any]], materialize_only: bool) -> tuple[str, str, str]:
    if materialize_only:
        return STATUS_PARTIAL, JUDGMENT_PARTIAL, DECISION_PARTIAL
    completed = sum(1 for row in runtime_rows if row.get("tester_status") == "completed" and row.get("runtime_status") == "completed" and row.get("report_status") == "completed")
    reached = sum(1 for row in gap_rows if row.get("gap_status") == "tester_reached_feature_last")
    matches = sum(1 for row in aligned_diff_rows if str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true")
    if completed == len(runtime_rows) and reached == len(gap_rows) and matches == len(aligned_diff_rows) and aligned_diff_rows:
        return STATUS_REPAIRED, JUDGMENT_REPAIRED, DECISION_REPAIRED
    return STATUS_PARTIAL, JUDGMENT_PARTIAL, DECISION_PARTIAL


def gate_rows(runtime_rows: Sequence[Mapping[str, Any]], gap_rows: Sequence[Mapping[str, Any]], raw_diff_rows: Sequence[Mapping[str, Any]], aligned_diff_rows: Sequence[Mapping[str, Any]], boundary_rows: Sequence[Mapping[str, Any]], asof_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    completed = sum(1 for row in runtime_rows if row.get("tester_status") == "completed" and row.get("runtime_status") == "completed" and row.get("report_status") == "completed")
    reached = sum(1 for row in gap_rows if row.get("gap_status") == "tester_reached_feature_last")
    raw_matches = sum(1 for row in raw_diff_rows if str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true")
    aligned_matches = sum(1 for row in aligned_diff_rows if str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true")
    return [
        {
            "gate_name": "run337P_evidence_reviewed",
            "status": "covered",
            "evidence_path": rel(RUN337P_GAP),
            "effect": "run337P(337P 실행)의 current-day gap(현재일 공백)을 원인 감사 입력으로 고정한다.",
        },
        {
            "gate_name": "tester_date_boundary_log_audited",
            "status": "covered" if boundary_rows else "covered_partial",
            "evidence_path": rel(RUN_DIR / "tester_date_boundary_log_audit.csv"),
            "effect": f"Strategy Tester(전략 테스터)의 실제 from/to(시작/종료) 로그를 기록한다; rows={len(boundary_rows)}.",
        },
        {
            "gate_name": "mt5_todate_boundary_repair_probe",
            "status": "covered" if completed == len(runtime_rows) else "covered_partial",
            "evidence_path": rel(RUN_DIR / "fresh_mt5_runtime_probe_result.csv"),
            "effect": f"ToDate boundary(종료일 경계) 수리 탐침을 MT5(메타트레이더5)에서 실행한다; completed={completed}/{len(runtime_rows)}.",
        },
        {
            "gate_name": "tester_reached_feature_last",
            "status": "covered_repaired" if reached == len(gap_rows) else "covered_blocker",
            "evidence_path": rel(RUN_DIR / "tester_feature_last_gap_reprobe.csv"),
            "effect": f"telemetry(텔레메트리)가 feature last(피처 마지막 시점)에 도달했는지 확인한다; reached={reached}/{len(gap_rows)}.",
        },
        {
            "gate_name": "proxy_mt5_difference_recorded",
            "status": "covered" if aligned_matches == len(aligned_diff_rows) and aligned_diff_rows else "covered_partial",
            "evidence_path": rel(RUN_DIR / "timestamp_aligned_proxy_mt5_difference.csv"),
            "effect": f"proxy expected(프록시 예상값)와 MT5 observed(관측값)를 비교한다; raw={raw_matches}/{len(raw_diff_rows)}, aligned={aligned_matches}/{len(aligned_diff_rows)}.",
        },
        {
            "gate_name": "asof_source_policy_boundary_reviewed",
            "status": "covered",
            "evidence_path": rel(RUN_DIR / "asof_source_policy_review.csv"),
            "effect": f"as-of source policy(시점 기준 원천 정책)가 forward pass/fail(전진 통과/실패)에 바로 쓰일 수 있는지 분리한다; rows={len(asof_rows)}.",
        },
        {
            "gate_name": "no_forward_or_goal_claim",
            "status": "covered",
            "evidence_path": rel(RUN_DIR / "final_tester_date_boundary_repair_review_decision.json"),
            "effect": "Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)를 주장하지 않는다.",
        },
    ]


def copy_reports_to_required_names(runtime_rows: Sequence[Mapping[str, Any]]) -> list[Path]:
    copied: list[Path] = []
    first_report = next((row.get("report_path") for row in runtime_rows if row.get("report_path")), "")
    if first_report:
        source = Path(str(first_report))
        if path_exists(source):
            target = RUN_DIR / "mt5_strategy_tester_report.html"
            shutil.copy2(io_path(source), io_path(target))
            copied.append(target)
    first_telemetry = next((TELEMETRY_DIR / f"{row.get('attempt_name')}_telemetry.csv" for row in runtime_rows if path_exists(TELEMETRY_DIR / f"{row.get('attempt_name')}_telemetry.csv")), None)
    if first_telemetry:
        target = RUN_DIR / "mt5_terminal_telemetry.csv"
        shutil.copy2(io_path(first_telemetry), io_path(target))
        copied.append(target)
    return copied


def build_receipts(status: str, judgment: str, decision: str, runtime_rows: Sequence[Mapping[str, Any]], gap_rows: Sequence[Mapping[str, Any]], aligned_diff_rows: Sequence[Mapping[str, Any]]) -> list[Path]:
    completed = sum(1 for row in runtime_rows if row.get("tester_status") == "completed" and row.get("runtime_status") == "completed" and row.get("report_status") == "completed")
    reached = sum(1 for row in gap_rows if row.get("gap_status") == "tester_reached_feature_last")
    matches = sum(1 for row in aligned_diff_rows if str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true")
    return [
        write_json(
            RUN_DIR / "data_integrity_receipt.json",
            {
                "run_id": RUN_ID,
                "data_source": "run337P repaired feature CSV and fresh MT5 tester output",
                "time_axis": "MT5 bar_time and feature bar_time_server use UTC-like server timestamp strings; ToDate boundary separately audited",
                "feature_label_boundary": "no model training, no threshold retune, no future feature fill; ToDate repair probes tester inclusion only",
                "integrity_judgment": "usable_for_runtime_probe_not_forward_decision",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RUN_DIR / "runtime_parity_receipt.json",
            {
                "run_id": RUN_ID,
                "runtime_completed": f"{completed}/{len(runtime_rows)}",
                "tester_reached_feature_last": f"{reached}/{len(gap_rows)}",
                "timestamp_aligned_signal_parity": f"{matches}/{len(aligned_diff_rows)}",
                "runtime_claim_boundary": "runtime_probe_only_no_runtime_authority",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RUN_DIR / "result_judgment_receipt.json",
            {
                "run_id": RUN_ID,
                "status": status,
                "judgment": judgment,
                "decision": decision,
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "runtime_authority": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RUN_DIR / "backtest_forensics_receipt.json",
            {
                "run_id": RUN_ID,
                "tester_identity": "FPMarketsSC-Live US100 M5 real-tick Strategy Tester date-boundary repair probe",
                "report_identity": [row.get("report_path", "") for row in runtime_rows],
                "trade_evidence": [{key: row.get(key, "") for key in ("attempt_name", "net_profit", "profit_factor", "trade_count", "max_drawdown_amount")} for row in runtime_rows],
                "backtest_judgment": "usable_with_boundary_for_runtime_probe_not_forward_decision",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RUN_DIR / "artifact_lineage_receipt.json",
            {
                "run_id": RUN_ID,
                "parent_run_id": PARENT_RUN_ID,
                "source_attempts": rel(RUN337P_ATTEMPTS),
                "lineage_judgment": "run337Q reuses run337P frozen model, feature order, threshold, risk, and lot; only tester ToDate boundary changes",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
    ]


def write_report(status: str, judgment: str, decision: str, latest_probe: Mapping[str, Any], runtime_rows: Sequence[Mapping[str, Any]], gap_rows: Sequence[Mapping[str, Any]], raw_diff_rows: Sequence[Mapping[str, Any]], aligned_diff_rows: Sequence[Mapping[str, Any]], asof_rows: Sequence[Mapping[str, Any]]) -> Path:
    completed = sum(1 for row in runtime_rows if row.get("tester_status") == "completed" and row.get("runtime_status") == "completed" and row.get("report_status") == "completed")
    reached = sum(1 for row in gap_rows if row.get("gap_status") == "tester_reached_feature_last")
    raw_matches = sum(1 for row in raw_diff_rows if str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true")
    aligned_matches = sum(1 for row in aligned_diff_rows if str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true")
    asof_watch = sum(1 for row in asof_rows if row.get("usable_for_forward_pass_fail") in {False, "false"})
    lines = [
        "# Stage337Q Tester Date Boundary Repair Review(337Q 테스터 종료일 경계 수리 리뷰)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- status(상태): `{status}`",
        f"- judgment(판정): `{judgment}`",
        f"- decision(결정): `{decision}`",
        f"- api_latest_us100_close(API 최신 US100 종가): `{latest_probe.get('last_close_utc', '')}`",
        f"- MT5 completed(MT5 완료): `{completed}/{len(runtime_rows)}`",
        f"- tester reached feature last(테스터 피처 끝 도달): `{reached}/{len(gap_rows)}`",
        f"- raw proxy parity(전체 프록시 동등성): `{raw_matches}/{len(raw_diff_rows)}`",
        f"- timestamp-aligned proxy parity(시점 맞춤 프록시 동등성): `{aligned_matches}/{len(aligned_diff_rows)}`",
        f"- asof policy rows needing forward caution(전진 주의 필요 정책 행): `{asof_watch}`",
        "- Forward Passed(전진 통과): `not_claimed`",
        "- Forward Failed(전진 실패): `not_claimed`",
        "- runtime authority(런타임 권위): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Runtime Metrics(런타임 지표)",
        "",
        "| attempt(시도) | status(상태) | net(순익) | PF(손익비) | trades(거래수) | DD(드로다운) |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in runtime_rows:
        status_label = f"{row.get('tester_status', '')}/{row.get('runtime_status', '')}/{row.get('report_status', '')}"
        lines.append(f"| `{row.get('attempt_name', '')}` | `{status_label}` | `{row.get('net_profit', '')}` | `{row.get('profit_factor', '')}` | `{row.get('trade_count', '')}` | `{row.get('max_drawdown_amount', '')}` |")
    lines.extend(
        [
            "",
            "## Boundary(경계)",
            "",
            "run337Q(337Q 실행)는 tester ToDate boundary(테스터 종료일 경계) 수리 탐침이다. ONNX(온엑스), feature order(피처 순서), threshold(임계값), risk/lot(위험/랏)은 그대로 유지했다. 이 결과는 runtime probe(런타임 탐침)일 뿐이며 Forward Passed/Failed(전진 통과/실패)나 runtime authority(런타임 권위)가 아니다.",
        ]
    )
    return write_md(REPORT_PATH, "\n".join(lines))


def write_decision_doc(status: str, judgment: str, decision: str, latest_probe: Mapping[str, Any]) -> Path:
    text = f"""# Stage337Q Decision(337Q 결정)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{status}`
- judgment(판정): `{judgment}`
- decision(결정): `{decision}`
- api_latest_us100_close(API 최신 US100 종가): `{latest_probe.get('last_close_utc', '')}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Effect(효과): run337Q(337Q 실행)는 run337P(337P 실행)의 tester current-day gap(테스터 현재일 공백)을 ToDate boundary(종료일 경계) 문제로 분해하고, 같은 ONNX/feature/threshold/risk/lot(온엑스/피처/임계값/위험/랏)으로 수리 탐침을 실행했다.
"""
    return write_md(DECISION_DOC, text)


def update_status_docs(status: str, decision: str, runtime_rows: Sequence[Mapping[str, Any]], gap_rows: Sequence[Mapping[str, Any]], aligned_diff_rows: Sequence[Mapping[str, Any]]) -> list[Path]:
    completed = sum(1 for row in runtime_rows if row.get("tester_status") == "completed" and row.get("runtime_status") == "completed" and row.get("report_status") == "completed")
    reached = sum(1 for row in gap_rows if row.get("gap_status") == "tester_reached_feature_last")
    aligned = sum(1 for row in aligned_diff_rows if str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true")
    selection_text = f"""# Stage337 Selection Status(337단계 선택 상태)

- stage_id(단계 ID): `{STAGE_ID}`
- stage_status(단계 상태): `open_active`
- selected_candidate(선택 후보): `none`
- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{decision}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- tester_boundary_probe_runtime(테스터 경계 탐침 런타임): `{completed}/{len(runtime_rows)} completed(완료)`
- tester_reached_feature_last(테스터 피처 끝 도달): `{reached}/{len(gap_rows)}`
- timestamp_aligned_proxy_parity(시점 맞춤 프록시 동등성): `{aligned}/{len(aligned_diff_rows)}`
- current blockers(현재 차단 요소): `asof_source_policy_review_required;fresh_boundary_repaired_forward_attribution_required`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed_for_stage337_new_work`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): run337Q(337Q 실행)는 tester ToDate boundary(테스터 종료일 경계) 수리 탐침을 실행했고, 결과는 선택이나 Forward decision(전진 판정)이 아니라 run337R(337R 실행)의 attribution/stress review(귀속/압박 리뷰) 입력이다.
"""
    write_md(SELECTED_STATUS, selection_text)

    focus_line = (
        "- >-\n"
        f"  Stage337 run337Q focus complete: Stage337(337단계) run337Q(337Q 실행)는 `{status}`로 tester date boundary repair review(테스터 종료일 경계 수리 리뷰)를 완료했다. "
        f"Effect(효과): MT5(메타트레이더5) `{completed}/{len(runtime_rows)}` 실행, tester reached feature last(테스터 피처 끝 도달) `{reached}/{len(gap_rows)}`, timestamp-aligned proxy parity(시점 맞춤 프록시 동등성) `{aligned}/{len(aligned_diff_rows)}`를 기록하고 Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    if path_exists(WORKSPACE_STATE):
        text, had_bom = read_text_lossless(WORKSPACE_STATE)
        lines = text.splitlines()
        for idx, line in enumerate(lines):
            if line.startswith("current_run_id:"):
                lines[idx] = f"current_run_id: {NEXT_RUN_ID}"
                break
        text = "\n".join(lines) + "\n"
        if "Stage337 run337Q focus complete" in text:
            text = re.sub(r"- >-\n  Stage337 run337Q focus complete:.*?(?=\n- >-|\Z)", focus_line.rstrip(), text, count=1, flags=re.S)
        else:
            lines = text.splitlines()
            try:
                idx = lines.index("current_focus:")
                lines.insert(idx + 1, focus_line.rstrip())
            except ValueError:
                lines.extend(["current_focus:", focus_line.rstrip()])
            text = "\n".join(lines) + "\n"
        write_text_preserving(WORKSPACE_STATE, text, had_bom)

    current_entry = f"""
## Stage337 run337Q(337Q 실행) - {TODAY}

- status(상태): `{status}`
- decision(결정): `{decision}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): tester ToDate boundary repair probe(테스터 종료일 경계 수리 탐침)를 MT5(메타트레이더5) `{completed}/{len(runtime_rows)}`로 실행했고, tester reached feature last(테스터 피처 끝 도달) `{reached}/{len(gap_rows)}`, timestamp-aligned proxy parity(시점 맞춤 프록시 동등성) `{aligned}/{len(aligned_diff_rows)}`를 기록했다.
"""
    if path_exists(CURRENT_STATE):
        text, had_bom = read_text_lossless(CURRENT_STATE)
        if "## Stage337 run337Q(337Q 실행)" in text:
            text = re.sub(r"## Stage337 run337Q\(337Q 실행\).*?(?=\n## |\Z)", current_entry.strip(), text, count=1, flags=re.S)
            write_text_preserving(CURRENT_STATE, text.rstrip() + "\n", had_bom)
        else:
            write_text_preserving(CURRENT_STATE, text.rstrip() + "\n\n" + current_entry.strip() + "\n", had_bom)

    if path_exists(CHANGELOG):
        text, had_bom = read_text_lossless(CHANGELOG)
        line = f"\n- {TODAY}: Stage337 run337Q(337Q 실행) `{status}`. Effect(효과): tester date boundary repair probe(테스터 종료일 경계 수리 탐침)를 MT5(메타트레이더5) `{completed}/{len(runtime_rows)}`로 실행했고 Forward/Goal(전진/목표) 주장은 없음.\n"
        if "Stage337 run337Q(337Q 실행)" in text:
            text = re.sub(r"\n- [^\n]*Stage337 run337Q\(337Q 실행\)[^\n]*", line.rstrip(), text, count=1)
            write_text_preserving(CHANGELOG, text.rstrip() + "\n", had_bom)
        else:
            write_text_preserving(CHANGELOG, text.rstrip() + line, had_bom)
    return [SELECTED_STATUS, WORKSPACE_STATE, CURRENT_STATE, CHANGELOG]


def update_registers(status: str, judgment: str, decision: str, artifact_paths: Sequence[Path]) -> list[Path]:
    artifacts = [
        upsert_csv(
            RUN_REGISTRY,
            ["run_id"],
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "family": "tester_date_boundary_repair_review",
                "lane": "runtime_parity_repair",
                "status": status,
                "judgment": judgment,
                "primary_report": rel(REPORT_PATH),
                "path": rel(REPORT_PATH),
                "notes": f"decision={decision};next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
            },
        ),
        upsert_csv(
            STAGE_LEDGER,
            ["run_key"],
            {
                "run_key": f"{RUN_ID}__tester_date_boundary_repair_review",
                "ledger_row_id": f"{RUN_ID}__tester_date_boundary_repair_review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "family": "tester_date_boundary_repair_review",
                "work_family": "runtime_parity_repair",
                "question": "can ToDate boundary repair make MT5 tester reach repaired feature last without retuning",
                "metric_scope": "runtime_boundary_repair_probe_no_forward_decision",
                "evidence_scope": "MT5 tester logs telemetry and proxy parity",
                "kpi_scope": "diagnostic_runtime_probe_not_forward_kpi",
                "status": status,
                "judgment": judgment,
                "claim_boundary": CLAIM_BOUNDARY,
                "primary_artifact": rel(REPORT_PATH),
                "path": rel(REPORT_PATH),
                "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
                "decision": decision,
            },
        ),
    ]
    generated = now_utc()
    rows: list[dict[str, Any]] = []
    for path in artifact_paths:
        if not path_exists(path) or not io_path(path).is_file():
            continue
        suffix = path.suffix.lower()
        rows.append(
            {
                "artifact_id": f"{RUN_ID}::{rel(path)}",
                "artifact_type": suffix.lstrip(".") or "file",
                "path": rel(path),
                "artifact_path": rel(path),
                "sha256": sha256_file_lf_normalized(path) if suffix in {".csv", ".json", ".md", ".txt", ".ini", ".set", ".py"} else sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": generated,
                "notes": status,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    artifacts.append(append_csv_rows(ARTIFACT_REGISTRY, rows))
    return artifacts


def main() -> int:
    args = parse_args()
    configure_base()
    generated_at_utc = now_utc()
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    MT5_DIR.mkdir(parents=True, exist_ok=True)
    FEATURE_COPY_DIR.mkdir(parents=True, exist_ok=True)
    MODEL_COPY_DIR.mkdir(parents=True, exist_ok=True)
    TELEMETRY_DIR.mkdir(parents=True, exist_ok=True)

    parent_runtime_rows = read_csv(RUN337P_RUNTIME) if path_exists(RUN337P_RUNTIME) else []
    parent_gap_rows = read_csv(RUN337P_GAP) if path_exists(RUN337P_GAP) else []
    latest_probe = latest_us100_close(Path(args.terminal_path))
    prepared = source_attempts(args.attempt_filter)
    feature_rows = feature_last_rows(prepared)
    feature_latest = max((pd.to_datetime(row["feature_last_timestamp"], utc=True) for row in feature_rows if row.get("feature_last_timestamp")), default=pd.Timestamp("1970-01-01", tz=UTC))
    tester_to_date = target_tester_to_date(feature_latest)

    attempts, handoff_rows, materialized_artifacts = base.build_attempts(prepared, Path(args.common_files_root))
    attempts = [rewrite_attempt_to_boundary(dict(attempt), tester_to_date) for attempt in attempts]
    proxy_rows = sanitize_proxy_rows(base.build_proxy_signal_expected_rows(attempts), default_source="stage337Q_python_onnx_inference_from_boundary_repair_features")
    terminal_recovery = {"status": "skipped_materialize_only"} if args.materialize_only else stop_target_terminal_if_running(Path(args.terminal_path))
    before_offsets = log_offsets([TESTER_LOG, TESTER_AGENT_LOG, TERMINAL_LOG])

    if args.materialize_only:
        execution_result: dict[str, Any] = {
            "compile": {"status": "not_attempted_materialize_only"},
            "execution_results": [],
            "strategy_tester_reports": [],
            "terminal_extra_args": ["/portable"],
        }
    else:
        execution_result = base.execute_attempts(
            attempts,
            terminal_path=Path(args.terminal_path),
            metaeditor_path=Path(args.metaeditor_path),
            common_files_root=Path(args.common_files_root),
            tester_profile_root=Path(args.tester_profile_root),
            terminal_data_root=Path(args.terminal_data_root),
            timeout_seconds=args.timeout_seconds,
            wait_timeout_seconds=args.wait_timeout_seconds,
            materialize_only=False,
        )

    runtime_rows = base.build_fresh_runtime_summary(attempts, execution_result)
    boundary_rows = tester_boundary_rows(before_offsets, attempts, tester_to_date)
    base.copy_runtime_outputs(Path(args.common_files_root), attempts)
    gap_rows = tester_gap_rows(runtime_rows, feature_rows, Path(args.common_files_root), latest_probe)
    raw_diff_rows = sanitize_diff_rows(base.build_signal_difference_rows(proxy_rows, runtime_rows))
    cutoff_by_attempt = {str(row.get("attempt_name", "")): str(row.get("tester_last_observed_bar_time", "")) for row in gap_rows}
    aligned_proxy_rows = sanitize_proxy_rows(build_timestamp_aligned_proxy_rows(attempts, cutoff_by_attempt), default_source="stage337Q_timestamp_aligned_python_onnx_inference")
    aligned_diff_rows = sanitize_diff_rows(base.build_signal_difference_rows(aligned_proxy_rows, runtime_rows))
    asof_rows = asof_policy_review_rows()
    metrics = metric_summary(runtime_rows)
    status, judgment, decision = classify(runtime_rows, gap_rows, aligned_diff_rows, bool(args.materialize_only))
    gates = gate_rows(runtime_rows, gap_rows, raw_diff_rows, aligned_diff_rows, boundary_rows, asof_rows)

    artifact_paths: list[Path] = [
        write_json(RUN_DIR / "parent_run337P_final_decision_snapshot.json", read_json(RUN337P_DIR / "final_runtime_data_feature_source_repair_probe_decision.json")),
        write_csv(RUN_DIR / "parent_run337P_gap_snapshot.csv", list(parent_gap_rows[0].keys()) if parent_gap_rows else ["status"], parent_gap_rows or [{"status": "missing"}]),
        write_csv(RUN_DIR / "parent_run337P_runtime_snapshot.csv", list(parent_runtime_rows[0].keys()) if parent_runtime_rows else ["status"], parent_runtime_rows or [{"status": "missing"}]),
        write_json(RUN_DIR / "fresh_us100_api_probe.json", latest_probe),
        write_json(RUN_DIR / "terminal_process_recovery.json", terminal_recovery),
        write_csv(
            RUN_DIR / "feature_last_timestamp_audit.csv",
            ["attempt_name", "feature_set_id", "feature_rows", "feature_first_timestamp", "feature_last_timestamp", "feature_csv_path", "feature_csv_sha256", "claim_boundary"],
            feature_rows,
        ),
        write_csv(
            RUN_DIR / "tester_date_boundary_log_audit.csv",
            ["attempt_name", "requested_to_date", "log_test_from", "log_test_to", "history_sync_from", "history_sync_to", "tick_sync_from", "tick_sync_to", "generated_ticks", "generated_bars", "source", "effect", "claim_boundary"],
            boundary_rows,
        ),
        write_csv(
            RUN_DIR / "asof_source_policy_review.csv",
            ["feature_set_id", "required_symbol", "latest_row_asof_age_minutes", "rows_over_max_age", "source_policy_judgment", "usable_for_runtime_probe", "usable_for_forward_pass_fail", "effect", "claim_boundary"],
            asof_rows,
        ),
        write_json(RUN_DIR / "boundary_repair_handoff_attempts.json", attempts),
        write_csv(
            RUN_DIR / "boundary_repair_handoff_attempt_manifest.csv",
            [
                "attempt_name",
                "artifact_slug",
                "source_set_path",
                "source_ini_path",
                "new_set_path",
                "new_ini_path",
                "source_model_path",
                "new_model_path",
                "source_feature_path",
                "new_feature_path",
                "model_common_path",
                "feature_common_path",
                "telemetry_common_path",
                "summary_common_path",
                "threshold_keys_unchanged",
                "risk_lot_keys_unchanged",
                "allowed_identity_keys_changed",
                "source_set_sha256",
                "new_set_sha256",
                "source_ini_sha256",
                "new_ini_sha256",
                "model_sha256",
                "feature_sha256",
                "materialization_status",
                "claim_boundary",
            ],
            handoff_rows,
        ),
        write_json(RUN_DIR / "runtime_execution_result.json", execution_result),
        write_csv(
            RUN_DIR / "fresh_mt5_runtime_probe_result.csv",
            [
                "attempt_name",
                "artifact_slug",
                "feature_set_id",
                "tester_status",
                "runtime_status",
                "report_status",
                "returncode",
                "blocker",
                "feature_ready_count",
                "model_ok_count",
                "tier_a_long_count",
                "tier_a_short_count",
                "tier_a_flat_count",
                "long_count",
                "short_count",
                "flat_count",
                "no_tier_count",
                "last_skip_reason",
                "order_attempt_count",
                "order_fill_count",
                "net_profit",
                "profit_factor",
                "trade_count",
                "expectancy",
                "recovery_factor",
                "max_drawdown_amount",
                "short_trade_count",
                "long_trade_count",
                "common_summary_path",
                "common_telemetry_path",
                "report_name",
                "report_path",
                "claim_boundary",
            ],
            runtime_rows,
        ),
        write_csv(
            RUN_DIR / "tester_feature_last_gap_reprobe.csv",
            ["attempt_name", "feature_set_id", "runtime_status", "report_status", "api_latest_us100_close_utc", "feature_last_timestamp", "tester_last_observed_bar_time", "tester_to_feature_last_gap_minutes", "tester_to_api_latest_gap_minutes", "telemetry_rows", "last_skip_reason", "gap_status", "claim_boundary"],
            gap_rows,
        ),
        write_csv(
            RUN_DIR / "proxy_expected_result.csv",
            [
                "attempt_name",
                "artifact_slug",
                "feature_set_id",
                "model_id",
                "expected_feature_ready_count",
                "expected_model_ok_count",
                "expected_short_count",
                "expected_long_count",
                "expected_flat_count",
                "expected_signal_count",
                "expected_signal_rate",
                "expected_long_share",
                "mean_p_short",
                "mean_p_flat",
                "mean_p_long",
                "mean_probability_margin",
                "max_probability_row_sum_abs_error",
                "feature_order_hash",
                "feature_csv_sha256",
                "model_sha256",
                "threshold_policy",
                "proxy_source",
                "claim_boundary",
            ],
            proxy_rows,
        ),
        write_csv(
            RUN_DIR / "timestamp_aligned_proxy_expected_result.csv",
            [
                "attempt_name",
                "artifact_slug",
                "feature_set_id",
                "model_id",
                "expected_feature_ready_count",
                "expected_model_ok_count",
                "expected_short_count",
                "expected_long_count",
                "expected_flat_count",
                "expected_signal_count",
                "expected_signal_rate",
                "expected_long_share",
                "mean_p_short",
                "mean_p_flat",
                "mean_p_long",
                "mean_probability_margin",
                "max_probability_row_sum_abs_error",
                "feature_order_hash",
                "feature_csv_sha256",
                "model_sha256",
                "threshold_policy",
                "proxy_source",
                "proxy_cutoff_utc",
                "proxy_row_scope",
                "full_feature_rows",
                "timestamp_aligned_feature_rows",
                "claim_boundary",
            ],
            aligned_proxy_rows,
        ),
        write_csv(
            RUN_DIR / "proxy_mt5_difference.csv",
            ["attempt_name", "artifact_slug", "dimension", "proxy_expected_value", "mt5_runtime_value", "difference_proxy_minus_mt5", "difference_status", "proxy_source", "mt5_source", "usable_for_runtime_signal_parity", "usable_for_forward_pass_fail", "runtime_skip_reason", "claim_boundary"],
            raw_diff_rows,
        ),
        write_csv(
            RUN_DIR / "timestamp_aligned_proxy_mt5_difference.csv",
            ["attempt_name", "artifact_slug", "dimension", "proxy_expected_value", "mt5_runtime_value", "difference_proxy_minus_mt5", "difference_status", "proxy_source", "mt5_source", "usable_for_runtime_signal_parity", "usable_for_forward_pass_fail", "runtime_skip_reason", "claim_boundary"],
            aligned_diff_rows,
        ),
        write_csv(
            RUN_DIR / "runtime_metric_summary.csv",
            ["attempt_name", "feature_set_id", "runtime_status", "report_status", "net_profit", "profit_factor", "trade_count", "expectancy", "recovery_factor", "max_drawdown_amount", "long_trade_count", "short_trade_count", "lot_normalized_net_per_trade", "claim_boundary"],
            metrics,
        ),
        write_csv(RUN_DIR / "required_gate_coverage_audit.csv", ["gate_name", "status", "evidence_path", "effect"], gates),
        write_json(
            RUN_DIR / "tester_settings_identity.json",
            {
                "run_id": RUN_ID,
                "parent_run_id": PARENT_RUN_ID,
                "requested_tester_to_date": tester_to_date,
                "feature_latest_timestamp": feature_latest.isoformat().replace("+00:00", "Z"),
                "terminal_path": str(args.terminal_path),
                "terminal_data_root": str(args.terminal_data_root),
                "common_files_root": str(args.common_files_root),
                "queued_attempts": [attempt["attempt_name"] for attempt in attempts],
                "model_training": "forbidden_not_performed",
                "threshold_retuning": "forbidden_not_performed",
                "lot_optimization": "forbidden_not_performed",
                "only_change": "tester_to_date_boundary_probe",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
    ]
    artifact_paths.extend(materialized_artifacts)
    artifact_paths.extend(base.copy_runtime_outputs(Path(args.common_files_root), attempts))
    artifact_paths.extend(copy_reports_to_required_names(runtime_rows))
    artifact_paths.extend(build_receipts(status, judgment, decision, runtime_rows, gap_rows, aligned_diff_rows))
    artifact_paths.append(write_report(status, judgment, decision, latest_probe, runtime_rows, gap_rows, raw_diff_rows, aligned_diff_rows, asof_rows))
    artifact_paths.append(write_decision_doc(status, judgment, decision, latest_probe))
    artifact_paths.extend(update_status_docs(status, decision, runtime_rows, gap_rows, aligned_diff_rows))

    completed = sum(1 for row in runtime_rows if row.get("tester_status") == "completed" and row.get("runtime_status") == "completed" and row.get("report_status") == "completed")
    reached = sum(1 for row in gap_rows if row.get("gap_status") == "tester_reached_feature_last")
    raw_matches = sum(1 for row in raw_diff_rows if str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true")
    aligned_matches = sum(1 for row in aligned_diff_rows if str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true")
    final_decision = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": status,
        "judgment": judgment,
        "decision": decision,
        "api_latest_us100_close_utc": latest_probe.get("last_close_utc", ""),
        "feature_latest_timestamp": feature_latest.isoformat().replace("+00:00", "Z"),
        "requested_tester_to_date": tester_to_date,
        "runtime_completed": completed,
        "runtime_total": len(runtime_rows),
        "tester_reached_feature_last": reached,
        "tester_gap_total": len(gap_rows),
        "signal_parity_matched_rows": raw_matches,
        "signal_parity_total_rows": len(raw_diff_rows),
        "timestamp_aligned_signal_parity_matched_rows": aligned_matches,
        "timestamp_aligned_signal_parity_total_rows": len(aligned_diff_rows),
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    artifact_paths.append(write_json(RUN_DIR / "final_tester_date_boundary_repair_review_decision.json", final_decision))
    artifact_paths.extend(update_registers(status, judgment, decision, [*artifact_paths, Path(__file__)]))
    artifact_paths.append(
        write_json(
            RUN_DIR / "run_manifest.json",
            {
                **final_decision,
                "generated_at_utc": generated_at_utc,
                "command": "python stage_pipelines/stage337/review_runtime_data_and_feature_source_repair_probe.py",
                "materialize_only": bool(args.materialize_only),
                "attempt_filter": args.attempt_filter,
                "artifacts": [rel(path) for path in artifact_paths if path_exists(path)],
            },
        )
    )
    print(json.dumps(final_decision, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
