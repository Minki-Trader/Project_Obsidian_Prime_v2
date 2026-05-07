from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd

from foundation.control_plane.ledger import io_path, json_ready, sha256_file_lf_normalized
from foundation.control_plane.mt5_tier_balance_completion import (
    FEATURE_ORDER_PATH,
    MODEL_INPUT_PATH,
    RAW_ROOT,
    TRAINING_SUMMARY_PATH,
)
from foundation.models.baseline_training import load_feature_order, validate_model_input_frame
from foundation.mt5 import runtime_support as mt5


ROOT = Path(__file__).resolve().parents[2]
LABEL_ID = "label_v1_fwd12_m5_logret_train_q33_3class"
SPLIT_CONTRACT = "split_v1_calendar_train_20220901_20241231_val_20250101_20260413"
WORKSPACE_STATE_PATH = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE_PATH = ROOT / "docs/context/current_working_state.md"
GOAL_PLAN_PATH = ROOT / "docs/workspace/stage20_32_goal_operating_plan.md"
DEFAULT_MAX_HORIZON_BARS = 12


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in (None, "", "NA"):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: json_ready(row.get(column, "")) for column in columns})


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def save_frame(path: Path, frame: pd.DataFrame) -> dict[str, Any]:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    if path.suffix == ".parquet":
        frame.to_parquet(io_path(path), index=False)
    else:
        frame.to_csv(io_path(path), index=False)
    return {"path": rel(path), "rows": int(len(frame)), "sha256": sha256_file_lf_normalized(path)}


def load_context() -> dict[str, Any]:
    tier_a_frame = pd.read_parquet(io_path(MODEL_INPUT_PATH))
    full_feature_order = load_feature_order(FEATURE_ORDER_PATH)
    validate_model_input_frame(tier_a_frame, full_feature_order)
    training_summary = read_json(TRAINING_SUMMARY_PATH)
    tier_b_feature_order = list(mt5.TIER_B_CORE_FEATURE_ORDER)
    tier_b_context = mt5.build_tier_b_partial_context_frames(
        raw_root=RAW_ROOT,
        tier_a_frame=tier_a_frame,
        tier_a_feature_order=full_feature_order,
        tier_b_feature_order=tier_b_feature_order,
        label_threshold=float(training_summary["threshold_log_return"]),
    )
    return {
        "tier_a_frame": tier_a_frame,
        "full_feature_order": full_feature_order,
        "tier_b_training_frame": tier_b_context["tier_b_training_frame"],
        "tier_b_fallback_frame": tier_b_context["tier_b_fallback_frame"],
        "tier_b_feature_order": tier_b_feature_order,
        "tier_b_context_summary": tier_b_context["summary"],
        "training_summary": training_summary,
    }


def core24_features() -> tuple[str, ...]:
    return (
        "log_return_1",
        "log_return_3",
        "return_zscore_20",
        "hl_range",
        "atr_14",
        "atr_14_over_atr_50",
        "bollinger_width_20",
        "adx_14",
        "di_spread_14",
        "ema20_ema50_diff",
        "ema20_ema50_spread_zscore_50",
        "rsi_14",
        "rsi_14_slope_3",
        "bb_position_20",
        "stoch_kd_diff",
        "ppo_hist_12_26_9",
        "roc_12",
        "historical_vol_20",
        "minutes_from_cash_open",
        "is_us_cash_open",
        "is_first_30m_after_open",
        "close_ema20_ratio",
        "close_open_ratio",
        "vortex_indicator",
    )


def volatility_session_features() -> tuple[str, ...]:
    return (
        "log_return_1",
        "log_return_3",
        "return_zscore_20",
        "hl_range",
        "atr_14",
        "atr_14_over_atr_50",
        "bollinger_width_20",
        "historical_vol_20",
        "adx_14",
        "di_spread_14",
        "rsi_14",
        "rsi_14_slope_3",
        "minutes_from_cash_open",
        "is_first_30m_after_open",
    )


def add_future_return_path(frame: pd.DataFrame, max_horizon_bars: int = DEFAULT_MAX_HORIZON_BARS) -> pd.DataFrame:
    work = frame.sort_values("timestamp").reset_index(drop=True).copy()
    returns = pd.to_numeric(work["log_return_1"], errors="coerce").fillna(0.0)
    cumulative = pd.Series(np.zeros(len(work), dtype="float64"))
    for horizon in range(1, max_horizon_bars + 1):
        cumulative = cumulative + returns.shift(-horizon)
        work[f"future_cum_log_return_{horizon}"] = cumulative.to_numpy(dtype="float64", copy=False)
    return work


def label_direction(frame: pd.DataFrame) -> np.ndarray:
    if "label_id" in frame.columns:
        label_id = pd.to_numeric(frame["label_id"], errors="coerce")
        direction = np.where(label_id.eq(2), 1, np.where(label_id.eq(0), -1, 0))
        return direction.astype("int8")
    label_text = frame.get("label_class", pd.Series([""] * len(frame))).astype(str).str.lower()
    direction = np.where(
        label_text.str.contains("long|up|buy"),
        1,
        np.where(label_text.str.contains("short|down|sell"), -1, 0),
    )
    return direction.astype("int8")


