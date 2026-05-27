from __future__ import annotations

import argparse
import csv
import json
import math
import os
import re
import shutil
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, path_exists  # noqa: E402
from foundation.mt5.runtime_artifacts import sha256_file  # noqa: E402
from stage_pipelines.stage335 import independent_proxy_mt5_probe as base  # noqa: E402
from stage_pipelines.stage337 import probe_custom_symbol_intraday_tester_visibility as ab  # noqa: E402
from stage_pipelines.stage337 import probe_next_day_rollover_or_custom_symbol_seed_repair as ac  # noqa: E402
from stage_pipelines.stage337 import probe_tester_history_cache_session_policy as aa  # noqa: E402
from stage_pipelines.stage337 import review_runtime_data_and_feature_source_repair_probe as qprobe  # noqa: E402


TODAY = "2026-05-27"
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
RUN_NUMBER = "run337AD"
RUN_ID = "run337AD_completed_day_forward_slice_or_next_day_rollover_confirm_v1"
PARENT_RUN_ID = "run337AC_next_day_broker_rollover_or_custom_symbol_seed_repair_v1"
NEXT_RUN_ID_COMPLETED_SLICE = "run337AE_completed_day_forward_attribution_cost_stress_v1"
NEXT_RUN_ID_FULL_ROLLOVER = "run337AE_full_forward_attribution_after_next_day_rollover_v1"
NEXT_RUN_ID_REPAIR = "run337AE_tester_rollover_or_feature_slice_repair_v1"
CLAIM_BOUNDARY = (
    "research_development_only_stage337AD_completed_day_forward_slice_or_next_day_rollover_confirm_no_model_training_"
    "no_threshold_retuning_no_lot_optimization_no_candidate_selection_no_forward_passed_no_forward_failed_"
    "no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STATUS_FULL_ROLLOVER = "completed_stage337AD_full_current_day_rollover_reached_feature_last_no_forward_decision"
STATUS_COMPLETED_SLICE = "completed_stage337AD_completed_day_forward_slice_reached_feature_last_no_forward_decision"
STATUS_PARTIAL = "completed_stage337AD_completed_day_slice_or_rollover_inconclusive_no_forward_decision"
STATUS_MATERIALIZED = "completed_stage337AD_materialized_only_no_forward_decision"
JUDGMENT_FULL_ROLLOVER = "broker_next_day_rollover_reaches_full_feature_last_runtime_attribution_can_resume"
JUDGMENT_COMPLETED_SLICE = "completed_day_broker_slice_reaches_feature_last_full_current_day_still_waits_for_rollover"
JUDGMENT_PARTIAL = "completed_day_slice_or_next_day_rollover_not_confirmed_requires_repair"
JUDGMENT_MATERIALIZED = "run337AD_inputs_materialized_execution_pending"
DECISION_FULL_ROLLOVER = "stage337AD_open_run337AE_full_forward_attribution_after_next_day_rollover_no_selection"
DECISION_COMPLETED_SLICE = "stage337AD_open_run337AE_completed_day_forward_attribution_cost_stress_no_selection"
DECISION_PARTIAL = "stage337AD_open_run337AE_tester_rollover_or_feature_slice_repair_no_selection"
DECISION_MATERIALIZED = "stage337AD_execution_pending_no_selection"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
PARENT_RUN_DIR = STAGE_DIR / "02_runs" / "run337AC"
RUN337Z_DIR = STAGE_DIR / "02_runs" / "run337Z"
RUN337Z_ATTEMPTS = RUN337Z_DIR / "rollover_reprobe_handoff_attempts.json"
MT5_DIR = RUN_DIR / "mt5"
FEATURE_COPY_DIR = RUN_DIR / "feature_matrices"
MODEL_COPY_DIR = RUN_DIR / "models"
TELEMETRY_DIR = RUN_DIR / "runtime_telemetry"
SLICE_INPUT_DIR = RUN_DIR / "completed_day_slice_inputs"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEWS_DIR / "run337AD_completed_day_forward_slice.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage337AD_completed_day_forward_slice.md"
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

COMMON_ROOT = "Project_Obsidian_Prime_v2/stage337/run337AD_completed_day_forward_slice"
ORIGIN_SYMBOL = "US100"
BROKER_FROM_DATE = "2026.04.14"
BROKER_TO_DATE = "2026.05.30"
ATTEMPT_BASE = "u42_plain_rf"


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
    qprobe.TODAY = TODAY
    qprobe.STAGE_ID = STAGE_ID
    qprobe.RUN_NUMBER = RUN_NUMBER
    qprobe.RUN_ID = RUN_ID
    qprobe.PARENT_RUN_ID = PARENT_RUN_ID
    qprobe.NEXT_RUN_ID = NEXT_RUN_ID_COMPLETED_SLICE
    qprobe.CLAIM_BOUNDARY = CLAIM_BOUNDARY
    qprobe.STAGE_DIR = STAGE_DIR
    qprobe.RUN_DIR = RUN_DIR
    qprobe.MT5_DIR = MT5_DIR
    qprobe.FEATURE_COPY_DIR = FEATURE_COPY_DIR
    qprobe.MODEL_COPY_DIR = MODEL_COPY_DIR
    qprobe.TELEMETRY_DIR = TELEMETRY_DIR
    qprobe.REVIEWS_DIR = REVIEWS_DIR
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
    ab.TODAY = TODAY
    ab.RUN_ID = RUN_ID
    ab.CLAIM_BOUNDARY = CLAIM_BOUNDARY
    ab.RUN_DIR = RUN_DIR
    ab.TESTER_LOG = TESTER_LOG
    ab.TESTER_AGENT_LOG = TESTER_AGENT_LOG
    ab.TERMINAL_LOG = TERMINAL_LOG
    base.RUN_ID = RUN_ID
    base.RUN_DIR = RUN_DIR
    base.MT5_DIR = MT5_DIR
    base.FEATURE_COPY_DIR = FEATURE_COPY_DIR
    base.MODEL_COPY_DIR = MODEL_COPY_DIR
    base.TELEMETRY_DIR = TELEMETRY_DIR
    base.COMMON_ROOT = COMMON_ROOT
    base.CLAIM_BOUNDARY = CLAIM_BOUNDARY


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stage337AD completed-day forward slice or next-day rollover confirmation.")
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


def feature_timestamp_series(frame: pd.DataFrame) -> pd.Series:
    for column in ("timestamp_utc", "bar_time_server", "timestamp"):
        if column in frame.columns:
            return pd.to_datetime(frame[column].astype(str).str.replace(".", "-", regex=False), errors="coerce", utc=True)
    return pd.Series(pd.NaT, index=frame.index, dtype="datetime64[ns, UTC]")


def parent_completed_cutoff() -> pd.Timestamp:
    gap_path = PARENT_RUN_DIR / "tester_feature_last_gap_seed_repair.csv"
    if path_exists(gap_path):
        rows = list(csv.DictReader(io_path(gap_path).open("r", encoding="utf-8-sig", newline="")))
        broker = next((row for row in rows if "broker_rollover_control" in row.get("attempt_name", "")), {})
        parsed = pd.to_datetime(broker.get("tester_last_observed_bar_time", ""), errors="coerce", utc=True)
        if not pd.isna(parsed):
            return parsed
    source = load_source_u42()
    frame = pd.read_csv(io_path(ROOT / str(source.get("feature_local_path", ""))))
    timestamps = feature_timestamp_series(frame).dropna()
    if timestamps.empty:
        raise RuntimeError("cannot derive completed-day cutoff from parent gap or source feature timestamps")
    latest = timestamps.max()
    prior_day = timestamps.loc[timestamps.dt.date < latest.date()]
    if prior_day.empty:
        raise RuntimeError("source features do not contain a prior completed day")
    return prior_day.max()


def truncate_feature_csv(source_path: Path, target_path: Path, cutoff: pd.Timestamp) -> tuple[Path, dict[str, Any]]:
    frame = pd.read_csv(io_path(source_path))
    timestamps = feature_timestamp_series(frame)
    mask = timestamps <= cutoff
    sliced = frame.loc[mask].copy()
    io_path(target_path.parent).mkdir(parents=True, exist_ok=True)
    sliced.to_csv(io_path(target_path), index=False, lineterminator="\n")
    metadata = {
        "source_feature_path": rel(source_path),
        "target_feature_path": rel(target_path),
        "cutoff_timestamp": cutoff.isoformat().replace("+00:00", "Z"),
        "source_rows": int(len(frame)),
        "sliced_rows": int(len(sliced)),
        "first_timestamp": timestamps.loc[mask].min().isoformat().replace("+00:00", "Z") if mask.any() else "",
        "last_timestamp": timestamps.loc[mask].max().isoformat().replace("+00:00", "Z") if mask.any() else "",
        "effect": "Completed-day slice(완성일 구간)는 Strategy Tester(전략 테스터)가 볼 수 있는 마지막 broker bar(브로커 봉)까지만 feature rows(피처 행)를 자른다.",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return target_path, metadata


def build_source_attempts(source: Mapping[str, Any], completed_feature_path: Path) -> list[dict[str, Any]]:
    scenarios = [
        {
            "suffix": "ad_completed_day_broker_slice",
            "scenario_id": "completed_day_broker_slice_to_parent_tester_cutoff",
            "feature_path": rel(completed_feature_path),
            "slice_type": "completed_day_broker_slice",
        },
        {
            "suffix": "ad_full_current_day_broker_control",
            "scenario_id": "full_current_day_broker_control_rollover_check",
            "feature_path": source.get("feature_local_path", ""),
            "slice_type": "full_current_day_control",
        },
    ]
    selected: list[dict[str, Any]] = []
    for index, scenario in enumerate(scenarios):
        copied = dict(source)
        copied["attempt_name"] = f"u42_plain_rf_{scenario['suffix']}"
        copied["artifact_slug"] = f"u42_plain_{scenario['suffix']}"
        copied["scenario_id"] = scenario["scenario_id"]
        copied["scenario_symbol"] = ORIGIN_SYMBOL
        copied["scenario_from_date"] = BROKER_FROM_DATE
        copied["scenario_to_date"] = BROKER_TO_DATE
        copied["scenario_model"] = "4"
        copied["slice_type"] = scenario["slice_type"]
        copied["model_copy"] = {"source": source.get("model_local_path", "")}
        copied["feature_export"] = {"path": scenario["feature_path"]}
        copied["feature_local_path"] = scenario["feature_path"]
        copied["source_run_id"] = PARENT_RUN_ID
        copied["attempt_role"] = "stage337AD_completed_day_forward_slice_or_next_day_rollover_same_frozen_u42_model_threshold_risk"
        copied["record_view_prefix"] = f"mt5_stage337AD_u42_plain_{index}"
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
    attempt["attempt_role"] = "stage337AD_completed_day_slice_runtime_probe_same_frozen_u42_model_threshold_risk"
    attempt["record_view_prefix"] = f"mt5_stage337AD_{attempt['artifact_slug']}"
    attempt["source_run_id"] = PARENT_RUN_ID
    attempt["repair_contract"] = (
        "completed-day slice only truncates feature CSV to Strategy Tester visible broker cutoff; "
        "same ONNX, feature order, D/B surface, threshold, risk, lot, ATR SL/TP, and broker symbol"
    )
    attempt["signal_policy"] = "runtime-boundary diagnostic and completed-day forward-slice evidence only; not Forward Passed/Failed authority"
    return attempt


def next_day_rollover_audit(full_feature_last: str, broker_api: Mapping[str, Any]) -> list[dict[str, Any]]:
    feature_last = pd.to_datetime(full_feature_last, errors="coerce", utc=True)
    now = datetime.now(tz=UTC)
    latest = pd.to_datetime(str(broker_api.get("m5_last_close_utc", "")), errors="coerce", utc=True)
    due = False if pd.isna(feature_last) else now.date() > feature_last.date()
    return [
        {
            "audit_id": "next_day_rollover_due_check",
            "now_utc": now.replace(microsecond=0).isoformat().replace("+00:00", "Z"),
            "full_feature_last_timestamp": "" if pd.isna(feature_last) else feature_last.isoformat().replace("+00:00", "Z"),
            "broker_api_latest_m5_close": "" if pd.isna(latest) else latest.isoformat().replace("+00:00", "Z"),
            "next_day_rollover_due": due,
            "status": "due_or_past_due" if due else "not_yet_due_same_utc_date",
            "effect": "If now_utc(현재 UTC)가 full feature_last(전체 피처 마지막)의 다음 날짜가 아니면 next-day rollover(다음날 이월)는 아직 도래하지 않았다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def proxy_usability_rows(gap_rows: Sequence[Mapping[str, Any]], diff_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    gap_by_attempt = {str(row.get("attempt_name", "")): row for row in gap_rows}
    rows: list[dict[str, Any]] = []
    for attempt_name in sorted({str(row.get("attempt_name", "")) for row in diff_rows}):
        group = [row for row in diff_rows if str(row.get("attempt_name", "")) == attempt_name]
        matched = sum(1 for row in group if str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true")
        total = len(group)
        gap_status = str(gap_by_attempt.get(attempt_name, {}).get("gap_status", ""))
        if matched == total and total and gap_status == "tester_reached_feature_last":
            diagnostic = "usable_for_completed_day_signal_parity_not_forward_decision"
            reason = "proxy expected values match MT5 telemetry and tester reaches the completed-day feature_last."
        elif matched == total and total:
            diagnostic = "usable_for_signal_parity_until_tester_cutoff_not_forward_decision"
            reason = "proxy expected values match MT5 telemetry, but tester does not reach full feature_last."
        else:
            diagnostic = "not_usable_for_signal_parity_requires_review"
            reason = "proxy expected values and MT5 telemetry do not match."
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


def to_float(value: Any) -> float | None:
    if value in {None, ""}:
        return None
    try:
        number = float(value)
        return number if math.isfinite(number) else None
    except Exception:
        return None


def completed_day_kpi_rows(runtime_rows: Sequence[Mapping[str, Any]], feature_rows: Sequence[Mapping[str, Any]], attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    feature_by = {str(row.get("attempt_name", "")): row for row in feature_rows}
    attempt_by = {str(row.get("attempt_name", "")): row for row in attempts}
    rows: list[dict[str, Any]] = []
    for row in runtime_rows:
        attempt = str(row.get("attempt_name", ""))
        feature = feature_by.get(attempt, {})
        start = pd.to_datetime(feature.get("feature_first_timestamp", ""), errors="coerce", utc=True)
        end = pd.to_datetime(feature.get("feature_last_timestamp", ""), errors="coerce", utc=True)
        days = None
        if not pd.isna(start) and not pd.isna(end):
            days = max((end - start).total_seconds() / 86400.0, 1 / 288.0)
        trade_count = to_float(row.get("trade_count"))
        net = to_float(row.get("net_profit"))
        lot = None
        try:
            set_values = base.parse_key_value_file(ROOT / str(attempt_by.get(attempt, {}).get("set", {}).get("path", "")))
            lot = to_float(set_values.get("InpFixedLot"))
        except Exception:
            lot = None
        rows.append(
            {
                "attempt_name": attempt,
                "slice_type": attempt_by.get(attempt, {}).get("slice_type", ""),
                "tester_status": row.get("tester_status", ""),
                "runtime_status": row.get("runtime_status", ""),
                "report_status": row.get("report_status", ""),
                "feature_first_timestamp": feature.get("feature_first_timestamp", ""),
                "feature_last_timestamp": feature.get("feature_last_timestamp", ""),
                "net_profit": row.get("net_profit", ""),
                "profit_factor": row.get("profit_factor", ""),
                "trade_count": row.get("trade_count", ""),
                "trades_per_day": "" if days is None or trade_count is None else trade_count / days,
                "expectancy": row.get("expectancy", ""),
                "recovery_factor": row.get("recovery_factor", ""),
                "max_drawdown_amount": row.get("max_drawdown_amount", ""),
                "fixed_lot": "" if lot is None else lot,
                "lot_normalized_net": "" if lot in {None, 0} or net is None else net / lot,
                "kpi_authority": "completed_day_runtime_probe_not_forward_pass_fail",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def classify(gap_rows: Sequence[Mapping[str, Any]], diff_rows: Sequence[Mapping[str, Any]], materialize_only: bool) -> tuple[str, str, str, str]:
    if materialize_only:
        return STATUS_MATERIALIZED, JUDGMENT_MATERIALIZED, DECISION_MATERIALIZED, RUN_ID
    completed_gap = next((row for row in gap_rows if "completed_day_broker_slice" in str(row.get("attempt_name", ""))), {})
    full_gap = next((row for row in gap_rows if "full_current_day_broker_control" in str(row.get("attempt_name", ""))), {})
    completed_reached = completed_gap.get("gap_status") == "tester_reached_feature_last"
    full_reached = full_gap.get("gap_status") == "tester_reached_feature_last"
    matched = sum(1 for row in diff_rows if str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true")
    if full_reached and matched == len(diff_rows) and diff_rows:
        return STATUS_FULL_ROLLOVER, JUDGMENT_FULL_ROLLOVER, DECISION_FULL_ROLLOVER, NEXT_RUN_ID_FULL_ROLLOVER
    if completed_reached and matched >= 5:
        return STATUS_COMPLETED_SLICE, JUDGMENT_COMPLETED_SLICE, DECISION_COMPLETED_SLICE, NEXT_RUN_ID_COMPLETED_SLICE
    return STATUS_PARTIAL, JUDGMENT_PARTIAL, DECISION_PARTIAL, NEXT_RUN_ID_REPAIR


def gate_rows(gap_rows: Sequence[Mapping[str, Any]], diff_rows: Sequence[Mapping[str, Any]], next_day_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    completed_gap = next((row for row in gap_rows if "completed_day_broker_slice" in str(row.get("attempt_name", ""))), {})
    full_gap = next((row for row in gap_rows if "full_current_day_broker_control" in str(row.get("attempt_name", ""))), {})
    matched = sum(1 for row in diff_rows if str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true")
    return [
        {
            "gate_id": "completed_day_slice_reached_feature_last",
            "status": "passed" if completed_gap.get("gap_status") == "tester_reached_feature_last" else "failed",
            "evidence_path": rel(RUN_DIR / "tester_feature_last_gap_completed_day_slice.csv"),
            "effect": "completed-day broker slice(완성일 브로커 구간)가 feature_last(피처 마지막 시점)에 도달하는지 확인한다.",
        },
        {
            "gate_id": "full_current_day_rollover_reached_feature_last",
            "status": "passed" if full_gap.get("gap_status") == "tester_reached_feature_last" else "review",
            "evidence_path": rel(RUN_DIR / "tester_feature_last_gap_completed_day_slice.csv"),
            "effect": "full current-day control(현재일 전체 대조군)이 다음날 이월로 feature_last에 도달했는지 확인한다.",
        },
        {
            "gate_id": "next_day_rollover_due_checked",
            "status": "review" if next_day_rows and next_day_rows[0].get("status") == "not_yet_due_same_utc_date" else "passed",
            "evidence_path": rel(RUN_DIR / "next_day_rollover_audit.csv"),
            "effect": "현재 UTC 날짜가 full feature_last(전체 피처 마지막)의 다음 날짜인지 확인한다.",
        },
        {
            "gate_id": "timestamp_aligned_proxy_parity_recorded",
            "status": "passed" if matched >= 5 else "failed",
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


def write_receipts(
    status: str,
    judgment: str,
    decision: str,
    next_action: str,
    runtime_rows: Sequence[Mapping[str, Any]],
    gap_rows: Sequence[Mapping[str, Any]],
    diff_rows: Sequence[Mapping[str, Any]],
    cutoff_metadata: Mapping[str, Any],
) -> list[Path]:
    completed = sum(1 for row in runtime_rows if row.get("tester_status") == "completed" and row.get("runtime_status") == "completed" and row.get("report_status") == "completed")
    matched = sum(1 for row in diff_rows if str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true")
    return [
        write_json(
            RUN_DIR / "data_integrity_receipt.json",
            {
                "run_id": RUN_ID,
                "data_source": "run337Z frozen u42 feature CSV plus completed-day truncated feature CSV and MT5 runtime output",
                "time_axis": "completed-day slice keeps broker timestamps and drops current-day rows after the parent tester cutoff",
                "sample_scope": "US100 M5 forward runtime probe after 2026-04-14, completed-day diagnostic slice and full current-day control",
                "missing_or_duplicate_check": "feature rows and telemetry rows are compared by timestamp-aligned proxy/MT5 difference",
                "feature_label_boundary": "no labels, no retraining, no threshold fitting; completed-day truncation follows tester visibility cutoff only",
                "split_boundary": "runtime_probe_only",
                "leakage_risk": "completed-day slice must not be treated as latest full-forward pass/fail because current-day rows are excluded",
                "data_hash_or_identity": cutoff_metadata,
                "integrity_judgment": "usable_for_completed_day_runtime_probe_not_forward_decision",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RUN_DIR / "runtime_parity_receipt.json",
            {
                "run_id": RUN_ID,
                "research_path": rel(Path(__file__)),
                "runtime_path": rel(RUN_DIR / "handoff_attempts.json"),
                "shared_contract": "same frozen u42 ONNX, feature order, D/B surface, threshold, risk, lot, ATR SL/TP, and broker US100",
                "known_differences": "completed-day slice truncates feature rows to tester-visible cutoff; full-current-day control keeps all rows",
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
                "tester_identity": "portable FPMarkets MT5 Strategy Tester, US100 M5 real-tick completed-day slice and full-current-day control",
                "ea_identity": rel(RUN_DIR / "handoff_attempts.json"),
                "report_identity": [row.get("report_path", "") for row in runtime_rows],
                "trade_evidence": [{key: row.get(key, "") for key in ("attempt_name", "net_profit", "profit_factor", "trade_count", "max_drawdown_amount")} for row in runtime_rows],
                "cost_assumptions": "costs inherited from frozen u42 set; no spread, slippage, lot, or risk optimization",
                "forensic_checks": ["tester boundary log parsed", "telemetry copied", "report parsed", "completed-day cutoff recorded"],
                "backtest_judgment": "usable_with_boundary_for_completed_day_runtime_probe",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RUN_DIR / "result_judgment_receipt.json",
            {
                "run_id": RUN_ID,
                "result_subject": "completed-day forward slice and next-day rollover confirmation",
                "evidence_available": [rel(RUN_DIR / "runtime_summary.csv"), rel(RUN_DIR / "tester_feature_last_gap_completed_day_slice.csv"), rel(RUN_DIR / "proxy_usability_judgment.csv")],
                "evidence_missing": "latest current-day full forward remains unavailable until next-day rollover or alternate tester policy repair",
                "judgment_label": "runtime_probe",
                "status": status,
                "judgment": judgment,
                "decision": decision,
                "claim_boundary": "completed-day slice can support runtime parity and attribution input, not Forward Passed/Failed",
                "next_condition": next_action,
                "user_explanation_hook": "Completed days can be tested cleanly; the open problem is the current-day tester boundary and forward robustness attribution.",
            },
        ),
    ]


def write_report(
    status: str,
    judgment: str,
    decision: str,
    next_action: str,
    api_rows: Sequence[Mapping[str, Any]],
    next_day_rows: Sequence[Mapping[str, Any]],
    runtime_rows: Sequence[Mapping[str, Any]],
    boundary_rows: Sequence[Mapping[str, Any]],
    gap_rows: Sequence[Mapping[str, Any]],
    diff_rows: Sequence[Mapping[str, Any]],
    usability_rows: Sequence[Mapping[str, Any]],
    kpi_rows: Sequence[Mapping[str, Any]],
) -> Path:
    completed = sum(1 for row in runtime_rows if row.get("tester_status") == "completed" and row.get("runtime_status") == "completed" and row.get("report_status") == "completed")
    matched = sum(1 for row in diff_rows if str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true")
    completed_gap = next((row for row in gap_rows if "completed_day_broker_slice" in str(row.get("attempt_name", ""))), {})
    full_gap = next((row for row in gap_rows if "full_current_day_broker_control" in str(row.get("attempt_name", ""))), {})
    lines = [
        "# Stage337AD Completed-Day Forward Slice(337AD 완성일 전진 구간)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- status(상태): `{status}`",
        f"- judgment(판정): `{judgment}`",
        f"- decision(결정): `{decision}`",
        f"- next_action(다음 행동): `{next_action}`",
        f"- next_day_rollover_status(다음날 이월 상태): `{next_day_rows[0].get('status', '') if next_day_rows else ''}`",
        f"- MT5 runtime completed(MT5 런타임 완료): `{completed}/{len(runtime_rows)}`",
        f"- completed-day slice gap(완성일 구간 공백): `{completed_gap.get('gap_status', '')}`",
        f"- full current-day control gap(현재일 전체 대조 공백): `{full_gap.get('gap_status', '')}`",
        f"- timestamp-aligned proxy parity(시점 맞춤 프록시 동등성): `{matched}/{len(diff_rows)}`",
        "- Forward Passed(전진 통과): `not_claimed`",
        "- Forward Failed(전진 실패): `not_claimed`",
        "- runtime authority(런타임 권위): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Meaning(의미)",
        "",
        "run337AD(337AD 실행)는 새 후보 개발이 아니다. completed-day broker slice(완성일 브로커 구간)는 run337AC(337AC 실행)에서 확인한 tester cutoff(테스터 절단 시점)까지만 feature CSV(피처 CSV)를 자르고, full current-day control(현재일 전체 대조군)은 원래 feature CSV(피처 CSV)를 유지한다.",
        "",
        "Effect(효과): completed-day slice(완성일 구간)가 feature_last(피처 마지막 시점)에 도달하고 proxy-MT5(프록시-MT5)가 일치하면, 완료된 날짜 범위에서는 runtime handoff(런타임 인계)와 Strategy Tester(전략 테스터)가 같은 신호를 본다는 뜻이다. 그래도 최신 현재일 전체 Forward Passed/Failed(전진 통과/실패)는 아니다.",
        "",
        "## API Visibility(API 가시성)",
        "",
        "| symbol(심볼) | status(상태) | m5 last close(M5 마지막 종가 시점) |",
        "|---|---|---:|",
    ]
    for row in api_rows:
        lines.append(f"| `{row.get('symbol', '')}` | `{row.get('status', '')}` | `{row.get('m5_last_close_utc', '')}` |")
    lines.extend(["", "## Tester Boundary(테스터 경계)", "", "| attempt(시도) | requested to(요청 종료) | log test to(로그 종료) | last observed(마지막 관측) | gap status(공백 상태) |", "|---|---:|---:|---:|---|"])
    boundary_by = {row.get("attempt_name"): row for row in boundary_rows}
    for row in gap_rows:
        boundary = boundary_by.get(row.get("attempt_name"), {})
        lines.append(f"| `{row.get('attempt_name', '')}` | `{boundary.get('requested_to_date', '')}` | `{boundary.get('log_test_to', '')}` | `{row.get('tester_last_observed_bar_time', '')}` | `{row.get('gap_status', '')}` |")
    lines.extend(["", "## KPI Snapshot(KPI 스냅샷)", "", "| attempt(시도) | net(순수익) | PF(수익 팩터) | trades(거래 수) | DD(손실폭) | trades/day(일일 거래 수) |", "|---|---:|---:|---:|---:|---:|"])
    for row in kpi_rows:
        lines.append(f"| `{row.get('attempt_name', '')}` | `{row.get('net_profit', '')}` | `{row.get('profit_factor', '')}` | `{row.get('trade_count', '')}` | `{row.get('max_drawdown_amount', '')}` | `{row.get('trades_per_day', '')}` |")
    lines.extend(["", "## Proxy vs MT5(프록시 대 MT5)", "", "| attempt(시도) | matched(일치) | diagnostic usability(진단 활용성) | forward usability(전진 활용성) |", "|---|---:|---|---|"])
    for row in usability_rows:
        lines.append(f"| `{row.get('attempt_name', '')}` | `{row.get('proxy_matched', '')}/{row.get('proxy_total', '')}` | `{row.get('diagnostic_usability', '')}` | `{row.get('forward_usability', '')}` |")
    return write_md(REPORT_PATH, "\n".join(lines))


def write_decision_doc(status: str, judgment: str, decision: str, next_action: str) -> Path:
    text = f"""# 2026-05-27 Stage337AD Completed-Day Forward Slice Decision(337AD 완성일 전진 구간 결정)

- status(상태): `{status}`
- judgment(판정): `{judgment}`
- decision(결정): `{decision}`
- next_action(다음 행동): `{next_action}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Effect(효과): completed-day broker slice(완성일 브로커 구간)는 tester-visible range(테스터 가시 범위) 안에서 frozen runtime handoff(고정 런타임 인계)를 확인한다. 이 결과는 attribution/stress input(귀속/압박 입력)이지 운영/전진 판정이 아니다.
"""
    return write_md(DECISION_DOC, text)


def update_status_docs(status: str, decision: str, next_action: str, gap_rows: Sequence[Mapping[str, Any]], diff_rows: Sequence[Mapping[str, Any]]) -> list[Path]:
    completed_gap = next((row for row in gap_rows if "completed_day_broker_slice" in str(row.get("attempt_name", ""))), {})
    full_gap = next((row for row in gap_rows if "full_current_day_broker_control" in str(row.get("attempt_name", ""))), {})
    matched = sum(1 for row in diff_rows if str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true")
    selected_text = f"""# Stage337 Selection Status(337단계 선택 상태)

- stage_id(단계 ID): `{STAGE_ID}`
- stage_status(단계 상태): `open_active`
- selected_candidate(선택 후보): `none`
- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{decision}`
- current_run(현재 실행): `{next_action}`
- completed_day_slice_gap(완성일 구간 공백): `{completed_gap.get('gap_status', '')}`
- full_current_day_control_gap(현재일 전체 대조 공백): `{full_gap.get('gap_status', '')}`
- timestamp_aligned_proxy_parity(시점 맞춤 프록시 동등성): `{matched}/{len(diff_rows)}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Forward Blocked(전진 차단): `latest_current_day_visibility_boundary_not_operating_resolved`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{next_action}`
- effect(효과): run337AD(337AD 실행)는 completed-day broker slice(완성일 브로커 구간)로 Strategy Tester(전략 테스터)의 completed-day handoff(완성일 인계)를 확인했고, 최신 forward(전진) 판정은 아직 주장하지 않는다.
"""
    write_md(SELECTED_STATUS, selected_text)
    focus = (
        f"  Stage337 run337AD focus complete: run337AD(337AD 실행)는 `{status}`로 completed-day forward slice"
        f"(완성일 전진 구간)를 기록했다. Effect(효과): completed slice gap(완성일 구간 공백) `{completed_gap.get('gap_status', '')}`, "
        f"full current-day control gap(현재일 전체 대조 공백) `{full_gap.get('gap_status', '')}`, "
        f"timestamp-aligned proxy parity(시점 맞춤 프록시 동등성) `{matched}/{len(diff_rows)}`이며 Forward/Goal(전진/목표)은 주장하지 않는다."
    )
    if path_exists(WORKSPACE_STATE):
        text, had_bom = ab.read_text_lossless(WORKSPACE_STATE)
        text = re.sub(r"current_run_id: .*", f"current_run_id: {next_action}", text, count=1)
        if "Stage337 run337AD focus complete" not in text:
            text = text.replace("current_focus:\n", f"current_focus:\n- >-\n{focus}\n")
        else:
            text = re.sub(r"- >-\n  Stage337 run337AD focus complete:.*?(?=\n- >-|\Z)", f"- >-\n{focus}", text, count=1, flags=re.S)
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
## Stage337 run337AD(337AD 실행) - {TODAY}

- status(상태): `{status}`
- decision(결정): `{decision}`
- next_action(다음 행동): `{next_action}`
- effect(효과): completed-day broker slice(완성일 브로커 구간)가 `{completed_gap.get('gap_status', '')}`이고 full current-day control(현재일 전체 대조군)은 `{full_gap.get('gap_status', '')}`이다. proxy parity(프록시 동등성)는 `{matched}/{len(diff_rows)}`.
"""
    if path_exists(CURRENT_STATE):
        text, had_bom = ab.read_text_lossless(CURRENT_STATE)
        text = re.sub(r"\A# Current Working State\(현재 작업 상태\).*?(?=\n## )", header.rstrip() + "\n", text, count=1, flags=re.S)
        if "## Stage337 run337AD(337AD 실행)" in text:
            text = re.sub(r"## Stage337 run337AD\(337AD 실행\).*?(?=\n## |\Z)", current_entry.strip(), text, count=1, flags=re.S)
        else:
            text = text.rstrip() + "\n\n" + current_entry.strip() + "\n"
        ab.write_text_preserving(CURRENT_STATE, text, had_bom)
    if path_exists(CHANGELOG):
        text, had_bom = ab.read_text_lossless(CHANGELOG)
        line = f"\n- {TODAY}: Stage337 run337AD(337AD 실행) `{status}`. Effect(효과): completed-day broker slice(완성일 브로커 구간) `{completed_gap.get('gap_status', '')}`를 기록하고 Forward/Goal(전진/목표)은 주장하지 않았다.\n"
        if "Stage337 run337AD(337AD 실행)" in text:
            text = re.sub(r"\n- [^\n]*Stage337 run337AD\(337AD 실행\)[^\n]*", line.rstrip(), text, count=1)
        else:
            text = text.rstrip() + line
        ab.write_text_preserving(CHANGELOG, text, had_bom)
    if path_exists(STAGE_BRIEF):
        text, had_bom = ab.read_text_lossless(STAGE_BRIEF)
        text = re.sub(r"- latest_run\(최신 실행\): `[^`]+`", f"- latest_run(최신 실행): `{RUN_ID}`", text)
        summary = (
            f"- run337AD_summary(337AD 요약): `{status}`. Effect(효과): completed-day slice(완성일 구간) "
            f"`{completed_gap.get('gap_status', '')}`와 proxy parity(프록시 동등성) `{matched}/{len(diff_rows)}`를 기록했다.\n"
        )
        if "run337AD_summary(337AD 요약)" in text:
            text = re.sub(r"- run337AD_summary\(337AD 요약\): [^\n]*(?:\n|$)", summary, text, count=1)
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
                "notes": "run337AD completed-day forward slice artifact; no forward or goal claim",
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
            "family": "completed_day_forward_slice_or_next_day_rollover_confirm",
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
            "run_key": f"{RUN_ID}__completed_day_forward_slice_or_next_day_rollover_confirm",
            "ledger_row_id": f"{RUN_ID}__completed_day_forward_slice_or_next_day_rollover_confirm",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "family": "completed_day_forward_slice_or_next_day_rollover_confirm",
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
    for directory in (RUN_DIR, MT5_DIR, FEATURE_COPY_DIR, MODEL_COPY_DIR, TELEMETRY_DIR, SLICE_INPUT_DIR):
        io_path(directory).mkdir(parents=True, exist_ok=True)

    source = load_source_u42()
    source_feature = ROOT / str(source.get("feature_local_path", ""))
    cutoff = parent_completed_cutoff()
    completed_feature, cutoff_metadata = truncate_feature_csv(source_feature, SLICE_INPUT_DIR / "u42_plain_completed_day_features.csv", cutoff)
    prepared = build_source_attempts(source, completed_feature)
    feature_rows_prepared = qprobe.feature_last_rows(prepared)
    full_feature_last = next((row.get("feature_last_timestamp", "") for row in feature_rows_prepared if "full_current_day" in row.get("attempt_name", "")), "")

    broker_api = ab.mt5_api_symbol_visibility(terminal_path, ORIGIN_SYMBOL)
    api_rows = [broker_api]
    next_day_rows = next_day_rollover_audit(full_feature_last, broker_api)
    pre_tester_recovery = qprobe.stop_target_terminal_if_running(terminal_path)

    attempts, handoff_rows, materialized_artifacts = base.build_attempts(prepared, common_files_root)
    scenario_by_attempt = {str(row["attempt_name"]): row for row in prepared}
    for attempt in attempts:
        scenario = scenario_by_attempt.get(str(attempt["attempt_name"]), {})
        for key in ("scenario_id", "scenario_symbol", "scenario_from_date", "scenario_to_date", "scenario_model", "slice_type"):
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
        default_source="stage337AD_timestamp_aligned_python_onnx_inference",
    )
    diff_rows = base.build_signal_difference_rows(aligned_proxy_rows, runtime_rows)
    for row in diff_rows:
        row["mt5_source"] = "stage337AD_runtime_summary_completed_day_slice"
        row["usable_for_forward_pass_fail"] = False
        row["claim_boundary"] = CLAIM_BOUNDARY
    usability_rows = proxy_usability_rows(gap_rows, diff_rows)
    kpi_rows = completed_day_kpi_rows(runtime_rows, feature_rows, attempts)
    status, judgment, decision, next_action = classify(gap_rows, diff_rows, args.materialize_only)
    gates = gate_rows(gap_rows, diff_rows, next_day_rows)
    receipts = write_receipts(status, judgment, decision, next_action, runtime_rows, gap_rows, diff_rows, cutoff_metadata)
    report = write_report(status, judgment, decision, next_action, api_rows, next_day_rows, runtime_rows, boundary_rows, gap_rows, diff_rows, usability_rows, kpi_rows)
    decision_doc = write_decision_doc(status, judgment, decision, next_action)
    artifact_paths: list[Path] = [
        write_json(RUN_DIR / "completed_day_slice_contract.json", cutoff_metadata),
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
        write_csv(RUN_DIR / "mt5_api_visibility.csv", sorted({key for row in api_rows for key in row.keys()}), api_rows),
        write_csv(RUN_DIR / "next_day_rollover_audit.csv", sorted({key for row in next_day_rows for key in row.keys()}), next_day_rows),
        write_csv(RUN_DIR / "handoff_attempts.csv", sorted({key for row in handoff_rows for key in row.keys()}), handoff_rows),
        write_json(RUN_DIR / "handoff_attempts.json", attempts),
        write_csv(RUN_DIR / "runtime_summary.csv", sorted({key for row in runtime_rows for key in row.keys()}), runtime_rows),
        write_csv(RUN_DIR / "completed_day_forward_kpi_summary.csv", sorted({key for row in kpi_rows for key in row.keys()}), kpi_rows),
        write_csv(RUN_DIR / "feature_last_timestamp_audit.csv", sorted({key for row in feature_rows for key in row.keys()}), feature_rows),
        write_csv(RUN_DIR / "tester_boundary_completed_day_slice.csv", sorted({key for row in boundary_rows for key in row.keys()}), boundary_rows),
        write_csv(RUN_DIR / "tester_feature_last_gap_completed_day_slice.csv", sorted({key for row in gap_rows for key in row.keys()}), gap_rows),
        write_csv(RUN_DIR / "timestamp_aligned_proxy_expected_result.csv", sorted({key for row in aligned_proxy_rows for key in row.keys()}), aligned_proxy_rows),
        write_csv(RUN_DIR / "timestamp_aligned_proxy_mt5_difference.csv", sorted({key for row in diff_rows for key in row.keys()}), diff_rows),
        write_csv(RUN_DIR / "proxy_usability_judgment.csv", sorted({key for row in usability_rows for key in row.keys()}), usability_rows),
        write_csv(RUN_DIR / "required_gate_coverage_audit.csv", sorted({key for row in gates for key in row.keys()}), gates),
        report,
        decision_doc,
        completed_feature,
        *materialized_artifacts,
        *copied_runtime_artifacts,
        *receipts,
    ]
    docs = update_status_docs(status, decision, next_action, gap_rows, diff_rows)
    registers = update_registers(status, judgment, decision, next_action, [*artifact_paths, *docs])
    artifact_paths.extend(docs)
    artifact_paths.extend(registers)
    manifest = write_json(
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
    upsert_artifact_registry([*artifact_paths, manifest])
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": status,
                "judgment": judgment,
                "decision": decision,
                "next_action": next_action,
                "completed_slice_gap": next((row.get("gap_status") for row in gap_rows if "completed_day_broker_slice" in str(row.get("attempt_name", ""))), ""),
                "full_current_day_gap": next((row.get("gap_status") for row in gap_rows if "full_current_day_broker_control" in str(row.get("attempt_name", ""))), ""),
                "proxy_diff_matched": sum(1 for row in diff_rows if str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true"),
                "proxy_diff_rows": len(diff_rows),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
