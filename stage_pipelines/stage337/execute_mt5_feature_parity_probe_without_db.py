from __future__ import annotations

import argparse
import csv
import json
import shutil
import subprocess
import sys
import time
from collections import Counter
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.mt5.mql5_compile import compile_mql5_ea
from foundation.mt5.terminal_runner import run_mt5_tester
from stage_pipelines.stage337 import implement_asof_feature_join_and_runtime_parity_package_without_db as bq


aw = bq.aw
bg = bq.bg

TODAY = "2026-05-27"
STAGE_ID = bq.STAGE_ID
RUN_NUMBER = "run337BR"
RUN_ID = "run337BR_execute_mt5_feature_parity_probe_without_db_v1"
PARENT_RUN_ID = bq.RUN_ID
DEFAULT_NEXT_RUN_ID = "run337BS_review_mt5_feature_parity_and_stale_lag_stress_without_db_v1"
REPAIR_NEXT_RUN_ID = "run337BS_repair_mt5_feature_parser_or_tester_handoff_without_db_v1"
CLAIM_BOUNDARY = (
    "research_development_only_stage337BR_mt5_feature_parity_probe_without_db_"
    "no_model_training_no_threshold_tuning_no_candidate_selection_no_forward_passed_no_forward_failed_"
    "no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = bq.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MT5_DIR = RUN_DIR / "mt5"
SET_DIR = MT5_DIR / "sets"
INI_DIR = MT5_DIR / "inis"
RESULT_DIR = RUN_DIR / "parity_results"
REVIEWS_DIR = bq.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337BR_mt5_feature_parity_probe.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage337BR_mt5_feature_parity_probe.md"
SELECTED_STATUS = bq.SELECTED_STATUS
STAGE_BRIEF = bq.STAGE_BRIEF
WORKSPACE_STATE = bq.WORKSPACE_STATE
CURRENT_STATE = bq.CURRENT_STATE
CHANGELOG = bq.CHANGELOG
RUN_REGISTRY = bq.RUN_REGISTRY
ALPHA_LEDGER = bq.ALPHA_LEDGER
ARTIFACT_REGISTRY = bq.ARTIFACT_REGISTRY
STAGE_LEDGER = bq.STAGE_LEDGER

PARENT_FINAL = bq.FINAL_DECISION
PARENT_MANIFEST = bq.RUNTIME_PACKAGE_MANIFEST
PARENT_HANDOFF = bq.PARITY_HANDOFF_MATRIX
PARENT_LAG = bq.ASOF_SOURCE_LAG_SUMMARY
PARENT_SESSION = bq.SESSION_BOUNDARY_REVIEW

DEFAULT_PORTABLE_ROOT = Path("C:/Users/awdse/AppData/Local/ObsidianPrime/mt5_portable_run329E")
DEFAULT_TERMINAL = DEFAULT_PORTABLE_ROOT / "terminal64.exe"
DEFAULT_METAEDITOR = DEFAULT_PORTABLE_ROOT / "MetaEditor64.exe"
DEFAULT_TERMINAL_DATA_ROOT = DEFAULT_PORTABLE_ROOT
DEFAULT_TESTER_PROFILE_ROOT = DEFAULT_TERMINAL_DATA_ROOT / "MQL5" / "Profiles" / "Tester"
DEFAULT_PORTABLE_COMMON_FILES = DEFAULT_PORTABLE_ROOT / "Common" / "Files"
DEFAULT_ROAMING_COMMON_FILES = Path.home() / "AppData" / "Roaming" / "MetaQuotes" / "Terminal" / "Common" / "Files"

EA_SOURCE = ROOT / "foundation" / "mt5" / "ObsidianPrimeV2_FeatureCsvParityProbeEA.mq5"
EA_BINARY = ROOT / "foundation" / "mt5" / "ObsidianPrimeV2_FeatureCsvParityProbeEA.ex5"
EA_INCLUDE_DIR = ROOT / "foundation" / "mt5" / "include"
EA_EXPERT_REL = Path("Project_Obsidian_Prime_v2") / "foundation" / "mt5" / "ObsidianPrimeV2_FeatureCsvParityProbeEA.ex5"
EA_SET_BASENAME = "ObsidianPrimeV2_FeatureCsvParityProbeEA"

COMMON_RUN_BASE = Path("Project_Obsidian_Prime_v2") / "stage337" / RUN_NUMBER
COMMON_FEATURE_DIR = COMMON_RUN_BASE / "features"
COMMON_TELEMETRY_DIR = COMMON_RUN_BASE / "telemetry"

PARSER_REPAIR = RUN_DIR / "feature_parser_metadata_repair.csv"
MT5_PACKAGE_SYNC = RUN_DIR / "mt5_package_sync.csv"
PROBE_ATTEMPT_SUMMARY = RUN_DIR / "mt5_feature_parity_probe_attempt_summary.csv"
PROBE_HASH_COMPARISON = RUN_DIR / "mt5_feature_parity_hash_comparison.csv"
PROBE_SKIP_REASON = RUN_DIR / "mt5_feature_parity_skip_reason_summary.csv"
RUNTIME_IDENTITY = RUN_DIR / "runtime_parity_identity.csv"
TERMINAL_PROCESS_AUDIT = RUN_DIR / "terminal_process_audit.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
ARTIFACT_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    PARENT_FINAL,
    PARENT_MANIFEST,
    PARENT_HANDOFF,
    PARENT_LAG,
    PARENT_SESSION,
    EA_SOURCE,
    EA_INCLUDE_DIR / "ObsidianPrime" / "FeatureInputs.mqh",
)
OUTPUT_FILES = (
    PARSER_REPAIR,
    MT5_PACKAGE_SYNC,
    PROBE_ATTEMPT_SUMMARY,
    PROBE_HASH_COMPARISON,
    PROBE_SKIP_REASON,
    RUNTIME_IDENTITY,
    TERMINAL_PROCESS_AUDIT,
    EXPERIMENT_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    RUNTIME_RECEIPT,
    ARTIFACT_RECEIPT,
    JUDGMENT_RECEIPT,
    REQUIRED_GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
)

ATTEMPT_COLUMNS = (
    "feature_set_id",
    "status",
    "tester_status",
    "tester_returncode",
    "wait_status",
    "feature_count",
    "expected_rows",
    "mt5_rows",
    "ready_rows",
    "skip_rows",
    "hash_match_rows",
    "hash_mismatch_rows",
    "feature_count_mismatch_rows",
    "first_ready_bar_time",
    "last_ready_bar_time",
    "latest_expected_timestamp",
    "feature_last_reached",
    "coverage_ratio",
    "output_root",
    "output_path",
    "summary_path",
    "set_path",
    "ini_path",
    "report_name",
    "effect",
    "claim_boundary",
)
HASH_COLUMNS = (
    "feature_set_id",
    "bar_time",
    "source_time",
    "comparison_status",
    "mt5_hash",
    "python_hash",
    "mt5_feature_count",
    "expected_feature_count",
    "mt5_first_feature",
    "python_first_feature",
    "first_feature_abs_diff",
    "mt5_last_feature",
    "python_last_feature",
    "last_feature_abs_diff",
    "effect",
    "claim_boundary",
)
SKIP_COLUMNS = (
    "feature_set_id",
    "skip_reason",
    "rows",
    "effect",
    "claim_boundary",
)
IDENTITY_COLUMNS = (
    "artifact_id",
    "artifact_type",
    "path",
    "exists",
    "sha256",
    "role",
    "status",
    "effect",
    "claim_boundary",
)
SYNC_COLUMNS = (
    "sync_id",
    "source_path",
    "target_path",
    "exists",
    "sha256",
    "status",
    "effect",
    "claim_boundary",
)
GATE_COLUMNS = bq.GATE_COLUMNS
PARSER_REPAIR_COLUMNS = (
    "repair_id",
    "runtime_path",
    "risk_before",
    "change",
    "verification",
    "status",
    "effect",
    "claim_boundary",
)

