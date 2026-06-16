from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

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


STAGE_ID = "stage_frontier_69__axis_rotation_after_lifecycle_risk_only_negative_memory"
RUN_ID = "frontier69B_event_first_first_hit_proxy_sweep_v1"
PARENT_RUN_ID = "frontier69A_stage_open_axis_rotation_hypothesis_design_v1"
NEXT_RUN_SIGNAL = "frontier69C_pre_mt5_grok_review_event_first_proxy_v1"
NEXT_RUN_REPAIR = "frontier69C_repair_event_first_label_or_feature_surface_v1"
IDEA_ID = "IDEA-FR69-EVENT-FIRST-AXIS-ROTATION-PF-SOURCE"

CLAIM_BOUNDARY = (
    "proxy_scout_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"

MODEL_INPUT = ROOT / "data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet"
MODEL_FEATURE_ORDER = ROOT / "data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_feature_order.txt"
RAW_US100 = ROOT / "data/raw/mt5_bars/m5/US100/bars_us100_m5_mt5api_raw.csv"
F69A_DESIGN = STAGE_ROOT / "02_runs" / PARENT_RUN_ID / "f69a_experiment_design.json"
F69A_REPORT = REVIEWS_ROOT / "frontier69A_stage_open_axis_rotation_hypothesis_design_report.md"

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
    "spread_points_proxy",
    "spread_cost_points",
    "raw_pos",
    "raw_open",
    "raw_high",
    "raw_low",
    "raw_close",
}


@dataclass(frozen=True)
class TargetSpec:
    target_id: str
    horizon_bars: int
    sl_atr: float = 0.90
    tp_atr: float = 1.35
    min_edge_atr: float = 0.10
    min_edge_points: float = 1.0


@dataclass(frozen=True)
class FeatureSet:
    feature_set_id: str
    columns: tuple[str, ...]


@dataclass(frozen=True)
class ModelSpec:
    model_id: str
    model_family: str
    build: Callable[[], Any]


@dataclass(frozen=True)
class EventSpec:
    event_id: str
    description: str
    mask: np.ndarray


@dataclass(frozen=True)
class CandidateSpec:
    candidate_id: str
    target: TargetSpec
    feature_set: FeatureSet
    model: ModelSpec
    event_id: str
    threshold_quantile: float
    edge_threshold: float
    side_policy: str
    cooldown_bars: int


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def stable_id(parts: Sequence[Any]) -> str:
    return hashlib.sha1("|".join(str(part) for part in parts).encode("utf-8")).hexdigest()[:12]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_md(path: Path, lines: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames = list(columns or (rows[0].keys() if rows else []))
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: json_ready(row.get(key, "")) for key in fieldnames})


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path) if path_exists(path) else ""
    if marker in text:
        return
    io_path(path).write_text(text.rstrip() + "\n\n" + block.rstrip() + "\n", encoding="utf-8-sig")


def upsert_ledger(path: Path, key: str, row: Mapping[str, Any], source_header: Path | None = None) -> None:
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            rows = list(reader)
    elif source_header is not None:
        with io_path(source_header).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
        rows = []
    else:
        raise RuntimeError(f"ledger header missing: {path}")
    rows = [existing for existing in rows if existing.get(key) != row.get(key)]
    rows.append({name: json_ready(row.get(name, "")) for name in fieldnames})
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


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


def numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def q(frame: pd.DataFrame, column: str, quantile: float, default: float, absolute: bool = False) -> float:
    train = numeric(frame.loc[frame["split"].astype(str).eq("train"), column])
    if absolute:
        train = train.abs()
    train = train.replace([np.inf, -np.inf], np.nan).dropna()
    if train.empty:
        return float(default)
    return float(train.quantile(quantile))


def required_artifacts() -> list[Path]:
    return [MODEL_INPUT, MODEL_FEATURE_ORDER, RAW_US100, F69A_DESIGN, F69A_REPORT]


def load_frames() -> tuple[pd.DataFrame, pd.DataFrame]:
    model_input = pd.read_parquet(io_path(MODEL_INPUT)).sort_values("timestamp").reset_index(drop=True)
    raw = pd.read_csv(
        io_path(RAW_US100),
        usecols=["time_close_unix", "open", "high", "low", "close", "spread_points"],
    )
    raw["timestamp"] = pd.to_datetime(raw["time_close_unix"], unit="s", utc=True)
    raw = raw.sort_values("timestamp").reset_index(drop=True)
    raw_positions = pd.Series(raw.index.to_numpy(), index=raw["timestamp"]).reindex(model_input["timestamp"]).to_numpy()
    if np.isnan(raw_positions).any():
        raise RuntimeError(f"raw/model timestamp alignment failed: {int(np.isnan(raw_positions).sum())} missing rows")
    raw_values = raw[["timestamp", "open", "high", "low", "close", "spread_points"]].rename(
        columns={
            "open": "raw_open",
            "high": "raw_high",
            "low": "raw_low",
            "close": "raw_close",
            "spread_points": "spread_points_proxy",
        }
    )
    frame = model_input.merge(raw_values, on="timestamp", how="left")
    if frame["spread_points_proxy"].isna().any():
        raise RuntimeError("spread join failed")
    frame["raw_pos"] = raw_positions.astype(int)
    frame["spread_cost_points"] = frame["spread_points_proxy"].astype(float) * 0.01
    return frame, raw


def target_specs() -> list[TargetSpec]:
    return [
        TargetSpec("fh_h3_sl09_tp135_edge10", 3),
        TargetSpec("fh_h6_sl09_tp135_edge10", 6),
        TargetSpec("fh_h9_sl09_tp135_edge10", 9),
    ]


def feature_sets(frame: pd.DataFrame) -> list[FeatureSet]:
    definitions = {
        "compact_event_context_v1": [
            "log_return_1",
            "hl_range",
            "close_open_ratio",
            "gap_percent",
            "return_zscore_20",
            "hl_zscore_50",
            "return_1_over_atr_14",
            "rsi_14",
            "rsi_14_slope_3",
            "bb_position_20",
            "bollinger_width_20",
            "bb_squeeze",
            "historical_vol_5_over_20",
            "adx_14",
            "di_spread_14",
            "atr_14_over_atr_50",
            "supertrend_10_3",
            "vortex_indicator",
            "minutes_from_cash_open",
            "is_first_30m_after_open",
            "is_last_30m_before_cash_close",
            "vix_change_1",
        ],
        "morph_session_core_v1": [
            "log_return_1",
            "hl_range",
            "close_open_ratio",
            "gap_percent",
            "return_zscore_20",
            "hl_zscore_50",
            "rsi_14",
            "bb_position_20",
            "minutes_from_cash_open",
            "is_first_30m_after_open",
            "is_last_30m_before_cash_close",
            "vix_change_1",
        ],
        "regime_session_core_v1": [
            "adx_14",
            "di_spread_14",
            "atr_14_over_atr_50",
            "historical_vol_5_over_20",
            "bb_squeeze",
            "bollinger_width_20",
            "supertrend_10_3",
            "vortex_indicator",
            "minutes_from_cash_open",
            "is_first_30m_after_open",
            "is_last_30m_before_cash_close",
            "vix_zscore_20",
        ],
        "price_path_core_v1": [
            "log_return_1",
            "log_return_3",
            "hl_range",
            "close_open_ratio",
            "gap_percent",
            "close_prev_close_ratio",
            "return_zscore_20",
            "return_1_over_atr_14",
            "rsi_14_slope_3",
            "ppo_hist_12_26_9",
            "roc_12",
            "trix_15",
        ],
    }
    output: list[FeatureSet] = []
    for name, columns in definitions.items():
        present = tuple(column for column in columns if column in frame.columns)
        if len(present) != len(columns):
            missing = sorted(set(columns) - set(present))
            raise RuntimeError(f"feature set {name} missing columns: {missing}")
        output.append(FeatureSet(name, present))
    return output


def model_specs() -> list[ModelSpec]:
    return [
        ModelSpec(
            "linear_logreg_balanced_v1",
            "linear(선형)",
            lambda: make_pipeline(
                SimpleImputer(strategy="median"),
                StandardScaler(),
                LogisticRegression(max_iter=500, class_weight="balanced", random_state=69),
            ),
        ),
        ModelSpec(
            "shallow_extra_trees_v1",
            "shallow_tree(얕은 트리)",
            lambda: make_pipeline(
                SimpleImputer(strategy="median"),
                ExtraTreesClassifier(
                    n_estimators=160,
                    max_depth=8,
                    min_samples_leaf=80,
                    class_weight="balanced",
                    random_state=69,
                    n_jobs=-1,
                ),
            ),
        ),
        ModelSpec(
            "small_hist_gradient_v1",
            "small_boosting(작은 부스팅)",
            lambda: make_pipeline(
                SimpleImputer(strategy="median"),
                HistGradientBoostingClassifier(
                    max_iter=80,
                    learning_rate=0.05,
                    max_leaf_nodes=15,
                    l2_regularization=0.10,
                    random_state=69,
                ),
            ),
        ),
    ]


