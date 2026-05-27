from __future__ import annotations

import argparse
import csv
import json
import math
import os
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, path_exists, sha256_file_lf_normalized  # noqa: E402
from foundation.mt5.runtime_artifacts import sha256_file  # noqa: E402
from stage_pipelines.stage335 import independent_proxy_mt5_probe as base  # noqa: E402
from stage_pipelines.stage337 import probe_custom_symbol_intraday_tester_visibility as ab  # noqa: E402
from stage_pipelines.stage337 import review_runtime_data_and_feature_source_repair_probe as qprobe  # noqa: E402


TODAY = "2026-05-27"
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
RUN_NUMBER = "run337AI"
RUN_ID = "run337AI_tester_visibility_alternative_repair_or_rollover_reprobe_v1"
PARENT_RUN_ID = "run337AH_execute_full_current_day_visibility_repair_and_no_overfit_preflight_v1"
NEXT_RUN_ID_FULL_ATTRIB = "run337AJ_full_current_day_forward_attribution_cost_curve_review_v1"
NEXT_RUN_ID_MODELING_POLICY = "run337AJ_source_modeling_policy_decision_or_custom_symbol_parity_repair_v1"
NEXT_RUN_ID_REPAIR = "run337AJ_data_history_cache_repair_or_next_rollover_wait_reprobe_v1"
NEXT_RUN_ID_RUNTIME_REPAIR = "run337AJ_runtime_output_repair_then_model_mode_reprobe_v1"
CLAIM_BOUNDARY = (
    "research_development_only_stage337AI_tester_visibility_alternative_repair_no_model_training_"
    "no_threshold_retuning_no_lot_optimization_no_candidate_selection_no_forward_passed_no_forward_failed_"
    "no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STATUS_REAL_TICK_REACHED = "completed_stage337AI_real_tick_full_current_day_reached_feature_last_no_forward_decision"
STATUS_ALTERNATIVE_BOUNDARY = "completed_stage337AI_alternative_tester_model_reaches_feature_last_boundary_only_no_forward_decision"
STATUS_ALL_GAP = "completed_stage337AI_all_tester_model_alternatives_gap_remain_no_forward_decision"
STATUS_RUNTIME_ISSUE = "completed_stage337AI_runtime_issue_no_forward_decision"
STATUS_MATERIALIZED = "completed_stage337AI_model_mode_reprobe_materialized_execution_pending_no_forward_decision"

JUDGMENT_REAL_TICK_REACHED = "real_tick_control_reached_feature_last_open_full_current_day_attribution_without_forward_decision"
JUDGMENT_ALTERNATIVE_BOUNDARY = "alternative_tester_model_reached_feature_last_real_tick_gap_remains_boundary_only_not_kpi_authority"
JUDGMENT_ALL_GAP = "all_tester_model_modes_gap_remain_current_day_boundary_not_resolved"
JUDGMENT_RUNTIME_ISSUE = "runtime_or_report_output_incomplete_repair_required_before_visibility_decision"
JUDGMENT_MATERIALIZED = "model_mode_reprobe_inputs_materialized_execution_pending"

DECISION_REAL_TICK_REACHED = "stage337AI_open_run337AJ_full_current_day_attribution_no_selection"
DECISION_ALTERNATIVE_BOUNDARY = "stage337AI_open_run337AJ_modeling_policy_or_custom_symbol_parity_repair_no_selection"
DECISION_ALL_GAP = "stage337AI_open_run337AJ_history_cache_repair_or_rollover_wait_reprobe_no_selection"
DECISION_RUNTIME_ISSUE = "stage337AI_open_run337AJ_runtime_output_repair_no_selection"
DECISION_MATERIALIZED = "stage337AI_execution_pending_no_selection"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
RUN337Z_ATTEMPTS = STAGE_DIR / "02_runs" / "run337Z" / "rollover_reprobe_handoff_attempts.json"
MT5_DIR = RUN_DIR / "mt5"
FEATURE_COPY_DIR = RUN_DIR / "feature_matrices"
MODEL_COPY_DIR = RUN_DIR / "models"
TELEMETRY_DIR = RUN_DIR / "runtime_telemetry"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEWS_DIR / "run337AI_tester_visibility_alternative_repair_or_rollover_reprobe.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage337AI_tester_visibility_alternative_repair_or_rollover_reprobe.md"
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

COMMON_ROOT = "Project_Obsidian_Prime_v2/stage337/run337AI_tester_visibility_model_mode_reprobe"
ORIGIN_SYMBOL = "US100"
BROKER_FROM_DATE = "2026.04.14"
BROKER_TO_DATE = "2026.05.30"
ATTEMPT_BASE = "u42_plain_rf"

MODEL_MODE_SCENARIOS = [
    {
        "suffix": "model4_real_ticks_control",
        "artifact_slug": "u42_plain_ai_model4_real_ticks",
        "scenario_id": "model4_real_ticks_control",
        "model_code": "4",
        "model_label": "real_ticks",
    },
    {
        "suffix": "model0_every_tick_generated",
        "artifact_slug": "u42_plain_ai_model0_every_tick_generated",
        "scenario_id": "model0_generated_every_tick_alternative",
        "model_code": "0",
        "model_label": "generated_every_tick",
    },
    {
        "suffix": "model1_m1_ohlc",
        "artifact_slug": "u42_plain_ai_model1_m1_ohlc",
        "scenario_id": "model1_m1_ohlc_alternative",
        "model_code": "1",
        "model_label": "m1_ohlc",
    },
    {
        "suffix": "model2_open_prices",
        "artifact_slug": "u42_plain_ai_model2_open_prices",
        "scenario_id": "model2_open_prices_alternative",
        "model_code": "2",
        "model_label": "open_prices",
    },
]


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return item.as_posix()


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


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


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return "" if not math.isfinite(value) else f"{value:.12g}"
    if isinstance(value, pd.Timestamp):
        return value.isoformat().replace("+00:00", "Z")
    if isinstance(value, (Mapping, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    return str(value)


def truthy(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "matched"}


def number(value: Any, default: float = 0.0) -> float:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return default
    return parsed if math.isfinite(parsed) else default


def columns_for(rows: Sequence[Mapping[str, Any]], fallback: Sequence[str]) -> list[str]:
    if not rows:
        return list(fallback)
    columns: list[str] = []
    for row in rows:
        for key in row:
            if key not in columns:
                columns.append(str(key))
    return columns


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, columns: Sequence[str], rows: Iterable[Mapping[str, Any]]) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    tmp = io_path(path).with_name(io_path(path).name + ".tmp")
    with tmp.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column, "")) for column in columns})
    os.replace(tmp, io_path(path))
    return path


