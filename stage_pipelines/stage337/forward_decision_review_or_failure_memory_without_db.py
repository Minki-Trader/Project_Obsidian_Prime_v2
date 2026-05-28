from __future__ import annotations

import argparse
import csv
import json
import math
import shutil
import subprocess
import sys
import time
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists  # noqa: E402
from foundation.mt5 import mql5_compile, runtime_support as mt5  # noqa: E402
from foundation.mt5.runtime_artifacts import sha256_file  # noqa: E402
from stage_pipelines.stage337 import execute_model_scout_mt5_runtime_probe_without_db as bv  # noqa: E402
from stage_pipelines.stage337 import forward_kpi_attribution_cost_stress_curve_pocket as eq  # noqa: E402
from stage_pipelines.stage337 import materialize_common_files_and_run_argmax_parity_probe as el  # noqa: E402
from stage_pipelines.stage337 import refresh_survivor_feature_handoff_and_surface_reprobe as eo  # noqa: E402
from stage_pipelines.stage337 import review_runtime_data_and_feature_source_repair_probe as qprobe  # noqa: E402
from stage_pipelines.stage337 import top3_weight_contract_refresh_and_runtime_probe as ep  # noqa: E402


RUN_NUMBER = "run337ER"
RUN_ID = "run337ER_forward_decision_review_or_failure_memory_without_db_v1"
PARENT_RUN_ID = eq.RUN_ID
NEXT_RUN_ID = "run337ES_no_overfit_repair_or_broker_rollover_reprobe_without_db_v1"
STAGE_ID = ep.STAGE_ID
STAGE_DIR = ep.STAGE_DIR
PARENT_RUN_DIR = STAGE_DIR / "02_runs" / "run337EQ"
PARENT_FINAL_DECISION = PARENT_RUN_DIR / "final_forward_decision_report.json"
PARENT_MT5_REPORT_SUMMARY = PARENT_RUN_DIR / "frozen_forward_mt5_report.csv"
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MT5_DIR = RUN_DIR / "mt5"
SET_DIR = MT5_DIR / "sets"
INI_DIR = MT5_DIR / "inis"
REPORT_DIR = MT5_DIR / "reports"
FEATURE_DIR = RUN_DIR / "feature_matrices"
MODEL_DIR = RUN_DIR / "models"
EXPECTED_DIR = RUN_DIR / "expected_probability_tapes"
TELEMETRY_DIR = RUN_DIR / "runtime_telemetry"
SEED_DIR = RUN_DIR / "shifted_custom_seed"

ATTEMPT_PACKAGE = RUN_DIR / "shifted_custom_attempt_package.csv"
COMMON_SYNC = RUN_DIR / "common_files_sync.csv"
EXPECTED_INDEX = RUN_DIR / "expected_probability_tape_index.csv"
MT5_EXECUTION_RESULT = RUN_DIR / "shifted_custom_mt5_execution_result.json"
MT5_REPORT_SUMMARY = RUN_DIR / "shifted_custom_mt5_report.csv"
TRADE_RECORDS = RUN_DIR / "shifted_custom_trade_records.csv"
PARSER_CHECKS = RUN_DIR / "shifted_custom_trade_report_parser_checks.csv"
PARSER_ERRORS = RUN_DIR / "shifted_custom_trade_report_parser_errors.csv"
REGIME_ATTRIBUTION = RUN_DIR / "shifted_custom_regime_attribution_report.csv"
DB_ATTRIBUTION = RUN_DIR / "shifted_custom_db_attribution_report.csv"
LOT_NORMALIZED = RUN_DIR / "shifted_custom_lot_normalized_report.csv"
COST_STRESS = RUN_DIR / "shifted_custom_cost_stress_report.csv"
CURVE_POCKET = RUN_DIR / "shifted_custom_curve_pocket_report.csv"
SIGNAL_ATTRIBUTION = RUN_DIR / "shifted_custom_signal_attribution_report.csv"
GATE_AUDIT = RUN_DIR / "shifted_custom_required_gate_coverage_audit.csv"
BROKER_GAP_REFERENCE = RUN_DIR / "broker_gap_reference.csv"
FAILURE_MEMORY = RUN_DIR / "failure_memory_matrix.csv"
FEATURE_SHIFT_AUDIT = RUN_DIR / "shifted_feature_contract.csv"
SEED_STATUS = RUN_DIR / "shifted_custom_symbol_seed_status.json"
FINAL_DECISION = RUN_DIR / "final_forward_decision_report.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
REPORT_PATH = STAGE_DIR / "03_reviews" / "run337ER_shifted_custom_failure_memory.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337ER_shifted_custom_failure_memory.md"

ORIGIN_SYMBOL = "US100"
SHIFTED_CUSTOM_SYMBOL = "US100.OPV337ERD"
CUSTOM_SYMBOL_PATH = "ObsidianPrime"
SHIFT_MINUTES = -1440
COMMON_ROOT = "Project_Obsidian_Prime_v2/s337ER"
SCRIPT_SOURCE = ROOT / "foundation" / "mt5" / "ObsidianPrimeV2_CustomSymbolSeed.mq5"
SCRIPT_RELATIVE = Path("Project_Obsidian_Prime_v2") / "foundation" / "mt5" / "ObsidianPrimeV2_CustomSymbolSeed.mq5"
SCRIPT_PRESET_NAME = "opv2_run337ER_shifted_custom_symbol_seed.set"
SCRIPT_STARTUP_INI_NAME = "opv2_run337ER_shifted_custom_symbol_seed_startup.ini"
FROM_UTC = "2026.04.14 00:00:00"
TO_UTC = "2026.05.29 00:00:00"
SHIFTED_FROM_DATE = "2026.04.13"
SHIFTED_TO_DATE = "2026.05.28"
DEPOSIT = eq.DEPOSIT
STRESS_POINTS = eq.STRESS_POINTS
ROLLING_WINDOWS = eq.ROLLING_WINDOWS

