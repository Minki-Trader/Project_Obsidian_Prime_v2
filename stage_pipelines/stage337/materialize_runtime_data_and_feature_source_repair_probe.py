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
from foundation.mt5.runtime_artifacts import export_mt5_feature_matrix_csv, sha256_file  # noqa: E402
from stage_pipelines.stage335 import independent_proxy_mt5_probe as base  # noqa: E402
from stage_pipelines.stage329 import materialize_forward_feature_frames as stage329b  # noqa: E402
from stage_pipelines.stage336 import review_fresh_mt5_runtime_probe_and_repair_decision as run336l  # noqa: E402
from stage_pipelines.stage336 import attempt_fresh_mt5_runtime_probe_or_block as run336k  # noqa: E402
from stage_pipelines.stage336 import materialize_live_safe_feature_handoff_repair as repair  # noqa: E402


TODAY = "2026-05-27"
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
RUN_NUMBER = "run337P"
RUN_ID = "run337P_materialize_runtime_data_and_feature_source_repair_probe_v1"
PARENT_RUN_ID = "run337O_review_fresh_mt5_runtime_probe_and_core56_repair_or_attribution_queue_v1"
NEXT_RUN_ID = "run337Q_review_runtime_data_and_feature_source_repair_probe_v1"
CLAIM_BOUNDARY = (
    "research_development_only_stage337P_runtime_data_and_feature_source_repair_probe_no_model_training_"
    "no_threshold_retuning_no_lot_optimization_no_candidate_selection_no_forward_passed_no_forward_failed_"
    "no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STATUS_COMPLETED = "completed_stage337P_asof_feature_source_repair_probe_runtime_completed_tester_gap_remains_no_forward_decision"
STATUS_PARTIAL = "completed_stage337P_asof_feature_source_repair_probe_partial_no_forward_decision"
STATUS_MATERIALIZED_ONLY = "completed_stage337P_repair_probe_inputs_materialized_execution_pending_no_forward_decision"
JUDGMENT_COMPLETED = "asof_macro_core56_source_repair_runtime_probe_completed_current_day_tester_gap_requires_review"
JUDGMENT_PARTIAL = "repair_probe_materialized_or_runtime_partial_requires_review"
DECISION_COMPLETED = "stage337P_open_run337Q_repair_probe_review_no_selection"
DECISION_PARTIAL = "stage337P_open_run337Q_repair_probe_repair_review_no_selection"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
RUN337O_DIR = STAGE_DIR / "02_runs" / "run337O"
RUN337N_DIR = STAGE_DIR / "02_runs" / "run337N"
RUN336_STAGE_DIR = ROOT / "stages" / "336_onnx_research_packet__constraint_bound_repair_defense_offense_rebuild"
RUN336K_ATTEMPTS = RUN336_STAGE_DIR / "02_runs" / "run336K" / "independent_handoff_attempts.json"
RAW_REFRESH_DIR = RUN_DIR / "raw_refresh_probe"
REPAIRED_SOURCE_DIR = RUN_DIR / "asof_repaired_feature_sources"
MT5_DIR = RUN_DIR / "mt5"
FEATURE_COPY_DIR = RUN_DIR / "feature_matrices"
MODEL_COPY_DIR = RUN_DIR / "models"
TELEMETRY_DIR = RUN_DIR / "runtime_telemetry"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
REPORT_PATH = REVIEWS_DIR / "run337P_runtime_data_and_feature_source_repair_probe.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage337P_runtime_data_and_feature_source_repair_probe.md"
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
COMMON_ROOT = "Project_Obsidian_Prime_v2/stage337/run337P_runtime_data_feature_source_repair_probe"

M5_SECONDS = 300
MAX_ASOF_AGE_MINUTES = 240.0
ATTEMPT_NAMES = ("c56_bal_rf", "c56_plain_rf", "m48_bal_rf", "m48_plain_rf", "u42_plain_rf")
FEATURE_SOURCE_BY_SET = {
    "core56_no_top3_weight_features": "asof_source_repair_probe",
    "macro48_no_equity_breadth_or_top3": "asof_source_repair_probe",
    "us100_technical42_no_external": "exact_us100_current_day_tester_gap_probe",
}
ASOF_FILL_FEATURES = {
    "vix_change_1",
    "vix_zscore_20",
    "us10yr_change_1",
    "us10yr_zscore_20",
    "usdx_change_1",
    "usdx_zscore_20",
    "nvda_xnas_log_return_1",
    "aapl_xnas_log_return_1",
    "msft_xnas_log_return_1",
    "amzn_xnas_log_return_1",
    "mega8_equal_return_1",
    "mega8_pos_breadth_1",
    "mega8_dispersion_5",
    "us100_minus_mega8_equal_return_1",
}


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
    if path.name == "artifact_registry.csv":
        with disk_path(path).open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
            writer.writeheader()
            for row in rows:
                writer.writerow({column: csv_value(row.get(column, "")) for column in columns})
        return path
    target = disk_path(path)
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
    io_path(path).write_text(text, encoding=encoding)
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
    parser = argparse.ArgumentParser(description="Stage337P runtime data and feature-source repair probe.")
    parser.add_argument("--terminal-path", default=str(DEFAULT_TERMINAL))
    parser.add_argument("--metaeditor-path", default=str(DEFAULT_METAEDITOR))
    parser.add_argument("--common-files-root", default=str(DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-data-root", default=str(DEFAULT_TERMINAL_DATA_ROOT))
    parser.add_argument("--timeout-seconds", type=int, default=1200)
    parser.add_argument("--wait-timeout-seconds", type=int, default=240)
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--attempt-filter", default="", help="Comma-separated subset of c56/m48/u42 repair-probe attempts.")
    return parser.parse_args()


def configure_modules() -> None:
    for module in (base,):
        module.TODAY = TODAY
        module.STAGE_ID = STAGE_ID
        module.RUN_NUMBER = RUN_NUMBER
        module.RUN_ID = RUN_ID
        module.PARENT_RUN_ID = PARENT_RUN_ID
        module.NEXT_RUN_ID = NEXT_RUN_ID
        module.STATUS_COMPLETED = STATUS_COMPLETED
        module.STATUS_PARTIAL = STATUS_PARTIAL
        module.STATUS_MATERIALIZED_ONLY = STATUS_MATERIALIZED_ONLY
        module.JUDGMENT_COMPLETED = JUDGMENT_COMPLETED
        module.JUDGMENT_PARTIAL = JUDGMENT_PARTIAL
        module.DECISION_COMPLETED = DECISION_COMPLETED
        module.DECISION_PARTIAL = DECISION_PARTIAL
        module.CLAIM_BOUNDARY = CLAIM_BOUNDARY
        module.STAGE_DIR = STAGE_DIR
        module.RUN_DIR = RUN_DIR
        module.MT5_DIR = MT5_DIR
        module.FEATURE_COPY_DIR = FEATURE_COPY_DIR
        module.MODEL_COPY_DIR = MODEL_COPY_DIR
        module.TELEMETRY_DIR = TELEMETRY_DIR
        module.REVIEWS_DIR = REVIEWS_DIR
        module.STAGE_LEDGER = STAGE_LEDGER
        module.RUN_REGISTRY = RUN_REGISTRY
        module.ARTIFACT_REGISTRY = ARTIFACT_REGISTRY
        module.DEFAULT_PORTABLE_ROOT = DEFAULT_PORTABLE_ROOT
        module.DEFAULT_TERMINAL = DEFAULT_TERMINAL
        module.DEFAULT_METAEDITOR = DEFAULT_METAEDITOR
        module.DEFAULT_COMMON_FILES = DEFAULT_COMMON_FILES
        module.DEFAULT_TESTER_PROFILE_ROOT = DEFAULT_TESTER_PROFILE_ROOT
        module.DEFAULT_TERMINAL_DATA_ROOT = DEFAULT_TERMINAL_DATA_ROOT
        module.COMMON_ROOT = COMMON_ROOT
        module.DECISION_DOC = DECISION_DOC
        module.PORTABLE_EA_SOURCE = DEFAULT_PORTABLE_ROOT / "MQL5" / "Experts" / module.mt5.EA_SOURCE_PATH
        module.PORTABLE_EA_EX5 = DEFAULT_PORTABLE_ROOT / "MQL5" / "Experts" / "Project_Obsidian_Prime_v2" / "foundation" / "mt5" / "ObsidianPrimeV2_RuntimeProbeEA.ex5"
    run336l.FRESH_RAW_ROOT = RAW_REFRESH_DIR
    repair.TODAY = TODAY
    repair.STAGE_ID = STAGE_ID
    repair.RUN_NUMBER = RUN_NUMBER
    repair.RUN_ID = RUN_ID
    repair.PARENT_RUN_ID = PARENT_RUN_ID
    repair.NEXT_RUN_ID = NEXT_RUN_ID
    repair.CLAIM_BOUNDARY = CLAIM_BOUNDARY
    repair.STAGE_DIR = STAGE_DIR
    repair.RUN_DIR = RUN_DIR
    repair.MT5_DIR = MT5_DIR
    repair.FEATURE_COPY_DIR = FEATURE_COPY_DIR
    repair.MODEL_COPY_DIR = MODEL_COPY_DIR
    repair.TELEMETRY_DIR = TELEMETRY_DIR
    repair.REVIEWS_DIR = REVIEWS_DIR
    repair.RAW_REFRESH_DIR = RAW_REFRESH_DIR
    repair.REPAIRED_SOURCE_DIR = REPAIRED_SOURCE_DIR
    repair.COMMON_ROOT = COMMON_ROOT
    repair.patch_modules()
    run336l.FRESH_RAW_ROOT = RAW_REFRESH_DIR


def floor_m5(value: datetime) -> datetime:
    value = value.astimezone(UTC).replace(second=0, microsecond=0)
    return value - timedelta(minutes=value.minute % 5)


def init_mt5(terminal_path: Path) -> None:
    ok = mt5_api.initialize(path=str(terminal_path), portable=True)
    if not ok:
        raise RuntimeError(f"MetaTrader5 initialize failed: {mt5_api.last_error()}")


def latest_us100_close(terminal_path: Path) -> datetime:
    init_mt5(terminal_path)
    try:
        mt5_api.symbol_select("US100", True)
        rates = mt5_api.copy_rates_from_pos("US100", mt5_api.TIMEFRAME_M5, 0, 10)
        if rates is None or len(rates) == 0:
            return floor_m5(datetime.now(tz=UTC))
        last_open = datetime.fromtimestamp(int(rates[-1]["time"]), tz=UTC)
        return last_open + timedelta(seconds=M5_SECONDS)
    finally:
        mt5_api.shutdown()


def export_rates_csv(path: Path, contract_symbol: str, broker_symbol: str, rates: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        columns = [
            "time_open_unix",
            "time_close_unix",
            "contract_symbol",
            "broker_symbol",
            "timeframe",
            "open",
            "high",
            "low",
            "close",
            "tick_volume",
            "spread_points",
            "real_volume",
            "time_basis",
        ]
        writer = csv.DictWriter(handle, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        for row in rates:
            opened = int(row["time"])
            writer.writerow(
                {
                    "time_open_unix": opened,
                    "time_close_unix": opened + M5_SECONDS,
                    "contract_symbol": contract_symbol,
                    "broker_symbol": broker_symbol,
                    "timeframe": "M5",
                    "open": row["open"],
                    "high": row["high"],
                    "low": row["low"],
                    "close": row["close"],
                    "tick_volume": int(row["tick_volume"]),
                    "spread_points": int(row["spread"]),
                    "real_volume": int(row["real_volume"]),
                    "time_basis": "MT5_PY_API_UNIX_SECONDS",
                }
            )


def probe_all_raw_symbols(terminal_path: Path) -> tuple[list[dict[str, Any]], dict[str, Any], list[Path]]:
    end_utc = latest_us100_close(terminal_path)
    start_utc = datetime(2026, 4, 14, tzinfo=UTC)
    rows: list[dict[str, Any]] = []
    artifacts: list[Path] = []
    init_mt5(terminal_path)
    try:
        terminal_info = mt5_api.terminal_info()
        account_info = mt5_api.account_info()
        for binding in run336l.fp.SYMBOL_BINDINGS:
            contract_symbol = binding.contract_symbol
            broker_symbol = binding.broker_symbol
            selected = mt5_api.symbol_select(broker_symbol, True)
            if not selected:
                rows.append(
                    {
                        "contract_symbol": contract_symbol,
                        "broker_symbol": broker_symbol,
                        "status": "blocked_symbol_select_failed",
                        "rows": 0,
                        "first_open_utc": "",
                        "last_open_utc": "",
                        "last_close_utc": "",
                        "csv_path": "",
                        "manifest_path": "",
                        "last_error": str(mt5_api.last_error()),
                    }
                )
                continue
            rates = mt5_api.copy_rates_range(broker_symbol, mt5_api.TIMEFRAME_M5, start_utc, end_utc)
            if rates is None or len(rates) == 0:
                rows.append(
                    {
                        "contract_symbol": contract_symbol,
                        "broker_symbol": broker_symbol,
                        "status": "blocked_no_rates_returned",
                        "rows": 0,
                        "first_open_utc": "",
                        "last_open_utc": "",
                        "last_close_utc": "",
                        "csv_path": "",
                        "manifest_path": "",
                        "last_error": str(mt5_api.last_error()),
                    }
                )
                continue
            first_open = datetime.fromtimestamp(int(rates[0]["time"]), tz=UTC)
            last_open = datetime.fromtimestamp(int(rates[-1]["time"]), tz=UTC)
            last_close = last_open + timedelta(seconds=M5_SECONDS)
            safe_broker = broker_symbol.lower().replace(".", "_")
            csv_path = RAW_REFRESH_DIR / contract_symbol / f"bars_{safe_broker}_m5_mt5api_raw.csv"
            manifest_path = csv_path.with_suffix(".manifest.json")
            export_rates_csv(csv_path, contract_symbol, broker_symbol, rates)
            manifest = {
                "manifest_version": "STAGE337P_RAW_REFRESH_PROBE_V1",
                "contract_symbol": contract_symbol,
                "broker_symbol": broker_symbol,
                "timeframe": "M5",
                "requested_from_utc": start_utc.isoformat().replace("+00:00", "Z"),
                "requested_to_utc": end_utc.isoformat().replace("+00:00", "Z"),
                "resolved_first_open_unix": int(rates[0]["time"]),
                "resolved_last_open_unix": int(rates[-1]["time"]),
                "resolved_last_close_unix": int(rates[-1]["time"]) + M5_SECONDS,
                "row_count": int(len(rates)),
                "terminal_path": getattr(terminal_info, "path", None),
                "terminal_data_path": getattr(terminal_info, "data_path", None),
                "account_login_present": getattr(account_info, "login", None),
                "csv_file": str(csv_path.resolve()),
                "claim_boundary": CLAIM_BOUNDARY,
                "generated_at_utc": now_utc(),
            }
            write_json(manifest_path, manifest)
            rows.append(
                {
                    "contract_symbol": contract_symbol,
                    "broker_symbol": broker_symbol,
                    "status": "completed",
                    "rows": int(len(rates)),
                    "first_open_utc": first_open.isoformat().replace("+00:00", "Z"),
                    "last_open_utc": last_open.isoformat().replace("+00:00", "Z"),
                    "last_close_utc": last_close.isoformat().replace("+00:00", "Z"),
                    "csv_path": rel(csv_path),
                    "manifest_path": rel(manifest_path),
                    "last_error": str(mt5_api.last_error()),
                }
            )
            artifacts.extend([csv_path, manifest_path])
    finally:
        mt5_api.shutdown()
    latest = {
        "requested_start_utc": start_utc.isoformat().replace("+00:00", "Z"),
        "requested_end_utc": end_utc.isoformat().replace("+00:00", "Z"),
        "us100_last_close_utc": end_utc.isoformat().replace("+00:00", "Z"),
        "tester_to_date": (end_utc.date() + timedelta(days=1)).strftime("%Y.%m.%d"),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return rows, latest, artifacts


def synchronize_history(terminal_path: Path, raw_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    init_mt5(terminal_path)
    try:
        for row in raw_rows:
            broker_symbol = str(row.get("broker_symbol", ""))
            if not broker_symbol:
                continue
            selected = mt5_api.symbol_select(broker_symbol, True)
            rates = mt5_api.copy_rates_from_pos(broker_symbol, mt5_api.TIMEFRAME_M5, 0, 2000) if selected else None
            rows.append(
                {
                    "broker_symbol": broker_symbol,
                    "selected": bool(selected),
                    "sync_rows": 0 if rates is None else int(len(rates)),
                    "last_error": str(mt5_api.last_error()),
                    "effect": "MT5 Python API(MT5 파이썬 API) history cache(히스토리 캐시)를 Strategy Tester(전략 테스터) 실행 전에 갱신한다.",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    finally:
        mt5_api.shutdown()
    return rows


def stop_target_terminal_if_running(terminal_path: Path) -> dict[str, Any]:
    probe = base.detect_running_terminal_processes(terminal_path)
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
    after = base.detect_running_terminal_processes(terminal_path)
    return {
        "before_status": probe.get("status"),
        "before_matching_processes": probe.get("matching_processes", []),
        "stopped": stopped,
        "after_status": after.get("status"),
        "after_matching_processes": after.get("matching_processes", []),
        "effect": "target portable terminal(대상 포터블 터미널)을 MT5 tester config(MT5 테스터 설정) 실행 전에 닫는다.",
    }


def build_repaired_foundation_frame(latest_close: pd.Timestamp) -> tuple[run336l.FreshRawContext, pd.DataFrame, dict[str, Any]]:
    context = run336l.FreshRawContext(latest_close)
    run336l.fp.WINDOW_START_UTC = run336l.PRELOAD_START_UTC
    run336l.fp.WINDOW_END_UTC = latest_close
    run336l.fp.load_raw_symbol = context.load_symbol
    run336l.fp.load_source_identity = context.source_identity
    frame, foundation_counts = run336l.fp.build_feature_frame(
        Path("."),
        weights_path=run336l.WEIGHTS_PATH,
        weights_version_label="run337P_same_weights_source_asof_repair_no_retune",
    )
    frame = frame.copy()
    frame["overnight_return"] = run336l.live_safe_overnight_return(frame)
    return context, frame, foundation_counts


def sorted_symbol_times(context: run336l.FreshRawContext, symbol: str) -> np.ndarray:
    binding = next(item for item in run336l.fp.SYMBOL_BINDINGS if item.contract_symbol == symbol)
    values = context.load_symbol(Path("."), binding)["timestamp"].dropna().sort_values().to_numpy(dtype="datetime64[ns]")
    return values


def asof_age_minutes(timestamps: pd.Series, source_times: np.ndarray) -> np.ndarray:
    targets = pd.to_datetime(timestamps, utc=True).to_numpy(dtype="datetime64[ns]")
    if len(source_times) == 0:
        return np.full(len(targets), np.inf, dtype="float64")
    positions = np.searchsorted(source_times, targets, side="right") - 1
    ages = np.full(len(targets), np.inf, dtype="float64")
    valid = positions >= 0
    deltas = targets[valid] - source_times[positions[valid]]
    ages[valid] = deltas.astype("timedelta64[s]").astype("float64") / 60.0
    return ages


def materialize_asof_feature_sources(
    context: run336l.FreshRawContext,
    frame: pd.DataFrame,
    latest_close: pd.Timestamp,
    feature_set_ids: Sequence[str],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Path], list[Path]]:
    summaries: list[dict[str, Any]] = []
    age_rows: list[dict[str, Any]] = []
    paths: dict[str, Path] = {}
    artifacts: list[Path] = []
    us100_times = set(context.load_symbol(Path("."), next(item for item in run336l.fp.SYMBOL_BINDINGS if item.contract_symbol == "US100"))["timestamp"])
    for feature_set_id in feature_set_ids:
        config = stage329b.FEATURE_SETS[feature_set_id]
        features = list(config["features"])
        required_symbols = list(config["required_symbols"])
        scoped = frame.loc[
            (frame["timestamp"] >= run336l.FORWARD_OUTPUT_START_UTC) & (frame["timestamp"] <= latest_close),
            ["timestamp", *features],
        ].copy()
        source_policy = FEATURE_SOURCE_BY_SET.get(feature_set_id, "exact")
        fill_columns = [feature for feature in features if feature in ASOF_FILL_FEATURES] if source_policy == "asof_source_repair_probe" else []
        repaired = scoped.copy()
        if fill_columns:
            repaired[fill_columns] = repaired[fill_columns].ffill()
        age_matrix: dict[str, np.ndarray] = {}
        for symbol in required_symbols:
            if symbol == "US100":
                continue
            ages = asof_age_minutes(repaired["timestamp"], sorted_symbol_times(context, symbol))
            age_matrix[symbol] = ages
            finite = ages[np.isfinite(ages)]
            age_rows.append(
                {
                    "feature_set_id": feature_set_id,
                    "required_symbol": symbol,
                    "source_policy": source_policy,
                    "max_asof_age_minutes": float(finite.max()) if len(finite) else "",
                    "latest_row_asof_age_minutes": float(ages[-1]) if len(ages) else "",
                    "rows_over_max_age": int((ages > MAX_ASOF_AGE_MINUTES).sum()),
                    "max_allowed_age_minutes": MAX_ASOF_AGE_MINUTES,
                    "policy_status": "accepted_for_probe" if source_policy == "asof_source_repair_probe" else "exact_or_reference",
                    "effect": "as-of age(시점 기준 나이)를 기록해 미래참조 없이 source gap(원천 공백)을 메우는지 확인한다.",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
        if age_matrix:
            max_age = np.nanmax(np.vstack([ages for ages in age_matrix.values()]), axis=0)
            age_ok = np.isfinite(max_age) & (max_age <= MAX_ASOF_AGE_MINUTES)
        else:
            max_age = np.zeros(len(repaired), dtype="float64")
            age_ok = np.ones(len(repaired), dtype=bool)
        finite_values = repaired[features].replace([np.inf, -np.inf], np.nan)
        finite_mask = np.isfinite(finite_values.to_numpy(dtype="float64")).all(axis=1)
        us100_alignment = repaired["timestamp"].isin(us100_times).to_numpy()
        valid_mask = finite_mask & us100_alignment & age_ok
        valid_frame = repaired.loc[valid_mask, ["timestamp", *features]].copy()
        valid_frame["symbol"] = "US100"
        valid_frame["split"] = f"run337P_{source_policy}"
        valid_frame = valid_frame[["timestamp", "symbol", "split", *features]]
        valid_frame[features] = valid_frame[features].astype("float32")
        feature_path = REPAIRED_SOURCE_DIR / f"{feature_set_id}_{source_policy}_features.csv"
        export_payload = export_mt5_feature_matrix_csv(valid_frame, features, feature_path)
        paths[feature_set_id] = feature_path
        artifacts.append(feature_path)
        summaries.append(
            {
                "feature_set_id": feature_set_id,
                "source_policy": source_policy,
                "feature_count": len(features),
                "feature_order_sha256": run336l.ordered_hash(features),
                "required_symbols": ";".join(required_symbols),
                "scope_rows": int(len(scoped)),
                "valid_rows": int(len(valid_frame)),
                "invalid_rows": int(len(scoped) - len(valid_frame)),
                "finite_missing_rows": int((~finite_mask).sum()),
                "age_blocked_rows": int((~age_ok).sum()),
                "first_valid_timestamp": valid_frame["timestamp"].min().isoformat() if len(valid_frame) else "",
                "last_valid_timestamp": valid_frame["timestamp"].max().isoformat() if len(valid_frame) else "",
                "latest_us100_close": latest_close.isoformat(),
                "max_asof_age_minutes": float(np.nanmax(max_age)) if len(max_age) else 0.0,
                "feature_csv_path": rel(feature_path),
                "feature_csv_sha256": export_payload["sha256"],
                "mt5_export_rows": export_payload["rows"],
                "repair_contract": "source_asof_last_known_no_future_fill_same_feature_order_same_model_no_retune",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return summaries, age_rows, paths, artifacts


def selected_attempts(attempt_filter: str, feature_source_paths: Mapping[str, Path]) -> list[dict[str, Any]]:
    allowed = set(ATTEMPT_NAMES)
    if attempt_filter.strip():
        requested = {item.strip() for item in attempt_filter.split(",") if item.strip()}
        unknown = requested - allowed
        if unknown:
            raise ValueError(f"Unsupported attempt_filter values: {sorted(unknown)}")
        allowed = requested
    source = read_json(RUN336K_ATTEMPTS)
    attempts: list[dict[str, Any]] = []
    for row in source:
        if row.get("attempt_name") not in allowed:
            continue
        copied = dict(row)
        copied["model_copy"] = {"source": row.get("model_local_path", "")}
        feature_set_id = str(row["feature_set_id"])
        copied["feature_export"] = {"path": rel(feature_source_paths[feature_set_id])}
        copied["source_run_id"] = "run336K_attempt_fresh_mt5_runtime_probe_or_block_v1"
        copied["repair_source_run_id"] = PARENT_RUN_ID
        copied["attempt_role"] = "stage337P_runtime_data_feature_source_repair_probe_same_model_threshold_risk"
        attempts.append(copied)
    return attempts


def rewrite_attempt_to_latest(attempt: dict[str, Any], tester_to_date: str) -> dict[str, Any]:
    tester = dict(attempt["ini"]["tester"])
    tester["ToDate"] = tester_to_date
    tester["Report"] = f"Project_Obsidian_Prime_v2_{RUN_ID}_{attempt['attempt_name']}"
    ini_path = Path(str(attempt["ini"]["path"]))
    attempt["ini"] = base.materialize_ini_file(tester, ini_path)
    attempt["to_date"] = tester_to_date
    attempt["attempt_role"] = "stage337P_runtime_data_feature_source_repair_probe_same_frozen_model_feature_threshold_risk"
    attempt["record_view_prefix"] = f"mt5_stage337P_{attempt['artifact_slug']}"
    attempt["source_run_id"] = "run336K_attempt_fresh_mt5_runtime_probe_or_block_v1"
    attempt["repair_source_run_id"] = PARENT_RUN_ID
    attempt["repair_contract"] = "source-asof no-future fill for macro/core56 or exact u42 tester-gap probe; same ONNX, feature order, threshold, risk, lot"
    attempt["signal_policy"] = "same frozen ONNX and runtime settings; repaired feature CSV changes source handoff policy only"
    return attempt


def telemetry_last_observed(attempt_name: str, common_files_root: Path, common_telemetry_path: str) -> tuple[str, int]:
    candidates = [TELEMETRY_DIR / f"{attempt_name}_telemetry.csv"]
    if common_telemetry_path:
        candidates.append(common_files_root / Path(common_telemetry_path))
    path = next((candidate for candidate in candidates if path_exists(candidate)), None)
    if path is None:
        return "", 0
    frame = pd.read_csv(io_path(path), usecols=lambda column: column in {"bar_time"})
    values = pd.to_datetime(frame["bar_time"].astype(str).str.replace(".", "-", regex=False), errors="coerce", utc=True).dropna()
    return (values.max().isoformat().replace("+00:00", "Z") if len(values) else "", int(len(values)))


def tester_gap_rows(runtime_rows: Sequence[Mapping[str, Any]], latest: Mapping[str, Any], freshness_rows: Sequence[Mapping[str, Any]], common_files_root: Path) -> list[dict[str, Any]]:
    latest_close = pd.to_datetime(latest.get("us100_last_close_utc"), utc=True)
    freshness = {row["attempt_name"]: row for row in freshness_rows}
    rows: list[dict[str, Any]] = []
    for row in runtime_rows:
        if row.get("runtime_status") == "completed":
            last_obs, telemetry_rows = telemetry_last_observed(
                str(row.get("attempt_name")),
                common_files_root,
                str(row.get("common_telemetry_path", "")),
            )
        else:
            last_obs, telemetry_rows = "", 0
        last_obs_ts = pd.to_datetime(last_obs, errors="coerce", utc=True)
        if pd.isna(last_obs_ts):
            gap_status = "tester_observed_window_missing"
        elif last_obs_ts < latest_close:
            gap_status = "tester_current_day_gap_remains"
        else:
            gap_status = "tester_reached_latest"
        rows.append(
            {
                "attempt_name": row.get("attempt_name", ""),
                "feature_set_id": row.get("feature_set_id", ""),
                "runtime_status": row.get("runtime_status", ""),
                "report_status": row.get("report_status", ""),
                "latest_us100_last_close_utc": latest_close,
                "feature_last_timestamp": freshness.get(str(row.get("attempt_name")), {}).get("feature_last_timestamp", ""),
                "tester_last_observed_bar_time": last_obs,
                "tester_to_latest_gap_minutes": "" if pd.isna(last_obs_ts) else (latest_close - last_obs_ts).total_seconds() / 60.0,
                "telemetry_rows": telemetry_rows,
                "last_skip_reason": row.get("last_skip_reason", ""),
                "gap_status": gap_status,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


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


def feature_timestamp_series(frame: pd.DataFrame) -> pd.Series:
    for column in ("timestamp_utc", "bar_time_server", "timestamp"):
        if column in frame.columns:
            return pd.to_datetime(frame[column].astype(str).str.replace(".", "-", regex=False), errors="coerce", utc=True)
    return pd.Series(pd.NaT, index=frame.index, dtype="datetime64[ns, UTC]")


def empty_proxy_row(attempt: Mapping[str, Any], *, cutoff: str, reason: str) -> dict[str, Any]:
    return {
        "attempt_name": attempt["attempt_name"],
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
        "proxy_source": reason,
        "proxy_cutoff_utc": cutoff,
        "proxy_row_scope": reason,
        "full_feature_rows": None,
        "timestamp_aligned_feature_rows": None,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_timestamp_aligned_proxy_rows(
    attempts: Sequence[Mapping[str, Any]],
    cutoff_by_attempt: Mapping[str, str],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for attempt in attempts:
        attempt_name = str(attempt["attempt_name"])
        cutoff_raw = str(cutoff_by_attempt.get(attempt_name, "")).strip()
        cutoff_ts = pd.to_datetime(cutoff_raw, errors="coerce", utc=True)
        if pd.isna(cutoff_ts):
            rows.append(empty_proxy_row(attempt, cutoff=cutoff_raw, reason="timestamp_aligned_unavailable_no_tester_observed_time"))
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
            threshold_id=f"stage337P_{attempt_name}_timestamp_aligned_fixed_min_margin",
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


def sanitize_stage337_proxy_rows(rows: Sequence[Mapping[str, Any]], *, default_source: str) -> list[dict[str, Any]]:
    cleaned: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        existing_source = str(item.get("proxy_source") or "")
        item["proxy_source"] = existing_source if "timestamp_aligned" in existing_source else default_source
        item["claim_boundary"] = CLAIM_BOUNDARY
        cleaned.append(item)
    return cleaned


def sanitize_stage337_signal_diff_rows(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    cleaned: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        item["mt5_source"] = "stage337P_mt5_runtime_tier_a_telemetry_summary"
        item["usable_for_forward_pass_fail"] = False
        item["claim_boundary"] = CLAIM_BOUNDARY
        cleaned.append(item)
    return cleaned


def classify(runtime_rows: Sequence[Mapping[str, Any]], tester_rows: Sequence[Mapping[str, Any]], materialize_only: bool) -> tuple[str, str, str]:
    if materialize_only:
        return STATUS_MATERIALIZED_ONLY, JUDGMENT_PARTIAL, DECISION_PARTIAL
    completed = sum(
        1
        for row in runtime_rows
        if row.get("tester_status") == "completed" and row.get("runtime_status") == "completed" and row.get("report_status") == "completed"
    )
    if completed == len(runtime_rows):
        return STATUS_COMPLETED, JUDGMENT_COMPLETED, DECISION_COMPLETED
    return STATUS_PARTIAL, JUDGMENT_PARTIAL, DECISION_PARTIAL


def gate_rows(
    runtime_rows: Sequence[Mapping[str, Any]],
    freshness_rows: Sequence[Mapping[str, Any]],
    signal_diff_rows: Sequence[Mapping[str, Any]],
    tester_rows: Sequence[Mapping[str, Any]],
    age_rows: Sequence[Mapping[str, Any]],
    raw_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    completed = sum(
        1
        for row in runtime_rows
        if row.get("tester_status") == "completed" and row.get("runtime_status") == "completed" and row.get("report_status") == "completed"
    )
    feature_gaps = sum(1 for row in freshness_rows if row.get("fresh_latest_handoff_status") != "covers_latest_broker_close")
    matches = sum(1 for row in signal_diff_rows if str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true")
    tester_gaps = sum(1 for row in tester_rows if row.get("gap_status") == "tester_current_day_gap_remains")
    raw_completed = sum(1 for row in raw_rows if row.get("status") == "completed")
    return [
        {
            "gate_name": "all_required_raw_symbols_probed",
            "status": "covered" if raw_completed == len(raw_rows) else "covered_partial",
            "evidence_path": rel(RUN_DIR / "fresh_forward_data_probe_summary.csv"),
            "effect": f"macro/equity/core56 source(원천) 심볼을 실제 브로커에서 다시 확인한다; completed={raw_completed}/{len(raw_rows)}.",
        },
        {
            "gate_name": "asof_source_policy_audited",
            "status": "covered",
            "evidence_path": rel(RUN_DIR / "source_asof_policy_audit.csv"),
            "effect": f"as-of fill(시점 기준 채움)이 미래참조 없이 허용 나이 안인지 확인한다; rows={len(age_rows)}.",
        },
        {
            "gate_name": "feature_handoff_repair_materialized",
            "status": "covered" if feature_gaps == 0 else "covered_with_gap",
            "evidence_path": rel(RUN_DIR / "feature_freshness_gap_audit.csv"),
            "effect": f"repair-probe feature handoff(수리 탐침 피처 인계)가 최신 close(종가)를 덮는지 확인한다; gaps={feature_gaps}.",
        },
        {
            "gate_name": "mt5_runtime_repair_probe",
            "status": "covered" if completed == len(runtime_rows) else "covered_partial",
            "evidence_path": rel(RUN_DIR / "fresh_mt5_runtime_probe_result.csv"),
            "effect": f"core56/m48/u42 repair-probe(수리 탐침)를 MT5(메타트레이더5)에서 실행한다; completed={completed}/{len(runtime_rows)}.",
        },
        {
            "gate_name": "proxy_mt5_difference_recorded",
            "status": "covered",
            "evidence_path": rel(RUN_DIR / "timestamp_aligned_proxy_mt5_difference.csv"),
            "effect": f"tester observed window(테스터 관측 구간)에 맞춘 proxy expected(프록시 예상값)와 MT5 observed(관측값)를 비교한다; matched={matches}/{len(signal_diff_rows)}.",
        },
        {
            "gate_name": "tester_current_day_gap_retested",
            "status": "covered_blocker" if tester_gaps else "covered_repaired",
            "evidence_path": rel(RUN_DIR / "tester_current_day_gap_reprobe.csv"),
            "effect": f"history sync(히스토리 동기화) 후 Strategy Tester(전략 테스터)가 최신 봉까지 도달하는지 확인한다; gap attempts={tester_gaps}.",
        },
        {
            "gate_name": "no_forward_or_goal_claim",
            "status": "covered",
            "evidence_path": rel(RUN_DIR / "final_runtime_data_feature_source_repair_probe_decision.json"),
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


def write_report(
    status: str,
    judgment: str,
    decision: str,
    latest: Mapping[str, Any],
    runtime_rows: Sequence[Mapping[str, Any]],
    tester_rows: Sequence[Mapping[str, Any]],
    feature_summaries: Sequence[Mapping[str, Any]],
    signal_diff_rows: Sequence[Mapping[str, Any]],
    timestamp_aligned_signal_diff_rows: Sequence[Mapping[str, Any]],
) -> Path:
    completed = sum(
        1
        for row in runtime_rows
        if row.get("tester_status") == "completed" and row.get("runtime_status") == "completed" and row.get("report_status") == "completed"
    )
    tester_gaps = sum(1 for row in tester_rows if row.get("gap_status") == "tester_current_day_gap_remains")
    raw_matches = sum(1 for row in signal_diff_rows if str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true")
    aligned_matches = sum(1 for row in timestamp_aligned_signal_diff_rows if str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true")
    lines = [
        "# Stage337P Runtime Data And Feature Source Repair Probe(337P 런타임 데이터 및 피처 원천 수리 탐침)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- status(상태): `{status}`",
        f"- judgment(판정): `{judgment}`",
        f"- decision(결정): `{decision}`",
        f"- latest US100 close(최신 US100 종가): `{latest.get('us100_last_close_utc', '')}`",
        f"- MT5 completed(MT5 완료): `{completed}/{len(runtime_rows)}`",
        f"- tester current-day gap attempts(테스터 현재일 공백 시도): `{tester_gaps}`",
        f"- raw proxy parity(전체 프록시 동등성): `{raw_matches}/{len(signal_diff_rows)}`",
        f"- timestamp-aligned proxy parity(시점 맞춤 프록시 동등성): `{aligned_matches}/{len(timestamp_aligned_signal_diff_rows)}`",
        "- Forward Passed(전진 통과): `not_claimed`",
        "- Forward Failed(전진 실패): `not_claimed`",
        "- runtime authority(런타임 권위): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Feature Sources(피처 원천)",
        "",
        "| feature_set(피처 세트) | policy(정책) | rows(행) | last(마지막) | max_age(최대 나이) |",
        "|---|---:|---:|---:|---:|",
    ]
    for row in feature_summaries:
        lines.append(
            f"| `{row.get('feature_set_id', '')}` | `{row.get('source_policy', '')}` | `{row.get('valid_rows', '')}` | `{row.get('last_valid_timestamp', '')}` | `{row.get('max_asof_age_minutes', '')}` |"
        )
    lines.extend(
        [
            "",
            "## Runtime Metrics(런타임 지표)",
            "",
            "| attempt(시도) | status(상태) | net(순익) | PF(손익비) | trades(거래수) | DD(드로다운) |",
            "|---|---:|---:|---:|---:|---:|",
        ]
    )
    for row in runtime_rows:
        status_label = f"{row.get('tester_status', '')}/{row.get('runtime_status', '')}/{row.get('report_status', '')}"
        lines.append(
            f"| `{row.get('attempt_name', '')}` | `{status_label}` | `{row.get('net_profit', '')}` | `{row.get('profit_factor', '')}` | `{row.get('trade_count', '')}` | `{row.get('max_drawdown_amount', '')}` |"
        )
    lines.extend(
        [
            "",
            "## Boundary(경계)",
            "",
            "as-of source repair(시점 기준 원천 수리)는 feature handoff(피처 인계) 수리 탐침일 뿐이다. timestamp-aligned proxy parity(시점 맞춤 프록시 동등성)는 tester observed window(테스터 관측 구간)에 맞춘 실행 의미 확인이다. model training(모델 학습), threshold retuning(임계값 재조정), lot optimization(랏 최적화), Forward Passed/Failed(전진 통과/실패)는 수행하지 않는다.",
        ]
    )
    return write_md(REPORT_PATH, "\n".join(lines))


def write_decision_doc(status: str, judgment: str, decision: str, latest: Mapping[str, Any]) -> Path:
    text = f"""# Stage337P Decision(337P 결정)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{status}`
- judgment(판정): `{judgment}`
- decision(결정): `{decision}`
- latest US100 close(최신 US100 종가): `{latest.get('us100_last_close_utc', '')}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Effect(효과): run337P(337P 실행)는 core56/m48 원천을 브로커 심볼과 as-of policy(시점 기준 정책)로 수리 탐침하고 MT5(메타트레이더5) 실행까지 확인했다. 현재일 tester gap(테스터 공백)은 별도 리뷰 대상으로 남긴다.
"""
    return write_md(DECISION_DOC, text)


def update_status_docs(status: str, decision: str, runtime_rows: Sequence[Mapping[str, Any]], tester_rows: Sequence[Mapping[str, Any]]) -> list[Path]:
    completed = sum(
        1
        for row in runtime_rows
        if row.get("tester_status") == "completed" and row.get("runtime_status") == "completed" and row.get("report_status") == "completed"
    )
    tester_gaps = sum(1 for row in tester_rows if row.get("gap_status") == "tester_current_day_gap_remains")
    selection_text = f"""# Stage337 Selection Status(337단계 선택 상태)

- stage_id(단계 ID): `{STAGE_ID}`
- stage_status(단계 상태): `open_active`
- selected_candidate(선택 후보): `none`
- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{decision}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- repair_probe_runtime(수리 탐침 런타임): `{completed}/{len(runtime_rows)} completed(완료)`
- current blockers(현재 차단 요소): `tester_current_day_gap_review_required;asof_source_policy_review_required`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed_for_stage337_new_work`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): run337P(337P 실행)는 core56/m48/u42 repair probe(수리 탐침)를 MT5(메타트레이더5)까지 실행했고 tester current-day gap(테스터 현재일 공백) `{tester_gaps}`개를 리뷰 대상으로 남겼다. 아직 선택 후보는 없다.
"""
    write_md(SELECTED_STATUS, selection_text)

    if path_exists(WORKSPACE_STATE):
        text, had_bom = read_text_lossless(WORKSPACE_STATE)
        lines = text.splitlines()
        for idx, line in enumerate(lines):
            if line.startswith("current_run_id:"):
                lines[idx] = f"current_run_id: {NEXT_RUN_ID}"
                break
        focus_line = (
            "- >-\n"
            f"  Stage337 run337P focus complete: Stage337(337단계) run337P(337P 실행)는 `{status}`로 runtime data and feature source repair probe(런타임 데이터 및 피처 원천 수리 탐침)를 완료했다. "
            f"Effect(효과): core56/m48/u42 수리 탐침을 MT5(메타트레이더5) `{completed}/{len(runtime_rows)}`로 실행하고, tester current-day gap(테스터 현재일 공백) `{tester_gaps}`개와 as-of source policy(시점 기준 원천 정책)를 run337Q(337Q 실행) 리뷰로 넘긴다. Forward/Goal(전진/목표)은 주장하지 않는다.\n"
        )
        if "Stage337 run337P focus complete" in text:
            text = re.sub(r"- >-\n  Stage337 run337P focus complete:.*?(?=\n- >-|\Z)", focus_line.rstrip(), text, count=1, flags=re.S)
            lines = text.splitlines()
        else:
            try:
                idx = lines.index("current_focus:")
                lines.insert(idx + 1, focus_line.rstrip())
            except ValueError:
                lines.extend(["current_focus:", focus_line.rstrip()])
        write_text_preserving(WORKSPACE_STATE, "\n".join(lines) + "\n", had_bom)
    current_entry = f"""
## Stage337 run337P(337P 실행) - {TODAY}

- status(상태): `{status}`
- decision(결정): `{decision}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): core56/m48/u42 repair probe(수리 탐침)를 MT5(메타트레이더5) `{completed}/{len(runtime_rows)}`로 실행했고, tester current-day gap(테스터 현재일 공백) `{tester_gaps}`개가 남았다. 결과는 선택이나 Forward decision(전진 판정)이 아니라 run337Q(337Q 실행) 리뷰 입력이다.
"""
    if path_exists(CURRENT_STATE):
        text, had_bom = read_text_lossless(CURRENT_STATE)
        if "## Stage337 run337P(337P 실행)" in text:
            text = re.sub(r"## Stage337 run337P\(337P 실행\).*?(?=\n## |\Z)", current_entry.strip(), text, count=1, flags=re.S)
            write_text_preserving(CURRENT_STATE, text.rstrip() + "\n", had_bom)
        else:
            write_text_preserving(CURRENT_STATE, text.rstrip() + "\n\n" + current_entry.strip() + "\n", had_bom)
    if path_exists(CHANGELOG):
        text, had_bom = read_text_lossless(CHANGELOG)
        line = f"\n- {TODAY}: Stage337 run337P(337P 실행) `{status}`. Effect(효과): runtime data and feature source repair probe(런타임 데이터 및 피처 원천 수리 탐침)를 MT5(메타트레이더5) `{completed}/{len(runtime_rows)}`로 실행했고 tester current-day gap(테스터 현재일 공백) `{tester_gaps}`개가 남았다. Forward/Goal(전진/목표) 주장은 없음.\n"
        if "Stage337 run337P(337P 실행)" in text:
            text = re.sub(r"\n- [^\n]*Stage337 run337P\(337P 실행\)[^\n]*", line.rstrip(), text, count=1)
            write_text_preserving(CHANGELOG, text.rstrip() + "\n", had_bom)
        else:
            write_text_preserving(CHANGELOG, text.rstrip() + line, had_bom)
    return [SELECTED_STATUS, WORKSPACE_STATE, CURRENT_STATE, CHANGELOG]


def build_receipts(
    status: str,
    judgment: str,
    decision: str,
    latest: Mapping[str, Any],
    runtime_rows: Sequence[Mapping[str, Any]],
    tester_rows: Sequence[Mapping[str, Any]],
    feature_summaries: Sequence[Mapping[str, Any]],
    timestamp_aligned_signal_diff_rows: Sequence[Mapping[str, Any]],
) -> list[Path]:
    completed = sum(
        1
        for row in runtime_rows
        if row.get("tester_status") == "completed" and row.get("runtime_status") == "completed" and row.get("report_status") == "completed"
    )
    aligned_matches = sum(1 for row in timestamp_aligned_signal_diff_rows if str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true")
    return [
        write_json(
            RUN_DIR / "data_integrity_receipt.json",
            {
                "run_id": RUN_ID,
                "latest_us100_last_close_utc": latest.get("us100_last_close_utc"),
                "feature_sources": [row.get("feature_csv_path", "") for row in feature_summaries],
                "asof_policy": f"last-known-no-future-fill max age {MAX_ASOF_AGE_MINUTES} minutes",
                "integrity_judgment": "repair_probe_usable_for_review_not_forward_decision",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RUN_DIR / "runtime_parity_receipt.json",
            {
                "run_id": RUN_ID,
                "runtime_completed": f"{completed}/{len(runtime_rows)}",
                "timestamp_aligned_signal_parity": f"{aligned_matches}/{len(timestamp_aligned_signal_diff_rows)}",
                "tester_gap_rows": [row for row in tester_rows if row.get("gap_status") == "tester_current_day_gap_remains"],
                "parity_judgment": "repair_probe_runtime_available_current_day_gap_review_required",
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
            RUN_DIR / "artifact_lineage_receipt.json",
            {
                "run_id": RUN_ID,
                "parent_run_id": PARENT_RUN_ID,
                "source_attempts": rel(RUN336K_ATTEMPTS),
                "parent_queue": rel(RUN337O_DIR / "run337P_runtime_data_and_feature_source_repair_queue.csv"),
                "lineage_judgment": "connected_with_repair_probe_boundary",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
    ]


def update_registers(status: str, judgment: str, decision: str, artifact_paths: Sequence[Path]) -> list[Path]:
    artifacts = [
        upsert_csv(
            RUN_REGISTRY,
            ["run_id"],
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "family": "runtime_data_feature_source_repair_probe",
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
                "run_key": f"{RUN_ID}__runtime_data_feature_source_repair_probe",
                "ledger_row_id": f"{RUN_ID}__runtime_data_feature_source_repair_probe",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "family": "runtime_data_feature_source_repair_probe",
                "work_family": "runtime_parity_repair",
                "question": "can tester/macro/core56 gaps be reduced with no-lookahead source repair probes",
                "metric_scope": "repair_probe_runtime_no_forward_decision",
                "evidence_scope": "asof_feature_source_repair_and_mt5_probe",
                "kpi_scope": "diagnostic_repair_probe_not_forward_kpi",
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
    rows: list[dict[str, Any]] = []
    generated = now_utc()
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
    configure_modules()
    generated_at_utc = now_utc()
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    MT5_DIR.mkdir(parents=True, exist_ok=True)
    REPAIRED_SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    raw_rows, latest, raw_artifacts = probe_all_raw_symbols(Path(args.terminal_path))
    latest_close = pd.to_datetime(latest["us100_last_close_utc"], utc=True)
    history_sync_rows = synchronize_history(Path(args.terminal_path), raw_rows)
    terminal_recovery = {"status": "skipped_materialize_only"} if args.materialize_only else stop_target_terminal_if_running(Path(args.terminal_path))

    context, frame, foundation_counts = build_repaired_foundation_frame(latest_close)
    feature_summaries, age_rows, feature_paths, feature_artifacts = materialize_asof_feature_sources(
        context,
        frame,
        latest_close,
        ["core56_no_top3_weight_features", "macro48_no_equity_breadth_or_top3", "us100_technical42_no_external"],
    )
    prepared_sources = selected_attempts(args.attempt_filter, feature_paths)
    attempts, handoff_rows, materialized_artifacts = base.build_attempts(prepared_sources, Path(args.common_files_root))
    attempts = [rewrite_attempt_to_latest(dict(attempt), str(latest["tester_to_date"])) for attempt in attempts]
    proxy_rows = sanitize_stage337_proxy_rows(
        base.build_proxy_signal_expected_rows(attempts),
        default_source="stage337P_python_onnx_inference_from_repair_probe_features",
    )
    freshness_rows = repair.build_feature_freshness_rows(attempts, latest)

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
    signal_diff_rows = sanitize_stage337_signal_diff_rows(base.build_signal_difference_rows(proxy_rows, runtime_rows))
    tester_rows = tester_gap_rows(runtime_rows, latest, freshness_rows, Path(args.common_files_root))
    cutoff_by_attempt = {str(row.get("attempt_name", "")): str(row.get("tester_last_observed_bar_time", "")) for row in tester_rows}
    timestamp_aligned_proxy_rows = sanitize_stage337_proxy_rows(
        build_timestamp_aligned_proxy_rows(attempts, cutoff_by_attempt),
        default_source="stage337P_timestamp_aligned_python_onnx_inference_cut_to_mt5_tester_last_observed_bar",
    )
    timestamp_aligned_signal_diff_rows = sanitize_stage337_signal_diff_rows(base.build_signal_difference_rows(timestamp_aligned_proxy_rows, runtime_rows))
    status, judgment, decision = classify(runtime_rows, tester_rows, bool(args.materialize_only))
    metrics = metric_summary(runtime_rows)
    gates = gate_rows(runtime_rows, freshness_rows, timestamp_aligned_signal_diff_rows, tester_rows, age_rows, raw_rows)

    artifact_paths: list[Path] = [
        write_csv(
            RUN_DIR / "fresh_forward_data_probe_summary.csv",
            ["contract_symbol", "broker_symbol", "status", "rows", "first_open_utc", "last_open_utc", "last_close_utc", "csv_path", "manifest_path", "last_error"],
            raw_rows,
        ),
        write_json(RUN_DIR / "fresh_forward_data_probe_latest.json", latest),
        write_csv(
            RUN_DIR / "terminal_history_sync_probe.csv",
            ["broker_symbol", "selected", "sync_rows", "last_error", "effect", "claim_boundary"],
            history_sync_rows,
        ),
        write_json(RUN_DIR / "terminal_process_recovery.json", terminal_recovery),
        write_json(RUN_DIR / "foundation_feature_counts.json", foundation_counts),
        write_csv(
            RUN_DIR / "asof_feature_set_summary.csv",
            [
                "feature_set_id",
                "source_policy",
                "feature_count",
                "feature_order_sha256",
                "required_symbols",
                "scope_rows",
                "valid_rows",
                "invalid_rows",
                "finite_missing_rows",
                "age_blocked_rows",
                "first_valid_timestamp",
                "last_valid_timestamp",
                "latest_us100_close",
                "max_asof_age_minutes",
                "feature_csv_path",
                "feature_csv_sha256",
                "mt5_export_rows",
                "repair_contract",
                "claim_boundary",
            ],
            feature_summaries,
        ),
        write_csv(
            RUN_DIR / "source_asof_policy_audit.csv",
            [
                "feature_set_id",
                "required_symbol",
                "source_policy",
                "max_asof_age_minutes",
                "latest_row_asof_age_minutes",
                "rows_over_max_age",
                "max_allowed_age_minutes",
                "policy_status",
                "effect",
                "claim_boundary",
            ],
            age_rows,
        ),
        write_json(RUN_DIR / "repair_handoff_attempts.json", attempts),
        write_csv(
            RUN_DIR / "independent_handoff_attempt_manifest.csv",
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
                "source_set_sha256",
                "new_set_sha256",
                "model_sha256",
                "feature_sha256",
                "materialization_status",
                "claim_boundary",
            ],
            handoff_rows,
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
            timestamp_aligned_proxy_rows,
        ),
        write_csv(
            RUN_DIR / "feature_freshness_gap_audit.csv",
            ["attempt_name", "artifact_slug", "feature_set_id", "feature_rows", "feature_first_timestamp", "feature_last_timestamp", "latest_us100_last_close_utc", "feature_to_latest_gap_minutes", "fresh_latest_handoff_status", "effect", "claim_boundary"],
            freshness_rows,
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
            RUN_DIR / "proxy_mt5_difference.csv",
            ["attempt_name", "artifact_slug", "dimension", "proxy_expected_value", "mt5_runtime_value", "difference_proxy_minus_mt5", "difference_status", "proxy_source", "mt5_source", "usable_for_runtime_signal_parity", "usable_for_forward_pass_fail", "runtime_skip_reason", "claim_boundary"],
            signal_diff_rows,
        ),
        write_csv(
            RUN_DIR / "timestamp_aligned_proxy_mt5_difference.csv",
            ["attempt_name", "artifact_slug", "dimension", "proxy_expected_value", "mt5_runtime_value", "difference_proxy_minus_mt5", "difference_status", "proxy_source", "mt5_source", "usable_for_runtime_signal_parity", "usable_for_forward_pass_fail", "runtime_skip_reason", "claim_boundary"],
            timestamp_aligned_signal_diff_rows,
        ),
        write_csv(
            RUN_DIR / "tester_current_day_gap_reprobe.csv",
            ["attempt_name", "feature_set_id", "runtime_status", "report_status", "latest_us100_last_close_utc", "feature_last_timestamp", "tester_last_observed_bar_time", "tester_to_latest_gap_minutes", "telemetry_rows", "last_skip_reason", "gap_status", "claim_boundary"],
            tester_rows,
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
                "tester_to_date": latest.get("tester_to_date"),
                "terminal_path": str(args.terminal_path),
                "terminal_data_root": str(args.terminal_data_root),
                "common_files_root": str(args.common_files_root),
                "queued_attempts": [attempt["attempt_name"] for attempt in attempts],
                "model_training": "forbidden_not_performed",
                "threshold_retuning": "forbidden_not_performed",
                "lot_optimization": "forbidden_not_performed",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
    ]
    artifact_paths.extend(raw_artifacts)
    artifact_paths.extend(feature_artifacts)
    artifact_paths.extend(materialized_artifacts)
    artifact_paths.extend(base.copy_runtime_outputs(Path(args.common_files_root), attempts))
    artifact_paths.extend(copy_reports_to_required_names(runtime_rows))
    artifact_paths.extend(build_receipts(status, judgment, decision, latest, runtime_rows, tester_rows, feature_summaries, timestamp_aligned_signal_diff_rows))
    artifact_paths.append(write_report(status, judgment, decision, latest, runtime_rows, tester_rows, feature_summaries, signal_diff_rows, timestamp_aligned_signal_diff_rows))
    artifact_paths.append(write_decision_doc(status, judgment, decision, latest))
    artifact_paths.extend(update_status_docs(status, decision, runtime_rows, tester_rows))

    completed = sum(
        1
        for row in runtime_rows
        if row.get("tester_status") == "completed" and row.get("runtime_status") == "completed" and row.get("report_status") == "completed"
    )
    final_decision = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": status,
        "judgment": judgment,
        "decision": decision,
        "latest_us100_last_close_utc": latest.get("us100_last_close_utc"),
        "runtime_completed": completed,
        "runtime_total": len(runtime_rows),
        "feature_latest_gap_attempts": sum(1 for row in freshness_rows if row.get("fresh_latest_handoff_status") != "covers_latest_broker_close"),
        "tester_current_day_gap_attempts": sum(1 for row in tester_rows if row.get("gap_status") == "tester_current_day_gap_remains"),
        "signal_parity_matched_rows": sum(1 for row in signal_diff_rows if str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true"),
        "signal_parity_total_rows": len(signal_diff_rows),
        "timestamp_aligned_signal_parity_matched_rows": sum(1 for row in timestamp_aligned_signal_diff_rows if str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true"),
        "timestamp_aligned_signal_parity_total_rows": len(timestamp_aligned_signal_diff_rows),
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    artifact_paths.append(write_json(RUN_DIR / "final_runtime_data_feature_source_repair_probe_decision.json", final_decision))
    artifact_paths.extend(update_registers(status, judgment, decision, [*artifact_paths, Path(__file__)]))
    artifact_paths.append(
        write_json(
            RUN_DIR / "run_manifest.json",
            {
                **final_decision,
                "generated_at_utc": generated_at_utc,
                "command": "python stage_pipelines/stage337/materialize_runtime_data_and_feature_source_repair_probe.py",
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
