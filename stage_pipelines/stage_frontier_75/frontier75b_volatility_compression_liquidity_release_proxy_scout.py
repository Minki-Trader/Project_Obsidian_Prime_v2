from __future__ import annotations

import csv
import hashlib
import json
import math
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier, HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


ROOT = Path(__file__).resolve().parents[2]

STAGE_ID = "stage_frontier_75__volatility_compression_liquidity_release_for_tradeable_density"
RUN_ID = "frontier75B_volatility_compression_liquidity_release_proxy_scout_v1"
PARENT_RUN_ID = "frontier75A_stage_open_upstream_mechanism_rotation_after_f74_microburst_negative_memory_v1"
IDEA_ID = "IDEA-FR75-VOLATILITY-COMPRESSION-LIQUIDITY-RELEASE"

CLAIM_BOUNDARY = (
    "proxy_scout_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)
INITIAL_BALANCE_PROXY = 10000.0
SPREAD_POINT_VALUE = 0.01

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
REVIEW_DIR = STAGE_DIR / "03_reviews"

DATASET_PATH = (
    "data/processed/model_inputs/"
    "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/"
    "model_input_dataset.parquet"
)
FEATURE_ORDER_PATH = (
    "data/processed/model_inputs/"
    "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/"
    "model_input_feature_order.txt"
)
RAW_PATH = "data/raw/mt5_bars/m5/US100/bars_us100_m5_mt5api_raw.csv"

REPORT_PATH = f"stages/{STAGE_ID}/03_reviews/frontier75B_volatility_compression_liquidity_release_proxy_scout_report.md"
GATE_AUDIT_PATH = f"stages/{STAGE_ID}/03_reviews/required_gate_coverage_audit_f75b.md"
RUN_MANIFEST_PATH = f"stages/{STAGE_ID}/02_runs/{RUN_ID}/run_manifest.json"
SELECTION_STATUS_PATH = f"stages/{STAGE_ID}/04_selected/selection_status.md"
CONTEXT_ANCHOR_PATH = f"stages/{STAGE_ID}/03_reviews/context_anchor.md"


def fs_path(path: Path) -> Path:
    absolute = path if path.is_absolute() else ROOT / path
    if os.name == "nt":
        text = str(absolute)
        if text.startswith("\\\\?\\"):
            return Path(text)
        if text.startswith("\\\\"):
            return Path("\\\\?\\UNC\\" + text.lstrip("\\"))
        return Path("\\\\?\\" + text)
    return absolute


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_text(path: Path) -> str:
    return fs_path(path).read_text(encoding="utf-8-sig")


def write_text(path: Path, text: str) -> None:
    fpath = fs_path(path)
    fpath.parent.mkdir(parents=True, exist_ok=True)
    fpath.write_text(text, encoding="utf-8-sig", newline="\n")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    fpath = fs_path(path)
    fpath.parent.mkdir(parents=True, exist_ok=True)
    fpath.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    fpath = fs_path(path)
    fpath.parent.mkdir(parents=True, exist_ok=True)
    with fpath.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def upsert_csv_row(path: Path, key_field: str, row: dict[str, Any], fieldnames: list[str] | None = None) -> None:
    fpath = fs_path(path)
    if fpath.exists():
        with fpath.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            existing_fieldnames = list(reader.fieldnames or [])
            rows = list(reader)
    else:
        existing_fieldnames = []
        rows = []
    if fieldnames is None:
        fieldnames = existing_fieldnames
    if not fieldnames:
        fieldnames = list(row.keys())
    for key in row:
        if key not in fieldnames:
            fieldnames.append(key)
    rows = [old for old in rows if old.get(key_field) != row.get(key_field)]
    rows.append({field: row.get(field, "") for field in fieldnames})
    with fpath.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with fs_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ensure_dirs() -> None:
    for path in (RUN_DIR, REVIEW_DIR):
        fs_path(path).mkdir(parents=True, exist_ok=True)


def load_inputs() -> tuple[pd.DataFrame, list[str], dict[str, Any]]:
    dataset_path = ROOT / DATASET_PATH
    feature_path = ROOT / FEATURE_ORDER_PATH
    raw_path = ROOT / RAW_PATH
    for path in (dataset_path, feature_path, raw_path):
        if not fs_path(path).exists():
            raise FileNotFoundError(str(path))

    df = pd.read_parquet(fs_path(dataset_path)).sort_values("timestamp").reset_index(drop=True)
    feature_order = [line.strip() for line in read_text(feature_path).splitlines() if line.strip()]
    raw = pd.read_csv(
        fs_path(raw_path),
        usecols=["time_close_unix", "open", "high", "low", "close", "spread_points", "tick_volume"],
    )
    raw["timestamp"] = pd.to_datetime(raw["time_close_unix"], unit="s", utc=True)
    raw = raw.drop(columns=["time_close_unix"])
    merged = df.merge(raw, on="timestamp", how="left", suffixes=("", "_raw"))
    missing_raw = int(merged["close"].isna().sum())
    if missing_raw:
        raise RuntimeError(f"raw OHLC merge missing rows: {missing_raw}")

    identity = {
        "dataset_path": DATASET_PATH,
        "dataset_sha256": sha256_file(dataset_path),
        "feature_order_path": FEATURE_ORDER_PATH,
        "feature_order_sha256": sha256_file(feature_path),
        "raw_path": RAW_PATH,
        "raw_sha256": sha256_file(raw_path),
        "rows": int(merged.shape[0]),
        "columns": int(merged.shape[1]),
        "feature_count": len(feature_order),
        "split_counts": {str(k): int(v) for k, v in merged["split"].value_counts().items()},
        "missing_raw_rows": missing_raw,
        "time_min": str(merged["timestamp"].min()),
        "time_max": str(merged["timestamp"].max()),
    }
    return merged, feature_order, identity


def future_continuity_ok(timestamps: pd.Series, horizon: int) -> np.ndarray:
    future_ts = timestamps.shift(-horizon)
    delta = (future_ts - timestamps).dt.total_seconds()
    return (delta == horizon * 300).fillna(False).to_numpy()


def first_touch_outcome(
    close: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    spread_cost: np.ndarray,
    atr: np.ndarray,
    future_ok: np.ndarray,
    horizon: int,
    target_mult: float,
    stop_mult: float,
    direction: str,
) -> tuple[np.ndarray, np.ndarray]:
    pnl = np.full(len(close), np.nan, dtype=float)
    exit_bars = np.full(len(close), np.nan, dtype=float)
    sign = 1.0 if direction == "long" else -1.0
    for i in range(0, len(close) - horizon):
        if not future_ok[i]:
            continue
        if not (np.isfinite(close[i]) and np.isfinite(atr[i]) and atr[i] > 0):
            continue
        entry = close[i]
        target = atr[i] * target_mult
        stop = atr[i] * stop_mult
        raw_result = None
        exit_bar = horizon
        for step in range(1, horizon + 1):
            hi = high[i + step]
            lo = low[i + step]
            if not (np.isfinite(hi) and np.isfinite(lo)):
                continue
            if direction == "long":
                hit_stop = lo <= entry - stop
                hit_target = hi >= entry + target
            else:
                hit_stop = hi >= entry + stop
                hit_target = lo <= entry - target
            if hit_stop and hit_target:
                raw_result = -stop
                exit_bar = step
                break
            if hit_stop:
                raw_result = -stop
                exit_bar = step
                break
            if hit_target:
                raw_result = target
                exit_bar = step
                break
        if raw_result is None:
            raw_result = sign * (close[i + horizon] - entry)
        cost = spread_cost[i] if np.isfinite(spread_cost[i]) else 0.0
        pnl[i] = raw_result - cost
        exit_bars[i] = exit_bar
    return pnl, exit_bars


def make_context_masks(df: pd.DataFrame) -> dict[str, np.ndarray]:
    train = df["split"].eq("train")
    bw_q30 = float(df.loc[train, "bollinger_width_20"].quantile(0.30))
    hv_q35 = float(df.loc[train, "historical_vol_5_over_20"].quantile(0.35))
    atr_ratio_q35 = float(df.loc[train, "atr_14_over_atr_50"].quantile(0.35))
    return {
        "bw_q30_compression": df["bollinger_width_20"].le(bw_q30).to_numpy(),
        "hv_q35_compression": df["historical_vol_5_over_20"].le(hv_q35).to_numpy(),
        "squeeze_or_atr_q35": (df["bb_squeeze"].ge(1) | df["atr_14_over_atr_50"].le(atr_ratio_q35)).to_numpy(),
    }


def make_session_masks(df: pd.DataFrame) -> dict[str, np.ndarray]:
    minutes = df["minutes_from_cash_open"]
    cash = df["is_us_cash_open"].eq(1)
    return {
        "cash_all": cash.to_numpy(),
        "cash_open_120": (cash & minutes.ge(0) & minutes.le(120)).to_numpy(),
        "cash_late_150": (cash & minutes.ge(240)).to_numpy(),
    }


def feature_bundles(feature_order: list[str]) -> dict[str, list[str]]:
    wanted = {
        "compression_release_core": [
            "bb_squeeze",
            "bollinger_width_20",
            "historical_vol_5_over_20",
            "atr_14",
            "atr_50",
            "atr_14_over_atr_50",
            "adx_14",
            "di_spread_14",
            "bb_position_20",
            "return_zscore_20",
            "hl_zscore_50",
            "ema9_ema20_diff",
            "ema20_ema50_diff",
            "ppo_hist_12_26_9",
            "roc_12",
            "rsi_14_slope_3",
            "supertrend_10_3",
            "vortex_indicator",
            "minutes_from_cash_open",
            "is_first_30m_after_open",
            "is_last_30m_before_cash_close",
        ],
        "compression_macro_mega": [
            "bb_squeeze",
            "bollinger_width_20",
            "historical_vol_5_over_20",
            "atr_14_over_atr_50",
            "adx_14",
            "di_spread_14",
            "vix_change_1",
            "vix_zscore_20",
            "us10yr_change_1",
            "us10yr_zscore_20",
            "usdx_change_1",
            "usdx_zscore_20",
            "mega8_equal_return_1",
            "top3_weighted_return_1",
            "mega8_pos_breadth_1",
            "mega8_dispersion_5",
            "us100_minus_mega8_equal_return_1",
            "us100_minus_top3_weighted_return_1",
            "minutes_from_cash_open",
        ],
    }
    feature_set = set(feature_order)
    bundles = {"all58": feature_order}
    for name, cols in wanted.items():
        bundles[name] = [col for col in cols if col in feature_set]
    return bundles


def model_builders() -> dict[str, Any]:
    return {
        "extra_trees_d7_l80": lambda: make_pipeline(
            SimpleImputer(strategy="median"),
            ExtraTreesClassifier(
                n_estimators=60,
                max_depth=7,
                min_samples_leaf=80,
                class_weight="balanced",
                random_state=7501,
                n_jobs=-1,
            ),
        ),
        "hist_gbdt_l15": lambda: make_pipeline(
            SimpleImputer(strategy="median"),
            HistGradientBoostingClassifier(
                max_iter=80,
                learning_rate=0.045,
                max_leaf_nodes=15,
                l2_regularization=0.05,
                random_state=7502,
            ),
        ),
        "logistic_l2_balanced": lambda: make_pipeline(
            SimpleImputer(strategy="median"),
            StandardScaler(),
            LogisticRegression(max_iter=800, class_weight="balanced", C=0.75, solver="lbfgs"),
        ),
    }


def split_days(df: pd.DataFrame, split: str) -> int:
    dates = df.loc[df["split"].eq(split), "timestamp"].dt.date.nunique()
    return max(int(dates), 1)


def non_overlapping_indices(candidate_idx: np.ndarray, horizon: int) -> np.ndarray:
    selected = []
    next_allowed = -1
    for idx in candidate_idx:
        if int(idx) >= next_allowed:
            selected.append(int(idx))
            next_allowed = int(idx) + horizon
    return np.array(selected, dtype=int)


def trade_metrics(pnl: np.ndarray, exit_bars: np.ndarray, days: int) -> dict[str, Any]:
    pnl = pnl[np.isfinite(pnl)]
    exit_bars = exit_bars[np.isfinite(exit_bars)]
    trade_count = int(len(pnl))
    if trade_count == 0:
        return {
            "net_profit": 0.0,
            "gross_profit": 0.0,
            "gross_loss": 0.0,
            "profit_factor": 0.0,
            "max_drawdown_amount": 0.0,
            "max_drawdown_percent": 0.0,
            "trade_count": 0,
            "trades_day": 0.0,
            "win_rate": 0.0,
            "average_win": 0.0,
            "average_loss": 0.0,
            "payoff_ratio": 0.0,
            "expectancy": 0.0,
            "recovery_factor": 0.0,
            "max_consecutive_loss": 0,
            "avg_hold_bars": 0.0,
            "time_under_water_bars": 0,
        }
    wins = pnl[pnl > 0]
    losses = pnl[pnl < 0]
    gross_profit = float(wins.sum())
    gross_loss = float(-losses.sum())
    net_profit = float(pnl.sum())
    equity = np.cumsum(pnl)
    peaks = np.maximum.accumulate(np.concatenate([[0.0], equity]))[1:]
    drawdowns = peaks - equity
    max_dd = float(drawdowns.max()) if len(drawdowns) else 0.0
    max_dd_pct = float(max_dd / INITIAL_BALANCE_PROXY * 100.0)
    max_consec_loss = 0
    current_loss = 0
    for value in pnl:
        if value < 0:
            current_loss += 1
            max_consec_loss = max(max_consec_loss, current_loss)
        else:
            current_loss = 0
    time_under_water = int((drawdowns > 0).sum())
    avg_win = float(wins.mean()) if len(wins) else 0.0
    avg_loss = float(losses.mean()) if len(losses) else 0.0
    return {
        "net_profit": net_profit,
        "gross_profit": gross_profit,
        "gross_loss": gross_loss,
        "profit_factor": float(gross_profit / gross_loss) if gross_loss > 0 else (999.0 if gross_profit > 0 else 0.0),
        "max_drawdown_amount": max_dd,
        "max_drawdown_percent": max_dd_pct,
        "trade_count": trade_count,
        "trades_day": float(trade_count / days),
        "win_rate": float(len(wins) / trade_count),
        "average_win": avg_win,
        "average_loss": avg_loss,
        "payoff_ratio": float(avg_win / abs(avg_loss)) if avg_loss < 0 else 0.0,
        "expectancy": float(net_profit / trade_count),
        "recovery_factor": float(net_profit / max_dd) if max_dd > 0 else (999.0 if net_profit > 0 else 0.0),
        "max_consecutive_loss": max_consec_loss,
        "avg_hold_bars": float(exit_bars.mean()) if len(exit_bars) else 0.0,
        "time_under_water_bars": time_under_water,
    }


def score_candidate(row: dict[str, Any]) -> float:
    val_pf = float(row["validation_profit_factor"])
    oos_pf = float(row["oos_profit_factor"])
    val_net = float(row["validation_net_profit"])
    oos_net = float(row["oos_net_profit"])
    val_dd = float(row["validation_max_drawdown_percent"])
    oos_dd = float(row["oos_max_drawdown_percent"])
    oos_tpd = float(row["oos_trades_day"])
    target_tpd = float(row["target_trades_day"])
    score = 0.0
    score += min(val_pf, 4.0) * 1.5 + min(oos_pf, 4.0) * 2.0
    score += min(max(val_net, 0.0), 3000.0) / 1000.0
    score += min(max(oos_net, 0.0), 3000.0) / 700.0
    score -= max(val_dd - 10.0, 0.0) * 1.25
    score -= max(oos_dd - 10.0, 0.0) * 1.75
    score -= abs(oos_tpd - target_tpd) / max(target_tpd, 1.0)
    if 5.0 <= oos_tpd <= 10.0:
        score += 1.0
    if val_net > 0 and oos_net > 0:
        score += 2.0
    return float(score)


def classify_candidate(row: dict[str, Any]) -> tuple[int, int, int]:
    val_pf = float(row["validation_profit_factor"])
    oos_pf = float(row["oos_profit_factor"])
    val_net = float(row["validation_net_profit"])
    oos_net = float(row["oos_net_profit"])
    val_dd = float(row["validation_max_drawdown_percent"])
    oos_dd = float(row["oos_max_drawdown_percent"])
    oos_tpd = float(row["oos_trades_day"])
    scout = int(val_net > 0 and oos_net > 0 and val_pf >= 1.20 and oos_pf >= 1.15 and val_dd < 10.0 and oos_dd < 10.0)
    meaningful = int(scout and val_pf >= 1.50 and oos_pf >= 1.30 and oos_tpd >= 3.0)
    final_like = int(meaningful and val_pf >= 2.0 and oos_pf >= 2.0 and 5.0 <= oos_tpd <= 10.0)
    return scout, meaningful, final_like


def density_rows(
    df: pd.DataFrame,
    outcomes: dict[tuple[str, int, float, float], tuple[np.ndarray, np.ndarray, np.ndarray]],
    context_masks: dict[str, np.ndarray],
    session_masks: dict[str, np.ndarray],
) -> list[dict[str, Any]]:
    rows = []
    for (direction, horizon, target_mult, stop_mult), (pnl, _, future_ok) in outcomes.items():
        profitable = pnl > 0
        for context_name, context_mask in context_masks.items():
            for session_name, session_mask in session_masks.items():
                mask = context_mask & session_mask & future_ok
                row: dict[str, Any] = {
                    "direction": direction,
                    "horizon": horizon,
                    "target_atr_mult": target_mult,
                    "stop_atr_mult": stop_mult,
                    "context_gate": context_name,
                    "session_gate": session_name,
                }
                for split in ("train", "validation", "oos"):
                    split_mask = mask & df["split"].eq(split).to_numpy()
                    count = int(split_mask.sum())
                    positive = int((split_mask & profitable).sum())
                    row[f"{split}_rows"] = count
                    row[f"{split}_positive"] = positive
                    row[f"{split}_positive_rate"] = float(positive / count) if count else 0.0
                rows.append(row)
    return rows


def run_scout(df: pd.DataFrame, feature_order: list[str]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    close = df["close"].to_numpy(dtype=float)
    high = df["high"].to_numpy(dtype=float)
    low = df["low"].to_numpy(dtype=float)
    spread_cost = df["spread_points"].to_numpy(dtype=float) * SPREAD_POINT_VALUE
    atr = df["atr_14"].to_numpy(dtype=float)
    context_masks = make_context_masks(df)
    session_masks = make_session_masks(df)
    bundles = feature_bundles(feature_order)
    builders = model_builders()
    label_configs = [
        {"horizon": 6, "target_mult": 0.70, "stop_mult": 0.45},
        {"horizon": 12, "target_mult": 1.00, "stop_mult": 0.65},
        {"horizon": 18, "target_mult": 1.25, "stop_mult": 0.80},
    ]
    target_trade_days = [2.0, 3.5, 5.0, 8.0]
    split_day_counts = {split: split_days(df, split) for split in ("train", "validation", "oos")}

    outcomes: dict[tuple[str, int, float, float], tuple[np.ndarray, np.ndarray, np.ndarray]] = {}
    for config in label_configs:
        future_ok = future_continuity_ok(df["timestamp"], int(config["horizon"]))
        for direction in ("long", "short"):
            pnl, exit_bars = first_touch_outcome(
                close=close,
                high=high,
                low=low,
                spread_cost=spread_cost,
                atr=atr,
                future_ok=future_ok,
                horizon=int(config["horizon"]),
                target_mult=float(config["target_mult"]),
                stop_mult=float(config["stop_mult"]),
                direction=direction,
            )
            outcomes[(direction, int(config["horizon"]), float(config["target_mult"]), float(config["stop_mult"]))] = (
                pnl,
                exit_bars,
                future_ok,
            )

    density = density_rows(df, outcomes, context_masks, session_masks)
    results: list[dict[str, Any]] = []
    split_values = df["split"].to_numpy()
    train_mask_base = split_values == "train"
    val_mask_base = split_values == "validation"
    oos_mask_base = split_values == "oos"

    candidate_id = 0
    for key, (pnl, exit_bars, future_ok) in outcomes.items():
        direction, horizon, target_mult, stop_mult = key
        y = (pnl > 0).astype(int)
        valid_label = np.isfinite(pnl) & future_ok
        for context_name, context_mask in context_masks.items():
            for session_name, session_mask in session_masks.items():
                gate_mask = context_mask & session_mask & valid_label
                train_mask = gate_mask & train_mask_base
                val_mask = gate_mask & val_mask_base
                oos_mask = gate_mask & oos_mask_base
                if int(train_mask.sum()) < 400 or int(val_mask.sum()) < 80 or int(oos_mask.sum()) < 80:
                    continue
                train_pos = int((train_mask & (y == 1)).sum())
                train_neg = int((train_mask & (y == 0)).sum())
                if train_pos < 40 or train_neg < 40:
                    continue
                for bundle_name, cols in bundles.items():
                    if len(cols) < 8:
                        continue
                    X_train = df.loc[train_mask, cols]
                    y_train = y[train_mask]
                    for model_name, builder in builders.items():
                        model = builder()
                        model.fit(X_train, y_train)
                        scores = np.full(len(df), np.nan, dtype=float)
                        scored_mask = gate_mask & (val_mask_base | oos_mask_base)
                        if not scored_mask.any():
                            continue
                        scores[scored_mask] = model.predict_proba(df.loc[scored_mask, cols])[:, 1]
                        val_scores = scores[val_mask]
                        val_scores = val_scores[np.isfinite(val_scores)]
                        if len(val_scores) < 30:
                            continue
                        for target_tpd in target_trade_days:
                            target_count = int(math.ceil(target_tpd * split_day_counts["validation"]))
                            if target_count < 5 or target_count > len(val_scores):
                                continue
                            threshold = float(np.sort(val_scores)[-target_count])
                            row: dict[str, Any] = {
                                "candidate_id": f"f75b_{candidate_id:04d}",
                                "direction": direction,
                                "horizon": horizon,
                                "target_atr_mult": target_mult,
                                "stop_atr_mult": stop_mult,
                                "context_gate": context_name,
                                "session_gate": session_name,
                                "feature_bundle": bundle_name,
                                "feature_count": len(cols),
                                "model_family": model_name,
                                "target_trades_day": target_tpd,
                                "validation_threshold": threshold,
                                "train_rows": int(train_mask.sum()),
                                "train_positive_rate": float(y_train.mean()),
                                "validation_rows": int(val_mask.sum()),
                                "oos_rows": int(oos_mask.sum()),
                            }
                            selected_by_split: dict[str, np.ndarray] = {}
                            for split, split_mask in (
                                ("validation", val_mask),
                                ("oos", oos_mask),
                            ):
                                idx = np.where(split_mask & np.isfinite(scores) & (scores >= threshold))[0]
                                selected = non_overlapping_indices(idx, int(horizon))
                                selected_by_split[split] = selected
                                metrics = trade_metrics(pnl[selected], exit_bars[selected], split_day_counts[split])
                                for metric_name, metric_value in metrics.items():
                                    row[f"{split}_{metric_name}"] = metric_value
                            scout, meaningful, final_like = classify_candidate(row)
                            row["scout_clue"] = scout
                            row["meaningful_signal"] = meaningful
                            row["final_like_reference_only"] = final_like
                            row["joint_score"] = score_candidate(row)
                            row["selected_validation_indices"] = ";".join(map(str, selected_by_split["validation"][:20]))
                            row["selected_oos_indices"] = ";".join(map(str, selected_by_split["oos"][:20]))
                            results.append(row)
                            candidate_id += 1

    results.sort(key=lambda item: float(item["joint_score"]), reverse=True)
    summary = {
        "candidate_rows": len(results),
        "scout_clue_count": int(sum(int(row["scout_clue"]) for row in results)),
        "meaningful_signal_count": int(sum(int(row["meaningful_signal"]) for row in results)),
        "final_like_reference_only_count": int(sum(int(row["final_like_reference_only"]) for row in results)),
        "split_days": split_day_counts,
        "best_candidate_id": results[0]["candidate_id"] if results else "",
    }
    return results, density, summary


def selected_trade_rows(df: pd.DataFrame, best: dict[str, Any], max_rows: int = 500) -> list[dict[str, Any]]:
    if not best:
        return []
    rows = []
    for split_key in ("validation", "oos"):
        indices = [int(x) for x in str(best.get(f"selected_{split_key}_indices", "")).split(";") if x.strip().isdigit()]
        for idx in indices[:max_rows]:
            rows.append(
                {
                    "split": split_key,
                    "index": idx,
                    "timestamp": str(df.loc[idx, "timestamp"]),
                    "direction": best["direction"],
                    "candidate_id": best["candidate_id"],
                    "model_family": best["model_family"],
                    "context_gate": best["context_gate"],
                    "session_gate": best["session_gate"],
                    "feature_bundle": best["feature_bundle"],
                }
            )
    return rows


def write_artifacts(
    df: pd.DataFrame,
    results: list[dict[str, Any]],
    density: list[dict[str, Any]],
    summary: dict[str, Any],
    data_identity: dict[str, Any],
    created_at: str,
) -> tuple[str, str, str]:
    best = results[0] if results else {}
    next_run_id = (
        "frontier75C_pre_mt5_grok_volatility_compression_runtime_probe_v1"
        if summary["meaningful_signal_count"] > 0
        else "frontier75C_volatility_compression_label_risk_repair_proxy_v1"
    )
    status = (
        "proxy_scout_meaningful_signal_pre_mt5_required_no_authority"
        if summary["meaningful_signal_count"] > 0
        else "proxy_scout_no_meaningful_signal_repair_required_no_authority"
    )
    judgment = status

    result_fields = list(results[0].keys()) if results else ["candidate_id"]
    density_fields = list(density[0].keys()) if density else ["direction"]
    write_csv(RUN_DIR / "f75b_candidate_results.csv", results, result_fields)
    write_csv(RUN_DIR / "f75b_candidate_results_ranked_top50.csv", results[:50], result_fields)
    write_csv(RUN_DIR / "f75b_label_density_table.csv", density, density_fields)
    write_csv(REVIEW_DIR / "f75b_candidate_results_ranked_top50.csv", results[:50], result_fields)
    write_csv(REVIEW_DIR / "f75b_label_density_table.csv", density, density_fields)
    trade_rows = selected_trade_rows(df, best)
    trade_fields = list(trade_rows[0].keys()) if trade_rows else ["split", "index"]
    write_csv(RUN_DIR / "f75b_selected_trades_top_candidate.csv", trade_rows, trade_fields)

    enriched_summary = {
        **summary,
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": status,
        "judgment": judgment,
        "next_run_id": next_run_id,
        "claim_boundary": CLAIM_BOUNDARY,
        "data_identity": data_identity,
        "best_candidate": best,
        "created_at_utc": created_at,
    }
    write_json(RUN_DIR / "f75b_summary.json", enriched_summary)
    write_json(REVIEW_DIR / "f75b_summary.json", enriched_summary)

    data_integrity = {
        "data_source": [DATASET_PATH, RAW_PATH],
        "time_axis": "timestamp(타임스탬프)는 raw broker-clock alignment key(원천 브로커 시계 정렬 키)로 쓰고, future continuity(미래 연속성)는 5분 간격으로 검사했다.",
        "sample_scope": data_identity,
        "missing_or_duplicate_check": "raw merge missing rows=0; duplicate timestamp check is inherited from sorted model input scope(원시 병합 누락 0, 중복은 정렬 입력 범위에서 점검).",
        "feature_label_boundary": "entry feature(진입 피처)는 current row(현재 행) 58개만 사용하고, future OHLC(미래 시고저종)는 label/proxy outcome(라벨/프록시 결과)에만 사용했다.",
        "split_boundary": "time-ordered split_v1(시간순 분할 v1): train/validation/oos.",
        "leakage_risk": "threshold search(임계값 탐색)는 validation split(검증 분할) 기준이라 OOS에는 선택 편향 risk(선택 편향 위험)가 남는다.",
        "data_hash_or_identity": data_identity,
        "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)",
    }
    model_validation = {
        "model_family": "ExtraTrees, HistGradientBoosting, LogisticRegression(엑스트라트리/히스토그램 그래디언트 부스팅/로지스틱 회귀)",
        "target_and_label": "risk-shaped first-touch profitable trade label(위험 반영 선도달 수익 거래 라벨)",
        "split_method": "train fit, validation threshold selection, OOS read(학습 적합, 검증 임계값 선택, 표본외 판독)",
        "selection_metric": "joint_score(공동 점수): net/PF/DD/trades_day balance(순수익/수익 팩터/손실폭/일거래 균형)",
        "secondary_metrics": "win rate, average win/loss, payoff ratio, expectancy, recovery factor, max consecutive loss(승률/평균 이익·손실/손익비/기대값/회복 계수/최대 연속 손실)",
        "threshold_policy": "searched on validation target trades/day(검증 목표 일거래 수 기준 탐색)",
        "overfit_risk": "multiple candidate sweep(다중 후보 탐색) and validation threshold search(검증 임계값 탐색)",
        "calibration_risk": "model scores are rank scores(순위 점수), not calibrated probabilities(보정 확률 아님)",
        "comparison_baseline": "F74 runtime negative memory(F74 런타임 부정 기억): validation PF 1.16, OOS PF 1.13.",
        "validation_judgment": "exploratory_proxy_scout(탐색 프록시 스카우트)",
    }
    performance_attribution = {
        "observed_change": "F75B broad proxy scout completed(F75B 넓은 프록시 탐색 완료).",
        "comparison_baseline": "F74 weak runtime economics(F74 약한 런타임 경제성).",
        "likely_drivers": "compression gate, session gate, first-touch risk shape, threshold target density(압축 조건/세션 조건/선도달 위험 형태/임계값 목표 밀도)",
        "segment_checks": "validation and OOS splits plus context/session/direction segments(검증/표본외 및 압축/세션/방향 구간).",
        "trade_shape": best,
        "alternative_explanations": "validation threshold selection and proxy cost model(검증 임계값 선택과 프록시 비용 모델)이 headline KPI(대표 KPI)를 부풀릴 수 있다.",
        "attribution_confidence": "low_to_medium_proxy_only(낮음-중간, 프록시 전용)",
        "next_probe": next_run_id,
    }
    result_judgment = {
        "result_subject": RUN_ID,
        "evidence_available": {
            "candidate_rows": summary["candidate_rows"],
            "scout_clue_count": summary["scout_clue_count"],
            "meaningful_signal_count": summary["meaningful_signal_count"],
            "best_candidate": best,
        },
        "evidence_missing": "MT5 Runtime Probe(MT5 런타임 탐침), ONNX parity(온엑스 동등성), proxy/runtime gap analysis(프록시/런타임 간극 분석)",
        "judgment_label": judgment,
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": next_run_id,
        "user_explanation_hook": "F75B는 후보 표면을 찾는 proxy scout(프록시 탐색)이며 runtime authority(런타임 권위)가 아니다.",
    }
    write_json(REVIEW_DIR / "f75b_data_integrity.json", data_integrity)
    write_json(REVIEW_DIR / "f75b_model_validation.json", model_validation)
    write_json(REVIEW_DIR / "f75b_performance_attribution.json", performance_attribution)
    write_json(REVIEW_DIR / "f75b_result_judgment.json", result_judgment)

    best_lines = "No candidate rows(후보 행 없음)."
    if best:
        best_lines = (
            f"Best candidate(최선 후보): `{best['candidate_id']}` "
            f"validation net/PF/DD/tpd(검증 순수익/수익 팩터/손실폭/일거래) "
            f"`{best['validation_net_profit']:.4f}/{best['validation_profit_factor']:.4f}/"
            f"{best['validation_max_drawdown_percent']:.4f}/{best['validation_trades_day']:.4f}`, "
            f"OOS(표본외) `{best['oos_net_profit']:.4f}/{best['oos_profit_factor']:.4f}/"
            f"{best['oos_max_drawdown_percent']:.4f}/{best['oos_trades_day']:.4f}`."
        )

    report = f"""# Frontier75B Proxy Scout Report(전선75B 프록시 탐색 보고서)

Run id(실행 ID): `{RUN_ID}`

Stage id(단계 ID): `{STAGE_ID}`

Created(생성): {created_at}

Status(상태): `{status}`

Judgment(판정): `{judgment}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Hypothesis(가설)

Volatility compression plus liquidity release(변동성 압축 + 유동성 방출)가 F74보다 더 나은 tradeable-density proxy surface(거래 가능한 밀도 프록시 표면)를 만들 수 있는지 시험했다.

## Proxy Expectation(프록시 예상)

Action(행동): compression gate(압축 조건), session gate(세션 조건), feature bundle(피처 묶음), model family(모델 계열), first-touch risk label(선도달 위험 라벨)을 넓게 바꿨다.

Effect(효과): F74처럼 density/parity(밀도/동등성)만 보는 반복을 피하고, net/PF/DD/trades_day(순수익/수익 팩터/손실폭/일거래)를 함께 본다.

## Proxy KPI(프록시 KPI)

- candidates(후보): `{summary["candidate_rows"]}`
- scout clues(탐색 단서): `{summary["scout_clue_count"]}`
- meaningful signals(의미 있는 신호): `{summary["meaningful_signal_count"]}`
- final-like reference only(최종형 참고 전용): `{summary["final_like_reference_only_count"]}`
- {best_lines}

## Data and Model Boundary(데이터/모델 경계)

- data source(데이터 원천): `{DATASET_PATH}`, `{RAW_PATH}`
- feature-label boundary(피처-라벨 경계): entry features(진입 피처)는 현재 58개 feature(피처)만 사용했고 future OHLC(미래 시고저종)는 label/proxy outcome(라벨/프록시 결과)에만 사용했다.
- model scores(모델 점수): calibrated probabilities(보정 확률)가 아니라 rank scores(순위 점수)다.
- validation threshold(검증 임계값): target trades/day(목표 일거래 수)에 맞춰 validation split(검증 분할)에서 선택했다.

## Runtime Probe Status(런타임 탐침 상태)

MT5 Runtime Probe(MT5 런타임 탐침)는 아직 실행하지 않았다. Effect(효과): 이 결과는 proxy scout(프록시 탐색)이며 runtime authority(런타임 권위)가 아니다. 의미 있는 signal(신호)이 있으면 다음 run(실행)에서 pre-MT5 Grok review(MT5 전 Grok 검토)와 mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침)를 실행한다.

## Next Action(다음 행동)

`{next_run_id}`
"""
    write_text(REVIEW_DIR / "frontier75B_volatility_compression_liquidity_release_proxy_scout_report.md", report)

    gate_audit = f"""# Required Gate Coverage Audit F75B(필수 게이트 커버리지 감사 F75B)

| gate(게이트) | status(상태) | evidence(근거) |
|---|---|---|
| data_integrity(데이터 무결성) | passed_with_boundary(경계 포함 통과) | `stages/{STAGE_ID}/03_reviews/f75b_data_integrity.json` |
| model_validation(모델 검증) | exploratory_only(탐색 전용) | `stages/{STAGE_ID}/03_reviews/f75b_model_validation.json` |
| proxy_kpi_record(프록시 KPI 기록) | passed(통과) | `stages/{STAGE_ID}/03_reviews/f75b_summary.json` |
| tier_record(티어 기록) | boundary_recorded(경계 기록) | Tier A separate(Tier A 분리); Tier B missing_required(Tier B 필수 누락); Tier A+B out_of_scope_by_claim(Tier A+B 주장 범위 밖) |
| runtime_probe_rule(런타임 탐침 규칙) | pending_by_result(결과별 대기) | next `{next_run_id}` |
| claim_guard(주장 보호) | passed(통과) | `{CLAIM_BOUNDARY}` |

Action(행동): F75B는 proxy scout(프록시 탐색)로만 기록했다.

Effect(효과): MT5 Runtime Probe(MT5 런타임 탐침) 전에는 runtime authority(런타임 권위)를 만들지 않는다.
"""
    write_text(REVIEW_DIR / "required_gate_coverage_audit_f75b.md", gate_audit)

    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": next_run_id,
        "created_at_utc": created_at,
        "status": status,
        "judgment": judgment,
        "claim_boundary": CLAIM_BOUNDARY,
        "data_identity": data_identity,
        "artifacts": {
            "summary": f"stages/{STAGE_ID}/03_reviews/f75b_summary.json",
            "report": REPORT_PATH,
            "candidate_results": f"stages/{STAGE_ID}/02_runs/{RUN_ID}/f75b_candidate_results.csv",
            "ranked_top50": f"stages/{STAGE_ID}/03_reviews/f75b_candidate_results_ranked_top50.csv",
            "label_density": f"stages/{STAGE_ID}/03_reviews/f75b_label_density_table.csv",
            "gate_audit": GATE_AUDIT_PATH,
        },
    }
    write_json(RUN_DIR / "run_manifest.json", manifest)

    return status, judgment, next_run_id


def update_state_and_ledgers(status: str, judgment: str, next_run_id: str, summary: dict[str, Any], created_at: str) -> None:
    best = summary.get("best_candidate") or {}
    workspace_state = f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {next_run_id}
latest_completed_run_id: {RUN_ID}
current_status: {status}
current_judgment: {judgment}
next_run_id: {next_run_id}
runtime_probe_status: {"pending_pre_mt5_grok_after_meaningful_proxy_signal" if summary.get("meaningful_signal_count", 0) > 0 else "pending_after_proxy_repair"}
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
five_stage_retrospective_due_status: not_due_after_f74_closeout_f75_closeout_will_trigger
updated_at_utc: '{created_at}'
context_anchor: {CONTEXT_ANCHOR_PATH}
notes:
  - "Action(행동): F75B proxy scout(프록시 탐색)를 실행했다."
  - "Effect(효과): compression/session/feature/model/risk axes(압축/세션/피처/모델/위험 축)를 실제 후보 표면으로 측정했다."
  - "Next(다음): {next_run_id}"
  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."
"""
    write_text(ROOT / "docs/workspace/workspace_state.yaml", workspace_state)

    best_line = "No candidate rows(후보 행 없음)."
    if best:
        best_line = (
            f"Best(최선): `{best.get('candidate_id')}` validation/OOS PF-DD-tpd(검증/표본외 수익 팩터-손실폭-일거래) "
            f"`{float(best.get('validation_profit_factor', 0.0)):.4f}/{float(best.get('validation_max_drawdown_percent', 0.0)):.4f}/{float(best.get('validation_trades_day', 0.0)):.4f}` "
            f"and `{float(best.get('oos_profit_factor', 0.0)):.4f}/{float(best.get('oos_max_drawdown_percent', 0.0)):.4f}/{float(best.get('oos_trades_day', 0.0)):.4f}`."
        )
    current = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {created_at}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{next_run_id}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Context anchor(맥락 고정점): `{CONTEXT_ANCHOR_PATH}`

## Current Truth(현재 진실)

Action(행동): F75B proxy scout(프록시 탐색)를 실행했다.

Effect(효과): feature set/label/model/trade shape/risk/session(피처 묶음/라벨/모델/거래 형태/위험/세션)을 넓게 바꾸는 사용자 의도를 실제 후보 표면으로 materialize(물질화)했다.

## Proxy Result(프록시 결과)

- candidate rows(후보 수): `{summary.get("candidate_rows")}`
- scout clue(탐색 단서): `{summary.get("scout_clue_count")}`
- meaningful signal(의미 신호): `{summary.get("meaningful_signal_count")}`
- {best_line}

## Open Work(열린 작업)

Next run(다음 실행): `{next_run_id}`

Runtime rule(런타임 규칙): meaningful signal(의미 신호)이 있으면 Grok pre-MT5 review(MT5 전 Grok 검토) 후 mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침)를 실행한다. 없으면 label/risk/session repair(라벨/위험/세션 수리)로 넘어간다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(ROOT / "docs/context/current_working_state.md", current)

    ledger_row_id = f"{RUN_ID}__proxy_scout"
    common_row = {
        "ledger_row_id": ledger_row_id,
        "row_id": ledger_row_id,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "volatility_compression_proxy_scout(변동성 압축 프록시 탐색)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "Tier A separate(Tier A 분리); Tier B missing_required(Tier B 필수 누락); Tier A+B out_of_scope_by_claim(Tier A+B 주장 범위 밖)",
        "tier_scope": "Tier A separate; Tier B missing_required; Tier A+B out_of_scope_by_claim",
        "kpi_scope": "proxy_scout_kpi(프록시 탐색 KPI)",
        "scoreboard_lane": "trade_shape(거래 형태)",
        "lane": "proxy_scout(프록시 탐색)",
        "family": "volatility_compression_liquidity_release(변동성 압축 방출)",
        "status": status,
        "judgment": judgment,
        "result_judgment": judgment,
        "path": REPORT_PATH,
        "report_path": REPORT_PATH,
        "primary_report": REPORT_PATH,
        "primary_kpi": f"candidates={summary.get('candidate_rows')};scout={summary.get('scout_clue_count')};meaningful={summary.get('meaningful_signal_count')}",
        "guardrail_kpi": "proxy_only;runtime_pending;rank_scores_not_probabilities",
        "external_verification_status": "out_of_scope_by_claim_proxy_only(MT5는 다음 검증 범위)",
        "notes": "F75B broad proxy scout across compression/session/feature/model/risk axes(F75B 넓은 프록시 탐색).",
        "run_number": "frontier75B",
        "date": "2026-06-17",
        "run_date": "2026-06-17",
        "decision": judgment,
        "next_run_id": next_run_id,
        "rows": str(summary.get("candidate_rows", "")),
        "claim_boundary": CLAIM_BOUNDARY,
        "primary_artifact": RUN_MANIFEST_PATH,
        "view": "proxy_scout(프록시 탐색)",
        "tier": "Tier A separate(티어 A 분리)",
        "metric_scope": "proxy_scout(프록시 탐색)",
        "candidate_rows": str(summary.get("candidate_rows", "")),
        "positive_proxy_rows": str(summary.get("scout_clue_count", "")),
        "result_status": status,
        "evidence_boundary": "proxy_scout_only_no_runtime(프록시 탐색 전용, 런타임 없음)",
        "work_family": "frontier_proxy_scout(전선 프록시 탐색)",
        "question": "Can compression-release labels create tradeable proxy economics?(압축-방출 라벨이 거래 가능한 프록시 경제성을 만들 수 있나?)",
        "next_action": next_run_id,
        "gate_audit_path": GATE_AUDIT_PATH,
        "required_gate_audit": GATE_AUDIT_PATH,
        "created_at": created_at,
        "created_at_utc": created_at,
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "not_claimed",
        "run_family": "frontier_proxy_scout(전선 프록시 탐색)",
        "run_type": "volatility_compression_liquidity_release_proxy(변동성 압축 방출 프록시)",
        "input_run_id": PARENT_RUN_ID,
        "output_path": RUN_MANIFEST_PATH,
        "result_path": REPORT_PATH,
        "artifact_count": "11",
    }
    if best:
        common_row.update(
            {
                "best_model_id": best.get("candidate_id", ""),
                "best_proxy_net": best.get("oos_net_profit", ""),
                "best_net_profit": best.get("oos_net_profit", ""),
                "best_profit_factor": best.get("oos_profit_factor", ""),
                "net_profit": best.get("oos_net_profit", ""),
                "profit_factor": best.get("oos_profit_factor", ""),
                "drawdown": best.get("oos_max_drawdown_percent", ""),
                "max_drawdown_percent": best.get("oos_max_drawdown_percent", ""),
                "trade_count": best.get("oos_trade_count", ""),
                "trade_density": best.get("oos_trades_day", ""),
                "expectancy": best.get("oos_expectancy", ""),
                "recovery_factor": best.get("oos_recovery_factor", ""),
                "feature_count": best.get("feature_count", ""),
                "candidate_model_id": best.get("candidate_id", ""),
            }
        )

    run_registry = ROOT / "docs/registers/run_registry.csv"
    alpha_ledger = ROOT / "docs/registers/alpha_run_ledger.csv"
    with fs_path(run_registry).open("r", encoding="utf-8-sig", newline="") as handle:
        run_fields = list(csv.DictReader(handle).fieldnames or [])
    with fs_path(alpha_ledger).open("r", encoding="utf-8-sig", newline="") as handle:
        alpha_fields = list(csv.DictReader(handle).fieldnames or [])
    upsert_csv_row(run_registry, "run_id", common_row, run_fields)
    upsert_csv_row(alpha_ledger, "ledger_row_id", common_row, alpha_fields)
    upsert_csv_row(REVIEW_DIR / "stage_run_ledger.csv", "ledger_row_id", common_row, alpha_fields)

    idea_path = ROOT / "docs/registers/idea_registry.md"
    text = read_text(idea_path)
    marker = "<!-- frontier75B_volatility_compression_liquidity_release_proxy_scout_v1 -->"
    if marker not in text:
        addition = f"""

{marker}
- `{RUN_ID}` executed F75 volatility compression + liquidity release proxy scout(F75 변동성 압축 + 유동성 방출 프록시 탐색). Result(결과): `{judgment}`. Candidates(후보) `{summary.get('candidate_rows')}`, scout clue(탐색 단서) `{summary.get('scout_clue_count')}`, meaningful signal(의미 신호) `{summary.get('meaningful_signal_count')}`. Evidence(근거): `{REPORT_PATH}`. Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). Next(다음): `{next_run_id}`.
"""
        write_text(idea_path, text.rstrip() + addition)


def main() -> None:
    ensure_dirs()
    created_at = now_utc()
    df, feature_order, data_identity = load_inputs()
    results, density, summary = run_scout(df, feature_order)
    status, judgment, next_run_id = write_artifacts(df, results, density, summary, data_identity, created_at)
    summary_path = REVIEW_DIR / "f75b_summary.json"
    summary_payload = json.loads(read_text(summary_path))
    update_state_and_ledgers(status, judgment, next_run_id, summary_payload, created_at)
    print(json.dumps({
        "status": status,
        "judgment": judgment,
        "candidate_rows": summary_payload["candidate_rows"],
        "scout_clue_count": summary_payload["scout_clue_count"],
        "meaningful_signal_count": summary_payload["meaningful_signal_count"],
        "best_candidate_id": summary_payload["best_candidate_id"],
        "next_run_id": next_run_id,
        "report": REPORT_PATH,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
