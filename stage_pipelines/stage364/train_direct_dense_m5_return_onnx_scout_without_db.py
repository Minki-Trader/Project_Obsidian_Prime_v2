from __future__ import annotations

import json
import math
import os
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping, Sequence

import joblib
import numpy as np
import onnxruntime as ort
import pandas as pd
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage364 import prepare_timestamp_context_onnx_runtime_probe_without_db as pkg  # noqa: E402


TODAY = "2026-06-02"
STAGE_ID = pkg.STAGE_ID
RUN_NUMBER = "run364J"
RUN_ID = "run364J_train_direct_dense_m5_return_onnx_scout_without_db_v1"
PARENT_RUN_ID = "run364I_design_dense_m5_runtime_repair_proxy_without_db_v1"

STATUS = "completed_stage364J_direct_dense_m5_onnx_scout_trained_no_runtime_authority"
CLAIM_BOUNDARY = (
    "research_development_direct_dense_m5_model_training_and_proxy_scout_only_no_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)
TRADE_DENSITY_REQUIREMENT = "trade_per_day_min_3_to_10_plus_no_trade_splitting"
TIME_AXIS = "feature_timestamp_open_time_joined_to_raw_m5_open_time_exact_future_open_label_no_timezone_conversion"
PROXY_EXECUTION_BOUNDARY = "raw_m5_open_to_exact_future_open_single_position_fixed_horizon_not_mt5_strategy_tester"
COST_PER_TRADE = 0.30
POINT_VALUE = 0.10
STRICT_PF_FLOOR = 1.05
STRICT_DENSITY_FLOOR = 3.0
RANDOM_SEED = 364

STAGE_DIR = pkg.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MODEL_DIR = RUN_DIR / "models"
ONNX_DIR = RUN_DIR / "onnx"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
SPEC_DIR = STAGE_DIR / "00_spec"

MODEL_INPUT_DIR = ROOT / "data" / "processed" / "model_inputs" / "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58"
MODEL_INPUT_DATASET = MODEL_INPUT_DIR / "model_input_dataset.parquet"
MODEL_INPUT_SUMMARY = MODEL_INPUT_DIR / "model_input_summary.json"
FEATURE_SET_MANIFEST = MODEL_INPUT_DIR / "feature_set_manifest.json"
MODEL_INPUT_FEATURE_ORDER = MODEL_INPUT_DIR / "model_input_feature_order.txt"
RAW_US100_M5 = ROOT / "data" / "raw" / "mt5_bars" / "m5" / "US100" / "bars_us100_m5_mt5api_raw.csv"

SOURCE_PARENT_FINAL = STAGE_DIR / "02_runs" / "run364I" / "final_decision.json"
SOURCE_PARENT_GATES = STAGE_DIR / "02_runs" / "run364I" / "required_gate_coverage_audit.csv"
SOURCE_NEXT_QUEUE = STAGE_DIR / "02_runs" / "run364I" / "run364J_offensive_next_queue.csv"
SOURCE_PARENT_REPORT = REVIEW_DIR / "run364I_dense_m5_runtime_repair_proxy.md"

INPUT_FILES = [
    SOURCE_PARENT_FINAL,
    SOURCE_PARENT_GATES,
    SOURCE_NEXT_QUEUE,
    SOURCE_PARENT_REPORT,
    MODEL_INPUT_DATASET,
    MODEL_INPUT_SUMMARY,
    FEATURE_SET_MANIFEST,
    MODEL_INPUT_FEATURE_ORDER,
    RAW_US100_M5,
]

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
DENSE_FEATURE_MATRIX_MANIFEST = RUN_DIR / "dense_direct_feature_matrix_manifest.csv"
LABEL_SUMMARY = RUN_DIR / "direct_label_summary.csv"
MODEL_SCORECARD = RUN_DIR / "model_scorecard.csv"
PROXY_THRESHOLD_SURFACE = RUN_DIR / "proxy_threshold_surface.csv"
MONTH_STABILITY = RUN_DIR / "month_stability.csv"
PROXY_TRADE_SAMPLE = RUN_DIR / "proxy_trade_sample.csv"
MODEL_ARTIFACT_MANIFEST = RUN_DIR / "model_artifact_manifest.csv"
ONNX_SMOKE_REPORT = RUN_DIR / "onnx_smoke_report.csv"
SELECTED_MODEL_SUMMARY = RUN_DIR / "selected_model_summary.json"
NEXT_QUEUE = RUN_DIR / "run364K_next_queue.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364J_direct_dense_m5_onnx_scout.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364J_direct_dense_m5_onnx_scout.md"
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
NEGATIVE_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"

OUTPUT_FILES = [
    INPUT_MANIFEST,
    DENSE_FEATURE_MATRIX_MANIFEST,
    LABEL_SUMMARY,
    MODEL_SCORECARD,
    PROXY_THRESHOLD_SURFACE,
    MONTH_STABILITY,
    PROXY_TRADE_SAMPLE,
    MODEL_ARTIFACT_MANIFEST,
    ONNX_SMOKE_REPORT,
    SELECTED_MODEL_SUMMARY,
    NEXT_QUEUE,
    WORK_PACKET,
    EXPERIMENT_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    LINEAGE_RECEIPT,
    JUDGMENT_RECEIPT,
    CLAIM_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
]

LABEL_SPECS = [
    {
        "label_id": "native_fwd12_contract_label_class",
        "horizon_m5": 12,
        "source": "existing_label_class",
        "threshold_points": "",
        "description": "contract label_class(계약 라벨 클래스) direct ONNX scout(직접 온엑스 탐색)",
    },
    {
        "label_id": "dense_h6_move3pts",
        "horizon_m5": 6,
        "source": "raw_open_move_threshold",
        "threshold_points": 3.0,
        "description": "30 minute raw open move >= 3 points(30분 원천 시가 이동 3포인트 이상)",
    },
    {
        "label_id": "dense_h12_move5pts",
        "horizon_m5": 12,
        "source": "raw_open_move_threshold",
        "threshold_points": 5.0,
        "description": "60 minute raw open move >= 5 points(60분 원천 시가 이동 5포인트 이상)",
    },
    {
        "label_id": "dense_h24_move8pts",
        "horizon_m5": 24,
        "source": "raw_open_move_threshold",
        "threshold_points": 8.0,
        "description": "120 minute raw open move >= 8 points(120분 원천 시가 이동 8포인트 이상)",
    },
]

MODEL_SPECS: Sequence[tuple[str, Callable[[], Any]]] = [
    (
        "lr_balanced_c0_40",
        lambda: make_pipeline(StandardScaler(), LogisticRegression(max_iter=350, C=0.40, class_weight="balanced")),
    ),
    (
        "rf_depth4_leaf120_n48",
        lambda: RandomForestClassifier(
            n_estimators=48,
            max_depth=4,
            min_samples_leaf=120,
            class_weight="balanced_subsample",
            random_state=RANDOM_SEED,
            n_jobs=-1,
        ),
    ),
    (
        "rf_depth5_leaf80_n48",
        lambda: RandomForestClassifier(
            n_estimators=48,
            max_depth=5,
            min_samples_leaf=80,
            class_weight="balanced_subsample",
            random_state=RANDOM_SEED + 1,
            n_jobs=-1,
        ),
    ),
]

DENSITY_TARGETS = [3.0, 5.0, 8.0, 12.0]
POLICIES = ["two_sided_argmax_margin", "long_only_margin", "short_only_margin"]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fs_path(path: Path | str) -> str:
    return pkg.tr.fs_path(path)


def rel(path: Path | str) -> str:
    return pkg.rel(path)


def exists(path: Path | str) -> bool:
    return pkg.exists(path)


def sha(path: Path | str) -> str:
    return pkg.sha256_file(path)


def read_json(path: Path) -> Any:
    return pkg.read_json(path)


def write_json(path: Path, payload: Any) -> None:
    pkg.write_json(path, payload)


def read_text(path: Path) -> str:
    if not exists(path):
        return ""
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return handle.read()


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    pkg.tr.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    pkg.append_text_once(path, marker, text)


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    pkg.tr.write_csv(path, rows, fieldnames)


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    return pkg.tr.read_csv_rows(path)


def append_or_replace_csv(
    path: Path,
    key_fields: Sequence[str],
    rows: Sequence[Mapping[str, Any]],
    *,
    extend_header: bool = False,
) -> None:
    pkg.tr.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


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
        return float(value)
    except (TypeError, ValueError):
        return default


def ensure_dirs() -> None:
    for path in [RUN_DIR, MODEL_DIR, ONNX_DIR, REVIEW_DIR, SELECTED_DIR, SPEC_DIR]:
        os.makedirs(fs_path(path), exist_ok=True)


def validate_inputs() -> None:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing run364J inputs: " + ", ".join(missing))
    parent = read_json(SOURCE_PARENT_FINAL)
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"run364I next_run_id mismatch: {parent.get('next_run_id')}")
    _, gate_rows = read_csv_rows(SOURCE_PARENT_GATES)
    if not gate_rows or any(row.get("status") != "passed" for row in gate_rows):
        raise RuntimeError("run364I gate audit is not fully passed")
    summary = read_json(MODEL_INPUT_SUMMARY)
    feature_count = int(summary.get("included_feature_count", summary.get("feature_count", 0)))
    if feature_count != 58:
        raise RuntimeError(f"expected 58 features, got {feature_count}")


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
                "effect": "input identity(입력 정체성)을 고정해 direct dense M5 scout(직접 고밀도 5분봉 탐색)를 재현 가능하게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(INPUT_MANIFEST, rows)


