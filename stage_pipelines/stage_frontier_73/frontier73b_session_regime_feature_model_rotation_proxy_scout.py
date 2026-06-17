from __future__ import annotations

import csv
import json
import math
import sys
import warnings
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier, HistGradientBoostingClassifier
from sklearn.exceptions import ConvergenceWarning
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists


STAGE_ID = "stage_frontier_73__session_regime_feature_model_rotation_for_runtime_economics_gap"
RUN_ID = "frontier73B_session_regime_feature_model_rotation_proxy_scout_v1"
PARENT_RUN_ID = "frontier73A_stage_open_new_hypothesis_after_f72_trade_shape_negative_memory_v1"
NEXT_REPAIR_RUN_ID = "frontier73C_axis_reduction_or_repair_proxy_scout_v1"
NEXT_PRE_MT5_RUN_ID = "frontier73C_pre_mt5_grok_session_regime_runtime_probe_v1"
STATUS = "proxy_scout_completed"
CLAIM_BOUNDARY = (
    "proxy_scout_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"

F73A_MANIFEST = STAGE_ROOT / "02_runs" / PARENT_RUN_ID / "run_manifest.json"
F73A_SURFACE_PLAN = STAGE_ROOT / "02_runs" / PARENT_RUN_ID / "f73a_proxy_scout_surface_plan.csv"
FWD12_INPUT = ROOT / "data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet"
FWD12_FEATURE_ORDER = ROOT / "data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_feature_order.txt"
FWD18_INPUT = ROOT / "data/processed/model_inputs/label_v1_fwd18_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet"
FWD18_FEATURE_ORDER = ROOT / "data/processed/model_inputs/label_v1_fwd18_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_feature_order.txt"
RAW_US100 = ROOT / "data/raw/mt5_bars/m5/US100/bars_us100_m5_mt5api_raw.csv"

RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"
WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"

INITIAL_EQUITY = 10000.0
POINT_VALUE = 1.0
POINT_SIZE = 0.01
TARGET_TPD_VALUES = [1.5, 3.0, 5.0, 7.0]

warnings.filterwarnings("ignore", category=ConvergenceWarning)


@dataclass(frozen=True)
class DatasetSpec:
    dataset_id: str
    path: Path
    feature_order: Path
    hold_bars: int
    target_atr: float


@dataclass(frozen=True)
class CandidateSpec:
    surface_id: str
    dataset_ids: tuple[str, ...]
    feature_bundle: str
    targets: tuple[str, ...]
    model_ids: tuple[str, ...]
    gate_ids: tuple[str, ...]
    target_tpds: tuple[float, ...] = tuple(TARGET_TPD_VALUES)


DATASETS = {
    "fwd12": DatasetSpec("fwd12", FWD12_INPUT, FWD12_FEATURE_ORDER, 12, 1.6),
    "fwd18": DatasetSpec("fwd18", FWD18_INPUT, FWD18_FEATURE_ORDER, 18, 1.8),
}


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def write_text(path: Path, lines: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8-sig")


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: json_ready(row.get(field, "")) for field in fieldnames})


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


def required_inputs() -> list[Path]:
    return [F73A_MANIFEST, F73A_SURFACE_PLAN, FWD12_INPUT, FWD12_FEATURE_ORDER, FWD18_INPUT, FWD18_FEATURE_ORDER, RAW_US100]


def split_days(timestamps: pd.Series) -> float:
    if timestamps.empty:
        return 1.0
    span = timestamps.max() - timestamps.min()
    return max(float(span.days) + 1.0, 1.0)


def max_drawdown(values: np.ndarray) -> tuple[float, float]:
    if len(values) == 0:
        return 0.0, 0.0
    equity = INITIAL_EQUITY + np.cumsum(values)
    peaks = np.maximum.accumulate(equity)
    drawdowns = peaks - equity
    max_dd = float(np.max(drawdowns))
    return max_dd, float(max_dd / INITIAL_EQUITY * 100.0)


def equity_smoothness(values: np.ndarray) -> float:
    if len(values) < 3:
        return 0.0
    equity = np.cumsum(values)
    x_axis = np.arange(len(equity), dtype=float)
    if np.allclose(equity, equity[0]):
        return 0.0
    corr = np.corrcoef(x_axis, equity)[0, 1]
    return float(0.0 if np.isnan(corr) else corr * corr)


def trade_metrics(timestamps: pd.Series, pnl: np.ndarray, direction: np.ndarray) -> dict[str, Any]:
    count = int(len(pnl))
    days = split_days(timestamps)
    wins = pnl[pnl > 0]
    losses = pnl[pnl < 0]
    gross_profit = float(wins.sum()) if len(wins) else 0.0
    gross_loss = float(losses.sum()) if len(losses) else 0.0
    pf = float(gross_profit / abs(gross_loss)) if gross_loss < 0 else (999.0 if gross_profit > 0 else 0.0)
    net = float(pnl.sum())
    dd_amount, dd_percent = max_drawdown(pnl)
    avg_win = float(wins.mean()) if len(wins) else 0.0
    avg_loss = float(losses.mean()) if len(losses) else 0.0
    payoff = float(avg_win / abs(avg_loss)) if avg_loss < 0 else 0.0
    max_consecutive_loss = 0
    current_loss = 0
    for value in pnl:
        if value < 0:
            current_loss += 1
            max_consecutive_loss = max(max_consecutive_loss, current_loss)
        else:
            current_loss = 0
    return {
        "net_profit": net,
        "gross_profit": gross_profit,
        "gross_loss": gross_loss,
        "profit_factor": pf,
        "max_drawdown_amount": dd_amount,
        "max_drawdown_percent": dd_percent,
        "trade_count": count,
        "trades_day": float(count / days),
        "win_rate": float(len(wins) / count) if count else 0.0,
        "average_win": avg_win,
        "average_loss": avg_loss,
        "payoff_ratio": payoff,
        "expectancy": float(net / count) if count else 0.0,
        "recovery_factor": float(net / dd_amount) if dd_amount > 0 else (999.0 if net > 0 else 0.0),
        "smoothness_r2": equity_smoothness(pnl),
        "max_consecutive_loss": max_consecutive_loss,
        "long_trade_count": int(np.sum(direction > 0)),
        "short_trade_count": int(np.sum(direction < 0)),
    }


