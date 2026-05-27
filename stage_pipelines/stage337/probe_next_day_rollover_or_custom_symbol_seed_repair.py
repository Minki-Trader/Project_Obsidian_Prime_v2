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
from typing import Any, Mapping, Sequence

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, path_exists  # noqa: E402
from foundation.mt5 import mql5_compile  # noqa: E402
from foundation.mt5.runtime_artifacts import sha256_file  # noqa: E402
from stage_pipelines.stage335 import independent_proxy_mt5_probe as base  # noqa: E402
from stage_pipelines.stage337 import probe_custom_symbol_intraday_tester_visibility as ab  # noqa: E402
from stage_pipelines.stage337 import probe_tester_history_cache_session_policy as aa  # noqa: E402
from stage_pipelines.stage337 import review_runtime_data_and_feature_source_repair_probe as qprobe  # noqa: E402


TODAY = "2026-05-27"
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
RUN_NUMBER = "run337AC"
RUN_ID = "run337AC_next_day_broker_rollover_or_custom_symbol_seed_repair_v1"
PARENT_RUN_ID = "run337AB_custom_symbol_intraday_tester_visibility_probe_v1"
NEXT_RUN_ID_BOUNDARY_REPAIRED = "run337AD_frozen_forward_attribution_after_tester_boundary_repair_v1"
NEXT_RUN_ID_COMPLETED_DAY = "run337AD_completed_day_forward_slice_or_next_day_rollover_confirm_v1"
NEXT_RUN_ID_REPAIR = "run337AD_custom_symbol_seed_or_tester_policy_repair_v1"
CLAIM_BOUNDARY = (
    "research_development_only_stage337AC_next_day_rollover_or_custom_symbol_seed_repair_no_model_training_"
    "no_threshold_retuning_no_lot_optimization_no_candidate_selection_no_forward_passed_no_forward_failed_"
    "no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STATUS_BOUNDARY_REPAIRED = "completed_stage337AC_broker_rollover_reached_feature_last_no_forward_decision"
STATUS_SHIFT_CONFIRMED = "completed_stage337AC_shifted_custom_seed_repair_confirms_current_day_tester_policy_no_forward_decision"
STATUS_PARTIAL = "completed_stage337AC_seed_repair_probe_inconclusive_no_forward_decision"
STATUS_MATERIALIZED = "completed_stage337AC_materialized_only_no_forward_decision"
JUDGMENT_BOUNDARY_REPAIRED = "broker_next_day_rollover_reaches_feature_last_runtime_forward_attribution_can_resume"
JUDGMENT_SHIFT_CONFIRMED = "shifted_custom_symbol_reaches_feature_last_while_broker_current_day_gap_remains"
JUDGMENT_PARTIAL = "custom_symbol_seed_repair_not_sufficient_or_runtime_outputs_incomplete"
JUDGMENT_MATERIALIZED = "run337AC_inputs_materialized_execution_pending"
DECISION_BOUNDARY_REPAIRED = "stage337AC_open_run337AD_frozen_forward_attribution_after_boundary_repair_no_selection"
DECISION_SHIFT_CONFIRMED = "stage337AC_open_run337AD_completed_day_forward_slice_or_next_day_rollover_confirm_no_selection"
DECISION_PARTIAL = "stage337AC_open_run337AD_custom_symbol_seed_or_tester_policy_repair_no_selection"
DECISION_MATERIALIZED = "stage337AC_execution_pending_no_selection"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
PARENT_RUN_DIR = STAGE_DIR / "02_runs" / "run337AB"
RUN337Z_DIR = STAGE_DIR / "02_runs" / "run337Z"
RUN337Z_ATTEMPTS = RUN337Z_DIR / "rollover_reprobe_handoff_attempts.json"
MT5_DIR = RUN_DIR / "mt5"
FEATURE_COPY_DIR = RUN_DIR / "feature_matrices"
MODEL_COPY_DIR = RUN_DIR / "models"
TELEMETRY_DIR = RUN_DIR / "runtime_telemetry"
SEED_INPUT_DIR = RUN_DIR / "seed_repair_inputs"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEWS_DIR / "run337AC_next_day_or_seed_repair.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage337AC_next_day_or_seed_repair.md"
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

COMMON_ROOT = "Project_Obsidian_Prime_v2/stage337/run337AC_next_day_or_seed_repair"
ORIGIN_SYMBOL = "US100"
SHIFTED_CUSTOM_SYMBOL = "US100.OPV337ACM"
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
SCRIPT_PRESET_NAME = "opv2_run337AC_shifted_custom_symbol_seed.set"
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
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
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
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    tmp = io_path(path).with_name(io_path(path).name + ".tmp")
    with tmp.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column, "")) for column in columns})
    os.replace(tmp, io_path(path))
    return path


def write_json(path: Path, payload: Any) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def write_md(path: Path, text: str) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")
    return path