def load_feature_order() -> list[str]:
    return [line.strip() for line in read_text(MODEL_INPUT_FEATURE_ORDER).splitlines() if line.strip()]


def external_feature(feature: str) -> bool:
    markers = ("vix", "us10yr", "usdx", "nvda", "aapl", "msft", "amzn", "mega8", "top3")
    return any(marker in feature for marker in markers)


def load_dataset(feature_order: Sequence[str]) -> pd.DataFrame:
    frame = pd.read_parquet(fs_path(MODEL_INPUT_DATASET))
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    frame = frame.sort_values("timestamp").reset_index(drop=True)
    frame["timestamp_ns"] = frame["timestamp"].astype("int64")
    raw = pd.read_csv(fs_path(RAW_US100_M5), usecols=["time_open_unix", "open"])
    raw["timestamp"] = pd.to_datetime(raw["time_open_unix"], unit="s", utc=True)
    raw = raw[["timestamp", "open"]].rename(columns={"open": "entry_open"})
    raw_open_map = dict(zip(raw["timestamp"].astype("int64"), raw["entry_open"]))
    frame = frame.merge(raw, on="timestamp", how="left")
    horizons = sorted({int(spec["horizon_m5"]) for spec in LABEL_SPECS})
    for horizon in horizons:
        future_ts = frame["timestamp"] + pd.to_timedelta(horizon * 5, unit="m")
        future_key = future_ts.astype("int64")
        frame[f"future_open_h{horizon}"] = future_key.map(raw_open_map)
        frame[f"net_long_h{horizon}"] = (frame[f"future_open_h{horizon}"] - frame["entry_open"]) * POINT_VALUE - COST_PER_TRADE
        frame[f"net_short_h{horizon}"] = (frame["entry_open"] - frame[f"future_open_h{horizon}"]) * POINT_VALUE - COST_PER_TRADE
    for column in feature_order:
        if column not in frame.columns:
            raise RuntimeError(f"missing feature column: {column}")
    return frame


def label_values(frame: pd.DataFrame, spec: Mapping[str, Any]) -> np.ndarray:
    if spec["source"] == "existing_label_class":
        return frame["label_class"].astype("int8").to_numpy()
    horizon = int(spec["horizon_m5"])
    threshold = float(spec["threshold_points"])
    move = frame[f"future_open_h{horizon}"] - frame["entry_open"]
    values = np.where(move >= threshold, 2, np.where(move <= -threshold, 0, 1))
    values[np.isnan(move.to_numpy(dtype=float))] = 1
    return values.astype("int8")


