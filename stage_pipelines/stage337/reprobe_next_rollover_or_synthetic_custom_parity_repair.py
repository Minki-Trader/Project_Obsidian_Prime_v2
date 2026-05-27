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
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, path_exists, sha256_file_lf_normalized  # noqa: E402
from foundation.mt5 import mql5_compile, runtime_support as mt5  # noqa: E402
from foundation.mt5.runtime_artifacts import sha256_file  # noqa: E402
from stage_pipelines.stage335 import independent_proxy_mt5_probe as base  # noqa: E402
from stage_pipelines.stage337 import probe_custom_symbol_intraday_tester_visibility as ab  # noqa: E402
from stage_pipelines.stage337 import review_runtime_data_and_feature_source_repair_probe as qprobe  # noqa: E402


TODAY = "2026-05-27"
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
RUN_NUMBER = "run337AK"
RUN_ID = "run337AK_next_rollover_or_synthetic_custom_parity_repair_v1"
PARENT_RUN_ID = "run337AJ_data_history_cache_repair_or_next_rollover_wait_reprobe_v1"
NEXT_RUN_ID_BROKER_REPAIRED = "run337AL_broker_forward_boundary_attribution_after_reach_v1"
NEXT_RUN_ID_SYNTHETIC_REPAIRED = "run337AL_exact_timestamp_policy_boundary_or_broker_rollover_wait_v1"
NEXT_RUN_ID_REPAIR = "run337AL_synthetic_custom_or_runtime_parity_repair_v1"
CLAIM_BOUNDARY = (
    "research_development_only_stage337AK_synthetic_custom_exact_timestamp_parity_repair_"
    "no_model_training_no_threshold_retuning_no_lot_optimization_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STATUS_BROKER_REPAIRED = "completed_stage337AK_broker_reached_feature_last_exact_timestamp_parity_no_forward_decision"
STATUS_SYNTHETIC_REPAIRED = "completed_stage337AK_synthetic_custom_exact_timestamp_proxy_parity_repaired_no_forward_decision"
STATUS_RUNTIME_ISSUE = "completed_stage337AK_runtime_issue_no_forward_decision"
STATUS_MISMATCH = "completed_stage337AK_exact_timestamp_proxy_mismatch_no_forward_decision"
STATUS_MATERIALIZED = "completed_stage337AK_materialized_only_no_forward_decision"
JUDGMENT_BROKER_REPAIRED = "broker_tester_boundary_reached_feature_last_but_forward_decision_still_not_claimed"
JUDGMENT_SYNTHETIC_REPAIRED = "synthetic_custom_tester_cycle_exact_proxy_parity_repaired_broker_gap_remains"
JUDGMENT_RUNTIME_ISSUE = "runtime_or_seed_issue_blocks_synthetic_parity_judgment"
JUDGMENT_MISMATCH = "exact_tester_cycle_proxy_still_mismatches_mt5_runtime"
JUDGMENT_MATERIALIZED = "run337AK_inputs_materialized_execution_pending"
DECISION_BROKER_REPAIRED = "stage337AK_open_run337AL_broker_boundary_attribution_no_selection"
DECISION_SYNTHETIC_REPAIRED = "stage337AK_open_run337AL_boundary_policy_or_rollover_wait_no_selection"
DECISION_RUNTIME_ISSUE = "stage337AK_runtime_or_seed_repair_continues_no_selection"
DECISION_MISMATCH = "stage337AK_exact_timestamp_proxy_mismatch_repair_continues_no_selection"
DECISION_MATERIALIZED = "stage337AK_execution_pending_no_selection"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
RUN337Z_DIR = STAGE_DIR / "02_runs" / "run337Z"
RUN337Z_ATTEMPTS = RUN337Z_DIR / "rollover_reprobe_handoff_attempts.json"
MT5_DIR = RUN_DIR / "mt5"
FEATURE_COPY_DIR = RUN_DIR / "feature_matrices"
MODEL_COPY_DIR = RUN_DIR / "models"
TELEMETRY_DIR = RUN_DIR / "runtime_telemetry"
SEED_INPUT_DIR = RUN_DIR / "seed_repair_inputs"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEWS_DIR / "run337AK_synthetic_custom_exact_timestamp_parity_repair.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage337AK_synthetic_custom_exact_timestamp_parity_repair.md"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
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

COMMON_ROOT = "Project_Obsidian_Prime_v2/stage337/run337AK_synthetic_custom_exact_timestamp_parity_repair"
ORIGIN_SYMBOL = "US100"
SHIFTED_CUSTOM_SYMBOL = "US100.OPV337AKM"
CUSTOM_SYMBOL_PATH = "ObsidianPrime"
SHIFT_MINUTES = -1440
FROM_UTC = "2026.04.14 00:00:00"
TO_UTC = "2026.05.28 00:00:00"
BROKER_FROM_DATE = "2026.04.14"
BROKER_TO_DATE = "2026.05.30"
SHIFTED_FROM_DATE = "2026.04.13"
SHIFTED_TO_DATE = "2026.05.28"
ATTEMPT_BASE = "u42_plain_rf"
SCRIPT_SOURCE = ROOT / "foundation" / "mt5" / "ObsidianPrimeV2_CustomSymbolSeed.mq5"
PORTABLE_SCRIPT = DEFAULT_PORTABLE_ROOT / "MQL5" / "Scripts" / "Project_Obsidian_Prime_v2" / "foundation" / "mt5" / "ObsidianPrimeV2_CustomSymbolSeed.mq5"
SCRIPT_PRESET_NAME = "opv2_run337AK_shifted_custom_symbol_seed.set"
SCRIPT_PRESET = DEFAULT_PORTABLE_ROOT / "MQL5" / "Presets" / SCRIPT_PRESET_NAME
SCRIPT_STARTUP_INI = MT5_DIR / "shifted_custom_symbol_seed_startup.ini"
SCRIPT_OUTPUT_COMMON = DEFAULT_COMMON_FILES / COMMON_ROOT / "shifted_custom_symbol_seed_status.json"


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return item.as_posix()


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


def columns_for(rows: Sequence[Mapping[str, Any]], defaults: Sequence[str] | None = None) -> list[str]:
    columns: list[str] = list(defaults or [])
    for row in rows:
        for column in row:
            if column not in columns:
                columns.append(column)
    return columns


def write_csv(path: Path, columns: Sequence[str], rows: Iterable[Mapping[str, Any]]) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    tmp = io_path(path).with_name(io_path(path).name + ".tmp")
    with tmp.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column, "")) for column in columns})
    os.replace(tmp, io_path(path))
    return path


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_json(path: Path, payload: Any) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_md(path: Path, text: str) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")
    return path


