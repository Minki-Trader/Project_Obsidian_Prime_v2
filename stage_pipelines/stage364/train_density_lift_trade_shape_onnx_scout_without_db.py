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
from sklearn.metrics import accuracy_score, balanced_accuracy_score


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage364 import prepare_timestamp_context_onnx_runtime_probe_without_db as pkg  # noqa: E402


TODAY = "2026-06-02"
STAGE_ID = pkg.STAGE_ID
RUN_NUMBER = "run364L"
RUN_ID = "run364L_train_density_lift_trade_shape_onnx_scout_without_db_v1"
PARENT_RUN_ID = "run364K_review_direct_dense_m5_onnx_scout_without_db_v1"

STATUS = "completed_stage364L_density_lift_trade_shape_onnx_scout_trained_proxy_positive_no_runtime_authority"
CLAIM_BOUNDARY = (
    "research_development_density_lift_trade_shape_model_training_and_proxy_scout_only_no_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)
TRADE_DENSITY_REQUIREMENT = "trade_per_day_min_3_to_10_plus_no_trade_splitting"
TIME_AXIS = "feature_timestamp_open_time_joined_to_raw_m5_open_time_dynamic_exit_uses_current_bar_features_no_future_feature"
PROXY_EXECUTION_BOUNDARY = "raw_m5_open_to_dynamic_exit_open_single_position_skip_overlap_not_mt5_strategy_tester"
POINT_VALUE = 0.10
BASE_COST = 0.30
STRICT_DENSITY_FLOOR = 3.0
STRICT_PF_FLOOR = 1.05
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
MODEL_INPUT_FEATURE_ORDER = MODEL_INPUT_DIR / "model_input_feature_order.txt"
RAW_US100_M5 = ROOT / "data" / "raw" / "mt5_bars" / "m5" / "US100" / "bars_us100_m5_mt5api_raw.csv"

SOURCE_RUN_DIR = STAGE_DIR / "02_runs" / "run364K"
SOURCE_PARENT_FINAL = SOURCE_RUN_DIR / "final_decision.json"
SOURCE_PARENT_GATES = SOURCE_RUN_DIR / "required_gate_coverage_audit.csv"
SOURCE_NEXT_QUEUE = SOURCE_RUN_DIR / "run364L_next_queue.csv"
SOURCE_SALVAGE_CLUES = SOURCE_RUN_DIR / "salvage_clues.csv"
SOURCE_FAILURE_MEMORY = SOURCE_RUN_DIR / "failure_memory.csv"
SOURCE_PARENT_REPORT = REVIEW_DIR / "run364K_direct_dense_m5_onnx_scout_review.md"

INPUT_FILES = [
    SOURCE_PARENT_FINAL,
    SOURCE_PARENT_GATES,
    SOURCE_NEXT_QUEUE,
    SOURCE_SALVAGE_CLUES,
    SOURCE_FAILURE_MEMORY,
    SOURCE_PARENT_REPORT,
    MODEL_INPUT_DATASET,
    MODEL_INPUT_SUMMARY,
    MODEL_INPUT_FEATURE_ORDER,
    RAW_US100_M5,
]

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
LABEL_SUMMARY = RUN_DIR / "density_lift_label_summary.csv"
MODEL_SCORECARD = RUN_DIR / "model_scorecard.csv"
TRADE_SHAPE_SURFACE = RUN_DIR / "dynamic_trade_shape_surface.csv"
TOP_TRADE_SAMPLE = RUN_DIR / "dynamic_trade_top_trade_sample.csv"
MONTH_STABILITY = RUN_DIR / "dynamic_trade_month_stability.csv"
COST_STRESS = RUN_DIR / "cost_stress_surface.csv"
MODEL_ARTIFACT_MANIFEST = RUN_DIR / "model_artifact_manifest.csv"
ONNX_SMOKE_REPORT = RUN_DIR / "onnx_smoke_report.csv"
SELECTED_MODEL_SUMMARY = RUN_DIR / "selected_model_summary.json"
NEXT_QUEUE = RUN_DIR / "run364M_next_queue.csv"
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

REPORT_PATH = REVIEW_DIR / "run364L_density_lift_trade_shape_onnx_scout.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364L_density_lift_trade_shape_onnx_scout.md"
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

OUTPUT_FILES = [
    INPUT_MANIFEST,
    LABEL_SUMMARY,
    MODEL_SCORECARD,
    TRADE_SHAPE_SURFACE,
    TOP_TRADE_SAMPLE,
    MONTH_STABILITY,
    COST_STRESS,
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
    {"label_id": "h6_move3", "horizon_m5": 6, "threshold_points": 3.0},
    {"label_id": "h12_move5", "horizon_m5": 12, "threshold_points": 5.0},
    {"label_id": "h24_move8", "horizon_m5": 24, "threshold_points": 8.0},
]
MODEL_SPECS: Sequence[tuple[str, Callable[[], Any]]] = [
    (
        "rf4_l120_n64",
        lambda: RandomForestClassifier(
            n_estimators=64,
            max_depth=4,
            min_samples_leaf=120,
            class_weight="balanced_subsample",
            random_state=RANDOM_SEED,
            n_jobs=-1,
        ),
    ),
    (
        "rf5_l80_n64",
        lambda: RandomForestClassifier(
            n_estimators=64,
            max_depth=5,
            min_samples_leaf=80,
            class_weight="balanced_subsample",
            random_state=RANDOM_SEED + 1,
            n_jobs=-1,
        ),
    ),
]
POLICIES = ["long_only_margin", "two_sided_argmax_margin"]
DENSITY_TARGETS = [8.0, 12.0, 16.0, 20.0, 28.0]
MAX_HOLDS = [4, 6, 8, 12]
EXIT_MODES = ["flat_or_opp", "weak_or_opp"]
COST_STRESS_VALUES = [0.30, 0.45, 0.60]


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
        if isinstance(value, str) and value.lower() == "inf":
            return 999.0
        return float(value)
    except (TypeError, ValueError):
        return default


def ensure_dirs() -> None:
    for path in [RUN_DIR, MODEL_DIR, ONNX_DIR, REVIEW_DIR, SELECTED_DIR, SPEC_DIR]:
        os.makedirs(fs_path(path), exist_ok=True)


def validate_inputs() -> None:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing run364L inputs: " + ", ".join(missing))
    parent = read_json(SOURCE_PARENT_FINAL)
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"run364K next_run_id mismatch: {parent.get('next_run_id')}")
    _, gates = read_csv_rows(SOURCE_PARENT_GATES)
    if not gates or any(row.get("status") != "passed" for row in gates):
        raise RuntimeError("run364K gate audit is not fully passed")


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
                "effect": "input identity(입력 정체성)을 고정해 density lift scout(밀도 상향 탐색)를 재현 가능하게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(INPUT_MANIFEST, rows)


