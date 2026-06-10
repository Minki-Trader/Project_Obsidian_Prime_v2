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

from foundation.control_plane.ledger import io_path  # noqa: E402
from foundation.mt5 import runtime_support as mt5  # noqa: E402
from stage_pipelines.stage364 import materialize_h17_bad_month_source_balance_repair_mt5_runtime_probe_inputs_without_db as pkg  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-06"
STAGE_ID = pkg.STAGE_ID
RUN_NUMBER = "run364CP"
RUN_ID = "run364CP_execute_h17_bad_month_source_balance_repair_mt5_runtime_probe_without_db_v1"
PARENT_RUN_ID = pkg.RUN_ID
NEXT_RUN_ID = "run364CQ_review_h17_bad_month_source_balance_repair_mt5_runtime_probe_without_db_v1"

STATUS_COMPLETED = "completed_stage364CP_h17_bad_month_source_balance_mt5_probe_outputs_available_review_required_no_authority"
STATUS_BLOCKED = "blocked_stage364CP_h17_bad_month_source_balance_mt5_probe_attempt_recorded_repair_required_no_authority"
JUDGMENT_COMPLETED = "mt5_runtime_probe_outputs_available_proxy_diff_review_required_no_authority"
JUDGMENT_BLOCKED = "mt5_runtime_probe_attempt_recorded_outputs_missing_or_failed_repair_required_no_authority"
DECISION_COMPLETED = "stage364CP_open_run364CQ_review_h17_bad_month_source_balance_mt5_runtime_probe"
DECISION_BLOCKED = "stage364CP_open_run364CQ_repair_or_review_h17_bad_month_source_balance_mt5_runtime_probe"
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

RUNTIME_PROBE_ATTEMPT_PACKAGE = RUN_DIR / "runtime_probe_attempt_package.csv"
TERMINAL_PROCESS_AUDIT = RUN_DIR / "terminal_process_audit.json"
MT5_EXECUTION_RESULT = RUN_DIR / "mt5_execution_result.json"
STRATEGY_TESTER_REPORTS = RUN_DIR / "strategy_tester_report_records.json"
EXECUTION_SUMMARY = RUN_DIR / "h17_bad_month_source_balance_mt5_probe_summary.csv"
PROXY_MT5_DIFF = RUN_DIR / "proxy_mt5_runtime_difference.csv"
RUNTIME_OUTPUT_COPY = RUN_DIR / "runtime_output_copy_manifest.csv"
RUNTIME_IDENTITY = RUN_DIR / "runtime_identity.csv"
EXPECTED_KPI_SUMMARY = RUN_DIR / "expected_kpi_summary.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
BACKTEST_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364CP_h17_bad_month_source_balance_repair_mt5_runtime_probe.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364CP_h17_bad_month_source_balance_repair_mt5_runtime_probe.md"
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
    pkg.TESTER_IDENTITY_CONTRACT,
    pkg.PROXY_MT5_COMPARISON_CONTRACT,
    pkg.RUNTIME_PARITY_CONTRACT,
    pkg.EXPECTED_KPI_SUMMARY,
    pkg.RUN_MANIFEST,
    pkg.SOURCE_FEATURE_MATRIX,
    pkg.SOURCE_ONNX,
    pkg.PORTABLE_EA_EX5,
]

OUTPUT_FILES = [
    RUNTIME_PROBE_ATTEMPT_PACKAGE,
    TERMINAL_PROCESS_AUDIT,
    MT5_EXECUTION_RESULT,
    STRATEGY_TESTER_REPORTS,
    EXECUTION_SUMMARY,
    PROXY_MT5_DIFF,
    RUNTIME_OUTPUT_COPY,
    RUNTIME_IDENTITY,
    EXPECTED_KPI_SUMMARY,
    WORK_PACKET,
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
    parser = argparse.ArgumentParser(description="Stage364CP h17 bad-month source-balance MT5 runtime probe.")
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


def rel(path: Path | str) -> str:
    return pkg.rel(path)


def fs_path(path: Path | str) -> str:
    return str(io_path(path))


def exists(path: Path | str) -> bool:
    return pkg.exists(path)


def sha(path: Path | str) -> str:
    return pkg.sha(path)


def read_json(path: Path) -> Any:
    return pkg.read_json(path)


def write_json(path: Path, payload: Any) -> None:
    pkg.write_json(path, pkg.parent.json_ready(payload))


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path), encoding="utf-8-sig").fillna("")


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    pkg.write_csv(path, rows, fieldnames)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    pkg.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    pkg.append_text_once(path, marker, text)


def append_or_replace_csv(
    path: Path,
    key_fields: Sequence[str],
    rows: Sequence[Mapping[str, Any]],
    *,
    extend_header: bool = True,
) -> None:
    target = path if Path(path).is_absolute() else ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    existing: list[dict[str, Any]] = []
    header: list[str] = []
    if target.exists():
        with target.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            header = list(reader.fieldnames or [])
            existing = [dict(row) for row in reader]
    if not header:
        for row in rows:
            for key in row:
                if key not in header:
                    header.append(str(key))
    if extend_header:
        for row in rows:
            for key in row:
                if key not in header:
                    header.append(str(key))

    def row_key(row: Mapping[str, Any]) -> tuple[str, ...]:
        return tuple(str(row.get(field, "")) for field in key_fields)

    replacement = {row_key(row): dict(row) for row in rows}
    kept = [row for row in existing if row_key(row) not in replacement]
    output_rows = kept + [replacement[key] for key in replacement]
    with target.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=header, extrasaction="ignore")
        writer.writeheader()
        for row in output_rows:
            writer.writerow({field: row.get(field, "") for field in header})