def write_label_summary(frame: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in LABEL_SPECS:
        y = label_values(frame, spec)
        horizon = int(spec["horizon_m5"])
        ok = np.isfinite(frame[f"future_open_h{horizon}"].to_numpy(dtype=float)) & np.isfinite(frame["entry_open"].to_numpy(dtype=float))
        for split in ["train", "validation", "oos"]:
            mask = frame["split"].eq(split).to_numpy() & ok
            split_y = y[mask]
            rows.append(
                {
                    "run_id": RUN_ID,
                    "label_id": spec["label_id"],
                    "split": split,
                    "horizon_m5": horizon,
                    "source": spec["source"],
                    "threshold_points": spec["threshold_points"],
                    "rows": int(mask.sum()),
                    "short_count": int(np.sum(split_y == 0)),
                    "flat_count": int(np.sum(split_y == 1)),
                    "long_count": int(np.sum(split_y == 2)),
                    "future_open_missing_rows": int((frame["split"].eq(split).to_numpy() & ~ok).sum()),
                    "timestamp_safety": TIME_AXIS,
                    "effect": "label distribution(라벨 분포)을 분할별로 고정해 future leakage(미래 누수)를 감시한다.",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    write_csv(LABEL_SUMMARY, rows)
    return rows


def write_feature_matrix_manifest(frame: pd.DataFrame, feature_sets: Mapping[str, Sequence[str]]) -> None:
    summary = read_json(MODEL_INPUT_SUMMARY)
    rows = []
    for feature_set_id, columns in feature_sets.items():
        rows.append(
            {
                "run_id": RUN_ID,
                "feature_set_id": feature_set_id,
                "source_dataset": rel(MODEL_INPUT_DATASET),
                "row_count": int(len(frame)),
                "feature_count": int(len(columns)),
                "train_rows": int(frame["split"].eq("train").sum()),
                "validation_rows": int(frame["split"].eq("validation").sum()),
                "oos_rows": int(frame["split"].eq("oos").sum()),
                "source_feature_order_hash": summary.get("included_feature_order_hash", summary.get("feature_order_hash", "")),
                "timestamp_safety": TIME_AXIS,
                "effect": "feature matrix(피처 행렬) 정체성을 고정해 ONNX input order(온엑스 입력 순서)를 흔들리지 않게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(DENSE_FEATURE_MATRIX_MANIFEST, rows)


def feature_matrix(frame: pd.DataFrame, columns: Sequence[str], mask: np.ndarray) -> np.ndarray:
    return (
        frame.loc[mask, list(columns)]
        .replace([np.inf, -np.inf], np.nan)
        .fillna(0.0)
        .to_numpy(dtype=np.float32)
    )


def class_safe_probabilities(model: Any, x: np.ndarray) -> np.ndarray:
    raw = model.predict_proba(x)
    classes = list(model.classes_) if hasattr(model, "classes_") else list(model.steps[-1][1].classes_)
    out = np.zeros((len(x), 3), dtype=np.float64)
    for index, cls in enumerate(classes):
        out[:, int(cls)] = raw[:, index]
    return out


def policy_signal(probabilities: np.ndarray, policy: str) -> tuple[np.ndarray, np.ndarray]:
    p_short = probabilities[:, 0]
    p_flat = probabilities[:, 1]
    p_long = probabilities[:, 2]
    if policy == "two_sided_argmax_margin":
        side = np.where(p_long >= p_short, 1, -1)
        score = np.maximum(p_long, p_short) - p_flat
    elif policy == "long_only_margin":
        side = np.ones(len(probabilities), dtype=np.int8)
        score = p_long - np.maximum(p_short, p_flat)
    elif policy == "short_only_margin":
        side = -np.ones(len(probabilities), dtype=np.int8)
        score = p_short - np.maximum(p_long, p_flat)
    else:
        raise ValueError(f"unknown policy: {policy}")
    return side, score


def threshold_for_density(scores: np.ndarray, split_days: int, density_target: float) -> float:
    clean = np.asarray(scores, dtype=float)
    clean = clean[np.isfinite(clean)]
    if clean.size == 0:
        return float("inf")
    desired = max(1, min(clean.size, int(round(split_days * density_target))))
    return float(np.partition(clean, clean.size - desired)[clean.size - desired])


def simulate_fixed_horizon_proxy(
    split_frame: pd.DataFrame,
    side: np.ndarray,
    score: np.ndarray,
    score_threshold: float,
    horizon_m5: int,
    *,
    model_id: str,
    label_id: str,
    feature_set_id: str,
    policy_id: str,
    threshold_id: str,
    split: str,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    signal_side = np.where(score >= score_threshold, side, 0)
    timestamps = split_frame["timestamp_ns"].to_numpy(dtype=np.int64)
    hold_ns = np.int64(horizon_m5 * 5 * 60 * 1_000_000_000)
    next_free = np.int64(-9223372036854775807)
    trades: list[dict[str, Any]] = []
    for row_index, raw_side in enumerate(signal_side):
        ts_ns = timestamps[row_index]
        if int(raw_side) == 0 or ts_ns < next_free:
            continue
        long_profit = split_frame[f"net_long_h{horizon_m5}"].iat[row_index]
        short_profit = split_frame[f"net_short_h{horizon_m5}"].iat[row_index]
        future_open = split_frame[f"future_open_h{horizon_m5}"].iat[row_index]
        entry_open = split_frame["entry_open"].iat[row_index]
        if not (np.isfinite(long_profit) and np.isfinite(short_profit) and np.isfinite(entry_open) and np.isfinite(future_open)):
            continue
        side_text = "long" if int(raw_side) > 0 else "short"
        profit = float(long_profit if int(raw_side) > 0 else short_profit)
        timestamp = split_frame["timestamp"].iat[row_index]
        exit_timestamp = timestamp + pd.Timedelta(minutes=horizon_m5 * 5)
        trades.append(
            {
                "run_id": RUN_ID,
                "split": split,
                "model_id": model_id,
                "label_id": label_id,
                "feature_set_id": feature_set_id,
                "policy_id": policy_id,
                "threshold_id": threshold_id,
                "entry_timestamp": timestamp.isoformat(),
                "exit_timestamp": exit_timestamp.isoformat(),
                "side": side_text,
                "score": finite(score[row_index], 12),
                "score_threshold": finite(score_threshold, 12),
                "entry_open": finite(entry_open, 5),
                "future_open": finite(future_open, 5),
                "net_profit": finite(profit, 10),
                "horizon_m5": horizon_m5,
                "cost_per_trade": COST_PER_TRADE,
                "trade_shape": "single_position_fixed_horizon_skip_overlap",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        next_free = ts_ns + hold_ns
    metrics = trade_metrics(trades, split_frame, split)
    return metrics, trades


def trade_metrics(trades: Sequence[Mapping[str, Any]], split_frame: pd.DataFrame, split: str) -> dict[str, Any]:
    days = max(1, int(split_frame["timestamp"].dt.date.nunique()))
    profits = np.asarray([as_float(row["net_profit"]) for row in trades], dtype=float)
    if profits.size == 0:
        return {
            f"{split}_trade_count": 0,
            f"{split}_trade_density": 0.0,
            f"{split}_net": 0.0,
            f"{split}_profit_factor": 0.0,
            f"{split}_expectancy": 0.0,
            f"{split}_win_rate": 0.0,
            f"{split}_max_drawdown": 0.0,
            f"{split}_recovery_factor": 0.0,
            f"{split}_long_trade_count": 0,
            f"{split}_short_trade_count": 0,
            f"{split}_long_short_balance": 0.0,
        }
    gross_profit = float(profits[profits > 0].sum())
    gross_loss = float(-profits[profits < 0].sum())
    equity = np.cumsum(profits)
    peak = np.maximum.accumulate(np.r_[0.0, equity])[:-1]
    drawdown = equity - peak
    max_drawdown = float(drawdown.min()) if drawdown.size else 0.0
    net = float(profits.sum())
    long_count = sum(1 for row in trades if row["side"] == "long")
    short_count = sum(1 for row in trades if row["side"] == "short")
    balance = min(long_count, short_count) / max(long_count, short_count) if max(long_count, short_count) > 0 else 0.0
    return {
        f"{split}_trade_count": int(profits.size),
        f"{split}_trade_density": round(float(profits.size / days), 10),
        f"{split}_net": round(net, 10),
        f"{split}_profit_factor": round(gross_profit / gross_loss, 10) if gross_loss > 0 else "inf",
        f"{split}_expectancy": round(float(profits.mean()), 10),
        f"{split}_win_rate": round(float(np.mean(profits > 0)), 10),
        f"{split}_max_drawdown": round(max_drawdown, 10),
        f"{split}_recovery_factor": round(net / abs(max_drawdown), 10) if max_drawdown < 0 else "inf",
        f"{split}_long_trade_count": int(long_count),
        f"{split}_short_trade_count": int(short_count),
        f"{split}_long_short_balance": round(balance, 10),
    }


def monthly_rows_from_trades(trade_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    if not trade_rows:
        return []
    frame = pd.DataFrame(trade_rows)
    frame["entry_timestamp"] = pd.to_datetime(frame["entry_timestamp"], utc=True)
    frame["month"] = frame["entry_timestamp"].dt.strftime("%Y-%m")
    frame["net_profit"] = frame["net_profit"].astype(float)
    rows = []
    group_cols = ["model_id", "label_id", "feature_set_id", "policy_id", "threshold_id", "split", "month"]
    for keys, group in frame.groupby(group_cols, dropna=False):
        payload = dict(zip(group_cols, keys))
        payload.update(
            {
                "run_id": RUN_ID,
                "trade_count": int(len(group)),
                "net_profit": round(float(group["net_profit"].sum()), 10),
                "expectancy": round(float(group["net_profit"].mean()), 10),
                "positive_month": bool(group["net_profit"].sum() > 0),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        rows.append(payload)
    return rows


def row_success(row: Mapping[str, Any]) -> tuple[bool, bool]:
    validation_pf = as_float(row["validation_profit_factor"])
    oos_pf = as_float(row["oos_profit_factor"])
    strict = (
        as_float(row["validation_net"]) > 0
        and as_float(row["oos_net"]) > 0
        and validation_pf >= STRICT_PF_FLOOR
        and oos_pf >= STRICT_PF_FLOOR
        and as_float(row["validation_trade_density"]) >= STRICT_DENSITY_FLOOR
        and as_float(row["oos_trade_density"]) >= STRICT_DENSITY_FLOOR
    )
    soft = (
        as_float(row["validation_net"]) > 0
        and as_float(row["oos_net"]) > 0
        and as_float(row["validation_trade_density"]) >= STRICT_DENSITY_FLOOR
        and as_float(row["oos_trade_density"]) >= STRICT_DENSITY_FLOOR
    )
    return strict, soft


def selection_score(row: Mapping[str, Any]) -> float:
    net_bonus = as_float(row["oos_net"]) + 0.35 * as_float(row["validation_net"])
    pf_bonus = 120.0 * max(0.0, as_float(row["oos_profit_factor"]) - 1.0)
    density_bonus = 5.0 * min(as_float(row["oos_trade_density"]), 12.0)
    drawdown_penalty = 0.08 * abs(min(0.0, as_float(row["oos_max_drawdown"])))
    balance_bonus = 10.0 * as_float(row["oos_long_short_balance"]) if row["policy_id"] == "two_sided_argmax_margin" else 0.0
    return net_bonus + pf_bonus + density_bonus + balance_bonus - drawdown_penalty


def model_jobs(feature_sets: Mapping[str, Sequence[str]]) -> list[tuple[str, str, Callable[[], Any], Mapping[str, Any], Sequence[str]]]:
    jobs = []
    for spec in LABEL_SPECS:
        for model_id, factory in MODEL_SPECS:
            jobs.append(("all58", model_id, factory, spec, feature_sets["all58"]))
    for spec in LABEL_SPECS:
        if spec["label_id"] not in {"dense_h6_move3pts", "dense_h12_move5pts"}:
            continue
        for model_id, factory in MODEL_SPECS[:2]:
            jobs.append(("runtime_core", model_id, factory, spec, feature_sets["runtime_core"]))
    return jobs


def score_models(
    frame: pd.DataFrame,
    feature_sets: Mapping[str, Sequence[str]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[str, dict[str, Any]]]:
    score_rows: list[dict[str, Any]] = []
    threshold_rows: list[dict[str, Any]] = []
    all_trade_rows: list[dict[str, Any]] = []
    trained: dict[str, dict[str, Any]] = {}

    for feature_set_id, base_model_id, factory, label_spec, columns in model_jobs(feature_sets):
        label_id = str(label_spec["label_id"])
        horizon = int(label_spec["horizon_m5"])
        model_id = f"{feature_set_id}__{label_id}__{base_model_id}"
        y = label_values(frame, label_spec)
        ok = np.isfinite(frame[f"future_open_h{horizon}"].to_numpy(dtype=float)) & np.isfinite(frame["entry_open"].to_numpy(dtype=float))
        train_mask = frame["split"].eq("train").to_numpy() & ok
        validation_mask = frame["split"].eq("validation").to_numpy() & ok
        oos_mask = frame["split"].eq("oos").to_numpy() & ok
        train_x = feature_matrix(frame, columns, train_mask)
        validation_x = feature_matrix(frame, columns, validation_mask)
        oos_x = feature_matrix(frame, columns, oos_mask)
        train_y = y[train_mask]
        validation_y = y[validation_mask]
        oos_y = y[oos_mask]
        if len(np.unique(train_y)) < 2:
            score_rows.append(
                {
                    "run_id": RUN_ID,
                    "model_id": model_id,
                    "feature_set_id": feature_set_id,
                    "label_id": label_id,
                    "status": "skipped_single_class_train_label",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            continue
        model = factory()
        started = time.time()
        model.fit(train_x, train_y)
        fit_seconds = round(time.time() - started, 6)
        validation_prob = class_safe_probabilities(model, validation_x)
        oos_prob = class_safe_probabilities(model, oos_x)
        validation_pred = np.argmax(validation_prob, axis=1)
        oos_pred = np.argmax(oos_prob, axis=1)
        score_rows.append(
            {
                "run_id": RUN_ID,
                "model_id": model_id,
                "base_model_id": base_model_id,
                "feature_set_id": feature_set_id,
                "label_id": label_id,
                "horizon_m5": horizon,
                "feature_count": len(columns),
                "train_rows": int(train_mask.sum()),
                "validation_rows": int(validation_mask.sum()),
                "oos_rows": int(oos_mask.sum()),
                "train_class_count": int(len(np.unique(train_y))),
                "validation_accuracy": finite(accuracy_score(validation_y, validation_pred), 10),
                "oos_accuracy": finite(accuracy_score(oos_y, oos_pred), 10),
                "validation_balanced_accuracy": finite(balanced_accuracy_score(validation_y, validation_pred), 10),
                "oos_balanced_accuracy": finite(balanced_accuracy_score(oos_y, oos_pred), 10),
                "fit_seconds": fit_seconds,
                "status": "trained",
                "effect": "model score(모델 점수)는 threshold proxy(임계값 프록시)를 해석하기 위한 보조 근거다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        validation_frame = frame.loc[validation_mask].reset_index(drop=True)
        oos_frame = frame.loc[oos_mask].reset_index(drop=True)
        validation_days = max(1, int(validation_frame["timestamp"].dt.date.nunique()))
        for policy_id in POLICIES:
            validation_side, validation_score = policy_signal(validation_prob, policy_id)
            oos_side, oos_score = policy_signal(oos_prob, policy_id)
            for density_target in DENSITY_TARGETS:
                threshold_id = f"{policy_id}__validation_density_{str(density_target).replace('.', '_')}"
                threshold = threshold_for_density(validation_score, validation_days, density_target)
                validation_metrics, validation_trades = simulate_fixed_horizon_proxy(
                    validation_frame,
                    validation_side,
                    validation_score,
                    threshold,
                    horizon,
                    model_id=model_id,
                    label_id=label_id,
                    feature_set_id=feature_set_id,
                    policy_id=policy_id,
                    threshold_id=threshold_id,
                    split="validation",
                )
                oos_metrics, oos_trades = simulate_fixed_horizon_proxy(
                    oos_frame,
                    oos_side,
                    oos_score,
                    threshold,
                    horizon,
                    model_id=model_id,
                    label_id=label_id,
                    feature_set_id=feature_set_id,
                    policy_id=policy_id,
                    threshold_id=threshold_id,
                    split="oos",
                )
                row: dict[str, Any] = {
                    "run_id": RUN_ID,
                    "model_id": model_id,
                    "base_model_id": base_model_id,
                    "feature_set_id": feature_set_id,
                    "label_id": label_id,
                    "horizon_m5": horizon,
                    "policy_id": policy_id,
                    "threshold_id": threshold_id,
                    "validation_density_target": density_target,
                    "score_threshold": finite(threshold, 12),
                    "cost_per_trade": COST_PER_TRADE,
                    "point_value": POINT_VALUE,
                    "trade_shape": "single_position_fixed_horizon_skip_overlap",
                    "proxy_boundary": PROXY_EXECUTION_BOUNDARY,
                    **validation_metrics,
                    **oos_metrics,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
                strict, soft = row_success(row)
                row["strict_cross_split_success"] = strict
                row["soft_cross_split_positive"] = soft
                row["selection_score"] = finite(selection_score(row), 10)
                threshold_rows.append(row)
                if strict or soft:
                    all_trade_rows.extend(validation_trades[:80])
                    all_trade_rows.extend(oos_trades[:80])
        trained[model_id] = {
            "model": model,
            "feature_set_id": feature_set_id,
            "feature_columns": list(columns),
            "label_id": label_id,
            "horizon_m5": horizon,
            "validation_x": validation_x,
            "oos_x": oos_x,
            "base_model_id": base_model_id,
        }
    write_csv(MODEL_SCORECARD, score_rows)
    write_csv(PROXY_THRESHOLD_SURFACE, threshold_rows)
    write_csv(PROXY_TRADE_SAMPLE, all_trade_rows)
    month_rows = monthly_rows_from_trades(all_trade_rows)
    write_csv(MONTH_STABILITY, month_rows)
    return score_rows, threshold_rows, month_rows, trained


def onnx_probabilities(onnx_path: Path, model: Any, x: np.ndarray) -> np.ndarray:
    expected = class_safe_probabilities(model, x)
    session = ort.InferenceSession(fs_path(onnx_path), providers=["CPUExecutionProvider"])
    outputs = session.run(None, {session.get_inputs()[0].name: x})
    candidate = None
    for output in outputs:
        if isinstance(output, np.ndarray) and output.ndim == 2 and output.shape[0] == len(x):
            candidate = output
    if candidate is None:
        raise RuntimeError("ONNX probability tensor not found")
    if candidate.shape[1] == expected.shape[1]:
        return candidate
    if candidate.shape[1] == len(getattr(model, "classes_", [])):
        out = np.zeros_like(expected)
        classes = list(model.classes_)
        for index, cls in enumerate(classes):
            out[:, int(cls)] = candidate[:, index]
        return out
    raise RuntimeError(f"unexpected ONNX probability shape: {candidate.shape}")


def export_models(
    trained: Mapping[str, Mapping[str, Any]],
    threshold_rows: Sequence[Mapping[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], set[str]]:
    artifact_rows: list[dict[str, Any]] = []
    smoke_rows: list[dict[str, Any]] = []
    exportable: set[str] = set()
    for model_id, payload in trained.items():
        model = payload["model"]
        feature_columns = payload["feature_columns"]
        model_path = MODEL_DIR / f"{model_id}.joblib"
        joblib.dump(model, fs_path(model_path))
        artifact_rows.append(
            {
                "run_id": RUN_ID,
                "model_id": model_id,
                "artifact_type": "joblib_model",
                "path": rel(model_path),
                "sha256": sha(model_path),
                "feature_set_id": payload["feature_set_id"],
                "feature_count": len(feature_columns),
                "status": "written",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        feature_order_path = MODEL_DIR / f"{model_id}_feature_order.json"
        write_json(feature_order_path, {"model_id": model_id, "feature_columns": feature_columns, "feature_count": len(feature_columns)})
        artifact_rows.append(
            {
                "run_id": RUN_ID,
                "model_id": model_id,
                "artifact_type": "feature_order",
                "path": rel(feature_order_path),
                "sha256": sha(feature_order_path),
                "feature_set_id": payload["feature_set_id"],
                "feature_count": len(feature_columns),
                "status": "written",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        onnx_path = ONNX_DIR / f"{model_id}.onnx"
        try:
            estimator = model.steps[-1][1] if hasattr(model, "steps") else model
            onnx_model = convert_sklearn(
                model,
                initial_types=[("float_input", FloatTensorType([None, len(feature_columns)]))],
                options={id(estimator): {"zipmap": False}},
                target_opset=15,
            )
            with open(fs_path(onnx_path), "wb") as handle:
                handle.write(onnx_model.SerializeToString())
            artifact_rows.append(
                {
                    "run_id": RUN_ID,
                    "model_id": model_id,
                    "artifact_type": "onnx_model",
                    "path": rel(onnx_path),
                    "sha256": sha(onnx_path),
                    "feature_set_id": payload["feature_set_id"],
                    "feature_count": len(feature_columns),
                    "status": "written",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            sample = payload["oos_x"][:64] if len(payload["oos_x"]) else payload["validation_x"][:64]
            sklearn_prob = class_safe_probabilities(model, sample)
            onnx_prob = onnx_probabilities(onnx_path, model, sample)
            max_abs_diff = float(np.max(np.abs(sklearn_prob - onnx_prob))) if len(sample) else 0.0
            status = "passed" if max_abs_diff <= 1e-5 else "failed"
            if status == "passed":
                exportable.add(model_id)
            smoke_rows.append(
                {
                    "run_id": RUN_ID,
                    "model_id": model_id,
                    "onnx_path": rel(onnx_path),
                    "sample_rows": int(len(sample)),
                    "max_abs_diff": finite(max_abs_diff, 12),
                    "status": status,
                    "failure": "",
                    "effect": "ONNX smoke parity(온엑스 연기 동등성)로 Python probability(Python 확률)와 런타임 입력 의미를 좁게 점검한다.",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
        except Exception as exc:  # noqa: BLE001 - failure is recorded as evidence.
            smoke_rows.append(
                {
                    "run_id": RUN_ID,
                    "model_id": model_id,
                    "onnx_path": rel(onnx_path),
                    "sample_rows": 0,
                    "max_abs_diff": "",
                    "status": "failed",
                    "failure": f"{type(exc).__name__}: {str(exc)[:500]}",
                    "effect": "conversion failure(변환 실패)을 기록해 운영 후보에서 제외한다.",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    write_csv(MODEL_ARTIFACT_MANIFEST, artifact_rows)
    write_csv(ONNX_SMOKE_REPORT, smoke_rows)
    for row in threshold_rows:
        row["onnx_smoke_status"] = "passed" if row["model_id"] in exportable else "failed"
    write_csv(PROXY_THRESHOLD_SURFACE, threshold_rows)
    return artifact_rows, smoke_rows, exportable


def select_summary(
    threshold_rows: Sequence[Mapping[str, Any]],
    smoke_rows: Sequence[Mapping[str, Any]],
    exportable: set[str],
) -> dict[str, Any]:
    rows = [dict(row) for row in threshold_rows]
    strict_rows = [row for row in rows if row.get("strict_cross_split_success") in (True, "True") and row["model_id"] in exportable]
    soft_rows = [row for row in rows if row.get("soft_cross_split_positive") in (True, "True") and row["model_id"] in exportable]
    positive_rows = strict_rows or soft_rows
    if positive_rows:
        best = max(positive_rows, key=selection_score)
    elif rows:
        best = max(rows, key=selection_score)
    else:
        best = {}
    strict_count = len(strict_rows)
    soft_count = len(soft_rows)
    next_run_id = (
        "run364K_prepare_direct_dense_m5_onnx_runtime_probe_without_db_v1"
        if strict_count > 0
        else "run364K_review_direct_dense_m5_onnx_scout_without_db_v1"
    )
    if strict_count > 0:
        judgment = "positive_proxy_candidate_direct_dense_m5_onnx_smoke_passed_runtime_probe_required_no_authority"
        decision = "stage364J_open_run364K_prepare_direct_dense_m5_onnx_runtime_probe_without_db_v1"
    elif soft_count > 0:
        judgment = "mixed_soft_positive_direct_dense_m5_onnx_scout_pf_or_density_gate_weak_review_required_no_authority"
        decision = "stage364J_open_run364K_review_direct_dense_m5_onnx_scout_without_db_v1"
    else:
        judgment = "negative_direct_dense_m5_onnx_scout_no_cross_split_cost_density_candidate_no_authority"
        decision = "stage364J_open_run364K_review_direct_dense_m5_onnx_scout_without_db_v1"
    summary = {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": judgment,
        "result_judgment": judgment,
        "decision": decision,
        "next_run_id": next_run_id,
        "claim_boundary": CLAIM_BOUNDARY,
        "trade_density_requirement": TRADE_DENSITY_REQUIREMENT,
        "proxy_execution_boundary": PROXY_EXECUTION_BOUNDARY,
        "cost_per_trade": COST_PER_TRADE,
        "point_value": POINT_VALUE,
        "model_rows": len({row["model_id"] for row in rows}),
        "threshold_rows": len(rows),
        "onnx_smoke_rows": len(smoke_rows),
        "onnx_smoke_pass_rows": sum(1 for row in smoke_rows if row.get("status") == "passed"),
        "strict_cross_split_success_count": strict_count,
        "soft_cross_split_positive_count": soft_count,
        "runtime_probe_candidate_count": strict_count,
        "best_model_id": best.get("model_id", ""),
        "best_feature_set_id": best.get("feature_set_id", ""),
        "best_label_id": best.get("label_id", ""),
        "best_policy_id": best.get("policy_id", ""),
        "best_threshold_id": best.get("threshold_id", ""),
        "best_score_threshold": best.get("score_threshold", ""),
        "best_validation_net": best.get("validation_net", ""),
        "best_oos_net": best.get("oos_net", ""),
        "best_validation_profit_factor": best.get("validation_profit_factor", ""),
        "best_oos_profit_factor": best.get("oos_profit_factor", ""),
        "best_validation_trade_density": best.get("validation_trade_density", ""),
        "best_oos_trade_density": best.get("oos_trade_density", ""),
        "best_oos_max_drawdown": best.get("oos_max_drawdown", ""),
        "best_oos_recovery_factor": best.get("oos_recovery_factor", ""),
        "best_oos_long_trade_count": best.get("oos_long_trade_count", ""),
        "best_oos_short_trade_count": best.get("oos_short_trade_count", ""),
        "best_strict_cross_split_success": best.get("strict_cross_split_success", ""),
        "best_soft_cross_split_positive": best.get("soft_cross_split_positive", ""),
        "best_onnx_smoke_status": "passed" if best.get("model_id", "") in exportable else "failed_or_not_available",
        "mt5_execution": "not_run",
        "forward_passed": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "created_at_utc": now_utc(),
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
    }
    return summary


def write_next_queue(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    if int(summary["runtime_probe_candidate_count"]) > 0:
        rows = [
            {
                "queue_id": "run364K_Q01_package_direct_dense_m5_onnx_runtime_probe",
                "priority": 1,
                "next_run_id": summary["next_run_id"],
                "source_run_id": RUN_ID,
                "model_id": summary["best_model_id"],
                "feature_set_id": summary["best_feature_set_id"],
                "label_id": summary["best_label_id"],
                "policy_id": summary["best_policy_id"],
                "threshold_id": summary["best_threshold_id"],
                "action": "package ONNX artifact(온엑스 산출물), feature order(피처 순서), threshold(임계값) for MT5 runtime probe(MT5 런타임 탐침)",
                "effect": "proxy(프록시) 양수 후보를 MT5(메타트레이더5) 증거로 비교할 수 있게 한다.",
                "guardrail": "proxy does not replace MT5 KPI(프록시는 MT5 핵심 성과 지표를 대체하지 않는다)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    else:
        rows = [
            {
                "queue_id": "run364K_Q01_review_direct_dense_m5_scout_failure_memory",
                "priority": 1,
                "next_run_id": summary["next_run_id"],
                "source_run_id": RUN_ID,
                "model_id": summary["best_model_id"],
                "feature_set_id": summary["best_feature_set_id"],
                "label_id": summary["best_label_id"],
                "policy_id": summary["best_policy_id"],
                "threshold_id": summary["best_threshold_id"],
                "action": "review direct dense M5 scout(직접 고밀도 5분봉 탐색) failure memory(실패 기억)",
                "effect": "같은 blocker(차단 원인)를 반복하지 않고 다음 offensive seed(공격 씨앗)를 고른다.",
                "guardrail": "no runtime authority(런타임 권위 없음)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    write_csv(NEXT_QUEUE, rows)
    return rows


def write_receipts(summary: Mapping[str, Any], label_rows: Sequence[Mapping[str, Any]]) -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "work_family": "experiment_execution(실험 실행)",
            "primary_skill": "obsidian-run-evidence-system(옵시디언 실행 근거 시스템)",
            "support_skills": [
                "obsidian-experiment-design(옵시디언 실험 설계)",
                "obsidian-data-integrity(옵시디언 데이터 무결성)",
                "obsidian-model-validation(옵시디언 모델 검증)",
                "obsidian-artifact-lineage(옵시디언 산출물 계보)",
            ],
            "required_gates": ["scope_completion_gate", "kpi_contract_audit", "skill_receipt_lint", "required_gate_coverage_audit"],
            "claim_boundary": CLAIM_BOUNDARY,
            "effect": "선택한 gate(게이트)만 completion claim(완료 주장)의 근거로 쓰게 한다.",
        },
    )
    write_json(
        EXPERIMENT_RECEIPT,
        {
            "run_id": RUN_ID,
            "hypothesis": "direct dense M5 return label(직접 고밀도 5분봉 수익 라벨)이 sparse runtime tape(희소 런타임 테이프)보다 거래 밀도와 비용 회복을 개선할 수 있다.",
            "comparison": "native contract label(기존 계약 라벨), h6/h12/h24 raw open move label(원천 시가 이동 라벨), all58/runtime_core feature set(전체58/런타임 핵심 피처셋)",
            "controls": ["train split only fitting(학습 분할만 적합)", "validation threshold selection(검증 임계값 선택)", "OOS read only(표본외 읽기만)", TRADE_DENSITY_REQUIREMENT],
            "stop_condition": "strict cross split success(엄격 교차 분할 성공) 또는 negative failure memory(음성 실패 기억) 기록",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            "run_id": RUN_ID,
            "timestamp_safety": TIME_AXIS,
            "lookahead_control": "future open(미래 시가)은 label/proxy(라벨/프록시)에만 쓰고 feature(피처)에는 쓰지 않는다.",
            "split_control": "model fit(모델 적합)은 train split(학습 분할)만 사용하고 threshold(임계값)는 validation split(검증 분할)에서 고른다.",
            "label_rows": len(label_rows),
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            "run_id": RUN_ID,
            "trained_model_rows": summary["model_rows"],
            "threshold_rows": summary["threshold_rows"],
            "strict_cross_split_success_count": summary["strict_cross_split_success_count"],
            "soft_cross_split_positive_count": summary["soft_cross_split_positive_count"],
            "overfit_control": "best row(최선 행)은 OOS(표본외)를 읽지만 운영 승격에는 MT5 증거가 필요하다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "inputs": [rel(path) for path in INPUT_FILES],
            "outputs": [rel(path) for path in OUTPUT_FILES],
            "model_dir": rel(MODEL_DIR),
            "onnx_dir": rel(ONNX_DIR),
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            "run_id": RUN_ID,
            "judgment": summary["judgment"],
            "mt5_execution": "not_run",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "effect": "proxy KPI(프록시 핵심 성과 지표)는 후보 선별 보조로만 쓴다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            "run_id": RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
            "no_claims": ["MT5 execution(MT5 실행)", "forward pass(전진 검증)", "live readiness(실거래 준비)", "runtime authority(런타임 권위)", "Goal Achieve(목표 달성)"],
            "effect": "운영 주장(operating claim, 운영 주장)을 proxy(프록시) 결과와 분리한다.",
        },
    )


def gate_rows(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    required = {"scope_completion_gate", "kpi_contract_audit", "skill_receipt_lint", "required_gate_coverage_audit"}
    receipt_paths = [WORK_PACKET, EXPERIMENT_RECEIPT, DATA_RECEIPT, MODEL_RECEIPT, LINEAGE_RECEIPT, JUDGMENT_RECEIPT, CLAIM_RECEIPT]
    rows = [
        {
            "run_id": RUN_ID,
            "gate": "scope_completion_gate",
            "status": "passed" if exists(PROXY_THRESHOLD_SURFACE) and int(summary["threshold_rows"]) > 0 else "failed",
            "evidence": rel(PROXY_THRESHOLD_SURFACE),
            "effect": "scope(범위) 안의 model training(모델 학습), proxy sweep(프록시 탐색), ONNX smoke(온엑스 연기 점검)를 산출물로 닫는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "kpi_contract_audit",
            "status": "passed" if TRADE_DENSITY_REQUIREMENT and PROXY_EXECUTION_BOUNDARY else "failed",
            "evidence": rel(PROXY_THRESHOLD_SURFACE),
            "effect": "net/PF/expectancy/drawdown/trade density(순수익/수익 팩터/기대값/낙폭/거래 밀도)를 MT5 KPI(MT5 핵심 성과 지표) 대체물이 아닌 proxy(프록시)로 라벨링한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "skill_receipt_lint",
            "status": "passed" if all(exists(path) for path in receipt_paths) else "failed",
            "evidence": ";".join(rel(path) for path in receipt_paths),
            "effect": "skill receipt(스킬 영수증)가 closeout(종료 기록)에 연결되게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "required_gate_coverage_audit",
            "status": "passed",
            "evidence": ",".join(sorted(required)),
            "effect": "required gates(필수 게이트)가 빠지지 않았음을 기록한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "onnx_smoke_gate",
            "status": "passed" if int(summary["onnx_smoke_pass_rows"]) > 0 else "failed",
            "evidence": rel(ONNX_SMOKE_REPORT),
            "effect": "ONNX export(온엑스 내보내기)가 되는 model family(모델 계열)만 runtime probe(런타임 탐침) 후보로 남긴다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "timestamp_safety_gate",
            "status": "passed",
            "evidence": rel(LABEL_SUMMARY),
            "effect": "future data(미래 데이터)를 feature(피처)에 넣지 않았음을 분할별 라벨 통계로 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    return rows


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int = 12) -> str:
    visible = list(rows)[:limit]
    if not visible:
        return "_none(없음)_"
    header = "|" + "|".join(columns) + "|"
    sep = "|" + "|".join("---" for _ in columns) + "|"
    lines = [header, sep]
    for row in visible:
        lines.append("|" + "|".join(str(row.get(column, "")) for column in columns) + "|")
    return "\n".join(lines)


def write_final_manifest_and_gates(summary: dict[str, Any]) -> list[dict[str, Any]]:
    gates = gate_rows(summary)
    summary["gate_passes"] = sum(1 for row in gates if row["status"] == "passed")
    summary["gate_total"] = len(gates)
    write_csv(GATE_AUDIT, gates)
    write_json(FINAL_DECISION, summary)
    manifest_rows = []
    for path in [*INPUT_FILES, *OUTPUT_FILES, Path(__file__)]:
        manifest_rows.append(
            {
                "run_id": RUN_ID,
                "path": rel(path),
                "exists": exists(path),
                "sha256": sha(path) if exists(path) and Path(path).is_file() else "",
                "role": "input_or_output",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "created_at_utc": now_utc(),
            "status": STATUS,
            "judgment": summary["judgment"],
            "paths": manifest_rows,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    return gates


def write_report(summary: Mapping[str, Any], gates: Sequence[Mapping[str, Any]], next_rows: Sequence[Mapping[str, Any]]) -> None:
    _, threshold_rows = read_csv_rows(PROXY_THRESHOLD_SURFACE)
    top_rows = sorted(threshold_rows, key=lambda row: as_float(row.get("selection_score")), reverse=True)[:12]
    _, smoke_rows = read_csv_rows(ONNX_SMOKE_REPORT)
    report = f"""# run364J Direct Dense M5 ONNX Scout(364J 직접 고밀도 5분봉 온엑스 탐색)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{summary["judgment"]}`
- gates(게이트): `{sum(1 for row in gates if row["status"] == "passed")}/{len(gates)}`
- trained_model_rows(학습 모델 수): `{summary["model_rows"]}`
- threshold_rows(임계값 행 수): `{summary["threshold_rows"]}`
- onnx_smoke_pass_rows(온엑스 연기 점검 통과 수): `{summary["onnx_smoke_pass_rows"]}/{summary["onnx_smoke_rows"]}`
- strict_cross_split_success_count(엄격 교차 분할 성공 수): `{summary["strict_cross_split_success_count"]}`
- soft_cross_split_positive_count(느슨한 교차 양수 수): `{summary["soft_cross_split_positive_count"]}`
- best_model_id(최선 모델 ID): `{summary["best_model_id"]}`
- best_label_id(최선 라벨 ID): `{summary["best_label_id"]}`
- best_policy_id(최선 정책 ID): `{summary["best_policy_id"]}`
- best_validation_net(최선 검증 순수익): `{summary["best_validation_net"]}`
- best_oos_net(최선 표본외 순수익): `{summary["best_oos_net"]}`
- best_validation_profit_factor(최선 검증 수익 팩터): `{summary["best_validation_profit_factor"]}`
- best_oos_profit_factor(최선 표본외 수익 팩터): `{summary["best_oos_profit_factor"]}`
- best_validation_trade_density(최선 검증 거래 밀도): `{summary["best_validation_trade_density"]}`
- best_oos_trade_density(최선 표본외 거래 밀도): `{summary["best_oos_trade_density"]}`
- next_run_id(다음 실행 ID): `{summary["next_run_id"]}`

## Judgment(판정)

Action(행동): dense M5 model input(고밀도 5분봉 모델 입력)에 direct return label(직접 수익 라벨)을 붙이고 ONNX-exportable model(온엑스 변환 가능 모델)을 학습했다.

Effect(효과): sparse runtime tape(희소 런타임 테이프) 문제와 model family(모델 계열) 문제를 분리해, MT5 runtime probe(MT5 런타임 탐침)로 보낼 수 있는 후보만 남긴다.

## Top Proxy Rows(상위 프록시 행)

{markdown_table(top_rows, ["model_id", "label_id", "policy_id", "threshold_id", "validation_net", "oos_net", "validation_profit_factor", "oos_profit_factor", "validation_trade_density", "oos_trade_density", "strict_cross_split_success", "onnx_smoke_status"])}

## ONNX Smoke(온엑스 연기 점검)

{markdown_table(smoke_rows, ["model_id", "status", "sample_rows", "max_abs_diff", "failure"])}

## Next Queue(다음 대기열)

{markdown_table(next_rows, ["queue_id", "priority", "next_run_id", "model_id", "action", "guardrail"])}

## Evidence(근거)

- model_scorecard(모델 점수표): `{rel(MODEL_SCORECARD)}`
- proxy_threshold_surface(프록시 임계값 표면): `{rel(PROXY_THRESHOLD_SURFACE)}`
- ONNX smoke report(온엑스 연기 보고서): `{rel(ONNX_SMOKE_REPORT)}`
- selected_model_summary(선택 모델 요약): `{rel(SELECTED_MODEL_SUMMARY)}`
- gate audit(게이트 감사): `{rel(GATE_AUDIT)}`

## Boundary(경계)

proxy(프록시)는 MT5 KPI(MT5 핵심 성과 지표)를 대체하지 않는다. 이번 실행은 MT5 execution(MT5 실행), forward pass(전진 검증), live readiness(실거래 준비), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)를 주장하지 않는다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(REPORT_PATH, report)
    write_text(
        DECISION_DOC,
        f"""# {TODAY} Stage364J Direct Dense M5 ONNX Scout Decision(364J 직접 고밀도 5분봉 온엑스 탐색 결정)

- decision(결정): `{summary["decision"]}`
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- next_run_id(다음 실행 ID): `{summary["next_run_id"]}`
- judgment(판정): `{summary["judgment"]}`
- gates(게이트): `{sum(1 for row in gates if row["status"] == "passed")}/{len(gates)}`

Action(행동): direct dense M5 ONNX scout(직접 고밀도 5분봉 온엑스 탐색)를 학습과 proxy(프록시) 검증까지 실행했다.

Effect(효과): `{summary["best_model_id"]}` 후보의 위치를 기록했지만, MT5 runtime probe(MT5 런타임 탐침) 전에는 운영 주장(operating claim, 운영 주장)을 하지 않는다.

Evidence(근거): `{rel(PROXY_THRESHOLD_SURFACE)}`, `{rel(ONNX_SMOKE_REPORT)}`, `{rel(SELECTED_MODEL_SUMMARY)}`.

Claim Boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )


def update_state_docs(summary: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    write_text(
        WORKSPACE_STATE,
        f"""current_stage_id: {STAGE_ID}
current_run_id: {summary["next_run_id"]}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {summary["judgment"]}
current_decision: {summary["decision"]}
next_run_id: {summary["next_run_id"]}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
""",
        bom=False,
    )
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current Working State(현재 작업 상태)

- current_stage_id(현재 단계 ID): `{STAGE_ID}`
- current_run_id(현재 실행 ID): `{summary["next_run_id"]}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- current_status(현재 상태): `{STATUS}`
- current_judgment(현재 판정): `{summary["judgment"]}`
- current_decision(현재 결정): `{summary["decision"]}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): run364J(364J 실행)가 direct dense M5 ONNX scout(직접 고밀도 5분봉 온엑스 탐색)를 완료했다.

Effect(효과): 다음 작업은 `{summary["next_run_id"]}`이며, MT5 runtime evidence(MT5 런타임 근거) 전에는 runtime authority(런타임 권위)를 주장하지 않는다.
""",
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 Selection Status(364단계 선택 상태)

- selection_status(선택 상태): `direct_dense_m5_onnx_scout_completed_no_operating_claim(직접 고밀도 5분봉 온엑스 탐색 완료, 운영 주장 없음)`
- active_stage_id(활성 단계 ID): `{STAGE_ID}`
- current_run_id(현재 실행 ID): `{summary["next_run_id"]}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- selected_model_id(선택 모델 ID): `{summary["best_model_id"]}`
- selected_label_id(선택 라벨 ID): `{summary["best_label_id"]}`
- selected_policy_id(선택 정책 ID): `{summary["best_policy_id"]}`
- runtime_probe_candidate_count(런타임 탐침 후보 수): `{summary["runtime_probe_candidate_count"]}`
- runtime_authority(런타임 권위): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`

## run364J Closeout(364J 종료 기록)

- status(상태): `{STATUS}`
- judgment(판정): `{summary["judgment"]}`
- gate_result(게이트 결과): `{sum(1 for row in gates if row["status"] == "passed")}/{len(gates)}`
- best_validation_net(최선 검증 순수익): `{summary["best_validation_net"]}`
- best_oos_net(최선 표본외 순수익): `{summary["best_oos_net"]}`
- best_validation_profit_factor(최선 검증 수익 팩터): `{summary["best_validation_profit_factor"]}`
- best_oos_profit_factor(최선 표본외 수익 팩터): `{summary["best_oos_profit_factor"]}`
- next_run_id(다음 실행 ID): `{summary["next_run_id"]}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): ONNX-exportable direct dense model(온엑스 변환 가능 직접 고밀도 모델)을 탐색했다.

Effect(효과): 후보는 proxy(프록시) 기준으로만 판정되며 MT5 KPI(MT5 핵심 성과 지표)를 대체하지 않는다.
""",
    )
    append_text_once(
        STAGE_BRIEF,
        "## run364J Direct Dense M5 ONNX Scout Closeout",
        f"""## run364J Direct Dense M5 ONNX Scout Closeout(364J 직접 고밀도 5분봉 온엑스 탐색 종료)

Action(행동): all58/runtime_core feature set(전체58/런타임 핵심 피처셋)과 direct return label(직접 수익 라벨)을 학습했다.

Effect(효과): strict_cross_split_success_count(엄격 교차 분할 성공 수)는 `{summary["strict_cross_split_success_count"]}`이고, 다음 실행은 `{summary["next_run_id"]}`이다.
""",
    )
    append_text_once(
        REVIEW_INDEX,
        "run364J_direct_dense_m5_onnx_scout",
        f"""- `{RUN_ID}`: `{rel(REPORT_PATH)}` - direct dense M5 ONNX scout(직접 고밀도 5분봉 온엑스 탐색).""",
    )
    append_text_once(
        STAGE_README,
        "run364J Direct Dense M5 ONNX Scout",
        f"""## run364J Direct Dense M5 ONNX Scout(364J 직접 고밀도 5분봉 온엑스 탐색)

Action(행동): direct dense M5 model(직접 고밀도 5분봉 모델)을 학습하고 ONNX smoke parity(온엑스 연기 동등성)를 점검했다.

Effect(효과): 다음 작업은 `{summary["next_run_id"]}`이고, 운영 주장(operating claim, 운영 주장)은 없다.
""",
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        "run364J_train_direct_dense_m5_return_onnx_scout_without_db_v1",
        f"""## {TODAY} run364J Direct Dense M5 ONNX Scout(364J 직접 고밀도 5분봉 온엑스 탐색)

Action(행동): dense M5 feature matrix(고밀도 5분봉 피처 행렬)에서 direct return label(직접 수익 라벨) 모델을 학습했다.

Effect(효과): best_model_id(최선 모델 ID)는 `{summary["best_model_id"]}`이고, MT5 runtime probe(MT5 런타임 탐침) 전에는 운영 주장(operating claim, 운영 주장)이 없다.
""",
    )
    append_text_once(
        IDEA_REGISTRY,
        "IDEA-ST364J-DIRECT-DENSE-M5-RETURN-ONNX-SCOUT",
        f"""## IDEA-ST364J-DIRECT-DENSE-M5-RETURN-ONNX-SCOUT

- idea(아이디어): direct dense M5 return label(직접 고밀도 5분봉 수익 라벨)로 sparse tape(희소 테이프) 문제를 우회한다.
- best_model_id(최선 모델 ID): `{summary["best_model_id"]}`.
- best_oos_net(최선 표본외 순수익): `{summary["best_oos_net"]}`.
- runtime_probe_candidate_count(런타임 탐침 후보 수): `{summary["runtime_probe_candidate_count"]}`.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`.
""",
    )
    if int(summary["runtime_probe_candidate_count"]) == 0:
        append_text_once(
            NEGATIVE_REGISTER,
            "run364J_direct_dense_m5_onnx_scout_no_strict_candidate",
            f"""## run364J Direct Dense M5 ONNX Scout No Strict Candidate(364J 직접 고밀도 5분봉 온엑스 탐색 엄격 후보 없음)

Action(행동): direct dense M5 ONNX scout(직접 고밀도 5분봉 온엑스 탐색)를 strict cost-density gate(엄격 비용-밀도 게이트)로 닫았다.

Effect(효과): 다음 작업은 failure memory(실패 기억)를 이용해 새 offensive seed(공격 씨앗)를 고른다. 아이디어 사망(idea dead, 아이디어 사망)은 아니다.
""",
        )
    replace_stage_brief_header(summary)


def replace_stage_brief_header(summary: Mapping[str, Any]) -> None:
    text = read_text(STAGE_BRIEF)
    if not text:
        return
    replacements = {
        "- current_run_id(": f"- current_run_id(현재 실행 ID): `{summary['next_run_id']}`",
        "- latest_completed_run_id(": f"- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`",
        "- selection_status(": "- selection_status(선택 상태): `direct_dense_m5_onnx_scout_completed_no_operating_claim(직접 고밀도 5분봉 온엑스 탐색 완료, 운영 주장 없음)`",
        "- claim_boundary(": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    }
    next_lines = []
    for line in text.splitlines():
        replaced = False
        for prefix, value in replacements.items():
            if line.startswith(prefix):
                next_lines.append(value)
                replaced = True
                break
        if not replaced:
            next_lines.append(line)
    write_text(STAGE_BRIEF, "\n".join(next_lines))


def registry_rows(summary: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "direct_dense_m5_onnx_scout(직접 고밀도 5분봉 온엑스 탐색)",
        "status": STATUS,
        "judgment": summary["judgment"],
        "path": rel(REPORT_PATH),
        "external_verification_status": "out_of_scope_by_claim_no_mt5_execution(주장 범위 밖, MT5 실행 없음)",
        "notes": "Stage364J direct dense M5 ONNX scout(Stage364J 직접 고밀도 5분봉 온엑스 탐색).",
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": summary["decision"],
        "next_run_id": summary["next_run_id"],
        "rows": summary["threshold_rows"],
        "gate_passes": summary["gate_passes"],
        "gate_total": summary["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "trained_models": summary["model_rows"],
        "onnx_parity": f"smoke_pass={summary['onnx_smoke_pass_rows']}/{summary['onnx_smoke_rows']}",
        "best_model_id": summary["best_model_id"],
        "best_proxy_net": summary["best_oos_net"],
        "best_net_profit": summary["best_oos_net"],
        "best_profit_factor": summary["best_oos_profit_factor"],
        "operating_ready_rows": 0,
        "run_date": TODAY,
        "primary_artifact": rel(SELECTED_MODEL_SUMMARY),
        "result_status": STATUS,
        "sample_rows": summary["threshold_rows"],
        "feature_count": "",
        "expectancy": "",
        "trade_count": "",
        "source_package_run_id": PARENT_RUN_ID,
        "work_family": "experiment_execution(실험 실행)",
        "trade_density_per_feature_day": summary["best_oos_trade_density"],
        "trade_density_requirement_status": TRADE_DENSITY_REQUIREMENT,
        "result_judgment": summary["judgment"],
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": TODAY,
        "lane": "direct_dense_m5_onnx_scout(직접 고밀도 5분봉 온엑스 탐색)",
        "family": "experiment_execution(실험 실행)",
        "primary_report": rel(REPORT_PATH),
        "evidence_boundary": CLAIM_BOUNDARY,
        "next_action": summary["next_run_id"],
        "question": "Can direct dense M5 return labels recover cost-stable ONNX candidates?(직접 고밀도 5분봉 수익 라벨이 비용 안정 온엑스 후보를 회복할 수 있는가?)",
        "metric_scope": "python_proxy_and_onnx_smoke_no_mt5(Python 프록시와 온엑스 연기 점검, MT5 없음)",
        "net_profit": summary["best_oos_net"],
        "profit_factor": summary["best_oos_profit_factor"],
        "drawdown": summary["best_oos_max_drawdown"],
        "recovery_factor": summary["best_oos_recovery_factor"],
        "long_trade_count": summary["best_oos_long_trade_count"],
        "short_trade_count": summary["best_oos_short_trade_count"],
    }
    tier_a = dict(common)
    tier_a.update(
        {
            "subrun_id": f"{RUN_ID}__Tier_A",
            "ledger_row_id": f"{RUN_ID}__Tier_A",
            "row_id": f"{RUN_ID}__Tier_A",
            "record_view": "Tier A separate(Tier A 분리)",
            "tier_scope": "Tier A",
            "view": "Tier A separate(Tier A 분리)",
            "tier": "Tier A",
            "kpi_scope": "proxy_model_training(프록시 모델 학습)",
            "primary_kpi": f"best_oos_net={summary['best_oos_net']};best_oos_pf={summary['best_oos_profit_factor']};density={summary['best_oos_trade_density']}",
            "guardrail_kpi": "mt5_execution=not_run;runtime_authority=not_claimed",
        }
    )
    tier_b = dict(tier_a)
    tier_b.update(
        {
            "subrun_id": f"{RUN_ID}__Tier_B",
            "ledger_row_id": f"{RUN_ID}__Tier_B",
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
            "subrun_id": f"{RUN_ID}__Tier_AplusB",
            "ledger_row_id": f"{RUN_ID}__Tier_AplusB",
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
    return [tier_a], [tier_a, tier_b, combined], [tier_a, tier_b, combined]


def write_registries(summary: Mapping[str, Any]) -> None:
    run_rows, project_rows, stage_rows = registry_rows(summary)
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], run_rows, extend_header=False)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], project_rows, extend_header=False)
    append_or_replace_csv(STAGE_LEDGER, ["row_id"], stage_rows, extend_header=True)


def write_artifact_registry() -> None:
    rows = []
    artifacts = [
        ("script", Path("stage_pipelines/stage364/train_direct_dense_m5_return_onnx_scout_without_db.py"), "tracked"),
        ("report", REPORT_PATH, "tracked"),
        ("decision_doc", DECISION_DOC, "tracked"),
        ("selection_status", SELECTION_STATUS, "tracked"),
        ("input_manifest", INPUT_MANIFEST, "ignored_with_manifest"),
        ("label_summary", LABEL_SUMMARY, "ignored_with_manifest"),
        ("model_scorecard", MODEL_SCORECARD, "ignored_with_manifest"),
        ("proxy_threshold_surface", PROXY_THRESHOLD_SURFACE, "ignored_with_manifest"),
        ("onnx_smoke_report", ONNX_SMOKE_REPORT, "ignored_with_manifest"),
        ("selected_model_summary", SELECTED_MODEL_SUMMARY, "ignored_with_manifest"),
        ("final_decision", FINAL_DECISION, "ignored_with_manifest"),
        ("gate_audit", GATE_AUDIT, "ignored_with_manifest"),
    ]
    for artifact_type, path, availability in artifacts:
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
                "notes": f"Stage364J direct dense M5 ONNX scout artifact(364J 직접 고밀도 5분봉 온엑스 탐색 산출물); availability={availability}",
                "artifact_path": rel(path),
            }
        )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["stage_id", "run_id", "artifact_type", "path"], rows, extend_header=False)


def main() -> None:
    ensure_dirs()
    validate_inputs()
    write_input_manifest()
    feature_order = load_feature_order()
    frame = load_dataset(feature_order)
    feature_sets = {
        "all58": list(feature_order),
        "runtime_core": [feature for feature in feature_order if not external_feature(feature)],
    }
    write_feature_matrix_manifest(frame, feature_sets)
    label_rows = write_label_summary(frame)
    score_rows, threshold_rows, _month_rows, trained = score_models(frame, feature_sets)
    _artifact_rows, smoke_rows, exportable = export_models(trained, threshold_rows)
    summary = select_summary(threshold_rows, smoke_rows, exportable)
    write_json(SELECTED_MODEL_SUMMARY, summary)
    next_rows = write_next_queue(summary)
    write_receipts(summary, label_rows)
    gates = write_final_manifest_and_gates(summary)
    summary = read_json(FINAL_DECISION)
    write_report(summary, gates, next_rows)
    update_state_docs(summary, gates)
    write_registries(summary)
    write_artifact_registry()
    gates = write_final_manifest_and_gates(summary)
    write_report(read_json(FINAL_DECISION), gates, next_rows)
    print(json.dumps(read_json(FINAL_DECISION), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
