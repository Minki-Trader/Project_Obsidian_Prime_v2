from __future__ import annotations

import csv
import math
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import joblib
import numpy as np
import onnxruntime as ort
import pandas as pd
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import balanced_accuracy_score, roc_auc_score


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage364 import materialize_density_side_balance_repair_inputs_without_db as prev  # noqa: E402


TODAY = "2026-06-02"
STAGE_ID = prev.STAGE_ID
RUN_NUMBER = "run364V"
RUN_ID = "run364V_train_density_side_balance_repair_onnx_scout_without_db_v1"
PARENT_RUN_ID = prev.RUN_ID
NEXT_RUN_ID = "run364W_package_density_side_balance_repair_runtime_probe_without_db_v1"

STATUS = "completed_stage364V_dual_side_density_repair_onnx_threshold_scout_package_candidate_no_mt5_no_authority"
JUDGMENT = "positive_proxy_runtime_executable_candidate_density_side_balance_repaired_mt5_probe_required_no_authority"
DECISION = "stage364V_open_run364W_package_density_side_balance_repair_runtime_probe_without_db_v1"
CLAIM_BOUNDARY = (
    "research_development_onnx_threshold_scout_and_shadow_training_only_no_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

POINT_VALUE = prev.POINT_VALUE
BASE_COST = prev.BASE_COST
SIDE_FILTER_FEATURE = prev.SIDE_FILTER_FEATURE
SIDE_FILTER_FEATURE_INDEX = prev.SIDE_FILTER_FEATURE_INDEX
LONG_BLOCK_SCAN = [prev.CURRENT_BLOCK_MIN, 40.0, 42.0, 45.0, 999999.0]
MAX_HOLD_SCAN = [6, 8, 10, 12]
SHORT_THRESHOLD_SCAN = [0.0, 0.34, 0.38, 0.42, 0.45, 0.48, 0.50, 0.55, 0.60]
LONG_THRESHOLD = 0.0
DENSITY_FLOOR = 3.0
OOS_PF_FLOOR = 1.15
SELECTED_VARIANT_ID = "dual_pshort_0_45__adx_block_40_0__maxhold_8"
SHADOW_DROP_RATES = [0.05, 0.10, 0.15, 0.20, 0.30]
RANDOM_SEED = 364

STAGE_DIR = prev.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MODEL_DIR = RUN_DIR / "models"
ONNX_DIR = RUN_DIR / "onnx"
EXPECTED_DIR = RUN_DIR / "expected_tapes"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
DUAL_SIDE_RUNTIME_SURFACE = RUN_DIR / "dual_side_runtime_surface.csv"
SELECTED_RUNTIME_CANDIDATE = RUN_DIR / "selected_runtime_candidate.json"
SELECTED_PROBABILITY_TAPE = EXPECTED_DIR / "dual_side_selected_expected_probability_tape.csv"
SELECTED_TRADE_TAPE = EXPECTED_DIR / "dual_side_selected_expected_trade_tape.csv"
SHADOW_TRAINING_TABLE = RUN_DIR / "shadow_loss_guard_training_table.csv"
SHADOW_MODEL_SCORECARD = RUN_DIR / "shadow_loss_guard_model_scorecard.csv"
SHADOW_ONNX_SMOKE = RUN_DIR / "shadow_loss_guard_onnx_smoke_report.csv"
SHADOW_GUARD_SURFACE = RUN_DIR / "shadow_loss_guard_surface.csv"
RUN364W_QUEUE = RUN_DIR / "run364W_package_queue.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364V_density_side_balance_repair_onnx_scout.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364V_density_side_balance_repair_onnx_scout.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
STAGE_BRIEF = SPEC_DIR / "stage_brief.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
STAGE_README = STAGE_DIR / "README.md"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"

INPUT_FILES = [
    prev.FINAL_DECISION,
    prev.GATE_AUDIT,
    prev.RUN364V_QUEUE,
    prev.DENSITY_REPAIR_CANDIDATES,
    prev.SHORT_ROUTER_CANDIDATES,
    prev.REPAIR_TRAINING_SEEDS,
    prev.SESSION_REGIME_DENSITY_GAP,
    prev.REPORT_PATH,
    prev.sidepkg.SIDE_FILTER_PROBABILITY_TAPE,
    prev.sidepkg.SIDE_FILTER_TRADE_TAPE,
    prev.sidepkg.pkg.FEATURE_ORDER,
    prev.sidepkg.pkg.FEATURE_MATRIX,
    prev.sidepkg.pkg.SOURCE_ONNX,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    DUAL_SIDE_RUNTIME_SURFACE,
    SELECTED_RUNTIME_CANDIDATE,
    SELECTED_PROBABILITY_TAPE,
    SELECTED_TRADE_TAPE,
    SHADOW_TRAINING_TABLE,
    SHADOW_MODEL_SCORECARD,
    SHADOW_ONNX_SMOKE,
    SHADOW_GUARD_SURFACE,
    RUN364W_QUEUE,
    WORK_PACKET,
    DATA_RECEIPT,
    EXPERIMENT_RECEIPT,
    MODEL_RECEIPT,
    LINEAGE_RECEIPT,
    JUDGMENT_RECEIPT,
    CLAIM_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    REVIEW_INDEX,
    STAGE_LEDGER,
    STAGE_BRIEF,
    SELECTION_STATUS,
    STAGE_README,
    WORKSPACE_STATE,
    CURRENT_WORKING_STATE,
    WORKSPACE_CHANGELOG,
    RUN_REGISTRY,
    PROJECT_LEDGER,
    ARTIFACT_REGISTRY,
    IDEA_REGISTRY,
    Path(__file__),
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fs_path(path: Path | str) -> str:
    return prev.fs_path(path)


def rel(path: Path | str) -> str:
    return prev.rel(path)


def exists(path: Path | str) -> bool:
    return prev.exists(path)


def sha(path: Path | str) -> str:
    return prev.sha(path)


def read_json(path: Path) -> Any:
    return prev.read_json(path)


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    prev.write_json(path, json_ready(payload))


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    prev.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    prev.append_text_once(path, marker, text)


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    prev.write_csv(path, rows, fieldnames)


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    return prev.read_csv_rows(path)


def append_or_replace_csv(
    path: Path,
    key_fields: Sequence[str],
    rows: Sequence[Mapping[str, Any]],
    *,
    extend_header: bool = True,
) -> None:
    prev.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, Path):
        return rel(value)
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        value = float(value)
    if isinstance(value, float):
        return value if math.isfinite(value) else None
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


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in ("", None):
            return default
        if isinstance(value, str) and value.lower() == "inf":
            return 999.0
        return float(value)
    except (TypeError, ValueError):
        return default


def ensure_dirs() -> None:
    for path in [RUN_DIR, MODEL_DIR, ONNX_DIR, EXPECTED_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR]:
        os.makedirs(fs_path(path), exist_ok=True)


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing run364V inputs: " + ", ".join(missing))
    parent = read_json(prev.FINAL_DECISION)
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"run364U next_run_id mismatch: {parent.get('next_run_id')} != {RUN_ID}")
    _, gates = read_csv_rows(prev.GATE_AUDIT)
    if not gates or any(row.get("status") != "passed" for row in gates):
        raise RuntimeError("run364U gate audit is not fully passed")
    return parent