def read_text(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    had_bom = raw.startswith(b"\xef\xbb\xbf")
    return raw.decode("utf-8-sig" if had_bom else "utf-8"), had_bom


def write_text(path: Path, text: str, had_bom: bool) -> Path:
    encoding = "utf-8-sig" if had_bom or path.suffix.lower() in {".md", ".txt"} else "utf-8"
    io_path(path).write_text(text.replace("\r\n", "\n").replace("\r", "\n"), encoding=encoding, newline="\n")
    return path


def upsert_csv(path: Path, key_columns: Sequence[str], row: Mapping[str, Any]) -> Path:
    rows = read_csv(path)
    columns = list(rows[0].keys()) if rows else list(row.keys())
    for column in row:
        if column not in columns:
            columns.append(column)
    key = tuple(str(row.get(column, "")) for column in key_columns)
    rows = [item for item in rows if tuple(str(item.get(column, "")) for column in key_columns) != key]
    rows.append({column: csv_value(row.get(column, "")) for column in columns})
    return write_csv(path, columns, rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stage337AK synthetic custom exact-timestamp proxy/MT5 parity repair.")
    parser.add_argument("--terminal", default=str(DEFAULT_TERMINAL))
    parser.add_argument("--metaeditor", default=str(DEFAULT_METAEDITOR))
    parser.add_argument("--common-files-root", default=str(DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-data-root", default=str(DEFAULT_TERMINAL_DATA_ROOT))
    parser.add_argument("--timeout-seconds", type=int, default=1200)
    parser.add_argument("--wait-timeout-seconds", type=int, default=240)
    parser.add_argument("--materialize-only", action="store_true")
    return parser.parse_args()


def configure_probe_modules() -> None:
    for module in (base, qprobe, ab):
        module.TODAY = TODAY
        module.STAGE_ID = STAGE_ID
        module.RUN_NUMBER = RUN_NUMBER
        module.RUN_ID = RUN_ID
        module.PARENT_RUN_ID = PARENT_RUN_ID
        module.CLAIM_BOUNDARY = CLAIM_BOUNDARY
        module.RUN_DIR = RUN_DIR
        module.MT5_DIR = MT5_DIR
        module.FEATURE_COPY_DIR = FEATURE_COPY_DIR
        module.MODEL_COPY_DIR = MODEL_COPY_DIR
        module.TELEMETRY_DIR = TELEMETRY_DIR
        module.DEFAULT_PORTABLE_ROOT = DEFAULT_PORTABLE_ROOT
        module.DEFAULT_TERMINAL = DEFAULT_TERMINAL
        module.DEFAULT_METAEDITOR = DEFAULT_METAEDITOR
        module.DEFAULT_COMMON_FILES = DEFAULT_COMMON_FILES
        module.DEFAULT_TESTER_PROFILE_ROOT = DEFAULT_TESTER_PROFILE_ROOT
        module.DEFAULT_TERMINAL_DATA_ROOT = DEFAULT_TERMINAL_DATA_ROOT
        module.TESTER_LOG = TESTER_LOG
        module.TESTER_AGENT_LOG = TESTER_AGENT_LOG
        module.TERMINAL_LOG = TERMINAL_LOG
        module.COMMON_ROOT = COMMON_ROOT
    base.STAGE_DIR = STAGE_DIR
    base.REVIEWS_DIR = REVIEWS_DIR
    base.PORTABLE_EA_SOURCE = DEFAULT_PORTABLE_ROOT / "MQL5" / "Experts" / mt5.EA_SOURCE_PATH
    base.PORTABLE_EA_EX5 = DEFAULT_PORTABLE_ROOT / "MQL5" / "Experts" / "Project_Obsidian_Prime_v2" / "foundation" / "mt5" / "ObsidianPrimeV2_RuntimeProbeEA.ex5"


def load_source_u42() -> dict[str, Any]:
    rows = read_json(RUN337Z_ATTEMPTS)
    source = next((row for row in rows if row.get("attempt_name") == ATTEMPT_BASE), None)
    if source is None:
        raise RuntimeError(f"missing {ATTEMPT_BASE} in {RUN337Z_ATTEMPTS}")
    return dict(source)


def shift_feature_csv(source_path: Path, target_path: Path, shift_minutes: int) -> Path:
    frame = pd.read_csv(io_path(source_path))
    delta = timedelta(minutes=shift_minutes)
    if "timestamp_utc" in frame.columns:
        ts = pd.to_datetime(frame["timestamp_utc"], errors="coerce", utc=True) + delta
        frame["timestamp_utc"] = ts.dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    if "bar_time_server" in frame.columns:
        server = pd.to_datetime(frame["bar_time_server"].astype(str).str.replace(".", "-", regex=False), errors="coerce", utc=True) + delta
        frame["bar_time_server"] = server.dt.strftime("%Y.%m.%d %H:%M:%S")
    if "split" in frame.columns:
        frame["split"] = frame["split"].astype(str) + f"__synthetic_shift_{shift_minutes}m"
    io_path(target_path.parent).mkdir(parents=True, exist_ok=True)
    frame.to_csv(io_path(target_path), index=False, lineterminator="\n")
    return target_path


def build_source_attempts(source: Mapping[str, Any], shifted_feature_path: Path) -> list[dict[str, Any]]:
    scenarios = [
        {
            "suffix": "ak_broker_rollover_control",
            "scenario_id": "broker_current_day_boundary_control_after_cache_warmup",
            "symbol": ORIGIN_SYMBOL,
            "feature_path": source.get("feature_local_path", ""),
            "from_date": BROKER_FROM_DATE,
            "to_date": BROKER_TO_DATE,
            "model": "4",
            "role": "broker control(브로커 대조군): original timestamps(원래 시각), real ticks(실제 틱)",
        },
        {
            "suffix": "ak_shifted_custom_exact_timestamp",
            "scenario_id": "custom_symbol_shift_minus_1440m_exact_timestamp_parity",
            "symbol": SHIFTED_CUSTOM_SYMBOL,
            "feature_path": rel(shifted_feature_path),
            "from_date": SHIFTED_FROM_DATE,
            "to_date": SHIFTED_TO_DATE,
            "model": "0",
            "role": "synthetic custom diagnostic(합성 커스텀 진단): no forward KPI authority(전진 KPI 권한 없음)",
        },
    ]
    selected: list[dict[str, Any]] = []
    for index, scenario in enumerate(scenarios):
        copied = dict(source)
        copied["attempt_name"] = f"u42_plain_rf_{scenario['suffix']}"
        copied["artifact_slug"] = f"u42_plain_{scenario['suffix']}"
        copied["scenario_id"] = scenario["scenario_id"]
        copied["scenario_symbol"] = scenario["symbol"]
        copied["scenario_from_date"] = scenario["from_date"]
        copied["scenario_to_date"] = scenario["to_date"]
        copied["scenario_model"] = scenario["model"]
        copied["scenario_role"] = scenario["role"]
        copied["model_copy"] = {"source": source.get("model_local_path", "")}
        copied["feature_export"] = {"path": scenario["feature_path"]}
        copied["source_run_id"] = PARENT_RUN_ID
        copied["attempt_role"] = "stage337AK_synthetic_custom_exact_timestamp_parity_same_frozen_u42_model_threshold_risk"
        copied["record_view_prefix"] = f"mt5_stage337AK_u42_plain_{index}"
        selected.append(copied)
    return selected


def rewrite_attempt_to_scenario(attempt: dict[str, Any]) -> dict[str, Any]:
    tester = dict(attempt["ini"]["tester"])
    tester["Symbol"] = attempt["scenario_symbol"]
    tester["FromDate"] = attempt["scenario_from_date"]
    tester["ToDate"] = attempt["scenario_to_date"]
    tester["Model"] = attempt["scenario_model"]
    tester["Report"] = f"Project_Obsidian_Prime_v2_{RUN_ID}_{attempt['attempt_name']}"
    attempt["ini"] = base.materialize_ini_file(tester, Path(str(attempt["ini"]["path"])))
    attempt["from_date"] = tester["FromDate"]
    attempt["to_date"] = tester["ToDate"]
    attempt["tester_symbol"] = tester["Symbol"]
    attempt["tester_model"] = tester.get("Model", "")
    attempt["attempt_role"] = "stage337AK_runtime_boundary_exact_timestamp_proxy_repair_same_frozen_u42_model_threshold_risk"
    attempt["record_view_prefix"] = f"mt5_stage337AK_{attempt['artifact_slug']}"
    attempt["source_run_id"] = PARENT_RUN_ID
    attempt["repair_contract"] = (
        "Only tester symbol/date/model mode and artifact paths are diagnostic inputs. ONNX, feature order, "
        "D/B surface, score threshold, risk, lot, and ATR SL/TP stay frozen."
    )
    attempt["signal_policy"] = "exact tester-cycle timestamp proxy diagnostic only; not Forward Passed/Failed authority"
    return attempt


def prepare_shifted_seed(terminal_path: Path, metaeditor_path: Path, materialize_only: bool) -> dict[str, Any]:
    io_path(PORTABLE_SCRIPT.parent).mkdir(parents=True, exist_ok=True)
    shutil.copy2(io_path(SCRIPT_SOURCE), io_path(PORTABLE_SCRIPT))
    io_path(SCRIPT_PRESET.parent).mkdir(parents=True, exist_ok=True)
    io_path(SCRIPT_OUTPUT_COMMON.parent).mkdir(parents=True, exist_ok=True)
    preset_text = "\n".join(
        [
            f"InpRunId={RUN_ID}",
            f"InpOriginSymbol={ORIGIN_SYMBOL}",
            f"InpCustomSymbol={SHIFTED_CUSTOM_SYMBOL}",
            f"InpCustomPath={CUSTOM_SYMBOL_PATH}",
            f"InpFromUtc={FROM_UTC}",
            f"InpToUtc={TO_UTC}",
            f"InpOutputPath={COMMON_ROOT}/shifted_custom_symbol_seed_status.json",
            "InpOutputUseCommonFiles=true",
            f"InpShiftMinutes={SHIFT_MINUTES}",
            "",
        ]
    )
    io_path(SCRIPT_PRESET).write_text(preset_text, encoding="utf-8")
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
    io_path(SCRIPT_STARTUP_INI.parent).mkdir(parents=True, exist_ok=True)
    io_path(SCRIPT_STARTUP_INI).write_text(startup_text, encoding="utf-8")
    compile_payload = (
        {"status": "not_attempted_materialize_only"}
        if materialize_only
        else mql5_compile.compile_mql5_ea(metaeditor_path, PORTABLE_SCRIPT, MT5_DIR / "shifted_custom_symbol_seed_compile.log")
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
        "effect": "custom symbol seed(커스텀 심볼 심기)를 준비해 Strategy Tester(전략 테스터) 가시성 경계를 분리한다.",
    }


def run_shifted_seed(terminal_path: Path, materialize_only: bool) -> dict[str, Any]:
    if materialize_only:
        return {"status": "not_attempted_materialize_only", "output_path": SCRIPT_OUTPUT_COMMON.as_posix()}
    if path_exists(SCRIPT_OUTPUT_COMMON):
        io_path(SCRIPT_OUTPUT_COMMON).unlink()
    before_offsets = qprobe.log_offsets([TERMINAL_LOG])
    process_recovery = qprobe.stop_target_terminal_if_running(terminal_path)
    command = [str(terminal_path), "/portable", f"/config:{io_path(SCRIPT_STARTUP_INI).resolve()}"]
    try:
        proc = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=240)
        run_status = "completed" if proc.returncode == 0 else "terminal_returncode_nonzero_output_checked"
    except subprocess.TimeoutExpired as exc:
        proc = exc
        run_status = "blocked_terminal_startup_timeout"
    deadline = time.monotonic() + 45
    while time.monotonic() < deadline and not path_exists(SCRIPT_OUTPUT_COMMON):
        time.sleep(1.0)
    output_payload: dict[str, Any] = {"status": "missing"}
    if path_exists(SCRIPT_OUTPUT_COMMON):
        output_payload = json.loads(io_path(SCRIPT_OUTPUT_COMMON).read_text(encoding="utf-8-sig"))
        local_output = RUN_DIR / "shifted_custom_symbol_seed_status.json"
        io_path(local_output.parent).mkdir(parents=True, exist_ok=True)
        shutil.copy2(io_path(SCRIPT_OUTPUT_COMMON), io_path(local_output))
        output_payload["repo_copy_path"] = rel(local_output)
        output_payload["repo_copy_sha256"] = sha256_file(local_output)
        if output_payload.get("status") == "completed":
            run_status = "completed_by_script_output"
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


def next_day_audit(feature_rows: Sequence[Mapping[str, Any]], broker_api: Mapping[str, Any]) -> list[dict[str, Any]]:
    broker_feature = next((row for row in feature_rows if "broker" in str(row.get("attempt_name", ""))), {})
    feature_last = pd.to_datetime(str(broker_feature.get("feature_last_timestamp", "")), errors="coerce", utc=True)
    latest = pd.to_datetime(str(broker_api.get("m5_last_close_utc", "")), errors="coerce", utc=True)
    now = datetime.now(tz=UTC)
    due = False if pd.isna(feature_last) else now.date() > feature_last.date()
    return [
        {
            "audit_id": "next_day_rollover_due_check",
            "now_utc": now.replace(microsecond=0).isoformat().replace("+00:00", "Z"),
            "feature_last_timestamp": "" if pd.isna(feature_last) else feature_last.isoformat().replace("+00:00", "Z"),
            "broker_api_latest_m5_close": "" if pd.isna(latest) else latest.isoformat().replace("+00:00", "Z"),
            "next_day_rollover_due": due,
            "status": "due_or_past_due" if due else "not_yet_due_same_utc_date",
            "effect": "next-day rollover(다음날 이월) 조건인지 확인한다. 효과: tester gap(테스터 공백)을 날짜 정책 문제와 분리한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def telemetry_timestamps(attempt: Mapping[str, Any], common_files_root: Path) -> dict[str, Any]:
    candidates = [TELEMETRY_DIR / f"{attempt['attempt_name']}_telemetry.csv"]
    if attempt.get("common_telemetry_path"):
        candidates.append(common_files_root / Path(str(attempt["common_telemetry_path"])))
    path = next((candidate for candidate in candidates if path_exists(candidate)), None)
    if path is None:
        return {"status": "missing", "timestamps": [], "telemetry_path": ""}
    frame = pd.read_csv(io_path(path), usecols=lambda column: column in {"record_type", "bar_time"})
    if "record_type" in frame.columns:
        frame = frame.loc[frame["record_type"].astype(str) == "cycle"]
    values = pd.to_datetime(frame["bar_time"].astype(str).str.replace(".", "-", regex=False), errors="coerce", utc=True).dropna()
    keys = values.dt.strftime("%Y-%m-%dT%H:%M:%SZ").tolist()
    return {
        "status": "completed" if keys else "empty",
        "timestamps": keys,
        "telemetry_path": rel(path) if str(path).startswith(str(ROOT)) else path.as_posix(),
        "cycle_rows": int(len(values)),
        "unique_cycle_timestamps": int(len(set(keys))),
        "first_cycle_timestamp": values.min().isoformat().replace("+00:00", "Z") if len(values) else "",
        "last_cycle_timestamp": values.max().isoformat().replace("+00:00", "Z") if len(values) else "",
    }


def feature_timestamp_keys(frame: pd.DataFrame) -> pd.Series:
    timestamps = qprobe.feature_timestamp_series(frame)
    return timestamps.dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def build_exact_timestamp_proxy_rows(
    attempts: Sequence[Mapping[str, Any]],
    runtime_rows: Sequence[Mapping[str, Any]],
    common_files_root: Path,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    window_rows: list[dict[str, Any]] = []
    runtime_by = {str(row.get("attempt_name")): row for row in runtime_rows}
    for attempt in attempts:
        attempt_name = str(attempt["attempt_name"])
        telemetry = telemetry_timestamps(attempt, common_files_root)
        set_values = base.parse_key_value_file(ROOT / str(attempt["set"]["path"]))
        feature_path = ROOT / str(attempt["feature_local_path"])
        model_path = ROOT / str(attempt["model_local_path"])
        feature_count = base.parse_int(set_values.get("InpFeatureCount"))
        frame_full = pd.read_csv(io_path(feature_path))
        feature_keys = feature_timestamp_keys(frame_full)
        telemetry_set = set(telemetry.get("timestamps", []))
        exact_mask = feature_keys.isin(telemetry_set)
        exact_frame = frame_full.loc[exact_mask].copy()
        first_ts = pd.to_datetime(telemetry.get("first_cycle_timestamp", ""), errors="coerce", utc=True)
        last_ts = pd.to_datetime(telemetry.get("last_cycle_timestamp", ""), errors="coerce", utc=True)
        feature_ts = qprobe.feature_timestamp_series(frame_full)
        if pd.isna(first_ts) or pd.isna(last_ts):
            continuous_rows = 0
        else:
            continuous_rows = int(((feature_ts >= first_ts) & (feature_ts <= last_ts)).sum())
        missing = len(telemetry_set - set(feature_keys.dropna()))
        window_rows.append(
            {
                "attempt_name": attempt_name,
                "artifact_slug": attempt.get("artifact_slug", ""),
                "tester_symbol": attempt.get("tester_symbol", ""),
                "telemetry_status": telemetry.get("status", ""),
                "telemetry_path": telemetry.get("telemetry_path", ""),
                "telemetry_cycle_rows": telemetry.get("cycle_rows", 0),
                "telemetry_unique_timestamps": telemetry.get("unique_cycle_timestamps", 0),
                "first_cycle_timestamp": telemetry.get("first_cycle_timestamp", ""),
                "last_cycle_timestamp": telemetry.get("last_cycle_timestamp", ""),
                "full_feature_rows": int(len(frame_full)),
                "continuous_window_feature_rows": continuous_rows,
                "exact_cycle_feature_rows": int(len(exact_frame)),
                "continuous_minus_exact_rows": continuous_rows - int(len(exact_frame)),
                "missing_feature_timestamps_for_telemetry": int(missing),
                "runtime_feature_ready_count": runtime_by.get(attempt_name, {}).get("feature_ready_count", ""),
                "effect": "continuous window(연속 창)과 exact tester cycle(정확 테스터 사이클)을 분리해 과대계산을 찾는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        if telemetry.get("status") != "completed":
            rows.append(
                {
                    "attempt_name": attempt_name,
                    "artifact_slug": attempt.get("artifact_slug", ""),
                    "feature_set_id": attempt.get("feature_set_id", ""),
                    "model_id": attempt.get("model_id", ""),
                    "expected_feature_ready_count": None,
                    "expected_model_ok_count": None,
                    "expected_short_count": None,
                    "expected_long_count": None,
                    "expected_flat_count": None,
                    "expected_signal_count": None,
                    "proxy_source": "exact_tester_cycle_timestamp_proxy_unavailable",
                    "proxy_row_scope": "missing_mt5_cycle_telemetry",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            continue
        cols = base.feature_columns(frame_full, feature_count)
        matrix = exact_frame.loc[:, cols].to_numpy(dtype="float64", copy=False)
        probabilities = base.model_probabilities(model_path, matrix) if len(exact_frame) else np.empty((0, 3), dtype="float64")
        rule = base.ThresholdRule(
            threshold_id=f"stage337AK_{attempt_name}_exact_cycle_fixed_min_margin",
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
                "artifact_slug": attempt.get("artifact_slug", ""),
                "feature_set_id": attempt.get("feature_set_id", ""),
                "model_id": attempt.get("model_id", ""),
                "expected_feature_ready_count": int(len(exact_frame)),
                "expected_model_ok_count": int(len(exact_frame)),
                "expected_short_count": short_count,
                "expected_long_count": long_count,
                "expected_flat_count": flat_count,
                "expected_signal_count": signal_count,
                "expected_signal_rate": signal_count / len(exact_frame) if len(exact_frame) else None,
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
                "proxy_source": "exact_tester_cycle_timestamp_python_onnx_inference",
                "proxy_row_scope": "feature_rows_with_timestamp_exactly_seen_in_mt5_cycle_telemetry",
                "proxy_first_cycle_utc": telemetry.get("first_cycle_timestamp", ""),
                "proxy_last_cycle_utc": telemetry.get("last_cycle_timestamp", ""),
                "full_feature_rows": int(len(frame_full)),
                "exact_cycle_feature_rows": int(len(exact_frame)),
                "telemetry_cycle_rows": telemetry.get("cycle_rows", 0),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows, window_rows


def tag_diff_rows(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    tagged: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        item["mt5_source"] = "stage337AK_runtime_summary_exact_tester_cycle"
        item["usable_for_forward_pass_fail"] = False
        item["claim_boundary"] = CLAIM_BOUNDARY
        tagged.append(item)
    return tagged


def runtime_completed(row: Mapping[str, Any]) -> bool:
    return (
        str(row.get("tester_status", "")) == "completed"
        and str(row.get("runtime_status", "")) == "completed"
        and str(row.get("report_status", "")) == "completed"
    )


def classify(
    seed_run: Mapping[str, Any],
    runtime_rows: Sequence[Mapping[str, Any]],
    gap_rows: Sequence[Mapping[str, Any]],
    diff_rows: Sequence[Mapping[str, Any]],
    materialize_only: bool,
) -> tuple[str, str, str, str]:
    if materialize_only:
        return STATUS_MATERIALIZED, JUDGMENT_MATERIALIZED, DECISION_MATERIALIZED, RUN_ID
    seed_ok = str((seed_run.get("script_output") or {}).get("status", "")) == "completed"
    if not seed_ok or not runtime_rows or any(not runtime_completed(row) for row in runtime_rows):
        return STATUS_RUNTIME_ISSUE, JUDGMENT_RUNTIME_ISSUE, DECISION_RUNTIME_ISSUE, NEXT_RUN_ID_REPAIR
    broker_gap = next((row for row in gap_rows if "broker_rollover_control" in str(row.get("attempt_name", ""))), {})
    shifted_gap = next((row for row in gap_rows if "shifted_custom_exact_timestamp" in str(row.get("attempt_name", ""))), {})
    matched = sum(1 for row in diff_rows if str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true")
    if broker_gap.get("gap_status") == "tester_reached_feature_last" and matched == len(diff_rows):
        return STATUS_BROKER_REPAIRED, JUDGMENT_BROKER_REPAIRED, DECISION_BROKER_REPAIRED, NEXT_RUN_ID_BROKER_REPAIRED
    if shifted_gap.get("gap_status") == "tester_reached_feature_last" and matched == len(diff_rows):
        return STATUS_SYNTHETIC_REPAIRED, JUDGMENT_SYNTHETIC_REPAIRED, DECISION_SYNTHETIC_REPAIRED, NEXT_RUN_ID_SYNTHETIC_REPAIRED
    return STATUS_MISMATCH, JUDGMENT_MISMATCH, DECISION_MISMATCH, NEXT_RUN_ID_REPAIR


def proxy_usability_rows(gap_rows: Sequence[Mapping[str, Any]], diff_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for attempt in sorted({str(row.get("attempt_name", "")) for row in diff_rows}):
        subset = [row for row in diff_rows if row.get("attempt_name") == attempt]
        matched = sum(1 for row in subset if str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true")
        gap = next((row for row in gap_rows if row.get("attempt_name") == attempt), {})
        synthetic = "shifted_custom_exact_timestamp" in attempt
        rows.append(
            {
                "attempt_name": attempt,
                "gap_status": gap.get("gap_status", ""),
                "proxy_matched": matched,
                "proxy_total": len(subset),
                "diagnostic_usability": "usable_for_runtime_signal_parity" if matched == len(subset) else "not_usable_until_mismatch_repaired",
                "forward_usability": "not_forward_authority_synthetic_shift" if synthetic else "blocked_until_broker_reaches_feature_last",
                "effect": "proxy(프록시) 사용 범위를 runtime signal parity(런타임 신호 동등성)로 제한한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def gate_rows(
    seed_run: Mapping[str, Any],
    runtime_rows: Sequence[Mapping[str, Any]],
    gap_rows: Sequence[Mapping[str, Any]],
    diff_rows: Sequence[Mapping[str, Any]],
    handoff_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    seed_ok = str((seed_run.get("script_output") or {}).get("status", "")) == "completed"
    runtime_ok = sum(1 for row in runtime_rows if runtime_completed(row))
    matched = sum(1 for row in diff_rows if str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true")
    shifted_gap = next((row for row in gap_rows if "shifted_custom_exact_timestamp" in str(row.get("attempt_name", ""))), {})
    no_retune = all(
        str(row.get("threshold_keys_unchanged", "")).lower() == "true"
        and str(row.get("risk_lot_keys_unchanged", "")).lower() == "true"
        for row in handoff_rows
    )
    return [
        {
            "gate_id": "seed_output_completed",
            "status": "passed" if seed_ok else "failed",
            "evidence_path": rel(RUN_DIR / "shifted_custom_symbol_seed_status.json"),
            "effect": "custom symbol seed(커스텀 심볼 심기)가 완료됐는지 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "mt5_runtime_completed",
            "status": "passed" if runtime_ok == len(runtime_rows) and runtime_rows else "failed",
            "evidence_path": rel(RUN_DIR / "runtime_summary.csv"),
            "effect": "Strategy Tester(전략 테스터)와 runtime telemetry(런타임 기록)가 모두 생겼는지 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "shifted_custom_reached_feature_last",
            "status": "passed" if shifted_gap.get("gap_status") == "tester_reached_feature_last" else "failed",
            "evidence_path": rel(RUN_DIR / "tester_feature_last_gap_exact_timestamp.csv"),
            "effect": "synthetic custom(합성 커스텀)이 feature_last(피처 마지막 시각)에 닿는지 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "exact_timestamp_proxy_mt5_parity",
            "status": "passed" if matched == len(diff_rows) and diff_rows else "failed",
            "evidence_path": rel(RUN_DIR / "exact_timestamp_proxy_mt5_difference.csv"),
            "effect": "MT5 cycle timestamp(MT5 사이클 시각)와 같은 feature row(피처 행)만 비교한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "no_retune_identity_guard",
            "status": "passed" if no_retune else "failed",
            "evidence_path": rel(RUN_DIR / "handoff_attempts.csv"),
            "effect": "threshold/risk/lot(임계값/위험/로트)이 바뀌지 않았는지 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "forward_claim_boundary",
            "status": "passed",
            "evidence_path": rel(RUN_DIR / "final_decision.json"),
            "effect": "Forward Passed/Failed(전진 통과/실패)와 Goal Achieve(목표 달성)를 주장하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def decision_payload(
    status: str,
    judgment: str,
    decision: str,
    next_action: str,
    seed_run: Mapping[str, Any],
    runtime_rows: Sequence[Mapping[str, Any]],
    gap_rows: Sequence[Mapping[str, Any]],
    diff_rows: Sequence[Mapping[str, Any]],
    window_rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    matched = sum(1 for row in diff_rows if str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true")
    broker_gap = next((row for row in gap_rows if "broker_rollover_control" in str(row.get("attempt_name", ""))), {})
    shifted_gap = next((row for row in gap_rows if "shifted_custom_exact_timestamp" in str(row.get("attempt_name", ""))), {})
    shifted_window = next((row for row in window_rows if "shifted_custom_exact_timestamp" in str(row.get("attempt_name", ""))), {})
    return {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "stage_id": STAGE_ID,
        "status": status,
        "judgment": judgment,
        "decision": decision,
        "next_action": next_action,
        "seed_status": (seed_run.get("script_output") or {}).get("status", ""),
        "runtime_completed": sum(1 for row in runtime_rows if runtime_completed(row)),
        "runtime_total": len(runtime_rows),
        "proxy_mt5_matched": matched,
        "proxy_mt5_rows": len(diff_rows),
        "broker_gap_status": broker_gap.get("gap_status", ""),
        "shifted_gap_status": shifted_gap.get("gap_status", ""),
        "shifted_continuous_window_rows": shifted_window.get("continuous_window_feature_rows", ""),
        "shifted_exact_cycle_rows": shifted_window.get("exact_cycle_feature_rows", ""),
        "shifted_continuous_minus_exact_rows": shifted_window.get("continuous_minus_exact_rows", ""),
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def receipt_payloads(final: Mapping[str, Any]) -> dict[Path, Mapping[str, Any]]:
    common = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": final.get("status", ""),
        "judgment": final.get("judgment", ""),
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return {
        RUN_DIR / "data_integrity_receipt.json": {
            **common,
            "receipt_type": "data_integrity",
            "data_source": "US100 broker data plus shifted custom symbol telemetry",
            "time_axis": "UTC bar timestamps; exact MT5 cycle timestamps are used for proxy rows",
            "sample_scope": "u42 technical42 Tier A forward runtime diagnostic; no label or threshold retune",
            "missing_or_duplicate_check": "continuous window and exact cycle counts are separated",
            "feature_label_boundary": "no label is built; frozen feature CSV is replayed",
            "split_boundary": "post-OOS forward diagnostic only",
            "leakage_risk": "synthetic shift cannot become forward KPI authority",
            "integrity_judgment": "usable_with_boundary",
        },
        RUN_DIR / "runtime_parity_receipt.json": {
            **common,
            "receipt_type": "runtime_parity",
            "research_path": rel(Path(__file__)),
            "runtime_path": rel(ROOT / "foundation" / "mt5" / "ObsidianPrimeV2_RuntimeProbeEA.mq5"),
            "shared_contract": "same ONNX, feature order, threshold, risk, lot, ATR SL/TP",
            "known_differences": "shifted custom symbol is synthetic and cannot support forward pass/fail",
            "parity_check": "exact MT5 cycle timestamp proxy versus runtime telemetry summary",
            "runtime_claim_boundary": "runtime_probe_research_only",
            "proxy_mt5_matched": final.get("proxy_mt5_matched", 0),
            "proxy_mt5_rows": final.get("proxy_mt5_rows", 0),
        },
        RUN_DIR / "model_validation_receipt.json": {
            **common,
            "receipt_type": "model_validation",
            "model_family": "frozen u42 ONNX random forest artifact",
            "split_method": "runtime probe only",
            "selection_metric": "not_applicable_no_selection",
            "threshold_policy": "fixed_existing_threshold_no_search",
            "overfit_risk": "tester-boundary repair could be mistaken for robustness if synthetic shift is overclaimed",
            "validation_judgment": "inconclusive_runtime_boundary",
        },
        RUN_DIR / "result_judgment_receipt.json": {
            **common,
            "receipt_type": "result_judgment",
            "result_subject": RUN_ID,
            "evidence_available": "MT5 reports, telemetry, exact timestamp proxy, seed output",
            "evidence_missing": "broker tester still must reach latest feature_last for true forward decision",
            "judgment_label": "runtime_probe",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": "broker-side tester reaches feature_last or data/runtime repair continues",
        },
    }


def report_text(final: Mapping[str, Any], api_rows: Sequence[Mapping[str, Any]], gap_rows: Sequence[Mapping[str, Any]], window_rows: Sequence[Mapping[str, Any]], usability: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "# Stage337AK Synthetic Custom Exact Timestamp Parity Repair(337AK 합성 커스텀 정확 시각 동등성 수리)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- status(상태): `{final['status']}`",
        f"- judgment(판정): `{final['judgment']}`",
        f"- decision(결정): `{final['decision']}`",
        f"- next_action(다음 행동): `{final['next_action']}`",
        f"- seed_status(심기 상태): `{final['seed_status']}`",
        f"- runtime completed(런타임 완료): `{final['runtime_completed']}/{final['runtime_total']}`",
        f"- exact proxy parity(정확 프록시 동등성): `{final['proxy_mt5_matched']}/{final['proxy_mt5_rows']}`",
        f"- broker gap(브로커 공백): `{final['broker_gap_status']}`",
        f"- shifted custom gap(이동 커스텀 공백): `{final['shifted_gap_status']}`",
        "- Forward Passed(전진 통과): `not_claimed`",
        "- Forward Failed(전진 실패): `not_claimed`",
        "- runtime authority(런타임 권위): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Meaning(의미)",
        "",
        "run337AK(337AK 실행)는 새 후보 개발이 아니다. MT5 cycle timestamp(MT5 사이클 시각)와 정확히 같은 feature row(피처 행)만 Python ONNX proxy(파이썬 온엑스 프록시)에 넣어, run337AC mismatch(불일치)가 continuous window overcount(연속 창 과대계산)인지 확인한다.",
        "",
        "Effect(효과): shifted custom(이동 커스텀)이 맞아도 synthetic diagnostic(합성 진단)일 뿐이며, broker forward decision(브로커 전진 판정)이나 Goal Achieve(목표 달성)는 열지 않는다.",
        "",
        "## API Visibility(API 가시성)",
        "",
        "| symbol(심볼) | status(상태) | custom(커스텀) | m5 last close(M5 마지막 종가 시각) |",
        "|---|---|---:|---:|",
    ]
    for row in api_rows:
        lines.append(f"| `{row.get('symbol', '')}` | `{row.get('status', '')}` | `{row.get('symbol_custom', '')}` | `{row.get('m5_last_close_utc', '')}` |")
    lines.extend(
        [
            "",
            "## Tester Gap(테스터 공백)",
            "",
            "| attempt(시도) | symbol(심볼) | feature last(피처 마지막) | tester last(테스터 마지막) | gap status(공백 상태) |",
            "|---|---|---:|---:|---|",
        ]
    )
    for row in gap_rows:
        lines.append(
            f"| `{row.get('attempt_name', '')}` | `{row.get('tester_symbol', '')}` | `{row.get('feature_last_timestamp', '')}` | `{row.get('tester_last_observed_bar_time', '')}` | `{row.get('gap_status', '')}` |"
        )
    lines.extend(
        [
            "",
            "## Exact Timestamp Scope(정확 시각 범위)",
            "",
            "| attempt(시도) | telemetry rows(기록 행) | continuous rows(연속 창 행) | exact rows(정확 행) | overcount(과대계산) |",
            "|---|---:|---:|---:|---:|",
        ]
    )
    for row in window_rows:
        lines.append(
            f"| `{row.get('attempt_name', '')}` | `{row.get('telemetry_cycle_rows', '')}` | `{row.get('continuous_window_feature_rows', '')}` | `{row.get('exact_cycle_feature_rows', '')}` | `{row.get('continuous_minus_exact_rows', '')}` |"
        )
    lines.extend(
        [
            "",
            "## Usability(사용 가능 범위)",
            "",
            "| attempt(시도) | proxy matched(프록시 일치) | diagnostic usability(진단 사용성) | forward usability(전진 사용성) |",
            "|---|---:|---|---|",
        ]
    )
    for row in usability:
        lines.append(
            f"| `{row.get('attempt_name', '')}` | `{row.get('proxy_matched', '')}/{row.get('proxy_total', '')}` | `{row.get('diagnostic_usability', '')}` | `{row.get('forward_usability', '')}` |"
        )
    return "\n".join(lines)


def decision_doc_text(final: Mapping[str, Any]) -> str:
    return f"""# 2026-05-27 Stage337AK Synthetic Custom Exact Timestamp Parity Decision(337AK 합성 커스텀 정확 시각 동등성 결정)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Effect(효과): exact tester cycle timestamp(정확 테스터 사이클 시각) 기준으로 proxy/MT5 parity(프록시/MT5 동등성)를 다시 판정한다. 이 결과는 runtime diagnostic(런타임 진단)이며 broker forward pass/fail(브로커 전진 통과/실패)이 아니다.
"""


def replace_line(text: str, prefix: str, replacement: str) -> str:
    pattern = re.compile(rf"^{re.escape(prefix)}.*$", flags=re.M)
    if pattern.search(text):
        return pattern.sub(replacement, text, count=1)
    return replacement + "\n" + text


def remove_duplicate_current_focus_sections(text: str) -> str:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    matches = list(re.finditer(r"(?m)^current_focus:\s*$", normalized))
    if not matches:
        return text
    if len(matches) > 1:
        normalized = normalized[: matches[1].start()].rstrip() + "\n"
    return normalized


def upsert_focus_block(text: str, focus: str) -> str:
    text = remove_duplicate_current_focus_sections(text)
    block = f"- >-\n  {focus}\n"
    if "current_focus:\n" not in text:
        return text.rstrip() + "\ncurrent_focus:\n" + block
    if "Stage337 run337AK focus complete" in text:
        return re.sub(r"- >-\n  Stage337 run337AK focus complete:.*?(?=\n- >-|\Z)", block.rstrip(), text, count=1, flags=re.S)
    return text.replace("current_focus:\n", "current_focus:\n" + block, 1)


def update_status_docs(final: Mapping[str, Any]) -> list[Path]:
    changed: list[Path] = []
    selected_text = f"""# Stage337 Selection Status(337단계 선택 상태)

- stage_id(단계 ID): `{STAGE_ID}`
- stage_status(단계 상태): `open_active`
- selected_candidate(선택 후보): `none`
- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{final['next_action']}`
- broker_gap_status(브로커 공백 상태): `{final['broker_gap_status']}`
- shifted_custom_gap_status(이동 커스텀 공백 상태): `{final['shifted_gap_status']}`
- exact_proxy_parity(정확 프록시 동등성): `{final['proxy_mt5_matched']}/{final['proxy_mt5_rows']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Forward Blocked(전진 차단): `broker_forward_data_boundary_unresolved`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): run337AK(337AK 실행)는 exact timestamp proxy(정확 시각 프록시)로 synthetic custom parity(합성 커스텀 동등성)를 수리했는지 확인하며, 전진 판정은 아직 주장하지 않는다.
"""
    changed.append(write_md(SELECTED_STATUS, selected_text))
    focus = (
        f"Stage337 run337AK focus complete: run337AK(337AK 실행)는 `{final['status']}`로 "
        f"synthetic custom exact timestamp parity repair(합성 커스텀 정확 시각 동등성 수리)를 완료했다. "
        f"Effect(효과): seed(심기) `{final['seed_status']}`, broker gap(브로커 공백) `{final['broker_gap_status']}`, "
        f"shifted gap(이동 공백) `{final['shifted_gap_status']}`, exact proxy/MT5 parity(정확 프록시/MT5 동등성) "
        f"`{final['proxy_mt5_matched']}/{final['proxy_mt5_rows']}`이며 Forward/Goal(전진/목표)은 주장하지 않는다."
    )
    if path_exists(WORKSPACE_STATE):
        text, bom = read_text(WORKSPACE_STATE)
        text = replace_line(text, "current_run_id:", f"current_run_id: {final['next_action']}")
        text = replace_line(text, "updated_on:", f"updated_on: '{TODAY}'")
        text = upsert_focus_block(text, focus)
        changed.append(write_text(WORKSPACE_STATE, text, bom))
    if path_exists(CURRENT_STATE):
        text, bom = read_text(CURRENT_STATE)
        entry = f"""## Stage337 run337AK(337AK 실행) - {TODAY}

- status(상태): `{final['status']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): exact tester cycle timestamp(정확 테스터 사이클 시각) 기준으로 proxy/MT5 parity(프록시/MT5 동등성)를 `{final['proxy_mt5_matched']}/{final['proxy_mt5_rows']}`까지 확인했다. Broker forward decision(브로커 전진 판정), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.
"""
        if "## Stage337 run337AK(337AK 실행)" in text:
            text = re.sub(r"## Stage337 run337AK\(337AK 실행\).*?(?=\n## |\Z)", entry.strip(), text, count=1, flags=re.S)
        else:
            text = text.rstrip() + "\n\n" + entry.strip() + "\n"
        changed.append(write_text(CURRENT_STATE, text, bom))
    if path_exists(CHANGELOG):
        text, bom = read_text(CHANGELOG)
        line = (
            f"- {TODAY}: Stage337 run337AK(337AK 실행) `{final['status']}`. "
            f"Effect(효과): exact timestamp proxy(정확 시각 프록시) `{final['proxy_mt5_matched']}/{final['proxy_mt5_rows']}`를 기록하고 Forward/Goal(전진/목표)은 주장하지 않음."
        )
        if "Stage337 run337AK(337AK 실행)" not in text:
            text = text.rstrip() + "\n" + line + "\n"
        changed.append(write_text(CHANGELOG, text, bom))
    if path_exists(STAGE_BRIEF):
        text, bom = read_text(STAGE_BRIEF)
        text = re.sub(r"- latest_run\([^)]*\): `[^`]*`", f"- latest_run(최신 실행): `{RUN_ID}`", text, count=1)
        summary = (
            f"- run337AK_summary(337AK 요약): `{final['status']}`. "
            f"Effect(효과): exact proxy/MT5 parity(정확 프록시/MT5 동등성) `{final['proxy_mt5_matched']}/{final['proxy_mt5_rows']}`, "
            f"broker gap(브로커 공백) `{final['broker_gap_status']}`, shifted gap(이동 공백) `{final['shifted_gap_status']}`.\n"
        )
        if "run337AK_summary(337AK 요약)" in text:
            text = re.sub(r"- run337AK_summary\(337AK 요약\): [^\n]*(?:\n|$)", summary, text, count=1)
        else:
            text = text.rstrip() + "\n" + summary
        changed.append(write_text(STAGE_BRIEF, text, bom))
    return changed


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "synthetic_custom_exact_timestamp_parity_repair",
        "family": "runtime_parity_repair",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_report": rel(REPORT_PATH),
        "notes": f"decision={final['decision']};next_action={final['next_action']};goal_achieve_not_claimed.",
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__synthetic_custom_exact_timestamp_parity_repair",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "synthetic_custom_exact_timestamp_parity_repair",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "runtime_boundary_parity_repair",
        "tier_scope": "Tier A u42 runtime diagnostic(티어 A u42 런타임 진단)",
        "kpi_scope": "diagnostic_runtime_probe_no_selection(진단 런타임 탐침, 선택 없음)",
        "scoreboard_lane": "runtime_parity_repair",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"exact_proxy_mt5={final['proxy_mt5_matched']}/{final['proxy_mt5_rows']};broker_gap={final['broker_gap_status']};shifted_gap={final['shifted_gap_status']}",
        "guardrail_kpi": "no_training;no_threshold_retune;no_lot_opt;synthetic_shift_not_forward_authority",
        "external_verification_status": "mt5_strategy_tester_attempted",
        "notes": f"decision={final['decision']};next_action={final['next_action']};goal_achieve_not_claimed.",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__synthetic_custom_exact_timestamp_parity_repair",
        "run_key": f"{RUN_ID}__synthetic_custom_exact_timestamp_parity_repair",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "runtime_parity_repair",
        "family": "synthetic_custom_exact_timestamp_parity_repair",
        "question": "does exact tester-cycle timestamp proxy repair the shifted custom MT5 mismatch",
        "evidence_scope": "MT5 custom symbol seed, tester reports, telemetry, exact timestamp proxy",
        "metric_scope": "runtime_signal_parity_no_forward_decision",
        "status": final["status"],
        "judgment": final["judgment"],
        "decision": final["decision"],
        "next_action": final["next_action"],
        "path": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "primary_artifact": rel(REPORT_PATH),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return [
        upsert_csv(RUN_REGISTRY, ["run_id"], run_row),
        upsert_csv(ALPHA_LEDGER, ["ledger_row_id"], alpha_row),
        upsert_csv(STAGE_LEDGER, ["run_key"], stage_row),
    ]


def append_artifacts(paths: Sequence[Path], final: Mapping[str, Any]) -> Path:
    rows = read_csv(ARTIFACT_REGISTRY)
    columns = list(rows[0].keys()) if rows else [
        "artifact_id",
        "artifact_type",
        "path",
        "sha256",
        "stage_id",
        "run_id",
        "created_at_utc",
        "notes",
        "artifact_path",
        "claim_boundary",
    ]
    for column in ("artifact_id", "artifact_type", "path", "artifact_path", "sha256", "stage_id", "run_id", "created_at_utc", "notes", "claim_boundary"):
        if column not in columns:
            columns.append(column)
    rows = [row for row in rows if row.get("run_id") != RUN_ID]
    generated = now_utc()
    seen: set[str] = set()
    for path in paths:
        if not path_exists(path) or not io_path(path).is_file():
            continue
        relative = rel(path)
        if relative in seen:
            continue
        seen.add(relative)
        suffix = path.suffix.lower()
        digest = sha256_file_lf_normalized(path) if suffix in {".csv", ".json", ".md", ".txt", ".py", ".yaml", ".ini", ".set"} else sha256_file(path)
        rows.append(
            {
                "artifact_id": f"{RUN_ID}::{relative}",
                "artifact_type": suffix.lstrip(".") or "file",
                "path": relative,
                "artifact_path": relative,
                "sha256": digest,
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": generated,
                "notes": final.get("status", ""),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return write_csv(ARTIFACT_REGISTRY, columns, rows)


def main() -> int:
    args = parse_args()
    configure_probe_modules()
    terminal_path = Path(args.terminal)
    metaeditor_path = Path(args.metaeditor)
    common_files_root = Path(args.common_files_root)
    tester_profile_root = Path(args.tester_profile_root)
    terminal_data_root = Path(args.terminal_data_root)

    for directory in (RUN_DIR, MT5_DIR, FEATURE_COPY_DIR, MODEL_COPY_DIR, TELEMETRY_DIR, SEED_INPUT_DIR):
        io_path(directory).mkdir(parents=True, exist_ok=True)

    source = load_source_u42()
    source_feature = ROOT / str(source.get("feature_local_path", ""))
    shifted_feature = shift_feature_csv(source_feature, SEED_INPUT_DIR / "u42_plain_shift_minus_1440m_features.csv", SHIFT_MINUTES)
    shift_contract = {
        "run_id": RUN_ID,
        "source_feature_path": rel(source_feature),
        "shifted_feature_path": rel(shifted_feature),
        "shift_minutes": SHIFT_MINUTES,
        "diagnostic_only": True,
        "effect": "feature timestamps(피처 시각)만 이동해 tester boundary(테스터 경계)를 분리한다.",
        "claim_boundary": CLAIM_BOUNDARY,
    }

    seed_prepare = prepare_shifted_seed(terminal_path, metaeditor_path, args.materialize_only)
    seed_run = run_shifted_seed(terminal_path, args.materialize_only)
    broker_api = ab.mt5_api_symbol_visibility(terminal_path, ORIGIN_SYMBOL)
    shifted_api = ab.mt5_api_symbol_visibility(terminal_path, SHIFTED_CUSTOM_SYMBOL)
    api_rows = [broker_api, shifted_api]
    pre_tester_recovery = qprobe.stop_target_terminal_if_running(terminal_path)

    prepared = build_source_attempts(source, shifted_feature)
    prepared_feature_rows = qprobe.feature_last_rows(prepared)
    next_day_rows = next_day_audit(prepared_feature_rows, broker_api)
    attempts, handoff_rows, materialized_artifacts = base.build_attempts(prepared, common_files_root)
    scenario_by_attempt = {str(row["attempt_name"]): row for row in prepared}
    for attempt in attempts:
        scenario = scenario_by_attempt.get(str(attempt["attempt_name"]), {})
        for key in ("scenario_id", "scenario_symbol", "scenario_from_date", "scenario_to_date", "scenario_model", "scenario_role"):
            attempt[key] = scenario.get(key, "")
    attempts = [rewrite_attempt_to_scenario(dict(attempt)) for attempt in attempts]

    before_offsets = qprobe.log_offsets([TESTER_LOG, TESTER_AGENT_LOG, TERMINAL_LOG])
    if args.materialize_only:
        execution_result: dict[str, Any] = {
            "compile": {"status": "not_attempted_materialize_only"},
            "execution_results": [],
            "strategy_tester_reports": [],
            "materialize_only": True,
        }
    else:
        execution_result = base.execute_attempts(
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
    runtime_rows = base.build_fresh_runtime_summary(attempts, execution_result)
    copied_runtime_artifacts = base.copy_runtime_outputs(common_files_root, attempts)
    feature_rows = qprobe.feature_last_rows(attempts)
    gap_rows = qprobe.tester_gap_rows(runtime_rows, feature_rows, common_files_root, {"last_close_utc": broker_api.get("m5_last_close_utc", "")})
    boundary_rows = ab.parse_tester_boundary_rows(before_offsets, attempts)
    boundary_by_attempt = {row["attempt_name"]: row for row in boundary_rows}
    for row in gap_rows:
        boundary = boundary_by_attempt.get(row.get("attempt_name"), {})
        row["scenario_id"] = boundary.get("scenario_id", "")
        row["tester_symbol"] = boundary.get("tester_symbol", "")
        row["tester_model"] = next((attempt.get("tester_model", "") for attempt in attempts if attempt.get("attempt_name") == row.get("attempt_name")), "")

    exact_proxy_rows, window_rows = build_exact_timestamp_proxy_rows(attempts, runtime_rows, common_files_root)
    diff_rows = tag_diff_rows(base.build_signal_difference_rows(exact_proxy_rows, runtime_rows))
    usability = proxy_usability_rows(gap_rows, diff_rows)
    status, judgment, decision, next_action = classify(seed_run, runtime_rows, gap_rows, diff_rows, args.materialize_only)
    final = decision_payload(status, judgment, decision, next_action, seed_run, runtime_rows, gap_rows, diff_rows, window_rows)
    gates = gate_rows(seed_run, runtime_rows, gap_rows, diff_rows, handoff_rows)

    artifacts: list[Path] = [
        write_json(RUN_DIR / "timestamp_shift_contract.json", shift_contract),
        write_json(RUN_DIR / "shifted_custom_symbol_seed_prepare.json", seed_prepare),
        write_json(RUN_DIR / "shifted_custom_symbol_seed_run.json", seed_run),
        write_json(RUN_DIR / "pre_tester_terminal_recovery.json", pre_tester_recovery),
        write_json(RUN_DIR / "execution_result.json", execution_result),
        write_json(RUN_DIR / "final_decision.json", final),
        write_csv(RUN_DIR / "custom_symbol_api_visibility.csv", columns_for(api_rows, ["symbol"]), api_rows),
        write_csv(RUN_DIR / "next_day_rollover_audit.csv", columns_for(next_day_rows, ["audit_id"]), next_day_rows),
        write_csv(RUN_DIR / "handoff_attempts.csv", columns_for(handoff_rows, ["attempt_name"]), handoff_rows),
        write_json(RUN_DIR / "handoff_attempts.json", attempts),
        write_csv(RUN_DIR / "runtime_summary.csv", columns_for(runtime_rows, ["attempt_name"]), runtime_rows),
        write_csv(RUN_DIR / "feature_last_timestamp_audit.csv", columns_for(feature_rows, ["attempt_name"]), feature_rows),
        write_csv(RUN_DIR / "tester_boundary_exact_timestamp.csv", columns_for(boundary_rows, ["attempt_name"]), boundary_rows),
        write_csv(RUN_DIR / "tester_feature_last_gap_exact_timestamp.csv", columns_for(gap_rows, ["attempt_name"]), gap_rows),
        write_csv(RUN_DIR / "exact_timestamp_proxy_scope.csv", columns_for(window_rows, ["attempt_name"]), window_rows),
        write_csv(RUN_DIR / "exact_timestamp_proxy_expected_result.csv", columns_for(exact_proxy_rows, ["attempt_name"]), exact_proxy_rows),
        write_csv(RUN_DIR / "exact_timestamp_proxy_mt5_difference.csv", columns_for(diff_rows, ["attempt_name"]), diff_rows),
        write_csv(RUN_DIR / "proxy_usability_exact_timestamp.csv", columns_for(usability, ["attempt_name"]), usability),
        write_csv(RUN_DIR / "required_gate_coverage_audit.csv", columns_for(gates, ["gate_id"]), gates),
        write_md(REPORT_PATH, report_text(final, api_rows, gap_rows, window_rows, usability)),
        write_md(DECISION_DOC, decision_doc_text(final)),
        shifted_feature,
        *materialized_artifacts,
        *copied_runtime_artifacts,
    ]
    if path_exists(RUN_DIR / "shifted_custom_symbol_seed_status.json"):
        artifacts.append(RUN_DIR / "shifted_custom_symbol_seed_status.json")
    for path, payload in receipt_payloads(final).items():
        artifacts.append(write_json(path, payload))
    artifacts.extend(update_status_docs(final))
    artifacts.extend(update_registers(final))
    manifest = write_json(
        RUN_DIR / "run_manifest.json",
        {
            **final,
            "generated_at_utc": now_utc(),
            "command": "python stage_pipelines/stage337/reprobe_next_rollover_or_synthetic_custom_parity_repair.py",
            "materialize_only": bool(args.materialize_only),
            "primary_family": "runtime_parity_repair",
            "primary_skill": "obsidian-runtime-parity",
            "support_skills": ["obsidian-data-integrity", "obsidian-model-validation", "obsidian-result-judgment"],
            "artifacts": [rel(path) for path in artifacts if path_exists(path)],
        },
    )
    artifacts.append(manifest)
    artifacts.append(append_artifacts([*artifacts, Path(__file__)], final))
    print(json.dumps(final, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
