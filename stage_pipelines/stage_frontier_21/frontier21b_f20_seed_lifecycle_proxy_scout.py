from __future__ import annotations

import csv
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

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from foundation.models.onnx_bridge import ordered_hash, sha256_file
from stage_pipelines.stage_frontier_02 import four_axis_proxy_scout as scout
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b
from stage_pipelines.stage_frontier_07 import frontier07b_adverse_excursion_risk_label_proxy_scout as f07b


STAGE_ID = "stage_frontier_21__f20_seed_lifecycle_dd_containment_onnx_scout"
RUN_ID = "frontier21B_f20_seed_lifecycle_proxy_scout_v1"
RUN_NUMBER = "frontier21B"
PARENT_RUN_ID = "frontier21A_stage_open_f20_seed_lifecycle_dd_containment_onnx_scout_v1"
NEXT_REPAIR_OR_CLOSEOUT_RUN_ID = "frontier21C_lifecycle_repair_or_closeout_decision_v1"
NEXT_PRE_EXPENSIVE_GROK_RUN_ID = "frontier21C_grok_pre_expensive_lifecycle_handoff_review_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_21/frontier21b_f20_seed_lifecycle_proxy_scout.py")

F21A_SUMMARY = STAGE_ROOT / "02_runs" / PARENT_RUN_ID / "stage_open_summary.json"
F21A_LOCK = STAGE_ROOT / "02_runs" / PARENT_RUN_ID / "lifecycle_lock.json"
F20_SUMMARY = Path(
    "stages/stage_frontier_20__train_only_feature_state_rule_atlas_onnx_scout/"
    "02_runs/frontier20B_feature_state_rule_atlas_proxy_scout_v1/final_summary.json"
)
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

ENTRY_FEATURE_LEFT = "vix_zscore_20"
ENTRY_FEATURE_RIGHT = "close_ema50_ratio"
ENTRY_LEFT_QUANTILE = 0.30
ENTRY_RIGHT_QUANTILE = 0.70
ENTRY_SIDE = 1
F20_VALIDATION_DD = 31.7443
F20_OOS_DD = 20.7766
SEED_PF = 1.20
SEED_VALIDATION_DD_CAP = 25.0
SEED_OOS_DD_CAP = 18.0
HANDOFF_PF = 1.50
HANDOFF_DD_CAP = 15.0


@dataclass(frozen=True)
class LifecycleProfile:
    profile_id: str
    role: str
    max_hold_bars: int
    atr_stop_multiplier: float
    atr_take_profit_multiplier: float
    cooldown_bars: int
    early_adverse_exit_enabled: bool


def main() -> int:
    ensure_dirs()
    created_at = utc_now()
    stage_open = read_json(F21A_SUMMARY)
    lock = read_json(F21A_LOCK)
    f20 = read_json(F20_SUMMARY)
    feature_order = read_feature_order()
    stage_context = validate_stage_context(stage_open, lock, feature_order)
    full, raw, source_integrity = f07b.load_training_packet()
    signal_context = build_fixed_entry_signal(full)
    result = run_lifecycle_grid(full, raw, profiles_from_lock(lock), signal_context)
    final = build_final(created_at, stage_open, lock, f20, feature_order, source_integrity, signal_context, result, stage_context)
    artifacts = write_artifacts(final, result)
    update_registries(final, artifacts)
    update_current_truth(final)
    print(json.dumps(json_ready({
        "status": final["status"],
        "judgment": final["judgment"],
        "run_id": RUN_ID,
        "scout_clue_rows": final["scout_clue_rows"],
        "seed_surface_rows": final["seed_surface_rows"],
        "handoff_candidate_rows": final["handoff_candidate_rows"],
        "best_profile_id": final["best_profile_id"],
        "next_run_id": final["next_run_id"],
        "report": REPORT_PATH.as_posix(),
    }), ensure_ascii=False, indent=2))
    return 0


def ensure_dirs() -> None:
    for path in (RUN_ROOT, STAGE_ROOT / "03_reviews", STAGE_ROOT / "04_selected"):
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_stage_context(stage_open: dict[str, Any], lock: dict[str, Any], feature_order: list[str]) -> dict[str, Any]:
    workspace = read_text(WORKSPACE_STATE)
    checks = {
        "workspace_current_stage_frontier21": f"current_stage_id: {STAGE_ID}" in workspace,
        "workspace_next_run_frontier21b": f"next_run_id: {RUN_ID}" in workspace,
        "stage_open_run_matches_parent": stage_open.get("run_id") == PARENT_RUN_ID,
        "entry_lock_present": lock.get("entry_lock", {}).get("definition") == "vix_zscore_20 <= q30 & close_ema50_ratio >= q70",
        "lifecycle_profile_cap_five": len(lock.get("lifecycle_grid", [])) == 5,
        "feature_order_hash_matches_contract": ordered_hash(feature_order) == EXPECTED_FEATURE_HASH,
        "feature_count_is_58": len(feature_order) == 58,
        "dataset_exists": path_exists(DATASET_PATH),
    }
    if not all(checks.values()):
        raise RuntimeError(f"Frontier21B context check failed: {json.dumps(checks, ensure_ascii=False)}")
    return {"checks": checks}