def read_json(path: Path) -> Any:
    if not path_exists(path):
        return {}
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def read_text(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    bom = raw.startswith(b"\xef\xbb\xbf")
    return raw.decode("utf-8-sig" if bom else "utf-8"), bom


def write_text(path: Path, text: str, had_bom: bool | None = None) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    encoding = "utf-8-sig" if had_bom or path.suffix.lower() in {".md", ".txt", ".yaml"} else "utf-8"
    normalized = text.replace("\r\n", "\n").replace("\r", "\n").rstrip() + "\n"
    io_path(path).write_text(normalized, encoding=encoding)
    return path


def write_md(path: Path, text: str) -> Path:
    return write_text(path, text, True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stage337AI tester visibility model-mode reprobe.")
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
        module.RUN_ID = RUN_ID
        module.RUN_DIR = RUN_DIR
        module.CLAIM_BOUNDARY = CLAIM_BOUNDARY
    base.STAGE_ID = STAGE_ID
    base.RUN_NUMBER = RUN_NUMBER
    base.PARENT_RUN_ID = PARENT_RUN_ID
    base.MT5_DIR = MT5_DIR
    base.FEATURE_COPY_DIR = FEATURE_COPY_DIR
    base.MODEL_COPY_DIR = MODEL_COPY_DIR
    base.TELEMETRY_DIR = TELEMETRY_DIR
    base.COMMON_ROOT = COMMON_ROOT
    qprobe.TODAY = TODAY
    qprobe.STAGE_ID = STAGE_ID
    qprobe.RUN_NUMBER = RUN_NUMBER
    qprobe.PARENT_RUN_ID = PARENT_RUN_ID
    qprobe.RUN_DIR = RUN_DIR
    qprobe.MT5_DIR = MT5_DIR
    qprobe.FEATURE_COPY_DIR = FEATURE_COPY_DIR
    qprobe.MODEL_COPY_DIR = MODEL_COPY_DIR
    qprobe.TELEMETRY_DIR = TELEMETRY_DIR
    qprobe.TESTER_LOG = TESTER_LOG
    qprobe.TESTER_AGENT_LOG = TESTER_AGENT_LOG
    qprobe.TERMINAL_LOG = TERMINAL_LOG
    ab.TESTER_LOG = TESTER_LOG
    ab.TESTER_AGENT_LOG = TESTER_AGENT_LOG
    ab.TERMINAL_LOG = TERMINAL_LOG


def load_source_u42() -> dict[str, Any]:
    rows = read_json(RUN337Z_ATTEMPTS)
    if not isinstance(rows, list):
        raise RuntimeError(f"source attempts is not a list: {RUN337Z_ATTEMPTS}")
    source = next((dict(row) for row in rows if row.get("attempt_name") == ATTEMPT_BASE), None)
    if source is None:
        raise RuntimeError(f"missing {ATTEMPT_BASE} in {RUN337Z_ATTEMPTS}")
    return source


def build_source_attempts(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    for index, scenario in enumerate(MODEL_MODE_SCENARIOS):
        copied = dict(source)
        copied["attempt_name"] = f"u42_plain_rf_ai_{scenario['suffix']}"
        copied["artifact_slug"] = scenario["artifact_slug"]
        copied["scenario_id"] = scenario["scenario_id"]
        copied["scenario_symbol"] = ORIGIN_SYMBOL
        copied["scenario_from_date"] = BROKER_FROM_DATE
        copied["scenario_to_date"] = BROKER_TO_DATE
        copied["scenario_model"] = scenario["model_code"]
        copied["tester_model_label"] = scenario["model_label"]
        copied["model_copy"] = {"source": source.get("model_local_path") or source.get("model_copy", {}).get("source", "")}
        copied["feature_export"] = {"path": source.get("feature_local_path", "")}
        copied["feature_local_path"] = source.get("feature_local_path", "")
        copied["source_run_id"] = PARENT_RUN_ID
        copied["attempt_role"] = "stage337AI_model_mode_visibility_reprobe_same_frozen_u42_model_threshold_risk"
        copied["record_view_prefix"] = f"mt5_stage337AI_u42_plain_model_mode_{index}"
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
    attempt["attempt_role"] = "stage337AI_tester_model_mode_visibility_reprobe_same_frozen_u42_model_threshold_risk"
    attempt["record_view_prefix"] = f"mt5_stage337AI_{attempt['artifact_slug']}"
    attempt["source_run_id"] = PARENT_RUN_ID
    attempt["repair_contract"] = (
        "same ONNX, feature order, D/B surface, score threshold, risk, lot, and ATR SL/TP; "
        "only MT5 Strategy Tester Model field is varied to diagnose visibility boundary"
    )
    attempt["signal_policy"] = "visibility diagnostic only; generated-model modes are not KPI authority"
    return attempt


def runtime_completed(row: Mapping[str, Any]) -> bool:
    return (
        str(row.get("tester_status", "")) == "completed"
        and str(row.get("runtime_status", "")) == "completed"
        and str(row.get("report_status", "")) == "completed"
    )


def proxy_usability_rows(gap_rows: Sequence[Mapping[str, Any]], diff_rows: Sequence[Mapping[str, Any]], attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    gap_by_attempt = {str(row.get("attempt_name", "")): row for row in gap_rows}
    attempt_by = {str(row.get("attempt_name", "")): row for row in attempts}
    rows: list[dict[str, Any]] = []
    for attempt_name in sorted(attempt_by):
        group = [row for row in diff_rows if str(row.get("attempt_name", "")) == attempt_name]
        matched = sum(1 for row in group if truthy(row.get("usable_for_runtime_signal_parity")))
        total = len(group)
        gap_status = str(gap_by_attempt.get(attempt_name, {}).get("gap_status", ""))
        tester_model = str(attempt_by[attempt_name].get("tester_model", ""))
        if tester_model == "4" and matched == total and total and gap_status == "tester_reached_feature_last":
            diagnostic = "real_tick_control_signal_parity_complete_open_attribution_review"
        elif tester_model != "4" and gap_status == "tester_reached_feature_last":
            diagnostic = "alternative_model_reaches_feature_last_boundary_only_not_kpi_authority"
        elif matched == total and total:
            diagnostic = "signal_parity_usable_until_tester_cutoff_not_forward_decision"
        else:
            diagnostic = "not_usable_for_signal_parity_requires_runtime_review"
        rows.append(
            {
                "attempt_name": attempt_name,
                "tester_model": tester_model,
                "tester_model_label": attempt_by[attempt_name].get("tester_model_label", ""),
                "gap_status": gap_status,
                "proxy_matched": matched,
                "proxy_total": total,
                "diagnostic_usability": diagnostic,
                "forward_usability": "not_usable_as_forward_pass_fail_decision",
                "allowed_use": "runtime signal parity(런타임 신호 동등성) and tester visibility diagnosis(테스터 가시성 진단)",
                "disallowed_use": "KPI authority(KPI 권위), Forward Passed/Failed(전방 통과/실패), candidate selection(후보 선택)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def runtime_kpi_rows(runtime_rows: Sequence[Mapping[str, Any]], attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    attempt_by = {str(row.get("attempt_name", "")): row for row in attempts}
    rows: list[dict[str, Any]] = []
    for row in runtime_rows:
        attempt_name = str(row.get("attempt_name", ""))
        trades = number(row.get("trade_count"), default=0.0)
        net = number(row.get("net_profit"), default=0.0)
        rows.append(
            {
                "attempt_name": attempt_name,
                "tester_model": attempt_by.get(attempt_name, {}).get("tester_model", ""),
                "tester_model_label": attempt_by.get(attempt_name, {}).get("tester_model_label", ""),
                "tester_status": row.get("tester_status", ""),
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
                "lot_normalized_net_per_trade": "" if trades <= 0 else net / trades,
                "kpi_authority": "diagnostic_only_not_forward_authority",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def model_mode_matrix_rows(
    runtime_rows: Sequence[Mapping[str, Any]],
    gap_rows: Sequence[Mapping[str, Any]],
    usability_rows: Sequence[Mapping[str, Any]],
    boundary_rows: Sequence[Mapping[str, Any]],
    attempts: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    runtime_by = {str(row.get("attempt_name", "")): row for row in runtime_rows}
    gap_by = {str(row.get("attempt_name", "")): row for row in gap_rows}
    usability_by = {str(row.get("attempt_name", "")): row for row in usability_rows}
    boundary_by = {str(row.get("attempt_name", "")): row for row in boundary_rows}
    rows: list[dict[str, Any]] = []
    for attempt in attempts:
        name = str(attempt.get("attempt_name", ""))
        model = str(attempt.get("tester_model", ""))
        gap_status = str(gap_by.get(name, {}).get("gap_status", ""))
        if model == "4" and gap_status == "tester_reached_feature_last":
            read = "real_tick_visibility_repaired_for_next_attribution"
        elif model == "4":
            read = "real_tick_visibility_gap_remains"
        elif gap_status == "tester_reached_feature_last":
            read = "alternative_model_reaches_boundary_only"
        else:
            read = "alternative_model_gap_remains"
        rows.append(
            {
                "attempt_name": name,
                "tester_model": model,
                "tester_model_label": attempt.get("tester_model_label", ""),
                "runtime_completed": runtime_completed(runtime_by.get(name, {})),
                "gap_status": gap_status,
                "feature_last_timestamp": gap_by.get(name, {}).get("feature_last_timestamp", ""),
                "tester_last_observed_bar_time": gap_by.get(name, {}).get("tester_last_observed_bar_time", ""),
                "tester_to_feature_last_gap_minutes": gap_by.get(name, {}).get("tester_to_feature_last_gap_minutes", ""),
                "proxy_matched": usability_by.get(name, {}).get("proxy_matched", ""),
                "proxy_total": usability_by.get(name, {}).get("proxy_total", ""),
                "log_test_to": boundary_by.get(name, {}).get("log_test_to", ""),
                "history_sync_to": boundary_by.get(name, {}).get("history_sync_to", ""),
                "tick_sync_to": boundary_by.get(name, {}).get("tick_sync_to", ""),
                "generated_ticks": boundary_by.get(name, {}).get("generated_ticks", ""),
                "policy_read": read,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def classify(
    attempts: Sequence[Mapping[str, Any]],
    runtime_rows: Sequence[Mapping[str, Any]],
    gap_rows: Sequence[Mapping[str, Any]],
    usability_rows: Sequence[Mapping[str, Any]],
    materialize_only: bool,
) -> tuple[str, str, str, str]:
    if materialize_only:
        return STATUS_MATERIALIZED, JUDGMENT_MATERIALIZED, DECISION_MATERIALIZED, RUN_ID
    runtime_total = len(runtime_rows)
    completed = sum(1 for row in runtime_rows if runtime_completed(row))
    if completed < runtime_total or runtime_total == 0:
        return STATUS_RUNTIME_ISSUE, JUDGMENT_RUNTIME_ISSUE, DECISION_RUNTIME_ISSUE, NEXT_RUN_ID_RUNTIME_REPAIR
    gap_by = {str(row.get("attempt_name", "")): row for row in gap_rows}
    usability_by = {str(row.get("attempt_name", "")): row for row in usability_rows}
    model4_attempts = [attempt for attempt in attempts if str(attempt.get("tester_model", "")) == "4"]
    model4_name = str(model4_attempts[0].get("attempt_name", "")) if model4_attempts else ""
    model4_reached = str(gap_by.get(model4_name, {}).get("gap_status", "")) == "tester_reached_feature_last"
    model4_usable = (
        str(usability_by.get(model4_name, {}).get("proxy_matched", "")) == str(usability_by.get(model4_name, {}).get("proxy_total", ""))
        and str(usability_by.get(model4_name, {}).get("proxy_total", "")) not in {"", "0"}
    )
    alt_reached = any(
        str(gap_by.get(str(attempt.get("attempt_name", "")), {}).get("gap_status", "")) == "tester_reached_feature_last"
        for attempt in attempts
        if str(attempt.get("tester_model", "")) != "4"
    )
    if model4_reached and model4_usable:
        return STATUS_REAL_TICK_REACHED, JUDGMENT_REAL_TICK_REACHED, DECISION_REAL_TICK_REACHED, NEXT_RUN_ID_FULL_ATTRIB
    if alt_reached:
        return STATUS_ALTERNATIVE_BOUNDARY, JUDGMENT_ALTERNATIVE_BOUNDARY, DECISION_ALTERNATIVE_BOUNDARY, NEXT_RUN_ID_MODELING_POLICY
    return STATUS_ALL_GAP, JUDGMENT_ALL_GAP, DECISION_ALL_GAP, NEXT_RUN_ID_REPAIR


def decision_payload(
    status: str,
    judgment: str,
    decision: str,
    next_action: str,
    runtime_rows: Sequence[Mapping[str, Any]],
    gap_rows: Sequence[Mapping[str, Any]],
    usability_rows: Sequence[Mapping[str, Any]],
    matrix_rows: Sequence[Mapping[str, Any]],
    broker_api: Mapping[str, Any],
) -> dict[str, Any]:
    completed = sum(1 for row in runtime_rows if runtime_completed(row))
    reached = sum(1 for row in gap_rows if row.get("gap_status") == "tester_reached_feature_last")
    matched = sum(number(row.get("proxy_matched"), 0.0) for row in usability_rows)
    total = sum(number(row.get("proxy_total"), 0.0) for row in usability_rows)
    model4 = next((row for row in matrix_rows if str(row.get("tester_model", "")) == "4"), {})
    alternatives = [row for row in matrix_rows if str(row.get("tester_model", "")) != "4"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": status,
        "judgment": judgment,
        "decision": decision,
        "next_action": next_action,
        "broker_api_status": broker_api.get("status", ""),
        "broker_api_m5_last_close_utc": broker_api.get("m5_last_close_utc", ""),
        "runtime_completed": completed,
        "runtime_total": len(runtime_rows),
        "tester_reached_feature_last": reached,
        "tester_gap_total": len(gap_rows),
        "model4_real_tick_gap_status": model4.get("gap_status", ""),
        "model4_real_tick_gap_minutes": model4.get("tester_to_feature_last_gap_minutes", ""),
        "alternative_modes_reached_feature_last": sum(1 for row in alternatives if row.get("gap_status") == "tester_reached_feature_last"),
        "alternative_modes_total": len(alternatives),
        "proxy_mt5_matched": int(matched),
        "proxy_mt5_rows": int(total),
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def gate_rows(
    final_decision: Mapping[str, Any],
    runtime_rows: Sequence[Mapping[str, Any]],
    gap_rows: Sequence[Mapping[str, Any]],
    usability_rows: Sequence[Mapping[str, Any]],
    matrix_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    all_runtime_complete = len(runtime_rows) > 0 and all(runtime_completed(row) for row in runtime_rows)
    has_model4 = any(str(row.get("tester_model", "")) == "4" for row in matrix_rows)
    has_alts = sum(1 for row in matrix_rows if str(row.get("tester_model", "")) != "4") >= 3
    proxy_total = sum(number(row.get("proxy_total"), 0.0) for row in usability_rows)
    proxy_matched = sum(number(row.get("proxy_matched"), 0.0) for row in usability_rows)
    gates = [
        ("frozen_identity_lock", "passed", "same ONNX/model/feature/threshold/risk/lot, only tester Model field varied"),
        ("mt5_execution_completed", "passed" if all_runtime_complete else "blocked", "all tester/runtime/report outputs must complete"),
        ("model4_real_tick_control_present", "passed" if has_model4 else "blocked", "real tick control is needed to avoid over-reading generated modes"),
        ("alternative_model_modes_present", "passed" if has_alts else "blocked", "generated alternatives isolate tester visibility policy"),
        ("feature_last_gap_measured", "passed" if len(gap_rows) == len(matrix_rows) and len(gap_rows) > 0 else "blocked", "tester last observed bar is compared with feature_last"),
        ("timestamp_aligned_proxy_mt5_measured", "passed" if proxy_total > 0 else "blocked", "proxy expected values are cut to MT5 observed timestamp"),
        ("timestamp_aligned_proxy_mt5_matched", "passed" if proxy_total > 0 and proxy_matched == proxy_total else "review", "proxy parity is diagnostic, not KPI authority"),
        ("forward_goal_not_claimed", "passed", "Forward Passed/Failed and Goal Achieve stay not_claimed"),
    ]
    return [
        {
            "gate_name": name,
            "status": status,
            "evidence_path": rel(RUN_DIR),
            "effect": effect,
            "final_status": final_decision.get("status", ""),
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for name, status, effect in gates
    ]


def receipt_payloads(final_decision: Mapping[str, Any], matrix_rows: Sequence[Mapping[str, Any]]) -> dict[Path, Mapping[str, Any]]:
    common = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": final_decision.get("status", ""),
        "decision": final_decision.get("decision", ""),
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return {
        RUN_DIR / "data_integrity_receipt.json": {
            **common,
            "receipt_type": "data_integrity",
            "effect": "US100 API visibility and tester observed window are recorded before judging forward data.",
        },
        RUN_DIR / "runtime_parity_receipt.json": {
            **common,
            "receipt_type": "runtime_parity",
            "proxy_mt5_matched": final_decision.get("proxy_mt5_matched", 0),
            "proxy_mt5_rows": final_decision.get("proxy_mt5_rows", 0),
            "effect": "Python proxy and MT5 runtime are compared at the same observed timestamp.",
        },
        RUN_DIR / "model_validation_receipt.json": {
            **common,
            "receipt_type": "model_validation",
            "model_training": "forbidden_not_performed",
            "threshold_retuning": "forbidden_not_performed",
            "tester_models": [row.get("tester_model") for row in matrix_rows],
            "effect": "The probe diagnoses tester visibility without fitting a new candidate.",
        },
        RUN_DIR / "result_judgment_receipt.json": {
            **common,
            "receipt_type": "result_judgment",
            "judgment": final_decision.get("judgment", ""),
            "effect": "The result is bounded to visibility repair and cannot become Forward Passed/Failed.",
        },
        RUN_DIR / "experiment_design_receipt.json": {
            **common,
            "receipt_type": "experiment_design",
            "hypothesis": "If generated tester modes reach feature_last while real ticks do not, the blocker is likely real-tick history/cache boundary.",
            "stop_condition": "Do not retune model, threshold, D/B rules, lot, risk, or ATR exits.",
            "effect": "The next run is chosen from evidence rather than KPI-chasing.",
        },
    }


def report_text(final_decision: Mapping[str, Any], matrix_rows: Sequence[Mapping[str, Any]], kpi_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "# Stage337AI Tester Visibility Alternative Repair Or Rollover Reprobe(337AI 테스터 가시성 대체 수리 또는 이월 재탐침)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- parent_run_id(상위 실행 ID): `{PARENT_RUN_ID}`",
        f"- status(상태): `{final_decision['status']}`",
        f"- judgment(판정): `{final_decision['judgment']}`",
        f"- decision(결정): `{final_decision['decision']}`",
        f"- next_action(다음 행동): `{final_decision['next_action']}`",
        "- Forward Passed(전방 통과): `not_claimed`",
        "- Forward Failed(전방 실패): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Meaning(의미)",
        "",
        "이번 실행은 같은 frozen ONNX(고정 ONNX), feature order(피처 순서), D/B decision surface(D/B 결정 표면), threshold(임계값), risk/lot(위험/로트), ATR SL/TP(ATR 손절/익절)을 유지했다.",
        "바꾼 것은 MT5 Strategy Tester Model(전략 테스터 모델) 값뿐이다. 효과(effect, 효과)는 full current-day(현재일 전체) 가시성 공백이 real tick history/cache(실제 틱 이력/캐시) 때문인지 좁히는 것이다.",
        "",
        "## Model Mode Matrix(모델 방식 행렬)",
        "",
        "| attempt(시도) | model(모델) | label(라벨) | gap(공백) | last observed(마지막 관측) | feature last(피처 끝) | proxy(프록시) | read(판독) |",
        "|---|---:|---|---|---|---|---:|---|",
    ]
    for row in matrix_rows:
        lines.append(
            f"| `{row.get('attempt_name', '')}` | `{row.get('tester_model', '')}` | `{row.get('tester_model_label', '')}` | "
            f"`{row.get('gap_status', '')}` | `{row.get('tester_last_observed_bar_time', '')}` | "
            f"`{row.get('feature_last_timestamp', '')}` | `{row.get('proxy_matched', '')}/{row.get('proxy_total', '')}` | "
            f"`{row.get('policy_read', '')}` |"
        )
    lines.extend(
        [
            "",
            "## KPI Snapshot(KPI 스냅샷)",
            "",
            "KPI(핵심 지표)는 진단 참고값이며, generated model mode(생성 모델 방식) 결과는 forward authority(전방 권위)가 아니다.",
            "",
            "| attempt(시도) | model(모델) | net(순익) | PF(수익 팩터) | trades(거래) | DD(손실폭) |",
            "|---|---:|---:|---:|---:|---:|",
        ]
    )
    for row in kpi_rows:
        lines.append(
            f"| `{row.get('attempt_name', '')}` | `{row.get('tester_model', '')}` | `{row.get('net_profit', '')}` | "
            f"`{row.get('profit_factor', '')}` | `{row.get('trade_count', '')}` | `{row.get('max_drawdown_amount', '')}` |"
        )
    lines.extend(
        [
            "",
            "## Boundary(경계)",
            "",
            "- selected_candidate(선택 후보): `none`",
            "- model_training(모델 학습): `forbidden_not_performed`",
            "- threshold_retuning(임계값 재조정): `forbidden_not_performed`",
            "- lot_optimization(로트 최적화): `forbidden_not_performed`",
            "- live_readiness(실거래 준비): `not_claimed`",
            "- runtime_authority(런타임 권위): `not_claimed`",
            "",
            "Effect(효과): 이 보고서는 다음 수리/판정 경로를 고르는 근거이며, Forward Passed/Failed(전방 통과/실패)를 닫지 않는다.",
        ]
    )
    return "\n".join(lines)


def decision_doc_text(final_decision: Mapping[str, Any]) -> str:
    return "\n".join(
        [
            "# 2026-05-27 Stage337AI Decision(337AI 결정)",
            "",
            f"- run_id(실행 ID): `{RUN_ID}`",
            f"- status(상태): `{final_decision['status']}`",
            f"- judgment(판정): `{final_decision['judgment']}`",
            f"- decision(결정): `{final_decision['decision']}`",
            f"- next_action(다음 행동): `{final_decision['next_action']}`",
            f"- model4_real_tick_gap_status(real tick 대조 공백 상태): `{final_decision['model4_real_tick_gap_status']}`",
            f"- alternative_modes_reached_feature_last(대체 방식 feature_last 도달): `{final_decision['alternative_modes_reached_feature_last']}/{final_decision['alternative_modes_total']}`",
            f"- proxy_mt5_parity(프록시/MT5 동등성): `{final_decision['proxy_mt5_matched']}/{final_decision['proxy_mt5_rows']}`",
            "- Forward Passed(전방 통과): `not_claimed`",
            "- Forward Failed(전방 실패): `not_claimed`",
            "- Goal Achieve(목표 달성): `not_claimed`",
            "",
            "Effect(효과): tester model mode(테스터 모델 방식) 경계만 판단했고, 후보 선택이나 운영 주장은 열지 않는다.",
        ]
    )


def replace_line(text: str, prefix: str, replacement: str) -> str:
    if re.search(rf"^{re.escape(prefix)}.*$", text, flags=re.M):
        return re.sub(rf"^{re.escape(prefix)}.*$", replacement, text, count=1, flags=re.M)
    return text.rstrip() + "\n" + replacement + "\n"


def upsert_focus_block(text: str, block: str) -> str:
    pattern = r"- >-\n  Stage337 run337AI focus complete:.*?(?=\n- >-|\Z)"
    replacement = "- >-\n  " + block.replace("\n", "\n  ")
    if re.search(pattern, text, flags=re.S):
        return re.sub(pattern, replacement, text, count=1, flags=re.S)
    if "current_focus:\n" in text:
        return text.replace("current_focus:\n", "current_focus:\n" + replacement + "\n", 1)
    return text.rstrip() + "\ncurrent_focus:\n" + replacement + "\n"


def update_status_docs(final_decision: Mapping[str, Any]) -> list[Path]:
    changed: list[Path] = []
    selected_text = f"""# Stage337 Selection Status(337단계 선택 상태)

- stage_id(단계 ID): `{STAGE_ID}`
- stage_status(단계 상태): `open_active`
- selected_candidate(선택 후보): `none`
- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final_decision['decision']}`
- current_run(현재 실행): `{final_decision['next_action']}`
- parent_run(상위 실행): `{PARENT_RUN_ID}`
- model4_real_tick_gap_status(real tick 대조 공백 상태): `{final_decision['model4_real_tick_gap_status']}`
- model4_real_tick_gap_minutes(real tick 공백 분): `{final_decision['model4_real_tick_gap_minutes']}`
- alternative_modes_reached_feature_last(대체 방식 feature_last 도달): `{final_decision['alternative_modes_reached_feature_last']}/{final_decision['alternative_modes_total']}`
- proxy_mt5_parity(프록시/MT5 동등성): `{final_decision['proxy_mt5_matched']}/{final_decision['proxy_mt5_rows']}`
- Forward Passed(전방 통과): `not_claimed`
- Forward Failed(전방 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final_decision['next_action']}`
- effect(효과): run337AI(337AI 실행)는 tester model mode(테스터 모델 방식)만 바꿔 visibility boundary(가시성 경계)를 재탐침했다. Forward/Goal(전방/목표)은 주장하지 않는다.
"""
    changed.append(write_md(SELECTED_STATUS, selected_text))

    focus = (
        f"Stage337 run337AI focus complete: run337AI(337AI 실행)는 `{final_decision['status']}`로 "
        f"tester visibility model-mode reprobe(테스터 가시성 모델 방식 재탐침)를 완료했다. "
        f"Effect(효과): model4 real tick gap(모델4 실제 틱 공백) `{final_decision['model4_real_tick_gap_status']}`, "
        f"alternative reached(대체 방식 도달) `{final_decision['alternative_modes_reached_feature_last']}/{final_decision['alternative_modes_total']}`, "
        f"proxy/MT5 parity(프록시/MT5 동등성) `{final_decision['proxy_mt5_matched']}/{final_decision['proxy_mt5_rows']}`이고 Forward/Goal(전방/목표)은 주장하지 않는다."
    )
    if path_exists(WORKSPACE_STATE):
        text, bom = read_text(WORKSPACE_STATE)
        text = replace_line(text, "current_run_id:", f"current_run_id: {final_decision['next_action']}")
        text = replace_line(text, "updated_on:", f"updated_on: '{TODAY}'")
        text = upsert_focus_block(text, focus)
        changed.append(write_text(WORKSPACE_STATE, text, bom))
    if path_exists(CURRENT_STATE):
        text, bom = read_text(CURRENT_STATE)
        entry = f"""## Stage337 run337AI(337AI 실행) - {TODAY}

- status(상태): `{final_decision['status']}`
- decision(결정): `{final_decision['decision']}`
- next_action(다음 행동): `{final_decision['next_action']}`
- effect(효과): tester model mode(테스터 모델 방식) 경계를 재탐침했고 Forward Passed/Failed(전방 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.
"""
        if "## Stage337 run337AI(337AI 실행)" in text:
            text = re.sub(r"## Stage337 run337AI\(337AI 실행\).*?(?=\n## |\Z)", entry.strip(), text, count=1, flags=re.S)
        else:
            text = text.rstrip() + "\n\n" + entry.strip() + "\n"
        changed.append(write_text(CURRENT_STATE, text, bom))
    if path_exists(CHANGELOG):
        text, bom = read_text(CHANGELOG)
        line = (
            f"- {TODAY}: Stage337 run337AI(337AI 실행) `{final_decision['status']}`. "
            f"Effect(효과): tester model mode(테스터 모델 방식) visibility(가시성)를 재탐침했고 Forward/Goal(전방/목표)은 주장하지 않음."
        )
        if "Stage337 run337AI(337AI 실행)" not in text:
            text = text.rstrip() + "\n" + line + "\n"
        changed.append(write_text(CHANGELOG, text, bom))
    if path_exists(STAGE_BRIEF):
        text, bom = read_text(STAGE_BRIEF)
        text = re.sub(r"- latest_run\([^)]*\): `[^`]*`", f"- latest_run(최신 실행): `{RUN_ID}`", text, count=1)
        summary = (
            f"- run337AI_summary(337AI 요약): `{final_decision['status']}`. "
            f"Effect(효과): model4 gap(모델4 공백) `{final_decision['model4_real_tick_gap_status']}`, "
            f"alternative reached(대체 방식 도달) `{final_decision['alternative_modes_reached_feature_last']}/{final_decision['alternative_modes_total']}`, "
            f"proxy parity(프록시 동등성) `{final_decision['proxy_mt5_matched']}/{final_decision['proxy_mt5_rows']}`를 기록했다.\n"
        )
        if "run337AI_summary(337AI 요약)" in text:
            text = re.sub(r"- run337AI_summary\(337AI 요약\): [^\n]*(?:\n|$)", summary, text, count=1)
        else:
            text = text.rstrip() + "\n" + summary
        changed.append(write_text(STAGE_BRIEF, text, bom))
    return changed


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


def update_registers(final_decision: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "tester_visibility_model_mode_reprobe",
        "status": final_decision["status"],
        "judgment": final_decision["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"decision={final_decision['decision']};next_action={final_decision['next_action']};goal_achieve_not_claimed.",
        "family": "runtime_parity_repair",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__tester_visibility_model_mode_reprobe",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "tester_visibility_model_mode_reprobe",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "runtime_visibility_repair",
        "tier_scope": "Tier A forward runtime probe with tester model-mode boundary(티어 A 전방 런타임 탐침, 테스터 모델 방식 경계)",
        "kpi_scope": "diagnostic_runtime_probe_no_selection(진단 런타임 탐침, 선택 없음)",
        "scoreboard_lane": "runtime_parity_repair",
        "status": final_decision["status"],
        "judgment": final_decision["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"model4_gap={final_decision['model4_real_tick_gap_status']};proxy_mt5={final_decision['proxy_mt5_matched']}/{final_decision['proxy_mt5_rows']}",
        "guardrail_kpi": "no_training;no_threshold_retune;no_lot_opt;generated_modes_not_kpi_authority",
        "external_verification_status": "mt5_strategy_tester_attempted",
        "notes": f"decision={final_decision['decision']};next_action={final_decision['next_action']};goal_achieve_not_claimed.",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__tester_visibility_model_mode_reprobe",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "runtime_parity_repair",
        "evidence_scope": "MT5 tester logs, runtime telemetry, timestamp-aligned proxy parity",
        "kpi_scope": "diagnostic_runtime_probe_not_forward_kpi",
        "status": final_decision["status"],
        "judgment": final_decision["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={final_decision['next_action']};goal_achieve_not_claimed.",
        "decision": final_decision["decision"],
        "run_key": f"{RUN_ID}__tester_visibility_model_mode_reprobe",
        "family": "tester_visibility_model_mode_reprobe",
        "question": "does changing only tester Model isolate the full current-day feature_last gap",
        "metric_scope": "tester_visibility_proxy_mt5_parity_no_forward_decision",
        "primary_artifact": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "next_action": final_decision["next_action"],
    }
    return [
        upsert_csv(RUN_REGISTRY, ["run_id"], run_row),
        upsert_csv(ALPHA_LEDGER, ["ledger_row_id"], alpha_row),
        upsert_csv(STAGE_LEDGER, ["run_key"], stage_row),
    ]


def append_artifacts(paths: Sequence[Path], final_decision: Mapping[str, Any]) -> Path:
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
                "notes": final_decision.get("status", ""),
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
    for directory in (RUN_DIR, MT5_DIR, FEATURE_COPY_DIR, MODEL_COPY_DIR, TELEMETRY_DIR):
        io_path(directory).mkdir(parents=True, exist_ok=True)

    source = load_source_u42()
    prepared = build_source_attempts(source)
    broker_api = ab.mt5_api_symbol_visibility(terminal_path, ORIGIN_SYMBOL)
    pre_tester_recovery = qprobe.stop_target_terminal_if_running(terminal_path)
    attempts, handoff_rows, materialized_artifacts = base.build_attempts(prepared, common_files_root)
    scenario_by_attempt = {str(row["attempt_name"]): row for row in prepared}
    for attempt in attempts:
        scenario = scenario_by_attempt.get(str(attempt["attempt_name"]), {})
        for key in ("scenario_id", "scenario_symbol", "scenario_from_date", "scenario_to_date", "scenario_model", "tester_model_label"):
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
    execution_result["pre_tester_recovery"] = pre_tester_recovery

    runtime_rows = base.build_fresh_runtime_summary(attempts, execution_result)
    copied_runtime_artifacts = base.copy_runtime_outputs(common_files_root, attempts)
    feature_rows = qprobe.feature_last_rows(attempts)
    gap_rows = qprobe.tester_gap_rows(runtime_rows, feature_rows, common_files_root, {"last_close_utc": broker_api.get("m5_last_close_utc", "")})
    boundary_rows = ab.parse_tester_boundary_rows(before_offsets, attempts)
    boundary_by_attempt = {row["attempt_name"]: row for row in boundary_rows}
    for row in gap_rows:
        row["scenario_id"] = boundary_by_attempt.get(row.get("attempt_name"), {}).get("scenario_id", "")
        row["tester_symbol"] = boundary_by_attempt.get(row.get("attempt_name"), {}).get("tester_symbol", "")
        row["tester_model"] = next((attempt.get("tester_model", "") for attempt in attempts if attempt.get("attempt_name") == row.get("attempt_name")), "")
    cutoff_by_attempt = {str(row.get("attempt_name", "")): str(row.get("tester_last_observed_bar_time", "")) for row in gap_rows}
    aligned_proxy_rows = qprobe.sanitize_proxy_rows(
        qprobe.build_timestamp_aligned_proxy_rows(attempts, cutoff_by_attempt),
        default_source="stage337AI_timestamp_aligned_python_onnx_inference",
    )
    diff_rows = base.build_signal_difference_rows(aligned_proxy_rows, runtime_rows)
    for row in diff_rows:
        row["mt5_source"] = "stage337AI_runtime_summary_model_mode_reprobe"
        row["usable_for_forward_pass_fail"] = False
        row["claim_boundary"] = CLAIM_BOUNDARY
    usability = proxy_usability_rows(gap_rows, diff_rows, attempts)
    kpis = runtime_kpi_rows(runtime_rows, attempts)
    matrix = model_mode_matrix_rows(runtime_rows, gap_rows, usability, boundary_rows, attempts)
    status, judgment, decision, next_action = classify(attempts, runtime_rows, gap_rows, usability, args.materialize_only)
    final_decision = decision_payload(status, judgment, decision, next_action, runtime_rows, gap_rows, usability, matrix, broker_api)
    gates = gate_rows(final_decision, runtime_rows, gap_rows, usability, matrix)

    artifacts: list[Path] = [
        write_json(RUN_DIR / "pre_tester_terminal_recovery.json", pre_tester_recovery),
        write_json(RUN_DIR / "execution_result.json", execution_result),
        write_json(RUN_DIR / "final_model_mode_reprobe_decision.json", final_decision),
        write_csv(RUN_DIR / "mt5_api_visibility.csv", columns_for([broker_api], ["status"]), [broker_api]),
        write_csv(RUN_DIR / "handoff_attempts.csv", columns_for(handoff_rows, ["status"]), handoff_rows),
        write_json(RUN_DIR / "handoff_attempts.json", attempts),
        write_csv(RUN_DIR / "runtime_summary.csv", columns_for(runtime_rows, ["status"]), runtime_rows),
        write_csv(RUN_DIR / "runtime_kpi_snapshot.csv", columns_for(kpis, ["status"]), kpis),
        write_csv(RUN_DIR / "feature_last_timestamp_audit.csv", columns_for(feature_rows, ["status"]), feature_rows),
        write_csv(RUN_DIR / "tester_boundary_model_mode_reprobe.csv", columns_for(boundary_rows, ["status"]), boundary_rows),
        write_csv(RUN_DIR / "tester_feature_last_gap_model_mode_reprobe.csv", columns_for(gap_rows, ["status"]), gap_rows),
        write_csv(RUN_DIR / "timestamp_aligned_proxy_expected_result.csv", columns_for(aligned_proxy_rows, ["status"]), aligned_proxy_rows),
        write_csv(RUN_DIR / "timestamp_aligned_proxy_mt5_difference.csv", columns_for(diff_rows, ["status"]), diff_rows),
        write_csv(RUN_DIR / "proxy_mt5_usability_model_mode.csv", columns_for(usability, ["status"]), usability),
        write_csv(RUN_DIR / "model_mode_repair_matrix.csv", columns_for(matrix, ["status"]), matrix),
        write_csv(RUN_DIR / "required_gate_coverage_audit.csv", columns_for(gates, ["status"]), gates),
        write_md(REPORT_PATH, report_text(final_decision, matrix, kpis)),
        write_md(DECISION_DOC, decision_doc_text(final_decision)),
        *materialized_artifacts,
        *copied_runtime_artifacts,
    ]
    for path, payload in receipt_payloads(final_decision, matrix).items():
        artifacts.append(write_json(path, payload))
    artifacts.extend(update_status_docs(final_decision))
    artifacts.extend(update_registers(final_decision))
    manifest = write_json(
        RUN_DIR / "run_manifest.json",
        {
            **final_decision,
            "generated_at_utc": now_utc(),
            "command": "python stage_pipelines/stage337/reprobe_tester_visibility_alternative_repair_or_rollover.py",
            "materialize_only": bool(args.materialize_only),
            "primary_family": "runtime_parity_repair",
            "primary_skill": "obsidian-runtime-parity",
            "support_skills": ["obsidian-data-integrity", "obsidian-model-validation", "obsidian-result-judgment"],
            "artifacts": [rel(path) for path in artifacts if path_exists(path)],
        },
    )
    artifacts.append(manifest)
    artifacts.append(append_artifacts([*artifacts, Path(__file__)], final_decision))
    print(json.dumps(final_decision, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
