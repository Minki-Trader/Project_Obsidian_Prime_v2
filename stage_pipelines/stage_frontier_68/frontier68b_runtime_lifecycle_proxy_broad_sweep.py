from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier, HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from stage_pipelines.stage_frontier_68.frontier68a_bridge_feasibility_and_label_design import (
    STAGE_ID,
    rel,
    sha256_file,
    upsert_ledger,
    write_csv,
    write_json,
    write_md,
)


RUN_ID = "frontier68B_runtime_lifecycle_proxy_broad_sweep_v1"
PARENT_RUN_ID = "frontier68A_stage_open_lifecycle_economics_proxy_design_v1"
NEXT_RUN_ID = "frontier68C_candidate_scoring_or_onnx_scout_export_v1"

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"

MODEL_INPUT = ROOT / "data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet"
RAW_US100 = ROOT / "data/raw/mt5_bars/m5/US100/bars_us100_m5_mt5api_raw.csv"
F68A_LABEL_DESIGN = REVIEWS_ROOT / "f68a_lifecycle_label_design_review.json"

CLAIM_BOUNDARY = (
    "proxy_broad_sweep_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

FEATURE_EXCLUDE = {
    "timestamp",
    "symbol",
    "future_timestamp",
    "future_log_return_12",
    "label",
    "label_class",
    "label_id",
    "split",
    "split_id",
    "horizon_bars",
    "horizon_minutes",
}


@dataclass(frozen=True)
class TargetSpec:
    target_id: str
    horizon_bars: int
    family: str
    min_utility_points: float
    mae_penalty: float
    cost_multiplier: float
    atr_stop_multiplier: float = 1.0
    atr_take_profit_multiplier: float = 1.5


@dataclass(frozen=True)
class ModelSpec:
    model_id: str
    family: str
    estimator: Any


@dataclass(frozen=True)
class FeatureSet:
    feature_set_id: str
    columns: tuple[str, ...]


@dataclass(frozen=True)
class EvalSpec:
    quantile: float
    cooldown_bars: int
    side_policy: str
    exit_mode: str


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def stable_id(parts: Sequence[Any]) -> str:
    text = "|".join(str(part) for part in parts)
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:12]


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def fmt(value: Any, digits: int = 6) -> str:
    if value is None:
        return ""
    try:
        number = float(value)
    except (TypeError, ValueError):
        return str(value)
    if not math.isfinite(number):
        return ""
    if abs(number - round(number)) < 1e-9:
        return str(int(round(number)))
    return f"{number:.{digits}f}".rstrip("0").rstrip(".")


def load_frames() -> tuple[pd.DataFrame, pd.DataFrame, np.ndarray]:
    model_input = pd.read_parquet(io_path(MODEL_INPUT))
    raw = pd.read_csv(
        io_path(RAW_US100),
        usecols=["time_close_unix", "high", "low", "close", "spread_points"],
    )
    raw["timestamp"] = pd.to_datetime(raw["time_close_unix"], unit="s", utc=True)
    raw = raw.sort_values("timestamp").reset_index(drop=True)
    raw_positions = pd.Series(raw.index.to_numpy(), index=raw["timestamp"]).reindex(model_input["timestamp"]).to_numpy()
    if np.isnan(raw_positions).any():
        missing = int(np.isnan(raw_positions).sum())
        raise RuntimeError(f"raw/model timestamp alignment failed: {missing} missing rows")
    return model_input, raw, raw_positions.astype(int)


def feature_sets(model_input: pd.DataFrame) -> list[FeatureSet]:
    all_features = [col for col in model_input.columns if col not in FEATURE_EXCLUDE]
    mega_prefixes = ("nvda_", "aapl_", "msft_", "amzn_", "mega8_", "top3_", "us100_minus_mega8", "us100_minus_top3")
    macro_prefixes = ("vix_", "us10yr_", "usdx_")
    session_cols = {"is_us_cash_open", "minutes_from_cash_open", "is_first_30m_after_open", "is_last_30m_before_cash_close"}
    no_mega = [col for col in all_features if not col.startswith(mega_prefixes)]
    core = [
        col
        for col in all_features
        if not col.startswith(mega_prefixes)
        and not col.startswith(macro_prefixes)
        and col not in session_cols
    ]
    session_regime = [col for col in all_features if col in core or col in session_cols or col.startswith(macro_prefixes)]
    return [
        FeatureSet("full58(전체58)", tuple(all_features)),
        FeatureSet("no_mega_top3(대형주_상위3제외)", tuple(no_mega)),
        FeatureSet("core_technical(핵심기술)", tuple(core)),
        FeatureSet("session_regime_no_mega(세션국면_대형주제외)", tuple(session_regime)),
    ]


def target_specs() -> list[TargetSpec]:
    return [
        TargetSpec("h1_ddp03_min1p5(1봉_손실벌점)", 1, "dd_penalized_close(손실폭벌점종가)", 1.5, 0.30, 1.0),
        TargetSpec("h2_ddp03_min1p5(2봉_손실벌점)", 2, "dd_penalized_close(손실폭벌점종가)", 1.5, 0.30, 1.0),
        TargetSpec("h3_ddp03_min1p5(3봉_손실벌점)", 3, "dd_penalized_close(손실폭벌점종가)", 1.5, 0.30, 1.0),
        TargetSpec("h6_ddp04_min3(6봉_손실벌점)", 6, "dd_penalized_close(손실폭벌점종가)", 3.0, 0.40, 1.0),
        TargetSpec("h9_ddp04_min3(9봉_손실벌점)", 9, "dd_penalized_close(손실폭벌점종가)", 3.0, 0.40, 1.0),
        TargetSpec("h12_ddp05_min5(12봉_손실벌점)", 12, "dd_penalized_close(손실폭벌점종가)", 5.0, 0.50, 1.0),
        TargetSpec("h12_atr_firsthit(12봉_ATR선타격)", 12, "atr_first_hit(평균진폭_선타격)", 0.0, 0.0, 1.0, 1.0, 1.5),
    ]


def model_specs() -> list[ModelSpec]:
    return [
        ModelSpec(
            "logreg_balanced(균형로지스틱)",
            "linear(선형)",
            make_pipeline(
                SimpleImputer(strategy="median"),
                StandardScaler(),
                LogisticRegression(max_iter=350, class_weight="balanced"),
            ),
        ),
        ModelSpec(
            "hgb_small(작은히스토그램부스팅)",
            "tree_boosting(트리부스팅)",
            make_pipeline(
                SimpleImputer(strategy="median"),
                HistGradientBoostingClassifier(
                    max_iter=80,
                    learning_rate=0.05,
                    max_leaf_nodes=15,
                    l2_regularization=0.10,
                    random_state=68,
                ),
            ),
        ),
        ModelSpec(
            "extra_trees_shallow(얕은엑스트라트리스)",
            "tree_bagging(트리배깅)",
            make_pipeline(
                SimpleImputer(strategy="median"),
                ExtraTreesClassifier(
                    n_estimators=120,
                    max_depth=10,
                    min_samples_leaf=60,
                    class_weight="balanced",
                    random_state=68,
                    n_jobs=-1,
                ),
            ),
        ),
    ]


def eval_specs() -> list[EvalSpec]:
    quantiles = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.975]
    cooldowns = [0, 1, 3, 6, 12]
    side_policies = ["both(양방향)", "long_only(롱만)", "short_only(숏만)"]
    exit_modes = ["close_horizon(만기종가)", "atr_sltp_conservative(보수적_ATR손익절)"]
    return [
        EvalSpec(quantile=q, cooldown_bars=cd, side_policy=side, exit_mode=exit_mode)
        for q in quantiles
        for cd in cooldowns
        for side in side_policies
        for exit_mode in exit_modes
    ]


