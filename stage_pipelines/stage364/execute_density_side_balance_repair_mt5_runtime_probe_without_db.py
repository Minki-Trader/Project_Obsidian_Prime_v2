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
from stage_pipelines.stage364 import package_density_side_balance_repair_runtime_probe_without_db as pkg  # noqa: E402


TODAY = "2026-06-02"
STAGE_ID = pkg.STAGE_ID
RUN_NUMBER = "run364X"
RUN_ID = "run364X_execute_density_side_balance_repair_mt5_runtime_probe_without_db_v1"
PARENT_RUN_ID = pkg.RUN_ID
NEXT_RUN_ID = "run364Y_review_density_side_balance_repair_mt5_runtime_probe_without_db_v1"

STATUS_COMPLETED = "completed_stage364X_density_side_balance_repair_mt5_runtime_probe_executed_review_required_no_authority"
STATUS_BLOCKED = "blocked_stage364X_density_side_balance_repair_mt5_runtime_probe_attempt_recorded_repair_required_no_authority"
JUDGMENT_COMPLETED = "mt5_runtime_probe_outputs_available_proxy_diff_review_required_no_authority"
JUDGMENT_BLOCKED = "mt5_runtime_probe_attempt_recorded_outputs_missing_or_failed_repair_required_no_authority"
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
EXECUTION_SUMMARY = RUN_DIR / "density_side_balance_repair_mt5_probe_summary.csv"
PROBABILITY_DIFF = RUN_DIR / "probability_runtime_difference.csv"
PROXY_MT5_DIFF = RUN_DIR / "proxy_mt5_runtime_difference.csv"
TELEMETRY_SKIP_SUMMARY = RUN_DIR / "runtime_skip_reason_summary.csv"
RUNTIME_OUTPUT_COPY = RUN_DIR / "runtime_output_copy_manifest.csv"
RUNTIME_IDENTITY = RUN_DIR / "runtime_identity.csv"
EXPECTED_KPI_SUMMARY = RUN_DIR / "expected_kpi_summary.csv"
BACKTEST_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364X_density_side_balance_repair_mt5_runtime_probe.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364X_density_side_balance_repair_mt5_runtime_probe.md"
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
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"

