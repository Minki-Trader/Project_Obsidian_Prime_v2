from __future__ import annotations

import argparse
import csv
import json
import math
import re
import shutil
import subprocess
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists  # noqa: E402
from foundation.mt5 import runtime_support as mt5  # noqa: E402
from stage_pipelines.stage337 import train_guarded_model_scouts_without_db as bu  # noqa: E402


aw = bu.aw
bg = bu.bg

TODAY = "2026-05-28"
STAGE_ID = bu.STAGE_ID
RUN_NUMBER = "run337BV"
RUN_ID = "run337BV_execute_model_scout_mt5_runtime_probe_without_db_v1"
PARENT_RUN_ID = bu.RUN_ID
NEXT_RUN_ID = "run337BW_review_model_scout_runtime_probe_without_db_v1"
REPAIR_NEXT_RUN_ID = "run337BW_repair_model_scout_runtime_probe_handoff_without_db_v1"
CLAIM_BOUNDARY = (
    "research_development_only_stage337BV_model_scout_mt5_runtime_probe_without_db_"
    "no_model_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = bu.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MT5_DIR = RUN_DIR / "mt5"
SET_DIR = MT5_DIR / "sets"
INI_DIR = MT5_DIR / "inis"
MODEL_COPY_DIR = RUN_DIR / "models"
FEATURE_COPY_DIR = RUN_DIR / "feature_matrices"
TELEMETRY_COPY_DIR = RUN_DIR / "runtime_telemetry"
REPORT_COPY_DIR = MT5_DIR / "reports"
REVIEWS_DIR = bu.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337BV_model_scout_mt5_runtime_probe.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337BV_model_scout_mt5_runtime_probe.md"
SELECTED_STATUS = bu.SELECTED_STATUS
STAGE_BRIEF = bu.STAGE_BRIEF
WORKSPACE_STATE = bu.WORKSPACE_STATE
CURRENT_STATE = bu.CURRENT_STATE
CHANGELOG = bu.CHANGELOG
RUN_REGISTRY = bu.RUN_REGISTRY
ALPHA_LEDGER = bu.ALPHA_LEDGER
ARTIFACT_REGISTRY = bu.ARTIFACT_REGISTRY
STAGE_LEDGER = bu.STAGE_LEDGER

PARENT_FINAL = bu.FINAL_DECISION
PARENT_PACKAGE = bu.MT5_RUNTIME_PROBE_PACKAGE
PARENT_PROXY_EXPECTED = bu.PROXY_EXPECTED_FORWARD
PARENT_QUEUE = bu.RUN337BV_QUEUE
PARENT_ONNX_PARITY = bu.ONNX_PARITY

DEFAULT_PORTABLE_ROOT = Path("C:/Users/awdse/AppData/Local/ObsidianPrime/mt5_portable_run329E")
DEFAULT_TERMINAL = DEFAULT_PORTABLE_ROOT / "terminal64.exe"
DEFAULT_METAEDITOR = DEFAULT_PORTABLE_ROOT / "MetaEditor64.exe"
DEFAULT_COMMON_FILES = DEFAULT_PORTABLE_ROOT / "Common" / "Files"
DEFAULT_TESTER_PROFILE_ROOT = DEFAULT_PORTABLE_ROOT / "MQL5" / "Profiles" / "Tester"
DEFAULT_TERMINAL_DATA_ROOT = DEFAULT_PORTABLE_ROOT
PORTABLE_EA_EX5 = (
    DEFAULT_PORTABLE_ROOT
    / "MQL5"
    / "Experts"
    / "Project_Obsidian_Prime_v2"
    / "foundation"
    / "mt5"
    / "ObsidianPrimeV2_RuntimeProbeEA.ex5"
)

EA_SOURCE = ROOT / mt5.EA_SOURCE_PATH
EA_BINARY = ROOT / "foundation" / "mt5" / "ObsidianPrimeV2_RuntimeProbeEA.ex5"
EA_INCLUDE_DIR = ROOT / "foundation" / "mt5" / "include"

COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage337/{RUN_NUMBER}_model_scout_mt5_runtime_probe"
COMMON_MODEL_DIR = f"{COMMON_ROOT}/models"
COMMON_FEATURE_DIR = f"{COMMON_ROOT}/features"
COMMON_TELEMETRY_DIR = f"{COMMON_ROOT}/telemetry"

ATTEMPT_PACKAGE = RUN_DIR / "runtime_probe_attempt_package.csv"
COMMON_SYNC = RUN_DIR / "common_files_sync.csv"
EXECUTION_SUMMARY = RUN_DIR / "model_scout_mt5_runtime_probe_summary.csv"
PROXY_MT5_DIFF = RUN_DIR / "proxy_mt5_runtime_difference.csv"
TELEMETRY_SKIP_SUMMARY = RUN_DIR / "runtime_skip_reason_summary.csv"
RUNTIME_IDENTITY = RUN_DIR / "runtime_identity.csv"
TESTER_SETTINGS_IDENTITY = RUN_DIR / "tester_settings_identity.json"
TERMINAL_PROCESS_AUDIT = RUN_DIR / "terminal_process_audit.json"
MT5_EXECUTION_RESULT = RUN_DIR / "mt5_execution_result.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
FORENSICS_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
ARTIFACT_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    PARENT_FINAL,
    PARENT_PACKAGE,
    PARENT_PROXY_EXPECTED,
    PARENT_QUEUE,
    PARENT_ONNX_PARITY,
    EA_SOURCE,
)
OUTPUT_FILES = (
    ATTEMPT_PACKAGE,
    COMMON_SYNC,
    EXECUTION_SUMMARY,
    PROXY_MT5_DIFF,
    TELEMETRY_SKIP_SUMMARY,
    RUNTIME_IDENTITY,
    TESTER_SETTINGS_IDENTITY,
    TERMINAL_PROCESS_AUDIT,
    MT5_EXECUTION_RESULT,
    EXPERIMENT_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    RUNTIME_RECEIPT,
    FORENSICS_RECEIPT,
    ARTIFACT_RECEIPT,
    JUDGMENT_RECEIPT,
    REQUIRED_GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    SELECTED_STATUS,
    WORKSPACE_STATE,
    CURRENT_STATE,
    CHANGELOG,
    STAGE_BRIEF,
    Path(__file__),
)

ATTEMPT_COLUMNS = (
    "attempt_name",
    "probe_id",
    "model_id",
    "branch_id",
    "feature_set_id",
    "model_family",
    "feature_count",
    "feature_order_hash",
    "threshold_id",
    "short_threshold",
    "long_threshold",
    "min_margin",
    "feature_local_path",
    "model_local_path",
    "feature_common_path",
    "model_common_path",
    "telemetry_common_path",
    "summary_common_path",
    "set_path",
    "ini_path",
    "report_name",
    "from_date",
    "to_date",
    "claim_boundary",
)

