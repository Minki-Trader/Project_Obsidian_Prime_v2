from __future__ import annotations

import json
import math
import shutil
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import joblib
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.models.onnx_bridge import ordered_sklearn_probabilities  # noqa: E402
from foundation.mt5 import runtime_support as mt5  # noqa: E402
from stage_pipelines.stage337 import (  # noqa: E402
    review_proxy_mt5_negative_lifecycle_cost_trade_shape_repair_training_without_db as iq,
)


aw = iq.aw

TODAY = "2026-06-01"
STAGE_ID = iq.STAGE_ID
STAGE_DIR = iq.STAGE_DIR
RUN_NUMBER = "run337IR"
RUN_ID = "run337IR_materialize_proxy_mt5_negative_lifecycle_cost_trade_shape_repair_runtime_probe_package_without_db_v1"
PARENT_RUN_ID = iq.RUN_ID
NEXT_RUN_ID = "run337IS_execute_proxy_mt5_negative_lifecycle_cost_trade_shape_repair_mt5_runtime_probe_without_db_v1"
STATUS = "completed_stage337IR_lifecycle_cost_trade_shape_repair_runtime_probe_package_materialized_no_mt5_execution"
JUDGMENT = "runtime_probe_package_ready_for_proxy_positive_lifecycle_cost_candidate_proxy_mt5_diff_required_no_selection"
DECISION = "stage337IR_open_run337IS_execute_lifecycle_cost_trade_shape_repair_mt5_runtime_probe"
CLAIM_BOUNDARY = (
    "research_development_runtime_probe_package_only_no_mt5_execution_in_IR_no_candidate_selection_"
    "no_forward_no_runtime_authority_no_operating_or_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MT5_DIR = RUN_DIR / "mt5"
SET_DIR = MT5_DIR / "sets"
INI_DIR = MT5_DIR / "inis"
MODEL_COPY_DIR = RUN_DIR / "models"
FEATURE_DIR = RUN_DIR / "feature_matrices"
EXPECTED_DIR = RUN_DIR / "expected_probability_tapes"
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run337IR_lifecycle_cost_repair_runtime_probe_package.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337IR_lifecycle_cost_trade_shape_repair_runtime_probe_package.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
STAGE_LEDGER = STAGE_DIR / "03_reviews" / "stage_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "README.md"
ROOT_CHANGELOG = ROOT / "CHANGELOG.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

DEFAULT_PORTABLE_ROOT = Path("C:/Users/awdse/AppData/Local/ObsidianPrime/mt5_portable_run329E")
DEFAULT_TERMINAL = DEFAULT_PORTABLE_ROOT / "terminal64.exe"
DEFAULT_METAEDITOR = DEFAULT_PORTABLE_ROOT / "MetaEditor64.exe"
DEFAULT_COMMON_FILES = DEFAULT_PORTABLE_ROOT / "Common" / "Files"
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

COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage337/{RUN_NUMBER}_lifecycle_cost_repair_probe"
COMMON_FEATURE_DIR = f"{COMMON_ROOT}/features"
COMMON_MODEL_DIR = f"{COMMON_ROOT}/models"
COMMON_TELEMETRY_DIR = f"{COMMON_ROOT}/telemetry"

FEATURE_MATRIX = FEATURE_DIR / "lifecycle_cost_repair_inner_holdout_features.csv"
FEATURE_MATRIX_MANIFEST = RUN_DIR / "runtime_feature_matrix_manifest.csv"
EXPECTED_PROBABILITY_TAPE = EXPECTED_DIR / "lifecycle_cost_repair_expected_probability_tape.csv"
EXPECTED_PROBABILITY_INDEX = RUN_DIR / "expected_probability_tape_index.csv"
MODEL_HANDOFF_MANIFEST = RUN_DIR / "model_handoff_manifest.csv"
COMMON_FILES_SYNC = RUN_DIR / "common_files_sync.csv"
TESTER_SET_MANIFEST = RUN_DIR / "tester_set_manifest.csv"
TESTER_INI_MANIFEST = RUN_DIR / "tester_ini_manifest.csv"
RUNTIME_PROBE_ATTEMPT_PACKAGE = RUN_DIR / "runtime_probe_attempt_package.csv"
TESTER_IDENTITY_CONTRACT = RUN_DIR / "tester_identity_contract.csv"
PROXY_MT5_COMPARISON_CONTRACT = RUN_DIR / "proxy_mt5_comparison_contract.csv"
RUNTIME_PARITY_CONTRACT = RUN_DIR / "runtime_parity_contract.csv"
EXECUTION_QUEUE = RUN_DIR / "run337IS_execution_queue.csv"
ROUTING_RECEIPT = RUN_DIR / "routing_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
FORENSICS_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    iq.FINAL_DECISION,
    iq.GATE_AUDIT,
    iq.POSITIVE_MATRIX,
    iq.ip.TRAINED_MODEL_MANIFEST,
    iq.ip.FEATURE_SCHEMA,
    iq.ip.ONNX_PARITY,
    iq.ip.io_review.inr.IN_INPUT_FRAME,
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
    CLAIM_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    WORKSPACE_STATE,
    CURRENT_WORKING_STATE,
    SELECTION_STATUS,
    STAGE_BRIEF,
    ROOT_CHANGELOG,
    WORKSPACE_CHANGELOG,
    RUN_REGISTRY,
    PROJECT_LEDGER,
    STAGE_LEDGER,
    ARTIFACT_REGISTRY,
    Path(__file__),
)


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def io(path: Path) -> Path:
    return aw.io_path(path)


def rel(path: Path | str) -> str:
    return aw.rel(path)


def display_path(path: Path | str) -> str:
    value = Path(path)
    try:
        if str(value.resolve()).lower().startswith(str(ROOT.resolve()).lower()):
            return rel(value)
    except OSError:
        pass
    return value.as_posix()