def profiles_from_lock(lock: dict[str, Any]) -> list[LifecycleProfile]:
    profiles: list[LifecycleProfile] = []
    for item in lock.get("lifecycle_grid", []):
        profiles.append(
            LifecycleProfile(
                profile_id=str(item["profile_id"]),
                role=str(item["role"]),
                max_hold_bars=int(item["max_hold_bars"]),
                atr_stop_multiplier=float(item["atr_stop_multiplier"]),
                atr_take_profit_multiplier=float(item["atr_take_profit_multiplier"]),
                cooldown_bars=int(item["cooldown_bars"]),
                early_adverse_exit_enabled=bool(item["early_adverse_exit_enabled"]),
            )
        )
    return profiles


def build_fixed_entry_signal(full: pd.DataFrame) -> dict[str, Any]:
    train_mask = full["split"].astype(str).eq("train")
    left_threshold = float(np.nanquantile(pd.to_numeric(full.loc[train_mask, ENTRY_FEATURE_LEFT], errors="coerce"), ENTRY_LEFT_QUANTILE))
    right_threshold = float(np.nanquantile(pd.to_numeric(full.loc[train_mask, ENTRY_FEATURE_RIGHT], errors="coerce"), ENTRY_RIGHT_QUANTILE))
    left = pd.to_numeric(full[ENTRY_FEATURE_LEFT], errors="coerce").to_numpy(dtype="float64")
    right = pd.to_numeric(full[ENTRY_FEATURE_RIGHT], errors="coerce").to_numpy(dtype="float64")
    signal = ((left <= left_threshold) & (right >= right_threshold)).astype("int64") * ENTRY_SIDE
    return {
        "signal": signal,
        "left_threshold": left_threshold,
        "right_threshold": right_threshold,
        "definition": "vix_zscore_20 <= q30 & close_ema50_ratio >= q70",
        "side": "long(롱)",
        "selection_boundary": "train_quantiles_from_fixed_F20_rule_then_forward_read_only(F20 고정 규칙의 학습 분위수, 이후 전진 읽기 전용)",
    }


def run_lifecycle_grid(
    full: pd.DataFrame,
    raw: pd.DataFrame,
    profiles: list[LifecycleProfile],
    signal_context: dict[str, Any],
) -> dict[str, Any]:
    signal = np.asarray(signal_context["signal"], dtype="int64")
    trade_rows: list[dict[str, Any]] = []
    metric_rows: list[dict[str, Any]] = []
    subperiod_rows: list[dict[str, Any]] = []
    for profile in profiles:
        trades = simulate_profile(full, raw, signal, profile)
        trade_rows.extend(trades)
        metric_rows.extend(evaluate_aggregates(trades, profile))
        subperiod_rows.extend(evaluate_subperiods(trades, profile))
    metrics = pd.DataFrame(metric_rows)
    subperiods = pd.DataFrame(subperiod_rows)
    summary = summarize_profiles(metrics, subperiods)
    return {
        "trades": trade_rows,
        "metrics": metric_rows,
        "subperiod_metrics": subperiod_rows,
        "candidate_summary": summary.to_dict(orient="records"),
    }


def simulate_profile(full: pd.DataFrame, raw: pd.DataFrame, signal: np.ndarray, profile: LifecycleProfile) -> list[dict[str, Any]]:
    trades: list[dict[str, Any]] = []
    for split in ("train", "validation", "oos"):
        split_indexes = np.flatnonzero(full["split"].astype(str).eq(split).to_numpy())
        trades.extend(simulate_split(full, raw, signal, profile, split_indexes, split))
    return trades


def simulate_split(
    full: pd.DataFrame,
    raw: pd.DataFrame,
    signal: np.ndarray,
    profile: LifecycleProfile,
    split_indexes: np.ndarray,
    split: str,
) -> list[dict[str, Any]]:
    if len(split_indexes) == 0:
        return []
    raw_open = raw["open"].astype("float64").to_numpy()
    raw_high = raw["high"].astype("float64").to_numpy()
    raw_low = raw["low"].astype("float64").to_numpy()
    raw_close = raw["close"].astype("float64").to_numpy()
    max_raw_index = int(full.iloc[split_indexes]["raw_index"].max())
    trades: list[dict[str, Any]] = []
    position: dict[str, Any] | None = None
    cooldown_until = -1

    for row_index in split_indexes:
        row = full.iloc[int(row_index)]
        raw_index = int(row["raw_index"])
        row_signal = int(signal[int(row_index)])
        if position is not None and raw_index >= int(position["entry_raw_index"]):
            exit_event = maybe_exit_position(position, raw_index, raw_high, raw_low, raw_close, profile)
            if exit_event is not None:
                trades.append(close_trade(position, exit_event, row, profile, split))
                position = None
                cooldown_until = int(exit_event["exit_raw_index"]) + int(profile.cooldown_bars)
        if position is None and row_signal != 0 and raw_index > cooldown_until and can_open(raw_index, max_raw_index, profile, raw_open):
            position = open_position(row_signal, raw_index, row_index, row, raw_open, profile)

    if position is not None:
        last_row = full.iloc[int(split_indexes[-1])]
        last_raw = min(max_raw_index, len(raw_close) - 1)
        event = {"exit_raw_index": last_raw, "exit_price": float(raw_close[last_raw]), "reason": "split_end_forced_close"}
        trades.append(close_trade(position, event, last_row, profile, split))
    return trades