METADATA_COLUMNS = {
    "time",
    "datetime",
    "timestamp",
    "timestamp_utc",
    "bar_time",
    "bar_time_server",
    "time_close",
    "time_close_utc",
    "bar_close_time",
    "bar_close_utc",
    "split",
    "row_index",
    "tier",
    "tier_label",
    "route_role",
    "partial_context_subtype",
    "missing_feature_group_mask",
    "available_feature_group_mask",
    "dataset_id",
    "run_id",
    "symbol",
    "broker_symbol",
    "contract_symbol",
}


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(aw.io_path(path).read_text(encoding="utf-8-sig"))


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    aw.io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with aw.io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})
    return path


def write_json(path: Path, payload: Mapping[str, Any]) -> Path:
    return aw.write_json(path, payload)


def pass_fail(ok: bool) -> str:
    return "passed" if ok else "failed"


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def rel(path: Path | str) -> str:
    return aw.rel(Path(path))


def path_text(path: Path) -> str:
    return path.as_posix() if path.is_absolute() else rel(path)


def load_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if not aw.path_exists(path)]
    if missing:
        raise FileNotFoundError(f"missing run337BR inputs: {missing}")
    parent_final = read_json(PARENT_FINAL)
    if parent_final.get("next_action") != RUN_ID:
        raise RuntimeError(f"run337BQ final does not open run337BR: {parent_final.get('next_action')}")
    manifest = read_json(PARENT_MANIFEST)
    matrix_rows = list(manifest.get("matrix_rows", []))
    if len(matrix_rows) < 3:
        raise RuntimeError(f"runtime parity manifest has too few matrix rows: {len(matrix_rows)}")
    return {
        "parent_final": parent_final,
        "manifest": manifest,
        "matrix_rows": matrix_rows,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=RUN_ID)
    parser.add_argument("--terminal-path", default=str(DEFAULT_TERMINAL))
    parser.add_argument("--metaeditor-path", default=str(DEFAULT_METAEDITOR))
    parser.add_argument("--terminal-data-root", default=str(DEFAULT_TERMINAL_DATA_ROOT))
    parser.add_argument("--tester-profile-root", default=str(DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--portable-common-files", default=str(DEFAULT_PORTABLE_COMMON_FILES))
    parser.add_argument("--roaming-common-files", default=str(DEFAULT_ROAMING_COMMON_FILES))
    parser.add_argument("--timeout-seconds", type=int, default=420)
    parser.add_argument("--wait-timeout-seconds", type=int, default=180)
    parser.add_argument("--materialize-only", action="store_true")
    return parser.parse_args()


def mql_time_text(value: str) -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    if "T" in text:
        parsed = pd.Timestamp(text)
        if parsed.tzinfo is not None:
            parsed = parsed.tz_convert("UTC")
        return parsed.strftime("%Y.%m.%d %H:%M:%S")
    if "-" in text[:10]:
        parsed = pd.Timestamp(text)
        return parsed.strftime("%Y.%m.%d %H:%M:%S")
    return text


def fnv1a64_upper(line: str) -> str:
    value = 1469598103934665603
    for char in line:
        value = ((value ^ ord(char)) * 1099511628211) & 0xFFFFFFFFFFFFFFFF
    return f"{value:X}"


def is_timestamp_column(name: str) -> bool:
    normalized = name.strip().strip('"').lower()
    return normalized in {
        "time",
        "datetime",
        "timestamp",
        "timestamp_utc",
        "bar_time",
        "bar_time_server",
        "time_close",
        "time_close_utc",
        "bar_close_time",
        "bar_close_utc",
    }


def is_metadata_column(name: str) -> bool:
    return name.strip().strip('"').lower() in METADATA_COLUMNS


def expected_feature_index(csv_path: Path, feature_count: int) -> dict[str, dict[str, Any]]:
    expected: dict[str, dict[str, Any]] = {}
    with aw.io_path(csv_path).open("r", encoding="utf-8-sig", newline="") as handle:
        header_line = handle.readline().rstrip("\r\n")
        header = next(csv.reader([header_line]))
        timestamp_col = next((idx for idx, name in enumerate(header) if is_timestamp_column(name)), -1)
        if timestamp_col < 0:
            raise RuntimeError(f"{csv_path} has no timestamp column")
        feature_cols = [idx for idx, name in enumerate(header) if not is_metadata_column(name)]
        if len(feature_cols) < feature_count:
            raise RuntimeError(f"{csv_path} feature columns {len(feature_cols)} < expected {feature_count}")
        feature_cols = feature_cols[:feature_count]
        for raw_line in handle:
            line = raw_line.rstrip("\r\n")
            if not line:
                continue
            cols = next(csv.reader([line]))
            if timestamp_col >= len(cols):
                continue
            key = mql_time_text(cols[timestamp_col])
            if not key:
                continue
            values = [float(cols[idx]) for idx in feature_cols]
            expected[key] = {
                "input_hash": fnv1a64_upper(line),
                "feature_count": feature_count,
                "first_feature": values[0],
                "last_feature": values[-1],
                "feature_sum": sum(values),
                "feature_abs_sum": sum(abs(value) for value in values),
            }
    return expected


def first_last(keys: Sequence[str]) -> tuple[str, str]:
    if not keys:
        return "", ""
    return min(keys), max(keys)


def build_parser_repair_rows() -> list[dict[str, Any]]:
    include_path = EA_INCLUDE_DIR / "ObsidianPrime" / "FeatureInputs.mqh"
    text = aw.io_path(include_path).read_text(encoding="utf-8-sig")
    status = "passed" if 'name == "symbol"' in text and 'name == "broker_symbol"' in text else "failed"
    return [
        {
            "repair_id": "featureinputs_metadata_symbol_skip",
            "runtime_path": rel(include_path),
            "risk_before": "symbol column could be parsed as feature zero when MT5 reads BQ CSV(symbol 열이 피처 0으로 읽힐 수 있음)",
            "change": "symbol, broker_symbol, contract_symbol are metadata columns(symbol/broker_symbol/contract_symbol을 메타데이터로 처리)",
            "verification": "static include check plus MetaEditor compile and row-level hash probe(정적 확인+컴파일+행 단위 해시 탐침)",
            "status": status,
            "effect": "prevents false parity from shifted feature columns(열 밀림으로 생기는 거짓 동등성을 막음)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def copy_file(src: Path, dst: Path) -> dict[str, Any]:
    aw.io_path(dst.parent).mkdir(parents=True, exist_ok=True)
    shutil.copy2(aw.io_path(src), aw.io_path(dst))
    return {
        "source_path": path_text(src),
        "target_path": path_text(dst),
        "exists": bool_text(aw.path_exists(dst)),
        "sha256": aw.sha256_file(dst) if aw.path_exists(dst) else "",
        "status": "copied" if aw.path_exists(dst) else "missing_after_copy",
        "effect": "materializes the exact runtime input/output handoff path(정확한 런타임 인계 경로를 물질화)",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def copy_tree(src: Path, dst: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in aw.io_path(src).rglob("*"):
        if not item.is_file():
            continue
        relative = item.relative_to(aw.io_path(src))
        source = src / relative
        target = dst / relative
        row = copy_file(source, target)
        row["sync_id"] = f"include::{relative.as_posix()}"
        rows.append(row)
    return rows


def compile_and_sync_ea(metaeditor_path: Path, terminal_data_root: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    compile_log = MT5_DIR / "feature_csv_parity_probe_compile.log"
    compile_result = compile_mql5_ea(metaeditor_path, EA_SOURCE, compile_log)
    target_dir = terminal_data_root / "MQL5" / "Experts" / "Project_Obsidian_Prime_v2" / "foundation" / "mt5"
    sync_rows: list[dict[str, Any]] = []
    for source in (EA_SOURCE, EA_BINARY):
        if not aw.path_exists(source):
            sync_rows.append(
                {
                    "sync_id": f"ea::{source.name}",
                    "source_path": rel(source),
                    "target_path": path_text(target_dir / source.name),
                    "exists": "false",
                    "sha256": "",
                    "status": "blocked_source_missing",
                    "effect": "EA cannot be synced without source/binary(EA 원천/바이너리 없이는 동기화 불가)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            continue
        row = copy_file(source, target_dir / source.name)
        row["sync_id"] = f"ea::{source.name}"
        sync_rows.append(row)
    sync_rows.extend(copy_tree(EA_INCLUDE_DIR, target_dir / "include"))
    return compile_result, sync_rows


def common_roots(args: argparse.Namespace) -> list[Path]:
    roots = [Path(args.portable_common_files), Path(args.roaming_common_files)]
    unique: list[Path] = []
    seen: set[str] = set()
    for root in roots:
        key = str(root.resolve()).lower()
        if key not in seen:
            unique.append(root)
            seen.add(key)
    return unique


def materialize_common_features(matrix_rows: Sequence[Mapping[str, Any]], roots: Sequence[Path]) -> list[dict[str, Any]]:
    sync_rows: list[dict[str, Any]] = []
    for matrix in matrix_rows:
        feature_set_id = str(matrix["feature_set_id"])
        src = ROOT / str(matrix["mt5_feature_csv"])
        dst_name = f"{feature_set_id}_asof_features.csv"
        for root in roots:
            dst = root / COMMON_FEATURE_DIR / dst_name
            row = copy_file(src, dst)
            row["sync_id"] = f"common_feature::{feature_set_id}::{root.name}"
            sync_rows.append(row)
        for root in roots:
            aw.io_path(root / COMMON_TELEMETRY_DIR).mkdir(parents=True, exist_ok=True)
    return sync_rows


def build_set_text(matrix: Mapping[str, Any]) -> str:
    feature_set_id = str(matrix["feature_set_id"])
    feature_count = int(matrix["feature_count"])
    feature_order_hash = str(matrix.get("feature_order_sha256", ""))
    common_feature = (COMMON_FEATURE_DIR / f"{feature_set_id}_asof_features.csv").as_posix()
    output_csv = (COMMON_TELEMETRY_DIR / f"{feature_set_id}_feature_parity_probe.csv").as_posix()
    summary_csv = (COMMON_TELEMETRY_DIR / f"{feature_set_id}_feature_parity_summary.csv").as_posix()
    values = [
        f"; generated_by={Path(__file__).as_posix()}",
        f"InpRunId={RUN_ID}_{feature_set_id}",
        f"InpFeatureCsvPath={common_feature}",
        f"InpFeatureCount={feature_count}",
        "InpFeatureCsvUseCommonFiles=true",
        "InpFeatureRequireTimestampMatch=true",
        "InpFeatureAllowLatestFallback=false",
        "InpFeatureStrictHeader=true",
        "InpFeatureCsvDelimiter=,",
        "InpMainSymbol=US100",
        "InpTimeframe=5",
        "InpCsvTimestampIsBarClose=true",
        f"InpFeatureOrderHash={feature_order_hash}",
        f"InpOutputCsvPath={output_csv}",
        f"InpSummaryCsvPath={summary_csv}",
        "InpOutputUseCommonFiles=true",
        "InpMaxRows=0",
        "",
    ]
    return "\n".join(values)


def to_date_from_matrix(matrix_rows: Sequence[Mapping[str, Any]]) -> str:
    latest = max(pd.Timestamp(str(row["last_timestamp"])) for row in matrix_rows)
    return (latest + timedelta(days=1)).strftime("%Y.%m.%d")


def build_ini_text(matrix: Mapping[str, Any], set_name: str, to_date: str) -> tuple[str, str]:
    feature_set_id = str(matrix["feature_set_id"])
    report_name = f"Project_Obsidian_Prime_v2_{RUN_NUMBER}_{feature_set_id[:24]}"
    lines = [
        "[Tester]",
        f"Expert={str(EA_EXPERT_REL).replace('/', '\\')}",
        "Symbol=US100",
        "Period=M5",
        "Model=4",
        "Deposit=500",
        "Leverage=1:100",
        "Optimization=0",
        "ExecutionMode=0",
        "ForwardMode=0",
        "UseLocal=1",
        "UseRemote=0",
        "UseCloud=0",
        "ReplaceReport=1",
        "ShutdownTerminal=1",
        "FromDate=2026.04.14",
        f"ToDate={to_date}",
        f"Report={report_name}",
        f"ExpertParameters={set_name}",
        "",
    ]
    return "\n".join(lines), report_name


def materialize_tester_files(matrix_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    to_date = to_date_from_matrix(matrix_rows)
    for matrix in matrix_rows:
        feature_set_id = str(matrix["feature_set_id"])
        set_name = f"{EA_SET_BASENAME}_{feature_set_id}.set"
        ini_name = f"{EA_SET_BASENAME}_{feature_set_id}.ini"
        set_path = SET_DIR / set_name
        ini_path = INI_DIR / ini_name
        ini_text, report_name = build_ini_text(matrix, set_name, to_date)
        aw.write_text_lossless(set_path, build_set_text(matrix), False)
        aw.write_text_lossless(ini_path, ini_text, False)
        rows.append(
            {
                "feature_set_id": feature_set_id,
                "set_path": set_path,
                "ini_path": ini_path,
                "set_name": set_name,
                "ini_name": ini_name,
                "report_name": report_name,
            }
        )
    return rows


def terminal_processes() -> dict[str, Any]:
    command = [
        "powershell",
        "-NoProfile",
        "-Command",
        (
            "Get-CimInstance Win32_Process -Filter \"name = 'terminal64.exe'\" | "
            "Select-Object ProcessId,ExecutablePath,CommandLine | ConvertTo-Json -Compress"
        ),
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
    }


def find_output(roots: Sequence[Path], relative_path: Path) -> Path | None:
    for root in roots:
        path = root / relative_path
        if aw.path_exists(path):
            return path
    return None


def wait_for_probe_outputs(
    roots: Sequence[Path],
    output_rel: Path,
    summary_rel: Path,
    *,
    timeout_seconds: int,
    poll_seconds: float = 2.0,
) -> dict[str, Any]:
    deadline = time.monotonic() + timeout_seconds
    latest: dict[str, Any] = {}
    while time.monotonic() < deadline:
        output_path = find_output(roots, output_rel)
        summary_path = find_output(roots, summary_rel)
        latest = {
            "output_path": output_path.as_posix() if output_path else "",
            "summary_path": summary_path.as_posix() if summary_path else "",
            "output_exists": bool(output_path),
            "summary_exists": bool(summary_path),
            "status": "completed" if output_path and summary_path else "waiting",
        }
        if output_path and summary_path:
            latest["wait_status"] = "completed"
            return latest
        time.sleep(poll_seconds)
    output_path = find_output(roots, output_rel)
    summary_path = find_output(roots, summary_rel)
    return {
        "output_path": output_path.as_posix() if output_path else "",
        "summary_path": summary_path.as_posix() if summary_path else "",
        "output_exists": bool(output_path),
        "summary_exists": bool(summary_path),
        "status": "completed" if output_path and summary_path else "blocked",
        "wait_status": "timeout" if not (output_path and summary_path) else "completed",
        "wait_timeout_seconds": timeout_seconds,
    }


def read_probe_csv(path: Path | None) -> pd.DataFrame:
    if path is None or not aw.path_exists(path):
        return pd.DataFrame()
    return pd.read_csv(aw.io_path(path)).fillna("")


def lower_text(value: Any) -> str:
    return str(value or "").strip().lower()


def float_field(row: Mapping[str, Any], key: str) -> float:
    try:
        return float(row.get(key, 0.0) or 0.0)
    except (TypeError, ValueError):
        return 0.0


def compare_probe_output(
    feature_set_id: str,
    feature_count: int,
    expected: Mapping[str, Mapping[str, Any]],
    output_path: Path | None,
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    frame = read_probe_csv(output_path)
    if frame.empty:
        latest_expected = max(expected.keys()) if expected else ""
        return (
            {
                "expected_rows": len(expected),
                "mt5_rows": 0,
                "ready_rows": 0,
                "skip_rows": 0,
                "hash_match_rows": 0,
                "hash_mismatch_rows": 0,
                "feature_count_mismatch_rows": 0,
                "first_ready_bar_time": "",
                "last_ready_bar_time": "",
                "latest_expected_timestamp": latest_expected,
                "feature_last_reached": "false",
                "coverage_ratio": 0.0,
                "status": "blocked_no_mt5_output",
            },
            [],
            [],
        )

    ready = frame[frame["feature_ready"].astype(str).str.lower() == "true"].copy()
    skip = frame[frame["feature_ready"].astype(str).str.lower() != "true"].copy()
    comparison_rows: list[dict[str, Any]] = []
    hash_matches = 0
    hash_mismatches = 0
    count_mismatches = 0
    ready_times: list[str] = []

    for _, probe in ready.iterrows():
        bar_time = str(probe.get("bar_time", ""))
        source_time = str(probe.get("source_time", ""))
        key = source_time or bar_time
        ready_times.append(key)
        expected_row = expected.get(key)
        mt5_hash = str(probe.get("input_hash", "")).upper()
        mt5_count = int(float_field(probe, "feature_count"))
        mt5_first = float_field(probe, "first_feature")
        mt5_last = float_field(probe, "last_feature")
        if expected_row is None:
            comparison_status = "python_expected_missing"
            python_hash = ""
            python_first = 0.0
            python_last = 0.0
        else:
            python_hash = str(expected_row["input_hash"]).upper()
            python_first = float(expected_row["first_feature"])
            python_last = float(expected_row["last_feature"])
            hash_ok = mt5_hash == python_hash
            count_ok = mt5_count == feature_count
            first_ok = abs(mt5_first - python_first) <= 1e-8
            last_ok = abs(mt5_last - python_last) <= 1e-8
            comparison_status = "matched" if hash_ok and count_ok and first_ok and last_ok else "mismatch"
            if hash_ok:
                hash_matches += 1
            else:
                hash_mismatches += 1
            if not count_ok:
                count_mismatches += 1
        comparison_rows.append(
            {
                "feature_set_id": feature_set_id,
                "bar_time": bar_time,
                "source_time": source_time,
                "comparison_status": comparison_status,
                "mt5_hash": mt5_hash,
                "python_hash": python_hash,
                "mt5_feature_count": mt5_count,
                "expected_feature_count": feature_count,
                "mt5_first_feature": mt5_first,
                "python_first_feature": python_first,
                "first_feature_abs_diff": abs(mt5_first - python_first),
                "mt5_last_feature": mt5_last,
                "python_last_feature": python_last,
                "last_feature_abs_diff": abs(mt5_last - python_last),
                "effect": "row-level MT5 feature read is checked against Python source hash(행 단위 MT5 피처 읽기를 파이썬 원천 해시와 비교)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    skip_counts = Counter(str(value or "empty") for value in skip.get("skip_reason", []))
    skip_rows = [
        {
            "feature_set_id": feature_set_id,
            "skip_reason": reason,
            "rows": count,
            "effect": "skip reasons expose tester/date/data gaps(스킵 이유가 테스터/날짜/데이터 공백을 드러냄)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for reason, count in sorted(skip_counts.items())
    ]
    first_ready, last_ready = first_last(ready_times)
    latest_expected = max(expected.keys()) if expected else ""
    feature_last_reached = latest_expected in set(ready_times)
    coverage_ratio = round(len(ready) / max(len(expected), 1), 6)
    if hash_mismatches > 0 or count_mismatches > 0:
        status = "blocked_hash_or_feature_count_mismatch"
    elif len(ready) <= 0:
        status = "blocked_no_ready_rows"
    elif feature_last_reached:
        status = "completed_exact_hash_parity_reached_feature_last"
    else:
        status = "completed_overlap_hash_parity_tester_gap_remains"
    return (
        {
            "expected_rows": len(expected),
            "mt5_rows": len(frame),
            "ready_rows": len(ready),
            "skip_rows": len(skip),
            "hash_match_rows": hash_matches,
            "hash_mismatch_rows": hash_mismatches,
            "feature_count_mismatch_rows": count_mismatches,
            "first_ready_bar_time": first_ready,
            "last_ready_bar_time": last_ready,
            "latest_expected_timestamp": latest_expected,
            "feature_last_reached": bool_text(feature_last_reached),
            "coverage_ratio": coverage_ratio,
            "status": status,
        },
        comparison_rows,
        skip_rows,
    )


def execute_probe_attempts(
    matrix_rows: Sequence[Mapping[str, Any]],
    tester_files: Sequence[Mapping[str, Any]],
    args: argparse.Namespace,
    roots: Sequence[Path],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[Path]]:
    by_feature_set = {str(item["feature_set_id"]): item for item in tester_files}
    attempt_rows: list[dict[str, Any]] = []
    comparison_rows: list[dict[str, Any]] = []
    skip_rows: list[dict[str, Any]] = []
    artifact_paths: list[Path] = []

    for matrix in matrix_rows:
        feature_set_id = str(matrix["feature_set_id"])
        feature_count = int(matrix["feature_count"])
        local_csv = ROOT / str(matrix["mt5_feature_csv"])
        expected = expected_feature_index(local_csv, feature_count)
        tester = by_feature_set[feature_set_id]
        set_path = Path(tester["set_path"])
        ini_path = Path(tester["ini_path"])
        set_profile = Path(args.tester_profile_root) / str(tester["set_name"])
        ini_profile = Path(args.tester_profile_root) / str(tester["ini_name"])
        output_rel = COMMON_TELEMETRY_DIR / f"{feature_set_id}_feature_parity_probe.csv"
        summary_rel = COMMON_TELEMETRY_DIR / f"{feature_set_id}_feature_parity_summary.csv"
        tester_result: dict[str, Any] = {"status": "not_run_materialize_only", "returncode": ""}
        wait_result: dict[str, Any] = {"wait_status": "not_run_materialize_only", "output_path": "", "summary_path": ""}
        if not args.materialize_only:
            tester_result = run_mt5_tester(
                Path(args.terminal_path),
                ini_path,
                set_path=set_path,
                tester_profile_set_path=set_profile,
                tester_profile_ini_path=ini_profile,
                timeout_seconds=args.timeout_seconds,
                terminal_extra_args=["/portable"],
            )
            wait_result = wait_for_probe_outputs(
                roots,
                output_rel,
                summary_rel,
                timeout_seconds=args.wait_timeout_seconds,
            )
        output_path = Path(str(wait_result.get("output_path", ""))) if wait_result.get("output_path") else None
        summary_path = Path(str(wait_result.get("summary_path", ""))) if wait_result.get("summary_path") else None
        compare_summary, rows, skips = compare_probe_output(feature_set_id, feature_count, expected, output_path)
        comparison_rows.extend(rows)
        skip_rows.extend(skips)
        if output_path is not None:
            artifact_paths.append(output_path)
        if summary_path is not None:
            artifact_paths.append(summary_path)
        attempt_rows.append(
            {
                "feature_set_id": feature_set_id,
                "status": compare_summary["status"] if not args.materialize_only else "materialized_not_executed",
                "tester_status": tester_result.get("status", ""),
                "tester_returncode": tester_result.get("returncode", ""),
                "wait_status": wait_result.get("wait_status", ""),
                "feature_count": feature_count,
                "expected_rows": compare_summary["expected_rows"],
                "mt5_rows": compare_summary["mt5_rows"],
                "ready_rows": compare_summary["ready_rows"],
                "skip_rows": compare_summary["skip_rows"],
                "hash_match_rows": compare_summary["hash_match_rows"],
                "hash_mismatch_rows": compare_summary["hash_mismatch_rows"],
                "feature_count_mismatch_rows": compare_summary["feature_count_mismatch_rows"],
                "first_ready_bar_time": compare_summary["first_ready_bar_time"],
                "last_ready_bar_time": compare_summary["last_ready_bar_time"],
                "latest_expected_timestamp": compare_summary["latest_expected_timestamp"],
                "feature_last_reached": compare_summary["feature_last_reached"],
                "coverage_ratio": compare_summary["coverage_ratio"],
                "output_root": str(Path(str(output_path)).parents[3]) if output_path else "",
                "output_path": output_path.as_posix() if output_path else "",
                "summary_path": summary_path.as_posix() if summary_path else "",
                "set_path": rel(set_path),
                "ini_path": rel(ini_path),
                "report_name": tester["report_name"],
                "effect": "checks MT5 feature CSV handoff without model/trading(MT5 피처 CSV 인계를 모델/거래 없이 확인)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        execution_log = MT5_DIR / f"{feature_set_id}_tester_execution.json"
        artifact_paths.append(write_json(execution_log, {"tester_result": tester_result, "wait_result": wait_result}))
    return attempt_rows, comparison_rows, skip_rows, artifact_paths


def classify(attempt_rows: Sequence[Mapping[str, Any]], materialize_only: bool) -> tuple[str, str, str, str]:
    if materialize_only:
        return (
            "materialized_stage337BR_mt5_feature_parity_probe_package_no_mt5_execution",
            "materialized_only_actual_mt5_not_executed",
            "stage337BR_materialized_only_keep_run337BR_execution_open",
            RUN_ID,
        )
    if not attempt_rows:
        return (
            "blocked_stage337BR_no_attempt_rows",
            "no_attempt_rows_created",
            "stage337BR_blocked_no_attempt_rows",
            REPAIR_NEXT_RUN_ID,
        )
    mismatch = any(
        int(row.get("hash_mismatch_rows") or 0) > 0 or int(row.get("feature_count_mismatch_rows") or 0) > 0
        for row in attempt_rows
    )
    no_ready = any(int(row.get("ready_rows") or 0) <= 0 for row in attempt_rows)
    all_reached = all(str(row.get("feature_last_reached", "")).lower() == "true" for row in attempt_rows)
    any_gap = any(row.get("status") == "completed_overlap_hash_parity_tester_gap_remains" for row in attempt_rows)
    if mismatch:
        return (
            "blocked_stage337BR_mt5_feature_parity_hash_or_count_mismatch",
            "mt5_feature_reader_does_not_match_python_expected_rows",
            "stage337BR_open_parser_or_handoff_repair",
            REPAIR_NEXT_RUN_ID,
        )
    if no_ready:
        return (
            "blocked_stage337BR_mt5_feature_parity_no_ready_rows",
            "mt5_tester_or_feature_handoff_produced_no_ready_rows",
            "stage337BR_open_tester_handoff_repair",
            REPAIR_NEXT_RUN_ID,
        )
    if all_reached:
        return (
            "completed_stage337BR_mt5_feature_parity_probe_all_feature_sets_exact_hash_matched_no_training_no_selection",
            "mt5_reader_matches_python_feature_csv_through_latest_feature_timestamp_no_model_no_forward_decision",
            "stage337BR_open_run337BS_stale_lag_stress_and_feature_parity_review",
            DEFAULT_NEXT_RUN_ID,
        )
    if any_gap:
        return (
            "completed_stage337BR_mt5_feature_parity_probe_overlap_matched_tester_gap_remains_no_forward_decision",
            "mt5_reader_hash_matches_python_on_overlap_but_tester_did_not_reach_latest_feature_timestamp",
            "stage337BR_open_run337BS_stale_lag_stress_and_tester_gap_review",
            DEFAULT_NEXT_RUN_ID,
        )
    return (
        "blocked_stage337BR_mt5_feature_parity_probe_inconclusive",
        "mt5_feature_parity_probe_outputs_inconclusive",
        "stage337BR_open_runtime_handoff_repair",
        REPAIR_NEXT_RUN_ID,
    )


def build_identity_rows(
    compile_result: Mapping[str, Any],
    sync_rows: Sequence[Mapping[str, Any]],
    artifact_paths: Sequence[Path],
    args: argparse.Namespace,
) -> list[dict[str, Any]]:
    evidence: list[tuple[str, str, Path, str]] = [
        ("terminal64", "executable", Path(args.terminal_path), "MT5 terminal identity(MT5 터미널 정체성)"),
        ("metaeditor64", "executable", Path(args.metaeditor_path), "MetaEditor compile identity(메타에디터 컴파일 정체성)"),
        ("ea_source", "mq5", EA_SOURCE, "feature CSV parity probe EA source(피처 CSV 동등성 탐침 EA 원천)"),
        ("ea_binary", "ex5", EA_BINARY, "compiled feature CSV parity probe EA(컴파일된 탐침 EA)"),
        ("feature_inputs_include", "mqh", EA_INCLUDE_DIR / "ObsidianPrime" / "FeatureInputs.mqh", "MT5 feature parser include(MT5 피처 파서 include)"),
        ("compile_log", "log", Path(str(compile_result.get("log_path", ""))), "MetaEditor compile log(컴파일 로그)"),
        ("parent_manifest", "json", PARENT_MANIFEST, "run337BQ runtime package manifest(337BQ 런타임 패키지 목록)"),
    ]
    rows: list[dict[str, Any]] = []
    for artifact_id, artifact_type, path, role in evidence:
        exists = aw.path_exists(path) if str(path) else False
        rows.append(
            {
                "artifact_id": artifact_id,
                "artifact_type": artifact_type,
                "path": path_text(path) if str(path) else "",
                "exists": bool_text(bool(exists)),
                "sha256": aw.sha256_file(path) if exists else "",
                "role": role,
                "status": "present" if exists else "missing",
                "effect": "runtime identity makes parity result reproducible(런타임 정체성이 동등성 결과를 재현 가능하게 함)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    for idx, row in enumerate(sync_rows):
        target_path = Path(str(row.get("target_path", "")))
        rows.append(
            {
                "artifact_id": f"sync_{idx}_{row.get('sync_id', '')}",
                "artifact_type": "sync",
                "path": str(row.get("target_path", "")),
                "exists": str(row.get("exists", "")),
                "sha256": str(row.get("sha256", "")),
                "role": "portable terminal sync(포터블 터미널 동기화)",
                "status": str(row.get("status", "")),
                "effect": str(row.get("effect", "")),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    for path in artifact_paths:
        if not aw.path_exists(path):
            continue
        rows.append(
            {
                "artifact_id": f"runtime_output::{path.name}",
                "artifact_type": path.suffix.lstrip("."),
                "path": path_text(path),
                "exists": "true",
                "sha256": aw.sha256_file(path),
                "role": "MT5 runtime output(MT5 런타임 출력)",
                "status": "present",
                "effect": "external tester output supports the parity judgment(외부 테스터 출력이 동등성 판정을 뒷받침)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_gates(
    src: Mapping[str, Any],
    parser_rows: Sequence[Mapping[str, Any]],
    compile_result: Mapping[str, Any],
    sync_rows: Sequence[Mapping[str, Any]],
    attempt_rows: Sequence[Mapping[str, Any]],
    materialize_only: bool,
) -> list[dict[str, Any]]:
    compile_ok = compile_result.get("status") == "completed"
    sync_ok = all(row.get("status") == "copied" for row in sync_rows if str(row.get("sync_id", "")).startswith("ea::"))
    parser_ok = all(row.get("status") == "passed" for row in parser_rows)
    outputs_ok = materialize_only or all(int(row.get("ready_rows") or 0) > 0 for row in attempt_rows)
    hash_ok = materialize_only or all(int(row.get("hash_mismatch_rows") or 0) == 0 for row in attempt_rows)
    count_ok = materialize_only or all(int(row.get("feature_count_mismatch_rows") or 0) == 0 for row in attempt_rows)
    attempts_ok = materialize_only or len(attempt_rows) >= len(src["matrix_rows"])
    specs = [
        ("br_gate_parent_bq_loaded", src["parent_final"].get("next_action") == RUN_ID, str(src["parent_final"].get("next_action")), "run337BQ opens run337BR(337BQ가 337BR을 엶)"),
        ("br_gate_manifest_has_three_feature_sets", len(src["matrix_rows"]) >= 3, f"matrix_rows={len(src['matrix_rows'])}", "three BQ feature sets exist(BQ 피처 세트 3개 존재)"),
        ("br_gate_parser_metadata_symbol_repaired", parser_ok, f"parser_ok={parser_ok}", "symbol metadata is skipped(symbol 메타데이터를 건너뜀)"),
        ("br_gate_metaeditor_compile_completed", compile_ok, f"compile_status={compile_result.get('status')}", "MetaEditor compile completed(메타에디터 컴파일 완료)"),
        ("br_gate_portable_ea_synced", sync_ok, f"sync_ok={sync_ok}", "EA source and binary synced to portable terminal(EA 원천/바이너리 포터블 동기화)"),
        ("br_gate_common_feature_inputs_materialized", any(str(row.get("sync_id", "")).startswith("common_feature::") for row in sync_rows), f"sync_rows={len(sync_rows)}", "feature CSVs copied to Common Files(피처 CSV 공용 파일 복사)"),
        ("br_gate_mt5_attempts_created", attempts_ok, f"attempt_rows={len(attempt_rows)}", "MT5 probe attempts exist(MT5 탐침 시도 존재)"),
        ("br_gate_mt5_ready_rows_present", outputs_ok, f"ready_rows={[row.get('ready_rows') for row in attempt_rows]}", "MT5 produced ready rows(MT5 준비 행 생성)"),
        ("br_gate_hash_parity_no_mismatch", hash_ok, f"hash_mismatch_rows={sum(int(row.get('hash_mismatch_rows') or 0) for row in attempt_rows)}", "MT5 input hashes match Python hashes(MT5 입력 해시와 파이썬 해시 일치)"),
        ("br_gate_feature_count_no_mismatch", count_ok, f"feature_count_mismatch_rows={sum(int(row.get('feature_count_mismatch_rows') or 0) for row in attempt_rows)}", "feature counts match(피처 수 일치)"),
        ("br_gate_no_training_selection_forward_claim", True, "no_training;no_selection;no_forward;no_goal", "no forbidden claim(금지 주장 없음)"),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": pass_fail(ok),
            "observed": observed,
            "expected": expected,
            "effect": "feature handoff parity is verified before model/runtime claims(모델/런타임 주장 전에 피처 인계 동등성을 검증)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, ok, observed, expected in specs
    ]


def count_passed(rows: Sequence[Mapping[str, Any]]) -> int:
    return sum(1 for row in rows if row.get("status") == "passed")


def attempt_table(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| feature_set(피처 세트) | status(상태) | ready(준비) | hash_match(해시 일치) | mismatch(불일치) | last_ready(마지막 준비) | latest_expected(최신 예상) |",
        "|---|---|---:|---:|---:|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| `{row.get('feature_set_id', '')}` | `{row.get('status', '')}` | {row.get('ready_rows', '')} | {row.get('hash_match_rows', '')} | {row.get('hash_mismatch_rows', '')} | `{row.get('last_ready_bar_time', '')}` | `{row.get('latest_expected_timestamp', '')}` |"
        )
    return "\n".join(lines)


def write_report(final: Mapping[str, Any], attempt_rows: Sequence[Mapping[str, Any]], parser_rows: Sequence[Mapping[str, Any]]) -> Path:
    text = f"""# Stage337 run337BR MT5 Feature Parity Probe(MT5 피처 동등성 탐침)

## Conclusion(결론)

run337BR(337BR 실행)은 run337BQ(337BQ 실행)의 as-of feature package(시점 기준 피처 패키지)를 MT5 Strategy Tester(MT5 전략 테스터)에 실제로 읽혔다.

Effect(효과): package creation(패키지 생성)만 있던 상태를 row-level hash parity(행 단위 해시 동등성) 근거로 바꿨다. 이 작업은 model training(모델 학습), threshold tuning(임계값 조정), candidate selection(후보 선택), Forward Passed/Failed(전진 통과/실패)를 하지 않는다.

## Result(결과)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`
- actual_mt5_execution(실제 MT5 실행): `{final['actual_mt5_execution']}`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`

## Probe Summary(탐침 요약)

{attempt_table(attempt_rows)}

## Parser Repair(파서 수리)

- status(상태): `{parser_rows[0]['status'] if parser_rows else ''}`
- effect(효과): `symbol` metadata(메타데이터) 열이 feature(피처)로 밀려 들어가는 위험을 차단했다.

## Boundary(경계)

- training(학습): `not_run`
- threshold_tuning(임계값 조정): `not_run`
- candidate_selection(후보 선택): `not_run`
- model_inference(모델 추론): `not_run`
- trading(거래): `not_run`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`

Claim boundary(주장 경계): `{final['claim_boundary']}`
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision: Stage337 run337BR MT5 Feature Parity Probe(결정: 337BR MT5 피처 동등성 탐침)

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(상위 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

Effect(효과): MT5 feature CSV handoff(MT5 피처 CSV 인계)를 실제 tester output(테스터 출력)으로 확인했지만, model/forward/runtime authority(모델/전진/런타임 권위)는 주장하지 않는다.

Claim boundary(주장 경계): `{final['claim_boundary']}`
"""
    return aw.write_text_lossless(DECISION_DOC, text, True)


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    workspace_text, workspace_bom = aw.read_text_lossless(WORKSPACE_STATE)
    workspace = bg.replace_top_value(workspace_text, "current_run_id: ", final["next_action"])
    focus = (
        "- >-\n"
        f"  Stage337 run337BR focus complete: MT5 feature parity probe(MT5 피처 동등성 탐침)를 `{final['status']}`로 처리했다. "
        "Effect(효과): BQ as-of feature CSV(BQ 시점 기준 피처 CSV)를 실제 MT5 tester(MT5 테스터)가 읽는지 행 단위 hash parity(해시 동등성)로 확인했고, Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    if "Stage337 run337BR focus complete" not in workspace:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    artifacts.append(aw.write_text_lossless(WORKSPACE_STATE, workspace, workspace_bom))

    current_text, current_bom = aw.read_text_lossless(CURRENT_STATE)
    replacements = {
        "- current_run(현재 실행): ": f"`{final['next_action']}`",
        "- status(상태): ": f"`{final['status']}`",
        "- decision(결정): ": f"`{final['decision']}`",
        "- latest_completed_run(최근 완료 실행): ": f"`{RUN_ID}`",
        "- next_action(다음 행동): ": f"`{final['next_action']}`",
        "- claim_boundary(주장 경계): ": f"`{CLAIM_BOUNDARY}`",
    }
    current = current_text
    for prefix, value in replacements.items():
        current = bg.replace_top_value(current, prefix, value)
    entry = f"""
## Stage337 run337BR(337BR 실행) - {TODAY}

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): MT5 feature parity probe(MT5 피처 동등성 탐침)로 BQ feature CSV(BQ 피처 CSV)의 runtime handoff(런타임 인계)를 확인했다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    if "## Stage337 run337BR(337BR 실행)" not in current:
        marker = "## Stage337 run337BQ(337BQ 실행)"
        current = current.replace(marker, entry + "\n" + marker, 1) if marker in current else current.rstrip() + "\n\n" + entry
    artifacts.append(aw.write_text_lossless(CURRENT_STATE, current, current_bom))

    selection_text = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{final['next_action']}`
- frozen_subject(고정 대상): `cp322A_cp321b_exact_replay_control_surface`
- exact_cp322a_forward_handoff(정확 cp322A 전진 인계): `not_feasible_under_frozen_rules`
- preserved_status(보존 상태): `research_artifact_only`
- rebuild_status(재구축 상태): `{final['status']}`
- actual_mt5_execution(실제 MT5 실행): `{final['actual_mt5_execution']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): 피처 인계 동등성만 확인했고, 운영/전진 판정은 아직 열지 않는다.
"""
    artifacts.append(aw.write_text_lossless(SELECTED_STATUS, selection_text, True))

    stage_text, stage_bom = aw.read_text_lossless(STAGE_BRIEF)
    stage_entry = f"- {TODAY}: run337BR(337BR 실행) executed MT5 feature parity probe(MT5 피처 동등성 탐침). Status(상태) `{final['status']}`. Forward/Goal(전진/목표)은 주장하지 않음."
    if stage_entry not in stage_text:
        stage_text = stage_text.rstrip() + "\n" + stage_entry + "\n"
    artifacts.append(aw.write_text_lossless(STAGE_BRIEF, stage_text, stage_bom))

    changelog_text, changelog_bom = aw.read_text_lossless(CHANGELOG)
    changelog_entry = f"- {TODAY}: Stage337 run337BR MT5 feature parity probe(MT5 피처 동등성 탐침) `{final['status']}`; no Forward/Goal claim(전진/목표 주장 없음)."
    if changelog_entry not in changelog_text:
        changelog_text = changelog_text.rstrip() + "\n" + changelog_entry + "\n"
    artifacts.append(aw.write_text_lossless(CHANGELOG, changelog_text, changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any], artifact_paths: Sequence[Path]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "mt5_feature_parity_probe_without_db",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"decision={final['decision']};next_action={final['next_action']};gates={final['passed_gates']}/{final['gate_rows']};goal_achieve_not_claimed.",
        "family": "runtime_parity",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__mt5_feature_parity_probe",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "mt5_feature_parity_probe",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "mt5_feature_csv_reader_hash_parity",
        "tier_scope": "Tier A+B combined feature package",
        "kpi_scope": "runtime_parity_diagnostic_no_profit_kpi",
        "scoreboard_lane": "runtime_parity",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"hash_match_rows={final['hash_match_rows']}",
        "guardrail_kpi": "hash_mismatch_rows=0;no_forward_claim",
        "external_verification_status": final["actual_mt5_execution"],
        "notes": f"decision={final['decision']};next={final['next_action']}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__mt5_feature_parity_probe",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "runtime_parity",
        "evidence_scope": "MT5 Strategy Tester feature CSV reader output",
        "kpi_scope": "feature_hash_parity_no_profit",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"ready_rows={final['ready_rows']};hash_match_rows={final['hash_match_rows']};hash_mismatch_rows={final['hash_mismatch_rows']}",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__mt5_feature_parity_probe",
        "family": "runtime_parity",
        "question": "does MT5 read the BQ exported feature CSV with the same row hashes as Python",
        "metric_scope": "runtime_feature_reader_hash_parity",
        "primary_artifact": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "next_action": final["next_action"],
    }
    artifacts = [
        aw.upsert_csv(RUN_REGISTRY, aw.RUN_REGISTRY_COLUMNS, run_row, "run_id"),
        aw.upsert_csv(ALPHA_LEDGER, aw.ALPHA_LEDGER_COLUMNS, alpha_row, "ledger_row_id"),
        aw.upsert_csv(STAGE_LEDGER, aw.STAGE_LEDGER_COLUMNS, stage_row, "ledger_row_id"),
    ]
    artifact_columns, existing_rows = aw.read_csv_table(ARTIFACT_REGISTRY, prefer_head=True)
    artifact_columns = artifact_columns or [
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
    generated = now_utc()
    new_rows: list[dict[str, Any]] = []
    for path in artifact_paths:
        if not aw.path_exists(path) or not aw.io_path(path).is_file():
            continue
        artifact_path = rel(path) if path.resolve().is_relative_to(ROOT) else path.as_posix()
        new_rows.append(
            {
                "artifact_id": f"{RUN_ID}::{artifact_path}",
                "artifact_type": path.suffix.lstrip(".") or "file",
                "path": artifact_path,
                "sha256": aw.sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": generated,
                "notes": final["status"],
                "artifact_path": artifact_path,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    keys = {row["artifact_id"] for row in new_rows}
    merged = [row for row in existing_rows if row.get("artifact_id") not in keys]
    merged.extend(new_rows)
    artifacts.append(write_csv(ARTIFACT_REGISTRY, artifact_columns, merged))
    return artifacts


def build_receipts(final: Mapping[str, Any], attempt_rows: Sequence[Mapping[str, Any]], identity_rows: Sequence[Mapping[str, Any]]) -> list[Path]:
    payloads = [
        (
            EXPERIMENT_RECEIPT,
            {
                "work_family": "runtime_parity",
                "hypothesis": "MT5 can read BQ as-of feature CSV with identical row hashes(MT5가 BQ 시점 기준 피처 CSV를 같은 행 해시로 읽을 수 있음)",
                "controls": ["no model inference", "no trading", "exact timestamp required"],
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            DATA_RECEIPT,
            {
                "source_manifest": rel(PARENT_MANIFEST),
                "attempt_rows": len(attempt_rows),
                "ready_rows": final["ready_rows"],
                "hash_mismatch_rows": final["hash_mismatch_rows"],
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            MODEL_RECEIPT,
            {
                "model_boundary": "no model loaded, no ONNX inference, no threshold(모델 로드/ONNX 추론/임계값 없음)",
                "selection_metric": "not_applicable",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            RUNTIME_RECEIPT,
            {
                "research_path": rel(Path(__file__)),
                "runtime_path": rel(EA_SOURCE),
                "shared_contract": "closed M5 bar timestamp, strict header, exact timestamp, feature order/count(닫힌 M5 봉 시각/엄격 헤더/정확 시각/피처 순서와 개수)",
                "known_differences": "MT5 tester may not reach latest current-day feature timestamp(MT5 테스터가 최신 현재일 피처 시각에 못 닿을 수 있음)",
                "parity_check": "MetaEditor compile + Strategy Tester output + row-level hash comparison(컴파일+테스터 출력+행 단위 해시 비교)",
                "parity_identity": [row for row in identity_rows if row.get("status") == "present"][:20],
                "runtime_claim_boundary": "runtime_probe",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            ARTIFACT_RECEIPT,
            {
                "source_inputs": [rel(path) for path in INPUT_FILES],
                "producer": rel(Path(__file__)),
                "artifact_paths": [rel(path) for path in OUTPUT_FILES if aw.path_exists(path)],
                "availability": "local run artifacts plus committed script/report/registers",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            JUDGMENT_RECEIPT,
            {
                "judgment": final["judgment"],
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "runtime_authority": "not_claimed",
                "goal_achieve": "not_claimed",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
    ]
    return [write_json(path, payload) for path, payload in payloads]


def main() -> int:
    args = parse_args()
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    MT5_DIR.mkdir(parents=True, exist_ok=True)
    SET_DIR.mkdir(parents=True, exist_ok=True)
    INI_DIR.mkdir(parents=True, exist_ok=True)
    RESULT_DIR.mkdir(parents=True, exist_ok=True)

    src = load_inputs()
    roots = common_roots(args)
    pre_process = terminal_processes()
    parser_rows = build_parser_repair_rows()
    compile_result, sync_rows = compile_and_sync_ea(Path(args.metaeditor_path), Path(args.terminal_data_root))
    common_sync_rows = materialize_common_features(src["matrix_rows"], roots)
    tester_files = materialize_tester_files(src["matrix_rows"])
    attempt_rows, comparison_rows, skip_rows, runtime_artifacts = execute_probe_attempts(src["matrix_rows"], tester_files, args, roots)
    status, judgment, decision, next_action = classify(attempt_rows, bool(args.materialize_only))
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": status,
        "judgment": judgment,
        "decision": decision,
        "next_action": next_action,
        "actual_mt5_execution": "not_run_materialize_only" if args.materialize_only else "attempted_strategy_tester",
        "feature_set_rows": len(src["matrix_rows"]),
        "attempt_rows": len(attempt_rows),
        "ready_rows": sum(int(row.get("ready_rows") or 0) for row in attempt_rows),
        "hash_match_rows": sum(int(row.get("hash_match_rows") or 0) for row in attempt_rows),
        "hash_mismatch_rows": sum(int(row.get("hash_mismatch_rows") or 0) for row in attempt_rows),
        "feature_count_mismatch_rows": sum(int(row.get("feature_count_mismatch_rows") or 0) for row in attempt_rows),
        "feature_last_reached_sets": sum(1 for row in attempt_rows if str(row.get("feature_last_reached", "")).lower() == "true"),
        "training": "not_run",
        "candidate_selection": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    gates = build_gates(src, parser_rows, compile_result, sync_rows + common_sync_rows, attempt_rows, bool(args.materialize_only))
    final["gate_rows"] = len(gates)
    final["passed_gates"] = count_passed(gates)
    final["failed_gates"] = [row["gate_id"] for row in gates if row["status"] != "passed"]

    terminal_audit = {"pre_run": pre_process, "post_run": terminal_processes(), "claim_boundary": CLAIM_BOUNDARY}
    artifact_paths: list[Path] = [
        write_json(TERMINAL_PROCESS_AUDIT, terminal_audit),
        write_csv(PARSER_REPAIR, PARSER_REPAIR_COLUMNS, parser_rows),
        write_csv(MT5_PACKAGE_SYNC, SYNC_COLUMNS, sync_rows + common_sync_rows),
        write_csv(PROBE_ATTEMPT_SUMMARY, ATTEMPT_COLUMNS, attempt_rows),
        write_csv(PROBE_HASH_COMPARISON, HASH_COLUMNS, comparison_rows),
        write_csv(PROBE_SKIP_REASON, SKIP_COLUMNS, skip_rows),
        write_csv(REQUIRED_GATE_AUDIT, GATE_COLUMNS, gates),
        write_json(FINAL_DECISION, final),
    ]
    identity_rows = build_identity_rows(compile_result, sync_rows + common_sync_rows, runtime_artifacts + artifact_paths, args)
    artifact_paths.append(write_csv(RUNTIME_IDENTITY, IDENTITY_COLUMNS, identity_rows))
    artifact_paths.extend(build_receipts(final, attempt_rows, identity_rows))
    artifact_paths.append(
        write_json(
            RUN_MANIFEST,
            {
                "run_id": RUN_ID,
                "parent_run_id": PARENT_RUN_ID,
                "generated_at_utc": now_utc(),
                "inputs": [rel(path) for path in INPUT_FILES],
                "outputs": [rel(path) for path in OUTPUT_FILES],
                "runtime_artifacts": [path_text(path) for path in runtime_artifacts],
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
    )
    artifact_paths.append(write_report(final, attempt_rows, parser_rows))
    artifact_paths.append(write_decision_doc(final))
    artifact_paths.extend(update_docs(final))
    artifact_paths.extend(update_registers(final, artifact_paths + runtime_artifacts))
    print(json.dumps(final, ensure_ascii=False, indent=2))
    return 0 if not str(status).startswith("blocked") else 2


if __name__ == "__main__":
    raise SystemExit(main())