def replace_prefixed_lines(path: Path, replacements: Mapping[str, str], *, bom: bool = True) -> None:
    pkg.replace_prefixed_lines(path, replacements, bom=bom)


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
    for path in [RUN_DIR, MT5_DIR, TELEMETRY_COPY_DIR, REPORT_COPY_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_parent() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing CP inputs(CP 입력 누락): " + ", ".join(missing))
    parent = read_json(pkg.FINAL_DECISION)
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"CO next_run_id mismatch(CO 다음 실행 ID 불일치): {parent.get('next_run_id')} != {RUN_ID}")
    gates = read_csv(pkg.GATE_AUDIT)
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("CO gate audit(CO 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    if parent.get("compile_status") != "completed" or parent.get("portable_ea_copied") is not True:
        raise RuntimeError("CO compile/sync(컴파일/동기화)가 CP MT5 runtime probe(CP MT5 런타임 탐침)에 충분하지 않습니다.")
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
        "effect": "terminal64.exe process(터미널 프로세스) 충돌을 먼저 확인해 기존 MT5 session(세션) 손상을 줄입니다.",
    }


def write_work_packet() -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "primary_family": "runtime_backtest(런타임 백테스트)",
            "primary_skill": "obsidian-runtime-parity(런타임 동등성)",
            "support_skills": [
                "obsidian-backtest-forensics(백테스트 포렌식)",
                "obsidian-run-evidence-system(실행 근거 시스템)",
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-performance-attribution(성과 귀속)",
            ],
            "required_gates": [
                "tester_execution_attempt_gate",
                "runtime_output_gate",
                "strategy_report_gate",
                "proxy_mt5_diff_gate",
                "runtime_parity_boundary_gate",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def enrich_attempts() -> list[dict[str, Any]]:
    attempts = read_csv(pkg.RUNTIME_PROBE_ATTEMPT_PACKAGE).to_dict("records")
    enriched: list[dict[str, Any]] = []
    for row in attempts:
        attempt = dict(row)
        set_path = ROOT / str(attempt.get("set_path", ""))
        ini_path = ROOT / str(attempt.get("ini_path", ""))
        attempt["source_package_run_id"] = attempt.get("run_id", PARENT_RUN_ID)
        attempt["run_id"] = RUN_ID
        attempt["parent_run_id"] = PARENT_RUN_ID
        attempt["next_run_id"] = NEXT_RUN_ID
        attempt["tier"] = str(attempt.get("tier") or "Tier A")
        attempt["split"] = str(attempt.get("split") or "validation_oos")
        attempt["ini_name"] = ini_path.name
        attempt["set_name"] = set_path.name
        attempt["common_telemetry_path"] = str(attempt.get("runtime_telemetry_expected", ""))
        attempt["common_summary_path"] = str(attempt.get("runtime_summary_expected", ""))
        attempt["ini"] = {"tester": {"Report": attempt.get("report_name", "")}}
        attempt["set"] = {"path": attempt.get("set_path", "")}
        attempt["execution_run_id"] = RUN_ID
        attempt["effect"] = "CO package(CO 패키지)를 실제 MT5 runtime probe(MT5 런타임 탐침) 실행 입력으로 고정합니다."
        attempt["claim_boundary"] = CLAIM_BOUNDARY
        enriched.append(attempt)
    if not enriched:
        raise RuntimeError("runtime_probe_attempt_package(런타임 탐침 시도 패키지)가 비어 있습니다.")
    write_csv(RUNTIME_PROBE_ATTEMPT_PACKAGE, enriched)
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
                io_path(target.parent).mkdir(parents=True, exist_ok=True)
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
                    "effect": "runtime telemetry(런타임 기록)를 run folder(실행 폴더)에 고정해 재검토 근거를 남깁니다.",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    write_csv(RUNTIME_OUTPUT_COPY, rows)
    return rows


def execute_attempts(args: argparse.Namespace, attempts: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    common_files_root = Path(args.common_files_root)
    tester_profile_root = Path(args.tester_profile_root)
    terminal_data_root = Path(args.terminal_data_root)
    terminal_probe = terminal_processes()
    write_json(TERMINAL_PROCESS_AUDIT, terminal_probe)

    execution_results: list[dict[str, Any]] = []
    report_records: list[dict[str, Any]] = []
    terminal_blocked = terminal_probe.get("status") != "no_terminal64_process" and not args.reuse_existing_execution
    previous_results: dict[str, Mapping[str, Any]] = {}
    if args.reuse_existing_execution and exists(MT5_EXECUTION_RESULT):
        try:
            previous_payload = read_json(MT5_EXECUTION_RESULT)
            if isinstance(previous_payload, list):
                previous_results = {
                    str(row.get("attempt_name")): row
                    for row in previous_payload
                    if isinstance(row, Mapping) and row.get("attempt_name")
                }
        except Exception:
            previous_results = {}
    if terminal_blocked:
        for attempt in attempts:
            execution_results.append(
                {
                    "attempt_name": attempt["attempt_name"],
                    "status": "blocked",
                    "blocker": "target_portable_terminal_already_running",
                    "runtime_outputs": {"status": "blocked", "wait_status": "skipped_terminal_already_running"},
                    "ini_path": attempt.get("ini_path", ""),
                    "set_path": attempt.get("set_path", ""),
                    "effect": "이미 실행 중인 terminal64.exe(터미널 프로세스)를 건드리지 않아 MT5 session(세션) 손상을 줄입니다.",
                }
            )
    else:
        for attempt in attempts:
            if not args.reuse_existing_execution:
                remove_runtime_outputs(common_files_root, attempt)
                mt5.remove_existing_mt5_report_artifacts(terminal_data_root, attempt, run_id=RUN_ID)
            profile_ini = tester_profile_root / str(attempt["ini_name"])
            profile_set = tester_profile_root / str(attempt["set_name"])
            try:
                if args.reuse_existing_execution:
                    previous = previous_results.get(str(attempt.get("attempt_name")))
                    tester_result = dict(previous) if previous else {
                        "status": "reused_existing_execution",
                        "command": "not_run_reuse_existing_execution",
                        "returncode": "",
                    }
                    tester_result["reuse_closeout"] = True
                else:
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
                tester_result["status"] = "blocked" if tester_result.get("status") != "reused_existing_execution" else "blocked_reused_outputs_missing"
                tester_result.setdefault("blocker", "runtime_outputs_missing_or_init_failed")
            execution_log = MT5_DIR / f"{attempt['attempt_name']}_tester_execution.json"
            write_json(execution_log, {"tester_result": tester_result, "runtime_outputs": runtime_outputs})
            execution_results.append(
                {
                    **tester_result,
                    "attempt_name": attempt["attempt_name"],
                    "model_id": attempt.get("model_id", ""),
                    "candidate_id": attempt.get("candidate_id", ""),
                    "runtime_outputs": runtime_outputs,
                    "ini_path": attempt.get("ini_path", ""),
                    "set_path": attempt.get("set_path", ""),
                    "claim_boundary": CLAIM_BOUNDARY,
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
    return execution_results, report_records, copy_rows


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


def runtime_summary_payload(path: Path) -> dict[str, Any]:
    if not exists(path):
        return {}
    try:
        frame = pd.read_csv(io_path(path), encoding="utf-8-sig").fillna("")
    except Exception as exc:  # pragma: no cover - defensive MT5 handoff parsing
        return {"parse_error": str(exc)}
    if frame.empty:
        return {"rows": 0}
    last = frame.iloc[-1].to_dict()
    return {"rows": len(frame), "last_summary": pkg.parent.json_ready(last)}


def report_usable(report_row: Mapping[str, Any]) -> bool:
    metrics = report_metrics_for_attempt(report_row)
    status = str(report_row.get("status") or metrics.get("status") or "")
    return status in {"completed", "usable", "parsed"}


def summarize_outputs(
    attempts: Sequence[Mapping[str, Any]],
    execution_results: Sequence[Mapping[str, Any]],
    report_records: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    executions = {row.get("attempt_name"): row for row in execution_results}
    reports = {row.get("attempt_name"): row for row in report_records}
    rows: list[dict[str, Any]] = []
    for attempt in attempts:
        execution = executions.get(attempt.get("attempt_name"), {})
        report = reports.get(attempt.get("attempt_name"), {})
        runtime = execution.get("runtime_outputs", {}) if isinstance(execution.get("runtime_outputs"), Mapping) else {}
        metrics = report_metrics_for_attempt(report)
        tester_status = execution.get("status", "not_attempted")
        blocker = execution.get("blocker", "")
        report_is_usable = report_usable(report)
        if (runtime.get("status") == "completed" or report_is_usable) and blocker == "terminal_timeout":
            tester_status = "completed_with_terminal_timeout_after_outputs_available"
            blocker = "terminal_timeout_after_outputs_available"
        local_summary = local_summary_path(attempt)
        local_telemetry = local_telemetry_path(attempt)
        summary_payload = runtime_summary_payload(local_summary)
        last_summary = summary_payload.get("last_summary", {}) if isinstance(summary_payload.get("last_summary"), Mapping) else {}
        rows.append(
            {
                "attempt_name": attempt.get("attempt_name", ""),
                "candidate_id": attempt.get("candidate_id", ""),
                "model_id": attempt.get("model_id", ""),
                "tester_status": tester_status,
                "runtime_status": runtime.get("status", "missing"),
                "runtime_wait_status": runtime.get("wait_status", ""),
                "report_status": report.get("status", "missing") if report else "missing",
                "returncode": execution.get("returncode", ""),
                "blocker": blocker,
                "local_telemetry_path": rel(local_telemetry) if exists(local_telemetry) else "",
                "local_summary_path": rel(local_summary) if exists(local_summary) else "",
                "report_path": report_path_from_record(report),
                "summary_rows": summary_payload.get("rows", ""),
                "feature_ready_count": last_summary.get("feature_ready_count", ""),
                "model_ok_count": last_summary.get("model_ok_count", ""),
                "order_attempt_count": last_summary.get("order_attempt_count", ""),
                "order_filled_count": last_summary.get("order_filled_count", last_summary.get("order_fill_count", "")),
                "net_profit": metrics.get("net_profit", ""),
                "profit_factor": metrics.get("profit_factor", ""),
                "trade_count": metrics.get("trade_count", ""),
                "expectancy": metrics.get("expectancy", ""),
                "recovery_factor": metrics.get("recovery_factor", ""),
                "max_drawdown_amount": metrics.get("max_drawdown_amount", ""),
                "max_drawdown_percent": metrics.get("max_drawdown_percent", ""),
                "long_trade_count": metrics.get("long_trade_count", ""),
                "short_trade_count": metrics.get("short_trade_count", ""),
                "win_rate_percent": metrics.get("win_rate_percent", ""),
                "comparison_status": "runtime_or_report_available" if runtime.get("status") == "completed" or report_usable(report) else "blocked_no_runtime_or_report_output",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(EXECUTION_SUMMARY, rows)
    return rows


def expected_kpi_rows() -> list[dict[str, Any]]:
    rows = read_csv(pkg.EXPECTED_KPI_SUMMARY).to_dict("records")
    copied: list[dict[str, Any]] = []
    for row in rows:
        payload = dict(row)
        payload["source_run_id"] = payload.get("run_id", PARENT_RUN_ID)
        payload["run_id"] = RUN_ID
        payload["claim_boundary"] = CLAIM_BOUNDARY
        copied.append(payload)
    write_csv(EXPECTED_KPI_SUMMARY, copied)
    return copied


def build_proxy_diff(expected_rows: Sequence[Mapping[str, Any]], summaries: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    expected = expected_rows[0] if expected_rows else {}
    rows: list[dict[str, Any]] = []
    for summary in summaries:
        expected_net = float_or_nan(expected.get("expected_proxy_net"))
        actual_net = float_or_nan(summary.get("net_profit"))
        expected_trades = float_or_nan(expected.get("expected_proxy_trade_count"))
        actual_trades = float_or_nan(summary.get("trade_count"))
        expected_pf = float_or_nan(expected.get("expected_proxy_profit_factor"))
        actual_pf = float_or_nan(summary.get("profit_factor"))
        expected_expectancy = float_or_nan(expected.get("expected_proxy_expectancy"))
        actual_expectancy = float_or_nan(summary.get("expectancy"))
        rows.append(
            {
                "attempt_name": summary.get("attempt_name", ""),
                "candidate_id": summary.get("candidate_id", ""),
                "expected_net_profit": finite(expected_net),
                "actual_mt5_net_profit": finite(actual_net),
                "net_profit_diff_actual_minus_expected": finite(actual_net - expected_net) if math.isfinite(expected_net) and math.isfinite(actual_net) else "",
                "expected_profit_factor": finite(expected_pf),
                "actual_mt5_profit_factor": finite(actual_pf),
                "profit_factor_diff_actual_minus_expected": finite(actual_pf - expected_pf) if math.isfinite(expected_pf) and math.isfinite(actual_pf) else "",
                "expected_expectancy": finite(expected_expectancy),
                "actual_mt5_expectancy": finite(actual_expectancy),
                "expectancy_diff_actual_minus_expected": finite(actual_expectancy - expected_expectancy) if math.isfinite(expected_expectancy) and math.isfinite(actual_expectancy) else "",
                "expected_trade_count": finite(expected_trades, 0),
                "actual_mt5_trade_count": finite(actual_trades, 0),
                "trade_count_diff_actual_minus_expected": finite(actual_trades - expected_trades, 0) if math.isfinite(expected_trades) and math.isfinite(actual_trades) else "",
                "actual_long_trade_count": summary.get("long_trade_count", ""),
                "actual_short_trade_count": summary.get("short_trade_count", ""),
                "actual_drawdown": summary.get("max_drawdown_amount", ""),
                "actual_recovery_factor": summary.get("recovery_factor", ""),
                "runtime_status": summary.get("runtime_status", ""),
                "report_status": summary.get("report_status", ""),
                "comparison_status": summary.get("comparison_status", ""),
                "diff_boundary": "proxy_expected_value(프록시 예상값)는 MT5 KPI(MT5 핵심 성과 지표)를 대체하지 않습니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(PROXY_MT5_DIFF, rows)
    return rows


def output_available_count(summaries: Sequence[Mapping[str, Any]]) -> int:
    return sum(1 for row in summaries if row.get("runtime_status") == "completed" or row.get("report_status") in {"completed", "usable", "parsed"})


def usable_report_count(report_records: Sequence[Mapping[str, Any]]) -> int:
    return sum(1 for row in report_records if report_usable(row))


def build_final(
    args: argparse.Namespace,
    parent: Mapping[str, Any],
    attempts: Sequence[Mapping[str, Any]],
    execution_results: Sequence[Mapping[str, Any]],
    report_records: Sequence[Mapping[str, Any]],
    summaries: Sequence[Mapping[str, Any]],
    proxy_rows: Sequence[Mapping[str, Any]],
    copy_rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    outputs_available = output_available_count(summaries)
    runtime_completed = sum(1 for row in summaries if row.get("runtime_status") == "completed")
    usable_reports = usable_report_count(report_records)
    status = STATUS_COMPLETED if outputs_available else STATUS_BLOCKED
    judgment = JUDGMENT_COMPLETED if outputs_available else JUDGMENT_BLOCKED
    decision = DECISION_COMPLETED if outputs_available else DECISION_BLOCKED
    summary = summaries[0] if summaries else {}
    proxy = proxy_rows[0] if proxy_rows else {}
    first_execution = execution_results[0] if execution_results else {}
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "stage_id": STAGE_ID,
        "status": status,
        "judgment": judgment,
        "decision": decision,
        "created_at_utc": now_utc(),
        "claim_boundary": CLAIM_BOUNDARY,
        "candidate_id": parent.get("candidate_id"),
        "attempt_count": len(attempts),
        "runtime_completed_rows": runtime_completed,
        "usable_report_rows": usable_reports,
        "outputs_available_rows": outputs_available,
        "runtime_output_copy_rows": len(copy_rows),
        "terminal_path": str(args.terminal_path),
        "common_files_root": str(args.common_files_root),
        "tester_profile_root": str(args.tester_profile_root),
        "terminal_data_root": str(args.terminal_data_root),
        "tester_first_status": summary.get("tester_status", first_execution.get("status", "")),
        "tester_first_blocker": summary.get("blocker", first_execution.get("blocker", "")),
        "expected_net_profit": proxy.get("expected_net_profit", parent.get("expected_proxy_net", "")),
        "actual_mt5_net_profit": proxy.get("actual_mt5_net_profit", summary.get("net_profit", "")),
        "net_profit_diff_actual_minus_expected": proxy.get("net_profit_diff_actual_minus_expected", ""),
        "expected_trade_count": proxy.get("expected_trade_count", parent.get("expected_proxy_trade_count", "")),
        "actual_mt5_trade_count": proxy.get("actual_mt5_trade_count", summary.get("trade_count", "")),
        "trade_count_diff_actual_minus_expected": proxy.get("trade_count_diff_actual_minus_expected", ""),
        "expected_profit_factor": proxy.get("expected_profit_factor", parent.get("expected_proxy_profit_factor", "")),
        "actual_mt5_profit_factor": proxy.get("actual_mt5_profit_factor", summary.get("profit_factor", "")),
        "actual_mt5_expectancy": proxy.get("actual_mt5_expectancy", summary.get("expectancy", "")),
        "actual_long_trade_count": proxy.get("actual_long_trade_count", summary.get("long_trade_count", "")),
        "actual_short_trade_count": proxy.get("actual_short_trade_count", summary.get("short_trade_count", "")),
        "actual_drawdown": proxy.get("actual_drawdown", summary.get("max_drawdown_amount", "")),
        "actual_recovery_factor": proxy.get("actual_recovery_factor", summary.get("recovery_factor", "")),
        "report_path": summary.get("report_path", ""),
        "comparison_status": summary.get("comparison_status", ""),
        "mt5_execution": "attempted",
        "external_verification_status": "mt5_runtime_probe_attempted_outputs_available" if outputs_available else "mt5_runtime_probe_attempted_outputs_missing_or_blocked",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "live_readiness": "not_claimed",
        "report_file": rel(REPORT_PATH),
        "final_decision": rel(FINAL_DECISION),
    }


def gate_rows(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    runtime_ok = int(final.get("runtime_completed_rows") or 0) > 0
    report_ok = int(final.get("usable_report_rows") or 0) > 0
    outputs_available = int(final.get("outputs_available_rows") or 0) > 0
    return [
        {
            "run_id": RUN_ID,
            "gate": "tester_execution_attempt_gate",
            "status": "passed",
            "evidence": rel(MT5_EXECUTION_RESULT),
            "effect": "MT5 Strategy Tester(MT5 전략 테스터) 실행 시도 또는 차단 사유를 기록합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "runtime_output_gate",
            "status": "passed" if runtime_ok else "blocked",
            "evidence": rel(RUNTIME_OUTPUT_COPY),
            "effect": "runtime telemetry/summary(런타임 기록/요약) 존재를 확인합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "strategy_report_gate",
            "status": "passed" if report_ok else "blocked",
            "evidence": rel(STRATEGY_TESTER_REPORTS),
            "effect": "tester KPI(테스터 핵심 성과 지표) 추출 여부를 고정합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "proxy_mt5_diff_gate",
            "status": "passed" if outputs_available else "blocked",
            "evidence": rel(PROXY_MT5_DIFF),
            "effect": "proxy expected value(프록시 예상값)와 MT5 KPI(MT5 핵심 성과 지표)를 분리합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "runtime_parity_boundary_gate",
            "status": "passed",
            "evidence": rel(RUNTIME_RECEIPT),
            "effect": "runtime probe(런타임 탐침)를 runtime authority(런타임 권위)로 승격하지 않게 합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "required_gate_coverage_audit",
            "status": "passed",
            "evidence": rel(GATE_AUDIT),
            "effect": "필수 gate(게이트)를 closeout(종료 기록)에 연결합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "final_claim_guard",
            "status": "passed",
            "evidence": rel(CLAIM_RECEIPT),
            "effect": "Goal Achieve(목표 달성), operating promotion(운영 승격), runtime authority(런타임 권위)를 모두 막습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def write_receipts(final: Mapping[str, Any]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(
        BACKTEST_RECEIPT,
        {
            **base,
            "tester_identity": rel(pkg.TESTER_IDENTITY_CONTRACT),
            "ea_identity": mt5.mt5_runtime_module_hashes(),
            "report_identity": rel(STRATEGY_TESTER_REPORTS),
            "trade_evidence": rel(EXECUTION_SUMMARY),
            "cost_assumptions": "broker-native Strategy Tester(브로커 원생 전략 테스터) output(출력)에서 확인합니다.",
            "forensic_checks": [rel(MT5_EXECUTION_RESULT), rel(STRATEGY_TESTER_REPORTS), rel(RUNTIME_OUTPUT_COPY), rel(PROXY_MT5_DIFF)],
            "backtest_judgment": "usable_with_boundary(경계 포함 사용 가능)" if int(final.get("usable_report_rows") or 0) else "blocked_or_inconclusive(차단 또는 불충분)",
        },
    )
    write_json(
        RUNTIME_RECEIPT,
        {
            **base,
            "research_path": rel(pkg.RUNTIME_POLICY_CONFIG),
            "runtime_path": [rel(pkg.RUNTIME_PROBE_ATTEMPT_PACKAGE), rel(pkg.TESTER_SET_MANIFEST), rel(pkg.TESTER_INI_MANIFEST)],
            "shared_contract": rel(pkg.RUNTIME_PARITY_CONTRACT),
            "known_differences": "MT5 tester(테스터) cost/fill/runtime(비용/체결/런타임)는 proxy(프록시)와 다를 수 있습니다.",
            "parity_check": [rel(EXECUTION_SUMMARY), rel(PROXY_MT5_DIFF)],
            "parity_identity": f"model={sha(pkg.SOURCE_ONNX)};set_manifest={sha(pkg.TESTER_SET_MANIFEST)};module_hashes={len(mt5.mt5_runtime_module_hashes())}",
            "runtime_claim_boundary": "runtime_probe(런타임 탐침), not authority(권위 아님)",
        },
    )
    write_json(
        PERFORMANCE_RECEIPT,
        {
            **base,
            "expected_vs_actual": rel(PROXY_MT5_DIFF),
            "attribution_scope": "proxy-vs-MT5 first pass(프록시 대 MT5 1차 비교)",
            "judgment": final["judgment"],
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "result_subject": RUN_ID,
            "evidence_available": [rel(EXECUTION_SUMMARY), rel(PROXY_MT5_DIFF), rel(STRATEGY_TESTER_REPORTS), rel(RUNTIME_OUTPUT_COPY)],
            "judgment_label": final["judgment"],
            "next_condition": NEXT_RUN_ID,
            "evidence_boundary": "runtime_probe_execution_attempt_no_authority(런타임 탐침 실행 시도, 권위 없음)",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(path).is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_and_local_mt5_outputs_if_available(추적 가능 및 로컬 MT5 출력 가능 시 고정)",
            "lineage_judgment": "connected_with_runtime_probe_boundary(런타임 탐침 경계 포함 연결)",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "mt5_execution": "attempted",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "live_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "effect": "MT5 runtime probe(MT5 런타임 탐침)를 operating claim(운영 주장)으로 승격하지 않습니다.",
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
                "candidate_id": final.get("candidate_id", ""),
                "source_package": rel(pkg.FINAL_DECISION),
                "runtime_module_hash_count": len(mt5.mt5_runtime_module_hashes()),
                "set_manifest": rel(pkg.TESTER_SET_MANIFEST),
                "ini_manifest": rel(pkg.TESTER_INI_MANIFEST),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int = 12) -> str:
    if not rows:
        return "_none(없음)_"
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows[:limit]:
        lines.append("| " + " | ".join(str(row.get(col, "")).replace("|", "\\|").replace("\n", " ") for col in columns) + " |")
    if len(rows) > limit:
        lines.append(f"| ... | {len(rows) - limit} more rows(추가 행) |  |  |")
    return "\n".join(lines)


def write_docs(final: Mapping[str, Any], summaries: Sequence[Mapping[str, Any]], proxy_rows: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]]) -> None:
    report = f"""# run364CP h17 bad-month source-balance MT5 runtime probe(17시 손실 월/원천 균형 MT5 런타임 탐침)

Updated(갱신): {final['created_at_utc']}

## Current Truth(현재 진실)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- judgment(판정): `{final['judgment']}`
- mt5_execution(MT5 실행): `{final['mt5_execution']}`
- runtime_authority(런타임 권위): `not_claimed`

## Action/Effect(행동/효과)

Action(행동): CO package(CO 패키지) `cm04_cj09_month08_12_pair_guard`를 MT5 Strategy Tester(MT5 전략 테스터)로 실행 시도하고 telemetry/report(런타임 기록/보고서)를 수집했습니다.

Effect(효과): proxy expected value(프록시 예상값)와 실제 MT5 output(MT5 출력)을 분리해 CQ review(CQ 검토)에서 차이(diff, 차이), 원인(attribution, 귀속), usability(활용 가능성)를 판단할 수 있게 했습니다.

## Execution Summary(실행 요약)

{markdown_table(summaries, ['attempt_name', 'tester_status', 'runtime_status', 'report_status', 'net_profit', 'profit_factor', 'trade_count', 'long_trade_count', 'short_trade_count', 'blocker', 'comparison_status'])}

## Proxy vs MT5(프록시 대 MT5)

{markdown_table(proxy_rows, ['attempt_name', 'expected_net_profit', 'actual_mt5_net_profit', 'net_profit_diff_actual_minus_expected', 'expected_trade_count', 'actual_mt5_trade_count', 'trade_count_diff_actual_minus_expected', 'expected_profit_factor', 'actual_mt5_profit_factor', 'comparison_status'])}

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'])}

## Boundary(경계)

This run(이번 실행)은 runtime probe attempt(런타임 탐침 시도)입니다. forward pass(전진 통과), live readiness(실거래 준비), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 모두 `not_claimed`입니다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# Stage364CP decision(결정): h17 bad-month source-balance MT5 runtime probe

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{final['decision']}`
- judgment(판정): `{final['judgment']}`
- runtime_completed_rows(런타임 완료 행): `{final['runtime_completed_rows']}`
- usable_report_rows(사용 가능 보고서 행): `{final['usable_report_rows']}`
- actual MT5 net/PF/trades(실제 MT5 순수익/수익 팩터/거래수): `{final['actual_mt5_net_profit']}` / `{final['actual_mt5_profit_factor']}` / `{final['actual_mt5_trade_count']}`
- next action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): CQ에서 proxy/MT5 diff(프록시/MT5 차이)를 검토하게 합니다.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, f"run364CP__{RUN_ID}", f"\n- run364CP__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - MT5 runtime probe(MT5 런타임 탐침) attempted(시도됨), next `{NEXT_RUN_ID}`.\n")
    append_text_once(STAGE_BRIEF, f"## run364CP__{RUN_ID}", f"\n## run364CP MT5 Runtime Probe Attempt(MT5 런타임 탐침 시도)\n\nAction(행동): CM04 runtime package(CM04 런타임 패키지)를 Strategy Tester(전략 테스터)로 실행 시도했습니다.\n\nEffect(효과): `{NEXT_RUN_ID}`에서 proxy/MT5 diff(프록시/MT5 차이)를 검토할 수 있습니다.\n")
    append_text_once(STAGE_README, f"run364CP__{RUN_ID}", f"\n<!-- run364CP__{RUN_ID} -->\n## run364CP MT5 runtime probe(MT5 런타임 탐침)\n\n`{final['candidate_id']}` probe(탐침) attempted(시도됨). Next(다음): `{NEXT_RUN_ID}`.\n")
    replace_prefixed_lines(
        STAGE_BRIEF,
        {
            "- current_run_id(현재 실행 ID):": f"- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`",
            "- latest_completed_run_id(최근 완료 실행 ID):": f"- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`",
            "- selection_status(선택 상태):": f"- selection_status(선택 상태): `{final['status']}`",
            "- claim_boundary(주장 경계):": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        },
        bom=True,
    )
    write_text(
        WORKSPACE_STATE,
        f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {final['status']}
current_judgment: {final['judgment']}
next_run_id: {NEXT_RUN_ID}
runtime_authority: not_claimed
operating_promotion: not_claimed
goal_achieve: not_claimed
updated_at_utc: {final['created_at_utc']}
""",
        bom=False,
    )
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Current truth(현재 진실): `run364CP` executed/attempted(실행/시도) CM04 MT5 runtime probe(CM04 MT5 런타임 탐침). runtime_completed_rows(런타임 완료 행)는 `{final['runtime_completed_rows']}`, usable_report_rows(사용 가능 보고서 행)는 `{final['usable_report_rows']}`, actual MT5 net/PF/trades(실제 MT5 순수익/수익 팩터/거래수)는 `{final['actual_mt5_net_profit']}` / `{final['actual_mt5_profit_factor']}` / `{final['actual_mt5_trade_count']}`입니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 proxy/MT5 diff(프록시/MT5 차이), cost stress(비용 압박), side balance(방향 균형), runtime output(런타임 출력)을 review(검토)합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""",
        bom=True,
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest MT5 runtime probe(최근 MT5 런타임 탐침): `{RUN_ID}`.

Actual MT5 net/PF/trades(실제 MT5 순수익/수익 팩터/거래수): `{final['actual_mt5_net_profit']}` / `{final['actual_mt5_profit_factor']}` / `{final['actual_mt5_trade_count']}`.

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""",
        bom=True,
    )
    append_text_once(WORKSPACE_CHANGELOG, f"run364CP__{RUN_ID}", f"\n<!-- run364CP__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` attempted MT5 runtime probe(MT5 런타임 탐침 시도); judgment `{final['judgment']}`; no authority claim(권위 주장 없음).\n")
    append_text_once(IDEA_REGISTRY, f"run364CP__{RUN_ID}", f"\n<!-- run364CP__{RUN_ID} -->\n- `{RUN_ID}`: CM04 source-balance guard(CM04 원천 균형 가드)를 MT5 runtime probe(MT5 런타임 탐침)로 실행 시도. Effect(효과): proxy expected value(프록시 예상값)와 tester output(테스터 출력)의 차이 검토 입력을 만든다.\n")


def write_ledgers(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    row = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__Tier_A",
        "parent_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "runtime_probe(런타임 탐침)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "external_verification_status": final["external_verification_status"],
        "notes": "Stage364CP attempts CM04 h17 bad-month source-balance MT5 probe(Stage364CP CM04 17시 손실 월/원천 균형 MT5 탐침 시도).",
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": final["decision"],
        "next_run_id": NEXT_RUN_ID,
        "rows": final["outputs_available_rows"],
        "gate_passes": sum(1 for row_item in gates if row_item["status"] == "passed"),
        "gate_total": len(gates),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "run_date": TODAY,
        "primary_artifact": rel(EXECUTION_SUMMARY),
        "result_status": final["status"],
        "source_package_run_id": PARENT_RUN_ID,
        "work_family": "runtime_backtest(런타임 백테스트)",
        "trade_density_requirement_status": "requires_review_from_mt5_trade_count(실제 MT5 거래수 기준 검토 필요)",
        "result_judgment": final["judgment"],
        "final_decision_path": rel(FINAL_DECISION),
        "created_at": final["created_at_utc"],
        "gate_audit_path": rel(GATE_AUDIT),
        "attempt_rows": final["attempt_count"],
        "runtime_completed_rows": final["runtime_completed_rows"],
        "usable_report_rows": final["usable_report_rows"],
        "net_profit": final["actual_mt5_net_profit"],
        "profit_factor": final["actual_mt5_profit_factor"],
        "expectancy": final["actual_mt5_expectancy"],
        "trade_count": final["actual_mt5_trade_count"],
        "long_trade_count": final["actual_long_trade_count"],
        "short_trade_count": final["actual_short_trade_count"],
        "evidence_scope": "mt5_runtime_probe_no_authority(MT5 런타임 탐침, 권위 없음)",
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
            "sha256": sha(path) if exists(path) and io_path(path).is_file() else "",
            "created_at": final["created_at_utc"],
            "claim_boundary": CLAIM_BOUNDARY,
            "artifact_id": f"{RUN_NUMBER}_{artifact_type}",
            "created_at_utc": final["created_at_utc"],
            "notes": note,
            "artifact_path": rel(path),
        }
        for artifact_type, path, note in [
            ("execution_summary", EXECUTION_SUMMARY, "MT5 runtime probe summary(MT5 런타임 탐침 요약)."),
            ("proxy_mt5_diff", PROXY_MT5_DIFF, "Proxy-vs-MT5 diff(프록시 대 MT5 차이)."),
            ("strategy_tester_reports", STRATEGY_TESTER_REPORTS, "Strategy tester report records(전략 테스터 보고서 기록)."),
            ("runtime_output_copy", RUNTIME_OUTPUT_COPY, "Runtime output copy manifest(런타임 출력 복사 목록)."),
            ("final_decision", FINAL_DECISION, "Final decision(최종 판정)."),
            ("run_manifest", RUN_MANIFEST, "Run manifest(실행 목록)."),
            ("report", REPORT_PATH, "Human report(사람용 보고서)."),
        ]
    ]
    append_or_replace_csv(ARTIFACT_REGISTRY, ["run_id", "artifact_type", "path"], artifact_rows, extend_header=True)
    repair_run_registry_line_endings(RUN_ID)


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
            "input_hashes": {rel(path): sha(path) for path in INPUT_FILES if exists(path) and io_path(path).is_file()},
            "output_files": [rel(path) for path in outputs],
            "output_hashes": {rel(path): sha(path) for path in outputs if io_path(path).is_file()},
        },
    )


def main() -> None:
    args = parse_args()
    ensure_dirs()
    parent = validate_parent()
    write_work_packet()
    attempts = enrich_attempts()
    expected_rows = expected_kpi_rows()
    execution_results, report_records, copy_rows = execute_attempts(args, attempts)
    summaries = summarize_outputs(attempts, execution_results, report_records)
    proxy_rows = build_proxy_diff(expected_rows, summaries)
    final = build_final(args, parent, attempts, execution_results, report_records, summaries, proxy_rows, copy_rows)
    gates = gate_rows(final)
    final["gate_passes"] = sum(1 for row in gates if row["status"] == "passed")
    final["gate_total"] = len(gates)
    write_receipts(final)
    gates = gate_rows(final)
    final["gate_passes"] = sum(1 for row in gates if row["status"] == "passed")
    final["gate_total"] = len(gates)
    write_docs(final, summaries, proxy_rows, gates)
    write_final_files(final, gates)
    write_ledgers(final, gates)
    write_final_files(final, gates)
    print(json.dumps(pkg.parent.json_ready(final), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