INPUT_FILES = [
    pkg.FINAL_DECISION,
    pkg.GATE_AUDIT,
    pkg.RUNTIME_PROBE_ATTEMPT_PACKAGE,
    pkg.TESTER_SET_MANIFEST,
    pkg.TESTER_INI_MANIFEST,
    pkg.RUNTIME_POLICY_CONFIG,
    pkg.COMMON_FILES_SYNC,
    pkg.scout.SELECTED_PROBABILITY_TAPE,
    pkg.scout.SELECTED_TRADE_TAPE,
    pkg.SOURCE_FEATURE_MATRIX,
    pkg.SOURCE_ONNX,
    pkg.PORTABLE_EA_EX5,
]

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
    BACKTEST_RECEIPT,
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
    IDEA_REGISTRY,
    Path(__file__),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stage364X density side-balance MT5 runtime probe.")
    parser.add_argument("--terminal-path", default=str(pkg.basepkg.DEFAULT_TERMINAL))
    parser.add_argument("--common-files-root", default=str(pkg.basepkg.DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(pkg.basepkg.DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-data-root", default=str(pkg.basepkg.DEFAULT_PORTABLE_ROOT))
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


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Mapping[str, Any]]) -> None:
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
        return rel(value)
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


def finite(value: Any, digits: int = 10) -> float | str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return ""
    if not math.isfinite(number):
        return ""
    return round(number, digits)


def float_or_nan(value: Any) -> float:
    try:
        if value in ("", None):
            return math.nan
        return float(value)
    except (TypeError, ValueError):
        return math.nan


def ensure_dirs() -> None:
    for path in [RUN_DIR, MT5_DIR, TELEMETRY_COPY_DIR, REPORT_COPY_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR]:
        os.makedirs(fs_path(path), exist_ok=True)


def validate_parent() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing run364X inputs(364X 입력 누락): " + ", ".join(missing))
    parent = pkg.read_json(pkg.FINAL_DECISION)
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"run364W next_run_id mismatch(다음 실행 ID 불일치): {parent.get('next_run_id')} != {RUN_ID}")
    _, gates = pkg.read_csv_rows(pkg.GATE_AUDIT)
    if not gates or any(row.get("status") != "passed" for row in gates):
        raise RuntimeError("run364W gate audit(게이트 감사)가 모두 passed(통과)가 아니다.")
    if parent.get("compile_status") != "completed" or parent.get("portable_ea_copied") is not True:
        raise RuntimeError("run364W compile/sync(컴파일/동기화)가 runtime probe(런타임 탐침)에 충분하지 않다.")
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
        "effect": "terminal64.exe process(터미널 프로세스) 충돌을 먼저 확인해 기존 세션 손상을 줄인다.",
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
        attempt["feature_set_id"] = "stage364W_density_side_balance_repair_features"
        attempt["ini_name"] = ini_path.name
        attempt["set_name"] = set_path.name
        attempt["common_telemetry_path"] = str(attempt.get("runtime_telemetry_expected", ""))
        attempt["common_summary_path"] = str(attempt.get("runtime_summary_expected", ""))
        attempt["ini"] = {"tester": {"Report": attempt.get("report_name", "")}}
        attempt["set"] = {"path": attempt.get("set_path", "")}
        attempt["execution_run_id"] = RUN_ID
        attempt["parent_package_run_id"] = PARENT_RUN_ID
        attempt["effect"] = "run364W package(패키지)를 실제 MT5 runtime probe(MT5 런타임 탐침) 입력으로 고정한다."
        enriched.append(attempt)
    if not enriched:
        raise RuntimeError("runtime_probe_attempt_package(런타임 탐침 시도 패키지)가 비어 있다.")
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