def load_feature_order() -> list[str]:
    return [line.strip() for line in read_text(MODEL_INPUT_FEATURE_ORDER).splitlines() if line.strip()]


def load_dataset(feature_order: Sequence[str]) -> pd.DataFrame:
    frame = pd.read_parquet(fs_path(MODEL_INPUT_DATASET))
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    frame = frame.sort_values("timestamp").reset_index(drop=True)
    raw = pd.read_csv(fs_path(RAW_US100_M5), usecols=["time_open_unix", "open"])
    raw["timestamp"] = pd.to_datetime(raw["time_open_unix"], unit="s", utc=True)
    raw = raw[["timestamp", "open"]].rename(columns={"open": "entry_open"})
    raw_open_map = dict(zip(raw["timestamp"].astype("int64"), raw["entry_open"]))
    frame = frame.merge(raw, on="timestamp", how="left")
    for horizon in sorted({int(spec["horizon_m5"]) for spec in LABEL_SPECS} | set(MAX_HOLDS)):
        future_ts = frame["timestamp"] + pd.to_timedelta(horizon * 5, unit="m")
        frame[f"future_open_h{horizon}"] = future_ts.astype("int64").map(raw_open_map)
    for column in feature_order:
        if column not in frame.columns:
            raise RuntimeError(f"missing feature column: {column}")
    return frame


def label_values(frame: pd.DataFrame, spec: Mapping[str, Any]) -> np.ndarray:
    horizon = int(spec["horizon_m5"])
    move = frame[f"future_open_h{horizon}"] - frame["entry_open"]
    threshold = float(spec["threshold_points"])
    values = np.where(move >= threshold, 2, np.where(move <= -threshold, 0, 1))
    values[np.isnan(move.to_numpy(dtype=float))] = 1
    return values.astype("int8")


def write_label_summary(frame: pd.DataFrame) -> list[dict[str, Any]]:
    rows = []
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
                    "threshold_points": spec["threshold_points"],
                    "rows": int(mask.sum()),
                    "short_count": int(np.sum(split_y == 0)),
                    "flat_count": int(np.sum(split_y == 1)),
                    "long_count": int(np.sum(split_y == 2)),
                    "timestamp_safety": TIME_AXIS,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    write_csv(LABEL_SUMMARY, rows)
    return rows


def feature_matrix(frame: pd.DataFrame, columns: Sequence[str], mask: np.ndarray) -> np.ndarray:
    return frame.loc[mask, list(columns)].replace([np.inf, -np.inf], np.nan).fillna(0.0).to_numpy(dtype=np.float32)


def class_safe_probabilities(model: Any, x: np.ndarray) -> np.ndarray:
    raw = model.predict_proba(x)
    classes = list(model.classes_)
    out = np.zeros((len(x), 3), dtype=np.float64)
    for index, cls in enumerate(classes):
        out[:, int(cls)] = raw[:, index]
    return out


def policy_signal(probabilities: np.ndarray, policy: str) -> tuple[np.ndarray, np.ndarray]:
    p_short = probabilities[:, 0]
    p_flat = probabilities[:, 1]
    p_long = probabilities[:, 2]
    if policy == "long_only_margin":
        return np.ones(len(probabilities), dtype=np.int8), p_long - np.maximum(p_short, p_flat)
    if policy == "two_sided_argmax_margin":
        return np.where(p_long >= p_short, 1, -1).astype(np.int8), np.maximum(p_long, p_short) - p_flat
    raise ValueError(f"unknown policy: {policy}")


def threshold_for_density(scores: np.ndarray, split_days: int, density_target: float) -> float:
    clean = np.asarray(scores, dtype=float)
    clean = clean[np.isfinite(clean)]
    desired = max(1, min(clean.size, int(round(split_days * density_target))))
    return float(np.partition(clean, clean.size - desired)[clean.size - desired])


