from __future__ import annotations

import argparse
import csv
import json
import math
import os
import re
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import MetaTrader5 as mt5_api
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, path_exists, sha256_file_lf_normalized  # noqa: E402
from foundation.mt5.runtime_artifacts import sha256_file  # noqa: E402
from stage_pipelines.stage335 import independent_proxy_mt5_probe as base  # noqa: E402
from stage_pipelines.stage337 import probe_custom_symbol_intraday_tester_visibility as ab  # noqa: E402
from stage_pipelines.stage337 import reprobe_tester_visibility_alternative_repair_or_rollover as ai  # noqa: E402
from stage_pipelines.stage337 import review_runtime_data_and_feature_source_repair_probe as qprobe  # noqa: E402


TODAY = "2026-05-27"
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
RUN_NUMBER = "run337AJ"
RUN_ID = "run337AJ_data_history_cache_repair_or_next_rollover_wait_reprobe_v1"
PARENT_RUN_ID = "run337AI_tester_visibility_alternative_repair_or_rollover_reprobe_v1"
NEXT_RUN_ID_REPAIRED = "run337AK_full_current_day_forward_attribution_after_cache_repair_v1"
NEXT_RUN_ID_GAP = "run337AK_next_rollover_or_synthetic_custom_parity_repair_v1"
NEXT_RUN_ID_RUNTIME_REPAIR = "run337AK_runtime_output_repair_then_cache_reprobe_v1"
CLAIM_BOUNDARY = (
    "research_development_only_stage337AJ_data_history_cache_repair_reprobe_no_model_training_"
    "no_threshold_retuning_no_lot_optimization_no_candidate_selection_no_forward_passed_no_forward_failed_"
    "no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STATUS_REPAIRED = "completed_stage337AJ_api_history_warmup_real_tick_reached_feature_last_no_forward_decision"
STATUS_GAP = "completed_stage337AJ_history_cache_warmup_gap_remains_no_forward_decision"
STATUS_RUNTIME_ISSUE = "completed_stage337AJ_runtime_issue_no_forward_decision"
STATUS_MATERIALIZED = "completed_stage337AJ_cache_repair_reprobe_materialized_execution_pending_no_forward_decision"

JUDGMENT_REPAIRED = "api_history_warmup_repaired_tester_feature_last_visibility_open_attribution_next"
JUDGMENT_GAP = "api_history_warmup_did_not_move_tester_current_day_boundary_rollover_or_synthetic_parity_repair_next"
JUDGMENT_RUNTIME_ISSUE = "runtime_or_report_output_incomplete_repair_required_before_cache_judgment"
JUDGMENT_MATERIALIZED = "cache_repair_reprobe_inputs_materialized_execution_pending"

DECISION_REPAIRED = "stage337AJ_open_run337AK_full_current_day_attribution_no_selection"
DECISION_GAP = "stage337AJ_open_run337AK_next_rollover_or_synthetic_custom_parity_repair_no_selection"
DECISION_RUNTIME_ISSUE = "stage337AJ_open_run337AK_runtime_output_repair_no_selection"
DECISION_MATERIALIZED = "stage337AJ_execution_pending_no_selection"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
RUN337Z_ATTEMPTS = STAGE_DIR / "02_runs" / "run337Z" / "rollover_reprobe_handoff_attempts.json"
MT5_DIR = RUN_DIR / "mt5"
FEATURE_COPY_DIR = RUN_DIR / "feature_matrices"
MODEL_COPY_DIR = RUN_DIR / "models"
TELEMETRY_DIR = RUN_DIR / "runtime_telemetry"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEWS_DIR / "run337AJ_data_history_cache_repair_or_next_rollover.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage337AJ_data_history_cache_repair_or_next_rollover.md"
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

COMMON_ROOT = "Project_Obsidian_Prime_v2/stage337/run337AJ_data_history_cache_repair_reprobe"
ORIGIN_SYMBOL = "US100"
BROKER_FROM_DATE = "2026.04.14"
BROKER_TO_DATE = "2026.05.30"
BROKER_WIDE_TO_DATE = "2026.06.03"
ATTEMPT_BASE = "u42_plain_rf"
FEATURE_TAIL_FROM = datetime(2026, 5, 27, 0, 0, tzinfo=UTC)
FEATURE_TAIL_TO = datetime(2026, 5, 27, 2, 10, tzinfo=UTC)

SCENARIOS = [
    {
        "suffix": "aj_api_warm_model4_real_ticks",
        "artifact_slug": "u42_plain_aj_api_warm_model4_real_ticks",
        "scenario_id": "api_warmup_model4_real_ticks_control",
        "model_code": "4",
        "model_label": "api_warm_real_ticks",
        "to_date": BROKER_TO_DATE,
    },
    {
        "suffix": "aj_api_warm_model0_generated",
        "artifact_slug": "u42_plain_aj_api_warm_model0_generated",
        "scenario_id": "api_warmup_model0_generated_bar_control",
        "model_code": "0",
        "model_label": "api_warm_generated_every_tick",
        "to_date": BROKER_TO_DATE,
    },
    {
        "suffix": "aj_api_warm_model4_wide_todate",
        "artifact_slug": "u42_plain_aj_api_warm_model4_wide_todate",
        "scenario_id": "api_warmup_model4_real_ticks_wide_todate",
        "model_code": "4",
        "model_label": "api_warm_real_ticks_wide_todate",
        "to_date": BROKER_WIDE_TO_DATE,
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
    if isinstance(value, datetime):
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
    if isinstance(value, (Mapping, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    if isinstance(value, (pd.Timestamp, datetime)):
        return value.isoformat().replace("+00:00", "Z")
    return str(value)


def number(value: Any, default: float = 0.0) -> float:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return default
    return parsed if math.isfinite(parsed) else default


def truthy(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "matched"}


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
    io_path(path).write_text(text.replace("\r\n", "\n").replace("\r", "\n").rstrip() + "\n", encoding=encoding)
    return path


def write_md(path: Path, text: str) -> Path:
    return write_text(path, text, True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stage337AJ data history cache repair and rollover reprobe.")
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
    for module in (base, qprobe, ab, ai):
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


def cache_snapshot_rows(root: Path, label: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    search_roots = [root / "Tester" / "bases", root / "Tester" / "cache", root / "bases"]
    for search_root in search_roots:
        if not path_exists(search_root):
            continue
        for path in io_path(search_root).rglob("*"):
            if not path.is_file():
                continue
            name = path.name
            full = path.as_posix()
            if "US100" not in full and "ObsidianPrimeV2_RuntimeProbeEA" not in name:
                continue
            stat = path.stat()
            rows.append(
                {
                    "snapshot_label": label,
                    "path": full,
                    "relative_to_portable": path.relative_to(io_path(root)).as_posix() if str(path).startswith(str(io_path(root))) else full,
                    "name": name,
                    "suffix": path.suffix,
                    "size_bytes": stat.st_size,
                    "mtime_utc": datetime.fromtimestamp(stat.st_mtime, tz=UTC).isoformat().replace("+00:00", "Z"),
                    "is_us100_history_or_tick": "US100" in full,
                    "is_tester_cache": "Tester/cache" in full.replace("\\", "/"),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    rows.sort(key=lambda row: (str(row["relative_to_portable"]), str(row["mtime_utc"])))
    return rows


def rates_summary(label: str, timeframe_name: str, rates: Any, bar_seconds: int) -> dict[str, Any]:
    if rates is None or len(rates) == 0:
        return {
            "warmup_label": label,
            "timeframe": timeframe_name,
            "rows": 0,
            "first_open_utc": "",
            "last_open_utc": "",
            "last_close_utc": "",
            "first_close": "",
            "last_close": "",
        }
    first_open = datetime.fromtimestamp(int(rates[0]["time"]), tz=UTC)
    last_open = datetime.fromtimestamp(int(rates[-1]["time"]), tz=UTC)
    return {
        "warmup_label": label,
        "timeframe": timeframe_name,
        "rows": int(len(rates)),
        "first_open_utc": first_open.isoformat().replace("+00:00", "Z"),
        "last_open_utc": last_open.isoformat().replace("+00:00", "Z"),
        "last_close_utc": (last_open + timedelta(seconds=bar_seconds)).isoformat().replace("+00:00", "Z"),
        "first_close": float(rates[0]["close"]),
        "last_close": float(rates[-1]["close"]),
    }


def ticks_summary(label: str, ticks: Any) -> dict[str, Any]:
    if ticks is None or len(ticks) == 0:
        return {"warmup_label": label, "timeframe": "ticks", "rows": 0, "first_time_utc": "", "last_time_utc": ""}
    first_time = datetime.fromtimestamp(int(ticks[0]["time"]), tz=UTC)
    last_time = datetime.fromtimestamp(int(ticks[-1]["time"]), tz=UTC)
    return {
        "warmup_label": label,
        "timeframe": "ticks",
        "rows": int(len(ticks)),
        "first_time_utc": first_time.isoformat().replace("+00:00", "Z"),
        "last_time_utc": last_time.isoformat().replace("+00:00", "Z"),
        "first_bid": float(ticks[0]["bid"]),
        "last_bid": float(ticks[-1]["bid"]),
    }


def mt5_history_warmup(terminal_path: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    started_at = now_utc()
    ok = mt5_api.initialize(path=str(terminal_path), portable=True)
    if not ok:
        return (
            {
                "status": "blocked_mt5_initialize_failed",
                "started_at_utc": started_at,
                "finished_at_utc": now_utc(),
                "last_error": str(mt5_api.last_error()),
                "effect": "MT5 API history warmup(API 이력 예열)을 시작하지 못해 tester cache(테스터 캐시) 수리 효과를 볼 수 없음.",
            },
            rows,
        )
    try:
        selected = mt5_api.symbol_select(ORIGIN_SYMBOL, True)
        if not selected:
            return (
                {
                    "status": "blocked_symbol_select_failed",
                    "started_at_utc": started_at,
                    "finished_at_utc": now_utc(),
                    "last_error": str(mt5_api.last_error()),
                    "effect": "US100 symbol select(심볼 선택)가 실패해 API warmup(API 예열)이 막힘.",
                },
                rows,
            )
        now_dt = datetime.now(tz=UTC)
        ranges = [
            ("feature_tail_20260527_0000_0210", FEATURE_TAIL_FROM, FEATURE_TAIL_TO),
            ("recent_12h", now_dt - timedelta(hours=12), now_dt),
            ("full_forward_tail_20260526_to_now", datetime(2026, 5, 26, 0, 0, tzinfo=UTC), now_dt),
        ]
        for label, start, end in ranges:
            for timeframe_name, timeframe, seconds in (
                ("M1", mt5_api.TIMEFRAME_M1, 60),
                ("M5", mt5_api.TIMEFRAME_M5, 300),
            ):
                rates = mt5_api.copy_rates_range(ORIGIN_SYMBOL, timeframe, start, end)
                row = rates_summary(label, timeframe_name, rates, seconds)
                row.update({"range_start_utc": start.isoformat().replace("+00:00", "Z"), "range_end_utc": end.isoformat().replace("+00:00", "Z")})
                row["last_error"] = str(mt5_api.last_error())
                row["claim_boundary"] = CLAIM_BOUNDARY
                rows.append(row)
        tick_ranges = [
            ("feature_last_10m_ticks_0155_0205", datetime(2026, 5, 27, 1, 55, tzinfo=UTC), datetime(2026, 5, 27, 2, 5, tzinfo=UTC)),
            ("recent_30m_ticks", now_dt - timedelta(minutes=30), now_dt),
        ]
        for label, start, end in tick_ranges:
            ticks = mt5_api.copy_ticks_range(ORIGIN_SYMBOL, start, end, mt5_api.COPY_TICKS_ALL)
            row = ticks_summary(label, ticks)
            row.update({"range_start_utc": start.isoformat().replace("+00:00", "Z"), "range_end_utc": end.isoformat().replace("+00:00", "Z")})
            row["last_error"] = str(mt5_api.last_error())
            row["claim_boundary"] = CLAIM_BOUNDARY
            rows.append(row)
        return (
            {
                "status": "completed",
                "started_at_utc": started_at,
                "finished_at_utc": now_utc(),
                "symbol": ORIGIN_SYMBOL,
                "last_error": str(mt5_api.last_error()),
                "warmup_rows": len(rows),
                "effect": "MT5 API history warmup(API 이력 예열)으로 terminal history cache(터미널 이력 캐시)에 US100 현재일 구간 읽기를 강제함.",
            },
            rows,
        )
    finally:
        mt5_api.shutdown()


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
    for index, scenario in enumerate(SCENARIOS):
        copied = dict(source)
        copied["attempt_name"] = f"u42_plain_rf_{scenario['suffix']}"
        copied["artifact_slug"] = scenario["artifact_slug"]
        copied["scenario_id"] = scenario["scenario_id"]
        copied["scenario_symbol"] = ORIGIN_SYMBOL
        copied["scenario_from_date"] = BROKER_FROM_DATE
        copied["scenario_to_date"] = scenario["to_date"]
        copied["scenario_model"] = scenario["model_code"]
        copied["tester_model_label"] = scenario["model_label"]
        copied["model_copy"] = {"source": source.get("model_local_path") or source.get("model_copy", {}).get("source", "")}
        copied["feature_export"] = {"path": source.get("feature_local_path", "")}
        copied["feature_local_path"] = source.get("feature_local_path", "")
        copied["source_run_id"] = PARENT_RUN_ID
        copied["attempt_role"] = "stage337AJ_api_history_cache_repair_reprobe_same_frozen_u42_model_threshold_risk"
        copied["record_view_prefix"] = f"mt5_stage337AJ_u42_plain_api_warm_{index}"
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
    attempt["attempt_role"] = "stage337AJ_api_history_cache_repair_reprobe_same_frozen_u42_model_threshold_risk"
    attempt["record_view_prefix"] = f"mt5_stage337AJ_{attempt['artifact_slug']}"
    attempt["source_run_id"] = PARENT_RUN_ID
    attempt["repair_contract"] = (
        "MT5 API history warmup plus tester re-run only; same ONNX, feature order, D/B surface, score threshold, "
        "risk, lot, and ATR SL/TP; Model/ToDate changes are diagnostic tester-boundary probes"
    )
    attempt["signal_policy"] = "cache repair diagnostic only; not Forward Passed/Failed authority"
    return attempt


def runtime_completed(row: Mapping[str, Any]) -> bool:
    return (
        str(row.get("tester_status", "")) == "completed"
        and str(row.get("runtime_status", "")) == "completed"
        and str(row.get("report_status", "")) == "completed"
    )


def classify(runtime_rows: Sequence[Mapping[str, Any]], matrix_rows: Sequence[Mapping[str, Any]], materialize_only: bool) -> tuple[str, str, str, str]:
    if materialize_only:
        return STATUS_MATERIALIZED, JUDGMENT_MATERIALIZED, DECISION_MATERIALIZED, RUN_ID
    if not runtime_rows or any(not runtime_completed(row) for row in runtime_rows):
        return STATUS_RUNTIME_ISSUE, JUDGMENT_RUNTIME_ISSUE, DECISION_RUNTIME_ISSUE, NEXT_RUN_ID_RUNTIME_REPAIR
    real_tick_reached = any(
        str(row.get("tester_model", "")) == "4" and row.get("gap_status") == "tester_reached_feature_last" for row in matrix_rows
    )
    if real_tick_reached:
        return STATUS_REPAIRED, JUDGMENT_REPAIRED, DECISION_REPAIRED, NEXT_RUN_ID_REPAIRED
    return STATUS_GAP, JUDGMENT_GAP, DECISION_GAP, NEXT_RUN_ID_GAP


def repair_matrix_rows(
    runtime_rows: Sequence[Mapping[str, Any]],
    gap_rows: Sequence[Mapping[str, Any]],
    usability_rows: Sequence[Mapping[str, Any]],
    boundary_rows: Sequence[Mapping[str, Any]],
    attempts: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    rows = ai.model_mode_matrix_rows(runtime_rows, gap_rows, usability_rows, boundary_rows, attempts)
    for row in rows:
        if row.get("gap_status") == "tester_reached_feature_last":
            row["cache_repair_read"] = "api_warmup_moved_tester_boundary"
        else:
            row["cache_repair_read"] = "api_warmup_did_not_move_tester_boundary"
        row["claim_boundary"] = CLAIM_BOUNDARY
    return rows


def decision_payload(
    status: str,
    judgment: str,
    decision: str,
    next_action: str,
    warmup_payload: Mapping[str, Any],
    broker_api: Mapping[str, Any],
    runtime_rows: Sequence[Mapping[str, Any]],
    gap_rows: Sequence[Mapping[str, Any]],
    usability_rows: Sequence[Mapping[str, Any]],
    matrix_rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    completed = sum(1 for row in runtime_rows if runtime_completed(row))
    reached = sum(1 for row in gap_rows if row.get("gap_status") == "tester_reached_feature_last")
    matched = int(sum(number(row.get("proxy_matched"), 0.0) for row in usability_rows))
    total = int(sum(number(row.get("proxy_total"), 0.0) for row in usability_rows))
    real_tick_rows = [row for row in matrix_rows if str(row.get("tester_model", "")) == "4"]
    real_tick_reached = sum(1 for row in real_tick_rows if row.get("gap_status") == "tester_reached_feature_last")
    max_gap = max((number(row.get("tester_to_feature_last_gap_minutes"), 0.0) for row in matrix_rows), default=0.0)
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": status,
        "judgment": judgment,
        "decision": decision,
        "next_action": next_action,
        "warmup_status": warmup_payload.get("status", ""),
        "broker_api_status": broker_api.get("status", ""),
        "broker_api_m5_last_close_utc": broker_api.get("m5_last_close_utc", ""),
        "runtime_completed": completed,
        "runtime_total": len(runtime_rows),
        "tester_reached_feature_last": reached,
        "tester_gap_total": len(gap_rows),
        "real_tick_reached_feature_last": real_tick_reached,
        "real_tick_total": len(real_tick_rows),
        "max_tester_to_feature_last_gap_minutes": max_gap,
        "proxy_mt5_matched": matched,
        "proxy_mt5_rows": total,
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def gate_rows(final_decision: Mapping[str, Any], warmup_rows: Sequence[Mapping[str, Any]], runtime_rows: Sequence[Mapping[str, Any]], matrix_rows: Sequence[Mapping[str, Any]], usability_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    proxy_total = sum(number(row.get("proxy_total"), 0.0) for row in usability_rows)
    proxy_matched = sum(number(row.get("proxy_matched"), 0.0) for row in usability_rows)
    gates = [
        ("frozen_identity_lock", "passed", "same ONNX/model/feature/threshold/risk/lot; API warmup is data-cache diagnostic"),
        ("api_history_warmup_attempted", "passed" if warmup_rows else "blocked", "US100 M1/M5 and feature-tail tick ranges are read through MT5 API"),
        ("mt5_execution_completed", "passed" if runtime_rows and all(runtime_completed(row) for row in runtime_rows) else "blocked", "all tester/runtime/report outputs must complete"),
        ("feature_last_gap_measured", "passed" if matrix_rows else "blocked", "tester last observed bar is compared with feature_last after cache warmup"),
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


def receipt_payloads(final_decision: Mapping[str, Any]) -> dict[Path, Mapping[str, Any]]:
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
            "data_source": "MT5 API US100 M1/M5/ticks plus Strategy Tester telemetry",
            "time_axis": "UTC bar close/open convention recorded in warmup and tester gap CSV",
            "integrity_judgment": "usable_with_boundary",
            "effect": "API-visible current-day data is separated from tester-visible current-day data.",
        },
        RUN_DIR / "runtime_parity_receipt.json": {
            **common,
            "receipt_type": "runtime_parity",
            "proxy_mt5_matched": final_decision.get("proxy_mt5_matched", 0),
            "proxy_mt5_rows": final_decision.get("proxy_mt5_rows", 0),
            "runtime_claim_boundary": "runtime_probe_research_only",
            "effect": "Python proxy and MT5 runtime are compared only over tester-observed rows.",
        },
        RUN_DIR / "model_validation_receipt.json": {
            **common,
            "receipt_type": "model_validation",
            "model_training": "forbidden_not_performed",
            "threshold_retuning": "forbidden_not_performed",
            "validation_judgment": "inconclusive_runtime_boundary",
            "effect": "No model or threshold was selected from current-day data.",
        },
        RUN_DIR / "result_judgment_receipt.json": {
            **common,
            "receipt_type": "result_judgment",
            "judgment": final_decision.get("judgment", ""),
            "claim_boundary": CLAIM_BOUNDARY,
            "effect": "The result is a cache-boundary judgment, not a forward pass/fail judgment.",
        },
        RUN_DIR / "experiment_design_receipt.json": {
            **common,
            "receipt_type": "experiment_design",
            "hypothesis": "If API warmup populates tester-visible current-day history, tester last observed should reach feature_last.",
            "stop_condition": "Do not change ONNX, feature order, threshold, D/B rule, lot, risk, or ATR exits.",
            "effect": "The next action is driven by cache movement or non-movement, not by KPI chasing.",
        },
    }


def report_text(final_decision: Mapping[str, Any], warmup_rows: Sequence[Mapping[str, Any]], matrix_rows: Sequence[Mapping[str, Any]], kpi_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "# Stage337AJ Data History Cache Repair Or Next Rollover(337AJ 데이터 이력 캐시 수리 또는 다음 이월)",
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
        "이번 실행은 MT5 API history warmup(API 이력 예열)으로 US100 current-day(현재일) M1/M5/tick(1분/5분/틱) 구간을 먼저 읽고, 같은 frozen ONNX(고정 ONNX)를 다시 Strategy Tester(전략 테스터)에 넣었다.",
        "Effect(효과): API-visible data(API에서 보이는 데이터)가 tester-visible data(테스터에서 보이는 데이터)로 넘어가는지 직접 본다.",
        "",
        "## Warmup(API 예열)",
        "",
        "| label(라벨) | type(유형) | rows(행) | last close/time(마지막 시각) |",
        "|---|---|---:|---|",
    ]
    for row in warmup_rows:
        last = row.get("last_close_utc") or row.get("last_time_utc") or ""
        lines.append(f"| `{row.get('warmup_label', '')}` | `{row.get('timeframe', '')}` | `{row.get('rows', '')}` | `{last}` |")
    lines.extend(
        [
            "",
            "## Tester Repair Matrix(테스터 수리 행렬)",
            "",
            "| attempt(시도) | model(모델) | to feature gap(피처 공백) | last observed(마지막 관측) | feature last(피처 끝) | proxy(프록시) | cache read(캐시 판독) |",
            "|---|---:|---:|---|---|---:|---|",
        ]
    )
    for row in matrix_rows:
        lines.append(
            f"| `{row.get('attempt_name', '')}` | `{row.get('tester_model', '')}` | `{row.get('tester_to_feature_last_gap_minutes', '')}` | "
            f"`{row.get('tester_last_observed_bar_time', '')}` | `{row.get('feature_last_timestamp', '')}` | "
            f"`{row.get('proxy_matched', '')}/{row.get('proxy_total', '')}` | `{row.get('cache_repair_read', '')}` |"
        )
    lines.extend(
        [
            "",
            "## KPI Snapshot(KPI 스냅샷)",
            "",
            "KPI(핵심 지표)는 cache repair diagnostic(캐시 수리 진단) 참고값이며 Forward authority(전방 권위)가 아니다.",
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
            "- runtime_authority(런타임 권위): `not_claimed`",
            "- live_readiness(실거래 준비): `not_claimed`",
            "",
            "Effect(효과): cache warmup(API 예열) 이후에도 tester boundary(테스터 경계)가 남으면 다음 작업은 rollover(이월) 또는 synthetic custom parity repair(합성 커스텀 동등성 수리)로 넘어간다.",
        ]
    )
    return "\n".join(lines)


def decision_doc_text(final_decision: Mapping[str, Any]) -> str:
    return "\n".join(
        [
            "# 2026-05-27 Stage337AJ Decision(337AJ 결정)",
            "",
            f"- run_id(실행 ID): `{RUN_ID}`",
            f"- status(상태): `{final_decision['status']}`",
            f"- judgment(판정): `{final_decision['judgment']}`",
            f"- decision(결정): `{final_decision['decision']}`",
            f"- next_action(다음 행동): `{final_decision['next_action']}`",
            f"- warmup_status(API 예열 상태): `{final_decision['warmup_status']}`",
            f"- real_tick_reached_feature_last(real tick 피처 끝 도달): `{final_decision['real_tick_reached_feature_last']}/{final_decision['real_tick_total']}`",
            f"- proxy_mt5_parity(프록시/MT5 동등성): `{final_decision['proxy_mt5_matched']}/{final_decision['proxy_mt5_rows']}`",
            "- Forward Passed(전방 통과): `not_claimed`",
            "- Forward Failed(전방 실패): `not_claimed`",
            "- Goal Achieve(목표 달성): `not_claimed`",
            "",
            "Effect(효과): MT5 API history warmup(API 이력 예열)의 tester cache(테스터 캐시) 효과만 판단했고 운영 주장은 열지 않는다.",
        ]
    )


def replace_line(text: str, prefix: str, replacement: str) -> str:
    if re.search(rf"^{re.escape(prefix)}.*$", text, flags=re.M):
        return re.sub(rf"^{re.escape(prefix)}.*$", replacement, text, count=1, flags=re.M)
    return text.rstrip() + "\n" + replacement + "\n"


def upsert_focus_block(text: str, block: str) -> str:
    pattern = r"- >-\n  Stage337 run337AJ focus complete:.*?(?=\n- >-|\Z)"
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
- warmup_status(API 예열 상태): `{final_decision['warmup_status']}`
- real_tick_reached_feature_last(real tick 피처 끝 도달): `{final_decision['real_tick_reached_feature_last']}/{final_decision['real_tick_total']}`
- max_tester_to_feature_last_gap_minutes(최대 테스터-피처 공백 분): `{final_decision['max_tester_to_feature_last_gap_minutes']}`
- proxy_mt5_parity(프록시/MT5 동등성): `{final_decision['proxy_mt5_matched']}/{final_decision['proxy_mt5_rows']}`
- Forward Passed(전방 통과): `not_claimed`
- Forward Failed(전방 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final_decision['next_action']}`
- effect(효과): run337AJ(337AJ 실행)는 MT5 API history warmup(API 이력 예열) 후 tester cache(테스터 캐시) 이동 여부를 재탐침했다. Forward/Goal(전방/목표)은 주장하지 않는다.
"""
    changed.append(write_md(SELECTED_STATUS, selected_text))
    focus = (
        f"Stage337 run337AJ focus complete: run337AJ(337AJ 실행)는 `{final_decision['status']}`로 "
        f"data history cache repair reprobe(데이터 이력 캐시 수리 재탐침)를 완료했다. "
        f"Effect(효과): warmup(API 예열) `{final_decision['warmup_status']}`, real_tick_reached(실제 틱 도달) "
        f"`{final_decision['real_tick_reached_feature_last']}/{final_decision['real_tick_total']}`, proxy/MT5 parity(프록시/MT5 동등성) "
        f"`{final_decision['proxy_mt5_matched']}/{final_decision['proxy_mt5_rows']}`이고 Forward/Goal(전방/목표)은 주장하지 않는다."
    )
    if path_exists(WORKSPACE_STATE):
        text, bom = read_text(WORKSPACE_STATE)
        text = replace_line(text, "current_run_id:", f"current_run_id: {final_decision['next_action']}")
        text = replace_line(text, "updated_on:", f"updated_on: '{TODAY}'")
        text = upsert_focus_block(text, focus)
        changed.append(write_text(WORKSPACE_STATE, text, bom))
    if path_exists(CURRENT_STATE):
        text, bom = read_text(CURRENT_STATE)
        entry = f"""## Stage337 run337AJ(337AJ 실행) - {TODAY}

- status(상태): `{final_decision['status']}`
- decision(결정): `{final_decision['decision']}`
- next_action(다음 행동): `{final_decision['next_action']}`
- effect(효과): MT5 API history warmup(API 이력 예열) 후 tester cache(테스터 캐시)가 feature_last(피처 끝)까지 움직이는지 검증했다. Forward Passed/Failed(전방 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.
"""
        if "## Stage337 run337AJ(337AJ 실행)" in text:
            text = re.sub(r"## Stage337 run337AJ\(337AJ 실행\).*?(?=\n## |\Z)", entry.strip(), text, count=1, flags=re.S)
        else:
            text = text.rstrip() + "\n\n" + entry.strip() + "\n"
        changed.append(write_text(CURRENT_STATE, text, bom))
    if path_exists(CHANGELOG):
        text, bom = read_text(CHANGELOG)
        line = (
            f"- {TODAY}: Stage337 run337AJ(337AJ 실행) `{final_decision['status']}`. "
            f"Effect(효과): API history warmup(API 이력 예열) 후 tester cache(테스터 캐시) 경계를 재탐침했고 Forward/Goal(전방/목표)은 주장하지 않음."
        )
        if "Stage337 run337AJ(337AJ 실행)" not in text:
            text = text.rstrip() + "\n" + line + "\n"
        changed.append(write_text(CHANGELOG, text, bom))
    if path_exists(STAGE_BRIEF):
        text, bom = read_text(STAGE_BRIEF)
        text = re.sub(r"- latest_run\([^)]*\): `[^`]*`", f"- latest_run(최신 실행): `{RUN_ID}`", text, count=1)
        summary = (
            f"- run337AJ_summary(337AJ 요약): `{final_decision['status']}`. "
            f"Effect(효과): warmup(API 예열) `{final_decision['warmup_status']}`, real tick reached(실제 틱 도달) "
            f"`{final_decision['real_tick_reached_feature_last']}/{final_decision['real_tick_total']}`, proxy parity(프록시 동등성) "
            f"`{final_decision['proxy_mt5_matched']}/{final_decision['proxy_mt5_rows']}`를 기록했다.\n"
        )
        if "run337AJ_summary(337AJ 요약)" in text:
            text = re.sub(r"- run337AJ_summary\(337AJ 요약\): [^\n]*(?:\n|$)", summary, text, count=1)
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
        "lane": "data_history_cache_repair_reprobe",
        "status": final_decision["status"],
        "judgment": final_decision["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"decision={final_decision['decision']};next_action={final_decision['next_action']};goal_achieve_not_claimed.",
        "family": "runtime_parity_repair",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__data_history_cache_repair_reprobe",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "data_history_cache_repair_reprobe",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "runtime_visibility_repair",
        "tier_scope": "Tier A forward runtime probe with API history warmup(티어 A 전방 런타임 탐침, API 이력 예열)",
        "kpi_scope": "diagnostic_runtime_probe_no_selection(진단 런타임 탐침, 선택 없음)",
        "scoreboard_lane": "runtime_parity_repair",
        "status": final_decision["status"],
        "judgment": final_decision["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"real_tick_reached={final_decision['real_tick_reached_feature_last']}/{final_decision['real_tick_total']};proxy_mt5={final_decision['proxy_mt5_matched']}/{final_decision['proxy_mt5_rows']}",
        "guardrail_kpi": "no_training;no_threshold_retune;no_lot_opt;cache_probe_not_kpi_authority",
        "external_verification_status": "mt5_strategy_tester_attempted",
        "notes": f"decision={final_decision['decision']};next_action={final_decision['next_action']};goal_achieve_not_claimed.",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__data_history_cache_repair_reprobe",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "runtime_parity_repair",
        "evidence_scope": "MT5 API warmup, tester logs, runtime telemetry, timestamp-aligned proxy parity",
        "kpi_scope": "diagnostic_runtime_probe_not_forward_kpi",
        "status": final_decision["status"],
        "judgment": final_decision["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={final_decision['next_action']};goal_achieve_not_claimed.",
        "decision": final_decision["decision"],
        "run_key": f"{RUN_ID}__data_history_cache_repair_reprobe",
        "family": "data_history_cache_repair_reprobe",
        "question": "does MT5 API history warmup move tester current-day feature_last boundary",
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

    cache_before = cache_snapshot_rows(terminal_data_root, "before_api_history_warmup")
    pre_warmup_recovery = qprobe.stop_target_terminal_if_running(terminal_path)
    warmup_payload, warmup_rows = (
        ({"status": "not_attempted_materialize_only", "effect": "materialize-only(물질화 전용) 실행"}, [])
        if args.materialize_only
        else mt5_history_warmup(terminal_path)
    )
    cache_after_warmup = cache_snapshot_rows(terminal_data_root, "after_api_history_warmup")
    post_warmup_recovery = qprobe.stop_target_terminal_if_running(terminal_path)
    broker_api = ab.mt5_api_symbol_visibility(terminal_path, ORIGIN_SYMBOL)
    post_broker_api_recovery = qprobe.stop_target_terminal_if_running(terminal_path)

    source = load_source_u42()
    prepared = build_source_attempts(source)
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
    execution_result["pre_warmup_recovery"] = pre_warmup_recovery
    execution_result["warmup"] = warmup_payload
    execution_result["post_warmup_recovery"] = post_warmup_recovery
    execution_result["post_broker_api_recovery"] = post_broker_api_recovery

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
        default_source="stage337AJ_timestamp_aligned_python_onnx_inference_after_api_warmup",
    )
    diff_rows = base.build_signal_difference_rows(aligned_proxy_rows, runtime_rows)
    for row in diff_rows:
        row["mt5_source"] = "stage337AJ_runtime_summary_after_api_history_warmup"
        row["usable_for_forward_pass_fail"] = False
        row["claim_boundary"] = CLAIM_BOUNDARY
    usability = ai.proxy_usability_rows(gap_rows, diff_rows, attempts)
    kpis = ai.runtime_kpi_rows(runtime_rows, attempts)
    matrix = repair_matrix_rows(runtime_rows, gap_rows, usability, boundary_rows, attempts)
    status, judgment, decision, next_action = classify(runtime_rows, matrix, args.materialize_only)
    final_decision = decision_payload(status, judgment, decision, next_action, warmup_payload, broker_api, runtime_rows, gap_rows, usability, matrix)
    gates = gate_rows(final_decision, warmup_rows, runtime_rows, matrix, usability)

    artifacts: list[Path] = [
        write_csv(RUN_DIR / "history_cache_snapshot_before.csv", columns_for(cache_before, ["status"]), cache_before),
        write_json(RUN_DIR / "pre_warmup_terminal_recovery.json", pre_warmup_recovery),
        write_json(RUN_DIR / "api_history_warmup.json", warmup_payload),
        write_csv(RUN_DIR / "api_history_warmup.csv", columns_for(warmup_rows, ["status"]), warmup_rows),
        write_csv(RUN_DIR / "history_cache_snapshot_after_warmup.csv", columns_for(cache_after_warmup, ["status"]), cache_after_warmup),
        write_json(RUN_DIR / "post_warmup_terminal_recovery.json", post_warmup_recovery),
        write_json(RUN_DIR / "post_broker_api_terminal_recovery.json", post_broker_api_recovery),
        write_json(RUN_DIR / "execution_result.json", execution_result),
        write_json(RUN_DIR / "final_data_history_cache_repair_decision.json", final_decision),
        write_csv(RUN_DIR / "mt5_api_visibility.csv", columns_for([broker_api], ["status"]), [broker_api]),
        write_csv(RUN_DIR / "handoff_attempts.csv", columns_for(handoff_rows, ["status"]), handoff_rows),
        write_json(RUN_DIR / "handoff_attempts.json", attempts),
        write_csv(RUN_DIR / "runtime_summary.csv", columns_for(runtime_rows, ["status"]), runtime_rows),
        write_csv(RUN_DIR / "runtime_kpi_snapshot.csv", columns_for(kpis, ["status"]), kpis),
        write_csv(RUN_DIR / "feature_last_timestamp_audit.csv", columns_for(feature_rows, ["status"]), feature_rows),
        write_csv(RUN_DIR / "tester_boundary_cache_repair_reprobe.csv", columns_for(boundary_rows, ["status"]), boundary_rows),
        write_csv(RUN_DIR / "tester_feature_last_gap_cache_repair_reprobe.csv", columns_for(gap_rows, ["status"]), gap_rows),
        write_csv(RUN_DIR / "timestamp_aligned_proxy_expected_result.csv", columns_for(aligned_proxy_rows, ["status"]), aligned_proxy_rows),
        write_csv(RUN_DIR / "timestamp_aligned_proxy_mt5_difference.csv", columns_for(diff_rows, ["status"]), diff_rows),
        write_csv(RUN_DIR / "proxy_mt5_usability_cache_repair.csv", columns_for(usability, ["status"]), usability),
        write_csv(RUN_DIR / "cache_repair_matrix.csv", columns_for(matrix, ["status"]), matrix),
        write_csv(RUN_DIR / "required_gate_coverage_audit.csv", columns_for(gates, ["status"]), gates),
        write_md(REPORT_PATH, report_text(final_decision, warmup_rows, matrix, kpis)),
        write_md(DECISION_DOC, decision_doc_text(final_decision)),
        *materialized_artifacts,
        *copied_runtime_artifacts,
    ]
    for path, payload in receipt_payloads(final_decision).items():
        artifacts.append(write_json(path, payload))
    artifacts.extend(update_status_docs(final_decision))
    artifacts.extend(update_registers(final_decision))
    manifest = write_json(
        RUN_DIR / "run_manifest.json",
        {
            **final_decision,
            "generated_at_utc": now_utc(),
            "command": "python stage_pipelines/stage337/reprobe_data_history_cache_repair_or_next_rollover.py",
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
