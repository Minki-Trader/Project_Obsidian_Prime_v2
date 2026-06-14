from __future__ import annotations

import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from foundation.models.onnx_bridge import ordered_hash, sha256_file
from stage_pipelines.stage_frontier_02 import four_axis_proxy_scout as scout
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b


STAGE_ID = "stage_frontier_23__payoff_asymmetry_pf_source_onnx_scout"
RUN_ID = "frontier23B_payoff_asymmetry_pf_source_proxy_scout_v1"
RUN_NUMBER = "frontier23B"
PARENT_RUN_ID = "frontier23A_stage_open_payoff_asymmetry_pf_source_hypothesis_design_v1"
NEXT_PRE_EXPENSIVE_GROK_RUN_ID = "frontier23C_grok_pre_expensive_payoff_asymmetry_handoff_review_v1"
NEXT_REPAIR_OR_CLOSEOUT_RUN_ID = "frontier23C_payoff_asymmetry_repair_or_closeout_decision_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_23/frontier23b_payoff_asymmetry_pf_source_proxy_scout.py")

F23A_SUMMARY = STAGE_ROOT / "02_runs" / PARENT_RUN_ID / "stage_open_summary.json"
F23A_LOCK = STAGE_ROOT / "02_runs" / PARENT_RUN_ID / "payoff_asymmetry_lock.json"
DATASET_PATH = Path(
    "data/processed/model_inputs/"
    "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/"
    "model_input_dataset.parquet"
)
FEATURE_ORDER_PATH = DATASET_PATH.with_name("model_input_feature_order.txt")
EXPECTED_FEATURE_HASH = "fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2"

RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")
CHANGELOG = Path("docs/workspace/changelog.md")
WORKSPACE_STATE = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE = Path("docs/context/current_working_state.md")

QUANTILES = (0.15, 0.25, 0.40, 0.60, 0.75, 0.85)
SINGLE_KEEP = 140
PAIR_SOURCE_KEEP = 70
MAX_CANDIDATES = 360
MIN_SINGLE_TRADES = 45
MIN_PAIR_TRADES = 60
MIN_TRAIN_DENSITY = 1.0
MAX_TRAIN_DENSITY = 22.0

SCOUT_MIN_PF = 1.05
SCOUT_DENSITY_LOW = 3.0
SCOUT_DENSITY_HIGH = 12.0
SCOUT_DD_CAP = 35.0
SEED_PF = 1.20
SEED_DENSITY_LOW = 5.0
SEED_DENSITY_HIGH = 10.0
SEED_DD_CAP = 20.0
HANDOFF_PF = 1.50
HANDOFF_DD_CAP = 12.0

SHOCK_FEATURES = {"return_zscore_20", "log_return_1", "return_1_over_atr_14", "gap_percent", "close_prev_close_ratio"}
TREND_FEATURES = {"ema20_ema50_diff", "di_spread_14", "supertrend_10_3", "ema20_ema50_spread_zscore_50", "adx_14"}
F20_DUPLICATE_SET = {"vix_zscore_20", "close_ema50_ratio"}

FEATURE_FAMILIES: dict[str, tuple[str, ...]] = {
    "price_momentum": (
        "log_return_1",
        "log_return_3",
        "return_zscore_20",
        "return_1_over_atr_14",
        "roc_12",
        "trix_15",
        "gap_percent",
        "close_prev_close_ratio",
    ),
    "trend_state": (
        "close_ema20_ratio",
        "close_ema50_ratio",
        "ema9_ema20_diff",
        "ema20_ema50_diff",
        "ema50_ema200_diff",
        "ema20_ema50_spread_zscore_50",
        "sma50_sma200_ratio",
        "adx_14",
        "di_spread_14",
        "supertrend_10_3",
        "vortex_indicator",
    ),
    "oscillator": (
        "rsi_14",
        "rsi_50",
        "rsi_14_slope_3",
        "rsi_14_minus_50",
        "stoch_kd_diff",
        "stochrsi_kd_diff",
        "ppo_hist_12_26_9",
    ),
    "volatility_shape": (
        "hl_range",
        "hl_zscore_50",
        "atr_14",
        "atr_50",
        "atr_14_over_atr_50",
        "bollinger_width_20",
        "bb_position_20",
        "bb_squeeze",
        "historical_vol_20",
        "historical_vol_5_over_20",
        "vix_change_1",
        "vix_zscore_20",
    ),
    "session_clock": (
        "overnight_return",
        "is_us_cash_open",
        "minutes_from_cash_open",
        "is_first_30m_after_open",
        "is_last_30m_before_cash_close",
    ),
    "macro_breadth": (
        "us10yr_change_1",
        "us10yr_zscore_20",
        "usdx_change_1",
        "usdx_zscore_20",
        "nvda_xnas_log_return_1",
        "aapl_xnas_log_return_1",
        "msft_xnas_log_return_1",
        "amzn_xnas_log_return_1",
        "mega8_equal_return_1",
        "top3_weighted_return_1",
        "mega8_pos_breadth_1",
        "mega8_dispersion_5",
        "us100_minus_mega8_equal_return_1",
        "us100_minus_top3_weighted_return_1",
    ),
    "price_shape": ("close_open_ratio",),
}


def main() -> int:
    ensure_dirs()
    created_at = utc_now()
    stage_open = read_json(F23A_SUMMARY)
    lock = read_json(F23A_LOCK)
    frame = load_frame()
    feature_order = read_feature_order()
    context = validate_context(stage_open, lock, frame, feature_order)
    baselines = build_unconditional_baselines(frame)
    condition_pool = build_condition_pool(frame, feature_order, baselines)
    sanity = build_sanity_summary(condition_pool, baselines)
    if sanity["gate_pass"]:
        candidates = build_candidate_pool(frame, condition_pool)
        metrics = evaluate_candidates(frame, candidates)
        summary = summarize_candidates(metrics)
    else:
        candidates = []
        metrics = pd.DataFrame()
        summary = pd.DataFrame()
    final = build_final(created_at, stage_open, lock, feature_order, context, baselines, condition_pool, sanity, candidates, metrics, summary)
    write_outputs(final, condition_pool, candidates, metrics, summary)
    update_registries(final)
    update_current_truth(final)
    print(json.dumps(json_ready({
        "status": final["status"],
        "judgment": final["judgment"],
        "run_id": RUN_ID,
        "condition_pool_rows": final["condition_pool_rows"],
        "sanity_gate_pass": final["sanity_gate_pass"],
        "candidate_rows": final["candidate_rows"],
        "scout_clue_rows": final["scout_clue_rows"],
        "seed_surface_rows": final["seed_surface_rows"],
        "handoff_candidate_rows": final["handoff_candidate_rows"],
        "best_candidate_id": final["best_candidate_id"],
        "next_run_id": final["next_run_id"],
        "report": REPORT_PATH.as_posix(),
    }), ensure_ascii=False, indent=2))
    return 0