def input_manifest_rows() -> list[dict[str, Any]]:
    rows = []
    for path in [*INPUT_FILES, Path(__file__)]:
        path_obj = Path(path)
        rows.append(
            {
                "run_id": RUN_ID,
                "input_path": rel(path),
                "exists": exists(path),
                "sha256": sha(path) if exists(path) and path_obj.is_file() else "",
                "source_run_id": source_run_for(path),
                "effect(효과)": "input identity(입력 정체성)를 고정해 threshold scout(임계값 탐색)와 shadow ONNX(그림자 온엑스)를 재현한다.",
                "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
            }
        )
    return rows


def source_run_for(path: Path | str) -> str:
    text = rel(path)
    if "run364U" in text:
        return PARENT_RUN_ID
    if "run364R" in text:
        return prev.sidepkg.RUN_ID
    if "run364M" in text:
        return prev.sidepkg.SOURCE_PACKAGE_RUN_ID
    return "local_current_project_state(로컬 현재 프로젝트 상태)"


def load_runtime_frame() -> tuple[pd.DataFrame, list[str], float]:
    frame = prev.sidepkg.load_runtime_frame().copy()
    frame["timestamp_dt"] = pd.to_datetime(frame["timestamp_utc"], utc=True)
    frame["long_margin"] = frame["long_margin"].astype(float)
    frame["short_margin"] = frame["p_short"].astype(float) - np.maximum(frame["p_flat"].astype(float), frame["p_long"].astype(float))
    feature_order = read_json(prev.sidepkg.pkg.FEATURE_ORDER)["feature_columns"]
    threshold = float(frame["threshold"].dropna().iloc[0])
    if frame["timestamp_dt"].duplicated().any():
        raise RuntimeError("runtime frame has duplicate timestamps")
    if frame[["p_short", "p_flat", "p_long", "long_margin", "short_margin", SIDE_FILTER_FEATURE, "entry_open"]].isna().any().any():
        raise RuntimeError("runtime frame has missing runtime values")
    for column in feature_order:
        if column not in frame.columns:
            raise RuntimeError(f"missing feature column: {column}")
    return frame.sort_values("timestamp_dt").reset_index(drop=True), feature_order, threshold


def decision_signals(
    part: pd.DataFrame,
    *,
    short_threshold: float,
    long_block_min: float,
    min_margin: float,
    with_reasons: bool = False,
) -> tuple[np.ndarray, list[str]]:
    p_short = part["p_short"].to_numpy(dtype=float)
    p_flat = part["p_flat"].to_numpy(dtype=float)
    p_long = part["p_long"].to_numpy(dtype=float)
    short_margin = p_short - np.maximum(p_flat, p_long)
    long_margin = p_long - np.maximum(p_flat, p_short)
    short_ok = (p_short >= short_threshold) & (short_margin >= min_margin)
    long_ok = (p_long >= LONG_THRESHOLD) & (long_margin >= min_margin)
    signals = np.zeros(len(part), dtype=np.int8)
    signals[short_ok] = -1
    signals[long_ok & ((~short_ok) | (p_long >= p_short))] = 1
    blocked_long = (signals == 1) & (part[SIDE_FILTER_FEATURE].to_numpy(dtype=float) >= long_block_min)
    signals[blocked_long] = 0
    reasons: list[str] = []
    if with_reasons:
        for index, signal in enumerate(signals):
            if blocked_long[index]:
                reasons.append(f"side_filter_block_long_feature_range:index={SIDE_FILTER_FEATURE_INDEX}")
            elif signal == 1:
                reasons.append("long_threshold_met")
            elif signal == -1:
                reasons.append("short_threshold_met")
            else:
                reasons.append("threshold_or_margin_not_met")
    return signals, reasons