CLAIM_BOUNDARY = (
    "research_development_only_stage337ER_shifted_custom_failure_memory_without_db_"
    "synthetic_timestamp_shift_diagnostic_only_no_new_training_no_threshold_tuning_no_lot_optimization_"
    "no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)
STATUS_COMPLETED = "completed_stage337ER_shifted_custom_failure_memory_no_forward_decision"
STATUS_BLOCKED = "blocked_stage337ER_shifted_custom_seed_or_runtime_gap_no_forward_decision"
JUDGMENT_COMPLETED = "synthetic_shifted_custom_reaches_latest_feature_window_and_strengthens_failure_memory_but_broker_forward_remains_blocked"
JUDGMENT_BLOCKED = "synthetic_shifted_custom_diagnostic_could_not_reach_latest_feature_window_or_parse_runtime_outputs"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stage337ER shifted custom diagnostic and failure memory review.")
    parser.add_argument("--terminal-path", default=str(bv.DEFAULT_TERMINAL))
    parser.add_argument("--metaeditor-path", default=str(bv.DEFAULT_METAEDITOR))
    parser.add_argument("--terminal-data-root", default=str(bv.DEFAULT_TERMINAL_DATA_ROOT))
    parser.add_argument("--common-files-root", default=str(bv.DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(bv.DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--from-date", default="2026.04.14")
    parser.add_argument("--to-date", default="2026.05.29")
    parser.add_argument("--shifted-from-date", default=SHIFTED_FROM_DATE)
    parser.add_argument("--shifted-to-date", default=SHIFTED_TO_DATE)
    parser.add_argument("--attempt-limit", type=int, default=7)
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--wait-timeout-seconds", type=int, default=120)
    parser.add_argument("--seed-timeout-seconds", type=int, default=240)
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--seed-only", action="store_true")
    return parser.parse_args()


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return item.as_posix()


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return "" if not math.isfinite(value) else f"{value:.12g}"
    if isinstance(value, (Mapping, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    return str(value)


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], columns: Sequence[str] | None = None) -> Path:
    rows = list(rows)
    fields = list(columns or (rows[0].keys() if rows else ["empty"]))
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: csv_value(row.get(field, "")) for field in fields})
    return path


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> Any:
    with io_path(path).open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def write_bom_text(path: Path, text: str) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8-sig")
    return path


def number(value: Any, default: float = 0.0) -> float:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return default
    return parsed if math.isfinite(parsed) else default


def safe_name(value: str, limit: int = 96) -> str:
    cleaned = "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in value)
    return cleaned[:limit].strip("_") or "attempt"


def short_attempt_id(base: Mapping[str, Any]) -> str:
    rank = int(number(base.get("proxy_rank")))
    model_code = str(base.get("model_id", "model")).split("__", 1)[0]
    return f"r{rank:02d}_{safe_name(model_code, 16)}"


def configure_eq_globals() -> None:
    eq.RUN_NUMBER = RUN_NUMBER
    eq.RUN_ID = RUN_ID
    eq.PARENT_RUN_ID = PARENT_RUN_ID
    eq.NEXT_RUN_ID = NEXT_RUN_ID
    eq.STAGE_ID = STAGE_ID
    eq.STAGE_DIR = STAGE_DIR
    eq.RUN_DIR = RUN_DIR
    eq.MT5_DIR = MT5_DIR
    eq.SET_DIR = SET_DIR
    eq.INI_DIR = INI_DIR
    eq.REPORT_DIR = REPORT_DIR
    eq.FEATURE_DIR = FEATURE_DIR
    eq.MODEL_DIR = MODEL_DIR
    eq.EXPECTED_DIR = EXPECTED_DIR
    eq.TELEMETRY_DIR = TELEMETRY_DIR
    eq.ATTEMPT_PACKAGE = ATTEMPT_PACKAGE
    eq.COMMON_SYNC = COMMON_SYNC
    eq.EXPECTED_INDEX = EXPECTED_INDEX
    eq.MT5_EXECUTION_RESULT = MT5_EXECUTION_RESULT
    eq.MT5_REPORT_SUMMARY = MT5_REPORT_SUMMARY
    eq.TRADE_RECORDS = TRADE_RECORDS
    eq.PARSER_CHECKS = PARSER_CHECKS
    eq.PARSER_ERRORS = PARSER_ERRORS
    eq.REGIME_ATTRIBUTION = REGIME_ATTRIBUTION
    eq.DB_ATTRIBUTION = DB_ATTRIBUTION
    eq.LOT_NORMALIZED = LOT_NORMALIZED
    eq.COST_STRESS = COST_STRESS
    eq.CURVE_POCKET = CURVE_POCKET
    eq.SIGNAL_ATTRIBUTION = SIGNAL_ATTRIBUTION
    eq.GATE_AUDIT = GATE_AUDIT
    eq.FINAL_DECISION = FINAL_DECISION
    eq.RUN_MANIFEST = RUN_MANIFEST
    eq.CLAIM_BOUNDARY = CLAIM_BOUNDARY
    eq.STATUS_COMPLETED = STATUS_COMPLETED
    eq.STATUS_BLOCKED = STATUS_BLOCKED
    eq.STRESS_POINTS = STRESS_POINTS
    eq.ROLLING_WINDOWS = ROLLING_WINDOWS


def portable_root(args: argparse.Namespace) -> Path:
    terminal = Path(args.terminal_path)
    return terminal.parent


def shifted_seed_paths(args: argparse.Namespace) -> dict[str, Path]:
    root = portable_root(args)
    return {
        "portable_script": root / "MQL5" / "Scripts" / SCRIPT_RELATIVE,
        "preset": root / "MQL5" / "Presets" / SCRIPT_PRESET_NAME,
        "startup_ini": root / "MQL5" / "Profiles" / "Tester" / SCRIPT_STARTUP_INI_NAME,
        "startup_ini_repo_copy": SEED_DIR / "shifted_custom_symbol_seed_startup.ini",
        "common_output": Path(args.common_files_root) / COMMON_ROOT / "shifted_custom_symbol_seed_status.json",
        "compile_log": MT5_DIR / "shifted_custom_symbol_seed_compile.log",
    }


def prepare_shifted_seed(args: argparse.Namespace) -> dict[str, Any]:
    paths = shifted_seed_paths(args)
    io_path(paths["portable_script"].parent).mkdir(parents=True, exist_ok=True)
    shutil.copy2(io_path(SCRIPT_SOURCE), io_path(paths["portable_script"]))
    io_path(paths["preset"].parent).mkdir(parents=True, exist_ok=True)
    preset_text = "\n".join(
        [
            f"InpRunId={RUN_ID}",
            f"InpOriginSymbol={ORIGIN_SYMBOL}",
            f"InpCustomSymbol={SHIFTED_CUSTOM_SYMBOL}",
            f"InpCustomPath={CUSTOM_SYMBOL_PATH}",
            f"InpFromUtc={FROM_UTC}",
            f"InpToUtc={TO_UTC}",
            f"InpOutputPath={COMMON_ROOT}/shifted_custom_symbol_seed_status.json",
            "InpOutputUseCommonFiles=true",
            f"InpShiftMinutes={SHIFT_MINUTES}",
            "",
        ]
    )
    io_path(paths["preset"]).write_text(preset_text, encoding="utf-8")
    startup_text = "\n".join(
        [
            "[StartUp]",
            r"Script=Project_Obsidian_Prime_v2\foundation\mt5\ObsidianPrimeV2_CustomSymbolSeed",
            f"ScriptParameters={SCRIPT_PRESET_NAME}",
            f"Symbol={ORIGIN_SYMBOL}",
            "Period=M1",
            "ShutdownTerminal=1",
            "",
        ]
    )
    io_path(paths["startup_ini"].parent).mkdir(parents=True, exist_ok=True)
    io_path(paths["startup_ini"]).write_text(startup_text, encoding="utf-8")
    io_path(paths["startup_ini_repo_copy"].parent).mkdir(parents=True, exist_ok=True)
    io_path(paths["startup_ini_repo_copy"]).write_text(startup_text, encoding="utf-8")
    compile_payload = (
        {"status": "not_attempted_materialize_only"}
        if args.materialize_only
        else mql5_compile.compile_mql5_ea(Path(args.metaeditor_path), paths["portable_script"], paths["compile_log"])
    )
    payload = {
        "script_source": rel(SCRIPT_SOURCE),
        "portable_script": paths["portable_script"].as_posix(),
        "portable_script_sha256": sha256_file(paths["portable_script"]) if path_exists(paths["portable_script"]) else "",
        "preset_path": paths["preset"].as_posix(),
        "preset_sha256": sha256_file(paths["preset"]) if path_exists(paths["preset"]) else "",
        "startup_ini": rel(paths["startup_ini"]),
        "startup_ini_sha256": sha256_file(paths["startup_ini"]) if path_exists(paths["startup_ini"]) else "",
        "startup_ini_repo_copy": rel(paths["startup_ini_repo_copy"]),
        "startup_ini_repo_copy_sha256": sha256_file(paths["startup_ini_repo_copy"]) if path_exists(paths["startup_ini_repo_copy"]) else "",
        "compile": compile_payload,
        "materialize_only": args.materialize_only,
        "claim_boundary": CLAIM_BOUNDARY,
        "effect": "shifted custom symbol seed prepares synthetic current-day visibility diagnostic without changing the frozen ONNX package.",
    }
    write_json(SEED_DIR / "shifted_custom_symbol_seed_prepare.json", payload)
    return payload


def run_shifted_seed(args: argparse.Namespace) -> dict[str, Any]:
    paths = shifted_seed_paths(args)
    if args.materialize_only:
        payload = {"status": "not_attempted_materialize_only", "output_path": paths["common_output"].as_posix()}
        write_json(SEED_DIR / "shifted_custom_symbol_seed_run.json", payload)
        return payload
    if path_exists(paths["common_output"]):
        io_path(paths["common_output"]).unlink()
    process_recovery = qprobe.stop_target_terminal_if_running(Path(args.terminal_path))
    command = [str(Path(args.terminal_path)), "/portable", f"/config:{paths['startup_ini']}"]
    try:
        proc = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=args.seed_timeout_seconds)
        status = "completed_terminal_returncode_zero" if proc.returncode == 0 else "terminal_returncode_nonzero_output_checked"
    except subprocess.TimeoutExpired as exc:
        proc = exc
        status = "blocked_terminal_startup_timeout"
    deadline = time.monotonic() + 60
    while time.monotonic() < deadline and not path_exists(paths["common_output"]):
        time.sleep(1.0)
    script_output: dict[str, Any] = {"status": "missing"}
    if path_exists(paths["common_output"]):
        script_output = read_json(paths["common_output"])
        shutil.copy2(io_path(paths["common_output"]), io_path(SEED_STATUS))
        script_output["repo_copy_path"] = rel(SEED_STATUS)
        script_output["repo_copy_sha256"] = sha256_file(SEED_STATUS)
        if script_output.get("status") == "completed":
            status = "completed_by_script_output"
    payload = {
        "status": status,
        "command": command,
        "returncode": getattr(proc, "returncode", None),
        "stdout": (getattr(proc, "stdout", "") or "")[-2000:],
        "stderr": (getattr(proc, "stderr", "") or "")[-2000:],
        "process_recovery": process_recovery,
        "script_output": script_output,
        "output_path": paths["common_output"].as_posix(),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(SEED_DIR / "shifted_custom_symbol_seed_run.json", payload)
    return payload


def shifted_frame(frame: pd.DataFrame, shift_minutes: int) -> pd.DataFrame:
    shifted = frame.copy()
    delta = timedelta(minutes=shift_minutes)
    shifted["timestamp"] = pd.to_datetime(shifted["timestamp"], errors="coerce", utc=True) + delta
    if "split" in shifted.columns:
        shifted["split"] = shifted["split"].astype(str) + f"__synthetic_shift_{shift_minutes}m"
    return shifted


def materialize_shifted_attempts(args: argparse.Namespace) -> list[dict[str, Any]]:
    common_files = Path(args.common_files_root)
    attempts: list[dict[str, Any]] = []
    sync_rows: list[dict[str, Any]] = []
    expected_rows: list[dict[str, Any]] = []
    shift_rows: list[dict[str, Any]] = []
    for directory in [MT5_DIR, SET_DIR, INI_DIR, REPORT_DIR, FEATURE_DIR, MODEL_DIR, EXPECTED_DIR, TELEMETRY_DIR, SEED_DIR]:
        io_path(directory).mkdir(parents=True, exist_ok=True)
    for base in el.selected_attempts(args.attempt_limit):
        attempt_name = str(base["attempt_name"])
        short_id = short_attempt_id(base)
        feature_order = eo.load_feature_order(str(base["feature_set_id"]))
        source_frame = pd.read_parquet(io_path(ep.FEATURE_FRAME_DIR / f"{base['feature_set_id']}.parquet"))
        source_frame = el.date_filter(source_frame, args.from_date, args.to_date)
        frame = shifted_frame(source_frame, SHIFT_MINUTES)
        local_features = FEATURE_DIR / f"{short_id}_m1440_features.csv"
        local_model = MODEL_DIR / f"{short_id}.onnx"
        expected_tape = EXPECTED_DIR / f"{short_id}_expected.csv"
        mt5.export_mt5_feature_matrix_csv(frame, feature_order, local_features, timestamp_column="timestamp", metadata_columns=("split",))
        shutil.copy2(io_path(Path(base["onnx_path"])), io_path(local_model))
        expected_rows.append(el.write_expected_probability_tape(base, frame, feature_order, expected_tape))
        common_feature_path = f"{COMMON_ROOT}/features/{local_features.name}"
        common_model_path = f"{COMMON_ROOT}/models/{local_model.name}"
        common_telemetry_path = f"{COMMON_ROOT}/t/{short_id}_telemetry.csv"
        common_summary_path = f"{COMMON_ROOT}/t/{short_id}_summary.csv"
        for old_path in [common_telemetry_path, common_summary_path]:
            target = common_files / Path(old_path)
            if path_exists(target):
                io_path(target).unlink()
        sync_rows.append({"sync_id": f"{attempt_name}::features", **mt5.copy_to_common_files(common_files, local_features, common_feature_path)})
        sync_rows.append({"sync_id": f"{attempt_name}::model", **mt5.copy_to_common_files(common_files, local_model, common_model_path)})
        set_name = f"opv2_{RUN_NUMBER}_{base['probe_id']}.set"
        ini_name = f"opv2_{RUN_NUMBER}_{base['probe_id']}.ini"
        set_path = SET_DIR / f"{short_id}.set"
        ini_path = INI_DIR / f"{short_id}.ini"
        report_name = f"Project_Obsidian_Prime_v2_{RUN_NUMBER}_{short_id}"
        params = {
            "InpRunId": f"{RUN_ID}_{attempt_name}",
            "InpExplorationLabel": "stage337ER_ShiftedCustomFailureMemory",
            "InpTierLabel": "Tier A synthetic-shift diagnostic",
            "InpPrimaryActiveTier": "tier_a",
            "InpSplitLabel": "forward_after_2026_04_14_shifted_minus1440m_synthetic",
            "InpMainSymbol": SHIFTED_CUSTOM_SYMBOL,
            "InpTimeframe": 5,
            "InpEnforceM5": True,
            "InpFeatureCsvPath": common_feature_path,
            "InpFeatureCount": int(base["feature_count"]),
            "InpFeatureCsvUseCommonFiles": True,
            "InpFeatureRequireTimestampMatch": True,
            "InpFeatureAllowLatestFallback": False,
            "InpFeatureStrictHeader": True,
            "InpFeatureCsvDelimiter": ",",
            "InpCsvTimestampIsBarClose": True,
            "InpModelPath": common_model_path,
            "InpModelId": base["model_id"],
            "InpModelBackend": "onnx",
            "InpModelUseCommonFiles": True,
            "InpModelUseCpuOnly": True,
            "InpModelNoConversion": False,
            "InpSetOutputShape": True,
            "InpFeatureOrderHash": base["feature_order_hash"],
            "InpFallbackEnabled": False,
            "InpShortThreshold": 0.55,
            "InpLongThreshold": 0.55,
            "InpMinMargin": 0.05,
            "InpDecisionMode": "argmax_probe",
            "InpInvertSignal": False,
            "InpSideFilterEnabled": False,
            "InpAllowTrading": True,
            "InpFixedLot": 0.10,
            "InpMagic": 3371500 + int(base["proxy_rank"]),
            "InpCloseOnFlatSignal": False,
            "InpReverseOnOppositeSignal": True,
            "InpMaxHoldBars": 12,
            "InpMaxConcurrentPositions": 1,
            "InpAtrSltpEnabled": False,
            "InpModelRiskSizingEnabled": False,
            "InpTelemetryEnabled": True,
            "InpTelemetryUseCommonFiles": True,
            "InpTelemetryCsvPath": common_telemetry_path,
            "InpSummaryCsvPath": common_summary_path,
        }
        mt5.materialize_tester_set_file(params, set_path, generated_by="stage337ER_shifted_custom_failure_memory")
        tester_config = mt5.TesterMaterializationConfig(
            expert=mt5.EA_EXPERT_PATH,
            symbol=SHIFTED_CUSTOM_SYMBOL,
            period="M5",
            model=0,
            deposit=DEPOSIT,
            leverage="1:100",
            shutdown_terminal=1,
            from_date=args.shifted_from_date,
            to_date=args.shifted_to_date,
            report=report_name,
        )
        mt5.materialize_tester_ini_file(tester_config, ini_path, set_file_path=Path(set_name))
        source_first = pd.to_datetime(source_frame["timestamp"], utc=True).min() if len(source_frame) else None
        source_last = pd.to_datetime(source_frame["timestamp"], utc=True).max() if len(source_frame) else None
        shifted_first = pd.to_datetime(frame["timestamp"], utc=True).min() if len(frame) else None
        shifted_last = pd.to_datetime(frame["timestamp"], utc=True).max() if len(frame) else None
        shift_rows.append(
            {
                "attempt_name": attempt_name,
                "proxy_rank": base["proxy_rank"],
                "feature_set_id": base["feature_set_id"],
                "source_first_timestamp": source_first,
                "source_last_timestamp": source_last,
                "shift_minutes": SHIFT_MINUTES,
                "shifted_first_timestamp": shifted_first,
                "shifted_last_timestamp": shifted_last,
                "feature_rows": len(frame),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        attempts.append(
            {
                **base,
                "short_attempt_id": short_id,
                "tier": "Tier A synthetic-shift diagnostic",
                "split": "forward_after_2026_04_14_shifted_minus1440m_synthetic",
                "feature_rows": len(frame),
                "source_feature_first_timestamp": str(source_first) if source_first is not None else "",
                "source_feature_last_timestamp": str(source_last) if source_last is not None else "",
                "feature_first_timestamp": str(shifted_first) if shifted_first is not None else "",
                "feature_last_timestamp": str(shifted_last) if shifted_last is not None else "",
                "synthetic_shift_minutes": SHIFT_MINUTES,
                "diagnostic_symbol": SHIFTED_CUSTOM_SYMBOL,
                "diagnostic_model_mode": 0,
                "diagnostic_route": "synthetic_shifted_custom_symbol_no_forward_authority",
                "common_telemetry_path": common_telemetry_path,
                "common_summary_path": common_summary_path,
                "common_feature_path": common_feature_path,
                "common_model_path": common_model_path,
                "local_feature_path": rel(local_features),
                "local_model_path": rel(local_model),
                "expected_probability_tape_path": rel(expected_tape),
                "set_name": set_name,
                "ini_name": ini_name,
                "set_path": rel(set_path),
                "ini_path": rel(ini_path),
                "ini": {"path": rel(ini_path), "tester": {"Report": report_name}},
                "set": {"path": rel(set_path)},
                "from_date": args.shifted_from_date,
                "to_date": args.shifted_to_date,
                "allow_trading": True,
                "fixed_lot": 0.10,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(ATTEMPT_PACKAGE, attempts)
    write_csv(COMMON_SYNC, sync_rows)
    write_csv(EXPECTED_INDEX, expected_rows)
    write_csv(FEATURE_SHIFT_AUDIT, shift_rows)
    return attempts


def broker_gap_reference() -> list[dict[str, Any]]:
    final = read_json(PARENT_FINAL_DECISION) if path_exists(PARENT_FINAL_DECISION) else {}
    summary_rows = read_csv(PARENT_MT5_REPORT_SUMMARY)
    row = {
        "source_run_id": PARENT_RUN_ID,
        "source_decision": final.get("decision", ""),
        "source_judgment": final.get("judgment", ""),
        "latest_feature_timestamp": final.get("latest_feature_timestamp", ""),
        "latest_runtime_timestamp": final.get("latest_runtime_timestamp", ""),
        "blocked_gate_count": len(final.get("blocked_gates", [])) if isinstance(final.get("blocked_gates"), list) else "",
        "rank1_net_profit": final.get("rank1_mt5_summary", {}).get("net_profit", "") if isinstance(final.get("rank1_mt5_summary"), Mapping) else "",
        "rank1_profit_factor": final.get("rank1_mt5_summary", {}).get("profit_factor", "") if isinstance(final.get("rank1_mt5_summary"), Mapping) else "",
        "rank1_drawdown": final.get("rank1_mt5_summary", {}).get("max_drawdown_amount", "") if isinstance(final.get("rank1_mt5_summary"), Mapping) else "",
        "mt5_report_rows": len(summary_rows),
        "effect": "broker Strategy Tester still remains the authority boundary; shifted custom is diagnostic only.",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(BROKER_GAP_REFERENCE, [row])
    return [row]


def visibility_lag_minutes(attempts: Sequence[Mapping[str, Any]], summary_rows: Sequence[Mapping[str, Any]]) -> float | None:
    latest_feature = eq.latest_feature_timestamp(attempts)
    latest_runtime = eq.latest_runtime_timestamp(summary_rows)
    if latest_feature is None or latest_runtime is None:
        return None
    return (latest_feature - latest_runtime).total_seconds() / 60.0


def build_shifted_gate_rows(
    seed_prepare: Mapping[str, Any],
    seed_run: Mapping[str, Any],
    summary_rows: Sequence[Mapping[str, Any]],
    trades: Sequence[Mapping[str, Any]],
    parser_errors: Sequence[Mapping[str, Any]],
    regime_rows: Sequence[Mapping[str, Any]],
    db_rows: Sequence[Mapping[str, Any]],
    lot_rows: Sequence[Mapping[str, Any]],
    cost_rows: Sequence[Mapping[str, Any]],
    curve_rows: Sequence[Mapping[str, Any]],
    attempts: Sequence[Mapping[str, Any]],
    broker_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    seed_output = seed_run.get("script_output", {}) if isinstance(seed_run.get("script_output"), Mapping) else {}
    latest_feature = eq.latest_feature_timestamp(attempts)
    latest_runtime = eq.latest_runtime_timestamp(summary_rows)
    lag = visibility_lag_minutes(attempts, summary_rows)
    seed_ok = seed_output.get("status") == "completed"
    lag_ok = lag is not None and lag <= 10
    rows = [
        ("frozen_identity", "covered", rel(ATTEMPT_PACKAGE), "ONNX, feature order, argmax decision, fixed lot, risk, and thresholds are unchanged."),
        ("broker_forward_gap_reference", "covered", rel(BROKER_GAP_REFERENCE), f"source_decision={broker_rows[0].get('source_decision', '') if broker_rows else ''}"),
        ("shifted_custom_seed_prepare", "covered" if seed_prepare else "blocked", rel(SEED_DIR / "shifted_custom_symbol_seed_prepare.json"), f"compile_status={seed_prepare.get('compile', {}).get('status', '') if isinstance(seed_prepare.get('compile'), Mapping) else ''}"),
        ("shifted_custom_seed_run", "covered" if seed_ok or seed_run.get("status") == "not_attempted_materialize_only" else "blocked", rel(SEED_STATUS), f"seed_status={seed_output.get('status', seed_run.get('status', ''))}"),
        ("shifted_latest_visibility", "covered_boundary" if lag_ok else "blocked", rel(MT5_REPORT_SUMMARY), f"feature_last={latest_feature};runtime_last={latest_runtime};lag_minutes={lag}"),
        ("mt5_report", "covered_boundary" if summary_rows else "blocked", rel(MT5_REPORT_SUMMARY), f"strategy_tester_report_rows={len(summary_rows)}"),
        ("trade_list_parse", "covered_boundary" if trades and not parser_errors else "blocked", rel(TRADE_RECORDS), f"trade_rows={len(trades)};parser_errors={len(parser_errors)}"),
        ("regime_attribution", "covered_boundary" if regime_rows else "blocked", rel(REGIME_ATTRIBUTION), "time/session/volatility/ADX/VIX/USD/rate slices generated where features exist."),
        ("db_attribution", "covered_boundary" if db_rows else "blocked", rel(DB_ATTRIBUTION), "D/B source unavailable; direction proxy boundary recorded."),
        ("lot_normalized", "covered_boundary" if lot_rows else "blocked", rel(LOT_NORMALIZED), "Fixed-lot and per-lot results generated without lot optimization."),
        ("cost_stress", "covered_boundary" if cost_rows else "blocked", rel(COST_STRESS), "Spread/slippage point stress generated after the fact."),
        ("curve_pocket", "covered_boundary" if curve_rows else "blocked", rel(CURVE_POCKET), "Worst month, chronology and rolling pockets generated."),
        ("forward_decision_authority", "out_of_scope_by_claim", rel(FINAL_DECISION), "Synthetic shifted custom route cannot claim Forward Passed or Forward Failed."),
        ("no_goal_achieve", "covered", rel(FINAL_DECISION), "Goal Achieve is not claimed in this run."),
    ]
    payload = [{"gate_name": name, "status": status, "evidence_path": path, "effect": effect, "claim_boundary": CLAIM_BOUNDARY} for name, status, path, effect in rows]
    write_csv(GATE_AUDIT, payload)
    return payload


def build_failure_memory_rows(
    summary_rows: Sequence[Mapping[str, Any]],
    curve_rows: Sequence[Mapping[str, Any]],
    cost_rows: Sequence[Mapping[str, Any]],
    trades: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    curve_by_attempt = {(row.get("attempt_name"), row.get("pocket_type")): row for row in curve_rows}
    cost_by_attempt = {(row.get("attempt_name"), number(row.get("extra_round_trip_points"))): row for row in cost_rows}
    rows: list[dict[str, Any]] = []
    for summary in summary_rows:
        attempt = summary.get("attempt_name", "")
        attempt_trades = [row for row in trades if row.get("attempt_name") == attempt]
        long_rows = [row for row in attempt_trades if str(row.get("direction", "")).lower() in {"buy", "long"}]
        short_rows = [row for row in attempt_trades if str(row.get("direction", "")).lower() in {"sell", "short"}]
        curve = curve_by_attempt.get((attempt, "attempt_summary"), {})
        cost_one = cost_by_attempt.get((attempt, 1.0), {})
        cost_five = cost_by_attempt.get((attempt, 5.0), {})
        net = number(summary.get("net_profit"))
        pf = number(summary.get("profit_factor"), math.nan)
        curve_read = str(curve.get("curve_read", ""))
        if net <= 0:
            kpi_read = "net_negative"
        elif not math.isfinite(pf) or pf <= 1.0:
            kpi_read = "pf_unprofitable"
        elif pf < 1.10:
            kpi_read = "pf_thin_below_1_10"
        elif curve_read != "constructive_forward_shape":
            kpi_read = f"curve_not_constructive::{curve_read}"
        else:
            kpi_read = "constructive_in_synthetic_route_only"
        rows.append(
            {
                "attempt_name": attempt,
                "proxy_rank": summary.get("proxy_rank", ""),
                "model_id": summary.get("model_id", ""),
                "feature_set_id": summary.get("feature_set_id", ""),
                "net_profit": summary.get("net_profit", ""),
                "profit_factor": summary.get("profit_factor", ""),
                "trade_count": summary.get("trade_count", ""),
                "max_drawdown_amount": summary.get("max_drawdown_amount", ""),
                "recovery_factor": summary.get("recovery_factor", ""),
                "expectancy": summary.get("expectancy", ""),
                "long_net_profit": sum(number(row.get("net_profit")) for row in long_rows),
                "long_trade_count": len(long_rows),
                "short_net_profit": sum(number(row.get("net_profit")) for row in short_rows),
                "short_trade_count": len(short_rows),
                "cost_1pt_pf": cost_one.get("profit_factor", ""),
                "cost_1pt_read": cost_one.get("stress_read", ""),
                "cost_5pt_net": cost_five.get("net_profit", ""),
                "cost_5pt_read": cost_five.get("stress_read", ""),
                "curve_read": curve_read,
                "worst_slice_axis": curve.get("worst_slice_axis", ""),
                "worst_slice_bucket": curve.get("worst_slice_bucket", ""),
                "worst_slice_net_profit": curve.get("worst_slice_net_profit", ""),
                "failure_memory_read": kpi_read,
                "authority_boundary": "synthetic_shifted_custom_diagnostic_only_no_forward_failed_claim",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(FAILURE_MEMORY, rows)
    return rows


def final_decision_payload(
    seed_run: Mapping[str, Any],
    summary_rows: Sequence[Mapping[str, Any]],
    curve_rows: Sequence[Mapping[str, Any]],
    gate_rows: Sequence[Mapping[str, Any]],
    attempts: Sequence[Mapping[str, Any]],
    failure_rows: Sequence[Mapping[str, Any]],
    broker_rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    blocked_gates = [row for row in gate_rows if row.get("status") == "blocked"]
    rank1 = next((row for row in summary_rows if str(row.get("proxy_rank")) == "1"), {})
    curve_rank1 = next((row for row in curve_rows if str(row.get("proxy_rank")) == "1" and row.get("pocket_type") == "attempt_summary"), {})
    failure_counts = {
        "attempts_with_negative_net": sum(1 for row in failure_rows if number(row.get("net_profit")) <= 0),
        "attempts_with_pf_below_1": sum(1 for row in failure_rows if number(row.get("profit_factor"), math.nan) <= 1.0),
        "attempts_with_cost_1pt_break_or_thin": sum(1 for row in failure_rows if str(row.get("cost_1pt_read", "")).startswith("cost_") and row.get("cost_1pt_read") != "cost_survives_this_scenario"),
        "attempts_with_nonconstructive_curve": sum(1 for row in failure_rows if row.get("curve_read") != "constructive_forward_shape"),
        "attempts_with_short_net_negative": sum(1 for row in failure_rows if number(row.get("short_net_profit")) < 0),
    }
    completed = not blocked_gates
    return {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS_COMPLETED if completed else STATUS_BLOCKED,
        "judgment": JUDGMENT_COMPLETED if completed else JUDGMENT_BLOCKED,
        "decision": "Forward Blocked",
        "diagnostic_decision": "failure_memory_strengthened_synthetic_shifted_custom_no_forward_failed_authority" if completed else "diagnostic_blocked_no_forward_decision",
        "next_action": NEXT_RUN_ID,
        "synthetic_symbol": SHIFTED_CUSTOM_SYMBOL,
        "shift_minutes": SHIFT_MINUTES,
        "seed_status": seed_run.get("script_output", {}).get("status", seed_run.get("status", "")) if isinstance(seed_run.get("script_output"), Mapping) else seed_run.get("status", ""),
        "latest_feature_timestamp": str(eq.latest_feature_timestamp(attempts)),
        "latest_runtime_timestamp": str(eq.latest_runtime_timestamp(summary_rows)),
        "latest_visibility_lag_minutes": visibility_lag_minutes(attempts, summary_rows),
        "attempt_rows": len(summary_rows),
        "trade_rows": len(read_csv(TRADE_RECORDS)),
        "rank1_mt5_summary": rank1,
        "rank1_curve_summary": curve_rank1,
        "failure_counts": failure_counts,
        "broker_forward_reference": broker_rows[0] if broker_rows else {},
        "blocked_gates": blocked_gates,
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed_synthetic_route",
        "forward_blocked": "claimed_by_broker_visibility_gap_reference",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "deployment": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def report_text(final: Mapping[str, Any]) -> str:
    rank1 = final.get("rank1_mt5_summary", {}) if isinstance(final.get("rank1_mt5_summary"), Mapping) else {}
    counts = final.get("failure_counts", {}) if isinstance(final.get("failure_counts"), Mapping) else {}
    broker = final.get("broker_forward_reference", {}) if isinstance(final.get("broker_forward_reference"), Mapping) else {}
    return f"""# run337ER shifted custom failure memory(시프트 커스텀 실패 기억)

## 판정

- decision(판정): `{final.get("decision", "")}`
- diagnostic decision(진단 판정): `{final.get("diagnostic_decision", "")}`
- status(상태): `{final.get("status", "")}`
- goal achieve(목표 달성): `not_claimed(주장 안 함)`

## 실행 효과

run337EQ의 broker Strategy Tester(브로커 전략 테스터)는 최신 feature(피처) `2026-05-28 06:00 UTC`까지 닿지 못해 Forward Blocked(전진 차단)으로 남았다. run337ER는 같은 frozen ONNX(고정 ONNX), feature order(피처 순서), argmax decision surface(argmax 결정 표면), threshold(임계값), fixed lot(고정 랏), risk logic(위험 로직)을 유지하고, timestamp shift(타임스탬프 이동) custom symbol(커스텀 심볼) `{SHIFTED_CUSTOM_SYMBOL}`만 써서 tester visibility(테스터 가시성)를 진단했다.

효과(effect, 효과)는 broker forward authority(브로커 전진 권한)를 우회하지 않고, 최신 구간이 보일 때 KPI(핵심 지표)와 curve pocket(곡선 포켓)이 어떤 실패 기억을 만드는지만 분리한 것이다.

## 핵심 수치

- seed status(seed 상태): `{final.get("seed_status", "")}`
- shifted feature last(이동 피처 마지막): `{final.get("latest_feature_timestamp", "")}`
- runtime last(런타임 마지막): `{final.get("latest_runtime_timestamp", "")}`
- latest lag minutes(최신 지연 분): `{final.get("latest_visibility_lag_minutes", "")}`
- attempt rows(시도 행): `{final.get("attempt_rows", "")}`
- trade rows(거래 행): `{final.get("trade_rows", "")}`
- rank1 net/PF/DD(rank1 순손익/손익비/낙폭): `{rank1.get("net_profit", "")}` / `{rank1.get("profit_factor", "")}` / `{rank1.get("max_drawdown_amount", "")}`
- failure counts(실패 개수): `{json.dumps(json_ready(counts), ensure_ascii=False, sort_keys=True)}`

## 경계

- Forward Passed(전진 통과): `not_claimed(주장 안 함)`
- Forward Failed(전진 실패): `not_claimed_synthetic_route(합성 경로라 주장 안 함)`
- Forward Blocked(전진 차단): `claimed_by_broker_visibility_gap_reference(브로커 가시성 공백 근거로 주장)`
- live readiness(실거래 준비), deployment(배포), operating promotion(운영 승격), runtime authority(런타임 권위): 모두 `not_claimed(주장 안 함)`

## 근거 파일

- shifted MT5 report(이동 MT5 보고): `{rel(MT5_REPORT_SUMMARY)}`
- regime attribution(국면 귀속): `{rel(REGIME_ATTRIBUTION)}`
- D/B attribution(D/B 귀속): `{rel(DB_ATTRIBUTION)}`
- lot normalized(랏 정규화): `{rel(LOT_NORMALIZED)}`
- cost stress(비용 스트레스): `{rel(COST_STRESS)}`
- curve pocket(곡선 포켓): `{rel(CURVE_POCKET)}`
- failure memory matrix(실패 기억 행렬): `{rel(FAILURE_MEMORY)}`
- gate audit(게이트 감사): `{rel(GATE_AUDIT)}`
- final decision(최종 판정): `{rel(FINAL_DECISION)}`

## 다음 작업

`{NEXT_RUN_ID}`는 broker rollover(브로커 롤오버) 재확인 또는 failure memory(실패 기억) 기반 no-overfit repair(비과적합 수리) 설계로 이어진다. 이 수리는 새 데이터에 threshold(임계값)를 맞추는 방식이 아니라, 실패 원인을 고립해서 후보군 설계를 다시 세우는 방식이어야 한다.
"""


def decision_text(final: Mapping[str, Any]) -> str:
    return f"""# 2026-05-28 Stage337ER decision(결정)

- run(실행): `{RUN_ID}`
- decision(판정): `{final.get("decision", "")}`
- diagnostic decision(진단 판정): `{final.get("diagnostic_decision", "")}`
- status(상태): `{final.get("status", "")}`

## 이유

run337ER의 shifted custom symbol(시프트 커스텀 심볼) 진단은 최신 feature window(피처 창)를 보는 데 성공했더라도 합성 경로(synthetic route, 합성 경로)다. 따라서 Forward Passed(전진 통과)나 Forward Failed(전진 실패)를 새로 주장하지 않는다.

기존 broker forward(브로커 전진) 판정은 run337EQ의 latest visibility gap(최신 가시성 공백) 때문에 Forward Blocked(전진 차단)로 유지한다.

## 금지 주장

live readiness(실거래 준비), deployment(배포), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 모두 주장하지 않는다.
"""


def main() -> int:
    args = parse_args()
    configure_eq_globals()
    seed_prepare = prepare_shifted_seed(args)
    seed_run = run_shifted_seed(args)
    if args.seed_only:
        payload = {"run_id": RUN_ID, "seed_prepare": seed_prepare, "seed_run": seed_run, "claim_boundary": CLAIM_BOUNDARY}
        print(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    attempts = materialize_shifted_attempts(args)
    execution = eq.run_mt5(args, attempts)
    summary_rows = eq.build_mt5_summary(execution, attempts)
    trades, _checks, parser_errors = eq.build_trade_records(execution, attempts)
    regime_rows = eq.build_regime_rows(trades)
    db_rows = eq.build_db_rows(trades)
    lot_rows = eq.build_lot_rows(trades)
    cost_rows = eq.build_cost_rows(trades)
    curve_rows = eq.build_curve_rows(trades, regime_rows, cost_rows)
    signal_rows = eq.build_signal_rows()
    broker_rows = broker_gap_reference()
    gate_rows = build_shifted_gate_rows(
        seed_prepare,
        seed_run,
        summary_rows,
        trades,
        parser_errors,
        regime_rows,
        db_rows,
        lot_rows,
        cost_rows,
        curve_rows,
        attempts,
        broker_rows,
    )
    failure_rows = build_failure_memory_rows(summary_rows, curve_rows, cost_rows, trades)
    final = final_decision_payload(seed_run, summary_rows, curve_rows, gate_rows, attempts, failure_rows, broker_rows)
    final["signal_attribution_rows"] = len(signal_rows)
    write_json(FINAL_DECISION, final)
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "inputs": [rel(PARENT_FINAL_DECISION), rel(PARENT_MT5_REPORT_SUMMARY), rel(ep.FINAL_DECISION), rel(ep.FEATURE_SET_SUMMARY)],
            "outputs": [
                rel(ATTEMPT_PACKAGE),
                rel(FEATURE_SHIFT_AUDIT),
                rel(SEED_STATUS),
                rel(MT5_EXECUTION_RESULT),
                rel(MT5_REPORT_SUMMARY),
                rel(TRADE_RECORDS),
                rel(REGIME_ATTRIBUTION),
                rel(DB_ATTRIBUTION),
                rel(LOT_NORMALIZED),
                rel(COST_STRESS),
                rel(CURVE_POCKET),
                rel(FAILURE_MEMORY),
                rel(GATE_AUDIT),
                rel(FINAL_DECISION),
                rel(REPORT_PATH),
                rel(DECISION_DOC),
                rel(RUN_MANIFEST),
            ],
            "from_date": args.from_date,
            "to_date": args.to_date,
            "shifted_from_date": args.shifted_from_date,
            "shifted_to_date": args.shifted_to_date,
            "shift_minutes": SHIFT_MINUTES,
            "created_at_utc": now_utc(),
            "claim_boundary": CLAIM_BOUNDARY,
            "script_sha256": sha256_file(Path(__file__)),
        },
    )
    write_bom_text(REPORT_PATH, report_text(final))
    write_bom_text(DECISION_DOC, decision_text(final))
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