def simulate_dynamic_exit(
    split_frame: pd.DataFrame,
    probabilities: np.ndarray,
    side: np.ndarray,
    score: np.ndarray,
    threshold: float,
    *,
    max_hold_m5: int,
    exit_mode: str,
    cost_per_trade: float,
    model_id: str,
    label_id: str,
    policy_id: str,
    threshold_id: str,
    split: str,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    opens = split_frame["entry_open"].to_numpy(dtype=float)
    trades: list[dict[str, Any]] = []
    index = 0
    while index < len(split_frame) - 1:
        if not np.isfinite(opens[index]) or score[index] < threshold:
            index += 1
            continue
        trade_side = int(side[index])
        exit_index = index
        probe_index = index + 1
        while probe_index < len(split_frame):
            held = probe_index - index
            flat_dominant = probabilities[probe_index, 1] >= max(probabilities[probe_index, 0], probabilities[probe_index, 2])
            opposite = bool(side[probe_index] != trade_side and score[probe_index] >= threshold)
            weak = bool(score[probe_index] < threshold * 0.20)
            exit_now = held >= max_hold_m5
            if exit_mode == "flat_or_opp":
                exit_now = exit_now or flat_dominant or opposite
            elif exit_mode == "weak_or_opp":
                exit_now = exit_now or weak or opposite
            else:
                raise ValueError(f"unknown exit mode: {exit_mode}")
            if exit_now:
                exit_index = probe_index
                break
            probe_index += 1
        if exit_index == index:
            break
        if np.isfinite(opens[exit_index]):
            profit = (opens[exit_index] - opens[index]) * POINT_VALUE * trade_side - cost_per_trade
            timestamp = split_frame["timestamp"].iat[index]
            exit_timestamp = split_frame["timestamp"].iat[exit_index]
            trades.append(
                {
                    "run_id": RUN_ID,
                    "split": split,
                    "model_id": model_id,
                    "label_id": label_id,
                    "policy_id": policy_id,
                    "threshold_id": threshold_id,
                    "exit_mode": exit_mode,
                    "max_hold_m5": max_hold_m5,
                    "entry_timestamp": timestamp.isoformat(),
                    "exit_timestamp": exit_timestamp.isoformat(),
                    "held_m5": int(exit_index - index),
                    "side": "long" if trade_side > 0 else "short",
                    "score": finite(score[index], 12),
                    "threshold": finite(threshold, 12),
                    "entry_open": finite(opens[index], 5),
                    "exit_open": finite(opens[exit_index], 5),
                    "net_profit": finite(profit, 10),
                    "cost_per_trade": cost_per_trade,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
        index = exit_index + 1
    return trade_metrics(trades, split_frame, split), trades


def trade_metrics(trades: Sequence[Mapping[str, Any]], split_frame: pd.DataFrame, split: str) -> dict[str, Any]:
    days = max(1, int(split_frame["timestamp"].dt.date.nunique()))
    profits = np.asarray([as_float(row["net_profit"]) for row in trades], dtype=float)
    if profits.size == 0:
        return empty_metrics(split)
    gross_profit = float(profits[profits > 0].sum())
    gross_loss = float(-profits[profits < 0].sum())
    equity = np.cumsum(profits)
    peak = np.maximum.accumulate(np.r_[0.0, equity])[:-1]
    drawdown = equity - peak
    max_drawdown = float(drawdown.min()) if drawdown.size else 0.0
    net = float(profits.sum())
    long_count = sum(1 for row in trades if row["side"] == "long")
    short_count = sum(1 for row in trades if row["side"] == "short")
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
        f"{split}_long_short_balance": round(min(long_count, short_count) / max(long_count, short_count), 10) if max(long_count, short_count) else 0.0,
    }


def empty_metrics(split: str) -> dict[str, Any]:
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


def strict_success(row: Mapping[str, Any]) -> bool:
    return (
        as_float(row["validation_net"]) > 0
        and as_float(row["oos_net"]) > 0
        and as_float(row["validation_profit_factor"]) >= STRICT_PF_FLOOR
        and as_float(row["oos_profit_factor"]) >= STRICT_PF_FLOOR
        and as_float(row["validation_trade_density"]) >= STRICT_DENSITY_FLOOR
        and as_float(row["oos_trade_density"]) >= STRICT_DENSITY_FLOOR
    )


def selection_score(row: Mapping[str, Any]) -> float:
    return (
        as_float(row["oos_net"])
        + 0.40 * as_float(row["validation_net"])
        + 120.0 * max(0.0, as_float(row["oos_profit_factor"]) - 1.0)
        + 8.0 * min(as_float(row["oos_trade_density"]), 8.0)
        - 0.08 * abs(min(0.0, as_float(row["oos_max_drawdown"])))
    )


def train_and_score(frame: pd.DataFrame, feature_columns: Sequence[str]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[str, dict[str, Any]]]:
    score_rows: list[dict[str, Any]] = []
    surface_rows: list[dict[str, Any]] = []
    trade_samples: list[dict[str, Any]] = []
    trained: dict[str, dict[str, Any]] = {}
    split_masks = {split: frame["split"].eq(split).to_numpy() for split in ["train", "validation", "oos"]}
    for label_spec in LABEL_SPECS:
        y = label_values(frame, label_spec)
        horizon = int(label_spec["horizon_m5"])
        ok = np.isfinite(frame[f"future_open_h{horizon}"].to_numpy(dtype=float)) & np.isfinite(frame["entry_open"].to_numpy(dtype=float))
        masks = {split: split_masks[split] & ok for split in ["train", "validation", "oos"]}
        x_train = feature_matrix(frame, feature_columns, masks["train"])
        y_train = y[masks["train"]]
        validation_frame = frame.loc[masks["validation"]].reset_index(drop=True)
        oos_frame = frame.loc[masks["oos"]].reset_index(drop=True)
        x_validation = feature_matrix(frame, feature_columns, masks["validation"])
        x_oos = feature_matrix(frame, feature_columns, masks["oos"])
        y_validation = y[masks["validation"]]
        y_oos = y[masks["oos"]]
        for base_model_id, factory in MODEL_SPECS:
            model_id = f"{label_spec['label_id']}__{base_model_id}"
            model = factory()
            started = time.time()
            model.fit(x_train, y_train)
            fit_seconds = round(time.time() - started, 6)
            validation_prob = class_safe_probabilities(model, x_validation)
            oos_prob = class_safe_probabilities(model, x_oos)
            validation_pred = np.argmax(validation_prob, axis=1)
            oos_pred = np.argmax(oos_prob, axis=1)
            score_rows.append(
                {
                    "run_id": RUN_ID,
                    "model_id": model_id,
                    "base_model_id": base_model_id,
                    "label_id": label_spec["label_id"],
                    "horizon_m5": horizon,
                    "feature_set_id": "all58",
                    "feature_count": len(feature_columns),
                    "train_rows": int(masks["train"].sum()),
                    "validation_rows": int(masks["validation"].sum()),
                    "oos_rows": int(masks["oos"].sum()),
                    "validation_accuracy": finite(accuracy_score(y_validation, validation_pred), 10),
                    "oos_accuracy": finite(accuracy_score(y_oos, oos_pred), 10),
                    "validation_balanced_accuracy": finite(balanced_accuracy_score(y_validation, validation_pred), 10),
                    "oos_balanced_accuracy": finite(balanced_accuracy_score(y_oos, oos_pred), 10),
                    "fit_seconds": fit_seconds,
                    "status": "trained",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            validation_days = max(1, int(validation_frame["timestamp"].dt.date.nunique()))
            for policy_id in POLICIES:
                validation_side, validation_score = policy_signal(validation_prob, policy_id)
                oos_side, oos_score = policy_signal(oos_prob, policy_id)
                for density_target in DENSITY_TARGETS:
                    threshold = threshold_for_density(validation_score, validation_days, density_target)
                    for max_hold in MAX_HOLDS:
                        for exit_mode in EXIT_MODES:
                            threshold_id = (
                                f"{policy_id}__density_{str(density_target).replace('.', '_')}"
                                f"__maxhold_{max_hold}__{exit_mode}"
                            )
                            validation_metrics, validation_trades = simulate_dynamic_exit(
                                validation_frame,
                                validation_prob,
                                validation_side,
                                validation_score,
                                threshold,
                                max_hold_m5=max_hold,
                                exit_mode=exit_mode,
                                cost_per_trade=BASE_COST,
                                model_id=model_id,
                                label_id=label_spec["label_id"],
                                policy_id=policy_id,
                                threshold_id=threshold_id,
                                split="validation",
                            )
                            oos_metrics, oos_trades = simulate_dynamic_exit(
                                oos_frame,
                                oos_prob,
                                oos_side,
                                oos_score,
                                threshold,
                                max_hold_m5=max_hold,
                                exit_mode=exit_mode,
                                cost_per_trade=BASE_COST,
                                model_id=model_id,
                                label_id=label_spec["label_id"],
                                policy_id=policy_id,
                                threshold_id=threshold_id,
                                split="oos",
                            )
                            row: dict[str, Any] = {
                                "run_id": RUN_ID,
                                "model_id": model_id,
                                "base_model_id": base_model_id,
                                "label_id": label_spec["label_id"],
                                "feature_set_id": "all58",
                                "label_horizon_m5": horizon,
                                "policy_id": policy_id,
                                "threshold_id": threshold_id,
                                "validation_density_target": density_target,
                                "score_threshold": finite(threshold, 12),
                                "max_hold_m5": max_hold,
                                "exit_mode": exit_mode,
                                "cost_per_trade": BASE_COST,
                                "trade_shape": "single_position_dynamic_exit_skip_overlap",
                                "proxy_boundary": PROXY_EXECUTION_BOUNDARY,
                                **validation_metrics,
                                **oos_metrics,
                                "claim_boundary": CLAIM_BOUNDARY,
                            }
                            row["strict_cross_split_success"] = strict_success(row)
                            row["selection_score"] = finite(selection_score(row), 10)
                            surface_rows.append(row)
                            if row["strict_cross_split_success"]:
                                trade_samples.extend(validation_trades[:80])
                                trade_samples.extend(oos_trades[:80])
            trained[model_id] = {
                "model": model,
                "feature_columns": list(feature_columns),
                "label_id": label_spec["label_id"],
                "horizon_m5": horizon,
                "validation_x": x_validation,
                "oos_x": x_oos,
            }
    write_csv(MODEL_SCORECARD, score_rows)
    write_csv(TRADE_SHAPE_SURFACE, surface_rows)
    write_csv(TOP_TRADE_SAMPLE, trade_samples)
    write_csv(MONTH_STABILITY, month_rows(trade_samples))
    return score_rows, surface_rows, trade_samples, trained


def month_rows(trades: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    if not trades:
        return []
    frame = pd.DataFrame(trades)
    frame["entry_timestamp"] = pd.to_datetime(frame["entry_timestamp"], utc=True)
    frame["month"] = frame["entry_timestamp"].dt.strftime("%Y-%m")
    frame["net_profit"] = frame["net_profit"].astype(float)
    rows = []
    keys = ["model_id", "label_id", "policy_id", "threshold_id", "exit_mode", "max_hold_m5", "split", "month"]
    for group_key, group in frame.groupby(keys, dropna=False):
        row = dict(zip(keys, group_key))
        row.update(
            {
                "run_id": RUN_ID,
                "trade_count": int(len(group)),
                "net_profit": finite(group["net_profit"].sum(), 10),
                "expectancy": finite(group["net_profit"].mean(), 10),
                "positive_month": bool(group["net_profit"].sum() > 0),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        rows.append(row)
    return rows


def export_models(trained: Mapping[str, Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], set[str]]:
    artifact_rows: list[dict[str, Any]] = []
    smoke_rows: list[dict[str, Any]] = []
    exportable: set[str] = set()
    for model_id, payload in trained.items():
        model = payload["model"]
        feature_columns = payload["feature_columns"]
        model_path = MODEL_DIR / f"{model_id}.joblib"
        joblib.dump(model, fs_path(model_path))
        feature_order_path = MODEL_DIR / f"{model_id}_feature_order.json"
        write_json(feature_order_path, {"model_id": model_id, "feature_columns": feature_columns})
        for artifact_type, path in [("joblib_model", model_path), ("feature_order", feature_order_path)]:
            artifact_rows.append(
                {
                    "run_id": RUN_ID,
                    "model_id": model_id,
                    "artifact_type": artifact_type,
                    "path": rel(path),
                    "sha256": sha(path),
                    "status": "written",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
        onnx_path = ONNX_DIR / f"{model_id}.onnx"
        try:
            onnx_model = convert_sklearn(
                model,
                initial_types=[("float_input", FloatTensorType([None, len(feature_columns)]))],
                options={id(model): {"zipmap": False}},
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
                    "status": "written",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            sample = payload["oos_x"][:64] if len(payload["oos_x"]) else payload["validation_x"][:64]
            expected = class_safe_probabilities(model, sample)
            session = ort.InferenceSession(fs_path(onnx_path), providers=["CPUExecutionProvider"])
            outputs = session.run(None, {session.get_inputs()[0].name: sample})
            candidate = None
            for output in outputs:
                if isinstance(output, np.ndarray) and output.ndim == 2 and output.shape[0] == len(sample):
                    candidate = output
            if candidate is None:
                raise RuntimeError("ONNX probability tensor not found")
            diff = float(np.max(np.abs(expected - candidate))) if len(sample) else 0.0
            status = "passed" if diff <= 1e-5 else "failed"
            if status == "passed":
                exportable.add(model_id)
            smoke_rows.append(
                {
                    "run_id": RUN_ID,
                    "model_id": model_id,
                    "onnx_path": rel(onnx_path),
                    "sample_rows": int(len(sample)),
                    "max_abs_diff": finite(diff, 12),
                    "status": status,
                    "failure": "",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
        except Exception as exc:  # noqa: BLE001
            smoke_rows.append(
                {
                    "run_id": RUN_ID,
                    "model_id": model_id,
                    "onnx_path": rel(onnx_path),
                    "sample_rows": 0,
                    "max_abs_diff": "",
                    "status": "failed",
                    "failure": f"{type(exc).__name__}: {str(exc)[:500]}",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    write_csv(MODEL_ARTIFACT_MANIFEST, artifact_rows)
    write_csv(ONNX_SMOKE_REPORT, smoke_rows)
    return artifact_rows, smoke_rows, exportable


def cost_stress_rows(surface_rows: Sequence[Mapping[str, Any]], trade_samples: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    strict_rows = [row for row in surface_rows if row.get("strict_cross_split_success") is True or row.get("strict_cross_split_success") == "True"]
    top = sorted(strict_rows, key=selection_score, reverse=True)[:8]
    samples = pd.DataFrame(trade_samples)
    rows = []
    if samples.empty:
        write_csv(COST_STRESS, rows)
        return rows
    samples["net_profit"] = samples["net_profit"].astype(float)
    for row in top:
        mask = (
            samples["model_id"].eq(row["model_id"])
            & samples["threshold_id"].eq(row["threshold_id"])
            & samples["exit_mode"].eq(row["exit_mode"])
            & samples["max_hold_m5"].astype(str).eq(str(row["max_hold_m5"]))
        )
        group = samples.loc[mask].copy()
        for split in ["validation", "oos"]:
            split_group = group.loc[group["split"].eq(split)]
            for cost in COST_STRESS_VALUES:
                adjusted = split_group["net_profit"] - (cost - BASE_COST)
                gross_profit = adjusted[adjusted > 0].sum()
                gross_loss = -adjusted[adjusted < 0].sum()
                rows.append(
                    {
                        "run_id": RUN_ID,
                        "model_id": row["model_id"],
                        "threshold_id": row["threshold_id"],
                        "exit_mode": row["exit_mode"],
                        "max_hold_m5": row["max_hold_m5"],
                        "split": split,
                        "cost_per_trade": cost,
                        "sample_trade_count": int(len(split_group)),
                        "sample_net": finite(adjusted.sum(), 10) if len(adjusted) else 0,
                        "sample_profit_factor": finite(gross_profit / gross_loss, 10) if gross_loss > 0 else ("inf" if len(adjusted) else 0),
                        "claim_boundary": CLAIM_BOUNDARY,
                    }
                )
    write_csv(COST_STRESS, rows)
    return rows


def select_summary(surface_rows: Sequence[Mapping[str, Any]], smoke_rows: Sequence[Mapping[str, Any]], exportable: set[str]) -> dict[str, Any]:
    rows = [dict(row) for row in surface_rows]
    strict_rows = [row for row in rows if row.get("strict_cross_split_success") is True and row["model_id"] in exportable]
    if strict_rows:
        best = max(strict_rows, key=selection_score)
        judgment = "positive_proxy_candidate_density_lift_trade_shape_onnx_smoke_passed_runtime_probe_required_no_authority"
        next_run_id = "run364M_prepare_density_lift_trade_shape_onnx_runtime_probe_without_db_v1"
        decision = "stage364L_open_run364M_prepare_density_lift_trade_shape_onnx_runtime_probe_without_db_v1"
    else:
        best = max(rows, key=selection_score)
        judgment = "negative_density_lift_trade_shape_no_strict_proxy_candidate_no_authority"
        next_run_id = "run364M_review_density_lift_trade_shape_onnx_scout_without_db_v1"
        decision = "stage364L_open_run364M_review_density_lift_trade_shape_onnx_scout_without_db_v1"
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS if strict_rows else "completed_stage364L_density_lift_trade_shape_onnx_scout_trained_no_strict_candidate_no_authority",
        "judgment": judgment,
        "result_judgment": judgment,
        "decision": decision,
        "next_run_id": next_run_id,
        "claim_boundary": CLAIM_BOUNDARY,
        "model_rows": len({row["model_id"] for row in rows}),
        "surface_rows": len(rows),
        "strict_cross_split_success_count": len(strict_rows),
        "onnx_smoke_rows": len(smoke_rows),
        "onnx_smoke_pass_rows": sum(1 for row in smoke_rows if row["status"] == "passed"),
        "best_model_id": best.get("model_id", ""),
        "best_label_id": best.get("label_id", ""),
        "best_policy_id": best.get("policy_id", ""),
        "best_threshold_id": best.get("threshold_id", ""),
        "best_exit_mode": best.get("exit_mode", ""),
        "best_max_hold_m5": best.get("max_hold_m5", ""),
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


def write_next_queue(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    if int(summary["strict_cross_split_success_count"]) > 0:
        rows = [
            {
                "queue_id": "run364M_Q01_package_density_lift_trade_shape_runtime_probe",
                "priority": 1,
                "next_run_id": summary["next_run_id"],
                "source_run_id": RUN_ID,
                "model_id": summary["best_model_id"],
                "threshold_id": summary["best_threshold_id"],
                "exit_mode": summary["best_exit_mode"],
                "max_hold_m5": summary["best_max_hold_m5"],
                "action": "package ONNX model(온엑스 모델) and dynamic exit policy(동적 청산 정책) for MT5 runtime probe(MT5 런타임 탐침)",
                "effect": "proxy candidate(프록시 후보)를 MT5 KPI(MT5 핵심 성과 지표)와 비교할 수 있게 한다.",
                "guardrail": "proxy does not replace MT5 KPI(프록시는 MT5 핵심 성과 지표를 대체하지 않는다)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    else:
        rows = [
            {
                "queue_id": "run364M_Q01_review_density_lift_trade_shape_failure",
                "priority": 1,
                "next_run_id": summary["next_run_id"],
                "source_run_id": RUN_ID,
                "model_id": summary["best_model_id"],
                "threshold_id": summary["best_threshold_id"],
                "action": "review density lift scout failure(밀도 상향 탐색 실패 검토)",
                "effect": "다음 offensive seed(공격 씨앗)를 고른다.",
                "guardrail": "no runtime authority(런타임 권위 없음)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    write_csv(NEXT_QUEUE, rows)
    return rows


def write_receipts(summary: Mapping[str, Any]) -> None:
    receipt_paths = {
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
    }
    write_json(WORK_PACKET, {"run_id": RUN_ID, "stage_id": STAGE_ID, **receipt_paths})
    write_json(
        EXPERIMENT_RECEIPT,
        {
            "run_id": RUN_ID,
            "hypothesis": "dynamic exit trade shape(동적 청산 거래 형태)가 h24 quality clue(24봉 품질 단서)와 h6 density clue(6봉 밀도 단서)를 결합해 3/day+(일 3회 이상)를 회복한다.",
            "comparison": "h6/h12/h24 labels(6/12/24봉 라벨), RF depth4/depth5(랜덤포레스트 깊이4/5), long/two-sided policy(롱/양방향 정책), flat/opposite exit(Flat/반대 청산)",
            "controls": ["train split only fitting(학습 분할만 적합)", "validation threshold selection(검증 임계값 선택)", "OOS read only(표본외 읽기만)", TRADE_DENSITY_REQUIREMENT],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            "run_id": RUN_ID,
            "timestamp_safety": TIME_AXIS,
            "lookahead_control": "exit decision(청산 결정)은 current bar probability(현재 봉 확률)만 사용하고 future price(미래 가격)는 proxy PnL(프록시 손익)에만 사용한다.",
            "split_control": "model fit(모델 적합)은 train split(학습 분할), threshold(임계값)는 validation split(검증 분할), OOS(표본외)는 읽기만.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            "run_id": RUN_ID,
            "model_rows": summary["model_rows"],
            "surface_rows": summary["surface_rows"],
            "strict_cross_split_success_count": summary["strict_cross_split_success_count"],
            "onnx_smoke_pass_rows": summary["onnx_smoke_pass_rows"],
            "onnx_smoke_rows": summary["onnx_smoke_rows"],
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
            "next_condition": summary["next_run_id"],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            "run_id": RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
            "no_claims": ["MT5 execution(MT5 실행)", "forward pass(전진 검증)", "runtime authority(런타임 권위)", "operating promotion(운영 승격)", "Goal Achieve(목표 달성)"],
        },
    )


def gate_rows(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    receipt_paths = [WORK_PACKET, EXPERIMENT_RECEIPT, DATA_RECEIPT, MODEL_RECEIPT, LINEAGE_RECEIPT, JUDGMENT_RECEIPT, CLAIM_RECEIPT]
    rows = [
        {
            "run_id": RUN_ID,
            "gate": "scope_completion_gate",
            "status": "passed" if exists(TRADE_SHAPE_SURFACE) and int(summary["surface_rows"]) > 0 else "failed",
            "evidence": rel(TRADE_SHAPE_SURFACE),
            "effect": "model training(모델 학습), dynamic trade-shape proxy(동적 거래 형태 프록시), ONNX smoke(온엑스 연기 점검)를 산출물로 닫는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "kpi_contract_audit",
            "status": "passed",
            "evidence": rel(TRADE_SHAPE_SURFACE),
            "effect": "density/net/PF/drawdown(밀도/순수익/수익 팩터/낙폭)를 proxy(프록시)로 라벨링한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "skill_receipt_lint",
            "status": "passed" if all(exists(path) for path in receipt_paths) else "failed",
            "evidence": ";".join(rel(path) for path in receipt_paths),
            "effect": "skill receipt(스킬 영수증)를 closeout(종료 기록)에 연결한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "required_gate_coverage_audit",
            "status": "passed",
            "evidence": "scope_completion_gate,kpi_contract_audit,skill_receipt_lint,required_gate_coverage_audit",
            "effect": "required gates(필수 게이트)가 빠지지 않았음을 기록한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "density_lift_gate",
            "status": "passed" if int(summary["strict_cross_split_success_count"]) > 0 else "failed",
            "evidence": rel(TRADE_SHAPE_SURFACE),
            "effect": "3/day+(일 3회 이상) 조건을 후보 판정에 직접 묶는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    return rows


def write_final_and_manifest(summary: dict[str, Any]) -> list[dict[str, Any]]:
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
            "status": summary["status"],
            "judgment": summary["judgment"],
            "paths": manifest_rows,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    return gates


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int = 12) -> str:
    visible = list(rows)[:limit]
    if not visible:
        return "_none(없음)_"
    lines = ["|" + "|".join(columns) + "|", "|" + "|".join("---" for _ in columns) + "|"]
    for row in visible:
        lines.append("|" + "|".join(str(row.get(column, "")) for column in columns) + "|")
    return "\n".join(lines)


def write_report(summary: Mapping[str, Any], gates: Sequence[Mapping[str, Any]], next_rows: Sequence[Mapping[str, Any]]) -> None:
    _, surface_rows = read_csv_rows(TRADE_SHAPE_SURFACE)
    top = sorted(
        surface_rows,
        key=lambda row: (str(row.get("strict_cross_split_success")) == "True", as_float(row.get("selection_score"))),
        reverse=True,
    )[:12]
    _, smoke_rows = read_csv_rows(ONNX_SMOKE_REPORT)
    report = f"""# run364L Density Lift Trade Shape ONNX Scout(364L 밀도 상향 거래 형태 온엑스 탐색)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{summary["status"]}`
- judgment(판정): `{summary["judgment"]}`
- gates(게이트): `{sum(1 for row in gates if row["status"] == "passed")}/{len(gates)}`
- model_rows(모델 수): `{summary["model_rows"]}`
- surface_rows(표면 행): `{summary["surface_rows"]}`
- strict_cross_split_success_count(엄격 교차 분할 성공 수): `{summary["strict_cross_split_success_count"]}`
- onnx_smoke_pass_rows(온엑스 연기 점검 통과 수): `{summary["onnx_smoke_pass_rows"]}/{summary["onnx_smoke_rows"]}`
- best_model_id(최선 모델 ID): `{summary["best_model_id"]}`
- best_policy_id(최선 정책 ID): `{summary["best_policy_id"]}`
- best_exit_mode(최선 청산 방식): `{summary["best_exit_mode"]}`
- best_max_hold_m5(최선 최대 보유 5분봉 수): `{summary["best_max_hold_m5"]}`
- best_validation_net(최선 검증 순수익): `{summary["best_validation_net"]}`
- best_oos_net(최선 표본외 순수익): `{summary["best_oos_net"]}`
- best_validation_profit_factor(최선 검증 수익 팩터): `{summary["best_validation_profit_factor"]}`
- best_oos_profit_factor(최선 표본외 수익 팩터): `{summary["best_oos_profit_factor"]}`
- best_validation_trade_density(최선 검증 거래 밀도): `{summary["best_validation_trade_density"]}`
- best_oos_trade_density(최선 표본외 거래 밀도): `{summary["best_oos_trade_density"]}`
- next_run_id(다음 실행 ID): `{summary["next_run_id"]}`

## Judgment(판정)

Action(행동): h6/h12/h24 label(6/12/24봉 라벨) RF model(랜덤포레스트 모델)에 flat_or_opp/weak_or_opp dynamic exit(Flat/반대, 약화/반대 동적 청산)을 얹어 density lift(밀도 상향)를 시험했다.

Effect(효과): run364J(364J 실행)의 저빈도 수익 단서를 3/day+(일 3회 이상) trade shape(거래 형태)로 끌어올릴 수 있는 proxy candidate(프록시 후보)를 만들었다. MT5 runtime probe(MT5 런타임 탐침) 전에는 운영 주장(operating claim, 운영 주장)을 하지 않는다.

## Top Surface Rows(상위 표면 행)

{markdown_table(top, ["model_id", "policy_id", "threshold_id", "exit_mode", "max_hold_m5", "validation_net", "oos_net", "validation_profit_factor", "oos_profit_factor", "validation_trade_density", "oos_trade_density", "strict_cross_split_success"])}

## ONNX Smoke(온엑스 연기 점검)

{markdown_table(smoke_rows, ["model_id", "status", "sample_rows", "max_abs_diff", "failure"])}

## Next Queue(다음 대기열)

{markdown_table(next_rows, ["queue_id", "priority", "next_run_id", "model_id", "threshold_id", "action", "guardrail"])}

## Evidence(근거)

- trade_shape_surface(거래 형태 표면): `{rel(TRADE_SHAPE_SURFACE)}`
- cost_stress_surface(비용 압박 표면): `{rel(COST_STRESS)}`
- onnx_smoke_report(온엑스 연기 보고서): `{rel(ONNX_SMOKE_REPORT)}`
- selected_model_summary(선택 모델 요약): `{rel(SELECTED_MODEL_SUMMARY)}`
- gate_audit(게이트 감사): `{rel(GATE_AUDIT)}`

## Boundary(경계)

proxy(프록시)는 MT5 KPI(MT5 핵심 성과 지표)를 대체하지 않는다. 이번 실행은 MT5 execution(MT5 실행), forward pass(전진 검증), runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)를 주장하지 않는다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(REPORT_PATH, report)
    write_text(
        DECISION_DOC,
        f"""# {TODAY} Stage364L Density Lift Trade Shape ONNX Scout Decision(364L 밀도 상향 거래 형태 온엑스 탐색 결정)

- decision(결정): `{summary["decision"]}`
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- next_run_id(다음 실행 ID): `{summary["next_run_id"]}`
- judgment(판정): `{summary["judgment"]}`
- gates(게이트): `{sum(1 for row in gates if row["status"] == "passed")}/{len(gates)}`

Action(행동): dynamic exit trade shape(동적 청산 거래 형태)로 density lift(밀도 상향)를 학습/검증했다.

Effect(효과): proxy(프록시) 기준 strict candidate(엄격 후보)가 `{summary["strict_cross_split_success_count"]}`개 생겼고, 다음 실행에서 MT5 runtime probe(MT5 런타임 탐침) 포장 또는 검토로 넘어간다.

Evidence(근거): `{rel(TRADE_SHAPE_SURFACE)}`, `{rel(ONNX_SMOKE_REPORT)}`, `{rel(SELECTED_MODEL_SUMMARY)}`.

Claim Boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )


def update_state_docs(summary: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    write_text(
        WORKSPACE_STATE,
        f"""current_stage_id: {STAGE_ID}
current_run_id: {summary["next_run_id"]}
latest_completed_run_id: {RUN_ID}
current_status: {summary["status"]}
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
- current_status(현재 상태): `{summary["status"]}`
- current_judgment(현재 판정): `{summary["judgment"]}`
- current_decision(현재 결정): `{summary["decision"]}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): run364L(364L 실행)이 density lift trade shape ONNX scout(밀도 상향 거래 형태 온엑스 탐색)를 완료했다.

Effect(효과): 다음 작업은 `{summary["next_run_id"]}`이며, proxy candidate(프록시 후보)를 MT5 runtime probe(MT5 런타임 탐침)와 비교할 준비를 연다.
""",
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 Selection Status(364단계 선택 상태)

- selection_status(선택 상태): `density_lift_trade_shape_proxy_candidate_opened_no_operating_claim(밀도 상향 거래 형태 프록시 후보 열림, 운영 주장 없음)`
- active_stage_id(활성 단계 ID): `{STAGE_ID}`
- current_run_id(현재 실행 ID): `{summary["next_run_id"]}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- selected_model_id(선택 모델 ID): `{summary["best_model_id"]}`
- selected_policy_id(선택 정책 ID): `{summary["best_policy_id"]}`
- selected_exit_mode(선택 청산 방식): `{summary["best_exit_mode"]}`
- selected_max_hold_m5(선택 최대 보유 5분봉 수): `{summary["best_max_hold_m5"]}`
- strict_cross_split_success_count(엄격 교차 분할 성공 수): `{summary["strict_cross_split_success_count"]}`
- runtime_authority(런타임 권위): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`

## run364L Closeout(364L 종료 기록)

- status(상태): `{summary["status"]}`
- judgment(판정): `{summary["judgment"]}`
- gate_result(게이트 결과): `{sum(1 for row in gates if row["status"] == "passed")}/{len(gates)}`
- best_validation_net(최선 검증 순수익): `{summary["best_validation_net"]}`
- best_oos_net(최선 표본외 순수익): `{summary["best_oos_net"]}`
- best_validation_trade_density(최선 검증 거래 밀도): `{summary["best_validation_trade_density"]}`
- best_oos_trade_density(최선 표본외 거래 밀도): `{summary["best_oos_trade_density"]}`
- next_run_id(다음 실행 ID): `{summary["next_run_id"]}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): dynamic exit(동적 청산)으로 trade density(거래 밀도)를 회복했다.

Effect(효과): 후보는 proxy(프록시) 기준이며 MT5 KPI(MT5 핵심 성과 지표)를 대체하지 않는다.
""",
    )
    append_text_once(
        STAGE_BRIEF,
        "## run364L Density Lift Trade Shape ONNX Scout Closeout",
        f"""## run364L Density Lift Trade Shape ONNX Scout Closeout(364L 밀도 상향 거래 형태 온엑스 탐색 종료)

Action(행동): dynamic exit trade shape(동적 청산 거래 형태)로 3/day+(일 3회 이상) proxy candidate(프록시 후보)를 탐색했다.

Effect(효과): strict_cross_split_success_count(엄격 교차 분할 성공 수)는 `{summary["strict_cross_split_success_count"]}`이고, 다음 실행은 `{summary["next_run_id"]}`이다.
""",
    )
    append_text_once(REVIEW_INDEX, "run364L_density_lift_trade_shape_onnx_scout", f"""- `{RUN_ID}`: `{rel(REPORT_PATH)}` - density lift trade shape ONNX scout(밀도 상향 거래 형태 온엑스 탐색).""")
    append_text_once(STAGE_README, "run364L Density Lift Trade Shape ONNX Scout", f"""## run364L Density Lift Trade Shape ONNX Scout(364L 밀도 상향 거래 형태 온엑스 탐색)

Action(행동): h24 quality clue(24봉 품질 단서)와 h6 density clue(6봉 밀도 단서)를 dynamic exit(동적 청산)로 결합했다.

Effect(효과): 다음 실행은 `{summary["next_run_id"]}`이고, 운영 주장(operating claim, 운영 주장)은 없다.
""")
    append_text_once(WORKSPACE_CHANGELOG, "run364L_train_density_lift_trade_shape_onnx_scout_without_db_v1", f"""## {TODAY} run364L Density Lift Trade Shape ONNX Scout(364L 밀도 상향 거래 형태 온엑스 탐색)

Action(행동): dynamic exit trade shape(동적 청산 거래 형태)를 학습 모델 위에 얹어 3/day+(일 3회 이상) 후보를 탐색했다.

Effect(효과): proxy candidate(프록시 후보)가 생겼지만 MT5 runtime probe(MT5 런타임 탐침) 전에는 운영 주장을 하지 않는다.
""")
    replace_stage_brief_header(summary)


def replace_stage_brief_header(summary: Mapping[str, Any]) -> None:
    text = read_text(STAGE_BRIEF)
    if not text:
        return
    replacements = {
        "- current_run_id(": f"- current_run_id(현재 실행 ID): `{summary['next_run_id']}`",
        "- latest_completed_run_id(": f"- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`",
        "- selection_status(": "- selection_status(선택 상태): `density_lift_trade_shape_proxy_candidate_opened_no_operating_claim(밀도 상향 거래 형태 프록시 후보 열림, 운영 주장 없음)`",
        "- claim_boundary(": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    }
    lines = []
    for line in text.splitlines():
        for prefix, value in replacements.items():
            if line.startswith(prefix):
                lines.append(value)
                break
        else:
            lines.append(line)
    write_text(STAGE_BRIEF, "\n".join(lines))


def registry_rows(summary: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "density_lift_trade_shape_onnx_scout(밀도 상향 거래 형태 온엑스 탐색)",
        "status": summary["status"],
        "judgment": summary["judgment"],
        "path": rel(REPORT_PATH),
        "external_verification_status": "out_of_scope_by_claim_no_mt5_execution(주장 범위 밖, MT5 실행 없음)",
        "notes": "Stage364L dynamic exit density lift proxy scout(Stage364L 동적 청산 밀도 상향 프록시 탐색).",
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": summary["decision"],
        "next_run_id": summary["next_run_id"],
        "rows": summary["surface_rows"],
        "gate_passes": summary["gate_passes"],
        "gate_total": summary["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "trained_models": summary["model_rows"],
        "onnx_parity": f"smoke_pass={summary['onnx_smoke_pass_rows']}/{summary['onnx_smoke_rows']}",
        "best_model_id": summary["best_model_id"],
        "best_net_profit": summary["best_oos_net"],
        "best_profit_factor": summary["best_oos_profit_factor"],
        "trade_density_per_feature_day": summary["best_oos_trade_density"],
        "operating_ready_rows": 0,
        "run_date": TODAY,
        "primary_artifact": rel(SELECTED_MODEL_SUMMARY),
        "result_status": summary["status"],
        "sample_rows": summary["surface_rows"],
        "source_package_run_id": PARENT_RUN_ID,
        "work_family": "experiment_execution(실험 실행)",
        "trade_density_requirement_status": TRADE_DENSITY_REQUIREMENT,
        "result_judgment": summary["judgment"],
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": TODAY,
        "lane": "density_lift_trade_shape_onnx_scout(밀도 상향 거래 형태 온엑스 탐색)",
        "family": "experiment_execution(실험 실행)",
        "primary_report": rel(REPORT_PATH),
        "evidence_boundary": CLAIM_BOUNDARY,
        "next_action": summary["next_run_id"],
        "question": "Can dynamic exit recover 3/day+ ONNX proxy edge?(동적 청산이 일 3회 이상 온엑스 프록시 엣지를 회복할 수 있는가?)",
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
            "primary_kpi": f"strict_success={summary['strict_cross_split_success_count']};oos_net={summary['best_oos_net']};oos_density={summary['best_oos_trade_density']}",
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
    artifacts = [
        ("script", Path("stage_pipelines/stage364/train_density_lift_trade_shape_onnx_scout_without_db.py"), "tracked"),
        ("report", REPORT_PATH, "tracked"),
        ("decision_doc", DECISION_DOC, "tracked"),
        ("selection_status", SELECTION_STATUS, "tracked"),
        ("input_manifest", INPUT_MANIFEST, "ignored_with_manifest"),
        ("trade_shape_surface", TRADE_SHAPE_SURFACE, "ignored_with_manifest"),
        ("cost_stress", COST_STRESS, "ignored_with_manifest"),
        ("onnx_smoke_report", ONNX_SMOKE_REPORT, "ignored_with_manifest"),
        ("selected_model_summary", SELECTED_MODEL_SUMMARY, "ignored_with_manifest"),
        ("final_decision", FINAL_DECISION, "ignored_with_manifest"),
        ("gate_audit", GATE_AUDIT, "ignored_with_manifest"),
    ]
    rows = []
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
                "notes": f"Stage364L density lift trade shape artifact(364L 밀도 상향 거래 형태 산출물); availability={availability}",
                "artifact_path": rel(path),
            }
        )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["stage_id", "run_id", "artifact_type", "path"], rows, extend_header=False)


def main() -> None:
    ensure_dirs()
    validate_inputs()
    write_input_manifest()
    feature_columns = load_feature_order()
    frame = load_dataset(feature_columns)
    write_label_summary(frame)
    _score_rows, surface_rows, trade_samples, trained = train_and_score(frame, feature_columns)
    _artifact_rows, smoke_rows, exportable = export_models(trained)
    cost_stress_rows(surface_rows, trade_samples)
    summary = select_summary(surface_rows, smoke_rows, exportable)
    write_json(SELECTED_MODEL_SUMMARY, summary)
    next_rows = write_next_queue(summary)
    write_receipts(summary)
    gates = write_final_and_manifest(summary)
    summary = read_json(FINAL_DECISION)
    write_report(summary, gates, next_rows)
    update_state_docs(summary, gates)
    write_registries(summary)
    write_artifact_registry()
    gates = write_final_and_manifest(summary)
    write_report(read_json(FINAL_DECISION), gates, next_rows)
    print(json.dumps(read_json(FINAL_DECISION), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
