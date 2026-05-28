from __future__ import annotations

import argparse
import csv
import json
import math
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

import joblib
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists  # noqa: E402
from foundation.mt5 import runtime_support as mt5  # noqa: E402
from stage_pipelines.stage337 import materialize_argmax_adapter_parity_probe_contract as ej  # noqa: E402
from stage_pipelines.stage337 import materialize_proxy_survivor_row_level_runtime_probe_inputs as eh  # noqa: E402
from stage_pipelines.stage337 import review_argmax_probe_decision_surface_implementation as ek  # noqa: E402
from stage_pipelines.stage337.design_directional_label_action_repair import (  # noqa: E402
    now_utc,
    read_csv,
    read_json,
    read_text_lossless,
    rel,
    replace_bullet_value,
    upsert_csv,
    write_csv,
    write_json,
    write_md,
    write_text_preserving,
)


TODAY = "2026-05-28"
STAGE_ID = eh.STAGE_ID
RUN_NUMBER = "run337EL"
RUN_ID = "run337EL_materialize_common_files_and_run_argmax_parity_probe_without_db_v1"
PARENT_RUN_ID = ek.RUN_ID
NEXT_RUN_ID = "run337EM_review_or_expand_argmax_runtime_parity_probe_without_db_v1"
STATUS_EXECUTED = "completed_stage337EL_argmax_runtime_parity_probe_executed_review_required_no_selection"
STATUS_BLOCKED = "blocked_stage337EL_argmax_runtime_parity_probe_handoff_or_terminal_issue_no_selection"
JUDGMENT_EXECUTED = "argmax_runtime_probe_executed_but_forward_and_runtime_authority_not_claimed"
JUDGMENT_BLOCKED = "argmax_runtime_probe_not_sufficient_for_parity_judgment_repair_required"
DECISION_EXECUTED = "stage337EL_open_run337EM_review_or_expand_argmax_runtime_parity_probe"
DECISION_BLOCKED = "stage337EL_open_run337EM_repair_argmax_runtime_parity_probe_handoff"
CLAIM_BOUNDARY = (
    "research_development_only_stage337EL_argmax_runtime_parity_probe_without_db_"
    "no_new_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = eh.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MT5_DIR = RUN_DIR / "mt5"
SET_DIR = MT5_DIR / "sets"
INI_DIR = MT5_DIR / "inis"
REPORT_COPY_DIR = MT5_DIR / "reports"
MODEL_DIR = RUN_DIR / "models"
FEATURE_DIR = RUN_DIR / "feature_matrices"
EXPECTED_DIR = RUN_DIR / "expected_probability_tapes"
TELEMETRY_DIR = RUN_DIR / "runtime_telemetry"
REVIEWS_DIR = eh.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337EL_argmax_runtime_parity_probe.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337EL_argmax_runtime_parity_probe.md"
SELECTED_STATUS = eh.SELECTED_STATUS
STAGE_BRIEF = eh.STAGE_BRIEF
WORKSPACE_STATE = eh.WORKSPACE_STATE
CURRENT_STATE = eh.CURRENT_STATE
CHANGELOG = eh.CHANGELOG
RUN_REGISTRY = eh.RUN_REGISTRY
ALPHA_LEDGER = eh.ALPHA_LEDGER
ARTIFACT_REGISTRY = eh.ARTIFACT_REGISTRY
STAGE_LEDGER = eh.STAGE_LEDGER

EK_FINAL = ek.FINAL_DECISION
EK_GATES = ek.REQUIRED_GATE_AUDIT
EK_SETTINGS_CONTRACT = ek.SETTINGS_CONTRACT
EK_COMPILE_REVIEW = ek.COMPILE_REVIEW
EK_EL_QUEUE = ek.EL_QUEUE
EJ_ADAPTER_PROBE_MANIFEST = ej.ADAPTER_PROBE_MANIFEST
EJ_FEATURE_HANDOFF_CONTRACT = ej.FEATURE_HANDOFF_CONTRACT
EH_FEATURE_HANDOFF = eh.FEATURE_HANDOFF
EG_PACKAGE_PRECHECK = STAGE_DIR / "02_runs" / "run337EG" / "survivor_package_precheck.csv"

DEFAULT_TERMINAL = Path("C:/Program Files/MetaTrader 5/terminal64.exe")
DEFAULT_COMMON_FILES = Path("C:/Users/awdse/AppData/Roaming/MetaQuotes/Terminal/Common/Files")
TERMINAL_DATA_ROOT = ROOT.parents[2]
DEFAULT_TESTER_PROFILE_ROOT = TERMINAL_DATA_ROOT / "MQL5" / "Profiles" / "Tester"
COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage337/{RUN_NUMBER}_argmax_runtime_parity_probe"
COMMON_MODEL_DIR = f"{COMMON_ROOT}/models"
COMMON_FEATURE_DIR = f"{COMMON_ROOT}/features"
COMMON_TELEMETRY_DIR = f"{COMMON_ROOT}/telemetry"

ATTEMPT_PACKAGE = RUN_DIR / "argmax_runtime_probe_attempt_package.csv"
COMMON_SYNC = RUN_DIR / "common_files_sync.csv"
EXPECTED_TAPE_INDEX = RUN_DIR / "expected_probability_tape_index.csv"
EXECUTION_RESULT = RUN_DIR / "mt5_execution_result.json"
EXECUTION_SUMMARY = RUN_DIR / "argmax_runtime_probe_execution_summary.csv"
RUNTIME_DIFF = RUN_DIR / "runtime_probability_decision_diff.csv"
TERMINAL_PROCESS_AUDIT = RUN_DIR / "terminal_process_audit.json"
RUNTIME_IDENTITY = RUN_DIR / "runtime_identity.csv"
TESTER_SETTINGS_IDENTITY = RUN_DIR / "tester_settings_identity.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
FORENSICS_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    EK_FINAL,
    EK_GATES,
    EK_SETTINGS_CONTRACT,
    EK_COMPILE_REVIEW,
    EK_EL_QUEUE,
    EJ_ADAPTER_PROBE_MANIFEST,
    EJ_FEATURE_HANDOFF_CONTRACT,
    EH_FEATURE_HANDOFF,
    EG_PACKAGE_PRECHECK,
    ROOT / mt5.EA_SOURCE_PATH,
)
OUTPUT_FILES = (
    ATTEMPT_PACKAGE,
    COMMON_SYNC,
    EXPECTED_TAPE_INDEX,
    EXECUTION_RESULT,
    EXECUTION_SUMMARY,
    RUNTIME_DIFF,
    TERMINAL_PROCESS_AUDIT,
    RUNTIME_IDENTITY,
    TESTER_SETTINGS_IDENTITY,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    RUNTIME_RECEIPT,
    FORENSICS_RECEIPT,
    JUDGMENT_RECEIPT,
    LINEAGE_RECEIPT,
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
    "proxy_rank",
    "feature_set_id",
    "feature_count",
    "feature_order_hash",
    "feature_local_path",
    "model_local_path",
    "expected_probability_tape_path",
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
EXPECTED_INDEX_COLUMNS = (
    "attempt_name",
    "model_id",
    "expected_probability_tape_path",
    "rows",
    "decision_long",
    "decision_short",
    "decision_flat",
    "feature_order_hash",
    "sha256",
    "claim_boundary",
)
SUMMARY_COLUMNS = (
    "attempt_name",
    "probe_id",
    "model_id",
    "tester_status",
    "runtime_status",
    "returncode",
    "blocker",
    "telemetry_cycle_rows",
    "ready_model_rows",
    "matched_rows",
    "expected_missing_rows",
    "probability_mismatch_rows",
    "decision_mismatch_rows",
    "max_abs_probability_diff",
    "first_ready_bar_time",
    "last_ready_bar_time",
    "comparison_status",
    "feature_ready_count",
    "model_ok_count",
    "long_count",
    "short_count",
    "flat_count",
    "order_attempt_count",
    "order_fill_count",
    "common_telemetry_path",
    "local_telemetry_path",
    "local_summary_path",
    "claim_boundary",
)
DIFF_COLUMNS = (
    "attempt_name",
    "bar_time",
    "expected_found",
    "probability_match",
    "decision_match",
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
GATE_COLUMNS = ("gate_id", "status", "observed", "expected", "effect", "claim_boundary")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stage337EL argmax runtime parity probe.")
    parser.add_argument("--terminal-path", default=str(DEFAULT_TERMINAL))
    parser.add_argument("--common-files-root", default=str(DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--attempt-limit", type=int, default=1)
    parser.add_argument("--from-date", default="2026.04.10")
    parser.add_argument("--to-date", default="2026.04.14")
    parser.add_argument("--timeout-seconds", type=int, default=420)
    parser.add_argument("--wait-timeout-seconds", type=int, default=90)
    parser.add_argument("--materialize-only", action="store_true")
    return parser.parse_args()


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


def write_local_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column, "")) for column in columns})
    return path


