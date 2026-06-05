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

import numpy as np
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
STAGE_ID = "351_onnx_trade_surface_rebuild__no_scaler_or_1d_scaler_runtime_contract"
RUN_NUMBER = "run351C"
RUN_ID = "run351C_execute_no_scaler_or_1d_scaler_onnx_trade_surface_mt5_probe_without_db_v1"
PARENT_RUN_ID = "run351B_rebuild_no_scaler_or_1d_scaler_onnx_trade_surface_without_db_v1"
NEXT_RUN_ID = "run351D_review_no_scaler_or_1d_scaler_onnx_trade_surface_mt5_probe_without_db_v1"

STATUS_COMPLETED = "completed_stage351C_no_scaler_1d_onnx_trade_surface_mt5_probe_executed_review_required_no_selection"
STATUS_BLOCKED = "blocked_stage351C_no_scaler_1d_onnx_trade_surface_mt5_probe_attempt_recorded_repair_required_no_selection"
CLAIM_BOUNDARY = (
    "runtime_probe_only_proxy_mt5_diff_recorded_no_candidate_selection_no_forward_pass_"
    "no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)
TRADE_DENSITY_REQUIREMENT = "trade_per_day_min_3_to_10_plus_no_trade_splitting"
PARITY_TOLERANCE = 1.0e-4

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MT5_DIR = RUN_DIR / "mt5"
SET_DIR = MT5_DIR / "sets"
INI_DIR = MT5_DIR / "inis"
TELEMETRY_COPY_DIR = RUN_DIR / "runtime_telemetry"
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_COPY_DIR = MT5_DIR / "reports"

REPORT_PATH = REVIEW_DIR / "run351C_no_scaler_1d_onnx_trade_surface_mt5_probe.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage351C_no_scaler_1d_onnx_trade_surface_mt5_probe.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"

RUN351B_DIR = STAGE_DIR / "02_runs" / "run351B"
SOURCE_FINAL_DECISION = RUN351B_DIR / "final_decision.json"
SOURCE_GATE_AUDIT = RUN351B_DIR / "required_gate_coverage_audit.csv"
SOURCE_ATTEMPT_PACKAGE = RUN351B_DIR / "runtime_probe_attempt_package.csv"
SOURCE_EXPECTED_TAPE = RUN351B_DIR / "expected" / "expected_tape.csv"
SOURCE_EXPECTED_INDEX = RUN351B_DIR / "expected" / "expected_tape_index.csv"
SOURCE_FEATURE_MANIFEST = RUN351B_DIR / "feature_matrix_manifest.csv"
SOURCE_MODEL_MANIFEST = RUN351B_DIR / "model_handoff_manifest.csv"
SOURCE_COMMON_SYNC = RUN351B_DIR / "common_files_sync.csv"
SOURCE_EA_SYNC = RUN351B_DIR / "ea_compile_and_sync_manifest.json"

ATTEMPT_PACKAGE = RUN_DIR / "runtime_probe_attempt_package.csv"
SET_RETARGET_MANIFEST = RUN_DIR / "set_retarget_manifest.csv"
INI_RETARGET_MANIFEST = RUN_DIR / "ini_retarget_manifest.csv"
TERMINAL_PROCESS_AUDIT = RUN_DIR / "terminal_process_audit.json"
MT5_EXECUTION_RESULT = RUN_DIR / "mt5_execution_result.json"
STRATEGY_TESTER_REPORTS = RUN_DIR / "strategy_tester_report_records.json"
RUNTIME_OUTPUT_COPY = RUN_DIR / "runtime_output_copy_manifest.csv"
EXECUTION_SUMMARY = RUN_DIR / "no_scaler_1d_mt5_probe_summary.csv"
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

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
ROOT_SELECTION_STATUS = ROOT / "docs" / "registers" / "selection_status.md"
ROOT_CHANGELOG = ROOT / "CHANGELOG.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

COMMON_ROOT = "Project_Obsidian_Prime_v2/stage351/run351C_no_scaler_1d_mt5_probe"
COMMON_TELEMETRY_DIR = f"{COMMON_ROOT}/telemetry"
EXPLORATION_LABEL = "stage351_ONNXTradeSurface__MT5RuntimeProbe"

INPUT_FILES = (
    SOURCE_FINAL_DECISION,
    SOURCE_GATE_AUDIT,
    SOURCE_ATTEMPT_PACKAGE,
    SOURCE_EXPECTED_TAPE,
    SOURCE_EXPECTED_INDEX,
    SOURCE_FEATURE_MANIFEST,
    SOURCE_MODEL_MANIFEST,
    SOURCE_COMMON_SYNC,
    SOURCE_EA_SYNC,
)

OUTPUT_FILES = (
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
    REPORT_PATH,
    DECISION_DOC,
    WORKSPACE_STATE,
    CURRENT_WORKING_STATE,
    SELECTION_STATUS,
    ROOT_SELECTION_STATUS,
    STAGE_LEDGER,
    RUN_REGISTRY,
    PROJECT_LEDGER,
    ARTIFACT_REGISTRY,
    Path(__file__),
)

fs_path = source_pkg.fs_path
exists = source_pkg.exists
required = source_pkg.required
ensure_parent = source_pkg.ensure_parent
rel = source_pkg.rel
sha256_file = source_pkg.sha256_file
read_json = source_pkg.read_json
write_json = source_pkg.write_json
write_csv = source_pkg.write_csv
read_csv_rows = source_pkg.read_csv_rows
write_bom_text = source_pkg.write_bom_text
append_text_once = source_pkg.append_text_once
append_or_replace_csv = source_pkg.append_or_replace_csv


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stage351C MT5 runtime probe for no-scaler/1D-scaler ONNX surfaces.")
    parser.add_argument("--terminal-path", default=str(source_pkg.DEFAULT_TERMINAL))
    parser.add_argument("--common-files-root", default=str(source_pkg.DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(source_pkg.DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-data-root", default=str(source_pkg.DEFAULT_PORTABLE_ROOT))
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--wait-timeout-seconds", type=int, default=240)
    parser.add_argument("--attempt", action="append", default=None)
    parser.add_argument("--max-attempts", type=int, default=2)
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--reuse-existing-outputs", action="store_true")
    return parser.parse_args()


def read_frame(path: Path) -> pd.DataFrame:
    return pd.read_csv(fs_path(path), encoding="utf-8-sig", low_memory=False).fillna("")


def read_text(path: Path) -> str:
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return handle.read()


def parse_set(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in read_text(path).splitlines():
        text = line.strip()
        if not text or text.startswith(";") or "=" not in text:
            continue
        key, value = text.split("=", 1)
        values[key.strip()] = value.strip()
    return values


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


def passed_gate(path: Path) -> bool:
    _fields, rows = read_csv_rows(required(path))
    return bool(rows) and all(str(row.get("status", "")).lower() == "passed" for row in rows)


def selected_source_attempts(args: argparse.Namespace) -> list[dict[str, str]]:
    _fields, rows = read_csv_rows(required(SOURCE_ATTEMPT_PACKAGE))
    if args.attempt:
        wanted = set(args.attempt)
        rows = [
            row
            for row in rows
            if row.get("attempt_name") in wanted
            or row.get("surface_id") in wanted
            or row.get("model_variant_id") in wanted
        ]
        if not rows:
            raise RuntimeError(f"no Stage351B attempts selected: {sorted(wanted)}")
    rows = sorted(rows, key=lambda row: (to_int(row.get("priority_rank")), str(row.get("probe_split"))))
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
        set_values = parse_set(required(source_set_path))
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
            "fixed_lot": set_values.get("InpFixedLot", ""),
            "max_hold_bars": set_values.get("InpMaxHoldBars", ""),
            "max_concurrent_positions": set_values.get("InpMaxConcurrentPositions", ""),
            "close_on_flat_signal": set_values.get("InpCloseOnFlatSignal", ""),
            "reverse_on_opposite_signal": set_values.get("InpReverseOnOppositeSignal", ""),
            "claim_boundary": CLAIM_BOUNDARY,
        }
        attempts.append(attempt)
        set_rows.append(
            {
                "attempt_name": attempt_name,
                "source_set_path": rel(source_set_path),
                "stage351c_set_path": rel(set_path),
                "set_sha256": set_payload["sha256"],
                "telemetry_path": common_telemetry,
                "effect": "retargeted_set_separates_stage351c_runtime_outputs",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        ini_rows.append(
            {
                "attempt_name": attempt_name,
                "source_ini_path": rel(source_ini_path),
                "stage351c_ini_path": rel(ini_path),
                "ini_sha256": ini_payload["sha256"],
                "report_name": report_name,
                "from_date": source["from_date"],
                "to_date": source["to_date"],
                "effect": "retargeted_ini_separates_stage351c_strategy_report",
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
            os.unlink(fs_path(path))


def copy_runtime_outputs(common_files_root: Path, attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for attempt in attempts:
        attempt_name = str(attempt["attempt_name"])
        for key, suffix in (("common_telemetry_path", "telemetry"), ("common_summary_path", "summary")):
            source = common_files_root / Path(str(attempt[key]))
            target = TELEMETRY_COPY_DIR / f"{attempt_name}_{suffix}.csv"
            copied = False
            if exists(source):
                ensure_parent(target)
                shutil.copy2(fs_path(source), fs_path(target))
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
        expected["surface_id"].astype(str).eq(str(attempt["surface_id"]))
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


def compare_attempt(
    attempt: Mapping[str, Any],
    execution: Mapping[str, Any],
    report: Mapping[str, Any],
    expected: pd.DataFrame,
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    attempt_name = str(attempt["attempt_name"])
    expected_by_time = expected_lookup(expected, attempt)
    expected_signal_rows = sum(
        1 for row in expected_by_time.values() if str(row.get("ea_mapped_expected_label", "")).lower() != "flat"
    )
    expected_proxy_gross = sum(to_float(row.get("proxy_fixed_horizon_gross_log_return"), 0.0) for row in expected_by_time.values())
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
                "surface_id": attempt.get("surface_id", ""),
                "model_variant_id": attempt.get("model_variant_id", ""),
                "probe_split": attempt.get("probe_split", ""),
                "tester_status": execution.get("status", "not_attempted"),
                "runtime_status": execution.get("runtime_outputs", {}).get("status", "missing"),
                "report_status": report.get("status", "missing") if report else "missing",
                "blocker": execution.get("blocker", "runtime_telemetry_missing"),
                "expected_rows": len(expected_by_time),
                "expected_signal_rows": expected_signal_rows,
                "expected_proxy_gross_log_return": expected_proxy_gross,
                "telemetry_cycle_rows": 0,
                "ready_model_rows": 0,
                "matched_rows": 0,
                "probability_match_rows": 0,
                "decision_match_rows": 0,
                "input_hash_match_rows": 0,
                "expected_missing_rows": 0,
                "max_abs_probability_diff": "",
                "comparison_status": "blocked_no_runtime_telemetry",
                **report_metric_summary(metrics, feature_day_count, calendar_days),
                "claim_boundary": CLAIM_BOUNDARY,
            },
            diff_rows,
            skip_rows,
        )

    telemetry = pd.read_csv(fs_path(local_telemetry), encoding="utf-8-sig", low_memory=False).fillna("")
    cycles = telemetry[telemetry["record_type"].astype(str).str.lower().eq("cycle")].copy()
    ready = cycles[
        cycles["feature_ready"].astype(str).str.lower().eq("true")
        & cycles["model_ok"].astype(str).str.lower().eq("true")
    ].copy()
    skipped = cycles.loc[~cycles.index.isin(ready.index)].copy()
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
    input_hash_match = 0
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
        dec_ok = str(row.get("decision", "")).strip().lower() == str(exp.get("ea_mapped_expected_label", "")).strip().lower()
        hash_ok = str(row.get("input_hash", "")).strip().upper() == str(exp.get("mt5_input_hash", "")).strip().upper()
        probability_match += int(prob_ok)
        decision_match += int(dec_ok)
        input_hash_match += int(hash_ok)
        matched += int(prob_ok and dec_ok and hash_ok)
        if not hash_ok:
            attribution = "feature_input_hash_mismatch"
        elif not prob_ok:
            attribution = "onnx_runtime_probability_mismatch"
        elif not dec_ok:
            attribution = "decision_surface_mismatch"
        else:
            attribution = "matched"
        diff_rows.append(
            {
                "attempt_name": attempt_name,
                "surface_id": attempt.get("surface_id", ""),
                "source_time": source_time,
                "expected_found": True,
                "input_hash_match": hash_ok,
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
                "expected_decision": exp.get("ea_mapped_expected_label", ""),
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
    elif probability_match == len(ready) and decision_match == len(ready) and input_hash_match == len(ready):
        comparison_status = "completed_probability_decision_input_hash_parity"
    else:
        comparison_status = "completed_with_proxy_mt5_diff"
    return (
        {
            "attempt_name": attempt_name,
            "surface_id": attempt.get("surface_id", ""),
            "model_variant_id": attempt.get("model_variant_id", ""),
            "probe_split": attempt.get("probe_split", ""),
            "runtime_contract": attempt.get("runtime_contract", ""),
            "tester_status": execution.get("status", "not_attempted"),
            "runtime_status": runtime.get("status", "not_attempted"),
            "report_status": report.get("status", "missing") if report else "missing",
            "returncode": execution.get("returncode", ""),
            "blocker": execution.get("blocker", ""),
            "expected_rows": len(expected_by_time),
            "expected_signal_rows": expected_signal_rows,
            "expected_proxy_gross_log_return": expected_proxy_gross,
            "telemetry_cycle_rows": int(len(cycles)),
            "ready_model_rows": int(len(ready)),
            "matched_rows": matched,
            "probability_match_rows": probability_match,
            "decision_match_rows": decision_match,
            "input_hash_match_rows": input_hash_match,
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


def compare_outputs(
    attempts: Sequence[Mapping[str, Any]],
    execution_results: Sequence[Mapping[str, Any]],
    report_records: Sequence[Mapping[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    expected = read_frame(required(SOURCE_EXPECTED_TAPE))
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
    source_final = read_json(required(SOURCE_FINAL_DECISION))
    source_ea_sync = read_json(required(SOURCE_EA_SYNC))
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
                "source_ea_compile_status": source_ea_sync.get("compile", {}).get("status", ""),
                "runtime_module_hashes": mt5.mt5_runtime_module_hashes(),
                "set_sha256": attempt.get("set_sha256", ""),
                "ini_sha256": attempt.get("ini_sha256", ""),
                "model_common_path": attempt.get("model_common_path", ""),
                "feature_csv_path": attempt.get("feature_csv_path", ""),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(RUNTIME_IDENTITY, rows)


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
        if str(row.get("comparison_status")) == "completed_probability_decision_input_hash_parity"
    ]
    positive_runtime_probe = (
        completed
        and parity_rows
        and to_float(best.get("net_profit"), 0.0) > 0.0
        and to_float(best.get("profit_factor"), 0.0) > 1.0
        and to_float(best.get("trade_density_per_feature_day"), 0.0) >= 3.0
    )
    if completed and positive_runtime_probe:
        judgment = "runtime_probe_positive_but_not_selected_mt5_review_required"
    elif completed:
        judgment = "runtime_probe_completed_weak_or_negative_mt5_review_required"
    else:
        judgment = "blocked_runtime_probe_outputs_missing_or_terminal_failed"
    status = STATUS_COMPLETED if completed else STATUS_BLOCKED
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "status": status,
        "judgment": judgment,
        "result_judgment": "runtime_probe" if completed else "blocked",
        "decision": "stage351C_open_run351D_review_runtime_probe",
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "attempt_rows": len(attempts),
        "source_attempt_rows": len(read_csv_rows(required(SOURCE_ATTEMPT_PACKAGE))[1]),
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
        "best_surface_id": best.get("surface_id", ""),
        "best_model_variant_id": best.get("model_variant_id", ""),
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
        gate_row("source_run351B_gates_passed", passed_gate(SOURCE_GATE_AUDIT), rel(SOURCE_GATE_AUDIT), "Stage351B handoff is gated before runtime execution."),
        gate_row("runtime_evidence_gate", runtime_ok, rel(MT5_EXECUTION_RESULT), "MT5 runtime outputs exist for attempted rows."),
        gate_row("strategy_report_forensics_gate", final["report_available_rows"] == final["attempt_rows"] and final["attempt_rows"] > 0, rel(STRATEGY_TESTER_REPORTS), "Strategy Tester reports were collected."),
        gate_row("scope_completion_gate", final["execution_result_rows"] == final["attempt_rows"] and final["attempt_rows"] > 0, rel(MT5_EXECUTION_RESULT), "All selected Stage351C attempts have execution records."),
        gate_row("kpi_contract_audit", exists(EXECUTION_SUMMARY) and final["summary_rows"] == final["attempt_rows"], rel(EXECUTION_SUMMARY), "MT5 KPI, risk, and trade density fields were written."),
        gate_row("proxy_mt5_diff_attribution_recorded", exists(PROXY_MT5_DIFF), rel(PROXY_MT5_DIFF), "Proxy-vs-MT5 row differences were recorded for attribution."),
        gate_row("trade_density_requirement_evaluated", exists(EXECUTION_SUMMARY), rel(EXECUTION_SUMMARY), "3-to-10+ trade/day and no trade splitting guardrails were evaluated."),
        gate_row("runtime_identity_recorded", exists(RUNTIME_IDENTITY), rel(RUNTIME_IDENTITY), "Terminal, model, feature, set, ini, and EA identities were recorded."),
        gate_row("artifact_lineage_recorded", exists(LINEAGE_RECEIPT) and exists(RUN_MANIFEST), f"{rel(LINEAGE_RECEIPT)};{rel(RUN_MANIFEST)}", "Artifact lineage connects source package, runtime outputs, and reports."),
        gate_row("tier_pair_rows_written", exists(STAGE_LEDGER) and exists(PROJECT_LEDGER), f"{rel(STAGE_LEDGER)};{rel(PROJECT_LEDGER)}", "Tier A/B/A+B ledger rows exist."),
        gate_row("final_claim_guard", no_forbidden, rel(FINAL_DECISION), "No operating or goal-achieve claim is made."),
    ]


def artifact_paths() -> list[Path]:
    paths = list(OUTPUT_FILES)
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
            "shared_contract": "58_feature_order_softmax_output_threshold_margin_matrix_tensor",
            "known_differences": "Stage351C uses MT5 Strategy Tester fills; proxy fixed-horizon EV is scout-only.",
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
            "next_condition": NEXT_RUN_ID,
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
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in artifact_paths() if exists(path)],
            "artifact_hashes": {rel(path): sha256_file(path) for path in artifact_paths() if exists(path) and path.is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "generated_with_manifest",
            "lineage_judgment": "connected_with_runtime_probe_boundary",
        },
    )


def write_final_manifest(final_seed: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    final = {
        **dict(final_seed),
        "gate_passes": sum(1 for gate in gates if gate.get("status") == "passed"),
        "gate_total": len(gates),
        "created_at_utc": now_utc(),
    }
    write_json(FINAL_DECISION, final)
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "run_number": RUN_NUMBER,
            "parent_run_id": PARENT_RUN_ID,
            "script": rel(Path(__file__)),
            "created_at_utc": now_utc(),
            "work_family": "runtime_backtest",
            "primary_skill": "obsidian-runtime-parity",
            "support_skills": ["obsidian-backtest-forensics", "obsidian-artifact-lineage", "obsidian-result-judgment"],
            "inputs": [rel(path) for path in INPUT_FILES],
            "outputs": [rel(path) for path in artifact_paths() if exists(path)],
            "external_verification_status": final["external_verification_status"],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    return final


def write_docs(final: Mapping[str, Any]) -> None:
    report = f"""# run351C No-Scaler/1D-Scaler ONNX MT5 Probe(351C 실행 스케일러 없음/1차원 스케일러 온엑스 MT5 탐침)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- gates(게이트): `{final['gate_passes']}/{final['gate_total']}`
- attempts(시도): `{final['attempt_rows']}` of source `{final['source_attempt_rows']}`
- runtime_completed_rows(런타임 완료 행): `{final['runtime_completed_rows']}`
- report_available_rows(보고서 확보 행): `{final['report_available_rows']}`
- proxy_mt5_parity_pass_rows(프록시-MT5 동등성 통과 행): `{final['proxy_mt5_parity_pass_rows']}`
- best_attempt(최상위 시도): `{final['best_attempt_name']}`
- best_split(최상위 분할): `{final['best_probe_split']}`
- best_net_profit(최상위 순수익): `{final['best_net_profit']}`
- best_profit_factor(최상위 수익 팩터): `{final['best_profit_factor']}`
- best_expectancy(최상위 기대값): `{final['best_expectancy']}`
- best_recovery_factor(최상위 회복 계수): `{final['best_recovery_factor']}`
- best_trade_count(최상위 거래 수): `{final['best_trade_count']}`
- best_trade_density_per_feature_day(최상위 피처일 거래 밀도): `{final['best_trade_density_per_feature_day']}`
- trade_density_status(거래 밀도 상태): `{final['best_trade_density_requirement_status']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`

Action(행동): Stage351B(351B 실행)의 ONNX(온엑스) handoff(인계)를 MT5 Strategy Tester(MT5 전략 테스터)에서 실행했다.

Effect(효과): proxy expected value(프록시 예상값)를 MT5 runtime telemetry(MT5 런타임 기록)와 Strategy Tester report(전략 테스터 보고서)로 비교할 수 있게 했다.

Boundary(경계): 이 결과는 runtime_probe(런타임 탐침)이며 candidate selection(후보 선택), operating promotion(운영 승격), runtime authority(런타임 권위), goal achieve(목표 달성)가 아니다.
"""
    decision = f"""# Stage351C Decision(351C 결정)

- decision(결정): `{final['decision']}`
- judgment(판정): `{final['judgment']}`
- external_verification_status(외부 검증 상태): `{final['external_verification_status']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- evidence(근거): `{rel(EXECUTION_SUMMARY)}`, `{rel(PROXY_MT5_DIFF)}`, `{rel(STRATEGY_TESTER_REPORTS)}`

Action(행동): MT5 runtime probe(MT5 런타임 탐침)를 실행하고 차이(diff, 차이)를 기록했다.
Effect(효과): Stage351D(351D 실행)는 수익 구조, 밀도, 동등성 차이를 보고 공격 탐색 또는 수리 방향을 고를 수 있다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    current = f"""# Current Working State(현재 작업 상태)

- current_stage_id(현재 단계 ID): `{STAGE_ID}`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- current_status(현재 상태): `{final['status']}`
- current_judgment(현재 판정): `{final['judgment']}`
- current_decision(현재 결정): `{final['decision']}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): Stage351C(351C 실행)에서 MT5 runtime probe(MT5 런타임 탐침)를 수행했다.

Effect(효과): Stage351D(351D 실행)는 proxy-vs-MT5 diff(프록시-MT5 차이), trade density(거래 밀도), report KPI(보고서 핵심 성과 지표)를 리뷰한다.
"""
    selection = f"""# Stage351 Selection Status(351단계 선택 상태)

- selection_status(선택 상태): `no_selection(선택 없음)`
- active_stage_id(활성 단계 ID): `{STAGE_ID}`
- latest_run_id(최근 실행 ID): `{RUN_ID}`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- best_attempt(최상위 시도): `{final['best_attempt_name']}`
- best_net_profit(최상위 순수익): `{final['best_net_profit']}`
- best_profit_factor(최상위 수익 팩터): `{final['best_profit_factor']}`
- best_trade_count(최상위 거래 수): `{final['best_trade_count']}`
- runtime_authority(런타임 권위): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
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
    append_text_once(
        STAGE_BRIEF,
        "## run351C No-Scaler/1D-Scaler ONNX MT5 Probe",
        f"""## run351C No-Scaler/1D-Scaler ONNX MT5 Probe(351C 실행 스케일러 없음/1차원 스케일러 온엑스 MT5 탐침)

- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- judgment(판정): `{final['judgment']}`
- attempts(시도): `{final['attempt_rows']}`
- runtime_completed_rows(런타임 완료 행): `{final['runtime_completed_rows']}`
- best_attempt(최상위 시도): `{final['best_attempt_name']}`
""",
    )
    changelog = f"""## {TODAY} run351C No-Scaler/1D-Scaler ONNX MT5 Probe

- action(행동): Stage351B(351B 실행)의 ONNX(온엑스) 시도 `{final['attempt_rows']}`개를 MT5 runtime probe(MT5 런타임 탐침)로 실행했다.
- effect(효과): best_attempt(최상위 시도) `{final['best_attempt_name']}`, net_profit(순수익) `{final['best_net_profit']}`, PF(수익 팩터) `{final['best_profit_factor']}`, density(밀도) `{final['best_trade_density_per_feature_day']}`를 기록했다.
- boundary(경계): no selection(선택 없음), no operating promotion(운영 승격 없음), no goal achieve(목표 달성 없음).
"""
    append_text_once(ROOT_CHANGELOG, "## 2026-06-01 run351C No-Scaler/1D-Scaler ONNX MT5 Probe", changelog)
    append_text_once(WORKSPACE_CHANGELOG, "## 2026-06-01 run351C No-Scaler/1D-Scaler ONNX MT5 Probe", changelog)


def write_registers(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "run_date": TODAY,
        "date": TODAY,
        "status": final["status"],
        "judgment": final["judgment"],
        "result_judgment": final["result_judgment"],
        "decision": final["decision"],
        "next_run_id": NEXT_RUN_ID,
        "primary_artifact": rel(FINAL_DECISION),
        "path": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "primary_report": rel(REPORT_PATH),
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
        "scoreboard_lane": "runtime_probe",
        "lane": "runtime_probe",
        "family": "runtime_backtest",
        "attempt_count": final["attempt_rows"],
        "external_verification_status": final["external_verification_status"],
        "net_profit": final["best_net_profit"],
        "profit_factor": final["best_profit_factor"],
        "expectancy": final["best_expectancy"],
        "drawdown": final["best_max_drawdown_amount"],
        "recovery_factor": final["best_recovery_factor"],
        "trade_count": final["best_trade_count"],
        "matched_rows": final["matched_rows"],
        "trade_density_per_feature_day": final["best_trade_density_per_feature_day"],
        "trade_density_requirement_status": final["best_trade_density_requirement_status"],
        "candidate_model_id": final["best_model_variant_id"],
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [base])
    ledger_rows = [
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__Tier A",
            "subrun_id": "Tier A",
            "view": "Tier A used(Tier A 사용)",
            "record_view": "Tier A used(Tier A 사용)",
            "tier": "Tier A",
            "tier_scope": "Tier A",
            "metric_scope": "mt5_runtime_probe",
            "kpi_scope": "mt5_runtime_probe",
            "primary_kpi": f"net_profit={final['best_net_profit']};pf={final['best_profit_factor']};trades={final['best_trade_count']}",
            "guardrail_kpi": f"density={final['best_trade_density_per_feature_day']};long_short={final['best_long_trade_count']}/{final['best_short_trade_count']};drawdown={final['best_max_drawdown_amount']}",
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__Tier B",
            "subrun_id": "Tier B",
            "view": "Tier B fallback used(Tier B 대체 사용)",
            "record_view": "Tier B fallback used(Tier B 대체 사용)",
            "tier": "Tier B",
            "tier_scope": "Tier B",
            "metric_scope": "missing_required",
            "kpi_scope": "missing_required",
            "result_status": "missing_required",
            "net_profit": "",
            "profit_factor": "",
            "expectancy": "",
            "drawdown": "",
            "recovery_factor": "",
            "trade_count": "",
            "primary_kpi": "missing_required",
            "guardrail_kpi": "missing_required",
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__Tier A+B",
            "subrun_id": "Tier A+B",
            "view": "Tier A+B combined(Tier A+B 합산)",
            "record_view": "Tier A+B combined(Tier A+B 합산)",
            "tier": "Tier A+B",
            "tier_scope": "Tier A+B",
            "metric_scope": "actual_routed_total_same_as_tier_a_no_fallback",
            "kpi_scope": "mt5_runtime_probe",
            "result_status": "same_as_tier_a_no_fallback",
        },
    ]
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], ledger_rows)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], ledger_rows)


def update_artifact_registry() -> None:
    rows = []
    for path in artifact_paths():
        if not exists(path):
            continue
        rows.append(
            {
                "artifact_id": f"{RUN_ID}__{rel(path).replace('/', '__').replace('.', '_')}",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": path.suffix.lstrip(".") or "artifact",
                "path": rel(path),
                "artifact_path": rel(path),
                "sha256": sha256_file(path) if path.is_file() else "",
                "created_at": TODAY,
                "created_at_utc": now_utc(),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def validate_or_raise(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    missing = [rel(path) for path in [FINAL_DECISION, RUN_MANIFEST, GATE_AUDIT, REPORT_PATH, EXECUTION_SUMMARY, PROXY_MT5_DIFF] if not exists(path)]
    if missing:
        raise FileNotFoundError("missing generated output: " + ", ".join(missing))
    failed = [gate for gate in gates if gate.get("status") != "passed"]
    if failed and not str(final.get("status", "")).startswith("blocked_"):
        write_json(
            SELF_CORRECTION_PLAN,
            {
                "run_id": RUN_ID,
                "failed_gates": failed,
                "mode": "plan_only",
                "repair_plan": [
                    "inspect terminal process audit",
                    "inspect MT5 execution logs",
                    "retry blocked attempts only after runtime handoff repair",
                ],
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
        raise RuntimeError("required gate audit failed: " + ", ".join(str(gate.get("gate_id")) for gate in failed))


def main() -> None:
    args = parse_args()
    for directory in [RUN_DIR, MT5_DIR, SET_DIR, INI_DIR, TELEMETRY_COPY_DIR, REPORT_COPY_DIR, REVIEW_DIR, DECISION_DOC.parent]:
        os.makedirs(fs_path(directory), exist_ok=True)
    for path in INPUT_FILES:
        required(path)
    attempts = materialize_attempts(args)
    execution_results, report_records, copy_rows = execute_attempts(args, attempts)
    summaries, diffs, _skips = compare_outputs(attempts, execution_results, report_records)
    final_seed = build_final(args, attempts, execution_results, report_records, summaries, diffs, copy_rows)
    write_receipts(final_seed)
    gates = make_gates(final_seed)
    write_csv(GATE_AUDIT, gates)
    final = write_final_manifest(final_seed, gates)
    write_docs(final)
    write_registers(final, gates)
    update_artifact_registry()
    write_receipts(final)
    gates = make_gates(final)
    write_csv(GATE_AUDIT, gates)
    final = write_final_manifest(final, gates)
    write_docs(final)
    write_registers(final, gates)
    update_artifact_registry()
    validate_or_raise(final, gates)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": final["status"],
                "judgment": final["judgment"],
                "attempt_rows": final["attempt_rows"],
                "runtime_completed_rows": final["runtime_completed_rows"],
                "report_available_rows": final["report_available_rows"],
                "proxy_mt5_parity_pass_rows": final["proxy_mt5_parity_pass_rows"],
                "best_attempt_name": final["best_attempt_name"],
                "best_net_profit": final["best_net_profit"],
                "best_profit_factor": final["best_profit_factor"],
                "best_trade_count": final["best_trade_count"],
                "best_trade_density_per_feature_day": final["best_trade_density_per_feature_day"],
                "gates": f"{final['gate_passes']}/{final['gate_total']}",
                "goal_achieve": final["goal_achieve"],
                "next_run_id": NEXT_RUN_ID,
            },
            indent=2,
            ensure_ascii=False,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