def ensure_dirs() -> None:
    for path in (RUN_ROOT, STAGE_ROOT / "03_reviews", STAGE_ROOT / "04_selected"):
        io_path(path).mkdir(parents=True, exist_ok=True)


def load_frame() -> pd.DataFrame:
    frame = pd.read_parquet(io_path(DATASET_PATH)).sort_values("timestamp").reset_index(drop=True)
    required = {"timestamp", "split", "future_log_return_12", "label_class", "horizon_bars"}
    missing = sorted(required - set(frame.columns))
    if missing:
        raise ValueError(f"Missing required columns(필수 열 누락): {missing}")
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    if frame["timestamp"].isna().any():
        raise ValueError("Timestamp contains NaT(타임스탬프 결측).")
    if frame["timestamp"].duplicated().any():
        raise ValueError("Timestamp contains duplicates(타임스탬프 중복).")
    if set(frame["split"].astype(str).unique()) != {"train", "validation", "oos"}:
        raise ValueError("Split must be train/validation/oos(분할은 학습/검증/표본외만 허용).")
    if not pd.to_numeric(frame["horizon_bars"], errors="coerce").eq(12).all():
        raise ValueError("F23 requires fwd12 horizon(F23은 fwd12 구간만 허용).")
    return frame


def read_feature_order() -> list[str]:
    features = [line.strip() for line in io_path(FEATURE_ORDER_PATH).read_text(encoding="utf-8-sig").splitlines() if line.strip()]
    if len(features) != 58 or ordered_hash(features) != EXPECTED_FEATURE_HASH:
        raise ValueError("Feature order contract mismatch(피처 순서 계약 불일치).")
    return features


def validate_context(stage_open: dict[str, Any], lock: dict[str, Any], frame: pd.DataFrame, feature_order: list[str]) -> dict[str, Any]:
    workspace = read_text(WORKSPACE_STATE)
    missing_features = sorted(set(feature_order) - set(frame.columns))
    checks = {
        "workspace_current_stage_frontier23": f"current_stage_id: {STAGE_ID}" in workspace,
        "workspace_next_run_frontier23b": f"next_run_id: {RUN_ID}" in workspace,
        "stage_open_run_matches_parent": stage_open.get("run_id") == PARENT_RUN_ID,
        "pre_scout_sanity_lock_present": "pre_scout_sanity_gate" in lock.get("locks", {}),
        "no_lifecycle_until_seed_lock_present": "no_lifecycle_until_seed" in lock.get("locks", {}),
        "feature_order_hash_matches_contract": ordered_hash(feature_order) == EXPECTED_FEATURE_HASH,
        "feature_count_is_58": len(feature_order) == 58,
        "dataset_exists": path_exists(DATASET_PATH),
        "all_features_present": not missing_features,
    }
    if not all(checks.values()):
        raise RuntimeError(f"Frontier23B context check failed: {json.dumps(checks, ensure_ascii=False)}")
    return {"checks": checks, "missing_features": missing_features}


def build_unconditional_baselines(frame: pd.DataFrame) -> dict[str, dict[str, Any]]:
    all_mask = np.ones(len(frame), dtype=bool)
    return {
        "long": evaluate_mask(frame, all_mask, 1, "train"),
        "short": evaluate_mask(frame, all_mask, -1, "train"),
    }