def fail_if_missing(paths: Sequence[Path]) -> list[Path]:
    return [path for path in paths if not path_exists(path)]


def append_once(text: str, entry: str, unique: str) -> str:
    if unique in text:
        return text
    return text.rstrip() + "\n" + entry + "\n"


def prepend_once(text: str, heading: str, entry: str, unique: str) -> str:
    if unique in text:
        return text
    return text.replace(heading, f"{heading}\n{entry}", 1)


def safe_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_")[:80]


def sha256(path: Path) -> str:
    return mt5.sha256_file(path)


def terminal_process_audit() -> dict[str, Any]:
    import subprocess

    command = [
        "powershell",
        "-NoProfile",
        "-Command",
        "Get-CimInstance Win32_Process -Filter \"name = 'terminal64.exe'\" | Select-Object ProcessId,ExecutablePath,CommandLine | ConvertTo-Json -Compress",
    ]
    proc = subprocess.run(command, text=True, capture_output=True, timeout=30)
    payload = proc.stdout.strip()
    return {
        "status": "no_terminal64_process" if not payload else "terminal64_process_present",
        "returncode": proc.returncode,
        "stdout": payload,
        "stderr": proc.stderr[-1000:],
    }


def load_feature_contracts() -> dict[str, dict[str, Any]]:
    rows = pd.read_csv(io_path(EH_FEATURE_HANDOFF)).to_dict("records")
    return {str(row["feature_set_id"]): row for row in rows}


def load_package_paths() -> dict[str, dict[str, str]]:
    rows = read_csv(EG_PACKAGE_PRECHECK)
    return {row["model_id"]: row for row in rows}


def selected_attempts(limit: int) -> list[dict[str, Any]]:
    manifest = pd.read_csv(io_path(EJ_ADAPTER_PROBE_MANIFEST)).sort_values("proxy_rank")
    package = load_package_paths()
    attempts: list[dict[str, Any]] = []
    for row in manifest.to_dict("records")[: max(1, limit)]:
        model_id = str(row["model_id"])
        package_row = package.get(model_id, {})
        attempts.append(
            {
                "attempt_name": f"rank{int(row['proxy_rank']):02d}_{safe_name(model_id)}",
                "probe_id": row["probe_id"],
                "model_id": model_id,
                "proxy_rank": int(row["proxy_rank"]),
                "onnx_path": ROOT / str(row["onnx_path"]),
                "model_path": ROOT / str(package_row.get("model_path", "")),
                "feature_set_id": row["feature_set_id"],
                "feature_count": int(row["feature_count"]),
                "feature_order_hash": row["feature_order_hash"],
            }
        )
    return attempts


def date_filter(frame: pd.DataFrame, from_date: str, to_date: str) -> pd.DataFrame:
    timestamps = pd.to_datetime(frame["timestamp"], utc=True)
    start = pd.Timestamp(from_date.replace(".", "-"), tz="UTC")
    end = pd.Timestamp(to_date.replace(".", "-"), tz="UTC")
    out = frame.loc[(timestamps >= start) & (timestamps < end)].copy()
    out["timestamp"] = pd.to_datetime(out["timestamp"], utc=True)
    return out


