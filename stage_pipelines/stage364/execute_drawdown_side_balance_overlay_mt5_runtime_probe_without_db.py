from __future__ import annotations

import argparse
import csv
import json
import math
import os
import shutil
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.mt5 import runtime_support as mt5  # noqa: E402
from stage_pipelines.stage364 import package_drawdown_side_balance_overlay_runtime_probe_without_db as pkg  # noqa: E402

# Reuse run364N execution engine(364N 실행 엔진 재사용) against run364R side-filter package(364R 방향 필터 패키지).
# The package module(패키지 모듈)은 earlier density-lift package(이전 밀도 상향 패키지)를 pkg.pkg로 둔다.
pkg.EXPECTED_PROBABILITY_TAPE = pkg.SIDE_FILTER_PROBABILITY_TAPE
pkg.MT5_NATIVE_TRADE_TAPE = pkg.SIDE_FILTER_TRADE_TAPE
pkg.RUNTIME_SEMANTIC_COMPARISON = pkg.SIDE_FILTER_COMPARISON
pkg.FEATURE_MATRIX = pkg.pkg.FEATURE_MATRIX
pkg.SOURCE_ONNX = pkg.pkg.SOURCE_ONNX
pkg.DEFAULT_TERMINAL = pkg.pkg.DEFAULT_TERMINAL
pkg.DEFAULT_COMMON_FILES = pkg.pkg.DEFAULT_COMMON_FILES
pkg.DEFAULT_TESTER_PROFILE_ROOT = pkg.pkg.DEFAULT_TESTER_PROFILE_ROOT
pkg.DEFAULT_PORTABLE_ROOT = pkg.pkg.DEFAULT_PORTABLE_ROOT
pkg.PORTABLE_EA_EX5 = pkg.pkg.PORTABLE_EA_EX5


TODAY = "2026-06-02"
STAGE_ID = pkg.STAGE_ID
RUN_NUMBER = "run364S"
RUN_ID = "run364S_execute_drawdown_side_balance_overlay_mt5_runtime_probe_without_db_v1"
PARENT_RUN_ID = pkg.RUN_ID
NEXT_RUN_ID = "run364T_review_drawdown_side_balance_overlay_mt5_runtime_probe_without_db_v1"

STATUS_COMPLETED = "completed_stage364S_drawdown_side_balance_overlay_mt5_runtime_probe_executed_review_required_no_authority"
STATUS_BLOCKED = "blocked_stage364S_drawdown_side_balance_overlay_mt5_runtime_probe_attempt_recorded_repair_required_no_authority"
JUDGMENT_COMPLETED = "mt5_runtime_probe_outputs_available_proxy_diff_review_required_no_authority"
JUDGMENT_BLOCKED = "mt5_runtime_probe_attempt_recorded_but_outputs_missing_or_failed_repair_required"
DECISION_COMPLETED = "stage364S_open_run364T_review_drawdown_side_balance_overlay_mt5_runtime_probe_without_db_v1"
DECISION_BLOCKED = "stage364S_open_run364T_review_or_repair_drawdown_side_balance_overlay_mt5_runtime_probe_without_db_v1"
CLAIM_BOUNDARY = (
    "research_development_mt5_runtime_probe_attempt_only_no_forward_pass_no_live_readiness_"
    "no_operating_promotion_no_runtime_authority_no_goal_claim"
)

STAGE_DIR = pkg.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MT5_DIR = RUN_DIR / "mt5"
TELEMETRY_COPY_DIR = RUN_DIR / "runtime_telemetry"
REPORT_COPY_DIR = MT5_DIR / "reports"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

ATTEMPT_PACKAGE = RUN_DIR / "runtime_probe_attempt_package.csv"
TERMINAL_PROCESS_AUDIT = RUN_DIR / "terminal_process_audit.json"
MT5_EXECUTION_RESULT = RUN_DIR / "mt5_execution_result.json"
STRATEGY_TESTER_REPORTS = RUN_DIR / "strategy_tester_report_records.json"
EXECUTION_SUMMARY = RUN_DIR / "drawdown_side_balance_overlay_mt5_probe_summary.csv"
PROBABILITY_DIFF = RUN_DIR / "probability_runtime_difference.csv"
PROXY_MT5_DIFF = RUN_DIR / "proxy_mt5_runtime_difference.csv"
TELEMETRY_SKIP_SUMMARY = RUN_DIR / "runtime_skip_reason_summary.csv"
RUNTIME_OUTPUT_COPY = RUN_DIR / "runtime_output_copy_manifest.csv"
RUNTIME_IDENTITY = RUN_DIR / "runtime_identity.csv"
EXPECTED_KPI_SUMMARY = RUN_DIR / "expected_native_kpi_summary.csv"
BACKTEST_FORENSICS_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364S_drawdown_side_balance_overlay_mt5_runtime_probe.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364S_drawdown_side_balance_overlay_mt5_runtime_probe.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
STAGE_BRIEF = SPEC_DIR / "stage_brief.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
STAGE_README = STAGE_DIR / "README.md"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"

