from __future__ import annotations

import argparse
import csv
import json
import math
import shutil
import subprocess
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Mapping, Sequence

import MetaTrader5 as mt5_api
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, path_exists, sha256_file_lf_normalized  # noqa: E402
from foundation.mt5.runtime_artifacts import sha256_file  # noqa: E402
from stage_pipelines.stage335 import independent_proxy_mt5_probe as base  # noqa: E402


TODAY = "2026-05-27"
STAGE_ID = "336_onnx_research_packet__constraint_bound_repair_defense_offense_rebuild"
RUN_NUMBER = "run336K"
RUN_ID = "run336K_attempt_fresh_mt5_runtime_probe_or_block_v1"
PARENT_RUN_ID = "run336J_materialize_proxy_expected_fresh_mt5_probe_inputs_v1"
NEXT_RUN_ID = "run336L_review_fresh_mt5_runtime_probe_and_repair_or_rebuild_decision_v1"
CLAIM_BOUNDARY = (
    "research_development_only_stage336K_fresh_mt5_runtime_probe_attempt_no_model_training_"
    "no_threshold_retuning_no_lot_optimization_no_direct_forward_pocket_filtering_"
    "no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_"
    "no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STATUS_COMPLETED = "completed_fresh_mt5_runtime_probe_attempt_materialized_no_forward_decision"
STATUS_PARTIAL = "completed_fresh_mt5_runtime_probe_attempt_with_feature_handoff_gaps_no_forward_decision"
STATUS_MATERIALIZED_ONLY = "completed_fresh_mt5_runtime_probe_inputs_materialized_execution_pending_no_forward_decision"
JUDGMENT_COMPLETED = "fresh_mt5_runtime_probe_completed_diagnostic_only_latest_feature_gap_audited"
JUDGMENT_PARTIAL = "fresh_mt5_runtime_probe_attempted_or_materialized_with_runtime_or_feature_gap_no_forward_decision"
DECISION_COMPLETED = "stage336K_fresh_mt5_probe_diagnostic_usable_not_forward_usable_no_selection"
DECISION_PARTIAL = "stage336K_fresh_mt5_probe_repair_required_before_forward_or_runtime_claim"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MT5_DIR = RUN_DIR / "mt5"
FEATURE_COPY_DIR = RUN_DIR / "feature_matrices"
MODEL_COPY_DIR = RUN_DIR / "models"
TELEMETRY_DIR = RUN_DIR / "runtime_telemetry"
RAW_REFRESH_DIR = RUN_DIR / "raw_refresh_probe"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage336K_fresh_mt5_runtime_probe.md"

DEFAULT_PORTABLE_ROOT = Path(r"C:\Users\awdse\AppData\Local\ObsidianPrime\mt5_portable_run329E")
DEFAULT_TERMINAL = DEFAULT_PORTABLE_ROOT / "terminal64.exe"
DEFAULT_METAEDITOR = DEFAULT_PORTABLE_ROOT / "MetaEditor64.exe"
DEFAULT_COMMON_FILES = DEFAULT_PORTABLE_ROOT / "Common" / "Files"
DEFAULT_TESTER_PROFILE_ROOT = DEFAULT_PORTABLE_ROOT / "MQL5" / "Profiles" / "Tester"
DEFAULT_TERMINAL_DATA_ROOT = DEFAULT_PORTABLE_ROOT
COMMON_ROOT = "Project_Obsidian_Prime_v2/stage336/run336K_fresh_mt5_runtime_probe"

BRANCH_ATTEMPT_MAP = [
    ("repair_proxy_exclusion_handoff_contract", "c56_plain_rf"),
    ("defense_cost_curve_underwater_gate", "c56_bal_rf"),
    ("defense_direction_symmetry_negative_control", "u42_bal_rf"),
    ("offense_m48_plain_density_quality_seed", "m48_plain_rf"),
    ("offense_cost_buffer_feature_interaction_seed", "m48_bal_rf"),
    ("runtime_parity_probe_bridge_contract", "u42_plain_rf"),
]

RAW_SYMBOLS = (
    ("US100", "US100"),
    ("VIX", "VIX"),
    ("US10YR", "US10YR"),
    ("USDX", "USDX"),
)

M5_SECONDS = 300


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return ""
        return f"{value:.12g}"
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
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def write_md(path: Path, text: str) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")
    return path


def simple_upsert_csv(path: Path, rows: Sequence[Mapping[str, Any]], *, key: str) -> None:
    existing: list[dict[str, str]] = []
    columns: list[str] = []
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            columns = list(reader.fieldnames or [])
            existing = [dict(row) for row in reader]
    if not columns:
        for row in rows:
            for column in row:
                if column not in columns:
                    columns.append(column)
    keys = {str(row.get(key, "")) for row in rows}
    merged = [row for row in existing if str(row.get(key, "")) not in keys]
    merged.extend({column: csv_value(row.get(column, "")) for column in columns} for row in rows)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        writer.writerows(merged)


def patch_base_module() -> None:
    base.TODAY = TODAY
    base.STAGE_ID = STAGE_ID
    base.RUN_NUMBER = RUN_NUMBER
    base.RUN_ID = RUN_ID
    base.PARENT_RUN_ID = PARENT_RUN_ID
    base.NEXT_RUN_ID = NEXT_RUN_ID
    base.STATUS_COMPLETED = STATUS_COMPLETED
    base.STATUS_PARTIAL = STATUS_PARTIAL
    base.STATUS_MATERIALIZED_ONLY = STATUS_MATERIALIZED_ONLY
    base.JUDGMENT_COMPLETED = JUDGMENT_COMPLETED
    base.JUDGMENT_PARTIAL = JUDGMENT_PARTIAL
    base.DECISION_COMPLETED = DECISION_COMPLETED
    base.DECISION_PARTIAL = DECISION_PARTIAL
    base.CLAIM_BOUNDARY = CLAIM_BOUNDARY
    base.STAGE_DIR = STAGE_DIR
    base.RUN_DIR = RUN_DIR
    base.MT5_DIR = MT5_DIR
    base.FEATURE_COPY_DIR = FEATURE_COPY_DIR
    base.MODEL_COPY_DIR = MODEL_COPY_DIR
    base.TELEMETRY_DIR = TELEMETRY_DIR
    base.REVIEWS_DIR = REVIEWS_DIR
    base.SELECTED_DIR = STAGE_DIR / "04_selected"
    base.STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
    base.INPUT_REFS = STAGE_DIR / "01_inputs" / "input_refs.md"
    base.STAGE_LEDGER = STAGE_LEDGER
    base.RUN_REGISTRY = RUN_REGISTRY
    base.ARTIFACT_REGISTRY = ARTIFACT_REGISTRY
    base.DECISION_DOC = DECISION_DOC
    base.DEFAULT_PORTABLE_ROOT = DEFAULT_PORTABLE_ROOT
    base.DEFAULT_TERMINAL = DEFAULT_TERMINAL
    base.DEFAULT_METAEDITOR = DEFAULT_METAEDITOR
    base.DEFAULT_COMMON_FILES = DEFAULT_COMMON_FILES
    base.DEFAULT_TESTER_PROFILE_ROOT = DEFAULT_TESTER_PROFILE_ROOT
    base.DEFAULT_TERMINAL_DATA_ROOT = DEFAULT_TERMINAL_DATA_ROOT
    base.PORTABLE_EA_SOURCE = DEFAULT_PORTABLE_ROOT / "MQL5" / "Experts" / base.mt5.EA_SOURCE_PATH
    base.PORTABLE_EA_EX5 = DEFAULT_PORTABLE_ROOT / "MQL5" / "Experts" / "Project_Obsidian_Prime_v2" / "foundation" / "mt5" / "ObsidianPrimeV2_RuntimeProbeEA.ex5"
    base.COMMON_ROOT = COMMON_ROOT


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stage336K fresh MT5 runtime probe attempt or exact blocker.")
    parser.add_argument("--terminal-path", default=str(DEFAULT_TERMINAL))
    parser.add_argument("--metaeditor-path", default=str(DEFAULT_METAEDITOR))
    parser.add_argument("--common-files-root", default=str(DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-data-root", default=str(DEFAULT_TERMINAL_DATA_ROOT))
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--wait-timeout-seconds", type=int, default=180)
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--attempt-filter", default="", help="Comma-separated attempt names for a narrow MT5 smoke run.")
    parser.add_argument("--end-utc", default="", help="Optional inclusive latest data probe end in ISO UTC.")
    return parser.parse_args()


def floor_m5(value: datetime) -> datetime:
    value = value.astimezone(UTC).replace(second=0, microsecond=0)
    return value - timedelta(minutes=value.minute % 5)


def parse_optional_utc(value: str) -> datetime:
    if not value:
        return floor_m5(datetime.now(tz=UTC))
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise ValueError(f"UTC timestamp must be timezone-aware: {value}")
    return floor_m5(parsed.astimezone(UTC))


def init_mt5(terminal_path: Path) -> None:
    try:
        ok = mt5_api.initialize(path=str(terminal_path), portable=True)
    except TypeError:
        ok = mt5_api.initialize(str(terminal_path))
    if not ok:
        raise RuntimeError(f"MetaTrader5 initialize failed: {mt5_api.last_error()}")


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


def probe_latest_raw_data(terminal_path: Path, end_utc: datetime) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    RAW_REFRESH_DIR.mkdir(parents=True, exist_ok=True)
    start_utc = datetime(2026, 4, 14, tzinfo=UTC)
    rows: list[dict[str, Any]] = []
    latest: dict[str, Any] = {
        "requested_start_utc": start_utc.isoformat().replace("+00:00", "Z"),
        "requested_end_utc": end_utc.isoformat().replace("+00:00", "Z"),
        "us100_rows": 0,
        "us100_last_open_unix": None,
        "tester_to_date": "2026.05.27",
    }
    init_mt5(terminal_path)
    try:
        terminal_info = mt5_api.terminal_info()
        account_info = mt5_api.account_info()
        for contract_symbol, broker_symbol in RAW_SYMBOLS:
            if not mt5_api.symbol_select(broker_symbol, True):
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
            csv_path = RAW_REFRESH_DIR / contract_symbol / f"bars_{broker_symbol.lower().replace('.', '_')}_m5_mt5api_raw.csv"
            manifest_path = csv_path.with_suffix(".manifest.json")
            export_rates_csv(csv_path, contract_symbol, broker_symbol, rates)
            manifest = {
                "manifest_version": "STAGE336K_RAW_REFRESH_PROBE_V1",
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
            if contract_symbol == "US100":
                latest["us100_rows"] = int(len(rates))
                latest["us100_last_open_unix"] = int(rates[-1]["time"])
                latest["us100_last_open_utc"] = last_open.isoformat().replace("+00:00", "Z")
                latest["us100_last_close_utc"] = last_close.isoformat().replace("+00:00", "Z")
                latest["tester_to_date"] = (last_open.date() + timedelta(days=1)).strftime("%Y.%m.%d")
                latest["terminal_path"] = getattr(terminal_info, "path", None)
                latest["terminal_data_path"] = getattr(terminal_info, "data_path", None)
                latest["account_login_present"] = getattr(account_info, "login", None)
    finally:
        mt5_api.shutdown()
    return rows, latest


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
        stopped.append(
            {
                "process_id": int(pid),
                "returncode": proc.returncode,
                "stdout": proc.stdout[-1000:],
                "stderr": proc.stderr[-1000:],
            }
        )
    after = base.detect_running_terminal_processes(terminal_path)
    return {
        "before_status": probe.get("status"),
        "before_matching_processes": probe.get("matching_processes", []),
        "stopped": stopped,
        "after_status": after.get("status"),
        "after_matching_processes": after.get("matching_processes", []),
        "effect": "target portable terminal is closed before MT5 tester config execution",
    }


def filter_attempts(attempts: list[dict[str, Any]], attempt_filter: str) -> list[dict[str, Any]]:
    if not attempt_filter.strip():
        return attempts
    keep = {item.strip() for item in attempt_filter.split(",") if item.strip()}
    return [attempt for attempt in attempts if str(attempt.get("attempt_name", "")) in keep]


def rewrite_attempt_to_latest(attempt: dict[str, Any], tester_to_date: str) -> dict[str, Any]:
    tester = dict(attempt["ini"]["tester"])
    tester["ToDate"] = tester_to_date
    tester["Report"] = f"Project_Obsidian_Prime_v2_{RUN_ID}_{attempt['attempt_name']}"
    ini_path = Path(str(attempt["ini"]["path"]))
    ini_payload = base.materialize_ini_file(tester, ini_path)
    attempt["ini"] = ini_payload
    attempt["to_date"] = tester_to_date
    attempt["common_telemetry_path"] = f"{COMMON_ROOT}/telemetry/{attempt['attempt_name']}_telemetry.csv"
    attempt["common_summary_path"] = f"{COMMON_ROOT}/telemetry/{attempt['attempt_name']}_summary.csv"
    return attempt


def feature_timestamp_bounds(path: Path) -> dict[str, Any]:
    frame = pd.read_csv(io_path(path), usecols=lambda column: column in {"bar_time_server", "timestamp_utc"})
    timestamp_column = "bar_time_server" if "bar_time_server" in frame.columns else "timestamp_utc"
    values = pd.to_datetime(frame[timestamp_column], errors="coerce", utc=True)
    valid = values.dropna()
    return {
        "feature_rows": int(len(frame)),
        "feature_first_timestamp": "" if valid.empty else valid.min().isoformat().replace("+00:00", "Z"),
        "feature_last_timestamp": "" if valid.empty else valid.max().isoformat().replace("+00:00", "Z"),
    }


def build_feature_freshness_rows(attempts: Sequence[Mapping[str, Any]], latest: Mapping[str, Any]) -> list[dict[str, Any]]:
    latest_close = pd.to_datetime(latest.get("us100_last_close_utc"), errors="coerce", utc=True)
    rows: list[dict[str, Any]] = []
    for attempt in attempts:
        feature_path = ROOT / str(attempt.get("feature_local_path", ""))
        bounds = feature_timestamp_bounds(feature_path)
        last_feature = pd.to_datetime(bounds["feature_last_timestamp"], errors="coerce", utc=True)
        gap_minutes = ""
        if pd.notna(latest_close) and pd.notna(last_feature):
            gap_minutes = max(0.0, (latest_close - last_feature).total_seconds() / 60.0)
        rows.append(
            {
                "attempt_name": attempt.get("attempt_name", ""),
                "artifact_slug": attempt.get("artifact_slug", ""),
                "feature_set_id": attempt.get("feature_set_id", ""),
                "feature_rows": bounds["feature_rows"],
                "feature_first_timestamp": bounds["feature_first_timestamp"],
                "feature_last_timestamp": bounds["feature_last_timestamp"],
                "latest_us100_last_close_utc": latest.get("us100_last_close_utc", ""),
                "feature_to_latest_gap_minutes": gap_minutes,
                "fresh_latest_handoff_status": "complete_to_latest" if gap_minutes == 0 else "feature_handoff_gap_to_latest",
                "effect": "latest broker bars exist, but frozen feature CSV must cover the same closed-bar timestamps before forward/runtime claims",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def branch_attempt_rows(attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    by_attempt = {str(attempt.get("attempt_name", "")): attempt for attempt in attempts}
    rows: list[dict[str, Any]] = []
    for branch_id, attempt_name in BRANCH_ATTEMPT_MAP:
        attempt = by_attempt.get(attempt_name)
        rows.append(
            {
                "branch_id": branch_id,
                "attempt_name": attempt_name,
                "artifact_slug": "" if attempt is None else attempt.get("artifact_slug", ""),
                "feature_set_id": "" if attempt is None else attempt.get("feature_set_id", ""),
                "model_id": "" if attempt is None else attempt.get("model_id", ""),
                "binding_status": "missing_attempt" if attempt is None else "bound_to_fresh_mt5_attempt",
                "branch_use": "diagnostic_runtime_probe_only",
                "selection_use": "blocked",
                "forward_decision_use": "blocked",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    rows.append(
        {
            "branch_id": "cross_branch_runtime_usability",
            "attempt_name": "all_bound_attempts",
            "artifact_slug": "cross_branch",
            "feature_set_id": "mixed",
            "model_id": "mixed",
            "binding_status": "summary_from_bound_attempts",
            "branch_use": "diagnostic_runtime_probe_only",
            "selection_use": "blocked",
            "forward_decision_use": "blocked",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )
    return rows


def branch_runtime_summary_rows(branch_rows: Sequence[Mapping[str, Any]], runtime_rows: Sequence[Mapping[str, Any]], freshness_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    runtime_by_attempt = {str(row.get("attempt_name", "")): row for row in runtime_rows}
    freshness_by_attempt = {str(row.get("attempt_name", "")): row for row in freshness_rows}
    output: list[dict[str, Any]] = []
    for row in branch_rows:
        attempt_name = str(row.get("attempt_name", ""))
        if attempt_name == "all_bound_attempts":
            continue
        runtime = runtime_by_attempt.get(attempt_name, {})
        freshness = freshness_by_attempt.get(attempt_name, {})
        output.append(
            {
                "branch_id": row.get("branch_id", ""),
                "attempt_name": attempt_name,
                "tester_status": runtime.get("tester_status", "not_attempted"),
                "runtime_status": runtime.get("runtime_status", "not_attempted"),
                "report_status": runtime.get("report_status", "missing"),
                "returncode": runtime.get("returncode", ""),
                "feature_ready_count": runtime.get("feature_ready_count", ""),
                "model_ok_count": runtime.get("model_ok_count", ""),
                "long_count": runtime.get("long_count", ""),
                "short_count": runtime.get("short_count", ""),
                "flat_count": runtime.get("flat_count", ""),
                "order_fill_count": runtime.get("order_fill_count", ""),
                "net_profit": runtime.get("net_profit", ""),
                "profit_factor": runtime.get("profit_factor", ""),
                "trade_count": runtime.get("trade_count", ""),
                "max_drawdown_amount": runtime.get("max_drawdown_amount", ""),
                "last_skip_reason": runtime.get("last_skip_reason", ""),
                "feature_last_timestamp": freshness.get("feature_last_timestamp", ""),
                "latest_us100_last_close_utc": freshness.get("latest_us100_last_close_utc", ""),
                "feature_to_latest_gap_minutes": freshness.get("feature_to_latest_gap_minutes", ""),
                "decision_use": "diagnostic_only_not_forward_pass_fail",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return output


def build_usability_decision(runtime_rows: Sequence[Mapping[str, Any]], freshness_rows: Sequence[Mapping[str, Any]], materialize_only: bool) -> list[dict[str, Any]]:
    completed = sum(1 for row in runtime_rows if row.get("tester_status") == "completed" and row.get("runtime_status") == "completed")
    total = len(runtime_rows)
    gaps = sum(1 for row in freshness_rows if row.get("fresh_latest_handoff_status") != "complete_to_latest")
    if materialize_only:
        label = "blocked_missing_fresh_mt5_execution"
        reason = "run336K materialized inputs only"
    elif completed == total and gaps == 0:
        label = "usable_diagnostic_only"
        reason = "fresh MT5 output completed and feature handoff covers latest broker bars, but still not forward pass/fail"
    elif completed:
        label = "usable_diagnostic_only_with_latest_feature_gap"
        reason = "fresh MT5 output completed, but feature CSV does not cover the latest US100 broker bars"
    else:
        label = "blocked_missing_fresh_mt5"
        reason = "fresh MT5 runtime output did not complete"
    return [
        {
            "decision_label": label,
            "fresh_runtime_completed": completed,
            "fresh_runtime_total": total,
            "feature_latest_gap_attempts": gaps,
            "forward_passed": "not_claimed",
            "forward_failed": "not_claimed",
            "runtime_authority": "not_claimed",
            "goal_achieve": "not_claimed",
            "reason": reason,
            "next_action": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_report(status: str, decision: str, latest_rows: Sequence[Mapping[str, Any]], runtime_rows: Sequence[Mapping[str, Any]], usability_rows: Sequence[Mapping[str, Any]]) -> Path:
    us100 = next((row for row in latest_rows if row.get("contract_symbol") == "US100"), {})
    completed = sum(1 for row in runtime_rows if row.get("tester_status") == "completed" and row.get("runtime_status") == "completed")
    text = f"""# run336K Fresh MT5 Runtime Probe(신규 MT5 런타임 탐침)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{status}`
- decision(결정): `{decision}`
- US100 latest close(US100 최신 종가 시각): `{us100.get('last_close_utc', '')}`
- US100 rows(US100 행): `{us100.get('rows', '')}`
- fresh MT5 completed(신규 MT5 완료): `{completed}/{len(runtime_rows)}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## What Was Tried(시도 내용)

MT5 API(메타트레이더5 API)로 2026-04-14 이후 최신 US100 M5 broker data(브로커 데이터)를 다시 확인하고, run330E/run335K frozen ONNX handoff(고정 온엑스 인계)를 run336K 전용 Common Files(공통 파일) 경로와 report/telemetry identity(보고서/기록 정체성)로 다시 실행했다.

Effect(효과): 데이터 부재와 런타임 부재를 분리했고, 모델/threshold/lot/risk/ATR(모델/임계값/랏/위험/ATR)은 바꾸지 않았다.

## Boundary(경계)

이 결과는 diagnostic runtime probe(진단 런타임 탐침)다. feature handoff(피처 인계)가 최신 broker bar(브로커 봉) 끝까지 완전히 이어지지 않으면 Forward Passed/Failed(전진 통과/실패)로 쓰지 않는다.
"""
    return write_md(REVIEWS_DIR / "run336K_fresh_mt5_runtime_probe_or_block.md", text)


def update_status_docs(status: str, decision: str, latest: Mapping[str, Any], usability_rows: Sequence[Mapping[str, Any]]) -> list[Path]:
    usability = usability_rows[0] if usability_rows else {}
    latest_close = csv_value(latest.get("us100_last_close_utc", "unknown"))
    fresh_completed = csv_value(usability.get("fresh_runtime_completed", "unknown"))
    fresh_total = csv_value(usability.get("fresh_runtime_total", "unknown"))
    feature_gap_attempts = csv_value(usability.get("feature_latest_gap_attempts", "unknown"))
    summary = (
        "- stage_status(단계 상태): `open_active`\n"
        "- selected_candidate(선택 후보): `none`\n"
        "- source_stage(원천 단계): `335_overfit_guard__failure_memory_constrained_research_handoff`\n"
        f"- current_run(현재 실행): `{NEXT_RUN_ID}`\n"
        f"- latest_materialization(최신 물질화): `{RUN_ID}`\n"
        f"- latest_decision(최신 결정): `{decision}`\n"
        f"- fresh MT5 runtime probe(신규 MT5 런타임 탐침): `{fresh_completed}/{fresh_total} completed(완료)`\n"
        f"- latest US100 close(최신 US100 종가): `{latest_close}`\n"
        f"- feature handoff gap(피처 인계 공백): `{feature_gap_attempts}/{fresh_total} attempts(시도)`\n"
        "- Forward Passed(전진 통과): `not_claimed`\n"
        "- Forward Failed(전진 실패): `not_claimed`\n"
        "- live_readiness(실거래 준비): `not_claimed`\n"
        "- deployment(배포): `not_claimed`\n"
        "- operating_promotion(운영 승격): `not_claimed`\n"
        "- runtime_authority(런타임 권위): `not_claimed`\n"
        "- goal_achieve(목표 달성): `not_claimed`\n"
        "- next_action(다음 행동): `run336L_review_fresh_mt5_runtime_probe_and_repair_or_rebuild_decision_v1`\n"
        "- effect(효과): run336K(336K 실행)는 최신 US100 M5 데이터와 fresh MT5 runtime probe(신규 MT5 런타임 탐침)를 실제로 확보했지만, frozen feature CSV(고정 피처 CSV)가 최신 broker bar(브로커 봉) 끝까지 이어지지 않아 forward pass/fail(전진 통과/실패)과 운영 주장은 계속 차단한다.\n"
    )
    write_md(SELECTED_STATUS, "# Stage336 Selection Status(336단계 선택 상태)\n\n" + summary)
    decision_text = f"""# Stage336K Decision(336K 결정)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{status}`
- decision(결정): `{decision}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
- next_action(다음 행동): `{NEXT_RUN_ID}`

Effect(효과): run336K(336K 실행)는 fresh MT5 runtime output(신규 MT5 런타임 출력)을 `{fresh_completed}/{fresh_total} completed(완료)`로 확보했고 US100 M5 broker data(브로커 데이터)는 `{latest_close}` close(종가)까지 확인했다. 다만 frozen feature CSV(고정 피처 CSV)가 최신 broker bar(브로커 봉) 끝까지 이어지지 않아 feature handoff gap(피처 인계 공백) `{feature_gap_attempts}/{fresh_total}`로 닫는다. 선택(candidate selection, 후보 선택), Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.
"""
    write_md(DECISION_DOC, decision_text)
    return [SELECTED_STATUS, DECISION_DOC]


def update_registers(status: str, judgment: str, decision: str, artifact_paths: Sequence[Path]) -> None:
    generated = now_utc()
    simple_upsert_csv(
        STAGE_LEDGER,
        [
            {
                "ledger_row_id": f"{RUN_ID}__fresh_mt5_runtime_probe",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "work_family": "runtime_parity",
                "evidence_scope": "fresh_mt5_runtime_probe_with_feature_handoff_gap",
                "kpi_scope": "runtime_diagnostic_no_forward_kpi_decision",
                "status": status,
                "judgment": judgment,
                "claim_boundary": CLAIM_BOUNDARY,
                "path": rel(REVIEWS_DIR / "run336K_fresh_mt5_runtime_probe_or_block.md"),
                "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
                "decision": decision,
            }
        ],
        key="ledger_row_id",
    )
    simple_upsert_csv(
        RUN_REGISTRY,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "runtime_parity",
                "status": status,
                "judgment": judgment,
                "path": rel(REVIEWS_DIR / "run336K_fresh_mt5_runtime_probe_or_block.md"),
                "notes": f"decision={decision};next_action={NEXT_RUN_ID};no_forward_pass_fail.",
            }
        ],
        key="run_id",
    )
    artifact_rows = []
    for path in artifact_paths:
        if not path_exists(path) or not io_path(path).is_file():
            continue
        suffix = path.suffix.lower()
        artifact_rows.append(
            {
                "artifact_id": f"{RUN_ID}::{rel(path)}",
                "artifact_type": suffix.lstrip(".") or "file",
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path) if suffix in {".csv", ".json", ".md", ".txt", ".ini", ".set", ".py"} else sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": generated,
                "notes": status,
            }
        )
    if artifact_rows:
        simple_upsert_csv(ARTIFACT_REGISTRY, artifact_rows, key="artifact_id")


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


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args()
    patch_base_module()
    generated_at_utc = now_utc()
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    MT5_DIR.mkdir(parents=True, exist_ok=True)

    end_utc = parse_optional_utc(args.end_utc)
    raw_rows, latest = probe_latest_raw_data(Path(args.terminal_path), end_utc)
    terminal_recovery = (
        {"status": "skipped_materialize_only"}
        if args.materialize_only
        else stop_target_terminal_if_running(Path(args.terminal_path))
    )
    raw_summary_path = write_csv(
        RUN_DIR / "fresh_forward_data_probe_summary.csv",
        [
            "contract_symbol",
            "broker_symbol",
            "status",
            "rows",
            "first_open_utc",
            "last_open_utc",
            "last_close_utc",
            "csv_path",
            "manifest_path",
            "last_error",
        ],
        raw_rows,
    )

    source_attempts = base.load_source_attempts()
    attempts, handoff_rows, materialized_artifacts = base.build_attempts(source_attempts, Path(args.common_files_root))
    attempts = filter_attempts(attempts, args.attempt_filter)
    attempts = [rewrite_attempt_to_latest(dict(attempt), str(latest["tester_to_date"])) for attempt in attempts]
    proxy_rows = base.build_proxy_signal_expected_rows(attempts)
    freshness_rows = build_feature_freshness_rows(attempts, latest)

    if args.materialize_only:
        execution_result = {
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
    signal_diff_rows = base.build_signal_difference_rows(proxy_rows, runtime_rows)
    numeric_rows = base.build_numeric_proxy_vs_fresh_mt5_rows(runtime_rows)
    branch_rows = branch_attempt_rows(attempts)
    branch_runtime_rows = branch_runtime_summary_rows(branch_rows, runtime_rows, freshness_rows)
    usability_rows = build_usability_decision(runtime_rows, freshness_rows, bool(args.materialize_only))
    status = STATUS_MATERIALIZED_ONLY if args.materialize_only else (STATUS_COMPLETED if usability_rows[0]["decision_label"] == "usable_diagnostic_only" else STATUS_PARTIAL)
    judgment = JUDGMENT_COMPLETED if status == STATUS_COMPLETED else JUDGMENT_PARTIAL
    decision = DECISION_COMPLETED if status == STATUS_COMPLETED else DECISION_PARTIAL

    artifact_paths: list[Path] = [
        raw_summary_path,
        write_json(RUN_DIR / "fresh_forward_data_probe_latest.json", latest),
        write_json(RUN_DIR / "terminal_process_recovery.json", terminal_recovery),
        write_json(RUN_DIR / "independent_handoff_attempts.json", attempts),
        write_csv(
            RUN_DIR / "branch_attempt_binding.csv",
            [
                "branch_id",
                "attempt_name",
                "artifact_slug",
                "feature_set_id",
                "model_id",
                "binding_status",
                "branch_use",
                "selection_use",
                "forward_decision_use",
                "claim_boundary",
            ],
            branch_rows,
        ),
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
            RUN_DIR / "feature_freshness_gap_audit.csv",
            [
                "attempt_name",
                "artifact_slug",
                "feature_set_id",
                "feature_rows",
                "feature_first_timestamp",
                "feature_last_timestamp",
                "latest_us100_last_close_utc",
                "feature_to_latest_gap_minutes",
                "fresh_latest_handoff_status",
                "effect",
                "claim_boundary",
            ],
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
            [
                "attempt_name",
                "artifact_slug",
                "dimension",
                "proxy_expected_value",
                "mt5_runtime_value",
                "difference_proxy_minus_mt5",
                "difference_status",
                "proxy_source",
                "mt5_source",
                "usable_for_runtime_signal_parity",
                "usable_for_forward_pass_fail",
                "runtime_skip_reason",
                "claim_boundary",
            ],
            signal_diff_rows,
        ),
        write_csv(
            RUN_DIR / "proxy_numeric_vs_fresh_mt5_difference.csv",
            [
                "protocol_id",
                "branch_id",
                "branch_name",
                "dimension",
                "proxy_expected_value",
                "fresh_mt5_runtime_value",
                "difference_proxy_minus_fresh_mt5",
                "difference_status",
                "proxy_source",
                "mt5_source",
                "independence_improvement",
                "usable_for_diagnostic_consistency",
                "usable_for_forward_pass_fail",
                "reason",
                "claim_boundary",
            ],
            numeric_rows,
        ),
        write_csv(
            RUN_DIR / "branch_fresh_mt5_runtime_summary.csv",
            [
                "branch_id",
                "attempt_name",
                "tester_status",
                "runtime_status",
                "report_status",
                "returncode",
                "feature_ready_count",
                "model_ok_count",
                "long_count",
                "short_count",
                "flat_count",
                "order_fill_count",
                "net_profit",
                "profit_factor",
                "trade_count",
                "max_drawdown_amount",
                "last_skip_reason",
                "feature_last_timestamp",
                "latest_us100_last_close_utc",
                "feature_to_latest_gap_minutes",
                "decision_use",
                "claim_boundary",
            ],
            branch_runtime_rows,
        ),
        write_csv(
            RUN_DIR / "usability_decision.csv",
            [
                "decision_label",
                "fresh_runtime_completed",
                "fresh_runtime_total",
                "feature_latest_gap_attempts",
                "forward_passed",
                "forward_failed",
                "runtime_authority",
                "goal_achieve",
                "reason",
                "next_action",
                "claim_boundary",
            ],
            usability_rows,
        ),
        write_json(
            RUN_DIR / "tester_settings_identity.json",
            {
                "run_id": RUN_ID,
                "tester_to_date": latest.get("tester_to_date"),
                "terminal_path": str(args.terminal_path),
                "terminal_data_root": str(args.terminal_data_root),
                "common_files_root": str(args.common_files_root),
                "model_training": "forbidden_not_performed",
                "threshold_retuning": "forbidden_not_performed",
                "lot_optimization": "forbidden_not_performed",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
    ]
    artifact_paths.extend(base.copy_runtime_outputs(Path(args.common_files_root), attempts))
    artifact_paths.extend(copy_reports_to_required_names(runtime_rows))
    report_path = write_report(status, decision, raw_rows, runtime_rows, usability_rows)
    artifact_paths.append(report_path)
    artifact_paths.extend(update_status_docs(status, decision, latest, usability_rows))
    final_decision = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": status,
        "judgment": judgment,
        "decision": decision,
        "fresh_runtime_completed": usability_rows[0]["fresh_runtime_completed"],
        "fresh_runtime_total": usability_rows[0]["fresh_runtime_total"],
        "feature_latest_gap_attempts": usability_rows[0]["feature_latest_gap_attempts"],
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    artifact_paths.append(write_json(RUN_DIR / "final_fresh_mt5_runtime_probe_decision.json", final_decision))
    manifest_path = write_json(
        RUN_DIR / "run_manifest.json",
        {
            **final_decision,
            "generated_at_utc": generated_at_utc,
            "command": "python stage_pipelines/stage336/attempt_fresh_mt5_runtime_probe_or_block.py",
            "materialize_only": bool(args.materialize_only),
            "attempt_filter": args.attempt_filter,
            "artifacts": [rel(path) for path in artifact_paths if path_exists(path)],
        },
    )
    artifact_paths.append(manifest_path)
    update_registers(status, judgment, decision, [*artifact_paths, Path(__file__)])
    print(json.dumps(final_decision, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
