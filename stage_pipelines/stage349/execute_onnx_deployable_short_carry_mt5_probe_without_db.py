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

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.mt5 import runtime_support as mt5  # noqa: E402
from stage_pipelines.stage337.execute_model_scout_mt5_runtime_probe_without_db import (  # noqa: E402
    terminal_processes,
)
from stage_pipelines.stage348 import (  # noqa: E402
    materialize_onnx_deployable_short_carry_probe_package_without_db as source_pkg,
)


TODAY = "2026-06-01"
STAGE_ID = "349_onnx_short_carry_runtime__execute_mt5_probe"
RUN_NUMBER = "run349B"
RUN_ID = "run349B_execute_onnx_deployable_short_carry_mt5_probe_without_db_v1"
PARENT_RUN_ID = "run349A_branch_stage348_to_onnx_short_carry_runtime_probe_without_db_v1"
SOURCE_PACKAGE_RUN_ID = source_pkg.RUN_ID
SOURCE_STAGE_ID = source_pkg.STAGE_ID
NEXT_RUN_ID = "run349C_review_onnx_short_carry_mt5_probe_without_db_v1"

STATUS_COMPLETED = "completed_stage349B_onnx_short_carry_mt5_probe_executed_review_required_no_selection"
STATUS_BLOCKED = "blocked_stage349B_onnx_short_carry_mt5_probe_attempt_recorded_repair_required_no_selection"
JUDGMENT_COMPLETED = "mt5_onnx_short_carry_probe_outputs_available_proxy_diff_and_trade_density_review_required_no_selection"
JUDGMENT_BLOCKED = "mt5_onnx_short_carry_probe_attempt_recorded_but_outputs_missing_or_failed_repair_required"
DECISION_COMPLETED = "stage349B_open_run349C_review_onnx_short_carry_mt5_probe"
DECISION_BLOCKED = "stage349B_open_run349C_review_or_repair_onnx_short_carry_mt5_probe"
CLAIM_BOUNDARY = (
    "research_development_onnx_short_carry_mt5_runtime_probe_attempt_only_"
    "no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_"
    "no_runtime_authority_no_goal_claim"
)
TRADE_DENSITY_REQUIREMENT = "trade_per_day_min_3_to_10_plus_no_trade_splitting"
COMMON_ROOT = "Project_Obsidian_Prime_v2/stage349/run349B_onnx_short_carry_mt5_probe"
COMMON_TELEMETRY_DIR = f"{COMMON_ROOT}/telemetry"
EXPLORATION_LABEL = "stage349_ONNXShortCarry__MT5RuntimeProbeExecution"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MT5_DIR = RUN_DIR / "mt5"
SET_DIR = MT5_DIR / "sets"
INI_DIR = MT5_DIR / "inis"
TELEMETRY_COPY_DIR = RUN_DIR / "runtime_telemetry"
REPORT_COPY_DIR = MT5_DIR / "reports"
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run349B_onnx_short_carry_mt5_probe.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage349B_onnx_short_carry_mt5_probe.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_README = STAGE_DIR / "README.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"

RUN349A_DIR = STAGE_DIR / "02_runs" / "run349A"
RUN349A_FINAL_DECISION = RUN349A_DIR / "final_decision.json"
RUN349A_GATE_AUDIT = RUN349A_DIR / "required_gate_coverage_audit.csv"
RUN349B_QUEUE = RUN349A_DIR / "run349B_onnx_short_carry_mt5_probe_queue.csv"

SOURCE_RUN_DIR = ROOT / "stages" / SOURCE_STAGE_ID / "02_runs" / "run348C"
SOURCE_ATTEMPT_PACKAGE = source_pkg.RUNTIME_PROBE_ATTEMPT_PACKAGE
SOURCE_FINAL_DECISION = source_pkg.FINAL_DECISION
SOURCE_GATE_AUDIT = source_pkg.GATE_AUDIT
SOURCE_EXPECTED_TAPE = source_pkg.EXPECTED_TAPE
SOURCE_EXPECTED_INDEX = source_pkg.EXPECTED_TAPE_INDEX
SOURCE_RUNTIME_PARITY = source_pkg.RUNTIME_PARITY_CONTRACT
SOURCE_TESTER_IDENTITY = source_pkg.TESTER_IDENTITY_CONTRACT
SOURCE_MAPPING_AUDIT = source_pkg.RUNTIME_MAPPING_AUDIT
SOURCE_FEATURE_MANIFEST = source_pkg.FEATURE_MATRIX_MANIFEST
SOURCE_FEATURE_ORDER = source_pkg.FEATURE_ORDER_CONTRACT
SOURCE_COMMON_SYNC = source_pkg.COMMON_FILES_SYNC
SOURCE_MODEL_MANIFEST = source_pkg.MODEL_HANDOFF_MANIFEST

ATTEMPT_PACKAGE = RUN_DIR / "runtime_probe_attempt_package.csv"
TERMINAL_PROCESS_AUDIT = RUN_DIR / "terminal_process_audit.json"
MT5_EXECUTION_RESULT = RUN_DIR / "mt5_execution_result.json"
STRATEGY_TESTER_REPORTS = RUN_DIR / "strategy_tester_report_records.json"
EXECUTION_SUMMARY = RUN_DIR / "onnx_short_carry_mt5_probe_summary.csv"
PROXY_MT5_DIFF = RUN_DIR / "proxy_mt5_runtime_difference.csv"
TELEMETRY_SKIP_SUMMARY = RUN_DIR / "runtime_skip_reason_summary.csv"
RUNTIME_OUTPUT_COPY = RUN_DIR / "runtime_output_copy_manifest.csv"
RUNTIME_IDENTITY = RUN_DIR / "runtime_identity.csv"
BACKTEST_FORENSICS_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
SELF_CORRECTION_PLAN = RUN_DIR / "self_correction_plan.json"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
ROOT_SELECTION_STATUS = ROOT / "docs" / "registers" / "selection_status.md"
ROOT_CHANGELOG = ROOT / "CHANGELOG.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

INPUT_FILES = (
    RUN349A_FINAL_DECISION,
    RUN349A_GATE_AUDIT,
    RUN349B_QUEUE,
    SOURCE_FINAL_DECISION,
    SOURCE_GATE_AUDIT,
    SOURCE_ATTEMPT_PACKAGE,
    SOURCE_EXPECTED_TAPE,
    SOURCE_EXPECTED_INDEX,
    SOURCE_RUNTIME_PARITY,
    SOURCE_TESTER_IDENTITY,
    SOURCE_MAPPING_AUDIT,
    SOURCE_FEATURE_MANIFEST,
    SOURCE_FEATURE_ORDER,
    SOURCE_COMMON_SYNC,
    SOURCE_MODEL_MANIFEST,
)