def future_path_payload(model_input: pd.DataFrame, raw: pd.DataFrame, raw_positions: np.ndarray, spec: TargetSpec) -> pd.DataFrame:
    horizon = int(spec.horizon_bars)
    valid = raw_positions + horizon < len(raw)
    frame = model_input.loc[valid].copy().reset_index(drop=True)
    idx = raw_positions[valid]
    high = raw["high"].to_numpy()
    low = raw["low"].to_numpy()
    close = raw["close"].to_numpy()
    entry_close = raw["close"].to_numpy()[idx]
    future_close = close[idx + horizon]
    max_high = np.array([high[i + 1 : i + horizon + 1].max() for i in idx], dtype=float)
    min_low = np.array([low[i + 1 : i + horizon + 1].min() for i in idx], dtype=float)
    spread_cost = frame["spread_points_proxy"].to_numpy(dtype=float) * 0.01 * float(spec.cost_multiplier)

    long_close_profit = future_close - entry_close - spread_cost
    short_close_profit = entry_close - future_close - spread_cost
    long_mae = entry_close - min_low
    short_mae = max_high - entry_close
    long_mfe = max_high - entry_close
    short_mfe = entry_close - min_low

    atr = frame["atr_14"].to_numpy(dtype=float)
    long_sltp = first_hit_profit(
        side=2,
        idx=idx,
        horizon=horizon,
        entry_close=entry_close,
        high=high,
        low=low,
        close=close,
        atr=atr,
        cost=spread_cost,
        stop_multiplier=spec.atr_stop_multiplier,
        take_profit_multiplier=spec.atr_take_profit_multiplier,
    )
    short_sltp = first_hit_profit(
        side=0,
        idx=idx,
        horizon=horizon,
        entry_close=entry_close,
        high=high,
        low=low,
        close=close,
        atr=atr,
        cost=spread_cost,
        stop_multiplier=spec.atr_stop_multiplier,
        take_profit_multiplier=spec.atr_take_profit_multiplier,
    )

    if spec.family.startswith("atr_first_hit"):
        long_utility = long_sltp - 0.25 * long_mae
        short_utility = short_sltp - 0.25 * short_mae
        min_utility = np.maximum(1.5, 0.15 * atr)
    else:
        long_utility = long_close_profit - float(spec.mae_penalty) * long_mae
        short_utility = short_close_profit - float(spec.mae_penalty) * short_mae
        min_utility = np.full_like(long_utility, float(spec.min_utility_points), dtype=float)

    y = np.where(
        (long_utility > min_utility) & (long_utility > short_utility),
        2,
        np.where((short_utility > min_utility) & (short_utility > long_utility), 0, 1),
    )
    frame["target_class"] = y
    frame["entry_close"] = entry_close
    frame["future_close"] = future_close
    frame["future_max_high"] = max_high
    frame["future_min_low"] = min_low
    frame["long_close_profit_points"] = long_close_profit
    frame["short_close_profit_points"] = short_close_profit
    frame["long_sltp_profit_points"] = long_sltp
    frame["short_sltp_profit_points"] = short_sltp
    frame["long_mae_points"] = long_mae
    frame["short_mae_points"] = short_mae
    frame["long_mfe_points"] = long_mfe
    frame["short_mfe_points"] = short_mfe
    frame["long_utility_points"] = long_utility
    frame["short_utility_points"] = short_utility
    return frame


def first_hit_profit(
    *,
    side: int,
    idx: np.ndarray,
    horizon: int,
    entry_close: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    atr: np.ndarray,
    cost: np.ndarray,
    stop_multiplier: float,
    take_profit_multiplier: float,
) -> np.ndarray:
    output = np.empty(len(idx), dtype=float)
    stop_distance = np.maximum(1.0, atr * float(stop_multiplier))
    take_distance = np.maximum(1.0, atr * float(take_profit_multiplier))
    for row_num, start in enumerate(idx):
        entry = float(entry_close[row_num])
        stop = float(stop_distance[row_num])
        take = float(take_distance[row_num])
        profit = (float(close[start + horizon]) - entry) if side == 2 else (entry - float(close[start + horizon]))
        for bar in range(start + 1, start + horizon + 1):
            if side == 2:
                stop_hit = float(low[bar]) <= entry - stop
                take_hit = float(high[bar]) >= entry + take
                if stop_hit:
                    profit = -stop
                    break
                if take_hit:
                    profit = take
                    break
            else:
                stop_hit = float(high[bar]) >= entry + stop
                take_hit = float(low[bar]) <= entry - take
                if stop_hit:
                    profit = -stop
                    break
                if take_hit:
                    profit = take
                    break
        output[row_num] = profit - float(cost[row_num])
    return output


def model_input_with_spread(model_input: pd.DataFrame, raw: pd.DataFrame) -> pd.DataFrame:
    spread_frame = raw[["timestamp", "spread_points"]].copy()
    frame = model_input.merge(spread_frame, on="timestamp", how="left")
    if frame["spread_points"].isna().any():
        raise RuntimeError("spread join failed")
    frame = frame.rename(columns={"spread_points": "spread_points_proxy"})
    return frame