def can_open(raw_index: int, max_raw_index: int, profile: LifecycleProfile, raw_open: np.ndarray) -> bool:
    entry_raw = raw_index + 1
    if entry_raw >= len(raw_open):
        return False
    return entry_raw + profile.max_hold_bars <= max_raw_index


def open_position(
    side: int,
    raw_index: int,
    row_index: int,
    row: pd.Series,
    raw_open: np.ndarray,
    profile: LifecycleProfile,
) -> dict[str, Any]:
    entry_raw = raw_index + 1
    entry_price = float(raw_open[entry_raw])
    atr_value = float(row["atr_14"])
    if not math.isfinite(atr_value) or atr_value <= 0.0:
        atr_value = max(abs(entry_price) * 0.001, 1.0)
    return {
        "side": int(side),
        "entry_raw_index": int(entry_raw),
        "entry_signal_row_index": int(row_index),
        "entry_signal_timestamp": str(row["timestamp"]),
        "entry_price": entry_price,
        "entry_atr": atr_value,
        "stop_distance": atr_value * profile.atr_stop_multiplier,
        "take_profit_distance": atr_value * profile.atr_take_profit_multiplier,
    }


def maybe_exit_position(
    position: dict[str, Any],
    raw_index: int,
    raw_high: np.ndarray,
    raw_low: np.ndarray,
    raw_close: np.ndarray,
    profile: LifecycleProfile,
) -> dict[str, Any] | None:
    side = int(position["side"])
    entry_raw = int(position["entry_raw_index"])
    age_bars = raw_index - entry_raw + 1
    entry_price = float(position["entry_price"])
    stop = float(position["stop_distance"])
    take_profit = float(position["take_profit_distance"])

    if stop > 0.0:
        stop_price = entry_price - stop if side > 0 else entry_price + stop
        stop_hit = float(raw_low[raw_index]) <= stop_price if side > 0 else float(raw_high[raw_index]) >= stop_price
        if stop_hit:
            return {"exit_raw_index": raw_index, "exit_price": stop_price, "reason": "atr_stop"}
    if take_profit > 0.0:
        take_profit_price = entry_price + take_profit if side > 0 else entry_price - take_profit
        take_hit = float(raw_high[raw_index]) >= take_profit_price if side > 0 else float(raw_low[raw_index]) <= take_profit_price
        if take_hit:
            return {"exit_raw_index": raw_index, "exit_price": take_profit_price, "reason": "atr_take_profit"}
    if profile.early_adverse_exit_enabled and stop > 0.0 and age_bars >= 2:
        unrealized = side * (math.log(float(raw_close[raw_index])) - math.log(entry_price))
        risk_floor = -0.55 * math.log1p(stop / max(entry_price, 1e-12))
        if unrealized <= risk_floor:
            return {"exit_raw_index": raw_index, "exit_price": float(raw_close[raw_index]), "reason": "early_adverse_exit"}
    if age_bars >= profile.max_hold_bars:
        return {"exit_raw_index": raw_index, "exit_price": float(raw_close[raw_index]), "reason": "max_hold"}
    return None


def close_trade(
    position: dict[str, Any],
    event: dict[str, Any],
    row: pd.Series,
    profile: LifecycleProfile,
    split: str,
) -> dict[str, Any]:
    side = int(position["side"])
    entry_price = float(position["entry_price"])
    exit_price = float(event["exit_price"])
    gross_log_return = side * (math.log(exit_price) - math.log(entry_price))
    net_log_return = gross_log_return - scout.ROUGH_COST_LOG_RETURN
    return {
        "profile_id": profile.profile_id,
        "profile_role": profile.role,
        "split": split,
        "entry_signal_timestamp": position["entry_signal_timestamp"],
        "exit_signal_timestamp": str(row["timestamp"]),
        "entry_raw_index": int(position["entry_raw_index"]),
        "exit_raw_index": int(event["exit_raw_index"]),
        "side": side,
        "entry_price": entry_price,
        "exit_price": exit_price,
        "entry_atr": float(position["entry_atr"]),
        "hold_bars": int(event["exit_raw_index"]) - int(position["entry_raw_index"]) + 1,
        "exit_reason": event["reason"],
        "gross_log_return": gross_log_return,
        "net_log_return": net_log_return,
        "proxy_cost_log_return": scout.ROUGH_COST_LOG_RETURN,
        "execution_boundary": "closed_bar_signal_next_bar_open_proxy_stop_first_when_same_bar_ambiguous(종료봉 신호 다음 봉 시가 프록시, 같은 봉 동시 충돌은 손절 우선)",
    }


def evaluate_aggregates(trades: list[dict[str, Any]], profile: LifecycleProfile) -> list[dict[str, Any]]:
    return [evaluate_trade_rows(trades, profile, split, "aggregate", split) for split in ("train", "validation", "oos")]


