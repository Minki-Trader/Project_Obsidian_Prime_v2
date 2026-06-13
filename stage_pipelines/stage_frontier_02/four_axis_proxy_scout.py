from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready
from foundation.models.onnx_bridge import ordered_hash, sha256_file


STAGE_ID = "stage_frontier_02__four_axis_joint_onnx_proxy_scout"
RUN_ID = "frontier02B_proxy_scout_execution_v1"
RUN_NUMBER = "frontier02B"
EXPLORATION_LABEL = "stage_frontier_02__four_axis_joint_onnx_proxy_scout"
DATASET_PATH = Path(
    "data/processed/model_inputs/"
    "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/"
    "model_input_dataset.parquet"
)
FEATURE_ORDER_PATH = DATASET_PATH.with_name("model_input_feature_order.txt")
FEATURE_MANIFEST_PATH = DATASET_PATH.with_name("feature_set_manifest.json")
MODEL_INPUT_SUMMARY_PATH = DATASET_PATH.with_name("model_input_summary.json")
RUN_ROOT = Path("stages") / STAGE_ID / "02_runs" / RUN_ID
REPORT_PATH = Path("stages") / STAGE_ID / "03_reviews" / f"{RUN_ID}_report.md"
EXPECTED_FEATURE_HASH = "fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2"
ROUGH_COST_LOG_RETURN = 0.00005
HOLD_BARS = 12
QUANTILES = (0.70, 0.75, 0.80, 0.85, 0.90, 0.95)
COOLDOWN_BARS = (6, 12, 18)
SIDE_MODES = ("both", "long_only", "short_only")
DENSITY_TARGET_LOW = 5.0
DENSITY_TARGET_HIGH = 10.0
PF_TARGET = 2.0
DD_TARGET_PERCENT = 10.0


@dataclass(frozen=True)
class SurfaceSpec:
    name: str
    components: tuple[tuple[str, float], ...]
    filters: tuple[str, ...]


SURFACES: tuple[SurfaceSpec, ...] = (
    SurfaceSpec(
        name="trend_follow_joint",
        components=(
            ("ema20_ema50_diff", 1.0),
            ("ema50_ema200_diff", 0.55),
            ("di_spread_14", 0.9),
            ("ppo_hist_12_26_9", 0.8),
            ("roc_12", 0.65),
            ("supertrend_10_3", 0.35),
        ),
        filters=("all_cash", "mid_cash", "trend_adx_ge20", "normal_vol"),
    ),
    SurfaceSpec(
        name="short_horizon_continuation",
        components=(
            ("log_return_3", 1.0),
            ("return_zscore_20", 0.8),
            ("rsi_14_minus_50", 0.55),
            ("stoch_kd_diff", 0.45),
            ("top3_weighted_return_1", 0.7),
        ),
        filters=("all_cash", "early_cash", "mid_cash", "normal_vol"),
    ),
    SurfaceSpec(
        name="mean_reversion_joint",
        components=(
            ("return_zscore_20", -1.0),
            ("bb_position_20", -0.8),
            ("rsi_14_minus_50", -0.65),
            ("stochrsi_kd_diff", -0.35),
            ("historical_vol_5_over_20", 0.25),
        ),
        filters=("all_cash", "quiet_adx_lt20", "normal_vol", "early_cash"),
    ),
    SurfaceSpec(
        name="squeeze_breakout_joint",
        components=(
            ("bb_squeeze", 0.45),
            ("roc_12", 0.9),
            ("di_spread_14", 0.8),
            ("ppo_hist_12_26_9", 0.7),
            ("historical_vol_5_over_20", 0.4),
        ),
        filters=("squeeze_only", "all_cash", "mid_cash", "trend_adx_ge20"),
    ),
    SurfaceSpec(
        name="macro_confirmation_joint",
        components=(
            ("mega8_pos_breadth_1", 0.75),
            ("mega8_equal_return_1", 0.7),
            ("top3_weighted_return_1", 0.85),
            ("us100_minus_top3_weighted_return_1", 0.55),
            ("vix_zscore_20", -0.35),
            ("us10yr_zscore_20", -0.2),
        ),
        filters=("all_cash", "mid_cash", "normal_vol", "last_30m"),
    ),
    SurfaceSpec(
        name="risk_off_counter_reversion",
        components=(
            ("vix_zscore_20", 0.55),
            ("usdx_zscore_20", 0.3),
            ("return_zscore_20", -0.8),
            ("bb_position_20", -0.6),
            ("atr_14_over_atr_50", 0.35),
        ),
        filters=("all_cash", "early_cash", "quiet_adx_lt20", "normal_vol"),
    ),
)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    payload = run_proxy_scout(output_root=Path(args.output_root) if args.output_root else RUN_ROOT)
    print(json.dumps(json_ready(payload), ensure_ascii=False, indent=2))
    return 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Frontier02 four-axis proxy scout.")
    parser.add_argument("--output-root", default=str(RUN_ROOT))
    return parser.parse_args(argv)