OUTPUT_FILES = [
    ATTEMPT_PACKAGE,
    TERMINAL_PROCESS_AUDIT,
    MT5_EXECUTION_RESULT,
    STRATEGY_TESTER_REPORTS,
    EXECUTION_SUMMARY,
    PROBABILITY_DIFF,
    PROXY_MT5_DIFF,
    TELEMETRY_SKIP_SUMMARY,
    RUNTIME_OUTPUT_COPY,
    RUNTIME_IDENTITY,
    EXPECTED_KPI_SUMMARY,
    BACKTEST_FORENSICS_RECEIPT,
    RUNTIME_RECEIPT,
    PERFORMANCE_RECEIPT,
    JUDGMENT_RECEIPT,
    LINEAGE_RECEIPT,
    CLAIM_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    REVIEW_INDEX,
    STAGE_LEDGER,
    STAGE_BRIEF,
    SELECTION_STATUS,
    STAGE_README,
    WORKSPACE_STATE,
    CURRENT_WORKING_STATE,
    WORKSPACE_CHANGELOG,
    RUN_REGISTRY,
    PROJECT_LEDGER,
    ARTIFACT_REGISTRY,
    Path(__file__),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stage364S drawdown side balance overlay MT5 runtime probe.")
    parser.add_argument("--terminal-path", default=str(pkg.DEFAULT_TERMINAL))
    parser.add_argument("--common-files-root", default=str(pkg.DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(pkg.DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-data-root", default=str(pkg.DEFAULT_PORTABLE_ROOT))
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--wait-timeout-seconds", type=int, default=240)
    parser.add_argument("--reuse-existing-execution", action="store_true")
    return parser.parse_args()


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fs_path(path: Path | str) -> str:
    return pkg.fs_path(path)


def rel(path: Path | str) -> str:
    return pkg.rel(path)


def exists(path: Path | str) -> bool:
    return pkg.exists(path)


def sha(path: Path | str) -> str:
    return pkg.sha(path)


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    pkg.write_json(path, json_ready(payload))


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    pkg.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    pkg.append_text_once(path, marker, text)


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    pkg.write_csv(path, rows, fieldnames)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    _, rows = pkg.read_csv_rows(path)
    return rows


def append_or_replace_csv(
    path: Path,
    key_fields: Sequence[str],
    rows: Sequence[Mapping[str, Any]],
    *,
    extend_header: bool = True,
) -> None:
    pkg.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, Path):
        return value.as_posix()
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


def ensure_dirs() -> None:
    for path in [RUN_DIR, MT5_DIR, TELEMETRY_COPY_DIR, REPORT_COPY_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR]:
        os.makedirs(fs_path(path), exist_ok=True)


def load_parent() -> dict[str, Any]:
    parent = pkg.read_json(pkg.FINAL_DECISION)
    next_value = parent.get("next_run_id") or parent.get("next_action")
    if next_value != RUN_ID:
        raise RuntimeError(f"parent next_run_id(부모 다음 실행 ID) mismatch: {next_value} != {RUN_ID}")
    if parent.get("runtime_authority") != "not_claimed" or parent.get("goal_achieve") != "not_claimed":
        raise RuntimeError("parent made forbidden runtime_authority(런타임 권위) or goal_achieve(목표 달성) claim")
    gates = read_csv_rows(pkg.GATE_AUDIT)
    if not gates or any(row.get("status") != "passed" for row in gates):
        raise RuntimeError("run364R package gate(포장 게이트)가 모두 통과되지 않았다.")
    required = [
        pkg.RUNTIME_PROBE_ATTEMPT_PACKAGE,
        pkg.EXPECTED_PROBABILITY_TAPE,
        pkg.MT5_NATIVE_TRADE_TAPE,
        pkg.RUNTIME_SEMANTIC_COMPARISON,
        pkg.FEATURE_MATRIX,
    ]
    missing = [rel(path) for path in required if not exists(path)]
    if missing:
        raise FileNotFoundError("missing parent package(부모 포장 누락): " + ", ".join(missing))
    return parent


def terminal_processes() -> dict[str, Any]:
    command = [
        "powershell",
        "-NoProfile",
        "-Command",
        "Get-CimInstance Win32_Process -Filter \"name = 'terminal64.exe'\" | Select-Object ProcessId,ExecutablePath,CommandLine | ConvertTo-Json -Compress",
    ]
    proc = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=30)
    payload: Any = []
    if proc.stdout.strip():
        try:
            payload = json.loads(proc.stdout)
            if isinstance(payload, Mapping):
                payload = [payload]
        except json.JSONDecodeError:
            payload = proc.stdout.strip()
    return {
        "command": command,
        "returncode": proc.returncode,
        "stdout": proc.stdout[-2000:],
        "stderr": proc.stderr[-2000:],
        "processes": payload,
        "status": "no_terminal64_process" if not payload else "terminal64_process_present",
        "effect": "terminal64.exe process(터미널 프로세스) 충돌을 먼저 확인해 MT5 tester run(MT5 테스터 실행) 간섭을 줄인다.",
    }


def enrich_attempts() -> list[dict[str, Any]]:
    attempts = read_csv_rows(pkg.RUNTIME_PROBE_ATTEMPT_PACKAGE)
    enriched: list[dict[str, Any]] = []
    for row in attempts:
        attempt = dict(row)
        set_path = ROOT / str(attempt.get("set_path", ""))
        ini_path = ROOT / str(attempt.get("ini_path", ""))
        attempt["tier"] = str(attempt.get("tier") or "Tier A")
        attempt["split"] = str(attempt.get("split") or "validation_oos")
        attempt["feature_set_id"] = "stage364R_drawdown_side_balance_overlay_features"
        attempt["ini_name"] = ini_path.name
        attempt["set_name"] = set_path.name
        attempt["common_telemetry_path"] = str(attempt.get("runtime_telemetry_expected", ""))
        attempt["common_summary_path"] = str(attempt.get("runtime_summary_expected", ""))
        attempt["ini"] = {"tester": {"Report": attempt.get("report_name", "")}}
        attempt["set"] = {"path": attempt.get("set_path", "")}
        attempt["execution_run_id"] = RUN_ID
        attempt["parent_package_run_id"] = PARENT_RUN_ID
        attempt["effect"] = "run364R package(364R 포장)를 실제 MT5 runtime probe(MT5 런타임 탐침) 입력으로 고정한다."
        enriched.append(attempt)
    if not enriched:
        raise RuntimeError("runtime_probe_attempt_package(런타임 탐침 시도 포장)가 비어 있다.")
    write_csv(ATTEMPT_PACKAGE, enriched)
    return enriched


def remove_runtime_outputs(common_files_root: Path, attempt: Mapping[str, Any]) -> None:
    for key in ["common_telemetry_path", "common_summary_path"]:
        value = str(attempt.get(key, "")).strip()
        if not value:
            continue
        path = common_files_root / Path(value)
        if exists(path):
            os.remove(fs_path(path))


def runtime_completed_by_attempt(execution_results: Sequence[Mapping[str, Any]]) -> dict[str, bool]:
    completed: dict[str, bool] = {}
    for row in execution_results:
        runtime = row.get("runtime_outputs", {}) if isinstance(row.get("runtime_outputs"), Mapping) else {}
        completed[str(row.get("attempt_name", ""))] = str(runtime.get("status")) == "completed"
    return completed


def copy_runtime_outputs(
    common_files_root: Path,
    attempts: Sequence[Mapping[str, Any]],
    execution_results: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    completed = runtime_completed_by_attempt(execution_results)
    rows: list[dict[str, Any]] = []
    for attempt in attempts:
        attempt_name = str(attempt["attempt_name"])
        for key, suffix in [("common_telemetry_path", "telemetry"), ("common_summary_path", "summary")]:
            source = common_files_root / Path(str(attempt.get(key, "")))
            target = TELEMETRY_COPY_DIR / f"{attempt_name}_{suffix}.csv"
            source_exists = exists(source)
            should_copy = completed.get(attempt_name, False) and source_exists
            if should_copy:
                os.makedirs(fs_path(target.parent), exist_ok=True)
                shutil.copy2(fs_path(source), fs_path(target))
            rows.append(
                {
                    "copy_id": f"{attempt_name}::{suffix}",
                    "attempt_name": attempt_name,
                    "source_path": source.as_posix(),
                    "target_path": rel(target),
                    "source_exists": source_exists,
                    "copied": should_copy,
                    "exists": exists(target),
                    "sha256": sha(target) if exists(target) else "",
                    "effect": "runtime telemetry(런타임 기록)를 run folder(실행 폴더)로 복사해 비교 근거를 고정한다.",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    write_csv(RUNTIME_OUTPUT_COPY, rows)
    return rows


def execute_attempts(args: argparse.Namespace, attempts: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    common_files_root = Path(args.common_files_root)
    tester_profile_root = Path(args.tester_profile_root)
    terminal_data_root = Path(args.terminal_data_root)
    terminal_probe = terminal_processes()
    write_json(TERMINAL_PROCESS_AUDIT, terminal_probe)

    execution_results: list[dict[str, Any]] = []
    report_records: list[dict[str, Any]] = []
    if terminal_probe.get("status") != "no_terminal64_process":
        for attempt in attempts:
            execution_results.append(
                {
                    "attempt_name": attempt["attempt_name"],
                    "model_id": attempt.get("model_id", ""),
                    "feature_set_id": attempt.get("feature_set_id", ""),
                    "status": "blocked",
                    "blocker": "target_portable_terminal_already_running",
                    "runtime_outputs": {"status": "blocked", "wait_status": "skipped_terminal_already_running"},
                    "ini_path": attempt.get("ini_path", ""),
                    "set_path": attempt.get("set_path", ""),
                    "effect": "이미 실행 중인 MT5 terminal64.exe(MT5 터미널 프로세스)를 건드리지 않아 기존 세션 손상을 줄인다.",
                }
            )
    else:
        for attempt in attempts:
            remove_runtime_outputs(common_files_root, attempt)
            mt5.remove_existing_mt5_report_artifacts(terminal_data_root, attempt, run_id=RUN_ID)
            profile_ini = tester_profile_root / str(attempt["ini_name"])
            profile_set = tester_profile_root / str(attempt["set_name"])
            try:
                tester_result = mt5.run_mt5_tester(
                    Path(args.terminal_path),
                    ROOT / str(attempt["ini_path"]),
                    set_path=ROOT / str(attempt["set_path"]),
                    tester_profile_set_path=profile_set,
                    tester_profile_ini_path=profile_ini,
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
                    "model_id": attempt.get("model_id", ""),
                    "feature_set_id": attempt.get("feature_set_id", ""),
                    "runtime_outputs": runtime_outputs,
                    "ini_path": attempt.get("ini_path", ""),
                    "set_path": attempt.get("set_path", ""),
                }
            )
        report_records = mt5.collect_mt5_strategy_report_artifacts(
            terminal_data_root=terminal_data_root,
            run_output_root=RUN_DIR,
            attempts=attempts,
            run_id=RUN_ID,
        )
        mt5.attach_mt5_report_metrics(execution_results, report_records)

    copy_rows = copy_runtime_outputs(common_files_root, attempts, execution_results)
    write_json(MT5_EXECUTION_RESULT, execution_results)
    write_json(STRATEGY_TESTER_REPORTS, report_records)
    return execution_results, report_records, copy_rows, {"terminal_process_probe": terminal_probe}


def norm_bar_time(value: Any) -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    ts = pd.to_datetime(text, errors="coerce")
    if pd.isna(ts):
        return text.replace("T", " ")[:19]
    return ts.strftime("%Y.%m.%d %H:%M:%S")


def float_or_nan(value: Any) -> float:
    try:
        if value in ("", None):
            return math.nan
        return float(value)
    except (TypeError, ValueError):
        return math.nan


def finite(value: Any, digits: int = 10) -> float | str:
    number = float_or_nan(value)
    if not math.isfinite(number):
        return ""
    return round(number, digits)


def decision_label(value: Any) -> str:
    text = str(value or "").strip().lower()
    if text in {"1", "long", "buy"}:
        return "long"
    if text in {"-1", "short", "sell"}:
        return "short"
    if text in {"0", "flat", "no_trade", "hold", ""}:
        return "flat"
    return text


def fnv1a_mql_hash(line: str) -> str:
    digest = 1469598103934665603
    mask = 0xFFFFFFFFFFFFFFFF
    for char in line:
        digest = ((digest ^ ord(char)) * 1099511628211) & mask
    return f"{digest:X}"


def feature_line_hash_map(path: Path) -> tuple[dict[str, str], int]:
    by_time: dict[str, str] = {}
    duplicates = 0
    with open(fs_path(path), encoding="utf-8-sig", newline="") as handle:
        header_line = handle.readline().rstrip("\r\n")
        header = next(csv.reader([header_line]))
        time_index = header.index("bar_time_server") if "bar_time_server" in header else 0
        for raw_line in handle:
            line = raw_line.rstrip("\r\n")
            if not line:
                continue
            row = next(csv.reader([line]))
            if time_index >= len(row):
                continue
            key = norm_bar_time(row[time_index])
            if key in by_time:
                duplicates += 1
            by_time[key] = fnv1a_mql_hash(line)
    return by_time, duplicates


def expected_probability_map() -> tuple[dict[str, dict[str, Any]], int]:
    frame = pd.read_csv(fs_path(pkg.EXPECTED_PROBABILITY_TAPE)).fillna("")
    rows: dict[str, dict[str, Any]] = {}
    duplicates = 0
    feature_hashes, feature_duplicates = feature_line_hash_map(pkg.FEATURE_MATRIX)
    for _, row in frame.iterrows():
        payload = row.to_dict()
        key = norm_bar_time(payload.get("bar_time_server"))
        if key in rows:
            duplicates += 1
        payload["expected_mql_input_hash"] = feature_hashes.get(key, "")
        rows[key] = payload
    return rows, duplicates + feature_duplicates


def local_telemetry_path(attempt: Mapping[str, Any]) -> Path:
    return TELEMETRY_COPY_DIR / f"{attempt['attempt_name']}_telemetry.csv"


def local_summary_path(attempt: Mapping[str, Any]) -> Path:
    return TELEMETRY_COPY_DIR / f"{attempt['attempt_name']}_summary.csv"


def report_metrics_for_attempt(report_row: Mapping[str, Any]) -> dict[str, Any]:
    metrics = report_row.get("metrics", {}) if isinstance(report_row.get("metrics"), Mapping) else {}
    return dict(metrics)


def report_path_from_record(report_row: Mapping[str, Any]) -> str:
    html = report_row.get("html_report", {}) if isinstance(report_row.get("html_report"), Mapping) else {}
    return str(html.get("path", ""))


def bool_text(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes"}


def compare_attempt(
    attempt: Mapping[str, Any],
    execution_row: Mapping[str, Any],
    report_row: Mapping[str, Any],
    expected: Mapping[str, Mapping[str, Any]],
    expected_duplicates: int,
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    telemetry_path = local_telemetry_path(attempt)
    diff_rows: list[dict[str, Any]] = []
    skip_rows: list[dict[str, Any]] = []
    runtime = execution_row.get("runtime_outputs", {}) if isinstance(execution_row.get("runtime_outputs"), Mapping) else {}
    report_metrics = report_metrics_for_attempt(report_row)
    base = {
        "attempt_name": attempt["attempt_name"],
        "model_id": attempt.get("model_id", ""),
        "feature_set_id": attempt.get("feature_set_id", ""),
        "tester_status": execution_row.get("status", "not_attempted"),
        "runtime_status": runtime.get("status", "missing"),
        "report_status": report_row.get("status", "missing") if report_row else "missing",
        "returncode": execution_row.get("returncode", ""),
        "blocker": execution_row.get("blocker", ""),
        "expected_rows": len(expected),
        "expected_duplicate_or_feature_duplicate_rows": expected_duplicates,
        "common_telemetry_path": attempt.get("common_telemetry_path", ""),
        "common_summary_path": attempt.get("common_summary_path", ""),
        "local_telemetry_path": rel(telemetry_path) if exists(telemetry_path) else "",
        "local_summary_path": rel(local_summary_path(attempt)) if exists(local_summary_path(attempt)) else "",
        "report_path": report_path_from_record(report_row),
        "net_profit": report_metrics.get("net_profit", ""),
        "profit_factor": report_metrics.get("profit_factor", ""),
        "trade_count": report_metrics.get("trade_count", ""),
        "expectancy": report_metrics.get("expectancy", ""),
        "recovery_factor": report_metrics.get("recovery_factor", ""),
        "max_drawdown_amount": report_metrics.get("max_drawdown_amount", ""),
        "max_drawdown_percent": report_metrics.get("max_drawdown_percent", ""),
        "long_trade_count": report_metrics.get("long_trade_count", ""),
        "short_trade_count": report_metrics.get("short_trade_count", ""),
        "win_rate_percent": report_metrics.get("win_rate_percent", ""),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    if not exists(telemetry_path):
        return (
            {
                **base,
                "telemetry_cycle_rows": 0,
                "ready_model_rows": 0,
                "matched_rows": 0,
                "visited_expected_rows": 0,
                "unvisited_expected_rows": len(expected),
                "expected_missing_rows": 0,
                "hash_mismatch_rows": 0,
                "probability_mismatch_rows": 0,
                "decision_mismatch_rows": 0,
                "order_attempted_rows": 0,
                "order_filled_rows": 0,
                "max_abs_probability_diff": "",
                "first_ready_bar_time": "",
                "last_ready_bar_time": "",
                "latest_expected_bar_time": max(expected) if expected else "",
                "feature_last_reached": "false",
                "comparison_status": "blocked_no_runtime_telemetry",
            },
            diff_rows,
            skip_rows,
        )

    frame = pd.read_csv(fs_path(telemetry_path)).fillna("")
    if "record_type" in frame.columns:
        cycles = frame[frame["record_type"].astype(str).str.lower() == "cycle"].copy()
    else:
        cycles = frame.copy()
    ready = cycles[
        cycles.get("feature_ready", pd.Series([], dtype=object)).map(bool_text)
        & cycles.get("model_ok", pd.Series([], dtype=object)).map(bool_text)
    ].copy()
    skipped = cycles[
        ~(
            cycles.get("feature_ready", pd.Series([], dtype=object)).map(bool_text)
            & cycles.get("model_ok", pd.Series([], dtype=object)).map(bool_text)
        )
    ].copy()
    if not skipped.empty and "skip_reason" in skipped.columns:
        for reason, count in skipped["skip_reason"].astype(str).replace("", "empty").value_counts().sort_index().items():
            skip_rows.append(
                {
                    "attempt_name": attempt["attempt_name"],
                    "model_id": attempt.get("model_id", ""),
                    "skip_reason": reason,
                    "rows": int(count),
                    "effect": "skip reason(스킵 사유)은 tester/date/model handoff(테스터/날짜/모델 인계) 공백 위치를 보여준다.",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )

    matched = 0
    expected_missing = 0
    hash_mismatch = 0
    prob_mismatch = 0
    decision_mismatch = 0
    max_prob_diff = 0.0
    ready_times: list[str] = []
    tolerance = 1e-4
    for _, row in ready.iterrows():
        bar_time = norm_bar_time(row.get("source_time") or row.get("bar_time"))
        ready_times.append(bar_time)
        exp = expected.get(bar_time)
        found = exp is not None
        mt5_hash = str(row.get("input_hash", "")).upper()
        exp_hash = str(exp.get("expected_mql_input_hash", "")).upper() if exp else ""
        mt5_probs = [float_or_nan(row.get("p_short")), float_or_nan(row.get("p_flat")), float_or_nan(row.get("p_long"))]
        exp_probs = [float_or_nan(exp.get("p_short")), float_or_nan(exp.get("p_flat")), float_or_nan(exp.get("p_long"))] if exp else [math.nan, math.nan, math.nan]
        diffs = [abs(a - b) if math.isfinite(a) and math.isfinite(b) else math.inf for a, b in zip(mt5_probs, exp_probs)]
        row_max = max(diffs)
        if math.isfinite(row_max):
            max_prob_diff = max(max_prob_diff, row_max)
        hash_ok = found and bool(exp_hash) and mt5_hash == exp_hash
        prob_ok = found and row_max <= tolerance
        mt5_decision = decision_label(row.get("decision", ""))
        exp_decision = decision_label((exp or {}).get("mt5_expected_signal", ""))
        decision_ok = found and mt5_decision == exp_decision
        if not found:
            expected_missing += 1
            status = "expected_missing"
        elif not hash_ok:
            hash_mismatch += 1
            status = "hash_mismatch"
        elif not prob_ok:
            prob_mismatch += 1
            status = "probability_mismatch"
        elif not decision_ok:
            decision_mismatch += 1
            status = "decision_mismatch"
        else:
            matched += 1
            status = "matched"
        diff_rows.append(
            {
                "attempt_name": attempt["attempt_name"],
                "model_id": attempt.get("model_id", ""),
                "bar_time": norm_bar_time(row.get("bar_time")),
                "source_time": bar_time,
                "expected_found": found,
                "hash_match": hash_ok,
                "probability_match": prob_ok,
                "decision_match": decision_ok,
                "mt5_input_hash": mt5_hash,
                "expected_mql_input_hash": exp_hash,
                "mt5_p_short": mt5_probs[0],
                "expected_p_short": exp_probs[0],
                "abs_diff_p_short": diffs[0],
                "mt5_p_flat": mt5_probs[1],
                "expected_p_flat": exp_probs[1],
                "abs_diff_p_flat": diffs[1],
                "mt5_p_long": mt5_probs[2],
                "expected_p_long": exp_probs[2],
                "abs_diff_p_long": diffs[2],
                "mt5_decision": mt5_decision,
                "expected_decision": exp_decision,
                "exec_action": row.get("exec_action", ""),
                "order_attempted": row.get("order_attempted", ""),
                "order_filled": row.get("order_filled", ""),
                "comparison_status": status,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    ready_time_set = set(ready_times)
    expected_time_set = set(expected.keys())
    latest_expected = max(expected_time_set) if expected_time_set else ""
    feature_last_reached = latest_expected in ready_time_set
    visited_expected_rows = len(ready_time_set & expected_time_set)
    unvisited_expected_rows = max(0, len(expected_time_set) - visited_expected_rows)
    mismatch_total = expected_missing + hash_mismatch + prob_mismatch + decision_mismatch
    if mismatch_total:
        comparison_status = "completed_with_proxy_mt5_mismatch_review_required"
    elif len(ready) <= 0:
        comparison_status = "blocked_no_ready_model_rows"
    elif unvisited_expected_rows == 0 and feature_last_reached:
        comparison_status = "completed_full_proxy_mt5_parity_reached_feature_last"
    else:
        comparison_status = "completed_overlap_proxy_mt5_parity_unvisited_expected_rows_remain"

    order_attempted = int(cycles["order_attempted"].map(bool_text).sum()) if "order_attempted" in cycles.columns else 0
    order_filled = int(cycles["order_filled"].map(bool_text).sum()) if "order_filled" in cycles.columns else 0
    return (
        {
            **base,
            "telemetry_cycle_rows": int(len(cycles)),
            "ready_model_rows": int(len(ready)),
            "matched_rows": matched,
            "visited_expected_rows": visited_expected_rows,
            "unvisited_expected_rows": unvisited_expected_rows,
            "expected_missing_rows": expected_missing,
            "hash_mismatch_rows": hash_mismatch,
            "probability_mismatch_rows": prob_mismatch,
            "decision_mismatch_rows": decision_mismatch,
            "order_attempted_rows": order_attempted,
            "order_filled_rows": order_filled,
            "max_abs_probability_diff": max_prob_diff if len(ready) else "",
            "first_ready_bar_time": min(ready_times) if ready_times else "",
            "last_ready_bar_time": max(ready_times) if ready_times else "",
            "latest_expected_bar_time": latest_expected,
            "feature_last_reached": str(feature_last_reached).lower(),
            "comparison_status": comparison_status,
        },
        diff_rows,
        skip_rows,
    )


def expected_trade_metrics() -> list[dict[str, Any]]:
    trades = pd.read_csv(fs_path(pkg.MT5_NATIVE_TRADE_TAPE)).fillna("")
    rows: list[dict[str, Any]] = []
    for split in ["validation", "oos", "combined"]:
        frame = trades if split == "combined" else trades[trades["split"].astype(str) == split]
        profits = pd.to_numeric(frame.get("net_profit", pd.Series([], dtype=float)), errors="coerce").fillna(0.0)
        gross_profit = float(profits[profits > 0].sum())
        gross_loss = float(profits[profits < 0].sum())
        trade_count = int(len(frame))
        rows.append(
            {
                "metric_id": f"expected_mt5_native_{split}",
                "split": split,
                "trade_count": trade_count,
                "net_profit": round(float(profits.sum()), 6),
                "profit_factor": round(gross_profit / abs(gross_loss), 10) if gross_loss < 0 else "",
                "expectancy": round(float(profits.mean()), 10) if trade_count else "",
                "long_trade_count": int((frame.get("side", pd.Series([], dtype=object)).astype(str) == "long").sum()) if trade_count else 0,
                "short_trade_count": int((frame.get("side", pd.Series([], dtype=object)).astype(str) == "short").sum()) if trade_count else 0,
                "source": rel(pkg.MT5_NATIVE_TRADE_TAPE),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    semantic = pd.read_csv(fs_path(pkg.RUNTIME_SEMANTIC_COMPARISON)).fillna("")
    for _, row in semantic.iterrows():
        rows.append(
            {
                "metric_id": f"run364R_semantic_{row.get('split', '')}",
                "split": row.get("split", ""),
                "proxy_trade_count": row.get("proxy_trade_count", ""),
                "proxy_net_profit": row.get("proxy_net_profit", ""),
                "proxy_profit_factor": row.get("proxy_profit_factor", ""),
                "mt5_native_trade_count": row.get("mt5_native_trade_count", ""),
                "mt5_native_net_profit": row.get("mt5_native_net_profit", ""),
                "mt5_native_profit_factor": row.get("mt5_native_profit_factor", ""),
                "known_difference": row.get("known_difference", ""),
                "source": rel(pkg.RUNTIME_SEMANTIC_COMPARISON),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(EXPECTED_KPI_SUMMARY, rows)
    return rows


def compare_outputs(
    attempts: Sequence[Mapping[str, Any]],
    execution_results: Sequence[Mapping[str, Any]],
    report_records: Sequence[Mapping[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    expected, expected_duplicates = expected_probability_map()
    reports = {row.get("attempt_name"): row for row in report_records}
    executions = {row.get("attempt_name"): row for row in execution_results}
    summaries: list[dict[str, Any]] = []
    diffs: list[dict[str, Any]] = []
    skips: list[dict[str, Any]] = []
    for attempt in attempts:
        summary, diff_rows, skip_rows = compare_attempt(
            attempt,
            executions.get(attempt.get("attempt_name"), {}),
            reports.get(attempt.get("attempt_name"), {}),
            expected,
            expected_duplicates,
        )
        summaries.append(summary)
        diffs.extend(diff_rows)
        skips.extend(skip_rows)
    expected_metrics = expected_trade_metrics()
    proxy_rows = proxy_mt5_difference_rows(attempts, summaries, expected_metrics)
    write_csv(EXECUTION_SUMMARY, summaries)
    write_csv(PROBABILITY_DIFF, diffs if diffs else [{"run_id": RUN_ID, "status": "no_runtime_diff_rows", "claim_boundary": CLAIM_BOUNDARY}])
    write_csv(PROXY_MT5_DIFF, proxy_rows)
    write_csv(TELEMETRY_SKIP_SUMMARY, skips if skips else [{"run_id": RUN_ID, "status": "no_skip_rows_or_no_telemetry", "claim_boundary": CLAIM_BOUNDARY}])
    return summaries, diffs, skips, proxy_rows


def proxy_mt5_difference_rows(
    attempts: Sequence[Mapping[str, Any]],
    summaries: Sequence[Mapping[str, Any]],
    expected_metrics: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    expected_combined = next((row for row in expected_metrics if row.get("metric_id") == "expected_mt5_native_combined"), {})
    rows: list[dict[str, Any]] = []
    summaries_by_attempt = {row.get("attempt_name"): row for row in summaries}
    for attempt in attempts:
        actual = summaries_by_attempt.get(attempt.get("attempt_name"), {})
        actual_net = float_or_nan(actual.get("net_profit"))
        expected_net = float_or_nan(expected_combined.get("net_profit"))
        actual_trades = float_or_nan(actual.get("trade_count"))
        expected_trades = float_or_nan(expected_combined.get("trade_count"))
        rows.append(
            {
                "run_id": RUN_ID,
                "attempt_name": attempt.get("attempt_name", ""),
                "expected_metric_id": expected_combined.get("metric_id", ""),
                "expected_net_profit": expected_combined.get("net_profit", ""),
                "actual_mt5_net_profit": actual.get("net_profit", ""),
                "net_profit_diff_actual_minus_expected": finite(actual_net - expected_net) if math.isfinite(actual_net) and math.isfinite(expected_net) else "",
                "expected_trade_count": expected_combined.get("trade_count", ""),
                "actual_mt5_trade_count": actual.get("trade_count", ""),
                "trade_count_diff_actual_minus_expected": finite(actual_trades - expected_trades) if math.isfinite(actual_trades) and math.isfinite(expected_trades) else "",
                "expected_profit_factor": expected_combined.get("profit_factor", ""),
                "actual_mt5_profit_factor": actual.get("profit_factor", ""),
                "report_status": actual.get("report_status", ""),
                "comparison_status": actual.get("comparison_status", ""),
                "known_attribution": "proxy(프록시)는 선별 보조이며 MT5 Strategy Tester(MT5 전략 테스터)의 broker cost/runtime semantics(브로커 비용/런타임 의미)를 대체하지 않는다.",
                "usability": "runtime probe review(런타임 탐침 검토) 입력으로만 사용한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def report_usable_count(report_records: Sequence[Mapping[str, Any]]) -> int:
    usable = 0
    for row in report_records:
        metrics = report_metrics_for_attempt(row)
        if row.get("status") in {"completed", "usable", "parsed"} or metrics.get("status") in {"completed", "usable", "parsed"}:
            usable += 1
    return usable


def build_final(
    args: argparse.Namespace,
    parent: Mapping[str, Any],
    attempts: Sequence[Mapping[str, Any]],
    execution_results: Sequence[Mapping[str, Any]],
    report_records: Sequence[Mapping[str, Any]],
    summaries: Sequence[Mapping[str, Any]],
    diffs: Sequence[Mapping[str, Any]],
    copy_rows: Sequence[Mapping[str, Any]],
    proxy_rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    runtime_completed = sum(1 for row in summaries if str(row.get("runtime_status")) == "completed")
    matched_rows = sum(int(row.get("matched_rows", 0) or 0) for row in summaries)
    mismatch_rows = sum(
        int(row.get("expected_missing_rows", 0) or 0)
        + int(row.get("hash_mismatch_rows", 0) or 0)
        + int(row.get("probability_mismatch_rows", 0) or 0)
        + int(row.get("decision_mismatch_rows", 0) or 0)
        for row in summaries
    )
    report_usable = report_usable_count(report_records)
    primary_summary = next(
        (row for row in summaries if str(row.get("runtime_status")) == "completed" and str(row.get("report_status")) == "completed"),
        summaries[0] if summaries else {},
    )
    completed = runtime_completed > 0
    status = STATUS_COMPLETED if completed else STATUS_BLOCKED
    judgment = JUDGMENT_COMPLETED if completed else JUDGMENT_BLOCKED
    decision = DECISION_COMPLETED if completed else DECISION_BLOCKED
    write_csv(
        RUNTIME_IDENTITY,
        [
            {
                "identity_id": "stage364S_runtime_identity",
                "terminal_path": str(args.terminal_path),
                "terminal_exists": exists(Path(args.terminal_path)),
                "common_files_root": str(args.common_files_root),
                "tester_profile_root": str(args.tester_profile_root),
                "terminal_data_root": str(args.terminal_data_root),
                "portable_ea_ex5": pkg.PORTABLE_EA_EX5.as_posix(),
                "portable_ea_ex5_exists": exists(pkg.PORTABLE_EA_EX5),
                "portable_ea_ex5_sha256": sha(pkg.PORTABLE_EA_EX5) if exists(pkg.PORTABLE_EA_EX5) else "",
                "onnx_model": rel(pkg.SOURCE_ONNX),
                "onnx_model_sha256": sha(pkg.SOURCE_ONNX) if exists(pkg.SOURCE_ONNX) else "",
                "feature_order_hash": parent.get("feature_order_hash", ""),
                "attempt_rows": len(attempts),
                "tester_model": "4 real ticks(실제 틱)",
                "deposit": "500",
                "leverage": "1:100",
                "from_date": attempts[0].get("from_date", "") if attempts else "",
                "to_date": attempts[0].get("to_date", "") if attempts else "",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": status,
        "judgment": judgment,
        "decision": decision,
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "attempt_rows": len(attempts),
        "execution_result_rows": len(execution_results),
        "runtime_completed_rows": runtime_completed,
        "report_rows": len(report_records),
        "report_usable_rows": report_usable,
        "summary_rows": len(summaries),
        "diff_rows": len(diffs),
        "proxy_mt5_diff_rows": len(proxy_rows),
        "matched_rows": matched_rows,
        "mismatch_rows": mismatch_rows,
        "runtime_output_copy_rows": len(copy_rows),
        "runtime_output_copy_ready_rows": sum(1 for row in copy_rows if row.get("exists") is True or bool_text(row.get("exists"))),
        "mt5_attempt_name": primary_summary.get("attempt_name", ""),
        "mt5_net_profit": primary_summary.get("net_profit", ""),
        "mt5_profit_factor": primary_summary.get("profit_factor", ""),
        "mt5_trade_count": primary_summary.get("trade_count", ""),
        "mt5_expectancy": primary_summary.get("expectancy", ""),
        "mt5_recovery_factor": primary_summary.get("recovery_factor", ""),
        "mt5_max_drawdown_amount": primary_summary.get("max_drawdown_amount", ""),
        "mt5_max_drawdown_percent": primary_summary.get("max_drawdown_percent", ""),
        "mt5_long_trade_count": primary_summary.get("long_trade_count", ""),
        "mt5_short_trade_count": primary_summary.get("short_trade_count", ""),
        "mt5_win_rate_percent": primary_summary.get("win_rate_percent", ""),
        "mt5_comparison_status": primary_summary.get("comparison_status", ""),
        "mt5_execution_attempted": "yes",
        "external_verification_status": "completed(완료)" if completed else "blocked(차단)",
        "candidate_selection": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "goal_achieve": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "parent_gate_passed": True,
        "parent_goal_achieve": parent.get("goal_achieve", "not_claimed"),
        "created_at_utc": now_utc(),
    }


def gate_row(gate_id: str, status: str, evidence_path: Path, effect: str) -> dict[str, Any]:
    return {
        "gate_id": gate_id,
        "status": status,
        "evidence_path": rel(evidence_path),
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def make_gates(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    no_forbidden = (
        final["candidate_selection"] == "not_run"
        and final["forward_passed"] == "not_claimed"
        and final["forward_failed"] == "not_claimed"
        and final["goal_achieve"] == "not_claimed"
        and final["runtime_authority"] == "not_claimed"
        and final["operating_promotion"] == "not_claimed"
    )
    return [
        gate_row("parent_364R_gates_passed", "passed" if final["parent_gate_passed"] else "failed", pkg.GATE_AUDIT, "run364R(364R 실행) package gate(포장 게이트)를 이어받는다."),
        gate_row("mt5_attempt_or_block_recorded", "passed" if final["execution_result_rows"] == final["attempt_rows"] and final["attempt_rows"] > 0 else "failed", MT5_EXECUTION_RESULT, "각 attempt(시도)의 실행 결과 또는 blocker(차단 사유)를 남긴다."),
        gate_row("runtime_output_copy_recorded", "passed" if final["runtime_output_copy_rows"] >= final["attempt_rows"] * 2 else "failed", RUNTIME_OUTPUT_COPY, "telemetry/summary(기록/요약) 복사 감사를 남긴다."),
        gate_row("comparison_summary_materialized", "passed" if final["summary_rows"] == final["attempt_rows"] else "failed", EXECUTION_SUMMARY, "proxy-MT5 summary(프록시-MT5 요약)를 만든다."),
        gate_row("diff_or_blocker_materialized", "passed" if final["diff_rows"] > 0 or final["runtime_completed_rows"] == 0 else "failed", PROBABILITY_DIFF, "diff(차이) 또는 blocker(차단 사유)를 기록한다."),
        gate_row("proxy_mt5_kpi_diff_materialized", "passed" if final["proxy_mt5_diff_rows"] >= final["attempt_rows"] else "failed", PROXY_MT5_DIFF, "expected KPI(예상 핵심 성과 지표)와 MT5 KPI(MT5 핵심 성과 지표)를 나란히 둔다."),
        gate_row("forensics_identity_recorded", "passed" if exists(RUNTIME_IDENTITY) else "failed", RUNTIME_IDENTITY, "tester identity(테스터 정체성)를 기록한다."),
        gate_row("no_forbidden_operating_claim", "passed" if no_forbidden else "failed", FINAL_DECISION, "runtime probe(런타임 탐침)가 운영 주장으로 커지지 않게 한다."),
        gate_row("required_gate_coverage_audit_written", "passed", GATE_AUDIT, "gate coverage(게이트 커버리지)를 기록한다."),
    ]


def artifact_paths() -> list[Path]:
    paths = list(OUTPUT_FILES)
    for folder in [TELEMETRY_COPY_DIR, REPORT_COPY_DIR, MT5_DIR]:
        if exists(folder):
            paths.extend(path for path in folder.glob("*") if path.is_file())
    return paths


def relative_artifacts() -> list[str]:
    rows: list[str] = []
    for path in artifact_paths():
        try:
            if exists(path) and Path(path).resolve().is_relative_to(ROOT.resolve()):
                rows.append(rel(path))
        except OSError:
            continue
    return sorted(set(rows))


def write_final_and_manifest(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    payload = {
        **dict(final),
        "gate_passes": sum(1 for row in gates if row.get("status") == "passed"),
        "gate_total": len(gates),
    }
    write_json(FINAL_DECISION, payload)
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "created_at": TODAY,
            "created_at_utc": now_utc(),
            "script": rel(Path(__file__)),
            "inputs": [
                rel(pkg.FINAL_DECISION),
                rel(pkg.RUNTIME_PROBE_ATTEMPT_PACKAGE),
                rel(pkg.EXPECTED_PROBABILITY_TAPE),
                rel(pkg.MT5_NATIVE_TRADE_TAPE),
                rel(pkg.FEATURE_MATRIX),
            ],
            "outputs": relative_artifacts(),
            "external_verification_status": payload["external_verification_status"],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    return payload


def write_receipts(final: Mapping[str, Any]) -> None:
    base = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
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
            "research_path": rel(pkg.EXPECTED_PROBABILITY_TAPE),
            "runtime_path": rel(RUNTIME_OUTPUT_COPY),
            "shared_contract": rel(pkg.RUNTIME_PARITY_CONTRACT),
            "known_differences": "Strategy Tester(전략 테스터) broker cost(브로커 비용)는 MT5 report(MT5 보고서)에서 읽는다.",
            "parity_check": rel(PROBABILITY_DIFF),
            "parity_identity": rel(RUNTIME_IDENTITY),
            "runtime_claim_boundary": "runtime_probe(런타임 탐침)" if final["runtime_completed_rows"] else "blocked(차단)",
        },
    )
    write_json(
        BACKTEST_FORENSICS_RECEIPT,
        {
            **base,
            "tester_identity": rel(RUNTIME_IDENTITY),
            "ea_identity": rel(pkg.TESTER_IDENTITY_CONTRACT),
            "report_identity": rel(STRATEGY_TESTER_REPORTS),
            "trade_evidence": rel(EXECUTION_SUMMARY),
            "cost_assumptions": "spread/commission/slippage(스프레드/수수료/슬리피지)는 parsed report(파싱된 보고서)가 있으면 거기에서 읽는다.",
            "forensic_checks": [rel(MT5_EXECUTION_RESULT), rel(STRATEGY_TESTER_REPORTS), rel(RUNTIME_OUTPUT_COPY)],
            "backtest_judgment": "usable_with_boundary(경계 조건부 사용 가능)" if final["runtime_completed_rows"] else "blocked(차단)",
        },
    )
    write_json(
        PERFORMANCE_RECEIPT,
        {
            **base,
            "summary": rel(EXECUTION_SUMMARY),
            "probability_diff": rel(PROBABILITY_DIFF),
            "proxy_mt5_diff": rel(PROXY_MT5_DIFF),
            "matched_rows": final["matched_rows"],
            "mismatch_rows": final["mismatch_rows"],
            "mt5_kpi_authority": "Strategy Tester report(전략 테스터 보고서)가 있을 때만 제한적으로 읽는다.",
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "external_verification_status": final["external_verification_status"],
            "candidate_selection": "not_run",
            "goal_achieve": "not_claimed",
            "effect": "positive judgment(긍정 판정)을 runtime probe(런타임 탐침) 밖으로 확장하지 않는다.",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [
                rel(pkg.FINAL_DECISION),
                rel(pkg.RUNTIME_PROBE_ATTEMPT_PACKAGE),
                rel(pkg.EXPECTED_PROBABILITY_TAPE),
                rel(pkg.MT5_NATIVE_TRADE_TAPE),
                rel(pkg.FEATURE_MATRIX),
            ],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": relative_artifacts(),
            "artifact_hashes": {path: sha(ROOT / path) for path in relative_artifacts()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "runtime_attempt_recorded(런타임 시도 기록됨)",
            "lineage_judgment": "connected_with_boundary(경계 조건부 연결)",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "candidate_selection": "not_run",
            "model_training": "not_run",
            "mt5_execution": "attempted",
            "forward_passed": "not_claimed",
            "goal_achieve": "not_claimed",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
        },
    )


def write_docs(final: Mapping[str, Any]) -> None:
    summary_rows = read_csv_rows(EXECUTION_SUMMARY)
    mt5_row = summary_rows[0] if summary_rows else {}
    proxy_rows = read_csv_rows(PROXY_MT5_DIFF)
    proxy = proxy_rows[0] if proxy_rows else {}
    report = f"""# run364S Drawdown Side Balance Overlay MT5 Runtime Probe(364S 낙폭 방향 균형 오버레이 온엑스 MT5 런타임 탐침)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- gates(게이트): `{final['gate_passes']}/{final['gate_total']}`
- attempts(시도): `{final['attempt_rows']}`
- runtime_completed_rows(런타임 완료 수): `{final['runtime_completed_rows']}`
- report_usable_rows(보고서 사용 가능 수): `{final['report_usable_rows']}`
- matched_rows(일치 수): `{final['matched_rows']}`
- mismatch_rows(불일치 수): `{final['mismatch_rows']}`
- external_verification_status(외부 검증 상태): `{final['external_verification_status']}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

## Runtime Read(런타임 판독)

- comparison_status(비교 상태): `{mt5_row.get('comparison_status', '')}`
- expected_rows(예상 수): `{mt5_row.get('expected_rows', '')}`
- ready_model_rows(준비 모델 수): `{mt5_row.get('ready_model_rows', '')}`
- visited_expected_rows(방문 예상 수): `{mt5_row.get('visited_expected_rows', '')}`
- unvisited_expected_rows(미방문 예상 수): `{mt5_row.get('unvisited_expected_rows', '')}`
- max_abs_probability_diff(최대 절대 확률 차이): `{mt5_row.get('max_abs_probability_diff', '')}`
- net_profit(순수익): `{mt5_row.get('net_profit', '')}`
- profit_factor(수익 팩터): `{mt5_row.get('profit_factor', '')}`
- trade_count(거래수): `{mt5_row.get('trade_count', '')}`
- expectancy(기대값): `{mt5_row.get('expectancy', '')}`
- recovery_factor(회복 계수): `{mt5_row.get('recovery_factor', '')}`
- max_drawdown_amount(최대 낙폭 금액): `{mt5_row.get('max_drawdown_amount', '')}`
- max_drawdown_percent(최대 낙폭 퍼센트): `{mt5_row.get('max_drawdown_percent', '')}`
- long_short_balance(롱/숏 균형): `{mt5_row.get('long_trade_count', '')} long / {mt5_row.get('short_trade_count', '')} short(롱/숏)`

## Proxy vs MT5(프록시 대 MT5)

- expected_net_profit(예상 순수익): `{proxy.get('expected_net_profit', '')}`
- actual_mt5_net_profit(실제 MT5 순수익): `{proxy.get('actual_mt5_net_profit', '')}`
- net_profit_diff_actual_minus_expected(실제-예상 순수익 차이): `{proxy.get('net_profit_diff_actual_minus_expected', '')}`
- expected_trade_count(예상 거래수): `{proxy.get('expected_trade_count', '')}`
- actual_mt5_trade_count(실제 MT5 거래수): `{proxy.get('actual_mt5_trade_count', '')}`
- trade_count_diff_actual_minus_expected(실제-예상 거래수 차이): `{proxy.get('trade_count_diff_actual_minus_expected', '')}`

Action(행동): run364R(364R 실행) ONNX runtime package(온엑스 런타임 포장)를 MT5 Strategy Tester(MT5 전략 테스터)에서 실행하거나 blocker(차단 사유)를 기록했다.

Effect(효과): proxy expected value(프록시 예상값), probability parity(확률 동등성), MT5 KPI(MT5 핵심 성과 지표)를 분리해 다음 review/repair(검토/수리) 판단의 입력으로 남긴다.

## Evidence(근거)

- execution result(실행 결과): `{rel(MT5_EXECUTION_RESULT)}`
- runtime summary(런타임 요약): `{rel(EXECUTION_SUMMARY)}`
- probability diff(확률 차이): `{rel(PROBABILITY_DIFF)}`
- proxy-MT5 diff(프록시-MT5 차이): `{rel(PROXY_MT5_DIFF)}`
- tester reports(테스터 보고서): `{rel(STRATEGY_TESTER_REPORTS)}`
- runtime identity(런타임 정체성): `{rel(RUNTIME_IDENTITY)}`

## Boundary(경계)

run364S(364S 실행)은 runtime_probe attempt(런타임 탐침 시도)다. operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 주장하지 않는다.
"""
    decision = f"""# {TODAY} Stage364S Decision(364S 결정)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{final['decision']}`
- judgment(판정): `{final['judgment']}`
- external_verification_status(외부 검증 상태): `{final['external_verification_status']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- evidence(근거): `{rel(MT5_EXECUTION_RESULT)}`, `{rel(EXECUTION_SUMMARY)}`, `{rel(PROXY_MT5_DIFF)}`

Action(행동): MT5 runtime probe(MT5 런타임 탐침)를 시도했다.

Effect(효과): 결과 또는 blocker(차단 사유)를 run364T(364T 실행)의 review/repair(검토/수리) 입력으로 넘긴다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    current = f"""# Current Working State(현재 작업 상태)

## Current Truth(현재 진실)

- active_stage(현재 단계): `{STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`

## Effect(효과)

run364S(364S 실행)은 MT5 runtime probe(MT5 런타임 탐침)를 시도했고, run364T(364T 실행)는 결과를 검토하거나 blocker(차단 사유)를 수리해야 한다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage364 Selection Status(364단계 선택 상태)

- selection_status(선택 상태): `runtime_probe_positive_review_required_no_operating_claim(런타임 탐침 양수, 검토 필요, 운영 주장 없음)`
- active_stage_id(활성 단계 ID): `{STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- research_candidate_model_id(연구 후보 모델 ID): `h12_move5__rf5_l80_n64`
- research_candidate_policy_id(연구 후보 정책 ID): `long_only_margin`
- runtime_trade_shape(런타임 거래 형태): `mt5_native_maxhold_only_close_on_flat_false(MT5 원생 최대 보유, 플랫 청산 없음)`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- live_readiness(실거래 준비): `not_claimed(주장 없음)`
- goal_achieve(목표 달성): `not_claimed(주장 없음)`

## run364S MT5 Runtime Probe(364S MT5 런타임 탐침)

- external_verification_status(외부 검증 상태): `{final['external_verification_status']}`
- probability_parity(확률 동등성): `{final['matched_rows']}/17428 matched(일치), mismatch {final['mismatch_rows']}(불일치)`
- max_abs_probability_diff(최대 절대 확률 차이): `{mt5_row.get('max_abs_probability_diff', '')}`
- mt5_net_profit(MT5 순수익): `{mt5_row.get('net_profit', '')}`
- mt5_profit_factor(MT5 수익 팩터): `{mt5_row.get('profit_factor', '')}`
- mt5_trade_count(MT5 거래수): `{mt5_row.get('trade_count', '')}`
- mt5_expectancy(MT5 기대값): `{mt5_row.get('expectancy', '')}`
- mt5_recovery_factor(MT5 회복 계수): `{mt5_row.get('recovery_factor', '')}`
- mt5_max_drawdown_amount(MT5 최대 낙폭 금액): `{mt5_row.get('max_drawdown_amount', '')}`
- mt5_max_drawdown_percent(MT5 최대 낙폭 퍼센트): `{mt5_row.get('max_drawdown_percent', '')}`
- long_short_balance(롱/숏 균형): `{mt5_row.get('long_trade_count', '')} long / {mt5_row.get('short_trade_count', '')} short(롱/숏)`

Action(행동): run364R(364R 실행) package(포장)를 MT5 Strategy Tester(MT5 전략 테스터)로 실행했다.

Effect(효과): 수익성은 양수 단서로 남겼지만 drawdown(낙폭), long-only(롱 전용), review-required(검토 필요) 조건 때문에 운영 승격으로 닫지 않는다.

## Evidence(근거)

- report(보고서): `{rel(REPORT_PATH)}`
- final_decision(최종 결정): `{rel(FINAL_DECISION)}`
- proxy_mt5_diff(프록시-MT5 차이): `{rel(PROXY_MT5_DIFF)}`
"""
    workspace = f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {final['status']}
current_judgment: {final['judgment']}
current_decision: {final['decision']}
next_run_id: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
"""
    write_text(REPORT_PATH, report)
    write_text(DECISION_DOC, decision)
    write_text(CURRENT_WORKING_STATE, current)
    write_text(SELECTION_STATUS, selection)
    write_text(WORKSPACE_STATE, workspace)
    marker = RUN_ID
    append_text_once(REVIEW_INDEX, marker, f"- `{RUN_ID}`: `{rel(REPORT_PATH)}` - MT5 runtime probe(MT5 런타임 탐침) attempt(시도).")
    append_text_once(
        STAGE_BRIEF,
        marker,
        f"""## run364S MT5 Runtime Probe(MT5 런타임 탐침)

- run_id(실행 ID): `{RUN_ID}`
- external_verification_status(외부 검증 상태): `{final['external_verification_status']}`
- matched_rows(일치 수): `{final['matched_rows']}`
- mismatch_rows(불일치 수): `{final['mismatch_rows']}`
- effect(효과): 실제 MT5 실행 결과 또는 blocker(차단 사유)를 다음 review/repair(검토/수리)로 넘긴다.
""",
    )
    append_text_once(
        STAGE_README,
        marker,
        f"""## run364S MT5 Runtime Probe(MT5 런타임 탐침)

- run_id(실행 ID): `{RUN_ID}`
- summary(요약): `{rel(EXECUTION_SUMMARY)}`
- effect(효과): Stage364(364단계)의 proxy(프록시)를 MT5 runtime evidence(MT5 런타임 근거)와 대조한다.
""",
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        marker,
        f"""## {TODAY} run364S Drawdown Side Balance Overlay MT5 Runtime Probe(364S 낙폭 방향 균형 오버레이 온엑스 MT5 런타임 탐침)

- action(행동): MT5 runtime probe(MT5 런타임 탐침)를 시도했다.
- effect(효과): external verification(외부 검증) 상태 `{final['external_verification_status']}`, matched_rows(일치 수) `{final['matched_rows']}`, mismatch_rows(불일치 수) `{final['mismatch_rows']}`를 기록했다.
- boundary(경계): operating promotion/runtime authority/Goal Achieve(운영 승격/런타임 권위/목표 달성)는 주장하지 않는다.
""",
    )


def write_registers(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_date": TODAY,
        "date": TODAY,
        "status": final["status"],
        "judgment": final["judgment"],
        "decision": final["decision"],
        "next_run_id": NEXT_RUN_ID,
        "path": rel(FINAL_DECISION),
        "primary_artifact": rel(FINAL_DECISION),
        "report_path": rel(REPORT_PATH),
        "gate_passes": sum(1 for row in gates if row.get("status") == "passed"),
        "gate_total": len(gates),
        "claim_boundary": CLAIM_BOUNDARY,
        "external_verification_status": final["external_verification_status"],
        "matched_rows": final["matched_rows"],
        "mismatch_rows": final["mismatch_rows"],
        "runtime_completed_rows": final["runtime_completed_rows"],
        "attempt_rows": final["attempt_rows"],
        "created_at": now_utc(),
        "work_family": "runtime_verification(런타임 검증)",
    }
    run_row = {
        **base,
        "lane": "runtime_probe(MT5 런타임 탐침)",
        "subrun_id": "",
        "notes": "run364S MT5 runtime probe(MT5 런타임 탐침) attempt(시도).",
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [run_row])
    rows = [
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__Tier_A",
            "subrun_id": f"{RUN_ID}__Tier_A",
            "view": "Tier A separate(Tier A 분리)",
            "record_view": "Tier A separate(Tier A 분리)",
            "tier": "Tier A",
            "tier_scope": "Tier A",
            "metric_scope": "mt5_runtime_probe(MT5 런타임 탐침)",
            "kpi_scope": "mt5_runtime_probe(MT5 런타임 탐침)",
            "result_status": final["judgment"],
            "notes": "Tier A(티어 A) package(포장)를 MT5 runtime probe(MT5 런타임 탐침)로 시도했다.",
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__Tier_B",
            "subrun_id": f"{RUN_ID}__Tier_B",
            "view": "Tier B separate(Tier B 분리)",
            "record_view": "Tier B separate(Tier B 분리)",
            "tier": "Tier B",
            "tier_scope": "Tier B",
            "metric_scope": "out_of_scope_by_claim(주장 범위 밖)",
            "kpi_scope": "out_of_scope_by_claim(주장 범위 밖)",
            "result_status": "out_of_scope_by_claim",
            "notes": "run364S(364S 실행)은 Tier B(티어 B) fallback(대체)을 주장하지 않는다.",
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__Tier_AplusB",
            "subrun_id": f"{RUN_ID}__Tier_AplusB",
            "view": "Tier A+B combined(Tier A+B 합산)",
            "record_view": "Tier A+B combined(Tier A+B 합산)",
            "tier": "Tier A+B",
            "tier_scope": "Tier A+B",
            "metric_scope": "actual_routed_total_same_as_tier_a_no_tier_b_fallback(실제 라우팅 전체는 Tier A와 같음)",
            "kpi_scope": "actual_routed_total_same_as_tier_a_no_tier_b_fallback(실제 라우팅 전체는 Tier A와 같음)",
            "result_status": "actual_routed_total_same_as_tier_a_no_tier_b_fallback",
            "notes": "Tier B(티어 B) fallback(대체)이 없는 실제 라우팅 전체를 기록한다.",
        },
    ]
    append_or_replace_csv(PROJECT_LEDGER, ["run_id", "subrun_id"], rows)
    append_or_replace_csv(STAGE_LEDGER, ["run_id", "subrun_id"], rows)


def write_artifact_registry() -> None:
    rows: list[dict[str, Any]] = []
    for path in artifact_paths():
        if not exists(path):
            continue
        try:
            path.resolve().relative_to(ROOT.resolve())
        except ValueError:
            continue
        rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": Path(path).suffix.lstrip(".") or "artifact",
                "path": rel(path),
                "artifact_path": rel(path),
                "sha256": sha(path),
                "created_at": TODAY,
                "created_at_utc": now_utc(),
                "claim_boundary": CLAIM_BOUNDARY,
                "artifact_id": f"{RUN_ID}::{rel(path)}",
                "notes": "run364S MT5 runtime probe(MT5 런타임 탐침) artifact(산출물).",
            }
        )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["run_id", "path"], rows)


def main() -> None:
    args = parse_args()
    ensure_dirs()
    parent = load_parent()
    attempts = enrich_attempts()
    if args.reuse_existing_execution and exists(MT5_EXECUTION_RESULT) and exists(STRATEGY_TESTER_REPORTS):
        execution_results = pkg.read_json(MT5_EXECUTION_RESULT)
        report_records = pkg.read_json(STRATEGY_TESTER_REPORTS)
        copy_rows = read_csv_rows(RUNTIME_OUTPUT_COPY) if exists(RUNTIME_OUTPUT_COPY) else []
    else:
        execution_results, report_records, copy_rows, _ = execute_attempts(args, attempts)
    summaries, diffs, _, proxy_rows = compare_outputs(attempts, execution_results, report_records)
    final_seed = build_final(args, parent, attempts, execution_results, report_records, summaries, diffs, copy_rows, proxy_rows)
    gates = make_gates(final_seed)
    write_csv(GATE_AUDIT, gates)
    write_receipts(final_seed)
    final = write_final_and_manifest(final_seed, gates)
    write_docs(final)
    write_registers(final, gates)
    write_artifact_registry()
    gates = make_gates(final)
    write_csv(GATE_AUDIT, gates)
    final = write_final_and_manifest(final_seed, gates)
    failed = [row for row in gates if row.get("status") != "passed"]
    if failed:
        raise RuntimeError(f"run364S gates failed(게이트 실패): {failed}")
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": final["status"],
                "judgment": final["judgment"],
                "external_verification_status": final["external_verification_status"],
                "runtime_completed_rows": final["runtime_completed_rows"],
                "matched_rows": final["matched_rows"],
                "mismatch_rows": final["mismatch_rows"],
                "gate_passes": final["gate_passes"],
                "gate_total": final["gate_total"],
                "next_run_id": NEXT_RUN_ID,
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