def evaluate_trade_rows(
    trades: list[dict[str, Any]],
    profile: LifecycleProfile,
    split: str,
    granularity: str,
    period: str,
) -> dict[str, Any]:
    selected = [
        row for row in trades
        if row["profile_id"] == profile.profile_id
        and row["split"] == split
        and (granularity == "aggregate" or row.get("period") == period)
    ]
    pnl = np.asarray([float(row["net_log_return"]) for row in selected], dtype="float64")
    times = pd.Series([row["entry_signal_timestamp"] for row in selected], dtype="object")
    metrics = scout.trade_metrics(pnl, pd.to_datetime(times, utc=True)) if len(selected) else scout.trade_metrics(pnl, pd.Series([], dtype="datetime64[ns, UTC]"))
    days = count_days_for_trade_set(selected)
    trade_count = int(len(selected))
    trades_per_day = float(trade_count / days) if days else 0.0
    sparse_floor = max(5, int(math.ceil(days / 2))) if days else 5
    sparse_flag = trade_count < sparse_floor
    pf999_sparse_flag = bool(float(metrics["profit_factor"]) >= 999.0 and sparse_flag)
    dd_risk = max(float(metrics["max_drawdown_percent"]), float(metrics["max_monthly_drawdown_percent"]))
    density_distance = scout.density_axis_distance(trades_per_day)
    pf_distance = scout.profit_factor_axis_distance(float(metrics["profit_factor"]), trade_count, sparse_flag, pf999_sparse_flag)
    dd_distance = max(0.0, (dd_risk - scout.DD_TARGET_PERCENT) / scout.DD_TARGET_PERCENT)
    smoothness_distance = scout.smoothness_axis_distance(metrics)
    return {
        "profile_id": profile.profile_id,
        "profile_role": profile.role,
        "split": split,
        "granularity": granularity,
        "period": period,
        "tier_scope": "Tier A(티어 A)",
        "record_view": "Tier A separate(티어 A 분리)",
        "max_hold_bars": profile.max_hold_bars,
        "atr_stop_multiplier": profile.atr_stop_multiplier,
        "atr_take_profit_multiplier": profile.atr_take_profit_multiplier,
        "cooldown_bars": profile.cooldown_bars,
        "early_adverse_exit_enabled": profile.early_adverse_exit_enabled,
        "trade_count": trade_count,
        "days_in_scope": days,
        "trades_per_day": trades_per_day,
        "long_trade_count": int(sum(1 for row in selected if int(row["side"]) > 0)),
        "short_trade_count": int(sum(1 for row in selected if int(row["side"]) < 0)),
        "net_profit": metrics["net_profit"],
        "profit_factor": metrics["profit_factor"],
        "expectancy": metrics["expectancy"],
        "win_rate": metrics["win_rate"],
        "max_drawdown_percent": metrics["max_drawdown_percent"],
        "max_monthly_drawdown_percent": metrics["max_monthly_drawdown_percent"],
        "dd_risk_percent": dd_risk,
        "underwater_ratio": metrics["underwater_ratio"],
        "max_loss_streak": metrics["max_loss_streak"],
        "equity_trend_r2": metrics["equity_trend_r2"],
        "sparse_flag": bool(sparse_flag),
        "pf999_sparse_flag": bool(pf999_sparse_flag),
        "density_axis_distance": density_distance,
        "pf_axis_distance": pf_distance,
        "dd_axis_distance": dd_distance,
        "smoothness_axis_distance": smoothness_distance,
        "aspiration_distance_score": density_distance + pf_distance + dd_distance + smoothness_distance,
        "proxy_cost_log_return": scout.ROUGH_COST_LOG_RETURN,
    }


def evaluate_subperiods(trades: list[dict[str, Any]], profile: LifecycleProfile) -> list[dict[str, Any]]:
    profile_trades = [row for row in trades if row["profile_id"] == profile.profile_id]
    if not profile_trades:
        return []
    frame = pd.DataFrame(profile_trades)
    times = pd.to_datetime(frame["entry_signal_timestamp"], utc=True).dt.tz_convert("America/New_York").dt.tz_localize(None)
    frame["month_period"] = times.dt.to_period("M").astype(str)
    frame["quarter_period"] = times.dt.to_period("Q").astype(str)
    rows: list[dict[str, Any]] = []
    for split in ("train", "validation", "oos"):
        split_frame = frame.loc[frame["split"].astype(str).eq(split)].copy()
        for column, granularity in (("month_period", "month"), ("quarter_period", "quarter")):
            for period in sorted(split_frame[column].dropna().unique()):
                marked = [dict(row) for row in split_frame.loc[split_frame[column].eq(period)].to_dict(orient="records")]
                for item in marked:
                    item["period"] = str(period)
                rows.append(evaluate_trade_rows(marked, profile, split, granularity, str(period)))
    return rows


def count_days_for_trade_set(trades: list[dict[str, Any]]) -> int:
    if not trades:
        return 0
    times = pd.Series([row["entry_signal_timestamp"] for row in trades])
    return scout.count_scope_days(pd.to_datetime(times, utc=True))


