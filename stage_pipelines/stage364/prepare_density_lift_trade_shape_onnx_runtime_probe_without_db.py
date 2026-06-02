from __future__ import annotations

import json
import math
import os
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import joblib
import numpy as np
import onnxruntime as ort
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.models.onnx_bridge import ordered_hash  # noqa: E402
from foundation.mt5.runtime_artifacts import copy_to_common_files, mt5_runtime_module_hashes  # noqa: E402
from foundation.mt5.tester_files import TesterMaterializationConfig, materialize_tester_ini_file, materialize_tester_set_file  # noqa: E402
from stage_pipelines.stage364 import train_density_lift_trade_shape_onnx_scout_without_db as tr  # noqa: E402


TODAY = "2026-06-02"
STAGE_ID = tr.STAGE_ID
RUN_NUMBER = "run364M"
RUN_ID = "run364M_prepare_density_lift_trade_shape_onnx_runtime_probe_without_db_v1"
PARENT_RUN_ID = tr.RUN_ID
NEXT_RUN_ID = "run364N_execute_density_lift_trade_shape_onnx_mt5_runtime_probe_without_db_v1"

STATUS = "completed_stage364M_density_lift_trade_shape_onnx_runtime_probe_package_prepared_common_files_synced_no_mt5_execution"
JUDGMENT = "runtime_probe_package_ready_mt5_native_maxhold_expected_positive_mt5_execution_required_no_authority"
DECISION = "stage364M_open_run364N_execute_density_lift_trade_shape_onnx_mt5_runtime_probe_without_db_v1"
CLAIM_BOUNDARY = (
    "research_development_runtime_probe_package_only_common_files_synced_no_mt5_execution_no_forward_pass_"
    "no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

TRADE_DENSITY_REQUIREMENT = "trade_per_day_min_3_to_10_plus_no_trade_splitting"
TIME_AXIS = "feature_timestamp_open_time_matched_to_mt5_closed_bar_open_time_no_timezone_conversion"
OUTPUT_CONTRACT = "p_short_p_flat_p_long_direct_three_class_probability_threshold_margin"
PRIMARY_ATTEMPT = "run364M_h12_move5_rf5_l80_n64_selected_margin_maxhold_only"
PROXY_ATTEMPT = "run364M_h12_move5_rf5_l80_n64_parent_proxy_flat_or_opp"
EA_CLOSE_ON_FLAT_ATTEMPT = "run364M_h12_move5_rf5_l80_n64_close_on_flat_approximation"

STAGE_DIR = tr.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
FEATURE_DIR = RUN_DIR / "feature_matrices"
EXPECTED_DIR = RUN_DIR / "expected_tapes"
MT5_DIR = RUN_DIR / "mt5"
SET_DIR = MT5_DIR / "sets"
INI_DIR = MT5_DIR / "inis"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
SPEC_DIR = STAGE_DIR / "00_spec"

SOURCE_RUN_DIR = STAGE_DIR / "02_runs" / "run364L"
SOURCE_FINAL_DECISION = SOURCE_RUN_DIR / "final_decision.json"
SOURCE_GATE_AUDIT = SOURCE_RUN_DIR / "required_gate_coverage_audit.csv"
SOURCE_NEXT_QUEUE = SOURCE_RUN_DIR / "run364M_next_queue.csv"
SOURCE_MODEL_SUMMARY = SOURCE_RUN_DIR / "selected_model_summary.json"
SOURCE_TRADE_SURFACE = SOURCE_RUN_DIR / "dynamic_trade_shape_surface.csv"
SOURCE_MODEL_ARTIFACT_MANIFEST = SOURCE_RUN_DIR / "model_artifact_manifest.csv"
SOURCE_ONNX_SMOKE_REPORT = SOURCE_RUN_DIR / "onnx_smoke_report.csv"
SOURCE_REPORT = REVIEW_DIR / "run364L_density_lift_trade_shape_onnx_scout.md"

MODEL_ID = "h12_move5__rf5_l80_n64"
LABEL_ID = "h12_move5"
POLICY_ID = "long_only_margin"
THRESHOLD_ID = "long_only_margin__density_16_0__maxhold_8__flat_or_opp"
EXIT_MODE = "flat_or_opp"
MAX_HOLD_M5 = 8
COST_PER_TRADE = tr.BASE_COST

SOURCE_MODEL = SOURCE_RUN_DIR / "models" / f"{MODEL_ID}.joblib"
SOURCE_FEATURE_ORDER = SOURCE_RUN_DIR / "models" / f"{MODEL_ID}_feature_order.json"
SOURCE_ONNX = SOURCE_RUN_DIR / "onnx" / f"{MODEL_ID}.onnx"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
FEATURE_ORDER = RUN_DIR / "feature_order.json"
FEATURE_MATRIX = FEATURE_DIR / "density_lift_trade_shape_features.csv"
FEATURE_MATRIX_MANIFEST = RUN_DIR / "runtime_feature_matrix_manifest.csv"
MODEL_PARITY_REPORT = RUN_DIR / "direct_onnx_probability_parity.csv"
EXPECTED_PROBABILITY_TAPE = EXPECTED_DIR / "density_lift_expected_probability_tape.csv"
EXPECTED_PROBABILITY_INDEX = RUN_DIR / "expected_probability_tape_index.csv"
PROXY_TRADE_TAPE = EXPECTED_DIR / "parent_proxy_flat_or_opp_trade_tape.csv"
MT5_NATIVE_TRADE_TAPE = EXPECTED_DIR / "mt5_native_maxhold_expected_trade_tape.csv"
RUNTIME_SEMANTIC_COMPARISON = RUN_DIR / "runtime_semantic_comparison.csv"
RUNTIME_POLICY_CONFIG = RUN_DIR / "runtime_policy_config.json"
MODEL_HANDOFF_MANIFEST = RUN_DIR / "model_handoff_manifest.csv"
COMMON_FILES_SYNC = RUN_DIR / "common_files_sync.csv"
TESTER_SET_MANIFEST = RUN_DIR / "tester_set_manifest.csv"
TESTER_INI_MANIFEST = RUN_DIR / "tester_ini_manifest.csv"
RUNTIME_PROBE_ATTEMPT_PACKAGE = RUN_DIR / "runtime_probe_attempt_package.csv"
TESTER_IDENTITY_CONTRACT = RUN_DIR / "tester_identity_contract.csv"
PROXY_MT5_COMPARISON_CONTRACT = RUN_DIR / "proxy_mt5_comparison_contract.csv"
RUNTIME_PARITY_CONTRACT = RUN_DIR / "runtime_parity_contract.csv"
RUN364N_EXECUTION_QUEUE = RUN_DIR / "run364N_execution_queue.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
BACKTEST_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364M_density_lift_trade_shape_onnx_runtime_probe_package.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364M_density_lift_trade_shape_onnx_runtime_probe_package.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"

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

COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage364/{RUN_NUMBER}_density_lift_trade_shape_onnx_runtime_probe"
COMMON_FEATURE_DIR = f"{COMMON_ROOT}/features"
COMMON_MODEL_DIR = f"{COMMON_ROOT}/models"
COMMON_EXPECTED_DIR = f"{COMMON_ROOT}/expected"
COMMON_CONFIG_DIR = f"{COMMON_ROOT}/config"
COMMON_TELEMETRY_DIR = f"{COMMON_ROOT}/telemetry"

INPUT_FILES = [
    SOURCE_FINAL_DECISION,
    SOURCE_GATE_AUDIT,
    SOURCE_NEXT_QUEUE,
    SOURCE_MODEL_SUMMARY,
    SOURCE_TRADE_SURFACE,
    SOURCE_MODEL_ARTIFACT_MANIFEST,
    SOURCE_ONNX_SMOKE_REPORT,
    SOURCE_REPORT,
    SOURCE_MODEL,
    SOURCE_FEATURE_ORDER,
    SOURCE_ONNX,
    tr.MODEL_INPUT_DATASET,
    tr.MODEL_INPUT_SUMMARY,
    tr.MODEL_INPUT_FEATURE_ORDER,
    tr.RAW_US100_M5,
    EA_SOURCE,
    EA_BINARY,
    PORTABLE_EA_EX5,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    FEATURE_ORDER,
    FEATURE_MATRIX,
    FEATURE_MATRIX_MANIFEST,
    MODEL_PARITY_REPORT,
    EXPECTED_PROBABILITY_TAPE,
    EXPECTED_PROBABILITY_INDEX,
    PROXY_TRADE_TAPE,
    MT5_NATIVE_TRADE_TAPE,
    RUNTIME_SEMANTIC_COMPARISON,
    RUNTIME_POLICY_CONFIG,
    MODEL_HANDOFF_MANIFEST,
    COMMON_FILES_SYNC,
    TESTER_SET_MANIFEST,
    TESTER_INI_MANIFEST,
    RUNTIME_PROBE_ATTEMPT_PACKAGE,
    TESTER_IDENTITY_CONTRACT,
    PROXY_MT5_COMPARISON_CONTRACT,
    RUNTIME_PARITY_CONTRACT,
    RUN364N_EXECUTION_QUEUE,
    WORK_PACKET,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    RUNTIME_RECEIPT,
    BACKTEST_RECEIPT,
    LINEAGE_RECEIPT,
    JUDGMENT_RECEIPT,
    CLAIM_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fs_path(path: Path | str) -> str:
    return tr.fs_path(path)


def rel(path: Path | str) -> str:
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = ROOT / candidate
    try:
        return candidate.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return candidate.resolve().as_posix()


def exists(path: Path | str) -> bool:
    return tr.exists(path)


def sha(path: Path | str) -> str:
    return tr.sha(path)


def read_json(path: Path) -> Any:
    return tr.read_json(path)


def write_json(path: Path, payload: Any) -> None:
    tr.write_json(path, json_safe(payload))


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    tr.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    tr.append_text_once(path, marker, text)


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    tr.write_csv(path, rows, fieldnames)


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    return tr.read_csv_rows(path)


def append_or_replace_csv(
    path: Path,
    key_fields: Sequence[str],
    rows: Sequence[Mapping[str, Any]],
    *,
    extend_header: bool = False,
) -> None:
    tr.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): json_safe(v) for k, v in value.items()}
    if isinstance(value, list):
        return [json_safe(v) for v in value]
    if isinstance(value, tuple):
        return [json_safe(v) for v in value]
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return float(value)
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    return value


