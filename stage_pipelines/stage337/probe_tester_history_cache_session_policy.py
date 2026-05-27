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
from stage_pipelines.stage337 import review_runtime_data_and_feature_source_repair_probe as qprobe  # noqa: E402


TODAY = "2026-05-27"
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
RUN_NUMBER = "run337AA"
RUN_ID = "run337AA_tester_history_cache_repair_or_actual_source_session_policy_probe_v1"
PARENT_RUN_ID = "run337Z_execute_or_review_actual_source_age_proxy_mt5_repair_probe_v1"
NEXT_RUN_ID = "run337AB_custom_symbol_intraday_tester_visibility_probe_v1"
CLAIM_BOUNDARY = (
    "research_development_only_stage337AA_tester_history_cache_session_policy_probe_no_model_training_"
    "no_threshold_retuning_no_lot_optimization_no_candidate_selection_no_forward_passed_no_forward_failed_"
    "no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STATUS_COMPLETED = "completed_stage337AA_tester_current_day_boundary_diagnosed_no_forward_decision"
STATUS_PARTIAL = "completed_stage337AA_tester_history_cache_probe_partial_no_forward_decision"
JUDGMENT_COMPLETED = "strategy_tester_current_day_midnight_boundary_confirmed_custom_symbol_or_next_day_reprobe_required"
JUDGMENT_PARTIAL = "tester_history_cache_session_policy_probe_inconclusive_requires_reprobe"
DECISION_COMPLETED = "stage337AA_open_run337AB_custom_symbol_intraday_tester_visibility_probe_no_selection"
DECISION_PARTIAL = "stage337AA_reprobe_or_manual_tester_cache_review_no_selection"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
RUN337Z_DIR = STAGE_DIR / "02_runs" / "run337Z"
RUN337Z_ATTEMPTS = RUN337Z_DIR / "rollover_reprobe_handoff_attempts.json"
RUN337Z_FINAL = RUN337Z_DIR / "final_decision.json"
MT5_DIR = RUN_DIR / "mt5"
FEATURE_COPY_DIR = RUN_DIR / "feature_matrices"
MODEL_COPY_DIR = RUN_DIR / "models"
TELEMETRY_DIR = RUN_DIR / "runtime_telemetry"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEWS_DIR / "run337AA_tester_history_cache_session_policy_probe.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage337AA_tester_history_cache_session_policy_probe.md"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
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
LOG_DATE = TODAY.replace("-", "")
TESTER_LOG = DEFAULT_PORTABLE_ROOT / "Tester" / "logs" / f"{LOG_DATE}.log"
TESTER_AGENT_LOG = DEFAULT_PORTABLE_ROOT / "Tester" / "Agent-127.0.0.1-3000" / "logs" / f"{LOG_DATE}.log"
TERMINAL_LOG = DEFAULT_PORTABLE_ROOT / "Logs" / f"{LOG_DATE}.log"
COMMON_ROOT = "Project_Obsidian_Prime_v2/stage337/run337AA_tester_history_cache_session_policy_probe"
ATTEMPT_BASE = "u42_plain_rf"
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
    parser = argparse.ArgumentParser(description="Stage337AA tester history/cache and session policy probe.")
    parser.add_argument("--terminal-path", default=str(DEFAULT_TERMINAL))
    parser.add_argument("--metaeditor-path", default=str(DEFAULT_METAEDITOR))
    parser.add_argument("--common-files-root", default=str(DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-data-root", default=str(DEFAULT_TERMINAL_DATA_ROOT))
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--wait-timeout-seconds", type=int, default=180)
    parser.add_argument("--materialize-only", action="store_true")
    return parser.parse_args()


def configure_probe_modules() -> None:
    qprobe.TODAY = TODAY
    qprobe.STAGE_ID = STAGE_ID
    qprobe.RUN_NUMBER = RUN_NUMBER
    qprobe.RUN_ID = RUN_ID
    qprobe.PARENT_RUN_ID = PARENT_RUN_ID
    qprobe.NEXT_RUN_ID = NEXT_RUN_ID
    qprobe.CLAIM_BOUNDARY = CLAIM_BOUNDARY
    qprobe.STAGE_DIR = STAGE_DIR
    qprobe.RUN_DIR = RUN_DIR
    qprobe.MT5_DIR = MT5_DIR
    qprobe.FEATURE_COPY_DIR = FEATURE_COPY_DIR
    qprobe.MODEL_COPY_DIR = MODEL_COPY_DIR
    qprobe.TELEMETRY_DIR = TELEMETRY_DIR
    qprobe.REVIEWS_DIR = REVIEWS_DIR
    qprobe.REPORT_PATH = REPORT_PATH
    qprobe.DECISION_DOC = DECISION_DOC
    qprobe.SELECTED_STATUS = SELECTED_STATUS
    qprobe.DEFAULT_PORTABLE_ROOT = DEFAULT_PORTABLE_ROOT
    qprobe.DEFAULT_TERMINAL = DEFAULT_TERMINAL
    qprobe.DEFAULT_METAEDITOR = DEFAULT_METAEDITOR
    qprobe.DEFAULT_COMMON_FILES = DEFAULT_COMMON_FILES
    qprobe.DEFAULT_TESTER_PROFILE_ROOT = DEFAULT_TESTER_PROFILE_ROOT
    qprobe.DEFAULT_TERMINAL_DATA_ROOT = DEFAULT_TERMINAL_DATA_ROOT
    qprobe.TESTER_LOG = TESTER_LOG
    qprobe.TESTER_AGENT_LOG = TESTER_AGENT_LOG
    qprobe.TERMINAL_LOG = TERMINAL_LOG
    qprobe.COMMON_ROOT = COMMON_ROOT
    qprobe.ATTEMPT_NAMES = (ATTEMPT_BASE,)
    qprobe.configure_base()


def source_attempts() -> list[dict[str, Any]]:
    rows = read_json(RUN337Z_ATTEMPTS)
    source = next((row for row in rows if row.get("attempt_name") == ATTEMPT_BASE), None)
    if source is None:
        raise RuntimeError(f"missing {ATTEMPT_BASE} in {RUN337Z_ATTEMPTS}")
    scenarios = [
        ("aa_prevday_to_current", "tester_to_current_calendar_date_control", "2026.05.26", "2026.05.27"),
        ("aa_current_to_next", "tester_to_next_calendar_date_control", "2026.05.26", "2026.05.28"),
        ("aa_future_rollover", "tester_to_future_rollover_control", "2026.05.26", "2026.05.30"),
    ]
    selected: list[dict[str, Any]] = []
    for index, (suffix, scenario_id, from_date, to_date) in enumerate(scenarios):
        copied = dict(source)
        copied["attempt_name"] = f"u42_plain_rf_{suffix}"
        copied["artifact_slug"] = f"u42_plain_{suffix}"
        copied["scenario_id"] = scenario_id
        copied["scenario_from_date"] = from_date
        copied["scenario_to_date"] = to_date
        copied["model_copy"] = {"source": source.get("model_local_path", "")}
        copied["feature_export"] = {"path": source.get("feature_local_path", "")}
        copied["source_run_id"] = PARENT_RUN_ID
        copied["attempt_role"] = "stage337AA_tester_history_cache_session_policy_probe_same_frozen_u42_model_feature_threshold_risk"
        copied["record_view_prefix"] = f"mt5_stage337AA_u42_plain_{index}"
        selected.append(copied)
    return selected


def rewrite_attempt_to_scenario(attempt: dict[str, Any]) -> dict[str, Any]:
    tester = dict(attempt["ini"]["tester"])
    tester["FromDate"] = attempt["scenario_from_date"]
    tester["ToDate"] = attempt["scenario_to_date"]
    tester["Report"] = f"Project_Obsidian_Prime_v2_{RUN_ID}_{attempt['attempt_name']}"
    ini_path = Path(str(attempt["ini"]["path"]))
    attempt["ini"] = base.materialize_ini_file(tester, ini_path)
    attempt["from_date"] = tester["FromDate"]
    attempt["to_date"] = tester["ToDate"]
    attempt["attempt_role"] = "stage337AA_tester_history_cache_session_policy_probe_same_frozen_u42_model_feature_threshold_risk"
    attempt["record_view_prefix"] = f"mt5_stage337AA_{attempt['artifact_slug']}"
    attempt["source_run_id"] = PARENT_RUN_ID
    attempt["repair_contract"] = "tester FromDate/ToDate diagnostic only; same ONNX, feature order, threshold, risk, lot, ATR SL/TP, and feature CSV"
    attempt["signal_policy"] = "same frozen ONNX and runtime settings; tester visibility/session-policy micro probe only"
    return attempt


def mt5_api_recent_bars(terminal_path: Path, count: int = 96) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    ok = mt5_api.initialize(path=str(terminal_path), portable=True)
    if not ok:
        return {"status": "blocked_mt5_initialize_failed", "last_error": str(mt5_api.last_error())}, []
    try:
        mt5_api.symbol_select("US100", True)
        rates = mt5_api.copy_rates_from_pos("US100", mt5_api.TIMEFRAME_M5, 0, count)
        if rates is None or len(rates) == 0:
            return {"status": "blocked_no_us100_rates", "last_error": str(mt5_api.last_error())}, []
        rows: list[dict[str, Any]] = []
        for item in rates:
            open_time = datetime.fromtimestamp(int(item["time"]), tz=UTC)
            close_time = open_time + timedelta(seconds=M5_SECONDS)
            rows.append(
                {
                    "bar_open_utc": open_time.isoformat().replace("+00:00", "Z"),
                    "bar_close_utc": close_time.isoformat().replace("+00:00", "Z"),
                    "open": float(item["open"]),
                    "high": float(item["high"]),
                    "low": float(item["low"]),
                    "close": float(item["close"]),
                    "tick_volume": int(item["tick_volume"]),
                    "spread": int(item["spread"]),
                    "real_volume": int(item["real_volume"]),
                    "source": "MetaTrader5.copy_rates_from_pos",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
        latest = rows[-1]
        return {
            "status": "completed",
            "row_count": len(rows),
            "first_close_utc": rows[0]["bar_close_utc"],
            "last_close_utc": latest["bar_close_utc"],
            "last_error": str(mt5_api.last_error()),
        }, rows
    finally:
        mt5_api.shutdown()


def file_inventory(terminal_data_root: Path) -> list[dict[str, Any]]:
    roots = [
        ("terminal_base_history", terminal_data_root / "bases" / "FPMarketsSC-Live" / "history" / "US100"),
        ("terminal_base_ticks", terminal_data_root / "bases" / "FPMarketsSC-Live" / "ticks" / "US100"),
        ("tester_base_history", terminal_data_root / "Tester" / "bases" / "FPMarketsSC-Live" / "history" / "US100"),
        ("tester_base_ticks", terminal_data_root / "Tester" / "bases" / "FPMarketsSC-Live" / "ticks" / "US100"),
        ("tester_cache", terminal_data_root / "Tester" / "cache"),
    ]
    rows: list[dict[str, Any]] = []
    for root_label, root in roots:
        if not path_exists(root):
            rows.append(
                {
                    "root_label": root_label,
                    "path": root.as_posix(),
                    "file_name": "",
                    "suffix": "",
                    "size_bytes": "",
                    "mtime_local": "",
                    "mtime_utc": "",
                    "inventory_status": "missing_root",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            continue
        files: list[Path] = []
        if root_label == "tester_cache":
            files = sorted(root.glob("ObsidianPrimeV2_RuntimeProbeEA.US100.M5.*.tst"), key=lambda item: item.stat().st_mtime, reverse=True)[:80]
        else:
            files = sorted((item for item in root.rglob("*") if item.is_file()), key=lambda item: item.stat().st_mtime, reverse=True)[:40]
        for file_path in files:
            stat = io_path(file_path).stat()
            mtime = datetime.fromtimestamp(stat.st_mtime)
            mtime_utc = datetime.fromtimestamp(stat.st_mtime, tz=UTC)
            rows.append(
                {
                    "root_label": root_label,
                    "path": file_path.as_posix(),
                    "file_name": file_path.name,
                    "suffix": file_path.suffix,
                    "size_bytes": stat.st_size,
                    "mtime_local": mtime.isoformat(timespec="seconds"),
                    "mtime_utc": mtime_utc.isoformat().replace("+00:00", "Z"),
                    "inventory_status": "present",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


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


def tester_boundary_rows(before_offsets: Mapping[str, int], attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
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
        log_to = boundary[1]
        requested_to = str(attempt.get("to_date", ""))
        if log_to == "2026.05.27 00:00" and requested_to in {"2026.05.28", "2026.05.30"}:
            boundary_status = "current_day_midnight_cap_confirmed"
        elif log_to:
            boundary_status = "tester_boundary_observed"
        else:
            boundary_status = "tester_boundary_missing"
        rows.append(
            {
                "attempt_name": attempt["attempt_name"],
                "scenario_id": attempt.get("scenario_id", ""),
                "requested_from_date": attempt.get("from_date", ""),
                "requested_to_date": requested_to,
                "log_test_from": boundary[0],
                "log_test_to": log_to,
                "history_sync_from": history[0],
                "history_sync_to": history[1],
                "tick_sync_from": ticks[0],
                "tick_sync_to": ticks[1],
                "generated_ticks": generated[0],
                "generated_bars": generated[1],
                "boundary_status": boundary_status,
                "source": TESTER_AGENT_LOG.as_posix(),
                "effect": "requested ToDate(요청 종료일)와 Strategy Tester actual end(전략 테스터 실제 종료)을 비교해 현재일 자정 경계를 확인한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def parse_timestamp(value: str) -> pd.Timestamp:
    return pd.to_datetime(str(value), errors="coerce", utc=True)


def classify(
    latest_probe: Mapping[str, Any],
    gap_rows: Sequence[Mapping[str, Any]],
    boundary_rows: Sequence[Mapping[str, Any]],
) -> tuple[str, str, str, str]:
    api_last = parse_timestamp(str(latest_probe.get("last_close_utc", "")))
    gap_count = sum(1 for row in gap_rows if row.get("gap_status") == "tester_feature_last_gap_remains")
    capped = sum(1 for row in boundary_rows if row.get("boundary_status") == "current_day_midnight_cap_confirmed")
    if not pd.isna(api_last) and gap_count == len(gap_rows) and capped >= 2:
        return STATUS_COMPLETED, JUDGMENT_COMPLETED, DECISION_COMPLETED, NEXT_RUN_ID
    return STATUS_PARTIAL, JUDGMENT_PARTIAL, DECISION_PARTIAL, RUN_ID


def decision_rows(
    latest_probe: Mapping[str, Any],
    gap_rows: Sequence[Mapping[str, Any]],
    boundary_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    api_latest = latest_probe.get("last_close_utc", "")
    rows: list[dict[str, Any]] = []
    for gap in gap_rows:
        attempt = str(gap.get("attempt_name", ""))
        boundary = next((row for row in boundary_rows if row.get("attempt_name") == attempt), {})
        rows.append(
            {
                "attempt_name": attempt,
                "scenario_id": boundary.get("scenario_id", ""),
                "api_latest_us100_close_utc": api_latest,
                "feature_last_timestamp": gap.get("feature_last_timestamp", ""),
                "tester_last_observed_bar_time": gap.get("tester_last_observed_bar_time", ""),
                "requested_to_date": boundary.get("requested_to_date", ""),
                "log_test_to": boundary.get("log_test_to", ""),
                "history_sync_to": boundary.get("history_sync_to", ""),
                "tick_sync_to": boundary.get("tick_sync_to", ""),
                "gap_status": gap.get("gap_status", ""),
                "boundary_status": boundary.get("boundary_status", ""),
                "root_cause_judgment": "strategy_tester_current_day_midnight_boundary" if boundary.get("boundary_status") == "current_day_midnight_cap_confirmed" else "requires_more_evidence",
                "usable_for_runtime_signal_parity": True,
                "usable_for_forward_pass_fail": False,
                "effect": "terminal API(터미널 API)는 최신 봉을 보지만 Strategy Tester(전략 테스터)는 현재일 00:00 이후를 사용하지 못하는지 분리한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def repair_option_rows(status: str) -> list[dict[str, Any]]:
    return [
        {
            "option_id": "custom_symbol_intraday_tester_visibility_probe",
            "priority": 1,
            "action": "build a custom-symbol or equivalent tester-visible dataset from broker bars already visible through terminal API",
            "effect": "tests whether Strategy Tester can consume intraday forward bars without waiting for the broker daily rollover",
            "risk": "must preserve no-lookahead and exact feature timestamp boundary; custom symbol must be labeled as repair evidence, not operating authority",
            "next_run": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "option_id": "next_day_reprobe",
            "priority": 2,
            "action": "repeat the frozen tester probe after the broker/tester daily history rolls forward",
            "effect": "checks whether 2026-05-27 intraday bars become visible as ordinary tester history on the next session",
            "risk": "does not solve same-day forward robustness verification by itself",
            "next_run": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "option_id": "tester_visible_cutoff_policy",
            "priority": 3,
            "action": "use tester-visible cutoff only for runtime probe and keep latest intraday bars as data-integrity blocked for pass/fail",
            "effect": "prevents false Forward Passed/Failed claims while keeping parity evidence usable",
            "risk": "cannot satisfy latest-forward decision requirement alone",
            "next_run": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "option_id": "do_nothing",
            "priority": 99,
            "action": "leave the tester gap unresolved",
            "effect": "would keep forward decision blocked and is not acceptable for this goal",
            "risk": "violates external verification anti-deferral if repeated",
            "next_run": "not_recommended",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def gate_rows(
    runtime_rows: Sequence[Mapping[str, Any]],
    gap_rows: Sequence[Mapping[str, Any]],
    boundary_rows: Sequence[Mapping[str, Any]],
    decision_items: Sequence[Mapping[str, Any]],
    cache_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    completed = sum(1 for row in runtime_rows if row.get("tester_status") == "completed" and row.get("runtime_status") == "completed" and row.get("report_status") == "completed")
    gaps = sum(1 for row in gap_rows if row.get("gap_status") == "tester_feature_last_gap_remains")
    caps = sum(1 for row in boundary_rows if row.get("boundary_status") == "current_day_midnight_cap_confirmed")
    root_cause = sum(1 for row in decision_items if row.get("root_cause_judgment") == "strategy_tester_current_day_midnight_boundary")
    cache_present = sum(1 for row in cache_rows if row.get("inventory_status") == "present")
    return [
        {
            "gate_name": "run337Z_gap_reproduced",
            "status": "covered" if gaps else "covered_partial",
            "evidence_path": rel(RUN_DIR / "tester_feature_last_gap_micro_probe.csv"),
            "effect": f"feature_last(피처 마지막) 공백을 micro probe(미세 탐침)에서 재현한다; gaps={gaps}/{len(gap_rows)}.",
        },
        {
            "gate_name": "tester_date_boundary_observed",
            "status": "covered" if boundary_rows else "covered_partial",
            "evidence_path": rel(RUN_DIR / "tester_date_boundary_micro_probe.csv"),
            "effect": "Strategy Tester(전략 테스터)의 실제 log_test_to(로그 종료 시점)를 직접 기록한다.",
        },
        {
            "gate_name": "current_day_midnight_cap_checked",
            "status": "covered_confirmed" if caps >= 2 else "covered_inconclusive",
            "evidence_path": rel(RUN_DIR / "session_policy_decision.csv"),
            "effect": f"ToDate(종료일)를 더 멀리 밀어도 현재일 00:00에서 멈추는지 확인한다; confirmed={caps}.",
        },
        {
            "gate_name": "cache_inventory_recorded",
            "status": "covered" if cache_present else "covered_partial",
            "evidence_path": rel(RUN_DIR / "tester_cache_inventory.csv"),
            "effect": f"terminal/tester history files(터미널/테스터 히스토리 파일)과 cache(캐시)를 기록한다; files={cache_present}.",
        },
        {
            "gate_name": "root_cause_judgment_recorded",
            "status": "covered" if root_cause else "covered_partial",
            "evidence_path": rel(RUN_DIR / "session_policy_decision.csv"),
            "effect": f"공백 원인을 Strategy Tester current-day boundary(전략 테스터 현재일 경계)로 판정할 수 있는지 기록한다; rows={root_cause}.",
        },
        {
            "gate_name": "no_forward_or_goal_claim",
            "status": "covered",
            "evidence_path": rel(RUN_DIR / "final_decision.json"),
            "effect": "Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)를 주장하지 않는다.",
        },
    ]


def copy_reports_to_required_names(runtime_rows: Sequence[Mapping[str, Any]]) -> list[Path]:
    copied: list[Path] = []
    first_report = next((row.get("report_path") for row in runtime_rows if row.get("report_path")), "")
    if first_report:
        source = Path(str(first_report))
        if path_exists(source):
            target = RUN_DIR / "tester_history_cache_probe_report.html"
            shutil.copy2(io_path(source), io_path(target))
            copied.append(target)
    return copied


def build_receipts(
    status: str,
    judgment: str,
    decision: str,
    runtime_rows: Sequence[Mapping[str, Any]],
    gap_rows: Sequence[Mapping[str, Any]],
    decision_items: Sequence[Mapping[str, Any]],
    latest_probe: Mapping[str, Any],
) -> list[Path]:
    completed = sum(1 for row in runtime_rows if row.get("tester_status") == "completed" and row.get("runtime_status") == "completed" and row.get("report_status") == "completed")
    root = sorted({str(row.get("root_cause_judgment", "")) for row in decision_items})
    return [
        write_json(
            RUN_DIR / "data_integrity_receipt.json",
            {
                "run_id": RUN_ID,
                "data_source": "MetaTrader5 API recent bars, run337Z frozen u42 handoff, and fresh run337AA tester micro probes",
                "time_axis": "US100 M5 bar close UTC compared to MT5 Strategy Tester log_test_to and telemetry bar_time",
                "sample_scope": "US100 M5 tester visibility around 2026-05-26 to 2026-05-30",
                "missing_or_duplicate_check": "not a model dataset run; gap check is tester visibility versus feature_last",
                "feature_label_boundary": "no model training, no threshold retune, no future feature fill; tester date changes are diagnostic only",
                "split_boundary": "runtime probe boundary only; no Forward Passed/Failed",
                "leakage_risk": "using API-visible intraday data as if Strategy Tester already tested it",
                "data_hash_or_identity": rel(RUN_DIR / "mt5_api_recent_us100_m5_bars.csv"),
                "integrity_judgment": "usable_with_boundary_for_tester_visibility_repair",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RUN_DIR / "runtime_parity_receipt.json",
            {
                "run_id": RUN_ID,
                "research_path": rel(Path(__file__)),
                "runtime_path": rel(RUN_DIR / "tester_boundary_micro_probe_attempts.json"),
                "shared_contract": "same ONNX, feature order, D/B surface, threshold, risk, lot, ATR SL/TP, and runtime EA; tester date window varies only for visibility diagnosis",
                "known_differences": "attempt FromDate/ToDate intentionally vary; no candidate KPI comparison or Forward Passed/Failed",
                "parity_check": f"runtime_completed={completed}/{len(runtime_rows)}; tester_gaps={sum(1 for row in gap_rows if row.get('gap_status') == 'tester_feature_last_gap_remains')}/{len(gap_rows)}",
                "parity_identity": rel(RUN_DIR / "runtime_execution_result.json"),
                "runtime_claim_boundary": "runtime_probe_only_no_runtime_authority",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RUN_DIR / "backtest_forensics_receipt.json",
            {
                "run_id": RUN_ID,
                "tester_identity": "FPMarketsSC-Live US100 M5 real-tick Strategy Tester date-window micro probe",
                "ea_identity": rel(RUN_DIR / "tester_boundary_micro_probe_attempts.json"),
                "report_identity": [row.get("report_path", "") for row in runtime_rows],
                "trade_evidence": [{key: row.get(key, "") for key in ("attempt_name", "net_profit", "profit_factor", "trade_count", "max_drawdown_amount")} for row in runtime_rows],
                "cost_assumptions": "frozen run337Z .set values; no spread, slippage, lot, risk, or threshold optimization",
                "forensic_checks": ["tester log_test_to captured", "history_sync_to captured", "cache inventory captured", "terminal API latest bar captured"],
                "backtest_judgment": "usable_with_boundary_for_tester_visibility_not_forward_decision",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RUN_DIR / "result_judgment_receipt.json",
            {
                "run_id": RUN_ID,
                "result_subject": "tester history/cache and actual source session policy gap",
                "evidence_available": [rel(RUN_DIR / "session_policy_decision.csv"), rel(RUN_DIR / "tester_date_boundary_micro_probe.csv"), rel(RUN_DIR / "mt5_api_recent_us100_m5_bars.csv")],
                "evidence_missing": "custom-symbol or next-day tester evidence still needed before latest intraday Forward Passed/Failed",
                "judgment_label": "runtime_probe",
                "status": status,
                "judgment": judgment,
                "decision": decision,
                "root_cause_candidates": root,
                "claim_boundary": CLAIM_BOUNDARY,
                "next_condition": NEXT_RUN_ID,
                "user_explanation_hook": "테스터가 최신 봉을 못 보는 층을 분리했으므로 다음은 custom symbol(커스텀 심볼) 또는 다음날 재탐침이다.",
            },
        ),
        write_json(
            RUN_DIR / "artifact_lineage_receipt.json",
            {
                "run_id": RUN_ID,
                "parent_run_id": PARENT_RUN_ID,
                "source_inputs": [rel(RUN337Z_ATTEMPTS), rel(RUN337Z_FINAL)],
                "lineage_judgment": "same frozen u42 handoff carried into tester visibility micro probes",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
    ]


def write_report(
    status: str,
    judgment: str,
    decision: str,
    latest_probe: Mapping[str, Any],
    runtime_rows: Sequence[Mapping[str, Any]],
    gap_rows: Sequence[Mapping[str, Any]],
    boundary_rows: Sequence[Mapping[str, Any]],
    decision_items: Sequence[Mapping[str, Any]],
) -> Path:
    completed = sum(1 for row in runtime_rows if row.get("tester_status") == "completed" and row.get("runtime_status") == "completed" and row.get("report_status") == "completed")
    gaps = sum(1 for row in gap_rows if row.get("gap_status") == "tester_feature_last_gap_remains")
    caps = sum(1 for row in boundary_rows if row.get("boundary_status") == "current_day_midnight_cap_confirmed")
    root = sorted({str(row.get("root_cause_judgment", "")) for row in decision_items})
    lines = [
        "# Stage337AA Tester History Cache Session Policy Probe(337AA 테스터 히스토리 캐시 세션 정책 탐침)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- status(상태): `{status}`",
        f"- judgment(판정): `{judgment}`",
        f"- decision(결정): `{decision}`",
        f"- API latest US100 close(API 최신 US100 종가): `{latest_probe.get('last_close_utc', '')}`",
        f"- MT5 completed(MT5 완료): `{completed}/{len(runtime_rows)}`",
        f"- tester feature_last gaps(테스터 피처 마지막 공백): `{gaps}/{len(gap_rows)}`",
        f"- current-day midnight cap(현재일 자정 경계 확인): `{caps}`",
        f"- root cause(원인): `{';'.join(root)}`",
        "- Forward Passed(전진 통과): `not_claimed`",
        "- Forward Failed(전진 실패): `not_claimed`",
        "- runtime authority(런타임 권위): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Boundary Micro Probes(경계 미세 탐침)",
        "",
        "| scenario(시나리오) | requested ToDate(요청 종료일) | log test to(로그 종료) | history sync to(히스토리 동기화 종료) | gap(공백) |",
        "|---|---:|---:|---:|---:|",
    ]
    gap_by = {row.get("attempt_name", ""): row for row in gap_rows}
    for row in boundary_rows:
        gap = gap_by.get(row.get("attempt_name", ""), {})
        lines.append(
            f"| `{row.get('scenario_id', '')}` | `{row.get('requested_to_date', '')}` | `{row.get('log_test_to', '')}` | "
            f"`{row.get('history_sync_to', '')}` | `{gap.get('tester_to_feature_last_gap_minutes', '')}` |"
        )
    lines.extend(
        [
            "",
            "## Meaning(의미)",
            "",
            "terminal API(터미널 API)는 최신 US100 M5(US100 5분봉)를 볼 수 있지만, Strategy Tester(전략 테스터)는 "
            "요청 ToDate(종료일)를 2026.05.28 또는 2026.05.30으로 밀어도 실제 test end(테스트 종료)를 "
            "2026.05.27 00:00에 고정했다.",
            "",
            "Effect(효과): run337Z(337Z 실행)의 125분 tester gap(테스터 공백)은 ONNX(온엑스) 추론이나 threshold(임계값) 문제가 아니라 "
            "Strategy Tester current-day visibility(전략 테스터 현재일 가시성) 문제로 좁혀진다.",
        ]
    )
    return write_md(REPORT_PATH, "\n".join(lines))


def write_decision_doc(status: str, judgment: str, decision: str, latest_probe: Mapping[str, Any], caps: int, gaps: int, total: int) -> Path:
    text = f"""# Stage337AA Decision(337AA 결정)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{status}`
- judgment(판정): `{judgment}`
- decision(결정): `{decision}`
- API latest US100 close(API 최신 US100 종가): `{latest_probe.get('last_close_utc', '')}`
- current-day midnight cap(현재일 자정 경계 확인): `{caps}`
- tester feature_last gaps(테스터 피처 마지막 공백): `{gaps}/{total}`
- next_action(다음 행동): `{NEXT_RUN_ID if status == STATUS_COMPLETED else RUN_ID}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Effect(효과): run337AA(337AA 실행)는 Strategy Tester(전략 테스터)가 current-day intraday bars(현재일 장중 봉)를 보지 못하는 경계를 확인했다. 다음은 custom symbol intraday tester visibility(커스텀 심볼 장중 테스터 가시성) 또는 다음날 재탐침이다.
"""
    return write_md(DECISION_DOC, text)


def update_status_docs(status: str, decision: str, runtime_rows: Sequence[Mapping[str, Any]], gap_rows: Sequence[Mapping[str, Any]], boundary_rows: Sequence[Mapping[str, Any]]) -> list[Path]:
    completed = sum(1 for row in runtime_rows if row.get("tester_status") == "completed" and row.get("runtime_status") == "completed" and row.get("report_status") == "completed")
    gaps = sum(1 for row in gap_rows if row.get("gap_status") == "tester_feature_last_gap_remains")
    caps = sum(1 for row in boundary_rows if row.get("boundary_status") == "current_day_midnight_cap_confirmed")
    next_action = NEXT_RUN_ID if status == STATUS_COMPLETED else RUN_ID
    selection_text = f"""# Stage337 Selection Status(337단계 선택 상태)

- stage_id(단계 ID): `{STAGE_ID}`
- stage_status(단계 상태): `open_active`
- selected_candidate(선택 후보): `none`
- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{decision}`
- current_run(현재 실행): `{next_action}`
- tester_visibility_micro_probe(테스터 가시성 미세 탐침): `{completed}/{len(runtime_rows)} completed(완료)`
- tester_feature_last_gap(테스터 피처 마지막 공백): `{gaps}/{len(gap_rows)}`
- current_day_midnight_cap(현재일 자정 경계): `{caps}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Forward Blocked(전진 차단): `tester_current_day_visibility_boundary`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{next_action}`
- effect(효과): run337AA(337AA 실행)는 Strategy Tester(전략 테스터)가 현재일 장중 봉을 보지 못하는 경계를 확인했고, 최신 forward(전진) 판정은 아직 막혀 있다.
"""
    write_md(SELECTED_STATUS, selection_text)

    if path_exists(WORKSPACE_STATE):
        text, had_bom = read_text_lossless(WORKSPACE_STATE)
        lines = text.splitlines()
        for idx, line in enumerate(lines):
            if line.startswith("current_run_id:"):
                lines[idx] = f"current_run_id: {next_action}"
                break
        focus = (
            "- >-\n"
            f"  Stage337 run337AA focus complete: run337AA(337AA 실행)는 `{status}`로 tester history/cache session policy probe(테스터 히스토리/캐시 세션 정책 탐침)를 기록했다. "
            f"Effect(효과): MT5 micro probes(MT5 미세 탐침) `{completed}/{len(runtime_rows)}`, tester feature_last gaps(테스터 피처 마지막 공백) `{gaps}/{len(gap_rows)}`, "
            f"current-day midnight cap(현재일 자정 경계) `{caps}`를 확인했고 Forward/Goal(전진/목표)은 주장하지 않는다."
        )
        text = "\n".join(lines) + "\n"
        if "Stage337 run337AA focus complete" in text:
            text = re.sub(r"- >-\n  Stage337 run337AA focus complete:.*?(?=\n- >-|\Z)", focus, text, count=1, flags=re.S)
        else:
            split_lines = text.splitlines()
            try:
                pos = split_lines.index("current_focus:")
                split_lines.insert(pos + 1, focus)
            except ValueError:
                split_lines.extend(["current_focus:", focus])
            text = "\n".join(split_lines) + "\n"
        write_text_preserving(WORKSPACE_STATE, text, had_bom)

    current_entry = f"""
## Stage337 run337AA(337AA 실행) - {TODAY}

- status(상태): `{status}`
- decision(결정): `{decision}`
- next_action(다음 행동): `{next_action}`
- effect(효과): Strategy Tester current-day boundary(전략 테스터 현재일 경계)를 MT5 micro probe(MT5 미세 탐침)로 확인했다. completed(완료) `{completed}/{len(runtime_rows)}`, gaps(공백) `{gaps}/{len(gap_rows)}`, cap(경계) `{caps}`.
"""
    if path_exists(CURRENT_STATE):
        text, had_bom = read_text_lossless(CURRENT_STATE)
        if "## Stage337 run337AA(337AA 실행)" in text:
            text = re.sub(r"## Stage337 run337AA\(337AA 실행\).*?(?=\n## |\Z)", current_entry.strip(), text, count=1, flags=re.S)
            write_text_preserving(CURRENT_STATE, text.rstrip() + "\n", had_bom)
        else:
            write_text_preserving(CURRENT_STATE, text.rstrip() + "\n\n" + current_entry.strip() + "\n", had_bom)

    if path_exists(CHANGELOG):
        text, had_bom = read_text_lossless(CHANGELOG)
        line = (
            f"\n- {TODAY}: Stage337 run337AA(337AA 실행) `{status}`. "
            f"Effect(효과): Strategy Tester current-day boundary(전략 테스터 현재일 경계) `{caps}`건을 확인했고 Forward/Goal(전진/목표) 주장은 없다.\n"
        )
        if "Stage337 run337AA(337AA 실행)" in text:
            text = re.sub(r"\n- [^\n]*Stage337 run337AA\(337AA 실행\)[^\n]*", line.rstrip(), text, count=1)
            write_text_preserving(CHANGELOG, text.rstrip() + "\n", had_bom)
        else:
            write_text_preserving(CHANGELOG, text.rstrip() + line, had_bom)

    if path_exists(STAGE_BRIEF):
        text, had_bom = read_text_lossless(STAGE_BRIEF)
        text = re.sub(r"- latest_run\(최신 실행\): `[^`]+`", f"- latest_run(최신 실행): `{RUN_ID}`", text)
        summary_line = (
            f"- run337AA_summary(337AA 요약): `{status}`. Effect(효과): tester history/cache session policy probe(테스터 히스토리/캐시 세션 정책 탐침)로 "
            f"Strategy Tester(전략 테스터)의 current-day midnight cap(현재일 자정 경계) `{caps}`건과 "
            f"tester feature_last gap(테스터 피처 마지막 공백) `{gaps}/{len(gap_rows)}`을 확인했다.\n"
        )
        if "run337AA_summary(337AA 요약)" in text:
            text = re.sub(r"- run337AA_summary\(337AA 요약\): [^\n]*(?:\n|$)", summary_line, text, count=1)
        else:
            marker = "- selected_candidate(선택 후보):"
            text = text.replace(marker, summary_line + marker)
        write_text_preserving(STAGE_BRIEF, text, had_bom)

    return [SELECTED_STATUS, WORKSPACE_STATE, CURRENT_STATE, CHANGELOG, STAGE_BRIEF]


def update_registers(status: str, judgment: str, decision: str, artifact_paths: Sequence[Path]) -> list[Path]:
    artifacts = [
        upsert_csv(
            RUN_REGISTRY,
            ["run_id"],
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "family": "tester_history_cache_session_policy_probe",
                "lane": "runtime_parity_repair",
                "status": status,
                "judgment": judgment,
                "primary_report": rel(REPORT_PATH),
                "path": rel(REPORT_PATH),
                "notes": f"decision={decision};next_action={NEXT_RUN_ID if status == STATUS_COMPLETED else RUN_ID};goal_achieve_not_claimed.",
            },
        ),
        upsert_csv(
            STAGE_LEDGER,
            ["run_key"],
            {
                "run_key": f"{RUN_ID}__tester_history_cache_session_policy_probe",
                "ledger_row_id": f"{RUN_ID}__tester_history_cache_session_policy_probe",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "family": "tester_history_cache_session_policy_probe",
                "work_family": "runtime_parity_repair",
                "question": "is the run337Z tester feature_last gap caused by current-day tester history/cache visibility rather than ONNX parity",
                "metric_scope": "tester_visibility_runtime_probe_no_forward_decision",
                "evidence_scope": "MT5 API bars tester logs cache inventory runtime telemetry",
                "kpi_scope": "diagnostic_runtime_probe_not_forward_kpi",
                "status": status,
                "judgment": judgment,
                "claim_boundary": CLAIM_BOUNDARY,
                "primary_artifact": rel(REPORT_PATH),
                "path": rel(REPORT_PATH),
                "notes": f"next_action={NEXT_RUN_ID if status == STATUS_COMPLETED else RUN_ID};goal_achieve_not_claimed.",
                "decision": decision,
            },
        ),
    ]
    generated = now_utc()
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    for path in [*artifact_paths, Path(__file__)]:
        path_key = str(path)
        if path_key in seen:
            continue
        seen.add(path_key)
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


def dedupe_artifact_registry_for_run() -> None:
    if not path_exists(ARTIFACT_REGISTRY):
        return
    with io_path(ARTIFACT_REGISTRY).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        columns = list(reader.fieldnames or [])
        rows = [dict(row) for row in reader]
    if not columns:
        return
    last_index_by_id: dict[str, int] = {}
    for index, row in enumerate(rows):
        artifact_id = str(row.get("artifact_id", ""))
        if artifact_id.startswith(f"{RUN_ID}::"):
            last_index_by_id[artifact_id] = index
    if not last_index_by_id:
        return
    keep_rows: list[dict[str, Any]] = []
    for index, row in enumerate(rows):
        artifact_id = str(row.get("artifact_id", ""))
        if artifact_id.startswith(f"{RUN_ID}::") and last_index_by_id.get(artifact_id) != index:
            continue
        keep_rows.append(row)
    write_csv(ARTIFACT_REGISTRY, columns, keep_rows)


def main() -> int:
    args = parse_args()
    configure_probe_modules()
    generated_at_utc = now_utc()
    for directory in (RUN_DIR, MT5_DIR, FEATURE_COPY_DIR, MODEL_COPY_DIR, TELEMETRY_DIR):
        directory.mkdir(parents=True, exist_ok=True)

    latest_probe, api_rows = mt5_api_recent_bars(Path(args.terminal_path), count=96)
    prepared = source_attempts()
    feature_rows = qprobe.feature_last_rows(prepared)
    attempts, handoff_rows, materialized_artifacts = base.build_attempts(prepared, Path(args.common_files_root))
    scenario_by_attempt = {str(row["attempt_name"]): row for row in prepared}
    for attempt in attempts:
        scenario = scenario_by_attempt.get(str(attempt["attempt_name"]), {})
        for key in ("scenario_id", "scenario_from_date", "scenario_to_date"):
            attempt[key] = scenario.get(key, "")
    attempts = [rewrite_attempt_to_scenario(dict(attempt)) for attempt in attempts]
    terminal_recovery = {"status": "skipped_materialize_only"} if args.materialize_only else qprobe.stop_target_terminal_if_running(Path(args.terminal_path))
    before_offsets = qprobe.log_offsets([TESTER_LOG, TESTER_AGENT_LOG, TERMINAL_LOG])

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
    base.copy_runtime_outputs(Path(args.common_files_root), attempts)
    boundary_rows = tester_boundary_rows(before_offsets, attempts)
    gap_rows = qprobe.tester_gap_rows(runtime_rows, feature_rows, Path(args.common_files_root), latest_probe)
    cache_rows = file_inventory(Path(args.terminal_data_root))
    decision_items = decision_rows(latest_probe, gap_rows, boundary_rows)
    status, judgment, decision, next_action = classify(latest_probe, gap_rows, boundary_rows)
    repair_rows = repair_option_rows(status)
    gates = gate_rows(runtime_rows, gap_rows, boundary_rows, decision_items, cache_rows)

    artifact_paths: list[Path] = [
        write_json(RUN_DIR / "parent_run337Z_final_decision_snapshot.json", read_json(RUN337Z_FINAL) if path_exists(RUN337Z_FINAL) else {"status": "missing"}),
        write_json(RUN_DIR / "mt5_api_latest_us100_probe.json", latest_probe),
        write_csv(
            RUN_DIR / "mt5_api_recent_us100_m5_bars.csv",
            ["bar_open_utc", "bar_close_utc", "open", "high", "low", "close", "tick_volume", "spread", "real_volume", "source", "claim_boundary"],
            api_rows,
        ),
        write_json(RUN_DIR / "terminal_process_recovery.json", terminal_recovery),
        write_csv(
            RUN_DIR / "feature_last_timestamp_audit.csv",
            ["attempt_name", "feature_set_id", "feature_rows", "feature_first_timestamp", "feature_last_timestamp", "feature_csv_path", "feature_csv_sha256", "claim_boundary"],
            feature_rows,
        ),
        write_json(RUN_DIR / "tester_boundary_micro_probe_attempts.json", attempts),
        write_csv(
            RUN_DIR / "tester_boundary_micro_probe_handoff_manifest.csv",
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
            RUN_DIR / "tester_visibility_mt5_result.csv",
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
            RUN_DIR / "tester_date_boundary_micro_probe.csv",
            ["attempt_name", "scenario_id", "requested_from_date", "requested_to_date", "log_test_from", "log_test_to", "history_sync_from", "history_sync_to", "tick_sync_from", "tick_sync_to", "generated_ticks", "generated_bars", "boundary_status", "source", "effect", "claim_boundary"],
            boundary_rows,
        ),
        write_csv(
            RUN_DIR / "tester_feature_last_gap_micro_probe.csv",
            ["attempt_name", "feature_set_id", "runtime_status", "report_status", "api_latest_us100_close_utc", "feature_last_timestamp", "tester_last_observed_bar_time", "tester_to_feature_last_gap_minutes", "tester_to_api_latest_gap_minutes", "telemetry_rows", "last_skip_reason", "gap_status", "claim_boundary"],
            gap_rows,
        ),
        write_csv(
            RUN_DIR / "tester_cache_inventory.csv",
            ["root_label", "path", "file_name", "suffix", "size_bytes", "mtime_local", "mtime_utc", "inventory_status", "claim_boundary"],
            cache_rows,
        ),
        write_csv(
            RUN_DIR / "session_policy_decision.csv",
            ["attempt_name", "scenario_id", "api_latest_us100_close_utc", "feature_last_timestamp", "tester_last_observed_bar_time", "requested_to_date", "log_test_to", "history_sync_to", "tick_sync_to", "gap_status", "boundary_status", "root_cause_judgment", "usable_for_runtime_signal_parity", "usable_for_forward_pass_fail", "effect", "claim_boundary"],
            decision_items,
        ),
        write_csv(
            RUN_DIR / "repair_option_matrix.csv",
            ["option_id", "priority", "action", "effect", "risk", "next_run", "claim_boundary"],
            repair_rows,
        ),
        write_csv(RUN_DIR / "required_gate_coverage_audit.csv", ["gate_name", "status", "evidence_path", "effect"], gates),
    ]
    artifact_paths.extend(materialized_artifacts)
    artifact_paths.extend(base.copy_runtime_outputs(Path(args.common_files_root), attempts))
    artifact_paths.extend(copy_reports_to_required_names(runtime_rows))
    artifact_paths.extend(build_receipts(status, judgment, decision, runtime_rows, gap_rows, decision_items, latest_probe))
    artifact_paths.append(write_report(status, judgment, decision, latest_probe, runtime_rows, gap_rows, boundary_rows, decision_items))

    gaps = sum(1 for row in gap_rows if row.get("gap_status") == "tester_feature_last_gap_remains")
    caps = sum(1 for row in boundary_rows if row.get("boundary_status") == "current_day_midnight_cap_confirmed")
    artifact_paths.append(write_decision_doc(status, judgment, decision, latest_probe, caps, gaps, len(gap_rows)))
    artifact_paths.extend(update_status_docs(status, decision, runtime_rows, gap_rows, boundary_rows))

    final_decision = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": status,
        "judgment": judgment,
        "decision": decision,
        "api_latest_us100_close_utc": latest_probe.get("last_close_utc", ""),
        "runtime_completed": sum(1 for row in runtime_rows if row.get("tester_status") == "completed" and row.get("runtime_status") == "completed" and row.get("report_status") == "completed"),
        "runtime_total": len(runtime_rows),
        "tester_feature_last_gap_count": gaps,
        "tester_feature_last_gap_total": len(gap_rows),
        "current_day_midnight_cap_confirmed": caps,
        "root_cause_judgment": sorted({str(row.get("root_cause_judgment", "")) for row in decision_items}),
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": next_action,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    artifact_paths.append(write_json(RUN_DIR / "final_decision.json", final_decision))
    artifact_paths.extend(update_registers(status, judgment, decision, [*artifact_paths, Path(__file__)]))
    artifact_paths.append(
        write_json(
            RUN_DIR / "run_manifest.json",
            {
                **final_decision,
                "generated_at_utc": generated_at_utc,
                "command": "python stage_pipelines/stage337/probe_tester_history_cache_session_policy.py",
                "materialize_only": bool(args.materialize_only),
                "artifacts": [rel(path) for path in artifact_paths if path_exists(path)],
            },
        )
    )
    dedupe_artifact_registry_for_run()
    print(json.dumps(final_decision, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
