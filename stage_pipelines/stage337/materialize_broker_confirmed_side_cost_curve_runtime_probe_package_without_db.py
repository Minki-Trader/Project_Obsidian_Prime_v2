from __future__ import annotations

import csv
import json
import math
import re
import shutil
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Mapping, Sequence

import joblib
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import json_ready, path_exists  # noqa: E402
from foundation.models.baseline_training import LABEL_ORDER  # noqa: E402
from foundation.models.onnx_bridge import ordered_sklearn_probabilities  # noqa: E402
from foundation.mt5 import runtime_support as mt5  # noqa: E402
from stage_pipelines.stage337 import review_broker_confirmed_side_cost_curve_training_without_db as ez  # noqa: E402


aw = ez.aw
ey = ez.ey

TODAY = "2026-05-31"
STAGE_ID = ez.STAGE_ID
RUN_NUMBER = "run337FA"
RUN_ID = "run337FA_materialize_broker_confirmed_side_cost_curve_runtime_probe_package_without_db_v1"
PARENT_RUN_ID = ez.RUN_ID
NEXT_RUN_ID = "run337FB_execute_broker_confirmed_side_cost_curve_mt5_runtime_probe_without_db_v1"
STATUS = "completed_stage337FA_side_cost_curve_runtime_probe_package_materialized_no_mt5_execution"
JUDGMENT = "runtime_probe_package_ready_for_mt5_attempt_proxy_diff_required_no_selection"
DECISION = "stage337FA_open_run337FB_execute_side_cost_curve_mt5_runtime_probe_without_db"
CLAIM_BOUNDARY = (
    "research_development_only_stage337FA_broker_confirmed_side_cost_curve_runtime_probe_package_without_db_"
    "no_new_training_no_threshold_tuning_no_lot_optimization_no_operating_selection_no_mt5_execution_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ez.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MT5_DIR = RUN_DIR / "mt5"
SET_DIR = MT5_DIR / "sets"
INI_DIR = MT5_DIR / "inis"
MODEL_COPY_DIR = RUN_DIR / "models"
FEATURE_DIR = RUN_DIR / "feature_matrices"
EXPECTED_DIR = RUN_DIR / "expected_probability_tapes"
REVIEWS_DIR = ez.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337FA_broker_confirmed_side_cost_curve_runtime_probe_package.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337FA_broker_confirmed_side_cost_curve_runtime_probe_package.md"
SELECTED_STATUS = ez.SELECTED_STATUS
STAGE_BRIEF = ez.STAGE_BRIEF
WORKSPACE_STATE = ez.WORKSPACE_STATE
CURRENT_STATE = ez.CURRENT_STATE
CHANGELOG = ez.CHANGELOG
RUN_REGISTRY = ez.RUN_REGISTRY
ALPHA_LEDGER = ez.ALPHA_LEDGER
ARTIFACT_REGISTRY = ez.ARTIFACT_REGISTRY
STAGE_LEDGER = ez.STAGE_LEDGER

EZ_FINAL = ez.FINAL_DECISION
EZ_GATES = ez.GATE_AUDIT
EZ_QUEUE = ez.FA_QUEUE
EZ_RUNTIME_QUEUE = ez.RUNTIME_PROBE_CANDIDATE_QUEUE
EZ_PACKAGE_CONTRACT = ez.RUNTIME_PROBE_PACKAGE_CONTRACT
EZ_PROXY_REVIEW = ez.PROXY_CLUE_REVIEW
EZ_ONNX_READINESS = ez.ONNX_READINESS_REVIEW

EY_FRAME = ey.EW_FRAME
EY_FEATURE_SCHEMA = ey.FEATURE_SCHEMA
EY_MODEL_MANIFEST = ey.TRAINED_MODEL_MANIFEST
EY_ONNX_PARITY = ey.ONNX_PARITY

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
EA_SOURCE = ROOT / "foundation" / "mt5" / "ObsidianPrimeV2_RuntimeProbeEA.mq5"
EA_BINARY = ROOT / "foundation" / "mt5" / "ObsidianPrimeV2_RuntimeProbeEA.ex5"
EA_INCLUDE_DIR = ROOT / "foundation" / "mt5" / "include" / "ObsidianPrime"

COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage337/{RUN_NUMBER}_side_cost_curve_runtime_probe"
COMMON_FEATURE_DIR = f"{COMMON_ROOT}/features"
COMMON_MODEL_DIR = f"{COMMON_ROOT}/models"
COMMON_TELEMETRY_DIR = f"{COMMON_ROOT}/telemetry"

FEATURE_MATRIX = FEATURE_DIR / "side_cost_curve_inner_holdout_features.csv"
FEATURE_MATRIX_MANIFEST = RUN_DIR / "runtime_feature_matrix_manifest.csv"
EXPECTED_PROBABILITY_TAPE = EXPECTED_DIR / "side_cost_curve_expected_probability_tape.csv"
EXPECTED_PROBABILITY_INDEX = RUN_DIR / "expected_probability_tape_index.csv"
MODEL_HANDOFF_MANIFEST = RUN_DIR / "model_handoff_manifest.csv"
COMMON_FILES_SYNC = RUN_DIR / "common_files_sync.csv"
TESTER_SET_MANIFEST = RUN_DIR / "tester_set_manifest.csv"
TESTER_INI_MANIFEST = RUN_DIR / "tester_ini_manifest.csv"
RUNTIME_PROBE_ATTEMPT_PACKAGE = RUN_DIR / "runtime_probe_attempt_package.csv"
TESTER_IDENTITY_CONTRACT = RUN_DIR / "tester_identity_contract.csv"
PROXY_MT5_COMPARISON_CONTRACT = RUN_DIR / "proxy_mt5_comparison_contract.csv"
RUNTIME_PARITY_CONTRACT = RUN_DIR / "runtime_parity_contract.csv"
EXECUTION_QUEUE = RUN_DIR / "run337FB_execution_queue.csv"
ROUTING_RECEIPT = RUN_DIR / "routing_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
FORENSICS_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    EZ_FINAL,
    EZ_GATES,
    EZ_QUEUE,
    EZ_RUNTIME_QUEUE,
    EZ_PACKAGE_CONTRACT,
    EZ_PROXY_REVIEW,
    EZ_ONNX_READINESS,
    EY_FRAME,
    EY_FEATURE_SCHEMA,
    EY_MODEL_MANIFEST,
    EY_ONNX_PARITY,
    EA_SOURCE,
    EA_BINARY,
)
OUTPUT_FILES = (
    FEATURE_MATRIX,
    FEATURE_MATRIX_MANIFEST,
    EXPECTED_PROBABILITY_TAPE,
    EXPECTED_PROBABILITY_INDEX,
    MODEL_HANDOFF_MANIFEST,
    COMMON_FILES_SYNC,
    TESTER_SET_MANIFEST,
    TESTER_INI_MANIFEST,
    RUNTIME_PROBE_ATTEMPT_PACKAGE,
    TESTER_IDENTITY_CONTRACT,
    PROXY_MT5_COMPARISON_CONTRACT,
    RUNTIME_PARITY_CONTRACT,
    EXECUTION_QUEUE,
    ROUTING_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    RUNTIME_RECEIPT,
    FORENSICS_RECEIPT,
    PERFORMANCE_RECEIPT,
    JUDGMENT_RECEIPT,
    LINEAGE_RECEIPT,
    GATE_AUDIT,
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

FEATURE_MANIFEST_COLUMNS = (
    "feature_matrix_id",
    "feature_set_id",
    "feature_count",
    "row_count",
    "first_source_time",
    "last_source_time",
    "feature_order_hash",
    "local_path",
    "local_sha256",
    "common_path",
    "common_sha256",
    "timestamp_semantics",
    "effect",
    "claim_boundary",
)
EXPECTED_INDEX_COLUMNS = (
    "expected_tape_id",
    "model_id",
    "task_id",
    "attempt_name",
    "row_count",
    "first_source_time",
    "last_source_time",
    "path",
    "sha256",
    "decision_mode",
    "allowed_use",
    "forbidden_use",
    "claim_boundary",
)
MODEL_HANDOFF_COLUMNS = (
    "attempt_name",
    "model_id",
    "task_id",
    "probe_priority",
    "source_model_path",
    "source_model_sha256",
    "local_model_path",
    "local_model_sha256",
    "source_onnx_path",
    "source_onnx_sha256",
    "local_onnx_path",
    "local_onnx_sha256",
    "common_onnx_path",
    "common_onnx_sha256",
    "feature_order_hash",
    "class_order_json",
    "handoff_status",
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
SET_COLUMNS = (
    "attempt_name",
    "model_id",
    "set_path",
    "set_sha256",
    "parameter_count",
    "decision_mode",
    "allow_trading",
    "fixed_lot",
    "max_hold_bars",
    "no_optimization_rule",
    "claim_boundary",
)
INI_COLUMNS = (
    "attempt_name",
    "model_id",
    "ini_path",
    "ini_sha256",
    "expert",
    "symbol",
    "period",
    "model",
    "deposit",
    "leverage",
    "from_date",
    "to_date",
    "report",
    "claim_boundary",
)
ATTEMPT_COLUMNS = (
    "attempt_name",
    "next_run_id",
    "probe_priority",
    "model_id",
    "task_id",
    "feature_set_id",
    "feature_count",
    "feature_order_hash",
    "feature_local_path",
    "feature_common_path",
    "model_local_path",
    "model_common_path",
    "expected_tape_path",
    "common_telemetry_path",
    "common_summary_path",
    "set_path",
    "set_name",
    "ini_path",
    "ini_name",
    "report_name",
    "from_date",
    "to_date",
    "decision_mode",
    "short_threshold",
    "long_threshold",
    "min_margin",
    "fixed_lot",
    "max_hold_bars",
    "known_proxy_runtime_difference",
    "forbidden_action",
    "effect",
    "claim_boundary",
)
CONTRACT_COLUMNS = (
    "contract_id",
    "subject",
    "requirement",
    "evidence_path",
    "known_difference",
    "blocked_if_missing",
    "forbidden_action",
    "effect",
    "claim_boundary",
)
QUEUE_COLUMNS = (
    "queue_id",
    "next_run_id",
    "priority",
    "task",
    "required_inputs",
    "required_outputs",
    "blocked_if_missing",
    "forbidden_action",
    "effect",
    "claim_boundary",
)
GATE_COLUMNS = (
    "gate_id",
    "status",
    "evidence_path",
    "observed",
    "expected",
    "effect",
    "claim_boundary",
)
EXPECTED_COLUMNS = (
    "attempt_name",
    "model_id",
    "task_id",
    "bar_time",
    "source_time",
    "feature_input_hash",
    "p_short",
    "p_flat",
    "p_long",
    "decision_class",
    "decision_label",
    "allowed_use",
    "forbidden_use",
    "claim_boundary",
)


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return aw.rel(path)


def read_csv(path: Path) -> list[dict[str, str]]:
    return aw.read_csv(path)


def read_json(path: Path) -> dict[str, Any]:
    return aw.read_json(path)


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    return aw.write_csv(path, columns, rows)


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> Path:
    aw.io_path(path.parent).mkdir(parents=True, exist_ok=True)
    aw.io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def fail_if_missing(paths: Sequence[Path]) -> list[Path]:
    return [path for path in paths if not path_exists(path)]


def repo_path(value: str) -> Path:
    path = Path(str(value))
    return path if path.is_absolute() else ROOT / path


def as_float(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.0
    return number if math.isfinite(number) else 0.0


def as_int(value: Any) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def csv_timestamp(value: Any) -> str:
    return pd.Timestamp(value).tz_convert("UTC").strftime("%Y.%m.%d %H:%M:%S")


def format_feature_value(value: Any) -> str:
    number = np.float32(float(value)).item()
    if not math.isfinite(float(number)):
        raise ValueError("non-finite feature value")
    return format(float(number), ".9g")


def fnv1a_mql_hash(line: str) -> str:
    digest = 1469598103934665603
    mask = 0xFFFFFFFFFFFFFFFF
    for char in line:
        digest = ((digest ^ ord(char)) * 1099511628211) & mask
    return f"{digest:X}"


def copy_file(source: Path, target: Path, sync_id: str, effect: str) -> dict[str, Any]:
    aw.io_path(target.parent).mkdir(parents=True, exist_ok=True)
    shutil.copy2(aw.io_path(source), aw.io_path(target))
    return {
        "sync_id": sync_id,
        "source_path": rel(source) if str(source).startswith(str(ROOT)) else source.as_posix(),
        "target_path": rel(target) if str(target).startswith(str(ROOT)) else target.as_posix(),
        "exists": path_exists(target),
        "sha256": aw.sha256_file(target) if path_exists(target) else "",
        "status": "synced(동기화됨)" if path_exists(target) else "missing(누락)",
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def load_features() -> list[str]:
    schema = read_json(EY_FEATURE_SCHEMA)
    return [str(item) for item in schema.get("features", [])]


def inner_holdout_frame(features: Sequence[str]) -> pd.DataFrame:
    frame = pd.read_parquet(aw.io_path(EY_FRAME)).copy()
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    frame.sort_values(["source_row_id", "timestamp"], inplace=True)
    _inner_train, inner_holdout = ey.split_inner(frame)
    missing = [feature for feature in features if feature not in inner_holdout.columns]
    if missing:
        raise ValueError(f"missing runtime features: {missing}")
    return inner_holdout.reset_index(drop=True)


def materialize_feature_matrix(frame: pd.DataFrame, features: Sequence[str]) -> tuple[pd.DataFrame, list[str], list[dict[str, Any]]]:
    aw.io_path(FEATURE_DIR).mkdir(parents=True, exist_ok=True)
    header = ["timestamp", *features]
    hashes: list[str] = []
    formatted_values: list[list[float]] = []
    with aw.io_path(FEATURE_MATRIX).open("w", encoding="utf-8", newline="") as handle:
        handle.write(",".join(header) + "\n")
        for _, row in frame.iterrows():
            timestamp = csv_timestamp(row["timestamp"])
            value_text = [format_feature_value(row[feature]) for feature in features]
            line = ",".join([timestamp, *value_text])
            handle.write(line + "\n")
            hashes.append(fnv1a_mql_hash(line))
            formatted_values.append([float(item) for item in value_text])
    values = pd.DataFrame(formatted_values, columns=list(features), dtype="float32")
    values.insert(0, "timestamp", [csv_timestamp(value) for value in frame["timestamp"]])
    feature_common = f"{COMMON_FEATURE_DIR}/side_cost_curve_inner_holdout_features.csv"
    sync_rows = [
        copy_file(
            FEATURE_MATRIX,
            DEFAULT_COMMON_FILES / Path(feature_common),
            "common_feature_matrix",
            "feature matrix(피처 행렬)를 Common Files(공용 파일)에 복사해 MT5 EA가 읽을 수 있게 한다.",
        )
    ]
    return values, hashes, sync_rows


def date_bounds(frame: pd.DataFrame) -> tuple[str, str, str, str]:
    first = pd.Timestamp(frame["timestamp"].min()).tz_convert("UTC")
    last = pd.Timestamp(frame["timestamp"].max()).tz_convert("UTC")
    from_date = first.strftime("%Y.%m.%d")
    to_date = (last + timedelta(days=1)).strftime("%Y.%m.%d")
    return first.strftime("%Y.%m.%d %H:%M:%S"), last.strftime("%Y.%m.%d %H:%M:%S"), from_date, to_date


def model_rows_by_id() -> dict[str, dict[str, str]]:
    return {row["model_id"]: row for row in read_csv(EY_MODEL_MANIFEST)}


def queue_rows() -> list[dict[str, str]]:
    return read_csv(EZ_RUNTIME_QUEUE)


def fitted_model(payload: Any) -> Any:
    if isinstance(payload, Mapping) and hasattr(payload.get("model"), "predict_proba"):
        return payload["model"]
    return payload


def materialize_models_and_expected(
    values: pd.DataFrame,
    input_hashes: Sequence[str],
    features: Sequence[str],
    first_time: str,
    last_time: str,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    aw.io_path(MODEL_COPY_DIR).mkdir(parents=True, exist_ok=True)
    aw.io_path(EXPECTED_DIR).mkdir(parents=True, exist_ok=True)
    model_lookup = model_rows_by_id()
    model_handoff: list[dict[str, Any]] = []
    expected_index_rows: list[dict[str, Any]] = []
    expected_rows: list[dict[str, Any]] = []
    set_rows: list[dict[str, Any]] = []
    ini_rows: list[dict[str, Any]] = []
    attempts: list[dict[str, Any]] = []
    sync_rows: list[dict[str, Any]] = []
    feature_common = f"{COMMON_FEATURE_DIR}/side_cost_curve_inner_holdout_features.csv"
    matrix = values.loc[:, features].astype("float32").to_numpy()
    _first_source, _last_source, from_date, to_date = date_bounds(pd.DataFrame({"timestamp": pd.to_datetime(values["timestamp"], format="%Y.%m.%d %H:%M:%S", utc=True)}))

    for index, queue in enumerate(queue_rows()):
        model_id = queue["model_id"]
        model = model_lookup[model_id]
        task_id = model["task_id"]
        attempt_name = f"fa_{model_id}"
        source_joblib = repo_path(model["model_path"])
        source_onnx = repo_path(model["onnx_path"])
        local_joblib = MODEL_COPY_DIR / f"{attempt_name}.joblib"
        local_onnx = MODEL_COPY_DIR / f"{attempt_name}.onnx"
        common_onnx = f"{COMMON_MODEL_DIR}/{attempt_name}.onnx"
        sync_rows.append(
            copy_file(
                source_joblib,
                local_joblib,
                f"local_joblib::{attempt_name}",
                "joblib model(joblib 모델)을 실행 폴더에 복사해 expected tape(예상 테이프)를 재현 가능하게 한다.",
            )
        )
        sync_rows.append(
            copy_file(
                source_onnx,
                local_onnx,
                f"local_onnx::{attempt_name}",
                "ONNX model(온엑스 모델)을 실행 폴더에 복사해 handoff(인계) 계보를 고정한다.",
            )
        )
        sync_rows.append(
            copy_file(
                local_onnx,
                DEFAULT_COMMON_FILES / Path(common_onnx),
                f"common_onnx::{attempt_name}",
                "ONNX model(온엑스 모델)을 Common Files(공용 파일)에 복사해 MT5 EA가 읽을 수 있게 한다.",
            )
        )

        fitted = fitted_model(joblib.load(aw.io_path(local_joblib)))
        probabilities = ordered_sklearn_probabilities(fitted, matrix, LABEL_ORDER)
        predictions = np.asarray(LABEL_ORDER, dtype=int)[np.argmax(probabilities, axis=1)]
        labels = {0: "short", 1: "flat", 2: "long"}
        row_start = len(expected_rows)
        for row_index, timestamp in enumerate(values["timestamp"].tolist()):
            decision_class = int(predictions[row_index])
            expected_rows.append(
                {
                    "attempt_name": attempt_name,
                    "model_id": model_id,
                    "task_id": task_id,
                    "bar_time": timestamp,
                    "source_time": timestamp,
                    "feature_input_hash": input_hashes[row_index],
                    "p_short": float(probabilities[row_index, 0]),
                    "p_flat": float(probabilities[row_index, 1]),
                    "p_long": float(probabilities[row_index, 2]),
                    "decision_class": decision_class,
                    "decision_label": labels[decision_class],
                    "allowed_use": "proxy-vs-MT5 runtime parity comparison(프록시-MT5 런타임 동등성 비교)",
                    "forbidden_use": "MT5 KPI substitute or operating selection(MT5 성과 대체 또는 운영 선택)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
        row_count = len(expected_rows) - row_start

        set_name = f"ObsidianPrimeV2_RuntimeProbeEA_{attempt_name}.set"
        ini_name = f"ObsidianPrimeV2_RuntimeProbeEA_{attempt_name}.ini"
        set_path = SET_DIR / set_name
        ini_path = INI_DIR / ini_name
        report_name = f"Project_Obsidian_Prime_v2_{RUN_ID}_{attempt_name}"
        set_values = {
            "InpRunId": f"{RUN_ID}_{attempt_name}",
            "InpExplorationLabel": "stage337FA_SideCostCurve__MT5RuntimeProbe",
            "InpTierLabel": "Tier A",
            "InpPrimaryActiveTier": "tier_a",
            "InpSplitLabel": "inner_holdout_runtime_probe",
            "InpMainSymbol": "US100",
            "InpTimeframe": 5,
            "InpEnforceM5": True,
            "InpFeatureCsvPath": feature_common,
            "InpFeatureCount": len(features),
            "InpFeatureCsvUseCommonFiles": True,
            "InpFeatureRequireTimestampMatch": True,
            "InpFeatureAllowLatestFallback": False,
            "InpFeatureStrictHeader": True,
            "InpFeatureCsvDelimiter": ",",
            "InpCsvTimestampIsBarClose": True,
            "InpModelPath": common_onnx,
            "InpModelId": model_id,
            "InpModelBackend": "onnx",
            "InpModelUseCommonFiles": True,
            "InpModelUseCpuOnly": True,
            "InpModelNoConversion": False,
            "InpSetOutputShape": True,
            "InpFeatureOrderHash": model["feature_order_hash"],
            "InpFallbackEnabled": False,
            "InpFallbackFeatureCsvPath": feature_common,
            "InpFallbackFeatureCount": len(features),
            "InpFallbackModelPath": common_onnx,
            "InpFallbackModelId": model_id,
            "InpFallbackModelBackend": "onnx",
            "InpFallbackFeatureOrderHash": model["feature_order_hash"],
            "InpShortThreshold": 0.0,
            "InpLongThreshold": 0.0,
            "InpMinMargin": 0.0,
            "InpDecisionMode": "argmax_probe",
            "InpInvertSignal": False,
            "InpFallbackShortThreshold": 0.0,
            "InpFallbackLongThreshold": 0.0,
            "InpFallbackMinMargin": 0.0,
            "InpFallbackDecisionMode": "argmax_probe",
            "InpFallbackInvertSignal": False,
            "InpAllowTrading": True,
            "InpFixedLot": 0.10,
            "InpMagic": 3375000 + index,
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
            "InpTelemetryCsvPath": f"{COMMON_TELEMETRY_DIR}/{attempt_name}_telemetry.csv",
            "InpSummaryCsvPath": f"{COMMON_TELEMETRY_DIR}/{attempt_name}_summary.csv",
        }
        set_payload = mt5.materialize_tester_set_file(set_values, set_path, generated_by=rel(Path(__file__)))
        ini_payload = mt5.materialize_tester_ini_file(
            mt5.TesterMaterializationConfig(
                shutdown_terminal=1,
                from_date=from_date,
                to_date=to_date,
                report=report_name,
            ),
            ini_path,
            set_file_path=Path(set_name),
        )

        model_handoff.append(
            {
                "attempt_name": attempt_name,
                "model_id": model_id,
                "task_id": task_id,
                "probe_priority": queue.get("probe_priority", ""),
                "source_model_path": model["model_path"],
                "source_model_sha256": model["model_sha256"],
                "local_model_path": rel(local_joblib),
                "local_model_sha256": aw.sha256_file(local_joblib),
                "source_onnx_path": model["onnx_path"],
                "source_onnx_sha256": model["onnx_sha256"],
                "local_onnx_path": rel(local_onnx),
                "local_onnx_sha256": aw.sha256_file(local_onnx),
                "common_onnx_path": common_onnx,
                "common_onnx_sha256": aw.sha256_file(DEFAULT_COMMON_FILES / Path(common_onnx)),
                "feature_order_hash": model["feature_order_hash"],
                "class_order_json": model["class_order_json"],
                "handoff_status": "ready_for_mt5_probe(MT5 탐침 준비)",
                "effect": "model, ONNX, and Common Files hashes are connected(모델, ONNX, 공용 파일 해시를 연결)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        expected_index_rows.append(
            {
                "expected_tape_id": f"expected::{attempt_name}",
                "model_id": model_id,
                "task_id": task_id,
                "attempt_name": attempt_name,
                "row_count": row_count,
                "first_source_time": first_time,
                "last_source_time": last_time,
                "path": rel(EXPECTED_PROBABILITY_TAPE),
                "sha256": "written_after_index",
                "decision_mode": "argmax_probe(최대확률 탐침)",
                "allowed_use": "proxy-vs-MT5 diff(프록시-MT5 차이)",
                "forbidden_use": "operating selection(운영 선택)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        set_rows.append(
            {
                "attempt_name": attempt_name,
                "model_id": model_id,
                "set_path": rel(set_path),
                "set_sha256": set_payload["sha256"],
                "parameter_count": set_payload["parameter_count"],
                "decision_mode": "argmax_probe(최대확률 탐침)",
                "allow_trading": True,
                "fixed_lot": 0.10,
                "max_hold_bars": 12,
                "no_optimization_rule": "fixed lot and fixed argmax probe; no threshold tuning(고정 로트와 고정 최대확률 탐침, 임계값 조정 없음)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        tester_values = ini_payload["tester"]
        ini_rows.append(
            {
                "attempt_name": attempt_name,
                "model_id": model_id,
                "ini_path": rel(ini_path),
                "ini_sha256": ini_payload["sha256"],
                "expert": tester_values.get("Expert", ""),
                "symbol": tester_values.get("Symbol", ""),
                "period": tester_values.get("Period", ""),
                "model": tester_values.get("Model", ""),
                "deposit": tester_values.get("Deposit", ""),
                "leverage": tester_values.get("Leverage", ""),
                "from_date": tester_values.get("FromDate", ""),
                "to_date": tester_values.get("ToDate", ""),
                "report": tester_values.get("Report", ""),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        attempts.append(
            {
                "attempt_name": attempt_name,
                "next_run_id": NEXT_RUN_ID,
                "probe_priority": queue.get("probe_priority", ""),
                "model_id": model_id,
                "task_id": task_id,
                "feature_set_id": model.get("feature_set_id", ""),
                "feature_count": len(features),
                "feature_order_hash": model["feature_order_hash"],
                "feature_local_path": rel(FEATURE_MATRIX),
                "feature_common_path": feature_common,
                "model_local_path": rel(local_onnx),
                "model_common_path": common_onnx,
                "expected_tape_path": rel(EXPECTED_PROBABILITY_TAPE),
                "common_telemetry_path": f"{COMMON_TELEMETRY_DIR}/{attempt_name}_telemetry.csv",
                "common_summary_path": f"{COMMON_TELEMETRY_DIR}/{attempt_name}_summary.csv",
                "set_path": rel(set_path),
                "set_name": set_name,
                "ini_path": rel(ini_path),
                "ini_name": ini_name,
                "report_name": report_name,
                "from_date": from_date,
                "to_date": to_date,
                "decision_mode": "argmax_probe",
                "short_threshold": 0.0,
                "long_threshold": 0.0,
                "min_margin": 0.0,
                "fixed_lot": 0.10,
                "max_hold_bars": 12,
                "known_proxy_runtime_difference": "proxy uses independent fwd12 log return; MT5 uses position lifecycle and broker costs(프록시는 독립 12봉 로그수익, MT5는 포지션 생명주기와 브로커 비용)",
                "forbidden_action": "treat attempt priority as selection or promotion(시도 우선순위를 선택이나 승격으로 취급)",
                "effect": "attempt is executable by run337FB without changing model logic(run337FB가 모델 로직 변경 없이 실행 가능)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    write_csv(EXPECTED_PROBABILITY_TAPE, EXPECTED_COLUMNS, expected_rows)
    expected_sha = aw.sha256_file(EXPECTED_PROBABILITY_TAPE)
    for row in expected_index_rows:
        row["sha256"] = expected_sha
    return model_handoff, expected_index_rows, expected_rows, set_rows, ini_rows, attempts, sync_rows


def build_contracts(attempts: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    tester_contract = [
        {
            "contract_id": "tester_identity",
            "subject": "MT5 Strategy Tester(MT5 전략 테스터)",
            "requirement": "US100 M5, Deposit=500, Leverage=1:100, Model=4 real ticks(US100 M5, 예수금 500, 레버리지 1:100, 실제 틱)",
            "evidence_path": rel(TESTER_INI_MANIFEST),
            "known_difference": "none in package; actual broker costs must be read from tester output(패키지상 없음, 실제 브로커 비용은 테스터 출력에서 읽어야 함)",
            "blocked_if_missing": "tester report, settings, trade list(테스터 보고서, 설정, 거래 목록)",
            "forbidden_action": "trust KPI without tester identity(테스터 정체성 없이 성과 신뢰)",
            "effect": "backtest evidence can be audited after execution(실행 후 백테스트 근거 감사 가능)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    proxy_contract = [
        {
            "contract_id": "proxy_mt5_diff",
            "subject": "proxy expected value vs MT5 runtime(프록시 예상값 대 MT5 런타임)",
            "requirement": "compare expected probabilities, input hash, decision, and KPI diff(예상 확률, 입력 해시, 결정, 성과 차이 비교)",
            "evidence_path": rel(EXPECTED_PROBABILITY_TAPE),
            "known_difference": "proxy independent fwd12 return vs MT5 lifecycle execution(프록시 독립 12봉 수익 대 MT5 생명주기 실행)",
            "blocked_if_missing": "runtime telemetry or expected tape(런타임 기록 또는 예상 테이프)",
            "forbidden_action": "use proxy net as MT5 profit(프록시 순값을 MT5 수익으로 사용)",
            "effect": "proxy is converted into a comparison baseline(프록시를 비교 기준으로 바꿈)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    runtime_contract = [
        {
            "contract_id": "runtime_parity_inputs",
            "subject": "feature/model handoff(피처/모델 인계)",
            "requirement": "feature_input_hash and ONNX probabilities must match on overlap(겹치는 구간에서 입력 해시와 ONNX 확률 일치)",
            "evidence_path": f"{rel(FEATURE_MATRIX)};{rel(MODEL_HANDOFF_MANIFEST)}",
            "known_difference": "MT5 reads Common Files; Python reads repo artifacts(MT5는 공용 파일, 파이썬은 저장소 산출물을 읽음)",
            "blocked_if_missing": "Common Files handoff or telemetry(공용 파일 인계 또는 런타임 기록)",
            "forbidden_action": "runtime authority from package only(패키지만으로 런타임 권위 주장)",
            "effect": "run337FB can test runtime parity row by row(run337FB가 행 단위 런타임 동등성을 시험 가능)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    queue = [
        {
            "queue_id": "fb_execute_side_cost_curve_mt5_runtime_probe",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "execute MT5 runtime probe for four side/cost/curve ONNX candidates(4개 방향/비용/곡선 ONNX 후보 MT5 런타임 탐침 실행)",
            "required_inputs": f"{rel(RUNTIME_PROBE_ATTEMPT_PACKAGE)};{rel(EXPECTED_PROBABILITY_TAPE)};{rel(COMMON_FILES_SYNC)}",
            "required_outputs": "runtime telemetry, tester reports, proxy-vs-MT5 diff, backtest forensic receipt(런타임 기록, 테스터 보고서, 프록시-MT5 차이, 백테스트 포렌식 영수증)",
            "blocked_if_missing": "terminal, broker visibility, tester output, telemetry(터미널, 브로커 가시성, 테스터 출력, 런타임 기록)",
            "forbidden_action": "Forward/Goal claim before MT5 evidence(MT5 근거 전 전진/목표 주장)",
            "effect": "package is handed to execution without changing thresholds or lots(임계값이나 로트 변경 없이 패키지를 실행으로 넘김)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    return tester_contract, proxy_contract, runtime_contract, queue


def include_hashes() -> dict[str, str]:
    paths = [EA_SOURCE, *sorted(EA_INCLUDE_DIR.glob("*.mqh"))]
    return {rel(path): aw.sha256_file(path) for path in paths if path_exists(path)}


def materialize_package() -> tuple[list[Path], dict[str, Any]]:
    features = load_features()
    frame = inner_holdout_frame(features)
    first_source, last_source, from_date, to_date = date_bounds(frame)
    values, input_hashes, sync_rows = materialize_feature_matrix(frame, features)
    model_handoff, expected_index_rows, expected_rows, set_rows, ini_rows, attempts, model_sync = materialize_models_and_expected(
        values,
        input_hashes,
        features,
        first_source,
        last_source,
    )
    sync_rows.extend(model_sync)
    tester_contract, proxy_contract, runtime_contract, execution_queue = build_contracts(attempts)
    feature_common = f"{COMMON_FEATURE_DIR}/side_cost_curve_inner_holdout_features.csv"
    feature_manifest = [
        {
            "feature_matrix_id": "side_cost_curve_inner_holdout_features",
            "feature_set_id": "ew_allowed_pretrade_features_v1",
            "feature_count": len(features),
            "row_count": len(frame),
            "first_source_time": first_source,
            "last_source_time": last_source,
            "feature_order_hash": read_json(EY_FEATURE_SCHEMA).get("feature_order_hash", ""),
            "local_path": rel(FEATURE_MATRIX),
            "local_sha256": aw.sha256_file(FEATURE_MATRIX),
            "common_path": feature_common,
            "common_sha256": aw.sha256_file(DEFAULT_COMMON_FILES / Path(feature_common)),
            "timestamp_semantics": "bar close timestamp, InpCsvTimestampIsBarClose=true(봉 마감 시각, InpCsvTimestampIsBarClose=true)",
            "effect": "MT5 can request closed-bar features by exact timestamp(MT5가 정확한 시각으로 마감봉 피처를 요청 가능)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]

    artifacts = [
        write_csv(FEATURE_MATRIX_MANIFEST, FEATURE_MANIFEST_COLUMNS, feature_manifest),
        write_csv(EXPECTED_PROBABILITY_INDEX, EXPECTED_INDEX_COLUMNS, expected_index_rows),
        write_csv(MODEL_HANDOFF_MANIFEST, MODEL_HANDOFF_COLUMNS, model_handoff),
        write_csv(COMMON_FILES_SYNC, SYNC_COLUMNS, sync_rows),
        write_csv(TESTER_SET_MANIFEST, SET_COLUMNS, set_rows),
        write_csv(TESTER_INI_MANIFEST, INI_COLUMNS, ini_rows),
        write_csv(RUNTIME_PROBE_ATTEMPT_PACKAGE, ATTEMPT_COLUMNS, attempts),
        write_csv(TESTER_IDENTITY_CONTRACT, CONTRACT_COLUMNS, tester_contract),
        write_csv(PROXY_MT5_COMPARISON_CONTRACT, CONTRACT_COLUMNS, proxy_contract),
        write_csv(RUNTIME_PARITY_CONTRACT, CONTRACT_COLUMNS, runtime_contract),
        write_csv(EXECUTION_QUEUE, QUEUE_COLUMNS, execution_queue),
        FEATURE_MATRIX,
        EXPECTED_PROBABILITY_TAPE,
    ]
    summary = {
        "feature_count": len(features),
        "feature_matrix_rows": len(frame),
        "first_source_time": first_source,
        "last_source_time": last_source,
        "tester_from_date": from_date,
        "tester_to_date": to_date,
        "expected_probability_rows": len(expected_rows),
        "attempt_rows": len(attempts),
        "model_handoff_rows": len(model_handoff),
        "common_sync_rows": len(sync_rows),
        "common_sync_ready_rows": sum(1 for row in sync_rows if row.get("exists") is True),
        "tester_set_rows": len(set_rows),
        "tester_ini_rows": len(ini_rows),
        "execution_queue_rows": len(execution_queue),
        "terminal_exists": path_exists(DEFAULT_TERMINAL),
        "metaeditor_exists": path_exists(DEFAULT_METAEDITOR),
        "common_files_root_exists": path_exists(DEFAULT_COMMON_FILES),
        "ea_source_sha256": aw.sha256_file(EA_SOURCE) if path_exists(EA_SOURCE) else "",
        "ea_binary_sha256": aw.sha256_file(EA_BINARY) if path_exists(EA_BINARY) else "",
        "portable_ea_exists": path_exists(PORTABLE_EA_EX5),
        "portable_ea_sha256": aw.sha256_file(PORTABLE_EA_EX5) if path_exists(PORTABLE_EA_EX5) else "",
        "include_module_hashes": include_hashes(),
    }
    return artifacts, summary


def build_gates(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    no_forbidden_claim = (
        final["mt5_execution"] == "not_run"
        and final["candidate_selection"] == "not_run"
        and final["forward_passed"] == "not_claimed"
        and final["forward_failed"] == "not_claimed"
        and final["goal_achieve"] == "not_claimed"
    )
    checks = [
        ("input_presence", final["missing_inputs"] == 0, str(final["missing_inputs"]), "0", rel(EZ_RUNTIME_QUEUE), "required EZ/EY inputs exist(필수 EZ/EY 입력 존재)"),
        ("parent_ez_gates_passed", final["ez_failed_gate_rows"] == 0, str(final["ez_failed_gate_rows"]), "0", rel(EZ_GATES), "EZ gates passed(EZ 게이트 통과)"),
        ("parent_next_action_matches", final["ez_next_action"] == RUN_ID, str(final["ez_next_action"]), RUN_ID, rel(EZ_FINAL), "FA follows EZ next action(FA가 EZ 다음 행동을 따름)"),
        ("feature_matrix_materialized", final["feature_matrix_rows"] > 1000 and final["feature_count"] == 58, f"rows={final['feature_matrix_rows']};features={final['feature_count']}", ">1000 and 58", rel(FEATURE_MATRIX_MANIFEST), "runtime feature matrix exists(런타임 피처 행렬 존재)"),
        ("expected_probability_tape_materialized", final["expected_probability_rows"] == final["feature_matrix_rows"] * final["attempt_rows"], f"expected={final['expected_probability_rows']};feature_rows={final['feature_matrix_rows']};attempts={final['attempt_rows']}", "feature_rows*attempts", rel(EXPECTED_PROBABILITY_INDEX), "expected probabilities exist for every attempt(모든 시도 예상 확률 존재)"),
        ("common_files_handoff_ready", final["common_sync_ready_rows"] == final["common_sync_rows"] and final["common_sync_rows"] >= 9, f"ready={final['common_sync_ready_rows']};rows={final['common_sync_rows']}", "all synced", rel(COMMON_FILES_SYNC), "Common Files handoff ready(공용 파일 인계 준비)"),
        ("tester_set_ini_materialized", final["tester_set_rows"] == final["tester_ini_rows"] == final["attempt_rows"] == 4, f"set={final['tester_set_rows']};ini={final['tester_ini_rows']};attempts={final['attempt_rows']}", "4/4/4", rel(RUNTIME_PROBE_ATTEMPT_PACKAGE), "tester files exist for each attempt(각 시도 테스터 파일 존재)"),
        ("argmax_no_tuning_contract", final["threshold_tuning"] == "not_run" and final["lot_optimization"] == "not_run", f"threshold={final['threshold_tuning']};lot={final['lot_optimization']}", "not_run/not_run", rel(TESTER_SET_MANIFEST), "argmax probe fixed with no tuning(최대확률 탐침 고정, 조정 없음)"),
        ("tester_identity_contract", final["terminal_exists"] and final["common_files_root_exists"] and final["portable_ea_exists"], f"terminal={final['terminal_exists']};common={final['common_files_root_exists']};ea={final['portable_ea_exists']}", "all true", rel(TESTER_IDENTITY_CONTRACT), "tester identity executable inputs exist(테스터 정체성 실행 입력 존재)"),
        ("proxy_mt5_comparison_contract", path_exists(PROXY_MT5_COMPARISON_CONTRACT), "present", "present", rel(PROXY_MT5_COMPARISON_CONTRACT), "proxy-MT5 diff required(프록시-MT5 차이 필요)"),
        ("execution_queue_materialized", final["execution_queue_rows"] == 1 and final["next_action"] == NEXT_RUN_ID, f"rows={final['execution_queue_rows']};next={final['next_action']}", f"1 and {NEXT_RUN_ID}", rel(EXECUTION_QUEUE), "FB execution queue opened(FB 실행 대기열 열림)"),
        ("no_forbidden_claim", no_forbidden_claim, f"mt5={final['mt5_execution']};selection={final['candidate_selection']};goal={final['goal_achieve']}", "not_run/not_claimed", rel(FINAL_DECISION), "FA materializes only, no operating claim(FA는 물질화만 하고 운영 주장 없음)"),
        ("required_gate_coverage_audit", True, "all required gates listed in closeout(모든 필수 게이트가 종료 기록에 있음)", "present", rel(GATE_AUDIT), "connects gates to completion claim(게이트를 완료 주장과 연결)"),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": "passed" if passed else "failed",
            "evidence_path": evidence,
            "observed": observed,
            "expected": expected,
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, passed, observed, expected, evidence, effect in checks
    ]


def build_receipts(final: Mapping[str, Any], artifact_paths: Sequence[Path]) -> list[Path]:
    routing = {
        "run_id": RUN_ID,
        "primary_family": "runtime_verification(런타임 검증)",
        "primary_skill": "obsidian-runtime-parity(옵시디언 런타임 동등성)",
        "support_skills": [
            "obsidian-backtest-forensics(옵시디언 백테스트 포렌식)",
            "obsidian-artifact-lineage(옵시디언 산출물 계보)",
            "obsidian-data-integrity(옵시디언 데이터 무결성)",
            "obsidian-result-judgment(옵시디언 결과 판정)",
        ],
        "required_gates": [row["gate_id"] for row in read_csv(GATE_AUDIT)] if path_exists(GATE_AUDIT) else [],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    data = {
        "research_path": rel(Path(__file__)),
        "runtime_path": rel(RUNTIME_PROBE_ATTEMPT_PACKAGE),
        "shared_contract": "58 features, bar-close timestamps, argmax_probe, [p_short,p_flat,p_long](58개 피처, 봉마감 시각, 최대확률 탐침, [숏/관망/롱] 확률)",
        "known_differences": "proxy expected value is independent fwd12; MT5 execution uses lifecycle and broker costs(프록시 예상값은 독립 12봉, MT5 실행은 생명주기와 브로커 비용)",
        "parity_check": "package materialized; tester execution pending(패키지 물질화, 테스터 실행 대기)",
        "runtime_claim_boundary": "runtime_probe_package_only(런타임 탐침 패키지 전용)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model = {
        "model_handoff_rows": final["model_handoff_rows"],
        "attempt_rows": final["attempt_rows"],
        "feature_order_hash": read_json(EY_FEATURE_SCHEMA).get("feature_order_hash", ""),
        "expected_probability_rows": final["expected_probability_rows"],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    runtime = {
        "terminal": DEFAULT_TERMINAL.as_posix(),
        "terminal_exists": final["terminal_exists"],
        "common_files_root": DEFAULT_COMMON_FILES.as_posix(),
        "portable_ea_ex5": PORTABLE_EA_EX5.as_posix(),
        "portable_ea_sha256": final["portable_ea_sha256"],
        "tester_profile_root": DEFAULT_TESTER_PROFILE_ROOT.as_posix(),
        "parity_identity": {
            "ea_source_sha256": final["ea_source_sha256"],
            "ea_binary_sha256": final["ea_binary_sha256"],
            "include_module_hashes": final["include_module_hashes"],
        },
        "claim_boundary": CLAIM_BOUNDARY,
    }
    forensics = {
        "tester_identity": "US100 M5 Deposit=500 Leverage=1:100 Model=4 real ticks(US100 M5 예수금 500 레버리지 1:100 실제 틱)",
        "ea_identity": rel(EA_SOURCE),
        "report_identity": "expected after run337FB(337FB 이후 기대)",
        "trade_evidence": "missing_required_until_execution(실행 전 필수 누락)",
        "cost_assumptions": "broker tester output required(브로커 테스터 출력 필요)",
        "backtest_judgment": "not_applicable_materialization_only(물질화 전용으로 해당 없음)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance = {
        "proxy_reference": rel(EZ_PROXY_REVIEW),
        "expected_probability_tape": rel(EXPECTED_PROBABILITY_TAPE),
        "required_next_diff": "diff, attribution, usability(차이, 귀속, 사용 가능성)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment = {
        "result_subject": RUN_ID,
        "judgment_label": final["judgment"],
        "evidence_available": [rel(RUNTIME_PROBE_ATTEMPT_PACKAGE), rel(COMMON_FILES_SYNC), rel(EXPECTED_PROBABILITY_TAPE)],
        "evidence_missing": "MT5 tester output and runtime telemetry(MT5 테스터 출력과 런타임 기록)",
        "goal_achieve": "not_claimed(주장 안 함)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths = [
        write_json(ROUTING_RECEIPT, routing),
        write_json(DATA_RECEIPT, data),
        write_json(MODEL_RECEIPT, model),
        write_json(RUNTIME_RECEIPT, runtime),
        write_json(FORENSICS_RECEIPT, forensics),
        write_json(PERFORMANCE_RECEIPT, performance),
        write_json(JUDGMENT_RECEIPT, judgment),
    ]
    all_artifacts = list(artifact_paths) + paths
    lineage = {
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in all_artifacts],
        "artifact_hashes": {
            rel(path): aw.sha256_file(path)
            for path in all_artifacts
            if path_exists(path) and aw.io_path(path).is_file()
        },
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "generated package plus Common Files handoff(생성 패키지와 공용 파일 인계)",
        "lineage_judgment": "connected_with_boundary; execution evidence pending(경계 조건부 연결, 실행 근거 대기)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths.append(write_json(LINEAGE_RECEIPT, lineage))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337FA Runtime Probe Package(337단계 337FA 런타임 탐침 패키지)

## Conclusion(결론)

run337FA(337FA 실행)는 run337EZ(337EZ 실행)의 4개 ONNX candidates(온엑스 후보)를 MT5 runtime probe(MT5 런타임 탐침)로 실행할 수 있게 package(패키지)를 만들었다.

Action(행동): inner holdout feature matrix(내부 보류 피처 행렬)와 expected probability tape(예상 확률 테이프)를 만들었다. Effect(효과): run337FB(337FB 실행)가 MT5 telemetry(MT5 기록)와 Python expected(파이썬 예상값)를 input hash(입력 해시)까지 비교할 수 있다.

Action(행동): Common Files handoff(공용 파일 인계), tester set/ini(테스터 설정), attempt package(시도 패키지)를 만들었다. Effect(효과): 다음 실행은 모델이나 threshold(임계값)를 바꾸지 않고 바로 MT5를 시도할 수 있다.

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- feature_matrix_rows(피처 행렬 행): `{final['feature_matrix_rows']}`
- expected_probability_rows(예상 확률 행): `{final['expected_probability_rows']}`
- attempts(시도): `{final['attempt_rows']}`
- common_sync(공용 파일 동기화): `{final['common_sync_ready_rows']}/{final['common_sync_rows']}`
- tester_window(테스터 구간): `{final['tester_from_date']}` to `{final['tester_to_date']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

## Boundary(경계)

- MT5 execution(MT5 실행): `not_run`
- candidate_selection(후보 선택): `not_run`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision(final: Mapping[str, Any]) -> Path:
    text = f"""# {TODAY} Stage337FA Decision(337FA 결정)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(RUNTIME_PROBE_ATTEMPT_PACKAGE)}`, `{rel(EXPECTED_PROBABILITY_TAPE)}`

Action(행동): MT5 runtime probe package(MT5 런타임 탐침 패키지)를 만들었다.
Effect(효과): run337FB(337FB 실행)에서 tester output(테스터 출력), telemetry(런타임 기록), proxy-vs-MT5 diff(프록시-MT5 차이)를 만들 수 있다.

Forward/Goal(전진/목표): `not_claimed`
runtime_authority(런타임 권위): `not_claimed`
claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return aw.write_text_lossless(DECISION_DOC, text, True)


def replace_line(text: str, prefix: str, replacement: str) -> str:
    pattern = re.compile(rf"^{re.escape(prefix)}.*$", flags=re.M)
    return pattern.sub(replacement, text, count=1) if pattern.search(text) else replacement + "\n" + text


FIELD_LABELS = {
    "current_run": "current_run(현재 실행)",
    "status": "status(상태)",
    "decision": "decision(결정)",
    "latest_completed_run": "latest_completed_run(최근 완료 실행)",
    "next_action": "next_action(다음 행동)",
    "claim_boundary": "claim_boundary(주장 경계)",
}


def replace_bullet_field(text: str, field_name: str, value: str) -> str:
    pattern = re.compile(rf"^- {re.escape(field_name)}(\([^)]+\))?: .*$", flags=re.M)
    replacement = f"- {FIELD_LABELS.get(field_name, field_name)}: {value}"
    return pattern.sub(replacement, text, count=1) if pattern.search(text) else replacement + "\n" + text


def upsert_section_before(text: str, marker: str, section: str, heading: str) -> str:
    pattern = re.compile(rf"^## {re.escape(heading)}.*?(?=^## )", flags=re.M | re.S)
    if pattern.search(text):
        return pattern.sub(section.rstrip() + "\n\n", text, count=1)
    return text.replace(marker, section.rstrip() + "\n\n" + marker, 1) if marker in text else text.rstrip() + "\n\n" + section.rstrip() + "\n"


def upsert_single_line(text: str, needle: str, entry: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if needle in line:
            lines[index] = entry
            trailing = "\n" if text.endswith("\n") else ""
            return "\n".join(lines) + trailing
    return text.rstrip() + "\n" + entry.rstrip() + "\n"


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    branch = ey.current_branch()
    workspace, workspace_bom = aw.read_text_lossless(WORKSPACE_STATE)
    workspace = replace_line(workspace, "current_run_id:", f"current_run_id: {final['next_action']}")
    workspace = replace_line(workspace, "updated_on:", f"updated_on: '{TODAY}'")
    workspace = replace_line(workspace, "active_branch:", f"active_branch: {branch}")
    focus = (
        "- >-\n"
        f"  Stage337 run337FA focus complete: run337FA(337FA 실행)는 `{final['status']}`로 MT5 runtime probe package(MT5 런타임 탐침 패키지)를 만들었다. "
        f"Effect(효과): feature rows(피처 행) `{final['feature_matrix_rows']}`, attempts(시도) `{final['attempt_rows']}`, Common Files handoff(공용 파일 인계) `{final['common_sync_ready_rows']}/{final['common_sync_rows']}`를 만들고 `{final['next_action']}`을 열었다. MT5/Forward/Goal(MT5/전진/목표)은 주장하지 않는다.\n"
    )
    if "Stage337 run337FA focus complete" in workspace:
        workspace = re.sub(
            r"- >-\n  Stage337 run337FA focus complete:.*?(?=\n- >-|\n[a-zA-Z_]+:|$)",
            focus.rstrip(),
            workspace,
            count=1,
            flags=re.S,
        )
    else:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    artifacts.append(aw.write_text_lossless(WORKSPACE_STATE, workspace, workspace_bom))

    current, current_bom = aw.read_text_lossless(CURRENT_STATE)
    for field_name, value in {
        "current_run": f"`{final['next_action']}`",
        "status": f"`{final['status']}`",
        "decision": f"`{final['decision']}`",
        "latest_completed_run": f"`{RUN_ID}`",
        "next_action": f"`{final['next_action']}`",
        "claim_boundary": f"`{CLAIM_BOUNDARY}`",
    }.items():
        current = replace_bullet_field(current, field_name, value)
    section = f"""## run337FA Runtime Probe Package(런타임 탐침 패키지)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- feature_matrix_rows(피처 행렬 행): `{final['feature_matrix_rows']}`
- expected_probability_rows(예상 확률 행): `{final['expected_probability_rows']}`
- attempts(시도): `{final['attempt_rows']}`
- common_sync(공용 파일 동기화): `{final['common_sync_ready_rows']}/{final['common_sync_rows']}`
- tester_window(테스터 구간): `{final['tester_from_date']}` to `{final['tester_to_date']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`
- effect(효과): ONNX candidates(온엑스 후보)를 MT5 runtime probe(MT5 런타임 탐침) 실행 대기열로 넘긴다. 실행과 운영 주장은 아직 하지 않는다.
- next_action(다음 행동): `{final['next_action']}`
"""
    current = upsert_section_before(current, "## run337EZ Side/Cost/Curve", section, "run337FA Runtime Probe Package")
    artifacts.append(aw.write_text_lossless(CURRENT_STATE, current, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{final['next_action']}`
- rebuild_status(재구축 상태): `{final['status']}`
- runtime_probe_attempts(런타임 탐침 시도): `{final['attempt_rows']}`
- common_files_handoff(공용 파일 인계): `{final['common_sync_ready_rows']}/{final['common_sync_rows']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): FA(337FA 실행)는 package(패키지)와 handoff(인계)만 만들며 MT5 execution(MT5 실행)과 operating selection(운영 선택)은 하지 않는다.
"""
    artifacts.append(aw.write_text_lossless(SELECTED_STATUS, selection, True))

    brief, brief_bom = aw.read_text_lossless(STAGE_BRIEF)
    brief_entry = (
        f"- {TODAY}: run337FA(337FA 실행) `{final['status']}`. "
        f"Effect(효과): feature rows(피처 행) `{final['feature_matrix_rows']}`, attempts(시도) `{final['attempt_rows']}`, Common Files handoff(공용 파일 인계) `{final['common_sync_ready_rows']}/{final['common_sync_rows']}`를 만들고 `{final['next_action']}`을 열었다. MT5/Forward/Goal(MT5/전진/목표)은 주장하지 않는다."
    )
    artifacts.append(aw.write_text_lossless(STAGE_BRIEF, upsert_single_line(brief, "run337FA(337FA 실행)", brief_entry), brief_bom))

    changelog, changelog_bom = aw.read_text_lossless(CHANGELOG)
    changelog_entry = (
        f"- {TODAY}: Stage337 run337FA(337FA 실행) `{final['status']}`. "
        f"Effect(효과): MT5 runtime probe package(MT5 런타임 탐침 패키지)를 만들고 `{final['next_action']}`을 열었다. MT5/Forward/Goal(MT5/전진/목표)은 주장하지 않았다."
    )
    artifacts.append(aw.write_text_lossless(CHANGELOG, upsert_single_line(changelog, "Stage337 run337FA", changelog_entry), changelog_bom))
    return artifacts


def upsert_csv_worktree(path: Path, columns: Sequence[str], row: Mapping[str, Any], key: str) -> Path:
    existing_columns, existing = aw.read_csv_table(path, prefer_head=False)
    merged_columns = list(existing_columns or columns)
    for column in columns:
        if column not in merged_columns:
            merged_columns.append(column)
    for column in row:
        if column not in merged_columns:
            merged_columns.append(column)
    key_value = str(row.get(key, ""))
    rows = [item for item in existing if str(item.get(key, "")) != key_value]
    rows.append({column: row.get(column, "") for column in merged_columns})
    return write_csv(path, merged_columns, rows)


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "side_cost_curve_runtime_probe_package",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"attempts={final['attempt_rows']};features={final['feature_matrix_rows']};expected={final['expected_probability_rows']};common_sync={final['common_sync_ready_rows']}/{final['common_sync_rows']};next_action={final['next_action']};goal_achieve_not_claimed.",
        "family": "runtime_verification_artifact_lineage_backtest_forensics",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__runtime_probe_package",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "runtime_probe_package",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "side_cost_curve_runtime_probe_package(방향/비용/곡선 런타임 탐침 패키지)",
        "tier_scope": "Tier A inner holdout runtime package, MT5 execution pending(Tier A 내부 보류 런타임 패키지, MT5 실행 대기)",
        "kpi_scope": "package only; no MT5 KPI(패키지 전용, MT5 성과 없음)",
        "scoreboard_lane": "runtime_verification",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"attempts={final['attempt_rows']};feature_rows={final['feature_matrix_rows']};expected_rows={final['expected_probability_rows']}",
        "guardrail_kpi": f"common_sync={final['common_sync_ready_rows']}/{final['common_sync_rows']};no_mt5_execution;no_selection;no_forward",
        "external_verification_status": "required_next_action",
        "notes": f"decision={final['decision']};next_action={final['next_action']};goal_achieve_not_claimed.",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__runtime_probe_package",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "runtime_verification_artifact_lineage_backtest_forensics",
        "evidence_scope": "feature matrix, expected probability tape, Common Files handoff, tester set/ini",
        "kpi_scope": "runtime_package_no_mt5_kpi",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"gates={final['passed_gates']}/{final['gate_rows']};next_action={final['next_action']};goal_achieve_not_claimed",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__runtime_probe_package",
        "family": "side_cost_curve_runtime_probe_package",
        "question": "can EY ONNX candidates be handed to MT5 runtime probe without changing model logic",
        "metric_scope": "package_identity_handoff_expected_tape",
        "primary_artifact": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "next_action": final["next_action"],
    }
    return [
        upsert_csv_worktree(RUN_REGISTRY, aw.RUN_REGISTRY_COLUMNS, run_row, "run_id"),
        upsert_csv_worktree(ALPHA_LEDGER, aw.ALPHA_LEDGER_COLUMNS, alpha_row, "ledger_row_id"),
        upsert_csv_worktree(STAGE_LEDGER, aw.STAGE_LEDGER_COLUMNS, stage_row, "ledger_row_id"),
    ]


def update_artifact_registry(paths: Sequence[Path]) -> Path:
    columns, rows = aw.read_csv_table(ARTIFACT_REGISTRY, prefer_head=False)
    columns = list(columns or aw.ARTIFACT_COLUMNS)
    for column in aw.ARTIFACT_COLUMNS:
        if column not in columns:
            columns.append(column)
    rows = [
        row
        for row in rows
        if not str(row.get("artifact_id", "")).startswith(f"{RUN_ID}::") and str(row.get("run_id", "")) != RUN_ID
    ]
    created_at = now_utc()
    seen: set[str] = set()
    for path in paths:
        if not path_exists(path) or not aw.io_path(path).is_file():
            continue
        artifact_path = rel(path)
        artifact_id = f"{RUN_ID}::{artifact_path}"
        if artifact_id in seen:
            continue
        seen.add(artifact_id)
        rows.append(
            {
                "artifact_id": artifact_id,
                "artifact_type": path.suffix.lstrip(".") or "file",
                "path": artifact_path,
                "sha256": aw.sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": STATUS,
                "artifact_path": artifact_path,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return write_csv(ARTIFACT_REGISTRY, columns, rows)


def make_final(summary: Mapping[str, Any]) -> dict[str, Any]:
    ez_final = read_json(EZ_FINAL)
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "missing_inputs": len(fail_if_missing(INPUT_FILES)),
        "ez_next_action": ez_final.get("next_action", ""),
        "ez_failed_gate_rows": sum(1 for row in read_csv(EZ_GATES) if row.get("status") != "passed"),
        "new_training": "not_run",
        "threshold_tuning": "not_run",
        "lot_optimization": "not_run",
        "candidate_selection": "not_run",
        "mt5_execution": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        **dict(summary),
    }
    return final


def main() -> int:
    for directory in (RUN_DIR, MT5_DIR, SET_DIR, INI_DIR, MODEL_COPY_DIR, FEATURE_DIR, EXPECTED_DIR):
        aw.io_path(directory).mkdir(parents=True, exist_ok=True)
    missing = fail_if_missing(INPUT_FILES)
    if missing:
        print(json.dumps({"run_id": RUN_ID, "status": "blocked_missing_inputs", "missing": [rel(path) for path in missing]}, ensure_ascii=False, indent=2))
        return 1

    artifacts, summary = materialize_package()
    final = make_final(summary)
    gates = build_gates(final)
    final["gate_rows"] = len(gates)
    final["passed_gates"] = sum(1 for row in gates if row["status"] == "passed")
    final["failed_gates"] = [row["gate_id"] for row in gates if row["status"] != "passed"]
    if final["failed_gates"]:
        final["status"] = "invalid_stage337FA_required_gate_failure_no_mt5_execution"
        final["judgment"] = "required_gate_failure_blocks_FB_runtime_execution"
        final["decision"] = "repair_stage337FA_required_gate_failure_before_FB"
        final["next_action"] = "repair_stage337FA_required_gate_failure_v1"

    artifacts.extend(
        [
            write_csv(GATE_AUDIT, GATE_COLUMNS, gates),
            write_json(FINAL_DECISION, final),
            write_json(
                RUN_MANIFEST,
                {
                    "run_id": RUN_ID,
                    "parent_run_id": PARENT_RUN_ID,
                    "inputs": [rel(path) for path in INPUT_FILES],
                    "outputs": [rel(path) for path in OUTPUT_FILES],
                    "claim_boundary": CLAIM_BOUNDARY,
                },
            ),
        ]
    )
    artifacts.extend(build_receipts(final, artifacts))
    artifacts.extend([write_report(final), write_decision(final)])
    artifacts.extend(update_docs(final))
    artifacts.extend(update_registers(final))
    artifacts.append(update_artifact_registry(artifacts))

    if final["failed_gates"]:
        print(json.dumps({"run_id": RUN_ID, "status": final["status"], "failed_gates": final["failed_gates"]}, ensure_ascii=False, indent=2))
        return 1
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": final["status"],
                "feature_matrix_rows": final["feature_matrix_rows"],
                "expected_probability_rows": final["expected_probability_rows"],
                "attempts": final["attempt_rows"],
                "common_sync": f"{final['common_sync_ready_rows']}/{final['common_sync_rows']}",
                "gates": f"{final['passed_gates']}/{final['gate_rows']}",
                "next_action": final["next_action"],
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
