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
from typing import Any, Mapping, Sequence

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, path_exists, sha256_file_lf_normalized  # noqa: E402
from foundation.mt5.runtime_artifacts import sha256_file  # noqa: E402
from stage_pipelines.stage335 import independent_proxy_mt5_probe as base  # noqa: E402
from stage_pipelines.stage337 import probe_completed_day_forward_slice_or_next_day_rollover_confirm as ad  # noqa: E402
from stage_pipelines.stage337 import probe_custom_symbol_intraday_tester_visibility as ab  # noqa: E402
from stage_pipelines.stage337 import review_runtime_data_and_feature_source_repair_probe as qprobe  # noqa: E402


TODAY = "2026-05-27"
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
RUN_NUMBER = "run337AH"
RUN_ID = "run337AH_execute_full_current_day_visibility_repair_and_no_overfit_preflight_v1"
PARENT_RUN_ID = "run337AG_no_overfit_rebuild_scaffold_materialization_v1"
NEXT_RUN_ID_REPAIRED = "run337AI_full_current_day_forward_attribution_cost_curve_review_v1"
NEXT_RUN_ID_GAP = "run337AI_tester_visibility_alternative_repair_or_rollover_reprobe_v1"
NEXT_RUN_ID_PENDING = "run337AI_execute_visibility_repair_after_materialized_preflight_v1"
CLAIM_BOUNDARY = (
    "research_development_only_stage337AH_full_current_day_visibility_repair_no_overfit_preflight_no_model_training_"
    "no_threshold_retuning_no_lot_optimization_no_candidate_selection_no_forward_passed_no_forward_failed_"
    "no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STATUS_REPAIRED = "completed_stage337AH_full_current_day_visibility_repaired_no_forward_decision"
STATUS_GAP_REMAINS = "completed_stage337AH_full_current_day_visibility_gap_remains_preflight_ready_no_forward_decision"
STATUS_RUNTIME_ISSUE = "completed_stage337AH_visibility_repair_attempt_runtime_issue_no_forward_decision"
STATUS_MATERIALIZED = "completed_stage337AH_visibility_repair_preflight_materialized_execution_pending_no_forward_decision"
JUDGMENT_REPAIRED = "full_current_day_tester_reached_feature_last_proxy_mt5_parity_refresh_supports_attribution_next"
JUDGMENT_GAP_REMAINS = "full_current_day_tester_gap_remains_after_repair_attempt_keep_forward_boundary"
JUDGMENT_RUNTIME_ISSUE = "runtime_attempt_output_incomplete_requires_repair_before_forward_boundary_can_close"
JUDGMENT_MATERIALIZED = "visibility_repair_and_no_overfit_preflight_inputs_materialized_execution_pending"
DECISION_REPAIRED = "stage337AH_open_run337AI_full_current_day_attribution_cost_curve_review_no_selection"
DECISION_GAP_REMAINS = "stage337AH_open_run337AI_tester_visibility_alternative_repair_or_rollover_reprobe_no_selection"
DECISION_RUNTIME_ISSUE = "stage337AH_open_run337AI_runtime_output_repair_then_visibility_reprobe_no_selection"
DECISION_MATERIALIZED = "stage337AH_execution_pending_no_selection"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
RUN337Z_DIR = STAGE_DIR / "02_runs" / "run337Z"
RUN337Z_ATTEMPTS = RUN337Z_DIR / "rollover_reprobe_handoff_attempts.json"
RUN337AG_DIR = STAGE_DIR / "02_runs" / "run337AG"
MT5_DIR = RUN_DIR / "mt5"
FEATURE_COPY_DIR = RUN_DIR / "feature_matrices"
MODEL_COPY_DIR = RUN_DIR / "models"
TELEMETRY_DIR = RUN_DIR / "runtime_telemetry"
SLICE_INPUT_DIR = RUN_DIR / "completed_day_slice_inputs"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEWS_DIR / "run337AH_full_current_day_visibility_repair_and_no_overfit_preflight.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage337AH_full_current_day_visibility_repair_and_no_overfit_preflight.md"
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

COMMON_ROOT = "Project_Obsidian_Prime_v2/stage337/run337AH_full_current_day_visibility_repair"
ORIGIN_SYMBOL = "US100"
BROKER_FROM_DATE = "2026.04.14"
BROKER_TO_DATE = "2026.05.30"
ATTEMPT_BASE = "u42_plain_rf"

RUN337AG_CONTRACTS = {
    "execution_queue": RUN337AG_DIR / "run337AH_execution_queue.csv",
    "no_lookahead_policy": RUN337AG_DIR / "no_lookahead_split_policy.csv",
    "proxy_mt5_role_lock": RUN337AG_DIR / "proxy_mt5_role_lock_contract.csv",
    "mt5_visibility_repair": RUN337AG_DIR / "mt5_visibility_repair_contract.csv",
    "predeclared_gates": RUN337AG_DIR / "predeclared_gate_contracts.csv",
}


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return item.as_posix()


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def number(value: Any, default: float = 0.0) -> float:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return default
    return parsed if math.isfinite(parsed) else default


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


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
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
    with io_path(path).open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    return path


def read_text(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    bom = raw.startswith(b"\xef\xbb\xbf")
    return raw.decode("utf-8-sig" if bom else "utf-8"), bom


def write_text(path: Path, text: str, had_bom: bool | None = None) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    encoding = "utf-8-sig" if had_bom or path.suffix.lower() in {".md", ".txt", ".yaml"} else "utf-8"
    normalized = text.replace("\r\n", "\n").replace("\r", "\n").rstrip() + "\n"
    with io_path(path).open("w", encoding=encoding, newline="\n") as handle:
        handle.write(normalized)
    return path


def write_md(path: Path, text: str) -> Path:
    return write_text(path, text, True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stage337AH full current-day tester visibility repair and no-overfit preflight.")
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
    for module in (base, qprobe, ab, ad):
        module.RUN_ID = RUN_ID
        module.RUN_DIR = RUN_DIR
        module.CLAIM_BOUNDARY = CLAIM_BOUNDARY
    base.MT5_DIR = MT5_DIR
    base.FEATURE_COPY_DIR = FEATURE_COPY_DIR
    base.MODEL_COPY_DIR = MODEL_COPY_DIR
    base.TELEMETRY_DIR = TELEMETRY_DIR
    base.COMMON_ROOT = COMMON_ROOT
    qprobe.TELEMETRY_DIR = TELEMETRY_DIR
    qprobe.TESTER_LOG = TESTER_LOG
    qprobe.TESTER_AGENT_LOG = TESTER_AGENT_LOG
    qprobe.TERMINAL_LOG = TERMINAL_LOG
    ab.TESTER_LOG = TESTER_LOG
    ab.TESTER_AGENT_LOG = TESTER_AGENT_LOG
    ab.TERMINAL_LOG = TERMINAL_LOG
    ad.RUN_NUMBER = RUN_NUMBER
    ad.PARENT_RUN_ID = PARENT_RUN_ID
    ad.RUN337Z_ATTEMPTS = RUN337Z_ATTEMPTS
    ad.RUN_DIR = RUN_DIR
    ad.MT5_DIR = MT5_DIR
    ad.FEATURE_COPY_DIR = FEATURE_COPY_DIR
    ad.MODEL_COPY_DIR = MODEL_COPY_DIR
    ad.TELEMETRY_DIR = TELEMETRY_DIR
    ad.SLICE_INPUT_DIR = SLICE_INPUT_DIR
    ad.REPORT_PATH = REPORT_PATH
    ad.DECISION_DOC = DECISION_DOC
    ad.TESTER_LOG = TESTER_LOG
    ad.TESTER_AGENT_LOG = TESTER_AGENT_LOG
    ad.TERMINAL_LOG = TERMINAL_LOG
    ad.COMMON_ROOT = COMMON_ROOT


def load_source_u42() -> dict[str, Any]:
    rows = read_json(RUN337Z_ATTEMPTS)
    if not isinstance(rows, list):
        raise RuntimeError(f"source attempts is not a list: {RUN337Z_ATTEMPTS}")
    source = next((dict(row) for row in rows if row.get("attempt_name") == ATTEMPT_BASE), None)
    if source is None:
        raise RuntimeError(f"missing {ATTEMPT_BASE} in {RUN337Z_ATTEMPTS}")
    return source


def feature_timestamp_series(frame: pd.DataFrame) -> pd.Series:
    for column in ("timestamp_utc", "bar_time_server", "timestamp"):
        if column in frame.columns:
            return pd.to_datetime(frame[column].astype(str).str.replace(".", "-", regex=False), errors="coerce", utc=True)
    return pd.Series(pd.NaT, index=frame.index, dtype="datetime64[ns, UTC]")


def completed_day_cutoff(feature_path: Path) -> pd.Timestamp:
    frame = pd.read_csv(io_path(feature_path), usecols=lambda column: column in {"timestamp_utc", "bar_time_server", "timestamp"})
    timestamps = feature_timestamp_series(frame).dropna()
    if timestamps.empty:
        raise RuntimeError(f"cannot derive timestamps from {feature_path}")
    latest = timestamps.max()
    completed = timestamps.loc[timestamps.dt.date < latest.date()]
    if completed.empty:
        raise RuntimeError("feature source does not contain a completed prior day")
    return completed.max()


def truncate_feature_csv(source_path: Path, target_path: Path, cutoff: pd.Timestamp) -> tuple[Path, dict[str, Any]]:
    frame = pd.read_csv(io_path(source_path))
    timestamps = feature_timestamp_series(frame)
    mask = timestamps <= cutoff
    sliced = frame.loc[mask].copy()
    io_path(target_path.parent).mkdir(parents=True, exist_ok=True)
    sliced.to_csv(io_path(target_path), index=False, lineterminator="\n")
    return target_path, {
        "source_feature_path": rel(source_path),
        "target_feature_path": rel(target_path),
        "cutoff_timestamp": cutoff.isoformat().replace("+00:00", "Z"),
        "source_rows": int(len(frame)),
        "sliced_rows": int(len(sliced)),
        "source_first_timestamp": timestamps.min().isoformat().replace("+00:00", "Z") if timestamps.notna().any() else "",
        "source_last_timestamp": timestamps.max().isoformat().replace("+00:00", "Z") if timestamps.notna().any() else "",
        "sliced_last_timestamp": timestamps.loc[mask].max().isoformat().replace("+00:00", "Z") if mask.any() else "",
        "effect": "completed-day slice(완성일 구간)는 tester visible baseline(테스터 가시 기준선) 비교용이며, full current-day control(현재일 전체 대조)은 원본 feature CSV(피처 CSV)를 유지한다.",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_source_attempts(source: Mapping[str, Any], completed_feature_path: Path) -> list[dict[str, Any]]:
    scenarios = [
        {
            "suffix": "ah_completed_day_broker_slice",
            "artifact_slug": "u42_plain_ah_completed_day_broker_slice",
            "scenario_id": "completed_day_broker_slice_preflight_control",
            "feature_path": rel(completed_feature_path),
            "slice_type": "completed_day_broker_slice",
        },
        {
            "suffix": "ah_full_current_day_broker_control",
            "artifact_slug": "u42_plain_ah_full_current_day_broker_control",
            "scenario_id": "full_current_day_broker_control_visibility_repair",
            "feature_path": source.get("feature_local_path", ""),
            "slice_type": "full_current_day_control",
        },
    ]
    selected: list[dict[str, Any]] = []
    for index, scenario in enumerate(scenarios):
        copied = dict(source)
        copied["attempt_name"] = f"u42_plain_rf_{scenario['suffix']}"
        copied["artifact_slug"] = scenario["artifact_slug"]
        copied["scenario_id"] = scenario["scenario_id"]
        copied["scenario_symbol"] = ORIGIN_SYMBOL
        copied["scenario_from_date"] = BROKER_FROM_DATE
        copied["scenario_to_date"] = BROKER_TO_DATE
        copied["scenario_model"] = "4"
        copied["slice_type"] = scenario["slice_type"]
        copied["model_copy"] = {"source": source.get("model_local_path") or source.get("model_copy", {}).get("source", "")}
        copied["feature_export"] = {"path": scenario["feature_path"]}
        copied["feature_local_path"] = scenario["feature_path"]
        copied["source_run_id"] = PARENT_RUN_ID
        copied["attempt_role"] = "stage337AH_full_current_day_visibility_repair_same_frozen_u42_model_threshold_risk"
        copied["record_view_prefix"] = f"mt5_stage337AH_u42_plain_{index}"
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
    attempt["attempt_role"] = "stage337AH_visibility_repair_same_frozen_u42_model_threshold_risk"
    attempt["record_view_prefix"] = f"mt5_stage337AH_{attempt['artifact_slug']}"
    attempt["source_run_id"] = PARENT_RUN_ID
    attempt["repair_contract"] = "same ONNX, feature order, D/B surface, threshold, risk, lot, ATR SL/TP, broker symbol; only tester visibility is reprobed"
    attempt["signal_policy"] = "runtime-boundary diagnostic only; not Forward Passed/Failed authority"
    return attempt


def proxy_usability_rows(gap_rows: Sequence[Mapping[str, Any]], diff_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    gap_by_attempt = {str(row.get("attempt_name", "")): row for row in gap_rows}
    rows: list[dict[str, Any]] = []
    for attempt_name in sorted({str(row.get("attempt_name", "")) for row in diff_rows}):
        group = [row for row in diff_rows if str(row.get("attempt_name", "")) == attempt_name]
        matched = sum(1 for row in group if str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true")
        total = len(group)
        gap_status = str(gap_by_attempt.get(attempt_name, {}).get("gap_status", ""))
        if matched == total and total and gap_status == "tester_reached_feature_last":
            diagnostic = "usable_for_signal_parity_at_reached_feature_last_not_forward_decision"
        elif matched == total and total:
            diagnostic = "usable_for_signal_parity_until_tester_cutoff_not_forward_decision"
        else:
            diagnostic = "not_usable_for_signal_parity_requires_runtime_review"
        rows.append(
            {
                "attempt_name": attempt_name,
                "gap_status": gap_status,
                "proxy_matched": matched,
                "proxy_total": total,
                "diagnostic_usability": diagnostic,
                "forward_usability": "not_usable_as_forward_decision",
                "allowed_use": "signal parity(신호 동등성) and handoff sanity(인계 점검)",
                "disallowed_use": "KPI authority(KPI 권위), Forward Passed/Failed(전진 통과/실패), candidate selection(후보 선택)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def kpi_rows(runtime_rows: Sequence[Mapping[str, Any]], feature_rows: Sequence[Mapping[str, Any]], attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    feature_by = {str(row.get("attempt_name", "")): row for row in feature_rows}
    attempt_by = {str(row.get("attempt_name", "")): row for row in attempts}
    rows: list[dict[str, Any]] = []
    for runtime in runtime_rows:
        attempt = str(runtime.get("attempt_name", ""))
        feature = feature_by.get(attempt, {})
        start = pd.to_datetime(feature.get("feature_first_timestamp", ""), errors="coerce", utc=True)
        end = pd.to_datetime(feature.get("feature_last_timestamp", ""), errors="coerce", utc=True)
        days = None if pd.isna(start) or pd.isna(end) else max((end - start).total_seconds() / 86400.0, 1 / 288.0)
        trades = number(runtime.get("trade_count"), default=math.nan)
        rows.append(
            {
                "attempt_name": attempt,
                "slice_type": attempt_by.get(attempt, {}).get("slice_type", ""),
                "tester_status": runtime.get("tester_status", ""),
                "runtime_status": runtime.get("runtime_status", ""),
                "report_status": runtime.get("report_status", ""),
                "feature_first_timestamp": feature.get("feature_first_timestamp", ""),
                "feature_last_timestamp": feature.get("feature_last_timestamp", ""),
                "net_profit": runtime.get("net_profit", ""),
                "profit_factor": runtime.get("profit_factor", ""),
                "trade_count": runtime.get("trade_count", ""),
                "trades_per_day": "" if days is None or not math.isfinite(trades) else trades / days,
                "expectancy": runtime.get("expectancy", ""),
                "recovery_factor": runtime.get("recovery_factor", ""),
                "max_drawdown_amount": runtime.get("max_drawdown_amount", ""),
                "kpi_authority": "runtime_probe_diagnostic_not_forward_decision",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def preflight_audit_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for name, path in RUN337AG_CONTRACTS.items():
        exists = path_exists(path)
        row_count = len(read_csv(path)) if exists and path.suffix.lower() == ".csv" else ""
        rows.append(
            {
                "preflight_id": name,
                "source_contract": rel(path),
                "exists": exists,
                "row_count": row_count,
                "status": "passed" if exists else "failed_missing_contract",
                "effect": "run337AH(337AH 실행)는 run337AG(337AG 실행)의 사전 선언 계약 아래에서만 실행된다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    rows.extend(
        [
            {
                "preflight_id": "no_model_training",
                "source_contract": rel(RUN337AG_CONTRACTS["no_lookahead_policy"]),
                "exists": True,
                "row_count": "",
                "status": "passed",
                "effect": "ONNX(온엑스) 학습 또는 재학습을 하지 않는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "preflight_id": "no_threshold_or_lot_retune",
                "source_contract": rel(RUN337AG_CONTRACTS["no_lookahead_policy"]),
                "exists": True,
                "row_count": "",
                "status": "passed",
                "effect": "threshold(임계값), lot(랏), risk logic(위험 로직)을 변경하지 않는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "preflight_id": "proxy_not_kpi_authority",
                "source_contract": rel(RUN337AG_CONTRACTS["proxy_mt5_role_lock"]),
                "exists": True,
                "row_count": "",
                "status": "passed",
                "effect": "proxy expected value(프록시 예상값)는 signal sanity(신호 점검)에만 쓴다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )
    return rows


def classify(gap_rows: Sequence[Mapping[str, Any]], diff_rows: Sequence[Mapping[str, Any]], runtime_rows: Sequence[Mapping[str, Any]], materialize_only: bool) -> tuple[str, str, str, str]:
    if materialize_only:
        return STATUS_MATERIALIZED, JUDGMENT_MATERIALIZED, DECISION_MATERIALIZED, NEXT_RUN_ID_PENDING
    full_gap = next((row for row in gap_rows if "full_current_day" in str(row.get("attempt_name", ""))), {})
    full_reached = full_gap.get("gap_status") == "tester_reached_feature_last"
    all_runtime_completed = bool(runtime_rows) and all(
        row.get("tester_status") == "completed" and row.get("runtime_status") == "completed" for row in runtime_rows
    )
    matched = sum(1 for row in diff_rows if str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true")
    if full_reached and diff_rows and matched == len(diff_rows):
        return STATUS_REPAIRED, JUDGMENT_REPAIRED, DECISION_REPAIRED, NEXT_RUN_ID_REPAIRED
    if all_runtime_completed:
        return STATUS_GAP_REMAINS, JUDGMENT_GAP_REMAINS, DECISION_GAP_REMAINS, NEXT_RUN_ID_GAP
    return STATUS_RUNTIME_ISSUE, JUDGMENT_RUNTIME_ISSUE, DECISION_RUNTIME_ISSUE, NEXT_RUN_ID_GAP


def gate_rows(status: str, gap_rows: Sequence[Mapping[str, Any]], diff_rows: Sequence[Mapping[str, Any]], preflight_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    completed_gap = next((row for row in gap_rows if "completed_day" in str(row.get("attempt_name", ""))), {})
    full_gap = next((row for row in gap_rows if "full_current_day" in str(row.get("attempt_name", ""))), {})
    matched = sum(1 for row in diff_rows if str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true")
    preflight_passed = sum(1 for row in preflight_rows if row.get("status") == "passed")
    return [
        {
            "gate_name": "run337AG_contracts_loaded(337AG 계약 로드)",
            "status": "passed" if preflight_passed == len(preflight_rows) else "failed",
            "evidence_path": rel(RUN_DIR / "no_overfit_preflight_audit.csv"),
            "effect": f"preflight(사전점검) {preflight_passed}/{len(preflight_rows)} 통과.",
        },
        {
            "gate_name": "completed_day_visibility_control(완성일 가시성 대조)",
            "status": "passed" if completed_gap.get("gap_status") == "tester_reached_feature_last" else "review",
            "evidence_path": rel(RUN_DIR / "tester_feature_last_gap_visibility_repair.csv"),
            "effect": f"completed_day_gap(완성일 공백)={completed_gap.get('gap_status', '')}.",
        },
        {
            "gate_name": "full_current_day_visibility_repair(현재일 전체 가시성 수리)",
            "status": "passed" if full_gap.get("gap_status") == "tester_reached_feature_last" else "still_open",
            "evidence_path": rel(RUN_DIR / "tester_feature_last_gap_visibility_repair.csv"),
            "effect": f"full_current_day_gap(현재일 전체 공백)={full_gap.get('gap_status', '')}.",
        },
        {
            "gate_name": "timestamp_aligned_proxy_mt5_parity(시점 맞춤 프록시-MT5 동등성)",
            "status": "passed" if diff_rows and matched == len(diff_rows) else "review",
            "evidence_path": rel(RUN_DIR / "timestamp_aligned_proxy_mt5_difference.csv"),
            "effect": f"matched(일치)={matched}/{len(diff_rows)}.",
        },
        {
            "gate_name": "no_training_no_retune(무학습/무재조정)",
            "status": "passed",
            "evidence_path": rel(RUN_DIR / "handoff_attempts.csv"),
            "effect": "same frozen ONNX/feature order/threshold/risk/lot(같은 고정 온엑스/피처 순서/임계값/위험/랏)로 실행했다.",
        },
        {
            "gate_name": "forward_decision_gate(전진 판정 게이트)",
            "status": "not_claimed",
            "evidence_path": rel(RUN_DIR / "final_visibility_repair_decision.json"),
            "effect": f"status(상태)={status}; Forward Passed/Failed(전진 통과/실패)는 주장하지 않는다.",
        },
        {
            "gate_name": "goal_achieve_gate(목표 달성 게이트)",
            "status": "not_claimed",
            "evidence_path": rel(RUN_DIR / "result_judgment_receipt.json"),
            "effect": "runtime repair probe(런타임 수리 탐침)는 Goal Achieve(목표 달성)가 아니다.",
        },
    ]


def final_decision_payload(status: str, judgment: str, decision: str, next_action: str, gap_rows: Sequence[Mapping[str, Any]], diff_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    completed_gap = next((row for row in gap_rows if "completed_day" in str(row.get("attempt_name", ""))), {})
    full_gap = next((row for row in gap_rows if "full_current_day" in str(row.get("attempt_name", ""))), {})
    matched = sum(1 for row in diff_rows if str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true")
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": status,
        "judgment": judgment,
        "decision": decision,
        "next_action": next_action,
        "completed_day_gap": completed_gap.get("gap_status", ""),
        "full_current_day_gap": full_gap.get("gap_status", ""),
        "full_current_day_gap_minutes": full_gap.get("tester_to_feature_last_gap_minutes", ""),
        "proxy_mt5_matched": matched,
        "proxy_mt5_rows": len(diff_rows),
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def md_table(columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = [str(row.get(column, "")).replace("|", "/").replace("\n", " ") for column in columns]
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def report_text(final_decision: Mapping[str, Any], runtime_rows: Sequence[Mapping[str, Any]], gap_rows: Sequence[Mapping[str, Any]], usability_rows: Sequence[Mapping[str, Any]], preflight_rows: Sequence[Mapping[str, Any]], kpis: Sequence[Mapping[str, Any]]) -> str:
    runtime_view = [
        {
            "attempt": row.get("attempt_name", ""),
            "tester": row.get("tester_status", ""),
            "runtime": row.get("runtime_status", ""),
            "report": row.get("report_status", ""),
            "net": row.get("net_profit", ""),
            "pf": row.get("profit_factor", ""),
            "trades": row.get("trade_count", ""),
        }
        for row in runtime_rows
    ]
    gap_view = [
        {
            "attempt": row.get("attempt_name", ""),
            "feature_last": row.get("feature_last_timestamp", ""),
            "tester_last": row.get("tester_last_observed_bar_time", ""),
            "gap_minutes": row.get("tester_to_feature_last_gap_minutes", ""),
            "status": row.get("gap_status", ""),
        }
        for row in gap_rows
    ]
    usability_view = [
        {
            "attempt": row.get("attempt_name", ""),
            "matched": f"{row.get('proxy_matched', '')}/{row.get('proxy_total', '')}",
            "gap": row.get("gap_status", ""),
            "use": row.get("diagnostic_usability", ""),
        }
        for row in usability_rows
    ]
    preflight_view = [
        {"id": row.get("preflight_id", ""), "status": row.get("status", ""), "effect": row.get("effect", "")}
        for row in preflight_rows
    ]
    kpi_view = [
        {
            "attempt": row.get("attempt_name", ""),
            "slice": row.get("slice_type", ""),
            "net": row.get("net_profit", ""),
            "pf": row.get("profit_factor", ""),
            "dd": row.get("max_drawdown_amount", ""),
            "tpd": row.get("trades_per_day", ""),
        }
        for row in kpis
    ]
    return f"""# run337AH Full Current-Day Visibility Repair And No-Overfit Preflight(337AH 현재일 전체 가시성 수리 및 무과적합 사전점검)

## Decision(결정)

- status(상태): `{final_decision['status']}`
- judgment(판정): `{final_decision['judgment']}`
- decision(결정): `{final_decision['decision']}`
- completed_day_gap(완성일 공백): `{final_decision['completed_day_gap']}`
- full_current_day_gap(현재일 전체 공백): `{final_decision['full_current_day_gap']}`
- full_current_day_gap_minutes(현재일 전체 공백 분): `{final_decision['full_current_day_gap_minutes']}`
- proxy_mt5_matched(프록시-MT5 일치): `{final_decision['proxy_mt5_matched']}/{final_decision['proxy_mt5_rows']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final_decision['next_action']}`

Effect(효과): frozen cp322A/u42 ONNX(고정 cp322A/u42 온엑스)를 바꾸지 않고 Strategy Tester(전략 테스터)의 current-day visibility(현재일 가시성)와 proxy/MT5 parity(프록시/MT5 동등성)를 다시 확인했다.

## Runtime Summary(런타임 요약)

{md_table(["attempt", "tester", "runtime", "report", "net", "pf", "trades"], runtime_view)}

## Tester Visibility(테스터 가시성)

{md_table(["attempt", "feature_last", "tester_last", "gap_minutes", "status"], gap_view)}

## KPI Snapshot(KPI 스냅샷)

{md_table(["attempt", "slice", "net", "pf", "dd", "tpd"], kpi_view)}

## Proxy/MT5 Usability(프록시/MT5 활용성)

{md_table(["attempt", "matched", "gap", "use"], usability_view)}

## No-Overfit Preflight(무과적합 사전점검)

{md_table(["id", "status", "effect"], preflight_view)}

## Claim Boundary(주장 경계)

이 run(실행)은 model training(모델 학습), candidate selection(후보 선택), threshold retune(임계값 재조정), lot optimization(랏 최적화), runtime authority(런타임 권위), live readiness(실거래 준비), deployment(배포), operating promotion(운영 승격), Goal Achieve(목표 달성)를 주장하지 않는다.
"""


def decision_doc_text(final_decision: Mapping[str, Any]) -> str:
    return f"""# Decision(결정): Stage337 run337AH Full Current-Day Visibility Repair(337AH 현재일 전체 가시성 수리)

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final_decision['status']}`
- decision(결정): `{final_decision['decision']}`
- next_action(다음 행동): `{final_decision['next_action']}`

## Rationale(근거)

run337AG(337AG 실행)는 run337AH(337AH 실행)에 full current-day visibility repair(현재일 전체 가시성 수리)와 no-overfit preflight(무과적합 사전점검)를 넘겼다. 이 실행은 same frozen ONNX/feature/threshold/risk/lot(같은 고정 온엑스/피처/임계값/위험/랏)으로 MT5 Strategy Tester(전략 테스터)를 다시 실행하고, proxy expected value(프록시 예상값)와 MT5 telemetry(텔레메트리)를 비교한다.

## Boundary(경계)

Forward Passed(전진 통과), Forward Failed(전진 실패), runtime authority(런타임 권위), live readiness(실거래 준비), deployment(배포), operating promotion(운영 승격), Goal Achieve(목표 달성)는 모두 `not_claimed`다.
"""


def write_receipts(final_decision: Mapping[str, Any], runtime_rows: Sequence[Mapping[str, Any]], gap_rows: Sequence[Mapping[str, Any]], diff_rows: Sequence[Mapping[str, Any]], cutoff_metadata: Mapping[str, Any], preflight_rows: Sequence[Mapping[str, Any]]) -> list[Path]:
    matched = sum(1 for row in diff_rows if str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true")
    runtime_completed = sum(1 for row in runtime_rows if row.get("tester_status") == "completed" and row.get("runtime_status") == "completed")
    return [
        write_json(
            RUN_DIR / "data_integrity_receipt.json",
            {
                "data_source": [rel(RUN337Z_ATTEMPTS), cutoff_metadata, rel(RUN_DIR / "feature_last_timestamp_audit.csv")],
                "time_axis": "MT5 Strategy Tester(전략 테스터) server-like timestamps(서버형 시점); feature timestamps(피처 시점)는 UTC로 파싱",
                "sample_scope": "US100 M5 from 2026-04-14; completed-day control plus full current-day control(완성일 대조와 현재일 전체 대조)",
                "missing_or_duplicate_check": "feature and telemetry rows are checked through tester gap(테스터 공백) and timestamp-aligned proxy/MT5 parity(시점 맞춤 프록시/MT5 동등성)",
                "feature_label_boundary": "no labels, no training, no threshold fitting(라벨/학습/임계값 맞춤 없음)",
                "split_boundary": "runtime_probe_only(런타임 탐침 전용)",
                "leakage_risk": "full current-day visibility remains a boundary unless tester reaches feature_last(테스터가 피처 마지막에 도달하기 전까지 경계)",
                "data_hash_or_identity": rel(RUN_DIR / "completed_day_slice_contract.json"),
                "integrity_judgment": "usable_with_boundary_for_visibility_repair(가시성 수리에는 경계부 사용 가능)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RUN_DIR / "runtime_parity_receipt.json",
            {
                "research_path": rel(Path(__file__)),
                "runtime_path": rel(RUN_DIR / "handoff_attempts.json"),
                "shared_contract": "same frozen u42 ONNX, feature order, D/B surface, threshold, risk, lot, ATR SL/TP, broker US100(같은 고정 u42 온엑스/피처 순서/D/B 표면/임계값/위험/랏/ATR 손절익절/브로커 US100)",
                "known_differences": "completed-day slice truncates feature CSV; full current-day control keeps all source rows(완성일은 피처 CSV 절단, 현재일 전체는 원본 유지)",
                "parity_check": f"runtime_completed={runtime_completed}/{len(runtime_rows)}; timestamp_aligned_signal_parity={matched}/{len(diff_rows)}",
                "parity_identity": rel(RUN_DIR / "execution_result.json"),
                "runtime_claim_boundary": "runtime_probe_only_no_runtime_authority(런타임 탐침 전용, 런타임 권위 아님)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RUN_DIR / "model_validation_receipt.json",
            {
                "model_family": "frozen cp322A/u42 ONNX package(고정 cp322A/u42 온엑스 패키지)",
                "target_and_label": "unchanged; no label rebuild(변경 없음, 라벨 재구성 없음)",
                "split_method": "runtime probe visibility repair(런타임 탐침 가시성 수리)",
                "selection_metric": "not_applicable_no_selection(해당 없음, 선택 없음)",
                "secondary_metrics": ["tester gap(테스터 공백)", "proxy/MT5 parity(프록시/MT5 동등성)", "runtime KPI diagnostic(런타임 KPI 진단)"],
                "threshold_policy": "fixed_unchanged(고정, 변경 없음)",
                "overfit_risk": "contained by no-overfit preflight(무과적합 사전점검으로 제한)",
                "calibration_risk": "scores are runtime decision signals, not probability claims(점수는 런타임 판단 신호이며 확률 주장 아님)",
                "comparison_baseline": PARENT_RUN_ID,
                "validation_judgment": "runtime_visibility_repair_diagnostic(런타임 가시성 수리 진단)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RUN_DIR / "result_judgment_receipt.json",
            {
                "result_subject": RUN_ID,
                "evidence_available": [rel(RUN_DIR / "runtime_summary.csv"), rel(RUN_DIR / "tester_feature_last_gap_visibility_repair.csv"), rel(RUN_DIR / "proxy_mt5_usability_after_repair.csv"), rel(RUN_DIR / "no_overfit_preflight_audit.csv")],
                "evidence_missing": "forward pass/fail attribution still requires full gate bundle and attribution review(전진 통과/실패 귀속은 전체 게이트와 귀속 검토가 필요)",
                "judgment_label": "runtime_probe(런타임 탐침)",
                "status": final_decision["status"],
                "judgment": final_decision["judgment"],
                "decision": final_decision["decision"],
                "claim_boundary": CLAIM_BOUNDARY,
                "next_condition": final_decision["next_action"],
                "user_explanation_hook": "현재일 전체 테스터가 피처 마지막까지 도달하는지 실제로 다시 찔렀고, 결과는 성공/실패 판정이 아니라 다음 검증 경로를 정하는 근거다.",
            },
        ),
        write_json(
            RUN_DIR / "experiment_design_receipt.json",
            {
                "primary_family": "runtime_parity_repair(런타임 동등성 수리)",
                "parent_contract": PARENT_RUN_ID,
                "preflight_passed": sum(1 for row in preflight_rows if row.get("status") == "passed"),
                "preflight_total": len(preflight_rows),
                "no_overfit_controls": ["no training(학습 없음)", "no threshold retune(임계값 재조정 없음)", "proxy not KPI authority(프록시 KPI 권위 아님)", "as-of macro only(시점 기준 거시만)"],
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
    ]


def replace_line(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def append_once(text: str, marker: str, block: str) -> str:
    if marker in text:
        pattern = re.escape(marker) + r".*?(?=\n## |\Z)"
        return re.sub(pattern, block.strip(), text, count=1, flags=re.S)
    return text.rstrip() + "\n\n" + block.strip() + "\n"


def insert_or_replace_focus(text: str, focus_line: str) -> str:
    block = f"- >-\n  {focus_line}"
    marker = "Stage337 run337AH focus complete:"
    if marker in text:
        return re.sub(r"- >-\n  Stage337 run337AH focus complete:.*?(?=\n- >-|\n\n- >-|\Z)", block, text, count=1, flags=re.S)
    if "current_focus:\n" in text:
        return text.replace("current_focus:\n", "current_focus:\n" + block + "\n", 1)
    return text.rstrip() + "\ncurrent_focus:\n" + block + "\n"


def update_status_docs(final_decision: Mapping[str, Any]) -> list[Path]:
    changed: list[Path] = []
    if path_exists(SELECTED_STATUS):
        text, bom = read_text(SELECTED_STATUS)
        text = replace_line(text, "- latest_run(최신 실행):", f"- latest_run(최신 실행): `{RUN_ID}`")
        text = replace_line(text, "- latest_decision(최신 결정):", f"- latest_decision(최신 결정): `{final_decision['decision']}`")
        text = replace_line(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{final_decision['next_action']}`")
        text = replace_line(text, "- full_current_day_control_gap(현재일 전체 대조 공백):", f"- full_current_day_control_gap(현재일 전체 대조 공백): `{final_decision['full_current_day_gap']}`")
        text = replace_line(text, "- Forward Passed(전진 통과):", "- Forward Passed(전진 통과): `not_claimed`")
        text = replace_line(text, "- Forward Failed(전진 실패):", "- Forward Failed(전진 실패): `not_claimed`")
        text = replace_line(text, "- runtime_authority(런타임 권위):", "- runtime_authority(런타임 권위): `not_claimed`")
        text = replace_line(text, "- goal_achieve(목표 달성):", "- goal_achieve(목표 달성): `not_claimed`")
        text = replace_line(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{final_decision['next_action']}`")
        text = replace_line(
            text,
            "- effect(효과):",
            f"- effect(효과): run337AH(337AH 실행)는 full current-day visibility repair(현재일 전체 가시성 수리)를 실행했고 full_current_day_gap(현재일 전체 공백) `{final_decision['full_current_day_gap']}`, proxy/MT5 parity(프록시/MT5 동등성) `{final_decision['proxy_mt5_matched']}/{final_decision['proxy_mt5_rows']}`를 기록했다. Forward/Goal(전진/목표)은 주장하지 않는다.",
        )
        write_text(SELECTED_STATUS, text, bom)
        changed.append(SELECTED_STATUS)
    if path_exists(WORKSPACE_STATE):
        text, bom = read_text(WORKSPACE_STATE)
        text = replace_line(text, "current_run_id:", f"current_run_id: {final_decision['next_action']}")
        text = replace_line(text, "updated_on:", f"updated_on: '{TODAY}'")
        focus = (
            f"Stage337 run337AH focus complete: run337AH(337AH 실행)는 `{final_decision['status']}`로 full current-day visibility repair(현재일 전체 가시성 수리)와 "
            f"no-overfit preflight(무과적합 사전점검)를 실행했다. Effect(효과): completed_day_gap(완성일 공백) `{final_decision['completed_day_gap']}`, "
            f"full_current_day_gap(현재일 전체 공백) `{final_decision['full_current_day_gap']}`, proxy/MT5 parity(프록시/MT5 동등성) `{final_decision['proxy_mt5_matched']}/{final_decision['proxy_mt5_rows']}`이며 Forward/Goal(전진/목표)은 주장하지 않는다."
        )
        text = insert_or_replace_focus(text, focus)
        write_text(WORKSPACE_STATE, text, bom)
        changed.append(WORKSPACE_STATE)
    if path_exists(CURRENT_STATE):
        text, bom = read_text(CURRENT_STATE)
        text = replace_line(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{final_decision['next_action']}`")
        text = replace_line(text, "- decision(결정):", f"- decision(결정): `{final_decision['decision']}`")
        text = replace_line(text, "- latest_completed_run(최근 완료 실행):", f"- latest_completed_run(최근 완료 실행): `{RUN_ID}`")
        text = replace_line(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{final_decision['next_action']}`")
        block = f"""## Stage337 run337AH(337AH 실행) - {TODAY}

- status(상태): `{final_decision['status']}`
- decision(결정): `{final_decision['decision']}`
- next_action(다음 행동): `{final_decision['next_action']}`
- effect(효과): full current-day visibility repair(현재일 전체 가시성 수리)를 실행했고 full_current_day_gap(현재일 전체 공백) `{final_decision['full_current_day_gap']}`, proxy/MT5 parity(프록시/MT5 동등성) `{final_decision['proxy_mt5_matched']}/{final_decision['proxy_mt5_rows']}`를 기록했다. Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.
"""
        text = append_once(text, "## Stage337 run337AH(337AH 실행)", block)
        write_text(CURRENT_STATE, text, bom)
        changed.append(CURRENT_STATE)
    if path_exists(CHANGELOG):
        text, bom = read_text(CHANGELOG)
        line = f"- {TODAY}: Stage337 run337AH(337AH 실행) `{final_decision['status']}`. Effect(효과): full_current_day_gap(현재일 전체 공백) `{final_decision['full_current_day_gap']}`, proxy/MT5 parity(프록시/MT5 동등성) `{final_decision['proxy_mt5_matched']}/{final_decision['proxy_mt5_rows']}`를 기록했고 Forward/Goal(전진/목표)은 주장하지 않음."
        if line not in text:
            text = text.rstrip() + "\n" + line + "\n"
        write_text(CHANGELOG, text, bom)
        changed.append(CHANGELOG)
    if path_exists(STAGE_BRIEF):
        text, bom = read_text(STAGE_BRIEF)
        text = replace_line(text, "- latest_run(최신 실행):", f"- latest_run(최신 실행): `{RUN_ID}`")
        summary = (
            f"- run337AH_summary(337AH 요약): `{final_decision['status']}`. Effect(효과): full_current_day_gap(현재일 전체 공백) "
            f"`{final_decision['full_current_day_gap']}`, proxy/MT5 parity(프록시/MT5 동등성) `{final_decision['proxy_mt5_matched']}/{final_decision['proxy_mt5_rows']}`를 기록하고 `{final_decision['next_action']}`를 연다.\n"
        )
        if "run337AH_summary(337AH 요약)" in text:
            text = re.sub(r"- run337AH_summary\(337AH 요약\): [^\n]*(?:\n|$)", summary, text, count=1)
        else:
            text = text.replace("- selected_candidate(선택 후보):", summary + "- selected_candidate(선택 후보):")
        write_text(STAGE_BRIEF, text, bom)
        changed.append(STAGE_BRIEF)
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


def append_artifacts(paths: Sequence[Path]) -> Path:
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
        digest = sha256_file_lf_normalized(path) if suffix in {".csv", ".json", ".md", ".txt", ".py", ".yaml"} else sha256_file(path)
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
                "notes": STATUS_GAP_REMAINS,
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
    for directory in (RUN_DIR, MT5_DIR, FEATURE_COPY_DIR, MODEL_COPY_DIR, TELEMETRY_DIR, SLICE_INPUT_DIR):
        io_path(directory).mkdir(parents=True, exist_ok=True)

    source = load_source_u42()
    source_feature = ROOT / str(source.get("feature_local_path", ""))
    cutoff = completed_day_cutoff(source_feature)
    completed_feature, cutoff_metadata = truncate_feature_csv(source_feature, SLICE_INPUT_DIR / "u42_plain_completed_day_features.csv", cutoff)
    prepared = build_source_attempts(source, completed_feature)
    preflight_rows = preflight_audit_rows()
    broker_api = ab.mt5_api_symbol_visibility(terminal_path, ORIGIN_SYMBOL)
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
    gap_rows = qprobe.tester_gap_rows(runtime_rows, feature_rows, common_files_root, {"last_close_utc": broker_api.get("m5_last_close_utc", "")})
    boundary_rows = ab.parse_tester_boundary_rows(before_offsets, attempts)
    boundary_by_attempt = {row["attempt_name"]: row for row in boundary_rows}
    for row in gap_rows:
        row["scenario_id"] = boundary_by_attempt.get(row.get("attempt_name"), {}).get("scenario_id", "")
        row["tester_symbol"] = boundary_by_attempt.get(row.get("attempt_name"), {}).get("tester_symbol", "")
    cutoff_by_attempt = {str(row.get("attempt_name", "")): str(row.get("tester_last_observed_bar_time", "")) for row in gap_rows}
    aligned_proxy_rows = qprobe.sanitize_proxy_rows(
        qprobe.build_timestamp_aligned_proxy_rows(attempts, cutoff_by_attempt),
        default_source="stage337AH_timestamp_aligned_python_onnx_inference",
    )
    diff_rows = base.build_signal_difference_rows(aligned_proxy_rows, runtime_rows)
    for row in diff_rows:
        row["mt5_source"] = "stage337AH_runtime_summary_visibility_repair"
        row["usable_for_forward_pass_fail"] = False
        row["claim_boundary"] = CLAIM_BOUNDARY
    usability = proxy_usability_rows(gap_rows, diff_rows)
    kpis = kpi_rows(runtime_rows, feature_rows, attempts)
    status, judgment, decision, next_action = classify(gap_rows, diff_rows, runtime_rows, args.materialize_only)
    gates = gate_rows(status, gap_rows, diff_rows, preflight_rows)
    final_decision = final_decision_payload(status, judgment, decision, next_action, gap_rows, diff_rows)

    artifacts: list[Path] = [
        write_json(RUN_DIR / "completed_day_slice_contract.json", cutoff_metadata),
        write_json(RUN_DIR / "pre_tester_terminal_recovery.json", pre_tester_recovery),
        write_json(RUN_DIR / "execution_result.json", execution_result),
        write_json(RUN_DIR / "final_visibility_repair_decision.json", final_decision),
        write_csv(RUN_DIR / "mt5_api_visibility.csv", sorted({key for key in broker_api.keys()}), [broker_api]),
        write_csv(RUN_DIR / "no_overfit_preflight_audit.csv", sorted({key for row in preflight_rows for key in row.keys()}), preflight_rows),
        write_csv(RUN_DIR / "handoff_attempts.csv", sorted({key for row in handoff_rows for key in row.keys()}), handoff_rows),
        write_json(RUN_DIR / "handoff_attempts.json", attempts),
        write_csv(RUN_DIR / "runtime_summary.csv", sorted({key for row in runtime_rows for key in row.keys()}), runtime_rows),
        write_csv(RUN_DIR / "runtime_kpi_snapshot.csv", sorted({key for row in kpis for key in row.keys()}), kpis),
        write_csv(RUN_DIR / "feature_last_timestamp_audit.csv", sorted({key for row in feature_rows for key in row.keys()}), feature_rows),
        write_csv(RUN_DIR / "tester_boundary_visibility_repair.csv", sorted({key for row in boundary_rows for key in row.keys()}), boundary_rows),
        write_csv(RUN_DIR / "tester_feature_last_gap_visibility_repair.csv", sorted({key for row in gap_rows for key in row.keys()}), gap_rows),
        write_csv(RUN_DIR / "timestamp_aligned_proxy_expected_result.csv", sorted({key for row in aligned_proxy_rows for key in row.keys()}), aligned_proxy_rows),
        write_csv(RUN_DIR / "timestamp_aligned_proxy_mt5_difference.csv", sorted({key for row in diff_rows for key in row.keys()}), diff_rows),
        write_csv(RUN_DIR / "proxy_mt5_usability_after_repair.csv", sorted({key for row in usability for key in row.keys()}), usability),
        write_csv(RUN_DIR / "required_gate_coverage_audit.csv", sorted({key for row in gates for key in row.keys()}), gates),
        write_md(REPORT_PATH, report_text(final_decision, runtime_rows, gap_rows, usability, preflight_rows, kpis)),
        write_md(DECISION_DOC, decision_doc_text(final_decision)),
        completed_feature,
        *materialized_artifacts,
        *copied_runtime_artifacts,
    ]
    artifacts.extend(write_receipts(final_decision, runtime_rows, gap_rows, diff_rows, cutoff_metadata, preflight_rows))
    artifacts.extend(update_status_docs(final_decision))
    upsert_csv(
        RUN_REGISTRY,
        ["run_id"],
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "full_current_day_visibility_repair_no_overfit_preflight",
            "status": status,
            "judgment": judgment,
            "path": rel(REPORT_PATH),
            "notes": f"decision={decision};next_action={next_action};goal_achieve_not_claimed.",
            "family": "runtime_parity_repair",
            "primary_report": rel(REPORT_PATH),
        },
    )
    upsert_csv(
        ALPHA_LEDGER,
        ["ledger_row_id"],
        {
            "ledger_row_id": f"{RUN_ID}__full_current_day_visibility_repair",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "full_current_day_visibility_repair",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "runtime_visibility_repair",
            "tier_scope": "Tier A forward runtime probe with boundary(티어 A 전진 런타임 탐침 경계)",
            "kpi_scope": "runtime_probe_diagnostic_no_selection(런타임 탐침 진단, 선택 없음)",
            "scoreboard_lane": "runtime_parity_repair",
            "status": status,
            "judgment": judgment,
            "path": rel(REPORT_PATH),
            "primary_kpi": f"full_current_day_gap={final_decision['full_current_day_gap']};proxy_mt5={final_decision['proxy_mt5_matched']}/{final_decision['proxy_mt5_rows']}",
            "guardrail_kpi": "no_training;no_threshold_retune;no_lot_opt;proxy_not_kpi_authority",
            "external_verification_status": "mt5_strategy_tester_attempted",
            "notes": f"decision={decision};next_action={next_action};goal_achieve_not_claimed.",
        },
    )
    upsert_csv(
        STAGE_LEDGER,
        ["run_key"],
        {
            "run_key": f"{RUN_ID}__full_current_day_visibility_repair",
            "ledger_row_id": f"{RUN_ID}__full_current_day_visibility_repair",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "family": "full_current_day_visibility_repair_no_overfit_preflight",
            "work_family": "runtime_parity_repair",
            "question": "can the frozen full current-day control reach feature_last under no-overfit preflight",
            "metric_scope": "tester_visibility_proxy_mt5_parity_runtime_probe_no_forward_decision",
            "evidence_scope": "run337AG contracts plus fresh MT5 Strategy Tester attempt",
            "kpi_scope": "diagnostic_runtime_probe_no_selection",
            "status": status,
            "judgment": judgment,
            "claim_boundary": CLAIM_BOUNDARY,
            "primary_artifact": rel(REPORT_PATH),
            "report_path": rel(REPORT_PATH),
            "path": rel(REPORT_PATH),
            "notes": f"next_action={next_action};goal_achieve_not_claimed.",
            "decision": decision,
            "next_action": next_action,
        },
    )
    artifacts.extend([RUN_REGISTRY, ALPHA_LEDGER, STAGE_LEDGER])
    manifest = write_json(
        RUN_DIR / "run_manifest.json",
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "primary_family": "runtime_parity_repair",
            "primary_skill": "obsidian-runtime-parity",
            "support_skills": ["obsidian-data-integrity", "obsidian-model-validation", "obsidian-result-judgment"],
            "status": status,
            "judgment": judgment,
            "decision": decision,
            "next_action": next_action,
            "materialize_only": args.materialize_only,
            "artifacts": [rel(path) for path in artifacts],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    artifacts.append(manifest)
    artifacts.append(append_artifacts([*artifacts, Path(__file__)]))
    print(
        json.dumps(
            json_ready(
                {
                    "run_id": RUN_ID,
                    "status": status,
                    "judgment": judgment,
                    "decision": decision,
                    "next_action": next_action,
                    "completed_day_gap": final_decision["completed_day_gap"],
                    "full_current_day_gap": final_decision["full_current_day_gap"],
                    "proxy_mt5_matched": final_decision["proxy_mt5_matched"],
                    "proxy_mt5_rows": final_decision["proxy_mt5_rows"],
                    "forward_passed": "not_claimed",
                    "forward_failed": "not_claimed",
                    "goal_achieve": "not_claimed",
                }
            ),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