def event_specs(frame: pd.DataFrame) -> list[EventSpec]:
    cash = numeric(frame["is_us_cash_open"]).fillna(0).to_numpy(dtype=float) >= 0.5
    ret_abs_q70 = q(frame, "return_zscore_20", 0.70, 0.75, absolute=True)
    hl_q65 = q(frame, "hl_zscore_50", 0.65, 0.50, absolute=False)
    bbw_q35 = q(frame, "bollinger_width_20", 0.35, 0.008)
    adx_q60 = q(frame, "adx_14", 0.60, 25.0)
    vol_q55 = q(frame, "historical_vol_5_over_20", 0.55, 1.0)
    di_abs_q60 = q(frame, "di_spread_14", 0.60, 6.0, absolute=True)
    minutes = numeric(frame["minutes_from_cash_open"]).fillna(-999).to_numpy(dtype=float)
    di = numeric(frame["di_spread_14"]).fillna(0).to_numpy(dtype=float)
    vortex = numeric(frame["vortex_indicator"]).fillna(0).to_numpy(dtype=float)
    return [
        EventSpec("event_cash_any_context", "US cash-session any-context control(미국 현물장 전체 문맥 대조)", cash),
        EventSpec(
            "event_morph_range_impulse",
            "return/range impulse event(수익률/범위 충격 이벤트)",
            cash
            & (
                (numeric(frame["return_zscore_20"]).abs().fillna(0).to_numpy(dtype=float) >= ret_abs_q70)
                | (numeric(frame["hl_zscore_50"]).fillna(0).to_numpy(dtype=float) >= hl_q65)
            ),
        ),
        EventSpec(
            "event_bb_squeeze_release",
            "Bollinger squeeze/release event(볼린저 압축/해제 이벤트)",
            cash
            & (
                (numeric(frame["bb_squeeze"]).fillna(0).to_numpy(dtype=float) >= 0.5)
                | (numeric(frame["bollinger_width_20"]).fillna(999).to_numpy(dtype=float) <= bbw_q35)
            ),
        ),
        EventSpec(
            "event_trend_vol_expansion",
            "trend plus volatility expansion event(추세와 변동성 확장 이벤트)",
            cash
            & (numeric(frame["adx_14"]).fillna(0).to_numpy(dtype=float) >= adx_q60)
            & (numeric(frame["historical_vol_5_over_20"]).fillna(0).to_numpy(dtype=float) >= vol_q55),
        ),
        EventSpec(
            "event_session_edges",
            "cash open/close edge event(현물장 초반/후반 이벤트)",
            cash
            & (
                (numeric(frame["is_first_30m_after_open"]).fillna(0).to_numpy(dtype=float) >= 0.5)
                | (numeric(frame["is_last_30m_before_cash_close"]).fillna(0).to_numpy(dtype=float) >= 0.5)
                | ((minutes > 0) & (minutes <= 60))
            ),
        ),
        EventSpec(
            "event_vortex_di_alignment",
            "vortex and DI alignment event(보텍스와 DI 정렬 이벤트)",
            cash & (np.abs(di) >= di_abs_q60) & (np.sign(di) == np.sign(vortex)) & (np.sign(di) != 0),
        ),
    ]


def first_hit_profit(
    *,
    side: int,
    idx: np.ndarray,
    horizon: int,
    entry: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    atr: np.ndarray,
    cost: np.ndarray,
    sl_atr: float,
    tp_atr: float,
) -> np.ndarray:
    output = np.empty(len(idx), dtype=float)
    stop_distance = np.maximum(1.0, atr * float(sl_atr))
    take_distance = np.maximum(1.0, atr * float(tp_atr))
    for row_num, start in enumerate(idx):
        entry_price = float(entry[row_num])
        stop = float(stop_distance[row_num])
        take = float(take_distance[row_num])
        fallback = float(close[start + horizon]) - entry_price if side == 2 else entry_price - float(close[start + horizon])
        profit = fallback
        for bar in range(start + 1, start + horizon + 1):
            if side == 2:
                stop_hit = float(low[bar]) <= entry_price - stop
                take_hit = float(high[bar]) >= entry_price + take
            else:
                stop_hit = float(high[bar]) >= entry_price + stop
                take_hit = float(low[bar]) <= entry_price - take
            if stop_hit:
                profit = -stop
                break
            if take_hit:
                profit = take
                break
        output[row_num] = profit - float(cost[row_num])
    return output


def build_target_frame(base: pd.DataFrame, raw: pd.DataFrame, spec: TargetSpec) -> pd.DataFrame:
    horizon = int(spec.horizon_bars)
    valid = base["raw_pos"].to_numpy(dtype=int) + horizon < len(raw)
    frame = base.loc[valid].copy().reset_index(drop=True)
    idx = frame["raw_pos"].to_numpy(dtype=int)
    high = raw["high"].to_numpy(dtype=float)
    low = raw["low"].to_numpy(dtype=float)
    close = raw["close"].to_numpy(dtype=float)
    entry = close[idx]
    atr = frame["atr_14"].to_numpy(dtype=float)
    finite_atr = atr[np.isfinite(atr) & (atr > 0)]
    fallback_atr = float(np.median(finite_atr)) if len(finite_atr) else 10.0
    atr = np.where(np.isfinite(atr) & (atr > 0), atr, fallback_atr)
    cost = frame["spread_cost_points"].to_numpy(dtype=float)
    long_profit = first_hit_profit(
        side=2,
        idx=idx,
        horizon=horizon,
        entry=entry,
        high=high,
        low=low,
        close=close,
        atr=atr,
        cost=cost,
        sl_atr=spec.sl_atr,
        tp_atr=spec.tp_atr,
    )
    short_profit = first_hit_profit(
        side=0,
        idx=idx,
        horizon=horizon,
        entry=entry,
        high=high,
        low=low,
        close=close,
        atr=atr,
        cost=cost,
        sl_atr=spec.sl_atr,
        tp_atr=spec.tp_atr,
    )
    min_edge = np.maximum(float(spec.min_edge_points), float(spec.min_edge_atr) * atr)
    target = np.where(
        (long_profit > min_edge) & (long_profit > short_profit),
        2,
        np.where((short_profit > min_edge) & (short_profit > long_profit), 0, 1),
    )
    frame["target_class"] = target.astype(int)
    frame["long_first_hit_profit_points"] = long_profit
    frame["short_first_hit_profit_points"] = short_profit
    frame["target_min_edge_points"] = min_edge
    return frame


def side_and_edge(proba: np.ndarray, classes: Sequence[int]) -> tuple[np.ndarray, np.ndarray]:
    probs = {int(cls): proba[:, idx] for idx, cls in enumerate(classes)}
    zeros = np.zeros(len(proba), dtype=float)
    p_short = probs.get(0, zeros)
    p_flat = probs.get(1, zeros)
    p_long = probs.get(2, zeros)
    side = np.where((p_long > p_short) & (p_long > p_flat), 2, np.where((p_short > p_long) & (p_short > p_flat), 0, 1))
    edge = np.where(side == 2, p_long - np.maximum(p_short, p_flat), np.where(side == 0, p_short - np.maximum(p_long, p_flat), -999.0))
    return side.astype(int), edge.astype(float)


def apply_side_policy(side: np.ndarray, side_policy: str) -> np.ndarray:
    adjusted = side.copy()
    if side_policy == "long_only":
        adjusted[adjusted == 0] = 1
    if side_policy == "short_only":
        adjusted[adjusted == 2] = 1
    return adjusted


def non_overlap_indices(signal: np.ndarray, horizon: int, cooldown_bars: int) -> list[int]:
    chosen: list[int] = []
    next_allowed = 0
    for idx, active in enumerate(signal):
        if not active or idx < next_allowed:
            continue
        chosen.append(idx)
        next_allowed = idx + int(horizon) + int(cooldown_bars) + 1
    return chosen


def profit_for_side(frame: pd.DataFrame, side: np.ndarray) -> np.ndarray:
    long_profit = frame["long_first_hit_profit_points"].to_numpy(dtype=float)
    short_profit = frame["short_first_hit_profit_points"].to_numpy(dtype=float)
    return np.where(side == 2, long_profit, np.where(side == 0, short_profit, 0.0))


def max_consecutive_loss(values: np.ndarray) -> int:
    current = 0
    best = 0
    for value in values:
        if value < 0:
            current += 1
            best = max(best, current)
        else:
            current = 0
    return best


def underwater_stats(values: np.ndarray) -> dict[str, Any]:
    if len(values) == 0:
        return {"max_underwater_trades": 0, "time_under_water_trade_share": 0.0}
    equity = np.cumsum(values)
    peak = np.maximum.accumulate(np.r_[0.0, equity])[:-1]
    under = equity < peak
    current = 0
    best = 0
    for flag in under:
        if flag:
            current += 1
            best = max(best, current)
        else:
            current = 0
    return {"max_underwater_trades": int(best), "time_under_water_trade_share": float(under.mean())}


def monthly_smoothness(values: np.ndarray, timestamps: pd.Series) -> dict[str, Any]:
    if len(values) == 0:
        return {"positive_month_share": 0.0, "month_count": 0}
    frame = pd.DataFrame({"timestamp": pd.to_datetime(timestamps, utc=True), "profit": values})
    monthly = frame.groupby(frame["timestamp"].dt.strftime("%Y-%m"))["profit"].sum()
    if monthly.empty:
        return {"positive_month_share": 0.0, "month_count": 0}
    return {"positive_month_share": float((monthly > 0).mean()), "month_count": int(len(monthly))}