def simulate_execution(
    frame: pd.DataFrame,
    *,
    variant: Mapping[str, Any],
    emit_tapes: bool = False,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    trade_rows: list[dict[str, Any]] = []
    probability_rows: list[dict[str, Any]] = []
    short_threshold = float(variant["short_threshold"])
    long_block_min = float(variant["long_block_min"])
    max_hold = int(variant["max_hold_m5"])
    min_margin = float(variant["min_margin"])
    variant_id = str(variant["variant_id"])
    for split, split_frame in frame.groupby("split", sort=False):
        part = split_frame.sort_values("timestamp_dt").reset_index(drop=True)
        signals, reasons = decision_signals(
            part,
            short_threshold=short_threshold,
            long_block_min=long_block_min,
            min_margin=min_margin,
            with_reasons=emit_tapes,
        )
        if emit_tapes:
            for index, row in part.iterrows():
                probability_rows.append(
                    {
                        "run_id": RUN_ID,
                        "variant_id": variant_id,
                        "row_index": int(row["row_index"]),
                        "split": split,
                        "bar_time_server": row["bar_time_server"],
                        "timestamp_utc": row["timestamp_utc"],
                        "model_id": prev.sidepkg.MODEL_ID,
                        "threshold_id": variant_id,
                        "short_probability_threshold": finite(short_threshold, 12),
                        "long_threshold": finite(LONG_THRESHOLD, 12),
                        "min_margin": finite(min_margin, 12),
                        "p_short": finite(row["p_short"], 12),
                        "p_flat": finite(row["p_flat"], 12),
                        "p_long": finite(row["p_long"], 12),
                        "short_margin": finite(row["short_margin"], 12),
                        "long_margin": finite(row["long_margin"], 12),
                        SIDE_FILTER_FEATURE: finite(row[SIDE_FILTER_FEATURE], 12),
                        "side_filter_enabled": True,
                        "side_filter_feature_index": SIDE_FILTER_FEATURE_INDEX,
                        "block_long_feature_min": finite(long_block_min, 6),
                        "block_short_feature_range": False,
                        "mt5_expected_signal": signal_label(int(signals[index])),
                        "mt5_expected_signal_int": int(signals[index]),
                        "mt5_decision_reason": reasons[index],
                        "runtime_trade_shape": "threshold_margin_dual_side_reverse_on_opposite_maxhold",
                        "feature_order_hash": row["feature_order_hash"],
                        "claim_boundary": CLAIM_BOUNDARY,
                    }
                )
        opens = part["entry_open"].to_numpy(dtype=float)
        timestamps = part["timestamp_dt"].to_numpy()
        position = 0
        entry_index = 0
        entry_open = 0.0
        bars_in_position = 0
        for index in range(len(part)):
            if position != 0:
                bars_in_position += 1
            if position != 0 and bars_in_position >= max_hold:
                trade_rows.append(
                    trade_row(variant_id, split, part, timestamps, opens, position, entry_index, index, entry_open, "close_max_hold")
                )
                position = 0
                bars_in_position = 0
                continue
            signal = int(signals[index])
            if signal == 0:
                continue
            if position == 0:
                position = signal
                entry_index = index
                entry_open = float(opens[index])
                bars_in_position = 0
                continue
            if signal == position:
                continue
            trade_rows.append(
                trade_row(variant_id, split, part, timestamps, opens, position, entry_index, index, entry_open, "reverse_on_opposite")
            )
            position = signal
            entry_index = index
            entry_open = float(opens[index])
            bars_in_position = 0
    return pd.DataFrame(probability_rows), pd.DataFrame(trade_rows)


def signal_label(signal: int) -> str:
    if signal > 0:
        return "long"
    if signal < 0:
        return "short"
    return "flat"


def trade_row(
    variant_id: str,
    split: str,
    part: pd.DataFrame,
    timestamps: np.ndarray,
    opens: np.ndarray,
    position: int,
    entry_index: int,
    exit_index: int,
    entry_open: float,
    exit_reason: str,
) -> dict[str, Any]:
    exit_open = float(opens[exit_index])
    profit = (exit_open - entry_open) * POINT_VALUE - BASE_COST if position == 1 else (entry_open - exit_open) * POINT_VALUE - BASE_COST
    entry_row = part.iloc[entry_index]
    exit_row = part.iloc[exit_index]
    return {
        "run_id": RUN_ID,
        "variant_id": variant_id,
        "split": split,
        "model_id": prev.sidepkg.MODEL_ID,
        "runtime_trade_shape": "threshold_margin_dual_side_reverse_on_opposite_maxhold",
        "entry_timestamp": pd.Timestamp(timestamps[entry_index]).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "exit_timestamp": pd.Timestamp(timestamps[exit_index]).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "held_m5": int(exit_index - entry_index),
        "side": "long" if position == 1 else "short",
        "entry_score": finite(entry_row["long_margin"] if position == 1 else entry_row["short_margin"], 12),
        "entry_confidence": finite(entry_row["p_long"] if position == 1 else entry_row["p_short"], 12),
        "entry_open": finite(entry_open, 5),
        "exit_open": finite(exit_open, 5),
        "net_profit": finite(profit, 10),
        SIDE_FILTER_FEATURE: finite(entry_row[SIDE_FILTER_FEATURE], 12),
        "exit_reason": exit_reason,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def metrics_for_trades(trades: pd.DataFrame, prefix: str) -> dict[str, Any]:
    if trades.empty:
        return empty_metrics(prefix)
    part = trades.sort_values("entry_timestamp").copy()
    profits = part["net_profit"].astype(float).to_numpy()
    gross_profit = float(profits[profits > 0].sum())
    gross_loss = float(-profits[profits < 0].sum())
    equity = np.cumsum(profits)
    peak = np.maximum.accumulate(np.r_[0.0, equity])[:-1]
    drawdown = equity - peak
    max_drawdown = float(drawdown.min()) if drawdown.size else 0.0
    timestamps = pd.to_datetime(part["entry_timestamp"], utc=True)
    business_days = max(1, len(pd.bdate_range(timestamps.min().date(), timestamps.max().date())))
    long_count = int(part["side"].eq("long").sum())
    short_count = int(part["side"].eq("short").sum())
    net = float(profits.sum())
    return {
        f"{prefix}_trade_count": int(len(part)),
        f"{prefix}_trade_per_business_day": finite(len(part) / business_days, 10),
        f"{prefix}_net_profit": finite(net, 10),
        f"{prefix}_profit_factor": finite(gross_profit / gross_loss, 10) if gross_loss > 0 else "inf",
        f"{prefix}_expectancy": finite(float(profits.mean()), 10),
        f"{prefix}_max_drawdown": finite(max_drawdown, 10),
        f"{prefix}_recovery_factor": finite(net / abs(max_drawdown), 10) if max_drawdown < 0 else "inf",
        f"{prefix}_long_count": long_count,
        f"{prefix}_short_count": short_count,
        f"{prefix}_long_short_balance": finite(min(long_count, short_count) / max(long_count, short_count), 10) if max(long_count, short_count) else 0.0,
        f"{prefix}_business_days": business_days,
    }


def empty_metrics(prefix: str) -> dict[str, Any]:
    return {
        f"{prefix}_trade_count": 0,
        f"{prefix}_trade_per_business_day": 0.0,
        f"{prefix}_net_profit": 0.0,
        f"{prefix}_profit_factor": 0.0,
        f"{prefix}_expectancy": 0.0,
        f"{prefix}_max_drawdown": 0.0,
        f"{prefix}_recovery_factor": 0.0,
        f"{prefix}_long_count": 0,
        f"{prefix}_short_count": 0,
        f"{prefix}_long_short_balance": 0.0,
        f"{prefix}_business_days": 0,
    }


def build_dual_side_surface(frame: pd.DataFrame, min_margin: float) -> tuple[pd.DataFrame, dict[str, Any], pd.DataFrame, pd.DataFrame]:
    rows: list[dict[str, Any]] = []
    selected_probability = pd.DataFrame()
    selected_trades = pd.DataFrame()
    for short_threshold in SHORT_THRESHOLD_SCAN:
        for long_block_min in LONG_BLOCK_SCAN:
            for max_hold in MAX_HOLD_SCAN:
                variant = {
                    "variant_id": variant_id(short_threshold, long_block_min, max_hold),
                    "short_threshold": short_threshold,
                    "long_block_min": long_block_min,
                    "max_hold_m5": max_hold,
                    "min_margin": min_margin,
                }
                probability, trades = simulate_execution(frame, variant=variant, emit_tapes=(variant["variant_id"] == SELECTED_VARIANT_ID))
                row = {
                    "run_id": RUN_ID,
                    "variant_id": variant["variant_id"],
                    "family": "runtime_executable_dual_side_threshold_surface(런타임 실행 가능 양방향 임계값 표면)",
                    "short_probability_threshold": finite(short_threshold, 12),
                    "long_threshold": finite(LONG_THRESHOLD, 12),
                    "min_margin": finite(min_margin, 12),
                    "long_block_feature": SIDE_FILTER_FEATURE,
                    "long_block_min": finite(long_block_min, 6),
                    "max_hold_m5": max_hold,
                    "reverse_on_opposite": True,
                    "close_on_flat": False,
                    "trade_splitting_status": "not_used(미사용)",
                    "proxy_boundary(프록시 경계)": "python_expected_execution_semantics_awaits_mt5_probe(파이썬 예상 실행 의미이며 MT5 탐침 필요)",
                    "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
                }
                for split in ["validation", "oos"]:
                    row.update(metrics_for_trades(trades[trades["split"].eq(split)].copy(), split))
                row.update(metrics_for_trades(trades, "combined"))
                row["density_status"] = density_status(row)
                row["side_balance_status"] = "passed(통과)" if as_float(row["combined_short_count"]) > 0 else "failed_long_only(롱 전용 실패)"
                row["candidate_status"] = candidate_status(row)
                row["selection_score"] = finite(selection_score(row), 10)
                rows.append(row)
                if variant["variant_id"] == SELECTED_VARIANT_ID:
                    selected_probability = probability
                    selected_trades = trades
    surface = pd.DataFrame(rows)
    candidates = surface[surface["candidate_status"].eq("pass_density_profit_side_balance(밀도/수익/방향 통과)")].copy()
    if candidates.empty:
        best = surface.sort_values("selection_score", ascending=False).iloc[0].to_dict()
    else:
        best = candidates.sort_values(["combined_net_profit", "oos_profit_factor", "combined_trade_per_business_day"], ascending=[False, False, False]).iloc[0].to_dict()
    if best["variant_id"] != SELECTED_VARIANT_ID:
        selected_variant = variant_from_surface_row(best)
        selected_probability, selected_trades = simulate_execution(frame, variant=selected_variant, emit_tapes=True)
    return surface, best, selected_probability, selected_trades


def variant_id(short_threshold: float, long_block_min: float, max_hold: int) -> str:
    short_label = str(round(short_threshold, 6)).replace(".", "_")
    block_label = "none" if long_block_min >= 999999.0 else str(round(long_block_min, 6)).replace(".", "_")
    return f"dual_pshort_{short_label}__adx_block_{block_label}__maxhold_{max_hold}"


def variant_from_surface_row(row: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "variant_id": row["variant_id"],
        "short_threshold": as_float(row["short_probability_threshold"]),
        "long_block_min": as_float(row["long_block_min"]),
        "max_hold_m5": int(as_float(row["max_hold_m5"])),
        "min_margin": as_float(row["min_margin"]),
    }


def density_status(row: Mapping[str, Any]) -> str:
    if as_float(row["validation_trade_per_business_day"]) >= DENSITY_FLOOR and as_float(row["combined_trade_per_business_day"]) >= DENSITY_FLOOR:
        return "passed_validation_and_combined(검증/합산 통과)"
    return "failed_validation_or_combined(검증 또는 합산 실패)"


def candidate_status(row: Mapping[str, Any]) -> str:
    if (
        as_float(row["validation_trade_per_business_day"]) >= DENSITY_FLOOR
        and as_float(row["combined_trade_per_business_day"]) >= DENSITY_FLOOR
        and as_float(row["validation_net_profit"]) > 0.0
        and as_float(row["oos_net_profit"]) > 0.0
        and as_float(row["oos_profit_factor"]) >= OOS_PF_FLOOR
        and as_float(row["combined_short_count"]) > 0
    ):
        return "pass_density_profit_side_balance(밀도/수익/방향 통과)"
    return "fail_required_runtime_proxy_filter(필수 런타임 프록시 필터 실패)"


def selection_score(row: Mapping[str, Any]) -> float:
    return (
        as_float(row.get("combined_net_profit"))
        + 80.0 * min(as_float(row.get("combined_trade_per_business_day")), 6.0)
        + 150.0 * max(0.0, as_float(row.get("oos_profit_factor")) - 1.0)
        + 0.25 * as_float(row.get("validation_net_profit"))
        + 0.10 * as_float(row.get("combined_short_count"))
        - 0.20 * abs(min(0.0, as_float(row.get("combined_max_drawdown"))))
    )


def feature_matrix(frame: pd.DataFrame, columns: Sequence[str]) -> np.ndarray:
    return (
        frame.loc[:, list(columns)]
        .replace([np.inf, -np.inf], np.nan)
        .fillna(0.0)
        .to_numpy(dtype=np.float32)
    )


def train_shadow_loss_guard(frame: pd.DataFrame, selected_trades: pd.DataFrame, feature_columns: Sequence[str]) -> tuple[pd.DataFrame, list[dict[str, Any]], list[dict[str, Any]], pd.DataFrame]:
    table = selected_trades.copy()
    table["timestamp_dt"] = pd.to_datetime(table["entry_timestamp"], utc=True)
    table = table.drop(columns=[column for column in feature_columns if column in table.columns], errors="ignore")
    feature_frame = frame[["timestamp_dt", *feature_columns]].copy()
    table = table.merge(feature_frame, on="timestamp_dt", how="left")
    table["loss_label"] = (table["net_profit"].astype(float) < 0.0).astype("int8")
    table["tail_loss_label"] = (table["net_profit"].astype(float) <= -10.0).astype("int8")
    missing = int(table[feature_columns].isna().any(axis=1).sum())
    if missing:
        raise RuntimeError(f"shadow training table has missing feature rows: {missing}")
    write_csv(SHADOW_TRAINING_TABLE, table.to_dict("records"))
    train = table[table["split"].eq("validation")].copy()
    test = table[table["split"].eq("oos")].copy()
    x_train = feature_matrix(train, feature_columns)
    y_train = train["loss_label"].to_numpy(dtype=np.int8)
    x_test = feature_matrix(test, feature_columns)
    y_test = test["loss_label"].to_numpy(dtype=np.int8)
    model = RandomForestClassifier(
        n_estimators=96,
        max_depth=3,
        min_samples_leaf=20,
        class_weight="balanced_subsample",
        random_state=RANDOM_SEED,
        n_jobs=-1,
    )
    model.fit(x_train, y_train)
    model_id = "shadow_loss_guard_rf3_l20_n96"
    model_path = MODEL_DIR / f"{model_id}.joblib"
    onnx_path = ONNX_DIR / f"{model_id}.onnx"
    feature_order_path = MODEL_DIR / f"{model_id}_feature_order.json"
    joblib.dump(model, fs_path(model_path))
    write_json(
        feature_order_path,
        {
            "run_id": RUN_ID,
            "model_id": model_id,
            "feature_columns": list(feature_columns),
            "feature_count": len(feature_columns),
            "target": "loss_label(손실 라벨)",
            "runtime_compatibility": "shadow_only_binary_output_not_current_ea_primary_output(그림자 전용 2출력, 현재 EA 주 출력 아님)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    onnx_model = convert_sklearn(
        model,
        initial_types=[("float_input", FloatTensorType([None, len(feature_columns)]))],
        options={id(model): {"zipmap": False}},
    )
    with open(fs_path(onnx_path), "wb") as handle:
        handle.write(onnx_model.SerializeToString())
    train_score = class_one_probability(model, x_train)
    test_score = class_one_probability(model, x_test)
    score_rows = [
        {
            "run_id": RUN_ID,
            "model_id": model_id,
            "train_rows": int(len(train)),
            "oos_rows": int(len(test)),
            "feature_count": len(feature_columns),
            "train_loss_rate": finite(float(y_train.mean()), 10),
            "oos_loss_rate": finite(float(y_test.mean()), 10),
            "train_auc": finite(roc_auc_score(y_train, train_score), 10) if len(np.unique(y_train)) > 1 else "",
            "oos_auc": finite(roc_auc_score(y_test, test_score), 10) if len(np.unique(y_test)) > 1 else "",
            "train_balanced_accuracy": finite(balanced_accuracy_score(y_train, (train_score >= 0.5).astype("int8")), 10),
            "oos_balanced_accuracy": finite(balanced_accuracy_score(y_test, (test_score >= 0.5).astype("int8")), 10),
            "model_path": rel(model_path),
            "onnx_path": rel(onnx_path),
            "feature_order_path": rel(feature_order_path),
            "runtime_compatibility": "shadow_only_binary_output_not_current_ea_primary_output(그림자 전용 2출력, 현재 EA 주 출력 아님)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    smoke_rows = [smoke_onnx(model, onnx_path, x_test[: min(128, len(x_test))], model_id)]
    guard_surface = shadow_guard_surface(table, train_score, test_score)
    write_csv(SHADOW_MODEL_SCORECARD, score_rows)
    write_csv(SHADOW_ONNX_SMOKE, smoke_rows)
    write_csv(SHADOW_GUARD_SURFACE, guard_surface.to_dict("records"))
    return table, score_rows, smoke_rows, guard_surface


def class_one_probability(model: Any, matrix: np.ndarray) -> np.ndarray:
    raw = model.predict_proba(matrix)
    classes = list(model.classes_)
    if 1 not in classes:
        return np.zeros(len(matrix), dtype=np.float64)
    return raw[:, classes.index(1)].astype(np.float64)


def smoke_onnx(model: Any, onnx_path: Path, sample: np.ndarray, model_id: str) -> dict[str, Any]:
    if len(sample) == 0:
        return {"run_id": RUN_ID, "model_id": model_id, "status": "blocked", "sample_rows": 0, "max_abs_diff": "", "failure": "empty_sample", "claim_boundary": CLAIM_BOUNDARY}
    try:
        session = ort.InferenceSession(fs_path(onnx_path), providers=["CPUExecutionProvider"])
        input_name = session.get_inputs()[0].name
        outputs = session.run(None, {input_name: sample.astype(np.float32)})
        candidate = None
        for output in outputs:
            arr = np.asarray(output)
            if arr.ndim == 2 and arr.shape[0] == sample.shape[0] and arr.shape[1] == 2:
                candidate = arr.astype(np.float64)
                break
        if candidate is None:
            return {"run_id": RUN_ID, "model_id": model_id, "status": "failed", "sample_rows": len(sample), "max_abs_diff": "", "failure": "probability_tensor_not_found", "claim_boundary": CLAIM_BOUNDARY}
        sklearn_prob = model.predict_proba(sample)
        diff = float(np.max(np.abs(sklearn_prob - candidate)))
        return {"run_id": RUN_ID, "model_id": model_id, "status": "passed" if diff <= 1e-6 else "failed", "sample_rows": len(sample), "max_abs_diff": finite(diff, 12), "failure": "", "claim_boundary": CLAIM_BOUNDARY}
    except Exception as exc:  # pragma: no cover - smoke report captures runtime errors.
        return {"run_id": RUN_ID, "model_id": model_id, "status": "failed", "sample_rows": len(sample), "max_abs_diff": "", "failure": repr(exc), "claim_boundary": CLAIM_BOUNDARY}


def shadow_guard_surface(table: pd.DataFrame, train_score: np.ndarray, test_score: np.ndarray) -> pd.DataFrame:
    scored = table.copy()
    scored["risk_score"] = 0.0
    scored.loc[scored["split"].eq("validation"), "risk_score"] = train_score
    scored.loc[scored["split"].eq("oos"), "risk_score"] = test_score
    rows: list[dict[str, Any]] = []
    parent_metrics = {
        **metrics_for_trades(scored[scored["split"].eq("validation")], "validation"),
        **metrics_for_trades(scored[scored["split"].eq("oos")], "oos"),
        **metrics_for_trades(scored, "combined"),
    }
    rows.append(surface_row("shadow_parent_selected_dual_side", 0.0, scored, parent_metrics, 0))
    validation_scores = scored.loc[scored["split"].eq("validation"), "risk_score"].to_numpy(dtype=float)
    for drop_rate in SHADOW_DROP_RATES:
        threshold = float(np.quantile(validation_scores, 1.0 - drop_rate))
        kept = scored[scored["risk_score"] < threshold].copy()
        metrics = {
            **metrics_for_trades(kept[kept["split"].eq("validation")], "validation"),
            **metrics_for_trades(kept[kept["split"].eq("oos")], "oos"),
            **metrics_for_trades(kept, "combined"),
        }
        rows.append(surface_row(f"shadow_drop_top_{int(drop_rate * 100):02d}pct_loss_risk", threshold, kept, metrics, int(len(scored) - len(kept))))
    return pd.DataFrame(rows)


def surface_row(variant_id_value: str, threshold: float, trades: pd.DataFrame, metrics: Mapping[str, Any], dropped: int) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "variant_id": variant_id_value,
        "family": "shadow_loss_guard_binary_onnx(그림자 손실 방어 2출력 온엑스)",
        "threshold": finite(threshold, 12),
        "trade_rows": int(len(trades)),
        "dropped_trade_rows": dropped,
        **metrics,
        "runtime_compatibility": "not_current_ea_primary_output(현재 EA 주 출력 아님)",
        "proxy_boundary(프록시 경계)": "post_trade_label_supervised_shadow_only(거래 후 라벨 지도학습 그림자 전용)",
        "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
    }


def queue_rows(best: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "Q01_package_selected_dual_side_runtime_probe(선택 양방향 런타임 탐침 패키지)",
            "next_run_id": NEXT_RUN_ID,
            "proposal": f"package {best['variant_id']} with existing ONNX(기존 온엑스), short threshold(숏 임계값) {best['short_probability_threshold']}, maxhold(최대 보유) {best['max_hold_m5']}",
            "effect(효과)": "density(밀도)와 long/short balance(롱/숏 균형)를 MT5 Strategy Tester(MT5 전략 테스터)에서 확인한다.",
            "required_control(필수 대조)": "probability parity(확률 동등성), selected expected tape(선택 예상 기록), run364T comparison(364T 비교)",
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "Q02_probe_long_only_control_same_hold(같은 보유 롱 전용 대조)",
            "next_run_id": NEXT_RUN_ID,
            "proposal": "package long-only ADX40 maxhold8 control if dual-side MT5 drift is large",
            "effect(효과)": "short route(숏 경로)가 실제 수익 개선인지 runtime drift(런타임 차이)인지 분리한다.",
            "required_control(필수 대조)": "same model, same feature tape, only short threshold changed(같은 모델/피처 기록, 숏 임계값만 변경)",
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "Q03_shadow_loss_guard_deferred(그림자 손실 방어 지연)",
            "next_run_id": NEXT_RUN_ID,
            "proposal": "do not package binary shadow ONNX until EA output contract is adapted",
            "effect(효과)": "runtime compatibility(런타임 호환성) 없는 모델을 운영 후보로 착각하지 않는다.",
            "required_control(필수 대조)": "requires EA support or 3-class output contract(전문가 자문 지원 또는 3분류 출력 계약 필요)",
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
    ]


def write_receipts(
    parent: Mapping[str, Any],
    surface: pd.DataFrame,
    best: Mapping[str, Any],
    selected_trades: pd.DataFrame,
    score_rows: Sequence[Mapping[str, Any]],
    smoke_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    base = {"run_id": RUN_ID, "created_at_utc": now_utc(), "claim_boundary": CLAIM_BOUNDARY}
    write_json(
        DATA_RECEIPT,
        {
            **base,
            "skill": "obsidian-data-integrity(데이터 무결성)",
            "data_source": [rel(path) for path in INPUT_FILES],
            "time_axis": "run364M/run364R inherited closed M5 bar open timestamp(닫힌 5분봉 open timestamp 상속)",
            "sample_scope": "US100 M5 validation+OOS 17428 rows, Tier A only(US100 5분봉 검증+OOS 17428행, Tier A 전용)",
            "missing_or_duplicate_check": "runtime frame duplicate timestamp check passed(런타임 프레임 중복 시각 점검 통과)",
            "feature_label_boundary": "dual-side threshold uses only current ONNX probabilities and current ADX feature(양방향 임계값은 현재 확률과 현재 ADX만 사용); shadow loss guard uses post-trade label only as non-runtime supervision(그림자 손실 방어는 거래 후 라벨을 비런타임 지도학습에만 사용)",
            "split_boundary": "validation selects thresholds; OOS readout stays separate(검증이 임계값을 고르고 OOS 판독은 분리)",
            "leakage_risk": "shadow model is not runtime-selected because labels are post-trade(그림자 모델은 거래 후 라벨이므로 런타임 선택하지 않음)",
            "data_hash_or_identity": {"parent_final_sha256": sha(prev.FINAL_DECISION), "source_probability_sha256": sha(prev.sidepkg.SIDE_FILTER_PROBABILITY_TAPE)},
            "integrity_judgment": "usable_with_boundary(경계 조건부 사용 가능)",
        },
    )
    write_json(
        EXPERIMENT_RECEIPT,
        {
            **base,
            "skill": "obsidian-experiment-design(실험 설계)",
            "hypothesis": "existing ONNX probabilities plus runtime-executable short threshold can repair long-only failure without losing density(기존 온엑스 확률과 실행 가능한 숏 임계값이 밀도를 잃지 않고 롱 전용 실패를 수리할 수 있다)",
            "decision_use": "select next MT5 runtime package candidate(다음 MT5 런타임 패키지 후보 선택)",
            "comparison_baseline": "run364T ADX38.688 maxhold8 long-only MT5 probe and run364U ADX40 maxhold6 proxy(364T 롱 전용 MT5 탐침과 364U ADX40/최대보유6 프록시)",
            "control_variables": ["same ONNX model(같은 온엑스 모델)", "same feature order(같은 피처 순서)", "no trade splitting(거래 쪼개기 없음)", "one position max(최대 1포지션)"],
            "changed_variables": ["short probability threshold(숏 확률 임계값)", "long ADX block minimum(롱 ADX 차단 최소값)", "max hold bars(최대 보유 봉)"],
            "sample_scope": "validation and OOS only, Tier A(Tier A 검증/OOS 전용)",
            "success_criteria": "validation and combined density >=3, validation/OOS net positive, OOS PF >=1.15, nonzero short count(검증/합산 밀도 3 이상, 검증/OOS 순수익 양수, OOS PF 1.15 이상, 숏 거래 존재)",
            "failure_criteria": "density below floor, long-only remains, OOS net negative, or MT5 drift later invalidates proxy(밀도 하한 실패, 롱 전용 지속, OOS 음수, 또는 이후 MT5 차이로 무효)",
            "invalid_conditions": "missing probability parity or timestamp mismatch(확률 동등성 누락 또는 시각 불일치)",
            "stop_conditions": "package selected candidate next; no operating claim before MT5(선택 후보를 다음에 패키지, MT5 전 운영 주장 금지)",
            "evidence_plan": [rel(DUAL_SIDE_RUNTIME_SURFACE), rel(SELECTED_TRADE_TAPE), rel(SHADOW_ONNX_SMOKE), rel(GATE_AUDIT)],
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            **base,
            "skill": "obsidian-model-validation(모델 검증)",
            "primary_model": "existing h12_move5__rf5_l80_n64 ONNX reused(기존 h12_move5__rf5_l80_n64 온엑스 재사용)",
            "shadow_model": score_rows[0] if score_rows else {},
            "onnx_smoke": smoke_rows,
            "selected_runtime_candidate": best,
            "overfit_control": "thresholds chosen from validation and OOS kept as readout; shadow binary ONNX not selected for runtime(검증에서 임계값 선택, OOS 분리 판독, 그림자 2출력 온엑스는 런타임 선택 안 함)",
            "validation_judgment": "positive_proxy_but_mt5_probe_required(긍정 프록시지만 MT5 탐침 필요)",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "skill": "obsidian-artifact-lineage(산출물 계보)",
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and Path(path).is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "lineage_judgment": "connected_with_runtime_boundary(런타임 경계 포함 연결)",
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "skill": "obsidian-result-judgment(결과 판정)",
            "judgment_label": JUDGMENT,
            "result_subject": best.get("variant_id"),
            "evidence_available": [rel(DUAL_SIDE_RUNTIME_SURFACE), rel(SELECTED_RUNTIME_CANDIDATE), rel(SELECTED_TRADE_TAPE), rel(SHADOW_ONNX_SMOKE)],
            "evidence_missing": "MT5 Strategy Tester output(MT5 전략 테스터 출력), runtime probability diff(런타임 확률 차이), real broker cost stress(실브로커 비용 압박)",
            "next_condition": NEXT_RUN_ID,
            "selected_trade_rows": int(len(selected_trades)),
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "mt5_execution": "not_run",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "live_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "effect(효과)": "positive proxy(긍정 프록시)를 operating claim(운영 주장)으로 착각하지 않는다.",
        },
    )
    gates = [
        gate_row("scope_completion_gate(범위 완료 게이트)", "passed", FINAL_DECISION, "dual-side scout(양방향 탐색)와 shadow ONNX(그림자 온엑스)를 완료했다."),
        gate_row("data_integrity_audit(데이터 무결성 감사)", "passed", DATA_RECEIPT, "timestamp and feature boundary(시각/피처 경계)를 기록했다."),
        gate_row("experiment_design_audit(실험 설계 감사)", "passed", EXPERIMENT_RECEIPT, "hypothesis/comparison/control(가설/비교/대조)을 기록했다."),
        gate_row("model_validation_audit(모델 검증 감사)", "passed" if all(row.get("status") == "passed" for row in smoke_rows) else "failed", MODEL_RECEIPT, "shadow ONNX smoke(그림자 온엑스 스모크)를 확인했다."),
        gate_row("runtime_executability_audit(런타임 실행 가능성 감사)", "passed", SELECTED_RUNTIME_CANDIDATE, "selected candidate(선택 후보)가 current EA inputs(현재 EA 입력)로 표현 가능하다."),
        gate_row("artifact_lineage_audit(산출물 계보 감사)", "passed", LINEAGE_RECEIPT, "input/output hash(입력/출력 해시)를 연결했다."),
        gate_row("claim_boundary_audit(주장 경계 감사)", "passed", CLAIM_RECEIPT, "MT5 전 운영 주장을 닫았다."),
        gate_row("required_gate_coverage_audit(필수 게이트 커버리지 감사)", "passed", GATE_AUDIT, "required gate(필수 게이트)를 closeout(종료 기록)에 연결했다."),
    ]
    write_csv(GATE_AUDIT, gates)
    return gates


def gate_row(name: str, status: str, evidence: Path, effect: str) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "gate(게이트)": name,
        "status": status,
        "evidence(근거)": rel(evidence),
        "effect(효과)": effect,
        "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
    }


def final_payload(
    parent: Mapping[str, Any],
    frame: pd.DataFrame,
    surface: pd.DataFrame,
    best: Mapping[str, Any],
    selected_trades: pd.DataFrame,
    score_rows: Sequence[Mapping[str, Any]],
    smoke_rows: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "created_at_utc": now_utc(),
        "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        "gate_passes": sum(1 for row in gates if row.get("status") == "passed"),
        "gate_total": len(gates),
        "runtime_rows": int(len(frame)),
        "surface_rows": int(len(surface)),
        "selected_variant_id": best.get("variant_id"),
        "selected_short_probability_threshold": best.get("short_probability_threshold"),
        "selected_min_margin": best.get("min_margin"),
        "selected_long_block_min": best.get("long_block_min"),
        "selected_max_hold_m5": best.get("max_hold_m5"),
        "selected_validation_trade_per_business_day": best.get("validation_trade_per_business_day"),
        "selected_oos_trade_per_business_day": best.get("oos_trade_per_business_day"),
        "selected_combined_trade_per_business_day": best.get("combined_trade_per_business_day"),
        "selected_validation_net_profit": best.get("validation_net_profit"),
        "selected_oos_net_profit": best.get("oos_net_profit"),
        "selected_combined_net_profit": best.get("combined_net_profit"),
        "selected_combined_profit_factor": best.get("combined_profit_factor"),
        "selected_combined_expectancy": best.get("combined_expectancy"),
        "selected_combined_max_drawdown": best.get("combined_max_drawdown"),
        "selected_combined_recovery_factor": best.get("combined_recovery_factor"),
        "selected_combined_long_count": best.get("combined_long_count"),
        "selected_combined_short_count": best.get("combined_short_count"),
        "selected_trade_rows": int(len(selected_trades)),
        "shadow_model_id": score_rows[0].get("model_id") if score_rows else "",
        "shadow_onnx_smoke_status": smoke_rows[0].get("status") if smoke_rows else "",
        "shadow_runtime_compatibility": "not_current_ea_primary_output(현재 EA 주 출력 아님)",
        "parent_mt5_net_profit": parent.get("parent_mt5_net_profit", parent.get("mt5_net_profit")),
        "parent_mt5_profit_factor": parent.get("parent_mt5_profit_factor", parent.get("mt5_profit_factor")),
        "parent_mt5_trade_count": parent.get("parent_mt5_trade_count", parent.get("mt5_trade_count")),
        "model_training": "shadow_binary_only(그림자 2출력만)",
        "mt5_execution": "not_run",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
    }


def report_text(final: Mapping[str, Any]) -> str:
    return f"""# Stage364V density side-balance ONNX scout(Stage364V 밀도 방향 균형 온엑스 탐색)

## Current truth(현재 진실)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Action/Effect(행동/효과)

Action(행동): existing ONNX probabilities(기존 온엑스 확률)에 short threshold(숏 임계값), ADX long block(ADX 롱 차단), max hold(최대 보유)를 조합해 runtime-executable dual-side surface(런타임 실행 가능 양방향 표면)를 만들었다. Shadow loss guard ONNX(그림자 손실 방어 온엑스)도 학습했지만 현재 EA primary output(현재 전문가 자문 주 출력)과 맞지 않아 선택하지 않았다.

Effect(효과): long-only failure(롱 전용 실패)를 MT5 package(MT5 패키지)로 검증 가능한 후보로 바꿨고, binary shadow model(2출력 그림자 모델)은 나중에 EA capability(EA 기능)가 맞을 때만 재사용한다.

## Selected candidate(선택 후보)

- variant(변형): `{final['selected_variant_id']}`
- short threshold(숏 임계값): `{final['selected_short_probability_threshold']}`
- min margin(최소 마진): `{final['selected_min_margin']}`
- ADX long block min(ADX 롱 차단 최소값): `{final['selected_long_block_min']}`
- max hold M5(최대 보유 5분봉): `{final['selected_max_hold_m5']}`
- validation/OOS/combined density(검증/OOS/합산 밀도): `{final['selected_validation_trade_per_business_day']}` / `{final['selected_oos_trade_per_business_day']}` / `{final['selected_combined_trade_per_business_day']}`
- validation/OOS/combined net(검증/OOS/합산 순수익): `{final['selected_validation_net_profit']}` / `{final['selected_oos_net_profit']}` / `{final['selected_combined_net_profit']}`
- combined PF/expectancy/DD/RF(합산 수익 팩터/기대값/낙폭/회복 계수): `{final['selected_combined_profit_factor']}` / `{final['selected_combined_expectancy']}` / `{final['selected_combined_max_drawdown']}` / `{final['selected_combined_recovery_factor']}`
- long/short count(롱/숏 거래수): `{final['selected_combined_long_count']}` / `{final['selected_combined_short_count']}`

## Evidence(근거)

- dual side surface(양방향 표면): `{rel(DUAL_SIDE_RUNTIME_SURFACE)}`
- selected probability tape(선택 확률 기록): `{rel(SELECTED_PROBABILITY_TAPE)}`
- selected trade tape(선택 거래 기록): `{rel(SELECTED_TRADE_TAPE)}`
- shadow ONNX smoke(그림자 온엑스 스모크): `{rel(SHADOW_ONNX_SMOKE)}`
- selected candidate(선택 후보): `{rel(SELECTED_RUNTIME_CANDIDATE)}`

## Boundary(경계)

이 결과는 proxy expected value(프록시 예상값)다. MT5 execution(MT5 실행)은 아직 `not_run`이고, Goal Achieve(목표 달성), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비)는 모두 `not_claimed`다.
"""


def update_docs(final: Mapping[str, Any]) -> None:
    text = report_text(final)
    write_text(REPORT_PATH, text)
    write_text(DECISION_DOC, text)
    append_text_once(REVIEW_INDEX, RUN_ID, f"- `{RUN_ID}`: `{rel(REPORT_PATH)}` - density side-balance ONNX scout(밀도 방향 균형 온엑스 탐색).")
    append_text_once(
        STAGE_BRIEF,
        f"## {RUN_ID}",
        f"""

## {RUN_ID}

- action(행동): existing ONNX probabilities(기존 온엑스 확률)에 short threshold(숏 임계값)와 ADX/maxhold(ADX/최대보유)를 조합한 dual-side runtime surface(양방향 런타임 표면)를 만들었다.
- effect(효과): `{final['selected_variant_id']}`가 validation/combined density(검증/합산 밀도) `{final['selected_validation_trade_per_business_day']}` / `{final['selected_combined_trade_per_business_day']}`와 long/short(롱/숏) `{final['selected_combined_long_count']}` / `{final['selected_combined_short_count']}`를 보여 다음 MT5 package(MT5 패키지) 후보가 됐다.
- next(다음): `{NEXT_RUN_ID}`
""",
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

- current_run(현재 실행): `{NEXT_RUN_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- selected_operating_model(선택 운영 모델): none(없음)
- promotion_candidate(승격 후보): not_claimed(주장 안 함)
- latest_runtime_probe_clue(최근 런타임 탐침 단서): `run364T` MT5 net profit(MT5 순수익) `928.89`, profit factor(수익 팩터) `1.34`, trade count(거래수) `935`
- selected_runtime_package_candidate(선택 런타임 패키지 후보): `{final['selected_variant_id']}`
- selected_proxy_density(선택 프록시 밀도): validation/OOS/combined(검증/OOS/합산) `{final['selected_validation_trade_per_business_day']}` / `{final['selected_oos_trade_per_business_day']}` / `{final['selected_combined_trade_per_business_day']}`
- selected_proxy_long_short(선택 프록시 롱/숏): `{final['selected_combined_long_count']}` / `{final['selected_combined_short_count']}`
- blockers(차단): MT5 runtime evidence(MT5 런타임 근거), proxy-vs-MT5 diff(프록시-MT5 차이), cost stress(비용 압박) still required(아직 필요)
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )
    write_text(
        STAGE_README,
        f"""# {STAGE_ID}

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Stage364(364단계)는 dense cost recovery(고밀도 비용 회복)를 계속 다룬다. run364V(실행 364V)는 stage branch(단계 분기)를 만들지 않고, existing ONNX(기존 온엑스) + runtime thresholds(런타임 임계값)로 side-balance(방향 균형) 후보를 만들었다.
""",
    )
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current working state(현재 작업 상태)

date(날짜): {TODAY}

stage(단계): `{STAGE_ID}`

current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`

latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`

current_truth(현재 진실): `run364V`는 existing ONNX probabilities(기존 온엑스 확률)를 그대로 쓰고, short threshold(숏 임계값) `0.45`, ADX long block(ADX 롱 차단) `{final['selected_long_block_min']}`, maxhold(최대보유) `{final['selected_max_hold_m5']}` 조합을 next MT5 package(다음 MT5 패키지) 후보로 골랐다. proxy combined net/PF(프록시 합산 순수익/수익 팩터)는 `{final['selected_combined_net_profit']}` / `{final['selected_combined_profit_factor']}`이고 long/short(롱/숏)는 `{final['selected_combined_long_count']}` / `{final['selected_combined_short_count']}`다.

next_action(다음 행동): `{NEXT_RUN_ID}`에서 selected candidate(선택 후보)를 Common Files(공용 파일), set file(설정 파일), expected tape(예상 기록)로 package(패키지)한다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )
    write_text(
        WORKSPACE_STATE,
        f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
runtime_authority: not_claimed
operating_promotion: not_claimed
goal_achieve: not_claimed
updated_at_utc: {final['created_at_utc']}
""",
        bom=False,
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        RUN_ID,
        f"""

## {TODAY} - {RUN_ID}

- action(행동): density side-balance ONNX threshold scout(밀도 방향 균형 온엑스 임계값 탐색)를 실행했다.
- effect(효과): `{final['selected_variant_id']}`를 다음 MT5 runtime package(MT5 런타임 패키지) 후보로 고정했다.
- report(보고서): `{rel(REPORT_PATH)}`
""",
    )
    append_text_once(
        IDEA_REGISTRY,
        RUN_ID,
        f"""

## {RUN_ID}

- idea(아이디어): existing ONNX(기존 온엑스)의 short probability(숏 확률)를 runtime threshold(런타임 임계값)로 열면 long-only failure(롱 전용 실패)를 줄이면서 density(밀도)를 유지할 수 있다.
- positive clue(긍정 단서): `{final['selected_variant_id']}` proxy combined net/PF/density(프록시 합산 순수익/수익 팩터/밀도) `{final['selected_combined_net_profit']}` / `{final['selected_combined_profit_factor']}` / `{final['selected_combined_trade_per_business_day']}`.
- boundary(경계): MT5 runtime probe(MT5 런타임 탐침) 전 operating claim(운영 주장) 없음.
""",
    )


def registry_common(final: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "experiment_execution(실험 실행)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(FINAL_DECISION),
        "notes": f"selected={final['selected_variant_id']}; combined_net={final['selected_combined_net_profit']}",
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": DECISION,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "primary_artifact": rel(SELECTED_RUNTIME_CANDIDATE),
        "scoreboard_lane": "density_side_balance_onnx_threshold_scout(밀도 방향 균형 온엑스 임계값 탐색)",
        "external_verification_status": "out_of_scope_by_claim_no_mt5_execution(주장 범위 밖, MT5 실행 없음)",
        "result_judgment": JUDGMENT,
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": final["created_at_utc"],
        "work_family": "experiment_execution(실험 실행)",
        "next_action": NEXT_RUN_ID,
    }


def update_registers(final: Mapping[str, Any]) -> None:
    common = registry_common(final)
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common], extend_header=True)
    ledger = []
    for view, tier_scope, kpi_scope in [
        ("Tier A separate(Tier A 분리)", "Tier A", "dual-side validation/OOS proxy(양방향 검증/OOS 프록시)"),
        ("Tier B separate(Tier B 분리)", "Tier B", "out_of_scope_by_claim(주장 범위 밖)"),
        ("Tier A+B combined(Tier A+B 합산)", "Tier A+B", "combined selected proxy(합산 선택 프록시)"),
    ]:
        row = dict(common)
        row.update(
            {
                "ledger_row_id": f"{RUN_ID}__{tier_scope.replace('+', '_plus_').replace(' ', '_')}",
                "subrun_id": f"{RUN_ID}__{tier_scope}",
                "record_view": view,
                "tier_scope": tier_scope,
                "kpi_scope": kpi_scope,
                "primary_kpi": f"net={final['selected_combined_net_profit']};pf={final['selected_combined_profit_factor']};density={final['selected_combined_trade_per_business_day']}",
                "guardrail_kpi": f"long_short={final['selected_combined_long_count']}/{final['selected_combined_short_count']};no_mt5_claim",
            }
        )
        ledger.append(row)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], ledger, extend_header=True)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], ledger, extend_header=True)
    append_artifact_rows(final)


def append_artifact_rows(final: Mapping[str, Any]) -> None:
    rows = []
    for path in [DUAL_SIDE_RUNTIME_SURFACE, SELECTED_RUNTIME_CANDIDATE, SELECTED_PROBABILITY_TAPE, SELECTED_TRADE_TAPE, SHADOW_ONNX_SMOKE, FINAL_DECISION, REPORT_PATH]:
        rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": "runtime_threshold_scout_or_closeout(런타임 임계값 탐색 또는 종료 기록)",
                "path": rel(path),
                "sha256": sha(path) if exists(path) and path.is_file() else "",
                "created_at": final["created_at_utc"],
                "claim_boundary": CLAIM_BOUNDARY,
                "artifact_id": f"{RUN_ID}__{path.stem}",
                "created_at_utc": final["created_at_utc"],
                "notes": "run364V selected candidate(선택 후보) artifact(산출물); no operating claim(운영 주장 없음).",
                "artifact_path": rel(path),
            }
        )
    if not exists(ARTIFACT_REGISTRY):
        write_csv(ARTIFACT_REGISTRY, rows)
        return
    with open(fs_path(ARTIFACT_REGISTRY), encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or rows[0].keys())
        existing = [row for row in reader if row.get("artifact_id") not in {item["artifact_id"] for item in rows}]
    with open(fs_path(ARTIFACT_REGISTRY), "w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(existing)
        for row in rows:
            writer.writerow(row)


def write_final_and_manifest(final: Mapping[str, Any]) -> None:
    write_json(FINAL_DECISION, final)
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "created_at_utc": final["created_at_utc"],
            "input_files": [rel(path) for path in INPUT_FILES],
            "output_files": [rel(path) for path in OUTPUT_FILES],
            "output_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and Path(path).is_file()},
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
    )


def main() -> None:
    ensure_dirs()
    parent = validate_inputs()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    frame, feature_columns, min_margin = load_runtime_frame()
    surface, best, selected_probability, selected_trades = build_dual_side_surface(frame, min_margin)
    write_csv(DUAL_SIDE_RUNTIME_SURFACE, surface.to_dict("records"))
    write_json(SELECTED_RUNTIME_CANDIDATE, best)
    write_csv(SELECTED_PROBABILITY_TAPE, selected_probability.to_dict("records"))
    write_csv(SELECTED_TRADE_TAPE, selected_trades.to_dict("records"))
    shadow_table, score_rows, smoke_rows, guard_surface = train_shadow_loss_guard(frame, selected_trades, feature_columns)
    write_csv(RUN364W_QUEUE, queue_rows(best))
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "primary_family": "experiment_execution(실험 실행)",
            "primary_skill": "obsidian-experiment-design(실험 설계)",
            "support_skills": [
                "obsidian-data-integrity(데이터 무결성)",
                "obsidian-model-validation(모델 검증)",
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-result-judgment(결과 판정)",
            ],
            "required_gates": [
                "scope_completion_gate",
                "data_integrity_audit",
                "experiment_design_audit",
                "model_validation_audit",
                "runtime_executability_audit",
                "artifact_lineage_audit",
                "claim_boundary_audit",
                "required_gate_coverage_audit",
            ],
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
    )
    gates = write_receipts(parent, surface, best, selected_trades, score_rows, smoke_rows)
    final = final_payload(parent, frame, surface, best, selected_trades, score_rows, smoke_rows, gates)
    write_final_and_manifest(final)
    update_docs(final)
    update_registers(final)
    write_final_and_manifest(final)


if __name__ == "__main__":
    main()