def configure_probe_modules() -> None:
    ab.TODAY = TODAY
    ab.STAGE_ID = STAGE_ID
    ab.RUN_NUMBER = RUN_NUMBER
    ab.RUN_ID = RUN_ID
    ab.PARENT_RUN_ID = PARENT_RUN_ID
    ab.NEXT_RUN_ID_SUCCESS = NEXT_RUN_ID_BOUNDARY_REPAIRED
    ab.NEXT_RUN_ID_REPAIR = NEXT_RUN_ID_REPAIR
    ab.CLAIM_BOUNDARY = CLAIM_BOUNDARY
    ab.RUN_DIR = RUN_DIR
    ab.MT5_DIR = MT5_DIR
    ab.FEATURE_COPY_DIR = FEATURE_COPY_DIR
    ab.MODEL_COPY_DIR = MODEL_COPY_DIR
    ab.TELEMETRY_DIR = TELEMETRY_DIR
    ab.REPORT_PATH = REPORT_PATH
    ab.DECISION_DOC = DECISION_DOC
    ab.TESTER_LOG = TESTER_LOG
    ab.TESTER_AGENT_LOG = TESTER_AGENT_LOG
    ab.TERMINAL_LOG = TERMINAL_LOG
    ab.COMMON_ROOT = COMMON_ROOT
    ab.configure_probe_modules()
    qprobe.CLAIM_BOUNDARY = CLAIM_BOUNDARY
    base.CLAIM_BOUNDARY = CLAIM_BOUNDARY
    base.RUN_ID = RUN_ID
    base.RUN_DIR = RUN_DIR
    base.MT5_DIR = MT5_DIR
    base.FEATURE_COPY_DIR = FEATURE_COPY_DIR
    base.MODEL_COPY_DIR = MODEL_COPY_DIR
    base.TELEMETRY_DIR = TELEMETRY_DIR
    base.COMMON_ROOT = COMMON_ROOT


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stage337AC next-day rollover or shifted custom-symbol seed repair probe.")
    parser.add_argument("--terminal", default=str(DEFAULT_TERMINAL))
    parser.add_argument("--metaeditor", default=str(DEFAULT_METAEDITOR))
    parser.add_argument("--common-files-root", default=str(DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-data-root", default=str(DEFAULT_TERMINAL_DATA_ROOT))
    parser.add_argument("--timeout-seconds", type=int, default=1200)
    parser.add_argument("--wait-timeout-seconds", type=int, default=240)
    parser.add_argument("--materialize-only", action="store_true")
    return parser.parse_args()


def load_source_u42() -> dict[str, Any]:
    rows = ab.read_json(RUN337Z_ATTEMPTS)
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
            "suffix": "ac_broker_rollover_control",
            "scenario_id": "broker_current_day_rollover_control",
            "symbol": ORIGIN_SYMBOL,
            "feature_path": source.get("feature_local_path", ""),
            "from_date": BROKER_FROM_DATE,
            "to_date": BROKER_TO_DATE,
            "model": "4",
            "role": "broker control keeps original timestamps and real-tick model",
        },
        {
            "suffix": "ac_shifted_custom_mirror",
            "scenario_id": "custom_symbol_shift_minus_1440m_seed_repair",
            "symbol": SHIFTED_CUSTOM_SYMBOL,
            "feature_path": rel(shifted_feature_path),
            "from_date": SHIFTED_FROM_DATE,
            "to_date": SHIFTED_TO_DATE,
            "model": "0",
            "role": "synthetic time-shift diagnostic only; no forward KPI authority",
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
        copied["attempt_role"] = "stage337AC_next_day_rollover_or_custom_symbol_seed_repair_same_frozen_u42_model_threshold_risk"
        copied["record_view_prefix"] = f"mt5_stage337AC_u42_plain_{index}"
        selected.append(copied)
    return selected


def rewrite_attempt_to_scenario(attempt: dict[str, Any]) -> dict[str, Any]:
    tester = dict(attempt["ini"]["tester"])
    tester["Symbol"] = attempt["scenario_symbol"]
    tester["FromDate"] = attempt["scenario_from_date"]
    tester["ToDate"] = attempt["scenario_to_date"]
    tester["Model"] = attempt["scenario_model"]
    tester["Report"] = f"Project_Obsidian_Prime_v2_{RUN_ID}_{attempt['attempt_name']}"
    ini_path = Path(str(attempt["ini"]["path"]))
    attempt["ini"] = base.materialize_ini_file(tester, ini_path)
    attempt["from_date"] = tester["FromDate"]
    attempt["to_date"] = tester["ToDate"]
    attempt["tester_symbol"] = tester["Symbol"]
    attempt["tester_model"] = tester.get("Model", "")
    attempt["attempt_role"] = "stage337AC_runtime_boundary_seed_repair_probe_same_frozen_u42_model_threshold_risk"
    attempt["record_view_prefix"] = f"mt5_stage337AC_{attempt['artifact_slug']}"
    attempt["source_run_id"] = PARENT_RUN_ID
    attempt["repair_contract"] = (
        "broker control keeps original timestamps; shifted custom mirror shifts symbol bars and feature timestamps by -1440 minutes "
        "only to test Strategy Tester completed-day visibility; no model, threshold, risk, lot, D/B surface, ATR SL/TP, or ONNX changes"
    )
    attempt["signal_policy"] = "runtime-boundary diagnostic only; shifted mirror is not forward KPI authority"
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
        "shift_minutes": SHIFT_MINUTES,
        "materialize_only": materialize_only,
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
        local_output = RUN_DIR / "shifted_custom_symbol_seed_status.json"
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


def next_day_audit(feature_rows: Sequence[Mapping[str, Any]], broker_api: Mapping[str, Any]) -> list[dict[str, Any]]:
    broker_feature = next((row for row in feature_rows if "broker" in str(row.get("attempt_name", ""))), {})
    feature_last = pd.to_datetime(str(broker_feature.get("feature_last_timestamp", "")), errors="coerce", utc=True)
    now = datetime.now(tz=UTC)
    latest = pd.to_datetime(str(broker_api.get("m5_last_close_utc", "")), errors="coerce", utc=True)
    due = False if pd.isna(feature_last) else now.date() > feature_last.date()
    return [
        {
            "audit_id": "next_day_rollover_due_check",
            "now_utc": now.replace(microsecond=0).isoformat().replace("+00:00", "Z"),
            "feature_last_timestamp": "" if pd.isna(feature_last) else feature_last.isoformat().replace("+00:00", "Z"),
            "broker_api_latest_m5_close": "" if pd.isna(latest) else latest.isoformat().replace("+00:00", "Z"),
            "next_day_rollover_due": due,
            "status": "due_or_past_due" if due else "not_yet_due_same_utc_date",
            "effect": "If now_utc is still the same UTC date as feature_last, the next-day broker rollover condition has not arrived yet.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def classify(
    runtime_rows: Sequence[Mapping[str, Any]],
    gap_rows: Sequence[Mapping[str, Any]],
    diff_rows: Sequence[Mapping[str, Any]],
    materialize_only: bool,
) -> tuple[str, str, str, str]:
    if materialize_only:
        return STATUS_MATERIALIZED, JUDGMENT_MATERIALIZED, DECISION_MATERIALIZED, RUN_ID
    broker_gap = next((row for row in gap_rows if "broker_rollover_control" in str(row.get("attempt_name", ""))), {})
    shifted_gap = next((row for row in gap_rows if "shifted_custom_mirror" in str(row.get("attempt_name", ""))), {})
    broker_reached = broker_gap.get("gap_status") == "tester_reached_feature_last"
    shifted_reached = shifted_gap.get("gap_status") == "tester_reached_feature_last"
    matched = sum(1 for row in diff_rows if str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true")
    if broker_reached:
        return STATUS_BOUNDARY_REPAIRED, JUDGMENT_BOUNDARY_REPAIRED, DECISION_BOUNDARY_REPAIRED, NEXT_RUN_ID_BOUNDARY_REPAIRED
    if shifted_reached and matched > 0:
        return STATUS_SHIFT_CONFIRMED, JUDGMENT_SHIFT_CONFIRMED, DECISION_SHIFT_CONFIRMED, NEXT_RUN_ID_COMPLETED_DAY
    return STATUS_PARTIAL, JUDGMENT_PARTIAL, DECISION_PARTIAL, NEXT_RUN_ID_REPAIR


def gate_rows(seed_run: Mapping[str, Any], next_day_rows: Sequence[Mapping[str, Any]], gap_rows: Sequence[Mapping[str, Any]], diff_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    broker_gap = next((row for row in gap_rows if "broker_rollover_control" in str(row.get("attempt_name", ""))), {})
    shifted_gap = next((row for row in gap_rows if "shifted_custom_mirror" in str(row.get("attempt_name", ""))), {})
    matched = sum(1 for row in diff_rows if str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true")
    return [
        {
            "gate_id": "next_day_rollover_due_checked",
            "status": "review" if next_day_rows and next_day_rows[0].get("status") == "not_yet_due_same_utc_date" else "passed",
            "evidence_path": rel(RUN_DIR / "next_day_rollover_audit.csv"),
            "effect": "현재 UTC 날짜가 feature_last 날짜를 지났는지 확인한다.",
        },
        {
            "gate_id": "shifted_custom_symbol_seed_output",
            "status": "passed" if (seed_run.get("script_output") or {}).get("status") == "completed" else "failed",
            "evidence_path": rel(RUN_DIR / "shifted_custom_symbol_seed_status.json"),
            "effect": "custom symbol(커스텀 심볼)에 -1440분 이동 M1 데이터를 심었는지 확인한다.",
        },
        {
            "gate_id": "broker_current_day_boundary_control",
            "status": "passed" if broker_gap.get("gap_status") == "tester_feature_last_gap_remains" else "review",
            "evidence_path": rel(RUN_DIR / "tester_feature_last_gap_seed_repair.csv"),
            "effect": "broker control(브로커 대조군)이 여전히 현재일 경계에 막히는지 확인한다.",
        },
        {
            "gate_id": "shifted_custom_tester_reached_feature_last",
            "status": "passed" if shifted_gap.get("gap_status") == "tester_reached_feature_last" else "failed",
            "evidence_path": rel(RUN_DIR / "tester_feature_last_gap_seed_repair.csv"),
            "effect": "하루 전 미러링된 custom symbol(커스텀 심볼)이 feature_last(피처 마지막 시점)에 도달하는지 확인한다.",
        },
        {
            "gate_id": "proxy_mt5_signal_window_parity",
            "status": "passed" if matched == len(diff_rows) and diff_rows else "review",
            "evidence_path": rel(RUN_DIR / "timestamp_aligned_proxy_mt5_difference.csv"),
            "effect": f"proxy expected(프록시 예상값)와 MT5 telemetry(MT5 기록)를 시점 맞춤으로 비교한다; matched={matched}/{len(diff_rows)}.",
        },
        {
            "gate_id": "no_retrain_no_threshold_or_lot_retune",
            "status": "passed",
            "evidence_path": rel(RUN_DIR / "handoff_attempts.csv"),
            "effect": "ONNX, feature order, threshold, risk, lot, ATR SL/TP를 바꾸지 않았음을 기록한다.",
        },
        {
            "gate_id": "claim_boundary_no_forward_goal",
            "status": "passed",
            "evidence_path": rel(RUN_DIR / "final_decision.json"),
            "effect": "Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)를 주장하지 않는다.",
        },
    ]


def proxy_usability_rows(gap_rows: Sequence[Mapping[str, Any]], diff_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    gap_by_attempt = {str(row.get("attempt_name", "")): row for row in gap_rows}
    rows: list[dict[str, Any]] = []
    for attempt_name in sorted({str(row.get("attempt_name", "")) for row in diff_rows}):
        group = [row for row in diff_rows if str(row.get("attempt_name", "")) == attempt_name]
        matched = sum(1 for row in group if str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true")
        total = len(group)
        gap_status = str(gap_by_attempt.get(attempt_name, {}).get("gap_status", ""))
        if matched == total and total and gap_status == "tester_feature_last_gap_remains":
            diagnostic = "usable_for_signal_parity_until_tester_cutoff_not_forward_decision"
            reason = "proxy expected values match MT5 telemetry, but tester still does not reach feature_last."
        elif matched == total and total and gap_status == "tester_reached_feature_last":
            diagnostic = "usable_for_signal_parity_and_boundary_diagnostic_not_forward_decision"
            reason = "proxy expected values match MT5 telemetry and tester reaches feature_last, but claim boundary still forbids forward authority."
        elif gap_status == "tester_reached_feature_last":
            diagnostic = "usable_for_boundary_visibility_only_not_signal_parity"
            reason = "tester reaches shifted feature_last, but generated-tick/custom-symbol window loses rows versus proxy expected values."
        else:
            diagnostic = "not_usable_requires_runtime_repair"
            reason = "tester output or feature window is incomplete."
        rows.append(
            {
                "attempt_name": attempt_name,
                "gap_status": gap_status,
                "proxy_matched": matched,
                "proxy_total": total,
                "diagnostic_usability": diagnostic,
                "forward_usability": "not_usable_as_forward_decision",
                "reason": reason,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def write_receipts(status: str, judgment: str, decision: str, next_action: str, seed_run: Mapping[str, Any], runtime_rows: Sequence[Mapping[str, Any]], gap_rows: Sequence[Mapping[str, Any]], diff_rows: Sequence[Mapping[str, Any]]) -> list[Path]:
    completed = sum(1 for row in runtime_rows if row.get("tester_status") == "completed" and row.get("runtime_status") == "completed" and row.get("report_status") == "completed")
    matched = sum(1 for row in diff_rows if str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true")
    return [
        write_json(
            RUN_DIR / "data_integrity_receipt.json",
            {
                "run_id": RUN_ID,
                "data_source": "US100 broker M1 copied into shifted custom symbol plus u42 feature CSV timestamp mirror",
                "time_axis": "broker control keeps real timestamps; shifted custom mirror subtracts 1440 minutes from bars and feature timestamps for tester-boundary diagnostics only",
                "sample_scope": "US100 M5 forward runtime boundary probe after 2026-04-14, not a forward KPI sample",
                "missing_or_duplicate_check": "feature_last and telemetry last observed are compared by attempt",
                "feature_label_boundary": "no labels, no retraining, no threshold fitting; shifted timestamps are synthetic diagnostic evidence only",
                "split_boundary": "runtime_probe_only",
                "leakage_risk": "high if shifted mirror is misused as forward KPI; claim boundary forbids it",
                "data_hash_or_identity": {"seed_status": (seed_run.get("script_output") or {}).get("status", ""), "runtime_rows": len(runtime_rows)},
                "integrity_judgment": "usable_for_runtime_boundary_diagnostic_not_forward_decision",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RUN_DIR / "runtime_parity_receipt.json",
            {
                "run_id": RUN_ID,
                "research_path": rel(Path(__file__)),
                "runtime_path": rel(RUN_DIR / "handoff_attempts.json"),
                "shared_contract": "same frozen u42 ONNX, feature order, D/B surface, threshold, risk, lot, ATR SL/TP; only symbol/time-axis diagnostic path changes for shifted mirror",
                "known_differences": "shifted custom mirror uses generated ticks and synthetic -1440 minute timestamp mirror; not KPI authority",
                "parity_check": f"runtime_completed={completed}/{len(runtime_rows)}; timestamp_aligned_signal_parity={matched}/{len(diff_rows)}",
                "parity_identity": rel(RUN_DIR / "execution_result.json"),
                "runtime_claim_boundary": "runtime_probe_only_no_runtime_authority",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RUN_DIR / "backtest_forensics_receipt.json",
            {
                "run_id": RUN_ID,
                "tester_identity": "portable FPMarkets MT5 Strategy Tester, broker US100 real-tick control and shifted custom-symbol generated-tick diagnostic",
                "ea_identity": rel(RUN_DIR / "handoff_attempts.json"),
                "report_identity": [row.get("report_path", "") for row in runtime_rows],
                "trade_evidence": [{key: row.get(key, "") for key in ("attempt_name", "net_profit", "profit_factor", "trade_count", "max_drawdown_amount")} for row in runtime_rows],
                "cost_assumptions": "costs inherited from frozen u42 set; generated-tick custom mirror is not cost or KPI authority",
                "forensic_checks": ["tester boundary log parsed", "telemetry copied", "report parsed when available", "seed output captured"],
                "backtest_judgment": "usable_for_boundary_diagnostic_not_forward_decision",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RUN_DIR / "result_judgment_receipt.json",
            {
                "run_id": RUN_ID,
                "result_subject": "next-day broker rollover or custom-symbol shifted seed repair",
                "evidence_available": [rel(RUN_DIR / "tester_boundary_seed_repair.csv"), rel(RUN_DIR / "tester_feature_last_gap_seed_repair.csv"), rel(RUN_DIR / "timestamp_aligned_proxy_mt5_difference.csv")],
                "evidence_missing": "true next-day broker rollover cannot be proven until UTC date advances beyond feature_last date",
                "judgment_label": "runtime_probe",
                "status": status,
                "judgment": judgment,
                "decision": decision,
                "claim_boundary": "shifted mirror can diagnose tester policy but cannot prove Forward Passed/Failed",
                "next_condition": next_action,
                "user_explanation_hook": "If shifted mirror reaches feature_last while broker control does not, the blocker is current-day tester policy, not ONNX parity.",
            },
        ),
    ]


def write_report(status: str, judgment: str, decision: str, next_action: str, api_rows: Sequence[Mapping[str, Any]], next_day_rows: Sequence[Mapping[str, Any]], runtime_rows: Sequence[Mapping[str, Any]], boundary_rows: Sequence[Mapping[str, Any]], gap_rows: Sequence[Mapping[str, Any]], diff_rows: Sequence[Mapping[str, Any]], usability_rows: Sequence[Mapping[str, Any]]) -> Path:
    completed = sum(1 for row in runtime_rows if row.get("tester_status") == "completed" and row.get("runtime_status") == "completed" and row.get("report_status") == "completed")
    matched = sum(1 for row in diff_rows if str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true")
    broker_gap = next((row for row in gap_rows if "broker_rollover_control" in str(row.get("attempt_name", ""))), {})
    shifted_gap = next((row for row in gap_rows if "shifted_custom_mirror" in str(row.get("attempt_name", ""))), {})
    lines = [
        "# Stage337AC Next-Day Rollover or Custom Symbol Seed Repair(337AC 다음날 이월 또는 커스텀 심볼 심기 수리)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- status(상태): `{status}`",
        f"- judgment(판정): `{judgment}`",
        f"- decision(결정): `{decision}`",
        f"- next_action(다음 행동): `{next_action}`",
        f"- next_day_rollover_status(다음날 이월 상태): `{next_day_rows[0].get('status', '') if next_day_rows else ''}`",
        f"- shifted_custom_symbol(이동 커스텀 심볼): `{SHIFTED_CUSTOM_SYMBOL}`",
        f"- shift_minutes(이동 분): `{SHIFT_MINUTES}`",
        f"- MT5 runtime completed(MT5 런타임 완료): `{completed}/{len(runtime_rows)}`",
        f"- broker control gap(브로커 대조 공백): `{broker_gap.get('gap_status', '')}`",
        f"- shifted custom gap(이동 커스텀 공백): `{shifted_gap.get('gap_status', '')}`",
        f"- timestamp-aligned proxy parity(시점 맞춤 프록시 동등성): `{matched}/{len(diff_rows)}`",
        "- Forward Passed(전진 통과): `not_claimed`",
        "- Forward Failed(전진 실패): `not_claimed`",
        "- runtime authority(런타임 권위): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Meaning(의미)",
        "",
        "run337AC(337AC 실행)는 새 후보 개발이 아니다. broker control(브로커 대조군)은 원래 시간축을 유지하고, shifted custom mirror(이동 커스텀 미러)는 같은 봉과 같은 feature value(피처 값)를 1440분 과거로 옮긴다.",
        "",
        "Effect(효과): 이동 미러가 feature_last(피처 마지막 시점)에 도달하면, custom symbol seed(커스텀 심볼 심기)와 feature handoff(피처 인계)는 과거 완성일에서는 작동한다는 뜻이다. 그 경우 현재 공백은 ONNX parity(온엑스 동등성)보다 Strategy Tester current-day policy(전략 테스터 현재일 정책) 쪽으로 좁혀진다.",
        "",
        "## API Visibility(API 가시성)",
        "",
        "| symbol(심볼) | status(상태) | custom(커스텀) | m5 last close(M5 마지막 종가 시점) |",
        "|---|---|---:|---:|",
    ]
    for row in api_rows:
        lines.append(f"| `{row.get('symbol', '')}` | `{row.get('status', '')}` | `{row.get('symbol_custom', '')}` | `{row.get('m5_last_close_utc', '')}` |")
    lines.extend(["", "## Tester Boundary(테스터 경계)", "", "| attempt(시도) | symbol(심볼) | requested to(요청 종료) | log test to(로그 종료) | last observed(마지막 관측) | gap status(공백 상태) |", "|---|---|---:|---:|---:|---|"])
    boundary_by = {row.get("attempt_name"): row for row in boundary_rows}
    for row in gap_rows:
        boundary = boundary_by.get(row.get("attempt_name"), {})
        lines.append(
            f"| `{row.get('attempt_name', '')}` | `{boundary.get('tester_symbol', '')}` | `{boundary.get('requested_to_date', '')}` | `{boundary.get('log_test_to', '')}` | `{row.get('tester_last_observed_bar_time', '')}` | `{row.get('gap_status', '')}` |"
        )
    lines.extend(
        [
            "",
            "## Proxy vs MT5(프록시 대 MT5)",
            "",
            "proxy expected(프록시 예상값)는 timestamp-aligned(시점 맞춤) runtime signal parity(런타임 신호 동등성)에만 쓴다. shifted mirror(이동 미러)는 synthetic diagnostic(합성 진단)이므로 Forward decision(전진 판정)이나 KPI authority(KPI 권위)가 아니다.",
            "",
            "| attempt(시도) | matched(일치) | diagnostic usability(진단 활용성) | forward usability(전진 활용성) |",
            "|---|---:|---|---|",
        ]
    )
    for row in usability_rows:
        lines.append(
            f"| `{row.get('attempt_name', '')}` | `{row.get('proxy_matched', '')}/{row.get('proxy_total', '')}` | `{row.get('diagnostic_usability', '')}` | `{row.get('forward_usability', '')}` |"
        )
    return write_md(REPORT_PATH, "\n".join(lines))


def write_decision_doc(status: str, judgment: str, decision: str, next_action: str) -> Path:
    text = f"""# 2026-05-27 Stage337AC Next-Day or Seed Repair Decision(337AC 다음날 또는 심기 수리 결정)

- status(상태): `{status}`
- judgment(판정): `{judgment}`
- decision(결정): `{decision}`
- next_action(다음 행동): `{next_action}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Effect(효과): run337AC(337AC 실행)는 broker current-day boundary(브로커 현재일 경계)와 shifted custom mirror(이동 커스텀 미러)를 분리했다. 이 결과는 tester policy repair evidence(테스터 정책 수리 근거)이며 운영/전진 판정이 아니다.
"""
    return write_md(DECISION_DOC, text)


def update_status_docs(status: str, decision: str, next_action: str, seed_run: Mapping[str, Any], gap_rows: Sequence[Mapping[str, Any]], diff_rows: Sequence[Mapping[str, Any]]) -> list[Path]:
    broker_gap = next((row for row in gap_rows if "broker_rollover_control" in str(row.get("attempt_name", ""))), {})
    shifted_gap = next((row for row in gap_rows if "shifted_custom_mirror" in str(row.get("attempt_name", ""))), {})
    matched = sum(1 for row in diff_rows if str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true")
    selected_text = f"""# Stage337 Selection Status(337단계 선택 상태)

- stage_id(단계 ID): `{STAGE_ID}`
- stage_status(단계 상태): `open_active`
- selected_candidate(선택 후보): `none`
- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{decision}`
- current_run(현재 실행): `{next_action}`
- shifted_custom_symbol(이동 커스텀 심볼): `{SHIFTED_CUSTOM_SYMBOL}`
- shifted_seed_status(이동 심기 상태): `{(seed_run.get('script_output') or {}).get('status', '')}`
- broker_control_gap(브로커 대조 공백): `{broker_gap.get('gap_status', '')}`
- shifted_custom_gap(이동 커스텀 공백): `{shifted_gap.get('gap_status', '')}`
- timestamp_aligned_proxy_parity(시점 맞춤 프록시 동등성): `{matched}/{len(diff_rows)}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Forward Blocked(전진 차단): `tester_current_day_visibility_boundary_not_operating_resolved`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{next_action}`
- effect(효과): run337AC(337AC 실행)는 shifted custom mirror(이동 커스텀 미러)로 Strategy Tester(전략 테스터)의 completed-day visibility(완성일 가시성)를 분리했고, 최신 forward(전진) 판정은 아직 주장하지 않는다.
"""
    write_md(SELECTED_STATUS, selected_text)

    focus = (
        f"  Stage337 run337AC focus complete: run337AC(337AC 실행)는 `{status}`로 next-day rollover/custom seed repair probe"
        f"(다음날 이월/커스텀 심볼 심기 수리 탐침)를 기록했다. Effect(효과): shifted seed(이동 심기) `{(seed_run.get('script_output') or {}).get('status', '')}`, "
        f"broker control gap(브로커 대조 공백) `{broker_gap.get('gap_status', '')}`, shifted custom gap(이동 커스텀 공백) `{shifted_gap.get('gap_status', '')}`, "
        f"timestamp-aligned proxy parity(시점 맞춤 프록시 동등성) `{matched}/{len(diff_rows)}`이며 Forward/Goal(전진/목표)은 주장하지 않는다."
    )
    if path_exists(WORKSPACE_STATE):
        text, had_bom = ab.read_text_lossless(WORKSPACE_STATE)
        text = re.sub(r"current_run_id: .*", f"current_run_id: {next_action}", text, count=1)
        if "Stage337 run337AC focus complete" not in text:
            text = text.replace("current_focus:\n", f"current_focus:\n- >-\n{focus}\n")
        else:
            text = re.sub(r"- >-\n  Stage337 run337AC focus complete:.*?(?=\n- >-|\Z)", f"- >-\n{focus}", text, count=1, flags=re.S)
        ab.write_text_preserving(WORKSPACE_STATE, text, had_bom)

    header = f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `337_onnx_research_packet__cost_buffer_direction_curve_rebuild_v1`
- current_run(현재 실행): `{next_action}`
- active_stage(활성 단계): `{STAGE_ID}`
- selected_research_baseline(선택 연구 기준): `none`
- target_surface(목표 표면): `cost_buffer_direction_curve_rebuild`
- status(상태): `{status}`
- decision(결정): `{decision}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- next_action(다음 행동): `{next_action}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    current_entry = f"""
## Stage337 run337AC(337AC 실행) - {TODAY}

- status(상태): `{status}`
- decision(결정): `{decision}`
- next_action(다음 행동): `{next_action}`
- effect(효과): shifted custom mirror(이동 커스텀 미러) `{SHIFTED_CUSTOM_SYMBOL}`로 tester current-day boundary(테스터 현재일 경계)를 분리했다. broker gap(브로커 공백) `{broker_gap.get('gap_status', '')}`, shifted gap(이동 공백) `{shifted_gap.get('gap_status', '')}`, proxy parity(프록시 동등성) `{matched}/{len(diff_rows)}`.
"""
    if path_exists(CURRENT_STATE):
        text, had_bom = ab.read_text_lossless(CURRENT_STATE)
        text = re.sub(r"\A# Current Working State\(현재 작업 상태\).*?(?=\n## )", header.rstrip() + "\n", text, count=1, flags=re.S)
        if "## Stage337 run337AC(337AC 실행)" in text:
            text = re.sub(r"## Stage337 run337AC\(337AC 실행\).*?(?=\n## |\Z)", current_entry.strip(), text, count=1, flags=re.S)
        else:
            text = text.rstrip() + "\n\n" + current_entry.strip() + "\n"
        ab.write_text_preserving(CURRENT_STATE, text, had_bom)

    if path_exists(CHANGELOG):
        text, had_bom = ab.read_text_lossless(CHANGELOG)
        line = f"\n- {TODAY}: Stage337 run337AC(337AC 실행) `{status}`. Effect(효과): shifted custom seed repair(이동 커스텀 심볼 심기 수리) `{shifted_gap.get('gap_status', '')}`를 기록하고 Forward/Goal(전진/목표)은 주장하지 않았다.\n"
        if "Stage337 run337AC(337AC 실행)" in text:
            text = re.sub(r"\n- [^\n]*Stage337 run337AC\(337AC 실행\)[^\n]*", line.rstrip(), text, count=1)
        else:
            text = text.rstrip() + line
        ab.write_text_preserving(CHANGELOG, text, had_bom)

    if path_exists(STAGE_BRIEF):
        text, had_bom = ab.read_text_lossless(STAGE_BRIEF)
        text = re.sub(r"- latest_run\(최신 실행\): `[^`]+`", f"- latest_run(최신 실행): `{RUN_ID}`", text)
        summary = (
            f"- run337AC_summary(337AC 요약): `{status}`. Effect(효과): shifted custom gap(이동 커스텀 공백) "
            f"`{shifted_gap.get('gap_status', '')}`와 proxy parity(프록시 동등성) `{matched}/{len(diff_rows)}`를 기록했다.\n"
        )
        if "run337AC_summary(337AC 요약)" in text:
            text = re.sub(r"- run337AC_summary\(337AC 요약\): [^\n]*(?:\n|$)", summary, text, count=1)
        else:
            text = text.replace("- selected_candidate(선택 후보):", summary + "- selected_candidate(선택 후보):")
        ab.write_text_preserving(STAGE_BRIEF, text, had_bom)
    return [SELECTED_STATUS, WORKSPACE_STATE, CURRENT_STATE, CHANGELOG, STAGE_BRIEF]


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
                "notes": "run337AC next-day rollover or shifted custom seed repair artifact; no forward or goal claim",
                "artifact_path": r,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(ARTIFACT_REGISTRY, columns, rows)


def update_registers(status: str, judgment: str, decision: str, next_action: str, artifact_paths: Sequence[Path]) -> list[Path]:
    aa.upsert_csv(
        RUN_REGISTRY,
        ["run_id"],
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "family": "next_day_rollover_or_custom_symbol_seed_repair",
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
            "run_key": f"{RUN_ID}__next_day_rollover_or_custom_symbol_seed_repair",
            "ledger_row_id": f"{RUN_ID}__next_day_rollover_or_custom_symbol_seed_repair",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "family": "next_day_rollover_or_custom_symbol_seed_repair",
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


def main() -> None:
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
        "effect": "Feature timestamps are shifted only to test completed-day tester visibility. Feature values, ONNX, thresholds, risk, lot, and D/B surface are unchanged.",
        "claim_boundary": CLAIM_BOUNDARY,
    }

    seed_prepare = prepare_shifted_seed(terminal_path, metaeditor_path, args.materialize_only)
    seed_run = run_shifted_seed(terminal_path, args.materialize_only)
    broker_api = ab.mt5_api_symbol_visibility(terminal_path, ORIGIN_SYMBOL)
    shifted_api = ab.mt5_api_symbol_visibility(terminal_path, SHIFTED_CUSTOM_SYMBOL)
    api_rows = [broker_api, shifted_api]
    pre_tester_recovery = qprobe.stop_target_terminal_if_running(terminal_path)

    prepared = build_source_attempts(source, shifted_feature)
    feature_rows_prepared = qprobe.feature_last_rows(prepared)
    next_day_rows = next_day_audit(feature_rows_prepared, broker_api)
    attempts, handoff_rows, materialized_artifacts = base.build_attempts(prepared, common_files_root)
    scenario_by_attempt = {str(row["attempt_name"]): row for row in prepared}
    for attempt in attempts:
        scenario = scenario_by_attempt.get(str(attempt["attempt_name"]), {})
        for key in ("scenario_id", "scenario_symbol", "scenario_from_date", "scenario_to_date", "scenario_model", "scenario_role"):
            attempt[key] = scenario.get(key, "")
    attempts = [rewrite_attempt_to_scenario(dict(attempt)) for attempt in attempts]
    before_offsets = qprobe.log_offsets([TESTER_AGENT_LOG, TESTER_LOG])
    if args.materialize_only:
        execution_result = {
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
    latest_probe = {"last_close_utc": broker_api.get("m5_last_close_utc", "")}
    gap_rows = qprobe.tester_gap_rows(runtime_rows, feature_rows, common_files_root, latest_probe)
    boundary_rows = ab.parse_tester_boundary_rows(before_offsets, attempts)
    boundary_by_attempt = {row["attempt_name"]: row for row in boundary_rows}
    for row in gap_rows:
        row["scenario_id"] = boundary_by_attempt.get(row.get("attempt_name"), {}).get("scenario_id", "")
        row["tester_symbol"] = boundary_by_attempt.get(row.get("attempt_name"), {}).get("tester_symbol", "")
    cutoff_by_attempt = {str(row.get("attempt_name", "")): str(row.get("tester_last_observed_bar_time", "")) for row in gap_rows}
    aligned_proxy_rows = qprobe.sanitize_proxy_rows(
        qprobe.build_timestamp_aligned_proxy_rows(attempts, cutoff_by_attempt),
        default_source="stage337AC_timestamp_aligned_python_onnx_inference",
    )
    diff_rows = base.build_signal_difference_rows(aligned_proxy_rows, runtime_rows)
    for row in diff_rows:
        row["mt5_source"] = "stage337AC_runtime_summary_seed_repair_probe"
        row["usable_for_forward_pass_fail"] = False
        row["claim_boundary"] = CLAIM_BOUNDARY

    status, judgment, decision, next_action = classify(runtime_rows, gap_rows, diff_rows, args.materialize_only)
    gates = gate_rows(seed_run, next_day_rows, gap_rows, diff_rows)
    usability_rows = proxy_usability_rows(gap_rows, diff_rows)
    receipts = write_receipts(status, judgment, decision, next_action, seed_run, runtime_rows, gap_rows, diff_rows)
    report = write_report(status, judgment, decision, next_action, api_rows, next_day_rows, runtime_rows, boundary_rows, gap_rows, diff_rows, usability_rows)
    decision_doc = write_decision_doc(status, judgment, decision, next_action)

    artifact_paths: list[Path] = [
        write_json(RUN_DIR / "timestamp_shift_contract.json", shift_contract),
        write_json(RUN_DIR / "shifted_custom_symbol_seed_prepare.json", seed_prepare),
        write_json(RUN_DIR / "shifted_custom_symbol_seed_run.json", seed_run),
        write_json(RUN_DIR / "pre_tester_terminal_recovery.json", pre_tester_recovery),
        write_json(RUN_DIR / "execution_result.json", execution_result),
        write_json(
            RUN_DIR / "final_decision.json",
            {
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
            },
        ),
        write_csv(RUN_DIR / "custom_symbol_api_visibility.csv", sorted({key for row in api_rows for key in row.keys()}), api_rows),
        write_csv(RUN_DIR / "next_day_rollover_audit.csv", sorted({key for row in next_day_rows for key in row.keys()}), next_day_rows),
        write_csv(RUN_DIR / "handoff_attempts.csv", sorted({key for row in handoff_rows for key in row.keys()}), handoff_rows),
        write_json(RUN_DIR / "handoff_attempts.json", attempts),
        write_csv(RUN_DIR / "runtime_summary.csv", sorted({key for row in runtime_rows for key in row.keys()}), runtime_rows),
        write_csv(RUN_DIR / "feature_last_timestamp_audit.csv", sorted({key for row in feature_rows for key in row.keys()}), feature_rows),
        write_csv(RUN_DIR / "tester_boundary_seed_repair.csv", sorted({key for row in boundary_rows for key in row.keys()}), boundary_rows),
        write_csv(RUN_DIR / "tester_feature_last_gap_seed_repair.csv", sorted({key for row in gap_rows for key in row.keys()}), gap_rows),
        write_csv(RUN_DIR / "timestamp_aligned_proxy_expected_result.csv", sorted({key for row in aligned_proxy_rows for key in row.keys()}), aligned_proxy_rows),
        write_csv(RUN_DIR / "timestamp_aligned_proxy_mt5_difference.csv", sorted({key for row in diff_rows for key in row.keys()}), diff_rows),
        write_csv(RUN_DIR / "proxy_usability_judgment.csv", sorted({key for row in usability_rows for key in row.keys()}), usability_rows),
        write_csv(RUN_DIR / "required_gate_coverage_audit.csv", sorted({key for row in gates for key in row.keys()}), gates),
        report,
        decision_doc,
        shifted_feature,
        *materialized_artifacts,
        *copied_runtime_artifacts,
        *receipts,
    ]
    if path_exists(RUN_DIR / "shifted_custom_symbol_seed_status.json"):
        artifact_paths.append(RUN_DIR / "shifted_custom_symbol_seed_status.json")
    docs = update_status_docs(status, decision, next_action, seed_run, gap_rows, diff_rows)
    registers = update_registers(status, judgment, decision, next_action, [*artifact_paths, *docs])
    artifact_paths.extend(docs)
    artifact_paths.extend(registers)
    write_json(
        RUN_DIR / "run_manifest.json",
        {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "status": status,
            "judgment": judgment,
            "decision": decision,
            "next_action": next_action,
            "artifact_count": len(artifact_paths),
            "artifact_paths": [rel(path) for path in artifact_paths],
            "materialize_only": args.materialize_only,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    upsert_artifact_registry([*artifact_paths, RUN_DIR / "run_manifest.json"])

    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": status,
                "judgment": judgment,
                "decision": decision,
                "next_action": next_action,
                "broker_gap": next((row.get("gap_status") for row in gap_rows if "broker_rollover_control" in str(row.get("attempt_name", ""))), ""),
                "shifted_gap": next((row.get("gap_status") for row in gap_rows if "shifted_custom_mirror" in str(row.get("attempt_name", ""))), ""),
                "proxy_diff_matched": sum(1 for row in diff_rows if str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true"),
                "proxy_diff_rows": len(diff_rows),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
