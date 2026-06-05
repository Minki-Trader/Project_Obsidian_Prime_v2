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
from stage_pipelines.stage337.execute_model_scout_mt5_runtime_probe_without_db import (  # noqa: E402
    terminal_processes,
)
from stage_pipelines.stage348 import (  # noqa: E402
    materialize_onnx_deployable_short_carry_probe_package_without_db as source_pkg,
)
from stage_pipelines.stage349 import (  # noqa: E402
    review_onnx_short_carry_mt5_probe_without_db as review349c,
)


TODAY = "2026-06-01"
STAGE_ID = "349_onnx_short_carry_runtime__execute_mt5_probe"
SOURCE_STAGE_ID = source_pkg.STAGE_ID
RUN_NUMBER = "run349D"
RUN_ID = "run349D_test_onnx_no_conversion_runtime_parity_diagnostic_without_db_v1"
PARENT_RUN_ID = "run349C_review_onnx_short_carry_mt5_probe_without_db_v1"
SOURCE_RUNTIME_RUN_ID = "run349B_execute_onnx_deployable_short_carry_mt5_probe_without_db_v1"
SOURCE_PACKAGE_RUN_ID = source_pkg.RUN_ID
BASE_ATTEMPT_NAME = "c03_xtrees_cashopen_q95q90"
ATTEMPT_NAME = f"{BASE_ATTEMPT_NAME}_noconv"
PARITY_TOLERANCE = 1.0e-4
COMMON_ROOT = "Project_Obsidian_Prime_v2/stage349/run349D_onnx_no_conversion_parity_diagnostic"
COMMON_TELEMETRY_DIR = f"{COMMON_ROOT}/telemetry"
EXPLORATION_LABEL = "stage349_ONNXShortCarry__NoConversionParityDiagnostic"
TRADE_DENSITY_REQUIREMENT = "trade_per_day_min_3_to_10_plus_no_trade_splitting"
CLAIM_BOUNDARY = (
    "research_development_onnx_no_conversion_runtime_parity_diagnostic_only_"
    "no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_"
    "no_runtime_authority_no_goal_claim"
)

NEXT_IF_PASSED = "run349E_execute_no_conversion_short_carry_reprobe_without_db_v1"
NEXT_IF_FAILED = "run349E_repair_treeensemble_onnx_operator_or_pivot_model_family_without_db_v1"
NEXT_IF_BLOCKED = "run349E_retry_or_repair_no_conversion_runtime_parity_diagnostic_without_db_v1"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MT5_DIR = RUN_DIR / "mt5"
SET_DIR = MT5_DIR / "sets"
INI_DIR = MT5_DIR / "inis"
TELEMETRY_COPY_DIR = RUN_DIR / "runtime_telemetry"
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run349D_onnx_no_conversion_runtime_parity_diagnostic.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage349D_onnx_no_conversion_runtime_parity_diagnostic.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_README = STAGE_DIR / "README.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"

RUN349B_DIR = STAGE_DIR / "02_runs" / "run349B"
RUN349B_SET = RUN349B_DIR / "mt5" / "sets" / f"OPV2_run349B_{BASE_ATTEMPT_NAME}.set"
RUN349B_INI = RUN349B_DIR / "mt5" / "inis" / f"OPV2_run349B_{BASE_ATTEMPT_NAME}.ini"
RUN349B_SUMMARY = RUN349B_DIR / "onnx_short_carry_mt5_probe_summary.csv"
RUN349C_DIR = STAGE_DIR / "02_runs" / "run349C"
RUN349C_FINAL = RUN349C_DIR / "final_decision.json"
RUN349C_GATES = RUN349C_DIR / "required_gate_coverage_audit.csv"
RUN349C_DIAGNOSTIC = RUN349C_DIR / "python_onnx_vs_expected_vs_mt5_diagnostic.csv"

SOURCE_EXPECTED_TAPE = source_pkg.EXPECTED_TAPE
SOURCE_RUNTIME_FEATURES = ROOT / "stages" / SOURCE_STAGE_ID / "02_runs" / "run348C" / "features" / "runtime_features.csv"
SOURCE_FEATURE_ORDER = source_pkg.FEATURE_ORDER_CONTRACT
SOURCE_MODEL_MANIFEST = source_pkg.MODEL_HANDOFF_MANIFEST
SOURCE_COMMON_SYNC = source_pkg.COMMON_FILES_SYNC

ATTEMPT_PACKAGE = RUN_DIR / "runtime_parity_attempt_package.csv"
TERMINAL_PROCESS_AUDIT = RUN_DIR / "terminal_process_audit.json"
MT5_EXECUTION_RESULT = RUN_DIR / "mt5_execution_result.json"
STRATEGY_TESTER_REPORTS = RUN_DIR / "strategy_tester_report_records.json"
RUNTIME_OUTPUT_COPY = RUN_DIR / "runtime_output_copy_manifest.csv"
NO_CONVERSION_DIFF = RUN_DIR / "no_conversion_proxy_mt5_runtime_difference.csv"
SUMMARY_CSV = RUN_DIR / "onnx_no_conversion_runtime_parity_summary.csv"
RUNTIME_IDENTITY = RUN_DIR / "runtime_identity.csv"
RUNTIME_PARITY_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
BACKTEST_FORENSICS_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
PERFORMANCE_ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "judgment_receipt.json"
ARTIFACT_LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_BOUNDARY_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
NEXT_ACTION_QUEUE = RUN_DIR / "next_action_queue.csv"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
ROOT_SELECTION_STATUS = ROOT / "docs" / "registers" / "selection_status.md"
ROOT_CHANGELOG = ROOT / "CHANGELOG.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

INPUT_FILES = (
    RUN349B_SET,
    RUN349B_INI,
    RUN349B_SUMMARY,
    RUN349C_FINAL,
    RUN349C_GATES,
    RUN349C_DIAGNOSTIC,
    SOURCE_EXPECTED_TAPE,
    SOURCE_RUNTIME_FEATURES,
    SOURCE_FEATURE_ORDER,
    SOURCE_MODEL_MANIFEST,
    SOURCE_COMMON_SYNC,
)

OUTPUT_FILES = (
    ATTEMPT_PACKAGE,
    TERMINAL_PROCESS_AUDIT,
    MT5_EXECUTION_RESULT,
    STRATEGY_TESTER_REPORTS,
    RUNTIME_OUTPUT_COPY,
    NO_CONVERSION_DIFF,
    SUMMARY_CSV,
    RUNTIME_IDENTITY,
    RUNTIME_PARITY_RECEIPT,
    BACKTEST_FORENSICS_RECEIPT,
    PERFORMANCE_ATTRIBUTION_RECEIPT,
    JUDGMENT_RECEIPT,
    ARTIFACT_LINEAGE_RECEIPT,
    CLAIM_BOUNDARY_RECEIPT,
    NEXT_ACTION_QUEUE,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
)