def run_proxy_scout(*, output_root: Path) -> dict[str, Any]:
    io_path(output_root).mkdir(parents=True, exist_ok=True)
    frame = load_and_validate_input()
    feature_order = read_feature_order(FEATURE_ORDER_PATH)
    z_frame = build_train_standardized_features(frame, feature_order)
    filters = build_filters(frame)
    metrics = evaluate_surface_grid(frame, z_frame, filters)
    summary = build_candidate_summary(metrics)
    top = summary.sort_values(
        ["validation_aspiration_distance_score", "validation_joint_pass_count", "oos_aspiration_distance_score"],
        ascending=[True, False, True],
    ).head(20)
    artifacts = write_artifacts(output_root, frame, feature_order, metrics, summary, top)
    report = write_report(metrics, summary, top, artifacts)
    manifest = write_manifest(output_root, frame, feature_order, artifacts, report)
    return {
        "status": "completed",
        "run_id": RUN_ID,
        "output_root": output_root.as_posix(),
        "candidate_rows": int(len(summary)),
        "metric_rows": int(len(metrics)),
        "top_surface": dict(top.iloc[0]) if len(top) else {},
        "manifest": manifest,
        "report": report,
    }


def load_and_validate_input() -> pd.DataFrame:
    if not io_path(DATASET_PATH).exists():
        raise FileNotFoundError(DATASET_PATH)
    frame = pd.read_parquet(io_path(DATASET_PATH))
    required = {"timestamp", "split", "future_log_return_12", "label", "label_class"}
    missing = sorted(required - set(frame.columns))
    if missing:
        raise ValueError(f"Missing required input columns: {missing}")
    frame = frame.sort_values("timestamp").reset_index(drop=True)
    if frame["timestamp"].isna().any():
        raise ValueError("Input contains missing timestamps.")
    if frame["timestamp"].duplicated().any():
        raise ValueError("Input contains duplicate timestamps.")
    if set(frame["split"].dropna().astype(str)) != {"train", "validation", "oos"}:
        raise ValueError("Input split must contain exactly train, validation, and oos.")
    return frame


def read_feature_order(path: Path) -> list[str]:
    features = [line.strip() for line in io_path(path).read_text(encoding="utf-8-sig").splitlines() if line.strip()]
    feature_hash = ordered_hash(features)
    if feature_hash != EXPECTED_FEATURE_HASH:
        raise ValueError(f"Feature order hash mismatch: {feature_hash} != {EXPECTED_FEATURE_HASH}")
    return features


def build_train_standardized_features(frame: pd.DataFrame, feature_order: list[str]) -> pd.DataFrame:
    train_mask = frame["split"].astype(str).eq("train")
    out = pd.DataFrame(index=frame.index)
    for column in feature_order:
        series = pd.to_numeric(frame[column], errors="coerce").astype("float64")
        train_values = series.loc[train_mask].replace([np.inf, -np.inf], np.nan).dropna()
        mean = float(train_values.mean()) if len(train_values) else 0.0
        std = float(train_values.std(ddof=0)) if len(train_values) else 1.0
        if not math.isfinite(std) or std <= 1e-12:
            std = 1.0
        out[column] = ((series - mean) / std).replace([np.inf, -np.inf], np.nan).fillna(0.0)
    return out