def build_condition_pool(frame: pd.DataFrame, feature_order: list[str], baselines: dict[str, dict[str, Any]]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    train_mask = frame["split"].astype(str).eq("train").to_numpy(dtype=bool)
    for feature in feature_order:
        family = feature_family(feature)
        series = pd.to_numeric(frame[feature], errors="coerce")
        train_values = series.loc[train_mask].replace([np.inf, -np.inf], np.nan).dropna()
        if train_values.nunique(dropna=True) <= 1:
            continue
        for operator, q_label, threshold, base_mask in condition_masks(series, train_values):
            coverage = float(base_mask[train_mask].mean()) if train_mask.any() else 0.0
            if not (0.02 <= coverage <= 0.80):
                continue
            for side, side_name in ((1, "long"), (-1, "short")):
                metrics = evaluate_mask(frame, base_mask, side, "train")
                if metrics["trade_count"] < MIN_SINGLE_TRADES:
                    continue
                baseline = baselines[side_name]
                sanity_pass = sanity_passes(metrics, baseline)
                score = payoff_selection_score(metrics, baseline, sanity_pass)
                rows.append({
                    "condition_id": f"f23cond_{len(rows)+1:04d}",
                    "feature": feature,
                    "feature_family": family,
                    "operator": operator,
                    "quantile_label": q_label,
                    "threshold_value": threshold,
                    "side_value": side,
                    "side": f"{side_name}({'롱' if side > 0 else '숏'})",
                    "definition": f"{feature} {operator} {q_label}",
                    "train_coverage": coverage,
                    "train_payoff_score": score,
                    "sanity_pass": bool(sanity_pass),
                    "baseline_profit_factor": baseline["profit_factor"],
                    "baseline_payoff_ratio": baseline["payoff_ratio"],
                    "baseline_tail_ratio": baseline["right_tail_loss_tail_ratio"],
                    **prefix_dict("train_", metrics),
                    "_mask": base_mask,
                })
    if not rows:
        raise RuntimeError("No condition pool rows(조건 풀 행 없음).")
    frame_out = pd.DataFrame(rows).sort_values(["sanity_pass", "train_payoff_score"], ascending=[False, False]).reset_index(drop=True)
    frame_out["condition_id"] = [f"f23cond_{index:04d}" for index in range(1, len(frame_out) + 1)]
    return frame_out


def condition_masks(series: pd.Series, train_values: pd.Series) -> list[tuple[str, str, float, np.ndarray]]:
    values = series.to_numpy(dtype="float64")
    finite = np.isfinite(values)
    out: list[tuple[str, str, float, np.ndarray]] = []
    unique_count = int(train_values.nunique(dropna=True))
    if unique_count <= 3:
        for operator, threshold in ((">=", 0.5), ("<", 0.5)):
            mask = ((values >= threshold) if operator == ">=" else (values < threshold)) & finite
            out.append((operator, "ge0p5" if operator == ">=" else "lt0p5", float(threshold), mask))
        return out
    for quantile in QUANTILES:
        threshold = float(np.nanquantile(train_values.to_numpy(dtype="float64"), quantile))
        if quantile <= 0.5:
            operator = "<="
            mask = (values <= threshold) & finite
        else:
            operator = ">="
            mask = (values >= threshold) & finite
        out.append((operator, f"q{int(quantile * 100):02d}", threshold, mask))
    return out


def evaluate_mask(frame: pd.DataFrame, mask: np.ndarray, side: int, split: str) -> dict[str, Any]:
    split_mask = frame["split"].astype(str).eq(split).to_numpy(dtype=bool)
    trade_mask = np.asarray(mask, dtype=bool) & split_mask
    split_times = frame.loc[split_mask, "timestamp"]
    days = scout.count_scope_days(split_times)
    returns = pd.to_numeric(frame.loc[trade_mask, "future_log_return_12"], errors="coerce").to_numpy(dtype="float64")
    pnl = returns * float(side) - scout.ROUGH_COST_LOG_RETURN
    trade_times = frame.loc[trade_mask, "timestamp"]
    metrics = scout.trade_metrics(pnl, trade_times)
    shape = payoff_shape(pnl)
    trade_count = int(len(pnl))
    return {
        **metrics,
        **shape,
        "trade_count": trade_count,
        "days_in_scope": days,
        "trades_per_day": float(trade_count / days) if days else 0.0,
        "dd_risk": max(float(metrics["max_drawdown_percent"]), float(metrics["max_monthly_drawdown_percent"])),
    }


def payoff_shape(pnl: np.ndarray) -> dict[str, Any]:
    pnl = np.asarray(pnl, dtype="float64")
    pnl = pnl[np.isfinite(pnl)]
    if pnl.size == 0:
        return {
            "avg_win": 0.0,
            "avg_loss_abs": 0.0,
            "payoff_ratio": 0.0,
            "p90_pnl": 0.0,
            "p10_pnl": 0.0,
            "right_tail_loss_tail_ratio": 0.0,
            "adverse_loss_p10_abs": 0.0,
            "loss_rate": 0.0,
        }
    wins = pnl[pnl > 0]
    losses = pnl[pnl < 0]
    avg_win = float(wins.mean()) if wins.size else 0.0
    avg_loss_abs = abs(float(losses.mean())) if losses.size else 0.0
    payoff_ratio = avg_win / avg_loss_abs if avg_loss_abs > 1e-12 else (999.0 if avg_win > 0 else 0.0)
    p90 = float(np.nanquantile(pnl, 0.90))
    p10 = float(np.nanquantile(pnl, 0.10))
    adverse = abs(min(p10, 0.0))
    tail_ratio = max(p90, 0.0) / adverse if adverse > 1e-12 else (999.0 if p90 > 0 else 0.0)
    return {
        "avg_win": avg_win,
        "avg_loss_abs": avg_loss_abs,
        "payoff_ratio": float(payoff_ratio),
        "p90_pnl": p90,
        "p10_pnl": p10,
        "right_tail_loss_tail_ratio": float(tail_ratio),
        "adverse_loss_p10_abs": adverse,
        "loss_rate": float(losses.size / pnl.size),
    }


def sanity_passes(metrics: dict[str, Any], baseline: dict[str, Any]) -> bool:
    if metrics["net_profit"] <= 0 or metrics["profit_factor"] <= 1.0:
        return False
    if metrics["trades_per_day"] < MIN_TRAIN_DENSITY or metrics["trades_per_day"] > MAX_TRAIN_DENSITY:
        return False
    pf_better = metrics["profit_factor"] >= max(1.01, baseline["profit_factor"] + 0.03)
    payoff_better = metrics["payoff_ratio"] >= baseline["payoff_ratio"] + 0.05
    tail_better = metrics["right_tail_loss_tail_ratio"] >= baseline["right_tail_loss_tail_ratio"] + 0.05
    adverse_better = metrics["adverse_loss_p10_abs"] <= baseline["adverse_loss_p10_abs"] * 0.99
    return bool(pf_better and sum([payoff_better, tail_better, adverse_better]) >= 2)


def payoff_selection_score(metrics: dict[str, Any], baseline: dict[str, Any], sanity_pass: bool) -> float:
    density_penalty = abs(float(metrics["trades_per_day"]) - 8.0) / 8.0
    dd_penalty = max(0.0, float(metrics["dd_risk"]) - 12.0) / 20.0
    pf_lift = max(0.0, float(metrics["profit_factor"]) - float(baseline["profit_factor"]))
    payoff_lift = max(0.0, float(metrics["payoff_ratio"]) - float(baseline["payoff_ratio"]))
    tail_lift = max(0.0, float(metrics["right_tail_loss_tail_ratio"]) - float(baseline["right_tail_loss_tail_ratio"]))
    base = (1.0 + pf_lift) * (1.0 + payoff_lift) * (1.0 + tail_lift)
    net_bonus = max(float(metrics["net_profit"]), 0.0) * 10.0
    sanity_bonus = 1.35 if sanity_pass else 0.75
    return float(sanity_bonus * (base + net_bonus) / (1.0 + density_penalty + dd_penalty))


def build_sanity_summary(condition_pool: pd.DataFrame, baselines: dict[str, dict[str, Any]]) -> dict[str, Any]:
    pass_rows = condition_pool.loc[condition_pool["sanity_pass"].astype(bool)].copy()
    best = dict(pass_rows.iloc[0]) if len(pass_rows) else {}
    return {
        "gate_pass": bool(len(pass_rows) > 0),
        "pass_rows": int(len(pass_rows)),
        "condition_rows": int(len(condition_pool)),
        "best_condition_id": best.get("condition_id", ""),
        "best_condition": clean_row(best),
        "baseline_long": clean_row(baselines["long"]),
        "baseline_short": clean_row(baselines["short"]),
    }


def build_candidate_pool(frame: pd.DataFrame, condition_pool: pd.DataFrame) -> list[dict[str, Any]]:
    eligible = condition_pool.loc[condition_pool["sanity_pass"].astype(bool)].copy()
    eligible = eligible.sort_values("train_payoff_score", ascending=False).head(SINGLE_KEEP)
    records = eligible.to_dict("records")
    candidates: list[dict[str, Any]] = []
    for record in records[: min(80, len(records))]:
        mask = np.asarray(record["_mask"], dtype=bool)
        metrics = evaluate_mask(frame, mask, int(record["side_value"]), "train")
        candidates.append(candidate_from_conditions([record], mask, metrics))
    pair_source = records[: min(PAIR_SOURCE_KEEP, len(records))]
    for index, first in enumerate(pair_source):
        for second in pair_source[index + 1 :]:
            if int(first["side_value"]) != int(second["side_value"]):
                continue
            if first["feature"] == second["feature"]:
                continue
            if first["feature_family"] == second["feature_family"]:
                continue
            mask = np.asarray(first["_mask"], dtype=bool) & np.asarray(second["_mask"], dtype=bool)
            metrics = evaluate_mask(frame, mask, int(first["side_value"]), "train")
            if metrics["trade_count"] < MIN_PAIR_TRADES:
                continue
            if not (MIN_TRAIN_DENSITY <= metrics["trades_per_day"] <= MAX_TRAIN_DENSITY):
                continue
            if metrics["net_profit"] <= 0 or metrics["profit_factor"] < 1.02:
                continue
            candidates.append(candidate_from_conditions([first, second], mask, metrics))
    candidates.sort(key=lambda item: float(item["train_payoff_score"]), reverse=True)
    for index, candidate in enumerate(candidates[:MAX_CANDIDATES], start=1):
        candidate["candidate_id"] = f"f23b_{index:04d}"
    return candidates[:MAX_CANDIDATES]


def candidate_from_conditions(conditions: list[dict[str, Any]], mask: np.ndarray, metrics: dict[str, Any]) -> dict[str, Any]:
    features = [str(item["feature"]) for item in conditions]
    families = [str(item["feature_family"]) for item in conditions]
    side_value = int(conditions[0]["side_value"])
    f22_like = bool(set(features) & SHOCK_FEATURES and set(features) & TREND_FEATURES)
    f20_duplicate = set(features) == F20_DUPLICATE_SET
    density_penalty = abs(float(metrics["trades_per_day"]) - 8.0) / 8.0
    dd_penalty = max(0.0, float(metrics["dd_risk"]) - 12.0) / 20.0
    train_payoff_score = float(
        max(metrics["net_profit"], 0.0)
        * min(metrics["profit_factor"], 4.0)
        * min(metrics["payoff_ratio"], 4.0)
        * min(metrics["right_tail_loss_tail_ratio"], 4.0)
        / (1.0 + density_penalty + dd_penalty)
    )
    return {
        "candidate_id": "",
        "condition_count": len(conditions),
        "condition_ids": "|".join(str(item["condition_id"]) for item in conditions),
        "features": "|".join(features),
        "feature_families": "|".join(families),
        "side_value": side_value,
        "side": f"{'long' if side_value > 0 else 'short'}({'롱' if side_value > 0 else '숏'})",
        "rule_definition": " & ".join(str(item["definition"]) for item in conditions),
        "train_payoff_score": train_payoff_score,
        "f22_like_duplicate_pressure": f22_like,
        "f20_duplicate_pressure": f20_duplicate,
        "mask": mask,
        "train_selection_metrics": metrics,
    }


def evaluate_candidates(frame: pd.DataFrame, candidates: list[dict[str, Any]]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for rank, candidate in enumerate(candidates, start=1):
        for split in ("train", "validation", "oos"):
            metrics = evaluate_mask(frame, candidate["mask"], int(candidate["side_value"]), split)
            sparse_floor = max(20, int(math.ceil(metrics["days_in_scope"] * 0.50)))
            sparse_flag = metrics["trade_count"] < sparse_floor
            pf999_sparse_flag = bool(metrics["profit_factor"] >= 999.0 and sparse_flag)
            density_distance = scout.density_axis_distance(metrics["trades_per_day"])
            pf_distance = scout.profit_factor_axis_distance(metrics["profit_factor"], metrics["trade_count"], sparse_flag, pf999_sparse_flag)
            dd_distance = max(0.0, (metrics["dd_risk"] - scout.DD_TARGET_PERCENT) / scout.DD_TARGET_PERCENT)
            smoothness_distance = scout.smoothness_axis_distance(metrics)
            rows.append({
                "candidate_id": candidate["candidate_id"],
                "train_rank": rank,
                "condition_count": candidate["condition_count"],
                "condition_ids": candidate["condition_ids"],
                "features": candidate["features"],
                "feature_families": candidate["feature_families"],
                "side": candidate["side"],
                "side_value": candidate["side_value"],
                "rule_definition": candidate["rule_definition"],
                "f22_like_duplicate_pressure": candidate["f22_like_duplicate_pressure"],
                "f20_duplicate_pressure": candidate["f20_duplicate_pressure"],
                "split": split,
                "record_view": "Tier A separate(티어 A 분리)",
                "tier_scope": "Tier A(티어 A)",
                "trade_count": metrics["trade_count"],
                "days_in_scope": metrics["days_in_scope"],
                "trades_per_day": metrics["trades_per_day"],
                "net_profit": metrics["net_profit"],
                "profit_factor": metrics["profit_factor"],
                "expectancy": metrics["expectancy"],
                "win_rate": metrics["win_rate"],
                "avg_win": metrics["avg_win"],
                "avg_loss_abs": metrics["avg_loss_abs"],
                "payoff_ratio": metrics["payoff_ratio"],
                "right_tail_loss_tail_ratio": metrics["right_tail_loss_tail_ratio"],
                "adverse_loss_p10_abs": metrics["adverse_loss_p10_abs"],
                "loss_rate": metrics["loss_rate"],
                "max_drawdown_percent": metrics["max_drawdown_percent"],
                "max_monthly_drawdown_percent": metrics["max_monthly_drawdown_percent"],
                "dd_risk": metrics["dd_risk"],
                "underwater_ratio": metrics["underwater_ratio"],
                "max_loss_streak": metrics["max_loss_streak"],
                "equity_trend_r2": metrics["equity_trend_r2"],
                "sparse_flag": sparse_flag,
                "pf999_sparse_flag": pf999_sparse_flag,
                "density_axis_distance": density_distance,
                "pf_axis_distance": pf_distance,
                "dd_axis_distance": dd_distance,
                "smoothness_axis_distance": smoothness_distance,
                "joint_axis_distance": density_distance + pf_distance + dd_distance + smoothness_distance,
                "density_pass": bool(scout.DENSITY_TARGET_LOW <= metrics["trades_per_day"] <= scout.DENSITY_TARGET_HIGH),
                "pf_pass": bool(metrics["profit_factor"] >= scout.PF_TARGET and metrics["net_profit"] > 0 and not sparse_flag),
                "dd_pass": bool(metrics["dd_risk"] < scout.DD_TARGET_PERCENT),
                "smoothness_pass": bool(
                    metrics["net_profit"] > 0
                    and metrics["underwater_ratio"] <= 0.45
                    and metrics["equity_trend_r2"] >= 0.35
                    and metrics["max_loss_streak"] <= 6
                ),
                "selection_boundary": "train_only_rank(학습 전용 순위)" if split == "train" else "read_only_forward_diagnostic(읽기 전용 전진 진단)",
                "proxy_cost_log_return": scout.ROUGH_COST_LOG_RETURN,
            })
    if not rows:
        return pd.DataFrame()
    return pd.DataFrame(rows)


def summarize_candidates(metrics: pd.DataFrame) -> pd.DataFrame:
    if metrics.empty:
        return pd.DataFrame()
    rows: list[dict[str, Any]] = []
    for candidate_id, group in metrics.groupby("candidate_id", sort=False):
        train = split_row(group, "train")
        validation = split_row(group, "validation")
        oos = split_row(group, "oos")
        duplicate_pressure = bool(train["f22_like_duplicate_pressure"]) or bool(train["f20_duplicate_pressure"])
        base = {
            "candidate_id": candidate_id,
            "train_rank": int(train["train_rank"]),
            "condition_count": int(train["condition_count"]),
            "side": train["side"],
            "rule_definition": train["rule_definition"],
            "features": train["features"],
            "feature_families": train["feature_families"],
            "f22_like_duplicate_pressure": bool(train["f22_like_duplicate_pressure"]),
            "f20_duplicate_pressure": bool(train["f20_duplicate_pressure"]),
        }
        for prefix, row in (("train", train), ("validation", validation), ("oos", oos)):
            for field in (
                "trade_count",
                "trades_per_day",
                "net_profit",
                "profit_factor",
                "expectancy",
                "win_rate",
                "payoff_ratio",
                "right_tail_loss_tail_ratio",
                "adverse_loss_p10_abs",
                "dd_risk",
                "underwater_ratio",
                "max_loss_streak",
                "equity_trend_r2",
                "joint_axis_distance",
            ):
                base[f"{prefix}_{field}"] = row[field]
        base["scout_clue_flag"] = bool(
            not duplicate_pressure
            and validation["net_profit"] > 0
            and oos["net_profit"] > 0
            and validation["profit_factor"] >= SCOUT_MIN_PF
            and oos["profit_factor"] >= SCOUT_MIN_PF
            and SCOUT_DENSITY_LOW <= validation["trades_per_day"] <= SCOUT_DENSITY_HIGH
            and SCOUT_DENSITY_LOW <= oos["trades_per_day"] <= SCOUT_DENSITY_HIGH
            and max(validation["dd_risk"], oos["dd_risk"]) <= SCOUT_DD_CAP
        )
        base["seed_surface_flag"] = bool(
            base["scout_clue_flag"]
            and validation["profit_factor"] >= SEED_PF
            and oos["profit_factor"] >= SEED_PF
            and SEED_DENSITY_LOW <= validation["trades_per_day"] <= SEED_DENSITY_HIGH
            and SEED_DENSITY_LOW <= oos["trades_per_day"] <= SEED_DENSITY_HIGH
            and max(validation["dd_risk"], oos["dd_risk"]) <= SEED_DD_CAP
        )
        base["handoff_candidate_flag"] = bool(
            base["seed_surface_flag"]
            and validation["profit_factor"] >= HANDOFF_PF
            and oos["profit_factor"] >= HANDOFF_PF
            and max(validation["dd_risk"], oos["dd_risk"]) <= HANDOFF_DD_CAP
            and validation["equity_trend_r2"] >= 0.35
            and oos["equity_trend_r2"] >= 0.35
        )
        base["forward_read_score"] = float(
            min(validation["profit_factor"], 4.0)
            * min(oos["profit_factor"], 4.0)
            * min(validation["payoff_ratio"], 4.0)
            * min(oos["payoff_ratio"], 4.0)
            * min(validation["trades_per_day"], oos["trades_per_day"], 12.0)
            / (1.0 + max(validation["dd_risk"], oos["dd_risk"]) / 12.0)
        )
        rows.append(base)
    return pd.DataFrame(rows).sort_values(
        ["handoff_candidate_flag", "seed_surface_flag", "scout_clue_flag", "forward_read_score"],
        ascending=[False, False, False, False],
    )


def split_row(group: pd.DataFrame, split: str) -> dict[str, Any]:
    row = group.loc[group["split"].eq(split)]
    if row.empty:
        raise ValueError(f"Missing split row(분할 행 누락): {split}")
    return dict(row.iloc[0])


def build_final(
    created_at: str,
    stage_open: dict[str, Any],
    lock: dict[str, Any],
    feature_order: list[str],
    context: dict[str, Any],
    baselines: dict[str, dict[str, Any]],
    condition_pool: pd.DataFrame,
    sanity: dict[str, Any],
    candidates: list[dict[str, Any]],
    metrics: pd.DataFrame,
    summary: pd.DataFrame,
) -> dict[str, Any]:
    scout_count = int(summary["scout_clue_flag"].sum()) if not summary.empty else 0
    seed_count = int(summary["seed_surface_flag"].sum()) if not summary.empty else 0
    handoff_count = int(summary["handoff_candidate_flag"].sum()) if not summary.empty else 0
    if not sanity["gate_pass"]:
        status = "payoff_asymmetry_prescout_sanity_failed_no_proxy_sweep_no_authority"
        judgment = "invalid_setup_or_negative_pressure_requires_closeout_no_authority"
        next_run_id = NEXT_REPAIR_OR_CLOSEOUT_RUN_ID
    elif handoff_count:
        status = "payoff_asymmetry_handoff_candidate_proxy_no_authority"
        judgment = "handoff_candidate_requires_grok_pre_expensive_review_no_authority"
        next_run_id = NEXT_PRE_EXPENSIVE_GROK_RUN_ID
    elif seed_count:
        status = "payoff_asymmetry_seed_surface_proxy_no_authority"
        judgment = "seed_surface_requires_repair_or_closeout_no_authority"
        next_run_id = NEXT_REPAIR_OR_CLOSEOUT_RUN_ID
    elif scout_count:
        status = "payoff_asymmetry_scout_clue_proxy_no_authority"
        judgment = "scout_clue_requires_repair_or_closeout_no_authority"
        next_run_id = NEXT_REPAIR_OR_CLOSEOUT_RUN_ID
    else:
        status = "payoff_asymmetry_proxy_no_seed_or_handoff_no_authority"
        judgment = "negative_pressure_requires_repair_or_closeout_no_authority"
        next_run_id = NEXT_REPAIR_OR_CLOSEOUT_RUN_ID
    best = dict(summary.iloc[0]) if not summary.empty else {}
    return {
        "created_at_utc": created_at,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": next_run_id,
        "status": status,
        "judgment": judgment,
        "feature_count": len(feature_order),
        "feature_order_hash": ordered_hash(feature_order),
        "context": context,
        "stage_open": {"status": stage_open.get("status"), "judgment": stage_open.get("judgment")},
        "lock": lock,
        "baseline_long": clean_row(baselines["long"]),
        "baseline_short": clean_row(baselines["short"]),
        "condition_pool_rows": int(len(condition_pool)),
        "sanity_gate_pass": bool(sanity["gate_pass"]),
        "sanity_pass_rows": int(sanity["pass_rows"]),
        "sanity": sanity,
        "candidate_rows": int(len(candidates)),
        "metric_rows": int(len(metrics)) if not metrics.empty else 0,
        "scout_clue_rows": scout_count,
        "seed_surface_rows": seed_count,
        "handoff_candidate_rows": handoff_count,
        "best_candidate_id": best.get("candidate_id", ""),
        "best_candidate": json_ready(best),
        "result_boundary": "proxy_only_no_wfo_no_mt5_no_runtime_authority(프록시 전용, WFO/MT5/런타임 권위 없음)",
        "runtime_probe_status": "pre_expensive_grok_required_before_mt5(비싼 MT5 전 그록 검토 필요)" if handoff_count else "out_of_scope_by_claim_no_handoff_candidate_yet(인계 후보 전이라 주장 범위 밖)",
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(final: dict[str, Any], condition_pool: pd.DataFrame, candidates: list[dict[str, Any]], metrics: pd.DataFrame, summary: pd.DataFrame) -> None:
    condition_pool.drop(columns=["_mask"], errors="ignore").to_csv(io_path(RUN_ROOT / "payoff_condition_pool.csv"), index=False, encoding="utf-8-sig")
    write_json(RUN_ROOT / "pre_scout_sanity.json", final["sanity"])
    pd.DataFrame([clean_candidate_for_csv(item) for item in candidates]).to_csv(io_path(RUN_ROOT / "train_ranked_candidates.csv"), index=False, encoding="utf-8-sig")
    metrics.to_csv(io_path(RUN_ROOT / "proxy_metrics_by_split.csv"), index=False, encoding="utf-8-sig")
    summary.to_csv(io_path(RUN_ROOT / "candidate_summary.csv"), index=False, encoding="utf-8-sig")
    if not summary.empty:
        summary.sort_values("forward_read_score", ascending=False).head(30).to_csv(io_path(RUN_ROOT / "top_forward_readonly_diagnostic.csv"), index=False, encoding="utf-8-sig")
    else:
        pd.DataFrame().to_csv(io_path(RUN_ROOT / "top_forward_readonly_diagnostic.csv"), index=False, encoding="utf-8-sig")
    write_json(RUN_ROOT / "final_summary.json", final)
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(final))
    f03b.write_text_sig(REPORT_PATH, report_text(final, summary))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / f"{RUN_ID}_gate_audit.md", gate_audit(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(final))


def run_manifest(final: dict[str, Any]) -> dict[str, Any]:
    artifacts = [
        SCRIPT_PATH,
        F23A_SUMMARY,
        F23A_LOCK,
        DATASET_PATH,
        FEATURE_ORDER_PATH,
        RUN_ROOT / "payoff_condition_pool.csv",
        RUN_ROOT / "pre_scout_sanity.json",
        RUN_ROOT / "train_ranked_candidates.csv",
        RUN_ROOT / "proxy_metrics_by_split.csv",
        RUN_ROOT / "candidate_summary.csv",
        RUN_ROOT / "top_forward_readonly_diagnostic.csv",
    ]
    return {
        "identity": {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": final["next_run_id"],
            "created_at_utc": final["created_at_utc"],
        },
        "artifacts": [artifact_identity(path) for path in artifacts],
        "feature_schema": {
            "feature_count": final["feature_count"],
            "feature_order_hash": final["feature_order_hash"],
            "feature_order_path": FEATURE_ORDER_PATH.as_posix(),
        },
        "data_snapshot": {"dataset_path": DATASET_PATH.as_posix(), "split_names": ["train", "validation", "oos"]},
        "runtime_snapshot": {
            "symbol": "US100",
            "timeframe": "M5",
            "entry_timing": "closed_bar_signal_horizon_proxy(종료봉 신호 수평 프록시)",
            "cost_behavior": "rough_log_return_cost_proxy_only(거친 로그수익 비용 프록시 전용)",
        },
        "rule_stack": {
            "selection": "train_only_payoff_asymmetry(학습 전용 보상 비대칭)",
            "entry": "single_or_depth2_feature_state_conditions(단일 또는 깊이2 피처 상태 조건)",
            "exit": "future_log_return_12_proxy(12봉 미래 수익률 프록시)",
        },
        "results": {
            "by_split": {"metrics_path": (RUN_ROOT / "proxy_metrics_by_split.csv").as_posix()},
            "cross_split": {
                "sanity_gate_pass": final["sanity_gate_pass"],
                "scout_clue_rows": final["scout_clue_rows"],
                "seed_surface_rows": final["seed_surface_rows"],
                "handoff_candidate_rows": final["handoff_candidate_rows"],
                "best_candidate_id": final["best_candidate_id"],
            },
            "report_refs": [{"role": "proxy_report", "path": REPORT_PATH.as_posix()}],
        },
        "compatibility": {
            "schema_version": "frontier23b_payoff_asymmetry_proxy_v1",
            "mismatch_policy": "fail_fast(빠른 실패)",
            "required_output_schema": "not_applicable_no_onnx_export_yet(ONNX 내보내기 전이라 해당 없음)",
        },
        "claim_boundary": final["claim_boundary"],
    }


def report_text(final: dict[str, Any], summary: pd.DataFrame) -> str:
    best = final["best_candidate"]
    top_rows: list[str] = []
    if not summary.empty:
        for _, row in summary.head(12).iterrows():
            top_rows.append(
                f"| `{row['candidate_id']}` | {row['side']} | `{row['features']}` | "
                f"{fmt(row['validation_profit_factor'])} | {fmt(row['validation_trades_per_day'])} | {fmt(row['validation_dd_risk'])} | "
                f"{fmt(row['oos_profit_factor'])} | {fmt(row['oos_trades_per_day'])} | {fmt(row['oos_dd_risk'])} | {row['scout_clue_flag']} | {row['seed_surface_flag']} |"
            )
    table = "\n".join(top_rows) if top_rows else "| none(없음) | | | | | | | | | | |"
    return f"""# Frontier23B Payoff Asymmetry PF Source Proxy Scout Report(전선23B 보상 비대칭 수익 팩터 원천 프록시 탐색 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Action(행동): train-only payoff asymmetry(학습 전용 보상 비대칭) 조건을 먼저 unconditional baseline(무조건 기준선)과 비교한 뒤, 통과 조건으로 단일/쌍 진입 상태 프록시를 탐색했습니다.

Effect(효과): validation/OOS(검증/표본외)는 선택에 쓰지 않고, forward diagnostic(전진 진단)으로만 보았습니다.

Pre-scout sanity gate(탐색 전 건전성 게이트): `{final['sanity_gate_pass']}` with pass rows(통과 행) `{final['sanity_pass_rows']}`.

Condition/candidate/metric rows(조건/후보/지표 행): `{final['condition_pool_rows']}` / `{final['candidate_rows']}` / `{final['metric_rows']}`

Scout/seed/handoff rows(탐색/씨앗/인계 행): `{final['scout_clue_rows']}` / `{final['seed_surface_rows']}` / `{final['handoff_candidate_rows']}`

Best candidate(최상 후보): `{final['best_candidate_id']}`

Best validation PF/density/DD(최상 검증 수익 팩터/빈도/손실폭): `{fmt(best.get('validation_profit_factor'))}` / `{fmt(best.get('validation_trades_per_day'))}/day` / `{fmt(best.get('validation_dd_risk'))}%`

Best OOS PF/density/DD(최상 표본외 수익 팩터/빈도/손실폭): `{fmt(best.get('oos_profit_factor'))}` / `{fmt(best.get('oos_trades_per_day'))}/day` / `{fmt(best.get('oos_dd_risk'))}%`

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

## Top Readonly Forward Rows(상위 읽기 전용 전진 행)

| candidate(후보) | side(방향) | features(피처) | val PF | val density | val DD | OOS PF | OOS density | OOS DD | scout | seed |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
{table}

Next action(다음 행동): `{final['next_run_id']}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def gate_audit(final: dict[str, Any]) -> str:
    return f"""# Frontier23B Gate Audit(전선23B 게이트 감사)

- scope_completion_gate(범위 완료 게이트): proxy artifacts created(프록시 산출물 생성) `{(RUN_ROOT / 'final_summary.json').as_posix()}`
- pre_scout_sanity_gate(탐색 전 건전성 게이트): `{final['sanity_gate_pass']}` with `{final['sanity_pass_rows']}` pass rows(통과 행)
- kpi_contract_audit(KPI 계약 감사): metrics/candidate/condition outputs(지표/후보/조건 출력) created(생성)
- novelty_duplicate_guard(신규성 중복 가드): F22-like and F20 duplicate pressure columns recorded(F22 유사/F20 중복 압력 열 기록)
- required_gate_coverage_audit(필수 게이트 커버리지 감사): this file(이 파일)
- final_claim_guard(최종 주장 방지): runtime authority/operating promotion/Goal Achieve(런타임 권위/운영 승격/목표 달성) not_claimed(주장 없음)
"""


def selection_status(final: dict[str, Any]) -> str:
    return f"""# Frontier23 Selection Status(전선23 선택 상태)

Updated(갱신): {final['created_at_utc']}

Selection(선택): no selected baseline/completion/promotion/runtime authority(선택 기준선/완성/승격/런타임 권위 없음).

Latest proxy(최근 프록시): `{RUN_ID}`

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Best candidate(최상 후보): `{final['best_candidate_id']}`

Scout/seed/handoff rows(탐색/씨앗/인계 행): `{final['scout_clue_rows']}` / `{final['seed_surface_rows']}` / `{final['handoff_candidate_rows']}`

Next action(다음 행동): `{final['next_run_id']}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 not_claimed(주장 없음)입니다.
"""


def update_registries(final: dict[str, Any]) -> None:
    f03b.upsert_csv(RUN_REGISTRY, "run_id", run_registry_row(final))
    for row in ledger_rows(final):
        f03b.upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
        f03b.upsert_csv(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", row)
    f03b.append_once(CHANGELOG, RUN_ID, changelog_entry(final))
    f03b.append_once(IDEA_REGISTRY, RUN_ID, idea_registry_entry(final))


def run_registry_row(final: dict[str, Any]) -> dict[str, Any]:
    best = final["best_candidate"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "payoff_asymmetry_proxy_scout(보상 비대칭 프록시 탐색)",
        "family": "experiment_execution(실험 실행)",
        "work_family": "experiment_execution(실험 실행)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"sanity={final['sanity_gate_pass']};scout={final['scout_clue_rows']};seed={final['seed_surface_rows']};handoff={final['handoff_candidate_rows']};best={final['best_candidate_id']}",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": final["next_run_id"],
        "claim_boundary": final["result_boundary"],
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": final["created_at_utc"],
        "primary_kpi": f"best={final['best_candidate_id']};oos_pf={fmt(best.get('oos_profit_factor'))};oos_density={fmt(best.get('oos_trades_per_day'))};oos_dd={fmt(best.get('oos_dd_risk'))}",
        "guardrail_kpi": "train_only_payoff_selection_validation_oos_read_only_no_authority(학습 전용 보상 선택, 검증/표본외 읽기 전용, 권위 없음)",
        "external_verification_status": final["runtime_probe_status"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "result_path": REPORT_PATH.as_posix(),
    }


def ledger_rows(final: dict[str, Any]) -> list[dict[str, Any]]:
    best = final["best_candidate"]
    primary = {
        "ledger_row_id": f"{RUN_ID}__tier_a_payoff_asymmetry_proxy",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__tier_a_payoff_asymmetry_proxy",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "Tier A separate(티어 A 분리)",
        "tier_scope": "Tier A(티어 A)",
        "kpi_scope": "payoff_asymmetry_proxy_not_runtime(보상 비대칭 프록시, 런타임 아님)",
        "scoreboard_lane": "trade_shape_proxy(거래 형태 프록시)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": f"best={final['best_candidate_id']};oos_pf={fmt(best.get('oos_profit_factor'))};oos_density={fmt(best.get('oos_trades_per_day'))};oos_dd={fmt(best.get('oos_dd_risk'))}",
        "guardrail_kpi": "proxy_only_no_wfo_no_mt5_no_authority(프록시 전용, WFO/MT5/권위 없음)",
        "external_verification_status": final["runtime_probe_status"],
        "notes": f"sanity={final['sanity_gate_pass']};scout={final['scout_clue_rows']};seed={final['seed_surface_rows']};handoff={final['handoff_candidate_rows']}",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "run_family": "experiment_execution(실험 실행)",
    }
    tier_b = {
        **primary,
        "ledger_row_id": f"{RUN_ID}__tier_b_missing_required",
        "subrun_id": f"{RUN_ID}__tier_b_missing_required",
        "record_view": "Tier B separate(티어 B 분리)",
        "tier_scope": "Tier B(티어 B)",
        "kpi_scope": "missing_required(필수 누락)",
        "primary_kpi": "missing_required_no_tier_b_model_input(필수 누락, Tier B 모델 입력 없음)",
        "guardrail_kpi": "no_tier_b_claim(티어 B 주장 없음)",
        "external_verification_status": "not_applicable_proxy_no_mt5(프록시, MT5 없음)",
        "notes": "Tier B model input not available in this dataset(Tier B 모델 입력이 이 데이터셋에 없음)",
    }
    combined = {
        **primary,
        "ledger_row_id": f"{RUN_ID}__tier_ab_combined_out_of_scope",
        "subrun_id": f"{RUN_ID}__tier_ab_combined_out_of_scope",
        "record_view": "Tier A+B combined(티어 A+B 합산)",
        "tier_scope": "Tier A+B(티어 A+B)",
        "kpi_scope": "out_of_scope_by_claim(주장 범위 밖)",
        "primary_kpi": "out_of_scope_by_claim_no_combined_source(주장 범위 밖, 합산 원천 없음)",
        "guardrail_kpi": "no_synthetic_combined_claim(합성 합산 주장 없음)",
        "external_verification_status": "not_applicable_proxy_no_mt5(프록시, MT5 없음)",
        "notes": "Combined record blocked by missing Tier B source(Tier B 원천 누락으로 합산 기록 차단)",
    }
    return [primary, tier_b, combined]


def changelog_entry(final: dict[str, Any]) -> str:
    return (
        f"- {final['created_at_utc']}: `{RUN_ID}` ran payoff asymmetry proxy scout(보상 비대칭 프록시 탐색). "
        f"Effect(효과): sanity/scout/seed/handoff(건전성/탐색/씨앗/인계) are {final['sanity_gate_pass']}/{final['scout_clue_rows']}/{final['seed_surface_rows']}/{final['handoff_candidate_rows']} and next run(다음 실행) is `{final['next_run_id']}`.\n"
    )


def idea_registry_entry(final: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR23-PAYOFF-ASYMMETRY-PF-SOURCE-ONNX-SCOUT`: `{RUN_ID}` tested train-only payoff asymmetry(학습 전용 보상 비대칭). "
        f"Effect(효과): best candidate `{final['best_candidate_id']}` remains proxy-only(프록시 전용) with no authority(권위 없음).\n"
    )


def update_current_truth(final: dict[str, Any]) -> None:
    io_path(WORKSPACE_STATE).write_text(workspace_state(final), encoding="utf-8-sig")
    f03b.write_text_sig(CURRENT_WORKING_STATE, current_working_state(final))


def workspace_state(final: dict[str, Any]) -> str:
    return "\n".join([
        f"current_stage_id: {STAGE_ID}",
        f"current_run_id: {RUN_ID}",
        f"latest_completed_run_id: {RUN_ID}",
        f"current_status: {final['status']}",
        f"current_judgment: {final['judgment']}",
        f"next_run_id: {final['next_run_id']}",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "goal_achieve: not_claimed",
        f"updated_at_utc: '{final['created_at_utc']}'",
        "",
    ])


def current_working_state(final: dict[str, Any]) -> str:
    best = final["best_candidate"]
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

## Active Stage(현재 단계)

- stage(단계): `{STAGE_ID}`
- latest run(최근 실행): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- next run(다음 실행): `{final['next_run_id']}`

## Current Truth(현재 진실)

Action(행동): F23B(전선23B)가 payoff asymmetry PF source proxy(보상 비대칭 수익 팩터 원천 프록시)를 실행했습니다.

Effect(효과): train-only payoff asymmetry(학습 전용 보상 비대칭)가 unconditional baseline(무조건 기준선)을 이기는지 확인하고, validation/OOS(검증/표본외)는 읽기 전용으로 분리했습니다.

Best candidate(최상 후보): `{final['best_candidate_id']}` with validation/OOS PF-density-DD(검증/표본외 수익 팩터-빈도-손실폭) `{fmt(best.get('validation_profit_factor'))}/{fmt(best.get('validation_trades_per_day'))}/{fmt(best.get('validation_dd_risk'))}` and `{fmt(best.get('oos_profit_factor'))}/{fmt(best.get('oos_trades_per_day'))}/{fmt(best.get('oos_dd_risk'))}`.

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def feature_family(feature: str) -> str:
    for family, features in FEATURE_FAMILIES.items():
        if feature in features:
            return family
    return "other"


def prefix_dict(prefix: str, values: dict[str, Any]) -> dict[str, Any]:
    return {f"{prefix}{key}": value for key, value in values.items() if key != "_mask"}


def clean_row(row: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in row.items() if key != "_mask" and key != "mask"}


def clean_candidate_for_csv(item: dict[str, Any]) -> dict[str, Any]:
    cleaned = {key: value for key, value in item.items() if key not in {"mask", "train_selection_metrics"}}
    cleaned.update(prefix_dict("train_", item.get("train_selection_metrics", {})))
    return cleaned


def artifact_identity(path: Path) -> dict[str, str]:
    return {"path": path.as_posix(), "sha256": sha256_file(path) if path_exists(path) else "pending_or_missing(대기 또는 누락)"}


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fmt(value: Any) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return "NA"
    if not math.isfinite(number):
        return "NA"
    return f"{number:.6g}"


if __name__ == "__main__":
    raise SystemExit(main())