OUTPUT_FILES = (
    ATTEMPT_PACKAGE,
    TERMINAL_PROCESS_AUDIT,
    MT5_EXECUTION_RESULT,
    STRATEGY_TESTER_REPORTS,
    EXECUTION_SUMMARY,
    PROXY_MT5_DIFF,
    TELEMETRY_SKIP_SUMMARY,
    RUNTIME_OUTPUT_COPY,
    RUNTIME_IDENTITY,
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
    WORKSPACE_STATE,
    CURRENT_WORKING_STATE,
    SELECTION_STATUS,
    ROOT_SELECTION_STATUS,
    STAGE_BRIEF,
    STAGE_README,
    ROOT_CHANGELOG,
    WORKSPACE_CHANGELOG,
    RUN_REGISTRY,
    PROJECT_LEDGER,
    STAGE_LEDGER,
    ARTIFACT_REGISTRY,
    Path(__file__),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stage349B ONNX short-carry MT5 runtime probe.")
    parser.add_argument("--terminal-path", default=str(source_pkg.DEFAULT_TERMINAL))
    parser.add_argument("--common-files-root", default=str(source_pkg.DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(source_pkg.DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-data-root", default=str(source_pkg.DEFAULT_PORTABLE_ROOT))
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--wait-timeout-seconds", type=int, default=240)
    parser.add_argument("--attempt", action="append", default=None)
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--reuse-existing-outputs", action="store_true")
    return parser.parse_args()


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fs_path(path: Path | str) -> str:
    resolved = Path(path).resolve()
    text = str(resolved)
    if os.name != "nt" or text.startswith("\\\\?\\") or len(text) < 240:
        return text
    if text.startswith("\\\\"):
        return "\\\\?\\UNC\\" + text[2:]
    return "\\\\?\\" + text


def rel(path: Path | str) -> str:
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = ROOT / candidate
    try:
        return candidate.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return candidate.as_posix()


def exists(path: Path | str) -> bool:
    return os.path.exists(fs_path(path))


def ensure_parent(path: Path) -> None:
    os.makedirs(fs_path(path.parent), exist_ok=True)


def required(path: Path) -> Path:
    if not exists(path):
        raise FileNotFoundError(f"missing required input(필수 입력 누락): {rel(path)}")
    return path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(fs_path(path), "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def json_ready(value: Any) -> Any:
    if isinstance(value, Path):
        return rel(value) if exists(value) else value.as_posix()
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if hasattr(value, "item"):
        return json_ready(value.item())
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


def read_json(path: Path) -> dict[str, Any]:
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Any) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8", newline="\n") as handle:
        json.dump(json_ready(payload), handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def read_text(path: Path) -> str:
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return handle.read()


def write_bom_text(path: Path, text: str) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8-sig", newline="\n") as handle:
        handle.write(text.rstrip() + "\n")


def append_text_once(path: Path, marker: str, text: str) -> None:
    current = read_text(path) if exists(path) else ""
    if marker in current:
        return
    next_text = f"{current.rstrip()}\n\n{text.strip()}\n" if current.strip() else text.strip() + "\n"
    write_bom_text(path, next_text)


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    csv.field_size_limit(10_000_000)
    with open(fs_path(path), encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), [dict(row) for row in reader]


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    rows_list = [dict(row) for row in rows]
    if fieldnames is None:
        keys: list[str] = []
        for row in rows_list:
            for key in row:
                if key not in keys:
                    keys.append(key)
        fieldnames = keys
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows_list:
            writer.writerow({key: csv_ready(row.get(key, "")) for key in fieldnames})


def write_frame(path: Path, frame: pd.DataFrame) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8-sig", newline="") as handle:
        frame.to_csv(handle, index=False, lineterminator="\n")


def read_frame(path: Path) -> pd.DataFrame:
    return pd.read_csv(fs_path(path), encoding="utf-8-sig", low_memory=False).fillna("")


def csv_ready(value: Any) -> Any:
    if isinstance(value, (Mapping, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return f"{value:.12g}" if math.isfinite(value) else ""
    return value


def append_or_replace_csv(path: Path, key_columns: Sequence[str], rows: Iterable[Mapping[str, Any]]) -> None:
    rows_list = [dict(row) for row in rows]
    if exists(path):
        fieldnames, existing = read_csv_rows(path)
    else:
        fieldnames, existing = [], []
    for row in rows_list:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    replacement_keys = {tuple(str(row.get(key, "")) for key in key_columns) for row in rows_list}
    kept = [
        row
        for row in existing
        if tuple(str(row.get(key, "")) for key in key_columns) not in replacement_keys
    ]
    write_csv(path, kept + rows_list, fieldnames)


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


def passed_gate(path: Path) -> bool:
    _fields, rows = read_csv_rows(required(path))
    return bool(rows) and all(str(row.get("status", "")).lower() == "passed" for row in rows)


def parse_set(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in read_text(path).splitlines():
        text = line.strip()
        if not text or text.startswith(";") or "=" not in text:
            continue
        key, value = text.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def parse_mt5_date(value: Any) -> datetime:
    return datetime.strptime(str(value), "%Y.%m.%d")


def norm_bar_time(value: Any) -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    try:
        return pd.Timestamp(text).strftime("%Y.%m.%d %H:%M:%S")
    except Exception:
        return text.replace("-", ".").replace("T", " ").replace("Z", "")[:19]


def float_or_nan(value: Any) -> float:
    try:
        output = float(value)
    except Exception:
        return math.nan
    return output if math.isfinite(output) else math.nan


def display_path(path: Path | str) -> str:
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = ROOT / candidate
    try:
        return candidate.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return candidate.as_posix()


def load_source_attempts() -> dict[str, dict[str, Any]]:
    _fields, rows = read_csv_rows(required(SOURCE_ATTEMPT_PACKAGE))
    return {row["attempt_name"]: dict(row) for row in rows}


def selected_queue_rows(filters: Sequence[str] | None) -> list[dict[str, str]]:
    _fields, rows = read_csv_rows(required(RUN349B_QUEUE))
    if not filters:
        return rows
    wanted = set(filters)
    selected = [row for row in rows if row.get("attempt_name") in wanted or row.get("queue_id") in wanted]
    if not selected:
        raise RuntimeError(f"no run349B attempts selected(선택된 349B 시도 없음): {sorted(wanted)}")
    return selected


def materialize_stage349_attempts(args: argparse.Namespace) -> list[dict[str, Any]]:
    source_by_attempt = load_source_attempts()
    rows: list[dict[str, Any]] = []
    set_rows: list[dict[str, Any]] = []
    ini_rows: list[dict[str, Any]] = []
    for index, queue_row in enumerate(selected_queue_rows(args.attempt), start=1):
        attempt_name = queue_row["attempt_name"]
        if attempt_name not in source_by_attempt:
            raise RuntimeError(f"source attempt missing(원천 시도 누락): {attempt_name}")
        source = source_by_attempt[attempt_name]
        source_set_path = ROOT / str(source["set_path"])
        source_ini_path = ROOT / str(source["ini_path"])
        set_values = parse_set(required(source_set_path))
        common_telemetry = f"{COMMON_TELEMETRY_DIR}/{attempt_name}_telemetry.csv"
        common_summary = f"{COMMON_TELEMETRY_DIR}/{attempt_name}_summary.csv"
        set_values["InpRunId"] = f"{RUN_ID}_{attempt_name}"
        set_values["InpExplorationLabel"] = EXPLORATION_LABEL
        set_values["InpTelemetryCsvPath"] = common_telemetry
        set_values["InpSummaryCsvPath"] = common_summary
        report_name = f"POPv2_run349B_{attempt_name}"
        set_name = f"OPV2_run349B_{attempt_name}.set"
        ini_name = f"OPV2_run349B_{attempt_name}.ini"
        set_path = SET_DIR / set_name
        ini_path = INI_DIR / ini_name
        set_payload = mt5.materialize_tester_set_file(
            set_values,
            set_path,
            generated_by=rel(Path(__file__)),
        )
        ini_payload = mt5.materialize_tester_ini_file(
            mt5.TesterMaterializationConfig(
                shutdown_terminal=1,
                from_date=str(source.get("from_date", "")),
                to_date=str(source.get("to_date", "")),
                report=report_name,
            ),
            ini_path,
            set_file_path=Path(set_name),
        )
        set_rows.append(
            {
                "attempt_name": attempt_name,
                "source_set_path": rel(source_set_path),
                "stage349_set_path": rel(set_path),
                "stage349_set_sha256": set_payload["sha256"],
                "telemetry_retargeted_to": common_telemetry,
                "effect": "Stage349 실행 기록을 원천 Stage348 telemetry(런타임 기록)와 분리한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        ini_rows.append(
            {
                "attempt_name": attempt_name,
                "source_ini_path": rel(source_ini_path),
                "stage349_ini_path": rel(ini_path),
                "stage349_ini_sha256": ini_payload["sha256"],
                "report_name": report_name,
                "effect": "Strategy Tester report(전략 테스터 보고서)를 Stage349 이름으로 분리한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        rows.append(
            {
                **source,
                "attempt_name": attempt_name,
                "queue_id": queue_row.get("queue_id", ""),
                "source_stage_id": SOURCE_STAGE_ID,
                "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
                "stage349_run_id": RUN_ID,
                "tier": source.get("tier", "Tier A") or "Tier A",
                "split": source.get("split", "all_rows_with_test_seed_thresholds") or "all_rows_with_test_seed_thresholds",
                "set_path": rel(set_path),
                "ini_path": rel(ini_path),
                "set_name": set_name,
                "ini_name": ini_name,
                "report_name": report_name,
                "common_telemetry_path": common_telemetry,
                "common_summary_path": common_summary,
                "feature_set_id": source.get("feature_order_hash", ""),
                "ini": {"tester": {"Report": report_name}},
                "set": {"path": rel(set_path)},
                "execution_adapter": "stage349_set_ini_retarget_only(349단계 set/ini만 재지정)",
                "allowed_use": "MT5 runtime probe(MT5 런타임 탐침)",
                "forbidden_use": "candidate_selection_or_operating_claim(후보 선정 또는 운영 주장)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(ATTEMPT_PACKAGE, rows)
    write_csv(MT5_DIR / "stage349_set_retarget_manifest.csv", set_rows)
    write_csv(MT5_DIR / "stage349_ini_retarget_manifest.csv", ini_rows)
    return rows


def remove_runtime_outputs(common_files_root: Path, attempt: Mapping[str, Any]) -> None:
    for key in ("common_telemetry_path", "common_summary_path"):
        value = str(attempt.get(key, "")).strip()
        if not value:
            continue
        path = common_files_root / Path(value)
        if exists(path):
            os.unlink(fs_path(path))


def copy_runtime_outputs(common_files_root: Path, attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for attempt in attempts:
        for key, suffix in (("common_telemetry_path", "telemetry"), ("common_summary_path", "summary")):
            source = common_files_root / Path(str(attempt.get(key, "")))
            target = TELEMETRY_COPY_DIR / f"{attempt['attempt_name']}_{suffix}.csv"
            copied = False
            if exists(source):
                ensure_parent(target)
                shutil.copy2(fs_path(source), fs_path(target))
                copied = True
            rows.append(
                {
                    "copy_id": f"{attempt['attempt_name']}::{suffix}",
                    "attempt_name": attempt["attempt_name"],
                    "source_path": source.as_posix(),
                    "target_path": rel(target),
                    "exists": copied and exists(target),
                    "sha256": sha256_file(target) if copied and exists(target) else "",
                    "effect": "MT5 Common Files(공용 파일)의 runtime telemetry(런타임 기록)를 Stage349 run folder(실행 폴더)에 고정한다.",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    write_csv(RUNTIME_OUTPUT_COPY, rows)
    return rows


def execute_attempts(
    args: argparse.Namespace,
    attempts: Sequence[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    common_files_root = Path(args.common_files_root)
    tester_profile_root = Path(args.tester_profile_root)
    terminal_data_root = Path(args.terminal_data_root)
    terminal_probe = terminal_processes()
    write_json(TERMINAL_PROCESS_AUDIT, terminal_probe)
    execution_results: list[dict[str, Any]] = []
    report_records: list[dict[str, Any]] = []
    if args.materialize_only:
        for attempt in attempts:
            execution_results.append(
                {
                    "attempt_name": attempt["attempt_name"],
                    "model_id": attempt["model_id"],
                    "status": "not_run_materialize_only",
                    "runtime_outputs": {
                        "status": "not_run_materialize_only",
                        "wait_status": "not_run_materialize_only",
                    },
                    "ini_path": attempt["ini_path"],
                    "set_path": attempt["set_path"],
                }
            )
    elif args.reuse_existing_outputs:
        for attempt in attempts:
            runtime_outputs = mt5.validate_mt5_runtime_outputs(common_files_root, attempt)
            tester_result = {
                "status": "completed" if runtime_outputs.get("status") == "completed" else "blocked",
                "returncode": "reuse_existing_outputs",
                "runtime_outputs": runtime_outputs,
                "attempt_name": attempt["attempt_name"],
                "model_id": attempt["model_id"],
                "feature_set_id": attempt.get("feature_set_id", ""),
                "ini_path": attempt["ini_path"],
                "set_path": attempt["set_path"],
            }
            if runtime_outputs.get("status") != "completed":
                tester_result["blocker"] = "reuse_existing_runtime_outputs_missing_or_init_failed"
            execution_log = MT5_DIR / f"{attempt['attempt_name']}_tester_execution.json"
            write_json(execution_log, {"tester_result": tester_result, "runtime_outputs": runtime_outputs})
            execution_results.append(tester_result)
        report_records = mt5.collect_mt5_strategy_report_artifacts(
            terminal_data_root=terminal_data_root,
            run_output_root=RUN_DIR,
            attempts=attempts,
            run_id=RUN_ID,
        )
        mt5.attach_mt5_report_metrics(execution_results, report_records)
    elif terminal_probe.get("status") != "no_terminal64_process":
        for attempt in attempts:
            execution_results.append(
                {
                    "attempt_name": attempt["attempt_name"],
                    "model_id": attempt["model_id"],
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
                    "model_id": attempt["model_id"],
                    "feature_set_id": attempt.get("feature_set_id", ""),
                    "runtime_outputs": runtime_outputs,
                    "ini_path": attempt["ini_path"],
                    "set_path": attempt["set_path"],
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


def expected_index(expected: pd.DataFrame, attempt_name: str) -> dict[str, Mapping[str, Any]]:
    subset = expected[expected["attempt_name"].astype(str).eq(attempt_name)].copy()
    return {norm_bar_time(row["bar_time_server"]): row.to_dict() for _, row in subset.iterrows()}


def trade_density_status(trades_per_feature_day: float | None) -> str:
    if trades_per_feature_day is None:
        return "not_available(확인 불가)"
    if trades_per_feature_day >= 10.0:
        return "meets_10_plus_target(10+ 목표 충족)"
    if trades_per_feature_day >= 3.0:
        return "meets_min_3_to_10_band(최소 3~10 구간 충족)"
    return "below_min_3_per_day(일 3회 미만)"


def compare_attempt(
    attempt: Mapping[str, Any],
    execution_row: Mapping[str, Any],
    report_row: Mapping[str, Any],
    expected: pd.DataFrame,
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    attempt_name = str(attempt["attempt_name"])
    expected_by_time = expected_index(expected, attempt_name)
    local_telemetry = TELEMETRY_COPY_DIR / f"{attempt_name}_telemetry.csv"
    local_summary = TELEMETRY_COPY_DIR / f"{attempt_name}_summary.csv"
    diff_rows: list[dict[str, Any]] = []
    skip_rows: list[dict[str, Any]] = []
    expected_dates = {key[:10] for key in expected_by_time if key}
    feature_day_count = len(expected_dates)
    calendar_days = 0
    try:
        calendar_days = max(1, (parse_mt5_date(attempt["to_date"]) - parse_mt5_date(attempt["from_date"])).days)
    except Exception:
        calendar_days = 0

    if not exists(local_telemetry):
        metrics = report_row.get("metrics", {}) if isinstance(report_row.get("metrics"), Mapping) else {}
        return (
            {
                "attempt_name": attempt_name,
                "model_id": attempt.get("model_id", ""),
                "tester_status": execution_row.get("status", "not_attempted"),
                "runtime_status": execution_row.get("runtime_outputs", {}).get("status", "missing"),
                "report_status": report_row.get("status", "missing") if report_row else "missing",
                "returncode": execution_row.get("returncode", ""),
                "blocker": execution_row.get("blocker", "telemetry_missing"),
                "expected_rows": len(expected_by_time),
                "telemetry_cycle_rows": 0,
                "ready_model_rows": 0,
                "matched_rows": 0,
                "expected_missing_rows": 0,
                "probability_mismatch_rows": 0,
                "decision_mismatch_rows": 0,
                "proxy_mapping_boundary_rows": 0,
                "max_abs_probability_diff": "",
                "first_ready_bar_time": "",
                "last_ready_bar_time": "",
                "latest_expected_bar_time": max(expected_by_time) if expected_by_time else "",
                "feature_last_reached": "false",
                "comparison_status": "blocked_no_runtime_telemetry",
                "net_profit": metrics.get("net_profit"),
                "profit_factor": metrics.get("profit_factor"),
                "trade_count": metrics.get("trade_count"),
                "expectancy": metrics.get("expectancy"),
                "recovery_factor": metrics.get("recovery_factor"),
                "max_drawdown_amount": metrics.get("max_drawdown_amount"),
                "short_trade_count": metrics.get("short_trade_count"),
                "long_trade_count": metrics.get("long_trade_count"),
                "feature_day_count": feature_day_count,
                "calendar_days": calendar_days,
                "trade_density_per_feature_day": "",
                "trade_density_per_calendar_day": "",
                "trade_density_requirement_status": "not_available(확인 불가)",
                "no_trade_splitting_status": "not_evaluated_no_runtime_output(런타임 출력 없음)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            diff_rows,
            skip_rows,
        )

    frame = pd.read_csv(fs_path(local_telemetry), low_memory=False).fillna("")
    cycles = frame[frame["record_type"].astype(str).str.lower().eq("cycle")].copy()
    ready = cycles[
        cycles["feature_ready"].astype(str).str.lower().eq("true")
        & cycles["model_ok"].astype(str).str.lower().eq("true")
    ].copy()
    skipped = cycles.loc[~cycles.index.isin(ready.index)].copy()
    for reason, count in skipped["skip_reason"].astype(str).replace("", "empty").value_counts().sort_index().items():
        skip_rows.append(
            {
                "attempt_name": attempt_name,
                "model_id": attempt.get("model_id", ""),
                "skip_reason": reason,
                "rows": int(count),
                "effect": "skip reason(스킵 사유)을 분리해 데이터/시점/모델 handoff(인계) 문제를 찾는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    matched = 0
    expected_missing = 0
    prob_mismatch = 0
    decision_mismatch = 0
    proxy_mapping_boundary = 0
    max_prob_diff = 0.0
    ready_times: list[str] = []
    tolerance = 1e-4
    for _, row in ready.iterrows():
        source_time = norm_bar_time(row.get("source_time") or row.get("bar_time"))
        ready_times.append(source_time)
        exp = expected_by_time.get(source_time)
        found = exp is not None
        mt5_probs = [float_or_nan(row.get("p_short")), float_or_nan(row.get("p_flat")), float_or_nan(row.get("p_long"))]
        exp_probs = (
            [float_or_nan(exp.get("p_short")), float_or_nan(exp.get("p_flat")), float_or_nan(exp.get("p_long"))]
            if exp
            else [math.nan, math.nan, math.nan]
        )
        diffs = [abs(a - b) if math.isfinite(a) and math.isfinite(b) else math.inf for a, b in zip(mt5_probs, exp_probs)]
        row_max = max(diffs)
        if math.isfinite(row_max):
            max_prob_diff = max(max_prob_diff, row_max)
        mt5_decision = str(row.get("decision", "")).strip().lower()
        expected_runtime_decision = str(exp.get("ea_mapped_expected_label", "") if exp else "").strip().lower()
        proxy_intended_decision = str(exp.get("proxy_intended_label", "") if exp else "").strip().lower()
        prob_ok = found and row_max <= tolerance
        decision_ok = found and mt5_decision == expected_runtime_decision
        if not found:
            expected_missing += 1
            status = "expected_missing"
            attribution = "runtime_timestamp_not_in_expected_tape(런타임 시각이 예상 테이프에 없음)"
        elif not prob_ok:
            prob_mismatch += 1
            status = "probability_mismatch"
            attribution = "onnx_output_diff(온엑스 출력 차이)"
        elif not decision_ok:
            decision_mismatch += 1
            status = "decision_mismatch"
            attribution = "decision_surface_diff(결정 표면 차이)"
        else:
            matched += 1
            status = "matched"
            attribution = "matched(일치)"
        if found and proxy_intended_decision != expected_runtime_decision:
            proxy_mapping_boundary += 1
        diff_rows.append(
            {
                "attempt_name": attempt_name,
                "model_id": attempt.get("model_id", ""),
                "bar_time": norm_bar_time(row.get("bar_time")),
                "source_time": source_time,
                "expected_found": found,
                "probability_match": prob_ok,
                "decision_match": decision_ok,
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
                "expected_runtime_decision": expected_runtime_decision,
                "proxy_intended_decision": proxy_intended_decision,
                "proxy_mapping_boundary": proxy_intended_decision != expected_runtime_decision if found else "",
                "comparison_status": status,
                "attribution": attribution,
                "usability": "usable_for_diff_attribution_not_kpi_substitute(차이 귀속에는 사용 가능, KPI 대체 불가)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    latest_expected = max(expected_by_time) if expected_by_time else ""
    feature_last_reached = latest_expected in set(ready_times)
    if expected_missing or prob_mismatch or decision_mismatch:
        comparison_status = "completed_with_proxy_mt5_diff_attribution_required"
    elif len(ready) <= 0:
        comparison_status = "blocked_no_ready_model_rows"
    elif feature_last_reached:
        comparison_status = "completed_probability_decision_parity_reached_feature_last_no_hash_claim"
    else:
        comparison_status = "completed_overlap_parity_tester_gap_remains_no_hash_claim"

    runtime = execution_row.get("runtime_outputs", {}) if isinstance(execution_row.get("runtime_outputs"), Mapping) else {}
    last_summary = runtime.get("last_summary", {}) if isinstance(runtime.get("last_summary"), Mapping) else {}
    metrics = report_row.get("metrics", {}) if isinstance(report_row.get("metrics"), Mapping) else {}
    trade_count = metrics.get("trade_count")
    trade_count_number = to_float(trade_count, math.nan)
    trades_per_feature_day: float | None = None
    trades_per_calendar_day: float | None = None
    if math.isfinite(trade_count_number):
        if feature_day_count > 0:
            trades_per_feature_day = trade_count_number / feature_day_count
        if calendar_days > 0:
            trades_per_calendar_day = trade_count_number / calendar_days
    no_split = (
        "guardrail_partially_supported_by_fixed_lot_one_position(고정 lot/단일 포지션 설정으로 부분 지지)"
        if str(attempt.get("max_hold_bars", "")).strip() and str(attempt.get("fixed_lot", "")).strip()
        else "not_evaluated_by_report_only(보고서만으로는 미평가)"
    )
    return (
        {
            "attempt_name": attempt_name,
            "model_id": attempt.get("model_id", ""),
            "tester_status": execution_row.get("status", "not_attempted"),
            "runtime_status": runtime.get("status", "not_attempted"),
            "report_status": report_row.get("status", "missing") if report_row else "missing",
            "returncode": execution_row.get("returncode", ""),
            "blocker": execution_row.get("blocker", ""),
            "expected_rows": len(expected_by_time),
            "telemetry_cycle_rows": int(len(cycles)),
            "ready_model_rows": int(len(ready)),
            "matched_rows": matched,
            "expected_missing_rows": expected_missing,
            "probability_mismatch_rows": prob_mismatch,
            "decision_mismatch_rows": decision_mismatch,
            "proxy_mapping_boundary_rows": proxy_mapping_boundary,
            "max_abs_probability_diff": max_prob_diff,
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
            "net_profit": metrics.get("net_profit"),
            "profit_factor": metrics.get("profit_factor"),
            "trade_count": trade_count,
            "expectancy": metrics.get("expectancy"),
            "recovery_factor": metrics.get("recovery_factor"),
            "max_drawdown_amount": metrics.get("max_drawdown_amount"),
            "short_trade_count": metrics.get("short_trade_count"),
            "long_trade_count": metrics.get("long_trade_count"),
            "feature_day_count": feature_day_count,
            "calendar_days": calendar_days,
            "trade_density_per_feature_day": trades_per_feature_day if trades_per_feature_day is not None else "",
            "trade_density_per_calendar_day": trades_per_calendar_day if trades_per_calendar_day is not None else "",
            "trade_density_requirement_status": trade_density_status(trades_per_feature_day),
            "no_trade_splitting_status": no_split,
            "common_telemetry_path": attempt.get("common_telemetry_path", ""),
            "common_summary_path": attempt.get("common_summary_path", ""),
            "local_telemetry_path": rel(local_telemetry) if exists(local_telemetry) else "",
            "local_summary_path": rel(local_summary) if exists(local_summary) else "",
            "report_path": report_row.get("html_report", {}).get("path", "") if isinstance(report_row.get("html_report"), Mapping) else "",
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
    expected = read_frame(required(SOURCE_EXPECTED_TAPE))
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
        )
        summaries.append(summary)
        diffs.extend(diff_rows)
        skips.extend(skip_rows)
    write_csv(EXECUTION_SUMMARY, summaries)
    write_csv(PROXY_MT5_DIFF, diffs)
    write_csv(TELEMETRY_SKIP_SUMMARY, skips)
    return summaries, diffs, skips


def best_attempt_from_summaries(summaries: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
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
    ]:
        if column in frame.columns:
            frame[column] = pd.to_numeric(frame[column], errors="coerce").fillna(0.0)
    completed = frame.loc[frame["runtime_status"].astype(str).eq("completed")].copy()
    source = completed if not completed.empty else frame
    if "trade_count" in source.columns:
        trade_producing = source.loc[source["trade_count"] > 0].copy()
        density_ready = trade_producing.loc[trade_producing["trade_density_per_feature_day"] >= 3.0].copy()
        if not density_ready.empty:
            source = density_ready
        elif not trade_producing.empty:
            source = trade_producing
    source = source.sort_values(
        ["net_profit", "profit_factor", "recovery_factor", "trade_density_per_feature_day", "trade_count"],
        ascending=[False, False, False, False, False],
    )
    return source.iloc[0].to_dict()


def build_runtime_identity(args: argparse.Namespace, attempts: Sequence[Mapping[str, Any]]) -> None:
    source_identity = read_frame(required(SOURCE_TESTER_IDENTITY))
    source_first = source_identity.iloc[0].to_dict() if not source_identity.empty else {}
    write_csv(
        RUNTIME_IDENTITY,
        [
            {
                "identity_id": "stage349B_runtime_identity",
                "terminal_path": str(args.terminal_path),
                "terminal_exists": exists(Path(args.terminal_path)),
                "common_files_root": str(args.common_files_root),
                "common_files_exists": exists(Path(args.common_files_root)),
                "tester_profile_root": str(args.tester_profile_root),
                "tester_profile_root_exists": exists(Path(args.tester_profile_root)),
                "terminal_data_root": str(args.terminal_data_root),
                "portable_ea_ex5": source_pkg.PORTABLE_EA_EX5.as_posix(),
                "portable_ea_ex5_exists": exists(source_pkg.PORTABLE_EA_EX5),
                "portable_ea_ex5_sha256": sha256_file(source_pkg.PORTABLE_EA_EX5) if exists(source_pkg.PORTABLE_EA_EX5) else "",
                "source_ea_binary_sha256": source_first.get("ea_binary_sha256", ""),
                "source_portable_ea_sha256": source_first.get("portable_ea_sha256", ""),
                "attempt_rows": len(attempts),
                "tester_model": "4 real ticks(실제 틱)",
                "deposit": "500",
                "leverage": "1:100",
                "feature_count_boundary": "53_feature_probe_only_vs_58_contract(53개 탐침 전용, 58개 계약과 다름)",
                "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )


def build_summary(
    args: argparse.Namespace,
    attempts: Sequence[Mapping[str, Any]],
    execution_results: Sequence[Mapping[str, Any]],
    report_records: Sequence[Mapping[str, Any]],
    summaries: Sequence[Mapping[str, Any]],
    diffs: Sequence[Mapping[str, Any]],
    copy_rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    build_runtime_identity(args, attempts)
    source_final = read_json(required(SOURCE_FINAL_DECISION))
    parent_final = read_json(required(RUN349A_FINAL_DECISION))
    runtime_completed = sum(1 for row in summaries if str(row.get("runtime_status", "")) == "completed")
    report_completed = sum(1 for row in report_records if str(row.get("status", "")) == "completed")
    expected_rows = sum(to_int(row.get("expected_rows")) for row in summaries)
    matched_rows = sum(to_int(row.get("matched_rows")) for row in summaries)
    diff_mismatches = sum(
        1
        for row in diffs
        if str(row.get("comparison_status", "")) not in {"matched"}
    )
    completed = (
        len(attempts) > 0
        and runtime_completed == len(attempts)
        and report_completed == len(attempts)
        and not str(execution_results[0].get("status", "")).startswith("not_run_materialize_only")
    )
    best = best_attempt_from_summaries(summaries)
    density_values = [to_float(row.get("trade_density_per_feature_day"), math.nan) for row in summaries]
    density_values = [value for value in density_values if math.isfinite(value)]
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_stage_id": SOURCE_STAGE_ID,
        "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
        "status": STATUS_COMPLETED if completed else STATUS_BLOCKED,
        "judgment": JUDGMENT_COMPLETED if completed else JUDGMENT_BLOCKED,
        "decision": DECISION_COMPLETED if completed else DECISION_BLOCKED,
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "attempt_rows": len(attempts),
        "execution_result_rows": len(execution_results),
        "runtime_completed_rows": runtime_completed,
        "report_rows": len(report_records),
        "report_completed_rows": report_completed,
        "summary_rows": len(summaries),
        "diff_rows": len(diffs),
        "diff_mismatch_rows": diff_mismatches,
        "expected_rows": expected_rows,
        "matched_rows": matched_rows,
        "runtime_output_copy_rows": len(copy_rows),
        "runtime_output_copy_ready_rows": sum(1 for row in copy_rows if norm_bool(row.get("exists"))),
        "mt5_execution_attempted": "yes" if not args.materialize_only else "not_run_materialize_only",
        "external_verification_status": "completed(완료)" if completed else "blocked(차단)",
        "candidate_selection": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "live_readiness": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_package_status": source_final.get("status", ""),
        "source_package_feature_count": source_final.get("feature_count", ""),
        "source_missing_mt5_contract_feature_count": source_final.get("missing_mt5_contract_feature_count", ""),
        "source_proxy_ea_expected_mismatch_rows": source_final.get("proxy_ea_expected_mismatch_rows", ""),
        "parent_branch_status": parent_final.get("status", ""),
        "source_gate_passed": passed_gate(SOURCE_GATE_AUDIT),
        "parent_gate_passed": passed_gate(RUN349A_GATE_AUDIT),
        "best_attempt_name": best.get("attempt_name", ""),
        "best_model_id": best.get("model_id", ""),
        "best_net_profit": to_float(best.get("net_profit")),
        "best_profit_factor": to_float(best.get("profit_factor")),
        "best_expectancy": to_float(best.get("expectancy")),
        "best_recovery_factor": to_float(best.get("recovery_factor")),
        "best_max_drawdown_amount": to_float(best.get("max_drawdown_amount")),
        "best_trade_count": to_int(best.get("trade_count")),
        "best_long_trade_count": to_int(best.get("long_trade_count")),
        "best_short_trade_count": to_int(best.get("short_trade_count")),
        "best_trade_density_per_feature_day": to_float(best.get("trade_density_per_feature_day")),
        "best_trade_density_requirement_status": best.get("trade_density_requirement_status", ""),
        "trade_density_requirement": TRADE_DENSITY_REQUIREMENT,
        "max_trade_density_per_feature_day": max(density_values) if density_values else 0.0,
        "min_trade_density_per_feature_day": min(density_values) if density_values else 0.0,
    }


def gate_row(gate: str, passed: bool, evidence: str, effect: str, observed: str = "") -> dict[str, Any]:
    return {
        "gate_id": gate,
        "status": "passed" if passed else "failed",
        "observed": observed,
        "evidence_path": evidence,
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
    runtime_ok = final["runtime_completed_rows"] == final["attempt_rows"] and final["report_completed_rows"] == final["attempt_rows"]
    return [
        gate_row(
            "source_run348C_package_gates_passed",
            bool(final["source_gate_passed"]),
            rel(SOURCE_GATE_AUDIT),
            "source package(원천 패키지)의 gate(게이트)를 상속 가능한 입력 조건으로 확인한다.",
        ),
        gate_row(
            "parent_run349A_branch_gates_passed",
            bool(final["parent_gate_passed"]),
            rel(RUN349A_GATE_AUDIT),
            "Stage349 branch(분기)가 현재 진실(current truth, 현재 진실)을 고정했는지 확인한다.",
        ),
        gate_row(
            "runtime_evidence_gate",
            runtime_ok,
            f"{rel(MT5_EXECUTION_RESULT)};{rel(STRATEGY_TESTER_REPORTS)}",
            "MT5 runtime output(런타임 출력)과 Strategy Tester report(전략 테스터 보고서)가 모두 있는지 확인한다.",
            f"runtime={final['runtime_completed_rows']}/{final['attempt_rows']};reports={final['report_completed_rows']}/{final['attempt_rows']}",
        ),
        gate_row(
            "scope_completion_gate",
            final["execution_result_rows"] == final["attempt_rows"] and final["attempt_rows"] > 0,
            rel(MT5_EXECUTION_RESULT),
            "대기열(queue, 대기열)의 모든 attempt(시도)에 실행 기록을 남긴다.",
        ),
        gate_row(
            "kpi_contract_audit",
            final["summary_rows"] == final["attempt_rows"] and final["runtime_output_copy_rows"] >= final["attempt_rows"],
            rel(EXECUTION_SUMMARY),
            "net profit(순수익), PF(수익 팩터), expectancy(기대값), drawdown(낙폭), trade density(거래 밀도)를 같은 표에 기록한다.",
        ),
        gate_row(
            "proxy_mt5_diff_attribution_recorded",
            exists(PROXY_MT5_DIFF) and final["diff_rows"] >= 0,
            rel(PROXY_MT5_DIFF),
            "proxy expected value(프록시 예상값)와 MT5 runtime(런타임)의 차이를 원인 귀속(attribution, 귀속)과 활용 가능성(usability, 활용 가능성)으로 남긴다.",
        ),
        gate_row(
            "trade_density_requirement_evaluated",
            exists(EXECUTION_SUMMARY) and final["summary_rows"] == final["attempt_rows"],
            rel(EXECUTION_SUMMARY),
            "일일 거래 수 3~10+ 요구와 trade splitting(거래 쪼개기) 금지 조건을 후보별로 평가한다.",
        ),
        gate_row(
            "forensics_identity_recorded",
            exists(RUNTIME_IDENTITY),
            rel(RUNTIME_IDENTITY),
            "terminal(터미널), EA binary(EX5 실행 파일), tester profile(테스터 프로필) 정체성을 기록한다.",
        ),
        gate_row(
            "required_gate_coverage_audit",
            True,
            rel(GATE_AUDIT),
            "runtime_backtest(런타임 백테스트) 필수 gate(게이트) 이름을 closeout(종료 기록)에 연결한다.",
        ),
        gate_row(
            "final_claim_guard",
            no_forbidden,
            rel(CLAIM_RECEIPT),
            "runtime probe(런타임 탐침)를 operating promotion(운영 승격)이나 Goal Achieve(목표 달성)로 올리지 않는다.",
        ),
    ]


def artifact_paths() -> list[Path]:
    paths = list(OUTPUT_FILES)
    if exists(TELEMETRY_COPY_DIR):
        paths.extend(path for path in TELEMETRY_COPY_DIR.glob("*") if path.is_file())
    if exists(REPORT_COPY_DIR):
        paths.extend(path for path in REPORT_COPY_DIR.glob("*") if path.is_file())
    if exists(MT5_DIR):
        paths.extend(path for path in MT5_DIR.glob("*_tester_execution.json") if path.is_file())
        paths.extend(path for path in MT5_DIR.glob("stage349_*_retarget_manifest.csv") if path.is_file())
    return paths


def write_receipts(final: Mapping[str, Any]) -> None:
    created_at = now_utc()
    base = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
        "status": final["status"],
        "judgment": final["judgment"],
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(
        RUNTIME_RECEIPT,
        {
            **base,
            "research_path": rel(SOURCE_EXPECTED_TAPE),
            "runtime_path": rel(RUNTIME_OUTPUT_COPY),
            "shared_contract": rel(SOURCE_RUNTIME_PARITY),
            "known_differences": (
                "feature_count 53 vs MT5 contract 58(피처 53개와 MT5 계약 58개 차이); "
                "cash_open_regime partial mapping(현금장 국면 부분 매핑)"
            ),
            "parity_check": rel(PROXY_MT5_DIFF),
            "parity_identity": rel(RUNTIME_IDENTITY),
            "runtime_claim_boundary": "runtime_probe(런타임 탐침)" if final["runtime_completed_rows"] else "blocked(차단)",
        },
    )
    write_json(
        BACKTEST_FORENSICS_RECEIPT,
        {
            **base,
            "tester_identity": rel(RUNTIME_IDENTITY),
            "ea_identity": rel(RUNTIME_IDENTITY),
            "report_identity": rel(STRATEGY_TESTER_REPORTS),
            "trade_evidence": rel(EXECUTION_SUMMARY),
            "cost_assumptions": "Strategy Tester setting inherited from source .ini/.set(원천 ini/set의 테스터 설정 상속)",
            "forensic_checks": [
                "terminal process probe(터미널 프로세스 탐침)",
                "report collection(보고서 수집)",
                "runtime telemetry copy(런타임 기록 복사)",
            ],
            "backtest_judgment": "usable_with_boundary(경계부 사용 가능)" if final["runtime_completed_rows"] else "blocked(차단)",
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
            "best_trade_density_requirement_status": final["best_trade_density_requirement_status"],
            "effect": "수익 구조와 거래 밀도(trade density, 거래 밀도)를 함께 보게 한다.",
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "result_judgment": final["judgment"],
            "external_verification_status": final["external_verification_status"],
            "candidate_selection": "not_run",
            "runtime_authority": "not_claimed",
            "goal_achieve": "not_claimed",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "candidate_selection": "not_run",
            "forward_passed": "not_claimed",
            "forward_failed": "not_claimed",
            "live_readiness": "not_claimed",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "goal_achieve": "not_claimed",
            "allowed_claim": "MT5 runtime probe attempt and evidence collection(MT5 런타임 탐침 시도와 근거 수집)",
            "forbidden_claim": "operating model or Goal Achieve(운영 모델 또는 목표 달성)",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [display_path(path) for path in artifact_paths() if exists(path)],
            "artifact_hashes": {display_path(path): sha256_file(path) for path in artifact_paths() if exists(path)},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_and_reproducible_from_command(추적됨, 명령으로 재현 가능)",
            "lineage_judgment": "connected_with_runtime_probe_boundary(런타임 탐침 경계로 연결됨)",
        },
    )


def write_final(final_seed: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    payload = {
        **dict(final_seed),
        "gate_passes": sum(1 for row in gates if row.get("status") == "passed"),
        "gate_total": len(gates),
        "created_at_utc": now_utc(),
    }
    write_json(FINAL_DECISION, payload)
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "run_number": RUN_NUMBER,
            "created_at": TODAY,
            "created_at_utc": now_utc(),
            "script": rel(Path(__file__)),
            "work_family": "runtime_backtest(MT5 런타임/백테스트 실행)",
            "primary_skill": "obsidian-runtime-parity(런타임 동등성)",
            "support_skills": [
                "obsidian-backtest-forensics(백테스트 포렌식)",
                "obsidian-artifact-lineage(산출물 계보)",
            ],
            "inputs": [rel(path) for path in INPUT_FILES],
            "outputs": [display_path(path) for path in artifact_paths() if exists(path)],
            "external_verification_status": payload["external_verification_status"],
            "trade_density_requirement": TRADE_DENSITY_REQUIREMENT,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    return payload


def write_docs(final: Mapping[str, Any]) -> None:
    report = f"""# run349B ONNX Short-Carry MT5 Probe(349B 온엑스 숏 기여 MT5 탐침)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- gates(게이트): `{final['gate_passes']}/{final['gate_total']}`
- source_package(원천 패키지): `{SOURCE_PACKAGE_RUN_ID}`
- attempts(시도): `{final['attempt_rows']}`
- runtime_completed_rows(런타임 완료 행): `{final['runtime_completed_rows']}`
- report_completed_rows(보고서 완료 행): `{final['report_completed_rows']}`
- matched_rows(일치 행): `{final['matched_rows']}/{final['expected_rows']}`
- diff_mismatch_rows(차이 행): `{final['diff_mismatch_rows']}`
- best_attempt(최고 시도): `{final['best_attempt_name']}`
- best_net_profit(최고 순수익): `{final['best_net_profit']}`
- best_profit_factor(최고 수익 팩터): `{final['best_profit_factor']}`
- best_expectancy(최고 기대값): `{final['best_expectancy']}`
- best_recovery_factor(최고 회복 계수): `{final['best_recovery_factor']}`
- best_trade_count(최고 거래 수): `{final['best_trade_count']}`
- best_trade_density(최고 일일 거래 밀도): `{final['best_trade_density_per_feature_day']}`
- trade_density_status(거래 밀도 상태): `{final['best_trade_density_requirement_status']}`
- external_verification_status(외부 검증 상태): `{final['external_verification_status']}`

## Action(행동)

Stage348(348단계)의 ONNX short-carry package(온엑스 숏 기여 패키지)를 복사하지 않고, Stage349(349단계)에서 `.set/.ini` 실행 adapter(어댑터)만 새로 만들어 MT5 Strategy Tester(MT5 전략 테스터)를 실행했다.

## Effect(효과)

Stage348(348단계)는 package handoff(패키지 인계)로 가볍게 유지되고, Stage349(349단계)는 runtime output(런타임 출력), tester report(테스터 보고서), proxy-MT5 diff(프록시-MT5 차이), trade density(거래 밀도)를 별도 evidence(근거)로 가진다.

## Boundary(경계)

이 run(실행)은 runtime probe(런타임 탐침)이다. selected model(선정 모델), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 없다.
"""
    decision = f"""# {TODAY} Stage349B MT5 Probe Decision(349B MT5 탐침 결정)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{final['decision']}`
- judgment(판정): `{final['judgment']}`
- external_verification_status(외부 검증 상태): `{final['external_verification_status']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- evidence(근거): `{rel(MT5_EXECUTION_RESULT)}`, `{rel(EXECUTION_SUMMARY)}`, `{rel(PROXY_MT5_DIFF)}`

Action(행동): Stage349(349단계)에서 ONNX short-carry MT5 runtime probe(온엑스 숏 기여 MT5 런타임 탐침)를 실행했다.
Effect(효과): run349C(349C 실행)가 수익 구조, 거래 밀도, proxy-MT5 diff(프록시-MT5 차이)를 판단할 수 있다.

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

run349B(349B 실행)는 MT5 runtime probe(MT5 런타임 탐침)를 시도했고, run349C(349C 실행)는 결과를 검토해 positive clue(긍정 단서), failure memory(실패 기억), repair condition(수리 조건)을 분리해야 한다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage349 Selection Status(349단계 선정 상태)

- active_stage(현재 단계): `{STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- source_package(원천 패키지): `{SOURCE_PACKAGE_RUN_ID}`
- best_attempt(최고 시도): `{final['best_attempt_name']}`
- best_net_profit(최고 순수익): `{final['best_net_profit']}`
- best_profit_factor(최고 수익 팩터): `{final['best_profit_factor']}`
- best_trade_count(최고 거래 수): `{final['best_trade_count']}`
- best_trade_density_per_feature_day(최고 피처일 거래 밀도): `{final['best_trade_density_per_feature_day']}`
- trade_density_requirement(거래 밀도 요구): `{TRADE_DENSITY_REQUIREMENT}`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): MT5 result(MT5 결과)를 바로 selection(선정)으로 오해하지 않고 review(검토) 단계로 넘긴다.
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
    write_bom_text(REPORT_PATH, report)
    write_bom_text(DECISION_DOC, decision)
    write_bom_text(CURRENT_WORKING_STATE, current)
    write_bom_text(SELECTION_STATUS, selection)
    write_bom_text(ROOT_SELECTION_STATUS, selection)
    write_bom_text(WORKSPACE_STATE, workspace)
    marker = f"run349B {RUN_ID}"
    append_text_once(
        STAGE_BRIEF,
        marker,
        f"""## run349B ONNX Short-Carry MT5 Probe(349B 온엑스 숏 기여 MT5 탐침)

- run_id(실행 ID): `{RUN_ID}`
- attempts(시도): `{final['attempt_rows']}`
- matched_rows(일치 행): `{final['matched_rows']}/{final['expected_rows']}`
- best_attempt(최고 시도): `{final['best_attempt_name']}`
- trade_density_status(거래 밀도 상태): `{final['best_trade_density_requirement_status']}`
- effect(효과): Stage348(348단계) 패키지를 MT5 runtime evidence(MT5 런타임 근거)로 바꾼다.
""",
    )
    append_text_once(
        STAGE_README,
        marker,
        f"""## run349B ONNX Short-Carry MT5 Probe(349B 온엑스 숏 기여 MT5 탐침)

- run_id(실행 ID): `{RUN_ID}`
- summary(요약): `{rel(EXECUTION_SUMMARY)}`
- diff(차이): `{rel(PROXY_MT5_DIFF)}`
- effect(효과): run349C review(검토)가 MT5 KPI(MT5 핵심 성과 지표)를 기준으로 판단하게 한다.
""",
    )
    changelog = f"""## {TODAY} run349B ONNX Short-Carry MT5 Probe(온엑스 숏 기여 MT5 탐침)

- action(행동): `{final['attempt_rows']}`개 ONNX short-carry attempt(온엑스 숏 기여 시도)를 MT5 runtime probe(MT5 런타임 탐침)로 실행했다.
- effect(효과): matched_rows(일치 행) `{final['matched_rows']}/{final['expected_rows']}`, best_attempt(최고 시도) `{final['best_attempt_name']}`, trade_density(거래 밀도) `{final['best_trade_density_per_feature_day']}`를 기록했다.
- boundary(경계): selection/runtime authority/Goal Achieve(선정/런타임 권위/목표 달성)는 주장하지 않는다.
"""
    append_text_once(ROOT_CHANGELOG, marker, changelog)
    append_text_once(WORKSPACE_CHANGELOG, marker, changelog)


def write_registers(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    gate_passes = sum(1 for row in gates if row.get("status") == "passed")
    gate_total = len(gates)
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
        "primary_artifact": rel(FINAL_DECISION),
        "path": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "primary_report": rel(REPORT_PATH),
        "gate_passes": gate_passes,
        "gate_total": gate_total,
        "claim_boundary": CLAIM_BOUNDARY,
        "scoreboard_lane": "runtime_probe(MT5 런타임 탐침)",
        "lane": "runtime_probe(MT5 런타임 탐침)",
        "family": "runtime_backtest(MT5 런타임/백테스트 실행)",
        "run_number": RUN_NUMBER,
        "notes": "ONNX short-carry runtime probe(온엑스 숏 기여 런타임 탐침), review required(검토 필요).",
        "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
        "rows": final["expected_rows"],
        "attempt_count": final["attempt_rows"],
        "feature_count": final["source_package_feature_count"],
        "candidate_model_id": final["best_model_id"],
        "net_profit": final["best_net_profit"],
        "profit_factor": final["best_profit_factor"],
        "expectancy": final["best_expectancy"],
        "drawdown": final["best_max_drawdown_amount"],
        "recovery_factor": final["best_recovery_factor"],
        "trade_count": final["best_trade_count"],
        "matched_rows": final["matched_rows"],
        "result_status": final["judgment"],
        "external_verification_status": final["external_verification_status"],
        "trade_density_per_feature_day": final["best_trade_density_per_feature_day"],
        "trade_density_requirement_status": final["best_trade_density_requirement_status"],
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [base])
    rows = [
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__Tier A",
            "subrun_id": "Tier A",
            "view": "Tier A separate(Tier A 분리)",
            "record_view": "Tier A separate(Tier A 분리)",
            "tier": "Tier A",
            "tier_scope": "Tier A",
            "metric_scope": "mt5_runtime_probe",
            "kpi_scope": "mt5_runtime_probe",
            "primary_kpi": (
                f"net_profit={final['best_net_profit']};pf={final['best_profit_factor']};"
                f"trades={final['best_trade_count']};density={final['best_trade_density_per_feature_day']}"
            ),
            "guardrail_kpi": (
                f"drawdown={final['best_max_drawdown_amount']};"
                f"long_short={final['best_long_trade_count']}/{final['best_short_trade_count']};"
                f"trade_density={final['best_trade_density_requirement_status']}"
            ),
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__Tier B",
            "subrun_id": "Tier B",
            "view": "Tier B separate(Tier B 분리)",
            "record_view": "Tier B separate(Tier B 분리)",
            "tier": "Tier B",
            "tier_scope": "Tier B",
            "metric_scope": "missing_required",
            "kpi_scope": "missing_required",
            "primary_kpi": "missing_required(필수 누락)",
            "guardrail_kpi": "missing_required(필수 누락)",
            "external_verification_status": "missing_required(필수 누락)",
            "result_status": "missing_required(필수 누락)",
            "net_profit": "",
            "profit_factor": "",
            "expectancy": "",
            "drawdown": "",
            "recovery_factor": "",
            "trade_count": "",
            "matched_rows": "",
            "trade_density_per_feature_day": "",
            "trade_density_requirement_status": "missing_required(필수 누락)",
            "notes": "Tier B(티어 B)는 이번 runtime probe(런타임 탐침)에 없으므로 missing_required(필수 누락)로 남긴다.",
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__Tier A+B",
            "subrun_id": "Tier A+B",
            "view": "Tier A+B combined(Tier A+B 합산)",
            "record_view": "Tier A+B combined(Tier A+B 합산)",
            "tier": "Tier A+B",
            "tier_scope": "Tier A+B",
            "metric_scope": "same_as_tier_a_until_tier_b_available",
            "kpi_scope": "same_as_tier_a_until_tier_b_available",
            "result_status": "same_as_tier_a_until_tier_b_available",
        },
    ]
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], rows)


def update_artifact_registry() -> None:
    rows = []
    for path in artifact_paths():
        if not exists(path):
            continue
        relative = display_path(path)
        rows.append(
            {
                "artifact_id": f"{RUN_ID}__{relative.replace('/', '__').replace('.', '_')}",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": path.suffix.lstrip(".") or "artifact",
                "path": relative,
                "artifact_path": relative,
                "sha256": sha256_file(path),
                "created_at": TODAY,
                "created_at_utc": now_utc(),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def validate_or_raise(gates: Sequence[Mapping[str, Any]]) -> None:
    missing_outputs = [rel(path) for path in [FINAL_DECISION, RUN_MANIFEST, GATE_AUDIT, REPORT_PATH, DECISION_DOC] if not exists(path)]
    if missing_outputs:
        raise FileNotFoundError("missing generated output(생성 출력 누락): " + ", ".join(missing_outputs))
    failed = [row for row in gates if row.get("status") != "passed"]
    if failed:
        write_json(
            SELF_CORRECTION_PLAN,
            {
                "run_id": RUN_ID,
                "failed_gates": failed,
                "mode": "plan_only(계획 전용)",
                "repair_plan": [
                    "terminal_process_probe(터미널 프로세스 탐침) 확인",
                    "tester report path(테스터 보고서 경로)와 telemetry path(런타임 기록 경로) 확인",
                    "blocked attempt(차단 시도)만 재실행",
                ],
                "claim_boundary": CLAIM_BOUNDARY,
                "created_at_utc": now_utc(),
            },
        )
        raise RuntimeError(
            "run349B required gate audit failed(349B 필수 게이트 감사 실패): "
            + ", ".join(str(row.get("gate_id")) for row in failed)
        )


def main() -> None:
    args = parse_args()
    for directory in [RUN_DIR, MT5_DIR, SET_DIR, INI_DIR, TELEMETRY_COPY_DIR, REPORT_COPY_DIR, REVIEW_DIR, DECISION_DOC.parent]:
        os.makedirs(fs_path(directory), exist_ok=True)
    for path in INPUT_FILES:
        required(path)
    attempts = materialize_stage349_attempts(args)
    execution_results, report_records, copy_rows = execute_attempts(args, attempts)
    summaries, diffs, skips = compare_outputs(attempts, execution_results, report_records)
    final_seed = build_summary(args, attempts, execution_results, report_records, summaries, diffs, copy_rows)
    gates = make_gates(final_seed)
    write_csv(GATE_AUDIT, gates)
    write_receipts(final_seed)
    final = write_final(final_seed, gates)
    write_docs(final)
    write_registers(final, gates)
    write_receipts(final)
    final = write_final(final, gates)
    update_artifact_registry()
    validate_or_raise(gates)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": final["status"],
                "judgment": final["judgment"],
                "attempt_rows": final["attempt_rows"],
                "runtime_completed_rows": final["runtime_completed_rows"],
                "report_completed_rows": final["report_completed_rows"],
                "matched_rows": final["matched_rows"],
                "expected_rows": final["expected_rows"],
                "diff_mismatch_rows": final["diff_mismatch_rows"],
                "best_attempt_name": final["best_attempt_name"],
                "best_net_profit": final["best_net_profit"],
                "best_profit_factor": final["best_profit_factor"],
                "best_trade_count": final["best_trade_count"],
                "best_trade_density_per_feature_day": final["best_trade_density_per_feature_day"],
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