def build_filters(frame: pd.DataFrame) -> dict[str, pd.Series]:
    train = frame["split"].astype(str).eq("train")
    atr = pd.to_numeric(frame["atr_14_over_atr_50"], errors="coerce")
    low, high = atr.loc[train].quantile([0.20, 0.80]).tolist()
    cash = pd.to_numeric(frame["is_us_cash_open"], errors="coerce").fillna(0).eq(1)
    first = pd.to_numeric(frame["is_first_30m_after_open"], errors="coerce").fillna(0).eq(1)
    last = pd.to_numeric(frame["is_last_30m_before_cash_close"], errors="coerce").fillna(0).eq(1)
    adx = pd.to_numeric(frame["adx_14"], errors="coerce")
    squeeze = pd.to_numeric(frame["bb_squeeze"], errors="coerce").fillna(0).eq(1)
    return {
        "all_cash": cash,
        "early_cash": cash & first,
        "mid_cash": cash & ~first & ~last,
        "last_30m": cash & last,
        "trend_adx_ge20": cash & adx.ge(20),
        "quiet_adx_lt20": cash & adx.lt(20),
        "squeeze_only": cash & squeeze,
        "normal_vol": cash & atr.ge(low) & atr.le(high),
    }


def evaluate_surface_grid(frame: pd.DataFrame, z_frame: pd.DataFrame, filters: dict[str, pd.Series]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for surface in SURFACES:
        score = build_surface_score(z_frame, surface)
        for filter_name in surface.filters:
            filter_mask = filters[filter_name].fillna(False).to_numpy(dtype=bool)
            train_mask = frame["split"].astype(str).eq("train").to_numpy(dtype=bool) & filter_mask
            train_abs = np.abs(score[train_mask])
            train_abs = train_abs[np.isfinite(train_abs)]
            if len(train_abs) < 100:
                continue
            for quantile in QUANTILES:
                threshold = float(np.quantile(train_abs, quantile))
                if not math.isfinite(threshold) or threshold <= 0:
                    continue
                for side_mode in SIDE_MODES:
                    raw_signal = signal_from_score(score, threshold, filter_mask, side_mode)
                    for cooldown in COOLDOWN_BARS:
                        signal = apply_cooldown(raw_signal, cooldown)
                        candidate_id = candidate_key(surface.name, filter_name, side_mode, quantile, cooldown)
                        for split in ("train", "validation", "oos"):
                            rows.append(
                                evaluate_split(
                                    frame,
                                    signal,
                                    split=split,
                                    candidate_id=candidate_id,
                                    surface=surface,
                                    filter_name=filter_name,
                                    side_mode=side_mode,
                                    quantile=quantile,
                                    threshold=threshold,
                                    cooldown=cooldown,
                                )
                            )
    metrics = pd.DataFrame(rows)
    if metrics.empty:
        raise RuntimeError("Proxy scout produced no metric rows.")
    metrics["validation_selector_boundary"] = np.where(
        metrics["split"].eq("validation"),
        "ranked_for_next_inspection",
        "diagnostic_not_selector",
    )
    return metrics


def build_surface_score(z_frame: pd.DataFrame, surface: SurfaceSpec) -> np.ndarray:
    score = np.zeros(len(z_frame), dtype="float64")
    total_weight = 0.0
    for column, weight in surface.components:
        score += float(weight) * z_frame[column].to_numpy(dtype="float64")
        total_weight += abs(float(weight))
    return score / max(total_weight, 1e-9)


def signal_from_score(score: np.ndarray, threshold: float, filter_mask: np.ndarray, side_mode: str) -> np.ndarray:
    signal = np.zeros(len(score), dtype="int8")
    if side_mode in {"both", "long_only"}:
        signal[(score >= threshold) & filter_mask] = 1
    if side_mode in {"both", "short_only"}:
        signal[(score <= -threshold) & filter_mask] = -1
    return signal


def apply_cooldown(raw_signal: np.ndarray, cooldown_bars: int) -> np.ndarray:
    signal = np.zeros(len(raw_signal), dtype="int8")
    next_allowed = 0
    for index, value in enumerate(raw_signal):
        if value == 0 or index < next_allowed:
            continue
        signal[index] = value
        next_allowed = index + int(cooldown_bars) + 1
    return signal


def evaluate_split(
    frame: pd.DataFrame,
    signal: np.ndarray,
    *,
    split: str,
    candidate_id: str,
    surface: SurfaceSpec,
    filter_name: str,
    side_mode: str,
    quantile: float,
    threshold: float,
    cooldown: int,
) -> dict[str, Any]:
    split_mask = frame["split"].astype(str).eq(split).to_numpy(dtype=bool)
    split_frame = frame.loc[split_mask, ["timestamp", "future_log_return_12"]].copy()
    split_signal = signal[split_mask].astype("int8")
    trade_mask = split_signal != 0
    days = count_scope_days(split_frame["timestamp"])
    pnl = (
        split_signal.astype("float64")
        * pd.to_numeric(split_frame["future_log_return_12"], errors="coerce").to_numpy(dtype="float64")
        - (trade_mask.astype("float64") * ROUGH_COST_LOG_RETURN)
    )
    trade_pnl = pnl[trade_mask]
    trade_times = split_frame.loc[trade_mask, "timestamp"]
    metrics = trade_metrics(trade_pnl, trade_times)
    trade_count = int(len(trade_pnl))
    trades_per_day = float(trade_count / days) if days else 0.0
    sparse_floor = max(30, int(math.ceil(days)))
    sparse_flag = trade_count < sparse_floor
    pf999_sparse_flag = bool(metrics["profit_factor"] >= 999.0 and sparse_flag)
    density_distance = density_axis_distance(trades_per_day)
    pf_distance = profit_factor_axis_distance(metrics["profit_factor"], trade_count, sparse_flag, pf999_sparse_flag)
    dd_risk = max(float(metrics["max_drawdown_percent"]), float(metrics["max_monthly_drawdown_percent"]))
    dd_distance = max(0.0, (dd_risk - DD_TARGET_PERCENT) / DD_TARGET_PERCENT)
    smoothness_distance = smoothness_axis_distance(metrics)
    aspiration_score = density_distance + pf_distance + dd_distance + smoothness_distance
    density_pass = DENSITY_TARGET_LOW <= trades_per_day <= DENSITY_TARGET_HIGH
    pf_pass = metrics["profit_factor"] >= PF_TARGET and not sparse_flag and metrics["net_profit"] > 0
    dd_pass = dd_risk < DD_TARGET_PERCENT
    smoothness_pass = (
        metrics["net_profit"] > 0
        and metrics["underwater_ratio"] <= 0.45
        and metrics["equity_trend_r2"] >= 0.35
        and metrics["max_loss_streak"] <= 6
    )
    return {
        "candidate_id": candidate_id,
        "surface": surface.name,
        "filter_name": filter_name,
        "side_mode": side_mode,
        "threshold_quantile": float(quantile),
        "threshold_value": threshold,
        "cooldown_bars": int(cooldown),
        "hold_bars": HOLD_BARS,
        "split": split,
        "tier_scope": "Tier A",
        "record_view": "Tier A separate",
        "trade_count": trade_count,
        "days_in_scope": days,
        "trades_per_day": trades_per_day,
        "sparse_floor": sparse_floor,
        "sparse_flag": bool(sparse_flag),
        "pf999_sparse_flag": pf999_sparse_flag,
        "long_trade_count": int((split_signal == 1).sum()),
        "short_trade_count": int((split_signal == -1).sum()),
        "net_profit": metrics["net_profit"],
        "profit_factor": metrics["profit_factor"],
        "expectancy": metrics["expectancy"],
        "win_rate": metrics["win_rate"],
        "max_drawdown_percent": metrics["max_drawdown_percent"],
        "max_monthly_drawdown_percent": metrics["max_monthly_drawdown_percent"],
        "underwater_ratio": metrics["underwater_ratio"],
        "max_loss_streak": metrics["max_loss_streak"],
        "equity_trend_r2": metrics["equity_trend_r2"],
        "density_axis_distance": density_distance,
        "pf_axis_distance": pf_distance,
        "dd_axis_distance": dd_distance,
        "smoothness_axis_distance": smoothness_distance,
        "aspiration_distance_score": aspiration_score,
        "density_pass": bool(density_pass),
        "pf_pass": bool(pf_pass),
        "dd_pass": bool(dd_pass),
        "smoothness_pass": bool(smoothness_pass),
        "joint_pass_count": int(density_pass) + int(pf_pass) + int(dd_pass) + int(smoothness_pass),
        "proxy_cost_log_return": ROUGH_COST_LOG_RETURN,
    }


def trade_metrics(trade_pnl: np.ndarray, trade_times: pd.Series) -> dict[str, Any]:
    trade_pnl = np.asarray(trade_pnl, dtype="float64")
    if trade_pnl.size == 0:
        return {
            "net_profit": 0.0,
            "profit_factor": 0.0,
            "expectancy": 0.0,
            "win_rate": 0.0,
            "max_drawdown_percent": 0.0,
            "max_monthly_drawdown_percent": 0.0,
            "underwater_ratio": 1.0,
            "max_loss_streak": 0,
            "equity_trend_r2": 0.0,
        }
    wins = trade_pnl[trade_pnl > 0]
    losses = trade_pnl[trade_pnl < 0]
    gross_profit = float(wins.sum()) if len(wins) else 0.0
    gross_loss = float(losses.sum()) if len(losses) else 0.0
    profit_factor = 999.0 if gross_loss == 0 and gross_profit > 0 else (gross_profit / abs(gross_loss) if gross_loss else 0.0)
    equity = np.cumsum(trade_pnl)
    peak = np.maximum.accumulate(np.maximum(equity, 0.0))
    drawdown_log = np.maximum(peak - equity, 0.0)
    max_drawdown_percent = 100.0 * (1.0 - math.exp(-float(drawdown_log.max()))) if len(drawdown_log) else 0.0
    underwater_ratio = float(np.mean(drawdown_log > 1e-12)) if len(drawdown_log) else 1.0
    max_loss_streak = longest_loss_streak(trade_pnl)
    r2 = equity_trend_r2(equity)
    monthly_dd = max_monthly_drawdown_percent(trade_pnl, trade_times)
    return {
        "net_profit": float(trade_pnl.sum()),
        "profit_factor": float(profit_factor),
        "expectancy": float(trade_pnl.mean()),
        "win_rate": float(len(wins) / len(trade_pnl)),
        "max_drawdown_percent": float(max_drawdown_percent),
        "max_monthly_drawdown_percent": float(monthly_dd),
        "underwater_ratio": underwater_ratio,
        "max_loss_streak": int(max_loss_streak),
        "equity_trend_r2": float(r2),
    }


def max_monthly_drawdown_percent(trade_pnl: np.ndarray, trade_times: pd.Series) -> float:
    if len(trade_pnl) == 0:
        return 0.0
    times = pd.to_datetime(trade_times).reset_index(drop=True).dt.tz_convert("America/New_York").dt.tz_localize(None)
    months = times.dt.to_period("M")
    max_dd = 0.0
    pnl_series = pd.Series(trade_pnl)
    for _, values in pnl_series.groupby(months):
        equity = values.cumsum().to_numpy(dtype="float64")
        peak = np.maximum.accumulate(np.maximum(equity, 0.0))
        dd = np.maximum(peak - equity, 0.0)
        if len(dd):
            max_dd = max(max_dd, float(dd.max()))
    return 100.0 * (1.0 - math.exp(-max_dd))


def longest_loss_streak(values: np.ndarray) -> int:
    best = 0
    current = 0
    for value in values:
        if value < 0:
            current += 1
            best = max(best, current)
        else:
            current = 0
    return best


def equity_trend_r2(equity: np.ndarray) -> float:
    if len(equity) < 3 or float(np.var(equity)) <= 1e-18:
        return 0.0
    x = np.arange(len(equity), dtype="float64")
    corr = np.corrcoef(x, equity)[0, 1]
    if not math.isfinite(float(corr)):
        return 0.0
    return float(corr * corr)


def density_axis_distance(trades_per_day: float) -> float:
    if DENSITY_TARGET_LOW <= trades_per_day <= DENSITY_TARGET_HIGH:
        return 0.0
    if trades_per_day < DENSITY_TARGET_LOW:
        return (DENSITY_TARGET_LOW - trades_per_day) / DENSITY_TARGET_LOW
    return (trades_per_day - DENSITY_TARGET_HIGH) / DENSITY_TARGET_HIGH


def profit_factor_axis_distance(profit_factor: float, trade_count: int, sparse_flag: bool, pf999_sparse_flag: bool) -> float:
    if trade_count <= 0:
        return 2.0
    sparse_penalty = 0.35 if sparse_flag else 0.0
    if pf999_sparse_flag:
        return 2.0 + sparse_penalty
    if profit_factor >= PF_TARGET:
        return sparse_penalty
    return ((PF_TARGET - max(profit_factor, 0.0)) / PF_TARGET) + sparse_penalty


def smoothness_axis_distance(metrics: dict[str, Any]) -> float:
    if metrics["net_profit"] <= 0:
        net_penalty = 1.0
    else:
        net_penalty = 0.0
    return float(
        net_penalty
        + 0.45 * (1.0 - min(max(metrics["equity_trend_r2"], 0.0), 1.0))
        + 0.45 * min(max(metrics["underwater_ratio"], 0.0), 1.0)
        + 0.10 * min(metrics["max_loss_streak"] / 10.0, 1.0)
    )


def count_scope_days(timestamps: pd.Series) -> int:
    local_dates = pd.to_datetime(timestamps).dt.tz_convert("America/New_York").dt.date
    return int(local_dates.nunique())


def build_candidate_summary(metrics: pd.DataFrame) -> pd.DataFrame:
    keys = ["candidate_id", "surface", "filter_name", "side_mode", "threshold_quantile", "cooldown_bars", "hold_bars"]
    summary_rows: list[dict[str, Any]] = []
    for key_values, group in metrics.groupby(keys, sort=False):
        base = dict(zip(keys, key_values))
        for split in ("train", "validation", "oos"):
            row = group.loc[group["split"].eq(split)]
            if row.empty:
                continue
            item = row.iloc[0]
            for column in (
                "trade_count",
                "days_in_scope",
                "trades_per_day",
                "sparse_flag",
                "pf999_sparse_flag",
                "net_profit",
                "profit_factor",
                "expectancy",
                "win_rate",
                "max_drawdown_percent",
                "max_monthly_drawdown_percent",
                "underwater_ratio",
                "max_loss_streak",
                "equity_trend_r2",
                "aspiration_distance_score",
                "joint_pass_count",
                "density_pass",
                "pf_pass",
                "dd_pass",
                "smoothness_pass",
            ):
                base[f"{split}_{column}"] = item[column]
        base["non_sparse_validation_oos"] = bool(
            not base.get("validation_sparse_flag", True) and not base.get("oos_sparse_flag", True)
        )
        base["positive_validation_oos"] = bool(base.get("validation_net_profit", 0) > 0 and base.get("oos_net_profit", 0) > 0)
        base["scout_clue_flag"] = bool(
            base["non_sparse_validation_oos"]
            and base["positive_validation_oos"]
            and float(base.get("validation_aspiration_distance_score", 99.0)) < 2.75
            and float(base.get("oos_aspiration_distance_score", 99.0)) < 3.25
        )
        summary_rows.append(base)
    summary = pd.DataFrame(summary_rows)
    summary["validation_rank"] = summary["validation_aspiration_distance_score"].rank(method="first")
    return summary


def write_artifacts(
    output_root: Path,
    frame: pd.DataFrame,
    feature_order: list[str],
    metrics: pd.DataFrame,
    summary: pd.DataFrame,
    top: pd.DataFrame,
) -> dict[str, dict[str, Any]]:
    artifacts: dict[str, dict[str, Any]] = {}
    metrics_path = output_root / "candidate_surface_metrics.csv"
    summary_path = output_root / "candidate_surface_summary.csv"
    top_path = output_root / "top_seed_surfaces.csv"
    input_audit_path = output_root / "input_integrity_audit.json"
    score_contract_path = output_root / "score_contract.json"
    metrics.to_csv(io_path(metrics_path), index=False, lineterminator="\n")
    summary.to_csv(io_path(summary_path), index=False, lineterminator="\n")
    top.to_csv(io_path(top_path), index=False, lineterminator="\n")
    input_audit = {
        "status": "pass",
        "dataset_path": DATASET_PATH.as_posix(),
        "dataset_sha256": sha256_file(DATASET_PATH),
        "rows": int(len(frame)),
        "split_counts": {str(k): int(v) for k, v in frame["split"].value_counts().to_dict().items()},
        "first_timestamp": pd.to_datetime(frame["timestamp"].min()).isoformat(),
        "last_timestamp": pd.to_datetime(frame["timestamp"].max()).isoformat(),
        "feature_order_path": FEATURE_ORDER_PATH.as_posix(),
        "feature_order_hash": ordered_hash(feature_order),
        "feature_count": len(feature_order),
        "model_input_summary_path": MODEL_INPUT_SUMMARY_PATH.as_posix(),
        "feature_manifest_path": FEATURE_MANIFEST_PATH.as_posix(),
        "label_boundary": "features_closed_bar_label_fwd12_proxy_scoring_only",
        "split_boundary": "train_thresholds_validation_rank_oos_diagnostic",
    }
    write_json(input_audit_path, input_audit)
    score_contract = {
        "density_target_trades_per_day": [DENSITY_TARGET_LOW, DENSITY_TARGET_HIGH],
        "profit_factor_target_low": PF_TARGET,
        "drawdown_target_percent": DD_TARGET_PERCENT,
        "rough_cost_log_return": ROUGH_COST_LOG_RETURN,
        "hold_bars": HOLD_BARS,
        "quantiles": list(QUANTILES),
        "cooldown_bars": list(COOLDOWN_BARS),
        "side_modes": list(SIDE_MODES),
        "selection_boundary": "validation_rank_only_oos_diagnostic_no_completion_claim",
    }
    write_json(score_contract_path, score_contract)
    for role, path in (
        ("candidate_surface_metrics", metrics_path),
        ("candidate_surface_summary", summary_path),
        ("top_seed_surfaces", top_path),
        ("input_integrity_audit", input_audit_path),
        ("score_contract", score_contract_path),
    ):
        artifacts[role] = {"path": path.as_posix(), "sha256": sha256_file(path)}
    return artifacts


def write_report(
    metrics: pd.DataFrame,
    summary: pd.DataFrame,
    top: pd.DataFrame,
    artifacts: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    io_path(REPORT_PATH.parent).mkdir(parents=True, exist_ok=True)
    best = top.iloc[0].to_dict()
    clue_count = int(summary["scout_clue_flag"].sum())
    val_rows = metrics.loc[metrics["split"].eq("validation")]
    oos_rows = metrics.loc[metrics["split"].eq("oos")]
    lines = [
        "# frontier02B Proxy Scout Report(전선02B 프록시 탐색 보고)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- status(상태): `completed_proxy_scout_no_authority(프록시 탐색 완료, 권위 없음)`",
        f"- metric_rows(측정 행): `{len(metrics)}`",
        f"- candidate_rows(후보 표면 행): `{len(summary)}`",
        f"- scout_clue_rows(탐색 단서 행): `{clue_count}`",
        "",
        "## Boundary(경계)",
        "",
        "이번 실행(run, 실행)은 cheap proxy replay(저비용 프록시 재생)입니다. ONNX model training(온엑스 모델 학습), WFO(워크포워드 최적화), MT5 runtime validation(MT5 런타임 검증), baseline selection(기준선 선택), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 주장하지 않습니다.",
        "",
        "## Best Validation Rank(검증 순위 1위)",
        "",
        f"- candidate_id(후보 ID): `{best.get('candidate_id')}`",
        f"- surface/filter/side(표면/필터/방향): `{best.get('surface')}` / `{best.get('filter_name')}` / `{best.get('side_mode')}`",
        f"- validation score(검증 점수): `{format_float(best.get('validation_aspiration_distance_score'))}`",
        f"- validation net/PF/density/DD(검증 순수익/수익 팩터/밀도/손실폭): `{format_float(best.get('validation_net_profit'))}` / `{format_float(best.get('validation_profit_factor'))}` / `{format_float(best.get('validation_trades_per_day'))}` / `{format_float(best.get('validation_max_drawdown_percent'))}%`",
        f"- OOS net/PF/density/DD(표본외 순수익/수익 팩터/밀도/손실폭): `{format_float(best.get('oos_net_profit'))}` / `{format_float(best.get('oos_profit_factor'))}` / `{format_float(best.get('oos_trades_per_day'))}` / `{format_float(best.get('oos_max_drawdown_percent'))}%`",
        f"- joint_pass_count(동시 통과 수): validation(검증) `{best.get('validation_joint_pass_count')}`, OOS(표본외) `{best.get('oos_joint_pass_count')}`",
        "",
        "## Read(판독)",
        "",
        scout_read(clue_count),
        "",
        "## Artifacts(산출물)",
        "",
    ]
    for role, record in artifacts.items():
        lines.append(f"- {role}: `{record['path']}` sha256(해시) `{record['sha256']}`")
    lines.extend(
        [
            "",
            "## Gate Boundary(게이트 경계)",
            "",
            "- Tier A separate(Tier A 분리): materialized(물질화)",
            "- Tier B separate(Tier B 분리): 이번 proxy run(프록시 실행)에서는 partial-context Tier B artifact(부분 문맥 Tier B 산출물)를 만들지 않았으므로 `missing_required(필수 누락)`입니다.",
            "- Tier A+B combined(Tier A+B 합산): routed Tier B fallback(라우팅 Tier B 대체)을 실행하지 않았으므로 `out_of_scope_by_claim(주장 범위 밖)`입니다.",
            "- Grok pre-expensive review(비싼 검증 전 그록 검토): 이번 cheap proxy replay(저비용 프록시 재생)에는 not required(필요 없음)입니다. WFO/MT5(워크포워드/MT5) 전에는 required(필요)입니다.",
        ]
    )
    io_path(REPORT_PATH).write_text("\n".join(lines) + "\n", encoding="utf-8-sig")
    return {"path": REPORT_PATH.as_posix(), "sha256": sha256_file(REPORT_PATH)}


def scout_read(clue_count: int) -> str:
    if clue_count > 0:
        return "Scout clue(탐색 단서)는 있습니다. 다만 proxy-only(프록시 전용)라서 다음 행동(action, 행동)은 seed surface(씨앗 표면)를 학습 가능한 ONNX-ready surface(온엑스 준비 표면)로 바꾸는 것입니다."
    return "Scout clue(탐색 단서)는 아직 약합니다. 다음 행동(action, 행동)은 점수 표면(score surface, 점수 표면)을 넓히거나 label/threshold contract(라벨/임계값 계약)를 수리하는 것입니다."


def write_manifest(
    output_root: Path,
    frame: pd.DataFrame,
    feature_order: list[str],
    artifacts: dict[str, dict[str, Any]],
    report: dict[str, Any],
) -> dict[str, Any]:
    manifest_path = output_root / "run_manifest.json"
    manifest = {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "exploration_label": EXPLORATION_LABEL,
        "status": "completed_proxy_scout_no_authority",
        "created_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "script_path": "stage_pipelines/stage_frontier_02/four_axis_proxy_scout.py",
        "script_sha256": sha256_file(Path("stage_pipelines/stage_frontier_02/four_axis_proxy_scout.py")),
        "inputs": {
            "model_input_dataset_path": DATASET_PATH.as_posix(),
            "model_input_dataset_sha256": sha256_file(DATASET_PATH),
            "feature_order_path": FEATURE_ORDER_PATH.as_posix(),
            "feature_order_hash": ordered_hash(feature_order),
            "rows": int(len(frame)),
            "split_counts": {str(k): int(v) for k, v in frame["split"].value_counts().to_dict().items()},
        },
        "proxy_contract": {
            "rough_cost_log_return": ROUGH_COST_LOG_RETURN,
            "hold_bars": HOLD_BARS,
            "density_target_trades_per_day": [DENSITY_TARGET_LOW, DENSITY_TARGET_HIGH],
            "profit_factor_target_low": PF_TARGET,
            "drawdown_target_percent": DD_TARGET_PERCENT,
            "selector_scope": "validation_only",
            "oos_use": "diagnostic_only",
        },
        "outputs": artifacts,
        "report": report,
        "external_verification_status": "out_of_scope_by_claim_no_mt5",
        "forbidden_claims": [
            "completion",
            "selected_baseline",
            "operating_promotion",
            "runtime_authority",
            "live_readiness",
            "goal_achieve",
        ],
    }
    write_json(manifest_path, manifest)
    return {"path": manifest_path.as_posix(), "sha256": sha256_file(manifest_path)}


def write_json(path: Path, payload: dict[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def candidate_key(surface: str, filter_name: str, side_mode: str, quantile: float, cooldown: int) -> str:
    q_text = str(int(round(quantile * 100)))
    return f"{surface}__{filter_name}__{side_mode}__q{q_text}__cd{cooldown}"


def format_float(value: Any) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return "NA"
    if not math.isfinite(number):
        return "NA"
    return f"{number:.6g}"


if __name__ == "__main__":
    raise SystemExit(main())