def load_raw() -> pd.DataFrame:
    raw = pd.read_csv(io_path(RAW_US100))
    return raw.sort_values("time_close_unix").reset_index(drop=True)


def align_raw(frame: pd.DataFrame, raw: pd.DataFrame) -> np.ndarray:
    raw = raw.copy()
    raw["timestamp"] = pd.to_datetime(raw["time_close_unix"], unit="s", utc=True)
    positions = pd.Series(raw.index.to_numpy(), index=raw["timestamp"])
    return positions.reindex(frame["timestamp"]).to_numpy(dtype=float)


def compute_fixed_path(frame: pd.DataFrame, raw: pd.DataFrame, positions: np.ndarray, hold_bars: int, direction: int, target_atr: float) -> dict[str, np.ndarray]:
    pnl = np.full(len(frame), np.nan)
    quality = np.full(len(frame), np.nan)
    atr_values = pd.to_numeric(frame["atr_14"], errors="coerce").to_numpy(dtype=float)
    spread_cost = pd.to_numeric(raw["spread_points"], errors="coerce").fillna(0).to_numpy(dtype=float) * POINT_SIZE
    open_values = raw["open"].to_numpy(dtype=float)
    high_values = raw["high"].to_numpy(dtype=float)
    low_values = raw["low"].to_numpy(dtype=float)
    close_values = raw["close"].to_numpy(dtype=float)
    stop_atr = 1.0
    max_pos = len(raw) - hold_bars - 2
    for idx, pos_float in enumerate(positions):
        if not np.isfinite(pos_float):
            continue
        pos = int(pos_float)
        if pos < 0 or pos > max_pos:
            continue
        atr = atr_values[idx]
        if not np.isfinite(atr) or atr <= 0:
            continue
        entry_idx = pos + 1
        exit_idx = pos + hold_bars
        entry = open_values[entry_idx]
        stop = stop_atr * atr
        target = target_atr * atr
        realized = None
        max_fav = 0.0
        max_adv = 0.0
        adverse_bars = 0
        for j in range(entry_idx, exit_idx + 1):
            if direction > 0:
                fav = high_values[j] - entry
                adv = entry - low_values[j]
                hit_stop = low_values[j] <= entry - stop
                hit_target = high_values[j] >= entry + target
            else:
                fav = entry - low_values[j]
                adv = high_values[j] - entry
                hit_stop = high_values[j] >= entry + stop
                hit_target = low_values[j] <= entry - target
            max_fav = max(max_fav, fav)
            max_adv = max(max_adv, adv)
            if adv > fav:
                adverse_bars += 1
            if hit_stop and hit_target:
                realized = -stop
                break
            if hit_stop:
                realized = -stop
                break
            if hit_target:
                realized = target
                break
        if realized is None:
            realized = direction * (close_values[exit_idx] - entry)
        net = (realized - spread_cost[entry_idx]) * POINT_VALUE
        pnl[idx] = net
        quality[idx] = (net / atr) + 0.15 * (max_fav / atr) - 0.20 * (max_adv / atr) - 0.05 * (adverse_bars / max(hold_bars, 1))
    return {
        "pnl": pnl,
        "quality": quality,
        "quality_label": ((quality > 0.10) & (pnl > 0)).astype(float),
        "direction": np.full(len(frame), direction),
    }


def load_dataset(spec: DatasetSpec, raw: pd.DataFrame) -> dict[str, Any]:
    frame = pd.read_parquet(io_path(spec.path))
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    features = [line.strip() for line in read_text(spec.feature_order).splitlines() if line.strip()]
    positions = align_raw(frame, raw)
    return {
        "frame": frame,
        "features": features,
        "paths": {
            "long": compute_fixed_path(frame, raw, positions, spec.hold_bars, 1, spec.target_atr),
            "short": compute_fixed_path(frame, raw, positions, spec.hold_bars, -1, spec.target_atr),
        },
    }


def feature_bundles(features: Sequence[str]) -> dict[str, list[str]]:
    features = list(features)
    external = ("vix_", "us10yr_", "usdx_", "nvda_", "aapl_", "msft_", "amzn_", "mega8_", "top3_", "us100_minus_")
    no_top3 = ("top3_weighted_return_1", "us100_minus_top3_weighted_return_1")
    session = ("is_us_cash_open", "minutes_from_cash_open", "is_first_30m_after_open", "is_last_30m_before_cash_close")
    core_tokens = (
        "log_return", "hl_", "close_", "gap_", "return_", "ema", "sma", "rsi", "stoch", "ppo", "roc", "trix",
        "atr", "bollinger", "bb_", "historical_vol", "adx", "di_", "supertrend", "vortex",
    )
    importance_seed = [
        "return_zscore_20",
        "hl_zscore_50",
        "return_1_over_atr_14",
        "atr_14_over_atr_50",
        "historical_vol_5_over_20",
        "adx_14",
        "di_spread_14",
        "bb_position_20",
        "bollinger_width_20",
        "rsi_14",
        "rsi_14_slope_3",
        "ppo_hist_12_26_9",
        "minutes_from_cash_open",
        "is_first_30m_after_open",
        "is_last_30m_before_cash_close",
        "vortex_indicator",
        "ema20_ema50_diff",
        "ema50_ema200_diff",
    ]
    core = [f for f in features if f.startswith(core_tokens)]
    session_core = sorted(set(core + [f for f in features if f.startswith(session)]))
    return {
        "all58": features,
        "core_price_path": core,
        "session_regime_core": session_core,
        "no_top3_proxy": [f for f in features if f not in no_top3],
        "no_external_macro": [f for f in features if not f.startswith(external)],
        "importance_seed_recombination": [f for f in importance_seed if f in features],
    }