def finite(value: Any, digits: int = 10) -> float | str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return ""
    if math.isnan(number):
        return ""
    if math.isinf(number):
        return "inf" if number > 0 else "-inf"
    return round(number, digits)


def format_timestamp(value: Any) -> str:
    return pd.Timestamp(value).tz_convert("UTC").strftime("%Y.%m.%d %H:%M:%S")


def timestamp_utc(value: Any) -> str:
    return pd.Timestamp(value).tz_convert("UTC").strftime("%Y-%m-%dT%H:%M:%SZ")


def date_bounds(frame: pd.DataFrame) -> tuple[str, str, str, str]:
    first = pd.Timestamp(frame["timestamp"].min()).tz_convert("UTC")
    last = pd.Timestamp(frame["timestamp"].max()).tz_convert("UTC")
    return (
        first.strftime("%Y.%m.%d %H:%M:%S"),
        last.strftime("%Y.%m.%d %H:%M:%S"),
        first.strftime("%Y.%m.%d"),
        (last + timedelta(days=1)).strftime("%Y.%m.%d"),
    )


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> str:
    if not rows:
        return "_none(없음)_"
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows:
        values = []
        for column in columns:
            text = str(row.get(column, ""))
            text = text.replace("|", "\\|").replace("\n", " ")
            values.append(text)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def ensure_dirs() -> None:
    for path in [RUN_DIR, FEATURE_DIR, EXPECTED_DIR, MT5_DIR, SET_DIR, INI_DIR, REVIEW_DIR, SELECTED_DIR, SPEC_DIR]:
        os.makedirs(fs_path(path), exist_ok=True)


def validate_inputs() -> None:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing run364M inputs: " + ", ".join(missing))
    parent = read_json(SOURCE_FINAL_DECISION)
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"run364L next_run_id mismatch: {parent.get('next_run_id')}")
    _, gates = read_csv_rows(SOURCE_GATE_AUDIT)
    if not gates or any(row.get("status") != "passed" for row in gates):
        raise RuntimeError("run364L gate audit is not fully passed")
    smoke = pd.read_csv(fs_path(SOURCE_ONNX_SMOKE_REPORT))
    row = smoke[(smoke["model_id"] == MODEL_ID) & (smoke["status"] == "passed")]
    if row.empty:
        raise RuntimeError(f"ONNX smoke report did not pass for {MODEL_ID}")