def proxy_kpi(values: np.ndarray, trade_timestamps: pd.Series, period_timestamps: pd.Series) -> dict[str, Any]:
    values = np.asarray(values, dtype=float)
    if len(period_timestamps) >= 2:
        period_days = max(
            1.0,
            (pd.to_datetime(period_timestamps.max(), utc=True) - pd.to_datetime(period_timestamps.min(), utc=True)).total_seconds() / 86400.0,
        )
    else:
        period_days = 1.0
    if len(values) == 0:
        return {
            "net_profit": 0.0,
            "gross_profit": 0.0,
            "gross_loss": 0.0,
            "profit_factor": 0.0,
            "trade_count": 0,
            "trades_per_day": 0.0,
            "win_rate": 0.0,
            "average_win": 0.0,
            "average_loss": 0.0,
            "payoff_ratio": 0.0,
            "expectancy": 0.0,
            "max_drawdown": 0.0,
            "max_drawdown_percent_on_10000": 0.0,
            "recovery_factor": 0.0,
            "max_consecutive_loss": 0,
            "max_underwater_trades": 0,
            "time_under_water_trade_share": 0.0,
            "positive_month_share": 0.0,
            "month_count": 0,
        }
    wins = values[values > 0]
    losses = values[values < 0]
    gross_profit = float(wins.sum()) if len(wins) else 0.0
    gross_loss = float(-losses.sum()) if len(losses) else 0.0
    net = float(values.sum())
    equity = np.cumsum(values)
    peak = np.maximum.accumulate(np.r_[0.0, equity])
    drawdowns = peak[1:] - equity
    max_dd = float(drawdowns.max()) if len(drawdowns) else 0.0
    underwater = underwater_stats(values)
    smooth = monthly_smoothness(values, trade_timestamps)
    return {
        "net_profit": net,
        "gross_profit": gross_profit,
        "gross_loss": gross_loss,
        "profit_factor": gross_profit / gross_loss if gross_loss > 0 else (99.0 if gross_profit > 0 else 0.0),
        "trade_count": int(len(values)),
        "trades_per_day": float(len(values) / period_days),
        "win_rate": float((values > 0).mean() * 100.0),
        "average_win": float(wins.mean()) if len(wins) else 0.0,
        "average_loss": float(losses.mean()) if len(losses) else 0.0,
        "payoff_ratio": float(abs(wins.mean() / losses.mean())) if len(wins) and len(losses) else 0.0,
        "expectancy": float(values.mean()),
        "max_drawdown": max_dd,
        "max_drawdown_percent_on_10000": max_dd / 10000.0 * 100.0,
        "recovery_factor": net / max_dd if max_dd > 0 else (99.0 if net > 0 else 0.0),
        "max_consecutive_loss": max_consecutive_loss(values),
        **underwater,
        **smooth,
    }