SUMMARY_COLUMNS = (
    "attempt_name",
    "model_id",
    "feature_set_id",
    "tester_status",
    "runtime_status",
    "report_status",
    "returncode",
    "blocker",
    "expected_rows",
    "telemetry_cycle_rows",
    "ready_model_rows",
    "matched_rows",
    "expected_missing_rows",
    "hash_mismatch_rows",
    "probability_mismatch_rows",
    "decision_mismatch_rows",
    "max_abs_probability_diff",
    "first_ready_bar_time",
    "last_ready_bar_time",
    "latest_expected_bar_time",
    "feature_last_reached",
    "comparison_status",
    "feature_ready_count",
    "model_ok_count",
    "long_count",
    "short_count",
    "flat_count",
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
    "common_telemetry_path",
    "common_summary_path",
    "local_telemetry_path",
    "local_summary_path",
    "report_path",
    "claim_boundary",
)

DIFF_COLUMNS = (
    "attempt_name",
    "model_id",
    "bar_time",
    "source_time",
    "expected_found",
    "hash_match",
    "probability_match",
    "decision_match",
    "mt5_input_hash",
    "expected_input_hash",
    "mt5_p_short",
    "expected_p_short",
    "abs_diff_p_short",
    "mt5_p_flat",
    "expected_p_flat",
    "abs_diff_p_flat",
    "mt5_p_long",
    "expected_p_long",
    "abs_diff_p_long",
    "mt5_decision",
    "expected_decision",
    "comparison_status",
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

GATE_COLUMNS = bu.GATE_COLUMNS


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def safe_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_")[:80]


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return "" if not math.isfinite(value) else f"{value:.12g}"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    return str(value)


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column, "")) for column in columns})
    return path