def summarize_profiles(metrics: pd.DataFrame, subperiods: pd.DataFrame) -> pd.DataFrame:
    baseline_id = "f21b_sim_baseline_hold12_no_stop"
    baseline_rows = metrics.loc[metrics["profile_id"].eq(baseline_id)]
    ref = {row["split"]: dict(row) for _, row in baseline_rows.iterrows()}
    rows: list[dict[str, Any]] = []
    for profile_id, group in metrics.groupby("profile_id", sort=False):
        train = split_row(group, "train")
        validation = split_row(group, "validation")
        oos = split_row(group, "oos")
        base = {
            "profile_id": profile_id,
            "profile_role": train["profile_role"],
            "max_hold_bars": train["max_hold_bars"],
            "atr_stop_multiplier": train["atr_stop_multiplier"],
            "atr_take_profit_multiplier": train["atr_take_profit_multiplier"],
            "cooldown_bars": train["cooldown_bars"],
            "early_adverse_exit_enabled": train["early_adverse_exit_enabled"],
            "selection_boundary": "pre_registered_capped_grid_train_rank_forward_read_only(사전 등록 상한 격자, 학습 순위와 전진 읽기 전용)",
        }
        for prefix, row in (("train", train), ("validation", validation), ("oos", oos)):
            for field in (
                "trade_count",
                "trades_per_day",
                "net_profit",
                "profit_factor",
                "expectancy",
                "win_rate",
                "dd_risk_percent",
                "underwater_ratio",
                "max_loss_streak",
                "equity_trend_r2",
                "smoothness_axis_distance",
                "aspiration_distance_score",
            ):
                base[f"{prefix}_{field}"] = row[field]
        base["validation_dd_reduction_vs_f20_report"] = F20_VALIDATION_DD - float(validation["dd_risk_percent"])
        base["oos_dd_reduction_vs_f20_report"] = F20_OOS_DD - float(oos["dd_risk_percent"])
        base["validation_dd_reduction_vs_sim_baseline"] = float(ref.get("validation", {}).get("dd_risk_percent", np.nan)) - float(validation["dd_risk_percent"])
        base["oos_dd_reduction_vs_sim_baseline"] = float(ref.get("oos", {}).get("dd_risk_percent", np.nan)) - float(oos["dd_risk_percent"])
        base["validation_smoothness_improvement_vs_sim_baseline"] = float(ref.get("validation", {}).get("smoothness_axis_distance", np.nan)) - float(validation["smoothness_axis_distance"])
        base["oos_smoothness_improvement_vs_sim_baseline"] = float(ref.get("oos", {}).get("smoothness_axis_distance", np.nan)) - float(oos["smoothness_axis_distance"])
        base["forward_subperiod_worst_dd"] = worst_subperiod_dd(subperiods, profile_id)
        base["scout_clue_flag"] = bool(
            float(validation["net_profit"]) > 0
            and float(oos["net_profit"]) > 0
            and 4.0 <= float(validation["trades_per_day"]) <= 12.0
            and 4.0 <= float(oos["trades_per_day"]) <= 12.0
            and float(validation["dd_risk_percent"]) < F20_VALIDATION_DD
            and float(oos["dd_risk_percent"]) < F20_OOS_DD
            and float(oos["profit_factor"]) >= 1.0
        )
        base["seed_surface_flag"] = bool(
            scout.DENSITY_TARGET_LOW <= float(validation["trades_per_day"]) <= scout.DENSITY_TARGET_HIGH
            and scout.DENSITY_TARGET_LOW <= float(oos["trades_per_day"]) <= scout.DENSITY_TARGET_HIGH
            and float(validation["profit_factor"]) >= SEED_PF
            and float(oos["profit_factor"]) >= SEED_PF
            and float(validation["dd_risk_percent"]) <= SEED_VALIDATION_DD_CAP
            and float(oos["dd_risk_percent"]) <= SEED_OOS_DD_CAP
            and float(validation["net_profit"]) > 0
            and float(oos["net_profit"]) > 0
        )
        base["handoff_candidate_flag"] = bool(
            scout.DENSITY_TARGET_LOW <= float(validation["trades_per_day"]) <= scout.DENSITY_TARGET_HIGH
            and scout.DENSITY_TARGET_LOW <= float(oos["trades_per_day"]) <= scout.DENSITY_TARGET_HIGH
            and float(validation["profit_factor"]) >= HANDOFF_PF
            and float(oos["profit_factor"]) >= HANDOFF_PF
            and float(validation["dd_risk_percent"]) <= HANDOFF_DD_CAP
            and float(oos["dd_risk_percent"]) <= HANDOFF_DD_CAP
            and float(base["validation_smoothness_improvement_vs_sim_baseline"]) > 0
            and float(base["oos_smoothness_improvement_vs_sim_baseline"]) > 0
        )
        base["forward_read_score"] = float(
            min(float(validation["profit_factor"]), 3.0)
            * min(float(oos["profit_factor"]), 3.0)
            * min(float(validation["trades_per_day"]), float(oos["trades_per_day"]), 12.0)
            / (1.0 + max(float(validation["dd_risk_percent"]), float(oos["dd_risk_percent"])) / 15.0)
        )
        rows.append(base)
    return pd.DataFrame(rows).sort_values(
        ["handoff_candidate_flag", "seed_surface_flag", "scout_clue_flag", "forward_read_score"],
        ascending=[False, False, False, False],
    )


def worst_subperiod_dd(subperiods: pd.DataFrame, profile_id: str) -> float:
    if subperiods.empty:
        return 0.0
    forward = subperiods.loc[
        subperiods["profile_id"].eq(profile_id)
        & subperiods["split"].isin(["validation", "oos"])
        & subperiods["granularity"].isin(["month", "quarter"])
    ]
    if forward.empty:
        return 0.0
    return float(forward["dd_risk_percent"].max())


def split_row(group: pd.DataFrame, split: str) -> dict[str, Any]:
    row = group.loc[group["split"].eq(split)]
    if row.empty:
        raise ValueError(f"Missing split row(분할 행 누락): {split}")
    return dict(row.iloc[0])