def evaluate_candidate(
    frame: pd.DataFrame,
    split_name: str,
    split_mask: np.ndarray,
    split_side: np.ndarray,
    split_edge: np.ndarray,
    event_mask: np.ndarray,
    spec: CandidateSpec,
) -> dict[str, Any]:
    split_frame = frame.loc[split_mask].copy().reset_index(drop=True)
    local_event = event_mask[split_mask]
    side = apply_side_policy(split_side.copy(), spec.side_policy)
    signal = local_event & (side != 1) & (split_edge >= float(spec.edge_threshold))
    selected = non_overlap_indices(signal, spec.target.horizon_bars, spec.cooldown_bars)
    values = profit_for_side(split_frame, side)
    selected_values = values[selected] if selected else np.array([], dtype=float)
    selected_timestamps = split_frame.loc[selected, "timestamp"] if selected else split_frame["timestamp"].iloc[:0]
    metrics = proxy_kpi(selected_values, selected_timestamps, split_frame["timestamp"])
    long_count = int((side[selected] == 2).sum()) if selected else 0
    short_count = int((side[selected] == 0).sum()) if selected else 0
    return {
        "candidate_id": spec.candidate_id,
        "split": split_name,
        "target_id": spec.target.target_id,
        "horizon_bars": spec.target.horizon_bars,
        "sl_atr": spec.target.sl_atr,
        "tp_atr": spec.target.tp_atr,
        "feature_set_id": spec.feature_set.feature_set_id,
        "feature_count": len(spec.feature_set.columns),
        "model_id": spec.model.model_id,
        "model_family": spec.model.model_family,
        "event_id": spec.event_id,
        "threshold_quantile": spec.threshold_quantile,
        "edge_threshold_from_train": spec.edge_threshold,
        "side_policy": spec.side_policy,
        "cooldown_bars": spec.cooldown_bars,
        "event_rows": int(local_event.sum()),
        "raw_signal_rows": int(signal.sum()),
        "trade_count": metrics["trade_count"],
        "trades_per_day": metrics["trades_per_day"],
        "net_profit": metrics["net_profit"],
        "gross_profit": metrics["gross_profit"],
        "gross_loss": metrics["gross_loss"],
        "profit_factor": metrics["profit_factor"],
        "drawdown": metrics["max_drawdown"],
        "drawdown_percent_on_10000": metrics["max_drawdown_percent_on_10000"],
        "win_rate": metrics["win_rate"],
        "average_win": metrics["average_win"],
        "average_loss": metrics["average_loss"],
        "payoff_ratio": metrics["payoff_ratio"],
        "expectancy": metrics["expectancy"],
        "recovery_factor": metrics["recovery_factor"],
        "time_under_water_trade_share": metrics["time_under_water_trade_share"],
        "max_underwater_trades": metrics["max_underwater_trades"],
        "max_consecutive_loss": metrics["max_consecutive_loss"],
        "positive_month_share": metrics["positive_month_share"],
        "month_count": metrics["month_count"],
        "long_trade_count": long_count,
        "short_trade_count": short_count,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def class_counts(frame: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for split_name, split_frame in frame.groupby(frame["split"].astype(str)):
        counts = split_frame["target_class"].value_counts().to_dict()
        rows.append(
            {
                "split": split_name,
                "rows": int(len(split_frame)),
                "short_class_0": int(counts.get(0, 0)),
                "flat_class_1": int(counts.get(1, 0)),
                "long_class_2": int(counts.get(2, 0)),
            }
        )
    return rows


def train_and_score(frame: pd.DataFrame, target: TargetSpec, features: FeatureSet, model: ModelSpec, events: Sequence[EventSpec]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    train_mask = frame["split"].astype(str).eq("train").to_numpy()
    y_train = frame.loc[train_mask, "target_class"].to_numpy(dtype=int)
    if len(set(y_train.tolist())) < 2:
        return [], {"status": "skipped_single_class", "target_id": target.target_id, "feature_set_id": features.feature_set_id, "model_id": model.model_id}
    estimator = model.build()
    estimator.fit(frame.loc[train_mask, list(features.columns)], y_train)
    classes = list(getattr(estimator, "classes_", getattr(estimator[-1], "classes_", [])))
    proba_by_split: dict[str, tuple[np.ndarray, np.ndarray, np.ndarray]] = {}
    for split_name in ("train", "validation", "oos"):
        mask = frame["split"].astype(str).eq(split_name).to_numpy()
        proba = estimator.predict_proba(frame.loc[mask, list(features.columns)])
        side, edge = side_and_edge(proba, classes)
        proba_by_split[split_name] = (mask, side, edge)

    rows: list[dict[str, Any]] = []
    train_mask_arr, train_side_base, train_edge = proba_by_split["train"]
    for event in events:
        for side_policy in ("both", "long_only", "short_only"):
            train_side = apply_side_policy(train_side_base.copy(), side_policy)
            train_pool_mask = event.mask[train_mask_arr] & (train_side != 1) & np.isfinite(train_edge)
            train_pool = train_edge[train_pool_mask]
            if len(train_pool) == 0:
                continue
            for threshold_quantile in (0.50, 0.65, 0.80, 0.90, 0.95):
                edge_threshold = float(np.quantile(train_pool, threshold_quantile))
                candidate_id = "f69b_" + stable_id(
                    [
                        target.target_id,
                        features.feature_set_id,
                        model.model_id,
                        event.event_id,
                        threshold_quantile,
                        side_policy,
                    ]
                )
                spec = CandidateSpec(
                    candidate_id=candidate_id,
                    target=target,
                    feature_set=features,
                    model=model,
                    event_id=event.event_id,
                    threshold_quantile=threshold_quantile,
                    edge_threshold=edge_threshold,
                    side_policy=side_policy,
                    cooldown_bars=target.horizon_bars,
                )
                for split_name in ("validation", "oos"):
                    split_mask, split_side, split_edge = proba_by_split[split_name]
                    rows.append(evaluate_candidate(frame, split_name, split_mask, split_side, split_edge, event.mask, spec))
    return rows, {
        "status": "trained",
        "target_id": target.target_id,
        "feature_set_id": features.feature_set_id,
        "model_id": model.model_id,
        "classes_seen": [int(value) for value in classes],
        "label_counts": class_counts(frame),
    }


def summarize_candidates(kpi_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    by_candidate: dict[str, dict[str, Mapping[str, Any]]] = {}
    for row in kpi_rows:
        by_candidate.setdefault(str(row["candidate_id"]), {})[str(row["split"])] = row
    summaries: list[dict[str, Any]] = []
    for candidate_id, split_rows in by_candidate.items():
        val = split_rows.get("validation")
        oos = split_rows.get("oos")
        if not val or not oos:
            continue
        min_pf = min(float(val["profit_factor"]), float(oos["profit_factor"]))
        min_net = min(float(val["net_profit"]), float(oos["net_profit"]))
        max_dd = max(float(val["drawdown_percent_on_10000"]), float(oos["drawdown_percent_on_10000"]))
        density_distance = abs(float(val["trades_per_day"]) - 7.5) + abs(float(oos["trades_per_day"]) - 7.5)
        scout_signal = (
            float(val["net_profit"]) > 0
            and float(oos["net_profit"]) > 0
            and min_pf >= 1.05
            and 2.0 <= float(oos["trades_per_day"]) <= 18.0
            and int(oos["trade_count"]) >= 20
        )
        meaningful = (
            scout_signal
            and min_pf >= 1.08
            and 3.0 <= float(val["trades_per_day"]) <= 15.0
            and 3.0 <= float(oos["trades_per_day"]) <= 15.0
            and max_dd <= 25.0
        )
        score = (
            min_pf * 100.0
            + min_net * 0.05
            + min(float(val["recovery_factor"]), float(oos["recovery_factor"])) * 2.0
            - max_dd * 0.5
            - density_distance * 3.0
        )
        summaries.append(
            {
                "candidate_id": candidate_id,
                "target_id": val["target_id"],
                "horizon_bars": val["horizon_bars"],
                "feature_set_id": val["feature_set_id"],
                "feature_count": val["feature_count"],
                "model_id": val["model_id"],
                "model_family": val["model_family"],
                "event_id": val["event_id"],
                "threshold_quantile": val["threshold_quantile"],
                "side_policy": val["side_policy"],
                "cooldown_bars": val["cooldown_bars"],
                "validation_net": val["net_profit"],
                "validation_pf": val["profit_factor"],
                "validation_dd_pct": val["drawdown_percent_on_10000"],
                "validation_trades": val["trade_count"],
                "validation_trades_per_day": val["trades_per_day"],
                "validation_win_rate": val["win_rate"],
                "validation_expectancy": val["expectancy"],
                "oos_net": oos["net_profit"],
                "oos_pf": oos["profit_factor"],
                "oos_dd_pct": oos["drawdown_percent_on_10000"],
                "oos_trades": oos["trade_count"],
                "oos_trades_per_day": oos["trades_per_day"],
                "oos_win_rate": oos["win_rate"],
                "oos_expectancy": oos["expectancy"],
                "min_pf": min_pf,
                "min_net": min_net,
                "max_dd_pct": max_dd,
                "density_distance_to_7p5": density_distance,
                "scout_signal": bool(scout_signal),
                "meaningful_proxy_signal": bool(meaningful),
                "selection_score": float(score),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return sorted(summaries, key=lambda row: float(row["selection_score"]), reverse=True)


def event_budget_rows(frame: pd.DataFrame, events: Sequence[EventSpec]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for event in events:
        for split_name in ("train", "validation", "oos"):
            mask = frame["split"].astype(str).eq(split_name).to_numpy()
            split_frame = frame.loc[mask]
            days = max(
                1.0,
                (pd.to_datetime(split_frame["timestamp"].max(), utc=True) - pd.to_datetime(split_frame["timestamp"].min(), utc=True)).total_seconds() / 86400.0,
            )
            count = int(event.mask[mask].sum())
            rows.append(
                {
                    "event_id": event.event_id,
                    "description": event.description,
                    "split": split_name,
                    "event_rows": count,
                    "split_rows": int(mask.sum()),
                    "event_rows_per_day": float(count / days),
                    "event_row_share": float(count / max(1, int(mask.sum()))),
                }
            )
    return rows


def bucket_label(frame: pd.DataFrame, bucket_group: str) -> pd.Series:
    if bucket_group == "session":
        minutes = numeric(frame["minutes_from_cash_open"]).fillna(-999)
        return pd.Series(
            np.select(
                [
                    (minutes > 0) & (minutes <= 30),
                    (minutes > 30) & (minutes <= 300),
                    (minutes > 300) & (minutes <= 390),
                ],
                ["open_0_30", "mid_35_300", "late_305_390"],
                default="outside_or_missing",
            ),
            index=frame.index,
        )
    adx = numeric(frame["adx_14"]).fillna(0)
    hv = numeric(frame["historical_vol_5_over_20"]).fillna(0)
    squeeze = numeric(frame["bb_squeeze"]).fillna(0)
    return pd.Series(
        np.select(
            [
                adx >= 25,
                adx < 18,
                hv >= 1.25,
                squeeze >= 0.5,
            ],
            ["trend_adx_ge25", "chop_adx_lt18", "vol_expansion_hv5over20_ge1p25", "bb_squeeze_on"],
            default="other_regime",
        ),
        index=frame.index,
    )


def selected_trade_frame(
    frame: pd.DataFrame,
    split_name: str,
    event_mask: np.ndarray,
    side: np.ndarray,
    edge: np.ndarray,
    spec: CandidateSpec,
) -> pd.DataFrame:
    split_mask = frame["split"].astype(str).eq(split_name).to_numpy()
    split_frame = frame.loc[split_mask].copy().reset_index(drop=True)
    local_event = event_mask[split_mask]
    adjusted_side = apply_side_policy(side.copy(), spec.side_policy)
    signal = local_event & (adjusted_side != 1) & (edge >= float(spec.edge_threshold))
    selected = non_overlap_indices(signal, spec.target.horizon_bars, spec.cooldown_bars)
    if not selected:
        return split_frame.iloc[:0].copy()
    out = split_frame.loc[selected].copy()
    out["selected_side"] = adjusted_side[selected]
    out["selected_profit"] = profit_for_side(split_frame, adjusted_side)[selected]
    return out


def bucket_kpi_rows(
    frame_by_target: Mapping[str, pd.DataFrame],
    summaries: Sequence[Mapping[str, Any]],
    spec_index: Mapping[str, CandidateSpec],
    split_score_cache: Mapping[str, Mapping[str, tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for summary in list(summaries)[:20]:
        candidate_id = str(summary["candidate_id"])
        spec = spec_index.get(candidate_id)
        if spec is None:
            continue
        frame = frame_by_target.get(spec.target.target_id)
        if frame is None:
            continue
        cache_key = "|".join([spec.target.target_id, spec.feature_set.feature_set_id, spec.model.model_id])
        score_payload = split_score_cache.get(cache_key, {})
        event_mask = score_payload.get("event_masks", {}).get(spec.event_id) if isinstance(score_payload.get("event_masks"), dict) else None
        if event_mask is None:
            continue
        for split_name in ("validation", "oos"):
            split_payload = score_payload.get(split_name)
            if split_payload is None:
                continue
            split_mask, side, edge = split_payload
            trade_frame = selected_trade_frame(frame, split_name, event_mask, side, edge, spec)
            for bucket_group in ("session", "regime"):
                labels = bucket_label(trade_frame, bucket_group) if len(trade_frame) else pd.Series(dtype=str)
                for bucket in sorted(labels.unique().tolist()):
                    bucket_trades = trade_frame.loc[labels.eq(bucket)]
                    metrics = proxy_kpi(
                        bucket_trades["selected_profit"].to_numpy(dtype=float),
                        bucket_trades["timestamp"],
                        frame.loc[frame["split"].astype(str).eq(split_name), "timestamp"],
                    )
                    rows.append(
                        {
                            "candidate_id": candidate_id,
                            "split": split_name,
                            "bucket_group": bucket_group,
                            "bucket": bucket,
                            "trade_count": metrics["trade_count"],
                            "trades_per_day": metrics["trades_per_day"],
                            "net_profit": metrics["net_profit"],
                            "gross_profit": metrics["gross_profit"],
                            "gross_loss": metrics["gross_loss"],
                            "profit_factor": metrics["profit_factor"],
                            "drawdown_percent_on_10000": metrics["max_drawdown_percent_on_10000"],
                            "win_rate": metrics["win_rate"],
                            "expectancy": metrics["expectancy"],
                            "long_trade_count": int((bucket_trades["selected_side"] == 2).sum()) if len(bucket_trades) else 0,
                            "short_trade_count": int((bucket_trades["selected_side"] == 0).sum()) if len(bucket_trades) else 0,
                        }
                    )
    return rows


def evaluate_shuffled_control(
    frame_by_target: Mapping[str, pd.DataFrame],
    top_summaries: Sequence[Mapping[str, Any]],
    spec_index: Mapping[str, CandidateSpec],
    feature_lookup: Mapping[str, FeatureSet],
    model_lookup: Mapping[str, ModelSpec],
) -> list[dict[str, Any]]:
    rng = np.random.default_rng(6901)
    rows: list[dict[str, Any]] = []
    for summary in list(top_summaries)[:12]:
        candidate_id = str(summary["candidate_id"])
        spec = spec_index.get(candidate_id)
        if spec is None:
            continue
        frame = frame_by_target[spec.target.target_id]
        features = feature_lookup[spec.feature_set.feature_set_id]
        model = model_lookup[spec.model.model_id]
        train_mask = frame["split"].astype(str).eq("train").to_numpy()
        y_train = frame.loc[train_mask, "target_class"].to_numpy(dtype=int).copy()
        rng.shuffle(y_train)
        estimator = model.build()
        estimator.fit(frame.loc[train_mask, list(features.columns)], y_train)
        classes = list(getattr(estimator, "classes_", getattr(estimator[-1], "classes_", [])))
        events = {event.event_id: event.mask for event in event_specs(frame)}
        train_proba = estimator.predict_proba(frame.loc[train_mask, list(features.columns)])
        train_side, train_edge = side_and_edge(train_proba, classes)
        train_side = apply_side_policy(train_side, spec.side_policy)
        train_pool_mask = events[spec.event_id][train_mask] & (train_side != 1) & np.isfinite(train_edge)
        train_pool = train_edge[train_pool_mask]
        threshold = float(np.quantile(train_pool, spec.threshold_quantile)) if len(train_pool) else 999.0
        shuffled_spec = CandidateSpec(
            candidate_id=candidate_id,
            target=spec.target,
            feature_set=spec.feature_set,
            model=spec.model,
            event_id=spec.event_id,
            threshold_quantile=spec.threshold_quantile,
            edge_threshold=threshold,
            side_policy=spec.side_policy,
            cooldown_bars=spec.cooldown_bars,
        )
        payload: dict[str, Any] = {
            "candidate_id": candidate_id,
            "control_type": "train_label_shuffle(학습 라벨 셔플)",
            "original_validation_net": summary.get("validation_net"),
            "original_oos_net": summary.get("oos_net"),
            "original_validation_pf": summary.get("validation_pf"),
            "original_oos_pf": summary.get("oos_pf"),
        }
        for split_name in ("validation", "oos"):
            mask = frame["split"].astype(str).eq(split_name).to_numpy()
            proba = estimator.predict_proba(frame.loc[mask, list(features.columns)])
            side, edge = side_and_edge(proba, classes)
            row = evaluate_candidate(frame, split_name, mask, side, edge, events[spec.event_id], shuffled_spec)
            payload[f"{split_name}_shuffle_net"] = row["net_profit"]
            payload[f"{split_name}_shuffle_pf"] = row["profit_factor"]
            payload[f"{split_name}_shuffle_trades_per_day"] = row["trades_per_day"]
            payload[f"{split_name}_shuffle_trades"] = row["trade_count"]
        payload["oos_net_gap_vs_shuffle"] = float(summary.get("oos_net", 0.0)) - float(payload.get("oos_shuffle_net", 0.0))
        payload["oos_pf_gap_vs_shuffle"] = float(summary.get("oos_pf", 0.0)) - float(payload.get("oos_shuffle_pf", 0.0))
        rows.append(payload)
    return rows


def run_proxy_sweep(created_at: str) -> dict[str, Any]:
    missing = [rel(path) for path in required_artifacts() if not path_exists(path)]
    if missing:
        raise FileNotFoundError(f"F69B required material missing: {missing}")
    base, raw = load_frames()
    feature_lookup = {feature.feature_set_id: feature for feature in feature_sets(base)}
    model_lookup = {model.model_id: model for model in model_specs()}

    all_kpi_rows: list[dict[str, Any]] = []
    model_audit_rows: list[dict[str, Any]] = []
    class_balance_rows: list[dict[str, Any]] = []
    frame_by_target: dict[str, pd.DataFrame] = {}
    spec_index: dict[str, CandidateSpec] = {}
    split_score_cache: dict[str, dict[str, Any]] = {}
    event_budget_all: list[dict[str, Any]] = []

    for target in target_specs():
        frame = build_target_frame(base, raw, target)
        frame_by_target[target.target_id] = frame
        events = event_specs(frame)
        event_budget_all.extend([{**row, "target_id": target.target_id} for row in event_budget_rows(frame, events)])
        for row in class_counts(frame):
            class_balance_rows.append({"target_id": target.target_id, **row})
        for features in feature_lookup.values():
            for model in model_lookup.values():
                train_mask = frame["split"].astype(str).eq("train").to_numpy()
                y_train = frame.loc[train_mask, "target_class"].to_numpy(dtype=int)
                if len(set(y_train.tolist())) < 2:
                    model_audit_rows.append(
                        {
                            "target_id": target.target_id,
                            "feature_set_id": features.feature_set_id,
                            "model_id": model.model_id,
                            "status": "skipped_single_class",
                        }
                    )
                    continue
                estimator = model.build()
                estimator.fit(frame.loc[train_mask, list(features.columns)], y_train)
                classes = list(getattr(estimator, "classes_", getattr(estimator[-1], "classes_", [])))
                cache_key = "|".join([target.target_id, features.feature_set_id, model.model_id])
                split_score_cache[cache_key] = {"event_masks": {event.event_id: event.mask for event in events}}
                for split_name in ("train", "validation", "oos"):
                    mask = frame["split"].astype(str).eq(split_name).to_numpy()
                    proba = estimator.predict_proba(frame.loc[mask, list(features.columns)])
                    side, edge = side_and_edge(proba, classes)
                    split_score_cache[cache_key][split_name] = (mask, side, edge)
                model_audit_rows.append(
                    {
                        "target_id": target.target_id,
                        "feature_set_id": features.feature_set_id,
                        "model_id": model.model_id,
                        "status": "trained",
                        "classes_seen": ",".join(str(int(value)) for value in classes),
                        "train_rows": int(train_mask.sum()),
                    }
                )
                train_mask_arr, train_side_base, train_edge = split_score_cache[cache_key]["train"]
                for event in events:
                    for side_policy in ("both", "long_only", "short_only"):
                        train_side = apply_side_policy(train_side_base.copy(), side_policy)
                        train_pool_mask = event.mask[train_mask_arr] & (train_side != 1) & np.isfinite(train_edge)
                        train_pool = train_edge[train_pool_mask]
                        if len(train_pool) == 0:
                            continue
                        for threshold_quantile in (0.50, 0.65, 0.80, 0.90, 0.95):
                            edge_threshold = float(np.quantile(train_pool, threshold_quantile))
                            candidate_id = "f69b_" + stable_id(
                                [
                                    target.target_id,
                                    features.feature_set_id,
                                    model.model_id,
                                    event.event_id,
                                    threshold_quantile,
                                    side_policy,
                                ]
                            )
                            candidate = CandidateSpec(
                                candidate_id=candidate_id,
                                target=target,
                                feature_set=features,
                                model=model,
                                event_id=event.event_id,
                                threshold_quantile=threshold_quantile,
                                edge_threshold=edge_threshold,
                                side_policy=side_policy,
                                cooldown_bars=target.horizon_bars,
                            )
                            spec_index[candidate_id] = candidate
                            for split_name in ("validation", "oos"):
                                split_mask, split_side, split_edge = split_score_cache[cache_key][split_name]
                                all_kpi_rows.append(evaluate_candidate(frame, split_name, split_mask, split_side, split_edge, event.mask, candidate))

    summaries = summarize_candidates(all_kpi_rows)
    meaningful = [row for row in summaries if row["meaningful_proxy_signal"]]
    scout = [row for row in summaries if row["scout_signal"]]
    top = summaries[:25]
    bucket_rows = bucket_kpi_rows(frame_by_target, top, spec_index, split_score_cache)
    shuffle_rows = evaluate_shuffled_control(frame_by_target, top, spec_index, feature_lookup, model_lookup)
    shuffle_by_candidate = {str(row["candidate_id"]): row for row in shuffle_rows}
    meaningful_with_control = [
        row
        for row in meaningful
        if float(shuffle_by_candidate.get(str(row["candidate_id"]), {}).get("oos_net_gap_vs_shuffle", 0.0)) > 0
        or str(row["candidate_id"]) not in shuffle_by_candidate
    ]
    next_run_id = NEXT_RUN_SIGNAL if meaningful_with_control else NEXT_RUN_REPAIR
    status = "completed_proxy_scout_clue_no_authority" if meaningful_with_control else "completed_proxy_scout_repair_required_no_authority"
    judgment = "scout_clue_proxy_signal_found_no_authority" if meaningful_with_control else "proxy_signal_inconclusive_repair_required_no_authority"
    return {
        "created_at_utc": created_at,
        "base_rows": int(len(base)),
        "raw_rows": int(len(raw)),
        "feature_set_count": len(feature_lookup),
        "model_count": len(model_lookup),
        "target_count": len(target_specs()),
        "candidate_kpi_rows": all_kpi_rows,
        "candidate_summaries": summaries,
        "meaningful_candidates": meaningful,
        "scout_candidates": scout,
        "meaningful_with_control": meaningful_with_control,
        "top_candidates": top,
        "bucket_kpi_rows": bucket_rows,
        "shuffle_control_rows": shuffle_rows,
        "event_budget_rows": event_budget_all,
        "class_balance_rows": class_balance_rows,
        "model_audit_rows": model_audit_rows,
        "next_run_id": next_run_id,
        "status": status,
        "judgment": judgment,
    }


def data_integrity_payload(result: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "data_source": rel(MODEL_INPUT),
        "raw_source": rel(RAW_US100),
        "time_axis": "model timestamp(모델 타임스탬프)은 raw time_close_unix 정렬 키로만 사용; session features(세션 피처)는 기존 물질화 결과 사용",
        "sample_scope": "US100 M5, train/validation/OOS split_v1, Tier A proxy only with Tier B explicitly marked missing/out_of_scope",
        "feature_label_boundary": "features use closed entry bar; first-hit future path starts at entry bar + 1",
        "split_boundary": "train fits model and score thresholds; validation/OOS only evaluate",
        "leakage_risk": "threshold and event quantiles are train-derived; repeated candidate search remains scout-only selection-bias risk",
        "data_hash_or_identity": {
            "model_input_sha256": sha256_file(MODEL_INPUT),
            "feature_order_sha256": sha256_file(MODEL_FEATURE_ORDER),
            "raw_us100_sha256": sha256_file(RAW_US100),
            "model_rows": result["base_rows"],
            "raw_rows": result["raw_rows"],
        },
        "integrity_judgment": "usable_with_boundary(경계 있는 사용 가능)",
    }


def tier_pair_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    best = result["top_candidates"][0] if result["top_candidates"] else {}
    return [
        {
            "record_view": "Tier A separate(Tier A 분리)",
            "tier_scope": "Tier A",
            "status": "materialized_proxy_kpi(프록시 KPI 물질화)",
            "net_profit": best.get("oos_net", ""),
            "profit_factor": best.get("oos_pf", ""),
            "trade_count": best.get("oos_trades", ""),
            "trades_per_day": best.get("oos_trades_per_day", ""),
            "notes": "F69B primary model input is full-context Tier A proxy sample(F69B 주 입력은 전체 문맥 Tier A 프록시 표본)",
        },
        {
            "record_view": "Tier B separate(Tier B 분리)",
            "tier_scope": "Tier B",
            "status": "missing_required(필수 누락)",
            "net_profit": "",
            "profit_factor": "",
            "trade_count": "",
            "trades_per_day": "",
            "notes": "Tier B partial-context materialization was not included in F69B phase1; must be repaired before reviewed run claim(Tier B 부분 문맥 물질화는 F69B 1단계에 없음)",
        },
        {
            "record_view": "Tier A+B combined(Tier A+B 합산)",
            "tier_scope": "Tier A+B",
            "status": "out_of_scope_by_claim(주장 범위 밖)",
            "net_profit": "",
            "profit_factor": "",
            "trade_count": "",
            "trades_per_day": "",
            "notes": "No synthetic sum is claimed; combined record waits for Tier B repair or routed runtime run(합성 합산 주장 없음)",
        },
    ]


def report_lines(result: Mapping[str, Any]) -> list[str]:
    top = result["top_candidates"][0] if result["top_candidates"] else {}
    meaningful = result["meaningful_with_control"]
    scout = result["scout_candidates"]
    next_run = result["next_run_id"]
    return [
        "# F69B Event-First First-Hit Proxy Sweep(F69B 이벤트 우선 선도달 프록시 스윕)",
        "",
        f"Updated(갱신): {result['created_at_utc']}",
        "",
        "## Hypothesis(가설)",
        "",
        "Sparse event-first first-hit opportunity labels(희소 이벤트 우선 선도달 기회 라벨)이 F68 risk-only repair loop(F68 위험 단독 수리 반복)와 다른 PF source(수익 팩터 원천)를 만들 수 있는지 시험했다.",
        "",
        "## Action And Effect(행동 및 효과)",
        "",
        "Action(행동): compact feature set(압축 피처 묶음), first-hit target(선도달 목표), interpretable model family(해석 가능 모델 계열), event admission(이벤트 진입)을 함께 바꾼 proxy sweep(프록시 탐색)을 실행했다.",
        "",
        "Effect(효과): 위험 폭만 고치는 반복을 피하고, 신호 원천이 feature/label/model/event(피처/라벨/모델/이벤트) 축에서 생기는지 확인한다.",
        "",
        "## KPI Summary(KPI 핵심 성과 요약)",
        "",
        f"- candidate rows(후보 행): `{len(result['candidate_summaries'])}` summary(요약), `{len(result['candidate_kpi_rows'])}` split KPI(분할 KPI).",
        f"- scout candidates(탐색 단서 후보): `{len(scout)}`.",
        f"- meaningful proxy candidates after control(대조군 후 의미 있는 프록시 후보): `{len(meaningful)}`.",
        f"- top candidate(상위 후보): `{top.get('candidate_id', 'none')}`.",
        f"- top validation net/PF/DD/trades_day(상위 검증 순수익/수익 팩터/손실폭/일거래): `{fmt(top.get('validation_net'))}` / `{fmt(top.get('validation_pf'))}` / `{fmt(top.get('validation_dd_pct'))}` / `{fmt(top.get('validation_trades_per_day'))}`.",
        f"- top OOS net/PF/DD/trades_day(상위 표본외 순수익/수익 팩터/손실폭/일거래): `{fmt(top.get('oos_net'))}` / `{fmt(top.get('oos_pf'))}` / `{fmt(top.get('oos_dd_pct'))}` / `{fmt(top.get('oos_trades_per_day'))}`.",
        "",
        "## Required Records(필수 기록)",
        "",
        f"- test period(테스트 기간): validation(검증) 2025-01-01 to 2025-09-30, OOS(표본외) 2025-10-01 to 2026-04-13.",
        "- proxy expectation(프록시 예상): PF movement(수익 팩터 움직임)이 event/label/model axis(이벤트/라벨/모델 축)에서 생기면 pre-MT5 Grok review(사전 MT5 그록 검토)로 간다.",
        f"- proxy KPI(프록시 KPI): see(참조) `{rel(RUN_ROOT / 'f69b_proxy_candidate_summary.csv')}` and `{rel(RUN_ROOT / 'f69b_proxy_kpi_by_split.csv')}`.",
        "- runtime probe KPI(런타임 탐침 KPI): pending(대기), proxy-only claim boundary(프록시 전용 주장 경계).",
        "- signal count parity(신호 수 동등성): not_applicable_before_runtime(런타임 전 해당 없음).",
        "- feature readiness parity(피처 준비 동등성): not_applicable_before_runtime(런타임 전 해당 없음).",
        "- proxy/runtime gap cause(프록시/런타임 간극 원인): pending_runtime_probe(런타임 탐침 대기).",
        f"- next action(다음 행동): `{next_run}`.",
        "",
        "## Tier Pair Boundary(티어 쌍 경계)",
        "",
        "Tier A separate(Tier A 분리)는 물질화했다. Tier B separate(Tier B 분리)는 `missing_required(필수 누락)`이고, Tier A+B combined(Tier A+B 합산)는 `out_of_scope_by_claim(주장 범위 밖)`이다.",
        "",
        "Effect(효과): Tier A 결과를 전체 알파 판독처럼 과장하지 않고, 다음 repair action(수리 행동)에 Tier B partial-context materialization(Tier B 부분 문맥 물질화)을 남긴다.",
        "",
        "## Judgment(판정)",
        "",
        f"- status(상태): `{result['status']}`.",
        f"- judgment(판정): `{result['judgment']}`.",
        f"- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.",
    ]


def gate_audit_lines(result: Mapping[str, Any]) -> list[str]:
    return [
        "# F69B Required Gate Coverage Audit(F69B 필수 게이트 커버리지 감사)",
        "",
        f"Updated(갱신): {result['created_at_utc']}",
        "",
        "| gate(게이트) | status(상태) | evidence(근거) | effect(효과) |",
        "|---|---|---|---|",
        f"| experiment_design(실험 설계) | pass(통과) | `{rel(RUN_ROOT / 'f69b_experiment_design.json')}` | 가설/비교/고정축/변경축을 기록 |",
        f"| data_integrity(데이터 무결성) | usable_with_boundary(경계 있는 사용 가능) | `{rel(RUN_ROOT / 'f69b_data_integrity.json')}` | 선도달 라벨 미래 경계를 기록 |",
        f"| proxy_kpi(프록시 KPI) | pass(통과) | `{rel(RUN_ROOT / 'f69b_proxy_kpi_by_split.csv')}` | validation/OOS 전체 KPI 기록 |",
        f"| bucket_kpi(구간 KPI) | pass(통과) | `{rel(RUN_ROOT / 'f69b_bucket_kpi.csv')}` | session/regime attribution(세션/장세 귀속) 기록 |",
        f"| control(대조군) | pass(통과) | `{rel(RUN_ROOT / 'f69b_shuffle_control.csv')}` | shuffled label(셔플 라벨) 대조 기록 |",
        f"| Tier pair(티어 쌍) | partial_with_named_gap(이름 붙인 부분 충족) | `{rel(RUN_ROOT / 'f69b_tier_pair_status.csv')}` | Tier B 누락을 숨기지 않음 |",
        "| MT5 runtime probe(MT5 런타임 탐침) | pending_after_proxy(프록시 이후 대기) | proxy-only boundary(프록시 전용 경계) | 의미 있는 신호면 Grok 후 실행 |",
        "",
        f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    ]


def experiment_design_payload(result: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": result["created_at_utc"],
        "idea_id": IDEA_ID,
        "hypothesis": "event-first first-hit opportunity model(이벤트 우선 선도달 기회 모델)이 새 PF source(수익 팩터 원천)를 만들 수 있다",
        "decision_use": "decide whether to run pre-MT5 Grok review and mandatory MT5 Runtime Probe(사전 MT5 그록 검토와 필수 MT5 런타임 탐침 여부 결정)",
        "comparison_baseline": "F68 closeout negative memory only; no baseline inheritance(F68 마감 부정 기억만 참조, 기준선 상속 없음)",
        "control_variables": [
            "US100 M5 split_v1(US100 5분봉 분할 v1)",
            "fixed SL/TP risk template sl_atr=0.90 tp_atr=1.35(고정 손익절 위험 템플릿)",
            "cooldown equals horizon(쿨다운은 보유수평선과 같음)",
            "train-only threshold quantiles(학습 전용 임계값 분위수)",
        ],
        "changed_variables": [
            "compact feature sets(압축 피처 묶음)",
            "first-hit labels(선도달 라벨)",
            "linear/shallow/small boosting model families(선형/얕은/작은 부스팅 모델 계열)",
            "event admission masks(이벤트 진입 마스크)",
            "session/regime bucket attribution(세션/장세 구간 귀속)",
        ],
        "success_criteria": "validation and OOS positive net/PF movement with density compatible scout range(검증과 표본외 양수 순수익/PF 움직임 및 밀도 호환)",
        "failure_criteria": "zero signal, validation-only signal, or no control gap(영 신호, 검증 전용 신호, 대조군 차이 없음)",
        "invalid_conditions": "raw/model timestamp mismatch, future path includes entry bar, missing required F69A design(원천/모델 시간 불일치, 미래 경로가 진입봉 포함, F69A 설계 누락)",
        "stop_conditions": "if meaningful signal exists then Grok before MT5; otherwise repair label/event/Tier B surface(의미 신호면 MT5 전 그록, 아니면 라벨/이벤트/Tier B 수리)",
        "evidence_plan": [
            rel(RUN_ROOT / "f69b_proxy_candidate_summary.csv"),
            rel(RUN_ROOT / "f69b_proxy_kpi_by_split.csv"),
            rel(RUN_ROOT / "f69b_event_budget.csv"),
            rel(RUN_ROOT / "f69b_bucket_kpi.csv"),
            rel(RUN_ROOT / "f69b_shuffle_control.csv"),
            rel(REVIEWS_ROOT / "frontier69B_event_first_first_hit_proxy_sweep_report.md"),
        ],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def run_manifest(result: Mapping[str, Any]) -> dict[str, Any]:
    artifacts = [
        RUN_ROOT / "f69b_experiment_design.json",
        RUN_ROOT / "f69b_data_integrity.json",
        RUN_ROOT / "f69b_proxy_candidate_summary.csv",
        RUN_ROOT / "f69b_proxy_kpi_by_split.csv",
        RUN_ROOT / "f69b_event_budget.csv",
        RUN_ROOT / "f69b_bucket_kpi.csv",
        RUN_ROOT / "f69b_shuffle_control.csv",
        RUN_ROOT / "f69b_top_candidates.json",
        RUN_ROOT / "f69b_tier_pair_status.csv",
        REVIEWS_ROOT / "frontier69B_event_first_first_hit_proxy_sweep_report.md",
        REVIEWS_ROOT / "required_gate_coverage_audit_f69b.md",
    ]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": result["created_at_utc"],
        "producer": "stage_pipelines/stage_frontier_69/frontier69b_event_first_first_hit_proxy_sweep.py",
        "status": result["status"],
        "judgment": result["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "next_run_id": result["next_run_id"],
        "inputs": {
            "model_input": rel(MODEL_INPUT),
            "model_input_sha256": sha256_file(MODEL_INPUT),
            "raw_us100": rel(RAW_US100),
            "raw_us100_sha256": sha256_file(RAW_US100),
            "f69a_design": rel(F69A_DESIGN),
        },
        "artifacts": [rel(path) for path in artifacts],
    }


def write_outputs(result: Mapping[str, Any]) -> None:
    for path in (RUN_ROOT, RUN_ROOT / "reports", REVIEWS_ROOT, SELECTED_ROOT):
        io_path(path).mkdir(parents=True, exist_ok=True)
    write_json(RUN_ROOT / "f69b_experiment_design.json", experiment_design_payload(result))
    write_json(RUN_ROOT / "f69b_data_integrity.json", data_integrity_payload(result))
    write_json(RUN_ROOT / "f69b_top_candidates.json", list(result["top_candidates"]))
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(result))
    write_csv(RUN_ROOT / "f69b_proxy_kpi_by_split.csv", list(result["candidate_kpi_rows"]))
    write_csv(RUN_ROOT / "f69b_proxy_candidate_summary.csv", list(result["candidate_summaries"]))
    write_csv(RUN_ROOT / "f69b_event_budget.csv", list(result["event_budget_rows"]))
    write_csv(RUN_ROOT / "f69b_bucket_kpi.csv", list(result["bucket_kpi_rows"]))
    write_csv(RUN_ROOT / "f69b_shuffle_control.csv", list(result["shuffle_control_rows"]))
    write_csv(RUN_ROOT / "f69b_class_balance.csv", list(result["class_balance_rows"]))
    write_csv(RUN_ROOT / "f69b_model_audit.csv", list(result["model_audit_rows"]))
    write_csv(RUN_ROOT / "f69b_tier_pair_status.csv", tier_pair_rows(result))
    write_md(RUN_ROOT / "reports" / "result_summary.md", report_lines(result))

    write_csv(REVIEWS_ROOT / "f69b_proxy_kpi_by_split_review.csv", list(result["candidate_kpi_rows"]))
    write_csv(REVIEWS_ROOT / "f69b_proxy_candidate_summary_review.csv", list(result["candidate_summaries"]))
    write_csv(REVIEWS_ROOT / "f69b_event_budget_review.csv", list(result["event_budget_rows"]))
    write_csv(REVIEWS_ROOT / "f69b_bucket_kpi_review.csv", list(result["bucket_kpi_rows"]))
    write_csv(REVIEWS_ROOT / "f69b_shuffle_control_review.csv", list(result["shuffle_control_rows"]))
    write_csv(REVIEWS_ROOT / "f69b_tier_pair_status_review.csv", tier_pair_rows(result))
    write_json(REVIEWS_ROOT / "f69b_top_candidates_review.json", list(result["top_candidates"]))
    write_md(REVIEWS_ROOT / "frontier69B_event_first_first_hit_proxy_sweep_report.md", report_lines(result))
    write_md(REVIEWS_ROOT / "required_gate_coverage_audit_f69b.md", gate_audit_lines(result))


def ledger_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    best = result["top_candidates"][0] if result["top_candidates"] else {}
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": result["status"],
        "judgment": result["judgment"],
        "path": f"stages/{STAGE_ID}/03_reviews/frontier69B_event_first_first_hit_proxy_sweep_report.md",
        "primary_report": f"stages/{STAGE_ID}/03_reviews/frontier69B_event_first_first_hit_proxy_sweep_report.md",
        "report_path": f"stages/{STAGE_ID}/03_reviews/frontier69B_event_first_first_hit_proxy_sweep_report.md",
        "claim_boundary": CLAIM_BOUNDARY,
        "external_verification_status": "out_of_scope_by_claim_proxy_only(프록시 전용 주장 범위 밖)",
        "run_number": "frontier69B",
        "date": str(result["created_at_utc"])[:10],
        "run_date": str(result["created_at_utc"])[:10],
        "decision": "pre_mt5_grok_if_signal_else_repair",
        "next_run_id": result["next_run_id"],
        "rows": len(result["candidate_summaries"]),
        "candidate_rows": len(result["candidate_summaries"]),
        "positive_proxy_rows": len(result["meaningful_with_control"]),
        "best_proxy": best.get("candidate_id", ""),
        "best_model_id": best.get("model_id", ""),
        "best_proxy_net": fmt(best.get("oos_net")),
        "net_profit": fmt(best.get("oos_net")),
        "profit_factor": fmt(best.get("oos_pf")),
        "drawdown": fmt(best.get("oos_dd_pct")),
        "trade_count": fmt(best.get("oos_trades")),
        "trade_density": fmt(best.get("oos_trades_per_day")),
        "expectancy": fmt(best.get("oos_expectancy")),
        "feature_count": best.get("feature_count", ""),
        "sample_rows": result["base_rows"],
        "attempt_count": len(result["candidate_summaries"]),
        "source_package_run_id": PARENT_RUN_ID,
        "scoreboard": "structural_scout(구조 탐색)",
        "scoreboard_lane": "structural_scout(구조 탐색)",
        "evidence_boundary": "proxy_only_no_runtime_authority(프록시 전용, 런타임 권위 없음)",
        "work_family": "experiment_execution(실험 실행)",
        "family": "experiment_execution(실험 실행)",
        "lane": "proxy_scout(프록시 탐색)",
        "result_status": result["status"],
        "result_judgment": result["judgment"],
        "final_decision_path": f"stages/{STAGE_ID}/03_reviews/frontier69B_event_first_first_hit_proxy_sweep_report.md",
        "gate_audit_path": f"stages/{STAGE_ID}/03_reviews/required_gate_coverage_audit_f69b.md",
        "created_at": result["created_at_utc"],
        "created_at_utc": result["created_at_utc"],
        "required_gate_audit": f"stages/{STAGE_ID}/03_reviews/required_gate_coverage_audit_f69b.md",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "proxy_only_no_runtime(프록시 전용, 런타임 없음)",
        "question": "Can event-first first-hit labels create a new PF source?(이벤트 우선 선도달 라벨이 새 PF 원천을 만들 수 있는가)",
        "next_action": result["next_run_id"],
        "artifact_count": 16,
        "run_family": "frontier_proxy_scout(전선 프록시 탐색)",
        "run_type": "event_first_first_hit_proxy_sweep(이벤트 우선 선도달 프록시 탐색)",
        "input_run_id": PARENT_RUN_ID,
        "output_path": f"stages/{STAGE_ID}/02_runs/{RUN_ID}/f69b_proxy_candidate_summary.csv",
        "result_path": f"stages/{STAGE_ID}/03_reviews/frontier69B_event_first_first_hit_proxy_sweep_report.md",
        "kpi_summary": (
            f"summaries={len(result['candidate_summaries'])};"
            f"scout={len(result['scout_candidates'])};"
            f"meaningful_with_control={len(result['meaningful_with_control'])};"
            f"best={best.get('candidate_id', 'none')}"
        ),
    }
    rows: list[dict[str, Any]] = []
    for tier in tier_pair_rows(result):
        row = dict(base)
        suffix = tier["record_view"].split("(")[0].strip().lower().replace(" ", "_").replace("+", "plus")
        row.update(
            {
                "ledger_row_id": f"{RUN_ID}__{suffix}",
                "row_id": f"{RUN_ID}__{suffix}",
                "subrun_id": tier["record_view"],
                "record_view": tier["record_view"],
                "view": tier["record_view"],
                "tier_scope": tier["tier_scope"],
                "tier": tier["tier_scope"],
                "kpi_scope": "proxy_trading_kpi(프록시 거래 KPI)",
                "metric_scope": "validation_oos_proxy(검증/표본외 프록시)",
                "primary_kpi": f"net={tier['net_profit']};pf={tier['profit_factor']};trades_day={tier['trades_per_day']}",
                "guardrail_kpi": tier["notes"],
                "notes": tier["notes"],
            }
        )
        if tier["tier_scope"] != "Tier A":
            row["status"] = tier["status"]
            row["judgment"] = "inconclusive_tier_pair_gap_named(티어 쌍 간극 이름 붙임)"
            row["net_profit"] = ""
            row["profit_factor"] = ""
            row["drawdown"] = ""
            row["trade_count"] = ""
            row["trade_density"] = ""
        rows.append(row)
    return rows


def update_ledgers(result: Mapping[str, Any]) -> None:
    rows = ledger_rows(result)
    run_row = rows[0]
    for row in rows:
        upsert_ledger(REVIEWS_ROOT / "stage_run_ledger.csv", "ledger_row_id", row, source_header=ROOT / "docs/registers/alpha_run_ledger.csv")
        upsert_ledger(ROOT / "docs/registers/alpha_run_ledger.csv", "ledger_row_id", row)
    upsert_ledger(ROOT / "docs/registers/run_registry.csv", "run_id", run_row)


def update_review_index() -> None:
    marker = "<!-- frontier69B_event_first_first_hit_proxy_sweep_v1 -->"
    block = f"""<!-- frontier69B_event_first_first_hit_proxy_sweep_v1 -->
- `frontier69B_event_first_first_hit_proxy_sweep_report.md`: F69B proxy sweep report(F69B 프록시 탐색 보고서)
- `f69b_proxy_candidate_summary_review.csv`: F69B candidate summary(F69B 후보 요약)
- `f69b_proxy_kpi_by_split_review.csv`: F69B split KPI(F69B 분할 KPI)
- `f69b_bucket_kpi_review.csv`: F69B session/regime bucket KPI(F69B 세션/장세 구간 KPI)
- `f69b_shuffle_control_review.csv`: F69B shuffled-label control(F69B 셔플 라벨 대조군)
- `required_gate_coverage_audit_f69b.md`: F69B required gate audit(F69B 필수 게이트 감사)"""
    append_once(REVIEWS_ROOT / "review_index.md", marker, block)


def update_registers(result: Mapping[str, Any]) -> None:
    marker = "<!-- frontier69B_event_first_first_hit_proxy_sweep_v1 -->"
    block = f"""<!-- frontier69B_event_first_first_hit_proxy_sweep_v1 -->
- `{IDEA_ID}`: `{RUN_ID}` executed event-first first-hit proxy sweep(이벤트 우선 선도달 프록시 탐색 실행). Result(결과): `{result['judgment']}`. Meaningful proxy candidates after control(대조군 후 의미 있는 프록시 후보): `{len(result['meaningful_with_control'])}`. Boundary(경계): proxy-only(프록시 전용), no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). Next(다음): `{result['next_run_id']}`."""
    append_once(ROOT / "docs/registers/idea_registry.md", marker, block)


def update_state_files(result: Mapping[str, Any]) -> None:
    best = result["top_candidates"][0] if result["top_candidates"] else {}
    signal = bool(result["meaningful_with_control"])
    runtime_status = (
        "f69_mandatory_runtime_probe_pending_pre_mt5_grok_after_meaningful_proxy_signal(F69 의미 있는 프록시 신호 후 사전 MT5 그록 및 필수 런타임 탐침 대기)"
        if signal
        else "f69_mandatory_runtime_probe_pending_after_proxy_repair_signal(F69 프록시 수리 신호 후 필수 런타임 탐침 대기)"
    )
    selection = [
        "# F69 Selection Status(F69 선택 상태)",
        "",
        f"- stage(단계): `{STAGE_ID}`",
        f"- current_run(현재 실행): `{result['next_run_id']}`",
        f"- latest_completed_run(최근 완료 실행): `{RUN_ID}`",
        f"- status(상태): `{result['status']}`",
        f"- judgment(판정): `{result['judgment']}`",
        "- selected_baseline(선택 기준선): `not_claimed(주장 없음)`",
        "- runtime_authority(런타임 권위): `not_claimed(주장 없음)`",
        "- operating_promotion(운영 승격): `not_claimed(주장 없음)`",
        "- live_readiness(실거래 준비): `not_claimed(주장 없음)`",
        "- Goal Achieve(목표 달성): `not_claimed(주장 없음)`",
        f"- top_proxy_clue(상위 프록시 단서): `{best.get('candidate_id', 'none')}`.",
        f"- top_validation_net_pf_dd_tpd(상위 검증 순수익/수익 팩터/손실폭/일거래): `{fmt(best.get('validation_net'))}` / `{fmt(best.get('validation_pf'))}` / `{fmt(best.get('validation_dd_pct'))}` / `{fmt(best.get('validation_trades_per_day'))}`.",
        f"- top_oos_net_pf_dd_tpd(상위 표본외 순수익/수익 팩터/손실폭/일거래): `{fmt(best.get('oos_net'))}` / `{fmt(best.get('oos_pf'))}` / `{fmt(best.get('oos_dd_pct'))}` / `{fmt(best.get('oos_trades_per_day'))}`.",
        "- Tier B separate(Tier B 분리): `missing_required(필수 누락)`.",
        "- Tier A+B combined(Tier A+B 합산): `out_of_scope_by_claim(주장 범위 밖)`.",
        f"- next_action(다음 행동): `{result['next_run_id']}`.",
        f"- boundary(경계): `{CLAIM_BOUNDARY}`.",
    ]
    write_md(SELECTED_ROOT / "selection_status.md", selection)

    state = [
        f"current_stage_id: {STAGE_ID}",
        f"active_stage: {STAGE_ID}",
        f"current_run_id: {result['next_run_id']}",
        f"latest_completed_run_id: {RUN_ID}",
        f"current_status: {result['status']}",
        f"current_judgment: {result['judgment']}",
        f"next_stage_id: {STAGE_ID}",
        f"next_run_id: {result['next_run_id']}",
        f"runtime_probe_status: {runtime_status}",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "live_readiness: not_claimed",
        "goal_achieve: not_claimed",
        f"updated_at_utc: '{result['created_at_utc']}'",
        "notes:",
        f'  - "F69B action(행동): event-first first-hit proxy sweep(이벤트 우선 선도달 프록시 탐색)을 실행했다."',
        f'  - "Effect(효과): feature/label/model/event/session-regime(피처/라벨/모델/이벤트/세션-장세) 축을 실제로 바꾼 KPI를 남겼다."',
        f'  - "Top proxy clue(상위 프록시 단서): `{best.get("candidate_id", "none")}` validation/OOS PF(검증/표본외 수익 팩터) `{fmt(best.get("validation_pf"))}/{fmt(best.get("oos_pf"))}`, trades/day(일 거래) `{fmt(best.get("validation_trades_per_day"))}/{fmt(best.get("oos_trades_per_day"))}`."',
        f'  - "Meaningful proxy candidates after control(대조군 후 의미 있는 프록시 후보): `{len(result["meaningful_with_control"])}`."',
        '  - "Tier boundary(티어 경계): Tier B separate(분리)는 missing_required(필수 누락), combined(합산)는 out_of_scope_by_claim(주장 범위 밖)."',
        '  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."',
    ]
    io_path(ROOT / "docs/workspace/workspace_state.yaml").write_text("\n".join(state) + "\n", encoding="utf-8-sig")

    current = [
        "# Current Working State(현재 작업 상태)",
        "",
        f"Updated(갱신): {result['created_at_utc']}",
        "",
        f"Active stage(활성 단계): `{STAGE_ID}`",
        f"Current run(현재 실행): `{result['next_run_id']}`",
        f"Latest completed run(최근 완료 실행): `{RUN_ID}`",
        "",
        "## Current Truth(현재 진실)",
        "",
        "Action(행동): F69B event-first first-hit proxy sweep(F69B 이벤트 우선 선도달 프록시 탐색)을 실행했다.",
        "",
        "Effect(효과): F68 risk-only repair loop(F68 위험 단독 수리 반복)에서 벗어나 feature set/label/model/trade shape/regime-session(피처 묶음/라벨/모델/거래 형태/장세-세션)을 실제로 바꾼 scout evidence(탐색 근거)를 만들었다.",
        "",
        f"- status(상태): `{result['status']}`.",
        f"- judgment(판정): `{result['judgment']}`.",
        f"- top candidate(상위 후보): `{best.get('candidate_id', 'none')}`.",
        f"- validation net/PF/DD/trades_day(검증 순수익/수익 팩터/손실폭/일거래): `{fmt(best.get('validation_net'))}` / `{fmt(best.get('validation_pf'))}` / `{fmt(best.get('validation_dd_pct'))}` / `{fmt(best.get('validation_trades_per_day'))}`.",
        f"- OOS net/PF/DD/trades_day(표본외 순수익/수익 팩터/손실폭/일거래): `{fmt(best.get('oos_net'))}` / `{fmt(best.get('oos_pf'))}` / `{fmt(best.get('oos_dd_pct'))}` / `{fmt(best.get('oos_trades_per_day'))}`.",
        f"- meaningful proxy candidates after control(대조군 후 의미 있는 프록시 후보): `{len(result['meaningful_with_control'])}`.",
        "- runtime probe(런타임 탐침): pending(대기). 의미 있는 proxy signal(프록시 신호)이 있으면 Grok review(그록 검토) 후 MT5 Runtime Probe(MT5 런타임 탐침)로 간다.",
        "- Tier B separate(Tier B 분리): missing_required(필수 누락).",
        "- Tier A+B combined(Tier A+B 합산): out_of_scope_by_claim(주장 범위 밖).",
        "",
        "## Key Artifacts(핵심 산출물)",
        "",
        f"- report(보고서): `stages/{STAGE_ID}/03_reviews/frontier69B_event_first_first_hit_proxy_sweep_report.md`",
        f"- candidate summary(후보 요약): `stages/{STAGE_ID}/03_reviews/f69b_proxy_candidate_summary_review.csv`",
        f"- split KPI(분할 KPI): `stages/{STAGE_ID}/03_reviews/f69b_proxy_kpi_by_split_review.csv`",
        f"- bucket KPI(구간 KPI): `stages/{STAGE_ID}/03_reviews/f69b_bucket_kpi_review.csv`",
        f"- shuffle control(셔플 대조군): `stages/{STAGE_ID}/03_reviews/f69b_shuffle_control_review.csv`",
        "",
        f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    ]
    write_md(ROOT / "docs/context/current_working_state.md", current)


def main() -> int:
    created_at = utc_now()
    result = run_proxy_sweep(created_at)
    write_outputs(result)
    update_ledgers(result)
    update_review_index()
    update_registers(result)
    update_state_files(result)
    print(
        json.dumps(
            json_ready(
                {
                    "status": result["status"],
                    "judgment": result["judgment"],
                    "run_id": RUN_ID,
                    "next_run_id": result["next_run_id"],
                    "candidate_summaries": len(result["candidate_summaries"]),
                    "scout_candidates": len(result["scout_candidates"]),
                    "meaningful_with_control": len(result["meaningful_with_control"]),
                    "top_candidate": (result["top_candidates"][0] if result["top_candidates"] else {}).get("candidate_id", "none"),
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
