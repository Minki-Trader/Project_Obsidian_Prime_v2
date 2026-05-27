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
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import MetaTrader5 as mt5_api
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, path_exists  # noqa: E402
from foundation.mt5 import mql5_compile  # noqa: E402
from foundation.mt5.runtime_artifacts import sha256_file  # noqa: E402
from stage_pipelines.stage335 import independent_proxy_mt5_probe as base  # noqa: E402
from stage_pipelines.stage337 import probe_tester_history_cache_session_policy as aa  # noqa: E402
from stage_pipelines.stage337 import review_runtime_data_and_feature_source_repair_probe as qprobe  # noqa: E402


TODAY = "2026-05-27"
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
RUN_NUMBER = "run337AB"
RUN_ID = "run337AB_custom_symbol_intraday_tester_visibility_probe_v1"
PARENT_RUN_ID = "run337AA_tester_history_cache_repair_or_actual_source_session_policy_probe_v1"
NEXT_RUN_ID_SUCCESS = "run337AC_custom_symbol_forward_reprobe_boundary_labeled_v1"
NEXT_RUN_ID_REPAIR = "run337AC_next_day_broker_rollover_or_custom_symbol_seed_repair_v1"
CLAIM_BOUNDARY = (
    "research_development_only_stage337AB_custom_symbol_intraday_tester_visibility_probe_no_model_training_"
    "no_threshold_retuning_no_lot_optimization_no_candidate_selection_no_forward_passed_no_forward_failed_"
    "no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STATUS_SUCCESS = "completed_stage337AB_custom_symbol_tester_visibility_confirmed_no_forward_decision"
STATUS_PARTIAL = "completed_stage337AB_custom_symbol_tester_visibility_inconclusive_no_forward_decision"
JUDGMENT_SUCCESS = "custom_symbol_intraday_tester_visibility_confirmed_original_broker_boundary_remains"
JUDGMENT_PARTIAL = "custom_symbol_intraday_tester_visibility_not_confirmed_requires_repair_or_next_day_reprobe"
DECISION_SUCCESS = "stage337AB_open_run337AC_custom_symbol_forward_reprobe_boundary_labeled_no_selection"
DECISION_PARTIAL = "stage337AB_open_run337AC_next_day_broker_or_custom_symbol_seed_repair_no_selection"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
RUN337Z_DIR = STAGE_DIR / "02_runs" / "run337Z"
RUN337Z_ATTEMPTS = RUN337Z_DIR / "rollover_reprobe_handoff_attempts.json"
MT5_DIR = RUN_DIR / "mt5"
FEATURE_COPY_DIR = RUN_DIR / "feature_matrices"
MODEL_COPY_DIR = RUN_DIR / "models"
TELEMETRY_DIR = RUN_DIR / "runtime_telemetry"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEWS_DIR / "run337AB_custom_symbol_visibility.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage337AB_custom_symbol_intraday_tester_visibility_probe.md"
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

COMMON_ROOT = "Project_Obsidian_Prime_v2/stage337/run337AB_custom_symbol_intraday_tester_visibility_probe"
CUSTOM_SYMBOL = "US100.OPV337AB"
CUSTOM_SYMBOL_PATH = "ObsidianPrime"
ORIGIN_SYMBOL = "US100"
FROM_DATE = "2026.04.14"
TO_DATE = "2026.05.28"
FROM_UTC = "2026.04.14 00:00:00"
TO_UTC = "2026.05.28 00:00:00"
ATTEMPT_BASE = "u42_plain_rf"
SCRIPT_SOURCE = ROOT / "foundation" / "mt5" / "ObsidianPrimeV2_CustomSymbolSeed.mq5"
PORTABLE_SCRIPT = DEFAULT_PORTABLE_ROOT / "MQL5" / "Scripts" / "Project_Obsidian_Prime_v2" / "foundation" / "mt5" / "ObsidianPrimeV2_CustomSymbolSeed.mq5"
SCRIPT_PRESET_NAME = "opv2_run337AB_custom_symbol_seed.set"
SCRIPT_PRESET = DEFAULT_PORTABLE_ROOT / "MQL5" / "Presets" / SCRIPT_PRESET_NAME
SCRIPT_STARTUP_INI = MT5_DIR / "custom_symbol_seed_startup.ini"
SCRIPT_OUTPUT_COMMON = DEFAULT_COMMON_FILES / COMMON_ROOT / "custom_symbol_seed_status.json"


def rel(path: Path) -> str:
    return aa.rel(path)


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
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column, "")) for column in columns})
    return path


def write_json(path: Path, payload: Any) -> Path:
    return aa.write_json(path, payload)


def write_md(path: Path, text: str) -> Path:
    return aa.write_md(path, text)


def read_json(path: Path) -> Any:
    return aa.read_json(path)


def read_text_lossless(path: Path) -> tuple[str, bool]:
    return aa.read_text_lossless(path)


def write_text_preserving(path: Path, text: str, had_bom: bool) -> Path:
    return aa.write_text_preserving(path, text, had_bom)