def exists(path: Path) -> bool:
    return io(path).exists()


def ensure_parent(path: Path) -> None:
    io(path.parent).mkdir(parents=True, exist_ok=True)


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io(path), low_memory=False)


def read_json(path: Path) -> Any:
    return json.loads(io(path).read_text(encoding="utf-8-sig"))


def write_csv(path: Path, frame: pd.DataFrame) -> Path:
    ensure_parent(path)
    target = path if len(str(path)) < 240 else io(path)
    frame.to_csv(target, index=False, encoding="utf-8-sig", lineterminator="\n")
    return path


def write_json(path: Path, payload: Any) -> Path:
    ensure_parent(path)
    io(path).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )
    return path


def write_bom_text(path: Path, text: str) -> Path:
    ensure_parent(path)
    io(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig", newline="\n")
    return path


def sha(path: Path) -> str:
    return aw.sha256_file(path)


def repo_path(value: str) -> Path:
    path = Path(str(value))
    return path if path.is_absolute() else ROOT / path


def passed_status(series: pd.Series) -> pd.Series:
    return series.astype(str).str.lower().isin(["pass", "passed", "true", "1", "yes"])


def csv_timestamp(value: object) -> str:
    timestamp = pd.Timestamp(value)
    if timestamp.tzinfo is None:
        timestamp = timestamp.tz_localize("UTC")
    else:
        timestamp = timestamp.tz_convert("UTC")
    return timestamp.strftime("%Y.%m.%d %H:%M:%S")


def format_feature_value(value: object) -> str:
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
    ensure_parent(target)
    shutil.copy2(io(source), io(target))
    return {
        "sync_id": sync_id,
        "source_path": display_path(source),
        "target_path": display_path(target),
        "exists": exists(target),
        "sha256": sha(target) if exists(target) else "",
        "status": "synced(동기화됨)" if exists(target) else "missing(누락)",
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def date_bounds(frame: pd.DataFrame) -> tuple[str, str, str, str]:
    timestamps = pd.to_datetime(frame["timestamp"], utc=True)
    first = timestamps.min()
    last = timestamps.max()
    from_date = first.strftime("%Y.%m.%d")
    to_date = (last + timedelta(days=1)).strftime("%Y.%m.%d")
    return first.strftime("%Y.%m.%d %H:%M:%S"), last.strftime("%Y.%m.%d %H:%M:%S"), from_date, to_date


def load_features() -> list[str]:
    schema = read_json(iq.ip.FEATURE_SCHEMA)
    return [str(feature) for feature in schema["features"]]


def max_hold_from_target(target: str) -> int:
    if target.endswith("fwd6"):
        return 6
    if target.endswith("fwd24"):
        return 24
    return 18


def attempt_name(index: int, model_id: str) -> str:
    return f"ir{index:02d}_{model_id}"


def inner_holdout_unique_frame(features: Sequence[str]) -> pd.DataFrame:
    positive = read_csv(iq.POSITIVE_MATRIX)
    if positive.empty:
        raise RuntimeError("no positive proxy candidate available for IR package")
    target = str(positive.iloc[0]["target_column"])
    valid_col = "hx_valid_fwd18" if target.endswith("fwd18") else "hx_valid_fwd6"
    frame = pd.read_parquet(io(iq.ip.io_review.inr.IN_INPUT_FRAME)).copy()
    task_frame = frame.loc[
        pd.to_numeric(frame[valid_col], errors="coerce").fillna(0).astype(int).eq(1)
        & pd.to_numeric(frame[target], errors="coerce").fillna(-1).astype(int).ne(-1)
    ].copy()
    _inner_train, inner_holdout = iq.ip.split_inner(task_frame)
    cost_order = {
        "spread_plus_extra0_points": 0,
        "spread_plus_extra2_points": 1,
        "spread_plus_extra5_points": 2,
    }
    inner_holdout["_cost_order"] = inner_holdout["cost_policy_id"].map(cost_order).fillna(99)
    unique = (
        inner_holdout.sort_values(["source_row_id", "_cost_order", "timestamp"])
        .drop_duplicates("source_row_id", keep="first")
        .sort_values("timestamp")
        .reset_index(drop=True)
    )
    missing = [feature for feature in features if feature not in unique.columns]
    if missing:
        raise ValueError(f"missing runtime features: {missing}")
    return unique


def materialize_feature_matrix(frame: pd.DataFrame, features: Sequence[str]) -> tuple[pd.DataFrame, list[str], list[dict[str, Any]]]:
    ensure_parent(FEATURE_MATRIX)
    header = ["timestamp", *features]
    hashes: list[str] = []
    formatted_values: list[list[float]] = []
    with io(FEATURE_MATRIX).open("w", encoding="utf-8", newline="") as handle:
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
    feature_common = f"{COMMON_FEATURE_DIR}/lifecycle_cost_repair_inner_holdout_features.csv"
    sync_rows = [
        copy_file(
            FEATURE_MATRIX,
            DEFAULT_COMMON_FILES / Path(feature_common),
            "common_feature_matrix",
            "Feature matrix(피처 행렬)를 Common Files(공용 파일)에 복사해 MT5 EA(전문가 자문)가 읽게 한다.",
        )
    ]
    return values, hashes, sync_rows


def materialize_models_and_expected(
    values: pd.DataFrame,
    hashes: Sequence[str],
    features: Sequence[str],
    first_time: str,
    last_time: str,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, list[dict[str, Any]]]:
    manifest = read_csv(iq.ip.TRAINED_MODEL_MANIFEST)
    model_lookup = {str(row["model_id"]): row for _, row in manifest.iterrows()}
    positive = read_csv(iq.POSITIVE_MATRIX).head(1)
    matrix = values.loc[:, features].astype("float32").to_numpy()
    _first_source, _last_source, from_date, to_date = date_bounds(
        pd.DataFrame({"timestamp": pd.to_datetime(values["timestamp"], format="%Y.%m.%d %H:%M:%S", utc=True)})
    )

    model_handoff: list[dict[str, Any]] = []
    expected_index: list[dict[str, Any]] = []
    expected_rows: list[dict[str, Any]] = []
    set_rows: list[dict[str, Any]] = []
    ini_rows: list[dict[str, Any]] = []
    attempts: list[dict[str, Any]] = []
    sync_rows: list[dict[str, Any]] = []
    labels = {0: "short", 1: "flat", 2: "long"}
    feature_common = f"{COMMON_FEATURE_DIR}/lifecycle_cost_repair_inner_holdout_features.csv"

    for index, (_, candidate) in enumerate(positive.iterrows(), start=1):
        model_id = str(candidate["model_id"])
        model = model_lookup[model_id]
        task_id = str(model["task_id"])
        target_column = str(model["target_column"])
        class_order = [int(item) for item in json.loads(str(model["class_order_json"]))]
        attempt = attempt_name(index, model_id)
        source_joblib = repo_path(str(model["model_path"]))
        source_onnx = repo_path(str(model["onnx_path"]))
        local_joblib = MODEL_COPY_DIR / f"{attempt}.joblib"
        local_onnx = MODEL_COPY_DIR / f"{attempt}.onnx"
        common_onnx = f"{COMMON_MODEL_DIR}/{attempt}.onnx"

        sync_rows.append(
            copy_file(
                source_joblib,
                local_joblib,
                f"local_joblib::{attempt}",
                "joblib model(joblib 모델)을 패키지에 복사해 expected tape(예상 테이프)를 재현한다.",
            )
        )
        sync_rows.append(
            copy_file(
                source_onnx,
                local_onnx,
                f"local_onnx::{attempt}",
                "ONNX model(ONNX 모델)을 패키지에 복사해 산출물 hash(해시)를 고정한다.",
            )
        )
        sync_rows.append(
            copy_file(
                local_onnx,
                DEFAULT_COMMON_FILES / Path(common_onnx),
                f"common_onnx::{attempt}",
                "ONNX model(ONNX 모델)을 Common Files(공용 파일)에 복사해 MT5 EA(전문가 자문)가 읽게 한다.",
            )
        )

        payload = joblib.load(io(local_joblib))
        fitted = payload["model"] if isinstance(payload, dict) and "model" in payload else payload
        probabilities = ordered_sklearn_probabilities(fitted, matrix, class_order)
        row_sum = probabilities.sum(axis=1, keepdims=True)
        probabilities = np.divide(probabilities, row_sum, out=np.zeros_like(probabilities), where=row_sum != 0.0)
        predictions = np.asarray(class_order, dtype=int)[np.argmax(probabilities, axis=1)]
        row_start = len(expected_rows)
        for row_index, timestamp in enumerate(values["timestamp"].tolist()):
            prob_by_class = {int(label): float(probabilities[row_index, pos]) for pos, label in enumerate(class_order)}
            decision_class = int(predictions[row_index])
            expected_rows.append(
                {
                    "attempt_name": attempt,
                    "model_id": model_id,
                    "task_id": task_id,
                    "bar_time": timestamp,
                    "source_time": timestamp,
                    "feature_input_hash": hashes[row_index],
                    "p_short": prob_by_class.get(0, 0.0),
                    "p_flat": prob_by_class.get(1, 0.0),
                    "p_long": prob_by_class.get(2, 0.0),
                    "decision_class": decision_class,
                    "decision_label": labels.get(decision_class, str(decision_class)),
                    "allowed_use": "proxy-vs-MT5 runtime parity comparison(프록시-MT5 런타임 동등성 비교)",
                    "forbidden_use": "MT5 KPI substitute or operating selection(MT5 핵심 성과 지표 대체 또는 운영 선택)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
        row_count = len(expected_rows) - row_start

        set_name = f"ObsidianPrimeV2_RuntimeProbeEA_{attempt}.set"
        ini_name = f"ObsidianPrimeV2_RuntimeProbeEA_{attempt}.ini"
        set_path = SET_DIR / set_name
        ini_path = INI_DIR / ini_name
        report_name = f"Project_Obsidian_Prime_v2_{RUN_NUMBER}_{attempt}"
        max_hold_bars = max_hold_from_target(target_column)
        set_values = {
            "InpRunId": f"{RUN_ID}_{attempt}",
            "InpExplorationLabel": "stage337IR_LifecycleCostRepair__MT5RuntimeProbe",
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
            "InpShortThreshold": 0.0,
            "InpLongThreshold": 0.0,
            "InpMinMargin": 0.0,
            "InpDecisionMode": "argmax_probe",
            "InpInvertSignal": False,
            "InpAllowTrading": True,
            "InpFixedLot": 0.10,
            "InpMagic": 3379300 + index,
            "InpDeviationPoints": 20,
            "InpCloseOnFlatSignal": False,
            "InpReverseOnOppositeSignal": True,
            "InpCloseOnlyOnOppositeSignal": False,
            "InpMaxHoldBars": max_hold_bars,
            "InpMaxConcurrentPositions": 1,
            "InpReentryCooldownBars": 0,
            "InpSameDirectionReentryCooldownBars": 0,
            "InpEntryTransitionOnly": False,
            "InpAtrSltpEnabled": False,
            "InpModelRiskSizingEnabled": False,
            "InpTelemetryEnabled": True,
            "InpTelemetryUseCommonFiles": True,
            "InpTelemetryCsvPath": f"{COMMON_TELEMETRY_DIR}/{attempt}_telemetry.csv",
            "InpSummaryCsvPath": f"{COMMON_TELEMETRY_DIR}/{attempt}_summary.csv",
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
                "attempt_name": attempt,
                "model_id": model_id,
                "task_id": task_id,
                "probe_priority": index,
                "source_model_path": model["model_path"],
                "source_model_sha256": model["model_sha256"],
                "local_model_path": rel(local_joblib),
                "local_model_sha256": sha(local_joblib),
                "source_onnx_path": model["onnx_path"],
                "source_onnx_sha256": model["onnx_sha256"],
                "local_onnx_path": rel(local_onnx),
                "local_onnx_sha256": sha(local_onnx),
                "common_onnx_path": common_onnx,
                "common_onnx_sha256": sha(DEFAULT_COMMON_FILES / Path(common_onnx)),
                "feature_order_hash": model["feature_order_hash"],
                "class_order_json": model["class_order_json"],
                "handoff_status": "ready_for_mt5_probe(MT5 탐침 준비)",
                "effect": "Model/ONNX/Common Files(모델/ONNX/공용 파일) hash(해시)를 연결한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        expected_index.append(
            {
                "expected_tape_id": f"expected::{attempt}",
                "model_id": model_id,
                "task_id": task_id,
                "attempt_name": attempt,
                "row_count": row_count,
                "first_source_time": first_time,
                "last_source_time": last_time,
                "path": rel(EXPECTED_PROBABILITY_TAPE),
                "sha256": "written_after_index",
                "decision_mode": "argmax_probe(최대 확률 탐침)",
                "allowed_use": "proxy-vs-MT5 diff(프록시-MT5 차이)",
                "forbidden_use": "operating selection(운영 선택)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        set_rows.append(
            {
                "attempt_name": attempt,
                "model_id": model_id,
                "set_path": rel(set_path),
                "set_sha256": set_payload["sha256"],
                "parameter_count": set_payload["parameter_count"],
                "decision_mode": "argmax_probe(최대 확률 탐침)",
                "allow_trading": True,
                "fixed_lot": 0.10,
                "max_hold_bars": max_hold_bars,
                "no_optimization_rule": "fixed lot and fixed argmax probe; no threshold tuning(고정 랏과 고정 argmax, 임계값 조정 없음)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        tester_values = ini_payload["tester"]
        ini_rows.append(
            {
                "attempt_name": attempt,
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
                "attempt_name": attempt,
                "next_run_id": NEXT_RUN_ID,
                "probe_priority": index,
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
                "common_telemetry_path": f"{COMMON_TELEMETRY_DIR}/{attempt}_telemetry.csv",
                "common_summary_path": f"{COMMON_TELEMETRY_DIR}/{attempt}_summary.csv",
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
                "max_hold_bars": max_hold_bars,
                "known_proxy_runtime_difference": "proxy score is signal sanity; MT5 uses broker lifecycle execution(프록시 점수는 신호 점검이고 MT5는 브로커 생명주기 실행)",
                "forbidden_action": "treat package priority as selection or promotion(패키지 우선순위를 선택/승격으로 취급)",
                "effect": "Attempt(시도)를 모델 로직 변경 없이 실행 가능하게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    expected_frame = pd.DataFrame(expected_rows)
    write_csv(EXPECTED_PROBABILITY_TAPE, expected_frame)
    expected_sha = sha(EXPECTED_PROBABILITY_TAPE)
    for row in expected_index:
        row["sha256"] = expected_sha
    return (
        pd.DataFrame(model_handoff),
        pd.DataFrame(expected_index),
        expected_frame,
        pd.DataFrame(set_rows),
        pd.DataFrame(ini_rows),
        pd.DataFrame(attempts),
        sync_rows,
    )


def contracts_and_queue() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    tester = pd.DataFrame(
        [
            {
                "contract_id": "tester_identity",
                "subject": "MT5 Strategy Tester(MT5 전략 테스터)",
                "requirement": "US100 M5, fixed lot, fixed argmax, no optimization(US100 M5, 고정 랏, 고정 argmax, 최적화 없음)",
                "evidence_path": rel(TESTER_INI_MANIFEST),
                "known_difference": "package only; actual broker costs are read after tester output(패키지 전용, 실제 비용은 테스터 출력 뒤 확인)",
                "blocked_if_missing": "tester report, settings, trade list(테스터 보고서, 설정, 거래 목록)",
                "forbidden_action": "trust KPI without tester identity(테스터 정체성 없이 KPI 신뢰)",
                "effect": "Backtest evidence(백테스트 근거)를 실행 뒤 감사할 수 있게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    proxy = pd.DataFrame(
        [
            {
                "contract_id": "proxy_mt5_diff",
                "subject": "proxy expected value vs MT5 runtime(프록시 예상값 대 MT5 런타임)",
                "requirement": "compare expected probabilities, input hash, decision, and KPI diff(예상 확률, 입력 해시, 결정, KPI 차이 비교)",
                "evidence_path": rel(EXPECTED_PROBABILITY_TAPE),
                "known_difference": "proxy is probability tape; MT5 is lifecycle execution(프록시는 확률 테이프, MT5는 생명주기 실행)",
                "blocked_if_missing": "runtime telemetry or expected tape(런타임 기록 또는 예상 테이프)",
                "forbidden_action": "use proxy net as MT5 profit(프록시 순수익을 MT5 수익으로 사용)",
                "effect": "Proxy(프록시)를 comparison baseline(비교 기준선)으로 바꾼다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    runtime = pd.DataFrame(
        [
            {
                "contract_id": "runtime_parity_inputs",
                "subject": "feature/model handoff(피처/모델 인계)",
                "requirement": "feature_input_hash and ONNX probabilities must match on overlap(겹치는 구간에서 입력 해시와 ONNX 확률 확인)",
                "evidence_path": f"{rel(FEATURE_MATRIX)};{rel(MODEL_HANDOFF_MANIFEST)}",
                "known_difference": "MT5 reads Common Files; Python reads repo artifacts(MT5는 공용 파일, Python은 저장소 산출물 사용)",
                "blocked_if_missing": "Common Files handoff or telemetry(공용 파일 인계 또는 런타임 기록)",
                "forbidden_action": "runtime authority from package only(패키지만으로 런타임 권위 주장)",
                "effect": "IS can compare runtime parity row by row(IS가 행 단위 런타임 동등성을 비교할 수 있다).",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    queue = pd.DataFrame(
        [
            {
                "queue_id": "is_execute_lifecycle_cost_repair_mt5_runtime_probe",
                "next_run_id": NEXT_RUN_ID,
                "priority": "P0",
                "task": "execute MT5 runtime probe for proxy-positive lifecycle/cost ONNX candidate(프록시 양성 생명주기/비용 ONNX 후보 MT5 런타임 탐침 실행)",
                "required_inputs": f"{rel(RUNTIME_PROBE_ATTEMPT_PACKAGE)};{rel(EXPECTED_PROBABILITY_TAPE)};{rel(COMMON_FILES_SYNC)}",
                "required_outputs": "runtime telemetry, tester reports, proxy-vs-MT5 diff(런타임 기록, 테스터 보고서, 프록시-MT5 차이)",
                "blocked_if_missing": "terminal, broker visibility, tester output, telemetry(터미널, 브로커 가시성, 테스터 출력, 런타임 기록)",
                "forbidden_action": "Forward/Goal claim before MT5 evidence(MT5 근거 전 전진/목표 주장)",
                "effect": "Package(패키지)를 실행으로 넘기며 threshold/lots(임계값/랏)은 바꾸지 않는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    return tester, proxy, runtime, queue


def include_hashes() -> dict[str, str]:
    paths = [EA_SOURCE, *sorted(EA_INCLUDE_DIR.glob("*.mqh"))]
    return {display_path(path): sha(path) for path in paths if exists(path)}


def materialize_package() -> dict[str, Any]:
    features = load_features()
    frame = inner_holdout_unique_frame(features)
    first_source, last_source, _from_date, _to_date = date_bounds(frame)
    values, hashes, sync_rows = materialize_feature_matrix(frame, features)
    model_handoff, expected_index, expected_rows, set_rows, ini_rows, attempts, model_sync = materialize_models_and_expected(
        values,
        hashes,
        features,
        first_source,
        last_source,
    )
    sync_rows.extend(model_sync)
    tester, proxy, runtime, queue = contracts_and_queue()
    feature_common = f"{COMMON_FEATURE_DIR}/lifecycle_cost_repair_inner_holdout_features.csv"
    schema = read_json(iq.ip.FEATURE_SCHEMA)
    feature_manifest = pd.DataFrame(
        [
            {
                "feature_matrix_id": "lifecycle_cost_repair_inner_holdout_features",
                "feature_set_id": iq.ip.FEATURE_SET_ID,
                "feature_count": len(features),
                "row_count": len(frame),
                "first_source_time": first_source,
                "last_source_time": last_source,
                "feature_order_hash": schema.get("feature_order_hash", ""),
                "local_path": rel(FEATURE_MATRIX),
                "local_sha256": sha(FEATURE_MATRIX),
                "common_path": feature_common,
                "common_sha256": sha(DEFAULT_COMMON_FILES / Path(feature_common)),
                "timestamp_semantics": "bar close timestamp, InpCsvTimestampIsBarClose=true(봉 마감 시각)",
                "effect": "MT5 can request closed-bar features by exact timestamp(MT5가 정확한 시각으로 마감봉 피처를 요청 가능).",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    write_csv(FEATURE_MATRIX_MANIFEST, feature_manifest)
    write_csv(EXPECTED_PROBABILITY_INDEX, expected_index)
    write_csv(MODEL_HANDOFF_MANIFEST, model_handoff)
    write_csv(COMMON_FILES_SYNC, pd.DataFrame(sync_rows))
    write_csv(TESTER_SET_MANIFEST, set_rows)
    write_csv(TESTER_INI_MANIFEST, ini_rows)
    write_csv(RUNTIME_PROBE_ATTEMPT_PACKAGE, attempts)
    write_csv(TESTER_IDENTITY_CONTRACT, tester)
    write_csv(PROXY_MT5_COMPARISON_CONTRACT, proxy)
    write_csv(RUNTIME_PARITY_CONTRACT, runtime)
    write_csv(EXECUTION_QUEUE, queue)

    return {
        "feature_count": len(features),
        "feature_matrix_rows": int(len(frame)),
        "expected_probability_rows": int(len(expected_rows)),
        "attempt_rows": int(len(attempts)),
        "model_handoff_rows": int(len(model_handoff)),
        "common_sync_rows": int(len(sync_rows)),
        "common_sync_ready_rows": int(sum(1 for row in sync_rows if row.get("exists") is True)),
        "tester_set_rows": int(len(set_rows)),
        "tester_ini_rows": int(len(ini_rows)),
        "first_source_time": first_source,
        "last_source_time": last_source,
        "candidate_model_ids": ";".join(attempts["model_id"].astype(str).tolist()) if not attempts.empty else "",
        "candidate_task_ids": ";".join(attempts["task_id"].astype(str).tolist()) if not attempts.empty else "",
        "feature_order_hash": schema.get("feature_order_hash", ""),
        "portable_terminal_exists": exists(DEFAULT_TERMINAL),
        "portable_metaeditor_exists": exists(DEFAULT_METAEDITOR),
        "portable_common_files_root": DEFAULT_COMMON_FILES.as_posix(),
        "portable_ea_ex5_exists": exists(PORTABLE_EA_EX5),
        "repo_ea_binary_exists": exists(EA_BINARY),
        "ea_module_hashes": include_hashes(),
        "next_action": NEXT_RUN_ID,
    }


def gate_row(gate: str, status: str, evidence: str, effect: str) -> dict[str, Any]:
    return {
        "gate_id": gate,
        "status": status,
        "evidence_path": evidence,
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def make_gates(summary: Mapping[str, Any]) -> pd.DataFrame:
    parent_gates = read_csv(iq.GATE_AUDIT)
    parent_passed = passed_status(parent_gates["status"]).all()
    expected_rows_ok = summary["expected_probability_rows"] == summary["feature_matrix_rows"] * summary["attempt_rows"]
    sync_ready = summary["common_sync_rows"] == summary["common_sync_ready_rows"] and summary["common_sync_rows"] >= 3
    return pd.DataFrame(
        [
            gate_row("parent_iq_gates_passed", "passed" if parent_passed else "failed", rel(iq.GATE_AUDIT), "IQ review(IQ 검토)가 통과한 후보만 package(패키지)화한다."),
            gate_row("proxy_positive_candidate_loaded", "passed" if summary["attempt_rows"] >= 1 else "failed", rel(iq.POSITIVE_MATRIX), "proxy-positive(프록시 양성) 후보를 불러온다."),
            gate_row("feature_matrix_materialized", "passed" if exists(FEATURE_MATRIX) and summary["feature_matrix_rows"] > 0 else "failed", rel(FEATURE_MATRIX), "MT5가 읽을 feature matrix(피처 행렬)를 만든다."),
            gate_row("expected_probability_tape_materialized", "passed" if exists(EXPECTED_PROBABILITY_TAPE) and expected_rows_ok else "failed", rel(EXPECTED_PROBABILITY_TAPE), "proxy expected value(프록시 예상값)를 MT5 diff(차이) 기준선으로 만든다."),
            gate_row("model_and_common_files_synced", "passed" if sync_ready else "failed", rel(COMMON_FILES_SYNC), "ONNX(ONNX)와 feature matrix(피처 행렬)를 Common Files(공용 파일)에 복사한다."),
            gate_row("tester_set_ini_materialized", "passed" if summary["tester_set_rows"] == summary["attempt_rows"] and summary["tester_ini_rows"] == summary["attempt_rows"] else "failed", f"{rel(TESTER_SET_MANIFEST)};{rel(TESTER_INI_MANIFEST)}", "MT5 Strategy Tester(MT5 전략 테스터) 실행 파일을 만든다."),
            gate_row("runtime_attempt_package_written", "passed" if exists(RUNTIME_PROBE_ATTEMPT_PACKAGE) and summary["attempt_rows"] >= 1 else "failed", rel(RUNTIME_PROBE_ATTEMPT_PACKAGE), "IS 실행이 읽을 attempt package(시도 패키지)를 만든다."),
            gate_row("proxy_mt5_contracts_written", "passed" if exists(PROXY_MT5_COMPARISON_CONTRACT) and exists(RUNTIME_PARITY_CONTRACT) else "failed", f"{rel(PROXY_MT5_COMPARISON_CONTRACT)};{rel(RUNTIME_PARITY_CONTRACT)}", "proxy-MT5 comparison(프록시-MT5 비교) 조건을 고정한다."),
            gate_row("execution_queue_opened", "passed" if exists(EXECUTION_QUEUE) else "failed", rel(EXECUTION_QUEUE), "다음 IS runtime probe(런타임 탐침) 실행으로 넘긴다."),
            gate_row("no_mt5_execution_in_ir", "passed", rel(CLAIM_RECEIPT), "IR은 package(패키지)만 만들고 MT5 실행은 하지 않는다."),
            gate_row("no_forbidden_operating_claim", "passed", rel(CLAIM_RECEIPT), "selected model(선정 모델), runtime authority(런타임 권위), Goal Achieve(목표 달성)를 주장하지 않는다."),
            gate_row("required_gate_coverage_audit_written", "passed", rel(GATE_AUDIT), "gate coverage(게이트 커버리지)를 closeout(종료 기록)에 연결한다."),
        ]
    )


def append_or_replace_csv(path: Path, key_columns: Iterable[str], row: Mapping[str, Any]) -> None:
    frame = read_csv(path) if exists(path) else pd.DataFrame()
    if frame.empty:
        frame = pd.DataFrame(columns=list(row.keys()))
    for column in row:
        if column not in frame.columns:
            frame[column] = ""
    mask = pd.Series(True, index=frame.index)
    for key in key_columns:
        if key in frame.columns:
            mask = mask & frame[key].astype(str).eq(str(row[key]))
        else:
            mask = mask & False
    frame = frame.loc[~mask].copy()
    frame = pd.concat([frame, pd.DataFrame([row])], ignore_index=True)
    ordered = list(dict.fromkeys(list(frame.columns) + list(row.keys())))
    write_csv(path, frame[ordered])


def append_text_once(path: Path, marker: str, text: str) -> None:
    current = io(path).read_text(encoding="utf-8-sig") if exists(path) else ""
    if marker in current:
        return
    next_text = (current.rstrip() + "\n\n" + text.strip() + "\n") if current.strip() else text.strip() + "\n"
    write_bom_text(path, next_text)


def artifact_paths() -> list[Path]:
    return list(OUTPUT_FILES)


def update_artifact_registry(paths: Sequence[Path]) -> None:
    registry = read_csv(ARTIFACT_REGISTRY) if exists(ARTIFACT_REGISTRY) else pd.DataFrame()
    required = ["stage_id", "run_id", "artifact_type", "path", "sha256", "created_at", "claim_boundary"]
    for column in required:
        if column not in registry.columns:
            registry[column] = ""
    rows = []
    for path in paths:
        if exists(path) and io(path).is_file():
            rows.append(
                {
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "artifact_type": "report" if path.suffix.lower() == ".md" else path.suffix.lower().lstrip("."),
                    "path": display_path(path),
                    "sha256": sha(path),
                    "created_at": TODAY,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    if rows:
        new_paths = {row["path"] for row in rows}
        registry = registry.loc[~registry["path"].astype(str).isin(new_paths)].copy()
        registry = pd.concat([registry, pd.DataFrame(rows)], ignore_index=True)
        columns = list(dict.fromkeys(required + list(registry.columns)))
        write_csv(ARTIFACT_REGISTRY, registry[columns])


def write_receipts(summary: Mapping[str, Any], gates: pd.DataFrame) -> None:
    base = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": now_utc(),
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(ROUTING_RECEIPT, {**base, "next_run_id": NEXT_RUN_ID, "attempt_rows": summary["attempt_rows"], "effect": "runtime probe package(런타임 탐침 패키지)를 IS execution(IS 실행)으로 넘긴다."})
    write_json(DATA_RECEIPT, {**base, "feature_matrix": rel(FEATURE_MATRIX), "feature_matrix_rows": summary["feature_matrix_rows"], "first_source_time": summary["first_source_time"], "last_source_time": summary["last_source_time"], "timestamp_semantics": "bar close timestamp(봉 마감 시각)", "effect": "MT5 입력 시각을 고정한다."})
    write_json(MODEL_RECEIPT, {**base, "candidate_model_ids": summary["candidate_model_ids"], "model_handoff_rows": summary["model_handoff_rows"], "feature_order_hash": summary["feature_order_hash"], "effect": "ONNX handoff(ONNX 인계) hash(해시)를 고정한다."})
    write_json(RUNTIME_RECEIPT, {**base, "research_path": rel(Path(__file__)), "runtime_path": "package_only_no_execution(패키지 전용, 실행 없음)", "shared_contract": rel(RUNTIME_PARITY_CONTRACT), "parity_check": rel(EXPECTED_PROBABILITY_TAPE), "runtime_claim_boundary": "runtime_probe_package_only(런타임 탐침 패키지 전용)"})
    write_json(FORENSICS_RECEIPT, {**base, "tester_identity": rel(TESTER_IDENTITY_CONTRACT), "ea_identity": summary["ea_module_hashes"], "report_identity": "not_run_in_IR(IR에서 미실행)", "trade_evidence": "not_available_until_IS(IS 전에는 없음)", "cost_assumptions": "Strategy Tester output required(전략 테스터 출력 필요)", "backtest_judgment": "inconclusive_package_only(패키지만으로 불충분)"})
    write_json(PERFORMANCE_RECEIPT, {**base, "observed_change": "runtime probe package materialized(런타임 탐침 패키지 물질화)", "comparison_baseline": rel(iq.FINAL_DECISION), "likely_drivers": "lifecycle-cost blend probe priority(생명주기 비용 혼합 탐침 우선순위)", "next_probe": NEXT_RUN_ID, "attribution_confidence": "not_applicable_until_mt5( MT5 전 해당 없음)"})
    write_json(JUDGMENT_RECEIPT, {**base, "decision": DECISION, "next_run_id": NEXT_RUN_ID, "gate_passes": int(gates["status"].astype(str).eq("passed").sum()), "gate_total": int(len(gates)), "judgment_label": JUDGMENT})
    write_json(CLAIM_RECEIPT, {**base, "candidate_selection": "not_run", "mt5_execution": "not_run_in_IR", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "goal_achieve": "not_claimed"})
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [display_path(path) for path in artifact_paths() if exists(path)],
            "artifact_hashes": {display_path(path): sha(path) for path in artifact_paths() if exists(path) and io(path).is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "generated_with_manifest(목록과 함께 생성)",
            "lineage_judgment": "connected_with_boundary(경계 조건부 연결)",
        },
    )


def write_final(summary: Mapping[str, Any], gates: pd.DataFrame) -> dict[str, Any]:
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "candidate_selection": "not_run",
        "mt5_runtime_probe": "not_run_in_IR",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "gate_passes": int(gates["status"].astype(str).eq("passed").sum()),
        "gate_total": int(len(gates)),
        "claim_boundary": CLAIM_BOUNDARY,
        **dict(summary),
    }
    write_json(FINAL_DECISION, final)
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "created_at": TODAY,
            "created_at_utc": now_utc(),
            "script": rel(Path(__file__)),
            "inputs": [rel(path) for path in INPUT_FILES],
            "outputs": [display_path(path) for path in OUTPUT_FILES if exists(path)],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    return final


def write_docs(final: Mapping[str, Any]) -> None:
    report = f"""# run337IR Lifecycle Cost Repair Runtime Probe Package(run337IR 생명주기 비용 수리 런타임 탐침 패키지)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- gates(게이트): `{final['gate_passes']}/{final['gate_total']}`
- candidate_model_ids(후보 모델 ID): `{final['candidate_model_ids']}`
- feature_matrix_rows(피처 행렬 행): `{final['feature_matrix_rows']}`
- expected_probability_rows(예상 확률 행): `{final['expected_probability_rows']}`
- common_sync(공용 파일 동기화): `{final['common_sync_ready_rows']}/{final['common_sync_rows']}`

## Action(행동)

IQ review(IQ 검토)의 probe priority(탐침 우선순위) 후보를 MT5 runtime probe(MT5 런타임 탐침) package(패키지)로 물질화했다.
Effect(효과): 다음 IS run(IS 실행)이 feature matrix(피처 행렬), ONNX(ONNX), expected tape(예상 테이프), tester set/ini(테스터 설정)를 바로 사용할 수 있다.

## Boundary(경계)

No MT5 execution in IR(IR에서 MT5 실행 없음), no candidate selection(후보 선택 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).

## Next(다음)

`{NEXT_RUN_ID}`에서 MT5 runtime probe(MT5 런타임 탐침)를 실행하고 proxy-MT5 diff(프록시-MT5 차이)를 기록한다.
"""
    decision = f"""# {TODAY} Stage337IR Decision(337IR 결정)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- evidence(근거): `{rel(RUNTIME_PROBE_ATTEMPT_PACKAGE)}`, `{rel(EXPECTED_PROBABILITY_TAPE)}`, `{rel(COMMON_FILES_SYNC)}`

Action(행동): proxy-positive(프록시 양성) lifecycle/cost(생명주기/비용) 후보를 MT5 runtime probe(MT5 런타임 탐침) 입력으로 만들었다.
Effect(효과): proxy expected value(프록시 예상값)를 MT5 runtime evidence(MT5 런타임 근거)와 비교할 수 있게 한다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    current = f"""# Current Working State(현재 작업 상태)

## Current Truth(현재 진실)

- active_stage(현재 단계): `{STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`

## Effect(효과)

IR package(IR 패키지)는 MT5 runtime probe(MT5 런타임 탐침) 실행에 필요한 파일을 만들었다.
효과는 IS run(IS 실행)이 proxy-MT5 diff(프록시-MT5 차이)를 실제 런타임 근거로 확인하게 하는 것이다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{DECISION}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- probe_priority_model(탐침 우선 모델): `{final['candidate_model_ids']}`
- MT5 execution(MT5 실행): `not_run_in_IR(IR에서 미실행)`
- runtime_authority(런타임 권위): `not_claimed(주장 안 함)`
- operating_promotion(운영 승격): `not_claimed(주장 안 함)`
- goal_achieve(목표 달성): `not_claimed(주장 안 함)`

Effect(효과): runtime package(런타임 패키지)를 selection(선택)이나 authority(권위)로 오해하지 않게 한다.
"""
    workspace = f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
current_decision: {DECISION}
next_run_id: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
"""
    write_bom_text(REPORT_PATH, report)
    write_bom_text(DECISION_DOC, decision)
    write_bom_text(CURRENT_WORKING_STATE, current)
    write_bom_text(SELECTION_STATUS, selection)
    write_bom_text(WORKSPACE_STATE, workspace)
    marker = f"run337IR {RUN_ID}"
    append_text_once(
        STAGE_BRIEF,
        marker,
        f"""## run337IR Lifecycle Cost Repair Runtime Probe Package(생명주기 비용 수리 런타임 탐침 패키지)

- run_id(실행 ID): `{RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- next(다음): `{NEXT_RUN_ID}`
- effect(효과): feature matrix(피처 행렬), ONNX(ONNX), expected tape(예상 테이프), tester files(테스터 파일)를 만들었다.
""",
    )
    changelog_entry = f"""## {TODAY} run337IR Lifecycle Cost Repair Runtime Probe Package(생명주기 비용 수리 런타임 탐침 패키지)

- action(행동): IQ probe priority(IQ 탐침 우선순위) 후보를 MT5 runtime probe(MT5 런타임 탐침) package(패키지)로 만들었다.
- effect(효과): `{NEXT_RUN_ID}`에서 proxy-MT5 diff(프록시-MT5 차이)를 실행 근거로 볼 수 있게 했다.
- boundary(경계): MT5 execution(MT5 실행), selected model(선정 모델), Goal Achieve(목표 달성)는 없다.
"""
    append_text_once(ROOT_CHANGELOG, marker, changelog_entry)
    append_text_once(WORKSPACE_CHANGELOG, marker, changelog_entry)


def update_registers(final: Mapping[str, Any]) -> None:
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_date": TODAY,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "primary_artifact": rel(FINAL_DECISION),
        "report_path": rel(REPORT_PATH),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], base)
    rows = [
        {
            **base,
            "view": "Tier A separate(Tier A 분리)",
            "tier": "Tier A",
            "metric_scope": "runtime_probe_package",
            "candidate_model_ids": final["candidate_model_ids"],
            "feature_matrix_rows": final["feature_matrix_rows"],
            "expected_probability_rows": final["expected_probability_rows"],
            "result_status": "runtime_probe_package_ready_no_mt5_execution",
        },
        {
            **base,
            "view": "Tier B separate(Tier B 분리)",
            "tier": "Tier B",
            "metric_scope": "missing_required",
            "result_status": "missing_required",
        },
        {
            **base,
            "view": "Tier A+B combined(Tier A+B 합산)",
            "tier": "Tier A+B",
            "metric_scope": "missing_required",
            "result_status": "missing_required",
        },
    ]
    for row in rows:
        append_or_replace_csv(PROJECT_LEDGER, ["run_id", "view"], row)
        append_or_replace_csv(STAGE_LEDGER, ["run_id", "view"], row)


def main() -> None:
    for path in (RUN_DIR, MT5_DIR, SET_DIR, INI_DIR, MODEL_COPY_DIR, FEATURE_DIR, EXPECTED_DIR, REVIEW_DIR, DECISION_DOC.parent):
        io(path).mkdir(parents=True, exist_ok=True)
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError(f"missing required input files: {missing}")
    summary = materialize_package()
    gates = make_gates(summary)
    write_csv(GATE_AUDIT, gates)
    write_receipts(summary, gates)
    final = write_final(summary, gates)
    write_docs(final)
    update_registers(final)
    update_artifact_registry(artifact_paths())
    failed = gates.loc[~gates["status"].astype(str).eq("passed")]
    if not failed.empty:
        raise RuntimeError(f"IR gates failed: {failed[['gate_id', 'status']].to_dict(orient='records')}")
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "attempt_rows": final["attempt_rows"],
                "candidate_model_ids": final["candidate_model_ids"],
                "feature_matrix_rows": final["feature_matrix_rows"],
                "expected_probability_rows": final["expected_probability_rows"],
                "common_sync": f"{final['common_sync_ready_rows']}/{final['common_sync_rows']}",
                "gates": f"{final['gate_passes']}/{final['gate_total']}",
                "next_action": NEXT_RUN_ID,
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
