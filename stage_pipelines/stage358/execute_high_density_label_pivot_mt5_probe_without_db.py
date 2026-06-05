from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import shutil
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.mt5 import runtime_support as mt5  # noqa: E402


TODAY = "2026-06-02"
STAGE_ID = "358_runtime_probe_handoff__high_density_label_pivot_mt5_check"
RUN_NUMBER = "run358C"
RUN_ID = "run358C_execute_high_density_label_pivot_mt5_probe_without_db_v1"
PARENT_RUN_ID = "run358B_package_high_density_label_pivot_mt5_probe_without_db_v1"
NEXT_REVIEW_RUN_ID = "run358D_review_high_density_label_pivot_mt5_probe_without_db_v1"
NEXT_REPAIR_RUN_ID = "run358D_repair_high_density_label_pivot_mt5_probe_execution_without_db_v1"
EXPLORATION_LABEL = "stage358_runtime_probe_handoff__high_density_label_pivot_mt5_execution"
CLAIM_BOUNDARY = (
    "runtime_probe_only_proxy_mt5_diff_recorded_no_candidate_selection_no_forward_pass_"
    "no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)
TRADE_DENSITY_REQUIREMENT = "trade_per_day_min_3_to_10_plus_no_trade_splitting"
PARITY_TOLERANCE = 1.0e-4

STATUS_COMPLETED = "completed_stage358C_high_density_label_pivot_mt5_probe_executed_review_required_no_selection"
STATUS_BLOCKED = "blocked_stage358C_high_density_label_pivot_mt5_probe_attempt_recorded_repair_required_no_selection"
JUDGMENT_POSITIVE = "runtime_probe_positive_but_review_required_no_selection"
JUDGMENT_WEAK = "runtime_probe_completed_weak_or_negative_review_required_no_selection"
JUDGMENT_BLOCKED = "blocked_runtime_probe_outputs_missing_or_terminal_failed_no_selection"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MT5_DIR = RUN_DIR / "mt5"
SET_DIR = MT5_DIR / "sets"
INI_DIR = MT5_DIR / "inis"
REPORT_COPY_DIR = MT5_DIR / "reports"
TELEMETRY_COPY_DIR = RUN_DIR / "runtime_telemetry"
REVIEW_DIR = STAGE_DIR / "03_reviews"

SOURCE_RUN_DIR = STAGE_DIR / "02_runs" / "run358B"
SOURCE_ATTEMPT_PACKAGE = SOURCE_RUN_DIR / "runtime_probe_attempt_package.csv"
SOURCE_EXPECTED_TAPE = SOURCE_RUN_DIR / "expected" / "proxy_expected_tape.csv"
SOURCE_EXPECTED_INDEX = SOURCE_RUN_DIR / "expected" / "proxy_expected_tape_index.csv"
SOURCE_MAPPING_AUDIT = SOURCE_RUN_DIR / "runtime_mapping_audit.csv"
SOURCE_COMMON_SYNC = SOURCE_RUN_DIR / "common_files_sync.csv"
SOURCE_FINAL_DECISION = SOURCE_RUN_DIR / "final_decision.json"
SOURCE_GATE_AUDIT = SOURCE_RUN_DIR / "required_gate_coverage_audit.csv"

ATTEMPT_PACKAGE = RUN_DIR / "runtime_probe_attempt_package.csv"
SET_RETARGET_MANIFEST = RUN_DIR / "set_retarget_manifest.csv"
INI_RETARGET_MANIFEST = RUN_DIR / "ini_retarget_manifest.csv"
TERMINAL_PROCESS_AUDIT = RUN_DIR / "terminal_process_audit.json"
MT5_EXECUTION_RESULT = RUN_DIR / "mt5_execution_result.json"
STRATEGY_TESTER_REPORTS = RUN_DIR / "strategy_tester_report_records.json"
RUNTIME_OUTPUT_COPY = RUN_DIR / "runtime_output_copy_manifest.csv"
EXECUTION_SUMMARY = RUN_DIR / "high_density_label_pivot_mt5_probe_summary.csv"
PROXY_MT5_DIFF = RUN_DIR / "proxy_mt5_runtime_difference.csv"
TELEMETRY_SKIP_SUMMARY = RUN_DIR / "runtime_skip_reason_summary.csv"
RUNTIME_IDENTITY = RUN_DIR / "runtime_identity.csv"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
BACKTEST_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
SELF_CORRECTION_PLAN = RUN_DIR / "self_correction_plan.json"

REPORT_PATH = REVIEW_DIR / "run358C_high_density_label_pivot_mt5_probe.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-06-02_stage358C_high_density_label_pivot_mt5_probe.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_README = STAGE_DIR / "README.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"

DEFAULT_PORTABLE_ROOT = Path("C:/Users/awdse/AppData/Local/ObsidianPrime/mt5_portable_run329E")
DEFAULT_TERMINAL = DEFAULT_PORTABLE_ROOT / "terminal64.exe"
DEFAULT_COMMON_FILES = DEFAULT_PORTABLE_ROOT / "Common" / "Files"
DEFAULT_TESTER_PROFILE_ROOT = DEFAULT_PORTABLE_ROOT / "MQL5" / "Profiles" / "Tester"
COMMON_ROOT = "Project_Obsidian_Prime_v2/stage358/run358C_high_density_label_pivot_mt5_probe"
COMMON_TELEMETRY_DIR = f"{COMMON_ROOT}/telemetry"


def io(path: Path) -> Path:
    return mt5._io_path(path)


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def exists(path: Path) -> bool:
    return io(path).exists()


def require(path: Path) -> Path:
    if not exists(path):
        raise FileNotFoundError(path.as_posix())
    return path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with io(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> None:
    io(path.parent).mkdir(parents=True, exist_ok=True)
    io(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_bom_text(path: Path, text: str) -> None:
    io(path.parent).mkdir(parents=True, exist_ok=True)
    io(path).write_text(text, encoding="utf-8-sig", newline="\n")


def read_text(path: Path) -> str:
    return io(path).read_text(encoding="utf-8-sig")


def read_json(path: Path) -> Any:
    return json.loads(read_text(path))


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with io(path).open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Iterable[str] | None = None) -> None:
    rows = [dict(row) for row in rows]
    if fieldnames is None:
        columns: list[str] = []
        for row in rows:
            for key in row:
                if key not in columns:
                    columns.append(key)
        fieldnames = columns
    fieldnames = list(fieldnames)
    io(path.parent).mkdir(parents=True, exist_ok=True)
    with io(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def append_or_replace_csv(path: Path, new_rows: list[dict[str, Any]], key_fields: list[str]) -> None:
    old_fields, old_rows = read_csv_rows(path) if exists(path) else ([], [])
    fieldnames = list(old_fields)
    if not fieldnames:
        for row in new_rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    new_keys = {tuple(str(row.get(key, "")) for key in key_fields) for row in new_rows}
    kept = [
        row
        for row in old_rows
        if tuple(str(row.get(key, "")) for key in key_fields) not in new_keys
    ]
    write_csv(path, kept + new_rows, fieldnames)


def read_frame(path: Path) -> pd.DataFrame:
    return pd.read_csv(io(path), encoding="utf-8-sig", low_memory=False).fillna("")


def parse_set(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in read_text(path).splitlines():
        text = line.strip()
        if not text or text.startswith(";") or "=" not in text:
            continue
        key, value = text.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): json_ready(val) for key, val in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return float(value)
    if isinstance(value, (np.bool_,)):
        return bool(value)
    if isinstance(value, Path):
        return value.as_posix()
    if pd.isna(value) if not isinstance(value, (str, bytes, Mapping, list, tuple)) else False:
        return ""
    return value


def to_float(value: Any, default: float = 0.0) -> float:
    try:
        output = float(value)
    except (TypeError, ValueError):
        return default
    return output if math.isfinite(output) else default


def to_int(value: Any, default: int = 0) -> int:
    return int(round(to_float(value, float(default))))


def norm_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def norm_bar_time(value: Any) -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    try:
        return pd.Timestamp(text).strftime("%Y.%m.%d %H:%M:%S")
    except Exception:
        return text.replace("-", ".").replace("T", " ").replace("Z", "")[:19]


def parse_mt5_date(value: Any) -> datetime:
    return datetime.strptime(str(value), "%Y.%m.%d")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stage358C MT5 runtime probe for high-density label pivot package.")
    parser.add_argument("--terminal-path", default=str(DEFAULT_TERMINAL))
    parser.add_argument("--common-files-root", default=str(DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-data-root", default=str(DEFAULT_PORTABLE_ROOT))
    parser.add_argument("--timeout-seconds", type=int, default=1200)
    parser.add_argument("--wait-timeout-seconds", type=int, default=300)
    parser.add_argument("--attempt", action="append", default=None)
    parser.add_argument("--max-attempts", type=int, default=4)
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--reuse-existing-outputs", action="store_true")
    return parser.parse_args()


def terminal_processes() -> dict[str, Any]:
    command = [
        "powershell",
        "-NoProfile",
        "-Command",
        "Get-Process terminal64 -ErrorAction SilentlyContinue | "
        "Select-Object Id,ProcessName,Path,StartTime | ConvertTo-Json -Compress",
    ]
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    stdout = result.stdout.strip()
    if not stdout:
        return {"status": "no_terminal64_process", "processes": [], "returncode": result.returncode}
    try:
        parsed = json.loads(stdout)
        processes = parsed if isinstance(parsed, list) else [parsed]
    except json.JSONDecodeError:
        processes = [{"raw": stdout}]
    return {
        "status": "terminal64_process_present",
        "processes": processes,
        "returncode": result.returncode,
        "stderr": result.stderr[-1000:],
    }


def selected_source_attempts(args: argparse.Namespace) -> list[dict[str, str]]:
    _fields, rows = read_csv_rows(require(SOURCE_ATTEMPT_PACKAGE))
    if args.attempt:
        wanted = set(args.attempt)
        rows = [
            row
            for row in rows
            if row.get("attempt_name") in wanted
            or row.get("model_id") in wanted
            or row.get("queue_rank") in wanted
        ]
        if not rows:
            raise RuntimeError(f"no Stage358B attempts selected: {sorted(wanted)}")
    rows = sorted(rows, key=lambda row: (to_int(row.get("queue_rank")), str(row.get("probe_split"))))
    if args.max_attempts and args.max_attempts > 0:
        rows = rows[: args.max_attempts]
    return rows


def materialize_attempts(args: argparse.Namespace) -> list[dict[str, Any]]:
    source_rows = selected_source_attempts(args)
    attempts: list[dict[str, Any]] = []
    set_rows: list[dict[str, Any]] = []
    ini_rows: list[dict[str, Any]] = []
    for source in source_rows:
        attempt_name = str(source["attempt_name"])
        source_set_path = ROOT / str(source["set_path"])
        source_ini_path = ROOT / str(source["ini_path"])
        set_values = parse_set(require(source_set_path))
        common_telemetry = f"{COMMON_TELEMETRY_DIR}/{attempt_name}_telemetry.csv"
        common_summary = f"{COMMON_TELEMETRY_DIR}/{attempt_name}_summary.csv"
        set_values["InpRunId"] = f"{RUN_ID}_{attempt_name}"
        set_values["InpExplorationLabel"] = EXPLORATION_LABEL
        set_values["InpTelemetryCsvPath"] = common_telemetry
        set_values["InpSummaryCsvPath"] = common_summary
        set_values["InpTelemetryUseCommonFiles"] = "true"
        report_name = f"POPv2_{RUN_NUMBER}_{attempt_name}"
        set_name = f"OPV2_{RUN_NUMBER}_{attempt_name}.set"
        ini_name = f"OPV2_{RUN_NUMBER}_{attempt_name}.ini"
        set_path = SET_DIR / set_name
        ini_path = INI_DIR / ini_name
        set_payload = mt5.materialize_tester_set_file(set_values, set_path, generated_by=rel(Path(__file__)))
        ini_payload = mt5.materialize_tester_ini_file(
            mt5.TesterMaterializationConfig(
                shutdown_terminal=1,
                from_date=str(source["from_date"]),
                to_date=str(source["to_date"]),
                report=report_name,
            ),
            ini_path,
            set_file_path=Path(set_name),
        )
        attempt = {
            **source,
            "run_id": RUN_ID,
            "source_run_id": PARENT_RUN_ID,
            "split": source["probe_split"],
            "source_set_path": rel(source_set_path),
            "source_ini_path": rel(source_ini_path),
            "set_name": set_name,
            "ini_name": ini_name,
            "set_path": rel(set_path),
            "ini_path": rel(ini_path),
            "set_sha256": set_payload["sha256"],
            "ini_sha256": ini_payload["sha256"],
            "common_telemetry_path": common_telemetry,
            "common_summary_path": common_summary,
            "report_name": report_name,
            "ini": {"tester": {"Report": report_name}},
            "claim_boundary": CLAIM_BOUNDARY,
        }
        attempts.append(attempt)
        set_rows.append(
            {
                "attempt_name": attempt_name,
                "source_set_path": rel(source_set_path),
                "stage358c_set_path": rel(set_path),
                "set_sha256": set_payload["sha256"],
                "telemetry_path": common_telemetry,
                "effect": "retargeted_set_separates_stage358c_runtime_outputs",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        ini_rows.append(
            {
                "attempt_name": attempt_name,
                "source_ini_path": rel(source_ini_path),
                "stage358c_ini_path": rel(ini_path),
                "ini_sha256": ini_payload["sha256"],
                "report_name": report_name,
                "from_date": source["from_date"],
                "to_date": source["to_date"],
                "effect": "retargeted_ini_separates_stage358c_strategy_report",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(ATTEMPT_PACKAGE, attempts)
    write_csv(SET_RETARGET_MANIFEST, set_rows)
    write_csv(INI_RETARGET_MANIFEST, ini_rows)
    return attempts


def remove_runtime_outputs(common_files_root: Path, attempt: Mapping[str, Any]) -> None:
    for key in ("common_telemetry_path", "common_summary_path"):
        path = common_files_root / Path(str(attempt[key]))
        if exists(path):
            io(path).unlink()


def copy_runtime_outputs(common_files_root: Path, attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for attempt in attempts:
        attempt_name = str(attempt["attempt_name"])
        for key, suffix in (("common_telemetry_path", "telemetry"), ("common_summary_path", "summary")):
            source = common_files_root / Path(str(attempt[key]))
            target = TELEMETRY_COPY_DIR / f"{attempt_name}_{suffix}.csv"
            copied = False
            if exists(source):
                io(target.parent).mkdir(parents=True, exist_ok=True)
                shutil.copy2(io(source), io(target))
                copied = True
            rows.append(
                {
                    "copy_id": f"{attempt_name}::{suffix}",
                    "attempt_name": attempt_name,
                    "source_path": source.as_posix(),
                    "target_path": rel(target),
                    "exists": copied and exists(target),
                    "sha256": sha256_file(target) if copied and exists(target) else "",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    write_csv(RUNTIME_OUTPUT_COPY, rows)
    return rows


def execute_attempts(
    args: argparse.Namespace,
    attempts: Sequence[Mapping[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    common_files_root = Path(args.common_files_root)
    tester_profile_root = Path(args.tester_profile_root)
    terminal_data_root = Path(args.terminal_data_root)
    terminal_probe = terminal_processes()
    write_json(TERMINAL_PROCESS_AUDIT, terminal_probe)
    execution_results: list[dict[str, Any]] = []
    if args.materialize_only:
        for attempt in attempts:
            execution_results.append(
                {
                    "attempt_name": attempt["attempt_name"],
                    "status": "not_run_materialize_only",
                    "runtime_outputs": {"status": "not_run_materialize_only"},
                    "ini_path": attempt["ini_path"],
                    "set_path": attempt["set_path"],
                }
            )
    elif args.reuse_existing_outputs:
        for attempt in attempts:
            runtime_outputs = mt5.validate_mt5_runtime_outputs(common_files_root, attempt)
            execution_results.append(
                {
                    "attempt_name": attempt["attempt_name"],
                    "status": "completed" if runtime_outputs.get("status") == "completed" else "blocked",
                    "runtime_outputs": runtime_outputs,
                    "ini_path": attempt["ini_path"],
                    "set_path": attempt["set_path"],
                }
            )
    elif terminal_probe.get("status") != "no_terminal64_process":
        for attempt in attempts:
            execution_results.append(
                {
                    "attempt_name": attempt["attempt_name"],
                    "status": "blocked",
                    "blocker": "target_portable_terminal_already_running",
                    "runtime_outputs": {"status": "blocked", "wait_status": "skipped_terminal_already_running"},
                    "ini_path": attempt["ini_path"],
                    "set_path": attempt["set_path"],
                }
            )
    else:
        for attempt in attempts:
            remove_runtime_outputs(common_files_root, attempt)
            mt5.remove_existing_mt5_report_artifacts(terminal_data_root, attempt, run_id=RUN_ID)
            try:
                tester_result = mt5.run_mt5_tester(
                    Path(args.terminal_path),
                    ROOT / str(attempt["ini_path"]),
                    set_path=ROOT / str(attempt["set_path"]),
                    tester_profile_set_path=tester_profile_root / str(attempt["set_name"]),
                    tester_profile_ini_path=tester_profile_root / str(attempt["ini_name"]),
                    timeout_seconds=args.timeout_seconds,
                    terminal_extra_args=["/portable"],
                )
            except subprocess.TimeoutExpired as exc:
                tester_result = {
                    "status": "blocked",
                    "command": exc.cmd,
                    "returncode": None,
                    "stdout": (exc.stdout or "")[-2000:] if isinstance(exc.stdout, str) else "",
                    "stderr": (exc.stderr or "")[-2000:] if isinstance(exc.stderr, str) else "",
                    "blocker": "terminal_timeout",
                }
            runtime_outputs = mt5.wait_for_mt5_runtime_outputs(
                common_files_root,
                attempt,
                timeout_seconds=args.wait_timeout_seconds,
                poll_seconds=2.0,
            )
            if runtime_outputs.get("status") != "completed":
                tester_result["status"] = "blocked"
                tester_result.setdefault("blocker", "runtime_outputs_missing_or_init_failed")
            execution_log = MT5_DIR / f"{attempt['attempt_name']}_tester_execution.json"
            write_json(execution_log, {"tester_result": tester_result, "runtime_outputs": runtime_outputs})
            execution_results.append(
                {
                    **tester_result,
                    "attempt_name": attempt["attempt_name"],
                    "runtime_outputs": runtime_outputs,
                    "ini_path": attempt["ini_path"],
                    "set_path": attempt["set_path"],
                }
            )
    report_records = mt5.collect_mt5_strategy_report_artifacts(
        terminal_data_root=Path(args.terminal_data_root),
        run_output_root=RUN_DIR,
        attempts=attempts,
        run_id=RUN_ID,
    )
    mt5.attach_mt5_report_metrics(execution_results, report_records)
    copy_rows = copy_runtime_outputs(common_files_root, attempts)
    write_json(MT5_EXECUTION_RESULT, execution_results)
    write_json(STRATEGY_TESTER_REPORTS, report_records)
    return execution_results, report_records, copy_rows


def expected_lookup(expected: pd.DataFrame, attempt: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    subset = expected[
        expected["queue_rank"].astype(str).eq(str(attempt["queue_rank"]))
        & expected["split"].astype(str).eq(str(attempt["probe_split"]))
    ].copy()
    return {norm_bar_time(row["bar_time_server"]): row.to_dict() for _, row in subset.iterrows()}


def metric_number(metrics: Mapping[str, Any], name: str) -> float:
    return to_float(metrics.get(name), math.nan)


def trade_density_status(value: float | None) -> str:
    if value is None or not math.isfinite(value):
        return "not_available"
    if value >= 10.0:
        return "meets_10_plus_target"
    if value >= 3.0:
        return "meets_min_3_to_10_band"
    return "below_min_3_per_day"


def report_metric_summary(metrics: Mapping[str, Any], feature_day_count: int, calendar_days: int) -> dict[str, Any]:
    trade_count = metric_number(metrics, "trade_count")
    feature_density = trade_count / feature_day_count if math.isfinite(trade_count) and feature_day_count else math.nan
    calendar_density = trade_count / calendar_days if math.isfinite(trade_count) and calendar_days else math.nan
    return {
        "net_profit": metrics.get("net_profit", ""),
        "profit_factor": metrics.get("profit_factor", ""),
        "expectancy": metrics.get("expectancy", ""),
        "recovery_factor": metrics.get("recovery_factor", ""),
        "max_drawdown_amount": metrics.get("max_drawdown_amount", ""),
        "max_drawdown_percent": metrics.get("max_drawdown_percent", ""),
        "trade_count": metrics.get("trade_count", ""),
        "long_trade_count": metrics.get("long_trade_count", ""),
        "short_trade_count": metrics.get("short_trade_count", ""),
        "win_rate_percent": metrics.get("win_rate_percent", ""),
        "feature_day_count": feature_day_count,
        "calendar_days": calendar_days,
        "trade_density_per_feature_day": feature_density if math.isfinite(feature_density) else "",
        "trade_density_per_calendar_day": calendar_density if math.isfinite(calendar_density) else "",
        "trade_density_requirement_status": trade_density_status(feature_density if math.isfinite(feature_density) else None),
    }


def no_trade_splitting_status(attempt: Mapping[str, Any]) -> str:
    max_positions = to_int(attempt.get("max_concurrent_positions"), 0)
    fixed_lot = to_float(attempt.get("fixed_lot"), 0.0)
    if max_positions == 1 and fixed_lot > 0.0:
        return "guardrail_supported_by_fixed_lot_and_single_position"
    return "not_supported_by_set_file"


def compare_attempt(
    attempt: Mapping[str, Any],
    execution: Mapping[str, Any],
    report: Mapping[str, Any],
    expected: pd.DataFrame,
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    attempt_name = str(attempt["attempt_name"])
    expected_by_time = expected_lookup(expected, attempt)
    expected_raw_signal_rows = sum(
        1 for row in expected_by_time.values() if str(row.get("proxy_raw_label", "")).lower() != "flat"
    )
    expected_selected_trade_rows = sum(1 for row in expected_by_time.values() if norm_bool(row.get("proxy_selected_trade")))
    feature_day_count = len({key[:10] for key in expected_by_time if key})
    calendar_days = 0
    try:
        calendar_days = max(1, (parse_mt5_date(attempt["to_date"]) - parse_mt5_date(attempt["from_date"])).days)
    except Exception:
        pass
    local_telemetry = TELEMETRY_COPY_DIR / f"{attempt_name}_telemetry.csv"
    local_summary = TELEMETRY_COPY_DIR / f"{attempt_name}_summary.csv"
    metrics = report.get("metrics", {}) if isinstance(report.get("metrics"), Mapping) else {}
    diff_rows: list[dict[str, Any]] = []
    skip_rows: list[dict[str, Any]] = []
    if not exists(local_telemetry):
        return (
            {
                "attempt_name": attempt_name,
                "queue_rank": attempt.get("queue_rank", ""),
                "model_id": attempt.get("model_id", ""),
                "probe_split": attempt.get("probe_split", ""),
                "tester_status": execution.get("status", "not_attempted"),
                "runtime_status": execution.get("runtime_outputs", {}).get("status", "missing"),
                "report_status": report.get("status", "missing") if report else "missing",
                "blocker": execution.get("blocker", "runtime_telemetry_missing"),
                "expected_rows": len(expected_by_time),
                "expected_raw_signal_rows": expected_raw_signal_rows,
                "expected_selected_trade_rows": expected_selected_trade_rows,
                "telemetry_cycle_rows": 0,
                "ready_model_rows": 0,
                "matched_rows": 0,
                "probability_match_rows": 0,
                "decision_match_rows": 0,
                "expected_missing_rows": 0,
                "max_abs_probability_diff": "",
                "comparison_status": "blocked_no_runtime_telemetry",
                **report_metric_summary(metrics, feature_day_count, calendar_days),
                "claim_boundary": CLAIM_BOUNDARY,
            },
            diff_rows,
            skip_rows,
        )

    telemetry = pd.read_csv(io(local_telemetry), encoding="utf-8-sig", low_memory=False).fillna("")
    cycles = telemetry[telemetry["record_type"].astype(str).str.lower().eq("cycle")].copy()
    ready = cycles[
        cycles["feature_ready"].astype(str).str.lower().eq("true")
        & cycles["model_ok"].astype(str).str.lower().eq("true")
    ].copy()
    skipped = cycles.loc[~cycles.index.isin(ready.index)].copy()
    if "skip_reason" in skipped.columns:
        for reason, count in skipped["skip_reason"].astype(str).replace("", "empty").value_counts().sort_index().items():
            skip_rows.append(
                {
                    "attempt_name": attempt_name,
                    "skip_reason": reason,
                    "rows": int(count),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )

    matched = 0
    probability_match = 0
    decision_match = 0
    expected_missing = 0
    max_abs = 0.0
    ready_times: list[str] = []
    for _, row in ready.iterrows():
        source_time = norm_bar_time(row.get("source_time") or row.get("bar_time"))
        ready_times.append(source_time)
        exp = expected_by_time.get(source_time)
        if exp is None:
            expected_missing += 1
            diff_rows.append(
                {
                    "attempt_name": attempt_name,
                    "source_time": source_time,
                    "expected_found": False,
                    "comparison_status": "expected_missing",
                    "attribution": "runtime_timestamp_not_in_expected_tape",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            continue
        mt5_probs = np.asarray([to_float(row.get("p_short")), to_float(row.get("p_flat")), to_float(row.get("p_long"))], dtype=float)
        exp_probs = np.asarray([to_float(exp.get("p_short")), to_float(exp.get("p_flat")), to_float(exp.get("p_long"))], dtype=float)
        diffs = np.abs(mt5_probs - exp_probs)
        row_max = float(np.max(diffs))
        max_abs = max(max_abs, row_max)
        prob_ok = row_max <= PARITY_TOLERANCE
        dec_ok = str(row.get("decision", "")).strip().lower() == str(exp.get("proxy_raw_label", "")).strip().lower()
        probability_match += int(prob_ok)
        decision_match += int(dec_ok)
        matched += int(prob_ok and dec_ok)
        if not prob_ok:
            attribution = "onnx_runtime_probability_mismatch"
        elif not dec_ok:
            attribution = "decision_surface_mismatch"
        else:
            attribution = "matched"
        diff_rows.append(
            {
                "attempt_name": attempt_name,
                "queue_rank": attempt.get("queue_rank", ""),
                "source_time": source_time,
                "expected_found": True,
                "probability_match": prob_ok,
                "decision_match": dec_ok,
                "mt5_p_short": float(mt5_probs[0]),
                "expected_p_short": float(exp_probs[0]),
                "abs_diff_p_short": float(diffs[0]),
                "mt5_p_flat": float(mt5_probs[1]),
                "expected_p_flat": float(exp_probs[1]),
                "abs_diff_p_flat": float(diffs[1]),
                "mt5_p_long": float(mt5_probs[2]),
                "expected_p_long": float(exp_probs[2]),
                "abs_diff_p_long": float(diffs[2]),
                "row_max_abs_diff": row_max,
                "mt5_decision": row.get("decision", ""),
                "expected_decision": exp.get("proxy_raw_label", ""),
                "proxy_selected_trade": exp.get("proxy_selected_trade", ""),
                "comparison_status": "matched" if attribution == "matched" else "mismatch",
                "attribution": attribution,
                "usability": "usable_for_runtime_parity_diff_not_mt5_kpi_substitute",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    runtime = execution.get("runtime_outputs", {}) if isinstance(execution.get("runtime_outputs"), Mapping) else {}
    last_summary = runtime.get("last_summary", {}) if isinstance(runtime.get("last_summary"), Mapping) else {}
    latest_expected = max(expected_by_time) if expected_by_time else ""
    feature_last_reached = latest_expected in set(ready_times)
    if len(ready) <= 0:
        comparison_status = "blocked_no_ready_model_rows"
    elif expected_missing:
        comparison_status = "completed_with_timestamp_gap"
    elif probability_match == len(ready) and decision_match == len(ready):
        comparison_status = "completed_probability_decision_parity"
    else:
        comparison_status = "completed_with_proxy_mt5_diff"
    return (
        {
            "attempt_name": attempt_name,
            "queue_rank": attempt.get("queue_rank", ""),
            "model_id": attempt.get("model_id", ""),
            "probe_split": attempt.get("probe_split", ""),
            "tester_status": execution.get("status", "not_attempted"),
            "runtime_status": runtime.get("status", "not_attempted"),
            "report_status": report.get("status", "missing") if report else "missing",
            "returncode": execution.get("returncode", ""),
            "blocker": execution.get("blocker", ""),
            "expected_rows": len(expected_by_time),
            "expected_raw_signal_rows": expected_raw_signal_rows,
            "expected_selected_trade_rows": expected_selected_trade_rows,
            "telemetry_cycle_rows": int(len(cycles)),
            "ready_model_rows": int(len(ready)),
            "matched_rows": matched,
            "probability_match_rows": probability_match,
            "decision_match_rows": decision_match,
            "expected_missing_rows": expected_missing,
            "max_abs_probability_diff": max_abs if len(ready) else "",
            "first_ready_bar_time": min(ready_times) if ready_times else "",
            "last_ready_bar_time": max(ready_times) if ready_times else "",
            "latest_expected_bar_time": latest_expected,
            "feature_last_reached": str(feature_last_reached).lower(),
            "comparison_status": comparison_status,
            "feature_ready_count": last_summary.get("feature_ready_count", ""),
            "model_ok_count": last_summary.get("model_ok_count", ""),
            "long_count": last_summary.get("long_count", ""),
            "short_count": last_summary.get("short_count", ""),
            "flat_count": last_summary.get("flat_count", ""),
            "order_attempt_count": last_summary.get("order_attempt_count", ""),
            "order_fill_count": last_summary.get("order_fill_count", ""),
            **report_metric_summary(metrics, feature_day_count, calendar_days),
            "fixed_lot": attempt.get("fixed_lot", ""),
            "max_concurrent_positions": attempt.get("max_concurrent_positions", ""),
            "max_hold_bars": attempt.get("max_hold_bars", ""),
            "no_trade_splitting_status": no_trade_splitting_status(attempt),
            "common_telemetry_path": attempt.get("common_telemetry_path", ""),
            "common_summary_path": attempt.get("common_summary_path", ""),
            "local_telemetry_path": rel(local_telemetry),
            "local_summary_path": rel(local_summary) if exists(local_summary) else "",
            "report_path": report.get("html_report", {}).get("path", "") if isinstance(report.get("html_report"), Mapping) else "",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        diff_rows,
        skip_rows,
    )


def compare_outputs(
    attempts: Sequence[Mapping[str, Any]],
    execution_results: Sequence[Mapping[str, Any]],
    report_records: Sequence[Mapping[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    expected = read_frame(require(SOURCE_EXPECTED_TAPE))
    execution_by_attempt = {row.get("attempt_name"): row for row in execution_results}
    report_by_attempt = {row.get("attempt_name"): row for row in report_records}
    summaries: list[dict[str, Any]] = []
    diffs: list[dict[str, Any]] = []
    skips: list[dict[str, Any]] = []
    for attempt in attempts:
        summary, diff_rows, skip_rows = compare_attempt(
            attempt,
            execution_by_attempt.get(attempt.get("attempt_name"), {}),
            report_by_attempt.get(attempt.get("attempt_name"), {}),
            expected,
        )
        summaries.append(summary)
        diffs.extend(diff_rows)
        skips.extend(skip_rows)
    write_csv(EXECUTION_SUMMARY, summaries)
    write_csv(PROXY_MT5_DIFF, diffs)
    write_csv(TELEMETRY_SKIP_SUMMARY, skips)
    return summaries, diffs, skips


def best_attempt(summaries: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    frame = pd.DataFrame(summaries).fillna("")
    if frame.empty:
        return {}
    for column in [
        "net_profit",
        "profit_factor",
        "recovery_factor",
        "trade_count",
        "expectancy",
        "max_drawdown_amount",
        "trade_density_per_feature_day",
        "matched_rows",
    ]:
        if column in frame.columns:
            frame[column] = pd.to_numeric(frame[column], errors="coerce").fillna(0.0)
    completed = frame.loc[frame["runtime_status"].astype(str).eq("completed")].copy()
    source = completed if not completed.empty else frame
    source = source.sort_values(
        ["net_profit", "profit_factor", "recovery_factor", "trade_density_per_feature_day", "trade_count", "matched_rows"],
        ascending=[False, False, False, False, False, False],
    )
    return source.iloc[0].to_dict()


def write_runtime_identity(args: argparse.Namespace, attempts: Sequence[Mapping[str, Any]]) -> None:
    source_final = read_json(require(SOURCE_FINAL_DECISION))
    rows = []
    for attempt in attempts:
        rows.append(
            {
                "attempt_name": attempt["attempt_name"],
                "terminal_path": args.terminal_path,
                "terminal_exists": exists(Path(args.terminal_path)),
                "common_files_root": args.common_files_root,
                "tester_profile_root": args.tester_profile_root,
                "terminal_data_root": args.terminal_data_root,
                "source_run_id": PARENT_RUN_ID,
                "source_status": source_final.get("status", ""),
                "runtime_module_hashes": mt5.mt5_runtime_module_hashes(),
                "set_sha256": attempt.get("set_sha256", ""),
                "ini_sha256": attempt.get("ini_sha256", ""),
                "model_common_path": attempt.get("model_common_path", ""),
                "feature_csv_path": attempt.get("feature_csv_path", ""),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(RUNTIME_IDENTITY, rows)


def passed_gate(path: Path) -> bool:
    _fields, rows = read_csv_rows(require(path))
    return bool(rows) and all(str(row.get("passed", row.get("status", ""))).lower() in {"true", "passed", "passed(통과)"} for row in rows)


def build_final(
    args: argparse.Namespace,
    attempts: Sequence[Mapping[str, Any]],
    execution_results: Sequence[Mapping[str, Any]],
    report_records: Sequence[Mapping[str, Any]],
    summaries: Sequence[Mapping[str, Any]],
    diffs: Sequence[Mapping[str, Any]],
    copy_rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    write_runtime_identity(args, attempts)
    runtime_completed = sum(1 for row in summaries if str(row.get("runtime_status")) == "completed")
    report_available = sum(1 for row in report_records if str(row.get("status", "")) != "missing")
    all_attempted = len(execution_results) == len(attempts) and len(attempts) > 0
    completed = all_attempted and runtime_completed == len(attempts) and report_available == len(attempts) and not args.materialize_only
    best = best_attempt(summaries)
    parity_rows = [
        row
        for row in summaries
        if str(row.get("comparison_status")) == "completed_probability_decision_parity"
    ]
    positive_runtime_probe = (
        completed
        and bool(parity_rows)
        and to_float(best.get("net_profit"), 0.0) > 0.0
        and to_float(best.get("profit_factor"), 0.0) > 1.0
        and to_float(best.get("trade_density_per_feature_day"), 0.0) >= 3.0
    )
    if completed and positive_runtime_probe:
        judgment = JUDGMENT_POSITIVE
    elif completed:
        judgment = JUDGMENT_WEAK
    else:
        judgment = JUDGMENT_BLOCKED
    status = STATUS_COMPLETED if completed else STATUS_BLOCKED
    next_run_id = NEXT_REVIEW_RUN_ID if completed else NEXT_REPAIR_RUN_ID
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "status": status,
        "judgment": judgment,
        "result_judgment": "runtime_probe" if completed else "blocked",
        "decision": f"stage358C_open_{next_run_id}",
        "next_run_id": next_run_id,
        "claim_boundary": CLAIM_BOUNDARY,
        "attempt_rows": len(attempts),
        "source_attempt_rows": len(read_csv_rows(require(SOURCE_ATTEMPT_PACKAGE))[1]),
        "execution_result_rows": len(execution_results),
        "runtime_completed_rows": runtime_completed,
        "report_rows": len(report_records),
        "report_available_rows": report_available,
        "summary_rows": len(summaries),
        "diff_rows": len(diffs),
        "diff_mismatch_rows": sum(1 for row in diffs if str(row.get("comparison_status")) != "matched"),
        "matched_rows": sum(to_int(row.get("matched_rows")) for row in summaries),
        "ready_model_rows": sum(to_int(row.get("ready_model_rows")) for row in summaries),
        "runtime_output_copy_rows": len(copy_rows),
        "runtime_output_copy_ready_rows": sum(1 for row in copy_rows if norm_bool(row.get("exists"))),
        "proxy_mt5_parity_pass_rows": len(parity_rows),
        "external_verification_status": "completed" if completed else "blocked",
        "best_attempt_name": best.get("attempt_name", ""),
        "best_queue_rank": best.get("queue_rank", ""),
        "best_model_id": best.get("model_id", ""),
        "best_probe_split": best.get("probe_split", ""),
        "best_net_profit": to_float(best.get("net_profit"), 0.0),
        "best_profit_factor": to_float(best.get("profit_factor"), 0.0),
        "best_expectancy": to_float(best.get("expectancy"), 0.0),
        "best_recovery_factor": to_float(best.get("recovery_factor"), 0.0),
        "best_max_drawdown_amount": to_float(best.get("max_drawdown_amount"), 0.0),
        "best_trade_count": to_int(best.get("trade_count"), 0),
        "best_long_trade_count": to_int(best.get("long_trade_count"), 0),
        "best_short_trade_count": to_int(best.get("short_trade_count"), 0),
        "best_trade_density_per_feature_day": to_float(best.get("trade_density_per_feature_day"), 0.0),
        "best_trade_density_requirement_status": best.get("trade_density_requirement_status", ""),
        "positive_runtime_probe": positive_runtime_probe,
        "trade_density_requirement": TRADE_DENSITY_REQUIREMENT,
        "candidate_selection": "not_run",
        "forward_passed": "not_claimed",
        "live_readiness": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
    }


def gate_row(gate_id: str, passed: bool, evidence: str, effect: str) -> dict[str, Any]:
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "gate_id": gate_id,
        "status": "passed" if passed else "failed",
        "evidence": evidence,
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
        "created_at_utc": now_utc(),
    }


def make_gates(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    runtime_ok = final["runtime_completed_rows"] == final["attempt_rows"] and final["attempt_rows"] > 0
    no_forbidden = all(
        final.get(key) in {"not_claimed", "not_run"}
        for key in ["candidate_selection", "forward_passed", "live_readiness", "runtime_authority", "operating_promotion", "goal_achieve"]
    )
    return [
        gate_row("source_run358B_gates_passed", passed_gate(SOURCE_GATE_AUDIT), rel(SOURCE_GATE_AUDIT), "Stage358B handoff is gated before runtime execution."),
        gate_row("runtime_evidence_gate", runtime_ok, rel(MT5_EXECUTION_RESULT), "MT5 runtime outputs exist for attempted rows."),
        gate_row("strategy_report_forensics_gate", final["report_available_rows"] == final["attempt_rows"] and final["attempt_rows"] > 0, rel(STRATEGY_TESTER_REPORTS), "Strategy Tester reports were collected."),
        gate_row("scope_completion_gate", final["execution_result_rows"] == final["attempt_rows"] and final["attempt_rows"] > 0, rel(MT5_EXECUTION_RESULT), "All selected Stage358C attempts have execution records."),
        gate_row("kpi_contract_audit", exists(EXECUTION_SUMMARY) and final["summary_rows"] == final["attempt_rows"], rel(EXECUTION_SUMMARY), "MT5 KPI, risk, and trade density fields were written."),
        gate_row("proxy_mt5_diff_attribution_recorded", exists(PROXY_MT5_DIFF), rel(PROXY_MT5_DIFF), "Proxy-vs-MT5 row differences were recorded for attribution."),
        gate_row("trade_density_requirement_evaluated", exists(EXECUTION_SUMMARY), rel(EXECUTION_SUMMARY), "3-to-10+ trade/day and no trade splitting guardrails were evaluated."),
        gate_row("runtime_identity_recorded", exists(RUNTIME_IDENTITY), rel(RUNTIME_IDENTITY), "Terminal, model, feature, set, ini, and EA identities were recorded."),
        gate_row("artifact_lineage_recorded", exists(LINEAGE_RECEIPT) and exists(RUN_MANIFEST), f"{rel(LINEAGE_RECEIPT)};{rel(RUN_MANIFEST)}", "Artifact lineage connects source package, runtime outputs, and reports."),
        gate_row("tier_pair_rows_written", exists(STAGE_LEDGER) and exists(PROJECT_LEDGER), f"{rel(STAGE_LEDGER)};{rel(PROJECT_LEDGER)}", "Tier A/B/A+B ledger rows exist."),
        gate_row("final_claim_guard", no_forbidden, rel(FINAL_DECISION), "No operating or goal-achieve claim is made."),
    ]


def artifact_paths() -> list[Path]:
    paths = [
        ATTEMPT_PACKAGE,
        SET_RETARGET_MANIFEST,
        INI_RETARGET_MANIFEST,
        TERMINAL_PROCESS_AUDIT,
        MT5_EXECUTION_RESULT,
        STRATEGY_TESTER_REPORTS,
        RUNTIME_OUTPUT_COPY,
        EXECUTION_SUMMARY,
        PROXY_MT5_DIFF,
        TELEMETRY_SKIP_SUMMARY,
        RUNTIME_IDENTITY,
        RUNTIME_RECEIPT,
        BACKTEST_RECEIPT,
        PERFORMANCE_RECEIPT,
        LINEAGE_RECEIPT,
        JUDGMENT_RECEIPT,
        CLAIM_RECEIPT,
        GATE_AUDIT,
        FINAL_DECISION,
        RUN_MANIFEST,
        SELF_CORRECTION_PLAN,
        REPORT_PATH,
        DECISION_DOC,
        Path(__file__),
    ]
    if exists(TELEMETRY_COPY_DIR):
        paths.extend(path for path in TELEMETRY_COPY_DIR.glob("*") if path.is_file())
    if exists(REPORT_COPY_DIR):
        paths.extend(path for path in REPORT_COPY_DIR.glob("*") if path.is_file())
    if exists(MT5_DIR):
        paths.extend(path for path in MT5_DIR.glob("*_tester_execution.json") if path.is_file())
    return paths


def write_receipts(final: Mapping[str, Any]) -> None:
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": final["status"],
        "judgment": final["judgment"],
        "created_at_utc": now_utc(),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(
        RUNTIME_RECEIPT,
        {
            **base,
            "research_path": rel(SOURCE_EXPECTED_TAPE),
            "runtime_path": rel(RUNTIME_OUTPUT_COPY),
            "shared_contract": "58_feature_order_softmax_output_pside_threshold_adx_filter_maxhold12",
            "known_differences": [
                "pside is represented by equal short/long thresholds and negative margin",
                "MT5 fills and lifecycle costs are authoritative for this probe",
                "proxy selected-trade count is non-overlap fixed horizon and is not an MT5 KPI substitute",
            ],
            "parity_check": rel(PROXY_MT5_DIFF),
            "parity_identity": rel(RUNTIME_IDENTITY),
            "runtime_claim_boundary": "runtime_probe" if final["external_verification_status"] == "completed" else "blocked",
        },
    )
    write_json(
        BACKTEST_RECEIPT,
        {
            **base,
            "tester_identity": rel(RUNTIME_IDENTITY),
            "report_identity": rel(STRATEGY_TESTER_REPORTS),
            "trade_evidence": rel(EXECUTION_SUMMARY),
            "cost_assumptions": "Strategy Tester broker settings from FPMarkets portable terminal.",
            "forensic_checks": ["terminal process probe", "report collection", "runtime telemetry copy"],
            "backtest_judgment": "usable_with_boundary" if final["external_verification_status"] == "completed" else "blocked",
        },
    )
    write_json(
        PERFORMANCE_RECEIPT,
        {
            **base,
            "summary": rel(EXECUTION_SUMMARY),
            "proxy_mt5_diff": rel(PROXY_MT5_DIFF),
            "best_attempt_name": final["best_attempt_name"],
            "best_net_profit": final["best_net_profit"],
            "best_profit_factor": final["best_profit_factor"],
            "best_expectancy": final["best_expectancy"],
            "best_recovery_factor": final["best_recovery_factor"],
            "best_trade_count": final["best_trade_count"],
            "best_trade_density_per_feature_day": final["best_trade_density_per_feature_day"],
            "positive_runtime_probe": final["positive_runtime_probe"],
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "result_subject": RUN_ID,
            "evidence_available": [rel(EXECUTION_SUMMARY), rel(PROXY_MT5_DIFF), rel(STRATEGY_TESTER_REPORTS)],
            "evidence_missing": ["forward replay", "runtime authority", "operating promotion evidence"],
            "judgment_label": final["result_judgment"],
            "next_condition": final["next_run_id"],
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "allowed_claims": ["runtime_probe", "proxy_mt5_diff_attribution"],
            "forbidden_claims": ["candidate_selection", "forward_passed", "live_readiness", "operating_promotion", "runtime_authority", "goal_achieve"],
            "goal_achieve": "not_claimed",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [
                rel(SOURCE_ATTEMPT_PACKAGE),
                rel(SOURCE_EXPECTED_TAPE),
                rel(SOURCE_EXPECTED_INDEX),
                rel(SOURCE_MAPPING_AUDIT),
                rel(SOURCE_COMMON_SYNC),
                rel(SOURCE_FINAL_DECISION),
            ],
            "producer": rel(Path(__file__)),
            "consumer": final["next_run_id"],
            "artifact_paths": [rel(path) for path in artifact_paths() if exists(path)],
            "artifact_hashes": {rel(path): sha256_file(path) for path in artifact_paths() if exists(path) and path.is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "generated_with_manifest",
            "lineage_judgment": "connected_with_runtime_probe_boundary",
        },
    )


def write_final_manifest(final_seed: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    final = {
        **final_seed,
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
        "primary_artifacts": {
            "execution_summary": rel(EXECUTION_SUMMARY),
            "proxy_mt5_diff": rel(PROXY_MT5_DIFF),
            "strategy_reports": rel(STRATEGY_TESTER_REPORTS),
            "runtime_identity": rel(RUNTIME_IDENTITY),
            "gate_audit": rel(GATE_AUDIT),
        },
    }
    write_json(FINAL_DECISION, final)
    write_json(
        RUN_MANIFEST,
        {
            **final,
            "artifacts": [
                {"path": rel(path), "sha256": sha256_file(path)}
                for path in artifact_paths()
                if exists(path) and path.is_file()
            ],
        },
    )
    return final


def write_self_correction_plan(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    failed = [row for row in gates if row["status"] != "passed"]
    write_json(
        SELF_CORRECTION_PLAN,
        {
            "run_id": RUN_ID,
            "status": "repair_required" if failed else "no_repair_required",
            "failed_gates": failed,
            "plan_only": bool(failed),
            "repair_policy": "do not relax gates or thresholds; repair handoff/runtime visibility only",
            "next_run_id": final["next_run_id"],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def ledger_rows(final: Mapping[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_date": TODAY,
        "date": TODAY,
        "status": final["status"],
        "judgment": final["judgment"],
        "decision": final["decision"],
        "next_run_id": final["next_run_id"],
        "primary_artifact": rel(FINAL_DECISION),
        "path": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "primary_report": rel(REPORT_PATH),
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
        "scoreboard_lane": "runtime_probe_execution(런타임 탐침 실행)",
        "lane": "runtime_probe_execution(런타임 탐침 실행)",
        "family": "runtime_backtest(런타임 백테스트)",
        "work_family": "runtime_backtest(런타임 백테스트)",
        "run_number": RUN_NUMBER,
        "notes": "Stage358B executable pside/all attempts were sent to MT5 Strategy Tester(358B 실행 가능 pside/all 시도를 MT5 전략 테스터에 보냄).",
        "source_package_run_id": PARENT_RUN_ID,
        "rows": final["summary_rows"],
        "candidate_rows": final["attempt_rows"],
        "external_verification_status": final["external_verification_status"],
        "result_status": final["status"],
        "trade_density_requirement_status": final["best_trade_density_requirement_status"],
        "result_judgment": final["judgment"],
        "final_decision_path": rel(FINAL_DECISION),
        "created_at": TODAY,
        "attempt_rows": final["attempt_rows"],
        "runtime_completed_rows": final["runtime_completed_rows"],
        "matched_rows": final["matched_rows"],
        "mismatch_rows": final["diff_mismatch_rows"],
        "positive_net_rows": "",
        "best_net_profit": final["best_net_profit"],
        "best_profit_factor": final["best_profit_factor"],
        "operating_ready_rows": 0,
        "candidate_model_id": final["best_model_id"],
        "net_profit": final["best_net_profit"],
        "profit_factor": final["best_profit_factor"],
        "expectancy": final["best_expectancy"],
        "drawdown": final["best_max_drawdown_amount"],
        "recovery_factor": final["best_recovery_factor"],
        "trade_count": final["best_trade_count"],
        "sample_rows": final["ready_model_rows"],
        "feature_count": 58,
        "primary_kpi": f"best_net={final['best_net_profit']};pf={final['best_profit_factor']};trades={final['best_trade_count']}",
        "guardrail_kpi": TRADE_DENSITY_REQUIREMENT,
        "runtime_attempt_rows": final["attempt_rows"],
        "max_drawdown_amount": final["best_max_drawdown_amount"],
        "long_trade_count": final["best_long_trade_count"],
        "short_trade_count": final["best_short_trade_count"],
        "trade_density_per_feature_day": final["best_trade_density_per_feature_day"],
    }
    run_registry_row = {
        **base,
        "ledger_row_id": f"{RUN_ID}__Tier_AplusB",
        "subrun_id": "Tier A+B",
        "record_view": "Tier A+B combined(Tier A+B 합산)",
        "view": "Tier A+B combined(Tier A+B 합산)",
        "tier": "Tier A+B",
        "tier_scope": "Tier A+B",
        "metric_scope": "same_as_tier_a_no_fallback(대체 없음 Tier A와 동일)",
        "kpi_scope": "same_as_tier_a_no_fallback(대체 없음 Tier A와 동일)",
        "row_id": f"{RUN_ID}__Tier_AplusB",
    }
    alpha_rows = [
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__Tier_A",
            "row_id": f"{RUN_ID}__Tier_A",
            "subrun_id": "Tier A",
            "record_view": "Tier A separate(Tier A 분리)",
            "view": "Tier A separate(Tier A 분리)",
            "tier": "Tier A",
            "tier_scope": "Tier A",
            "metric_scope": "runtime_probe_execution_full_context(런타임 탐침 실행 전체 문맥)",
            "kpi_scope": "runtime_probe_execution_full_context(런타임 탐침 실행 전체 문맥)",
            "question": "Do Stage358B pside/all attempts survive MT5 Strategy Tester?(358B pside/all 시도가 MT5 전략 테스터에서 살아남는가?)",
            "next_action": final["next_run_id"],
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__Tier_B",
            "row_id": f"{RUN_ID}__Tier_B",
            "subrun_id": "Tier B",
            "record_view": "Tier B separate(Tier B 분리)",
            "view": "Tier B separate(Tier B 분리)",
            "tier": "Tier B",
            "tier_scope": "Tier B",
            "metric_scope": "missing_required_no_partial_context_runtime_execution(Tier B 부분 문맥 런타임 실행 없음 필수 누락)",
            "kpi_scope": "missing_required_no_partial_context_runtime_execution(Tier B 부분 문맥 런타임 실행 없음 필수 누락)",
            "result_status": "missing_required(필수 누락)",
            "primary_kpi": "tier_b_runtime_execution_rows=0",
            "notes": "Tier B partial-context runtime execution is not materialized in Stage358C(Tier B 부분 문맥 런타임 실행은 358C에서 미산출).",
            "question": "Can Tier B partial-context runtime execution be produced?(Tier B 부분 문맥 런타임 실행을 만들 수 있는가?)",
            "next_action": final["next_run_id"],
        },
        {
            **run_registry_row,
            "question": "Can Stage358B package be verified by MT5?(358B 패키지를 MT5로 검증할 수 있는가?)",
            "next_action": final["next_run_id"],
        },
    ]
    return run_registry_row, alpha_rows, alpha_rows


def write_ledgers(final: Mapping[str, Any]) -> None:
    run_row, alpha_rows, stage_rows = ledger_rows(final)
    append_or_replace_csv(RUN_REGISTRY, [run_row], ["run_id"])
    append_or_replace_csv(PROJECT_LEDGER, alpha_rows, ["ledger_row_id"])
    append_or_replace_csv(STAGE_LEDGER, stage_rows, ["ledger_row_id"])


def write_artifact_registry() -> None:
    rows = []
    for path in artifact_paths():
        if not exists(path) or not path.is_file():
            continue
        artifact_id = f"{RUN_ID}::{path.stem}"
        rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": path.suffix.lstrip(".") or "file",
                "path": rel(path),
                "artifact_path": rel(path),
                "sha256": sha256_file(path),
                "created_at": TODAY,
                "created_at_utc": now_utc(),
                "claim_boundary": CLAIM_BOUNDARY,
                "artifact_id": artifact_id,
                "notes": "Stage358C runtime probe execution artifact(358C 런타임 탐침 실행 산출물)",
            }
        )
    append_or_replace_csv(ARTIFACT_REGISTRY, rows, ["artifact_id"])


def write_docs(final: Mapping[str, Any]) -> None:
    next_run_id = final["next_run_id"]
    workspace_state = f"""current_stage_id: {STAGE_ID}
current_run_id: {next_run_id}
latest_completed_run_id: {RUN_ID}
current_status: {final["status"]}
current_judgment: {final["judgment"]}
current_decision: {final["decision"]}
next_run_id: {next_run_id}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
"""
    io(WORKSPACE_STATE.parent).mkdir(parents=True, exist_ok=True)
    io(WORKSPACE_STATE).write_text(workspace_state, encoding="utf-8")

    current_text = f"""# Current Working State(현재 작업 상태)

- current_stage_id(현재 단계 ID): `{STAGE_ID}`
- current_run_id(현재 실행 ID): `{next_run_id}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- current_status(현재 상태): `{final["status"]}`
- current_judgment(현재 판정): `{final["judgment"]}`
- current_decision(현재 결정): `{final["decision"]}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): Stage358C(358C 실행)에서 Stage358B(358B 실행)의 MT5 runtime probe package(MT5 런타임 탐침 패키지)를 Strategy Tester(전략 테스터)에 실행하거나 실행 차단 근거를 기록했다.

Effect(효과): proxy expected value(프록시 예상값)와 MT5 runtime evidence(MT5 런타임 근거)의 비교 범위가 명확해졌고, 운영 주장(operating claim, 운영 주장)은 아직 없다.
"""
    write_bom_text(CURRENT_WORKING_STATE, current_text)

    selection_text = f"""# Stage358 Selection Status(358단계 선택 상태)

- selection_status(선택 상태): `runtime_probe_execution_recorded_no_selection(런타임 탐침 실행 기록, 선택 없음)`
- active_stage_id(활성 단계 ID): `{STAGE_ID}`
- latest_run_id(최근 실행 ID): `{RUN_ID}`
- current_run_id(현재 실행 ID): `{next_run_id}`
- source_run_id(원천 실행 ID): `{PARENT_RUN_ID}`
- attempt_rows(시도 행): `{final["attempt_rows"]}`
- runtime_completed_rows(런타임 완료 행): `{final["runtime_completed_rows"]}`
- report_available_rows(보고서 사용 가능 행): `{final["report_available_rows"]}`
- best_net_profit(최선 순수익): `{final["best_net_profit"]}`
- best_profit_factor(최선 수익 팩터): `{final["best_profit_factor"]}`
- best_trade_count(최선 거래수): `{final["best_trade_count"]}`
- best_trade_density_per_feature_day(최선 피처일별 거래수): `{final["best_trade_density_per_feature_day"]}`
- runtime_authority(런타임 권위): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`

Action(행동): Stage358C(358C 실행)의 MT5 Strategy Tester(MT5 전략 테스터) 결과를 selection(선택) 없이 기록했다.

Effect(효과): 다음 작업은 review/repair(검토/수리) 경계에서 MT5 KPI(MT5 핵심 성과 지표)와 proxy-MT5 diff(프록시-MT5 차이)를 판정한다.
"""
    write_bom_text(SELECTION_STATUS, selection_text)

    brief_text = f"""# Stage358 Runtime Probe Handoff(358단계 런타임 탐침 인계)

- canonical_stage_id(정식 단계 ID): `{STAGE_ID}`
- current_run_id(현재 실행 ID): `{next_run_id}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- source_run_id(원천 실행 ID): `{PARENT_RUN_ID}`
- selection_status(선택 상태): `runtime_probe_execution_recorded_no_selection(런타임 탐침 실행 기록, 선택 없음)`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Stage358C Closeout(358C 종료 기록)

- attempt_rows(시도 행): `{final["attempt_rows"]}`
- runtime_completed_rows(런타임 완료 행): `{final["runtime_completed_rows"]}`
- report_available_rows(보고서 사용 가능 행): `{final["report_available_rows"]}`
- proxy_mt5_parity_pass_rows(프록시-MT5 동등성 통과 행): `{final["proxy_mt5_parity_pass_rows"]}`
- best_attempt_name(최선 시도 이름): `{final["best_attempt_name"]}`
- best_net_profit(최선 순수익): `{final["best_net_profit"]}`
- best_profit_factor(최선 수익 팩터): `{final["best_profit_factor"]}`
- best_trade_count(최선 거래수): `{final["best_trade_count"]}`

Action(행동): Stage358B(358B 실행)에서 만든 pside/all(방향확률/전체 세션) MT5 attempt(시도)를 실행하고 결과를 수집했다.

Effect(효과): proxy(프록시) 신호가 MT5 runtime(런타임)에서 같은 확률/판정으로 관측되는지와 Strategy Tester(전략 테스터) KPI가 어떤지 다음 review(검토)에서 판단할 수 있다.

## Required Boundary(필수 경계)

운영 승격(operating promotion, 운영 승격), 런타임 권위(runtime authority, 런타임 권위), 실거래 준비(live readiness, 실거래 준비), 목표 달성(goal achieve, 목표 달성)은 아직 주장하지 않는다.
"""
    write_bom_text(STAGE_BRIEF, brief_text)

    readme_text = f"""# Stage358 Runtime Probe Handoff(358단계 런타임 탐침 인계)

- current_run(현재 실행): `{next_run_id}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- source_run(원천 실행): `{PARENT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): Stage358C(358C 실행)는 Stage358B(358B 실행)의 executable package(실행 가능 패키지)를 MT5 Strategy Tester(MT5 전략 테스터)에 연결했다.

Effect(효과): Stage358(358단계)은 proxy scout(프록시 탐색)에서 runtime evidence(런타임 근거) 판정으로 이동했다.

## Current Evidence(현재 근거)

- attempt_rows(시도 행): `{final["attempt_rows"]}`
- runtime_completed_rows(런타임 완료 행): `{final["runtime_completed_rows"]}`
- report_available_rows(보고서 사용 가능 행): `{final["report_available_rows"]}`
- best_net_profit(최선 순수익): `{final["best_net_profit"]}`
- best_profit_factor(최선 수익 팩터): `{final["best_profit_factor"]}`
- best_trade_density_per_feature_day(최선 피처일별 거래수): `{final["best_trade_density_per_feature_day"]}`

## Next Work(다음 작업)

- next_run_id(다음 실행 ID): `{next_run_id}`
- action(행동): runtime review/repair(런타임 검토/수리)를 수행한다.
- effect(효과): MT5 KPI(MT5 핵심 성과 지표), proxy-MT5 diff(프록시-MT5 차이), cost stress(비용 압박), trade shape(거래 형태)를 판정한다.
"""
    write_bom_text(STAGE_README, readme_text)

    report_text = f"""# Stage358C High-Density Label Pivot MT5 Probe(358C 고밀도 라벨 전환 MT5 탐침)

## Result(결과)

- status(상태): `{final["status"]}`
- judgment(판정): `{final["judgment"]}`
- next_run_id(다음 실행 ID): `{next_run_id}`
- attempt_rows(시도 행): `{final["attempt_rows"]}`
- runtime_completed_rows(런타임 완료 행): `{final["runtime_completed_rows"]}`
- report_available_rows(보고서 사용 가능 행): `{final["report_available_rows"]}`
- matched_rows(일치 행): `{final["matched_rows"]}`
- diff_mismatch_rows(차이 불일치 행): `{final["diff_mismatch_rows"]}`

Action(행동): Stage358B(358B 실행)의 pside/all(방향확률/전체 세션) attempt(시도)를 MT5 Strategy Tester(MT5 전략 테스터)로 실행하고 telemetry(원격측정), report(보고서), proxy-MT5 diff(프록시-MT5 차이)를 수집했다.

Effect(효과): proxy expected value(프록시 예상값)가 MT5 KPI(MT5 핵심 성과 지표)를 대체하지 않도록, 실제 runtime evidence(런타임 근거)와 분리해 비교할 수 있다.

## Best Runtime Read(최선 런타임 판독)

- best_attempt_name(최선 시도 이름): `{final["best_attempt_name"]}`
- best_model_id(최선 모델 ID): `{final["best_model_id"]}`
- best_probe_split(최선 탐침 분할): `{final["best_probe_split"]}`
- best_net_profit(최선 순수익): `{final["best_net_profit"]}`
- best_profit_factor(최선 수익 팩터): `{final["best_profit_factor"]}`
- best_expectancy(최선 기대값): `{final["best_expectancy"]}`
- best_recovery_factor(최선 회복 계수): `{final["best_recovery_factor"]}`
- best_trade_count(최선 거래수): `{final["best_trade_count"]}`
- best_trade_density_per_feature_day(최선 피처일별 거래수): `{final["best_trade_density_per_feature_day"]}`

## Artifacts(산출물)

- execution_summary(실행 요약): `{rel(EXECUTION_SUMMARY)}`
- proxy_mt5_diff(프록시-MT5 차이): `{rel(PROXY_MT5_DIFF)}`
- strategy_tester_reports(전략 테스터 보고서): `{rel(STRATEGY_TESTER_REPORTS)}`
- runtime_identity(런타임 정체성): `{rel(RUNTIME_IDENTITY)}`
- gate_audit(게이트 감사): `{rel(GATE_AUDIT)}`
- final_decision(최종 결정): `{rel(FINAL_DECISION)}`

## Claim Boundary(주장 경계)

This run(이번 실행)은 runtime probe(런타임 탐침)이다. operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), goal achieve(목표 달성)는 주장하지 않는다.
"""
    write_bom_text(REPORT_PATH, report_text)

    decision_text = f"""# Decision: Stage358C High-Density Label Pivot MT5 Probe(결정: 358C 고밀도 라벨 전환 MT5 탐침)

- decision(결정): `{final["decision"]}`
- status(상태): `{final["status"]}`
- judgment(판정): `{final["judgment"]}`
- next_run_id(다음 실행 ID): `{next_run_id}`

Action(행동): Stage358C(358C 실행)의 MT5 Strategy Tester(MT5 전략 테스터) 실행 근거를 기록했다.

Effect(효과): 다음 작업은 runtime review/repair(런타임 검토/수리)로 이동하며, 운영 주장(operating claim, 운영 주장)은 계속 닫아 둔다.
"""
    write_bom_text(DECISION_DOC, decision_text)


def main() -> None:
    args = parse_args()
    io(RUN_DIR).mkdir(parents=True, exist_ok=True)
    attempts = materialize_attempts(args)
    execution_results, report_records, copy_rows = execute_attempts(args, attempts)
    summaries, diffs, _skips = compare_outputs(attempts, execution_results, report_records)
    final_seed = build_final(args, attempts, execution_results, report_records, summaries, diffs, copy_rows)
    gates = make_gates(final_seed)
    write_csv(GATE_AUDIT, gates)
    final = write_final_manifest(final_seed, gates)
    write_self_correction_plan(final, gates)
    write_receipts(final)
    gates = make_gates(final)
    write_csv(GATE_AUDIT, gates)
    final = write_final_manifest(final, gates)
    write_docs(final)
    write_ledgers(final)
    write_artifact_registry()
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