def ordered_probabilities(model: Any, matrix: np.ndarray) -> np.ndarray:
    probs = np.asarray(model.predict_proba(matrix), dtype="float64")
    classes = [int(value) for value in getattr(model, "classes_", [0, 1, 2])]
    ordered = np.zeros((len(probs), 3), dtype="float64")
    for source_index, cls in enumerate(classes):
        if cls in {0, 1, 2}:
            ordered[:, cls] = probs[:, source_index]
    return ordered


def write_expected_probability_tape(
    attempt: Mapping[str, Any],
    frame: pd.DataFrame,
    feature_order: Sequence[str],
    output_path: Path,
) -> dict[str, Any]:
    model = joblib.load(io_path(Path(str(attempt["model_path"]))))
    matrix = frame.loc[:, list(feature_order)].to_numpy(dtype="float64", copy=False)
    probs = ordered_probabilities(model, matrix)
    decisions = np.asarray(["short", "flat", "long"], dtype=object)[probs.argmax(axis=1)]
    payload = pd.DataFrame(
        {
            "bar_time": frame["timestamp"].dt.strftime("%Y.%m.%d %H:%M:%S"),
            "timestamp_utc": frame["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "split": frame.get("split", "").astype(str).to_numpy() if "split" in frame.columns else "",
            "p_short": probs[:, 0],
            "p_flat": probs[:, 1],
            "p_long": probs[:, 2],
            "decision": decisions,
        }
    )
    io_path(output_path.parent).mkdir(parents=True, exist_ok=True)
    payload.to_csv(io_path(output_path), index=False, encoding="utf-8", float_format="%.12g")
    counts = payload["decision"].value_counts().to_dict()
    return {
        "attempt_name": attempt["attempt_name"],
        "model_id": attempt["model_id"],
        "expected_probability_tape_path": rel(output_path),
        "rows": len(payload),
        "decision_long": int(counts.get("long", 0)),
        "decision_short": int(counts.get("short", 0)),
        "decision_flat": int(counts.get("flat", 0)),
        "feature_order_hash": attempt["feature_order_hash"],
        "sha256": sha256(output_path),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def copy_to_common(common_root: Path, local_path: Path, common_path: str, sync_id: str, effect: str) -> dict[str, Any]:
    target = common_root / Path(common_path)
    io_path(target.parent).mkdir(parents=True, exist_ok=True)
    if path_exists(target):
        io_path(target).unlink()
    shutil.copy2(io_path(local_path), io_path(target))
    return {
        "sync_id": sync_id,
        "source_path": rel(local_path),
        "target_path": target.as_posix(),
        "exists": "true" if path_exists(target) else "false",
        "sha256": sha256(target) if path_exists(target) else "",
        "status": "copied" if path_exists(target) else "missing_after_copy",
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def materialize_attempts(args: argparse.Namespace) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    common_root = Path(args.common_files_root)
    feature_contracts = load_feature_contracts()
    attempts: list[dict[str, Any]] = []
    sync_rows: list[dict[str, Any]] = []
    expected_index: list[dict[str, Any]] = []
    for attempt in selected_attempts(args.attempt_limit):
        feature_row = feature_contracts[str(attempt["feature_set_id"])]
        feature_order = json.loads(str(feature_row["included_features_json"]))
        source = ROOT / str(feature_row["source_model_input"])
        frame = date_filter(pd.read_parquet(io_path(source)), args.from_date, args.to_date)
        local_features = FEATURE_DIR / f"{attempt['attempt_name']}_features.csv"
        local_model = MODEL_DIR / f"{attempt['attempt_name']}.onnx"
        expected_tape = EXPECTED_DIR / f"{attempt['attempt_name']}_expected_probability_tape.csv"
        feature_export = mt5.export_mt5_feature_matrix_csv(frame, feature_order, local_features, timestamp_column="timestamp", metadata_columns=("split",))
        io_path(local_model.parent).mkdir(parents=True, exist_ok=True)
        shutil.copy2(io_path(Path(str(attempt["onnx_path"]))), io_path(local_model))
        expected_index.append(write_expected_probability_tape(attempt, frame, feature_order, expected_tape))
        common_feature_path = f"{COMMON_FEATURE_DIR}/{local_features.name}"
        common_model_path = f"{COMMON_MODEL_DIR}/{local_model.name}"
        common_telemetry_path = f"{COMMON_TELEMETRY_DIR}/{attempt['attempt_name']}_telemetry.csv"
        common_summary_path = f"{COMMON_TELEMETRY_DIR}/{attempt['attempt_name']}_summary.csv"
        for common_file in (common_telemetry_path, common_summary_path):
            target = common_root / Path(common_file)
            if path_exists(target):
                io_path(target).unlink()
        sync_rows.append(copy_to_common(common_root, local_features, common_feature_path, f"{attempt['attempt_name']}::features", "feature CSV copied to Common Files(피처 CSV를 Common Files로 복사)"))
        sync_rows.append(copy_to_common(common_root, local_model, common_model_path, f"{attempt['attempt_name']}::model", "ONNX copied to Common Files(ONNX를 Common Files로 복사)"))
        report_name = f"Project_Obsidian_Prime_v2_{RUN_NUMBER}_{attempt['attempt_name']}"
        set_name = f"opv2_{RUN_NUMBER}_{attempt['probe_id']}.set"
        ini_name = f"opv2_{RUN_NUMBER}_{attempt['probe_id']}.ini"
        set_path = SET_DIR / f"{attempt['attempt_name']}.set"
        ini_path = INI_DIR / f"{attempt['attempt_name']}.ini"
        params = {
            "InpRunId": f"{RUN_ID}_{attempt['attempt_name']}",
            "InpExplorationLabel": "stage337_ArgmaxRuntimeParityProbe",
            "InpTierLabel": "Tier A",
            "InpPrimaryActiveTier": "tier_a",
            "InpSplitLabel": "argmax_parity_probe",
            "InpMainSymbol": "US100",
            "InpTimeframe": 5,
            "InpEnforceM5": True,
            "InpFeatureCsvPath": common_feature_path,
            "InpFeatureCount": int(attempt["feature_count"]),
            "InpFeatureCsvUseCommonFiles": True,
            "InpFeatureRequireTimestampMatch": True,
            "InpFeatureAllowLatestFallback": False,
            "InpFeatureStrictHeader": True,
            "InpFeatureCsvDelimiter": ",",
            "InpCsvTimestampIsBarClose": True,
            "InpModelPath": common_model_path,
            "InpModelId": attempt["model_id"],
            "InpModelBackend": "onnx",
            "InpModelUseCommonFiles": True,
            "InpModelUseCpuOnly": True,
            "InpModelNoConversion": False,
            "InpSetOutputShape": True,
            "InpFeatureOrderHash": attempt["feature_order_hash"],
            "InpFallbackEnabled": False,
            "InpFallbackFeatureCsvPath": common_feature_path,
            "InpFallbackFeatureCount": int(attempt["feature_count"]),
            "InpFallbackModelPath": common_model_path,
            "InpFallbackModelId": f"{attempt['model_id']}_fallback_disabled",
            "InpFallbackModelBackend": "onnx",
            "InpFallbackFeatureOrderHash": attempt["feature_order_hash"],
            "InpShortThreshold": 0.55,
            "InpLongThreshold": 0.55,
            "InpMinMargin": 0.05,
            "InpDecisionMode": "argmax_probe",
            "InpInvertSignal": False,
            "InpFallbackShortThreshold": 0.55,
            "InpFallbackLongThreshold": 0.55,
            "InpFallbackMinMargin": 0.05,
            "InpFallbackDecisionMode": "argmax_probe",
            "InpFallbackInvertSignal": False,
            "InpSideFilterEnabled": False,
            "InpAllowTrading": False,
            "InpFixedLot": 0.10,
            "InpMagic": 3371200 + int(attempt["proxy_rank"]),
            "InpCloseOnFlatSignal": False,
            "InpReverseOnOppositeSignal": True,
            "InpCloseOnlyOnOppositeSignal": False,
            "InpMaxHoldBars": 12,
            "InpMaxConcurrentPositions": 1,
            "InpReentryCooldownBars": 0,
            "InpSameDirectionReentryCooldownBars": 0,
            "InpAtrSltpEnabled": False,
            "InpModelRiskSizingEnabled": False,
            "InpTelemetryEnabled": True,
            "InpTelemetryUseCommonFiles": True,
            "InpTelemetryCsvPath": common_telemetry_path,
            "InpSummaryCsvPath": common_summary_path,
        }
        set_payload = mt5.materialize_tester_set_file(params, set_path, generated_by="stage_pipelines.stage337.materialize_common_files_and_run_argmax_parity_probe")
        ini_payload = mt5.materialize_tester_ini_file(
            mt5.TesterMaterializationConfig(
                expert=mt5.EA_EXPERT_PATH,
                symbol="US100",
                period="M5",
                model=4,
                deposit=500.0,
                leverage="1:100",
                shutdown_terminal=1,
                from_date=args.from_date,
                to_date=args.to_date,
                report=report_name,
            ),
            ini_path,
            set_file_path=Path(set_name),
        )
        attempts.append(
            {
                **attempt,
                "feature_local_path": rel(local_features),
                "model_local_path": rel(local_model),
                "expected_probability_tape_path": rel(expected_tape),
                "feature_common_path": common_feature_path,
                "model_common_path": common_model_path,
                "common_telemetry_path": common_telemetry_path,
                "common_summary_path": common_summary_path,
                "set_path": rel(set_path),
                "ini_path": rel(ini_path),
                "set_name": set_name,
                "ini_name": ini_name,
                "report_name": report_name,
                "from_date": args.from_date,
                "to_date": args.to_date,
                "set_payload": set_payload,
                "ini_payload": ini_payload,
                "feature_export": feature_export,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return attempts, sync_rows, expected_index


def bool_text(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes"}


def compare_runtime(attempt: Mapping[str, Any], common_root: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    telemetry_common = common_root / Path(str(attempt["common_telemetry_path"]))
    summary_common = common_root / Path(str(attempt["common_summary_path"]))
    local_telemetry = TELEMETRY_DIR / Path(str(attempt["common_telemetry_path"])).name
    local_summary = TELEMETRY_DIR / Path(str(attempt["common_summary_path"])).name
    if path_exists(telemetry_common):
        io_path(local_telemetry.parent).mkdir(parents=True, exist_ok=True)
        shutil.copy2(io_path(telemetry_common), io_path(local_telemetry))
    if path_exists(summary_common):
        io_path(local_summary.parent).mkdir(parents=True, exist_ok=True)
        shutil.copy2(io_path(summary_common), io_path(local_summary))
    if not path_exists(local_telemetry):
        return (
            {
                "attempt_name": attempt["attempt_name"],
                "probe_id": attempt["probe_id"],
                "model_id": attempt["model_id"],
                "runtime_status": "blocked_telemetry_missing",
                "telemetry_cycle_rows": 0,
                "ready_model_rows": 0,
                "matched_rows": 0,
                "expected_missing_rows": 0,
                "probability_mismatch_rows": 0,
                "decision_mismatch_rows": 0,
                "max_abs_probability_diff": "",
                "first_ready_bar_time": "",
                "last_ready_bar_time": "",
                "comparison_status": "blocked_telemetry_missing",
                "common_telemetry_path": attempt["common_telemetry_path"],
                "local_telemetry_path": rel(local_telemetry),
                "local_summary_path": rel(local_summary) if path_exists(local_summary) else "",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            [],
        )
    telemetry = pd.read_csv(io_path(local_telemetry))
    cycles = telemetry.loc[telemetry["record_type"].astype(str).eq("cycle")].copy()
    ready = cycles.loc[cycles["feature_ready"].map(bool_text) & cycles["model_ok"].map(bool_text)].copy()
    expected = pd.read_csv(io_path(ROOT / str(attempt["expected_probability_tape_path"])))
    expected_by_time = expected.set_index("bar_time")
    diff_rows: list[dict[str, Any]] = []
    max_abs = 0.0
    probability_mismatch = 0
    decision_mismatch = 0
    expected_missing = 0
    matched = 0
    tolerance = 1e-5
    for row in ready.to_dict("records"):
        bar_time = str(row.get("bar_time", ""))
        if bar_time not in expected_by_time.index:
            expected_missing += 1
            diff_rows.append(
                {
                    "attempt_name": attempt["attempt_name"],
                    "bar_time": bar_time,
                    "expected_found": "false",
                    "comparison_status": "expected_missing",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            continue
        exp = expected_by_time.loc[bar_time]
        if isinstance(exp, pd.DataFrame):
            exp = exp.iloc[0]
        diffs = {
            "p_short": abs(float(row["p_short"]) - float(exp["p_short"])),
            "p_flat": abs(float(row["p_flat"]) - float(exp["p_flat"])),
            "p_long": abs(float(row["p_long"]) - float(exp["p_long"])),
        }
        row_max = max(diffs.values())
        max_abs = max(max_abs, row_max)
        prob_ok = row_max <= tolerance
        decision_ok = str(row.get("decision", "")) == str(exp["decision"])
        probability_mismatch += 0 if prob_ok else 1
        decision_mismatch += 0 if decision_ok else 1
        matched += 1 if prob_ok and decision_ok else 0
        diff_rows.append(
            {
                "attempt_name": attempt["attempt_name"],
                "bar_time": bar_time,
                "expected_found": "true",
                "probability_match": str(prob_ok).lower(),
                "decision_match": str(decision_ok).lower(),
                "mt5_p_short": row["p_short"],
                "expected_p_short": exp["p_short"],
                "abs_diff_p_short": diffs["p_short"],
                "mt5_p_flat": row["p_flat"],
                "expected_p_flat": exp["p_flat"],
                "abs_diff_p_flat": diffs["p_flat"],
                "mt5_p_long": row["p_long"],
                "expected_p_long": exp["p_long"],
                "abs_diff_p_long": diffs["p_long"],
                "mt5_decision": row.get("decision", ""),
                "expected_decision": exp["decision"],
                "comparison_status": "matched" if prob_ok and decision_ok else "mismatch",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    summary_status = "matched" if len(ready) > 0 and expected_missing == 0 and probability_mismatch == 0 and decision_mismatch == 0 else "mismatch_or_incomplete"
    summary_row = {
        "attempt_name": attempt["attempt_name"],
        "probe_id": attempt["probe_id"],
        "model_id": attempt["model_id"],
        "runtime_status": "completed" if len(ready) > 0 else "blocked_no_ready_rows",
        "telemetry_cycle_rows": int(len(cycles)),
        "ready_model_rows": int(len(ready)),
        "matched_rows": int(matched),
        "expected_missing_rows": int(expected_missing),
        "probability_mismatch_rows": int(probability_mismatch),
        "decision_mismatch_rows": int(decision_mismatch),
        "max_abs_probability_diff": max_abs if len(ready) else "",
        "first_ready_bar_time": str(ready["bar_time"].iloc[0]) if len(ready) else "",
        "last_ready_bar_time": str(ready["bar_time"].iloc[-1]) if len(ready) else "",
        "comparison_status": summary_status,
        "common_telemetry_path": attempt["common_telemetry_path"],
        "local_telemetry_path": rel(local_telemetry),
        "local_summary_path": rel(local_summary) if path_exists(local_summary) else "",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    if path_exists(local_summary):
        summary = pd.read_csv(io_path(local_summary))
        if not summary.empty:
            last = summary.iloc[-1].to_dict()
            for key in ("feature_ready_count", "model_ok_count", "long_count", "short_count", "flat_count", "order_attempt_count", "order_fill_count"):
                summary_row[key] = last.get(key, "")
    return summary_row, diff_rows


def run_attempts(args: argparse.Namespace, attempts: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    execution_results: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []
    diff_rows: list[dict[str, Any]] = []
    if args.materialize_only:
        for attempt in attempts:
            summary_rows.append(
                {
                    "attempt_name": attempt["attempt_name"],
                    "probe_id": attempt["probe_id"],
                    "model_id": attempt["model_id"],
                    "tester_status": "materialize_only",
                    "runtime_status": "not_run",
                    "comparison_status": "not_run",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
        return execution_results, summary_rows, diff_rows
    common_root = Path(args.common_files_root)
    tester_profile_root = Path(args.tester_profile_root)
    for attempt in attempts:
        try:
            result = mt5.run_mt5_tester(
                Path(args.terminal_path),
                ROOT / str(attempt["ini_path"]),
                set_path=ROOT / str(attempt["set_path"]),
                tester_profile_set_path=tester_profile_root / str(attempt["set_name"]),
                tester_profile_ini_path=tester_profile_root / str(attempt["ini_name"]),
                timeout_seconds=args.timeout_seconds,
            )
        except subprocess.TimeoutExpired as exc:
            result = {
                "status": "blocked",
                "command": exc.cmd,
                "returncode": None,
                "stdout": (exc.stdout or "")[-2000:] if isinstance(exc.stdout, str) else "",
                "stderr": (exc.stderr or "")[-2000:] if isinstance(exc.stderr, str) else "",
                "blocker": "terminal_timeout",
            }
        wait = mt5.wait_for_mt5_runtime_outputs(common_root, attempt, timeout_seconds=args.wait_timeout_seconds, poll_seconds=2.0)
        summary, diffs = compare_runtime(attempt, common_root)
        summary["tester_status"] = result.get("status", "")
        summary["returncode"] = result.get("returncode", "")
        summary["blocker"] = result.get("blocker", "")
        execution_results.append({"attempt_name": attempt["attempt_name"], "tester": result, "runtime_wait": wait})
        summary_rows.append(summary)
        diff_rows.extend(diffs)
    return execution_results, summary_rows, diff_rows


def identity_rows(paths: Sequence[tuple[str, str, Path, str]]) -> list[dict[str, Any]]:
    rows = []
    for artifact_id, artifact_type, path, role in paths:
        exists = path_exists(path)
        rows.append(
            {
                "artifact_id": artifact_id,
                "artifact_type": artifact_type,
                "path": rel(path),
                "exists": str(exists).lower(),
                "sha256": sha256(path) if exists and io_path(path).is_file() else "",
                "role": role,
                "status": "present" if exists else "missing",
                "effect": "identity evidence(정체성 근거)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_gates(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    ek_failed = sum(1 for row in read_csv(EK_GATES) if row.get("status") != "passed")
    ek_final = read_json(EK_FINAL)
    gates = [
        ("input_presence", final["missing_inputs"] == 0, final["missing_inputs"], "0", "EL 입력이 있어야 한다."),
        ("parent_ek_gates_passed", ek_failed == 0, ek_failed, "0", "부모 EK 게이트가 통과해야 한다."),
        ("parent_next_action_matches", ek_final.get("next_action") == RUN_ID, ek_final.get("next_action", ""), RUN_ID, "라우팅이 EL로 이어져야 한다."),
        ("common_files_synced", final["common_sync_failed_rows"] == 0 and final["common_sync_rows"] >= 2, f"failed={final['common_sync_failed_rows']};rows={final['common_sync_rows']}", "failed=0;rows>=2", "Common Files 인계가 성공해야 한다."),
        ("attempt_package_ready", final["attempt_rows"] >= 1, final["attempt_rows"], ">=1", "실행 시도 패키지가 있어야 한다."),
        ("terminal_process_clear_at_start", final["terminal_process_status"] == "no_terminal64_process", final["terminal_process_status"], "no_terminal64_process", "실행 전 기존 terminal64 프로세스가 없어야 한다."),
        ("runtime_probe_attempted", final["materialize_only"] == "true" or final["tester_attempt_rows"] >= 1, f"materialize_only={final['materialize_only']};tester_attempts={final['tester_attempt_rows']}", "materialize_only or attempts>=1", "터미널 탐침을 시도해야 한다."),
        ("telemetry_ready_or_blocker_named", final["ready_model_rows"] > 0 or final["blocked_attempt_rows"] > 0, f"ready={final['ready_model_rows']};blocked={final['blocked_attempt_rows']}", "ready>0 or blocker>0", "텔레메트리 준비 또는 차단 사유가 있어야 한다."),
        ("no_forbidden_claim", final["forward_passed"] == "not_claimed" and final["runtime_authority"] == "not_claimed", f"forward={final['forward_passed']};authority={final['runtime_authority']}", "not_claimed;not_claimed", "런타임 탐침을 운영 권위로 과장하지 않는다."),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": "passed" if passed else "failed",
            "observed": observed,
            "expected": expected,
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, passed, observed, expected, effect in gates
    ]


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337EL Argmax Runtime Parity Probe(런타임 동등성 탐침)

## Conclusion(결론)

run337EL(337EL 실행)는 argmax probe mode(argmax 탐침 모드)를 Common Files(공통 파일) 인계와 MT5 Strategy Tester(MT5 전략 테스터) 실행으로 좁게 확인했다.

Action(행동): feature CSV(피처 CSV), ONNX(온엑스), set/ini(설정/초기화 파일), expected probability tape(예상 확률 테이프)를 만들고 터미널 탐침을 시도했다.

Effect(효과): 이 결과는 runtime parity(런타임 동등성) 탐침 근거일 뿐이며 Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.

## Result(결과)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- attempt_rows(시도 행): `{final['attempt_rows']}`
- tester_attempt_rows(테스터 시도 행): `{final['tester_attempt_rows']}`
- ready_model_rows(준비 모델 행): `{final['ready_model_rows']}`
- matched_rows(일치 행): `{final['matched_rows']}`
- probability_mismatch_rows(확률 불일치 행): `{final['probability_mismatch_rows']}`
- decision_mismatch_rows(결정 불일치 행): `{final['decision_mismatch_rows']}`
- blocked_attempt_rows(차단 시도 행): `{final['blocked_attempt_rows']}`
- gates_passed(게이트 통과): `{final['passed_gates']}/{final['gate_rows']}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337EL

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- decision(결정): `{final['decision']}`
- judgment(판정): `{final['judgment']}`
- effect(효과): argmax runtime parity probe(argmax 런타임 동등성 탐침)를 시도했고, 다음 실행에서 리뷰/확장/수리 여부를 판단한다.
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(EXECUTION_SUMMARY)}`, `{rel(RUNTIME_DIFF)}`, `{rel(EXECUTION_RESULT)}`
- next_action(다음 행동): `{final['next_action']}`
- Forward/Goal(전진/목표): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(DECISION_DOC, text)


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = re.sub(r"^current_run_id: .*$", f"current_run_id: {final['next_action']}", workspace_text, count=1, flags=re.MULTILINE)
    focus_entry = (
        "- >-\n"
        f"  Stage337 run337EL focus complete: argmax runtime parity probe(argmax 런타임 동등성 탐침)를 시도했고 ready_model_rows(준비 모델 행) "
        f"`{final['ready_model_rows']}`, matched_rows(일치 행) `{final['matched_rows']}`를 기록했다. Effect(효과): 다음 실행에서 리뷰/확장/수리를 결정한다."
    )
    workspace_text = prepend_once(workspace_text, "current_focus:", focus_entry, "Stage337 run337EL focus complete")
    artifacts.append(write_text_preserving(WORKSPACE_STATE, workspace_text, workspace_bom))

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    for field_name, value in {
        "current_run": f"`{final['next_action']}`",
        "status": f"`{final['status']}`",
        "decision": f"`{final['decision']}`",
        "latest_completed_run": f"`{RUN_ID}`",
        "next_action": f"`{final['next_action']}`",
        "claim_boundary": f"`{CLAIM_BOUNDARY}`",
    }.items():
        current_text = replace_bullet_value(current_text, field_name, value)
    section = f"""
## Stage337 run337EL(337EL 실행) - {TODAY}

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): Common Files 인계와 argmax runtime parity probe(argmax 런타임 동등성 탐침)를 시도했다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    marker = "## Stage337 run337EK("
    if "## Stage337 run337EL(337EL 실행)" not in current_text:
        current_text = current_text.replace(marker, section + "\n" + marker, 1) if marker in current_text else current_text.rstrip() + "\n\n" + section
    artifacts.append(write_text_preserving(CURRENT_STATE, current_text, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{final['next_action']}`
- frozen_subject(고정 대상): `cp322A_cp321b_exact_replay_control_surface`
- exact_cp322a_forward_handoff(정확 cp322A 전진 인계): `not_feasible_under_frozen_rules`
- preserved_status(보존 상태): `research_artifact_only`
- rebuild_status(재구축 상태): `{final['status']}`
- argmax_runtime_probe(argmax 런타임 탐침): `attempted`
- ready_model_rows(준비 모델 행): `{final['ready_model_rows']}`
- matched_rows(일치 행): `{final['matched_rows']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): runtime parity review/expansion/repair(런타임 동등성 리뷰/확장/수리)로 진행한다.
"""
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_entry = (
        f"- {TODAY}: run337EL(337EL 실행) attempted argmax runtime parity probe(argmax 런타임 동등성 탐침). "
        f"Status(상태) `{final['status']}`. Forward/Goal(전진/목표)은 주장하지 않음."
    )
    artifacts.append(write_text_preserving(STAGE_BRIEF, append_once(stage_text, stage_entry, "run337EL(337EL 실행) attempted argmax"), stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_entry = f"- {TODAY}: Stage337 run337EL attempted argmax runtime parity probe and opened `{final['next_action']}` without Forward/Goal claims."
    artifacts.append(write_text_preserving(CHANGELOG, append_once(changelog_text, changelog_entry, "Stage337 run337EL attempted argmax"), changelog_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path], final: Mapping[str, Any]) -> list[Path]:
    generated = now_utc()
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "argmax_runtime_parity_probe_without_db",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"ready={final['ready_model_rows']};matched={final['matched_rows']};blocked={final['blocked_attempt_rows']};next={final['next_action']};goal_achieve_not_claimed.",
        "family": "runtime_parity_backtest_forensics_result_judgment",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__argmax_runtime_parity_probe",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "argmax_runtime_parity_probe",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "runtime_parity_probe_no_selection",
        "tier_scope": "tier_a_probe",
        "kpi_scope": "probability_decision_parity_not_profitability",
        "scoreboard_lane": "runtime_parity_result_judgment",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"ready={final['ready_model_rows']};matched={final['matched_rows']};prob_mismatch={final['probability_mismatch_rows']};decision_mismatch={final['decision_mismatch_rows']}",
        "guardrail_kpi": "no_selection;no_forward;runtime_authority_not_claimed",
        "external_verification_status": "mt5_strategy_tester_attempted",
        "notes": f"decision={final['decision']};next={final['next_action']}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__argmax_runtime_parity_probe",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "runtime_parity_backtest_forensics_result_judgment",
        "evidence_scope": "Common Files handoff, MT5 tester attempt, telemetry comparison",
        "kpi_scope": "runtime_probability_decision_parity",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={final['next_action']};goal_achieve_not_claimed",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__argmax_runtime_parity_probe",
        "family": "runtime_parity_backtest_forensics_result_judgment",
        "question": "does the argmax probe mode reproduce Python proxy meaning in MT5",
        "metric_scope": "telemetry_probability_decision_diff",
        "primary_artifact": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "next_action": final["next_action"],
    }
    artifacts = [
        upsert_csv(RUN_REGISTRY, "run_id", run_row),
        upsert_csv(ALPHA_LEDGER, "ledger_row_id", alpha_row),
        upsert_csv(STAGE_LEDGER, "ledger_row_id", stage_row),
    ]
    artifact_columns: list[str] = []
    artifact_rows: list[dict[str, str]] = []
    if path_exists(ARTIFACT_REGISTRY):
        with io_path(ARTIFACT_REGISTRY).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            artifact_columns = list(reader.fieldnames or [])
            artifact_rows = [dict(row) for row in reader]
    if not artifact_columns:
        artifact_columns = ["artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes", "artifact_path", "claim_boundary"]
    new_rows = []
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
    artifact_rows = [row for row in artifact_rows if row.get("artifact_id") not in keys and row.get("run_id") != RUN_ID]
    artifact_rows.extend(new_rows)
    artifacts.append(write_csv(ARTIFACT_REGISTRY, artifact_columns, artifact_rows))
    return artifacts


def main() -> int:
    args = parse_args()
    for directory in (RUN_DIR, MT5_DIR, SET_DIR, INI_DIR, REPORT_COPY_DIR, MODEL_DIR, FEATURE_DIR, EXPECTED_DIR, TELEMETRY_DIR):
        io_path(directory).mkdir(parents=True, exist_ok=True)
    missing = fail_if_missing(INPUT_FILES)
    if missing:
        print(json.dumps({"run_id": RUN_ID, "status": "blocked_missing_inputs", "missing": [rel(path) for path in missing]}, ensure_ascii=False, indent=2))
        return 1
    process_audit = terminal_process_audit()
    write_json(TERMINAL_PROCESS_AUDIT, process_audit)
    attempts, sync_rows, expected_index = materialize_attempts(args)
    write_local_csv(ATTEMPT_PACKAGE, ATTEMPT_COLUMNS, attempts)
    write_local_csv(COMMON_SYNC, SYNC_COLUMNS, sync_rows)
    write_local_csv(EXPECTED_TAPE_INDEX, EXPECTED_INDEX_COLUMNS, expected_index)
    execution_results, summary_rows, diff_rows = run_attempts(args, attempts)
    write_json(EXECUTION_RESULT, {"run_id": RUN_ID, "execution_results": execution_results})
    write_local_csv(EXECUTION_SUMMARY, SUMMARY_COLUMNS, summary_rows)
    write_local_csv(RUNTIME_DIFF, DIFF_COLUMNS, diff_rows)
    identity = identity_rows(
        [
            ("terminal64", "executable", Path(args.terminal_path), "MT5 terminal identity(MT5 터미널 정체성)"),
            ("runtime_ea_source", "mq5", ROOT / mt5.EA_SOURCE_PATH, "EA source(EA 원천)"),
            ("runtime_ea_binary", "ex5", ROOT / "foundation" / "mt5" / "ObsidianPrimeV2_RuntimeProbeEA.ex5", "EA binary(EA 바이너리)"),
            ("attempt_package", "csv", ATTEMPT_PACKAGE, "attempt package(시도 패키지)"),
            ("execution_summary", "csv", EXECUTION_SUMMARY, "execution summary(실행 요약)"),
        ]
    )
    write_local_csv(RUNTIME_IDENTITY, IDENTITY_COLUMNS, identity)
    write_json(
        TESTER_SETTINGS_IDENTITY,
        {
            "run_id": RUN_ID,
            "terminal_path": args.terminal_path,
            "common_files_root": args.common_files_root,
            "tester_profile_root": args.tester_profile_root,
            "from_date": args.from_date,
            "to_date": args.to_date,
            "attempt_limit": args.attempt_limit,
            "materialize_only": args.materialize_only,
        },
    )
    ready_model_rows = sum(int(row.get("ready_model_rows") or 0) for row in summary_rows)
    matched_rows = sum(int(row.get("matched_rows") or 0) for row in summary_rows)
    probability_mismatch_rows = sum(int(row.get("probability_mismatch_rows") or 0) for row in summary_rows)
    decision_mismatch_rows = sum(int(row.get("decision_mismatch_rows") or 0) for row in summary_rows)
    blocked_attempt_rows = sum(1 for row in summary_rows if str(row.get("runtime_status", "")).startswith("blocked") or str(row.get("comparison_status", "")).startswith("blocked"))
    status = STATUS_EXECUTED if ready_model_rows > 0 else STATUS_BLOCKED
    judgment = JUDGMENT_EXECUTED if ready_model_rows > 0 else JUDGMENT_BLOCKED
    decision = DECISION_EXECUTED if ready_model_rows > 0 else DECISION_BLOCKED
    final: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": status,
        "judgment": judgment,
        "decision": decision,
        "next_action": NEXT_RUN_ID,
        "ek_next_action": read_json(EK_FINAL).get("next_action", ""),
        "ek_failed_gate_rows": sum(1 for row in read_csv(EK_GATES) if row.get("status") != "passed"),
        "missing_inputs": len(missing),
        "materialize_only": str(args.materialize_only).lower(),
        "terminal_process_status": process_audit["status"],
        "attempt_rows": len(attempts),
        "common_sync_rows": len(sync_rows),
        "common_sync_failed_rows": sum(1 for row in sync_rows if row["status"] != "copied"),
        "expected_probability_tape_rows": sum(int(row["rows"]) for row in expected_index),
        "tester_attempt_rows": len(execution_results),
        "summary_rows": len(summary_rows),
        "diff_rows": len(diff_rows),
        "ready_model_rows": ready_model_rows,
        "matched_rows": matched_rows,
        "probability_mismatch_rows": probability_mismatch_rows,
        "decision_mismatch_rows": decision_mismatch_rows,
        "blocked_attempt_rows": blocked_attempt_rows,
        "model_training": "not_run",
        "threshold_tuning": "not_run",
        "lot_optimization": "not_run",
        "candidate_selection": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    gates = build_gates(final)
    final["gate_rows"] = len(gates)
    final["passed_gates"] = sum(1 for row in gates if row["status"] == "passed")
    final["failed_gates"] = [row["gate_id"] for row in gates if row["status"] != "passed"]
    write_csv(REQUIRED_GATE_AUDIT, GATE_COLUMNS, gates)
    write_json(FINAL_DECISION, final)
    write_json(RUN_MANIFEST, {"run_id": RUN_ID, "parent_run_id": PARENT_RUN_ID, "inputs": [rel(path) for path in INPUT_FILES], "outputs": [rel(path) for path in OUTPUT_FILES], "claim_boundary": CLAIM_BOUNDARY})
    receipts = [
        write_json(DATA_RECEIPT, {"run_id": RUN_ID, "status": "completed", "attempt_rows": len(attempts), "claim_boundary": CLAIM_BOUNDARY}),
        write_json(MODEL_RECEIPT, {"run_id": RUN_ID, "model_training": "not_run", "expected_probability_tape_rows": final["expected_probability_tape_rows"], "claim_boundary": CLAIM_BOUNDARY}),
        write_json(RUNTIME_RECEIPT, {"run_id": RUN_ID, "runtime_probe_execution": "attempted", "ready_model_rows": ready_model_rows, "claim_boundary": CLAIM_BOUNDARY}),
        write_json(FORENSICS_RECEIPT, {"run_id": RUN_ID, "tester_settings": rel(TESTER_SETTINGS_IDENTITY), "execution_result": rel(EXECUTION_RESULT), "claim_boundary": CLAIM_BOUNDARY}),
        write_json(JUDGMENT_RECEIPT, {"run_id": RUN_ID, "judgment_label": "runtime_probe" if ready_model_rows > 0 else "blocked", "claim_boundary": CLAIM_BOUNDARY}),
        write_json(LINEAGE_RECEIPT, {"run_id": RUN_ID, "parent_run_id": PARENT_RUN_ID, "inputs": [rel(path) for path in INPUT_FILES], "outputs": [rel(path) for path in OUTPUT_FILES], "claim_boundary": CLAIM_BOUNDARY}),
    ]
    tracked = [write_report(final), write_decision_doc(final)]
    tracked.extend(update_docs(final))
    tracked.extend(update_registers([*OUTPUT_FILES, *receipts, *tracked], final))
    if final["failed_gates"]:
        print(json.dumps({"run_id": RUN_ID, "status": "gate_failed", "failed_gates": final["failed_gates"], "ready_model_rows": ready_model_rows}, ensure_ascii=False, indent=2))
        return 1
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": status,
                "attempt_rows": len(attempts),
                "ready_model_rows": ready_model_rows,
                "matched_rows": matched_rows,
                "probability_mismatch_rows": probability_mismatch_rows,
                "decision_mismatch_rows": decision_mismatch_rows,
                "next_action": NEXT_RUN_ID,
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