def read_csv(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def write_md(path: Path, text: str) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")
    return path


def read_text_lossless(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    had_bom = raw.startswith(b"\xef\xbb\xbf")
    return raw.decode("utf-8-sig"), had_bom


def write_text_preserving(path: Path, text: str, had_bom: bool) -> Path:
    encoding = "utf-8-sig" if had_bom or path.suffix.lower() in {".md", ".txt"} else "utf-8"
    io_path(path).write_text(text, encoding=encoding)
    return path


def sha256(path: Path) -> str:
    return mt5.sha256_file(path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stage337BV model scout MT5 runtime probe.")
    parser.add_argument("--terminal-path", default=str(DEFAULT_TERMINAL))
    parser.add_argument("--metaeditor-path", default=str(DEFAULT_METAEDITOR))
    parser.add_argument("--common-files-root", default=str(DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-data-root", default=str(DEFAULT_TERMINAL_DATA_ROOT))
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--wait-timeout-seconds", type=int, default=240)
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--attempt-filter", default="", help="Comma-separated attempt names or model ids.")
    return parser.parse_args()


def copy_file(src: Path, dst: Path, sync_id: str, effect: str) -> dict[str, Any]:
    io_path(dst.parent).mkdir(parents=True, exist_ok=True)
    if not path_exists(src):
        return {
            "sync_id": sync_id,
            "source_path": rel(src),
            "target_path": dst.as_posix(),
            "exists": "false",
            "sha256": "",
            "status": "blocked_source_missing",
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    shutil.copy2(io_path(src), io_path(dst))
    return {
        "sync_id": sync_id,
        "source_path": rel(src),
        "target_path": dst.as_posix(),
        "exists": "true" if path_exists(dst) else "false",
        "sha256": sha256(dst) if path_exists(dst) else "",
        "status": "copied" if path_exists(dst) else "missing_after_copy",
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def copy_tree(src: Path, dst: Path, prefix: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path_exists(src):
        rows.append(
            {
                "sync_id": f"{prefix}::missing",
                "source_path": rel(src),
                "target_path": dst.as_posix(),
                "exists": "false",
                "sha256": "",
                "status": "blocked_source_tree_missing",
                "effect": "include module sync(포함 모듈 동기화)이 없으면 EA compile/run(컴파일/실행) 정체성이 약해진다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        return rows
    for source in sorted(io_path(src).rglob("*")):
        if not source.is_file():
            continue
        relative = source.relative_to(io_path(src))
        rows.append(
            copy_file(
                Path(str(source)),
                dst / relative,
                f"{prefix}::{relative.as_posix()}",
                "include module sync(포함 모듈 동기화)로 portable terminal(포터블 터미널)이 같은 코드를 보게 한다.",
            )
        )
    return rows


def compile_and_sync_ea(metaeditor_path: Path, terminal_data_root: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    compile_log = MT5_DIR / "runtime_probe_compile.log"
    compile_result = mt5.compile_mql5_ea(metaeditor_path, EA_SOURCE, compile_log)
    target_dir = terminal_data_root / "MQL5" / "Experts" / "Project_Obsidian_Prime_v2" / "foundation" / "mt5"
    rows = [
        copy_file(EA_SOURCE, target_dir / EA_SOURCE.name, "ea_source::RuntimeProbeEA", "EA source(전문가 자문 원천)를 terminal data root(터미널 데이터 루트)에 동기화한다."),
        copy_file(EA_BINARY, target_dir / EA_BINARY.name, "ea_binary::RuntimeProbeEA", "EA binary(전문가 자문 바이너리)를 terminal data root(터미널 데이터 루트)에 동기화한다."),
    ]
    rows.extend(copy_tree(EA_INCLUDE_DIR, target_dir / "include", "ea_include"))
    return compile_result, rows


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
    }


def remove_runtime_outputs(common_files_root: Path, attempt: Mapping[str, Any]) -> None:
    for key in ("common_telemetry_path", "common_summary_path"):
        value = str(attempt.get(key, "")).strip()
        if not value:
            continue
        path = common_files_root / Path(value)
        if path_exists(path):
            io_path(path).unlink()


def load_parent() -> tuple[dict[str, Any], list[dict[str, str]], pd.DataFrame]:
    parent = read_json(PARENT_FINAL)
    if parent.get("next_action") != RUN_ID:
        raise RuntimeError(f"parent next_action mismatch: {parent.get('next_action')} != {RUN_ID}")
    if parent.get("forward_passed") != "not_claimed" or parent.get("goal_achieve") != "not_claimed":
        raise RuntimeError("parent made a forbidden forward/goal claim")
    package_rows = read_csv(PARENT_PACKAGE)
    proxy = pd.read_csv(io_path(PARENT_PROXY_EXPECTED))
    return parent, package_rows, proxy


def attempt_filter(args: argparse.Namespace) -> set[str]:
    return {item.strip() for item in str(args.attempt_filter or "").split(",") if item.strip()}


def feature_to_date(paths: Sequence[Path]) -> str:
    latest: pd.Timestamp | None = None
    for path in paths:
        frame = pd.read_csv(io_path(path), usecols=lambda column: column in {"timestamp_utc", "bar_time_server"})
        if "timestamp_utc" in frame.columns:
            values = pd.to_datetime(frame["timestamp_utc"], utc=True, errors="coerce")
        elif "bar_time_server" in frame.columns:
            values = pd.to_datetime(frame["bar_time_server"], utc=True, errors="coerce")
        else:
            continue
        local_latest = values.max()
        if pd.notna(local_latest) and (latest is None or local_latest > latest):
            latest = local_latest
    if latest is None:
        return "2026.05.28"
    return (latest.date() + timedelta(days=1)).strftime("%Y.%m.%d")


def materialize_attempts(package_rows: Sequence[Mapping[str, str]], args: argparse.Namespace) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[Path]]:
    filters = attempt_filter(args)
    selected = []
    for row in package_rows:
        attempt_name = safe_name(str(row["model_id"]))
        if filters and attempt_name not in filters and str(row["model_id"]) not in filters:
            continue
        selected.append(dict(row, attempt_name=attempt_name))
    if not selected:
        raise RuntimeError("no run337BV probe attempts selected")

    feature_paths = [ROOT / str(row["feature_csv_path"]) for row in selected]
    to_date = feature_to_date(feature_paths)
    attempts: list[dict[str, Any]] = []
    sync_rows: list[dict[str, Any]] = []
    artifacts: list[Path] = []
    common_files_root = Path(args.common_files_root)

    for index, row in enumerate(selected):
        attempt_name = str(row["attempt_name"])
        model_id = str(row["model_id"])
        feature_set_id = str(row["feature_set_id"])
        feature_local_source = ROOT / str(row["feature_csv_path"])
        model_local_source = ROOT / str(row["onnx_path"])
        feature_copy = FEATURE_COPY_DIR / f"{feature_set_id}_asof_features.csv"
        model_copy = MODEL_COPY_DIR / f"{attempt_name}.onnx"
        sync_rows.append(copy_file(feature_local_source, feature_copy, f"local_feature::{attempt_name}", "feature CSV(피처 CSV)를 run folder(실행 폴더)에 복사한다."))
        sync_rows.append(copy_file(model_local_source, model_copy, f"local_model::{attempt_name}", "ONNX model(온엑스 모델)을 run folder(실행 폴더)에 복사한다."))
        artifacts.extend([feature_copy, model_copy])

        feature_common = f"{COMMON_FEATURE_DIR}/{feature_set_id}_asof_features.csv"
        model_common = f"{COMMON_MODEL_DIR}/{attempt_name}.onnx"
        telemetry_common = f"{COMMON_TELEMETRY_DIR}/{attempt_name}_telemetry.csv"
        summary_common = f"{COMMON_TELEMETRY_DIR}/{attempt_name}_summary.csv"
        sync_rows.append(copy_file(feature_copy, common_files_root / Path(feature_common), f"common_feature::{attempt_name}", "Common Files(공용 파일) feature handoff(피처 인계)를 만든다."))
        sync_rows.append(copy_file(model_copy, common_files_root / Path(model_common), f"common_model::{attempt_name}", "Common Files(공용 파일) model handoff(모델 인계)를 만든다."))

        set_name = f"ObsidianPrimeV2_RuntimeProbeEA_{attempt_name}.set"
        ini_name = f"ObsidianPrimeV2_RuntimeProbeEA_{attempt_name}.ini"
        report_name = f"Project_Obsidian_Prime_v2_{RUN_ID}_{attempt_name}"
        set_path = SET_DIR / set_name
        ini_path = INI_DIR / ini_name
        set_values = {
            "InpRunId": RUN_ID,
            "InpExplorationLabel": "stage337_ModelScout__MT5RuntimeProbe",
            "InpTierLabel": "Tier A",
            "InpPrimaryActiveTier": "tier_a",
            "InpSplitLabel": "forward_after_2026_04_14",
            "InpMainSymbol": "US100",
            "InpTimeframe": 5,
            "InpEnforceM5": True,
            "InpFeatureCsvPath": feature_common,
            "InpFeatureCount": int(float(row["feature_count"])),
            "InpFeatureCsvUseCommonFiles": True,
            "InpFeatureRequireTimestampMatch": True,
            "InpFeatureAllowLatestFallback": False,
            "InpFeatureStrictHeader": True,
            "InpFeatureCsvDelimiter": ",",
            "InpCsvTimestampIsBarClose": True,
            "InpModelPath": model_common,
            "InpModelId": model_id,
            "InpModelBackend": "onnx",
            "InpModelUseCommonFiles": True,
            "InpModelUseCpuOnly": True,
            "InpModelNoConversion": False,
            "InpSetOutputShape": True,
            "InpFeatureOrderHash": row["feature_order_hash"],
            "InpFallbackEnabled": False,
            "InpFallbackFeatureCsvPath": feature_common,
            "InpFallbackFeatureCount": int(float(row["feature_count"])),
            "InpFallbackModelPath": model_common,
            "InpFallbackModelId": model_id,
            "InpFallbackModelBackend": "onnx",
            "InpFallbackFeatureOrderHash": row["feature_order_hash"],
            "InpShortThreshold": float(row["short_threshold"]),
            "InpLongThreshold": float(row["long_threshold"]),
            "InpMinMargin": float(row["min_margin"]),
            "InpInvertSignal": False,
            "InpFallbackShortThreshold": float(row["short_threshold"]),
            "InpFallbackLongThreshold": float(row["long_threshold"]),
            "InpFallbackMinMargin": float(row["min_margin"]),
            "InpFallbackInvertSignal": False,
            "InpAllowTrading": True,
            "InpFixedLot": 0.10,
            "InpMagic": 3372200 + index,
            "InpDeviationPoints": 20,
            "InpCloseOnFlatSignal": False,
            "InpReverseOnOppositeSignal": True,
            "InpCloseOnlyOnOppositeSignal": False,
            "InpMaxHoldBars": 12,
            "InpMaxConcurrentPositions": 1,
            "InpReentryCooldownBars": 0,
            "InpSameDirectionReentryCooldownBars": 0,
            "InpEntryTransitionOnly": False,
            "InpAtrSltpEnabled": False,
            "InpModelRiskSizingEnabled": False,
            "InpTelemetryEnabled": True,
            "InpTelemetryUseCommonFiles": True,
            "InpTelemetryCsvPath": telemetry_common,
            "InpSummaryCsvPath": summary_common,
        }
        set_payload = mt5.materialize_tester_set_file(set_values, set_path, generated_by=rel(Path(__file__)))
        ini_payload = mt5.materialize_tester_ini_file(
            mt5.TesterMaterializationConfig(
                shutdown_terminal=1,
                from_date="2026.04.14",
                to_date=to_date,
                report=report_name,
            ),
            ini_path,
            set_file_path=Path(set_name),
        )
        artifacts.extend([set_path, ini_path])
        attempts.append(
            {
                **row,
                "attempt_name": attempt_name,
                "set": set_payload,
                "ini": ini_payload,
                "set_name": set_name,
                "ini_name": ini_name,
                "report_name": report_name,
                "feature_local_path": rel(feature_copy),
                "model_local_path": rel(model_copy),
                "feature_common_path": feature_common,
                "model_common_path": model_common,
                "common_telemetry_path": telemetry_common,
                "common_summary_path": summary_common,
                "from_date": "2026.04.14",
                "to_date": to_date,
                "tier": "Tier A",
                "split": "forward_after_2026_04_14",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return attempts, sync_rows, artifacts


def execute_attempts(
    attempts: Sequence[dict[str, Any]],
    args: argparse.Namespace,
    compile_payload: Mapping[str, Any],
) -> dict[str, Any]:
    common_files_root = Path(args.common_files_root)
    tester_profile_root = Path(args.tester_profile_root)
    terminal_data_root = Path(args.terminal_data_root)
    terminal_probe = terminal_processes()
    execution_results: list[dict[str, Any]] = []
    report_records: list[dict[str, Any]] = []
    if args.materialize_only:
        return {
            "compile": compile_payload,
            "terminal_process_probe": terminal_probe,
            "execution_results": [
                {
                    "attempt_name": attempt["attempt_name"],
                    "status": "not_run_materialize_only",
                    "runtime_outputs": {"status": "not_run_materialize_only", "wait_status": "not_run_materialize_only"},
                }
                for attempt in attempts
            ],
            "strategy_tester_reports": [],
            "portable_ea_ex5": PORTABLE_EA_EX5.as_posix(),
            "portable_ea_ex5_exists": path_exists(PORTABLE_EA_EX5),
            "portable_ea_ex5_sha256": sha256(PORTABLE_EA_EX5) if path_exists(PORTABLE_EA_EX5) else "",
        }

    can_run = compile_payload.get("status") == "completed" or path_exists(PORTABLE_EA_EX5)
    if not can_run:
        for attempt in attempts:
            execution_results.append(
                {
                    "attempt_name": attempt["attempt_name"],
                    "status": "blocked",
                    "blocker": "compile_blocked_and_no_portable_ex5_fallback",
                    "runtime_outputs": {"status": "blocked", "wait_status": "skipped_compile_blocked"},
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
                    ROOT / str(attempt["ini"]["path"]),
                    set_path=ROOT / str(attempt["set"]["path"]),
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
                    "runtime_outputs": runtime_outputs,
                    "attempt_name": attempt["attempt_name"],
                    "model_id": attempt["model_id"],
                    "feature_set_id": attempt["feature_set_id"],
                    "ini_path": attempt["ini"]["path"],
                    "set_path": attempt["set"]["path"],
                }
            )
        report_records = mt5.collect_mt5_strategy_report_artifacts(
            terminal_data_root=terminal_data_root,
            run_output_root=RUN_DIR,
            attempts=attempts,
            run_id=RUN_ID,
        )
        mt5.attach_mt5_report_metrics(execution_results, report_records)
    return {
        "compile": compile_payload,
        "terminal_process_probe": terminal_probe,
        "terminal_extra_args": ["/portable"],
        "execution_results": execution_results,
        "strategy_tester_reports": report_records,
        "portable_ea_ex5": PORTABLE_EA_EX5.as_posix(),
        "portable_ea_ex5_exists": path_exists(PORTABLE_EA_EX5),
        "portable_ea_ex5_sha256": sha256(PORTABLE_EA_EX5) if path_exists(PORTABLE_EA_EX5) else "",
    }


def copy_runtime_outputs(common_files_root: Path, attempts: Sequence[Mapping[str, Any]]) -> list[Path]:
    copied: list[Path] = []
    io_path(TELEMETRY_COPY_DIR).mkdir(parents=True, exist_ok=True)
    for attempt in attempts:
        for key, suffix in (("common_telemetry_path", "telemetry"), ("common_summary_path", "summary")):
            src = common_files_root / Path(str(attempt.get(key, "")))
            if not path_exists(src):
                continue
            dst = TELEMETRY_COPY_DIR / f"{attempt['attempt_name']}_{suffix}.csv"
            shutil.copy2(io_path(src), io_path(dst))
            copied.append(dst)
    return copied


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
        return float(value)
    except Exception:
        return math.nan


def expected_index(proxy: pd.DataFrame, model_id: str) -> dict[str, Mapping[str, Any]]:
    subset = proxy[proxy["model_id"].astype(str) == model_id].copy()
    return {norm_bar_time(row["bar_time"]): row.to_dict() for _, row in subset.iterrows()}


def expected_decision(value: Any) -> str:
    text = str(value or "").strip().lower()
    return "flat" if text in {"no_trade", "none", "-1"} else text


def compare_attempt(
    attempt: Mapping[str, Any],
    execution_row: Mapping[str, Any],
    report_row: Mapping[str, Any],
    proxy: pd.DataFrame,
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    model_id = str(attempt["model_id"])
    expected = expected_index(proxy, model_id)
    common_root = Path(str(execution_row.get("runtime_outputs", {}).get("telemetry_path", "")))
    local_telemetry = TELEMETRY_COPY_DIR / f"{attempt['attempt_name']}_telemetry.csv"
    local_summary = TELEMETRY_COPY_DIR / f"{attempt['attempt_name']}_summary.csv"
    telemetry_path = local_telemetry if path_exists(local_telemetry) else common_root
    diff_rows: list[dict[str, Any]] = []
    skip_rows: list[dict[str, Any]] = []
    if not path_exists(telemetry_path):
        return (
            {
                "attempt_name": attempt["attempt_name"],
                "model_id": model_id,
                "feature_set_id": attempt["feature_set_id"],
                "tester_status": execution_row.get("status", "not_attempted"),
                "runtime_status": execution_row.get("runtime_outputs", {}).get("status", "missing"),
                "report_status": report_row.get("status", "missing") if report_row else "missing",
                "returncode": execution_row.get("returncode", ""),
                "blocker": execution_row.get("blocker", "telemetry_missing"),
                "expected_rows": len(expected),
                "telemetry_cycle_rows": 0,
                "ready_model_rows": 0,
                "matched_rows": 0,
                "expected_missing_rows": 0,
                "hash_mismatch_rows": 0,
                "probability_mismatch_rows": 0,
                "decision_mismatch_rows": 0,
                "max_abs_probability_diff": "",
                "first_ready_bar_time": "",
                "last_ready_bar_time": "",
                "latest_expected_bar_time": max(expected) if expected else "",
                "feature_last_reached": "false",
                "comparison_status": "blocked_no_runtime_telemetry",
                "common_telemetry_path": attempt.get("common_telemetry_path", ""),
                "common_summary_path": attempt.get("common_summary_path", ""),
                "local_telemetry_path": "",
                "local_summary_path": "",
                "report_path": "",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            diff_rows,
            skip_rows,
        )

    frame = pd.read_csv(io_path(telemetry_path)).fillna("")
    cycles = frame[frame["record_type"].astype(str).str.lower() == "cycle"].copy()
    ready = cycles[
        (cycles["feature_ready"].astype(str).str.lower() == "true")
        & (cycles["model_ok"].astype(str).str.lower() == "true")
    ].copy()
    skipped = cycles[(cycles["feature_ready"].astype(str).str.lower() != "true") | (cycles["model_ok"].astype(str).str.lower() != "true")]
    for reason, count in skipped["skip_reason"].astype(str).replace("", "empty").value_counts().sort_index().items():
        skip_rows.append(
            {
                "attempt_name": attempt["attempt_name"],
                "model_id": model_id,
                "skip_reason": reason,
                "rows": int(count),
                "effect": "skip reason(스킵 사유)은 tester/date/model handoff(테스터/날짜/모델 인계) 공백을 보여준다.",
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
        exp_hash = str(exp.get("feature_input_hash", "")).upper() if exp else ""
        mt5_probs = [float_or_nan(row.get("p_short")), float_or_nan(row.get("p_flat")), float_or_nan(row.get("p_long"))]
        exp_probs = [float_or_nan(exp.get("p_short")), float_or_nan(exp.get("p_flat")), float_or_nan(exp.get("p_long"))] if exp else [math.nan, math.nan, math.nan]
        diffs = [abs(a - b) if math.isfinite(a) and math.isfinite(b) else math.inf for a, b in zip(mt5_probs, exp_probs)]
        row_max = max(diffs)
        max_prob_diff = max(max_prob_diff, row_max if math.isfinite(row_max) else 0.0)
        hash_ok = found and mt5_hash == exp_hash
        prob_ok = found and row_max <= tolerance
        mt5_decision = str(row.get("decision", "")).strip().lower()
        exp_decision = expected_decision(exp.get("decision_label", "")) if exp else ""
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
                "model_id": model_id,
                "bar_time": norm_bar_time(row.get("bar_time")),
                "source_time": bar_time,
                "expected_found": found,
                "hash_match": hash_ok,
                "probability_match": prob_ok,
                "decision_match": decision_ok,
                "mt5_input_hash": mt5_hash,
                "expected_input_hash": exp_hash,
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
                "comparison_status": status,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    latest_expected = max(expected) if expected else ""
    feature_last_reached = latest_expected in set(ready_times)
    if expected_missing or hash_mismatch or prob_mismatch or decision_mismatch:
        comparison_status = "blocked_proxy_mt5_mismatch"
    elif len(ready) <= 0:
        comparison_status = "blocked_no_ready_model_rows"
    elif feature_last_reached:
        comparison_status = "completed_exact_proxy_mt5_parity_reached_feature_last"
    else:
        comparison_status = "completed_overlap_proxy_mt5_parity_tester_gap_remains"
    runtime = execution_row.get("runtime_outputs", {}) if isinstance(execution_row.get("runtime_outputs"), Mapping) else {}
    last_summary = runtime.get("last_summary", {}) if isinstance(runtime.get("last_summary"), Mapping) else {}
    metrics = report_row.get("metrics", {}) if isinstance(report_row.get("metrics"), Mapping) else {}
    return (
        {
            "attempt_name": attempt["attempt_name"],
            "model_id": model_id,
            "feature_set_id": attempt["feature_set_id"],
            "tester_status": execution_row.get("status", "not_attempted"),
            "runtime_status": runtime.get("status", "not_attempted"),
            "report_status": report_row.get("status", "missing") if report_row else "missing",
            "returncode": execution_row.get("returncode", ""),
            "blocker": execution_row.get("blocker", ""),
            "expected_rows": len(expected),
            "telemetry_cycle_rows": int(len(cycles)),
            "ready_model_rows": int(len(ready)),
            "matched_rows": matched,
            "expected_missing_rows": expected_missing,
            "hash_mismatch_rows": hash_mismatch,
            "probability_mismatch_rows": prob_mismatch,
            "decision_mismatch_rows": decision_mismatch,
            "max_abs_probability_diff": max_prob_diff,
            "first_ready_bar_time": min(ready_times) if ready_times else "",
            "last_ready_bar_time": max(ready_times) if ready_times else "",
            "latest_expected_bar_time": latest_expected,
            "feature_last_reached": feature_last_reached,
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
            "trade_count": metrics.get("trade_count"),
            "expectancy": metrics.get("expectancy"),
            "recovery_factor": metrics.get("recovery_factor"),
            "max_drawdown_amount": metrics.get("max_drawdown_amount"),
            "short_trade_count": metrics.get("short_trade_count"),
            "long_trade_count": metrics.get("long_trade_count"),
            "common_telemetry_path": attempt.get("common_telemetry_path", ""),
            "common_summary_path": attempt.get("common_summary_path", ""),
            "local_telemetry_path": rel(local_telemetry) if path_exists(local_telemetry) else "",
            "local_summary_path": rel(local_summary) if path_exists(local_summary) else "",
            "report_path": report_row.get("html_report", {}).get("path", "") if isinstance(report_row.get("html_report"), Mapping) else "",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        diff_rows,
        skip_rows,
    )


def compare_all(attempts: Sequence[Mapping[str, Any]], execution: Mapping[str, Any], proxy: pd.DataFrame) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    results = {str(row.get("attempt_name", "")): row for row in execution.get("execution_results", [])}
    reports = {str(row.get("attempt_name", "")): row for row in execution.get("strategy_tester_reports", [])}
    summaries: list[dict[str, Any]] = []
    diffs: list[dict[str, Any]] = []
    skips: list[dict[str, Any]] = []
    for attempt in attempts:
        summary, diff_rows, skip_rows = compare_attempt(
            attempt,
            results.get(str(attempt["attempt_name"]), {}),
            reports.get(str(attempt["attempt_name"]), {}),
            proxy,
        )
        summaries.append(summary)
        diffs.extend(diff_rows)
        skips.extend(skip_rows)
    return summaries, diffs, skips


def classify(summary_rows: Sequence[Mapping[str, Any]], materialize_only: bool) -> tuple[str, str, str, str]:
    if materialize_only:
        return (
            "materialized_stage337BV_model_scout_mt5_runtime_probe_package_no_mt5_execution",
            "materialized_only_actual_mt5_not_executed",
            "stage337BV_keep_runtime_probe_execution_open",
            RUN_ID,
        )
    if not summary_rows:
        return (
            "blocked_stage337BV_no_probe_summary_rows",
            "no_runtime_probe_summary_created",
            "stage337BV_blocked_no_summary_rows",
            REPAIR_NEXT_RUN_ID,
        )
    blocked = [row for row in summary_rows if str(row.get("comparison_status", "")).startswith("blocked")]
    if blocked:
        return (
            "blocked_stage337BV_model_scout_mt5_runtime_probe_proxy_mismatch_or_no_output",
            "mt5_runtime_probe_missing_or_proxy_mt5_mismatch_requires_repair",
            "stage337BV_open_runtime_probe_handoff_repair",
            REPAIR_NEXT_RUN_ID,
        )
    all_reached = all(str(row.get("feature_last_reached", "")).lower() == "true" for row in summary_rows)
    if all_reached:
        return (
            "completed_stage337BV_model_scout_mt5_runtime_probe_exact_proxy_parity_no_forward_decision",
            "mt5_runtime_matches_proxy_expected_through_feature_last_no_forward_pass_fail_claim",
            "stage337BV_open_run337BW_runtime_probe_review_and_forward_diagnostic_attribution",
            NEXT_RUN_ID,
        )
    return (
        "completed_stage337BV_model_scout_mt5_runtime_probe_overlap_parity_tester_gap_remains_no_forward_decision",
        "mt5_runtime_matches_proxy_expected_on_overlap_but_tester_did_not_reach_feature_last",
        "stage337BV_open_run337BW_runtime_probe_gap_review",
        NEXT_RUN_ID,
    )


def build_gates(
    parent: Mapping[str, Any],
    attempts: Sequence[Mapping[str, Any]],
    sync_rows: Sequence[Mapping[str, Any]],
    execution: Mapping[str, Any],
    summary_rows: Sequence[Mapping[str, Any]],
    diff_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    def row(gate_id: str, passed: bool, observed: str, expected: str, effect: str) -> dict[str, Any]:
        return {
            "gate_id": gate_id,
            "status": "passed" if passed else "failed",
            "observed": observed,
            "expected": expected,
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }

    compile_ok = execution.get("compile", {}).get("status") == "completed" or execution.get("portable_ea_ex5_exists")
    sync_ok = all(str(item.get("status")) == "copied" for item in sync_rows if str(item.get("sync_id", "")).startswith(("common_", "local_", "ea_binary")))
    tester_attempted = any(str(item.get("status")) != "not_run_materialize_only" for item in execution.get("execution_results", []))
    mismatches = sum(
        1
        for item in diff_rows
        if item.get("comparison_status") not in {"matched"}
    )
    return [
        row("bv_gate_parent_bu_loaded", parent.get("next_action") == RUN_ID, str(parent.get("next_action")), RUN_ID, "BU 산출물에서 BV 실행을 열었는지 확인한다."),
        row("bv_gate_attempts_materialized", len(attempts) == 6, f"attempts={len(attempts)}", "6 attempts", "6개 scout model(스카우트 모델)을 모두 MT5 입력으로 만들었는지 확인한다."),
        row("bv_gate_common_files_synced", sync_ok, f"sync_rows={len(sync_rows)}", "Common Files synced", "MT5 terminal(터미널)이 읽을 feature/model(피처/모델)을 동기화한다."),
        row("bv_gate_compile_or_existing_ex5", bool(compile_ok), str(execution.get("compile", {}).get("status")), "compile completed or existing ex5", "EA compile(컴파일) 또는 기존 EX5(실행 파일) 정체성을 확보한다."),
        row("bv_gate_tester_attempted", tester_attempted, f"results={len(execution.get('execution_results', []))}", "tester attempted unless materialize-only", "실제 Strategy Tester(전략 테스터)를 시도했는지 확인한다."),
        row("bv_gate_runtime_outputs", all(str(item.get("runtime_status")) == "completed" for item in summary_rows), f"completed={sum(str(item.get('runtime_status')) == 'completed' for item in summary_rows)}/{len(summary_rows)}", "runtime outputs completed", "telemetry(런타임 기록)가 실제로 나왔는지 확인한다."),
        row("bv_gate_proxy_mt5_no_mismatch", mismatches == 0 and bool(diff_rows), f"mismatches={mismatches};diff_rows={len(diff_rows)}", "zero mismatches", "proxy expected(프록시 예상)와 MT5 runtime(런타임)이 같은지 확인한다."),
        row("bv_gate_no_forward_or_goal_claim", True, "forward_passed=not_claimed;goal=not_claimed", "no forbidden claim", "runtime probe(런타임 탐침)만 닫고 Forward/Goal(전진/목표)은 주장하지 않는다."),
    ]


def build_identity_rows(attempts: Sequence[Mapping[str, Any]], sync_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    paths = [
        ("ea_source", EA_SOURCE, "EA source(전문가 자문 원천)"),
        ("ea_binary", EA_BINARY, "EA binary(전문가 자문 바이너리)"),
        ("portable_ea", PORTABLE_EA_EX5, "portable terminal EA(포터블 터미널 전문가 자문)"),
        ("parent_package", PARENT_PACKAGE, "BU MT5 probe package(BU MT5 탐침 패키지)"),
        ("parent_proxy_expected", PARENT_PROXY_EXPECTED, "BU proxy expected(BU 프록시 예상)"),
    ]
    for artifact_id, path, role in paths:
        rows.append(
            {
                "artifact_id": artifact_id,
                "artifact_type": path.suffix.lstrip(".") or "file",
                "path": rel(path) if path.is_absolute() and str(path).startswith(str(ROOT)) else path.as_posix(),
                "exists": path_exists(path),
                "sha256": sha256(path) if path_exists(path) and io_path(path).is_file() else "",
                "role": role,
                "status": "present" if path_exists(path) else "missing",
                "effect": "runtime identity(런타임 정체성)을 고정해 결과 해석을 가능하게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    for attempt in attempts:
        for key, role in (("model_local_path", "local ONNX model(로컬 온엑스 모델)"), ("feature_local_path", "local feature CSV(로컬 피처 CSV)")):
            path = ROOT / str(attempt.get(key, ""))
            rows.append(
                {
                    "artifact_id": f"{attempt['attempt_name']}::{key}",
                    "artifact_type": path.suffix.lstrip(".") or "file",
                    "path": rel(path),
                    "exists": path_exists(path),
                    "sha256": sha256(path) if path_exists(path) and io_path(path).is_file() else "",
                    "role": role,
                    "status": "present" if path_exists(path) else "missing",
                    "effect": "attempt(시도)별 입력 정체성을 기록한다.",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    for item in sync_rows:
        rows.append(
            {
                "artifact_id": str(item.get("sync_id", "")),
                "artifact_type": "sync",
                "path": str(item.get("target_path", "")),
                "exists": item.get("exists", ""),
                "sha256": item.get("sha256", ""),
                "role": "handoff sync(인계 동기화)",
                "status": item.get("status", ""),
                "effect": item.get("effect", ""),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def write_report(final: Mapping[str, Any], summary_rows: Sequence[Mapping[str, Any]]) -> Path:
    lines = [
        "# Stage337 run337BV Model Scout MT5 Runtime Probe(모델 스카우트 MT5 런타임 탐침)",
        "",
        "## Conclusion(결론)",
        "",
        f"run337BV(337BV 실행)는 run337BU(337BU 실행)의 proxy expected(프록시 예상)와 MT5 runtime telemetry(MT5 런타임 기록)를 비교했다.",
        "",
        f"Effect(효과): status(상태)는 `{final['status']}`이고, Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 모두 주장하지 않는다.",
        "",
        "## Result(결과)",
        "",
        f"- status(상태): `{final['status']}`",
        f"- judgment(판정): `{final['judgment']}`",
        f"- decision(결정): `{final['decision']}`",
        f"- next_action(다음 행동): `{final['next_action']}`",
        f"- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`",
        f"- attempts(시도): `{final['attempt_rows']}`",
        f"- matched_rows(일치 행): `{final['matched_rows']}`",
        f"- mismatch_rows(불일치 행): `{final['mismatch_rows']}`",
        "",
        "## Runtime Summary(런타임 요약)",
        "",
        "| model(모델) | feature_set(피처 세트) | status(상태) | ready(준비) | matched(일치) | max diff(최대 차이) | feature last(피처 끝) | trades(거래) | net(순익) |",
        "|---|---|---|---:|---:|---:|---|---:|---:|",
    ]
    for row in summary_rows:
        lines.append(
            "| `{model}` | `{feature}` | `{status}` | {ready} | {matched} | {diff} | `{last}` | {trades} | {net} |".format(
                model=row.get("model_id", ""),
                feature=row.get("feature_set_id", ""),
                status=row.get("comparison_status", ""),
                ready=row.get("ready_model_rows", ""),
                matched=row.get("matched_rows", ""),
                diff=row.get("max_abs_probability_diff", ""),
                last=row.get("feature_last_reached", ""),
                trades=row.get("trade_count", ""),
                net=row.get("net_profit", ""),
            )
        )
    lines.extend(
        [
            "",
            "## Boundary(경계)",
            "",
            "- forward_selection(전진 선택): `not_run`",
            "- threshold_tuning(임계값 조정): `not_run`",
            "- candidate_selection(후보 선택): `not_run`",
            "- Forward Passed/Failed(전진 통과/실패): `not_claimed`",
            "- runtime_authority(런타임 권위): `not_claimed`",
            "- Goal Achieve(목표 달성): `not_claimed`",
            "",
            f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        ]
    )
    return write_md(REPORT_PATH, "\n".join(lines))


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    return write_md(
        DECISION_DOC,
        f"""# Decision: Stage337 run337BV Model Scout MT5 Runtime Probe(결정: 모델 스카우트 MT5 런타임 탐침)

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(상위 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

Effect(효과): MT5 runtime telemetry(MT5 런타임 기록)를 proxy expected(프록시 예상)와 비교했지만, 이것은 runtime probe(런타임 탐침) 근거다. Forward Passed/Failed(전진 통과/실패), operating promotion(운영 승격), runtime authority(런타임 권위)는 주장하지 않는다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )


def build_receipts(final: Mapping[str, Any], summary_rows: Sequence[Mapping[str, Any]]) -> list[Path]:
    completed = sum(1 for row in summary_rows if str(row.get("runtime_status")) == "completed")
    payloads = [
        (
            EXPERIMENT_RECEIPT,
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "hypothesis": "BU scout ONNX outputs should match MT5 RuntimeProbeEA telemetry under fixed feature order and fixed threshold.",
                "controls": "no model training, no threshold tuning, no lot optimization, fixed Common Files handoff",
                "stop_condition": "any hash/probability/decision mismatch blocks runtime parity claim",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            DATA_RECEIPT,
            {
                "data_source": "run337BQ feature CSVs and run337BO refreshed US100 forward window",
                "time_axis": "bar_time/source_time exact M5 close timestamp",
                "rows_compared": final["diff_rows"],
                "missing_or_duplicate_check": "expected_missing_rows and telemetry ready rows in summary",
                "integrity_judgment": "usable_with_boundary" if completed else "blocked_or_inconclusive",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            MODEL_RECEIPT,
            {
                "model_subject": "run337BU guarded scout ONNX models",
                "model_rows": final["attempt_rows"],
                "threshold_policy": "fixed_short040_long040_margin002 only",
                "selection_metric": "none",
                "validation_judgment": "runtime_probe_input_only",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            RUNTIME_RECEIPT,
            {
                "research_path": rel(bu.PROXY_EXPECTED_FORWARD),
                "runtime_path": rel(REPORT_PATH),
                "shared_contract": "feature order hash, feature_input_hash, p_short/p_flat/p_long, decision label, bar_time",
                "known_differences": "MT5 telemetry uses flat where Python proxy labels no_trade",
                "parity_check": rel(PROXY_MT5_DIFF),
                "parity_identity": rel(RUNTIME_IDENTITY),
                "runtime_claim_boundary": "runtime_probe_only_no_runtime_authority",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            FORENSICS_RECEIPT,
            {
                "tester_identity": "portable MT5 Strategy Tester(전략 테스터); US100; M5; model 4(real ticks, 실제 틱); deposit 500; leverage 1:100",
                "ea_identity": rel(EA_SOURCE),
                "report_identity": rel(REPORT_COPY_DIR),
                "trade_evidence": "strategy reports collected when MT5 produced report artifacts",
                "cost_assumptions": "broker tester native spread/slippage; no extra modeled commission",
                "forensic_checks": ["tester returncode", "runtime summary", "strategy report artifact", "proxy/MT5 row diff"],
                "backtest_judgment": final["judgment"],
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            ARTIFACT_RECEIPT,
            {
                "source_inputs": [rel(path) for path in INPUT_FILES],
                "producer": rel(Path(__file__)),
                "artifact_paths": [rel(path) for path in OUTPUT_FILES if path_exists(path)],
                "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
                "availability": "run artifacts local/ignored, reports and registers tracked",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            JUDGMENT_RECEIPT,
            {
                "result_subject": RUN_ID,
                "evidence_available": [rel(REPORT_PATH), rel(EXECUTION_SUMMARY), rel(PROXY_MT5_DIFF)],
                "evidence_missing": "full forward attribution and operating review remain out of scope",
                "judgment_label": final["judgment"],
                "next_condition": final["next_action"],
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
    ]
    return [write_json(path, payload) for path, payload in payloads]


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace = bg.replace_top_value(workspace_text, "current_run_id: ", final["next_action"])
    workspace = bg.replace_top_value(workspace, "updated_on: ", f"'{TODAY}'")
    focus_entry = (
        "- >-\n"
        f"  Stage337 run337BV focus complete: model scout MT5 runtime probe(모델 스카우트 MT5 런타임 탐침)를 `{final['status']}`로 닫았다. "
        "Effect(효과): proxy expected(프록시 예상)와 MT5 telemetry(MT5 기록)를 비교했고, 결과 리뷰를 run337BW(337BW 실행)로 넘긴다.\n"
    )
    if "Stage337 run337BV focus complete" not in workspace:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus_entry, 1)
    artifacts.append(write_text_preserving(WORKSPACE_STATE, workspace, workspace_bom))

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    current = current_text
    replacements = {
        "- current_run(현재 실행): ": f"`{final['next_action']}`",
        "- status(상태): ": f"`{final['status']}`",
        "- decision(결정): ": f"`{final['decision']}`",
        "- latest_completed_run(최근 완료 실행): ": f"`{RUN_ID}`",
        "- next_action(다음 행동): ": f"`{final['next_action']}`",
        "- claim_boundary(주장 경계): ": f"`{CLAIM_BOUNDARY}`",
    }
    for prefix, value in replacements.items():
        current = bg.replace_top_value(current, prefix, value)
    entry = f"""
## Stage337 run337BV(337BV 실행) - {TODAY}

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): MT5 runtime telemetry(MT5 런타임 기록)와 proxy expected(프록시 예상)를 비교했다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    if "## Stage337 run337BV(337BV 실행)" not in current:
        marker = "## Stage337 run337BU(337BU"
        current = current.replace(marker, entry + "\n" + marker, 1) if marker in current else current.rstrip() + "\n\n" + entry
    artifacts.append(write_text_preserving(CURRENT_STATE, current, current_bom))

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
- effect(효과): 다음은 runtime probe review(런타임 탐침 리뷰)와 forward diagnostic attribution(전진 진단 귀속)이다.
"""
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection_text, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_entry = f"- {TODAY}: run337BV(337BV 실행) executed model scout MT5 runtime probe(모델 스카우트 MT5 런타임 탐침). Status(상태) `{final['status']}`. Forward/Goal(전진/목표)은 주장하지 않음."
    if stage_entry not in stage_text:
        stage_text = stage_text.rstrip() + "\n" + stage_entry + "\n"
    artifacts.append(write_text_preserving(STAGE_BRIEF, stage_text, stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_entry = f"- {TODAY}: Stage337 run337BV executed model scout MT5 runtime probe(모델 스카우트 MT5 런타임 탐침) and opened `{final['next_action']}`."
    if changelog_entry not in changelog_text:
        changelog_text = changelog_text.rstrip() + "\n" + changelog_entry + "\n"
    artifacts.append(write_text_preserving(CHANGELOG, changelog_text, changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any], artifact_paths: Sequence[Path]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "model_scout_mt5_runtime_probe_without_db",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"decision={final['decision']};next_action={final['next_action']};attempts={final['attempt_rows']};goal_achieve_not_claimed.",
        "family": "runtime_parity_backtest_forensics",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__model_scout_mt5_runtime_probe",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "model_scout_mt5_runtime_probe",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "proxy_mt5_runtime_comparison",
        "tier_scope": "Tier A runtime probe; no operating claim",
        "kpi_scope": "runtime_parity_and_strategy_tester_diagnostic",
        "scoreboard_lane": "model_scout_runtime_probe",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"matched_rows={final['matched_rows']}",
        "guardrail_kpi": f"mismatch_rows={final['mismatch_rows']};forward_goal_not_claimed",
        "external_verification_status": final["actual_mt5_execution"],
        "notes": f"decision={final['decision']};next={final['next_action']}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__model_scout_mt5_runtime_probe",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "runtime_parity_backtest_forensics",
        "evidence_scope": "MT5 telemetry, strategy tester report, proxy-vs-MT5 diff",
        "kpi_scope": "runtime_probe_no_forward_decision",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"attempts={final['attempt_rows']};mismatch_rows={final['mismatch_rows']}",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__model_scout_mt5_runtime_probe",
        "family": "runtime_parity_backtest_forensics",
        "question": "do BU scout ONNX outputs match MT5 RuntimeProbeEA telemetry on the forward feature window",
        "metric_scope": "runtime_parity_and_tester_diagnostic",
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
        if not path_exists(path) or not io_path(path).is_file():
            continue
        artifact_path = rel(path)
        new_rows.append(
            {
                "artifact_id": f"{RUN_ID}::{artifact_path}",
                "artifact_type": path.suffix.lstrip(".") or "file",
                "path": artifact_path,
                "sha256": sha256(path),
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


def main() -> int:
    args = parse_args()
    for directory in (RUN_DIR, MT5_DIR, SET_DIR, INI_DIR, MODEL_COPY_DIR, FEATURE_COPY_DIR, TELEMETRY_COPY_DIR, REPORT_COPY_DIR):
        io_path(directory).mkdir(parents=True, exist_ok=True)

    parent, package_rows, proxy = load_parent()
    pre_process = terminal_processes()
    compile_result, ea_sync = compile_and_sync_ea(Path(args.metaeditor_path), Path(args.terminal_data_root))
    attempts, sync_rows, attempt_artifacts = materialize_attempts(package_rows, args)
    sync_rows = list(ea_sync) + sync_rows
    execution = execute_attempts(attempts, args, compile_result)
    copied_runtime = copy_runtime_outputs(Path(args.common_files_root), attempts)
    summary_rows, diff_rows, skip_rows = compare_all(attempts, execution, proxy)
    status, judgment, decision, next_action = classify(summary_rows, bool(args.materialize_only))
    gates = build_gates(parent, attempts, sync_rows, execution, summary_rows, diff_rows)
    passed_gates = sum(1 for row in gates if row["status"] == "passed")
    mismatch_rows = sum(1 for row in diff_rows if row.get("comparison_status") != "matched")
    actual_mt5_execution = "attempted_strategy_tester" if any(row.get("tester_status") not in {"not_run_materialize_only", ""} for row in summary_rows) else "not_run_materialize_only"
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": status,
        "judgment": judgment,
        "decision": decision,
        "next_action": next_action,
        "attempt_rows": len(attempts),
        "summary_rows": len(summary_rows),
        "diff_rows": len(diff_rows),
        "matched_rows": sum(int(row.get("matched_rows") or 0) for row in summary_rows),
        "mismatch_rows": mismatch_rows,
        "runtime_completed_rows": sum(1 for row in summary_rows if str(row.get("runtime_status")) == "completed"),
        "feature_last_reached_rows": sum(1 for row in summary_rows if str(row.get("feature_last_reached")).lower() == "true"),
        "actual_mt5_execution": actual_mt5_execution,
        "forward_selection": "not_run",
        "threshold_tuning": "not_run",
        "candidate_selection": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        "gate_rows": len(gates),
        "passed_gates": passed_gates,
        "failed_gates": [row["gate_id"] for row in gates if row["status"] != "passed"],
    }

    attempt_rows = [
        {column: attempt.get(column, "") for column in ATTEMPT_COLUMNS}
        for attempt in attempts
    ]
    artifacts: list[Path] = []
    artifacts.extend(
        [
            write_csv(ATTEMPT_PACKAGE, ATTEMPT_COLUMNS, attempt_rows),
            write_csv(COMMON_SYNC, SYNC_COLUMNS, sync_rows),
            write_csv(EXECUTION_SUMMARY, SUMMARY_COLUMNS, summary_rows),
            write_csv(PROXY_MT5_DIFF, DIFF_COLUMNS, diff_rows),
            write_csv(TELEMETRY_SKIP_SUMMARY, ["attempt_name", "model_id", "skip_reason", "rows", "effect", "claim_boundary"], skip_rows),
            write_csv(RUNTIME_IDENTITY, IDENTITY_COLUMNS, build_identity_rows(attempts, sync_rows)),
            write_json(TESTER_SETTINGS_IDENTITY, {
                "terminal_path": str(args.terminal_path),
                "terminal_data_root": str(args.terminal_data_root),
                "common_files_root": str(args.common_files_root),
                "tester_profile_root": str(args.tester_profile_root),
                "model": 4,
                "deposit": 500,
                "leverage": "1:100",
                "from_date": "2026.04.14",
                "to_date": attempts[0].get("to_date", "") if attempts else "",
                "claim_boundary": CLAIM_BOUNDARY,
            }),
            write_json(TERMINAL_PROCESS_AUDIT, {"pre_run": pre_process, "post_run": terminal_processes(), "claim_boundary": CLAIM_BOUNDARY}),
            write_json(MT5_EXECUTION_RESULT, execution),
            write_csv(REQUIRED_GATE_AUDIT, GATE_COLUMNS, gates),
            write_json(FINAL_DECISION, final),
            write_json(RUN_MANIFEST, {
                "run_id": RUN_ID,
                "parent_run_id": PARENT_RUN_ID,
                "inputs": [rel(path) for path in INPUT_FILES],
                "outputs": [rel(path) for path in OUTPUT_FILES],
                "claim_boundary": CLAIM_BOUNDARY,
            }),
        ]
    )
    artifacts.extend(attempt_artifacts)
    artifacts.extend(copied_runtime)
    artifacts.extend(build_receipts(final, summary_rows))
    artifacts.append(write_report(final, summary_rows))
    artifacts.append(write_decision_doc(final))
    artifacts.extend(update_docs(final))
    artifacts.extend(update_registers(final, artifacts))

    print(json.dumps(final, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not final["failed_gates"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