def event_duration_arrays(
    frame: pd.DataFrame,
    spec: Any,
    base_threshold: float,
    *,
    max_horizon_bars: int = DEFAULT_MAX_HORIZON_BARS,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    future_cols = [f"future_cum_log_return_{horizon}" for horizon in range(1, max_horizon_bars + 1)]
    values = frame[future_cols].to_numpy(dtype="float64", copy=False)
    threshold = abs(float(base_threshold) * float(spec.threshold_multiplier))
    directions = label_direction(frame)
    durations: list[int] = []
    events: list[int] = []
    usable_mask: list[bool] = []
    for row_index in range(len(frame)):
        row = values[row_index]
        valid_count = int(np.isfinite(row).sum())
        if valid_count < 1:
            durations.append(0)
            events.append(0)
            usable_mask.append(False)
            continue
        horizon_values = row[:valid_count]
        direction = int(directions[row_index])
        if spec.event_name == "abs_move_3x":
            hits = np.flatnonzero(np.abs(horizon_values) >= threshold)
            usable = True
        elif spec.event_name == "adverse_direction_1p5x":
            if direction == 0:
                hits = np.array([], dtype=int)
                usable = False
            else:
                signed_path = direction * horizon_values
                hits = np.flatnonzero(signed_path <= -threshold)
                usable = True
        elif spec.event_name == "profit_decay_after_peak_2x":
            if direction == 0:
                hits = np.array([], dtype=int)
                usable = False
            else:
                signed_path = direction * horizon_values
                peak_path = np.maximum.accumulate(signed_path)
                peak_threshold = abs(float(base_threshold) * float(spec.peak_multiplier or 2.0))
                hits = np.flatnonzero((peak_path >= peak_threshold) & (signed_path <= peak_path * 0.5))
                usable = True
        else:
            raise ValueError(f"Unknown event_name: {spec.event_name}")
        if hits.size:
            durations.append(int(hits[0]) + 1)
            events.append(1)
        else:
            durations.append(valid_count)
            events.append(0)
        usable_mask.append(usable)
    return (
        np.asarray(durations, dtype="int16"),
        np.asarray(events, dtype="int8"),
        np.asarray(usable_mask, dtype=bool),
    )


def build_survival_frame(
    frame: pd.DataFrame,
    spec: Any,
    base_threshold: float,
    *,
    max_horizon_bars: int = DEFAULT_MAX_HORIZON_BARS,
) -> pd.DataFrame:
    work = add_future_return_path(frame, max_horizon_bars)
    durations, events, usable = event_duration_arrays(work, spec, base_threshold, max_horizon_bars=max_horizon_bars)
    work["duration_bars"] = durations
    work["event_observed"] = events
    work["event_name"] = spec.event_name
    work["threshold_multiplier"] = float(spec.threshold_multiplier)
    work["event_threshold_abs_log_return"] = abs(float(base_threshold) * float(spec.threshold_multiplier))
    work = work.loc[usable & (work["duration_bars"] >= 1)].copy()
    work["event_observed"] = work["event_observed"].astype("int8")
    work["duration_bars"] = work["duration_bars"].astype("int16")
    return work


def fit_preprocessor(train: pd.DataFrame, feature_names: Sequence[str]) -> dict[str, Any]:
    raw = train.loc[:, list(feature_names)].apply(pd.to_numeric, errors="coerce").replace([np.inf, -np.inf], np.nan)
    medians = raw.median(axis=0).fillna(0.0)
    filled = raw.fillna(medians)
    variances = filled.var(axis=0)
    usable = [
        column
        for column in filled.columns
        if float(variances.get(column, 0.0)) > 1.0e-12 and filled[column].nunique(dropna=True) > 1
    ]
    if not usable:
        raise ValueError("No usable model features after low-variance filtering.")
    means = filled.loc[:, usable].mean(axis=0)
    stds = filled.loc[:, usable].std(axis=0).replace(0.0, 1.0).fillna(1.0)
    return {
        "feature_names": list(usable),
        "dropped_features": [name for name in feature_names if name not in set(usable)],
        "medians": {name: float(medians.get(name, 0.0)) for name in usable},
        "means": {name: float(means.get(name, 0.0)) for name in usable},
        "stds": {name: float(stds.get(name, 1.0)) for name in usable},
        "clip": 8.0,
    }


def transform_features(frame: pd.DataFrame, preprocess: Mapping[str, Any]) -> pd.DataFrame:
    features = list(preprocess["feature_names"])
    raw = frame.loc[:, features].apply(pd.to_numeric, errors="coerce").replace([np.inf, -np.inf], np.nan)
    for name in features:
        raw[name] = raw[name].fillna(float(preprocess["medians"].get(name, 0.0)))
        raw[name] = (raw[name] - float(preprocess["means"].get(name, 0.0))) / float(preprocess["stds"].get(name, 1.0))
    return raw.clip(lower=-float(preprocess.get("clip", 8.0)), upper=float(preprocess.get("clip", 8.0)))


def replace_markdown_section(text: str, heading_prefix: str, new_section: str) -> str:
    start = text.find(heading_prefix)
    if start < 0:
        return text.rstrip() + "\n\n" + new_section.rstrip() + "\n"
    next_start = text.find("\n## ", start + 1)
    if next_start < 0:
        return text[:start] + new_section.rstrip() + "\n"
    return text[:start] + new_section.rstrip() + "\n\n" + text[next_start + 1 :]


def replace_top_level_yaml_block(text: str, marker: str, block: str) -> str:
    pattern = re.compile(rf"^{re.escape(marker)}:\n(?:^[^\S\r\n]{{2}}.*\n?)+", re.MULTILINE)
    replacement = block.rstrip() + "\n"
    if pattern.search(text):
        return pattern.sub(replacement, text, count=1)
    return text.rstrip() + "\n" + replacement