def train_eval_surface(
    frame: pd.DataFrame,
    features: FeatureSet,
    model_spec: ModelSpec,
    target_spec: TargetSpec,
    eval_grid: Sequence[EvalSpec],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    train_mask = frame["split"].eq("train")
    validation_mask = frame["split"].eq("validation")
    oos_mask = frame["split"].eq("oos")
    label_counts = {
        split: {str(k): int(v) for k, v in frame.loc[frame["split"].eq(split), "target_class"].value_counts().to_dict().items()}
        for split in ["train", "validation", "oos"]
    }
    estimator = model_spec.estimator
    estimator.fit(frame.loc[train_mask, list(features.columns)], frame.loc[train_mask, "target_class"])
    classes = list(getattr(estimator, "classes_", getattr(estimator[-1], "classes_", [])))
    train_side, train_edge = side_and_edge(estimator.predict_proba(frame.loc[train_mask, list(features.columns)]), classes)
    train_edges = train_edge[train_edge > -100.0]
    if len(train_edges) == 0:
        train_edges = np.array([999.0])

    rows: list[dict[str, Any]] = []
    split_cache: dict[str, dict[str, Any]] = {}
    for split_name, mask in [("validation", validation_mask), ("oos", oos_mask)]:
        split_frame = frame.loc[mask].copy().reset_index(drop=True)
        proba = estimator.predict_proba(split_frame.loc[:, list(features.columns)])
        side, edge = side_and_edge(proba, classes)
        split_cache[split_name] = {"frame": split_frame, "side": side, "edge": edge}

    candidate_base = [
        target_spec.target_id,
        features.feature_set_id,
        model_spec.model_id,
    ]
    for eval_spec in eval_grid:
        threshold = float(np.quantile(train_edges, eval_spec.quantile))
        candidate_id = "f68b_" + stable_id([*candidate_base, eval_spec.quantile, eval_spec.cooldown_bars, eval_spec.side_policy, eval_spec.exit_mode])
        for split_name, cache in split_cache.items():
            split_frame = cache["frame"]
            edge = cache["edge"]
            side = cache["side"]
            side = apply_side_policy(side, eval_spec.side_policy)
            signal = (side != 1) & (edge >= threshold)
            profit = profit_for_side(split_frame, side, eval_spec.exit_mode)
            chosen = non_overlap_indices(signal, int(target_spec.horizon_bars), int(eval_spec.cooldown_bars))
            metrics = proxy_kpi(profit[chosen], split_frame.loc[chosen, "timestamp"] if chosen else split_frame["timestamp"].iloc[:0])
            long_count = int((side[chosen] == 2).sum()) if chosen else 0
            short_count = int((side[chosen] == 0).sum()) if chosen else 0
            row = {
                "candidate_id": candidate_id,
                "split": split_name,
                "target_id": target_spec.target_id,
                "target_family": target_spec.family,
                "horizon_bars": target_spec.horizon_bars,
                "feature_set_id": features.feature_set_id,
                "feature_count": len(features.columns),
                "model_id": model_spec.model_id,
                "model_family": model_spec.family,
                "threshold_quantile": eval_spec.quantile,
                "edge_threshold_from_train": threshold,
                "cooldown_bars": eval_spec.cooldown_bars,
                "side_policy": eval_spec.side_policy,
                "exit_mode": eval_spec.exit_mode,
                "signal_count": int(signal.sum()),
                "trade_count": metrics["trade_count"],
                "trades_per_day": metrics["trades_per_day"],
                "net_profit_proxy_points": metrics["net_profit"],
                "gross_profit_proxy_points": metrics["gross_profit"],
                "gross_loss_proxy_points": metrics["gross_loss"],
                "profit_factor": metrics["profit_factor"],
                "expectancy_proxy_points": metrics["expectancy"],
                "win_rate_percent": metrics["win_rate_percent"],
                "average_win_proxy_points": metrics["average_win"],
                "average_loss_proxy_points": metrics["average_loss"],
                "payoff_ratio": metrics["payoff_ratio"],
                "max_drawdown_proxy_points": metrics["max_drawdown"],
                "proxy_dd_percent_on_10000_points": metrics["proxy_dd_percent_on_10000"],
                "recovery_factor": metrics["recovery_factor"],
                "max_consecutive_loss": metrics["max_consecutive_loss"],
                "long_trade_count": long_count,
                "short_trade_count": short_count,
                "density_band_read": density_read(metrics["trades_per_day"]),
                "four_axis_distance_score": four_axis_distance(metrics),
                "claim_boundary": CLAIM_BOUNDARY,
            }
            rows.append(row)
    label_payload = {
        "target_id": target_spec.target_id,
        "feature_set_id": features.feature_set_id,
        "model_id": model_spec.model_id,
        "label_counts": label_counts,
        "classes_seen": [int(x) for x in classes],
    }
    return rows, [], label_payload


def side_and_edge(proba: np.ndarray, classes: Sequence[int]) -> tuple[np.ndarray, np.ndarray]:
    probs = {int(cls): proba[:, idx] for idx, cls in enumerate(classes)}
    zeros = np.zeros(len(proba), dtype=float)
    p_short = probs.get(0, zeros)
    p_flat = probs.get(1, zeros)
    p_long = probs.get(2, zeros)
    side = np.where(
        (p_long > p_short) & (p_long > p_flat),
        2,
        np.where((p_short > p_long) & (p_short > p_flat), 0, 1),
    )
    edge = np.where(
        side == 2,
        p_long - np.maximum(p_short, p_flat),
        np.where(side == 0, p_short - np.maximum(p_long, p_flat), -999.0),
    )
    return side.astype(int), edge.astype(float)


def apply_side_policy(side: np.ndarray, side_policy: str) -> np.ndarray:
    adjusted = side.copy()
    if side_policy.startswith("long_only"):
        adjusted[adjusted == 0] = 1
    if side_policy.startswith("short_only"):
        adjusted[adjusted == 2] = 1
    return adjusted


def profit_for_side(frame: pd.DataFrame, side: np.ndarray, exit_mode: str) -> np.ndarray:
    if exit_mode.startswith("atr_sltp"):
        long_col = "long_sltp_profit_points"
        short_col = "short_sltp_profit_points"
    else:
        long_col = "long_close_profit_points"
        short_col = "short_close_profit_points"
    long_profit = frame[long_col].to_numpy(dtype=float)
    short_profit = frame[short_col].to_numpy(dtype=float)
    return np.where(side == 2, long_profit, np.where(side == 0, short_profit, 0.0))


def non_overlap_indices(signal: np.ndarray, horizon_bars: int, cooldown_bars: int) -> list[int]:
    chosen: list[int] = []
    next_allowed = 0
    step = max(1, int(horizon_bars)) + max(0, int(cooldown_bars))
    for idx, ok in enumerate(signal):
        if bool(ok) and idx >= next_allowed:
            chosen.append(idx)
            next_allowed = idx + step
    return chosen


def proxy_kpi(profits: np.ndarray, times: pd.Series) -> dict[str, Any]:
    profits = np.asarray(profits, dtype=float)
    if len(profits) == 0:
        return {
            "trade_count": 0,
            "trades_per_day": 0.0,
            "net_profit": 0.0,
            "gross_profit": 0.0,
            "gross_loss": 0.0,
            "profit_factor": 0.0,
            "expectancy": 0.0,
            "win_rate_percent": 0.0,
            "average_win": 0.0,
            "average_loss": 0.0,
            "payoff_ratio": 0.0,
            "max_drawdown": 0.0,
            "proxy_dd_percent_on_10000": 0.0,
            "recovery_factor": 0.0,
            "max_consecutive_loss": 0,
        }
    gross_profit = float(profits[profits > 0].sum())
    gross_loss = float(-profits[profits < 0].sum())
    net_profit = float(profits.sum())
    equity = np.cumsum(profits)
    peak = np.maximum.accumulate(np.r_[0.0, equity])
    drawdowns = peak[1:] - equity
    max_drawdown = float(drawdowns.max()) if len(drawdowns) else 0.0
    days = max((pd.to_datetime(times.max()) - pd.to_datetime(times.min())).days, 1) if len(times) else 1
    wins = profits[profits > 0]
    losses = profits[profits < 0]
    avg_win = float(wins.mean()) if len(wins) else 0.0
    avg_loss = float(losses.mean()) if len(losses) else 0.0
    max_consecutive_loss = 0
    current_loss = 0
    for value in profits:
        if value < 0:
            current_loss += 1
            max_consecutive_loss = max(max_consecutive_loss, current_loss)
        else:
            current_loss = 0
    return {
        "trade_count": int(len(profits)),
        "trades_per_day": float(len(profits) / days),
        "net_profit": net_profit,
        "gross_profit": gross_profit,
        "gross_loss": gross_loss,
        "profit_factor": gross_profit / gross_loss if gross_loss > 0 else 99.0,
        "expectancy": net_profit / len(profits),
        "win_rate_percent": float((profits > 0).mean() * 100.0),
        "average_win": avg_win,
        "average_loss": avg_loss,
        "payoff_ratio": abs(avg_win / avg_loss) if avg_loss < 0 else 99.0,
        "max_drawdown": max_drawdown,
        "proxy_dd_percent_on_10000": max_drawdown / 10000.0 * 100.0,
        "recovery_factor": net_profit / max_drawdown if max_drawdown > 0 else 99.0,
        "max_consecutive_loss": int(max_consecutive_loss),
    }


def density_read(trades_per_day: float) -> str:
    if 5.0 <= float(trades_per_day) <= 10.0:
        return "inside_goal_band(목표대역안)"
    if float(trades_per_day) < 5.0:
        return "below_goal_band(목표대역미만)"
    return "above_goal_band(목표대역초과)"


def four_axis_distance(metrics: Mapping[str, Any]) -> float:
    tpd = float(metrics["trades_per_day"])
    pf = float(metrics["profit_factor"])
    dd = float(metrics["proxy_dd_percent_on_10000"])
    recovery = float(metrics["recovery_factor"])
    net = float(metrics["net_profit"])
    density_score = 1.0 if 5.0 <= tpd <= 10.0 else max(0.0, 1.0 - min(abs(tpd - 7.5) / 7.5, 1.0))
    pf_score = min(max(pf, 0.0) / 2.0, 1.5)
    dd_score = max(0.0, 1.0 - max(dd - 10.0, 0.0) / 20.0)
    recovery_score = max(0.0, min(recovery / 3.0, 1.0)) if net > 0 else 0.0
    return float(0.30 * density_score + 0.30 * pf_score + 0.20 * dd_score + 0.20 * recovery_score)


def candidate_summary(kpi_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, dict[str, Mapping[str, Any]]] = {}
    for row in kpi_rows:
        grouped.setdefault(str(row["candidate_id"]), {})[str(row["split"])] = row
    summaries: list[dict[str, Any]] = []
    for candidate_id, split_rows in grouped.items():
        val = split_rows.get("validation", {})
        oos = split_rows.get("oos", {})
        if not val or not oos:
            continue
        score = min(float(val.get("four_axis_distance_score", 0.0)), float(oos.get("four_axis_distance_score", 0.0)))
        dual_positive = float(val.get("net_profit_proxy_points", 0.0)) > 0 and float(oos.get("net_profit_proxy_points", 0.0)) > 0
        density_ok = str(val.get("density_band_read", "")).startswith("inside") and str(oos.get("density_band_read", "")).startswith("inside")
        pf_floor = min(float(val.get("profit_factor", 0.0)), float(oos.get("profit_factor", 0.0)))
        max_dd = max(
            float(val.get("proxy_dd_percent_on_10000_points", 0.0)),
            float(oos.get("proxy_dd_percent_on_10000_points", 0.0)),
        )
        summaries.append(
            {
                "candidate_id": candidate_id,
                "target_id": val.get("target_id", ""),
                "feature_set_id": val.get("feature_set_id", ""),
                "model_id": val.get("model_id", ""),
                "threshold_quantile": val.get("threshold_quantile", ""),
                "cooldown_bars": val.get("cooldown_bars", ""),
                "side_policy": val.get("side_policy", ""),
                "exit_mode": val.get("exit_mode", ""),
                "validation_net": val.get("net_profit_proxy_points", ""),
                "validation_pf": val.get("profit_factor", ""),
                "validation_tpd": val.get("trades_per_day", ""),
                "validation_dd_pct_proxy": val.get("proxy_dd_percent_on_10000_points", ""),
                "oos_net": oos.get("net_profit_proxy_points", ""),
                "oos_pf": oos.get("profit_factor", ""),
                "oos_tpd": oos.get("trades_per_day", ""),
                "oos_dd_pct_proxy": oos.get("proxy_dd_percent_on_10000_points", ""),
                "min_four_axis_distance_score": score,
                "dual_positive_proxy": dual_positive,
                "density_inside_both": density_ok,
                "min_pf": pf_floor,
                "max_validation_oos_dd_pct_proxy": max_dd,
                "summary_read": summary_read(dual_positive, density_ok, pf_floor, score),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    summaries.sort(
        key=lambda row: (
            candidate_priority(row),
            bool(row["dual_positive_proxy"]),
            bool(row["density_inside_both"]),
            float(row["min_four_axis_distance_score"]),
            float(row["min_pf"]),
            float(row["oos_net"]),
        ),
        reverse=True,
    )
    return summaries


def candidate_priority(row: Mapping[str, Any]) -> int:
    read = str(row.get("summary_read", ""))
    if read.startswith("meaningful_proxy_signal_density_band"):
        return 50
    if read.startswith("scout_clue_density_band"):
        return 40
    if read.startswith("meaningful_proxy_signal_pf_clue"):
        return 30
    if read.startswith("scout_clue_near_four_axis"):
        return 20
    if read.startswith("weak_proxy_clue"):
        return 10
    return 0


def summary_read(dual_positive: bool, density_ok: bool, pf_floor: float, score: float) -> str:
    if dual_positive and density_ok and pf_floor >= 1.05:
        return "meaningful_proxy_signal_density_band(의미있는_프록시신호_밀도대역)"
    if dual_positive and density_ok:
        return "scout_clue_density_band_pf_weak(밀도대역_PF약함_탐색단서)"
    if dual_positive and pf_floor >= 1.25:
        return "meaningful_proxy_signal_pf_clue_density_gap(의미있는_프록시신호_PF단서_밀도간극)"
    if dual_positive and score >= 0.70:
        return "scout_clue_near_four_axis_proxy(네축근접_탐색단서)"
    if dual_positive:
        return "weak_proxy_clue_dual_positive(약한_프록시단서_양쪽양수)"
    return "no_forward_proxy_candidate(전진_프록시후보없음)"


def is_density_clue(row: Mapping[str, Any]) -> bool:
    return bool(row.get("dual_positive_proxy")) and bool(row.get("density_inside_both"))


def is_pf_clue(row: Mapping[str, Any]) -> bool:
    return bool(row.get("dual_positive_proxy")) and float(row.get("min_pf", 0.0)) >= 1.25 and not bool(row.get("density_inside_both"))


def is_proxy_goal_joint(row: Mapping[str, Any]) -> bool:
    return (
        bool(row.get("dual_positive_proxy"))
        and bool(row.get("density_inside_both"))
        and float(row.get("min_pf", 0.0)) >= 2.0
        and float(row.get("max_validation_oos_dd_pct_proxy", 99.0)) <= 10.0
    )


def rank_density_clue(row: Mapping[str, Any]) -> tuple[float, float, float, float]:
    return (
        float(row.get("min_four_axis_distance_score", 0.0)),
        float(row.get("min_pf", 0.0)),
        -float(row.get("max_validation_oos_dd_pct_proxy", 99.0)),
        float(row.get("oos_net", 0.0)),
    )


def rank_pf_clue(row: Mapping[str, Any]) -> tuple[float, float, float]:
    return (
        float(row.get("min_pf", 0.0)),
        float(row.get("min_four_axis_distance_score", 0.0)),
        float(row.get("oos_net", 0.0)),
    )


def candidate_group_stats(summaries: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    density_clues = [row for row in summaries if is_density_clue(row)]
    pf_clues = [row for row in summaries if is_pf_clue(row)]
    strict_density = [
        row
        for row in density_clues
        if str(row.get("summary_read", "")).startswith("meaningful_proxy_signal_density_band")
    ]
    density_and_dd = [
        row
        for row in density_clues
        if float(row.get("max_validation_oos_dd_pct_proxy", 99.0)) <= 10.0
    ]
    joint_proxy = [row for row in summaries if is_proxy_goal_joint(row)]
    density_sorted = sorted(density_clues, key=rank_density_clue, reverse=True)
    pf_sorted = sorted(pf_clues, key=rank_pf_clue, reverse=True)
    low_dd_density_sorted = sorted(
        density_and_dd,
        key=lambda row: (
            -float(row.get("max_validation_oos_dd_pct_proxy", 99.0)),
            float(row.get("min_pf", 0.0)),
            float(row.get("min_four_axis_distance_score", 0.0)),
        ),
        reverse=True,
    )
    return {
        "density_band_dual_positive_count": len(density_clues),
        "density_band_strict_pf_count": len(strict_density),
        "density_band_and_proxy_dd_under_10_count": len(density_and_dd),
        "pf_clue_density_gap_count": len(pf_clues),
        "proxy_goal_joint_pass_count": len(joint_proxy),
        "best_density_clue": density_sorted[0] if density_sorted else {},
        "best_pf_clue": pf_sorted[0] if pf_sorted else {},
        "best_low_dd_density_clue": low_dd_density_sorted[0] if low_dd_density_sorted else {},
    }


def compact_review_summaries(summaries: Sequence[Mapping[str, Any]], top: Sequence[Mapping[str, Any]]) -> list[Mapping[str, Any]]:
    stats = candidate_group_stats(summaries)
    selected: dict[str, Mapping[str, Any]] = {}

    def add_rows(rows: Sequence[Mapping[str, Any]]) -> None:
        for row in rows:
            selected.setdefault(str(row.get("candidate_id", "")), row)

    add_rows(top)
    add_rows([row for row in summaries if is_density_clue(row)][:250])
    add_rows([row for row in summaries if is_pf_clue(row)][:250])
    add_rows([row for row in summaries if str(row.get("summary_read", "")).startswith("scout_clue_near_four_axis")][:250])
    for key in ("best_density_clue", "best_pf_clue", "best_low_dd_density_clue"):
        row = stats.get(key)
        if row:
            selected.setdefault(str(row.get("candidate_id", "")), row)
    return list(selected.values())


def run_broad_sweep(created_at: str) -> dict[str, Any]:
    model_input_raw, raw, raw_positions = load_frames()
    model_input = model_input_with_spread(model_input_raw, raw)
    labels: list[dict[str, Any]] = []
    all_kpi_rows: list[dict[str, Any]] = []
    all_trade_rows: list[dict[str, Any]] = []
    eval_grid = eval_specs()
    fsets = feature_sets(model_input)
    models = model_specs()
    targets = target_specs()
    for target in targets:
        frame = future_path_payload(model_input, raw, raw_positions, target)
        for fset in fsets:
            for model in models:
                kpi_rows, trade_rows, label_payload = train_eval_surface(frame, fset, model, target, eval_grid)
                all_kpi_rows.extend(kpi_rows)
                labels.append(label_payload)
    summaries = candidate_summary(all_kpi_rows)
    top = summaries[:25]
    meaningful = [row for row in summaries if str(row["summary_read"]).startswith("meaningful_proxy_signal")]
    all_trade_rows = top_trade_rows_for_summaries(top[:5], model_input, raw, raw_positions)
    group_stats = candidate_group_stats(summaries)
    artifact_paths = write_outputs(created_at, model_input, all_kpi_rows, summaries, top, all_trade_rows, labels, group_stats)
    return {
        "created_at_utc": created_at,
        "kpi_rows": all_kpi_rows,
        "candidate_summaries": summaries,
        "top_candidates": top,
        "meaningful_candidates": meaningful,
        "candidate_group_stats": group_stats,
        "label_payloads": labels,
        "artifact_paths": artifact_paths,
        "input_rows": int(len(model_input)),
        "feature_count": len([col for col in model_input.columns if col not in FEATURE_EXCLUDE and col != "spread_points_proxy"]),
    }


def top_trade_rows_for_summaries(
    top: Sequence[Mapping[str, Any]],
    model_input: pd.DataFrame,
    raw: pd.DataFrame,
    raw_positions: np.ndarray,
) -> list[dict[str, Any]]:
    if not top:
        return []
    targets = {spec.target_id: spec for spec in target_specs()}
    fsets = {spec.feature_set_id: spec for spec in feature_sets(model_input)}
    models = {spec.model_id: spec for spec in model_specs()}
    rows: list[dict[str, Any]] = []
    for summary in top:
        target = targets[str(summary["target_id"])]
        fset = fsets[str(summary["feature_set_id"])]
        model = models[str(summary["model_id"])]
        frame = future_path_payload(model_input, raw, raw_positions, target)
        train_mask = frame["split"].eq("train")
        oos_mask = frame["split"].eq("oos")
        estimator = model.estimator
        estimator.fit(frame.loc[train_mask, list(fset.columns)], frame.loc[train_mask, "target_class"])
        classes = list(getattr(estimator, "classes_", getattr(estimator[-1], "classes_", [])))
        _, train_edge = side_and_edge(estimator.predict_proba(frame.loc[train_mask, list(fset.columns)]), classes)
        train_edges = train_edge[train_edge > -100.0]
        if len(train_edges) == 0:
            continue
        threshold = float(np.quantile(train_edges, float(summary["threshold_quantile"])))
        split_frame = frame.loc[oos_mask].copy().reset_index(drop=True)
        side, edge = side_and_edge(estimator.predict_proba(split_frame.loc[:, list(fset.columns)]), classes)
        side = apply_side_policy(side, str(summary["side_policy"]))
        signal = (side != 1) & (edge >= threshold)
        profit = profit_for_side(split_frame, side, str(summary["exit_mode"]))
        chosen = non_overlap_indices(signal, int(target.horizon_bars), int(summary["cooldown_bars"]))
        for order, idx in enumerate(chosen[:150]):
            rows.append(
                {
                    "candidate_id": summary["candidate_id"],
                    "rank_order_within_candidate": order,
                    "timestamp": str(split_frame.loc[idx, "timestamp"]),
                    "side": "long(롱)" if side[idx] == 2 else "short(숏)",
                    "edge": float(edge[idx]),
                    "profit_proxy_points": float(profit[idx]),
                    "entry_close": float(split_frame.loc[idx, "entry_close"]),
                    "future_close": float(split_frame.loc[idx, "future_close"]),
                    "long_mae_points": float(split_frame.loc[idx, "long_mae_points"]),
                    "short_mae_points": float(split_frame.loc[idx, "short_mae_points"]),
                    "split": "oos(표본외)",
                    "row_audit_scope": "top5_candidates_first150_oos_trades(상위5후보_표본외_앞150거래)",
                }
            )
    return rows


def write_outputs(
    created_at: str,
    model_input: pd.DataFrame,
    kpi_rows: Sequence[Mapping[str, Any]],
    summaries: Sequence[Mapping[str, Any]],
    top: Sequence[Mapping[str, Any]],
    trade_rows: Sequence[Mapping[str, Any]],
    labels: Sequence[Mapping[str, Any]],
    group_stats: Mapping[str, Any],
) -> list[str]:
    io_path(RUN_ROOT / "reports").mkdir(parents=True, exist_ok=True)
    io_path(REVIEWS_ROOT).mkdir(parents=True, exist_ok=True)
    kpi_path = RUN_ROOT / "f68b_proxy_kpi_by_split.csv"
    summary_path = RUN_ROOT / "f68b_proxy_candidate_summary.csv"
    top_path = RUN_ROOT / "f68b_top_candidates.json"
    trade_path = RUN_ROOT / "f68b_top_candidate_oos_trade_rows.csv"
    label_path = RUN_ROOT / "f68b_label_distribution.json"
    report_path = RUN_ROOT / "reports" / "result_summary.md"
    review_report = REVIEWS_ROOT / "frontier68B_proxy_broad_sweep_report.md"
    review_kpi = REVIEWS_ROOT / "f68b_proxy_kpi_by_split_review.csv"
    review_summary = REVIEWS_ROOT / "f68b_proxy_candidate_summary_review.csv"
    review_top = REVIEWS_ROOT / "f68b_top_candidates_review.json"
    review_trade = REVIEWS_ROOT / "f68b_top_candidate_oos_trade_rows_review.csv"
    review_label = REVIEWS_ROOT / "f68b_label_distribution_review.json"

    write_csv(kpi_path, kpi_rows)
    write_csv(summary_path, summaries)
    write_json(
        top_path,
        {
            "run_id": RUN_ID,
            "top_candidates": top,
            "candidate_group_stats": group_stats,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_csv(trade_path, trade_rows)
    write_json(label_path, {"run_id": RUN_ID, "label_payloads": labels, "claim_boundary": CLAIM_BOUNDARY})
    write_md(report_path, build_report(created_at, model_input, summaries, top, labels, group_stats))

    review_summaries = compact_review_summaries(summaries, top)
    review_candidate_ids = {str(row["candidate_id"]) for row in review_summaries}
    review_kpi_rows = [row for row in kpi_rows if str(row.get("candidate_id", "")) in review_candidate_ids]
    write_csv(review_kpi, review_kpi_rows)
    write_csv(review_summary, review_summaries)
    write_json(
        review_top,
        {
            "run_id": RUN_ID,
            "top_candidates": top,
            "candidate_group_stats": group_stats,
            "review_candidate_count": len(review_summaries),
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_csv(review_trade, trade_rows)
    write_json(review_label, {"run_id": RUN_ID, "label_payloads": labels, "claim_boundary": CLAIM_BOUNDARY})
    write_md(review_report, build_report(created_at, model_input, summaries, top, labels, group_stats))

    full_artifacts = [
        artifact_identity(kpi_path, len(kpi_rows)),
        artifact_identity(summary_path, len(summaries)),
        artifact_identity(top_path, len(top)),
        artifact_identity(trade_path, len(trade_rows)),
        artifact_identity(label_path, len(labels)),
        artifact_identity(report_path, None),
    ]
    review_artifacts = [
        artifact_identity(review_kpi, len(review_kpi_rows)),
        artifact_identity(review_summary, len(review_summaries)),
        artifact_identity(review_top, len(top)),
        artifact_identity(review_trade, len(trade_rows)),
        artifact_identity(review_label, len(labels)),
        artifact_identity(review_report, None),
    ]

    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": created_at,
        "status": "completed_proxy_broad_sweep_no_authority(프록시 넓은 탐색 완료, 권위 없음)",
        "claim_boundary": CLAIM_BOUNDARY,
        "producer": "stage_pipelines/stage_frontier_68/frontier68b_runtime_lifecycle_proxy_broad_sweep.py",
        "source_inputs": [
            rel(MODEL_INPUT),
            rel(RAW_US100),
            rel(F68A_LABEL_DESIGN),
        ],
        "artifacts": [
            rel(kpi_path),
            rel(summary_path),
            rel(top_path),
            rel(trade_path),
            rel(label_path),
            rel(report_path),
            rel(review_report),
        ],
        "full_artifact_identities": full_artifacts,
        "review_artifact_identities": review_artifacts,
        "review_compaction": {
            "review_summary_rows": len(review_summaries),
            "review_kpi_rows": len(review_kpi_rows),
            "reason": "full CSV artifacts stay under 02_runs; 03_reviews carries compact review rows(전체 CSV는 02_runs에 두고 03_reviews는 압축 검토 행만 보관)",
        },
        "next_run_id": NEXT_RUN_ID,
    }
    write_json(RUN_ROOT / "run_manifest.json", manifest)
    return [rel(path) for path in [kpi_path, summary_path, top_path, trade_path, label_path, report_path, review_report, review_summary, review_kpi]]


def artifact_identity(path: Path, rows: int | None) -> dict[str, Any]:
    stat = io_path(path).stat()
    return {
        "path": rel(path),
        "sha256": sha256_file(path),
        "bytes": int(stat.st_size),
        "rows": rows,
    }


def candidate_report_lines(title: str, row: Mapping[str, Any]) -> list[str]:
    if not row:
        return [f"## {title}", "", "- candidate(후보): `none(없음)`.", ""]
    return [
        f"## {title}",
        "",
        f"- candidate_id(후보 ID): `{row.get('candidate_id', 'none')}`.",
        f"- target(목표): `{row.get('target_id', '')}`.",
        f"- feature/model(피처/모델): `{row.get('feature_set_id', '')}` / `{row.get('model_id', '')}`.",
        f"- threshold/cooldown/side/exit(임계값/대기봉/방향/청산): `{fmt(row.get('threshold_quantile'))}/{row.get('cooldown_bars', '')}/{row.get('side_policy', '')}/{row.get('exit_mode', '')}`.",
        f"- validation net/PF/trades_day/proxy_DD%(검증 순수익/수익 팩터/일 거래/프록시 손실폭%): `{fmt(row.get('validation_net'))}/{fmt(row.get('validation_pf'))}/{fmt(row.get('validation_tpd'))}/{fmt(row.get('validation_dd_pct_proxy'))}`.",
        f"- OOS net/PF/trades_day/proxy_DD%(표본외 순수익/수익 팩터/일 거래/프록시 손실폭%): `{fmt(row.get('oos_net'))}/{fmt(row.get('oos_pf'))}/{fmt(row.get('oos_tpd'))}/{fmt(row.get('oos_dd_pct_proxy'))}`.",
        f"- min PF/max proxy DD%(최소 수익 팩터/최대 프록시 손실폭%): `{fmt(row.get('min_pf'))}/{fmt(row.get('max_validation_oos_dd_pct_proxy'))}`.",
        f"- read(판독): `{row.get('summary_read', '')}`.",
        "",
    ]


def build_report(
    created_at: str,
    model_input: pd.DataFrame,
    summaries: Sequence[Mapping[str, Any]],
    top: Sequence[Mapping[str, Any]],
    labels: Sequence[Mapping[str, Any]],
    group_stats: Mapping[str, Any],
) -> list[str]:
    meaningful_count = sum(1 for row in summaries if str(row["summary_read"]).startswith("meaningful_proxy_signal"))
    label_variants = len({payload["target_id"] for payload in labels})
    best_density = group_stats.get("best_density_clue", {})
    best_pf = group_stats.get("best_pf_clue", {})
    best_low_dd_density = group_stats.get("best_low_dd_density_clue", {})
    best_density_aware = top[0] if top else {}
    lines = [
        "# F68B Runtime Lifecycle Proxy Broad Sweep(F68B 런타임 생명주기 프록시 넓은 탐색)",
        "",
        f"Updated(갱신): {created_at}",
        "",
        "## Action And Effect(행동 및 효과)",
        "",
        "Action(행동): raw US100 M5 bars(원천 US100 5분봉)에서 forward path(전방 경로), MFE/MAE(최대 유리/불리 이동), cost proxy(비용 프록시), ATR first-hit(평균진폭 선타격)을 계산하고, feature set/label/model/trade shape/risk(피처 묶음/라벨/모델/거래 형태/위험) 조합을 넓게 시험했다.",
        "",
        "Effect(효과): F68이 alignment-only(정렬 전용) 단계로 좁아지지 않고, 실제 nonzero proxy signal(영이 아닌 프록시 신호)과 four-axis distance(네 축 목표까지 거리)를 가진 scout surface(탐색 표면)를 얻었다.",
        "",
        "## Measurement Scope(측정 범위)",
        "",
        f"- input rows(입력 행): `{len(model_input)}`.",
        f"- label variants(라벨 변형): `{label_variants}`.",
        f"- candidate summaries(후보 요약): `{len(summaries)}`.",
        f"- meaningful PF/density signal candidates(의미 있는 수익 팩터/밀도 신호 후보): `{meaningful_count}`.",
        f"- density-band dual-positive clues(밀도대역 양쪽 양수 단서): `{group_stats.get('density_band_dual_positive_count', 0)}`.",
        f"- density-band strict PF clues(밀도대역 엄격 수익 팩터 단서): `{group_stats.get('density_band_strict_pf_count', 0)}`.",
        f"- density-band plus proxy DD under 10 clues(밀도대역 및 프록시 손실폭 10 미만 단서): `{group_stats.get('density_band_and_proxy_dd_under_10_count', 0)}`.",
        f"- PF clue with density gap candidates(밀도 간극이 있는 수익 팩터 단서 후보): `{group_stats.get('pf_clue_density_gap_count', 0)}`.",
        f"- proxy joint pass count(프록시 네 축 동시 통과 수): `{group_stats.get('proxy_goal_joint_pass_count', 0)}`.",
        "- scoreboard(점수판): structural_scout(구조 탐색) and proxy trading read(프록시 거래 판독).",
        "- parity level(동등성 수준): P1_dataset_feature_aligned(P1 데이터셋/피처 정렬); MT5 runtime parity(MT5 런타임 동등성)는 아직 아님.",
        "",
    ]
    lines.extend(candidate_report_lines("Best Density-Aware Proxy Clue(최선 밀도 고려 프록시 단서)", best_density_aware))
    lines.extend(candidate_report_lines("Best Density Clue(최선 밀도 단서)", best_density))
    lines.extend(candidate_report_lines("Best Low-DD Density Clue(최선 저손실폭 밀도 단서)", best_low_dd_density))
    lines.extend(candidate_report_lines("Best PF Clue With Density Gap(최선 수익 팩터 단서와 밀도 간극)", best_pf))
    lines.extend(
        [
            "## Gap Read(간극 판독)",
            "",
            "- Four-axis proxy completion candidate(네 축 프록시 완성 후보): `none(없음)`.",
            "- Plain meaning(쉬운 뜻): density clues(밀도 단서)는 거래 수가 맞지만 PF(수익 팩터)가 약하고, PF clues(수익 팩터 단서)는 거래 수가 너무 적다.",
            "- Effect(효과): F68C는 한 후보만 밀지 말고 density repair(밀도 수리)와 PF repair(수익 팩터 수리)를 같이 비교해야 한다.",
            "",
        ]
    )
    lines.extend(
        [
        "## Boundary(경계)",
        "",
        "- This is proxy-only(프록시 전용) evidence(근거)다. MT5 Runtime Probe(MT5 런타임 탐침), Strategy Tester(전략 테스터), ONNX handoff(ONNX 인계)는 아직 실행하지 않았다.",
        "- Proxy DD%(프록시 손실폭 %)는 10000 proxy points(프록시 포인트) 기준 정규화 수치이며 account DD(계좌 손실폭) 권위가 아니다.",
        "- Next action(다음 행동): pre-MT5 Grok review(그록 사전 검토) 전 후보를 줄이고, 필요하면 ONNX scout export(ONNX 탐색 내보내기)를 준비한다.",
        "",
        f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        ]
    )
    return lines


def update_ledgers_and_state(created_at: str, result: Mapping[str, Any]) -> None:
    summaries = list(result["candidate_summaries"])
    meaningful = list(result["meaningful_candidates"])
    top = list(result["top_candidates"])
    group_stats = dict(result.get("candidate_group_stats", {}))
    best = top[0] if top else {}
    best_density = group_stats.get("best_density_clue", {}) or {}
    best_pf = group_stats.get("best_pf_clue", {}) or {}
    density_count = int(group_stats.get("density_band_dual_positive_count", 0))
    pf_gap_count = int(group_stats.get("pf_clue_density_gap_count", 0))
    joint_pass_count = int(group_stats.get("proxy_goal_joint_pass_count", 0))
    status = "completed_proxy_broad_sweep_no_authority(프록시 넓은 탐색 완료, 권위 없음)"
    judgment = (
        "proxy_clues_found_axes_split_no_runtime_authority(프록시 단서 발견, 축 분리, 런타임 권위 없음)"
        if meaningful or density_count
        else "proxy_broad_sweep_no_meaningful_signal_yet(프록시 넓은 탐색, 의미 있는 신호 아직 없음)"
    )
    row = {
        "ledger_row_id": f"{RUN_ID}__proxy_broad_sweep",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "proxy_broad_sweep(프록시 넓은 탐색)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "proxy_broad_sweep(프록시 넓은 탐색)",
        "tier_scope": "Tier A+B planned(티어 A+B 계획)",
        "kpi_scope": "proxy_trading_and_four_axis_distance(프록시 거래 및 네 축 거리)",
        "scoreboard_lane": "structural_scout(구조 탐색)",
        "status": status,
        "judgment": judgment,
        "path": f"stages/{STAGE_ID}/03_reviews/frontier68B_proxy_broad_sweep_report.md",
        "primary_kpi": (
            f"best_density_aware={best.get('candidate_id', 'none')};"
            f"best_density_clue={best_density.get('candidate_id', 'none')};"
            f"best_pf_clue={best_pf.get('candidate_id', 'none')};"
            f"density_clues={density_count};pf_gap_clues={pf_gap_count};"
            f"proxy_joint_pass={joint_pass_count}"
        ),
        "guardrail_kpi": "runtime_probe_pending;proxy_dd_is_normalized_not_account_authority(런타임 탐침 대기, 프록시 손실폭은 계좌 권위 아님)",
        "external_verification_status": "out_of_scope_by_claim_proxy_only(프록시 주장 범위 밖)",
        "notes": "F68B completed broad proxy sweep across labels/features/models/trade shapes/risk; density and PF clues split; no runtime authority claimed.",
        "hcardrail_kpi": "runtime_probe_pending;proxy_only",
        "run_number": "frontier68B",
        "date": "2026-06-17",
        "decision": "proceed_to_f68c_candidate_scoring_or_onnx_scout_export",
        "next_run_id": NEXT_RUN_ID,
        "rows": len(summaries),
        "gate_passes": 5,
        "gate_total": 5,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": f"stages/{STAGE_ID}/03_reviews/frontier68B_proxy_broad_sweep_report.md",
        "trained_models": len(target_specs()) * len(feature_sets(pd.read_parquet(io_path(MODEL_INPUT)).head(1))) * len(model_specs()),
        "onnx_parity": "not_applicable_no_export_yet(아직 내보내기 없음)",
        "best_proxy": best.get("candidate_id", ""),
        "candidate_rows": len(summaries),
        "positive_proxy_rows": len(meaningful),
        "best_model_id": best.get("model_id", ""),
        "best_proxy_net": fmt(best.get("oos_net")),
        "run_date": "2026-06-17",
        "primary_artifact": f"stages/{STAGE_ID}/02_runs/{RUN_ID}/f68b_proxy_candidate_summary.csv",
        "view": "proxy_broad_sweep(프록시 넓은 탐색)",
        "tier": "Tier A+B planned(티어 A+B 계획)",
        "metric_scope": "validation_oos_proxy(검증/표본외 프록시)",
        "net_profit": fmt(best.get("oos_net")),
        "profit_factor": fmt(best.get("oos_pf")),
        "expectancy": "",
        "drawdown": fmt(best.get("oos_dd_pct_proxy")),
        "recovery_factor": "",
        "trade_count": "",
        "result_status": status,
        "feature_count": result.get("feature_count", ""),
        "lane": "proxy_broad_sweep(프록시 넓은 탐색)",
        "family": "experiment_execution(실험 실행)",
        "primary_report": f"stages/{STAGE_ID}/03_reviews/frontier68B_proxy_broad_sweep_report.md",
        "sample_rows": result.get("input_rows", ""),
        "attempt_count": len(summaries),
        "source_package_run_id": PARENT_RUN_ID,
        "row_id": f"{RUN_ID}__proxy_broad_sweep",
        "scoreboard": "structural_scout(구조 탐색)",
        "evidence_boundary": "proxy_only_no_runtime_authority(프록시 전용, 런타임 권위 없음)",
        "work_family": "experiment_execution(실험 실행)",
        "evidence_scope": "proxy_broad_sweep(프록시 넓은 탐색)",
        "run_key": RUN_ID,
        "question": "Can lifecycle path labels produce meaningful proxy signals?(생명주기 경로 라벨이 의미 있는 프록시 신호를 만들 수 있는가)",
        "next_action": NEXT_RUN_ID,
        "result_judgment": judgment,
        "final_decision_path": f"stages/{STAGE_ID}/03_reviews/frontier68B_proxy_broad_sweep_report.md",
        "created_at": created_at,
        "gate_audit_path": f"stages/{STAGE_ID}/02_runs/{RUN_ID}/run_manifest.json",
        "artifact_count": len(result.get("artifact_paths", [])),
        "created_at_utc": created_at,
        "required_gate_audit": "proxy_broad_sweep_artifacts_and_claim_boundary_recorded(프록시 넓은 탐색 산출물 및 주장 경계 기록)",
        "kpi_summary": (
            f"candidate_summaries={len(summaries)};meaningful_proxy_candidates={len(meaningful)};"
            f"density_clues={density_count};pf_gap_clues={pf_gap_count};"
            f"proxy_joint_pass={joint_pass_count};best_density_aware={best.get('candidate_id', 'none')}"
        ),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "trade_density": fmt(best.get("oos_tpd")),
        "source_authority": "proxy_only_no_runtime(프록시 전용, 런타임 없음)",
        "goal_achieve": "not_claimed",
        "run_family": "frontier_proxy_broad_sweep(전선 프록시 넓은 탐색)",
        "run_type": "proxy_broad_sweep(프록시 넓은 탐색)",
        "input_run_id": PARENT_RUN_ID,
        "output_path": f"stages/{STAGE_ID}/02_runs/{RUN_ID}/f68b_proxy_candidate_summary.csv",
        "result_path": f"stages/{STAGE_ID}/03_reviews/frontier68B_proxy_broad_sweep_report.md",
        "strict_joint_pass_count": joint_pass_count,
    }
    upsert_ledger(REVIEWS_ROOT / "stage_run_ledger.csv", "ledger_row_id", row)
    upsert_ledger(ROOT / "docs/registers/alpha_run_ledger.csv", "ledger_row_id", row)
    upsert_ledger(ROOT / "docs/registers/run_registry.csv", "run_id", row)
    update_review_index()
    update_current_state(created_at, status, judgment, best, best_density, best_pf, len(meaningful), group_stats)


def update_review_index() -> None:
    lines = [
        "# F68 Review Index(F68 검토 색인)",
        "",
        "- `../00_spec/stage_brief.md`: F68 stage brief(F68 단계 개요)",
        "- `runA_report.md`: F68A stage open report(F68A 단계 개방 보고서)",
        "- `grok_stage_open_receipt.md`: F68 Grok stage-open receipt(F68 그록 단계 개방 영수증)",
        "- `stage_run_ledger.csv`: F68 stage-local run ledger(F68 단계 로컬 실행 장부)",
        "- `frontier68A_bridge_feasibility_and_label_design_report.md`: F68A bridge feasibility and label design report(F68A 연결 가능성 및 라벨 설계 보고서)",
        "- `f68a_input_inventory_review.csv`: F68A input inventory(F68A 입력 목록)",
        "- `f68a_bridge_feasibility_checklist_review.json`: F68A bridge feasibility checklist(F68A 연결 가능성 체크리스트)",
        "- `f68a_lifecycle_label_design_review.json`: F68A lifecycle label design(F68A 생명주기 라벨 설계)",
        "- `frontier68B_proxy_broad_sweep_report.md`: F68B proxy broad sweep report(F68B 프록시 넓은 탐색 보고서)",
        "- `f68b_proxy_candidate_summary_review.csv`: F68B candidate summary(F68B 후보 요약)",
        "- `f68b_proxy_kpi_by_split_review.csv`: F68B split KPI(F68B 분할 핵심 성과 지표)",
        "- `f68b_top_candidates_review.json`: F68B top candidates(F68B 상위 후보)",
        "",
        "Current status(현재 상태): `f68b_proxy_broad_sweep_completed_no_authority(F68B 프록시 넓은 탐색 완료, 권위 없음)`",
        f"Next action(다음 행동): `{NEXT_RUN_ID}`",
    ]
    write_md(REVIEWS_ROOT / "review_index.md", lines)


def update_current_state(
    created_at: str,
    status: str,
    judgment: str,
    best: Mapping[str, Any],
    best_density: Mapping[str, Any],
    best_pf: Mapping[str, Any],
    meaningful_count: int,
    group_stats: Mapping[str, Any],
) -> None:
    density_count = int(group_stats.get("density_band_dual_positive_count", 0))
    pf_gap_count = int(group_stats.get("pf_clue_density_gap_count", 0))
    joint_pass_count = int(group_stats.get("proxy_goal_joint_pass_count", 0))
    selection = [
        "# F68 Selection Status(F68 선택 상태)",
        "",
        f"- stage(단계): `{STAGE_ID}`",
        f"- current_run(현재 실행): `{NEXT_RUN_ID}`",
        f"- latest_completed_run(최근 완료 실행): `{RUN_ID}`",
        f"- status(상태): `{status}`",
        "- selected_baseline(선택 기준선): `not_claimed(주장 없음)`",
        "- runtime_authority(런타임 권위): `not_claimed(주장 없음)`",
        "- operating_promotion(운영 승격): `not_claimed(주장 없음)`",
        "- live_readiness(실거래 준비): `not_claimed(주장 없음)`",
        "- Goal Achieve(목표 달성): `not_claimed(주장 없음)`",
        f"- completed_action(완료 행동): F68B proxy broad sweep(F68B 프록시 넓은 탐색)을 완료했고 meaningful PF/density signal candidates(의미 있는 수익 팩터/밀도 신호 후보) `{meaningful_count}`개와 density clues(밀도 단서) `{density_count}`개를 기록했다.",
        f"- best_density_aware_clue(최선 밀도 고려 단서): `{best.get('candidate_id', 'none')}`.",
        f"- best_pf_gap_clue(최선 수익 팩터 간극 단서): `{best_pf.get('candidate_id', 'none')}`.",
        f"- proxy_joint_pass_count(프록시 네 축 동시 통과 수): `{joint_pass_count}`.",
        f"- next_action(다음 행동): `{NEXT_RUN_ID}` candidate scoring or ONNX scout export(후보 점수화 또는 ONNX 탐색 내보내기).",
        "- boundary(경계): proxy-only(프록시 전용), no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).",
    ]
    write_md(STAGE_ROOT / "04_selected" / "selection_status.md", selection)

    state = [
        f"current_stage_id: {STAGE_ID}",
        f"active_stage: {STAGE_ID}",
        f"current_run_id: {NEXT_RUN_ID}",
        f"latest_completed_run_id: {RUN_ID}",
        f"current_status: {status}",
        f"current_judgment: {judgment}",
        f"next_stage_id: {STAGE_ID}",
        f"next_run_id: {NEXT_RUN_ID}",
        "runtime_probe_status: f68_mandatory_runtime_probe_pending_after_meaningful_proxy_signal_and_pre_mt5_grok_review(F68 의미 있는 프록시 신호 및 MT5 전 그록 검토 후 필수 런타임 탐침 대기)",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "live_readiness: not_claimed",
        "goal_achieve: not_claimed",
        f"updated_at_utc: '{created_at}'",
        "notes:",
        f'  - "F68B completed(완료): proxy broad sweep(프록시 넓은 탐색)에서 meaningful PF/density signal candidates(의미 있는 수익 팩터/밀도 신호 후보) `{meaningful_count}`개, density clues(밀도 단서) `{density_count}`개, PF gap clues(수익 팩터 간극 단서) `{pf_gap_count}`개를 기록했다."',
        f'  - "Best density-aware clue(최선 밀도 고려 단서): candidate(후보) `{best.get("candidate_id", "none")}`, validation/OOS PF(검증/표본외 수익 팩터) `{fmt(best.get("validation_pf"))}/{fmt(best.get("oos_pf"))}`, validation/OOS trades/day(검증/표본외 일 거래 수) `{fmt(best.get("validation_tpd"))}/{fmt(best.get("oos_tpd"))}`."',
        f'  - "Best PF gap clue(최선 수익 팩터 간극 단서): candidate(후보) `{best_pf.get("candidate_id", "none")}`, validation/OOS PF(검증/표본외 수익 팩터) `{fmt(best_pf.get("validation_pf"))}/{fmt(best_pf.get("oos_pf"))}`, validation/OOS trades/day(검증/표본외 일 거래 수) `{fmt(best_pf.get("validation_tpd"))}/{fmt(best_pf.get("oos_tpd"))}`."',
        f'  - "Proxy joint pass(프록시 네 축 동시 통과): `{joint_pass_count}`. Axis split(축 분리): density clues(밀도 단서)는 PF가 약하고, PF clues(수익 팩터 단서)는 밀도가 낮다."',
        '  - "Boundary(경계): F68B is proxy-only(프록시 전용) and does not claim MT5 runtime authority(MT5 런타임 권위), ONNX readiness(ONNX 준비), live readiness(실거래 준비), or Goal Achieve(목표 달성)."',
        f'  - "Next action(다음 행동): `{NEXT_RUN_ID}`에서 후보 축소와 ONNX scout export(ONNX 탐색 내보내기) 가능성을 검토하고 MT5 전 Grok review(그록 검토)를 준비한다."',
    ]
    io_path(ROOT / "docs/workspace/workspace_state.yaml").write_text("\n".join(state) + "\n", encoding="utf-8-sig")

    current_working_state = [
        "# Current Working State(현재 작업 상태)",
        "",
        f"Updated(갱신): {created_at}",
        "",
        f"Active stage(활성 단계): `{STAGE_ID}`",
        "",
        f"Current run(현재 실행): `{NEXT_RUN_ID}`",
        "",
        f"Latest completed run(최근 완료 실행): `{RUN_ID}`",
        "",
        "## Current Truth(현재 진실)",
        "",
        "Action(행동): F68B runtime lifecycle proxy broad sweep(F68B 런타임 생명주기 프록시 넓은 탐색)을 실행했다.",
        "",
        "Effect(효과): feature set/label/model/trade shape/risk(피처 묶음/라벨/모델/거래 형태/위험)을 한 번에 바꿔 보며, F68이 proxy/runtime alignment(프록시/런타임 정렬)만 하고 멈추지 않도록 실제 scout surface(탐색 표면)를 만들었다.",
        "",
        f"- F68B status(F68B 상태): `{status}`.",
        f"- meaningful PF/density signal candidates(의미 있는 수익 팩터/밀도 신호 후보): `{meaningful_count}`.",
        f"- density clues(밀도 단서): `{density_count}`.",
        f"- PF gap clues(수익 팩터 간극 단서): `{pf_gap_count}`.",
        f"- proxy joint pass count(프록시 네 축 동시 통과 수): `{joint_pass_count}`.",
        f"- best density-aware candidate(최선 밀도 고려 후보): `{best.get('candidate_id', 'none')}`.",
        f"- best density validation/OOS net/PF/trades_day/proxy_DD%(최선 밀도 검증/표본외 순수익/수익 팩터/일 거래/프록시 손실폭%): `{fmt(best_density.get('validation_net'))}/{fmt(best_density.get('validation_pf'))}/{fmt(best_density.get('validation_tpd'))}/{fmt(best_density.get('validation_dd_pct_proxy'))}` / `{fmt(best_density.get('oos_net'))}/{fmt(best_density.get('oos_pf'))}/{fmt(best_density.get('oos_tpd'))}/{fmt(best_density.get('oos_dd_pct_proxy'))}`.",
        f"- best PF gap validation/OOS net/PF/trades_day/proxy_DD%(최선 수익 팩터 간극 검증/표본외 순수익/수익 팩터/일 거래/프록시 손실폭%): `{fmt(best_pf.get('validation_net'))}/{fmt(best_pf.get('validation_pf'))}/{fmt(best_pf.get('validation_tpd'))}/{fmt(best_pf.get('validation_dd_pct_proxy'))}` / `{fmt(best_pf.get('oos_net'))}/{fmt(best_pf.get('oos_pf'))}/{fmt(best_pf.get('oos_tpd'))}/{fmt(best_pf.get('oos_dd_pct_proxy'))}`.",
        "- gap read(간극 판독): density clues(밀도 단서)는 PF(수익 팩터)가 약하고 PF clues(수익 팩터 단서)는 일 거래 수가 낮다.",
        "- mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침): still pending(아직 대기). F68C에서 후보를 줄이고 pre-MT5 Grok review(그록 사전 검토)를 거친 뒤 물질화한다.",
        "",
        "## Key Artifacts(핵심 산출물)",
        "",
        f"- F68B report(F68B 보고서): `stages/{STAGE_ID}/03_reviews/frontier68B_proxy_broad_sweep_report.md`",
        f"- F68B summary(F68B 요약): `stages/{STAGE_ID}/03_reviews/f68b_proxy_candidate_summary_review.csv`",
        f"- F68B KPI(F68B 핵심 성과 지표): `stages/{STAGE_ID}/03_reviews/f68b_proxy_kpi_by_split_review.csv`",
        f"- F68B top candidates(F68B 상위 후보): `stages/{STAGE_ID}/03_reviews/f68b_top_candidates_review.json`",
        "",
        f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    ]
    write_md(ROOT / "docs/context/current_working_state.md", current_working_state)


def main() -> int:
    created_at = utc_now()
    result = run_broad_sweep(created_at)
    update_ledgers_and_state(created_at, result)
    print(
        json.dumps(
            json_ready(
                {
                    "status": "completed_proxy_broad_sweep_no_authority",
                    "run_id": RUN_ID,
                    "next_run_id": NEXT_RUN_ID,
                    "candidate_summaries": len(result["candidate_summaries"]),
                    "meaningful_proxy_candidates": len(result["meaningful_candidates"]),
                    "best_candidate": (result["top_candidates"][0] if result["top_candidates"] else {}).get("candidate_id", "none"),
                    "density_band_dual_positive_count": result["candidate_group_stats"].get("density_band_dual_positive_count", 0),
                    "pf_clue_density_gap_count": result["candidate_group_stats"].get("pf_clue_density_gap_count", 0),
                    "proxy_goal_joint_pass_count": result["candidate_group_stats"].get("proxy_goal_joint_pass_count", 0),
                    "best_density_clue": result["candidate_group_stats"].get("best_density_clue", {}).get("candidate_id", "none"),
                    "best_pf_clue": result["candidate_group_stats"].get("best_pf_clue", {}).get("candidate_id", "none"),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