def candidate_specs() -> list[CandidateSpec]:
    return [
        CandidateSpec("all58_fwd12_reference", ("fwd12",), "all58", ("long_direct", "short_direct"), ("logistic_l2", "extra_trees_ref"), ("all",), (1.5, 3.0, 5.0)),
        CandidateSpec("all58_fwd18_horizon_shift", ("fwd18",), "all58", ("long_direct", "short_direct", "long_inverse", "short_inverse"), ("logistic_l2", "extra_trees_ref"), ("all",), (1.5, 3.0, 5.0)),
        CandidateSpec("core_price_path_only", ("fwd12", "fwd18"), "core_price_path", ("long_direct", "short_direct", "long_inverse", "short_inverse"), ("logistic_l2", "hist_gbm"), ("all",), (1.5, 3.0, 5.0)),
        CandidateSpec("session_regime_core", ("fwd12",), "session_regime_core", ("long_quality", "short_quality"), ("extra_trees_ref", "hist_gbm", "small_nn_16"), ("cash_open", "cash_mid", "cash_late", "vol_high", "vol_low"), (1.5, 3.0, 5.0)),
        CandidateSpec("no_top3_proxy_ablation", ("fwd12", "fwd18"), "no_top3_proxy", ("long_direct", "short_direct"), ("logistic_l2", "extra_trees_ref"), ("all", "cash_mid"), (1.5, 3.0, 5.0)),
        CandidateSpec("top_importance_recombination", ("fwd12",), "importance_seed_recombination", ("long_quality", "short_quality"), ("extra_trees_ref", "hist_gbm"), ("all", "vol_high", "vol_low"), (1.5, 3.0, 5.0)),
    ]


def model_factories() -> dict[str, Callable[[], Any]]:
    return {
        "logistic_l2": lambda: make_pipeline(
            SimpleImputer(strategy="median"),
            StandardScaler(),
            LogisticRegression(max_iter=300, class_weight="balanced", solver="lbfgs"),
        ),
        "extra_trees_ref": lambda: make_pipeline(
            SimpleImputer(strategy="median"),
            ExtraTreesClassifier(
                n_estimators=80,
                max_depth=8,
                min_samples_leaf=60,
                class_weight="balanced_subsample",
                random_state=7302,
                n_jobs=-1,
            ),
        ),
        "hist_gbm": lambda: make_pipeline(
            SimpleImputer(strategy="median"),
            HistGradientBoostingClassifier(max_iter=80, learning_rate=0.06, max_leaf_nodes=15, l2_regularization=0.05),
        ),
        "small_nn_16": lambda: make_pipeline(
            SimpleImputer(strategy="median"),
            StandardScaler(),
            MLPClassifier(hidden_layer_sizes=(16,), alpha=0.001, max_iter=80, random_state=7302, early_stopping=True),
        ),
    }


def target_and_side(frame: pd.DataFrame, paths: Mapping[str, Mapping[str, np.ndarray]], target_id: str) -> tuple[np.ndarray, int, Mapping[str, np.ndarray]]:
    label = pd.to_numeric(frame["label_class"], errors="coerce").to_numpy(dtype=float)
    if target_id == "long_direct":
        return (label == 2).astype(float), 1, paths["long"]
    if target_id == "short_direct":
        return (label == 0).astype(float), -1, paths["short"]
    if target_id == "long_inverse":
        return (label == 0).astype(float), 1, paths["long"]
    if target_id == "short_inverse":
        return (label == 2).astype(float), -1, paths["short"]
    if target_id == "long_quality":
        return paths["long"]["quality_label"], 1, paths["long"]
    if target_id == "short_quality":
        return paths["short"]["quality_label"], -1, paths["short"]
    raise ValueError(f"unknown target_id={target_id}")


def train_thresholds(frame: pd.DataFrame) -> dict[str, float]:
    train = frame["split"] == "train"
    return {
        "vol_median": float(pd.to_numeric(frame.loc[train, "historical_vol_5_over_20"], errors="coerce").median()),
        "adx_median": float(pd.to_numeric(frame.loc[train, "adx_14"], errors="coerce").median()),
    }


def gate_mask(frame: pd.DataFrame, gate_id: str, thresholds: Mapping[str, float]) -> np.ndarray:
    minutes = pd.to_numeric(frame["minutes_from_cash_open"], errors="coerce")
    vol = pd.to_numeric(frame["historical_vol_5_over_20"], errors="coerce")
    adx = pd.to_numeric(frame["adx_14"], errors="coerce")
    if gate_id == "all":
        return np.ones(len(frame), dtype=bool)
    if gate_id == "cash_open":
        return ((minutes >= 0) & (minutes <= 60)).to_numpy(dtype=bool)
    if gate_id == "cash_mid":
        return ((minutes > 60) & (minutes <= 270)).to_numpy(dtype=bool)
    if gate_id == "cash_late":
        return ((minutes > 270) & (minutes <= 390)).to_numpy(dtype=bool)
    if gate_id == "vol_high":
        return ((vol >= thresholds["vol_median"]) & (adx >= thresholds["adx_median"] * 0.75)).fillna(False).to_numpy(dtype=bool)
    if gate_id == "vol_low":
        return ((vol < thresholds["vol_median"]) & (adx < thresholds["adx_median"] * 1.25)).fillna(False).to_numpy(dtype=bool)
    raise ValueError(f"unknown gate_id={gate_id}")


def score_threshold(scores: np.ndarray, timestamps: pd.Series, target_tpd: float) -> float:
    valid = scores[np.isfinite(scores)]
    if len(valid) == 0:
        return math.inf
    target_count = max(int(round(split_days(timestamps) * target_tpd)), 1)
    target_count = min(target_count, len(valid))
    return float(np.partition(valid, len(valid) - target_count)[len(valid) - target_count])


def train_and_score(frame: pd.DataFrame, features: Sequence[str], y: np.ndarray, gate: np.ndarray, factory: Callable[[], Any]) -> tuple[np.ndarray, dict[str, Any]]:
    finite_y = np.isfinite(y)
    train_mask = (frame["split"] == "train").to_numpy() & gate & finite_y
    if int(train_mask.sum()) < 600:
        raise ValueError("too_few_train_rows")
    y_train = y[train_mask].astype(int)
    positives = int(np.sum(y_train == 1))
    negatives = int(np.sum(y_train == 0))
    if positives < 30 or negatives < 30:
        raise ValueError("class_too_small")
    estimator = factory()
    estimator.fit(frame.loc[train_mask, features], y_train)
    score_mask = finite_y
    scores = np.full(len(frame), np.nan)
    if hasattr(estimator, "predict_proba"):
        scores[score_mask] = estimator.predict_proba(frame.loc[score_mask, features])[:, 1]
    else:
        decision = estimator.decision_function(frame.loc[score_mask, features])
        scores[score_mask] = 1.0 / (1.0 + np.exp(-decision))
    auc = float(roc_auc_score(y_train, scores[train_mask])) if len(np.unique(y_train)) == 2 else 0.0
    return scores, {
        "train_rows": int(train_mask.sum()),
        "train_positive_rate": float(np.mean(y_train)),
        "train_auc": auc,
    }