fs_path = review349c.fs_path
exists = review349c.exists
required = review349c.required
ensure_parent = review349c.ensure_parent
rel = review349c.rel
sha256_file = review349c.sha256_file
read_json = review349c.read_json
write_json = review349c.write_json
write_csv = review349c.write_csv
read_csv_rows = review349c.read_csv_rows
append_or_replace_csv = review349c.append_or_replace_csv
write_bom_text = review349c.write_bom_text
append_text_once = review349c.append_text_once
json_ready = review349c.json_ready
to_float = review349c.to_float
to_int = review349c.to_int


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Stage349D ONNX no-conversion MT5 parity diagnostic.")
    parser.add_argument("--terminal-path", default=str(source_pkg.DEFAULT_TERMINAL))
    parser.add_argument("--common-files-root", default=str(source_pkg.DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(source_pkg.DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-data-root", default=str(source_pkg.DEFAULT_PORTABLE_ROOT))
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--wait-timeout-seconds", type=int, default=240)
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--reuse-existing-outputs", action="store_true")
    return parser.parse_args()


def parse_set(path: Path) -> dict[str, Any]:
    values: dict[str, Any] = {}
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line or line.startswith(";") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip()
    return values


def parse_tester_ini(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    in_tester = False
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line:
                continue
            if line.startswith("[") and line.endswith("]"):
                in_tester = line.lower() == "[tester]"
                continue
            if in_tester and "=" in line:
                key, value = line.split("=", 1)
                values[key.strip()] = value.strip()
    return values


def gate_passed(path: Path) -> bool:
    _fields, rows = read_csv_rows(required(path))
    return bool(rows) and all(str(row.get("status", "")).lower() == "passed" for row in rows)


def norm_time(value: Any) -> str:
    text = str(value).strip()
    if not text:
        return ""
    text = text.replace("T", " ").replace("Z", "")
    if "-" in text[:10]:
        text = text.replace("-", ".")
    if "." in text[10:]:
        text = text.split(".", 1)[0]
    return text[:19]


def fnv1a64_upper(line: str) -> str:
    value = 1469598103934665603
    for char in line:
        value = ((value ^ ord(char)) * 1099511628211) & 0xFFFFFFFFFFFFFFFF
    return f"{value:X}"


def feature_input_hash_by_time() -> dict[str, str]:
    hashes: dict[str, str] = {}
    with open(fs_path(required(SOURCE_RUNTIME_FEATURES)), encoding="utf-8-sig", newline="") as handle:
        _header = handle.readline()
        for raw_line in handle:
            line = raw_line.rstrip("\r\n")
            if not line:
                continue
            key = norm_time(line.split(",", 1)[0])
            if key:
                hashes[key] = fnv1a64_upper(line)
    return hashes


def metric_value(metrics: Mapping[str, Any], key: str) -> Any:
    value = metrics.get(key, "")
    if value is None:
        return ""
    return value


def trade_density_status(value: float | None) -> str:
    if value is None or not math.isfinite(value):
        return "not_available(확인 불가)"
    if value >= 10.0:
        return "meets_10_plus_target(10+ 목표 충족)"
    if value >= 3.0:
        return "meets_min_3_to_10_band(최소 3~10 구간 충족)"
    return "below_min_3_per_day(일 3회 미만)"


def expected_rows_by_time() -> dict[str, Mapping[str, Any]]:
    expected = pd.read_csv(fs_path(required(SOURCE_EXPECTED_TAPE)), encoding="utf-8-sig", low_memory=False).fillna("")
    subset = expected[expected["attempt_name"].astype(str).eq(BASE_ATTEMPT_NAME)].copy()
    return {norm_time(row["bar_time_server"]): row.to_dict() for _, row in subset.iterrows()}


def materialize_attempt() -> dict[str, Any]:
    source_set = parse_set(required(RUN349B_SET))
    source_ini = parse_tester_ini(required(RUN349B_INI))
    common_telemetry = f"{COMMON_TELEMETRY_DIR}/{ATTEMPT_NAME}_telemetry.csv"
    common_summary = f"{COMMON_TELEMETRY_DIR}/{ATTEMPT_NAME}_summary.csv"
    report_name = f"POPv2_run349D_{ATTEMPT_NAME}"
    set_name = f"OPV2_run349D_{ATTEMPT_NAME}.set"
    ini_name = f"OPV2_run349D_{ATTEMPT_NAME}.ini"
    set_path = SET_DIR / set_name
    ini_path = INI_DIR / ini_name

    set_values = dict(source_set)
    set_values["InpRunId"] = f"{RUN_ID}_{ATTEMPT_NAME}"
    set_values["InpExplorationLabel"] = EXPLORATION_LABEL
    set_values["InpModelNoConversion"] = True
    set_values["InpTelemetryCsvPath"] = common_telemetry
    set_values["InpSummaryCsvPath"] = common_summary
    set_values["InpMagic"] = 3496003
    set_payload = mt5.materialize_tester_set_file(
        set_values,
        set_path,
        generated_by="stage_pipelines/stage349/test_onnx_no_conversion_runtime_parity_diagnostic_without_db.py",
    )

    cfg = mt5.TesterMaterializationConfig(
        expert=source_ini.get("Expert", "Project_Obsidian_Prime_v2\\foundation\\mt5\\ObsidianPrimeV2_RuntimeProbeEA.ex5"),
        symbol=source_ini.get("Symbol", "US100"),
        period=source_ini.get("Period", "M5"),
        model=to_int(source_ini.get("Model", 4), 4),
        deposit=to_float(source_ini.get("Deposit", 500), 500.0),
        leverage=source_ini.get("Leverage", "1:100"),
        optimization=to_int(source_ini.get("Optimization", 0), 0),
        execution_mode=to_int(source_ini.get("ExecutionMode", 0), 0),
        forward_mode=to_int(source_ini.get("ForwardMode", 0), 0),
        use_local=to_int(source_ini.get("UseLocal", 1), 1),
        use_remote=to_int(source_ini.get("UseRemote", 0), 0),
        use_cloud=to_int(source_ini.get("UseCloud", 0), 0),
        replace_report=1,
        shutdown_terminal=1,
        from_date=source_ini.get("FromDate", "2024.07.30"),
        to_date=source_ini.get("ToDate", "2025.01.01"),
        report=report_name,
    )
    ini_payload = mt5.materialize_tester_ini_file(cfg, ini_path, set_file_path=Path(set_name))
    attempt = {
        "attempt_name": ATTEMPT_NAME,
        "base_attempt_name": BASE_ATTEMPT_NAME,
        "variant": "InpModelNoConversion=true",
        "model_id": set_values.get("InpModelId", ""),
        "model_path": set_values.get("InpModelPath", ""),
        "feature_csv_path": set_values.get("InpFeatureCsvPath", ""),
        "feature_count": set_values.get("InpFeatureCount", ""),
        "feature_order_hash": set_values.get("InpFeatureOrderHash", ""),
        "tier": set_values.get("InpTierLabel", "Tier A"),
        "split": set_values.get("InpSplitLabel", "all_rows_with_test_seed_thresholds"),
        "from_date": cfg.from_date,
        "to_date": cfg.to_date,
        "report_name": report_name,
        "common_telemetry_path": common_telemetry,
        "common_summary_path": common_summary,
        "set_name": set_name,
        "ini_name": ini_name,
        "set_path": rel(set_path),
        "ini_path": rel(ini_path),
        "set_sha256": set_payload["sha256"],
        "ini_sha256": ini_payload["sha256"],
        "ini": {"tester": {"Report": report_name}},
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(ATTEMPT_PACKAGE, [attempt])
    return attempt


def remove_runtime_outputs(common_files_root: Path, attempt: Mapping[str, Any]) -> None:
    for key in ("common_telemetry_path", "common_summary_path"):
        target = common_files_root / Path(str(attempt[key]))
        if exists(target):
            os.unlink(fs_path(target))


def copy_runtime_outputs(common_files_root: Path, attempt: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, suffix in (("common_telemetry_path", "telemetry"), ("common_summary_path", "summary")):
        source = common_files_root / Path(str(attempt[key]))
        target = TELEMETRY_COPY_DIR / f"{ATTEMPT_NAME}_{suffix}.csv"
        copied = False
        if exists(source):
            ensure_parent(target)
            shutil.copy2(fs_path(source), fs_path(target))
            copied = True
        rows.append(
            {
                "copy_id": f"{ATTEMPT_NAME}::{suffix}",
                "attempt_name": ATTEMPT_NAME,
                "source_path": source.as_posix(),
                "target_path": rel(target),
                "exists": copied and exists(target),
                "sha256": sha256_file(target) if copied and exists(target) else "",
                "effect": "MT5 Common Files(공용 파일)의 runtime telemetry(런타임 기록)를 Stage349D run folder(실행 폴더)에 고정한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(RUNTIME_OUTPUT_COPY, rows)
    return rows


def execute_attempt(args: argparse.Namespace, attempt: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    common_files_root = Path(args.common_files_root)
    tester_profile_root = Path(args.tester_profile_root)
    terminal_data_root = Path(args.terminal_data_root)
    terminal_probe = terminal_processes()
    write_json(TERMINAL_PROCESS_AUDIT, terminal_probe)
    execution_results: list[dict[str, Any]] = []
    report_records: list[dict[str, Any]] = []

    if args.materialize_only:
        execution_results.append(
            {
                "attempt_name": ATTEMPT_NAME,
                "model_id": attempt.get("model_id", ""),
                "status": "not_run_materialize_only",
                "runtime_outputs": {"status": "not_run_materialize_only"},
                "ini_path": attempt["ini_path"],
                "set_path": attempt["set_path"],
            }
        )
    elif args.reuse_existing_outputs:
        runtime_outputs = mt5.validate_mt5_runtime_outputs(common_files_root, attempt)
        execution_results.append(
            {
                "attempt_name": ATTEMPT_NAME,
                "model_id": attempt.get("model_id", ""),
                "status": "completed" if runtime_outputs.get("status") == "completed" else "blocked",
                "runtime_outputs": runtime_outputs,
                "ini_path": attempt["ini_path"],
                "set_path": attempt["set_path"],
            }
        )
    elif terminal_probe.get("status") != "no_terminal64_process":
        execution_results.append(
            {
                "attempt_name": ATTEMPT_NAME,
                "model_id": attempt.get("model_id", ""),
                "status": "blocked",
                "blocker": "target_portable_terminal_already_running",
                "runtime_outputs": {"status": "blocked", "wait_status": "skipped_terminal_already_running"},
                "ini_path": attempt["ini_path"],
                "set_path": attempt["set_path"],
            }
        )
    else:
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
        execution_results.append(
            {
                **tester_result,
                "attempt_name": ATTEMPT_NAME,
                "model_id": attempt.get("model_id", ""),
                "runtime_outputs": runtime_outputs,
                "ini_path": attempt["ini_path"],
                "set_path": attempt["set_path"],
            }
        )

    report_records = mt5.collect_mt5_strategy_report_artifacts(
        terminal_data_root=terminal_data_root,
        run_output_root=RUN_DIR,
        attempts=[attempt],
        run_id=RUN_ID,
    )
    mt5.attach_mt5_report_metrics(execution_results, report_records)
    copy_rows = copy_runtime_outputs(common_files_root, attempt)
    write_json(MT5_EXECUTION_RESULT, execution_results)
    write_json(STRATEGY_TESTER_REPORTS, report_records)
    return execution_results, report_records, copy_rows


def compare_runtime(attempt: Mapping[str, Any], execution_row: Mapping[str, Any], report_row: Mapping[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    expected = expected_rows_by_time()
    feature_hashes = feature_input_hash_by_time()
    telemetry_path = TELEMETRY_COPY_DIR / f"{ATTEMPT_NAME}_telemetry.csv"
    summary_path = TELEMETRY_COPY_DIR / f"{ATTEMPT_NAME}_summary.csv"
    metrics = report_row.get("metrics", {}) if isinstance(report_row.get("metrics"), Mapping) else {}
    diff_rows: list[dict[str, Any]] = []

    if not exists(telemetry_path):
        summary = {
            "attempt_name": ATTEMPT_NAME,
            "base_attempt_name": BASE_ATTEMPT_NAME,
            "variant": "InpModelNoConversion=true",
            "tester_status": execution_row.get("status", "not_attempted"),
            "runtime_status": execution_row.get("runtime_outputs", {}).get("status", "missing"),
            "report_status": report_row.get("status", "missing") if report_row else "missing",
            "rows_compared": 0,
            "matched_time_rows": 0,
            "probability_match_rows": 0,
            "python_expected_mt5_max_abs_diff": "",
            "parity_status": "blocked_runtime_telemetry_missing(런타임 기록 누락)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        return summary, diff_rows

    telemetry = pd.read_csv(fs_path(telemetry_path), encoding="utf-8-sig", low_memory=False).fillna("")
    cycles = telemetry[telemetry["record_type"].astype(str).str.lower().eq("cycle")].copy()
    cycles = cycles[cycles["feature_ready"].astype(str).str.lower().eq("true")].copy()
    max_abs = 0.0
    matched_time = 0
    probability_match = 0
    decision_mismatch = 0
    input_hash_match = 0
    input_hash_mismatch = 0
    first_diff: dict[str, Any] | None = None
    for _, row in cycles.iterrows():
        key = norm_time(row.get("bar_time", ""))
        exp = expected.get(key)
        if exp is None:
            continue
        matched_time += 1
        mt5_input_hash = str(row.get("input_hash", "")).strip().upper()
        expected_input_hash = feature_hashes.get(key, "").upper()
        input_hash_ok = bool(mt5_input_hash and expected_input_hash and mt5_input_hash == expected_input_hash)
        if input_hash_ok:
            input_hash_match += 1
        else:
            input_hash_mismatch += 1
        diffs = {
            "p_short_abs_diff": abs(to_float(row.get("p_short")) - to_float(exp.get("p_short"))),
            "p_flat_abs_diff": abs(to_float(row.get("p_flat")) - to_float(exp.get("p_flat"))),
            "p_long_abs_diff": abs(to_float(row.get("p_long")) - to_float(exp.get("p_long"))),
        }
        row_max = max(diffs.values())
        max_abs = max(max_abs, row_max)
        runtime_decision = str(row.get("decision", "")).strip().lower()
        expected_decision = str(exp.get("ea_mapped_expected_label", "")).strip().lower()
        decision_ok = not runtime_decision or not expected_decision or runtime_decision == expected_decision
        if not decision_ok:
            decision_mismatch += 1
        if row_max <= PARITY_TOLERANCE:
            probability_match += 1
        elif first_diff is None:
            first_diff = {
                "bar_time": key,
                "runtime_p_short": to_float(row.get("p_short")),
                "runtime_p_flat": to_float(row.get("p_flat")),
                "runtime_p_long": to_float(row.get("p_long")),
                "expected_p_short": to_float(exp.get("p_short")),
                "expected_p_flat": to_float(exp.get("p_flat")),
                "expected_p_long": to_float(exp.get("p_long")),
                **diffs,
                "runtime_decision": runtime_decision,
                "expected_decision": expected_decision,
                "mt5_input_hash": mt5_input_hash,
                "expected_input_hash": expected_input_hash,
                "input_hash_match": input_hash_ok,
            }
        diff_rows.append(
            {
                "attempt_name": ATTEMPT_NAME,
                "base_attempt_name": BASE_ATTEMPT_NAME,
                "bar_time": key,
                **diffs,
                "row_max_abs_diff": row_max,
                "probability_match": row_max <= PARITY_TOLERANCE,
                "runtime_decision": runtime_decision,
                "expected_decision": expected_decision,
                "decision_match": decision_ok,
                "mt5_input_hash": mt5_input_hash,
                "expected_input_hash": expected_input_hash,
                "input_hash_match": input_hash_ok,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    if summary_path.exists():
        runtime_summary = pd.read_csv(fs_path(summary_path), encoding="utf-8-sig", low_memory=False).fillna("")
        last_runtime_summary = runtime_summary.iloc[-1].to_dict() if not runtime_summary.empty else {}
    else:
        last_runtime_summary = {}

    expected_dates = {key[:10] for key in expected if key}
    feature_day_count = len(expected_dates)
    trade_count = to_int(metric_value(metrics, "trade_count"), 0)
    density = trade_count / feature_day_count if feature_day_count else None
    parity_pass = matched_time > 0 and probability_match == matched_time and max_abs <= PARITY_TOLERANCE
    summary = {
        "attempt_name": ATTEMPT_NAME,
        "base_attempt_name": BASE_ATTEMPT_NAME,
        "variant": "InpModelNoConversion=true",
        "tester_status": execution_row.get("status", "not_attempted"),
        "runtime_status": execution_row.get("runtime_outputs", {}).get("status", "missing"),
        "report_status": report_row.get("status", "missing") if report_row else "missing",
        "rows_compared": matched_time,
        "runtime_feature_ready_rows": len(cycles),
        "expected_rows": len(expected),
        "probability_match_rows": probability_match,
        "decision_mismatch_rows": decision_mismatch,
        "input_hash_match_rows": input_hash_match,
        "input_hash_mismatch_rows": input_hash_mismatch,
        "input_hash_status": "matched(일치)" if matched_time > 0 and input_hash_match == matched_time else "mismatch_or_missing(불일치 또는 누락)",
        "python_expected_mt5_max_abs_diff": max_abs if matched_time else "",
        "parity_tolerance": PARITY_TOLERANCE,
        "parity_passed": parity_pass,
        "parity_status": "passed(통과)" if parity_pass else "failed_mismatch_or_missing(불일치 또는 누락)",
        "first_mismatch": first_diff or {},
        "net_profit": metric_value(metrics, "net_profit"),
        "profit_factor": metric_value(metrics, "profit_factor"),
        "expectancy": metric_value(metrics, "expectancy"),
        "max_drawdown_amount": metric_value(metrics, "max_drawdown_amount"),
        "recovery_factor": metric_value(metrics, "recovery_factor"),
        "trade_count": trade_count,
        "long_trade_count": metric_value(metrics, "long_trade_count"),
        "short_trade_count": metric_value(metrics, "short_trade_count"),
        "trade_density_per_feature_day": density if density is not None else "",
        "trade_density_status": trade_density_status(density),
        "summary_long_count": to_int(last_runtime_summary.get("long_count"), 0),
        "summary_short_count": to_int(last_runtime_summary.get("short_count"), 0),
        "summary_flat_count": to_int(last_runtime_summary.get("flat_count"), 0),
        "model_ok_count": to_int(last_runtime_summary.get("model_ok_count"), 0),
        "feature_ready_count": to_int(last_runtime_summary.get("feature_ready_count"), 0),
        "effect": "InpModelNoConversion=true(변환 없음)이 MT5 ONNX probability(확률) 불일치를 고치는지 확인한다.",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(NO_CONVERSION_DIFF, diff_rows)
    write_csv(SUMMARY_CSV, [summary])
    return summary, diff_rows


def build_final(
    args: argparse.Namespace,
    attempt: Mapping[str, Any],
    execution_results: Sequence[Mapping[str, Any]],
    report_records: Sequence[Mapping[str, Any]],
    copy_rows: Sequence[Mapping[str, Any]],
    parity_summary: Mapping[str, Any],
    diff_rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    runtime_completed = str(parity_summary.get("runtime_status")) == "completed"
    report_completed = str(parity_summary.get("report_status")) == "completed"
    parity_passed = bool(parity_summary.get("parity_passed"))
    input_hash_matched = str(parity_summary.get("input_hash_status", "")) == "matched(일치)"
    blocked = not runtime_completed
    if blocked:
        status = "blocked_stage349D_onnx_no_conversion_runtime_parity_diagnostic_repair_required_no_selection"
        judgment = "blocked_no_conversion_runtime_outputs_missing_or_terminal_unavailable"
        result_judgment = "blocked(차단)"
        decision = "stage349D_open_run349E_retry_or_repair_no_conversion_runtime_parity_diagnostic"
        next_run_id = NEXT_IF_BLOCKED
    elif parity_passed:
        status = "completed_stage349D_onnx_no_conversion_runtime_parity_passed_reprobe_required_no_selection"
        judgment = "repair_positive_no_conversion_resolves_mt5_onnx_probability_mismatch_kpi_still_not_selected"
        result_judgment = "repair_positive(수리 긍정)"
        decision = "stage349D_open_run349E_execute_no_conversion_short_carry_reprobe"
        next_run_id = NEXT_IF_PASSED
    else:
        status = "completed_stage349D_onnx_no_conversion_runtime_parity_still_mismatch_repair_required_no_selection"
        judgment = (
            "negative_no_conversion_failed_input_hash_matched_treeensemble_onnx_operator_repair_required"
            if input_hash_matched
            else "negative_no_conversion_did_not_resolve_mt5_onnx_probability_mismatch_feature_or_operator_repair_required"
        )
        result_judgment = "negative(부정)"
        decision = "stage349D_open_run349E_treeensemble_onnx_operator_or_model_family_repair"
        next_run_id = NEXT_IF_FAILED

    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_runtime_run_id": SOURCE_RUNTIME_RUN_ID,
        "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
        "attempt_name": ATTEMPT_NAME,
        "base_attempt_name": BASE_ATTEMPT_NAME,
        "status": status,
        "judgment": judgment,
        "result_judgment": result_judgment,
        "decision": decision,
        "next_run_id": next_run_id,
        "claim_boundary": CLAIM_BOUNDARY,
        "created_at_utc": now_utc(),
        "materialize_only": bool(args.materialize_only),
        "reuse_existing_outputs": bool(args.reuse_existing_outputs),
        "runtime_completed": runtime_completed,
        "report_completed": report_completed,
        "parity_passed": parity_passed,
        "parity_tolerance": PARITY_TOLERANCE,
        "rows_compared": parity_summary.get("rows_compared", 0),
        "probability_match_rows": parity_summary.get("probability_match_rows", 0),
        "input_hash_match_rows": parity_summary.get("input_hash_match_rows", 0),
        "input_hash_mismatch_rows": parity_summary.get("input_hash_mismatch_rows", 0),
        "input_hash_status": parity_summary.get("input_hash_status", ""),
        "python_expected_mt5_max_abs_diff": parity_summary.get("python_expected_mt5_max_abs_diff", ""),
        "decision_mismatch_rows": parity_summary.get("decision_mismatch_rows", 0),
        "trade_count": parity_summary.get("trade_count", ""),
        "trade_density_per_feature_day": parity_summary.get("trade_density_per_feature_day", ""),
        "trade_density_status": parity_summary.get("trade_density_status", ""),
        "net_profit": parity_summary.get("net_profit", ""),
        "profit_factor": parity_summary.get("profit_factor", ""),
        "expectancy": parity_summary.get("expectancy", ""),
        "max_drawdown_amount": parity_summary.get("max_drawdown_amount", ""),
        "recovery_factor": parity_summary.get("recovery_factor", ""),
        "long_trade_count": parity_summary.get("long_trade_count", ""),
        "short_trade_count": parity_summary.get("short_trade_count", ""),
        "runtime_output_copy_ready_rows": sum(1 for row in copy_rows if str(row.get("exists", "")).lower() == "true"),
        "execution_result_rows": len(execution_results),
        "report_record_rows": len(report_records),
        "diff_rows": len(diff_rows),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "goal_achieve": "not_claimed",
    }


def make_gates(final: Mapping[str, Any], attempt: Mapping[str, Any]) -> list[dict[str, Any]]:
    def row(gate_id: str, passed: bool, evidence: str, effect: str) -> dict[str, Any]:
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

    return [
        row(
            "parent_run349C_review_gate",
            gate_passed(RUN349C_GATES),
            rel(RUN349C_GATES),
            "run349C review(검토)가 MT5 mismatch(불일치)를 먼저 고정했는지 확인한다.",
        ),
        row(
            "no_conversion_set_ini_materialized",
            exists(ROOT / str(attempt["set_path"])) and exists(ROOT / str(attempt["ini_path"])),
            f"{attempt['set_path']};{attempt['ini_path']}",
            "InpModelNoConversion=true(변환 없음) 파라미터만 바꾼 실행 인계를 만든다.",
        ),
        row(
            "mt5_runtime_output_observed",
            bool(final["runtime_completed"]),
            rel(MT5_EXECUTION_RESULT),
            "MT5 runtime telemetry(런타임 기록)가 실제 생성됐는지 확인한다.",
        ),
        row(
            "strategy_report_collected",
            bool(final["report_completed"]),
            rel(STRATEGY_TESTER_REPORTS),
            "Strategy Tester report(전략 테스터 보고서)를 외부 검증 근거로 고정한다.",
        ),
        row(
            "parity_diagnostic_written",
            exists(NO_CONVERSION_DIFF) and exists(SUMMARY_CSV),
            f"{rel(NO_CONVERSION_DIFF)};{rel(SUMMARY_CSV)}",
            "expected probability(예상 확률)와 MT5 probability(MT5 확률)의 행 단위 차이를 기록한다.",
        ),
        row(
            "result_judgment_recorded",
            final.get("result_judgment") in {"repair_positive(수리 긍정)", "negative(부정)", "blocked(차단)"},
            rel(FINAL_DECISION),
            "수리 성공/실패/차단을 운영 주장 없이 판정한다.",
        ),
        row(
            "tier_pair_rows_written",
            exists(STAGE_LEDGER) and exists(PROJECT_LEDGER),
            f"{rel(STAGE_LEDGER)};{rel(PROJECT_LEDGER)}",
            "Tier A used(Tier A 사용), Tier B missing_required(필수 누락), Tier A+B combined(Tier A+B 합산)을 기록한다.",
        ),
        row(
            "artifact_lineage_recorded",
            exists(ARTIFACT_LINEAGE_RECEIPT) and exists(RUN_MANIFEST),
            f"{rel(ARTIFACT_LINEAGE_RECEIPT)};{rel(RUN_MANIFEST)}",
            "원천 set/model/expected tape(예상 테이프)와 새 산출물 계보를 연결한다.",
        ),
        row(
            "final_claim_guard",
            all(final.get(key) == "not_claimed" for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]),
            rel(FINAL_DECISION),
            "runtime authority(런타임 권위), 운영 승격, 목표 달성을 주장하지 않는다.",
        ),
    ]


def write_runtime_identity(args: argparse.Namespace, attempt: Mapping[str, Any]) -> None:
    diag = pd.read_csv(fs_path(required(RUN349C_DIAGNOSTIC)), encoding="utf-8-sig", low_memory=False).fillna("")
    model_path = ""
    model_sha = ""
    subset = diag[diag["attempt_name"].astype(str).eq(BASE_ATTEMPT_NAME)]
    if not subset.empty:
        model_path = str(subset.iloc[0].get("model_path", ""))
        repo_model = ROOT / model_path
        model_sha = sha256_file(repo_model) if exists(repo_model) else ""
    common_model = Path(args.common_files_root) / Path(str(attempt.get("model_path", "")))
    rows = [
        {
            "identity_type": "terminal64",
            "path": str(args.terminal_path),
            "sha256": sha256_file(Path(args.terminal_path)) if exists(Path(args.terminal_path)) else "",
            "status": "present" if exists(Path(args.terminal_path)) else "missing",
        },
        {
            "identity_type": "repo_model",
            "path": model_path,
            "sha256": model_sha,
            "status": "present" if model_sha else "missing",
        },
        {
            "identity_type": "common_files_model",
            "path": common_model.as_posix(),
            "sha256": sha256_file(common_model) if exists(common_model) else "",
            "status": "present" if exists(common_model) else "missing",
        },
    ]
    for module in mt5.mt5_runtime_module_hashes():
        rows.append(
            {
                "identity_type": "mt5_runtime_module",
                "path": module.get("path", ""),
                "sha256": module.get("sha256", ""),
                "status": module.get("status", ""),
            }
        )
    write_csv(RUNTIME_IDENTITY, rows)


def write_receipts(final: Mapping[str, Any], attempt: Mapping[str, Any]) -> None:
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "created_at_utc": now_utc(),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(
        RUNTIME_PARITY_RECEIPT,
        {
            **base,
            "research_path": rel(SOURCE_EXPECTED_TAPE),
            "runtime_path": attempt["set_path"],
            "shared_contract": "feature order 53(피처 순서 53), output order [p_short,p_flat,p_long](출력 순서), closed M5 bar timestamp(닫힌 5분봉 시각)",
            "known_differences": "only InpModelNoConversion=true(변환 없음) differs from run349B c03.",
            "parity_check": rel(SUMMARY_CSV),
            "parity_identity": rel(RUNTIME_IDENTITY),
            "runtime_claim_boundary": "runtime_probe(런타임 탐침)",
            "parity_passed": final["parity_passed"],
            "max_abs_diff": final["python_expected_mt5_max_abs_diff"],
        },
    )
    write_json(
        BACKTEST_FORENSICS_RECEIPT,
        {
            **base,
            "tester_report": rel(STRATEGY_TESTER_REPORTS),
            "tester_settings": "US100 M5, Model=4(real ticks, 실제 틱), Deposit=500, Leverage=1:100, same run349B date window(동일 기간)",
            "spread_commission_slippage": "broker Strategy Tester report(브로커 전략 테스터 보고서) 기준; synthetic cost overlay(합성 비용 덧씌우기) 없음",
            "trade_list_identity": rel(STRATEGY_TESTER_REPORTS),
            "forensic_gaps": [] if final["report_completed"] else ["strategy_report_missing(전략 테스터 보고서 누락)"],
        },
    )
    write_json(
        PERFORMANCE_ATTRIBUTION_RECEIPT,
        {
            **base,
            "comparison": "run349B c03 InpModelNoConversion=false(변환 있음) vs run349D c03 InpModelNoConversion=true(변환 없음)",
            "summary": rel(SUMMARY_CSV),
            "kpi": {
                "net_profit": final["net_profit"],
                "profit_factor": final["profit_factor"],
                "expectancy": final["expectancy"],
                "trade_count": final["trade_count"],
                "trade_density_per_feature_day": final["trade_density_per_feature_day"],
            },
            "judgment": final["judgment"],
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "result_judgment": final["result_judgment"],
            "status": final["status"],
            "decision": final["decision"],
            "next_run_id": final["next_run_id"],
            "forbidden_claims": ["candidate_selection", "forward_passed", "live_readiness", "operating_promotion", "runtime_authority", "goal_achieve"],
        },
    )
    write_json(
        ARTIFACT_LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [rel(RUN349B_SET), rel(RUN349B_INI), rel(RUN349C_DIAGNOSTIC), rel(SOURCE_EXPECTED_TAPE)],
            "producer": rel(Path(__file__)),
            "consumer": final["next_run_id"],
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {rel(path): sha256_file(path) for path in OUTPUT_FILES if exists(path) and path.is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked",
            "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
        },
    )
    write_json(
        CLAIM_BOUNDARY_RECEIPT,
        {
            **base,
            "allowed_claims": ["runtime_probe_diagnostic(런타임 탐침 진단)", "repair_positive_if_parity_passes(동등성 통과 시 수리 긍정)"],
            "forbidden_claims": ["candidate_selection", "forward_passed", "live_readiness", "operating_promotion", "runtime_authority", "goal_achieve"],
            "goal_achieve": "not_claimed",
        },
    )


def write_next_action_queue(final: Mapping[str, Any]) -> None:
    rows = [
        {
            "queue_id": final["next_run_id"],
            "stage_id": STAGE_ID,
            "source_run_id": RUN_ID,
            "priority": 1,
            "action": final["decision"],
            "condition": final["judgment"],
            "effect": "runtime parity(런타임 동등성) 원인에 맞춰 다음 수리 또는 재탐침을 연다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(NEXT_ACTION_QUEUE, rows)


def write_final_and_manifest(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]], attempt: Mapping[str, Any]) -> None:
    payload = dict(final)
    payload["gate_passes"] = sum(1 for row in gates if row.get("status") == "passed")
    payload["gate_total"] = len(gates)
    write_json(FINAL_DECISION, payload)
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": now_utc(),
        "parent_run_id": PARENT_RUN_ID,
        "source_runtime_run_id": SOURCE_RUNTIME_RUN_ID,
        "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
        "attempt": attempt,
        "inputs": [rel(path) for path in INPUT_FILES],
        "outputs": [rel(path) for path in OUTPUT_FILES if exists(path)],
        "gates": rel(GATE_AUDIT),
        "final_decision": rel(FINAL_DECISION),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(RUN_MANIFEST, manifest)


def write_docs(final: Mapping[str, Any]) -> None:
    report = f"""# run349D ONNX No-Conversion Runtime Parity Diagnostic(349D 온엑스 변환 없음 런타임 동등성 진단)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- result_judgment(결과 판정): `{final['result_judgment']}`
- gates(게이트): `{final['gate_passes']}/{final['gate_total']}`
- base_attempt(기준 시도): `{BASE_ATTEMPT_NAME}`
- variant(변형): `InpModelNoConversion=true`
- runtime_completed(런타임 완료): `{final['runtime_completed']}`
- report_completed(보고서 완료): `{final['report_completed']}`
- parity_passed(동등성 통과): `{final['parity_passed']}`
- rows_compared(비교 행): `{final['rows_compared']}`
- probability_match_rows(확률 일치 행): `{final['probability_match_rows']}`
- input_hash_match_rows(입력 해시 일치 행): `{final['input_hash_match_rows']}`
- input_hash_mismatch_rows(입력 해시 불일치 행): `{final['input_hash_mismatch_rows']}`
- input_hash_status(입력 해시 상태): `{final['input_hash_status']}`
- max_abs_diff(최대 절대 차이): `{final['python_expected_mt5_max_abs_diff']}`
- net_profit(순수익): `{final['net_profit']}`
- profit_factor(수익 팩터): `{final['profit_factor']}`
- trade_count(거래 수): `{final['trade_count']}`
- trade_density(거래 밀도): `{final['trade_density_per_feature_day']}`
- next_run_id(다음 실행 ID): `{final['next_run_id']}`

Action(행동): run349B c03의 ONNX(온엑스) 모델과 feature handoff(피처 인계)는 그대로 두고, MT5 `.set`의 `InpModelNoConversion`만 `true`로 바꿔 Strategy Tester(전략 테스터)를 실행했다.

Effect(효과): MT5 ONNX runtime(런타임) 확률 불일치가 conversion(변환) 문제인지, 아니면 TreeEnsembleClassifier/operator runtime(트리 앙상블 분류기/연산자 런타임) 문제인지 좁힌다.

Input hash effect(입력 해시 효과): input_hash(입력 해시)가 일치하면 feature parser(피처 파서)는 같은 CSV row(CSV 행)를 넣은 것이므로, 남은 원인은 MT5 ONNX operator/runtime(온엑스 연산자/런타임) 쪽으로 좁혀진다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    decision = f"""# Stage349D Decision(349D 결정)

- decision(결정): `{final['decision']}`
- next_run_id(다음 실행 ID): `{final['next_run_id']}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): no-conversion diagnostic(변환 없음 진단)을 Stage349(349단계) 안에서 별도 run(실행)으로 닫았다.

Effect(효과): 운영 후보 선정(candidate selection, 후보 선정) 없이 runtime parity repair(런타임 동등성 수리) 방향만 정한다.
"""
    current = f"""# Current Working State(현재 작업 상태)

- current_stage_id(현재 단계 ID): `{STAGE_ID}`
- current_run_id(현재 실행 ID): `{final['next_run_id']}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- current_status(현재 상태): `{final['status']}`
- current_judgment(현재 판정): `{final['judgment']}`
- current_decision(현재 결정): `{final['decision']}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): Stage349D(349D 실행)는 `InpModelNoConversion=true` runtime probe(런타임 탐침)를 실행했다.

Effect(효과): 다음 작업은 결과에 따라 no-conversion full reprobe(변환 없음 전체 재탐침) 또는 TreeEnsembleClassifier/operator repair(트리 앙상블 분류기/연산자 수리)로 좁혀진다.
"""
    selection = f"""# Stage349 Selection Status(349단계 선택 상태)

- selection_status(선정 상태): `no_selection(선정 없음)`
- latest_run_id(최근 실행 ID): `{RUN_ID}`
- latest_judgment(최근 판정): `{final['judgment']}`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`

Action(행동): Stage349D 결과는 repair diagnostic(수리 진단)으로만 기록한다.

Effect(효과): 수익 후보처럼 보이더라도 MT5 parity(런타임 동등성)와 KPI(핵심 성과 지표)가 닫히기 전에는 운영 주장으로 올라가지 않는다.
"""
    stage_brief = f"""# Stage349 ONNX Short-Carry Runtime Probe(349단계 온엑스 숏 기여 런타임 탐침)

- stage_id(단계 ID): `{STAGE_ID}`
- active_question(현재 질문): Stage348 ONNX deployable short-carry package(배포 가능 온엑스 숏 기여 패키지)가 MT5 runtime(런타임)에서 같은 확률/결정 의미를 유지하는가?
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- current_run_id(현재 실행 ID): `{final['next_run_id']}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Evidence Chain(근거 연결)

- run349A branch(분기): Stage348C 산출물을 Stage349 runtime probe(런타임 탐침)로 넘겼다.
- run349B execution(실행): MT5 Strategy Tester(전략 테스터) 4개 attempt(시도)를 실행했고, ExtraTrees(엑스트라 트리)는 거래 밀도는 충족했지만 손실/PF/DD가 깨졌다.
- run349C review(검토): Python ONNX(파이썬 온엑스)와 expected tape(예상 테이프)는 일치하지만 MT5 ONNX 확률은 불일치한다고 판정했다.
- run349D no-conversion diagnostic(변환 없음 진단): `InpModelNoConversion=true`를 단일 c03 attempt(시도)에 적용해 원인 수리를 좁혔다.

## Latest Result(최신 결과)

- parity_passed(동등성 통과): `{final['parity_passed']}`
- max_abs_diff(최대 절대 차이): `{final['python_expected_mt5_max_abs_diff']}`
- input_hash_status(입력 해시 상태): `{final['input_hash_status']}`
- trade_count(거래 수): `{final['trade_count']}`
- net_profit(순수익): `{final['net_profit']}`
- profit_factor(수익 팩터): `{final['profit_factor']}`
- next_condition(다음 조건): `{final['next_run_id']}`

Effect(효과): Stage349는 운영 승격 단계가 아니라 MT5 ONNX runtime parity(런타임 동등성) 원인을 닫는 분기 단계로 유지된다.
"""
    write_bom_text(REPORT_PATH, report)
    write_bom_text(DECISION_DOC, decision)
    write_bom_text(CURRENT_WORKING_STATE, current)
    write_bom_text(SELECTION_STATUS, selection)
    write_bom_text(ROOT_SELECTION_STATUS, selection)
    write_bom_text(STAGE_BRIEF, stage_brief)
    append_text_once(
        STAGE_README,
        "## run349D ONNX No-Conversion Runtime Parity Diagnostic",
        f"""## run349D ONNX No-Conversion Runtime Parity Diagnostic

- run_id(실행 ID): `{RUN_ID}`
- parity_passed(동등성 통과): `{final['parity_passed']}`
- max_abs_diff(최대 절대 차이): `{final['python_expected_mt5_max_abs_diff']}`
- next_run_id(다음 실행 ID): `{final['next_run_id']}`
- effect(효과): MT5 ONNX conversion(변환) 가설을 실제 Strategy Tester(전략 테스터)로 검증했다.
""",
    )
    changelog = f"""## {TODAY} run349D ONNX No-Conversion Runtime Parity Diagnostic

- action(행동): `InpModelNoConversion=true` 단일 c03 MT5 runtime probe(런타임 탐침)를 실행했다.
- effect(효과): parity_passed(동등성 통과) `{final['parity_passed']}`, max_abs_diff(최대 절대 차이) `{final['python_expected_mt5_max_abs_diff']}`, next_run(다음 실행) `{final['next_run_id']}`를 기록했다.
"""
    append_text_once(ROOT_CHANGELOG, "## 2026-06-01 run349D ONNX No-Conversion Runtime Parity Diagnostic", changelog)
    append_text_once(WORKSPACE_CHANGELOG, "## 2026-06-01 run349D ONNX No-Conversion Runtime Parity Diagnostic", changelog)


def write_registers(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    workspace_state = "\n".join(
        [
            f"current_stage_id: {STAGE_ID}",
            f"current_run_id: {final['next_run_id']}",
            f"latest_completed_run_id: {RUN_ID}",
            f"current_status: {final['status']}",
            f"current_judgment: {final['judgment']}",
            f"current_decision: {final['decision']}",
            f"next_run_id: {final['next_run_id']}",
            f"claim_boundary: {CLAIM_BOUNDARY}",
            f"updated_at: {TODAY}",
            "",
        ]
    )
    write_bom_text(WORKSPACE_STATE, workspace_state)
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "status": final["status"],
        "judgment": final["judgment"],
        "result_judgment": final["result_judgment"],
        "decision": final["decision"],
        "next_run_id": final["next_run_id"],
        "report_path": rel(REPORT_PATH),
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": TODAY,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [run_row])
    ledger_base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "status": final["status"],
        "judgment": final["judgment"],
        "result_judgment": final["result_judgment"],
        "net_profit": final["net_profit"],
        "profit_factor": final["profit_factor"],
        "expectancy": final["expectancy"],
        "max_drawdown_amount": final["max_drawdown_amount"],
        "recovery_factor": final["recovery_factor"],
        "trade_count": final["trade_count"],
        "trade_density_per_feature_day": final["trade_density_per_feature_day"],
        "long_trade_count": final["long_trade_count"],
        "short_trade_count": final["short_trade_count"],
        "report_path": rel(REPORT_PATH),
        "final_decision_path": rel(FINAL_DECISION),
        "claim_boundary": CLAIM_BOUNDARY,
        "created_at": TODAY,
    }
    ledger_rows = [
        {
            **ledger_base,
            "ledger_row_id": f"{RUN_ID}__Tier A",
            "subrun_id": "Tier A",
            "view": "Tier A used(Tier A 사용)",
            "record_view": "Tier A used(Tier A 사용)",
            "tier": "Tier A",
            "tier_scope": "Tier A",
            "metric_scope": "single_c03_no_conversion_runtime_parity_diagnostic",
            "kpi_scope": "MT5 Strategy Tester report(MT5 전략 테스터 보고서)",
            "guardrail_kpi": TRADE_DENSITY_REQUIREMENT,
        },
        {
            **ledger_base,
            "ledger_row_id": f"{RUN_ID}__Tier B",
            "subrun_id": "Tier B",
            "view": "Tier B fallback used(Tier B 대체 사용)",
            "record_view": "Tier B fallback used(Tier B 대체 사용)",
            "tier": "Tier B",
            "tier_scope": "Tier B",
            "metric_scope": "missing_required",
            "kpi_scope": "missing_required",
            "net_profit": "",
            "profit_factor": "",
            "expectancy": "",
            "max_drawdown_amount": "",
            "recovery_factor": "",
            "trade_count": "",
            "trade_density_per_feature_day": "",
            "long_trade_count": "",
            "short_trade_count": "",
            "guardrail_kpi": "missing_required(필수 누락)",
            "result_status": "missing_required(필수 누락)",
        },
        {
            **ledger_base,
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
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], ledger_rows)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], ledger_rows)


def update_artifact_registry() -> None:
    rows = []
    for path in OUTPUT_FILES:
        if not exists(path):
            continue
        relative = rel(path)
        rows.append(
            {
                "artifact_id": f"{RUN_ID}__{relative.replace('/', '__').replace('.', '_')}",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": path.suffix.lstrip(".") or "artifact",
                "path": relative,
                "artifact_path": relative,
                "sha256": sha256_file(path) if path.is_file() else "",
                "created_at": TODAY,
                "created_at_utc": now_utc(),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def validate(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    missing = [rel(path) for path in [FINAL_DECISION, RUN_MANIFEST, GATE_AUDIT, REPORT_PATH, DECISION_DOC, SUMMARY_CSV, NEXT_ACTION_QUEUE] if not exists(path)]
    if missing:
        raise FileNotFoundError("missing generated output(생성 출력 누락): " + ", ".join(missing))
    if final.get("goal_achieve") != "not_claimed":
        raise RuntimeError("forbidden goal claim(금지된 목표 주장)")
    if not gates:
        raise RuntimeError("gate audit missing(게이트 감사 누락)")


def main() -> None:
    for directory in [RUN_DIR, MT5_DIR, SET_DIR, INI_DIR, TELEMETRY_COPY_DIR, REVIEW_DIR, DECISION_DOC.parent]:
        os.makedirs(fs_path(directory), exist_ok=True)
    for path in INPUT_FILES:
        required(path)
    args = parse_args()
    attempt = materialize_attempt()
    execution_results, report_records, copy_rows = execute_attempt(args, attempt)
    execution_row = execution_results[0] if execution_results else {}
    report_row = report_records[0] if report_records else {}
    parity_summary, diff_rows = compare_runtime(attempt, execution_row, report_row)
    final_seed = build_final(args, attempt, execution_results, report_records, copy_rows, parity_summary, diff_rows)
    gates = make_gates(final_seed, attempt)
    write_csv(GATE_AUDIT, gates)
    write_runtime_identity(args, attempt)
    write_receipts(final_seed, attempt)
    write_next_action_queue(final_seed)
    final_with_gates = {**final_seed, "gate_passes": sum(1 for row in gates if row.get("status") == "passed"), "gate_total": len(gates)}
    write_final_and_manifest(final_with_gates, gates, attempt)
    final = read_json(FINAL_DECISION)
    write_docs(final)
    write_registers(final, gates)
    update_artifact_registry()
    gates = make_gates(final, attempt)
    write_csv(GATE_AUDIT, gates)
    final_with_gates = {**final, "gate_passes": sum(1 for row in gates if row.get("status") == "passed"), "gate_total": len(gates)}
    write_final_and_manifest(final_with_gates, gates, attempt)
    final = read_json(FINAL_DECISION)
    write_docs(final)
    write_registers(final, gates)
    update_artifact_registry()
    validate(final, gates)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": final["status"],
                "judgment": final["judgment"],
                "result_judgment": final["result_judgment"],
                "parity_passed": final["parity_passed"],
                "rows_compared": final["rows_compared"],
                "probability_match_rows": final["probability_match_rows"],
                "input_hash_match_rows": final["input_hash_match_rows"],
                "input_hash_mismatch_rows": final["input_hash_mismatch_rows"],
                "input_hash_status": final["input_hash_status"],
                "max_abs_diff": final["python_expected_mt5_max_abs_diff"],
                "net_profit": final["net_profit"],
                "profit_factor": final["profit_factor"],
                "trade_count": final["trade_count"],
                "trade_density_per_feature_day": final["trade_density_per_feature_day"],
                "gates": f"{final['gate_passes']}/{final['gate_total']}",
                "goal_achieve": final["goal_achieve"],
                "next_run_id": final["next_run_id"],
            },
            indent=2,
            ensure_ascii=False,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