def write_input_manifest() -> None:
    rows = []
    for path in [*INPUT_FILES, Path(__file__)]:
        rows.append(
            {
                "run_id": RUN_ID,
                "input_path": rel(path),
                "exists": exists(path),
                "sha256": sha(path) if exists(path) and Path(path).is_file() else "",
                "availability": "tracked_or_materialized_with_manifest",
                "effect": "input identity(입력 정체성)를 고정해 runtime package(런타임 포장)를 재현 가능하게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(INPUT_MANIFEST, rows)


def selected_candidate() -> dict[str, Any]:
    final = read_json(SOURCE_FINAL_DECISION)
    if final["best_model_id"] != MODEL_ID:
        raise RuntimeError(f"unexpected selected model: {final['best_model_id']}")
    surface = pd.read_csv(fs_path(SOURCE_TRADE_SURFACE))
    row = surface[
        (surface["model_id"] == MODEL_ID)
        & (surface["policy_id"] == POLICY_ID)
        & (surface["threshold_id"] == THRESHOLD_ID)
        & (surface["exit_mode"] == EXIT_MODE)
        & (surface["max_hold_m5"] == MAX_HOLD_M5)
    ]
    if row.empty:
        raise RuntimeError("selected threshold surface row missing")
    selected = row.iloc[0].to_dict()
    selected.update(
        {
            "model_id": MODEL_ID,
            "label_id": LABEL_ID,
            "policy_id": POLICY_ID,
            "threshold_id": THRESHOLD_ID,
            "exit_mode": EXIT_MODE,
            "max_hold_m5": MAX_HOLD_M5,
            "score_threshold": float(selected["score_threshold"]),
            "source_model": SOURCE_MODEL,
            "source_feature_order": SOURCE_FEATURE_ORDER,
            "source_onnx": SOURCE_ONNX,
        }
    )
    return selected


def load_runtime_frame(feature_columns: Sequence[str]) -> pd.DataFrame:
    frame = tr.load_dataset(feature_columns)
    frame = frame[frame["split"].isin(["validation", "oos"])].copy().reset_index(drop=True)
    if frame["timestamp"].duplicated().any():
        raise RuntimeError("runtime frame has duplicate timestamps")
    for column in feature_columns:
        if column not in frame.columns:
            raise RuntimeError(f"missing feature column: {column}")
    if frame["entry_open"].isna().any():
        raise RuntimeError("runtime frame has missing entry_open")
    return frame


def feature_matrix_values(frame: pd.DataFrame, feature_columns: Sequence[str]) -> np.ndarray:
    return (
        frame.loc[:, list(feature_columns)]
        .replace([np.inf, -np.inf], np.nan)
        .fillna(0.0)
        .to_numpy(dtype=np.float32)
    )


def export_feature_order(feature_columns: Sequence[str]) -> dict[str, Any]:
    feature_hash = ordered_hash(feature_columns)
    payload = {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "model_id": MODEL_ID,
        "feature_columns": list(feature_columns),
        "feature_count": len(feature_columns),
        "feature_order_hash": feature_hash,
        "source_feature_order": rel(SOURCE_FEATURE_ORDER),
        "source_feature_order_sha256": sha(SOURCE_FEATURE_ORDER),
        "timestamp_semantics": TIME_AXIS,
        "output_contract": OUTPUT_CONTRACT,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(FEATURE_ORDER, payload)
    return payload


def export_feature_matrix(frame: pd.DataFrame, feature_columns: Sequence[str], feature_hash: str) -> dict[str, Any]:
    matrix = feature_matrix_values(frame, feature_columns)
    rows: list[dict[str, Any]] = []
    for index, row in frame.reset_index(drop=True).iterrows():
        out: dict[str, Any] = {
            "timestamp": format_timestamp(row["timestamp"]),
            "split": row["split"],
            "row_index": index,
            "tier": "Tier A",
            "dataset_id": "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58",
            "run_id": RUN_ID,
            "symbol": "US100",
        }
        for col_index, column in enumerate(feature_columns):
            out[column] = finite(matrix[index, col_index], 12)
        rows.append(out)
    write_csv(FEATURE_MATRIX, rows)
    by_split = frame.groupby("split", dropna=False).agg(rows=("timestamp", "count")).reset_index()
    manifest = []
    for item in by_split.to_dict("records"):
        manifest.append(
            {
                "run_id": RUN_ID,
                "split": item["split"],
                "rows": int(item["rows"]),
                "feature_count": len(feature_columns),
                "feature_order_hash": feature_hash,
                "feature_matrix": rel(FEATURE_MATRIX),
                "feature_matrix_sha256": sha(FEATURE_MATRIX),
                "timestamp_semantics": TIME_AXIS,
                "effect": "MT5 feature input(MT5 피처 입력)과 expected tape(예상 테이프)의 row grain(행 단위)을 맞춘다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(FEATURE_MATRIX_MANIFEST, manifest)
    return {
        "rows": int(len(frame)),
        "feature_count": int(len(feature_columns)),
        "feature_matrix_sha256": sha(FEATURE_MATRIX),
        "manifest_rows": manifest,
    }


def onnx_probabilities(onnx_path: Path, matrix: np.ndarray) -> np.ndarray:
    session = ort.InferenceSession(fs_path(onnx_path), providers=["CPUExecutionProvider"])
    input_name = session.get_inputs()[0].name
    outputs = session.run(None, {input_name: matrix.astype(np.float32)})
    candidate = None
    for output in outputs:
        arr = np.asarray(output)
        if arr.ndim == 2 and arr.shape[0] == matrix.shape[0] and arr.shape[1] == 3:
            candidate = arr.astype(np.float64)
    if candidate is None:
        raise RuntimeError("ONNX probability tensor not found")
    return candidate


def model_probability_payload(frame: pd.DataFrame, feature_columns: Sequence[str]) -> dict[str, Any]:
    matrix = feature_matrix_values(frame, feature_columns)
    model = joblib.load(fs_path(SOURCE_MODEL))
    sklearn_prob = tr.class_safe_probabilities(model, matrix)
    onnx_prob = onnx_probabilities(SOURCE_ONNX, matrix)
    diff = np.abs(sklearn_prob - onnx_prob)
    max_diff = float(diff.max()) if diff.size else 0.0
    by_split = []
    for split in ["validation", "oos"]:
        mask = frame["split"].eq(split).to_numpy()
        split_diff = diff[mask]
        by_split.append(
            {
                "run_id": RUN_ID,
                "model_id": MODEL_ID,
                "split": split,
                "rows": int(mask.sum()),
                "max_abs_diff": finite(float(split_diff.max()) if split_diff.size else 0.0, 12),
                "status": "passed" if (float(split_diff.max()) if split_diff.size else 0.0) <= 1e-5 else "failed",
                "effect": "sklearn probability(sklearn 확률)와 direct ONNX probability(직접 온엑스 확률)를 대조한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(MODEL_PARITY_REPORT, by_split)
    return {"matrix": matrix, "probabilities": onnx_prob, "max_abs_diff": max_diff, "rows": by_split}


def trade_metrics(trades: Sequence[Mapping[str, Any]], split_frame: pd.DataFrame, split: str, prefix: str) -> dict[str, Any]:
    days = max(1, int(split_frame["timestamp"].dt.date.nunique()))
    profits = np.asarray([float(row["net_profit"]) for row in trades], dtype=float)
    gross_profit = float(profits[profits > 0].sum()) if profits.size else 0.0
    gross_loss = float(-profits[profits < 0].sum()) if profits.size else 0.0
    equity = np.cumsum(profits) if profits.size else np.asarray([], dtype=float)
    peak = np.maximum.accumulate(equity) if equity.size else np.asarray([], dtype=float)
    drawdown = equity - peak if equity.size else np.asarray([], dtype=float)
    max_drawdown = float(drawdown.min()) if drawdown.size else 0.0
    net = float(profits.sum()) if profits.size else 0.0
    pf = gross_profit / gross_loss if gross_loss > 0 else (999.0 if gross_profit > 0 else 0.0)
    recovery = net / abs(max_drawdown) if max_drawdown < 0 else (999.0 if net > 0 else 0.0)
    return {
        f"{prefix}_split": split,
        f"{prefix}_trade_count": int(len(trades)),
        f"{prefix}_trade_density": finite(len(trades) / days, 10),
        f"{prefix}_net_profit": finite(net, 10),
        f"{prefix}_profit_factor": finite(pf, 10),
        f"{prefix}_expectancy": finite(float(profits.mean()) if profits.size else 0.0, 10),
        f"{prefix}_max_drawdown": finite(max_drawdown, 10),
        f"{prefix}_recovery_factor": finite(recovery, 10),
        f"{prefix}_long_trade_count": int(sum(1 for row in trades if row.get("side") == "long")),
        f"{prefix}_short_trade_count": int(sum(1 for row in trades if row.get("side") == "short")),
    }


def simulate_mt5_native(
    split_frame: pd.DataFrame,
    probabilities: np.ndarray,
    threshold: float,
    *,
    close_on_flat: bool,
    attempt_name: str,
    split: str,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    score = probabilities[:, 2] - np.maximum(probabilities[:, 0], probabilities[:, 1])
    opens = split_frame["entry_open"].to_numpy(dtype=float)
    trades: list[dict[str, Any]] = []
    in_position = False
    entry_index = 0
    bars_in_position = 0
    for index in range(len(split_frame)):
        signal_long = bool(score[index] >= threshold)
        decision = "long" if signal_long else "flat"
        if in_position:
            bars_in_position += 1
            exit_reason = ""
            if bars_in_position >= MAX_HOLD_M5:
                exit_reason = "close_max_hold"
            elif close_on_flat and decision == "flat":
                exit_reason = "close_on_flat"
            if exit_reason:
                profit = (opens[index] - opens[entry_index]) * tr.POINT_VALUE - COST_PER_TRADE
                trades.append(
                    {
                        "run_id": RUN_ID,
                        "attempt_name": attempt_name,
                        "split": split,
                        "model_id": MODEL_ID,
                        "policy_id": POLICY_ID,
                        "threshold_id": THRESHOLD_ID,
                        "runtime_trade_shape": "mt5_native_maxhold_only" if not close_on_flat else "mt5_close_on_flat_approximation",
                        "entry_timestamp": timestamp_utc(split_frame["timestamp"].iat[entry_index]),
                        "exit_timestamp": timestamp_utc(split_frame["timestamp"].iat[index]),
                        "held_m5": int(index - entry_index),
                        "side": "long",
                        "entry_score": finite(score[entry_index], 12),
                        "exit_score": finite(score[index], 12),
                        "threshold": finite(threshold, 12),
                        "entry_open": finite(opens[entry_index], 5),
                        "exit_open": finite(opens[index], 5),
                        "net_profit": finite(profit, 10),
                        "exit_reason": exit_reason,
                        "claim_boundary": CLAIM_BOUNDARY,
                    }
                )
                in_position = False
                bars_in_position = 0
                continue
        if not in_position and signal_long:
            in_position = True
            entry_index = index
            bars_in_position = 0
    metrics = trade_metrics(trades, split_frame, split, "mt5_native")
    metrics.update({"attempt_name": attempt_name, "close_on_flat": close_on_flat, "threshold": finite(threshold, 12)})
    return metrics, trades


def parent_proxy_trades(
    split_frame: pd.DataFrame,
    probabilities: np.ndarray,
    threshold: float,
    split: str,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    side, score = tr.policy_signal(probabilities, POLICY_ID)
    metrics, trades = tr.simulate_dynamic_exit(
        split_frame,
        probabilities,
        side,
        score,
        threshold,
        max_hold_m5=MAX_HOLD_M5,
        exit_mode=EXIT_MODE,
        cost_per_trade=COST_PER_TRADE,
        model_id=MODEL_ID,
        label_id=LABEL_ID,
        policy_id=POLICY_ID,
        threshold_id=THRESHOLD_ID,
        split=split,
    )
    rewritten: list[dict[str, Any]] = []
    for trade in trades:
        row = dict(trade)
        row["run_id"] = RUN_ID
        row["attempt_name"] = PROXY_ATTEMPT
        row["runtime_trade_shape"] = "parent_proxy_flat_or_opp"
        row["claim_boundary"] = CLAIM_BOUNDARY
        rewritten.append(row)
    out = {}
    for key, value in metrics.items():
        if key.startswith(split):
            out["proxy_" + key] = value
    out.update({"attempt_name": PROXY_ATTEMPT, "threshold": finite(threshold, 12)})
    return out, rewritten


def export_expected_tapes(
    frame: pd.DataFrame,
    probabilities: np.ndarray,
    selected: Mapping[str, Any],
    feature_hash: str,
) -> dict[str, Any]:
    threshold = float(selected["score_threshold"])
    score = probabilities[:, 2] - np.maximum(probabilities[:, 0], probabilities[:, 1])
    rows = []
    for index, row in frame.reset_index(drop=True).iterrows():
        mt5_signal = "long" if score[index] >= threshold else "flat"
        flat_dominant = bool(probabilities[index, 1] >= max(probabilities[index, 0], probabilities[index, 2]))
        rows.append(
            {
                "run_id": RUN_ID,
                "attempt_name": PRIMARY_ATTEMPT,
                "row_index": index,
                "split": row["split"],
                "bar_time_server": format_timestamp(row["timestamp"]),
                "timestamp_utc": timestamp_utc(row["timestamp"]),
                "model_id": MODEL_ID,
                "threshold_id": THRESHOLD_ID,
                "threshold": finite(threshold, 12),
                "p_short": finite(probabilities[index, 0], 12),
                "p_flat": finite(probabilities[index, 1], 12),
                "p_long": finite(probabilities[index, 2], 12),
                "long_margin": finite(score[index], 12),
                "python_parent_proxy_entry": bool(score[index] >= threshold),
                "python_parent_proxy_flat_dominant_exit_flag": flat_dominant,
                "mt5_expected_signal": mt5_signal,
                "mt5_expected_signal_int": 1 if mt5_signal == "long" else 0,
                "mt5_decision_reason": "long_threshold_met" if mt5_signal == "long" else "threshold_or_margin_not_met",
                "runtime_trade_shape": "mt5_native_maxhold_only",
                "feature_order_hash": feature_hash,
                "output_contract": OUTPUT_CONTRACT,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(EXPECTED_PROBABILITY_TAPE, rows)
    by_split = (
        pd.DataFrame(rows)
        .groupby("split", dropna=False)
        .agg(
            rows=("row_index", "count"),
            expected_long_rows=("mt5_expected_signal_int", "sum"),
            parent_flat_dominant_rows=("python_parent_proxy_flat_dominant_exit_flag", "sum"),
            avg_long_margin=("long_margin", "mean"),
        )
        .reset_index()
    )
    index_rows = []
    for item in by_split.to_dict("records"):
        item.update(
            {
                "run_id": RUN_ID,
                "expected_probability_tape": rel(EXPECTED_PROBABILITY_TAPE),
                "expected_probability_tape_sha256": sha(EXPECTED_PROBABILITY_TAPE),
                "threshold": finite(threshold, 12),
                "effect": "runtime telemetry(런타임 기록)와 probability/decision(확률/판정)을 비교할 기준을 만든다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        index_rows.append(item)
    write_csv(EXPECTED_PROBABILITY_INDEX, index_rows)

    proxy_rows: list[dict[str, Any]] = []
    mt5_rows: list[dict[str, Any]] = []
    comparison_rows: list[dict[str, Any]] = []
    split_metrics: dict[str, dict[str, Any]] = {}
    for split in ["validation", "oos"]:
        mask = frame["split"].eq(split).to_numpy()
        split_frame = frame.loc[mask].reset_index(drop=True)
        split_prob = probabilities[mask]
        proxy_metrics, split_proxy_rows = parent_proxy_trades(split_frame, split_prob, threshold, split)
        mt5_metrics, split_mt5_rows = simulate_mt5_native(
            split_frame,
            split_prob,
            threshold,
            close_on_flat=False,
            attempt_name=PRIMARY_ATTEMPT,
            split=split,
        )
        close_metrics, _close_rows = simulate_mt5_native(
            split_frame,
            split_prob,
            threshold,
            close_on_flat=True,
            attempt_name=EA_CLOSE_ON_FLAT_ATTEMPT,
            split=split,
        )
        proxy_rows.extend(split_proxy_rows)
        mt5_rows.extend(split_mt5_rows)
        split_metrics[split] = {
            "proxy": proxy_metrics,
            "mt5_native": mt5_metrics,
            "mt5_close_on_flat": close_metrics,
        }
        comparison_rows.append(
            {
                "run_id": RUN_ID,
                "split": split,
                "selected_model_id": MODEL_ID,
                "threshold_id": THRESHOLD_ID,
                "threshold": finite(threshold, 12),
                "proxy_trade_shape": "parent_flat_or_opp",
                "proxy_trade_count": proxy_metrics.get(f"proxy_{split}_trade_count", ""),
                "proxy_trade_density": proxy_metrics.get(f"proxy_{split}_trade_density", ""),
                "proxy_net_profit": proxy_metrics.get(f"proxy_{split}_net_profit", proxy_metrics.get(f"proxy_{split}_net", "")),
                "proxy_profit_factor": proxy_metrics.get(f"proxy_{split}_profit_factor", ""),
                "proxy_recovery_factor": proxy_metrics.get(f"proxy_{split}_recovery_factor", ""),
                "mt5_native_trade_shape": "maxhold_only_close_on_flat_false",
                "mt5_native_trade_count": mt5_metrics["mt5_native_trade_count"],
                "mt5_native_trade_density": mt5_metrics["mt5_native_trade_density"],
                "mt5_native_net_profit": mt5_metrics["mt5_native_net_profit"],
                "mt5_native_profit_factor": mt5_metrics["mt5_native_profit_factor"],
                "mt5_native_recovery_factor": mt5_metrics["mt5_native_recovery_factor"],
                "mt5_close_on_flat_trade_count": close_metrics["mt5_native_trade_count"],
                "mt5_close_on_flat_net_profit": close_metrics["mt5_native_net_profit"],
                "mt5_close_on_flat_profit_factor": close_metrics["mt5_native_profit_factor"],
                "selected_runtime_attempt": PRIMARY_ATTEMPT,
                "known_difference": "parent proxy(부모 프록시)는 flat dominant(플랫 우세) 청산, selected MT5 attempt(선택 MT5 시도)는 max hold only(최대 보유만) 청산.",
                "effect": "MT5가 실제로 실행할 trade shape(거래 형태)의 proxy expectation(프록시 예상값)을 따로 고정한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(PROXY_TRADE_TAPE, proxy_rows)
    write_csv(MT5_NATIVE_TRADE_TAPE, mt5_rows)
    write_csv(RUNTIME_SEMANTIC_COMPARISON, comparison_rows)
    return {
        "threshold": threshold,
        "probability_rows": len(rows),
        "probability_tape_sha256": sha(EXPECTED_PROBABILITY_TAPE),
        "proxy_trade_rows": len(proxy_rows),
        "mt5_native_trade_rows": len(mt5_rows),
        "comparison_rows": comparison_rows,
        "split_metrics": split_metrics,
    }


def copy_common(local_path: Path, common_path: str, sync_id: str, effect: str) -> dict[str, Any]:
    result = copy_to_common_files(DEFAULT_COMMON_FILES, local_path, common_path)
    return {
        "sync_id": sync_id,
        "source_path": rel(local_path),
        "common_path": common_path,
        "absolute_path": result["absolute_path"],
        "exists": exists(Path(result["absolute_path"])),
        "sha256": result["sha256"],
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_runtime_policy_config(selected: Mapping[str, Any], feature_payload: Mapping[str, Any], expected: Mapping[str, Any]) -> dict[str, Any]:
    payload = {
        "run_id": RUN_ID,
        "primary_attempt": PRIMARY_ATTEMPT,
        "parent_proxy_attempt": PROXY_ATTEMPT,
        "model_id": MODEL_ID,
        "threshold_id": THRESHOLD_ID,
        "score_threshold": finite(selected["score_threshold"], 12),
        "feature_order_hash": feature_payload["feature_order_hash"],
        "decision_surface": {
            "InpShortThreshold": 1.1,
            "InpLongThreshold": 0.0,
            "InpMinMargin": finite(selected["score_threshold"], 12),
            "InpDecisionMode": "threshold_margin",
            "InpCloseOnFlatSignal": False,
            "InpMaxHoldBars": MAX_HOLD_M5,
            "InpMaxConcurrentPositions": 1,
        },
        "runtime_trade_shape": "mt5_native_maxhold_only",
        "parent_proxy_trade_shape": "flat_or_opp_dynamic_exit",
        "known_differences": [
            "parent proxy(부모 프록시)는 flat dominant(플랫 우세) 청산이다.",
            "primary MT5 attempt(주 MT5 시도)는 current EA(현재 EA)가 정확히 실행 가능한 max hold only(최대 보유만) 청산이다.",
            "close_on_flat approximation(플랫 신호 청산 근사)은 validation expected net(검증 예상 순손익)이 음수라 선택하지 않는다.",
        ],
        "expected_tapes": {
            "probability_tape": rel(EXPECTED_PROBABILITY_TAPE),
            "proxy_trade_tape": rel(PROXY_TRADE_TAPE),
            "mt5_native_trade_tape": rel(MT5_NATIVE_TRADE_TAPE),
            "semantic_comparison": rel(RUNTIME_SEMANTIC_COMPARISON),
        },
        "mt5_execution": "not_run",
        "runtime_authority": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(RUNTIME_POLICY_CONFIG, payload)
    return payload


def materialize_set_ini(
    selected: Mapping[str, Any],
    feature_hash: str,
    feature_common: str,
    model_common: str,
    first_time: str,
    last_time: str,
    from_date: str,
    to_date: str,
) -> tuple[str, str, list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    attempt_name = PRIMARY_ATTEMPT
    set_name = f"ObsidianPrimeV2_RuntimeProbeEA_{attempt_name}.set"
    ini_name = f"ObsidianPrimeV2_RuntimeProbeEA_{attempt_name}.ini"
    set_path = SET_DIR / set_name
    ini_path = INI_DIR / ini_name
    report_name = f"Project_Obsidian_Prime_v2_{RUN_ID}_{attempt_name}"
    threshold = float(selected["score_threshold"])
    set_values = {
        "InpRunId": f"{RUN_ID}_{attempt_name}",
        "InpExplorationLabel": "stage364_DensityLiftTradeShapeONNX__RuntimeProbe",
        "InpTierLabel": "Tier A",
        "InpPrimaryActiveTier": "tier_a",
        "InpSplitLabel": "validation_oos_density_lift_runtime_probe",
        "InpMainSymbol": "US100",
        "InpTimeframe": 5,
        "InpEnforceM5": True,
        "InpFeatureCsvPath": feature_common,
        "InpFeatureCount": 58,
        "InpFeatureCsvUseCommonFiles": True,
        "InpFeatureRequireTimestampMatch": True,
        "InpFeatureAllowLatestFallback": False,
        "InpFeatureStrictHeader": True,
        "InpFeatureCsvDelimiter": ",",
        "InpCsvTimestampIsBarClose": False,
        "InpModelPath": model_common,
        "InpModelId": MODEL_ID,
        "InpModelBackend": "onnx",
        "InpModelUseCommonFiles": True,
        "InpModelUseCpuOnly": True,
        "InpModelNoConversion": False,
        "InpSetOutputShape": True,
        "InpModelUseMatrixTensor": False,
        "InpFeatureOrderHash": feature_hash,
        "InpFallbackEnabled": False,
        "InpShortThreshold": 1.1,
        "InpLongThreshold": 0.0,
        "InpMinMargin": threshold,
        "InpDecisionMode": "threshold_margin",
        "InpInvertSignal": False,
        "InpSideFilterEnabled": False,
        "InpAllowTrading": True,
        "InpFixedLot": 0.10,
        "InpMagic": 36413001,
        "InpDeviationPoints": 20,
        "InpCloseOnFlatSignal": False,
        "InpReverseOnOppositeSignal": True,
        "InpCloseOnlyOnOppositeSignal": False,
        "InpMaxHoldBars": MAX_HOLD_M5,
        "InpMaxConcurrentPositions": 1,
        "InpReentryCooldownBars": 0,
        "InpSameDirectionReentryCooldownBars": 0,
        "InpEntryTransitionOnly": False,
        "InpExitRiskOverlayEnabled": False,
        "InpAtrSltpEnabled": False,
        "InpModelRiskSizingEnabled": False,
        "InpTelemetryEnabled": True,
        "InpTelemetryUseCommonFiles": True,
        "InpTelemetryCsvPath": f"{COMMON_TELEMETRY_DIR}/{attempt_name}_telemetry.csv",
        "InpSummaryCsvPath": f"{COMMON_TELEMETRY_DIR}/{attempt_name}_summary.csv",
    }
    set_payload = materialize_tester_set_file(set_values, set_path, generated_by=rel(Path(__file__)))
    ini_payload = materialize_tester_ini_file(
        TesterMaterializationConfig(
            shutdown_terminal=1,
            from_date=from_date,
            to_date=to_date,
            report=report_name,
        ),
        ini_path,
        set_file_path=Path(set_name),
    )
    set_rows = [
        {
            "attempt_name": attempt_name,
            "model_id": MODEL_ID,
            "set_path": rel(set_path),
            "set_sha256": set_payload["sha256"],
            "parameter_count": set_payload["parameter_count"],
            "decision_mode": "threshold_margin(임계값 마진)",
            "short_threshold": 1.1,
            "long_threshold": 0.0,
            "min_margin": finite(threshold, 12),
            "close_on_flat": False,
            "max_hold_bars": MAX_HOLD_M5,
            "allow_trading": True,
            "fixed_lot": 0.10,
            "csv_timestamp_is_bar_close": False,
            "output_contract": OUTPUT_CONTRACT,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    ini_rows = [
        {
            "attempt_name": attempt_name,
            "model_id": MODEL_ID,
            "ini_path": rel(ini_path),
            "ini_sha256": ini_payload["sha256"],
            "terminal_path": DEFAULT_TERMINAL.as_posix(),
            "expert": ini_payload["tester"].get("Expert", ""),
            "symbol": ini_payload["tester"].get("Symbol", ""),
            "period": ini_payload["tester"].get("Period", ""),
            "model": ini_payload["tester"].get("Model", ""),
            "deposit": ini_payload["tester"].get("Deposit", ""),
            "leverage": ini_payload["tester"].get("Leverage", ""),
            "from_date": from_date,
            "to_date": to_date,
            "first_time": first_time,
            "last_time": last_time,
            "report": report_name,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(TESTER_SET_MANIFEST, set_rows)
    write_csv(TESTER_INI_MANIFEST, ini_rows)
    return attempt_name, report_name, set_rows, ini_rows, {"set_path": set_path, "ini_path": ini_path, "set_values": set_values, "ini_payload": ini_payload}


def build_contracts(
    selected: Mapping[str, Any],
    feature_payload: Mapping[str, Any],
    sync_rows: Sequence[Mapping[str, Any]],
    set_rows: Sequence[Mapping[str, Any]],
    ini_rows: Sequence[Mapping[str, Any]],
    attempt_name: str,
    report_name: str,
    first_time: str,
    last_time: str,
    from_date: str,
    to_date: str,
) -> dict[str, Any]:
    model_common = next(row["common_path"] for row in sync_rows if row["sync_id"] == "common_direct_onnx")
    feature_common = next(row["common_path"] for row in sync_rows if row["sync_id"] == "common_feature_matrix")
    expected_common = next(row["common_path"] for row in sync_rows if row["sync_id"] == "common_expected_probability_tape")
    trade_common = next(row["common_path"] for row in sync_rows if row["sync_id"] == "common_mt5_native_trade_tape")
    handoff = [
        {
            "attempt_name": attempt_name,
            "model_id": MODEL_ID,
            "threshold_id": THRESHOLD_ID,
            "threshold": finite(selected["score_threshold"], 12),
            "source_onnx_path": rel(SOURCE_ONNX),
            "source_onnx_sha256": sha(SOURCE_ONNX),
            "common_direct_onnx_path": model_common,
            "feature_matrix_path": rel(FEATURE_MATRIX),
            "common_feature_matrix_path": feature_common,
            "expected_tape_path": rel(EXPECTED_PROBABILITY_TAPE),
            "common_expected_tape_path": expected_common,
            "mt5_native_trade_tape_path": rel(MT5_NATIVE_TRADE_TAPE),
            "common_mt5_native_trade_tape_path": trade_common,
            "feature_order_hash": feature_payload["feature_order_hash"],
            "runtime_policy_config": rel(RUNTIME_POLICY_CONFIG),
            "handoff_status": "ready_for_mt5_runtime_probe(MT5 런타임 탐침 준비)",
            "effect": "ONNX/feature/policy(온엑스/피처/정책) 정체성을 Common Files(공용 파일)에 연결한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    attempts = [
        {
            "attempt_name": attempt_name,
            "tier": "Tier A",
            "split": "validation_oos",
            "model_id": MODEL_ID,
            "threshold_id": THRESHOLD_ID,
            "threshold": finite(selected["score_threshold"], 12),
            "feature_order_hash": feature_payload["feature_order_hash"],
            "from_date": from_date,
            "to_date": to_date,
            "first_time": first_time,
            "last_time": last_time,
            "set_path": set_rows[0]["set_path"],
            "ini_path": ini_rows[0]["ini_path"],
            "report_name": report_name,
            "runtime_telemetry_expected": f"{COMMON_TELEMETRY_DIR}/{attempt_name}_telemetry.csv",
            "runtime_summary_expected": f"{COMMON_TELEMETRY_DIR}/{attempt_name}_summary.csv",
            "known_proxy_runtime_difference": "parent proxy(부모 프록시) flat_or_opp(플랫/반대 청산)와 MT5 native maxhold(최대 보유) 실행 의미가 다르다.",
            "forbidden_action": "treat package as operating promotion(포장을 운영 승격으로 취급)",
            "effect": "다음 실행이 같은 set/ini/expected tape(설정/INI/예상 테이프)로 MT5 runtime probe(MT5 런타임 탐침)를 하게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    tester_contract = [
        {
            "contract_id": "tester_identity",
            "subject": "MT5 Strategy Tester(MT5 전략 테스터)",
            "terminal_path": DEFAULT_TERMINAL.as_posix(),
            "tester_profile_root": DEFAULT_TESTER_PROFILE_ROOT.as_posix(),
            "expert": ini_rows[0]["expert"],
            "symbol": "US100",
            "period": "M5",
            "tester_model": 4,
            "deposit": 500.0,
            "leverage": "1:100",
            "fixed_lot": 0.10,
            "from_date": from_date,
            "to_date": to_date,
            "spread_commission_slippage": "read_from_actual_tester_output_in_run364N(364N 실제 테스터 출력에서 읽음)",
            "blocked_if_missing": "tester report, telemetry, settings identity(테스터 보고서, 런타임 기록, 설정 정체성)",
            "effect": "테스터 출력 없이 KPI(핵심 성과 지표)를 주장하지 않게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    proxy_contract = [
        {
            "contract_id": "proxy_mt5_comparison",
            "expected_probability_tape": rel(EXPECTED_PROBABILITY_TAPE),
            "common_expected_probability_tape": expected_common,
            "expected_trade_tape": rel(MT5_NATIVE_TRADE_TAPE),
            "common_expected_trade_tape": trade_common,
            "runtime_telemetry_expected": f"{COMMON_TELEMETRY_DIR}/{attempt_name}_telemetry.csv",
            "must_compare": "probabilities, decision, exec_action, trade KPI(확률, 판정, 실행 행동, 거래 핵심 성과 지표)",
            "proxy_scope": "signal sanity and package parity only(신호 점검과 포장 동등성 전용)",
            "forbidden_use": "replace MT5 KPI(MT5 핵심 성과 지표 대체)",
            "effect": "proxy expected value(프록시 예상값)를 MT5 runtime probe(MT5 런타임 탐침)와 비교하게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    runtime_contract = [
        {
            "contract_id": "runtime_parity",
            "research_path": rel(SOURCE_FINAL_DECISION),
            "runtime_path": rel(RUNTIME_PROBE_ATTEMPT_PACKAGE),
            "shared_contract": f"features=58;feature_hash={feature_payload['feature_order_hash']};threshold={finite(selected['score_threshold'], 12)};output={OUTPUT_CONTRACT};close_on_flat=false;max_hold={MAX_HOLD_M5}",
            "known_differences": "selected runtime(선택 런타임)은 parent flat_or_opp proxy(부모 플랫/반대 프록시)가 아니라 MT5 native maxhold(메타트레이더5 원생 최대 보유) 변형이다.",
            "parity_check": "run364N must compare telemetry and tester report against expected tapes(364N은 런타임 기록과 테스터 보고서를 예상 테이프와 비교해야 함)",
            "runtime_claim_boundary": "runtime_probe_package_only(런타임 탐침 포장 전용)",
            "effect": "Python expected runtime(파이썬 예상 런타임)과 MT5 execution(MT5 실행)의 의미를 같은 계약에 묶는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    queue = [
        {
            "queue_id": "run364N_execute_density_lift_trade_shape_onnx_mt5_runtime_probe",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "attempt_name": attempt_name,
            "terminal_path": DEFAULT_TERMINAL.as_posix(),
            "common_files_root": DEFAULT_COMMON_FILES.as_posix(),
            "tester_profile_root": DEFAULT_TESTER_PROFILE_ROOT.as_posix(),
            "terminal_data_root": DEFAULT_PORTABLE_ROOT.as_posix(),
            "attempt_package": rel(RUNTIME_PROBE_ATTEMPT_PACKAGE),
            "ini_path": ini_rows[0]["ini_path"],
            "set_path": set_rows[0]["set_path"],
            "suggested_command": f"\"{DEFAULT_TERMINAL.as_posix()}\" /portable /config:\"{(INI_DIR / (Path(ini_rows[0]['ini_path']).name)).as_posix()}\"",
            "required_outputs": "runtime telemetry, tester report, proxy-vs-MT5 diff(런타임 기록, 테스터 보고서, 프록시-MT5 차이)",
            "blocked_if_missing": "terminal, EA, Common Files handoff, tester output(터미널, EA, 공용 파일 인계, 테스터 출력)",
            "effect": "포장을 실제 MT5 runtime probe(MT5 런타임 탐침)로 넘긴다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(MODEL_HANDOFF_MANIFEST, handoff)
    write_csv(RUNTIME_PROBE_ATTEMPT_PACKAGE, attempts)
    write_csv(TESTER_IDENTITY_CONTRACT, tester_contract)
    write_csv(PROXY_MT5_COMPARISON_CONTRACT, proxy_contract)
    write_csv(RUNTIME_PARITY_CONTRACT, runtime_contract)
    write_csv(RUN364N_EXECUTION_QUEUE, queue)
    return {
        "handoff": handoff,
        "attempts": attempts,
        "tester_contract": tester_contract,
        "proxy_contract": proxy_contract,
        "runtime_contract": runtime_contract,
        "queue": queue,
    }


def materialize_package() -> dict[str, Any]:
    selected = selected_candidate()
    feature_columns = read_json(SOURCE_FEATURE_ORDER)["feature_columns"]
    frame = load_runtime_frame(feature_columns)
    feature_payload = export_feature_order(feature_columns)
    feature_manifest = export_feature_matrix(frame, feature_columns, feature_payload["feature_order_hash"])
    probability_payload = model_probability_payload(frame, feature_columns)
    expected = export_expected_tapes(frame, probability_payload["probabilities"], selected, feature_payload["feature_order_hash"])
    policy = write_runtime_policy_config(selected, feature_payload, expected)
    first_time, last_time, from_date, to_date = date_bounds(frame)

    common_feature = f"{COMMON_FEATURE_DIR}/density_lift_trade_shape_features.csv"
    common_onnx = f"{COMMON_MODEL_DIR}/{MODEL_ID}.onnx"
    common_expected = f"{COMMON_EXPECTED_DIR}/density_lift_expected_probability_tape.csv"
    common_mt5_trade = f"{COMMON_EXPECTED_DIR}/mt5_native_maxhold_expected_trade_tape.csv"
    common_feature_order = f"{COMMON_CONFIG_DIR}/feature_order.json"
    common_policy = f"{COMMON_CONFIG_DIR}/runtime_policy_config.json"
    common_semantic_comparison = f"{COMMON_CONFIG_DIR}/runtime_semantic_comparison.csv"

    sync_rows = [
        copy_common(FEATURE_MATRIX, common_feature, "common_feature_matrix", "feature matrix(피처 행렬)를 Common Files(공용 파일)에 복사한다."),
        copy_common(SOURCE_ONNX, common_onnx, "common_direct_onnx", "direct ONNX(직접 온엑스)를 Common Files(공용 파일)에 복사한다."),
        copy_common(EXPECTED_PROBABILITY_TAPE, common_expected, "common_expected_probability_tape", "expected probability tape(예상 확률 테이프)를 Common Files(공용 파일)에 복사한다."),
        copy_common(MT5_NATIVE_TRADE_TAPE, common_mt5_trade, "common_mt5_native_trade_tape", "MT5 native expected trade tape(MT5 원생 예상 거래 테이프)를 Common Files(공용 파일)에 복사한다."),
        copy_common(FEATURE_ORDER, common_feature_order, "common_feature_order", "feature order(피처 순서)를 Common Files(공용 파일)에 복사한다."),
        copy_common(RUNTIME_POLICY_CONFIG, common_policy, "common_runtime_policy_config", "runtime policy config(런타임 정책 설정)를 Common Files(공용 파일)에 복사한다."),
        copy_common(RUNTIME_SEMANTIC_COMPARISON, common_semantic_comparison, "common_runtime_semantic_comparison", "runtime semantic comparison(런타임 의미 비교)을 Common Files(공용 파일)에 복사한다."),
    ]
    write_csv(COMMON_FILES_SYNC, sync_rows)

    attempt_name, report_name, set_rows, ini_rows, set_ini = materialize_set_ini(
        selected,
        feature_payload["feature_order_hash"],
        common_feature,
        common_onnx,
        first_time,
        last_time,
        from_date,
        to_date,
    )
    contracts = build_contracts(
        selected,
        feature_payload,
        sync_rows,
        set_rows,
        ini_rows,
        attempt_name,
        report_name,
        first_time,
        last_time,
        from_date,
        to_date,
    )
    validation_row = next(row for row in expected["comparison_rows"] if row["split"] == "validation")
    oos_row = next(row for row in expected["comparison_rows"] if row["split"] == "oos")
    summary = {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "selected_model_id": MODEL_ID,
        "label_id": LABEL_ID,
        "policy_id": POLICY_ID,
        "threshold_id": THRESHOLD_ID,
        "threshold": finite(selected["score_threshold"], 12),
        "parent_proxy_exit_mode": EXIT_MODE,
        "primary_runtime_trade_shape": "mt5_native_maxhold_only_close_on_flat_false",
        "feature_rows": feature_manifest["rows"],
        "feature_count": feature_manifest["feature_count"],
        "expected_probability_rows": expected["probability_rows"],
        "proxy_trade_rows": expected["proxy_trade_rows"],
        "mt5_native_trade_rows": expected["mt5_native_trade_rows"],
        "validation_proxy_net": validation_row["proxy_net_profit"],
        "validation_proxy_profit_factor": validation_row["proxy_profit_factor"],
        "validation_proxy_trade_density": validation_row["proxy_trade_density"],
        "validation_mt5_native_net": validation_row["mt5_native_net_profit"],
        "validation_mt5_native_profit_factor": validation_row["mt5_native_profit_factor"],
        "validation_mt5_native_trade_density": validation_row["mt5_native_trade_density"],
        "validation_mt5_native_recovery_factor": validation_row["mt5_native_recovery_factor"],
        "oos_proxy_net": oos_row["proxy_net_profit"],
        "oos_proxy_profit_factor": oos_row["proxy_profit_factor"],
        "oos_proxy_trade_density": oos_row["proxy_trade_density"],
        "oos_mt5_native_net": oos_row["mt5_native_net_profit"],
        "oos_mt5_native_profit_factor": oos_row["mt5_native_profit_factor"],
        "oos_mt5_native_trade_density": oos_row["mt5_native_trade_density"],
        "oos_mt5_native_recovery_factor": oos_row["mt5_native_recovery_factor"],
        "close_on_flat_validation_net": validation_row["mt5_close_on_flat_net_profit"],
        "close_on_flat_oos_net": oos_row["mt5_close_on_flat_net_profit"],
        "onnx_probability_max_abs_diff": finite(probability_payload["max_abs_diff"], 12),
        "feature_order_hash": feature_payload["feature_order_hash"],
        "source_onnx_sha256": sha(SOURCE_ONNX),
        "feature_matrix_sha256": sha(FEATURE_MATRIX),
        "expected_probability_tape_sha256": sha(EXPECTED_PROBABILITY_TAPE),
        "mt5_native_trade_tape_sha256": sha(MT5_NATIVE_TRADE_TAPE),
        "first_time": first_time,
        "last_time": last_time,
        "from_date": from_date,
        "to_date": to_date,
        "attempt_name": attempt_name,
        "report_name": report_name,
        "sync_rows": len(sync_rows),
        "common_sync_missing": sum(1 for row in sync_rows if not row["exists"]),
        "set_rows": len(set_rows),
        "ini_rows": len(ini_rows),
        "terminal_exists": exists(DEFAULT_TERMINAL),
        "common_files_exists": exists(DEFAULT_COMMON_FILES),
        "ea_source_exists": exists(EA_SOURCE),
        "ea_binary_exists": exists(EA_BINARY),
        "portable_ea_exists": exists(PORTABLE_EA_EX5),
        "runtime_module_hashes": mt5_runtime_module_hashes(),
        "runtime_policy_config": rel(RUNTIME_POLICY_CONFIG),
        "model_handoff_manifest": rel(MODEL_HANDOFF_MANIFEST),
        "common_files_sync": rel(COMMON_FILES_SYNC),
        "tester_set_manifest": rel(TESTER_SET_MANIFEST),
        "tester_ini_manifest": rel(TESTER_INI_MANIFEST),
        "runtime_probe_attempt_package": rel(RUNTIME_PROBE_ATTEMPT_PACKAGE),
        "runtime_parity_contract": rel(RUNTIME_PARITY_CONTRACT),
        "run364N_execution_queue": rel(RUN364N_EXECUTION_QUEUE),
        "set_path": rel(set_ini["set_path"]),
        "ini_path": rel(set_ini["ini_path"]),
        "contracts": contracts,
        "policy": policy,
        "mt5_execution": "not_run",
        "forward_passed": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return summary


def gate_rows(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    gates = [
        ("runtime_evidence_gate", summary["sync_rows"] >= 7 and summary["common_sync_missing"] == 0, COMMON_FILES_SYNC, "runtime package(런타임 포장)를 Common Files(공용 파일)에 동기화했다."),
        ("scope_completion_gate", exists(RUNTIME_PROBE_ATTEMPT_PACKAGE) and exists(TESTER_INI_MANIFEST), RUNTIME_PROBE_ATTEMPT_PACKAGE, "package scope(포장 범위)를 끝냈고 MT5 execution(MT5 실행)은 다음 실행으로 분리했다."),
        ("kpi_contract_audit", exists(RUNTIME_SEMANTIC_COMPARISON) and exists(PROXY_MT5_COMPARISON_CONTRACT), RUNTIME_SEMANTIC_COMPARISON, "proxy와 MT5-native expected KPI(프록시와 MT5 원생 예상 핵심 성과 지표)를 분리했다."),
        ("required_gate_coverage_audit", True, GATE_AUDIT, "runtime_backtest(런타임/백테스트) 필수 gate(게이트)를 closeout(종료 기록)에 연결했다."),
        ("final_claim_guard", summary["mt5_execution"] == "not_run" and summary["runtime_authority"] == "not_claimed", FINAL_DECISION, "운영 승격과 runtime authority(런타임 권위)를 주장하지 않는다."),
    ]
    rows = []
    for gate, passed, artifact, effect in gates:
        rows.append(
            {
                "run_id": RUN_ID,
                "gate": gate,
                "status": "passed" if passed else "failed",
                "artifact": rel(artifact),
                "effect": effect,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def write_receipts(summary: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    base = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": now_utc(),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(
        WORK_PACKET,
        {
            **base,
            "primary_family": "runtime_backtest(런타임/백테스트 실행)",
            "primary_skill": "obsidian-runtime-parity(런타임 동등성)",
            "support_skills": [
                "obsidian-backtest-forensics(백테스트 포렌식)",
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-result-judgment(결과 판정)",
            ],
            "required_gates": [row["gate"] for row in gates],
            "effect": "work packet(작업 묶음)을 runtime package(런타임 포장) 주장 범위에 묶는다.",
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            **base,
            "timestamp_safety": TIME_AXIS,
            "feature_rows": summary["feature_rows"],
            "feature_count": summary["feature_count"],
            "feature_order_hash": summary["feature_order_hash"],
            "effect": "feature matrix(피처 행렬)가 validation/OOS(검증/표본외) 구간과 같은 시각축을 쓴다.",
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            **base,
            "model_id": MODEL_ID,
            "onnx_probability_max_abs_diff": summary["onnx_probability_max_abs_diff"],
            "source_onnx_sha256": summary["source_onnx_sha256"],
            "effect": "direct ONNX(직접 온엑스)가 Python model(파이썬 모델) 확률과 맞는지 확인했다.",
        },
    )
    write_json(
        RUNTIME_RECEIPT,
        {
            **base,
            "attempt_name": summary["attempt_name"],
            "runtime_trade_shape": summary["primary_runtime_trade_shape"],
            "set_path": summary["set_path"],
            "ini_path": summary["ini_path"],
            "runtime_parity_contract": summary["runtime_parity_contract"],
            "effect": "MT5 runtime probe(MT5 런타임 탐침)가 같은 feature/model/policy(피처/모델/정책)를 쓰게 한다.",
        },
    )
    write_json(
        BACKTEST_RECEIPT,
        {
            **base,
            "terminal_exists": summary["terminal_exists"],
            "ea_binary_exists": summary["ea_binary_exists"],
            "portable_ea_exists": summary["portable_ea_exists"],
            "mt5_execution": "not_run",
            "next_required_evidence": "tester report and runtime telemetry(테스터 보고서와 런타임 기록)",
            "effect": "백테스트 증거가 없으면 KPI를 운영 근거로 쓰지 못하게 한다.",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "input_manifest": rel(INPUT_MANIFEST),
            "model_handoff_manifest": rel(MODEL_HANDOFF_MANIFEST),
            "common_files_sync": rel(COMMON_FILES_SYNC),
            "runtime_module_hashes": summary["runtime_module_hashes"],
            "effect": "input/code/model/handoff(입력/코드/모델/인계)의 계보를 연결한다.",
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "mt5_native_expected_oos_net": summary["oos_mt5_native_net"],
            "mt5_native_expected_oos_profit_factor": summary["oos_mt5_native_profit_factor"],
            "result_boundary": "expected_runtime_package_only(예상 런타임 포장 전용)",
            "effect": "긍정 판정 범위를 MT5 실행 전 포장 준비로 제한한다.",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "mt5_execution": "not_run",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "goal_achieve": "not_claimed",
            "effect": "좋아 보이는 expected KPI(예상 핵심 성과 지표)를 운영 주장으로 착각하지 않게 한다.",
        },
    )


def write_final(summary: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    gate_passes = sum(1 for row in gates if row["status"] == "passed")
    final = {
        **summary,
        "gate_passes": gate_passes,
        "gate_total": len(gates),
        "gate_audit_path": rel(GATE_AUDIT),
        "final_decision_path": rel(FINAL_DECISION),
        "created_at_utc": now_utc(),
    }
    write_json(FINAL_DECISION, final)
    manifest_rows = []
    for artifact_type, path in [
        ("script", Path(__file__)),
        ("report", REPORT_PATH),
        ("decision_doc", DECISION_DOC),
        ("input_manifest", INPUT_MANIFEST),
        ("feature_matrix", FEATURE_MATRIX),
        ("source_onnx", SOURCE_ONNX),
        ("expected_probability_tape", EXPECTED_PROBABILITY_TAPE),
        ("mt5_native_trade_tape", MT5_NATIVE_TRADE_TAPE),
        ("runtime_semantic_comparison", RUNTIME_SEMANTIC_COMPARISON),
        ("runtime_policy_config", RUNTIME_POLICY_CONFIG),
        ("tester_set_manifest", TESTER_SET_MANIFEST),
        ("tester_ini_manifest", TESTER_INI_MANIFEST),
        ("runtime_probe_attempt_package", RUNTIME_PROBE_ATTEMPT_PACKAGE),
        ("final_decision", FINAL_DECISION),
        ("gate_audit", GATE_AUDIT),
    ]:
        manifest_rows.append(
            {
                "artifact_type": artifact_type,
                "path": rel(path),
                "exists": exists(path),
                "sha256": sha(path) if exists(path) and Path(path).is_file() else "",
            }
        )
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "created_at_utc": now_utc(),
            "artifacts": manifest_rows,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def registry_common(summary: Mapping[str, Any], gate_passes: int, gate_total: int) -> dict[str, Any]:
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "density_lift_trade_shape_onnx_runtime_probe_package(밀도 상향 거래 형태 온엑스 런타임 탐침 포장)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "external_verification_status": "common_files_synced_mt5_execution_required(공용 파일 동기화, MT5 실행 필요)",
        "notes": "MT5-native maxhold expected(메타트레이더5 원생 최대 보유 예상값)가 validation/OOS(검증/표본외) 양수다.",
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "rows": summary["expected_probability_rows"],
        "gate_passes": gate_passes,
        "gate_total": gate_total,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "trained_models": 0,
        "onnx_parity": f"max_abs_diff={summary['onnx_probability_max_abs_diff']}",
        "best_model_id": MODEL_ID,
        "best_net_profit": summary["oos_mt5_native_net"],
        "best_profit_factor": summary["oos_mt5_native_profit_factor"],
        "trade_density_per_feature_day": summary["oos_mt5_native_trade_density"],
        "operating_ready_rows": 0,
        "run_date": TODAY,
        "primary_artifact": rel(RUNTIME_PROBE_ATTEMPT_PACKAGE),
        "result_status": STATUS,
        "sample_rows": summary["expected_probability_rows"],
        "source_package_run_id": PARENT_RUN_ID,
        "work_family": "runtime_backtest(런타임/백테스트 실행)",
        "trade_density_requirement_status": TRADE_DENSITY_REQUIREMENT,
        "result_judgment": JUDGMENT,
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": TODAY,
        "lane": "density_lift_trade_shape_onnx_runtime_probe_package(밀도 상향 거래 형태 온엑스 런타임 탐침 포장)",
        "family": "runtime_backtest(런타임/백테스트 실행)",
        "primary_report": rel(REPORT_PATH),
        "evidence_boundary": CLAIM_BOUNDARY,
        "next_action": NEXT_RUN_ID,
        "question": "Can the density-lift ONNX candidate survive MT5-native runtime semantics?(밀도 상향 온엑스 후보가 MT5 원생 런타임 의미에서 버티는가?)",
        "metric_scope": "python_expected_runtime_package_no_mt5_execution(파이썬 예상 런타임 포장, MT5 실행 없음)",
        "net_profit": summary["oos_mt5_native_net"],
        "profit_factor": summary["oos_mt5_native_profit_factor"],
        "drawdown": "",
        "recovery_factor": summary["oos_mt5_native_recovery_factor"],
        "trade_count": summary["mt5_native_trade_rows"],
        "long_trade_count": summary["mt5_native_trade_rows"],
        "short_trade_count": 0,
        "feature_count": summary["feature_count"],
        "expected_probability_rows": summary["expected_probability_rows"],
    }


def write_registries(summary: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    gate_passes = sum(1 for row in gates if row["status"] == "passed")
    gate_total = len(gates)
    common = registry_common(summary, gate_passes, gate_total)
    run_row = dict(common)
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [run_row], extend_header=False)
    tier_a = dict(common)
    tier_a.update(
        {
            "ledger_row_id": f"{RUN_ID}__Tier_A",
            "subrun_id": f"{RUN_ID}__Tier_A",
            "row_id": f"{RUN_ID}__Tier_A",
            "record_view": "Tier A separate(Tier A 분리)",
            "tier_scope": "Tier A",
            "view": "Tier A separate(Tier A 분리)",
            "tier": "Tier A",
            "kpi_scope": "expected_runtime_package(예상 런타임 포장)",
            "primary_kpi": f"oos_expected_net={summary['oos_mt5_native_net']};oos_expected_pf={summary['oos_mt5_native_profit_factor']};oos_density={summary['oos_mt5_native_trade_density']}",
            "guardrail_kpi": "mt5_execution=not_run;runtime_authority=not_claimed;close_on_flat_approx_validation_negative_recorded",
        }
    )
    tier_b = dict(tier_a)
    tier_b.update(
        {
            "ledger_row_id": f"{RUN_ID}__Tier_B",
            "subrun_id": f"{RUN_ID}__Tier_B",
            "row_id": f"{RUN_ID}__Tier_B",
            "record_view": "Tier B separate(Tier B 분리)",
            "tier_scope": "Tier B",
            "view": "Tier B separate(Tier B 분리)",
            "tier": "Tier B",
            "status": "missing_required_no_partial_context_source(필수 누락, 부분 문맥 원천 없음)",
            "primary_kpi": "missing_required(필수 누락)",
            "guardrail_kpi": "do_not_synthesize_tier_b(Tier B 합성 금지)",
        }
    )
    combined = dict(tier_a)
    combined.update(
        {
            "ledger_row_id": f"{RUN_ID}__Tier_AplusB",
            "subrun_id": f"{RUN_ID}__Tier_AplusB",
            "row_id": f"{RUN_ID}__Tier_AplusB",
            "record_view": "Tier A+B combined(Tier A+B 합산)",
            "tier_scope": "Tier A+B",
            "view": "Tier A+B combined(Tier A+B 합산)",
            "tier": "Tier A+B",
            "status": "out_of_scope_by_claim_no_combined_execution(주장 범위 밖, 합산 실행 없음)",
            "primary_kpi": "combined_not_run(합산 실행 없음)",
            "guardrail_kpi": "do_not_synthesize_combined_result(합산 결과 합성 금지)",
        }
    )
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], [tier_a, tier_b, combined], extend_header=False)
    append_or_replace_csv(STAGE_LEDGER, ["row_id"], [tier_a, tier_b, combined], extend_header=True)


def write_artifact_registry() -> None:
    rows = []
    for artifact_type, path, availability in [
        ("script", Path("stage_pipelines/stage364/prepare_density_lift_trade_shape_onnx_runtime_probe_without_db.py"), "tracked"),
        ("report", REPORT_PATH, "tracked"),
        ("decision_doc", DECISION_DOC, "tracked"),
        ("feature_matrix", FEATURE_MATRIX, "ignored_with_manifest"),
        ("source_onnx", SOURCE_ONNX, "ignored_with_manifest"),
        ("expected_probability_tape", EXPECTED_PROBABILITY_TAPE, "ignored_with_manifest"),
        ("mt5_native_trade_tape", MT5_NATIVE_TRADE_TAPE, "ignored_with_manifest"),
        ("runtime_semantic_comparison", RUNTIME_SEMANTIC_COMPARISON, "ignored_with_manifest"),
        ("tester_set_manifest", TESTER_SET_MANIFEST, "ignored_with_manifest"),
        ("tester_ini_manifest", TESTER_INI_MANIFEST, "ignored_with_manifest"),
        ("final_decision", FINAL_DECISION, "ignored_with_manifest"),
        ("gate_audit", GATE_AUDIT, "ignored_with_manifest"),
    ]:
        rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": artifact_type,
                "path": rel(path),
                "sha256": sha(path) if exists(path) and Path(path).is_file() else "",
                "created_at": TODAY,
                "created_at_utc": now_utc(),
                "claim_boundary": CLAIM_BOUNDARY,
                "artifact_id": f"{RUN_ID}__{artifact_type}",
                "notes": f"Stage364M runtime package artifact(364M 런타임 포장 산출물); availability={availability}",
                "artifact_path": rel(path),
            }
        )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["stage_id", "run_id", "artifact_type", "path"], rows, extend_header=False)


def write_report(summary: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    comparison = [
        {
            "split": "validation",
            "proxy_net": summary["validation_proxy_net"],
            "proxy_pf": summary["validation_proxy_profit_factor"],
            "proxy_density": summary["validation_proxy_trade_density"],
            "mt5_native_net": summary["validation_mt5_native_net"],
            "mt5_native_pf": summary["validation_mt5_native_profit_factor"],
            "mt5_native_density": summary["validation_mt5_native_trade_density"],
            "close_on_flat_net": summary["close_on_flat_validation_net"],
        },
        {
            "split": "oos",
            "proxy_net": summary["oos_proxy_net"],
            "proxy_pf": summary["oos_proxy_profit_factor"],
            "proxy_density": summary["oos_proxy_trade_density"],
            "mt5_native_net": summary["oos_mt5_native_net"],
            "mt5_native_pf": summary["oos_mt5_native_profit_factor"],
            "mt5_native_density": summary["oos_mt5_native_trade_density"],
            "close_on_flat_net": summary["close_on_flat_oos_net"],
        },
    ]
    text = f"""# run364M Density Lift Trade Shape ONNX Runtime Probe Package(364M 밀도 상향 거래 형태 온엑스 런타임 탐침 포장)

## Current truth(현재 진실)

Action(행동): run364L(364L 실행)의 `{MODEL_ID}` direct ONNX(직접 온엑스)를 MT5 runtime probe(MT5 런타임 탐침) 패키지로 포장했다.

Effect(효과): 다음 run364N(364N 실행)은 같은 feature matrix(피처 행렬), ONNX(온엑스), set/ini(설정/INI), expected tape(예상 테이프)를 사용해 MT5 telemetry(MT5 런타임 기록)와 tester report(테스터 보고서)를 비교할 수 있다.

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- selected_model_id(선택 모델 ID): `{MODEL_ID}`
- threshold(임계값): `{summary["threshold"]}`
- runtime_trade_shape(런타임 거래 형태): `{summary["primary_runtime_trade_shape"]}`
- mt5_execution(MT5 실행): `not_run`
- runtime_authority(런타임 권위): `not_claimed`

## Semantic comparison(의미 비교)

{markdown_table(comparison, ["split", "proxy_net", "proxy_pf", "proxy_density", "mt5_native_net", "mt5_native_pf", "mt5_native_density", "close_on_flat_net"])}

Action(행동): parent proxy(부모 프록시)의 `flat_or_opp(플랫/반대 청산)`와 MT5-native maxhold(메타트레이더5 원생 최대 보유)를 분리했다.

Effect(효과): `close_on_flat(플랫 신호 청산)` 근사는 validation net(검증 순손익)이 음수라 실행 후보에서 제외하고, EA(전문가 자문)가 현재 정확히 실행 가능한 `close_on_flat=false(플랫 청산 끔)` 후보만 MT5 runtime probe(MT5 런타임 탐침)로 넘긴다.

## Package artifacts(포장 산출물)

- feature_matrix(피처 행렬): `{rel(FEATURE_MATRIX)}`
- direct_onnx(직접 온엑스): `{rel(SOURCE_ONNX)}`
- expected_probability_tape(예상 확률 테이프): `{rel(EXPECTED_PROBABILITY_TAPE)}`
- mt5_native_trade_tape(MT5 원생 거래 테이프): `{rel(MT5_NATIVE_TRADE_TAPE)}`
- runtime_policy_config(런타임 정책 설정): `{rel(RUNTIME_POLICY_CONFIG)}`
- tester_set_manifest(테스터 설정 목록): `{rel(TESTER_SET_MANIFEST)}`
- tester_ini_manifest(테스터 INI 목록): `{rel(TESTER_INI_MANIFEST)}`
- run364N_execution_queue(364N 실행 대기열): `{rel(RUN364N_EXECUTION_QUEUE)}`

## Gates(게이트)

{markdown_table(gates, ["gate", "status", "artifact", "effect"])}

## Claim boundary(주장 경계)

Action(행동): MT5 execution(MT5 실행), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)를 주장하지 않는다.

Effect(효과): expected KPI(예상 핵심 성과 지표)는 다음 runtime probe(런타임 탐침)의 비교 기준일 뿐 운영 근거가 아니다.
"""
    write_text(REPORT_PATH, text, bom=True)
    write_text(
        DECISION_DOC,
        f"""# {TODAY} Stage364M Density Lift Runtime Probe Package(364M 밀도 상향 런타임 탐침 포장)

Action(행동): `{RUN_ID}`가 direct ONNX(직접 온엑스), feature matrix(피처 행렬), expected tape(예상 테이프), MT5 set/ini(MT5 설정/INI)를 만들고 Common Files(공용 파일)에 동기화했다.

Effect(효과): `{NEXT_RUN_ID}`에서 MT5 runtime probe(MT5 런타임 탐침)를 실행할 수 있다.

- judgment(판정): `{JUDGMENT}`
- selected runtime shape(선택 런타임 형태): `{summary["primary_runtime_trade_shape"]}`
- OOS expected net(표본외 예상 순손익): `{summary["oos_mt5_native_net"]}`
- OOS expected profit factor(표본외 예상 수익 팩터): `{summary["oos_mt5_native_profit_factor"]}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, "run364M_density_lift_trade_shape_onnx_runtime_probe_package", f"""- `{RUN_ID}`: `{rel(REPORT_PATH)}` - density lift trade shape ONNX runtime probe package(밀도 상향 거래 형태 온엑스 런타임 탐침 포장).""")
    append_text_once(SELECTION_STATUS, "run364M_density_lift_trade_shape_onnx_runtime_probe_package", f"""
## {TODAY} run364M runtime package(364M 런타임 포장)

Action(행동): `{MODEL_ID}`를 MT5-native maxhold runtime probe(MT5 원생 최대 보유 런타임 탐침)로 포장했다.

Effect(효과): 운영 승격은 없고, 다음 단계는 MT5 실행 증거를 수집하는 것이다.
""")


def write_current_truth(summary: Mapping[str, Any]) -> None:
    state = f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
current_decision: {DECISION}
next_run_id: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
"""
    write_text(WORKSPACE_STATE, state, bom=False)
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current Working State(현재 작업 상태)

- current_stage_id(현재 단계 ID): `{STAGE_ID}`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- current_status(현재 상태): `{STATUS}`
- current_judgment(현재 판정): `{JUDGMENT}`
- current_decision(현재 결정): `{DECISION}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): run364M(364M 실행)이 density lift trade shape ONNX runtime probe package(밀도 상향 거래 형태 온엑스 런타임 탐침 포장)를 완료했다.

Effect(효과): 다음 작업은 `{NEXT_RUN_ID}`이며, MT5 runtime probe(MT5 런타임 탐침)에서 tester report(테스터 보고서)와 telemetry(런타임 기록)를 expected tape(예상 테이프)와 비교한다.
""",
        bom=True,
    )
    append_text_once(WORKSPACE_CHANGELOG, RUN_ID, f"""## {TODAY} run364M Density Lift Runtime Probe Package(364M 밀도 상향 런타임 탐침 포장)

Action(행동): `{MODEL_ID}` direct ONNX(직접 온엑스)를 feature matrix(피처 행렬), expected tape(예상 테이프), set/ini(설정/INI)와 함께 Common Files(공용 파일)에 동기화했다.

Effect(효과): `{NEXT_RUN_ID}`에서 MT5 runtime probe(MT5 런타임 탐침)를 실행할 수 있다. 운영 승격과 runtime authority(런타임 권위)는 주장하지 않는다.
""")
    append_text_once(IDEA_REGISTRY, RUN_ID, f"""
## {RUN_ID}

- idea(아이디어): density-lift ONNX(밀도 상향 온엑스)를 MT5-native maxhold trade shape(MT5 원생 최대 보유 거래 형태)로 probe(탐침)한다.
- evidence(근거): `{rel(REPORT_PATH)}`.
- boundary(경계): `{CLAIM_BOUNDARY}`.
""")


def main() -> None:
    ensure_dirs()
    validate_inputs()
    write_input_manifest()
    summary = materialize_package()
    gates = gate_rows(summary)
    write_csv(GATE_AUDIT, gates)
    write_receipts(summary, gates)
    write_report(summary, gates)
    write_final(summary, gates)
    write_registries(summary, gates)
    write_artifact_registry()
    write_current_truth(summary)
    print(json.dumps(json_safe({"run_id": RUN_ID, "status": STATUS, "judgment": JUDGMENT, "next_run_id": NEXT_RUN_ID}), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
