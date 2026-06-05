from __future__ import annotations

import json
import math
import shutil
import sys
from datetime import timedelta
from pathlib import Path
from typing import Iterable, Sequence

import joblib
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.models.onnx_bridge import ordered_sklearn_probabilities  # noqa: E402
from foundation.mt5 import runtime_support as mt5  # noqa: E402
from stage_pipelines.stage337 import (  # noqa: E402
    review_proxy_negative_trade_shape_offensive_pivot_training_without_db as ia,
)

aw = ia.aw

TODAY = "2026-06-01"
STAGE_ID = ia.STAGE_ID
STAGE_DIR = ia.STAGE_DIR
RUN_NUMBER = "run337IB"
RUN_ID = "run337IB_materialize_proxy_positive_offensive_pivot_runtime_probe_package_without_db_v1"
PARENT_RUN_ID = ia.RUN_ID
NEXT_RUN_ID = "run337IC_execute_proxy_positive_offensive_pivot_mt5_runtime_probe_without_db_v1"
STATUS = "completed_stage337IB_proxy_positive_runtime_probe_package_materialized_no_mt5_execution"
JUDGMENT = "runtime_probe_package_ready_for_mt5_attempt_proxy_diff_required_no_selection"
DECISION = "stage337IB_open_run337IC_execute_proxy_positive_offensive_pivot_mt5_runtime_probe"
CLAIM_BOUNDARY = (
    "research_development_runtime_probe_package_only_no_mt5_execution_in_IB_no_candidate_selection_"
    "no_forward_no_runtime_authority_no_operating_or_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MT5_DIR = RUN_DIR / "mt5"
SET_DIR = MT5_DIR / "sets"
INI_DIR = MT5_DIR / "inis"
MODEL_COPY_DIR = RUN_DIR / "models"
FEATURE_DIR = RUN_DIR / "feature_matrices"
EXPECTED_DIR = RUN_DIR / "expected_probability_tapes"
REVIEW_DIR = ia.REVIEW_DIR
REPORT_PATH = REVIEW_DIR / "run337IB_proxy_positive_runtime_probe_package.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337IB_proxy_positive_runtime_probe_package.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
STAGE_LEDGER = STAGE_DIR / "03_reviews" / "stage_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
SELECTION_STATUS = ROOT / "docs" / "registers" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "README.md"
CHANGELOG = ROOT / "CHANGELOG.md"

DEFAULT_PORTABLE_ROOT = Path("C:/Users/awdse/AppData/Local/ObsidianPrime/mt5_portable_run329E")
DEFAULT_TERMINAL = DEFAULT_PORTABLE_ROOT / "terminal64.exe"
DEFAULT_METAEDITOR = DEFAULT_PORTABLE_ROOT / "MetaEditor64.exe"
DEFAULT_COMMON_FILES = DEFAULT_PORTABLE_ROOT / "Common" / "Files"
DEFAULT_TESTER_PROFILE_ROOT = DEFAULT_PORTABLE_ROOT / "MQL5" / "Profiles" / "Tester"
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

COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage337/{RUN_NUMBER}_proxy_positive_offensive_pivot_runtime_probe"
COMMON_FEATURE_DIR = f"{COMMON_ROOT}/features"
COMMON_MODEL_DIR = f"{COMMON_ROOT}/models"
COMMON_TELEMETRY_DIR = f"{COMMON_ROOT}/telemetry"

FEATURE_MATRIX = FEATURE_DIR / "proxy_positive_inner_holdout_features.csv"
FEATURE_MATRIX_MANIFEST = RUN_DIR / "runtime_feature_matrix_manifest.csv"
EXPECTED_PROBABILITY_TAPE = EXPECTED_DIR / "proxy_positive_expected_probability_tape.csv"
EXPECTED_PROBABILITY_INDEX = RUN_DIR / "expected_probability_tape_index.csv"
MODEL_HANDOFF_MANIFEST = RUN_DIR / "model_handoff_manifest.csv"
COMMON_FILES_SYNC = RUN_DIR / "common_files_sync.csv"
TESTER_SET_MANIFEST = RUN_DIR / "tester_set_manifest.csv"
TESTER_INI_MANIFEST = RUN_DIR / "tester_ini_manifest.csv"
RUNTIME_PROBE_ATTEMPT_PACKAGE = RUN_DIR / "runtime_probe_attempt_package.csv"
TESTER_IDENTITY_CONTRACT = RUN_DIR / "tester_identity_contract.csv"
PROXY_MT5_COMPARISON_CONTRACT = RUN_DIR / "proxy_mt5_comparison_contract.csv"
RUNTIME_PARITY_CONTRACT = RUN_DIR / "runtime_parity_contract.csv"
EXECUTION_QUEUE = RUN_DIR / "run337IC_execution_queue.csv"
ROUTING_RECEIPT = RUN_DIR / "routing_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
FORENSICS_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "lineage_receipt.json"
CLAIM_BOUNDARY_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"


def _ensure_dirs() -> None:
    for path in [
        RUN_DIR,
        MT5_DIR,
        SET_DIR,
        INI_DIR,
        MODEL_COPY_DIR,
        FEATURE_DIR,
        EXPECTED_DIR,
        REVIEW_DIR,
        DECISION_DOC.parent,
        RUN_REGISTRY.parent,
    ]:
        aw.io_path(path).mkdir(parents=True, exist_ok=True)


def _read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(aw.io_path(path))


def _read_json(path: Path) -> dict:
    return json.loads(aw.io_path(path).read_text(encoding="utf-8-sig"))


def _write_csv(path: Path, frame: pd.DataFrame) -> None:
    aw.io_path(path.parent).mkdir(parents=True, exist_ok=True)
    frame.to_csv(aw.io_path(path), index=False, encoding="utf-8-sig", lineterminator="\n")


def _write_json(path: Path, payload: dict) -> None:
    aw.io_path(path.parent).mkdir(parents=True, exist_ok=True)
    aw.io_path(path).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _write_bom_text(path: Path, text: str) -> None:
    aw.io_path(path.parent).mkdir(parents=True, exist_ok=True)
    aw.io_path(path).write_text(text, encoding="utf-8-sig")


def _sha(path: Path) -> str:
    return aw.sha256_file(path)


def _path_exists(path: Path) -> bool:
    return aw.io_path(path).exists()


def _repo_path(value: str) -> Path:
    path = Path(str(value))
    return path if path.is_absolute() else ROOT / path


def _csv_timestamp(value: object) -> str:
    return pd.Timestamp(value).tz_convert("UTC").strftime("%Y.%m.%d %H:%M:%S")


def _format_feature_value(value: object) -> str:
    number = np.float32(float(value)).item()
    if not math.isfinite(float(number)):
        raise ValueError("non-finite feature value")
    return format(float(number), ".9g")


def _fnv1a_mql_hash(line: str) -> str:
    digest = 1469598103934665603
    mask = 0xFFFFFFFFFFFFFFFF
    for char in line:
        digest = ((digest ^ ord(char)) * 1099511628211) & mask
    return f"{digest:X}"


def _copy_file(source: Path, target: Path, sync_id: str, effect: str) -> dict:
    aw.io_path(target.parent).mkdir(parents=True, exist_ok=True)
    shutil.copy2(aw.io_path(source), aw.io_path(target))
    return {
        "sync_id": sync_id,
        "source_path": aw.rel(source) if str(source).startswith(str(ROOT)) else source.as_posix(),
        "target_path": aw.rel(target) if str(target).startswith(str(ROOT)) else target.as_posix(),
        "exists": _path_exists(target),
        "sha256": _sha(target) if _path_exists(target) else "",
        "status": "synced(동기화됨)" if _path_exists(target) else "missing(누락)",
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def _date_bounds(frame: pd.DataFrame) -> tuple[str, str, str, str]:
    first = pd.Timestamp(frame["timestamp"].min()).tz_convert("UTC")
    last = pd.Timestamp(frame["timestamp"].max()).tz_convert("UTC")
    from_date = first.strftime("%Y.%m.%d")
    to_date = (last + timedelta(days=1)).strftime("%Y.%m.%d")
    return first.strftime("%Y.%m.%d %H:%M:%S"), last.strftime("%Y.%m.%d %H:%M:%S"), from_date, to_date


def _load_features() -> list[str]:
    schema = _read_json(ia.hz.FEATURE_SCHEMA)
    return [str(feature) for feature in schema["features"]]


def _inner_holdout_unique_frame(features: Sequence[str]) -> pd.DataFrame:
    frame = pd.read_parquet(aw.io_path(ia.hz.hy.hx.HX_INPUT_FRAME)).copy()
    positive = _read_csv(ia.POSITIVE_MATRIX)
    best_target = str(positive.iloc[0]["target_column"])
    valid_col = "hx_valid_fwd18" if best_target.endswith("fwd18") else "hx_valid_fwd6"
    task_frame = frame.loc[(frame[valid_col] == 1) & (frame[best_target] != -1)].copy()
    _inner_train, inner_holdout = ia.hz._split_inner(task_frame)
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


def _materialize_feature_matrix(frame: pd.DataFrame, features: Sequence[str]) -> tuple[pd.DataFrame, list[str], list[dict]]:
    header = ["timestamp", *features]
    hashes: list[str] = []
    formatted_values: list[list[float]] = []
    with aw.io_path(FEATURE_MATRIX).open("w", encoding="utf-8", newline="") as handle:
        handle.write(",".join(header) + "\n")
        for _, row in frame.iterrows():
            timestamp = _csv_timestamp(row["timestamp"])
            value_text = [_format_feature_value(row[feature]) for feature in features]
            line = ",".join([timestamp, *value_text])
            handle.write(line + "\n")
            hashes.append(_fnv1a_mql_hash(line))
            formatted_values.append([float(item) for item in value_text])
    values = pd.DataFrame(formatted_values, columns=list(features), dtype="float32")
    values.insert(0, "timestamp", [_csv_timestamp(value) for value in frame["timestamp"]])
    feature_common = f"{COMMON_FEATURE_DIR}/proxy_positive_inner_holdout_features.csv"
    sync_rows = [
        _copy_file(
            FEATURE_MATRIX,
            DEFAULT_COMMON_FILES / Path(feature_common),
            "common_feature_matrix",
            "Feature matrix(피처 행렬)를 Common Files(공용 파일)에 복사해 MT5 EA가 읽게 한다.",
        )
    ]
    return values, hashes, sync_rows


def _max_hold_from_target(target: str) -> int:
    if target.endswith("fwd6"):
        return 6
    if target.endswith("fwd24"):
        return 24
    return 18


def _attempt_name(index: int, model_id: str) -> str:
    return f"ib{index:02d}_{model_id}"


def _materialize_models_and_expected(
    values: pd.DataFrame,
    hashes: Sequence[str],
    features: Sequence[str],
    first_time: str,
    last_time: str,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, list[dict]]:
    manifest = _read_csv(ia.hz.TRAINED_MODEL_MANIFEST)
    model_lookup = {row["model_id"]: row for _, row in manifest.iterrows()}
    positive = _read_csv(ia.POSITIVE_MATRIX).head(2)
    matrix = values.loc[:, features].astype("float32").to_numpy()
    _first_source, _last_source, from_date, to_date = _date_bounds(
        pd.DataFrame({"timestamp": pd.to_datetime(values["timestamp"], format="%Y.%m.%d %H:%M:%S", utc=True)})
    )

    model_handoff: list[dict] = []
    expected_index: list[dict] = []
    expected_rows: list[dict] = []
    set_rows: list[dict] = []
    ini_rows: list[dict] = []
    attempts: list[dict] = []
    sync_rows: list[dict] = []
    labels = {0: "short", 1: "flat", 2: "long"}
    feature_common = f"{COMMON_FEATURE_DIR}/proxy_positive_inner_holdout_features.csv"

    for index, (_, candidate) in enumerate(positive.iterrows(), start=1):
        model_id = str(candidate["model_id"])
        model = model_lookup[model_id]
        task_id = str(model["task_id"])
        target_column = str(model["target_column"])
        attempt_name = _attempt_name(index, model_id)
        source_joblib = _repo_path(model["model_path"])
        source_onnx = _repo_path(model["onnx_path"])
        local_joblib = MODEL_COPY_DIR / f"{attempt_name}.joblib"
        local_onnx = MODEL_COPY_DIR / f"{attempt_name}.onnx"
        common_onnx = f"{COMMON_MODEL_DIR}/{attempt_name}.onnx"
        sync_rows.append(
            _copy_file(
                source_joblib,
                local_joblib,
                f"local_joblib::{attempt_name}",
                "joblib model(joblib 모델)을 패키지에 복사해 expected tape(예상 테이프)를 재현한다.",
            )
        )
        sync_rows.append(
            _copy_file(
                source_onnx,
                local_onnx,
                f"local_onnx::{attempt_name}",
                "ONNX model(ONNX 모델)을 패키지에 복사해 산출물 계보를 고정한다.",
            )
        )
        sync_rows.append(
            _copy_file(
                local_onnx,
                DEFAULT_COMMON_FILES / Path(common_onnx),
                f"common_onnx::{attempt_name}",
                "ONNX model(ONNX 모델)을 Common Files(공용 파일)에 복사해 MT5 EA가 읽게 한다.",
            )
        )

        payload = joblib.load(aw.io_path(local_joblib))
        fitted = payload["model"] if isinstance(payload, dict) and "model" in payload else payload
        probabilities = ordered_sklearn_probabilities(fitted, matrix, [0, 1, 2])
        row_sum = probabilities.sum(axis=1, keepdims=True)
        probabilities = np.divide(probabilities, row_sum, out=np.zeros_like(probabilities), where=row_sum != 0.0)
        predictions = np.asarray([0, 1, 2], dtype=int)[np.argmax(probabilities, axis=1)]
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
                    "feature_input_hash": hashes[row_index],
                    "p_short": float(probabilities[row_index, 0]),
                    "p_flat": float(probabilities[row_index, 1]),
                    "p_long": float(probabilities[row_index, 2]),
                    "decision_class": decision_class,
                    "decision_label": labels[decision_class],
                    "allowed_use": "proxy-vs-MT5 runtime parity comparison(프록시-MT5 런타임 동등성 비교)",
                    "forbidden_use": "MT5 KPI substitute or operating selection(MT5 KPI 대체 또는 운영 선택)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
        row_count = len(expected_rows) - row_start

        set_name = f"ObsidianPrimeV2_RuntimeProbeEA_{attempt_name}.set"
        ini_name = f"ObsidianPrimeV2_RuntimeProbeEA_{attempt_name}.ini"
        set_path = SET_DIR / set_name
        ini_path = INI_DIR / ini_name
        report_name = f"Project_Obsidian_Prime_v2_{RUN_ID}_{attempt_name}"
        max_hold_bars = _max_hold_from_target(target_column)
        set_values = {
            "InpRunId": f"{RUN_ID}_{attempt_name}",
            "InpExplorationLabel": "stage337IB_ProxyPositiveOffensivePivot__MT5RuntimeProbe",
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
            "InpMagic": 3378100 + index,
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
            "InpTelemetryCsvPath": f"{COMMON_TELEMETRY_DIR}/{attempt_name}_telemetry.csv",
            "InpSummaryCsvPath": f"{COMMON_TELEMETRY_DIR}/{attempt_name}_summary.csv",
        }
        set_payload = mt5.materialize_tester_set_file(set_values, set_path, generated_by=aw.rel(Path(__file__)))
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
                "probe_priority": index,
                "source_model_path": model["model_path"],
                "source_model_sha256": model["model_sha256"],
                "local_model_path": aw.rel(local_joblib),
                "local_model_sha256": _sha(local_joblib),
                "source_onnx_path": model["onnx_path"],
                "source_onnx_sha256": model["onnx_sha256"],
                "local_onnx_path": aw.rel(local_onnx),
                "local_onnx_sha256": _sha(local_onnx),
                "common_onnx_path": common_onnx,
                "common_onnx_sha256": _sha(DEFAULT_COMMON_FILES / Path(common_onnx)),
                "feature_order_hash": model["feature_order_hash"],
                "class_order_json": model["class_order_json"],
                "handoff_status": "ready_for_mt5_probe(MT5 탐침 준비)",
                "effect": "Model, ONNX, and Common Files hashes are connected(모델/ONNX/공용 파일 해시 연결).",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        expected_index.append(
            {
                "expected_tape_id": f"expected::{attempt_name}",
                "model_id": model_id,
                "task_id": task_id,
                "attempt_name": attempt_name,
                "row_count": row_count,
                "first_source_time": first_time,
                "last_source_time": last_time,
                "path": aw.rel(EXPECTED_PROBABILITY_TAPE),
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
                "set_path": aw.rel(set_path),
                "set_sha256": set_payload["sha256"],
                "parameter_count": set_payload["parameter_count"],
                "decision_mode": "argmax_probe(최대확률 탐침)",
                "allow_trading": True,
                "fixed_lot": 0.10,
                "max_hold_bars": max_hold_bars,
                "no_optimization_rule": "fixed lot and fixed argmax probe; no threshold tuning(고정 랏/고정 argmax, 임계값 조정 없음)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        tester_values = ini_payload["tester"]
        ini_rows.append(
            {
                "attempt_name": attempt_name,
                "model_id": model_id,
                "ini_path": aw.rel(ini_path),
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
                "probe_priority": index,
                "model_id": model_id,
                "task_id": task_id,
                "feature_set_id": model.get("feature_set_id", ""),
                "feature_count": len(features),
                "feature_order_hash": model["feature_order_hash"],
                "feature_local_path": aw.rel(FEATURE_MATRIX),
                "feature_common_path": feature_common,
                "model_local_path": aw.rel(local_onnx),
                "model_common_path": common_onnx,
                "expected_tape_path": aw.rel(EXPECTED_PROBABILITY_TAPE),
                "common_telemetry_path": f"{COMMON_TELEMETRY_DIR}/{attempt_name}_telemetry.csv",
                "common_summary_path": f"{COMMON_TELEMETRY_DIR}/{attempt_name}_summary.csv",
                "set_path": aw.rel(set_path),
                "set_name": set_name,
                "ini_path": aw.rel(ini_path),
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
                "known_proxy_runtime_difference": "proxy score used replicated cost policies; MT5 uses one broker execution path(프록시 점수는 비용 정책 복제를 사용, MT5는 브로커 실행 경로 1개 사용)",
                "forbidden_action": "treat package priority as selection or promotion(패키지 우선순위를 선택/승격으로 취급)",
                "effect": "Attempt can be executed without changing model logic(모델 로직 변경 없이 실행 가능).",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    expected_frame = pd.DataFrame(expected_rows)
    _write_csv(EXPECTED_PROBABILITY_TAPE, expected_frame)
    expected_sha = _sha(EXPECTED_PROBABILITY_TAPE)
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


def _contracts_and_queue() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    tester = pd.DataFrame(
        [
            {
                "contract_id": "tester_identity",
                "subject": "MT5 Strategy Tester(MT5 전략 테스터)",
                "requirement": "US100 M5, fixed lot, fixed argmax, no optimization(US100 M5, 고정 랏, 고정 argmax, 최적화 없음)",
                "evidence_path": aw.rel(TESTER_INI_MANIFEST),
                "known_difference": "package only; actual broker costs must be read from tester output(패키지 전용, 실제 브로커 비용은 테스터 출력에서 확인)",
                "blocked_if_missing": "tester report, settings, trade list(테스터 보고서, 설정, 거래 목록)",
                "forbidden_action": "trust KPI without tester identity(테스터 정체성 없이 KPI 신뢰)",
                "effect": "Backtest evidence can be audited after execution(실행 후 백테스트 근거 감사 가능).",
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
                "evidence_path": aw.rel(EXPECTED_PROBABILITY_TAPE),
                "known_difference": "proxy is unique-row probability tape; MT5 is lifecycle execution(프록시는 고유 행 확률 테이프, MT5는 생명주기 실행)",
                "blocked_if_missing": "runtime telemetry or expected tape(런타임 기록 또는 예상 테이프)",
                "forbidden_action": "use proxy net as MT5 profit(프록시 순익을 MT5 수익으로 사용)",
                "effect": "Proxy is converted into a comparison baseline(프록시를 비교 기준선으로 바꿈).",
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
                "evidence_path": f"{aw.rel(FEATURE_MATRIX)};{aw.rel(MODEL_HANDOFF_MANIFEST)}",
                "known_difference": "MT5 reads Common Files; Python reads repo artifacts(MT5는 공용 파일, Python은 저장소 산출물 읽음)",
                "blocked_if_missing": "Common Files handoff or telemetry(공용 파일 인계 또는 런타임 기록)",
                "forbidden_action": "runtime authority from package only(패키지만으로 런타임 권위 주장)",
                "effect": "IC can test runtime parity row by row(IC가 행 단위 런타임 동등성 시험 가능).",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    queue = pd.DataFrame(
        [
            {
                "queue_id": "ic_execute_proxy_positive_offensive_pivot_mt5_runtime_probe",
                "next_run_id": NEXT_RUN_ID,
                "priority": "P0",
                "task": "execute MT5 runtime probe for two proxy-positive ONNX candidates(프록시 양수 ONNX 후보 2개 MT5 런타임 탐침 실행)",
                "required_inputs": f"{aw.rel(RUNTIME_PROBE_ATTEMPT_PACKAGE)};{aw.rel(EXPECTED_PROBABILITY_TAPE)};{aw.rel(COMMON_FILES_SYNC)}",
                "required_outputs": "runtime telemetry, tester reports, proxy-vs-MT5 diff, backtest forensic receipt(런타임 기록, 테스터 보고서, 프록시-MT5 차이, 백테스트 포렌식 영수증)",
                "blocked_if_missing": "terminal, broker visibility, tester output, telemetry(터미널, 브로커 가시성, 테스터 출력, 런타임 기록)",
                "forbidden_action": "Forward/Goal claim before MT5 evidence(MT5 근거 전 전진/목표 주장)",
                "effect": "Package is handed to execution without changing thresholds or lots(임계값/랏 변경 없이 패키지를 실행으로 넘김).",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    return tester, proxy, runtime, queue


def _include_hashes() -> dict[str, str]:
    return {aw.rel(path): _sha(path) for path in [EA_SOURCE, *sorted(EA_INCLUDE_DIR.glob("*.mqh"))] if _path_exists(path)}


def _materialize_package() -> tuple[dict, list[Path]]:
    features = _load_features()
    frame = _inner_holdout_unique_frame(features)
    first_source, last_source, from_date, to_date = _date_bounds(frame)
    values, hashes, sync_rows = _materialize_feature_matrix(frame, features)
    model_handoff, expected_index, expected_rows, set_rows, ini_rows, attempts, model_sync = _materialize_models_and_expected(
        values,
        hashes,
        features,
        first_source,
        last_source,
    )
    sync_rows.extend(model_sync)
    tester, proxy, runtime, queue = _contracts_and_queue()
    feature_common = f"{COMMON_FEATURE_DIR}/proxy_positive_inner_holdout_features.csv"
    feature_manifest = pd.DataFrame(
        [
            {
                "feature_matrix_id": "proxy_positive_inner_holdout_features",
                "feature_set_id": ia.hz.FEATURE_SET_ID,
                "feature_count": len(features),
                "row_count": len(frame),
                "first_source_time": first_source,
                "last_source_time": last_source,
                "feature_order_hash": _read_json(ia.hz.FEATURE_SCHEMA).get("feature_order_hash", ""),
                "local_path": aw.rel(FEATURE_MATRIX),
                "local_sha256": _sha(FEATURE_MATRIX),
                "common_path": feature_common,
                "common_sha256": _sha(DEFAULT_COMMON_FILES / Path(feature_common)),
                "timestamp_semantics": "bar close timestamp, InpCsvTimestampIsBarClose=true(봉 마감 시각)",
                "effect": "MT5 can request closed-bar features by exact timestamp(MT5가 정확한 시각으로 마감봉 피처 요청 가능).",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    _write_csv(FEATURE_MATRIX_MANIFEST, feature_manifest)
    _write_csv(EXPECTED_PROBABILITY_INDEX, expected_index)
    _write_csv(MODEL_HANDOFF_MANIFEST, model_handoff)
    _write_csv(COMMON_FILES_SYNC, pd.DataFrame(sync_rows))
    _write_csv(TESTER_SET_MANIFEST, set_rows)
    _write_csv(TESTER_INI_MANIFEST, ini_rows)
    _write_csv(RUNTIME_PROBE_ATTEMPT_PACKAGE, attempts)
    _write_csv(TESTER_IDENTITY_CONTRACT, tester)
    _write_csv(PROXY_MT5_COMPARISON_CONTRACT, proxy)
    _write_csv(RUNTIME_PARITY_CONTRACT, runtime)
    _write_csv(EXECUTION_QUEUE, queue)
    summary = {
        "feature_count": len(features),
        "feature_matrix_rows": int(len(frame)),
        "first_source_time": first_source,
        "last_source_time": last_source,
        "tester_from_date": from_date,
        "tester_to_date": to_date,
        "expected_probability_rows": int(len(expected_rows)),
        "attempt_rows": int(len(attempts)),
        "model_handoff_rows": int(len(model_handoff)),
        "common_sync_rows": int(len(sync_rows)),
        "common_sync_ready_rows": int(sum(1 for row in sync_rows if row.get("exists") is True)),
        "tester_set_rows": int(len(set_rows)),
        "tester_ini_rows": int(len(ini_rows)),
        "execution_queue_rows": int(len(queue)),
        "terminal_exists": _path_exists(DEFAULT_TERMINAL),
        "metaeditor_exists": _path_exists(DEFAULT_METAEDITOR),
        "common_files_root_exists": _path_exists(DEFAULT_COMMON_FILES),
        "ea_source_exists": _path_exists(EA_SOURCE),
        "ea_binary_exists": _path_exists(EA_BINARY),
        "portable_ea_exists": _path_exists(PORTABLE_EA_EX5),
        "ea_source_sha256": _sha(EA_SOURCE) if _path_exists(EA_SOURCE) else "",
        "ea_binary_sha256": _sha(EA_BINARY) if _path_exists(EA_BINARY) else "",
        "portable_ea_sha256": _sha(PORTABLE_EA_EX5) if _path_exists(PORTABLE_EA_EX5) else "",
        "include_module_hashes": _include_hashes(),
    }
    artifacts = [
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
    ]
    return summary, artifacts


def _gate_row(gate: str, status: str, evidence: str, effect: str) -> dict:
    return {
        "gate": gate,
        "status": status,
        "evidence": evidence,
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def _make_gates(summary: dict) -> pd.DataFrame:
    ia_gates = _read_csv(ia.GATE_AUDIT)
    gates = [
        _gate_row(
            "parent_ia_gates_passed",
            "pass" if ia_gates["status"].astype(str).str.lower().isin(["pass", "passed"]).all() else "fail",
            aw.rel(ia.GATE_AUDIT),
            "IB starts only after IA review passed.",
        ),
        _gate_row(
            "positive_candidates_packaged",
            "pass" if summary["attempt_rows"] == 2 and summary["model_handoff_rows"] == 2 else "fail",
            aw.rel(MODEL_HANDOFF_MANIFEST),
            "Two proxy-positive candidates are packaged for MT5.",
        ),
        _gate_row(
            "unique_feature_matrix_materialized",
            "pass" if summary["feature_matrix_rows"] > 1000 and _path_exists(FEATURE_MATRIX) else "fail",
            aw.rel(FEATURE_MATRIX),
            "Runtime feature matrix uses unique source rows.",
        ),
        _gate_row(
            "expected_probability_tape_materialized",
            "pass" if summary["expected_probability_rows"] == summary["feature_matrix_rows"] * summary["attempt_rows"] else "fail",
            aw.rel(EXPECTED_PROBABILITY_TAPE),
            "Python expected probability tape is ready for MT5 diff.",
        ),
        _gate_row(
            "common_files_handoff_complete",
            "pass" if summary["common_sync_ready_rows"] == summary["common_sync_rows"] else "fail",
            aw.rel(COMMON_FILES_SYNC),
            "Feature and ONNX files are copied to Common Files.",
        ),
        _gate_row(
            "tester_files_materialized",
            "pass" if summary["tester_set_rows"] == summary["tester_ini_rows"] == summary["attempt_rows"] else "fail",
            f"{aw.rel(TESTER_SET_MANIFEST)};{aw.rel(TESTER_INI_MANIFEST)}",
            "Each attempt has tester set and ini files.",
        ),
        _gate_row(
            "execution_environment_visibility_recorded",
            "pass",
            aw.rel(RUNTIME_RECEIPT),
            "Terminal, MetaEditor, Common Files, and EA visibility are recorded.",
        ),
        _gate_row(
            "next_execution_queue_opened",
            "pass" if summary["execution_queue_rows"] == 1 else "fail",
            aw.rel(EXECUTION_QUEUE),
            "IC execution is queued after package materialization.",
        ),
        _gate_row(
            "no_forbidden_operating_claim",
            "pass",
            aw.rel(CLAIM_BOUNDARY_RECEIPT),
            "IB does not claim MT5 success, runtime authority, operating promotion, or Goal achievement.",
        ),
        _gate_row(
            "required_gate_coverage_audit_written",
            "pass",
            aw.rel(GATE_AUDIT),
            "Gate coverage is recorded for closeout.",
        ),
    ]
    return pd.DataFrame(gates)


def _append_or_replace_csv(path: Path, key_columns: Iterable[str], row: dict) -> None:
    if path.exists():
        frame = _read_csv(path)
    else:
        frame = pd.DataFrame()
    for column in row:
        if column not in frame.columns:
            frame[column] = ""
    if frame.empty:
        frame = pd.DataFrame(columns=list(row.keys()))
    mask = pd.Series(False, index=frame.index)
    for idx, key in enumerate(key_columns):
        current = frame[key].astype(str).eq(str(row[key])) if key in frame.columns else False
        mask = current if idx == 0 else mask & current
    frame = frame.loc[~mask].copy()
    frame = pd.concat([frame, pd.DataFrame([row])], ignore_index=True)
    ordered = list(dict.fromkeys(list(frame.columns) + list(row.keys())))
    _write_csv(path, frame[ordered])


def _artifact_paths() -> list[Path]:
    return [
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
        CLAIM_BOUNDARY_RECEIPT,
        GATE_AUDIT,
        FINAL_DECISION,
        RUN_MANIFEST,
        REPORT_PATH,
        DECISION_DOC,
    ]


def _update_artifact_registry(paths: list[Path]) -> None:
    if ARTIFACT_REGISTRY.exists():
        registry = pd.read_csv(aw.io_path(ARTIFACT_REGISTRY))
    else:
        registry = pd.DataFrame()
    required = ["stage_id", "run_id", "artifact_type", "path", "sha256", "created_at", "claim_boundary"]
    for column in required:
        if column not in registry.columns:
            registry[column] = ""
    rows = []
    for path in paths + list(MODEL_COPY_DIR.glob("*")):
        if path.exists():
            rows.append(
                {
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "artifact_type": "report" if path.suffix.lower() == ".md" else path.suffix.lower().lstrip("."),
                    "path": aw.rel(path),
                    "sha256": _sha(path),
                    "created_at": TODAY,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    if rows:
        new_paths = {row["path"] for row in rows}
        registry = registry.loc[~registry["path"].astype(str).isin(new_paths)].copy()
        registry = pd.concat([registry, pd.DataFrame(rows)], ignore_index=True)
        columns = list(dict.fromkeys(required + list(registry.columns)))
        registry[columns].to_csv(
            aw.io_path(ARTIFACT_REGISTRY),
            index=False,
            encoding="utf-8-sig",
            lineterminator="\n",
        )


def _write_receipts(summary: dict, gates: pd.DataFrame) -> None:
    _write_json(
        ROUTING_RECEIPT,
        {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "effect": "Package routes proxy-positive candidates to MT5 execution.",
        },
    )
    _write_json(
        DATA_RECEIPT,
        {
            "run_id": RUN_ID,
            "feature_matrix_rows": summary["feature_matrix_rows"],
            "feature_count": summary["feature_count"],
            "first_source_time": summary["first_source_time"],
            "last_source_time": summary["last_source_time"],
            "tier_scope": "Tier A unique-row runtime package; Tier B missing_required",
        },
    )
    _write_json(
        MODEL_RECEIPT,
        {
            "run_id": RUN_ID,
            "attempt_rows": summary["attempt_rows"],
            "model_handoff_rows": summary["model_handoff_rows"],
            "effect": "ONNX candidates are copied and hash-anchored for MT5.",
        },
    )
    _write_json(
        RUNTIME_RECEIPT,
        {
            "run_id": RUN_ID,
            "terminal_exists": summary["terminal_exists"],
            "metaeditor_exists": summary["metaeditor_exists"],
            "common_files_root_exists": summary["common_files_root_exists"],
            "ea_source_exists": summary["ea_source_exists"],
            "ea_binary_exists": summary["ea_binary_exists"],
            "portable_ea_exists": summary["portable_ea_exists"],
            "tester_profile_root": str(DEFAULT_TESTER_PROFILE_ROOT),
            "effect": "Execution environment visibility is recorded before IC attempt.",
        },
    )
    _write_json(
        FORENSICS_RECEIPT,
        {
            "run_id": RUN_ID,
            "tester_identity_contract": aw.rel(TESTER_IDENTITY_CONTRACT),
            "mt5_execution": "not_run_in_IB",
            "effect": "Backtest forensics requirements are prepared before execution.",
        },
    )
    _write_json(
        PERFORMANCE_RECEIPT,
        {
            "run_id": RUN_ID,
            "mt5_kpi": "not_measured",
            "expected_probability_rows": summary["expected_probability_rows"],
            "effect": "Performance comparison is deferred only to queued IC execution attempt.",
        },
    )
    _write_json(
        JUDGMENT_RECEIPT,
        {
            "run_id": RUN_ID,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "next_run_id": NEXT_RUN_ID,
            "gate_passes": int(gates["status"].astype(str).eq("pass").sum()),
            "gate_total": int(len(gates)),
        },
    )
    _write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "model_handoff_manifest": aw.rel(MODEL_HANDOFF_MANIFEST),
            "common_files_sync": aw.rel(COMMON_FILES_SYNC),
            "include_module_hashes": summary["include_module_hashes"],
            "artifact_registry_updated": True,
        },
    )
    _write_json(
        CLAIM_BOUNDARY_RECEIPT,
        {
            "run_id": RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
            "mt5_execution": "not_run_in_IB",
            "candidate_selection": "not_run",
            "goal_achieve_claim": "not_claimed",
            "runtime_authority_claim": "not_claimed",
            "operating_promotion_claim": "not_claimed",
            "live_readiness_claim": "not_claimed",
        },
    )


def _write_final(summary: dict, gates: pd.DataFrame) -> None:
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "candidate_selection": "not_run",
        "mt5_execution": "not_run_in_IB",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "gate_passes": int(gates["status"].astype(str).eq("pass").sum()),
        "gate_total": int(len(gates)),
        "claim_boundary": CLAIM_BOUNDARY,
        **summary,
    }
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at": TODAY,
        "script": aw.rel(Path(__file__)),
        "inputs": [
            aw.rel(ia.FINAL_DECISION),
            aw.rel(ia.GATE_AUDIT),
            aw.rel(ia.POSITIVE_MATRIX),
            aw.rel(ia.hz.TRAINED_MODEL_MANIFEST),
            aw.rel(ia.hz.FEATURE_SCHEMA),
        ],
        "outputs": [aw.rel(path) for path in _artifact_paths() if path.exists()],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    _write_json(FINAL_DECISION, final)
    _write_json(RUN_MANIFEST, manifest)


def _write_docs(summary: dict, gates: pd.DataFrame) -> None:
    gate_passes = int(gates["status"].astype(str).eq("pass").sum())
    gate_total = int(len(gates))
    report = f"""﻿# Stage 337IB Proxy-Positive Runtime Probe Package

## Summary

- run_id: `{RUN_ID}`
- parent_run_id: `{PARENT_RUN_ID}`
- judgment: `{JUDGMENT}`
- gates: `{gate_passes}/{gate_total}`
- attempts(시도): `{summary['attempt_rows']}`
- feature_matrix_rows(피처 행): `{summary['feature_matrix_rows']}`
- expected_probability_rows(예상 확률 행): `{summary['expected_probability_rows']}`
- terminal_exists(터미널 존재): `{summary['terminal_exists']}`

## Result

IB materialized(물질화) MT5 runtime probe package(MT5 런타임 탐침 패키지) for two proxy-positive ONNX candidates(프록시 양수 ONNX 후보 2개).
Effect(효과): IC can attempt(시도) MT5 execution(MT5 실행) without changing model logic(모델 로직).

## Boundary

No MT5 execution in IB(IB에서 MT5 실행 없음), no candidate selection(후보 선택 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).

## Next

Open `{NEXT_RUN_ID}` to run MT5 Strategy Tester(MT5 전략 테스터) and compare proxy expected value(프록시 예상값) with runtime evidence(런타임 근거).
"""
    decision = f"""﻿# Decision: Stage 337IB Runtime Probe Package

- date: `{TODAY}`
- run_id: `{RUN_ID}`
- decision: `{DECISION}`
- judgment: `{JUDGMENT}`
- next_run_id: `{NEXT_RUN_ID}`

## Reason

IA review(검토)는 proxy-positive(프록시 양수) ONNX candidates(ONNX 후보)를 확인했고, proxy expected value(프록시 예상값)는 MT5 runtime probe(MT5 런타임 탐침)와 비교해야 한다.

## Effect

IB package(패키지)는 feature matrix(피처 행렬), ONNX handoff(ONNX 인계), expected tape(예상 테이프), tester set/ini(테스터 설정)를 고정해 IC 실행 시도를 가능하게 한다.

## Boundary

`{CLAIM_BOUNDARY}`
"""
    _write_bom_text(REPORT_PATH, report)
    _write_bom_text(DECISION_DOC, decision)
    _write_bom_text(
        WORKSPACE_STATE,
        f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
current_decision: {DECISION}
next_run_id: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
""",
    )
    _write_bom_text(
        CURRENT_WORKING_STATE,
        f"""﻿# Current Working State

## Current Truth

- active_stage: `{STAGE_ID}`
- latest_completed_run: `{RUN_ID}`
- current_run: `{NEXT_RUN_ID}`
- status: `{STATUS}`
- judgment: `{JUDGMENT}`
- decision: `{DECISION}`

## Effect

IB package(패키지)는 proxy-positive(프록시 양수) 후보를 MT5 runtime probe(MT5 런타임 탐침) 실행 입력으로 바꿨다.
효과는 IC가 외부 MT5 비교를 시도할 수 있게 하는 것이다.

## Claim Boundary

`{CLAIM_BOUNDARY}`
""",
    )
    _write_bom_text(
        SELECTION_STATUS,
        f"""﻿# Selection Status

- latest_run: `{RUN_ID}`
- current_run: `{NEXT_RUN_ID}`
- model_selection: not_selected
- runtime_package: materialized_not_authoritative
- mt5_execution: queued
- goal_achieve: not_claimed
- operating_promotion: not_claimed
- live_readiness: not_claimed

효과는 runtime package(런타임 패키지)를 selected model(선택 모델)이나 runtime authority(런타임 권위)로 오해하지 않게 하는 것이다.
""",
    )
    _write_bom_text(
        STAGE_BRIEF,
        f"""﻿# {STAGE_ID}

Latest completed run: `{RUN_ID}`

IB materialized(물질화) runtime probe package(런타임 탐침 패키지) for `{summary['attempt_rows']}` proxy-positive ONNX candidates(프록시 양수 ONNX 후보).
Next(다음): `{NEXT_RUN_ID}` MT5 execution attempt(MT5 실행 시도).
""",
    )
    existing = aw.io_path(CHANGELOG).read_text(encoding="utf-8-sig") if CHANGELOG.exists() else "﻿# Changelog\n"
    entry = (
        f"\n## {TODAY} - {RUN_ID}\n\n"
        f"- Materialized(물질화) MT5 runtime probe package(런타임 탐침 패키지) for `{summary['attempt_rows']}` proxy-positive candidates(프록시 양수 후보).\n"
        f"- Queued(대기열 등록) IC MT5 execution attempt(MT5 실행 시도).\n"
    )
    _write_bom_text(CHANGELOG, existing.rstrip() + "\n" + entry)


def _update_ledgers(summary: dict, gates: pd.DataFrame) -> None:
    row = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "attempt_rows": summary["attempt_rows"],
        "feature_matrix_rows": summary["feature_matrix_rows"],
        "gate_passes": int(gates["status"].astype(str).eq("pass").sum()),
        "gate_total": int(len(gates)),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": aw.rel(REPORT_PATH),
    }
    _append_or_replace_csv(RUN_REGISTRY, ["run_id"], row)
    _append_or_replace_csv(PROJECT_LEDGER, ["run_id"], row)
    _append_or_replace_csv(STAGE_LEDGER, ["run_id"], row)


def main() -> None:
    _ensure_dirs()
    summary, _artifacts = _materialize_package()
    gates = _make_gates(summary)
    _write_csv(GATE_AUDIT, gates)
    _write_receipts(summary, gates)
    _write_final(summary, gates)
    _write_docs(summary, gates)
    _update_ledgers(summary, gates)
    _update_artifact_registry(_artifact_paths())

    failed = gates.loc[~gates["status"].astype(str).eq("pass")]
    if not failed.empty:
        raise RuntimeError(f"IB gates failed: {failed[['gate', 'status']].to_dict(orient='records')}")

    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "attempt_rows": summary["attempt_rows"],
                "feature_matrix_rows": summary["feature_matrix_rows"],
                "expected_probability_rows": summary["expected_probability_rows"],
                "common_sync": f"{summary['common_sync_ready_rows']}/{summary['common_sync_rows']}",
                "terminal_exists": summary["terminal_exists"],
                "portable_ea_exists": summary["portable_ea_exists"],
                "gate_passes": int(gates["status"].astype(str).eq("pass").sum()),
                "gate_total": int(len(gates)),
                "next_run_id": NEXT_RUN_ID,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