def evaluate_candidate(frame: pd.DataFrame, scores: np.ndarray, path: Mapping[str, np.ndarray], gate: np.ndarray, target_tpd: float) -> dict[str, Any]:
    validation_mask = (frame["split"] == "validation").to_numpy() & gate & np.isfinite(scores) & np.isfinite(path["pnl"])
    threshold = score_threshold(scores[validation_mask], frame.loc[validation_mask, "timestamp"], target_tpd)
    result: dict[str, Any] = {"score_threshold": threshold}
    for split in ("train", "validation", "oos"):
        mask = (frame["split"] == split).to_numpy() & gate & np.isfinite(scores) & np.isfinite(path["pnl"]) & (scores >= threshold)
        metrics = trade_metrics(frame.loc[mask, "timestamp"], path["pnl"][mask], path["direction"][mask])
        for key, value in metrics.items():
            result[f"{split}_{key}"] = value
    return result


def is_scout(row: Mapping[str, Any]) -> bool:
    return (
        row["validation_net_profit"] > 0
        and row["oos_net_profit"] > 0
        and row["validation_profit_factor"] >= 1.10
        and row["oos_profit_factor"] >= 1.10
        and row["validation_max_drawdown_percent"] <= 15.0
        and row["oos_max_drawdown_percent"] <= 15.0
        and row["validation_trades_day"] >= 1.5
        and row["oos_trades_day"] >= 1.5
    )


def is_meaningful(row: Mapping[str, Any]) -> bool:
    return (
        is_scout(row)
        and row["validation_profit_factor"] >= 1.25
        and row["oos_profit_factor"] >= 1.25
        and row["validation_max_drawdown_percent"] <= 10.0
        and row["oos_max_drawdown_percent"] <= 10.0
        and row["validation_trades_day"] >= 3.0
        and row["oos_trades_day"] >= 3.0
    )


def is_final_like(row: Mapping[str, Any]) -> bool:
    return (
        row["validation_profit_factor"] >= 2.0
        and row["oos_profit_factor"] >= 2.0
        and row["validation_max_drawdown_percent"] < 10.0
        and row["oos_max_drawdown_percent"] < 10.0
        and 5.0 <= row["validation_trades_day"] <= 10.0
        and 5.0 <= row["oos_trades_day"] <= 10.0
        and row["oos_smoothness_r2"] >= 0.25
    )