def build_final(
    created_at: str,
    stage_open: dict[str, Any],
    lock: dict[str, Any],
    f20: dict[str, Any],
    feature_order: list[str],
    source_integrity: dict[str, Any],
    signal_context: dict[str, Any],
    result: dict[str, Any],
    stage_context: dict[str, Any],
) -> dict[str, Any]:
    summary = pd.DataFrame(result["candidate_summary"])
    handoff_count = int(summary["handoff_candidate_flag"].sum()) if not summary.empty else 0
    seed_count = int(summary["seed_surface_flag"].sum()) if not summary.empty else 0
    scout_count = int(summary["scout_clue_flag"].sum()) if not summary.empty else 0
    best = dict(summary.iloc[0]) if not summary.empty else {}
    if handoff_count:
        status = "lifecycle_handoff_candidate_proxy_needs_pre_expensive_grok_no_authority"
        judgment = "handoff_candidate_proxy_observation(인계 후보 프록시 관찰)"
        next_run_id = NEXT_PRE_EXPENSIVE_GROK_RUN_ID
    elif seed_count:
        status = "lifecycle_seed_surface_proxy_no_runtime_no_authority"
        judgment = "seed_surface(씨앗 표면)"
        next_run_id = NEXT_REPAIR_OR_CLOSEOUT_RUN_ID
    elif scout_count:
        status = "lifecycle_scout_clue_proxy_no_runtime_no_authority"
        judgment = "scout_clue(탐색 단서)"
        next_run_id = NEXT_REPAIR_OR_CLOSEOUT_RUN_ID
    else:
        status = "lifecycle_proxy_no_forward_clue_repair_or_closeout_required"
        judgment = "negative_pressure_needs_repair_or_closeout(부정 압력, 수리 또는 마감 필요)"
        next_run_id = NEXT_REPAIR_OR_CLOSEOUT_RUN_ID
    return {
        "created_at_utc": created_at,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": next_run_id,
        "status": status,
        "judgment": judgment,
        "stage_open_run": stage_open.get("run_id"),
        "feature_count": len(feature_order),
        "feature_order_hash": ordered_hash(feature_order),
        "source_integrity": source_integrity,
        "stage_context": stage_context,
        "entry_signal": {
            key: value for key, value in signal_context.items() if key != "signal"
        },
        "f20_reference": f20_reference(f20),
        "profile_count": len(lock.get("lifecycle_grid", [])),
        "metric_rows": len(result["metrics"]),
        "subperiod_metric_rows": len(result["subperiod_metrics"]),
        "trade_rows": len(result["trades"]),
        "scout_clue_rows": scout_count,
        "seed_surface_rows": seed_count,
        "handoff_candidate_rows": handoff_count,
        "best_profile_id": best.get("profile_id", ""),
        "best_profile": best,
        "result_boundary": "proxy_only_no_wfo_no_mt5_no_runtime_authority(프록시 전용, WFO/MT5/런타임 권위 없음)",
        "runtime_probe_status": "pre_expensive_grok_required_before_mt5(비싼 MT5 전 그록 검토 필요)" if handoff_count else "out_of_scope_by_claim_no_handoff_candidate_yet(인계 후보 전이라 주장 범위 밖)",
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def f20_reference(f20: dict[str, Any]) -> dict[str, Any]:
    best = f20.get("best_candidate", {})
    return {
        "candidate_id": best.get("candidate_id"),
        "rule_definition": best.get("rule_definition"),
        "side": best.get("side"),
        "validation_profit_factor": best.get("validation_profit_factor"),
        "validation_trades_per_day": best.get("validation_trades_per_day"),
        "validation_dd_risk": best.get("validation_dd_risk"),
        "oos_profit_factor": best.get("oos_profit_factor"),
        "oos_trades_per_day": best.get("oos_trades_per_day"),
        "oos_dd_risk": best.get("oos_dd_risk"),
    }


def write_artifacts(final: dict[str, Any], result: dict[str, Any]) -> dict[str, Path]:
    artifacts = {
        "run_manifest": RUN_ROOT / "run_manifest.json",
        "final_summary": RUN_ROOT / "final_summary.json",
        "candidate_summary": RUN_ROOT / "candidate_summary.csv",
        "metrics_by_split": RUN_ROOT / "metrics_by_split.csv",
        "subperiod_metrics": RUN_ROOT / "subperiod_metrics.csv",
        "trade_log": RUN_ROOT / "trade_log.csv",
        "report": REPORT_PATH,
        "gate_audit": STAGE_ROOT / "03_reviews" / f"{RUN_ID}_gate_audit.md",
    }
    write_json(artifacts["run_manifest"], run_manifest(final, artifacts))
    write_json(artifacts["final_summary"], final)
    write_csv(artifacts["candidate_summary"], result["candidate_summary"])
    write_csv(artifacts["metrics_by_split"], result["metrics"])
    write_csv(artifacts["subperiod_metrics"], result["subperiod_metrics"])
    write_csv(artifacts["trade_log"], result["trades"])
    f03b.write_text_sig(REPORT_PATH, report_text(final, artifacts))
    f03b.write_text_sig(artifacts["gate_audit"], gate_audit(final, artifacts))
    return artifacts


def run_manifest(final: dict[str, Any], artifacts: dict[str, Path]) -> dict[str, Any]:
    return {
        "identity": {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": final["next_run_id"],
            "created_at_utc": final["created_at_utc"],
        },
        "artifacts": [
            artifact_identity(SCRIPT_PATH),
            artifact_identity(DATASET_PATH),
            artifact_identity(FEATURE_ORDER_PATH),
            artifact_identity(F21A_LOCK),
            artifact_identity(F20_SUMMARY),
            *[artifact_identity(path) for path in artifacts.values() if path != artifacts["run_manifest"]],
        ],
        "feature_schema": {
            "feature_count": final["feature_count"],
            "feature_order_hash": final["feature_order_hash"],
            "feature_order_path": FEATURE_ORDER_PATH.as_posix(),
        },
        "runtime_snapshot": {
            "symbol": "US100",
            "timeframe": "M5",
            "entry_timing": "next_bar_open_proxy(다음 봉 시가 프록시)",
            "max_concurrent_positions": 1,
            "cost_behavior": "rough_log_return_cost_proxy_only(거친 로그수익률 비용 프록시 전용)",
        },
        "rule_stack": {
            "entry": final["entry_signal"],
            "position_exit": "pre_registered_lifecycle_grid(사전 등록 생명주기 격자)",
        },
        "results": {
            "by_split": {"proxy": "metrics_by_split.csv"},
            "cross_split": {
                "scout_clue_rows": final["scout_clue_rows"],
                "seed_surface_rows": final["seed_surface_rows"],
                "handoff_candidate_rows": final["handoff_candidate_rows"],
                "best_profile_id": final["best_profile_id"],
            },
            "report_refs": [{"role": "proxy_report", "path": REPORT_PATH.as_posix()}],
        },
        "compatibility": {
            "schema_version": "frontier21b_proxy_v1",
            "mismatch_policy": "fail_fast(빠른 실패)",
            "required_output_schema": "not_applicable_no_onnx_export_yet(ONNX 내보내기 전이라 해당 없음)",
        },
    }


def report_text(final: dict[str, Any], artifacts: dict[str, Path]) -> str:
    best = final["best_profile"]
    return f"""# Frontier21B F20 Seed Lifecycle Proxy Scout Report(전선21B F20 씨앗 생명주기 프록시 탐색 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Action(행동): fixed F20 entry(고정 F20 진입)에 5개 pre-registered lifecycle profiles(사전 등록 생명주기 프로필)를 적용했습니다.

Effect(효과): DD(손실폭) 변화가 entry retuning(진입 재조정)이 아니라 lifecycle/risk stack(생명주기/위험 묶음)에서 왔는지 분리했습니다.

Entry signal(진입 신호): `{final['entry_signal']['definition']}`, `{final['entry_signal']['side']}`

Scout/seed/handoff rows(탐색/씨앗/인계 행): `{final['scout_clue_rows']}` / `{final['seed_surface_rows']}` / `{final['handoff_candidate_rows']}`

Best profile by forward read(전진 읽기 기준 최상 프로필): `{final['best_profile_id']}`

Best validation PF/density/DD(최상 검증 수익 팩터/빈도/손실폭): `{fmt(best.get('validation_profit_factor'))}` / `{fmt(best.get('validation_trades_per_day'))}/day` / `{fmt(best.get('validation_dd_risk_percent'))}%`

Best OOS PF/density/DD(최상 표본외 수익 팩터/빈도/손실폭): `{fmt(best.get('oos_profit_factor'))}` / `{fmt(best.get('oos_trades_per_day'))}/day` / `{fmt(best.get('oos_dd_risk_percent'))}%`

DD reduction vs F20 report(전선20 보고 대비 손실폭 감소): validation(검증) `{fmt(best.get('validation_dd_reduction_vs_f20_report'))}`, OOS(표본외) `{fmt(best.get('oos_dd_reduction_vs_f20_report'))}`.

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

Artifacts(산출물): `{artifacts['candidate_summary'].as_posix()}`, `{artifacts['metrics_by_split'].as_posix()}`, `{artifacts['trade_log'].as_posix()}`

Next action(다음 행동): `{final['next_run_id']}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def gate_audit(final: dict[str, Any], artifacts: dict[str, Path]) -> str:
    return f"""# Frontier21B Gate Audit(전선21B 게이트 감사)

- scope_completion_gate(범위 완료 게이트): proxy artifacts created(프록시 산출물 생성) `{artifacts['final_summary'].as_posix()}`
- kpi_contract_audit(KPI 계약 감사): metrics_by_split/candidate_summary/trade_log(분할 지표/후보 요약/거래 기록) created(생성)
- skill_receipt_lint(스킬 영수증 점검): F21A Grok receipt(전선21A 그록 영수증) reused, F21B report(보고서) records claim boundary(주장 경계 기록)
- required_gate_coverage_audit(필수 게이트 커버리지 감사): this file(이 파일)
- final_claim_guard(최종 주장 방지): runtime authority/operating promotion/Goal Achieve(런타임 권위/운영 승격/목표 달성) not_claimed(주장 없음)
"""


def update_registries(final: dict[str, Any], artifacts: dict[str, Path]) -> None:
    f03b.upsert_csv(RUN_REGISTRY, "run_id", run_registry_row(final))
    for row in ledger_rows(final):
        f03b.upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
        f03b.upsert_csv(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", row)
    f03b.append_once(CHANGELOG, RUN_ID, changelog_entry(final))
    f03b.append_once(IDEA_REGISTRY, RUN_ID, idea_registry_entry(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(final))


def run_registry_row(final: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "experiment_execution(실험 실행)",
        "family": "experiment_execution(실험 실행)",
        "work_family": "experiment_execution(실험 실행)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"scout={final['scout_clue_rows']};seed={final['seed_surface_rows']};handoff={final['handoff_candidate_rows']};next={final['next_run_id']}",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": final["next_run_id"],
        "claim_boundary": final["result_boundary"],
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": final["created_at_utc"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "result_path": REPORT_PATH.as_posix(),
    }


def ledger_rows(final: dict[str, Any]) -> list[dict[str, Any]]:
    best = final["best_profile"]
    primary = {
        "ledger_row_id": f"{RUN_ID}__tier_a_lifecycle_proxy",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__tier_a_lifecycle_proxy",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "Tier A separate(티어 A 분리)",
        "tier_scope": "Tier A(티어 A)",
        "kpi_scope": "lifecycle_proxy_not_runtime(생명주기 프록시, 런타임 아님)",
        "scoreboard_lane": "trade_shape_proxy(거래 형태 프록시)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": (
            f"best={final['best_profile_id']};"
            f"oos_pf={fmt(best.get('oos_profit_factor'))};"
            f"oos_density={fmt(best.get('oos_trades_per_day'))};"
            f"oos_dd={fmt(best.get('oos_dd_risk_percent'))}"
        ),
        "guardrail_kpi": "proxy_only_no_wfo_no_mt5_no_authority(프록시 전용, WFO/MT5/권위 없음)",
        "external_verification_status": final["runtime_probe_status"],
        "notes": f"scout={final['scout_clue_rows']};seed={final['seed_surface_rows']};handoff={final['handoff_candidate_rows']}",
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


def selection_status(final: dict[str, Any]) -> str:
    return f"""# Frontier21 Selection Status(전선21 선택 상태)

Updated(갱신): {final['created_at_utc']}

Selection(선택): no selected baseline/completion/promotion/runtime authority(선택 기준선/완성/승격/런타임 권위 없음).

Latest proxy(최근 프록시): `{RUN_ID}`

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Best profile(최상 프로필): `{final['best_profile_id']}`

Scout/seed/handoff rows(탐색/씨앗/인계 행): `{final['scout_clue_rows']}` / `{final['seed_surface_rows']}` / `{final['handoff_candidate_rows']}`

Next action(다음 행동): `{final['next_run_id']}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 not_claimed(주장 없음)입니다.
"""


def changelog_entry(final: dict[str, Any]) -> str:
    return (
        f"- {final['created_at_utc']}: `{RUN_ID}` ran fixed F20 seed lifecycle proxy scout(고정 F20 씨앗 생명주기 프록시 탐색). "
        f"Effect(효과): scout/seed/handoff(탐색/씨앗/인계) counts are {final['scout_clue_rows']}/{final['seed_surface_rows']}/{final['handoff_candidate_rows']} and next run(다음 실행) is `{final['next_run_id']}`.\n"
    )


def idea_registry_entry(final: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR21-F20-SEED-LIFECYCLE-DD-CONTAINMENT-ONNX-SCOUT`: `{RUN_ID}` tested capped lifecycle profiles(상한 생명주기 프로필) on the fixed F20 seed(고정 F20 씨앗). "
        f"Effect(효과): best profile `{final['best_profile_id']}` is proxy-only(프록시 전용) and not authority(권위 아님).\n"
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
    best = final["best_profile"]
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

## Active Stage(현재 단계)

- stage(단계): `{STAGE_ID}`
- latest run(최근 실행): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- next run(다음 실행): `{final['next_run_id']}`

## Current Truth(현재 진실)

Action(행동): F21B(전선21B)가 fixed F20 seed lifecycle proxy(고정 F20 씨앗 생명주기 프록시)를 실행했습니다.

Effect(효과): 생명주기 프로필이 DD(손실폭), PF(수익 팩터), density(빈도)를 어떻게 바꾸는지 proxy-only(프록시 전용) 근거로 분리했습니다.

Best profile(최상 프로필): `{final['best_profile_id']}` with validation/OOS PF-density-DD(검증/표본외 수익 팩터-빈도-손실폭) `{fmt(best.get('validation_profit_factor'))}/{fmt(best.get('validation_trades_per_day'))}/{fmt(best.get('validation_dd_risk_percent'))}` and `{fmt(best.get('oos_profit_factor'))}/{fmt(best.get('oos_trades_per_day'))}/{fmt(best.get('oos_dd_risk_percent'))}`.

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def artifact_identity(path: Path) -> dict[str, str]:
    return {"path": path.as_posix(), "sha256": sha256_file(path) if path_exists(path) else "pending_or_missing(대기 또는 누락)"}


def read_feature_order() -> list[str]:
    return [line.strip() for line in io_path(FEATURE_ORDER_PATH).read_text(encoding="utf-8-sig").splitlines() if line.strip()]


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    if not rows:
        io_path(path).write_text("", encoding="utf-8-sig")
        return
    header = list(rows[0].keys())
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=header, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: f03b.stringify(row.get(column, "")) for column in header})


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