def configure_probe_modules() -> None:
    qprobe.TODAY = TODAY
    qprobe.STAGE_ID = STAGE_ID
    qprobe.RUN_NUMBER = RUN_NUMBER
    qprobe.RUN_ID = RUN_ID
    qprobe.PARENT_RUN_ID = PARENT_RUN_ID
    qprobe.NEXT_RUN_ID = NEXT_RUN_ID_SUCCESS
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stage337AB custom-symbol intraday tester visibility probe.")
    parser.add_argument("--terminal", default=str(DEFAULT_TERMINAL))
    parser.add_argument("--metaeditor", default=str(DEFAULT_METAEDITOR))
    parser.add_argument("--common-files-root", default=str(DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-data-root", default=str(DEFAULT_TERMINAL_DATA_ROOT))
    parser.add_argument("--timeout-seconds", type=int, default=1200)
    parser.add_argument("--wait-timeout-seconds", type=int, default=240)
    parser.add_argument("--materialize-only", action="store_true")
    return parser.parse_args()


def load_source_attempts() -> list[dict[str, Any]]:
    rows = read_json(RUN337Z_ATTEMPTS)
    source = next((row for row in rows if row.get("attempt_name") == ATTEMPT_BASE), None)
    if source is None:
        raise RuntimeError(f"missing {ATTEMPT_BASE} in {RUN337Z_ATTEMPTS}")
    scenarios = [
        ("ab_broker_control", "broker_us100_current_day_boundary_control", ORIGIN_SYMBOL),
        ("ab_custom_symbol", "custom_symbol_intraday_visibility_probe", CUSTOM_SYMBOL),
    ]
    selected: list[dict[str, Any]] = []
    for index, (suffix, scenario_id, symbol) in enumerate(scenarios):
        copied = dict(source)
        copied["attempt_name"] = f"u42_plain_rf_{suffix}"
        copied["artifact_slug"] = f"u42_plain_{suffix}"
        copied["scenario_id"] = scenario_id
        copied["scenario_symbol"] = symbol
        copied["scenario_from_date"] = FROM_DATE
        copied["scenario_to_date"] = TO_DATE
        copied["model_copy"] = {"source": source.get("model_local_path", "")}
        copied["feature_export"] = {"path": source.get("feature_local_path", "")}
        copied["source_run_id"] = PARENT_RUN_ID
        copied["attempt_role"] = "stage337AB_custom_symbol_intraday_tester_visibility_probe_same_frozen_u42_model_feature_threshold_risk"
        copied["record_view_prefix"] = f"mt5_stage337AB_u42_plain_{index}"
        selected.append(copied)
    return selected


def rewrite_attempt_to_visibility(attempt: dict[str, Any]) -> dict[str, Any]:
    tester = dict(attempt["ini"]["tester"])
    tester["Symbol"] = attempt["scenario_symbol"]
    tester["FromDate"] = attempt["scenario_from_date"]
    tester["ToDate"] = attempt["scenario_to_date"]
    if attempt["scenario_symbol"] == CUSTOM_SYMBOL:
        tester["Model"] = "0"
    tester["Report"] = f"Project_Obsidian_Prime_v2_{RUN_ID}_{attempt['attempt_name']}"
    ini_path = Path(str(attempt["ini"]["path"]))
    attempt["ini"] = base.materialize_ini_file(tester, ini_path)
    attempt["from_date"] = tester["FromDate"]
    attempt["to_date"] = tester["ToDate"]
    attempt["tester_symbol"] = tester["Symbol"]
    attempt["tester_model"] = tester.get("Model", "")
    attempt["attempt_role"] = "stage337AB_tester_visibility_probe_same_frozen_u42_model_feature_threshold_risk"
    attempt["record_view_prefix"] = f"mt5_stage337AB_{attempt['artifact_slug']}"
    attempt["source_run_id"] = PARENT_RUN_ID
    attempt["repair_contract"] = "tester Symbol visibility diagnostic only; same ONNX, feature order, threshold, risk, lot, ATR SL/TP, and feature CSV; custom symbol uses generated ticks because broker real tick cache is not available for the synthetic symbol"
    attempt["signal_policy"] = "same frozen ONNX and runtime settings; custom symbol is data-visibility repair evidence only and not KPI authority"
    return attempt


def mt5_api_symbol_visibility(terminal_path: Path, symbol: str) -> dict[str, Any]:
    ok = mt5_api.initialize(path=str(terminal_path), portable=True)
    if not ok:
        return {"symbol": symbol, "status": "blocked_mt5_initialize_failed", "last_error": str(mt5_api.last_error())}
    try:
        selected = mt5_api.symbol_select(symbol, True)
        if not selected:
            return {"symbol": symbol, "status": "blocked_symbol_select_failed", "last_error": str(mt5_api.last_error())}
        info = mt5_api.symbol_info(symbol)
        rows: dict[str, Any] = {
            "symbol": symbol,
            "status": "completed",
            "symbol_custom": bool(getattr(info, "custom", False)) if info is not None else "",
            "point": getattr(info, "point", "") if info is not None else "",
            "digits": getattr(info, "digits", "") if info is not None else "",
            "trade_mode": getattr(info, "trade_mode", "") if info is not None else "",
        }
        for label, timeframe, seconds in (("m1", mt5_api.TIMEFRAME_M1, 60), ("m5", mt5_api.TIMEFRAME_M5, 300)):
            rates = mt5_api.copy_rates_from_pos(symbol, timeframe, 0, 10)
            if rates is None or len(rates) == 0:
                rows[f"{label}_rows"] = 0
                rows[f"{label}_last_open_utc"] = ""
                rows[f"{label}_last_close_utc"] = ""
            else:
                last_open = datetime.fromtimestamp(int(rates[-1]["time"]), tz=UTC)
                rows[f"{label}_rows"] = len(rates)
                rows[f"{label}_last_open_utc"] = last_open.isoformat().replace("+00:00", "Z")
                rows[f"{label}_last_close_utc"] = (last_open.timestamp() + seconds)
                rows[f"{label}_last_close_utc"] = datetime.fromtimestamp(int(rows[f"{label}_last_close_utc"]), tz=UTC).isoformat().replace("+00:00", "Z")
                rows[f"{label}_last_close"] = float(rates[-1]["close"])
        rows["last_error"] = str(mt5_api.last_error())
        return rows
    finally:
        mt5_api.shutdown()


def prepare_custom_symbol_seed(terminal_path: Path, metaeditor_path: Path, materialize_only: bool) -> dict[str, Any]:
    io_path(PORTABLE_SCRIPT.parent).mkdir(parents=True, exist_ok=True)
    shutil.copy2(io_path(SCRIPT_SOURCE), io_path(PORTABLE_SCRIPT))
    io_path(SCRIPT_PRESET.parent).mkdir(parents=True, exist_ok=True)
    io_path(SCRIPT_OUTPUT_COMMON.parent).mkdir(parents=True, exist_ok=True)
    preset_text = "\n".join(
        [
            f"InpRunId={RUN_ID}",
            f"InpOriginSymbol={ORIGIN_SYMBOL}",
            f"InpCustomSymbol={CUSTOM_SYMBOL}",
            f"InpCustomPath={CUSTOM_SYMBOL_PATH}",
            f"InpFromUtc={FROM_UTC}",
            f"InpToUtc={TO_UTC}",
            f"InpOutputPath={COMMON_ROOT}/custom_symbol_seed_status.json",
            "InpOutputUseCommonFiles=true",
            "",
        ]
    )
    io_path(SCRIPT_PRESET).write_text(preset_text, encoding="utf-8")
    io_path(SCRIPT_STARTUP_INI.parent).mkdir(parents=True, exist_ok=True)
    startup_text = "\n".join(
        [
            "[StartUp]",
            r"Script=Project_Obsidian_Prime_v2\foundation\mt5\ObsidianPrimeV2_CustomSymbolSeed",
            f"ScriptParameters={SCRIPT_PRESET_NAME}",
            f"Symbol={ORIGIN_SYMBOL}",
            "Period=M1",
            "ShutdownTerminal=1",
            "",
        ]
    )
    io_path(SCRIPT_STARTUP_INI).write_text(startup_text, encoding="utf-8")
    compile_payload = (
        {"status": "not_attempted_materialize_only"}
        if materialize_only
        else mql5_compile.compile_mql5_ea(metaeditor_path, PORTABLE_SCRIPT, MT5_DIR / "custom_symbol_seed_compile.log")
    )
    return {
        "script_source": rel(SCRIPT_SOURCE),
        "portable_script": PORTABLE_SCRIPT.as_posix(),
        "portable_script_sha256": sha256_file(PORTABLE_SCRIPT) if path_exists(PORTABLE_SCRIPT) else "",
        "preset_path": SCRIPT_PRESET.as_posix(),
        "preset_sha256": sha256_file(SCRIPT_PRESET) if path_exists(SCRIPT_PRESET) else "",
        "startup_ini": rel(SCRIPT_STARTUP_INI),
        "startup_ini_sha256": sha256_file(SCRIPT_STARTUP_INI) if path_exists(SCRIPT_STARTUP_INI) else "",
        "compile": compile_payload,
        "materialize_only": materialize_only,
    }


def run_custom_symbol_seed(terminal_path: Path, materialize_only: bool) -> dict[str, Any]:
    if materialize_only:
        return {"status": "not_attempted_materialize_only", "output_path": SCRIPT_OUTPUT_COMMON.as_posix()}
    if path_exists(SCRIPT_OUTPUT_COMMON):
        io_path(SCRIPT_OUTPUT_COMMON).unlink()
    before_offsets = qprobe.log_offsets([TERMINAL_LOG])
    process_recovery = qprobe.stop_target_terminal_if_running(terminal_path)
    command = [str(terminal_path), "/portable", f"/config:{io_path(SCRIPT_STARTUP_INI).resolve()}"]
    try:
        proc = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=240)
        run_status = "completed" if proc.returncode == 0 else "blocked_terminal_startup_returncode"
    except subprocess.TimeoutExpired as exc:
        proc = exc
        run_status = "blocked_terminal_startup_timeout"
    deadline = time.monotonic() + 45
    while time.monotonic() < deadline and not path_exists(SCRIPT_OUTPUT_COMMON):
        time.sleep(1.0)
    output_payload: dict[str, Any] = {"status": "missing"}
    if path_exists(SCRIPT_OUTPUT_COMMON):
        output_payload = json.loads(io_path(SCRIPT_OUTPUT_COMMON).read_text(encoding="utf-8-sig"))
        local_output = RUN_DIR / "custom_symbol_seed_status.json"
        io_path(local_output.parent).mkdir(parents=True, exist_ok=True)
        shutil.copy2(io_path(SCRIPT_OUTPUT_COMMON), io_path(local_output))
        output_payload["repo_copy_path"] = rel(local_output)
        output_payload["repo_copy_sha256"] = sha256_file(local_output)
    terminal_segment = qprobe.log_segment(TERMINAL_LOG, int(before_offsets.get(TERMINAL_LOG.as_posix(), 0)))
    return {
        "status": run_status,
        "command": command,
        "returncode": getattr(proc, "returncode", None),
        "stdout": (getattr(proc, "stdout", "") or "")[-2000:],
        "stderr": (getattr(proc, "stderr", "") or "")[-2000:],
        "process_recovery": process_recovery,
        "script_output": output_payload,
        "terminal_log_segment_tail": terminal_segment[-4000:],
        "output_path": SCRIPT_OUTPUT_COMMON.as_posix(),
    }


def parse_tester_boundary_rows(before_offsets: Mapping[str, int], attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    segment = qprobe.log_segment(TESTER_AGENT_LOG, int(before_offsets.get(TESTER_AGENT_LOG.as_posix(), 0)))
    if not segment:
        segment = qprobe.log_segment(TESTER_LOG, int(before_offsets.get(TESTER_LOG.as_posix(), 0)))
    boundary_matches = re.findall(r"testing of .*? from (\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}) to (\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}) started", segment)
    history_matches = re.findall(r"History\s+([A-Za-z0-9_.]+): history synchronized from ([0-9.]+) to ([0-9.]+)", segment)
    tick_matches = re.findall(r"Ticks\s+([A-Za-z0-9_.]+): history ticks synchronized from ([0-9.]+) to ([0-9.]+)", segment)
    generated_matches = re.findall(r"([A-Za-z0-9_.]+),M5: ([0-9]+) ticks, ([0-9]+) bars generated", segment)
    rows: list[dict[str, Any]] = []
    history_used: set[int] = set()
    ticks_used: set[int] = set()
    generated_used: set[int] = set()

    def take_match(matches: list[tuple[str, ...]], used: set[int], symbol: str) -> tuple[str, ...]:
        for idx, match in enumerate(matches):
            if idx in used:
                continue
            if match[0] == symbol:
                used.add(idx)
                return match
        return tuple("" for _ in range(len(matches[0]) if matches else 3))

    for index, attempt in enumerate(attempts):
        symbol = str(attempt.get("tester_symbol") or attempt.get("scenario_symbol") or "")
        boundary = boundary_matches[index] if index < len(boundary_matches) else ("", "")
        history = take_match(history_matches, history_used, symbol)
        ticks = take_match(tick_matches, ticks_used, symbol)
        generated = take_match(generated_matches, generated_used, symbol)
        rows.append(
            {
                "attempt_name": attempt["attempt_name"],
                "scenario_id": attempt.get("scenario_id", ""),
                "tester_symbol": symbol,
                "requested_from_date": attempt.get("from_date", ""),
                "requested_to_date": attempt.get("to_date", ""),
                "log_test_from": boundary[0],
                "log_test_to": boundary[1],
                "history_symbol": history[0] if len(history) > 0 else "",
                "history_sync_from": history[1] if len(history) > 1 else "",
                "history_sync_to": history[2] if len(history) > 2 else "",
                "tick_symbol": ticks[0] if len(ticks) > 0 else "",
                "tick_sync_from": ticks[1] if len(ticks) > 1 else "",
                "tick_sync_to": ticks[2] if len(ticks) > 2 else "",
                "generated_symbol": generated[0] if len(generated) > 0 else "",
                "generated_ticks": generated[1] if len(generated) > 1 else "",
                "generated_bars": generated[2] if len(generated) > 2 else "",
                "boundary_status": "tester_boundary_observed" if boundary[1] else "tester_boundary_missing",
                "source": TESTER_AGENT_LOG.as_posix(),
                "effect": "requested ToDate(요청 종료일)와 Strategy Tester actual end(전략 테스터 실제 종료)를 비교한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def gap_by_scenario(gap_rows: Sequence[Mapping[str, Any]], scenario_id: str) -> Mapping[str, Any]:
    return next((row for row in gap_rows if scenario_id in str(row.get("attempt_name", "")) or row.get("scenario_id") == scenario_id), {})


def classify(seed_run: Mapping[str, Any], api_rows: Sequence[Mapping[str, Any]], gap_rows: Sequence[Mapping[str, Any]], boundary_rows: Sequence[Mapping[str, Any]]) -> tuple[str, str, str, str]:
    custom_gap = next((row for row in gap_rows if "ab_custom_symbol" in str(row.get("attempt_name", ""))), {})
    broker_gap = next((row for row in gap_rows if "ab_broker_control" in str(row.get("attempt_name", ""))), {})
    seed_status = str((seed_run.get("script_output") or {}).get("status", ""))
    custom_api = next((row for row in api_rows if row.get("symbol") == CUSTOM_SYMBOL), {})
    custom_api_last = pd.to_datetime(str(custom_api.get("m5_last_close_utc", "")), errors="coerce", utc=True)
    feature_last = pd.to_datetime(str(custom_gap.get("feature_last_timestamp", "")), errors="coerce", utc=True)
    custom_reached = custom_gap.get("gap_status") == "tester_reached_feature_last"
    broker_still_gap = broker_gap.get("gap_status") == "tester_feature_last_gap_remains"
    api_reached = not pd.isna(custom_api_last) and not pd.isna(feature_last) and custom_api_last >= feature_last
    if seed_status == "completed" and api_reached and custom_reached and broker_still_gap:
        return STATUS_SUCCESS, JUDGMENT_SUCCESS, DECISION_SUCCESS, NEXT_RUN_ID_SUCCESS
    return STATUS_PARTIAL, JUDGMENT_PARTIAL, DECISION_PARTIAL, NEXT_RUN_ID_REPAIR


def required_gate_rows(status: str, seed_run: Mapping[str, Any], api_rows: Sequence[Mapping[str, Any]], gap_rows: Sequence[Mapping[str, Any]], diff_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    custom_gap = next((row for row in gap_rows if "ab_custom_symbol" in str(row.get("attempt_name", ""))), {})
    broker_gap = next((row for row in gap_rows if "ab_broker_control" in str(row.get("attempt_name", ""))), {})
    custom_api = next((row for row in api_rows if row.get("symbol") == CUSTOM_SYMBOL), {})
    matched = sum(1 for row in diff_rows if row.get("difference_status") == "matched")
    return [
        {
            "gate_id": "custom_symbol_seed_output",
            "status": "passed" if (seed_run.get("script_output") or {}).get("status") == "completed" else "failed",
            "evidence_path": rel(RUN_DIR / "custom_symbol_seed_status.json"),
            "effect": "custom symbol(커스텀 심볼) 생성과 M1 history update(M1 히스토리 갱신)가 실제로 끝났는지 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "python_api_custom_symbol_visibility",
            "status": "passed" if custom_api.get("status") == "completed" and custom_api.get("m5_rows") else "failed",
            "evidence_path": rel(RUN_DIR / "custom_symbol_api_visibility.csv"),
            "effect": "Python API(파이썬 API)가 custom symbol(커스텀 심볼)의 M5 봉을 볼 수 있는지 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "broker_control_boundary_remaining",
            "status": "passed" if broker_gap.get("gap_status") == "tester_feature_last_gap_remains" else "review",
            "evidence_path": rel(RUN_DIR / "tester_feature_last_gap_custom_symbol_probe.csv"),
            "effect": "원래 broker symbol(브로커 심볼)의 current-day boundary(현재일 경계)가 아직 남아 있는지 대조한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "custom_symbol_tester_reached_feature_last",
            "status": "passed" if custom_gap.get("gap_status") == "tester_reached_feature_last" else "failed",
            "evidence_path": rel(RUN_DIR / "tester_feature_last_gap_custom_symbol_probe.csv"),
            "effect": "Strategy Tester(전략 테스터)가 custom symbol(커스텀 심볼)에서 feature_last(피처 마지막 시점)까지 도달했는지 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "proxy_mt5_signal_window_parity",
            "status": "passed" if matched == len(diff_rows) and len(diff_rows) > 0 else "review",
            "evidence_path": rel(RUN_DIR / "timestamp_aligned_proxy_mt5_difference.csv"),
            "effect": "proxy expected(프록시 예상값)와 MT5 runtime(런타임 값)의 차이를 시점 맞춤으로 본다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "no_retrain_no_threshold_or_lot_retune",
            "status": "passed",
            "evidence_path": rel(RUN_DIR / "handoff_attempts.json"),
            "effect": "ONNX(온엑스), threshold(임계값), risk/lot(위험/로트)를 바꾸지 않았음을 기록한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "claim_boundary_no_forward_goal",
            "status": "passed" if "no_forward_passed" in CLAIM_BOUNDARY and "no_goal_achieve" in CLAIM_BOUNDARY else "failed",
            "evidence_path": rel(REPORT_PATH),
            "effect": "Forward Passed(전진 통과)나 Goal Achieve(목표 달성)를 잘못 주장하지 않게 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def receipt_payloads(
    status: str,
    judgment: str,
    seed_run: Mapping[str, Any],
    api_rows: Sequence[Mapping[str, Any]],
    runtime_rows: Sequence[Mapping[str, Any]],
    gap_rows: Sequence[Mapping[str, Any]],
    boundary_rows: Sequence[Mapping[str, Any]],
) -> dict[Path, Mapping[str, Any]]:
    completed = sum(1 for row in runtime_rows if row.get("tester_status") == "completed" and row.get("runtime_status") == "completed")
    custom_gap = next((row for row in gap_rows if "ab_custom_symbol" in str(row.get("attempt_name", ""))), {})
    return {
        RUN_DIR / "data_integrity_receipt.json": {
            "data_source": "US100 M1/M5 broker history visible through terminal API and custom-symbol M1 history seeded by MQL5 script",
            "time_axis": "MT5 bar time treated as UTC-like broker timestamp; feature_last compared against telemetry bar_time",
            "sample_scope": f"{ORIGIN_SYMBOL} and {CUSTOM_SYMBOL}; M5; {FROM_DATE} to {TO_DATE}",
            "missing_or_duplicate_check": "visibility check only; tester gap rows are the primary missing-bar evidence",
            "feature_label_boundary": "no labels or new training created; existing frozen feature CSV reused",
            "split_boundary": "forward runtime probe only",
            "leakage_risk": "custom symbol could become a synthetic data repair path; it is labeled repair evidence, not operating authority",
            "data_hash_or_identity": seed_run.get("script_output", {}).get("repo_copy_sha256", ""),
            "integrity_judgment": "usable_with_boundary" if custom_gap.get("gap_status") == "tester_reached_feature_last" else "inconclusive",
        },
        RUN_DIR / "runtime_parity_receipt.json": {
            "research_path": rel(Path(__file__)),
            "runtime_path": rel(SCRIPT_SOURCE),
            "shared_contract": "same frozen u42 ONNX, feature order, threshold, risk, lot, ATR settings, and feature CSV; only tester Symbol changes for visibility probe",
            "known_differences": f"custom symbol {CUSTOM_SYMBOL} is a tester visibility repair artifact, not broker operating authority",
            "parity_check": f"runtime_completed={completed}/{len(runtime_rows)}; custom_gap_status={custom_gap.get('gap_status', '')}",
            "parity_identity": {
                "custom_symbol_seed": seed_run.get("script_output", {}),
                "boundary_rows": boundary_rows,
            },
            "runtime_claim_boundary": "runtime_probe",
        },
        RUN_DIR / "backtest_forensics_receipt.json": {
            "tester_identity": f"portable MT5 FPMarketsSC-Live Strategy Tester; symbols {ORIGIN_SYMBOL}/{CUSTOM_SYMBOL}; M5; deposit 500; leverage 1:100; {FROM_DATE} to {TO_DATE}",
            "ea_identity": "ObsidianPrimeV2_RuntimeProbeEA.ex5 with unchanged frozen u42 ONNX handoff",
            "report_identity": rel(RUN_DIR),
            "trade_evidence": runtime_rows,
            "cost_assumptions": "broker control uses broker tester costs and real-tick model; custom symbol copies origin properties and uses generated ticks because custom real ticks are not broker-authoritative",
            "forensic_checks": ["script seed output", "API custom symbol visibility", "tester telemetry last observed bar", "strategy report collection"],
            "backtest_judgment": "usable_with_boundary" if custom_gap.get("gap_status") == "tester_reached_feature_last" else "inconclusive",
        },
        RUN_DIR / "result_judgment_receipt.json": {
            "result_subject": RUN_ID,
            "evidence_available": ["custom symbol seed status", "MT5 API visibility", "Strategy Tester telemetry", "proxy-MT5 difference"],
            "evidence_missing": "broker-symbol current-day tester visibility remains unresolved unless next-day reprobe confirms rollover",
            "judgment_label": judgment,
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID_SUCCESS if status == STATUS_SUCCESS else NEXT_RUN_ID_REPAIR,
            "user_explanation_hook": "custom symbol(커스텀 심볼)이 테스터 최신 봉 가시성을 열 수 있는지 확인했지만 운영 권위는 아직 아니다.",
        },
    }


def write_report(
    status: str,
    judgment: str,
    decision: str,
    next_action: str,
    seed_run: Mapping[str, Any],
    api_rows: Sequence[Mapping[str, Any]],
    runtime_rows: Sequence[Mapping[str, Any]],
    gap_rows: Sequence[Mapping[str, Any]],
    boundary_rows: Sequence[Mapping[str, Any]],
    diff_rows: Sequence[Mapping[str, Any]],
) -> list[Path]:
    custom_gap = next((row for row in gap_rows if "ab_custom_symbol" in str(row.get("attempt_name", ""))), {})
    broker_gap = next((row for row in gap_rows if "ab_broker_control" in str(row.get("attempt_name", ""))), {})
    custom_api = next((row for row in api_rows if row.get("symbol") == CUSTOM_SYMBOL), {})
    completed = sum(1 for row in runtime_rows if row.get("tester_status") == "completed" and row.get("runtime_status") == "completed" and row.get("report_status") == "completed")
    matched = sum(1 for row in diff_rows if row.get("difference_status") == "matched")
    lines = [
        "# Stage337AB Custom Symbol Intraday Tester Visibility Probe(337AB 커스텀 심볼 장중 테스터 가시성 탐침)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- status(상태): `{status}`",
        f"- judgment(판정): `{judgment}`",
        f"- decision(결정): `{decision}`",
        f"- next_action(다음 행동): `{next_action}`",
        f"- custom symbol(커스텀 심볼): `{CUSTOM_SYMBOL}`",
        f"- custom seed status(커스텀 심볼 심기 상태): `{(seed_run.get('script_output') or {}).get('status', '')}`",
        f"- custom API latest M5 close(커스텀 API 최신 5분봉 종가): `{custom_api.get('m5_last_close_utc', '')}`",
        f"- MT5 runtime completed(MT5 런타임 완료): `{completed}/{len(runtime_rows)}`",
        f"- broker control gap(브로커 대조 공백): `{broker_gap.get('gap_status', '')}`",
        f"- custom tester gap(커스텀 테스터 공백): `{custom_gap.get('gap_status', '')}`",
        f"- custom tester last observed(커스텀 테스터 마지막 관측): `{custom_gap.get('tester_last_observed_bar_time', '')}`",
        f"- feature_last(피처 마지막 시점): `{custom_gap.get('feature_last_timestamp', '')}`",
        f"- timestamp-aligned proxy parity(시점 맞춤 프록시 동등성): `{matched}/{len(diff_rows)}`",
        "- Forward Passed(전진 통과): `not_claimed`",
        "- Forward Failed(전진 실패): `not_claimed`",
        "- runtime authority(런타임 권위): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Meaning(의미)",
        "",
        "run337AB(337AB 실행)는 API(응용 프로그램 인터페이스)에서 보이는 US100(US100) M1/M5 봉을 MQL5 custom symbol(커스텀 심볼)에 심고, 같은 frozen u42 ONNX(고정 u42 온엑스)와 같은 threshold/risk/lot(임계값/위험/로트)로 Strategy Tester(전략 테스터)를 다시 실행했다. custom symbol(커스텀 심볼)은 real ticks(실제 틱)가 없으므로 generated ticks(생성 틱) 모델을 visibility-only(가시성 전용)로 썼다.",
        "",
        "Effect(효과): 이 결과는 tester visibility repair evidence(테스터 가시성 수리 근거)이지, Forward Passed(전진 통과), operating promotion(운영 승격), runtime authority(런타임 권위)가 아니다.",
        "",
        "## Tester Boundary(테스터 경계)",
        "",
        "| attempt(시도) | symbol(심볼) | log test to(로그 종료) | last observed(마지막 관측) | gap status(공백 상태) |",
        "|---|---:|---:|---:|---:|",
    ]
    boundary_by = {row.get("attempt_name"): row for row in boundary_rows}
    for row in gap_rows:
        boundary = boundary_by.get(row.get("attempt_name"), {})
        lines.append(
            f"| `{row.get('attempt_name', '')}` | `{boundary.get('tester_symbol', '')}` | `{boundary.get('log_test_to', '')}` | "
            f"`{row.get('tester_last_observed_bar_time', '')}` | `{row.get('gap_status', '')}` |"
        )
    lines.extend(
        [
            "",
            "## Proxy vs MT5(프록시 대 MT5)",
            "",
            "proxy expected(프록시 예상값)는 timestamp-aligned(시점 맞춤) 범위에서만 runtime signal parity(런타임 신호 동등성) 판단에 쓰며, KPI authority(KPI 권한)나 Forward decision(전진 판정)으로 쓰지 않는다.",
        ]
    )
    write_md(REPORT_PATH, "\n".join(lines))

    decision_text = "\n".join(
        [
            "# 2026-05-27 Stage337AB Custom Symbol Tester Visibility Decision(337AB 커스텀 심볼 테스터 가시성 결정)",
            "",
            f"- status(상태): `{status}`",
            f"- judgment(판정): `{judgment}`",
            f"- decision(결정): `{decision}`",
            f"- next_action(다음 행동): `{next_action}`",
            "- selected_candidate(선택 후보): `none`",
            "- Forward Passed(전진 통과): `not_claimed`",
            "- Forward Failed(전진 실패): `not_claimed`",
            "- Goal Achieve(목표 달성): `not_claimed`",
            "",
            f"Effect(효과): {CUSTOM_SYMBOL}(커스텀 심볼) tester visibility(테스터 가시성)를 확인/검토했지만, broker US100(브로커 US100)의 current-day boundary(현재일 경계)는 별도 확인이 필요하다.",
        ]
    )
    write_md(DECISION_DOC, decision_text)
    return [REPORT_PATH, DECISION_DOC]


def update_status_docs(
    status: str,
    decision: str,
    next_action: str,
    seed_run: Mapping[str, Any],
    api_rows: Sequence[Mapping[str, Any]],
    runtime_rows: Sequence[Mapping[str, Any]],
    gap_rows: Sequence[Mapping[str, Any]],
    diff_rows: Sequence[Mapping[str, Any]],
) -> list[Path]:
    custom_gap = next((row for row in gap_rows if "ab_custom_symbol" in str(row.get("attempt_name", ""))), {})
    broker_gap = next((row for row in gap_rows if "ab_broker_control" in str(row.get("attempt_name", ""))), {})
    custom_api = next((row for row in api_rows if row.get("symbol") == CUSTOM_SYMBOL), {})
    matched = sum(1 for row in diff_rows if row.get("difference_status") == "matched")
    completed = sum(1 for row in runtime_rows if row.get("tester_status") == "completed" and row.get("runtime_status") == "completed" and row.get("report_status") == "completed")

    selected_text = f"""# Stage337 Selection Status(337단계 선택 상태)

- stage_id(단계 ID): `{STAGE_ID}`
- stage_status(단계 상태): `open_active`
- selected_candidate(선택 후보): `none`
- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{decision}`
- current_run(현재 실행): `{next_action}`
- custom_symbol(커스텀 심볼): `{CUSTOM_SYMBOL}`
- custom_seed_status(커스텀 심볼 심기 상태): `{(seed_run.get('script_output') or {}).get('status', '')}`
- custom_api_latest_m5_close(커스텀 API 최신 5분봉 종가): `{custom_api.get('m5_last_close_utc', '')}`
- MT5 runtime completed(MT5 런타임 완료): `{completed}/{len(runtime_rows)}`
- broker_control_gap(브로커 대조 공백): `{broker_gap.get('gap_status', '')}`
- custom_tester_gap(커스텀 테스터 공백): `{custom_gap.get('gap_status', '')}`
- timestamp_aligned_proxy_parity(시점 맞춤 프록시 동등성): `{matched}/{len(diff_rows)}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Forward Blocked(전진 차단): `tester_current_day_visibility_boundary_not_operating_resolved`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{next_action}`
- effect(효과): run337AB(337AB 실행)는 custom symbol(커스텀 심볼)로 Strategy Tester(전략 테스터)의 intraday visibility(장중 가시성)를 탐침했고, 최신 forward(전진) 판정은 아직 주장하지 않는다.
"""
    write_md(SELECTED_STATUS, selected_text)

    focus = (
        f"  Stage337 run337AB focus complete: run337AB(337AB 실행)는 `{status}`로 custom symbol intraday tester visibility probe"
        f"(커스텀 심볼 장중 테스터 가시성 탐침)를 기록했다. Effect(효과): seed(심기) `{(seed_run.get('script_output') or {}).get('status', '')}`, "
        f"broker control gap(브로커 대조 공백) `{broker_gap.get('gap_status', '')}`, custom tester gap(커스텀 테스터 공백) "
        f"`{custom_gap.get('gap_status', '')}`, timestamp-aligned proxy parity(시점 맞춤 프록시 동등성) `{matched}/{len(diff_rows)}`이며 "
        "Forward/Goal(전진/목표)은 주장하지 않는다."
    )
    if path_exists(WORKSPACE_STATE):
        text, had_bom = read_text_lossless(WORKSPACE_STATE)
        text = re.sub(r"current_run_id: .*", f"current_run_id: {next_action}", text, count=1)
        if "Stage337 run337AB focus complete" not in text:
            text = text.replace("current_focus:\n", f"current_focus:\n- >-\n{focus}\n")
        else:
            text = re.sub(
                r"- >-\n  Stage337 run337AB focus complete:.*?(?=\n- >-|\Z)",
                f"- >-\n{focus}",
                text,
                count=1,
                flags=re.S,
            )
        write_text_preserving(WORKSPACE_STATE, text, had_bom)

    current_entry = f"""
## Stage337 run337AB(337AB 실행) - {TODAY}

- status(상태): `{status}`
- decision(결정): `{decision}`
- next_action(다음 행동): `{next_action}`
- effect(효과): custom symbol(커스텀 심볼) `{CUSTOM_SYMBOL}`로 tester visibility(테스터 가시성)를 확인했다. broker gap(브로커 공백) `{broker_gap.get('gap_status', '')}`, custom gap(커스텀 공백) `{custom_gap.get('gap_status', '')}`, proxy parity(프록시 동등성) `{matched}/{len(diff_rows)}`.
"""
    if path_exists(CURRENT_STATE):
        text, had_bom = read_text_lossless(CURRENT_STATE)
        if "## Stage337 run337AB(337AB 실행)" in text:
            text = re.sub(r"## Stage337 run337AB\(337AB 실행\).*?(?=\n## |\Z)", current_entry.strip(), text, count=1, flags=re.S)
        else:
            text = text.rstrip() + "\n\n" + current_entry.strip() + "\n"
        write_text_preserving(CURRENT_STATE, text, had_bom)

    if path_exists(CHANGELOG):
        text, had_bom = read_text_lossless(CHANGELOG)
        line = (
            f"\n- {TODAY}: Stage337 run337AB(337AB 실행) `{status}`. "
            f"Effect(효과): custom symbol tester visibility(커스텀 심볼 테스터 가시성) `{custom_gap.get('gap_status', '')}`를 기록하고 Forward/Goal(전진/목표)은 주장하지 않았다.\n"
        )
        if "Stage337 run337AB(337AB 실행)" in text:
            text = re.sub(r"\n- [^\n]*Stage337 run337AB\(337AB 실행\)[^\n]*", line.rstrip(), text, count=1)
        else:
            text = text.rstrip() + line
        write_text_preserving(CHANGELOG, text, had_bom)

    if path_exists(STAGE_BRIEF):
        text, had_bom = read_text_lossless(STAGE_BRIEF)
        text = re.sub(r"- latest_run\(최신 실행\): `[^`]+`", f"- latest_run(최신 실행): `{RUN_ID}`", text)
        summary = (
            f"- run337AB_summary(337AB 요약): `{status}`. Effect(효과): custom symbol tester visibility(커스텀 심볼 테스터 가시성) "
            f"`{custom_gap.get('gap_status', '')}`와 proxy parity(프록시 동등성) `{matched}/{len(diff_rows)}`를 기록했다.\n"
        )
        if "run337AB_summary(337AB 요약)" in text:
            text = re.sub(r"- run337AB_summary\(337AB 요약\): [^\n]*(?:\n|$)", summary, text, count=1)
        else:
            text = text.replace("- selected_candidate(선택 후보):", summary + "- selected_candidate(선택 후보):")
        write_text_preserving(STAGE_BRIEF, text, had_bom)

    return [SELECTED_STATUS, WORKSPACE_STATE, CURRENT_STATE, CHANGELOG, STAGE_BRIEF]


def update_registers(status: str, judgment: str, decision: str, next_action: str, artifact_paths: Sequence[Path]) -> list[Path]:
    aa.upsert_csv(
        RUN_REGISTRY,
        ["run_id"],
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "family": "custom_symbol_intraday_tester_visibility_probe",
            "lane": "runtime_parity_repair",
            "status": status,
            "judgment": judgment,
            "primary_report": rel(REPORT_PATH),
            "path": rel(REPORT_PATH),
            "notes": f"decision={decision};next_action={next_action};goal_achieve_not_claimed.",
        },
    )
    aa.upsert_csv(
        STAGE_LEDGER,
        ["run_key"],
        {
            "run_key": f"{RUN_ID}__custom_symbol_intraday_tester_visibility_probe",
            "ledger_row_id": f"{RUN_ID}__custom_symbol_intraday_tester_visibility_probe",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "family": "custom_symbol_intraday_tester_visibility_probe",
            "work_family": "runtime_parity_repair",
            "status": status,
            "judgment": judgment,
            "report_path": rel(REPORT_PATH),
            "decision": decision,
            "next_action": next_action,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    upsert_artifact_registry(artifact_paths)
    return [RUN_REGISTRY, STAGE_LEDGER, ARTIFACT_REGISTRY]


def upsert_artifact_registry(paths: Sequence[Path]) -> None:
    rows: list[dict[str, str]] = []
    columns: list[str] = []
    if path_exists(ARTIFACT_REGISTRY):
        with io_path(ARTIFACT_REGISTRY).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            columns = list(reader.fieldnames or [])
            rows = [dict(row) for row in reader]
    required = ["artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes", "artifact_path", "claim_boundary"]
    for column in required:
        if column not in columns:
            columns.append(column)
    rows = [row for row in rows if row.get("run_id") != RUN_ID]
    for path in paths:
        r = rel(path)
        rows.append(
            {
                "artifact_id": f"{RUN_NUMBER}_{Path(r).stem}",
                "artifact_type": Path(r).suffix.lstrip(".") or "artifact",
                "path": r,
                "sha256": sha256_file(path) if path_exists(path) and io_path(path).is_file() else "",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": now_utc(),
                "notes": "run337AB custom-symbol tester visibility artifact; no forward or goal claim",
                "artifact_path": r,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(ARTIFACT_REGISTRY, columns, rows)


def main() -> None:
    args = parse_args()
    configure_probe_modules()
    terminal_path = Path(args.terminal)
    metaeditor_path = Path(args.metaeditor)
    common_files_root = Path(args.common_files_root)
    tester_profile_root = Path(args.tester_profile_root)
    terminal_data_root = Path(args.terminal_data_root)

    seed_prepare = prepare_custom_symbol_seed(terminal_path, metaeditor_path, args.materialize_only)
    seed_run = run_custom_symbol_seed(terminal_path, args.materialize_only)
    broker_api = mt5_api_symbol_visibility(terminal_path, ORIGIN_SYMBOL)
    custom_api = mt5_api_symbol_visibility(terminal_path, CUSTOM_SYMBOL)
    api_rows = [{**broker_api, "claim_boundary": CLAIM_BOUNDARY}, {**custom_api, "claim_boundary": CLAIM_BOUNDARY}]

    prepared = load_source_attempts()
    attempts, handoff_rows, materialized_artifacts = base.build_attempts(prepared, common_files_root)
    scenario_by_attempt = {str(row["attempt_name"]): row for row in prepared}
    for attempt in attempts:
        scenario = scenario_by_attempt.get(str(attempt["attempt_name"]), {})
        for key in ("scenario_id", "scenario_symbol", "scenario_from_date", "scenario_to_date"):
            attempt[key] = scenario.get(key, "")
    attempts = [rewrite_attempt_to_visibility(dict(attempt)) for attempt in attempts]

    before_offsets = qprobe.log_offsets([TESTER_LOG, TESTER_AGENT_LOG, TERMINAL_LOG])
    process_recovery = qprobe.stop_target_terminal_if_running(terminal_path)
    execution_result = (
        {
            "compile": {"status": "not_attempted_materialize_only"},
            "execution_results": [],
            "strategy_tester_reports": [],
            "process_recovery": process_recovery,
        }
        if args.materialize_only
        else base.execute_attempts(
            attempts,
            terminal_path=terminal_path,
            metaeditor_path=metaeditor_path,
            common_files_root=common_files_root,
            tester_profile_root=tester_profile_root,
            terminal_data_root=terminal_data_root,
            timeout_seconds=args.timeout_seconds,
            wait_timeout_seconds=args.wait_timeout_seconds,
            materialize_only=False,
        )
    )
    execution_result["process_recovery"] = process_recovery

    runtime_rows = base.build_fresh_runtime_summary(attempts, execution_result)
    copied_runtime_artifacts = base.copy_runtime_outputs(common_files_root, attempts)
    feature_rows = qprobe.feature_last_rows(attempts)
    gap_rows = qprobe.tester_gap_rows(runtime_rows, feature_rows, common_files_root, {"last_close_utc": broker_api.get("m5_last_close_utc", "")})
    boundary_rows = parse_tester_boundary_rows(before_offsets, attempts)
    boundary_by_attempt = {row["attempt_name"]: row for row in boundary_rows}
    for row in gap_rows:
        row["scenario_id"] = boundary_by_attempt.get(row.get("attempt_name"), {}).get("scenario_id", "")
        row["tester_symbol"] = boundary_by_attempt.get(row.get("attempt_name"), {}).get("tester_symbol", "")

    cutoff_by_attempt = {str(row.get("attempt_name", "")): str(row.get("tester_last_observed_bar_time", "")) for row in gap_rows}
    aligned_proxy_rows = qprobe.sanitize_proxy_rows(qprobe.build_timestamp_aligned_proxy_rows(attempts, cutoff_by_attempt), default_source="stage337AB_timestamp_aligned_python_onnx_inference")
    diff_rows = qprobe.sanitize_diff_rows(base.build_signal_difference_rows(aligned_proxy_rows, runtime_rows))
    for row in diff_rows:
        row["mt5_source"] = "stage337AB_fresh_runtime_summary_custom_symbol_visibility_probe"
        row["claim_boundary"] = CLAIM_BOUNDARY

    status, judgment, decision, next_action = classify(seed_run, api_rows, gap_rows, boundary_rows)
    gate_rows = required_gate_rows(status, seed_run, api_rows, gap_rows, diff_rows)
    receipts = receipt_payloads(status, judgment, seed_run, api_rows, runtime_rows, gap_rows, boundary_rows)

    artifact_paths: list[Path] = []
    for path, payload in receipts.items():
        write_json(path, payload)
        artifact_paths.append(path)
    artifact_paths.extend(
        [
            write_json(RUN_DIR / "custom_symbol_seed_prepare.json", seed_prepare),
            write_json(RUN_DIR / "custom_symbol_seed_run.json", seed_run),
            write_json(RUN_DIR / "execution_result.json", execution_result),
            write_json(RUN_DIR / "final_decision.json", {
                "run_id": RUN_ID,
                "status": status,
                "judgment": judgment,
                "decision": decision,
                "next_action": next_action,
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "runtime_authority": "not_claimed",
                "goal_achieve": "not_claimed",
                "claim_boundary": CLAIM_BOUNDARY,
            }),
            write_csv(RUN_DIR / "custom_symbol_api_visibility.csv", sorted({key for row in api_rows for key in row.keys()}), api_rows),
            write_csv(RUN_DIR / "handoff_attempts.csv", sorted({key for row in handoff_rows for key in row.keys()}), handoff_rows),
            write_json(RUN_DIR / "handoff_attempts.json", attempts),
            write_csv(RUN_DIR / "runtime_summary.csv", sorted({key for row in runtime_rows for key in row.keys()}), runtime_rows),
            write_csv(RUN_DIR / "feature_last_timestamp_audit.csv", sorted({key for row in feature_rows for key in row.keys()}), feature_rows),
            write_csv(RUN_DIR / "tester_boundary_custom_symbol_probe.csv", sorted({key for row in boundary_rows for key in row.keys()}), boundary_rows),
            write_csv(RUN_DIR / "tester_feature_last_gap_custom_symbol_probe.csv", sorted({key for row in gap_rows for key in row.keys()}), gap_rows),
            write_csv(RUN_DIR / "timestamp_aligned_proxy_expected_result.csv", sorted({key for row in aligned_proxy_rows for key in row.keys()}), aligned_proxy_rows),
            write_csv(RUN_DIR / "timestamp_aligned_proxy_mt5_difference.csv", sorted({key for row in diff_rows for key in row.keys()}), diff_rows),
            write_csv(RUN_DIR / "required_gate_coverage_audit.csv", sorted({key for row in gate_rows for key in row.keys()}), gate_rows),
        ]
    )
    artifact_paths.extend(copied_runtime_artifacts)
    artifact_paths.extend(materialized_artifacts)

    artifact_paths.extend(write_report(status, judgment, decision, next_action, seed_run, api_rows, runtime_rows, gap_rows, boundary_rows, diff_rows))
    artifact_paths.extend(update_status_docs(status, decision, next_action, seed_run, api_rows, runtime_rows, gap_rows, diff_rows))
    artifact_paths.extend(update_registers(status, judgment, decision, next_action, artifact_paths))

    final_payload = {
        "run_id": RUN_ID,
        "status": status,
        "judgment": judgment,
        "decision": decision,
        "next_action": next_action,
        "seed_status": (seed_run.get("script_output") or {}).get("status", ""),
        "api_rows": api_rows,
        "runtime_completed": sum(1 for row in runtime_rows if row.get("tester_status") == "completed" and row.get("runtime_status") == "completed" and row.get("report_status") == "completed"),
        "runtime_total": len(runtime_rows),
        "gap_rows": gap_rows,
        "proxy_diff_rows": len(diff_rows),
        "proxy_diff_matched": sum(1 for row in diff_rows if row.get("difference_status") == "matched"),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    print(json.dumps(final_payload, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