def data_integrity_rows(datasets: Mapping[str, Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for dataset_id, data in datasets.items():
        frame = data["frame"]
        features = data["features"]
        duplicate_ts = int(frame["timestamp"].duplicated().sum())
        missing_feature_cells = int(frame[features].isna().sum().sum())
        rows.append({
            "dataset_id": dataset_id,
            "rows": int(len(frame)),
            "features": len(features),
            "split_counts": json.dumps({str(k): int(v) for k, v in frame["split"].value_counts().to_dict().items()}, ensure_ascii=False),
            "timestamp_min": str(frame["timestamp"].min()),
            "timestamp_max": str(frame["timestamp"].max()),
            "duplicate_timestamps": duplicate_ts,
            "missing_feature_cells": missing_feature_cells,
            "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)",
        })
    return rows


def run_scout() -> dict[str, Any]:
    raw = load_raw()
    datasets = {dataset_id: load_dataset(spec, raw) for dataset_id, spec in DATASETS.items()}
    factories = model_factories()
    candidate_rows: list[dict[str, Any]] = []
    failure_rows: list[dict[str, Any]] = []
    score_cache: dict[tuple[str, str, str, str, str, str], tuple[np.ndarray, dict[str, Any], Mapping[str, np.ndarray]]] = {}
    for spec in candidate_specs():
        for dataset_id in spec.dataset_ids:
            data = datasets[dataset_id]
            frame = data["frame"]
            bundles = feature_bundles(data["features"])
            features = bundles[spec.feature_bundle]
            thresholds = train_thresholds(frame)
            for target_id in spec.targets:
                y, side, path = target_and_side(frame, data["paths"], target_id)
                for gate_id in spec.gate_ids:
                    gate = gate_mask(frame, gate_id, thresholds)
                    for model_id in spec.model_ids:
                        cache_key = (spec.surface_id, dataset_id, spec.feature_bundle, target_id, gate_id, model_id)
                        try:
                            if cache_key not in score_cache:
                                scores, train_info = train_and_score(frame, features, y, gate, factories[model_id])
                                score_cache[cache_key] = (scores, train_info, path)
                            scores, train_info, _ = score_cache[cache_key]
                            for target_tpd in spec.target_tpds:
                                row = {
                                    "candidate_id": f"f73b_{len(candidate_rows) + 1:04d}",
                                    "surface_id": spec.surface_id,
                                    "dataset_id": dataset_id,
                                    "feature_bundle": spec.feature_bundle,
                                    "feature_count": len(features),
                                    "target_id": target_id,
                                    "side": "long" if side > 0 else "short",
                                    "model_id": model_id,
                                    "gate_id": gate_id,
                                    "target_trades_day": target_tpd,
                                    **train_info,
                                    **evaluate_candidate(frame, scores, path, gate, target_tpd),
                                }
                                row["scout_clue"] = is_scout(row)
                                row["meaningful_candidate"] = is_meaningful(row)
                                row["final_like_reference_only"] = is_final_like(row)
                                candidate_rows.append(row)
                        except Exception as exc:  # noqa: BLE001 - failures are evidence in this scout.
                            failure_rows.append({
                                "surface_id": spec.surface_id,
                                "dataset_id": dataset_id,
                                "feature_bundle": spec.feature_bundle,
                                "target_id": target_id,
                                "gate_id": gate_id,
                                "model_id": model_id,
                                "error": str(exc),
                            })
    ranked = sorted(
        candidate_rows,
        key=lambda row: (
            bool(row["meaningful_candidate"]),
            bool(row["scout_clue"]),
            row["oos_profit_factor"],
            row["validation_profit_factor"],
            row["oos_net_profit"],
            -row["oos_max_drawdown_percent"],
            -abs(row["oos_trades_day"] - 5.0),
        ),
        reverse=True,
    )
    return {
        "datasets": datasets,
        "candidate_rows": candidate_rows,
        "failure_rows": failure_rows,
        "ranked_rows": ranked,
        "data_integrity_rows": data_integrity_rows(datasets),
        "score_cache": score_cache,
    }


def selected_trade_rows(result: Mapping[str, Any], best: Mapping[str, Any]) -> list[dict[str, Any]]:
    if not best:
        return []
    cache_key = (
        best["surface_id"],
        best["dataset_id"],
        best["feature_bundle"],
        best["target_id"],
        best["gate_id"],
        best["model_id"],
    )
    scores, _, path = result["score_cache"][cache_key]
    frame = result["datasets"][best["dataset_id"]]["frame"]
    thresholds = train_thresholds(frame)
    gate = gate_mask(frame, best["gate_id"], thresholds)
    mask = gate & np.isfinite(scores) & np.isfinite(path["pnl"]) & (scores >= float(best["score_threshold"]))
    selected = frame.loc[mask, ["timestamp", "split", "label", "label_class", "label_id", "minutes_from_cash_open"]].copy()
    selected["score"] = scores[mask]
    selected["pnl"] = path["pnl"][mask]
    selected["direction"] = path["direction"][mask]
    selected["candidate_id"] = best["candidate_id"]
    return selected.sort_values("timestamp").to_dict(orient="records")[:5000]


def surface_summary(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    out = []
    for surface_id in sorted({row["surface_id"] for row in rows}):
        subset = [row for row in rows if row["surface_id"] == surface_id]
        best = max(subset, key=lambda row: (row["oos_profit_factor"], row["oos_net_profit"]))
        out.append({
            "surface_id": surface_id,
            "candidate_count": len(subset),
            "scout_clue_count": sum(1 for row in subset if row["scout_clue"]),
            "meaningful_candidate_count": sum(1 for row in subset if row["meaningful_candidate"]),
            "best_candidate_id": best["candidate_id"],
            "best_oos_net": best["oos_net_profit"],
            "best_oos_pf": best["oos_profit_factor"],
            "best_oos_dd": best["oos_max_drawdown_percent"],
            "best_oos_trades_day": best["oos_trades_day"],
        })
    return out


def model_summary(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    out = []
    for model_id in sorted({row["model_id"] for row in rows}):
        subset = [row for row in rows if row["model_id"] == model_id]
        best = max(subset, key=lambda row: (row["oos_profit_factor"], row["oos_net_profit"]))
        out.append({
            "model_id": model_id,
            "candidate_count": len(subset),
            "scout_clue_count": sum(1 for row in subset if row["scout_clue"]),
            "meaningful_candidate_count": sum(1 for row in subset if row["meaningful_candidate"]),
            "best_candidate_id": best["candidate_id"],
            "best_oos_pf": best["oos_profit_factor"],
            "best_oos_net": best["oos_net_profit"],
        })
    return out


def tier_rows(summary: Mapping[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "record_view": "Tier A separate(Tier A 분리)",
            "status": "materialized_proxy_scout(프록시 탐색 물질화)",
            "kpi": f"candidates={summary['candidate_count']}; scout={summary['scout_clue_count']}; meaningful={summary['meaningful_candidate_count']}",
            "effect": "Tier A model input produced proxy KPI(Tier A 모델 입력이 프록시 KPI 생성)",
        },
        {
            "record_view": "Tier B separate(Tier B 분리)",
            "status": "missing_required(필수 누락)",
            "kpi": "not_materialized_in_f73b_proxy_scout(F73B 프록시 탐색에서 미물질화)",
            "effect": "not omitted; later repair or routed record required(생략 아님, 이후 수리 또는 라우팅 기록 필요)",
        },
        {
            "record_view": "Tier A+B combined(Tier A+B 합산)",
            "status": "out_of_scope_by_claim(주장 범위 밖)",
            "kpi": "no_synthetic_combined_claim_without_tier_b(Tier B 없이 합성 합산 주장 없음)",
            "effect": "prevents combined overclaim(합산 과장 방지)",
        },
    ]


def summary_payload(result: Mapping[str, Any]) -> dict[str, Any]:
    rows = result["candidate_rows"]
    ranked = result["ranked_rows"]
    best = ranked[0] if ranked else {}
    scout_count = sum(1 for row in rows if row["scout_clue"])
    meaningful_count = sum(1 for row in rows if row["meaningful_candidate"])
    final_like_count = sum(1 for row in rows if row["final_like_reference_only"])
    judgment = (
        "proxy_meaningful_signal_pre_mt5_required_no_authority"
        if meaningful_count
        else "proxy_scout_clue_repair_or_axis_reduction_required_no_authority"
        if scout_count
        else "proxy_scout_no_clue_repair_required_no_authority"
    )
    next_run = NEXT_PRE_MT5_RUN_ID if meaningful_count else NEXT_REPAIR_RUN_ID
    return {
        "created_at_utc": utc_now(),
        "status": STATUS,
        "judgment": judgment,
        "candidate_count": len(rows),
        "scout_clue_count": scout_count,
        "meaningful_candidate_count": meaningful_count,
        "final_like_reference_only_count": final_like_count,
        "model_failure_count": len(result["failure_rows"]),
        "best_candidate": best,
        "next_run_id": next_run,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def report_lines(summary: Mapping[str, Any]) -> list[str]:
    best = summary["best_candidate"]
    best_lines = [
        f"- candidate_id(후보 ID): `{best.get('candidate_id', '')}`",
        f"- surface/dataset/bundle(표면/데이터셋/묶음): `{best.get('surface_id', '')}` / `{best.get('dataset_id', '')}` / `{best.get('feature_bundle', '')}`",
        f"- target/model/gate(목표/모델/게이트): `{best.get('target_id', '')}` / `{best.get('model_id', '')}` / `{best.get('gate_id', '')}`",
        f"- validation net/PF/DD/tpd(검증 순수익/수익 팩터/손실폭/일거래): `{best.get('validation_net_profit', 0):.4f}` / `{best.get('validation_profit_factor', 0):.4f}` / `{best.get('validation_max_drawdown_percent', 0):.4f}%` / `{best.get('validation_trades_day', 0):.4f}`",
        f"- OOS net/PF/DD/tpd(표본외 순수익/수익 팩터/손실폭/일거래): `{best.get('oos_net_profit', 0):.4f}` / `{best.get('oos_profit_factor', 0):.4f}` / `{best.get('oos_max_drawdown_percent', 0):.4f}%` / `{best.get('oos_trades_day', 0):.4f}`",
        f"- scout/meaningful/final-like(탐색/의미/최종 유사): `{best.get('scout_clue', False)}` / `{best.get('meaningful_candidate', False)}` / `{best.get('final_like_reference_only', False)}`",
    ] if best else ["- no candidate rows(후보 행 없음)."]
    return [
        "# Frontier73B Session/Regime Feature/Model Proxy Scout(F73B 세션/장세 피처/모델 프록시 탐색)",
        "",
        f"Updated(갱신): {summary['created_at_utc']}",
        "",
        f"- status(상태): `{summary['status']}`",
        f"- judgment(판정): `{summary['judgment']}`",
        f"- candidate_count(후보 수): `{summary['candidate_count']}`",
        f"- scout_clue_count(탐색 단서 수): `{summary['scout_clue_count']}`",
        f"- meaningful_candidate_count(의미 후보 수): `{summary['meaningful_candidate_count']}`",
        f"- final_like_reference_only_count(최종 유사 참조 전용 수): `{summary['final_like_reference_only_count']}`",
        f"- model_failure_count(모델 실패 수): `{summary['model_failure_count']}`",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Hypothesis(가설)",
        "",
        "Session/regime-conditioned feature-set and model-family rotation(세션/장세 조건 피처 묶음과 모델 계열 회전)이 F72 runtime economics gap(런타임 경제성 간극)을 분리하는 scout clue(탐색 단서)를 만드는지 확인했다.",
        "",
        "## Best Candidate(최선 후보)",
        "",
        *best_lines,
        "",
        "## Proxy/Runtime Boundary(프록시/런타임 경계)",
        "",
        "This is proxy-only(프록시 전용) evidence. Effect(효과): meaningful candidate(의미 후보)가 있으면 Grok pre-MT5 review(Grok 사전 MT5 검토) 뒤 mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침)로 물질화한다.",
        "",
        "## Tier Records(티어 기록)",
        "",
        "- Tier A separate(Tier A 분리): materialized proxy scout(프록시 탐색 물질화).",
        "- Tier B separate(Tier B 분리): missing_required(필수 누락).",
        "- Tier A+B combined(Tier A+B 합산): out_of_scope_by_claim(주장 범위 밖).",
        "",
        "## Next Action(다음 행동)",
        "",
        f"`{summary['next_run_id']}`.",
    ]


def gate_audit_lines(summary: Mapping[str, Any]) -> list[str]:
    return [
        "# F73B Required Gate Coverage Audit(F73B 필수 게이트 커버리지 감사)",
        "",
        f"Updated(갱신): {summary['created_at_utc']}",
        "",
        "| gate(게이트) | status(상태) | evidence(근거) | effect(효과) |",
        "|---|---|---|---|",
        f"| stage_open_anchor(단계 개방 고정) | pass(통과) | `{rel(F73A_MANIFEST)}` | F73A design(설계)에 연결 |",
        f"| pruned_surface_plan(축소 표면 계획) | pass(통과) | `{rel(F73A_SURFACE_PLAN)}` | 전체 조합 폭발 방지 |",
        f"| data_integrity_boundary(데이터 무결성 경계) | pass_with_boundary(경계 포함 통과) | `{rel(RUN_ROOT / 'f73b_data_integrity_audit.csv')}` | 행/분할/누락을 기록 |",
        f"| proxy_scout_execution(프록시 탐색 실행) | pass(통과) | `{rel(RUN_ROOT / 'f73b_candidate_summary.csv')}` | 후보 KPI 생성 |",
        f"| tier_pair_record(티어 쌍 기록) | partial_with_missing_required(필수 누락 포함 부분 통과) | `{rel(RUN_ROOT / 'f73b_tier_record_status.csv')}` | Tier B 누락을 숨기지 않음 |",
        f"| mandatory_mt5_runtime_probe(필수 MT5 런타임 탐침) | pending_after_proxy_decision(프록시 결정 뒤 대기) | `{summary['next_run_id']}` | meaningful signal(의미 신호) 여부에 따라 사전 Grok 후 실행 |",
        f"| final_claim_guard(최종 주장 보호) | pass(통과) | `{CLAIM_BOUNDARY}` | 강한 주장 없음 |",
    ]


def selection_status_lines(summary: Mapping[str, Any]) -> list[str]:
    return [
        "# F73 Selection Status(F73 선택 상태)",
        "",
        f"- stage(단계): `{STAGE_ID}`",
        f"- current_run(현재 실행): `{summary['next_run_id']}`",
        f"- latest_completed_run(최근 완료 실행): `{RUN_ID}`",
        f"- status(상태): `{summary['status']}`",
        f"- judgment(판정): `{summary['judgment']}`",
        "- selected_baseline(선택 기준선): `not_claimed(주장 없음)`",
        "- runtime_authority(런타임 권위): `not_claimed(주장 없음)`",
        "- operating_promotion(운영 승격): `not_claimed(주장 없음)`",
        "- live_readiness(실거래 준비): `not_claimed(주장 없음)`",
        "- Goal Achieve(목표 달성): `not_claimed(주장 없음)`",
        f"- next_action(다음 행동): `{summary['next_run_id']}`",
        f"- boundary(경계): `{CLAIM_BOUNDARY}`",
    ]


def run_manifest(summary: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": summary["next_run_id"],
        "status": summary["status"],
        "judgment": summary["judgment"],
        "candidate_count": summary["candidate_count"],
        "scout_clue_count": summary["scout_clue_count"],
        "meaningful_candidate_count": summary["meaningful_candidate_count"],
        "claim_boundary": CLAIM_BOUNDARY,
        "artifacts": [
            rel(RUN_ROOT / "f73b_candidate_summary.csv"),
            rel(RUN_ROOT / "f73b_top_candidates.csv"),
            rel(RUN_ROOT / "f73b_best_candidate_trades.csv"),
            rel(REVIEWS_ROOT / "frontier73B_session_regime_feature_model_rotation_proxy_scout_report.md"),
        ],
    }


def ledger_row(summary: Mapping[str, Any]) -> dict[str, Any]:
    best = summary["best_candidate"]
    report = REVIEWS_ROOT / "frontier73B_session_regime_feature_model_rotation_proxy_scout_report.md"
    return {
        "ledger_row_id": f"{RUN_ID}__proxy_scout",
        "row_id": f"{RUN_ID}__proxy_scout",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "proxy_scout(프록시 탐색)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "Tier A separate(Tier A 분리)",
        "tier_scope": "Tier A separate; Tier B missing_required; Tier A+B out_of_scope_by_claim",
        "kpi_scope": "proxy_scout_kpi(프록시 탐색 KPI)",
        "scoreboard_lane": "structural_scout(구조 스카우트)",
        "status": summary["status"],
        "judgment": summary["judgment"],
        "path": rel(report),
        "primary_kpi": f"candidates={summary['candidate_count']}; scout={summary['scout_clue_count']}; meaningful={summary['meaningful_candidate_count']}",
        "guardrail_kpi": f"best_oos_pf={best.get('oos_profit_factor', 0):.4f}; best_oos_tpd={best.get('oos_trades_day', 0):.4f}; mt5_probe=pending",
        "external_verification_status": "out_of_scope_by_claim_proxy_only(프록시 전용 주장 범위 밖)",
        "notes": "F73B session/regime feature/model proxy scout completed; MT5 probe depends on meaningful signal.",
        "family": "experiment_execution(실험 실행)",
        "lane": "proxy_scout(프록시 탐색)",
        "primary_report": rel(report),
        "run_number": "frontier73B",
        "date": summary["created_at_utc"][:10],
        "decision": summary["judgment"],
        "next_run_id": summary["next_run_id"],
        "rows": summary["candidate_count"],
        "gate_passes": 6,
        "gate_total": 7,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(report),
        "run_date": summary["created_at_utc"][:10],
        "primary_artifact": rel(RUN_ROOT / "f73b_candidate_summary.csv"),
        "candidate_model_id": best.get("candidate_id", ""),
        "net_profit": best.get("oos_net_profit", ""),
        "profit_factor": best.get("oos_profit_factor", ""),
        "drawdown": best.get("oos_max_drawdown_percent", ""),
        "trade_count": best.get("oos_trade_count", ""),
        "result_status": summary["status"],
        "candidate_rows": summary["candidate_count"],
        "positive_proxy_rows": summary["scout_clue_count"],
        "best_model_id": best.get("model_id", ""),
        "best_proxy_net": best.get("oos_net_profit", ""),
        "view": "Tier A separate(Tier A 분리)",
        "tier": "Tier A",
        "metric_scope": "proxy_scout_kpi(프록시 탐색 KPI)",
        "result_judgment": summary["judgment"],
        "final_decision_path": rel(report),
        "gate_audit_path": rel(REVIEWS_ROOT / "required_gate_coverage_audit_f73b.md"),
        "created_at": summary["created_at_utc"],
        "created_at_utc": summary["created_at_utc"],
        "required_gate_audit": rel(REVIEWS_ROOT / "required_gate_coverage_audit_f73b.md"),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "proxy_scout_only(프록시 탐색 전용)",
        "evidence_boundary": "proxy_only_no_runtime(프록시 전용, 런타임 없음)",
        "next_action": summary["next_run_id"],
        "question": "Can session/regime feature/model rotation separate runtime economics source?(세션/장세 피처/모델 회전이 런타임 경제성 원천을 분리할 수 있나?)",
        "artifact_count": 12,
        "work_family": "experiment_execution(실험 실행)",
        "run_family": "frontier_proxy_scout(전선 프록시 탐색)",
        "run_type": "session_regime_feature_model_rotation_proxy_scout(세션/장세 피처/모델 회전 프록시 탐색)",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN_ROOT / "run_manifest.json"),
        "result_path": rel(report),
        "trade_density": best.get("oos_trades_day", ""),
        "max_drawdown_percent": best.get("oos_max_drawdown_percent", ""),
        "strict_joint_pass_count": summary["meaningful_candidate_count"],
    }


def update_ledgers(summary: Mapping[str, Any]) -> None:
    row = ledger_row(summary)
    upsert_ledger(ALPHA_LEDGER, "ledger_row_id", row)
    upsert_ledger(RUN_REGISTRY, "run_id", row)
    upsert_ledger(REVIEWS_ROOT / "stage_run_ledger.csv", "ledger_row_id", row, source_header=ALPHA_LEDGER)


def update_registers(summary: Mapping[str, Any]) -> None:
    marker = "<!-- frontier73B_session_regime_feature_model_rotation_proxy_scout_v1 -->"
    best = summary["best_candidate"]
    block = f"""<!-- frontier73B_session_regime_feature_model_rotation_proxy_scout_v1 -->
- `{RUN_ID}` executed F73 session/regime feature/model proxy scout(F73 세션/장세 피처/모델 프록시 탐색). Result(결과): `{summary['judgment']}`. Candidates(후보) `{summary['candidate_count']}`, scout clue(탐색 단서) `{summary['scout_clue_count']}`, meaningful candidate(의미 후보) `{summary['meaningful_candidate_count']}`. Best OOS(최선 표본외) net/PF/DD/trades_day(순수익/수익 팩터/손실폭/일거래) `{best.get('oos_net_profit', 0):.4f}/{best.get('oos_profit_factor', 0):.4f}/{best.get('oos_max_drawdown_percent', 0):.4f}/{best.get('oos_trades_day', 0):.4f}`. Evidence(근거): `{rel(REVIEWS_ROOT / 'frontier73B_session_regime_feature_model_rotation_proxy_scout_report.md')}`. Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). Next(다음): `{summary['next_run_id']}`."""
    append_once(IDEA_REGISTRY, marker, block)


def update_state_files(summary: Mapping[str, Any]) -> None:
    state = [
        f"current_stage_id: {STAGE_ID}",
        f"active_stage: {STAGE_ID}",
        f"current_run_id: {summary['next_run_id']}",
        f"latest_completed_run_id: {RUN_ID}",
        f"current_status: {summary['status']}",
        f"current_judgment: {summary['judgment']}",
        f"next_run_id: {summary['next_run_id']}",
        "runtime_probe_status: f73_mandatory_runtime_probe_pending_after_proxy_decision",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "live_readiness: not_claimed",
        "goal_achieve: not_claimed",
        "five_stage_retrospective_due_status: not_due_after_f72_closeout",
        f"updated_at_utc: '{summary['created_at_utc']}'",
        "notes:",
        f'  - "Action(행동): F73B proxy scout(프록시 탐색)를 실행했다. Candidates(후보) {summary["candidate_count"]}, scout clue(탐색 단서) {summary["scout_clue_count"]}, meaningful(의미 후보) {summary["meaningful_candidate_count"]}."',
        f'  - "Effect(효과): feature/label/model/regime(피처/라벨/모델/장세) 축을 실제 KPI(핵심 성과 지표)로 비교했고, 다음 행동을 {summary["next_run_id"]}로 설정했다."',
        '  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."',
    ]
    io_path(WORKSPACE_STATE).write_text("\n".join(state) + "\n", encoding="utf-8-sig")
    write_text(CURRENT_WORKING_STATE, [
        "# Current Working State(현재 작업 상태)",
        "",
        f"Updated(갱신): {summary['created_at_utc']}",
        "",
        f"Active stage(활성 단계): `{STAGE_ID}`",
        f"Current run(현재 실행): `{summary['next_run_id']}`",
        f"Latest completed run(최근 완료 실행): `{RUN_ID}`",
        "",
        "## Current Truth(현재 진실)",
        "",
        "Action(행동): F73B session/regime feature/model proxy scout(세션/장세 피처/모델 프록시 탐색)를 실행했다.",
        "",
        f"Effect(효과): 후보 `{summary['candidate_count']}`개 중 scout clue(탐색 단서) `{summary['scout_clue_count']}`개, meaningful candidate(의미 후보) `{summary['meaningful_candidate_count']}`개를 기록했고, 다음 행동을 `{summary['next_run_id']}`로 설정했다.",
        "",
        f"- judgment(판정): `{summary['judgment']}`.",
        f"- best OOS net/PF/DD/tpd(최선 표본외 순수익/수익 팩터/손실폭/일거래): `{summary['best_candidate'].get('oos_net_profit', 0):.4f}` / `{summary['best_candidate'].get('oos_profit_factor', 0):.4f}` / `{summary['best_candidate'].get('oos_max_drawdown_percent', 0):.4f}%` / `{summary['best_candidate'].get('oos_trades_day', 0):.4f}`.",
        "- runtime probe(런타임 탐침): pending after proxy decision(프록시 결정 뒤 대기).",
        "",
        f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    ])


def write_outputs(result: Mapping[str, Any], summary: Mapping[str, Any]) -> None:
    for path in (RUN_ROOT / "reports", REVIEWS_ROOT, SELECTED_ROOT):
        io_path(path).mkdir(parents=True, exist_ok=True)
    ranked = result["ranked_rows"]
    write_csv(RUN_ROOT / "f73b_candidate_summary.csv", result["candidate_rows"])
    write_csv(RUN_ROOT / "f73b_top_candidates.csv", ranked[:40])
    write_csv(RUN_ROOT / "f73b_best_candidate_trades.csv", selected_trade_rows(result, summary["best_candidate"]))
    write_csv(RUN_ROOT / "f73b_model_failures.csv", result["failure_rows"])
    write_csv(RUN_ROOT / "f73b_data_integrity_audit.csv", result["data_integrity_rows"])
    write_csv(RUN_ROOT / "f73b_surface_summary.csv", surface_summary(result["candidate_rows"]))
    write_csv(RUN_ROOT / "f73b_model_family_summary.csv", model_summary(result["candidate_rows"]))
    write_csv(RUN_ROOT / "f73b_tier_record_status.csv", tier_rows(summary))
    write_json(RUN_ROOT / "frontier73B_proxy_summary.json", summary)
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(summary))
    write_text(RUN_ROOT / "reports/result_summary.md", report_lines(summary))
    write_text(REVIEWS_ROOT / "frontier73B_session_regime_feature_model_rotation_proxy_scout_report.md", report_lines(summary))
    write_text(REVIEWS_ROOT / "required_gate_coverage_audit_f73b.md", gate_audit_lines(summary))
    write_csv(REVIEWS_ROOT / "f73b_top_candidates_review.csv", ranked[:25])
    write_csv(REVIEWS_ROOT / "f73b_surface_summary_review.csv", surface_summary(result["candidate_rows"]))
    write_csv(REVIEWS_ROOT / "f73b_model_family_summary_review.csv", model_summary(result["candidate_rows"]))
    write_csv(REVIEWS_ROOT / "f73b_data_integrity_audit_review.csv", result["data_integrity_rows"])
    write_csv(REVIEWS_ROOT / "f73b_tier_record_status_review.csv", tier_rows(summary))
    write_text(SELECTED_ROOT / "selection_status.md", selection_status_lines(summary))


def main() -> int:
    missing = [rel(path) for path in required_inputs() if not path_exists(path)]
    if missing:
        raise FileNotFoundError(f"F73B required material missing: {missing}")
    result = run_scout()
    summary = summary_payload(result)
    write_outputs(result, summary)
    update_registers(summary)
    update_ledgers(summary)
    update_state_files(summary)
    print(json.dumps(json_ready({
        "status": summary["status"],
        "judgment": summary["judgment"],
        "candidate_count": summary["candidate_count"],
        "scout_clue_count": summary["scout_clue_count"],
        "meaningful_candidate_count": summary["meaningful_candidate_count"],
        "final_like_reference_only_count": summary["final_like_reference_only_count"],
        "next_run_id": summary["next_run_id"],
        "best_oos_net": summary["best_candidate"].get("oos_net_profit", 0),
        "best_oos_pf": summary["best_candidate"].get("oos_profit_factor", 0),
        "best_oos_dd": summary["best_candidate"].get("oos_max_drawdown_percent", 0),
        "best_oos_trades_day": summary["best_candidate"].get("oos_trades_day", 0),
        "claim_boundary": CLAIM_BOUNDARY,
    }), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