def copy_runtime_outputs(common_files_root: Path, attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for attempt in attempts:
        attempt_name = str(attempt["attempt_name"])
        for key, suffix in [("common_telemetry_path", "telemetry"), ("common_summary_path", "summary")]:
            source = common_files_root / Path(str(attempt.get(key, "")))
            target = TELEMETRY_COPY_DIR / f"{attempt_name}_{suffix}.csv"
            source_exists = exists(source)
            copied = False
            if source_exists:
                os.makedirs(fs_path(target.parent), exist_ok=True)
                shutil.copy2(fs_path(source), fs_path(target))
                copied = True
            rows.append(
                {
                    "copy_id": f"{attempt_name}::{suffix}",
                    "attempt_name": attempt_name,
                    "source_path": source.as_posix(),
                    "target_path": rel(target),
                    "source_exists": source_exists,
                    "copied": copied,
                    "exists": exists(target),
                    "sha256": sha(target) if exists(target) else "",
                    "effect": "runtime telemetry(런타임 기록)를 run folder(실행 폴더)에 고정해 비교 근거를 남긴다.",
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
                    "status": "blocked",
                    "blocker": "target_portable_terminal_already_running",
                    "runtime_outputs": {"status": "blocked", "wait_status": "skipped_terminal_already_running"},
                    "ini_path": attempt.get("ini_path", ""),
                    "set_path": attempt.get("set_path", ""),
                    "effect": "이미 실행 중인 terminal64.exe(터미널 프로세스)를 건드리지 않아 세션 손상을 줄인다.",
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

    copy_rows = copy_runtime_outputs(common_files_root, attempts)
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


def decision_label(value: Any) -> str:
    text = str(value or "").strip().lower()
    if text in {"1", "long", "buy"}:
        return "long"
    if text in {"-1", "short", "sell"}:
        return "short"
    if text in {"0", "flat", "no_trade", "hold", ""}:
        return "flat"
    return text


def bool_text(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes"}


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
    frame = pd.read_csv(fs_path(pkg.scout.SELECTED_PROBABILITY_TAPE)).fillna("")
    rows: dict[str, dict[str, Any]] = {}
    duplicates = 0
    feature_hashes, feature_duplicates = feature_line_hash_map(pkg.SOURCE_FEATURE_MATRIX)
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
        "variant_id": attempt.get("variant_id", ""),
        "feature_set_id": attempt.get("feature_set_id", ""),
        "tester_status": execution_row.get("status", "not_attempted"),
        "runtime_status": runtime.get("status", "missing"),
        "report_status": report_row.get("status", "missing") if report_row else "missing",
        "returncode": execution_row.get("returncode", ""),
        "blocker": execution_row.get("blocker", ""),
        "expected_rows": len(expected),
        "expected_duplicate_or_feature_duplicate_rows": expected_duplicates,
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
    cycles = frame[frame["record_type"].astype(str).str.lower() == "cycle"].copy() if "record_type" in frame.columns else frame.copy()
    feature_ready = cycles.get("feature_ready", pd.Series([False] * len(cycles))).map(bool_text)
    model_ok = cycles.get("model_ok", pd.Series([False] * len(cycles))).map(bool_text)
    ready = cycles[feature_ready & model_ok].copy()
    skipped = cycles[~(feature_ready & model_ok)].copy()
    if not skipped.empty and "skip_reason" in skipped.columns:
        for reason, count in skipped["skip_reason"].astype(str).replace("", "empty").value_counts().sort_index().items():
            skip_rows.append(
                {
                    "attempt_name": attempt["attempt_name"],
                    "model_id": attempt.get("model_id", ""),
                    "skip_reason": reason,
                    "rows": int(count),
                    "effect": "skip reason(건너뜀 사유)은 tester/date/model handoff(테스터/날짜/모델 인계) 공백 위치를 보여준다.",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )

    matched = expected_missing = hash_mismatch = prob_mismatch = decision_mismatch = 0
    max_prob_diff = 0.0
    ready_times: list[str] = []
    tolerance = 1e-4
    for _, row in ready.iterrows():
        source_time = norm_bar_time(row.get("source_time") or row.get("bar_time"))
        ready_times.append(source_time)
        exp = expected.get(source_time)
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
                "source_time": source_time,
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
    visited_expected_rows = len(ready_time_set & expected_time_set)
    unvisited_expected_rows = max(0, len(expected_time_set) - visited_expected_rows)
    latest_expected = max(expected_time_set) if expected_time_set else ""
    feature_last_reached = latest_expected in ready_time_set
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
    rows = read_csv_rows(pkg.EXPECTED_KPI_SUMMARY)
    out = []
    for row in rows:
        payload = dict(row)
        payload["metric_id"] = f"expected_proxy_{payload.get('split', '')}"
        out.append(payload)
    write_csv(EXPECTED_KPI_SUMMARY, out)
    return out


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
    expected_combined = next((row for row in expected_metrics if row.get("split") == "combined"), {})
    summaries_by_attempt = {row.get("attempt_name"): row for row in summaries}
    rows: list[dict[str, Any]] = []
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
                "expected_net_profit": expected_combined.get("net_profit", ""),
                "actual_mt5_net_profit": actual.get("net_profit", ""),
                "net_profit_diff_actual_minus_expected": finite(actual_net - expected_net) if math.isfinite(actual_net) and math.isfinite(expected_net) else "",
                "expected_trade_count": expected_combined.get("trade_count", ""),
                "actual_mt5_trade_count": actual.get("trade_count", ""),
                "trade_count_diff_actual_minus_expected": finite(actual_trades - expected_trades) if math.isfinite(actual_trades) and math.isfinite(expected_trades) else "",
                "expected_profit_factor": expected_combined.get("profit_factor", ""),
                "actual_mt5_profit_factor": actual.get("profit_factor", ""),
                "expected_long_count": expected_combined.get("long_trade_count", ""),
                "actual_long_count": actual.get("long_trade_count", ""),
                "expected_short_count": expected_combined.get("short_trade_count", ""),
                "actual_short_count": actual.get("short_trade_count", ""),
                "report_status": actual.get("report_status", ""),
                "comparison_status": actual.get("comparison_status", ""),
                "known_attribution": "proxy(프록시)는 신호 보조이며 MT5 Strategy Tester(MT5 전략 테스터)의 broker cost/runtime semantics(브로커 비용/런타임 의미)를 대체하지 않는다.",
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
    completed_runtime = sum(1 for row in summaries if row.get("runtime_status") == "completed")
    usable_reports = report_usable_count(report_records)
    total_mismatches = sum(int(row.get("hash_mismatch_rows") or 0) + int(row.get("probability_mismatch_rows") or 0) + int(row.get("decision_mismatch_rows") or 0) for row in summaries)
    total_ready = sum(int(row.get("ready_model_rows") or 0) for row in summaries)
    total_matched = sum(int(row.get("matched_rows") or 0) for row in summaries)
    status = STATUS_COMPLETED if completed_runtime > 0 else STATUS_BLOCKED
    judgment = JUDGMENT_COMPLETED if completed_runtime > 0 else JUDGMENT_BLOCKED
    summary = summaries[0] if summaries else {}
    proxy = proxy_rows[0] if proxy_rows else {}
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "stage_id": STAGE_ID,
        "status": status,
        "judgment": judgment,
        "decision": "stage364X_open_run364Y_review_density_side_balance_repair_mt5_runtime_probe_without_db_v1",
        "created_at_utc": now_utc(),
        "claim_boundary": CLAIM_BOUNDARY,
        "attempt_count": len(attempts),
        "runtime_completed_rows": completed_runtime,
        "usable_report_rows": usable_reports,
        "ready_model_rows": total_ready,
        "matched_rows": total_matched,
        "mismatch_rows": total_mismatches,
        "probability_diff_rows": len(diffs),
        "runtime_output_copy_rows": len(copy_rows),
        "terminal_path": str(args.terminal_path),
        "common_files_root": str(args.common_files_root),
        "tester_profile_root": str(args.tester_profile_root),
        "terminal_data_root": str(args.terminal_data_root),
        "selected_variant_id": parent.get("selected_variant_id"),
        "expected_net_profit": proxy.get("expected_net_profit", parent.get("expected_combined_net_profit")),
        "actual_mt5_net_profit": proxy.get("actual_mt5_net_profit", summary.get("net_profit", "")),
        "net_profit_diff_actual_minus_expected": proxy.get("net_profit_diff_actual_minus_expected", ""),
        "expected_trade_count": proxy.get("expected_trade_count", parent.get("expected_combined_trade_count")),
        "actual_mt5_trade_count": proxy.get("actual_mt5_trade_count", summary.get("trade_count", "")),
        "trade_count_diff_actual_minus_expected": proxy.get("trade_count_diff_actual_minus_expected", ""),
        "actual_mt5_profit_factor": proxy.get("actual_mt5_profit_factor", summary.get("profit_factor", "")),
        "actual_long_trade_count": proxy.get("actual_long_count", summary.get("long_trade_count", "")),
        "actual_short_trade_count": proxy.get("actual_short_count", summary.get("short_trade_count", "")),
        "report_path": summary.get("report_path", ""),
        "comparison_status": summary.get("comparison_status", ""),
        "mt5_execution": "attempted",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "live_readiness": "not_claimed",
    }


def gate_rows(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    runtime_ok = int(final.get("runtime_completed_rows") or 0) > 0
    report_ok = int(final.get("usable_report_rows") or 0) > 0
    return [
        {
            "run_id": RUN_ID,
            "gate(게이트)": "tester_execution_attempt_gate(테스터 실행 시도 게이트)",
            "status": "passed",
            "evidence(근거)": rel(MT5_EXECUTION_RESULT),
            "effect(효과)": "MT5 Strategy Tester(MT5 전략 테스터) 실행 시도를 기록한다.",
        },
        {
            "run_id": RUN_ID,
            "gate(게이트)": "runtime_output_gate(런타임 출력 게이트)",
            "status": "passed" if runtime_ok else "blocked",
            "evidence(근거)": rel(RUNTIME_OUTPUT_COPY),
            "effect(효과)": "runtime telemetry/summary(런타임 기록/요약) 존재를 확인한다.",
        },
        {
            "run_id": RUN_ID,
            "gate(게이트)": "strategy_report_gate(전략 테스터 보고서 게이트)",
            "status": "passed" if report_ok else "blocked",
            "evidence(근거)": rel(STRATEGY_TESTER_REPORTS),
            "effect(효과)": "tester KPI(테스터 핵심 성과 지표)의 출처를 고정한다.",
        },
        {
            "run_id": RUN_ID,
            "gate(게이트)": "proxy_mt5_diff_gate(프록시-MT5 차이 게이트)",
            "status": "passed" if runtime_ok else "blocked",
            "evidence(근거)": rel(PROXY_MT5_DIFF),
            "effect(효과)": "proxy expected value(프록시 예상값)와 MT5 KPI(MT5 핵심 성과 지표)를 분리한다.",
        },
        {
            "run_id": RUN_ID,
            "gate(게이트)": "runtime_parity_audit(런타임 동등성 감사)",
            "status": "passed" if runtime_ok else "blocked",
            "evidence(근거)": rel(PROBABILITY_DIFF),
            "effect(효과)": "probability/decision parity(확률/판정 동등성) 차이를 측정한다.",
        },
        {
            "run_id": RUN_ID,
            "gate(게이트)": "claim_boundary_audit(주장 경계 감사)",
            "status": "passed",
            "evidence(근거)": rel(CLAIM_RECEIPT),
            "effect(효과)": "runtime probe(런타임 탐침)를 runtime authority(런타임 권위)로 승격하지 않는다.",
        },
        {
            "run_id": RUN_ID,
            "gate(게이트)": "required_gate_coverage_audit(필수 게이트 커버리지 감사)",
            "status": "passed" if runtime_ok and report_ok else "blocked",
            "evidence(근거)": rel(GATE_AUDIT),
            "effect(효과)": "필수 gate(게이트)를 closeout(종료 기록)에 연결한다.",
        },
    ]


def write_receipts(final: Mapping[str, Any]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(
        BACKTEST_RECEIPT,
        {
            **base,
            "tester_identity": rel(pkg.TESTER_IDENTITY_CONTRACT),
            "ea_identity": pkg.mt5_runtime_module_hashes(),
            "report_identity": rel(STRATEGY_TESTER_REPORTS),
            "trade_evidence": rel(EXECUTION_SUMMARY),
            "cost_assumptions": "broker-native tester output(브로커 네이티브 테스터 출력)에서 확인한다.",
            "forensic_checks": [rel(MT5_EXECUTION_RESULT), rel(STRATEGY_TESTER_REPORTS), rel(RUNTIME_OUTPUT_COPY)],
            "backtest_judgment": "usable_with_boundary(경계 포함 사용 가능)" if int(final.get("usable_report_rows") or 0) else "blocked_or_inconclusive(차단 또는 불충분)",
        },
    )
    write_json(
        RUNTIME_RECEIPT,
        {
            **base,
            "research_path": rel(pkg.scout.FINAL_DECISION),
            "runtime_path": rel(pkg.RUNTIME_PROBE_ATTEMPT_PACKAGE),
            "shared_contract": rel(pkg.RUNTIME_PARITY_CONTRACT),
            "known_differences": "MT5 tester(테스터) 비용/체결 의미는 proxy(프록시)와 다를 수 있다.",
            "parity_check": rel(PROBABILITY_DIFF),
            "runtime_claim_boundary": "runtime_probe(런타임 탐침), not authority(권위 아님)",
        },
    )
    write_json(
        PERFORMANCE_RECEIPT,
        {
            **base,
            "expected_vs_actual": rel(PROXY_MT5_DIFF),
            "attribution_scope": "proxy-vs-MT5 first pass(프록시-MT5 1차 비교)",
            "judgment": final["judgment"],
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "result_subject": RUN_ID,
            "evidence_available": [rel(EXECUTION_SUMMARY), rel(PROXY_MT5_DIFF), rel(PROBABILITY_DIFF)],
            "judgment_label": final["judgment"],
            "next_condition": NEXT_RUN_ID,
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and Path(path).is_file()},
            "lineage_judgment": "connected_with_boundary(경계 포함 연결됨)",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "mt5_execution": "attempted",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "goal_achieve": "not_claimed",
            "effect": "MT5 runtime probe(MT5 런타임 탐침)를 operating claim(운영 주장)으로 승격하지 않는다.",
        },
    )
    write_csv(
        RUNTIME_IDENTITY,
        [
            {
                "run_id": RUN_ID,
                "parent_run_id": PARENT_RUN_ID,
                "attempt_count": final["attempt_count"],
                "terminal_path": final["terminal_path"],
                "selected_variant_id": final.get("selected_variant_id", ""),
                "source_package": rel(pkg.FINAL_DECISION),
                "runtime_module_hash_count": len(pkg.mt5_runtime_module_hashes()),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> str:
    if not rows:
        return "_none(없음)_"
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(col, "")).replace("|", "\\|").replace("\n", " ") for col in columns) + " |")
    return "\n".join(lines)


def write_docs(final: Mapping[str, Any], summaries: Sequence[Mapping[str, Any]], proxy_rows: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]]) -> None:
    text = f"""# Stage364X density side-balance MT5 runtime probe(Stage364X 밀도 방향 균형 MT5 런타임 탐침)

## Current truth(현재 진실)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- judgment(판정): `{final["judgment"]}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
- runtime_authority(런타임 권위): `not_claimed`

## Action/Effect(행동/효과)

Action(행동): `run364W` package(패키지)를 MT5 Strategy Tester(MT5 전략 테스터)로 실행하고 telemetry/report(런타임 기록/보고서)를 수집했다.

Effect(효과): Python proxy(파이썬 프록시)와 MT5 runtime(런타임)의 probability/decision/KPI(확률/판정/핵심 성과 지표) 차이를 review(검토) 가능한 산출물로 만들었다.

## Execution summary(실행 요약)

{markdown_table(summaries, ["attempt_name", "tester_status", "runtime_status", "report_status", "net_profit", "profit_factor", "trade_count", "long_trade_count", "short_trade_count", "ready_model_rows", "matched_rows", "mismatch_rows", "comparison_status"])}

## Proxy vs MT5(프록시 대 MT5)

{markdown_table(proxy_rows, ["attempt_name", "expected_net_profit", "actual_mt5_net_profit", "net_profit_diff_actual_minus_expected", "expected_trade_count", "actual_mt5_trade_count", "trade_count_diff_actual_minus_expected", "expected_profit_factor", "actual_mt5_profit_factor", "report_status", "comparison_status"])}

## Gates(게이트)

{markdown_table(gates, ["gate(게이트)", "status", "evidence(근거)", "effect(효과)"])}

## Boundary(경계)

이 run(실행)은 runtime probe(런타임 탐침)다. forward pass(전진 통과), live readiness(실거래 준비), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 모두 `not_claimed`다.
"""
    write_text(REPORT_PATH, text)
    write_text(DECISION_DOC, text)
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current working state(현재 작업 상태)

date(날짜): {TODAY}

stage(단계): `{STAGE_ID}`

current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`

latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`

current_truth(현재 진실): `run364X`는 `run364W` package(패키지)를 MT5 Strategy Tester(MT5 전략 테스터)로 실행 시도했다. runtime_completed_rows(런타임 완료 행)는 `{final["runtime_completed_rows"]}`, usable_report_rows(사용 가능 보고서 행)는 `{final["usable_report_rows"]}`, actual MT5 net/PF/trades(실제 MT5 순수익/수익 팩터/거래수)는 `{final["actual_mt5_net_profit"]}` / `{final["actual_mt5_profit_factor"]}` / `{final["actual_mt5_trade_count"]}`다.

next_action(다음 행동): `{NEXT_RUN_ID}`에서 proxy-vs-MT5 diff(프록시-MT5 차이), cost stress(비용 압박), side balance(방향 균형)를 review(검토)한다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )
    write_text(
        WORKSPACE_STATE,
        f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {final["status"]}
current_judgment: {final["judgment"]}
next_run_id: {NEXT_RUN_ID}
runtime_authority: not_claimed
operating_promotion: not_claimed
goal_achieve: not_claimed
updated_at_utc: {final["created_at_utc"]}
""",
    )
    append_text_once(
        REVIEW_INDEX,
        f"- [{RUN_NUMBER}]",
        f"- [{RUN_NUMBER}] {RUN_ID}: {rel(REPORT_PATH)} - MT5 runtime probe(MT5 런타임 탐침), authority(권위) not_claimed(주장 안 함)\n",
    )
    append_text_once(
        STAGE_BRIEF,
        f"## {RUN_NUMBER}",
        f"\n## {RUN_NUMBER} MT5 runtime probe(MT5 런타임 탐침)\n\n- current truth(현재 진실): run364W package(패키지)를 Strategy Tester(전략 테스터)로 실행 시도했다.\n- effect(효과): proxy-vs-MT5 diff(프록시-MT5 차이) review(검토) 입력을 만들었다.\n",
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

- current_run(현재 실행): `{NEXT_RUN_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- selected_operating_model(선택 운영 모델): none(없음)
- promotion_candidate(승격 후보): not_claimed(주장 안 함)
- selected_runtime_package_candidate(선택 런타임 패키지 후보): `{final["selected_variant_id"]}`
- latest_mt5_probe(최근 MT5 탐침): `{RUN_ID}`
- actual_mt5_net_pf_trades(실제 MT5 순수익/수익 팩터/거래수): `{final["actual_mt5_net_profit"]}` / `{final["actual_mt5_profit_factor"]}` / `{final["actual_mt5_trade_count"]}`
- proxy_mt5_diff(프록시-MT5 차이): `{final["net_profit_diff_actual_minus_expected"]}` net(순수익), `{final["trade_count_diff_actual_minus_expected"]}` trades(거래수)
- blockers(차단): review(검토), cost stress(비용 압박), runtime authority audit(런타임 권위 감사) still required(아직 필요)
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )
    write_text(
        STAGE_README,
        f"""# {STAGE_ID}

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current truth(현재 진실): density side-balance repair candidate(밀도 방향 균형 수리 후보)의 MT5 runtime probe(MT5 런타임 탐침)를 실행 시도했다.

Next action(다음 행동): run364Y review(검토).
""",
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        f"- {RUN_ID}",
        f"- {RUN_ID}: executed MT5 runtime probe(MT5 런타임 탐침 실행) for selected density side-balance repair candidate(선택 밀도 방향 균형 수리 후보); authority(권위) not claimed(주장 안 함).\n",
    )
    append_text_once(
        IDEA_REGISTRY,
        f"- {RUN_ID}",
        f"- {RUN_ID}: MT5 runtime probe(MT5 런타임 탐침) produced proxy-vs-MT5 diff(프록시-MT5 차이) for dual-side threshold(양방향 임계값) candidate.\n",
    )


def write_ledgers(final: Mapping[str, Any]) -> None:
    gates = gate_rows(final)
    row = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__Tier_A",
        "parent_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "runtime_probe(런타임 탐침)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "external_verification_status": "mt5_runtime_probe_attempted(MT5 런타임 탐침 시도됨)",
        "notes": "Stage364X executes selected density side-balance repair candidate MT5 probe(Stage364X 선택 밀도 방향 균형 수리 후보 MT5 탐침 실행).",
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": final["decision"],
        "next_run_id": NEXT_RUN_ID,
        "rows": final["ready_model_rows"],
        "gate_passes": sum(1 for row_item in gates if row_item["status"] == "passed"),
        "gate_total": len(gates),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "run_date": TODAY,
        "primary_artifact": rel(EXECUTION_SUMMARY),
        "result_status": final["status"],
        "source_package_run_id": PARENT_RUN_ID,
        "work_family": "runtime_verification(런타임 검증)",
        "trade_density_requirement_status": "requires_review_from_mt5_trade_count(실제 MT5 거래수 기준 검토 필요)",
        "result_judgment": final["judgment"],
        "final_decision_path": rel(FINAL_DECISION),
        "created_at": final["created_at_utc"],
        "gate_audit_path": rel(GATE_AUDIT),
        "attempt_rows": final["attempt_count"],
        "runtime_completed_rows": final["runtime_completed_rows"],
        "matched_rows": final["matched_rows"],
        "mismatch_rows": final["mismatch_rows"],
        "net_profit": final["actual_mt5_net_profit"],
        "profit_factor": final["actual_mt5_profit_factor"],
        "trade_count": final["actual_mt5_trade_count"],
        "long_trade_count": final["actual_long_trade_count"],
        "short_trade_count": final["actual_short_trade_count"],
        "evidence_scope": "mt5_runtime_probe_no_authority(런타임 탐침, 권위 없음)",
    }
    append_or_replace_csv(STAGE_LEDGER, ["run_id", "subrun_id"], [row], extend_header=True)
    append_or_replace_csv(PROJECT_LEDGER, ["run_id", "subrun_id"], [row], extend_header=True)
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [row], extend_header=True)
    artifact_rows = [
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "artifact_type": artifact_type,
            "path": rel(path),
            "sha256": sha(path) if exists(path) and Path(path).is_file() else "",
            "created_at": final["created_at_utc"],
            "claim_boundary": CLAIM_BOUNDARY,
            "artifact_id": f"{RUN_NUMBER}_{artifact_type}",
            "created_at_utc": final["created_at_utc"],
            "notes": note,
            "artifact_path": rel(path),
        }
        for artifact_type, path, note in [
            ("execution_summary", EXECUTION_SUMMARY, "MT5 runtime probe summary(MT5 런타임 탐침 요약)."),
            ("probability_diff", PROBABILITY_DIFF, "Probability runtime diff(확률 런타임 차이)."),
            ("proxy_mt5_diff", PROXY_MT5_DIFF, "Proxy-vs-MT5 diff(프록시-MT5 차이)."),
            ("strategy_tester_reports", STRATEGY_TESTER_REPORTS, "Strategy tester report records(전략 테스터 보고서 기록)."),
            ("final_decision", FINAL_DECISION, "Final decision(최종 판정)."),
            ("run_manifest", RUN_MANIFEST, "Run manifest(실행 목록)."),
        ]
    ]
    append_or_replace_csv(ARTIFACT_REGISTRY, ["run_id", "artifact_type", "path"], artifact_rows, extend_header=True)


def write_final_files(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    write_csv(GATE_AUDIT, gates)
    write_json(FINAL_DECISION, final)
    outputs = [path for path in OUTPUT_FILES if exists(path)]
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": final["status"],
            "judgment": final["judgment"],
            "claim_boundary": CLAIM_BOUNDARY,
            "input_files": [rel(path) for path in INPUT_FILES],
            "output_files": [rel(path) for path in outputs],
            "output_hashes": {rel(path): sha(path) for path in outputs if Path(path).is_file()},
        },
    )


def main() -> None:
    args = parse_args()
    ensure_dirs()
    parent = validate_parent()
    attempts = enrich_attempts()
    execution_results, report_records, copy_rows, _ = execute_attempts(args, attempts)
    summaries, diffs, _skips, proxy_rows = compare_outputs(attempts, execution_results, report_records)
    final = build_final(args, parent, attempts, execution_results, report_records, summaries, diffs, copy_rows, proxy_rows)
    gates = gate_rows(final)
    final["gate_passes"] = sum(1 for row in gates if row["status"] == "passed")
    final["gate_total"] = len(gates)
    write_receipts(final)
    write_docs(final, summaries, proxy_rows, gates)
    write_final_files(final, gates)
    write_ledgers(final)
    write_final_files(final, gates)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
