from __future__ import annotations

import csv
import json
import math
import shutil
import sys
from datetime import timedelta, UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.models.onnx_bridge import ordered_hash  # noqa: E402
from foundation.mt5 import runtime_support as mt5  # noqa: E402
from stage_pipelines.stage338 import review_group_safe_onnx_proxy_scores_for_mt5_probe_without_db as rv  # noqa: E402


aw = rv.aw

TODAY = "2026-06-01"
STAGE_ID = rv.STAGE_ID
STAGE_DIR = rv.STAGE_DIR
RUN_NUMBER = "run338G"
RUN_ID = "run338G_materialize_runtime_collapsed_onnx_mt5_probe_package_without_db_v1"
PARENT_RUN_ID = rv.RUN_ID
NEXT_RUN_ID = "run338H_execute_runtime_collapsed_onnx_mt5_probe_without_db_v1"
STATUS = "completed_stage338G_runtime_collapsed_onnx_mt5_probe_package_materialized_no_mt5_execution"
JUDGMENT = "mt5_runtime_probe_package_ready_proxy_mt5_comparison_required_no_selection"
DECISION = "stage338G_open_run338H_execute_runtime_collapsed_onnx_mt5_probe"
CLAIM_BOUNDARY = (
    "research_development_runtime_probe_package_only_no_mt5_execution_no_candidate_selection_"
    "no_forward_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MT5_DIR = RUN_DIR / "mt5"
SET_DIR = MT5_DIR / "sets"
INI_DIR = MT5_DIR / "inis"
MODEL_DIR = RUN_DIR / "models"
FEATURE_DIR = RUN_DIR / "feature_matrices"
EXPECTED_DIR = RUN_DIR / "expected_probability_tapes"
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run338G_runtime_collapsed_mt5_probe_package.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage338G_runtime_collapsed_mt5_probe_package.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_README = STAGE_DIR / "README.md"
STAGE_LEDGER = STAGE_DIR / "03_reviews" / "stage_run_ledger.csv"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
ROOT_CHANGELOG = ROOT / "CHANGELOG.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

DEFAULT_PORTABLE_ROOT = Path("C:/Users/awdse/AppData/Local/ObsidianPrime/mt5_portable_run329E")
DEFAULT_TERMINAL = DEFAULT_PORTABLE_ROOT / "terminal64.exe"
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

COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage338/{RUN_NUMBER}_runtime_collapsed_onnx_mt5_probe"
COMMON_FEATURE_DIR = f"{COMMON_ROOT}/features"
COMMON_MODEL_DIR = f"{COMMON_ROOT}/models"
COMMON_TELEMETRY_DIR = f"{COMMON_ROOT}/telemetry"

FEATURE_MATRIX = FEATURE_DIR / "runtime_collapsed_holdout_features.csv"
FEATURE_MATRIX_MANIFEST = RUN_DIR / "runtime_feature_matrix_manifest.csv"
EXPECTED_PROBABILITY_TAPE = EXPECTED_DIR / "runtime_collapsed_expected_probability_tape.csv"
EXPECTED_PROBABILITY_INDEX = RUN_DIR / "expected_probability_tape_index.csv"
MODEL_HANDOFF_MANIFEST = RUN_DIR / "model_handoff_manifest.csv"
COMMON_FILES_SYNC = RUN_DIR / "common_files_sync.csv"
TESTER_SET_MANIFEST = RUN_DIR / "tester_set_manifest.csv"
TESTER_INI_MANIFEST = RUN_DIR / "tester_ini_manifest.csv"
RUNTIME_PROBE_ATTEMPT_PACKAGE = RUN_DIR / "runtime_probe_attempt_package.csv"
TESTER_IDENTITY_CONTRACT = RUN_DIR / "tester_identity_contract.csv"
PROXY_MT5_COMPARISON_CONTRACT = RUN_DIR / "proxy_mt5_comparison_contract.csv"
RUNTIME_PARITY_CONTRACT = RUN_DIR / "runtime_parity_contract.csv"
RUN338H_EXECUTION_QUEUE = RUN_DIR / "run338H_execution_queue.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
FORENSICS_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    rv.FINAL_DECISION,
    rv.RUN338G_PACKAGE_QUEUE,
    rv.COLLAPSED_PREDICTION_TAPE,
    rv.COLLAPSED_RUNTIME_PROXY,
    rv.tr.FEATURE_ORDER,
    rv.tr.ONNX_PARITY_AUDIT,
    rv.tr.rv.TRAINING_FEATURE_SCHEMA,
    rv.tr.rv.GROUP_SAFE_SPLIT_ASSIGNMENT,
    rv.tr.rv.mat.INPUT_FRAME,
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
    RUN338H_EXECUTION_QUEUE,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    RUNTIME_RECEIPT,
    FORENSICS_RECEIPT,
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
    STAGE_README,
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


def io(path: Path | str) -> Path:
    return aw.io_path(path)


def rel(path: Path | str) -> str:
    return aw.rel(path)


def exists(path: Path | str) -> bool:
    return io(path).exists()


def ensure_parent(path: Path) -> None:
    io(path.parent).mkdir(parents=True, exist_ok=True)


def read_csv(path: Path) -> pd.DataFrame:
    return rv.read_csv(path)


def read_json(path: Path) -> Any:
    return rv.read_json(path)


def write_csv(path: Path, frame: pd.DataFrame) -> Path:
    return rv.write_csv(path, frame)


def write_json(path: Path, payload: Any) -> Path:
    return rv.write_json(path, payload)


def write_bom_text(path: Path, text: str) -> Path:
    return rv.write_bom_text(path, text)


def append_text_once(path: Path, marker: str, text: str) -> None:
    rv.append_text_once(path, marker, text)


def append_or_replace_csv(path: Path, key_columns: Sequence[str], row: Mapping[str, Any]) -> None:
    rv.append_or_replace_csv(path, key_columns, row)


def sha(path: Path) -> str:
    return aw.sha256_file(path)


def display_path(path: Path | str) -> str:
    return rv.display_path(path)


def passed_status(series: pd.Series) -> pd.Series:
    return rv.passed_status(series)


def repo_path(value: str) -> Path:
    path = Path(str(value))
    return path if path.is_absolute() else ROOT / path


def csv_timestamp(value: object) -> str:
    return pd.Timestamp(value).tz_convert("UTC").strftime("%Y.%m.%d %H:%M:%S")


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
        "source_path": rel(source) if str(source).lower().startswith(str(ROOT).lower()) else source.as_posix(),
        "target_path": rel(target) if str(target).lower().startswith(str(ROOT).lower()) else target.as_posix(),
        "exists": exists(target),
        "sha256": sha(target) if exists(target) else "",
        "status": "synced(동기화됨)" if exists(target) else "missing(누락)",
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def date_bounds(frame: pd.DataFrame) -> tuple[str, str, str, str]:
    first = pd.Timestamp(frame["timestamp"].min()).tz_convert("UTC")
    last = pd.Timestamp(frame["timestamp"].max()).tz_convert("UTC")
    from_date = first.strftime("%Y.%m.%d")
    to_date = (last + timedelta(days=1)).strftime("%Y.%m.%d")
    return first.strftime("%Y.%m.%d %H:%M:%S"), last.strftime("%Y.%m.%d %H:%M:%S"), from_date, to_date


def attempt_name(model_id: str, min_prob: float, min_margin: float) -> str:
    return f"g01_{model_id}_p{int(round(min_prob * 100)):02d}_m{int(round(min_margin * 100)):02d}"


def load_runtime_collapsed_feature_frame(feature_names: Sequence[str]) -> pd.DataFrame:
    frame, _feature_names = rv.tr.load_training_frame()
    if list(feature_names) != list(_feature_names):
        raise RuntimeError("feature order mismatch between run338E and training frame")
    valid = pd.to_numeric(frame[rv.tr.PRIMARY_LABEL], errors="coerce").fillna(-1).astype(int).ne(-1)
    holdout = frame.loc[frame["run338D_group_safe_split"].astype(str).eq("inner_holdout") & valid].copy()
    holdout = holdout.sort_values(["timestamp", "source_row_id"]).reset_index(drop=True)
    collapsed = holdout.drop_duplicates("timestamp", keep="last").copy().reset_index(drop=True)
    tape = pd.read_parquet(str(io(rv.COLLAPSED_PREDICTION_TAPE))).sort_values(["timestamp", "source_row_id"]).reset_index(drop=True)
    if len(collapsed) != len(tape):
        raise RuntimeError(f"collapsed feature/tape row mismatch: {len(collapsed)} != {len(tape)}")
    same_time = pd.to_datetime(collapsed["timestamp"], utc=True, errors="coerce").eq(
        pd.to_datetime(tape["timestamp"], utc=True, errors="coerce")
    )
    same_source = collapsed["source_row_id"].astype(str).eq(tape["source_row_id"].astype(str))
    if not bool((same_time & same_source).all()):
        raise RuntimeError("collapsed feature/tape identity mismatch")
    for column in tape.columns:
        if column not in collapsed.columns:
            collapsed[column] = tape[column].to_numpy()
    return collapsed


def write_feature_matrix(frame: pd.DataFrame, feature_names: Sequence[str]) -> tuple[list[str], pd.DataFrame]:
    ensure_parent(FEATURE_MATRIX)
    header = ["timestamp", *feature_names]
    hashes: list[str] = []
    with io(FEATURE_MATRIX).open("w", encoding="utf-8", newline="") as handle:
        handle.write(",".join(header) + "\n")
        for _, row in frame.iterrows():
            timestamp = csv_timestamp(row["timestamp"])
            values = [format_feature_value(row[feature]) for feature in feature_names]
            line = ",".join([timestamp, *values])
            handle.write(line + "\n")
            hashes.append(fnv1a_mql_hash(line))
    manifest = pd.DataFrame(
        [
            {
                "matrix_id": "runtime_collapsed_holdout_features",
                "path": rel(FEATURE_MATRIX),
                "rows": int(len(frame)),
                "feature_count": int(len(feature_names)),
                "first_timestamp": csv_timestamp(frame["timestamp"].iloc[0]),
                "last_timestamp": csv_timestamp(frame["timestamp"].iloc[-1]),
                "feature_order_hash": ordered_hash(feature_names),
                "sha256": sha(FEATURE_MATRIX),
                "timestamp_semantics": "bar close timestamp, InpCsvTimestampIsBarClose=true(봉 마감 시각)",
                "effect": "MT5 EA(메타트레이더5 전문가 자문)가 Python(파이썬)과 같은 feature(피처) 행을 읽게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    write_csv(FEATURE_MATRIX_MANIFEST, manifest)
    return hashes, manifest


def build_package() -> tuple[dict[str, Any], dict[str, pd.DataFrame], list[Path]]:
    parent_final = read_json(rv.FINAL_DECISION)
    parent_gates = read_csv(rv.GATE_AUDIT)
    queue = read_csv(rv.RUN338G_PACKAGE_QUEUE).iloc[0].to_dict()
    feature_order_frame = read_csv(rv.tr.FEATURE_ORDER)
    feature_names = feature_order_frame["feature_name"].astype(str).tolist()
    feature_hash = ordered_hash(feature_names)
    model_id = str(queue["model_id"])
    min_prob = float(queue["min_prob"])
    min_margin = float(queue["min_margin"])
    name = attempt_name(model_id, min_prob, min_margin)
    source_onnx = repo_path(str(queue["onnx_path"]))
    local_onnx = MODEL_DIR / f"{name}.onnx"
    common_onnx = f"{COMMON_MODEL_DIR}/{name}.onnx"
    feature_common = f"{COMMON_FEATURE_DIR}/runtime_collapsed_holdout_features.csv"
    frame = load_runtime_collapsed_feature_frame(feature_names)
    first_time, last_time, from_date, to_date = date_bounds(frame)
    hashes, feature_manifest = write_feature_matrix(frame, feature_names)
    sync_rows = [
        copy_file(
            FEATURE_MATRIX,
            DEFAULT_COMMON_FILES / Path(feature_common),
            "common_feature_matrix",
            "feature matrix(피처 행렬)를 Common Files(공용 파일)에 복사해 MT5 EA(전문가 자문)가 읽게 한다.",
        ),
        copy_file(
            source_onnx,
            local_onnx,
            f"local_onnx::{name}",
            "ONNX model(온엑스 모델)을 패키지에 복사해 산출물 hash(해시)를 고정한다.",
        ),
        copy_file(
            local_onnx,
            DEFAULT_COMMON_FILES / Path(common_onnx),
            f"common_onnx::{name}",
            "ONNX model(온엑스 모델)을 Common Files(공용 파일)에 복사해 MT5 EA(전문가 자문)가 읽게 한다.",
        ),
    ]

    labels = {0: "short", 1: "flat", 2: "long"}
    expected_rows: list[dict[str, Any]] = []
    p_short_col = f"{model_id}_proba_class_0"
    p_flat_col = f"{model_id}_proba_class_1"
    p_long_col = f"{model_id}_proba_class_2"
    for index, row in frame.iterrows():
        p_short = float(row[p_short_col])
        p_flat = float(row[p_flat_col])
        p_long = float(row[p_long_col])
        short_margin = p_short - max(p_flat, p_long)
        long_margin = p_long - max(p_flat, p_short)
        short_ok = p_short >= min_prob and short_margin >= min_margin
        long_ok = p_long >= min_prob and long_margin >= min_margin
        decision_class = 1
        if long_ok and (not short_ok or p_long >= p_short):
            decision_class = 2
        elif short_ok:
            decision_class = 0
        expected_rows.append(
            {
                "attempt_name": name,
                "model_id": model_id,
                "bar_time": csv_timestamp(row["timestamp"]),
                "source_time": csv_timestamp(row["timestamp"]),
                "source_row_id": row["source_row_id"],
                "feature_input_hash": hashes[index],
                "p_short": p_short,
                "p_flat": p_flat,
                "p_long": p_long,
                "decision_class": decision_class,
                "decision_label": labels[decision_class],
                "decision_mode": "threshold_margin(임계값/마진)",
                "short_threshold": min_prob,
                "long_threshold": min_prob,
                "min_margin": min_margin,
                "allowed_use": "proxy-vs-MT5 runtime parity comparison(프록시-MT5 런타임 동등성 비교)",
                "forbidden_use": "MT5 KPI substitute or operating selection(MT5 KPI 대체 또는 운영 선택)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    expected_frame = pd.DataFrame(expected_rows)
    write_csv(EXPECTED_PROBABILITY_TAPE, expected_frame)
    expected_index = pd.DataFrame(
        [
            {
                "expected_tape_id": f"expected::{name}",
                "model_id": model_id,
                "attempt_name": name,
                "row_count": int(len(expected_frame)),
                "first_source_time": first_time,
                "last_source_time": last_time,
                "path": rel(EXPECTED_PROBABILITY_TAPE),
                "sha256": sha(EXPECTED_PROBABILITY_TAPE),
                "decision_mode": "threshold_margin(임계값/마진)",
                "allowed_use": "proxy-vs-MT5 diff(프록시-MT5 차이)",
                "forbidden_use": "operating selection(운영 선택)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    write_csv(EXPECTED_PROBABILITY_INDEX, expected_index)

    set_name = f"ObsidianPrimeV2_RuntimeProbeEA_{name}.set"
    ini_name = f"ObsidianPrimeV2_RuntimeProbeEA_{name}.ini"
    set_path = SET_DIR / set_name
    ini_path = INI_DIR / ini_name
    report_name = f"Project_Obsidian_Prime_v2_{RUN_ID}_{name}"
    set_values = {
        "InpRunId": f"{RUN_ID}_{name}",
        "InpExplorationLabel": "stage338_RuntimeCollapsedONNX__MT5RuntimeProbe",
        "InpTierLabel": "Tier A",
        "InpPrimaryActiveTier": "tier_a",
        "InpSplitLabel": "inner_holdout_runtime_collapsed_probe",
        "InpMainSymbol": "US100",
        "InpTimeframe": 5,
        "InpEnforceM5": True,
        "InpFeatureCsvPath": feature_common,
        "InpFeatureCount": len(feature_names),
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
        "InpFeatureOrderHash": feature_hash,
        "InpFallbackEnabled": False,
        "InpShortThreshold": min_prob,
        "InpLongThreshold": min_prob,
        "InpMinMargin": min_margin,
        "InpDecisionMode": "threshold_margin",
        "InpInvertSignal": False,
        "InpAllowTrading": True,
        "InpFixedLot": 0.10,
        "InpMagic": 3387101,
        "InpDeviationPoints": 20,
        "InpCloseOnFlatSignal": False,
        "InpReverseOnOppositeSignal": True,
        "InpCloseOnlyOnOppositeSignal": False,
        "InpMaxHoldBars": 18,
        "InpMaxConcurrentPositions": 1,
        "InpReentryCooldownBars": 0,
        "InpSameDirectionReentryCooldownBars": 0,
        "InpEntryTransitionOnly": False,
        "InpAtrSltpEnabled": False,
        "InpModelRiskSizingEnabled": False,
        "InpTelemetryEnabled": True,
        "InpTelemetryUseCommonFiles": True,
        "InpTelemetryCsvPath": f"{COMMON_TELEMETRY_DIR}/{name}_telemetry.csv",
        "InpSummaryCsvPath": f"{COMMON_TELEMETRY_DIR}/{name}_summary.csv",
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
    tester_values = ini_payload["tester"]
    model_handoff = pd.DataFrame(
        [
            {
                "attempt_name": name,
                "model_id": model_id,
                "source_onnx_path": rel(source_onnx),
                "source_onnx_sha256": sha(source_onnx),
                "local_onnx_path": rel(local_onnx),
                "local_onnx_sha256": sha(local_onnx),
                "common_onnx_path": common_onnx,
                "common_onnx_sha256": sha(DEFAULT_COMMON_FILES / Path(common_onnx)),
                "feature_order_hash": feature_hash,
                "class_order_json": json.dumps([0, 1, 2]),
                "handoff_status": "ready_for_mt5_probe(MT5 탐침 준비)",
                "effect": "model/ONNX/Common Files(모델/온엑스/공용 파일) hash(해시)를 연결한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    set_manifest = pd.DataFrame(
        [
            {
                "attempt_name": name,
                "model_id": model_id,
                "set_path": rel(set_path),
                "set_sha256": set_payload["sha256"],
                "parameter_count": set_payload["parameter_count"],
                "decision_mode": "threshold_margin(임계값/마진)",
                "short_threshold": min_prob,
                "long_threshold": min_prob,
                "min_margin": min_margin,
                "allow_trading": True,
                "fixed_lot": 0.10,
                "max_hold_bars": 18,
                "no_optimization_rule": "fixed lot and fixed threshold; no tester optimization(고정 랏/고정 임계값, 테스터 최적화 없음)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    ini_manifest = pd.DataFrame(
        [
            {
                "attempt_name": name,
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
        ]
    )
    attempts = pd.DataFrame(
        [
            {
                "attempt_name": name,
                "next_run_id": NEXT_RUN_ID,
                "probe_priority": 1,
                "tier": "Tier A",
                "split": "inner_holdout_runtime_collapsed_probe",
                "model_id": model_id,
                "feature_set_id": "run338D_training_feature_schema",
                "feature_count": len(feature_names),
                "feature_order_hash": feature_hash,
                "feature_local_path": rel(FEATURE_MATRIX),
                "feature_common_path": feature_common,
                "model_local_path": rel(local_onnx),
                "model_common_path": common_onnx,
                "expected_tape_path": rel(EXPECTED_PROBABILITY_TAPE),
                "common_telemetry_path": f"{COMMON_TELEMETRY_DIR}/{name}_telemetry.csv",
                "common_summary_path": f"{COMMON_TELEMETRY_DIR}/{name}_summary.csv",
                "set_path": rel(set_path),
                "set_name": set_name,
                "ini_path": rel(ini_path),
                "ini_name": ini_name,
                "report_name": report_name,
                "from_date": from_date,
                "to_date": to_date,
                "decision_mode": "threshold_margin",
                "short_threshold": min_prob,
                "long_threshold": min_prob,
                "min_margin": min_margin,
                "fixed_lot": 0.10,
                "max_hold_bars": 18,
                "known_proxy_runtime_difference": "proxy uses log-return cost proxy; MT5 uses broker execution path(프록시는 로그수익 비용 프록시, MT5는 브로커 실행 경로)",
                "forbidden_action": "treat package priority as selection or promotion(패키지 우선순위를 선택/승격으로 취급)",
                "effect": "attempt(시도)를 모델 로직 변경 없이 실행할 수 있다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    contracts = {
        "tester": pd.DataFrame(
            [
                {
                    "contract_id": "tester_identity",
                    "subject": "MT5 Strategy Tester(MT5 전략 테스터)",
                    "terminal_path": DEFAULT_TERMINAL.as_posix(),
                    "tester_profile_root": DEFAULT_TESTER_PROFILE_ROOT.as_posix(),
                    "expert": tester_values.get("Expert", ""),
                    "symbol": tester_values.get("Symbol", ""),
                    "period": tester_values.get("Period", ""),
                    "deposit": tester_values.get("Deposit", ""),
                    "leverage": tester_values.get("Leverage", ""),
                    "model": tester_values.get("Model", ""),
                    "from_date": tester_values.get("FromDate", ""),
                    "to_date": tester_values.get("ToDate", ""),
                    "spread_commission_slippage": "read from actual tester output in run338H(338H 실제 테스터 출력에서 읽음)",
                    "blocked_if_missing": "tester report, telemetry, settings identity(테스터 보고서, 런타임 기록, 설정 정체성)",
                    "effect": "tester output(테스터 출력) 없이 KPI를 신뢰하지 않게 한다.",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            ]
        ),
        "proxy": pd.DataFrame(
            [
                {
                    "contract_id": "proxy_mt5_comparison",
                    "expected_tape": rel(EXPECTED_PROBABILITY_TAPE),
                    "runtime_telemetry_expected": f"{COMMON_TELEMETRY_DIR}/{name}_telemetry.csv",
                    "must_compare": "feature_input_hash, probabilities, decision, trade KPI(피처 입력 해시/확률/판단/거래 KPI)",
                    "proxy_scope": "signal sanity and routing only(신호 점검과 라우팅 전용)",
                    "forbidden_use": "replace MT5 KPI(MT5 KPI 대체)",
                    "effect": "proxy expected value(프록시 예상값)를 MT5 runtime probe(MT5 런타임 탐침)와 비교하게 한다.",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            ]
        ),
        "runtime": pd.DataFrame(
            [
                {
                    "contract_id": "runtime_parity",
                    "research_path": rel(rv.tr.FINAL_DECISION),
                    "runtime_path": rel(set_path),
                    "shared_contract": f"features={len(feature_names)};feature_hash={feature_hash};threshold={min_prob};margin={min_margin}",
                    "known_differences": "Python parquet and MT5 Common Files handoff path differ(파이썬 parquet와 MT5 공용 파일 인계 경로 다름)",
                    "parity_check": "run338H must compare telemetry against expected tape(338H는 런타임 기록과 예상 테이프 비교 필요)",
                    "runtime_claim_boundary": "runtime_probe_package_only(런타임 탐침 패키지 전용)",
                    "effect": "Python 연구와 MT5 실행 의미를 같은 계약에 묶는다.",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            ]
        ),
    }
    execution_queue = pd.DataFrame(
        [
            {
                "queue_id": "run338H_execute_runtime_collapsed_onnx_mt5_probe",
                "next_run_id": NEXT_RUN_ID,
                "priority": "P0",
                "attempt_name": name,
                "terminal_path": DEFAULT_TERMINAL.as_posix(),
                "common_files_root": DEFAULT_COMMON_FILES.as_posix(),
                "tester_profile_root": DEFAULT_TESTER_PROFILE_ROOT.as_posix(),
                "terminal_data_root": DEFAULT_PORTABLE_ROOT.as_posix(),
                "attempt_package": rel(RUNTIME_PROBE_ATTEMPT_PACKAGE),
                "required_outputs": "runtime telemetry, tester report, proxy-vs-MT5 diff(런타임 기록, 테스터 보고서, 프록시-MT5 차이)",
                "blocked_if_missing": "terminal, EA, common files handoff, tester output(터미널, EA, 공용 파일 인계, 테스터 출력)",
                "effect": "패키지를 실제 MT5 runtime probe(MT5 런타임 탐침)로 넘긴다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    write_csv(MODEL_HANDOFF_MANIFEST, model_handoff)
    write_csv(COMMON_FILES_SYNC, pd.DataFrame(sync_rows))
    write_csv(TESTER_SET_MANIFEST, set_manifest)
    write_csv(TESTER_INI_MANIFEST, ini_manifest)
    write_csv(RUNTIME_PROBE_ATTEMPT_PACKAGE, attempts)
    write_csv(TESTER_IDENTITY_CONTRACT, contracts["tester"])
    write_csv(PROXY_MT5_COMPARISON_CONTRACT, contracts["proxy"])
    write_csv(RUNTIME_PARITY_CONTRACT, contracts["runtime"])
    write_csv(RUN338H_EXECUTION_QUEUE, execution_queue)
    summary = {
        "attempt_name": name,
        "model_id": model_id,
        "package_rows": int(len(frame)),
        "feature_count": int(len(feature_names)),
        "feature_order_hash": feature_hash,
        "min_prob": min_prob,
        "min_margin": min_margin,
        "from_date": from_date,
        "to_date": to_date,
        "first_time": first_time,
        "last_time": last_time,
        "expected_rows": int(len(expected_frame)),
        "sync_rows": int(len(sync_rows)),
        "common_sync_missing": int(sum(1 for row in sync_rows if not row["exists"])),
        "set_rows": int(len(set_manifest)),
        "ini_rows": int(len(ini_manifest)),
        "terminal_exists": exists(DEFAULT_TERMINAL),
        "common_files_exists": exists(DEFAULT_COMMON_FILES),
        "ea_binary_exists": exists(EA_BINARY),
        "portable_ea_exists": exists(PORTABLE_EA_EX5),
        "parent_gate_passed": bool(passed_status(parent_gates["status"]).all()),
        "parent_goal_achieve": parent_final.get("goal_achieve", "not_claimed"),
        "input_frame_sha256": sha(rv.tr.rv.mat.INPUT_FRAME),
        "feature_matrix_sha256": sha(FEATURE_MATRIX),
        "expected_tape_sha256": sha(EXPECTED_PROBABILITY_TAPE),
        "local_onnx_sha256": sha(local_onnx),
        "common_onnx_sha256": sha(DEFAULT_COMMON_FILES / Path(common_onnx)),
        "next_run_id": NEXT_RUN_ID,
        "effect": "MT5 runtime probe(MT5 런타임 탐침)를 실행할 수 있는 file handoff(파일 인계)를 만든다.",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return summary, {
        "feature_manifest": feature_manifest,
        "model_handoff": model_handoff,
        "sync": pd.DataFrame(sync_rows),
        "set": set_manifest,
        "ini": ini_manifest,
        "attempts": attempts,
        "tester": contracts["tester"],
        "proxy": contracts["proxy"],
        "runtime": contracts["runtime"],
        "queue": execution_queue,
    }, [local_onnx, DEFAULT_COMMON_FILES / Path(common_onnx), DEFAULT_COMMON_FILES / Path(feature_common), set_path, ini_path]


def gate_row(gate: str, status: str, evidence: str, effect: str) -> dict[str, Any]:
    return {"gate_id": gate, "status": status, "evidence_path": evidence, "effect": effect, "claim_boundary": CLAIM_BOUNDARY}


def make_gates(summary: Mapping[str, Any]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            gate_row("parent_338F_gates_passed", "passed" if summary["parent_gate_passed"] else "failed", rel(rv.GATE_AUDIT), "run338F(338F 실행) proxy review(프록시 검토)를 이어받는다."),
            gate_row("feature_matrix_written", "passed" if summary["package_rows"] > 0 and exists(FEATURE_MATRIX) else "failed", rel(FEATURE_MATRIX_MANIFEST), "MT5 feature CSV(MT5 피처 CSV)를 만든다."),
            gate_row("model_handoff_synced", "passed" if summary["common_sync_missing"] == 0 else "failed", rel(COMMON_FILES_SYNC), "ONNX/feature(온엑스/피처)를 Common Files(공용 파일)에 복사한다."),
            gate_row("expected_probability_tape_written", "passed" if summary["expected_rows"] == summary["package_rows"] else "failed", rel(EXPECTED_PROBABILITY_INDEX), "proxy-vs-MT5 비교용 expected tape(예상 테이프)를 만든다."),
            gate_row("tester_set_ini_materialized", "passed" if summary["set_rows"] == 1 and summary["ini_rows"] == 1 else "failed", rel(TESTER_INI_MANIFEST), "Strategy Tester(전략 테스터) 설정 파일을 만든다."),
            gate_row("runtime_parity_contract_written", "passed" if exists(RUNTIME_PARITY_CONTRACT) else "failed", rel(RUNTIME_PARITY_CONTRACT), "Python/MT5 shared contract(공유 계약)를 기록한다."),
            gate_row("tester_identity_visible", "passed" if summary["terminal_exists"] and summary["common_files_exists"] and summary["ea_binary_exists"] and summary["portable_ea_exists"] else "failed", rel(TESTER_IDENTITY_CONTRACT), "terminal/EA/Common Files(터미널/EA/공용 파일) 가시성을 확인한다."),
            gate_row("run338H_execution_queue_opened", "passed" if exists(RUN338H_EXECUTION_QUEUE) else "failed", rel(RUN338H_EXECUTION_QUEUE), "다음 MT5 execution(실행) queue(대기열)를 연다."),
            gate_row("no_forbidden_mt5_or_selection_claim", "passed", rel(FINAL_DECISION), "패키지 생성만 하고 MT5 KPI/선택/운영 주장을 하지 않는다."),
            gate_row("required_gate_coverage_audit_written", "passed", rel(GATE_AUDIT), "required gate coverage(필수 게이트 커버리지)를 기록한다."),
        ]
    )


def write_receipts(summary: Mapping[str, Any], artifact_paths: Sequence[Path]) -> None:
    base = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": now_utc(),
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(
        DATA_RECEIPT,
        {
            **base,
            "data_source": rel(rv.tr.rv.mat.INPUT_FRAME),
            "time_axis": "runtime-collapsed timestamp unique holdout(런타임 축약 시각 고유 홀드아웃)",
            "sample_scope": f"rows={summary['package_rows']};features={summary['feature_count']}",
            "feature_label_boundary": rel(rv.tr.rv.mat.FEATURE_LABEL_BOUNDARY_AUDIT),
            "split_boundary": rel(rv.tr.rv.GROUP_SAFE_SPLIT_MANIFEST),
            "feature_matrix": rel(FEATURE_MATRIX),
            "integrity_judgment": "usable_for_mt5_runtime_probe_package(런타임 탐침 패키지 사용 가능)",
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            **base,
            "model_id": summary["model_id"],
            "onnx_path": rel(MODEL_DIR / f"{summary['attempt_name']}.onnx"),
            "onnx_hash": summary["local_onnx_sha256"],
            "feature_order_hash": summary["feature_order_hash"],
            "threshold": {"short": summary["min_prob"], "long": summary["min_prob"], "margin": summary["min_margin"]},
            "selection_metric": "not_selected_runtime_probe_package_only(선택 없음_런타임 탐침 패키지 전용)",
        },
    )
    write_json(
        RUNTIME_RECEIPT,
        {
            **base,
            "research_path": rel(rv.tr.FINAL_DECISION),
            "runtime_path": rel(RUNTIME_PROBE_ATTEMPT_PACKAGE),
            "shared_contract": rel(RUNTIME_PARITY_CONTRACT),
            "known_differences": "Python proxy path and MT5 Common Files path differ(파이썬 프록시 경로와 MT5 공용 파일 경로 다름)",
            "parity_check": "deferred_to_run338H_runtime_telemetry(338H 런타임 기록으로 연기)",
            "runtime_claim_boundary": "runtime_probe_package_only(런타임 탐침 패키지 전용)",
        },
    )
    write_json(
        FORENSICS_RECEIPT,
        {
            **base,
            "tester_identity": rel(TESTER_IDENTITY_CONTRACT),
            "ea_identity": {"source": rel(EA_SOURCE), "binary": rel(EA_BINARY), "portable_binary": PORTABLE_EA_EX5.as_posix()},
            "report_identity": "not_available_until_run338H(338H 전까지 없음)",
            "trade_evidence": "not_available_no_mt5_execution(실행 없음)",
            "cost_assumptions": "actual spread/commission/slippage read from tester output in run338H(실제 비용은 338H 테스터 출력에서 읽음)",
            "backtest_judgment": "not_applicable_package_only(패키지 전용이라 해당 없음)",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [display_path(path) for path in list(OUTPUT_FILES) + list(artifact_paths) if exists(path)],
            "artifact_hashes": {display_path(path): sha(path) for path in list(OUTPUT_FILES) + list(artifact_paths) if exists(path)},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "generated_and_common_files_synced(생성 및 공용 파일 동기화됨)",
            "lineage_judgment": "connected_with_boundary(경계 조건부 연결)",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "candidate_selection": "not_run",
            "model_training": "not_run",
            "mt5_execution": "not_run",
            "forward_passed": "not_claimed",
            "goal_achieve": "not_claimed",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
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
        "claim_boundary": CLAIM_BOUNDARY,
        "candidate_selection": "not_run",
        "model_training": "not_run",
        "mt5_execution": "not_run",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "gate_passes": int(gates["status"].astype(str).eq("passed").sum()),
        "gate_total": int(len(gates)),
        **dict(summary),
    }
    write_json(FINAL_DECISION, final)
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "created_at": TODAY,
            "created_at_utc": now_utc(),
            "script": rel(Path(__file__)),
            "inputs": [rel(path) for path in INPUT_FILES],
            "outputs": [display_path(path) for path in OUTPUT_FILES if exists(path)],
            "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    return final


def write_docs(final: Mapping[str, Any]) -> None:
    report = f"""# run338G Runtime-Collapsed MT5 Probe Package(런타임 축약 MT5 탐침 패키지)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- gates(게이트): `{final['gate_passes']}/{final['gate_total']}`
- attempt(시도): `{final['attempt_name']}`
- model_id(모델 ID): `{final['model_id']}`
- rows(행): `{final['package_rows']}`
- features(피처): `{final['feature_count']}`
- feature_order_hash(피처 순서 해시): `{final['feature_order_hash']}`
- tester_range(테스터 구간): `{final['from_date']}` to `{final['to_date']}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

## Action(행동)

run338F(338F 실행)의 timestamp-unique proxy(시각 고유 프록시)를 MT5 runtime probe package(MT5 런타임 탐침 패키지)로 물질화했다.
Effect(효과): run338H(338H 실행)가 같은 ONNX(온엑스), feature CSV(피처 CSV), threshold(임계값), expected tape(예상 테이프)를 들고 실제 MT5(메타트레이더5)를 실행할 수 있다.

## Runtime Parity(런타임 동등성)

- research_path(연구 경로): `{rel(rv.tr.FINAL_DECISION)}`
- runtime_path(런타임 경로): `{rel(RUNTIME_PROBE_ATTEMPT_PACKAGE)}`
- shared_contract(공유 계약): `{rel(RUNTIME_PARITY_CONTRACT)}`
- known_differences(알려진 차이): Python proxy path(파이썬 프록시 경로)와 MT5 Common Files path(MT5 공용 파일 경로)는 다르다.
- parity_check(동등성 검사): run338H(338H 실행)의 telemetry-vs-expected tape(런타임 기록 대 예상 테이프) 비교가 필요하다.
- runtime_claim_boundary(런타임 주장 경계): runtime_probe_package_only(런타임 탐침 패키지 전용)

## Backtest Forensics(백테스트 포렌식)

- tester_identity(테스터 정체성): `{rel(TESTER_IDENTITY_CONTRACT)}`
- report_identity(보고서 정체성): not_available_until_run338H(338H 전까지 없음)
- trade_evidence(거래 근거): not_available_no_mt5_execution(실행 없음)
- cost_assumptions(비용 가정): actual tester output required(실제 테스터 출력 필요)

## Boundary(경계)

run338G(338G 실행)는 package only(패키지 전용)이다. MT5 execution(MT5 실행), candidate selection(후보 선택), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 없다.
"""
    decision = f"""# {TODAY} Stage338G Decision(338G 결정)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- evidence(근거): `{rel(RUNTIME_PROBE_ATTEMPT_PACKAGE)}`, `{rel(TESTER_SET_MANIFEST)}`, `{rel(TESTER_INI_MANIFEST)}`, `{rel(COMMON_FILES_SYNC)}`

Action(행동): runtime-collapsed ONNX(런타임 축약 온엑스) MT5 probe package(MT5 탐침 패키지)를 만들었다.
Effect(효과): 다음 실행은 외부 검증 지연 없이 MT5 runtime probe(MT5 런타임 탐침)를 바로 시도할 수 있다.

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

run338G(338G 실행)는 ONNX/feature/set/ini/expected tape(온엑스/피처/설정/INI/예상 테이프)를 연결했다. run338H(338H 실행)는 실제 MT5 runtime probe(MT5 런타임 탐침)를 시도해야 한다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage338 Selection Status(338단계 선택 상태)

- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- packaged_model(패키지 모델): `{final['model_id']}`
- package_rows(패키지 행): `{final['package_rows']}`
- feature_count(피처 수): `{final['feature_count']}`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- goal_achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): MT5 probe package(MT5 탐침 패키지)를 선정 모델로 오해하지 않게 한다.
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
    marker = f"run338G {RUN_ID}"
    append_text_once(STAGE_BRIEF, marker, f"""## run338G MT5 Probe Package(MT5 탐침 패키지)

- run_id(실행 ID): `{RUN_ID}`
- attempt(시도): `{final['attempt_name']}`
- rows(행): `{final['package_rows']}`
- next(다음): `{NEXT_RUN_ID}`
- effect(효과): MT5 runtime probe(MT5 런타임 탐침) 실행 준비 파일을 만들었다.
""")
    append_text_once(STAGE_README, marker, f"""## run338G MT5 Probe Package(MT5 탐침 패키지)

- run_id(실행 ID): `{RUN_ID}`
- attempt_package(시도 패키지): `{rel(RUNTIME_PROBE_ATTEMPT_PACKAGE)}`
- effect(효과): Stage338(338단계)이 MT5 runtime probe(MT5 런타임 탐침) 직전까지 왔다.
""")
    changelog = f"""## {TODAY} run338G Runtime-Collapsed MT5 Probe Package(런타임 축약 MT5 탐침 패키지)

- action(행동): `{final['package_rows']}`행 feature matrix(피처 행렬), ONNX(온엑스), set/ini(설정/INI), expected tape(예상 테이프)를 만들었다.
- effect(효과): run338H(338H 실행)에서 proxy-MT5 comparison(프록시-MT5 비교)을 실제로 시도할 수 있다.
- boundary(경계): MT5 execution/selection/Goal Achieve(MT5 실행/선택/목표 달성)는 없다.
"""
    append_text_once(ROOT_CHANGELOG, marker, changelog)
    append_text_once(WORKSPACE_CHANGELOG, marker, changelog)


def write_registers(final: Mapping[str, Any], gates: pd.DataFrame) -> None:
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
        "gate_passes": int(gates["status"].astype(str).eq("passed").sum()),
        "gate_total": int(len(gates)),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], base)
    rows = [
        {**base, "view": "Tier A separate(Tier A 분리)", "tier": "Tier A", "metric_scope": "runtime_probe_package", "sample_rows": final["package_rows"], "feature_count": final["feature_count"], "result_status": JUDGMENT},
        {**base, "view": "Tier B separate(Tier B 분리)", "tier": "Tier B", "metric_scope": "missing_required", "result_status": "missing_required"},
        {**base, "view": "Tier A+B combined(Tier A+B 합산)", "tier": "Tier A+B", "metric_scope": "same_as_tier_a_until_tier_b_available", "sample_rows": final["package_rows"], "result_status": "same_as_tier_a_until_tier_b_available"},
    ]
    for row in rows:
        append_or_replace_csv(PROJECT_LEDGER, ["run_id", "view"], row)
        append_or_replace_csv(STAGE_LEDGER, ["run_id", "view"], row)


def update_artifact_registry(paths: Sequence[Path]) -> None:
    if exists(ARTIFACT_REGISTRY):
        registry = read_csv(ARTIFACT_REGISTRY)
    else:
        registry = pd.DataFrame()
    required = ["stage_id", "run_id", "artifact_type", "path", "sha256", "created_at", "claim_boundary"]
    for column in required:
        if column not in registry.columns:
            registry[column] = ""
    rows = []
    for path in paths:
        if not exists(path):
            continue
        rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": path.suffix.lstrip(".") or "artifact",
                "path": display_path(path),
                "sha256": sha(path),
                "created_at": TODAY,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    if rows:
        new_paths = {row["path"] for row in rows}
        registry = registry.loc[~((registry["run_id"].astype(str) == RUN_ID) & registry["path"].astype(str).isin(new_paths))].copy()
        registry = pd.concat([registry, pd.DataFrame(rows)], ignore_index=True)
    ordered = registry[required + [column for column in registry.columns if column not in required]]
    ensure_parent(ARTIFACT_REGISTRY)
    temp_path = ARTIFACT_REGISTRY.with_suffix(".tmp.csv")
    with io(temp_path).open("w", encoding="utf-8-sig", newline="") as handle:
        ordered.to_csv(handle, index=False, lineterminator="\n")
    io(temp_path).replace(io(ARTIFACT_REGISTRY))


def main() -> None:
    for path in [RUN_DIR, MT5_DIR, SET_DIR, INI_DIR, MODEL_DIR, FEATURE_DIR, EXPECTED_DIR, REVIEW_DIR]:
        io(path).mkdir(parents=True, exist_ok=True)
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError(f"missing run338G inputs: {missing}")
    summary, _tables, handoff_paths = build_package()
    gates = make_gates(summary)
    write_csv(GATE_AUDIT, gates)
    write_receipts(summary, handoff_paths)
    final = write_final(summary, gates)
    write_docs(final)
    write_registers(final, gates)
    update_artifact_registry([path for path in list(OUTPUT_FILES) + list(handoff_paths) if path != ARTIFACT_REGISTRY])
    failed = gates.loc[~gates["status"].astype(str).eq("passed")]
    if not failed.empty:
        raise RuntimeError(f"run338G gates failed: {failed[['gate_id', 'status']].to_dict(orient='records')}")
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "attempt_name": final["attempt_name"],
                "package_rows": final["package_rows"],
                "feature_count": final["feature_count"],
                "gate_passes": final["gate_passes"],
                "gate_total": final["gate_total"],
                "next_run_id": NEXT_RUN_ID,
                "mt5_execution": "not_run",
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
